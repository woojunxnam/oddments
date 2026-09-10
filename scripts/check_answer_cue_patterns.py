"""Flag structural cues that let a candidate pick an SBA key without doing the legal work.

MA-Q-0426 failed its independent realism review twice on wording_not_guessable. The
second failure was structural rather than verbal: exactly one of five options said the
arrangement was not permitted while the other four validated or excused it, so the key
was selectable on polarity alone. That shape is mechanically detectable.

Two signals:

  POLARITY_SINGLETON  Every option but one asserts the same permissive/prohibitive
                      direction, the odd one out is the key, and the item asks which
                      assessment is correct. A test-wise candidate picks the singleton.
  KEY_RULE_ECHO       The keyed option reuses markedly more distinctive vocabulary from
                      its own canonical rule summaries than any distractor does, so the
                      key can be matched by recalling the rule text rather than applying it.

Neither is an error. A prohibition question may legitimately have one lawful answer, and
a key may legitimately track a regulation's operative words. They are drafting signals:
answer them before a freeze is spent on an independent auditor.

    python scripts/check_answer_cue_patterns.py
    python scripts/check_answer_cue_patterns.py --question MA-Q-0426
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, QAReport, load_records

PROHIBITIVE = (
    "may not", "must not", "cannot", "can not", "shall not", "is prohibited", "are prohibited",
    "prohibits", "impermissible", "not permissible", "not permitted", "not allowed",
    "does not authorize", "do not authorize", "not authorized", "unlawful", "violates",
    "violation", "must refuse", "must decline", "may refuse", "must not be",
)
PERMISSIVE = (
    "is permissible", "are permissible", "is permitted", "are permitted", "is acceptable",
    "acceptable", "authorizes", "authorize the", "may dispense", "may fill", "may be filled",
    "no violation", "controls", "is engaged", "permits",
)
# Tuned against the 272 released SBA items so the echo signal reports outliers rather
# than the ordinary case: a key naturally shares some vocabulary with its own rule.
# min 5 / ratio 2.0 fires on 22% of the bank, min 7 / ratio 3.0 on 3.7%.
ECHO_MIN_OVERLAP = 7
ECHO_MIN_RATIO = 3.0

STOPWORDS = frozenset(
    """a an the and or of to in for on by with as is are be been being that this those these it its
    not no any all each may must shall can when where which who whom whose if then than from at into
    under over per such other same only also more most less least both either neither"""
    .split()
)


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:['-][a-z0-9]+)*", (text or "").lower())


def _content_tokens(text: str) -> set[str]:
    return {token for token in _tokens(text) if token not in STOPWORDS and len(token) > 3}


def option_polarity(text: str) -> str:
    lowered = (text or "").lower()
    prohibitive = any(marker in lowered for marker in PROHIBITIVE)
    permissive = any(marker in lowered for marker in PERMISSIVE)
    if prohibitive and not permissive:
        return "PROHIBITIVE"
    if permissive and not prohibitive:
        return "PERMISSIVE"
    return "NEUTRAL"


def analyze_answer_cues(
    questions: dict[str, dict[str, Any]] | None = None,
    rules: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if rules is None:
        rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}
    if questions is None:
        questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}

    findings: list[dict[str, Any]] = []
    scoped = [q for q in questions.values() if q.get("question_type") == "SBA" and len(q.get("choices", [])) >= 4]

    for question in sorted(scoped, key=lambda q: q["question_id"]):
        key = question["correct_choice_ids"][0]
        choices = {choice["id"]: choice["text"] for choice in question["choices"]}

        polarities = {choice_id: option_polarity(text) for choice_id, text in choices.items()}
        others = [p for choice_id, p in polarities.items() if choice_id != key]
        key_polarity = polarities[key]
        opposite = "PERMISSIVE" if key_polarity == "PROHIBITIVE" else "PROHIBITIVE"
        # The cue is that no distractor shares the key's direction, not that every
        # distractor states the opposite one. A distractor that merely excuses the actor
        # reads as neutral here but still leaves the key as the lone dissenting option.
        if (
            key_polarity != "NEUTRAL"
            and others
            and not any(p == key_polarity for p in others)
            and sum(1 for p in others if p == opposite) >= len(others) / 2
        ):
            findings.append(
                {
                    "code": "POLARITY_SINGLETON",
                    "question_id": question["question_id"],
                    "detail": (
                        f"key {key} is the only {key_polarity.lower()} option; of the other "
                        f"{len(others)}, {sum(1 for p in others if p == opposite)} are "
                        f"{opposite.lower()} and none dissent"
                    ),
                }
            )

        rule_vocabulary: set[str] = set()
        for rule_id in question.get("rule_ids", []):
            rule = rules.get(rule_id)
            if rule:
                rule_vocabulary |= _content_tokens(rule.get("rule_summary", ""))
        if rule_vocabulary:
            overlaps = {
                choice_id: len(_content_tokens(text) & rule_vocabulary)
                for choice_id, text in choices.items()
            }
            key_overlap = overlaps[key]
            distractor_max = max(value for choice_id, value in overlaps.items() if choice_id != key)
            if key_overlap >= ECHO_MIN_OVERLAP and key_overlap >= distractor_max * ECHO_MIN_RATIO:
                findings.append(
                    {
                        "code": "KEY_RULE_ECHO",
                        "question_id": question["question_id"],
                        "detail": (
                            f"key {key} shares {key_overlap} distinctive term(s) with its rule "
                            f"summaries against {distractor_max} for the closest distractor"
                        ),
                    }
                )

    by_question: dict[str, list[str]] = {}
    for finding in findings:
        by_question.setdefault(finding["question_id"], []).append(finding["code"])

    return {
        "scope": "canonical SBA questions",
        "sba_count": len(scoped),
        "finding_count": len(findings),
        "flagged_question_count": len(by_question),
        "findings": findings,
    }


def answer_cue_report(
    report_data: dict[str, Any] | None = None,
    questions: dict[str, dict[str, Any]] | None = None,
) -> QAReport:
    """Warn only about content that has not yet passed an independent audit.

    These are pre-freeze drafting gates. A released item already survived a fresh
    auditor, so re-flagging it on every validate_all run is noise, not signal.
    """
    report = QAReport()
    data = report_data or analyze_answer_cues()
    if questions is None:
        questions = {record["question_id"]: record for _, record in load_records(DATA / "questions")}
    pending = [
        finding
        for finding in data["findings"]
        if questions.get(finding["question_id"], {}).get("lifecycle_status") != "RELEASED"
    ]
    for finding in pending:
        report.warn(
            f"{finding['question_id']} is unreleased and shows an answer cue: "
            f"{finding['code']} - {finding['detail']}"
        )
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", help="only report this question id")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    data = analyze_answer_cues()
    if args.question:
        data["findings"] = [f for f in data["findings"] if f["question_id"] == args.question]
        data["finding_count"] = len(data["findings"])

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    for finding in data["findings"]:
        print(f"{finding['question_id']}  {finding['code']:20s} {finding['detail']}")
    print(
        f"\nanswer cue patterns: {data['finding_count']} finding(s) across "
        f"{data['flagged_question_count']} of {data['sba_count']} SBA item(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
