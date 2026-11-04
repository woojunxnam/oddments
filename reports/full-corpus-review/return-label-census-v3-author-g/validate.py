"""Immutable source-only v3 packet checks; never registration/completion/legal credit."""
import copy
import datetime
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
P = 'reports/full-corpus-review/return-label-census-v3-author-g'
BASE = '39e7a566cc05ba6f489807605db83b239f790773'
CID = 'NOTE-CENSUS-V3-RETURN-PATHWAYS-ADD-001'
sys.path.insert(0,str(ROOT/'scripts'))
import note_review_queue as q
import notes_census_reassessment as cr
from notes_revision import load_notes


def load(path):
    return json.loads((ROOT/path).read_bytes())


def read(path,digest):
    raw = (ROOT/path).read_bytes()
    assert q.raw_sha(raw) == digest, path
    return raw


def preserve(old,new):
    assert len(old['claims']) == 29 and len(new['claims']) == 30
    assert new['claims'][:29] == old['claims']
    assert new['claims'][29]['claim_id'] == CID
    assert all(new['sources'][key] == value for key,value in old['sources'].items())
    assert new['units'][0]['unit_content_sha256'] == old['units'][0]['unit_content_sha256']
    assert new['units'][0]['claim_count'] == 30
    assert new['units'][0]['source_blocked_claim_count'] == 2
    assert new['units'][0]['independent_verified_claim_count'] == 0
    assert new['units'][0]['census_status'] == 'COMPLETE_AUTHOR_ENUMERATION_PENDING_INDEPENDENT_COMPLETENESS_CHECK'
    assert new['current_review_valid'] is False and new['current_coverage_credit'] == 0
    assert new['registration_executed'] is False
    for claim in new['claims']:
        assert claim['independent'] is False
    assert new['claims'][29]['related_question_ids'] == []
    assert new['claims'][29]['question_alignment'] == 'NOT_ASSESSED'
    assert new['claims'][29]['review_status'] == 'AUTHOR_SOURCE_CHECKED'
    assert new['author_provenance'] == {'actor_id':'/root/independent_case_g','session_id':'/root/independent_case_g'}
    assert new['author_instance'] == 'gpt-independent-phase3-g-root-independent_case_g-20261103'


def validate():
    report = load(P+'/author-report.json')
    pres = load(P+'/preservation-manifest.json')
    old = load(pres['original_census']['path'])
    new = load(P+'/census.json')
    candidate = load(P+'/registration-candidate.json')
    state = load(q.STATE)
    notes = load_notes(ROOT)
    unit = next(u for c in notes['chapters'] for u in c['units'] if u['id']=='return-pathways')
    preserve(old,new)
    for item in pres['protected_source_files']:
        raw = read(item['path'],item['raw_sha256'])
        assert raw == subprocess.check_output(['git','show',BASE+':'+item['path']],cwd=ROOT)
    assert pres['old_claims'] == {c['claim_id']:q.digest(c) for c in old['claims']}
    assert pres['old_source_objects'] == {k:q.digest(v) for k,v in old['sources'].items()}
    assert len(pres['old_source_objects']) == 32
    assert pres['actual_D36_carried_legal_blockers'] == report['actual_D36_carried_legal_blockers'] == {}
    assert [c['claim_id'] for c in new['claims'] if c['review_status']=='SOURCE_BLOCKED'] == pres['old_author_SOURCE_BLOCKED_claim_ids']
    assert candidate['added_claim_ids'] == [CID] and candidate['changed_claim_ids'] == []
    assert candidate['source_only_registration_candidate'] is True and candidate['actual_registration_executed'] is False
    assert candidate['claim_mapping'] == {c['claim_id']:[c['claim_id']] for c in old['claims']}
    snapshot = load(P+'/evidence/parent-snapshot.json')
    job = next(j for j in state['jobs'] if j['job_id']==candidate['previous_job_id'])
    assert job['status']=='INTEGRATED' and job['sequence']==36
    assert q.digest(job) == snapshot['parent_job_sha256'] == candidate['previous_job_sha256']
    assert job == snapshot['parent_job']
    assert q.raw_sha(unit['body'].encode()) == report['body_sha256'] == candidate['body_sha256']
    assert (ROOT/P/'evidence/return-pathways-existing-body.txt').read_bytes() == unit['body'].encode()
    assert q.raw_sha(snapshot['exact_omission'].encode()) == candidate['omission_resolutions'][0]['omission_sha256']
    assert len(candidate['omission_resolutions']) == 1
    bound,carried = cr.validate_record(state,candidate,ROOT,notes,read)
    assert len(bound['claim_record_sha256s'])==30 and carried=={}
    for field in ['census','registration_candidate','parent_report','parent_result','fresh_primary_register','materiality_and_primary_memo','preservation_manifest']:
        read(report[field]['path'],report[field]['raw_sha256'])
    sources = load(P+'/evidence/source-register.json')['sources']
    assert len(sources)==2
    for sid,source in sources.items():
        assert source['retrieved_at'].startswith('2026-11-04T10:02:08')
        assert source['http_status']==200 and source['tls_verification'] is True
        assert source['effective_date'] is None and 'UNKNOWN' in source['effective_date_note']
        assert read(source['source_evidence'],source['source_evidence_sha256']).startswith(b'%PDF')
        text = ' '.join(read(source['extracted_path'],source['extracted_sha256']).decode().split())
        meta = json.loads(read(source['metadata_path'],source['metadata_sha256']))
        assert meta['body_verification']=='CORRECT_OFFICIAL_DOCUMENT_CONTROLLING_PROVISIONS_PERSONALLY_READ'
        assert meta['used_as_legal_proof'] is True
        if sid=='GL3-practice9':
            assert 'A pharmacy shall label the multi-drug-single-dose package in accordance with 247 CMR 9.08(5) prior to re-dispensing.' in text
        else:
            assert 'Prior to re-dispensing, if the compliance package has removable cells' in text
            assert 'the name, strength, physical description, and total quantity of each drug dispensed' in text
    manifest = ROOT/P/'artifact-manifest.json'
    if manifest.exists():
        items=json.loads(manifest.read_text())['files']
        assert {r['path'] for r in items} == {str(p.relative_to(ROOT)) for p in (ROOT/P).rglob('*') if p.is_file() and p!=manifest}
        for item in items:read(item['path'],item['raw_sha256'])
    return old,new,candidate,state,unit


def negatives(old,new,candidate,state,unit):
    rejected=[]
    def reject(name,call):
        try:call()
        except (AssertionError,ValueError,KeyError):rejected.append(name)
        else:raise AssertionError('Mutation accepted: '+name)
    def changed_new(mutate):
        changed=copy.deepcopy(new);mutate(changed);preserve(old,changed)
    reject('old29_statement_mutation',lambda:changed_new(lambda x:x['claims'][0].update(statement_ko='Changed old proposition')))
    reject('old32_source_object_mutation',lambda:changed_new(lambda x:next(iter(x['sources'].values())).update(checked_at='NEW_DATE')))
    reject('second_added_atom_forbidden',lambda:changed_new(lambda x:x['claims'].append(dict(x['claims'][-1],claim_id='UNAUTHORIZED-SECOND-ATOM'))))
    reject('historical_author_SB013_deleted',lambda:changed_new(lambda x:x['claims'].pop(12)))
    reject('historical_author_SB026_upgraded',lambda:changed_new(lambda x:x['claims'][25].update(review_status='AUTHOR_SOURCE_CHECKED',blocker=None)))
    reject('automatic_current_completion_credit',lambda:changed_new(lambda x:x.update(current_review_valid=True,current_coverage_credit=1)))
    changed_unit=copy.deepcopy(unit);changed_unit['body']+=' Unauthorized body change.'
    reject('body_change_outside_census_scope',lambda:cr.validate_record(state,candidate,ROOT,{'chapters':[{'units':[changed_unit]}]},read))
    cleared=copy.deepcopy(candidate);cleared['omission_resolutions']=[]
    reject('D36_negative_omission_mapping_deleted',lambda:cr.validate_record(state,cleared,ROOT,{'chapters':[{'units':[unit]}]},read))
    rewritten=copy.deepcopy(candidate);rewritten['previous_report']['raw_sha256']='0'*64
    reject('D36_negative_report_binding_rewritten',lambda:cr.validate_record(state,rewritten,ROOT,{'chapters':[{'units':[unit]}]},read))
    return rejected


if __name__=='__main__':
    old,new,candidate,state,unit=validate();cases=negatives(old,new,candidate,state,unit)
    result={'status':'PASS_SOURCE_PRESERVATION_AND_READ_ONLY_NATIVE_CANDIDATE_COMPATIBILITY','validated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_claim_objects_preserved':29,'original_source_objects_preserved':32,'new_atoms':1,'final_claims':30,'historical_author_SB_preserved':2,'actual_D36_carried_legal_blockers':{},'fresh_current_official_primary_payloads':2,'negative_cases_rejected':cases,'body_edits':0,'native_registrations':0,'new_independent_audits':0,'new_current_COMPLETE':0,'new_legal_PASS':0,'all_new_credits':0}
    if '--receipt' in sys.argv:
        assert not (ROOT/P/'artifact-manifest.json').exists()
        (ROOT/P/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
