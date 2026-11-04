"""Real current findings must not disappear behind a supported answer key."""
import copy
import json
from pathlib import Path
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_full_corpus_review import apply_independent_legacy_review, validate_default_review_safety, build, OUT


def record(qid):
    letter='c' if qid=='MA-CASE-0798' else 'f'
    source=json.loads((ROOT/f'reports/full-corpus-review/independent-phase5-{letter}-review.json').read_bytes())
    return next(r for r in source['records'] if r['question_id']==qid)


@pytest.mark.parametrize('qid', ['MA-CASE-0812','MA-CASE-0813','MA-CASE-0814','MA-CASE-0816','MA-CASE-0798'])
def test_supported_key_and_realism_pass_do_not_mask_actual_hold_or_rationale_defect(qid):
    audit=record(qid);original=copy.deepcopy(audit)
    assert audit['legal_review']['existing_answer_correct']=='YES' and audit['realism_review']['verdict']=='PASS'
    row=dict(question_id=qid,disposition='KEEP',blocker=None,answer_key_assessment='CORRECT')
    apply_independent_legacy_review(row,audit)
    expected='MINOR_EDIT' if qid=='MA-CASE-0798' else 'HOLD_FOR_LEGAL_REVIEW'
    assert row['disposition']==expected and row['blocker']
    assert row['author_disposition']=='KEEP' and row['answer_key_assessment']=='CORRECT'
    assert row['independent_legacy_is_canonical_release_evidence'] is False
    assert audit==original
    with pytest.raises(ValueError,match='Uncontained independent finding'):
        validate_default_review_safety([qid],{},[audit])


@pytest.mark.parametrize('previous',['HOLD','HOLD_FOR_LEGAL_REVIEW','HOLD_SOURCE_RELATIONSHIP','DELETE','REPLACE','MAJOR_REWRITE'])
def test_later_supported_opinion_cannot_clear_a_previous_unchanged_content_failure(previous):
    audit=copy.deepcopy(record('MA-CASE-0812'))
    audit['legal_review'].update(verdict='KEEP',blocker=None)
    row=dict(question_id=audit['question_id'],disposition=previous,blocker='existing unresolved finding',answer_key_assessment='CORRECT')
    apply_independent_legacy_review(row,audit)
    assert row['disposition']==previous and row['blocker']=='existing unresolved finding'


def test_incomplete_realism_review_cannot_become_a_default_pass():
    audit=copy.deepcopy(record('MA-CASE-0812'));audit['legal_review']['verdict']='KEEP'
    audit['realism_review']['verdict']='NOT_ASSESSED'
    row=dict(question_id=audit['question_id'],disposition='KEEP',blocker=None,answer_key_assessment='CORRECT')
    apply_independent_legacy_review(row,audit)
    assert row['disposition']=='HOLD'
    with pytest.raises(ValueError,match='Uncontained independent finding'):
        validate_default_review_safety([audit['question_id']],{},[audit])


def test_actual_editorial_hold_survives_later_positive_independent_opinion_in_final_ledger():
    payload=build()[OUT/'question-ledger.jsonl']
    rows={r['question_id']:r for r in map(json.loads,payload.splitlines())}
    row=rows['MA-CASE-0781']
    assert row['independent_legacy_legal_assessment']['verdict']=='KEEP'
    assert row['independent_legacy_realism_assessment']['verdict']=='PASS'
    assert row['disposition']=='HOLD'
    assert row['implementation_status']=='HELD_FROM_DEFAULT_PRESERVED_IN_ARCHIVE'
    selection=json.loads((ROOT/'practice_expansion/2026-10-28-representative/selection.json').read_bytes())
    original=next(h for h in selection['holds'] if h['legacy_question_id']=='MA-CASE-0781')
    assert row['default_practice_hold']==original and row['blocker']==original['reason']
    assert row['disposition_before_default_hold']=='KEEP'
    assert row['independent_legacy_is_canonical_release_evidence'] is False
