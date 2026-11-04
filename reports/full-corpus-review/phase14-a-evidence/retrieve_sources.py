"""Fresh independent public-primary retrieval; default TLS/proxy remain enabled."""
from pathlib import Path
from datetime import datetime, timezone
import concurrent.futures, hashlib, json, re, subprocess, urllib.request
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent/'sources'
SOURCES={
 'cfr21-530':'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-E/part-530',
 'cfr21-558-6':'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-E/part-558/section-558.6',
 'cfr42-493':'https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-G/part-493',
 'cfr21-203-30':'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-203/subpart-C/section-203.30',
 'cfr21-1305':'https://www.ecfr.gov/current/title-21/chapter-II/part-1305',
 'cfr21-1311':'https://www.ecfr.gov/current/title-21/chapter-II/part-1311',
 'cfr21-1307-11':'https://www.ecfr.gov/current/title-21/chapter-II/part-1307/section-1307.11',
 'cfr21-1301-74':'https://www.ecfr.gov/current/title-21/chapter-II/part-1301/section-1301.74',
 'cfr21-1301-76':'https://www.ecfr.gov/current/title-21/chapter-II/part-1301/section-1301.76',
 'cfr21-1317':'https://www.ecfr.gov/current/title-21/chapter-II/part-1317',
 'cfr21-1304':'https://www.ecfr.gov/current/title-21/chapter-II/part-1304',
 'ma-policy2026-01':'https://www.mass.gov/doc/2026-01-loss-or-theft-of-controlled-substances-pdf/download',
 'ma-105-700':'https://www.mass.gov/doc/105-cmr-700-implementation-of-mgl-c94c-0/download',
 'ma-247-9':'https://www.mass.gov/doc/247-cmr-9-code-of-professional-conduct/download',
 'ma112-58':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section58',
 'ma94c-1':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section1',
 'ma94c-19':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section19',
}
class Text(HTMLParser):
 def __init__(self): super().__init__(); self.out=[]; self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'): self.skip+=1
  if t in ('p','div','h1','h2','h3','h4','li','section','br'): self.out.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style'): self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.out.append(d)
def sha(b):return hashlib.sha256(b).hexdigest()
def fetch(pair):
 name,url=pair; now=datetime.now(timezone.utc).isoformat()
 m={'source_id':name,'requested_url':url,'official_url':url,'retrieved_at':now,'retrieval_method':'Python urllib.request direct HTTPS; system default TLS certificate verification and proxy settings','law_checked_date':now[:10]}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 independent research'})
  with urllib.request.urlopen(req,timeout=45) as r:
   b=r.read();m.update(status=r.status,final_url=r.url,headers=dict(r.headers));ext='pdf' if b.startswith(b'%PDF') else 'html'
  raw=OUT/(name+'.'+ext);raw.write_bytes(b)
  if ext=='pdf':subprocess.run(['pdftotext','-layout',str(raw),str(OUT/(name+'.txt'))],check=True)
  else:
   p=Text();p.feed(b.decode('utf-8',errors='replace'));(OUT/(name+'.txt')).write_text(re.sub(r'\n[ \t]*\n+', '\n\n',''.join(p.out)))
  txt=OUT/(name+'.txt');m.update(raw_path=str(raw.relative_to(ROOT)),raw_sha256=sha(b),evidence_path=str(txt.relative_to(ROOT)),evidence_sha256=sha(txt.read_bytes()),text_sha256=sha(txt.read_bytes()),raw_bytes=len(b),public_raw_redistribution=True)
 except Exception as e:m.update(error=type(e).__name__+': '+str(e),status='FAILED')
 (OUT/(name+'.meta.json')).write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');return m
if __name__=='__main__':
 OUT.mkdir(parents=True,exist_ok=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
  for m in pool.map(fetch,SOURCES.items()):print(m['source_id'],m['status'],m.get('raw_bytes'),m.get('error',''))
