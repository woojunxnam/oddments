from __future__ import annotations

from copy import deepcopy

from check_sba_answer_length import analyze_sba_answer_length


def _sba(canonical_question, number: int, keyed_longest: bool) -> dict:
    question = deepcopy(canonical_question)
    question["question_id"] = f"MA-Q-{number:04d}"
    question["question_type"] = "SBA"
    question["correct_choice_ids"] = ["A"]
    question["choices"] = [
        {
            "id": "A",
            "text": (
                "Correct option with wording deliberately longer than every distractor"
                if keyed_longest
                else "Correct option"
            ),
        },
        {"id": "B", "text": "Distractor with deliberately more balanced wording"},
        {"id": "C", "text": "Another distractor"},
        {"id": "D", "text": "Final distractor"},
    ]
    return question


def _baseline(canonical_question) -> list[dict]:
    questions = []
    for index in range(230):
        question = _sba(canonical_question, index + 1, keyed_longest=index < 149)
        question["verification_status"] = "RELEASED"
        question["lifecycle_status"] = "RELEASED"
        questions.append(question)
    return questions


def test_live_baseline_is_measured_exactly() -> None:
    report, failed = analyze_sba_answer_length()
    assert failed is False
    assert report["inherited_baseline"]["sba_count"] == 230
    assert report["inherited_baseline"]["first_longest_keyed"] == 149
    assert report["inherited_baseline"]["first_longest_share"] == 0.647826


def test_inherited_debt_passes_but_prospective_tranche_regression_fails(canonical_question) -> None:
    questions = _baseline(canonical_question)
    questions.extend(_sba(canonical_question, 407 + index, keyed_longest=index < 6) for index in range(10))

    report, failed = analyze_sba_answer_length(questions)

    assert failed is True
    assert any(
        gate["code"] == "PROSPECTIVE_TRANCHE_SHARE" and gate["status"] == "FAIL"
        for gate in report["gates"]
    )


def test_balanced_prospective_tranche_passes(canonical_question) -> None:
    questions = _baseline(canonical_question)
    questions.extend(_sba(canonical_question, 407 + index, keyed_longest=index < 5) for index in range(10))

    report, failed = analyze_sba_answer_length(questions)

    assert failed is False
    assert report["prospective"]["first_longest_share"] == 0.5


def test_individual_extreme_fails_even_before_minimum_sample(canonical_question) -> None:
    questions = _baseline(canonical_question)
    extreme = _sba(canonical_question, 407, keyed_longest=True)
    extreme["choices"][0]["text"] = "This correct answer contains a deliberately excessive number of tokens that makes the key conspicuously longer than every plausible distractor in this item"
    questions.append(extreme)

    report, failed = analyze_sba_answer_length(questions)

    assert failed is True
    assert report["prospective"]["individual_extremes"][0]["question_id"] == "MA-Q-0407"


def test_freeze_mode_requires_minimum_tranche_sample(canonical_question) -> None:
    questions = _baseline(canonical_question)
    questions.append(_sba(canonical_question, 407, keyed_longest=False))

    report, failed = analyze_sba_answer_length(questions, require_prospective_sample=True)

    assert failed is True
    assert any(gate["code"] == "PROSPECTIVE_TRANCHE_SAMPLE" for gate in report["gates"])
