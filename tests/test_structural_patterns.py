from __future__ import annotations

from copy import deepcopy


def _question(canonical_question, question_id: str, stem: str) -> dict:
    question = deepcopy(canonical_question)
    question["question_id"] = question_id
    question["stem"] = stem
    question["question_type"] = "SBA"
    question["correct_choice_ids"] = ["A"]
    return question


def test_repeated_distractor_template_is_rejected(canonical_question) -> None:
    from check_structural_patterns import analyze_structural_patterns

    phrase = "This repeated distractor phrase deliberately crosses the ten token detector threshold today."
    questions = []
    for index in range(3):
        question = _question(canonical_question, f"MA-Q-99{index:02d}", f"Unique stem number {index} asks a distinct legal question.")
        question["choices"][1]["text"] = f"{phrase} Variant {index}."
        questions.append(question)
    report, failed = analyze_structural_patterns(questions)
    assert failed is True
    assert any(finding["code"] == "REPEATED_DISTRACTOR_TEMPLATE" for finding in report["findings"])


def test_concentrated_sata_keys_are_rejected(canonical_question) -> None:
    from check_structural_patterns import analyze_structural_patterns

    questions = []
    for index in range(10):
        question = _question(canonical_question, f"MA-Q-98{index:02d}", f"SATA scenario {index} has distinct operative facts.")
        question["question_type"] = "SATA"
        question["correct_choice_ids"] = ["A", "B", "C"]
        for choice_index, choice in enumerate(question["choices"]):
            choice["text"] = f"Proposition {choice_index} for scenario {index} uses unique facts and legal consequences."
        questions.append(question)
    report, failed = analyze_structural_patterns(questions)
    assert failed is True
    codes = {finding["code"] for finding in report["findings"]}
    assert "SATA_KEY_CONCENTRATION" in codes
    assert "SATA_CORRECT_COUNT_CONCENTRATION" in codes


def test_reused_ordered_response_key_is_rejected(canonical_question) -> None:
    from check_structural_patterns import analyze_structural_patterns

    questions = []
    for index in range(2):
        question = _question(canonical_question, f"MA-Q-97{index:02d}", f"Ordered scenario {index} uses a separate chronology.")
        question["question_type"] = "ORDERED_RESPONSE"
        question["correct_choice_ids"] = ["C", "A", "E", "B", "D"]
        for choice_index, choice in enumerate(question["choices"]):
            choice["text"] = f"Event {choice_index} in chronology {index} has a unique factual marker."
        questions.append(question)
    report, failed = analyze_structural_patterns(questions)
    assert failed is True
    assert any(finding["code"] == "ORDERED_RESPONSE_KEY_REUSE" for finding in report["findings"])
