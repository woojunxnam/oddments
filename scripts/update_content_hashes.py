from __future__ import annotations

from qa_common import (
    DATA,
    dependency_snapshot,
    drug_consequence_rule_ids,
    load_records,
    semantic_content_hash,
    write_json,
)


def main() -> int:
    rules: dict[str, dict] = {}
    for path, rule in load_records(DATA / "rules"):
        if not isinstance(rule.get("content_version"), int):
            raise ValueError(f"{path}: set content_version before updating hashes")
        rule["content_hash"] = semantic_content_hash(rule, "rule")
        write_json(path, rule)
        rules[rule["rule_id"]] = rule

    for path, drug in load_records(DATA / "drugs"):
        if not isinstance(drug.get("content_version"), int):
            raise ValueError(f"{path}: set content_version before updating hashes")
        dependency_ids = sorted(drug_consequence_rule_ids(drug))
        unknown_ids = [rule_id for rule_id in dependency_ids if rule_id not in rules]
        if unknown_ids:
            raise ValueError(f"{path}: unknown consequence rule IDs: {unknown_ids}")
        drug["verified_rule_dependencies"] = {
            rule_id: dependency_snapshot(rules[rule_id]) for rule_id in dependency_ids
        }
        drug["content_hash"] = semantic_content_hash(drug, "drug")
        write_json(path, drug)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
