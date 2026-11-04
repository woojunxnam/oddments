from __future__ import annotations

from collections import Counter
from datetime import date

from qa_common import (
    DATA,
    ROOT,
    dependency_snapshot,
    load_json,
    load_records,
    question_audit_hash,
    write_json,
)
from release_context import named_dependency_snapshot

TODAY = date(2026, 8, 14).isoformat()

LEGAL_AUDIT_ID = "AUDIT-GPT-FRESH-EXP1-V3-A-LEGAL-REAUDIT-2026-08-14"
REALISM_AUDIT_ID = "AUDIT-GPT-FRESH-EXP1-V3-A-REALISM-REAUDIT-2026-08-14"
AUDITOR_INSTANCE = "GPT-FRESH-EXP1-V3-A"

WAVE2 = {
    "MA-Q-0091",
    "MA-Q-0093",
    "MA-Q-0094",
    "MA-Q-0097",
    "MA-Q-0099",
    "MA-Q-0100",
    "MA-Q-0101",
    "MA-Q-0102",
    "MA-Q-0103",
    "MA-Q-0104",
    "MA-Q-0105",
    "MA-Q-0106",
    "MA-Q-0107",
    "MA-Q-0108",
    "MA-Q-0109",
    "MA-Q-0111",
    "MA-Q-0112",
    "MA-Q-0113",
    "MA-Q-0114",
    "MA-Q-0116",
    "MA-Q-0117",
    "MA-Q-0121",
    "MA-Q-0125",
    "MA-Q-0126",
    "MA-Q-0127",
    "MA-Q-0128",
    "MA-Q-0129",
}
QUARANTINED = {"MA-Q-0098", "MA-Q-0110"}
FULL_V3_SCOPE = WAVE2 | QUARANTINED


def result_index(audit: dict) -> dict[str, dict]:
    return {item["Question_ID"]: item for item in audit.get("results", [])}


def sync_family_release_counts() -> None:
    released_counts: Counter[str] = Counter()
    for _, question in load_records(DATA / "questions"):
        if (
            question.get("verification_status") == "RELEASED"
            and question.get("lifecycle_status") == "RELEASED"
        ):
            released_counts[question["family_id"]] += 1

    matrix_path = DATA / "exam_style" / "question_family_matrix.json"
    matrix = load_json(matrix_path)
    for family in matrix.get("families", []):
        family["current_released_count"] = released_counts.get(family["family_id"], 0)
    matrix["last_reviewed"] = TODAY
    write_json(matrix_path, matrix)


def main() -> int:
    if len(WAVE2) != 27 or len(FULL_V3_SCOPE) != 29:
        raise RuntimeError("unexpected Wave 2 scope size")

    legal = load_json(DATA / "audits" / f"{LEGAL_AUDIT_ID}.json")
    realism = load_json(DATA / "audits" / f"{REALISM_AUDIT_ID}.json")

    for audit, review_type in ((legal, "LEGAL_VERIFICATION"), (realism, "REALISM_REVIEW")):
        if audit.get("audit_status") != "FULLY_ADJUDICATED":
            raise RuntimeError(f"{audit.get('audit_id')} is not fully adjudicated")
        if not audit.get("independent"):
            raise RuntimeError(f"{audit.get('audit_id')} is not independent")
        if audit.get("auditor_instance") != AUDITOR_INSTANCE:
            raise RuntimeError(f"unexpected auditor instance in {audit.get('audit_id')}")
        if audit.get("review_type") != review_type:
            raise RuntimeError(f"unexpected review type in {audit.get('audit_id')}")
        if set(audit.get("question_ids", [])) != FULL_V3_SCOPE:
            raise RuntimeError(f"unexpected question scope in {audit.get('audit_id')}")
        if set(audit.get("question_hashes", {})) != FULL_V3_SCOPE:
            raise RuntimeError(f"unexpected hash scope in {audit.get('audit_id')}")

    legal_results = result_index(legal)
    realism_results = result_index(realism)
    if set(legal_results) != FULL_V3_SCOPE or set(realism_results) != FULL_V3_SCOPE:
        raise RuntimeError("audit result scope mismatch")

    rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}
    drugs = {record["drug_id"]: record for _, record in load_records(DATA / "drugs")}
    blueprint = load_json(DATA / "blueprint.json")
    style_profile = load_json(DATA / "exam_style" / "mpje_style_profile.json")

    # Verify every audited hash before any release-state mutation.
    for qid in sorted(FULL_V3_SCOPE):
        path = DATA / "questions" / f"ma-q-{qid[-4:]}.json"
        question = load_json(path)
        if question.get("question_id") != qid:
            raise RuntimeError(f"question ID mismatch at {path}")
        actual_hash = question_audit_hash(question)
        if legal["question_hashes"][qid] != actual_hash:
            raise RuntimeError(f"stale legal audit hash for {qid}")
        if realism["question_hashes"][qid] != actual_hash:
            raise RuntimeError(f"stale realism audit hash for {qid}")

    # The two realism failures must remain quarantined rather than being silently ignored.
    for qid in QUARANTINED:
        if legal_results[qid].get("Verdict") != "KEEP" or legal_results[qid].get("Existing_Answer_Correct") != "YES":
            raise RuntimeError(f"unexpected legal disposition for quarantined {qid}")
        if realism_results[qid].get("Verdict") == "KEEP" or realism_results[qid].get("Realism_Verdict") == "PASS":
            raise RuntimeError(f"expected realism failure for quarantined {qid}")
        question = load_json(DATA / "questions" / f"ma-q-{qid[-4:]}.json")
        if question.get("verification_status") == "RELEASED" or question.get("lifecycle_status") == "RELEASED":
            raise RuntimeError(f"quarantined question already released: {qid}")

    for qid in sorted(WAVE2):
        if legal_results[qid].get("Verdict") != "KEEP" or legal_results[qid].get("Existing_Answer_Correct") != "YES":
            raise RuntimeError(f"legal release gate failed for {qid}")
        if realism_results[qid].get("Verdict") != "KEEP" or realism_results[qid].get("Realism_Verdict") != "PASS":
            raise RuntimeError(f"realism release gate failed for {qid}")

        path = DATA / "questions" / f"ma-q-{qid[-4:]}.json"
        question = load_json(path)
        question["audits"] = [LEGAL_AUDIT_ID, REALISM_AUDIT_ID]
        question["verification_status"] = "RELEASED"
        question["lifecycle_status"] = "RELEASED"
        question["last_legal_review"] = TODAY
        question["duplicate_review_status"] = "CLEAR"
        question["independent_audit_status"] = "PASSED"
        question["final_adjudication"] = {
            "decision": "KEEP",
            "adjudicator": "GPT-5.6-Sol editor after independent Issue #27 audit",
            "date": TODAY,
            "notes": (
                "Wave 2 admission after one fresh independent auditor completed current-hash legal "
                "KEEP/YES and realism KEEP/PASS under the single-auditor release policy."
            ),
            "verified_dependencies": {
                "rules": {
                    rule_id: dependency_snapshot(rules[rule_id])
                    for rule_id in question.get("rule_ids", [])
                },
                "drugs": {
                    drug_id: dependency_snapshot(drugs[drug_id])
                    for drug_id in question.get("drug_ids", [])
                },
                "blueprint": named_dependency_snapshot(blueprint, "blueprint_id"),
                "style_profile": named_dependency_snapshot(style_profile, "profile_id"),
            },
        }
        write_json(path, question)

    sync_family_release_counts()

    allowlist_path = ROOT / "site" / "generated" / "preview_allowlist.json"
    allowlist = load_json(allowlist_path)
    ids = list(allowlist.get("question_ids", []))
    if len(ids) != 58:
        raise RuntimeError(f"expected pre-Wave-2 preview count 58, found {len(ids)}")
    if any(qid in ids for qid in QUARANTINED):
        raise RuntimeError("quarantined question unexpectedly present in preview before Wave 2")
    for qid in sorted(WAVE2):
        if qid not in ids:
            ids.append(qid)
    if any(qid in ids for qid in QUARANTINED):
        raise RuntimeError("quarantined question leaked into preview")

    allowlist["generated_date"] = TODAY
    allowlist["source_audits"] = list(
        dict.fromkeys(list(allowlist.get("source_audits", [])) + [LEGAL_AUDIT_ID, REALISM_AUDIT_ID])
    )
    allowlist["notice"] = (
        "Preview contains the prior audited set plus Batch 1 Waves 1-2 questions that passed the repository's "
        "current legal and realism admission gates. MA-Q-0098 and MA-Q-0110 remain quarantined and are not shown."
    )
    allowlist["question_ids"] = ids
    write_json(allowlist_path, allowlist)

    if len(ids) != 85:
        raise RuntimeError(f"expected 85 preview questions after Wave 2, found {len(ids)}")

    released_batch1 = 0
    for number in range(91, 131):
        question = load_json(DATA / "questions" / f"ma-q-{number:04d}.json")
        if question.get("verification_status") == "RELEASED" and question.get("lifecycle_status") == "RELEASED":
            released_batch1 += 1
    if released_batch1 != 38:
        raise RuntimeError(f"expected 38 released Batch 1 questions, found {released_batch1}")

    print("admitted Batch 1 Wave 2: 27 RELEASED questions; preview allowlist now 85; Q0098/Q0110 quarantined")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
