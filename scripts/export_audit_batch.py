from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from qa_common import DATA, ROOT, load_records, question_audit_hash, write_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--auditor", choices=["CLAUDE", "GPT", "HUMAN"], required=True)
    parser.add_argument("--review-type", choices=["LEGAL_VERIFICATION", "REALISM_REVIEW"], required=True)
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
    review_code = "LEGAL" if args.review_type == "LEGAL_VERIFICATION" else "REALISM"
    audit_id = f"AUDIT-{args.auditor}-{review_code}-{audit_date}-{args.start + 1:04d}"
    output = args.output or ROOT / "audits" / args.auditor.casefold() / audit_date / f"{audit_id}.json"
    legal_fields = [
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
    ]
    realism_fields = [
        "Question_ID",
        "Verdict",
        "Severity",
        "Realism_Verdict",
        "Profile_ID",
        "Reviewed_Date",
        "Criteria",
        "Notes",
    ]
    payload = {
        "audit_id": audit_id,
        "auditor": args.auditor,
        "audit_date": audit_date,
        "review_type": args.review_type,
        "independent": True,
        "audit_status": "STRUCTURAL_TRIAGE_ONLY",
        "question_ids": [question["question_id"] for question in batch],
        "question_hashes": {question["question_id"]: question_audit_hash(question) for question in batch},
        "questions": batch,
        "result_contract": {
            "required_fields": legal_fields if args.review_type == "LEGAL_VERIFICATION" else realism_fields,
            "warning": (
                "STRUCTURAL_TRIAGE_ONLY cannot satisfy release. Auditors must not modify canonical questions."
            ),
        },
    }
    write_json(output, payload)
    print(f"exported {len(batch)} questions to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
