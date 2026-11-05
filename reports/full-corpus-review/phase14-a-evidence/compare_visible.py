"""Project visible content only, then nominate nearest neighbors for actual reading."""
from pathlib import Path
import json, math, re, collections, hashlib
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
FIELDS=('question_id','question_type','stem','choices','correct_choice_ids','explanation')
def visible(q):return {k:q[k] for k in FIELDS if k in q}
def sha(b):return hashlib.sha256(b).hexdigest()
def tok(q):return collections.Counter(re.findall(r'[a-z0-9]+',(q['stem']+' '+ ' '.join(c['text'] for c in q['choices'])).lower()))
def run():
 assigned=json.loads((OUT/'assigned-visible-input.json').read_bytes())['records']
 canonical=[dict(collection='canonical439',path=str(p.relative_to(ROOT)),content=visible(json.loads(p.read_bytes()))) for p in sorted((ROOT/'data/questions').glob('*.json'))]
 config=json.loads((ROOT/'site/practice-expansion/publication.json').read_bytes())
 paths=['practice_expansion/2026-10-23/candidates/questions.json']+[b['path'] for b in config['additional_banks']]
 public=[dict(collection='public2349',path=p,content=visible(q)) for p in paths for q in json.loads((ROOT/p).read_bytes())['questions']]
 assert len(canonical)==439 and len(public)==2349
 corpus=canonical+public;counts=[tok(v['content']) for v in corpus];df=collections.Counter()
 for c in counts:df.update(c.keys())
 idf={t:math.log((1+len(corpus))/(1+n))+1 for t,n in df.items()}
 def vector(c):
  d={t:(1+math.log(n))*idf.get(t,math.log(len(corpus)+1)) for t,n in c.items()};norm=math.sqrt(sum(x*x for x in d.values()));return {t:x/norm for t,x in d.items()}
 vectors=[vector(c) for c in counts];rows=[];read={}
 for a in assigned:
  q=a['original_visible_content'];v=vector(tok(q));scores=[sum(w*o.get(t,0) for t,w in v.items()) for o in vectors]
  row={'question_id':q['question_id'],'method':'TF-IDF unigram cosine stem+all choices; scores nominate only; human/model semantic comparison separate','neighbors':[]}
  for label,indices in [('canonical439',range(439)),('public2349',range(439,len(corpus)))]:
   top=sorted((i for i in indices if corpus[i]['content']['question_id']!=q['question_id']),key=lambda i:scores[i],reverse=True)[:2]
   for i in top:
    c=corpus[i];key=c['collection']+':'+c['content']['question_id'];read[key]=c
    row['neighbors'].append({'collection':label,'question_id':c['content']['question_id'],'score':round(scores[i],8),'visible_sha256':sha(json.dumps(c['content'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()),'path':c['path']})
  rows.append(row)
 (OUT/'nearest-candidates.json').write_text(json.dumps({'canonical_count':439,'public_count':2349,'results':rows},ensure_ascii=False,indent=2)+'\n')
 (OUT/'nearest-visible-read-packet.json').write_text(json.dumps(list(read.values()),ensure_ascii=False,indent=2)+'\n')
 print('Measured',len(rows),'items; unique projected nearest candidates',len(read))
 for row in rows:print(row['question_id'],' '.join(n['collection']+':'+n['question_id']+'='+str(n['score']) for n in row['neighbors']))
if __name__=='__main__':run()
