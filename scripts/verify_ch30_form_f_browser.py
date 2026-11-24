#!/usr/bin/env python3
"""Regression test for isolated Form F (A–E histories remain untouched)."""
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
            page.goto(target + "mock-120-f.html", wait_until="domcontentloaded", timeout=60000)
            page.locator("#mock-open-f").wait_for(timeout=30000)
            assert page.locator("#mock-error").is_hidden(), page.locator("#mock-error").inner_text()
            assert page.locator("#mock-open-f").is_enabled()
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")
            source = page.evaluate("""() => {
                const q=window.MPJE_CH30_FORM_F_QUESTIONS, f=window.MPJE_CH30_FORM_F_MOCK;
                return {all:q,ordered:f.forms.F,signature:f.bankSignature,minutes:f.minutes};
            }""")
            questions = {q["id"]: q for q in source["all"]}
            assert len(questions) == len(source["ordered"]) == 120
            assert len(set(source["ordered"])) == 120
            assert {q["kind"] for q in questions.values()} == {"single", "multi"}
            assert sum(q["kind"] == "single" for q in questions.values()) == 61
            assert sum(q["kind"] == "multi" for q in questions.values()) == 59
            assert set(source["ordered"]) == set(questions)
            assert all(q["id"].startswith("F") and len(q["choices"]) == 5 for q in questions.values())
            assert page.locator('script[src="questions.js"]').count() == 0
            assert page.locator('script[src="progress.js"]').count() == 0

            old_key = "mpje-side-notes-ch30-mock120-v1"
            old_progress = "mpje-side-notes-ch30-question-progress-v1"
            e_key = "mpje-side-notes-ch30-form-e-mock120-v1"
            page.evaluate("(key)=>localStorage.setItem(key, 'E-DO-NOT-CHANGE')", e_key)
            c_key = "mpje-side-notes-ch30-form-f-mock120-v1"
            page.evaluate("""([a,b]) => {
                localStorage.setItem(a,'AB-DO-NOT-CHANGE');
                localStorage.setItem(b,'PROGRESS-DO-NOT-CHANGE');
            }""", [old_key, old_progress])
            page.locator("#mock-open-f").click()
            assert page.locator("#mock-running").is_visible()
            assert page.locator("#mock-completed").is_hidden()
            assert page.locator("#mock-review").is_hidden()
            assert page.locator("#mock-position").inner_text() == "Question 1 of 120"
            page.locator("#mock-next").click()
            assert "does not allow skipping" in page.locator("#mock-running-note").inner_text()

            first = questions[source["ordered"][0]]
            for choice in first["correct"]:
                page.locator('#mock-question input[value="' + choice + '"]').check()
            before = page.evaluate("(key)=>JSON.parse(localStorage.getItem(key)).current.F", c_key)
            assert before["index"] == 0
            assert sorted(before["draft"][first["id"]]) == sorted(first["correct"])
            page.reload(wait_until="domcontentloaded")
            assert page.locator("#mock-running").is_visible()
            assert sorted(page.locator("#mock-question input:checked").evaluate_all("(xs)=>xs.map(x=>x.value)")) == sorted(first["correct"])
            page.locator("#mock-next").click()
            assert page.locator("#mock-position").inner_text() == "Question 2 of 120"

            wrong_id = next(qid for qid in source["ordered"][1:] if questions[qid]["kind"] == "multi")
            for qid in source["ordered"][1:]:
                chosen = questions[qid]["correct"]
                if qid == wrong_id:
                    chosen = chosen[:1]  # Strict subset of SATA key is incorrect.
                for answer in chosen:
                    page.locator('#mock-question input[value="' + answer + '"]').check()
                page.locator("#mock-next").click()
            assert page.locator("#mock-completed").is_visible()
            assert "119/120" in page.locator("#mock-score").inner_text()
            assert page.locator("#mock-review-picker option").count() == 120
            page.locator("#review-hub-filter").select_option("incorrect")
            assert page.locator("#review-hub-list button").count() == 1
            page.locator("#mock-review-picker").select_option("0")
            assert page.locator("#mock-review .mock-explanations p").count() >= 4
            assert page.locator("#mock-review .exam-reference a").first.get_attribute("href") == first["url"]
            assert page.locator("#mock-review .mock-explanations p").count() >= 5
            assert page.evaluate("(key)=>JSON.parse(localStorage.getItem(key)).current.F.status", c_key) == "completed"
            assert page.evaluate("(key)=>localStorage.getItem(key)", old_key) == "AB-DO-NOT-CHANGE"
            assert page.evaluate("(key)=>localStorage.getItem(key)", old_progress) == "PROGRESS-DO-NOT-CHANGE"
            assert page.evaluate("(key)=>localStorage.getItem(key)", e_key) == "E-DO-NOT-CHANGE"

            with page.expect_download() as download:
                page.locator("#mock-download").click()
            assert download.value.suggested_filename.startswith("mpje-ch30-mock-F-")
            page.locator("#mock-retake").click()
            state = page.evaluate("(key)=>JSON.parse(localStorage.getItem(key))", c_key)
            assert state["current"]["F"]["status"] == "active"
            assert len(state["history"]) == 1
            assert all(state["current"]["F"]["exposureAtStart"].values())
            page.evaluate("""(key) => {
                const state=JSON.parse(localStorage.getItem(key));
                state.current.F.deadlineAt=Date.now()-1000;
                localStorage.setItem(key,JSON.stringify(state));
            }""", c_key)
            page.reload(wait_until="domcontentloaded")
            assert page.locator("#mock-completed").is_visible()
            after = page.evaluate("(key)=>JSON.parse(localStorage.getItem(key)).current.F", c_key)
            assert after["finishReason"] == "time-expired"
            assert len(after["submitted"]) == 0
            assert "0/120" in page.locator("#mock-score").inner_text()
            assert page.locator('script[src="mock-review-tools-f.js"]').count() == 1
            page.locator("#review-hub-filter").select_option("unanswered")
            assert page.locator("#review-hub-list button").count() == 120
            assert not errors, f"Browser exceptions ({width}px): {errors}"
            context.close()
        browser.close()
        print("PASS: Form F 120 unique IDs, five-option SBA/SATA, stable manifest")
        print("PASS: 150-minute timer, no skipping/backtracking, draft reload, exact scoring")
        print("PASS: A/B state isolation, after-exam source/choice review, retake/expiry")
        print("PASS: mobile 390px and desktop 1280px, no uncaught browser exceptions")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    args = parser.parse_args()
    verify(args.base_url)
