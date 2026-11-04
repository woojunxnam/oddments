import urllib.request,json,hashlib,datetime,subprocess,shutil
from pathlib import Path
B=Path('reports/full-corpus-review/independent-notes/notes101-final-second-b');(B/'sources').mkdir(parents=True,exist_ok=True)
for n,f in [('assignment','notes101-final-second-b-assignment.json'),('visible-input','notes101-final-second-b-visible-input.json'),('related-context','notes101-final-second-b-related-context.json')]:shutil.copyfile('/workspace/scratch/'+f,B/(n+'.json'))
for key,url in [('licensure','https://www.mass.gov/doc/247-cmr-3-pharmacist-licensure-requirements/download'),('reporting','https://www.mass.gov/doc/247-cmr-20-reporting-and-disciplinary-action/download')]:
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (Independent legal source review)'}),timeout=45) as r:raw=r.read();status=r.status;resolved=r.url;headers=dict(r.headers)
  assert raw.startswith(b'%PDF');rp=B/'sources'/(key+'.pdf');tp=B/'sources'/(key+'.txt');rp.write_bytes(raw);subprocess.run(['pdftotext','-layout',str(rp),str(tp)],check=True)
  m={'official_url':url,'retrieved_at':t,'retrieval_status':'LIVE_HTTPS_GET','method':'urllib HTTPS GET; inherited proxy; TLS verification enabled','status':status,'resolved_url':resolved,'headers':headers,'raw_path':str(rp),'raw_sha256':hashlib.sha256(raw).hexdigest(),'text_path':str(tp),'text_sha256':hashlib.sha256(tp.read_bytes()).hexdigest()}
 except Exception as e:m={'official_url':url,'attempted_at':t,'retrieval_status':'LIVE_GET_FAILED','error':str(e)}
 (B/'sources'/(key+'.meta.json')).write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print(json.dumps(m,ensure_ascii=False))
