from pathlib import Path
import json,hashlib,subprocess,datetime
R=Path('/workspace/oddments');S=Path('/workspace/scratch');EXPECTED='4b5371b3bdafcaf8e2f6773fe44454e0cc934494';H=lambda b:hashlib.sha256(b).hexdigest();canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def git(*a):return subprocess.check_output(['git','-C',str(R),*a],text=True).strip()
def read(p):
 b=(R/p).read_bytes();assert b==subprocess.check_output(['git','-C',str(R),'show',EXPECTED+':'+p]);return b
assert git('rev-parse','HEAD')==EXPECTED and not git('status','--porcelain','--untracked-files=no')
rows=[json.loads(x)for x in read('reports/full-corpus-review/question-ledger.jsonl').decode().splitlines()];assert len(rows)==2349;collections={};objects={};keys={}
for row in rows:
 p=row['collection']
 if p not in collections:
  raw=read(p);data=json.loads(raw);collections[p]={'sha256':H(raw),'questions':{q['question_id']:q for q in data['questions']}if'questions'in data else{data['question_id']:data}}
 q=collections[p]['questions'][row['question_id']];assert H(canon(q))==row['content_sha256'];objects[row['question_id']]=H(canon(q));keys[row['question_id']]=q['correct_choice_ids']
assert len(collections)==4
state_paths=['reports/full-corpus-review/independent-notes-work-queue.json','reports/full-corpus-review/remaining9-procedural-work-queue.json','reports/full-corpus-review/source3-recovered-legal-work-queue.json'];states={p:H(read(p))for p in state_paths};all_source_paths=set(state_paths)
for p in state_paths:
 state=json.loads(read(p));assert all(j['status']=='INTEGRATED'for j in state['jobs'])
 for j in state['jobs']:
  result=j['result'];sources=[result.get('evidence',{}).get('path')]+[x.get('evidence_path')for x in result.get('results',[])]+[result.get('result_path')]
  for path in sources:
   if path and(R/path).is_file():all_source_paths.add(path)
source_history={p:H(read(p))for p in sorted(all_source_paths)}
selection_path='practice_expansion/2026-10-28-representative/selection.json';selraw=read(selection_path);selection=json.loads(selraw);assert len(selection['recommended_ids'])==202
archive='reports/representative-rewrite/archive-review-notices.json';archive_raw=read(archive);archive_obj=json.loads(archive_raw);old790=next(x for x in rows if x['question_id']=='MA-CASE-0790');negative_fields={k:old790[k]for k in ['disposition','blocker','author_disposition','independent_legacy_legal_assessment','independent_legacy_realism_assessment','independent_legacy_realism_supplementary_assessment']if k in old790}
units=[json.loads(x)for x in read('reports/full-corpus-review/notes-unit-ledger.jsonl').decode().splitlines()];body_sha={u['unit_id']:u['actual_effective_body_sha256']for u in units};assert len(body_sha)==306
payloadraw=read('site/notes/content.js');payload=json.loads(payloadraw.decode().split('window.MPJE_NOTES = ',1)[1].rsplit(';',1)[0]);body_fields={u['id']:{k:u[k]for k in('id','title','body','html','text','body_sha256')if k in u}for c in payload['chapters']for u in c['units']};assert len(body_fields)==306
baseline={'source_head':EXPECTED,'question_objects':objects,'question_keys':keys,'four_collection_raw_sha256s':{p:v['sha256']for p,v in collections.items()},'source_native_states':states,'source_native_reports_results_history_raw_sha256s':source_history,'selection_path':selection_path,'selection_raw_sha256':H(selraw),'ordered202_default_ids':selection['recommended_ids'],'archive_notices_path':archive,'archive_notices_raw_sha256':H(archive_raw),'case790_archive_notices':[x for x in archive_obj['notices']if'MA-CASE-0790'in x['question_ids']],'case790_selected_notices':[x for x in selection['archive_review_notices']if'MA-CASE-0790'in x['question_ids']],'case790_negative_fields':negative_fields,'all306_actual_effective_body_sha256s':body_sha,'published_payload306_body_fields':body_fields,'source_input_sha256s':{p:H(read(p))for p in ['notes/guide.json','notes/study/guide.json','notes/refresh/guide.json','revisions/notes/held-n1-activation.json','revisions/notes/protected-migration-held-n1.json','docs/RELEASE_POLICY.md','docs/AUDIT_WORKFLOW.md','docs/SOURCE_USE_POLICY.md','docs/QUESTION_AUTHORING_STANDARD.md']}}
(S/'final-source3-generation-baseline.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2)+'\n')
log=S/'final-source3-actual-full-corpus.log';started=datetime.datetime.now(datetime.timezone.utc).isoformat()
with log.open('wb')as f:res=subprocess.run(['/workspace/mpje-venv/bin/python','scripts/build_full_corpus_review.py'],cwd=R,stdout=f,stderr=subprocess.STDOUT)
receipt={'source_head':EXPECTED,'command':['/workspace/mpje-venv/bin/python','scripts/build_full_corpus_review.py'],'cwd':str(R),'started_at':started,'completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit_code':res.returncode,'regular_full_producer_attempts':1,'log_path':str(log),'log_sha256':H(log.read_bytes()),'new_canonical_release_credit':0};(S/'final-source3-actual-full-corpus-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt),flush=True)
if res.returncode:raise SystemExit(res.returncode)
assert git('rev-parse','HEAD')==EXPECTED
for p,v in collections.items():assert H((R/p).read_bytes())==v['sha256']
for p,sha in {**states,**source_history,**baseline['source_input_sha256s']}.items():assert H((R/p).read_bytes())==sha
assert(R/selection_path).read_bytes()==selraw and(R/archive).read_bytes()==archive_raw
newrows=[json.loads(x)for x in(R/'reports/full-corpus-review/question-ledger.jsonl').read_text().splitlines()];assert{r['question_id']:r['content_sha256']for r in newrows}==objects
new790=next(r for r in newrows if r['question_id']=='MA-CASE-0790');assert all(new790[k]==v for k,v in negative_fields.items())
p=json.loads((R/'reports/full-corpus-review/progress.json').read_bytes());nu=[json.loads(x)for x in(R/'reports/full-corpus-review/notes-unit-ledger.jsonl').read_text().splitlines()];assert len(nu)==306 and sum(len(r['atomic_claim_ids'])for r in nu)==p['atomic_claims_enumerated']==7086 and {r['unit_id']:r['actual_effective_body_sha256']for r in nu}==body_sha
proof={**receipt,'actual_progress':p,'all2349_source_objects_keys_and_IDs_unchanged':True,'four_bank_entire_bytes_unchanged':True,'bank77_raw_sha256':baseline['four_collection_raw_sha256s']['practice_expansion/2026-10-28-representative/questions.json'],'ordered202_defaults_unchanged':True,'all306_current_body_hashes_unchanged':True,'CASE790_primary_realism_legal_negative_fields_unchanged':True,'CASE790_both_notice_sources_previous_notices_and_history_unchanged':True,'all_source82_Q9_Q3_states_reports_result_history_bytes_unchanged':True,'new_canonical_release_credit':0,'actual_changed_paths':git('diff','--name-only').splitlines()};(S/'final-source3-full-corpus-output-verification.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'phase':'ACTUAL_FULL_OUTPUT_VERIFIED','key_assessed':p['independent_legacy_legal_assessed'],'key_unassessed':p['independent_legacy_keys_unassessed'],'realism_pass':p['independent_legacy_realism_pass'],'notes':p['independent_note_completeness_legal_review'],'actual_changed_paths':proof['actual_changed_paths']},ensure_ascii=False),flush=True)
