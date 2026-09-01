from __future__ import annotations

import re
from typing import Any

from qa_common import DATA, load_records


BASELINE_MAX_ID = 406
BASELINE_REFERENCE_SBA_COUNT = 230
BASELINE_REFERENCE_FIRST_LONGEST = 149
TRANCHE_SIZE = 33
PROSPECTIVE_MIN_SBA = 10
PROSPECTIVE_MAX_FIRST_LONGEST_SHARE = 0.50
EXTREME_TOKEN_RATIO = 1.6
EXTREME_TOKEN_DELTA = 6


def _number(question: dict[str, Any]) -> int:
    return int(question["question_id"].rsplit("-", 1)[1])


def _first_longest_is_keyed(question: dict[str, Any]) -> bool:
    lengths = {choice["id"]: len(choice["text"]) for choice in question["choices"]}
    maximum = max(lengths.values())
    first_longest = next(choice["id"] for choice in question["choices"] if lengths[choice["id"]] == maximum)
    return first_longest == question["correct_choice_ids"][0]


def _tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*", text)


def _summary(questions: list[dict[str, Any]]) -> dict[str, Any]:
    sba = [question for question in questions if question.get("question_type") == "SBA"]
    keyed = sum(_first_longest_is_keyed(question) for question in sba)
    return {
        "sba_count": len(sba),
        "first_longest_keyed": keyed,
        "first_longest_share": round(keyed / len(sba), 6) if sba else None,
        "question_ids": [question["question_id"] for question in sba],
    }


def _tranches(questions: list[dict[str, Any]], *, first_id: int) -> list[dict[str, Any]]:
    if not questions:
        return []
    maximum = max(_number(question) for question in questions)
    rows = []
    start = first_id
    while start <= maximum:
        scoped = [question for question in questions if start <= _number(question) < start + TRANCHE_SIZE]
        if scoped:
            rows.append(
                {
                    "id_range": f"MA-Q-{start:04d}..MA-Q-{start + TRANCHE_SIZE - 1:04d}",
                    **_summary(scoped),
                }
            )
        start += TRANCHE_SIZE
    return rows


def _extreme_items(questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings = []
    for question in questions:
        if question.get("question_type") != "SBA":
            continue
        key = question["correct_choice_ids"][0]
        lengths = {choice["id"]: len(_tokens(choice["text"])) for choice in question["choices"]}
        correct = lengths[key]
        distractor_max = max(length for choice_id, length in lengths.items() if choice_id != key)
        if correct >= distractor_max * EXTREME_TOKEN_RATIO and correct - distractor_max >= EXTREME_TOKEN_DELTA:
            findings.append(
                {
                    "question_id": question["question_id"],
                    "correct_token_count": correct,
                    "longest_distractor_token_count": distractor_max,
                }
            )
    return findings


def analyze_sba_answer_length(
    questions: list[dict[str, Any]] | None = None,
    *,
    require_prospective_sample: bool = False,
) -> tuple[dict[str, Any], bool]:
    records = questions if questions is not None else [record for _, record in load_records(DATA / "questions")]
    baseline = [
        question
        for question in records
        if _number(question) <= BASELINE_MAX_ID
        and question.get("verification_status") == "RELEASED"
        and question.get("lifecycle_status") == "RELEASED"
    ]
    prospective = [question for question in records if _number(question) > BASELINE_MAX_ID]

    baseline_summary = _summary(baseline)
    prospective_summary = _summary(prospective)
    projected_summary = _summary(baseline + prospective)
    prospective_tranches = _tranches(prospective, first_id=BASELINE_MAX_ID + 1)
    extreme_items = _extreme_items(prospective)
    gates: list[dict[str, Any]] = []

    def gate(code: str, passed: bool, detail: str) -> None:
        gates.append({"code": code, "status": "PASS" if passed else "FAIL", "detail": detail})

    gate(
        "BASELINE_COHORT_INTEGRITY",
        baseline_summary["sba_count"] == BASELINE_REFERENCE_SBA_COUNT,
        f"Expected {BASELINE_REFERENCE_SBA_COUNT} RELEASED SBA items through MA-Q-{BASELINE_MAX_ID:04d}; observed {baseline_summary['sba_count']}.",
    )
    gate(
        "INHERITED_DEBT_NON_REGRESSION",
        baseline_summary["first_longest_keyed"] <= BASELINE_REFERENCE_FIRST_LONGEST,
        f"Inherited cohort may improve but must not exceed {BASELINE_REFERENCE_FIRST_LONGEST}/{BASELINE_REFERENCE_SBA_COUNT}; observed {baseline_summary['first_longest_keyed']}/{baseline_summary['sba_count']}.",
    )

    for tranche in prospective_tranches:
        enough = tranche["sba_count"] >= PROSPECTIVE_MIN_SBA
        if enough:
            gate(
                "PROSPECTIVE_TRANCHE_SHARE",
                tranche["first_longest_share"] <= PROSPECTIVE_MAX_FIRST_LONGEST_SHARE,
                f"{tranche['id_range']} must be <= {PROSPECTIVE_MAX_FIRST_LONGEST_SHARE:.0%}; observed {tranche['first_longest_keyed']}/{tranche['sba_count']} ({tranche['first_longest_share']:.1%}).",
            )
        elif require_prospective_sample:
            gate(
                "PROSPECTIVE_TRANCHE_SAMPLE",
                False,
                f"{tranche['id_range']} has {tranche['sba_count']} SBA items; at least {PROSPECTIVE_MIN_SBA} are required at freeze.",
            )

    projected_pass = (
        projected_summary["first_longest_keyed"] * BASELINE_REFERENCE_SBA_COUNT
        <= BASELINE_REFERENCE_FIRST_LONGEST * projected_summary["sba_count"]
    )
    gate(
        "PROJECTED_BANK_NON_REGRESSION",
        projected_pass,
        f"Projected bank must not exceed {BASELINE_REFERENCE_FIRST_LONGEST}/{BASELINE_REFERENCE_SBA_COUNT}; observed {projected_summary['first_longest_keyed']}/{projected_summary['sba_count']}.",
    )
    gate(
        "PROSPECTIVE_INDIVIDUAL_EXTREMES",
        not extreme_items,
        f"Found {len(extreme_items)} prospective SBA item(s) at or above both the {EXTREME_TOKEN_RATIO:.1f}x and +{EXTREME_TOKEN_DELTA}-token thresholds.",
    )

    failed = any(item["status"] == "FAIL" for item in gates)
    report = {
        "metric": {
            "aggregate": "Correct choice is the first choice among those tied for maximum character length.",
            "tie_policy": "Choice order is canonical repository order; a tied keyed option counts only when it appears first among the tied maxima.",
            "individual_extreme": "Correct-option token count is at least 1.6x and six tokens longer than the longest distractor.",
        },
        "threshold_basis": {
            "baseline_reference": f"{BASELINE_REFERENCE_FIRST_LONGEST}/{BASELINE_REFERENCE_SBA_COUNT}",
            "historical_33_id_tranches": _tranches(baseline, first_id=11),
            "rationale": "The 50% prospective ceiling is materially below the 64.78% inherited rate and is consistent with the improved recent 33-ID cohorts (42.9%, 22.2%, 52.6%, 42.1%).",
        },
        "thresholds": {
            "baseline_max_id": BASELINE_MAX_ID,
            "prospective_min_sba_per_tranche": PROSPECTIVE_MIN_SBA,
            "prospective_max_first_longest_share": PROSPECTIVE_MAX_FIRST_LONGEST_SHARE,
            "extreme_token_ratio": EXTREME_TOKEN_RATIO,
            "extreme_token_delta": EXTREME_TOKEN_DELTA,
        },
        "inherited_baseline": baseline_summary,
        "prospective": {
            **prospective_summary,
            "tranches": prospective_tranches,
            "individual_extremes": extreme_items,
        },
        "projected_bank": projected_summary,
        "gates": gates,
        "severity": "ERROR" if failed else "PASS",
    }
    return report, failed


if __name__ == "__main__":
    result, failed = analyze_sba_answer_length()
    print(
        "SBA answer length: "
        f"{result['severity']} inherited={result['inherited_baseline']['first_longest_keyed']}/{result['inherited_baseline']['sba_count']} "
        f"prospective={result['prospective']['first_longest_keyed']}/{result['prospective']['sba_count']}"
    )
    for item in result["gates"]:
        print(f"{item['status']} [{item['code']}] {item['detail']}")
    raise SystemExit(1 if failed else 0)
