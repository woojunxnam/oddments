from pathlib import Path
import json,subprocess,concurrent.futures,datetime
root=Path('/workspace/pr192-final');merge='e8f9b9bcffdb5cf8849ee97ba75b9526bd1cff67';base='https://woojunxnam.github.io/oddments/';site='/tmp/mpje-pr192-final-site'
commands=[('assets',['python','/tmp/verify-pr192-deployment.py',merge,'41806902060']),('public',['python','scripts/verify_public_practice.py','--site',site,'--base-url',base,'--output','/tmp/pr192-production-public']),('rewrites',['python','scripts/verify_representative_rewrites.py','--site',site,'--base-url',base,'--evidence','/tmp/pr192-production-rewrites']),('userdata',['python','scripts/verify_q0012_withdrawal_browser.py','--site',site,'--base-url',base,'--output','/tmp/pr192-production-userdata'])]
def run(item):
 name,args=item;path=Path('/tmp/pr192-production-'+name+'.log')
 with path.open('w') as log:p=subprocess.run(args,cwd=root,stdout=log,stderr=subprocess.STDOUT)
 return {'name':name,'status':'PASS' if p.returncode==0 else 'FAIL','exit_code':p.returncode,'log':str(path)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(run,commands))
r={'head':'4c6380f14b516e6486c8ce8e8fdfcf75eb9ce7aa','merge':merge,'pages_run':41806902060,'checks':rows,'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS' if all(x['status']=='PASS' for x in rows) else 'FAIL'};Path('/tmp/pr192-production-status.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));raise SystemExit(r['status']!='PASS')
