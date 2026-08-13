from __future__ import annotations

import json


def authority() -> dict:
    return {
        "authority": "21 CFR 1306.22",
        "source_type": "FEDERAL_REGULATION",
        "exact_section": "1306.22(a)",
        "official_url": "https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.22",
        "law_checked_date": "2026-08-13",
    }


def legal_audit(count: int = 30, scope: str = "INITIAL_BATCH") -> dict:
    question_ids = [f"MA-Q-{index:04d}" for index in range(1, count + 1)]
    results = [
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
    ]
    return {
        "audit_id": "AUDIT-GPT-LEGAL-TEST",
        "auditor": "GPT",
        "audit_date": "2026-08-13",
        "audit_scope": scope,
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


def test_fully_adjudicated_authorities_are_strict(tmp_path, monkeypatch) -> None:
    audit = legal_audit()
    result = audit["results"][0]
    result["Existing_Answer_Correct"] = "NOT_ASSESSED"
    result["authorities"] = [
        {
            "authority": "",
            "source_type": "FEDERAL_REGULATION",
            "exact_section": "",
            "official_url": "not-a-url",
            "law_checked_date": None,
        }
    ]
    report = run_audit_validation(tmp_path, monkeypatch, audit)
    assert any("answer was not assessed" in error for error in report.errors)
    assert any("lacks law_checked_date" in error for error in report.errors)
    assert any("lacks exact_section" in error for error in report.errors)
    assert any("lacks authority" in error for error in report.errors)
    assert any("invalid official_url" in error for error in report.errors)


def test_multiple_official_authorities_pass(tmp_path, monkeypatch) -> None:
    audit = legal_audit()
    second = authority()
    second.update(
        {
            "authority": "M.G.L. c.94C",
            "source_type": "MA_STATUTE",
            "exact_section": "18",
            "official_url": "https://www.mass.gov/info-details/mass-general-laws-c94c-ss-18",
        }
    )
    audit["results"][0]["authorities"].append(second)
    report = run_audit_validation(tmp_path, monkeypatch, audit)
    assert report.errors == []


def test_structural_triage_may_leave_legal_fields_unassessed(tmp_path, monkeypatch) -> None:
    audit = legal_audit()
    audit["audit_status"] = "STRUCTURAL_TRIAGE_ONLY"
    for result in audit["results"]:
        result["Existing_Answer_Correct"] = "NOT_ASSESSED"
        result["authorities"] = []
    report = run_audit_validation(tmp_path, monkeypatch, audit)
    assert report.errors == []


def test_reaudit_allows_one_question(tmp_path, monkeypatch) -> None:
    report = run_audit_validation(tmp_path, monkeypatch, legal_audit(1, "REAUDIT"))
    assert report.errors == []


def test_initial_batch_rejects_fewer_than_thirty_questions(tmp_path, monkeypatch) -> None:
    report = run_audit_validation(tmp_path, monkeypatch, legal_audit(29, "INITIAL_BATCH"))
    assert any("too short" in error or "30" in error for error in report.errors)
