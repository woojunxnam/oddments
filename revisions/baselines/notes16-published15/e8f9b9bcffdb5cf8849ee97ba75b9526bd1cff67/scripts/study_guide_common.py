from __future__ import annotations

from typing import Any

from qa_common import deterministic_hash


# The content model is versioned because the hash is taken over a fixed field list, and a
# frozen audit package records the hash of the prose an auditor actually reviewed. If the
# field list simply grew, every historical package would stop verifying against its own
# recorded hash and the audit trail would be invalidated by an unrelated schema change.
# Freezing the list per version keeps an old package checkable forever.
STUDY_GUIDE_HASH_FIELDS_V1 = (
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

# V2 adds the teaching fields: expository orientation, comparison tables, worked examples
# and retrieval prompts. They are hashed like any other prose so an independent auditor
# adjudicates the teaching material, not only the legal assertions.
STUDY_GUIDE_HASH_FIELDS_V2 = (
    "section_id",
    "title",
    "areas",
    "topic",
    "subtopic",
    "learning_objectives",
    "rule_ids",
    "verified_rule_dependencies",
    "orientation",
    "comparison_tables",
    "worked_examples",
    "retrieval_prompts",
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

STUDY_GUIDE_HASH_FIELD_SETS = {
    1: STUDY_GUIDE_HASH_FIELDS_V1,
    2: STUDY_GUIDE_HASH_FIELDS_V2,
}
CURRENT_CONTENT_MODEL_VERSION = 2
STUDY_GUIDE_HASH_FIELDS = STUDY_GUIDE_HASH_FIELD_SETS[CURRENT_CONTENT_MODEL_VERSION]


def study_guide_content_hash(section: dict[str, Any], *, model_version: int | None = None) -> str:
    """Hash a section under a given content model.

    `model_version` is for re-deriving the hash of a snapshot frozen under an earlier model;
    live sections always use the current one.
    """
    fields = STUDY_GUIDE_HASH_FIELD_SETS[model_version or CURRENT_CONTENT_MODEL_VERSION]
    return deterministic_hash({field: section.get(field) for field in fields})


# Every field whose entries carry rule_ids directly. A comparison table is handled
# separately because its grounding sits on each row rather than on the table.
GROUNDED_FIELDS = (
    "orientation",
    "worked_examples",
    "retrieval_prompts",
    "quick_review",
    "decision_logic",
    "ma_vs_federal",
    "exceptions",
    "timing_deadlines",
    "forms_records",
    "role_duties",
    "common_traps",
    "drug_examples",
)


def legal_point_rule_ids(section: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for field in GROUNDED_FIELDS:
        for item in section.get(field, []):
            ids.update(item.get("rule_ids", []))
    for table in section.get("comparison_tables", []):
        for row in table.get("rows", []):
            ids.update(row.get("rule_ids", []))
    return ids
