import urllib.request,json,hashlib,datetime
from pathlib import Path
from html.parser import HTMLParser
class P(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.main=0;self.all=[];self.content=[]
 def handle_starttag(self,t,a):
  if t in ['script','style','noscript']:self.skip+=1
  if t=='main':self.main+=1
 def handle_endtag(self,t):
  if t in ['script','style','noscript']:self.skip=max(0,self.skip-1)
  if t=='main':self.main=max(0,self.main-1)
 def handle_data(self,d):
  if not self.skip and d.strip():
   self.all.append(d.strip())
   if self.main:self.content.append(d.strip())
b=Path('reports/full-corpus-review/independent-notes/notes101-reassessment-b/sources');b.mkdir(exist_ok=True)
urls={'tirf':'https://www.fda.gov/drugs/risk-evaluation-and-mitigation-strategies-rems/transmucosal-immediate-release-fentanyl-tirf-medicines','schedule2':'https://www.ecfr.gov/current/title-21/chapter-II/part-1308/section-1308.12'}
for k,u in urls.items():
 with urllib.request.urlopen(u,timeout=55) as r:raw=r.read();meta={'official_url':u,'resolved_url':r.url,'status':r.status,'headers':dict(r.headers),'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'urllib HTTPS GET inherited proxy/TLS enabled'}
 (b/(k+'.raw.html')).write_bytes(raw);p=P();p.feed(raw.decode(errors='replace'));text='\n'.join(p.content or p.all)+'\n';(b/(k+'.txt')).write_text(text)
 meta.update(raw_path=str(b/(k+'.raw.html')),raw_sha256=hashlib.sha256(raw).hexdigest(),text_path=str(b/(k+'.txt')),text_sha256=hashlib.sha256(text.encode()).hexdigest());(b/(k+'.meta.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');print(k,meta['status'],meta['raw_sha256'])
