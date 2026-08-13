from __future__ import annotations

from qa_common import (
    DATA,
    SCHEMAS,
    QAReport,
    find_placeholders,
    index_records,
    load_records,
    print_report,
    validate_schema_records,
)


def validate_rules() -> tuple[QAReport, dict[str, dict]]:
    report = QAReport()
    records = load_records(DATA / "rules")
    validate_schema_records(records, SCHEMAS / "rule.schema.json", report)
    rules = index_records(records, "rule_id", report)
    for path, rule in records:
        placeholders = find_placeholders(rule)
        if placeholders:
            report.error(f"{path}: literal placeholder(s): {sorted(set(placeholders))}")
        for authority in rule.get("authority", []):
            if not authority.get("url"):
                report.error(f"{path}: authority missing source URL")
            if not authority.get("section"):
                report.error(f"{path}: authority missing source section")
        if not rule.get("last_verified"):
            report.error(f"{path}: missing verification date")
        for related_id in rule.get("related_rule_ids", []):
            if related_id not in rules:
                report.error(f"{path}: unknown related_rule_id {related_id}")
        for superseded_id in rule.get("supersedes", []):
            if superseded_id not in rules:
                report.error(f"{path}: unknown supersedes rule_id {superseded_id}")
    return report, rules


def main() -> int:
    report, _ = validate_rules()
    return print_report("rules", report)


if __name__ == "__main__":
    raise SystemExit(main())

