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


def test_author_archive_warning_binds_actual_individual_finding_and_cannot_invent_a_defect(tmp_path,monkeypatch):
    source='reports/full-corpus-review/unit3a-author-review.json'
    report=json.loads((ROOT/source).read_bytes())
    qid='MA-EXP-0121'
    row=next(r for r in report['records'] if r['question_id']==qid)
    questions={q['question_id']:q for q in json.loads((ROOT/builder.ARCHIVES[0]).read_bytes())['questions']}
    target=tmp_path/source;target.parent.mkdir(parents=True,exist_ok=True)
    monkeypatch.setattr(builder,'ROOT',tmp_path)
    monkeypatch.setattr(builder,'REPORTS',tmp_path/'reports/representative-rewrite')
    builder.REPORTS.mkdir(parents=True)
    notice=dict(question_ids=[qid],issue_type='AUTHOR_REVIEW_FINDING',reason='실제 미해결 저자 지적',
        original_author_blocker=row['blocker'],question_record_hashes={qid:row['record_sha256']},review_source=source)
    def save():
        target.write_text(json.dumps(report))
        notice['review_source_sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
        (builder.REPORTS/'archive-review-notices.json').write_text(json.dumps(dict(
            schema_version='practice-archive-review-notices/1',notices=[notice])))
    save(); assert len(builder.archive_review_notices(questions,{}))==1
    original=row['disposition'];row['disposition']='KEEP';save()
    with pytest.raises(ValueError,match='individual nonKEEP'):builder.archive_review_notices(questions,{})
    row['disposition']=original;notice['original_author_blocker']='invented blocker';save()
    with pytest.raises(ValueError,match='individual nonKEEP'):builder.archive_review_notices(questions,{})
    notice['original_author_blocker']=row['blocker'];row['choice_by_choice_findings'].pop('D');save()
    with pytest.raises(ValueError,match='individual nonKEEP'):builder.archive_review_notices(questions,{})


@pytest.mark.parametrize('defect',[None,'question_hash','quote','credit'])
def test_editorial_cue_holds_require_actual_current_text_and_never_legal_credit(tmp_path,monkeypatch,defect):
    relative='reports/full-corpus-review/phase5-default-editorial-holds.json'
    source=json.loads((ROOT/relative).read_bytes())
    holds=json.loads((ROOT/'reports/representative-rewrite/default-holds.json').read_bytes())['holds']
    hold=copy.deepcopy(next(h for h in holds if h.get('finding_type')=='ROOT_EDITORIAL_WORDING_HOLD'))
    row=next(r for r in source['records'] if r['question_id']==hold['legacy_question_id'])
    questions={q['question_id']:q for q in json.loads((ROOT/builder.ARCHIVES[1]).read_bytes())['questions']}
    if defect=='question_hash':row['record_sha256']='0'*64
    elif defect=='quote':row['choice_evidence'][0]['exact_quote']='invented quoted requirement'
    elif defect=='credit':source['independent_legal_credit']=1
    path=tmp_path/relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(source))
    hold['evidence_report_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    monkeypatch.setattr(builder,'ROOT',tmp_path)
    if defect:
        with pytest.raises(ValueError):builder.validate_editorial_wording_holds([hold],questions,{})
    else:
        hashes={};builder.validate_editorial_wording_holds([hold],questions,hashes)
        assert relative in hashes
