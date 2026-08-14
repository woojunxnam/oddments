from __future__ import annotations

from collections import Counter, defaultdict

from qa_common import (
    ABSOLUTE_WORDS,
    BLOCKED_RULE_STATUSES,
    DATA,
    HEDGE_WORDS,
    ROOT,
    SCHEMAS,
    VERIFIED_DRUG_STATUSES,
    VERIFIED_RULE_STATUSES,
    QAReport,
    dependency_snapshot,
    drug_consequence_rule_ids,
    find_placeholders,
    index_records,
    load_json,
    load_records,
    normalize_text,
    print_report,
    question_audit_hash,
    validate_schema_records,
)
from release_context import named_dependency_snapshot, style_profile_snapshot
from validate_audits import validate_audits
from validate_drugs import validate_drugs
from validate_rules import validate_rules


def validate_questions(
    rules: dict[str, dict] | None = None,
    drugs: dict[str, dict] | None = None,
    audits: dict[str, dict] | None = None,
    release_requirements: dict | None = None,
    blueprint: dict | None = None,
    style_profile: dict | None = None,
) -> tuple[QAReport, dict[str, dict]]:
    report = QAReport()
    if rules is None:
        rule_report, rules = validate_rules()
        report.extend(rule_report)
    if drugs is None:
        drug_report, drugs = validate_drugs(rules)
        report.extend(drug_report)
    records = load_records(DATA / "questions")
    validate_schema_records(records, SCHEMAS / "question.schema.json", report)
    questions = index_records(records, "question_id", report)
    if audits is None:
        audit_report, audits = validate_audits(set(questions), data_root=DATA)
        report.extend(audit_report)
    if release_requirements is None:
        release_requirements = load_json(ROOT / "data" / "release_requirements.json")
    if blueprint is None:
        blueprint = load_json(ROOT / "data" / "blueprint.json")
    if style_profile is None:
        style_profile = load_json(ROOT / "data" / "exam_style" / "mpje_style_profile.json")
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
        if not correct_ids:
            report.error(f"{path}: missing answer")
        unknown_correct = sorted(set(correct_ids) - set(choice_ids))
        if unknown_correct:
            report.error(f"{path}: correct choice not found in choices: {unknown_correct}")
        if question.get("question_type") == "SBA" and len(correct_ids) != 1:
            report.error(f"{path}: SBA must have exactly one answer")
        if question.get("question_type") == "SATA" and not correct_ids:
            report.error(f"{path}: SATA must have at least one answer")
        if question.get("question_type") == "ORDERED_RESPONSE":
            if len(correct_ids) != len(choice_ids) or set(correct_ids) != set(choice_ids):
                report.error(f"{path}: ORDERED_RESPONSE must use every choice exactly once in the correct order")

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
                if drug:
                    if drug.get("verification_status") not in VERIFIED_DRUG_STATUSES:
                        report.error(f"{path}: released question references HOLD/unverified drug {drug_id}")
                    for transitive_rule_id in sorted(drug_consequence_rule_ids(drug)):
                        transitive_rule = rules.get(transitive_rule_id)
                        if transitive_rule is None:
                            continue
                        if transitive_rule.get("status") != "CURRENT" or transitive_rule.get("status") in BLOCKED_RULE_STATUSES:
                            report.error(
                                f"{path}: released question drug {drug_id} depends on blocked rule "
                                f"{transitive_rule_id} ({transitive_rule.get('status')})"
                            )
                        if transitive_rule.get("verification_status") not in VERIFIED_RULE_STATUSES:
                            report.error(
                                f"{path}: released question drug {drug_id} depends on HOLD/unverified rule "
                                f"{transitive_rule_id}"
                            )
            if question.get("duplicate_review_status") != "CLEAR":
                report.error(f"{path}: released question has unresolved duplicate-family review")
            final_adjudication = question.get("final_adjudication")
            if release_requirements.get("final_adjudication_required") and final_adjudication is None:
                report.error(f"{path}: released question lacks final adjudication")
            elif final_adjudication is not None:
                required_decision = release_requirements.get("final_decision_required")
                if final_adjudication.get("decision") != required_decision:
                    report.error(
                        f"{path}: released question final adjudication must be {required_decision}"
                    )
                expected_dependencies = {
                    "rules": {rule_id: dependency_snapshot(rules[rule_id]) for rule_id in rule_ids if rule_id in rules},
                    "drugs": {
                        drug_id: dependency_snapshot(drugs[drug_id])
                        for drug_id in question.get("drug_ids", [])
                        if drug_id in drugs
                    },
                    "blueprint": named_dependency_snapshot(blueprint, "blueprint_id"),
                    "style_profile": named_dependency_snapshot(style_profile, "profile_id"),
                }
                if final_adjudication.get("verified_dependencies") != expected_dependencies:
                    report.error(f"{path}: adjudicated dependency versions/hashes do not match current canonical dependencies")
            if not question.get("last_legal_review"):
                report.error(f"{path}: released question lacks legal-review date")

            audit_ids = question.get("audits", [])
            if not audit_ids:
                report.error(f"{path}: released question must reference at least one canonical audit")
            resolved_audits = []
            for audit_id in audit_ids:
                audit = audits.get(audit_id)
                if audit is None:
                    report.error(f"{path}: referenced audit does not exist: {audit_id}")
                else:
                    resolved_audits.append(audit)
            current_question_hash = question_audit_hash(question)
            legal_passes: list[dict] = []
            realism_passes: list[dict] = []
            referenced_audit_ids = {audit.get("audit_id") for audit in resolved_audits}
            for audit in resolved_audits:
                if question.get("question_id") not in audit.get("question_ids", []):
                    report.error(f"{path}: audit {audit.get('audit_id')} does not cover {qid}")
                    continue
                if audit.get("question_hashes", {}).get(qid) != current_question_hash:
                    report.error(f"{path}: audit {audit.get('audit_id')} was not performed on current question content")
                    continue
                if not audit.get("independent") or audit.get("audit_status") != "FULLY_ADJUDICATED":
                    continue
                result = next(
                    (item for item in audit.get("results", []) if item.get("Question_ID") == qid),
                    None,
                )
                if result is None:
                    continue
                if audit.get("review_type") == "LEGAL_VERIFICATION":
                    if result.get("Verdict") == "KEEP" and result.get("Existing_Answer_Correct") == "YES":
                        legal_passes.append(audit)
                    else:
                        report.error(
                            f"{path}: current legal audit {audit.get('audit_id')} does not independently pass"
                        )
                elif audit.get("review_type") == "REALISM_REVIEW":
                    if audit.get("style_profile") != style_profile_snapshot(style_profile):
                        report.error(
                            f"{path}: realism audit {audit.get('audit_id')} uses a stale style profile"
                        )
                    elif result.get("Verdict") == "KEEP" and result.get("Realism_Verdict") == "PASS":
                        realism_passes.append(audit)
                    else:
                        report.error(
                            f"{path}: current realism audit {audit.get('audit_id')} does not pass"
                        )

            # A failed fully adjudicated audit on the current question content cannot be
            # hidden by removing its ID from the question's selected release evidence.
            for audit in audits.values():
                if audit.get("audit_id") in referenced_audit_ids:
                    continue
                if not audit.get("independent") or audit.get("audit_status") != "FULLY_ADJUDICATED":
                    continue
                if audit.get("question_hashes", {}).get(qid) != current_question_hash:
                    continue
                result = next(
                    (item for item in audit.get("results", []) if item.get("Question_ID") == qid),
                    None,
                )
                if result is None:
                    continue
                if audit.get("review_type") == "LEGAL_VERIFICATION":
                    if result.get("Verdict") != "KEEP" or result.get("Existing_Answer_Correct") != "YES":
                        report.error(
                            f"{path}: current legal audit {audit.get('audit_id')} does not independently pass"
                        )
                elif (
                    audit.get("review_type") == "REALISM_REVIEW"
                    and audit.get("style_profile") == style_profile_snapshot(style_profile)
                    and (result.get("Verdict") != "KEEP" or result.get("Realism_Verdict") != "PASS")
                ):
                    report.error(
                        f"{path}: current realism audit {audit.get('audit_id')} does not pass"
                    )

            for label, passes, requirement in (
                ("legal", legal_passes, release_requirements.get("legal_verification", {})),
                ("realism", realism_passes, release_requirements.get("realism_review", {})),
            ):
                if len(passes) < requirement.get("minimum_passes", 1):
                    report.error(f"{path}: insufficient current independent {label} audit passes")
                auditors = {audit.get("auditor") for audit in passes}
                if len(auditors) < requirement.get("minimum_distinct_auditors", 1):
                    report.error(f"{path}: insufficient distinct {label} auditors")
                missing_auditors = set(requirement.get("required_auditor_types", [])) - auditors
                if missing_auditors:
                    report.error(
                        f"{path}: missing required {label} auditor types {sorted(missing_auditors)}"
                    )

            if release_requirements.get("initial_batch_history_required"):
                initial_history = any(
                    audit.get("audit_scope") == "INITIAL_BATCH"
                    and audit.get("review_type") == "LEGAL_VERIFICATION"
                    and audit.get("independent")
                    and audit.get("audit_status") == "FULLY_ADJUDICATED"
                    and qid in audit.get("question_ids", [])
                    and any(result.get("Question_ID") == qid for result in audit.get("results", []))
                    for audit in audits.values()
                )
                if not initial_history:
                    report.error(f"{path}: released question lacks valid INITIAL_BATCH audit history")
            if question.get("independent_audit_status") != "PASSED":
                report.error(f"{path}: released question status summary must be PASSED after stored audit gates pass")

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
