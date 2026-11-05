from pathlib import Path
exec(Path('/tmp/notes120_b_fetch.py').read_text().split('with concurrent.futures.ThreadPoolExecutor')[0])
(S/'conduct-failed-attempt.meta.json').write_bytes((S/'conduct.meta.json').read_bytes())
urls={'conduct':'https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download','opillorder':'https://www.mass.gov/doc/oral-contraceptive-standing-order-0/download','oralprep':'https://www.mass.gov/doc/pharmacist-oral-prep-guidelines-8-2026/download','pep':'https://www.mass.gov/doc/pharmacist-pep-guidelines-9-2026/download','sti':'https://www.mass.gov/doc/pharmacist-guidance-for-sti-tx-8-2026/download','doxypep':'https://www.mass.gov/doc/pharmacist-guidance-doxypep-8-2026/download'}
import zipfile,io,xml.etree.ElementTree as ET
for k,url in urls.items():
 result=fetch(k,url)
 m=json.loads((S/(k+'.meta.json')).read_bytes())
 if m.get('raw_path') and Path(m['raw_path']).read_bytes().startswith(b'PK'):
  old=Path(m['raw_path']);rp=old.with_suffix('.docx');old.rename(rp);raw=rp.read_bytes();z=zipfile.ZipFile(io.BytesIO(raw));root=ET.fromstring(z.read('word/document.xml'));text='\n'.join(''.join(p.itertext()) for p in root.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'))+'\n';tp=Path(m['text_path']);tp.write_text(text);m.update(raw_path=str(rp),text_sha256=hashlib.sha256(tp.read_bytes()).hexdigest(),text_extraction='DOCX word/document.xml paragraphs; tables retained in document order');(S/(k+'.meta.json')).write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
 print(result)
