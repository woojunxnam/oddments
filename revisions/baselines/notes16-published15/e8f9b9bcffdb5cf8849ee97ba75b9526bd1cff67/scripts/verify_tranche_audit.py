"""Controller-side verification of a fresh independent tranche audit before any release.

Generalizes the one-off Pre-Batch3 T3 verifier (scripts/verify_t3_audit_evidence.py) so
Batch 3 tranches do not re-implement it. The auditor's own report is never evidence: every
condition below is recomputed from the repository.

Unlike the T3 verifier this tool tolerates a PARTIAL result. A tranche audit may return
some questions release-qualifying and others not. That is a legitimate audit outcome, not
a verification failure, so the tool separates two questions:

  * did the audit process hold?  (independence, blind lock, boundary, binding, schema)
  * which questions did it clear? (per-question release eligibility)

Only the first can FAIL the verification. The second is reported as a partition.

    python scripts/verify_tranche_audit.py --config audits/remediation/2026-08-19/B3A-AUDIT-VERIFY-CONFIG.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, ROOT, QUESTION_AUDIT_FIELDS, load_json, load_records, question_audit_hash, write_json
from release_context import style_profile_snapshot
from validate_audits import validate_audits


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


def show(sha: str, path: str) -> dict:
    return json.loads(subprocess.check_output(["git", "show", f"{sha}:{path}"], cwd=ROOT).decode("utf-8"))


def commit_epoch(sha: str) -> int:
    return int(git("show", "-s", "--format=%ct", sha))


def run(cfg: dict) -> tuple[Check, dict]:
    check = Check()
    qids = cfg["question_ids"]
    legal_id, realism_id = cfg["legal_audit_id"], cfg["realism_audit_id"]
    lock_path = cfg["lock_path"]
    allowed_paths = {lock_path, f"data/audits/{legal_id}.json", f"data/audits/{realism_id}.json"}
    if cfg.get("adjudication_report_path"):
        allowed_paths.add(cfg["adjudication_report_path"])

    questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}
    style_profile = load_json(DATA / "exam_style" / "mpje_style_profile.json")
    _, audits = validate_audits()

    # --- 1. auditor identity, distinct from the author ------------------------
    identity = {}
    for audit_id in (legal_id, realism_id):
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
            item["auditor"] == cfg["auditor"]
            and item["auditor_instance"] == cfg["auditor_instance"]
            and item["independent"] is True
            and item["audit_status"] == "FULLY_ADJUDICATED"
            and item["audit_scope"] == cfg["audit_scope"]
            for item in identity.values()
        )
        and identity[legal_id]["review_type"] == "LEGAL_VERIFICATION"
        and identity[realism_id]["review_type"] == "REALISM_REVIEW"
        and cfg["auditor_instance"] != cfg["author_instance"],
        identity,
    )

    # --- 2. Phase-1 lock precedes the audit records and never moved -----------
    lock_files = git("show", "--name-only", "--format=", cfg["lock_commit_sha"]).splitlines()
    lock_epoch = commit_epoch(cfg["lock_commit_sha"])
    records_epoch = commit_epoch(cfg["audit_head_sha"])
    ordering = {
        "lock_commit": cfg["lock_commit_sha"],
        "lock_commit_files": lock_files,
        "records_commit": cfg["audit_head_sha"],
        "records_commit_files": git("show", "--name-only", "--format=", cfg["audit_head_sha"]).splitlines(),
        "lock_is_ancestor_of_records": subprocess.call(
            ["git", "merge-base", "--is-ancestor", cfg["lock_commit_sha"], cfg["audit_head_sha"]], cwd=ROOT
        ) == 0,
        "lock_epoch": lock_epoch,
        "records_epoch": records_epoch,
        "seconds_between": records_epoch - lock_epoch,
        "lock_blob_at_lock_commit": git("rev-parse", f"{cfg['lock_commit_sha']}:{lock_path}"),
        "lock_blob_at_head": git("rev-parse", f"{cfg['audit_head_sha']}:{lock_path}"),
    }
    check(
        "02_lock_precedes_and_is_immutable",
        lock_files == [lock_path]
        and ordering["lock_is_ancestor_of_records"]
        and lock_epoch < records_epoch
        and ordering["lock_blob_at_lock_commit"] == cfg["lock_blob"]
        and ordering["lock_blob_at_head"] == cfg["lock_blob"],
        ordering,
    )

    # --- 3. audit branch touched nothing but its own three artifacts ----------
    changed = git("diff", "--name-only", cfg["audit_base_sha"], cfg["audit_head_sha"]).splitlines()
    check(
        "03_no_canonical_or_tooling_edits",
        set(changed) == allowed_paths,
        {"changed": changed, "allowed": sorted(allowed_paths)},
    )

    # --- 4. the audit base descends from an unchanged represented candidate --
    merge_base = git("merge-base", cfg["audit_head_sha"], cfg["candidate_sha"])
    candidate_is_ancestor_of_base = subprocess.call(
        ["git", "merge-base", "--is-ancestor", cfg["candidate_sha"], cfg["audit_base_sha"]], cwd=ROOT
    ) == 0
    base_is_ancestor_of_head = subprocess.call(
        ["git", "merge-base", "--is-ancestor", cfg["audit_base_sha"], cfg["audit_head_sha"]], cwd=ROOT
    ) == 0
    canonical_drift_to_audit_base = git(
        "diff",
        "--name-only",
        cfg["candidate_sha"],
        cfg["audit_base_sha"],
        "--",
        "data/questions",
        "data/rules",
        "data/drugs",
        "data/blueprint.json",
        "data/exam_style/mpje_style_profile.json",
    ).splitlines()
    check(
        "04_audit_base_is_the_candidate",
        merge_base == cfg["candidate_sha"]
        and candidate_is_ancestor_of_base
        and base_is_ancestor_of_head
        and not canonical_drift_to_audit_base,
        {
            "merge_base": merge_base,
            "candidate_sha": cfg["candidate_sha"],
            "audit_base_sha": cfg["audit_base_sha"],
            "candidate_is_ancestor_of_base": candidate_is_ancestor_of_base,
            "base_is_ancestor_of_head": base_is_ancestor_of_head,
            "canonical_drift_to_audit_base": canonical_drift_to_audit_base,
        },
    )

    # --- 5. exact current question hashes match the audit records ------------
    current = {qid: question_audit_hash(questions[qid]) for qid in qids if qid in questions}
    missing = [qid for qid in qids if qid not in questions]
    binding = {audit_id: audits.get(audit_id, {}).get("question_hashes") for audit_id in (legal_id, realism_id)}
    check(
        "05_records_bound_to_current_hashes",
        not missing and all(item == current for item in binding.values()),
        {"missing_questions": missing, "matches": {k: (v == current) for k, v in binding.items()}},
    )

    # --- 6. audited content identical to the represented candidate -----------
    drift = []
    for qid in qids:
        source = show(cfg["candidate_sha"], f"data/questions/{qid.lower()}.json")
        audited = {field: source.get(field) for field in QUESTION_AUDIT_FIELDS}
        live = {field: questions.get(qid, {}).get(field) for field in QUESTION_AUDIT_FIELDS}
        if audited != live:
            drift.append(qid)
    check("06_no_substantive_drift_since_candidate", not drift, drift or f"identical to {cfg['candidate_sha'][:12]}")

    # --- 7. coverage: every question adjudicated exactly once in each record --
    legal_results = {item["Question_ID"]: item for item in audits.get(legal_id, {}).get("results", [])}
    realism_results = {item["Question_ID"]: item for item in audits.get(realism_id, {}).get("results", [])}
    coverage = {
        "legal_count": len(audits.get(legal_id, {}).get("results", [])),
        "realism_count": len(audits.get(realism_id, {}).get("results", [])),
        "legal_missing": sorted(set(qids) - set(legal_results)),
        "realism_missing": sorted(set(qids) - set(realism_results)),
        "legal_extra": sorted(set(legal_results) - set(qids)),
        "realism_extra": sorted(set(realism_results) - set(qids)),
    }
    check(
        "07_full_coverage_no_extras",
        coverage["legal_count"] == coverage["realism_count"] == len(qids)
        and not any(coverage[k] for k in ("legal_missing", "realism_missing", "legal_extra", "realism_extra")),
        coverage,
    )

    # --- 8. every LEGAL result is structurally complete ----------------------
    required = ["Question_ID", "Verdict", "Severity", "Existing_Answer_Correct",
                "authorities", "Problem", "Proposed_Answer", "Proposed_Rewrite", "Proposed_Explanation"]
    legal_defects = []
    for qid in qids:
        item = legal_results.get(qid, {})
        for field in required:
            if field not in item:
                legal_defects.append(f"{qid}:missing:{field}")
        for authority in item.get("authorities", []):
            for field in ("authority", "source_type", "exact_section", "official_url", "law_checked_date"):
                if not authority.get(field):
                    legal_defects.append(f"{qid}:authority_missing:{field}")
            if not str(authority.get("official_url", "")).startswith("https://"):
                legal_defects.append(f"{qid}:authority_url_not_https")
        if len(item.get("authorities", [])) < 1:
            legal_defects.append(f"{qid}:no_authority")
    check("08_legal_results_structurally_complete", not legal_defects, legal_defects or "all complete")

    # --- 9. every REALISM result carries the full ten-criterion grid ---------
    realism_defects = []
    for qid in qids:
        item = realism_results.get(qid, {})
        criteria = item.get("Criteria", {})
        if set(criteria) != set(REALISM_CRITERIA):
            realism_defects.append(f"{qid}:criteria_set")
        if not item.get("Notes"):
            realism_defects.append(f"{qid}:no_notes")
        if item.get("Realism_Verdict") not in ("PASS", "FAIL"):
            realism_defects.append(f"{qid}:verdict={item.get('Realism_Verdict')}")
        # A FAIL must be explained by at least one false criterion, and a PASS by none.
        false_criteria = [k for k, v in criteria.items() if not v]
        if item.get("Realism_Verdict") == "PASS" and false_criteria:
            realism_defects.append(f"{qid}:pass_with_false_criteria:{false_criteria}")
        if item.get("Realism_Verdict") == "FAIL" and not false_criteria:
            realism_defects.append(f"{qid}:fail_without_false_criterion")
    check("09_realism_results_structurally_complete", not realism_defects, realism_defects or "all complete")

    # --- 10. realism style profile is current --------------------------------
    check(
        "10_realism_style_profile_current",
        audits.get(realism_id, {}).get("style_profile") == style_profile_snapshot(style_profile),
        {"record": audits.get(realism_id, {}).get("style_profile"),
         "current": style_profile_snapshot(style_profile)},
    )

    # --- 11. full-bank comparison evidence names real comparators ------------
    bank_size = len(questions)
    comparison_defects = []
    for qid in qids:
        notes = realism_results.get(qid, {}).get("Notes", "")
        named = sorted({token for token in questions if token in notes and token != qid})
        if not named:
            comparison_defects.append(f"{qid}:no_named_comparator")
    check(
        "11_full_bank_comparison_evidence",
        not comparison_defects and bank_size == cfg["expected_bank_size"],
        {"bank_size_actual": bank_size, "bank_size_expected": cfg["expected_bank_size"],
         "defects": comparison_defects or "none"},
    )

    # --- 12. blind lock integrity, and blind answers vs canonical keys -------
    lock = show(cfg["audit_head_sha"], lock_path)
    lock_items = lock.get("questions", lock.get("responses", []))
    blind = {item["question_id"]: item["selected_choice_ids"] for item in lock_items}
    canonical = {qid: questions[qid]["correct_choice_ids"] for qid in qids if qid in questions}
    matches = {qid: sorted(blind.get(qid, [])) == sorted(canonical.get(qid, [])) for qid in qids}
    old_flag_names = (
        "canonical_key_inspected_before_lock",
        "canonical_explanation_inspected_before_lock",
        "canonical_rules_inspected_before_lock",
        "author_reasoning_inspected_before_lock",
    )
    if any(key in lock for key in old_flag_names):
        flags = {key: lock.get(key) for key in old_flag_names}
    else:
        contamination_flags = lock.get("contamination_flags", {})
        flags = {
            "canonical_key_inspected_before_lock": contamination_flags.get("answer_key_or_explanation_inspected"),
            "canonical_explanation_inspected_before_lock": contamination_flags.get("answer_key_or_explanation_inspected"),
            "canonical_rules_inspected_before_lock": contamination_flags.get("prohibited_repository_content_inspected"),
            "author_reasoning_inspected_before_lock": contamination_flags.get("controller_reasoning_inspected"),
        }
    contamination_status = lock.get("contamination_status")
    if contamination_status is None:
        contamination_status = "CONTAMINATED" if lock.get("contamination_flags", {}).get("any_contamination") else "CLEAN"
    blind_package_blob = lock.get("blind_package_blob")
    if blind_package_blob is None:
        blind_package_blob = lock.get("blind_package", {}).get("git_blob_sha1")
    lock_state = {
        "auditor_instance": lock.get("auditor_instance"),
        "contamination_status": contamination_status,
        "blind_package_blob": blind_package_blob,
        "represented_candidate_sha": lock.get("represented_candidate_sha"),
        "locked_question_count": len(blind),
        "blind_matches_key_count": sum(matches.values()),
        "blind_mismatches": sorted(q for q, ok in matches.items() if not ok),
        "not_inspected_flags": flags,
    }
    check(
        "12_blind_lock_integrity",
        lock_state["auditor_instance"] == cfg["auditor_instance"]
        and lock_state["contamination_status"] == "CLEAN"
        and lock_state["blind_package_blob"] == cfg["blind_blob"]
        and lock_state["represented_candidate_sha"] == cfg["candidate_sha"]
        and lock_state["locked_question_count"] == len(qids)
        and not any(flags.values()),
        lock_state,
    )

    # --- 13. the blind package locked against is the one published ----------
    published = git("rev-parse", f"origin/{cfg['freeze_branch']}:{cfg['blind_path']}")
    check("13_blind_package_matches_published", published == cfg["blind_blob"],
          {"published": published, "locked": cfg["blind_blob"]})

    # --- 14. no worktree divergence from the committed audit records --------
    divergence = git("diff", "--name-only", cfg["audit_head_sha"], "--", "data/audits").splitlines()
    check("14_no_uncommitted_audit_edits", not divergence, divergence or "clean")

    # --- 15. release-eligibility partition (informational, never a failure) --
    eligible, blocked = [], {}
    for qid in qids:
        legal = legal_results.get(qid, {})
        realism = realism_results.get(qid, {})
        reasons = []
        if legal.get("Verdict") != "KEEP":
            reasons.append(f"legal_verdict={legal.get('Verdict')}")
        if legal.get("Existing_Answer_Correct") != "YES":
            reasons.append(f"existing_answer_correct={legal.get('Existing_Answer_Correct')}")
        if realism.get("Verdict") != "KEEP":
            reasons.append(f"realism_verdict={realism.get('Verdict')}")
        if realism.get("Realism_Verdict") != "PASS":
            reasons.append(f"realism_result={realism.get('Realism_Verdict')}")
        false_criteria = [k for k, v in realism.get("Criteria", {}).items() if not v]
        if false_criteria:
            reasons.append(f"criteria_false={false_criteria}")
        if reasons:
            blocked[qid] = reasons
        else:
            eligible.append(qid)
    check(
        "15_release_partition_computed",
        len(eligible) + len(blocked) == len(qids),
        {"eligible_count": len(eligible), "blocked_count": len(blocked), "blocked": blocked},
    )

    # --- 16. no hidden current-hash adjudicated failure on an eligible item --
    hidden = []
    for qid in eligible:
        for audit_id, audit in sorted(audits.items()):
            if not audit.get("independent") or audit.get("audit_status") != "FULLY_ADJUDICATED":
                continue
            if audit.get("question_hashes", {}).get(qid) != current.get(qid):
                continue
            result = next((i for i in audit.get("results", []) if i.get("Question_ID") == qid), None)
            if result is None:
                continue
            if audit.get("review_type") == "LEGAL_VERIFICATION":
                if result.get("Verdict") != "KEEP" or result.get("Existing_Answer_Correct") != "YES":
                    hidden.append({"question_id": qid, "audit_id": audit_id})
            elif audit.get("review_type") == "REALISM_REVIEW":
                if audit.get("style_profile") != style_profile_snapshot(style_profile):
                    continue
                if result.get("Verdict") != "KEEP" or result.get("Realism_Verdict") != "PASS":
                    hidden.append({"question_id": qid, "audit_id": audit_id})
    check("16_no_hidden_current_hash_failure_on_eligible", not hidden, hidden or "none")

    payload = {
        "report_type": "TRANCHE_FRESH_AUDIT_EVIDENCE_VERIFICATION",
        "tranche": cfg["tranche"],
        "controller_issue": cfg["controller_issue"],
        "authorizing_issue": cfg["authorizing_issue"],
        "audit_pr": cfg["audit_pr"],
        "audit_branch": cfg["audit_branch"],
        "audit_base_sha": cfg["audit_base_sha"],
        "audit_head_sha": cfg["audit_head_sha"],
        "phase1_lock_commit": cfg["lock_commit_sha"],
        "phase1_lock_blob": cfg["lock_blob"],
        "represented_candidate_sha": cfg["candidate_sha"],
        "auditor": cfg["auditor"],
        "auditor_instance": cfg["auditor_instance"],
        "author_instance": cfg["author_instance"],
        "author_is_not_auditor": cfg["auditor_instance"] != cfg["author_instance"],
        "process_status": "PASS" if check.ok else "FAIL",
        "release_eligible": eligible,
        "release_blocked": blocked,
        "checks": check.results,
        "failures": check.failures,
    }
    return check, payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    cfg = load_json(Path(args.config))
    check, payload = run(cfg)
    output = Path(args.out) if args.out else ROOT / cfg["output_path"]
    write_json(output, payload)

    for key, value in payload["checks"].items():
        print(f"[{value['status']}] {key}")
    for failure in check.failures:
        print(f"FAIL {failure}")
    print(f"release eligible: {len(payload['release_eligible'])}/{len(cfg['question_ids'])}")
    for qid, reasons in payload["release_blocked"].items():
        print(f"  blocked {qid}: {reasons}")
    print(f"process verification: {'PASS' if check.ok else 'FAIL'} -> {output.relative_to(ROOT).as_posix()}")
    return 0 if check.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
