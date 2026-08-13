from __future__ import annotations

import json
from copy import deepcopy


def legal_audit() -> dict:
    question_ids = [f"MA-Q-{index:04d}" for index in range(1, 31)]
    results = [
        {
            "Question_ID": question_id,
            "Verdict": "KEEP",
            "Severity": "Low",
            "Existing_Answer_Correct": "YES",
            "Authority": "Test authority",
            "Exact_Section": "1.1",
            "Official_URL": "https://example.gov/rule",
            "Law_Checked_Date": "2026-08-13",
            "Problem": "",
            "Proposed_Answer": "",
            "Proposed_Rewrite": "",
            "Proposed_Explanation": "",
        }
        for question_id in question_ids
    ]
    return {
        "audit_id": "AUDIT-GPT-LEGAL-TEST",
        "auditor": "GPT",
        "audit_date": "2026-08-13",
        "review_type": "LEGAL_VERIFICATION",
        "independent": True,
        "audit_status": "FULLY_ADJUDICATED",
        "question_ids": question_ids,
        "question_hashes": {question_id: "a" * 64 for question_id in question_ids},
        "results": results,
    }


def run_audit_validation(tmp_path, monkeypatch, audit: dict):
    import validate_audits as module

    directory = tmp_path / "data" / "audits"
    directory.mkdir(parents=True)
    (directory / "audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    monkeypatch.setattr(module, "DATA", tmp_path / "data")
    return module.validate_audits(set(audit["question_ids"]) | {"MA-Q-9999"})[0]


def test_audit_result_set_mismatch_fails(tmp_path, monkeypatch) -> None:
    audit = legal_audit()
    audit["results"][-1]["Question_ID"] = "MA-Q-9999"
    report = run_audit_validation(tmp_path, monkeypatch, audit)
    assert any("sets must match exactly" in error for error in report.errors)


def test_duplicate_audit_question_id_fails(tmp_path, monkeypatch) -> None:
    audit = legal_audit()
    audit["results"][-1]["Question_ID"] = audit["results"][0]["Question_ID"]
    report = run_audit_validation(tmp_path, monkeypatch, audit)
    assert any("duplicate Question_ID" in error for error in report.errors)


def test_fully_adjudicated_legal_fields_are_required(tmp_path, monkeypatch) -> None:
    audit = legal_audit()
    result = audit["results"][0]
    result["Existing_Answer_Correct"] = "NOT_ASSESSED"
    result["Law_Checked_Date"] = None
    result["Exact_Section"] = ""
    result["Authority"] = ""
    result["Official_URL"] = "not-a-url"
    report = run_audit_validation(tmp_path, monkeypatch, audit)
    assert any("answer was not assessed" in error for error in report.errors)
    assert any("lacks Law_Checked_Date" in error for error in report.errors)
    assert any("lacks Exact_Section" in error for error in report.errors)
    assert any("lacks Authority" in error for error in report.errors)
    assert any("invalid Official_URL" in error for error in report.errors)


def test_structural_triage_may_leave_legal_fields_unassessed(tmp_path, monkeypatch) -> None:
    audit = legal_audit()
    audit["audit_status"] = "STRUCTURAL_TRIAGE_ONLY"
    for result in audit["results"]:
        result["Existing_Answer_Correct"] = "NOT_ASSESSED"
        result["Law_Checked_Date"] = None
        result["Exact_Section"] = ""
        result["Authority"] = ""
        result["Official_URL"] = ""
    report = run_audit_validation(tmp_path, monkeypatch, audit)
    assert report.errors == []
