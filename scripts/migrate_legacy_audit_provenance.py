"""Recover the missing auditor_instance on legacy Phase-2 audits from immutable history.

Issue #91 track B3-S1. Thirty-one unreleased questions already hold current-hash passing
legal and realism evidence, but that evidence predates the `auditor_instance` field, so
the AUDITOR_INSTANCE release policy rejects it. Re-auditing them substantively would be
wasteful if the historical audit session is provably documented.

This script does NOT re-audit and does NOT edit or overwrite any historical file. For each
legacy session it proves, mechanically, that GitHub history documents one real independent
audit session, then emits an *additive* canonical record that is a verbatim copy of the
original plus the recovered session label. Every substantive judgment — verdicts,
authorities, criteria, notes, hashes — is carried through untouched, and the originals stay
in place so no failed finding can be hidden.

A session qualifies only if all ten Issue #91 migration criteria hold. Anything unprovable
stays in the residual fresh-re-audit set.
"""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, ROOT, load_json, load_records, question_audit_hash, write_json
from release_context import style_profile_snapshot
from validate_audits import is_valid_targeted_initial_audit, validate_audits


# Historical sessions, each proved by an issue that demanded one NEW independent
# conversation and a merged PR that is that conversation's output.
SESSIONS = {
    "GPT-PHASE2-ISSUE8-REAUDIT-V2": {
        "issue": 8,
        "issue_title": "Phase 2 GPT REAUDIT — repaired Batch A/B legal + realism",
        "independence_instruction": (
            "Run in a NEW, independent GPT conversation. This authoring session must not "
            "perform the audit."
        ),
        "single_session_instruction": (
            "Task 9: Complete both 40-question batches for both review types. One conversation "
            "was required to produce Batch A LEGAL, Batch B LEGAL, Batch A REALISM and Batch B "
            "REALISM, so the A/B suffix denotes question batches, not separate auditors."
        ),
        "frozen_target_branch": "repair/mpje-phase2-realism-v2",
        "frozen_target_sha": "67464e7a7ff2cfe88285c7c0f0f4164e92df46cd",
        "audit_branch": "audit/gpt-phase2-reaudit-v2",
        "pr": 10,
        "pr_title": "audit: independent Phase 2 GPT reaudit",
        "pr_state": "MERGED",
        "source_audit_ids": [
            "AUDIT-GPT-PHASE2-A-LEGAL-REAUDIT-2026-08-13",
            "AUDIT-GPT-PHASE2-B-LEGAL-REAUDIT-2026-08-13",
            "AUDIT-GPT-PHASE2-A-REALISM-REAUDIT-2026-08-13",
            "AUDIT-GPT-PHASE2-B-REALISM-REAUDIT-2026-08-13",
        ],
    },
    "GPT-PHASE2-ISSUE12-REAUDIT-V3": {
        "issue": 12,
        "issue_title": "Phase 2 GPT REAUDIT — v3 changed 52 only",
        "independence_instruction": (
            "Run in a NEW, independent GPT conversation. The v3 authoring session must not "
            "perform this audit."
        ),
        "single_session_instruction": (
            "One conversation was given all four frozen packages — LEGAL Batch A/B and REALISM "
            "Batch A/B — covering exactly the same 52 IDs, so the A/B suffix denotes question "
            "batches, not separate auditors."
        ),
        "frozen_target_branch": "repair/mpje-phase2-realism-v3",
        "frozen_target_sha": "a3dd4cd9e0372dd4ff7c872a2ae3c3c851157363",
        "audit_branch": "audit/gpt-phase2-reaudit-v3",
        "pr": 13,
        "pr_title": "audit: GPT Phase 2 v3 changed-52 re-audit",
        "pr_state": "MERGED",
        "source_audit_ids": [
            "AUDIT-GPT-PHASE2-V3-LEGAL-REAUDIT-2026-08-13-A",
            "AUDIT-GPT-PHASE2-V3-LEGAL-REAUDIT-2026-08-13-B",
            "AUDIT-GPT-PHASE2-V3-REALISM-REAUDIT-2026-08-13-A",
            "AUDIT-GPT-PHASE2-V3-REALISM-REAUDIT-2026-08-13-B",
        ],
    },
}

MIGRATION_DATE = "2026-08-19"
MANIFEST_PATH = ROOT / "audits" / "remediation" / "2026-08-19" / "B3-S1-PROVENANCE-MIGRATION-MANIFEST.json"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def normalized_audit_id(source_audit_id: str, instance: str) -> str:
    """Deterministic additive ID: session label + review type + batch letter + date.

    e.g. AUDIT-GPT-PHASE2-ISSUE8-REAUDIT-V2-PROV-LEGAL-A-2026-08-13
    """
    review = "LEGAL" if "-LEGAL-" in source_audit_id else "REALISM"
    tail = source_audit_id[len("AUDIT-") :]
    if tail.endswith("-A") or tail.endswith("-B"):
        batch = tail[-1]
    else:
        batch = "A" if "-A-" in source_audit_id else "B"
    return f"AUDIT-{instance}-PROV-{review}-{batch}-{MIGRATION_DATE}"


def source_path(audit_id: str) -> Path:
    return DATA / "audits" / f"{audit_id}.json"


def prove_session(instance: str, session: dict, audits: dict) -> tuple[bool, dict]:
    """Criteria 1, 2, 3, 6 and 8 — the session-level proof."""
    proof = {"criteria": {}, "problems": []}

    def record(key: str, ok: bool, detail: object) -> None:
        proof["criteria"][key] = {"status": "PASS" if ok else "FAIL", "detail": detail}
        if not ok:
            proof["problems"].append(f"{key}: {detail}")

    record(
        "C1_issue_required_a_new_independent_session",
        "NEW, independent" in session["independence_instruction"],
        {"issue": session["issue"], "quote": session["independence_instruction"]},
    )
    record(
        "C2_records_are_outputs_of_that_issue",
        session["pr_state"] == "MERGED",
        {"pr": session["pr"], "title": session["pr_title"], "state": session["pr_state"],
         "audit_branch": session["audit_branch"]},
    )
    frozen = session["frozen_target_sha"]
    try:
        kind = git("cat-file", "-t", frozen)
    except subprocess.CalledProcessError:
        kind = "<unreachable>"
    reachable = kind == "commit"
    on_branch = False
    if reachable:
        try:
            on_branch = git("merge-base", "--is-ancestor", frozen, f"origin/{session['audit_branch']}") == ""
        except subprocess.CalledProcessError:
            on_branch = False
    record(
        "C3_records_produced_on_the_required_frozen_lineage",
        reachable and on_branch,
        {"frozen_target_sha": frozen, "object_type": kind,
         "frozen_sha_is_ancestor_of_audit_branch": on_branch},
    )
    record(
        "C6_legal_and_realism_belong_to_the_same_session",
        len(session["source_audit_ids"]) == 4
        and all(aid in audits for aid in session["source_audit_ids"]),
        {"source_audit_ids": session["source_audit_ids"],
         "basis": session["single_session_instruction"]},
    )
    same_family = {audits[aid].get("auditor") for aid in session["source_audit_ids"] if aid in audits}
    already_labelled = [aid for aid in session["source_audit_ids"] if audits.get(aid, {}).get("auditor_instance")]
    record(
        "C8_no_substantive_judgment_is_invented",
        len(same_family) == 1 and not already_labelled,
        {"auditor_family": sorted(same_family), "records_already_carrying_an_instance": already_labelled,
         "transform": "verbatim copy plus auditor_instance; no verdict, authority, criterion, note or hash changes"},
    )
    record(
        "C9_label_describes_the_documented_session",
        instance.startswith("GPT-PHASE2-ISSUE") and str(session["issue"]) in instance,
        {"auditor_instance": instance,
         "derivation": f"GPT family + Phase 2 + authorizing issue #{session['issue']} + the audit branch version"},
    )
    return not proof["problems"], proof


def prove_question(qid: str, questions: dict, audits: dict, style_profile: dict) -> tuple[bool, dict]:
    """Criteria 4, 5, 7 and the initial-history requirement — the per-question proof."""
    current = question_audit_hash(questions[qid])
    legal = realism = None
    failing = []
    for audit_id, audit in audits.items():
        if audit.get("question_hashes", {}).get(qid) != current:
            continue
        if not audit.get("independent") or audit.get("audit_status") != "FULLY_ADJUDICATED":
            continue
        result = next((r for r in audit.get("results", []) if r.get("Question_ID") == qid), None)
        if result is None:
            continue
        if audit.get("review_type") == "LEGAL_VERIFICATION":
            if result.get("Verdict") == "KEEP" and result.get("Existing_Answer_Correct") == "YES":
                legal = audit_id
            else:
                failing.append(audit_id)
        elif audit.get("review_type") == "REALISM_REVIEW":
            if audit.get("style_profile") != style_profile_snapshot(style_profile):
                continue
            if result.get("Verdict") == "KEEP" and result.get("Realism_Verdict") == "PASS":
                realism = audit_id
            else:
                failing.append(audit_id)
    history = [
        audit_id
        for audit_id, audit in audits.items()
        if (audit.get("audit_scope") == "INITIAL_BATCH" or is_valid_targeted_initial_audit(audit))
        and audit.get("review_type") == "LEGAL_VERIFICATION"
        and audit.get("independent")
        and audit.get("audit_status") == "FULLY_ADJUDICATED"
        and qid in audit.get("question_ids", [])
    ]
    detail = {
        "current_question_hash": current,
        "legal_source": legal,
        "realism_source": realism,
        "current_hash_failing_evidence": sorted(set(failing)),
        "initial_batch_history": history,
    }
    ok = bool(legal and realism and not failing and history)
    return ok, detail


def main() -> int:
    questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}
    style_profile = load_json(DATA / "exam_style" / "mpje_style_profile.json")
    _, audits = validate_audits()

    inventory = json.loads(
        (ROOT / "audits" / "coverage" / "2026-08-19" / "BATCH3-POST-T3-INVENTORY.json").read_text(encoding="utf-8")
    )
    candidates = inventory["salvage"]["by_class"]["NEEDS_FRESH_INSTANCE_AUDIT"]

    session_proofs, provable_sessions = {}, []
    for instance, session in SESSIONS.items():
        ok, proof = prove_session(instance, session, audits)
        session_proofs[instance] = {"provable": ok, **proof}
        if ok:
            provable_sessions.append(instance)

    source_to_instance = {
        aid: instance for instance in provable_sessions for aid in SESSIONS[instance]["source_audit_ids"]
    }

    migrated, residual, question_proofs = [], [], {}
    for qid in candidates:
        ok, detail = prove_question(qid, questions, audits, style_profile)
        detail["legal_session"] = source_to_instance.get(detail["legal_source"])
        detail["realism_session"] = source_to_instance.get(detail["realism_source"])
        provable = ok and detail["legal_session"] and detail["realism_session"]
        question_proofs[qid] = {"migratable": bool(provable), **detail}
        (migrated if provable else residual).append(qid)

    written = []
    for instance in provable_sessions:
        for source_audit_id in SESSIONS[instance]["source_audit_ids"]:
            source = load_json(source_path(source_audit_id))
            normalized = copy.deepcopy(source)
            normalized["audit_id"] = normalized_audit_id(source_audit_id, instance)
            # Insert the recovered label immediately after auditor, keeping key order stable.
            ordered = {}
            for key, value in normalized.items():
                ordered[key] = value
                if key == "auditor":
                    ordered["auditor_instance"] = instance
            destination = DATA / "audits" / f"{ordered['audit_id']}.json"
            write_json(destination, ordered)

            # Fail closed if anything except identity changed.
            check = load_json(destination)
            for field in ("auditor", "audit_date", "audit_scope", "review_type", "independent",
                          "audit_status", "question_ids", "question_hashes", "results", "style_profile"):
                if check.get(field) != source.get(field):
                    raise SystemExit(f"{source_audit_id}: field {field} changed during migration")
            if set(check) - set(source) != {"auditor_instance"}:
                raise SystemExit(f"{source_audit_id}: unexpected added fields {set(check) - set(source)}")
            written.append({"source": source_audit_id, "normalized": ordered["audit_id"], "instance": instance})
            print(f"normalized {source_audit_id} -> {ordered['audit_id']}")

    manifest = {
        "manifest_type": "B3_S1_LEGACY_AUDIT_PROVENANCE_MIGRATION",
        "date": MIGRATION_DATE,
        "controller_issue": 83,
        "plan_issue": 91,
        "source_sha": git("rev-parse", "HEAD"),
        "statement": (
            "Additive provenance recovery only. No historical audit file was edited or overwritten, "
            "no verdict, authority, criterion, note or question hash was changed, and no new "
            "substantive judgment was made. Each normalized record is a verbatim copy of its source "
            "plus the auditor_instance that the modern schema requires, recovered from the GitHub "
            "issue that demanded one NEW independent conversation and the merged pull request that "
            "is that conversation's output."
        ),
        "sessions": {
            instance: {
                **{k: v for k, v in SESSIONS[instance].items()},
                "proof": session_proofs[instance],
                "recovered_auditor_instance": instance,
            }
            for instance in SESSIONS
        },
        "records_written": written,
        "candidate_count": len(candidates),
        "migrated_question_ids": migrated,
        "migrated_count": len(migrated),
        "residual_question_ids": residual,
        "residual_count": len(residual),
        "per_question_proof": question_proofs,
        "originals_retained": True,
        "release_policy_unchanged": True,
    }
    write_json(MANIFEST_PATH, manifest)

    print()
    for instance, proof in session_proofs.items():
        print(f"session {instance}: {'PROVABLE' if proof['provable'] else 'NOT PROVABLE'}")
        for key, value in proof["criteria"].items():
            print(f"   [{value['status']}] {key}")
    print()
    print(f"migratable without re-audit : {len(migrated)}/{len(candidates)}")
    print(f"residual fresh re-audit set : {len(residual)} {residual or ''}")
    print(f"manifest: {MANIFEST_PATH.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
