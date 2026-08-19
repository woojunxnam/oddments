"""Batch 3 B3-B realism repair R1 — MA-Q-0288 only.

CLAUDE-FRESH-B3B returned legal KEEP / Existing_Answer_Correct YES and realism
MINOR_EDIT / FAIL on the single criterion authentic_distractors. Two defects, both in
item construction rather than law, and both mine as author:

  1. Under the old key A/C/D/E the only incorrect option was "that the patient has no
     outstanding account balance with the pharmacy", which has no regulatory nexus to
     247 CMR 9.15(2). The whole discriminating power of a five-option SATA rested on one
     distractor no prepared candidate would credit.
  2. The old stem asked which determinations the pharmacist must "still" make after the
     prescriber confirmed authorship by telephone. That supports a reasonable reading on
     which determination (c), authenticity, has been discharged. It is the single item in
     the tranche where the auditor's Phase-1 blind answer diverged from the key, and the
     divergence was exactly that reading.

The repair changes the construction rather than paraphrasing it:

  * The telephone-confirmation framing is removed entirely, so nothing in the scenario
    discharges any determination and the enumerative reading is the only reading.
  * The item now discriminates the 247 CMR 9.15(2) determinations from two genuinely
    adjacent Massachusetts obligations, so both incorrect options are ones a prepared
    candidate could credit:
      - verifying that the prescriber holds a current Massachusetts Controlled Substances
        Registration, which is plausible because 247 CMR 9.15 is headed "Verifying a
        Practitioner's Prescriptive Authority" yet is not among the enumerated
        determinations; and
      - screening the patient's history in the Prescription Monitoring Program, which is
        plausible because the immediately preceding paragraph, 247 CMR 9.15(1), imposes a
        monitoring-program obligation, but that paragraph requires registration and
        maintained login information rather than a determination about the prescription.

Authority re-opened independently for this repair. Verbatim from the official published
247 CMR 9.00 (12/6/24), section 9.15 "Verifying a Practitioner's Prescriptive Authority":

  (1) A pharmacist who dispenses medications reported to the Massachusetts Prescription
      Monitoring Program ("PMP") shall register with and maintain login information for
      the electronic system to monitor the prescribing and dispensing of controlled
      substances authorized by M.G.L. c. 94C, s. 24A, known as PMP or MassPAT.
  (2) A pharmacist may not fill a prescription unless the pharmacist, in the exercise of
      his or her professional judgment, determines that:
      (a) the prescription was issued for a legitimate medical purpose by a practitioner
          acting in the usual course of his or her professional practice;
      (b) there is a valid patient-practitioner relationship;
      (c) the prescription is authentic; and
      (d) the dispensing is in accordance with M.G.L. c. 94C, s. 19(a).

The schema caps a question at five choices, so the offered set carries three of the four
determinations and the two adjacent duties. The fourth determination, compliance with
M.G.L. c. 94C, s. 19(a), is named in related_facts so the explanation stays complete.

No new rule record is created. MA-PRESCRIPTION-VALIDITY-DETERMINATION already carries
247 CMR 9.15(2) and MA-PMP-REGISTRATION-DUTY already carries 247 CMR 9.15(1); the repaired
item cites both because its reasoning turns on the boundary between them.

Refuses to touch any question other than MA-Q-0288.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, load_json, load_records, question_audit_hash, semantic_content_hash, write_json


REPAIR_ID = "MA-Q-0288"
REPAIR_DATE = "2026-08-19"

REPAIR = {
    "family_id": "B3B_0288R1_MA_VALIDITY_VS_ADJACENT_DUTIES",
    "topic": "Pharmacist practice",
    "subtopic": "Determinations versus adjacent duties",
    "difficulty": 5,
    "question_type": "SATA",
    "rule_ids": ["MA-PRESCRIPTION-VALIDITY-DETERMINATION", "MA-PMP-REGISTRATION-DUTY"],
    "stem": (
        "A newly licensed Massachusetts pharmacist is about to fill prescriptions on her own for the "
        "first time and asks her preceptor what the regulation requires of her professional judgment "
        "before any prescription may be filled. Which of the following are among the determinations the "
        "regulation requires her to make? Select all that apply."
    ),
    "choices": [
        ("A", "That the prescriber holds a current Massachusetts Controlled Substances Registration."),
        ("B", "That the prescription was issued for a legitimate medical purpose by a practitioner acting in the usual course of professional practice."),
        ("C", "That there is a valid patient-practitioner relationship."),
        ("D", "That the patient's history has been screened in the Prescription Monitoring Program."),
        ("E", "That the prescription is authentic."),
    ],
    "correct_choice_ids": ["B", "C", "E"],
    "core_reasoning": (
        "247 CMR 9.15(2) permits a pharmacist to fill a prescription only where the pharmacist, in the "
        "exercise of professional judgment, determines that the prescription was issued for a legitimate "
        "medical purpose by a practitioner acting in the usual course of professional practice, that "
        "there is a valid patient-practitioner relationship, that the prescription is authentic, and that "
        "the dispensing is in accordance with M.G.L. c. 94C, section 19(a). Two obligations that sit "
        "immediately around that list are not on it. The section is headed Verifying a Practitioner's "
        "Prescriptive Authority, but confirming a current Massachusetts Controlled Substances "
        "Registration is not one of the enumerated determinations. 247 CMR 9.15(1) does impose a "
        "monitoring-program obligation, but it is to register with and maintain login information for "
        "the system, not to make a determination about the prescription in front of the pharmacist."
    ),
    "choice_analysis": {
        "A": "The section heading invites this, but registration verification is not among the determinations 247 CMR 9.15(2) enumerates.",
        "B": "Correct: this is the determination in 247 CMR 9.15(2)(a).",
        "C": "Correct: this is the determination in 247 CMR 9.15(2)(b).",
        "D": "247 CMR 9.15(1) requires registration with and maintained login information for the monitoring program, which is an access obligation rather than a determination.",
        "E": "Correct: this is the determination in 247 CMR 9.15(2)(c).",
    },
    "reasoning_steps": [
        "Separate the determinations enumerated in 247 CMR 9.15(2) from the neighbouring obligation in 247 CMR 9.15(1)",
        "Read the section heading as descriptive rather than as adding a registration-verification determination",
        "Select only the items the regulation states the pharmacist must determine",
    ],
    "related_facts": [
        "The fourth determination in 247 CMR 9.15(2) is that the dispensing is in accordance with M.G.L. c. 94C, section 19(a).",
    ],
    "mpje_trap": (
        "The section is headed after prescriptive authority and sits directly beside the "
        "monitoring-program duty, so two genuinely adjacent obligations read like determinations "
        "without appearing on the enumerated list."
    ),
}


def main() -> int:
    questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}
    rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}

    for rule_id, record in rules.items():
        if semantic_content_hash(record, "rule") != record["content_hash"]:
            raise SystemExit(f"{rule_id} content hash has drifted; refusing to repair on a drifted tree")

    record = questions[REPAIR_ID]
    if record.get("verification_status") == "RELEASED":
        raise SystemExit(f"{REPAIR_ID} is RELEASED; a realism repair must not mutate released content")
    old_hash = question_audit_hash(record)

    unknown = [r for r in REPAIR["rule_ids"] if r not in rules]
    if unknown:
        raise SystemExit(f"{REPAIR_ID} references unknown rules {unknown}")

    updated = dict(record)
    updated.update(
        {
            "family_id": REPAIR["family_id"],
            "topic": REPAIR["topic"],
            "subtopic": REPAIR["subtopic"],
            "difficulty": REPAIR["difficulty"],
            "question_type": REPAIR["question_type"],
            "stem": REPAIR["stem"],
            "choices": [{"id": cid, "text": text} for cid, text in REPAIR["choices"]],
            "correct_choice_ids": list(REPAIR["correct_choice_ids"]),
            "rule_ids": list(REPAIR["rule_ids"]),
            "drug_ids": [],
            "reasoning_steps": list(REPAIR["reasoning_steps"]),
            "explanation": {
                "core_reasoning": REPAIR["core_reasoning"],
                "choice_analysis": REPAIR["choice_analysis"],
                "related_facts": list(REPAIR["related_facts"]),
                "mpje_trap": REPAIR["mpje_trap"],
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
    write_json(DATA / "questions" / f"{REPAIR_ID.lower()}.json", updated)
    new_hash = question_audit_hash(updated)

    matrix_path = DATA / "exam_style" / "question_family_matrix.json"
    matrix = load_json(matrix_path)
    retired = record["family_id"]
    known = {family["family_id"] for family in matrix["families"]}
    if REPAIR["family_id"] in known:
        raise SystemExit(f"{REPAIR['family_id']} already exists; a repair family must be new")
    matrix["families"] = [f for f in matrix["families"] if f["family_id"] != retired]
    matrix["families"].append(
        {
            "family_id": REPAIR["family_id"],
            "area": record["area"],
            "topic": REPAIR["topic"],
            "subtopic": REPAIR["subtopic"],
            "primary_rule_ids": list(REPAIR["rule_ids"]),
            "secondary_rule_ids": [],
            "scenario_types": ["practice scenario"],
            "common_traps": [REPAIR["mpje_trap"]],
            "target_difficulties": [REPAIR["difficulty"]],
            "target_item_types": [REPAIR["question_type"]],
            "drug_required": False,
            "max_questions_in_final_bank": 2,
            "current_candidate_count": 1,
            "current_released_count": 0,
        }
    )
    write_json(matrix_path, matrix)

    print(f"retired family {retired} -> {REPAIR['family_id']}")
    print(f"{REPAIR_ID}: {old_hash} -> {new_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
