from __future__ import annotations

import shutil
from copy import deepcopy

from build_study_guide_data import build_study_guide_payload
from qa_common import DATA
from validate_study_guide import validate_study_guide


def test_canonical_study_guide_pilot_validates(registry_indexes) -> None:
    rules, _ = registry_indexes
    report, sections = validate_study_guide(rules)

    assert report.ok
    assert len(sections) == 5
    verified = [s for s in sections.values() if s["verification_status"] == "VERIFIED"]
    pending = [s for s in sections.values() if s["verification_status"] == "AUDIT_PENDING"]
    # Every section is either independently verified or still fails closed, and the
    # audit reference tracks that state exactly. Counts move as tranches publish.
    assert len(verified) + len(pending) == len(sections)
    assert verified
    assert all(section["independent_audit_id"] for section in verified)
    assert all(section["last_verified"] for section in verified)
    assert all(section["independent_audit_id"] is None for section in pending)
    assert all(section["last_verified"] is None for section in pending)


def test_public_payload_fails_closed_until_independent_verification() -> None:
    from qa_common import load_records

    canonical = {section["section_id"]: section for _, section in load_records(DATA / "study_guide" / "sections")}
    verified_ids = {sid for sid, section in canonical.items() if section["verification_status"] == "VERIFIED"}
    assert verified_ids
    assert verified_ids != set(canonical)

    public = build_study_guide_payload(include_pending=False)
    development = build_study_guide_payload(include_pending=True)

    # The public payload carries exactly the independently verified sections; anything
    # still pending is absent at the static-file layer, not merely hidden in the UI.
    assert {section["section_id"] for section in public["sections"]} == verified_ids
    assert public["meta"]["section_count"] == len(verified_ids)
    assert public["meta"]["pending_section_count"] == len(canonical) - len(verified_ids)
    assert public["question_to_sections"]
    assert development["meta"]["section_count"] == len(canonical)


def test_rule_hash_change_makes_dependent_sections_stale(tmp_path, registry_indexes) -> None:
    rules, _ = registry_indexes
    changed_rules = deepcopy(rules)
    changed_rules["FED-CS-SCHEDULES"]["content_hash"] = "f" * 64
    temp_data = tmp_path / "data"
    shutil.copytree(DATA / "study_guide", temp_data / "study_guide")

    from validate_questions import validate_questions

    _, questions = validate_questions(rules)
    report, _ = validate_study_guide(changed_rules, questions, data_root=temp_data)

    assert not report.ok
    assert any("stale dependency snapshot for FED-CS-SCHEDULES" in error for error in report.errors)


def test_every_pilot_practice_link_is_release_usable(registry_indexes) -> None:
    rules, _ = registry_indexes
    report, sections = validate_study_guide(rules)
    assert report.ok

    from validate_questions import validate_questions

    _, questions = validate_questions(rules)
    linked = {
        question_id for section in sections.values() for question_id in section["practice_question_ids"]
    }
    assert linked
    assert all(questions[question_id]["verification_status"] == "RELEASED" for question_id in linked)
    assert all(questions[question_id]["lifecycle_status"] == "RELEASED" for question_id in linked)
