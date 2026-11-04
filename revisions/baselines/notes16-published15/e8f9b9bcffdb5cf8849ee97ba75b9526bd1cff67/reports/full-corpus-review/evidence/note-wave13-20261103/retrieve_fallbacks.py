import concurrent.futures,hashlib,json,re,subprocess,tempfile
from pathlib import Path
import urllib.request, urllib.error
from html.parser import HTMLParser
class TextParser(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag in ("script","style"):self.skip+=1
 def handle_endtag(self,tag):
  if tag in ("script","style"):self.skip=max(0,self.skip-1)
 def handle_data(self,data):
  if not self.skip and data.strip():self.parts.append(data.strip())
OUT=Path(__file__).parent
sources={
'cmr21':'https://www.mass.gov/doc/247-cmr-21-registration-of-outsourcing-facilities/download',
'cmr13':'https://www.mass.gov/doc/247-cmr-13-registration-requirements-and-minimal-professional-standards-for-nuclear-pharmacies/download',
'cmr7':'https://www.mass.gov/doc/247-cmr-7-wholesale-druggists/download',
'cmr20':'https://www.mass.gov/doc/247-cmr-20-reporting/download',
'policy795':'https://www.mass.gov/doc/2023-07-non-sterile-compounding-pdf/download',
'rapid':'https://www.mass.gov/doc/2025-01-rapid-microbial-methods-rapid-sterility-testing-pdf/download',
'copies':'https://www.mass.gov/doc/2020-02-compounding-copies-of-commercially-available-drugs-pdf/download',
'c112s39d':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section39D',
'usp800advisory':'https://www.mass.gov/doc/usp-800-in-community-pharmacies/download',
'niosh':'https://www.cdc.gov/niosh/docs/2025-103/',
'fda503a':'https://www.fda.gov/drugs/human-drug-compounding/fdc-act-provisions-apply-human-drug-compounding',
'503a':'https://www.govinfo.gov/content/pkg/USCODE-2025-title21/html/USCODE-2025-title21-chap9-subchapV-partA-sec353a.htm',
'503b':'https://www.govinfo.gov/content/pkg/USCODE-2025-title21/html/USCODE-2025-title21-chap9-subchapV-partA-sec353b.htm',
'mou':'https://www.fda.gov/drugs/human-drug-compounding/memorandum-understanding-addressing-certain-distributions-compounded-drugs',
'dea5':'https://www.ecfr.gov/current/title-21/section-1307.11',
'ae':'https://www.ecfr.gov/current/title-21/section-310.305',
'ae-guidance':'https://www.fda.gov/media/90997/download',
'sade':'https://www.mass.gov/doc/2025-02-serious-adverse-drug-events-sades-pdf/download',
'exemption2027':'https://www.fda.gov/media/194424/download?attachment=',
'exemptionindex':'https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/exemptions-under-drug-supply-chain-security-act',
'dscsapharm':'https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/pharmacists-utilize-dscsa-requirements-protect-your-patients',
'dscsanotify':'https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/notify-fda-illegitimate-products',
'dscsa581':'https://www.govinfo.gov/content/pkg/USCODE-2025-title21/html/USCODE-2025-title21-chap9-subchapV-partH-sec360eee.htm',
'dscsa582':'https://www.govinfo.gov/content/pkg/USCODE-2025-title21/html/USCODE-2025-title21-chap9-subchapV-partH-sec360eee-1.htm',
'usp797faq':'https://pages.usp.org/rs/711-SXF-172/images/USP_HQS_797_FAQs_December2023_V6__002.pdf?version=0',
'usp797':'https://www.usp.org/compounding/general-chapter-797',
'usp795':'https://www.usp.org/compounding/general-chapter-795',
'inspection':'https://www.mass.gov/doc/sterile-compounding-pharmacy-inspection-template-pdf/download',
'environment':'https://www.mass.gov/doc/2026-03-action-level-environmental-monitoring-results/download',
}
def fetch(kv):
 sid,url=kv
 try:

  try:r=urllib.request.urlopen(url,timeout=55)
  except urllib.error.HTTPError as e:r=e
  raw=r.read(); ext='pdf' if raw.startswith(b'%PDF') else 'html'; h=hashlib.sha256(raw).hexdigest()
  if ext=='pdf':
   with tempfile.TemporaryDirectory() as t:
    Path(t+'/in.pdf').write_bytes(raw); subprocess.run(['pdftotext','-layout',t+'/in.pdf',t+'/out.txt'],check=True); content=Path(t+'/out.txt').read_text()
  else:
   parser=TextParser();parser.feed(raw.decode('utf-8',errors='replace'));content='\n'.join(parser.parts)
  content='\n'.join(line.rstrip() for line in content.splitlines())+'\n'
  blocked=r.status!=200 or bool(re.search(r'\bPage Not Found\b|Access Denied|Request Rejected|404 Not Found|Just a moment',content,re.I))
  meta=dict(official_url=url,final_url=r.geturl(),checked_at='2026-11-03',source_class='PUBLIC_OFFICIAL',retrieval_method='Fresh official HTTPS urllib; pdf pdftotext-layout or PythonHTMLParser text',http_status=r.status,retrieval_status='SOURCE_BLOCKED' if blocked else 'RETRIEVED',original_bytes_sha256=h,bytes=len(raw),effective_date=None,effective_date_note='Individual effective date not yet established; reviewed current official posting 2026-11-03')
  if sid.startswith('usp') and sid!='usp800advisory':
   memo='USP copyright: full fetched bytes/text not redistributed. URL and fetched raw SHA retained in source metadata. Public landing/FAQ is not the full current USP chapter; technical claims require direct current chapter access. AUTHOR read retained only as self-written factual memorandum.\n'
   (OUT/(sid+'-memo.txt')).write_text(memo); meta.update(source_evidence=str(OUT/(sid+'-memo.txt')),source_evidence_sha256=hashlib.sha256(memo.encode()).hexdigest(),copyright_limitation='No full USP chapter retrieved. No fetched USP text redistributed.',retrieval_status='PUBLIC_LANDING_OR_FAQ_ONLY_NOT_FULL_CHAPTER' if not blocked else 'SOURCE_BLOCKED')
  else:
   (OUT/(sid+'.'+ext)).write_bytes(raw); (OUT/(sid+'.txt')).write_text(content); meta.update(original_file=str(OUT/(sid+'.'+ext)),source_evidence=str(OUT/(sid+'.txt')),source_evidence_sha256=hashlib.sha256(content.encode()).hexdigest())
  return sid,meta,content[:450]
 except Exception as e:
  memo=f'HTTPS request failed: {type(e).__name__}: {e}\n';(OUT/(sid+'-error.txt')).write_text(memo)
  return sid,dict(official_url=url,checked_at='2026-11-03',source_class='PUBLIC_OFFICIAL',retrieval_status='SOURCE_BLOCKED',http_status=None,effective_date=None,effective_date_note='Not established; fetch failed',source_evidence=str(OUT/(sid+'-error.txt')),source_evidence_sha256=hashlib.sha256(memo.encode()).hexdigest()),memo
sources={
'503a-code25pdf':'https://www.govinfo.gov/content/pkg/USCODE-2025-title21/pdf/USCODE-2025-title21-chap9-subchapV-partA-sec353a.pdf',
'503b-code25pdf':'https://www.govinfo.gov/content/pkg/USCODE-2025-title21/pdf/USCODE-2025-title21-chap9-subchapV-partA-sec353b.pdf',
'dscsa581-code25pdf':'https://www.govinfo.gov/content/pkg/USCODE-2025-title21/pdf/USCODE-2025-title21-chap9-subchapV-partH-sec360eee.pdf',
'dscsa582-code25pdf':'https://www.govinfo.gov/content/pkg/USCODE-2025-title21/pdf/USCODE-2025-title21-chap9-subchapV-partH-sec360eee-1.pdf',
}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(fetch,sources.items()))
manifest=json.loads((OUT/'sources-manifest.json').read_text());manifest.update({s:m for s,m,_ in results});manifest['niosh']['retrieval_status']='SOURCE_BLOCKED';manifest['niosh']['failure_note']='HTTP200 contained empty non-source body; no credit'
(OUT/'sources-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
for sid,m,p in results:print(sid,m['http_status'],m['retrieval_status'],m.get('bytes'),repr(p[:120]))
