from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from qa_common import DATA, ROOT, load_json, load_records, question_audit_hash

SOURCE_SHA = "516771a93f939c843ba4c2be7ef745718606f448"
BASELINE_SHA = "beeb96d71768b9fb275bdb0005d9cd012e0d1328"
BASELINE_MATRIX_SHA = "b3a2e0d8b7b9f04b13ccfe0da2642948a7adf829"
DATE = "2026-08-18"
BASELINE_PATH = Path("/tmp/FINAL-PRE-BATCH3-COVERAGE-MATRIX.json")
OUT = ROOT / "audits" / "coverage" / DATE

REQUIRED_AREA = {1: 26, 2: 40, 3: 29, 4: 25}
EXPECTED_ATOMS = 46

# Explicit current-semantic confirmations used only for locked legacy-salvage/debt items.
# These do not introduce a new competency definition; they implement the prior gate's
# already-locked salvage/diversity plan using the current audited T1 presentations.
EXPLICIT_PROMOTIONS = {
    "2.1e": ["MA-Q-0032"],
    "2.4": ["MA-Q-0088"],
    "3.2": ["MA-Q-0030", "MA-Q-0036"],
    "3.3a": ["MA-Q-0085"],
    "4.2e": ["MA-Q-0059", "MA-Q-0060"],
    "4.4": ["MA-Q-0087"],
}

# These question presentations changed after the post-Batch2 matrix but were freshly
# audited on their current hashes. They may still be promoted only where the prior
# matrix already classified the same question as a direct legacy candidate, or where
# they are explicitly listed above.
CHANGED_T1_ALLOWED = {
    "MA-Q-0032", "MA-Q-0036", "MA-Q-0079", "MA-Q-0082", "MA-Q-0083", "MA-Q-0084"
}

KNOWN_TAXONOMY_FIXES = {
    "MA-Q-0085": 3,
    "MA-Q-0087": 4,
    "MA-Q-0088": 2,
}


def release_usable(q: dict) -> bool:
    return (
        q.get("verification_status") == "RELEASED"
        and q.get("lifecycle_status") == "RELEASED"
        and q.get("independent_audit_status") == "PASSED"
        and q.get("duplicate_review_status") == "CLEAR"
        and q.get("final_adjudication", {}).get("decision") == "KEEP"
    )


def dependency_record(record: dict, *, include_authority: bool) -> dict:
    out = {
        "content_version": record.get("content_version"),
        "content_hash": record.get("content_hash"),
    }
    if include_authority:
        for key in ("status", "verification_status", "authority"):
            if key in record:
                out[key] = record[key]
    return out


def refreshed_evidence(q: dict, rules: dict[str, dict], drugs: dict[str, dict]) -> dict:
    return {
        "question_id": q["question_id"],
        "family_id": q.get("family_id"),
        "current_area": q.get("area"),
        "topic": q.get("topic"),
        "subtopic": q.get("subtopic"),
        "question_hash": question_audit_hash(q),
        "verification_status": q.get("verification_status"),
        "lifecycle_status": q.get("lifecycle_status"),
        "independent_audit_status": q.get("independent_audit_status"),
        "duplicate_review_status": q.get("duplicate_review_status"),
        "final_decision": q.get("final_adjudication", {}).get("decision"),
        "rule_dependencies": {
            rid: dependency_record(rules[rid], include_authority=True)
            for rid in q.get("rule_ids", [])
        },
        "drug_dependencies": {
            did: dependency_record(drugs[did], include_authority=False)
            for did in q.get("drug_ids", [])
        },
    }


def headline_id(atom: str) -> str:
    return re.sub(r"[a-z]$", "", atom)


def write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    if not BASELINE_PATH.exists():
        raise SystemExit(f"missing baseline matrix: {BASELINE_PATH}")
    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    if baseline.get("post_batch2_source_sha") != BASELINE_SHA:
        raise SystemExit("baseline matrix source SHA mismatch")
    if baseline.get("atomic_count") != EXPECTED_ATOMS or len(baseline.get("rows", [])) != EXPECTED_ATOMS:
        raise SystemExit("baseline matrix atomic-count mismatch")

    questions = {q["question_id"]: q for _, q in load_records(DATA / "questions")}
    rules = {r["rule_id"]: r for _, r in load_records(DATA / "rules")}
    drugs = {d["drug_id"]: d for _, d in load_records(DATA / "drugs")}

    # Current release-usable bank and area capacity.
    released = {qid: q for qid, q in questions.items() if release_usable(q)}
    area_counts = Counter(int(q["area"]) for q in released.values())
    area_deficits = {area: max(0, need - area_counts.get(area, 0)) for area, need in REQUIRED_AREA.items()}

    # Known taxonomy mismatches from Issue #40 must now be corrected exactly.
    taxonomy_fixes = {}
    for qid, expected_area in KNOWN_TAXONOMY_FIXES.items():
        q = questions[qid]
        taxonomy_fixes[qid] = {
            "expected_nabp_area": expected_area,
            "current_area": q.get("area"),
            "resolved": q.get("area") == expected_area,
            "release_usable": release_usable(q),
            "question_hash": question_audit_hash(q),
        }
    unresolved_taxonomy = sorted(qid for qid, rec in taxonomy_fixes.items() if not rec["resolved"])

    updated_rows = []
    promotion_log = []
    for old_row in baseline["rows"]:
        row = json.loads(json.dumps(old_row))
        atom = row["atomic_id"]
        selected_by_id: dict[str, dict] = {}

        # Baseline selected evidence must remain current and unchanged in meaning/hash.
        for old_ev in old_row.get("selected_release_evidence", []):
            qid = old_ev["question_id"]
            q = questions[qid]
            if not release_usable(q):
                raise SystemExit(f"baseline selected evidence is no longer release-usable: {atom} {qid}")
            current_hash = question_audit_hash(q)
            if current_hash != old_ev.get("question_hash"):
                raise SystemExit(f"baseline selected evidence hash drift: {atom} {qid}")
            selected_by_id[qid] = refreshed_evidence(q, rules, drugs)

        # Promote only candidates that the previous final matrix had already manually
        # classified as direct semantic legacy salvage evidence and that are now fully released.
        old_candidates = {ev["question_id"]: ev for ev in old_row.get("legacy_salvage_candidates", [])}
        for qid, old_ev in old_candidates.items():
            q = questions[qid]
            if not release_usable(q):
                continue
            old_hash = old_ev.get("question_hash")
            current_hash = question_audit_hash(q)
            if old_hash != current_hash and qid not in CHANGED_T1_ALLOWED:
                raise SystemExit(f"legacy candidate changed without explicit semantic allowance: {atom} {qid}")
            selected_by_id[qid] = refreshed_evidence(q, rules, drugs)
            promotion_log.append({
                "atomic_id": atom,
                "question_id": qid,
                "basis": "prior_final_matrix_direct_legacy_candidate_now_release_usable",
                "old_hash": old_hash,
                "current_hash": current_hash,
            })

        # Explicit locked remediation-plan mappings verified against current audited stems.
        for qid in EXPLICIT_PROMOTIONS.get(atom, []):
            q = questions[qid]
            if not release_usable(q):
                raise SystemExit(f"explicit promotion is not release-usable: {atom} {qid}")
            selected_by_id[qid] = refreshed_evidence(q, rules, drugs)
            promotion_log.append({
                "atomic_id": atom,
                "question_id": qid,
                "basis": "locked_post_batch2_remediation_plan_plus_current_semantic_confirmation",
                "current_hash": question_audit_hash(q),
            })

        selected = list(selected_by_id.values())
        row["selected_release_evidence"] = selected
        row["direct_release_usable_count"] = len(selected)
        row["legacy_salvage_candidates"] = [
            refreshed_evidence(questions[ev["question_id"]], rules, drugs)
            for ev in old_row.get("legacy_salvage_candidates", [])
            if not release_usable(questions[ev["question_id"]])
        ]

        if selected:
            if any(int(ev.get("current_area")) == int(row["nabp_area"]) for ev in selected):
                row["semantic_status"] = "PASS_DIRECT"
            else:
                row["semantic_status"] = "PASS_FORMAL_MAP"
            if old_row.get("semantic_status", "").startswith("FAIL"):
                row["post_t1_change"] = "PROMOTED_TO_PASS_AFTER_GUARDED_T1_RELEASE"
        else:
            # A no-evidence row may not magically pass. Preserve the prior manual semantic classification.
            row["semantic_status"] = old_row["semantic_status"]

        updated_rows.append(row)

    failed_rows = [r for r in updated_rows if r["direct_release_usable_count"] < 1]
    failed_atoms = [r["atomic_id"] for r in failed_rows]

    # Recompute headline diversity on the updated selected evidence.
    rows_by_headline: dict[str, list[dict]] = {}
    for row in updated_rows:
        rows_by_headline.setdefault(headline_id(row["atomic_id"]), []).append(row)

    old_headline = {h["headline"]: h for h in baseline.get("headline_family_diversity", [])}
    headline_results = []
    diversity_debts = []
    for head, rows in sorted(rows_by_headline.items(), key=lambda kv: [int(x) for x in kv[0].split(".")]):
        families = sorted({
            ev["family_id"]
            for row in rows
            for ev in row.get("selected_release_evidence", [])
            if ev.get("family_id")
        })
        atomic_failed = any(row["direct_release_usable_count"] < 1 for row in rows)
        prior_exception = old_headline.get(head, {}).get("exception_justification")
        if atomic_failed:
            status = "FAIL_ATOMIC_COVERAGE"
        elif len(families) >= 2:
            status = "PASS_TWO_PLUS_FAMILIES"
        elif prior_exception:
            status = "PASS_NARROW_EXCEPTION"
        else:
            status = "FAIL_FAMILY_DIVERSITY"
            diversity_debts.append(head)
        headline_results.append({
            "headline": head,
            "atomic_ids": [r["atomic_id"] for r in rows],
            "distinct_selected_families": families,
            "family_count": len(families),
            "status": status,
            "exception_justification": prior_exception,
        })

    capacity_pass = all(v == 0 for v in area_deficits.values())
    atom_pass = not failed_atoms
    diversity_pass = not diversity_debts
    taxonomy_pass = not unresolved_taxonomy
    gate_pass = atom_pass and capacity_pass and diversity_pass and taxonomy_pass

    # Expected post-T1 locked salvage outcome sanity checks.
    expected_promoted = {"2.1e", "2.4", "3.3a", "4.2e", "4.4"}
    baseline_failed = set(baseline["failed_atomic_ids"])
    now_passed_from_baseline_fail = baseline_failed - set(failed_atoms)
    if now_passed_from_baseline_fail != expected_promoted:
        raise SystemExit(
            f"unexpected baseline-fail promotion set: {sorted(now_passed_from_baseline_fail)}; "
            f"expected {sorted(expected_promoted)}"
        )
    expected_remaining = {
        "1.2b", "1.2c", "2.3b", "4.2c", "4.3", "4.5a", "4.5b", "4.5c",
        "4.5d", "4.6", "4.7b", "4.7c", "4.7d",
    }
    if set(failed_atoms) != expected_remaining:
        raise SystemExit(f"unexpected residual atomic gaps: {sorted(failed_atoms)}")

    matrix = {
        "gate": "PRE_BATCH3_FULL_COMPETENCY_COVERAGE_DEBT_POST_T1",
        "verdict": "PASS" if gate_pass else "FAIL",
        "batch3": "UNLOCKED" if gate_pass else "BLOCKED",
        "audit_date": DATE,
        "post_t1_source_sha": SOURCE_SHA,
        "baseline_post_batch2_source_sha": BASELINE_SHA,
        "baseline_final_matrix_commit": BASELINE_MATRIX_SHA,
        "nabp_competency_source": baseline.get("nabp_competency_source"),
        "nabp_profile": baseline.get("nabp_profile"),
        "atomic_count": EXPECTED_ATOMS,
        "atomic_pass_count": EXPECTED_ATOMS - len(failed_atoms),
        "atomic_fail_count": len(failed_atoms),
        "failed_atomic_ids": failed_atoms,
        "promoted_atomic_ids_from_t1": sorted(now_passed_from_baseline_fail),
        "rows": updated_rows,
        "headline_family_diversity": headline_results,
        "headline_family_diversity_debts": diversity_debts,
        "taxonomy_fixes": taxonomy_fixes,
        "unresolved_known_taxonomy_mismatches": unresolved_taxonomy,
        "release_usable_capacity": {
            "total": len(released),
            "area_counts": {str(a): area_counts.get(a, 0) for a in range(1, 5)},
            "required_120_mock": {str(a): REQUIRED_AREA[a] for a in range(1, 5)},
            "deficits": {str(a): area_deficits[a] for a in range(1, 5)},
            "blueprint_faithful_mock_without_reuse": capacity_pass,
        },
        "promotion_log": promotion_log,
        "methodology": {
            "semantic_baseline": "Final post-Batch2 46-row manual matrix at b3a2e0d8...",
            "promotion_rule": "Promote only prior direct legacy candidates that are now release-usable, plus explicit mappings locked by prior remediation plan and confirmed against current audited T1 semantics.",
            "baseline_selected_evidence_hash_drift_allowed": False,
            "current_release_usable_definition": "RELEASED lifecycle+verification, PASSED independent audit, CLEAR duplicate review, final KEEP adjudication",
            "headline_family_default_minimum": 2,
        },
    }

    gate_fail_reasons = []
    if failed_atoms:
        gate_fail_reasons.append(f"{len(failed_atoms)} of 46 atomic competencies lack qualifying direct release-usable coverage")
    for area, deficit in area_deficits.items():
        if deficit:
            gate_fail_reasons.append(
                f"Area {area} release-usable count {area_counts.get(area,0)} is below required {REQUIRED_AREA[area]} by {deficit}"
            )
    for head in diversity_debts:
        gate_fail_reasons.append(f"headline family-diversity debt: {head}")
    if unresolved_taxonomy:
        gate_fail_reasons.append(f"unresolved known taxonomy mismatches: {', '.join(unresolved_taxonomy)}")
    matrix["gate_fail_reasons"] = gate_fail_reasons

    plan = {
        "gate_source_sha": SOURCE_SHA,
        "gate_verdict": matrix["verdict"],
        "batch3": matrix["batch3"],
        "completed_legacy_salvage": {
            "t1_admitted": 29,
            "t1_quarantined": ["MA-Q-0028"],
            "area_1_legacy_priority_released": 6,
            "area_2_legacy_priority_released": 16,
            "atomic_gaps_closed": sorted(now_passed_from_baseline_fail),
            "transfer_family_diversity_candidate_families_added": [
                "P2_0030_FED_EPCS_TRANSFER", "P2_0036_FED_EPCS_TRANSFER_REFILLS"
            ],
        },
        "remaining_atomic_gaps": failed_atoms,
        "remaining_atomic_gaps_by_area": {
            str(area): [r["atomic_id"] for r in failed_rows if int(r["nabp_area"]) == area]
            for area in range(1,5)
        },
        "remaining_mock_capacity_deficits": {str(a): area_deficits[a] for a in range(1,5)},
        "remaining_headline_family_diversity_debts": diversity_debts,
        "known_taxonomy_fixes_resolved": not unresolved_taxonomy,
        "next_locked_action": (
            "Targeted pre-Batch3 coverage-remediation authoring for residual direct semantic gaps, "
            "Area-1/Area-2 capacity deficits, and any remaining headline family-diversity debt; "
            "then the same freeze/audit/adjudication/release process and another full gate rerun."
        ),
        "authoring_floor": {
            "area_1_new_questions_minimum_for_capacity": area_deficits[1],
            "area_2_new_questions_minimum_for_capacity": area_deficits[2],
            "note": "Capacity minima are lower bounds, not a total authoring quota. Residual semantic and family-diversity gaps may require additional distinct questions."
        },
    }

    md = [
        "# Post-T1 Pre-Batch3 Competency Coverage Gate",
        "",
        f"- Exact post-T1 canonical remediation SHA: `{SOURCE_SHA}`",
        f"- Baseline final post-Batch2 matrix: `{BASELINE_MATRIX_SHA}` / source `{BASELINE_SHA}`",
        f"- Verdict: **{matrix['verdict']} — Batch 3 {'may unlock' if gate_pass else 'remains blocked'}**",
        f"- Atomic competency result: **{matrix['atomic_pass_count']}/46 PASS; {matrix['atomic_fail_count']}/46 FAIL**",
        f"- Failed atoms: {', '.join(failed_atoms) if failed_atoms else 'none'}",
        f"- Release-usable bank: **{len(released)}**",
        f"- Area counts: **{area_counts.get(1,0)} / {area_counts.get(2,0)} / {area_counts.get(3,0)} / {area_counts.get(4,0)}**",
        f"- Required mock allocation: **26 / 40 / 29 / 25**",
        f"- Capacity deficits: **{area_deficits[1]} / {area_deficits[2]} / {area_deficits[3]} / {area_deficits[4]}**",
        f"- Headline family-diversity debt: **{', '.join(diversity_debts) if diversity_debts else 'none'}**",
        f"- Known Q0085/Q0087/Q0088 taxonomy mismatches: **{'RESOLVED' if not unresolved_taxonomy else 'UNRESOLVED'}**",
        "",
        "## What T1 closed",
        "",
        "The guarded T1 release converts five previously failed atomic competencies from non-release-usable legacy evidence to direct current-hash audited release evidence:",
        "",
        "- `2.1e` — practitioner refill-authorization limits: Q0032",
        "- `2.4` — returning/reusing drugs: Q0088",
        "- `3.3a` — prospective DUR: Q0085",
        "- `4.2e` — controlled-substance inventories: Q0059/Q0060",
        "- `4.4` — product selection/interchange: Q0087",
        "",
        "The prior 3.2 transfer family-diversity debt is also re-evaluated with released Q0030 and Q0036 as distinct transfer families.",
        "",
        "## Remaining atomic gaps",
        "",
    ]
    for row in failed_rows:
        md.append(f"- **{row['atomic_id']} — {row['label']}**: {row['semantic_status']}. {row.get('rationale','')}")
    md += [
        "",
        "## Capacity consequence",
        "",
        f"After T1, Area 1 has {area_counts.get(1,0)} release-usable questions vs 26 required, and Area 2 has {area_counts.get(2,0)} vs 40 required. At least {area_deficits[1]} additional Area-1 and {area_deficits[2]} additional Area-2 questions are therefore still required for one 120-question blueprint-faithful mock, even before semantic/family-diversity constraints are considered.",
        "",
        "## Next locked action",
        "",
        "Legacy-first T1 salvage is complete. The next tranche may now be targeted pre-Batch3 coverage remediation: author only residual direct semantic gaps, capacity deficits, and unresolved family-diversity needs; freeze/hash; fresh independent legal + realism audit; adjudicate/release; rerun this full gate. Batch 3 stays blocked until the gate passes.",
        "",
    ]

    OUT.mkdir(parents=True, exist_ok=True)
    write_json(OUT / "POST-T1-PRE-BATCH3-COVERAGE-MATRIX.json", matrix)
    write_json(OUT / "POST-T1-PRE-BATCH3-REMEDIATION-PLAN.json", plan)
    (OUT / "POST-T1-PRE-BATCH3-COVERAGE-DEBT.md").write_text("\n".join(md), encoding="utf-8")

    print(f"post-T1 coverage gate: {matrix['verdict']}")
    print(f"atomic={matrix['atomic_pass_count']}/46 pass; failures={','.join(failed_atoms)}")
    print(f"released={len(released)} area_counts={dict(sorted(area_counts.items()))} deficits={area_deficits}")
    print(f"diversity_debts={diversity_debts}")
    print(f"taxonomy_unresolved={unresolved_taxonomy}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
