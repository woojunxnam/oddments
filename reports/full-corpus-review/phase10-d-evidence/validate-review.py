"""Read-only exact-scope/byte/record validator; does not grant release credit."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys,subprocess
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
import review_queue as queue
from build_full_corpus_review import validate_independent_source_bytes
base=ROOT/'reports/full-corpus-review/phase10-d-evidence'
report_path=ROOT/'reports/full-corpus-review/independent-phase10-d-review.json'
report=json.loads(report_path.read_text())
assignment=json.load(open('/tmp/independent-phase10-d-assignment.json'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def require(v,msg):
 if not v:raise ValueError(msg)
require(report['stage']=='independent-legacy','stage')
require(report['question_hashes']==assignment['question_hashes'],'assignment exact hashes')
require(report['canonical_audit'] is False and report['canonical_release_credit']==0 and report['author_review_credit']==0,'credits')
queue.validate_independent_provenance(assignment,report)
job=dict(assignment,result={k:report[k] for k in ['actor_provenance','auditor','auditor_instance']})
packet=json.loads((base/'assigned-visible-input.json').read_text())
pby={q['question_id']:q for q in packet['records']}
ledger=queue.read_ledger(ROOT)
require(len(report['records'])==40 and {r['question_id'] for r in report['records']}==set(assignment['question_hashes']),'exact40')
checks=0
for r in report['records']:
 qid=r['question_id'];q=pby[qid]
 require(queue.current_hash(ROOT,ledger[qid])==assignment['question_hashes'][qid],'current underlying record '+qid)
 queue.validate_independent_evidence(job,{'question_id':qid},report)
 opts=r['legal_review']['option_reviews']
 require([x['choice_id'] for x in opts]==[x['id'] for x in q['choices']],'option exact order '+qid)
 require([x['text'] for x in opts]==[x['text'] for x in q['choices']],'visible all option text '+qid)
 require(r['original_reading']['input_sha256']==sha(base/'assigned-visible-input.json'),'input SHA '+qid)
 require(r['legal_review']['stored_choice_ids']==q['correct_choice_ids'],'stored key '+qid)
 require(r['legal_review']['existing_explanation_review']['core_reasoning_read']==q['explanation']['core_reasoning'],'original KO core '+qid)
 require(r['legal_review']['existing_explanation_review']['learning_boundary_read']==q['explanation']['learning_boundary'],'original boundary '+qid)
 for o in opts:
  require(o['finding_ko'] and o['authorities'],'individual option authority '+qid)
  require(o['existing_ko_rationale']==q['explanation']['choice_analysis'][o['choice_id']],'all original KO distractors '+qid)
  for a in o['authorities']:
   validate_independent_source_bytes(a,ROOT)
   src=report['source_index'][a['source_id']]
   require(a['official_url']==src['official_url'],'official URL/source binding '+qid)
   require(a['raw_path']==src['raw_path'] and a['raw_sha256']==src['raw_sha256'],'retained primary binding '+qid)
   m=json.loads((ROOT/a['metadata_path']).read_text())
   require(sha(ROOT/a['metadata_path'])==a['metadata_sha256'],'retrieval meta hash '+qid)
   require(m['http_status']==200 and m['legal_payload_confirmed'] is True and m['document_identity_confirmed'] is True,'real legal payload '+qid)
   require(m['official_url']==a['official_url'] and m['raw_sha256']==a['raw_sha256'],'retrieval metadata exact source '+qid)
   require(sha(ROOT/a['text_evidence_path'])==a['text_sha256'],'extracted text '+qid)
   for k in ['retrieved_at','read_at']:
    require(datetime.fromisoformat(a[k]).tzinfo is not None,'aware timestamp '+qid)
  checks+=1
 if r['legal_review']['existing_answer_correct']=='YES':
  neg='INCORRECT' in q['stem']
  expected=[o['choice_id'] for o in opts if (o['statement_truth']=='FALSE' if neg else o['statement_truth']=='TRUE')]
  require(expected==r['legal_review']['expected_choice_ids']==q['correct_choice_ids'],'manual truth -> polarity -> exact key '+qid)
 else:require(r['legal_review']['verdict']=='HOLD' and r['legal_review']['blocker'],'ambiguous hold '+qid)
 require(r['realism_review']['finding_ko'] and r['realism_review']['nearby_items_directly_read_stem_and_all_choices'],'separate actual realism '+qid)
 if r['realism_review']['verdict']=='PASS':require(all(r['realism_review']['criteria'].values()),'all PASS criteria '+qid)
for source in report['sources']:
 validate_independent_source_bytes(source,ROOT)
 require(sha(ROOT/source['metadata_path'])==source['metadata_sha256'],'source metadata SHA')
 if source.get('text_evidence_path'):require(sha(ROOT/source['text_evidence_path'])==source['text_sha256'],'top source text SHA')
for b in [report['input_binding'],report['source_index_binding'],report['style_evidence']]:require(sha(ROOT/b['path'])==b['raw_sha256'],'top evidence binding')
# The result is created after the real commit. At that point validate_result uses the actual 40-character commit, never a fabricated committed placeholder.
result_path=Path('/tmp/independent-phase10-d-result.json')
result_checked=False
if result_path.exists():
 result=json.loads(result_path.read_text());queue.validate_result(assignment,result)
 require(result['worker_commit']==subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'actual worker HEAD')
 require(all(x['evidence_sha256']==sha(report_path) for x in result['results']),'actual report SHA in envelope')
 result_checked=True
receipt={'checked_at':datetime.now(timezone.utc).isoformat(),'status':'PASS','report_path':str(report_path.relative_to(ROOT)),'report_sha256':sha(report_path),'exact_records':40,'all_options':checks,'source_records':len(report['sources']),'native_validate_independent_evidence':'PASS for all40','native_validate_independent_source_bytes':'PASS for all retained primary/format sources and each option authority','native_validate_result':'PASS with actual worker HEAD' if result_checked else 'Deferred until post-commit actual result envelope exists','canonical_release_credit':0,'author_review_credit':0}
print(json.dumps(receipt,ensure_ascii=False,indent=2))
