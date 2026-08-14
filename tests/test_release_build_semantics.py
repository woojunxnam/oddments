from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_production_release_build_matches_canonical_released_set(tmp_path: Path) -> None:
    output = tmp_path / "released-questions.json"
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_site_data.py"), "--output", str(output)],
        cwd=ROOT,
        check=True,
    )
    payload = json.loads(output.read_text(encoding="utf-8"))

    expected_ids: set[str] = set()
    for path in (ROOT / "data" / "questions").glob("*.json"):
        question = json.loads(path.read_text(encoding="utf-8"))
        if (
            question.get("verification_status") == "RELEASED"
            and question.get("lifecycle_status") == "RELEASED"
        ):
            expected_ids.add(question["question_id"])

    actual_ids = {question["question_id"] for question in payload.get("questions", [])}
    assert actual_ids == expected_ids
    assert payload["meta"]["question_count"] == len(expected_ids)
    assert payload["meta"]["release_status"] == (
        "RELEASE_AVAILABLE" if expected_ids else "NO_RELEASED_QUESTIONS"
    )
