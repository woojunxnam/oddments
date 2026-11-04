"""Real native validation and complete immutable preparation/source proofs."""
import json,subprocess,sys,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT/'scripts'))
import note_review_queue as q
import notes_census_reassessment as nr
P='reports/full-corpus-review/final19-census-author/w3-d-22-v2/'
BASE='e22b88e65b16b4336ad4c174a34300d354e095c3';DRAFT='80724326f8e9587b1a5ce6dab6898ffe88a1d3e0'
def blob(commit,path):return subprocess.check_output(['git','show',commit+':'+path],cwd=ROOT)
def write(path,obj):(ROOT/path).write_bytes(q.encoded(obj))
paths={}
def retain(path,sha=None):
 if path not in paths:
  head=blob('HEAD',path);dst=q.safe_path(ROOT,path)
  if not dst.exists():dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(head)
  assert dst.read_bytes()==head
  paths[path]=q.raw_sha(head)
 if sha:assert paths[path]==sha
 return (ROOT/path).read_bytes()
def authority_paths(obj):
 if isinstance(obj,list):
  for v in obj:authority_paths(v)
 elif isinstance(obj,dict):
  for k,v in obj.items():
   if k.endswith('_path')and isinstance(v,str)and obj.get(k[:-5]+'_sha256'):retain(v,obj[k[:-5]+'_sha256'])
   if k=='source_evidence'and isinstance(v,str)and obj.get('source_evidence_sha256'):retain(v,obj['source_evidence_sha256'])
   if isinstance(v,(list,dict)):authority_paths(v)
index=json.loads(retain(P+'final-proposal-index.json'));rec=json.loads(retain(index['record_path'],index['record_sha256']));state=json.loads(retain(q.STATE));assert blob(BASE,q.STATE)==(ROOT/q.STATE).read_bytes();q.validate_state(state)
invraw=Path('/workspace/scratch/notes-final19-verified-inventory.json').read_bytes();assert q.raw_sha(invraw)==index['full_native_inventory_raw_sha256'];inv=json.loads(invraw);notes=inv['notes'];ledger=retain(q.LEDGER,index['committed_selected_ledger_sha256'])
for b in inv['units'].values():retain(b['census_path'],b['census_sha256'])
actual=q.inventory(ROOT,notes,ledger_raw=ledger);assert actual['total_units']==306 and actual['units']==inv['units']and actual['ledger_sha256']==inv['ledger_sha256']
body={u['id']:u['body']for c in notes['chapters']for u in c['units']};assert len(body)==306
for uid,b in inv['units'].items():assert q.raw_sha(body[uid].encode())==b['body_sha256']
report=json.loads(retain(rec['previous_report']['path'],rec['previous_report']['raw_sha256']));job=next(j for j in state['jobs']if j['job_id']==rec['previous_job_id']);retain(rec['previous_result']['path'],rec['previous_result']['raw_sha256'])
for path,sha in q.validate_evidence(job,job['result'],report):retain(path,sha)
old=json.loads(retain(rec['previous_binding']['census_path'],rec['previous_binding']['census_sha256']));new=json.loads(retain(index['census_path'],index['census_sha256']));draft=json.loads(retain(P+'census.json'));assert len(old['claims'])==17 and len(new['claims'])==19 and new['claims']==draft['claims'] and new['sources']==draft['sources']
assert all(q.digest(a)==q.digest(b)for a,b in zip(old['claims'],new['claims']));assert all(q.digest(s)==q.digest(new['sources'][k])for k,s in old['sources'].items());assert rec['changed_claim_ids']==[]
assert retain(P+'body.txt')==body['w3-d-22'].encode()and q.raw_sha(body['w3-d-22'].encode())==rec['body_sha256']
authority_paths(new);authority_paths(report)
draftpaths=subprocess.check_output(['git','ls-tree','-r','--name-only',DRAFT,'--',P],cwd=ROOT,text=True).splitlines()
assert len(draftpaths)==16
for path in draftpaths:assert retain(path)==blob(DRAFT,path)
sourceproof=[]
for key,s in json.loads(retain(P+'retained-primary-source-manifest.json')).items():
 raw=retain(s['source_evidence'],s['source_evidence_sha256']);text=retain(s['text_evidence_path'],s['text_evidence_sha256']);meta_raw=retain(s['retrieval_metadata_path'],s['retrieval_metadata_sha256']);meta=json.loads(meta_raw)
 assert raw.startswith(b'%PDF-')and meta['raw_sha256']==q.raw_sha(raw)and meta['status_code']==200 and meta['valid_pdf'] is True
 extracted=subprocess.check_output(['pdftotext','-layout','-','-'],input=raw);assert extracted==text
 assert meta['requested_at_utc']<=meta['completed_at_utc']and meta['completed_at_utc'].startswith('2026-11-04')
 for suffix,current in [('.raw',raw),('.txt',text),('.meta.json',meta_raw)]:assert current==blob(s['retained_from_commit'],s['retained_original_base']+suffix)==retain(s['retained_original_base']+suffix)
 sourceproof.append({'source_key':key,'official_url':s['official_url'],'exact_section':s['exact_section'],'raw_sha256':q.raw_sha(raw),'text_sha256':q.raw_sha(text),'metadata_sha256':q.raw_sha(meta_raw),'original_get_started_at_utc':meta['requested_at_utc'],'original_get_completed_at_utc':meta['completed_at_utc'],'author_read_date':s['author_read_date'],'version_or_effective_date_status':s['version_or_effective_date_status'],'raw_pdf_extracted_text_equals_retained_text':True,'original_worker_commit_equals_own_head_equals_disk':True,'new_retrieval':False})
# Actual public API, unmodified disk_reader, committed replacement and real integrated parent.
binding,carried=nr.validate_record(state,rec,ROOT,notes,nr.disk_reader(ROOT));assert len(binding['claim_record_sha256s'])==19 and rec['author_provenance']['actor_id']in binding['known_author_ids']and carried=={}
originalrow=next(r for r in report['records']if r['unit_id']=='w3-d-22');assert len(originalrow['omissions'])==2 and all(q.raw_sha(o.encode())==r['omission_sha256']for o,r in zip(originalrow['omissions'],rec['omission_resolutions']))
assert rec['claim_mapping']=={c['claim_id']:[c['claim_id']]for c in old['claims']}
assert all(new['claims'][17+i]['claim_id']==r['claim_ids'][0]for i,r in enumerate(rec['omission_resolutions']))
changed=subprocess.check_output(['git','diff','--name-only',BASE,'HEAD'],cwd=ROOT,text=True).splitlines();assert changed and all(path.startswith(P)for path in changed)
assert subprocess.check_output(['git','diff','--name-only',DRAFT,'HEAD','--','reports/full-corpus-review/notes120-census-author/','reports/full-corpus-review/final86-census-author/'],cwd=ROOT)==b''
head=q.git(ROOT,'rev-parse','HEAD');at=datetime.datetime.now(datetime.timezone.utc).isoformat()
write(P+'native-final-validation.json',{'validated_at_utc':at,'validation_head':head,'isolated_root_state_commit':BASE,'native_validate_record':'PASSED','real_disk_reader_used':True,'strict_notes_input_raw_sha256':q.raw_sha(invraw),'selected_ledger_sha256':q.raw_sha(ledger),'full306_native_inventory_recomputed':True,'all306_body_hashes_reconfirmed':True,'validation_context_ko':'root의 실제 strict notes 전체306개를 exactSHA로 읽고 own committed ledger/census 전체로 q.inventory를 재실행했다. 별도 load_notes 재실행이나 임의 projection/가짜 ledger/guard완화 없이 공식 validate_record API의 명시 notes 인자를 사용했다. disk_reader는 격리된 이 작업트리 HEAD 바이트만 읽었다.','replacement_binding':binding,'carried_legal_blockers':carried,'original_author_exclusion_ids':rec['previous_binding']['known_author_ids'],'expected_registration_exclusion_union':sorted(set(job['known_author_ids'])|set(rec['previous_binding']['known_author_ids'])|set(binding['known_author_ids'])),'controller_registration_performed':False,'canonical_release_credit':0,'question_audit_credit':0,'independent_audit_credit':0})
write(P+'final-preservation-and-source-proof.json',{'validated_at_utc':at,'validation_head':head,'root_integration_state_commit':BASE,'all17_claims_canonical_preserved':True,'all_original_sources_canonical_preserved':True,'original_claim_sha256s':{c['claim_id']:q.digest(c)for c in old['claims']},'original_source_sha256s':{k:q.digest(s)for k,s in old['sources'].items()},'body_bytes_preserved':True,'body_sha256':rec['body_sha256'],'original_claim_count':17,'final_claim_count':19,'added_claim_count':2,'added_author_source_checked_count':2,'changed_claim_ids':[],'old807_all16_preparation_files_byte_immutable':True,'old_notes120_and_final86_prefixes_byte_immutable':True,'all_reference_head_equals_disk':True,'reference_count':len(paths),'reference_path_sha256s':paths,'source_pdf_text_metadata_checks':sourceproof,'exact_two_omission_sha_bindings':True,'authored_paths_from_root_base':changed,'all_authored_paths_in_unique_prefix':True,'queue_ledger_original_census_report_body_generated_guard_mutations':0,'controller_registration_performed':False,'independent_credit':0,'release_credit':0})
print(json.dumps({'native':'PASSED','original17':'canonical preserved','final19':True,'source_pdf_text_meta':'PASSED','references_head_equals_disk':len(paths),'old807_all16_immutable':True,'registration':False},ensure_ascii=False))
