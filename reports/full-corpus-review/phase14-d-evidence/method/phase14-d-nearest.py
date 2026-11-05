import json,re,math,collections,hashlib
from pathlib import Path
root=Path('/workspace/independent-wave14-d');out=root/'reports/full-corpus-review/phase14-d-evidence';packet=json.load(open(out/'assigned-visible-input.json'))
fields=['question_id','question_type','stem','choices','correct_choice_ids','explanation']
def visible(q):return {k:q[k] for k in fields if k in q}
canonical=[visible(json.load(open(p))) for p in (root/'data/questions').glob('*.json')]
config=json.load(open(root/'site/practice-expansion/publication.json'))
public=[];family={};collectionsmap={}
for path in ['practice_expansion/2026-10-23/candidates/questions.json']+[b['path'] for b in config['additional_banks']]:
 for q in json.load(open(root/path))['questions']:
  public.append(visible(q));family[q['question_id']]=q.get('family_id');collectionsmap[q['question_id']]=path
allq=canonical+public
def tok(q):return re.findall(r'[a-z0-9]+',(q.get('stem','')+' '+' '.join(c['text'] for c in q['choices'])).lower())
df=collections.Counter()
for q in allq:df.update(set(tok(q)))
idf={t:math.log((1+len(allq))/(1+n))+1 for t,n in df.items()}
def vec(q):
 v={t:n*idf[t] for t,n in collections.Counter(tok(q)).items()}; norm=math.sqrt(sum(n*n for n in v.values()));return {t:n/norm for t,n in v.items()}
vs={q['question_id']:vec(q) for q in allq}
rows=[];selected={}
for r in packet['records']:
 q=r['original_visible_content'];v=vs[q['question_id']];row={'question_id':q['question_id'],'family_id':family[q['question_id']],'collection':collectionsmap[q['question_id']]}
 for label,bank in [('canonical',canonical),('public',public)]:
  scores=[]
  for other in bank:
   if other['question_id']==q['question_id']:continue
   w=vs[other['question_id']];score=sum(a*w.get(t,0) for t,a in v.items());scores.append((score,other))
  best=sorted(scores,key=lambda x:(-x[0],x[1]['question_id']))[:2]
  row[label+'_nearest']=[{'question_id':o['question_id'],'cosine_similarity':round(s,6)} for s,o in best]
  for s,o in best:selected[o['question_id']]=o
 rows.append(row)
payload=dict(method='TF-IDF word cosine on current stem and all choice texts, exclusion of same ID; lexical scores only for candidate discovery',canonical_count=len(canonical),public_count=len(public),records=rows,compared_visible_originals=list(selected.values()),prohibited_fields_excluded=True)
(out/'nearest-visible-comparison.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
print('counts',len(canonical),len(public),'unique nearest',len(selected))
for r in rows:print(r['question_id'],r['family_id'],r['canonical_nearest'],r['public_nearest'])
