from __future__ import annotations

import json
from copy import deepcopy

from qa_common import semantic_content_hash


def run_drug_validation(tmp_path, monkeypatch, drug: dict, rules: dict):
    import validate_drugs as module

    directory = tmp_path / "data" / "drugs"
    directory.mkdir(parents=True)
    (directory / "drug.json").write_text(json.dumps(drug, indent=2) + "\n", encoding="utf-8")
    monkeypatch.setattr(module, "DATA", tmp_path / "data")
    return module.validate_drugs(rules)[0]


def test_drug_consequence_unknown_rule_fails(tmp_path, monkeypatch, registry_indexes) -> None:
    rules, drugs = registry_indexes
    drug = deepcopy(drugs["pregabalin"])
    drug["legal_consequences"]["refill"]["rule_ids"] = ["MA-NOT-A-RULE"]
    drug["verified_rule_dependencies"].pop("MA-RX-CV-REFILL")
    drug["verified_rule_dependencies"]["MA-NOT-A-RULE"] = {
        "content_version": 1,
        "content_hash": "a" * 64,
    }
    drug["content_hash"] = semantic_content_hash(drug, "drug")
    report = run_drug_validation(tmp_path, monkeypatch, drug, rules)
    assert any("legal consequence references unknown rule_id MA-NOT-A-RULE" in error for error in report.errors)


def test_blocked_rule_prevents_dependent_verified_drug(tmp_path, monkeypatch, registry_indexes) -> None:
    rules, drugs = registry_indexes
    drug = deepcopy(drugs["pregabalin"])
    rule_id = "MA-CS-QUANTITY-II-III"
    rules[rule_id]["status"] = "DRAFT"
    rules[rule_id]["content_version"] += 1
    rules[rule_id]["content_hash"] = semantic_content_hash(rules[rule_id], "rule")
    report = run_drug_validation(tmp_path, monkeypatch, drug, rules)
    assert any(f"verified drug depends on blocked rule {rule_id}" in error for error in report.errors)
