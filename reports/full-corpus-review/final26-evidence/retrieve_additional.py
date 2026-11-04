import subprocess,json,hashlib,concurrent.futures
from pathlib import Path
from datetime import datetime,timezone
from html.parser import HTMLParser
class TextParser(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,data):self.parts.append(data)
root=Path('/workspace/independent-final26'); out=root/'reports/full-corpus-review/final26-evidence/sources';out.mkdir(parents=True,exist_ok=True)
urls={
'mgl39d':'https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section39D',
'cfr310':'https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-310/subpart-D/section-310.305',
'collector':'https://www.ecfr.gov/current/title-21/chapter-II/part-1317/section-1317.75',
'fda503bpage':'https://www.fda.gov/regulatory-information/search-fda-guidance-documents/adverse-event-reporting-outsourcing-facilities-under-section-503b-federal-food-drug-and-cosmetic-act'
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
