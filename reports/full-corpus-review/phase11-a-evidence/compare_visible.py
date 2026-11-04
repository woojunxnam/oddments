import collections, hashlib, json, math, pathlib, re, sys
ROOT=pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
from export_legacy_review_input import CORE_FIELDS, digest
E=pathlib.Path(__file__).resolve().parent
assigned=json.loads((E/'assigned-visible-input.json').read_bytes())
defaults=set(json.loads((E/'context/default-ids-at-assignment.json').read_bytes())['recommended_ids'])
def visible(q):return {k:q[k] for k in CORE_FIELDS if k in q}
def words(q):return re.findall(r'[a-z0-9]+',(q['stem']+' '+' '.join(c['text'] for c in q['choices'])).lower())
canonical={};expansion={}
for file in (ROOT/'data/questions').glob('*.json'):
 q=json.loads(file.read_bytes());canonical[q['question_id']]=visible(q)
config=json.loads((ROOT/'site/practice-expansion/publication.json').read_bytes())
paths=['practice_expansion/2026-10-23/candidates/questions.json']+[x['path'] for x in config['additional_banks']]
for path in paths:
 for q in json.loads((ROOT/path).read_bytes())['questions']:expansion[q['question_id']]=visible(q)
allq={**canonical,**expansion}
df=collections.Counter(w for q in allq.values() for w in set(words(q)))
def vector(q):
 c=collections.Counter(words(q));v={w:n*(1+math.log(len(allq)/(1+df[w]))) for w,n in c.items()};norm=math.sqrt(sum(x*x for x in v.values()));return {w:n/norm for w,n in v.items()}
vec={i:vector(q) for i,q in allq.items()}
def sim(a,b):return sum(v*vec[b].get(w,0) for w,v in vec[a].items())
rows=[];selected={}
for r in assigned['records']:
 qid=r['question_id'];row={'question_id':qid}
 for label,pool in [('canonical',canonical),('public_default',{i:expansion[i] for i in defaults if i in expansion}),('public_other',expansion)]:
  candidates=sorted(((sim(qid,i),i) for i in pool if i!=qid),reverse=True)[:1]
  row[label]=[{'question_id':i,'search_cosine':s,'visible_content_sha256':digest(allq[i])} for s,i in candidates]
  for _,i in candidates:selected[i]=allq[i]
 rows.append(row)
out={'method':'TF-IDF cosine of visible stem plus every choice; search aid only, independent manual semantic review required','canonical_count':len(canonical),'public_count':len(expansion),'public_default_count':len(defaults),'matches':rows,'visible_candidates':selected}
(E/'nearest-visible-comparison-input.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'canonical_count':len(canonical),'public_count':len(expansion),'selected_unique':len(selected),'matches':rows},ensure_ascii=False))
