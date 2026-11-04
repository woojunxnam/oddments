#!/usr/bin/env python3
"""Lexical near-neighbor candidates across stored records; NOT semantic/legal verdicts."""
import json
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
ROOT=Path(__file__).resolve().parents[1]
def main():
 old=[]
 for p in ['practice_expansion/2026-10-23/candidates/questions.json','practice_expansion/2026-10-26-plus/questions.json']:
  old+=json.loads((ROOT/p).read_text())['questions']
 canonical=[]
 for p in sorted((ROOT/'data/questions').glob('*.json')):
  d=json.loads(p.read_text());canonical+=d if isinstance(d,list) else [d]
 new=json.loads((ROOT/'practice_expansion/2026-10-27-quality/questions.json').read_text())['questions']
 qs=old+canonical+new
 # Context + choices; keep numbers. Boilerplate reduction only for retrieval, not edits.
 texts=[q['stem']+'\n'+'\n'.join(c['text'] for c in q['choices']) for q in qs]
 x=TfidfVectorizer(ngram_range=(1,2),min_df=2,sublinear_tf=True,strip_accents='unicode',token_pattern=r'(?u)\b\w+\b').fit_transform(texts)
 sim=(x@x.T).toarray();np.fill_diagonal(sim,-1)
 rows=[]
 for i,q in enumerate(qs):
  idx=np.argsort(sim[i])[-5:][::-1]
  rows.append(dict(question_id=q['question_id'],neighbors=[dict(question_id=qs[j]['question_id'],cosine=round(float(sim[i,j]),4),same_declared_family=q['family_id']==qs[j]['family_id']) for j in idx]))
 unique=[]
 for i in range(len(qs)):
  for j in np.where(sim[i,i+1:]>=.9)[0]+i+1:
   unique.append(dict(a=qs[i]['question_id'],b=qs[j]['question_id'],cosine=round(float(sim[i,j]),4),same_declared_family=qs[i]['family_id']==qs[j]['family_id']))
 result=dict(method='Word and bigram TF-IDF over stem and options, numeric tokens preserved; cosine >=0.90 is a review flag, not a semantic duplicate finding.',records=len(qs),baseline_records=len(old)+len(canonical),new_records=len(new),pairs_at_0_90=len(unique),cross_family_pairs_at_0_90=sum(not x['same_declared_family'] for x in unique),pairs=unique,nearest_neighbors=rows)
 out=ROOT/'reports/practice-quality/near-neighbors.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print({k:v for k,v in result.items() if k not in ['pairs','nearest_neighbors']})
if __name__=='__main__':main()
