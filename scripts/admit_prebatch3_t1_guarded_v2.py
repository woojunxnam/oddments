from __future__ import annotations

from collections import Counter
from copy import deepcopy
from datetime import date
from pathlib import Path

from qa_common import DATA, ROOT, dependency_snapshot, load_json, load_records, question_audit_hash, write_json
from release_context import named_dependency_snapshot

SOURCE_SHA = "c044680e6efbf07d7975ae033754c8e366fa91fa"
TODAY = date(2026, 8, 18).isoformat()

T1 = {
    "MA-Q-0004", "MA-Q-0009", "MA-Q-0013", "MA-Q-0015", "MA-Q-0016", "MA-Q-0017",
    "MA-Q-0020", "MA-Q-0027", "MA-Q-0028", "MA-Q-0030", "MA-Q-0032", "MA-Q-0034",
    "MA-Q-0036", "MA-Q-0040", "MA-Q-0059", "MA-Q-0060", "MA-Q-0075", "MA-Q-0076",
    "MA-Q-0077", "MA-Q-0078", "MA-Q-0079", "MA-Q-0080", "MA-Q-0081", "MA-Q-0082",
    "MA-Q-0083", "MA-Q-0084", "MA-Q-0085", "MA-Q-0086", "MA-Q-0087", "MA-Q-0088",
}
QUARANTINED = "MA-Q-0028"
ADMIT = T1 - {QUARANTINED}

B_IDS = {
    "MA-Q-0004", "MA-Q-0009", "MA-Q-0013", "MA-Q-0015", "MA-Q-0016", "MA-Q-0017",
    "MA-Q-0020", "MA-Q-0027", "MA-Q-0030", "MA-Q-0034", "MA-Q-0040", "MA-Q-0059",
    "MA-Q-0060", "MA-Q-0075", "MA-Q-0076", "MA-Q-0077", "MA-Q-0078", "MA-Q-0080",
    "MA-Q-0081", "MA-Q-0085", "MA-Q-0086", "MA-Q-0087", "MA-Q-0088",
}
D_IDS = {"MA-Q-0032", "MA-Q-0036"}
H_IDS = {"MA-Q-0079", "MA-Q-0082", "MA-Q-0083", "MA-Q-0084"}

AUDITS = {
    "B": (
        "AUDIT-GPT-FRESH-COV-T1-B-LEGAL-INITIAL-2026-08-17",
        "AUDIT-GPT-FRESH-COV-T1-B-REALISM-INITIAL-2026-08-17",
        "GPT-FRESH-COV-T1-B",
    ),
    "D": (
        "AUDIT-GPT-FRESH-COV-T1-D-LEGAL-REAUDIT-2026-08-17",
        "AUDIT-GPT-FRESH-COV-T1-D-REALISM-REAUDIT-2026-08-17",
        "GPT-FRESH-COV-T1-D",
    ),
    "H": (
        "AUDIT-GPT-FRESH-COV-T1-H-LEGAL-REAUDIT-PRE-BATCH3-T1-R2-V4-2026-08-18",
        "AUDIT-GPT-FRESH-COV-T1-H-REALISM-REAUDIT-PRE-BATCH3-T1-R2-V4-2026-08-18",
        "GPT-FRESH-COV-T1-H",
    ),
}

EXPECTED_H_HASHES = {
    "MA-Q-0079": "dfaaa6be825dcc4f188c4aa8d0bd586328491e6d66b8663bc5b741d6ad647428",
    "MA-Q-0082": "0850168860dff36347501ca395ac6887ba14487f29dde0abf8b6227d77cc405a",
    "MA-Q-0083": "a01cb4554aef91a992a30898babf9de7c9901b10b8c1ed0fdcea40fb57779097",
    "MA-Q-0084": "c68af619264bf35ac429d32997d2e52083d17e93692ac4ebe3d4ccdf4b3b33da",
}
EXPECTED_Q0028_HASH = "9479b83d2dae97ceff373869d477e9e402bd6d5970095600387fa47f290c2e23"


def qpath(qid: str) -> Path:
    return DATA / "questions" / f"ma-q-{qid[-4:]}.json"


def result_index(audit: dict) -> dict[str, dict]:
    return {item["Question_ID"]: item for item in audit.get("results", [])}


def load_audit(audit_id: str, review_type: str, auditor_instance: str) -> dict:
    audit = load_json(DATA / "audits" / f"{audit_id}.json")
    if audit.get("audit_id") != audit_id:
        raise RuntimeError(f"audit id mismatch: {audit_id}")
    if audit.get("audit_status") != "FULLY_ADJUDICATED":
        raise RuntimeError(f"audit not fully adjudicated: {audit_id}")
    if audit.get("independent") is not True:
        raise RuntimeError(f"audit not independent: {audit_id}")
    if audit.get("review_type") != review_type:
        raise RuntimeError(f"review type mismatch: {audit_id}")
    if audit.get("auditor_instance") != auditor_instance:
        raise RuntimeError(f"auditor instance mismatch: {audit_id}")
    return audit


def pair_for(qid: str) -> tuple[str, str, str]:
    if qid in B_IDS:
        return AUDITS["B"]
    if qid in D_IDS:
        return AUDITS["D"]
    if qid in H_IDS:
        return AUDITS["H"]
    raise RuntimeError(f"no evidence partition for {qid}")


def sync_family_counts() -> None:
    candidate_counts: Counter[str] = Counter()
    released_counts: Counter[str] = Counter()
    for _, question in load_records(DATA / "questions"):
        family_id = question.get("family_id")
        if not family_id:
            continue
        candidate_counts[family_id] += 1
        if question.get("verification_status") == "RELEASED" and question.get("lifecycle_status") == "RELEASED":
            released_counts[family_id] += 1

    path = DATA / "exam_style" / "question_family_matrix.json"
    matrix = load_json(path)
    known = {family["family_id"] for family in matrix.get("families", [])}
    missing = sorted(set(candidate_counts) - known)
    if missing:
        raise RuntimeError(f"question family missing from matrix: {missing}")
    for family in matrix.get("families", []):
        fid = family["family_id"]
        family["current_candidate_count"] = candidate_counts.get(fid, 0)
        family["current_released_count"] = released_counts.get(fid, 0)
    matrix["last_reviewed"] = TODAY
    write_json(path, matrix)


def main() -> int:
    if len(T1) != 30 or len(ADMIT) != 29 or len(B_IDS) != 23 or len(D_IDS) != 2 or len(H_IDS) != 4:
        raise RuntimeError("locked T1/evidence partition size mismatch")
    if B_IDS | D_IDS | H_IDS != ADMIT or (B_IDS & D_IDS) or (B_IDS & H_IDS) or (D_IDS & H_IDS):
        raise RuntimeError("evidence partition is not an exact disjoint cover of the 29 admission IDs")

    loaded_audits: dict[str, dict] = {}
    loaded_results: dict[str, dict[str, dict]] = {}
    for key, (legal_id, realism_id, auditor_instance) in AUDITS.items():
        legal = load_audit(legal_id, "LEGAL_VERIFICATION", auditor_instance)
        realism = load_audit(realism_id, "REALISM_REVIEW", auditor_instance)
        loaded_audits[legal_id] = legal
        loaded_audits[realism_id] = realism
        loaded_results[legal_id] = result_index(legal)
        loaded_results[realism_id] = result_index(realism)

    rules = {r["rule_id"]: r for _, r in load_records(DATA / "rules")}
    drugs = {d["drug_id"]: d for _, d in load_records(DATA / "drugs")}
    blueprint = load_json(DATA / "blueprint.json")
    style_profile = load_json(DATA / "exam_style" / "mpje_style_profile.json")

    before_questions = {qid: load_json(qpath(qid)) for qid in T1}
    before_hashes = {qid: question_audit_hash(q) for qid, q in before_questions.items()}
    q0190_before = question_audit_hash(load_json(qpath("MA-Q-0190")))

    # Pre-mutation current-hash legal + realism gate for all 29.
    evidence_by_question: dict[str, tuple[str, str]] = {}
    for qid in sorted(ADMIT):
        legal_id, realism_id, _ = pair_for(qid)
        legal = loaded_audits[legal_id]
        realism = loaded_audits[realism_id]
        actual_hash = before_hashes[qid]
        if legal.get("question_hashes", {}).get(qid) != actual_hash:
            raise RuntimeError(f"stale legal audit hash for {qid}: {legal_id}")
        if realism.get("question_hashes", {}).get(qid) != actual_hash:
            raise RuntimeError(f"stale realism audit hash for {qid}: {realism_id}")
        lres = loaded_results[legal_id].get(qid)
        rres = loaded_results[realism_id].get(qid)
        if not lres or lres.get("Verdict") != "KEEP" or lres.get("Existing_Answer_Correct") != "YES":
            raise RuntimeError(f"legal release gate failed for {qid}")
        if not rres or rres.get("Verdict") != "KEEP" or rres.get("Realism_Verdict") != "PASS":
            raise RuntimeError(f"realism release gate failed for {qid}")
        evidence_by_question[qid] = (legal_id, realism_id)

    for qid, expected in EXPECTED_H_HASHES.items():
        if before_hashes[qid] != expected:
            raise RuntimeError(f"Auditor-H frozen hash mismatch for {qid}")

    # Q0028 must match D's failed current-hash realism evidence and stay quarantined.
    d_legal_id, d_realism_id, _ = AUDITS["D"]
    if before_hashes[QUARANTINED] != EXPECTED_Q0028_HASH:
        raise RuntimeError("Q0028 current hash differs from adjudicated quarantine hash")
    dlegal = loaded_audits[d_legal_id]
    drealism = loaded_audits[d_realism_id]
    if dlegal.get("question_hashes", {}).get(QUARANTINED) != EXPECTED_Q0028_HASH:
        raise RuntimeError("Q0028 D legal hash mismatch")
    if drealism.get("question_hashes", {}).get(QUARANTINED) != EXPECTED_Q0028_HASH:
        raise RuntimeError("Q0028 D realism hash mismatch")
    q28l = loaded_results[d_legal_id][QUARANTINED]
    q28r = loaded_results[d_realism_id][QUARANTINED]
    if q28l.get("Verdict") != "KEEP" or q28l.get("Existing_Answer_Correct") != "YES":
        raise RuntimeError("unexpected Q0028 legal disposition")
    if q28r.get("Realism_Verdict") != "FAIL" or q28r.get("Verdict") in {"KEEP", "PASS"}:
        raise RuntimeError("Q0028 is not carrying the required failed realism evidence")
    if q28r.get("Criteria", {}).get("distinct_from_bank") is not False:
        raise RuntimeError("Q0028 failed realism evidence does not preserve distinct_from_bank=false")

    allowlist_path = ROOT / "site" / "generated" / "preview_allowlist.json"
    allowlist = load_json(allowlist_path)
    before_preview_ids = list(allowlist.get("question_ids", []))
    before_preview_count = len(before_preview_ids)
    before_preview_t1 = sorted(set(before_preview_ids) & T1)
    q0028_was_in_preview = QUARANTINED in before_preview_ids
    if not q0028_was_in_preview:
        raise RuntimeError("expected current source preview to contain Q0028 before quarantine removal")

    # Release metadata only; question audit hashes must remain unchanged.
    for qid in sorted(ADMIT):
        path = qpath(qid)
        question = load_json(path)
        legal_id, realism_id = evidence_by_question[qid]
        question["audits"] = [legal_id, realism_id]
        question["verification_status"] = "RELEASED"
        question["lifecycle_status"] = "RELEASED"
        question["last_legal_review"] = TODAY
        question["duplicate_review_status"] = "CLEAR"
        question["independent_audit_status"] = "PASSED"
        question["final_adjudication"] = {
            "decision": "KEEP",
            "adjudicator": "GPT-5.6-Sol release-governance editor after independent T1 B/D/H audits",
            "date": TODAY,
            "notes": (
                "Pre-Batch3 T1 guarded admission under Issue #65. Current-hash legal KEEP/YES and realism "
                "KEEP/PASS evidence was selected per question from fresh Auditor B, D, or H evidence. "
                "MA-Q-0028 remains quarantined after current-hash realism failure and is not released."
            ),
            "verified_dependencies": {
                "rules": {rid: dependency_snapshot(rules[rid]) for rid in question.get("rule_ids", [])},
                "drugs": {did: dependency_snapshot(drugs[did]) for did in question.get("drug_ids", [])},
                "blueprint": named_dependency_snapshot(blueprint, "blueprint_id"),
                "style_profile": named_dependency_snapshot(style_profile, "profile_id"),
            },
        }
        write_json(path, question)

    # Preserve Q0028 canonical question record untouched; only remove its preview membership.
    q28_after = load_json(qpath(QUARANTINED))
    if q28_after != before_questions[QUARANTINED]:
        raise RuntimeError("Q0028 canonical record changed during guarded admission")

    sync_family_counts()

    ids = [qid for qid in before_preview_ids if qid != QUARANTINED]
    for qid in sorted(ADMIT):
        if qid not in ids:
            ids.append(qid)
    if QUARANTINED in ids:
        raise RuntimeError("Q0028 leaked into post-admission preview")

    all_selected_audits = []
    for qid in sorted(ADMIT):
        all_selected_audits.extend(evidence_by_question[qid])
    # D realism is also the explicit quarantine evidence; preserve it in preview provenance even though Q0028 is excluded.
    all_selected_audits.append(d_realism_id)
    all_selected_audits.append(d_legal_id)

    allowlist["generated_date"] = TODAY
    allowlist["source_audits"] = list(dict.fromkeys(list(allowlist.get("source_audits", [])) + all_selected_audits))
    allowlist["notice"] = (
        "Preview contains prior released questions plus the 29 Pre-Batch3 T1 legacy questions admitted under "
        "Issue #65 after current-hash independent legal and full-bank realism evidence. MA-Q-0028 is quarantined "
        "after a current-hash realism distinctness failure and is not shown."
    )
    allowlist["question_ids"] = ids
    write_json(allowlist_path, allowlist)

    after_preview_count = len(ids)
    after_preview_t1 = sorted(set(ids) & T1)

    # Post-mutation assertions.
    after_questions = {qid: load_json(qpath(qid)) for qid in T1}
    after_hashes = {qid: question_audit_hash(q) for qid, q in after_questions.items()}
    if after_hashes != before_hashes:
        changed_hashes = sorted(qid for qid in T1 if after_hashes[qid] != before_hashes[qid])
        raise RuntimeError(f"substantive T1 question content changed during admission: {changed_hashes}")

    released = {
        qid for qid, q in after_questions.items()
        if q.get("verification_status") == "RELEASED" and q.get("lifecycle_status") == "RELEASED"
    }
    if released != ADMIT:
        raise RuntimeError(f"released T1 set mismatch: {sorted(released)}")
    q28 = after_questions[QUARANTINED]
    if q28.get("verification_status") == "RELEASED" or q28.get("lifecycle_status") == "RELEASED":
        raise RuntimeError("Q0028 was incorrectly released")
    if q28.get("final_adjudication") is not None:
        raise RuntimeError("Q0028 received an unexpected release adjudication")
    if QUARANTINED in load_json(allowlist_path).get("question_ids", []):
        raise RuntimeError("Q0028 remains in preview after quarantine")

    for qid in sorted(ADMIT):
        q = after_questions[qid]
        expected_audits = list(evidence_by_question[qid])
        if q.get("audits") != expected_audits:
            raise RuntimeError(f"selected audit references mismatch for {qid}")
        if q.get("final_adjudication", {}).get("decision") != "KEEP":
            raise RuntimeError(f"missing KEEP adjudication for {qid}")

    if question_audit_hash(load_json(qpath("MA-Q-0190"))) != q0190_before:
        raise RuntimeError("unrelated Q0190 substantive content changed")

    report = {
        "report_type": "PRE_BATCH3_T1_GUARDED_ADMISSION_V2",
        "issue": 65,
        "date": TODAY,
        "source_branch": "repair/pre-batch3-legacy-salvage-t1-r1",
        "source_sha": SOURCE_SHA,
        "source_exact_head_qa_run": 32156260366,
        "admitted_count": len(ADMIT),
        "admitted_ids": sorted(ADMIT),
        "quarantined_id": QUARANTINED,
        "quarantined_hash": EXPECTED_Q0028_HASH,
        "evidence_partition": {
            "GPT-FRESH-COV-T1-B": sorted(B_IDS),
            "GPT-FRESH-COV-T1-D": sorted(D_IDS),
            "GPT-FRESH-COV-T1-H": sorted(H_IDS),
        },
        "question_hashes_before_and_after_equal": True,
        "current_hash_gate": "PASS",
        "dependency_snapshot_gate": "CAPTURED_FROM_EXACT_SOURCE_TREE",
        "preview": {
            "before_count": before_preview_count,
            "after_count": after_preview_count,
            "before_t1_ids": before_preview_t1,
            "after_t1_ids": after_preview_t1,
            "q0028_was_present_before": q0028_was_in_preview,
            "q0028_present_after": False,
        },
        "release_assertions": {
            "exactly_29_t1_released": True,
            "q0028_not_released": True,
            "q0028_not_previewed": True,
            "all_released_items_have_selected_current_hash_pass_evidence": True,
            "t1_substantive_hashes_unchanged": True,
            "q0190_substantive_hash_unchanged": True,
        },
    }
    report_path = ROOT / "audits" / "remediation" / TODAY / "PRE-BATCH3-T1-GUARDED-ADMISSION-V2-REPORT.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(report_path, report)

    print(f"T1 guarded admission preflight/mutation: PASS; released={len(released)}; preview {before_preview_count}->{after_preview_count}")
    print(f"Q0028 quarantined and removed from preview; prior T1 preview members={len(before_preview_t1)}, after={len(after_preview_t1)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
