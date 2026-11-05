"""Actual native postcommit validation; result envelope/proof stay outside Git."""
from pathlib import Path
from datetime import datetime, timezone
import copy, hashlib, json, subprocess, sys
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
import review_queue as q
import build_full_corpus_review as b
def sha(x):return hashlib.sha256(x).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args],text=True).strip()
def main():
 report_path='reports/full-corpus-review/independent-phase14-a-review.json';report_bytes=(ROOT/report_path).read_bytes();report=load(ROOT/report_path)
 job=load(OUT/'assignment.json');packet=load(OUT/'assigned-visible-input.json');head=git('rev-parse','HEAD');base='f4a9661259129a94341712ad44c0f468b687d7d5'
 assert len(head)==40 and git('branch','--show-current')==job['worker_branch']
 assert git('merge-base',base,head)==base
 status=git('status','--porcelain');assert status=='',status
 assert subprocess.check_output(['git','-C',str(ROOT),'show',head+':'+report_path])==report_bytes
 assert report['scope']['assignment_sha256']==sha((OUT/'assignment.json').read_bytes())
 assert report['scope']['visible_packet_sha256']==sha((OUT/'assigned-visible-input.json').read_bytes())
 assert set(job['question_hashes'])==set(r['question_id'] for r in report['records']) and len(report['records'])==40
 config=load(ROOT/'site/practice-expansion/publication.json');paths=['practice_expansion/2026-10-23/candidates/questions.json']+[a['path'] for a in config['additional_banks']]
 current={r['question_id']:r for p in paths for r in load(ROOT/p)['questions']}
 assert all(q.digest(current[qid])==h for qid,h in job['question_hashes'].items())
 for r in report['records']:
  v=next(x for x in packet['records'] if x['question_id']==r['question_id'])['original_visible_content']
  assert r['record_sha256']==job['question_hashes'][r['question_id']]
  assert r['read_scope']['all_choices']==[c['id'] for c in v['choices']]
  assert [c['choice_id'] for c in r['legal_review']['choice_by_choice_findings']]==[c['id'] for c in v['choices']]
  assert r['legal_review']['stored_key']==v['correct_choice_ids']
  assert r['legal_review']['original_explanation_review']['visible_explanation_sha256']==q.digest(v['explanation'])
  assert len(r['realism_review']['criteria'])==10 and set(r['realism_review']['criteria'])==set(r['realism_review']['criterion_findings_ko'])
  assert (r['realism_review']['verdict']=='PASS')==all(r['realism_review']['criteria'].values())
  assert r['release_eligible'] is False
 sources=list(report['sources'])
 for r in report['records']:
  sources.extend(r['legal_review']['authorities'])
  for c in r['legal_review']['choice_by_choice_findings']:sources.extend(c['authorities'])
 for a in sources:
  b.validate_independent_source_bytes(a,ROOT)
  if 'metadata_path' in a:assert sha((ROOT/a['metadata_path']).read_bytes())==a['metadata_sha256']
 rawmetas=0
 for p in (OUT/'sources').glob('*.meta.json'):
  m=load(p)
  if m['status']==200:
   assert sha((ROOT/m['raw_path']).read_bytes())==m['raw_sha256']
   assert sha((ROOT/m['evidence_path']).read_bytes())==m['evidence_sha256']==m['text_sha256'];rawmetas+=1
 nabp=next(a for a in report['sources'] if a['source_id']=='nabp-public-sample-style')
 assert sha(Path('/tmp/independent-phase14-a-nabp-sample.pdf').read_bytes())==nabp['raw_sha256']
 assert sha(Path('/tmp/independent-phase14-a-nabp-sample.txt').read_bytes())==nabp['private_text_sha256']
 envelope={'stage':'independent-legacy','independent_of_authors':True,'auditor':report['auditor'],'auditor_instance':report['auditor_instance'],'actor_provenance':report['actor_provenance'],'question_hashes':job['question_hashes'],'worker_commit':head,'results':[{'question_id':r['question_id'],'disposition':r['disposition'],'evidence_path':report_path,'evidence_sha256':sha(report_bytes)} for r in report['records']]}
 q.validate_result(job,envelope)
 j=copy.deepcopy(job);j['result']=envelope
 for row in envelope['results']:q.validate_independent_evidence(j,row,report)
 changed=git('diff','--name-only',base,head).splitlines();prefix='reports/full-corpus-review/phase14-a-evidence/'
 assert all(p==report_path or p.startswith(prefix) for p in changed)
 assert not any('nabp' in p.lower() and p.endswith(('.pdf','.txt','.html')) for p in changed)
 proof={'verified_at':datetime.now(timezone.utc).isoformat(),'worker_commit':head,'branch':job['worker_branch'],'base_commit':base,'report_path':report_path,'report_sha256':sha(report_bytes),'native_validate_result':'PASS','native_validate_independent_evidence_rows':40,'strict_validate_independent_source_bytes_calls':len(sources),'strict_source_bytes':'PASS','raw_text_meta_successful_retrievals_checked':rawmetas,'current_original_record_hashes_checked':40,'source_binding_and_metadata_hashes':'PASS','assignment_and_packet_hashes':'PASS','report_matches_git_show_HEAD':'PASS','changed_paths':changed,'only_owned_prefix_and_report_changed':'PASS','worktree_status':status,'clean':'PASS','full_loader_protected_qa':'NOT_RUN; sparse tree excludes full immutable preimage; native qrow/source checks used without validator weakening','summary':report['summary'],'canonical_audit':False,'canonical_release_credit':0,'release_eligible':False}
 ep=Path('/tmp/independent-phase14-a-result.json');pp=Path('/tmp/independent-phase14-a-postcommit-proof.json');ep.write_text(json.dumps(envelope,ensure_ascii=False,indent=2)+'\n');pp.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in proof.items() if k!='changed_paths'},ensure_ascii=False,indent=2));print('envelope',ep,'proof',pp)
if __name__=='__main__':main()
