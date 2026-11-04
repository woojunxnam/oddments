#!/usr/bin/env python3
"""Structural curation, not independent legal approval or a semantic uniqueness guarantee."""
import collections,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from audit_practice_quality import analyze,normalize,signature
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'practice_expansion/2026-10-27-quality'
def build():
 paths=['practice_expansion/2026-10-23/candidates/questions.json','practice_expansion/2026-10-26-plus/questions.json']
 old=sum((json.loads((ROOT/p).read_text())['questions'] for p in paths),[])
 new=json.loads((BASE/'questions.json').read_text())['questions']
 audit=analyze(old,'old');ledger={r['question_id']:r for r in audit['question_ledger']}
 families=collections.defaultdict(list)
 for q in old:families[q['family_id']].append(q)
 selected=[];packs=set();stems=set(); decisions=[]
 for family,qs in sorted(families.items()):
  def score(q):
   l=ledger[q['question_id']];flags=l['flags']
   return (signature(q) in packs,normalize(q['stem']) in stems,
    3*('IRRELEVANT_SECOND_CASE' in flags)+3*('INCORRECT' in q['stem'])+2*('SOLE_LONGEST_KEY_HEURISTIC' in flags)+('ABSOLUTE_DISTRACTOR_HEURISTIC' in flags),
    l['option_set_group_size'],l['stem_group_size'],l['maximum_choice_reuse'],q['question_id'])
  q=min(qs,key=score);selected.append(q);packs.add(signature(q));stems.add(normalize(q['stem']))
  decisions.append(dict(family_id=family,representative=q['question_id'],retained_other_variants=[x['question_id'] for x in qs if x!=q],basis='Lexical repetition and wording-risk heuristics, one representative per existing declared family. Not a legal audit.'))
 # One stem or full option set per default pool; keep alternate family variants in archive.
 deduplicated=[];seen_stems=set();seen_packs=set();omitted=[]
 for q in selected:
  stem=normalize(q['stem']);pack=signature(q)
  if stem in seen_stems or pack in seen_packs:
   omitted.append(dict(question_id=q['question_id'],family_id=q['family_id'],reason='Exact normalized stem or complete option set already represented; still available in all-variants view.'));continue
  seen_stems.add(stem);seen_packs.add(pack);deduplicated.append(q)
 selected=deduplicated+new
 result=dict(edition='2026-10-27.quality1',recommended_ids=[q['question_id'] for q in selected],new_ids=[q['question_id'] for q in new],decisions=decisions,omitted_default_representatives=omitted,stats=dict(recommended=len(selected),legacy_representatives=len(deduplicated),new=len(new),available_total=len(old)+len(new)),input_hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},scope='All existing variants remain reachable. Recommended selection reduces repetition; family labels do not prove independent legal decision paths.')
 (BASE/'selection.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 reports=ROOT/'reports/practice-quality';reports.mkdir(exist_ok=True,parents=True)
 comparisons=[analyze(selected,'recommended_selection'),analyze(new,'individually_authored_96')]
 (reports/'after-audit.json').write_text(json.dumps(dict(date='2026-10-27',results=comparisons),ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(result['stats']));print([{k:r[k] for k in ['scope','total_questions','additional_identical_stem_occurrences','questions_in_identical_option_sets','unique_normalized_choices']} for r in comparisons])
 return result
if __name__=='__main__':build()
