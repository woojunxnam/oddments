from __future__ import annotations

from collections import Counter

from qa_common import DATA, ROOT, dependency_snapshot, load_json, load_records, question_audit_hash, write_json

BASE_SHA = "beeb96d71768b9fb275bdb0005d9cd012e0d1328"
AREA1 = ["MA-Q-0075", "MA-Q-0076", "MA-Q-0077", "MA-Q-0078", "MA-Q-0079", "MA-Q-0080"]
AREA2 = [
    "MA-Q-0004", "MA-Q-0009", "MA-Q-0013", "MA-Q-0015", "MA-Q-0016", "MA-Q-0017",
    "MA-Q-0020", "MA-Q-0027", "MA-Q-0034", "MA-Q-0040", "MA-Q-0081", "MA-Q-0082",
    "MA-Q-0083", "MA-Q-0084", "MA-Q-0085", "MA-Q-0086",
]
SEMANTIC_EXTRA = [
    "MA-Q-0028", "MA-Q-0030", "MA-Q-0032", "MA-Q-0036",
    "MA-Q-0059", "MA-Q-0060", "MA-Q-0087", "MA-Q-0088",
]
T1 = AREA1 + AREA2 + SEMANTIC_EXTRA
GAP_TARGETS = {
    "2.1e": ["MA-Q-0028", "MA-Q-0032"],
    "2.4": ["MA-Q-0088"],
    "3.2_diversity": ["MA-Q-0030", "MA-Q-0036"],
    "3.3a": ["MA-Q-0085"],
    "4.2e": ["MA-Q-0059", "MA-Q-0060"],
    "4.4": ["MA-Q-0087"],
}


def main() -> int:
    if len(T1) != 30 or len(set(T1)) != 30:
        raise RuntimeError("Tranche 1 must contain exactly 30 unique legacy questions")

    questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}
    rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}
    drugs = {record["drug_id"]: record for _, record in load_records(DATA / "drugs")}
    family_matrix = load_json(DATA / "exam_style" / "question_family_matrix.json")
    family_by_id = {f["family_id"]: f for f in family_matrix.get("families", [])}

    released_family_counts = Counter()
    for q in questions.values():
        if q.get("verification_status") == "RELEASED" and q.get("lifecycle_status") == "RELEASED":
            released_family_counts[q["family_id"]] += 1

    records = []
    all_rule_ids: set[str] = set()
    all_drug_ids: set[str] = set()
    for qid in T1:
        q = questions[qid]
        if int(qid[-4:]) > 90:
            raise RuntimeError(f"non-legacy question in T1: {qid}")
        if q.get("verification_status") == "RELEASED" or q.get("lifecycle_status") == "RELEASED":
            raise RuntimeError(f"T1 question unexpectedly already released: {qid}")
        rule_ids = list(q.get("rule_ids", []))
        drug_ids = list(q.get("drug_ids", []))
        all_rule_ids.update(rule_ids)
        all_drug_ids.update(drug_ids)
        family = family_by_id.get(q["family_id"])
        records.append({
            "question_id": qid,
            "priority_group": (
                "AREA1_CAPACITY" if qid in AREA1 else
                "AREA2_CAPACITY" if qid in AREA2 else
                "SEMANTIC_GAP_OR_DIVERSITY"
            ),
            "area": q["area"],
            "family_id": q["family_id"],
            "topic": q["topic"],
            "subtopic": q["subtopic"],
            "difficulty": q["difficulty"],
            "question_type": q["question_type"],
            "question_hash": question_audit_hash(q),
            "verification_status": q["verification_status"],
            "lifecycle_status": q["lifecycle_status"],
            "last_legal_review": q.get("last_legal_review"),
            "duplicate_review_status": q.get("duplicate_review_status"),
            "independent_audit_status": q.get("independent_audit_status"),
            "current_key": q.get("correct_choice_ids"),
            "stem": q["stem"],
            "choices": q["choices"],
            "rule_ids": rule_ids,
            "drug_ids": drug_ids,
            "family_release_state": {
                "current_released_count": released_family_counts[q["family_id"]],
                "max_questions_in_final_bank": family.get("max_questions_in_final_bank") if family else None,
                "matrix_known": family is not None,
            },
        })

    rule_dependencies = {}
    for rid in sorted(all_rule_ids):
        rule = rules.get(rid)
        if rule is None:
            rule_dependencies[rid] = {"missing": True}
            continue
        rule_dependencies[rid] = {
            **dependency_snapshot(rule),
            "title": rule.get("title"),
            "status": rule.get("status"),
            "verification_status": rule.get("verification_status"),
            "last_verified": rule.get("last_verified"),
            "authority": rule.get("authority", []),
            "rule_summary": rule.get("rule_summary"),
        }

    drug_dependencies = {}
    for did in sorted(all_drug_ids):
        drug = drugs.get(did)
        if drug is None:
            drug_dependencies[did] = {"missing": True}
            continue
        drug_dependencies[did] = {
            **dependency_snapshot(drug),
            "generic_name": drug.get("generic_name"),
            "brand_names": drug.get("brand_names", []),
            "federal_schedule": drug.get("federal_schedule"),
            "ma_schedule": drug.get("ma_schedule"),
            "verification_status": drug.get("verification_status"),
            "last_verified": drug.get("last_verified"),
            "authority": drug.get("authority", []),
        }

    inventory = {
        "program": "PRE_BATCH3_COVERAGE_REMEDIATION",
        "tranche": "LEGACY_SALVAGE_T1",
        "base_post_batch2_sha": BASE_SHA,
        "question_count": len(records),
        "question_ids": T1,
        "area1_capacity_ids": AREA1,
        "area2_capacity_ids": AREA2,
        "semantic_gap_or_diversity_ids": SEMANTIC_EXTRA,
        "gap_target_map": GAP_TARGETS,
        "questions": records,
        "rule_dependencies": rule_dependencies,
        "drug_dependencies": drug_dependencies,
        "next_contract": {
            "phase": "CURRENT_LAW_AND_REALISM_EDITOR_REVIEW",
            "instructions": [
                "Independently solve each item before trusting its current key or explanation.",
                "Use current official Massachusetts/federal sources only for legal repair decisions.",
                "Review every option independently, including all SATA choices.",
                "Repair only where needed; do not promote lifecycle/verification status during editor review.",
                "Check semantic distinctness against the full current canonical bank before freezing.",
                "After editor review, freeze exact repaired hashes and dependency snapshots for a fresh independent legal + realism audit."
            ],
        },
    }
    out = ROOT / "audits" / "remediation" / "2026-08-17" / "T1-LEGACY-SALVAGE-INVENTORY.json"
    write_json(out, inventory)
    print(
        f"T1 inventory: questions={len(records)} area1={len(AREA1)} area2={len(AREA2)} "
        f"semantic_extra={len(SEMANTIC_EXTRA)} rules={len(rule_dependencies)} drugs={len(drug_dependencies)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
