from __future__ import annotations

from copy import deepcopy
from datetime import date

from conftest import ROOT
from qa_common import load_json, semantic_content_hash
from release_context import validate_release_date


def context() -> tuple[dict, dict]:
    blueprint = load_json(ROOT / "data" / "blueprint.json")
    profile = load_json(ROOT / "data" / "exam_style" / "mpje_style_profile.json")
    return blueprint, profile


def test_pre2027_release_context_allowed_on_2026_08_13() -> None:
    blueprint, profile = context()
    assert validate_release_date(blueprint, profile, reference_date=date(2026, 8, 13)).errors == []


def test_pre2027_release_context_allowed_on_2027_02_28() -> None:
    blueprint, profile = context()
    assert validate_release_date(blueprint, profile, reference_date=date(2027, 2, 28)).errors == []


def test_pre2027_release_context_blocked_on_2027_03_01() -> None:
    blueprint, profile = context()
    report = validate_release_date(blueprint, profile, reference_date=date(2027, 3, 1))
    assert any("BLUEPRINT_REVIEW_REQUIRED" in error for error in report.errors)


def test_explicit_historical_exam_target_remains_supported() -> None:
    blueprint, profile = context()
    report = validate_release_date(
        blueprint,
        profile,
        reference_date=date(2027, 3, 1),
        target_exam_date=date(2027, 2, 28),
    )
    assert report.errors == []


def test_blueprint_and_profile_hashes_ignore_formatting_only_changes() -> None:
    blueprint, profile = context()
    reformatted_blueprint = deepcopy(blueprint)
    reformatted_blueprint["exam"] = "  Massachusetts   MPJE "
    reformatted_profile = deepcopy(profile)
    reformatted_profile["familiarity_goal"] = "  " + profile["familiarity_goal"].replace(" ", "   ")
    assert semantic_content_hash(reformatted_blueprint, "blueprint") == blueprint["content_hash"]
    assert semantic_content_hash(reformatted_profile, "style_profile") == profile["content_hash"]


def test_material_profile_change_changes_hash() -> None:
    _, profile = context()
    changed = deepcopy(profile)
    changed["item_types"] = ["SBA"]
    assert semantic_content_hash(changed, "style_profile") != profile["content_hash"]
