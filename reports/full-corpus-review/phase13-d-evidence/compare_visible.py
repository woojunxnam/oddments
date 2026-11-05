import json,pathlib,re,hashlib
BASE=pathlib.Path(__file__).resolve().parent
ROOT=BASE.parents[2]
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def view(q):return {k:q.get(k) for k in ('question_id','question_type','stem','choices')}
def words(q):return set(re.findall(r'[a-z0-9]+',q.get('stem','').lower()+' '+' '.join(c['text'] for c in q['choices'])))
def score(a,b):return len(a&b)/len(a|b)
assigned=json.load(open(BASE/'assigned-visible-input.json'))['records']
canonical=[view(json.load(open(p))) for p in sorted((ROOT/'data/questions').glob('*.json'))]
pubcfg=json.load(open(ROOT/'site/practice-expansion/publication.json'))
paths=['practice_expansion/2026-10-23/candidates/questions.json']+[a['path'] for a in pubcfg['additional_banks']]
public=[view(q) for p in paths for q in json.load(open(ROOT/p))['questions']]
rows=[]
for r in assigned:
 q=r['original_visible_content'];a=words(q);row={'question_id':q['question_id']}
 for label,bank in [('canonical',canonical),('public',public)]:
  candidates=[(score(a,words(b)),b) for b in bank if b['question_id']!=q['question_id']]
  val,b=max(candidates,key=lambda x:x[0]);row[label]={'jaccard_token_score':round(val,6),'visible_sha256':digest(b),'visible':b}
 rows.append(row)
out={'method':'Token Jaccard candidate discovery; semantic verdict requires direct stem/all choices reading','canonical_count':len(canonical),'public_count':len(public),'records':rows}
(BASE/'nearest-visible.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
seen=set()
for r in rows:
 print(r['question_id'],[(k,r[k]['visible']['question_id'],r[k]['jaccard_token_score']) for k in ('canonical','public')])
 for k in ('canonical','public'):
  b=r[k]['visible']
  if b['question_id'] not in seen:print(json.dumps(b,ensure_ascii=False));seen.add(b['question_id'])
