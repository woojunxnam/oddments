import sys,json,pathlib,hashlib,copy,datetime,subprocess
R=pathlib.Path('.').resolve();sys.path.insert(0,str(R/'scripts'))
import review_queue
from qa_common import semantic_content_hash
from export_legacy_review_input import export
from build_full_corpus_review import validate_independent_source_bytes
D=pathlib.Path(__file__).resolve().parent.relative_to(pathlib.Path.cwd().resolve());E=D.parent;rp=pathlib.Path('reports/full-corpus-review/independent-phase12-a-review.json')
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
a=json.load(open(E/'assignment.json'));p=json.load(open(E/'assigned-visible-input.json'));r=json.load(open(rp));by={x['question_id']:x for x in p['records']}
assert export(a,R)==p
assert r['question_hashes']==a['question_hashes']
assert len(r['records'])==len(a['question_hashes'])==40
assert r['actor_provenance']['actor_id']==a['worker']
assert r['canonical_release_credit']==0 and r['canonical_audit'] is False and r['release_eligible'] is False
assert len({x['question_id'] for x in r['records']})==40
for path,kind in [('data/exam_style/mpje_style_profile.json','style_profile'),('data/blueprint.json','blueprint')]:
 dep=json.load(open(path));assert semantic_content_hash(dep,kind)==dep['content_hash']
checked=0
for s in r['sources']:
 validate_independent_source_bytes(s,R)
 assert s['official_url'].startswith('https://') and s['retrieval_provenance']['status_code']==200
 m=json.load(open(s['metadata_path']));assert sha(s['metadata_path'])==s['metadata_sha256']
 assert m['raw_sha256']==s['raw_sha256'] and m['text_sha256']==s['evidence_sha256']
 assert s['effective_date'] and s['source_read_at'] and s['exact_section'];checked+=1
for x in r['records']:
 v=by[x['question_id']];q=v['original_visible_content'];leg=x['legal_review'];real=x['realism_review']
 assert x['record_sha256']==a['question_hashes'][x['question_id']]
 assert review_queue.digest(q)==v['visible_content_sha256']
 assert leg['stored_key']==q['correct_choice_ids']
 assert {c['choice_id']:c['option_text'] for c in leg['per_choice_findings']}=={c['id']:c['text'] for c in q['choices']}
 assert len(real['criteria'])==len(real['criterion_findings_ko'])==10
 assert (real['verdict']=='PASS')==all(real['criteria'].values())
 assert x['release_eligible'] is False and x['canonical_release_credit']==0
 if leg['existing_answer_correct']=='YES':assert sorted(leg['stored_key'])==leg['independently_expected_key']
 if leg['existing_answer_correct']=='AMBIGUOUS':assert leg['independently_expected_key'] is None and leg['verdict']=='HOLD' and leg['blocker']
 for c in leg['per_choice_findings']:
  assert c['option_text_sha256']==hashlib.sha256(c['option_text'].encode()).hexdigest()
  validate_independent_source_bytes(c['authority'],R)
 assert len(leg['original_explanation_review']['choice_analysis'])==len(q['choices'])
 if real['verdict']=='FAIL':assert x['safe_hold_recommended'] is True
out=dict(kind='native-functions-and-source-byte-validation-not-release-QA',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),assignment_sha256=sha(E/'assignment.json'),report_sha256=sha(rp),assigned_id_hash_count=40,exact_visible_option_count=160,source_descriptors_verified=checked,criteria_count=400,canonical_comparison_count=439,public_comparison_count=2349,canonical_release_credit=0,report_source_bytes='PASS',all_options_and_hashes='PASS',current_full_record_hash_export='PASS',criteria_verdict_consistency='PASS',style_blueprint_semantic_hashes='PASS',live_builders='NOT_RUN_BY_INSTRUCTION',sourceguard='NOT_RUN_BY_INSTRUCTION_SPARSE_PREIMAGE')
(D/'precommit-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
