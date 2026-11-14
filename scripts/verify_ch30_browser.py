#!/usr/bin/env python3
"""Smoke-test published Chapter 30 individual checks, review lists and Random 10."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright


def verify_latest_set(browser, target: str) -> None:
    """Check the newest set on the actual page, using an isolated browser profile."""
    source = Path(__file__).resolve().parents[1] / "site/mpje-side-notes/exam-simulation-30/questions.js"
    match = re.search(r"window\.MPJE_CH30_QUESTIONS\s*=\s*(\[[\s\S]*\]);\s*$", source.read_text())
    assert match, "Canonical question data is not parseable"
    expected = json.loads(match.group(1))
    latest = max(q["set"] for q in expected)
    context = browser.new_context(viewport={"width": 390, "height": 844})
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    page.goto(target + "?set=" + str(latest), wait_until="domcontentloaded", timeout=60000)
    page.locator("#question-grid .ch30-question").first.wait_for(timeout=30000)
    live = page.evaluate("window.MPJE_CH30_QUESTIONS")
    assert live == expected, "Published question data does not match this commit"
    questions = [q for q in live if q["set"] == latest]
    assert len(questions) == 5
    assert page.locator("#set-heading").inner_text() == f"Practice Set {latest}"
    assert page.locator("#question-grid .ch30-question").count() == 5
    assert page.locator("#question-grid .exam-feedback").count() == 0
    for index, q in enumerate(questions):
        card = page.locator('#question-grid [data-question-id="' + q["id"] + '"]')
        for letter in q["correct"]:
            card.locator('input[value="' + letter + '"]').check()
        card.locator(".ch30-check").click()
        assert card.locator(".exam-right").count() == 1
        assert card.locator(".exam-explanations > p").count() >= 4
        assert card.locator(".exam-reference a").get_attribute("href") == q["url"]
        assert page.locator("#question-grid .exam-feedback").count() == index + 1
    assert page.locator("#set-progress").inner_text() == "5/5 checked"
    multi = next(q for q in questions if q["kind"] == "multi")
    card = page.locator('#question-grid [data-question-id="' + multi["id"] + '"]')
    card.locator(".ch30-retry").click()
    card.locator('input[value="' + multi["correct"][0] + '"]').check()
    card.locator(".ch30-check").click()
    assert card.locator(".exam-wrong").count() == 1, "Incomplete SATA accepted"
    card.locator(".ch30-retry").click()
    extra = next(letter for letter in "ABCD" if letter not in multi["correct"])
    for letter in multi["correct"] + [extra]:
        card.locator('input[value="' + letter + '"]').check()
    card.locator(".ch30-check").click()
    assert card.locator(".exam-wrong").count() == 1, "Overselected SATA accepted"
    saved_selector = '#saved-question-grid [data-question-id="' + multi["id"] + '"]'
    assert page.locator(saved_selector).count() == 1
    page.reload(wait_until="domcontentloaded")
    assert page.locator(saved_selector).count() == 1
    assert not errors, "Newest-set browser errors: " + "; ".join(errors)
    context.close()
    print(f"PASS: public bank matches all {len(expected)} committed questions; Set {latest} all five checks, hidden keys, four-choice rationales and source links")
    print("PASS: newest-set incomplete and overselected SATA rejected; repeated-miss bookmark persisted")


def verify(base_url: str) -> None:
    target = urljoin(base_url.rstrip("/") + "/", "mpje-side-notes/exam-simulation-30/")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        page.goto(target, wait_until="domcontentloaded", timeout=60000)
        page.locator("#question-grid .ch30-question").first.wait_for(timeout=30000)

        fixed = page.locator('#question-grid [data-question-id="E30-001"]')
        assert fixed.count() == 1
        assert page.locator("#question-grid .ch30-question").count() == 5
        assert fixed.locator(".exam-feedback").count() == 0
        assert page.locator("#question-grid .exam-feedback").count() == 0
        # One wrong attempt must not reveal the remaining four answers.
        fixed.locator('input[value="A"]').check()
        fixed.get_by_role("button", name="Check this answer").click()
        assert fixed.locator(".exam-wrong").count() == 1
        assert page.locator("#question-grid .exam-feedback").count() == 1
        assert page.locator("#set-progress").inner_text().startswith("1/5 checked")
        assert page.locator('#wrong-question-grid [data-question-id="E30-001"]').count() == 1

        # Repeated mistake auto-saves the question; user can retry individually.
        fixed.get_by_role("button", name="Try this question again").click()
        fixed.locator('input[value="A"]').check()
        fixed.get_by_role("button", name="Check this answer").click()
        assert page.locator('#saved-question-grid [data-question-id="E30-001"]').count() == 1
        assert page.locator('#wrong-question-grid [data-question-id="E30-001"]').count() == 1

        # Correct recovery clears wrong queue but does not delete bookmark.
        fixed.get_by_role("button", name="Try this question again").click()
        fixed.locator('input[value="C"]').check()
        fixed.get_by_role("button", name="Check this answer").click()
        page.locator("#wrong-refresh").click()
        assert page.locator('#wrong-question-grid [data-question-id="E30-001"]').count() == 0
        assert page.locator('#saved-question-grid [data-question-id="E30-001"]').count() == 1

        # Manual bookmark must be independent of wrong-count history.
        second = page.locator('#question-grid [data-question-id="E30-002"]')
        second.get_by_role("button", name="Save question: E30-002").click()
        assert page.locator('#saved-question-grid [data-question-id="E30-002"]').count() == 1

        random_cards = page.locator("#random-question-grid .ch30-question")
        assert random_cards.count() == 10
        def random_ids_and_counts():
            ids = random_cards.evaluate_all("(els) => els.map(el => el.dataset.questionId)")
            areas = random_cards.evaluate_all("(els) => els.map(el => Number(el.dataset.area))")
            counts = {area: areas.count(area) for area in (1, 2, 3, 4)}
            assert len(ids) == 10 and len(set(ids)) == 10
            assert counts == {1: 2, 2: 3, 3: 3, 4: 2}, counts
            return set(ids)
        before = random_ids_and_counts()
        page.locator("#random-new-top").click()
        after = random_ids_and_counts()
        assert before != after, "New Random 10 repeated the same question combination"
        first_random = random_cards.first
        first_random.locator('input[value="A"]').check()
        first_random.get_by_role("button", name="Check this answer").click()
        assert page.locator("#random-question-grid .exam-feedback").count() == 1
        assert page.locator("#random-progress").inner_text().endswith("1/10 checked")
        assert page.locator("#random-question-grid .exam-reference").count() == 1
        page.reload(wait_until="domcontentloaded")
        assert page.locator('#saved-question-grid [data-question-id="E30-001"]').count() == 1
        assert page.locator('#saved-question-grid [data-question-id="E30-002"]').count() == 1
        assert page.locator("#random-question-grid .exam-feedback").count() == 1
        assert page.locator("#review-nav-count").inner_text().find("saved") != -1
        assert not errors, "Browser JavaScript exceptions: " + "; ".join(errors)
        verify_latest_set(browser, target)
        browser.close()
        print("PASS: fixed per-question check; two mistakes auto-bookmark; wrong review recovery")
        print("PASS: manual saved questions; Random 10 quotas and new combination; per-item random feedback")
        print("PASS: localStorage persistence, 5-question and 10-question modes, no browser JS exceptions")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    args = parser.parse_args()
    verify(args.base_url)


if __name__ == "__main__":
    main()
