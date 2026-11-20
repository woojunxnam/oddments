#!/usr/bin/env python3
"""Browser QA for Chapter 30 mixed mock forms and focused incorrect-answer review."""
from __future__ import annotations

import argparse
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

OLD_AB = "mpje-side-notes-ch30-mock120-v1"
OLD_C = "mpje-side-notes-ch30-form-c-mock120-v1"
MIX_KEY = "mpje-side-notes-ch30-mixed-mock120-v1"
REVIEW_KEY = "mpje-side-notes-ch30-mock-review-markers-v1"


def verify(base_url: str) -> None:
    url = urljoin(base_url.rstrip("/") + "/", "mpje-side-notes/exam-simulation-30/")
    with sync_playwright() as play:
        browser = play.chromium.launch(headless=True)
        for width in (390, 1280):
            ctx = browser.new_context(
                viewport={"width": width, "height": 850},
                accept_downloads=True,
            )
            page = ctx.new_page()
            errors: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("dialog", lambda dialog: dialog.accept())
            page.goto(url + "mock-120-mixes.html", wait_until="domcontentloaded", timeout=60000)
            page.locator("#mock-open-cd1").wait_for(timeout=30000)
            assert page.locator("#mock-error").is_hidden(), page.locator("#mock-error").inner_text()
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")
            structure = page.evaluate("""() => {
              const a=window.MPJE_CH30_QUESTIONS,c=window.MPJE_CH30_FORM_C_QUESTIONS,
                d=window.MPJE_CH30_FORM_D_QUESTIONS,m=window.MPJE_CH30_MIXED_MOCK_FORMS,
                ab=window.MPJE_CH30_MOCK_FORMS.forms;
              return {ids:[...a,...c,...d].map(q=>q.id),forms:m.forms,
                original:{A:ab.A,B:ab.B,C:window.MPJE_CH30_FORM_C_QUESTIONS.map(q=>q.id),
                  D:d.map(q=>q.id)},kinds:d.map(q=>q.kind)};
            }""")
            assert len(structure["ids"]) == len(set(structure["ids"])) == 480
            assert structure["kinds"].count("single") == 92
            assert structure["kinds"].count("multi") == 28
            bank = {name: set(ids) for name, ids in structure["original"].items()}
            mixes = structure["forms"]
            assert list(mixes) == ["CD1", "CD2", "ALL1", "ALL2", "ALL3", "ALL4"]
            for name, ordered in mixes.items():
                assert len(ordered) == len(set(ordered)) == 120
                origin = {f: len(set(ordered) & ids) for f, ids in bank.items()}
                if name.startswith("CD"):
                    assert origin == {"A": 0, "B": 0, "C": 60, "D": 60}
                else:
                    assert origin == {"A": 30, "B": 30, "C": 30, "D": 30}
            assert set(mixes["CD1"]).isdisjoint(mixes["CD2"])
            assert set(mixes["CD1"] + mixes["CD2"]) == bank["C"] | bank["D"]
            assert len(set(sum([mixes["ALL" + str(i)] for i in range(1, 5)], []))) == 480

            page.evaluate("""([ab,c])=>{
                localStorage.setItem(ab,'AB-KEEP');
                localStorage.setItem(c,'C-KEEP');
            }""", [OLD_AB, OLD_C])
            page.locator("#mock-open-cd1").click()
            assert page.locator("#mock-running").is_visible()
            assert page.locator("#mock-completed").is_hidden()
            assert page.locator("#mock-review").is_hidden()
            first = page.evaluate("""() => {
              const id=window.MPJE_CH30_MIXED_MOCK_FORMS.forms.CD1[0];
              return [...window.MPJE_CH30_FORM_C_QUESTIONS,...window.MPJE_CH30_FORM_D_QUESTIONS].find(x=>x.id===id);
            }""")
            wrong = next((x for x in ["A", "B", "C", "D"] if x not in first["correct"]), None)
            if wrong is None:
                # All options correct on a SATA case: submitting just one is an exact-match error.
                wrong = "A"
            page.locator(f'#mock-question input[value="{wrong}"]').check()
            page.locator("#mock-next").click()
            assert page.locator("#mock-position").inner_text() == "Question 2 of 120"
            second = page.evaluate("""() => {
              const id=window.MPJE_CH30_MIXED_MOCK_FORMS.forms.CD1[1];
              return [...window.MPJE_CH30_FORM_C_QUESTIONS,...window.MPJE_CH30_FORM_D_QUESTIONS].find(x=>x.id===id);
            }""")
            for answer in second["correct"]:
                page.locator(f'#mock-question input[value="{answer}"]').check()
            page.locator("#mock-next").click()
            page.locator("#mock-finish-early").click()
            assert page.locator("#mock-completed").is_visible()
            assert page.locator("#mock-review-picker option").count() == 120
            page.locator("#review-hub-list button").first.wait_for(timeout=5000)
            assert page.locator("#review-hub-summary").inner_text().count("Incorrect") == 1
            assert "Unanswered" in page.locator("#review-hub-summary").inner_text()
            assert page.locator("#review-hub-list button").count() == 119
            page.locator("#review-hub-filter").select_option("incorrect")
            assert page.locator("#review-hub-list button").count() == 1
            assert first["id"] in page.locator("#mock-review").get_attribute("data-current-question-id")
            assert page.locator("#mock-review .mock-explanations p").count() >= 4
            assert page.locator("#mock-review .exam-reference a").get_attribute("href") == first["url"]
            page.locator("#review-hub-mark").click()
            assert "1/119" in page.locator("#review-hub-summary").inner_text()
            assert page.evaluate("(key)=>JSON.parse(localStorage.getItem(key)).current.CD1.status", MIX_KEY) == "completed"
            with page.expect_download() as download_info:
                page.locator("#review-hub-export").click()
            assert download_info.value.suggested_filename.startswith("mpje-cd1-missed-")
            assert page.evaluate("(k)=>localStorage.getItem(k)", OLD_AB) == "AB-KEEP"
            assert page.evaluate("(k)=>localStorage.getItem(k)", OLD_C) == "C-KEEP"
            assert page.evaluate("(k)=>!!JSON.parse(localStorage.getItem(k)).records", REVIEW_KEY)
            page.reload(wait_until="domcontentloaded")
            page.locator("#review-hub-summary").wait_for(timeout=30000)
            assert "1/119" in page.locator("#review-hub-summary").inner_text()
            page.locator("#review-hub-filter").select_option("pending")
            assert page.locator("#review-hub-list button").count() == 118
            page.locator("#review-hub-next").click()
            assert page.locator("#mock-review .exam-reference a").count() == 1

            # Every other form can start without overwriting a previous mix's completed state.
            for name in ("CD2", "ALL1", "ALL2", "ALL3", "ALL4"):
                page.locator("#mock-open-" + name.lower()).click()
                assert page.locator("#mock-running").is_visible()
                assert "Question 1 of 120" in page.locator("#mock-position").inner_text()
                page.locator("#mock-finish-early").click()
                assert page.locator("#mock-completed").is_visible()
                assert page.locator("#mock-review-picker option").count() == 120
                page.locator("#mock-dashboard").wait_for(state="visible")
            assert page.evaluate("(key)=>JSON.parse(localStorage.getItem(key)).current.CD1.status", MIX_KEY) == "completed"
            assert not errors, f"Browser exceptions ({width}px): {errors}"
            ctx.close()

        # Legacy Form A is still readable after results were saved, including the focused review.
        context = browser.new_context(viewport={"width": 390, "height": 850})
        a_page = context.new_page()
        a_page.on("pageerror", lambda e: (_ for _ in ()).throw(AssertionError(str(e))))
        a_page.on("dialog", lambda dialog: dialog.accept())
        a_page.goto(url + "mock-120.html?form=A")
        a_page.locator("#mock-open-a").click()
        a_page.locator("#mock-finish-early").click()
        a_page.locator("#review-hub-list button").first.wait_for()
        assert a_page.locator("#review-hub-list button").count() == 120
        a_page.locator("#review-hub-mark").click()
        assert "1/120" in a_page.locator("#review-hub-summary").inner_text()
        a_page.reload()
        assert "1/120" in a_page.locator("#review-hub-summary").inner_text()
        assert a_page.locator("#mock-review .exam-reference a").count() == 1
        context.close()
        browser.close()
        print("PASS: C/D and A/B/C/D mix partitions and unique IDs; 120 questions per exam")
        print("PASS: 150-minute timed sessions, original A/B and C exam keys unchanged")
        print("PASS: focused incorrect-only filters, review markers, CSV, reload and mobile layouts")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8173/")
    verify(parser.parse_args().base_url)
