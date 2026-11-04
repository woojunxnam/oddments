import pathlib,json,hashlib,subprocess,sys,datetime,collections,urllib.parse
R=pathlib.Path('/workspace/sata-current-id-author-g');ROOT=pathlib.Path('/workspace/oddments');P=R/'reports/full-corpus-review/sata-remediation-current-id-author';E=P/'evidence';RP=P/'g-review.json';A=json.load(open('/tmp/sata-current-id-author-g-assignment.json'));V=json.load(open('/tmp/sata-current-id-author-g-visible.json'));report=json.load(open(RP));actor={'actor_id':'/root/independent_case_g','session_id':'/root/independent_case_g','stable_instance':'gpt-independent-phase3-g-root-independent_case_g-20261103'}
def sha(b):return hashlib.sha256(b).hexdigest()
def digest(x):return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def git(*args):return subprocess.check_output(['git','-C',str(R),*args])
sys.path.insert(0,str(ROOT/'scripts'));import remediation_author_reviews as native;import build_full_corpus_review as full;import review_queue
bankrel='practice_expansion/2026-10-28-representative/questions.json'
def load_assigned(root):return {q['question_id']:q for q in json.load(open(root/bankrel))['questions'] if q['question_id'] in A['question_hashes']}
questions=load_assigned(R);current_root=load_assigned(ROOT)
assert set(questions)=={'MA-RW-0081','MA-RW-0082','MA-RW-0083'} and {k:digest(v) for k,v in questions.items()}==A['question_hashes']=={k:digest(v) for k,v in current_root.items()}
assert native.expected_actor(questions)==actor==report['actor_provenance'] and A['required_author_actor_id']==actor['actor_id']
assert report['question_hashes']==A['question_hashes'] and report['job_id']==A['job_id'] and report['stage']=='author' and report['schema_version']==native.SCHEMA
assert report['canonical_audit'] is False and report['canonical_release_credit']==report['independent_review_credit']==report['author_review_credit_before_root_integration']==0 and report['independent_of_authors'] is False
assert 'worker_commit' not in report and not any(k in report for k in ['report_sha256','self_sha256'])
assert report['input_contract']['assignment_raw_sha256']==sha(pathlib.Path('/tmp/sata-current-id-author-g-assignment.json').read_bytes())
assert sha((R/report['input_contract']['safe_visible_input_path']).read_bytes())==report['input_contract']['safe_visible_input_sha256']
assert sha((R/report['input_contract']['direct_read_history_path']).read_bytes())==report['input_contract']['direct_read_history_sha256']
assert sha((R/report['input_contract']['native_author_contract_path']).read_bytes())==report['input_contract']['native_author_contract_sha256']
for q in V:
 src=questions[q['question_id']]
 assert all(q[k]==src[k] for k in ['question_id','question_type','stem','choices','correct_choice_ids','explanation'])
assert len(report['records'])==3 and sum(len(x['choice_by_choice_findings']) for x in report['records'])==14
count=0;source_ids=set()
for row in report['records']:
 q=questions[row['question_id']];full.validate_review(q,row)
 assert row['current_ID_stem_all_choices_key_all_Korean_explanations_read'] and row['reviewer_provenance']['independent'] is False
 assert all(row['reviewer_provenance'][k]==v for k,v in actor.items())
 assert row['record_sha256']==A['question_hashes'][q['question_id']]
 assert row['checked_at'].startswith('2026-11-04') and row['disposition']=='KEEP' and row['blocker'] is None
 assert row['legal_review_status']=='AUTHOR_SOURCE_CHECKED_NOT_INDEPENDENT'
 truth=[]
 for c in q['choices']:
  count+=1;f=row['choice_by_choice_findings'][c['id']];assert f['original_choice_text']==c['text'] and f['original_choice_text_sha256']==sha(c['text'].encode())
  assert type(f['expected_true']) is bool and f['finding_ko'] and f['exact_authority'] and f['authorities']
  assert f['original_korean_rationale_read'] and f['original_korean_rationale_sha256']==sha(q['explanation']['choice_analysis'][c['id']].encode())
  assert f['rationale_assessment']=='SUPPORTED_IN_EXPLICIT_STEM_SCOPE'
  if f['expected_true']:truth.append(c['id'])
  for a in f['authorities']:
   source_ids.add(a['source_id']);assert a['official_url'].startswith('https://') and urllib.parse.urlparse(a['official_url']).hostname=='www.mass.gov'
   assert a['exact_section'] and a['law_checked_date']=='2026-11-04' and a['version_or_effective_date_status']
   assert a['body_verified_current_primary'] is True and a['used_as_legal_proof'] is True and a['http_status']==200
   assert sha((R/a['raw_path']).read_bytes())==a['raw_sha256'] and sha((R/a['retrieval_metadata_path']).read_bytes())==a['retrieval_metadata_sha256']
   m=json.load(open(R/a['retrieval_metadata_path']));assert m['official_url']==a['official_url'] and m['raw_sha256']==a['raw_sha256'] and m['http_status']==200
   assert m['retrieved_at'].startswith('2026-11-04') and m['tls_verification'] and m['retrieval_method']=='LIVE_OFFICIAL_HTTPS_urllib'
   assert m['body_verified_current_primary'] is True and m['used_as_legal_proof'] is True
 assert truth==row['author_expected_choice_ids']==q['correct_choice_ids'] and 2<=len(truth)<len(q['choices'])
 ex=row['explanation_review'];assert ex['full_core_read'] and ex['all_korean_choice_rationales_read'] and ex['rationale_count']==len(q['choices'])
 assert ex['core_sha256']==sha(q['explanation']['core_reasoning'].encode()) and ex['learning_boundary_sha256']==sha(q['explanation']['learning_boundary'].encode())
 assert row['bounded_style_and_logic_check']['mixed_correct_incorrect'] and row['bounded_style_and_logic_check']['at_least_two_correct']
assert count==14 and source_ids=={'admin','intern','ec','ec-order'}
assert sha((R/report['source_register_path']).read_bytes())==report['source_register_sha256']
reg=json.load(open(R/report['source_register_path']));assert reg['failed_payload_as_verified_proof']==reg['source_access_blockers']==0
for ex in reg['excluded_attempts']:
 assert ex['used_as_legal_proof'] is False and sha((R/ex['metadata_path']).read_bytes())==ex['metadata_sha256']
 m=json.load(open(R/ex['metadata_path']));assert m['used_as_legal_proof'] is False and sha((R/m['raw_path']).read_bytes())==m['raw_sha256']
out={'stage':'author','job_id':A['job_id'],'question_hashes':A['question_hashes'],'worker_commit':git('rev-parse','HEAD').decode().strip(),'actor_provenance':actor,'canonical_audit':False,'canonical_release_credit':0,'independent_of_authors':False,'independent_review_credit':0,'results':[{'question_id':r['question_id'],'disposition':'AUTHOR_REVIEWED' if r['disposition']=='KEEP' else r['disposition'],'evidence_path':str(RP.relative_to(R)),'evidence_sha256':sha(RP.read_bytes())} for r in report['records']]}
review_queue.validate_result(A,out);native.validate_submission(A,out)
native_head_status='NOT_RUN_PRECOMMIT_REQUIRES_RETAINED_HEAD_SOURCE_BYTES'
if '--postcommit' in sys.argv:
 assert git('show','HEAD:'+str(RP.relative_to(R)))==RP.read_bytes()
 for f in E.rglob('*'):
  if f.is_file():assert git('show','HEAD:'+str(f.relative_to(R)))==f.read_bytes()
 native.validate_report(R,A,out,RP.read_bytes(),questions);native_head_status='PASS_REAL_CURRENT_HEAD_RETAINED_BYTES'
 assert not git('status','--porcelain')
 pathlib.Path('/tmp/sata-current-id-author-g-result.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
summary={'status':'PASS','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'current_worker_and_root_whole_record_hashes':3,'complete_current_visible_objects_match':3,'choices_and_korean_rationales':14,'fresh_current_official_sources':4,'mixed_SATA_expected_sets':{x['question_id']:x['author_expected_choice_ids'] for x in report['records']},'existing_validate_review':'PASS3','native_validate_submission':'PASS','review_queue_validate_result':'PASS','native_validate_report_HEAD':native_head_status,'dispositions':{'AUTHOR_REVIEWED':3},'body_key_source_metadata_draft_changes':0,'independent_credit':0,'canonical_release_credit':0,'credit_before_root_registry_and_integration':0,'report_sha256':sha(RP.read_bytes()),'worker_commit':out['worker_commit'],'envelope_written':'--postcommit' in sys.argv,'root_submit_integrate_registry':'NOT_RUN_ROOT_ONLY'}
print(json.dumps(summary,ensure_ascii=False,indent=2))
