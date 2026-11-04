"""Regressions for actual retained findings that lacked archive warnings."""
import copy
import json
from pathlib import Path
import pytest
from build_full_corpus_review import validate_independent_archive_safety

ROOT = Path(__file__).resolve().parents[1]

def record(filename, qid):
    source = json.loads((ROOT / 'reports/full-corpus-review' / filename).read_text())
    return next(r for r in source['records'] if r['question_id'] == qid)

@pytest.mark.parametrize('filename,qid', [
    ('pub05-14-independent-review.json', 'MA-EXP-0385'),
    ('wave2-independent-review.json', 'MA-CASE-0118'),
    ('independent-phase7-b-review.json', 'MA-CASE-1054'),
    ('independent-phase7-c-review.json', 'MA-CASE-1006'),
])
def test_real_retained_negative_cannot_lose_its_archive_warning(filename, qid):
    row = record(filename, qid)
    selection = json.loads((ROOT / 'practice_expansion/2026-10-28-representative/selection.json').read_text())
    validate_independent_archive_safety(selection, [row])
    missing = copy.deepcopy(selection)
    missing['archive_review_notices'] = [n for n in missing['archive_review_notices'] if qid not in n['question_ids']]
    missing['holds'] = [h for h in missing['holds'] if h['legacy_question_id'] != qid]
    with pytest.raises(ValueError, match='Unsurfaced independent archive finding: ' + qid):
        validate_independent_archive_safety(missing, [row])

def test_pending_editorial_assessment_does_not_become_a_fabricated_failure():
    row = record('wave2-independent-review.json', 'MA-CASE-0001')
    assert row['realism_review']['verdict'] == 'EDITORIAL_REVIEW_REQUIRED'
    validate_independent_archive_safety({'archive_review_notices': [], 'holds': []}, [row])
