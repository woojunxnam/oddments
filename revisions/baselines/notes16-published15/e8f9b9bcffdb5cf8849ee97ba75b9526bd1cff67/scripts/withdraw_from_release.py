"""Guarded, non-destructive temporary withdrawal of a released question.

The repository had a release path but no withdrawal path. When a released question is found
to rest on authority that has since been superseded, it must stop being release-usable while
the question itself, its hash and its whole audit history are preserved untouched.

This tool uses only statuses the question schema already defines:

    verification_status : RELEASED -> HOLD
    lifecycle_status    : RELEASED -> REVIEW_REQUIRED

Neither field is part of QUESTION_AUDIT_FIELDS, so question_audit_hash is unchanged and every
existing audit record stays bound to the current hash. The schema sets additionalProperties
false, so the reason cannot live on the question record; it is written to a governance record
instead.

    python scripts/withdraw_from_release.py --config audits/controller/WITHDRAWAL-XXX.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, ROOT, QUESTION_AUDIT_FIELDS, load_json, load_records, question_audit_hash, write_json
from guarded_release import sync_family_matrix

WITHDRAWN_VERIFICATION = "HOLD"
WITHDRAWN_LIFECYCLE = "REVIEW_REQUIRED"
QUARANTINED_ID = "MA-Q-0028"
PREVIEW = ROOT / "site" / "generated" / "preview_allowlist.json"

# Fields that must survive a withdrawal byte-for-byte, so history is preserved rather than reset.
PRESERVED = [
    *QUESTION_AUDIT_FIELDS,
    "audits",
    "final_adjudication",
    "independent_audit_status",
    "duplicate_review_status",
    "last_legal_review",
    "development_fixture",
]


def snapshot(records: dict) -> dict:
    return {
        qid: {
            "hash": question_audit_hash(r),
            "record": json.loads(json.dumps(r, sort_keys=True)),
        }
        for qid, r in records.items()
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    cfg = load_json(Path(args.config))

    targets = cfg["question_ids"]
    questions = {r["question_id"]: r for _, r in load_records(DATA / "questions")}
    before = snapshot(questions)

    released_before = sorted(q for q, r in questions.items() if r.get("verification_status") == "RELEASED")
    problems = []

    for qid in targets:
        if qid not in questions:
            raise SystemExit(f"{qid} does not exist")
        if questions[qid].get("verification_status") != "RELEASED":
            raise SystemExit(f"{qid} is not RELEASED; refusing to withdraw a question that is not released")
        if cfg.get("expected_hashes", {}).get(qid) not in (None, before[qid]["hash"]):
            raise SystemExit(f"{qid} hash {before[qid]['hash']} does not match the expected hash in the config")

    # --- mutate exactly two status fields on exactly the target questions -------------------
    for qid in targets:
        record = dict(questions[qid])
        record["verification_status"] = WITHDRAWN_VERIFICATION
        record["lifecycle_status"] = WITHDRAWN_LIFECYCLE
        write_json(DATA / "questions" / f"{qid.lower()}.json", record)

    # --- family bookkeeping: released counts must follow the withdrawal --------------------
    family_changes = sync_family_matrix()

    # --- remove them from the preview allowlist -------------------------------------------
    allowlist = load_json(PREVIEW)
    ids_before = list(allowlist["question_ids"])
    allowlist["question_ids"] = [q for q in ids_before if q not in set(targets)]
    allowlist["generated_date"] = cfg["withdrawal_date"]
    allowlist["notice"] = cfg["preview_notice"]
    write_json(PREVIEW, allowlist)
    removed = [q for q in ids_before if q not in allowlist["question_ids"]]

    # ------------------------------- assertions -------------------------------------------
    after_records = {r["question_id"]: r for _, r in load_records(DATA / "questions")}
    after = snapshot(after_records)

    for qid in targets:
        if after[qid]["hash"] != before[qid]["hash"]:
            problems.append(f"{qid}: question_audit_hash changed, {before[qid]['hash']} -> {after[qid]['hash']}")
        for field in PRESERVED:
            if after_records[qid].get(field) != questions[qid].get(field) and field not in (
                "verification_status", "lifecycle_status"
            ):
                # questions[qid] is the pre-mutation dict for every field we did not touch
                problems.append(f"{qid}: preserved field {field} was altered")
        if after_records[qid]["verification_status"] != WITHDRAWN_VERIFICATION:
            problems.append(f"{qid}: verification_status not set to {WITHDRAWN_VERIFICATION}")
        if after_records[qid]["lifecycle_status"] != WITHDRAWN_LIFECYCLE:
            problems.append(f"{qid}: lifecycle_status not set to {WITHDRAWN_LIFECYCLE}")
        if not after_records[qid].get("audits"):
            problems.append(f"{qid}: audit history was emptied")

    untouched = [q for q in after if q not in targets and after[q]["record"] != before[q]["record"]]
    if untouched:
        problems.append(f"unrelated question records changed: {untouched}")

    if after_records[QUARANTINED_ID].get("verification_status") == "RELEASED":
        problems.append(f"{QUARANTINED_ID} quarantine broken")
    if QUARANTINED_ID in allowlist["question_ids"]:
        problems.append(f"{QUARANTINED_ID} present in the preview allowlist")
    if sorted(removed) != sorted(targets):
        problems.append(f"preview removal mismatch: removed {removed}, expected {targets}")

    released_after = sorted(q for q, r in after_records.items() if r.get("verification_status") == "RELEASED")
    if set(released_before) - set(released_after) != set(targets):
        problems.append("released set changed by something other than the targets")

    report = {
        "report_type": "GUARDED_TEMPORARY_WITHDRAWAL",
        "withdrawal_date": cfg["withdrawal_date"],
        "controller_issue": cfg.get("controller_issue"),
        "authorizing_issue": cfg.get("authorizing_issue"),
        "reason_code": cfg["reason_code"],
        "reason": cfg["reason"],
        "reversible": True,
        "how_to_reverse": (
            "Restore verification_status RELEASED and lifecycle_status RELEASED and re-add the id to the "
            "preview allowlist, once an independent current-authority audit clears the current hash."
        ),
        "question_ids": targets,
        "hashes_preserved": {q: after[q]["hash"] for q in targets},
        "status_before": {q: {"verification_status": "RELEASED", "lifecycle_status": "RELEASED"} for q in targets},
        "status_after": {q: {"verification_status": WITHDRAWN_VERIFICATION,
                             "lifecycle_status": WITHDRAWN_LIFECYCLE} for q in targets},
        "audit_history_preserved": {q: after_records[q]["audits"] for q in targets},
        "final_adjudication_preserved": {q: after_records[q]["final_adjudication"] is not None for q in targets},
        "prior_release_record_preserved": (
            "The guarded admission reports that released these questions remain in audits/remediation and "
            "are not altered by this withdrawal."
        ),
        "family_matrix_changes": family_changes,
        "preview": {"before_count": len(ids_before), "after_count": len(allowlist["question_ids"]),
                    "removed": removed},
        "released_count": {"before": len(released_before), "after": len(released_after)},
        "assertions": {
            "hash_unchanged": all(after[q]["hash"] == before[q]["hash"] for q in targets),
            "audit_history_intact": all(after_records[q].get("audits") for q in targets),
            "no_unrelated_question_changed": not untouched,
            "q0028_quarantine_intact": after_records[QUARANTINED_ID].get("verification_status") != "RELEASED",
            "schema_enums_only": True,
        },
        "problems": problems,
    }
    write_json(ROOT / cfg["report_path"], report)

    print(f"withdrawn: {targets}")
    print(f"  hashes preserved : {report['assertions']['hash_unchanged']}")
    print(f"  audits intact    : {report['assertions']['audit_history_intact']}")
    print(f"  preview          : {len(ids_before)} -> {len(allowlist['question_ids'])} (removed {removed})")
    print(f"  released count   : {len(released_before)} -> {len(released_after)}")
    if problems:
        for p in problems:
            print("PROBLEM:", p)
        return 1
    print("WITHDRAWAL ASSERTIONS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
