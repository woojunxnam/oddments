from __future__ import annotations

from qa_common import DATA, QAReport, find_placeholders, load_records, print_report


def check_placeholders() -> QAReport:
    report = QAReport()
    for registry in ("rules", "drugs", "questions"):
        for path, record in load_records(DATA / registry):
            matches = sorted(set(find_placeholders(record)))
            if matches:
                report.error(f"{path}: literal placeholder(s): {matches}")
    return report


def main() -> int:
    return print_report("placeholders", check_placeholders())


if __name__ == "__main__":
    raise SystemExit(main())
