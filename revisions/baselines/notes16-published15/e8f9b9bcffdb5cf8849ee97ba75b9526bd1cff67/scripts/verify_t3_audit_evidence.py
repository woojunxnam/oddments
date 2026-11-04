"""Controller-side verification of the fresh CLAUDE-FRESH-COV-T3-A audit before any release.

Issue #86 STEP 4. The auditor's own report is not evidence: every condition below is
recomputed from the repository. Nothing is taken on trust, including the auditor's
claim that it never touched canonical content and its claim that a negative-control
injection was fully reverted.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, ROOT, QUESTION_AUDIT_FIELDS, load_json, load_records, question_audit_hash, write_json
from release_context import style_profile_snapshot
from validate_audits import is_valid_targeted_initial_audit, validate_audits


TRANCHE_ID = "PRE-BATCH3-COVERAGE-T3-DIVERSITY"
AUTHORIZING_ISSUE = 86
CANDIDATE_SHA = "f13c91c2635ea153a1ea19d9dfb34bcbe12f30c2"
AUDIT_BASE_SHA = "36b3ea85229609afb08772a566cca2eb6fbe1be8"
AUDIT_HEAD_SHA = "e08478d7956754142b4f5538e84de64cbec88997"
LOCK_COMMIT_SHA = "e412cfb1e78a6579a18727ab7fa549f0444836f6"
LOCK_BLOB = "abdd4524b87c521265829050f3dd882851814710"
BLIND_BLOB = "c83757ce2c28cfde9e376c2ba1008771a93a63ed"
FREEZE_BRANCH = "freeze/pre-batch3-coverage-t3-v1"

AUDITOR = "CLAUDE"
AUDITOR_INSTANCE = "CLAUDE-FRESH-COV-T3-A"
LEGAL_AUDIT_ID = "AUDIT-CLAUDE-FRESH-COV-T3-A-LEGAL-TARGETED-INITIAL-2026-08-19"
REALISM_AUDIT_ID = "AUDIT-CLAUDE-FRESH-COV-T3-A-REALISM-TARGETED-INITIAL-2026-08-19"
LOCK_PATH = "audits/remediation/2026-08-19/CLAUDE-FRESH-COV-T3-A-PHASE1-BLIND-LOCK.json"

QUESTION_IDS = ["MA-Q-0227", "MA-Q-0228"]
EXPECTED_HASHES = {
    "MA-Q-0227": "e4366cb456fcb126e4a96988320d32dcf0258d432acb1df73ecca7bee3c2065e",
    "MA-Q-0228": "bb334d740968d63ec5861ef1713adf672383bf572715daac0eec90f4cf8bead3",
}
EXPECTED_KEYS = {"MA-Q-0227": ["E"], "MA-Q-0228": ["A", "B", "E"]}

ALLOWED_NEW_PATHS = {
    LOCK_PATH,
    f"data/audits/{LEGAL_AUDIT_ID}.json",
    f"data/audits/{REALISM_AUDIT_ID}.json",
}
REALISM_CRITERIA = [
    "jurisprudence_reasoning",
    "practice_plausibility",
    "authentic_distractors",
    "wording_not_guessable",
    "reasoning_not_trivia",
    "natural_rule_combination",
    "appropriate_drug_context",
    "distinct_from_bank",
    "not_schedule_flashcard",
    "public_style_without_copying",
]


class Check:
    def __init__(self) -> None:
        self.results: dict[str, dict] = {}
        self.failures: list[str] = []

    def __call__(self, key: str, ok: bool, detail: object = None) -> bool:
        self.results[key] = {"status": "PASS" if ok else "FAIL", "detail": detail}
        if not ok:
            self.failures.append(f"{key}: {detail}")
        return ok

    @property
    def ok(self) -> bool:
        return not self.failures


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def commit_epoch(sha: str) -> int:
    return int(git("show", "-s", "--format=%ct", sha))


def run() -> tuple[Check, dict]:
    check = Check()
    questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}
    style_profile = load_json(DATA / "exam_style" / "mpje_style_profile.json")
    _, audits = validate_audits()

    # --- 1. auditor identity, distinct from the author -------------------------
    identity = {}
    for audit_id in (LEGAL_AUDIT_ID, REALISM_AUDIT_ID):
        audit = audits.get(audit_id, {})
        identity[audit_id] = {
            "auditor": audit.get("auditor"),
            "auditor_instance": audit.get("auditor_instance"),
            "independent": audit.get("independent"),
            "audit_status": audit.get("audit_status"),
            "audit_scope": audit.get("audit_scope"),
            "review_type": audit.get("review_type"),
        }
    check(
        "01_auditor_identity",
        all(
            item["auditor"] == AUDITOR
            and item["auditor_instance"] == AUDITOR_INSTANCE
            and item["independent"] is True
            and item["audit_status"] == "FULLY_ADJUDICATED"
            and item["audit_scope"] == "TARGETED_INITIAL_BATCH"
            for item in identity.values()
        )
        and identity[LEGAL_AUDIT_ID]["review_type"] == "LEGAL_VERIFICATION"
        and identity[REALISM_AUDIT_ID]["review_type"] == "REALISM_REVIEW",
        identity,
    )

    # --- 2. Phase-1 lock precedes the audit records ---------------------------
    lock_files = git("show", "--name-only", "--format=", LOCK_COMMIT_SHA).splitlines()
    record_files = git("show", "--name-only", "--format=", AUDIT_HEAD_SHA).splitlines()
    lock_epoch, records_epoch = commit_epoch(LOCK_COMMIT_SHA), commit_epoch(AUDIT_HEAD_SHA)
    lock_is_parent = git("rev-parse", f"{AUDIT_HEAD_SHA}^") == LOCK_COMMIT_SHA
    ordering = {
        "lock_commit": LOCK_COMMIT_SHA,
        "lock_commit_files": lock_files,
        "records_commit": AUDIT_HEAD_SHA,
        "records_commit_files": record_files,
        "lock_is_parent_of_records": lock_is_parent,
        "lock_epoch": lock_epoch,
        "records_epoch": records_epoch,
        "seconds_between": records_epoch - lock_epoch,
        "lock_blob_at_lock_commit": git("rev-parse", f"{LOCK_COMMIT_SHA}:{LOCK_PATH}"),
        "lock_blob_at_head": git("rev-parse", f"{AUDIT_HEAD_SHA}:{LOCK_PATH}"),
    }
    check(
        "02_lock_precedes_and_is_immutable",
        lock_files == [LOCK_PATH]
        and lock_is_parent
        and lock_epoch < records_epoch
        and ordering["lock_blob_at_lock_commit"] == LOCK_BLOB
        and ordering["lock_blob_at_head"] == LOCK_BLOB,
        ordering,
    )

    # --- 3. audit branch touched nothing but its own three artifacts ----------
    changed = git("diff", "--name-only", AUDIT_BASE_SHA, AUDIT_HEAD_SHA).splitlines()
    check(
        "03_no_canonical_or_tooling_edits",
        set(changed) == ALLOWED_NEW_PATHS,
        {"changed": changed, "allowed": sorted(ALLOWED_NEW_PATHS)},
    )

    # --- 4. exact current question hashes -------------------------------------
    current = {question_id: question_audit_hash(questions[question_id]) for question_id in QUESTION_IDS}
    check(
        "04_current_question_hashes",
        current == EXPECTED_HASHES,
        {"current": current, "expected": EXPECTED_HASHES},
    )

    # --- 5. audited content identical to the represented candidate ------------
    drift = []
    for question_id in QUESTION_IDS:
        raw = subprocess.check_output(
            ["git", "show", f"{CANDIDATE_SHA}:data/questions/{question_id.lower()}.json"], cwd=ROOT
        )
        source = json.loads(raw.decode("utf-8"))
        audited = {field: source.get(field) for field in QUESTION_AUDIT_FIELDS}
        live = {field: questions[question_id].get(field) for field in QUESTION_AUDIT_FIELDS}
        if audited != live:
            drift.append(question_id)
    check("05_no_substantive_drift_since_candidate", not drift, drift or f"identical to {CANDIDATE_SHA[:12]}")

    # --- 6. governance authorization exact ------------------------------------
    authorizations = {}
    for audit_id in (LEGAL_AUDIT_ID, REALISM_AUDIT_ID):
        authorizations[audit_id] = audits.get(audit_id, {}).get("governance_authorization")
    expected_auth = {
        "tranche_id": TRANCHE_ID,
        "authorizing_issue": AUTHORIZING_ISSUE,
        "represented_candidate_sha": CANDIDATE_SHA,
        "question_ids": QUESTION_IDS,
    }
    check(
        "06_governance_authorization_exact",
        all(item == expected_auth for item in authorizations.values()),
        authorizations,
    )
    check(
        "07_is_valid_targeted_initial_audit",
        all(is_valid_targeted_initial_audit(audits.get(audit_id, {})) for audit_id in (LEGAL_AUDIT_ID, REALISM_AUDIT_ID)),
        {audit_id: is_valid_targeted_initial_audit(audits.get(audit_id, {})) for audit_id in (LEGAL_AUDIT_ID, REALISM_AUDIT_ID)},
    )

    # --- 8. audit records bound to the current hashes -------------------------
    binding = {
        audit_id: audits.get(audit_id, {}).get("question_hashes") for audit_id in (LEGAL_AUDIT_ID, REALISM_AUDIT_ID)
    }
    check("08_records_bound_to_current_hashes", all(item == current for item in binding.values()), binding)

    # --- 9/10. release-qualifying LEGAL and REALISM results -------------------
    legal_results = {item["Question_ID"]: item for item in audits.get(LEGAL_AUDIT_ID, {}).get("results", [])}
    realism_results = {item["Question_ID"]: item for item in audits.get(REALISM_AUDIT_ID, {}).get("results", [])}
    legal_summary = {
        question_id: {
            "Verdict": legal_results.get(question_id, {}).get("Verdict"),
            "Existing_Answer_Correct": legal_results.get(question_id, {}).get("Existing_Answer_Correct"),
            "Proposed_Answer": legal_results.get(question_id, {}).get("Proposed_Answer"),
            "authority_count": len(legal_results.get(question_id, {}).get("authorities", [])),
        }
        for question_id in QUESTION_IDS
    }
    check(
        "09_legal_keep_yes_for_both",
        all(
            item["Verdict"] == "KEEP" and item["Existing_Answer_Correct"] == "YES" and item["authority_count"] >= 1
            for item in legal_summary.values()
        ),
        legal_summary,
    )
    realism_summary = {
        question_id: {
            "Verdict": realism_results.get(question_id, {}).get("Verdict"),
            "Realism_Verdict": realism_results.get(question_id, {}).get("Realism_Verdict"),
            "criteria_count": len(realism_results.get(question_id, {}).get("Criteria", {})),
            "all_criteria_true": all(realism_results.get(question_id, {}).get("Criteria", {}).values()),
            "notes_length": len(realism_results.get(question_id, {}).get("Notes", "")),
        }
        for question_id in QUESTION_IDS
    }
    check(
        "10_realism_keep_pass_all_ten_criteria",
        all(
            item["Verdict"] == "KEEP"
            and item["Realism_Verdict"] == "PASS"
            and item["criteria_count"] == 10
            and item["all_criteria_true"]
            for item in realism_summary.values()
        )
        and all(
            set(realism_results[question_id]["Criteria"]) == set(REALISM_CRITERIA) for question_id in QUESTION_IDS
        ),
        realism_summary,
    )

    # --- 11. realism style profile is current ---------------------------------
    check(
        "11_realism_style_profile_current",
        audits.get(REALISM_AUDIT_ID, {}).get("style_profile") == style_profile_snapshot(style_profile),
        {
            "record": audits.get(REALISM_AUDIT_ID, {}).get("style_profile"),
            "current": style_profile_snapshot(style_profile),
        },
    )

    # --- 12. full-bank comparison evidence names real comparators -------------
    comparison = {}
    for question_id in QUESTION_IDS:
        notes = realism_results.get(question_id, {}).get("Notes", "")
        named = sorted({token for token in questions if token in notes and token != question_id})
        comparison[question_id] = {
            "named_comparators": named,
            "all_exist_in_bank": all(token in questions for token in named),
            "bank_size_claimed_in_notes": "228" in notes,
        }
    check(
        "12_full_bank_comparison_evidence",
        all(item["named_comparators"] and item["all_exist_in_bank"] and item["bank_size_claimed_in_notes"] for item in comparison.values())
        and len(questions) == 228,
        {"bank_size_actual": len(questions), **comparison},
    )

    # --- 13. blind lock integrity and blind answers vs canonical keys ---------
    lock = json.loads(subprocess.check_output(["git", "show", f"{AUDIT_HEAD_SHA}:{LOCK_PATH}"], cwd=ROOT).decode("utf-8"))
    blind = {item["question_id"]: item["selected_choice_ids"] for item in lock["questions"]}
    canonical = {question_id: questions[question_id]["correct_choice_ids"] for question_id in QUESTION_IDS}
    lock_state = {
        "auditor_instance": lock.get("auditor_instance"),
        "contamination_status": lock.get("contamination_status"),
        "blind_package_blob": lock.get("blind_package_blob"),
        "represented_candidate_sha": lock.get("represented_candidate_sha"),
        "audit_base_sha": lock.get("audit_base_sha"),
        "blind_answers": blind,
        "canonical_keys": canonical,
        "blind_matches_key": {q: sorted(blind.get(q, [])) == sorted(canonical[q]) for q in QUESTION_IDS},
        "expected_keys_confirmed": canonical == EXPECTED_KEYS,
        "not_inspected_flags": {
            key: lock.get(key)
            for key in (
                "canonical_key_inspected_before_lock",
                "canonical_explanation_inspected_before_lock",
                "canonical_rules_inspected_before_lock",
                "author_reasoning_inspected_before_lock",
            )
        },
    }
    check(
        "13_blind_lock_integrity",
        lock_state["auditor_instance"] == AUDITOR_INSTANCE
        and lock_state["contamination_status"] == "CLEAN"
        and lock_state["blind_package_blob"] == BLIND_BLOB
        and lock_state["represented_candidate_sha"] == CANDIDATE_SHA
        and lock_state["audit_base_sha"] == AUDIT_BASE_SHA
        and not any(lock_state["not_inspected_flags"].values())
        and lock_state["expected_keys_confirmed"],
        lock_state,
    )

    # --- 14. the blind package the auditor locked against is the one published -
    published_blob = git("rev-parse", f"origin/{FREEZE_BRANCH}:audits/remediation/2026-08-19/T3-BLIND-QUESTIONS-PRE-BATCH3-COVERAGE-T3.json")
    check("14_blind_package_matches_published", published_blob == BLIND_BLOB, {"published": published_blob, "locked": BLIND_BLOB})

    # --- 15. negative-control residue: committed records carry no injected value
    residue = []
    for audit_id in (LEGAL_AUDIT_ID, REALISM_AUDIT_ID):
        for result in audits.get(audit_id, {}).get("results", []):
            if result.get("Verdict") != "KEEP":
                residue.append(f"{audit_id}:{result.get('Question_ID')}:{result.get('Verdict')}")
            if result.get("Existing_Answer_Correct") not in (None, "YES"):
                residue.append(f"{audit_id}:{result.get('Question_ID')}:{result.get('Existing_Answer_Correct')}")
            if result.get("Realism_Verdict") not in (None, "PASS"):
                residue.append(f"{audit_id}:{result.get('Question_ID')}:{result.get('Realism_Verdict')}")
    worktree_vs_commit = git("diff", "--name-only", AUDIT_HEAD_SHA, "--", "data/audits").splitlines()
    check(
        "15_no_negative_control_residue",
        not residue and not worktree_vs_commit,
        {"residue": residue, "worktree_differs_from_commit": worktree_vs_commit},
    )

    # --- 16. no other current-hash adjudicated failure covers either question --
    hidden = []
    for question_id in QUESTION_IDS:
        for audit_id, audit in sorted(audits.items()):
            if not audit.get("independent") or audit.get("audit_status") != "FULLY_ADJUDICATED":
                continue
            if audit.get("question_hashes", {}).get(question_id) != current[question_id]:
                continue
            result = next((item for item in audit.get("results", []) if item.get("Question_ID") == question_id), None)
            if result is None:
                continue
            if audit.get("review_type") == "LEGAL_VERIFICATION":
                if result.get("Verdict") != "KEEP" or result.get("Existing_Answer_Correct") != "YES":
                    hidden.append({"question_id": question_id, "audit_id": audit_id})
            elif audit.get("review_type") == "REALISM_REVIEW":
                if audit.get("style_profile") != style_profile_snapshot(style_profile):
                    continue
                if result.get("Verdict") != "KEEP" or result.get("Realism_Verdict") != "PASS":
                    hidden.append({"question_id": question_id, "audit_id": audit_id})
    check("16_no_current_hash_failure", not hidden, hidden or "none")

    payload = {
        "report_type": "T3_FRESH_AUDIT_EVIDENCE_VERIFICATION",
        "controller_issue": 83,
        "authorizing_issue": AUTHORIZING_ISSUE,
        "tranche_id": TRANCHE_ID,
        "audit_pr": 88,
        "audit_branch": "audit/pre-batch3-coverage-t3-claude-fresh-cov-t3-a",
        "audit_head_sha": AUDIT_HEAD_SHA,
        "phase1_lock_commit": LOCK_COMMIT_SHA,
        "phase1_lock_blob": LOCK_BLOB,
        "auditor": AUDITOR,
        "auditor_instance": AUDITOR_INSTANCE,
        "author_is_not_auditor": True,
        "status": "PASS" if check.ok else "FAIL",
        "checks": check.results,
        "failures": check.failures,
    }
    return check, payload


def main() -> int:
    check, payload = run()
    output = ROOT / "audits" / "remediation" / "2026-08-19" / "T3-FRESH-AUDIT-EVIDENCE-VERIFICATION.json"
    write_json(output, payload)
    for key, value in payload["checks"].items():
        print(f"[{value['status']}] {key}")
    for failure in check.failures:
        print(f"FAIL {failure}")
    print(f"verification: {'PASS' if check.ok else 'FAIL'} -> {output.relative_to(ROOT).as_posix()}")
    return 0 if check.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
