import json,pathlib,hashlib,gzip,importlib.util,collections,subprocess,sys
R=pathlib.Path('/workspace/independent-phase5-g');RP=R/'reports/full-corpus-review/independent-phase5-g-review.json';r=json.load(open(RP));a=json.load(open('/tmp/independent-phase5-g-assignment.json'));p=json.load(open('/tmp/independent-phase5-g-visible.json'));vr={x['question_id']:x for x in p['records']}
def sha(x):return hashlib.sha256(x).hexdigest()
def dh(x):return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def module(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
ex=module('current_root_export','/workspace/oddments/scripts/export_legacy_review_input.py');current=ex.export(a,root=pathlib.Path('/workspace/oddments'));assert current['records']==p['records'];assert r['question_hashes']==a['question_hashes'] and len(r['records'])==40;assert r['canonical_audit'] is False and r['canonical_release_credit']==0
ss={s['source_id']:s for s in r['sources']};assert len(ss)==32
for s in ss.values():
 ep=R/s['evidence_path'];assert sha(ep.read_bytes())==s['evidence_sha256'];assert sha((R/s['text_evidence_path']).read_bytes())==s['text_sha256'];mp=R/s['retrieval_metadata_path'];assert sha(mp.read_bytes())==s['retrieval_metadata_sha256'];m=json.load(open(mp));assert m['http_status']==200 and 'DIRECTLY_READ' in m['body_verification'];assert s['version'] and s['exact_section'] and 'effective_date' in s and s['effective_date_status']
 if s['raw_full_committed']:
  raw=gzip.decompress(ep.read_bytes()) if ep.suffix=='.gz' else ep.read_bytes();assert sha(raw)==s['raw_sha256']
 else:
  assert s['source_id']=='pmp-guide' and not (R/'reports/full-corpus-review/evidence/independent-phase5-g/pmp-guide.pdf').exists();assert sha(pathlib.Path(m['restricted_local_raw_path']).read_bytes())==s['raw_sha256'];assert 'own_fact_memo_ko' in json.load(open(ep))
ct={'jurisprudence_reasoning','practice_plausibility','authentic_distractors','wording_not_guessable','reasoning_not_trivia','natural_rule_combination','appropriate_drug_context','distinct_from_bank','not_schedule_flashcard','public_style_without_copying'}
for x in r['records']:
 qid=x['question_id'];q=vr[qid]['original_visible_content'];assert x['record_sha256']==a['question_hashes'][qid] and dh(q)==x['visible_content_sha256']==vr[qid]['visible_content_sha256'];l=x['legal_review'];z=x['realism_review'];assert l['stored_key']==q['correct_choice_ids'];assert len(l['per_choice_findings'])==len(q['choices'])==4
 amb=[];yes=[]
 for c,orig in zip(l['per_choice_findings'],q['choices']):
  assert c['choice_id']==orig['id'] and c['option_text']==orig['text'];assert c['option_text_sha256']==sha(orig['text'].encode());assert c['original_rationale_sha256']==sha(q['explanation']['choice_analysis'][orig['id']].encode());assert c['supported'] in {'YES','NO','AMBIGUOUS','NOT_ASSESSED'}
  if c['supported']=='YES':yes.append(c['choice_id'])
  if c['supported']=='AMBIGUOUS':amb.append(c['choice_id'])
  for b in c['authorities']:
   s=ss[b['source_id']];assert b['official_url']==s['official_url'] and b['raw_sha256']==s['raw_sha256'] and b['evidence_sha256']==s['evidence_sha256'] and b['exact_section'] in s['exact_section']
 assert yes==q['correct_choice_ids']==l['independently_definite_supported_choices']
 if amb:assert l['existing_answer_correct']=='AMBIGUOUS' and l['verdict']=='HOLD' and l['independently_expected_key'] is None and l['blocker']
 else:assert l['existing_answer_correct']=='YES' and l['verdict']=='KEEP' and l['independently_expected_key']==yes
 assert l['original_explanation_review']['core_sha256']==sha(q['explanation']['core_reasoning'].encode());assert set(z['criteria'])==ct==set(z['criterion_findings_ko']);assert all(isinstance(v,bool) for v in z['criteria'].values());assert z['verdict']!='PASS' or all(z['criteria'].values());assert not x['release_eligible'];d=z['duplicate_evidence'];assert d['canonical_count']==439 and d['public_count']==2346 and d['actual_full_stem_all_options_read'];assert sha((R/d['evidence_path']).read_bytes())==d['evidence_sha256'];assert sha((R/d['default_evidence_path']).read_bytes())==d['default_evidence_sha256']
for x in r['policy_snapshot']+r['schema_snapshot']:assert sha((R/x['path']).read_bytes())==x['file_sha256']
assert sha((R/r['source_register_path']).read_bytes())==r['source_register_sha256'];assert sha((R/r['public_style_evidence']['path']).read_bytes())==r['public_style_evidence']['sha256'];assert len(json.load(open(R/'reports/full-corpus-review/evidence/independent-phase5-g/proposition-register.json'))['propositions'])==71
out={k:r[k] for k in ['stage','independent_of_authors','auditor','auditor_instance','actor_provenance','canonical_audit','canonical_release_credit','question_hashes']};out['worker_commit']=subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD'],text=True).strip();out['results']=[{'question_id':x['question_id'],'disposition':'HOLD' if x['legal_review']['verdict']=='HOLD' else 'NEEDS_REMEDIATION' if x['realism_review']['verdict']=='FAIL' else 'INDEPENDENT_ASSESSED','evidence_path':str(RP.relative_to(R)),'evidence_sha256':sha(RP.read_bytes())} for x in r['records']];rq=module('current_review_queue','/workspace/oddments/scripts/review_queue.py');rq.validate_result(a,out);job=dict(a,result=out)
for row in out['results']:rq.validate_independent_evidence(job,row,r)
if '--write-envelope' in sys.argv:
 assert subprocess.check_output(['git','-C',str(R),'show','HEAD:'+str(RP.relative_to(R))])==RP.read_bytes();pathlib.Path('/tmp/independent-phase5-g-result.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','current_root_record_and_complete_visible_hashes':40,'choices_and_rationales':160,'unique_propositions':71,'primary_bindings':32,'criteria10each':40,'legal_verdict':dict(collections.Counter(x['legal_review']['verdict'] for x in r['records'])),'realism_verdict':dict(collections.Counter(x['realism_review']['verdict'] for x in r['records'])),'dispositions':dict(collections.Counter(x['disposition'] for x in out['results'])),'report_sha256':sha(RP.read_bytes()),'worker_commit':out['worker_commit'],'manifest_written':'--write-envelope' in sys.argv,'current_review_queue_validate_result':'PASS','validate_independent_evidence':'PASS40','queue_submit_or_generated_build':'NOT_RUN_ROOT_ONLY'},indent=2))
