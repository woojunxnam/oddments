import json,hashlib,datetime,sys,subprocess,copy
from pathlib import Path
root=Path('/workspace/independent-wave14-d');sys.path.insert(0,str(root/'scripts'))
import review_queue as q
from build_full_corpus_review import validate_independent_source_bytes
from export_legacy_review_input import export
from qa_common import semantic_content_hash
out=root/'reports/full-corpus-review/phase14-d-evidence';job=json.load(open(out/'assignment.json'));packet=json.load(open(out/'assigned-visible-input.json'));rp=root/'reports/full-corpus-review/independent-phase14-d-review.json';report=json.load(open(rp));sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
fresh=export(job,root)
assert packet['records']==fresh['records'] and packet['question_hashes']==fresh['question_hashes'] and packet['job_id']==fresh['job_id']
assert set(job['question_hashes'])=={x['question_id'] for x in report['records']}
sourcecalls=0;authoritycalls=0;choicecalls=0
for d in report['sources']:
 validate_independent_source_bytes(d,root);sourcecalls+=1
 assert sha(root/d['metadata_path'])==d['metadata_sha256']
 m=json.load(open(root/d['metadata_path']));memo=json.load(open(root/d['evidence_path']))
 assert memo['retrieval_metadata']==m
 assert all(d[k]==m[k] for k in m)
 for k in ['raw_path','text_path']:assert k not in d
 for kind in ['raw','text']:
  ext='raw' if kind=='raw' else 'txt';assert sha(Path('/tmp/phase14-d-private')/(d['source_id']+'.'+ext))==d[kind+'_sha256']
 datetime.datetime.fromisoformat(d['retrieved_at']);assert d['public_raw_redistribution'] is False
 assert d['law_checked_date']=='2026-11-04'
for row in report['records']:
 assert row['record_sha256']==job['question_hashes'][row['question_id']]
 assert len(row['legal_review']['per_choice_findings'])==4
 assert len(row['legal_review']['original_explanation_review']['per_choice_explanation_findings'])==4
 assert len(row['realism_review']['criteria'])==len(row['realism_review']['criterion_findings_ko'])==10
 assert row['release_eligible'] is False
 assert row['realism_review']['duplicate_evidence']['evidence_sha256']==sha(root/row['realism_review']['duplicate_evidence']['evidence_path'])
 for a in row['legal_review']['authorities']:validate_independent_source_bytes(a,root);authoritycalls+=1;assert a['substantive_content_verified'] is True
 for c in row['legal_review']['per_choice_findings']:
  assert hashlib.sha256(c['option_text'].encode()).hexdigest()==c['option_sha256']
  for a in c['authorities']:validate_independent_source_bytes(a,root);choicecalls+=1;assert a['substantive_content_verified'] is True
for rel,kind in [('data/exam_style/mpje_style_profile.json','style_profile'),('data/blueprint.json','blueprint')]:
 o=json.load(open(root/rel));assert semantic_content_hash(o,kind)==o['content_hash'];assert sha(root/rel)==report[kind]['file_sha256']
assert len(report['records'])==40
base='f4a9661259129a94341712ad44c0f468b687d7d5'
for rel in ['reports/full-corpus-review/phase14-d-evidence/assignment.json','reports/full-corpus-review/phase14-d-evidence/assigned-visible-input.json']:
 assert subprocess.check_output(['git','show',base+':'+rel],cwd=root)==(root/rel).read_bytes()
proof=dict(checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),actor='/root/independent_wave14_d',report_sha256=sha(rp),current_original_hashes_verified=40,visible_export_rows_equal=True,packet_envelope_metadata_note="Parent packet schema_version/scope prose differ from current exporter; all40 visible rows, hashes and job_id equal",unchanged_root_input_bytes=True,strict_source_byte_validation_calls=dict(report_sources=sourcecalls,record_authorities=authoritycalls,per_choice_authorities=choicecalls),raw_text_meta_sha_verified_sources=sourcecalls,exact_40_ids=True,complete_160_choice_binding=True,style_blueprint_semantic_hashes_current=True,source_law_credit_failed_attempts=0,full_repository_QA='NOT_RUN worker scope;no loader/protected guard bypass',canonical_release_credit=0)
print(json.dumps(proof,indent=2))
if '--postcommit' in sys.argv:
 commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip();rel=rp.relative_to(root).as_posix()
 env=dict(stage='independent-legacy',independent_of_authors=True,auditor=report['auditor'],auditor_instance=report['auditor_instance'],actor_provenance=report['actor_provenance'],question_hashes=job['question_hashes'],worker_commit=commit,results=[dict(question_id=x['question_id'],disposition='INDEPENDENT_ASSESSED' if x['realism_review']['verdict']=='PASS' else 'NEEDS_REMEDIATION',evidence_path=rel,evidence_sha256=sha(rp)) for x in report['records']])
 q.validate_result(job,env);jobcopy=copy.deepcopy(job);jobcopy['result']=env
 for row in env['results']:q.validate_independent_evidence(jobcopy,row,report)
 assert subprocess.check_output(['git','show',commit+':'+rel],cwd=root)==rp.read_bytes()
 changed=subprocess.check_output(['git','diff','--name-only',base+'..'+commit],cwd=root,text=True).splitlines()
 assert changed and all(x.startswith('reports/full-corpus-review/phase14-d-evidence/') or x==rel for x in changed)
 assert not any(x.endswith('/assignment.json') or x.endswith('/assigned-visible-input.json') for x in changed)
 assert not subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True).strip()
 proof.update(worker_commit=commit,native_validate_result='PASS',native_validate_independent_evidence_rows=40,committed_report_bytes_equal=True,changed_file_count=len(changed),changed_paths_ownprefix_only=True,working_tree_clean=True,worker_commit_40hex=True,envelope_committed=False)
 Path('/tmp/independent-phase14-d-result.json').write_text(json.dumps(env,ensure_ascii=False,indent=2)+'\n')
 Path('/tmp/independent-phase14-d-postcommit-proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
 print('postcommit',json.dumps(proof,indent=2))
