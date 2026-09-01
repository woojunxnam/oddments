from __future__ import annotations

from typing import Any

from qa_common import DATA, dependency_snapshot, load_json, load_records
from validate_questions import validate_questions
from validate_rules import validate_rules
from validate_study_guide import validate_study_guide


def build_study_guide_payload(*, include_pending: bool = False) -> dict[str, Any]:
    rule_report, rules = validate_rules()
    question_report, questions = validate_questions(rules)
    guide_report, sections = validate_study_guide(rules, questions)
    if not rule_report.ok or not question_report.ok or not guide_report.ok:
        raise ValueError("Study Guide canonical validation failed")

    index = load_json(DATA / "study_guide" / "index.json")
    output = []
    for entry in index["sections"]:
        section = sections[entry["section_id"]]
        if section["verification_status"] != "VERIFIED" and not include_pending:
            continue
        authorities = []
        for rule_id in section["rule_ids"]:
            for authority in rules[rule_id]["authority"]:
                authorities.append(
                    {
                        "rule_id": rule_id,
                        "name": authority["name"],
                        "section": authority["section"],
                        "url": authority["url"],
                        "last_verified": rules[rule_id]["last_verified"],
                    }
                )
        output.append({**section, "navigation": entry, "authorities": authorities})

    question_to_sections: dict[str, list[str]] = {}
    for section in output:
        for question_id in section["practice_question_ids"]:
            question_to_sections.setdefault(question_id, []).append(section["section_id"])
    return {
        "meta": {
            "guide_id": index["guide_id"],
            "schema_version": index["schema_version"],
            "canonical_source": "data/study_guide/",
            "include_pending": include_pending,
            "public_verified_section_count": sum(
                section["verification_status"] == "VERIFIED" for section in sections.values()
            ),
            "pending_section_count": sum(
                section["verification_status"] == "AUDIT_PENDING" for section in sections.values()
            ),
            "section_count": len(output),
        },
        "sections": output,
        "question_to_sections": {key: value for key, value in sorted(question_to_sections.items())},
    }


def build_study_guide_coverage() -> dict[str, Any]:
    _, rules = validate_rules()
    _, questions = validate_questions(rules)
    _, sections = validate_study_guide(rules, questions)
    families = load_json(DATA / "exam_style" / "question_family_matrix.json")["families"]
    current_rules = {
        rule_id for rule_id, rule in rules.items() if rule.get("status") == "CURRENT"
    }
    any_rules = {rule_id for section in sections.values() for rule_id in section["rule_ids"]}
    verified_rules = {
        rule_id
        for section in sections.values()
        if section["verification_status"] == "VERIFIED"
        for rule_id in section["rule_ids"]
    }
    linked_questions = {
        question_id for section in sections.values() for question_id in section["practice_question_ids"]
    }
    released_families = {
        question["family_id"]
        for question in questions.values()
        if question.get("verification_status") == "RELEASED" and question.get("lifecycle_status") == "RELEASED"
    }
    linked_families = {questions[question_id]["family_id"] for question_id in linked_questions}
    family_topics = {(family["area"], family["topic"]) for family in families}
    guide_topics = {(area, section["topic"]) for section in sections.values() for area in section["areas"]}
    return {
        "guide_id": load_json(DATA / "study_guide" / "index.json")["guide_id"],
        "sections": {
            "total": len(sections),
            "by_status": {
                status: sum(section["verification_status"] == status for section in sections.values())
                for status in ("VERIFIED", "AUDIT_PENDING", "HOLD", "REVIEW_REQUIRED")
            },
        },
        "canonical_rules": {
            "current_total": len(current_rules),
            "covered_by_any_section": len(current_rules & any_rules),
            "covered_by_verified_public_section": len(current_rules & verified_rules),
            "uncovered_rule_ids": sorted(current_rules - any_rules),
        },
        "released_question_families": {
            "total": len(released_families),
            "covered_by_practice_links": len(released_families & linked_families),
            "uncovered_family_ids": sorted(released_families - linked_families),
        },
        "family_topic_proxies": {
            "total": len(family_topics),
            "covered": len(family_topics & guide_topics),
            "uncovered": [
                {"area": area, "topic": topic} for area, topic in sorted(family_topics - guide_topics)
            ],
        },
    }
