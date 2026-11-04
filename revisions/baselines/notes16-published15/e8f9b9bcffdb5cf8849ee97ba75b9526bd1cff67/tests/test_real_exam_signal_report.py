from __future__ import annotations

from qa_common import load_json


def test_batch4_real_exam_signal_report_has_measured_sources_and_discards_recall(root) -> None:
    report = load_json(
        root / "audits" / "coverage" / "2026-09-01" / "BATCH4-REAL-EXAM-SIGNAL-REPORT.json"
    )
    counts = report["sources_reviewed"]
    assert counts["official_source_count"] == len(report["official_sources"]) == 8
    assert counts["Massachusetts_report_count"] == len(report["Massachusetts_candidate_reports"]) == 20
    assert counts["cross_state_report_count"] == len(report["cross_state_candidate_reports"]) == 26
    assert counts["all_evidence_record_count"] == 54

    records = (
        report["official_sources"]
        + report["Massachusetts_candidate_reports"]
        + report["cross_state_candidate_reports"]
    )
    source_ids = [record["source_id"] for record in records]
    assert len(source_ids) == len(set(source_ids)) == 54
    assert all(record["source_url"].startswith("https://") for record in records)

    discarded = report["prohibited_recall_content_encountered_and_discarded_count"]
    assert discarded["report_level_encounter_count"] == 9
    assert discarded["discarded_content_unit_count"] == 17
    assert discarded["retained_recalled_question_count"] == 0
    assert discarded["retained_answer_choice_count"] == 0
    assert discarded["retained_candidate_answer_correctness_inference_count"] == 0
    assert discarded["verdict"] == "ALL_RECALL_DETAILS_DISCARDED"

    eras = report["blueprint_era_separation"]
    assert list(eras["pre_2027_current"]["weights_percent"].values()) == [22, 33, 24, 21]
    assert list(eras["post_2027_future"]["weights_percent"].values()) == [30, 30, 20, 20]
    assert eras["mixing_verdict"] == "ERA_SEPARATED"
