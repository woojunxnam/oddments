"""One actual A34 nonlegal read receipt; no legal or release credit."""
import copy
import json
from pathlib import Path
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import after190_historical_context as h
import notes_after190_annotation as a
from published15_test_view import published15_root
ROOT=published15_root(ROOT)


@pytest.fixture
def receipt():
    state=json.loads((ROOT/a.LEGACY_STATE).read_bytes())
    return h.ALLOWED[4],state['jobs'][33]


def resolve(e,job,read=a.committed,pointers=None):
    return h.resolve(ROOT,job,*e[2:6],e[6]if pointers is None else pointers,{},read)


def test_actual_a34_report_has_only_the_exact_historical_read_reference(receipt):
    e,job=receipt
    report_raw=(ROOT/e[2]).read_bytes()
    assert a.sha(report_raw)==e[3]
    references=[(path,sha,pointer)for path,sha,pointer in
                a.retained_evidence_references(json.loads(report_raw))if path==h.PROGRESS]
    assert references==[(e[4],e[5],e[6][0])]
    assert job['job_id']==e[0] and job['result']['worker_commit']==h.WAVE10_WORKER
    result=resolve(e,job)
    assert result['current_binding_override']is False
    assert result['question_audit_credit']==result['canonical_release_credit']==0


@pytest.mark.parametrize('defect',['missing','tamper','pointer','primary_pointer','extra_pointer',
                                  'report','report_sha','worker','origin','origin_sha','job','sequence'])
def test_new_receipt_fails_closed_without_enrolling_similar_references(receipt,defect):
    entry,job=receipt;e=list(entry);job=copy.deepcopy(job);read=a.committed
    if defect in {'missing','tamper'}:
        def read(root,path,bindings):
            if path==e[7]:
                if defect=='missing':raise ValueError('Missing retained snapshot')
                return b'{}\n'
            return a.committed(root,path,bindings)
    elif defect=='pointer':e[6]=('/methodology/read_docs/4/path',)
    elif defect=='primary_pointer':e[6]=('/sources/0/evidence_path',)
    elif defect=='extra_pointer':e[6]+=('/sources/0/evidence_path',)
    elif defect=='report':e[2]=a.WAVE10_REPORTS[35]
    elif defect=='report_sha':e[3]='0'*64
    elif defect=='worker':job['result']['worker_commit']='0'*40
    elif defect=='origin':e[4]='docs/RELEASE_POLICY.md'
    elif defect=='origin_sha':e[5]='0'*64
    elif defect=='job':job['job_id']='another-job'
    else:job['sequence']=35
    if defect in {'missing','tamper','pointer','primary_pointer','extra_pointer','worker'}:
        with pytest.raises(ValueError):resolve(e,job,read)
    else:assert resolve(e,job,read)is None


@pytest.mark.parametrize('registry',[h.ORIGINAL_REGISTRY,h.PREVIOUS_REGISTRY,h.REGISTRY])
def test_all_three_immutable_registry_raw_hashes_are_required(receipt,registry):
    e,job=receipt
    def read(root,path,bindings):
        raw=a.committed(root,path,bindings)
        return raw+b'\n'if path==registry else raw
    with pytest.raises(ValueError,match='registry'):resolve(e,job,read)


@pytest.mark.parametrize('defect',['old_change','old_delete','old_reclassify','private_add',
                                  'new_delete','new_extra','provenance_worker','provenance_commit',
                                  'provenance_blob','provenance_method','chain'])
def test_rehashing_v3_cannot_change_old_scope_or_new_provenance(receipt,monkeypatch,defect):
    e,job=receipt;data=json.loads((ROOT/h.REGISTRY).read_bytes())
    if defect=='old_change':data['entries'][0]['origin_raw_sha256']='0'*64
    elif defect=='old_delete':data['entries'].pop(0)
    elif defect=='old_reclassify':data['entries'][0]['reference_semantics']='PRIMARY_AUTHORITY'
    elif defect=='private_add':data['private_extracted_descriptors'].append(data['private_extracted_descriptors'][0])
    elif defect=='new_delete':data['entries'].pop()
    elif defect=='new_extra':data['entries'].append(data['entries'][-1])
    elif defect=='chain':data['previous_registry']['path']=h.ORIGINAL_REGISTRY
    else:
        field={'provenance_worker':'worker_commit','provenance_commit':'source_commit',
               'provenance_blob':'source_git_blob_sha1','provenance_method':'method'}[defect]
        data['entries'][-1]['preparation_provenance'][field]='CHANGED'
    raw=a.notes_queue.encoded(data);monkeypatch.setattr(h,'REGISTRY_SHA',a.sha(raw))
    def read(root,path,bindings):
        return raw if path==h.REGISTRY else a.committed(root,path,bindings)
    with pytest.raises(ValueError):resolve(e,job,read)


@pytest.mark.parametrize('path',['docs/RELEASE_POLICY.md','docs/AUDIT_WORKFLOW.md',
    'docs/SOURCE_USE_POLICY.md','docs/QUESTION_AUTHORING_STANDARD.md',
    'data/exam_style/mpje_style_profile.json',h.SELECTION,'data/questions/ma-q-0012.json'])
def test_new_snapshot_cannot_alias_current_governance_selector_blueprint_or_primary(receipt,path):
    entry,job=receipt;e=list(entry);e[4]=path
    assert resolve(e,job)is None


def test_current_builder_comparison_still_rejects_the_1477_snapshot(receipt,monkeypatch):
    e,_=receipt;old=(ROOT/e[7]).read_bytes();current=(ROOT/h.PROGRESS).read_bytes()
    original=a.committed
    def old_counter(root,path,bindings):
        if path==h.PROGRESS:bindings[path]=a.sha(old);return old
        return original(root,path,bindings)
    check_output=a.subprocess.check_output
    def actual_builder(command,*args,**kwargs):
        return current if command[0]==sys.executable else check_output(command,*args,**kwargs)
    monkeypatch.setattr(a,'committed',old_counter)
    monkeypatch.setattr(a.subprocess,'check_output',actual_builder)
    with pytest.raises(ValueError,match='Current progress differs'):
        a.bind_current_review_context(ROOT,{})


@pytest.mark.parametrize('path',['docs/RELEASE_POLICY.md','docs/AUDIT_WORKFLOW.md',
    'docs/SOURCE_USE_POLICY.md','docs/QUESTION_AUTHORING_STANDARD.md'])
def test_actual_a34_governance_bytes_cannot_be_replaced_by_history(receipt,monkeypatch,path):
    _,job=receipt;state=json.loads((ROOT/a.LEGACY_STATE).read_bytes());original=a.committed
    def changed(root,relative,bindings):
        raw=original(root,relative,bindings)
        return raw+b' changed'if relative==path else raw
    monkeypatch.setattr(a,'committed',changed)
    with pytest.raises(ValueError,match='retained source payload changed'):
        a.bind_legacy_checkpoint(ROOT,job,state,{})


def test_actual_selector_keeps_all_59_negatives_and_27_new_holds_contained():
    from build_full_corpus_review import validate_default_review_safety,validate_independent_archive_safety
    records=[row for path in a.WAVE10_REPORTS.values()for row in json.loads((ROOT/path).read_bytes())['records']]
    negative={r['question_id']for r in records if r['legal_review']['verdict']!='KEEP'or
              r['legal_review']['existing_answer_correct']!='YES'or r['realism_review']['verdict']!='PASS'}
    selection=json.loads((ROOT/h.SELECTION).read_bytes())
    assert len(negative)==59 and len(selection['recommended_ids'])==202
    assert len(negative&{row['question_id']for row in selection['safety_holds']})==27
    validate_default_review_safety(selection['recommended_ids'],{},records)
    validate_independent_archive_safety(selection,records)
    # Each existing finding must still reject a restored current default.
    for qid in negative:
        with pytest.raises(ValueError,match='Uncontained independent finding'):
            validate_default_review_safety(selection['recommended_ids']+[qid],{},records)
    for row in selection['safety_holds']:
        if row['question_id']not in negative:continue
        changed=copy.deepcopy(selection)
        changed['safety_holds']=[h for h in changed['safety_holds']if h['question_id']!=row['question_id']]
        # Remove any parallel display so a missing hold cannot hide in another notice.
        changed['archive_review_notices']=[dict(n,question_ids=[q for q in n['question_ids']if q!=row['question_id']])
                                           for n in changed['archive_review_notices']]
        with pytest.raises(ValueError,match='Unsurfaced independent archive finding'):
            validate_independent_archive_safety(changed,records)
