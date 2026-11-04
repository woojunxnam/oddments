"""Three actual integrated native parents; append-only author artifacts only."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT/'scripts'))
import note_review_queue as q
import notes_census_reassessment as nr
BASE='b19b58cfd56699fc62e0723b9ded621f73c45866';IG='2f41b903ed1ea85bcbe4b7f88ca2555f3704fed0'
P='reports/full-corpus-review/final19-census-author/w4-b-17-v2/'
SPECS=[('w4-b-17',64,41,43,'3d2142510882880cf1e7a4592ed7feabba1bf607b9c4e23827ceed53b1c60f09','640bcb7bb541f980eade7f587a9a70d0cc4adcbde83dd5b4d6a876cc274e7ca4'),('w5-a-12',65,17,18,'87469103eeb5638394e5bdc33e24d19af669e200435788b95921ff4bfb81bb4b','d6b07781bbd667753dfdb4fd32bc1b2080ba5fef8e08d4e26df37041158a794f'),('parallel-duties',67,10,12,'2ab4bc977b35bc6f1cb0f5537d8df327c83d4becffb347b78fdf43b3d8cb85e6','0d1c4ab3ead2e96634c50bab6b4465fe5b253534fe786f53e573f9d3020ffa98')]
def blob(commit,path):return subprocess.check_output(['git','show',commit+':'+path],cwd=ROOT)
def write(path,obj):
 (ROOT/path).write_bytes(q.encoded(obj));return q.raw_sha((ROOT/path).read_bytes())
paths={}
def read(path,sha=None):
 if path not in paths:
  raw=blob('HEAD',path);assert (ROOT/path).read_bytes()==raw;paths[path]=raw
 if sha:assert q.raw_sha(paths[path])==sha
 return paths[path]
state=json.loads(read(q.STATE));assert read(q.STATE)==blob(BASE,q.STATE);q.validate_state(state)
igstate=json.loads(blob(IG,q.STATE));guard=json.loads((ROOT/(P+'bundle-own-head-strict-native-inventory-proof.json')).read_bytes());assert guard['source_guard_passed']is True
invraw=(ROOT/(P+'bundle-own-head-strict-native-inventory.json')).read_bytes();assert q.raw_sha(invraw)==guard['inventory_raw_sha256'];inv=json.loads(invraw);notes=inv['notes'];ledger=read(q.LEDGER,inv['ledger_sha256']);current=q.inventory(ROOT,notes,ledger_raw=ledger);assert current['total_units']==306 and current['units']==inv['units']
ledgerrows=[json.loads(l)for l in ledger.decode().splitlines()];out=[]
for uid,seq,nold,nnew,rsha,esha in SPECS:
 prefix='reports/full-corpus-review/final19-census-author/'+uid+'-v2/';prep=json.loads((ROOT/(prefix+'preparation-index.json')).read_bytes());job=nr.latest_jobs(state)[uid];assert job['sequence']==seq and job['status']=='INTEGRATED'and job['unit_bindings'][uid]==prep['original_binding']==current['units'][uid]
 assert q.digest(job)==q.digest(next(j for j in igstate['jobs']if j['sequence']==seq))
 result=job['result'];assert job['result_sha256']==esha and result['evidence']['raw_sha256']==rsha
 report=json.loads(read(result['evidence']['path'],rsha));read(result['result_path'],esha);assert read(result['evidence']['path'])==(ROOT/(prefix+'inputs/report.json')).read_bytes()
 for path,sha in q.validate_evidence(job,result,report):read(path,sha)
 census=json.loads((ROOT/(prefix+'census.json')).read_bytes());assert len(census['claims'])==nnew
 old=json.loads(read(prep['original_binding']['census_path'],prep['original_binding']['census_sha256']));assert len(old['claims'])==nold
 assert all(q.digest(a)==q.digest(b)for a,b in zip(old['claims'],census['claims']))and all(q.digest(s)==q.digest(census['sources'][sid])for sid,s in old['sources'].items())
 for s in census['sources'].values():
  if not s['source_evidence'].startswith(prefix):read(s['source_evidence'],s['source_evidence_sha256'])
 fields={k:next(r for r in ledgerrows if r['unit_id']==uid)[k]for k in nr.LEDGER_FIELDS};assert q.digest(fields)==prep['original_binding']['ledger_binding_sha256']
 row=next(r for r in report['records']if r['unit_id']==uid);assert row['completeness']=='OMISSIONS_FOUND'and len(row['omissions'])==len(prep['omission_resolutions'])
 for omission,res in zip(row['omissions'],prep['omission_resolutions']):assert q.raw_sha(omission.encode())==res['omission_sha256']
 census['stage']='AUTHOR_PROPOSAL_PENDING_INDEPENDENT_REASSESSMENT';csha=write(prefix+'final-census.json',census)
 rec={'schema_version':1,'purpose':nr.PURPOSE,'reassessment_id':'final19-census-'+uid+'-v2','unit_id':uid,'body_sha256':prep['body_sha256'],'previous_job_id':job['job_id'],'previous_job_sha256':q.digest(job),'previous_binding':prep['original_binding'],'previous_result':{'path':result['result_path'],'raw_sha256':esha},'previous_report':result['evidence'],'previous_ledger_fields':fields,'replacement':{'census_path':prefix+'final-census.json','census_sha256':csha,'notes_revision':fields['atomic_census_notes_revision']},'author_provenance':prep['author_provenance'],'change_basis':'실제 통합된 비저자 보고서의 원누락을 같은실제보완저자가 별도명제로 append했다. 원명제/source/body/기존보류를보존하고 법규 HOLD/SB 해소·독립 PASS·release판정을 수행하지 않는다.','claim_mapping':{cid:[cid]for cid in prep['original_binding']['claim_record_sha256s']},'added_claim_ids':prep['added_claim_ids'],'changed_claim_ids':[],'omission_resolutions':prep['omission_resolutions']};rrsha=write(prefix+'reassessment.json',rec)
 item={'unit_id':uid,'sequence':seq,'census_path':prefix+'final-census.json','census_sha256':csha,'record_path':prefix+'reassessment.json','record_sha256':rrsha,'previous_job_id':job['job_id'],'previous_job_sha256':q.digest(job),'previous_report':rec['previous_report'],'previous_result':rec['previous_result'],'original_claim_count':nold,'final_claim_count':nnew,'actual_integrated_parent_commit':IG,'root_state_commit':BASE,'controller_registration_performed':False,'independent_credit':0,'release_credit':0};write(prefix+'final-proposal-index.json',item);out.append(item)
write(P+'bundle-final-index.json',{'purpose':nr.PURPOSE,'root_state_commit':BASE,'actual_integration_commit':IG,'source_guard_proof':P+'bundle-own-head-strict-native-inventory-proof.json','own_actual_full_inventory_raw_sha256':q.raw_sha(invraw),'ledger_sha256':inv['ledger_sha256'],'records':out,'controller_registration_performed':False,'canonical_release_credit':0,'question_audit_credit':0,'independent_audit_credit':0})
write(P+'bundle-final-materialization-proof.json',{'root_state_commit':BASE,'integration_commit':IG,'references_head_equals_disk':{p:q.raw_sha(raw)for p,raw in paths.items()},'full306_native_inventory_matched':True,'controller_registration_performed':False})
print([(r['unit_id'],r['sequence'],r['original_claim_count'],r['final_claim_count'])for r in out])
