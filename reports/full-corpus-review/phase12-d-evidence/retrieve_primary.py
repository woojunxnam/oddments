"""Native-session official HTTP retrieval; no prior review evidence is read."""
import json,hashlib,subprocess,re,concurrent.futures,sys
from pathlib import Path
from datetime import datetime,timezone
from urllib.request import Request,urlopen
from urllib.error import HTTPError
from html.parser import HTMLParser
BASE=Path(__file__).resolve().parent
class Text(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.out=[]
 def handle_starttag(self,t,a):
  if t in ('script','style','noscript'):self.skip+=1
  if t in ('p','div','section','li','h1','h2','h3','h4','br','tr'):self.out.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style','noscript') and self.skip:self.skip-=1
  if t in ('p','div','section','li','h1','h2','h3','h4','tr'):self.out.append('\n')
 def handle_data(self,d):
  if not self.skip:self.out.append(d)
def sha(b):return hashlib.sha256(b).hexdigest()
registry=json.load(open('notes/guide.json'))['sources']
config=json.load(open('site/practice-expansion/publication.json'))
ids=set(json.load(open(BASE/'assignment.json'))['question_hashes']);sids=set();locators={}
for path in ['practice_expansion/2026-10-23/candidates/questions.json']+[a['path'] for a in config['additional_banks']]:
 for q in json.load(open(path))['questions']:
  if q['question_id'] in ids:
   sids.update(q.get('source_ids',[]));locators[q['question_id']]={'family_id':q['family_id'],'source_ids':q.get('source_ids',[]),'collection':path}
(BASE/'source-locators.json').write_text(json.dumps(locators,ensure_ascii=False,indent=2)+'\n')
urls={s:registry[s]['url'] for s in sorted(sids)}
urls.update({'fed-1311':'https://www.ecfr.gov/current/title-21/chapter-II/part-1311','fed-1300':'https://www.ecfr.gov/current/title-21/chapter-II/part-1300','ma-94C-7':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section7','ma-pmp-gaba':'https://www.mass.gov/info-details/prescription-monitoring-program-pmp-reporting-requirements','nabp-format':'https://nabp.pharmacy/programs/examinations/mpje/take-the-mpje-exam/','nabp-competency':'https://nabp.pharmacy/programs/examinations/mpje/competency-statements/'})
urls.update({'ma-pmp-current':'https://www.mass.gov/info-details/pharmacy-reporting-and-data-submission','fed-oxy-schedule':'https://www.ecfr.gov/current/title-21/chapter-II/part-1308/section-1308.12'})
if len(sys.argv)>1:urls={k:v for k,v in urls.items() if k in sys.argv[1:]}
def get(item):
 sid,url=item; started=datetime.now(timezone.utc).isoformat();meta={'source_id':sid,'requested_url':url,'started_at':started,'method':'GET','retrieval_method':'Python urllib HTTPS through inherited proxy with default TLS verification','retrieval_actor':'/root/independent_wave12_d','official_primary':True}
 try:
  try:r=urlopen(Request(url,headers={'User-Agent':'MPJE-independent-review/1.0'}),timeout=60)
  except HTTPError as e:r=e
  raw=r.read();meta.update(http_status=r.status,final_url=r.url,headers={k:v for k,v in r.headers.items() if k.lower() in ('date','content-type','last-modified','etag','content-location','content-length')});r.close()
  ispdf=raw.startswith(b'%PDF');rp=BASE/'sources'/(sid+('.pdf' if ispdf else '.html'));rp.write_bytes(raw)
  if ispdf:
   tp=rp.with_suffix('.txt');subprocess.run(['pdftotext','-layout',str(rp),str(tp)],check=True);text=tp.read_text()
  else:
   p=Text();p.feed(raw.decode('utf-8','replace'));text=re.sub(r'\n[ \t]*\n(?:[ \t]*\n)*','\n\n',''.join(p.out));tp=rp.with_suffix('.txt');tp.write_text(text)
  title=re.search(r'<title[^>]*>(.*?)</title>',raw.decode('utf-8','replace'),re.S|re.I)
  meta.update(raw_path=str(rp.relative_to(Path.cwd())) if rp.is_relative_to(Path.cwd()) else str(rp),raw_sha256=sha(raw),text_path=str(tp.relative_to(Path.cwd())) if tp.is_relative_to(Path.cwd()) else str(tp),text_sha256=sha(tp.read_bytes()),raw_bytes=len(raw),document_identity=(re.sub(r'\s+',' ',title.group(1)).strip() if title else 'PDF: '+re.sub(r'\s+',' ',text[:450])),retrieval_success=200<=r.status<300)
 except Exception as e:meta.update(retrieval_success=False,error=type(e).__name__+': '+str(e))
 meta['completed_at']=datetime.now(timezone.utc).isoformat(); mp=BASE/'sources'/(sid+'.meta.json');mp.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');return meta
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 for m in pool.map(get,urls.items()):print(m['source_id'],m.get('http_status'),m.get('raw_bytes'),m.get('document_identity','')[:140],flush=True)
