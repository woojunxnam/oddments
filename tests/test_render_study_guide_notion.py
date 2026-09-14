from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

import pytest

from render_study_guide_notion import KO_SUMMARY, esc, korean_problems, load_guide, render, selected


@pytest.fixture(scope="module")
def guide() -> tuple[dict, dict, list[str]]:
    return load_guide()


def first_verified(guide: tuple[dict, dict, list[str]]) -> tuple[dict, dict]:
    rules, sections, order = guide
    chosen = selected(sections, order)
    assert chosen, "the public guide holds at least one verified section"
    return rules, chosen[0]


def mirrored_notes(section: dict[str, Any]) -> dict[str, Any]:
    """Korean notes that restate every English item word for word, so they keep every number."""

    def ko(text: str) -> str:
        return f"한국어 {text}"

    return {
        "section_id": section["section_id"],
        "source_content_hash": section["content_hash"],
        "learning_objectives": [ko(text) for text in section["learning_objectives"]],
        "orientation": [ko(item["text"]) for item in section["orientation"]],
        "comparison_tables": [
            {"title": ko(table["title"]), "row_notes": [ko(" ".join(row["cells"])) for row in table["rows"]]}
            for table in section["comparison_tables"]
        ],
        "decision_logic": [
            {"condition": ko(step["condition"]), "action": ko(step["action"])} for step in section["decision_logic"]
        ],
        "worked_examples": [
            {
                "scenario": ko(example["scenario"]),
                "steps": [ko(step) for step in example["steps"]],
                "resolution": ko(example["resolution"]),
            }
            for example in section["worked_examples"]
        ],
        "timing_deadlines": [
            ko(" ".join((item["event"], item["timeframe"], item["consequence"]))) for item in section["timing_deadlines"]
        ],
        "role_duties": [ko(" ".join((item["role"], item["duty"]))) for item in section["role_duties"]],
        **{
            field: [ko(item["text"]) for item in section[field]]
            for field in ("ma_vs_federal", "exceptions", "forms_records", "common_traps", "quick_review")
        },
        "drug_examples": [ko(item["teaching_point"]) for item in section["drug_examples"]],
        "retrieval_prompts": [
            {"prompt": ko(item["prompt"]), "answer": ko(item["answer"])} for item in section["retrieval_prompts"]
        ],
    }


def test_escaping_covers_notion_syntax_and_underscore_runs() -> None:
    assert esc("a_b*c[d]<e>") == "a\\_b\\*c\\[d\\]\\<e\\>"
    # A bare run of underscores is parsed as bold markers and the blank vanishes.
    assert esc("______") == "\\_" * 6


def test_verified_section_renders_with_contiguous_headings_and_no_bare_blanks(guide) -> None:
    rules, section = first_verified(guide)
    text = render(section, rules)

    numbers = [int(number) for number in re.findall(r"(?m)^## (\d+)\. ", text)]
    assert numbers == list(range(1, len(numbers) + 1))
    assert section["independent_audit_id"] in text
    assert not re.search(r"(?<!\\)__", text)


def test_every_table_row_carries_one_cell_per_column(guide) -> None:
    rules, sections, order = guide
    for section in selected(sections, order):
        for table in re.findall(r"<table[^>]*>(.*?)</table>", render(section, rules), re.S):
            widths = {len(re.findall(r"<td>", row)) for row in re.findall(r"<tr>(.*?)</tr>", table, re.S)}
            assert len(widths) == 1, section["section_id"]


def test_a_section_awaiting_audit_is_not_rendered_unless_asked(guide) -> None:
    _, sections, order = guide
    held_back = next(section_id for section_id in order if section_id in sections)
    pending = deepcopy(sections)
    pending[held_back]["verification_status"] = "AUDIT_PENDING"

    assert held_back not in {section["section_id"] for section in selected(pending, order)}
    assert held_back in {section["section_id"] for section in selected(pending, order, include_pending=True)}


def test_korean_notes_render_as_toggles_without_disturbing_the_english(guide) -> None:
    rules, section = first_verified(guide)
    notes = mirrored_notes(section)
    assert korean_problems(section, notes) == []

    english = render(section, rules)
    bilingual = render(section, rules, notes)

    assert KO_SUMMARY not in english
    assert bilingual.count(f"<summary>{KO_SUMMARY}</summary>") >= len(section["orientation"])
    # Every English line survives, in order, with the Korean toggles only added between them.
    remaining = iter(bilingual.splitlines())
    assert all(line in remaining for line in english.splitlines())


def test_korean_notes_are_refused_when_stale_untranslated_or_missing_a_number(guide) -> None:
    _, section = first_verified(guide)

    stale = mirrored_notes(section)
    stale["source_content_hash"] = "0" * 64
    assert any("content hash" in problem for problem in korean_problems(section, stale))

    untranslated = mirrored_notes(section)
    untranslated["quick_review"] = [item["text"] for item in section["quick_review"]]
    assert any(problem.startswith("quick_review[0]: no Korean text") for problem in korean_problems(section, untranslated))

    numbered = next(
        (index for index, item in enumerate(section["retrieval_prompts"]) if re.search(r"\d", item["answer"])), None
    )
    if numbered is None:
        pytest.skip("this section's self-test answers carry no numbers")
    lossy = mirrored_notes(section)
    lossy["retrieval_prompts"][numbered]["answer"] = "한국어 요약"
    assert any(
        problem.startswith(f"retrieval_prompts[{numbered}].answer: drops number")
        for problem in korean_problems(section, lossy)
    )
