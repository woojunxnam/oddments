"""Synthetic lifecycle tests; no fixture is actual law or a future activation."""
import copy
import ast
import inspect
import json
import subprocess
from pathlib import Path

import pytest

from test_notes_body_reassessment import correction,put,final_review,RECORD
from test_note_review_queue import repo,worker_result,integrate_files,NOW,LATER
from test_notes_census_reassessment import commit,persist,authority
import note_review_queue as q
import notes_body_reassessment as body
import notes_census_reassessment as census
import notes_inactive_census_successor as successor
from notes_independent_metadata import load_metadata

PREFIX='reports/full-corpus-review/body-corrections/fixture/inactive-successor/'


def test_actual_source_preview_has_no_registration_activation_or_current_credit():
    root=Path(__file__).resolve().parents[1]
    before={p:q.raw_sha((root/p).read_bytes())for p in [q.STATE,q.LEDGER,'site/notes/complete-notes.md',
        'revisions/notes/protected-migration-after190.json','revisions/notes/protected-migration-independent-notes-wave3.json']}
    from notes_revision import load_notes
    actual=q.inventory(root,load_notes(root))['units']['w3-a-3']['body_sha256']
    if actual==successor.SCOPE['body_sha256']:
        with pytest.raises(ValueError,match='real M'):successor.preview(root)
        assert all(q.raw_sha((root/p).read_bytes())==v for p,v in before.items())
        return
    value=successor.preview(root)
    assert not value['registration_record_created']and not value['current_review_valid']
    assert value['old_claim_count']==24 and value['new_claim_count']==25 and value['original_sources_preserved']==42
    assert value['parent_completeness']=='OMISSIONS_FOUND'and value['parent_legal_status']=='LEGAL_HOLD'
    assert value['current_completeness_credit']==value['current_author_credit']==value['current_legal_credit']==0
    assert len(value['source_packet_bindings'])==15 and value['publication_blocker']==body.BLOCKER
    assert all(q.raw_sha((root/p).read_bytes())==v for p,v in before.items())


def test_ordinary_census_only_body_registration_and_reader_rules_are_unchanged():
    # Prepared from c0cf's actual definitions. No old Git object is read in CI.
    expected={'validate_record':'ac8f4eb7a5ab760c75d07775c1903dad435b881e751cb9ac5f47e53d9600b279',
        'validate_registered':'1844237db260811fec222dc1501de8ae9e7204ea0d8efe28d89079c61567a0fc',
        'registered_specs':'9df7cb528d3c64699c8eb6b98eb906b3ae501d79025e630575974efff33fd2ff',
        'register':'f9c6ffc2ebef78d3b8c9b0036e79b29ba70f62d4af8966ed90c78b7b9424d9a9'}
    for name,digest in expected.items():
        node=ast.parse(inspect.getsource(getattr(census,name))).body[0]
        assert q.raw_sha(ast.dump(node,include_attributes=False).encode())==digest


@pytest.fixture
def successor_fixture(correction,monkeypatch):
    root,notes,inv,state,old,br=correction;uid=br['unit_id']
    # Add an actual unenumerated sentence to the synthetic inactive body before
    # its first whole-body review. It does not alter the original active body.
    revision=json.loads((root/br['replacement']['revision']['path']).read_bytes())
    candidate=revision['units'][0];classification='Container change alone does not determine every legal classification.'
    candidate['body']+=' '+classification;candidate['body_sha256']=q.raw_sha(candidate['body'].encode())
    original=json.loads((root/br['replacement']['census_path']).read_bytes())
    for c in original['claims']:c['unit_content_sha256']=candidate['body_sha256']
    original['units'][0]['unit_content_sha256']=candidate['body_sha256']
    br['replacement']['revision']=put(root,br['replacement']['revision']['path'],revision)
    cb=put(root,br['replacement']['census_path'],original);br['replacement']['census_sha256']=cb['raw_sha256']
    br['edit_spans'][0].update(new_text=candidate['body'],new_text_sha256=candidate['body_sha256'])
    put(root,RECORD,br);commit(root,'synthetic inactive body with classification census omission')
    jid=body.register(state,inv,root,RECORD,notes,NOW);persist(root,state)
    parent=q.claim(state,inv,'parent-reviewer','parent-session','Synthetic non-author parent review',at=NOW)
    def parent_review(report):
        final_review(parent,root,resolve=True)(report)
        row=report['records'][0];row.update(completeness='OMISSIONS_FOUND',omissions=['Classification sentence omitted from synthetic census'],legal_status='LEGAL_HOLD')
        row['claims'][1].update(legal_status='LEGAL_HOLD',finding='Unchanged legal blocker retained',blocker='Synthetic unresolved authority')
    result,_=worker_result((root,notes,inv),state,parent,parent_review)
    q.submit(state,jid,parent['lease_token'],q.encoded(result),root,inv,NOW);persist(root,state)
    integrate_files(root,result);q.integrate(state,jid,root,inv,NOW);persist(root,state)
    br=json.loads((root/RECORD).read_bytes());old_census=json.loads((root/br['replacement']['census_path']).read_bytes())
    new=copy.deepcopy(old_census);new.update(author_provenance={'actor_id':'census-author-e','session_id':'census-author-e-session'},
        author_instance='census-author-e-instance',canonical_audit=False,independent_of_authors=False,
        canonical_release_credit=0,question_audit_credit=0,current_coverage_credit=0)
    add=copy.deepcopy(new['claims'][0]);add.update(claim_id='fixture-classification-add',statement_ko=classification)
    new['claims'].append(add);new['units'][0]['claim_count']=3
    replacement=put(root,PREFIX+'census25.json',new)
    ledger=root/(PREFIX+'active-ledger.jsonl');ledger.parent.mkdir(parents=True,exist_ok=True);ledger.write_bytes((root/q.LEDGER).read_bytes())
    commit(root,'synthetic census-only addition with immutable actual active-ledger snapshot')
    scope=dict(unit_id=uid,parent_job_id=jid,parent_job_sha256=q.digest(parent),
        parent_report_sha256=parent['result']['evidence']['raw_sha256'],body_record_path=RECORD,
        body_record_sha256=q.raw_sha((root/RECORD).read_bytes()),old_census_sha256=br['replacement']['census_sha256'],
        new_census_path=replacement['path'],new_census_sha256=replacement['raw_sha256'],body_sha256=candidate['body_sha256'],
        active_semantic_sha256=successor.semantic_sha(notes),old_claim_count=2,old_source_count=1,
        total_units=6,enumerated_units=5,added_source_ids=[],
        parent_claim_counts={'KEEP':1,'LEGAL_HOLD':1},added_claim_id=add['claim_id'],
        packet_bindings={replacement['path']:replacement['raw_sha256']},
        omission_sha256=q.raw_sha(b'Classification sentence omitted from synthetic census'))
    monkeypatch.setattr(successor,'SCOPE',scope);monkeypatch.setattr(successor,'PREFIX',PREFIX)
    record=successor.propose(root,'synthetic-inactive-census25',PREFIX+'active-ledger.jsonl',notes)
    path=PREFIX+'record.json';put(root,path,record);commit(root,'synthetic inactive successor proposal, not active N1')
    return root,notes,inv,state,parent,record,path


def register(fixture):
    root,notes,inv,state,_,_,path=fixture
    jid=successor.register(state,inv,root,path,notes,NOW);persist(root,state)
    return next(j for j in state['jobs']if j['job_id']==jid)


def review(job,unresolved=False):
    def edit(report):
        row=report['records'][0];uid=row['unit_id'];contract=job['inactive_census_successor_review']
        row.update(actual_body_sha256=contract['candidate_body_sha256'],reviewed_at=NOW,
            inactive_census_successor_review={**contract,'final_candidate_body_read_completely':True,
                'final_census_read_completely':True,'all_original_omissions_reassessed':True,
                'all_original_propositions_preserved':True,'all_derived_inputs_read_completely':True,
                'no_current_credit_before_matching_active_binding':True},
            original_omission_reassessments=[{'omission_sha256':o['raw_sha256'],
                'decision':'UNRESOLVED_REMAINS_OMISSION'if unresolved else'RESOLVED_BY_FRESH_COMPLETE_BODY_CENSUS_REVIEW',
                'finding':'Synthetic fresh comparison of entire candidate and final inventory'}for o in contract['parent_omissions']])
        row['legal_status']='LEGAL_HOLD'
        if unresolved:row.update(completeness='OMISSIONS_FOUND',omissions=[o['omission']for o in contract['parent_omissions']])
        for c in row['claims']:
            inherited=job['carried_legal_blockers'][uid].get(c['claim_id'])
            if inherited:
                c.update(legal_status='LEGAL_HOLD',inherited_legal_blockers=inherited)
            else:
                a=authority(q.OUTPUT+'fixture-official.txt')
                a['source_retrieval']={'mode':'SAME_DAY_RETAINED_CACHE','http_status':200,'transport':'SYNTHETIC_TEST_ONLY',
                    'document_identity_status':'OFFICIAL_DOCUMENT_TARGET_PROVISIONS_DIRECTLY_READ',
                    'raw_sha256':a['evidence_sha256'],'retrieved_at_utc':NOW,'read_at_utc':NOW}
                c.update(legal_status='KEEP',authorities=[a]);c.pop('blocker',None)
    return edit


def integrate(fixture,job,edit=None):
    root,notes,inv,state,*_=fixture
    q.claim(state,inv,'successor-reviewer','successor-session','Actual new non-author/non-parent fixture reviewer',at=NOW)
    result,_=worker_result((root,notes,inv),state,job,edit or review(job))
    q.submit(state,job['job_id'],job['lease_token'],q.encoded(result),root,inv,NOW);persist(root,state)
    integrate_files(root,result);q.integrate(state,job['job_id'],root,inv,NOW);persist(root,state)
    return result


def test_registration_keeps_real_m_and_all_current_credit_zero_and_is_idempotent(successor_fixture):
    root,notes,inv,state,parent,r,path=successor_fixture;before=q.encoded(parent);ledger=(root/q.LEDGER).read_bytes()
    job=register(successor_fixture);meta=load_metadata(root,notes);uid=r['unit_id']
    assert meta['units'][uid]['completeness']=='PENDING_INACTIVE_BODY_CENSUS_SUCCESSOR'
    assert meta['units'][uid]['legal_status']=='LEGAL_HOLD'and meta['units'][uid]['requires_review']
    assert not meta['units'][uid]['current_review_valid'] and not meta['units'][uid]['candidate_review_valid']
    assert meta['progress']['processed_units']==4 and meta['progress']['pending_inactive_census_successor_units']==1
    assert q.encoded(parent)==before and (root/q.LEDGER).read_bytes()==ledger
    assert successor.register(state,inv,root,path,notes,NOW)==job['job_id']
    assert len(state['jobs'])==3 and successor.registered_specs(root,notes)==[]
    assert len(meta['units'][uid]['review_history'])==2


@pytest.mark.parametrize('who',['body-author','census-author-e','census-author-e-instance','parent-reviewer','parent-session'])
def test_authors_and_parent_actual_session_cannot_self_certify_successor(successor_fixture,who):
    root,notes,inv,state,*_=successor_fixture;register(successor_fixture)
    with pytest.raises(ValueError,match='self-audit|fresh non-parent'):
        q.claim(state,inv,who,who,'Synthetic attempt',auditor_instance=who,at=NOW)


def test_result_integrates_with_holds_and_history_but_remains_inactive_zero_credit(successor_fixture):
    root,notes,inv,state,parent,r,_=successor_fixture;job=register(successor_fixture);integrate(successor_fixture,job)
    m=load_metadata(root,notes);row=m['units'][r['unit_id']]
    assert row['candidate_review_valid']and not row['current_review_valid']and row['requires_review']
    assert row['completeness']=='COMPLETE'and row['legal_status']=='LEGAL_HOLD'
    assert any(h['completeness']=='OMISSIONS_FOUND'for h in row['review_history'])
    assert m['progress']['processed_units']==4 and m['progress']['reviewed_body_candidates_not_current_credit']==1
    assert q.progress(state,inv,root)['independent_completeness_legal_processed_units']==4
    assert successor.registered_specs(root,notes)==[]
    # Explicit synthetic future16 activation; production implementation has none.
    active=copy.deepcopy(notes);candidate=json.loads((root/r['body_parent_record']['path']).read_bytes())['replacement']['revision']
    unit=json.loads((root/candidate['path']).read_bytes())['units'][0]
    for c in active['chapters']:c['units']=[unit if u['id']==r['unit_id']else u for u in c['units']]
    new=json.loads((root/r['replacement']['census_path']).read_bytes());rows=[json.loads(x)for x in(root/q.LEDGER).read_text().splitlines()]
    rows=[census.replacement_row(r,new)if x['unit_id']==r['unit_id']else x for x in rows]
    (root/q.LEDGER).write_text(''.join(json.dumps(x)+'\n'for x in rows));put(root,'notes-fixture.json',active);commit(root,'synthetic future16 exact body+census selection')
    meta=load_metadata(root,active);assert meta['units'][r['unit_id']]['current_review_valid']
    assert meta['units'][r['unit_id']]['legal_status']=='LEGAL_HOLD' and meta['progress']['processed_units']==5
    specs=body.ordered_specs(root,body.registered_specs(root,active)+successor.registered_specs(root,active))
    assert specs[-1]['path']==r['replacement']['census_path']and body.census_snapshot(root,specs[-1],active)[r['unit_id']]==unit


@pytest.mark.parametrize('defect',['purpose','body','parent','old_binding','old_report','new_census','mapping','extra_atom',
    'missing_negative','snapshot','other305','extra_field','credit','active_unit','new_revision'])
def test_exact_record_and_all_preservation_boundaries_reject_tamper(successor_fixture,defect):
    root,notes,inv,state,parent,r,path=successor_fixture;r=copy.deepcopy(r)
    if defect=='purpose':r['purpose']=census.PURPOSE
    elif defect=='body':r['body_sha256']='0'*64
    elif defect=='parent':r['previous_job_id']='missing-parent'
    elif defect=='old_binding':r['previous_binding']['census_sha256']='0'*64
    elif defect=='old_report':r['previous_report']['raw_sha256']='0'*64
    elif defect=='new_census':r['replacement']['census_sha256']='0'*64
    elif defect=='mapping':r['claim_mapping'].pop(next(iter(r['claim_mapping'])))
    elif defect=='extra_atom':r['added_claim_ids'].append('invented-addition')
    elif defect=='missing_negative':r['previous_job_sha256']='0'*64
    elif defect=='snapshot':r['active_ledger_snapshot']['raw_sha256']='0'*64
    elif defect=='other305':r['other_current_bindings_sha256']='0'*64
    elif defect=='extra_field':r['skip_body_guard']=True
    elif defect=='credit':r['current_coverage_credit']=True
    elif defect=='active_unit':r['active_unit_record_sha256']='0'*64
    else:r['replacement']['notes_revision']='FAKE_ACTIVE_N1'
    with pytest.raises(ValueError):successor.validate_record(state,r,root,notes,inv=inv)


@pytest.mark.parametrize('defect',['resolve_hold','missing_read','wrong_body','missing_omission','bad_retrieval'])
def test_fresh_report_cannot_close_unchanged_hold_or_skip_full_review(successor_fixture,defect):
    root,notes,inv,state,*_=successor_fixture;job=register(successor_fixture)
    q.claim(state,inv,'successor-reviewer','successor-session','Actual new fixture reviewer',at=NOW)
    def edit(report):
        review(job)(report);row=report['records'][0]
        if defect=='resolve_hold':
            c=next(c for c in row['claims']if c['claim_id']in job['carried_legal_blockers'][row['unit_id']]);c['legal_status']='KEEP'
        elif defect=='missing_read':row['inactive_census_successor_review']['final_census_read_completely']=False
        elif defect=='wrong_body':row['actual_body_sha256']='0'*64
        elif defect=='missing_omission':row['original_omission_reassessments']=[]
        else:row['claims'][0]['authorities'][0]['source_retrieval']['http_status']=403
    result,_=worker_result((root,notes,inv),state,job,edit)
    with pytest.raises(ValueError):q.submit(state,job['job_id'],job['lease_token'],q.encoded(result),root,inv,NOW)


def test_current_wave_and_ordinary_census_body_rule_cannot_be_bypassed(successor_fixture):
    root,notes,inv,state,parent,r,path=successor_fixture
    projected={**r,'purpose':census.PURPOSE,'reassessment_id':'not-an-exception'}
    with pytest.raises(ValueError,match='Body changes are outside census-only'):
        census.validate_record(state,projected,root,notes,census.disk_reader(root))
    # An actually pending unrelated wave blocks registration without mutation.
    q.plan(state,inv,root,batches=1,size=1,at=NOW);before=q.encoded(state)
    # The fixture has one unenumerated remaining unit; install a queued shape to
    # exercise only registration ordering, never a legal source/census binding.
    state['jobs'].append(dict(job_id='synthetic-pending-unrelated',sequence=len(state['jobs'])+1,
        stage=q.STAGE,status='QUEUED',attempt=0,unit_ids=['not-enumerated'],
        unit_bindings={'not-enumerated':{'claim_record_sha256s':{}}}))
    pending=q.encoded(state)
    with pytest.raises(ValueError,match='Finish current native wave'):
        successor.register(state,inv,root,path,notes,NOW)
    assert q.encoded(state)==pending


@pytest.mark.parametrize('defect',['old_claim','old_source','extra_new_claim'])
def test_even_a_rehashed_new_source_cannot_rewrite_old_claims_or_sources(successor_fixture,monkeypatch,defect):
    root,notes,inv,state,parent,r,_=successor_fixture;r=copy.deepcopy(r)
    path=r['replacement']['census_path'];new=json.loads((root/path).read_bytes())
    if defect=='old_claim':new['claims'][0]['statement_ko']+=' Different legal scope.'
    elif defect=='old_source':new['sources'][next(iter(new['sources']))]['official_url']='https://example.gov/different-scope'
    else:
        new['claims'].append(dict(new['claims'][-1],claim_id='extra-unbound-proposition'))
    raw=q.encoded(new);(root/path).write_bytes(raw);commit(root,'synthetic otherwise-committed source tamper')
    scope=copy.deepcopy(successor.SCOPE);scope['new_census_sha256']=q.raw_sha(raw);scope['packet_bindings'][path]=q.raw_sha(raw)
    monkeypatch.setattr(successor,'SCOPE',scope);r['replacement']['census_sha256']=q.raw_sha(raw)
    with pytest.raises(ValueError,match='old24 claim JSON/42 sources'):
        successor.validate_record(state,r,root,notes,inv=inv)


def test_shallow_reader_needs_head_snapshots_only_and_retains_inactive_hold(successor_fixture,tmp_path):
    root,notes,inv,state,*_=successor_fixture;job=register(successor_fixture);result=integrate(successor_fixture,job)
    shallow=tmp_path/'shallow';subprocess.run(['git','clone','-q','--depth','1',root.as_uri(),str(shallow)],check=True)
    assert (shallow/'.git/shallow').is_file()
    for captured in state['jobs']:
        with pytest.raises(subprocess.CalledProcessError):
            q.git(shallow,'cat-file','-e',captured['result']['worker_commit']+'^{commit}')
    meta=load_metadata(shallow,notes);uid=successor.SCOPE['unit_id']
    assert meta['units'][uid]['candidate_review_valid']and not meta['units'][uid]['current_review_valid']
    assert meta['units'][uid]['legal_status']=='LEGAL_HOLD'and meta['progress']['processed_units']==4


def test_recover_uses_new_token_without_losing_inactive_binding_or_negative(successor_fixture):
    root,notes,inv,state,*_=successor_fixture;job=register(successor_fixture)
    q.claim(state,inv,'first-successor','first-successor-session','Actual fresh fixture session',at=NOW)
    token=job['lease_token'];binding=copy.deepcopy(job['unit_bindings']);negative=copy.deepcopy(job['carried_legal_blockers'])
    assert q.recover(state,LATER)==[job['job_id']]
    q.claim(state,inv,'replacement-successor','replacement-session','Actual recovery fixture session',at=LATER)
    assert job['attempt']==2 and job['lease_token']!=token
    assert job['unit_bindings']==binding and job['carried_legal_blockers']==negative
    with pytest.raises(ValueError,match='Stale or absent'):
        q.heartbeat(state,job['job_id'],token,inv,at=LATER)


@pytest.mark.parametrize('defect',['active_body','other_binding','duplicate','mixed','negative','nonroot'])
def test_live_scope_duplicate_negative_and_root_only_boundaries(successor_fixture,defect):
    root,notes,inv,state,parent,r,path=successor_fixture;job=register(successor_fixture)
    if defect in {'active_body','other_binding'}:
        changed=copy.deepcopy(inv)
        if defect=='active_body':changed['notes']['chapters'][0]['units'][0]['body']+=' Unbounded change.'
        else:changed['units']['a-second']['ledger_binding_sha256']='0'*64
        with pytest.raises(ValueError):q.current(job,changed,state)
    elif defect=='duplicate':
        changed=copy.deepcopy(state);changed['inactive_census_successors']*=2
        with pytest.raises(ValueError):q.validate_state(changed)
    elif defect=='mixed':
        job['reassessment_id']='fake-ordinary-path'
        with pytest.raises(ValueError):q.validate_state(state)
    elif defect=='negative':
        job['carried_legal_blockers'][r['unit_id']]={}
        with pytest.raises(ValueError,match='negative/contract'):
            successor.validate_registered(state,root,notes)
    else:
        before=(root/q.STATE).read_bytes()
        with pytest.raises(ValueError,match='Only root'):
            with q.checkpoint(root,'census-author-e'):pytest.fail('non-root wrote successor checkpoint')
        assert (root/q.STATE).read_bytes()==before
