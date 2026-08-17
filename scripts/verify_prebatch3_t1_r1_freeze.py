from __future__ import annotations

import hashlib
import json
from pathlib import Path

from freeze_legacy_salvage_t1_r1 import AUDITOR_INSTANCE, CANDIDATE_BRANCH, CANDIDATE_SHA, QUESTION_IDS, index
from qa_common import DATA, dependency_snapshot, drug_consequence_rule_ids, load_json, question_audit_hash, semantic_content_hash

ROOT = Path("audits/remediation/2026-08-17")
BLIND_PATH = ROOT / "GPT-C-BLIND-QUESTIONS-PRE-BATCH3-LEGACY-SALVAGE-T1-R1.json"
LEGAL_PATH = ROOT / "GPT-C-LEGAL-PRE-BATCH3-LEGACY-SALVAGE-T1-R1.json"
REALISM_PATH = ROOT / "GPT-C-REALISM-PRE-BATCH3-LEGACY-SALVAGE-T1-R1.json"
MANIFEST_PATH = ROOT / "PRE-BATCH3-LEGACY-SALVAGE-T1-R1-CLEAN-FREEZE-MANIFEST.json"


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    manifest = read(MANIFEST_PATH)
    legal = read(LEGAL_PATH)
    realism = read(REALISM_PATH)
    blind = read(BLIND_PATH)

    allowed_manifest = {
        "manifest_type", "created_date", "candidate_branch", "candidate_sha", "freeze_branch",
        "auditor_instance_reserved", "question_count", "question_ids", "question_hashes",
        "dependency_snapshots", "blind_question_package", "packages", "independence_sanitized",
        "locked_next_step",
    }
    allowed_common = {
        "package_type", "audit_date", "audit_scope", "auditor", "auditor_instance", "independent",
        "candidate_sha", "tranche", "question_ids", "question_hashes", "dependency_snapshots",
        "blind_question_package", "content_boundary", "independence_note",
    }
    assert set(manifest) == allowed_manifest
    assert set(legal) == allowed_common | {"review_type", "source_policy", "result_contract"}
    assert set(realism) == allowed_common | {"review_type", "full_bank_comparison_required", "criteria_required", "result_contract"}
    assert set(blind) == {"package_type", "audit_date", "auditor_instance", "candidate_sha", "question_ids", "questions", "content_boundary"}

    assert manifest["candidate_branch"] == CANDIDATE_BRANCH
    assert manifest["candidate_sha"] == CANDIDATE_SHA
    assert manifest["auditor_instance_reserved"] == AUDITOR_INSTANCE
    assert manifest["question_count"] == 3
    assert manifest["question_ids"] == QUESTION_IDS
    assert manifest["independence_sanitized"] is True

    for package in (legal, realism):
        assert package["candidate_sha"] == CANDIDATE_SHA
        assert package["auditor_instance"] == AUDITOR_INSTANCE
        assert package["audit_scope"] == "REAUDIT"
        assert package["question_ids"] == QUESTION_IDS
        assert package["question_hashes"] == manifest["question_hashes"]
        assert package["dependency_snapshots"] == manifest["dependency_snapshots"]
        assert package["blind_question_package"] == manifest["blind_question_package"]

    assert blind["candidate_sha"] == CANDIDATE_SHA
    assert blind["auditor_instance"] == AUDITOR_INSTANCE
    assert blind["question_ids"] == QUESTION_IDS
    assert len(blind["questions"]) == 3
    for item in blind["questions"]:
        assert set(item) == {"question_id", "question_type", "stem", "choices"}

    assert sha(BLIND_PATH) == manifest["blind_question_package"]["sha256"]
    assert sha(LEGAL_PATH) == manifest["packages"][str(LEGAL_PATH)]["sha256"]
    assert sha(REALISM_PATH) == manifest["packages"][str(REALISM_PATH)]["sha256"]

    questions = index(DATA / "questions", "question_id")
    rules = index(DATA / "rules", "rule_id")
    drugs = index(DATA / "drugs", "drug_id")
    selected = [questions[qid] for qid in QUESTION_IDS]

    recomputed_q = {qid: question_audit_hash(questions[qid]) for qid in QUESTION_IDS}
    assert recomputed_q == manifest["question_hashes"]

    blind_by_id = {item["question_id"]: item for item in blind["questions"]}
    for q in selected:
        assert blind_by_id[q["question_id"]] == {
            "question_id": q["question_id"],
            "question_type": q.get("question_type"),
            "stem": q.get("stem"),
            "choices": q.get("choices"),
        }

    direct_rule_ids = sorted({rid for q in selected for rid in q.get("rule_ids", [])})
    drug_ids = sorted({did for q in selected for did in q.get("drug_ids", [])})
    transitive_rule_ids = sorted({rid for did in drug_ids for rid in drug_consequence_rule_ids(drugs[did])})
    all_rule_ids = sorted(set(direct_rule_ids) | set(transitive_rule_ids))

    rule_snapshots = {}
    for rid in all_rule_ids:
        record = rules[rid]
        assert record.get("content_hash") == semantic_content_hash(record, "rule")
        rule_snapshots[rid] = dependency_snapshot(record)

    drug_snapshots = {}
    for did in drug_ids:
        record = drugs[did]
        assert record.get("content_hash") == semantic_content_hash(record, "drug")
        drug_snapshots[did] = dependency_snapshot(record)

    style = load_json(DATA / "exam_style" / "mpje_style_profile.json")
    assert style.get("content_hash") == semantic_content_hash(style, "style_profile")
    blueprint = load_json(DATA / "blueprint.json")
    assert blueprint.get("content_hash") == semantic_content_hash(blueprint, "blueprint")

    expected_dependencies = {
        "rules": rule_snapshots,
        "drugs": drug_snapshots,
        "blueprint": {"blueprint_id": blueprint["blueprint_id"], **dependency_snapshot(blueprint)},
        "style_profile": {"profile_id": style["profile_id"], **dependency_snapshot(style)},
    }
    assert expected_dependencies == manifest["dependency_snapshots"]

    print("sanitized T1 r1 changed-item freeze mechanical verification: PASS")
    print(f"blind_sha256={sha(BLIND_PATH)}")
    print(f"legal_sha256={sha(LEGAL_PATH)}")
    print(f"realism_sha256={sha(REALISM_PATH)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
