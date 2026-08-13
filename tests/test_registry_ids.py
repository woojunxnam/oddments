from __future__ import annotations

import pytest

from qa_common import QAReport, index_records


@pytest.mark.parametrize(
    ("id_field", "record_id"),
    [
        ("rule_id", "MA-DUPLICATE-RULE"),
        ("drug_id", "duplicate-drug"),
        ("question_id", "MA-Q-9999"),
    ],
)
def test_duplicate_registry_ids_are_rejected(tmp_path, id_field, record_id) -> None:
    first_path = tmp_path / "first.json"
    second_path = tmp_path / "second.json"
    report = QAReport()
    index_records(
        [(first_path, {id_field: record_id}), (second_path, {id_field: record_id})],
        id_field,
        report,
    )
    assert any(f"duplicate {id_field} {record_id}" in error for error in report.errors)

