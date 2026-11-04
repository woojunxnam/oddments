from __future__ import annotations

import re

from qa_common import (
    DATA,
    SCHEMAS,
    QAReport,
    find_placeholders,
    index_records,
    load_records,
    print_report,
    semantic_content_hash,
    validate_schema_records,
)


def _provision_key(section: str) -> str:
    """A normalised handle for the SECTION an authority URL points at.

    Subsections are dropped: a URL addresses the whole section page, so 24B1/2(b) and
    24B1/2(c)(5) should resolve to the same link and must be compared together.
    """
    trimmed = re.sub(r"\([^)]*\)", " ", section or "")
    trimmed = re.sub(r"[\s.,§]+", " ", trimmed).strip().lower()
    trimmed = re.sub(r"\bm g l\b", "mgl", trimmed)
    # Drop the bare section marker so "s. 21A" and "§ 21A" reach the same key.
    trimmed = re.sub(r"\bs\b", " ", trimmed)
    # Keep only the leading citation, so "18(d3/4), read with 18(d)" collapses to one key.
    return " ".join(trimmed.split()[:4])


def _url_identity(url: str) -> str:
    """What document a URL points at, ignoring which of two equivalent forms it uses.

    mass.gov publishes each CMR chapter twice: a landing page at
    /regulations/247-CMR-900-... and the PDF at /doc/247-cmr-9-.../download. Both resolve,
    so treating them as different targets would bury a genuinely broken link in stylistic
    noise. The regulations form spells the chapter with the trailing ".00" as two zeros.
    """
    lowered = (url or "").strip().lower()
    match = re.search(r"/(doc|regulations)/(\d{2,3})-cmr-(\d+)", lowered)
    if match:
        form, title, chapter = match.group(1), match.group(2), match.group(3)
        # Only the regulations form appends the ".00"; the doc form already carries the
        # plain chapter number, so stripping there would turn 700 into 7.
        if form == "regulations" and len(chapter) > 2 and chapter.endswith("00"):
            chapter = chapter[:-2]
        return f"massgov {title} cmr {chapter}"
    return lowered


def _report_url_divergence(records: list[tuple[object, dict]], report: QAReport) -> None:
    """Two rules citing the same provision must point at the same page.

    A URL that does not resolve looks identical to one that does: the check above only
    asks whether the field is present. Divergence is the signal available offline, and it
    is what a mistyped link actually looks like -- MA-CDTM-QUALIFICATIONS pointed at
    Section24B1~2 while five sibling rules pointed at Section24B%201~2, and only the
    siblings loaded.
    """
    urls_by_provision: dict[str, dict[str, list[str]]] = {}
    for _, rule in records:
        for authority in rule.get("authority", []):
            key = _provision_key(authority.get("section", ""))
            url = (authority.get("url") or "").strip()
            if not key or not url:
                continue
            urls_by_provision.setdefault(key, {}).setdefault(_url_identity(url), []).append(
                (rule["rule_id"], url)
            )
    for key, urls in sorted(urls_by_provision.items()):
        if len(urls) < 2:
            continue
        ranked = sorted(urls.items(), key=lambda item: (-len(item[1]), item[0]))
        _, majority = ranked[0]
        majority_url = majority[0][1]
        for _, entries in ranked[1:]:
            if len(entries) < len(majority):
                rule_ids = sorted({rule_id for rule_id, _ in entries})
                url = entries[0][1]
                report.warn(
                    f"authority URL divergence for {key!r}: {rule_ids} use {url} while "
                    f"{len(majority)} other rule(s) use {majority_url}"
                )


def validate_rules() -> tuple[QAReport, dict[str, dict]]:
    report = QAReport()
    records = load_records(DATA / "rules")
    validate_schema_records(records, SCHEMAS / "rule.schema.json", report)
    rules = index_records(records, "rule_id", report)
    _report_url_divergence(records, report)
    for path, rule in records:
        placeholders = find_placeholders(rule)
        if placeholders:
            report.error(f"{path}: literal placeholder(s): {sorted(set(placeholders))}")
        for authority in rule.get("authority", []):
            if not authority.get("url"):
                report.error(f"{path}: authority missing source URL")
            if not authority.get("section"):
                report.error(f"{path}: authority missing source section")
        if not rule.get("last_verified"):
            report.error(f"{path}: missing verification date")
        expected_hash = semantic_content_hash(rule, "rule")
        if rule.get("content_hash") != expected_hash:
            report.error(f"{path}: content_hash mismatch; run scripts/update_content_hashes.py")
        for related_id in rule.get("related_rule_ids", []):
            if related_id not in rules:
                report.error(f"{path}: unknown related_rule_id {related_id}")
        for superseded_id in rule.get("supersedes", []):
            if superseded_id not in rules:
                report.error(f"{path}: unknown supersedes rule_id {superseded_id}")
    return report, rules


def main() -> int:
    report, _ = validate_rules()
    return print_report("rules", report)


if __name__ == "__main__":
    raise SystemExit(main())
