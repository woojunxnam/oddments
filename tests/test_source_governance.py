from __future__ import annotations

import json

from jsonschema import Draft202012Validator, FormatChecker

from check_private_paths import check_private_paths


def test_restricted_private_paths_cannot_be_tracked() -> None:
    report = check_private_paths(
        [
            "local_private/source.pdf",
            "docs/private_sources/notes.md",
            "licensed_sources/bank.txt",
            "exports/content.private.pdf",
            "exports/content.licensed.pdf",
        ]
    )
    assert len(report.errors) == 5


def test_documented_example_directory_is_allowed() -> None:
    report = check_private_paths(["local_private.example/README.md"])
    assert report.errors == []


def test_unknown_source_permission_must_fail_closed(root) -> None:
    schema = json.loads((root / "schemas" / "source_manifest.schema.json").read_text(encoding="utf-8"))
    manifest = {
        "source_id": "SOURCE-UNKNOWN-TEST",
        "source_class": "LICENSED_PRIVATE",
        "title": "Unknown licensed source",
        "publisher": "Unknown Publisher",
        "url": None,
        "access_type": "UNKNOWN",
        "authority_level": "NON_AUTHORITY",
        "permission_status": "VERIFIED",
        "legal_authority_allowed": False,
        "question_text_storage_allowed": False,
        "ai_processing_allowed": True,
        "public_repo_allowed": False,
        "notes": "Synthetic schema test.",
        "last_reviewed": "2026-08-13"
    }
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(manifest))
    assert errors
