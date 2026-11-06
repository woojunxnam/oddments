#!/usr/bin/env python3
"""Read-only concept-overlap screen for private Next40 author drafts.

The probes describe legal decisions, not private question/answer content. Results
are CANDIDATES FOR HUMAN REVIEW, never authoritative duplicate CLEAR flags.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

PROBES = {
    "IMG_0005_nonsterile_area": (
        (r"non[\s-]?sterile|nonsterile", 3),
        (r"compound(?:ing|ed|s)?", 2),
        (r"designat(?:ed|ion)|separat(?:e|ion)|dedicat(?:ed|ion)", 3),
        (r"counter|work\s?area|preparation area", 2),
        (r"cross.contaminat|facility requirement|compounding area", 3),
    ),
    "IMG_0008_referral_payment": (
        (r"anti[\s-]?kickback|kickback|remuneration", 4),
        (r"referr(?:al|ed|ing)?|induc(?:e|ing|ement)", 3),
        (r"nursing.home|health.care.facility|administrator", 2),
        (r"medicare|federal.health.care.program", 2),
        (r"payment|compensation|fee|commission|value", 1),
    ),
    "IMG_0040_civil_subpoena": (
        (r"subpoena|discovery request|court.order", 4),
        (r"hipaa|protected.health.information|privacy.rule|phi", 2),
        (r"protective.order|notice.to.the.patient|satisfactory.assurance", 4),
        (r"civil.lawsuit|attorney|litigation|judicial.proceeding", 2),
        (r"disclos(?:e|ure)|patient.record|authorization", 1),
    ),
    "IMG_0131_therapeutic_interchange": (
        (r"lisinopril|losartan", 4),
        (r"therapeutic.interchange|different.active.ingredient", 4),
        (r"interchangeab(?:le|ility)|generic.substitut|drug.substitut", 3),
        (r"formulary|insurance|payer|preferred.alternative", 2),
        (r"prescriber.authorization|prescriber.approval|collaborative.drug.therapy", 3),
    ),
}


def corpus_paths(root: Path) -> list[Path]:
    paths = set(root.glob("practice_expansion/**/questions.json"))
    paths.update(root.glob("data/questions/ma-q-*.json"))
    draft = root / "site/draft-practice/questions.json"
    if draft.is_file():
        paths.add(draft)
    return sorted(path for path in paths if path.is_file())


def question_records(path: Path) -> list[dict]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        rows = raw
    elif isinstance(raw, dict) and isinstance(raw.get("questions"), list):
        rows = raw["questions"]
    elif isinstance(raw, dict) and isinstance(raw.get("items"), list):
        rows = raw["items"]
    elif isinstance(raw, dict):
        rows = [raw] if ("stem" in raw or "question" in raw) else []
    else:
        rows = []
    return [row for row in rows if isinstance(row, dict)]


def searchable_text(row: dict) -> str:
    parts = [row.get(field, "") for field in (
        "stem", "scenario", "lead_in", "question", "question_text", "topic", "title"
    )]
    for c in row.get("choices", []):
        if isinstance(c, dict):
            parts.append(c.get("text", ""))
        elif isinstance(c, str):
            parts.append(c)
    parts = [part for part in parts if isinstance(part, str)]
    return " ".join(parts).lower()


def overlaps(row: dict, probe: tuple) -> tuple[int, int, list[str]]:
    text = searchable_text(row)
    hits = [(pattern, weight) for pattern, weight in probe if re.search(pattern, text, re.I)]
    return len(hits), sum(weight for _, weight in hits), [p for p, _ in hits]


def screen(root: Path, *, limit: int = 12) -> dict:
    paths = corpus_paths(root)
    if not paths:
        raise FileNotFoundError("No supported repository question JSON sources found")
    sources = {}
    candidates = {name: [] for name in PROBES}
    for path in paths:
        rel = path.relative_to(root).as_posix()
        rows = question_records(path)
        sources[rel] = len(rows)
        for pos, row in enumerate(rows):
            text = searchable_text(row)
            if not text:
                continue
            ident = str(row.get("question_id") or row.get("id") or f"row:{pos + 1}")
            for name, probe in PROBES.items():
                hit_count, score, patterns = overlaps(row, probe)
                if hit_count < 2:
                    continue
                candidates[name].append({
                    "id": ident, "source": rel, "score": score,
                    "matched_concepts": hit_count,
                    "snippet": re.sub(r"\s+", " ", text[:230]).strip(),
                })
    result = {
        "screen_type": "concept_overlap_not_exact_or_semantic_clearance",
        "scope": "public repository question JSON files only",
        "file_count": len(paths),
        "source_counts": sources,
        "total_record_occurrences": sum(sources.values()),
        "probes": {},
        "duplicate_review_status": "NOT_CLEAR_NEEDS_HUMAN_FULL_TEXT_COMPARISON",
    }
    for name, matches in candidates.items():
        matches.sort(key=lambda v: (-v["score"], -v["matched_concepts"], v["id"], v["source"]))
        result["probes"][name] = {
            "candidate_occurrences": len(matches),
            "top": matches[:limit],
        }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--limit", type=int, default=12)
    args = parser.parse_args()
    result = screen(args.root.resolve(), limit=args.limit)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"SCOPE: {result['file_count']} JSON files / {result['total_record_occurrences']} records (includes repeated variants)")
    for source, count in result["source_counts"].items():
        print(f"SOURCE: {source}: {count}")
    for name, section in result["probes"].items():
        print(f"\nPROBE: {name}; possible overlaps: {section['candidate_occurrences']}")
        for item in section["top"]:
            print(f"  {item['score']:02d} {item['id']} [{item['source']}] {item['snippet'][:175]}")
    print("STATUS: NOT_CLEAR — lexical concept screening does not prove independent legal or duplicate audit")


if __name__ == "__main__":
    main()
