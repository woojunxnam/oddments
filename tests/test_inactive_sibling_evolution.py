"""Actual controller functions, synthetic legal content; no real registration."""
import copy
import json

import pytest

from test_note_review_queue import repo,worker_result,integrate_files,NOW
from test_notes_body_reassessment import correction,put
from test_notes_census_reassessment import commit,persist,final_review
from test_notes_inactive_census_successor import successor_fixture,register,integrate
import note_review_queue as q
import notes_body_reassessment as body
import notes_census_reassessment as census
import notes_inactive_census_successor as inactive
from notes_independent_metadata import load_metadata


def sibling_record(fixture,uid):
    root,notes,inv,state,_,_,_=fixture
    parent=census.latest_jobs(state)[uid];binding=parent['unit_bindings'][uid]
    original=json.loads((root/binding['census_path']).read_bytes());path='reports/full-corpus-review/sibling-'+uid
    new=copy.deepcopy(original);new.update(author_provenance={'actor_id':'sibling-author','session_id':'sibling-author-session'},
        units=[copy.deepcopy(u)for u in original['units']if u['unit_id']==uid],
        claims=[copy.deepcopy(c)for c in original['claims']if c['unit_id']==uid])
    added=dict(new['claims'][0],claim_id=uid+'-new-atom',statement_ko='Additional sibling atom '+uid)
    new['claims'].append(added);new['units'][0].update(claim_count=3,census_status='COMPLETE_AUTHOR_ENUMERATION_PENDING_INDEPENDENT_COMPLETENESS_CHECK')
    cb=put(root,path+'-census.json',new)
    row=next(json.loads(x)for x in(root/q.LEDGER).read_text().splitlines()if json.loads(x)['unit_id']==uid)
    r=dict(schema_version=1,purpose=census.PURPOSE,reassessment_id='sibling-'+uid,unit_id=uid,
        body_sha256=binding['body_sha256'],previous_job_id=parent['job_id'],previous_job_sha256=q.digest(parent),
        previous_binding=binding,previous_result={'path':parent['result']['result_path'],'raw_sha256':parent['result_sha256']},
        previous_report=parent['result']['evidence'],previous_ledger_fields={k:row.get(k)for k in census.LEDGER_FIELDS},
        replacement={'census_path':cb['path'],'census_sha256':cb['raw_sha256'],'notes_revision':row['atomic_census_notes_revision']},
        author_provenance=new['author_provenance'],change_basis='Synthetic independently recorded missing sibling atom',
        claim_mapping={c['claim_id']:[c['claim_id']]for c in original['claims']if c['unit_id']==uid},
        changed_claim_ids=[],added_claim_ids=[added['claim_id']],omission_resolutions=[
            {'omission_sha256':q.raw_sha(b'Omitted sibling atom'),'claim_ids':[added['claim_id']],'explanation':'Explicit synthetic atom for the recorded omission'}])
    put(root,path+'-record.json',r);commit(root,'immutable actual synthetic sibling version')
    return path+'-record.json',r,new


def select(root,notes,record,new):
    rows=[json.loads(x)for x in(root/q.LEDGER).read_text().splitlines()]
    rows=[census.replacement_row(record,new)if x['unit_id']==record['unit_id']else x for x in rows]
    (root/q.LEDGER).write_text(''.join(json.dumps(x)+'\n'for x in rows));commit(root,'select registered sibling census')
    return q.inventory(root,notes)


@pytest.mark.parametrize('correction',['sibling_omissions'],indirect=True)
@pytest.mark.parametrize('order',['siblings-first','inactive-first'])
def test_three_legitimate_sibling_versions_preserve_historical_body_and_inactive_zero_credit(successor_fixture,order):
    root,notes,inv,state,parent,r,path=successor_fixture
    original_body_record=(root/r['body_parent_record']['path']).read_bytes();original_parent=q.encoded(parent)
    snapshot=(root/r['active_ledger_snapshot']['path']).read_bytes()
    job=None
    if order=='inactive-first':job=register(successor_fixture);integrate(successor_fixture,job)
    for uid in ['a-second','m-third','b-fourth']:
        p,record,new=sibling_record((root,notes,inv,state,parent,r,path),uid)
        jid=census.register(state,inv,root,p,notes,NOW);persist(root,state)
        inv=select(root,notes,record,new);node=q.job_for(state,jid)
        body.validate_registered(state,root,notes,inv=inv)  # Historical C31 never froze live305.
        if job:
            proof=inactive.sibling_evolution(job,inv,state)
            assert proof[-1]['native_census_supersessions'][-1]['independent_credit_created']==0
            assert load_metadata(root,notes)['units'][r['unit_id']]['current_review_valid']is False
        q.claim(state,inv,'sibling-reviewer-'+uid,'sibling-session-'+uid,'Synthetic actual separate non-author',at=NOW)
        result,_=worker_result((root,notes,inv),state,node,lambda report:final_review(node,report))
        q.submit(state,jid,node['lease_token'],q.encoded(result),root,inv,NOW);persist(root,state)
        integrate_files(root,result);q.integrate(state,jid,root,inv,NOW);persist(root,state)
    if job:
        assert len(inactive.sibling_evolution(job,inv,state))==3
        assert q.digest({k:b for k,b in inv['units'].items()if k!=r['unit_id']})!=r['other_current_bindings_sha256']
        assert (root/r['active_ledger_snapshot']['path']).read_bytes()==snapshot
    else:
        # Retain a NEW actual current snapshot before registration; never patch
        # the earlier immutable record or fabricate an active candidate ledger.
        newpath=path.replace('record.json','after-siblings-ledger.jsonl')
        (root/newpath).write_bytes((root/q.LEDGER).read_bytes());commit(root,'retain new real active binding snapshot')
        replacement=inactive.propose(root,'after-three-native-siblings',newpath,notes)
        put(root,path.replace('record.json','after-siblings-record.json'),replacement);commit(root,'new inactive registration proposal')
        jid=inactive.register(state,inv,root,path.replace('record.json','after-siblings-record.json'),notes,NOW);persist(root,state)
        job=q.job_for(state,jid);assert inactive.sibling_evolution(job,inv,state)==[]
    assert (root/r['body_parent_record']['path']).read_bytes()==original_body_record and q.encoded(parent)==original_parent
    assert load_metadata(root,notes)['units'][r['unit_id']]['current_review_valid']is False
    changed=copy.deepcopy(inv);changed['units']['last']['ledger_binding_sha256']='0'*64
    with pytest.raises(ValueError,match='no exact append-only'):
        inactive.current(job,changed,state)
    # A completed latest version cannot be silently rewound to the original
    # snapshot merely because its original fingerprint would match again.
    old=q.inventory(root,notes,ledger_raw=snapshot)
    with pytest.raises(ValueError):inactive.current(job,old,state)
