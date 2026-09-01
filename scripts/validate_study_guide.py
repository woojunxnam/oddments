from __future__ import annotations

from pathlib import Path
from typing import Any

from qa_common import (
    BLOCKED_RULE_STATUSES,
    DATA,
    SCHEMAS,
    VERIFIED_RULE_STATUSES,
    QAReport,
    dependency_snapshot,
    find_placeholders,
    index_records,
    load_json,
    load_records,
    print_report,
    validate_schema_records,
)
from study_guide_common import legal_point_rule_ids, study_guide_content_hash
from validate_questions import validate_questions
from validate_rules import validate_rules


def validate_study_guide(
    rules: dict[str, dict[str, Any]] | None = None,
    questions: dict[str, dict[str, Any]] | None = None,
    *,
    data_root: Path = DATA,
) -> tuple[QAReport, dict[str, dict[str, Any]]]:
    report = QAReport()
    if rules is None:
        rule_report, rules = validate_rules()
        report.extend(rule_report)
    if questions is None:
        if data_root != DATA:
            raise ValueError("questions must be supplied when validating a non-canonical study-guide root")
        question_report, questions = validate_questions(rules)
        report.extend(question_report)

    section_root = data_root / "study_guide" / "sections"
    records = load_records(section_root)
    validate_schema_records(records, SCHEMAS / "study_guide_section.schema.json", report)
    sections = index_records(records, "section_id", report)

    index_path = data_root / "study_guide" / "index.json"
    if not index_path.exists():
        report.error(f"{index_path}: missing study-guide index")
        return report, sections
    index = load_json(index_path)
    entries = index.get("sections", [])
    indexed_ids = [entry.get("section_id") for entry in entries]
    if len(indexed_ids) != len(set(indexed_ids)):
        report.error(f"{index_path}: duplicate section_id")
    if set(indexed_ids) != set(sections):
        report.error(f"{index_path}: section registry does not exactly match section files")
    orders = [entry.get("order") for entry in entries]
    if orders != list(range(1, len(entries) + 1)):
        report.error(f"{index_path}: section order must be contiguous starting at 1")

    for path, section in records:
        placeholders = find_placeholders(section)
        if placeholders:
            report.error(f"{path}: literal placeholder(s): {sorted(set(placeholders))}")
        if section.get("content_hash") != study_guide_content_hash(section):
            report.error(f"{path}: content_hash mismatch; run scripts/update_study_guide_hashes.py")

        rule_ids = set(section.get("rule_ids", []))
        dependencies = section.get("verified_rule_dependencies", {})
        if set(dependencies) != rule_ids:
            report.error(f"{path}: verified_rule_dependencies must exactly match rule_ids")
        grounded = legal_point_rule_ids(section)
        if grounded != rule_ids:
            missing = sorted(rule_ids - grounded)
            extra = sorted(grounded - rule_ids)
            report.error(f"{path}: grounded legal-point rules differ; missing={missing} extra={extra}")

        for rule_id in rule_ids:
            rule = rules.get(rule_id)
            if not rule:
                report.error(f"{path}: unknown rule_id {rule_id}")
                continue
            if rule.get("status") in BLOCKED_RULE_STATUSES or rule.get("status") != "CURRENT":
                report.error(f"{path}: rule {rule_id} is not current")
            if rule.get("verification_status") not in VERIFIED_RULE_STATUSES:
                report.error(f"{path}: rule {rule_id} is not primary/official-policy verified")
            if not rule.get("authority") or any(not authority.get("url") for authority in rule["authority"]):
                report.error(f"{path}: rule {rule_id} lacks official authority metadata")
            if dependencies.get(rule_id) != dependency_snapshot(rule):
                report.error(f"{path}: stale dependency snapshot for {rule_id}")

        for question_id in section.get("practice_question_ids", []):
            question = questions.get(question_id)
            if not question:
                report.error(f"{path}: unknown practice_question_id {question_id}")
            elif not (
                question.get("verification_status") == "RELEASED"
                and question.get("lifecycle_status") == "RELEASED"
            ):
                report.error(f"{path}: practice question {question_id} is not RELEASE-usable")

        if section.get("verification_status") == "VERIFIED" and not section.get("independent_audit_id"):
            report.error(f"{path}: VERIFIED guide prose requires independent_audit_id")

    return report, sections


if __name__ == "__main__":
    result, _ = validate_study_guide()
    raise SystemExit(print_report("study guide", result))
