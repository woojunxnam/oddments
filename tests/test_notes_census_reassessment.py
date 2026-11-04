"""Census-only remediation keeps negative history and requires fresh current review."""
import copy
import json
import subprocess

import pytest

from test_note_review_queue import (repo, claimed, worker_result, integrate_files, NOW, LATER)
import note_review_queue as queue
import notes_census_reassessment as revisions
from notes_independent_metadata import load_metadata

RECORD = 'reports/full-corpus-review/fixture-reassessment-v1.json'
REPLACEMENT = 'reports/full-corpus-review/fixture-census-v2.json'


def authority(path):
    return dict(source_type='PUBLIC_OFFICIAL',official_url='https://example.gov/statute',exact_section='section 1',
        law_checked_date='2026-11-03',version_or_effective_date_status='current fixture',evidence_path=path,
        evidence_sha256=queue.raw_sha(b'Official fixture authority bytes'))


def commit(root,message):
    queue.git(root,'add','.'); queue.git(root,'commit','-qm',message)


def persist(root,state):
    (root/queue.STATE).write_bytes(queue.encoded(state)); commit(root,'checkpoint')


@pytest.fixture
def remediation(repo,request):
    root,notes,inv = repo; state,old = claimed(repo)
    def omissions(report):
        mode = getattr(request,'param',1)
        count = mode['count'] if isinstance(mode,dict) else mode
        for row in report['records'][:count]:
            row.update(completeness='OMISSIONS_FOUND',omissions=['Omitted operational clock'],legal_status='LEGAL_HOLD')
        report['records'][0]['claims'][0]['legal_status'] = 'LEGAL_HOLD'
        if isinstance(mode,dict) and mode.get('legal') == 'KEEP':
            path = queue.OUTPUT+'fixture-official.txt'
            target = root.parent/'worker-1'/path; target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text('Official fixture authority bytes')
            for row in report['records']:
                row['legal_status'] = 'LEGAL_HOLD' if row['omissions'] else 'KEEP'
                for claim in row['claims']:
                    claim.update(legal_status='KEEP',authorities=[authority(path)])
                    claim.pop('blocker')
    result,worker = worker_result(repo,state,old,omissions)
    queue.submit(state,old['job_id'],old['lease_token'],queue.encoded(result),root,inv,NOW)
    integrate_files(root,result); queue.integrate(state,old['job_id'],root,inv,NOW); persist(root,state)
    uid = old['unit_ids'][0]; binding = old['unit_bindings'][uid]
    census = json.loads((root/binding['census_path']).read_bytes())
    replacement = dict(census,author_provenance={'actor_id':'correction-author','session_id':'correction-session'},
                       units=[copy.deepcopy(census['units'][0])],
                       claims=[copy.deepcopy(c) for c in census['claims'] if c['unit_id'] == uid],sources={})
    replacement['units'][0].update(claim_count=3,
        census_status='COMPLETE_AUTHOR_ENUMERATION_PENDING_INDEPENDENT_COMPLETENESS_CHECK')
    extra = dict(replacement['claims'][0],claim_id=uid+'-added-clock',statement_ko='New omitted operational clock')
    replacement['claims'].append(extra)
    (root/REPLACEMENT).write_bytes(queue.encoded(replacement))
    row = next(json.loads(x) for x in (root/queue.LEDGER).read_text().splitlines() if json.loads(x)['unit_id'] == uid)
    spec = dict(schema_version=1,purpose=revisions.PURPOSE,reassessment_id='clock-census-v2',unit_id=uid,
        body_sha256=binding['body_sha256'],previous_job_id=old['job_id'],previous_job_sha256=queue.digest(old),
        previous_binding=copy.deepcopy(binding),previous_result={'path':result['result_path'],'raw_sha256':old['result_sha256']},
        previous_report=copy.deepcopy(result['evidence']),
        previous_ledger_fields={k:row.get(k) for k in revisions.LEDGER_FIELDS},
        replacement={'census_path':REPLACEMENT,'census_sha256':queue.raw_sha((root/REPLACEMENT).read_bytes()),'notes_revision':'current'},
        author_provenance=replacement['author_provenance'],change_basis='Add the independently identified missing clock',
        claim_mapping={cid:[cid] for cid in binding['claim_record_sha256s']},added_claim_ids=[extra['claim_id']],changed_claim_ids=[],
        omission_resolutions=[{'omission_sha256':queue.raw_sha(b'Omitted operational clock'),
                              'claim_ids':[extra['claim_id']],'explanation':'Enumerates the omitted operative clock; needs independent review'}])
    (root/RECORD).write_bytes(queue.encoded(spec)); commit(root,'versioned author correction fixture')
    return root,notes,inv,state,old,spec


def register(fixture):
    root,notes,inv,state,old,spec = fixture
    identifier = revisions.register(state,inv,root,RECORD,notes,NOW)
    persist(root,state)
    return state['jobs'][-1]


def switch_ledger(fixture):
    root,notes,inv,state,old,spec = fixture
    census = json.loads((root/REPLACEMENT).read_bytes())
    rows = [json.loads(x) for x in (root/queue.LEDGER).read_text().splitlines()]
    rows = [revisions.replacement_row(spec,census) if r['unit_id'] == spec['unit_id'] else r for r in rows]
    (root/queue.LEDGER).write_text(''.join(json.dumps(r)+'\n' for r in rows)); commit(root,'select corrected census')
    return queue.inventory(root,notes)


def final_review(job,report):
    for row in report['records']:
        row['reassessment_review'] = {**job['reassessment_review'],'final_census_read_completely':True,
                                      'all_original_omissions_reassessed':True,'all_original_propositions_preserved':True}
        for claim in row['claims']:
            inherited = job['carried_legal_blockers'][row['unit_id']].get(claim['claim_id'])
            if inherited:
                claim['inherited_legal_blockers'] = inherited
                if any(c['legal_status'] == 'LEGAL_HOLD' for c in inherited): claim['legal_status'] = 'LEGAL_HOLD'
        row['legal_status'] = 'LEGAL_HOLD' if any(c['legal_status'] == 'LEGAL_HOLD' for c in row['claims']) else 'SOURCE_BLOCKED'


def test_registration_immediately_removes_only_revised_current_credit_and_keeps_immutable_history(remediation):
    root,notes,inv,state,old,spec = remediation
    original = queue.encoded(old); old_report = (root/old['result']['evidence']['path']).read_bytes()
    before = load_metadata(root,notes); assert before['progress']['processed_units'] == 5
    job = register(remediation)
    # Registration itself removes current credit, even before generated ledger selects v2.
    metadata = load_metadata(root,notes); row = metadata['units'][spec['unit_id']]
    assert metadata['progress']['processed_units'] == 4
    assert metadata['progress']['pending_census_reassessment_units'] == 1
    assert row['current_review_valid'] is False and row['completeness'] == 'PENDING_REASSESSMENT'
    assert row['legal_status'] == 'LEGAL_HOLD' and row['requires_review'] is True
    assert row['review_history'][0]['completeness'] == 'OMISSIONS_FOUND'
    assert row['review_history'][0]['findings'] and row['omissions']
    for uid in old['unit_ids'][1:]: assert metadata['units'][uid] == before['units'][uid]
    assert queue.encoded(old) == original and (root/old['result']['evidence']['path']).read_bytes() == old_report
    assert queue.progress(state,inv,root)['independent_completeness_legal_processed_units'] == 4
    with pytest.raises(ValueError,match='Assigned ledger'):
        queue.claim(state,inv,'new-auditor','fresh-session','Checked author identities',at=NOW)
    assert revisions.register(state,inv,root,RECORD,notes,NOW) == job['job_id']
    assert len(state['jobs']) == 2 and len(state['reassessments']) == 1


def test_new_final_census_needs_fresh_non_author_and_preserves_unresolved_legal_blockers(remediation):
    root,notes,_,state,old,spec = remediation; job = register(remediation); inv = switch_ledger(remediation)
    for actor,session in [('correction-author','other-session'),('other','correction-session'),('known-author','fresh')]:
        with pytest.raises(ValueError,match='cannot self-audit'):
            queue.claim(state,inv,actor,session,'Root author check',at=NOW)
    queue.claim(state,inv,'new-auditor','new-session','Root checked original and correcting authors',at=NOW)
    result,worker = worker_result((root,notes,inv),state,job,lambda report:final_review(job,report))
    queue.submit(state,job['job_id'],job['lease_token'],queue.encoded(result),root,inv,NOW)
    persist(root,state)
    assert load_metadata(root,notes)['progress']['processed_units'] == 4  # SUBMITTED is still pending
    integrate_files(root,result); queue.integrate(state,job['job_id'],root,inv,NOW); persist(root,state)
    metadata = load_metadata(root,notes); row = metadata['units'][spec['unit_id']]
    assert metadata['progress']['processed_units'] == 5  # never six
    assert metadata['progress']['complete_units'] == 5
    assert metadata['progress']['historical_review_records'] == 6
    assert metadata['progress']['pending_census_reassessment_units'] == 0
    assert row['current_review_valid'] is True and row['completeness'] == 'COMPLETE'
    assert row['legal_status'] == 'LEGAL_HOLD' and row['review_history'][0]['omissions']
    assert queue.progress(state,inv,root)['independent_completeness_legal_processed_units'] == 5
    before = queue.encoded(state)
    queue.submit(state,job['job_id'],job['lease_token'],queue.encoded(result),root,inv,NOW)
    queue.integrate(state,job['job_id'],root,inv,NOW)
    assert queue.encoded(state) == before


@pytest.mark.parametrize('defect',['no_delta','missing_mapping','drop_old_claim','wrong_omission','old_report_sha',
                                  'old_job_sha','forged_author','duplicate_added','body_change','changed_away_original'])
def test_registration_rejects_scope_delta_provenance_and_historical_mutations(remediation,defect):
    root,notes,inv,state,old,spec = remediation
    replacement = json.loads((root/REPLACEMENT).read_bytes())
    if defect == 'changed_away_original':
        replacement['claims'][0]['statement_ko'] = 'Different proposition replacing a held original'
        spec['changed_claim_ids'] = [replacement['claims'][0]['claim_id']]
    elif defect == 'no_delta':
        replacement['claims'][-1]['statement_ko'] = replacement['claims'][0]['statement_ko']
    elif defect == 'missing_mapping': spec['claim_mapping'].pop(next(iter(spec['claim_mapping'])))
    elif defect == 'drop_old_claim': replacement['claims'].pop(0); replacement['units'][0]['claim_count'] -= 1
    elif defect == 'wrong_omission': spec['omission_resolutions'][0]['omission_sha256'] = '0'*64
    elif defect == 'old_report_sha': spec['previous_report']['raw_sha256'] = '0'*64
    elif defect == 'old_job_sha': spec['previous_job_sha256'] = '0'*64
    elif defect == 'forged_author': replacement['author_provenance']['actor_id'] = 'hidden-author'
    elif defect == 'duplicate_added': spec['added_claim_ids'] *= 2
    elif defect == 'body_change':
        notes['chapters'][0]['units'][0]['body'] += ' new body'
        (root/'notes-fixture.json').write_bytes(queue.encoded(notes))
    (root/REPLACEMENT).write_bytes(queue.encoded(replacement))
    spec['replacement']['census_sha256'] = queue.raw_sha((root/REPLACEMENT).read_bytes())
    (root/RECORD).write_bytes(queue.encoded(spec)); commit(root,'defective correction fixture')
    before = queue.encoded(state)
    with pytest.raises(ValueError): revisions.register(state,inv,root,RECORD,notes,NOW)
    assert queue.encoded(state) == before


@pytest.mark.parametrize('defect',['unchanged_failure_override','unacknowledged_blocker','no_final_census_assessment'])
def test_new_opinion_cannot_override_original_failure_or_skip_final_census(remediation,defect):
    root,notes,_,state,old,spec = remediation; job = register(remediation); inv = switch_ledger(remediation)
    queue.claim(state,inv,'new-auditor','new-session','Checked both authors',at=NOW)
    def change(report):
        final_review(job,report); row = report['records'][0]; claim = row['claims'][0]
        if defect == 'unchanged_failure_override': claim['legal_status'] = 'SOURCE_BLOCKED'
        elif defect == 'unacknowledged_blocker': claim.pop('inherited_legal_blockers')
        else: row.pop('reassessment_review')
    result,worker = worker_result((root,notes,inv),state,job,change)
    with pytest.raises(ValueError,match='blockers|final-census'):
        queue.submit(state,job['job_id'],job['lease_token'],queue.encoded(result),root,inv,NOW)
    assert job['status'] == 'LEASED'


def test_reassessment_recovery_token_sequence_duplicate_and_current_staleness(remediation):
    root,notes,original_inv,state,old,spec = remediation; job = register(remediation); inv = switch_ledger(remediation)
    queue.claim(state,inv,'new-auditor','new-session','Checked both authors',at=NOW)
    token = job['lease_token']; queue.recover(state,LATER)
    with pytest.raises(ValueError,match='Assigned ledger'):
        queue.progress(state,original_inv)  # recovery cannot reopen the initial parent-ledger transition
    queue.claim(state,inv,'replacement-auditor','replacement-session','Checked replacement',at=LATER)
    with pytest.raises(ValueError,match='Stale'): queue.heartbeat(state,job['job_id'],token,inv,at=LATER)
    duplicate = copy.deepcopy(state); duplicate['jobs'].append(copy.deepcopy(job))
    duplicate['jobs'][-1].update(job_id='forged-job',sequence=3)
    with pytest.raises(ValueError,match='duplicate reassessment'): queue.validate_state(duplicate)
    reordered = copy.deepcopy(state); reordered['jobs'][0]['status'] = 'SUBMITTED'
    with pytest.raises(ValueError,match='predecessor'): queue.validate_state(reordered)
    changed = copy.deepcopy(inv); changed['units'][spec['unit_id']]['census_sha256'] = '0'*64
    with pytest.raises(ValueError,match='Assigned ledger'): queue.progress(state,changed)
    old['result_sha256'] = '0'*64
    with pytest.raises(ValueError,match='history changed'): queue.validate_state(state)


def test_builder_hook_and_shallow_reader_validate_historical_raw_snapshots_and_current_only(remediation,tmp_path,monkeypatch):
    root,notes,_,state,old,spec = remediation; register(remediation); inv = switch_ledger(remediation)
    specs = revisions.registered_specs(root,notes)
    assert specs == [{'path':REPLACEMENT,'notes_revision':'current',
                      'supersedes':{spec['unit_id']:spec['previous_binding']['census_path']}}]
    metadata = load_metadata(root,notes)
    raw = (root/queue.LEDGER).read_bytes()
    rows = [json.loads(x) for x in raw.decode().splitlines()]
    for row in rows: row['independent_atomic_census_review'] = metadata['units'].get(row['unit_id'])
    computed = ''.join(json.dumps(r)+'\n' for r in rows).encode()
    assert load_metadata(root,notes,ledger_raw=computed) == metadata
    global_config=tmp_path/'empty-global.gitconfig';global_config.write_text('')
    monkeypatch.setenv('GIT_CONFIG_GLOBAL',str(global_config))
    shallow = tmp_path/'shallow'
    subprocess.run(['git','clone','-q','--depth','1',root.as_uri(),str(shallow)],check=True)
    queue.git(shallow,'config','user.name','Census snapshot fixture')
    queue.git(shallow,'config','user.email','fixture@example.test')
    with pytest.raises(subprocess.CalledProcessError): queue.git(shallow,'cat-file','-e',old['result']['worker_commit']+'^{commit}')
    assert load_metadata(shallow,notes) == metadata
    old_census = shallow/spec['previous_binding']['census_path']
    old_census.write_bytes(old_census.read_bytes()+b' '); commit(shallow,'tamper old snapshot')
    with pytest.raises(ValueError,match='SHA|snapshot'): load_metadata(shallow,notes)


@pytest.mark.parametrize('remediation',[2],indirect=True)
def test_distinct_units_can_queue_together_but_integrate_in_sequence(remediation):
    root,notes,inv,state,old,spec = remediation; first = register(remediation)
    uid = old['unit_ids'][1]; binding = old['unit_bindings'][uid]
    replacement = json.loads((root/binding['census_path']).read_bytes())
    replacement['units'] = [u for u in replacement['units'] if u['unit_id'] == uid]
    replacement['units'][0].update(claim_count=3,census_status='COMPLETE_AUTHOR_ENUMERATION_PENDING_INDEPENDENT_COMPLETENESS_CHECK')
    replacement['claims'] = [c for c in replacement['claims'] if c['unit_id'] == uid]
    extra = dict(replacement['claims'][0],claim_id=uid+'-added-clock',statement_ko='Omitted clock for second unit')
    replacement['claims'].append(extra); replacement['sources'] = {}; replacement['author_provenance'] = spec['author_provenance']
    path = REPLACEMENT.replace('v2','second-v2'); record_path = RECORD.replace('v1','second-v1')
    (root/path).write_bytes(queue.encoded(replacement))
    record = copy.deepcopy(spec)
    row = next(json.loads(x) for x in (root/queue.LEDGER).read_text().splitlines() if json.loads(x)['unit_id'] == uid)
    record.update(reassessment_id='second-unit-v2',unit_id=uid,body_sha256=binding['body_sha256'],previous_binding=binding,
        previous_ledger_fields={k:row.get(k) for k in revisions.LEDGER_FIELDS},
        replacement={'census_path':path,'census_sha256':queue.raw_sha((root/path).read_bytes()),'notes_revision':'current'},
        claim_mapping={cid:[cid] for cid in binding['claim_record_sha256s']},added_claim_ids=[extra['claim_id']])
    record['omission_resolutions'][0]['claim_ids'] = [extra['claim_id']]
    (root/record_path).write_bytes(queue.encoded(record)); commit(root,'second unit correction')
    revisions.register(state,inv,root,record_path,notes,NOW); persist(root,state)
    assert len(state['jobs']) == 3
    assert load_metadata(root,notes)['progress']['processed_units'] == 3
    # Supply the builder's current computed ledger for both registered revisions.
    rows = [json.loads(x) for x in (root/queue.LEDGER).read_text().splitlines()]
    for entry in state['reassessments']:
        r = entry['record']; census = json.loads((root/r['replacement']['census_path']).read_bytes())
        rows = [revisions.replacement_row(r,census) if row['unit_id'] == r['unit_id'] else row for row in rows]
    (root/queue.LEDGER).write_text(''.join(json.dumps(r)+'\n' for r in rows)); commit(root,'select both revised censuses')
    current = queue.inventory(root,notes)
    last = state['jobs'][-1]; last['status'] = 'SUBMITTED'
    with pytest.raises(ValueError,match='assignment order'): queue.integrate(state,last['job_id'],root,current,NOW)
    last['status'] = 'QUEUED'
    assert queue.claim(state,current,'fresh','fresh-session','Checked all authors',at=NOW)['job_id'] == first['job_id']
    blocked_record = dict(record,reassessment_id='not-started-v3')
    blocked_path = record_path.replace('.json','-unregistered.json')
    (root/blocked_path).write_bytes(queue.encoded(blocked_record)); commit(root,'pending registration fixture')
    with pytest.raises(ValueError,match='Finish current wave'):
        revisions.register(state,current,root,blocked_path,notes,NOW)


@pytest.mark.parametrize('remediation',[{'count':1,'legal':'KEEP'}],indirect=True)
def test_pure_omission_hold_can_only_become_keep_after_actual_fresh_final_census_review(remediation):
    root,notes,_,state,old,spec = remediation; job = register(remediation); inv = switch_ledger(remediation)
    assert job['carried_legal_blockers'] == {spec['unit_id']:{}}
    assert load_metadata(root,notes)['progress']['legal_keep_units'] == 4
    queue.claim(state,inv,'new-auditor','new-session','Checked both author histories',at=NOW)
    def review(report):
        final_review(job,report)
        row = report['records'][0]; row['legal_status'] = 'KEEP'
        for claim in row['claims']:
            claim.update(legal_status='KEEP',authorities=[authority(queue.OUTPUT+'fixture-official.txt')])
            claim.pop('blocker')
    result,worker = worker_result((root,notes,inv),state,job,review)
    queue.submit(state,job['job_id'],job['lease_token'],queue.encoded(result),root,inv,NOW)
    persist(root,state)
    assert load_metadata(root,notes)['units'][spec['unit_id']]['legal_status'] == 'LEGAL_HOLD'
    integrate_files(root,result); queue.integrate(state,job['job_id'],root,inv,NOW); persist(root,state)
    metadata = load_metadata(root,notes); row = metadata['units'][spec['unit_id']]
    assert metadata['progress']['legal_keep_units'] == 5 and row['legal_status'] == 'KEEP'
    assert row['review_history'][0]['completeness'] == 'OMISSIONS_FOUND'
    assert row['canonical_release_credit'] == row['question_audit_credit'] == 0


def test_original_author_exclusions_survive_rewritten_author_metadata_and_cannot_be_deleted(remediation):
    root,notes,inv,state,old,spec = remediation
    census = json.loads((root/REPLACEMENT).read_bytes()); census.pop('reviewer_provenance')
    for claim in census['claims']: claim['reviewer_provenance'] = 'correction-author'
    (root/REPLACEMENT).write_bytes(queue.encoded(census))
    spec['replacement']['census_sha256'] = queue.raw_sha((root/REPLACEMENT).read_bytes())
    spec['changed_claim_ids'] = sorted(spec['claim_mapping'])
    (root/RECORD).write_bytes(queue.encoded(spec)); commit(root,'author provenance correction')
    job = register(remediation); current = switch_ledger(remediation)
    assert 'known-author' not in job['unit_bindings'][spec['unit_id']]['known_author_ids']
    assert 'known-author' in job['known_author_ids']
    with pytest.raises(ValueError,match='cannot self-audit'):
        queue.claim(state,current,'known-author','different-session','Source writer remains disqualified',at=NOW)
    job['known_author_ids'] = []; persist(root,state)
    with pytest.raises(ValueError,match='author provenance'): load_metadata(root,notes)


@pytest.mark.parametrize('defect',['record_raw','carried_blocker','registration_event','worker_commit'])
def test_registered_record_provenance_and_worker_commit_checks_remain_strict(remediation,defect):
    root,notes,_,state,old,spec = remediation; job = register(remediation); inv = switch_ledger(remediation)
    if defect == 'record_raw':
        path = root/RECORD; path.write_bytes(path.read_bytes()+b' '); commit(root,'tamper version record')
    elif defect == 'carried_blocker':
        job['carried_legal_blockers'][spec['unit_id']] = {}; persist(root,state)
    elif defect == 'registration_event':
        state['events'] = [e for e in state['events'] if e['kind'] != 'REGISTER_CENSUS_REASSESSMENT']; persist(root,state)
    else:
        queue.claim(state,inv,'new-auditor','new-session','Checked authors',at=NOW)
        result,worker = worker_result((root,notes,inv),state,job,lambda report:final_review(job,report))
        (worker/queue.OUTPUT/'extra.txt').write_text('extra evidence')
        queue.git(worker,'add','.'); queue.git(worker,'commit','-qm','branch advanced after exact result commit')
        with pytest.raises(ValueError,match='branch/commit mismatch'):
            queue.submit(state,job['job_id'],job['lease_token'],queue.encoded(result),root,inv,NOW)
        return
    with pytest.raises(ValueError): load_metadata(root,notes)


def test_later_census_version_preserves_all_ancestral_legal_blockers_and_negative_history(remediation):
    root,notes,_,state,old,spec = remediation; job = register(remediation); inv = switch_ledger(remediation)
    queue.claim(state,inv,'new-auditor','new-session','Checked authors',at=NOW)
    def still_incomplete(report):
        final_review(job,report)
        report['records'][0].update(completeness='OMISSIONS_FOUND',omissions=['Another omitted exception'])
    result,worker = worker_result((root,notes,inv),state,job,still_incomplete)
    queue.submit(state,job['job_id'],job['lease_token'],queue.encoded(result),root,inv,NOW)
    integrate_files(root,result); queue.integrate(state,job['job_id'],root,inv,NOW); persist(root,state)
    previous = copy.deepcopy(job); uid = spec['unit_id']
    census = json.loads((root/REPLACEMENT).read_bytes())
    extra = dict(census['claims'][0],claim_id=uid+'-new-exception',statement_ko='Another omitted exception proposition')
    census['claims'].append(extra); census['units'][0]['claim_count'] += 1
    path = REPLACEMENT.replace('v2','v3'); record_path = RECORD.replace('v1','v3')
    (root/path).write_bytes(queue.encoded(census))
    record = copy.deepcopy(spec); row = next(json.loads(x) for x in (root/queue.LEDGER).read_text().splitlines()
                                           if json.loads(x)['unit_id'] == uid)
    record.update(reassessment_id='clock-census-v3',previous_job_id=job['job_id'],previous_job_sha256=queue.digest(job),
        previous_binding=job['unit_bindings'][uid],previous_report=result['evidence'],
        previous_result={'path':result['result_path'],'raw_sha256':job['result_sha256']},
        previous_ledger_fields={k:row.get(k) for k in revisions.LEDGER_FIELDS},
        replacement={'census_path':path,'census_sha256':queue.raw_sha((root/path).read_bytes()),'notes_revision':'current'},
        claim_mapping={cid:[cid] for cid in job['unit_bindings'][uid]['claim_record_sha256s']},
        added_claim_ids=[extra['claim_id']],changed_claim_ids=[],
        omission_resolutions=[{'omission_sha256':queue.raw_sha(b'Another omitted exception'),
                              'claim_ids':[extra['claim_id']],'explanation':'Newly enumerates the further omission'}])
    (root/record_path).write_bytes(queue.encoded(record)); commit(root,'third census version')
    revisions.register(state,inv,root,record_path,notes,NOW); persist(root,state)
    latest = state['jobs'][-1]; inherited = latest['carried_legal_blockers'][uid][old['unit_bindings'][uid]['source_blocked_claim_ids'][0]]
    assert {b['original_report_sha256'] for b in inherited} == {old['result']['evidence']['raw_sha256'],result['evidence']['raw_sha256']}
    assert job == previous
    metadata = load_metadata(root,notes)
    assert metadata['progress']['processed_units'] == 4
    history = metadata['units'][uid]['review_history']
    assert len(history) == 2 and all(h['completeness'] == 'OMISSIONS_FOUND' for h in history)
    assert metadata['units'][uid]['legal_status'] == 'LEGAL_HOLD'
    assert len(revisions.registered_specs(root,notes)) == 2
