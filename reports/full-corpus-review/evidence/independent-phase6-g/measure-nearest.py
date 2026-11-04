import hashlib,json,pathlib,sys
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
ROOT=pathlib.Path('/workspace/independent-phase6-g')
OUT=ROOT/'reports/full-corpus-review/evidence/independent-phase6-g'
packet=json.load(open('/tmp/independent-phase6-g-visible.json'))
assigned={r['question_id']:r['original_visible_content'] for r in packet['records']}
def safe(q):
 return {k:q.get(k) for k in ['question_id','family_id','question_type','stem','choices']}
canonical=[safe(json.load(open(p))) for p in sorted((ROOT/'data/questions').glob('*.json'))]
cfg=json.load(open(ROOT/'site/practice-expansion/publication.json'))
paths=['practice_expansion/2026-10-23/candidates/questions.json']+[x['path'] for x in cfg['additional_banks']]
public=[];family={};fullhash={}
for path in paths:
 for q in json.load(open(ROOT/path))['questions']:
  public.append(safe(q));family[q['question_id']]=q.get('family_id')
  if q['question_id'] in assigned:
   fullhash[q['question_id']]=hashlib.sha256(json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def text(q):return q['stem']+'\n'+'\n'.join(c['text'] for c in q['choices'])
allrows=canonical+public+list(assigned.values())
v=TfidfVectorizer(ngram_range=(1,2),lowercase=True,sublinear_tf=True)
mat=v.fit_transform([text(q) for q in allrows]);scores=(mat[-40:]@mat[:len(canonical)+len(public)].T).toarray()
comparisons=[];display={}
for i,(qid,q) in enumerate(assigned.items()):
 assert fullhash[qid]==packet['question_hashes'][qid]
 def nearest(start,end,other_family=False):
  for j in sorted(range(start,end),key=lambda j:(-scores[i,j],allrows[j]['question_id'])):
   c=allrows[j]
   if c['question_id']==qid:continue
   if other_family and c.get('family_id')==family.get(qid):continue
   display[c['question_id']]=c
   return {'question_id':c['question_id'],'family_id':c.get('family_id'),'cosine':round(float(scores[i,j]),6),'full_stem_and_all_options':c}
 comparisons.append({'question_id':qid,'family_id':family[qid],'canonical_nearest':nearest(0,len(canonical)),'public_nearest':nearest(len(canonical),len(canonical)+len(public)),'public_nearest_other_family':nearest(len(canonical),len(canonical)+len(public),True)})
out={'method':'TF-IDF word unigrams+bigrams, sublinear_tf; cosine over complete stem and every option; self excluded; scores only select candidates and do not determine semantic verdict','canonical_count':len(canonical),'public_count':len(public),'read_date':'2026-11-04','corpus_files':[{ 'path':p,'raw_sha256':hashlib.sha256((ROOT/p).read_bytes()).hexdigest()} for p in paths], 'comparisons':comparisons}
(OUT/'nearest-comparisons.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
(OUT/'assigned-family-map.json').write_text(json.dumps(family and {k:family[k] for k in assigned},indent=2)+'\n')
print('corpus',len(canonical),len(public),'unique nearest',len(display))
(OUT/'nearest-display.json').write_text(json.dumps(list(display.values()),ensure_ascii=False,indent=2)+'\n')
print('OUTPUT',OUT/'nearest-comparisons.json')
