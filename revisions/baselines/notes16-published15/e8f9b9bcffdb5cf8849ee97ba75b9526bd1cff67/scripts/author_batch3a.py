"""Apply Batch 3 tranche B3-A: 27 Area 1 rules and 33 questions, MA-Q-0229..MA-Q-0261.

Fail-closed: refuses to overwrite any existing canonical rule or question, refuses to
extend a family that is already saturated at its final-bank maximum, and refuses to run
if any existing rule's stored content hash has drifted.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch3a_questions import QUESTIONS
from batch3a_rules import RULES
from qa_common import DATA, load_json, load_records, semantic_content_hash, write_json


AUTHORING_DATE = "2026-08-19"
EXPECTED_IDS = [f"MA-Q-{index:04d}" for index in range(229, 262)]

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
    "max_questions_in_final_bank": 2,
    "current_released_count": 0,
}


def main() -> int:
    if [q["question_id"] for q in QUESTIONS] != EXPECTED_IDS:
        raise SystemExit("question IDs do not match the locked B3-A range MA-Q-0229..MA-Q-0261")

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
    print(f"wrote {len(RULES)} new Area 1 rules")

    known_rules = set(existing_rules) | {r["rule_id"] for r in RULES}
    for question in QUESTIONS:
        unknown = [r for r in question["rule_ids"] if r not in known_rules]
        if unknown:
            raise SystemExit(f"{question['question_id']} references unknown rules {unknown}")
        path = DATA / "questions" / f"{question['question_id'].lower()}.json"
        if path.exists():
            raise SystemExit(f"{path} already exists; refusing to overwrite")
        write_json(path, {**question, **CANDIDATE_STATUS})
    print(f"wrote {len(QUESTIONS)} new Area 1 questions")

    matrix_path = DATA / "exam_style" / "question_family_matrix.json"
    matrix = load_json(matrix_path)
    known_families = {family["family_id"] for family in matrix["families"]}
    released_counts = Counter(
        record.get("family_id")
        for _, record in load_records(DATA / "questions")
        if record.get("verification_status") == "RELEASED"
    )
    saturated = {
        family["family_id"]
        for family in matrix["families"]
        if released_counts.get(family["family_id"], 0) >= family["max_questions_in_final_bank"]
    }

    added = 0
    for question in QUESTIONS:
        family_id = question["family_id"]
        if family_id in saturated:
            raise SystemExit(f"{family_id} is already saturated; B3-A must not extend it")
        if family_id in known_families:
            raise SystemExit(f"{family_id} already exists; B3-A families must be new")
        matrix["families"].append(
            {
                "family_id": family_id,
                "area": question["area"],
                "topic": question["topic"],
                "subtopic": question["subtopic"],
                "primary_rule_ids": list(question["rule_ids"]),
                "scenario_types": ["practice scenario"],
                "common_traps": [question["explanation"]["mpje_trap"]],
                "target_difficulties": [question["difficulty"]],
                "target_item_types": [question["question_type"]],
                "current_candidate_count": 1,
                **FAMILY_DEFAULTS,
            }
        )
        known_families.add(family_id)
        added += 1
    write_json(matrix_path, matrix)
    print(f"added {added} new families to the question family matrix")

    print(f"SBA keys: {dict(sorted(Counter(q['correct_choice_ids'][0] for q in QUESTIONS if q['question_type'] == 'SBA').items()))}")
    print(f"SATA correct-counts: {dict(sorted(Counter(len(q['correct_choice_ids']) for q in QUESTIONS if q['question_type'] == 'SATA').items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
