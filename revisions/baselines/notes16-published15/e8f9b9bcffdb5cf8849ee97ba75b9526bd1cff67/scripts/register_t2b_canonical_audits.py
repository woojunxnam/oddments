"""Register the accepted Auditor-B current-MA-Q-0213 evidence canonically.

Issue #83 PHASE B. The two canonical-ready records produced on PR #80
(head 346ebc39408ad710a1024bd0bfdac013ed1e3f1e) are already expressed in the
post-PR81 canonical audit schema, so this script performs a byte-faithful copy into
`data/audits/` under their exact audit IDs. It verifies the immutable blob SHAs first
and fails closed if any semantic field would change.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, ROOT, write_json


AUDITOR_INSTANCE = "GPT-FRESH-COV-T2-B"
ACCEPTED_AUDIT_PR = 77
ACCEPTED_AUDIT_HEAD = "5242f4c74f06402e0d1b27362831156e0e84a547"
NORMALIZATION_PR = 80
NORMALIZATION_HEAD = "346ebc39408ad710a1024bd0bfdac013ed1e3f1e"
CURRENT_Q0213_HASH = "689120dad57db1ef46087cda3450a8df13799d865c67dd9942f46d7911b1ce23"

SOURCES = {
    "LEGAL_VERIFICATION": {
        "path": "audits/remediation/2026-08-19/AUDIT-GPT-FRESH-COV-T2-B-Q0213-CANONICAL-LEGAL-NORMALIZATION.json",
        "blob": "88f671ddb3b10d8d2b12d1f67aae716dc4bf0312",
        "audit_id": "AUDIT-GPT-FRESH-COV-T2-B-LEGAL-REAUDIT-2026-08-19",
    },
    "REALISM_REVIEW": {
        "path": "audits/remediation/2026-08-19/AUDIT-GPT-FRESH-COV-T2-B-Q0213-CANONICAL-REALISM-NORMALIZATION.json",
        "blob": "f0fb52cad741548f797a939210ef8e56075da544",
        "audit_id": "AUDIT-GPT-FRESH-COV-T2-B-REALISM-REAUDIT-2026-08-19",
    },
}


def load_immutable_source(blob_sha: str) -> dict:
    raw = subprocess.check_output(["git", "cat-file", "blob", blob_sha], cwd=ROOT)
    return json.loads(raw.decode("utf-8"))


def assert_accepted_semantics(review_type: str, record: dict) -> None:
    expected = SOURCES[review_type]
    if record.get("audit_id") != expected["audit_id"]:
        raise SystemExit(f"{review_type}: audit_id {record.get('audit_id')!r} != {expected['audit_id']!r}")
    if record.get("auditor") != "GPT" or record.get("auditor_instance") != AUDITOR_INSTANCE:
        raise SystemExit(f"{review_type}: auditor provenance drift")
    if record.get("review_type") != review_type:
        raise SystemExit(f"{review_type}: review_type drift")
    if record.get("independent") is not True or record.get("audit_status") != "FULLY_ADJUDICATED":
        raise SystemExit(f"{review_type}: independence/adjudication drift")
    if record.get("question_ids") != ["MA-Q-0213"]:
        raise SystemExit(f"{review_type}: Auditor-B evidence must cover exactly MA-Q-0213")
    if record.get("question_hashes") != {"MA-Q-0213": CURRENT_Q0213_HASH}:
        raise SystemExit(f"{review_type}: Auditor-B evidence must be bound to the current MA-Q-0213 hash")

    result = record["results"][0]
    if result.get("Question_ID") != "MA-Q-0213" or result.get("Verdict") != "KEEP":
        raise SystemExit(f"{review_type}: accepted Auditor-B verdict is KEEP")
    if review_type == "LEGAL_VERIFICATION":
        if result.get("Existing_Answer_Correct") != "YES":
            raise SystemExit("accepted Auditor-B legal result is Existing_Answer_Correct=YES")
        if not result.get("authorities"):
            raise SystemExit("accepted Auditor-B legal result must retain its authorities")
    else:
        if result.get("Realism_Verdict") != "PASS":
            raise SystemExit("accepted Auditor-B realism result is PASS")
        if not all(result.get("Criteria", {}).values()):
            raise SystemExit("accepted Auditor-B realism result passes all ten criteria")
        if len(result.get("Criteria", {})) != 10:
            raise SystemExit("accepted Auditor-B realism result records all ten criteria")


def main() -> int:
    written = []
    for review_type, source in SOURCES.items():
        record = load_immutable_source(source["blob"])
        assert_accepted_semantics(review_type, record)
        destination = DATA / "audits" / f"{source['audit_id']}.json"
        write_json(destination, record)
        # Re-read and compare so a formatting-only write can never alter semantics.
        if json.loads(destination.read_text(encoding="utf-8")) != record:
            raise SystemExit(f"{review_type}: registered record differs from the accepted source record")
        written.append(destination)
        print(f"registered {destination.relative_to(ROOT).as_posix()} from blob {source['blob']}")

    provenance = {
        "report_type": "T2_AUDITOR_B_CANONICAL_REGISTRATION",
        "controller_issue": 83,
        "auditor": "GPT",
        "auditor_instance": AUDITOR_INSTANCE,
        "accepted_audit_pr": ACCEPTED_AUDIT_PR,
        "accepted_audit_head": ACCEPTED_AUDIT_HEAD,
        "canonical_ready_normalization_pr": NORMALIZATION_PR,
        "canonical_ready_normalization_head": NORMALIZATION_HEAD,
        "current_question_hash": {"MA-Q-0213": CURRENT_Q0213_HASH},
        "statement": (
            "The accepted Auditor-B canonical-ready records were copied verbatim into data/audits/ "
            "under their exact audit IDs. No semantic field was rewritten or reinterpreted."
        ),
        "immutable_sources": {
            source["path"]: {"git_blob_sha": source["blob"], "registered_as": f"data/audits/{source['audit_id']}.json"}
            for source in SOURCES.values()
        },
        "accepted_results": {
            "LEGAL_VERIFICATION": {"Verdict": "KEEP", "Existing_Answer_Correct": "YES"},
            "REALISM_REVIEW": {"Verdict": "KEEP", "Realism_Verdict": "PASS", "criteria_passed": 10},
        },
    }
    report_path = ROOT / "audits" / "remediation" / "2026-08-19" / "T2-AUDITOR-B-CANONICAL-REGISTRATION-PROVENANCE.json"
    write_json(report_path, provenance)
    print(f"wrote {report_path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
