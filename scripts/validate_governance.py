from __future__ import annotations

from collections import Counter

from qa_common import DATA, SCHEMAS, QAReport, index_records, load_records, load_json, print_report, validate_schema_records
from release_context import validate_versioned_context


def validate_family_matrix(
    matrix: dict,
    questions: dict[str, dict],
    rules: dict[str, dict],
    matrix_path: object = "question_family_matrix.json",
) -> QAReport:
    report = QAReport()
    family_ids = [family.get("family_id") for family in matrix.get("families", [])]
    if len(family_ids) != len(set(family_ids)):
        report.error(f"{matrix_path}: duplicate family_id")
    actual_counts = Counter(question.get("family_id") for question in questions.values())
    matrix_families = {family.get("family_id"): family for family in matrix.get("families", [])}
    missing_families = set(actual_counts) - set(matrix_families)
    if missing_families:
        report.error(f"{matrix_path}: actual question families missing from matrix: {sorted(missing_families)}")
    released_counts = Counter(
        question.get("family_id")
        for question in questions.values()
        if question.get("verification_status") == "RELEASED"
        and question.get("lifecycle_status") == "RELEASED"
    )
    for family_id, family in matrix_families.items():
        candidate_count = actual_counts.get(family_id, 0)
        released_count = released_counts.get(family_id, 0)
        if family.get("current_candidate_count") != candidate_count:
            report.error(f"{matrix_path}: stale current_candidate_count for {family_id}")
        if family.get("current_released_count") != released_count:
            report.error(f"{matrix_path}: stale current_released_count for {family_id}")
        maximum = family.get("max_questions_in_final_bank", 0)
        if released_count > maximum:
            report.error(f"{matrix_path}: released family {family_id} exceeds max_questions_in_final_bank")
        elif candidate_count > maximum:
            report.warn(
                f"{matrix_path}: candidate family {family_id} has {candidate_count} candidates "
                f"for a final-bank maximum of {maximum}"
            )
        for rule_id in family.get("primary_rule_ids", []) + family.get("secondary_rule_ids", []):
            if rule_id not in rules:
                report.error(f"{matrix_path}: {family_id} references unknown rule_id {rule_id}")
    return report


def validate_governance(
    rules: dict[str, dict],
    questions: dict[str, dict],
) -> QAReport:
    report = QAReport()

    source_records = load_records(DATA / "source_manifests")
    validate_schema_records(source_records, SCHEMAS / "source_manifest.schema.json", report)
    sources = index_records(source_records, "source_id", report)

    signal_records = load_records(DATA / "source_signals")
    validate_schema_records(signal_records, SCHEMAS / "source_signal.schema.json", report)
    signals = index_records(signal_records, "signal_id", report)
    for path, signal in signal_records:
        source = sources.get(signal.get("source_id"))
        if source is None:
            report.error(f"{path}: source signal references unknown source_id {signal.get('source_id')}")
            continue
        if source.get("source_class") != "PUBLIC_NON_OFFICIAL":
            report.error(f"{path}: abstract source signals must derive only from PUBLIC_NON_OFFICIAL sources")
        if source.get("permission_status") != "VERIFIED":
            report.error(f"{path}: source permission is not VERIFIED")
        if not source.get("ai_processing_allowed") or not source.get("public_repo_allowed"):
            report.error(f"{path}: source permissions do not allow this public abstract signal")

    for question_id, question in questions.items():
        signal_ids = question.get("source_signal_ids", [])
        for signal_id in signal_ids:
            if signal_id not in signals:
                report.error(f"{question_id}: unknown source_signal_id {signal_id}")

    profile_path = DATA / "exam_style" / "mpje_style_profile.json"
    profile = load_json(profile_path)
    validate_schema_records([(profile_path, profile)], SCHEMAS / "exam_style_profile.schema.json", report)
    sources_by_url = {source.get("url"): source for source in sources.values()}
    for profile_source in profile.get("sources", []):
        source = sources_by_url.get(profile_source.get("url"))
        if source is None:
            report.error(f"{profile_path}: style source URL lacks a source manifest")
        elif source.get("source_class") != "PUBLIC_OFFICIAL" or source.get("permission_status") != "VERIFIED":
            report.error(f"{profile_path}: style source is not a verified PUBLIC_OFFICIAL source")
    blueprint = load_json(DATA / "blueprint.json")
    blueprint_path = DATA / "blueprint.json"
    validate_schema_records([(blueprint_path, blueprint)], SCHEMAS / "blueprint.schema.json", report)
    report.extend(validate_versioned_context(blueprint, profile))

    requirements_path = DATA / "release_requirements.json"
    requirements = load_json(requirements_path)
    validate_schema_records(
        [(requirements_path, requirements)],
        SCHEMAS / "release_requirements.schema.json",
        report,
    )
    for label in ("legal_verification", "realism_review"):
        requirement = requirements.get(label, {})
        minimum_passes = requirement.get("minimum_passes", 0)
        minimum_distinct = requirement.get("minimum_distinct_auditors", 0)
        required_types = requirement.get("required_auditor_types", [])
        basis = requirement.get("distinctness_basis", "AUDITOR_TYPE")
        if minimum_distinct > minimum_passes:
            report.error(f"{requirements_path}: {label} distinct-auditor minimum exceeds pass minimum")
        if basis == "AUDITOR_TYPE" and len(required_types) > minimum_distinct:
            report.error(f"{requirements_path}: {label} required auditor types exceed distinct-auditor minimum")

    matrix_path = DATA / "exam_style" / "question_family_matrix.json"
    matrix = load_json(matrix_path)
    validate_schema_records([(matrix_path, matrix)], SCHEMAS / "question_family_matrix.schema.json", report)
    if matrix.get("profile_id") != profile.get("profile_id"):
        report.error(f"{matrix_path}: profile_id does not match the current style profile")
    report.extend(validate_family_matrix(matrix, questions, rules, matrix_path))

    return report


def main() -> int:
    from validate_questions import validate_questions
    from validate_rules import validate_rules

    rule_report, rules = validate_rules()
    question_report, questions = validate_questions(rules)
    rule_report.extend(question_report)
    rule_report.extend(validate_governance(rules, questions))
    return print_report("governance", rule_report)


if __name__ == "__main__":
    raise SystemExit(main())
