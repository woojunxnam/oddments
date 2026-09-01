from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def canonical_released_ids() -> set[str]:
    expected_ids: set[str] = set()
    for path in (ROOT / "data" / "questions").glob("*.json"):
        question = json.loads(path.read_text(encoding="utf-8"))
        if (
            question.get("verification_status") == "RELEASED"
            and question.get("lifecycle_status") == "RELEASED"
        ):
            expected_ids.add(question["question_id"])
    return expected_ids


def test_production_release_build_matches_canonical_released_set(tmp_path: Path) -> None:
    output = tmp_path / "released-questions.json"
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_site_data.py"), "--output", str(output)],
        cwd=ROOT,
        check=True,
    )
    payload = json.loads(output.read_text(encoding="utf-8"))

    expected_ids = canonical_released_ids()

    actual_ids = {question["question_id"] for question in payload.get("questions", [])}
    assert actual_ids == expected_ids
    assert payload["meta"]["question_count"] == len(expected_ids)
    assert payload["meta"]["release_status"] == (
        "RELEASE_AVAILABLE" if expected_ids else "NO_RELEASED_QUESTIONS"
    )


def test_tracked_public_payload_is_release_only_and_not_client_filtered() -> None:
    payload = json.loads((ROOT / "site" / "generated" / "questions.json").read_text(encoding="utf-8"))
    actual_ids = {question["question_id"] for question in payload["questions"]}

    assert actual_ids == canonical_released_ids()
    assert payload["meta"]["question_count"] == 366
    assert payload["meta"]["development_fixture_mode"] is False
    assert "MA-Q-0028" not in actual_ids
    assert "MA-Q-0172" not in actual_ids
    assert all(question["verification_status"] == "RELEASED" for question in payload["questions"])
    assert all(question["lifecycle_status"] == "RELEASED" for question in payload["questions"])
    assert "preview-filter.js" not in (ROOT / "site" / "index.html").read_text(encoding="utf-8")
