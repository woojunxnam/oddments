from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from conftest import write_question


def run_question_validation(tmp_path, monkeypatch, question, registry_indexes):
    import validate_questions as module

    temp_data = tmp_path / "data"
    write_question(temp_data, question)
    monkeypatch.setattr(module, "DATA", temp_data)
    rules, drugs = registry_indexes
    return module.validate_questions(rules, drugs)[0]


def test_blank_answer_rejected(tmp_path, monkeypatch, canonical_question, registry_indexes) -> None:
    question = deepcopy(canonical_question)
    question["correct_choice_ids"] = []
    report = run_question_validation(tmp_path, monkeypatch, question, registry_indexes)
    assert any("missing answer" in error or "non-empty" in error for error in report.errors)


def test_zero_answer_sata_rejected(tmp_path, monkeypatch, canonical_sata, registry_indexes) -> None:
    question = deepcopy(canonical_sata)
    question["correct_choice_ids"] = []
    question["allow_zero_correct"] = False
    report = run_question_validation(tmp_path, monkeypatch, question, registry_indexes)
    assert any("SATA has zero answers" in error for error in report.errors)


@pytest.mark.parametrize("placeholder", ["TODO", "TBD", "FIXME", "{drug_ref(x)}", "{d.indication}"])
def test_placeholder_rejected(tmp_path, monkeypatch, canonical_question, registry_indexes, placeholder) -> None:
    question = deepcopy(canonical_question)
    question["stem"] = f"This sufficiently long fixture contains the forbidden marker {placeholder} and must fail."
    report = run_question_validation(tmp_path, monkeypatch, question, registry_indexes)
    assert any("literal placeholder" in error for error in report.errors)


def test_unknown_drug_id_rejected(tmp_path, monkeypatch, canonical_question, registry_indexes) -> None:
    question = deepcopy(canonical_question)
    question["drug_ids"] = ["not-a-known-drug"]
    report = run_question_validation(tmp_path, monkeypatch, question, registry_indexes)
    assert any("unknown drug_id not-a-known-drug" in error for error in report.errors)


def test_unknown_rule_id_rejected(tmp_path, monkeypatch, canonical_question, registry_indexes) -> None:
    question = deepcopy(canonical_question)
    question["rule_ids"] = ["MA-NOT-A-RULE"]
    report = run_question_validation(tmp_path, monkeypatch, question, registry_indexes)
    assert any("unknown rule_id MA-NOT-A-RULE" in error for error in report.errors)


def test_duplicate_question_ids_rejected(tmp_path, monkeypatch, canonical_question, registry_indexes) -> None:
    import validate_questions as module

    temp_data = tmp_path / "data"
    write_question(temp_data, canonical_question, "first.json")
    write_question(temp_data, canonical_question, "second.json")
    monkeypatch.setattr(module, "DATA", temp_data)
    rules, drugs = registry_indexes
    report, _ = module.validate_questions(rules, drugs)
    assert any("duplicate question_id MA-Q-0001" in error for error in report.errors)


def test_duplicated_choice_explanation_rejected(tmp_path, monkeypatch, canonical_question, registry_indexes) -> None:
    question = deepcopy(canonical_question)
    question["explanation"]["choice_analysis"]["B"] = question["explanation"]["choice_analysis"]["A"]
    report = run_question_validation(tmp_path, monkeypatch, question, registry_indexes)
    assert any("identical choice-analysis" in error for error in report.errors)


def test_released_question_referencing_hold_rule_rejected(
    tmp_path,
    monkeypatch,
    canonical_question,
    registry_indexes,
) -> None:
    import validate_questions as module

    question = deepcopy(canonical_question)
    question.update(
        {
            "verification_status": "RELEASED",
            "lifecycle_status": "RELEASED",
            "duplicate_review_status": "CLEAR",
            "independent_audit_status": "PASSED",
            "final_adjudication": {
                "decision": "KEEP",
                "adjudicator": "Test Editor",
                "date": "2026-08-13",
                "notes": "Test-only adjudication fixture."
            },
        }
    )
    temp_data = tmp_path / "data"
    write_question(temp_data, question)
    monkeypatch.setattr(module, "DATA", temp_data)
    rules, drugs = registry_indexes
    blocked_id = question["rule_ids"][0]
    rules[blocked_id]["verification_status"] = "HOLD"
    report, _ = module.validate_questions(rules, drugs)
    assert any(f"released question references HOLD/unverified rule {blocked_id}" in error for error in report.errors)


def test_released_question_referencing_hold_drug_rejected(
    tmp_path,
    monkeypatch,
    canonical_question,
    registry_indexes,
) -> None:
    import validate_questions as module

    question = deepcopy(canonical_question)
    question.update(
        {
            "verification_status": "RELEASED",
            "lifecycle_status": "RELEASED",
            "duplicate_review_status": "CLEAR",
            "independent_audit_status": "PASSED",
            "final_adjudication": {
                "decision": "KEEP",
                "adjudicator": "Test Editor",
                "date": "2026-08-13",
                "notes": "Test-only adjudication fixture."
            },
        }
    )
    temp_data = tmp_path / "data"
    write_question(temp_data, question)
    monkeypatch.setattr(module, "DATA", temp_data)
    rules, drugs = registry_indexes
    blocked_id = question["drug_ids"][0]
    drugs[blocked_id]["verification_status"] = "HOLD"
    report, _ = module.validate_questions(rules, drugs)
    assert any(f"released question references HOLD/unverified drug {blocked_id}" in error for error in report.errors)

