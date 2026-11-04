import json,hashlib,datetime,concurrent.futures,subprocess
from pathlib import Path
import urllib.request,html,re
class Response:
 def __init__(self,url):
  with urllib.request.urlopen(url,timeout=55) as r:self.content=r.read();self.url=r.url;self.status_code=r.status;self.headers=r.headers
class Requests:
 def get(self,url,timeout=55):return Response(url)
requests=Requests()
base=Path('reports/full-corpus-review/independent-notes/notes101-b');out=base/'sources';out.mkdir(exist_ok=True)
x=json.load(open(base/'visible-input.json')); urls={c['official_url'] for u in x['units'] for c in u['claims'] if c.get('official_url')}
urls.update(['https://www.mass.gov/doc/247-cmr-20-reporting/download','https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download','https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section24G','https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/personal-representatives/index.html'])
def fetch(url):
 key=hashlib.sha256(url.encode()).hexdigest()[:16];meta={'official_url':url,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'requests GET inherited HTTPS proxy, TLS verification enabled','key':key}
 try:
  r=requests.get(url,timeout=55);raw=r.content;ext='pdf' if raw.startswith(b'%PDF') else 'html';p=out/(key+'.'+ext);p.write_bytes(raw);meta.update(status=r.status_code,resolved_url=r.url,headers=dict(r.headers),raw_path=str(p),raw_sha256=hashlib.sha256(raw).hexdigest())
  if ext=='pdf':subprocess.run(['pdftotext','-layout',str(p),str(out/(key+'.txt'))],check=True)
  else:(out/(key+'.txt')).write_text(html.unescape(re.sub('<[^>]+>', '\n', raw.decode('utf-8',errors='replace'))))
  meta['text_path']=str(out/(key+'.txt'));meta['text_sha256']=hashlib.sha256((out/(key+'.txt')).read_bytes()).hexdigest()
 except Exception as e:meta['error']=str(e)
 (out/(key+'.meta.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');return {k:meta.get(k) for k in ['key','official_url','status','error']}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 rows=list(ex.map(fetch,sorted(urls)))
(base/'retrieval-index.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
for r in rows:print(r)
