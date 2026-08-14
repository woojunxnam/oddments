from __future__ import annotations

from copy import deepcopy

import pytest

from conftest import ROOT, write_question
from qa_common import dependency_snapshot, load_json, question_audit_hash, semantic_content_hash
from release_context import named_dependency_snapshot, style_profile_snapshot


def release_context() -> tuple[dict, dict, dict]:
    requirements = load_json(ROOT / "data" / "release_requirements.json")
    blueprint = load_json(ROOT / "data" / "blueprint.json")
    profile = load_json(ROOT / "data" / "exam_style" / "mpje_style_profile.json")
    return requirements, blueprint, profile


def release_fixture(question: dict, rules: dict, drugs: dict) -> tuple[dict, dict]:
    requirements, blueprint, profile = release_context()
    question = deepcopy(question)
    audit_ids = ["AUDIT-GPT-LEGAL-TEST", "AUDIT-GPT-REALISM-TEST"]
    question.update(
        {
            "verification_status": "RELEASED",
            "lifecycle_status": "RELEASED",
            "audits": audit_ids,
            "duplicate_review_status": "CLEAR",
            "independent_audit_status": "PASSED",
            "final_adjudication": {
                "decision": "KEEP",
                "adjudicator": "Test Editor",
                "date": "2026-08-13",
                "notes": "Synthetic release-gate fixture.",
                "verified_dependencies": {
                    "rules": {rule_id: dependency_snapshot(rules[rule_id]) for rule_id in question["rule_ids"]},
                    "drugs": {drug_id: dependency_snapshot(drugs[drug_id]) for drug_id in question["drug_ids"]},
                    "blueprint": named_dependency_snapshot(blueprint, "blueprint_id"),
                    "style_profile": named_dependency_snapshot(profile, "profile_id"),
                },
            },
        }
    )
    content_hash = question_audit_hash(question)

    legal = {
        "audit_id": audit_ids[0],
        "auditor": "GPT",
        "auditor_instance": "GPT-TEST-A",
        "audit_scope": "INITIAL_BATCH",
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
    }
    realism = {
        "audit_id": audit_ids[1],
        "auditor": "GPT",
        "auditor_instance": "GPT-TEST-A",
        "audit_scope": "REAUDIT",
        "independent": True,
        "audit_status": "FULLY_ADJUDICATED",
        "review_type": "REALISM_REVIEW",
        "style_profile": style_profile_snapshot(profile),
        "question_ids": [question["question_id"]],
        "question_hashes": {question["question_id"]: content_hash},
        "results": [
            {
                "Question_ID": question["question_id"],
                "Verdict": "KEEP",
                "Realism_Verdict": "PASS",
            }
        ],
    }
    return question, {audit_ids[0]: legal, audit_ids[1]: realism}


def run_release_validation(
    tmp_path,
    monkeypatch,
    question,
    rules,
    drugs,
    audits,
    context_override: tuple[dict, dict, dict] | None = None,
):
    import validate_questions as module

    temp_data = tmp_path / "data"
    write_question(temp_data, question)
    monkeypatch.setattr(module, "DATA", temp_data)
    requirements, blueprint, profile = context_override or release_context()
    return module.validate_questions(rules, drugs, audits, requirements, blueprint, profile)[0]


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


@pytest.mark.parametrize("dependency", ["blueprint", "style_profile"])
def test_changed_release_context_hash_invalidates_released_question(
    tmp_path, monkeypatch, canonical_question, registry_indexes, dependency
) -> None:
    rules, drugs = registry_indexes
    question, audits = release_fixture(canonical_question, rules, drugs)
    requirements, blueprint, profile = release_context()
    record = blueprint if dependency == "blueprint" else profile
    record["content_version"] += 1
    record["content_hash"] = "f" * 64
    report = run_release_validation(
        tmp_path,
        monkeypatch,
        question,
        rules,
        drugs,
        audits,
        (requirements, blueprint, profile),
    )
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
    assert run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits).errors
    question["final_adjudication"]["decision"] = "KEEP"
    assert run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits).errors == []


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
    assert any("insufficient current independent legal audit passes" in error for error in report.errors)


def test_stale_current_legal_audit_cannot_release(
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


def test_one_current_legal_pass_is_sufficient(
    tmp_path, monkeypatch, canonical_question, registry_indexes
) -> None:
    rules, drugs = registry_indexes
    question, audits = release_fixture(canonical_question, rules, drugs)
    legal = [audit for audit in audits.values() if audit["review_type"] == "LEGAL_VERIFICATION"]
    assert len(legal) == 1
    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert report.errors == []


def test_same_independent_instance_can_supply_legal_and_realism(
    tmp_path, monkeypatch, canonical_question, registry_indexes
) -> None:
    rules, drugs = registry_indexes
    question, audits = release_fixture(canonical_question, rules, drugs)
    assert audits["AUDIT-GPT-LEGAL-TEST"]["auditor_instance"] == audits["AUDIT-GPT-REALISM-TEST"]["auditor_instance"]
    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert report.errors == []


@pytest.mark.parametrize(
    ("field", "value"),
    [("Verdict", "MAJOR_REWRITE"), ("Existing_Answer_Correct", "NO")],
)
def test_current_legal_failure_blocks_release(
    tmp_path, monkeypatch, canonical_question, registry_indexes, field, value
) -> None:
    rules, drugs = registry_indexes
    question, audits = release_fixture(canonical_question, rules, drugs)
    audits["AUDIT-GPT-LEGAL-TEST"]["results"][0][field] = value
    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert any("does not independently pass" in error for error in report.errors)


def test_current_realism_failure_blocks_release(
    tmp_path, monkeypatch, canonical_question, registry_indexes
) -> None:
    rules, drugs = registry_indexes
    question, audits = release_fixture(canonical_question, rules, drugs)
    audits["AUDIT-GPT-REALISM-TEST"]["results"][0]["Realism_Verdict"] = "FAIL"
    audits["AUDIT-GPT-REALISM-TEST"]["results"][0]["Verdict"] = "MAJOR_REWRITE"
    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert any("does not independently pass" in error for error in report.errors)


def test_unreferenced_current_failed_legal_audit_blocks_release(
    tmp_path, monkeypatch, canonical_question, registry_indexes
) -> None:
    rules, drugs = registry_indexes
    question, audits = release_fixture(canonical_question, rules, drugs)
    failed = deepcopy(audits["AUDIT-GPT-LEGAL-TEST"])
    failed["audit_id"] = "AUDIT-HUMAN-LEGAL-FAILED"
    failed["auditor"] = "HUMAN"
    failed["auditor_instance"] = "HUMAN-LEGAL-FAILED"
    failed["results"][0]["Verdict"] = "MAJOR_REWRITE"
    audits[failed["audit_id"]] = failed
    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert any("AUDIT-HUMAN-LEGAL-FAILED" in error for error in report.errors)


def test_reaudit_without_initial_batch_history_cannot_release(
    tmp_path, monkeypatch, canonical_question, registry_indexes
) -> None:
    rules, drugs = registry_indexes
    question, audits = release_fixture(canonical_question, rules, drugs)
    audits["AUDIT-GPT-LEGAL-TEST"]["audit_scope"] = "REAUDIT"
    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert any("lacks valid INITIAL_BATCH audit history" in error for error in report.errors)


def test_stale_realism_profile_snapshot_cannot_release(
    tmp_path, monkeypatch, canonical_question, registry_indexes
) -> None:
    rules, drugs = registry_indexes
    question, audits = release_fixture(canonical_question, rules, drugs)
    audits["AUDIT-GPT-REALISM-TEST"]["style_profile"]["content_hash"] = "0" * 64
    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert any("uses a stale style profile" in error for error in report.errors)
