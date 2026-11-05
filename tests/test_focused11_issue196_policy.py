from __future__ import annotations

from copy import deepcopy

import pytest
import validate_audits as policy

# Pure policy fixtures only; no question body, legal review, or release record.
TRANCHE = "FOCUSED-MPJE336-FOCUSED11"
IDS = ['MA-Q-0441', 'MA-Q-0446', 'MA-Q-0448', 'MA-Q-0451', 'MA-Q-0452', 'MA-Q-0453', 'MA-Q-0456', 'MA-Q-0459', 'MA-Q-0461', 'MA-Q-0465', 'MA-Q-0468']
HASHES = {'MA-Q-0441': '4fc702e7e02938457b0af345e38c0162371cb8c528179be5425a7a95ee7e81ad', 'MA-Q-0446': 'b18989503ce0edd87ef3cd4b79b8f50cbfe566191a0a526f5427c266430093f0', 'MA-Q-0448': '3c4c8135761b4e208a7140cef7708dde10856f64018f081db5f50c411c8b04d3', 'MA-Q-0451': '34bda60837330705badc801838713229d646778ffeb6fe18be46fa99cc177be9', 'MA-Q-0452': '835adcd1f23f0321039dae094234831105550a7a91fa3ad30be41df700a960a4', 'MA-Q-0453': '5b677d3ac2d38b2fbdcde25b0d7c0737ca864888f0127e20fb7a67bd2471d3d8', 'MA-Q-0456': '11131c31be205b22c34607ca84567245bd665c11169aaf430e9b98ff00473d63', 'MA-Q-0459': 'afc59770277751e2d4afa76f8a26737dc4b6a5a0d1af4cfbe29ede6d79ae8f95', 'MA-Q-0461': '9d28d6e3aabf5416217d9e7a40efc4afee641a4932b79e9c0caa1c533ea1a95e', 'MA-Q-0465': '1d05ea3862897d2cddff4e302ccd7ea447f66fbf51ba428dc954ca4aa670a894', 'MA-Q-0468': 'c121ac08b6232b2f5d3d4471cad3fb6232b920d98731aeecb3eedf6fa7f893f6'}
SHA = "40905fc1b895e2254f0a979f6d87e2f7e474021c"


def fixture(review_type="LEGAL_VERIFICATION"):
    return {
        "audit_scope": "TARGETED_INITIAL_BATCH",
        "review_type": review_type,
        "independent": True,
        "audit_status": "FULLY_ADJUDICATED",
        "governance_authorization": {
            "tranche_id": TRANCHE,
            "authorizing_issue": 196,
            "represented_candidate_sha": SHA,
            "question_ids": IDS.copy(),
        },
        "question_ids": IDS.copy(),
        "question_hashes": HASHES.copy(),
        "results": [{"Question_ID": qid} for qid in IDS],
    }


@pytest.mark.parametrize("review_type", ["LEGAL_VERIFICATION", "REALISM_REVIEW"])
def test_issue196_exact_scope_and_hashes_are_accepted(review_type):
    audit = fixture(review_type)
    assert policy._targeted_initial_governance_errors(audit) == []
    assert policy.is_valid_targeted_initial_audit(audit)


@pytest.mark.parametrize("field,value", [
    ("authorizing_issue", 195),
    ("represented_candidate_sha", "0" * 40),
    ("represented_candidate_sha", "A" * 40),
    ("tranche_id", "UNAUTHORIZED-FOCUSED11"),
])
def test_issue196_rejects_wrong_authorization(field, value):
    audit = fixture()
    audit["governance_authorization"][field] = value
    assert policy._targeted_initial_governance_errors(audit)
    assert not policy.is_valid_targeted_initial_audit(audit)


@pytest.mark.parametrize("mutation", ["missing", "extra", "stale", "null", "missing_map"])
def test_issue196_rejects_any_hash_map_mismatch(mutation):
    audit = fixture()
    if mutation == "missing":
        audit["question_hashes"].pop(IDS[0])
    elif mutation == "extra":
        audit["question_hashes"]["MA-Q-0999"] = "a" * 64
    elif mutation == "stale":
        audit["question_hashes"][IDS[0]] = "0" * 64
    elif mutation == "null":
        audit["question_hashes"] = None
    else:
        del audit["question_hashes"]
    assert any("exact authorized hashes" in e for e in policy._targeted_initial_governance_errors(audit))
    assert not policy.is_valid_targeted_initial_audit(audit)


@pytest.mark.parametrize("target,mutation", [
    ("question_ids", "missing"), ("question_ids", "extra"),
    ("authorization", "missing"), ("authorization", "extra"),
])
def test_issue196_rejects_any_id_scope_change(target, mutation):
    audit = fixture()
    ids = audit["question_ids"] if target == "question_ids" else audit["governance_authorization"]["question_ids"]
    ids.pop() if mutation == "missing" else ids.append("MA-Q-0999")
    assert policy._targeted_initial_governance_errors(audit)
    assert not policy.is_valid_targeted_initial_audit(audit)


@pytest.mark.parametrize("field,value", [
    ("independent", False),
    ("audit_status", "STRUCTURAL_TRIAGE_ONLY"),
    ("audit_scope", "REAUDIT"),
    ("audit_scope", "INITIAL_BATCH"),
])
def test_issue196_does_not_replace_other_initial_admission_requirements(field, value):
    audit = fixture()
    audit[field] = value
    assert not policy.is_valid_targeted_initial_audit(audit)


@pytest.mark.parametrize("count", [0, 1, 10, 12, 29, 30, 40, 41])
def test_issue196_exact_eleven_does_not_authorize_other_counts(count):
    audit = fixture()
    ids = [f"MA-Q-{i+1000:04d}" for i in range(count)]
    audit["question_ids"] = ids
    audit["question_hashes"] = {qid: "a" * 64 for qid in ids}
    audit["results"] = [{"Question_ID": qid} for qid in ids]
    audit["governance_authorization"]["question_ids"] = ids.copy()
    assert not policy.is_valid_targeted_initial_audit(audit)


@pytest.mark.parametrize("tranche", ["PRE-BATCH3-COVERAGE-T2", "PRE-BATCH3-COVERAGE-T3-DIVERSITY", "BATCH3-B3F"])
def test_original_three_authorizations_keep_their_existing_no_fixed_hash_policy(tranche):
    authority = policy.TARGETED_INITIAL_BATCH_AUTHORIZATIONS[tranche]
    assert "question_hashes" not in authority
    audit = fixture()
    ids = sorted(authority["question_ids"])
    audit["question_ids"] = ids
    audit["question_hashes"] = {qid: "a" * 64 for qid in ids}
    audit["results"] = [{"Question_ID": qid} for qid in ids]
    audit["governance_authorization"] = {
        "tranche_id": tranche,
        "authorizing_issue": authority["authorizing_issue"],
        "represented_candidate_sha": authority["represented_candidate_sha"],
        "question_ids": ids.copy(),
    }
    assert policy._targeted_initial_governance_errors(audit) == []
    assert policy.is_valid_targeted_initial_audit(audit)
    audit["question_hashes"][ids[0]] = "b" * 64
    assert policy._targeted_initial_governance_errors(audit) == []
    assert policy.is_valid_targeted_initial_audit(audit)
