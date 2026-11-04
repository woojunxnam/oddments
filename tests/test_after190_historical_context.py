"""Actual retained receipts and synthetic negative cases; no new legal audit."""
import copy
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import notes_after190_annotation as a
import after190_historical_context as h


@pytest.fixture(scope='module')
def state():return json.loads((ROOT/a.LEGACY_STATE).read_bytes())


def job_for(state,sequence):return state['jobs'][sequence-1]


@pytest.mark.parametrize('index',range(4))
def test_exact_historical_receipt_uses_retained_head_bytes_without_replacing_current_binding(state,index):
    e=h.ALLOWED[index];job=job_for(state,e[1]);bindings={}
    current=a.committed(ROOT,e[4],bindings);current_sha=a.sha(current)
    assert current_sha!=e[5]
    result=h.resolve(ROOT,job,e[2],e[3],e[4],e[5],e[6],bindings,a.committed)
    assert result['current_binding_override']is False and result['retained_raw_sha256']==e[5]
    assert bindings[e[4]]==current_sha and bindings[e[7]]==e[5]
    assert result['question_audit_credit']==result['canonical_release_credit']==0


@pytest.mark.parametrize('defect',['job','report','report_sha','origin','old_sha','primary_pointer'])
def test_receipt_cannot_be_used_by_another_report_job_origin_or_authority(state,defect):
    e=h.ALLOWED[0];job=copy.deepcopy(job_for(state,30));path,sha,origin,old,pointers=e[2],e[3],e[4],e[5],e[6]
    if defect=='job':job['job_id']='different-job'
    elif defect=='report':path=h.ALLOWED[2][2]
    elif defect=='report_sha':sha='0'*64
    elif defect=='origin':origin='docs/RELEASE_POLICY.md'
    elif defect=='old_sha':old='0'*64
    else:pointers=('/sources/0/evidence_path',)
    if defect=='primary_pointer':
        with pytest.raises(ValueError,match='reference location'):h.resolve(ROOT,job,path,sha,origin,old,pointers,{},a.committed)
    else:assert h.resolve(ROOT,job,path,sha,origin,old,pointers,{},a.committed)is None


@pytest.mark.parametrize('path',['docs/RELEASE_POLICY.md','docs/AUDIT_WORKFLOW.md','docs/SOURCE_USE_POLICY.md',
    'docs/QUESTION_AUTHORING_STANDARD.md','data/exam_style/mpje_style_profile.json','data/questions/ma-q-0012.json'])
def test_governance_primary_and_question_paths_are_not_historical_aliases(state,path):
    e=h.ALLOWED[0]
    assert h.resolve(ROOT,job_for(state,30),e[2],e[3],path,e[5],e[6],{},a.committed)is None


@pytest.mark.parametrize('defect',['extra_governance','new_origin','wide_pointer','override','credit','private_index','private_memo','private_hash','private_verified'])
def test_even_rehashed_registry_cannot_expand_the_bounded_receipts_or_private_scope(state,monkeypatch,defect):
    data=json.loads((ROOT/h.REGISTRY).read_bytes());e=data['entries'][0]
    if defect=='extra_governance':data['entries'].append(dict(e,origin_path='docs/RELEASE_POLICY.md'))
    elif defect=='new_origin':e['origin_path']='reports/full-corpus-review/notes-unit-ledger.jsonl'
    elif defect=='wide_pointer':e['reference_pointers'].append('/sources/0/evidence_path')
    elif defect=='override':e['current_binding_override']=True
    elif defect=='credit':data['question_audit_credit']=False
    elif defect=='private_index':data['private_extracted_descriptors'][0]['source_index']=9
    elif defect=='private_memo':data['private_extracted_descriptors'][0]['retained_memo_path']='docs/RELEASE_POLICY.md'
    elif defect=='private_hash':data['private_extracted_descriptors'][0]['extracted_sha256']='0'*64
    else:data['private_extracted_descriptors'][0]['runtime_text_bytes_verified']=True
    raw=a.notes_queue.encoded(data);monkeypatch.setattr(h,'REGISTRY_SHA',a.sha(raw));original=a.committed
    def read(root,path,bindings):
        if path==h.REGISTRY:bindings[path]=a.sha(raw);return raw
        return original(root,path,bindings)
    e=h.ALLOWED[0]
    with pytest.raises(ValueError):h.resolve(ROOT,job_for(state,30),e[2],e[3],e[4],e[5],e[6],{},read)


def test_missing_or_changed_retained_bytes_cannot_fall_back_to_current_progress(state):
    e=h.ALLOWED[0];original=a.committed
    def changed(root,path,bindings):
        if path==e[7]:return b'{}\n'
        return original(root,path,bindings)
    with pytest.raises(ValueError,match='SOURCE_BLOCKED'):h.resolve(ROOT,job_for(state,30),e[2],e[3],e[4],e[5],e[6],{},changed)


@pytest.mark.parametrize('index',range(4))
def test_private_extracted_descriptor_verifies_only_retained_memo_and_never_opens_private_text(state,index):
    values=h.PRIVATE_ALLOWED[index];job=job_for(state,31);report=json.loads((ROOT/h.ALLOWED[2][2]).read_bytes());seen=[]
    def read(root,path,bindings):
        assert not Path(path).is_absolute();seen.append(path);return a.committed(root,path,bindings)
    result=h.resolve_private(ROOT,job,h.ALLOWED[2][2],h.ALLOWED[2][3],report,values[4],values[5],
        {f'/sources/{values[0]}/extracted_path'}, {},read)
    assert result['runtime_text_bytes_verified']is False and result['public_raw_redistribution']is False
    assert values[7]in seen and values[4]not in seen


@pytest.mark.parametrize('defect',['report','index','source_id','copyright','memo','sha','similar_path','public_evidence'])
def test_private_descriptor_cannot_expand_to_other_absolute_or_public_evidence(state,defect):
    v=h.PRIVATE_ALLOWED[0];report=json.loads((ROOT/h.ALLOWED[2][2]).read_bytes());source=report['sources'][8]
    path,sha,pointer,report_sha=v[4],v[5],'/sources/8/extracted_path',h.ALLOWED[2][3]
    if defect=='report':report_sha='0'*64
    elif defect=='index':pointer='/sources/9/extracted_path'
    elif defect=='source_id':source['source_id']='other'
    elif defect=='copyright':source['public_raw_redistribution']=True
    elif defect=='memo':source['evidence_path']='docs/RELEASE_POLICY.md'
    elif defect=='sha':sha='0'*64
    elif defect=='similar_path':path=path+'.copy'
    else:pointer='/sources/8/evidence_path'
    args=(ROOT,job_for(state,31),h.ALLOWED[2][2],report_sha,report,path,sha,{pointer},{},a.committed)
    if defect in {'report','sha','similar_path'}:assert h.resolve_private(*args)is None
    else:
        with pytest.raises(ValueError):h.resolve_private(*args)


@pytest.mark.parametrize('attack',['current_counter','derived_counter'])
def test_current_counter_validation_rejects_old_or_forged_progress_even_with_valid_history(monkeypatch,attack):
    original=subprocess.check_output;old=(ROOT/h.ALLOWED[0][7]).read_bytes();current=(ROOT/h.PROGRESS).read_bytes()
    def derived(command,*args,**kwargs):
        if command[0]==sys.executable:return current if attack=='current_counter'else old
        return original(command,*args,**kwargs)
    if attack=='current_counter':
        head_read=a.committed
        def old_counter(root,path,bindings):
            if path==h.PROGRESS:bindings[path]=a.sha(old);return old  # model a committed stale current counter
            return head_read(root,path,bindings)
        monkeypatch.setattr(a,'committed',old_counter)
    monkeypatch.setattr(subprocess,'check_output',derived)
    with pytest.raises(ValueError,match='Current progress differs'):a.bind_current_review_context(ROOT,{})


def test_legal_primary_payloads_keep_their_current_exact_byte_check(state,monkeypatch):
    job=job_for(state,31);report=json.loads((ROOT/h.ALLOWED[2][2]).read_bytes())
    primary=report['sources'][0]['evidence_path'];original=a.committed
    def changed(root,path,bindings):
        if path==primary:return b'Changed actual primary bytes'
        return original(root,path,bindings)
    monkeypatch.setattr(a,'committed',changed)
    with pytest.raises(ValueError,match='retained source payload changed'):a.bind_legacy_checkpoint(ROOT,job,state,{})


def test_current_operational_runbook_must_still_match_head_even_when_old_receipt_is_valid(state,monkeypatch):
    e=h.ALLOWED[1];assert h.resolve(ROOT,job_for(state,30),e[2],e[3],e[4],e[5],e[6],{},a.committed)
    original=a.safe_bytes
    def changed(root,path):return original(root,path)+b' changed'if path==h.RUNBOOK else original(root,path)
    monkeypatch.setattr(a,'safe_bytes',changed)
    with pytest.raises(ValueError,match='Uncommitted'):a.bind_current_review_context(ROOT,{})


def test_history_runtime_works_in_real_shallow_checkout_without_original_worker_objects(state,tmp_path,monkeypatch):
    config=tmp_path/'empty.gitconfig';config.write_text('');monkeypatch.setenv('GIT_CONFIG_GLOBAL',str(config))
    shallow=tmp_path/'shallow'
    subprocess.run(['git','clone','-q','--depth','1','--no-checkout',ROOT.as_uri(),str(shallow)],check=True)
    paths=[h.REGISTRY,h.PREVIOUS_REGISTRY,*{e[7]for e in h.ALLOWED}]
    subprocess.run(['git','-C',str(shallow),'checkout','HEAD','--',*paths],check=True)
    for e in h.ALLOWED:
        job=job_for(state,e[1]);worker=job['result']['worker_commit']
        with pytest.raises(subprocess.CalledProcessError):subprocess.check_output(['git','-C',str(shallow),'cat-file','-e',worker+'^{commit}'],stderr=subprocess.DEVNULL)
        assert h.resolve(shallow,job,e[2],e[3],e[4],e[5],e[6],{},a.committed)['retained_raw_sha256']==e[5]
