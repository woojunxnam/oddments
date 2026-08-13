from __future__ import annotations

import json
import hashlib
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SCHEMAS = ROOT / "schemas"
PLACEHOLDER_PATTERNS = (
    re.compile(r"\{[^{}]+\}"),
    re.compile(r"\b(?:TODO|TBD|FIXME)\b", re.IGNORECASE),
    re.compile(r"\{drug_ref", re.IGNORECASE),
    re.compile(r"\{d\.", re.IGNORECASE),
)
ABSOLUTE_WORDS = re.compile(r"\b(?:always|never|only|all|none)\b", re.IGNORECASE)
HEDGE_WORDS = re.compile(
    r"\b(?:generally|may|might|typically|ordinarily|unless|if|when|can)\b",
    re.IGNORECASE,
)
BLOCKED_RULE_STATUSES = {"DRAFT", "SUPERSEDED", "TEMPORARY", "UNCLEAR"}
VERIFIED_RULE_STATUSES = {"PRIMARY_VERIFIED", "OFFICIAL_POLICY_VERIFIED"}
VERIFIED_DRUG_STATUSES = {"PRIMARY_VERIFIED", "OFFICIAL_POLICY_VERIFIED"}

SEMANTIC_FIELDS = {
    "rule": (
        "rule_id",
        "title",
        "jurisdiction",
        "area",
        "topic",
        "subtopic",
        "rule_summary",
        "exam_relevance",
        "authority",
        "status",
        "effective_date",
        "supersedes",
        "numeric_facts",
        "exceptions",
        "common_confusions",
        "related_rule_ids",
        "verification_status",
    ),
    "drug": (
        "drug_id",
        "generic_name",
        "brand_names",
        "main_indications",
        "therapeutic_class",
        "federal_status",
        "massachusetts_status",
        "legal_consequences",
        "authorities",
        "verified_rule_dependencies",
        "verification_status",
    ),
}

QUESTION_AUDIT_FIELDS = (
    "question_id",
    "family_id",
    "area",
    "topic",
    "subtopic",
    "difficulty",
    "question_type",
    "provenance",
    "source_signal_ids",
    "stem",
    "choices",
    "correct_choice_ids",
    "explanation",
    "rule_ids",
    "drug_ids",
    "reasoning_steps",
)


@dataclass
class QAReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def extend(self, other: "QAReport") -> None:
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)

    @property
    def ok(self) -> bool:
        return not self.errors


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _canonicalize(value: Any, *, sort_lists: bool) -> Any:
    if isinstance(value, str):
        return " ".join(value.split())
    if isinstance(value, dict):
        return {key: _canonicalize(value[key], sort_lists=sort_lists) for key in sorted(value)}
    if isinstance(value, list):
        normalized = [_canonicalize(item, sort_lists=sort_lists) for item in value]
        if sort_lists:
            return sorted(
                normalized,
                key=lambda item: json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
            )
        return normalized
    return value


def deterministic_hash(value: Any, *, sort_lists: bool = False) -> str:
    canonical = _canonicalize(value, sort_lists=sort_lists)
    encoded = json.dumps(canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def semantic_content_hash(record: dict[str, Any], record_type: str) -> str:
    fields = SEMANTIC_FIELDS[record_type]
    semantic = {field: record.get(field) for field in fields}
    return deterministic_hash(semantic, sort_lists=True)


def dependency_snapshot(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "content_version": record.get("content_version"),
        "content_hash": record.get("content_hash"),
    }


def question_audit_hash(question: dict[str, Any]) -> str:
    content = {field: question.get(field) for field in QUESTION_AUDIT_FIELDS}
    return deterministic_hash(content)


def drug_consequence_rule_ids(drug: dict[str, Any]) -> set[str]:
    rule_ids: set[str] = set()
    for consequence in drug.get("legal_consequences", {}).values():
        if isinstance(consequence, dict):
            rule_ids.update(consequence.get("rule_ids", []))
    return rule_ids


def iter_json_files(directory: Path) -> list[Path]:
    return sorted(path for path in directory.glob("*.json") if path.is_file())


def load_records(directory: Path) -> list[tuple[Path, dict[str, Any]]]:
    return [(path, load_json(path)) for path in iter_json_files(directory)]


def index_records(
    records: Iterable[tuple[Path, dict[str, Any]]],
    id_field: str,
    report: QAReport,
) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    owners: dict[str, Path] = {}
    for path, record in records:
        record_id = record.get(id_field)
        if not record_id:
            report.error(f"{path}: missing {id_field}")
            continue
        if record_id in index:
            report.error(f"duplicate {id_field} {record_id}: {owners[record_id]} and {path}")
            continue
        index[record_id] = record
        owners[record_id] = path
    return index


def validate_schema_records(
    records: Iterable[tuple[Path, dict[str, Any]]],
    schema_path: Path,
    report: QAReport,
) -> None:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for path, record in records:
        for error in sorted(validator.iter_errors(record), key=lambda item: list(item.absolute_path)):
            location = ".".join(str(part) for part in error.absolute_path) or "<root>"
            report.error(f"{path}:{location}: {error.message}")


def text_values(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from text_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from text_values(child)


def find_placeholders(value: Any) -> list[str]:
    matches: list[str] = []
    for text in text_values(value):
        for pattern in PLACEHOLDER_PATTERNS:
            matches.extend(match.group(0) for match in pattern.finditer(text))
    return matches


def normalize_text(text: str, normalize_numbers: bool = False) -> str:
    normalized = text.casefold()
    if normalize_numbers:
        normalized = re.sub(r"\b\d+(?:\.\d+)?\b", "<num>", normalized)
    normalized = re.sub(r"[^a-z0-9<>]+", " ", normalized)
    return " ".join(normalized.split())


def token_jaccard(left: str, right: str) -> float:
    left_tokens = set(normalize_text(left, normalize_numbers=True).split())
    right_tokens = set(normalize_text(right, normalize_numbers=True).split())
    if not left_tokens and not right_tokens:
        return 1.0
    return len(left_tokens & right_tokens) / max(1, len(left_tokens | right_tokens))


def chi_square_uniform(counts: dict[str, int]) -> tuple[float, int, float]:
    total = sum(counts.values())
    categories = [key for key, value in counts.items() if value or key in "ABCDE"]
    categories = sorted(set(categories))
    if total == 0 or len(categories) < 2:
        return 0.0, 0, 1.0
    expected = total / len(categories)
    chi_square = sum((counts.get(category, 0) - expected) ** 2 / expected for category in categories)
    degrees = len(categories) - 1
    # Wilson-Hilferty normal approximation avoids a SciPy dependency.
    if degrees <= 0:
        return chi_square, degrees, 1.0
    z_value = ((chi_square / degrees) ** (1 / 3) - (1 - 2 / (9 * degrees))) / math.sqrt(2 / (9 * degrees))
    p_value = 0.5 * math.erfc(z_value / math.sqrt(2))
    return chi_square, degrees, min(1.0, max(0.0, p_value))


def print_report(label: str, report: QAReport) -> int:
    for warning in report.warnings:
        print(f"WARNING [{label}] {warning}")
    for error in report.errors:
        print(f"ERROR [{label}] {error}")
    print(f"{label}: {len(report.errors)} error(s), {len(report.warnings)} warning(s)")
    return 0 if report.ok else 1
