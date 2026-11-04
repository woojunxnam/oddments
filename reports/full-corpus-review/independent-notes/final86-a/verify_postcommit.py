import json,hashlib,subprocess,sys,re
from pathlib import Path
from datetime import datetime,timezone
P=Path('reports/full-corpus-review/independent-notes/final86-a');sys.path.insert(0,str(Path('scripts').resolve()));import note_review_queue as q
sha=lambda b:hashlib.sha256(b).hexdigest();run=lambda *a:subprocess.check_output(a).decode().strip()
j=json.loads((P/'assignment.json').read_bytes());r=json.loads((P/'review.json').read_bytes());head=run('git','rev-parse','HEAD')
assert re.fullmatch('[0-9a-f]{40}',head);assert run('git','branch','--show-current')==j['worker_branch'];assert run('git','status','--porcelain')==''
result={k:r[k] for k in ['stage','actor_provenance','auditor','auditor_instance','independent_of_authors','canonical_audit','canonical_release_credit','question_audit_credit']};result.update(worker_commit=head,unit_hashes={uid:b['body_sha256'] for uid,b in j['unit_bindings'].items()},results=[{k:row[k] for k in ['unit_id','completeness','legal_status']} for row in r['records']],evidence={'path':str(P/'review.json'),'raw_sha256':sha((P/'review.json').read_bytes())},result_path=q.OUTPUT+j['job_id']+'-result.json')
q.validate_result(j,result);q.validate_evidence(j,result,r);assert q.committed_evidence(j,result,Path.cwd())==r
manifest=json.loads((P/'file-manifest.json').read_bytes());actual={str(f) for f in P.rglob('*') if f.is_file() and f.name!='file-manifest.json'};assert actual==set(manifest['files'])
for path,item in manifest['files'].items():
 f=Path(path);data=f.read_bytes();assert sha(data)==item['sha256'] and len(data)==item['bytes'];assert subprocess.check_output(['git','show',head+':'+path])==data
assert subprocess.check_output(['git','show',head+':'+str(P/'file-manifest.json')])==(P/'file-manifest.json').read_bytes()
sourcecount=0;excerptcount=0
for mp in sorted((P/'sources').glob('*.meta.json')):
 m=json.loads(mp.read_bytes());n=mp.name.split('.')[0];assert sha((P/'sources'/(n+m['raw_extension'])).read_bytes())==m['raw_sha256'];assert sha((P/'sources'/(n+'.txt')).read_bytes())==m['text_sha256'];assert m['content_validity']!='PENDING_MANUAL_SOFT404_ACCESS_AND_SCOPE_CHECK';sourcecount+=1
for row in r['records']:
 assert row['binding']==j['unit_bindings'][row['unit_id']]
 for claim in row['claims']:
  for a in claim['authorities']:
   for pf,hf in [('evidence_path','evidence_sha256'),('text_evidence_path','text_evidence_sha256'),('retrieval_metadata_path','retrieval_metadata_sha256')]:assert sha(Path(a[pf]).read_bytes())==a[hf]
   t=Path(a['text_evidence_path']).read_text();start,end=a['text_character_range'];assert t[start:end]==a['evidence_excerpt'];assert t[:start].count('\n')+1==a['text_line_range'][0] and t[:end].count('\n')+1==a['text_line_range'][1];assert len(a['evidence_excerpt'].strip())>20;excerptcount+=1
paths=set(run('git','log','--format=','--name-only',j['base_commit']+'..'+head).splitlines())-{''};assert paths and all(p.startswith(str(P)+'/') for p in paths)
roothead=run('git','-C','/workspace/oddments','rev-parse','HEAD');state=json.loads(subprocess.check_output(['git','-C','/workspace/oddments','show',roothead+':reports/full-corpus-review/independent-notes-work-queue.json']));actualjob=[x for x in state['jobs'] if x['job_id']==j['job_id']];assert len(actualjob)==1 and actualjob[0]['unit_bindings']==j['unit_bindings'] and actualjob[0]['worker_branch']==j['worker_branch']
envelope=Path('/workspace/scratch/notes-final86-a-result-envelope.json');envelope.write_bytes(q.encoded(result))
proof={'validated_at_utc':datetime.now(timezone.utc).isoformat(),'worker_commit':head,'report_raw_sha256':result['evidence']['raw_sha256'],'native_validate_result':'PASS_ACTUAL_POSTCOMMIT','native_validate_evidence':'PASS_ACTUAL_POSTCOMMIT','native_committed_evidence':'PASS_ACTUAL_POSTCOMMIT','file_manifest_files_checked':len(manifest['files']),'file_manifest_raw_sha256':sha((P/'file-manifest.json').read_bytes()),'all_manifest_and_manifest_itself_committed_bytes_match':True,'source_raw_text_meta_sets_checked':sourcecount,'authority_excerpt_character_and_line_ranges_checked':excerptcount,'all_worker_commit_range_paths_within_exact_own_prefix':True,'own_changed_paths_count':len(paths),'selected_job_current_root_binding_equal':True,'root_head_observed_at_postcommit':roothead,'clean':True,'envelope_path':str(envelope),'envelope_raw_sha256':sha(envelope.read_bytes()),'canonical_release_credit':0,'question_audit_credit':0}
if '--remote' in sys.argv:
 remote=run('git','ls-remote','origin','refs/heads/'+j['worker_branch']).split()[0];assert remote==head;proof.update(remote_branch=j['worker_branch'],remote_40_sha=remote,remote_equal_worker_commit=True)
Path('/workspace/scratch/notes-final86-a-postcommit-validation.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps(proof,ensure_ascii=False,indent=2))
