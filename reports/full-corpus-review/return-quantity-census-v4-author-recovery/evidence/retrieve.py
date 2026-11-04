from pathlib import Path
from urllib.request import urlopen,Request
from urllib.error import HTTPError
from datetime import datetime,timezone
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,subprocess
BASE=Path(__file__).resolve().parent
SOURCES={'cmr9':'https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download','policy2023-01':'https://www.mass.gov/doc/2023-01-compliance-packaging-and-reusable-dose-planners-pdf/download'}
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
class Text(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.out=[]
 def handle_starttag(self,t,a):
  if t in ['script','style','noscript']:self.skip+=1
  if t in ['p','div','br','h1','h2','h3','h4','li','section','article']:self.out.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style','noscript']:self.skip=max(0,self.skip-1)
  if t in ['p','div','h1','h2','h3','h4','li','section','article']:self.out.append('\n')
 def handle_data(self,d):
  if not self.skip:self.out.append(d)
def get(item):
 key,url=item;at=now();status=None
 try:
  with urlopen(Request(url,headers={'User-Agent':'MPJE-independent-official-review/1'}),timeout=50) as r:
   raw=r.read();status=r.status;resolved=r.url;ct=r.headers.get('Content-Type','');last=r.headers.get('Last-Modified')
 except HTTPError as e:raw=e.read();status=e.code;resolved=e.url;ct=e.headers.get('Content-Type','');last=None
 except Exception as e:
  (BASE/(key+'.error.json')).write_text(json.dumps(dict(url=url,retrieved_at_utc=at,error=repr(e)),indent=2));return key,str(e)
 suffix='.pdf' if raw.startswith(b'%PDF') else '.html';p=BASE/(key+suffix);p.write_bytes(raw)
 if suffix=='.pdf':subprocess.run(['pdftotext','-layout',str(p),str(BASE/(key+'.txt'))],check=True)
 else:
  parser=Text();parser.feed(raw.decode('utf-8',errors='replace'));text='\n'.join(x.strip() for x in ''.join(parser.out).splitlines() if x.strip());(BASE/(key+'.txt')).write_text(text+'\n')
 txt=(BASE/(key+'.txt')).read_bytes();meta=dict(source_id=key,official_url=url,resolved_url=resolved,http_status=status,content_type=ct,last_modified=last,retrieved_at_utc=at,completed_at_utc=now(),normal_TLS_certificate_verification=True,transport='urllib.request HTTPS via inherited proxy; default verified TLS; no bypass',raw_path=p.name,raw_sha256=sha(raw),text_path=key+'.txt',text_sha256=sha(txt),raw_bytes=len(raw))
 (BASE/(key+'.meta.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');return key,status,len(raw)
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=3) as pool:
  for x in pool.map(get,SOURCES.items()):print(*x,flush=True)
