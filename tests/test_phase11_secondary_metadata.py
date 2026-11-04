"""Fixed procedural retries add bounded coverage and preserve primary failures."""
import copy
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import phase11_secondary_metadata as secondary
import review_queue as queue

REPORT = secondary.PREFIX+'fixture-procedural-review.json'
ENVELOPE = secondary.PREFIX+'fixture-procedural-result.json'
SOURCE = secondary.PREFIX+'evidence/fixture-procedural/source.txt'
RAW = secondary.PREFIX+'evidence/fixture-procedural/source.pdf'
COLLECTION = 'practice_expansion/fixture/questions.json'


def write(root,path,value):
    target = root/path; target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def commit(root):
    queue.git(root,'add','.'); queue.git(root,'commit','-qm','synthetic supplementary consumer fixture')


def save(root,state,report=None,refresh=False):
    if report is not None: write(root,REPORT,report)
    if refresh:
        for row in state['jobs'][0]['result']['results']:
            row['evidence_sha256'] = secondary.sha((root/REPORT).read_bytes())
        for e in state['events']:
            if e['kind'] == 'SUBMIT': e['result_sha256'] = queue.digest(state['jobs'][0]['result'])
        write(root,ENVELOPE,state['jobs'][0]['result'])
        state['phase11_fresh_two_scope']['result_envelope']['raw_sha256'] = secondary.sha((root/ENVELOPE).read_bytes())
    write(root,secondary.STATE,state); commit(root)


@pytest.fixture
def fixture(tmp_path):
    root = tmp_path/'repo'; root.mkdir()
    subprocess.run(['git','init','-q','-b','main',str(root)],check=True)
    queue.git(root,'config','user.name','Fixture'); queue.git(root,'config','user.email','fixture@example.invalid')
    state = queue.empty('independent-legacy')
    scope = dict(schema_version=1, purpose=secondary.PURPOSE, question_ids=list(secondary.IDS),
        previous_evidence={}, root_actor='/root', automatic_release_credit=0)
    state['phase11_fresh_two_scope'] = scope
    questions = {qid:dict(question_id=qid,stem='Read this synthetic original case',
        choices=[dict(id=c,text='Synthetic choice '+c) for c in 'ABCD']) for qid in secondary.IDS}
    primary = [dict(question_id=qid,record_sha256=queue.digest(questions[qid]),release_eligible=False,
        exposure_limitations=dict(prior_item_conclusion_seen=True,fresh_whole_key_credit=0),
        legal_review=dict(verdict='HOLD',existing_answer_correct='NOT_ASSESSED',
            independently_expected_key=[],
            blocker='PRIOR_CONCLUSION_EXPOSURE_REQUIRES_GENUINELY_FRESH_SESSION'),
        realism_review=dict(verdict='FAIL')) for qid in secondary.IDS]
    parent = dict(stage='independent-legacy',independent_of_authors=True,canonical_audit=False,
        canonical_release_credit=0,auditor_instance='GPT:prior-parent-session',
        actor_provenance=dict(actor_id='/root/recover_d_review',session_id='/root/recover_d_review'),
        records=copy.deepcopy(primary))
    parent_path = secondary.PREFIX+'recovered-phase11-d-review.json'
    write(root,parent_path,parent)
    for row in primary:
        scope['previous_evidence'][row['question_id']] = dict(report_path=parent_path,
            report_sha256=secondary.sha((root/parent_path).read_bytes()), record_sha256=queue.digest(row),
            question_record_sha256=row['record_sha256'],original_actor='/root/recover_d_review',
            reason='ROOT_ATTESTED_PRIOR_PROCEDURAL_EXPOSURE_NOT_A_SUBSTANTIVE_LEGAL_VERDICT')
    state['jobs'] = [dict(job_id=secondary.JOB_ID, sequence=1,
        question_hashes={qid:queue.digest(q) for qid,q in questions.items()},
        status='QUEUED',attempt=0,stage='independent-legacy')]
    primary.extend([{'question_id':'another-assessed','legal_review':{'existing_answer_correct':'YES','verdict':'HOLD'},
        'realism_review':{'verdict':'FAIL'}},
        {'question_id':'another-unassessed','legal_review':{'existing_answer_correct':'NOT_ASSESSED','verdict':'HOLD'},
         'realism_review':{'verdict':'FAIL'}}])
    write(root,COLLECTION,{'questions':list(questions.values())})
    collections = dict.fromkeys(secondary.IDS,COLLECTION)
    reviewer = dict(actor_provenance={'actor_id':secondary.ACTOR,'session_id':secondary.ACTOR},auditor='GPT',
        auditor_instance='GPT:actual-fresh-fixture-session',controller_independence_basis='Root assigned a genuinely new fixture actor; declaration is not identity proof',
        known_author_ids=['/root','known-original-author'])
    scope['fresh_reviewer'] = reviewer
    provenance = dict(stage='independent-legacy',independent_of_authors=True,auditor=reviewer['auditor'],
        auditor_instance=reviewer['auditor_instance'],actor_provenance={**reviewer['actor_provenance'],'identity_basis':'Descriptive provenance'},
        canonical_audit=False,canonical_release_credit=0)
    (root/SOURCE).parent.mkdir(parents=True,exist_ok=True); (root/SOURCE).write_bytes(b'Official fixture extracted text')
    (root/RAW).write_bytes(b'Official fixture raw payload')
    authority = dict(official_url='https://example.gov/current-law',exact_section='section 1',law_checked_date='2026-11-03',
        version_and_commencement_basis='Current fixture; separate commencement unknown',evidence_path=SOURCE,
        evidence_sha256=secondary.sha((root/SOURCE).read_bytes()),raw_evidence_path=RAW,raw_sha256=secondary.sha((root/RAW).read_bytes()))
    job = state['jobs'][0]
    report = dict(provenance,job_id=job['job_id'],question_hashes=job['question_hashes'],sources=[authority],records=[])
    for old in primary[:2]:
        record = dict(question_id=old['question_id'],record_sha256=old['record_sha256'],
            read_scope={'original_stem':True,'all_choices_read':['A','B','C','D'],
                'complete_core_reasoning_read':True,'stored_key_read':True,'learning_boundary_read':True,
                'all_choice_explanations_read':['A','B','C','D'],'hidden_statement_truth_read':False,
                'prior_question_author_or_independent_verdicts_read':False},release_eligible=False,
            legal_review=dict(existing_answer_correct='YES',verdict='KEEP',authorities=[authority],
                              finding_ko='Synthetic official-source assessment'),
            realism_review=dict(verdict='PASS',finding_ko='Synthetic style assessment'))
        report['records'].append(record)
    write(root,REPORT,report)
    manifest = dict(provenance,question_hashes=job['question_hashes'],worker_commit='b'*40,
        results=[dict(question_id=qid,disposition='INDEPENDENT_ASSESSED',evidence_path=REPORT,
                      evidence_sha256=secondary.sha((root/REPORT).read_bytes())) for qid in secondary.IDS])
    # Standard envelopes may omit canonical fields; no new controller format is required.
    manifest.pop('canonical_audit'); manifest.pop('canonical_release_credit')
    write(root,ENVELOPE,manifest)
    scope['result_envelope'] = {'path':ENVELOPE,'raw_sha256':secondary.sha((root/ENVELOPE).read_bytes())}
    job.update(status='INTEGRATED',worker=secondary.ACTOR,attempt=1,result=manifest,
        integrated_commit='c'*40,integrated_at='2026-11-03T23:28:20+00:00')
    job['worker_branch'] = 'mission/'+job['job_id']+'-attempt-1'
    state['events'] = [dict(kind='CLAIM',job_id=job['job_id'],worker=secondary.ACTOR,attempt=1),
        dict(kind='SUBMIT',job_id=job['job_id'],result_sha256=queue.digest(manifest)),
        dict(kind='INTEGRATE',job_id=job['job_id'],commit=job['integrated_commit'])]
    save(root,state)
    return root,state,report,primary,questions,collections


def load(fixture):
    root,state,report,primary,questions,collections = fixture
    return secondary.load_metadata(root,primary,questions,collections)


def test_integrated_retry_adds_only_unique_key_coverage_and_preserves_every_primary_failure(fixture):
    root,state,report,primary,questions,collections = fixture
    before = copy.deepcopy(primary); original = (root/state['phase11_fresh_two_scope']['previous_evidence'][secondary.IDS[0]]['report_path']).read_bytes()
    result = load(fixture); p = result['progress']
    assert p['primary_key_assessed'] == 1 and p['primary_keys_unassessed'] == 3
    assert p['effective_key_assessed'] == 3 and p['effective_keys_unassessed'] == 1
    assert p['unique_originals_read'] == 4 and p['supplementary_new_key_assessed'] == 2
    assert p['canonical_release_credit'] == 0
    assert primary == before and primary[2]['realism_review']['verdict'] == 'FAIL'
    assert primary[0]['legal_review']['existing_answer_correct'] == 'NOT_ASSESSED'
    assert primary[0]['legal_review']['verdict'] == 'HOLD'
    for review in result['assessments'].values():
        assert review['supplementary_only'] and review['does_not_override_primary'] and review['canonical_release_credit'] == 0
        assert review['record']['legal_review']['verdict'] == 'KEEP'
    assert (root/state['phase11_fresh_two_scope']['previous_evidence'][secondary.IDS[0]]['report_path']).read_bytes() == original


@pytest.mark.parametrize('status',['QUEUED','LEASED','SUBMITTED'])
def test_unintegrated_is_zero_credit_and_fresh_files_are_not_read(fixture,status):
    root,state,report,*_ = fixture; state['jobs'][0]['status'] = status; save(root,state)
    (root/REPORT).unlink(); (root/ENVELOPE).unlink(); (root/RAW).unlink()
    p = load(fixture)['progress']
    assert p['effective_key_assessed'] == p['primary_key_assessed'] == 1
    assert p['supplementary_integrated_records'] == p['supplementary_new_key_assessed'] == 0


def test_unassessed_retry_is_not_new_key_credit_and_legal_hold_is_not_hidden(fixture):
    root,state,report,*_ = fixture
    report['records'][0]['legal_review'].update(existing_answer_correct='NOT_ASSESSED',verdict='HOLD')
    report['records'][1]['legal_review'].update(existing_answer_correct='AMBIGUOUS',verdict='HOLD')
    save(root,state,report,refresh=True)
    result = load(fixture)
    assert result['progress']['supplementary_new_key_assessed'] == 1
    assert result['progress']['effective_key_assessed'] == 2
    assert result['progress']['effective_keys_unassessed'] == 2
    assert result['progress']['supplementary_legal_verdict_counts'] == {'HOLD':2}
    assert result['assessments'][secondary.IDS[1]]['record']['legal_review']['verdict'] == 'HOLD'


@pytest.mark.parametrize('defect',['header_extra','header_other_na','extra_job','extra_job_unintegrated','job_extra','job_id',
    'wrong_parent','parent_raw','parent_row','old_actor','current_body','uncommitted_body','session','instance','known_author',
    'no_reviewer','report_raw','raw_source','text_source','envelope_raw','envelope_result','submit_event','integrate_event',
    'claim_event','worker_commit','branch','canonical','row_release','unknown_key','extra_report_id','duplicate_result',
    'forged_report_actor','new_exposure','incomplete_read','prior_instance'])
def test_scope_history_identity_current_hash_and_raw_mutations_fail_closed(fixture,defect):
    root,state,report,primary,questions,collections = fixture
    scope = state['phase11_fresh_two_scope']; job = state['jobs'][0]; refresh = False; save_report = False
    if defect == 'header_extra': scope['question_ids'].append('another-unassessed')
    elif defect == 'header_other_na': scope['question_ids'][0] = 'another-unassessed'
    elif defect in {'extra_job','extra_job_unintegrated'}:
        extra = copy.deepcopy(job); extra.update(job_id='unexpected-generic-plan',sequence=2,
            status='LEASED' if defect.endswith('unintegrated') else 'INTEGRATED',question_hashes={'another-unassessed':'a'*64})
        state['jobs'].append(extra)
    elif defect == 'job_extra': job['question_hashes']['another-unassessed'] = 'a'*64
    elif defect == 'job_id': job['job_id'] = 'different-two-job'
    elif defect == 'wrong_parent': scope['previous_evidence'][secondary.IDS[0]]['report_path'] = secondary.PREFIX+'independent-phase2-e-review.json'
    elif defect == 'parent_raw': scope['previous_evidence'][secondary.IDS[0]]['report_sha256'] = '0'*64
    elif defect == 'parent_row': scope['previous_evidence'][secondary.IDS[0]]['record_sha256'] = '0'*64
    elif defect == 'old_actor': scope['fresh_reviewer']['actor_provenance']['actor_id'] = '/root/recover_d_review'
    elif defect in {'current_body','uncommitted_body'}:
        questions[secondary.IDS[0]] = dict(questions[secondary.IDS[0]],stem='Changed original body')
        write(root,COLLECTION,{'questions':list(questions.values())})
    elif defect == 'session': job['result']['actor_provenance']['session_id'] = 'renamed-session'
    elif defect == 'prior_instance':
        binding = scope['previous_evidence'][secondary.IDS[0]]
        scope['fresh_reviewer']['auditor_instance'] = json.loads((root/binding['report_path']).read_bytes())['auditor_instance']
    elif defect == 'instance': scope['fresh_reviewer']['auditor_instance'] = 'another-instance'
    elif defect == 'known_author': scope['fresh_reviewer']['known_author_ids'].append(secondary.ACTOR)
    elif defect == 'no_reviewer': scope.pop('fresh_reviewer')
    elif defect == 'report_raw': (root/REPORT).write_bytes((root/REPORT).read_bytes()+b' ')
    elif defect == 'raw_source': (root/RAW).write_bytes(b'changed raw source')
    elif defect == 'text_source': (root/SOURCE).write_bytes(b'changed extracted text')
    elif defect == 'envelope_raw': scope['result_envelope']['raw_sha256'] = '0'*64
    elif defect == 'envelope_result':
        write(root,ENVELOPE,dict(job['result'],worker_commit='d'*40))
        scope['result_envelope']['raw_sha256'] = secondary.sha((root/ENVELOPE).read_bytes())
    elif defect.endswith('_event'): state['events'] = [e for e in state['events'] if e['kind'] != defect[:-6].upper()]
    elif defect == 'worker_commit': job['result']['worker_commit'] = 'z'*40
    elif defect == 'branch': job['worker_branch'] = 'mission/unrelated-branch'
    elif defect == 'canonical': report['canonical_release_credit'] = 1; save_report = refresh = True
    elif defect == 'row_release': report['records'][0]['release_eligible'] = True; save_report = refresh = True
    elif defect == 'unknown_key': report['records'][0]['legal_review']['existing_answer_correct'] = 'PASS'; save_report = refresh = True
    elif defect == 'extra_report_id': report['records'].append(copy.deepcopy(report['records'][0])); save_report = refresh = True
    elif defect == 'duplicate_result': job['result']['results'][1] = copy.deepcopy(job['result']['results'][0])
    elif defect == 'forged_report_actor': report['actor_provenance']['actor_id'] = 'forged'; save_report = refresh = True
    elif defect == 'incomplete_read': report['records'][0]['read_scope']['stored_key_read'] = False; save_report = refresh = True
    elif defect == 'new_exposure': report['records'][0]['read_scope']['hidden_statement_truth_read'] = True; save_report = refresh = True
    if defect != 'uncommitted_body': save(root,state,report if save_report else None,refresh)
    with pytest.raises(ValueError): load(fixture)


def test_parent_cannot_be_relabelled_from_a_substantive_hold_even_if_new_hashes_are_supplied(fixture):
    root,state,report,primary,*_ = fixture; qid = secondary.IDS[0]
    binding = state['phase11_fresh_two_scope']['previous_evidence'][qid]
    parent = json.loads((root/binding['report_path']).read_bytes())
    row = next(r for r in parent['records'] if r['question_id'] == qid)
    row['legal_review']['blocker'] = 'ACTUAL_LEGAL_SOURCE_UNRESOLVED'
    primary[0] = copy.deepcopy(row); write(root,binding['report_path'],parent)
    binding['record_sha256'] = queue.digest(row); binding['report_sha256'] = secondary.sha((root/binding['report_path']).read_bytes())
    save(root,state)
    with pytest.raises(ValueError,match='substantive or other NOT_ASSESSED'): load(fixture)


@pytest.mark.parametrize('mutation',['no_exposure','credit','provisional_key'])
def test_parent_exposure_contract_cannot_be_rehashed_away(fixture,mutation):
    root,state,_,primary,*_ = fixture
    scope = state['phase11_fresh_two_scope']; binding = scope['previous_evidence'][secondary.IDS[0]]
    parent = json.loads((root/binding['report_path']).read_bytes())
    row = parent['records'][0]
    if mutation == 'no_exposure': row['exposure_limitations']['prior_item_conclusion_seen'] = False
    elif mutation == 'credit': row['exposure_limitations']['fresh_whole_key_credit'] = 1
    else: row['legal_review']['independently_expected_key'] = ['A']
    primary[0] = copy.deepcopy(row)
    write(root,binding['report_path'],parent)
    for item in scope['previous_evidence'].values():
        item['report_sha256'] = secondary.sha((root/item['report_path']).read_bytes())
    binding['record_sha256'] = queue.digest(row)
    save(root,state)
    with pytest.raises(ValueError,match='substantive or other NOT_ASSESSED'): load(fixture)


def test_counts_are_unions_without_fixed_baseline_totals_or_duplicate_originals(fixture):
    _,_,report,primary,*_ = fixture
    primary += [{'question_id':'later-'+str(i),'legal_review':{'existing_answer_correct':'YES','verdict':'HOLD'}} for i in range(7)]
    p = secondary.counts(primary,report['records'])
    assert p['primary_key_assessed'] == 8 and p['effective_key_assessed'] == 10 and p['unique_originals_read'] == 11
    assert secondary.counts(report['records'],report['records'])['supplementary_new_key_assessed'] == 0
    with pytest.raises(ValueError,match='Duplicate supplementary'): secondary.counts(primary,report['records']*2)
    with pytest.raises(ValueError,match='Duplicate primary'): secondary.counts(primary+primary[:1],report['records'])


def test_two_consumers_union_without_overwriting_original_progress_or_duplicate_credit(fixture):
    _,_,report,primary,*_ = fixture
    old_primary = [{'question_id':qid,'legal_review':{'existing_answer_correct':'NOT_ASSESSED','verdict':'HOLD'}}
                   for qid in ('MA-CASE-0401','MA-CASE-0441')]
    old_records = [dict(row,legal_review={'existing_answer_correct':'YES','verdict':'KEEP'}) for row in old_primary]
    first = {'assessments':{row['question_id']:{'record':row} for row in old_records},'records':old_records}
    second = load(fixture)
    before = copy.deepcopy((primary,first,second))
    combined = secondary.combine_metadata(primary+old_primary,first,second)
    assert combined['progress']['unique_originals_read'] == 6
    assert combined['progress']['primary_key_assessed'] == 1
    assert combined['progress']['effective_key_assessed'] == 5
    assert combined['progress']['supplementary_new_key_assessed'] == 4
    assert len(combined['assessments']) == 4
    assert (primary,first,second) == before
    with pytest.raises(ValueError,match='Overlapping'):
        secondary.combine_metadata(primary+old_primary,second,second)


def test_absent_new_state_carries_no_credit_and_does_not_read_future_reports(fixture):
    root,_,_,primary,questions,collections = fixture
    (root/secondary.STATE).unlink()
    result = secondary.load_metadata(root,primary,questions,collections)
    assert result['assessments'] == {} and result['records'] == []
    assert result['progress']['effective_key_assessed'] == 1


@pytest.mark.parametrize('field',['version_and_commencement_basis','raw_evidence_path','raw_sha256'])
def test_official_authority_requires_raw_payload_and_explicit_commencement_limit(fixture,field):
    root,state,report,*_ = fixture
    for row in report['records']:
        row['legal_review']['authorities'][0].pop(field,None)
    save(root,state,report,refresh=True)
    with pytest.raises(ValueError,match='Incomplete supplementary official authority'):
        load(fixture)


def test_shallow_consumer_needs_no_original_worker_objects_or_branches(fixture,tmp_path):
    root,state,report,primary,questions,collections = fixture; destination = tmp_path/'shallow'
    subprocess.run(['git','clone','-q','--depth','1',root.as_uri(),str(destination)],check=True)
    with pytest.raises(subprocess.CalledProcessError): queue.git(destination,'cat-file','-e',state['jobs'][0]['result']['worker_commit']+'^{commit}')
    assert secondary.load_metadata(destination,primary,questions,collections) == load(fixture)


def test_secondary_keep_cannot_authorize_default_return_or_hide_primary_failures(fixture):
    from build_full_corpus_review import validate_default_review_safety
    _,_,_,primary,*_ = fixture
    supplemental = load(fixture)['records']
    with pytest.raises(ValueError,match='Uncontained independent finding'):
        validate_default_review_safety([secondary.IDS[0]],{},primary+supplemental)
    with pytest.raises(ValueError,match='Uncontained independent finding'):
        validate_default_review_safety(['another-assessed'],{},primary+supplemental)
    validate_default_review_safety([],{},primary+supplemental)


