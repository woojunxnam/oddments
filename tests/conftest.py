from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


@pytest.fixture
def root() -> Path:
    return ROOT


@pytest.fixture
def canonical_question() -> dict:
    path = ROOT / "data" / "questions" / "ma-q-0001.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture
def canonical_sata() -> dict:
    path = ROOT / "data" / "questions" / "ma-q-0002.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture
def canonical_ordered() -> dict:
    path = ROOT / "data" / "questions" / "ma-q-0007.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture
def registry_indexes() -> tuple[dict, dict]:
    from validate_drugs import validate_drugs
    from validate_rules import validate_rules

    rule_report, rules = validate_rules()
    drug_report, drugs = validate_drugs()
    assert rule_report.ok
    assert drug_report.ok
    return deepcopy(rules), deepcopy(drugs)


def write_question(temp_data: Path, question: dict, filename: str = "question.json") -> None:
    directory = temp_data / "questions"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / filename).write_text(json.dumps(question, indent=2) + "\n", encoding="utf-8")

