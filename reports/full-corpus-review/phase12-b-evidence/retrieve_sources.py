"""Actual official HTTPS retrieval; TLS/proxy inherited. No prior audit inputs."""
import json,hashlib,urllib.request,urllib.error,re,subprocess
from pathlib import Path
from datetime import datetime,timezone
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor
BASE=Path(__file__).resolve().parent/'official';BASE.mkdir(exist_ok=True)
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
  if t in ('p','div','section','h1','h2','h3','h4','li','tr','br'):self.parts.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
URLS={
'ma247-9-page':'https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards',
'ma247-9':'https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download',
'ma112-12f':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section12F',
'fda-medguides':'https://www.fda.gov/drugs/drug-safety-and-availability/medication-guides',
'fda-rems':'https://www.fda.gov/drugs/drug-safety-and-availability/risk-evaluation-and-mitigation-strategies-rems',
'cdc-vis':'https://www.cdc.gov/vaccines/hcp/vis/about/facts-vis.html',
'medicaid-dur':'https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title42-section1396r-8&num=0&edition=prelim',
}
for s in ['160.103']:URLS['cfr45-'+s]='https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-160/section-'+s
for s in ['164.502','164.504','164.506','164.508','164.510','164.514','164.520','164.522','164.524','164.526','164.530']:URLS['cfr45-'+s]='https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/section-'+s
for s in ['208.20','208.24','310.501','310.515','1306.04']:
 URLS['cfr21-'+s]='https://www.ecfr.gov/current/title-21/part-'+s.split('.')[0]+'/section-'+s

def sha(x):return hashlib.sha256(x).hexdigest()
def fetch(kv):
 key,url=kv;start=datetime.now(timezone.utc).isoformat();meta=dict(source_id=key,official_url=url,retrieval_started_at=start,method='urllib HTTPS GET, inherited proxy and CA, TLS verification enabled',new_live_retrieval=True)
 try:
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 Independent legal review'}),timeout=50) as r:raw=r.read();status=r.status;final=r.url;headers=dict(r.headers)
  except urllib.error.HTTPError as r:raw=r.read();status=r.code;final=r.url;headers=dict(r.headers)
  meta.update(http_status=status,final_url=final,response_headers=headers,raw_sha256=sha(raw),retrieved_at=datetime.now(timezone.utc).isoformat())
  suffix='.pdf' if raw.startswith(b'%PDF') else '.html';path=BASE/(key+suffix);path.write_bytes(raw)
  if suffix=='.pdf':
   subprocess.run(['pdftotext','-layout',str(path),str(BASE/(key+'.txt'))],check=True);txt=(BASE/(key+'.txt')).read_text()
  else:
   p=Text();p.feed(raw.decode('utf-8',errors='replace'));txt='\n'.join(re.sub(r'[ \t]+',' ',x).strip() for x in ''.join(p.parts).splitlines() if x.strip());(BASE/(key+'.txt')).write_text(txt)
  titles=re.findall(r'<title[^>]*>(.*?)</title>',raw.decode('utf-8',errors='replace'),re.S|re.I)
  meta.update(raw_path=str(path.relative_to(BASE.parent.parent.parent.parent)),text_path=str((BASE/(key+'.txt')).relative_to(BASE.parent.parent.parent.parent)),text_sha256=sha(txt.encode()),document_title=re.sub('<[^>]+>','',titles[0]).strip() if titles else ('PDF: '+key),identity_validation='PENDING_DIRECT_TEXT_READ',legal_verified=False)
 except Exception as e:meta.update(error=type(e).__name__+': '+str(e),retrieved_at=datetime.now(timezone.utc).isoformat(),legal_verified=False)
 (BASE/(key+'.meta.json')).write_text(json.dumps(meta,indent=2)+'\n');return {k:meta.get(k) for k in ['source_id','http_status','document_title','error','raw_sha256']}
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=5) as pool:
  for result in pool.map(fetch,URLS.items()):print(json.dumps(result),flush=True)
