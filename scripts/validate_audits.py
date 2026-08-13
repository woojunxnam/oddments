from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from qa_common import DATA, SCHEMAS, QAReport, index_records, load_records, print_report, validate_schema_records


def _valid_official_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def validate_audits(
    known_question_ids: set[str] | None = None,
    data_root: Path | None = None,
) -> tuple[QAReport, dict[str, dict]]:
    report = QAReport()
    records = load_records((data_root or DATA) / "audits")
    validate_schema_records(records, SCHEMAS / "audit.schema.json", report)
    audits = index_records(records, "audit_id", report)

    for path, audit in records:
        question_ids = audit.get("question_ids", [])
        result_ids = [result.get("Question_ID") for result in audit.get("results", [])]
        hash_ids = set(audit.get("question_hashes", {}))
        if len(result_ids) != len(set(result_ids)):
            report.error(f"{path}: duplicate Question_ID in results")
        if set(question_ids) != set(result_ids):
            report.error(f"{path}: question_ids and results Question_ID sets must match exactly")
        if set(question_ids) != hash_ids:
            report.error(f"{path}: question_ids and question_hashes keys must match exactly")
        if known_question_ids is not None:
            for question_id in sorted(set(question_ids) - known_question_ids):
                report.error(f"{path}: unknown question ID {question_id}")

        if audit.get("audit_status") != "FULLY_ADJUDICATED":
            continue
        for result in audit.get("results", []):
            question_id = result.get("Question_ID", "<missing>")
            if audit.get("review_type") == "LEGAL_VERIFICATION":
                if result.get("Existing_Answer_Correct") == "NOT_ASSESSED":
                    report.error(f"{path}: {question_id} is fully adjudicated but answer was not assessed")
                authorities = result.get("authorities", [])
                if not authorities:
                    report.error(f"{path}: {question_id} is fully adjudicated but lacks authorities")
                for index, authority in enumerate(authorities):
                    label = f"{question_id} authority[{index}]"
                    for field in ("authority", "source_type", "exact_section", "law_checked_date"):
                        value = authority.get(field)
                        if value is None or not str(value).strip():
                            report.error(f"{path}: {label} lacks {field}")
                    if not _valid_official_url(authority.get("official_url")):
                        report.error(f"{path}: {label} has invalid official_url")
            elif audit.get("review_type") == "REALISM_REVIEW":
                criteria = result.get("Criteria", {})
                if result.get("Realism_Verdict") == "PASS" and not all(criteria.values()):
                    report.error(f"{path}: {question_id} realism PASS requires every criterion to pass")
    return report, audits


def main() -> int:
    report, _ = validate_audits()
    return print_report("audits", report)


if __name__ == "__main__":
    raise SystemExit(main())
