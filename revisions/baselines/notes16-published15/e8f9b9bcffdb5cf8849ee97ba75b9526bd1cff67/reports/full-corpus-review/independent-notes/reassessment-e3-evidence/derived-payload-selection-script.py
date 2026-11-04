import json,pathlib,hashlib,datetime,subprocess
root=pathlib.Path('/workspace/oddments');e=pathlib.Path('/workspace/census-reassessment-e3/reports/full-corpus-review/independent-notes/reassessment-e3-evidence');out=[]
for fn in ['site/notes/study-data.js','site/notes/refresh-data.js']:
 p=root/fn;s=p.read_text();d=json.loads(s[s.index('{'):].rstrip().removesuffix(';'));selected=[]
 for k in ['lessons','comparisons','clocks','cards']:
  for i,x in enumerate(d.get(k,[])):
   if 'w1-b-1'in x.get('note_units',[]):selected.append({'json_pointer':'/'+k+'/'+str(i),'payload':x})
 mids={x['payload'].get('module_id')for x in selected};lids={x['payload'].get('id')for x in selected};modules=[x for x in d.get('modules',[])if x.get('id')in mids or any(i in json.dumps(x,ensure_ascii=False)for i in lids if i)]
 o={'source_path':fn,'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'read_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'controller_head':subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip(),'selection_method':'actual exact note_units and associated module/lesson link','records':selected,'associated_modules':modules};out.append(o);print(fn,json.dumps({'records':selected,'associated_modules':modules},ensure_ascii=False,indent=2))
(e/'actual-current-derived-payloads.json').write_text(json.dumps({'sources':out,'scope':'Actual current committed repository payloads read; remote deployment HTTP not checked. Past independent metadata is display context and never controlling legal evidence.'},ensure_ascii=False,indent=2)+'\n')
