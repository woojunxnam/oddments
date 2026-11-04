"""Guarded Pre-Batch3 T2 release of exactly MA-Q-0211..MA-Q-0226.

Issue #83 PHASE D, following the established T1 pattern (Issue #65 / PR #66).

The script refuses to mutate anything unless the Phase C preflight passes first, and
it re-asserts the release boundary afterwards: exactly the sixteen T2 questions move to
RELEASED, no audited substantive content changes, no unrelated question changes, no
registry semantics change, MA-Q-0028 stays quarantined and MA-Q-0190 stays untouched.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from preflight_prebatch3_t2_release import (
    A_LEGAL_AUDIT_ID,
    A_REALISM_AUDIT_ID,
    AUTHORIZING_ISSUE,
    B_LEGAL_AUDIT_ID,
    B_REALISM_AUDIT_ID,
    QUARANTINED_ID,
    Q0213,
    REPRESENTED_CANDIDATE_SHA,
    T2_IDS,
    TRANCHE_ID,
    UNCHANGED_IDS,
    audited_content,
)
from preflight_prebatch3_t2_release import run as run_preflight
from qa_common import DATA, ROOT, load_json, load_records, question_audit_hash, semantic_content_hash, write_json
from release_context import named_dependency_snapshot


RELEASE_DATE = "2026-08-19"
CONTROLLER_ISSUE = 83
UNTOUCHED_WITNESS_ID = "MA-Q-0190"

ADJUDICATOR = (
    "Claude Code release-governance controller under Issue #83 after independent "
    "GPT-FRESH-COV-T2-A and GPT-FRESH-COV-T2-B audits"
)
ADJUDICATION_NOTES = (
    "Pre-Batch3 Coverage T2 guarded admission under Issue #83, authorized as tranche "
    f"{TRANCHE_ID} by Issue #{AUTHORIZING_ISSUE}. Current-hash legal KEEP/YES and full-bank "
    "realism KEEP/PASS evidence was selected per question: the fifteen unchanged items use the "
    "deterministically normalized GPT-FRESH-COV-T2-A targeted-initial evidence, and the repaired "
    "MA-Q-0213 uses the fresh GPT-FRESH-COV-T2-B current-hash re-audit. The historical "
    "pre-repair MA-Q-0213 realism failure remains stored against its original content hash and "
    "was not converted to a pass. MA-Q-0028 remains quarantined and is not released or previewed."
)
# Selected legal-evidence dates, so last_legal_review reports the review that actually
# supports each item rather than a blanket release stamp.
LEGAL_REVIEW_DATES = {question_id: "2026-08-18" for question_id in UNCHANGED_IDS}
LEGAL_REVIEW_DATES[Q0213] = "2026-08-19"

PREVIEW_SOURCE_AUDITS = [A_LEGAL_AUDIT_ID, A_REALISM_AUDIT_ID, B_LEGAL_AUDIT_ID, B_REALISM_AUDIT_ID]
PREVIEW_NOTICE = (
    "Preview contains prior released questions plus the 29 Pre-Batch3 T1 legacy questions admitted "
    "under Issue #65 and the 16 Pre-Batch3 Coverage T2 questions MA-Q-0211 through MA-Q-0226 "
    "admitted under Issue #83 after current-hash independent legal and full-bank realism evidence. "
    "MA-Q-0028 is quarantined after a current-hash realism distinctness failure and is not shown."
)


def question_path(question_id: str) -> Path:
    return DATA / "questions" / f"{question_id.lower()}.json"


def snapshot_registries() -> dict:
    def semantic(directory: str, id_field: str, record_type: str) -> dict:
        return {
            record[id_field]: semantic_content_hash(record, record_type)
            for _, record in load_records(DATA / directory)
        }

    blueprint = load_json(DATA / "blueprint.json")
    style_profile = load_json(DATA / "exam_style" / "mpje_style_profile.json")
    return {
        "rules": semantic("rules", "rule_id", "rule"),
        "drugs": semantic("drugs", "drug_id", "drug"),
        "blueprint": semantic_content_hash(blueprint, "blueprint"),
        "style_profile": semantic_content_hash(style_profile, "style_profile"),
    }


def snapshot_questions() -> dict:
    return {
        record["question_id"]: {
            "audited_content_hash": question_audit_hash(record),
            "audited_content": audited_content(record),
            "verification_status": record.get("verification_status"),
            "lifecycle_status": record.get("lifecycle_status"),
            "independent_audit_status": record.get("independent_audit_status"),
            "duplicate_review_status": record.get("duplicate_review_status"),
            "final_adjudication": record.get("final_adjudication"),
            "audits": list(record.get("audits", [])),
            "development_fixture": record.get("development_fixture"),
        }
        for _, record in load_records(DATA / "questions")
    }


def release_question(question_id: str, evidence: dict, rules: dict, drugs: dict, context: dict) -> None:
    path = question_path(question_id)
    question = load_json(path)
    question["verification_status"] = "RELEASED"
    question["lifecycle_status"] = "RELEASED"
    question["last_legal_review"] = LEGAL_REVIEW_DATES[question_id]
    question["audits"] = [evidence["legal"], evidence["realism"]]
    question["duplicate_review_status"] = "CLEAR"
    question["independent_audit_status"] = "PASSED"
    question["final_adjudication"] = {
        "decision": "KEEP",
        "adjudicator": ADJUDICATOR,
        "date": RELEASE_DATE,
        "notes": ADJUDICATION_NOTES,
        "verified_dependencies": {
            "rules": {
                rule_id: {
                    "content_version": rules[rule_id].get("content_version"),
                    "content_hash": rules[rule_id].get("content_hash"),
                }
                for rule_id in question.get("rule_ids", [])
                if rule_id in rules
            },
            "drugs": {
                drug_id: {
                    "content_version": drugs[drug_id].get("content_version"),
                    "content_hash": drugs[drug_id].get("content_hash"),
                }
                for drug_id in question.get("drug_ids", [])
                if drug_id in drugs
            },
            "blueprint": context["blueprint"],
            "style_profile": context["style_profile"],
        },
    }
    # development_fixture keeps the established RELEASED convention: every canonical
    # question in this repository, released or not, stays a development fixture until
    # the bank leaves preview mode. PR #66 released 29 T1 questions the same way.
    question["development_fixture"] = True
    write_json(path, question)


def sync_family_matrix() -> dict:
    path = DATA / "exam_style" / "question_family_matrix.json"
    matrix = load_json(path)
    questions = [record for _, record in load_records(DATA / "questions")]
    candidate_counts: dict[str, int] = {}
    released_counts: dict[str, int] = {}
    for question in questions:
        family_id = question.get("family_id")
        candidate_counts[family_id] = candidate_counts.get(family_id, 0) + 1
        if question.get("verification_status") == "RELEASED" and question.get("lifecycle_status") == "RELEASED":
            released_counts[family_id] = released_counts.get(family_id, 0) + 1

    changed = {}
    for family in matrix["families"]:
        family_id = family["family_id"]
        candidate = candidate_counts.get(family_id, 0)
        released = released_counts.get(family_id, 0)
        if family["current_candidate_count"] != candidate or family["current_released_count"] != released:
            changed[family_id] = {
                "current_candidate_count": [family["current_candidate_count"], candidate],
                "current_released_count": [family["current_released_count"], released],
            }
        family["current_candidate_count"] = candidate
        family["current_released_count"] = released
    write_json(path, matrix)
    return changed


def sync_preview_allowlist() -> dict:
    path = ROOT / "site" / "generated" / "preview_allowlist.json"
    allowlist = load_json(path)
    before_ids = list(allowlist["question_ids"])
    before_audits = list(allowlist["source_audits"])

    after_ids = list(dict.fromkeys([*before_ids, *T2_IDS]))
    if QUARANTINED_ID in after_ids:
        raise SystemExit(f"{QUARANTINED_ID} must never re-enter the preview allowlist")
    after_audits = list(dict.fromkeys([*before_audits, *PREVIEW_SOURCE_AUDITS]))

    allowlist["generated_date"] = RELEASE_DATE
    allowlist["source_audits"] = after_audits
    allowlist["notice"] = PREVIEW_NOTICE
    allowlist["question_ids"] = after_ids
    write_json(path, allowlist)
    return {
        "before_count": len(before_ids),
        "after_count": len(after_ids),
        "added_ids": [question_id for question_id in after_ids if question_id not in before_ids],
        "removed_ids": [question_id for question_id in before_ids if question_id not in after_ids],
        "source_audits_before_count": len(before_audits),
        "source_audits_after_count": len(after_audits),
        "source_audits_added": [audit_id for audit_id in after_audits if audit_id not in before_audits],
        "source_audits_unique": len(after_audits) == len(set(after_audits)),
        "q0028_present_after": QUARANTINED_ID in after_ids,
    }


def assert_release_boundary(before_questions: dict, before_registries: dict) -> dict:
    after_questions = snapshot_questions()
    after_registries = snapshot_registries()
    failures: list[str] = []

    newly_released = sorted(
        question_id
        for question_id, after in after_questions.items()
        if after["verification_status"] == "RELEASED"
        and after["lifecycle_status"] == "RELEASED"
        and not (
            before_questions[question_id]["verification_status"] == "RELEASED"
            and before_questions[question_id]["lifecycle_status"] == "RELEASED"
        )
    )
    if newly_released != T2_IDS:
        failures.append(f"newly released set is {newly_released}, expected exactly MA-Q-0211..MA-Q-0226")

    for question_id in T2_IDS:
        before, after = before_questions[question_id], after_questions[question_id]
        if before["audited_content"] != after["audited_content"]:
            failures.append(f"{question_id}: audited substantive content changed during release")
        if before["audited_content_hash"] != after["audited_content_hash"]:
            failures.append(f"{question_id}: question_audit_hash changed during release")
        if after["independent_audit_status"] != "PASSED" or after["duplicate_review_status"] != "CLEAR":
            failures.append(f"{question_id}: release status summary fields were not set")
        if (after["final_adjudication"] or {}).get("decision") != "KEEP":
            failures.append(f"{question_id}: final adjudication is not KEEP")
        if after["development_fixture"] is not True:
            failures.append(f"{question_id}: development_fixture drifted from the RELEASED convention")

    for question_id, before in before_questions.items():
        after = after_questions[question_id]
        if before["audited_content"] != after["audited_content"]:
            if question_id not in T2_IDS:
                failures.append(f"{question_id}: unrelated question content changed")
        if question_id in T2_IDS:
            continue
        if before != after:
            failures.append(f"{question_id}: unrelated question release/adjudication state changed")

    if before_registries != after_registries:
        failures.append("rule/drug/blueprint/style semantic content changed during release")

    quarantined = after_questions[QUARANTINED_ID]
    if quarantined["verification_status"] == "RELEASED" or quarantined["lifecycle_status"] == "RELEASED":
        failures.append(f"{QUARANTINED_ID} quarantine was broken")
    allowlist = load_json(ROOT / "site" / "generated" / "preview_allowlist.json")
    if QUARANTINED_ID in allowlist["question_ids"]:
        failures.append(f"{QUARANTINED_ID} entered the public preview allowlist")

    witness = after_questions[UNTOUCHED_WITNESS_ID]
    if witness != before_questions[UNTOUCHED_WITNESS_ID]:
        failures.append(f"{UNTOUCHED_WITNESS_ID} content was modified")

    _, audits = _load_audits()
    historical = audits.get(A_REALISM_AUDIT_ID, {})
    historical_result = next(
        (item for item in historical.get("results", []) if item.get("Question_ID") == Q0213), {}
    )
    if historical_result.get("Realism_Verdict") != "FAIL" or historical_result.get("Verdict") != "MAJOR_REWRITE":
        failures.append("the historical MA-Q-0213 realism failure is no longer visible")

    return {
        "exactly_sixteen_t2_released": newly_released == T2_IDS,
        "newly_released_ids": newly_released,
        "t2_audited_content_unchanged": all(
            before_questions[question_id]["audited_content_hash"]
            == after_questions[question_id]["audited_content_hash"]
            for question_id in T2_IDS
        ),
        "no_unrelated_question_state_change": not any("unrelated question" in item for item in failures),
        "no_registry_semantic_mutation": before_registries == after_registries,
        "q0028_not_released": quarantined["verification_status"] != "RELEASED",
        "q0028_not_previewed": QUARANTINED_ID not in allowlist["question_ids"],
        "q0190_untouched": witness == before_questions[UNTOUCHED_WITNESS_ID],
        "historical_q0213_failure_visible": historical_result.get("Realism_Verdict") == "FAIL",
        "failures": failures,
    }


def _load_audits():
    from validate_audits import validate_audits

    return validate_audits()


def main() -> int:
    preflight, preflight_payload = run_preflight()
    if not preflight.ok:
        print("PREFLIGHT FAILED - no release mutation performed")
        for failure in preflight.failures:
            print(f"  {failure}")
        return 1
    print("preflight: PASS")

    before_questions = snapshot_questions()
    before_registries = snapshot_registries()
    blueprint = load_json(DATA / "blueprint.json")
    style_profile = load_json(DATA / "exam_style" / "mpje_style_profile.json")
    context = {
        "blueprint": named_dependency_snapshot(blueprint, "blueprint_id"),
        "style_profile": named_dependency_snapshot(style_profile, "profile_id"),
    }
    rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}
    drugs = {record["drug_id"]: record for _, record in load_records(DATA / "drugs")}

    evidence_partition = preflight_payload["evidence_partition"]
    for question_id in T2_IDS:
        release_question(question_id, evidence_partition[question_id], rules, drugs, context)
        print(f"released {question_id} <- {evidence_partition[question_id]}")

    family_changes = sync_family_matrix()
    preview = sync_preview_allowlist()
    boundary = assert_release_boundary(before_questions, before_registries)

    report = {
        "report_type": "PRE_BATCH3_T2_GUARDED_ADMISSION_V1",
        "controller_issue": CONTROLLER_ISSUE,
        "tranche_id": TRANCHE_ID,
        "authorizing_issue": AUTHORIZING_ISSUE,
        "date": RELEASE_DATE,
        "source_branch": "repair/pre-batch3-coverage-t2-r1",
        "source_sha": "bfc1be694053f84bf688126246131f16df1374d1",
        "represented_candidate_sha": REPRESENTED_CANDIDATE_SHA,
        "released_count": len(T2_IDS),
        "released_ids": T2_IDS,
        "quarantined_id": QUARANTINED_ID,
        "evidence_partition": {
            "GPT-FRESH-COV-T2-A": UNCHANGED_IDS,
            "GPT-FRESH-COV-T2-B": [Q0213],
        },
        "selected_audits": evidence_partition,
        "current_question_hashes": preflight_payload["current_question_hashes"],
        "q0213_hash_provenance": {
            "original_pre_repair_hash": preflight_payload["historical_q0213_failure"]["bound_hash"],
            "current_repaired_hash": preflight_payload["current_question_hashes"][Q0213],
            "historical_failure_audit": A_REALISM_AUDIT_ID,
            "current_pass_audits": [B_LEGAL_AUDIT_ID, B_REALISM_AUDIT_ID],
        },
        "question_hashes_before_and_after_equal": boundary["t2_audited_content_unchanged"],
        "current_hash_gate": "PASS",
        "dependency_snapshot_gate": "CAPTURED_FROM_EXACT_SOURCE_TREE",
        "family_matrix_changes": family_changes,
        "preview": preview,
        "release_assertions": {
            key: value for key, value in boundary.items() if key not in {"failures", "newly_released_ids"}
        },
        "release_boundary_failures": boundary["failures"],
        "preflight": preflight_payload["checks"],
    }
    output = ROOT / "audits" / "remediation" / "2026-08-19" / "PRE-BATCH3-T2-GUARDED-ADMISSION-V1-REPORT.json"
    write_json(output, report)

    print(json.dumps({key: report["release_assertions"][key] for key in report["release_assertions"]}, indent=2))
    print(f"preview: {preview['before_count']} -> {preview['after_count']}")
    print(f"report: {output.relative_to(ROOT).as_posix()}")
    if boundary["failures"]:
        for failure in boundary["failures"]:
            print(f"RELEASE BOUNDARY FAILURE: {failure}")
        return 1
    print("release boundary: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
