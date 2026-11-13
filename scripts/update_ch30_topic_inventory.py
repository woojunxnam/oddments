#!/usr/bin/env python3
"""Build/validate Chapter 30's fast Area+topic count ledger.

Usage:
  python scripts/update_ch30_topic_inventory.py --write
  python scripts/update_ch30_topic_inventory.py --check

Only the small inventory JSON is rewritten. The canonical questions and
all previous question IDs, stems and answers remain unchanged.
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "site" / "mpje-side-notes" / "exam-simulation-30"
QUESTION_FILE = DIR / "questions.js"
CATALOG_FILE = DIR / "topic-catalog.json"
INVENTORY_FILE = DIR / "topic-inventory.json"


def read_questions():
    text = QUESTION_FILE.read_text(encoding="utf-8")
    match = re.search(
        r"window\.MPJE_CH30_QUESTIONS\s*=\s*(\[[\s\S]*\]);\s*$", text
    )
    if not match:
        raise ValueError("Cannot locate canonical MPJE_CH30_QUESTIONS JSON data")
    questions = json.loads(match.group(1))
    if not isinstance(questions, list):
        raise ValueError("Questions must be a JSON array")
    return questions


def build():
    questions = read_questions()
    catalog = json.loads(CATALOG_FILE.read_text(encoding="utf-8"))
    entries = catalog["topics"]
    definitions = {row["key"]: row for row in entries}
    if len(entries) != len(definitions):
        raise ValueError("Duplicate keys in topic catalog")

    ids = set()
    stems = set()
    topic_ids = defaultdict(list)
    area_counts = Counter()
    question_metadata = []
    for q in questions:
        qid = q["id"]
        stem = " ".join(q["stem"].lower().split())
        if qid in ids or stem in stems:
            raise ValueError(f"Duplicate ID or stem: {qid}")
        ids.add(qid)
        stems.add(stem)
        topic = q.get("topicKey")
        if topic not in definitions:
            raise ValueError(f"Question {qid} has unknown/missing topicKey: {topic}")
        area = int(q["area"])
        if area != int(definitions[topic]["area"]):
            raise ValueError(f"Question {qid} Area {area} mismatches topic {topic}")
        if area not in (1, 2, 3, 4):
            raise ValueError(f"Unrecognized NABP Area: {area}")
        if len(q["choices"]) != 4 or not q["correct"]:
            raise ValueError(f"Invalid answer structure: {qid}")
        topic_ids[topic].append(qid)
        area_counts[str(area)] += 1
        question_metadata.append({
            "id": qid, "set": q["set"], "area": area, "topic_key": topic
        })

    topic_rows = []
    for row in entries:
        key = row["key"]
        topic_rows.append({
            "key": key, "area": row["area"], "label": row["label"],
            "priority": row["priority"], "count": len(topic_ids[key]),
            "question_ids": topic_ids[key],
        })
    next_candidates = {}
    for area in (1, 2, 3, 4):
        ordered = sorted(
            (row for row in topic_rows if row["area"] == area),
            key=lambda row: (row["priority"] != "high", row["count"], row["key"]),
        )
        next_candidates[str(area)] = [
            {"topic_key": row["key"], "count": row["count"],
             "priority": row["priority"]} for row in ordered[:3]
        ]

    inventory = {
        "schema_version": 1,
        "blueprint": catalog["blueprint"],
        "question_count": len(questions),
        "area_counts": {
            str(a): area_counts[str(a)] for a in (1, 2, 3, 4)
        },
        "topic_counts": topic_rows,
        "question_topics": question_metadata,
        "next_candidate_topics": next_candidates,
        "new_five_area_quota": {"1": 1, "2": 2, "3": 1, "4": 1},
        "random_ten_area_quota": {"1": 2, "2": 3, "3": 3, "4": 2},
        "priority_note": catalog["priority_note"],
    }
    return json.dumps(inventory, ensure_ascii=False, indent=2) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="Regenerate inventory")
    mode.add_argument("--check", action="store_true", help="Fail if inventory is stale")
    args = parser.parse_args()
    try:
        result = build()
        if args.write:
            INVENTORY_FILE.write_text(result, encoding="utf-8")
            print(f"Wrote {INVENTORY_FILE.relative_to(ROOT)}")
        elif not INVENTORY_FILE.exists() or INVENTORY_FILE.read_text(encoding="utf-8") != result:
            raise ValueError(
                "Chapter 30 topic inventory is stale; "
                "run python scripts/update_ch30_topic_inventory.py --write"
            )
        else:
            print("Chapter 30 topic inventory: PASS")
    except (KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"Chapter 30 topic inventory: FAIL — {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
