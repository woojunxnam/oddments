from __future__ import annotations

from typing import Any

from qa_common import deterministic_hash


STUDY_GUIDE_HASH_FIELDS = (
    "section_id",
    "title",
    "areas",
    "topic",
    "subtopic",
    "learning_objectives",
    "rule_ids",
    "verified_rule_dependencies",
    "quick_review",
    "decision_logic",
    "ma_vs_federal",
    "exceptions",
    "timing_deadlines",
    "forms_records",
    "role_duties",
    "common_traps",
    "drug_examples",
    "practice_question_ids",
)


def study_guide_content_hash(section: dict[str, Any]) -> str:
    return deterministic_hash({field: section.get(field) for field in STUDY_GUIDE_HASH_FIELDS})


def legal_point_rule_ids(section: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for field in (
        "quick_review",
        "decision_logic",
        "ma_vs_federal",
        "exceptions",
        "timing_deadlines",
        "forms_records",
        "role_duties",
        "common_traps",
        "drug_examples",
    ):
        for item in section.get(field, []):
            ids.update(item.get("rule_ids", []))
    return ids
