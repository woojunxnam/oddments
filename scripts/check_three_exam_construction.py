"""Assemble three distinct 120-question mock exams from the released pool, sharing no question.

The blueprint's per-area minima are the product of one exam's allocation and the number of exams the
bank is meant to support: 26/40/29/25 per exam, three exams, giving 78/120/87/75. The final coverage
gate builds ONE mock and proves the bank can seat it; it does not prove three can be seated at once
out of the same pool, which is the property the minima actually encode.

This check builds all three against a single used-set, so a question drawn into exam 1 is gone for
exams 2 and 3. It reports, per exam, the area allocation, the heaviest family, and whether any
question repeats; and across exams, that the three selections are pairwise disjoint.

Questions are ordered round-robin by family within each area, the same ordering the coverage gate
uses, so a family holding k questions contributes its first to exam 1, its second to exam 2 and so
on rather than saturating one exam.

    python scripts/check_three_exam_construction.py
    python scripts/check_three_exam_construction.py --json audits/coverage/THREE-EXAM-CONSTRUCTION.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from prebatch3_final_coverage_gate import Bank, REQUIRED_AREA_ALLOCATION, MOCK_SIZE

TARGET_SETS = 3
FAMILY_REPEAT_CEILING = TARGET_SETS   # a family may not supply more than this many items to one exam


def ordered_pool(items: list[dict]) -> list[dict]:
    """Round-robin across families so no exam is family-saturated."""
    by_family: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        by_family[item["family_id"]].append(item)
    ordered: list[dict] = []
    rank = 0
    while len(ordered) < len(items):
        for family_id in sorted(by_family):
            bucket = by_family[family_id]
            if rank < len(bucket):
                ordered.append(bucket[rank])
        rank += 1
    return ordered


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    bank = Bank()
    by_area: dict[int, list[dict]] = defaultdict(list)
    for question_id in sorted(bank.questions):
        usable = bank.release_usable(question_id)
        if usable:
            by_area[usable["area"]].append(usable)

    print("release-usable by area:",
          {a: len(by_area.get(a, [])) for a in sorted(REQUIRED_AREA_ALLOCATION)})
    print("required for three exams:",
          {a: n * TARGET_SETS for a, n in sorted(REQUIRED_AREA_ALLOCATION.items())})
    print()

    used: set[str] = set()
    exams, failures = [], []
    for index in range(1, TARGET_SETS + 1):
        selection: dict[int, list[str]] = {}
        shortfalls: dict[int, int] = {}
        for area, required in sorted(REQUIRED_AREA_ALLOCATION.items()):
            pool = [q for q in ordered_pool(by_area.get(area, [])) if q["question_id"] not in used]
            chosen = [q["question_id"] for q in pool[:required]]
            if len(chosen) < required:
                shortfalls[area] = required - len(chosen)
            used.update(chosen)
            selection[area] = chosen

        picked = [q for area in sorted(selection) for q in selection[area]]
        families = Counter(bank.questions[q]["family_id"] for q in picked)
        worst_family, worst_count = (families.most_common(1) or [("", 0)])[0]
        exam = {
            "exam": index,
            "size": len(picked),
            "area_allocation": {str(a): len(v) for a, v in sorted(selection.items())},
            "shortfalls_by_area": {str(a): n for a, n in shortfalls.items()},
            "distinct_families": len(families),
            "max_family_repeat": worst_count,
            "heaviest_family": worst_family,
            "question_ids": picked,
        }
        exams.append(exam)

        if shortfalls:
            failures.append(f"exam {index} short by area {exam['shortfalls_by_area']}")
        if len(picked) != MOCK_SIZE:
            failures.append(f"exam {index} assembled {len(picked)} of {MOCK_SIZE}")
        if worst_count > FAMILY_REPEAT_CEILING:
            failures.append(f"exam {index} family {worst_family} supplies {worst_count} items "
                            f"(ceiling {FAMILY_REPEAT_CEILING})")

        print(f"exam {index}: {len(picked):>3} questions  areas "
              f"{exam['area_allocation']}  families {len(families)}  "
              f"heaviest {worst_count}x {worst_family or '-'}"
              + (f"  SHORT {exam['shortfalls_by_area']}" if shortfalls else ""))

    all_ids = [q for exam in exams for q in exam["question_ids"]]
    reuse = [q for q, n in Counter(all_ids).items() if n > 1]
    if reuse:
        failures.append(f"{len(reuse)} question(s) appear in more than one exam: {sorted(reuse)[:5]}")

    print()
    print(f"total distinct questions consumed: {len(set(all_ids))} of {len(all_ids)} drawn")
    print(f"pairwise disjoint: {not reuse}")

    report = {
        "check": "THREE_EXAM_CONSTRUCTION",
        "target_sets": TARGET_SETS,
        "per_exam_allocation": {str(a): n for a, n in sorted(REQUIRED_AREA_ALLOCATION.items())},
        "release_usable_by_area": {str(a): len(by_area.get(a, [])) for a in sorted(REQUIRED_AREA_ALLOCATION)},
        "exams": exams,
        "no_reuse_across_exams": not reuse,
        "failures": failures,
        "verdict": "PASS" if not failures else "FAIL",
    }
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {args.json}")

    print(f"\nVERDICT: {report['verdict']}")
    for failure in failures:
        print(f"  {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
