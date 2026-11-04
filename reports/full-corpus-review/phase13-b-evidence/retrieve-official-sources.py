from pathlib import Path
from datetime import datetime,timezone
import urllib.request,urllib.error,json,hashlib,concurrent.futures,subprocess
from html.parser import HTMLParser
class TextParser(HTMLParser):
 def __init__(self): super().__init__(); self.parts=[]
 def handle_data(self,data): self.parts.append(data.strip())
base=Path('/workspace/independent-wave13-b/reports/full-corpus-review/phase13-b-evidence/sources');base.mkdir(parents=True,exist_ok=True)
urls={
'ma247-9':'https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download',
'ma105-700':'https://www.mass.gov/doc/105-cmr-700-implementation-of-mgl-c94c-0/download',
'ma94c18':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18',
'ma94c23':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section23',
'ma94c24a':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section24A',
'partial-dcp':'https://www.mass.gov/doc/schedule-ii-partial-fill-requests-pdf/download',
'cfr1306-13':'https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.13',
'cfr1306-22':'https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.22',
'cfr1306-23':'https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.23',
'cfr1306-25':'https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.25',
'cfr1306-08':'https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.08',
'pmp-guide':'https://www.mass.gov/doc/pmp-data-submission-dispenser-guide-version-52-pdf/download',
'nabp-sample':'https://nabp.pharmacy/wp-content/uploads/2020/07/MPJE-Sample-Questions.pdf',
'nabp-competency':'https://nabp.pharmacy/programs/examinations/mpje/competency-statements/',
'nabp-format':'https://nabp.pharmacy/programs/examinations/mpje/take-the-mpje-exam/'}
def fetch(item):
 key,url=item;start=datetime.now(timezone.utc).isoformat();status=None
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 independent-law-review'}),timeout=45) as r: raw=r.read();status=r.status;final=r.url;ctype=r.headers.get('Content-Type')
 except urllib.error.HTTPError as e:raw=e.read();status=e.code;final=e.url;ctype=e.headers.get('Content-Type')
 except Exception as e:return {'id':key,'error':str(e),'at':start}
 suffix='.pdf' if raw.startswith(b'%PDF') else '.html';p=base/(key+suffix)
 # NABP: retain payload only outside repo; record SHA and own memo later.
 if key.startswith('nabp'):p=Path('/tmp')/('phase13-b-'+key+suffix)
 p.write_bytes(raw)
 if suffix=='.pdf':
  tp=p.with_suffix('.txt');subprocess.run(['pdftotext','-layout',str(p),str(tp)],check=True);txt=tp.read_text()
 else:
  parser=TextParser();parser.feed(raw.decode('utf-8',errors='replace'));txt='\n'.join(x for x in parser.parts if x);tp=p.with_suffix('.txt');tp.write_text(txt)
 meta={'source_id':key,'official_url':url,'final_url':final,'http_status':status,'content_type':ctype,'retrieved_at':start,'completed_at':datetime.now(timezone.utc).isoformat(),'retrieval_method':'urllib HTTPS through inherited proxy with default TLS verification','raw_sha256':hashlib.sha256(raw).hexdigest(),'text_sha256':hashlib.sha256(txt.encode()).hexdigest(),'raw_path':str(p),'text_path':str(tp),'law_checked_date':'2026-11-04','read_status':'PENDING_IDENTITY_AND_TEXT_REVIEW','effective_date':'NOT_YET_ASSESSED'}
 (base/(key+'.meta.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');return {'id':key,'http_status':status,'bytes':len(raw),'text_chars':len(txt)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 for r in ex.map(fetch,urls.items()): print(r)
