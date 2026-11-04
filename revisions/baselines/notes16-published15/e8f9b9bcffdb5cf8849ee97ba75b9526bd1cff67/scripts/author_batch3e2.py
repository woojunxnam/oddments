"""Apply the B3-E v2 expansion: 15 rules and 21 questions, MA-Q-0370..MA-Q-0390.

Fail-closed. Refuses to overwrite any existing rule or question, refuses to run on a drifted tree,
refuses to exceed any family's max_questions_in_final_bank, and refuses to create a family that
already exists.

Two family behaviours are needed here, unlike earlier tranches:

  * the four Area-2 questions attach to families that ALREADY exist, occupying their second
    final-bank slot; the matrix entry is updated rather than created;
  * the seventeen Area-3 and Area-4 questions each create a new family at the Batch-3 standard cap
    of 2, so a later top-up has somewhere to go.

No cap is raised anywhere.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch3e2_questions import QUESTIONS
from batch3e2_rules import RULES
from qa_common import DATA, load_json, load_records, semantic_content_hash, write_json


AUTHORING_DATE = "2026-08-20"
EXPECTED_IDS = [f"MA-Q-{index:04d}" for index in range(370, 391)]
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

# Area-2 questions deliberately reuse an approved family's free second slot.
EXPECTED_REUSED_FAMILIES = {
    "PATIENT_PROFILE_REASONABLE_EFFORT_STANDARD",
    "CPA_VALID_CONSTITUTION_AND_BIENNIAL_CURRENCY",
    "COUNSELLING_OFFER_METHOD_AND_CONTAINER_LABEL",
    "PROSPECTIVE_DRUG_REVIEW_MANDATORY_VS_MENU",
}


def main() -> int:
    if [q["question_id"] for q in QUESTIONS] != EXPECTED_IDS:
        raise SystemExit("question IDs do not match the locked range MA-Q-0370..MA-Q-0390")

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
    released_counts = Counter(
        record["family_id"] for record in all_questions.values()
        if record.get("verification_status") == "RELEASED"
    )

    reused, created = [], []
    for question in QUESTIONS:
        family_id = question["family_id"]
        if family_id in by_id:
            if family_id not in EXPECTED_REUSED_FAMILIES:
                raise SystemExit(f"{family_id} already exists but was not an approved reuse target")
            family = by_id[family_id]
            if candidate_counts[family_id] > family["max_questions_in_final_bank"]:
                raise SystemExit(
                    f"{family_id} would hold {candidate_counts[family_id]} candidates against a cap of "
                    f"{family['max_questions_in_final_bank']}"
                )
            if released_counts[family_id] >= family["max_questions_in_final_bank"]:
                raise SystemExit(f"{family_id} is already saturated on released count")
            reused.append(family_id)
            continue
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

    # Recompute every touched family's candidate count from the canonical records.
    for family_id in set(reused) | set(created):
        by_id[family_id]["current_candidate_count"] = candidate_counts[family_id]

    write_json(matrix_path, matrix)
    print(f"created {len(created)} new families; reused a free second slot in {len(reused)}")
    for family_id in sorted(set(reused)):
        print(f"  second slot: {family_id} -> {candidate_counts[family_id]}/"
              f"{by_id[family_id]['max_questions_in_final_bank']}")

    print(f"areas: {dict(sorted(Counter(q['area'] for q in QUESTIONS).items()))}")
    print(f"SBA keys: {dict(sorted(Counter(q['correct_choice_ids'][0] for q in QUESTIONS if q['question_type'] == 'SBA').items()))}")
    print(f"SATA correct-counts: {dict(sorted(Counter(len(q['correct_choice_ids']) for q in QUESTIONS if q['question_type'] == 'SATA').items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
