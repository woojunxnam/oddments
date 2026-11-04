"""Bind only real INTEGRATED predecessors from this checkout's committed native state."""
import json,sys,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
import note_review_queue as q
import notes_census_reassessment as nr
P='reports/full-corpus-review/notes120-census-author/'
def write(path,obj):
 (ROOT/path).write_bytes(q.encoded(obj));return q.raw_sha((ROOT/path).read_bytes())
def materialize(path,sha=None):
 raw=subprocess.check_output(['git','show','HEAD:'+path],cwd=ROOT)
 if sha:assert q.raw_sha(raw)==sha
 dst=ROOT/path
 if not dst.exists():dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
 assert dst.read_bytes()==raw
 return raw
state=json.loads(materialize(q.STATE));nr.validate_chain(state)
index=json.loads((ROOT/(P+'preparation-index.json')).read_bytes());ledger=[json.loads(l)for l in materialize(q.LEDGER).decode().splitlines()]
fullinv_path=Path('/workspace/scratch/notes120-verified-inventory.json');invraw=fullinv_path.read_bytes();fullinv=json.loads(invraw)
assert q.raw_sha(invraw)=='7cf289aa77c60447eaf007249fb482b7ad1774a7fa687c086cdd8228d0275442'
units={u['id']:u for ch in fullinv['notes']['chapters']for u in ch['units']}
assert len(units)==306
for uid,b in fullinv['units'].items():assert q.raw_sha(units[uid]['body'].encode())==b['body_sha256']
finals=[];pending=[]
for row in index['records']:
 uid=row['unit_id'];job=nr.latest_jobs(state).get(uid)
 if not job or job['status']!='INTEGRATED':pending.append(uid);continue
 assert job['unit_bindings'][uid]==row['original_binding']
 materialize(row['original_binding']['census_path'],row['original_binding']['census_sha256'])
 result=job['result'];report=json.loads(materialize(result['evidence']['path'],result['evidence']['raw_sha256']))
 materialize(result['result_path'],job['result_sha256'])
 review=next(r for r in report['records']if r['unit_id']==uid);assert review['completeness']=='OMISSIONS_FOUND'
 for path,sha in q.validate_evidence(job,result,report):materialize(path,sha)
 fields={k:next(r for r in ledger if r['unit_id']==uid)[k]for k in nr.LEDGER_FIELDS};assert q.digest(fields)==row['original_binding']['ledger_binding_sha256']
 census=json.loads((ROOT/row['census_path']).read_bytes());census['stage']='AUTHOR_PROPOSAL_PENDING_INDEPENDENT_REASSESSMENT';csha=write(row['census_path'],census)
 for source in census['sources'].values():
  if not source['source_evidence'].startswith(P):materialize(source['source_evidence'],source['source_evidence_sha256'])
 rec={'schema_version':1,'purpose':nr.PURPOSE,'reassessment_id':'notes120-census-omission-'+uid+'-v1','unit_id':uid,'body_sha256':row['body_sha256'],'previous_job_id':job['job_id'],'previous_job_sha256':q.digest(job),'previous_binding':row['original_binding'],'previous_result':{'path':result['result_path'],'raw_sha256':job['result_sha256']},'previous_report':result['evidence'],'previous_ledger_fields':fields,'replacement':{'census_path':row['census_path'],'census_sha256':csha,'notes_revision':fields['atomic_census_notes_revision']},'author_provenance':index['author_provenance'],'change_basis':'실제 native INTEGRATED 독립감사의 원 누락지적을 보존하고 별도 저자가 누락명제만 append했다. 기존 법규 HOLD/SOURCE_BLOCKED 해소 및 독립 PASS 인정은 수행하지 않는다.','claim_mapping':{cid:[cid]for cid in row['original_binding']['claim_record_sha256s']},'added_claim_ids':row['added_claim_ids'],'changed_claim_ids':[],'omission_resolutions':[{'omission_sha256':q.raw_sha(o.encode()),'claim_ids':row['added_claim_ids'],'explanation':'단원 전문과 기존 원자 전량을 읽고 이 누락에 해당하는 실제 새 명제를 append했다. 원 claim/source canonical 내용과 기존 blocker는 보존한다. 정확한 법규 적용범위를 확정하지 못한 신규 명제는 SOURCE_BLOCKED로 열거하며 독립 완전성 해소 여부는 새 실제 비저자 감사자가 판단한다.'}for o in review['omissions']]}
 rp=P+uid+'-reassessment.json';rsha=write(rp,rec)
 row['census_sha256']=csha;row['final_integrated_predecessor_record']=rp
 finals.append({'unit_id':uid,'census_path':row['census_path'],'census_sha256':csha,'record_path':rp,'record_sha256':rsha,'previous_job_id':job['job_id'],'previous_job_sha256':q.digest(job),'previous_report':result['evidence']})
write(P+'preparation-index.json',index)
write(P+'proposal-index.json',{'purpose':nr.PURPOSE,'author_provenance':index['author_provenance'],'canonical_release_credit':0,'question_audit_credit':0,'independent_audit_credit':0,'finalized_real_integrated_predecessors':finals,'pending_integrated_predecessors':pending,'notes_inventory_raw_sha256':q.raw_sha(invraw),'all306_body_hashes_reconfirmed':True})
print(json.dumps({'finalized':[r['unit_id']for r in finals],'pending':pending},ensure_ascii=False))
