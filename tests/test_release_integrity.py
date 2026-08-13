from __future__ import annotations

from copy import deepcopy

import pytest

from conftest import write_question
from qa_common import dependency_snapshot, question_audit_hash, semantic_content_hash


def release_fixture(question: dict, rules: dict, drugs: dict) -> tuple[dict, dict]:
    question = deepcopy(question)
    question.update(
        {
            "verification_status": "RELEASED",
            "lifecycle_status": "RELEASED",
            "audits": ["AUDIT-GPT-LEGAL-TEST", "AUDIT-CLAUDE-REALISM-TEST"],
            "duplicate_review_status": "CLEAR",
            "independent_audit_status": "PASSED",
            "realism": {
                "profile_id": "MPJE-MA-PRE2027",
                "score": 4,
                "scenario_realism": 4,
                "distractor_quality": 4,
                "multi_rule_reasoning": 4,
                "wording_naturalness": 4,
                "reviewer": "Test Reviewer",
                "reviewed_date": "2026-08-13",
                "notes": "Synthetic release-gate fixture.",
            },
            "final_adjudication": {
                "decision": "KEEP",
                "adjudicator": "Test Editor",
                "date": "2026-08-13",
                "notes": "Synthetic release-gate fixture.",
                "verified_dependencies": {
                    "rules": {rule_id: dependency_snapshot(rules[rule_id]) for rule_id in question["rule_ids"]},
                    "drugs": {drug_id: dependency_snapshot(drugs[drug_id]) for drug_id in question["drug_ids"]},
                },
            },
        }
    )
    content_hash = question_audit_hash(question)
    audits = {
        "AUDIT-GPT-LEGAL-TEST": {
            "audit_id": "AUDIT-GPT-LEGAL-TEST",
            "independent": True,
            "audit_status": "FULLY_ADJUDICATED",
            "review_type": "LEGAL_VERIFICATION",
            "question_ids": [question["question_id"]],
            "question_hashes": {question["question_id"]: content_hash},
            "results": [
                {
                    "Question_ID": question["question_id"],
                    "Verdict": "KEEP",
                    "Existing_Answer_Correct": "YES",
                }
            ],
        },
        "AUDIT-CLAUDE-REALISM-TEST": {
            "audit_id": "AUDIT-CLAUDE-REALISM-TEST",
            "independent": True,
            "audit_status": "FULLY_ADJUDICATED",
            "review_type": "REALISM_REVIEW",
            "question_ids": [question["question_id"]],
            "question_hashes": {question["question_id"]: content_hash},
            "results": [
                {
                    "Question_ID": question["question_id"],
                    "Verdict": "KEEP",
                    "Realism_Verdict": "PASS",
                    "Profile_ID": "MPJE-MA-PRE2027",
                }
            ],
        },
    }
    return question, audits


def run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits):
    import validate_questions as module

    temp_data = tmp_path / "data"
    write_question(temp_data, question)
    monkeypatch.setattr(module, "DATA", temp_data)
    return module.validate_questions(rules, drugs, audits)[0]


def test_fully_gated_release_fixture_passes(tmp_path, monkeypatch, canonical_question, registry_indexes) -> None:
    rules, drugs = registry_indexes
    question, audits = release_fixture(canonical_question, rules, drugs)
    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert report.errors == []


def test_changed_rule_hash_invalidates_released_question(
    tmp_path, monkeypatch, canonical_question, registry_indexes
) -> None:
    rules, drugs = registry_indexes
    question, audits = release_fixture(canonical_question, rules, drugs)
    rule = rules[question["rule_ids"][0]]
    rule["rule_summary"] += " Material legal change."
    rule["content_version"] += 1
    rule["content_hash"] = semantic_content_hash(rule, "rule")
    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert any("adjudicated dependency versions/hashes" in error for error in report.errors)


def test_changed_drug_hash_invalidates_released_question(
    tmp_path, monkeypatch, canonical_question, registry_indexes
) -> None:
    rules, drugs = registry_indexes
    question, audits = release_fixture(canonical_question, rules, drugs)
    drug = drugs[question["drug_ids"][0]]
    drug["therapeutic_class"] += " revised"
    drug["content_version"] += 1
    drug["content_hash"] = semantic_content_hash(drug, "drug")
    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert any("adjudicated dependency versions/hashes" in error for error in report.errors)


@pytest.mark.parametrize("decision", ["DELETE", "MAJOR_REWRITE", "MINOR_EDIT"])
def test_non_keep_final_adjudication_cannot_release(
    tmp_path, monkeypatch, canonical_question, registry_indexes, decision
) -> None:
    rules, drugs = registry_indexes
    question, audits = release_fixture(canonical_question, rules, drugs)
    question["final_adjudication"]["decision"] = decision
    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert any("final adjudication must be KEEP" in error for error in report.errors)


def test_minor_edit_can_release_only_after_re_adjudicated_keep(
    tmp_path, monkeypatch, canonical_question, registry_indexes
) -> None:
    rules, drugs = registry_indexes
    question, audits = release_fixture(canonical_question, rules, drugs)
    question["final_adjudication"]["decision"] = "MINOR_EDIT"
    first = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert first.errors
    question["final_adjudication"]["decision"] = "KEEP"
    second = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert second.errors == []


def test_nonexistent_audit_id_cannot_release(tmp_path, monkeypatch, canonical_question, registry_indexes) -> None:
    rules, drugs = registry_indexes
    question, audits = release_fixture(canonical_question, rules, drugs)
    question["audits"].append("AUDIT-NOT-FOUND")
    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert any("referenced audit does not exist" in error for error in report.errors)


def test_triage_only_audit_cannot_release(tmp_path, monkeypatch, canonical_question, registry_indexes) -> None:
    rules, drugs = registry_indexes
    question, audits = release_fixture(canonical_question, rules, drugs)
    audits["AUDIT-GPT-LEGAL-TEST"]["audit_status"] = "STRUCTURAL_TRIAGE_ONLY"
    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert any("fully adjudicated legal KEEP audit" in error for error in report.errors)


def test_audit_of_old_question_content_cannot_release(
    tmp_path, monkeypatch, canonical_question, registry_indexes
) -> None:
    rules, drugs = registry_indexes
    question, audits = release_fixture(canonical_question, rules, drugs)
    audits["AUDIT-GPT-LEGAL-TEST"]["question_hashes"][question["question_id"]] = "0" * 64
    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert any("not performed on current question content" in error for error in report.errors)


def test_blocked_transitive_drug_rule_prevents_question_release(
    tmp_path, monkeypatch, canonical_question, registry_indexes
) -> None:
    rules, drugs = registry_indexes
    question, audits = release_fixture(canonical_question, rules, drugs)
    transitive_only = "MA-CS-QUANTITY-II-III"
    assert transitive_only not in question["rule_ids"]
    rules[transitive_only]["status"] = "DRAFT"
    rules[transitive_only]["content_version"] += 1
    rules[transitive_only]["content_hash"] = semantic_content_hash(rules[transitive_only], "rule")
    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert any(f"depends on blocked rule {transitive_only}" in error for error in report.errors)
