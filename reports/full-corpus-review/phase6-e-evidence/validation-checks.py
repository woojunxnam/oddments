import json,pathlib,hashlib,sys,datetime,subprocess,collections,copy
w=pathlib.Path('/workspace/independent-phase6-e'); ctl=pathlib.Path('/workspace/oddments'); rel='reports/full-corpus-review/independent-phase6-e-review.json'; pre='reports/full-corpus-review/phase6-e-evidence'; e=w/pre
sys.path.insert(0,str(ctl/'scripts'));import review_queue as rq;import export_legacy_review_input as exporter
sha=lambda b:hashlib.sha256(b).hexdigest(); load=lambda p:json.loads(p.read_text())
job=load(pathlib.Path('/tmp/independent-phase6-e-assignment.json')); report=load(w/rel); packet=load(e/'original-visible-input.json'); expected_ids={f'MA-CASE-{n:04}' for n in range(881,921)}
assert set(job['question_hashes'])==expected_ids
assert packet==exporter.export(job,root=w)
assert packet==exporter.export(job,root=ctl)
assert set(r['question_id'] for r in report['records'])==expected_ids and len(report['records'])==40
assert report['stage']=='independent-legacy' and report['job_id']==job['job_id']
assert report['actor_provenance']=={'actor_id':'/root/independent_case_e','session_id':'/root/independent_case_e'}
assert report['auditor']=='GPT' and report['auditor_instance']=='gpt-independent-session-root-independent_case_e-20261103'
assert report['canonical_audit'] is False and report['canonical_release_credit']==report['author_review_credit']==report['canonical_question_audit_credit']==0
assert report['reviewed_at']==datetime.datetime.now(datetime.timezone.utc).date().isoformat()=='2026-11-04'
assert report['provenance']['input_packet_raw_sha256']==sha((e/'original-visible-input.json').read_bytes())
# Exact string deduplication is lossless and no shorter paraphrases replace the read input.
def deref(x,catalog):
 if isinstance(x,dict):
  if set(x)=={'text_ref'}:return catalog[x['text_ref']]
  return {k:deref(v,catalog) for k,v in x.items()}
 if isinstance(x,list):return [deref(v,catalog) for v in x]
 return x
cat=load(e/'exact-visible-text-catalog.json'); originals={r['question_id']:r for r in packet['records']}; assert len(cat['catalog'])==275
for m in cat['question_maps']:assert deref(m['content_refs'],cat['catalog'])==originals[m['question_id']]['original_visible_content']
assert len(cat['question_maps'])==40
source_by={s['source_id']:s for s in report['sources']};assert len(source_by)==35
for s in report['sources']:
 assert s['official_url'].startswith('https://') and s['retrieved_at_utc'].startswith('2026-11-04')
 assert sha((w/s['raw_path']).read_bytes())==s['raw_sha256']
 if s['used_as_law']:
  assert s['http_status']==200 and s['evidence_status']=='DIRECT_CURRENT_PRIMARY_SECTION_READ'
  assert s['law_checked_date']=='2026-11-04' and s['exact_section'] and s['version_or_effective_date_status']
  if s['raw_path'].endswith('.pdf'):assert (w/s['raw_path']).read_bytes().startswith(b'%PDF')
 else:assert s['source_id'] in {'112-24Bhalf','94c-19B','nabp-live'}
assert sum(s['used_as_law'] for s in report['sources'])==32
assert source_by['112-24Bhalf']['http_status']==404 and source_by['nabp-live']['http_status']==403
criteria_names={'jurisprudence_reasoning','practice_plausibility','authentic_distractors','wording_not_guessable','reasoning_not_trivia','natural_rule_combination','appropriate_drug_context','distinct_from_bank','not_schedule_flashcard','public_style_without_copying'}
for r in report['records']:
 q=originals[r['question_id']]['original_visible_content'];l=r['legal_review'];rr=r['realism_review']
 assert r['record_sha256']==job['question_hashes'][r['question_id']]
 assert r['visible_content_sha256']==rq.digest(q)
 assert r['release_eligible'] is False
 assert all(r['read_scope'][k] is True for k in ['original_full_stem','all_options','stored_key','korean_core','all_korean_distractors','learning_boundary'])
 assert r['read_scope']['option_count']==5
 assert len(l['per_choice_findings'])==5 and l['stored_key']==q['correct_choice_ids']
 independently_expected=[]
 for qc,c in zip(q['choices'],l['per_choice_findings']):
  assert (qc['id'],qc['text'])==(c['choice_id'],c['option_text'])
  assert sha(c['option_text'].encode())==c['option_sha256']
  assert isinstance(c['is_supported'],bool) and c['finding_ko'] and c['authorities']
  if c['is_supported']:independently_expected.append(c['choice_id'])
  for a in c['authorities']:
   s=source_by[a['authority']];assert s['used_as_law'] and s['http_status']==200
   assert a['official_url']==s['official_url'] and a['evidence_path']==s['raw_path'] and a['evidence_sha256']==s['raw_sha256']
   assert a['exact_section'] and a['law_checked_date']=='2026-11-04' and a['version_or_effective_date_status']
   assert sha((w/a['evidence_path']).read_bytes())==a['evidence_sha256']
 assert independently_expected==l['independently_expected_key']==l['stored_key']
 assert l['existing_answer_correct']=='YES' and l['verdict']=='KEEP' and l['blocker'] is None
 er=l['original_explanation_review'];assert er['distractor_count']==len(er['per_choice_findings'])==5
 assert er['core_reasoning_read_completely'] and er['all_distractor_explanations_read_completely'] and er['learning_boundary_read_completely']
 assert set(rr['criteria'])==set(rr['criterion_findings_ko'])==criteria_names
 assert all(type(v)==bool for v in rr['criteria'].values()) and all(rr['criterion_findings_ko'].values())
 assert (rr['verdict']=='PASS')==all(rr['criteria'].values())
 assert rr['duplicate_evidence']['nearest_original_full_stems_all_choices_read'] is True
 nd=rr['duplicate_evidence'];assert sha((w/nd['evidence_path']).read_bytes())==nd['evidence_sha256']
 assert r['disposition']==('INDEPENDENT_ASSESSED' if rr['verdict']=='PASS' else 'NEEDS_REMEDIATION')
 assert r['safe_hold_recommended']==(rr['verdict']=='FAIL')
assert collections.Counter(r['realism_review']['verdict'] for r in report['records'])=={'PASS':3,'FAIL':37}
# Re-bind actual original nearest stems and every option, and the real corpus bytes.
dup=load(e/'duplicate-comparison.json');assert dup['canonical_count']==439 and dup['public_count']==2346
original_near={}
for c in dup['public_collections']:
 assert sha((w/c['path']).read_bytes())==c['sha256']
 for q in load(w/c['path'])['questions']:original_near[q['question_id']]={'question_id':q['question_id'],'stem':q['stem'],'choices':q['choices']}
canon=load(e/'canonical-corpus-file-bindings.json');assert len(canon['files'])==439
for c in canon['files']:
 assert sha((w/c['path']).read_bytes())==c['raw_sha256']
 q=load(w/c['path']);original_near[q['question_id']]={'question_id':q['question_id'],'stem':q['stem'],'choices':q['choices']}
assert len(original_near)==439+2346
snapshots={q['question_id']:q for q in dup['nearest_full_text_snapshots']};assert len(snapshots)==97
for q in snapshots.values():assert q==original_near[q['question_id']]
nearcat=load(e/'nearest-exact-text-catalog.json');assert len(nearcat['catalog'])==392
assert len(nearcat['question_maps'])==97
for m in nearcat['question_maps']:assert deref(m['original_refs'],nearcat['catalog'])==snapshots[m['question_id']]
for doc in report['read_docs']:
 assert sha((ctl/doc['path']).read_bytes())==sha((w/doc['evidence_path']).read_bytes())==doc['raw_sha256']
 assert doc['used_as_Massachusetts_legal_authority'] is False
for field in ['style_profile','schema_reference']:
 z=report[field];assert sha((w/z['evidence_path']).read_bytes())==z['file_sha256']
style=report['style_profile'];assert sha((w/style['public_sample_reference_path']).read_bytes())==style['public_sample_reference_sha256']
publicstyle=load(w/style['public_sample_reference_path']);assert publicstyle['cache_http_status']==200 and publicstyle['fresh_live_status']==403
assert publicstyle['cache_retrieved_at_utc'].startswith('2026-11-03') and publicstyle['actual_read_date_utc']=='2026-11-04'
assert sha(pathlib.Path(publicstyle['local_cache_path']).read_bytes())==publicstyle['cache_raw_sha256']=='b8544f403990191075747b231c81cde4449c6eb83333cfb1d9f05b5e1273d30d'
# Controller checks, read only. Provisional HEAD is solely for precommit validation, never submitted.
result={k:copy.deepcopy(report[k]) for k in ['stage','independent_of_authors','auditor','auditor_instance','actor_provenance']}
result.update(question_hashes=job['question_hashes'],worker_commit=subprocess.check_output(['git','-C',str(w),'rev-parse','HEAD'],text=True).strip(),results=[{'question_id':r['question_id'],'disposition':r['disposition'],'evidence_path':rel,'evidence_sha256':sha((w/rel).read_bytes())} for r in report['records']])
rq.validate_result(job,result);j=copy.deepcopy(job);j['result']=result
for row in result['results']:rq.validate_independent_evidence(j,row,report)
# No tracked original or unrelated file can be modified.
status=subprocess.check_output(['git','-C',str(w),'status','--porcelain','--untracked-files=all'],text=True)
for line in status.splitlines():
 path=line[3:];assert path==rel or path.startswith(pre+'/'),path
checks={'status':'PASS','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'controller_validation_script_sha256':sha((ctl/'scripts/review_queue.py').read_bytes()),'checks':{'current_root_validate_result':'PASS','current_root_validate_independent_evidence_40':'PASS','full_question_record_digest_assignment_packet_worktree_and_controller_40':'PASS','lossless_original_all_field_catalog_roundtrip_40':'PASS','all_original_stems_options_keys_korean_explanations_bound':'PASS','choice_text_hash_manual_support_and_key_set_200':'PASS','per_option_current_official_primary_raw_sha_section_url_date_version':'PASS','source_attempts_35_used_primary_32_failed_403_404_not_proof':'PASS','canonical_439_public_2346_corpus_bytes':'PASS','nearest_original_full_stems_all_choices_97_catalog_roundtrip':'PASS','realism_10_criteria_each_and_dispositions_40':'PASS','same_session_actual_provenance_and_canonical_credit_zero':'PASS','Nov3_public_style_cache_and_Nov4_live403_preserved':'PASS','only_allowed_report_evidence_paths_modified':'PASS'},'limits':'Schema checks and SHA checks bind reported evidence; they do not themselves prove legal correctness or actual independence. No canonical admission/release credit; no original or queue mutations.'}
if '--verify-only' not in sys.argv:
 (e/'validation-log.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','question_count':40,'option_count':200,'used_primary_count':32,'fresh_attempt_count':35,'nearest_originals':97,'realism_pass':3,'realism_fail':37},ensure_ascii=False))
