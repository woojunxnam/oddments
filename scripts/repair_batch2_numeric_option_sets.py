from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS = ROOT / "data" / "questions"

PATCHES = {
    "MA-Q-0153": {
        "A": "A maximum stock of 40 analgesic units",
        "B": "A maximum stock of 60 analgesic units",
        "C": "A maximum stock of 75 analgesic units",
        "D": "A maximum stock of 100 analgesic units",
        "E": "A maximum stock of 150 analgesic units",
    },
    "MA-Q-0190": {
        "A": "A 72-hour partial-fill window",
        "B": "A 7-day partial-fill window",
        "C": "A 90-day partial-fill window",
        "D": "A 60-day period measured from the prescription issue date",
        "E": "A 6-month partial-fill window",
    },
}


def main() -> int:
    for qid, replacements in PATCHES.items():
        path = QUESTIONS / f"{qid.lower()}.json"
        question = json.loads(path.read_text(encoding="utf-8"))
        by_id = {choice["id"]: choice for choice in question["choices"]}
        for choice_id, text in replacements.items():
            by_id[choice_id]["text"] = text
        path.write_text(json.dumps(question, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"repaired normalized numeric option sets for {len(PATCHES)} Batch 2 questions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
