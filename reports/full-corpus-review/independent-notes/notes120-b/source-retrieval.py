import json,urllib.request,hashlib,datetime,subprocess,concurrent.futures
from pathlib import Path
from html.parser import HTMLParser
B=Path('reports/full-corpus-review/independent-notes/notes120-b');S=B/'sources';S.mkdir(exist_ok=True)
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
urls={
'cdtm':'https://www.mass.gov/doc/247-cmr-16-collaborative-drug-therapy-management/download','intern':'https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download','conduct':'https://www.mass.gov/doc/247-cmr-9-code-of-professional-conduct/download','prescribing':'https://www.mass.gov/doc/pharmacist-prescribing-of-certain-medications/download','administration':'https://www.mass.gov/doc/pharmacist-administration-of-medications-pdf/download','ecfaq':'https://www.mass.gov/info-details/emergency-contraception-information-for-pharmacies','ecorder':'https://www.mass.gov/doc/standing-order-for-dispensing-emergency-contraception-pills/download','naloxone':'https://www.mass.gov/doc/2024-01-naloxone-dispensing-pdf/download','naloxoneorder':'https://www.mass.gov/doc/statewide-standing-order/download','ept':'https://www.mass.gov/doc/2020-08-expedited-partner-therapy-prescriptions-pdf/download','access':'https://www.mass.gov/info-details/massachusetts-access-law-common-questions-and-answers-qa','birthcontrol':'https://www.mass.gov/info-details/information-for-pharmacists-about-access-to-birth-control-and-emergency-contraception','hivindex':'https://www.mass.gov/lists/guidelines-for-pharmacists-to-prescribe-oral-prep-pep-sti-treatment-and-doxypep','opill':'https://www.fda.gov/news-events/press-announcements/fda-approves-first-nonprescription-daily-oral-contraceptive','planb':'https://www.fda.gov/drugs/postmarket-drug-safety-information-patients-and-providers/plan-b-one-step-15-mg-levonorgestrel-information','ella':'https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=2bf93d23-cddd-4613-9066-5b5fa090404b','mifepristone':'https://www.fda.gov/drugs/postmarket-drug-safety-information-patients-and-providers/questions-and-answers-mifepristone-medical-termination-pregnancy-through-ten-weeks-gestation','truvada':'https://medlineplus.gov/druginfo/meds/a612036.html'}
for k,chapter,section in [('cdtmlaw','112','24B%201~2'),('definition','94C','1'),('eclaw','94C','19A'),('naloxonelaw','94C','19B'),('prescribinglaw','94C','19F')]:urls[k]='https://malegislature.gov/Laws/GeneralLaws/PartI/Title'+('XVI' if chapter=='112' else 'XV')+'/Chapter'+chapter+'/Section'+section
for k in ['A','C','D','S']:urls['medindex'+k]='https://medlineplus.gov/druginfo/drug_'+k+'a.html'
def fetch(k,url):
 m={'official_url':url,'attempted_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'urllib HTTPS GET; inherited proxy; TLS verification enabled'}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (Independent legal source review)'}),timeout=40) as r:raw=r.read();m.update(status=r.status,resolved_url=r.url,headers=dict(r.headers),retrieved_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),retrieval_status='LIVE_HTTPS_GET')
  rp=S/(k+('.pdf' if raw.startswith(b'%PDF') else '.html'));tp=S/(k+'.txt');rp.write_bytes(raw)
  if raw.startswith(b'%PDF'):subprocess.run(['pdftotext','-layout',str(rp),str(tp)],check=True)
  else:p=P();p.feed(raw.decode(errors='replace'));tp.write_text('\n'.join(p.body or p.all)+'\n')
  m.update(raw_path=str(rp),raw_sha256=hashlib.sha256(raw).hexdigest(),text_path=str(tp),text_sha256=hashlib.sha256(tp.read_bytes()).hexdigest())
 except Exception as e:m.update(retrieval_status='LIVE_GET_FAILED',error=str(e))
 (S/(k+'.meta.json')).write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');return k,m.get('status',m.get('error')),m.get('raw_sha256')
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as x:
 for r in x.map(lambda z:fetch(*z),urls.items()):print(*r)
