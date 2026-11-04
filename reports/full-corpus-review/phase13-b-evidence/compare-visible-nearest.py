from pathlib import Path
import json,re,hashlib,difflib
root=Path('/workspace/independent-wave13-b');ev=root/'reports/full-corpus-review/phase13-b-evidence'
p=json.loads((ev/'assigned-visible-input.json').read_bytes());assigned={r['question_id']:r for r in p['records']}
def visible(q):return {k:q.get(k) for k in ('question_id','family_id','question_type','stem','choices')}
def words(q):return set(re.findall(r'[a-z0-9]+',(q.get('stem','')+' '+' '.join(str(c.get('text','')) for c in q.get('choices',[]))).lower()))
can=[visible(json.loads(f.read_bytes())) for f in (root/'data/questions').glob('*.json')]
conf=json.loads((root/'site/practice-expansion/publication.json').read_bytes());paths=['practice_expansion/2026-10-23/candidates/questions.json']+[a['path'] for a in conf['additional_banks']]
pub=[];context={}
for path in paths:
 for q in json.loads((root/path).read_bytes())['questions']:
  pub.append(visible(q))
  if q['question_id'] in assigned:context[q['question_id']]={k:q.get(k) for k in ['family_id','topic','area','source_ids','note_evidence']}
selection=json.loads((root/'practice_expansion/2026-10-28-representative/selection.json').read_bytes());defaults=set(selection['recommended_ids'])
rows=[];selected={}
for qid,r in assigned.items():
 q=r['original_visible_content'];w=words(q);row={'question_id':qid,'public_default':qid in defaults,'source_context':context[qid]}
 for label,pool in [('canonical',can),('public',pub)]:
  scored=sorted(((len(w&words(x))/max(1,len(w|words(x))),x) for x in pool if x['question_id']!=qid),key=lambda x:x[0],reverse=True)[:3]
  row[label+'_nearest']=[{'question_id':x['question_id'],'token_jaccard':round(s,6),'public_default':x['question_id'] in defaults} for s,x in scored]
  for _,x in scored[:1]:selected[x['question_id']]=x
 rows.append(row)
out={'method':'lowercase stem+all choices word-set Jaccard; top3 candidates per pool; no semantic verdict from score','canonical_count':len(can),'public_count':len(pub),'records':rows,'nearest_visible_records':list(selected.values())}
(ev/'nearest-visible-comparison.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Counts',len(can),len(pub),'selected',len(selected))
for x in selected.values():print(json.dumps(x,ensure_ascii=False))
print('contexts',json.dumps(context,ensure_ascii=False))
