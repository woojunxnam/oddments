import json,difflib,hashlib
from pathlib import Path
root=Path('.')
p=json.load(open('reports/full-corpus-review/phase10-d-evidence/assigned-visible-input.json'))
collections={json.loads(l)['collection'] for l in open('reports/full-corpus-review/question-ledger.jsonl')}
visible={}
for c in sorted(collections):
 for q in json.load(open(c))['questions']:
  visible[q['question_id']]={'question_id':q['question_id'],'stem':q['stem'],'choices':[{'id':z['id'],'text':z['text']} for z in q['choices']],'collection':c}
assigned={q['question_id'] for q in p['records']}
records=[]
for q in p['records']:
 near=sorted([(difflib.SequenceMatcher(None,q['stem'].lower(),z['stem'].lower()).ratio(),qid) for qid,z in visible.items() if qid!=q['question_id']],reverse=True)[:2]
 records.append({'target':q['question_id'],'nearest_candidates':[dict(similarity_candidate_only=score,**visible[qid]) for score,qid in near]})
out=root/'reports/full-corpus-review/phase10-d-evidence/nearby-visible-candidates.json'
out.write_text(json.dumps({'purpose':'VISIBLE_STEM_AND_ALL_OPTIONS_FOR_DIRECT_DUPLICATE_REVIEW; similarity only locates candidates; no keys or author judgements projected','records':records},ensure_ascii=False,indent=2)+'\n')
for row in records[:8]:
 print('TARGET',row['target'])
 for z in row['nearest_candidates']:
  print(z['question_id'],'candidate_similarity',round(z['similarity_candidate_only'],3),'\n'+z['stem'])
  for c in z['choices']:print(c['id']+': '+c['text'])
