"""Draft33 spacing override regression: presentation-only, no canonical payload edits."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site" / "draft-practice"


def test_spacing_overrides_cover_exact_affected_range():
    text = (SITE / "explanation-spacing.js").read_text(encoding="utf-8")
    ids = re.findall(r'"(MA-DRAFT33-\\d{3})": \\{', text)
    assert ids == [f"MA-DRAFT33-{n:03d}" for n in range(22, 34)]
    assert text.count("choices:{") == 12
    assert "MutationObserver(applySpacing)" in text


def test_display_only_integration_preserves_question_json():
    html = (SITE / "index.html").read_text(encoding="utf-8")
    assert '<script src="explanation-spacing.js" defer></script>' in html
    assert html.index('src="explanation-spacing.js"') < html.index('src="app.js"')
    code = (SITE / "explanation-spacing.js").read_text(encoding="utf-8")
    assert "localStorage.setItem" not in code
    assert "proposed_key" not in code
    assert "content_hash" not in code
    assert "textContent" in code
