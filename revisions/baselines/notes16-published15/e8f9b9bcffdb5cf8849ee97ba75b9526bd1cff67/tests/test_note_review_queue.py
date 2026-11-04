"""Resumable note audits bind live bodies/censuses and accountable Git evidence."""
import copy
import json
from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import note_review_queue as queue

NOW = '2026-11-03T12:00:00+00:00'
LATER = '2026-11-03T14:00:00+00:00'
CENSUS = 'reports/full-corpus-review/fixture-census.json'


@pytest.fixture
def repo(tmp_path):
    root = tmp_path/'repo'; root.mkdir()
    ids = ['z-first','a-second','m-third','b-fourth','last','not-enumerated']
    units = [{'id':uid,'body':'actual body '+uid} for uid in ids]
    units[0]['independent_content_review'] = {'decision':'KEEP'}
    notes = {'chapters':[{'units':units}]}
    census = {'reviewer_provenance':{'actual_worker':'known-author','session_id':'author-session'},
              'units':[], 'claims':[]}
    rows = []
    for index,unit in enumerate(units):
        uid = unit['id']; body = queue.raw_sha(unit['body'].encode()); enumerated = index < 5
        claim_ids = [uid+'-claim1',uid+'-claim2'] if enumerated else []
        rows.append({'unit_id':uid,'chapter_id':'chapter','actual_effective_body_sha256':body,
            'atomic_claim_census_complete':enumerated,
            'atomic_claim_census_status':'AUTHOR_ENUMERATED' if enumerated else 'NOT_ENUMERATED',
            'atomic_census_source':CENSUS if enumerated else None,'atomic_census_notes_revision':'current',
            'atomic_claim_ids':claim_ids,'atomic_source_blocked_count':1 if enumerated else 0})
        if not enumerated: continue
        census['units'].append({'unit_id':uid,'unit_content_sha256':body,'body_read_completely':True,'claim_count':2})
        census['claims'].extend({'claim_id':cid,'unit_id':uid,'unit_content_sha256':body,
            'statement_ko':'legal claim '+cid,'review_status':'SOURCE_BLOCKED' if n == 0 else 'AUTHOR_SOURCE_CHECKED',
            'reviewer_provenance':'source-author'} for n,cid in enumerate(claim_ids))
    for relative,value in [(CENSUS,census),('notes-fixture.json',notes)]:
        path = root/relative; path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(queue.encoded(value))
    ledger = root/queue.LEDGER
    ledger.write_text(''.join(json.dumps(row)+'\n' for row in rows))
    subprocess.run(['git','init','-q','-b','main',str(root)],check=True)
    queue.git(root,'config','user.name','Fixture'); queue.git(root,'config','user.email','fixture@example.test')
    queue.git(root,'add','.'); queue.git(root,'commit','-qm','fixture inputs')
    return root,notes,queue.inventory(root,notes)


def planned(repo, batches=1, size=5):
    root,notes,inv = repo; state = queue.empty(root)
    queue.plan(state,inv,root,batches=batches,size=size,at=NOW)
    return state


def claimed(repo, state=None, worker='fresh-auditor'):
    state = state or planned(repo)
    job = queue.claim(state,repo[2],worker,worker+'-session','Root assigned a fresh session after checking known authors',at=NOW)
    return state,job


def evidence_for(job):
    header = {'stage':queue.STAGE,'independent_of_authors':True,'canonical_audit':False,
              'canonical_release_credit':0,'question_audit_credit':0,
              **{key:copy.deepcopy(job[key]) for key in ('actor_provenance','auditor','auditor_instance')}}
    records = []
    for uid,binding in job['unit_bindings'].items():
        records.append({'unit_id':uid,'binding':copy.deepcopy(binding),'body_read_completely':True,
            'completeness':'COMPLETE','completeness_method':'Read the entire body against every enumerated proposition',
            'omissions':[],'legal_status':'SOURCE_BLOCKED',
            'claims':[{'claim_id':cid,'claim_record_sha256':sha,'legal_status':'SOURCE_BLOCKED',
                       'claim_read_completely':True,
                       'finding':'Attempted current source verification; controlling scope remains unavailable',
                       'blocker':'Current official source could not be established','authorities':[]}
                      for cid,sha in binding['claim_record_sha256s'].items()]})
    return {**header,'records':records}


def worker_result(repo,state,job,change=None):
    root,notes,inv = repo
    worker = root.parent/('worker-'+str(job['sequence']))
    queue.prepare_worktree(state,job['job_id'],job['lease_token'],inv,root,worker,NOW)
    report = evidence_for(job)
    if change: change(report)
    path = queue.OUTPUT+job['job_id']+'-evidence.json'
    target = worker/path; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(queue.encoded(report))
    queue.git(worker,'add','.'); queue.git(worker,'commit','-qm','independent note findings')
    result = {k:copy.deepcopy(report[k]) for k in ('stage','independent_of_authors','canonical_audit',
        'canonical_release_credit','question_audit_credit','actor_provenance','auditor','auditor_instance')}
    result.update(worker_commit=queue.git(worker,'rev-parse','HEAD'),
        unit_hashes={uid:b['body_sha256'] for uid,b in job['unit_bindings'].items()},
        result_path=queue.OUTPUT+job['job_id']+'-result.json',
        evidence={'path':path,'raw_sha256':queue.raw_sha(target.read_bytes())},
        results=[{k:r[k] for k in ('unit_id','completeness','legal_status')} for r in report['records']])
    return result,worker


def integrate_files(root,result):
    queue.git(root,'cherry-pick',result['worker_commit'])
    path = root/result['result_path']; path.write_bytes(queue.encoded(result))
    queue.git(root,'add',result['result_path']); queue.git(root,'commit','-qm','persist exact submitted result manifest')


def test_deterministic_ledger_order_default_five_and_prior_keep_is_not_completeness(repo):
    state = planned(repo)
    assert state['jobs'][0]['unit_ids'] == ['z-first','a-second','m-third','b-fourth','last']
    assert queue.plan(state,repo[2],repo[0],at=NOW) == []
    same = planned(repo)
    assert state == same
    p = queue.progress(state,repo[2])
    assert p['existing_current_body_content_keep_units'] == 1
    assert p['independent_completeness_legal_processed_units'] == 0
    assert p['not_enumerated_units'] == 1
    assert p['coverage_is_pass'] is p['existing_content_keep_is_completeness_credit'] is False
    assert all(b['source_blocked_claim_ids'] for b in state['jobs'][0]['unit_bindings'].values())


def test_checkpoint_resume_single_root_writer_and_crash_rollback(repo):
    root,_,inv = repo
    with pytest.raises(ValueError,match='Only root'):
        with queue.checkpoint(root,'fresh-auditor'): pytest.fail('worker received write access')
    assert not (root/queue.STATE).exists()
    with queue.checkpoint(root,'/root') as state:
        queue.plan(state,inv,root,at=NOW)
    before = (root/queue.STATE).read_bytes()
    with pytest.raises(RuntimeError):
        with queue.checkpoint(root,'/root') as state:
            state['events'].append({'uncommitted':True}); raise RuntimeError('crash')
    assert (root/queue.STATE).read_bytes() == before
    with queue.checkpoint(root,'/root') as state:
        job = queue.claim(state,inv,'fresh','fresh-session','Fresh actor confirmed by root',at=NOW)
        token = job['lease_token']
    with queue.checkpoint(root,'/root') as state:
        assert queue.claim(state,inv,'fresh','fresh-session','Fresh actor confirmed by root',at=NOW)['lease_token'] == token
    wrong = json.loads((root/queue.STATE).read_bytes()); wrong['controller_root'] = '/other/worktree'
    with pytest.raises(ValueError,match='Controller worktree'):
        queue.validate_state(wrong,root)


@pytest.mark.parametrize('actor,session', [('known-author','fresh-session'),('fresh','author-session'),('source-author','fresh-session')])
def test_known_body_or_source_author_cannot_claim_self_audit(repo,actor,session):
    with pytest.raises(ValueError,match='cannot self-audit'):
        queue.claim(planned(repo),repo[2],actor,session,'Declared independent is not enough',at=NOW)


def test_missing_controller_basis_and_session_change_are_not_independence(repo):
    with pytest.raises(ValueError,match='independence basis'):
        queue.claim(planned(repo),repo[2],'fresh','session','',at=NOW)
    state,job = claimed(repo)
    with pytest.raises(ValueError,match='session differs'):
        queue.claim(state,repo[2],'fresh-auditor','forged-new-session','basis',at=NOW)


def test_expired_token_is_fenced_and_recovery_uses_new_branch(repo):
    state,job = claimed(repo); token = job['lease_token']; branch = job['worker_branch']
    queue.heartbeat(state,job['job_id'],token,repo[2],at=NOW)
    assert queue.recover(state,LATER) == [job['job_id']]
    assert queue.recover(state,LATER) == []
    replacement = queue.claim(state,repo[2],'replacement','replacement-session','Fresh replacement confirmed',at=LATER)
    assert replacement['attempt'] == 2 and replacement['worker_branch'] != branch
    with pytest.raises(ValueError,match='Stale'):
        queue.heartbeat(state,job['job_id'],token,repo[2],at=LATER)


def test_root_registered_author_alias_survives_stale_recovery(repo):
    state = planned(repo)
    queue.claim(state,repo[2],'fresh','fresh-session','Root checked extra source author alias',
                known_authors=['known-external-author'],at=NOW)
    queue.recover(state,LATER)
    with pytest.raises(ValueError,match='cannot self-audit'):
        queue.claim(state,repo[2],'known-external-author','new-session','New attempt cannot erase known author',at=LATER)


def test_inventory_rejects_stale_body_ledger_duplicate_claim_and_extra_unit(repo):
    root,notes,inv = repo
    changed = copy.deepcopy(notes); changed['chapters'][0]['units'][0]['body'] += ' changed'
    with pytest.raises(ValueError,match='Stale ledger'):
        queue.inventory(root,changed)
    path = root/CENSUS; original = path.read_bytes(); census = json.loads(original)
    census['claims'].append(census['claims'][0]); path.write_bytes(queue.encoded(census))
    with pytest.raises(ValueError,match='Duplicate'):
        queue.inventory(root,notes)
    path.write_bytes(original)
    ledger = root/queue.LEDGER; ledger.write_bytes(ledger.read_bytes()+b'{"unit_id":"unknown-extra"}\n')
    with pytest.raises(ValueError,match='inventory'):
        queue.inventory(root,notes)


def test_census_raw_sha_change_blocks_outstanding_job_even_when_claims_unchanged(repo):
    state,job = claimed(repo); root,notes,inv = repo
    path = root/CENSUS; path.write_bytes(path.read_bytes()+b'\n')
    changed = queue.inventory(root,notes)
    with pytest.raises(ValueError,match='census/body changed'):
        queue.heartbeat(state,job['job_id'],job['lease_token'],changed,at=NOW)


def test_unrelated_ledger_annotations_do_not_invalidate_bound_units(repo):
    state,job = claimed(repo); root,notes,inv = repo
    path = root/queue.LEDGER; rows = [json.loads(x) for x in path.read_text().splitlines()]
    rows[-1]['future_note16_review_annotation'] = 'new unrelated author metadata'
    path.write_text(''.join(json.dumps(r)+'\n' for r in rows))
    updated = queue.inventory(root,notes)
    assert updated['ledger_sha256'] != inv['ledger_sha256']
    queue.heartbeat(state,job['job_id'],job['lease_token'],updated,at=NOW)


def test_plan_rejects_uncommitted_inputs_missing_from_worker_snapshot(repo):
    root,notes,inv = repo; path = root/queue.LEDGER
    path.write_text(path.read_text().replace('{"unit_id":','{ "unit_id":',1))
    updated = queue.inventory(root,notes)
    with pytest.raises(ValueError,match='Commit current note ledger'):
        queue.plan(queue.empty(root),updated,root,at=NOW)


def append_note_checkpoint(root,number):
    with queue.checkpoint(Path(root),'/root') as state:
        state['events'].append({'writer':number})


def test_competing_root_processes_serialize_checkpoint_updates(repo):
    import multiprocessing
    root = repo[0]; context = multiprocessing.get_context('fork')
    processes = [context.Process(target=append_note_checkpoint,args=(str(root),n)) for n in range(6)]
    for process in processes: process.start()
    for process in processes:
        process.join(10); assert process.exitcode == 0
    assert {event['writer'] for event in json.loads((root/queue.STATE).read_bytes())['events']} == set(range(6))


@pytest.mark.parametrize('defect', ['forged_actor','different_session','no_independence','canonical_credit',
    'unknown_unit','duplicate_claim','missing_blocked_claim','unknown_pass','failed_complete','hash','unsupported_keep'])
def test_failed_evidence_cannot_complete_job(repo,defect):
    state,job = claimed(repo)
    def change(report):
        row = report['records'][0]
        if defect == 'forged_actor': report['actor_provenance']['actor_id'] = 'invented-auditor'
        elif defect == 'different_session': report['actor_provenance']['session_id'] = 'different-session'
        elif defect == 'no_independence': report['independent_of_authors'] = False
        elif defect == 'canonical_credit': report['question_audit_credit'] = 1
        elif defect == 'unknown_unit': row['unit_id'] = 'unknown-extra'
        elif defect == 'duplicate_claim': row['claims'].append(row['claims'][0])
        elif defect == 'missing_blocked_claim': row['claims'].pop(0)
        elif defect == 'unknown_pass': row['claims'][0]['legal_status'] = 'PASS'
        elif defect == 'failed_complete': row['omissions'] = ['Omitted scope exception']
        elif defect == 'hash': row['binding']['census_sha256'] = '0'*64
        else:
            for c in row['claims']: c['legal_status'] = 'KEEP'
            row['legal_status'] = 'KEEP'
    result,_ = worker_result(repo,state,job,change)
    with pytest.raises(ValueError):
        queue.submit(state,job['job_id'],job['lease_token'],queue.encoded(result),repo[0],repo[2],NOW)
    assert job['status'] == 'LEASED' and not any(e['kind'] == 'SUBMIT' for e in state['events'])


def test_actual_git_submission_integration_exact_result_sha_resume_and_coverage(repo):
    state,job = claimed(repo); root,notes,inv = repo
    result,worker = worker_result(repo,state,job)
    raw = queue.encoded(result)
    queue.submit(state,job['job_id'],job['lease_token'],raw,root,inv,NOW)
    queue.submit(state,job['job_id'],job['lease_token'],raw,root,inv,NOW)
    with pytest.raises(ValueError,match='Conflicting'):
        queue.submit(state,job['job_id'],job['lease_token'],raw+b' ',root,inv,NOW)
    assert queue.progress(state,inv)['independent_completeness_legal_processed_units'] == 0
    changed = copy.deepcopy(result); changed['independent_of_authors'] = False
    with pytest.raises(ValueError): queue.submit(state,job['job_id'],job['lease_token'],queue.encoded(changed),root,inv,NOW)
    integrate_files(root,result)
    path = root/result['result_path']; original = path.read_bytes(); path.write_bytes(original+b' ')
    with pytest.raises(ValueError,match='Result SHA'):
        queue.integrate(state,job['job_id'],root,inv,NOW)
    path.write_bytes(original)
    queue.integrate(state,job['job_id'],root,inv,NOW)
    queue.integrate(state,job['job_id'],root,inv,NOW)
    queue.submit(state,job['job_id'],job['lease_token'],raw,root,inv,LATER)
    assert sum(e['kind'] == 'SUBMIT' for e in state['events']) == sum(e['kind'] == 'INTEGRATE' for e in state['events']) == 1
    p = queue.progress(state,inv,root)
    assert p['independent_completeness_legal_processed_units'] == p['completeness']['COMPLETE'] == 5
    assert p['legal']['SOURCE_BLOCKED'] == 5 and p['legal']['KEEP'] == 0 and p['question_audit_credit'] == 0
    assert queue.plan(state,inv,root,at=LATER) == []


def test_keep_requires_exact_committed_current_official_source_bytes(repo):
    state,job = claimed(repo); root,_,inv = repo
    worker = root.parent/'worker-1'
    queue.prepare_worktree(state,job['job_id'],job['lease_token'],inv,root,worker,NOW)
    path = queue.OUTPUT+'source/current-official.txt'
    source = worker/path; source.parent.mkdir(parents=True,exist_ok=True); source.write_bytes(b'fresh official section')
    def change(report):
        for row in report['records']:
            row['legal_status'] = 'KEEP'
            for c in row['claims']:
                c.update(legal_status='KEEP',blocker=None,authorities=[{'source_type':'PUBLIC_OFFICIAL',
                    'official_url':'https://www.mass.gov/doc/current-source/download','exact_section':'Section 1',
                    'law_checked_date':'2026-11-03','version_or_effective_date_status':'Current compilation; individual effective date not established',
                    'evidence_path':path,'evidence_sha256':queue.raw_sha(source.read_bytes())}])
    result,_ = worker_result(repo,state,job,change)
    queue.submit(state,job['job_id'],job['lease_token'],queue.encoded(result),root,inv,NOW)
    integrate_files(root,result)
    original = (root/path).read_bytes(); (root/path).write_bytes(b'changed source')
    with pytest.raises(ValueError,match='unintegrated'):
        queue.integrate(state,job['job_id'],root,inv,NOW)
    (root/path).write_bytes(original)
    queue.integrate(state,job['job_id'],root,inv,NOW)
    assert queue.progress(state,inv,root)['legal']['KEEP'] == 5
    (root/path).write_bytes(b'changed after checkpoint')
    with pytest.raises(ValueError,match='unintegrated'):
        queue.progress(state,inv,root)


def add_explicit_nonlegal(repo):
    root,notes,inv = repo; path = root/CENSUS; census = json.loads(path.read_bytes())
    uid = 'last'; census['claims'] = [c for c in census['claims'] if c['unit_id'] != uid]
    unit = next(u for u in census['units'] if u['unit_id'] == uid)
    unit.update(claim_count=0,nonlegal_inventory_only=True,
                legal_verification_status='NOT_APPLICABLE_EDITORIAL_METHOD_NO_LEGAL_CLAIMS')
    census['editorial_nonlegal_inventory'] = {uid:{'body_read_completely':True,'legal_claim_count':0,
        'classification':'EDITORIAL_EVIDENCE_MANAGEMENT_NOT_SUBSTANTIVE_LEGAL_RULE',
        'items':[{'item':'Source review method','finding_ko':'Editorial method, not a legal rule'}],
        'census_completion_basis_ko':'Author read the complete body and found only editorial evidence management'}}
    path.write_bytes(queue.encoded(census))
    path = root/queue.LEDGER; rows = [json.loads(x) for x in path.read_text().splitlines()]
    row = next(r for r in rows if r['unit_id'] == uid); row.update(atomic_claim_ids=[],atomic_source_blocked_count=0)
    path.write_text(''.join(json.dumps(r)+'\n' for r in rows))
    queue.git(root,'add','.'); queue.git(root,'commit','-qm','explicit zero legal claim author classification')
    return root,notes,queue.inventory(root,notes)


@pytest.mark.parametrize('confirmed',[True,False])
def test_explicit_zero_legal_claim_unit_requires_independent_classification_check(repo,confirmed):
    repo = add_explicit_nonlegal(repo); state,job = claimed(repo)
    def change(report):
        row = next(r for r in report['records'] if r['unit_id'] == 'last')
        row['nonlegal_classification_review'] = {'confirmed':confirmed,
            'finding':'Independent full body check confirms editorial scope' if confirmed else 'Found a substantive legal exception'}
        row.update(legal_status='NOT_APPLICABLE_NONLEGAL' if confirmed else 'LEGAL_HOLD',
                   completeness='COMPLETE' if confirmed else 'OMISSIONS_FOUND',
                   omissions=[] if confirmed else ['Omitted substantive exception'])
    result,_ = worker_result(repo,state,job,change)
    queue.submit(state,job['job_id'],job['lease_token'],queue.encoded(result),repo[0],repo[2],NOW)
    integrate_files(repo[0],result); queue.integrate(state,job['job_id'],repo[0],repo[2],NOW)
    p = queue.progress(state,repo[2],repo[0])
    assert p['legal']['NOT_APPLICABLE_NONLEGAL'] == int(confirmed)
    assert p['legal']['KEEP'] == 0
    assert p['legal']['LEGAL_HOLD'] == int(not confirmed)


def test_arbitrary_empty_census_is_not_completed_or_independently_credited(repo):
    root,notes,inv = repo; path = root/CENSUS; census = json.loads(path.read_bytes())
    census['claims'] = [c for c in census['claims'] if c['unit_id'] != 'last']
    next(u for u in census['units'] if u['unit_id'] == 'last')['claim_count'] = 0
    path.write_bytes(queue.encoded(census))
    with pytest.raises(ValueError,match='explicit reviewed nonlegal'):
        queue.inventory(root,notes)
    repo = add_explicit_nonlegal(repo); state,job = claimed(repo)
    result,_ = worker_result(repo,state,job)
    with pytest.raises(ValueError,match='Independent assessment'):
        queue.submit(state,job['job_id'],job['lease_token'],queue.encoded(result),repo[0],repo[2],NOW)


def test_worker_commit_hash_and_scope_mismatch_are_rejected(repo):
    state,job = claimed(repo); result,worker = worker_result(repo,state,job)
    base = copy.deepcopy(result); base['worker_commit'] = job['base_commit']
    with pytest.raises(ValueError,match='commit mismatch'):
        queue.submit(state,job['job_id'],job['lease_token'],queue.encoded(base),repo[0],repo[2],NOW)
    path = worker/'notes-fixture.json'; path.write_bytes(path.read_bytes()+b' ')
    queue.git(worker,'add','.'); queue.git(worker,'commit','-qm','unauthorized body edit')
    queue.git(worker,'revert','--no-edit','HEAD')
    result['worker_commit'] = queue.git(worker,'rev-parse','HEAD')
    with pytest.raises(ValueError,match='outside note evidence scope'):
        queue.submit(state,job['job_id'],job['lease_token'],queue.encoded(result),repo[0],repo[2],NOW)


def test_multiple_evidence_only_worker_commits_are_allowed(repo):
    state,job = claimed(repo); result,worker = worker_result(repo,state,job)
    path = worker/(queue.OUTPUT+'additional-retrieval.txt'); path.write_bytes(b'additional evidence metadata')
    queue.git(worker,'add','.'); queue.git(worker,'commit','-qm','additional retrieval provenance')
    result['worker_commit'] = queue.git(worker,'rev-parse','HEAD')
    queue.submit(state,job['job_id'],job['lease_token'],queue.encoded(result),repo[0],repo[2],NOW)
    assert job['status'] == 'SUBMITTED'


def test_evidence_commit_bytes_and_integration_sequence_are_guarded(repo):
    state = planned(repo,batches=2,size=2); state,first = claimed(repo,state,'first')
    _,second = claimed(repo,state,'second')
    result,_ = worker_result(repo,state,second)
    bad = copy.deepcopy(result); bad['evidence']['raw_sha256'] = '0'*64
    with pytest.raises(ValueError,match='SHA mismatch'):
        queue.submit(state,second['job_id'],second['lease_token'],queue.encoded(bad),repo[0],repo[2],NOW)
    queue.submit(state,second['job_id'],second['lease_token'],queue.encoded(result),repo[0],repo[2],NOW)
    with pytest.raises(ValueError,match='assignment order'):
        queue.integrate(state,second['job_id'],repo[0],repo[2],NOW)
    assert first['status'] == 'LEASED' and second['status'] == 'SUBMITTED'


def test_omissions_and_legal_hold_are_processed_coverage_without_pass(repo):
    state,job = claimed(repo)
    def change(report):
        row = report['records'][0]; row.update(completeness='OMISSIONS_FOUND',omissions=['Missing statutory exception'],legal_status='LEGAL_HOLD')
    result,_ = worker_result(repo,state,job,change)
    queue.submit(state,job['job_id'],job['lease_token'],queue.encoded(result),repo[0],repo[2],NOW)
    integrate_files(repo[0],result); queue.integrate(state,job['job_id'],repo[0],repo[2],NOW)
    p = queue.progress(state,repo[2])
    assert p['completeness']['OMISSIONS_FOUND'] == p['legal']['LEGAL_HOLD'] == 1
    assert p['completeness']['COMPLETE'] == p['legal']['SOURCE_BLOCKED'] == 4


def test_question_queues_are_never_selected_as_state_and_worktree_reconnect_is_exact(repo):
    assert queue.STATE not in {'reports/full-corpus-review/work-queue.json',
                              'reports/full-corpus-review/independent-legacy-work-queue.json'}
    state,job = claimed(repo); root,_,inv = repo; destination = root.parent/'fresh-worktree'
    queue.prepare_worktree(state,job['job_id'],job['lease_token'],inv,root,destination,NOW)
    assert queue.prepare_worktree(state,job['job_id'],job['lease_token'],inv,root,destination,NOW) == str(destination)
    with pytest.raises(ValueError,match='Wrong worker'):
        queue.prepare_worktree(state,job['job_id'],job['lease_token'],inv,root,root,NOW)
