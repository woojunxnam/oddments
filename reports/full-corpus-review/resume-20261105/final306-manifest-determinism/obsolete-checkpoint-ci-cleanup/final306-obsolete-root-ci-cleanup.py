from pathlib import Path
import subprocess,json,datetime,hashlib,re,urllib.parse
R=Path('/workspace/oddments');O=Path('/workspace/scratch/final306-obsolete-root-ci-cleanup');O.mkdir(exist_ok=True);BRANCH='mission/mpje-after193-wave12';CURRENT='cfff5e131b0068e0259fb1f9d6eefb78f50f705e';REMOTE_CAP='6bfad9fc3f7d97bdb483d5d5de68415ba51b0441';H=lambda b:hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def command(argv,label):
 started=now();p=subprocess.run(argv,cwd=R,capture_output=True);(O/(label+'.stdout.raw')).write_bytes(p.stdout);(O/(label+'.stderr.raw')).write_bytes(p.stderr);rec={'started_at':started,'completed_at':now(),'argv':argv,'exit_code':p.returncode,'stdout_path':label+'.stdout.raw','stdout_sha256':H(p.stdout),'stderr_path':label+'.stderr.raw','stderr_sha256':H(p.stderr)};dump(O/(label+'.receipt.json'),rec);return p,rec
def git(*args):return subprocess.run(['git',*args],cwd=R,capture_output=True)
def ancestor(a,b):return git('merge-base','--is-ancestor',a,b).returncode==0
def remote(label):
 p,rec=command(['git','ls-remote','--heads','origin','refs/heads/'+BRANCH],label);lines=p.stdout.decode().splitlines();sha=lines[0].split()[0]if p.returncode==0 and len(lines)==1 else None
 return sha,rec
serial=0
def api(method,endpoint,label):
 global serial
 serial+=1;ident=f'{serial:03d}-{label}';p,rec=command(['gh','api','--include','--method',method,endpoint],ident);raw=p.stdout;parts=raw.split(b'\r\n\r\n',1)
 if len(parts)==1:parts=raw.split(b'\n\n',1)
 match=re.search(rb'^HTTP/\S+\s+(\d+)',raw);status=int(match.group(1))if match else None
 body=parts[1]if len(parts)==2 else b'';payload=None
 if body.strip():
  try:payload=json.loads(body)
  except ValueError:pass
 (O/(ident+'.body.raw')).write_bytes(body);rec.update(http_status=status,body_path=ident+'.body.raw',body_sha256=H(body));dump(O/(ident+'.receipt.json'),rec);return payload,rec
assert git('rev-parse','HEAD').stdout.decode().strip()==CURRENT
rsha,rrec=remote('initial-remote-ref');assert rsha and ancestor(rsha,REMOTE_CAP)
allruns={};list_receipts=[]
for status in['queued','in_progress']:
 for page in range(1,21):
  endpoint='repos/woojunxnam/oddments/actions/runs?'+urllib.parse.urlencode({'branch':BRANCH,'status':status,'per_page':100,'page':page})
  payload,rec=api('GET',endpoint,'list-'+status+'-'+str(page));list_receipts.append(rec);assert rec['http_status']==200 and isinstance(payload,dict)
  runs=payload['workflow_runs']
  for run in runs:allruns[run['id']]=run
  if len(runs)<100:break
 else:raise ValueError('Pagination limit reached; do not assume full inventory')
allowed=[];excluded=[];lineage={}
for run in allruns.values():
 sha=run.get('head_sha');proof={'head_sha':sha,'actual_ancestor_of_current':bool(sha and ancestor(sha,CURRENT)),'actual_ancestor_of_remote_at_initial_observation':bool(sha and ancestor(sha,rsha))};lineage[sha]=proof
 good=run.get('head_branch')==BRANCH and sha!=CURRENT and proof['actual_ancestor_of_current'] and proof['actual_ancestor_of_remote_at_initial_observation'] and run.get('status')in{'queued','in_progress'}
 item={k:run.get(k)for k in['id','name','head_sha','head_branch','event','status','conclusion','html_url','created_at','updated_at']};item['lineage_proof']=proof
 (allowed if good else excluded).append(item)
allowobj={'observed_at':now(),'actual_current_root_head':CURRENT,'actual_remote_head':rsha,'remote_cap':REMOTE_CAP,'strict_branch':BRANCH,'allowed_head_sha256s':sorted({x['head_sha']for x in allowed}),'allowed_runs':allowed,'excluded_runs':excluded,'fresh_api_list_receipts':list_receipts,'lineage':lineage,'future_candidate_main_PR193_other_branches_excluded':True,'cancellation_is_not_PASS_credit':True};allowpath=O/'allowlist-before-any-cancellation.json';dump(allowpath,allowobj);allowhash=H(allowpath.read_bytes());print(json.dumps({'phase':'ALLOWLIST_PERSISTED','allowed':len(allowed),'excluded':len(excluded),'allowlist_sha256':allowhash}),flush=True)
results=[]
for run in allowed:
 assert git('rev-parse','HEAD').stdout.decode().strip()==CURRENT
 remote_now,rproof=remote('pre-cancel-remote-'+str(run['id']));data,proof=api('GET','repos/woojunxnam/oddments/actions/runs/'+str(run['id']),'pre-cancel-'+str(run['id']))
 safe=bool(remote_now and ancestor(remote_now,REMOTE_CAP)and proof['http_status']==200 and isinstance(data,dict)and data.get('head_branch')==BRANCH and data.get('head_sha')==run['head_sha']and data['head_sha']!=CURRENT and ancestor(data['head_sha'],CURRENT)and ancestor(data['head_sha'],remote_now)and data.get('status')in{'queued','in_progress'})
 item={'run':run,'allowlist_sha256':allowhash,'remote_ref_before_cancel':remote_now,'fresh_run_receipt':proof,'eligible_at_action_time':safe,'cancel_requested':False}
 if safe:
  response,cancel=api('POST','repos/woojunxnam/oddments/actions/runs/'+str(run['id'])+'/cancel','cancel-'+str(run['id']));item.update(cancel_requested=True,cancel_response_receipt=cancel,cancel_request_accepted=cancel['http_status']==202 and cancel['exit_code']==0)
 else:item['reason']='Fresh status/identity/remote/ancestry could not be verified or run already completed; left untouched.'
 results.append(item);dump(O/'cancellation-requests.json',results);print(json.dumps({'phase':'ACTION','run_id':run['id'],'requested':item['cancel_requested'],'accepted':item.get('cancel_request_accepted'),'fresh_status':data.get('status')if isinstance(data,dict)else None}),flush=True)
# Final status observation is freshly queried even if request raced completion.
final=[]
for item in results:
 run=item['run'];data,proof=api('GET','repos/woojunxnam/oddments/actions/runs/'+str(run['id']),'final-'+str(run['id']));final.append({'id':run['id'],'head_sha':run['head_sha'],'head_branch':run['head_branch'],'status':data.get('status')if isinstance(data,dict)else None,'conclusion':data.get('conclusion')if isinstance(data,dict)else None,'fresh_receipt':proof})
dump(O/'final-status-observations.json',final)
summary={'purpose':'AUTHORIZED_OBSOLETE_OWN_CONTROLLER_CHECKPOINT_CI_CANCELLATION_NO_PASS_CREDIT','observed_at':now(),'root_head':CURRENT,'remote_cap':REMOTE_CAP,'initial_remote_head':rsha,'strict_branch':BRANCH,'allowlist_path':str(allowpath),'allowlist_sha256':allowhash,'initial_active_runs_observed':len(allruns),'allowlisted_runs':len(allowed),'excluded_runs':excluded,'cancellation_requests':len([x for x in results if x['cancel_requested']]),'accepted_cancellation_requests':len([x for x in results if x.get('cancel_request_accepted')]),'final_status_observations':final,'still_noncompleted_run_ids':[x['id']for x in final if x['status']!='completed'],'root_or_workflow_or_remote_branch_mutations':0,'main_PR193_other_branches_future_candidate_touched':False,'PASS_or_QA_or_release_credit':0,'root_head_after':git('rev-parse','HEAD').stdout.decode().strip()};assert summary['root_head_after']==CURRENT
dump(O/'summary.json',summary);manifest={str(p.relative_to(O)):H(p.read_bytes())for p in O.iterdir()if p.is_file()and p.name!='artifact-sha256.json'};dump(O/'artifact-sha256.json',manifest)
print(json.dumps({'summary':str(O/'summary.json'),'sha256':H((O/'summary.json').read_bytes()),'requests':summary['cancellation_requests'],'accepted':summary['accepted_cancellation_requests'],'pending_final':summary['still_noncompleted_run_ids']}),flush=True)
