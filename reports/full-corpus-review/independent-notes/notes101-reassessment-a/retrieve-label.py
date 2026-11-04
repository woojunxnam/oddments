import json,hashlib,urllib.request,datetime
from pathlib import Path
from html.parser import HTMLParser
OUT=Path(__file__).resolve().parent/'sources'
class Text(HTMLParser):
 def __init__(self):super().__init__();self.a=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
  if t in ['p','div','li','h1','h2','h3','h4','br','tr']:self.a.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(self.skip-1,0)
 def handle_data(self,d):
  if not self.skip:self.a.append(d)
def retrieve(name,url):
 at=datetime.datetime.now(datetime.timezone.utc).isoformat();req=urllib.request.Request(url,headers={'User-Agent':'Independent note authority review/1.0'})
 with urllib.request.urlopen(req,timeout=60) as r:raw=r.read();status=r.status;headers=dict(r.headers);final=r.url
 (OUT/(name+'.raw')).write_bytes(raw)
 p=Text();p.feed(raw.decode('utf-8',errors='replace'));txt='\n'.join(x.strip() for x in ''.join(p.a).splitlines() if x.strip())+'\n';(OUT/(name+'.txt')).write_text(txt)
 meta={'official_url':url,'final_url':final,'retrieved_at':at,'http_status':status,'headers':headers,'raw_sha256':hashlib.sha256(raw).hexdigest(),'text_sha256':hashlib.sha256(txt.encode()).hexdigest(),'method':'Direct HTTPS GET; HTMLParser removes script/style; raw retained'}
 (OUT/(name+'.meta.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');print(name,status,len(raw),meta['raw_sha256'])
retrieve('zenatane-current','https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=27b3cf26-f22e-5b70-1c24-009933b7c6ee')
