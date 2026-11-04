import json,hashlib,sys,subprocess,copy
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path('/workspace/independent-final26');sys.path.insert(0,str(ROOT/'scripts'))
import review_queue as q
from build_full_corpus_review import validate_independent_source_bytes
from export_legacy_review_input import export
P='reports/full-corpus-review/independent-final26-review.json';E='reports/full-corpus-review/final26-evidence/'
sha=lambda b:hashlib.sha256(b).hexdigest()
report=json.loads((ROOT/P).read_bytes());job=json.loads((ROOT/(E+'assignment.json')).read_bytes());packet=json.loads((ROOT/(E+'assigned-visible-input.json')).read_bytes())
phase=sys.argv[1];worker=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert export(job,ROOT)==packet,'Current actual full-object SHA/visible packet differs'
assert len(report['records'])==26 and {r['question_id']:r['record_sha256'] for r in report['records']}==job['question_hashes']
assert report['question_hashes']==job['question_hashes']
authorities=list(report['sources'])
for r in report['records']:
 authorities+=r['legal_review']['authorities']
 for c in r['legal_review']['choice_by_choice_findings']:authorities+=c['authorities']
for a in authorities:
 validate_independent_source_bytes(a,ROOT)
 for pk,hk in [('text_path','text_sha256'),('metadata_path','metadata_sha256')]:
  if pk in a:assert sha((ROOT/a[pk]).read_bytes())==a[hk],pk
 assert a['evidence_path'] and a['evidence_sha256']
 assert not any(k in a and a[k] is None for k in ['raw_path','text_path'])
results=[dict(question_id=r['question_id'],disposition=r['disposition'],evidence_path=P,evidence_sha256=sha((ROOT/P).read_bytes()))for r in report['records']]
result={k:report[k] for k in ['stage','independent_of_authors','auditor','auditor_instance','actor_provenance']};result.update(question_hashes=job['question_hashes'],worker_commit=worker,results=results)
q.validate_result(job,result);q.validate_independent_provenance(job,result)
j=copy.deepcopy(job);j['result']=result
for row in results:q.validate_independent_evidence(j,row,report)
for r in report['records']:
 assert len(r['legal_review']['choice_by_choice_findings']) in [4,5]
 assert len(r['realism_review']['criteria'])==10 and len(r['realism_review']['criterion_findings_ko'])==10
 assert (r['realism_review']['verdict']=='PASS')==all(r['realism_review']['criteria'].values())
 assert r['legal_review']['stored_key']==r['legal_review']['independently_expected_key']
 assert r['release_eligible'] is False
assert report['canonical_audit'] is False and report['canonical_release_credit']==0
# Restrict all tracked/untracked mutations to own report/evidence paths.
status=subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],cwd=ROOT,text=True)
for line in status.splitlines():
 path=line[3:];assert path==P or path.startswith(E),path
if phase=='postcommit':
 assert not status,'Worktree not clean'
 for p in [P]+[a[k] for a in authorities for k in ['evidence_path','raw_path','text_path','metadata_path'] if k in a]:
  assert subprocess.check_output(['git','show','HEAD:'+p],cwd=ROOT)==(ROOT/p).read_bytes(),p
 changed=subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r','HEAD'],cwd=ROOT,text=True).splitlines()
 assert changed and all(p==P or p.startswith(E) for p in changed)
else:changed=[]
evidence=dict(phase=phase,checked_at=datetime.now(timezone.utc).isoformat(),worker_commit=worker,actual_full_record_hashes_verified=26,visible_packet_equality=True,strict_source_byte_calls=len(authorities),top_level_source_count=len(report['sources']),each_legal_authorities_checked=True,each_choice_authorities_checked=True,native_validate_result='PASS',native_validate_provenance='PASS',native_validate_each26_evidence='PASS',report_sha256=sha((ROOT/P).read_bytes()),own_range_verified=True,worktree_clean=(status==''),head_raw_and_source_bytes_verified=phase=='postcommit',changed_paths=changed)
target=ROOT/(E+'precommit-validation.json') if phase=='precommit' else Path('/tmp/independent-final26-postcommit-validation.json');target.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n')
if phase=='postcommit':Path('/tmp/independent-final26-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(evidence,ensure_ascii=False))
