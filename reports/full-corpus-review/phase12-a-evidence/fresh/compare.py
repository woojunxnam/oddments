import pathlib,json,re,hashlib,collections,math
R=pathlib.Path('.');D=pathlib.Path(__file__).resolve().parent.relative_to(pathlib.Path.cwd().resolve())
p=json.load(open(D.parent/'assigned-visible-input.json')); conf=json.load(open('site/practice-expansion/publication.json'))
canonical=[]
for f in sorted(pathlib.Path('data/questions').glob('*.json')):
 q=json.load(open(f));canonical.append({k:q[k] for k in ('question_id','stem','choices')})
public=[];locators={}
for f in ['practice_expansion/2026-10-23/candidates/questions.json']+[b['path'] for b in conf['additional_banks']]:
 b=json.load(open(f))
 for q in b['questions']:
  public.append({k:q[k] for k in ('question_id','stem','choices')})
  if q['question_id'] in p['question_hashes']:locators[q['question_id']]={k:q.get(k) for k in ('family_id','source_ids')}
def tok(q):return collections.Counter(re.findall(r'[a-z0-9]+',q['stem'].lower()+' '+' '.join(c['text'] for c in q['choices'])))
allq=canonical+public;N=len(allq);df=collections.Counter(t for q in allq for t in tok(q));idf={t:math.log((N+1)/(n+1))+1 for t,n in df.items()}
def vec(q):
 v={t:n*idf[t] for t,n in tok(q).items()};norm=math.sqrt(sum(n*n for n in v.values()));return {t:n/norm for t,n in v.items()}
vs={q['question_id']:vec(q) for q in allq}
def score(v,w):return sum(n*w.get(t,0) for t,n in v.items())
comparisons=[];read={}
for r in p['records']:
 q=r['original_visible_content'];v=vs[q['question_id']];row={'question_id':q['question_id']}
 for name,pool in [('canonical',canonical),('public',public)]:
  nearest=sorted([(score(v,vs[x['question_id']]),x) for x in pool if x['question_id']!=q['question_id']],key=lambda x:x[0],reverse=True)[:3]
  row[name]=[{'question_id':x['question_id'],'cosine_tfidf_visible_stem_and_choices':s} for s,x in nearest]
  for s,x in nearest:read[x['question_id']]=x
 comparisons.append(row)
(D/'nearest-comparisons.json').write_text(json.dumps({'method':'TF-IDF cosine English lowercase alphanumeric stem and all choices; self excluded; top3 per pool; score is candidate ranking only','canonical_count':len(canonical),'public_count':len(public),'records':comparisons},indent=2)+'\n')
(D/'nearest-visible-input.json').write_text(json.dumps({'scope':'visible stem and all choices only; no keys, author truths, or audit metadata','records':list(read.values())},ensure_ascii=False,indent=2)+'\n')
(D/'locator-whitelist.json').write_text(json.dumps(locators,ensure_ascii=False,indent=2)+'\n')
print('canonical',len(canonical),'public',len(public),'nearest_unique',len(read))
for r in comparisons:print(r['question_id'],r['canonical'][0],r['public'][0])
