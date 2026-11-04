"""Source gating/routing tests. Positive model fixtures are never publication proof."""
import copy
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import notes_held_sixteenth as held
import notes_published15_closure as old
import notes_inactive_census_successor as inactive
import verify_representative_protected as protected
from notes_independent_metadata import load_metadata
from test_notes_published15_closure import published,put,commit
from test_note_review_queue import repo
from test_notes_census_reassessment import remediation


def test_actual_guard_readiness_never_fabricates_a_publication_or_activation():
    before={p:old.sha((ROOT/p).read_bytes())for p in [inactive.q.STATE,inactive.q.LEDGER,old.FIFTEENTH,old.FOURTEENTH,old.EXPORT]}
    state=held.readiness(ROOT)
    assert state['status'] in {'BLOCKED','EXPLICIT_CHECK_REQUIRED'}
    assert not state['active_body_written']and not state['registration_performed']
    result=subprocess.run([sys.executable,str(ROOT/'scripts/notes_held_sixteenth.py'),'--check'],capture_output=True,text=True)
    if state['blockers']:assert result.returncode==1 and 'BLOCKED'in result.stdout
    else:assert result.returncode==0  # Future actual binding must pass the full real gate.
    assert all(old.sha((ROOT/p).read_bytes())==value for p,value in before.items())


def test_absent_activation_source_is_exact_noop_and_unapproved_source_fails(tmp_path):
    root=tmp_path/'repo';root.mkdir();subprocess.run(['git','init','-q',str(root)],check=True)
    subprocess.run(['git','-C',str(root),'config','user.name','Fixture'],check=True)
    subprocess.run(['git','-C',str(root),'config','user.email','fixture@example.invalid'],check=True)
    data={'edition':'M','chapters':[]}
    assert held.apply_if_bound(root,data)is data
    put(root,held.SOURCE,{'self_declared':'approved'});commit(root,'synthetic unapproved source')
    with pytest.raises(ValueError,match='no actual published15'):
        held.apply_if_bound(root,data)


def test_actual_metadata_binding_export_preserves_current_counters_and_inactive_status():
    before=load_metadata(ROOT);bindings={};after=load_metadata(ROOT,source_bindings=bindings)
    assert before==after and len(bindings)>100
    inv=inactive.q.inventory(ROOT)
    assert after['units']['w3-a-3']['current_review_valid']==(inv['units']['w3-a-3']['body_sha256']==inactive.SCOPE['body_sha256'])
    assert after['units']['w3-a-3']['legal_status']=='LEGAL_HOLD'
    assert after['progress']['complete_units']+after['progress']['omissions_found_units']==after['progress']['processed_units']
    for p,sha in bindings.items():assert old.sha(old.committed(ROOT,p))==sha


@pytest.mark.parametrize('defect',[None,'not_ig','author','claim','integration','submission','report_bytes'])
def test_native_job_gate_preserves_actual_head_provenance_and_source_bytes(remediation,defect):
    root,notes,inv,state,job,spec=remediation
    if defect=='not_ig':job['status']='SUBMITTED'
    elif defect=='author':job['known_author_ids'].append(job['actor_provenance']['actor_id'])
    elif defect in {'claim','integration','submission'}:
        kind={'claim':'CLAIM','integration':'INTEGRATE','submission':'SUBMIT'}[defect]
        state['events']=[e for e in state['events']if not(e.get('kind')==kind and e.get('job_id')==job['job_id'])]
    elif defect=='report_bytes':(root/job['result']['evidence']['path']).write_bytes(b'{}\n')
    if defect:
        with pytest.raises(ValueError):held.validate_job(root,state,job)
    else:assert len(held.validate_job(root,state,job)['records'])==5


def test_approved_publication_alone_cannot_invent_a_fresh25_job(tmp_path,monkeypatch):
    root=tmp_path/'repo';root.mkdir();subprocess.run(['git','init','-q',str(root)],check=True)
    subprocess.run(['git','-C',str(root),'config','user.name','Fixture'],check=True)
    subprocess.run(['git','-C',str(root),'config','user.email','fixture@example.invalid'],check=True)
    put(root,inactive.q.STATE,inactive.q.empty(root))
    config=dict(schema_version=1,purpose='N1_HELD_BUILDER_SOURCE_NOT_PUBLICATION_APPROVAL',edition=held.EDITION,
        unit_id='w3-a-3',closure={'path':'synthetic-closure','raw_sha256':'0'*64},review={'job_id':'NO_FUTURE_JOB'},
        required_sibling_jobs={uid:'NO_FUTURE_JOB'for uid in held.SIBLINGS},release_eligible=False,current_legal_pass=False,
        canonical_release_credit=0,question_audit_credit=0,new_author_review_credit=0,new_independent_legal_audit_credit=0)
    source=put(root,held.SOURCE,config);commit(root,'synthetic already-approved-publication boundary only')
    monkeypatch.setattr(held,'APPROVED_ACTIVATION_SOURCES',{(held.SOURCE,source['raw_sha256']):{'closure':config['closure'],'review':config['review']}})
    monkeypatch.setattr(old,'validate',lambda *a,**k:{'SYNTHETIC_PUBLICATION_BOUNDARY_ONLY':True})
    with pytest.raises(ValueError,match='actual latest inactive25'):
        held.source_contract(root)


def test_substitution_changes_only_one_unit_and_never_marks_it_legal_pass(tmp_path,monkeypatch):
    root=tmp_path;put(root,held.SOURCE,b'SYNTHETIC_STUBBED_VALIDATED_SOURCE')
    previous={'edition':'M','revision_provenance':{'base_guide_sha256':'a'*64},'chapters':[{'units':[
        {'id':'w3-a-3','body':'Synthetic old scope'},*({'id':'sibling-'+str(i),'body':'Unchanged synthetic body'}for i in range(305))]}]}
    candidate={'id':'w3-a-3','body':'Synthetic corrected scope','content_version':'SYNTHETIC_CANDIDATE'}
    scope=copy.deepcopy(inactive.SCOPE);scope['active_semantic_sha256']=inactive.semantic_sha(previous);monkeypatch.setattr(inactive,'SCOPE',scope)
    monkeypatch.setattr(held,'source_contract',lambda root:({}, {}, {}, {},previous,candidate,{'raw_sha256':'b'*64}))
    new=held.apply_if_bound(root,previous)
    assert new['chapters'][0]['units'][1:]==previous['chapters'][0]['units'][1:]
    assert new['chapters'][0]['units'][0]==candidate and 'independent_content_review'not in candidate
    assert new['revision_provenance']['review_status']=='HELD_COMPLETE_CENSUS_NOT_LEGAL_PASS'
    changed=copy.deepcopy(previous);changed['chapters'][0]['units'][1]['body']='Unauthorized sibling edit'
    with pytest.raises(ValueError,match='only exact M'):held.apply_if_bound(root,changed)


@pytest.mark.parametrize('field,value',[('jobs',[{'id':'rewritten'}]),('events',[{'kind':'rewritten'}])])
def test_published_checkpoint_history_is_append_only(published,field,value):
    root,_,_,_,closure=published;p='reports/full-corpus-review/fixture-state.json'
    original={'jobs':[{'id':'old'}],'events':[{'kind':'old'}]}
    # Pure prefix checker isolation: publication bytes come from this explicit
    # synthetic context, not an alias available to the real source reader.
    current=copy.deepcopy(original);current[field]=value;put(root,p,current);commit(root,'synthetic invalid checkpoint')
    from unittest.mock import patch
    with patch.object(old,'old_bytes',return_value=old.encoded(original)):
        with pytest.raises(ValueError,match='history cannot be rewritten'):held.checkpoint_prefix(root,closure,p)


@pytest.mark.parametrize('credit',[False,1])
def test_even_rehashed_migration_cannot_claim_credit(published,monkeypatch,credit):
    root,_,_,binding,_=published
    value=dict(closure=binding,canonical_audit=False,daily_eligible=False,public_unit_legal_status='LEGAL_HOLD',
        body_delta={'other305_unchanged':True},canonical_release_credit=credit)
    ref=put(root,held.MANIFEST,value);commit(root,'synthetic invalid migration')
    monkeypatch.setattr(held,'APPROVED_MIGRATIONS',{(held.MANIFEST,ref['raw_sha256']):{'closure':binding}})
    with pytest.raises(ValueError,match='cannot claim legal/release credit'):held.decode(root,old.EXPORT,b'CURRENT')


def test_sixteenth_routes_old_checks_to_fixed_view_and_skips_live_old15(published,monkeypatch):
    root,_,_,binding,_=published;raw=(root/old.EXPORT).read_bytes()
    value=dict(closure=binding,canonical_audit=False,daily_eligible=False,public_unit_legal_status='LEGAL_HOLD',
        body_delta={'other305_unchanged':True},canonical_release_credit=0,question_audit_credit=0,
        new_markdown_sha256=old.sha(raw))
    ref=put(root,held.MANIFEST,value);commit(root,'synthetic already-validated current-contract routing fixture')
    monkeypatch.setattr(held,'APPROVED_MIGRATIONS',{(held.MANIFEST,ref['raw_sha256']):{'closure':binding}})
    monkeypatch.setattr(held,'expected_migration',lambda *a:value)
    import notes_after190_annotation
    monkeypatch.setattr(notes_after190_annotation,'decode',lambda *a:pytest.fail('old15 read live N1'))
    assert protected.migrated_baseline_bytes(root,old.EXPORT,raw)==b'SYNTHETIC ORIGINAL BASELINE\n'


def test_current_counter_rejection_cannot_be_skipped_after_a_valid_old_view(published,monkeypatch):
    # Boundary isolation only. Actual fresh25/current N1 are unavailable; the
    # real counter validator's source/derived tamper tests run separately.
    root,_,_,binding,closure=published;unit={'id':'w3-a-3','body':'SYNTHETIC VALIDATED CURRENT CONTRACT'}
    notes={'chapters':[{'units':[unit]}]};job={'unit_bindings':{'w3-a-3':{'binding':'SYNTHETIC'}}}
    monkeypatch.setattr(held,'source_contract',lambda r:({},closure,{},job,notes,unit,{'path':'source','raw_sha256':'0'*64}))
    monkeypatch.setattr(old,'validate',lambda *a,**k:closure)
    monkeypatch.setattr(held,'checkpoint_prefix',lambda *a:None)
    monkeypatch.setattr(held,'apply_if_bound',lambda *a:notes)
    import notes_revision,notes_independent_metadata,notes_after190_annotation
    monkeypatch.setattr(notes_revision,'load_notes',lambda *a:notes)
    monkeypatch.setattr(inactive.q,'inventory',lambda *a,**k:{'units':job['unit_bindings']})
    monkeypatch.setattr(inactive,'sibling_evolution',lambda *a:[])
    monkeypatch.setattr(notes_independent_metadata,'load_metadata',lambda *a,**k:{'units':{'w3-a-3':{
        'current_review_valid':True,'completeness':'COMPLETE','legal_status':'LEGAL_HOLD','requires_review':True,'notice':'HOLD'}}})
    monkeypatch.setattr(notes_after190_annotation,'bind_native_author',lambda *a:{})
    def reject(*args):raise ValueError('CURRENT_SOURCE_COUNTER_REJECTED')
    monkeypatch.setattr(notes_after190_annotation,'bind_current_review_context',reject)
    put(root,inactive.q.LEDGER,b'SYNTHETIC ALREADY VALIDATED LEDGER\n');commit(root,'synthetic counter boundary')
    with pytest.raises(ValueError,match='CURRENT_SOURCE_COUNTER_REJECTED'):
        held.expected_migration(root,binding)


def test_historical_test_adapter_never_uses_current_n1_inputs(published,monkeypatch):
    root,_,_,binding,_=published;metadata={'closure':binding}
    ref=put(root,held.MANIFEST,metadata);commit(root,'synthetic historical test view adapter')
    monkeypatch.setattr(held,'APPROVED_MIGRATIONS',{(held.MANIFEST,ref['raw_sha256']):{'closure':binding}})
    from published15_test_view import published15_root,release
    try:
        view=published15_root(root)
        assert (view/'scripts/notes_revision.py').read_bytes()==b'M\n'
        assert (root/'scripts/notes_revision.py').read_bytes().startswith(b'N1 LIVE')
        assert published15_root(root)==view
    finally:release(root)
