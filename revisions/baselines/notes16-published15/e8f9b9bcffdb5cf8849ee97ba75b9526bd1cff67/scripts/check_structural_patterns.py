from __future__ import annotations

from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable

from qa_common import DATA, load_records, normalize_text, token_jaccard


PHASE2_IDS = {f"MA-Q-{number:04d}" for number in range(11, 10000)}
NGRAM_SIZE = 10


def _tokens(text: str) -> list[str]:
    return normalize_text(text, normalize_numbers=True).split()


def _ngrams(text: str, size: int = NGRAM_SIZE) -> set[str]:
    tokens = _tokens(text)
    return {" ".join(tokens[index : index + size]) for index in range(len(tokens) - size + 1)}


def _choice_signature(question: dict[str, Any]) -> tuple[str, ...]:
    return tuple(sorted(normalize_text(choice["text"], normalize_numbers=True) for choice in question["choices"]))


def _phase2_questions(data_root: Path) -> list[dict[str, Any]]:
    records = [record for _, record in load_records(data_root / "questions")]
    return [record for record in records if record.get("question_id") in PHASE2_IDS]


def _repeated_ngrams(
    texts: Iterable[tuple[str, str]], *, minimum_questions: int
) -> list[dict[str, Any]]:
    owners: dict[str, set[str]] = defaultdict(set)
    for question_id, value in texts:
        for ngram in _ngrams(value):
            owners[ngram].add(question_id)
    findings = []
    for ngram, question_ids in owners.items():
        if len(question_ids) >= minimum_questions:
            findings.append(
                {
                    "ngram": ngram,
                    "question_ids": sorted(question_ids),
                    "question_count": len(question_ids),
                }
            )
    return sorted(findings, key=lambda item: (-item["question_count"], item["ngram"]))


def analyze_structural_patterns(
    questions: list[dict[str, Any]] | None = None, *, data_root: Path = DATA
) -> tuple[dict[str, Any], bool]:
    scoped = questions if questions is not None else _phase2_questions(data_root)
    findings: list[dict[str, Any]] = []

    option_sets: dict[tuple[str, ...], list[str]] = defaultdict(list)
    for question in scoped:
        option_sets[_choice_signature(question)].append(question["question_id"])
    for question_ids in option_sets.values():
        if len(question_ids) > 1:
            findings.append(
                {
                    "code": "REPEATED_OPTION_SET",
                    "question_ids": sorted(question_ids),
                    "detail": "Two or more items reuse the same normalized option set.",
                }
            )

    distractor_texts = []
    explanation_texts = []
    for question in scoped:
        correct = set(question["correct_choice_ids"])
        distractor_texts.extend(
            (question["question_id"], choice["text"])
            for choice in question["choices"]
            if choice["id"] not in correct
        )
        explanation = question.get("explanation", {})
        explanation_texts.append((question["question_id"], explanation.get("core_reasoning", "")))
        explanation_texts.extend(
            (question["question_id"], value)
            for value in explanation.get("choice_analysis", {}).values()
        )
        explanation_texts.append((question["question_id"], explanation.get("mpje_trap", "")))

    repeated_distractors = _repeated_ngrams(distractor_texts, minimum_questions=3)
    if repeated_distractors:
        findings.append(
            {
                "code": "REPEATED_DISTRACTOR_TEMPLATE",
                "detail": "A ten-token distractor phrase occurs in at least three questions.",
                "examples": repeated_distractors[:10],
            }
        )

    repeated_explanations = _repeated_ngrams(explanation_texts, minimum_questions=4)
    if repeated_explanations:
        findings.append(
            {
                "code": "REPEATED_EXPLANATION_TEMPLATE",
                "detail": "A ten-token explanation phrase occurs in at least four questions.",
                "examples": repeated_explanations[:10],
            }
        )

    near_duplicate_pairs = []
    for left_index, left in enumerate(scoped):
        for right in scoped[left_index + 1 :]:
            left_stem = normalize_text(left["stem"], normalize_numbers=True)
            right_stem = normalize_text(right["stem"], normalize_numbers=True)
            sequence = SequenceMatcher(None, left_stem, right_stem).ratio()
            jaccard = token_jaccard(left["stem"], right["stem"])
            if sequence >= 0.82 or jaccard >= 0.76:
                near_duplicate_pairs.append(
                    {
                        "question_ids": [left["question_id"], right["question_id"]],
                        "sequence_ratio": round(sequence, 4),
                        "token_jaccard": round(jaccard, 4),
                    }
                )
    if near_duplicate_pairs:
        findings.append(
            {
                "code": "NEAR_DUPLICATE_STEM",
                "detail": "A normalized stem pair crosses the structural similarity threshold.",
                "examples": near_duplicate_pairs[:10],
            }
        )

    sata = [question for question in scoped if question["question_type"] == "SATA"]
    sata_patterns = Counter("".join(sorted(question["correct_choice_ids"])) for question in sata)
    sata_counts = Counter(len(question["correct_choice_ids"]) for question in sata)
    if len(sata) >= 10:
        top_pattern, top_pattern_count = sata_patterns.most_common(1)[0]
        if top_pattern_count / len(sata) > 0.25:
            findings.append(
                {
                    "code": "SATA_KEY_CONCENTRATION",
                    "detail": f"SATA key {top_pattern} occurs {top_pattern_count}/{len(sata)} times.",
                }
            )
        top_count, top_count_frequency = sata_counts.most_common(1)[0]
        if top_count_frequency / len(sata) > 0.55:
            findings.append(
                {
                    "code": "SATA_CORRECT_COUNT_CONCENTRATION",
                    "detail": f"SATA correct-count {top_count} occurs {top_count_frequency}/{len(sata)} times.",
                }
            )

    ordered = [question for question in scoped if question["question_type"] == "ORDERED_RESPONSE"]
    ordered_patterns = Counter("".join(question["correct_choice_ids"]) for question in ordered)
    repeated_ordered = {pattern: count for pattern, count in ordered_patterns.items() if count > 1}
    if repeated_ordered:
        findings.append(
            {
                "code": "ORDERED_RESPONSE_KEY_REUSE",
                "detail": "Ordered-response answer orders must not repeat.",
                "patterns": repeated_ordered,
            }
        )

    sba_length_leaks = []
    for question in scoped:
        if question["question_type"] != "SBA":
            continue
        correct_id = question["correct_choice_ids"][0]
        lengths = {choice["id"]: len(_tokens(choice["text"])) for choice in question["choices"]}
        correct_length = lengths[correct_id]
        distractor_max = max(length for choice_id, length in lengths.items() if choice_id != correct_id)
        if correct_length >= distractor_max * 1.6 and correct_length - distractor_max >= 6:
            sba_length_leaks.append(
                {
                    "question_id": question["question_id"],
                    "correct_length": correct_length,
                    "longest_distractor": distractor_max,
                }
            )
    if sba_length_leaks:
        findings.append(
            {
                "code": "SBA_ANSWER_LENGTH_LEAKAGE",
                "detail": "A correct SBA option is materially longer than every distractor.",
                "examples": sba_length_leaks,
            }
        )

    report = {
        "scope": "MA-Q-0011+" if questions is None else "provided questions",
        "question_count": len(scoped),
        "thresholds": {
            "ngram_size": NGRAM_SIZE,
            "distractor_minimum_questions": 3,
            "explanation_minimum_questions": 4,
            "stem_sequence_ratio": 0.82,
            "stem_token_jaccard": 0.76,
            "sata_key_max_share": 0.25,
            "sata_correct_count_max_share": 0.55,
            "sba_correct_length_ratio": 1.6,
            "sba_correct_length_delta": 6,
        },
        "distributions": {
            "question_types": dict(sorted(Counter(question["question_type"] for question in scoped).items())),
            "sata_answer_sets": dict(sorted(sata_patterns.items())),
            "sata_correct_counts": {str(key): value for key, value in sorted(sata_counts.items())},
            "ordered_response_keys": dict(sorted(ordered_patterns.items())),
        },
        "finding_count": len(findings),
        "findings": findings,
        "severity": "PASS" if not findings else "ERROR",
    }
    return report, bool(findings)


if __name__ == "__main__":
    result, failed = analyze_structural_patterns()
    print(f"structural patterns: {result['finding_count']} finding(s)")
    for finding in result["findings"]:
        print(f"ERROR [{finding['code']}] {finding['detail']}")
    raise SystemExit(1 if failed else 0)
