"""Batch 3 B3-A realism repair R1 — MA-Q-0241 and MA-Q-0256 only.

The CLAUDE-FRESH-B3A audit returned legal KEEP / Existing_Answer_Correct YES for both,
and realism MINOR_EDIT / FAIL on the single criterion distinct_from_bank:

  * MA-Q-0241 repeated three of MA-Q-0076's four keyed propositions (the 247 CMR 8.05(2)
    technician / certified-technician transport-and-handling ladder).
  * MA-Q-0256 tested the same per-calendar-year CE minimum and no-carry-forward
    discrimination as MA-Q-0079.

Both are moved onto genuinely different current-law decision paths rather than
paraphrased. Path selection was made against the full 294-question candidate universe
(this lineage's 261 plus the frozen B3-B tranche of 33) at CMR-paragraph granularity,
after four earlier candidate paths were rejected for collisions that the rule-id level
had hidden:

  * 247 CMR 8.06(1) rejected — already keyed by the released sibling MA-Q-0247.
  * 247 CMR 4.02(5) rejected — already keyed by the released sibling MA-Q-0254.
  * 247 CMR 3.01(7) rejected — already keyed by the released sibling MA-Q-0249.
  * 247 CMR 4.03(4)(a) pharmacy-law hours rejected — already keyed by MA-Q-0257.

Selected paths, each verbatim-verified from the official published regulation and keyed
nowhere in the 294-question universe:

  * MA-Q-0241 -> 247 CMR 8.05(3), first sentence. A certified pharmacy technician,
    pharmacy technician, or pharmacy technician trainee may not handle any hydrocodone-only
    extended release medication that is not in an abuse deterrent form. The keyed axis is
    the product test, not the personnel ladder MA-Q-0076 keys.
  * MA-Q-0256 -> 247 CMR 4.03(7). A registrant may not earn more than eight contact hours
    of continuing education in a calendar day. This is a rate limit on earning, not the
    per-calendar-year total minimum MA-Q-0079 keys, and is not a symmetric reversal of it.

Deliberately NOT used: the second sentence of 247 CMR 8.05(3), the pharmacy-intern
carve-out. The officially published PDF truncates it mid-word at a page boundary
("...may handle hydrocodone-only ex"), so it is not verbatim-verified and nothing in
these items asserts it.

No new rule record is created. Both propositions are already carried verbatim by existing
canonical rules — MA-CII-SUPPORT-HANDLING already states 247 CMR 8.05(3), and
MA-CE-ANNUAL-STRUCTURE already states 247 CMR 4.03(7) with the eight-hour figure in its
numeric_facts — so the repair keys previously unkeyed content rather than duplicating a rule.

Refuses to touch any question other than these two.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, load_json, load_records, question_audit_hash, semantic_content_hash, write_json


REPAIR_IDS = ["MA-Q-0241", "MA-Q-0256"]
REPAIR_DATE = "2026-08-19"

OLD_HASHES = {"MA-Q-0241": None, "MA-Q-0256": None}

REPAIRS = {
    "MA-Q-0241": {
        "family_id": "B3A_0241R1_MA_HYDROCODONE_ER_HANDLING_BAR",
        "topic": "Pharmacy personnel",
        "subtopic": "Product-specific handling prohibition",
        "difficulty": 5,
        "question_type": "SATA",
        "rule_ids": ["MA-CII-SUPPORT-HANDLING"],
        "stem": (
            "A Massachusetts pharmacy stocks a hydrocodone-only extended release product that is not "
            "formulated in an abuse deterrent form. The pharmacist on duty is working out how the "
            "regulation treats that product where support personnel are concerned. Which statements are "
            "correct? Select all that apply."
        ),
        "choices": [
            ("A", "The prohibition turns on whether the product is in an abuse deterrent form."),
            ("B", "The prohibition reaches every extended release opioid product the pharmacy stocks."),
            ("C", "It reaches pharmacy technician trainees as well as licensed and certified technicians."),
            ("D", "Pharmacist approval evidenced by written policies and procedures permits a certified technician to handle it."),
            ("E", "A hydrocodone-only extended release product in an abuse deterrent form falls outside the prohibition."),
        ],
        "correct_choice_ids": ["A", "C", "E"],
        "core_reasoning": (
            "247 CMR 8.05(3) provides that a certified pharmacy technician, pharmacy technician, or pharmacy "
            "technician trainee may not handle any hydrocodone-only extended release medication that is not "
            "in an abuse deterrent form. Two features of that sentence decide the item. It is drawn by "
            "product, so the abuse deterrent formulation is what removes a hydrocodone-only extended "
            "release product from its reach, and it names all three support-personnel categories, so a "
            "higher credential grade does not escape it. The pharmacist approval and written policies "
            "mechanism in 247 CMR 8.05(2) governs assistance with Schedule II controlled substances "
            "generally and does not qualify this prohibition."
        ),
        "choice_analysis": {
            "A": "Correct: the prohibition is written against medication that is not in an abuse deterrent form.",
            "B": "The prohibition is confined to hydrocodone-only extended release medication.",
            "C": "Correct: certified pharmacy technicians, pharmacy technicians and pharmacy technician trainees are all named.",
            "D": "That approval mechanism belongs to 247 CMR 8.05(2) and does not qualify the 247 CMR 8.05(3) prohibition.",
            "E": "Correct: an abuse deterrent formulation is outside the sentence's reach.",
        },
        "reasoning_steps": [
            "Identify the product as hydrocodone-only extended release and not in an abuse deterrent form",
            "Read the prohibition as drawn by product formulation rather than by credential grade",
            "Confirm that all three support-personnel categories are named and that no approval mechanism qualifies it",
        ],
        "related_facts": [
            "247 CMR 8.05(1) places accountability for and security of Schedule II controlled substances directly on the pharmacist.",
        ],
        "mpje_trap": (
            "A product-specific prohibition does not bend to the credential ladder, so the certified "
            "technician's broader Schedule II role and the pharmacy's approved written policies both fail to reach it."
        ),
    },
    "MA-Q-0256": {
        "family_id": "B3A_0256R1_MA_CE_DAILY_CAP",
        "topic": "Licensure",
        "subtopic": "Continuing education daily cap",
        "difficulty": 5,
        "question_type": "SBA",
        "rule_ids": ["MA-CE-ANNUAL-STRUCTURE"],
        "stem": (
            "A Massachusetts pharmacist is behind on continuing education for the current calendar year. "
            "She attends an intensive live conference held on a single day in December and the authorized "
            "provider issues her a statement of credit for 12 contact hours earned that day. She wants to "
            "apply all 12 to that calendar year. How many of those contact hours may she apply?"
        ),
        "choices": [
            ("A", "The full 12, because the daily restriction applies to home study rather than live programs."),
            ("B", "The full 12, because live conference programming carries no daily restriction."),
            ("C", "Ten, because a registrant may not exceed ten contact hours in a calendar day."),
            ("D", "None, because contact hours earned in December are credited to the following cycle."),
            ("E", "Eight, because a registrant may not earn more than eight contact hours in a calendar day."),
        ],
        "correct_choice_ids": ["E"],
        "core_reasoning": (
            "247 CMR 4.03(7) provides that a registrant may not earn more than eight contact hours of "
            "continuing education in a calendar day. The provision is written without reference to delivery "
            "format, so it binds a live conference as it would home study, and it caps the day rather than "
            "the year. Eight of the 12 hours issued for that single day may therefore be applied."
        ),
        "choice_analysis": {
            "A": "247 CMR 4.03(7) is silent as to format; the home-study limit is the separate 15-hour annual cap in 247 CMR 4.03(4)(b).",
            "B": "The daily cap is not disapplied for live programming.",
            "C": "The figure in 247 CMR 4.03(7) is eight contact hours, not ten.",
            "D": "No provision defers December hours to the following cycle; hours are attributed to the calendar year in which they are earned.",
            "E": "Correct: the daily cap is eight contact hours.",
        },
        "reasoning_steps": [
            "Recognise that the constraint at issue is a per-calendar-day cap rather than an annual total",
            "Note that 247 CMR 4.03(7) does not distinguish delivery format",
            "Apply the eight-hour figure to the single day of attendance",
        ],
        "related_facts": [
            "Contact hours may not be carried over from one calendar year to another under 247 CMR 4.03(5).",
        ],
        "mpje_trap": (
            "The annual arithmetic is a distraction: a single day cannot yield more than eight contact "
            "hours however long the programme runs or however it is delivered."
        ),
    },
}


def main() -> int:
    questions = {record["question_id"]: record for path, record in load_records(DATA / "questions")}
    existing_rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}

    for rule_id, record in existing_rules.items():
        if semantic_content_hash(record, "rule") != record["content_hash"]:
            raise SystemExit(f"{rule_id} content hash has drifted; refusing to repair on a drifted tree")

    for question_id in REPAIR_IDS:
        record = questions[question_id]
        if record.get("verification_status") == "RELEASED":
            raise SystemExit(f"{question_id} is RELEASED; a realism repair must not mutate released content")
        OLD_HASHES[question_id] = question_audit_hash(record)

    known_rules = set(existing_rules)
    new_hashes = {}
    for question_id, repair in REPAIRS.items():
        record = dict(questions[question_id])
        unknown = [r for r in repair["rule_ids"] if r not in known_rules]
        if unknown:
            raise SystemExit(f"{question_id} references unknown rules {unknown}")
        record.update(
            {
                "family_id": repair["family_id"],
                "topic": repair["topic"],
                "subtopic": repair["subtopic"],
                "difficulty": repair["difficulty"],
                "question_type": repair["question_type"],
                "stem": repair["stem"],
                "choices": [{"id": cid, "text": text} for cid, text in repair["choices"]],
                "correct_choice_ids": list(repair["correct_choice_ids"]),
                "rule_ids": list(repair["rule_ids"]),
                "drug_ids": [],
                "reasoning_steps": list(repair["reasoning_steps"]),
                "explanation": {
                    "core_reasoning": repair["core_reasoning"],
                    "choice_analysis": repair["choice_analysis"],
                    "related_facts": list(repair["related_facts"]),
                    "mpje_trap": repair["mpje_trap"],
                },
                # Repaired content carries no audit evidence until the focused REAUDIT returns.
                "verification_status": "AUDIT_PENDING",
                "lifecycle_status": "AUDIT_PENDING",
                "last_legal_review": REPAIR_DATE,
                "audits": [],
                "duplicate_review_status": "PENDING",
                "independent_audit_status": "PENDING",
                "final_adjudication": None,
            }
        )
        write_json(DATA / "questions" / f"{question_id.lower()}.json", record)
        new_hashes[question_id] = question_audit_hash(record)

    matrix_path = DATA / "exam_style" / "question_family_matrix.json"
    matrix = load_json(matrix_path)
    known_families = {family["family_id"] for family in matrix["families"]}
    retired = {questions[q]["family_id"] for q in REPAIR_IDS}
    matrix["families"] = [f for f in matrix["families"] if f["family_id"] not in retired]
    for question_id, repair in REPAIRS.items():
        if repair["family_id"] in known_families:
            raise SystemExit(f"{repair['family_id']} already exists; a repair family must be new")
        matrix["families"].append(
            {
                "family_id": repair["family_id"],
                "area": questions[question_id]["area"],
                "topic": repair["topic"],
                "subtopic": repair["subtopic"],
                "primary_rule_ids": list(repair["rule_ids"]),
                "secondary_rule_ids": [],
                "scenario_types": ["practice scenario"],
                "common_traps": [repair["mpje_trap"]],
                "target_difficulties": [repair["difficulty"]],
                "target_item_types": [repair["question_type"]],
                "drug_required": False,
                "max_questions_in_final_bank": 2,
                "current_candidate_count": 1,
                "current_released_count": 0,
            }
        )
    write_json(matrix_path, matrix)
    print(f"retired families {sorted(retired)} and added {sorted(r['family_id'] for r in REPAIRS.values())}")

    for question_id in REPAIR_IDS:
        print(f"{question_id}: {OLD_HASHES[question_id]} -> {new_hashes[question_id]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
