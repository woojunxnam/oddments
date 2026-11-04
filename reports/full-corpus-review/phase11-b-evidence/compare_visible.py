import json,pathlib,re,hashlib
from collections import Counter
BASE=pathlib.Path(__file__).resolve().parent;ROOT=BASE.parents[2]
def digest(q):return hashlib.sha256(json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def visible(q):
 return {k:q[k] for k in ('question_id','question_type','stem','choices','correct_choice_ids') if k in q}
def tokens(q):return Counter(re.findall(r'[a-z0-9]+',(q['stem']+' '+' '.join(c['text'] for c in q['choices'])).lower()))
def sim(a,b):return sum((a&b).values())/sum((a|b).values())
p=json.load(open(BASE/'assigned-visible-input.json'));assigned=[x['original_visible_content'] for x in p['records']]
canonical=[visible(json.load(open(x))) for x in (ROOT/'data/questions').glob('*.json')]
config=json.load(open(ROOT/'site/practice-expansion/publication.json'))
paths=['practice_expansion/2026-10-23/candidates/questions.json']+[x['path'] for x in config['additional_banks']]
public=[visible(q) for path in paths for q in json.load(open(ROOT/path))['questions']]
defaults=json.load(open(BASE/'context/default-ids-at-assignment.json'))['recommended_ids']
records=[];candidates={}
for q in assigned:
 row={'question_id':q['question_id']}
 for typ,pool in [('canonical',canonical),('public',public)]:
  scored=sorted([(sim(tokens(q),tokens(other)),other) for other in pool if other['question_id']!=q['question_id']],key=lambda x:(-x[0],x[1]['question_id']))
  score,other=scored[0];candidates[other['question_id']]=other
  row[typ+'_closest']={'question_id':other['question_id'],'visible_sha256':digest(other),'discovery_similarity':score,'default_at_assignment':other['question_id'] in defaults,'visible_input_path':'duplicate-visible-candidates.json'}
 records.append(row)
out={'scope':'Similarity is discovery only. Human semantic comparison required; only question-visible whitelist exported.','canonical_count':len(canonical),'public_count':len(public),'records':records}
(BASE/'duplicate-discovery.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(BASE/'duplicate-visible-candidates.json').write_text(json.dumps({'scope':'Visible whitelist only; no hidden truth or prior audit','questions':list(candidates.values())},ensure_ascii=False,indent=2)+'\n')
print('candidates',len(candidates),'canonical',len(canonical),'public',len(public))
for q in candidates.values():print(json.dumps(q,ensure_ascii=False))
