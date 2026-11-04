"""Read-only audit-binding checks; no queue/build/source edits or release credit."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
W=Path(__file__).resolve().parents[4];R=Path('/workspace/oddments');P='reports/full-corpus-review/independent-notes/';E=P+'body-v1-c-evidence/';F='reports/full-corpus-review/body-corrections/w3-a-3-v1/'
sys.path.insert(0,str(R/'scripts'));import note_review_queue as q;import notes_body_reassessment as br
from notes_revision import load_notes

def sha(b):return hashlib.sha256(b).hexdigest()
def git(root,*a):return subprocess.check_output(['git','-C',str(root),*a],stderr=subprocess.PIPE)
def j(p):return json.loads(p.read_bytes())
def make_envelope(a,r):
 d={k:a[k]for k in ['stage','actor_provenance','auditor','auditor_instance']};d.update(independent_of_authors=True,canonical_audit=False,canonical_release_credit=0,question_audit_credit=0,worker_commit=git(W,'rev-parse','HEAD').decode().strip(),unit_hashes={u:b['body_sha256']for u,b in a['unit_bindings'].items()},evidence={'path':P+'body-v1-c-review.json','raw_sha256':sha((W/(P+'body-v1-c-review.json')).read_bytes())},result_path=P+a['job_id']+'-result.json',results=[{k:x[k]for k in ['unit_id','completeness','legal_status']}for x in r['records']]);return d

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--record',action='store_true');ap.add_argument('--write-envelope',action='store_true');ap.add_argument('--postcommit',action='store_true');ar=ap.parse_args()
 a=j(Path('/tmp/w3-a-3-body-c-assignment.json'));r=j(W/(P+'body-v1-c-review.json'));m=make_envelope(a,r);uid='w3-a-3';b=a['unit_bindings'][uid];row=r['records'][0];checks=[]
 q.validate_result(a,m);q.validate_evidence(a,m,r);checks+=['current_root_native_result_and_full_body_evidence_contract_PASS']
 head=git(R,'rev-parse','HEAD').decode().strip();state=json.loads(git(R,'show',head+':'+q.STATE));actualjob=next(z for z in state['jobs']if z['job_id']==a['job_id']);assert actualjob['unit_bindings']==a['unit_bindings']and actualjob['body_correction_review']==a['body_correction_review']and actualjob['carried_legal_blockers']==a['carried_legal_blockers']and actualjob['reconsidered_legal_negatives']==a['reconsidered_legal_negatives'];notes=load_notes(R);committed_ledger=git(R,'show',head+':'+q.LEDGER);inv=q.inventory(R,notes=notes,ledger_raw=committed_ledger);q.current(a,inv,state);br.validate_registered(state,R,notes,inv=inv);checks+=['current_root_committed_registration_inventory_inactive_candidate_bridge_PASS']
 for path in [q.STATE,'scripts/note_review_queue.py','scripts/notes_body_reassessment.py',F+'registrations/after-census-v2.json',b['census_path'],a['body_correction_review']['revision']['path'],a['body_correction_review']['derived_preview']['path']]:assert git(R,'show',head+':'+path)==(R/path).read_bytes()
 checks+=['runtime_helper_and_immutable_inputs_equal_current_committed_root_bytes_explicit_committed_ledger_raw']
 vr=j(R/(F+'registrations/after-census-v2.json'));assert sha((R/(F+'registrations/after-census-v2.json')).read_bytes())==a['body_reassessment_record_sha256'];c=j(R/b['census_path']);assert len(c['claims'])==24 and sha((R/b['census_path']).read_bytes())==b['census_sha256'];assert all(q.digest(z)==b['claim_record_sha256s'][z['claim_id']]for z in c['claims']);candidate=j(R/a['body_correction_review']['revision']['path'])['units'][0];assert sha(candidate['body'].encode())==b['body_sha256'];active=br.units(notes);assert sha(active[uid]['body'].encode())!=b['body_sha256']
 archive=j(R/(F+'archive/old-effective-notes.json'));oldunits=br.units(archive);assert len(active)==len(oldunits)==306 and all(active[k]['body']==oldunits[k]['body']for k in active);checks+=['candidate24_census_claim_body_exact_hashes','all306_active_bodies_unchanged_candidate_not_active']
 for x in vr['archived_parent'].values():assert sha((R/x['path']).read_bytes())==x['raw_sha256']and git(R,'show',head+':'+x['path'])==(R/x['path']).read_bytes()
 oldc={z['claim_id']:z for z in j(R/(F+'archive/parent-census.json'))['claims']if z['unit_id']==uid};newc={z['claim_id']:z for z in c['claims']};assert len(oldc)==23 and len(newc)==24;assert set(vr['claim_mapping'])==set(oldc);assert sum(oldc[k]['statement_ko']==newc[k]['statement_ko']for k in oldc)==22
 result=oldunits[uid]['body']
 for span in vr['edit_spans']:
  assert sha(span['old_text'].encode())==span['old_text_sha256']and sha(span['new_text'].encode())==span['new_text_sha256'];assert result.count(span['old_text'])==1;result=result.replace(span['old_text'],span['new_text'])
 assert result==candidate['body'];assert br.derived_inputs(R,notes,uid,candidate)==j(R/a['body_correction_review']['derived_preview']['path'])['items'];checks+=['immutable_parent_census_report_result_and306body_snapshot','22_original_statements_preserved_actual_edit_span_reconstruction','actual_effective_derived_inputs_and_candidate_hashes_equal_registered_preview']
 for claim in row['claims']:
  cid=claim['claim_id'];assert claim['inherited_legal_blockers']==a['carried_legal_blockers'][uid].get(cid,[])
 held=next(z for z in row['claims']if z['claim_id'].endswith('-011'));assert held['legal_status']=='LEGAL_HOLD'and held['finding']==held['inherited_legal_blockers'][0]['finding']and held['blocker']==held['inherited_legal_blockers'][0]['blocker']
 for cid,neg in a['reconsidered_legal_negatives'][uid].items():
  claim=next(z for z in row['claims']if z['claim_id']==cid);assert claim['original_legal_negatives']==neg and claim['body_negative_reassessment']['decision']=='RESOLVED_BY_CHANGED_BODY_AND_PROPOSITION';assert claim['legal_status']=='KEEP'
 assert row['original_omission_reassessments']==[]and a['body_correction_review']['parent_omissions']==[];assert row['completeness']=='OMISSIONS_FOUND'and row['legal_status']=='LEGAL_HOLD'and len(row['omissions'])==1;assert row['new_omission_assessments'][0]['body_quote']in candidate['body'];checks+=['011_exact_mandatory_LEGAL_HOLD_carry','019_024_original_negatives_and_changed_statement_fresh_decisions','parent_omissions_empty_preserved_new_material_omission_exposed']
 for source in r['sources']:
  assert sha((W/source['evidence_path']).read_bytes())==source['evidence_sha256']==source['raw_sha256'];assert source['http_status']==200 and source['verification_status']=='OFFICIAL_DOCUMENT_TARGET_PROVISIONS_DIRECTLY_READ';assert q.instant(source['retrieved_at'])<=q.instant(source['read_at_utc'])<=q.instant(row['reviewed_at'])
 checks+=['all8_LIVE_official_raw_payload_hashes_and_actual_retrieval_read_review_order']
 inputs=j(W/(E+'questions-safe.json'));idx=j(W/(E+'questions-lossless.json'))
 def un(x):
  if isinstance(x,dict):return idx['texts'][x['text_ref']-1]if set(x)=={'text_ref'}else{k:un(v)for k,v in x.items()}
  if isinstance(x,list):return[un(v)for v in x]
  return x
 assert un(idx['records'])==[z['original_visible_content']for z in inputs['records']];assert len(inputs['records'])==37 and len(idx['texts'])==193 and sum(len(z['original_visible_content']['choices'])for z in inputs['records'])==159;banks={}
 for z in inputs['records']:
  path=z['collection'];qid=z['original_visible_content']['question_id']
  if path not in banks:
   x=json.loads(git(R,'show',inputs['source_root_head']+':'+path));banks[path]={x['question_id']:x}if'question_id'in x else{t['question_id']:t for t in x['questions']}
  original=banks[path][qid];assert q.digest(original)==z['whole_record_sha256']and{key:original[key]for key in z['original_visible_content']}==z['original_visible_content'];assert '_statement_truth'not in json.dumps(z['original_visible_content'])
 checks+=['37safe_originals_159choices_all_visible_fields_193string_lossless_reconstruction']
 if ar.write_envelope:Path('/tmp/w3-a-3-body-c-result.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
 if ar.postcommit:
  assert j(Path('/tmp/w3-a-3-body-c-result.json'))==m;q.committed_evidence(a,m,W)
  for source in r['sources']:assert sha(git(W,'show',m['worker_commit']+':'+source['evidence_path']))==source['raw_sha256']
  changed=git(W,'diff','--name-only',a['base_commit']+'..'+m['worker_commit']).decode().splitlines();assert changed and all(p.startswith(P+'body-v1-c-')for p in changed);assert not git(W,'status','--porcelain').strip();checks+=['current_root_native_committed_evidence_PASS','all8_sources_committed_exact_original_payload_bytes','whole_worker_commit_range_owned_prefix_only','worker_worktree_clean']
 out={'status':'PASS','current_root_native_helper_commit':head,'committed_ledger_raw_sha256':sha(committed_ledger),'ledger_runtime_mode':'git show current-root-HEAD:ledger passed directly to inventory(ledger_raw=...), never uncommitted generated ledger','worker_commit_checked':m['worker_commit'],'report_raw_sha256':m['evidence']['raw_sha256'],'postcommit':ar.postcommit,'checks':checks,'validation_is_not_legal_truth_or_release_credit':True}
 if ar.record:(W/(E+'precommit-validation.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(out,ensure_ascii=False))
if __name__=='__main__':main()
