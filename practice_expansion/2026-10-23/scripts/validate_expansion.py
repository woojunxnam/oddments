#!/usr/bin/env python3
"""Structural and lexical diagnostics. This does not verify law or realism."""
from __future__ import annotations
import argparse, collections, hashlib, json, re, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_expansion import canonical_hash, normalized
ROOT=Path(__file__).resolve().parents[1]

def validate(existing:Path|None=None)->dict:
 d=json.loads((ROOT/'candidates/questions.json').read_text()); qs=d['questions'];errors=[]
 def check(ok,msg):
  if not ok:errors.append(msg)
 check(len(qs)==1024,'count != 1024'); check(len({q['question_id'] for q in qs})==1024,'duplicate ID')
 fc=collections.Counter(q['family_id'] for q in qs)
 check(len(fc)==256 and set(fc.values())=={4},'family count/size mismatch')
 check(len({normalized(q['stem']) for q in qs})==1024,'exact normalized stem duplicate')
 answerpos=collections.Counter();sata=collections.Counter();length_longest=0;length_total=0;absolute=[]
 for q in qs:
  qid=q['question_id'];choices=q['choices'];a=q['correct_choice_ids']
  check(q['content_sha256']==canonical_hash({k:v for k,v in q.items() if k!='content_sha256'}),qid+' hash mismatch')
  check(q['lifecycle_status']=='DRAFT' and not q['publication_eligible'],qid+' publication gate violation')
  check(q['verification_status']=='NOT_INDEPENDENTLY_REVIEWED' and q['independent_legal_audit'] is None and q['independent_realism_audit'] is None,qid+' fabricated audit status')
  check(len(choices)==4 and {c['id'] for c in choices}==set('ABCD'),qid+' choice structure')
  check(len({normalized(c['text']) for c in choices})==4,qid+' duplicate choices')
  check(len(a)==len(set(a)) and set(a)<=set('ABCD') and len(a)>=1,qid+' answer set')
  check(set(q['explanation']['choice_analysis'])==set('ABCD'),qid+' missing rationale')
  check(len(set(q['explanation']['choice_analysis'].values()))==4,qid+' duplicate rationale')
  check(bool(q['note_evidence']) and bool(q['source_ids']),qid+' missing evidence links')
  check(all(s in d['sources'] for s in q['source_ids']),qid+' unresolved source')
  truth=q['_statement_truth'];expected=[c['id'] for c in choices if ((not truth[c['id']]) if q['negative_lead_in'] else truth[c['id']])]
  check(a==expected,qid+' answer/truth mapping')
  if q['question_type']=='SBA':
   check(len(a)==1,qid+' SBA count');answerpos.update(a)
   lens={c['id']:len(c['text'].split()) for c in choices};length_total+=1
   if lens[a[0]]>max(n for k,n in lens.items() if k!=a[0]):length_longest+=1
  else:sata[len(a)]+=1
  if any(re.search(r'\b(always|never|automatically|every|all|only)\b',c['text'],re.I) for c in choices):absolute.append(qid)
 check(set(answerpos.values())=={192},'SBA option-position imbalance')
 original_report={'status':'NOT_RUN'}
 if existing is not None:
  originals=[]
  for p in sorted(existing.glob('*.json')):
   v=json.loads(p.read_text());
   if isinstance(v,dict) and 'stem' in v:originals.append(v)
  old_ids={q['question_id'] for q in originals};old_stems={normalized(q['stem']):q['question_id'] for q in originals}
  collisions=[q['question_id'] for q in qs if q['question_id'] in old_ids]
  exact=[{'new':q['question_id'],'old':old_stems[normalized(q['stem'])]} for q in qs if normalized(q['stem']) in old_stems]
  check(not collisions,'existing ID collision');check(not exact,'existing exact stem match')
  # Shared-family variants intentionally have the same case context. Compare families, not 1,024 copies.
  fams=json.loads((ROOT/'authoring/families.json').read_text())
  from sklearn.feature_extraction.text import TfidfVectorizer
  import numpy as np
  texts=[f['case_a']+' '+f['case_b'] for f in fams]+[q['stem'] for q in originals]
  vectors=TfidfVectorizer(ngram_range=(1,2),stop_words='english',min_df=1).fit_transform(texts)
  sim=(vectors[:len(fams)]@vectors[len(fams):].T).toarray()
  nearest=[]
  for i,f in enumerate(fams):
   j=int(np.argmax(sim[i]));nearest.append({'new_family':f['family_id'],'existing_question':originals[j]['question_id'],'tfidf_cosine':round(float(sim[i,j]),4)})
  same=(vectors[:len(fams)]@vectors[:len(fams)].T).toarray();np.fill_diagonal(same,0)
  cross=[{'family_a':fams[i]['family_id'],'family_b':fams[j]['family_id'],'tfidf_cosine':round(float(same[i,j]),4)} for i in range(len(fams)) for j in range(i+1,len(fams)) if same[i,j]>=.25]
  original_report={'status':'LEXICAL_SCREEN_ONLY','existing_records_read':len(originals),
   'existing_stored_status_counts':dict(collections.Counter(q.get('lifecycle_status') for q in originals)),
   'existing_id_collisions':collisions,'existing_exact_stem_matches':exact,
   'highest_existing_similarities':sorted(nearest,key=lambda x:-x['tfidf_cosine'])[:40],
   'new_cross_family_pairs_above_025':sorted(cross,key=lambda x:-x['tfidf_cosine']),
   'semantic_duplicate_clearance':False,'threshold_note':'0.25 is a screening choice, not a validated semantic-duplicate threshold.'}
 report={'status':'STRUCTURAL_PASS' if not errors else 'STRUCTURAL_FAIL','errors':errors,
  'question_count':len(qs),'family_count':len(fc),'types':dict(collections.Counter(q['question_type'] for q in qs)),
  'areas':dict(collections.Counter(q['area'] for q in qs)),
  'sba_answer_positions':dict(sorted(answerpos.items())),
  'sata_answer_cardinalities':dict(sorted(sata.items())),
  'exact_normalized_new_stem_duplicates':1024-len({normalized(q['stem']) for q in qs}),
  'design_warnings':{'fixed_four_variant_family_pattern':True,'negative_lead_in_items':sum(q['negative_lead_in'] for q in qs),
   'items_with_absolute_cue_words':len(absolute),'absolute_cue_item_ids':absolute,
   'sba_correct_option_strictly_longest':length_longest,'sba_total':length_total,
   'comment':'These are review flags, not passed realism gates. Some distractors are easy or formulaic; independent item-writing review is required.'},
  'independently_legal_audited':0,'independently_realism_audited':0,'new_released':0,
  'original_bank_comparison':original_report,
  'coverage':{'referenced_units':d['stats']['referenced_note_units'],'total_note_units':306,
              'note_counts_are_not_legal_coverage_or_exam_readiness':True},
  'legal_accuracy_tested_by_this_script':False}
 (ROOT/'reports/structural-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 return report
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--existing-questions',type=Path);a=p.parse_args();r=validate(a.existing_questions)
 print(json.dumps({k:v for k,v in r.items() if k not in ['design_warnings','original_bank_comparison']},ensure_ascii=False,indent=2))
 print('Realism warnings:',{k:v for k,v in r['design_warnings'].items() if not k.endswith('_ids')})
 raise SystemExit(bool(r['errors']))
