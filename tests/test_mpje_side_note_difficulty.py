"""Regression guard for the Massachusetts MPJE Chapter 28 difficulty expansion.

Scope: public side-note UI only; does not change or assert canonical RELEASED audit status.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site" / "mpje-side-notes"
ASSETS = {
    "licensure-ce": "difficulty-reviewed-01.js",
    "personnel": "difficulty-reviewed-02.js",
    "pharmacy-mor": "difficulty-reviewed-03.js",
    "schedules-registration": "difficulty-reviewed-04.js",
    "prescription-validity": "difficulty-reviewed-05.js",
    "cii-core": "difficulty-reviewed-06.js",
    "cii-partial-outstate": "difficulty-reviewed-07.js",
    "refills-transfer": "difficulty-reviewed-08.js",
    "pmp-oud": "difficulty-reviewed-09.js",
    "label-interchange": "difficulty-reviewed-10.js",
    "counseling-dur": "difficulty-reviewed-11.js",
    "rems": "difficulty-reviewed-12.js",
    "privacy": "difficulty-reviewed-13.js",
    "vaccination-administration": "difficulty-reviewed-14.js",
    "cdtm": "difficulty-reviewed-15.js",
    "prescribing-public-health": "difficulty-reviewed-16.js",
    "ordering-inventory": "difficulty-reviewed-17.js",
    "security-loss-disposal": "difficulty-reviewed-18.js",
    "storage-shipping": "difficulty-reviewed-19.js",
    "shared-automation": "difficulty-reviewed-20.js",
    "nonsterile-compounding": "difficulty-reviewed-21.js",
    "sterile-compounding": "difficulty-reviewed-22.js",
    "hd-outsourcing-nuclear": "difficulty-reviewed-23.js",
    "fda-supply-chain": "difficulty-reviewed-24.js",
    "numbers-records": "difficulty-reviewed-25.js",
    "drug-directory": "difficulty-reviewed-26.js",
    "open-register": "difficulty-reviewed-27.js",
}


def read_difficulty(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    marker = "), {"
    assert marker in text, f"Missing data wrapper in {path}"
    return json.loads(text[text.index(marker) + 3 : text.rfind(");")])


def test_expanded_chapters_have_20_new_items_each() -> None:
    seen_questions: set[str] = set()
    for slug, filename in ASSETS.items():
        data = read_difficulty(SITE / filename)
        assert set(data) == {slug}
        assert set(data[slug]) == {"moderate", "hard"}
        for tier, questions in data[slug].items():
            assert len(questions) == 10, (slug, tier)
            for q in questions:
                assert len(q["choices"]) == 4
                assert len(set(q["choices"])) == 4
                assert len(q["explanations"]) == 4
                assert q["answer"] in "ABCD"
                assert q["explanations"]["ABCD".index(q["answer"])].startswith("Correct.")
                assert q["citation"]
                assert q["sourceUrl"].startswith("https://")
                assert q["sourceUrl"].split("/")[2] in {
                    "www.ecfr.gov", "malegislature.gov", "www.mass.gov",
                    "www.fda.gov", "www.accessdata.fda.gov", "www.hhs.gov",
                    "www.deadiversion.usdoj.gov", "www.cdc.gov", "www.govinfo.gov", "pe.usps.com", "doi.usp.org", "pages.usp.org", "www.dea.gov", "nabp.pharmacy"
                }
                stem = re.sub(r"\W+", "", q["question"].lower())
                assert stem not in seen_questions, (slug, tier, q["question"])
                seen_questions.add(stem)
    assert len(seen_questions) == 540
    assert len(ASSETS) == 27


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js is not installed")
@pytest.mark.parametrize(
    "name",
    ["quiz.js", "practice-review.js", *ASSETS.values()],
)
def test_javascript_syntax(name: str) -> None:
    subprocess.run(["node", "--check", str(SITE / name)], check=True, capture_output=True)


def test_cumulative_page_loads_tiers_before_renderer() -> None:
    page = (SITE / "cumulative-practice" / "index.html").read_text(encoding="utf-8")
    js = (SITE / "practice-review.js").read_text(encoding="utf-8")
    picker = (SITE / "quiz.js").read_text(encoding="utf-8")
    for chapter, filename in ASSETS.items():
        assert f'src="../{filename}"' in page
        assert page.index(f'src="../{filename}"') < page.index('src="../practice-review.js"')
        assert chapter in js
    for section in ["review-original", "review-extra", "review-moderate", "review-hard"]:
        assert f'id="{section}"' in page
    assert "1,080 practice questions" in page
    assert "270 new Moderate and 270 new Hard" in page
    assert "moderateCases.length + hardCases.length" in js
    assert "c.slug !== 'drug-memorization'" in js
    assert "? '40' : '20'" in picker
