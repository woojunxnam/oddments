from __future__ import annotations

from collections import Counter
from datetime import date

from qa_common import (
    BLOCKED_RULE_STATUSES,
    DATA,
    ROOT,
    VERIFIED_DRUG_STATUSES,
    VERIFIED_RULE_STATUSES,
    dependency_snapshot,
    drug_consequence_rule_ids,
    load_json,
    load_records,
    question_audit_hash,
    write_json,
)
from release_context import named_dependency_snapshot, style_profile_snapshot

TODAY = date(2026, 8, 17).isoformat()
SOURCE_CANDIDATE_SHA = "f85b650c1b3344184186229ec45bf1d233a4e971"
BATCH_IDS = [f"MA-Q-{number:04d}" for number in range(131, 211)]
IMPACT9 = {
    "MA-Q-0147",
    "MA-Q-0164",
    "MA-Q-0165",
    "MA-Q-0172",
    "MA-Q-0173",
    "MA-Q-0175",
    "MA-Q-0193",
    "MA-Q-0194",
    "MA-Q-0195",
}
B_FRESH_PASS5 = {
    "MA-Q-0145",
    "MA-Q-0146",
    "MA-Q-0166",
    "MA-Q-0171",
    "MA-Q-0196",
}

A_LEGAL_W1 = "AUDIT-GPT-FRESH-EXP2-A-LEGAL-INITIAL-W1-2026-08-15"
A_LEGAL_W2 = "AUDIT-GPT-FRESH-EXP2-A-LEGAL-INITIAL-W2-2026-08-15"
A_REALISM_W1 = "AUDIT-GPT-FRESH-EXP2-A-REALISM-INITIAL-W1-2026-08-15"
A_REALISM_W2 = "AUDIT-GPT-FRESH-EXP2-A-REALISM-INITIAL-W2-2026-08-15"
B_LEGAL = "AUDIT-GPT-FRESH-EXP2-B-LEGAL-REAUDIT-IMPACT14-2026-08-17"
B_REALISM_RAW_PATH = ROOT / "audits" / "reaudit" / "2026-08-17" / "GPT-FRESH-EXP2-B-REALISM-REAUDIT-IMPACT14.json"
C_LEGAL = "AUDIT-GPT-FRESH-EXP2-C-LEGAL-REAUDIT-R2-IMPACT9"
C_REALISM = "AUDIT-GPT-FRESH-EXP2-C-REALISM-REAUDIT-R2-IMPACT9"


def result_index(audit: dict) -> dict[str, dict]:
    return {item["Question_ID"]: item for item in audit.get("results", [])}


def wave_ids(qid: str) -> tuple[str, str]:
    number = int(qid[-4:])
    if number <= 170:
        return A_LEGAL_W1, A_REALISM_W1
    return A_LEGAL_W2, A_REALISM_W2


def dependency_blockers(question: dict, rules: dict[str, dict], drugs: dict[str, dict]) -> list[str]:
    blockers: list[str] = []
    for rule_id in question.get("rule_ids", []):
        rule = rules.get(rule_id)
        if rule is None:
            blockers.append(f"UNKNOWN_RULE:{rule_id}")
            continue
        if rule.get("status") != "CURRENT" or rule.get("status") in BLOCKED_RULE_STATUSES:
            blockers.append(f"RULE_NOT_CURRENT:{rule_id}:{rule.get('status')}")
        if rule.get("verification_status") not in VERIFIED_RULE_STATUSES:
            blockers.append(f"RULE_NOT_VERIFIED:{rule_id}:{rule.get('verification_status')}")
    for drug_id in question.get("drug_ids", []):
        drug = drugs.get(drug_id)
        if drug is None:
            blockers.append(f"UNKNOWN_DRUG:{drug_id}")
            continue
        if drug.get("verification_status") not in VERIFIED_DRUG_STATUSES:
            blockers.append(f"DRUG_NOT_VERIFIED:{drug_id}:{drug.get('verification_status')}")
        for rule_id in sorted(drug_consequence_rule_ids(drug)):
            rule = rules.get(rule_id)
            if rule is None:
                blockers.append(f"UNKNOWN_TRANSITIVE_RULE:{drug_id}:{rule_id}")
                continue
            if rule.get("status") != "CURRENT" or rule.get("status") in BLOCKED_RULE_STATUSES:
                blockers.append(f"TRANSITIVE_RULE_NOT_CURRENT:{drug_id}:{rule_id}:{rule.get('status')}")
            if rule.get("verification_status") not in VERIFIED_RULE_STATUSES:
                blockers.append(
                    f"TRANSITIVE_RULE_NOT_VERIFIED:{drug_id}:{rule_id}:{rule.get('verification_status')}"
                )
    return blockers


def verify_current_audit(
    qid: str,
    question: dict,
    audit: dict,
    *,
    review_type: str,
    style_profile: dict,
) -> list[str]:
    blockers: list[str] = []
    if audit.get("audit_status") != "FULLY_ADJUDICATED" or not audit.get("independent"):
        blockers.append(f"AUDIT_NOT_FULLY_INDEPENDENT:{audit.get('audit_id')}")
        return blockers
    if audit.get("review_type") != review_type:
        blockers.append(f"AUDIT_TYPE_MISMATCH:{audit.get('audit_id')}")
        return blockers
    if qid not in audit.get("question_ids", []):
        blockers.append(f"AUDIT_SCOPE_MISSING:{audit.get('audit_id')}")
        return blockers
    actual_hash = question_audit_hash(question)
    if audit.get("question_hashes", {}).get(qid) != actual_hash:
        blockers.append(f"STALE_AUDIT_HASH:{audit.get('audit_id')}")
        return blockers
    result = result_index(audit).get(qid)
    if result is None:
        blockers.append(f"AUDIT_RESULT_MISSING:{audit.get('audit_id')}")
        return blockers
    if review_type == "LEGAL_VERIFICATION":
        if result.get("Verdict") != "KEEP" or result.get("Existing_Answer_Correct") != "YES":
            blockers.append(f"LEGAL_NOT_PASS:{audit.get('audit_id')}")
    else:
        if audit.get("style_profile") != style_profile_snapshot(style_profile):
            blockers.append(f"STALE_STYLE_PROFILE:{audit.get('audit_id')}")
        if result.get("Verdict") != "KEEP" or result.get("Realism_Verdict") != "PASS":
            blockers.append(f"REALISM_NOT_PASS:{audit.get('audit_id')}")
    return blockers


def main() -> int:
    if len(BATCH_IDS) != 80 or len(IMPACT9) != 9 or len(B_FRESH_PASS5) != 5:
        raise RuntimeError("unexpected Batch 2 governance scope")

    audit_records = {record["audit_id"]: record for _, record in load_records(DATA / "audits")}
    required_canonical_audits = {
        A_LEGAL_W1,
        A_LEGAL_W2,
        A_REALISM_W1,
        A_REALISM_W2,
        B_LEGAL,
        C_LEGAL,
        C_REALISM,
    }
    missing = sorted(required_canonical_audits - set(audit_records))
    if missing:
        raise RuntimeError(f"missing canonical audits required for governance: {missing}")

    b_realism_raw = load_json(B_REALISM_RAW_PATH)
    if b_realism_raw.get("audit_id") != "AUDIT-GPT-FRESH-EXP2-B-REALISM-REAUDIT-IMPACT14-2026-08-17":
        raise RuntimeError("unexpected Issue #39 raw realism audit")
    if b_realism_raw.get("audit_status") != "FULLY_ADJUDICATED" or not b_realism_raw.get("independent"):
        raise RuntimeError("Issue #39 raw realism audit is not fully adjudicated independent evidence")

    rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}
    drugs = {record["drug_id"]: record for _, record in load_records(DATA / "drugs")}
    blueprint = load_json(DATA / "blueprint.json")
    style_profile = load_json(DATA / "exam_style" / "mpje_style_profile.json")
    matrix_path = DATA / "exam_style" / "question_family_matrix.json"
    matrix = load_json(matrix_path)
    matrix_families = {family["family_id"]: family for family in matrix.get("families", [])}

    # Release counts already in the bank before this Batch 2 governance pass.
    released_family_counts: Counter[str] = Counter()
    for _, question in load_records(DATA / "questions"):
        if question.get("verification_status") == "RELEASED" and question.get("lifecycle_status") == "RELEASED":
            released_family_counts[question["family_id"]] += 1

    released_ids: list[str] = []
    blocked: dict[str, list[str]] = {}
    selected_evidence: dict[str, dict[str, str]] = {}

    b_raw_results = result_index(b_realism_raw)
    for qid in BATCH_IDS:
        path = DATA / "questions" / f"ma-q-{qid[-4:]}.json"
        question = load_json(path)
        if question.get("question_id") != qid:
            blocked[qid] = ["QUESTION_ID_MISMATCH"]
            continue

        a_legal_id, a_realism_id = wave_ids(qid)
        if qid in IMPACT9:
            legal_id, realism_id = C_LEGAL, C_REALISM
        elif qid in B_FRESH_PASS5:
            legal_id, realism_id = B_LEGAL, a_realism_id
        else:
            legal_id, realism_id = a_legal_id, a_realism_id

        blockers: list[str] = []
        blockers.extend(
            verify_current_audit(
                qid,
                question,
                audit_records[legal_id],
                review_type="LEGAL_VERIFICATION",
                style_profile=style_profile,
            )
        )
        blockers.extend(
            verify_current_audit(
                qid,
                question,
                audit_records[realism_id],
                review_type="REALISM_REVIEW",
                style_profile=style_profile,
            )
        )

        # For the five Issue #39 PASS questions outside Round-2 Impact9, require the fresh
        # raw realism evidence as an additional support gate without canonicalizing the
        # mixed #39 artifact (which also contains pre-R2 failures that are context-stale).
        if qid in B_FRESH_PASS5:
            actual_hash = question_audit_hash(question)
            if b_realism_raw.get("question_hashes", {}).get(qid) != actual_hash:
                blockers.append("ISSUE39_RAW_REALISM_STALE_HASH")
            result = b_raw_results.get(qid, {})
            if result.get("Verdict") != "KEEP" or result.get("Realism_Verdict") != "PASS":
                blockers.append("ISSUE39_RAW_REALISM_NOT_PASS")

        blockers.extend(dependency_blockers(question, rules, drugs))

        family = matrix_families.get(question.get("family_id"))
        if family is None:
            blockers.append(f"UNKNOWN_FAMILY:{question.get('family_id')}")
        else:
            maximum = family.get("max_questions_in_final_bank", 0)
            if released_family_counts[question["family_id"]] >= maximum:
                blockers.append(f"FAMILY_CAP:{question['family_id']}:{maximum}")

        if blockers:
            blocked[qid] = sorted(set(blockers))
            continue

        question["audits"] = [legal_id, realism_id]
        question["verification_status"] = "RELEASED"
        question["lifecycle_status"] = "RELEASED"
        question["last_legal_review"] = audit_records[legal_id].get("audit_date", TODAY)
        question["duplicate_review_status"] = "CLEAR"
        question["independent_audit_status"] = "PASSED"
        question["final_adjudication"] = {
            "decision": "KEEP",
            "adjudicator": "GPT-5.6-Sol release-governance editor after independent Batch 2 audits",
            "date": TODAY,
            "notes": (
                "Batch 2 Round-2 release governance. Current-hash legal and realism evidence was selected "
                "question-by-question. The Issue #39 mixed realism artifact is retained as historical raw "
                "evidence; Round-2 Impact9 uses the fresh Issue #44 GPT-FRESH-EXP2-C audit."
            ),
            "verified_dependencies": {
                "rules": {
                    rule_id: dependency_snapshot(rules[rule_id])
                    for rule_id in question.get("rule_ids", [])
                    if rule_id in rules
                },
                "drugs": {
                    drug_id: dependency_snapshot(drugs[drug_id])
                    for drug_id in question.get("drug_ids", [])
                    if drug_id in drugs
                },
                "blueprint": named_dependency_snapshot(blueprint, "blueprint_id"),
                "style_profile": named_dependency_snapshot(style_profile, "profile_id"),
            },
        }
        write_json(path, question)
        released_ids.append(qid)
        released_family_counts[question["family_id"]] += 1
        selected_evidence[qid] = {"legal": legal_id, "realism": realism_id}

    # Synchronize family release counts with the actual post-governance bank state.
    final_family_counts: Counter[str] = Counter()
    for _, question in load_records(DATA / "questions"):
        if question.get("verification_status") == "RELEASED" and question.get("lifecycle_status") == "RELEASED":
            final_family_counts[question["family_id"]] += 1
    for family in matrix.get("families", []):
        family["current_released_count"] = final_family_counts.get(family["family_id"], 0)
    matrix["last_reviewed"] = TODAY
    write_json(matrix_path, matrix)

    # Public preview admission is release-derived only: append questions actually promoted.
    allowlist_path = ROOT / "site" / "generated" / "preview_allowlist.json"
    allowlist = load_json(allowlist_path)
    preview_ids = list(allowlist.get("question_ids", []))
    for qid in released_ids:
        if qid not in preview_ids:
            preview_ids.append(qid)
    used_audits = sorted({audit_id for pair in selected_evidence.values() for audit_id in pair.values()})
    allowlist["generated_date"] = TODAY
    allowlist["source_audits"] = list(
        dict.fromkeys(list(allowlist.get("source_audits", [])) + used_audits)
    )
    allowlist["notice"] = (
        "Preview contains prior released questions plus only Batch 2 questions promoted to RELEASED by "
        "Round-2 release governance after current-hash legal/realism evidence and dependency checks."
    )
    allowlist["question_ids"] = preview_ids
    write_json(allowlist_path, allowlist)

    released_batch2_area = Counter()
    total_released_area = Counter()
    for _, question in load_records(DATA / "questions"):
        is_released = question.get("verification_status") == "RELEASED" and question.get("lifecycle_status") == "RELEASED"
        if not is_released:
            continue
        total_released_area[question["area"]] += 1
        if question.get("question_id") in released_ids:
            released_batch2_area[question["area"]] += 1

    report = {
        "batch": "EXP2",
        "governance_round": "REALISM_R2",
        "date": TODAY,
        "source_candidate_sha": SOURCE_CANDIDATE_SHA,
        "batch_question_ids": BATCH_IDS,
        "released_ids": released_ids,
        "released_count": len(released_ids),
        "unreleased_ids": sorted(blocked),
        "unreleased_count": len(blocked),
        "blocking_reasons": blocked,
        "selected_current_evidence": selected_evidence,
        "supporting_history": {
            "initial_auditor_instance": "GPT-FRESH-EXP2-A",
            "issue39_auditor_instance": "GPT-FRESH-EXP2-B",
            "issue44_auditor_instance": "GPT-FRESH-EXP2-C",
            "issue39_realism_handling": (
                "Retained as raw historical/fresh supporting evidence, but not canonicalized into data/audits "
                "because it contains pre-R2 realism failures whose semantic-distinctness context was changed "
                "by the Round-2 repairs. Its five unaffected PASS results are required as an additional support "
                "gate for Q0145/Q0146/Q0166/Q0171/Q0196."
            ),
        },
        "released_batch2_counts_by_area": {str(area): released_batch2_area.get(area, 0) for area in range(1, 5)},
        "total_release_usable_counts_by_area": {str(area): total_released_area.get(area, 0) for area in range(1, 5)},
        "preview_question_count": len(preview_ids),
        "qa": {"status": "PENDING_EXACT_HEAD_CI"},
    }
    report_path = ROOT / "audits" / "release" / "2026-08-17" / "BATCH2-RELEASE-GOVERNANCE-R2.json"
    write_json(report_path, report)

    print(
        f"Batch 2 governance: released={len(released_ids)} unreleased={len(blocked)} "
        f"areas={dict(sorted(released_batch2_area.items()))} total_usable={dict(sorted(total_released_area.items()))}"
    )
    if blocked:
        for qid in sorted(blocked):
            print(f"BLOCKED {qid}: {'; '.join(blocked[qid])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
