from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "data" / "questions"

PATCHES = {
    "MA-Q-0093": {
        "choices": {
            "A": "Dispense the brand unless the patient specifically requests the interchangeable product."
        },
        "choice_analysis": {
            "A": "Patient preference does not create a prescriber no-substitution direction or reverse the Massachusetts interchange default."
        },
    },
    "MA-Q-0096": {
        "choices": {
            "D": "The pathway includes vaginal rings and injectable contraceptives whenever the patient prefers those dosage forms."
        },
        "correct_choice_ids": ["A", "C"],
        "choice_analysis": {
            "D": "The current pathway is limited to eligible patches and self-administered oral hormonal contraceptives; patient preference does not expand the authorized dosage forms."
        },
        "core_reasoning": "The pathway is bounded by required screening, the official protocol and labeling, and the specifically authorized dosage forms. Eligible patches and self-administered oral hormonal contraceptives are within scope; other dosage forms are not added by patient preference.",
    },
    "MA-Q-0100": {
        "choices": {
            "E": "Retail CDTM requires a referred, consenting adult within the disease, agreement, and setting limits."
        },
    },
    "MA-Q-0104": {
        "choices": {
            "C": "247 CMR 8 limits technician and trainee duties; an internal policy cannot delegate pharmacist judgment."
        },
    },
    "MA-Q-0105": {
        "choices": {
            "E": "Schedule II handling depends on personnel category and supervision; pharmacist judgment remains nondelegable."
        },
    },
    "MA-Q-0108": {
        "choices": {
            "A": "The general rule requires 20 contact hours in each calendar year of the two-year cycle."
        },
    },
    "MA-Q-0109": {
        "choices": {
            "A": "Compounding CE is entirely federal and adds no Massachusetts pharmacist requirement.",
            "B": "Technician training replaces the pharmacist’s ordinary renewal CE.",
            "E": "The compounding CE rule applies to patients rather than pharmacists."
        },
        "choice_analysis": {
            "A": "Massachusetts has a pharmacist CE requirement tied to covered compounding activity.",
            "B": "Compounding CE supplements rather than replaces the general pharmacist renewal framework.",
            "E": "The requirement is imposed on pharmacists engaged in or overseeing the covered activity."
        },
    },
    "MA-Q-0118": {
        "choices": {
            "C": "The prescription must include required patient, practitioner, drug, strength, directions, date, registration, cautionary, and refill information."
        },
    },
    "MA-Q-0121": {
        "choices": {
            "B": "Qualifying out-of-state Schedule III-VI prescriptions may be filled within 30 days; Schedule III-V require pharmacist verification."
        },
    },
    "MA-Q-0122": {
        "choices": {
            "D": "Massachusetts Schedule VI covers prescription drugs outside Schedules I-V and has no federal counterpart."
        },
        "core_reasoning": "Massachusetts uses Schedule VI for prescription drugs not otherwise assigned to Schedules I-V. Federal law has no Schedule VI category, so Massachusetts Schedule VI status alone does not establish federal controlled status.",
    },
}


def apply_patch(question: dict, patch: dict) -> None:
    choice_map = {choice["id"]: choice for choice in question["choices"]}
    for choice_id, text in patch.get("choices", {}).items():
        choice_map[choice_id]["text"] = text
    if "correct_choice_ids" in patch:
        question["correct_choice_ids"] = patch["correct_choice_ids"]
    if "core_reasoning" in patch:
        question["explanation"]["core_reasoning"] = patch["core_reasoning"]
    for choice_id, text in patch.get("choice_analysis", {}).items():
        question["explanation"]["choice_analysis"][choice_id] = text


def main() -> None:
    for question_id, patch in PATCHES.items():
        number = int(question_id.rsplit("-", 1)[1])
        path = QUESTIONS / f"ma-q-{number:04d}.json"
        question = json.loads(path.read_text(encoding="utf-8"))
        if question["question_id"] != question_id:
            raise SystemExit(f"Question ID mismatch in {path}")
        apply_patch(question, patch)
        path.write_text(json.dumps(question, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Applied structural/realism fixes to {len(PATCHES)} Batch 1 questions.")


if __name__ == "__main__":
    main()
