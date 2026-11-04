import concurrent.futures, datetime, hashlib, json, pathlib, subprocess, urllib.request, urllib.error
ROOT = pathlib.Path(__file__).resolve().parent
loc = json.loads((ROOT/'source-locators.json').read_bytes())['sources']
urls = {k:v['url'] for k,v in loc.items()}
urls.update({
 'nabp-sample':'https://nabp.pharmacy/wp-content/uploads/2020/07/MPJE-Sample-Questions.pdf',
 'supremacy':'https://constitution.congress.gov/browse/article-6/clause-2/',
 'fda-opill':'https://www.fda.gov/news-events/press-announcements/fda-approves-first-nonprescription-daily-oral-contraceptive',
})
(ROOT/'official').mkdir(exist_ok=True)
def fetch(pair):
 key,url=pair; start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 meta={'source_id':key,'requested_url':url,'official_url':url,'retrieved_at':start,'retrieval_method':'Python urllib.request via inherited HTTPS proxy; TLS verification enabled','http_status':None,'final_url':None,'raw_sha256':None,'text_sha256':None,'legal_evidence_usable':False}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (independent public-source review)'})
  with urllib.request.urlopen(req,timeout=45) as r: raw=r.read(); meta.update(http_status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'))
 except urllib.error.HTTPError as e: raw=e.read(); meta.update(http_status=e.code,final_url=e.url,error=str(e))
 except Exception as e: raw=b'';meta['error']=str(e)
 meta['raw_sha256']=hashlib.sha256(raw).hexdigest()
 if key.startswith('nabp'):
  tmp=pathlib.Path('/tmp/phase11-a-'+key+'.pdf');tmp.write_bytes(raw)
  out=subprocess.run(['pdftotext','-layout',str(tmp),'-'],capture_output=True)
  text=out.stdout.decode(errors='replace')
  meta['retention']='URL, raw/text hashes and independently written comparison memo only; NABP full raw/text not committed'
  meta['temporary_path']=str(tmp)
 else:
  ext='.pdf' if raw.startswith(b'%PDF') else '.html'
  file=ROOT/'official'/(key+ext);file.write_bytes(raw)
  meta['evidence_path']=str(file.relative_to(ROOT.parents[2]))
  if ext=='.pdf':text=subprocess.run(['pdftotext','-layout',str(file),'-'],capture_output=True).stdout.decode(errors='replace')
  else:
   from html.parser import HTMLParser
   class Extractor(HTMLParser):
    def __init__(self):super().__init__();self.skip=0;self.lines=[]
    def handle_starttag(self,tag,attrs):
     if tag in ('script','style'):self.skip+=1
    def handle_endtag(self,tag):
     if tag in ('script','style'):self.skip=max(0,self.skip-1)
    def handle_data(self,data):
     if not self.skip and data.strip():self.lines.append(data.strip())
   parser=Extractor();parser.feed(raw.decode(errors='replace'));text='\n'.join(parser.lines)
  textfile=ROOT/'official'/(key+'.txt');textfile.write_text(text)
  meta['text_evidence_path']=str(textfile.relative_to(ROOT.parents[2]))
 meta['text_sha256']=hashlib.sha256(text.encode()).hexdigest()
 meta['legal_evidence_usable']=meta['http_status']==200 and len(text)>150 and not any(x in text[:1500].lower() for x in ['page not found','access denied','request blocked'])
 metafile=ROOT/'official'/(key+'.meta.json');metafile.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
 return {k:meta[k] for k in ('source_id','http_status','legal_evidence_usable','final_url')}|{'text_length':len(text)}
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
  for result in pool.map(fetch,urls.items()):print(json.dumps(result))
