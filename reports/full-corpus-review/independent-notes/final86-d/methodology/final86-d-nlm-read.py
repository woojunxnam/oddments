import json,xml.etree.ElementTree as E,re,sys
from pathlib import Path
b=Path('/workspace/notes-final86-d/reports/full-corpus-review/independent-notes/final86-d');n={'h':'urn:hl7-org:v3'};rows=[]
for p in sorted((b/'sources').glob('*.xml')):
 
 try:rt=E.fromstring(p.read_bytes())
 except E.ParseError:continue
 tid=rt.find('h:setId',n);title=rt.find('h:title',n);eff=rt.find('h:effectiveTime',n);v=rt.find('h:versionNumber',n)
 d={'key':p.stem,'setid':tid.attrib if tid is not None else {},'title':' '.join(title.itertext()) if title is not None else '', 'effective_time':eff.attrib if eff is not None else {},'version':v.attrib if v is not None else {},'sections':[]}
 for sec in rt.findall('.//h:section',n):
  tt=sec.find('h:title',n);tx=sec.find('h:text',n)
  if tt is None or tx is None:continue
  name=' '.join(tt.itertext());content=re.sub(r'\s+',' ',' '.join(tx.itertext())).strip();d['sections'].append({'title':name,'text':content})
 rows.append(d)
(b/'nlm-label-review-data.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
for i,d in enumerate(rows):
 if int(sys.argv[1])<=i<int(sys.argv[2]):
  print('\n',i,d['key'],d['title'],d['effective_time'],d['version'])
  for s in d['sections']:
   if any(w in s['title'].lower() for w in ['description','indications','controlled substance','rems','dosage forms']):print(s['title'],s['text'][:1800])
