from pathlib import Path
import json,sys,hashlib,subprocess,copy
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
import review_queue as q
from build_full_corpus_review import validate_independent_source_bytes
EV=ROOT/'reports/full-corpus-review/phase13-b-evidence';REPORT='reports/full-corpus-review/independent-phase13-b-review.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def git(*a):return subprocess.check_output(['git','-C',str(ROOT),*a]).decode().strip()
def require(x,msg):
 if not x:raise ValueError(msg)
job=json.loads((EV/'assignment.json').read_bytes());packet=json.loads((EV/'assigned-visible-input.json').read_bytes());raw=(ROOT/REPORT).read_bytes();report=json.loads(raw);commit=git('rev-parse','HEAD')
require(len(commit)==40,'full commit SHA')
require(git('branch','--show-current')==job['worker_branch'],'worker branch')
require(not git('status','--porcelain'),'worker tree must be clean after commit')
require(subprocess.check_output(['git','-C',str(ROOT),'show',commit+':'+REPORT])==raw,'commit report differs from disk')
require(report['input_bindings']['assignment_sha256']==sha(EV/'assignment.json'),'assignment bytes changed')
require(report['input_bindings']['visible_input_sha256']==sha(EV/'assigned-visible-input.json'),'packet bytes changed')
require(report['input_bindings']['question_hashes']==job['question_hashes'],'report hash map')
require({r['question_id'] for r in report['records']}==set(job['question_hashes']) and len(report['records'])==40,'exact forty')
# Original records are used solely as a hash preimage. Hidden fields are never printed.
conf=json.loads((ROOT/'site/practice-expansion/publication.json').read_bytes());paths=['practice_expansion/2026-10-23/candidates/questions.json']+[a['path'] for a in conf['additional_banks']]
found={}
for path in paths:
 for original in json.loads((ROOT/path).read_bytes())['questions']:
  if original['question_id'] in job['question_hashes']:
   qid=original['question_id'];require(qid not in found,'duplicate original ID');found[qid]=q.digest(original)
require(found==job['question_hashes'],'current whole-record hash changed')
packet_by_id={x['question_id']:x for x in packet['records']}
for r in report['records']:
 original=packet_by_id[r['question_id']]['original_visible_content'];require(q.digest(original)==r['visible_content_sha256'],'visible projection hash')
 require(r['record_sha256']==job['question_hashes'][r['question_id']],'record binding')
 require(set(r['legal_review']['per_choice_findings'])=={c['id'] for c in original['choices']},'missing choice finding')
 for c in original['choices']:
  f=r['legal_review']['per_choice_findings'][c['id']];require(f['option_text']==c['text'],'option text mismatch');require(f['authorities'],'authority missing')
  for a in f['authorities']:validate_independent_source_bytes(a,ROOT)
 require(len(r['realism_review']['criteria'])==10 and len(r['realism_review']['criterion_findings_ko'])==10,'incomplete realism rubric')
 require((r['realism_review']['verdict']=='PASS')==all(r['realism_review']['criteria'].values()),'false realism pass')
for s in report['sources']:
 validate_independent_source_bytes(s,ROOT)
 meta=ROOT/s['metadata_path'];require(sha(meta)==s['metadata_sha256'],'metadata SHA')
 require(subprocess.check_output(['git','-C',str(ROOT),'show',commit+':'+s['metadata_path']])==meta.read_bytes(),'metadata not in worker commit')
 if not s.get('public_raw_redistribution') is False:
  require(sha(ROOT/s['text_path'])==s['text_sha256'],'source extracted text SHA')
  require(subprocess.check_output(['git','-C',str(ROOT),'show',commit+':'+s['raw_path']])==(ROOT/s['raw_path']).read_bytes(),'raw source not in worker commit')
  require(subprocess.check_output(['git','-C',str(ROOT),'show',commit+':'+s['text_path']])==(ROOT/s['text_path']).read_bytes(),'text source not in worker commit')
 else:
  require(Path(s['raw_path']).exists() and sha(s['raw_path'])==s['raw_sha256'],'local NABP raw SHA')
  require(Path(s['text_path']).exists() and sha(s['text_path'])==s['text_sha256'],'local NABP text SHA')
  require(subprocess.check_output(['git','-C',str(ROOT),'show',commit+':'+s['evidence_path']])==(ROOT/s['evidence_path']).read_bytes(),'memo not in worker commit')
for path,b in report['methodology_files'].items():require(sha(ROOT/path)==b['file_sha256']==sha(ROOT/b['snapshot_path']),'methodology binding')
reportsha=hashlib.sha256(raw).hexdigest()
envelope={k:report[k] for k in ['stage','independent_of_authors','auditor','auditor_instance','actor_provenance','canonical_audit','canonical_release_credit','author_review_credit']}
envelope.update(question_hashes=job['question_hashes'],worker_commit=commit,results=[{'question_id':r['question_id'],'disposition':'NEEDS_REMEDIATION' if r['realism_review']['verdict']=='FAIL' else 'INDEPENDENT_ASSESSED','evidence_path':REPORT,'evidence_sha256':reportsha} for r in report['records']])
q.validate_result(job,envelope);j=copy.deepcopy(job);j['result']=envelope
for row in envelope['results']:q.validate_independent_evidence(j,row,report)
changed=git('diff-tree','--no-commit-id','--name-only','-r','HEAD').splitlines()
require(all(x.startswith('reports/full-corpus-review/phase13-b-evidence/') or x==REPORT for x in changed),'commit changed path outside own range')
require(not any(x.endswith('/assignment.json') or x.endswith('/assigned-visible-input.json') for x in changed),'root input mutated in worker commit')
Path('/tmp/independent-phase13-b-result.json').write_text(json.dumps(envelope,ensure_ascii=False,indent=2)+'\n')
proof={'stage':'independent-legacy','actor_provenance':report['actor_provenance'],'worker_commit':commit,'report_path':REPORT,'report_sha256':reportsha,'native_validate_result':'PASS','native_validate_independent_evidence_count':40,'original_current_hash_count':len(found),'source_bindings_count':len(report['sources']),'source_raw_text_metadata_shas':'PASS; NABP raw/text separately rechecked at declared /tmp paths; only own memo is committed','input_unchanged':'PASS','clean_worker_tree':'PASS','only_own_paths_changed':'PASS','report_commit_equals_disk':'PASS','canonical_release_credit':0,'release_eligible':False,'envelope_path':'/tmp/independent-phase13-b-result.json','envelope_committed':False,'summary':report['summary']}
Path('/tmp/independent-phase13-b-postcommit-proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps(proof,ensure_ascii=False,indent=2))
