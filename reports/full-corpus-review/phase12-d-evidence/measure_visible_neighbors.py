"""TF-IDF retrieval over current visible text; scores do not decide semantic duplication."""
import json,re,math,hashlib
from collections import Counter
from pathlib import Path
B=Path(__file__).resolve().parent
packet=json.load(open(B/'assigned-visible-input.json'));assignment=json.load(open(B/'assignment.json'));config=json.load(open('site/practice-expansion/publication.json'))
public=[];canonical=[]
for p in ['practice_expansion/2026-10-23/candidates/questions.json']+[a['path'] for a in config['additional_banks']]:
 for q in json.load(open(p))['questions']:public.append({k:q[k] for k in ('question_id','family_id','stem','choices')})
for p in sorted(Path('data/questions').glob('*.json')):
 d=json.load(open(p))
 for q in d if isinstance(d,list) else [d]:canonical.append({k:q[k] for k in ('question_id','family_id','stem','choices')})
allqs=canonical+public
def tokens(q):
 words=re.findall(r'\b\w+\b',(q['stem']+'\n'+'\n'.join(c['text'] for c in q['choices'])).lower());return words+[' '.join(x) for x in zip(words,words[1:])]
cts=[Counter(tokens(q)) for q in allqs];df=Counter()
for ct in cts:df.update(ct.keys())
idf={t:math.log((1+len(allqs))/(1+n))+1 for t,n in df.items()}
def vector(ct):
 v={t:(1+math.log(n))*idf[t] for t,n in ct.items() if t in idf};norm=math.sqrt(sum(x*x for x in v.values()));return {t:x/norm for t,x in v.items()} if norm else {}
vec=[vector(c) for c in cts];rows=[];unique={}
for r in packet['records']:
 q=r['original_visible_content'];a=vector(Counter(tokens(q)));scores=[sum(w*v.get(t,0) for t,w in a.items()) for v in vec];groups={}
 for label,lo,hi in [('canonical',0,len(canonical)),('public',len(canonical),len(allqs))]:
  ix=sorted((i for i in range(lo,hi) if allqs[i]['question_id']!=q['question_id']),key=lambda i:scores[i],reverse=True)
  selected=ix[:2];family=next((x['family_id'] for x in public if x['question_id']==q['question_id']),None)
  other=next((i for i in ix if allqs[i]['family_id']!=family),None)
  if other is not None and other not in selected:selected.append(other)
  groups[label]=[{'question_id':allqs[i]['question_id'],'cosine':round(scores[i],6),'same_declared_family':allqs[i]['family_id']==family,'visible_candidate_sha256':hashlib.sha256(json.dumps(allqs[i],sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()} for i in selected]
  for i in selected:unique[allqs[i]['question_id']]=allqs[i]
 rows.append({'question_id':q['question_id'],'nearest':groups})
result={'method':'Word and adjacent bigram TF-IDF with sublinear term frequency, smoothed IDF and L2 normalization over current canonical/public visible stem+all options; self excluded; top two plus nearest different family. Scores are retrieval only, not a semantic verdict.','canonical_count':len(canonical),'public_count':len(public),'rows':rows,'unique_candidates':list(unique.values())}
(B/'nearest-visible-candidates.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('counts',len(canonical),len(public),'unique candidates',len(unique))
for q in unique.values():print(json.dumps(q,ensure_ascii=False))
