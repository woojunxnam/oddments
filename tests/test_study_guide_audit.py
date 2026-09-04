from __future__ import annotations

import hashlib
from pathlib import Path

from qa_common import load_json, load_records
from validate_study_guide_audits import validate_study_guide_audits


def test_independent_study_guide_audit_binds_exact_freeze_and_keep(root: Path) -> None:
    audit_path = (
        root
        / "audits"
        / "study_guide"
        / "2026-09-01"
        / "GPT-FRESH-B4-SG-PILOT-V1-AUDIT.json"
    )
    audit = load_json(audit_path)
    report, audits = validate_study_guide_audits()

    assert report.ok
    assert audit["audit_id"] in audits
    assert audit["auditor_instance"] == "GPT-FRESH-B4-SG-PILOT-V1"
    assert audit["represented_freeze_sha"] == "46a2140dc0b4821248f511cff4ca69427388f887"
    package = root / audit["audit_package_path"]
    assert audit["audit_package_sha256"] == hashlib.sha256(
        package.read_bytes().replace(b"\r\n", b"\n")
    ).hexdigest()
    dispositions = {result["section_id"]: result["disposition"] for result in audit["results"]}
    assert dispositions == {
        "SG-CONTROLLED-SCHEDULES": "KEEP",
        "SG-CII-LIFECYCLE": "MAJOR_REWRITE",
        "SG-CIII-V-REFILL-TRANSFER": "MAJOR_REWRITE",
        "SG-MA-SCHEDULE-VI": "MINOR_EDIT",
        "SG-FED-MA-INTERACTION": "MINOR_EDIT",
    }
    sections = {
        section["section_id"]: section
        for _, section in load_records(root / "data" / "study_guide" / "sections")
    }
    # The pilot audit did not KEEP these four, so it certifies none of them and each has
    # since been repaired past its pilot hash. A later audit may have published one of
    # them at a newer hash; that is not the pilot audit's verdict.
    for section_id in dispositions.keys() - {"SG-CONTROLLED-SCHEDULES"}:
        assert sections[section_id]["independent_audit_id"] != audit["audit_id"]
        assert sections[section_id]["content_hash"] != audit["section_hashes"][section_id]


def test_every_public_section_holds_a_current_hash_keep(root: Path) -> None:
    """A section is public only on an independent KEEP bound to its exact current hash.

    validate_study_guide_audits no longer treats an older audit of a since-repaired
    section as drift, so this pins the guarantee that replaced it: publication still
    requires a KEEP, from the section's own audit, at the hash now on disk, with every
    criterion passing.
    """
    report, audits = validate_study_guide_audits()
    assert report.ok

    sections = {
        section["section_id"]: section
        for _, section in load_records(root / "data" / "study_guide" / "sections")
    }
    verified = {
        section_id: section
        for section_id, section in sections.items()
        if section["verification_status"] == "VERIFIED"
    }
    assert verified

    for section_id, section in verified.items():
        audit = audits[section["independent_audit_id"]]
        assert audit["independent"] is True
        assert audit["audit_status"] == "FULLY_ADJUDICATED"
        result = next(item for item in audit["results"] if item["section_id"] == section_id)
        assert result["disposition"] == "KEEP"
        assert result["section_hash"] == section["content_hash"]
        assert result["practice_mapping_verdict"] == "PASS"
        assert all(verdict == "PASS" for verdict in result["criteria"].values())

    for section_id, section in sections.items():
        if section_id in verified:
            continue
        # Anything without such a KEEP stays private, whatever earlier audits said.
        assert section["verification_status"] == "AUDIT_PENDING"
        assert section["independent_audit_id"] is None
        for audit in audits.values():
            result = next(
                (item for item in audit["results"] if item["section_id"] == section_id),
                None,
            )
            if result is not None and result["disposition"] == "KEEP":
                assert result["section_hash"] != section["content_hash"]
