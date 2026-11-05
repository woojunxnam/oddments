"""Bounded retry rejects provenance/source drift and cannot erase primary negatives."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import shutil

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import source3_recovered_legal_metadata as route
import review_queue as queue
from export_legacy_review_input import CORE_FIELDS
from phase11_secondary_metadata import combine_metadata

COLLECTION = 'practice_expansion/fixture/questions.json'
PARENT = route.PREFIX + 'fixture-primary.json'
AUTHOR = route.PREFIX + 'fixture-author.json'
REVIEWER = '/root/genuinely-new-fixture-session'


def write(root, path, value):
    p = root / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def commit(root):
    queue.git(root, 'add', '.')
    queue.git(root, 'commit', '--allow-empty', '-qm', 'Synthetic exact-three contract fixture')


@pytest.fixture
def data(tmp_path, monkeypatch):
    root = tmp_path / 'repo'
    root.mkdir()
    subprocess.run(['git', 'init', '-q', '-b', 'main', str(root)], check=True)
    queue.git(root, 'config', 'user.name', 'Synthetic fixture')
    queue.git(root, 'config', 'user.email', 'fixture@example.invalid')
    discovery=json.loads((ROOT/route.RECOVERY_REPORT).read_bytes())
    retained=[route.RECOVERY_REPORT]
    for key in ('policy_metadata','official_current_policy_list'):
        source=discovery['new_source'][key]
        retained.extend(source[k]for k in ('metadata_path','raw_path','text_path','links_path')if k in source)
    for path in retained:
        dest=root/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/path,dest)
    questions = {uid: dict(question_id=uid, question_type='SBA', stem='Which statement is correct?',
        choices=[dict(id='A', text='First synthetic option'), dict(id='B', text='Second synthetic option')],
        correct_choice_ids=['A'], explanation=dict(core_reasoning='합성 근거',
            choice_analysis={'A': '합성 정답 이유', 'B': '합성 오답 이유'}, learning_boundary='합성 범위')) for uid in route.IDS}
    hashes = {uid: queue.digest(q) for uid, q in questions.items()}
    primary = [dict(question_id=uid, record_sha256=hashes[uid], release_eligible=False,
        legal_review=dict(existing_answer_correct='NOT_ASSESSED', verdict='HOLD',
            blocker='SYNTHETIC_UNAVAILABLE_CURRENT_OFFICIAL_DEFINITION', independently_expected_key=[]),
        realism_review=dict(verdict='FAIL'), read_scope={'prior_author_or_independent_verdicts_read': False}) for uid in route.IDS]
    provenance = dict(stage='independent-legacy', independent_of_authors=True,
        actor_provenance={'actor_id':'/root/fixture-old', 'session_id':'/root/fixture-old'},
        auditor='GPT', auditor_instance='GPT:fixture-old', canonical_audit=False, canonical_release_credit=0)
    parent = dict(provenance, records=copy.deepcopy(primary))
    write(root, PARENT, parent)
    parents = {uid: dict(report_path=PARENT, report_sha256=route.sha((root/PARENT).read_bytes()),
        record_sha256=queue.digest(row), question_record_sha256=hashes[uid],
        original_actor='/root/fixture-old', original_session='/root/fixture-old',
        original_actor_provenance=copy.deepcopy(provenance['actor_provenance']),
        original_release_eligibility={'release_eligible':False},
        original_expected_key_representation=[],
        original_auditor_instance='GPT:fixture-old', legal_blocker='SYNTHETIC_UNAVAILABLE_CURRENT_OFFICIAL_DEFINITION',
        parent_key_status='NOT_ASSESSED', parent_verdict='HOLD', exposure_limitations=None,
        read_scope_exposure={'prior_author_or_independent_verdicts_read': False}) for uid, row in zip(route.IDS, primary)}
    monkeypatch.setattr(route, 'PARENTS', parents)
    write(root, AUTHOR, {'author_session':'original-fixture-author'})
    monkeypatch.setattr(route, 'AUTHOR_BINDINGS', {AUTHOR: dict(raw_sha256=route.sha((root/AUTHOR).read_bytes()),
                                                            known_principals=['original-fixture-author'])})
    reviewer = dict(actor_provenance={'actor_id':REVIEWER, 'session_id':REVIEWER}, auditor='GPT',
        auditor_instance='GPT:actual-new-fixture', known_author_ids=['original-fixture-author'],
        target_question_ids=list(route.IDS), current_target_prior_conclusions_read=False,
        current_target_author_or_editor=False, new_independent_person_credit=0,
        controller_independence_basis='Root confirms this actual separate fixture session; labels are not identity proof.')
    scope = dict(schema_version=1, purpose=route.PURPOSE, question_ids=list(route.IDS),
        previous_evidence=copy.deepcopy(parents), root_actor='/root', automatic_release_credit=0, fresh_reviewer=reviewer)
    scope['recovered_source_reference']={'path':route.RECOVERY_REPORT,'raw_sha256':route.RECOVERY_REPORT_SHA}
    state = queue.empty('independent-legacy')
    state[route.SCOPE_KEY] = scope
    job = dict(job_id=route.JOB_ID, sequence=1, question_hashes=hashes, status='INTEGRATED', attempt=1,
        stage='independent-legacy', worker=REVIEWER, worker_branch='mission/'+route.JOB_ID+'-attempt-1',
        integrated_commit='c'*40, integrated_at='2026-11-04T22:01:00+00:00',
        submitted_at='2026-11-04T22:00:30+00:00',
        excluded_worker_actor_ids=['/root',route.ENGINEER,'original-fixture-author','/root/fixture-old','GPT:fixture-old'])
    state['jobs'] = [job]
    prefix = route.PREFIX + 'source3-independent/' + route.JOB_ID + '/'
    raw = prefix + 'official.raw'; text = prefix + 'official.txt'; meta = prefix + 'official.meta.json'
    for p, content in [(raw,b'Synthetic official raw bytes'),(text,b'Synthetic official extracted text')]:
        (root/p).parent.mkdir(parents=True, exist_ok=True)
        (root/p).write_bytes(content)
    metadata = dict(official_url='https://example.gov/current-law', raw_path=raw,
        raw_sha256=route.sha((root/raw).read_bytes()), text_path=text, text_sha256=route.sha((root/text).read_bytes()),
        retrieved_at='2026-11-04T21:00:00+00:00', read_at='2026-11-04T21:20:00+00:00', status=200,
        method='SYNTHETIC_FIXTURE_NOT_LIVE_REQUEST', document_identity_status='OFFICIAL_TARGET_PROVISIONS_DIRECTLY_READ')
    metadata['source_kind']='OFFICIAL_STATUTE'
    write(root, meta, metadata)
    authority = dict(metadata, source_id='fixture-law', metadata_path=meta,
        metadata_sha256=route.sha((root/meta).read_bytes()), exact_section='Fixture clause 1',
        effective_date_or_version_basis='Fixture version; initial commencement unknown', law_checked_date='2026-11-04')
    fresh_provenance = dict(provenance, actor_provenance=reviewer['actor_provenance'],
        auditor_instance=reviewer['auditor_instance'])
    report = dict(fresh_provenance, purpose=route.PURPOSE, question_hashes=hashes,
        new_independent_people_credit=0,new_unique_original_question_credit=0,new_realism_pass_credit=0,
        reviewed_at='2026-11-04', review_started_at='2026-11-04T20:30:00+00:00',
        review_completed_at='2026-11-04T22:00:00+00:00',
        native_assignment_binding={k:copy.deepcopy(job[k]) for k in
            ('job_id','sequence','question_hashes','stage','worker','worker_branch','attempt')}, records=[])
    for uid, q in questions.items():
        legal = dict(existing_answer_correct='YES', verdict='KEEP', stored_key=['A'], question_type='SBA',
            polarity='CORRECT', polarity_and_sata_combination_checked=True,
            exceptions_and_federal_state_scope_checked=True, prior_conclusions_read=False, hidden_truth_read=False,
            finding_ko='실제 판정이 아닌 합성 계약검사', independently_expected_key=['A'], authorities=[copy.deepcopy(authority)],
            source_scope_limitation_ko='합성 판정이며 정책 문서와 정식 CMR을 구분한다. 별도 효력·적용 범위를 인증하지 않는다.',
            original_explanation_review=dict(core_reasoning_sha256=route.sha(q['explanation']['core_reasoning'].encode()),
                learning_boundary_sha256=route.sha(q['explanation']['learning_boundary'].encode()),
                core_reasoning_read=True, learning_boundary_read=True, finding_ko='원 해설 전체 검토 합성값',
                choice_rationales=[dict(choice_id=c, read=True, finding_ko='각 원 해설 합성 검토',
                    rationale_sha256=route.sha(q['explanation']['choice_analysis'][c].encode())) for c in ['A','B']]),
            per_choice_findings=[dict(choice_id=c, option_text_sha256=route.sha(q['choices'][i]['text'].encode()),
                finding_ko='각 보기의 합성 법규 검토', proposition_supported=c=='A',
                selected_by_independent_polarity=c=='A', authority_refs=['fixture-law']) for i,c in enumerate(['A','B'])])
        report['records'].append(dict(question_id=uid, record_sha256=hashes[uid], release_eligible=False,
            visible_content_sha256=queue.digest({k:q[k]for k in CORE_FIELDS}), legal_review=legal,
            realism_review=dict(verdict='NOT_ASSESSED', blocker='BOUND_LEGAL_ONLY_RETRY_PRESERVE_PRIMARY_REALISM',
                                finding_ko='현실성은 이번 법규 전용 재검사에서 새 판정하지 않는다.')))
    path = prefix + 'report.json'; envelope = prefix + 'result.json'
    write(root, path, report)
    manifest = dict(fresh_provenance, question_hashes=hashes, worker_commit='b'*40,
        results=[dict(question_id=uid, disposition='INDEPENDENT_ASSESSED', evidence_path=path,
                      evidence_sha256=route.sha((root/path).read_bytes())) for uid in route.IDS])
    job['result'] = manifest
    write(root, envelope, manifest)
    scope['result_envelope'] = dict(path=envelope, raw_sha256=route.sha((root/envelope).read_bytes()))
    state['events'] = [dict(kind='CLAIM',job_id=route.JOB_ID,worker=REVIEWER,attempt=1,at='2026-11-04T20:00:00+00:00'),
        dict(kind='SUBMIT',job_id=route.JOB_ID,result_sha256=queue.digest(manifest),at=job['submitted_at']),
        dict(kind='INTEGRATE',job_id=route.JOB_ID,commit=job['integrated_commit'],at=job['integrated_at'])]
    write(root, COLLECTION, {'questions':list(questions.values())})
    write(root, route.STATE, state)
    commit(root)
    return dict(root=root,state=state,report=report,primary=primary,questions=questions,
                collections=dict.fromkeys(route.IDS,COLLECTION),report_path=path,envelope_path=envelope,
                raw=raw,text=text,meta=meta)


def load(d, **kwargs):
    return route.load_metadata(d['root'],d['primary'],d['questions'],d['collections'],**kwargs)


def refresh(d, report=True):
    root=d['root'];state=d['state'];job=state['jobs'][0];scope=state[route.SCOPE_KEY]
    if report:
        write(root,d['report_path'],d['report'])
        for row in job['result']['results']:
            row['evidence_sha256']=route.sha((root/d['report_path']).read_bytes())
    write(root,d['envelope_path'],job['result'])
    scope['result_envelope']['raw_sha256']=route.sha((root/d['envelope_path']).read_bytes())
    for e in state['events']:
        if e['kind']=='SUBMIT': e['result_sha256']=queue.digest(job['result'])
    write(root,route.STATE,state);commit(root)


def test_unique_key_union_preserves_original_holds_failures_and_bytes(data):
    before=copy.deepcopy(data['primary']);old=(data['root']/PARENT).read_bytes();bindings={}
    result=load(data,source_bindings=bindings)
    assert result['progress']['supplementary_new_key_assessed']==3
    assert result['progress']['effective_key_assessed']==3
    assert result['progress']['canonical_release_credit']==0
    assert data['primary']==before and (data['root']/PARENT).read_bytes()==old
    assert all(x['realism_review']['verdict']=='FAIL'and x['legal_review']['verdict']=='HOLD' for x in data['primary'])
    assert all(p['does_not_override_primary'] and p['canonical_release_credit']==0 for p in result['assessments'].values())
    assert all(p in bindings for p in [route.STATE,PARENT,AUTHOR,COLLECTION,data['report_path'],data['envelope_path'],data['raw'],data['text'],data['meta']])
    with pytest.raises(ValueError,match='Overlapping'):
        combine_metadata(data['primary'],result,result)


@pytest.mark.parametrize('status',['QUEUED','LEASED','SUBMITTED'])
def test_pending_native_work_has_no_credit_and_does_not_read_unfinished_report(data,status):
    data['state']['jobs'][0]['status']=status
    write(data['root'],route.STATE,data['state']);commit(data['root'])
    for p in [data['report_path'],data['envelope_path'],data['raw'],data['text'],data['meta']]:
        (data['root']/p).unlink()
    result=load(data)
    assert result['progress']['supplementary_new_key_assessed']==0 and result['records']==[]


@pytest.mark.parametrize('defect',[
    'extra_scope','parent_raw','parent_row','parent_question','substantive_parent','parent_actor','author_history',
    'extra_job','extra_job_id','missing_author','reviewer_parent','reviewer_root','reviewer_engineer','reviewer_author',
    'instance_parent','session_alias','claim_exclusion','claim_event','submit_event','integrate_event','native_binding',
    'worker_commit','report_actor','envelope_raw','envelope_unbound','report_extra','canonical','release',
    'hidden_truth','prior_conclusion','option_hash','rationale_hash','visible_hash','partial_options','missing_authority',
    'wrong_key','polarity','selection','realism_pass','raw_source','text_source','meta_source','failed_http',
    'metadata_raw_binding','old_cache_retimed','review_before_read','wrong_source_host','missing_effective_limit',
    'current_body','duplicate_primary','preclaim_source','preclaim_review','duplicate_claim','unresolved_assessed_option',
    'fresh_release_field_missing','parent_release_presence_forged'])
def test_every_native_source_identity_and_scope_mutation_fails_closed(data,defect):
    d=data;root=d['root'];state=d['state'];scope=state[route.SCOPE_KEY];job=state['jobs'][0]
    row=d['report']['records'][0];legal=row['legal_review'];reviewer=scope['fresh_reviewer'];uid=route.IDS[0]
    if defect=='extra_scope': scope['question_ids'].append('MA-EXP-9999')
    elif defect in {'parent_raw','parent_row','parent_question','parent_actor'}:
        key={'parent_raw':'report_sha256','parent_row':'record_sha256','parent_question':'question_record_sha256','parent_actor':'original_actor'}[defect]
        scope['previous_evidence'][uid][key]='0'*64
    elif defect=='substantive_parent':
        p=json.loads((root/PARENT).read_bytes());p['records'][0]['legal_review']['blocker']='REAL_SUBSTANTIVE_SOURCE_HOLD'
        write(root,PARENT,p);scope['previous_evidence'][uid]['report_sha256']=route.sha((root/PARENT).read_bytes())
        scope['previous_evidence'][uid]['record_sha256']=queue.digest(p['records'][0]);d['primary'][0]=copy.deepcopy(p['records'][0])
    elif defect=='author_history': write(root,AUTHOR,{'author_session':'different-author'})
    elif defect=='extra_job': state['jobs'].append(copy.deepcopy(job))
    elif defect=='extra_job_id': job['job_id']='not-the-fixed-three'
    elif defect=='missing_author': reviewer['known_author_ids']=[]
    elif defect.startswith('reviewer_'):
        value={'reviewer_parent':'/root/fixture-old','reviewer_root':'/root','reviewer_engineer':route.ENGINEER,'reviewer_author':'original-fixture-author'}[defect]
        reviewer['actor_provenance']={'actor_id':value,'session_id':value}
    elif defect=='instance_parent': reviewer['auditor_instance']='GPT:fixture-old'
    elif defect=='session_alias': reviewer['actor_provenance']['session_id']='same-person-renamed'
    elif defect=='claim_exclusion': job['excluded_worker_actor_ids']=[]
    elif defect.endswith('_event'): state['events']=[e for e in state['events']if e['kind']!=defect[:-6].upper()]
    elif defect=='native_binding': d['report']['native_assignment_binding']['attempt']=2
    elif defect=='worker_commit': job['result']['worker_commit']='z'*40
    elif defect=='report_actor': d['report']['actor_provenance']['session_id']='forged-session'
    elif defect=='envelope_raw': scope['result_envelope']['raw_sha256']='0'*64
    elif defect=='envelope_unbound': scope['result_envelope'].pop('raw_sha256')
    elif defect=='report_extra': d['report']['records'].append(copy.deepcopy(row))
    elif defect=='canonical': d['report']['canonical_release_credit']=1
    elif defect=='release': row['release_eligible']=True
    elif defect=='hidden_truth': legal['hidden_truth_read']=True
    elif defect=='prior_conclusion': legal['prior_conclusions_read']=True
    elif defect=='option_hash': legal['per_choice_findings'][0]['option_text_sha256']='0'*64
    elif defect=='rationale_hash': legal['original_explanation_review']['choice_rationales'][0]['rationale_sha256']='0'*64
    elif defect=='visible_hash': row['visible_content_sha256']='0'*64
    elif defect=='partial_options': legal['per_choice_findings'].pop()
    elif defect=='missing_authority': legal['authorities']=[]
    elif defect=='wrong_key': legal['independently_expected_key']=['B']
    elif defect=='polarity': legal['polarity']='INCORRECT'
    elif defect=='selection': legal['per_choice_findings'][1]['selected_by_independent_polarity']=True
    elif defect=='realism_pass': row['realism_review']['verdict']='PASS'
    elif defect in {'raw_source','text_source','meta_source'}:
        p={'raw_source':d['raw'],'text_source':d['text'],'meta_source':d['meta']}[defect]
        (root/p).write_bytes(b'Committed mutation of retained evidence')
    elif defect in {'failed_http','metadata_raw_binding','old_cache_retimed','review_before_read'}:
        meta=json.loads((root/d['meta']).read_bytes())
        if defect=='failed_http':meta['status']=403
        elif defect=='metadata_raw_binding':meta['raw_sha256']='0'*64
        elif defect=='old_cache_retimed':meta['retrieved_at']='2026-11-03T21:00:00+00:00'
        else:meta['read_at']='2026-11-04T23:00:00+00:00'
        write(root,d['meta'],meta)
        for r in d['report']['records']:r['legal_review']['authorities'][0]['metadata_sha256']=route.sha((root/d['meta']).read_bytes())
    elif defect=='wrong_source_host':legal['authorities'][0]['official_url']='https://commercial.invalid/law'
    elif defect=='missing_effective_limit':legal['authorities'][0]['effective_date_or_version_basis']=''
    elif defect=='current_body':
        d['questions'][uid]['stem']='Changed question';write(root,COLLECTION,{'questions':list(d['questions'].values())})
    elif defect=='duplicate_primary':d['primary'].append(copy.deepcopy(d['primary'][0]))
    elif defect=='preclaim_source':state['events'][0]['at']='2026-11-04T21:30:00+00:00'
    elif defect=='preclaim_review':state['events'][0]['at']='2026-11-04T23:00:00+00:00'
    elif defect=='duplicate_claim':state['events'].append(copy.deepcopy(state['events'][0]))
    elif defect=='unresolved_assessed_option':legal['per_choice_findings'][1]['proposition_supported']=None
    elif defect=='fresh_release_field_missing':row.pop('release_eligible')
    elif defect=='parent_release_presence_forged':scope['previous_evidence'][uid]['original_release_eligibility']={}
    if defect not in {'envelope_raw','envelope_unbound','submit_event'}:
        refresh(d)
    else:
        write(root,route.STATE,state);commit(root)
    with pytest.raises(ValueError):load(d)


def test_incomplete_and_ambiguous_stay_hold_with_only_actual_assessed_credit(data):
    row=data['report']['records'][0];row['legal_review'].update(existing_answer_correct='NOT_ASSESSED',verdict='HOLD',
        independently_expected_key=[],blocker='Actual unavailable primary source; no inferred key')
    row=data['report']['records'][1];row['legal_review'].update(existing_answer_correct='AMBIGUOUS',verdict='HOLD',
        independently_expected_key=[],blocker='Actual scope ambiguity')
    refresh(data);r=load(data)
    assert r['progress']['supplementary_new_key_assessed']==2
    assert r['progress']['supplementary_legal_verdict_counts']=={'HOLD':2,'KEEP':1}


def test_pending_native_identity_is_already_guarded(data):
    data['state']['jobs'][0]['status']='LEASED'
    data['state'][route.SCOPE_KEY]['fresh_reviewer']['actor_provenance']={'actor_id':'/root/fixture-old','session_id':'/root/fixture-old'}
    refresh(data)
    with pytest.raises(ValueError,match='Old actual'):load(data)


def test_negative_retry_reaches_existing_source_bound_notice_dispatch(data,monkeypatch):
    import supplementary_checkpoint_bindings as retained
    root=data['root']
    # The real dispatcher retains this added exact consumer beside the original three.
    assert any(consumer is route and path==route.STATE for consumer,path in retained.CONSUMERS)
    monkeypatch.setattr(retained,'CONSUMERS',((route,route.STATE),))
    empty='practice_expansion/2026-10-23/candidates/questions.json'
    write(root,empty,{'questions':[]})
    write(root,'site/practice-expansion/publication.json',{'additional_banks':[{'path':COLLECTION}]})
    row=data['report']['records'][0]
    row['legal_review'].update(existing_answer_correct='NO',verdict='MAJOR_REWRITE',
        independently_expected_key=['B'],finding_ko='합성 사례의 정답 오류를 구체적으로 기록한다.')
    for choice in row['legal_review']['per_choice_findings']:
        choice['selected_by_independent_polarity']=choice['choice_id']=='B'
    row=data['report']['records'][1]
    row['legal_review'].update(existing_answer_correct='AMBIGUOUS',verdict='HOLD',
        independently_expected_key=[],blocker='합성 범위 미확인')
    refresh(data)
    bindings={};sources=retained.validated_sources(root,data['primary'],source_bindings=bindings)
    assert set(sources)==set(route.IDS)
    for uid in route.IDS[:2]:
        source=sources[uid]
        assert source['negative'] and source['source_path']==data['report_path']
        assert source['source_sha256']==route.sha((root/data['report_path']).read_bytes())
        assert source['record_sha256']==queue.digest(data['questions'][uid])
        assert source['does_not_override_primary'] and source['canonical_release_credit']==0
    assert all(path in bindings for path in [route.STATE,data['report_path'],data['meta'],data['raw'],data['text']])
    assert all(row['legal_review']['verdict']=='HOLD' and row['realism_review']['verdict']=='FAIL' for row in data['primary'])


def test_actual_fresh_read_across_midnight_is_valid_without_retiming_sources(data):
    root=data['root'];report=data['report'];metadata=json.loads((root/data['meta']).read_bytes())
    data['state']['events'][0]['at']='2026-11-04T23:58:00+00:00'
    report['review_started_at']='2026-11-04T23:59:00+00:00'
    report['review_completed_at']='2026-11-05T00:02:00+00:00';report['reviewed_at']='2026-11-05'
    data['state']['jobs'][0].update(submitted_at='2026-11-05T00:03:00+00:00',integrated_at='2026-11-05T00:04:00+00:00')
    data['state']['events'][1]['at']='2026-11-05T00:03:00+00:00'
    data['state']['events'][2]['at']='2026-11-05T00:04:00+00:00'
    metadata.update(retrieved_at='2026-11-04T23:59:10+00:00',read_at='2026-11-05T00:01:00+00:00')
    write(root,data['meta'],metadata)
    for row in report['records']:
        row['legal_review']['authorities'][0].update(law_checked_date='2026-11-05',
            metadata_sha256=route.sha((root/data['meta']).read_bytes()))
    refresh(data)
    assert load(data)['progress']['supplementary_new_key_assessed']==3


def test_source_review_date_cannot_be_relabelled_to_completion_date(data):
    root=data['root'];report=data['report']
    report['review_completed_at']='2026-11-05T00:02:00+00:00';report['reviewed_at']='2026-11-05'
    # Actual source read remains Nov4; recording Nov5 as its law_checked_date is false.
    report['records'][0]['legal_review']['authorities'][0]['law_checked_date']='2026-11-05'
    refresh(data)
    with pytest.raises(ValueError,match='read-date binding'):load(data)


def test_registration_proposal_does_not_mutate_root_and_native_claim_reconnects_idempotently(data):
    from prepare_source3_recovered_legal import prepare
    root=data['root'];reviewer=copy.deepcopy(data['state'][route.SCOPE_KEY]['fresh_reviewer'])
    (root/route.STATE).unlink()
    ledger=[dict(question_id=uid,collection=COLLECTION,content_sha256=queue.digest(q))for uid,q in data['questions'].items()]
    (root/'reports/full-corpus-review/question-ledger.jsonl').write_text('\n'.join(json.dumps(r)for r in ledger)+'\n')
    commit(root);head=queue.git(root,'rev-parse','HEAD')
    state=prepare(root,reviewer)
    assert queue.git(root,'rev-parse','HEAD')==head and not(root/route.STATE).exists()
    assert state['jobs'][0]['status']=='QUEUED' and state['jobs'][0]['attempt']==0
    assert state[route.SCOPE_KEY]['prepared_source_head']==head
    claimed=queue.claim(state,REVIEWER,at='2026-11-04T22:02:00+00:00')
    repeated=queue.claim(state,REVIEWER,at='2026-11-04T22:03:00+00:00')
    assert repeated is claimed and repeated['attempt']==1
    assert sum(e['kind']=='CLAIM'for e in state['events'])==1
    assert not(root/route.STATE).exists() and queue.git(root,'status','--porcelain')==''


def test_registration_cannot_reset_existing_native_state(data):
    from prepare_source3_recovered_legal import prepare
    before=(data['root']/route.STATE).read_bytes()
    with pytest.raises(ValueError,match='reused/recovered'):
        prepare(data['root'],data['state'][route.SCOPE_KEY]['fresh_reviewer'])
    assert(data['root']/route.STATE).read_bytes()==before


@pytest.mark.parametrize('uid',route.IDS)
def test_actual_parent_header_row_and_release_presence_match_exact_source_schema(uid):
    binding=route.PARENTS[uid]
    raw=subprocess.check_output(['git','-C',str(ROOT),'show','HEAD:'+binding['report_path']])
    assert route.sha(raw)==binding['report_sha256']
    source=json.loads(raw);route.validate_parent_identity(source,binding)
    row=next(r for r in source['records']if r['question_id']==uid)
    assert queue.digest(row)==binding['record_sha256']
    assert row['record_sha256']==binding['question_record_sha256']
    assert {k:row[k]for k in ('release_eligible',)if k in row}==binding['original_release_eligibility']
    assert row['legal_review']['existing_answer_correct']=='NOT_ASSESSED'
    assert row['legal_review']['verdict']=='HOLD'
    assert row['legal_review']['blocker']==binding['legal_blocker']
    assert row['legal_review'].get('independently_expected_key')==binding['original_expected_key_representation']


@pytest.mark.parametrize('defect',['recovery_reference','recovery_report','recovered_policy_raw',
    'recovered_policy_meta','recovered_index_links','target_scope','target_exposed','target_author',
    'new_person_scope','new_person_report','new_unique_original','new_realism_credit','source_kind_missing',
    'source_kind_meta_mismatch','scope_limitation_missing'])
def test_recovered_source_trace_target_blindness_and_reuse_cannot_be_forged(data,defect):
    root=data['root'];scope=data['state'][route.SCOPE_KEY];reviewer=scope['fresh_reviewer']
    if defect=='recovery_reference':scope['recovered_source_reference']['raw_sha256']='0'*64
    elif defect=='recovery_report':(root/route.RECOVERY_REPORT).write_bytes((root/route.RECOVERY_REPORT).read_bytes()+b' ')
    elif defect in {'recovered_policy_raw','recovered_policy_meta','recovered_index_links'}:
        discovery=json.loads((root/route.RECOVERY_REPORT).read_bytes())
        source=discovery['new_source']['official_current_policy_list'if defect.endswith('links')else'policy_metadata']
        key={'recovered_policy_raw':'raw_path','recovered_policy_meta':'metadata_path','recovered_index_links':'links_path'}[defect]
        (root/source[key]).write_bytes(b'Changed retained discovery evidence')
    elif defect=='target_scope':reviewer['target_question_ids']=list(route.IDS[:-1])
    elif defect=='target_exposed':reviewer['current_target_prior_conclusions_read']=True
    elif defect=='target_author':reviewer['current_target_author_or_editor']=True
    elif defect=='new_person_scope':reviewer['new_independent_person_credit']=1
    elif defect=='new_person_report':data['report']['new_independent_people_credit']=1
    elif defect=='new_unique_original':data['report']['new_unique_original_question_credit']=1
    elif defect=='new_realism_credit':data['report']['new_realism_pass_credit']=1
    elif defect=='source_kind_missing':data['report']['records'][0]['legal_review']['authorities'][0].pop('source_kind')
    elif defect=='source_kind_meta_mismatch':data['report']['records'][0]['legal_review']['authorities'][0]['source_kind']='OFFICIAL_REGULATION'
    else:data['report']['records'][0]['legal_review']['source_scope_limitation_ko']=''
    refresh(data)
    with pytest.raises(ValueError):load(data)


def policy_authority(data,source_kind=None,url=None,text_suffix=''):
    """Real public policy bytes, explicitly synthetic metadata, synthetic questions."""
    root=data['root'];metadata=json.loads((root/data['meta']).read_bytes())
    policy=ROOT/'reports/full-corpus-review/remaining-source3-availability/policy2025-02-definitions'
    (root/data['raw']).write_bytes(policy.with_suffix('.pdf').read_bytes())
    (root/data['text']).write_text(policy.with_suffix('.txt').read_text()+text_suffix)
    kind=source_kind or route.POLICY_SOURCE_KIND
    metadata.update(official_url=url or route.POLICY_URL,source_kind=kind,
        raw_sha256=route.sha((root/data['raw']).read_bytes()),text_sha256=route.sha((root/data['text']).read_bytes()),
        method='SYNTHETIC_FIXTURE_TIMES_AND_STATUS_NOT_A_LIVE_RETRIEVAL')
    write(root,data['meta'],metadata)
    for row in data['report']['records']:
        source=row['legal_review']['authorities'][0]
        source.update(official_url=metadata['official_url'],source_kind=kind,
            raw_sha256=metadata['raw_sha256'],text_sha256=metadata['text_sha256'],
            metadata_sha256=route.sha((root/data['meta']).read_bytes()),
            exact_section='Policy2025-02, I and II.F/H/I',
            effective_date_or_version_basis='Printed Adopted8/7/25; independent commencement unknown; agency policy is not enacted CMR')


def test_actual_adopted_policy_is_an_agency_source_without_cmr_or_release_promotion(data):
    policy_authority(data);refresh(data)
    r=load(data)
    assert len(r['records'])==3 and r['progress']['supplementary_new_key_assessed']==3
    assert all(x['legal_review']['verdict']=='HOLD'for x in data['primary'])
    assert all(x['record']['legal_review']['authorities'][0]['source_kind']==route.POLICY_SOURCE_KIND
               for x in r['assessments'].values())
    assert r['progress']['canonical_release_credit']==0


@pytest.mark.parametrize('kind,url,suffix',[
    ('OFFICIAL_REGULATION',None,''),
    ('OFFICIAL_STATUTE',None,''),
    ('OFFICIAL_REGULATION',route.DRAFT_URL,''),
    ('OFFICIAL_REGULATION','https://www.mass.gov/doc/247-cmr-synthetic-proposed/download','\nDRAFT proposed revisions\n'),
    (None,None,'\nDRAFT\n')])
def test_policy_cannot_be_called_cmr_and_draft_documents_cannot_gain_current_law_credit(data,kind,url,suffix):
    policy_authority(data,kind,url,suffix);refresh(data)
    with pytest.raises(ValueError):load(data)


