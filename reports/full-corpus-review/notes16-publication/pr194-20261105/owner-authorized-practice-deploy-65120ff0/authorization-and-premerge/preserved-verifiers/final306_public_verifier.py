#!/usr/bin/env python3
"""Exact-candidate public verification. No network or browser action occurs before main().

Historical PR193 algorithms are parameterized; historical responses/PASS values are
never inputs. Invocation requires an approved, deployed, exact candidate and merge.
All evidence is written outside the immutable checkout and expected publish tree.
"""
from __future__ import annotations
import argparse
import ast
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone, timedelta
import hashlib
import html
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import time
import urllib.request
from urllib.parse import urlsplit

ORIGIN='https://woojunxnam.github.io/oddments/'
REPO='woojunxnam/oddments'
CRITICAL14=('index.html','practice-expansion/index.html','practice-expansion/build.json','practice-expansion/quality-review.html','notes/build.json','notes/content.js','notes/notes.js','notes/book.html','notes/complete-notes.md','notes/study-data.js','notes/refresh-data.js','generated/questions.json','generated/study_guide.json','generated/preview_allowlist.json')
QA_FILES=('qa.yml','practice-quality-qa.yml','representative-quality-qa.yml','notes-qa.yml','refresh-qa.yml','exam-study-qa.yml','public-practice-qa.yml','practice-expansion-qa.yml')
SCRIPTS=('verify_public_practice.py','verify_notes_browser.py','verify_refresh_browser.py','verify_q0012_withdrawal_browser.py','verify_representative_rewrites.py')
# Approved task scope, compared against computed candidate data, never treated as measured data.
APPROVED_SCOPE={'questions':2349,'key_assessed':2312,'key_unassessed':37,'effective_realism_PASS':880,'note_units':306,'note_claims':7086,'claim_LEGAL_HOLD':36,'claim_SOURCE_BLOCKED':890,'default_questions':202,'representative_questions':77}
BANK77_SHA='99520b18352b850fdf0148370d7fe34059a242b79e01f3909fc2f489244cc999'

def now():return datetime.now(timezone.utc).isoformat()
def sha(raw):return hashlib.sha256(raw).hexdigest()
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def require(condition,message):
    if not condition:raise ValueError(message)
def full_sha(v):
    if not re.fullmatch('[0-9a-f]{40}',v):raise argparse.ArgumentTypeError('Require an actual full40 lowercase commit SHA')
    return v
def positive(v):
    try:x=int(v)
    except ValueError:raise argparse.ArgumentTypeError('Require an actual positive run ID')
    if x<=0:raise argparse.ArgumentTypeError('Require an actual positive run ID')
    return x

def parser():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--candidate-sha',required=True,type=full_sha)
    p.add_argument('--merge-sha',required=True,type=full_sha)
    p.add_argument('--pages-run-id',required=True,type=positive)
    p.add_argument('--qa-run-ids',required=True,nargs='+',type=positive,help='Actual successful premerge run IDs covering all eight workflows on exact candidate SHA')
    p.add_argument('--checkout',required=True,type=Path,help='Clean frozen actual merge checkout with candidate object available')
    p.add_argument('--evidence-output',required=True,type=Path,help='New nonexisting external evidence directory')
    p.add_argument('--expected-site',required=True,type=Path,help='Fresh exact candidate/merge published output outside checkout')
    p.add_argument('--expected-manifest',required=True,type=Path,help='Fresh JSON: source_head,source_tree,exit_code=0,all_file_sha256 for entire40-file publish output')
    p.add_argument('--pr-number',required=True,type=positive,help='Actual new merged PR, never historical193 by default')
    p.add_argument('--premerge-pr-proof',required=True,type=Path,help='Actual root-retained premerge raw5 API head/base/merge-ref/tree proof; never a generated placeholder')
    p.add_argument('--python',default=sys.executable,help='Interpreter with Playwright and project dependencies')
    return p

def adapt_browser_source(name,source):
    """Only switch the exact loopback-selection block; preserve every assert AST."""
    if name=='verify_notes_browser.py':
        before="""    if not args.inline_preview:
        class Handler(http.server.SimpleHTTPRequestHandler):
            def log_message(self,*args):pass
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(SITE)))
        threading.Thread(target=server.serve_forever,daemon=True).start()
        base=f'http://127.0.0.1:{server.server_port}/'
    else:base=''"""
    elif name=='verify_refresh_browser.py':
        before="""    if not a.inline_preview:
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(a.site)))
        threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
    else:base='https://refresh-preview.invalid/'"""
    else:raise ValueError('Adapter scope is exactly notes and refresh')
    require(source.count(before)==1,'Original origin-selection block changed; stop for review')
    after='    base='+repr(ORIGIN);adapted=source.replace(before,after)
    assertions=lambda text:[ast.dump(n,include_attributes=False)for n in ast.walk(ast.parse(text))if isinstance(n,ast.Assert)]
    require(assertions(source)==assertions(adapted),'Browser assert AST changed')
    return adapted,{'original_sha256':sha(source.encode()),'adapted_sha256':sha(adapted.encode()),'removed_selection':before,'replacement':after,'all_assert_AST_identical':True,'origin':ORIGIN,'isolated_context':True,'real_user_profile_used':False,'assert_count':len(assertions(source)),'inline_preview_used':False}


WORKFLOW_JOBS={'qa.yml':('validate',),'practice-quality-qa.yml':('quality',),'representative-quality-qa.yml':('revision','production'),'notes-qa.yml':('notes',),'refresh-qa.yml':('refresh',),'exam-study-qa.yml':('study','production'),'public-practice-qa.yml':('public-practice',),'practice-expansion-qa.yml':('draft',)}
PRODUCTION_IF="github.event_name == 'workflow_run' && github.event.workflow_run.conclusion == 'success' && github.event.workflow_run.head_branch == 'main'"

def workflow_jobs_contract(filename,text):
    require(filename in WORKFLOW_JOBS,'Unknown required workflow')
    require(text.count('\njobs:')==1,'Workflow jobs declaration changed')
    blocks=re.findall(r'^  ([A-Za-z_][\w-]*):\s*\n(.*?)(?=^  [A-Za-z_][\w-]*:\s*$|\Z)',text.split('\njobs:',1)[1],re.M|re.S)
    jobs=dict(blocks);require(len(jobs)==len(blocks)and tuple(jobs)==WORKFLOW_JOBS[filename],'Declared workflow jobs changed')
    require(all(not re.search(r'^    (name|strategy):',block,re.M)for block in jobs.values()),'Job name/matrix contract changed')
    if 'production'in jobs:
        required=next(n for n in jobs if n!='production')
        condition=lambda b:re.findall(r'^    if:\s*(.+)$',b,re.M)
        require(condition(jobs[required])==["github.event_name != 'workflow_run'"]and condition(jobs['production'])==[PRODUCTION_IF],'Exact conditional production source changed')
    return tuple(jobs)

def validation_jobs(filename,event,jobs,workflow_text,allow_pending=False):
    """Only exact false-if production SKIPPED on push/PR is a valid skip."""
    require(event in {'push','pull_request'},'Validation run must be actual push or pull_request')
    names=workflow_jobs_contract(filename,workflow_text);observed=[j.get('name')for j in jobs]
    require(len(observed)==len(set(observed))and set(observed)<=set(names),'Unknown or duplicate validation job')
    missing=set(names)-set(observed)
    require(not missing or allow_pending,'Required validation job missing')
    pending=bool(missing);checks=[]
    for job in jobs:
        name=job['name'];state=job.get('status');conclusion=job.get('conclusion')
        if state!='completed':
            require(allow_pending and state in {'queued','in_progress','waiting','pending','requested'},'Validation job did not complete')
            pending=True;checks.append({'name':name,'status':'PENDING','actual_status':state,'actual_conclusion':conclusion});continue
        if name=='production':
            require(filename in {'exam-study-qa.yml','representative-quality-qa.yml'}and conclusion=='skipped','Only exact false-if production SKIPPED is allowed on push/PR')
            checks.append({'name':name,'status':'EXPECTED_CONDITIONAL_SKIPPED','source_if':PRODUCTION_IF,'actual_event':event})
        else:
            require(conclusion=='success','Required validation job failed/cancelled/skipped: '+name)
            checks.append({'name':name,'status':'SUCCESS'})
    return {'status':'PENDING'if pending else'SUCCESS','job_checks':checks,'missing_pending_job_names':sorted(missing),'arbitrary_skips_allowed':False}

def require_pr_binding(pr,candidate,merge,number):
    require(pr.get('number')==number and pr.get('merged')is True and pr.get('merge_commit_sha')==merge,'Actual PR merge mismatch')
    require(pr.get('head',{}).get('sha')==candidate,'Actual merged PR head is not tested candidate')
    require(pr.get('base',{}).get('ref')=='main'and pr.get('base',{}).get('repo',{}).get('full_name')==REPO,'Actual PR base is not exact official main')


def utc_moment(value):
    require(isinstance(value,str),'Actual UTC timestamp required')
    try:dt=datetime.fromisoformat(value.replace('Z','+00:00'))
    except ValueError:raise ValueError('Invalid actual UTC timestamp')
    require(dt.utcoffset()==timedelta(0),'Timestamp must be UTC-aware')
    return dt

def load_premerge_proof(path,candidate,candidate_tree,pull_number):
    """Recompute actual raw API values; metadata assertions alone grant no proof."""
    path=path.resolve();raw=path.read_bytes();p=json.loads(raw);require(p.get('schema_version')==1 and p.get('purpose')=='ACTUAL_PREMERGE_HEAD_BASE_AND_TREE_PROOF'and p.get('repository')==REPO and p.get('pull_number')==pull_number,'Wrong premerge proof schema/purpose/repository/PR')
    require(p.get('candidate_sha')==candidate and p.get('candidate_tree')==candidate_tree and p.get('merge_ref_tree')==candidate_tree,'Premerge proof candidate/tree scope changed')
    for key in('candidate_sha','candidate_tree','base_sha','merge_ref_sha','merge_ref_tree'):full_sha(p.get(key,''))
    observed=utc_moment(p.get('observed_at_utc'));require(observed<=datetime.now(timezone.utc),'Premerge proof claims a future observation')
    api='https://api.github.com/repos/'+REPO+'/';urls={'pull':api+'pulls/'+str(pull_number),'main_commit':api+'commits/main','candidate_commit':api+'commits/'+candidate,'merge_ref':api+'git/ref/pull/'+str(pull_number)+'/merge','merge_ref_commit':api+'commits/'+p['merge_ref_sha']};payload={};originals={}
    for key,url in urls.items():
        b=p.get(key,{});relative=b.get('path');require(isinstance(relative,str)and relative and'\\'not in relative,'Raw API relative path required');rp=PurePosixPath(relative);require(not rp.is_absolute()and'..'not in rp.parts and rp.parts!=('.',),'Unsafe raw API path');file=(path.parent/relative).resolve();require(path.parent in file.parents,'Raw API path escapes proof directory')
        require(b.get('official_url')==url and type(b.get('http_status'))is int and b['http_status']==200 and b.get('tls_verified')is True,'Exact official actual200/TLS API binding required')
        require(utc_moment(b.get('retrieved_at_utc'))<=observed,'Raw retrieval follows claimed premerge observation');data=file.read_bytes();require(re.fullmatch('[0-9a-f]{64}',b.get('raw_sha256',''))and sha(data)==b['raw_sha256'],'Original API raw SHA mismatch: '+key);payload[key]=json.loads(data);originals[key]=data
    pr=payload['pull'];main=payload['main_commit'];cc=payload['candidate_commit'];ref=payload['merge_ref'];mc=payload['merge_ref_commit']
    require(pr.get('number')==pull_number and pr.get('state')=='open'and pr.get('merged')is False and pr.get('head',{}).get('sha')==candidate,'Retained raw PR was not actual open premerge candidate')
    require(pr.get('base',{}).get('ref')=='main'and pr.get('base',{}).get('repo',{}).get('full_name')==REPO and pr['base'].get('sha')==main.get('sha')==p['base_sha'],'Retained raw main/base commit mismatch')
    require(cc.get('sha')==candidate and cc.get('commit',{}).get('tree',{}).get('sha')==mc.get('commit',{}).get('tree',{}).get('sha')==candidate_tree,'Actual raw candidate and PR merge-ref trees differ')
    require(ref.get('ref')=='refs/pull/'+str(pull_number)+'/merge'and ref.get('object',{}).get('sha')==mc.get('sha')==p['merge_ref_sha'],'Actual raw PR merge ref/commit mismatch')
    require({candidate,p['base_sha']}<={x.get('sha')for x in mc.get('parents',[])},'Actual raw PR merge parents do not include candidate and base')
    return {'proof':p,'raw':raw,'raw_sha256':sha(raw),'original_response_bytes':originals,'actual_raw_values_recomputed':True}

class Verification:
    def __init__(self,a):
        self.a=a;self.root=a.checkout.resolve();self.site=a.expected_site.resolve();self.out=a.evidence_output.resolve();self.counter=0;self.results={};self.script_hashes={};self.verifier_sha=sha(Path(__file__).read_bytes())
        require(len(a.qa_run_ids)==len(set(a.qa_run_ids)),'Duplicate QA run IDs')
        require(self.root.is_dir()and self.site.is_dir(),'Actual checkout and expected published tree required')
        require(not self.out.exists(),'Evidence directory already exists; never overwrite previous observations')
        for parent in(self.root,self.site):require(not(self.out==parent or parent in self.out.parents or self.out in parent.parents),'Evidence must be disjoint from checkout and expected site')
        require(self.root!=self.site and self.root not in self.site.parents,'Published output must be outside checkout')
        require(self.git('rev-parse','HEAD')==a.merge_sha,'Checkout must be the exact actual merge')
        require(not self.git('status','--porcelain'),'Frozen checkout must be clean')
        self.manifest=json.loads(a.expected_manifest.read_bytes());require(self.manifest.get('source_head')in{a.candidate_sha,a.merge_sha}and self.manifest.get('exit_code')==0,'Fresh successful expected build must bind exact candidate/merge')
        self.expected=self.manifest.get('all_file_sha256');require(isinstance(self.expected,dict)and len(self.expected)==40,'Exact complete40-file expected manifest required')
        actual={p.relative_to(self.site).as_posix():sha(p.read_bytes())for p in self.site.rglob('*')if p.is_file()};require(actual==self.expected,'Entire expected publish directory must equal fresh manifest; no extra/missing/modified assets')
        require(set(CRITICAL14)<=set(actual),'Critical14 omitted')
        self.premerge=load_premerge_proof(a.premerge_pr_proof,a.candidate_sha,self.git('rev-parse',a.candidate_sha+'^{tree}'),a.pr_number)
        require(self.manifest.get('source_tree')==self.git('rev-parse',self.manifest['source_head']+'^{tree}'),'Expected manifest must bind actual source_tree as well as full source_head')
        for path,digest in actual.items():
            pp=PurePosixPath(path);require(not pp.is_absolute()and'..'not in pp.parts and'?'not in path and'#'not in path and re.fullmatch('[0-9a-f]{64}',digest),'Unsafe expected asset path/hash')
        for name in SCRIPTS:self.script_hashes[name]=sha((self.root/'scripts'/name).read_bytes())
        self.required_names={}
        for file in QA_FILES:
            text=(self.root/'.github/workflows'/file).read_text();match=re.search(r'^name:\s*(.+)$',text,re.M);require(match,'Workflow name missing');self.required_names[match.group(1).strip('"\'')]=file
        require(len(self.required_names)==8,'Expected eight distinct required QA workflows')
        self.out.mkdir(parents=True);(self.out/'executed-verifier-source.py').write_bytes(Path(__file__).read_bytes());(self.out/'premerge-proof.source.json').write_bytes(self.premerge['raw']);(self.out/'premerge').mkdir()
        for key,raw in self.premerge['original_response_bytes'].items():(self.out/'premerge'/(key+'.response.raw.json')).write_bytes(raw)
        self.write('inputs.json',{'started_at':now(),'candidate':a.candidate_sha,'merge':a.merge_sha,'checkout':str(self.root),'site':str(self.site),'expected_manifest_sha256':sha(a.expected_manifest.read_bytes()),'expected_manifest':self.manifest,'qa_run_ids':a.qa_run_ids,'pages_run_id':a.pages_run_id,'required_workflows':self.required_names,'source_script_sha256s':self.script_hashes,'executed_verifier_sha256':self.verifier_sha,'actual_premerge_proof_raw_sha256':self.premerge['raw_sha256'],'fresh_measurements_only':True,'status':'RUNNING_NOT_PASS'})
    def git(self,*args):return subprocess.check_output(['git','-C',str(self.root),*args],text=True).strip()
    def write(self,path,x):
        p=self.out/path;require(not p.exists(),'Refuse evidence overwrite: '+str(path));p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
    def stable(self):
        require(sha(Path(__file__).read_bytes())==self.verifier_sha,'Executed verifier source changed')
        require(self.git('rev-parse','HEAD')==self.a.merge_sha and not self.git('status','--porcelain'),'Frozen checkout changed')
        for n,h in self.script_hashes.items():require(sha((self.root/'scripts'/n).read_bytes())==h,'Browser source changed')
    def api(self,endpoint,label):
        self.counter+=1;prefix=f'api/{self.counter:03d}-{label}';cmd=['gh','api','--hostname','github.com','--include','--method','GET',endpoint];start=now();p=subprocess.run(cmd,capture_output=True,env={k:v for k,v in os.environ.items()if k not in {'GH_DEBUG','DEBUG'}})
        raw=p.stdout;parts=re.split(b'\r?\n\r?\n',raw,maxsplit=1);m=re.search(rb'^HTTP/\S+\s+(\d+)',raw);status=int(m.group(1))if m else None
        (self.out/(prefix+'.http.raw')).parent.mkdir(parents=True,exist_ok=True);(self.out/(prefix+'.http.raw')).write_bytes(raw);(self.out/(prefix+'.stderr.raw')).write_bytes(p.stderr)
        self.write(prefix+'.receipt.json',{'started_at':start,'completed_at':now(),'command':cmd,'exit_code':p.returncode,'http_status':status,'raw_sha256':sha(raw),'stderr_sha256':sha(p.stderr)})
        require(p.returncode==0 and status==200 and len(parts)==2,'Fresh API read failed: '+endpoint)
        return json.loads(parts[1])
    def paged(self,endpoint,key,label):
        all_rows=[]
        for page in range(1,101):
            x=self.api(endpoint+('&'if'?'in endpoint else'?')+f'per_page=100&page={page}',label+'-'+str(page));rows=x[key]if key else x;require(isinstance(rows,list),'API pagination shape changed');all_rows.extend(rows)
            if len(rows)<100:return all_rows
        raise ValueError('Pagination limit reached; no partial gate claim')
    def api_snapshot(self,label):
        a=self.a;pr=self.api(f'repos/{REPO}/pulls/{a.pr_number}',label+'-pull');require_pr_binding(pr,a.candidate_sha,a.merge_sha,a.pr_number);require(utc_moment(self.premerge['proof']['observed_at_utc'])<=utc_moment(pr['merged_at'])+timedelta(seconds=1),'Retained proof was not observed before actual merge')
        cand=self.api(f'repos/{REPO}/git/commits/{a.candidate_sha}',label+'-candidate');merge=self.api(f'repos/{REPO}/git/commits/{a.merge_sha}',label+'-merge');main=self.api(f'repos/{REPO}/git/ref/heads/main',label+'-main')
        trees=[cand['tree']['sha'],merge['tree']['sha'],self.git('rev-parse',a.candidate_sha+'^{tree}'),self.git('rev-parse',a.merge_sha+'^{tree}')];require(len(set(trees))==1,'Tested and merged local/API trees differ; stop for review/revalidation');require(main['object']['sha']==a.merge_sha,'Current main moved from exact merge')
        pages=self.api(f'repos/{REPO}/actions/runs/{a.pages_run_id}',label+'-pages');require(pages['head_sha']==a.merge_sha and pages['status']=='completed'and pages['conclusion']=='success'and pages['path']=='.github/workflows/pages.yml','Actual exact-merge Pages run did not succeed')
        pj=self.paged(f'repos/{REPO}/actions/runs/{a.pages_run_id}/jobs','jobs',label+'-pages-jobs');require(pj and all(j['status']=='completed'and j['conclusion']=='success'for j in pj),'Pages jobs incomplete/unsuccessful')
        covered=set();qa=[]
        for rid in a.qa_run_ids:
            run=self.api(f'repos/{REPO}/actions/runs/{rid}',label+'-qa-'+str(rid));require(run['head_sha']==a.candidate_sha and run['name']in self.required_names and run['path']=='.github/workflows/'+self.required_names[run['name']]and run['status']=='completed'and run['conclusion']=='success','Required premerge QA ID is wrong SHA/workflow or not successful: '+str(rid));covered.add(run['name']);qa.append({k:run.get(k)for k in('id','head_sha','name','path','status','conclusion','html_url','run_attempt')})
            if run.get('event')=='pull_request':
                associations=run.get('pull_requests',[])
                if associations:require(any(x.get('number')==a.pr_number and x.get('head',{}).get('sha')==a.candidate_sha and x.get('base',{}).get('ref')=='main'and x.get('base',{}).get('sha')==self.premerge['proof']['base_sha']for x in associations),'Provided actual PR run association conflicts with retained proof')
                qa[-1]['PR_association_field_empty_after_merge']=not bool(associations);qa[-1]['PR_binding_basis']='ACTUAL_CURRENT_PR_HEAD_BASE_PLUS_RETAINED_PREMERGE_RAW_HEAD_BASE_MERGE_REF_TREE_PROOF'
            jobs=self.paged(f'repos/{REPO}/actions/runs/{rid}/jobs','jobs',label+'-qa-jobs-'+str(rid));job_check=validation_jobs(self.required_names[run['name']],run.get('event'),jobs,(self.root/run['path']).read_text());require(job_check['status']=='SUCCESS','Candidate required validation incomplete');qa[-1]['job_check']=job_check
            for job in jobs:
                if job.get('conclusion')=='success':require(utc_moment(job.get('completed_at'))<=utc_moment(self.premerge['proof']['observed_at_utc']),'Premerge proof was not freshly captured after candidate QA completion')
        require(covered==set(self.required_names),'Must supply successful premerge IDs for all eight workflows on exact candidate')
        # Main jobs are fresh observations: pending never becomes success, and public
        # software verification does not claim final nine-workflow/two-production completion.
        run_inventories={}
        for h in {a.candidate_sha,a.merge_sha}:
            run_inventories[h]=self.paged(f'repos/{REPO}/actions/runs?head_sha={h}','workflow_runs',label+'-runs-'+h[:10]);self.paged(f'repos/{REPO}/commits/{h}/check-runs','check_runs',label+'-checks-'+h[:10])
        main_runs=[r for r in run_inventories[a.merge_sha]if r.get('head_sha')==a.merge_sha]
        postmerge=[]
        for name,file in self.required_names.items():
            choices=[r for r in main_runs if r.get('event')=='push'and r.get('name')==name and r.get('path')=='.github/workflows/'+file]
            if not choices:postmerge.append({'name':name,'status':'MISSING_RUN_NOT_PASSED','conclusion':None});continue
            run=max(choices,key=lambda r:(r.get('created_at',''),r.get('id',0),r.get('run_attempt',0)));jobs=self.paged(f'repos/{REPO}/actions/runs/{run["id"]}/jobs','jobs',label+'-main-jobs-'+str(run['id']));row={k:run.get(k)for k in('id','name','head_sha','event','path','status','conclusion','html_url','run_attempt')};row['jobs']=[{k:j.get(k)for k in('id','name','status','conclusion','html_url')}for j in jobs]
            try:row['job_check']=validation_jobs(file,run.get('event'),jobs,(self.root/run['path']).read_text(),allow_pending=run['status']!='completed')
            except ValueError as error:row['job_check']={'status':'FAILED','error':str(error)}
            postmerge.append(row)
        failed=[r for r in postmerge if r.get('job_check',{}).get('status')=='FAILED'or r['status']=='completed'and(r['conclusion']!='success'or r.get('job_check',{}).get('status')!='SUCCESS')]
        pending=[r for r in postmerge if r['status']!='completed'or r.get('job_check',{}).get('status')=='PENDING']
        postmerge_status='FAILED'if failed else 'PENDING'if pending else 'ALL_SUCCESS'
        additional_production=[]
        for run in main_runs:
            if run.get('event')not in {'workflow_run','workflow_dispatch'}or run.get('path')not in {'.github/workflows/exam-study-qa.yml','.github/workflows/representative-quality-qa.yml'}:continue
            row={k:run.get(k)for k in('id','name','head_sha','event','path','status','conclusion','html_url')};jobs=self.paged(f'repos/{REPO}/actions/runs/{run["id"]}/jobs','jobs',label+'-additional-production-jobs-'+str(run['id']));row['jobs']=[{k:j.get(k)for k in('id','name','status','conclusion','html_url')}for j in jobs];row['final_trigger_and_production_completion_credit']=0;additional_production.append(row)
        deployments=self.paged(f'repos/{REPO}/deployments?sha={a.merge_sha}',None,label+'-deployments');success=[]
        for d in deployments:
            if d.get('sha')!=a.merge_sha:continue
            statuses=self.paged(f'repos/{REPO}/deployments/{d["id"]}/statuses',None,label+'-deployment-'+str(d['id']))
            if statuses and statuses[0].get('state')=='success':
                url=statuses[0].get('environment_url','');require(url.rstrip('/')==ORIGIN.rstrip('/'),'Deployment succeeded for a different origin');success.append(d['id'])
        require(success,'No fresh successful exact-merge deployment status')
        record={'observed_at':now(),'candidate':a.candidate_sha,'merge':a.merge_sha,'four_way_tree_equivalent':True,'tree':trees[0],'pages_run_id':a.pages_run_id,'exact_pages_success':True,'successful_deployment_ids':success,'required_candidate_qa_runs':qa,'candidate_QA_status':'ALL_SUCCESS','postmerge_core_8_plus_successful_Pages_status':postmerge_status,'postmerge_core_workflows':postmerge,'postmerge_additional_production_observations':additional_production,'final_main9_and_production2_completion_asserted':False,'binding_status':'PASS'};self.write('api-'+label+'-summary.json',record);return record
    def assets(self,label):
        def one(item):
            path,expected=item;url=ORIGIN+path;require(not urlsplit(url).query and not urlsplit(url).fragment,'Canonical asset URL contains query/fragment');headers={'User-Agent':'MPJE-Exact-Candidate-Public-Verifier/1','Cache-Control':'no-cache','Pragma':'no-cache'};row={'path':path,'url':url,'expected_sha256':expected,'started_at':now(),'request_headers':headers}
            try:
                with urllib.request.urlopen(urllib.request.Request(url,headers=headers,method='GET'),timeout=60)as response:raw=response.read();row.update(http_status=response.status,final_url=response.url,response_headers=dict(response.headers),bytes=len(raw),response_sha256=sha(raw));target=self.out/'https'/label/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw);row['raw_path']=str(target.relative_to(self.out));row['matches_expected']=response.status==200 and response.url==url and sha(raw)==expected
            except Exception as e:row.update(error=repr(e),matches_expected=False)
            row['completed_at']=now();return row
        with ThreadPoolExecutor(max_workers=4)as pool:rows=list(pool.map(one,self.expected.items()))
        failures=[r['path']for r in rows if not r['matches_expected']];record={'observed_at':now(),'canonical_origin':ORIGIN,'query_or_cachebuster_used':False,'TLS_verification':True,'candidate':self.a.candidate_sha,'merge':self.a.merge_sha,'requests':rows,'count':len(rows),'matched':sum(r['matches_expected']for r in rows),'critical14':list(CRITICAL14),'failures':failures};self.write('https40-'+label+'.json',record);require(not failures and len(rows)==40,'Fresh canonical response mismatch: '+str(failures));return record
    def json_js(self,path,prefix):return json.loads((self.site/path).read_text().split(prefix,1)[1].rsplit(';',1)[0])
    def rebuild_expected_bytes(self):
        # Future explicit execution only: publisher output is external, never ROOT/site.
        self.stable();target=self.out/'source-bound-publish-rebuild';cmd=[self.a.python,'scripts/publish_practice.py','--output',str(target)];started=now();tick=time.monotonic();log=self.out/'source-bound-publish-rebuild.log'
        with log.open('wb')as f:p=subprocess.run(cmd,cwd=self.root,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=f,stderr=subprocess.STDOUT)
        self.stable();actual={x.relative_to(target).as_posix():sha(x.read_bytes())for x in target.rglob('*')if x.is_file()}
        self.write('source-bound-publish-rebuild.json',{'started_at':started,'completed_at':now(),'wall_seconds':time.monotonic()-tick,'command':cmd,'source_head':self.a.merge_sha,'exit_code':p.returncode,'log_sha256':sha(log.read_bytes()),'all_file_sha256':actual,'matches_new_expected_manifest':actual==self.expected})
        require(p.returncode==0 and actual==self.expected,'Fresh external publisher bytes differ from new exact candidate manifest')
    def candidate_metrics(self):
        progress=json.loads((self.root/'reports/full-corpus-review/progress.json').read_bytes());rows=[json.loads(x)for x in(self.root/'reports/full-corpus-review/question-ledger.jsonl').read_text().splitlines()];by={r['question_id']:r for r in rows};require(len(by)==len(rows),'Duplicate current question IDs')
        excluded=set(progress['independent_legacy_context38_supplementary_review']['excluded_context_conditioned_primary_key_ids']);primary={uid for uid,r in by.items()if r['independent_legacy_legal_assessment']['existing_answer_correct']!='NOT_ASSESSED'};supp={uid for uid,r in by.items()if r.get('independent_legacy_supplementary_assessment',{}).get('record',{}).get('legal_review',{}).get('existing_answer_correct','NOT_ASSESSED')!='NOT_ASSESSED'};effective=(primary-excluded)|supp
        notes=self.json_js('notes/content.js','window.MPJE_NOTES = ');units=[u for c in notes['chapters']for u in c['units']];nu=[json.loads(x)for x in(self.root/'reports/full-corpus-review/notes-unit-ledger.jsonl').read_text().splitlines()];np=notes['independent_note_review_progress'];require(np==progress['independent_note_completeness_legal_review'],'Candidate notes payload census differs from current progress')
        markup=(self.site/'practice-expansion/index.html').read_text();match=re.search(r'<script\b[^>]*\bid="payload"[^>]*>(.*?)</script>',markup,re.S);require(match,'Published practice payload not found');practice=json.loads(match.group(1));selection=json.loads((self.root/'practice_expansion/2026-10-28-representative/selection.json').read_bytes());require(practice['quality_selection']['recommended_ids']==selection['recommended_ids'],'Default ID order changed in published payload')
        bankpath='practice_expansion/2026-10-28-representative/questions.json';bank=json.loads((self.root/bankpath).read_bytes());require(sha((self.root/bankpath).read_bytes())==BANK77_SHA,'Preserved77 bank bytes changed')
        metrics={'questions':len(by),'key_assessed':len(effective),'key_unassessed':len(by)-len(effective),'effective_realism_PASS':progress['independent_legacy_realism_pass'],'note_units':len(units),'note_claims':sum(len(u['atomic_claim_ids'])for u in nu),'claim_LEGAL_HOLD':np['claim_legal_hold_count'],'claim_SOURCE_BLOCKED':np['claim_source_blocked_count'],'default_questions':len(selection['recommended_ids']),'representative_questions':len(bank['questions'])};require(metrics==APPROVED_SCOPE,'Computed candidate scope differs from approved current task: '+str(metrics));require(len(practice['questions'])==len(by)and np['complete_units']==np['processed_units']==306,'Candidate corpus/census incomplete')
        require(len(effective)==progress['independent_legacy_legal_assessed']and len(by)-len(effective)==progress['independent_legacy_keys_unassessed'],'Effective legal union/progress mismatch')
        collections={}
        for r in rows:
            if r['collection']not in collections:collections[r['collection']]={q['question_id']:q for q in json.loads((self.root/r['collection']).read_bytes())['questions']}
            q=collections[r['collection']][r['question_id']];require(sha(canonical(q))==r['content_sha256'],'Current question hash mismatch: '+r['question_id'])
        rawpass={uid for uid,r in by.items()if r['independent_legacy_realism_assessment']['verdict']=='PASS'}
        fresh38={uid:r['independent_legacy_supplementary_assessment']['record']for uid,r in by.items()if uid in excluded and r.get('independent_legacy_supplementary_assessment',{}).get('record',{}).get('realism_review',{}).get('verdict')=='PASS'}
        exposed=set()
        for uid,r in fresh38.items():
            rs=r.get('read_scope',{})
            if any(rs.get(k)is True for k in('accidental_hidden_truth_exposure','prior_author_or_independent_conclusions_read','prior_question_author_or_independent_verdicts_read','hidden_statement_truth_read','hidden_truth_used_as_evidence'))or any(isinstance(rs.get(k),str)and'ACCIDENTAL'in rs[k].upper()for k in('hidden_truth','prior_assigned_author_or_independent_conclusions')):exposed.add(uid)
        conflicts={uid for uid in fresh38 if by[uid]['independent_legacy_realism_assessment']['verdict']=='FAIL'};basepass=(rawpass-excluded)|(set(fresh38)-conflicts-exposed)
        rs=json.loads((self.root/'reports/full-corpus-review/realism-completion-v1/controller-scope.json').read_bytes());priorpass={uid for uid,rr in rs['prior_supplementary'].items()if any(x['realism_verdict']=='PASS'for x in rr)};priornegative={uid for uid,rr in rs['prior_supplementary'].items()if any(x['realism_verdict']in{'FAIL','HOLD','MINOR_EDIT','MAJOR_REWRITE'}for x in rr)}
        freshpass={uid for uid,r in by.items()if r.get('independent_legacy_realism_supplementary_assessment',{}).get('record',{}).get('realism_review',{}).get('verdict')=='PASS'};blocked={uid for uid in freshpass if by[uid]['independent_legacy_realism_assessment']['verdict']in{'HOLD','MINOR_EDIT','MAJOR_REWRITE','FAIL'}}|(freshpass&priornegative)
        require(len(basepass|(freshpass-(rawpass|priorpass)-blocked))==metrics['effective_realism_PASS'],'Effective realism union/progress mismatch')
        bodymap={u['unit_id']:u['actual_effective_body_sha256']for u in nu};require({u['id']:u['body_sha256']for u in units}==bodymap,'Published306 unit body hashes changed')
        claim_counts={kind:sum(u['independent_atomic_census_review']['claim_counts'].get(kind,0)for u in units)for kind in('KEEP','LEGAL_HOLD','SOURCE_BLOCKED')}
        require(claim_counts=={'KEEP':np['claim_keep_count'],'LEGAL_HOLD':metrics['claim_LEGAL_HOLD'],'SOURCE_BLOCKED':metrics['claim_SOURCE_BLOCKED']}and sum(claim_counts.values())==metrics['note_claims'],'Actual candidate public unit claim counts do not match7086/36/890')
        require(np['coverage_is_legal_pass']is False and np['canonical_release_credit']==np['question_audit_credit']==0 and practice['canonical_released_question_count']==0,'Census/publication incorrectly grants legal/canonical credit')
        for field in('claim_keep_count','claim_legal_hold_count','claim_source_blocked_count'):require(np[field]==progress['independent_note_completeness_legal_review'][field],'Claim status count mismatch')
        quality=html.unescape(re.sub('<[^>]+>',' ',(self.site/'practice-expansion/quality-review.html').read_text()));require(f'{metrics["key_assessed"]}/{metrics["questions"]}'in quality and '306/306'in quality and f'현실성 PASS {metrics["effective_realism_PASS"]}'in quality,'Candidate quality page has stale counts')
        n1=next(u for u in units if u['id']=='w3-a-3');review=n1['independent_atomic_census_review'];require(review['legal_status']=='LEGAL_HOLD'and review['requires_review']and review['current_review_valid']and review['review_history']and any(f['claim_id']=='NOTE-WAVE8-W3-A-3-011'and f['legal_status']=='LEGAL_HOLD'and f.get('blocker')for f in review['findings']),'Candidate N1 HOLD011/history missing')
        case=by['MA-CASE-0790'];require(case['disposition']=='HOLD_FOR_LEGAL_REVIEW'and case['independent_legacy_legal_assessment']['verdict']=='HOLD'and case['independent_legacy_realism_assessment']['verdict']=='NOT_ASSESSED'and case['independent_legacy_realism_supplementary_assessment']['record']['realism_review']['verdict']=='FAIL'and case['independent_legacy_supplementary_assessment']['record']['legal_review']['verdict']=='KEEP','CASE0790 actual primary/supplementary grades changed')
        require('MA-CASE-0790'not in selection['recommended_ids'],'CASE0790 restored to default');notices=[n for n in selection['archive_review_notices']if'MA-CASE-0790'in n['question_ids']];require(notices and all(n.get('previous_notices')and n.get('reason')for n in notices),'CASE0790 negative or previous history missing');require([n for n in practice['representative_revision']['archive_review_notices']if'MA-CASE-0790'in n['question_ids']]==notices,'Published CASE0790 source/history differs')
        self.write('candidate-derived-metrics.json',{'observed_at':now(),'metrics':metrics,'progress_raw_sha256':sha((self.root/'reports/full-corpus-review/progress.json').read_bytes()),'note_progress':np,'CASE0790_primary_and_supplementary_and_notice_history_preserved':True,'new_canonical_credit':0});return metrics,notes,practice
    def browsers(self):
        adapter=self.out/'origin-only-browser-adapter.py'
        adapter.write_text('''from pathlib import Path\nimport ast,json,sys\nROOT=Path('''+repr(str(self.root))+''')\nOUT=Path('''+repr(str(self.out))+''')\nsys.path.insert(0,'''+repr(str(Path(__file__).resolve().parent))+''')\nfrom final306_public_verifier import adapt_browser_source\nname=sys.argv[1]\nassert name in {'verify_notes_browser.py','verify_refresh_browser.py'}\nassert '--inline-preview' not in sys.argv\np=ROOT/'scripts'/name\nadapted,proof=adapt_browser_source(name,p.read_text())\n(OUT/(name+'.origin-adapter.json')).write_text(json.dumps(proof,indent=2)+'\\n')\nsys.path.insert(0,str(ROOT/'scripts'))\nsys.argv=[str(p),*sys.argv[2:]]\nexec(compile(adapted,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})\n''')
        a=self.a;cases=[('public-practice',[a.python,'scripts/verify_public_practice.py','--base-url',ORIGIN,'--site',str(self.site),'--output',str(self.out/'public-practice')]),('notes',[a.python,str(adapter),'verify_notes_browser.py','--output',str(self.out/'notes')]),('refresh',[a.python,str(adapter),'verify_refresh_browser.py','--site',str(self.site),'--output',str(self.out/'refresh')]),('q0012-withdrawal',[a.python,'scripts/verify_q0012_withdrawal_browser.py','--base-url',ORIGIN,'--site',str(self.site),'--output',str(self.out/'q0012-withdrawal')]),('representative-rewrites',[a.python,'scripts/verify_representative_rewrites.py','--base-url',ORIGIN,'--site',str(self.site),'--evidence',str(self.out/'representative-rewrites')])];runs=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
        for name,cmd in cases:
            self.stable();start=now();tick=time.monotonic();log=self.out/(name+'.log')
            with log.open('wb')as f:p=subprocess.run(cmd,cwd=self.root,env=env,stdout=f,stderr=subprocess.STDOUT)
            self.stable();row={'suite':name,'argv':cmd,'cwd':str(self.root),'started_at':start,'completed_at':now(),'wall_seconds':time.monotonic()-tick,'exit_code':p.returncode,'actual_origin':ORIGIN,'source_head':self.a.merge_sha,'raw_log_sha256':sha(log.read_bytes()),'isolated_synthetic_storage':True,'real_user_profile_used':False};self.write(name+'-execution.json',row);runs.append(row)
        self.write('browser-runs.json',runs);require(all(x['exit_code']==0 for x in runs),'Actual browser suite failed; preserve evidence, no bypass')
        for name,_ in cases:
            report=json.loads((self.out/name/'report.json').read_bytes());errs=report.get('page_errors',report.get('errors',report.get('javascript_errors',[])));require(not errs,'Browser reported JS errors: '+name)
        practice_report=json.loads((self.out/'public-practice/report.json').read_bytes());require(practice_report.get('environment')=='production HTTP'and practice_report.get('passed',0)>0,'Practice report was not actual production HTTP')
        note_report=json.loads((self.out/'notes/report.json').read_bytes());require(note_report.get('mode')=='http-browser-regression'and note_report.get('storage_and_navigation_tested')is True and note_report.get('checks_passed')and not note_report.get('external_requests'),'Notes real-origin navigation/storage not verified')
        refresh_report=json.loads((self.out/'refresh/report.json').read_bytes());require(refresh_report.get('mode')=='REAL_HTTP_REAL_ORIGIN_STORAGE'and refresh_report.get('count',0)>0,'Refresh report used simulated storage')
        rewrite_report=json.loads((self.out/'representative-rewrites/report.json').read_bytes());require(rewrite_report.get('mode')=='PRODUCTION_HTTP_REAL_ORIGIN'and rewrite_report.get('status')=='passed'and rewrite_report.get('new_cases_planned')==rewrite_report.get('new_cases_exercised')==77,'All77 representative cases were not exercised on actual production origin')
        withdrawal=json.loads((self.out/'q0012-withdrawal/report.json').read_bytes());require(withdrawal.get('status')=='PASS'and withdrawal.get('base_url')==ORIGIN and withdrawal.get('head')==self.a.merge_sha and withdrawal.get('stored_session_answers_hash_and_score_preserved')and withdrawal.get('bookmarks_wrong_and_completed_preserved'),'Q0012 actual-origin session/progress preservation failed')
        return runs
    def public_state(self,metrics,expected_notes,expected_practice):
        from playwright.sync_api import sync_playwright,expect
        errors=[];requests=[];checks={};directory=self.out/'public-state';directory.mkdir()
        with sync_playwright()as p:
            launch={'headless':True}
            if os.environ.get('CHROMIUM_PATH'):launch['executable_path']=os.environ['CHROMIUM_PATH']
            browser=p.chromium.launch(**launch);context=browser.new_context(viewport={'width':1440,'height':1000});page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append({'method':r.method,'url':r.url}))
            page.goto(ORIGIN+'practice-expansion/quality-review.html',wait_until='networkidle');expect(page.locator('tr').filter(has_text='독립 legacy 정답 평가')).to_contain_text(f'{metrics["key_assessed"]}/{metrics["questions"]}');expect(page.locator('tr').filter(has_text='독립 노트 열거 완전성 확인')).to_contain_text('306/306');page.screenshot(path=str(directory/'quality-current.png'),full_page=True)
            page.goto(ORIGIN+'practice-expansion/',wait_until='networkidle');diag=page.evaluate('MPJE_DIAGNOSTICS()');require(diag['total']==metrics['questions']and diag['filtered']==metrics['default_questions'],'Actual practice diagnostics mismatch');actual=page.evaluate('JSON.parse(document.querySelector("#payload").textContent)');require(actual==expected_practice,'Actual live practice payload differs from expected candidate')
            page.goto(ORIGIN+'practice-expansion/#MA-CASE-0790',wait_until='networkidle');expect(page.locator('#q-meta')).to_contain_text('MA-CASE-0790');expected_notice=next(n for n in expected_practice['representative_revision']['archive_review_notices']if'MA-CASE-0790'in n['question_ids']);expect(page.locator('.archive-review-warning')).to_contain_text(expected_notice['reason']);page.screenshot(path=str(directory/'case0790-preserved-hold.png'),full_page=True)
            page.goto(ORIGIN+'notes/',wait_until='networkidle');actual_notes=page.evaluate('window.MPJE_NOTES');require(actual_notes==expected_notes,'Actual public notes payload differs from candidate');unit=next(u for c in actual_notes['chapters']for u in c['units']if u['id']=='w3-a-3');chapter=next(c['id']for c in actual_notes['chapters']if any(u['id']=='w3-a-3'for u in c['units']));page.goto(ORIGIN+'notes/#chapter/'+chapter+'/w3-a-3',wait_until='networkidle');expect(page.locator('#w3-a-3')).to_contain_text('보류');page.screenshot(path=str(directory/'N1-held011-history.png'),full_page=True)
            page.goto(ORIGIN+'notes/#study/today',wait_until='networkidle');page.wait_for_function('(()=>{const s=JSON.parse(localStorage.getItem("oddments.mpje.exam-study.v1")||"null");return !!s?.daily?.ids?.length})()');study=page.evaluate('({state:JSON.parse(localStorage.getItem("oddments.mpje.exam-study.v1")),lessons:MPJE_EXAM_STUDY.lessons})');n1lessons={x['id']for x in study['lessons']if'w3-a-3'in x['note_units']};require(n1lessons and not n1lessons.intersection(study['state']['daily']['ids']),'N1 entered actual study daily selection')
            page.goto(ORIGIN+'notes/#refresh/today',wait_until='networkidle');page.wait_for_function('(()=>{const s=JSON.parse(localStorage.getItem("oddments.mpje.refresh.v1")||"null");return !!s?.daily?.ids?.length})()');refresh=page.evaluate('({state:JSON.parse(localStorage.getItem("oddments.mpje.refresh.v1")),cards:MPJE_REFRESH.cards})');n1cards={x['id']for x in refresh['cards']if'w3-a-3'in x['note_units']};require(n1cards and not n1cards.intersection(refresh['state']['daily']['ids']),'N1 entered actual refresh daily selection');page.screenshot(path=str(directory/'N1-daily-excluded.png'),full_page=True)
            require(not errors and all(r['method']=='GET'for r in requests),'Actual public-state JS/network mutation error');checks={'practice_diagnostics':diag,'metrics':metrics,'N1_review':unit['independent_atomic_census_review'],'N1_body_sha256':unit['body_sha256'],'study_daily_ids':study['state']['daily']['ids'],'N1_study_lesson_ids':sorted(n1lessons),'refresh_daily_ids':refresh['state']['daily']['ids'],'N1_refresh_card_ids':sorted(n1cards),'N1_daily_selected':0,'CASE0790_exact_source_notice_and_negative_history_retained':True,'javascript_errors':errors,'requests':requests,'browser_version':browser.version,'real_user_profile_used':False,'canonical_or_legal_audit_credit':0};browser.close()
        self.write('public-state/report.json',{'observed_at':now(),'status':'PASS',**checks});return checks
    def run(self):
        self.stable();initial=self.api_snapshot('initial');self.rebuild_expected_bytes();metrics,notes,practice=self.candidate_metrics();self.assets('initial');runs=self.browsers();state=self.public_state(metrics,notes,practice);self.assets('final');final=self.api_snapshot('final');self.stable();require(initial['tree']==final['tree'],'Deployed tree moved during verification')
        self.write('observation.json',{'observed_at':now(),'public_software_checks_status':'PASS','candidate_QA_status':'ALL_SUCCESS','postmerge_core_8_plus_successful_Pages_status':final['postmerge_core_8_plus_successful_Pages_status'],'overall_status':'PUBLIC_VERIFIED_MAIN_'+final['postmerge_core_8_plus_successful_Pages_status']+'_FINAL_PRODUCTION_PROOF_PENDING','postmerge_additional_production_observations':final['postmerge_additional_production_observations'],'overall_release_completion_asserted':False,'requires_separate_final_main9_plus_production2_success_proof':True,'exact_candidate':self.a.candidate_sha,'exact_merge':self.a.merge_sha,'tree':final['tree'],'origin':ORIGIN,'canonical40_matched':40,'critical14_matched':14,'browser_suites_passed':len(runs),'N1_daily_selected':state['N1_daily_selected'],'actual_metrics':metrics,'pages_run_id':self.a.pages_run_id,'required_QA_run_ids':self.a.qa_run_ids,'old_PR193_results_reused':False,'question_or_canonical_audit_credit':0,'physical_device_testing':False})
        return final['postmerge_core_8_plus_successful_Pages_status']
    def finish_manifest(self):
        self.write('artifact-sha256.json',{p.relative_to(self.out).as_posix():sha(p.read_bytes())for p in sorted(self.out.rglob('*'))if p.is_file()})

def main(argv=None):
    a=parser().parse_args(argv);v=None
    try:
        v=Verification(a);postmerge=v.run();v.finish_manifest();print(json.dumps({'public_software_checks_status':'PASS','postmerge_core_status':postmerge,'overall_release_completion_asserted':False,'postmerge_status_in':'api-final-summary.json','evidence':str(v.out)}));return 1 if postmerge=='FAILED'else 0
    except Exception as error:
        if v is not None:
            v.write('failure.json',{'observed_at':now(),'status':'FAIL','error':repr(error),'no_release_or_audit_credit':True});v.finish_manifest()
        print('VERIFICATION FAILED: '+repr(error),file=sys.stderr);return 1
if __name__=='__main__':raise SystemExit(main())
