from __future__ import annotations

import hashlib
import json
from pathlib import Path

from qa_common import question_audit_hash, semantic_content_hash

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_CANDIDATE_SHA = "e8b42047f2579f0b83822bc15dcc640c5e9ba236"
QUESTION_ID = "MA-Q-0213"
QUESTION_PATH = ROOT / "data/questions/ma-q-0213.json"
EXPECTED_QUESTION_HASH = "689120dad57db1ef46087cda3450a8df13799d865c67dd9942f46d7911b1ce23"
EXPECTED_QUESTION_BLOB = "4f16c9b25308e1a2936a39882b4271a570ace42d"
EXPECTED_RULE_IDS = ["MA-COUNSELING-REMOTE-DELIVERY", "MA-COUNSELING"]

DEPENDENCIES = [
    (
        ROOT / "data/rules/ma-counseling-remote-delivery.json",
        "MA-COUNSELING-REMOTE-DELIVERY",
        "8775dfc91c1c633979acd4aae50ade32c42af5a68262ad258f3a9f1c163bb822",
        "4298e962255da6e47ad133672454c16a4f53d7bd",
    ),
    (
        ROOT / "data/rules/ma-counseling.json",
        "MA-COUNSELING",
        "e8f6fbdb5b0bdb7ec7f1512527eeeac5dbe49e0b761ac0f498fa9da11faedd82",
        "0825a6eb514ab1a0ee433d7061ecdcef47b44c1c",
    ),
]

FAMILY_ID = "T2_0213_MA_COUNSELING_REMOTE_DELIVERY_OFFER"
FAMILY_MATRIX_PATH = ROOT / "data/exam_style/question_family_matrix.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def find_family(value):
    if isinstance(value, dict):
        if value.get("family_id") == FAMILY_ID:
            return value
        for child in value.values():
            found = find_family(child)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_family(child)
            if found is not None:
                return found
    return None


def main() -> None:
    question = load_json(QUESTION_PATH)
    require(question.get("question_id") == QUESTION_ID, "question ID mismatch")
    require(question_audit_hash(question) == EXPECTED_QUESTION_HASH, "question audit hash mismatch")
    require(git_blob_sha(QUESTION_PATH) == EXPECTED_QUESTION_BLOB, "question Git blob mismatch")
    require(question.get("rule_ids") == EXPECTED_RULE_IDS, "question dependency order mismatch")

    expected_status = {
        "verification_status": "AUDIT_PENDING",
        "lifecycle_status": "AUDIT_PENDING",
        "duplicate_review_status": "PENDING",
        "independent_audit_status": "PENDING",
        "audits": [],
        "final_adjudication": None,
        "development_fixture": True,
    }
    for key, expected in expected_status.items():
        require(question.get(key) == expected, f"question status mismatch: {key}")

    for path, expected_rule_id, expected_hash, expected_blob in DEPENDENCIES:
        record = load_json(path)
        require(record.get("rule_id") == expected_rule_id, f"rule ID mismatch: {path}")
        require(record.get("content_version") == 1, f"content_version mismatch: {expected_rule_id}")
        require(record.get("content_hash") == expected_hash, f"stored content_hash mismatch: {expected_rule_id}")
        require(semantic_content_hash(record, "rule") == expected_hash, f"recomputed content_hash mismatch: {expected_rule_id}")
        require(git_blob_sha(path) == expected_blob, f"Git blob mismatch: {expected_rule_id}")

    family_matrix = load_json(FAMILY_MATRIX_PATH)
    family = find_family(family_matrix)
    require(family is not None, "family matrix entry not found")
    require(family.get("primary_rule_ids") == ["MA-COUNSELING-REMOTE-DELIVERY"], "family primary rule mismatch")
    require(family.get("secondary_rule_ids") == ["MA-COUNSELING"], "family secondary rule mismatch")

    print("pre-batch3 coverage T2 Q0213 r1 v1 freeze mechanical verification: PASS")


if __name__ == "__main__":
    main()
