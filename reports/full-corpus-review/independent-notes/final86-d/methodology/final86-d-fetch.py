import json,hashlib,subprocess,concurrent.futures,datetime,urllib.request,urllib.error,re,html,shutil
from pathlib import Path
from html.parser import HTMLParser
root=Path('/workspace/notes-final86-d');base=root/'reports/full-corpus-review/independent-notes/final86-d';out=base/'sources';out.mkdir(exist_ok=True);p=json.loads((base/'visible-input.json').read_bytes())
urls=set()
for x in p['units']:
 for c in x['claims']:
  for a in [c]+c.get('authorities',[])+c.get('additional_authorities',[]):
   if a.get('official_url'):urls.add(a['official_url'])
urls.add('https://www.mass.gov/doc/247-cmr-20-reporting-obligations/download')
urls.add('https://oig.hhs.gov/compliance/physician-education/fraud-abuse-laws/')
class Cleaner(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
  if t in ('p','div','li','br','section','tr','h1','h2','h3','h4'):self.parts.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
def fetch(url):
 key=hashlib.sha256(url.encode()).hexdigest()[:16];mp=out/(key+'.meta.json')
 if mp.exists():return json.loads(mp.read_bytes())
 old=Path('/workspace/notes120-d/reports/full-corpus-review/independent-notes/notes120-d/sources')
 if (old/(key+'.meta.json')).exists():
  m=json.loads((old/(key+'.meta.json')).read_bytes())
  if m.get('status_code')==200 and m.get('requested_at_utc','').startswith('2026-11-04'):
   for z in old.glob(key+'.*'):shutil.copyfile(z,out/z.name)
   m['retention_note_ko']='같은 실제 instance의 2026-11-04 원 GET 증거를 원시각·raw/text bytes·원 metadata와 함께 retained. 이번 배치 새 GET 아님.';m['original_retained_metadata']=json.loads((old/(key+'.meta.json')).read_bytes())
   for f in ['raw_path','text_path']:
    if m.get(f):m[f]=str((out/Path(m[f]).name).relative_to(root))
   mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');return m
 t=datetime.datetime.now(datetime.timezone.utc).isoformat();m={'official_url':url,'requested_at_utc':t,'retrieval_mode':'ACTUAL_NEW_GET_NO_CACHE_SUBSTITUTION'}
 try:
  r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 legal source verification'}),timeout=55);raw=r.read();ext='.pdf' if raw.startswith(b'%PDF') else '.json' if raw.lstrip().startswith(b'{') else '.xml' if '/spls/' in url else '.html';rp=out/(key+ext);rp.write_bytes(raw);m.update(status_code=r.status,final_url=r.url,response_headers=dict(r.headers),completed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),raw_path=str(rp.relative_to(root)),raw_sha256=hashlib.sha256(raw).hexdigest());tp=out/(key+'.txt')
  if ext=='.pdf':subprocess.run(['pdftotext','-layout',str(rp),str(tp)],check=True)
  elif ext=='.json':tp.write_text(json.dumps(json.loads(raw),ensure_ascii=False,indent=2)+'\n')
  else:
   z=Cleaner();z.feed(raw.decode('utf-8',errors='replace'));tp.write_text(re.sub(r'\n[ \t]*\n+', '\n', ''.join(z.parts)))
  m.update(text_path=str(tp.relative_to(root)),text_sha256=hashlib.sha256(tp.read_bytes()).hexdigest())
 except Exception as e:
  m['error']=str(e)
  if isinstance(e,urllib.error.HTTPError):
   raw=e.read();rp=out/(key+'.error.html');rp.write_bytes(raw);m.update(error_status=e.code,error_raw_path=str(rp.relative_to(root)),error_raw_sha256=hashlib.sha256(raw).hexdigest())
 mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');return m
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:res=list(ex.map(fetch,sorted(urls)))
(base/'source-index.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
for m in res:print(m['official_url'],m.get('status_code'),m.get('error'),m.get('retention_note_ko',''))
