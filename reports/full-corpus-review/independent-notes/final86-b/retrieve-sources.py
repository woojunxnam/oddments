from pathlib import Path
import json,urllib.request,datetime,hashlib,subprocess,concurrent.futures
from html.parser import HTMLParser
B=Path('reports/full-corpus-review/independent-notes/final86-b');S=B/'sources';S.mkdir(exist_ok=True)
class P(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.main=0;self.all=[];self.body=[]
 def handle_starttag(self,t,a):
  if t in ['script','style','noscript']:self.skip+=1
  if t=='main':self.main+=1
 def handle_endtag(self,t):
  if t in ['script','style','noscript']:self.skip=max(0,self.skip-1)
  if t=='main':self.main=max(0,self.main-1)
 def handle_data(self,d):
  if not self.skip and d.strip():
   self.all.append(d.strip())
   if self.main:self.body.append(d.strip())
def fetch(k,url):
 m={'official_url':url,'attempted_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'urllib HTTPS GET inherited proxy; TLS verification enabled'}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (Independent source review)'}),timeout=35) as r:raw=r.read();m.update(status=r.status,resolved_url=r.url,headers=dict(r.headers),retrieved_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
  rp=S/(k+('.pdf' if raw.startswith(b'%PDF') else '.html'));tp=S/(k+'.txt');rp.write_bytes(raw)
  if raw.startswith(b'%PDF'):subprocess.run(['pdftotext','-layout',str(rp),str(tp)],check=True)
  else:p=P();p.feed(raw.decode(errors='replace'));tp.write_text('\n'.join(p.body or p.all)+'\n')
  text=tp.read_text();soft=any(x in text.lower() for x in ['page not found','requested page could not be found','access denied','error 404','403 forbidden'])
  m.update(retrieval_status='SOFT_200_ERROR' if soft else 'LIVE_HTTPS_GET_PENDING_CONTENT_REVIEW',raw_path=str(rp),raw_sha256=hashlib.sha256(raw).hexdigest(),text_path=str(tp),text_sha256=hashlib.sha256(tp.read_bytes()).hexdigest())
 except Exception as e:m.update(retrieval_status='GET_FAILED',error=str(e))
 (S/(k+'.meta.json')).write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');return k,m.get('status',m.get('error')),m.get('retrieval_status'),m.get('raw_sha256')
urls={
'definitions':'https://www.mass.gov/doc/2025-02-definitions-pdf/download','cqi':'https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download','reporting':'https://www.mass.gov/doc/247-cmr-20-reporting/download','defective':'https://www.mass.gov/doc/2024-04-defective-drug-preparations/download','wholesale':'https://www.mass.gov/doc/247-cmr-7-wholesale-druggists/download','conduct':'https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download','outsourcingma':'https://www.mass.gov/doc/247-cmr-21-registration-requirements-and-professional-standards-for-outsourcing-facilities-0/download','39D':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section39D',
'exemption2024':'https://www.fda.gov/media/179256/download?attachment','exemption2026':'https://www.fda.gov/media/194424/download?attachment=',
'pharmacists':'https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/pharmacists-utilize-dscsa-requirements-protect-your-patients','illegitimate':'https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/notify-fda-illegitimate-products','ind':'https://www.fda.gov/drugs/types-applications/investigational-new-drug-ind-application','nda':'https://www.fda.gov/drugs/types-applications/new-drug-application-nda','anda':'https://www.fda.gov/drugs/types-applications/abbreviated-new-drug-application-anda','bla':'https://www.fda.gov/vaccines-blood-biologics/development-approval-process-cber/biologics-license-applications-bla-process-cber','biosimilar':'https://www.fda.gov/drugs/biosimilars/biosimilar-basics-patients','otc':'https://www.fda.gov/drugs/types-applications/drug-application-process-nonprescription-drugs','monograph':'https://www.fda.gov/drugs/otc-drug-review-process-otc-drug-monographs','offlabel':'https://www.fda.gov/patients/learn-about-expanded-access-and-other-treatment-options/understanding-unapproved-use-approved-drugs-label','eua':'https://www.fda.gov/emergency-preparedness-and-response/mcm-legal-regulatory-and-policy-framework/emergency-use-authorization','fdaterms':'https://www.fda.gov/consumers/consumer-updates/understanding-fda-terms-possible-new-therapies-prevent-and-treat-diseases','expanded':'https://www.fda.gov/news-events/public-health-focus/expanded-access','supplement':'https://www.fda.gov/food/dietary-supplements','ndi':'https://www.fda.gov/food/new-dietary-ingredient-ndi-notification-process/new-dietary-ingredients-dietary-supplements-background-industry','cosmetic':'https://www.fda.gov/cosmetics/cosmetics-laws-regulations/fda-authority-over-cosmetics-how-cosmetics-are-not-fda-approved-are-fda-regulated','homeopathic':'https://www.fda.gov/drugs/information-drug-class/homeopathic-products','510k':'https://www.fda.gov/medical-devices/device-approvals-and-clearances/510k-clearances','ndc':'https://www.fda.gov/drugs/drug-approvals-and-databases/ndc-product-file-definitions','ndcformat':'https://www.fda.gov/drugs/electronic-drug-registration-and-listing-system-edrls/national-drug-code-format','labels':'https://labels.fda.gov/','compounding':'https://www.fda.gov/drugs/human-drug-compounding/fdc-act-provisions-apply-human-drug-compounding','outsourcing':'https://www.fda.gov/drugs/human-drug-compounding/information-outsourcing-facilities','503Breports':'https://www.fda.gov/drugs/human-drug-compounding/adverse-event-reporting-outsourcing-facilities-under-section-503b-federal-food-drug-and-cosmetic-act','oos':'https://www.fda.gov/media/71001/download',
'recall':'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-7/subpart-A/section-7.3','310.305':'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-310/subpart-D/section-310.305','1307.11':'https://www.ecfr.gov/current/title-21/section-1307.11'}
for sec in ['351','352','353b','355h','360eee','360eee-1']:urls['usc'+sec]='https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title21-section'+sec+'&num=0&edition=prelim'
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
  for r in ex.map(lambda z:fetch(*z),urls.items()):print(*r,flush=True)
