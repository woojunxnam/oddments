"""VAX15–PUB04 original 40-question, 160-option author source-review contract.

No independent legal/psychometric audit is represented by these tests.
"""
import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_full_corpus_review import record_hash, validate_review


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def review():
    return read("reports/full-corpus-review/vax15-pub04-author-review.json")


def originals():
    return {q["question_id"]: q for q in read(
        "practice_expansion/2026-10-23/candidates/questions.json"
    )["questions"]}


def test_exact_40_ids_160_complete_choice_findings_and_current_hashes():
    source = review()
    records = source["records"]
    expected = {f"MA-EXP-{n:04d}" for n in range(345, 385)}
    assert len(records) == len(expected) == 40
    assert {r["question_id"] for r in records} == expected
    assert len({r["question_id"] for r in records}) == 40
    assert sum(len(r["choice_by_choice_findings"]) for r in records) == 160
    assert source["coverage"]["choice_findings"] == 160
    assert source["coverage"]["unique_families"] == 10
    questions = originals()
    baseline = read(
        "reports/full-corpus-review/baseline-inventory.json"
    )["question_record_hashes"]
    for row in records:
        qid = row["question_id"]
        question = questions[qid]
        assert row["record_sha256"] == baseline[qid] == record_hash(question)
        validate_review(question, row)
        assert row["reviewer_provenance"]["independent"] is False
        assert row["quality_assessment"] is None
        assert row["checked_at"] == "2026-11-02"
        assert set(row["choice_by_choice_findings"]) == {
            choice["id"] for choice in question["choices"]
        }
        for finding in row["choice_by_choice_findings"].values():
            assert type(finding["statement_supported"]) is bool
            assert finding["finding_ko"].strip()
            assert finding["exact_authority"].strip()
            assert finding["official_url"].startswith("https://")


def test_key_polarity_is_opposite_for_ten_incorrect_prompts():
    questions = originals()
    negative_ids = []
    for row in review()["records"]:
        q = questions[row["question_id"]]
        negative = row["answer_key_crosscheck"]["lead_polarity"] == (
            "SELECT_INCORRECT_STATEMENT"
        )
        findings = row["choice_by_choice_findings"]
        expected = [
            choice["id"] for choice in q["choices"]
            if findings[choice["id"]]["statement_supported"] == (not negative)
        ]
        assert expected == q["correct_choice_ids"], q["question_id"]
        assert row["answer_key_crosscheck"]["expected_from_official_statements"] == expected
        assert row["answer_key_crosscheck"]["stored"] == expected
        assert row["answer_key_crosscheck"]["matches"] is True
        if q["question_type"] == "SBA":
            assert len(expected) == 1
        if negative:
            negative_ids.append(q["question_id"])
    assert negative_ids == [f"MA-EXP-{i:04d}" for i in range(348, 385, 4)]


def test_three_all_correct_sata_are_identified_without_changing_public_history():
    questions = originals()
    selection = read("practice_expansion/2026-10-28-representative/selection.json")
    reviewed = {r["question_id"]: r for r in review()["records"]}
    low_discrimination = ("MA-EXP-0351", "MA-EXP-0367", "MA-EXP-0383")
    for qid in low_discrimination:
        q = questions[qid]
        assert q["question_type"] == "SATA"
        assert set(q["correct_choice_ids"]) == {c["id"] for c in q["choices"]}
        assert reviewed[qid]["disposition"] == "MAJOR_REWRITE"
        assert reviewed[qid]["answer_key_crosscheck"]["all_correct_sata"] is True
        assert qid not in selection["recommended_ids"]
        assert qid in {h["legacy_question_id"] for h in selection["holds"]}
        assert "Four-of-four SATA" in reviewed[qid]["blocker"]
    assert {r["question_id"] for r in review()["records"]
            if r["disposition"] == "MAJOR_REWRITE"} == set(low_discrimination)


def test_publishing_review_does_not_claim_cdtm_cross_path_or_independent_audit():
    source = review()
    assert source["coverage"]["conditionally_source_checked_ids"] == 4
    assert source["coverage"]["author_source_checked_ids"] == 36
    conditional = {r["question_id"] for r in source["records"]
                   if r["legal_review_status"]
                   == "AUTHOR_CONDITIONAL_SOURCE_CHECK_NOT_INDEPENDENT"}
    assert conditional == {f"MA-EXP-{n:04d}" for n in range(373, 377)}
    assert all(r["original_answer_status"] == "CORRECT_WITH_SCOPE_QUALIFICATION"
               for r in source["records"] if r["question_id"] in conditional)
    for entry in source["source_register"]:
        assert not ("247-cmr-1700" in entry["url"].lower())  # DRAFT 247 CMR17 is not authority.
    assert any("supersedes DCP 23-04-118" in x.get("version", "")
               for x in source["source_register"])
    assert any("supersedes DCP 25-04-124" in x.get("version", "")
               for x in source["source_register"])
    progress = read("reports/full-corpus-review/progress.json")
    assert progress["current_questions"] == 2346
    assert progress["question_ids_with_review_records"] >= 285
    assert progress["legal_review_counts"]["NOT_REVERIFIED_IN_FULL_CORPUS_REVIEW"] <= 2061
    assert progress["author_review_records_by_file"]["vax15-pub04-author-review.json"] == 40
    assert progress["open_claims"] == 4
    assert progress["canonical_independent_audit_this_session"] == "NOT_RUN"
    assert progress["notes_units_with_complete_atomic_claim_census"] >= 12


def test_stale_question_or_missing_option_fails_review_integrity():
    question = originals()["MA-EXP-0365"]
    row = next(r for r in review()["records"] if r["question_id"] == question["question_id"])
    stale = copy.deepcopy(question)
    stale["choices"][0]["text"] += " Unreviewed addendum."
    with pytest.raises(ValueError, match="Stale review"):
        validate_review(stale, row)
    incomplete = copy.deepcopy(row)
    incomplete["choice_by_choice_findings"].pop("B")
    with pytest.raises(ValueError, match="Missing choice"):
        validate_review(question, incomplete)


def test_following_four_coun03_questions_use_their_own_later_review():
    rows = {json.loads(s)["question_id"]: json.loads(s)
            for s in (ROOT / "reports/full-corpus-review/question-ledger.jsonl")
            .read_text(encoding="utf-8").splitlines()}
    path = 'reports/full-corpus-review/wave10-1-author-review.json'
    later = {r['question_id']:r for r in json.loads((ROOT/path).read_text())['records']}
    for n in range(425, 429):
        row = rows[f"MA-EXP-{n:04d}"]
        evidence = later[row['question_id']]
        assert row['checked_at'] == evidence['checked_at']
        assert row['content_sha256'] == evidence['record_sha256']
        assert row['review_evidence']['source_path'] == path
        assert row['reviewer_provenance'] == evidence['reviewer_provenance']
