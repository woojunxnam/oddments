from __future__ import annotations

from build_site_data import build_site_payload, derive_realism_reviews
from qa_common import question_audit_hash


def test_release_site_data_excludes_audit_pending_fixtures() -> None:
    payload = build_site_payload(include_fixtures=False)
    assert payload["questions"] == []
    assert payload["meta"]["development_fixture_mode"] is False
    assert payload["meta"]["release_status"] == "NO_RELEASED_QUESTIONS"
    assert "safe_to_memorize" not in payload["meta"]
    assert payload["meta"]["blueprint"]["content_hash"]
    assert payload["meta"]["style_profile"]["content_hash"]


def test_development_site_data_is_explicitly_unsafe() -> None:
    payload = build_site_payload(include_fixtures=True)
    assert len(payload["questions"]) == 10
    assert payload["meta"]["development_fixture_mode"] is True
    assert payload["meta"]["release_status"] == "DEVELOPMENT_ONLY"
    assert all(question["realism_reviews"] == [] for question in payload["questions"])


def test_realism_output_is_derived_from_canonical_audit(canonical_question) -> None:
    question = dict(canonical_question)
    question["audits"] = ["AUDIT-HUMAN-REALISM-DERIVATION"]
    audit = {
        "audit_id": question["audits"][0],
        "auditor": "HUMAN",
        "review_type": "REALISM_REVIEW",
        "question_hashes": {question["question_id"]: question_audit_hash(question)},
        "style_profile": {
            "profile_id": "MPJE-MA-PRE2027",
            "content_version": 1,
            "content_hash": "a" * 64,
        },
        "results": [
            {
                "Question_ID": question["question_id"],
                "Verdict": "KEEP",
                "Realism_Verdict": "PASS",
                "Reviewed_Date": "2026-08-13",
                "Criteria": {"practice_plausibility": True},
                "Notes": "Derived display fixture.",
            }
        ],
    }
    reviews = derive_realism_reviews(question, {audit["audit_id"]: audit})
    assert reviews[0]["audit_id"] == audit["audit_id"]
    assert reviews[0]["notes"] == "Derived display fixture."
