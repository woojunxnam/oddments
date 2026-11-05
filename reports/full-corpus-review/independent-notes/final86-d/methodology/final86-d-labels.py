import json,re
from pathlib import Path
root=Path('/workspace/notes-final86-d');base=root/'reports/full-corpus-review/independent-notes/final86-d';rows=[]
for p in sorted((base/'sources').glob('*.meta.json')):
 m=json.loads(p.read_bytes())
 if m.get('status_code')!=200:continue
 rp=root/m['raw_path']
 if rp.suffix!='.json' or 'api.fda.gov' not in m['official_url']:continue
 data=json.loads(rp.read_bytes());r=data.get('results',[{}])[0];f=r.get('openfda',{})
 out={'key':p.name[:16],'url':m['official_url'],'setid':r.get('set_id'),'effective_time':r.get('effective_time'),'version':r.get('version'),'openfda':f,'sections':{}}
 for k in ['description','indications_and_usage','dosage_and_administration','dosage_forms_and_strengths','clinical_pharmacology','drug_abuse_and_dependence','controlled_substance','active_ingredient','purpose','warnings_and_cautions','boxed_warning']:
  if k in r:out['sections'][k]=' '.join(r[k])
 rows.append(out)
rows.sort(key=lambda x:' '.join(x['openfda'].get('brand_name',[])).lower())
(base/'product-label-review-data.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
for i,r in enumerate(rows):
 if int(__import__('sys').argv[1])<=i<int(__import__('sys').argv[2]):
  print(i,r['key'],'date',r['effective_time'],'v',r['version'],'brands',r['openfda'].get('brand_name'),'generic',r['openfda'].get('generic_name'),'route',r['openfda'].get('route'))
  for k,limit in [('description',650),('indications_and_usage',450),('clinical_pharmacology',350),('controlled_substance',450),('active_ingredient',400),('purpose',200)]:
   if k in r['sections']:print(k+':',r['sections'][k][:limit])
