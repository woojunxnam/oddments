from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from qa_common import DATA, ROOT, load_json, load_records, print_report, question_audit_hash, write_json
from release_context import named_dependency_snapshot, style_profile_snapshot, validate_release_date
from validate_audits import validate_audits
from validate_drugs import validate_drugs
from validate_questions import validate_questions
from validate_rules import validate_rules


def derive_realism_reviews(question: dict, audits: dict[str, dict]) -> list[dict]:
    question_hash = question_audit_hash(question)
    reviews = []
    for audit_id in question.get("audits", []):
        audit = audits.get(audit_id)
        if not audit or audit.get("review_type") != "REALISM_REVIEW":
            continue
        if audit.get("question_hashes", {}).get(question["question_id"]) != question_hash:
            continue
        result = next(
            (item for item in audit.get("results", []) if item.get("Question_ID") == question["question_id"]),
            None,
        )
        if result and result.get("Verdict") == "KEEP" and result.get("Realism_Verdict") == "PASS":
            reviews.append(
                {
                    "audit_id": audit_id,
                    "auditor": audit.get("auditor"),
                    "reviewed_date": result.get("Reviewed_Date"),
                    "criteria": result.get("Criteria", {}),
                    "notes": result.get("Notes", ""),
                    "style_profile": audit.get("style_profile"),
                }
            )
    return reviews


def build_site_payload(include_fixtures: bool = False) -> dict:
    rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}
    drugs = {record["drug_id"]: record for _, record in load_records(DATA / "drugs")}
    _, audits = validate_audits()
    blueprint = load_json(DATA / "blueprint.json")
    style_profile = load_json(DATA / "exam_style" / "mpje_style_profile.json")
    questions = []
    for _, question in load_records(DATA / "questions"):
        released = question.get("verification_status") == "RELEASED" and question.get("lifecycle_status") == "RELEASED"
        if not released and not (include_fixtures and question.get("development_fixture")):
            continue
        authorities = []
        for rule_id in question.get("rule_ids", []):
            for authority in rules.get(rule_id, {}).get("authority", []):
                authorities.append(
                    {
                        "rule_id": rule_id,
                        "name": authority["name"],
                        "section": authority["section"],
                        "url": authority["url"],
                        "last_verified": rules[rule_id]["last_verified"],
                    }
                )
        drug_checks = [drugs[drug_id] for drug_id in question.get("drug_ids", []) if drug_id in drugs]
        realism_reviews = derive_realism_reviews(question, audits)
        questions.append(
            {
                **question,
                "authorities": authorities,
                "drug_checks": drug_checks,
                "realism_reviews": realism_reviews,
            }
        )
    return {
        "meta": {
            "canonical_source": "data/",
            "development_fixture_mode": include_fixtures,
            "release_status": (
                "DEVELOPMENT_ONLY"
                if include_fixtures
                else "RELEASE_AVAILABLE"
                if questions
                else "NO_RELEASED_QUESTIONS"
            ),
            "question_count": len(questions),
            "blueprint": named_dependency_snapshot(blueprint, "blueprint_id"),
            "style_profile": named_dependency_snapshot(style_profile, "profile_id"),
        },
        "blueprint": __import__("json").loads((DATA / "blueprint.json").read_text(encoding="utf-8")),
        "questions": questions,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-fixtures", action="store_true")
    parser.add_argument("--target-exam-date", type=date.fromisoformat)
    parser.add_argument("--output", type=Path, default=ROOT / "site" / "generated" / "questions.json")
    args = parser.parse_args()
    rule_report, rules = validate_rules()
    drug_report, drugs = validate_drugs(rules)
    question_report, _ = validate_questions(rules, drugs)
    rule_report.extend(drug_report)
    rule_report.extend(question_report)
    if not rule_report.ok:
        print_report("site-data release gate", rule_report)
        return 1
    if not args.include_fixtures:
        context_report = validate_release_date(
            load_json(DATA / "blueprint.json"),
            load_json(DATA / "exam_style" / "mpje_style_profile.json"),
            reference_date=date.today(),
            target_exam_date=args.target_exam_date,
        )
        if not context_report.ok:
            print_report("site-data release context", context_report)
            return 1
    payload = build_site_payload(args.include_fixtures)
    write_json(args.output, payload)
    print(f"built site data: {payload['meta']['question_count']} questions -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
