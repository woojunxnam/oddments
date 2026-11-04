import json,pathlib,re,math,collections,hashlib
root=pathlib.Path(__file__).resolve().parents[3]; out=root/'reports/full-corpus-review/phase12-c-evidence'
packet=json.loads((out/'assigned-visible-input.json').read_text()); ids=set(packet['question_hashes'])
paths=['practice_expansion/2026-10-23/candidates/questions.json']+[b['path'] for b in json.loads((root/'site/practice-expansion/publication.json').read_text())['additional_banks']]
def visible(q): return {k:q.get(k) for k in ['question_id','family_id','stem','choices']}
public=[]; loc={}
for path in paths:
 for q in json.loads((root/path).read_text())['questions']:
  public.append(visible(q))
  if q['question_id'] in ids: loc[q['question_id']]={k:q.get(k) for k in ['question_id','family_id','source_ids']}
canonical=[]
for path in sorted((root/'data/questions').glob('*.json')):
 v=json.loads(path.read_text())
 for q in v if isinstance(v,list) else [v]:canonical.append(visible(q))
allq=canonical+public
text=lambda q:q['stem']+' '+' '.join(c['text'] for c in q['choices'])
def tokens(q):
 t=re.findall(r'\b\w+\b',text(q).lower());return t+[' '.join(x) for x in zip(t,t[1:])]
raw=[collections.Counter(tokens(q)) for q in allq];df=collections.Counter(k for r in raw for k in r)
vs=[]
for r in raw:
 v={k:(1+math.log(n))*math.log((1+len(raw))/(1+df[k])) for k,n in r.items()}; norm=math.sqrt(sum(n*n for n in v.values()));vs.append({k:n/norm for k,n in v.items()})
def score(i,j):return sum(n*vs[j].get(k,0) for k,n in vs[i].items())
index={q['question_id']:i for i,q in enumerate(allq)};results=[];candidates={}
for qid in sorted(ids):
 i=index[qid];family=allq[i]['family_id']; categories={'canonical':range(len(canonical)),'public':range(len(canonical),len(allq)),'public_different_family':[j for j in range(len(canonical),len(allq)) if allq[j]['family_id']!=family]}; rec={'question_id':qid,'family_id':family}
 for kind,positions in categories.items():
  top=sorted(((score(i,j),j) for j in positions if j!=i),reverse=True)[:1]
  rec[kind]=[dict(question_id=allq[j]['question_id'],cosine=round(s,6),same_family=allq[j]['family_id']==family) for s,j in top]
  for s,j in top:candidates[allq[j]['question_id']]=allq[j]
 results.append(rec)
default=set(json.loads((out/'context/default-ids-at-assignment.json').read_text()))
data=dict(method='word unigram+bigram TF-IDF cosine; sublinear TF; one vocabulary; algorithm only retrieves candidates',canonical_count=len(canonical),public_count=len(public),assigned_default_ids=sorted(ids&default),nearest=sorted(results,key=lambda x:x['question_id']),visible_candidates=sorted(candidates.values(),key=lambda q:q['question_id']),input_sha256={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths},canonical_source_files=439,canonical_input_manifest_sha256=hashlib.sha256(''.join(str(p.relative_to(root))+':'+hashlib.sha256(p.read_bytes()).hexdigest()+'\n' for p in sorted((root/'data/questions').glob('*.json'))).encode()).hexdigest())
(out/'nearest-visible.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');(out/'locator-metadata.json').write_text(json.dumps(loc,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in data.items() if k not in ['visible_candidates','nearest']},ensure_ascii=False));print('unique candidates',len(candidates))

