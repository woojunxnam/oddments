from __future__ import annotations

from qa_common import DATA, load_json, write_json


CHOICE_TEXT_UPDATES = {
    "MA-Q-0107": {
        "B": "23 hours: Monday contributes 11 hours and Tuesday is capped at 12 hours."
    },
    "MA-Q-0112": {
        "C": "Promptly address the patient or representative, provide directions to correct or minimize harm, and notify the prescriber as professional judgment indicates."
    },
    "MA-Q-0114": {
        "D": "Annual CQI education extends to pharmacy personnel, so support staff cannot be excluded solely for lacking final judgment authority."
    },
    "MA-Q-0116": {
        "E": "Keep the serious-event records; their retention period is at least five years from report filing."
    },
    "MA-Q-0117": {
        "C": "For this qualifying return, accept it, quarantine it outside saleable inventory, and arrange proper disposition."
    },
    "MA-Q-0122": {
        "C": "Do not import federal Schedule II or III-V controls solely from Massachusetts Schedule VI status; determine federal scheduling separately."
    },
    "MA-Q-0124": {
        "B": "Use the Schedule III-V oral pathway; record a request for the practitioner's written prescription within seven days or any shorter controlling federal period."
    },
    "MA-Q-0125": {
        "C": "July 10, the registrant's first day of controlled-substance activity."
    }
}


def main() -> int:
    for qid, updates in CHOICE_TEXT_UPDATES.items():
        path = DATA / "questions" / f"ma-q-{qid[-4:]}.json"
        record = load_json(path)
        choices = {choice["id"]: choice for choice in record["choices"]}
        for choice_id, text in updates.items():
            choices[choice_id]["text"] = text
        write_json(path, record)
    print(f"polished answer-cue balance in {len(CHOICE_TEXT_UPDATES)} Batch 1 v2 questions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
