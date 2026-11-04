"""Read-only validation of this actual session's report and immutable source bindings."""
import copy,hashlib,json,sys,subprocess
from pathlib import Path
from collections import Counter
import jsonschema
ROOT=Path(__file__).resolve().parents[3];BASE=Path('reports/full-corpus-review/recovered-phase11-d-evidence');REPORT=Path('reports/full-corpus-review/recovered-phase11-d-review.json');sys.path.insert(0,str(ROOT/'scripts'))
import review_queue as queue
from build_full_corpus_review import validate_independent_source_bytes
from export_legacy_review_input import export
from qa_common import semantic_content_hash

def read(p):return json.loads((ROOT/p).read_bytes())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
job=read(BASE/'assignment.json');report=read(REPORT);packet=read(BASE/'assigned-visible-input.json')
assert packet==export(job,ROOT)
assert report['question_hashes']==job['question_hashes']
assert len(report['records'])==40 and {r['question_id'] for r in report['records']}==set(job['question_hashes'])
assert report['canonical_audit'] is False and report['canonical_release_credit']==report['author_review_credit']==0
assert report['actor_provenance']==dict(actor_id='/root/recover_d_review',session_id='/root/recover_d_review')
queue.validate_independent_provenance(job,report)
byid={r['question_id']:r['original_visible_content'] for r in packet['records']}
criteria={'jurisprudence_reasoning','practice_plausibility','authentic_distractors','wording_not_guessable','reasoning_not_trivia','natural_rule_combination','appropriate_drug_context','distinct_from_bank','not_schedule_flashcard','public_style_without_copying'}
for row in report['records']:
 q=byid[row['question_id']];legal=row['legal_review'];real=row['realism_review'];expected=[]
 assert row['record_sha256']==job['question_hashes'][row['question_id']]
 assert len(legal['per_choice_findings'])==len(q['choices'])==4
 for c,find in zip(q['choices'],legal['per_choice_findings']):
  assert find['choice_id']==c['id'] and find['option_text']==c['text'] and find['option_text_sha256']==hashlib.sha256(c['text'].encode()).hexdigest()
  truth=find['statement_supported'];select=not truth if 'INCORRECT' in q['stem'] else truth
  assert find['selected_under_polarity']==select
  if select:expected.append(c['id'])
  assert find['finding_ko'] and find['authorities']
  for a in find['authorities']:
   assert a['http_status']==200 and a['legal_authority_used'] is True and a['official_url'].startswith('https://')
   validate_independent_source_bytes(a,ROOT)
   assert sha(a['retrieval_metadata_path'])==a['retrieval_metadata_sha256']
 assert expected==legal['stored_key']==q['correct_choice_ids']
 if row['question_id'] in {'MA-EXP-0338','MA-EXP-0339'}:
  assert legal['verdict']=='HOLD' and legal['existing_answer_correct']=='NOT_ASSESSED' and legal['independently_expected_key']==[]
  assert legal['blocker']=='PRIOR_CONCLUSION_EXPOSURE_REQUIRES_GENUINELY_FRESH_SESSION'
  assert row['exposure_limitations']['fresh_whole_key_credit']==0
 else:assert legal['independently_expected_key']==expected and legal['existing_answer_correct']=='YES'
 if q['question_type']=='SBA':assert len(expected)==1
 assert legal['original_explanation_review']['all_choice_rationales_read_in_full'] is True
 assert set(legal['original_explanation_review']['choice_analysis'])=={c['id'] for c in q['choices']}
 for c in q['choices']:assert legal['original_explanation_review']['choice_analysis'][c['id']]['original_rationale_sha256']==hashlib.sha256(q['explanation']['choice_analysis'][c['id']].encode()).hexdigest()
 assert set(real['criteria'])==set(real['criterion_findings_ko'])==criteria
 assert (real['verdict']=='PASS')==all(real['criteria'].values())
 assert row['release_eligible'] is False
for source in report['sources']:
 validate_independent_source_bytes(source,ROOT)
 assert sha(source['retrieval_metadata_path'])==source['retrieval_metadata_sha256']
 if source['http_status']!=200:assert source['legal_authority_used'] is False
for doc in report['context']['read_docs']:assert sha(doc['path'])==doc['sha256']
for kind,file,schema in [('style_profile','mpje_style_profile.json','exam_style_profile.schema.json'),('blueprint','blueprint.json','blueprint.schema.json')]:
 p=BASE/'context'/file;s=BASE/'context'/schema;v=read(p);jsonschema.Draft202012Validator(read(s)).validate(v)
 assert semantic_content_hash(v,kind)==v['content_hash'];assert sha(p)==report[kind]['file_sha256'] and sha(s)==report[kind]['schema_sha256']
result={k:copy.deepcopy(report[k]) for k in ['stage','independent_of_authors','auditor','auditor_instance','actor_provenance','question_hashes']}
result['worker_commit']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
result['results']=[dict(question_id=r['question_id'],disposition='HOLD' if r['legal_review']['verdict']=='HOLD' else ('INDEPENDENT_ASSESSED' if r['realism_review']['verdict']=='PASS' else 'NEEDS_REMEDIATION'),evidence_path=str(REPORT),evidence_sha256=sha(REPORT)) for r in report['records']]
queue.validate_result(job,result);bound=copy.deepcopy(job);bound['result']=result
for r in result['results']:queue.validate_independent_evidence(bound,r,report)
print(json.dumps(dict(status='PASS',report_path=str(REPORT),report_sha256=sha(REPORT),records=40,choices=160,dispositions=dict(Counter(r['disposition'] for r in result['results'])),source_payloads_bound=len(report['sources']),canonical_release_credit=0,author_review_credit=0,note='Read-only native/current original/source/schema/binding validation. Does not submit, integrate, release or waive exposure holds.'),ensure_ascii=False,indent=2))
