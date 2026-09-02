from __future__ import annotations

import hashlib
import json
from pathlib import Path

from qa_common import load_json, load_records, question_audit_hash
from study_guide_common import study_guide_content_hash


def test_study_guide_pilot_freeze_is_exact_and_has_no_controller_verdicts(root: Path) -> None:
    directory = root / "audits" / "study_guide" / "2026-09-01"
    package = load_json(directory / "BATCH4-SG-PILOT-V1-AUDIT-PACKAGE.json")
    manifest = load_json(directory / "BATCH4-SG-PILOT-V1-FREEZE-MANIFEST.json")
    sections = {record["section_id"]: record for _, record in load_records(root / "data" / "study_guide" / "sections")}
    questions = {record["question_id"]: record for _, record in load_records(root / "data" / "questions")}

    assert package["independent"] is True
    assert package["author_is_not_auditor"] is True
    assert package["auditor_instance_reserved"] == "GPT-FRESH-B4-SG-PILOT-V1"
    assert len(package["sections"]) == 5
    assert set(package["section_ids"]) == set(sections)
    revised_section_ids = {
        "SG-CII-LIFECYCLE",
        "SG-CIII-V-REFILL-TRANSFER",
        "SG-MA-SCHEDULE-VI",
        "SG-FED-MA-INTERACTION",
    }
    for frozen in package["sections"]:
        section = frozen["full_prose_under_review"]
        current = sections[frozen["section_id"]]
        assert frozen["content_hash"] == study_guide_content_hash(section)
        if frozen["section_id"] == "SG-CONTROLLED-SCHEDULES":
            assert frozen["content_hash"] == study_guide_content_hash(current)
            assert current["verification_status"] == "VERIFIED"
            assert current["independent_audit_id"] == "AUDIT-SG-GPT-FRESH-B4-SG-PILOT-V1"
        else:
            assert frozen["section_id"] in revised_section_ids
            assert frozen["content_hash"] != study_guide_content_hash(current)
            assert current["verification_status"] == "AUDIT_PENDING"
            assert current["independent_audit_id"] is None
        assert {item["rule_id"] for item in frozen["rule_dependencies"]} == set(section["rule_ids"])
        assert {item["question_id"] for item in frozen["practice_question_dependencies"]} == set(
            section["practice_question_ids"]
        )
        for item in frozen["practice_question_dependencies"]:
            assert item["question_hash"] == question_audit_hash(questions[item["question_id"]])

    package_bytes = (directory / "BATCH4-SG-PILOT-V1-AUDIT-PACKAGE.json").read_bytes().replace(b"\r\n", b"\n")
    assert manifest["audit_package_sha256"] == hashlib.sha256(package_bytes).hexdigest()
    package_text = json.dumps(package, ensure_ascii=False).lower()
    assert "expected_verdict" not in package_text
    assert "repair_hint" not in package_text
