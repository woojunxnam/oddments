from __future__ import annotations

import argparse
from collections import Counter
from datetime import date

from qa_common import (
    BLOCKED_RULE_STATUSES,
    DATA,
    ROOT,
    VERIFIED_DRUG_STATUSES,
    VERIFIED_RULE_STATUSES,
    dependency_snapshot,
    load_json,
    load_records,
    question_audit_hash,
    write_json,
)
from release_context import named_dependency_snapshot, style_profile_snapshot

TODAY = date(2026, 8, 17).isoformat()
SOURCE_SHA = "2f7dcd6b6ea06787e1e0a5dc76f93b0f2fc78eab"
ORIGINAL_T1_SHA = "c99161a7f3e50bb95491de98f895795989d22a16"

B_LEGAL = "AUDIT-GPT-FRESH-COV-T1-B-LEGAL-INITIAL-2026-08-17"
B_REALISM = "AUDIT-GPT-FRESH-COV-T1-B-REALISM-INITIAL-2026-08-17"
D_LEGAL = "AUDIT-GPT-FRESH-COV-T1-D-LEGAL-REAUDIT-2026-08-17"
D_REALISM = "AUDIT-GPT-FRESH-COV-T1-D-REALISM-REAUDIT-2026-08-17"

T1_ALL = {
    "MA-Q-0004", "MA-Q-0009", "MA-Q-0013", "MA-Q-0015", "MA-Q-0016", "MA-Q-0017",
    "MA-Q-0020", "MA-Q-0027", "MA-Q-0028", "MA-Q-0030", "MA-Q-0032", "MA-Q-0034",
    "MA-Q-0036", "MA-Q-0040", "MA-Q-0059", "MA-Q-0060", "MA-Q-0075", "MA-Q-0076",
    "MA-Q-0077", "MA-Q-0078", "MA-Q-0079", "MA-Q-0080", "MA-Q-0081", "MA-Q-0082",
    "MA-Q-0083", "MA-Q-0084", "MA-Q-0085", "MA-Q-0086", "MA-Q-0087", "MA-Q-0088",
}
QUARANTINE = "MA-Q-0028"
CHANGED_PASS = {"MA-Q-0032", "MA-Q-0036"}
ADMIT = T1_ALL - {QUARANTINE}
UNCHANGED_PASS = ADMIT - CHANGED_PASS

EXPECTED_CHANGED_HASHES = {
    "MA-Q-0032": "f819dd7808361e9c1722049b7b3c8542d9ad85b0980fa5d140500f10733edd88",
    "MA-Q-0036": "4a13dec96ebf24eaa258600e797267957d45f1318935daafc594c17edc72c388",
}
EXPECTED_QUARANTINE_HASH = "9479b83d2dae97ceff373869d477e9e402bd6d5970095600387fa47f290c2e23"

RESULT_PATH = ROOT / "audits" / "remediation" / "2026-08-17" / "PRE-BATCH3-T1-GUARDED-ADMISSION.json"


def qpath(qid: str):
    return DATA / "questions" / f"ma-q-{qid[-4:]}.json"


def audit_index() -> dict[str, dict]:
    return {record["audit_id"]: record for _, record in load_records(DATA / "audits")}


def result_for(audit: dict, qid: str) -> dict:
    result = next((item for item in audit.get("results", []) if item.get("Question_ID") == qid), None)
    if result is None:
        raise RuntimeError(f"{audit.get('audit_id')} has no result for {qid}")
    return result


def require_audit_identity(audit: dict, *, review_type: str) -> None:
    if not audit.get("independent") or audit.get("audit_status") != "FULLY_ADJUDICATED":
        raise RuntimeError(f"audit not independently fully adjudicated: {audit.get('audit_id')}")
    if audit.get("review_type") != review_type:
        raise RuntimeError(f"audit review type mismatch: {audit.get('audit_id')}")


def require_current_pass(
    *, qid: str, question: dict, legal: dict, realism: dict, style_profile: dict
) -> str:
    current_hash = question_audit_hash(question)
    if legal.get("question_hashes", {}).get(qid) != current_hash:
        raise RuntimeError(f"{qid}: current hash does not match legal audit")
    if realism.get("question_hashes", {}).get(qid) != current_hash:
        raise RuntimeError(f"{qid}: current hash does not match realism audit")
    legal_result = result_for(legal, qid)
    realism_result = result_for(realism, qid)
    if legal_result.get("Verdict") != "KEEP" or legal_result.get("Existing_Answer_Correct") != "YES":
        raise RuntimeError(f"{qid}: legal audit is not KEEP/YES")
    if realism_result.get("Verdict") != "KEEP" or realism_result.get("Realism_Verdict") != "PASS":
        raise RuntimeError(f"{qid}: realism audit is not KEEP/PASS")
    if realism.get("style_profile") != style_profile_snapshot(style_profile):
        raise RuntimeError(f"{qid}: realism audit style profile is stale")
    return current_hash


def require_dependency_releaseability(question: dict, rules: dict[str, dict], drugs: dict[str, dict]) -> None:
    qid = question["question_id"]
    for rule_id in question.get("rule_ids", []):
        rule = rules.get(rule_id)
        if rule is None:
            raise RuntimeError(f"{qid}: unknown rule {rule_id}")
        if rule.get("status") != "CURRENT" or rule.get("status") in BLOCKED_RULE_STATUSES:
            raise RuntimeError(f"{qid}: blocked rule {rule_id}")
        if rule.get("verification_status") not in VERIFIED_RULE_STATUSES:
            raise RuntimeError(f"{qid}: unverified rule {rule_id}")
    for drug_id in question.get("drug_ids", []):
        drug = drugs.get(drug_id)
        if drug is None:
            raise RuntimeError(f"{qid}: unknown drug {drug_id}")
        if drug.get("verification_status") not in VERIFIED_DRUG_STATUSES:
            raise RuntimeError(f"{qid}: unverified drug {drug_id}")


def load_state():
    questions = {qid: load_json(qpath(qid)) for qid in sorted(T1_ALL)}
    rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}
    drugs = {record["drug_id"]: record for _, record in load_records(DATA / "drugs")}
    audits = audit_index()
    blueprint = load_json(DATA / "blueprint.json")
    style_profile = load_json(DATA / "exam_style" / "mpje_style_profile.json")
    matrix = load_json(DATA / "exam_style" / "question_family_matrix.json")
    allowlist = load_json(ROOT / "site" / "generated" / "preview_allowlist.json")
    return questions, rules, drugs, audits, blueprint, style_profile, matrix, allowlist


def preflight() -> dict:
    questions, rules, drugs, audits, blueprint, style_profile, matrix, allowlist = load_state()

    for audit_id in (B_LEGAL, B_REALISM, D_LEGAL, D_REALISM):
        if audit_id not in audits:
            raise RuntimeError(f"missing canonical audit: {audit_id}")
    require_audit_identity(audits[B_LEGAL], review_type="LEGAL_VERIFICATION")
    require_audit_identity(audits[B_REALISM], review_type="REALISM_REVIEW")
    require_audit_identity(audits[D_LEGAL], review_type="LEGAL_VERIFICATION")
    require_audit_identity(audits[D_REALISM], review_type="REALISM_REVIEW")

    current_hashes: dict[str, str] = {}
    for qid in sorted(UNCHANGED_PASS):
        q = questions[qid]
        if q.get("verification_status") == "RELEASED" or q.get("lifecycle_status") == "RELEASED":
            raise RuntimeError(f"{qid}: unexpectedly already RELEASED at source boundary")
        current_hashes[qid] = require_current_pass(
            qid=qid,
            question=q,
            legal=audits[B_LEGAL],
            realism=audits[B_REALISM],
            style_profile=style_profile,
        )
        require_dependency_releaseability(q, rules, drugs)

    for qid in sorted(CHANGED_PASS):
        q = questions[qid]
        if q.get("verification_status") == "RELEASED" or q.get("lifecycle_status") == "RELEASED":
            raise RuntimeError(f"{qid}: unexpectedly already RELEASED at source boundary")
        current_hashes[qid] = require_current_pass(
            qid=qid,
            question=q,
            legal=audits[D_LEGAL],
            realism=audits[D_REALISM],
            style_profile=style_profile,
        )
        if current_hashes[qid] != EXPECTED_CHANGED_HASHES[qid]:
            raise RuntimeError(f"{qid}: changed-item hash differs from Issue #57 lock")
        require_dependency_releaseability(q, rules, drugs)
        if qid not in audits[B_LEGAL].get("question_ids", []):
            raise RuntimeError(f"{qid}: lacks required INITIAL_BATCH legal history")

    quarantine = questions[QUARANTINE]
    quarantine_hash = question_audit_hash(quarantine)
    if quarantine_hash != EXPECTED_QUARANTINE_HASH:
        raise RuntimeError("Q0028: current hash differs from Issue #57 quarantine lock")
    if audits[D_LEGAL].get("question_hashes", {}).get(QUARANTINE) != quarantine_hash:
        raise RuntimeError("Q0028: D legal audit is not on current content")
    if audits[D_REALISM].get("question_hashes", {}).get(QUARANTINE) != quarantine_hash:
        raise RuntimeError("Q0028: D realism audit is not on current content")
    if result_for(audits[D_LEGAL], QUARANTINE).get("Verdict") != "KEEP" or result_for(audits[D_LEGAL], QUARANTINE).get("Existing_Answer_Correct") != "YES":
        raise RuntimeError("Q0028: expected current legal KEEP/YES quarantine evidence")
    q28_realism = result_for(audits[D_REALISM], QUARANTINE)
    if q28_realism.get("Realism_Verdict") != "FAIL" or q28_realism.get("Verdict") not in {"DELETE", "DROP"}:
        raise RuntimeError("Q0028: expected current failed realism DROP/DELETE evidence")
    if quarantine.get("verification_status") == "RELEASED" or quarantine.get("lifecycle_status") == "RELEASED":
        raise RuntimeError("Q0028: must not be RELEASED before guarded admission")

    # Project family release counts before mutation and reject any cap violation up front.
    all_questions = [record for _, record in load_records(DATA / "questions")]
    current_released = Counter(
        q.get("family_id") for q in all_questions
        if q.get("verification_status") == "RELEASED" and q.get("lifecycle_status") == "RELEASED"
    )
    projected = current_released.copy()
    for qid in ADMIT:
        projected[questions[qid]["family_id"]] += 1
    families = {family["family_id"]: family for family in matrix.get("families", [])}
    for family_id, count in projected.items():
        family = families.get(family_id)
        if family is None:
            raise RuntimeError(f"missing family matrix entry: {family_id}")
        if count > family.get("max_questions_in_final_bank", 0):
            raise RuntimeError(
                f"projected release exceeds family maximum: {family_id} {count} > {family.get('max_questions_in_final_bank')}"
            )

    before_ids = list(allowlist.get("question_ids", []))
    return {
        "questions": questions,
        "rules": rules,
        "drugs": drugs,
        "audits": audits,
        "blueprint": blueprint,
        "style_profile": style_profile,
        "matrix": matrix,
        "allowlist": allowlist,
        "current_hashes": current_hashes,
        "quarantine_hash": quarantine_hash,
        "before_preview_ids": before_ids,
    }


def sync_family_release_counts() -> None:
    released_counts: Counter[str] = Counter()
    for _, question in load_records(DATA / "questions"):
        if question.get("verification_status") == "RELEASED" and question.get("lifecycle_status") == "RELEASED":
            released_counts[question["family_id"]] += 1
    matrix_path = DATA / "exam_style" / "question_family_matrix.json"
    matrix = load_json(matrix_path)
    for family in matrix.get("families", []):
        family["current_released_count"] = released_counts.get(family["family_id"], 0)
    matrix["last_reviewed"] = TODAY
    write_json(matrix_path, matrix)


def apply() -> dict:
    state = preflight()
    questions = state["questions"]
    rules = state["rules"]
    drugs = state["drugs"]
    blueprint = state["blueprint"]
    style_profile = state["style_profile"]

    for qid in sorted(ADMIT):
        q = questions[qid]
        if qid in CHANGED_PASS:
            audit_ids = [D_LEGAL, D_REALISM]
            note = (
                "Pre-Batch3 T1 guarded admission after fresh changed-item current-hash legal KEEP/YES and "
                "FULL-bank realism KEEP/PASS under Issue #54; Issue #56 quarantines MA-Q-0028."
            )
        else:
            audit_ids = [B_LEGAL, B_REALISM]
            note = (
                "Pre-Batch3 T1 guarded admission after fresh INITIAL_BATCH current-hash legal KEEP/YES and "
                "FULL-bank realism KEEP/PASS; Issue #56 quarantines MA-Q-0028."
            )
        q["verification_status"] = "RELEASED"
        q["lifecycle_status"] = "RELEASED"
        q["last_legal_review"] = TODAY
        q["audits"] = audit_ids
        q["duplicate_review_status"] = "CLEAR"
        q["independent_audit_status"] = "PASSED"
        q["final_adjudication"] = {
            "decision": "KEEP",
            "adjudicator": "GPT-5.6-Sol governance after Issues #54 and #56",
            "date": TODAY,
            "notes": note,
            "verified_dependencies": {
                "rules": {rule_id: dependency_snapshot(rules[rule_id]) for rule_id in q.get("rule_ids", [])},
                "drugs": {drug_id: dependency_snapshot(drugs[drug_id]) for drug_id in q.get("drug_ids", [])},
                "blueprint": named_dependency_snapshot(blueprint, "blueprint_id"),
                "style_profile": named_dependency_snapshot(style_profile, "profile_id"),
            },
        }
        write_json(qpath(qid), q)

    # Q0028 is intentionally not written. Its exact failed audited record remains intact.
    sync_family_release_counts()

    allowlist_path = ROOT / "site" / "generated" / "preview_allowlist.json"
    allowlist = state["allowlist"]
    before_ids = list(state["before_preview_ids"])
    ids = [qid for qid in before_ids if qid != QUARANTINE]
    for qid in sorted(ADMIT):
        if qid not in ids:
            ids.append(qid)
    allowlist["generated_date"] = TODAY
    allowlist["source_audits"] = list(dict.fromkeys(
        list(allowlist.get("source_audits", [])) + [B_LEGAL, B_REALISM, D_LEGAL, D_REALISM]
    ))
    allowlist["notice"] = (
        "Preview contains prior released questions plus the 29 Pre-Batch3 T1 legacy questions admitted by guarded "
        "release governance after current-hash legal/realism verification. MA-Q-0028 remains quarantined after "
        "fresh realism failure and is excluded from preview."
    )
    allowlist["question_ids"] = ids
    write_json(allowlist_path, allowlist)

    added = [qid for qid in ids if qid not in before_ids]
    removed = [qid for qid in before_ids if qid not in ids]
    result = {
        "governance_issue": 57,
        "source_sha": SOURCE_SHA,
        "original_t1_candidate_sha": ORIGINAL_T1_SHA,
        "admitted_count": len(ADMIT),
        "admitted_question_ids": sorted(ADMIT),
        "quarantined_question_id": QUARANTINE,
        "quarantined_question_hash": state["quarantine_hash"],
        "before_preview_count": len(before_ids),
        "after_preview_count": len(ids),
        "preview_added_ids": added,
        "preview_removed_ids": removed,
        "audit_evidence": {
            "unchanged_27": [B_LEGAL, B_REALISM],
            "changed_q0032_q0036": [D_LEGAL, D_REALISM],
        },
        "current_question_hashes": state["current_hashes"],
    }
    write_json(RESULT_PATH, result)
    print(
        f"guarded T1 admission applied: {len(ADMIT)} RELEASED; Q0028 quarantined; "
        f"preview {len(before_ids)} -> {len(ids)} (added {len(added)}, removed {len(removed)})"
    )
    return result


def verify_post() -> None:
    questions, rules, drugs, audits, blueprint, style_profile, matrix, allowlist = load_state()
    released = {
        qid for qid, q in questions.items()
        if q.get("verification_status") == "RELEASED" and q.get("lifecycle_status") == "RELEASED"
    }
    if released != ADMIT:
        raise RuntimeError(f"T1 release set mismatch: expected {len(ADMIT)}, got {sorted(released)}")
    q28 = questions[QUARANTINE]
    if q28.get("verification_status") == "RELEASED" or q28.get("lifecycle_status") == "RELEASED":
        raise RuntimeError("Q0028 was incorrectly released")
    if q28.get("audits") or q28.get("final_adjudication") is not None:
        raise RuntimeError("Q0028 quarantine metadata was unexpectedly converted into release evidence")
    if question_audit_hash(q28) != EXPECTED_QUARANTINE_HASH:
        raise RuntimeError("Q0028 substantive hash changed during release")
    preview_ids = list(allowlist.get("question_ids", []))
    if QUARANTINE in preview_ids:
        raise RuntimeError("Q0028 remains in preview allowlist")
    missing_preview = sorted(ADMIT - set(preview_ids))
    if missing_preview:
        raise RuntimeError(f"released T1 IDs missing from preview: {missing_preview}")

    for qid in sorted(ADMIT):
        q = questions[qid]
        expected_audits = [D_LEGAL, D_REALISM] if qid in CHANGED_PASS else [B_LEGAL, B_REALISM]
        if q.get("audits") != expected_audits:
            raise RuntimeError(f"{qid}: release audit references differ from guarded set")
        if q.get("duplicate_review_status") != "CLEAR" or q.get("independent_audit_status") != "PASSED":
            raise RuntimeError(f"{qid}: release status summaries invalid")
        if q.get("final_adjudication", {}).get("decision") != "KEEP":
            raise RuntimeError(f"{qid}: final adjudication is not KEEP")
        legal = audits[D_LEGAL] if qid in CHANGED_PASS else audits[B_LEGAL]
        realism = audits[D_REALISM] if qid in CHANGED_PASS else audits[B_REALISM]
        require_current_pass(qid=qid, question=q, legal=legal, realism=realism, style_profile=style_profile)

    actual_released_counts = Counter(
        q.get("family_id") for _, q in load_records(DATA / "questions")
        if q.get("verification_status") == "RELEASED" and q.get("lifecycle_status") == "RELEASED"
    )
    for family in matrix.get("families", []):
        if family.get("current_released_count") != actual_released_counts.get(family["family_id"], 0):
            raise RuntimeError(f"stale family released count: {family['family_id']}")

    result = load_json(RESULT_PATH)
    if result.get("admitted_count") != 29 or result.get("quarantined_question_id") != QUARANTINE:
        raise RuntimeError("release result artifact mismatch")
    if result.get("preview_removed_ids") != [QUARANTINE]:
        raise RuntimeError(f"expected only Q0028 preview removal, got {result.get('preview_removed_ids')}")
    print(
        f"post-release guard PASS: 29 T1 RELEASED; Q0028 quarantined; preview count {len(preview_ids)}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--verify-post", action="store_true")
    args = parser.parse_args()
    if sum([args.check, args.apply, args.verify_post]) != 1:
        raise SystemExit("choose exactly one of --check, --apply, --verify-post")
    if args.check:
        state = preflight()
        print(
            f"preflight PASS: {len(ADMIT)} admission candidates; Q0028 quarantined; "
            f"preview count {len(state['before_preview_ids'])}"
        )
    elif args.apply:
        apply()
    else:
        verify_post()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
