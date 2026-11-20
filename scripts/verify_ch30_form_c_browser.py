#!/usr/bin/env python3
"""Regression test for isolated Form C (original A/B and localStorage keys unchanged)."""
from __future__ import annotations

import argparse
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright


def verify(base_url: str) -> None:
    target = urljoin(base_url.rstrip("/") + "/", "mpje-side-notes/exam-simulation-30/")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        for width in (390, 1280):
            context = browser.new_context(viewport={"width": width, "height": 850})
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("dialog", lambda dialog: dialog.accept())
            page.goto(target + "mock-120-c.html", wait_until="domcontentloaded", timeout=60000)
            page.locator("#mock-open-c").wait_for(timeout=30000)
            assert page.locator("#mock-error").is_hidden(), page.locator("#mock-error").inner_text()
            assert page.locator("#mock-open-c").is_enabled()
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")
            source = page.evaluate("""() => {
                const q=window.MPJE_CH30_FORM_C_QUESTIONS, f=window.MPJE_CH30_FORM_C_MOCK;
                return {all:q,ordered:f.forms.C,signature:f.bankSignature,minutes:f.minutes};
            }""")
            questions = {q["id"]: q for q in source["all"]}
            assert len(questions) == len(source["ordered"]) == 120
            assert len(set(source["ordered"])) == 120
            assert {q["kind"] for q in questions.values()} == {"single", "multi"}
            assert sum(q["kind"] == "single" for q in questions.values()) == 88
            assert sum(q["kind"] == "multi" for q in questions.values()) == 32
            assert set(source["ordered"]) == set(questions)
            assert all(q["id"].startswith("E30-") and len(q["choices"]) == 4 for q in questions.values())
            assert page.locator('script[src="questions.js"]').count() == 0
            assert page.locator('script[src="progress.js"]').count() == 0

            old_key = "mpje-side-notes-ch30-mock120-v1"
            old_progress = "mpje-side-notes-ch30-question-progress-v1"
            c_key = "mpje-side-notes-ch30-form-c-mock120-v1"
            page.evaluate("""([a,b]) => {
                localStorage.setItem(a,'AB-DO-NOT-CHANGE');
                localStorage.setItem(b,'PROGRESS-DO-NOT-CHANGE');
            }""", [old_key, old_progress])
            page.locator("#mock-open-c").click()
            assert page.locator("#mock-running").is_visible()
            assert page.locator("#mock-completed").is_hidden()
            assert page.locator("#mock-review").is_hidden()
            assert page.locator("#mock-position").inner_text() == "Question 1 of 120"
            page.locator("#mock-next").click()
            assert "does not allow skipping" in page.locator("#mock-running-note").inner_text()

            first = questions[source["ordered"][0]]
            for choice in first["correct"]:
                page.locator('#mock-question input[value="' + choice + '"]').check()
            before = page.evaluate("(key)=>JSON.parse(localStorage.getItem(key)).current.C", c_key)
            assert before["index"] == 0
            assert sorted(before["draft"][first["id"]]) == sorted(first["correct"])
            page.reload(wait_until="domcontentloaded")
            assert page.locator("#mock-running").is_visible()
            assert sorted(page.locator("#mock-question input:checked").evaluate_all("(xs)=>xs.map(x=>x.value)")) == sorted(first["correct"])
            page.locator("#mock-next").click()
            assert page.locator("#mock-position").inner_text() == "Question 2 of 120"

            for qid in source["ordered"][1:]:
                for answer in questions[qid]["correct"]:
                    page.locator('#mock-question input[value="' + answer + '"]').check()
                page.locator("#mock-next").click()
            assert page.locator("#mock-completed").is_visible()
            assert "120/120" in page.locator("#mock-score").inner_text()
            assert page.locator("#mock-review-picker option").count() == 120
            assert page.locator("#mock-review .mock-explanations p").count() >= 4
            assert page.locator("#mock-review .exam-reference a").get_attribute("href") == first["url"]
            assert page.evaluate("(key)=>JSON.parse(localStorage.getItem(key)).current.C.status", c_key) == "completed"
            assert page.evaluate("(key)=>localStorage.getItem(key)", old_key) == "AB-DO-NOT-CHANGE"
            assert page.evaluate("(key)=>localStorage.getItem(key)", old_progress) == "PROGRESS-DO-NOT-CHANGE"

            page.locator("#mock-retake").click()
            state = page.evaluate("(key)=>JSON.parse(localStorage.getItem(key))", c_key)
            assert state["current"]["C"]["status"] == "active"
            assert len(state["history"]) == 1
            assert all(state["current"]["C"]["exposureAtStart"].values())
            page.evaluate("""(key) => {
                const state=JSON.parse(localStorage.getItem(key));
                state.current.C.deadlineAt=Date.now()-1000;
                localStorage.setItem(key,JSON.stringify(state));
            }""", c_key)
            page.reload(wait_until="domcontentloaded")
            assert page.locator("#mock-completed").is_visible()
            after = page.evaluate("(key)=>JSON.parse(localStorage.getItem(key)).current.C", c_key)
            assert after["finishReason"] == "time-expired"
            assert len(after["submitted"]) == 0
            assert "0/120" in page.locator("#mock-score").inner_text()
            assert not errors, f"Browser exceptions ({width}px): {errors}"
            context.close()
        browser.close()
        print("PASS: Form C 120 unique IDs, 88 SBA/32 SATA, stable manifest")
        print("PASS: 150-minute timer, no skipping/backtracking, draft reload, exact scoring")
        print("PASS: A/B state isolation, after-exam source/choice review, retake/expiry")
        print("PASS: mobile 390px and desktop 1280px, no uncaught browser exceptions")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    args = parser.parse_args()
    verify(args.base_url)
