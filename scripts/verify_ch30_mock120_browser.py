#!/usr/bin/env python3
"""End-to-end test for two fixed 120-question Chapter 30 practice exams.

Run against local or deployed site:
  python scripts/verify_ch30_mock120_browser.py --base-url https://.../oddments/
Uses original public question data and test-only browser contexts; no exam answer content leaks.
"""
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
            errors: list[str] = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.on("dialog", lambda dialog: dialog.accept())
            page.goto(target + "mock-120.html", wait_until="domcontentloaded", timeout=60000)
            page.locator("#mock-open-a").wait_for(timeout=30000)
            assert page.locator("#mock-error").is_hidden(), page.locator("#mock-error").inner_text()
            assert page.locator("#mock-open-a").is_enabled()
            assert page.locator("#mock-open-b").is_enabled()
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")

            info = page.evaluate("""() => {
              const f=window.MPJE_CH30_MOCK_FORMS, q=window.MPJE_CH30_QUESTIONS;
              return {length:q.length,a:f.forms.A,b:f.forms.B,
                kindA:f.forms.A.map(id=>q.find(v=>v.id===id).kind),
                kindB:f.forms.B.map(id=>q.find(v=>v.id===id).kind)};
            }""")
            assert info["length"] == 240
            assert len(info["a"]) == len(info["b"]) == 120
            assert len(set(info["a"] + info["b"])) == 240
            assert info["kindA"].count("single") == info["kindB"].count("single") == 72
            assert info["kindA"].count("multi") == info["kindB"].count("multi") == 48

            page.locator("#mock-open-a").click()
            assert page.locator("#mock-running").is_visible()
            assert page.locator("#mock-completed").is_hidden()
            assert page.locator("#mock-open-b").is_disabled()
            assert page.locator("#mock-review").is_hidden()
            assert page.locator("#mock-timer").inner_text().startswith(("2:30:", "2:29:"))
            assert page.locator("#mock-running .exam-explanations").count() == 0
            q_a = page.evaluate("""() => window.MPJE_CH30_MOCK_FORMS.forms.A.map(id =>
              window.MPJE_CH30_QUESTIONS.find(q=>q.id===id))""")
            # Official 2026 MPJE bulletin prohibits skipping unanswered questions.
            page.locator("#mock-next").click()
            assert page.locator("#mock-position").inner_text() == "Question 1 of 120"
            assert "does not allow skipping" in page.locator("#mock-running-note").inner_text()
            # First response is kept as draft through reload. No progress answer is recorded yet.
            first = q_a[0]
            for answer in first["correct"]:
                page.locator('#mock-question input[value="' + answer + '"]').check()
            before = page.evaluate("""() => {
              const raw=JSON.parse(localStorage.getItem('mpje-side-notes-ch30-mock120-v1'));
              return {index:raw.current.A.index,draft:raw.current.A.draft};
            }""")
            assert before["index"] == 0 and before["draft"][first["id"]] == sorted(first["correct"])
            page.reload(wait_until="domcontentloaded")
            assert page.locator("#mock-running").is_visible()
            assert sorted(page.locator("#mock-question input:checked").evaluate_all("(xs)=>xs.map(x=>x.value)")) == sorted(first["correct"])
            page.locator("#mock-next").click()
            assert page.locator("#mock-position").inner_text() == "Question 2 of 120"
            assert page.locator("#mock-completed").is_hidden()
            assert page.evaluate("(id) => window.MPJE_CH30_PROGRESS.get(id).attempts", first["id"]) == 0

            for item in q_a[1:]:
                for answer in item["correct"]:
                    page.locator('#mock-question input[value="' + answer + '"]').check()
                page.locator("#mock-next").click()
            assert page.locator("#mock-completed").is_visible()
            assert page.locator("#mock-running").is_hidden()
            assert page.locator("#mock-score").inner_text().find("120/120") != -1
            assert page.locator("#mock-review .mock-explanations p").count() >= 4
            assert page.locator("#mock-review .exam-reference a").get_attribute("href") == first["url"]
            assert page.locator("#mock-review-picker option").count() == 120
            assert page.evaluate("(id)=>window.MPJE_CH30_PROGRESS.get(id).attempts", first["id"]) == 1
            assert page.locator("#mock-open-b").is_enabled()

            page.locator("#mock-open-b").click()
            assert page.locator("#mock-running").is_visible()
            assert page.locator("#mock-position").inner_text() == "Question 1 of 120"
            b_state = page.evaluate("""() => JSON.parse(
              localStorage.getItem('mpje-side-notes-ch30-mock120-v1')).current.B""")
            assert not any(b_state["exposureAtStart"].values()), "Disjoint B must remain unseen on fresh profile"
            # Force a time-expiry edge case in a test-only browser profile.
            page.evaluate("""() => {
              const key='mpje-side-notes-ch30-mock120-v1';
              const state=JSON.parse(localStorage.getItem(key));
              state.current.B.deadlineAt=Date.now()-1000;
              localStorage.setItem(key,JSON.stringify(state));
            }""")
            page.reload(wait_until="domcontentloaded")
            assert page.locator("#mock-completed").is_visible()
            b_end = page.evaluate("""() => JSON.parse(
              localStorage.getItem('mpje-side-notes-ch30-mock120-v1')).current.B""")
            assert b_end["finishReason"] == "time-expired"
            assert len(b_end["submitted"]) == 0
            assert "0/120" in page.locator("#mock-score").inner_text()
            assert page.evaluate("(id)=>window.MPJE_CH30_PROGRESS.get(id).attempts", info["b"][0]) == 0
            page.locator("#mock-retake").click()
            post = page.evaluate("""() => JSON.parse(
              localStorage.getItem('mpje-side-notes-ch30-mock120-v1'))""")
            assert post["current"]["B"]["status"] == "active"
            assert len(post["history"]) == 1
            assert not errors, f"Mock browser exceptions ({width}px): {errors}"
            context.close()
        browser.close()
        print("PASS: disjoint fixed 120/120 manifests, 72 SBA/48 SATA each")
        print("PASS: 150-minute clock, form isolation, reload drafts, one-way progression")
        print("PASS: 120/120 perfect exact-match scoring, post-exam explanations, progress sync")
        print("PASS: time expiry, unvisited questions stay unseen, historical retake")
        print("PASS: mobile 390px and desktop 1280px browser tests, no uncaught JS errors")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    args = parser.parse_args()
    verify(args.base_url)
