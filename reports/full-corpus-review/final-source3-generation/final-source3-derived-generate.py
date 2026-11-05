from pathlib import Path
import json,hashlib,subprocess,datetime,shutil,sys
R=Path('/workspace/oddments');S=Path('/workspace/scratch');E=R/'reports/full-corpus-review/final-source3-generation';E.mkdir(exist_ok=True)
H=lambda b:hashlib.sha256(b).hexdigest();B=json.loads((S/'final-source3-generation-baseline.json').read_text());canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def git(*a):return subprocess.check_output(['git','-C',str(R),*a],text=True).strip()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def payload(path,prefix):return json.loads((R/path).read_text().split(prefix,1)[1].rsplit(';',1)[0])
def protected():
 for k in ['four_collection_raw_sha256s','source_native_states','source_native_reports_results_history_raw_sha256s','source_input_sha256s','daily_selector_code_sha256s']:
  for p,sha in B[k].items():assert H((R/p).read_bytes())==sha,(k,p)
 assert H((R/B['selection_path']).read_bytes())==B['selection_raw_sha256']
 assert H((R/B['archive_notices_path']).read_bytes())==B['archive_notices_raw_sha256']
 rows=[json.loads(x)for x in(R/'reports/full-corpus-review/question-ledger.jsonl').read_text().splitlines()]
 assert {x['question_id']:x['content_sha256']for x in rows}==B['question_objects']
 x=next(x for x in rows if x['question_id']=='MA-CASE-0790');assert all(x[k]==v for k,v in B['case790_negative_fields'].items())
 units=[json.loads(x)for x in(R/'reports/full-corpus-review/notes-unit-ledger.jsonl').read_text().splitlines()]
 assert {x['unit_id']:x['actual_effective_body_sha256']for x in units}==B['all306_actual_effective_body_sha256s']
 assert len(units)==306 and sum(len(x['atomic_claim_ids'])for x in units)==7086
 return rows

def commit(stage,allowed,proof,files):
 changed=git('diff','--name-only').splitlines();assert set(changed)<=set(allowed),(stage,changed)
 assert not git('diff','--cached','--name-only')
 for name in files:shutil.copyfile(S/name,E/name)
 dump(E/(stage+'-verification.json'),proof)
 subprocess.run(['git','add','--',*changed,str(E.relative_to(R))],cwd=R,check=True)
 subprocess.run(['git','commit','-m','Preserve actual source3 '+stage+' generation and safety evidence'],cwd=R,check=True)
 print(json.dumps({'phase':stage,'commit':git('rev-parse','HEAD'),'changed_generated':changed}),flush=True)

rows=protected();assert git('rev-parse','HEAD')==B['source_head']
p=json.loads((R/'reports/full-corpus-review/progress.json').read_text());excluded=set(p['independent_legacy_context38_supplementary_review']['excluded_context_conditioned_primary_key_ids'])
primary={r['question_id']for r in rows if r.get('independent_legacy_legal_assessment',{}).get('existing_answer_correct','NOT_ASSESSED')!='NOT_ASSESSED'}-excluded
supp={r['question_id']for r in rows if r.get('independent_legacy_supplementary_assessment',{}).get('record',{}).get('legal_review',{}).get('existing_answer_correct','NOT_ASSESSED')!='NOT_ASSESSED'}
assert len(primary|supp)==p['independent_legacy_legal_assessed']==2312 and 2349-len(primary|supp)==p['independent_legacy_keys_unassessed']==37
old=[json.loads(x)for x in subprocess.check_output(['git','show',B['source_head']+':reports/full-corpus-review/question-ledger.jsonl'],cwd=R,text=True).splitlines()]
oldmap={r['question_id']:r for r in old};changes=[r['question_id']for r in rows if r!=oldmap[r['question_id']]]
assert set(changes)=={'MA-CASE-0785','MA-CASE-0786','MA-CASE-0790'}
for r in rows:
 if r['question_id']in changes:
  x=dict(r);x.pop('independent_legacy_supplementary_assessment');assert x==oldmap[r['question_id']]
proof={'source_head':B['source_head'],'primary_after_context_exclusion_count':len(primary),'supplementary_assessed_unique_count':len(supp),'effective_unique_union':len(primary|supp),'effective_unassessed':37,'changed_ledger_row_ids':changes,'only_added_current_source3_legal_supplementary_metadata':True,'all_original_primary_fields_exactly_preserved':True,'realism_effective_unchanged':p['independent_legacy_realism_pass'],'all2349_source_objects_keys_IDs_unchanged':True,'all306_body_records_7086_claims_unchanged':True,'source82_Q9_Q3_reports_results_and_states_exact':True,'CASE790_negative_and_both_notice_histories_exact':True,'new_canonical_or_person_or_question_read_credit':0,'old_final16_manifest_pending_root_regeneration':True}
commit('full-corpus',['reports/full-corpus-review/progress.json','reports/full-corpus-review/question-ledger.jsonl'],proof,['final-source3-generation-baseline.json','final-source3-actual-full-corpus.log','final-source3-actual-full-corpus-receipt.json','final-source3-full-corpus-output-verification.json','final-source3-full-corpus-generate.py'])

stages=[('notes','scripts/build_ultimate_notes.py',['site/notes/content.js','site/notes/book.html','site/notes/complete-notes.md','site/notes/build.json']),('study','scripts/build_exam_study.py',['site/notes/study-data.js','site/notes/study-build.json','site/notes/study.html']),('refresh','scripts/build_refresh.py',['site/notes/refresh-data.js','site/notes/refresh-build.json'])]
for stage,script,allowed in stages:
 assert not git('status','--porcelain');head=git('rev-parse','HEAD');log=S/('final-source3-actual-'+stage+'.log');start=datetime.datetime.now(datetime.timezone.utc)
 print(json.dumps({'phase':stage,'source_head':head,'started_at':start.isoformat()}),flush=True)
 with log.open('wb')as f:res=subprocess.run(['/workspace/mpje-venv/bin/python',script],cwd=R,stdout=f,stderr=subprocess.STDOUT)
 end=datetime.datetime.now(datetime.timezone.utc);receipt={'source_head':head,'command':['/workspace/mpje-venv/bin/python',script],'cwd':str(R),'started_at':start.isoformat(),'completed_at':end.isoformat(),'wall_seconds':(end-start).total_seconds(),'exit_code':res.returncode,'log_path':str(log),'log_sha256':H(log.read_bytes()),'attempt':1,'new_canonical_release_or_qa_credit':0}
 receipt_path=S/('final-source3-actual-'+stage+'-receipt.json');dump(receipt_path,receipt);print(json.dumps(receipt),flush=True)
 if res.returncode:
  shutil.copyfile(log,E/log.name);shutil.copyfile(receipt_path,E/receipt_path.name)
  print('SOURCE_GUARD_OR_BUILD_FAILURE_PRESERVED_NO_BYPASS',flush=True);sys.exit(res.returncode)
 assert git('rev-parse','HEAD')==head;protected()
 notes=payload('site/notes/content.js','window.MPJE_NOTES = ');units=[u for c in notes['chapters']for u in c['units']]
 fields={u['id']:{k:u[k]for k in('id','title','body','html','text','body_sha256')if k in u}for u in units};assert fields==B['published_payload306_body_fields']
 n1=next(u for u in units if u['id']=='w3-a-3');n=n1['independent_atomic_census_review'];assert n['requires_review']and n['legal_status']=='LEGAL_HOLD'and n['notice'];assert n1['atomic_source_review']['count']>0
 proof={'source_head':head,'exit_code':0,'all306_semantic_bodies_html_text_titles_exact':True,'other305_body_records_exact':True,'active_N1_w3_a_3_LEGAL_HOLD_requires_review_and_notice':True,'original011_annotation_and_native_reports_exact':True,'source82_Q9_Q3_and_question2349_bytes_keys_history_exact':True,'ordered202_default_and_bank77_and_notice_histories_exact':True,'daily_selector_code_unchanged':True,'old_final16_manifest_pending_root_regeneration':True,'full_qa_or_release_credit':0}
 if stage in('study','refresh'):
  data=payload('site/notes/study-data.js','window.MPJE_EXAM_STUDY = ');assert[x['id']for x in data['lessons']]==B['derived_history_ids_before_regeneration']['study_lesson_ids'];assert[x['id']for x in data['modules']]==B['derived_history_ids_before_regeneration']['study_module_ids']
  related=[x for x in data['lessons']if'w3-a-3'in x['note_units']];assert related
  for x in related:assert any(z['unit_id']=='w3-a-3'and z['legal_status']=='LEGAL_HOLD'and z['notice']for z in x['independent_atomic_census_reviews'])
  proof['study_history_lesson64_module16_ID_order_exact']=True;proof['N1_study_lesson_ids_with_review_notice_and_daily_exclusion']=[x['id']for x in related]
 if stage=='refresh':
  data=payload('site/notes/refresh-data.js','window.MPJE_REFRESH = ');assert[x['id']for x in data['cards']]==B['derived_history_ids_before_regeneration']['refresh_card_ids']
  related=[x for x in data['cards']if'w3-a-3'in x['note_units']];assert related
  for x in related:assert any(z['unit_id']=='w3-a-3'and z['legal_status']=='LEGAL_HOLD'and z['notice']for z in x['independent_atomic_census_reviews'])
  js="const fs=require('fs'),C=require('./site/notes/refresh-core.js'),d=JSON.parse(fs.readFileSync(process.argv[1],'utf8'));const day=C.dayKey();process.stdout.write(JSON.stringify({day,ids:C.dailyCards(d.cards,{},day)}));"
  fp=S/'final-source3-refresh-actual-payload.json';dump(fp,data);result=json.loads(subprocess.check_output(['node','-e',js,str(fp)],cwd=R,text=True));assert not(set(result['ids'])&{x['id']for x in related})
  proof['refresh_card232_history_ID_order_exact']=True;proof['N1_refresh_card_ids_with_review_notice']=[x['id']for x in related];proof['actual_existing_refresh_pure_daily_selector_result']=result;proof['N1_daily_selected_count']=0
 commit(stage,allowed,proof,[log.name,receipt_path.name])
assert not git('status','--porcelain');print(json.dumps({'phase':'ALL_GENERATORS_COMPLETED','head':git('rev-parse','HEAD')}),flush=True)
