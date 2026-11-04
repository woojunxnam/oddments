"""Fixed procedural retries add bounded coverage and preserve primary failures."""
import copy
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import phase11_context38_metadata as secondary
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
        state['phase11_context38_scope']['result_envelope']['raw_sha256'] = secondary.sha((root/ENVELOPE).read_bytes())
    write(root,secondary.STATE,state); commit(root)


@pytest.fixture
def fixture(tmp_path):
    root = tmp_path/'repo'; root.mkdir()
    subprocess.run(['git','init','-q','-b','main',str(root)],check=True)
    queue.git(root,'config','user.name','Fixture'); queue.git(root,'config','user.email','fixture@example.invalid')
    state = queue.empty('independent-legacy')
    scope = dict(schema_version=1, purpose=secondary.PURPOSE, question_ids=list(secondary.IDS),
        previous_evidence={}, root_actor='/root', automatic_release_credit=0)
    state['phase11_context38_scope'] = scope
    questions = {qid:dict(question_id=qid,stem='Read this synthetic original case',
        choices=[dict(id=c,text='Synthetic choice '+c) for c in 'ABCD']) for qid in secondary.IDS}
    primary = [dict(question_id=qid,record_sha256=queue.digest(questions[qid]),release_eligible=False,
                legal_review=dict(verdict='KEEP',existing_answer_correct='YES'),
        realism_review=dict(verdict='PASS' if i < 7 else 'FAIL')) for i,qid in enumerate(secondary.IDS)]
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
            reason='ROOT_ATTESTED_AGGREGATE_PRIOR_CONCLUSION_EXPOSURE_NOT_FRESH')
    checkpoint_path=root/secondary.CHECKPOINT; checkpoint_path.parent.mkdir(parents=True,exist_ok=True)
    checkpoint_path.write_bytes((ROOT/secondary.CHECKPOINT).read_bytes())
    disclosure=dict(schema_version=1,purpose='ROOT_ATTESTED_AGGREGATE_PRIOR_CONCLUSION_EXPOSURE_NO_FRESH_CREDIT',
        controller_actor='/root',context_conditioned_actor='/root/recover_d_review',spawn_context='fork_turns_all',
        observed_at_utc='2026-11-04T13:07:49+00:00',question_ids=list(secondary.IDS),actual_new_reviewer=secondary.ACTOR,
        primary_fresh_key_credit=0,canonical_release_credit=0,reason='Synthetic actual root exposure disclosure',
        checkpoint={'path':secondary.CHECKPOINT,'raw_sha256':secondary.CHECKPOINT_SHA},
        parent_report={'path':parent_path,'raw_sha256':secondary.sha((root/parent_path).read_bytes())},
        prior_summary=dict(assigned_count=40,legal_keep=38,legal_hold=2,key_yes=38,key_ambiguous=2,
            ambiguous_ids=['MA-EXP-0338','MA-EXP-0339']))
    write(root,secondary.DISCLOSURE,disclosure)
    scope['exposure_disclosure']={'path':secondary.DISCLOSURE,'raw_sha256':secondary.sha((root/secondary.DISCLOSURE).read_bytes())}
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
    report['native_assignment_binding'] = dict(job_id=job['job_id'],sequence=1,
        question_hashes=job['question_hashes'],stage='independent-legacy',worker=secondary.ACTOR,
        worker_branch='mission/'+job['job_id']+'-attempt-1',attempt=1)
    for old in primary[:38]:
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


def test_exact38_integrated_fresh_keys_replace_only_conditioned_credit(fixture):
    _,_,_,primary,*_ = fixture; before=copy.deepcopy(primary)
    result=load(fixture); p=result['progress']
    assert len(result['primary_limitations']) == 38
    assert result['excluded_primary_key_ids'] == list(secondary.IDS)
    assert p['raw_primary_key_assessed'] == 39 and p['primary_key_assessed'] == 1
    assert p['effective_key_assessed'] == 39 and p['supplementary_new_key_assessed'] == 38
    assert p['unique_originals_read'] == 40
    assert p['excluded_context_conditioned_primary_realism_pass'] == 7
    assert p['fresh_context38_realism_pass'] == 38
    assert p['fresh_context38_pass_with_preserved_primary_fail'] == 31
    assert p['effective_realism_pass'] == 7
    assert primary == before and all(row['legal_review']['existing_answer_correct']=='YES' for row in primary[:38])


@pytest.mark.parametrize('status',['QUEUED','LEASED','SUBMITTED'])
def test_unintegrated_fresh38_immediately_excludes_conditioned_primary_keys(fixture,status):
    root,state,_,primary,*_ = fixture
    state['jobs'][0]['status']=status;save(root,state)
    (root/REPORT).unlink();(root/ENVELOPE).unlink()
    result=load(fixture)
    assert len(result['excluded_primary_key_ids']) == 38
    assert result['records'] == []
    assert result['progress']['effective_key_assessed'] == 1
    assert result['progress']['supplementary_new_key_assessed'] == 0
    assert all(row['legal_review']['existing_answer_correct']=='YES' for row in primary[:38])


@pytest.mark.parametrize('mutation',['actor','scope','summary','fork','credit','parent','checkpoint','time','nohash'])
def test_exposure_disclosure_cannot_be_rehashed_to_change_scope_or_history(fixture,mutation):
    root,state,*_=fixture;scope=state['phase11_context38_scope']
    value=json.loads((root/secondary.DISCLOSURE).read_bytes())
    if mutation=='actor':value['context_conditioned_actor']='/root/somebody-else'
    elif mutation=='scope':value['question_ids']=value['question_ids'][:-1]
    elif mutation=='summary':value['prior_summary']['key_yes']=37
    elif mutation=='fork':value['spawn_context']='fork_turns_none'
    elif mutation=='credit':value['primary_fresh_key_credit']=38
    elif mutation=='parent':value['parent_report']['raw_sha256']='0'*64
    elif mutation=='checkpoint':value['checkpoint']['raw_sha256']='0'*64
    elif mutation=='time':value['observed_at_utc']='2026-11-04T13:07:49'
    write(root,secondary.DISCLOSURE,value)
    scope['exposure_disclosure']['raw_sha256']=secondary.sha((root/secondary.DISCLOSURE).read_bytes())
    if mutation=='nohash':scope['exposure_disclosure'].pop('raw_sha256')
    save(root,state)
    with pytest.raises(ValueError):load(fixture)


@pytest.mark.parametrize('mutation',['extra_job','extra_id','old_actor','parent_row','current_object','raw','text','native','exposure'])
def test_scope_parent_identity_current_content_and_sources_fail_closed(fixture,mutation):
    root,state,report,primary,questions,*_=fixture;scope=state['phase11_context38_scope'];refresh=False
    if mutation=='extra_job':state['jobs'].append(copy.deepcopy(state['jobs'][0]))
    elif mutation=='extra_id':state['jobs'][0]['question_hashes']['MA-EXP-0338']='0'*64
    elif mutation=='old_actor':scope['fresh_reviewer']['actor_provenance']['actor_id']='/root/recover_d_review'
    elif mutation=='parent_row':scope['previous_evidence'][secondary.IDS[0]]['record_sha256']='0'*64
    elif mutation=='current_object':
        questions[secondary.IDS[0]]['stem']='Changed'
        write(root,COLLECTION,{'questions':list(questions.values())})
    elif mutation=='raw':(root/RAW).write_bytes(b'altered raw')
    elif mutation=='text':(root/SOURCE).write_bytes(b'altered text')
    elif mutation=='native':report['native_assignment_binding']['attempt']=2;refresh=True
    elif mutation=='exposure':report['records'][0]['read_scope']['prior_question_author_or_independent_verdicts_read']=True;refresh=True
    save(root,state,report if refresh else None,refresh)
    with pytest.raises(ValueError):load(fixture)


def test_aggregate_union_excludes38_before_adding_all_actual_fresh_disjoint_results(fixture):
    *_,primary,questions,collections=fixture
    new=load(fixture)
    old_primary=[dict(question_id=qid,legal_review=dict(existing_answer_correct='NOT_ASSESSED'),realism_review=dict(verdict='FAIL'))
                 for qid in ('MA-EXP-0338','MA-EXP-0339','MA-CASE-0401','MA-CASE-0441')]
    old_records=[dict(row,legal_review=dict(existing_answer_correct='YES',verdict='KEEP'),realism_review=dict(verdict='PASS')) for row in old_primary]
    older={'assessments':{row['question_id']:{'record':row} for row in old_records},'records':old_records}
    before=copy.deepcopy(primary+old_primary)
    result=secondary.combine_metadata(primary+old_primary,older,new)
    assert result['progress']['unique_originals_read']==44
    assert result['progress']['primary_key_assessed']==1
    assert result['progress']['effective_key_assessed']==43
    assert result['progress']['supplementary_new_key_assessed']==42
    assert primary+old_primary==before
    with pytest.raises(ValueError):secondary.combine_metadata(primary+old_primary,new,new)


def test_fresh_positive_cannot_authorize_a_default_return(fixture):
    result=load(fixture)
    assert len(result['records'])==38
    with pytest.raises(ValueError,match='cannot return to default'):
        secondary.validate_default_safety([secondary.IDS[0]],result)
    secondary.validate_default_safety([],result)


def test_retained_exposure_cannot_lose_queue_to_restore_primary_credit(fixture):
    root,*_=fixture
    (root/secondary.STATE).unlink()
    with pytest.raises(ValueError,match='cannot restore conditioned primary credit'):
        load(fixture)


@pytest.mark.parametrize('exposure',['boolean','explicit_accidental'])
def test_reexposed_unassessed_key_cannot_reintroduce_realism_pass_credit(fixture,exposure):
    root,state,report,*_=fixture
    row=report['records'][0]
    if exposure=='boolean':row['read_scope']['prior_question_author_or_independent_verdicts_read']=True
    else:row['read_scope']['hidden_truth']='ACCIDENTAL prior exposure'
    row['legal_review'].update(existing_answer_correct='NOT_ASSESSED',verdict='HOLD')
    save(root,state,report,refresh=True)
    p=load(fixture)['progress']
    assert p['effective_key_assessed']==38
    assert p['fresh_context38_pass_with_procedural_exposure']==1
    assert p['effective_realism_pass']==6


