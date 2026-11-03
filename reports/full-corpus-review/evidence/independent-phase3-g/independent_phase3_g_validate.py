import collections,gzip,hashlib,importlib.util,json,pathlib,sys
ROOT=pathlib.Path('/workspace/independent-phase3-g')
RP=ROOT/'reports/full-corpus-review/independent-phase3-g-review.json'
report=json.load(open(RP));a=json.load(open('/tmp/independent-phase3-g-assignment.json'))
packet=json.load(open('/workspace/oddments/reports/full-corpus-review/independent-phase3-g-visible-input.json'))
visible={r['question_id']:r for r in packet['records']}
def sha(b):return hashlib.sha256(b).hexdigest()
def objsha(o):return sha(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
assert set(report['question_hashes'])==set(a['question_hashes'])==set(visible)
assert report['question_hashes']==a['question_hashes']
assert len(report['records'])==40
assert report['canonical_audit'] is False and report['canonical_release_credit']==0
assert report['actor_provenance']['actor_id']==report['actor_provenance']['session_id']=='/root/independent_case_g'
sources={s['source_id']:s for s in report['sources']}
assert len(sources)==29
criteria={'jurisprudence_reasoning','practice_plausibility','authentic_distractors','wording_not_guessable','reasoning_not_trivia','natural_rule_combination','appropriate_drug_context','distinct_from_bank','not_schedule_flashcard','public_style_without_copying'}
for s in sources.values():
 path=ROOT/s['evidence_path'];raw=path.read_bytes()
 assert sha(raw)==s['evidence_sha256']
 if path.suffix=='.gz':raw=gzip.decompress(raw)
 assert sha(raw)==s['raw_sha256']
 assert sha((ROOT/s['text_evidence_path']).read_bytes())==s['text_evidence_sha256']
 assert s['official_url'].startswith('https://') and s['law_checked_date']=='2026-11-03'
 assert s['exact_section'] and s['version'] and 'effective_date' in s
 assert s['retrieval_provenance']['http_status']==200
 assert 'DIRECTLY_READ' in s['retrieval_provenance']['body_verification']
for r in report['records']:
 qid=r['question_id'];vr=visible[qid];q=vr['original_visible_content']
 assert r['record_sha256']==a['question_hashes'][qid]
 assert objsha(q)==vr['visible_content_sha256']==r['visible_content_sha256']
 lr=r['legal_review'];rr=r['realism_review']
 assert lr['existing_answer_correct'] in {'YES','NO','AMBIGUOUS','NOT_ASSESSED'}
 assert lr['stored_key']==q['correct_choice_ids']==lr['independently_expected_key']
 assert len(lr['per_choice_findings'])==len(q['choices'])==4
 for c,orig in zip(lr['per_choice_findings'],q['choices']):
  assert c['choice_id']==orig['id'] and c['option_text']==orig['text']
  assert c['option_text_sha256']==sha(orig['text'].encode())
  assert c['original_rationale_sha256']==sha(q['explanation']['choice_analysis'][orig['id']].encode())
  assert c['supported'] in {'YES','NO','AMBIGUOUS','NOT_ASSESSED'}
  assert c['authorities']
  for ref in c['authorities']:
   s=sources[ref['source_id']]
   assert ref['official_url']==s['official_url']
   assert ref['raw_sha256']==s['raw_sha256'] and ref['evidence_sha256']==s['evidence_sha256']
 assert set(rr['criteria'])==criteria==set(rr['criterion_findings_ko'])
 assert all(isinstance(v,bool) for v in rr['criteria'].values())
 assert rr['verdict']!='PASS' or all(rr['criteria'].values())
 assert rr['verdict']=='FAIL' and r['release_eligible'] is False
 assert rr['duplicate_evidence']['canonical_count']==439
 assert rr['duplicate_evidence']['public_count']==2346
 assert rr['duplicate_evidence']['status']=='RUN_AND_MANUALLY_READ'
 assert sha((ROOT/rr['duplicate_evidence']['evidence_path']).read_bytes())==rr['duplicate_evidence']['evidence_sha256']
 assert lr['original_explanation_review']['core_sha256']==sha(q['explanation']['core_reasoning'].encode())
 if qid in {'MA-CASE-0542','MA-CASE-0545'}:assert lr['verdict']=='HOLD' and lr['blocker']
 else:assert lr['verdict']=='KEEP'
assert sha((ROOT/report['source_register_path']).read_bytes())==report['source_register_sha256']
for p in report['policy_snapshot']+report['schema_snapshot']:
 assert sha((ROOT/p['path']).read_bytes())==p['file_sha256']
assert len(json.load(open(ROOT/'reports/full-corpus-review/evidence/independent-phase3-g/independent-proposition-findings.json'))['propositions'])==80
counts=dict(collections.Counter(r['legal_review']['verdict'] for r in report['records']))
result_path=pathlib.Path('/tmp/independent-phase3-g-result.json')
if result_path.exists():
 result=json.load(open(result_path))
 spec=importlib.util.spec_from_file_location('current_root_review_queue','/workspace/oddments/scripts/review_queue.py')
 mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 mod.validate_result(a,result)
 job=dict(a,result=result)
 for row in result['results']:
  mod.validate_independent_evidence(job,row,report)
  assert row['evidence_sha256']==sha(RP.read_bytes())
 print('current root review_queue.validate_result + validate_independent_evidence: PASS (read-only)')
print(json.dumps(dict(status='PASS',assigned=40,exact_visible_hashes=40,option_and_rationale_bindings=160,unique_propositions=80,source_raw_bindings=len(sources),legal_verdict=counts,report_sha256=sha(RP.read_bytes()),notes='No canonical release validator, queue submit, ledger update or generated build was run.'),ensure_ascii=False,indent=2))
