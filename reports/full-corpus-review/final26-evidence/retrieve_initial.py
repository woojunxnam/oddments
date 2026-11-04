import subprocess,json,hashlib,concurrent.futures
from pathlib import Path
from datetime import datetime,timezone
from html.parser import HTMLParser
class TextParser(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,data):self.parts.append(data)
root=Path('/workspace/independent-final26'); out=root/'reports/full-corpus-review/final26-evidence/sources';out.mkdir(parents=True,exist_ok=True)
urls={
'em2026':'https://www.mass.gov/doc/2026-03-action-level-environmental-monitoring-results/download',
'cmr20':'https://www.mass.gov/doc/247-cmr-20-reporting/download',
'defect':'https://www.mass.gov/doc/2024-04-defective-drug-preparations/download',
'fda503b':'https://www.fda.gov/media/90997/download',
'cmr222':'https://www.mass.gov/doc/105-cmr-222-massachusetts-immunization-information-system/download',
'form222':'https://www.ecfr.gov/current/title-21/chapter-II/part-1305/section-1305.13',
'liner':'https://www.ecfr.gov/current/title-21/chapter-II/part-1317/section-1317.60',
'linerinventory':'https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.11',
'nabpsample':'https://nabp.pharmacy/wp-content/uploads/2020/07/MPJE-Sample-Questions.pdf',
'nabpformat':'https://nabp.pharmacy/programs/examinations/mpje/take-the-mpje-exam/',
'nabpcompetency':'https://nabp.pharmacy/programs/examinations/mpje/competency-statements/'
}
def get(item):
 sid,url=item;t=datetime.now(timezone.utc).isoformat();z=subprocess.run(['curl','-L','--max-time','60','-sS','-w','\n%{http_code}\n%{url_effective}\n%{content_type}',url],capture_output=True);raw,status,final,ctype=z.stdout.rsplit(b'\n',3);status=int(status);final=final.decode();ctype=ctype.decode()
 private=sid.startswith('nabp');p=(Path('/tmp')/('final26-'+sid+'.raw')) if private else out/(sid+'.raw');p.write_bytes(raw)
 if raw.startswith(b'%PDF'):
  dest=Path('/tmp')/('final26-'+sid+'.txt') if private else out/(sid+'.txt');z=subprocess.run(['pdftotext','-layout',str(p),str(dest)],capture_output=True);txt=dest.read_text() if dest.exists() else z.stderr.decode()
 else:
  soup=TextParser();soup.feed(raw.decode(errors='replace'));txt='\n'.join(soup.parts);dest=Path('/tmp')/('final26-'+sid+'.txt') if private else out/(sid+'.txt');dest.write_text(txt)
 m=dict(source_id=sid,official_url=url,final_url=final,status=status,content_type=ctype,retrieved_at=t,method='LIVE curl GET inherited proxy TLS verified',raw_sha256=hashlib.sha256(raw).hexdigest(),text_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),public_raw_redistribution=not private)
 if not private:m.update(raw_path=str(p.relative_to(root)),text_path=str(dest.relative_to(root)))
 (out/(sid+'.meta.json')).write_text(json.dumps(m,indent=2)+'\n');return sid,status,len(raw),txt[:120]
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 for z in ex.map(get,urls.items()):print(z)
