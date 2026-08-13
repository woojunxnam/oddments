from __future__ import annotations

from collections import Counter, defaultdict

from qa_common import (
    ABSOLUTE_WORDS,
    BLOCKED_RULE_STATUSES,
    DATA,
    HEDGE_WORDS,
    SCHEMAS,
    VERIFIED_DRUG_STATUSES,
    VERIFIED_RULE_STATUSES,
    QAReport,
    find_placeholders,
    index_records,
    load_records,
    normalize_text,
    print_report,
    validate_schema_records,
)
from validate_drugs import validate_drugs
from validate_rules import validate_rules


def validate_questions(
    rules: dict[str, dict] | None = None,
    drugs: dict[str, dict] | None = None,
) -> tuple[QAReport, dict[str, dict]]:
    report = QAReport()
    if rules is None:
        rule_report, rules = validate_rules()
        report.extend(rule_report)
    if drugs is None:
        drug_report, drugs = validate_drugs()
        report.extend(drug_report)
    records = load_records(DATA / "questions")
    validate_schema_records(records, SCHEMAS / "question.schema.json", report)
    questions = index_records(records, "question_id", report)
    core_explanations: dict[str, list[str]] = defaultdict(list)
    family_counts: Counter[str] = Counter()
    topic_counts: Counter[str] = Counter()
    drug_counts: Counter[str] = Counter()

    for path, question in records:
        qid = question.get("question_id", str(path))
        placeholders = find_placeholders(question)
        if placeholders:
            report.error(f"{path}: literal placeholder(s): {sorted(set(placeholders))}")
        choices = question.get("choices", [])
        choice_ids = [choice.get("id") for choice in choices]
        if len(choice_ids) != len(set(choice_ids)):
            report.error(f"{path}: duplicate choice ID")
        correct_ids = question.get("correct_choice_ids", [])
        if not correct_ids and not question.get("allow_zero_correct", False):
            report.error(f"{path}: missing answer")
        unknown_correct = sorted(set(correct_ids) - set(choice_ids))
        if unknown_correct:
            report.error(f"{path}: correct choice not found in choices: {unknown_correct}")
        if question.get("question_type") == "SBA" and len(correct_ids) != 1:
            report.error(f"{path}: SBA must have exactly one answer")
        if question.get("question_type") == "SATA" and not correct_ids and not question.get("allow_zero_correct", False):
            report.error(f"{path}: SATA has zero answers without explicit allowance")

        choice_analysis = question.get("explanation", {}).get("choice_analysis", {})
        missing_analysis = sorted(set(choice_ids) - set(choice_analysis))
        extra_analysis = sorted(set(choice_analysis) - set(choice_ids))
        if missing_analysis:
            report.error(f"{path}: choice-analysis missing for {missing_analysis}")
        if extra_analysis:
            report.error(f"{path}: choice-analysis references unknown choices {extra_analysis}")
        normalized_analysis = [normalize_text(value) for value in choice_analysis.values() if value]
        if len(normalized_analysis) != len(set(normalized_analysis)):
            report.error(f"{path}: identical choice-analysis text for multiple options")

        rule_ids = question.get("rule_ids", [])
        if not rule_ids:
            report.error(f"{path}: missing rule_id")
        for rule_id in rule_ids:
            if rule_id not in rules:
                report.error(f"{path}: unknown rule_id {rule_id}")
        for drug_id in question.get("drug_ids", []):
            if drug_id not in drugs:
                report.error(f"{path}: unknown drug_id {drug_id}")

        is_released = question.get("verification_status") == "RELEASED" or question.get("lifecycle_status") == "RELEASED"
        if is_released:
            if question.get("verification_status") != "RELEASED" or question.get("lifecycle_status") != "RELEASED":
                report.error(f"{path}: release status fields disagree")
            for rule_id in rule_ids:
                rule = rules.get(rule_id)
                if not rule:
                    continue
                if rule.get("status") != "CURRENT" or rule.get("status") in BLOCKED_RULE_STATUSES:
                    report.error(f"{path}: released question references blocked rule {rule_id} ({rule.get('status')})")
                if rule.get("verification_status") not in VERIFIED_RULE_STATUSES:
                    report.error(f"{path}: released question references HOLD/unverified rule {rule_id}")
            for drug_id in question.get("drug_ids", []):
                drug = drugs.get(drug_id)
                if drug and drug.get("verification_status") not in VERIFIED_DRUG_STATUSES:
                    report.error(f"{path}: released question references HOLD/unverified drug {drug_id}")
            if question.get("duplicate_review_status") != "CLEAR":
                report.error(f"{path}: released question has unresolved duplicate-family review")
            if question.get("independent_audit_status") != "PASSED":
                report.error(f"{path}: released question lacks passed independent audit")
            if question.get("final_adjudication") is None:
                report.error(f"{path}: released question lacks final adjudication")
            if not question.get("last_legal_review"):
                report.error(f"{path}: released question lacks legal-review date")

        if question.get("difficulty") == 5 and len(question.get("reasoning_steps", [])) < 3:
            report.error(f"{path}: difficulty 5 requires at least three reasoning steps")
        core = normalize_text(question.get("explanation", {}).get("core_reasoning", ""), normalize_numbers=True)
        if core:
            core_explanations[core].append(qid)
        family_counts[question.get("family_id", "<missing>")] += 1
        topic_counts[question.get("topic", "<missing>")] += 1
        drug_counts.update(question.get("drug_ids", []))

        choice_lengths = {choice["id"]: len(choice["text"].split()) for choice in choices if "id" in choice and "text" in choice}
        if question.get("question_type") == "SBA" and len(correct_ids) == 1 and choice_lengths:
            correct_length = choice_lengths.get(correct_ids[0], 0)
            distractor_lengths = [length for choice_id, length in choice_lengths.items() if choice_id != correct_ids[0]]
            if distractor_lengths and correct_length >= max(distractor_lengths) * 1.5 and correct_length - max(distractor_lengths) >= 4:
                report.warn(f"{qid}: correct option is materially longer than distractors")
            texts = {choice["id"]: choice["text"] for choice in choices}
            correct_hedged = bool(HEDGE_WORDS.search(texts.get(correct_ids[0], "")))
            distractor_hedges = [bool(HEDGE_WORDS.search(text)) for choice_id, text in texts.items() if choice_id != correct_ids[0]]
            if correct_hedged and distractor_hedges and not any(distractor_hedges):
                report.warn(f"{qid}: correct answer is the only hedged option")
        absolute_count = sum(bool(ABSOLUTE_WORDS.search(choice.get("text", ""))) for choice in choices)
        if absolute_count >= max(2, len(choices) - 1):
            report.warn(f"{qid}: excessive absolute-language distractors")

    for normalized, ids in core_explanations.items():
        if len(ids) > 1:
            report.warn(f"repeated explanation block in {', '.join(sorted(ids))}")
    for family, count in family_counts.items():
        if count > 4:
            report.warn(f"family {family} appears {count} times")
    if questions:
        topic_limit = max(4, round(len(questions) * 0.35))
        for topic, count in topic_counts.items():
            if count > topic_limit:
                report.warn(f"topic concentration: {topic} appears {count}/{len(questions)} times")
        drug_limit = max(3, round(len(questions) * 0.25))
        for drug_id, count in drug_counts.items():
            if count > drug_limit:
                report.warn(f"drug concentration: {drug_id} appears {count}/{len(questions)} times")
    return report, questions


def main() -> int:
    report, _ = validate_questions()
    return print_report("questions", report)


if __name__ == "__main__":
    raise SystemExit(main())

