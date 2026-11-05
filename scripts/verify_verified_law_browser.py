#!/usr/bin/env python3
"""Exercise the existing canonical viewer's curated entry points over real HTTP.

Uses a separate synthetic browser context. This is software QA, not a legal audit.
"""
from __future__ import annotations

import argparse
from functools import partial
import hashlib
import http.server
import json
import os
from pathlib import Path
import subprocess
import threading
from datetime import datetime, timezone
from urllib.parse import urlencode

from playwright.sync_api import sync_playwright, expect
from qa_common import question_audit_hash

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=Path, default=ROOT / 'site')
    parser.add_argument('--base-url')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    if out.exists():
        raise ValueError('Use a new evidence directory; previous results are retained')
    if out == ROOT or ROOT in out.parents:
        raise ValueError('Write browser evidence outside the repository')
    out.mkdir(parents=True)
    payload = json.loads((args.site / 'generated/questions.json').read_text())
    manifest = json.loads((args.site / 'verified-law/sets.json').read_text())
    overlay = json.loads((args.site / 'verified-law/delivery-holds.json').read_text())
    held_ids = {hold['question_id'] for hold in overlay['holds']}
    by_id = {question['question_id']: question for question in payload['questions']}
    first_set = manifest['sets'][0]
    first_id = first_set['questions'][0]['question_id']
    first_ids = {reference['question_id'] for reference in first_set['questions']}
    outside_id = next(question['question_id'] for question in payload['questions'] if question['question_id'] not in first_ids and question['question_id'] not in held_ids)
    historical = json.loads((ROOT / 'data/questions/ma-q-0012.json').read_text())
    historical['question_content_hash'] = question_audit_hash(historical)
    server = None
    if args.base_url:
        base = args.base_url.rstrip('/') + '/'
    else:
        class Quiet(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *args):
                pass
        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(args.site)))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        base = f'http://127.0.0.1:{server.server_port}/'
    checks, errors = [], []
    status, failure = 'FAIL', None

    def passed(name):
        checks.append(name)
        print('PASS: ' + name, flush=True)

    def answer_correctly(target):
        item = target.evaluate('({type:state.question.question_type,correct:state.question.correct_choice_ids})')
        for choice in item['correct']:
            if item['type'] == 'ORDERED_RESPONSE':
                target.locator(f'.choice[data-choice-id="{choice}"] button').click()
            else:
                target.locator(f'#choice-form input[value="{choice}"]').check()
        target.locator('#check-answer').click()
        expect(target.locator('#result')).to_have_text('Correct.')

    try:
        with sync_playwright() as playwright:
            launch = {'headless': True}
            if os.environ.get('CHROMIUM_PATH'):
                launch['executable_path'] = os.environ['CHROMIUM_PATH']
            browser = playwright.chromium.launch(**launch)
            context = browser.new_context(viewport={'width': 1440, 'height': 1000}, accept_downloads=True)
            page = context.new_page()
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(base, wait_until='load')
            page.wait_for_function('state.payload && state.guide && state.delivery.ready')
            stored = page.evaluate('''async question => {
                const record = MpjeSessions.buildCompletedSession({
                    sessionId: 'curated-retained-history', examType: 'TOPIC_QUIZ',
                    sessionSeed: 'curated-history-seed', startedAt: '2026-11-03T00:00:00Z',
                    completedAt: '2026-11-03T00:01:00Z', queue: [question],
                    responses: [{answered: true, selected: ['B'], correct: false}]
                });
                await MpjeStorage.saveSession(record);
                const progress = MpjeStorage.defaultProgress();
                progress.wrong = [question.question_id]; progress.completed = [question.question_id];
                progress.bookmarks = [question.question_id]; MpjeStorage.saveProgress(progress);
                localStorage.setItem('curated-unrelated-canary', 'unchanged');
                return {record, progressRaw: localStorage.getItem('ma-mpje-progress-v2')};
            }''', historical)
            held_history = page.evaluate('''async question => {
                const record = MpjeSessions.buildCompletedSession({
                    sessionId: 'curated-held-history', examType: 'TOPIC_QUIZ',
                    sessionSeed: 'pre-hold-history-seed', startedAt: '2026-11-03T00:02:00Z',
                    completedAt: '2026-11-03T00:03:00Z', queue: [question],
                    responses: [{answered:true, selected:['B'], correct:false}]
                });
                await MpjeStorage.saveSession(record);
                const progress = MpjeStorage.loadProgress();
                for (const field of ['wrong','bookmarks','completed']) progress[field].push(question.question_id);
                MpjeStorage.saveProgress(progress);
                return {record, progressRaw:localStorage.getItem('ma-mpje-progress-v2')};
            }''', by_id[overlay['holds'][0]['question_id']])
            stored['records'] = [held_history['record'], stored['record']]
            stored['progressRaw'] = held_history['progressRaw']

            page.goto(base + 'verified-law/', wait_until='load')
            expect(page.locator('.collection-card')).to_have_count(len(manifest['sets']))
            expect(page.locator('#collection-status')).to_contain_text('기존 승인 문항')
            expect(page.locator('body')).to_contain_text('해설은 영어')
            page.set_viewport_size({'width': 320, 'height': 900})
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
            page.screenshot(path=str(out / 'collection-mobile.png'), full_page=True)
            passed('topic entry lists only the current approved collection, with a usable 320px layout')

            for selected in manifest['sets']:
                for reference in selected['questions']:
                    uid = reference['question_id']
                    page.goto(base + '?' + urlencode({'set': selected['id'], 'question': uid, 'seed': 'curated-browser'}), wait_until='load')
                    expect(page.locator('#question-stem')).to_have_text(by_id[uid]['stem'])
                    actual = page.evaluate('({id:state.question.question_id, hash:state.question.question_content_hash, queue:state.queue.map(q=>q.question_id)})')
                    assert actual == {'id': uid, 'hash': reference['question_content_hash'], 'queue': [uid]}
            passed('every listed question opens the exact existing ID, current content hash and unchanged stem')

            page.goto(base + '?' + urlencode({'question': first_id, 'seed': 'curated-answer'}), wait_until='load')
            expect(page.locator('#question-stem')).to_have_text(by_id[first_id]['stem'])
            assert page.evaluate('localStorage.getItem("ma-mpje-progress-v2")') == stored['progressRaw']
            assert page.evaluate('async () => await MpjeStorage.getSession("curated-retained-history")') == stored['record']
            answer_correctly(page)
            expect(page.locator('#choice-analysis dd')).to_have_count(len(by_id[first_id]['choices']))
            after = page.evaluate('async () => await MpjeStorage.exportData()')
            assert after['exam_history'] == stored['records']
            assert historical['question_id'] in after['progress']['bookmarks']
            assert historical['question_id'] in after['progress']['wrong']
            assert historical['question_id'] in after['progress']['completed']
            assert page.evaluate('localStorage.getItem("curated-unrelated-canary")') == 'unchanged'
            passed('direct-ID grading reuses shuffled choices and preserves previous session answers, hashes and bookmarks')

            with page.expect_download() as download:
                page.locator('#export-study-data').click()
            export_path = download.value.path()
            exported = json.loads(Path(export_path).read_text())
            assert exported['exam_history'] == stored['records']
            await_import = page.evaluate('async bundle => await MpjeStorage.importData(bundle)', exported)
            assert await_import['imported_sessions'] == len(stored['records'])
            assert page.evaluate('async () => await MpjeStorage.getSession("curated-retained-history")') == stored['record']
            page.locator('#history-button').click()
            page.locator('[data-history-id="curated-retained-history"]').click()
            expect(page.locator('#history-detail')).to_contain_text(historical['question_content_hash'])
            passed('the existing backup/import and history viewer retain old records byte-equivalent')

            page.goto(base + '?' + urlencode({'set': first_set['id']}), wait_until='load')
            page.wait_for_function('state.curated.ready && state.question')
            expected_ids = [item['question_id'] for item in first_set['questions']]
            assert page.evaluate('state.queue.map(q=>q.question_id)') == expected_ids
            page.locator('[data-mode="random"]').click()
            assert set(page.evaluate('state.queue.map(q=>q.question_id)')) <= set(expected_ids)
            page.locator('[data-mode="quick20"]').click()
            quotas = page.evaluate('MpjeSessions.QUICK_20_QUOTAS')
            enough = all(sum(str(by_id[uid]['area']) == str(area) for uid in expected_ids) >= count for area, count in quotas.items())
            if enough:
                expect(page.locator('#question-position')).to_have_text('1 / 20')
                assert set(page.evaluate('state.queue.map(q=>q.question_id)')) <= set(expected_ids)
            else:
                expect(page.locator('#empty-state')).to_contain_text('Unable to start this session')
                expect(page.locator('#question-panel')).to_be_hidden()
            passed('all existing modes keep the selected intersection; insufficient Quick20 pools never backfill')

            invalid = [
                {'question': 'MA-Q-0012'}, {'question': 'MA-Q-0028'}, {'question': 'MA-Q-9999'},
                {'question': 'bad'}, {'question': ''}, {'set': 'unknown-set'},
                {'set': first_set['id'], 'question': outside_id},
            ]
            for parameters in invalid:
                page.goto(base + '?' + urlencode(parameters), wait_until='load')
                expect(page.locator('#curated-title')).to_have_text('선택한 학습 범위를 열 수 없습니다')
                expect(page.locator('#question-panel')).to_be_hidden()
                page.locator('[data-mode="study"]').click()
                expect(page.locator('#question-panel')).to_be_hidden()
                assert page.evaluate('state.queue.length') == 0
            passed('unknown, malformed, quarantined and out-of-set links fail closed without a default question')

            reviews = {review['id']: review for review in overlay['reviews']}
            progress_before_holds = page.evaluate('localStorage.getItem("ma-mpje-progress-v2")')
            for hold in overlay['holds']:
                page.goto(base + '?' + urlencode({'question': hold['question_id']}), wait_until='load')
                expect(page.locator('#curated-description')).to_contain_text(hold['reason'])
                expect(page.locator('#question-panel')).to_be_hidden()
                expect(page.locator('#curated-review-link')).to_have_attribute('href', reviews[hold['review_id']]['url'])
                page.locator('[data-mode="study"]').click()
                expect(page.locator('#question-panel')).to_be_hidden()
                assert page.evaluate('state.queue.length') == 0
                refused = page.evaluate('''id => {
                    state.question = state.payload.questions.find(question => question.question_id === id);
                    state.selected = new Set(state.question.correct_choice_ids); state.answered = false;
                    checkAnswer();
                    return {answered:state.answered, question:state.question, count:state.payload.questions.length};
                }''', hold['question_id'])
                assert refused == {'answered': False, 'question': None, 'count': len(payload['questions'])}
                assert page.evaluate('localStorage.getItem("ma-mpje-progress-v2")') == progress_before_holds
            assert page.evaluate('async () => await MpjeStorage.getSession("curated-held-history")') == held_history['record']
            passed('every current delivery hold refuses direct entry and grading while original payload and old held-item history remain intact')

            page.goto(base, wait_until='load')
            page.wait_for_function('state.payload && state.guide && state.delivery.ready')
            eligible = page.evaluate('filteredQuestions().map(question => question.question_id)')
            assert len(eligible) == len(payload['questions']) - len(held_ids)
            assert not held_ids.intersection(eligible)
            expect(page.locator('#delivery-notice')).to_contain_text(f"{len(held_ids)}문항")
            for mode in ['study', 'random', 'mock', 'quick20', 'wrong', 'bookmarked']:
                page.locator(f'[data-mode="{mode}"]').click()
                assert not held_ids.intersection(page.evaluate('state.queue.map(question => question.question_id)'))
            page.evaluate('''id => startMode('browse',[state.payload.questions.find(question=>question.question_id===id)])''', overlay['holds'][0]['question_id'])
            expect(page.locator('#question-panel')).to_be_hidden()
            assert page.evaluate('state.queue.length') == 0
            passed('default, filtered, mock, Quick20, review and override pools exclude delivery-held hashes without altering canonical data')

            stale_overlay = json.loads(json.dumps(overlay))
            stale_overlay['holds'][0]['question_content_hash'] = '0' * 64
            def stale_holds_response(route):
                route.fulfill(status=200, content_type='application/json', body=json.dumps(stale_overlay))
            context.route('**/verified-law/delivery-holds.json', stale_holds_response)
            for suffix in ['', '?' + urlencode({'question': first_id})]:
                page.goto(base + suffix, wait_until='load')
                expect(page.locator('#curated-description')).to_contain_text('보류된 문항이 변경')
                page.locator('[data-mode="study"]').click()
                expect(page.locator('#question-panel')).to_be_hidden()
                assert page.evaluate('state.delivery.ready === false && state.queue.length === 0')
            context.unroute('**/verified-law/delivery-holds.json', stale_holds_response)
            passed('a stale delivery hold blocks default and direct learning pending review rather than auto-releasing or carrying its old verdict')

            stale = json.loads(json.dumps(manifest))
            stale['sets'][0]['questions'][0]['question_content_hash'] = '0' * 64
            def stale_response(route):
                route.fulfill(status=200, content_type='application/json', body=json.dumps(stale))
            context.route('**/verified-law/sets.json', stale_response)
            page.goto(base + '?' + urlencode({'set': first_set['id']}), wait_until='load')
            expect(page.locator('#curated-description')).to_contain_text('문항이 갱신')
            expect(page.locator('#question-panel')).to_be_hidden()
            assert page.evaluate('state.queue.length') == 0
            context.unroute('**/verified-law/sets.json', stale_response)
            passed('a changed manifest content hash blocks the selected scope')

            changed = json.loads(json.dumps(payload))
            next(q for q in changed['questions'] if q['question_id'] == first_id)['question_content_hash'] = 'f' * 64
            def changed_payload(route):
                route.fulfill(status=200, content_type='application/json', body=json.dumps(changed))
            context.route('**/generated/questions.json', changed_payload)
            page.goto(base + '?' + urlencode({'set': first_set['id']}), wait_until='load')
            expect(page.locator('#curated-description')).to_contain_text('문항이 갱신')
            expect(page.locator('#question-panel')).to_be_hidden()
            context.unroute('**/generated/questions.json', changed_payload)
            passed('a changed payload content hash cannot inherit the old collection binding')

            reordered = json.loads(json.dumps(manifest))
            reordered['sets'][0]['questions'].reverse()
            def reordered_manifest(route):
                route.fulfill(status=200, content_type='application/json', body=json.dumps(reordered))
            context.route('**/verified-law/sets.json', reordered_manifest)
            page.goto(base + '?' + urlencode({'set': first_set['id']}), wait_until='load')
            page.wait_for_function('state.curated.ready && state.question')
            assert page.evaluate('state.queue.map(q=>q.question_id)') == list(reversed(expected_ids))
            context.unroute('**/verified-law/sets.json', reordered_manifest)
            passed('a valid curriculum selection preserves its declared study order')

            page.goto(base + 'verified-law/', wait_until='load')
            expect(page.locator('.collection-card')).to_have_count(len(manifest['sets']))
            note = first_set['notes'][0]
            href = f'../notes/#chapter/{note["chapter_id"]}/{note["unit_id"]}'
            page.locator(f'a[href="{href}"]').first.click()
            expect(page.locator('#' + note['unit_id'])).to_be_visible()
            passed('collection notes open the existing detailed unit without replacing its review notices')

            denied = browser.new_context(viewport={'width': 320, 'height': 900})
            denied.add_init_script("Object.defineProperty(window,'localStorage',{configurable:true,get(){throw new DOMException('Blocked','SecurityError')}});Object.defineProperty(window,'indexedDB',{configurable:true,get(){throw new DOMException('Blocked','SecurityError')}})")
            blocked = denied.new_page(); blocked.on('pageerror', lambda error: errors.append(str(error)))
            blocked.goto(base + '?' + urlencode({'question': first_id}), wait_until='load')
            expect(blocked.locator('#question-stem')).to_have_text(by_id[first_id]['stem'])
            expect(blocked.locator('#storage-status')).to_contain_text('저장할 수 없습니다')
            answer_correctly(blocked)
            assert blocked.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
            blocked.screenshot(path=str(out / 'direct-question-blocked-storage-mobile.png'), full_page=True)
            passed('denied localStorage and IndexedDB retain in-session direct-ID learning with an explicit notice')
            denied.close()

            page.goto(base, wait_until='load')
            page.wait_for_function('state.payload && state.guide && state.delivery.ready')
            expect(page.locator('#curated-context')).to_be_hidden()
            assert page.evaluate('state.payload.questions.length') == len(payload['questions'])
            assert page.evaluate('async () => await MpjeStorage.getSession("curated-retained-history")') == stored['record']
            passed('ordinary root navigation keeps the full approved bank and all previous history')
            assert not errors, errors
            browser.close()
            status = 'PASS'
    except Exception as error:
        failure = repr(error)
        raise
    finally:
        report = {
            'status': status, 'observed_at_utc': datetime.now(timezone.utc).isoformat(),
            'mode': 'REAL_HTTP_EXISTING_CANONICAL_VIEWER', 'base_url': base,
            'source_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
            'source_worktree_dirty': bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True).strip()),
            'checks_passed': len(checks), 'checks': checks, 'javascript_errors': errors, 'failure': failure,
            'sets': len(manifest['sets']), 'existing_unique_questions': len({q['question_id'] for item in manifest['sets'] for q in item['questions']}),
            'delivery_held_count': len(overlay['holds']), 'canonical_status_or_payload_changed': False,
            'new_question_or_independent_legal_audit_credit': 0, 'real_user_profile_used': False,
            'manifest_sha256': hashlib.sha256((args.site / 'verified-law/sets.json').read_bytes()).hexdigest(),
            'canonical_payload_sha256': hashlib.sha256((args.site / 'generated/questions.json').read_bytes()).hexdigest(),
            'tested_file_sha256': {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in [ROOT / 'site/app.js', ROOT / 'site/index.html',
                    *sorted((ROOT / 'site/verified-law').glob('*')),
                    ROOT / 'scripts/verify_verified_law_browser.py', ROOT / 'tests/test_verified_law_collections.cjs'] if path.is_file()},
        }
        (out / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        if server:
            server.shutdown()
    print(json.dumps({'status': status, 'checks_passed': len(checks), 'evidence': str(out)}))


if __name__ == '__main__':
    main()
