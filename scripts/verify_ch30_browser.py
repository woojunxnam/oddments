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


def verify_unanswered_mode(browser, target: str) -> None:
    """Check unanswered prioritization, exact-ten fallback and selection modes."""
    context = browser.new_context(viewport={"width": 390, "height": 844})
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    page.goto(target, wait_until="domcontentloaded", timeout=60000)
    page.locator("#random-question-grid .ch30-question").first.wait_for(timeout=30000)

    # Across all Areas, leave exactly the 2/3/3/2 quota unanswered.
    # Every other question has a persisted Check Answer attempt.
    unseen = page.evaluate("""() => {
      const quota = {1:2, 2:3, 3:3, 4:2};
      const all = window.MPJE_CH30_QUESTIONS;
      const unseen = [1,2,3,4].flatMap(area =>
        all.filter(q => q.area === area).slice(0, quota[area]).map(q => q.id));
      const items = {};
      all.forEach(q => {
        if (!unseen.includes(q.id)) {
          // Simulate attempts graded against this question's current content.
          // A legacy revision-1 attempt to a revised question is intentionally
          // archived and becomes unseen in the real app, so do not seed it here.
          items[q.id] = {attempts:1, wrongCount:0, needsReview:false,
            saved:false, lastCorrect:true, revision:Number(q.revision)||1};
        }
      });
      localStorage.setItem('mpje-side-notes-ch30-question-progress-v1',
        JSON.stringify({version:1, items, migratedFixed:true, migratedRandom:true}));
      localStorage.removeItem('mpje-side-notes-ch30-random10-v1');
      return unseen;
    }""")
    page.reload(wait_until="domcontentloaded")
    cards = page.locator("#random-question-grid .ch30-question")
    cards.first.wait_for(timeout=30000)
    assert page.locator("#random-mode").input_value() == "unseen"

    def ids():
        values = cards.evaluate_all("(els) => els.map(el => el.dataset.questionId)")
        assert len(values) == 10 and len(set(values)) == 10
        areas = cards.evaluate_all("(els) => els.map(el => Number(el.dataset.area))")
        assert {a: areas.count(a) for a in (1, 2, 3, 4)} == {1:2, 2:3, 3:3, 4:2}
        return set(values)

    first = ids()
    assert first == set(unseen), "Unanswered-first failed to select all ten unseen"
    assert "10/10 have never been checked" in page.locator("#random-message").inner_text()
    assert "Random set #" not in page.locator("#random-message").inner_text()
    assert page.locator("#random-progress").inner_text() == "0/10 checked"

    page.locator("#random-new-top").click()
    second = ids()
    assert second != first, "An identical set must be avoided"
    assert len(second & set(unseen)) == 9, "Fallback should sacrifice only one unseen item"

    # Changing the mode must not discard in-progress answer selections.
    first_card = cards.first
    first_card.locator('input[value="A"]').check()
    page.locator("#random-mode").select_option("all")
    assert ids() == second
    assert first_card.locator('input[value="A"]').is_checked()
    page.locator("#random-new-top").click()
    third = ids()
    assert third != second
    assert page.locator("#random-mode").input_value() == "all"
    page.reload(wait_until="domcontentloaded")
    assert ids() == third and page.locator("#random-mode").input_value() == "all"
    assert page.locator("#random-progress").inner_text() == "0/10 checked"
    assert not errors, "Unanswered-first browser errors: " + "; ".join(errors)
    context.close()
    print("PASS: unanswered-first 2/3/3/2 quotas, 10-unseen priority, minimal fallback, all-mode, answer retention and reload")


def verify_legacy_random_session(browser, target: str) -> None:
    """Old random sessions retain their answers without showing set numbers."""
    context = browser.new_context(viewport={"width": 390, "height": 844})
    page = context.new_page()
    page.goto(target, wait_until="domcontentloaded", timeout=60000)
    page.locator("#random-question-grid .ch30-question").first.wait_for(timeout=30000)
    legacy_id = page.evaluate("""() => {
      const raw = JSON.parse(localStorage.getItem('mpje-side-notes-ch30-random10-v1'));
      raw.number = 42;
      delete raw.mode;
      const first = window.MPJE_CH30_QUESTIONS.find(q => q.id === raw.ids[0]);
      raw.answers = {[first.id]: [first.correct[0]]};
      raw.checked = {[first.id]: true};
      localStorage.setItem('mpje-side-notes-ch30-random10-v1', JSON.stringify(raw));
      return first.id;
    }""")
    page.reload(wait_until="domcontentloaded")
    assert page.locator("#random-mode").input_value() == "all"
    card = page.locator('#random-question-grid [data-question-id="' + legacy_id + '"]')
    assert card.locator(".exam-feedback").count() == 1
    assert card.locator(".exam-explanations > p").count() >= 4
    assert "Random set #" not in page.locator("#random-progress").inner_text()
    assert "Random set #" not in page.locator("#random-message").inner_text()
    state = page.evaluate("""() => JSON.parse(
      localStorage.getItem('mpje-side-notes-ch30-random10-v1'))""")
    assert "number" not in state and state["mode"] == "all"
    context.close()
    print("PASS: prior random-session answers and checks retained; legacy set counter removed")


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
        verify_unanswered_mode(browser, target)
        verify_legacy_random_session(browser, target)
        verify_legal_revision_archive(browser, target)
        browser.close()
        print("PASS: fixed per-question check; two mistakes auto-bookmark; wrong review recovery")
        print("PASS: manual saved questions; Random 10 quotas and new combination; per-item random feedback")
        print("PASS: localStorage persistence, 5-question and 10-question modes, no browser JS exceptions")


def verify_legal_revision_archive(browser, target: str) -> None:
    """Previously answered, revised IDs must lose current credit without losing old history."""
    context = browser.new_context(viewport={"width": 390, "height": 844})
    page = context.new_page()
    page.goto(target + "?set=41", wait_until="domcontentloaded", timeout=60000)
    page.locator('#question-grid [data-question-id="E30-203"]').wait_for(timeout=30000)
    page.evaluate("""() => {
      localStorage.setItem('mpje-side-notes-ch30-question-progress-v1',
        JSON.stringify({version:1,migratedFixed:true,migratedRandom:true,items:{
          'E30-203':{attempts:3,wrongCount:2,needsReview:true,saved:true,lastCorrect:false},
          'E30-209':{attempts:1,wrongCount:0,needsReview:false,saved:false,lastCorrect:true},
          'E30-028':{attempts:4,wrongCount:1,needsReview:false,saved:true,lastCorrect:true}
        }}));
      localStorage.setItem('mpje-side-notes-ch30-v1',JSON.stringify({
        set:41,answers:{'E30-203':['A','D'],'E30-202':['C']},
        checked:{'E30-203':true,'E30-202':true},submitted:{41:true}
      }));
      localStorage.setItem('mpje-side-notes-ch30-random10-v1',JSON.stringify({
        ids:['E30-203','E30-001','E30-002','E30-003','E30-028','E30-005','E30-006','E30-007','E30-004','E30-015'],
        answers:{'E30-203':['A','D'],'E30-001':['C']},
        checked:{'E30-203':true,'E30-001':true},submitted:false,mode:'all'
      }));
    }""")
    page.reload(wait_until="domcontentloaded")
    values = page.evaluate("""() => {
      const p=window.MPJE_CH30_PROGRESS;
      const f=JSON.parse(localStorage.getItem('mpje-side-notes-ch30-v1'));
      const r=JSON.parse(localStorage.getItem('mpje-side-notes-ch30-random10-v1'));
      return {current:p.get('E30-203'),old:p.getArchived('E30-203'),
        current209:p.get('E30-209'),old209:p.getArchived('E30-209'),
        untouched:p.get('E30-028'),fixed203:f.checked['E30-203'],
        fixed202:f.checked['E30-202'],random203:r.checked['E30-203'],
        random001:r.checked['E30-001']};
    }""")
    assert values['current']['attempts']==0 and values['current']['saved'], values
    assert len(values['old'])==1 and values['old'][0]['attempts']==3, values
    assert values['old'][0]['wrongCount']==2, values
    assert values['current209']['attempts']==0 and values['old209'][0]['attempts']==1, values
    assert values['untouched']['attempts']==4 and values['untouched']['saved'], values
    assert values['fixed203'] is None and values['fixed202'] is True, values
    assert values['random203'] is None and values['random001'] is True, values
    card = page.locator('#question-grid [data-question-id="E30-203"]')
    assert card.locator('.exam-feedback').count()==0, "Stale answer exposed revised key"
    assert card.locator('.exam-history').count()>=1
    page.reload(wait_until="domcontentloaded")
    again=page.evaluate("""() => ({
      attempts:window.MPJE_CH30_PROGRESS.get('E30-203').attempts,
      archive:window.MPJE_CH30_PROGRESS.getArchived('E30-203').length
    })""")
    assert again=={"attempts":0,"archive":1}, again
    context.close()
    print("PASS: question revision archives old mistakes, retains bookmarks and unrelated IDs; clears old fixed/random selected answers")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    args = parser.parse_args()
    verify(args.base_url)


if __name__ == "__main__":
    main()
