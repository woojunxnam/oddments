"""Read-only by default. This validates audit bindings, not legal truth or release credit."""
import argparse,gzip,hashlib,json,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parents[4]
R=Path('/workspace/oddments')
S=Path('/tmp/census-reassessment-v2-c-controller-snapshot')
P='reports/full-corpus-review/independent-notes/'
E=P+'census-v2-c-evidence/'
sys.path.insert(0,str(R/'scripts'))
import note_review_queue as q
from notes_revision import load_notes

def raw(p):return p.read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.PIPE)
def envelope(a,r):
 d={k:a[k] for k in ['stage','actor_provenance','auditor','auditor_instance']}
 d.update(independent_of_authors=True,canonical_audit=False,canonical_release_credit=0,question_audit_credit=0,worker_commit=git(W,'rev-parse','HEAD').decode().strip(),unit_hashes={u:b['body_sha256'] for u,b in a['unit_bindings'].items()},evidence={'path':P+'census-v2-c-review.json','raw_sha256':sha(raw(W/(P+'census-v2-c-review.json')))},result_path=P+a['job_id']+'-result.json',results=[{k:x[k] for k in ['unit_id','completeness','legal_status']} for x in r['records']])
 return d

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--postcommit',action='store_true');ap.add_argument('--record',action='store_true');ap.add_argument('--write-envelope',action='store_true');args=ap.parse_args()
 a=json.loads(raw(Path('/tmp/census-reassessment-v2-c-assignment.json')));r=json.loads(raw(W/(P+'census-v2-c-review.json')));m=envelope(a,r);uid=a['unit_ids'][0];b=a['unit_bindings'][uid];checks=[]
 q.validate_result(a,m);q.validate_evidence(a,m,r);checks+=['current_root_native_validate_result','current_root_native_validate_evidence']
 q.current(a,q.inventory(S));checks+=['committed_e332_runtime_snapshot_native_inventory_current']
 roothead=git(R,'rev-parse','HEAD').decode().strip();state=json.loads(raw(R/q.STATE));job=next(j for j in state['jobs'] if j['job_id']==a['job_id']);assert job['unit_bindings']==a['unit_bindings'];assert job['actor_provenance']==a['actor_provenance'];q.current(a,q.inventory(R),state);checks+=['current_root_native_inventory_current']
 for rel in [b['census_path'],'reports/full-corpus-review/census-corrections/v2/record/w2-c-12-census-v2-record.json',q.LEDGER,q.STATE]:assert git(R,'show',roothead+':'+rel)==raw(R/rel)
 checks+=['current_root_runtime_binding_files_equal_current_committed_bytes']
 cn=json.loads(raw(S/b['census_path']));assert sha(raw(S/b['census_path']))==b['census_sha256'];assert len(cn['claims'])==22
 for c in cn['claims']:assert q.digest(c)==b['claim_record_sha256s'][c['claim_id']]
 version=json.loads(raw(S/'reports/full-corpus-review/census-corrections/v2/record/w2-c-12-census-v2-record.json'));assert sha(raw(S/'reports/full-corpus-review/census-corrections/v2/record/w2-c-12-census-v2-record.json'))==a['reassessment_record_sha256']
 old=json.loads(raw(S/version['previous_binding']['census_path']));old={c['claim_id']:c for c in old['claims'] if c['unit_id']==uid};new={c['claim_id']:c for c in cn['claims']};assert len(old)==21 and all(new[k]==v for k,v in old.items());assert set(new)-set(old)==set(version['added_claim_ids'])
 for f in [version['previous_report'],version['previous_result']]:assert sha(raw(S/f['path']))==f['raw_sha256'] and raw(S/f['path'])==git(R,'show',roothead+':'+f['path'])
 assert r['records'][0]['reassessment_review']=={**a['reassessment_review'],'final_census_read_completely':True,'all_original_omissions_reassessed':True,'all_original_propositions_preserved':True};assert r['records'][0]['omission_resolution_assessments'][0]['omission_sha256']==a['reassessment_review']['omission_resolutions'][0]['omission_sha256'];checks+=['all22_exact_canonical_claim_hashes','all21_original_whole_json_objects_preserved','original_report_and_result_raw_bytes_preserved','exact_reassessment_review_and_omission_resolution']
 body=json.loads(raw(W/(E+'body-first-input.json')));assert sha(body['body'].encode())==b['body_sha256'];actual={u['id']:u for c in load_notes(R)['chapters'] for u in c['units']};assert actual[uid]['body']==body['body'];checks+=['current_final_actual_load_notes_body_unchanged']
 for s in r['sources']:
  data=raw(W/s['evidence_path']);assert sha(data)==s['evidence_sha256'];assert sha(gzip.decompress(data) if s['payload_type']=='HTML' else data)==s['raw_sha256'];assert s['http_status']==200 and s['verification_status']=='VERIFIED_TARGETED_PRIMARY_TEXT_READ'
 checks+=['all5_retained_fresh_primary_response_and_container_hashes']
 packet=json.loads(raw(W/(E+'practice-safe-inputs.json')));index=json.loads(raw(W/(E+'practice-lossless-index.json')))
 def un(x):
  if isinstance(x,dict):return index['texts'][x['text_ref']-1] if set(x)=={'text_ref'} else {k:un(v) for k,v in x.items()}
  if isinstance(x,list):return [un(v) for v in x]
  return x
 assert un(index['records'])==[v['original_visible_content'] for v in packet['records']]
 banks={}
 for row in packet['records']:
  path=row['collection']
  if path not in banks:banks[path]={z['question_id']:z for z in json.loads(raw(S/path))['questions']}
  original=banks[path][row['original_visible_content']['question_id']];assert q.digest(original)==row['whole_record_sha256'];assert {k:original[k] for k in row['original_visible_content']}==row['original_visible_content']
 assert len(packet['records'])==31 and sum(len(z['original_visible_content']['choices']) for z in packet['records'])==133;assert len(index['texts'])==132;checks+=['all31_safe_original_question_projections_133choices_and132string_lossless_reconstruction']
 assert all(x['inherited_legal_blockers']==a['carried_legal_blockers'][uid].get(x['claim_id'],[]) for x in r['records'][0]['claims']);checks+=['carried_legal_blockers_exact_no_census_only_clearance']
 if args.postcommit:
  assert json.loads(Path('/tmp/census-reassessment-v2-c-result.json').read_text())==m
  q.committed_evidence(a,m,W)
  changed=git(W,'diff','--name-only',a['base_commit']+'..'+m['worker_commit']).decode().splitlines();assert changed and all(p.startswith(P+'census-v2-c-') for p in changed);assert not git(W,'status','--porcelain').strip();checks+=['current_root_native_committed_evidence_exact_worker40sha','all_commit_range_paths_owned_prefix_only','worker_worktree_clean_postcommit']
 if args.write_envelope:
  assert args.postcommit is False
  Path('/tmp/census-reassessment-v2-c-result.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
 out={'status':'PASS','checks':checks,'controller_helper_root':str(R),'controller_helper_head':roothead,'runtime_snapshot_commit':(S/'SNAPSHOT_COMMIT.txt').read_text().strip(),'report_raw_sha256':m['evidence']['raw_sha256'],'worker_commit_checked':m['worker_commit'],'postcommit':args.postcommit,'verification_does_not_constitute_legal_or_question_release_credit':True}
 if args.record:(W/(E+'precommit-validation.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(out,ensure_ascii=False))
if __name__=='__main__':main()
