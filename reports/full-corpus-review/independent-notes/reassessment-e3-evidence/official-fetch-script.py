import urllib.request,urllib.error,pathlib,json,hashlib,datetime,concurrent.futures,subprocess,html.parser
w=pathlib.Path('/workspace/census-reassessment-e3');out=w/'reports/full-corpus-review/independent-notes/reassessment-e3-evidence';pre=str(out.relative_to(w))
urls={'scope': 'https://www.mass.gov/doc/2020-15-scope-of-practice-pdf/download', 'cmr8': 'https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download', 'cmr9': 'https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download', 'ratios2026': 'https://www.mass.gov/doc/2026-02-ratios-supervision-and-dedicated-training-personnel/download', 'mgl112-24': 'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section24'}
class Text(html.parser.HTMLParser):
 def __init__(self):super().__init__();self.a=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
  if t in ('p','div','br','li','h1','h2','h3','h4','h5','section','pre'):self.a.append('\n')
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
  if t in ('p','div','li','section','pre'):self.a.append('\n')
 def handle_data(self,s):
  if not self.skip:self.a.append(s)
def get(k,u):
 at=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=45);b=r.read();code=r.status;resolved=r.url;ct=r.headers.get('Content-Type','')
 except urllib.error.HTTPError as x:b=x.read();code=x.code;resolved=x.url;ct=x.headers.get('Content-Type','')
 ext='.pdf' if b.startswith(b'%PDF') else '.html';p=out/(k+ext);p.write_bytes(b)
 if ext=='.pdf':subprocess.run(['pdftotext','-layout',str(p),str(out/(k+'.txt'))],check=True)
 else:
  parser=Text();parser.feed(b.decode('utf-8',errors='replace'));txt='\n'.join(s.strip() for s in ''.join(parser.a).splitlines() if s.strip());(out/(k+'.txt')).write_text(txt+'\n')
 m={'source_id':k,'official_url':u,'resolved_url':resolved,'retrieved_at_utc':at,'actual_actor':'/root/independent_case_e','http_status':code,'content_type':ct,'raw_path':pre+'/'+p.name,'raw_sha256':hashlib.sha256(b).hexdigest(),'extracted_text_path':pre+'/'+k+'.txt','extracted_text_sha256':hashlib.sha256((out/(k+'.txt')).read_bytes()).hexdigest(),'fresh_live_retrieval':True,'same_day_cache_reuse':False,'old_Nov3_cache_reuse':False,'retrieval_method':'Fresh HTTPS GET with inherited proxy and normal default TLS certificate verification; source author conclusions not used as proof','read_status':'PENDING_DIRECT_READ'}
 (out/(k+'-retrieval.json')).write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');return k,code,len(b),m['raw_sha256']
with concurrent.futures.ThreadPoolExecutor(max_workers=6)as ex:
 for r in ex.map(lambda x:get(*x),urls.items()):print(*r)
