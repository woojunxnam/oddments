from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


def test_all_canonical_records_validate_against_schemas(root: Path) -> None:
    registries = {
        "rules": "rule.schema.json",
        "drugs": "drug.schema.json",
        "questions": "question.schema.json",
    }
    errors = []
    for registry, schema_name in registries.items():
        schema = json.loads((root / "schemas" / schema_name).read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        for path in sorted((root / "data" / registry).glob("*.json")):
            record = json.loads(path.read_text(encoding="utf-8"))
            for error in validator.iter_errors(record):
                errors.append(f"{path}: {error.message}")
    assert errors == []


def test_valid_question_fixture_passes_registry_validation(tmp_path, monkeypatch, canonical_question, registry_indexes) -> None:
    import validate_questions as module
    from conftest import write_question

    temp_data = tmp_path / "data"
    write_question(temp_data, canonical_question)
    monkeypatch.setattr(module, "DATA", temp_data)
    rules, drugs = registry_indexes
    report, questions = module.validate_questions(rules, drugs)
    assert report.errors == []
    assert list(questions) == ["MA-Q-0001"]

