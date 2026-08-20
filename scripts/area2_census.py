"""Area-2 capacity census: machine-derived accounting over the family records.

Issue #91 needs 66 new Area-2 questions split into two locked tranches, so a pooled count is
not sufficient. B3-C and B3-D each need 33, and one family may fill only one slot.

Every summary number here is recomputed from the `families` records on each run. Nothing is
typed by hand. If a narrative and this summary disagree, this summary wins.

    python scripts/area2_census.py --recompute
    python scripts/area2_census.py --add path/to/new_records.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, ROOT, load_json, load_records, write_json

CENSUS_PATH = ROOT / "audits" / "controller" / "AREA2-SOURCE-CENSUS.json"

TRANCHE_TARGET = 33
TOTAL_TARGET = 66
VALID_TRANCHES = {"B3C", "B3D", "EITHER"}
VALID_VIABILITY = {"YES", "NO", "UNRESOLVED"}

REQUIRED_FIELDS = [
    "source", "official_url", "exact_section", "operative_proposition", "actor", "trigger",
    "professional_decision", "conditions", "exceptions", "tranche", "theme", "why_area_2",
    "closest_question_ids", "closest_family_ids", "same_proposition_already_keyed",
    "same_discrimination_already_tested", "proposed_family_id", "family_novelty",
    "scenario_sketch", "viability",
]


def validate(records: list) -> list:
    problems = []
    seen_family, seen_prop = {}, {}
    for i, r in enumerate(records):
        tag = r.get("proposed_family_id") or f"record[{i}]"
        for f in REQUIRED_FIELDS:
            if f not in r:
                problems.append(f"{tag}: missing field {f}")
        if r.get("viability") not in VALID_VIABILITY:
            problems.append(f"{tag}: viability {r.get('viability')!r} not in {sorted(VALID_VIABILITY)}")
        if r.get("tranche") not in VALID_TRANCHES:
            problems.append(f"{tag}: tranche {r.get('tranche')!r} not in {sorted(VALID_TRANCHES)}")
        if r.get("viability") == "NO" and not r.get("rejection_reason"):
            problems.append(f"{tag}: viability NO requires rejection_reason")
        if r.get("viability") == "YES":
            if r.get("same_proposition_already_keyed") is True:
                problems.append(f"{tag}: cannot be YES while the same proposition is already keyed")
            if r.get("same_discrimination_already_tested") is True:
                problems.append(f"{tag}: cannot be YES while the same discrimination is already tested")
        fid = r.get("proposed_family_id")
        if fid:
            if fid in seen_family:
                problems.append(f"{tag}: duplicate proposed_family_id, first seen at {seen_family[fid]}")
            seen_family[fid] = tag
        # a proposition may be reused across records only if the tested decision differs
        key = (r.get("exact_section"), (r.get("operative_proposition") or "")[:160])
        if r.get("viability") == "YES":
            if key in seen_prop and r.get("professional_decision") == seen_prop[key]:
                problems.append(f"{tag}: identical proposition AND identical professional decision as an earlier YES record")
            seen_prop[key] = r.get("professional_decision")
    return problems


def summarize(records: list) -> dict:
    yes = [r for r in records if r.get("viability") == "YES"]
    no = [r for r in records if r.get("viability") == "NO"]
    unresolved = [r for r in records if r.get("viability") == "UNRESOLVED"]

    b3c_only = [r for r in yes if r["tranche"] == "B3C"]
    b3d_only = [r for r in yes if r["tranche"] == "B3D"]
    either = [r for r in yes if r["tranche"] == "EITHER"]

    need_c = max(0, TRANCHE_TARGET - len(b3c_only))
    need_d = max(0, TRANCHE_TARGET - len(b3d_only))
    either_needed = need_c + need_d
    feasible = either_needed <= len(either) and len(yes) >= TOTAL_TARGET

    # A feasible allocation assigns EITHER families to whichever tranche still needs them.
    alloc_c = min(len(either), need_c)
    alloc_d = min(len(either) - alloc_c, need_d)
    guaranteed_c = len(b3c_only) + alloc_c
    guaranteed_d = len(b3d_only) + alloc_d

    by_source = defaultdict(lambda: {"YES": 0, "NO": 0, "UNRESOLVED": 0})
    by_theme = defaultdict(lambda: {"YES": 0, "NO": 0, "UNRESOLVED": 0})
    for r in records:
        by_source[r.get("source", "<unknown>")][r.get("viability", "UNRESOLVED")] += 1
        by_theme[r.get("theme", "<unassigned>")][r.get("viability", "UNRESOLVED")] += 1

    # Concentration warning gate: is one source starting to dominate the viable pool?
    src_yes = Counter(r.get("source", "<unknown>") for r in yes)
    top_source, top_count = (src_yes.most_common(1)[0] if src_yes else ("<none>", 0))
    concentration = round(top_count / len(yes), 3) if yes else 0.0

    rejection_reasons = Counter(
        (r.get("rejection_category") or (r.get("rejection_reason") or "<unspecified>")[:70]) for r in no
    )

    return {
        "targets": {"per_tranche": TRANCHE_TARGET, "total": TOTAL_TARGET},
        "raw_candidates_reviewed": len(records),
        "viable_yes": len(yes),
        "rejected_no": len(no),
        "unresolved": len(unresolved),
        "b3c_only_families": len(b3c_only),
        "b3d_only_families": len(b3d_only),
        "either_unassigned_capacity": len(either),
        "guaranteed_b3c_capacity": guaranteed_c,
        "guaranteed_b3d_capacity": guaranteed_d,
        "total_nonoverlapping_guaranteed_capacity": guaranteed_c + guaranteed_d,
        "b3c_shortfall": max(0, TRANCHE_TARGET - guaranteed_c),
        "b3d_shortfall": max(0, TRANCHE_TARGET - guaranteed_d),
        "either_families_needed_for_feasibility": either_needed,
        "either_families_available": len(either),
        "allocation_feasible": bool(feasible),
        "decision_gate": (
            "CASE A - capacity proven" if feasible else
            ("CASE B - pooled total reached but theme allocation fails"
             if len(yes) >= TOTAL_TARGET else
             "CASE C - fewer than 66 defensible new families so far (census incomplete)")
        ),
        "by_source": {k: dict(v) for k, v in sorted(by_source.items())},
        "by_theme": {k: dict(v) for k, v in sorted(by_theme.items())},
        "concentration": {
            "top_source": top_source,
            "top_source_viable_families": top_count,
            "share_of_viable_pool": concentration,
            "warning_gate": (
                "REVIEW REQUIRED - one source exceeds 40% of the viable pool; prove each further "
                "family from it tests a different professional decision"
                if concentration > 0.40 and top_count >= 5 else "ok"
            ),
        },
        "rejection_reasons": dict(rejection_reasons),
    }


def bank_context() -> dict:
    questions = {r["question_id"]: r for _, r in load_records(DATA / "questions")}
    area2 = [q for q in questions.values() if q["area"] == 2]
    matrix = load_json(DATA / "exam_style" / "question_family_matrix.json")
    fams = {f["family_id"]: f for f in matrix["families"]}
    released = Counter(q.get("family_id") for q in questions.values()
                       if q.get("verification_status") == "RELEASED")
    saturated = sorted({q["family_id"] for q in area2
                        if released.get(q["family_id"], 0)
                        >= fams.get(q["family_id"], {}).get("max_questions_in_final_bank", 2)})
    return {
        "comparator_main": "506c3d9a95d90d44c35d01487cc7ec4eb9d98d43",
        "bank_size": len(questions),
        "released": sum(1 for q in questions.values() if q.get("verification_status") == "RELEASED"),
        "area_2_present": len(area2),
        "area_2_target": 120,
        "area_2_deficit": 120 - len(area2),
        "area_2_distinct_families": len({q["family_id"] for q in area2}),
        "area_2_saturated_families": saturated,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--add", help="JSON file holding a list of new family records")
    parser.add_argument("--recompute", action="store_true")
    args = parser.parse_args()

    census = load_json(CENSUS_PATH) if CENSUS_PATH.exists() else {"report_type": "AREA2_SOURCE_CENSUS"}
    records = census.get("families") or []

    # one-time migration from the earlier "paths" key
    if not records and census.get("paths"):
        migrated = []
        for p in census["paths"]:
            migrated.append({
                "source": p.get("source"), "official_url": p.get("official_url"),
                "exact_section": p.get("exact_section"),
                "operative_proposition": p.get("verbatim_operative_proposition"),
                "actor": p.get("actor"), "trigger": p.get("trigger"),
                "professional_decision": p.get("pharmacist_decision_or_action"),
                "conditions": p.get("conditions"), "exceptions": p.get("exceptions"),
                "tranche": p.get("tranche", "EITHER"), "theme": p.get("theme", "<unassigned>"),
                "why_area_2": p.get("why_area_2"),
                "closest_question_ids": p.get("existing_closest_bank_ids", []),
                "closest_family_ids": p.get("closest_family_ids", []),
                "same_proposition_already_keyed": p.get("same_paragraph_already_keyed_elsewhere", False),
                "same_discrimination_already_tested": False,
                "proposed_family_id": p.get("proposed_distinct_decision_family"),
                "family_novelty": p.get("family_novelty", ""),
                "scenario_sketch": p.get("scenario_sketch", ""),
                "viability": p.get("viability"),
                "rejection_reason": p.get("rejection_reason"),
            })
        records = migrated
        census.pop("paths", None)
        print(f"migrated {len(records)} legacy path records into the families schema")

    if args.add:
        new = json.loads(Path(args.add).read_text(encoding="utf-8"))
        known = {r.get("proposed_family_id") for r in records}
        added = [r for r in new if r.get("proposed_family_id") not in known]
        records.extend(added)
        print(f"added {len(added)} of {len(new)} submitted records ({len(new) - len(added)} already present)")

    problems = validate(records)
    census["families"] = records
    census["bank_context"] = bank_context()
    census["summary"] = summarize(records)
    census["record_integrity"] = {"problems": problems, "clean": not problems}
    write_json(CENSUS_PATH, census)

    s = census["summary"]
    print()
    print(f"records reviewed      : {s['raw_candidates_reviewed']}")
    print(f"  viable YES          : {s['viable_yes']}")
    print(f"  rejected NO         : {s['rejected_no']}")
    print(f"  unresolved          : {s['unresolved']}")
    print(f"B3C-only families     : {s['b3c_only_families']}")
    print(f"B3D-only families     : {s['b3d_only_families']}")
    print(f"EITHER families       : {s['either_unassigned_capacity']}")
    print(f"guaranteed B3C        : {s['guaranteed_b3c_capacity']} / {TRANCHE_TARGET}   shortfall {s['b3c_shortfall']}")
    print(f"guaranteed B3D        : {s['guaranteed_b3d_capacity']} / {TRANCHE_TARGET}   shortfall {s['b3d_shortfall']}")
    print(f"total non-overlapping : {s['total_nonoverlapping_guaranteed_capacity']} / {TOTAL_TARGET}")
    print(f"concentration         : {s['concentration']['top_source_viable_families']} from "
          f"{s['concentration']['top_source'][:60]} ({s['concentration']['share_of_viable_pool']}) "
          f"-> {s['concentration']['warning_gate']}")
    print(f"DECISION GATE         : {s['decision_gate']}")
    if problems:
        print()
        print("RECORD INTEGRITY PROBLEMS:")
        for p in problems:
            print("  -", p)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
