"""Evidence freshness and actual containment, not a legal pass certificate."""
import copy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from build_full_corpus_review import validate_note_census, validate_review, record_hash
from notes_revision import load_notes


def read(path):
    return json.loads((ROOT/path).read_text())


def bank():
    return {q['question_id']: q for q in read('practice_expansion/2026-10-23/candidates/questions.json')['questions']}


def test_first_cohort_has_exact_fresh_option_reviews_and_independent_failures_are_held():
    questions = bank()
    expected = {f'MA-EXP-{i:04d}' for i in range(385, 425)}
    records = [r for name in ['pub05-09', 'pub10-14']
               for r in read(f'reports/full-corpus-review/{name}-author-review.json')['records']]
    assert len(records) == 40 and {r['question_id'] for r in records} == expected
    for record in records:
        validate_review(questions[record['question_id']], record)
    audit = read('reports/full-corpus-review/pub05-14-independent-review.json')
    assert audit['independent_of_authors'] and not audit['canonical_audit']
    assert audit['summary']['realism_pass'] == 0
    selection = read('practice_expansion/2026-10-28-representative/selection.json')
    held = {i for h in selection['holds'] for i in [h['legacy_question_id'], *h.get('affected_archive_ids', [])]}
    assert expected <= held
    assert not expected.intersection(selection['recommended_ids'])
    assert {'MA-EXP-0351', 'MA-EXP-0367', 'MA-EXP-0383'} <= held


def test_atomic_census_requires_fresh_units_and_actual_evidence():
    census = read('reports/full-corpus-review/pub05-14-note-census.json')
    effective = {u['id']: u for c in load_notes(revision_id='2026-10-30.cdtm13-vax04.1')['chapters'] for u in c['units']}
    assert len(validate_note_census(census, effective, bank())) == 12
    stale = copy.deepcopy(effective)
    stale[census['units'][0]['unit_id']]['body'] += ' unreviewed edit'
    with pytest.raises(ValueError, match='Stale census unit'):
        validate_note_census(census, stale, bank())
    missing = copy.deepcopy(census)
    missing['claims'].pop()
    with pytest.raises(ValueError, match='Incomplete census'):
        validate_note_census(missing, effective, bank())
    altered = copy.deepcopy(census)
    next(iter(altered['sources'].values()))['source_evidence_sha256'] = '0'*64
    with pytest.raises(ValueError, match='Stale census evidence'):
        validate_note_census(altered, effective, bank())


def test_partial_product_clause_report_cannot_claim_complete_units():
    census = read('reports/full-corpus-review/note-wave2-census.json')
    effective = {u['id']: u for c in load_notes(revision_id='2026-10-30.cdtm13-vax04.1')['chapters'] for u in c['units']}
    public_ids = {json.loads(line)['question_id']: None for line in
                  (ROOT/'reports/full-corpus-review/question-ledger.jsonl').read_text().splitlines()}
    units = validate_note_census(census, effective, public_ids)
    complete = [u for u in units.values() if u['census_status'].startswith('COMPLETE_AUTHOR_')]
    assert len(units) == 20 and len(complete) == 4
    altered = copy.deepcopy(census)
    altered['units'][0]['census_status'] = 'COMPLETE_AUTHOR_ENUMERATION_PENDING_INDEPENDENT_COMPLETENESS_CHECK'
    with pytest.raises(ValueError, match='Partial clauses'):
        validate_note_census(altered, effective, public_ids)
