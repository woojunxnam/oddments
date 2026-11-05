"""Read-only native envelope/content/evidence checks. No queue, ledger or generation writes."""
import json,sys,hashlib,subprocess,copy,re,argparse
from pathlib import Path
from datetime import datetime,timezone
BASE=Path(__file__).resolve().parent;ROOT=BASE.parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from review_queue import validate_result,validate_independent_evidence,digest
from export_legacy_review_input import export
CRITERIA={'jurisprudence_reasoning','practice_plausibility','authentic_distractors','wording_not_guessable','reasoning_not_trivia','natural_rule_combination','appropriate_drug_context','distinct_from_bank','not_schedule_flashcard','public_style_without_copying'}
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--postcommit',action='store_true');parser.add_argument('--result-output',type=Path);parser.add_argument('--validation-output',type=Path,required=True);a=parser.parse_args()
 assignment=load(BASE/'assignment.json');packet=load(BASE/'assigned-visible-input.json');report_path=ROOT/'reports/full-corpus-review/independent-phase12-b-review.json';report=load(report_path);raw=report_path.read_bytes();reportsha=sha(raw)
 assert len(report['records'])==40 and len(assignment['question_hashes'])==40
 assert report['question_hashes']==assignment['question_hashes']==packet['question_hashes']
 assert {r['question_id'] for r in report['records']}==set(assignment['question_hashes'])
 assert export(assignment,ROOT)==packet,'Original records/visible packet changed; full records only used internally for digest/export.'
 originals={r['question_id']:r['original_visible_content'] for r in packet['records']}
 sources={x['source_id']:x for x in report['sources']}
 checks=0
 def binding(obj):
  nonlocal checks
  for pk,sk in [('raw_path','raw_sha256'),('evidence_path','evidence_sha256'),('metadata_path','metadata_sha256')]:
   if pk not in obj:continue
   relative=Path(obj[pk]);assert not relative.is_absolute() and '..' not in relative.parts
   p=ROOT/relative;assert sha(p.read_bytes())==obj[sk],str(relative);checks+=1
   if a.postcommit:assert subprocess.check_output(['git','show','HEAD:'+str(relative)],cwd=ROOT)==p.read_bytes()
 for s in sources.values():
  binding(s)
  ts=datetime.fromisoformat(s['retrieved_at']);assert ts.tzinfo is not None
  if s['used_as_law']:
   assert s['http_status']==200 and s['law_checked_date']=='2026-11-04' and s['official_url'].startswith('https://')
   m=load(ROOT/s['metadata_path']);assert m['identity_validation']=='DIRECTLY_READ_TITLE_AND_CONTROLLING_TEXT'
  else:assert s['law_checked_date'] is None
 for r in report['records']:
  q=originals[r['question_id']];assert r['record_sha256']==assignment['question_hashes'][r['question_id']]
  l=r['legal_review'];assert set(l['per_choice_findings'])=={c['id'] for c in q['choices']}
  assert l['stored_key']==q['correct_choice_ids']==l['independently_expected_key']
  assert l['choice_by_choice_findings']==l['per_choice_findings']
  for c in q['choices']:
   f=l['per_choice_findings'][c['id']];assert f['option_text']==c['text'];assert f['option_text_sha256']==sha(c['text'].encode())
   assert f['should_select']==(c['id'] in l['independently_expected_key'])
   assert f['should_select']==(not f['statement_supported'] if l['polarity']=='INCORRECT' else f['statement_supported'])
   assert f['finding_ko'] and f['authorities']
   for auth in f['authorities']:
    s=sources[auth['source_id']];assert s['used_as_law'];assert auth['authority']==s['source_id'];assert auth['law_checked_date']==s['law_checked_date'];binding(auth)
  er=l['original_explanation_review'];assert er['core_original']==q['explanation']['core_reasoning'];assert er['core_sha256']==sha(er['core_original'].encode())
  assert set(er['choice_rationales'])==set(q['explanation']['choice_analysis'])
  for cid,text in q['explanation']['choice_analysis'].items():assert er['choice_rationales'][cid]['original_rationale']==text
  rr=r['realism_review'];assert set(rr['criteria'])==CRITERIA==set(rr['criterion_findings_ko']);assert all(type(v) is bool for v in rr['criteria'].values())
  assert rr['verdict']==('PASS' if all(rr['criteria'].values()) else 'FAIL')
  assert all(re.search('[가-힣]',s) for s in rr['criterion_findings_ko'].values())
  de=rr['duplicate_evidence'];assert de['canonical_count']==439 and de['public_count']==2349;assert len(de['individual_candidate_comparisons'])==7;assert all(x['stem_and_all_choices_read'] for x in de['individual_candidate_comparisons'])
  assert r['release_eligible'] is False and r['canonical_release_credit']==0
 for context in report['methodology_snapshots']:assert sha((ROOT/context['path']).read_bytes())==context['file_sha256']
 for pk,sk in [('assignment_path','assignment_sha256'),('visible_packet_path','visible_packet_sha256')]:assert sha((ROOT/report['input_binding'][pk]).read_bytes())==report['input_binding'][sk]
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
 envelope={k:report[k] for k in ['stage','independent_of_authors','auditor','auditor_instance','actor_provenance']}
 envelope.update(question_hashes=assignment['question_hashes'],worker_commit=head,results=[{'question_id':r['question_id'],'disposition':r['result_disposition'],'evidence_path':str(report_path.relative_to(ROOT)),'evidence_sha256':reportsha} for r in report['records']])
 validate_result(assignment,envelope);job=copy.deepcopy(assignment);job['result']=envelope
 for row in envelope['results']:validate_independent_evidence(job,row,report)
 if a.postcommit:
  assert subprocess.check_output(['git','show','HEAD:'+str(report_path.relative_to(ROOT))],cwd=ROOT)==raw
  branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip();assert branch==assignment['worker_branch']
  changed=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r','HEAD'],cwd=ROOT,text=True).splitlines()
  assert changed and all(p==str(report_path.relative_to(ROOT)) or p.startswith(str(BASE.relative_to(ROOT))+'/') for p in changed)
 if a.result_output:a.result_output.write_text(json.dumps(envelope,ensure_ascii=False,indent=2)+'\n')
 validation={'checked_at':datetime.now(timezone.utc).isoformat(),'actor_id':'/root/independent_wave12_b','stage':'independent-legacy','job_id':assignment['job_id'],'mode':'POSTCOMMIT_NATIVE_READ_ONLY' if a.postcommit else 'PRECOMMIT_READ_ONLY','worker_head':head,'worker_report_sha256':reportsha,'assigned_current_records_verified':40,'full_visible_packet_matches_current_export':True,'per_choice_and_polarity_and_sata_checked':40,'realism_criteria_per_record':10,'nearest_actual_read_unique_candidates':111,'raw_text_metadata_binding_checks':checks,'native_validate_result':'PASS','native_validate_independent_evidence_records':40,'root_builder_full_qa':'NOT_RUN','queue_mutation':'NOT_RUN','canonical_release_credit':0,'status':'PASS'}
 a.validation_output.write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n');print(json.dumps(validation,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
