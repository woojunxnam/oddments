from __future__ import annotations

from copy import deepcopy

from validate_governance import validate_family_matrix


def family(family_id: str, candidates: int, released: int, maximum: int = 2) -> dict:
    return {
        "family_id": family_id,
        "primary_rule_ids": ["FED-CS-SCHEDULES"],
        "secondary_rule_ids": [],
        "current_candidate_count": candidates,
        "current_released_count": released,
        "max_questions_in_final_bank": maximum,
    }


def question(family_id: str, released: bool = False) -> dict:
    status = "RELEASED" if released else "AUDIT_PENDING"
    return {
        "family_id": family_id,
        "verification_status": status,
        "lifecycle_status": status,
    }


def test_zero_question_planned_family_passes(registry_indexes) -> None:
    rules, _ = registry_indexes
    matrix = {"families": [family("ACTUAL", 1, 0), family("PLANNED", 0, 0)]}
    report = validate_family_matrix(matrix, {"Q1": question("ACTUAL")}, rules)
    assert report.errors == []


def test_actual_question_without_matrix_family_fails(registry_indexes) -> None:
    rules, _ = registry_indexes
    report = validate_family_matrix({"families": []}, {"Q1": question("MISSING")}, rules)
    assert any("actual question families missing" in error for error in report.errors)


def test_stale_candidate_count_fails(registry_indexes) -> None:
    rules, _ = registry_indexes
    matrix = {"families": [family("ACTUAL", 0, 0)]}
    report = validate_family_matrix(matrix, {"Q1": question("ACTUAL")}, rules)
    assert any("stale current_candidate_count" in error for error in report.errors)


def test_released_family_over_max_fails(registry_indexes) -> None:
    rules, _ = registry_indexes
    questions = {f"Q{index}": question("ACTUAL", released=True) for index in range(3)}
    matrix = {"families": [family("ACTUAL", 3, 3, maximum=2)]}
    report = validate_family_matrix(matrix, questions, rules)
    assert any("released family ACTUAL exceeds" in error for error in report.errors)


def test_extra_draft_candidates_only_warn(registry_indexes) -> None:
    rules, _ = registry_indexes
    questions = {f"Q{index}": question("ACTUAL") for index in range(4)}
    matrix = {"families": [family("ACTUAL", 4, 0, maximum=2)]}
    report = validate_family_matrix(matrix, questions, rules)
    assert report.errors == []
    assert any("candidate family ACTUAL" in warning for warning in report.warnings)
