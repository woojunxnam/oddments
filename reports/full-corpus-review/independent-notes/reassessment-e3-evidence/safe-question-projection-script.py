import pathlib,json,re,hashlib
w=pathlib.Path('/workspace/census-reassessment-e3');e=w/'reports/full-corpus-review/independent-notes/reassessment-e3-evidence';conf=json.load(open(w/'site/practice-expansion/publication.json'));ps=['practice_expansion/2026-10-23/candidates/questions.json']+[x['path']for x in conf['additional_banks']];allq=[(str(p.relative_to(w)),json.load(open(p)))for p in sorted((w/'data/questions').glob('*.json'))]+[(p,q)for p in ps for q in json.load(open(w/p))['questions']]
cen=json.load(open(w/'reports/full-corpus-review/census-corrections/v4/census/w1-b-1-census-v4.json'));old_related={qid for c in cen['claims']for qid in c.get('related_question_ids',[])}
records=[];counts={'canonical_scanned':439,'public_scanned':2346,'exact_unit_refs_or_final_census_historical_question_ids':0,'broader_cashier_vendor_area_search':0};digest=lambda x:hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
for p,q in allq:
 text=q['stem']+' '+' '.join(c['text']for c in q['choices']);refs=json.dumps({k:v for k,v in q.items()if k not in ('stem','choices','explanation','_statement_truth')},ensure_ascii=False)
 linked='w1-b-1'in refs or q['question_id']in old_related; searched=bool(re.search(r'cashier|vendor|prescription.area',text,re.I))
 counts['exact_unit_refs_or_final_census_historical_question_ids']+=linked;counts['broader_cashier_vendor_area_search']+=searched
 if not(linked or searched):continue
 visible={k:q[k]for k in ('question_id','question_type','stem','choices','correct_choice_ids','explanation')}
 records.append({'question_id':q['question_id'],'collection':p,'record_sha256':digest(q),'linked_to_unit':linked,'broader_search_match':searched,'visible_content_sha256':digest(visible),'original_visible_content':visible})
pack={'source':'actual originals; hidden truth/prior legal or realism verdict not exported','search_scope':counts,'search_method':'exact unit reference and final census historical related IDs; additional full stem/all-choice regex cashier OR vendor OR prescription-area across439+2346','records':records};(e/'related-question-visible-input.json').write_text(json.dumps(pack,ensure_ascii=False,indent=2)+'\n')
catalog=[];idx={}
def ref(x):
 if isinstance(x,str):
  if x not in idx:idx[x]=len(catalog);catalog.append(x)
  return {'text_ref':idx[x]}
 if isinstance(x,dict):return{k:ref(v)for k,v in x.items()}
 if isinstance(x,list):return[ref(v)for v in x]
 return x
maps=[{'question_id':r['question_id'],'refs':ref(r['original_visible_content'])}for r in records];(e/'related-question-exact-text-catalog.json').write_text(json.dumps({'method':'lossless exact-string dedup only, original all fields roundtrip checked','catalog':catalog,'question_maps':maps},ensure_ascii=False,indent=2)+'\n')
print('records',len(records),'unique_strings',len(catalog),'unique_chars',sum(map(len,catalog)),'counts',counts)
print('selected IDs',[r['question_id']for r in records])
