import concurrent.futures,datetime,hashlib,json,pathlib,subprocess,urllib.request,urllib.error
from html.parser import HTMLParser
class TextParser(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ("script","style"):self.skip+=1
 def handle_endtag(self,t):
  if t in ("script","style"):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip and d.strip():self.parts.append(d.strip())
BASE=pathlib.Path(__file__).resolve().parent
sources={
'ma2479':'https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download',
'packpolicy':'https://www.mass.gov/doc/2023-01-compliance-packaging-and-reusable-dose-planners-pdf/download',
'ma12d':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section12D',
'ma12ee':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section12EE',
'ma21c':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section21C',
'agdcp':'https://www.mass.gov/news/dispensing-authorized-generics-circular-letter-dcp-22-01-112',
'agfda':'https://www.fda.gov/drugs/abbreviated-new-drug-application-anda/fda-list-authorized-generic-drugs',
'purple':'https://purplebooksearch.fda.gov/',
'cpscguide':'https://www.cpsc.gov/s3fs-public/PoisonPreventionPackagingAGuideforHealthcareProfessionals.pdf',
'cpscinfo':'https://www.cpsc.gov/Business--Manufacturing/Business-Education/Business-Guidance/PPPA',
'cfr170014':'https://www.ecfr.gov/current/title-16/chapter-II/subchapter-E/part-1700/section-1700.14',
'cfr170015':'https://www.ecfr.gov/current/title-16/chapter-II/subchapter-E/part-1700/section-1700.15',
'cfr211132':'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-211/subpart-G/section-211.132',
'deacmea':'https://www.deadiversion.usdoj.gov/meth/cma2005.html',
'fdacmea':'https://www.fda.gov/drugs/postmarket-drug-safety-information-patients-and-providers/legal-requirements-sale-and-purchase-drug-products-containing-pseudoephedrine-ephedrine-and',
'cfr131430':'https://www.ecfr.gov/current/title-21/chapter-II/part-1314/subpart-B/section-1314.30',
'cfr131420':'https://www.ecfr.gov/current/title-21/chapter-II/part-1314/subpart-B/section-1314.20',
'syringe':'https://www.mass.gov/advisory/sale-of-hypodermic-syringes-needles',
'ma19':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section19',
'nabpsample':'https://nabp.pharmacy/wp-content/uploads/2020/07/MPJE-Sample-Questions.pdf',
'nabpcompetency':'https://nabp.pharmacy/programs/examinations/mpje/competency-statements/',
'nabpformat':'https://nabp.pharmacy/programs/examinations/mpje/take-the-mpje-exam/'
}
def fetch(pair):
 k,url=pair; meta={'source_id':k,'official_url':url,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'retrieval_method':'LIVE urllib HTTPS via inherited proxy; TLS verification enabled'}
 try:
  try:
   resp=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40)
  except urllib.error.HTTPError as e: resp=e
  raw=resp.read();meta.update(http_status=resp.code,final_url=resp.url,content_type=resp.headers.get('Content-Type',''),raw_sha256=hashlib.sha256(raw).hexdigest())
  (BASE/(k+'.raw')).write_bytes(raw)
  if raw.startswith(b'%PDF'):
   subprocess.run(['pdftotext','-layout',str(BASE/(k+'.raw')),str(BASE/(k+'.txt'))],check=True)
   txt=(BASE/(k+'.txt')).read_text()
  else:
   parser=TextParser();parser.feed(raw.decode('utf-8',errors='replace'));txt='\n'.join(parser.parts)
   (BASE/(k+'.txt')).write_text(txt)
  meta.update(text_sha256=hashlib.sha256((BASE/(k+'.txt')).read_bytes()).hexdigest(),text_length=len(txt),document_available=resp.code==200 and not any(x in txt[:300] for x in ['Access Denied','Page Not Found','Just a moment','Page not found']))
 except Exception as e:meta['error']=str(e)
 (BASE/(k+'.meta.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
 return meta
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
  for m in pool.map(fetch,sources.items()):print(json.dumps(m))
