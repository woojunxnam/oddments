from __future__ import annotations

import argparse
from collections import defaultdict
from difflib import SequenceMatcher
from itertools import combinations
from pathlib import Path
from typing import Any

from qa_common import DATA, ROOT, load_records, normalize_text, token_jaccard, write_json


DEFAULT_THRESHOLD = 0.82


def option_signature(question: dict[str, Any]) -> tuple[str, ...]:
    return tuple(sorted(normalize_text(choice.get("text", ""), normalize_numbers=True) for choice in question.get("choices", [])))


def detect_duplicates(threshold: float = DEFAULT_THRESHOLD) -> dict[str, Any]:
    records = [record for _, record in load_records(DATA / "questions")]
    exact_groups: dict[str, list[str]] = defaultdict(list)
    numeric_groups: dict[str, list[str]] = defaultdict(list)
    option_groups: dict[tuple[str, ...], list[str]] = defaultdict(list)
    for question in records:
        qid = question["question_id"]
        exact_groups[normalize_text(question["stem"])].append(qid)
        numeric_groups[normalize_text(question["stem"], normalize_numbers=True)].append(qid)
        option_groups[option_signature(question)].append(qid)

    pairs: dict[tuple[str, str], dict[str, Any]] = {}

    def add_pair(left: str, right: str, kind: str, score: float, family: str) -> None:
        key = tuple(sorted((left, right)))
        entry = pairs.setdefault(
            key,
            {
                "question_ids": list(key),
                "match_types": [],
                "similarity_score": 0.0,
                "family_suggestion": family,
                "recommended_manual_review": True,
            },
        )
        entry["match_types"].append(kind)
        entry["similarity_score"] = max(entry["similarity_score"], round(score, 4))

    for groups, kind, score in (
        (exact_groups, "EXACT_STEM", 1.0),
        (numeric_groups, "NORMALIZED_NUMERIC_STEM", 0.99),
        (option_groups, "SAME_OPTION_SET", 0.98),
    ):
        for _, ids in groups.items():
            if len(ids) < 2:
                continue
            question_by_id = {question["question_id"]: question for question in records}
            for left, right in combinations(sorted(ids), 2):
                family = question_by_id[left].get("family_id") or question_by_id[right].get("family_id") or "MANUAL_REVIEW"
                add_pair(left, right, kind, score, family)

    for left, right in combinations(records, 2):
        left_stem = left["stem"]
        right_stem = right["stem"]
        sequence = SequenceMatcher(
            None,
            normalize_text(left_stem, normalize_numbers=True),
            normalize_text(right_stem, normalize_numbers=True),
            autojunk=False,
        ).ratio()
        jaccard = token_jaccard(left_stem, right_stem)
        combined = (sequence + jaccard) / 2
        if combined >= threshold:
            add_pair(
                left["question_id"],
                right["question_id"],
                "FUZZY_LOCAL",
                combined,
                left.get("family_id") if left.get("family_id") == right.get("family_id") else "MANUAL_REVIEW",
            )

    findings = sorted(pairs.values(), key=lambda item: (-item["similarity_score"], item["question_ids"]))
    return {
        "config": {
            "method": "exact, numeric normalization, option-set equality, SequenceMatcher plus token Jaccard",
            "fuzzy_threshold": threshold,
            "deterministic": True,
            "auto_delete": False,
        },
        "question_count": len(records),
        "finding_count": len(findings),
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    parser.add_argument("--output", type=Path, default=ROOT / "duplicate_report.json")
    args = parser.parse_args()
    report = detect_duplicates(args.threshold)
    write_json(args.output, report)
    print(f"duplicate detector: {report['finding_count']} finding(s); report={args.output}")
    return 1 if report["finding_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
