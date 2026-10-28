#!/usr/bin/env python3
"""Real-HTTP revision/history regression. No simulated storage or legal-audit claim."""
from __future__ import annotations

import argparse
import functools
import http.server
import json
import os
from pathlib import Path
import threading

from playwright.sync_api import expect, sync_playwright
from publish_practice import build_payload

ROOT = Path(__file__).resolve().parents[1]
KEY = 'oddments.mpje.practice.v1'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=Path, default=ROOT / 'public-site')
    parser.add_argument('--base-url', help='Use deployed production HTTP instead of a local HTTP server.')
    parser.add_argument('--evidence', type=Path, default=ROOT / 'test-results/representative-rewrites')
    args = parser.parse_args()
    args.evidence.mkdir(parents=True, exist_ok=True)
    data = build_payload()
    revision = data['representative_revision']
    by_id = {q['question_id']: q for q in data['questions']}
    new = [by_id[i] for i in revision['new_ids']]
    first = new[0]
    legacy_id = first['revision_of']
    legacy_attempt = dict(correct=False, selected=[by_id[legacy_id]['choices'][0]['id']], at='2026-10-27T20:00:00Z', edition='2026-10-27.practice3-quality')
    seed = dict(v=1, bookmarks=[legacy_id, 'MA-REV-0096'], attempts={legacy_id: legacy_attempt}, theme='light', large=False)
    server = None
    if args.base_url:
        base = args.base_url.rstrip('/') + '/'
    else:
        class Quiet(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *args):
                pass
        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(args.site)))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        base = f'http://127.0.0.1:{server.server_port}/'
    checks, errors, exercised_ids = [], [], []
    status, failure = 'failed', None
    def ok(message):
        checks.append(message)
        print('PASS:', message, flush=True)
    try:
        with sync_playwright() as p:
            exe = os.environ.get('CHROMIUM_PATH')
            browser = p.chromium.launch(headless=True, **({'executable_path': exe} if exe else {}))
            context = browser.new_context(viewport={'width': 1440, 'height': 1000}, accept_downloads=True)
            context.add_init_script('if(!localStorage.getItem("revision-test-seeded")){localStorage.setItem(' + json.dumps(KEY) + ',' + json.dumps(json.dumps(seed)) + ');localStorage.setItem("revision-test-seeded","1");localStorage.setItem("unrelated-progress-canary","unchanged");}')
            page = context.new_page()
            page.on('pageerror', lambda e: errors.append(str(e)))
            diag = lambda: page.evaluate('MPJE_DIAGNOSTICS()')
            state = lambda: page.evaluate('(key)=>JSON.parse(localStorage.getItem(key))', KEY)
            page.goto(base + 'practice-expansion/', wait_until='networkidle')
            assert diag()['active'] == first['question_id']
            assert diag()['filtered'] == revision['stats']['recommended']
            assert diag()['total'] == data['published_question_count']
            assert state()['attempts'][legacy_id] == legacy_attempt
            assert first['question_id'] not in state()['attempts']
            expect(page.locator('#bookmark')).to_have_attribute('aria-pressed', 'false')
            ok('old attempt and bookmarks load unchanged; revised default has no inherited attempt/bookmark')
            page.goto(base + 'practice-expansion/#' + legacy_id, wait_until='networkidle')
            assert diag()['active'] == legacy_id
            expect(page.locator('#bookmark')).to_have_attribute('aria-pressed', 'true')
            page.locator('#revision-notice a').click()
            expect(page.locator('#q-meta')).to_contain_text(first['question_id'])
            expect(page.locator('#bookmark')).to_have_attribute('aria-pressed', 'false')
            ok('old exact deep link remains usable and revision cross-link opens the separate new ID')
            for key in first['correct_choice_ids']:
                page.locator('#choice-' + key).check()
            page.locator('#check').click()
            assert state()['attempts'][legacy_id] == legacy_attempt
            assert state()['attempts'][first['question_id']]['correct'] is True
            page.locator('#bookmark').click()
            page.reload(wait_until='networkidle')
            assert state()['attempts'][legacy_id] == legacy_attempt
            assert {legacy_id, first['question_id'], 'MA-REV-0096'} <= set(state()['bookmarks'])
            assert page.evaluate('localStorage.getItem("unrelated-progress-canary")') == 'unchanged'
            ok('new scoring and reload preserve old attempt byte-equivalent values and unrelated storage')
            page.locator('#revision-notice a').click()
            expect(page.locator('#q-meta')).to_contain_text(legacy_id)
            ok('revised case links back to its immutable original')
            for hold in revision['holds']:
                page.goto(base + 'practice-expansion/#' + hold['legacy_question_id'], wait_until='load')
                assert diag()['heldForReview'] is True
                expect(page.locator('#revision-notice')).to_contain_text('검토 보류')
                assert hold['legacy_question_id'] not in data['quality_selection']['recommended_ids']
            ok(f'all {len(revision["holds"])} held originals remain reachable with a visible review notice')
            page.goto(base + 'practice-expansion/?bank=rewrite', wait_until='networkidle')
            expect(page.locator('#collection')).to_have_value('representative-20261028')
            assert diag()['filtered'] == len(new)
            page.set_viewport_size({'width': 320, 'height': 900})
            for q in new:
                # Exercise actual form controls and both grading outcomes for every new item.
                page.locator('#query').fill(q['question_id'])
                page.locator('#catalog button').click()
                assert diag()['active'] == q['question_id']
                assert page.locator('#cases .case').count() == 1
                expect(page.locator('#q-title')).to_have_text('법규 적용 사례')
                wrong = next(c['id'] for c in q['choices'] if c['id'] not in q['correct_choice_ids'])
                page.locator('#choice-' + wrong).check()
                page.locator('#check').click()
                expect(page.locator('#answer-heading')).to_contain_text('불일치')
                assert state()['attempts'][q['question_id']]['correct'] is False
                page.locator('#catalog button').click()
                for key in q['correct_choice_ids']:
                    page.locator('#choice-' + key).check()
                page.locator('#check').click()
                expect(page.locator('#answer-heading')).not_to_contain_text('불일치')
                assert state()['attempts'][q['question_id']]['correct'] is True
                assert page.locator('#rationales .rationale').count() == len(q['choices'])
                expected_refs = sum(len(refs) for refs in q['explanation']['choice_authorities'].values())
                assert page.locator('#rationales a').count() == expected_refs
                assert page.locator('#notes a').count() == len(q['note_evidence'])
                shown = ', '.join(sorted(diag()['displayLabels'][key] for key in q['correct_choice_ids']))
                assert shown in page.locator('#answer-heading').inner_text()
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'), q['question_id']
                exercised_ids.append(q['question_id'])
            ok(f'every new case ({len(new)}) passes wrong/correct grading, shuffled-letter mapping, exact citation links and 320px layout')
            page.screenshot(path=str(args.evidence / 'revision-mobile.png'), full_page=True)
            page.set_viewport_size({'width': 1440, 'height': 1000})
            page.screenshot(path=str(args.evidence / 'revision-desktop.png'), full_page=True)
            with page.expect_download() as download:
                page.locator('#export').click()
            download.value.save_as(str(args.evidence / 'progress.json'))
            backup = json.loads((args.evidence / 'progress.json').read_text())
            assert backup['attempts'][legacy_id] == legacy_attempt
            assert set(revision['new_ids']) <= set(backup['attempts'])
            page.locator('#import-file').set_input_files(str(args.evidence / 'progress.json'))
            expect(page.locator('#storage-msg')).to_contain_text('기록을 가져왔습니다')
            assert state()['attempts'][legacy_id] == legacy_attempt
            ok('backup/import keeps all old and revised attempts under their own IDs')
            page.goto(base + 'practice-expansion/', wait_until='networkidle')
            page.locator('#practice').click()
            assert len(diag()['sessionIds']) == 20
            assert set(diag()['sessionIds']) <= set(data['quality_selection']['recommended_ids'])
            page.locator('#end-session').click()
            page.locator('#timed').click()
            assert len(diag()['sessionIds']) == len(set(diag()['sessionFamilies'])) == 120
            assert set(diag()['sessionIds']) <= set(data['quality_selection']['recommended_ids'])
            page.locator('#end-session').click()
            ok('standard20 and timed120 draw only the revised default pool, without duplicate families')
            page.locator('#query').fill('no-matching-filter-for-chaos')
            page.evaluate('''ids=>{window.MPJEQuality.chaos=(pool,n)=>{const old=pool.find(q=>q.question_id===ids.old),fresh=pool.find(q=>q.question_id===ids.fresh);if(!old||!fresh)throw Error('archive missing from Chaos pool');return Array.from({length:n},(_,i)=>i%2?fresh:old);};}''', {'old': legacy_id, 'fresh': first['question_id']})
            page.locator('#chaos').click()
            assert diag()['sessionIds'] == [legacy_id, first['question_id']] * 5
            assert len(set(diag()['sessionFamilies'])) == 1
            page.locator('#end-session').click()
            ok('unrestricted Chaos10 still accepts old/new versions of one family and repeated exact IDs despite empty filters')
            page.goto(base + 'practice-expansion/?bank=quality', wait_until='load')
            assert diag()['filtered'] == 96
            page.goto(base + 'practice-expansion/?bank=original', wait_until='load')
            assert diag()['filtered'] == 1024
            page.goto(base + 'practice-expansion/?bank=plus', wait_until='load')
            assert diag()['filtered'] == 1152
            ok('all three prior collection entry points retain their original counts')
            assert not errors, errors
            ok('no uncaught JavaScript errors')
            browser.close()
            status = 'passed'
    except BaseException as exc:
        failure = {'type': type(exc).__name__, 'message': str(exc)}
        raise
    finally:
        if server:
            server.shutdown()
        report = dict(mode='PRODUCTION_HTTP_REAL_ORIGIN' if args.base_url else 'LOCAL_HTTP_REAL_ORIGIN',
            status=status, failure=failure, completed_checks=len(checks), checks=checks,
            new_cases_planned=len(new), new_cases_exercised=len(exercised_ids),
            exercised_question_ids=exercised_ids, page_errors=errors,
            independent_legal_review=False, physical_device_test=False)
        (args.evidence / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
