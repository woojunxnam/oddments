from __future__ import annotations

import hashlib
from pathlib import Path

from qa_common import load_json
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
