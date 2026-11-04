"""Reusable fail-closed guarded release for an audited tranche.

Generalizes the pattern established for Pre-Batch3 T1 (Issue #65 / PR #66) and T2
(Issue #83 / PR #84) so later tranches do not re-implement release governance. A tranche
is described once in TRANCHES; everything else — preflight, mutation, family/preview
synchronization and release-boundary assertions — is shared.

The script refuses to mutate anything unless every preflight check passes, and it
re-asserts the boundary afterwards: exactly the tranche's questions move to RELEASED, no
audited substantive content changes, no unrelated question or registry record changes,
MA-Q-0028 stays quarantined and MA-Q-0190 stays untouched.

    python scripts/guarded_release.py --tranche PRE-BATCH3-COVERAGE-T3-DIVERSITY
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import (
    BLOCKED_RULE_STATUSES,
    DATA,
    ROOT,
    QUESTION_AUDIT_FIELDS,
    VERIFIED_DRUG_STATUSES,
    VERIFIED_RULE_STATUSES,
    load_json,
    load_records,
    question_audit_hash,
    semantic_content_hash,
    write_json,
)
from release_context import named_dependency_snapshot, style_profile_snapshot
from validate_audits import is_valid_targeted_initial_audit, validate_audits


QUARANTINED_ID = "MA-Q-0028"
UNTOUCHED_WITNESS_ID = "MA-Q-0190"

TRANCHES = {
    "PRE-BATCH3-COVERAGE-T3-DIVERSITY": {
        "report_type": "PRE_BATCH3_T3_GUARDED_ADMISSION_V1",
        "controller_issue": 83,
        "authorizing_issue": 86,
        "release_date": "2026-08-19",
        "source_branch": "remediation/pre-batch3-coverage-t3-diversity",
        "represented_candidate_sha": "f13c91c2635ea153a1ea19d9dfb34bcbe12f30c2",
        "question_ids": ["MA-Q-0227", "MA-Q-0228"],
        "expected_hashes": {
            "MA-Q-0227": "e4366cb456fcb126e4a96988320d32dcf0258d432acb1df73ecca7bee3c2065e",
            "MA-Q-0228": "bb334d740968d63ec5861ef1713adf672383bf572715daac0eec90f4cf8bead3",
        },
        "evidence": {
            "MA-Q-0227": {
                "legal": "AUDIT-CLAUDE-FRESH-COV-T3-A-LEGAL-TARGETED-INITIAL-2026-08-19",
                "realism": "AUDIT-CLAUDE-FRESH-COV-T3-A-REALISM-TARGETED-INITIAL-2026-08-19",
            },
            "MA-Q-0228": {
                "legal": "AUDIT-CLAUDE-FRESH-COV-T3-A-LEGAL-TARGETED-INITIAL-2026-08-19",
                "realism": "AUDIT-CLAUDE-FRESH-COV-T3-A-REALISM-TARGETED-INITIAL-2026-08-19",
            },
        },
        "legal_review_dates": {"MA-Q-0227": "2026-08-19", "MA-Q-0228": "2026-08-19"},
        "adjudicator": (
            "Claude Code release-governance controller under Issue #86 after the independent "
            "CLAUDE-FRESH-COV-T3-A blind-locked legal and full-bank realism audit"
        ),
        "adjudication_notes": (
            "Pre-Batch3 Coverage T3 diversity guarded admission under Issue #86, authorized as tranche "
            "PRE-BATCH3-COVERAGE-T3-DIVERSITY. These two items close the only two deficits left by the "
            "post-T2 Pre-Batch3 gate: headline 4.3 and headline 4.6 each rested on a single scenario "
            "family. Release rests on current-hash independent evidence from CLAUDE-FRESH-COV-T3-A, whose "
            "Phase-1 blind lock was committed before any canonical key access and whose blind answers "
            "matched both canonical keys. MA-Q-0028 remains quarantined and is not released or previewed."
        ),
        "preview_source_audits": [
            "AUDIT-CLAUDE-FRESH-COV-T3-A-LEGAL-TARGETED-INITIAL-2026-08-19",
            "AUDIT-CLAUDE-FRESH-COV-T3-A-REALISM-TARGETED-INITIAL-2026-08-19",
        ],
        "preview_notice": (
            "Preview contains prior released questions plus the 29 Pre-Batch3 T1 legacy questions admitted "
            "under Issue #65, the 16 Pre-Batch3 Coverage T2 questions MA-Q-0211 through MA-Q-0226 admitted "
            "under Issue #83, and the 2 Pre-Batch3 T3 diversity questions MA-Q-0227 and MA-Q-0228 admitted "
            "under Issue #86, each after current-hash independent legal and full-bank realism evidence. "
            "MA-Q-0028 is quarantined after a current-hash realism distinctness failure and is not shown."
        ),
        "report_path": "audits/remediation/2026-08-19/PRE-BATCH3-T3-GUARDED-ADMISSION-V1-REPORT.json",
        "preflight_path": "audits/remediation/2026-08-19/PRE-BATCH3-T3-GUARDED-RELEASE-PREFLIGHT.json",
    }
}


def audited_content(question: dict) -> dict:
    return {field: question.get(field) for field in QUESTION_AUDIT_FIELDS}


def result_for(audit: dict, question_id: str) -> dict | None:
    return next((item for item in audit.get("results", []) if item.get("Question_ID") == question_id), None)


class Preflight:
    def __init__(self) -> None:
        self.checks: dict[str, dict] = {}
        self.failures: list[str] = []

    def __call__(self, key: str, ok: bool, detail: object = None) -> bool:
        self.checks[key] = {"status": "PASS" if ok else "FAIL", "detail": detail}
        if not ok:
            self.failures.append(f"{key}: {detail}")
        return ok

    @property
    def ok(self) -> bool:
        return not self.failures


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


def snapshot_registries() -> dict:
    blueprint = load_json(DATA / "blueprint.json")
    style_profile = load_json(DATA / "exam_style" / "mpje_style_profile.json")
    return {
        "rules": {r["rule_id"]: semantic_content_hash(r, "rule") for _, r in load_records(DATA / "rules")},
        "drugs": {d["drug_id"]: semantic_content_hash(d, "drug") for _, d in load_records(DATA / "drugs")},
        "blueprint": semantic_content_hash(blueprint, "blueprint"),
        "style_profile": semantic_content_hash(style_profile, "style_profile"),
    }


def preflight(config: dict) -> tuple[Preflight, dict]:
    pre = Preflight()
    question_ids = config["question_ids"]
    questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}
    rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}
    drugs = {record["drug_id"]: record for _, record in load_records(DATA / "drugs")}
    blueprint = load_json(DATA / "blueprint.json")
    style_profile = load_json(DATA / "exam_style" / "mpje_style_profile.json")
    _, audits = validate_audits()

    current = {question_id: question_audit_hash(questions[question_id]) for question_id in question_ids}
    pre("01_recomputed_current_hashes", current == config["expected_hashes"], current)

    already_released = [
        question_id
        for question_id in question_ids
        if questions[question_id].get("verification_status") == "RELEASED"
    ]
    pre("02_not_already_released", not already_released, already_released or "all candidates are unreleased")

    problems: list[str] = []
    for question_id in question_ids:
        evidence = config["evidence"][question_id]
        for audit_id, review_type in ((evidence["legal"], "LEGAL_VERIFICATION"), (evidence["realism"], "REALISM_REVIEW")):
            audit = audits.get(audit_id)
            if audit is None:
                problems.append(f"{question_id}: audit {audit_id} is not registered")
                continue
            if audit.get("review_type") != review_type:
                problems.append(f"{question_id}: {audit_id} is not a {review_type}")
            if audit.get("independent") is not True or audit.get("audit_status") != "FULLY_ADJUDICATED":
                problems.append(f"{question_id}: {audit_id} is not independent/fully adjudicated")
            if audit.get("question_hashes", {}).get(question_id) != current[question_id]:
                problems.append(f"{question_id}: {audit_id} is not bound to the current hash")
                continue
            result = result_for(audit, question_id)
            if result is None:
                problems.append(f"{question_id}: {audit_id} has no result row")
                continue
            if review_type == "LEGAL_VERIFICATION":
                if result.get("Verdict") != "KEEP" or result.get("Existing_Answer_Correct") != "YES":
                    problems.append(f"{question_id}: {audit_id} legal evidence is not KEEP/YES")
            else:
                if result.get("Verdict") != "KEEP" or result.get("Realism_Verdict") != "PASS":
                    problems.append(f"{question_id}: {audit_id} realism evidence is not KEEP/PASS")
                if not all(result.get("Criteria", {}).values()):
                    problems.append(f"{question_id}: {audit_id} realism criteria are not all true")
                if audit.get("style_profile") != style_profile_snapshot(style_profile):
                    problems.append(f"{question_id}: {audit_id} uses a stale style profile")
    pre("03_current_hash_legal_and_realism_evidence", not problems, problems or config["evidence"])

    history = {
        question_id: sorted(
            audit_id
            for audit_id, audit in audits.items()
            if (audit.get("audit_scope") == "INITIAL_BATCH" or is_valid_targeted_initial_audit(audit))
            and audit.get("review_type") == "LEGAL_VERIFICATION"
            and audit.get("independent")
            and audit.get("audit_status") == "FULLY_ADJUDICATED"
            and question_id in audit.get("question_ids", [])
            and result_for(audit, question_id) is not None
        )
        for question_id in question_ids
    }
    pre("04_valid_initial_audit_history", all(history.values()), history)

    dependency_problems: list[str] = []
    dependency_snapshots: dict[str, dict] = {}
    for question_id in question_ids:
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
    pre("05_dependency_verification", not dependency_problems, dependency_problems or dependency_snapshots)

    current_hash_failures: list[dict] = []
    for question_id in question_ids:
        for audit_id, audit in sorted(audits.items()):
            if not audit.get("independent") or audit.get("audit_status") != "FULLY_ADJUDICATED":
                continue
            if audit.get("question_hashes", {}).get(question_id) != current[question_id]:
                continue
            result = result_for(audit, question_id)
            if result is None:
                continue
            if audit.get("review_type") == "LEGAL_VERIFICATION":
                if result.get("Verdict") != "KEEP" or result.get("Existing_Answer_Correct") != "YES":
                    current_hash_failures.append({"question_id": question_id, "audit_id": audit_id})
            elif audit.get("review_type") == "REALISM_REVIEW":
                if audit.get("style_profile") != style_profile_snapshot(style_profile):
                    continue
                if result.get("Verdict") != "KEEP" or result.get("Realism_Verdict") != "PASS":
                    current_hash_failures.append({"question_id": question_id, "audit_id": audit_id})
    pre("06_no_current_hash_failure", not current_hash_failures, current_hash_failures or "none")

    allowlist = load_json(ROOT / "site" / "generated" / "preview_allowlist.json")
    quarantined = questions[QUARANTINED_ID]
    pre(
        "07_quarantine_intact",
        quarantined.get("verification_status") != "RELEASED"
        and quarantined.get("lifecycle_status") != "RELEASED"
        and QUARANTINED_ID not in allowlist.get("question_ids", []),
        {
            "verification_status": quarantined.get("verification_status"),
            "in_preview": QUARANTINED_ID in allowlist.get("question_ids", []),
        },
    )

    released_before = sorted(
        question_id
        for question_id, question in questions.items()
        if question.get("verification_status") == "RELEASED" and question.get("lifecycle_status") == "RELEASED"
    )
    preview_before = list(allowlist.get("question_ids", []))
    pre(
        "08_preview_captured_before_mutation",
        len(preview_before) == len(set(preview_before)),
        {
            "preview_before_count": len(preview_before),
            "released_before_count": len(released_before),
            "tranche_in_preview_before": sorted(set(preview_before) & set(question_ids)),
        },
    )

    payload = {
        "report_type": f"{config['report_type']}_PREFLIGHT",
        "tranche_id": config.get("tranche_id"),
        "authorizing_issue": config["authorizing_issue"],
        "question_ids": question_ids,
        "status": "PASS" if pre.ok else "FAIL",
        "current_question_hashes": current,
        "evidence": config["evidence"],
        "dependency_snapshots": dependency_snapshots,
        "release_context": {
            "blueprint": named_dependency_snapshot(blueprint, "blueprint_id"),
            "style_profile": named_dependency_snapshot(style_profile, "profile_id"),
        },
        "preview_before_count": len(preview_before),
        "released_before_count": len(released_before),
        "checks": pre.checks,
        "failures": pre.failures,
    }
    return pre, payload


def release_question(question_id: str, config: dict, rules: dict, drugs: dict, context: dict) -> None:
    path = DATA / "questions" / f"{question_id.lower()}.json"
    question = load_json(path)
    evidence = config["evidence"][question_id]
    question["verification_status"] = "RELEASED"
    question["lifecycle_status"] = "RELEASED"
    question["last_legal_review"] = config["legal_review_dates"][question_id]
    question["audits"] = [evidence["legal"], evidence["realism"]]
    question["duplicate_review_status"] = "CLEAR"
    question["independent_audit_status"] = "PASSED"
    question["final_adjudication"] = {
        "decision": "KEEP",
        "adjudicator": config["adjudicator"],
        "date": config["release_date"],
        "notes": config["adjudication_notes"],
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


def sync_preview_allowlist(config: dict) -> dict:
    path = ROOT / "site" / "generated" / "preview_allowlist.json"
    allowlist = load_json(path)
    before_ids = list(allowlist["question_ids"])
    before_audits = list(allowlist["source_audits"])
    after_ids = list(dict.fromkeys([*before_ids, *config["question_ids"]]))
    if QUARANTINED_ID in after_ids:
        raise SystemExit(f"{QUARANTINED_ID} must never re-enter the preview allowlist")
    after_audits = list(dict.fromkeys([*before_audits, *config["preview_source_audits"]]))
    allowlist["generated_date"] = config["release_date"]
    allowlist["source_audits"] = after_audits
    allowlist["notice"] = config["preview_notice"]
    allowlist["question_ids"] = after_ids
    write_json(path, allowlist)
    return {
        "before_count": len(before_ids),
        "after_count": len(after_ids),
        "added_ids": [q for q in after_ids if q not in before_ids],
        "removed_ids": [q for q in before_ids if q not in after_ids],
        "source_audits_added": [a for a in after_audits if a not in before_audits],
        "source_audits_unique": len(after_audits) == len(set(after_audits)),
        "q0028_present_after": QUARANTINED_ID in after_ids,
    }


def assert_release_boundary(config: dict, before_questions: dict, before_registries: dict) -> dict:
    question_ids = config["question_ids"]
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
    if newly_released != sorted(question_ids):
        failures.append(f"newly released set is {newly_released}, expected exactly {sorted(question_ids)}")

    for question_id in question_ids:
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
        if question_id in question_ids:
            continue
        if before != after_questions[question_id]:
            failures.append(f"{question_id}: unrelated question state changed")

    if before_registries != after_registries:
        failures.append("rule/drug/blueprint/style semantic content changed during release")

    quarantined = after_questions[QUARANTINED_ID]
    allowlist = load_json(ROOT / "site" / "generated" / "preview_allowlist.json")
    if quarantined["verification_status"] == "RELEASED" or QUARANTINED_ID in allowlist["question_ids"]:
        failures.append(f"{QUARANTINED_ID} quarantine was broken")
    if after_questions[UNTOUCHED_WITNESS_ID] != before_questions[UNTOUCHED_WITNESS_ID]:
        failures.append(f"{UNTOUCHED_WITNESS_ID} content was modified")

    return {
        "exactly_tranche_released": newly_released == sorted(question_ids),
        "newly_released_ids": newly_released,
        "audited_content_unchanged": all(
            before_questions[q]["audited_content_hash"] == after_questions[q]["audited_content_hash"]
            for q in question_ids
        ),
        "no_unrelated_question_state_change": not any("unrelated question" in item for item in failures),
        "no_registry_semantic_mutation": before_registries == after_registries,
        "q0028_not_released": quarantined["verification_status"] != "RELEASED",
        "q0028_not_previewed": QUARANTINED_ID not in allowlist["question_ids"],
        "q0190_untouched": after_questions[UNTOUCHED_WITNESS_ID] == before_questions[UNTOUCHED_WITNESS_ID],
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--tranche", choices=sorted(TRANCHES), help="a tranche registered in TRANCHES")
    group.add_argument("--tranche-file", help="path to a tranche config JSON, for large generated tranches")
    args = parser.parse_args()
    if args.tranche:
        config = {"tranche_id": args.tranche, **TRANCHES[args.tranche]}
    else:
        config = load_json(ROOT / args.tranche_file if not Path(args.tranche_file).is_absolute() else Path(args.tranche_file))
        required = {"tranche_id", "question_ids", "expected_hashes", "evidence", "legal_review_dates",
                    "adjudicator", "adjudication_notes", "preview_source_audits", "preview_notice",
                    "report_path", "preflight_path", "report_type", "controller_issue",
                    "authorizing_issue", "release_date", "source_branch", "represented_candidate_sha"}
            
        missing = required - set(config)
        if missing:
            raise SystemExit(f"tranche config is missing required keys: {sorted(missing)}")

    pre, preflight_payload = preflight(config)
    write_json(ROOT / config["preflight_path"], preflight_payload)
    for key, value in preflight_payload["checks"].items():
        print(f"[{value['status']}] {key}")
    if not pre.ok:
        print("PREFLIGHT FAILED - no release mutation performed")
        for failure in pre.failures:
            print(f"  {failure}")
        return 1

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

    for question_id in config["question_ids"]:
        release_question(question_id, config, rules, drugs, context)
        print(f"released {question_id} <- {config['evidence'][question_id]}")

    family_changes = sync_family_matrix()
    preview = sync_preview_allowlist(config)
    boundary = assert_release_boundary(config, before_questions, before_registries)

    report = {
        "report_type": config["report_type"],
        # Must come from the resolved config, not args.tranche: a --tranche-file run leaves
        # args.tranche None and would otherwise write a null tranche_id into the release report.
        "tranche_id": config["tranche_id"],
        "controller_issue": config["controller_issue"],
        "authorizing_issue": config["authorizing_issue"],
        "date": config["release_date"],
        "source_branch": config["source_branch"],
        "represented_candidate_sha": config["represented_candidate_sha"],
        "released_count": len(config["question_ids"]),
        "released_ids": config["question_ids"],
        "evidence": config["evidence"],
        "current_question_hashes": preflight_payload["current_question_hashes"],
        "question_hashes_before_and_after_equal": boundary["audited_content_unchanged"],
        "current_hash_gate": "PASS",
        "family_matrix_changes": family_changes,
        "preview": preview,
        "release_assertions": {k: v for k, v in boundary.items() if k not in {"failures", "newly_released_ids"}},
        "release_boundary_failures": boundary["failures"],
        "preflight": preflight_payload["checks"],
    }
    write_json(ROOT / config["report_path"], report)
    print(json.dumps(report["release_assertions"], indent=2))
    print(f"preview: {preview['before_count']} -> {preview['after_count']}")
    print(f"report: {config['report_path']}")
    if boundary["failures"]:
        for failure in boundary["failures"]:
            print(f"RELEASE BOUNDARY FAILURE: {failure}")
        return 1
    print("release boundary: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
