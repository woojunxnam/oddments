import urllib.request,urllib.error,json,hashlib,subprocess,re,html,concurrent.futures
from pathlib import Path
from datetime import datetime,timezone
E=Path(__file__).resolve().parent
loc=json.loads((E/'source-locators.json').read_text())
wanted=['src-da8a8280d110','src-4b5f3e5e6f00','src-5ae56622aa3c','src-eb2292f04d83','src-16f1fbbdd07a','src-0a51fd50980a','src-a8947630c051','src-a397fe32483f','src-b2350e40af92','src-deef2ce4e7c3','src-8614174367a6','src-ab1d7b3de5ad','src-178a92a2b64d','src-7965e55e6e8c','src-607e95c04a30','src-93c05bdb2764']
items=[s for s in loc if s['id'] in wanted]+[{'id':'cfr1306','title':'21 CFR 1306','url':'https://www.ecfr.gov/current/title-21/chapter-II/part-1306'},{'id':'fda-orange-preface','title':'FDA Orange Book Preface','url':'https://www.fda.gov/drugs/development-approval-process-drugs/orange-book-preface'},{'id':'nabp-sample','title':'NABP public MPJE sample style','url':'https://nabp.pharmacy/wp-content/uploads/2020/07/MPJE-Sample-Questions.pdf'},{'id':'nabp-competency','title':'NABP MPJE competency','url':'https://nabp.pharmacy/programs/examinations/mpje/competency-statements/'},{'id':'nabp-format','title':'NABP public format','url':'https://nabp.pharmacy/programs/examinations/mpje/take-the-mpje-exam/'}]
def fetch(s):
 t=datetime.now(timezone.utc).isoformat(); sid=s['id'];url=s['url']; status=None
 try:
  r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 independent legal audit'}),timeout=45);raw=r.read();status=r.status;final=r.url;ct=r.headers.get('Content-Type','')
 except urllib.error.HTTPError as e:raw=e.read();status=e.code;final=e.url;ct=e.headers.get('Content-Type','')
 except Exception as e:raw=str(e).encode();final=url;ct='error'
 pdf=raw.startswith(b'%PDF'); ext='.pdf' if pdf else '.html'; rp=E/(sid+ext);rp.write_bytes(raw)
 if pdf:
  subprocess.run(['pdftotext','-layout',str(rp),str(E/(sid+'.txt'))],check=True);txt=(E/(sid+'.txt')).read_text()
 else:
  txt=raw.decode('utf8','replace');txt=re.sub(r'<(script|style).*?</\1>','',txt,flags=re.S|re.I);txt=html.unescape(re.sub('<[^>]+>',' ',txt));txt=re.sub(r'[ \t]+',' ',txt);(E/(sid+'.txt')).write_text(txt)
 m=dict(s,requested_at=t,completed_at=datetime.now(timezone.utc).isoformat(),http_status=status,final_url=final,content_type=ct,raw_path=str(rp),raw_sha256=hashlib.sha256(raw).hexdigest(),text_path=str(E/(sid+'.txt')),text_sha256=hashlib.sha256(txt.encode()).hexdigest(),retrieval='LIVE_HTTPS_OFFICIAL_NORMAL_PROXY_TLS_VERIFIED',validity='REQUIRES_HUMAN_DOCUMENT_IDENTITY_REVIEW')
 (E/(sid+'.meta.json')).write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');return (sid,status,len(raw),pdf)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 for r in pool.map(fetch,items):print(r,flush=True)
