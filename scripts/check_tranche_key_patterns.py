"""Detect key patterns that are invisible bank-wide but present inside one authoring tranche.

CLAUDE-FRESH-B3C raised a tranche-level finding no existing gate could see: inside tranche B3-C one
option letter carried a correct answer in 11 of 12 SATA items, and not one SATA item had three
correct options although three is the released bank's modal count. The existing detectors measure the
WHOLE pool, where a thirty-question tranche cannot move the share far enough to trip a threshold.

The two patterns do NOT carry the same risk, and this check does not pretend otherwise.

  site/shuffle.js re-letters every item at render time (shuffleQuestionChoices, seeded per
  question_id), so which STORED letter holds a correct answer is decoupled from what the candidate
  sees. A stored-slot bias is therefore invisible during an exam and is reported here as a warning:
  it is bank hygiene for anyone reading site/generated/questions.json directly, not an exam defect.

  The same function maps correct_choice_ids one-for-one, so HOW MANY options are correct is
  unchanged by shuffling. A candidate who learns that SATA items are never three-correct gains real
  information. Correct-count patterns are therefore errors.

Because tranche boundaries are an authoring artifact — build_mock orders each area round-robin by
family, not by tranche — the count check that governs release is the one over the pool a candidate
actually faces. Per-tranche count omission is reported as an error anyway, because it is the earliest
signal that an authoring pass has drifted, and it is cheap to correct before a tranche is audited.

    python scripts/check_tranche_key_patterns.py
    python scripts/check_tranche_key_patterns.py --range 328 360 --label B3-D
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, load_records

SLOT_PRESENCE_MAX = 0.80        # warn: no letter should carry a correct answer in >80% of a tranche's SATA
SBA_KEY_SHARE_MAX = 0.50        # warn: no letter should be the SBA key in >50% of a tranche
MATERIAL_COUNT_SHARE = 0.25     # a correct-count holding this share of the bank must not be wholly absent
MIN_SATA_TO_JUDGE = 6           # below this the shares carry no signal

TRANCHES = [
    ("B3-A", 229, 261), ("B3-B", 262, 294), ("B3-C", 295, 327),
    ("B3-D", 328, 360), ("B3-E", 361, 390),
]


def material_counts(questions: dict) -> dict[int, float]:
    """Correct-counts that make up a material share of the whole SATA pool."""
    sata = [q for q in questions.values() if q["question_type"] == "SATA"]
    tally = Counter(len(q["correct_choice_ids"]) for q in sata)
    return {n: c / len(sata) for n, c in tally.items() if c / len(sata) >= MATERIAL_COUNT_SHARE}


def analyse(label: str, questions: list[dict], material: dict[int, float]) -> dict:
    sata = [q for q in questions if q["question_type"] == "SATA"]
    sba = [q for q in questions if q["question_type"] == "SBA"]
    errors, warnings = [], []

    slot, counts = {}, Counter(len(q["correct_choice_ids"]) for q in sata)
    if len(sata) >= MIN_SATA_TO_JUDGE:
        slot = {ch: sum(1 for q in sata if ch in q["correct_choice_ids"]) / len(sata) for ch in "ABCDE"}
        worst = max(slot, key=slot.get)
        if slot[worst] > SLOT_PRESENCE_MAX:
            warnings.append({
                "code": "TRANCHE_SATA_SLOT_CONCENTRATION",
                "detail": f"option {worst} carries a correct answer in {slot[worst]:.0%} of this "
                          f"tranche's SATA items (threshold {SLOT_PRESENCE_MAX:.0%})",
                "exam_visible": False,
                "reason_not_error": "site/shuffle.js re-letters each item, so stored slot is not what a candidate sees",
            })

        for n, share in sorted(material.items()):
            if counts.get(n, 0) == 0:
                errors.append({
                    "code": "TRANCHE_SATA_COUNT_OMISSION",
                    "detail": f"no {n}-correct SATA item in this tranche, though {n}-correct is "
                              f"{share:.0%} of the bank's SATA; observed {dict(sorted(counts.items()))}",
                    "exam_visible": True,
                    "reason_error": "shuffling preserves how many options are correct",
                })

    keys = {}
    if sba:
        tally = Counter(q["correct_choice_ids"][0] for q in sba)
        keys = {ch: tally.get(ch, 0) / len(sba) for ch in "ABCDE"}
        worst = max(keys, key=keys.get)
        if keys[worst] > SBA_KEY_SHARE_MAX:
            warnings.append({
                "code": "TRANCHE_SBA_KEY_CONCENTRATION",
                "detail": f"option {worst} is the key in {keys[worst]:.0%} of this tranche's SBA "
                          f"items (threshold {SBA_KEY_SHARE_MAX:.0%})",
                "exam_visible": False,
                "reason_not_error": "site/shuffle.js re-letters each item, so stored slot is not what a candidate sees",
            })

    return {
        "tranche": label, "questions": len(questions), "sata": len(sata), "sba": len(sba),
        "sata_slot_presence": {k: round(v, 3) for k, v in slot.items()},
        "sata_correct_counts": dict(sorted(counts.items())),
        "sba_key_share": {k: round(v, 3) for k, v in keys.items()},
        "errors": errors, "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--range", nargs=2, type=int, metavar=("FIRST", "LAST"))
    parser.add_argument("--label", default="AD-HOC")
    parser.add_argument("--json", type=Path, help="also write the full report here")
    args = parser.parse_args()

    questions = {r["question_id"]: r for _, r in load_records(DATA / "questions")}
    material = material_counts(questions)
    print(f"material SATA correct-counts bank-wide: "
          f"{ {n: f'{s:.0%}' for n, s in sorted(material.items())} }\n")

    groups = [(args.label, args.range[0], args.range[1])] if args.range else TRANCHES
    reports, errors = [], 0
    for label, first, last in groups:
        selected = [questions[f"MA-Q-{n:04d}"] for n in range(first, last + 1)
                    if f"MA-Q-{n:04d}" in questions]
        if not selected:
            continue
        report = analyse(label, selected, material)
        reports.append(report)
        errors += len(report["errors"])
        status = "FAIL" if report["errors"] else ("WARN" if report["warnings"] else "PASS")
        slots = "  ".join(f"{k}:{v:.0%}" for k, v in report["sata_slot_presence"].items())
        print(f"{label:<7} {status}  n={report['questions']:>3} SATA={report['sata']:>3}  "
              f"[{slots}]  counts={report['sata_correct_counts']}")
        for item in report["errors"]:
            print(f"        ERROR {item['code']}: {item['detail']}")
        for item in report["warnings"]:
            print(f"        warn  {item['code']}: {item['detail']}")

    if args.json:
        args.json.write_text(json.dumps({"material_counts": material, "tranches": reports},
                                        indent=2) + "\n", encoding="utf-8")
        print(f"\nwrote {args.json}")
    print(f"\n{errors} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
