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
    # The guide grows toward full coverage of the canonical rules, so pin the pilot set as
    # a floor rather than the total.
    assert {"SG-CONTROLLED-SCHEDULES", "SG-CII-LIFECYCLE", "SG-CIII-V-REFILL-TRANSFER",
            "SG-MA-SCHEDULE-VI", "SG-FED-MA-INTERACTION"} <= set(sections)
    verified = [s for s in sections.values() if s["verification_status"] == "VERIFIED"]
    pending = [s for s in sections.values() if s["verification_status"] == "AUDIT_PENDING"]
    # Every section is either independently verified or still fails closed, and the
    # audit reference tracks that state exactly. Counts move as tranches publish.
    assert len(verified) + len(pending) == len(sections)
    # `verified` is legitimately empty while the whole guide sits between content models:
    # every section was re-authored and none has been re-audited yet. Publication is what
    # the invariants below protect, not the count.
    assert all(section["independent_audit_id"] for section in verified)
    assert all(section["last_verified"] for section in verified)
    assert all(section["independent_audit_id"] is None for section in pending)
    assert all(section["last_verified"] is None for section in pending)


def test_public_payload_fails_closed_until_independent_verification() -> None:
    from qa_common import load_records

    canonical = {section["section_id"]: section for _, section in load_records(DATA / "study_guide" / "sections")}
    verified_ids = {sid for sid, section in canonical.items() if section["verification_status"] == "VERIFIED"}
    # No section may be public without independent verification. That the filter is a real
    # filter and not a no-op is proved by the test below, which holds a section back whatever
    # the corpus happens to look like; asserting here that some section is unverified would
    # only pin today's state, and the whole guide is verified once a round completes.

    public = build_study_guide_payload(include_pending=False)
    development = build_study_guide_payload(include_pending=True)

    # The public payload carries exactly the independently verified sections; anything
    # still pending is absent at the static-file layer, not merely hidden in the UI.
    assert {section["section_id"] for section in public["sections"]} == verified_ids
    assert public["meta"]["section_count"] == len(verified_ids)
    assert public["meta"]["pending_section_count"] == len(canonical) - len(verified_ids)
    # The public question map is built from public sections only, so it empties when nothing
    # is verified rather than leaking a pending section through a practice-question link.
    assert set(public["question_to_sections"]) <= {
        qid for sid in verified_ids for qid in canonical[sid]["practice_question_ids"]
    }
    assert bool(public["question_to_sections"]) == any(
        canonical[sid]["practice_question_ids"] for sid in verified_ids
    )
    assert development["meta"]["section_count"] == len(canonical)


def test_public_payload_holds_back_a_section_that_is_not_verified(monkeypatch) -> None:
    """The public filter must exclude an unverified section even when every real one passes.

    Comparing the public payload against the verified set says nothing when the two coincide,
    which is exactly the state after a full audit round. So put one section back into
    AUDIT_PENDING and watch it leave the public payload while staying in the development one.
    """
    import build_study_guide_data
    from qa_common import load_records

    canonical = {section["section_id"]: section for _, section in load_records(DATA / "study_guide" / "sections")}
    # Hold back a published section, so the filter is shown removing something that would otherwise be
    # public, whatever else in the corpus happens to be awaiting audit at the time.
    published = [sid for sid in sorted(canonical) if canonical[sid]["verification_status"] == "VERIFIED"]
    assert published, "the corpus holds at least one published section to hold back"
    held_back = published[0]
    real_validate = build_study_guide_data.validate_study_guide

    def one_section_pending(*args, **kwargs):
        report, sections = real_validate(*args, **kwargs)
        sections = deepcopy(sections)
        sections[held_back]["verification_status"] = "AUDIT_PENDING"
        sections[held_back]["independent_audit_id"] = None
        sections[held_back]["last_verified"] = None
        return report, sections

    monkeypatch.setattr(build_study_guide_data, "validate_study_guide", one_section_pending)
    public = build_study_guide_data.build_study_guide_payload(include_pending=False)
    development = build_study_guide_data.build_study_guide_payload(include_pending=True)

    assert held_back not in {section["section_id"] for section in public["sections"]}
    assert held_back in {section["section_id"] for section in development["sections"]}
    already_pending = sum(section["verification_status"] == "AUDIT_PENDING" for section in canonical.values())
    assert public["meta"]["section_count"] == len(published) - 1
    assert public["meta"]["pending_section_count"] == already_pending + 1
    # The practice-question map must not leak the held-back section through a shared question.
    assert held_back not in {sid for sids in public["question_to_sections"].values() for sid in sids}


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
