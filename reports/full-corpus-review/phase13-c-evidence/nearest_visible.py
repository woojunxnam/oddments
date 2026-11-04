import json,re,math,collections,hashlib
from pathlib import Path
E=Path(__file__).resolve().parent;R=E.parents[2];p=json.loads((E/'assigned-visible-input.json').read_text());cfg=json.loads((R/'site/practice-expansion/publication.json').read_text())
def visible(q):return {k:q.get(k) for k in ['question_id','stem','choices']}
c=[visible(json.loads(f.read_text())) for f in sorted((R/'data/questions').glob('ma-q-*.json'))]
paths=['practice_expansion/2026-10-23/candidates/questions.json']+[a['path'] for a in cfg['additional_banks']]
b=[visible(q) for path in paths for q in json.loads((R/path).read_text())['questions']]
def words(q):return collections.Counter(re.findall('[a-z]{3,}',q['stem'].lower()+' '+' '.join(x['text'].lower() for x in q['choices'])))
allq=c+b;df=collections.Counter(t for q in allq for t in words(q));n=len(allq)
def vec(q):return {t:v*(1+math.log((n+1)/(df[t]+1))) for t,v in words(q).items()}
def sim(a,b):return sum(v*b.get(t,0) for t,v in a.items())/(sum(v*v for v in a.values())*sum(v*v for v in b.values()))**.5
cv=[(q,vec(q)) for q in c];bv=[(q,vec(q)) for q in b];out=[]
for r in p['records']:
 q=r['original_visible_content'];v=vec(q);row={'question_id':q['question_id']}
 for label,pool in [('canonical',cv),('public',bv)]:
  near=sorted([(sim(v,vv),qq) for qq,vv in pool if qq['question_id']!=q['question_id']],key=lambda x:x[0],reverse=True)[:1]
  row[label]=[dict(score=sc,visible=qq) for sc,qq in near]
 out.append(row)
(E/'nearest-visible.json').write_text(json.dumps(dict(method='IDF weighted term cosine; stem and all choices only; candidate discovery not semantic verdict',canonical_count=len(c),public_count=len(b),records=out),ensure_ascii=False,indent=2)+'\n')
for row in out:print(row['question_id'],[(k,row[k][0]['visible']['question_id'],round(row[k][0]['score'],3)) for k in ['canonical','public']])
