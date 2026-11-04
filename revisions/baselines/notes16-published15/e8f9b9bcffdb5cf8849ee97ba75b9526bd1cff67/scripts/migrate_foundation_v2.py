from __future__ import annotations

from qa_common import DATA, dependency_snapshot, load_json, load_records, semantic_content_hash, write_json


CONSEQUENCE_RULES = {
    "buprenorphine-naloxone": {
        "refill": ["FED-CS-REFILL-III-IV"],
        "transfer": ["FED-CS-SCHEDULES"],
        "partial_fill": ["FED-CS-SCHEDULES"],
        "masspat": ["MA-PMP-REPORTING"],
        "quantity_limit": ["MA-CS-QUANTITY-II-III"],
    },
    "gabapentin": {
        "refill": ["FED-CS-SCHEDULES"],
        "transfer": ["FED-CS-SCHEDULES"],
        "partial_fill": ["FED-CS-SCHEDULES"],
        "masspat": ["MA-PMP-REPORTING"],
        "quantity_limit": ["MA-CS-QUANTITY-II-III"],
    },
    "methylphenidate": {
        "refill": ["FED-CS-SCHEDULES"],
        "transfer": ["MA-CII-PARTIAL-PATIENT"],
        "partial_fill": ["MA-CII-PARTIAL-PATIENT"],
        "masspat": ["MA-PMP-REPORTING"],
        "quantity_limit": ["MA-CS-QUANTITY-II-III"],
    },
    "pregabalin": {
        "refill": ["MA-RX-CV-REFILL"],
        "transfer": ["FED-CS-SCHEDULES"],
        "partial_fill": ["FED-CS-SCHEDULES"],
        "masspat": ["MA-PMP-REPORTING"],
        "quantity_limit": ["MA-CS-QUANTITY-II-III"],
    },
    "pseudoephedrine": {
        "refill": ["FED-PSE-QUANTITY"],
        "transfer": ["FED-PSE-QUANTITY"],
        "partial_fill": ["FED-PSE-QUANTITY"],
        "masspat": ["MA-PMP-REPORTING"],
        "quantity_limit": ["FED-PSE-QUANTITY"],
    },
}

SCOPE_LIMITED_SUMMARIES = {
    ("buprenorphine-naloxone", "transfer"): (
        "This foundation verifies Schedule III classification but does not yet establish a complete transfer rule."
    ),
    ("buprenorphine-naloxone", "partial_fill"): (
        "Schedule III classification does not activate this registry's Schedule II-only partial-fill rule; "
        "a complete Schedule III partial-fill pathway is not modeled."
    ),
    ("gabapentin", "refill"): (
        "This foundation records the Massachusetts Schedule VI framework but does not yet establish a complete refill rule."
    ),
    ("gabapentin", "transfer"): (
        "This foundation records the Massachusetts Schedule VI framework but does not yet establish a complete transfer rule."
    ),
    ("methylphenidate", "refill"): (
        "This foundation verifies Schedule II classification but does not yet store the federal no-refill rule as a canonical dependency."
    ),
    ("pregabalin", "transfer"): (
        "This foundation verifies Schedule V classification but does not yet establish every transfer pathway."
    ),
    ("pregabalin", "partial_fill"): (
        "This foundation verifies Schedule V classification but does not yet establish a complete partial-fill rule."
    ),
    ("pseudoephedrine", "refill"): (
        "This foundation models ordinary nonprescription retail sales; prescription refill analysis is outside this fixture's scope."
    ),
    ("pseudoephedrine", "transfer"): (
        "This foundation models ordinary nonprescription retail sales; prescription transfer analysis is outside this fixture's scope."
    ),
    ("pseudoephedrine", "partial_fill"): (
        "This foundation models ordinary nonprescription retail sales; prescription partial-fill analysis is outside this fixture's scope."
    ),
}


def main() -> int:
    blueprint_path = DATA / "blueprint.json"
    blueprint = load_json(blueprint_path)
    blueprint.setdefault("blueprint_id", "MPJE-MA-PRE2027-BLUEPRINT")
    blueprint.setdefault("content_version", 1)
    blueprint["content_hash"] = semantic_content_hash(blueprint, "blueprint")
    write_json(blueprint_path, blueprint)

    profile_path = DATA / "exam_style" / "mpje_style_profile.json"
    profile = load_json(profile_path)
    profile.setdefault("content_version", 1)
    profile["content_hash"] = semantic_content_hash(profile, "style_profile")
    write_json(profile_path, profile)

    matrix_path = DATA / "exam_style" / "question_family_matrix.json"
    matrix = load_json(matrix_path)
    for family in matrix.get("families", []):
        old_count = family.pop("current_question_count", None)
        family.setdefault("current_candidate_count", old_count if old_count is not None else 0)
        family.setdefault("current_released_count", 0)
    write_json(matrix_path, matrix)

    rules: dict[str, dict] = {}
    for path, rule in load_records(DATA / "rules"):
        rule.setdefault("content_version", 1)
        rule["content_hash"] = semantic_content_hash(rule, "rule")
        write_json(path, rule)
        rules[rule["rule_id"]] = rule

    for path, drug in load_records(DATA / "drugs"):
        drug.setdefault("content_version", 1)
        mappings = CONSEQUENCE_RULES[drug["drug_id"]]
        consequences = {}
        for name, value in drug["legal_consequences"].items():
            summary = SCOPE_LIMITED_SUMMARIES.get(
                (drug["drug_id"], name),
                value["summary"] if isinstance(value, dict) else value,
            )
            consequences[name] = {"summary": summary, "rule_ids": mappings[name]}
        drug["legal_consequences"] = consequences
        dependency_ids = sorted({rule_id for rule_ids in mappings.values() for rule_id in rule_ids})
        drug["verified_rule_dependencies"] = {
            rule_id: dependency_snapshot(rules[rule_id]) for rule_id in dependency_ids
        }
        drug["content_hash"] = semantic_content_hash(drug, "drug")
        write_json(path, drug)

    for path, question in load_records(DATA / "questions"):
        question.pop("allow_zero_correct", None)
        question.pop("realism", None)
        question.setdefault("source_signal_ids", [])
        write_json(path, question)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
