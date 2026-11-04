from pathlib import Path
from datetime import datetime,timezone
import urllib.request,urllib.error,hashlib,json,concurrent.futures,subprocess
BASE=Path('reports/full-corpus-review/phase10-d-evidence')
URLS={
'c13s22':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleII/Chapter13/Section22',
'cmr6':'https://www.mass.gov/doc/247-cmr-6-licensure-of-pharmacies/download',
'cmr9':'https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download',
'cmr10':'https://www.mass.gov/doc/247-cmr-10-disciplinary-proceedings/download',
'cmr14':'https://www.mass.gov/doc/247-cmr-14-petition-for-waiver/download',
'policy2022-02':'https://www.mass.gov/doc/2022-02-extended-absence-or-departure-of-a-manager-of-record-or-designated-pharmacist-in-charge-pdf/download',
'cmr6-page':'https://www.mass.gov/regulations/247-CMR-600-licensure-of-pharmacies',
'cmr9-page':'https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards',
'cmr10-page':'https://www.mass.gov/regulations/247-CMR-1000-disciplinary-proceedings',
'cmr14-page':'https://www.mass.gov/regulations/247-CMR-1400-petition-for-waiver'}
def now():return datetime.now(timezone.utc).isoformat()
def fetch(pair):
 sid,url=pair;start=now();error=None;data=b'';status=None;final=url;headers={}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (independent legal source verification)'}),timeout=45) as r:
   data=r.read();status=r.status;final=r.url;headers=dict(r.headers)
 except urllib.error.HTTPError as e:
  status=e.code;data=e.read();headers=dict(e.headers);error=str(e)
 except Exception as e:error=repr(e)
 raw=BASE/(sid+'.raw');raw.write_bytes(data)
 typ='pdf' if data.startswith(b'%PDF-') else 'html'
 txt=BASE/(sid+'.txt')
 if typ=='pdf':subprocess.run(['pdftotext','-layout',str(raw),str(txt)],check=True)
 else:
  from html.parser import HTMLParser
  class Extract(HTMLParser):
   def __init__(self):super().__init__();self.parts=[]
   def handle_data(self,d):
    if d.strip():self.parts.append(d.strip())
  parser=Extract();parser.feed(data.decode('utf-8',errors='replace'));txt.write_text('\n'.join(parser.parts))
 meta={'source_id':sid,'official_url':url,'requested_url':url,'final_url':final,'http_status':status,'retrieved_at':now(),'retrieval_started_at':start,'timezone':'Etc/UTC','transport':'urllib.request; default verified TLS; inherited proxy/CA','error':error,'headers':headers,'document_type':typ,'raw_path':str(raw),'raw_sha256':hashlib.sha256(data).hexdigest(),'text_evidence_path':str(txt),'text_sha256':hashlib.sha256(txt.read_bytes()).hexdigest(),'body_bytes':len(data),'read_at':None,'is_legal_evidence':status==200 and len(data)>1000 and (typ=='pdf' or sid=='c13s22')}
 (BASE/(sid+'-retrieval.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
 return {k:meta[k] for k in ('source_id','http_status','document_type','body_bytes','error')}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 for result in pool.map(fetch,URLS.items()):print(json.dumps(result))
