"""Apply tranche B3-F: 11 rules and 16 Area-3 questions, MA-Q-0391..MA-Q-0406.

Fail-closed, on the same terms as the earlier tranche appliers. It refuses to overwrite any existing
rule or question, refuses to run on a drifted tree, and refuses to create a family that already
exists. Unlike B3-E v2 there is no approved reuse target here: all sixteen questions open a new
family at the Batch-3 standard cap of 2, so a later top-up has somewhere to go without raising a cap.

B3-F exists because the B3-S3 legacy salvage returned nothing usable, leaving a measured Area-3
deficit of six against the Issue #91 minimum of 87.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch3f_questions import QUESTIONS
from batch3f_rules import RULES
from qa_common import DATA, load_json, load_records, semantic_content_hash, write_json


AUTHORING_DATE = "2026-08-20"
EXPECTED_IDS = [f"MA-Q-{index:04d}" for index in range(391, 407)]
FAMILY_CAP = 2

CANDIDATE_STATUS = {
    "verification_status": "AUDIT_PENDING",
    "lifecycle_status": "AUDIT_PENDING",
    "last_legal_review": AUTHORING_DATE,
    "audits": [],
    "duplicate_review_status": "PENDING",
    "independent_audit_status": "PENDING",
    "final_adjudication": None,
    "development_fixture": True,
}

FAMILY_DEFAULTS = {
    "secondary_rule_ids": [],
    "drug_required": False,
    "max_questions_in_final_bank": FAMILY_CAP,
    "current_released_count": 0,
}


def main() -> int:
    if [q["question_id"] for q in QUESTIONS] != EXPECTED_IDS:
        raise SystemExit("question IDs do not match the locked range MA-Q-0391..MA-Q-0406")
    if any(q["area"] != 3 for q in QUESTIONS):
        raise SystemExit("B3-F is an Area-3 top-up; refusing to write a question from another area")

    existing_rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}
    for rule_id, record in existing_rules.items():
        if semantic_content_hash(record, "rule") != record["content_hash"]:
            raise SystemExit(f"{rule_id} content hash has drifted; refusing to author on a drifted tree")

    for rule in RULES:
        if rule["rule_id"] in existing_rules:
            raise SystemExit(f"{rule['rule_id']} already exists; refusing to overwrite")
        record = dict(rule)
        record["content_hash"] = semantic_content_hash(record, "rule")
        write_json(DATA / "rules" / f"{record['rule_id'].lower()}.json", record)
    print(f"wrote {len(RULES)} new rules")

    known_rules = set(existing_rules) | {r["rule_id"] for r in RULES}
    for question in QUESTIONS:
        unknown = [r for r in question["rule_ids"] if r not in known_rules]
        if unknown:
            raise SystemExit(f"{question['question_id']} references unknown rules {unknown}")
        path = DATA / "questions" / f"{question['question_id'].lower()}.json"
        if path.exists():
            raise SystemExit(f"{path} already exists; refusing to overwrite")
        write_json(path, {**question, **CANDIDATE_STATUS})
    print(f"wrote {len(QUESTIONS)} new questions")

    matrix_path = DATA / "exam_style" / "question_family_matrix.json"
    matrix = load_json(matrix_path)
    by_id = {family["family_id"]: family for family in matrix["families"]}

    all_questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}
    candidate_counts = Counter(record["family_id"] for record in all_questions.values())

    created = []
    for question in QUESTIONS:
        family_id = question["family_id"]
        if family_id in by_id:
            raise SystemExit(f"{family_id} already exists; B3-F opens only new families")
        family = {
            "family_id": family_id,
            "area": question["area"],
            "topic": question["topic"],
            "subtopic": question["subtopic"],
            "primary_rule_ids": list(question["rule_ids"]),
            "scenario_types": ["practice scenario"],
            "common_traps": [question["explanation"]["mpje_trap"]],
            "target_difficulties": [question["difficulty"]],
            "target_item_types": [question["question_type"]],
            "current_candidate_count": 0,
            **FAMILY_DEFAULTS,
        }
        by_id[family_id] = family
        matrix["families"].append(family)
        created.append(family_id)

    for family_id in created:
        by_id[family_id]["current_candidate_count"] = candidate_counts[family_id]

    write_json(matrix_path, matrix)
    print(f"created {len(created)} new families, each capped at {FAMILY_CAP}")

    sba = [q for q in QUESTIONS if q["question_type"] == "SBA"]
    sata = [q for q in QUESTIONS if q["question_type"] == "SATA"]
    print(f"areas: {dict(sorted(Counter(q['area'] for q in QUESTIONS).items()))}")
    print(f"types: SBA {len(sba)} / SATA {len(sata)}")
    print(f"SBA keys: {dict(sorted(Counter(q['correct_choice_ids'][0] for q in sba).items()))}")
    print(f"SATA correct-counts: {dict(sorted(Counter(len(q['correct_choice_ids']) for q in sata).items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
