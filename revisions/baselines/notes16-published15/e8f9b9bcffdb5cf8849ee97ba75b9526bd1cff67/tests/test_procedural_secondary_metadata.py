"""Fixed procedural retries add bounded coverage and preserve primary failures."""
import copy
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import procedural_secondary_metadata as secondary
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
        state['procedural_recheck_scope']['result_envelope']['raw_sha256'] = secondary.sha((root/ENVELOPE).read_bytes())
    write(root,secondary.STATE,state); commit(root)


@pytest.fixture
def fixture(tmp_path):
    root = tmp_path/'repo'; root.mkdir()
    subprocess.run(['git','init','-q','-b','main',str(root)],check=True)
    queue.git(root,'config','user.name','Fixture'); queue.git(root,'config','user.email','fixture@example.invalid')
    state = json.loads((ROOT/secondary.STATE).read_bytes())
    scope = state['procedural_recheck_scope']; primary = []
    ledger = {r['question_id']:r for r in map(json.loads,(ROOT/'reports/full-corpus-review/question-ledger.jsonl').read_text().splitlines())}
    questions = {}; banks = {}
    for qid,binding in scope['previous_evidence'].items():
        raw = (ROOT/binding['report_path']).read_bytes()
        target = root/binding['report_path']; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(raw)
        parent = json.loads(raw); primary.append(next(r for r in parent['records'] if r['question_id'] == qid))
        path = ledger[qid]['collection']
        if path not in banks: banks[path] = json.loads((ROOT/path).read_bytes())
        questions[qid] = next(q for q in banks[path]['questions'] if q['question_id'] == qid)
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
    before = copy.deepcopy(primary); original = (root/state['procedural_recheck_scope']['previous_evidence'][secondary.IDS[0]]['report_path']).read_bytes()
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
    assert (root/state['procedural_recheck_scope']['previous_evidence'][secondary.IDS[0]]['report_path']).read_bytes() == original


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


@pytest.mark.parametrize('defect',['header_extra','header_other_na','extra_job','extra_job_unintegrated','job_extra',
    'wrong_parent','parent_raw','parent_row','old_actor','current_body','uncommitted_body','session','instance','known_author',
    'no_reviewer','report_raw','raw_source','text_source','envelope_raw','envelope_result','submit_event','integrate_event',
    'claim_event','worker_commit','branch','canonical','row_release','unknown_key','extra_report_id','duplicate_result',
    'forged_report_actor','new_exposure','incomplete_read','prior_instance'])
def test_scope_history_identity_current_hash_and_raw_mutations_fail_closed(fixture,defect):
    root,state,report,primary,questions,collections = fixture
    scope = state['procedural_recheck_scope']; job = state['jobs'][0]; refresh = False; save_report = False
    if defect == 'header_extra': scope['question_ids'].append('another-unassessed')
    elif defect == 'header_other_na': scope['question_ids'][0] = 'another-unassessed'
    elif defect in {'extra_job','extra_job_unintegrated'}:
        extra = copy.deepcopy(job); extra.update(job_id='unexpected-generic-plan',sequence=2,
            status='LEASED' if defect.endswith('unintegrated') else 'INTEGRATED',question_hashes={'another-unassessed':'a'*64})
        state['jobs'].append(extra)
    elif defect == 'job_extra': job['question_hashes']['another-unassessed'] = 'a'*64
    elif defect == 'wrong_parent': scope['previous_evidence'][secondary.IDS[0]]['report_path'] = scope['previous_evidence'][secondary.IDS[1]]['report_path']
    elif defect == 'parent_raw': scope['previous_evidence'][secondary.IDS[0]]['report_sha256'] = '0'*64
    elif defect == 'parent_row': scope['previous_evidence'][secondary.IDS[0]]['record_sha256'] = '0'*64
    elif defect == 'old_actor': scope['fresh_reviewer']['actor_provenance']['actor_id'] = '/root/independent_case_e'
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
    binding = state['procedural_recheck_scope']['previous_evidence'][qid]
    parent = json.loads((root/binding['report_path']).read_bytes())
    row = next(r for r in parent['records'] if r['question_id'] == qid)
    row['legal_review']['blocker'] = 'ACTUAL_LEGAL_SOURCE_UNRESOLVED'
    primary[0] = copy.deepcopy(row); write(root,binding['report_path'],parent)
    binding['record_sha256'] = queue.digest(row); binding['report_sha256'] = secondary.sha((root/binding['report_path']).read_bytes())
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


def test_builder_exposes_secondary_separately_and_keeps_all_primary_and_publication_fields(fixture,monkeypatch):
    import build_full_corpus_review as builder
    root,state,report,_,questions,collections = fixture
    real_load = secondary.load_metadata; captured = {}
    def load_fixture(repo,primary,current_questions,current_collections):
        captured['primary'] = copy.deepcopy(primary)
        value = real_load(root,primary,questions,collections)
        captured['progress'] = value['progress']
        return value
    monkeypatch.setattr(secondary,'load_metadata',load_fixture)
    outputs = builder.build()
    rows = {r['question_id']:r for r in map(json.loads,outputs[ROOT/'reports/full-corpus-review/question-ledger.jsonl'].splitlines())}
    progress = json.loads(outputs[ROOT/'reports/full-corpus-review/progress.json'])
    originals = {r['question_id']:r for r in captured['primary']}
    for qid in secondary.IDS:
        row = rows[qid]
        assert row['independent_legacy_legal_assessment'] == originals[qid]['legal_review']
        assert row['independent_legacy_realism_assessment'] == originals[qid]['realism_review']
        assert row['independent_legacy_legal_assessment']['existing_answer_correct'] == 'NOT_ASSESSED'
        assert row['independent_legacy_supplementary_assessment']['record']['legal_review']['verdict'] == 'KEEP'
        assert row['answer_key_assessment'] == 'INDEPENDENT_LEGACY_NOT_ASSESSED'
        assert row['disposition'] == 'HOLD_FOR_LEGAL_REVIEW'
        assert row['publication_status'] == 'PRACTICE_CONFIG_ARCHIVE'
    assert progress['independent_legacy_legal_assessed'] == captured['progress']['effective_key_assessed']
    assert progress['independent_legacy_originals_read'] == len(originals)
    assert progress['independent_legacy_keys_unassessed'] == captured['progress']['primary_keys_unassessed']-2
    assert progress['independent_legacy_procedural_supplementary_review']['canonical_release_credit'] == 0
    assert progress['canonical_independent_audit_this_session'] == 'NOT_RUN'
    # Every primary FAIL remains present even when an unrelated supplementary KEEP is added.
    for qid,record in originals.items():
        if record['realism_review']['verdict'] == 'FAIL':
            assert rows[qid]['independent_legacy_realism_assessment'] == record['realism_review']


def test_quality_scope_explains_unique_count_and_preserved_primary_holds(fixture,tmp_path,monkeypatch):
    import build_quality_status as quality
    result = load(fixture)
    for relative in ('practice_expansion/2026-10-28-representative/selection.json',
        'reports/representative-rewrite/pattern-metrics.json','reports/full-corpus-review/progress.json',
        'reports/full-corpus-review/inventory-definitions.json','site/practice-expansion/quality-review.html'):
        target = tmp_path/relative; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes((ROOT/relative).read_bytes())
    path = tmp_path/'reports/full-corpus-review/progress.json'; progress = json.loads(path.read_bytes())
    progress['independent_legacy_procedural_supplementary_review'] = result['progress']
    path.write_text(json.dumps(progress))
    monkeypatch.setattr(quality,'ROOT',tmp_path)
    _,html = quality.output()
    assert '고유 ID 기준' in html and '기존 primary 정답 평가' in html
    assert 'NOT_ASSESSED·HOLD·현실성 FAIL' in html and '정답 평가 수는 법규 PASS 수가 아닙니다' in html
