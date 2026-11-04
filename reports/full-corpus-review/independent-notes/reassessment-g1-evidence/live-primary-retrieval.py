import concurrent.futures,datetime,hashlib,json,pathlib,subprocess,urllib.request
ROOT=pathlib.Path('/workspace/census-reassessment-g1');OUT=ROOT/'reports/full-corpus-review/independent-notes/reassessment-g1-evidence';OUT.mkdir(parents=True,exist_ok=True)
SPECS={
'practice':'https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download',
'license':'https://www.mass.gov/doc/247-cmr-6-licensure-of-pharmacies/download',
'reporting':'https://www.mass.gov/doc/247-cmr-20-reporting/download',
'interim':'https://www.mass.gov/doc/2022-02-extended-absence-or-departure-of-a-manager-of-record-or-designated-pharmacist-in-charge-pdf/download',
'ma700':'https://www.mass.gov/doc/105-cmr-700-implementation-of-mgl-c94c-0/download',
'1304-11':'https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.11',
'1304-04':'https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.04',
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
