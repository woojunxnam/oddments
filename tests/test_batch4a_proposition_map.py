from __future__ import annotations

from collections import Counter

from qa_common import DATA, load_json, load_records


def test_batch4a_final_map_is_complete_current_and_within_headroom(root) -> None:
    path = root / "audits" / "coverage" / "2026-09-01" / "B4-A-PROPOSITION-MAP-FINAL.json"
    report = load_json(path)
    slots = report["slots"]
    rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}
    families = {item["family_id"]: item for item in load_json(DATA / "exam_style" / "question_family_matrix.json")["families"]}

    assert report["status"] == "FINAL_REVIEWED_FOR_AUTHORING"
    assert [slot["question_id"] for slot in slots] == [f"MA-Q-{number:04d}" for number in range(407, 440)]
    assert Counter(slot["area"] for slot in slots) == {1: 9, 2: 12, 3: 7, 4: 5}
    assert report["multi_rule_count"] == sum(slot["multi_rule"] for slot in slots) == 14
    assert report["controls"]["area4_compounding_slot_count"] == 2
    assert report["controls"]["cdtm_slot_count"] == 1
    assert report["authority_review"]["final_unresolved_authority_risks"] == 0

    for slot in slots:
        assert slot["family_id"] in families
        assert slot["family_headroom_at_review"] >= 1
        assert slot["planned_question_type"] in {"SBA", "SATA"}
        assert 3 <= slot["planned_difficulty"] <= 5
        assert "MA-MH-SUD-ADMIN" not in slot["rule_ids"]
        assert slot["closest_existing_question_ids"]
        assert slot["novelty_rationale"]
        assert set(slot["rule_ids"]) == {item["rule_id"] for item in slot["official_authority"]}
        for dependency in slot["official_authority"]:
            rule = rules[dependency["rule_id"]]
            assert rule["status"] == "CURRENT"
            assert dependency["content_hash"] == rule["content_hash"]
            assert dependency["content_version"] == rule["content_version"]
            assert dependency["authorities"]
