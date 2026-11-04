"""Apply the second, fail-closed repair of MA-Q-0203 after its fresh v1 REAUDIT.

The v1 repair's legal key was correct, but the independent auditor found a stale
drug dependency and a full-bank realism collision with MA-Q-0202. This script
replaces that scenario with an oral-liquid-single-dose scope question. It does
not release or self-audit the result.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, ROOT, load_json, question_audit_hash, write_json


REPAIR_DATE = "2026-08-20"
SOURCE_SHA = "c15c49e76e1a5c87d35a6cc5bb111f2e7b427cb2"
QUESTION_ID = "MA-Q-0203"
OLD_HASH = "107a7f63b2d39141ecd1a17da6cbe8ecf704f059aa7b2aad2b956e08d9f79488"
NEW_HASH = "ce251a6a745881352e0dfbc030efd479603cf96c4d43d2a1ae3a3cfed76c335d"
OLD_FAMILY = "B2_DRUG_MULTI_DRUG_SIII_EXCLUSION"
NEW_FAMILY = "B2_ORAL_LIQUID_SINGLE_DOSE_SCOPE"


REPAIR = {
    "family_id": NEW_FAMILY,
    "subtopic": "Oral-liquid-single-dose boundary",
    "stem": (
        "A Massachusetts pharmacy plans to place each dose of Schedule II methylphenidate oral solution in its "
        "own oral-liquid-single-dose container. No second drug will be in any container. All requirements outside "
        "247 CMR 9.08(3)(b) are left for separate review. What does paragraph (3)(b) decide?"
    ),
    "choices": [
        ("A", "It prohibits the plan because Schedule II drugs may never use any form of compliance packaging."),
        ("B", "It prohibits the plan because oral-liquid packaging becomes multi-drug whenever other prescriptions are dispensed that day."),
        ("C", "It does not prohibit this oral-liquid-single-dose plan; the paragraph targets Schedule II or III drugs in multi-drug-single-dose packages."),
        ("D", "It permits the plan only after the prescriber signs a controlled-substance packaging authorization."),
        ("E", "It permits the plan because patient consent converts the container into manufacturer packaging."),
    ],
    "correct_choice_ids": ["C"],
    "explanation": {
        "core_reasoning": (
            "247 CMR 9.08 distinguishes oral-liquid-single-dose, single-drug-single-dose and multi-drug-single-dose "
            "packaging. Paragraph (3)(b) bars Schedule II and III controlled substances only from the "
            "multi-drug-single-dose form. A container holding one measured dose of methylphenidate oral solution "
            "and no second drug is not that form, so paragraph (3)(b) does not itself prohibit the plan. Every "
            "other applicable packaging, labeling, compatibility and controlled-substance requirement still must "
            "be reviewed."
        ),
        "choice_analysis": {
            "A": "This expands a prohibition tied to one packaging form into a ban on every compliance-packaging form.",
            "B": "Packaging type depends on what the container holds, not on unrelated prescriptions dispensed that day.",
            "C": "Correct: paragraph (3)(b) is confined to Schedule II/III drugs in multi-drug-single-dose packages.",
            "D": "The paragraph does not create a prescriber-authorization pathway for this packaging decision.",
            "E": "Patient consent does not change the physical packaging category.",
        },
        "related_facts": [
            "Paragraph (3)(b) does not waive the separate conditions that govern oral-liquid-single-dose packaging."
        ],
        "mpje_trap": (
            "Treating the controlled-substance schedule as dispositive while ignoring the packaging category named "
            "in the prohibition."
        ),
    },
    "drug_ids": ["methylphenidate"],
    "reasoning_steps": [
        "Identify methylphenidate as Schedule II",
        "Classify a one-drug measured liquid dose as oral-liquid-single-dose rather than multi-drug-single-dose packaging",
        "Apply paragraph (3)(b) only to the packaging form it names while preserving other requirements",
    ],
}


def apply_question(question: dict) -> None:
    for field in ("family_id", "subtopic", "stem", "correct_choice_ids", "explanation", "drug_ids", "reasoning_steps"):
        question[field] = REPAIR[field]
    question["choices"] = [{"id": choice_id, "text": text} for choice_id, text in REPAIR["choices"]]
    question["verification_status"] = "AUDIT_PENDING"
    question["lifecycle_status"] = "AUDIT_PENDING"
    question["last_legal_review"] = REPAIR_DATE
    question["audits"] = []
    question["duplicate_review_status"] = "PENDING"
    question["independent_audit_status"] = "PENDING"
    question["final_adjudication"] = None
    question["development_fixture"] = True


def main() -> int:
    question_path = DATA / "questions" / "ma-q-0203.json"
    question = load_json(question_path)
    before = question_audit_hash(question)
    if before not in {OLD_HASH, NEW_HASH}:
        raise SystemExit(f"{QUESTION_ID}: expected {OLD_HASH} or idempotent {NEW_HASH}, found {before}")
    apply_question(question)
    after = question_audit_hash(question)
    if after != NEW_HASH:
        raise SystemExit(f"{QUESTION_ID}: expected repaired hash {NEW_HASH}, found {after}")
    write_json(question_path, question)

    matrix_path = DATA / "exam_style" / "question_family_matrix.json"
    matrix = load_json(matrix_path)
    matches = [row for row in matrix["families"] if row["family_id"] in {OLD_FAMILY, NEW_FAMILY}]
    if len(matches) != 1:
        raise SystemExit(f"family matrix expected one old/new row, found {len(matches)}")
    family = matches[0]
    family["family_id"] = NEW_FAMILY
    family["subtopic"] = "Oral-liquid-single-dose boundary"
    family["common_traps"] = [
        "Treating a schedule-based prohibition as if it ignored the packaging form named in the rule."
    ]
    write_json(matrix_path, matrix)

    report = {
        "record_id": "BATCH3-Q0203-V2-REPAIR",
        "recorded_by": "GPT_DESKTOP_CONTROLLER_AUTHOR_NOT_AUDITOR",
        "recorded_on": REPAIR_DATE,
        "controller_issue": 83,
        "authorizing_issue": 91,
        "source_sha": SOURCE_SHA,
        "question_id": QUESTION_ID,
        "old_question_hash": OLD_HASH,
        "new_question_hash": NEW_HASH,
        "prior_audits": {
            "legal": "AUDIT-GPT-FRESH-B3-MINIMUM-REPAIRS-V1-LEGAL-REAUDIT-2026-08-20",
            "realism": "AUDIT-GPT-FRESH-B3-MINIMUM-REPAIRS-V1-REALISM-REAUDIT-2026-08-20",
        },
        "verified_defects": [
            "drug_ids named oxycodone while the v1 scenario concerned buprenorphine",
            "the v1 scenario duplicated MA-Q-0202 choice A's stable Schedule III buprenorphine multi-drug pouch decision",
        ],
        "repair_scope": (
            "Replace the duplicated maintenance/multi-drug scenario with a different packaging-category application: "
            "Schedule II methylphenidate in oral-liquid-single-dose containers. Correct the drug dependency to "
            "methylphenidate and preserve AUDIT_PENDING state."
        ),
        "release_status": "NOT_RELEASED_PENDING_NEW_FRESH_INDEPENDENT_REAUDIT",
        "self_audit_performed": False,
    }
    report_path = ROOT / "audits" / "remediation" / REPAIR_DATE / "BATCH3-Q0203-V2-REPAIR.json"
    write_json(report_path, report)
    print(json.dumps({"question_id": QUESTION_ID, "old_hash": OLD_HASH, "new_hash": after}, indent=2))
    print("release status: NOT_RELEASED_PENDING_NEW_FRESH_INDEPENDENT_REAUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
