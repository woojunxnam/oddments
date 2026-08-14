from __future__ import annotations

from datetime import date

from qa_common import DATA, ROOT, dependency_snapshot, load_json, load_records, write_json
from release_context import named_dependency_snapshot

TODAY = date(2026, 8, 14).isoformat()

CURRENT_A_LEGAL = "AUDIT-GPT-FRESH-EXP1-V2-A-LEGAL-REAUDIT-2026-08-14"
CURRENT_A_REALISM = "AUDIT-GPT-FRESH-EXP1-V2-A-REALISM-REAUDIT-2026-08-14"
CURRENT_B_LEGAL = "AUDIT-GPT-FRESH-EXP1-V2-B-LEGAL-2026-08-14"

INITIAL_GPT_LEGAL = "AUDIT-GPT-EXP1-LEGAL-INITIAL-2026-08-14"
INITIAL_DESKTOP_LEGAL = "AUDIT-GPT-DESKTOP-EXP1-LEGAL-INITIAL-2026-08-14"
INITIAL_DESKTOP_REALISM = "AUDIT-GPT-DESKTOP-EXP1-REALISM-INITIAL-2026-08-14"

WAVE1_CURRENT = {
    "MA-Q-0092",
    "MA-Q-0095",
    "MA-Q-0096",
    "MA-Q-0115",
    "MA-Q-0118",
    "MA-Q-0119",
    "MA-Q-0120",
    "MA-Q-0122",
    "MA-Q-0123",
    "MA-Q-0124",
}
WAVE1_UNCHANGED = {"MA-Q-0130"}
WAVE1 = WAVE1_CURRENT | WAVE1_UNCHANGED


def main() -> int:
    rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}
    drugs = {record["drug_id"]: record for _, record in load_records(DATA / "drugs")}
    blueprint = load_json(DATA / "blueprint.json")
    style_profile = load_json(DATA / "exam_style" / "mpje_style_profile.json")

    for qid in sorted(WAVE1):
        path = DATA / "questions" / f"ma-q-{qid[-4:]}.json"
        question = load_json(path)
        if question.get("question_id") != qid:
            raise RuntimeError(f"question ID mismatch at {path}")

        if qid in WAVE1_CURRENT:
            question["audits"] = [CURRENT_A_LEGAL, CURRENT_A_REALISM, CURRENT_B_LEGAL]
        else:
            question["audits"] = [INITIAL_GPT_LEGAL, INITIAL_DESKTOP_LEGAL, INITIAL_DESKTOP_REALISM]

        question["verification_status"] = "RELEASED"
        question["lifecycle_status"] = "RELEASED"
        question["last_legal_review"] = TODAY
        question["duplicate_review_status"] = "CLEAR"
        question["independent_audit_status"] = "PASSED"
        question["final_adjudication"] = {
            "decision": "KEEP",
            "adjudicator": "GPT-5.6-Sol editor after independent audit A/B",
            "date": TODAY,
            "notes": (
                "Wave 1 admission after current-hash legal and realism gates. "
                "MA-Q-0130 remained unchanged from the independently audited INITIAL_BATCH content."
                if qid == "MA-Q-0130"
                else "Wave 1 admission after independent current-hash legal A/B KEEP/YES and realism A KEEP/PASS."
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

    allowlist_path = ROOT / "site" / "generated" / "preview_allowlist.json"
    allowlist = load_json(allowlist_path)
    ids = list(allowlist.get("question_ids", []))
    for qid in sorted(WAVE1):
        if qid not in ids:
            ids.append(qid)
    allowlist["generated_date"] = TODAY
    allowlist["source_audits"] = list(dict.fromkeys(
        list(allowlist.get("source_audits", []))
        + [CURRENT_A_LEGAL, CURRENT_A_REALISM, CURRENT_B_LEGAL,
           INITIAL_GPT_LEGAL, INITIAL_DESKTOP_LEGAL, INITIAL_DESKTOP_REALISM]
    ))
    allowlist["notice"] = (
        "Preview contains the prior Phase 2 audited set plus Batch 1 Wave 1 questions that passed the repository's "
        "current legal/realism admission gates. Remaining Batch 1 questions stay quarantined and are not shown."
    )
    allowlist["question_ids"] = ids
    write_json(allowlist_path, allowlist)

    if len(ids) != 58:
        raise RuntimeError(f"expected 58 preview questions after Wave 1, found {len(ids)}")

    print("admitted Batch 1 Wave 1: 11 RELEASED questions; preview allowlist now 58")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
