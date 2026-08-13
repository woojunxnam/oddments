from __future__ import annotations

from copy import deepcopy

from qa_common import semantic_content_hash


def test_semantic_hash_ignores_whitespace_and_unordered_list_order(registry_indexes) -> None:
    rules, _ = registry_indexes
    original = rules["MA-RX-CV-REFILL"]
    reformatted = deepcopy(original)
    reformatted["rule_summary"] = "  " + reformatted["rule_summary"].replace(" ", "   ") + "  "
    reformatted["authority"] = list(reversed(reformatted["authority"]))
    reformatted["common_confusions"] = list(reversed(reformatted["common_confusions"]))
    assert semantic_content_hash(reformatted, "rule") == original["content_hash"]


def test_semantic_hash_changes_for_legal_meaning_change(registry_indexes) -> None:
    rules, _ = registry_indexes
    original = rules["MA-RX-CV-REFILL"]
    changed = deepcopy(original)
    changed["numeric_facts"][0]["value"] = 99
    assert semantic_content_hash(changed, "rule") != original["content_hash"]
