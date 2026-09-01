"""Guardedly publish exact-current-hash Study Guide sections with independent KEEP evidence."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, ROOT, load_json, load_records, write_json
from study_guide_common import study_guide_content_hash
from validate_study_guide_audits import validate_study_guide_audits


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", required=True)
    args = parser.parse_args()
    audit_path = Path(args.audit)
    if not audit_path.is_absolute():
        audit_path = ROOT / audit_path
    audit = load_json(audit_path)

    report, audits = validate_study_guide_audits()
    if not report.ok:
        for error in report.errors:
            print(f"ERROR: {error}")
        return 1
    if audit.get("audit_id") not in audits:
        raise SystemExit("audit is not in the canonical Study Guide audit directory")

    paths = {
        section["section_id"]: path
        for path, section in load_records(DATA / "study_guide" / "sections")
    }
    sections = {
        section["section_id"]: section
        for _, section in load_records(DATA / "study_guide" / "sections")
    }
    published: list[str] = []
    for result in audit["results"]:
        if result["disposition"] != "KEEP":
            continue
        section_id = result["section_id"]
        section = sections[section_id]
        if section["content_hash"] != result["section_hash"]:
            raise SystemExit(f"stale KEEP disposition for {section_id}")
        if study_guide_content_hash(section) != section["content_hash"]:
            raise SystemExit(f"semantic content hash mismatch for {section_id}")
        if any(value != "PASS" for value in result["criteria"].values()):
            raise SystemExit(f"KEEP disposition contains failed criteria for {section_id}")
        if result["practice_mapping_verdict"] != "PASS":
            raise SystemExit(f"KEEP disposition contains failed practice mapping for {section_id}")
        section["verification_status"] = "VERIFIED"
        section["independent_audit_id"] = audit["audit_id"]
        section["last_verified"] = audit["audit_date"]
        write_json(paths[section_id], section)
        published.append(section_id)

    subprocess.check_call(
        [sys.executable, str(ROOT / "scripts" / "generate_artifacts.py"), "--write"],
        cwd=ROOT,
    )
    print(f"published {len(published)} exact-current-hash section(s): {published}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
