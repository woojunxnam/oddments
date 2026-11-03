"""VAX05–14 source-bound author-review contract; NOT independent law certification."""
import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_full_corpus_review import record_hash, validate_review


def read(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def cohort():
    return read("reports/full-corpus-review/vax05-14-author-review.json")


def source_questions():
    paths = (
        "practice_expansion/2026-10-23/candidates/questions.json",
        "practice_expansion/2026-10-28-representative/questions.json",
    )
    return {q["question_id"]: q for path in paths for q in read(path)["questions"]}


def test_exact_existing_ids_and_every_option_have_hash_bound_author_findings():
    data = cohort()
    records = data["records"]
    expected = {f"MA-EXP-{n:04d}" for n in range(305, 345)}
    expected |= {f"MA-RW-{n:04d}" for n in range(45, 49)}
    assert len(records) == len(expected) == 44
    assert {r["question_id"] for r in records} == expected
    assert len({r["question_id"] for r in records}) == 44
    assert sum(len(r["choice_by_choice_findings"]) for r in records) == 177
    assert data["coverage"]["choice_findings"] == 177
    questions = source_questions()
    baseline = read("reports/full-corpus-review/baseline-inventory.json")["question_record_hashes"]
    for review in records:
        q = questions[review["question_id"]]
        assert review["record_sha256"] == record_hash(q) == baseline[q["question_id"]]
        validate_review(q, review)
        assert set(review["choice_by_choice_findings"]) == {c["id"] for c in q["choices"]}
        assert review["reviewer_provenance"]["independent"] is False
        assert review["legal_review_status"] == "AUTHOR_SOURCE_CHECKED_NOT_INDEPENDENT"
        for finding in review["choice_by_choice_findings"].values():
            assert type(finding["statement_supported"]) is bool
            assert finding["finding_ko"].strip() and finding["exact_authority"].strip()
            assert finding["official_url"].startswith("https://")


def test_incorrect_lead_keys_select_false_statements_not_true_statements():
    by_id = source_questions()
    incorrect = []
    for record in cohort()["records"]:
        question = by_id[record["question_id"]]
        findings = record["choice_by_choice_findings"]
        negative = record["answer_key_crosscheck"]["lead_polarity"] == "SELECT_INCORRECT_STATEMENT"
        expected = [
            choice["id"] for choice in question["choices"]
            if findings[choice["id"]]["statement_supported"] == (not negative)
        ]
        assert expected == question["correct_choice_ids"], record["question_id"]
        assert record["answer_key_crosscheck"]["matches"]
        assert record["answer_key_crosscheck"]["expected_from_official_statements"] == expected
        if question["question_type"] == "SBA":
            assert len(expected) == 1
        if negative:
            incorrect.append(record["question_id"])
            assert all(not findings[key]["statement_supported"] for key in expected)
    assert incorrect == [f"MA-EXP-{number:04d}" for number in range(308, 345, 4)]


def test_inherited_all_correct_sata_is_not_mislabeled_as_realistic():
    records = {r["question_id"]: r for r in cohort()["records"]}
    questions = source_questions()
    for qid in ("MA-EXP-0319", "MA-EXP-0335"):
        q = questions[qid]
        assert q["question_type"] == "SATA"
        assert set(q["correct_choice_ids"]) == {c["id"] for c in q["choices"]}
        assert records[qid]["disposition"] == "MAJOR_REWRITE"
        assert "all-correct" in records[qid]["blocker"]


def test_unreviewed_questions_not_credited_and_independence_not_claimed():
    progress = read("reports/full-corpus-review/progress.json")
    assert progress["current_questions"] == 2346
    assert progress["question_ids_with_review_records"] >= 245
    assert progress["legal_review_counts"]["NOT_REVERIFIED_IN_FULL_CORPUS_REVIEW"] <= 2101
    assert progress["author_review_records_by_file"]["vax05-14-author-review.json"] == 44
    assert progress["canonical_reaudits_this_session"] == 0
    assert progress["canonical_independent_audit_this_session"] == "NOT_RUN"
    assert progress["notes_units_with_complete_atomic_claim_census"] == 0


def test_stale_question_or_missing_option_cannot_claim_review():
    questions = source_questions()
    record = next(r for r in cohort()["records"] if r["question_id"] == "MA-EXP-0329")
    original = questions[record["question_id"]]
    changed = copy.deepcopy(original)
    changed["choices"][0]["text"] += " Unreviewed addition."
    with pytest.raises(ValueError, match="Stale review"):
        validate_review(changed, record)
    bad = copy.deepcopy(record)
    bad["choice_by_choice_findings"].pop("A")
    with pytest.raises(ValueError, match="Missing choice"):
        validate_review(original, bad)
