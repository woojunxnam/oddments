from __future__ import annotations

from collections import Counter

from qa_common import DATA, load_json, load_records


def test_batch4a_candidates_match_final_map_when_present(root) -> None:
    proposition_map = load_json(
        root / "audits" / "coverage" / "2026-09-01" / "B4-A-PROPOSITION-MAP-FINAL.json"
    )
    questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}
    expected_ids = [f"MA-Q-{number:04d}" for number in range(407, 440)]
    present = [qid for qid in expected_ids if qid in questions]
    if not present:
        return

    assert present == expected_ids, "B4-A must enter the candidate bank as one complete locked range"
    slots = {slot["question_id"]: slot for slot in proposition_map["slots"]}
    selected = [questions[qid] for qid in expected_ids]
    for question in selected:
        slot = slots[question["question_id"]]
        assert question["family_id"] == slot["family_id"]
        assert question["area"] == slot["area"]
        assert question["difficulty"] == slot["planned_difficulty"]
        assert question["question_type"] == slot["planned_question_type"]
        assert question["rule_ids"] == slot["rule_ids"]
        assert question["provenance"] == "GEN"
        assert question["source_signal_ids"] == []
        assert question["verification_status"] == question["lifecycle_status"]
        if question["verification_status"] == "RELEASED":
            assert question["independent_audit_status"] == "PASSED"
            assert len(question["audits"]) >= 2
            assert question["final_adjudication"]["decision"] == "KEEP"
        else:
            assert question["verification_status"] == "AUDIT_PENDING"
            assert question["independent_audit_status"] == "PENDING"
            assert question["final_adjudication"] is None

    assert Counter(question["area"] for question in selected) == {1: 9, 2: 12, 3: 7, 4: 5}
    assert Counter(question["question_type"] for question in selected) == {"SBA": 19, "SATA": 14}
