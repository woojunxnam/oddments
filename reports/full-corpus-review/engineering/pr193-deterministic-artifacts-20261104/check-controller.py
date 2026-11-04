import os,subprocess,json,time
from pathlib import Path
from datetime import datetime,timezone
qa=Path('/workspace/mpje-pr193-qa');out=Path('/workspace/scratch/mpje-pr193-2a7-all-deterministic-checks-v1');out.mkdir(exist_ok=False)
python='/workspace/mpje-ci-checks-venv/bin/python'
commands=[
 ('representative-rewrites',[python,'scripts/build_representative_rewrites.py','--check']),
 ('representative-audit-ledger',[python,'scripts/build_representative_audit_ledger.py','--check']),
 ('representative-similarity',[python,'scripts/audit_representative_similarity.py','--check']),
 ('full-protection',[python,'scripts/verify_representative_protected.py']),
 ('full-corpus',[python,'scripts/build_full_corpus_review.py','--check']),
 ('quality-status',[python,'scripts/build_quality_status.py','--check']),
 ('exam-study',[python,'scripts/build_exam_study.py','--check']),
 ('refresh',[python,'scripts/build_refresh.py','--check']),
 ('ultimate-notes',[python,'scripts/build_ultimate_notes.py','--check']),
 ('quality-javascript',['node','--check','site/practice-expansion/quality-core.js']),
 ('external-publication',[python,'scripts/publish_practice.py','--output',str(out/'published-site')]),
]
head=lambda:subprocess.check_output(['git','-C',str(qa),'rev-parse','HEAD'],text=True).strip()
fixed=head();assert fixed=='2a7f76e5a2cb785a60cf78dc125bd4a7715f4f7a'
runs=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
for name,command in commands:
 assert head()==fixed
 start=time.monotonic();began=datetime.now(timezone.utc).isoformat();log=out/(name+'.log')
 print('START',name,flush=True)
 with log.open('w')as stream:
  completed=subprocess.run(command,cwd=qa,env=env,stdout=stream,stderr=subprocess.STDOUT)
 row=dict(name=name,command=command,started_at_utc=began,ended_at_utc=datetime.now(timezone.utc).isoformat(),seconds=round(time.monotonic()-start,2),exit_code=completed.returncode,log=str(log),qa_head=fixed)
 assert head()==fixed
 runs.append(row);(out/'runs.json').write_text(json.dumps(runs,ensure_ascii=False,indent=2)+'\n')
 print('END',name,'exit',completed.returncode,'seconds',row['seconds'],flush=True)
print('COMPLETE',len(runs),'failed',sum(r['exit_code']!=0 for r in runs),flush=True)
