from __future__ import annotations

import argparse
import json

from build_site_data import build_site_payload
from check_answer_distribution import analyze_answer_distribution
from check_structural_patterns import analyze_structural_patterns
from detect_duplicates import detect_duplicates
from qa_common import ROOT, QAReport, load_json, print_report, write_json


def artifact_payloads() -> dict:
    distribution, _ = analyze_answer_distribution()
    structural_patterns, _ = analyze_structural_patterns()
    return {
        ROOT / "duplicate_report.json": detect_duplicates(),
        ROOT / "answer_distribution_report.json": distribution,
        ROOT / "structural_pattern_report.json": structural_patterns,
        ROOT / "site" / "generated" / "questions.json": build_site_payload(include_fixtures=True),
    }


def check_generated_artifacts() -> QAReport:
    report = QAReport()
    for path, expected in artifact_payloads().items():
        if not path.exists() or load_json(path) != expected:
            report.error(f"stale generated artifact: {path.relative_to(ROOT)}; run scripts/generate_artifacts.py --write")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    payloads = artifact_payloads()
    if args.write:
        for path, payload in payloads.items():
            write_json(path, payload)
            print(f"generated {path.relative_to(ROOT)}")
        return 0
    return print_report("generated artifacts", check_generated_artifacts())


if __name__ == "__main__":
    raise SystemExit(main())
