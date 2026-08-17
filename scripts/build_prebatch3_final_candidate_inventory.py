from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from qa_common import DATA, ROOT, dependency_snapshot, load_json, load_records, question_audit_hash, write_json

POST_BATCH2_SHA = "beeb96d71768b9fb275bdb0005d9cd012e0d1328"
PRELIMINARY_HEAD = "b459aa8cc554e000077e5acadd8a05217dc1731f"
PROXY_PATH = Path("/tmp/PRE-BATCH3-ATOMIC-COVERAGE-PROXY.json")
OUT_DIR = ROOT / "audits" / "coverage" / "2026-08-17"
TARGET_ALLOCATION = {1: 26, 2: 40, 3: 29, 4: 25}


def main() -> int:
    if not PROXY_PATH.exists():
        raise RuntimeError("missing exact preliminary proxy staged by workflow")
    proxy = json.loads(PROXY_PATH.read_text(encoding="utf-8"))
    if proxy.get("atomic_count") != 46:
        raise RuntimeError("expected 46 atomic competencies")

    questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}
    rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}
    drugs = {record["drug_id"]: record for _, record in load_records(DATA / "drugs")}

    rows = []
    for row in proxy["rows"]:
        candidates = []
        for candidate in row.get("candidate_questions", []):
            qid = candidate["question_id"]
            q = questions.get(qid)
            if q is None:
                candidates.append({**candidate, "current_status": "MISSING"})
                continue
            release_usable = q.get("verification_status") == "RELEASED" and q.get("lifecycle_status") == "RELEASED"
            candidates.append(
                {
                    **candidate,
                    "current_area": q.get("area"),
                    "question_hash": question_audit_hash(q),
                    "verification_status": q.get("verification_status"),
                    "lifecycle_status": q.get("lifecycle_status"),
                    "duplicate_review_status": q.get("duplicate_review_status"),
                    "independent_audit_status": q.get("independent_audit_status"),
                    "final_decision": (q.get("final_adjudication") or {}).get("decision"),
                    "release_usable": release_usable,
                    "rule_snapshots": {
                        rid: dependency_snapshot(rules[rid]) for rid in q.get("rule_ids", []) if rid in rules
                    },
                    "drug_snapshots": {
                        did: dependency_snapshot(drugs[did]) for did in q.get("drug_ids", []) if did in drugs
                    },
                }
            )
        rows.append(
            {
                "atomic_id": row["atomic_id"],
                "area": row["area"],
                "label": row["label"],
                "preliminary_proxy_status": row["proxy_status"],
                "candidate_count": len(candidates),
                "release_usable_candidate_count": sum(1 for c in candidates if c.get("release_usable")),
                "candidate_questions": candidates,
            }
        )

    area_all = Counter()
    area_released = Counter()
    released_ids = []
    for q in questions.values():
        area_all[q["area"]] += 1
        if q.get("verification_status") == "RELEASED" and q.get("lifecycle_status") == "RELEASED":
            area_released[q["area"]] += 1
            released_ids.append(q["question_id"])

    capacity = {
        "source_sha": POST_BATCH2_SHA,
        "target_question_count": 120,
        "required_area_allocation": {str(k): v for k, v in TARGET_ALLOCATION.items()},
        "canonical_counts_by_area": {str(a): area_all[a] for a in range(1, 5)},
        "release_usable_counts_by_area": {str(a): area_released[a] for a in range(1, 5)},
        "release_usable_total": len(released_ids),
        "deficit_by_area": {str(a): max(0, TARGET_ALLOCATION[a] - area_released[a]) for a in range(1, 5)},
        "blueprint_faithful_mock_without_reuse": all(area_released[a] >= TARGET_ALLOCATION[a] for a in range(1, 5)),
        "released_question_ids": sorted(released_ids),
    }

    inventory = {
        "status": "MACHINE_CANDIDATE_INVENTORY_NOT_SEMANTIC_ADJUDICATION",
        "post_batch2_source_sha": POST_BATCH2_SHA,
        "preliminary_proxy_source_sha": PRELIMINARY_HEAD,
        "atomic_count": len(rows),
        "method": (
            "Carries forward only candidate-discovery rows from the exact preliminary proxy, then refreshes each "
            "candidate against the exact post-Batch2 question state, current audit hash, lifecycle maturity, and "
            "direct rule/drug dependency snapshots. Candidate presence does not itself establish semantic coverage."
        ),
        "rows": rows,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUT_DIR / "FINAL-PRE-BATCH3-CANDIDATE-MATURITY.json", inventory)
    write_json(OUT_DIR / "FINAL-PRE-BATCH3-MOCK-CAPACITY.json", capacity)

    print(
        "post-Batch2 candidate inventory built: "
        f"atomic={len(rows)} released={len(released_ids)} "
        f"areas={dict(sorted(area_released.items()))} "
        f"deficits={capacity['deficit_by_area']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
