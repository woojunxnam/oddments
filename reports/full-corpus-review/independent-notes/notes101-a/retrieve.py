import concurrent.futures,datetime,hashlib,json,pathlib,subprocess,urllib.request,urllib.error
from html.parser import HTMLParser
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag in ["script","style"]:self.skip+=1
 def handle_endtag(self,tag):
  if tag in ["script","style"]:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip and d.strip():self.parts.append(d.strip())
OUT=pathlib.Path(__file__).parent; SRC=OUT/'sources'; SRC.mkdir(exist_ok=True)
p=json.loads((OUT/'notes101-a-visible-input.json').read_text())
urls=sorted({c['official_url'] for x in p['units'] for c in x['claims'] if c.get('official_url')})
urls += ['https://www.ecfr.gov/api/versioner/v1/full/2026-11-02/title-45.xml?part=164','https://www.ecfr.gov/api/versioner/v1/full/2026-11-02/title-45.xml?part=160','https://www.ecfr.gov/api/versioner/v1/full/2026-11-02/title-21.xml?part=1317','https://www.ecfr.gov/api/versioner/v1/full/2026-11-02/title-21.xml?part=1308','https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section24G']
def fetch(item):
 i,url=item;stem=f'{i:02d}'; meta={'url':url,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=65);raw=r.read();(SRC/(stem+'.raw')).write_bytes(raw);meta.update(status=r.status,final_url=r.url,headers=dict(r.headers),raw_sha256=hashlib.sha256(raw).hexdigest())
  if raw.startswith(b'%PDF'):
   subprocess.run(['pdftotext','-layout',str(SRC/(stem+'.raw')),str(SRC/(stem+'.txt'))],check=True)
  else:
   parser=Text();parser.feed(raw.decode('utf-8',errors='replace'));(SRC/(stem+'.txt')).write_text('\n'.join(parser.parts))
  meta['text_sha256']=hashlib.sha256((SRC/(stem+'.txt')).read_bytes()).hexdigest()
 except Exception as e:meta['error']=str(e)
 (SRC/(stem+'.meta.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');return stem,meta.get('status'),url,meta.get('error')
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
 for row in pool.map(fetch,enumerate(urls,1)): print(*row,flush=True)
