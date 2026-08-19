from __future__ import annotations

import json
from copy import deepcopy

from conftest import ROOT, write_question
from qa_common import dependency_snapshot, load_json, question_audit_hash
from release_context import named_dependency_snapshot, style_profile_snapshot


T2_IDS = [f"MA-Q-{index:04d}" for index in range(211, 227)]
T2_TRANCHE = "PRE-BATCH3-COVERAGE-T2"
T2_AUTHORIZING_ISSUE = 68
T2_REPRESENTED_CANDIDATE_SHA = "b849159ef18d37618ca6badf886e465502436e1b"


def authority() -> dict:
    return {
        "authority": "21 CFR 1306.22",
        "source_type": "FEDERAL_REGULATION",
        "exact_section": "1306.22(a)",
        "official_url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.22",
        "law_checked_date": "2026-08-13",
    }


def governance_authorization() -> dict:
    return {
        "tranche_id": T2_TRANCHE,
        "authorizing_issue": T2_AUTHORIZING_ISSUE,
        "represented_candidate_sha": T2_REPRESENTED_CANDIDATE_SHA,
        "question_ids": T2_IDS.copy(),
    }


def legal_audit(question_ids: list[str], scope: str) -> dict:
    return {
        "audit_id": "AUDIT-GPT-LEGAL-POLICY-TEST",
        "auditor": "GPT",
        "auditor_instance": "GPT-POLICY-TEST",
        "audit_date": "2026-08-19",
        "audit_scope": scope,
        "review_type": "LEGAL_VERIFICATION",
        "independent": True,
        "audit_status": "FULLY_ADJUDICATED",
        "question_ids": question_ids,
        "question_hashes": {question_id: "a" * 64 for question_id in question_ids},
        "results": [
            {
                "Question_ID": question_id,
                "Verdict": "KEEP",
                "Severity": "Low",
                "Existing_Answer_Correct": "YES",
                "authorities": [authority()],
                "Problem": "",
                "Proposed_Answer": "",
                "Proposed_Rewrite": "",
                "Proposed_Explanation": "",
            }
            for question_id in question_ids
        ],
    }


def targeted_legal_audit() -> dict:
    audit = legal_audit(T2_IDS.copy(), "TARGETED_INITIAL_BATCH")
    audit["audit_id"] = "AUDIT-GPT-TARGETED-T2-TEST"
    audit["governance_authorization"] = governance_authorization()
    return audit


def run_audit_validation(tmp_path, audit: dict):
    import validate_audits as module

    directory = tmp_path / "data" / "audits"
    directory.mkdir(parents=True)
    (directory / "audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    return module.validate_audits(set(audit.get("question_ids", [])), data_root=tmp_path / "data")[0]


def test_ordinary_initial_batch_below_thirty_still_fails(tmp_path) -> None:
    ids = [f"MA-Q-{index:04d}" for index in range(1, 30)]
    report = run_audit_validation(tmp_path, legal_audit(ids, "INITIAL_BATCH"))
    assert report.errors
    assert any("30" in error or "too short" in error for error in report.errors)


def test_ordinary_initial_batch_thirty_remains_accepted(tmp_path) -> None:
    ids = [f"MA-Q-{index:04d}" for index in range(1, 31)]
    report = run_audit_validation(tmp_path, legal_audit(ids, "INITIAL_BATCH"))
    assert report.errors == []


def test_targeted_initial_without_governance_authorization_fails(tmp_path) -> None:
    audit = targeted_legal_audit()
    del audit["governance_authorization"]
    report = run_audit_validation(tmp_path, audit)
    assert any("governance_authorization" in error for error in report.errors)


def test_targeted_initial_authorization_question_set_mismatch_fails(tmp_path) -> None:
    audit = targeted_legal_audit()
    audit["governance_authorization"]["question_ids"][-1] = "MA-Q-9999"
    report = run_audit_validation(tmp_path, audit)
    assert any("question_ids" in error and "exact" in error for error in report.errors)


def test_targeted_initial_malformed_represented_candidate_sha_fails(tmp_path) -> None:
    audit = targeted_legal_audit()
    audit["governance_authorization"]["represented_candidate_sha"] = "B" * 40
    report = run_audit_validation(tmp_path, audit)
    assert any("represented_candidate_sha" in error for error in report.errors)


def test_targeted_initial_exact_governance_metadata_is_required(tmp_path) -> None:
    audit = targeted_legal_audit()
    audit["governance_authorization"]["authorizing_issue"] = 69
    report = run_audit_validation(tmp_path, audit)
    assert any("issue 68" in error for error in report.errors)


def test_correctly_authorized_sixteen_question_targeted_initial_is_accepted(tmp_path) -> None:
    report = run_audit_validation(tmp_path, targeted_legal_audit())
    assert report.errors == []


def release_context() -> tuple[dict, dict, dict]:
    requirements = load_json(ROOT / "data" / "release_requirements.json")
    blueprint = load_json(ROOT / "data" / "blueprint.json")
    profile = load_json(ROOT / "data" / "exam_style" / "mpje_style_profile.json")
    return requirements, blueprint, profile


def t2_release_fixture(question: dict, rules: dict, drugs: dict) -> tuple[dict, dict]:
    requirements, blueprint, profile = release_context()
    question = deepcopy(question)
    question["question_id"] = T2_IDS[0]
    audit_ids = ["AUDIT-GPT-LEGAL-CURRENT-T2-TEST", "AUDIT-GPT-REALISM-CURRENT-T2-TEST"]
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
                "date": "2026-08-19",
                "notes": "Synthetic targeted-initial release-policy fixture.",
                "verified_dependencies": {
                    "rules": {rule_id: dependency_snapshot(rules[rule_id]) for rule_id in question["rule_ids"]},
                    "drugs": {drug_id: dependency_snapshot(drugs[drug_id]) for drug_id in question["drug_ids"]},
                    "blueprint": named_dependency_snapshot(blueprint, "blueprint_id"),
                    "style_profile": named_dependency_snapshot(profile, "profile_id"),
                },
            },
        }
    )
    current_hash = question_audit_hash(question)
    legal = {
        "audit_id": audit_ids[0],
        "auditor": "GPT",
        "auditor_instance": "GPT-T2-CURRENT",
        "audit_scope": "REAUDIT",
        "independent": True,
        "audit_status": "FULLY_ADJUDICATED",
        "review_type": "LEGAL_VERIFICATION",
        "question_ids": [question["question_id"]],
        "question_hashes": {question["question_id"]: current_hash},
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
        "auditor_instance": "GPT-T2-CURRENT",
        "audit_scope": "REAUDIT",
        "independent": True,
        "audit_status": "FULLY_ADJUDICATED",
        "review_type": "REALISM_REVIEW",
        "style_profile": style_profile_snapshot(profile),
        "question_ids": [question["question_id"]],
        "question_hashes": {question["question_id"]: current_hash},
        "results": [
            {
                "Question_ID": question["question_id"],
                "Verdict": "KEEP",
                "Realism_Verdict": "PASS",
            }
        ],
    }
    return question, {legal["audit_id"]: legal, realism["audit_id"]: realism}


def run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits):
    import validate_questions as module

    temp_data = tmp_path / "data"
    write_question(temp_data, question)
    monkeypatch.setattr(module, "DATA", temp_data)
    requirements, blueprint, profile = release_context()
    return module.validate_questions(rules, drugs, audits, requirements, blueprint, profile)[0]


def test_authorized_targeted_initial_can_satisfy_initial_history_presence(
    tmp_path, monkeypatch, canonical_question, registry_indexes
) -> None:
    rules, drugs = registry_indexes
    question, audits = t2_release_fixture(canonical_question, rules, drugs)
    history = targeted_legal_audit()
    audits[history["audit_id"]] = history
    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert report.errors == []


def test_reaudit_only_still_cannot_satisfy_initial_history(
    tmp_path, monkeypatch, canonical_question, registry_indexes
) -> None:
    rules, drugs = registry_indexes
    question, audits = t2_release_fixture(canonical_question, rules, drugs)
    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert any("lacks valid INITIAL_BATCH audit history" in error for error in report.errors)


def test_unauthorized_targeted_initial_cannot_satisfy_initial_history(
    tmp_path, monkeypatch, canonical_question, registry_indexes
) -> None:
    rules, drugs = registry_indexes
    question, audits = t2_release_fixture(canonical_question, rules, drugs)
    history = targeted_legal_audit()
    history["governance_authorization"]["authorizing_issue"] = 69
    audits[history["audit_id"]] = history
    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert any("lacks valid INITIAL_BATCH audit history" in error for error in report.errors)


def test_targeted_history_does_not_replace_current_hash_legal_gate(
    tmp_path, monkeypatch, canonical_question, registry_indexes
) -> None:
    rules, drugs = registry_indexes
    question, audits = t2_release_fixture(canonical_question, rules, drugs)
    history = targeted_legal_audit()
    audits[history["audit_id"]] = history
    audits["AUDIT-GPT-LEGAL-CURRENT-T2-TEST"]["question_hashes"][question["question_id"]] = "0" * 64
    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert any("not performed on current question content" in error for error in report.errors)
    assert any("insufficient current independent legal audit passes" in error for error in report.errors)


def test_targeted_history_does_not_replace_current_hash_realism_gate(
    tmp_path, monkeypatch, canonical_question, registry_indexes
) -> None:
    rules, drugs = registry_indexes
    question, audits = t2_release_fixture(canonical_question, rules, drugs)
    history = targeted_legal_audit()
    audits[history["audit_id"]] = history
    realism = audits["AUDIT-GPT-REALISM-CURRENT-T2-TEST"]
    realism["results"][0]["Verdict"] = "MAJOR_REWRITE"
    realism["results"][0]["Realism_Verdict"] = "FAIL"
    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert any("current realism audit" in error and "does not pass" in error for error in report.errors)


def test_targeted_history_does_not_hide_failed_current_hash_audit(
    tmp_path, monkeypatch, canonical_question, registry_indexes
) -> None:
    rules, drugs = registry_indexes
    question, audits = t2_release_fixture(canonical_question, rules, drugs)
    history = targeted_legal_audit()
    audits[history["audit_id"]] = history
    failed = deepcopy(audits["AUDIT-GPT-LEGAL-CURRENT-T2-TEST"])
    failed["audit_id"] = "AUDIT-HUMAN-LEGAL-CURRENT-T2-FAILED"
    failed["auditor"] = "HUMAN"
    failed["auditor_instance"] = "HUMAN-T2-FAILED"
    failed["results"][0]["Verdict"] = "MAJOR_REWRITE"
    audits[failed["audit_id"]] = failed
    report = run_release_validation(tmp_path, monkeypatch, question, rules, drugs, audits)
    assert any("AUDIT-HUMAN-LEGAL-CURRENT-T2-FAILED" in error for error in report.errors)


def test_q0028_quarantine_state_is_unchanged() -> None:
    question = load_json(ROOT / "data" / "questions" / "ma-q-0028.json")
    assert question["question_id"] == "MA-Q-0028"
    assert question["verification_status"] == "AUDIT_PENDING"
    assert question["lifecycle_status"] == "AUDIT_PENDING"
    assert question["audits"] == []
    assert question["independent_audit_status"] == "PENDING"
    assert question["final_adjudication"] is None
    assert question["development_fixture"] is True


T3_IDS = ["MA-Q-0227", "MA-Q-0228"]
T3_TRANCHE = "PRE-BATCH3-COVERAGE-T3-DIVERSITY"
T3_AUTHORIZING_ISSUE = 86
T3_REPRESENTED_CANDIDATE_SHA = "f13c91c2635ea153a1ea19d9dfb34bcbe12f30c2"


def targeted_t3_legal_audit() -> dict:
    audit = legal_audit(T3_IDS.copy(), "TARGETED_INITIAL_BATCH")
    audit["audit_id"] = "AUDIT-CLAUDE-TARGETED-T3-TEST"
    audit["auditor"] = "CLAUDE"
    audit["auditor_instance"] = "CLAUDE-POLICY-TEST"
    audit["governance_authorization"] = {
        "tranche_id": T3_TRANCHE,
        "authorizing_issue": T3_AUTHORIZING_ISSUE,
        "represented_candidate_sha": T3_REPRESENTED_CANDIDATE_SHA,
        "question_ids": T3_IDS.copy(),
    }
    return audit


def test_authorized_two_question_t3_targeted_initial_is_accepted(tmp_path) -> None:
    report = run_audit_validation(tmp_path, targeted_t3_legal_audit())
    assert report.errors == []


def test_t3_targeted_initial_rejects_wrong_authorizing_issue(tmp_path) -> None:
    audit = targeted_t3_legal_audit()
    audit["governance_authorization"]["authorizing_issue"] = 83
    report = run_audit_validation(tmp_path, audit)
    assert any("issue 86" in error for error in report.errors)


def test_t3_targeted_initial_rejects_wrong_candidate_sha(tmp_path) -> None:
    audit = targeted_t3_legal_audit()
    audit["governance_authorization"]["represented_candidate_sha"] = "0" * 40
    report = run_audit_validation(tmp_path, audit)
    assert any("represented_candidate_sha" in error for error in report.errors)


def test_t3_targeted_initial_rejects_extra_question(tmp_path) -> None:
    audit = targeted_t3_legal_audit()
    audit["question_ids"].append("MA-Q-0229")
    audit["question_hashes"]["MA-Q-0229"] = "b" * 64
    audit["results"].append(dict(audit["results"][0], Question_ID="MA-Q-0229"))
    report = run_audit_validation(tmp_path, audit)
    assert any("question_ids" in error for error in report.errors)


def test_unregistered_tranche_is_still_rejected(tmp_path) -> None:
    audit = targeted_t3_legal_audit()
    audit["governance_authorization"]["tranche_id"] = "PRE-BATCH3-COVERAGE-T9-UNAUTHORIZED"
    report = run_audit_validation(tmp_path, audit)
    assert any("not governance-authorized" in error for error in report.errors)
