import urllib.request,pathlib,json,hashlib,datetime,subprocess,concurrent.futures
from html.parser import HTMLParser
class TextParser(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,s):self.parts.append(s)
 def text(self):return "\n".join(x.strip() for x in self.parts if x.strip())

D=pathlib.Path(__file__).resolve().parent.relative_to(pathlib.Path.cwd().resolve())
urls={
'opill-index':'https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name=Opill',
'opill-current':'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=69dfa2ac-6a7e-4587-929c-9acabd97973b'
}
def get(kv):
 k,u=kv;t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  r=urllib.request.urlopen(u,timeout=60);raw=r.read();ext='pdf' if raw.startswith(b'%PDF') else 'html';rp=D/(k+'.'+ext);rp.write_bytes(raw)
  if ext=='pdf':subprocess.run(['pdftotext','-layout',str(rp),str(D/(k+'.txt'))],check=True)
  else:
   parser=TextParser();parser.feed(raw.decode('utf-8',errors='replace'));(D/(k+'.txt')).write_text(parser.text())
  meta=dict(official_url=u,final_url=r.url,status_code=r.status,response_headers=dict(r.headers),retrieved_at=t,retrieval_completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),method='urllib HTTPS GET; default certificate verification; ordinary configured proxy; no TLS bypass',raw_path=str(rp),raw_sha256=hashlib.sha256(raw).hexdigest(),text_path=str(D/(k+'.txt')),text_sha256=hashlib.sha256((D/(k+'.txt')).read_bytes()).hexdigest(),content_type=r.headers.get('Content-Type'),response_bytes=len(raw))
 except Exception as e:meta=dict(official_url=u,retrieved_at=t,error=repr(e))
 (D/(k+'.meta.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');return k,meta.get('status_code'),meta.get('response_bytes'),meta.get('error')
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
 for r in ex.map(get,urls.items()):print(r)
