from __future__ import annotations

import json

from jsonschema import Draft202012Validator, FormatChecker

from qa_common import DATA, ROOT, load_json, load_records, question_audit_hash


def _pr10_records(review_code: str) -> list[dict]:
    records: list[dict] = []
    pattern = f"AUDIT-GPT-PHASE2-*-{review_code}-REAUDIT-2026-08-13.json"
    for path in sorted((DATA / "audits").glob(pattern)):
        records.append(load_json(path))
    return records


def _scope_and_hashes() -> tuple[set[str], dict[str, str]]:
    legal_records = _pr10_records("LEGAL")
    realism_records = _pr10_records("REALISM")
    legal_non_keep = {
        result["Question_ID"]
        for record in legal_records
        for result in record["results"]
        if result["Verdict"] != "KEEP"
    }
    realism_fail = {
        result["Question_ID"]
        for record in realism_records
        for result in record["results"]
        if result["Realism_Verdict"] == "FAIL"
    }
    hashes: dict[str, str] = {}
    for record in legal_records + realism_records:
        for qid, value in record["question_hashes"].items():
            assert qid not in hashes or hashes[qid] == value
            hashes[qid] = value
    return legal_non_keep | realism_fail, hashes


def test_v3_changes_exact_pr10_union_and_preserves_other_hashes() -> None:
    scope, frozen_hashes = _scope_and_hashes()
    questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}
    assert len(scope) == 52
    assert len(frozen_hashes) == 80
    assert {qid for qid in frozen_hashes if question_audit_hash(questions[qid]) != frozen_hashes[qid]} == scope
    assert all(
        question_audit_hash(questions[qid]) == frozen_hashes[qid]
        for qid in set(frozen_hashes) - scope
    )


def test_v3_changed_questions_remove_reviewed_templates() -> None:
    scope, _ = _scope_and_hashes()
    questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}
    forbidden = (
        "would apply if",
        "predicate is missing",
        "if its alternate trigger",
        "after documenting whether",
        "On this record",
        "For this scenario",
        "Under these facts",
        "At this stage",
        "Given the described event",
        "canonical rules",
    )
    for qid in scope:
        text = json.dumps(questions[qid], ensure_ascii=False)
        assert not any(fragment in text for fragment in forbidden), qid


def test_v3_high_risk_legal_repairs_are_explicit() -> None:
    questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}

    q23 = questions["MA-Q-0023"]
    assert "FED-CII-EMERGENCY-FOLLOWUP" in q23["rule_ids"]
    assert "within seven days" in " ".join(q23["explanation"]["related_facts"]).casefold()

    q24_facts = " ".join(questions["MA-Q-0024"]["explanation"]["related_facts"])
    assert "generic buprenorphine sublingual tablets" in q24_facts
    assert "Subutex brand product is discontinued" in q24_facts

    q43 = questions["MA-Q-0043"]
    assert q43["choices"][1]["text"].startswith("A non-opioid Schedule III prescription may qualify")
    assert "required to be considered" not in q43["choices"][1]["text"]

    q58_text = json.dumps(questions["MA-Q-0058"], ensure_ascii=False)
    assert "one business day" in q58_text
    assert "45 calendar days" in q58_text

    q81_text = json.dumps(questions["MA-Q-0081"], ensure_ascii=False)
    for required in (
        "$1,000,000",
        "five years",
        "pre-July 2017 PharmD grandfather",
        "Board-equivalent education/residency pathway",
        "five additional related CE contact hours",
        "controlled-substance registration",
        "MassHealth participation attestation",
    ):
        assert required in q81_text


def test_v3_reaudit_packages_are_schema_valid_and_changed_only() -> None:
    scope, _ = _scope_and_hashes()
    schema = load_json(ROOT / "schemas" / "audit.schema.json")
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    package_paths = sorted((ROOT / "audits" / "reaudit" / "2026-08-13").glob("GPT-V3-*.json"))
    assert len(package_paths) == 4
    coverage = {"LEGAL_VERIFICATION": set(), "REALISM_REVIEW": set()}
    for path in package_paths:
        package = load_json(path)
        assert not list(validator.iter_errors(package)), path
        assert package["audit_status"] == "STRUCTURAL_TRIAGE_ONLY"
        assert 1 <= len(package["question_ids"]) <= 40
        assert set(package["question_ids"]) == set(package["question_hashes"])
        assert set(package["question_ids"]) == {result["Question_ID"] for result in package["results"]}
        assert set(package["question_ids"]) <= scope
        coverage[package["review_type"]].update(package["question_ids"])
    assert coverage == {"LEGAL_VERIFICATION": scope, "REALISM_REVIEW": scope}
