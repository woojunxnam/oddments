#!/usr/bin/env python3
"""Reproducible non-adjudicative quality diagnostics against both existing banks."""
import hashlib,json,re
from collections import Counter
from pathlib import Path
P=Path(__file__).resolve().parents[1];R=P.parents[1]
new=json.loads((P/'questions.json').read_text())['questions'];old=json.loads((R/'practice_expansion/2026-10-23/candidates/questions.json').read_text())['questions']
canonical=[json.loads(p.read_text()) for p in (R/'data/questions').glob('*.json')]
def norm(s):return re.sub(r'\s+',' ',s).lower().strip()
def fingerprint(q):return norm(q.get('stem',''))+' | '+' | '.join(sorted(norm(x.get('text','')) for x in q.get('choices',[])))
newfps=[fingerprint(q) for q in new];oldfps={fingerprint(q) for q in old+canonical}
assert len(set(newfps))==len(newfps),'Exact question+choice duplicates in new bank'
assert not set(newfps)&oldfps,'Exact question+choice duplicate with existing bank'
correct_longest=[];cue_by_truth={True:Counter(),False:Counter()};overlap=[]
for q in new:
    if q['question_type']=='SBA':
        lengths={x['id']:len(x['text'].split()) for x in q['choices']};ans=q['correct_choice_ids'][0]
        if lengths[ans]>max(n for k,n in lengths.items() if k!=ans):correct_longest.append(q['question_id'])
    for c in q['choices']:
        truth=c['id'] in q['correct_choice_ids']
        for w in re.findall(r'\b(?:always|never|automatically|solely|every|all|only)\b',c['text'].lower()):cue_by_truth[truth][w]+=1
# Lexical nearest neighbours, not a certificate of semantic novelty.
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    import numpy as np
    texts=[fingerprint(q) for q in old+canonical+new]
    vec=TfidfVectorizer(ngram_range=(1,2),min_df=2,max_features=40000,sublinear_tf=True)
    x=vec.fit_transform(texts);base=x[:len(old)+len(canonical)];nx=x[len(old)+len(canonical):]
    for start in range(0,len(new),100):
        a=(nx[start:start+100]@base.T).toarray()
        for j,row in enumerate(a):
            k=int(row.argmax());overlap.append(dict(new_id=new[start+j]['question_id'],existing_id=(old+canonical)[k].get('question_id'),similarity=round(float(row[k]),4)))
    overlap.sort(key=lambda z:z['similarity'],reverse=True)
except ImportError:overlap=[dict(status='sklearn unavailable; similarity not run')]
report=dict(new_questions=len(new),original_practice_questions=len(old),canonical_records=len(canonical),
 exact_combined_stem_choice_collisions=0,exact_new_combined_duplicates=0,
 repeated_stem_occurrences=len(new)-len(set(norm(q['stem']) for q in new)),
 repeated_stem_note='Same work-queue lead-in is reused; distinct actions and answer states are in the choices. Numerical cases also reuse a tagged decision model.',
 models=len({q['family_id'] for q in new}),model_counts=dict(Counter(q['practice_angle'] for q in new)),
 correct_unique_longest_SBA=len(correct_longest),SBA_count=sum(q['question_type']=='SBA' for q in new),
 correct_unique_longest_ids=correct_longest,
 lexical_cues={str(k):dict(v) for k,v in cue_by_truth.items()},
 nearest_existing_items=overlap[:60],
 independent_semantic_adjudication=False,psychometric_calibration=False,
 interpretation='These are flags to inspect, not independent legal/realism audits. Related concepts deliberately recur; zero exact collisions does not prove all semantic decisions are new.')
(P/'reports/quality-diagnostics.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('correct_unique_longest_ids','nearest_existing_items')},ensure_ascii=False,indent=2))
print('Highest lexical matches:',overlap[:8])
