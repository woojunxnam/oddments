"""Flag canonical law that sits inside a Study Guide section's declared scope but is not used.

Every Study Guide section audited so far has failed on the same thing: a controlling
provision missing from inside the section's own declared scope. That failure mode is
mechanically detectable before a freeze is spent, because the canonical rule records
already carry area, topic, subtopic and pinpoint authority citations.

Three signals, all deterministic:

  TOPIC_NEIGHBOUR      A CURRENT verified rule shares (area, topic) with a rule the
                       section already depends on, but the section does not cite it.
  AUTHORITY_NEIGHBOUR  A CURRENT verified rule cites the same parent provision as a
                       rule the section already depends on -- 247 CMR 9.04(12) beside
                       9.04(13), 21 CFR 1306.08 beside 1306.25 -- but is not cited.
  UNUSED_AUTHORITY     A rule the section cites carries an authority whose citation
                       never appears in the section prose, so the section leans on the
                       rule while using only part of what it stands for.

None of these is an error on its own. A neighbour can be genuinely out of scope, and a
section may legitimately rely on one half of a rule. They are drafting signals: answer
each one before freezing, or expect an independent auditor to raise it.

    python scripts/check_study_guide_scope_coverage.py
    python scripts/check_study_guide_scope_coverage.py --section SG-CII-LIFECYCLE
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, QAReport, VERIFIED_RULE_STATUSES, load_records, print_report
from study_guide_common import STUDY_GUIDE_HASH_FIELDS

NARROW_TOPIC_MAX = 6

PROSE_FIELDS = (
    "title",
    "topic",
    "subtopic",
    "learning_objectives",
    "quick_review",
    "decision_logic",
    "ma_vs_federal",
    "exceptions",
    "timing_deadlines",
    "forms_records",
    "role_duties",
    "common_traps",
    "drug_examples",
)

# "247 CMR 9.04(13)" -> "247 CMR 9.04"; "21 CFR 1306.13(b)(1)-(b)(2)" -> "21 CFR 1306.13";
# "M.G.L. c. 94C, s. 18(d3/4), read with s. 18(d)" -> "M.G.L. c. 94C, s. 18".
CITATION_PATTERNS = (
    re.compile(r"\b(\d{2,3}\s*CMR\s*\d+\.\d+)", re.IGNORECASE),
    re.compile(r"\b(\d{1,2}\s*CFR\s*\d+\.\d+)", re.IGNORECASE),
    re.compile(r"(M\.?G\.?L\.?\s*c\.?\s*\d+[A-Z]?\s*,?\s*(?:s\.|§)\s*\d+[A-Z]?)", re.IGNORECASE),
)


def _normalize_citation(text: str) -> str:
    return re.sub(r"[\s.,§]+", " ", text).strip().lower().replace("m g l ", "mgl ")


def parent_citations(text: str) -> set[str]:
    """Pinpoint-free parent provisions mentioned anywhere in `text`."""
    found: set[str] = set()
    for pattern in CITATION_PATTERNS:
        for match in pattern.finditer(text or ""):
            found.add(_normalize_citation(match.group(1)))
    return found


def section_prose(section: dict[str, Any]) -> str:
    chunks: list[str] = []
    for field in PROSE_FIELDS:
        value = section.get(field)
        if isinstance(value, str):
            chunks.append(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    chunks.append(item)
                elif isinstance(item, dict):
                    chunks.extend(str(v) for k, v in item.items() if k != "rule_ids")
    return "\n".join(chunks)


def rule_citations(rule: dict[str, Any]) -> set[str]:
    citations: set[str] = set()
    for authority in rule.get("authority", []):
        citations |= parent_citations(authority.get("section", ""))
    return citations


def analyze_scope_coverage(
    sections: dict[str, dict[str, Any]] | None = None,
    rules: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if rules is None:
        rules = {record["rule_id"]: record for _, record in load_records(DATA / "rules")}
    if sections is None:
        sections = {
            record["section_id"]: record
            for _, record in load_records(DATA / "study_guide" / "sections")
        }

    usable = {
        rule_id: rule
        for rule_id, rule in rules.items()
        if rule.get("status") == "CURRENT" and rule.get("verification_status") in VERIFIED_RULE_STATUSES
    }
    citations_by_rule = {rule_id: rule_citations(rule) for rule_id, rule in usable.items()}

    # A topic shared by many rules is a weak scope signal; one shared by a handful is a
    # strong one. "Dispensing requirements" holds dozens of unrelated rules, while
    # "Prescription transfer" holds three that genuinely belong together.
    topic_sizes: dict[tuple[int, str], int] = {}
    for rule in usable.values():
        key = (rule["area"], rule["topic"])
        topic_sizes[key] = topic_sizes.get(key, 0) + 1

    section_rows = []
    for section_id, section in sorted(sections.items()):
        cited = [rule_id for rule_id in section.get("rule_ids", []) if rule_id in usable]
        areas = set(section.get("areas", []))
        prose = section_prose(section)
        prose_citations = parent_citations(prose)

        cited_topics = {(usable[rule_id]["area"], usable[rule_id]["topic"]) for rule_id in cited}
        cited_citations: set[str] = set()
        for rule_id in cited:
            cited_citations |= citations_by_rule[rule_id]

        findings: list[dict[str, Any]] = []
        for rule_id, rule in sorted(usable.items()):
            if rule_id in section.get("rule_ids", []):
                continue
            if areas and rule["area"] not in areas:
                continue
            topic_key = (rule["area"], rule["topic"])
            if topic_key in cited_topics:
                narrow = topic_sizes.get(topic_key, 0) <= NARROW_TOPIC_MAX
                findings.append(
                    {
                        "code": "TOPIC_NEIGHBOUR",
                        "strength": "MEDIUM" if narrow else "LOW",
                        "rule_id": rule_id,
                        "detail": (
                            f"shares area {rule['area']} topic {rule['topic']!r} with a cited rule "
                            f"({topic_sizes.get(topic_key, 0)} rule(s) carry that topic)"
                        ),
                        "authority": [a.get("section") for a in rule.get("authority", [])],
                    }
                )
                continue
            shared = citations_by_rule[rule_id] & cited_citations
            if shared:
                findings.append(
                    {
                        "code": "AUTHORITY_NEIGHBOUR",
                        "strength": "HIGH",
                        "rule_id": rule_id,
                        "detail": f"cites the same parent provision as a dependency: {sorted(shared)}",
                        "authority": [a.get("section") for a in rule.get("authority", [])],
                    }
                )

        for rule_id in cited:
            for authority in usable[rule_id].get("authority", []):
                pinpoints = parent_citations(authority.get("section", ""))
                if pinpoints and not (pinpoints & prose_citations):
                    findings.append(
                        {
                            "code": "UNUSED_AUTHORITY",
                            "strength": "HIGH",
                            "rule_id": rule_id,
                            "detail": (
                                f"dependency authority {authority.get('section')!r} is never "
                                "referenced in the section prose"
                            ),
                            "authority": [authority.get("section")],
                        }
                    )

        order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        findings.sort(key=lambda f: (order[f["strength"]], f["code"], f["rule_id"]))
        actionable = [f for f in findings if f["strength"] != "LOW"]
        section_rows.append(
            {
                "section_id": section_id,
                "verification_status": section.get("verification_status"),
                "cited_rule_count": len(cited),
                "finding_count": len(findings),
                "actionable_count": len(actionable),
                "findings": findings,
            }
        )

    return {
        "scope": "canonical study guide sections",
        "usable_rule_count": len(usable),
        "section_count": len(section_rows),
        "finding_count": sum(row["finding_count"] for row in section_rows),
        "actionable_count": sum(row["actionable_count"] for row in section_rows),
        "sections": section_rows,
    }


def scope_coverage_report(report_data: dict[str, Any] | None = None) -> QAReport:
    """Warn only about sections that have not yet passed an independent audit.

    This is a pre-freeze drafting gate. A VERIFIED section already survived a fresh
    auditor at its exact hash, so re-flagging it on every validate_all run is noise.
    """
    report = QAReport()
    data = report_data or analyze_scope_coverage()
    for row in data["sections"]:
        if row["verification_status"] == "VERIFIED" or not row["actionable_count"]:
            continue
        codes = sorted({f["code"] for f in row["findings"] if f["strength"] != "LOW"})
        report.warn(
            f"{row['section_id']} is unpublished with {row['actionable_count']} unused in-scope "
            f"canonical signal(s) ({', '.join(codes)}); review before freezing"
        )
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--section", help="only report this section id")
    parser.add_argument("--json", action="store_true", help="print the full machine-readable report")
    parser.add_argument("--all", action="store_true", help="include LOW-strength topic neighbours")
    args = parser.parse_args()

    data = analyze_scope_coverage()
    if args.section:
        data["sections"] = [row for row in data["sections"] if row["section_id"] == args.section]
        data["finding_count"] = sum(row["finding_count"] for row in data["sections"])
        data["actionable_count"] = sum(row["actionable_count"] for row in data["sections"])

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    for row in data["sections"]:
        shown = row["findings"] if args.all else [f for f in row["findings"] if f["strength"] != "LOW"]
        print(f"\n{row['section_id']}  [{row['verification_status']}]  "
              f"{row['cited_rule_count']} cited rule(s), {row['actionable_count']} actionable "
              f"of {row['finding_count']} signal(s)")
        for finding in shown:
            print(f"   [{finding['strength']:6s}] {finding['code']:20s} {finding['rule_id']}")
            print(f"      {finding['detail']}")
            if finding["authority"]:
                print(f"      authority: {finding['authority']}")
    print(f"\nstudy guide scope coverage: {data['actionable_count']} actionable of "
          f"{data['finding_count']} signal(s) across {data['section_count']} section(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
