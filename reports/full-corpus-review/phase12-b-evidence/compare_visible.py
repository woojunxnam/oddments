"""Retrieval only: original stems/options; no hidden truth or prior audit fields."""
import json,re,math,hashlib
from pathlib import Path
from collections import Counter
BASE=Path(__file__).resolve().parent
packet=json.loads((BASE/'assigned-visible-input.json').read_text());assigned=packet['records']
config=json.load(open('site/practice-expansion/publication.json'))
paths=['practice_expansion/2026-10-23/candidates/questions.json']+[x['path'] for x in config['additional_banks']]
public=[];metadata={};canonical=[]
def visible(q):return {k:q[k] for k in ('question_id','stem','choices')}
for path in paths:
 for q in json.load(open(path))['questions']:
  public.append(visible(q));metadata[q['question_id']]={k:q[k] for k in ['family_id','source_ids'] if k in q}
for path in sorted(Path('data/questions').glob('*.json')):
 obj=json.load(open(path))
 for q in obj if isinstance(obj,list) else [obj]:canonical.append(visible(q))
source_ids={s for r in assigned for s in metadata[r['question_id']].get('source_ids',[])}
sources=json.load(open('notes/guide.json'))['sources']
locators={s:{k:sources[s][k] for k in ['id','title','url'] if k in sources[s]} for s in source_ids}
(BASE/'source-locators.json').write_text(json.dumps(locators,ensure_ascii=False,indent=2)+'\n')
(BASE/'assigned-metadata-whitelist.json').write_text(json.dumps(metadata|{},ensure_ascii=False,indent=2)+'\n') if False else None
(BASE/'assigned-metadata-whitelist.json').write_text(json.dumps({r['question_id']:metadata[r['question_id']] for r in assigned},ensure_ascii=False,indent=2)+'\n')
qs=canonical+public
stop=set('a an the is are of to and or in for with by that this which select one answer all apply statements accurately described cases related requirements proposed interpretation incorrect conclusion correctly addresses case'.split())
def counts(q):
 s=q['stem']+' '+' '.join(c['text'] for c in q['choices']);tok=[t for t in re.findall(r'[a-z0-9]+',s.lower()) if t not in stop]
 return Counter(tok+[' '.join(x) for x in zip(tok,tok[1:])])
cs=[counts(q) for q in qs];df=Counter(t for c in cs for t in c);n=len(qs)
def vector(c):
 v={t:(1+math.log(k))*(math.log((n+1)/(df[t]+1))+1) for t,k in c.items()};norm=math.sqrt(sum(w*w for w in v.values()));return {t:w/norm for t,w in v.items()}
vs=[vector(c) for c in cs]
rows=[];read={}
default_ids=set(json.loads((BASE/'context/default-ids-at-assignment.json').read_text()))
for r in assigned:
 q=r['original_visible_content'];v=vector(counts(q));sim=[sum(w*vs[j].get(t,0) for t,w in v.items()) if q['question_id']!=x['question_id'] else -1 for j,x in enumerate(qs)]
 row={'question_id':q['question_id'],'canonical_nearest':[],'public_nearest':[]}
 for field,indices in [('canonical_nearest',range(len(canonical))),('public_nearest',range(len(canonical),len(qs)))]:
  for j in sorted(indices,key=lambda j:sim[j],reverse=True)[:3]:
   row[field].append({'question_id':qs[j]['question_id'],'cosine':round(sim[j],6)});read[qs[j]['question_id']]=qs[j]
 row['default_nearest']=[]
 for j in sorted([j for j,x in enumerate(qs) if x['question_id'] in default_ids],key=lambda j:sim[j],reverse=True)[:1]:
  row['default_nearest'].append({'question_id':qs[j]['question_id'],'cosine':round(sim[j],6)});read[qs[j]['question_id']]=qs[j]
 rows.append(row)
output={'method':'Word/bigram sublinear TF-IDF cosine over original English stem plus every option; English case/question boilerplate stopwords removed; self ID excluded; retrieval flags only, not semantic verdicts. Top 3 in canonical/public, plus top 1 in assignment default pool; actual visible read separately.','canonical_count':len(canonical),'public_count':len(public),'assignment_default_count':len(default_ids),'rows':rows}
(BASE/'nearest-candidates.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
(BASE/'nearest-visible-input.json').write_text(json.dumps(list(read.values()),ensure_ascii=False,indent=2)+'\n')
print('counts',len(canonical),len(public),'unique visible candidates',len(read));print(json.dumps(locators,ensure_ascii=False,indent=2))
