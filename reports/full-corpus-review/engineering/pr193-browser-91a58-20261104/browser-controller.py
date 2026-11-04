import os,subprocess,json,time,sys
from pathlib import Path
from datetime import datetime,timezone
qa=Path('/workspace/mpje-pr193-qa');expected=sys.argv[1];out=Path(sys.argv[2]);site=Path(sys.argv[3]);out.mkdir(exist_ok=False)
python='/workspace/mpje-ci-checks-venv/bin/python'
cases=[
 ('public-practice',[python,'scripts/verify_public_practice.py','--site',str(site),'--output',str(out/'public-practice')]),
 ('representative-rewrites',[python,'scripts/verify_representative_rewrites.py','--site',str(site),'--evidence',str(out/'representative-rewrites')]),
 ('q0012-withdrawal',[python,'scripts/verify_q0012_withdrawal_browser.py','--site',str(site),'--output',str(out/'q0012-withdrawal')]),
 ('refresh',[python,'scripts/verify_refresh_browser.py','--site',str(site),'--output',str(out/'refresh')]),
 ('notes',[python,'scripts/verify_notes_browser.py','--output',str(out/'notes')]),
]
head=lambda:subprocess.check_output(['git','-C',str(qa),'rev-parse','HEAD'],text=True).strip()
assert head()==expected
rows=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
for name,command in cases:
 if (out/'pause-after-current').exists():
  print('PAUSED_BEFORE',name,flush=True);break
 assert head()==expected
 begin=datetime.now(timezone.utc).isoformat();start=time.monotonic();log=out/(name+'.log')
 print('START',name,flush=True)
 with log.open('w')as stream:result=subprocess.run(command,cwd=qa,env=env,stdout=stream,stderr=subprocess.STDOUT)
 actual=head()
 row=dict(name=name,command=command,started_at_utc=begin,ended_at_utc=datetime.now(timezone.utc).isoformat(),
  seconds=round(time.monotonic()-start,2),exit_code=result.returncode,log=str(log),expected_qa_head=expected,
  actual_qa_head_after=actual,exact_head_valid=actual==expected)
 rows.append(row);(out/'runs.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 print('END',name,'exit',result.returncode,'seconds',row['seconds'],flush=True)
 assert actual==expected
print('COMPLETE',len(rows),'failed',sum(r['exit_code']!=0 for r in rows),flush=True)
