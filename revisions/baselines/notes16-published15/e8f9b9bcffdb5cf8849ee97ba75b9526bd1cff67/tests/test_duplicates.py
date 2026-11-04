from __future__ import annotations

from copy import deepcopy

from conftest import write_question


def test_exact_duplicate_stems_are_reported(tmp_path, monkeypatch, canonical_question) -> None:
    import detect_duplicates as module

    first = deepcopy(canonical_question)
    second = deepcopy(canonical_question)
    second["question_id"] = "MA-Q-9999"
    second["family_id"] = "MANUAL_DUPLICATE_TEST"
    temp_data = tmp_path / "data"
    write_question(temp_data, first, "first.json")
    write_question(temp_data, second, "second.json")
    monkeypatch.setattr(module, "DATA", temp_data)
    report = module.detect_duplicates()
    assert report["finding_count"] >= 1
    assert "EXACT_STEM" in report["findings"][0]["match_types"]
    assert report["findings"][0]["recommended_manual_review"] is True


def test_normalized_numeric_duplicate_stems_are_reported(tmp_path, monkeypatch, canonical_question) -> None:
    import detect_duplicates as module

    first = deepcopy(canonical_question)
    second = deepcopy(canonical_question)
    second["question_id"] = "MA-Q-9998"
    second["stem"] = first["stem"].replace("five months", "four months").replace("five times", "four times")
    temp_data = tmp_path / "data"
    write_question(temp_data, first, "first.json")
    write_question(temp_data, second, "second.json")
    monkeypatch.setattr(module, "DATA", temp_data)
    report = module.detect_duplicates()
    assert report["finding_count"] >= 1
    assert any("FUZZY_LOCAL" in finding["match_types"] for finding in report["findings"])

