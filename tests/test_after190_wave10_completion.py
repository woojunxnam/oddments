"""Bounded unpublished15 extension; fixtures below create no legal assessment."""
import copy
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import notes_after190_annotation as a
from published15_test_view import published15_root
ROOT=published15_root(ROOT)


@pytest.fixture
def state():
    return json.loads((ROOT/a.LEGACY_STATE).read_bytes())


def complete_shape(state):
    """In-memory shape only: cannot pass the actual report/source gate."""
    for job in state['jobs'][33:]:
        job.update(status='INTEGRATED',result={'SYNTHETIC_SCOPE_ONLY':True},
                   integrated_commit='1'*40,integrated_at='2026-11-04T00:00:00Z')
        state['events'].append(dict(kind='INTEGRATE',job_id=job['job_id'],commit=job['integrated_commit']))
    return state


def pending_shape(state):
    """An explicit historical lifecycle fixture, not the live completed state."""
    ids={job['job_id'] for job in state['jobs'][33:]}
    for job in state['jobs'][33:]:
        job['status']='LEASED'
        for key in ('result','submitted_at','integrated_commit','integrated_at'):
            job.pop(key,None)
    state['events']=[event for event in state['events'] if not
                     (event.get('job_id') in ids and event.get('kind') in {'SUBMIT','INTEGRATE'})]
    return state


def test_exact_allocation_distinguishes_actual_receipts_from_a_pending_fixture(state):
    assert len(state['jobs'])==37
    assert a.WAVE10_DEFINITION_COMMIT=='08a417e2e53e83501e2756792cda0168fe4ae8a7'
    assert all((j['job_id'],a.question_queue.digest(j['question_hashes']),j['worker'])==a.WAVE10[j['sequence']]
               for j in state['jobs'][33:])
    assert all(j['status']=='INTEGRATED' and j.get('result') for j in state['jobs'][33:])
    a.validate_legacy_scope(state)
    pending=pending_shape(copy.deepcopy(state))
    assert all(j['status']=='LEASED' and 'result' not in j for j in pending['jobs'][33:])
    with pytest.raises(ValueError,match='pending/LEASED'):
        a.validate_legacy_scope(pending)


@pytest.mark.parametrize('defect',['old33_only','extra38','id','hash','actor','stage','priority',
                                  'policy','missing_ig','fake_ig','still_submitted','old_history','old_negative_receipt'])
def test_scope_or_status_edit_cannot_create_a_future_receipt(state,defect):
    state=complete_shape(state);a.validate_legacy_scope(state)
    job=state['jobs'][35]
    if defect=='old33_only':state['jobs']=state['jobs'][:33]
    elif defect=='extra38':state['jobs'].append(dict(job,sequence=38))
    elif defect=='id':job['job_id']+='-other'
    elif defect=='hash':job['question_hashes'][next(iter(job['question_hashes']))]='0'*64
    elif defect=='actor':job['worker']='/root/unapproved-actor'
    elif defect=='stage':job['stage']='author'
    elif defect=='priority':job['priority_source_sha256']['site/practice-expansion/publication.json']='0'*64
    elif defect=='policy':job['selection_policy']='ARBITRARY'
    elif defect=='missing_ig':state['events']=[e for e in state['events']if not(e.get('kind')=='INTEGRATE'and e.get('job_id')==job['job_id'])]
    elif defect=='fake_ig':job.pop('result')
    elif defect=='still_submitted':job['status']='SUBMITTED'
    elif defect=='old_negative_receipt':
        state['jobs'][29]['result']['results'][0]['evidence_sha256']='0'*64
    else:state['events']=[e for e in state['events']if not(e.get('kind')=='INTEGRATE'and e.get('job_id')==state['jobs'][32]['job_id'])]
    with pytest.raises(ValueError):a.validate_legacy_scope(state)


def test_shape_only_future_ig_cannot_pass_the_actual_source_gate(state):
    state=complete_shape(state);a.validate_legacy_scope(state)
    with pytest.raises(ValueError,match='Result stage|IDs/hashes'):
        a.bind_legacy_checkpoint(ROOT,state['jobs'][35],state,{})


def test_pending_actual_sources_cannot_reuse_old_unpublished_ready_manifest_or_write(monkeypatch):
    paths=[a.MANIFEST,a.EXPORT,a.BUILD,a.PARENT]
    before={p:(ROOT/p).read_bytes()for p in paths}
    # A stale candidate may already say ready=true. Actual new jobs still block.
    saved=json.loads(before[a.MANIFEST]);saved['annotation_inputs_ready']=True
    original=a.safe_bytes
    monkeypatch.setattr(a,'safe_bytes',lambda root,p:a.notes_queue.encoded(saved)if p==a.MANIFEST else original(root,p))
    # The real four jobs are now integrated. Inject the explicitly pending
    # checkpoint at the reader boundary to keep testing the refusal contract.
    pending=pending_shape(json.loads((ROOT/a.LEGACY_STATE).read_bytes()))
    read=a.committed
    def pending_checkpoint(root,path,bindings):
        if path==a.LEGACY_STATE:
            raw=a.notes_queue.encoded(pending)
            bindings[path]=a.sha(raw)
            return raw
        return read(root,path,bindings)
    monkeypatch.setattr(a,'committed',pending_checkpoint)
    with pytest.raises(ValueError,match='pending/LEASED'):
        a.decode(ROOT,a.EXPORT,before[a.EXPORT])
    assert all((ROOT/p).read_bytes()==raw for p,raw in before.items())


@pytest.mark.parametrize('defect',[None,'stronger_negative','positive_key','ambiguous_key','keep','unsafe',
                                 'missing_id','credit','bool_credit','missing_blocker','blocked_scope'])
def test_c4_exposure_boundary_cannot_be_turned_into_fresh_key_credit(defect):
    report={'whole_key_credit_blocked_ids':sorted(a.WAVE10_NO_KEY_CREDIT),
            'records':[dict(question_id=qid,legal_review={'existing_answer_correct':'NOT_ASSESSED','verdict':'HOLD',
                        'whole_key_assessment_credit':0,'fresh_whole_key_credit':0,
                        'blocker':'PROCEDURAL_PRIOR_SOURCE_CONCLUSION_EXPOSURE: synthetic boundary fixture'},
                            safe_hold_recommended=True)for qid in sorted(a.WAVE10_NO_KEY_CREDIT)]}
    if defect=='positive_key':report['records'][0]['legal_review']['existing_answer_correct']='YES'
    elif defect=='stronger_negative':report['records'][0]['legal_review']['verdict']='MAJOR_REWRITE'
    elif defect=='ambiguous_key':report['records'][0]['legal_review']['existing_answer_correct']='AMBIGUOUS'
    elif defect=='keep':report['records'][0]['legal_review']['verdict']='KEEP'
    elif defect=='unsafe':report['records'][0]['safe_hold_recommended']=False
    elif defect=='missing_id':report['records'].pop()
    elif defect=='credit':report['records'][0]['legal_review']['fresh_whole_key_credit']=1
    elif defect=='bool_credit':report['records'][0]['legal_review']['whole_key_assessment_credit']=False
    elif defect=='missing_blocker':report['records'][0]['legal_review'].pop('blocker')
    elif defect=='blocked_scope':report['whole_key_credit_blocked_ids'].pop()
    if defect not in {None,'stronger_negative'}:
        with pytest.raises(ValueError,match='zero fresh whole-key credit'):
            a.validate_wave10_key_limits({'sequence':36},report)
    else:
        a.validate_wave10_key_limits({'sequence':36},report)
        # Same source-context precaution must not become a batch-wide key ban.
        a.validate_wave10_key_limits({'sequence':35},{'records':[]})


@pytest.mark.parametrize('defect',[None,'missing_hold','restored_default'])
def test_current_c4_containment_is_checked_separately_from_source_declarations(defect):
    selection=json.loads((ROOT/'practice_expansion/2026-10-28-representative/selection.json').read_bytes())
    qid=sorted(a.WAVE10_NO_KEY_CREDIT)[0]
    if defect=='missing_hold':selection['safety_holds']=[row for row in selection['safety_holds'] if row['question_id']!=qid]
    elif defect=='restored_default':selection['recommended_ids'].append(qid)
    if defect is None:a.validate_wave10_default_holds(selection)
    else:
        with pytest.raises(ValueError,match='explicit and excluded'):
            a.validate_wave10_default_holds(selection)


@pytest.fixture
def synthetic_receipt(tmp_path,state):
    """HEAD-only synthetic metadata receipt: no official-law/PASS claim."""
    root=tmp_path/'receipt';root.mkdir()
    subprocess.run(['git','init','-q',str(root)],check=True)
    for key,value in [('user.email','fixture@example.invalid'),('user.name','Synthetic fixture')]:
        subprocess.run(['git','-C',str(root),'config',key,value],check=True)
    job=copy.deepcopy(state['jobs'][35]);actor={'actor_id':job['worker'],'session_id':job['worker']}
    report=dict(stage='independent-legacy',independent_of_authors=True,auditor='GPT',
        auditor_instance='SYNTHETIC_METADATA_NOT_A_REAL_REVIEW',actor_provenance=actor,
        canonical_audit=False,canonical_release_credit=0,sources=[],
        whole_key_credit_blocked_ids=sorted(a.WAVE10_NO_KEY_CREDIT),
        records=[dict(question_id=qid,record_sha256=raw,
                      legal_review={'existing_answer_correct':'NOT_ASSESSED','verdict':'HOLD',
                                    'whole_key_assessment_credit':0,'fresh_whole_key_credit':0,
                                    'blocker':'PROCEDURAL_PRIOR_SOURCE_CONCLUSION_EXPOSURE: synthetic metadata'},
                      safe_hold_recommended=True)for qid,raw in job['question_hashes'].items()])
    raw=a.notes_queue.encoded(report);path=a.WAVE10_REPORTS[36]
    result=dict(stage='independent-legacy',independent_of_authors=True,auditor='GPT',
        auditor_instance=report['auditor_instance'],actor_provenance=actor,
        worker_commit='2'*40,question_hashes=job['question_hashes'],
        results=[dict(question_id=qid,disposition='HOLD',evidence_path=path,evidence_sha256=a.sha(raw))
                 for qid in job['question_hashes']])
    job.update(status='INTEGRATED',result=result)
    events=[dict(kind='CLAIM',job_id=job['job_id'],worker=job['worker'],attempt=job['attempt']),
            dict(kind='SUBMIT',job_id=job['job_id'],result_sha256=a.notes_queue.digest(result))]
    for path,value in [(path,raw),(a.WAVE10_RESULTS[36],a.notes_queue.encoded(result))]:
        target=root/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(value)
    subprocess.run(['git','-C',str(root),'add','.'],check=True)
    subprocess.run(['git','-C',str(root),'commit','-qm','Synthetic metadata-only contract fixture'],check=True)
    return root,job,{'events':events},report


def test_new_source_receipt_uses_only_head_bytes_and_exposes_exact_no_key_credit_ids(synthetic_receipt):
    root,job,state,_=synthetic_receipt;bindings={}
    row=a.bind_legacy_checkpoint(root,job,state,bindings)
    assert row['evidence_path']==a.WAVE10_REPORTS[36] and row['result_path']==a.WAVE10_RESULTS[36]
    assert row['source_context_exposure_no_fresh_key_credit_ids']==sorted(a.WAVE10_NO_KEY_CREDIT)
    assert row['new_question_audit_credit']==row['new_canonical_release_credit']==0
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_output(['git','-C',str(root),'cat-file','-e',job['result']['worker_commit']+'^{commit}'],stderr=subprocess.DEVNULL)


@pytest.mark.parametrize('defect',['report_raw','record_hash','stage','source_credit','instance','claim_event','submit_event','envelope'])
def test_new_source_receipt_preserves_exact_raw_rows_actor_stage_and_history(synthetic_receipt,defect):
    root,job,state,report=synthetic_receipt
    if defect=='report_raw':(root/a.WAVE10_REPORTS[36]).write_bytes(b'{}\n')
    elif defect in {'claim_event','submit_event'}:
        kind='CLAIM'if defect=='claim_event'else'SUBMIT';state['events']=[e for e in state['events']if e['kind']!=kind]
    elif defect=='envelope':(root/a.WAVE10_RESULTS[36]).write_bytes(b'{}\n')
    else:
        if defect=='record_hash':report['records'][0]['record_sha256']='0'*64
        elif defect=='stage':report['stage']='author'
        elif defect=='source_credit':report['canonical_release_credit']=True
        else:report['auditor_instance']='different-session'
        # Even a freshly committed mutation cannot be admitted by copying a
        # changed digest into an otherwise unchanged captured report receipt.
        raw=a.notes_queue.encoded(report);(root/a.WAVE10_REPORTS[36]).write_bytes(raw)
        for row in job['result']['results']:row['evidence_sha256']=a.sha(raw)
        for event in state['events']:
            if event['kind']=='SUBMIT':event['result_sha256']=a.notes_queue.digest(job['result'])
        (root/a.WAVE10_RESULTS[36]).write_bytes(a.notes_queue.encoded(job['result']))
        subprocess.run(['git','-C',str(root),'add','.'],check=True)
        subprocess.run(['git','-C',str(root),'commit','-qm','Synthetic invalid source change'],check=True)
    with pytest.raises(ValueError):a.bind_legacy_checkpoint(root,job,state,{})


def test_wave10_receipt_works_in_shallow_head_without_worker_object(synthetic_receipt,tmp_path):
    root,job,state,_=synthetic_receipt;shallow=tmp_path/'shallow'
    subprocess.run(['git','clone','-q','--depth','1',root.as_uri(),str(shallow)],check=True)
    assert (shallow/'.git/shallow').is_file()
    row=a.bind_legacy_checkpoint(shallow,job,state,{})
    assert row['new_question_audit_credit']==0


def test_old1_to33_sources_and_prior69_negative_rows_remain_the_actual_head_bytes(state):
    # This extension never authors/replaces reports. Exact receipts are still
    # checked using their original captured hashes and row/source validators.
    assert a.question_queue.digest(state['jobs'][:33])==a.PRIOR_LEGACY_RECEIPTS_SHA
    negative_ids=set()
    for job in state['jobs'][29:33]:
        bindings={};row=a.bind_legacy_checkpoint(ROOT,job,state,bindings)
        assert row['evidence_sha256']==a.sha((ROOT/row['evidence_path']).read_bytes())
        assert row['new_question_audit_credit']==0
        report=json.loads((ROOT/row['evidence_path']).read_bytes())
        negative_ids.update(r['question_id']for r in report['records']if
            r['legal_review']['verdict']!='KEEP'or r['legal_review']['existing_answer_correct']!='YES'or
            r['realism_review']['verdict']!='PASS')
    selection=json.loads((ROOT/'practice_expansion/2026-10-28-representative/selection.json').read_bytes())
    assert len(negative_ids)==69 and not negative_ids&set(selection['recommended_ids'])
    assert a.PARENT_SHA=='53537abd57b56bc8a839901a766de916c7a06b4275beba8bd2ebf435adf0353e'
    assert a.SEMANTIC=='e1519c0290ff220eb8251307e26340d76d394a7ec1f3e651194d4495a03f1824'
    assert a.CENSUS_COUNT==6989
