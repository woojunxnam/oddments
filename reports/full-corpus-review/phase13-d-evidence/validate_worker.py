"""Read-only native result/evidence/current-content/postcommit proof for phase13-d.
This is a scoped audit submission check, not whole-repository QA or release credit.
"""
import copy,datetime,hashlib,json,pathlib,subprocess,sys
B=pathlib.Path(__file__).resolve().parent;R=B.parents[2];P=B.relative_to(R).as_posix()
sys.path.insert(0,str(R/'scripts'))
import review_queue as q
from export_legacy_review_input import export
from build_full_corpus_review import validate_independent_source_bytes
REPORT='reports/full-corpus-review/independent-phase13-d-review.json'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(R),*args]).decode().strip()
def committed(path):
 raw=(R/path).read_bytes();stored=subprocess.check_output(['git','-C',str(R),'show','HEAD:'+path]);assert raw==stored,path;return raw
assignment=json.load(open(B/'assignment.json'));packet=json.load(open(B/'assigned-visible-input.json'));report=json.load(open(R/REPORT))
exported=export(assignment,root=R)
assert exported['records']==packet['records'] and exported['question_hashes']==packet['question_hashes'] and exported['job_id']==packet['job_id'] and exported['stage']==packet['stage'],'Current original content or visible projection changed'
assert packet['schema_version']==1,'Expected root packet v1 envelope; exported payload records must still match exactly'
assert report['question_hashes']==assignment['question_hashes']
assert {r['question_id'] for r in report['records']}==set(assignment['question_hashes']) and len(report['records'])==40
assert report['actor_provenance']=={'actor_id':'/root/independent_wave13_d','session_id':'/root/independent_wave13_d'}
assert report['canonical_release_credit']==0 and report['canonical_audit'] is False and report['release_eligible'] is False
report_sha=sha((R/REPORT).read_bytes());commit=git('rev-parse','HEAD')
rows=[]
for r in report['records']:
 assert r['record_sha256']==assignment['question_hashes'][r['question_id']]
 assert len(r['realism_review']['criteria'])==10 and len(r['realism_review']['criterion_findings_ko'])==10
 assert all(r['realism_review']['criterion_findings_ko'].values())
 assert r['realism_review']['verdict']!='PASS' or all(r['realism_review']['criteria'].values())
 inp=next(x for x in packet['records'] if x['question_id']==r['question_id'])['original_visible_content']
 assert set(r['legal_review']['choice_by_choice_findings'])=={c['id'] for c in inp['choices']}
 for c in inp['choices']:
  f=r['legal_review']['choice_by_choice_findings'][c['id']];assert f['option_text']==c['text'] and f['option_text_sha256']==sha(c['text'].encode())
 disposition='HOLD' if r['legal_review']['verdict']=='HOLD' else 'NEEDS_REMEDIATION' if r['legal_review']['verdict']!='KEEP' or r['realism_review']['verdict']!='PASS' else 'INDEPENDENT_ASSESSED'
 rows.append({'question_id':r['question_id'],'disposition':disposition,'evidence_path':REPORT,'evidence_sha256':report_sha})
envelope={'stage':'independent-legacy','independent_of_authors':True,'auditor':report['auditor'],'auditor_instance':report['auditor_instance'],'actor_provenance':report['actor_provenance'],'canonical_audit':False,'canonical_release_credit':0,'release_eligible':False,'question_hashes':assignment['question_hashes'],'worker_commit':commit,'results':rows}
q.validate_result(assignment,envelope)
job=copy.deepcopy(assignment);job['result']=envelope
for row in rows:q.validate_independent_evidence(job,row,report)
proof={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'postcommit':('--postcommit' in sys.argv),'worker_commit':commit,'worker_branch':git('branch','--show-current'),'report_path':REPORT,'report_sha256':report_sha,'native_validate_result':'PASS','native_validate_independent_evidence_rows':40,'current_original_hashes_and_complete_visible_input':'PASS','all_40_option_bindings_and_10_realism_criteria':'PASS','source_payload_checks':[],'canonical_release_credit':0,'full_repository_QA':'NOT_RUN_BY_WORKER; root controller owns full immutable corpus QA; no guard modified or bypassed'}
for s in report['sources']:
 validate_independent_source_bytes(s,R)
 paths=[s['evidence_path'],s['metadata_path']]+([s['raw_path']] if s.get('raw_path') else [])
 meta=json.load(open(R/s['metadata_path']));assert sha((R/s['metadata_path']).read_bytes())==s['metadata_sha256']
 if s.get('raw_path'):assert sha((R/s['raw_path']).read_bytes())==meta['raw_sha256'] and sha((R/s['evidence_path']).read_bytes())==meta['text_sha256']
 if not meta.get('document_available',False):assert s['used_as_legal_authority'] is False
 if '--postcommit' in sys.argv:
  for p in paths:committed(p)
 proof['source_payload_checks'].append({'source_id':s['source_id'],'retained_paths':paths,'status':'PASS','document_available':meta.get('document_available',False)})
if '--postcommit' in sys.argv:
 committed(REPORT);committed(P+'/assigned-visible-input.json');committed(P+'/assignment.json')
 assert len(commit)==40 and git('status','--porcelain')=='','Worker worktree must be clean'
 base=git('rev-parse','a1bf03a6');changed=git('diff','--name-only',base,commit).splitlines()
 assert all(p.startswith(P+'/') or p==REPORT for p in changed),changed
 assert P+'/assignment.json' not in changed and P+'/assigned-visible-input.json' not in changed
 assert not any(p.endswith(('.raw','.txt')) and '/nabp' in p for p in changed)
 for p in changed:committed(p)
 proof['changed_paths']=changed;proof['clean_worktree']='PASS';proof['own_range_only']='PASS';proof['all_worker_changed_bytes_committed']='PASS';proof['nabp_copyrighted_raw_not_committed']='PASS';proof['root_base_commit']=base
 for m in report['methodology_and_schema_snapshots']:assert sha((R/m['snapshot_path']).read_bytes())==m['file_sha256']
 out=pathlib.Path('/tmp/independent-phase13-d-result.json');out.write_text(json.dumps(envelope,ensure_ascii=False,indent=2)+'\n')
 proof['envelope_path']=str(out);proof['envelope_sha256']=sha(out.read_bytes())
 proofpath=pathlib.Path('/tmp/independent-phase13-d-postcommit-validation.json');proofpath.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'worker_commit':commit,'report_sha256':report_sha,'envelope':str(out),'proof':str(proofpath),'proof_sha256':sha(proofpath.read_bytes()),'native_validation':'PASS'}))
else:print(json.dumps({'precommit_scoped_validation':'PASS','assigned_records':40,'sources':len(report['sources']),'report_sha256':report_sha}))
