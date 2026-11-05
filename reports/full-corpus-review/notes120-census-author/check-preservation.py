"""Record exact original-object preservation and committed input-byte equality."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
import note_review_queue as q
P='reports/full-corpus-review/notes120-census-author/'
index=json.loads((ROOT/(P+'proposal-index.json')).read_bytes());paths={};rows=[];statuses=[]
def add(path,sha=None):
 if not path:return
 if path in paths:
  if sha:assert paths[path]['disk_sha256']==sha
  return
 dst=q.safe_path(ROOT,path);head=subprocess.check_output(['git','show','HEAD:'+path],cwd=ROOT)
 if not dst.exists():dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(head)
 raw=dst.read_bytes()
 assert raw==head
 if sha:assert q.raw_sha(raw)==sha
 paths[path]={'head_sha256':q.raw_sha(head),'disk_sha256':q.raw_sha(raw),'head_equals_disk':True}
def authority_paths(obj):
 if isinstance(obj,list):
  for child in obj:authority_paths(child)
 elif isinstance(obj,dict):
  for key,val in obj.items():
   if key.endswith('_path') and isinstance(val,str):
    skey=key[:-5]+'_sha256'
    if obj.get(skey):add(val,obj[skey])
   if key=='source_evidence'and isinstance(val,str)and obj.get('source_evidence_sha256'):add(val,obj['source_evidence_sha256'])
   if isinstance(val,(dict,list)):authority_paths(val)
for p in index['finalized_real_integrated_predecessors']:
 raw=(ROOT/p['record_path']).read_bytes();assert q.raw_sha(raw)==p['record_sha256'];record=json.loads(raw);add(p['record_path'],p['record_sha256'])
 b=record['previous_binding'];add(b['census_path'],b['census_sha256']);old=json.loads((ROOT/b['census_path']).read_bytes());new=json.loads((ROOT/p['census_path']).read_bytes());uid=p['unit_id']
 oldclaims=[c for c in old['claims']if c['unit_id']==uid];newbyid={c['claim_id']:c for c in new['claims']}
 assert [c['claim_id']for c in oldclaims]==list(record['claim_mapping'])
 assert all(record['claim_mapping'][c['claim_id']]==[c['claim_id']]and q.digest(c)==q.digest(newbyid[c['claim_id']])for c in oldclaims)
 assert all(q.digest(s)==q.digest(new['sources'][sid])for sid,s in old['sources'].items())
 assert record['changed_claim_ids']==[]
 assert (ROOT/(P+'bodies/'+uid+'.txt')).read_bytes()==next(x['unit']['body'].encode()for ab in 'bcde'for x in json.loads(Path('/workspace/scratch/notes120-'+ab+'-visible-input.json').read_bytes())['units']if x['unit']['id']==uid)
 assert q.raw_sha((ROOT/(P+'bodies/'+uid+'.txt')).read_bytes())==record['body_sha256']
 add(p['census_path'],p['census_sha256']);authority_paths(new['sources'])
 for key in ['previous_report','previous_result']:
  e=record[key];add(e['path'],e['raw_sha256'])
 report=json.loads((ROOT/record['previous_report']['path']).read_bytes());authority_paths([a for r in report['records']for c in r['claims']for a in c.get('authorities',[])])
 originalrow=next(r for r in report['records']if r['unit_id']==uid)
 assert len(record['omission_resolutions'])==len(originalrow['omissions'])
 for o,res in zip(originalrow['omissions'],record['omission_resolutions']):assert q.raw_sha(o.encode())==res['omission_sha256']
 appended=[newbyid[cid]for cid in record['added_claim_ids']];statuses.extend(c['review_status']for c in appended)
 assert len(new['claims'])==len(oldclaims)+len(appended)
 rows.append({'unit_id':uid,'original_claim_count':len(oldclaims),'proposed_claim_count':len(new['claims']),'added_claim_count':len(appended),'all_original_claim_canonical_records_preserved':True,'original_sources_preserved_count':len(old['sources']),'all_original_source_canonical_records_preserved':True,'original_body_bytes_preserved':True,'changed_claim_ids':[],'original_omission_count':len(originalrow['omissions']),'exact_omission_sha_binding':True})
assert len(rows)==9 and sum(r['original_claim_count']for r in rows)==179 and sum(r['proposed_claim_count']for r in rows)==194
assert statuses.count('AUTHOR_SOURCE_CHECKED')==6 and statuses.count('SOURCE_BLOCKED')==9
base='eb74b0f4';changed=subprocess.check_output(['git','diff','--name-only',base,'HEAD'],cwd=ROOT).decode().splitlines();assert changed and all(p.startswith(P)for p in changed)
head=q.git(ROOT,'rev-parse','HEAD')
(ROOT/(P+'historical-byte-check.json')).write_bytes(q.encoded({'validation_head':head,'committed_input_path_count':len(paths),'all_head_equals_disk':True,'paths':paths}))
(ROOT/(P+'preservation-and-scope-check.json')).write_bytes(q.encoded({'validation_head':head,'root_integration_base':q.git(ROOT,'rev-parse',base),'records':rows,'original_claims':179,'proposed_claims':194,'added_claims':15,'added_author_source_checked':6,'added_source_blocked':9,'all_original_claims_and_sources_canonical_preserved':True,'all_original_bodies_byte_preserved':True,'all_changed_claim_ids_empty':True,'authored_committed_diff_paths_from_root_base':changed,'all_authored_diff_paths_in_own_prefix':True,'shared_queue_ledger_body_question_generated_guard_modifications':0,'controller_registration_performed':False,'canonical_release_credit':0,'question_audit_credit':0,'independent_audit_credit':0}))
print(json.dumps({'units':len(rows),'claims':'179 + 15 = 194','new_statuses':'6 AUTHOR_SOURCE_CHECKED / 9 SOURCE_BLOCKED','committed_head_equals_disk_paths':len(paths),'outside_prefix_authored_changes':0},ensure_ascii=False))
