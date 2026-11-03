import json,pathlib,hashlib,gzip,importlib.util,sys,collections,subprocess
R=pathlib.Path('/workspace/independent-phase4-g');RP=R/'reports/full-corpus-review/independent-phase4-g-review.json';r=json.load(open(RP));a=json.load(open('/tmp/independent-phase4-g-assignment.json'));p=json.load(open('/tmp/independent-phase4-g-visible.json'));vr={x['question_id']:x for x in p['records']}
def sha(x):return hashlib.sha256(x).hexdigest()
def dh(x):return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
ex=module('current_root_export','/workspace/oddments/scripts/export_legacy_review_input.py');current=ex.export(a,root=pathlib.Path('/workspace/oddments'));assert current['question_hashes']==a['question_hashes'];assert current['records']==p['records']
assert r['question_hashes']==a['question_hashes'] and set(vr)==set(a['question_hashes']) and len(r['records'])==40
assert r['canonical_audit'] is False and r['canonical_release_credit']==0
sources={x['source_id']:x for x in r['sources']};assert len(sources)==26
for s in sources.values():
 path=R/s['evidence_path'];raw=path.read_bytes();assert sha(raw)==s['evidence_sha256']
 if path.suffix=='.gz':raw=gzip.decompress(raw)
 assert sha(raw)==s['raw_sha256'];assert sha((R/s['text_evidence_path']).read_bytes())==s['text_sha256'];assert sha((R/s['retrieval_metadata_path']).read_bytes())==s['retrieval_metadata_sha256'];m=json.load(open(R/s['retrieval_metadata_path']));assert m['body_verification']=='APPLICABLE_PRIMARY_BODY_DIRECTLY_READ' and m['http_status']==200
 assert s['version'] and s['exact_section'] and s['effective_date_status'] and s['law_checked_date']=='2026-11-03'
criteria={'jurisprudence_reasoning','practice_plausibility','authentic_distractors','wording_not_guessable','reasoning_not_trivia','natural_rule_combination','appropriate_drug_context','distinct_from_bank','not_schedule_flashcard','public_style_without_copying'}
for x in r['records']:
 qid=x['question_id'];v=vr[qid];q=v['original_visible_content'];assert x['record_sha256']==a['question_hashes'][qid] and dh(q)==v['visible_content_sha256']==x['visible_content_sha256'];l=x['legal_review'];z=x['realism_review'];assert l['stored_key']==q['correct_choice_ids']==l['independently_expected_key'];assert l['existing_answer_correct'] in {'YES','NO','AMBIGUOUS','NOT_ASSESSED'};assert len(l['per_choice_findings'])==len(q['choices'])==4
 for c,orig in zip(l['per_choice_findings'],q['choices']):
  assert c['option_text']==orig['text'] and c['choice_id']==orig['id'];assert c['option_text_sha256']==sha(orig['text'].encode());assert c['original_rationale_sha256']==sha(q['explanation']['choice_analysis'][orig['id']].encode());assert c['supported'] in {'YES','NO','AMBIGUOUS','NOT_ASSESSED'} and c['authorities']
  for b in c['authorities']:
   s=sources[b['source_id']];assert b['raw_sha256']==s['raw_sha256'] and b['evidence_sha256']==s['evidence_sha256'] and b['official_url']==s['official_url'];assert b['exact_section'] in s['exact_section']
 assert l['original_explanation_review']['core_sha256']==sha(q['explanation']['core_reasoning'].encode())
 assert set(z['criteria'])==criteria==set(z['criterion_findings_ko']);assert all(isinstance(v,bool) for v in z['criteria'].values());assert z['verdict']!='PASS' or all(z['criteria'].values());assert not x['release_eligible'];d=z['duplicate_evidence'];assert d['canonical_count']==439 and d['public_count']==2346 and d['all_actual_nearest_full_stems_and_options_read'];assert sha((R/d['evidence_path']).read_bytes())==d['evidence_sha256'];assert sha((R/d['default_comparison_path']).read_bytes())==d['default_comparison_sha256']
for x in r['policy_snapshot']+r['schema_snapshot']:assert sha((R/x['path']).read_bytes())==x['file_sha256']
assert sha((R/r['source_register_path']).read_bytes())==r['source_register_sha256']
assert sha((R/r['public_style_evidence']['path']).read_bytes())==r['public_style_evidence']['sha256']
assert len(json.load(open(R/'reports/full-corpus-review/evidence/independent-phase4-g/proposition-register.json'))['propositions'])==77
result={k:r[k] for k in ['stage','independent_of_authors','auditor','auditor_instance','actor_provenance','canonical_audit','canonical_release_credit','question_hashes']};result['worker_commit']=subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD'],text=True).strip();result['results']=[{'question_id':x['question_id'],'disposition':'NEEDS_REMEDIATION' if x['realism_review']['verdict']=='FAIL' else 'INDEPENDENT_ASSESSED','evidence_path':str(RP.relative_to(R)),'evidence_sha256':sha(RP.read_bytes())} for x in r['records']]
pathlib.Path('/tmp/independent-phase4-g-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');rq=module('current_root_review_queue','/workspace/oddments/scripts/review_queue.py');rq.validate_result(a,result);job=dict(a,result=result)
for row in result['results']:rq.validate_independent_evidence(job,row,r)
print(json.dumps({'status':'PASS','current_root_record_hashes_and_complete_visible_content':40,'choice_and_rationale_bindings':160,'unique_propositions':77,'primary_raw_and_source_bindings':26,'ten_criteria_each':40,'report_sha256':sha(RP.read_bytes()),'worker_commit':result['worker_commit'],'manifest_sha256':sha(pathlib.Path('/tmp/independent-phase4-g-result.json').read_bytes()),'current_root_review_queue_validate_result':'PASS','current_root_validate_independent_evidence':'PASS40','queue_submit_or_generated_build':'NOT_RUN_ROOT_ONLY'},indent=2))
