"""Deterministic smoke tests for read-only Next40 duplicate screening."""
import importlib.util
import json
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "next40_duplicate_screen", Path(__file__).resolve().parents[1] / "scripts/next40_duplicate_screen.py"
)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def test_scan_sample_and_no_false_clear(tmp_path):
    sample = tmp_path / "practice_expansion" / "sample" / "questions.json"
    sample.parent.mkdir(parents=True)
    sample.write_text(json.dumps({"questions": [
        {"question_id": "X1", "stem": "A nonsterile compounding designated area is required.", "choices": []},
        {"question_id": "X2", "stem": "An attorney subpoena seeks HIPAA records without a protective order.", "choices": []},
    ]}), encoding="utf-8")
    out = module.screen(tmp_path)
    assert out["total_record_occurrences"] == 2
    assert out["probes"]["IMG_0005_nonsterile_area"]["top"][0]["id"] == "X1"
    assert out["probes"]["IMG_0040_civil_subpoena"]["top"][0]["id"] == "X2"
    assert out["duplicate_review_status"] == "NOT_CLEAR_NEEDS_HUMAN_FULL_TEXT_COMPARISON"


def test_canonical_one_question_file(tmp_path):
    q = tmp_path / "data/questions/ma-q-0001.json"
    q.parent.mkdir(parents=True)
    q.write_text(json.dumps({"question_id": "M1", "stem": "Medicare pharmacy referral kickback payment"}))
    out = module.screen(tmp_path)
    assert out["source_counts"]["data/questions/ma-q-0001.json"] == 1
    assert out["probes"]["IMG_0008_referral_payment"]["top"][0]["id"] == "M1"
