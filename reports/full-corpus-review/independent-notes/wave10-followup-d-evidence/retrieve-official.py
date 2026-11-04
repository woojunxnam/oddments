from pathlib import Path
from datetime import datetime,timezone
from html.parser import HTMLParser
import urllib.request,urllib.error,hashlib,json,concurrent.futures,subprocess
B=Path('reports/full-corpus-review/independent-notes/wave10-followup-d-evidence')
URLS={
'cmr9':'https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download',
'policy2018-01':'https://www.mass.gov/doc/2018-01-permitted-prescription-changes-and-additions-pdf/download',
'hipaa164-530':'https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.530',
'cmr15':'https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download',
'cmr700':'https://www.mass.gov/doc/105-cmr-700-implementation-of-mgl-c94c-0/download',
'cfr208':'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-208',
'cfr310-501':'https://www.ecfr.gov/current/title-21/section-310.501',
'cfr310-515':'https://www.ecfr.gov/current/title-21/section-310.515',
'cfr456-705':'https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-C/part-456/subpart-K/section-456.705',
'fda-medicines':'https://www.fda.gov/patients/learn-about-your-medicines',
'cdc-vis':'https://www.cdc.gov/vaccines/hcp/about-vis/index.html',
'fda-rems':'https://www.fda.gov/drugs/drug-safety-and-availability/risk-evaluation-and-mitigation-strategies-rems',
'fda-clozapine':'https://www.fda.gov/drugs/drug-safety-and-availability/fda-removes-risk-evaluation-and-mitigation-strategy-rems-program-antipsychotic-drug-clozapine',
'fda-mifepristone':'https://www.fda.gov/drugs/postmarket-drug-safety-information-patients-and-providers/questions-and-answers-mifepristone-medical-termination-pregnancy-through-ten-weeks-gestation',
'policy2023-05':'https://www.mass.gov/doc/2023-05-access-to-reproductive-health-medications/download',
'fda-mifepristone-rems':'https://www.accessdata.fda.gov/drugsatfda_docs/rems/Mifepristone_2023_01_03_REMS_Full.pdf',
'cfr1306-04':'https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.04',
'usc355-1':'https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title21-section355-1&num=0&edition=prelim'}
class E(HTMLParser):
 def __init__(self):super().__init__();self.p=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if d.strip() and not self.skip:self.p.append(d.strip())
def now():return datetime.now(timezone.utc).isoformat()
def fetch(pair):
 sid,url=pair;at=now();data=b'';code=None;final=url;headers={};error=None
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (official primary source audit)'}),timeout=45) as r:data=r.read();code=r.status;final=r.url;headers=dict(r.headers)
 except urllib.error.HTTPError as e:code=e.code;data=e.read();headers=dict(e.headers);error=str(e)
 except Exception as e:error=repr(e)
 raw=B/(sid+'.raw');raw.write_bytes(data);txt=B/(sid+'.txt');typ='pdf' if data.startswith(b'%PDF-') else 'html'
 if typ=='pdf':subprocess.run(['pdftotext','-layout',str(raw),str(txt)],check=True)
 else:
  p=E();p.feed(data.decode('utf-8',errors='replace'));txt.write_text('\n'.join(p.p))
 m={'source_id':sid,'official_url':url,'requested_url':url,'final_url':final,'http_status':code,'retrieved_at':at,'retrieval_completed_at':now(),'read_at':None,'timezone':'Etc/UTC','transport':'urllib with default verified TLS and inherited proxy/CA','headers':headers,'error':error,'document_type':typ,'raw_path':str(raw),'raw_sha256':hashlib.sha256(data).hexdigest(),'text_evidence_path':str(txt),'text_sha256':hashlib.sha256(txt.read_bytes()).hexdigest(),'body_bytes':len(data),'document_identity_confirmed':False,'legal_payload_confirmed':False}
 (B/(sid+'-retrieval.json')).write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
 return {k:m[k] for k in ['source_id','http_status','document_type','body_bytes','error']}
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
  for x in pool.map(fetch,URLS.items()):print(json.dumps(x))
