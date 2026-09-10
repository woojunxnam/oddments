from __future__ import annotations

import hashlib
import json
from pathlib import Path

from qa_common import load_json, load_records, question_audit_hash
from study_guide_common import study_guide_content_hash


def test_study_guide_pilot_freeze_is_exact_and_has_no_controller_verdicts(root: Path) -> None:
    directory = root / "audits" / "study_guide" / "2026-09-01"
    package = load_json(directory / "BATCH4-SG-PILOT-V1-AUDIT-PACKAGE.json")
    model = package.get("content_model_version", 1)
    manifest = load_json(directory / "BATCH4-SG-PILOT-V1-FREEZE-MANIFEST.json")
    sections = {record["section_id"]: record for _, record in load_records(root / "data" / "study_guide" / "sections")}
    questions = {record["question_id"]: record for _, record in load_records(root / "data" / "questions")}

    assert package["independent"] is True
    assert package["author_is_not_auditor"] is True
    assert package["auditor_instance_reserved"] == "GPT-FRESH-B4-SG-PILOT-V1"
    assert len(package["sections"]) == 5
    # The pilot froze every section that existed then. The guide has grown since, so the
    # freeze covers a subset of the current sections rather than all of them.
    assert set(package["section_ids"]) <= set(sections)
    revised_section_ids = {
        "SG-CII-LIFECYCLE",
        "SG-CIII-V-REFILL-TRANSFER",
        "SG-MA-SCHEDULE-VI",
        "SG-FED-MA-INTERACTION",
    }
    for frozen in package["sections"]:
        section = frozen["full_prose_under_review"]
        current = sections[frozen["section_id"]]
        assert frozen["content_hash"] == study_guide_content_hash(section, model_version=model)
        # The pilot certifies a section only while that section still stands at the exact
        # hash the pilot froze. Every section has since moved -- four were repaired, and
        # SG-CONTROLLED-SCHEDULES was re-authored into the current content model -- so the
        # pilot audit now certifies none of them. What must never happen is a section
        # claiming the pilot as its certifying audit at a hash the pilot never saw.
        assert frozen["section_id"] in revised_section_ids | {"SG-CONTROLLED-SCHEDULES"}
        if current["independent_audit_id"] == "AUDIT-SG-GPT-FRESH-B4-SG-PILOT-V1":
            assert current["content_hash"] == frozen["content_hash"]
            assert current["verification_status"] == "VERIFIED"
        else:
            assert current["verification_status"] != "VERIFIED" or current["independent_audit_id"]
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
    model = package.get("content_model_version", 1)
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
        assert study_guide_content_hash(frozen["full_prose_under_review"], model_version=model) == expected_hashes[section_id]
        # The V2 freeze is historical provenance: REPAIR-V3 moved every section past
        # the audited hash, so its MINOR_EDIT dispositions bind none of the current prose.
        assert study_guide_content_hash(current) != expected_hashes[section_id]
        assert current["independent_audit_id"] != "AUDIT-SG-B4-SG-REPAIR-V2-2026-09-02"

    package_bytes = package_path.read_bytes().replace(b"\r\n", b"\n")
    assert manifest["audit_package_sha256"] == hashlib.sha256(package_bytes).hexdigest()
    package_text = json.dumps(package, ensure_ascii=False).lower()
    assert "expected_verdict" not in package_text
    assert "repair_hint" not in package_text


def test_study_guide_repair_v3_freeze_binds_current_pending_sections(root: Path) -> None:
    directory = root / "audits" / "study_guide" / "2026-09-04"
    package_path = directory / "BATCH4-SG-REPAIR-V3-AUDIT-PACKAGE.json"
    package = load_json(package_path)
    model = package.get("content_model_version", 1)
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

    audit_path = directory / "GPT-FRESH-B4-SG-REPAIR-V3-AUDIT.json"
    v3_results: dict[str, dict] = {}
    if audit_path.is_file():
        audit = load_json(audit_path)
        assert audit["auditor_instance"] == package["auditor_instance_reserved"]
        assert audit["section_ids"] == revised_section_ids
        v3_results = {result["section_id"]: result for result in audit["results"]}

    for frozen in package["sections"]:
        section_id = frozen["section_id"]
        current = sections[section_id]
        assert frozen["content_version"] == 3
        assert study_guide_content_hash(frozen["full_prose_under_review"], model_version=model) == frozen["content_hash"]
        assert manifest["section_hashes"][section_id] == frozen["content_hash"]
        result = v3_results.get(section_id)

        if study_guide_content_hash(current) != frozen["content_hash"]:
            # A later repair moved this section past the audited hash. Whatever V3 said
            # about it is historical: it must not still be published on that verdict. It
            # may well be published on a later audit's verdict, which is the point of the
            # repair-and-re-audit cycle, so only the V3 certification is ruled out here.
            assert current["content_version"] > frozen["content_version"]
            assert current["independent_audit_id"] != "AUDIT-SG-B4-SG-REPAIR-V3-2026-09-04"
            continue

        # A frozen section still at its audited hash is public only where the V3 audit
        # gave it KEEP with every criterion passing; otherwise it stays private.
        assert frozen["content_hash"] == current["content_hash"]
        if result is not None and result["disposition"] == "KEEP":
            assert result["section_hash"] == frozen["content_hash"]
            assert all(verdict == "PASS" for verdict in result["criteria"].values())
            assert result["practice_mapping_verdict"] == "PASS"
            assert current["verification_status"] == "VERIFIED"
            assert current["independent_audit_id"] == "AUDIT-SG-B4-SG-REPAIR-V3-2026-09-04"
        else:
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


def test_study_guide_repair_v4_freeze_binds_the_two_repaired_sections(root: Path) -> None:
    directory = root / "audits" / "study_guide" / "2026-09-10"
    package_path = directory / "BATCH4-SG-REPAIR-V4-AUDIT-PACKAGE.json"
    package = load_json(package_path)
    model = package.get("content_model_version", 1)
    manifest = load_json(directory / "BATCH4-SG-REPAIR-V4-FREEZE-MANIFEST.json")
    config = load_json(directory / "BATCH4-SG-REPAIR-V4-FREEZE-CONFIG.json")
    sections = {record["section_id"]: record for _, record in load_records(root / "data" / "study_guide" / "sections")}
    questions = {record["question_id"]: record for _, record in load_records(root / "data" / "questions")}
    rules = {record["rule_id"]: record for _, record in load_records(root / "data" / "rules")}
    repaired = ["SG-CIII-V-REFILL-TRANSFER", "SG-MA-SCHEDULE-VI"]

    assert package["auditor_instance_reserved"] == "GPT-FRESH-B4-SG-REPAIR-V4"
    assert package["independent"] is True
    assert package["author_is_not_auditor"] is True
    assert package["section_ids"] == repaired
    assert config["represented_candidate_sha"] == package["represented_candidate_sha"]
    # SG-CII-LIFECYCLE is pending too, but carries an unrepaired MAJOR_REWRITE and is
    # deliberately out of this cycle.
    assert "SG-CII-LIFECYCLE" not in package["section_ids"]
    assert sections["SG-CII-LIFECYCLE"]["verification_status"] == "AUDIT_PENDING"

    audit_path = directory / "GPT-FRESH-B4-SG-REPAIR-V4-AUDIT.json"
    v4_results: dict[str, dict] = {}
    if audit_path.is_file():
        audit = load_json(audit_path)
        assert audit["auditor_instance"] == package["auditor_instance_reserved"]
        v4_results = {result["section_id"]: result for result in audit["results"]}

    for frozen in package["sections"]:
        section_id = frozen["section_id"]
        current = sections[section_id]
        assert frozen["content_version"] == 4
        assert study_guide_content_hash(frozen["full_prose_under_review"], model_version=model) == frozen["content_hash"]
        assert manifest["section_hashes"][section_id] == frozen["content_hash"]

        if study_guide_content_hash(current) != frozen["content_hash"]:
            # Moved past the audited hash. A later audit may have published it since; only
            # certification by this audit is ruled out.
            assert current["content_version"] > frozen["content_version"]
            assert current["independent_audit_id"] != "AUDIT-SG-B4-SG-REPAIR-V4-2026-09-10"
            continue

        result = v4_results.get(section_id)
        if result is not None and result["disposition"] == "KEEP":
            assert result["section_hash"] == frozen["content_hash"]
            assert all(verdict == "PASS" for verdict in result["criteria"].values())
            assert result["practice_mapping_verdict"] == "PASS"
            assert current["verification_status"] == "VERIFIED"
            assert current["independent_audit_id"] == "AUDIT-SG-B4-SG-REPAIR-V4-2026-09-10"
        else:
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

    prior = manifest["prior_audit_reference"]
    assert prior["auditor_instance"] == "GPT-FRESH-B4-SG-REPAIR-V3"
    assert prior["reuse_for_repaired_hashes"] is False
    prior_bytes = (root / prior["path"]).read_bytes().replace(b"\r\n", b"\n")
    assert prior["sha256"] == hashlib.sha256(prior_bytes).hexdigest()
    package_text = json.dumps(package, ensure_ascii=False).lower()
    assert "expected_verdict" not in package_text
    assert "repair_hint" not in package_text
    assert "gpt-fresh-b4-sg-repair-v3" not in package_text
    assert "verification_notes" not in package_text


def test_study_guide_repair_v5_freeze_binds_the_three_repaired_sections(root: Path) -> None:
    directory = root / "audits" / "study_guide" / "2026-09-10"
    package_path = directory / "BATCH4-SG-REPAIR-V5-AUDIT-PACKAGE.json"
    package = load_json(package_path)
    model = package.get("content_model_version", 1)
    manifest = load_json(directory / "BATCH4-SG-REPAIR-V5-FREEZE-MANIFEST.json")
    config = load_json(directory / "BATCH4-SG-REPAIR-V5-FREEZE-CONFIG.json")
    sections = {record["section_id"]: record for _, record in load_records(root / "data" / "study_guide" / "sections")}
    questions = {record["question_id"]: record for _, record in load_records(root / "data" / "questions")}
    rules = {record["rule_id"]: record for _, record in load_records(root / "data" / "rules")}
    frozen_ids = ["SG-CIII-V-REFILL-TRANSFER", "SG-MA-SCHEDULE-VI", "SG-MA-ORAL-PRESCRIPTIONS"]

    assert package["auditor_instance_reserved"] == "GPT-FRESH-B4-SG-REPAIR-V5"
    assert package["independent"] is True
    assert package["author_is_not_auditor"] is True
    assert package["section_ids"] == frozen_ids
    assert config["represented_candidate_sha"] == package["represented_candidate_sha"]
    # SG-CII-LIFECYCLE carries an unrepaired MAJOR_REWRITE and is deliberately out of scope.
    assert "SG-CII-LIFECYCLE" not in package["section_ids"]
    assert sections["SG-CII-LIFECYCLE"]["verification_status"] == "AUDIT_PENDING"

    audit_path = directory / "GPT-FRESH-B4-SG-REPAIR-V5-AUDIT.json"
    v5_results: dict[str, dict] = {}
    if audit_path.is_file():
        audit = load_json(audit_path)
        assert audit["auditor_instance"] == package["auditor_instance_reserved"]
        v5_results = {result["section_id"]: result for result in audit["results"]}

    for frozen in package["sections"]:
        section_id = frozen["section_id"]
        current = sections[section_id]
        assert study_guide_content_hash(frozen["full_prose_under_review"], model_version=model) == frozen["content_hash"]
        assert manifest["section_hashes"][section_id] == frozen["content_hash"]

        if study_guide_content_hash(current) != frozen["content_hash"]:
            assert current["content_version"] > frozen["content_version"]
            assert current["verification_status"] == "AUDIT_PENDING"
            assert current["independent_audit_id"] != "AUDIT-SG-B4-SG-REPAIR-V5-2026-09-10"
            continue

        result = v5_results.get(section_id)
        if result is not None and result["disposition"] == "KEEP":
            assert result["section_hash"] == frozen["content_hash"]
            assert all(verdict == "PASS" for verdict in result["criteria"].values())
            assert result["practice_mapping_verdict"] == "PASS"
            assert current["verification_status"] == "VERIFIED"
            assert current["independent_audit_id"] == "AUDIT-SG-B4-SG-REPAIR-V5-2026-09-10"
        else:
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

    prior = manifest["prior_audit_reference"]
    assert prior["auditor_instance"] == "GPT-FRESH-B4-SG-REPAIR-V4"
    assert prior["reuse_for_repaired_hashes"] is False
    package_text = json.dumps(package, ensure_ascii=False).lower()
    assert "gpt-fresh-b4-sg-repair-v4" not in package_text
    assert "verification_notes" not in package_text


def test_an_older_package_stays_verifiable_after_the_content_model_grows() -> None:
    """A freeze is a record of what an auditor reviewed, so a later schema change must not
    invalidate it.

    The section hash is taken over a fixed field list. When the teaching fields were added
    that list grew, and re-deriving an old package's hash under the new list made every
    historical package fail. Packages therefore record the model they were frozen under.
    """
    legacy_section = {
        "section_id": "SG-LEGACY",
        "title": "Legacy section",
        "areas": [3],
        "topic": "t",
        "subtopic": "s",
        "learning_objectives": ["objective one"],
        "rule_ids": ["FED-X"],
        "verified_rule_dependencies": {"FED-X": {"content_version": 1, "content_hash": "a" * 64}},
        "quick_review": [{"text": "a point", "rule_ids": ["FED-X"]}],
        "decision_logic": [],
        "ma_vs_federal": [],
        "exceptions": [],
        "timing_deadlines": [],
        "forms_records": [],
        "role_duties": [],
        "common_traps": [],
        "drug_examples": [],
        "practice_question_ids": [],
    }
    frozen_hash = study_guide_content_hash(legacy_section, model_version=1)

    # The same snapshot under the current model is a different hash, which is exactly why the
    # version has to be recorded rather than assumed.
    assert study_guide_content_hash(legacy_section) != frozen_hash
    assert study_guide_content_hash(legacy_section, model_version=1) == frozen_hash


def test_every_freeze_package_records_the_model_its_hashes_were_taken_under(root: Path) -> None:
    # Packages predating the versioning carry no field and are read as model 1; anything
    # written since must say so, or a future model change silently breaks its verification.
    for path in sorted((root / "audits" / "study_guide").glob("**/*-AUDIT-PACKAGE.json")):
        package = load_json(path)
        version = package.get("content_model_version", 1)
        assert version in {1, 2}, f"{path}: unknown content model {version}"
        for section in package["sections"]:
            derived = study_guide_content_hash(
                section["full_prose_under_review"], model_version=version
            )
            assert derived == section["content_hash"], f"{path}: {section['section_id']} does not re-derive"
