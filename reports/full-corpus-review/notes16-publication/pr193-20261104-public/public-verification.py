"""Actual public PR193 deployment evidence; only this evidence prefix is written."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import urllib.request

ROOT=Path('/workspace/mpje-pr193-public')
OUT=ROOT/'reports/full-corpus-review/notes16-publication/pr193-20261104-public'
ORIGIN='https://woojunxnam.github.io/oddments/'
MERGE='c8e8f7b825e576887220867b322779dc5b1c8d67'
CANDIDATE='12d1751707f917737736b1aba208b2468d054d72'
PYTHON='/workspace/mpje-ci-checks-venv/bin/python'
EXPECTED=Path('/workspace/scratch/pr193-12d175-build-output-equivalence.json')
SITE=Path('/workspace/scratch/mpje-pr193-12d175-site')

def now():return datetime.now(timezone.utc).isoformat()
def sha(raw):return hashlib.sha256(raw).hexdigest()
def write(path,value):
    path=OUT/path
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args],text=True).strip()

def api_snapshot(label):
    endpoints={
      'pull193':'repos/woojunxnam/oddments/pulls/193',
      'merge_commit':'repos/woojunxnam/oddments/git/commits/'+MERGE,
      'candidate_commit':'repos/woojunxnam/oddments/git/commits/'+CANDIDATE,
      'main_ref':'repos/woojunxnam/oddments/git/ref/heads/main',
      'pages_run':'repos/woojunxnam/oddments/actions/runs/41907593476',
      'pages_jobs':'repos/woojunxnam/oddments/actions/runs/41907593476/jobs',
      'merge_runs':'repos/woojunxnam/oddments/actions/runs?head_sha='+MERGE+'&per_page=100',
      'merge_checks':'repos/woojunxnam/oddments/commits/'+MERGE+'/check-runs?per_page=100',
      'candidate_runs':'repos/woojunxnam/oddments/actions/runs?head_sha='+CANDIDATE+'&per_page=100',
      'deployments':'repos/woojunxnam/oddments/deployments?sha='+MERGE+'&per_page=100',
    }
    data={}
    for name,endpoint in endpoints.items():
        start=now();result=subprocess.run(['gh','api',endpoint],capture_output=True)
        target=Path('api')/label/(name+'.json')
        raw_path=Path('api')/label/(name+'.response.json')
        (OUT/raw_path).parent.mkdir(parents=True,exist_ok=True)
        (OUT/raw_path).write_bytes(result.stdout)
        payload=json.loads(result.stdout) if result.returncode==0 else {'error':result.stderr.decode()}
        write(target,{'observed_at_utc':start,'command':['gh','api',endpoint],'exit_code':result.returncode,
                      'response_raw_path':raw_path.as_posix(),'response_raw_sha256':sha(result.stdout),'response':payload})
        data[name]=payload
    for run in data.get('merge_runs',{}).get('workflow_runs',[]):
        runid=run['id'];endpoint='repos/woojunxnam/oddments/actions/runs/'+str(runid)+'/jobs?per_page=100'
        result=subprocess.run(['gh','api',endpoint],capture_output=True)
        write(Path('api')/label/('merge-run-'+str(runid)+'-jobs.json'),
              {'observed_at_utc':now(),'command':['gh','api',endpoint],'exit_code':result.returncode,
               'response':json.loads(result.stdout) if result.returncode==0 else result.stderr.decode()})
    for deployment in data.get('deployments',[]):
        endpoint='repos/woojunxnam/oddments/deployments/'+str(deployment['id'])+'/statuses'
        result=subprocess.run(['gh','api',endpoint],capture_output=True)
        write(Path('api')/label/('deployment-'+str(deployment['id'])+'-statuses.json'),
              {'observed_at_utc':now(),'command':['gh','api',endpoint],'exit_code':result.returncode,
               'response':json.loads(result.stdout) if result.returncode==0 else result.stderr.decode()})
    merge_tree=data['merge_commit']['tree']['sha'];candidate_tree=data['candidate_commit']['tree']['sha']
    local_merge=git('rev-parse',MERGE+'^{tree}');local_candidate=git('rev-parse',CANDIDATE+'^{tree}')
    summary=dict(observed_at_utc=now(),merge_sha=MERGE,candidate_sha=CANDIDATE,
      api_merge_tree=merge_tree,api_candidate_tree=candidate_tree,local_merge_tree=local_merge,
      local_candidate_tree=local_candidate,tree_equivalent=len({merge_tree,candidate_tree,local_merge,local_candidate})==1,
      merged=data['pull193']['merged'],pr_merge_sha=data['pull193']['merge_commit_sha'],
      pages_head=data['pages_run']['head_sha'],pages_status=data['pages_run']['status'],pages_conclusion=data['pages_run']['conclusion'],
      merge_workflows=[{k:r.get(k) for k in ('id','name','head_sha','status','conclusion','html_url')}for r in data['merge_runs']['workflow_runs']])
    write('api-'+label+'-summary.json',summary)
    print(json.dumps(summary,ensure_ascii=False),flush=True)

def fetch40(label):
    expected=json.loads(EXPECTED.read_bytes());hashes=expected['all_file_sha256']
    local={p:sha((SITE/p).read_bytes()) for p in hashes}
    assert local==hashes and len(hashes)==40
    def one(item):
        path,digest=item;url=ORIGIN+path;start=now();headers={'User-Agent':'MPJE-PR193-Public-Verification/1','Cache-Control':'no-cache','Pragma':'no-cache'}
        row=dict(path=path,url=url,request_headers=headers,started_at_utc=start,expected_sha256=digest)
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=50) as response:
                raw=response.read();row.update(status=response.status,final_url=response.url,response_headers=dict(response.headers),
                    response_bytes=len(raw),response_sha256=sha(raw),matches_expected=sha(raw)==digest)
                if path in ('practice-expansion/build.json','practice-expansion/publication.json','notes/build.json','notes/study-build.json','notes/refresh-build.json'):
                    row['response_json']=json.loads(raw)
        except Exception as error:row.update(error=repr(error),matches_expected=False)
        row['completed_at_utc']=now();return row
    with ThreadPoolExecutor(max_workers=4)as pool:rows=list(pool.map(one,hashes.items()))
    report=dict(observed_at_utc=now(),origin=ORIGIN,mode='CANONICAL_URLS_NO_QUERY_PARAMETERS',tls_verification=True,
        source_commit=MERGE,expected_build_commit=CANDIDATE,expected_manifest_sha256=sha(EXPECTED.read_bytes()),
        expected_manifest=expected,local_expected_bytes_verified=True,total=len(rows),matched=sum(r['matches_expected']for r in rows),
        failures=[r['path']for r in rows if not r['matches_expected']],requests=rows)
    write('https40-'+label+'.json',report)
    print(json.dumps({k:report[k] for k in ('observed_at_utc','total','matched','failures')},ensure_ascii=False),flush=True)

def cli_help():
    reports=[]
    for script in ('verify_public_practice.py','verify_notes_browser.py','verify_refresh_browser.py','verify_q0012_withdrawal_browser.py','verify_representative_rewrites.py'):
        command=[PYTHON,'scripts/'+script,'--help'];result=subprocess.run(command,cwd=ROOT,capture_output=True)
        text=result.stdout.decode()+result.stderr.decode();(OUT/(script+'.help.txt')).write_text(text)
        reports.append(dict(command=command,exit_code=result.returncode,source_sha256=sha((ROOT/'scripts'/script).read_bytes()),
                            help_sha256=sha(text.encode()),supports_base_url='--base-url'in text))
    write('cli-help.json',reports);print(json.dumps(reports,ensure_ascii=False),flush=True)

def browsers():
    cases=[
      ('public-practice',[PYTHON,'scripts/verify_public_practice.py','--base-url',ORIGIN,'--site',str(SITE),'--output',str(OUT/'public-practice')]),
      ('notes',[PYTHON,str(OUT/'production-browser-adapter.py'),'verify_notes_browser.py','--output',str(OUT/'notes')]),
      ('refresh',[PYTHON,str(OUT/'production-browser-adapter.py'),'verify_refresh_browser.py','--site',str(SITE),'--output',str(OUT/'refresh')]),
      ('q0012-withdrawal',[PYTHON,'scripts/verify_q0012_withdrawal_browser.py','--base-url',ORIGIN,'--site',str(SITE),'--output',str(OUT/'q0012-withdrawal')]),
      ('representative-rewrites',[PYTHON,'scripts/verify_representative_rewrites.py','--base-url',ORIGIN,'--site',str(SITE),'--evidence',str(OUT/'representative-rewrites')]),
    ]
    assert git('rev-parse','HEAD')==MERGE
    rows=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
    for name,command in cases:
        start=now();tick=time.monotonic();print('START',name,start,flush=True)
        with(OUT/(name+'.log')).open('w')as log:
            result=subprocess.run(command,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
        row=dict(name=name,command=command,started_at_utc=start,ended_at_utc=now(),seconds=round(time.monotonic()-tick,2),
          exit_code=result.returncode,actual_origin=ORIGIN,source_head_before=MERGE,source_head_after=git('rev-parse','HEAD'),
          log_path=name+'.log',log_sha256=sha((OUT/(name+'.log')).read_bytes()))
        rows.append(row);write('browser-runs.json',rows);print('END',name,'exit',result.returncode,'seconds',row['seconds'],flush=True)
        assert row['source_head_after']==MERGE
    print('COMPLETE',len(rows),'failed',sum(row['exit_code']!=0 for row in rows),flush=True)

if __name__=='__main__':
    command=sys.argv[1]
    if command=='api':api_snapshot(sys.argv[2])
    elif command=='https40':fetch40(sys.argv[2])
    elif command=='help':cli_help()
    elif command=='browsers':browsers()
    else:raise ValueError(command)
