"""Fail-closed preflight for the guarded Pre-Batch3 T2 release of MA-Q-0211..MA-Q-0226.

Issue #83 PHASE C. Every check below must pass before any RELEASED mutation. The
script never repairs anything and never relaxes a rule: it only measures the exact
current repository state and reports the first evidence that would make release unsafe.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import (
    BLOCKED_RULE_STATUSES,
    DATA,
    ROOT,
    VERIFIED_DRUG_STATUSES,
    VERIFIED_RULE_STATUSES,
    QUESTION_AUDIT_FIELDS,
    load_json,
    load_records,
    question_audit_hash,
    semantic_content_hash,
    write_json,
)
from release_context import named_dependency_snapshot, style_profile_snapshot
from validate_audits import is_valid_targeted_initial_audit, validate_audits


T2_IDS = [f"MA-Q-{index:04d}" for index in range(211, 227)]
Q0213 = "MA-Q-0213"
UNCHANGED_IDS = [question_id for question_id in T2_IDS if question_id != Q0213]
QUARANTINED_ID = "MA-Q-0028"

TRANCHE_ID = "PRE-BATCH3-COVERAGE-T2"
AUTHORIZING_ISSUE = 68
REPRESENTED_CANDIDATE_SHA = "b849159ef18d37618ca6badf886e465502436e1b"
AUDITOR_B_ACCEPTED_HEAD = "5242f4c74f06402e0d1b27362831156e0e84a547"

A_LEGAL_AUDIT_ID = "AUDIT-GPT-FRESH-COV-T2-A-LEGAL-TARGETED-INITIAL-2026-08-18"
A_REALISM_AUDIT_ID = "AUDIT-GPT-FRESH-COV-T2-A-REALISM-TARGETED-INITIAL-2026-08-18"
B_LEGAL_AUDIT_ID = "AUDIT-GPT-FRESH-COV-T2-B-LEGAL-REAUDIT-2026-08-19"
B_REALISM_AUDIT_ID = "AUDIT-GPT-FRESH-COV-T2-B-REALISM-REAUDIT-2026-08-19"

AUDITOR_A_CURRENT_PASSING_HASHES = {
    "MA-Q-0211": "0e64b008982afd70481d5cbb98764c33333b9575abf880225d2c342b62e84b30",
    "MA-Q-0212": "804b1f109276192cd626f3d609fc627003e619aa1eed23c39b0d1945b4a20682",
    "MA-Q-0214": "35a7f054480e5c46f8aa3293f30e3ad3716e5f2786ecb6bc741d0068868c94c6",
    "MA-Q-0215": "60cacb955e6fef4d02699c6b3b80f869920551d484dbb9afe8bd1114b911f685",
    "MA-Q-0216": "a59cab0514d45b1e1d10f67e9c01c8d78fda5309abb469c156a37dbd8078f2e5",
    "MA-Q-0217": "e4a5cdd5a5189c56ec9946cfaed177350c425fddff1d17451ea0ceb73399cd66",
    "MA-Q-0218": "ad1ee83f096695440b0068e5989fd8997af7c92020a25fb5d4b6d40b10d036ab",
    "MA-Q-0219": "6caa187601ecc06d17efb4dfa295df327d9fd2f08e9ef60d0027ef215e3a98f3",
    "MA-Q-0220": "72dfe8a9eb2a34ebf251327d80bf8046eec880650ba3070160c8a37d999bc47e",
    "MA-Q-0221": "97d16d872b91e45425ccca675c25cd35bdd9bde85168a4d44c396c95610c6921",
    "MA-Q-0222": "ea4d8ab19e3e1e54132ca076842ce21d47779152c5e0652e6575892454baa571",
    "MA-Q-0223": "857eca7ddc6176091b9ab209244613cb80cb47ae03f10aea48299bab527e5a11",
    "MA-Q-0224": "b4fe81e97a7a555753af73ea9d9f65be6b8d889ddb074ee52ebfaadd66dd96d9",
    "MA-Q-0225": "1cacd9445f05b72dfb15015db5c9d26faee59649a5db714e1e0ec1e236e91444",
    "MA-Q-0226": "7afaf435fff0676352d13f668e5873e3376c902ba96ee0160a83c48d539b29d9",
}
AUDITOR_B_CURRENT_Q0213_HASH = "689120dad57db1ef46087cda3450a8df13799d865c67dd9942f46d7911b1ce23"
HISTORICAL_Q0213_FAILURE_HASH = "993eee2f3d84d3532d757924fa22421c93a7cf16d69b26d40d5f660ca3624548"


class Preflight:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.checks: dict[str, dict] = {}

    def check(self, key: str, ok: bool, detail: object = None) -> bool:
        self.checks[key] = {"status": "PASS" if ok else "FAIL", "detail": detail}
        if not ok:
            self.failures.append(f"{key}: {detail}")
        return ok

    @property
    def ok(self) -> bool:
        return not self.failures


def git_show(sha: str, path: str) -> dict:
    raw = subprocess.check_output(["git", "show", f"{sha}:{path}"], cwd=ROOT)
    return json.loads(raw.decode("utf-8"))


def audited_content(question: dict) -> dict:
    return {field: question.get(field) for field in QUESTION_AUDIT_FIELDS}


def result_for(audit: dict, question_id: str) -> dict | None:
    return next((item for item in audit.get("results", []) if item.get("Question_ID") == question_id), None)


def run() -> tuple[Preflight, dict]:
    pre = Preflight()
    questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}
    rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}
    drugs = {record["drug_id"]: record for _, record in load_records(DATA / "drugs")}
    blueprint = load_json(DATA / "blueprint.json")
    style_profile = load_json(DATA / "exam_style" / "mpje_style_profile.json")
    _, audits = validate_audits()

    # --- 1. recompute all 16 current T2 question_audit_hash values --------------
    current_hashes = {question_id: question_audit_hash(questions[question_id]) for question_id in T2_IDS}
    pre.check("01_recomputed_current_t2_hashes", len(current_hashes) == 16, current_hashes)

    # --- 2. the 15 unchanged IDs must exact-match the Auditor-A passing hashes ---
    mismatched = {
        question_id: {"current": current_hashes[question_id], "auditor_a": expected}
        for question_id, expected in AUDITOR_A_CURRENT_PASSING_HASHES.items()
        if current_hashes[question_id] != expected
    }
    pre.check("02_fifteen_unchanged_match_auditor_a_hashes", not mismatched, mismatched or "15/15 exact match")

    # --- 3. current MA-Q-0213 must exact-match the Auditor-B hash ---------------
    pre.check(
        "03_q0213_matches_auditor_b_hash",
        current_hashes[Q0213] == AUDITOR_B_CURRENT_Q0213_HASH,
        {"current": current_hashes[Q0213], "auditor_b": AUDITOR_B_CURRENT_Q0213_HASH},
    )

    # --- 4/5. current-hash legal + realism pass evidence per partition ----------
    evidence_partition: dict[str, dict] = {}
    evidence_problems: list[str] = []
    for question_id in T2_IDS:
        if question_id == Q0213:
            legal_id, realism_id = B_LEGAL_AUDIT_ID, B_REALISM_AUDIT_ID
        else:
            legal_id, realism_id = A_LEGAL_AUDIT_ID, A_REALISM_AUDIT_ID
        evidence_partition[question_id] = {"legal": legal_id, "realism": realism_id}

        for audit_id, review_type in ((legal_id, "LEGAL_VERIFICATION"), (realism_id, "REALISM_REVIEW")):
            audit = audits.get(audit_id)
            if audit is None:
                evidence_problems.append(f"{question_id}: selected audit {audit_id} is not registered")
                continue
            if audit.get("review_type") != review_type:
                evidence_problems.append(f"{question_id}: {audit_id} is not a {review_type}")
            if audit.get("independent") is not True or audit.get("audit_status") != "FULLY_ADJUDICATED":
                evidence_problems.append(f"{question_id}: {audit_id} is not independent/fully adjudicated")
            if audit.get("question_hashes", {}).get(question_id) != current_hashes[question_id]:
                evidence_problems.append(f"{question_id}: {audit_id} is not bound to the current content hash")
                continue
            result = result_for(audit, question_id)
            if result is None:
                evidence_problems.append(f"{question_id}: {audit_id} has no result row")
                continue
            if review_type == "LEGAL_VERIFICATION":
                if result.get("Verdict") != "KEEP" or result.get("Existing_Answer_Correct") != "YES":
                    evidence_problems.append(f"{question_id}: {audit_id} legal evidence is not KEEP/YES")
            else:
                if result.get("Verdict") != "KEEP" or result.get("Realism_Verdict") != "PASS":
                    evidence_problems.append(f"{question_id}: {audit_id} realism evidence is not KEEP/PASS")
                if audit.get("style_profile") != style_profile_snapshot(style_profile):
                    evidence_problems.append(f"{question_id}: {audit_id} uses a stale style profile snapshot")

    pre.check(
        "04_05_current_hash_legal_and_realism_pass_evidence",
        not evidence_problems,
        evidence_problems or evidence_partition,
    )

    # --- 6. the historical MA-Q-0213 failure is retained at the old hash only ---
    a_realism = audits.get(A_REALISM_AUDIT_ID, {})
    a_realism_q0213 = result_for(a_realism, Q0213) or {}
    historical = {
        "audit_id": A_REALISM_AUDIT_ID,
        "bound_hash": a_realism.get("question_hashes", {}).get(Q0213),
        "Verdict": a_realism_q0213.get("Verdict"),
        "Severity": a_realism_q0213.get("Severity"),
        "Realism_Verdict": a_realism_q0213.get("Realism_Verdict"),
        "distinct_from_bank": a_realism_q0213.get("Criteria", {}).get("distinct_from_bank"),
    }
    pre.check(
        "06_historical_q0213_failure_visible_at_old_hash_only",
        historical["bound_hash"] == HISTORICAL_Q0213_FAILURE_HASH
        and historical["bound_hash"] != current_hashes[Q0213]
        and historical["Verdict"] == "MAJOR_REWRITE"
        and historical["Realism_Verdict"] == "FAIL"
        and historical["distinct_from_bank"] is False,
        historical,
    )

    # --- 7. valid TARGETED_INITIAL_BATCH legal history for all 16 --------------
    history: dict[str, list[str]] = {}
    for question_id in T2_IDS:
        history[question_id] = sorted(
            audit_id
            for audit_id, audit in audits.items()
            if (audit.get("audit_scope") == "INITIAL_BATCH" or is_valid_targeted_initial_audit(audit))
            and audit.get("review_type") == "LEGAL_VERIFICATION"
            and audit.get("independent")
            and audit.get("audit_status") == "FULLY_ADJUDICATED"
            and question_id in audit.get("question_ids", [])
            and result_for(audit, question_id) is not None
        )
    missing_history = {question_id: ids for question_id, ids in history.items() if not ids}
    authorization = audits.get(A_LEGAL_AUDIT_ID, {}).get("governance_authorization", {})
    pre.check(
        "07_targeted_initial_legal_history_for_all_16",
        not missing_history
        and authorization.get("tranche_id") == TRANCHE_ID
        and authorization.get("authorizing_issue") == AUTHORIZING_ISSUE
        and authorization.get("represented_candidate_sha") == REPRESENTED_CANDIDATE_SHA
        and sorted(authorization.get("question_ids", [])) == T2_IDS,
        missing_history or {"authorization": authorization, "per_question_history": history},
    )

    # --- 8. current direct dependency identity and semantic hashes -------------
    dependency_problems: list[str] = []
    dependency_snapshots: dict[str, dict] = {}
    for question_id in T2_IDS:
        question = questions[question_id]
        snapshot = {"rules": {}, "drugs": {}}
        for rule_id in question.get("rule_ids", []):
            rule = rules.get(rule_id)
            if rule is None:
                dependency_problems.append(f"{question_id}: unknown rule {rule_id}")
                continue
            if semantic_content_hash(rule, "rule") != rule.get("content_hash"):
                dependency_problems.append(f"{question_id}: rule {rule_id} content_hash is stale")
            if rule.get("status") != "CURRENT" or rule.get("status") in BLOCKED_RULE_STATUSES:
                dependency_problems.append(f"{question_id}: rule {rule_id} status {rule.get('status')} blocks release")
            if rule.get("verification_status") not in VERIFIED_RULE_STATUSES:
                dependency_problems.append(f"{question_id}: rule {rule_id} is HOLD/unverified")
            snapshot["rules"][rule_id] = {
                "content_version": rule.get("content_version"),
                "content_hash": rule.get("content_hash"),
            }
        for drug_id in question.get("drug_ids", []):
            drug = drugs.get(drug_id)
            if drug is None:
                dependency_problems.append(f"{question_id}: unknown drug {drug_id}")
                continue
            if semantic_content_hash(drug, "drug") != drug.get("content_hash"):
                dependency_problems.append(f"{question_id}: drug {drug_id} content_hash is stale")
            if drug.get("verification_status") not in VERIFIED_DRUG_STATUSES:
                dependency_problems.append(f"{question_id}: drug {drug_id} is HOLD/unverified")
            snapshot["drugs"][drug_id] = {
                "content_version": drug.get("content_version"),
                "content_hash": drug.get("content_hash"),
            }
        dependency_snapshots[question_id] = snapshot

    if semantic_content_hash(blueprint, "blueprint") != blueprint.get("content_hash"):
        dependency_problems.append("blueprint content_hash is stale")
    if semantic_content_hash(style_profile, "style_profile") != style_profile.get("content_hash"):
        dependency_problems.append("style profile content_hash is stale")
    if style_profile.get("valid_for_exams_before") != blueprint.get("applies_to_exams_before"):
        dependency_problems.append("style profile validity date does not match the blueprint")

    context = {
        "blueprint": named_dependency_snapshot(blueprint, "blueprint_id"),
        "style_profile": named_dependency_snapshot(style_profile, "profile_id"),
    }
    pre.check(
        "08_direct_dependency_and_semantic_hash_verification",
        not dependency_problems,
        dependency_problems or {"context": context, "per_question": dependency_snapshots},
    )

    # --- 9. no fully adjudicated current-hash failure for any T2 item ----------
    current_hash_failures: list[dict] = []
    for question_id in T2_IDS:
        for audit_id, audit in sorted(audits.items()):
            if not audit.get("independent") or audit.get("audit_status") != "FULLY_ADJUDICATED":
                continue
            if audit.get("question_hashes", {}).get(question_id) != current_hashes[question_id]:
                continue
            result = result_for(audit, question_id)
            if result is None:
                continue
            if audit.get("review_type") == "LEGAL_VERIFICATION":
                if result.get("Verdict") != "KEEP" or result.get("Existing_Answer_Correct") != "YES":
                    current_hash_failures.append({"question_id": question_id, "audit_id": audit_id, "type": "LEGAL"})
            elif audit.get("review_type") == "REALISM_REVIEW":
                if audit.get("style_profile") != style_profile_snapshot(style_profile):
                    continue
                if result.get("Verdict") != "KEEP" or result.get("Realism_Verdict") != "PASS":
                    current_hash_failures.append({"question_id": question_id, "audit_id": audit_id, "type": "REALISM"})
    pre.check(
        "09_no_current_hash_adjudicated_failure",
        not current_hash_failures,
        current_hash_failures or "no fully adjudicated current-hash failure covers any T2 item",
    )

    # --- 10. MA-Q-0028 quarantine ---------------------------------------------
    allowlist_path = ROOT / "site" / "generated" / "preview_allowlist.json"
    allowlist = load_json(allowlist_path)
    quarantined = questions[QUARANTINED_ID]
    q0028_state = {
        "verification_status": quarantined.get("verification_status"),
        "lifecycle_status": quarantined.get("lifecycle_status"),
        "in_preview_allowlist": QUARANTINED_ID in allowlist.get("question_ids", []),
        "question_audit_hash": question_audit_hash(quarantined),
    }
    pre.check(
        "10_q0028_remains_quarantined_and_unpreviewed",
        q0028_state["verification_status"] != "RELEASED"
        and q0028_state["lifecycle_status"] != "RELEASED"
        and q0028_state["in_preview_allowlist"] is False,
        q0028_state,
    )

    # --- 11. preview membership before mutation --------------------------------
    preview_before = list(allowlist.get("question_ids", []))
    released_before = sorted(
        question_id
        for question_id, question in questions.items()
        if question.get("verification_status") == "RELEASED" and question.get("lifecycle_status") == "RELEASED"
    )
    preview_state = {
        "preview_before_count": len(preview_before),
        "preview_before_contains_any_t2": sorted(set(preview_before) & set(T2_IDS)),
        "released_before_count": len(released_before),
        "released_before_contains_any_t2": sorted(set(released_before) & set(T2_IDS)),
        "source_audits_before_count": len(allowlist.get("source_audits", [])),
    }
    pre.check(
        "11_preview_membership_captured_before_mutation",
        len(preview_before) == len(set(preview_before)),
        preview_state,
    )

    # --- 12. no substantive T2 change since the accepted evidence ---------------
    substantive_problems: list[str] = []
    for question_id in UNCHANGED_IDS:
        source = git_show(REPRESENTED_CANDIDATE_SHA, f"data/questions/{question_id.lower()}.json")
        if audited_content(source) != audited_content(questions[question_id]):
            substantive_problems.append(f"{question_id}: audited content differs from {REPRESENTED_CANDIDATE_SHA[:12]}")
    q0213_source = git_show(AUDITOR_B_ACCEPTED_HEAD, "data/questions/ma-q-0213.json")
    if audited_content(q0213_source) != audited_content(questions[Q0213]):
        substantive_problems.append(f"{Q0213}: audited content differs from Auditor-B accepted head")
    pre.check(
        "12_no_substantive_t2_change_since_accepted_evidence",
        not substantive_problems,
        substantive_problems
        or {
            "fifteen_unchanged_compared_against": REPRESENTED_CANDIDATE_SHA,
            "q0213_compared_against": AUDITOR_B_ACCEPTED_HEAD,
            "compared_fields": list(QUESTION_AUDIT_FIELDS),
        },
    )

    payload = {
        "report_type": "PRE_BATCH3_T2_GUARDED_RELEASE_PREFLIGHT",
        "controller_issue": 83,
        "tranche_id": TRANCHE_ID,
        "authorizing_issue": AUTHORIZING_ISSUE,
        "question_ids": T2_IDS,
        "status": "PASS" if pre.ok else "FAIL",
        "current_question_hashes": current_hashes,
        "evidence_partition": evidence_partition,
        "dependency_snapshots": dependency_snapshots,
        "release_context": context,
        "preview_before": preview_state,
        "preview_before_ids": preview_before,
        "released_before_count": len(released_before),
        "historical_q0213_failure": historical,
        "checks": pre.checks,
        "failures": pre.failures,
    }
    return pre, payload


def main() -> int:
    pre, payload = run()
    output = ROOT / "audits" / "remediation" / "2026-08-19" / "PRE-BATCH3-T2-GUARDED-RELEASE-PREFLIGHT.json"
    write_json(output, payload)
    for key, value in payload["checks"].items():
        print(f"[{value['status']}] {key}")
    for failure in pre.failures:
        print(f"FAIL {failure}")
    print(f"preflight: {'PASS' if pre.ok else 'FAIL'} -> {output.relative_to(ROOT).as_posix()}")
    return 0 if pre.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
