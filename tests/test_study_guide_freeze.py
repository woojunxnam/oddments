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


def test_study_guide_repair_freeze_binds_only_revised_pending_sections(root: Path) -> None:
    directory = root / "audits" / "study_guide" / "2026-09-02"
    package_path = directory / "BATCH4-SG-REPAIR-V2-AUDIT-PACKAGE.json"
    package = load_json(package_path)
    manifest = load_json(directory / "BATCH4-SG-REPAIR-V2-FREEZE-MANIFEST.json")
    config = load_json(directory / "BATCH4-SG-REPAIR-V2-FREEZE-CONFIG.json")
    sections = {record["section_id"]: record for _, record in load_records(root / "data" / "study_guide" / "sections")}
    expected_hashes = {
        "SG-CII-LIFECYCLE": "76f9c5d5455b60985473779403140fb620f970c4aefb30a427d6e245369a603b",
        "SG-CIII-V-REFILL-TRANSFER": "c988b33e24c6e7f92cf83dc28be23ae8a0159dcb3d66259a171c7ef7cddbbc20",
        "SG-MA-SCHEDULE-VI": "acd8cf4012eaf122517c6c36785e077b5a63a9e13d5eb72e823e9047a8ed61b4",
        "SG-FED-MA-INTERACTION": "36fea844335a78a330d0954b2ea3356a23136a37e39c98a1e7532b5f507c146e",
    }

    assert config["represented_candidate_sha"] == "b2055a91a88ac96474c601365a82347aa24d7009"
    assert package["auditor_instance_reserved"] == "GPT-FRESH-B4-SG-REPAIR-V2"
    assert package["section_ids"] == list(expected_hashes)
    assert manifest["manifest_type"] == "STUDY_GUIDE_REPAIR_CLEAN_FREEZE"
    assert manifest["section_hashes"] == expected_hashes
    for frozen in package["sections"]:
        section_id = frozen["section_id"]
        current = sections[section_id]
        assert frozen["content_hash"] == expected_hashes[section_id]
        assert study_guide_content_hash(frozen["full_prose_under_review"]) == expected_hashes[section_id]
        # The V2 freeze is historical provenance: REPAIR-V3 moved every section past
        # the audited hash, so its MINOR_EDIT dispositions bind none of the current prose.
        assert study_guide_content_hash(current) != expected_hashes[section_id]
        assert current["verification_status"] == "AUDIT_PENDING"
        assert current["independent_audit_id"] is None

    package_bytes = package_path.read_bytes().replace(b"\r\n", b"\n")
    assert manifest["audit_package_sha256"] == hashlib.sha256(package_bytes).hexdigest()
    package_text = json.dumps(package, ensure_ascii=False).lower()
    assert "expected_verdict" not in package_text
    assert "repair_hint" not in package_text


def test_study_guide_repair_v3_freeze_binds_current_pending_sections(root: Path) -> None:
    directory = root / "audits" / "study_guide" / "2026-09-04"
    package_path = directory / "BATCH4-SG-REPAIR-V3-AUDIT-PACKAGE.json"
    package = load_json(package_path)
    manifest = load_json(directory / "BATCH4-SG-REPAIR-V3-FREEZE-MANIFEST.json")
    config = load_json(directory / "BATCH4-SG-REPAIR-V3-FREEZE-CONFIG.json")
    sections = {record["section_id"]: record for _, record in load_records(root / "data" / "study_guide" / "sections")}
    questions = {record["question_id"]: record for _, record in load_records(root / "data" / "questions")}
    rules = {record["rule_id"]: record for _, record in load_records(root / "data" / "rules")}
    revised_section_ids = [
        "SG-CII-LIFECYCLE",
        "SG-CIII-V-REFILL-TRANSFER",
        "SG-MA-SCHEDULE-VI",
        "SG-FED-MA-INTERACTION",
    ]

    assert package["auditor_instance_reserved"] == "GPT-FRESH-B4-SG-REPAIR-V3"
    assert package["independent"] is True
    assert package["author_is_not_auditor"] is True
    assert package["section_ids"] == revised_section_ids
    assert manifest["manifest_type"] == "STUDY_GUIDE_REPAIR_CLEAN_FREEZE"
    assert config["represented_candidate_sha"] == package["represented_candidate_sha"]

    for frozen in package["sections"]:
        section_id = frozen["section_id"]
        current = sections[section_id]
        assert frozen["content_version"] == 3
        assert frozen["content_hash"] == current["content_hash"]
        assert study_guide_content_hash(frozen["full_prose_under_review"]) == frozen["content_hash"]
        assert study_guide_content_hash(current) == frozen["content_hash"]
        assert manifest["section_hashes"][section_id] == frozen["content_hash"]
        assert current["verification_status"] == "AUDIT_PENDING"
        assert current["independent_audit_id"] is None
        for dependency in frozen["rule_dependencies"]:
            rule = rules[dependency["rule_id"]]
            assert dependency["content_version"] == rule["content_version"]
            assert dependency["content_hash"] == rule["content_hash"]
        for dependency in frozen["practice_question_dependencies"]:
            assert dependency["lifecycle_status"] == "RELEASED"
            assert dependency["question_hash"] == question_audit_hash(questions[dependency["question_id"]])

    package_bytes = package_path.read_bytes().replace(b"\r\n", b"\n")
    assert manifest["audit_package_sha256"] == hashlib.sha256(package_bytes).hexdigest()

    # The V2 audit is bound as historical provenance in the manifest only. It must not
    # reach the auditor package, or the V3 auditor inherits the prior findings.
    prior = manifest["prior_audit_reference"]
    assert prior["auditor_instance"] == "GPT-FRESH-B4-SG-REPAIR-V2"
    assert prior["reuse_for_repaired_hashes"] is False
    prior_bytes = (root / prior["path"]).read_bytes().replace(b"\r\n", b"\n")
    assert prior["sha256"] == hashlib.sha256(prior_bytes).hexdigest()
    package_text = json.dumps(package, ensure_ascii=False).lower()
    assert "expected_verdict" not in package_text
    assert "repair_hint" not in package_text
    assert "gpt-fresh-b4-sg-repair-v2" not in package_text
    assert "verification_notes" not in package_text
