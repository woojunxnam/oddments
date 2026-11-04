"""Read-only native queue and evidence checks for the assigned review."""
from pathlib import Path
import copy
import hashlib
import json
import subprocess
import sys
from collections import Counter
import jsonschema

ROOT=Path(__file__).resolve().parents[3]
BASE=Path('reports/full-corpus-review/phase11-c-evidence')
REPORT=Path('reports/full-corpus-review/independent-phase11-c-review.json')
sys.path.insert(0,str(ROOT/'scripts'))
import review_queue
from export_legacy_review_input import export
from qa_common import semantic_content_hash
from build_full_corpus_review import validate_independent_source_bytes

def read(p): return json.loads((ROOT/p).read_bytes())
def sha(p): return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()

job=read(BASE/'assignment.json');report=read(REPORT);packet=read(BASE/'assigned-visible-input.json')
assert packet==export(job,ROOT)
assert report['question_hashes']==job['question_hashes']
assert len(report['records'])==40
assert {r['question_id'] for r in report['records']}==set(job['question_hashes'])
assert report['canonical_audit'] is False and report['canonical_release_credit']==0
assert report['author_review_credit']==0
review_queue.validate_independent_provenance(job,report)
required_criteria={'jurisprudence_reasoning','practice_plausibility','authentic_distractors','wording_not_guessable','reasoning_not_trivia','natural_rule_combination','appropriate_drug_context','distinct_from_bank','not_schedule_flashcard','public_style_without_copying'}
byid={r['question_id']:r['original_visible_content'] for r in packet['records']}
for r in report['records']:
 q=byid[r['question_id']];legal=r['legal_review'];real=r['realism_review']
 assert r['record_sha256']==job['question_hashes'][r['question_id']]
 assert len(legal['per_choice_findings'])==len(q['choices'])
 independently_selected=[]
 for choice, finding in zip(q['choices'],legal['per_choice_findings']):
  assert choice['id']==finding['choice_id'] and choice['text']==finding['option_text']
  assert finding['option_text_sha256']==hashlib.sha256(choice['text'].encode()).hexdigest()
  truth=finding['statement_supported']
  if (not truth if 'INCORRECT' in q['stem'] else truth):independently_selected.append(choice['id'])
  for authority in finding['authorities']:
   assert authority['http_status']==200 and authority['legal_authority_used'] is True
   validate_independent_source_bytes(authority,ROOT)
 assert independently_selected==legal['independently_expected_key']==legal['stored_key']==q['correct_choice_ids']
 if q['question_type']=='SBA':assert len(independently_selected)==1
 assert legal['original_explanation_review']['all_choice_rationales_read_in_full'] is True
 assert set(legal['original_explanation_review']['choice_analysis'])=={c['id'] for c in q['choices']}
 assert set(real['criteria'])==set(real['criterion_findings_ko'])==required_criteria
 assert (real['verdict']=='PASS')==all(real['criteria'].values())
 assert r['release_eligible'] is False
 for source in legal['authorities']:validate_independent_source_bytes(source,ROOT)
for source in report['sources']:
 validate_independent_source_bytes(source,ROOT)
 assert sha(source['retrieval_metadata_path'])==source['retrieval_metadata_sha256']
 if source['http_status']!=200:assert source['legal_authority_used'] is False
for doc in report['context']['read_docs']:assert sha(doc['path'])==doc['sha256']
for object_type,file,schema in [('style_profile','mpje_style_profile.json','exam_style_profile.schema.json'),('blueprint','blueprint.json','blueprint.schema.json')]:
 p=BASE/'context/review-methodology'/file;s=BASE/'context/review-methodology'/schema
 value=read(p);jsonschema.Draft202012Validator(read(s)).validate(value)
 assert semantic_content_hash(value,object_type)==value['content_hash']
 assert report[object_type]['file_sha256']==sha(p)
 assert report[object_type]['schema_sha256']==sha(s)

head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
result={k:copy.deepcopy(report[k]) for k in ['stage','independent_of_authors','auditor','auditor_instance','actor_provenance','question_hashes']}
result['worker_commit']=head
result['results']=[dict(question_id=r['question_id'],disposition='INDEPENDENT_ASSESSED' if r['legal_review']['verdict']=='KEEP' and r['realism_review']['verdict']=='PASS' else 'NEEDS_REMEDIATION',evidence_path=str(REPORT),evidence_sha256=sha(REPORT)) for r in report['records']]
review_queue.validate_result(job,result)
bound_job=copy.deepcopy(job);bound_job['result']=result
for row in result['results']:review_queue.validate_independent_evidence(bound_job,row,report)
out=dict(status='PASS',native_checks=['export_legacy_review_input.export exact whole-record hash and visible whitelist binding','review_queue.validate_independent_provenance','review_queue.validate_result','review_queue.validate_independent_evidence x40','build_full_corpus_review.validate_independent_source_bytes every actual authority','qa_common.semantic_content_hash style/blueprint; native JSON schemas'],question_count=40,choice_count=160,dispositions=dict(Counter(r['disposition'] for r in result['results'])),report_path=str(REPORT),report_sha256=sha(REPORT),canonical_release_credit=0,author_review_credit=0,note='Read-only validation. No submit/integrate/generated/bank/governance mutation. Final worker commit must be rebound after committing this evidence.')
(ROOT/BASE/'native-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
