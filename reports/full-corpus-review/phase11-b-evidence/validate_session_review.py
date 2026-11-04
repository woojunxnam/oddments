import json,pathlib,sys,hashlib,datetime,subprocess
BASE=pathlib.Path(__file__).resolve().parent;ROOT=BASE.parents[2];sys.path.insert(0,str(ROOT/'scripts'))
import review_queue as queue
from export_legacy_review_input import export
from build_full_corpus_review import validate_independent_source_bytes
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report_path=ROOT/'reports/full-corpus-review/independent-phase11-b-review.json';report=json.loads(report_path.read_bytes());assignment=json.loads((BASE/'assignment.json').read_bytes())
checks={}
def check(name,value):
 if not value:raise AssertionError(name)
 checks[name]='PASS'
check('native_current_original_hashes_and_visible_whitelist',export(assignment,ROOT)==json.loads((BASE/'assigned-visible-input.json').read_bytes())==json.loads((BASE/'reexported-visible-input.json').read_bytes()))
queue.validate_independent_provenance(assignment,report);checks['native_independent_actor_provenance']='PASS'
check('exact40_unique_ids_hashes',len(report['records'])==40 and len({r['question_id'] for r in report['records']})==40 and {r['question_id']:r['record_sha256'] for r in report['records']}==assignment['question_hashes']==report['question_hashes'])
check('no_canonical_or_author_credit',report['canonical_audit'] is False and report['canonical_release_credit']==0 and report['author_review_credit']==0)
check('retained_progress_context_exact_binding',sha(ROOT/report['progress_binding']['path'])==report['progress_binding']['sha256'] and 'phase11-b-evidence/context/' in report['progress_binding']['path'])
by_source={s['source_id']:s for s in report['sources']}
for source in report['sources']:
 validate_independent_source_bytes(source,ROOT)
 check('metadata_'+source['source_id'],sha(ROOT/source['retrieval_metadata_path'])==source['retrieval_metadata_sha256'])
 meta=json.loads((ROOT/source['retrieval_metadata_path']).read_bytes())
 check('actual_URL_'+source['source_id'],source['official_url']==meta['official_url'])
 check('aware_timestamp_'+source['source_id'],datetime.datetime.fromisoformat(meta['retrieved_at']).utcoffset() is not None)
 if source['used_as_law']:
  check('successful_law_body_'+source['source_id'],meta['http_status']==200 and meta.get('successful_primary_retrieval') is True and source['law_checked_date']==report['reviewed_at'])
for r in report['records']:
 visible=next(q['original_visible_content'] for q in json.loads((BASE/'assigned-visible-input.json').read_bytes())['records'] if q['question_id']==r['question_id'])
 f=r['legal_review']['per_choice_findings'];criteria=r['realism_review']['criteria'];qid=r['question_id']
 check('all_options_and_10criteria_'+qid,set(f)=={c['id'] for c in visible['choices']} and len(criteria)==10 and set(criteria)==set(r['realism_review']['criterion_findings_ko']))
 check('pass_iff_all10_'+qid,all(criteria.values())==(r['realism_review']['verdict']=='PASS'))
 check('all_choice_texts_bound_'+qid,all(f[c['id']]['option_text']==c['text'] and f[c['id']]['option_text_sha256']==hashlib.sha256(c['text'].encode()).hexdigest() for c in visible['choices']))
 for c in f.values():
  for a in c['authorities']:
   validate_independent_source_bytes(a,ROOT)
   check('used_source_'+a['authority'],by_source[a['authority']]['used_as_law'])
 if r['legal_review']['existing_answer_correct']=='YES':
  independent=[k for k,v in f.items() if (v['statement_supported'] is False if r['legal_review']['polarity']=='INCORRECT' else v['statement_supported'] is True)]
  check('independent_polarity_and_stored_key_'+qid,independent==r['legal_review']['independently_expected_key']==visible['correct_choice_ids'])
 check('actual_duplicate_comparison_'+qid,all(r['realism_review']['duplicate_evidence'][k]['stem_and_all_options_directly_read'] for k in ['canonical_lexical_closest_comparison','canonical_topic_comparison','public_closest_comparison']))
check('ambiguous_scope_not_suppressed',[r['question_id'] for r in report['records'] if r['legal_review']['existing_answer_correct']=='AMBIGUOUS']==['MA-EXP-0273','MA-EXP-0276'])
check('source_failed_attempt_not_credited',not by_source['21usc822']['used_as_law'] and by_source['21usc822']['http_status']==404)
check('NABP_no_raw_retained',all('raw_path' not in s for s in report['sources'] if s['source_id'].startswith('nabp-')))
check('default_projection_empty',report['progress_binding']['assigned_default_ids']==json.loads((BASE/'context/default-ids-at-assignment.json').read_bytes())['assignment_default_ids']==[])
check('change_scope_only_assigned_report_evidence',all(p.startswith('reports/full-corpus-review/phase11-b-evidence/') or p=='reports/full-corpus-review/independent-phase11-b-review.json' for p in subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).splitlines() for p in [p[3:].rstrip('/')]))
out={'verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'report_path':str(report_path.relative_to(ROOT)),'report_sha256':sha(report_path),'method':'Native export_legacy_review_input.export, review_queue.validate_independent_provenance, build_full_corpus_review.validate_independent_source_bytes plus per-choice/polarity/criteria/path assertions. No shared state or generated artifacts written.','checks':checks,'summary':report['summary'],'queue_submit':'NOT_RUN_ROOT_ONLY','canonical_release':'NOT_RUN_NO_CREDIT'}
(BASE/'validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print('PASS',len(checks),'checks',out['report_sha256'])
