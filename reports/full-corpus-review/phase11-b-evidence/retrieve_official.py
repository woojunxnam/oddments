import urllib.request,urllib.error,json,hashlib,datetime,pathlib,subprocess,concurrent.futures
from html.parser import HTMLParser
BASE=pathlib.Path(__file__).resolve().parent
URLS={
'247-cmr-16':'https://www.mass.gov/doc/247-cmr-16-collaborative-drug-therapy-management/download',
'247-cmr-4':'https://www.mass.gov/doc/247-cmr-4-personal-registration-renewal-continuing-education-requirement/download',
'ce-policy':'https://www.mass.gov/doc/2021-04-continuing-education-ce-requirements-pdf/download',
'105-cmr-700':'https://www.mass.gov/doc/105-cmr-700-implementation-of-mgl-c94c-0/download',
'mgl112-24b':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section24B',
'mgl94c-7':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section7',
'21usc822':'https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title21-section822&num=0&edition=prelim',
'21cfr1301-22':'https://www.ecfr.gov/current/title-21/section-1301.22',
'nabp-competency':'https://nabp.pharmacy/programs/examinations/mpje/competency-statements/',
'nabp-format':'https://nabp.pharmacy/programs/examinations/mpje/take-the-mpje-exam/'}
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,s):self.parts.append(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def get(k,u):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();raw=b''
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 independent law review'}),timeout=50) as r:
   raw=r.read();status=r.status;final=r.url;headers=dict(r.headers)
  error=None
 except urllib.error.HTTPError as e:raw=e.read();status=e.code;final=e.url;headers=dict(e.headers);error=str(e)
 except Exception as e:status=None;final=u;headers={};error=repr(e)
 end=datetime.datetime.now(datetime.timezone.utc).isoformat()
 meta=dict(source_id=k,requested_url=u,official_url=final,retrieved_at=start,retrieval_completed_at=end,http_status=status,tls_verification=True,method='Python urllib.request.urlopen via inherited proxy; default certificate verification',raw_sha256=sha(raw),bytes=len(raw),response_headers=headers,error=error)
 if not k.startswith('nabp'):
  out=BASE/'official';out.mkdir(exist_ok=True)
  ext='pdf' if raw.startswith(b'%PDF') else 'html';p=out/(k+'.'+ext);p.write_bytes(raw)
  if ext=='pdf':
   subprocess.run(['pdftotext','-layout',str(p),str(out/(k+'.txt'))],check=False,capture_output=True)
   txt=(out/(k+'.txt')).read_bytes() if (out/(k+'.txt')).exists() else b''
  else:
   parser=Text();parser.feed(raw.decode(errors='replace'));txt='\n'.join(parser.parts).encode();(out/(k+'.txt')).write_bytes(txt)
  meta.update(raw_path=str(p.relative_to(BASE)),text_path='official/'+k+'.txt',text_sha256=sha(txt))
  meta['successful_primary_retrieval']=bool(status==200 and len(raw)>1000 and not any(x in txt[:5000].lower() for x in [b'access denied',b'page not found',b'error 404']))
 else:meta['retention']='URL, metadata and payload SHA only; NABP raw/text not retained or committed'
 (BASE/(k+'-retrieval.json')).write_text(json.dumps(meta,indent=2)+'\n')
 return {k:{a:meta[a] for a in ['http_status','bytes','error']}}
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
  for result in ex.map(lambda kv:get(*kv),URLS.items()):print(json.dumps(result))
