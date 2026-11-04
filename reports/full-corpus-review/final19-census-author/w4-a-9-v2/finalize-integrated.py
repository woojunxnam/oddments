"""Finalize against real immutable integrated job60; never register controller state."""
import copy,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT/'scripts'))
import note_review_queue as q
import notes_census_reassessment as nr
P='reports/full-corpus-review/final19-census-author/w4-a-9-v2/'
ROOT_BASE='af6b3901b62d8e7c6aae209a0d5e5643a447bb37'
INTEGRATED='f72332b7bb45f8717385eec3f0bee337df1c8c96'
INVENTORY=ROOT/(P+'own-head-strict-native-inventory.json')
INVSHA=json.loads((ROOT/(P+'own-head-strict-native-inventory-proof.json')).read_bytes())['inventory_raw_sha256']
def blob(commit,path):return subprocess.check_output(['git','show',commit+':'+path],cwd=ROOT)
def write(path,obj):
 dst=ROOT/path;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(q.encoded(obj));return q.raw_sha(dst.read_bytes())
materialized={}
def materialize(path,sha=None):
 if path not in materialized:
  raw=blob('HEAD',path);dst=ROOT/path
  if not dst.exists():dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
  assert dst.read_bytes()==raw
  materialized[path]=raw
 if sha:assert q.raw_sha(materialized[path])==sha
 return materialized[path]
state=json.loads(materialize(q.STATE));assert materialized[q.STATE]==blob(ROOT_BASE,q.STATE);q.validate_state(state)
prep=json.loads((ROOT/(P+'preparation-index.json')).read_bytes());uid=prep['unit_id'];job=nr.latest_jobs(state)[uid]
assert job['sequence']==60 and job['status']=='INTEGRATED' and job['unit_bindings'][uid]==prep['original_binding']
original_job=next(j for j in json.loads(blob(INTEGRATED,q.STATE))['jobs']if j['sequence']==60);assert q.digest(job)==q.digest(original_job)
raw=INVENTORY.read_bytes();assert q.raw_sha(raw)==INVSHA;captured=json.loads(raw);notes=captured['notes'];assert captured['total_units']==306
for binding in captured['units'].values():materialize(binding['census_path'],binding['census_sha256'])
ledgerraw=materialize(q.LEDGER);assert q.raw_sha(ledgerraw)==captured['ledger_sha256']
# Full native inventory, all306 units, all selected censuses; no projection or substitute ledger.
current=q.inventory(ROOT,notes,ledger_raw=ledgerraw)
assert current['total_units']==306 and current['units']==captured['units'] and current['ledger_sha256']==captured['ledger_sha256']
assert current['units'][uid]==job['unit_bindings'][uid]
actual={u['id']:u for ch in notes['chapters']for u in ch['units']};assert len(actual)==306
for u,b in captured['units'].items():assert q.raw_sha(actual[u]['body'].encode())==b['body_sha256']
result=job['result'];report=json.loads(materialize(result['evidence']['path'],result['evidence']['raw_sha256']));assert result['evidence']['raw_sha256']=='55ff9ea9dd7fc07d88091abedbcfc1fbc6596ed105deeb594e4e9117e1385ec4'
assert job['result_sha256']=='e328874a32c906399bf706c2c7cadb27540a1626a7c72e499f32a9707e8908ee';materialize(result['result_path'],job['result_sha256'])
assert (ROOT/(P+'inputs/report.json')).read_bytes()==materialized[result['evidence']['path']]
for path,sha in q.validate_evidence(job,result,report):materialize(path,sha)
for src in json.loads((ROOT/(P+'census.json')).read_bytes())['sources'].values():
 if not src['source_evidence'].startswith(P):materialize(src['source_evidence'],src['source_evidence_sha256'])
row=next(r for r in report['records']if r['unit_id']==uid);assert row['completeness']=='OMISSIONS_FOUND'and len(row['omissions'])==2
fields={k:next(r for r in [json.loads(l)for l in ledgerraw.decode().splitlines()]if r['unit_id']==uid)[k]for k in nr.LEDGER_FIELDS};assert q.digest(fields)==prep['original_binding']['ledger_binding_sha256']
census=json.loads((ROOT/(P+'census.json')).read_bytes());census['stage']='AUTHOR_PROPOSAL_PENDING_INDEPENDENT_REASSESSMENT';csha=write(P+'final-census.json',census)
rec={'schema_version':1,'purpose':nr.PURPOSE,'reassessment_id':'final19-census-w4-a-9-v2','unit_id':uid,'body_sha256':prep['body_sha256'],'previous_job_id':job['job_id'],'previous_job_sha256':q.digest(job),'previous_binding':prep['original_binding'],'previous_result':{'path':result['result_path'],'raw_sha256':job['result_sha256']},'previous_report':result['evidence'],'previous_ledger_fields':fields,'replacement':{'census_path':P+'final-census.json','census_sha256':csha,'notes_revision':fields['atomic_census_notes_revision']},'author_provenance':prep['author_provenance'],'change_basis':'실제 통합된 job60의 새 누락2개를 동일 실제 보완저자가 각각 새 SOURCE_BLOCKED 명제로 append했다. 원30개와 원source/body를 보존하며 법규 HOLD/SOURCE_BLOCKED 해소나 독립 PASS 판정은 하지 않는다.','claim_mapping':{cid:[cid]for cid in prep['original_binding']['claim_record_sha256s']},'added_claim_ids':prep['added_claim_ids'],'changed_claim_ids':[],'omission_resolutions':prep['omission_resolutions']}
assert all(q.raw_sha(o.encode())==r['omission_sha256']for o,r in zip(row['omissions'],rec['omission_resolutions']))
rsha=write(P+'reassessment.json',rec)
write(P+'final-proposal-index.json',{'purpose':nr.PURPOSE,'author_provenance':prep['author_provenance'],'actual_integrated_parent_commit':INTEGRATED,'isolated_root_state_commit':ROOT_BASE,'unit_id':uid,'census_path':P+'final-census.json','census_sha256':csha,'record_path':P+'reassessment.json','record_sha256':rsha,'previous_job_id':job['job_id'],'previous_job_sha256':q.digest(job),'previous_result':rec['previous_result'],'previous_report':rec['previous_report'],'full_native_inventory_raw_sha256':INVSHA,'committed_selected_ledger_sha256':q.raw_sha(ledgerraw),'full306_native_inventory_recomputed':True,'all306_body_hashes_reconfirmed':True,'old03_preparation_files_immutable':True,'controller_registration_performed':False,'canonical_release_credit':0,'question_audit_credit':0,'independent_audit_credit':0})
write(P+'final-preparation-materialization.json',{'state_commit':ROOT_BASE,'integration_commit':INTEGRATED,'all_materialized_head_equals_disk':True,'paths':{p:q.raw_sha(b)for p,b in materialized.items()},'full306_native_inventory_recomputed':True,'selected_unit_claims':len(current['units'][uid]['claim_record_sha256s']),'controller_registration_performed':False})
print('Finalized actual job60 parent; full306 strict native inventory matched; commit before native disk_reader validation')
