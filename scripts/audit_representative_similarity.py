#!/usr/bin/env python3
"""Retrieve near-text candidates across archives/canonical records and the rewrite unit.

Cosine similarity is a search aid. Editorial decision-path comparisons are separate.
All before/after counts below use one shared fitted vocabulary for comparability.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/representative-rewrite/near-candidates.json'


def compute():
    paths = [ROOT / 'practice_expansion' / part / 'questions.json' for part in (
        '2026-10-23/candidates', '2026-10-26-plus', '2026-10-27-quality', '2026-10-28-representative')]
    banks = [json.loads(p.read_text())['questions'] for p in paths]
    canonical = []
    for p in sorted((ROOT / 'data/questions').glob('*.json')):
        value = json.loads(p.read_text())
        canonical.extend(value if isinstance(value, list) else [value])
    previous = sum(banks[:3], [])
    new = banks[3]
    questions = previous + canonical + new
    texts = [q['stem'] + '\n' + '\n'.join(c['text'] for c in q['choices']) for q in questions]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True,
        strip_accents='unicode', token_pattern=r'(?u)\b\w+\b')
    vectors = vectorizer.fit_transform(texts)
    scores = (vectors @ vectors.T).toarray()
    np.fill_diagonal(scores, -1)
    index = {q['question_id']: i for i, q in enumerate(questions)}
    old_selection = json.loads((ROOT / 'practice_expansion/2026-10-27-quality/selection.json').read_text())
    new_selection = json.loads((ROOT / 'practice_expansion/2026-10-28-representative/selection.json').read_text())
    def pairs(ids):
        positions = [index[i] for i in ids]
        result = []
        for offset, i in enumerate(positions):
            for j in positions[offset + 1:]:
                if scores[i, j] >= .90:
                    result.append(dict(a=questions[i]['question_id'], b=questions[j]['question_id'],
                        cosine=round(float(scores[i, j]), 6), same_declared_family=questions[i]['family_id'] == questions[j]['family_id']))
        return result
    scopes = {
        'baseline_full_2272': [q['question_id'] for q in previous],
        'current_full': [q['question_id'] for q in previous + new],
        'baseline_default_451': old_selection['recommended_ids'],
        'current_default': new_selection['recommended_ids'],
    }
    full_pairs = pairs([q['question_id'] for q in questions])
    neighbors = []
    for q in new:
        i = index[q['question_id']]
        nearest = sorted(range(len(questions)), key=lambda j: (-float(scores[i, j]), questions[j]['question_id']))[:5]
        neighbors.append(dict(question_id=q['question_id'], neighbors=[dict(question_id=questions[j]['question_id'],
            cosine=round(float(scores[i, j]), 6), same_declared_family=q['family_id'] == questions[j]['family_id']) for j in nearest],
            author_decision_comparisons=q['comparison_with_existing_quality']))
    revision_bank = json.loads(paths[-1].read_text())
    return dict(date=revision_bank.get('updated_at', revision_bank['authored_at']), method='Word+bigram TF-IDF cosine; min_df2; sublinear_tf; numeric tokens retained; >=0.90 review threshold; one combined vocabulary for before/after comparisons.',
        records=len(questions), canonical_records_including_nonpublic=len(canonical), new_records=len(new),
        input_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        scope_counts={name: dict(records=len(ids), near_text_pairs_at_0_90=len(pairs(ids))) for name, ids in scopes.items()},
        all_corpus_pairs_at_0_90=full_pairs, new_question_nearest_neighbors=neighbors,
        semantic_duplicate_verdict='NOT_DETERMINED_BY_ALGORITHM',
        limits=['A shared rule or high score is not automatically a duplicate.',
                'Low lexical similarity does not establish distinct legal decisions.',
                'Original archives are retained; near-text repetitions there are not falsely reported as removed.',
                'See semantic-review.json and each authored comparison for actual editorial judgments.'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = compute()
    content = (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode()
    if args.check:
        if not OUT.exists() or OUT.read_bytes() != content:
            raise SystemExit('Near-candidate report drift')
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_bytes(content)
    print(json.dumps(data['scope_counts']))


if __name__ == '__main__':
    main()
