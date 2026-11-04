from __future__ import annotations

from datetime import date

from qa_common import QAReport, dependency_snapshot, semantic_content_hash


def named_dependency_snapshot(record: dict, id_field: str) -> dict:
    return {"id": record.get(id_field), **dependency_snapshot(record)}


def style_profile_snapshot(profile: dict) -> dict:
    return {"profile_id": profile.get("profile_id"), **dependency_snapshot(profile)}


def validate_versioned_context(blueprint: dict, style_profile: dict) -> QAReport:
    report = QAReport()
    if blueprint.get("content_hash") != semantic_content_hash(blueprint, "blueprint"):
        report.error("data/blueprint.json: content_hash mismatch; run scripts/update_content_hashes.py")
    if style_profile.get("content_hash") != semantic_content_hash(style_profile, "style_profile"):
        report.error(
            "data/exam_style/mpje_style_profile.json: content_hash mismatch; "
            "run scripts/update_content_hashes.py"
        )
    if style_profile.get("valid_for_exams_before") != blueprint.get("applies_to_exams_before"):
        report.error("style profile validity date does not match the current blueprint")
    return report


def validate_release_date(
    blueprint: dict,
    style_profile: dict,
    *,
    reference_date: date,
    target_exam_date: date | None = None,
) -> QAReport:
    report = validate_versioned_context(blueprint, style_profile)
    target = target_exam_date or reference_date
    blueprint_cutoff = date.fromisoformat(blueprint["applies_to_exams_before"])
    profile_cutoff = date.fromisoformat(style_profile["valid_for_exams_before"])
    reverify_after = date.fromisoformat(blueprint["release_guard"]["must_reverify_after"])
    if target >= min(blueprint_cutoff, profile_cutoff) or target > reverify_after:
        report.error(
            "BLUEPRINT_REVIEW_REQUIRED: target exam date is outside the current blueprint/style-profile window"
        )
    return report
