import json,hashlib,urllib.request,datetime,subprocess
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
def retrieve(name,url,pdf=False):
 at=datetime.datetime.now(datetime.timezone.utc).isoformat();req=urllib.request.Request(url,headers={'User-Agent':'Independent note authority review/1.0'})
 with urllib.request.urlopen(req,timeout=60) as r:raw=r.read();status=r.status;headers=dict(r.headers);final=r.url
 path=OUT/(name+('.pdf' if pdf else '.raw'));path.write_bytes(raw)
 if pdf:subprocess.run(['pdftotext','-layout',str(path),str(OUT/(name+'.txt'))],check=True)
 else:
  p=Text();p.feed(raw.decode('utf-8',errors='replace'));txt='\n'.join(x.strip() for x in ''.join(p.a).splitlines() if x.strip())+'\n';(OUT/(name+'.txt')).write_text(txt)
 meta={'official_url':url,'final_url':final,'retrieved_at':at,'retrieval_kind':'LIVE_DIRECT_HTTPS_GET','http_status':status,'headers':headers,'raw_sha256':hashlib.sha256(raw).hexdigest(),'text_sha256':hashlib.sha256((OUT/(name+'.txt')).read_bytes()).hexdigest(),'method':'pdftotext -layout' if pdf else 'HTMLParser removes script/style; raw retained'}
 (OUT/(name+'.meta.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');print(name,status,len(raw),meta['raw_sha256'])
retrieve('vaccine','https://www.mass.gov/doc/2023-02-vaccine-administration-pdf/download',True)
retrieve('ratios','https://www.mass.gov/doc/2026-02-ratios-supervision-and-dedicated-training-personnel/download',True)
retrieve('law24g','https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section24G')
