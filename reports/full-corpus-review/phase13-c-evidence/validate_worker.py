import json,hashlib,subprocess,sys,copy
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[3];E=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'scripts'))
import review_queue as q
from build_full_corpus_review import validate_independent_source_bytes
H=lambda b:hashlib.sha256(b).hexdigest()
report_path='reports/full-corpus-review/independent-phase13-c-review.json';report=json.loads((R/report_path).read_text());job=json.loads((E/'assignment.json').read_text());packet=json.loads((E/'assigned-visible-input.json').read_text());sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip();assert len(sha)==40
raw=(R/report_path).read_bytes();assert subprocess.check_output(['git','show',sha+':'+report_path],cwd=R)==raw
assert report['actor_provenance']=={'actor_id':'/root/independent_wave13_c','session_id':'/root/independent_wave13_c'}
assert report['canonical_release_credit']==0 and report['canonical_audit'] is False and report['release_eligible'] is False
assert len(report['records'])==40 and report['question_hashes']==job['question_hashes']==packet['question_hashes']
assert {x['question_id']:x['record_sha256'] for x in report['records']}==job['question_hashes']
for row in packet['records']:assert q.digest(row['original_visible_content'])==row['visible_content_sha256']
config=json.loads((R/'site/practice-expansion/publication.json').read_text());paths=['practice_expansion/2026-10-23/candidates/questions.json']+[x['path'] for x in config['additional_banks']]
originals={x['question_id']:x for path in paths for x in json.loads((R/path).read_text())['questions'] if x['question_id'] in job['question_hashes']}
assert {k:q.digest(v) for k,v in originals.items()}==job['question_hashes']
for source in report['sources']:
 validate_independent_source_bytes(source,R)
 mp=R/source['metadata_path'];assert H(mp.read_bytes())==source['metadata_sha256']
 assert subprocess.check_output(['git','show',sha+':'+source['metadata_path']],cwd=R)==mp.read_bytes()
 ev=R/source['evidence_path'];assert subprocess.check_output(['git','show',sha+':'+source['evidence_path']],cwd=R)==ev.read_bytes()
 if source.get('public_raw_redistribution'):
  rp=R/source['raw_path'];assert subprocess.check_output(['git','show',sha+':'+source['raw_path']],cwd=R)==rp.read_bytes()
 else:
  # Private original is verified locally, not claimed to be a committed public payload.
  assert H(Path(source['raw_path']).read_bytes())==source['raw_sha256']
  assert H(Path(source['private_text_path']).read_bytes())==source['text_sha256']
allowed={'reports/full-corpus-review/independent-phase13-c-review.json'}
changed=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r',sha],cwd=R,text=True).splitlines()
assert all(x in allowed or x.startswith('reports/full-corpus-review/phase13-c-evidence/') for x in changed)
assert not any(x.endswith('/assignment.json') or x.endswith('/assigned-visible-input.json') for x in changed)
assert subprocess.check_output(['git','status','--porcelain'],cwd=R,text=True)==''
results=[]
for row in report['records']:
 disposition='INDEPENDENT_ASSESSED' if row['legal_review']['verdict']=='KEEP' and row['realism_review']['verdict']=='PASS' else 'NEEDS_REMEDIATION'
 results.append(dict(question_id=row['question_id'],disposition=disposition,evidence_path=report_path,evidence_sha256=H(raw)))
envelope={k:report[k] for k in ['stage','independent_of_authors','auditor','auditor_instance','actor_provenance','canonical_audit','canonical_release_credit']};envelope.update(question_hashes=job['question_hashes'],worker_commit=sha,results=results)
q.validate_result(job,envelope);j=copy.deepcopy(job);j['result']=envelope
for row in envelope['results']:q.validate_independent_evidence(j,row,report)
envpath=Path('/tmp/independent-phase13-c-result.json');envpath.write_text(json.dumps(envelope,ensure_ascii=False,indent=2)+'\n')
proof={'stage':'independent-legacy','validated_at':datetime.now(timezone.utc).isoformat(),'worker_commit':sha,'report_path':report_path,'report_sha256':H(raw),'assignment_question_count':40,'whole_current_original_hashes':'PASS','committed_report_and_source_raw_text_metadata_hashes':'PASS','private_copyrighted_original_and_text_hashes':'PASS_LOCAL_NOT_PUBLIC_COMMIT','q.validate_result':'PASS','q.validate_independent_evidence':'PASS_40','own_paths_only':'PASS','root_inputs_unchanged_in_worker_commit':'PASS','clean_worktree':'PASS','canonical_release_credit':0,'envelope_path':str(envpath),'envelope_sha256':H(envpath.read_bytes()),'whole_repository_qa':'NOT_RUN_WORKER_SCOPE_ROOT_OWNS_INTEGRATION'}
proofpath=Path('/tmp/independent-phase13-c-postcommit-validation.json');proofpath.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps(proof,ensure_ascii=False,indent=2))
