from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from qa_common import DATA, ROOT, chi_square_uniform, load_records, write_json


WARNING_P = 0.05
ERROR_P = 0.001
MIN_ERROR_SAMPLE = 40
MAX_SHARE_WARNING = 0.40
MAX_SHARE_ERROR = 0.55


def analyze_answer_distribution() -> tuple[dict, bool]:
    counts = Counter({letter: 0 for letter in "ABCDE"})
    for _, question in load_records(DATA / "questions"):
        if question.get("question_type") == "SBA" and len(question.get("correct_choice_ids", [])) == 1:
            counts[question["correct_choice_ids"][0]] += 1
    total = sum(counts.values())
    chi_square, degrees, p_value = chi_square_uniform(dict(counts))
    max_share = max(counts.values(), default=0) / total if total else 0.0
    severity = "PASS"
    failed = False
    if total >= MIN_ERROR_SAMPLE and (p_value < ERROR_P or max_share > MAX_SHARE_ERROR):
        severity = "ERROR"
        failed = True
    elif total >= 10 and (p_value < WARNING_P or max_share > MAX_SHARE_WARNING):
        severity = "WARNING"
    report = {
        "sba_count": total,
        "frequencies": dict(counts),
        "chi_square": round(chi_square, 6),
        "degrees_of_freedom": degrees,
        # libm implementations can differ in the final floating-point bits.
        # Quantize tracked output so Windows and Linux regenerate byte-identical JSON.
        "p_value_approx": round(p_value, 12),
        "max_answer_share": round(max_share, 6),
        "severity": severity,
        "thresholds": {
            "warning_p": WARNING_P,
            "error_p": ERROR_P,
            "minimum_error_sample": MIN_ERROR_SAMPLE,
            "max_share_warning": MAX_SHARE_WARNING,
            "max_share_error": MAX_SHARE_ERROR,
        },
        "note": "Choice shuffling does not excuse a structurally biased canonical bank.",
    }
    return report, failed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "answer_distribution_report.json")
    args = parser.parse_args()
    report, failed = analyze_answer_distribution()
    write_json(args.output, report)
    print(
        "answer distribution: "
        f"{report['severity']} n={report['sba_count']} frequencies={report['frequencies']} "
        f"chi2={report['chi_square']} p~{report['p_value_approx']:.6g}"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
