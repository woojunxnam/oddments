#!/usr/bin/env python3
"""Exercise the draft33 learner flow locally or on the actual Pages origin."""
from __future__ import annotations

import argparse
import functools
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading
import time
import urllib.request

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def verify(base_url: str, output: Path) -> dict:
    base = base_url.rstrip('/') + '/'
    output.mkdir(parents=True, exist_ok=True)
    expected = (ROOT / 'site/draft-practice/questions.json').read_bytes()
    with urllib.request.urlopen(base + 'draft-practice/questions.json?qa=' + str(time.time_ns()), timeout=30) as response:
        actual = response.read()
    assert actual == expected, 'Draft questions differ from this checkout'
    payload = json.loads(actual)
    checks = ['Actual HTTP questions bytes match the checkout']
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(accept_downloads=True)
        context.add_init_script("localStorage.setItem('mpje.canonical.qa-sentinel','old-canonical');localStorage.setItem('mpje.practice.qa-sentinel','old-legacy');")
        page = context.new_page()
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto(base + 'draft-practice/')
        page.wait_for_function("document.querySelector('#load-status').textContent.includes('제안 답 채점 32개')")
        assert page.locator('#question-list button').count() == 33
        assert not page.locator('#question-panel').is_hidden()
        for index, q in enumerate(payload['questions']):
            page.locator('[data-question-id="' + q['id'] + '"]').click()
            assert page.locator('#question-stem').inner_text() == q['stem']
            assert page.locator('#choices input').count() == 4
            assert page.locator('#choices').inner_text().strip() == '\n'.join(c['id'] + '. ' + c['text'] for c in q['choices'])
            if q['scoring_policy'] == 'NO_GRADE':
                assert page.locator('#hold-notice').is_visible()
                assert '운영' in page.locator('#hold-notice').inner_text()
            page.locator('#choices input[value="' + q['proposed_key'][0] + '"]').check()
            page.locator('#check').click()
            assert page.locator('#explanation').is_visible()
            assert page.locator('#core-reasoning').inner_text() == q['core_ko']
            for reason in q['analysis_ko'].values():
                assert reason in page.locator('#choice-analysis').inner_text()
            if q['scoring_policy'] == 'NO_GRADE':
                assert '점수 집계를 하지 않습니다' in page.locator('#result').inner_text()
            else:
                assert '작성자 제안 답과 일치' in page.locator('#result').inner_text()
        assert '채점·확인 33/33 · 제안 답 일치 32 · 다름 0 · HOLD 확인 1' in page.locator('#progress').inner_text()
        checks.append('All33 stems/132 choices and Korean rationales render; 32 proposed-key matches + HOLD excluded')
        first = payload['questions'][0]
        page.locator('[data-question-id="' + first['id'] + '"]').click()
        wrong = next(c['id'] for c in first['choices'] if c['id'] != first['proposed_key'][0])
        page.locator('#choices input[value="' + wrong + '"]').check()
        page.locator('#check').click()
        assert '제안 답과 다릅니다' in page.locator('#result').inner_text()
        note = '<img src=x onerror="window.__injected=1"> 검토 메모 😀'
        page.locator('#note').fill(note)
        page.locator('#bookmark').click()
        assert page.locator('#bookmark').get_attribute('aria-pressed') == 'true'
        page.locator('#scope').select_option('wrong')
        assert page.locator('#question-list button').count() == 1
        page.locator('#scope').select_option('bookmarked')
        assert page.locator('#question-list button').count() == 1
        page.locator('#scope').select_option('hold')
        assert page.locator('#question-list button').count() == 1
        assert '채점 제외' in page.locator('#question-status').inner_text()
        page.locator('#scope').select_option('all')
        page.locator('#search').fill('Thalidomide')
        assert page.locator('#question-list button').count() == 1
        page.locator('#search').fill('검색결과없음x73825')
        assert page.locator('#empty').is_visible()
        page.locator('#search').fill('')
        page.locator('[data-question-id="' + first['id'] + '"]').click()
        page.reload()
        page.wait_for_function("document.querySelector('#question-stem').textContent.length>10")
        assert page.locator('#note').input_value() == note
        assert page.locator('#bookmark').get_attribute('aria-pressed') == 'true'
        assert page.locator('#choices input[value="' + wrong + '"]').is_checked()
        assert page.evaluate('window.__injected === undefined')
        assert page.evaluate("localStorage.getItem('mpje.canonical.qa-sentinel')") == 'old-canonical'
        assert page.evaluate("localStorage.getItem('mpje.practice.qa-sentinel')") == 'old-legacy'
        checks.append('Wrong-answer/bookmark/HOLD/search filters, reload persistence and existing storage isolation')
        with page.expect_download() as info:
            page.locator('#export').click()
        backup = output / 'synthetic-study-backup.json'
        info.value.save_as(backup)
        data = json.loads(backup.read_text())
        assert len(data['records']) == 33
        assert not any('matches' in r or 'stem' in r for r in data['records'])
        before = page.evaluate("localStorage.getItem('mpje.draft33.practice.v1')")
        stale = json.loads(backup.read_text()); stale['records'][0]['content_hash'] = '0' * 64
        page.locator('#import').set_input_files({'name': 'stale.json', 'mimeType': 'application/json', 'buffer': json.dumps(stale).encode()})
        page.wait_for_function("document.querySelector('#backup-status').textContent.includes('기존 기록은 변경하지 않았습니다')")
        assert page.evaluate("localStorage.getItem('mpje.draft33.practice.v1')") == before
        page.locator('#import').set_input_files(backup)
        page.wait_for_function("document.querySelector('#backup-status').textContent.includes('일치하는 연습 기록')")
        assert page.locator('#note').input_value() == note
        checks.append('Exact-version backup restore, stale hash atomic rejection, escaped note content and no stored score trust')
        page.goto(base + 'draft-practice/#MA-DRAFT33-033')
        page.wait_for_function("document.querySelector('#position').textContent.includes('MA-DRAFT33-033')")
        assert page.locator('#question-stem').inner_text() == payload['questions'][-1]['stem']
        page.goto(base + 'draft-practice/#unknown')
        page.wait_for_function("document.querySelector('#load-status').textContent.includes('요청한 문항을 찾지 못해')")
        assert page.locator('#question-stem').inner_text() == first['stem']
        page.locator('#next').click()
        assert page.locator('#question-stem').inner_text() == payload['questions'][1]['stem']
        page.locator('#previous').click()
        assert page.locator('#question-stem').inner_text() == first['stem']
        page.locator('#shuffle').click()
        assert page.locator('#question-list button').count() == 33
        checks.append('Direct links, unknown-ID recovery, previous/next and shuffled33 preserve IDs')
        for width in (320, 390, 768, 1440):
            page.set_viewport_size({'width': width, 'height': 900})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), width
            page.screenshot(path=str(output / f'draft33-{width}.png'), full_page=False)
        checks.append('No horizontal overflow at320/390/768/1440 widths')
        assert not errors, errors
        context.close()
        context = browser.new_context()
        context.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new DOMException('blocked','SecurityError')}})")
        page = context.new_page(); page.goto(base + 'draft-practice/')
        page.wait_for_function("document.querySelector('#load-status').textContent.includes('제안 답 채점 32개')")
        assert page.locator('#storage-warning').is_visible()
        page.locator('#choices input[value="' + first['proposed_key'][0] + '"]').check(); page.locator('#check').click()
        assert '작성자 제안 답과 일치' in page.locator('#result').inner_text()
        checks.append('Blocked storage has visible notice and working in-memory grading')
        context.close()
        context = browser.new_context(); page = context.new_page()
        page.route('**/draft-practice/questions.json', lambda route: route.fulfill(status=503, body='unavailable'))
        page.goto(base + 'draft-practice/'); page.locator('#load-error').wait_for(state='visible')
        assert page.locator('#question-panel').is_hidden()
        assert page.locator('#question-list button').count() == 0
        checks.append('Payload failure is visible and provides no stale grading UI')
        context.close()
        malformed = json.loads(actual)
        malformed['questions'][0]['analysis_ko'] = {'A|B|C|D': '합쳐진 잘못된 해설'}
        body = {k: v for k, v in malformed['questions'][0].items() if k != 'content_hash'}
        malformed['questions'][0]['content_hash'] = hashlib.sha256(json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        context = browser.new_context(); page = context.new_page()
        page.route('**/draft-practice/questions.json', lambda route: route.fulfill(status=200, content_type='application/json', body=json.dumps(malformed, ensure_ascii=False)))
        page.goto(base + 'draft-practice/'); page.locator('#load-error').wait_for(state='visible')
        assert page.locator('#question-panel').is_hidden()
        assert page.locator('#question-list button').count() == 0
        checks.append('Rehashed malformed combined rationale keys are rejected before display or grading')
        context.close(); browser.close()
    result = {'status': 'PASS', 'base_url': base, 'question_count': 33, 'proposed_key_gradable': 32, 'held_ungraded': 1, 'questions_sha256': hashlib.sha256(actual).hexdigest(), 'checks_passed': checks, 'uncaught_js_errors': errors, 'real_user_profile_used': False, 'canonical_RELEASED_or_legal_audit_credit': 0}
    (output / 'report.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url')
    parser.add_argument('--site', type=Path, default=ROOT / 'site')
    parser.add_argument('--output', type=Path, default=ROOT / 'test-results/draft33')
    args = parser.parse_args()
    server = None
    try:
        base = args.base_url
        if not base:
            handler = functools.partial(SimpleHTTPRequestHandler, directory=str(args.site))
            server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
            threading.Thread(target=server.serve_forever, daemon=True).start()
            base = f'http://127.0.0.1:{server.server_port}/'
        print(json.dumps(verify(base, args.output), ensure_ascii=False))
    finally:
        if server:
            server.shutdown(); server.server_close()


if __name__ == '__main__':
    main()
