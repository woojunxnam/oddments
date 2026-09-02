"""Validate the B4-A authored range against its final map and sync family counts.

This script does not author or rewrite substantive question content. It fails closed if any
question is missing or if its locked taxonomy and dependencies differ from the reviewed map.
After the checks pass, it normalizes candidate-only governance fields and recomputes the family
matrix candidate/released counts from the complete canonical question directory.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, ROOT, load_json, load_records, write_json


MAP_PATH = ROOT / "audits" / "coverage" / "2026-09-01" / "B4-A-PROPOSITION-MAP-FINAL.json"
MATRIX_PATH = DATA / "exam_style" / "question_family_matrix.json"
AUTHORING_DATE = "2026-09-01"

LOCKED_FIELDS = {
    "family_id": "family_id",
    "area": "area",
    "difficulty": "planned_difficulty",
    "question_type": "planned_question_type",
    "rule_ids": "rule_ids",
}

CANDIDATE_GOVERNANCE = {
    "verification_status": "AUDIT_PENDING",
    "lifecycle_status": "AUDIT_PENDING",
    "last_legal_review": AUTHORING_DATE,
    "audits": [],
    "duplicate_review_status": "PENDING",
    "independent_audit_status": "PENDING",
    "final_adjudication": None,
    "development_fixture": True,
}


def main() -> int:
    proposition_map = load_json(MAP_PATH)
    slots = proposition_map["slots"]
    expected_ids = [f"MA-Q-{number:04d}" for number in range(407, 440)]
    if [slot["question_id"] for slot in slots] != expected_ids:
        raise SystemExit("the final proposition map no longer contains the locked MA-Q-0407..0439 range")

    known_rules = {record["rule_id"] for _, record in load_records(DATA / "rules")}
    for slot in slots:
        qid = slot["question_id"]
        path = DATA / "questions" / f"{qid.lower()}.json"
        if not path.exists():
            raise SystemExit(f"missing authored question {qid}")
        question = load_json(path)
        if question.get("question_id") != qid:
            raise SystemExit(f"{path}: question_id does not match filename")
        for question_field, map_field in LOCKED_FIELDS.items():
            if question.get(question_field) != slot[map_field]:
                raise SystemExit(
                    f"{qid}: {question_field} differs from final map: "
                    f"{question.get(question_field)!r} != {slot[map_field]!r}"
                )
        unknown_rules = sorted(set(question["rule_ids"]) - known_rules)
        if unknown_rules:
            raise SystemExit(f"{qid}: unknown rule dependencies {unknown_rules}")
        if question.get("provenance") != "GEN" or question.get("source_signal_ids") != []:
            raise SystemExit(f"{qid}: B4-A must remain GEN with no recalled-question signal IDs")
        write_json(path, {**question, **CANDIDATE_GOVERNANCE})

    questions = [record for _, record in load_records(DATA / "questions")]
    candidate_counts = Counter(record["family_id"] for record in questions)
    released_counts = Counter(
        record["family_id"]
        for record in questions
        if record.get("verification_status") == "RELEASED"
        and record.get("lifecycle_status") == "RELEASED"
    )

    matrix = load_json(MATRIX_PATH)
    families = {family["family_id"]: family for family in matrix["families"]}
    missing_families = sorted(set(candidate_counts) - set(families))
    if missing_families:
        raise SystemExit(f"questions reference families absent from the matrix: {missing_families}")
    for family_id, family in families.items():
        family["current_candidate_count"] = candidate_counts.get(family_id, 0)
        family["current_released_count"] = released_counts.get(family_id, 0)
    matrix["last_reviewed"] = AUTHORING_DATE
    write_json(MATRIX_PATH, matrix)

    print(f"validated and normalized {len(slots)} B4-A candidates")
    print(f"synced {len(families)} family records from {len(questions)} canonical questions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
