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


def validate_drugs() -> tuple[QAReport, dict[str, dict]]:
    report = QAReport()
    records = load_records(DATA / "drugs")
    validate_schema_records(records, SCHEMAS / "drug.schema.json", report)
    drugs = index_records(records, "drug_id", report)
    for path, drug in records:
        placeholders = find_placeholders(drug)
        if placeholders:
            report.error(f"{path}: literal placeholder(s): {sorted(set(placeholders))}")
        if not drug.get("main_indications"):
            report.error(f"{path}: drug record missing concise indication")
        if not drug.get("last_verified"):
            report.error(f"{path}: missing verification date")
        for authority in drug.get("authorities", []):
            if not authority.get("url"):
                report.error(f"{path}: authority missing source URL")
            if not authority.get("section"):
                report.error(f"{path}: authority missing source section")
    return report, drugs


def main() -> int:
    report, _ = validate_drugs()
    return print_report("drugs", report)


if __name__ == "__main__":
    raise SystemExit(main())

