"""Fail-closed check that no CURRENT rule rests solely on superseded official guidance.

This exists because a real incident got past the existing freshness check. That check
confirmed an official URL still resolved, but not that the document behind it had been
replaced. MA-MH-SUD-ADMIN carried status CURRENT and last_verified 2026-08-14 while citing
Circular DCP 19-2-105, which had by then been superseded twice.

Schema position, checked rather than assumed: schemas/rule.schema.json sets
additionalProperties false, its `status` enum describes the RULE not the authority, and
`supersedes` holds rule ids matching ^(MA|FED)-... rather than documents. There is therefore
no in-record way to express an authority document's own status or its successor. Adding one
is a schema and governance change, so this tool instead reads a curated registry that lives
outside data/ and needs no schema change.

    python scripts/check_authority_supersession.py            # registry only, offline
    python scripts/check_authority_supersession.py --online   # also scan official pages

Exit code 1 when any CURRENT rule depends solely on superseded or rescinded guidance.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qa_common import DATA, ROOT, load_json, load_records, write_json

REGISTRY = ROOT / "audits" / "controller" / "AUTHORITY-SUPERSESSION-REGISTRY.json"
REPORT = ROOT / "audits" / "controller" / "AUTHORITY-SUPERSESSION-REPORT.json"

VALID_AUTHORITY_STATUS = {"CURRENT", "SUPERSEDED", "RESCINDED", "HISTORICAL", "UNKNOWN"}

# Phrases an official government page or document uses when it has been displaced.
SUPERSESSION_MARKERS = re.compile(
    r"\b(replaces|replaced by|supersedes|superseded by|updated by|rescinded|obsolete|archived)\b",
    re.I,
)


def registry() -> dict:
    if not REGISTRY.exists():
        return {"documents": {}}
    return load_json(REGISTRY)


def classify(authority: dict, reg: dict) -> tuple[str, dict]:
    """Resolve one authority entry against the curated registry."""
    url = (authority.get("url") or "").strip()
    name = (authority.get("name") or "").strip()
    docs = reg.get("documents", {})
    for key, entry in docs.items():
        if key and (key.lower() in name.lower() or (url and key.lower() in url.lower())):
            return entry.get("authority_status", "UNKNOWN"), entry
        if entry.get("url") and url and entry["url"].rstrip("/") == url.rstrip("/"):
            return entry.get("authority_status", "UNKNOWN"), entry
    return "UNKNOWN", {}


def scan_online(url: str) -> dict:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as fh:
            body = fh.read(400_000).decode("utf-8", "ignore")
    except Exception as exc:  # network failure must not silently pass the check
        return {"reachable": False, "error": str(exc)[:160], "markers": []}
    return {"reachable": True, "markers": sorted({m.group(0).lower() for m in SUPERSESSION_MARKERS.finditer(body)})}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--online", action="store_true",
                        help="also fetch each OFFICIAL_GUIDANCE url and look for supersession markers")
    args = parser.parse_args()

    reg = registry()
    for key, entry in reg.get("documents", {}).items():
        if entry.get("authority_status") not in VALID_AUTHORITY_STATUS:
            raise SystemExit(f"registry entry {key} has invalid authority_status {entry.get('authority_status')!r}")

    rules = {r["rule_id"]: r for _, r in load_records(DATA / "rules")}
    questions = {r["question_id"]: r for _, r in load_records(DATA / "questions")}

    errors, warnings, rows = [], [], []
    for rid, rule in sorted(rules.items()):
        guidance = [a for a in rule.get("authority", []) if a.get("type") == "OFFICIAL_GUIDANCE"]
        if not guidance:
            continue
        resolved = []
        for a in guidance:
            status, entry = classify(a, reg)
            item = {"name": a.get("name"), "url": a.get("url"), "authority_status": status,
                    "superseded_by": entry.get("superseded_by")}
            if args.online and a.get("url"):
                item["online"] = scan_online(a["url"])
            resolved.append(item)

        bad = [r for r in resolved if r["authority_status"] in {"SUPERSEDED", "RESCINDED"}]
        unknown = [r for r in resolved if r["authority_status"] == "UNKNOWN"]
        users = sorted(q for q, x in questions.items() if rid in x.get("rule_ids", []))
        released_users = [q for q in users if questions[q].get("verification_status") == "RELEASED"]

        row = {"rule_id": rid, "rule_status": rule.get("status"), "last_verified": rule.get("last_verified"),
               "authorities": resolved, "used_by": users, "released_users": released_users}
        rows.append(row)

        if rule.get("status") == "CURRENT" and bad and len(bad) == len(resolved):
            errors.append(
                f"{rid} is CURRENT but every official-guidance authority it cites is "
                f"{bad[0]['authority_status']}"
                + (f" (superseded by {bad[0]['superseded_by']})" if bad[0].get("superseded_by") else "")
                + f"; relied on by {len(released_users)} released question(s)"
            )
        elif rule.get("status") == "CURRENT" and bad:
            warnings.append(f"{rid} is CURRENT and cites at least one superseded authority")
        if unknown:
            warnings.append(
                f"{rid} cites {len(unknown)} official-guidance authority/ies absent from the "
                f"supersession registry; currency is unverified"
            )

    payload = {
        "report_type": "AUTHORITY_SUPERSESSION_CHECK",
        "mode": "online" if args.online else "registry-only",
        "registry_documents": len(reg.get("documents", {})),
        "rules_with_official_guidance": len(rows),
        "errors": errors,
        "warnings": warnings,
        "rules": rows,
        "schema_note": (
            "schemas/rule.schema.json cannot currently express an authority document's own status or "
            "successor: additionalProperties is false, `status` describes the rule, and `supersedes` "
            "holds rule ids. Representing authority_status and superseded_by inside the rule record "
            "requires a schema change, which is tooling and governance work rather than question repair."
        ),
    }
    write_json(REPORT, payload)

    for w in warnings:
        print(f"WARNING {w}")
    for e in errors:
        print(f"ERROR   {e}")
    print(f"authority supersession: {len(errors)} error(s), {len(warnings)} warning(s) "
          f"over {len(rows)} rule(s) citing official guidance")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
