import json,pathlib,hashlib,numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
w=pathlib.Path('/workspace/independent-sata-remediation-e');e=w/'reports/full-corpus-review/substantive-remediation-independent-e/evidence';ds=json.load(open('/tmp/sata-remediation-independent-e-visible.json'));config=json.load(open(w/'site/practice-expansion/publication.json'));paths=['practice_expansion/2026-10-23/candidates/questions.json']+[a['path']for a in config['additional_banks']];qs=[('canonical',json.load(open(p)))for p in sorted((w/'data/questions').glob('*.json'))]+[('public',q)for p in paths for q in json.load(open(w/p))['questions']];assert len(qs)==2785
text=lambda x:x['stem']+' '+' '.join(c['text']for c in x['choices']);vec=TfidfVectorizer(stop_words='english',ngram_range=(1,2),sublinear_tf=True);mat=vec.fit_transform([text(q)for _,q in qs]+[text(q)for q in ds]);scores=cosine_similarity(mat[-3:],mat[:-3]);results=[];selected={};digest=lambda x:hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
for k,d in enumerate(ds):
 found=[]
 for collection,n in [('canonical',3),('public',5)]:
  ix=[i for i,(c,q)in enumerate(qs)if c==collection];rank=sorted(ix,key=lambda i:scores[k,i],reverse=True)[:n]
  # Include the immutable original target as comparator even if lexical rank differs.
  anchor=[i for i,(c,q)in enumerate(qs)if c==collection and q['question_id']==d['original_question_id']]
  for i in rank+anchor:
   c,q=qs[i];qid=q['question_id']
   if qid not in [x['question_id']for x in found]:found.append({'question_id':qid,'collection':c,'similarity':float(scores[k,i]),'original_anchor':qid==d['original_question_id']})
   selected[qid]={'question_id':qid,'collection':c,'record_sha256':digest(q),'stem':q['stem'],'choices':q['choices']}
 results.append({'draft_key':d['draft_key'],'nearest':found})
o={'method':'TF-IDF English unigram/bigram with stop-word removal and sublinearTF over every complete stem+allchoices in439canonical+2346public. Read top3canonical/top5public plus immutable target anchor. No author duplicate decisions or hidden truth/keys/audits in visible comparator projection.','corpus':{'canonical':439,'public':2346},'comparisons':results,'selected_original_comparators':list(selected.values())};(e/'nearest-original-comparison-input.json').write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'comparisons':results,'unique_nearest_originals':len(selected)},ensure_ascii=False,indent=2))
cat=[];idx={}
def ref(v):
 if isinstance(v,str):
  if v not in idx:idx[v]=len(cat);cat.append(v)
  return {'text_ref':idx[v]}
 if isinstance(v,dict):return{k:ref(z)for k,z in v.items()}
 if isinstance(v,list):return[ref(z)for z in v]
 return v
maps=[{'question_id':q['question_id'],'refs':ref({k:q[k]for k in ['question_id','stem','choices']})}for q in selected.values()];(e/'nearest-exact-text-catalog.json').write_text(json.dumps({'catalog':cat,'question_maps':maps,'method':'Lossless exact-string dedup only'},ensure_ascii=False,indent=2)+'\n');print('strings',len(cat),'chars',sum(map(len,cat)))
