"""Read-only native postcommit verification; never submits or edits a queue."""
import sys,json,hashlib,subprocess,copy
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path.cwd();sys.path.insert(0,str(ROOT/'scripts'))
import review_queue as rq
import export_legacy_review_input as exporter
B=ROOT/'reports/full-corpus-review/phase12-d-evidence';RP='reports/full-corpus-review/independent-phase12-d-review.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a])
a=json.loads((B/'assignment.json').read_text());r=json.loads((ROOT/RP).read_text());packet=json.loads((B/'assigned-visible-input.json').read_text());raw=(ROOT/RP).read_bytes();head=git('rev-parse','HEAD').decode().strip()
assert len(a['question_hashes'])==40
assert r['question_hashes']==a['question_hashes']
assert r['actor_provenance']=={'actor_id':'/root/independent_wave12_d','session_id':'/root/independent_wave12_d'}
assert r['canonical_audit'] is False and r['canonical_release_credit']==0 and r['release_eligible'] is False
assert exporter.export(a,ROOT)==packet,'native export differs from root visible packet/current full record hashes'
results=[{'question_id':x['question_id'],'disposition':x['disposition'],'evidence_path':RP,'evidence_sha256':sha(raw)} for x in r['records']]
envelope={'stage':'independent-legacy','independent_of_authors':True,'auditor':r['auditor'],'auditor_instance':r['auditor_instance'],'actor_provenance':r['actor_provenance'],'question_hashes':a['question_hashes'],'worker_commit':head,'results':results}
rq.validate_result(a,envelope)
job=copy.deepcopy(a);job['result']=envelope
for x in results:rq.validate_independent_evidence(job,x,r)
assert git('show',head+':'+RP)==raw,'worker commit/report byte mismatch'
assert git('show',head+':'+str((B/'assignment.json').relative_to(ROOT)))==(B/'assignment.json').read_bytes()
assert git('show',head+':'+str((B/'assigned-visible-input.json').relative_to(ROOT)))==(B/'assigned-visible-input.json').read_bytes()
assert len(r['records'])==40 and len({x['question_id'] for x in r['records']})==40
pd={x['question_id']:x for x in packet['records']}
for x in r['records']:
 q=pd[x['question_id']]['original_visible_content'];l=x['legal_review'];v=x['realism_review']
 assert x['record_sha256']==a['question_hashes'][x['question_id']]
 assert l['stored_key']==q['correct_choice_ids']==l['independently_expected_key']
 assert [z['option_text'] for z in l['per_choice_findings']]==[c['text'] for c in q['choices']]
 assert all(z['option_text_sha256']==sha(z['option_text'].encode()) for z in l['per_choice_findings'])
 assert {z['choice_id'] for z in l['original_explanation_review']['per_choice_findings']}==set(q['explanation']['choice_analysis'])
 assert all(z['rationale_sha256']==sha(q['explanation']['choice_analysis'][z['choice_id']].encode()) for z in l['original_explanation_review']['per_choice_findings'])
 assert len(v['criteria'])==10 and set(v['criteria'])==set(v['criterion_findings_ko'])
 assert all(isinstance(y,bool) for y in v['criteria'].values()) and all(v['criterion_findings_ko'].values())
 assert (v['verdict']=='PASS')==all(v['criteria'].values())
 assert x['release_eligible'] is False and x['canonical_release_credit']==0
 assert v['duplicate_evidence']['canonical_count']==439 and v['duplicate_evidence']['public_count']==2349
refs={}
for s in r['sources']+r['style_sources']:
 for pk,hk in [('evidence_path','evidence_sha256'),('text_path','text_sha256'),('metadata_path','metadata_sha256')]:
  p=s[pk];expected=s[hk];assert sha((ROOT/p).read_bytes())==expected,p
  assert git('show',head+':'+p)==(ROOT/p).read_bytes(),p
  refs[p]=expected
 m=json.loads((ROOT/s['metadata_path']).read_text());assert m['http_status']==200 and m['retrieval_success'] is True
 for k in ('started_at','completed_at'):assert datetime.fromisoformat(m[k]).tzinfo is not None
 if s in r['sources']:
  assert s['law_checked_date']==m['completed_at'][:10]
  assert s['source_id'] not in ('ma-pmp-gaba','ma-pmp-guide')
for m in r['methodology']:
 assert sha((ROOT/m['snapshot_path']).read_bytes())==m['file_sha256']
 assert sha((ROOT/m['path']).read_bytes())==m['file_sha256']
changed=git('diff-tree','--no-commit-id','--name-only','-r',head).decode().splitlines()
assert all(p==RP or p.startswith('reports/full-corpus-review/phase12-d-evidence/') for p in changed),changed
assert not any(p.endswith('ma-pmp-guide.pdf') or p.endswith('ma-pmp-guide.txt') for p in git('ls-tree','-r','--name-only',head,'reports/full-corpus-review/phase12-d-evidence').decode().splitlines())
assert len(json.loads((B/'nearest-visible-candidates.json').read_text())['unique_candidates'])==100
out=Path('/tmp/independent-phase12-d-result.json');out.write_text(json.dumps(envelope,ensure_ascii=False,indent=2)+'\n')
att={'stage':'independent-legacy','actor_id':r['actor_provenance']['actor_id'],'validated_at':datetime.now(timezone.utc).isoformat(),'worker_commit':head,'report_path':RP,'report_sha256':sha(raw),'assigned_count':40,'source_or_style_ref_files_verified':len(refs),'native_result_validation':'PASS','native_per_record_evidence_validation':'PASS','native_current_full_record_hash_and_visible_packet_validation':'PASS','git_worker_report_byte_validation':'PASS','immutable_assignment_packet_validation':'PASS','per_choice_and_rationale_hashes_validation':'PASS','ten_criteria_and_nearest_439_2349_validation':'PASS','committed_source_hash_and_aware_timestamp_validation':'PASS','vendor_restricted_raw_exclusion':'PASS','changes_confined_to_own_evidence_and_report':'PASS','canonical_release_credit':0,'result_envelope_path':str(out),'result_envelope_sha256':sha(out.read_bytes()),'full_repository_QA':'NOT_RUN_ROOT_INTEGRATOR_SCOPE'}
Path('/tmp/independent-phase12-d-postcommit-validation.json').write_text(json.dumps(att,ensure_ascii=False,indent=2)+'\n');print(json.dumps(att,ensure_ascii=False,indent=2))
