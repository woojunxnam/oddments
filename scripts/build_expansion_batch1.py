from __future__ import annotations

import base64
import gzip
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS_DIR = ROOT / "data" / "questions"
MATRIX_PATH = ROOT / "data" / "exam_style" / "question_family_matrix.json"
PAYLOAD_DIR = ROOT / "scripts" / "expansion_batch1_payload"


def load_questions() -> list[dict]:
    parts = sorted(PAYLOAD_DIR.glob("*.txt"))
    if len(parts) != 8:
        raise SystemExit(f"Expected 8 payload chunks, found {len(parts)}")
    payload = "".join(path.read_text(encoding="utf-8").strip() for path in parts)
    if len(payload) != 30148:
        raise SystemExit(f"Unexpected payload length: {len(payload)}")
    decoded = gzip.decompress(base64.b64decode(payload)).decode("utf-8")
    return json.loads(decoded)


QUESTIONS = load_questions()


def family_for(question: dict) -> dict:
    return {
        "family_id": question["family_id"],
        "area": question["area"],
        "topic": question["topic"],
        "subtopic": question["subtopic"],
        "primary_rule_ids": question["rule_ids"][:1],
        "secondary_rule_ids": question["rule_ids"][1:],
        "drug_required": bool(question["drug_ids"]),
        "scenario_types": [question["question_type"].lower()],
        "common_traps": [question["explanation"]["mpje_trap"]],
        "target_difficulties": [question["difficulty"]],
        "target_item_types": [question["question_type"]],
        "max_questions_in_final_bank": 2,
        "current_candidate_count": 1,
        "current_released_count": 0,
    }


def main() -> None:
    QUESTIONS_DIR.mkdir(parents=True, exist_ok=True)
    expected_ids = [f"MA-Q-{number:04d}" for number in range(91, 131)]
    actual_ids = [question["question_id"] for question in QUESTIONS]
    if actual_ids != expected_ids:
        raise SystemExit(f"Expansion IDs are not exact/ordered: {actual_ids}")

    for question in QUESTIONS:
        number = int(question["question_id"].rsplit("-", 1)[1])
        path = QUESTIONS_DIR / f"ma-q-{number:04d}.json"
        path.write_text(json.dumps(question, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    expansion_ids = {question["family_id"] for question in QUESTIONS}
    matrix["families"] = [
        family for family in matrix["families"] if family.get("family_id") not in expansion_ids
    ]
    matrix["families"].extend(family_for(question) for question in QUESTIONS)
    matrix["last_reviewed"] = "2026-08-14"
    MATRIX_PATH.write_text(json.dumps(matrix, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    checker_path = ROOT / "scripts" / "check_structural_patterns.py"
    checker_text = checker_path.read_text(encoding="utf-8")
    checker_text = checker_text.replace(
        'PHASE2_IDS = {f"MA-Q-{number:04d}" for number in range(11, 91)}',
        'PHASE2_IDS = {f"MA-Q-{number:04d}" for number in range(11, 10000)}',
    )
    checker_text = checker_text.replace(
        '"scope": "MA-Q-0011..MA-Q-0090" if questions is None else "provided questions",',
        '"scope": "MA-Q-0011+" if questions is None else "provided questions",',
    )
    checker_path.write_text(checker_text, encoding="utf-8")

    print(f"Wrote {len(QUESTIONS)} expansion questions and {len(expansion_ids)} family rows.")


if __name__ == "__main__":
    main()
