from __future__ import annotations

import json

from check_answer_distribution import analyze_answer_distribution
from check_placeholders import check_placeholders
from detect_duplicates import detect_duplicates
from qa_common import DATA, ROOT, QAReport, print_report, write_json
from validate_drugs import validate_drugs
from validate_questions import validate_questions
from validate_rules import validate_rules


def validate_blueprint() -> QAReport:
    report = QAReport()
    path = DATA / "blueprint.json"
    blueprint = json.loads(path.read_text(encoding="utf-8"))
    weights = [area.get("weight_percent") for area in blueprint.get("areas", [])]
    if len(weights) != 4 or sum(weights) != 100:
        report.error(f"{path}: blueprint must contain four areas totaling 100%")
    if blueprint.get("target_question_count_per_mock") != 120:
        report.error(f"{path}: target question count must be 120 for the current target")
    if not blueprint.get("review_date"):
        report.error(f"{path}: missing review date")
    for source in blueprint.get("sources", []):
        if not source.get("url"):
            report.error(f"{path}: source missing URL")
    if not blueprint.get("release_guard", {}).get("must_reverify_after"):
        report.error(f"{path}: missing blueprint reverification guard")
    return report


def main() -> int:
    combined = QAReport()
    rule_report, rules = validate_rules()
    combined.extend(rule_report)
    drug_report, drugs = validate_drugs()
    combined.extend(drug_report)
    question_report, _ = validate_questions(rules, drugs)
    combined.extend(question_report)
    combined.extend(check_placeholders())
    combined.extend(validate_blueprint())

    duplicate_report = detect_duplicates()
    write_json(ROOT / "duplicate_report.json", duplicate_report)
    if duplicate_report["finding_count"]:
        combined.error(f"duplicate detector found {duplicate_report['finding_count']} pair(s); manual review required")

    distribution_report, distribution_failed = analyze_answer_distribution()
    write_json(ROOT / "answer_distribution_report.json", distribution_report)
    if distribution_report["severity"] == "WARNING":
        combined.warn("answer-position distribution exceeded warning threshold")
    elif distribution_failed:
        combined.error("answer-position distribution exceeded error threshold")

    return print_report("all", combined)


if __name__ == "__main__":
    raise SystemExit(main())
