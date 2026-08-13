from __future__ import annotations

import argparse
import hashlib
from datetime import date
from pathlib import Path

from qa_common import DATA, ROOT, load_records, write_json


def question_hash(question: dict) -> str:
    import json

    canonical = json.dumps(question, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--auditor", choices=["CLAUDE", "GPT", "HUMAN"], required=True)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=40)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not 30 <= args.count <= 40:
        parser.error("--count must be between 30 and 40")
    records = [record for _, record in load_records(DATA / "questions")]
    batch = records[args.start : args.start + args.count]
    if len(batch) != args.count:
        parser.error("the registry does not contain enough questions for the requested 30-40 item batch")
    audit_date = date.today().isoformat()
    audit_id = f"AUDIT-{args.auditor}-{audit_date}-{args.start + 1:04d}"
    output = args.output or ROOT / "audits" / args.auditor.casefold() / audit_date / f"{audit_id}.json"
    payload = {
        "audit_id": audit_id,
        "auditor": args.auditor,
        "audit_date": audit_date,
        "audit_status": "STRUCTURAL_TRIAGE_ONLY",
        "question_ids": [question["question_id"] for question in batch],
        "question_hashes": {question["question_id"]: question_hash(question) for question in batch},
        "questions": batch,
        "result_contract": {
            "required_fields": [
                "Question_ID",
                "Verdict",
                "Severity",
                "Existing_Answer_Correct",
                "Authority",
                "Exact_Section",
                "Official_URL",
                "Law_Checked_Date",
                "Problem",
                "Proposed_Answer",
                "Proposed_Rewrite",
                "Proposed_Explanation",
            ],
            "warning": "STRUCTURAL_TRIAGE_ONLY is not legal validation. Auditors must not modify canonical questions.",
        },
    }
    write_json(output, payload)
    print(f"exported {len(batch)} questions to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
