from pathlib import Path
import subprocess,json,hashlib,datetime,concurrent.futures,time
R=Path('/workspace/oddments');S=Path('/workspace/scratch');D=S/'pre-final-owned-checkpoint-ci-raw';D.mkdir(exist_ok=True);CAP='5b213997972747c2d4ea9a80b02cf33ddfc1af5c';REPO='woojunxnam/oddments';ACTIVE={'queued','in_progress','requested','waiting','pending'};H=lambda b:hashlib.sha256(b).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def git(*args):return subprocess.check_output(['git','-C',str(R),*args],text=True).strip()
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
assert git('rev-parse','HEAD')==CAP and not git('status','--porcelain','--untracked-files=no')
inputs={};owned={}
for name in('independent-notes-work-queue.json','remaining9-procedural-work-queue.json'):
 p=R/'reports/full-corpus-review'/name;b=p.read_bytes();inputs[str(p.relative_to(R))]=H(b);assert b==subprocess.check_output(['git','-C',str(R),'show',CAP+':'+str(p.relative_to(R))])
 for j in json.loads(b)['jobs']:
  actor=j.get('actor_provenance',j.get('result',{}).get('actor_provenance',{}));assert actor.get('actor_id','').startswith('/root/')
  assert j['status']=='INTEGRATED';branch=j['worker_branch'];commit=j['result']['worker_commit'];assert len(commit)==40
  owned[branch]={'kind':'EXACT_OWNED_NATIVE_WORKER','cap':commit,'actual_actor_provenance':actor,'source_queue':str(p.relative_to(R)),'job_id':j['job_id'],'sequence':j['sequence']}
owned['mission/mpje-after193-wave12']={'kind':'EXPLICIT_AUTHORIZED_INTERMEDIATE_CONTROLLER_ANCESTORS','cap':CAP,'not_release_candidate':True}
eng='engineering/remaining9-procedural-contract';local_eng=git('rev-parse','refs/heads/'+eng);cut=int(git('show','-s','--format=%ct',CAP));engcap=next(sha for sha in git('rev-list','refs/heads/'+eng).splitlines()if int(git('show','-s','--format=%ct',sha))<=cut)
owned[eng]={'kind':'EXPLICIT_OWNED_ENGINEERING_KNOWN_PRE_CHECKPOINT_ANCESTORS','cap':engcap,'local_tip_at_observation':local_eng,'checkpoint_commit_unix':cut,'newer_engineering_tip_excluded':local_eng!=engcap}
write(S/'pre-final-owned-checkpoint-ci-ownership.json',{'root_head':CAP,'scope_sources':inputs,'owned_branch_caps':owned,'future_candidate_or_main_or_public_PR193_excluded':True,'new_legal_or_release_credit':0})
api_counter=0
def api(endpoint,method='GET',rawpath=None):
 args=['gh','api','-X',method,'repos/'+REPO+'/'+endpoint];res=subprocess.run(args,text=True,capture_output=True)
 if rawpath:rawpath.write_text(res.stdout)
 return {'exit_code':res.returncode,'stdout':res.stdout,'stderr':res.stderr,'endpoint':endpoint,'method':method}
def get_json(endpoint,rawpath):
 v=api(endpoint,rawpath=rawpath)
 if v['exit_code']:raise RuntimeError(v['stderr'])
 return json.loads(v['stdout'])
def list_status(status):
 allruns=[];page=1
 while True:
  path=D/f'initial-{status}-page{page}.json';obj=get_json(f'actions/runs?status={status}&per_page=100&page={page}',path);rows=obj['workflow_runs'];allruns.extend(rows)
  if len(rows)<100:break
  page+=1
 return status,allruns
with concurrent.futures.ThreadPoolExecutor(max_workers=5)as pool:groups=list(pool.map(list_status,sorted(ACTIVE)))
runs={r['id']:r for _,rr in groups for r in rr};initial={'purpose':'FRESH_ACTIVE_RUN_INVENTORY_ONLY_KNOWN_OWNED_SCOPE','root_head':CAP,'observed_at':now(),'statuses':{k:len(v)for k,v in groups},'active_runs':list(runs.values()),'root_mutated':False,'pass_credit':0};write(S/'pre-final-owned-checkpoint-ci-observation.json',initial)
def ancestor(sha,cap):
 return subprocess.run(['git','-C',str(R),'merge-base','--is-ancestor',sha,cap],capture_output=True).returncode==0
eligible=[];skipped=[]
for run in runs.values():
 branch=run.get('head_branch');owner=owned.get(branch);reason=None
 if branch in {'main','master'}:reason='PROTECTED_MAIN'
 elif any(p.get('number')==193 for p in run.get('pull_requests',[])):reason='PROTECTED_PUBLIC_PR193'
 elif run.get('head_repository',{}).get('full_name')!=REPO:reason='FOREIGN_HEAD_REPOSITORY'
 elif not owner:reason='BRANCH_OUTSIDE_EXPLICIT_AUTHORIZED_SCOPE'
 elif not ancestor(run['head_sha'],owner['cap']):reason='HEAD_NOT_KNOWN_ANCESTOR_OF_AUTHORIZED_CAP_FUTURE_OR_OUT_OF_SCOPE'
 if reason:skipped.append({'run_id':run['id'],'head_branch':branch,'head_sha':run['head_sha'],'status':run['status'],'reason':reason})
 else:eligible.append(run)
result={'purpose':'CANCEL_ONLY_ACTUAL_OWNED_INTERMEDIATE_EVIDENCE_AND_AUTHORIZED_CONTROLLER_CHECKPOINT_CI_NOT_FINAL_QA','root_head':CAP,'started_at':now(),'ownership_path':str(S/'pre-final-owned-checkpoint-ci-ownership.json'),'initial_observation_path':str(S/'pre-final-owned-checkpoint-ci-observation.json'),'eligible_initial_count':len(eligible),'skipped_initial':skipped,'actions':[],'remote_branches_deleted':False,'workflow_files_changed':False,'root_head_or_source_or_snapshot_changed':False,'cancelled_runs_count_as_pass':False,'new_legal_or_release_credit':0,'future_candidate_CI_still_required':True}
out=S/'pre-final-owned-checkpoint-ci-cancellations.json';write(out,result);print(json.dumps({'phase':'ACTUAL_OWNED_SCOPE_SELECTED','eligible':len(eligible),'skipped':len(skipped),'engineering_cap':engcap,'engineering_newer_tip_not_authorized':local_eng},ensure_ascii=False),flush=True)
for run in sorted(eligible,key=lambda r:(r['status']!='in_progress',r['created_at'],r['id'])):
 rid=run['id'];branch=run['head_branch'];owner=owned[branch];before_path=D/f'{rid}-before.json';before=get_json(f'actions/runs/{rid}',before_path);action={'run_id':rid,'url':before.get('html_url'),'head_branch':branch,'head_sha':before['head_sha'],'authorized_cap':owner['cap'],'ownership_kind':owner['kind'],'fresh_run_observed_at':now(),'fresh_run_path':str(before_path),'fresh_run_sha256':H(before_path.read_bytes()),'status_before':before['status']}
 if before['head_branch']!=branch or before['head_sha']!=run['head_sha']or before['status']not in ACTIVE or not ancestor(before['head_sha'],owner['cap'])or any(p.get('number')==193 for p in before.get('pull_requests',[])):
  action['action']='SKIPPED_AFTER_FRESH_STATUS_OR_IDENTITY_RECHECK'
 else:
  remote=git('ls-remote','--heads','origin','refs/heads/'+branch).split();action['fresh_remote_branch_tip']=remote[0]if remote else None
  local_tip=git('rev-parse','refs/heads/'+branch)if owner['kind']!='EXPLICIT_AUTHORIZED_INTERMEDIATE_CONTROLLER_ANCESTORS'else CAP
  if not remote or remote[0]!=local_tip or(owner['kind']=='EXACT_OWNED_NATIVE_WORKER'and remote[0]!=owner['cap']):action['action']='SKIPPED_REMOTE_LOCAL_OR_BOUND_WORKER_TIP_MISMATCH'
  else:
   action['cancel_requested_at']=now();request=api(f'actions/runs/{rid}/cancel',method='POST');action['cancel_request_response']=request;action['action']='CANCEL_REQUEST_ACCEPTED'if request['exit_code']==0 else'CANCEL_REQUEST_REJECTED_OR_ALREADY_FINISHED'
   after_path=D/f'{rid}-after.json';after=get_json(f'actions/runs/{rid}',after_path);action.update({'status_after':after['status'],'conclusion_after':after.get('conclusion'),'after_observed_at':now(),'after_run_path':str(after_path),'after_run_sha256':H(after_path.read_bytes())})
 result['actions'].append(action);write(out,result);print(json.dumps({'run_id':rid,'branch':branch,'head_sha':run['head_sha'][:10],'action':action['action'],'status_after':action.get('status_after'),'conclusion_after':action.get('conclusion_after')},ensure_ascii=False),flush=True)
# Final status observation is independent of request acceptance; no success credit is inferred.
final=[]
for a in result['actions']:
 if a['action']!='CANCEL_REQUEST_ACCEPTED':continue
 rid=a['run_id'];p=D/f'{rid}-final.json';r=get_json(f'actions/runs/{rid}',p);final.append({'run_id':rid,'head_branch':r['head_branch'],'head_sha':r['head_sha'],'status':r['status'],'conclusion':r.get('conclusion'),'raw_path':str(p),'raw_sha256':H(p.read_bytes())})
result['final_observations']=final;result['completed_at']=now();result['accepted_cancel_requests']=sum(a['action']=='CANCEL_REQUEST_ACCEPTED'for a in result['actions']);result['observed_cancelled']=sum(a['conclusion']=='cancelled'for a in final);result['observed_not_yet_cancelled']=[a for a in final if a['conclusion']!='cancelled'];assert git('rev-parse','HEAD')==CAP and not git('status','--porcelain','--untracked-files=no')
for p,sha in inputs.items():assert H((R/p).read_bytes())==sha
write(out,result);print(json.dumps({'phase':'COMPLETED','receipt':str(out),'receipt_sha256':H(out.read_bytes()),'accepted_cancel_requests':result['accepted_cancel_requests'],'observed_cancelled':result['observed_cancelled'],'not_yet_final':len(result['observed_not_yet_cancelled']),'root_unchanged':True,'pass_credit':0},ensure_ascii=False),flush=True)
