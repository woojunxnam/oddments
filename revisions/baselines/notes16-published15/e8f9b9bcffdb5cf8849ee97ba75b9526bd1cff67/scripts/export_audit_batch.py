from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from qa_common import DATA, ROOT, load_json, load_records, question_audit_hash, write_json
from release_context import style_profile_snapshot


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--auditor", choices=["CLAUDE", "GPT", "HUMAN"], required=True)
    parser.add_argument("--auditor-instance")
    parser.add_argument("--audit-id")
    parser.add_argument("--review-type", choices=["LEGAL_VERIFICATION", "REALISM_REVIEW"], required=True)
    parser.add_argument("--audit-scope", choices=["INITIAL_BATCH", "REAUDIT"], required=True)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=40)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    minimum = 30 if args.audit_scope == "INITIAL_BATCH" else 1
    if not minimum <= args.count <= 40:
        parser.error(f"--count must be between {minimum} and 40 for {args.audit_scope}")
    records = [record for _, record in load_records(DATA / "questions")]
    batch = records[args.start : args.start + args.count]
    if len(batch) != args.count:
        parser.error("the registry does not contain enough questions for the requested batch")
    audit_date = date.today().isoformat()
    review_code = "LEGAL" if args.review_type == "LEGAL_VERIFICATION" else "REALISM"
    audit_id = args.audit_id or f"AUDIT-{args.auditor}-{review_code}-{args.audit_scope}-{audit_date}-{args.start + 1:04d}"
    output = args.output or ROOT / "audits" / args.auditor.casefold() / audit_date / f"{audit_id}.json"
    legal_fields = [
        "Question_ID",
        "Verdict",
        "Severity",
        "Existing_Answer_Correct",
        "authorities",
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
        "Reviewed_Date",
        "Criteria",
        "Notes",
    ]
    payload = {
        "audit_id": audit_id,
        "auditor": args.auditor,
        "audit_date": audit_date,
        "audit_scope": args.audit_scope,
        "review_type": args.review_type,
        "independent": True,
        "audit_status": "STRUCTURAL_TRIAGE_ONLY",
        "question_ids": [question["question_id"] for question in batch],
        "question_hashes": {question["question_id"]: question_audit_hash(question) for question in batch},
        "questions": batch,
        "result_contract": {
            "required_fields": legal_fields if args.review_type == "LEGAL_VERIFICATION" else realism_fields,
            "warning": "STRUCTURAL_TRIAGE_ONLY cannot satisfy release. Auditors must not modify canonical questions.",
        },
    }
    if args.auditor_instance:
        payload["auditor_instance"] = args.auditor_instance
    if args.review_type == "REALISM_REVIEW":
        profile = load_json(DATA / "exam_style" / "mpje_style_profile.json")
        payload["style_profile"] = style_profile_snapshot(profile)
    write_json(output, payload)
    print(f"exported {len(batch)} questions to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
