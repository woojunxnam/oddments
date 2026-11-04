import json,hashlib
from pathlib import Path
import re, math
from collections import Counter
r=Path('/workspace/independent-final26');out=r/'reports/full-corpus-review/final26-evidence';packet=json.loads((out/'assigned-visible-input.json').read_bytes()); config=json.loads((r/'site/practice-expansion/publication.json').read_bytes())
core=['question_id','question_type','stem','choices','correct_choice_ids','explanation']
paths=['practice_expansion/2026-10-23/candidates/questions.json']+[x['path'] for x in config['additional_banks']]
bank=[];families={};inputs={}
for p in paths:
 raw=(r/p).read_bytes();inputs[p]=hashlib.sha256(raw).hexdigest()
 for q in json.loads(raw)['questions']:
  families[q['question_id']]=q.get('family_id');bank.append({k:q[k] for k in core})
canonical=[]
for p in sorted((r/'data/questions').glob('*.json')):
 x=json.loads(p.read_bytes());xs=x if isinstance(x,list) else [x]
 for q in xs:canonical.append({k:q[k] for k in core})
qs=canonical+bank;texts=[q['stem']+'\n'+'\n'.join(c['text'] for c in q['choices']) for q in qs]
def terms(t):
 w=re.findall(r'(?u)\b\w+\b',t.lower());return Counter(w+[' '.join(w[i:i+2]) for i in range(len(w)-1)])
cs=[terms(t) for t in texts];df=Counter(k for c in cs for k in c);idf={k:math.log((1+len(cs))/(1+n))+1 for k,n in df.items() if n>=2}
def vector(c):
 z={k:(1+math.log(n))*idf[k] for k,n in c.items() if k in idf};norm=math.sqrt(sum(x*x for x in z.values()));return {k:x/norm for k,x in z.items()}
m=[vector(c) for c in cs];rows=[];candidates={}
for row in packet['records']:
 q=row['original_visible_content'];t=q['stem']+'\n'+'\n'.join(c['text'] for c in q['choices']);vec=vector(terms(t));scores=[sum(x*z.get(k,0) for k,x in vec.items()) for z in m];groups={}
 for name,a,b in [('canonical439',0,len(canonical)),('public2349',len(canonical),len(qs))]:
  ix=sorted([i for i in range(a,b) if qs[i]['question_id']!=q['question_id']],key=lambda i:(-scores[i],qs[i]['question_id']))[:2]
  groups[name]=[dict(question_id=qs[i]['question_id'],cosine=float(scores[i]),visible_sha256=hashlib.sha256(json.dumps(qs[i],sort_keys=True,ensure_ascii=False).encode()).hexdigest())for i in ix]
  for i in ix:candidates[qs[i]['question_id']]=qs[i]
 rows.append(dict(question_id=q['question_id'],family_id=families[q['question_id']],nearest=groups))
res=dict(method='TF-IDF word/bigram cosine over visible stem and all choices; numeric tokens retained; score is retrieval only',canonical_count=len(canonical),public_count=len(bank),inputs=inputs,records=rows)
(out/'nearest-candidates.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n');(out/'nearest-visible-input.json').write_text(json.dumps(list(candidates.values()),ensure_ascii=False,indent=2)+'\n');print('counts',len(canonical),len(bank),'candidate visible',len(candidates));print(json.dumps(rows,ensure_ascii=False,indent=2))
