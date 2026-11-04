import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_batch4_phase0_artifacts_freeze_measured_main_state(root: Path) -> None:
    coverage = root / "audits" / "coverage" / "2026-09-01"
    inventory = load(coverage / "BATCH4-BASELINE-INVENTORY.json")
    propositions = load(coverage / "BATCH4-PROPOSITION-CENSUS.json")
    families = load(coverage / "BATCH4-FAMILY-HEADROOM.json")
    plan = load(coverage / "BATCH4-PLAN-V1.json")

    assert inventory["github"]["source_live_main_sha"] == "5f07f49e43d50dff7a8a2f8c49f0a58135d120d7"
    assert inventory["bank"]["released_questions"] == 366
    assert inventory["bank"]["released_by_area"] == {"1": 78, "2": 120, "3": 93, "4": 75}
    assert inventory["four_exam_target"]["deficit_by_area"] == {"1": 26, "2": 40, "3": 23, "4": 25}
    assert inventory["four_exam_target"]["deficit_total"] == 114
    assert inventory["unreleased_capacity"]["current_release_usable_capacity"] == 0
    assert inventory["bank"]["next_free_question_id"] == "MA-Q-0407"

    assert propositions["summary"]["released_questions"] == 366
    assert propositions["summary"]["atomic_competencies_passed"] == 46
    assert propositions["summary"]["atomic_competencies_total"] == 46
    assert families["summary"]["families_in_matrix"] == 455
    assert families["summary"]["saturated_family_count"] == 46
    assert families["summary"]["matrix_count_mismatches"] == []

    assert plan["controller_issue"] == 121
    assert plan["question_target"]["candidate_count"] == 132
    assert plan["question_target"]["reserved_range"] == {
        "first_id": "MA-Q-0407",
        "last_id": "MA-Q-0538",
        "contiguous": True,
    }
    assert sum(tranche["count"] for tranche in plan["question_target"]["tranches"]) == 132
