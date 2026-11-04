import concurrent.futures,datetime,hashlib,json,pathlib,subprocess,urllib.request
ROOT=pathlib.Path('/workspace/independent-phase6-g');OUT=ROOT/'reports/full-corpus-review/evidence/independent-phase6-g';OUT.mkdir(parents=True,exist_ok=True)
SPECS={
'admin':'https://www.mass.gov/doc/pharmacist-administration-of-medications-pdf/download',
'cdtm':'https://www.mass.gov/doc/247-cmr-16-collaborative-drug-therapy-management/download',
'physician':'https://www.mass.gov/doc/243-cmr-2-licensing-and-the-practice-of-medicine-0/download',
'ec':'https://www.mass.gov/info-details/emergency-contraception-information-for-pharmacies',
'ec-order':'https://www.mass.gov/doc/standing-order-for-dispensing-emergency-contraception-pills/download',
'naloxone':'https://www.mass.gov/doc/2024-01-naloxone-dispensing-pdf/download',
'practice':'https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download',
'changes':'https://www.mass.gov/doc/2018-01-permitted-prescription-changes-and-additions-pdf/download',
'format':'https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download',
'law19a':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section19A',
'law19b':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section19B',
'law23':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section23',
'clozapine':'https://www.fda.gov/drugs/drug-safety-communications/fda-removes-risk-evaluation-and-mitigation-strategy-rems-program-antipsychotic-drug-clozapine',
'mifepristone':'https://www.fda.gov/drugs/postmarket-drug-safety-information-patients-and-providers/questions-and-answers-mifepristone-medical-termination-pregnancy-through-ten-weeks-gestation',
'sublocade':'https://www.accessdata.fda.gov/drugsatfda_docs/label/2026/209819s037lbl.pdf',
'brixadi':'https://www.accessdata.fda.gov/drugsatfda_docs/label/2026/210136s012lbl.pdf',
'spravato':'https://www.accessdata.fda.gov/drugsatfda_docs/label/2026/211243s026lbl.pdf',
'ipledge':'https://www.fda.gov/drugs/postmarket-drug-safety-information-patients-and-providers/ipledge-risk-evaluation-and-mitigation-strategy-rems',
'opill':'https://www.fda.gov/news-events/press-announcements/fda-approves-first-nonprescription-daily-oral-contraceptive',
'ella':'https://www.accessdata.fda.gov/drugsatfda_docs/label/2021/022474s011lbl.pdf',
'narcan':'https://www.fda.gov/news-events/press-announcements/fda-approves-first-over-counter-naloxone-nasal-spray',
'rems':'https://www.fda.gov/drugs/drug-safety-and-availability/risk-evaluation-and-mitigation-strategies-rems',
'xwaiver':'https://www.samhsa.gov/substance-use/treatment/statutes-regulations-guidelines/mat-act',
'1306-02':'https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.02',
'1306-03':'https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.03',
'1306-04':'https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.04',
'1306-05':'https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.05',
'1306-07':'https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.07',
'1306-08':'https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.08',
'1306-11':'https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.11',
'1306-22':'https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.22',
'1306-25':'https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.25',
'1307-11':'https://www.ecfr.gov/current/title-21/chapter-II/part-1307/section-1307.11',
'1308-12':'https://www.ecfr.gov/current/title-21/chapter-II/part-1308/section-1308.12',
'1308-13':'https://www.ecfr.gov/current/title-21/chapter-II/part-1308/section-1308.13',
'1308-14':'https://www.ecfr.gov/current/title-21/chapter-II/part-1308/section-1308.14',
'nabp':'https://nabp.pharmacy/wp-content/uploads/2020/07/MPJE-Sample-Questions.pdf',
}
def get(item):
 sid,url=item;now=datetime.datetime.now(datetime.timezone.utc);m={'source_id':sid,'official_url':url,'law_checked_date':now.date().isoformat(),'retrieved_at':now.isoformat(),'tls_verification':True,'proxy':'inherited normal proxy','retrieval_method':'LIVE_OFFICIAL_HTTPS_urllib','live_attempt':True}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (independent legal review)'}),timeout=35) as z:raw=z.read();m.update(http_status=z.status,resolved_url=z.url,content_type=z.headers.get('content-type'))
 except Exception as e:
  m.update(live_error=str(e),http_status=getattr(e,'code',None));(OUT/(sid+'-retrieval.json')).write_text(json.dumps(m,indent=2)+'\n');return sid,m
 m['raw_sha256']=hashlib.sha256(raw).hexdigest();t=OUT/(sid+('.pdf' if raw.startswith(b'%PDF') else '.html'));t.write_bytes(raw)
 if raw.startswith(b'%PDF'):subprocess.run(['pdftotext','-layout',str(t),str(OUT/(sid+'.txt'))],check=True)
 else:
  from lxml import html
  try:
   d=html.fromstring(raw.decode('utf-8',errors='replace'))
   for n in d.xpath('//script|//style|//nav|//header|//footer'):n.drop_tree()
   txt='\n'.join(x.strip() for x in d.text_content().splitlines() if x.strip())
  except Exception:txt=raw.decode(errors='replace')
  (OUT/(sid+'.txt')).write_text(txt)
 m.update(raw_evidence_path=str(t.relative_to(ROOT)),text_evidence_path=str((OUT/(sid+'.txt')).relative_to(ROOT)),text_sha256=hashlib.sha256((OUT/(sid+'.txt')).read_bytes()).hexdigest(),body_verification='PENDING_DIRECT_READ_NOT_AUTOMATICALLY_VERIFIED');(OUT/(sid+'-retrieval.json')).write_text(json.dumps(m,indent=2)+'\n');return sid,m
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
  for sid,m in ex.map(get,SPECS.items()):print(sid,m.get('http_status'),m.get('raw_sha256'))
