import json,hashlib,urllib.request,urllib.error,datetime,subprocess,concurrent.futures
from pathlib import Path
from html.parser import HTMLParser
OUT=Path(__file__).resolve().parent/'sources'
class Text(HTMLParser):
 def __init__(self):super().__init__();self.a=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
  if t in ['p','div','li','h1','h2','h3','h4','br','tr','section','pre']:self.a.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(self.skip-1,0)
 def handle_data(self,d):
  if not self.skip:self.a.append(d)
def retrieve(item):
 name,url=item;at=datetime.datetime.now(datetime.timezone.utc).isoformat();req=urllib.request.Request(url,headers={'User-Agent':'Independent source review/1.0'});meta={'official_url':url,'retrieved_at':at,'retrieval_kind':'LIVE_DIRECT_HTTPS_ATTEMPT'}
 try:
  try:r=urllib.request.urlopen(req,timeout=60)
  except urllib.error.HTTPError as e:r=e
  with r:raw=r.read();status=r.status;headers=dict(r.headers);final=r.url
  pdf=raw.startswith(b'%PDF');ext='.pdf' if pdf else '.raw';path=OUT/(name+ext);path.write_bytes(raw)
  if pdf:subprocess.run(['pdftotext','-layout',str(path),str(OUT/(name+'.txt'))],check=True)
  else:
   p=Text();p.feed(raw.decode('utf-8',errors='replace'));txt='\n'.join(x.strip() for x in ''.join(p.a).splitlines() if x.strip())+'\n';(OUT/(name+'.txt')).write_text(txt)
  meta.update(retrieval_kind='LIVE_DIRECT_HTTPS_GET',http_status=status,headers=headers,final_url=final,raw_extension=ext,raw_sha256=hashlib.sha256(raw).hexdigest(),text_sha256=hashlib.sha256((OUT/(name+'.txt')).read_bytes()).hexdigest(),method='pdftotext -layout' if pdf else 'HTMLParser excludes script/style; raw retained',content_validity='PENDING_MANUAL_SOFT404_ACCESS_AND_SCOPE_CHECK')
 except Exception as e:meta.update(error=str(e),http_status=getattr(e,'code',None))
 (OUT/(name+'.meta.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');return name,meta.get('http_status'),meta.get('raw_sha256'),meta.get('error')
p=json.loads((OUT.parent/'visible-input.json').read_text());urls=[]
for u in p['units']:
 for c in u['claims']:
  for a in [c,*c.get('additional_authorities',[])]:
   url=a.get('official_url')
   if url and url not in urls:urls.append(url)
urls.extend(['https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title21-section353a&num=0&edition=prelim','https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title21-section353b&num=0&edition=prelim','https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title21-section360eee&num=0&edition=prelim'])
items=[(f'{n:02}',url) for n,url in enumerate(urls,1)];(OUT.parent/'source-index.json').write_text(json.dumps(dict(items),indent=2)+'\n')
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 for r in ex.map(retrieve,items):print(*r,flush=True)
