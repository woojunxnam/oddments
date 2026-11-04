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
'247-13':'https://www.mass.gov/doc/247-cmr-13-registration-requirements-and-minimal-professional-standards-for-nuclear-pharmacies/download',
'247-15':'https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download',
'247-20':'https://www.mass.gov/doc/247-cmr-20-reporting/download',
'policy-definitions':'https://www.mass.gov/doc/2025-02-definitions-pdf/download',
'247-9':'https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download',
'mgl39d':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section39D',
'mgl94c9':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section9',
'fda-applications':'https://www.fda.gov/drugs/how-drugs-are-developed-and-approved/types-applications',
'fda-otc':'https://www.fda.gov/drugs/types-applications/drug-application-process-nonprescription-drugs',
'fda-ndc':'https://www.fda.gov/drugs/drug-approvals-and-databases/national-drug-code-directory',
'fda-eua':'https://www.fda.gov/emergency-preparedness-and-response/mcm-legal-regulatory-and-policy-framework/emergency-use-authorization',
'fda-dscsa':'https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/pharmacists-utilize-dscsa-requirements-protect-your-patients',
'fda-exemptions':'https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/exemptions-under-drug-supply-chain-security-act',
'fda-notify':'https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/notify-fda-illegitimate-products',
'fda-recalls':'https://www.fda.gov/safety/industry-guidance-recalls/recalls-background-and-definitions',
'fda-recall-enforce':'https://www.fda.gov/safety/enforcement-reports/enforcement-report-information-and-definitions',
'21usc360eee1':'https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title21-section360eee-1&num=0&edition=prelim',
'21usc353b':'https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title21-section353b&num=0&edition=prelim',
'nabp-sample':'https://nabp.pharmacy/wp-content/uploads/2020/07/MPJE-Sample-Questions.pdf',
'nabp-competency':'https://nabp.pharmacy/programs/examinations/mpje/competency-statements/',
'nabp-format':'https://nabp.pharmacy/programs/examinations/mpje/take-the-mpje-exam/'
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
