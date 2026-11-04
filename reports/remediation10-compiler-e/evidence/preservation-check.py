import sys,json,subprocess,hashlib
from pathlib import Path
root=Path('/workspace/remediation10-compiler-e');sys.path.insert(0,str(root/'scripts'))
import remediation_batch_registry as b
base='4e5f150cc60908386d52fdbaeaae33351a1a5144'
expected={'scripts/build_full_corpus_review.py','scripts/build_representative_audit_ledger.py','scripts/build_representative_rewrites.py','scripts/publish_practice.py','scripts/remediation_author_reviews.py','scripts/review_queue.py','tests/test_sata_remediation_candidates.py','tests/test_remediation_author_reviews.py','tests/test_full_corpus_review.py'}
changed=subprocess.check_output(['git','-C',str(root),'diff','--name-status',base,'HEAD'],text=True).splitlines()
modified={line.split('\t')[1] for line in changed if line.startswith('M\t')}
assert modified==expected and all(line[0] in {'M','A'} for line in changed)
a=b.allocation(root);old=b.read(root,b.OLD_ALLOCATION);bank=b.read(root,b.BASE+'/questions.json')
byid={q['question_id']:q for q in bank['questions']}
assert len(byid)==77
for q,h in a['prior_representative_question_hashes'].items():assert b.digest(byid[q])==h
for sid,h in a['prior_representative_source_hashes'].items():assert b.digest(bank['sources'][sid])==h
assert len(old['representative_question_hashes'])==74 and len(old['representative_source_hashes'])==81
for q,h in old['representative_question_hashes'].items():assert b.digest(byid[q])==h
for sid,h in old['representative_source_hashes'].items():assert b.digest(bank['sources'][sid])==h
paths=[*b.PUBLIC_BANKS,'reports/full-corpus-review/work-queue.json','reports/full-corpus-review/independent-legacy-work-queue.json','reports/full-corpus-review/independent-notes-work-queue.json','site/practice-expansion/publication.json','notes/guide.json','docs/RELEASE_POLICY.md','docs/AUDIT_WORKFLOW.md','docs/SOURCE_USE_POLICY.md','docs/QUESTION_AUTHORING_STANDARD.md']
raws={}
for p in paths:
 before=subprocess.check_output(['git','-C',str(root),'show',base+':'+p]);now=(root/p).read_bytes();assert before==now;raws[p]=b.sha(now)
payload=b.authoring_payload(root);primary_paths={s['raw_path'] for s in payload['sources'].values()}
primary_hashes={s['raw_sha256'] for s in payload['sources'].values()}
queue=b.read(root,'reports/full-corpus-review/work-queue.json');iq=b.read(root,'reports/full-corpus-review/independent-legacy-work-queue.json')
assert len(queue['jobs'])==53 and len(iq['jobs'])==37
result=dict(stage='ENGINEERING_SOURCE_PRESERVATION_NOT_LEGAL_REVIEW',base_commit=base,code_commit=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip(),existing_modified_paths=sorted(modified),unmodified_source_raw_sha256s=raws,stored_questions_unchanged=2349,old_representative_objects_unchanged=77,old_historical_rewrite_objects_unchanged=74,old_representative_sources_unchanged=90,old_historical_sources_unchanged=81,old_allocation_raw_sha256=b.sha((root/b.OLD_ALLOCATION).read_bytes()),new_registry_raw_sha256=b.sha((root/b.REGISTRY).read_bytes()),new_allocation_raw_sha256=b.sha((root/b.ALLOCATION).read_bytes()),new_authoring_raw_sha256=b.sha((root/b.AUTHORING).read_bytes()),new_current_id_baseline_raw_sha256=b.sha((root/b.CURRENT_BASELINE).read_bytes()),new_full_record_hashes=b.current_baseline(root)['candidate_question_hashes'],native_author_jobs=53,native_independent_jobs=37,new_native_author_and_independent_jobs_registered_by_worker=0,new_authority_records=len(payload['sources']),new_used_G_primary_raw_paths=len(primary_paths),new_used_G_unique_primary_payload_hashes=len(primary_hashes),retained_G_F_source_files=len(b.read(root,b.RETENTION)['files']),all40_options_and_Korean_findings_literal=True,old8_v1_plus_new2_v2=True,source_capture_dates_preserved=True,history_migration=False,shared_generated_or_queue_or_publication_writes=False,new_author_review_credit=0,new_independent_review_credit=0,canonical_release_credit=0,public_activation=False)
p=root/'reports/remediation10-compiler-e/evidence/preservation.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b.encoded(result));print(json.dumps({k:v for k,v in result.items() if k not in ('unmodified_source_raw_sha256s','new_full_record_hashes')},indent=2))
