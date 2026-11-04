import json,pathlib,hashlib,importlib.util,collections,subprocess,sys,urllib.parse
R=pathlib.Path('/workspace/independent-phase8-g');ROOT=pathlib.Path('/workspace/oddments')
E=R/'reports/full-corpus-review/evidence/independent-phase8-g';RP=R/'reports/full-corpus-review/independent-phase8-g-review.json'
r=json.load(open(RP));a=json.load(open('/tmp/independent-phase8-g-assignment.json'));p=json.load(open('/tmp/independent-phase8-g-visible.json'));vr={x['question_id']:x for x in p['records']}
def sha(b):return hashlib.sha256(b).hexdigest()
def dh(x):return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def mod(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def git(*args):return subprocess.check_output(['git','-C',str(R),*args])
# Protected raw objects and ledger enter exporter code only. No raw object or hidden value is printed.
ex=mod('current_root_safe_export',ROOT/'scripts/export_legacy_review_input.py');current=ex.export(a,root=ROOT)
assert current['records']==p['records'] and current['question_hashes']==a['question_hashes']==r['question_hashes']
assert set(vr)=={f'MA-EXP-{i:04d}' for i in range(89,129)} and len(r['records'])==40
assert r['actor_provenance']=={'actor_id':'/root/independent_case_g','session_id':'/root/independent_case_g'}
assert r['auditor_instance']=='gpt-independent-phase3-g-root-independent_case_g-20261103'
assert r['stage']=='independent-legacy' and r['independent_of_authors'] is True and r['canonical_audit'] is False
assert r['canonical_release_credit']==r['author_review_credit']==0 and r['reviewed_at']=='2026-11-04'
ss={s['source_id']:s for s in r['sources']};assert set(ss)=={'intern-tech','practice','scope-policy','reporting','1306-11','1306-12','1306-25','ma721'}
for s in ss.values():
 assert s['source_type']=='PUBLIC_OFFICIAL' and s['official_url'].startswith('https://')
 assert urllib.parse.urlparse(s['official_url']).hostname in {'www.mass.gov','www.ecfr.gov'}
 assert sha((R/s['evidence_path']).read_bytes())==s['evidence_sha256']==s['raw_sha256']
 assert sha((R/s['retrieval_metadata_path']).read_bytes())==s['retrieval_metadata_sha256']
 assert sha((R/s['text_evidence_path']).read_bytes())==s['text_sha256']
 m=json.load(open(R/s['retrieval_metadata_path']))
 assert m['http_status']==200 and m['body_verification']=='APPLICABLE_OFFICIAL_SECTIONS_DIRECTLY_READ'
 assert m['retrieved_at'].startswith('2026-11-04') and m['tls_verification'] is True and m['retrieval_method']=='LIVE_OFFICIAL_HTTPS_urllib'
 assert m['raw_sha256']==s['raw_sha256'] and s['law_checked_date']=='2026-11-04'
 assert s['version_or_effective_date_status'] and s['effective_date_status'] and s['exact_section'] and s['raw_full_committed']
props=json.load(open(E/'proposition-register.json'))['propositions'];assert len(props)==77;pm={x['proposition_id']:x for x in props}
fm={x['question_id']:x for x in json.load(open('/tmp/independent-phase8-g-family-only.json'))}
crit={'jurisprudence_reasoning','practice_plausibility','authentic_distractors','wording_not_guessable','reasoning_not_trivia','natural_rule_combination','appropriate_drug_context','distinct_from_bank','not_schedule_flashcard','public_style_without_copying'}
count=0;polarity=collections.Counter();bad=[]
for x in r['records']:
 q=vr[x['question_id']]['original_visible_content'];assert set(q)=={'question_id','question_type','stem','choices','correct_choice_ids','explanation'}
 assert x['record_sha256']==a['question_hashes'][x['question_id']]==fm[x['question_id']]['record_sha256']
 assert dh(q)==vr[x['question_id']]['visible_content_sha256']==x['visible_content_sha256']
 assert x['family_id']==fm[x['question_id']]['family_id'] and x['collection']==fm[x['question_id']]['collection']
 assert all(x['read_scope'][k] for k in ['original_stem','all_choices','stored_key','complete_korean_core','all_korean_distractor_rationales','complete_visible_explanation'])
 l=x['legal_review'];z=x['realism_review'];assert l['stored_key']==q['correct_choice_ids'];assert len(l['per_choice_findings'])==len(q['choices'])==4
 yes=[];no=[]
 for c,orig in zip(l['per_choice_findings'],q['choices']):
  count+=1;assert c['choice_id']==orig['id'] and c['option_text']==orig['text']
  assert c['option_text_sha256']==sha(orig['text'].encode())==pm[c['proposition_id']]['option_text_sha256']
  assert c['original_rationale_read'] and c['original_rationale_sha256']==sha(q['explanation']['choice_analysis'][orig['id']].encode())
  assert c['supported'] in {'YES','NO','AMBIGUOUS','NOT_ASSESSED'} and c['supported']==pm[c['proposition_id']]['supported']
  assert c['supported'] in {'YES','NO'}
  (yes if c['supported']=='YES' else no).append(c['choice_id'])
  assert c['authorities'] and c['subject_condition_exception_review_ko'] and c['original_rationale_finding_ko']
  for au in c['authorities']:
   s=ss[au['source_id']];assert au['official_url']==s['official_url'] and au['exact_section'] in s['exact_section']
   assert au['raw_sha256']==s['raw_sha256'] and au['evidence_sha256']==s['evidence_sha256'] and au['law_checked_date']=='2026-11-04'
 assert yes==l['independently_definite_supported_choices'] and l['possible_supported_choices_pending_missing_facts']==[]
 negative='INCORRECT' in q['stem'];expected=no if negative else yes
 assert l['independently_expected_key']==expected==q['correct_choice_ids'] and l['existing_answer_correct']=='YES' and l['verdict']=='KEEP' and l['blocker'] is None
 if q['question_type']!='SATA':assert len(expected)==1
 polarity['INCORRECT_SBA' if negative else 'SATA' if q['question_type']=='SATA' else 'POSITIVE_SBA']+=1
 exr=l['original_explanation_review'];assert exr['complete_core_read'] and exr['all_choice_rationales_read'] and exr['rationale_count']==4
 assert exr['core_sha256']==sha(q['explanation']['core_reasoning'].encode()) and exr['learning_boundary_sha256']==sha(q['explanation']['learning_boundary'].encode())
 assert exr['assessment']=='SUPPORTED_IN_STATED_SCOPE' and len(exr['choice_findings'])==4
 assert set(z['criteria'])==set(z['criterion_findings_ko'])==crit and all(isinstance(v,bool) for v in z['criteria'].values()) and all(z['criterion_findings_ko'].values())
 assert (z['verdict']=='PASS')==all(z['criteria'].values()) and not x['release_eligible']
 assert x['safe_hold_recommended']==(z['verdict']=='FAIL') and x['canonical_release_credit']==x['author_review_credit']==0 and x['canonical_audit'] is False
 d=z['duplicate_evidence'];assert d['canonical_count']==439 and d['public_count']==2346 and d['current_committed_default_count']==298 and d['actual_full_stem_all_options_read']
 assert sha((R/d['evidence_path']).read_bytes())==d['evidence_sha256'] and sha((R/d['default_evidence_path']).read_bytes())==d['default_evidence_sha256']
 for k in ['nearest_canonical','nearest_public','nearest_public_other_family','nearest_current_default']:
  v=d[k]['full_stem_and_all_options'];assert v['stem'] and len(v['choices'])>=4 and v['question_id']!=x['question_id']
 assert d['semantic_comparison_ko'] and d['current_default_comparison_ko'] and d['current_default_pool'] is False and x['currently_recommended'] is False
 assert x['metadata_review']['automatic_item_error_or_legal_hold'] is False
 assert x['metadata_review']['additional_current_note_content_alignment']=='NOT_ASSESSED_NO_CONFLICT_INFERRED_FROM_HASH'
 if z['verdict']=='FAIL':
  bad.append(x['question_id']);assert z['actual_problematic_options']
  for c in z['actual_problematic_options']:assert c['option_sha256']==sha(c['text'].encode()) and any(o['id']==c['choice_id'] and o['text']==c['text'] for o in q['choices'])
assert count==160 and polarity=={'POSITIVE_SBA':20,'INCORRECT_SBA':10,'SATA':10}
assert len(bad)==19 and collections.Counter(x['realism_review']['verdict'] for x in r['records'])=={'FAIL':19,'PASS':21}
for z in r['policy_snapshot']+r['schema_snapshot']:assert sha((R/z['path']).read_bytes())==z['file_sha256']
sys.path.insert(0,str(R/'scripts'));from qa_common import semantic_content_hash
style=json.load(open(R/r['style_profile']['path']));assert semantic_content_hash(style,'style_profile')==r['style_profile']['semantic_hash']==style['content_hash']
assert sha((R/r['style_profile']['path']).read_bytes())==r['style_profile']['file_sha256']
from jsonschema import Draft202012Validator
Draft202012Validator(json.load(open(R/'schemas/exam_style_profile.schema.json'))).validate(style)
assert sha((R/r['source_register_path']).read_bytes())==r['source_register_sha256']
assert sha((R/r['public_style_evidence']['path']).read_bytes())==r['public_style_evidence']['sha256']
nm=json.load(open(E/'nabp-retrieval.json'));assert nm['http_status']==200 and nm['retrieved_at'].startswith('2026-11-04')
assert sha((R/nm['raw_evidence_path']).read_bytes())==r['public_style_evidence']['raw_sha256']=='b8544f403990191075747b231c81cde4449c6eb83333cfb1d9f05b5e1273d30d'
assert len(r['excluded_source_attempts'])==2
for z in r['excluded_source_attempts']:assert not z['used_as_verified_authority'] and sha((R/z['metadata_path']).read_bytes())==z['metadata_sha256']
for pk,hk in [('whitelist_path','whitelist_raw_sha256'),('family_only_path','family_only_sha256'),('read_history_path','read_history_sha256'),('proposition_register_path','proposition_register_sha256'),('same_session_history_path','same_session_history_sha256')]:
 assert sha((R/r['input_evidence'][pk]).read_bytes())==r['input_evidence'][hk]
assert r['input_evidence']['assignment_raw_sha256']==sha(pathlib.Path('/tmp/independent-phase8-g-assignment.json').read_bytes())
hist=json.load(open(E/'same-session-exposure-history.json'));assert not hist['author_of_assigned_current_questions'] and all(not x.get('assigned_id_intersection') for x in hist['prior_safe_input_id_checks'])
meta=json.load(open(E/'root-metadata-status.json'));bindings=meta['question_note_body_bindings'];assert len(bindings)==52
assert all(x['matches_original_raw_snapshot'] and x['question_note_evidence_body_sha256']==x['original_raw_guide_body_sha256'] for x in bindings)
historical={x['question_id'] for x in bindings if not x['matches_current_effective_body']}
assert len(historical)==12 and historical==set(meta['historical_noncurrent_snapshot_question_ids'])
assert meta['historical_input_guide_binding']['promised_raw_guide_snapshot_matches'] and meta['historical_input_guide_binding']['all52_question_note_body_bindings_match_promised_raw_snapshot']
assert meta['historical_input_guide_binding']['bank_input_guide_sha256']==meta['historical_input_guide_binding']['actual_raw_guide_file_sha256']
assert meta['current_note_content_alignment']=='NOT_ASSESSED_NO_CONTENT_CONFLICT_INFERRED_FROM_HASH_DIFFERENCE'
assert r['root_metadata_evidence']['automatic_legal_or_item_hold'] is False and r['root_metadata_evidence']['historical_noncurrent_overlay_bindings']==12
for x in r['records']:assert (x['metadata_review']['effective_note_alignment']=='HISTORICAL_NOTE_SNAPSHOT_NOT_CURRENT')==(x['question_id'] in historical)
assert sha((R/r['root_metadata_evidence']['path']).read_bytes())==r['root_metadata_evidence']['sha256']
defaults=json.load(open(E/'default-only-input.json'));assert len(defaults['recommended_ids'])==298 and not(set(defaults['recommended_ids'])&set(vr))
assert r['default_pool_snapshot']['assigned_default_intersection_count']==0
nearest=json.load(open(E/'nearest-display.json'));assert len(nearest)==68 and all(x['stem'] and len(x['choices'])>=4 for x in nearest)
out={k:r[k] for k in ['stage','independent_of_authors','auditor','auditor_instance','actor_provenance','canonical_audit','canonical_release_credit','author_review_credit','question_hashes']}
out['worker_commit']=git('rev-parse','HEAD').decode().strip()
out['results']=[{'question_id':x['question_id'],'disposition':'NEEDS_REMEDIATION' if x['realism_review']['verdict']=='FAIL' else 'INDEPENDENT_ASSESSED','evidence_path':str(RP.relative_to(R)),'evidence_sha256':sha(RP.read_bytes())} for x in r['records']]
rq=mod('current_root_review_queue',ROOT/'scripts/review_queue.py');rq.validate_result(a,out);job=dict(a,result=out)
for row in out['results']:rq.validate_independent_evidence(job,row,r)
if '--write-envelope' in sys.argv:
 assert git('show','HEAD:'+str(RP.relative_to(R)))==RP.read_bytes()
 for f in E.rglob('*'):
  if f.is_file():assert git('show','HEAD:'+str(f.relative_to(R)))==f.read_bytes()
 pathlib.Path('/tmp/independent-phase8-g-result.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','current_root_record_and_complete_visible_hashes':40,'choices_and_rationales':160,'manual_propositions':77,'primary_source_bindings':8,'criteria_assessed':400,'polarity_counts':dict(polarity),'legal_answers':r['counters']['legal_answer_correct'],'legal_verdicts':r['counters']['legal_verdict'],'realism_verdicts':r['counters']['realism_verdict'],'dispositions':dict(collections.Counter(x['disposition'] for x in out['results'])),'historical_raw_snapshot_valid':52,'historical_snapshot_noncurrent_not_automatic_defect':12,'nearest_full_stem_options_candidates':68,'assigned_default_intersection':0,'style_profile_semantic_and_schema':'PASS','current_root_validate_result':'PASS','current_root_validate_independent_evidence':'PASS40','report_sha256':sha(RP.read_bytes()),'worker_commit':out['worker_commit'],'envelope_written':'--write-envelope' in sys.argv,'queue_submit_or_integrate':'NOT_RUN_ROOT_ONLY'},ensure_ascii=False,indent=2))
