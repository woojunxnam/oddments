import concurrent.futures, datetime, gzip, hashlib, json, pathlib, subprocess, urllib.request

ROOT=pathlib.Path('/workspace/independent-phase3-g')
OUT=ROOT/'reports/full-corpus-review/evidence/independent-phase3-g'
OUT.mkdir(parents=True,exist_ok=True)
CACHE=pathlib.Path('/workspace/oddments/reports/full-corpus-review/evidence')
SPECS={
 'vaccine':('https://www.mass.gov/doc/2023-02-vaccine-administration-pdf/download','note-wave11-20261103/vaccine.pdf'),
 'administration':('https://www.mass.gov/doc/pharmacist-administration-of-medications-pdf/download','wave5-3-20261103/admin.pdf'),
 'cdtm':('https://www.mass.gov/doc/247-cmr-16-collaborative-drug-therapy-management/download','wave7-3-20261103/cdtm.pdf'),
 'cdtm-statute':('https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section24B%201~2','wave7-3-20261103/cdtmlaw.html'),
 'ec-order':('https://www.mass.gov/doc/standing-order-for-dispensing-emergency-contraception-pills/download','wave7-3-20261103/ecorder.pdf'),
 'ec-pharmacy':('https://www.mass.gov/info-details/emergency-contraception-information-for-pharmacies','wave7-3-20261103/ec.html'),
 'naloxone-policy':('https://www.mass.gov/doc/2024-01-naloxone-dispensing-pdf/download','wave7-3-20261103/nalox.pdf'),
 'opioid-antagonist-law':('https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section19B','wave7-3-20261103/law19b.html'),
 'contraception-law':('https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section19F',None),
 'practice':('https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download',None),
 'miis':('https://www.mass.gov/doc/105-cmr-222-massachusetts-immunization-information-system/download',None),
 'clozapine':('https://www.fda.gov/drugs/drug-safety-and-availability/fda-removes-risk-evaluation-and-mitigation-strategy-rems-program-antipsychotic-drug-clozapine','wave5-3-20261103/clozapine.html'),
 'boxed-rems':('https://www.fda.gov/drugs/risk-evaluation-and-mitigation-strategies-rems/rems-different-boxed-warnings',None),
 'brixadi':('https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=5d8a8fd0-8619-422a-a664-d1d2e8970f48','wave5-3-20261103/brixadi.html'),
 'spravato':('https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=d81a6a79-a74a-44b7-822c-0dfa3036eaed','wave5-3-20261103/spravato.html'),
 'tirf':('https://www.fda.gov/drugs/risk-evaluation-and-mitigation-strategies-rems/transmucosal-immediate-release-fentanyl-tirf-medicines','wave5-3-20261103/tirf.html'),
 'planb':('https://www.fda.gov/drugs/postmarket-drug-safety-information-patients-and-providers/plan-b-one-step-15-mg-levonorgestrel-information','wave7-3-20261103/planb.html'),
 'opill':('https://www.fda.gov/news-events/press-announcements/fda-approves-first-nonprescription-daily-oral-contraceptive','wave7-3-20261103/opill.html'),
 'ella':('https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=50a53ff5-0249-4747-a58e-a78c3c915fc9',None),
 'mifepristone':('https://www.fda.gov/drugs/postmarket-drug-safety-information-patients-and-providers/questions-and-answers-mifepristone-medical-termination-pregnancy-through-ten-weeks-gestation','wave7-3-20261103/mife.html'),
 'sublocade':('https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=6189fb21-9432-45f8-8481-0bfaf3ccde95','wave7-3-20261103/sublocade.html'),
 'vis':('https://www.cdc.gov/vaccines/hcp/vis/about/facts-vis.html',None),
}

def get(item):
 sid,(url,cache)=item
 meta={'source_id':sid,'official_url':url,'law_checked_date':'2026-11-03','retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tls_verification':True,'proxy':'inherited normal proxy','retrieval_method':'LIVE_OFFICIAL_HTTPS_urllib','live_attempt':True}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (independent legal review)'})
  with urllib.request.urlopen(req,timeout=35) as r:
   raw=r.read();meta.update(http_status=r.status,resolved_url=r.url,content_type=r.headers.get('content-type'))
 except Exception as e:
  meta['live_error']=str(e);meta['http_status']=getattr(e,'code',None)
  if cache and (CACHE/cache).exists():
   raw=(CACHE/cache).read_bytes();meta.update(retrieval_method='SAME_DAY_OFFICIAL_RAW_CACHE_REREAD_AFTER_LIVE_FAILURE',cache_source_path=str(CACHE/cache),cache_retrieved_date='2026-11-03')
  else:
   (OUT/(sid+'-retrieval.json')).write_text(json.dumps(meta,indent=2)+'\n');return sid,meta
 meta['raw_sha256']=hashlib.sha256(raw).hexdigest()
 if raw.startswith(b'%PDF'):
  target=OUT/(sid+'.pdf');target.write_bytes(raw)
  subprocess.run(['pdftotext','-layout',str(target),str(OUT/(sid+'.txt'))],check=True)
 else:
  target=OUT/(sid+'.html.gz');target.write_bytes(gzip.compress(raw,mtime=0))
  from lxml import html
  try:
   doc=html.fromstring(raw)
   for n in doc.xpath('//script|//style|//nav|//header|//footer'):n.drop_tree()
   txt='\n'.join(x.strip() for x in doc.text_content().splitlines() if x.strip())
  except Exception:txt=raw.decode(errors='replace')
  (OUT/(sid+'.txt')).write_text(txt)
 meta['raw_evidence_path']=str(target.relative_to(ROOT));meta['text_evidence_path']=str((OUT/(sid+'.txt')).relative_to(ROOT));meta['text_sha256']=hashlib.sha256((OUT/(sid+'.txt')).read_bytes()).hexdigest()
 meta['body_verification']='PENDING_DIRECT_READ_NOT_AUTOMATICALLY_VERIFIED'
 (OUT/(sid+'-retrieval.json')).write_text(json.dumps(meta,indent=2)+'\n')
 return sid,meta

if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=7) as ex:
  for sid,m in ex.map(get,SPECS.items()):print(sid,m.get('http_status'),m.get('retrieval_method'),m.get('raw_sha256'))
