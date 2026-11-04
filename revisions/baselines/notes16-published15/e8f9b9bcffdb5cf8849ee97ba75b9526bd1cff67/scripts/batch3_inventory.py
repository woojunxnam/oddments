"""Measure the exact post-T3 bank state that Batch 3 must be planned against.

Issue #83 Phase G. Nothing here is estimated: every number is computed from the current
canonical tree, and unreleased candidates are only counted as usable capacity if they
actually carry current-hash release-qualifying evidence.
"""

from __future__ import annotations

import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, ROOT, load_json, load_records, question_audit_hash, write_json
from release_context import style_profile_snapshot
from validate_audits import validate_audits


# Three non-overlapping blueprint-faithful 120-question mocks.
MOCK_ALLOCATION = {1: 26, 2: 40, 3: 29, 4: 25}
TARGET_SETS = 3
TARGET_TOTAL = 360
QUARANTINED_ID = "MA-Q-0028"


def released(question: dict) -> bool:
    return question.get("verification_status") == "RELEASED" and question.get("lifecycle_status") == "RELEASED"


def main() -> int:
    questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}
    style_profile = load_json(DATA / "exam_style" / "mpje_style_profile.json")
    _, audits = validate_audits()
    matrix = load_json(DATA / "exam_style" / "question_family_matrix.json")

    released_ids = sorted(qid for qid, q in questions.items() if released(q))
    unreleased_ids = sorted(qid for qid in questions if qid not in set(released_ids))

    released_by_area = Counter(questions[qid]["area"] for qid in released_ids)
    unreleased_by_area = Counter(questions[qid]["area"] for qid in unreleased_ids)

    # Which unreleased candidates could actually be released today? Passing current-hash
    # evidence is not sufficient on its own: release_requirements uses AUDITOR_INSTANCE
    # distinctness, and the legacy Phase-2 audit records predate the auditor_instance
    # field, so evidence that "passes" can still fail the real release gate.
    instanceless_audits = {aid for aid, a in audits.items() if not a.get("auditor_instance")}
    salvage_ready, salvage_blocked = [], {}
    salvage_class: dict[str, str] = {}
    for qid in unreleased_ids:
        if qid == QUARANTINED_ID:
            salvage_blocked[qid] = "quarantined"
            salvage_class[qid] = "QUARANTINED"
            continue
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
        if failing:
            salvage_blocked[qid] = f"current-hash failing evidence: {sorted(set(failing))}"
            salvage_class[qid] = "NEEDS_REPAIR_AND_REAUDIT"
        elif legal and realism:
            if legal in instanceless_audits or realism in instanceless_audits:
                salvage_blocked[qid] = (
                    "current-hash evidence passes but comes from instance-less legacy audits "
                    f"({sorted({legal, realism} & instanceless_audits)}); the AUDITOR_INSTANCE "
                    "release policy rejects it"
                )
                salvage_class[qid] = "NEEDS_FRESH_INSTANCE_AUDIT"
            else:
                salvage_ready.append(qid)
                salvage_class[qid] = "RELEASABLE_NOW"
        else:
            missing = [k for k, v in (("legal", legal), ("realism", realism)) if not v]
            salvage_blocked[qid] = f"no current-hash {'/'.join(missing)} evidence"
            salvage_class[qid] = "NEEDS_FRESH_AUDIT"

    required = {area: count * TARGET_SETS for area, count in MOCK_ALLOCATION.items()}
    deficit = {area: max(0, required[area] - released_by_area.get(area, 0)) for area in MOCK_ALLOCATION}

    # Salvage can only help the area a candidate already sits in.
    salvage_by_area = Counter(questions[qid]["area"] for qid in salvage_ready)
    salvage_pool_by_area = Counter(
        questions[qid]["area"] for qid in unreleased_ids if qid != QUARANTINED_ID
    )
    new_authoring_needed_if_all_salvage_lands = {
        area: max(0, deficit[area] - salvage_pool_by_area.get(area, 0)) for area in MOCK_ALLOCATION
    }

    families = {f["family_id"]: f for f in matrix["families"]}
    released_family_counts = Counter(questions[qid]["family_id"] for qid in released_ids)
    saturated = {
        fid: {"released": released_family_counts[fid], "max": families[fid]["max_questions_in_final_bank"]}
        for fid in released_family_counts
        if fid in families and released_family_counts[fid] >= families[fid]["max_questions_in_final_bank"]
    }
    headroom_in_existing_families = sum(
        max(0, families[fid]["max_questions_in_final_bank"] - released_family_counts.get(fid, 0))
        for fid in families
    )

    numeric_ids = sorted(int(qid.split("-")[-1]) for qid in questions)
    gaps = [n for n in range(1, max(numeric_ids) + 1) if n not in set(numeric_ids)]

    type_dist = Counter(questions[qid]["question_type"] for qid in released_ids)
    difficulty_dist = Counter(questions[qid]["difficulty"] for qid in released_ids)
    drug_backed = sum(1 for qid in released_ids if questions[qid].get("drug_ids"))

    report = {
        "report_type": "BATCH3_POST_T3_INVENTORY",
        "controller_issue": 83,
        "source_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "objective": {
            "target_total_release_usable": TARGET_TOTAL,
            "target_sets": TARGET_SETS,
            "per_set_allocation": {str(k): v for k, v in MOCK_ALLOCATION.items()},
            "required_by_area": {str(k): v for k, v in required.items()},
        },
        "bank": {
            "total_canonical_questions": len(questions),
            "released": len(released_ids),
            "unreleased": len(unreleased_ids),
            "quarantined": [QUARANTINED_ID],
            "highest_used_question_id": f"MA-Q-{max(numeric_ids):04d}",
            "id_gaps": gaps,
            "next_free_question_id": f"MA-Q-{max(numeric_ids) + 1:04d}",
        },
        "released_by_area": {str(k): released_by_area.get(k, 0) for k in sorted(MOCK_ALLOCATION)},
        "unreleased_by_area": {str(k): unreleased_by_area.get(k, 0) for k in sorted(MOCK_ALLOCATION)},
        "deficit_to_three_sets_by_area": {str(k): v for k, v in deficit.items()},
        "deficit_total": sum(deficit.values()),
        "salvage": {
            "unreleased_excluding_quarantine": len(unreleased_ids) - 1,
            "releasable_today": salvage_ready,
            "releasable_today_count": len(salvage_ready),
            "release_ready_by_area": {str(k): v for k, v in sorted(salvage_by_area.items())},
            "salvage_pool_by_area": {str(k): v for k, v in sorted(salvage_pool_by_area.items())},
            "classification_counts": dict(Counter(salvage_class.values())),
            "classification_by_area": {
                cls: dict(Counter(questions[q]["area"] for q, c in salvage_class.items() if c == cls))
                for cls in sorted(set(salvage_class.values()))
            },
            "by_class": {
                cls: sorted(q for q, c in salvage_class.items() if c == cls)
                for cls in sorted(set(salvage_class.values()))
            },
            "instanceless_legacy_audits": sorted(instanceless_audits),
            "note": (
                "Passing current-hash evidence is not release capacity on its own. "
                "data/release_requirements.json uses distinctness_basis AUDITOR_INSTANCE, and the "
                "legacy Phase-2 audit records carry no auditor_instance, so questions resting only on "
                "them fail the real release gate with 'lacks auditor_instance required by release policy'."
            ),
        },
        "new_authoring_needed_if_every_salvage_candidate_landed": {
            str(k): v for k, v in new_authoring_needed_if_all_salvage_lands.items()
        },
        "new_authoring_needed_total_if_no_salvage": sum(deficit.values()),
        "new_authoring_needed_total_if_all_salvage": sum(new_authoring_needed_if_all_salvage_lands.values()),
        "family_state": {
            "families_in_matrix": len(families),
            "families_with_released_questions": len(released_family_counts),
            "saturated_families": saturated,
            "saturated_family_count": len(saturated),
            "headroom_in_existing_families": headroom_in_existing_families,
        },
        "released_distributions": {
            "question_type": dict(type_dist),
            "difficulty": {str(k): v for k, v in sorted(difficulty_dist.items())},
            "drug_backed": drug_backed,
            "non_drug": len(released_ids) - drug_backed,
        },
    }
    output = ROOT / "audits" / "coverage" / "2026-08-19" / "BATCH3-POST-T3-INVENTORY.json"
    write_json(output, report)

    print(f"source SHA                : {report['source_sha']}")
    print(f"canonical / released      : {report['bank']['total_canonical_questions']} / {report['bank']['released']}")
    print(f"highest QID / next free   : {report['bank']['highest_used_question_id']} / {report['bank']['next_free_question_id']}  gaps={gaps or 'none'}")
    print(f"released by area          : {report['released_by_area']}")
    print(f"required for 3 sets       : {report['objective']['required_by_area']}")
    print(f"deficit by area           : {report['deficit_to_three_sets_by_area']}  total={report['deficit_total']}")
    print(f"unreleased by area        : {report['unreleased_by_area']}")
    print(f"releasable TODAY          : {len(salvage_ready)}")
    print(f"salvage classification    : {report['salvage']['classification_counts']}")
    print(f"  by area                 : {report['salvage']['classification_by_area']}")
    print(f"salvage pool by area      : {report['salvage']['salvage_pool_by_area']}")
    print(f"new authoring if ALL salvage lands: {report['new_authoring_needed_if_every_salvage_candidate_landed']} total={report['new_authoring_needed_total_if_all_salvage']}")
    print(f"new authoring if NO salvage      : total={report['new_authoring_needed_total_if_no_salvage']}")
    print(f"saturated families        : {report['family_state']['saturated_family_count']}")
    print(f"released types/difficulty : {report['released_distributions']['question_type']} / {report['released_distributions']['difficulty']}")
    print(f"report: {output.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
