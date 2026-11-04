"""Read-only native post-commit checks; writes only the designated /tmp envelope."""
from pathlib import Path
import json,sys,hashlib,subprocess,copy
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
from review_queue import validate_result,validate_independent_evidence,digest
BASE=Path(__file__).resolve().parent
assignment=json.loads((BASE/'assignment.json').read_text())
report_path='reports/full-corpus-review/independent-phase12-c-review.json'
raw=(ROOT/report_path).read_bytes();report=json.loads(raw)
worker_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
committed=subprocess.check_output(['git','show',worker_commit+':'+report_path],cwd=ROOT)
assert committed==raw
assert len(report['records'])==40
assert {x['question_id'] for x in report['records']}==set(assignment['question_hashes'])
assert report['canonical_audit'] is False and report['canonical_release_credit']==0 and report['release_eligible'] is False
# Programmatic record digest only; no hidden or prior metadata is printed or used as authority.
questions=json.loads((ROOT/'practice_expansion/2026-10-23/candidates/questions.json').read_text())['questions']
actual={q['question_id']:digest(q) for q in questions if q['question_id'] in assignment['question_hashes']}
assert actual==assignment['question_hashes']
for r in report['records']:
 assert r['record_sha256']==assignment['question_hashes'][r['question_id']]
 assert r['release_eligible'] is False
 assert len(r['legal_review']['per_choice_findings'])==4
 assert all(f['authorities'] for f in r['legal_review']['per_choice_findings'])
 assert len(r['realism_review']['criteria'])==10
 assert set(r['realism_review']['criteria'])==set(r['realism_review']['criterion_findings_ko'])
 for criterion,value in r['realism_review']['criteria'].items():
  assert r['realism_review']['criterion_findings_ko'][criterion].strip()
  assert value in (True,False,None)
 assert r['realism_review']['criteria']['public_style_without_copying'] is None
for src in report['sources']:
 for p,h in [('evidence_path','evidence_sha256'),('text_path','text_sha256'),('retrieval_provenance_path','retrieval_provenance_sha256')]:
  b=(ROOT/src[p]).read_bytes();assert hashlib.sha256(b).hexdigest()==src[h]
 assert src['retrieval']['status']==200 and src['document_identity_verified']
 assert src['law_checked_date']=='2026-11-04'
assert report['duplicate_method']['canonical_count']==439 and report['duplicate_method']['public_count']==2349
assert report['duplicate_method']['candidate_visible_records_read']==76
result=dict(stage='independent-legacy',independent_of_authors=True,auditor=report['auditor'],auditor_instance=report['auditor_instance'],actor_provenance=report['actor_provenance'],question_hashes=assignment['question_hashes'],worker_commit=worker_commit,results=[dict(question_id=r['question_id'],disposition=r['disposition'],evidence_path=report_path,evidence_sha256=hashlib.sha256(raw).hexdigest()) for r in report['records']])
validate_result(assignment,result)
job=copy.deepcopy(assignment);job['result']=result
for row in result['results']:validate_independent_evidence(job,row,report)
path=Path('/tmp/independent-phase12-c-result.json');path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(native_validate_result='PASS',native_validate_independent_evidence='PASS_40',current_canonical_record_hashes='PASS_40',source_raw_text_meta_hashes='PASS',option_findings=160,criterion_findings=400,worker_commit=worker_commit,report_sha256=hashlib.sha256(raw).hexdigest(),result_path=str(path),summary=report['summary']),ensure_ascii=False,indent=2))
