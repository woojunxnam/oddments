"""Apply Batch 3 tranche B3-E: 9 rules and 9 Area-4 questions, MA-Q-0361..MA-Q-0369.

Fail-closed: refuses to overwrite any existing canonical rule or question, refuses to run if any
existing rule's stored content hash has drifted, refuses to extend a family that is already
saturated at its final-bank maximum, and refuses to create a family that already exists in the
matrix before this run.

Unlike B3-A and B3-B, this tranche places one question in each of nine new families. That is
permitted by the repository's own governance: schemas/question_family_matrix.schema.json requires a
per-family max_questions_in_final_bank of {"type": "integer", "minimum": 1}, and
validate_governance.validate_family_matrix errors only when the RELEASED count exceeds it. The cap
used for every new family here is 2, the same value author_batch3a.py and author_batch3b.py use.
See audits/controller/AREA2-FAMILY-SLOT-CAPACITY-ANALYSIS.json for the proof, and
audits/controller/BATCH3-CD-AREA2-ALLOCATION.json for the slot-by-slot allocation.
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from batch3e_questions import QUESTIONS
from batch3e_rules import RULES
from qa_common import DATA, load_json, load_records, semantic_content_hash, write_json


AUTHORING_DATE = "2026-08-20"
EXPECTED_IDS = [f"MA-Q-{index:04d}" for index in range(361, 370)]
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
        raise SystemExit("question IDs do not match the locked B3-E range MA-Q-0361..MA-Q-0369")

    per_family = Counter(q["family_id"] for q in QUESTIONS)
    over = {fid: n for fid, n in per_family.items() if n > FAMILY_CAP}
    if over:
        raise SystemExit(f"tranche would place more questions than the family cap allows: {over}")

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
    pre_existing = {family["family_id"]: family for family in matrix["families"]}
    released_counts = Counter(
        record.get("family_id")
        for _, record in load_records(DATA / "questions")
        if record.get("verification_status") == "RELEASED"
    )
    saturated = {
        family_id
        for family_id, family in pre_existing.items()
        if released_counts.get(family_id, 0) >= family["max_questions_in_final_bank"]
    }

    created: dict[str, dict] = {}
    for question in QUESTIONS:
        family_id = question["family_id"]
        if family_id in saturated:
            raise SystemExit(f"{family_id} is already saturated; B3-E must not extend it")
        if family_id in pre_existing:
            raise SystemExit(f"{family_id} already exists in the matrix; B3-E families must be new")
        if family_id in created:
            # Second slot of a family this tranche just created.
            created[family_id]["current_candidate_count"] += 1
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
            "current_candidate_count": 1,
            **FAMILY_DEFAULTS,
        }
        created[family_id] = family
        matrix["families"].append(family)

    # A family carrying two questions must advertise both difficulties and both item types it uses.
    for question in QUESTIONS:
        family = created[question["family_id"]]
        if question["difficulty"] not in family["target_difficulties"]:
            family["target_difficulties"].append(question["difficulty"])
        if question["question_type"] not in family["target_item_types"]:
            family["target_item_types"].append(question["question_type"])
        trap = question["explanation"]["mpje_trap"]
        if trap not in family["common_traps"]:
            family["common_traps"].append(trap)
    for family in created.values():
        family["target_difficulties"] = sorted(family["target_difficulties"])

    write_json(matrix_path, matrix)
    doubled = sorted(fid for fid, n in per_family.items() if n == 2)
    print(f"added {len(created)} new families to the question family matrix "
          f"({len(doubled)} of them carrying two candidates)")
    for fid in doubled:
        print(f"  two slots: {fid}")

    print(f"SBA keys: {dict(sorted(Counter(q['correct_choice_ids'][0] for q in QUESTIONS if q['question_type'] == 'SBA').items()))}")
    print(f"SATA correct-counts: {dict(sorted(Counter(len(q['correct_choice_ids']) for q in QUESTIONS if q['question_type'] == 'SATA').items()))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
