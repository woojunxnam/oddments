from __future__ import annotations

from qa_common import (
    BLOCKED_RULE_STATUSES,
    DATA,
    SCHEMAS,
    VERIFIED_DRUG_STATUSES,
    VERIFIED_RULE_STATUSES,
    QAReport,
    dependency_snapshot,
    drug_consequence_rule_ids,
    find_placeholders,
    index_records,
    load_records,
    print_report,
    semantic_content_hash,
    validate_schema_records,
)
from validate_rules import validate_rules


def validate_drugs(rules: dict[str, dict] | None = None) -> tuple[QAReport, dict[str, dict]]:
    report = QAReport()
    if rules is None:
        rule_report, rules = validate_rules()
        report.extend(rule_report)
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
        expected_hash = semantic_content_hash(drug, "drug")
        if drug.get("content_hash") != expected_hash:
            report.error(f"{path}: content_hash mismatch; run scripts/update_content_hashes.py")
        for authority in drug.get("authorities", []):
            if not authority.get("url"):
                report.error(f"{path}: authority missing source URL")
            if not authority.get("section"):
                report.error(f"{path}: authority missing source section")
        consequence_rule_ids = drug_consequence_rule_ids(drug)
        recorded_dependencies = drug.get("verified_rule_dependencies", {})
        if set(recorded_dependencies) != consequence_rule_ids:
            report.error(f"{path}: verified_rule_dependencies must exactly match legal-consequence rule_ids")
        for rule_id in sorted(consequence_rule_ids):
            rule = rules.get(rule_id)
            if rule is None:
                report.error(f"{path}: legal consequence references unknown rule_id {rule_id}")
                continue
            if recorded_dependencies.get(rule_id) != dependency_snapshot(rule):
                report.error(f"{path}: stale verified rule dependency {rule_id}")
            if drug.get("verification_status") in VERIFIED_DRUG_STATUSES:
                if rule.get("status") in BLOCKED_RULE_STATUSES or rule.get("status") != "CURRENT":
                    report.error(f"{path}: verified drug depends on blocked rule {rule_id} ({rule.get('status')})")
                if rule.get("verification_status") not in VERIFIED_RULE_STATUSES:
                    report.error(f"{path}: verified drug depends on HOLD/unverified rule {rule_id}")
    return report, drugs


def main() -> int:
    report, _ = validate_drugs()
    return print_report("drugs", report)


if __name__ == "__main__":
    raise SystemExit(main())
