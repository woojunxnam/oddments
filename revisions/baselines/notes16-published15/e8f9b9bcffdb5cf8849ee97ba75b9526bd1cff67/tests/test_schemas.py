from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


def test_all_canonical_records_validate_against_schemas(root: Path) -> None:
    registries = {
        "rules": "rule.schema.json",
        "drugs": "drug.schema.json",
        "questions": "question.schema.json",
        "audits": "audit.schema.json",
        "source_manifests": "source_manifest.schema.json",
        "source_signals": "source_signal.schema.json",
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

    standalone = {
        root / "data" / "blueprint.json": "blueprint.schema.json",
        root / "data" / "exam_style" / "mpje_style_profile.json": "exam_style_profile.schema.json",
        root / "data" / "exam_style" / "question_family_matrix.json": "question_family_matrix.schema.json",
        root / "data" / "release_requirements.json": "release_requirements.schema.json",
    }
    for path, schema_name in standalone.items():
        schema = json.loads((root / "schemas" / schema_name).read_text(encoding="utf-8"))
        record = json.loads(path.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        assert list(validator.iter_errors(record)) == []


def test_question_cannot_store_duplicate_realism_metadata(root: Path, canonical_question) -> None:
    schema = json.loads((root / "schemas" / "question.schema.json").read_text(encoding="utf-8"))
    canonical_question["realism"] = {"score": 5}
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(canonical_question))
    assert errors


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
