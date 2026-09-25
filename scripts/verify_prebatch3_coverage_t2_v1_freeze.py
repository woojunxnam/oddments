from __future__ import annotations

import hashlib
import json
from pathlib import Path

from qa_common import (
    DATA,
    dependency_snapshot,
    load_json,
    load_records,
    question_audit_hash,
    semantic_content_hash,
)

CANDIDATE_SHA = "b849159ef18d37618ca6badf886e465502436e1b"
FREEZE_BRANCH = "freeze/pre-batch3-coverage-t2-v1"
AUDITOR_INSTANCE = "GPT-FRESH-COV-T2-A"
QUESTION_IDS = [f"MA-Q-{i:04d}" for i in range(211, 227)]
ROOT = Path("audits/remediation/2026-08-18")
BLIND_PATH = ROOT / "GPT-T2A-BLIND-QUESTIONS-PRE-BATCH3-COVERAGE-T2.json"
LEGAL_PATH = ROOT / "GPT-T2A-LEGAL-PRE-BATCH3-COVERAGE-T2.json"
REALISM_PATH = ROOT / "GPT-T2A-REALISM-PRE-BATCH3-COVERAGE-T2.json"
MANIFEST_PATH = ROOT / "PRE-BATCH3-COVERAGE-T2-CLEAN-FREEZE-V1-MANIFEST.json"


def index(directory: Path, id_field: str) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for _, record in load_records(directory):
        rid = record.get(id_field)
        if rid:
            result[rid] = record
    return result


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    manifest = load_json(MANIFEST_PATH)
    blind = load_json(BLIND_PATH)
    legal = load_json(LEGAL_PATH)
    realism = load_json(REALISM_PATH)

    assert manifest["represented_candidate_sha"] == CANDIDATE_SHA
    assert manifest["freeze_branch"] == FREEZE_BRANCH
    assert manifest["auditor_instance_reserved"] == AUDITOR_INSTANCE
    assert manifest["question_ids"] == QUESTION_IDS
    assert manifest["question_count"] == 16
    assert manifest["independence_sanitized"] is True

    assert sha256_file(BLIND_PATH) == manifest["packages"][str(BLIND_PATH)]["sha256"]
    assert sha256_file(LEGAL_PATH) == manifest["packages"][str(LEGAL_PATH)]["sha256"]
    assert sha256_file(REALISM_PATH) == manifest["packages"][str(REALISM_PATH)]["sha256"]

    for package in (legal, realism):
        assert package["represented_candidate_sha"] == CANDIDATE_SHA
        assert package["freeze_branch"] == FREEZE_BRANCH
        assert package["auditor_instance"] == AUDITOR_INSTANCE
        assert package["question_ids"] == QUESTION_IDS
        assert package["question_hashes"] == manifest["question_hashes"]
        assert package["dependency_snapshots"] == manifest["dependency_snapshots"]
        assert package["blind_question_package"] == manifest["blind_question_package"]

    assert blind["represented_candidate_sha"] == CANDIDATE_SHA
    assert blind["auditor_instance"] == AUDITOR_INSTANCE
    assert blind["question_ids"] == QUESTION_IDS
    assert len(blind["questions"]) == 16
    for item in blind["questions"]:
        assert set(item) == {"question_id", "question_type", "stem", "choices"}

    questions = index(DATA / "questions", "question_id")
    rules = index(DATA / "rules", "rule_id")
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
        assert q.get("verification_status") == "AUDIT_PENDING"
        assert q.get("lifecycle_status") == "AUDIT_PENDING"
        assert q.get("independent_audit_status") == "PENDING"
        assert q.get("duplicate_review_status") == "PENDING"
        assert q.get("audits") == []
        assert q.get("final_adjudication") is None
        assert q.get("development_fixture") is True

    direct_rule_ids = sorted({rid for q in selected for rid in q.get("rule_ids", [])})
    assert all(not q.get("drug_ids") for q in selected)
    rule_snapshots = {}
    for rid in direct_rule_ids:
        record = rules[rid]
        assert record.get("content_hash") == semantic_content_hash(record, "rule")
        rule_snapshots[rid] = dependency_snapshot(record)

    style = load_json(DATA / "exam_style" / "mpje_style_profile.json")
    assert style.get("content_hash") == semantic_content_hash(style, "style_profile")
    blueprint = load_json(DATA / "blueprint.json")
    assert blueprint.get("content_hash") == semantic_content_hash(blueprint, "blueprint")

    expected_dependencies = {
        "rules": rule_snapshots,
        "drugs": {},
        "blueprint": {"blueprint_id": blueprint["blueprint_id"], **dependency_snapshot(blueprint)},
        "style_profile": {"profile_id": style["profile_id"], **dependency_snapshot(style)},
    }
    assert expected_dependencies == manifest["dependency_snapshots"]
    assert realism["full_bank_comparison_required"] is True
    assert realism["canonical_bank_reference"]["scope"] == "FULL_CANONICAL_BANK"

    print("pre-batch3 coverage T2 v1 freeze mechanical verification: PASS")
    print(f"blind_sha256={sha256_file(BLIND_PATH)}")
    print(f"legal_sha256={sha256_file(LEGAL_PATH)}")
    print(f"realism_sha256={sha256_file(REALISM_PATH)}")
    for qid in QUESTION_IDS:
        print(f"question_hash[{qid}]={recomputed_q[qid]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
