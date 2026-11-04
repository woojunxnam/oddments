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

@pytest.mark.parametrize('mutation', ['promote', 'credit', 'rewrite_snapshot'])
def test_historical_warning_cannot_promote_or_rewrite_its_retained_review(tmp_path, monkeypatch, mutation):
    import hashlib
    import build_representative_rewrites as builder
    source_path = 'reports/full-corpus-review/pub05-14-independent-review.json'
    notices = json.loads((ROOT / 'reports/representative-rewrite/archive-review-notices.json').read_text())
    notice = copy.deepcopy(next(n for n in notices['notices'] if n['issue_type'] == 'HISTORICAL_REVIEW_FINDING' and 'MA-EXP-0385' in n['question_ids']))
    source = tmp_path / source_path
    source.parent.mkdir(parents=True)
    source.write_bytes((ROOT / source_path).read_bytes())
    reports = tmp_path / 'reports/representative-rewrite'
    reports.mkdir(parents=True)
    target = reports / 'archive-review-notices.json'
    payload = {'schema_version': 'practice-archive-review-notices/1', 'notices': [notice]}
    target.write_text(json.dumps(payload, ensure_ascii=False))
    bank = json.loads((ROOT / 'practice_expansion/2026-10-23/candidates/questions.json').read_text())
    question = next(q for q in bank['questions'] if q['question_id'] == 'MA-EXP-0385')
    monkeypatch.setattr(builder, 'ROOT', tmp_path)
    monkeypatch.setattr(builder, 'REPORTS', reports)
    assert len(builder._existing_archive_review_notices({'MA-EXP-0385': question}, {})) == 1
    if mutation == 'promote':
        notice['issue_type'] = 'INDEPENDENT_REVIEW_FINDING'
    elif mutation == 'credit':
        notice['new_independent_review_credit'] = 1
    else:
        changed = json.loads(source.read_bytes())
        changed['scope_ko'] = 'rewritten historical scope'
        source.write_text(json.dumps(changed, ensure_ascii=False))
        notice['review_source_sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
    target.write_text(json.dumps(payload, ensure_ascii=False))
    with pytest.raises(ValueError, match='provenance|exact retained review snapshot'):
        builder._existing_archive_review_notices({'MA-EXP-0385': question}, {})
