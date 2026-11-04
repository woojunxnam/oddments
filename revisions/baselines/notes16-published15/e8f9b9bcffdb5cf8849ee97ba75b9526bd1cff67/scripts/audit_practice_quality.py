#!/usr/bin/env python3
"""Exhaustive structural audit, not an independent legal/psychometric adjudication.

Normalization preserves dates and quantities. Shared generic lead-ins are not by
themselves semantic duplicates. Complete option-set reuse is reported separately.
"""
from __future__ import annotations
import argparse, collections, hashlib, json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def normalize(text: str) -> str:
    return re.sub(r'[^\w]+', ' ', text.casefold()).strip()
def sha(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def signature(q):
    return tuple(sorted(normalize(c['text']) for c in q['choices']))
def analyze(qs, label):
    stems=collections.defaultdict(list); options=collections.defaultdict(list); packs=collections.defaultdict(list)
    keys=collections.defaultdict(list); families=collections.defaultdict(list); rows=[]
    for q in qs:
        i=q['question_id'];stems[normalize(q['stem'])].append(i);packs[signature(q)].append(i);families[q['family_id']].append(i)
        for c in q['choices']:
            options[normalize(c['text'])].append(i)
            if c['id'] in q['correct_choice_ids']: keys[normalize(c['text'])].append(i)
    for q in qs:
        flags=[];i=q['question_id']; cc=q['choices'];a=set(q['correct_choice_ids'])
        if len(stems[normalize(q['stem'])])>1:flags.append('REUSED_STEM')
        if len(packs[signature(q)])>1:flags.append('IDENTICAL_OPTION_SET')
        if len(families[q['family_id']])>1:flags.append('RELATED_FAMILY_VARIANTS')
        if 'Case A:' in q['stem'] and 'Case B:' in q['stem'] and ('addresses Case A' in q['stem'] or 'addresses Case B' in q['stem']):flags.append('IRRELEVANT_SECOND_CASE')
        if q['question_type']=='SBA':
            right=[c for c in cc if c['id'] in a];wrong=[c for c in cc if c['id'] not in a]
            if len(right)==1 and wrong and len(right[0]['text'])>max(len(c['text']) for c in wrong):flags.append('SOLE_LONGEST_KEY_HEURISTIC')
        if any(re.search(r'\b(always|never|every|automatically|any|only)\b',c['text'],re.I) for c in cc if c['id'] not in a):flags.append('ABSOLUTE_DISTRACTOR_HEURISTIC')
        rows.append(dict(question_id=i,family_id=q['family_id'],question_type=q['question_type'],area=q['area'],
                         flags=flags,stem_group_size=len(stems[normalize(q['stem'])]),option_set_group_size=len(packs[signature(q)]),
                         maximum_choice_reuse=max(len(options[normalize(c['text'])]) for c in cc),
                         legal_adjudication='NOT_PERFORMED_BY_STRUCTURAL_AUDIT'))
    return dict(scope=label,total_questions=len(qs),families=len(families),total_choice_slots=sum(len(q['choices']) for q in qs),
                unique_normalized_choices=len(options),reused_choice_slots=sum(len(v)-1 for v in options.values()),
                unique_normalized_stems=len(stems),additional_identical_stem_occurrences=sum(len(v)-1 for v in stems.values()),
                questions_in_identical_option_sets=sum(len(v) for v in packs.values() if len(v)>1),
                repeated_option_set_groups=sum(len(v)>1 for v in packs.values()),
                flag_counts=dict(collections.Counter(f for r in rows for f in r['flags'])),
                most_reused_choices=[dict(text=k,count=len(v),question_ids=v) for k,v in sorted(options.items(),key=lambda x:-len(x[1]))[:25]],
                repeated_stem_groups=[dict(question_ids=v,normalized_stem=k) for k,v in stems.items() if len(v)>1],
                repeated_option_sets=[dict(question_ids=v,normalized_options=list(k)) for k,v in packs.items() if len(v)>1],
                question_ledger=rows)
def run():
    paths=['practice_expansion/2026-10-23/candidates/questions.json','practice_expansion/2026-10-26-plus/questions.json']
    banks=[json.loads((ROOT/p).read_text())['questions'] for p in paths]
    canonical=[]
    for p in sorted((ROOT/'data/questions').glob('*.json')):
        d=json.loads(p.read_text());canonical.extend(d if isinstance(d,list) else [d])
    results=[analyze(banks[0],'original_1024'),analyze(banks[1],'plus_1152'),analyze(sum(banks,[]),'online_expansion_2176'),analyze(canonical,'canonical_records_not_all_public'),analyze(sum(banks,[])+canonical,'all_stored_question_records')]
    out=ROOT/'reports/practice-quality';out.mkdir(parents=True,exist_ok=True)
    data=dict(date='2026-10-27',base_commit='403f370d964e4861e7fb033a737aa98d27194174',
              input_hashes={p:sha((ROOT/p).read_bytes()) for p in paths},normalization='Case-fold + punctuation/whitespace normalization; numerical values preserved.',
              boundaries=['Same stem can introduce genuinely different options; stem reuse alone is not a semantic-duplicate verdict.',
                          'Repeated short numerical choices are not automatically a defect.',
                          'Heuristics identify review candidates, not proof of legal error or real-exam difficulty.',
                          'Canonical records include non-public states. No release/audit flag is changed.'],results=results)
    data['canonical_file_hashes']={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in sorted((ROOT/'data/questions').glob('*.json'))}
    answer_groups=collections.defaultdict(list)
    for q in sum(banks,[]):
        keyed=tuple(sorted(normalize(c['text']) for c in q['choices'] if c['id'] in q['correct_choice_ids']))
        answer_groups[keyed].append(q['question_id'])
    groups=[dict(answer_texts=list(k),question_ids=v) for k,v in answer_groups.items() if len(v)>1]
    reuse=dict(scope='online_2176_original',definition='Identical normalized text sets of keyed correct choices; choice letters ignored. The same legally correct quantity or action can recur legitimately. Not a duplicate verdict.',groups=groups,questions_in_repeated_correct_answer_sets=sum(len(x['question_ids']) for x in groups),group_count=len(groups))
    (out/'answer-reuse.json').write_text(json.dumps(reuse,ensure_ascii=False,indent=2)+'\n')
    (out/'baseline-audit.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps([{k:r[k] for k in ['scope','total_questions','families','unique_normalized_choices','additional_identical_stem_occurrences','questions_in_identical_option_sets']} for r in results],ensure_ascii=False,indent=2))
    return data
if __name__=='__main__':run()
