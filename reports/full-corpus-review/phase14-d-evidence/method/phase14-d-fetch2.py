import urllib.request,urllib.error,hashlib,json,subprocess,concurrent.futures,datetime
from html.parser import HTMLParser
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.suppressed=False
 def handle_starttag(self,t,a):
  if t in ["script","style"]:self.suppressed=True
 def handle_endtag(self,t):
  if t in ["script","style"]:self.suppressed=False
 def handle_data(self,d):
  if not self.suppressed and d.strip():self.parts.append(d.strip())
from pathlib import Path

root=Path('/workspace/independent-wave14-d'); pub=root/'reports/full-corpus-review/phase14-d-evidence/sources'; rawroot=Path('/tmp/phase14-d-private')
sources={
'cfr7-3':'https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfcfr/CFRSearch.cfm?fr=7.3',
'cfr314-80':'https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfcfr/CFRSearch.cfm?fr=314.80',
'fda503b':'https://www.fda.gov/media/90997/download',
'fda-orange-preface':'https://www.fda.gov/drugs/development-approval-process-drugs/orange-book-preface',
'fda-smallletter':'https://www.fda.gov/media/194424/download?attachment=',
'gov-dscsa':'https://www.govinfo.gov/content/pkg/USCODE-2024-title21/html/USCODE-2024-title21-chap9-subchapV-partH-sec360eee-1.htm',
'gov353b':'https://www.govinfo.gov/content/pkg/USCODE-2024-title21/html/USCODE-2024-title21-chap9-subchapV-partA-sec353b.htm'
}
def fetch(k,u):
 t=datetime.datetime.now(datetime.timezone.utc).isoformat(); 
 try:r=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=75)
 except urllib.error.HTTPError as e:r=e
 raw=r.read(); rp=rawroot/(k+'.raw');rp.write_bytes(raw)
 if raw.startswith(b'%PDF'):
  subprocess.run(['pdftotext','-layout',str(rp),str(rawroot/(k+'.txt'))],check=True);txt=(rawroot/(k+'.txt')).read_text()
 else:
  p=Parser();p.feed(raw.decode('utf-8',errors='replace'));txt='\n'.join(p.parts);(rawroot/(k+'.txt')).write_text(txt)
 meta=dict(source_id=k,official_url=u,final_url=r.url,status=r.status,content_type=r.headers.get('Content-Type'),retrieved_at=t,method='urllib.request inherited proxy; TLS verification enabled',raw_sha256=hashlib.sha256(raw).hexdigest(),text_sha256=hashlib.sha256(txt.encode()).hexdigest(),raw_retention='private temporary uncommitted',text_retention='private temporary uncommitted',public_raw_redistribution=False)
 (pub/(k+'.meta.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
 return k,r.status,len(raw),len(txt),txt[:60]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 for x in ex.map(lambda x:fetch(*x),sources.items()):print(x)
