"""Protect zero-claim scope and prevent warnings from becoming invented defects."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from build_full_corpus_review import verified_nonlegal_census
from notes_revision import load_notes
import build_representative_rewrites as builder


def nonlegal_input():
    census = json.loads((ROOT/'reports/full-corpus-review/note-wave16-census.json').read_bytes())
    unit = next(u for u in census['units'] if u['unit_id'] == 'w6-b-16')
    effective = next(u for c in load_notes()['chapters'] for u in c['units'] if u['id'] == unit['unit_id'])
    return census, unit, effective


def test_only_exact_independently_classified_method_body_can_have_zero_legal_claims():
    census, unit, effective = nonlegal_input()
    assert verified_nonlegal_census(census, unit, effective)
    for field, value in [('unit_id','w6-b-17'), ('unit_content_sha256','0'*64),
                         ('claim_count',1), ('nonlegal_inventory_only',False)]:
        changed = copy.deepcopy(unit); changed[field] = value
        assert not verified_nonlegal_census(census, changed, effective)
    changed = copy.deepcopy(census); changed.pop('editorial_nonlegal_inventory')
    assert not verified_nonlegal_census(changed, unit, effective)
    changed = copy.deepcopy(effective); changed['body'] += '\nA new legal requirement.'
    with pytest.raises(ValueError, match='classification scope changed'):
        verified_nonlegal_census(census, unit, changed)


def test_nonlegal_proof_cannot_be_rebound_after_changing_independent_finding(tmp_path):
    census, unit, effective = nonlegal_input()
    author = 'reports/full-corpus-review/note-wave16-census.json'
    proof = 'reports/full-corpus-review/nonlegal-w6-b-16-independent-classification.json'
    for path in [author, proof]:
        target = tmp_path/path; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT/path, target)
    path = tmp_path/proof
    value = json.loads(path.read_bytes()); value['classification'] = 'LEGAL_CLAIMS_FOUND'
    path.write_text(json.dumps(value))
    with pytest.raises(ValueError, match='independent classification changed'):
        verified_nonlegal_census(census, unit, effective, tmp_path)


def test_independent_archive_warning_requires_an_actual_negative_or_hold(tmp_path, monkeypatch):
    source = 'reports/full-corpus-review/independent-phase2-e-review.json'
    raw = (ROOT/source).read_bytes()
    target = tmp_path/source; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(raw)
    report = json.loads(raw)
    bank = json.loads((ROOT/'practice_expansion/2026-10-26-plus/questions.json').read_bytes())
    questions = {q['question_id']:q for q in bank['questions']}
    monkeypatch.setattr(builder, 'ROOT', tmp_path)
    monkeypatch.setattr(builder, 'REPORTS', tmp_path/'reports/representative-rewrite')
    builder.REPORTS.mkdir(parents=True)
    path = builder.REPORTS/'archive-review-notices.json'
    def notice(qid):
        row = next(r for r in report['records'] if r['question_id'] == qid)
        data = dict(schema_version='practice-archive-review-notices/1', notices=[dict(
            question_ids=[qid], issue_type='INDEPENDENT_REVIEW_FINDING', reason='개별 검토 안내',
            question_record_hashes={qid:row['record_sha256']}, review_source=source,
            review_source_sha256=hashlib.sha256(target.read_bytes()).hexdigest())])
        path.write_text(json.dumps(data))
    notice('MA-CASE-0426')
    assert len(builder.archive_review_notices(questions, {})) == 1
    notice('MA-CASE-0421')
    with pytest.raises(ValueError, match='lacks a negative or blocked review'):
        builder.archive_review_notices(questions, {})
    report['independent_of_authors'] = False
    target.write_text(json.dumps(report))
    notice('MA-CASE-0426')
    with pytest.raises(ValueError, match='independent review provenance'):
        builder.archive_review_notices(questions, {})
