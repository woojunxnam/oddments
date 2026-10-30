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

            # A collection's stored total and the usable scope intersection are different counts.
            expect(page.get_by_label('문항 포함 범위', exact=True)).to_have_attribute('id', 'scope')
            expect(page.get_by_label('문항 모음 (선택)', exact=True)).to_have_attribute('id', 'collection')
            expect(page.locator('#scope')).to_have_attribute('aria-describedby', 'scope-help')
            expect(page.locator('#collection')).to_have_attribute('aria-describedby', 'collection-help')
            expect(page.locator('#filter-summary')).to_have_attribute('role', 'status')
            expect(page.locator('#filter-summary')).to_have_attribute('aria-live', 'polite')
            recommended_ids = set(data['quality_selection']['recommended_ids'])
            for scope in ['recommended', 'all']:
                page.locator('#scope').select_option(scope)
                for collection in ['', *[group['id'] for group in data['collections']]]:
                    page.locator('#collection').select_option(collection)
                    stored = [q for q in data['questions'] if not collection or q['collection_id'] == collection]
                    expected = {q['question_id'] for q in stored if scope == 'all' or q['question_id'] in recommended_ids}
                    observed = diag()
                    assert set(observed['filteredIds']) == expected, (scope, collection)
                    assert observed['filterSummary']['collectionTotal'] == len(stored)
                    assert observed['filterSummary']['scopeCount'] == len(expected)
                    assert observed['filterSummary']['matchedCount'] == len(expected)
                    expect(page.locator('#filter-summary')).to_have_text(f'현재 조건에 맞는 {len(expected):,}문항')
                    expect(page.locator('#collection option:checked')).to_contain_text(f'총 {len(stored):,}개')
                    expect(page.locator('#filter-breakdown')).to_contain_text(f'전체 {len(stored):,}개')
            ok('both inclusion scopes intersect every collection; stored totals and actual result counts are separately labelled')

            page.locator('#scope').select_option('recommended')
            legacy_collection = by_id[legacy_id]['collection_id']
            page.locator('#collection').select_option(legacy_collection)
            page.locator('#saved').select_option('bookmarks')
            assert set(diag()['filteredIds']) == {qid for qid in seed['bookmarks'] if by_id[qid]['collection_id'] == legacy_collection}
            expect(page.locator('#filter-exception')).to_be_visible()
            expect(page.locator('#filter-exception')).to_contain_text('북마크 복습')
            page.locator('#saved').select_option('wrong')
            assert diag()['filteredIds'] == [legacy_id]
            expect(page.locator('#filter-exception')).to_contain_text('오답 복습')
            page.locator('#saved').select_option('')
            page.locator('#query').fill(legacy_id)
            assert diag()['filteredIds'] == [legacy_id]
            expect(page.locator('#filter-exception')).to_contain_text('ID 검색')
            page.locator('#collection').select_option('representative-20261028')
            assert diag()['filteredIds'] == []  # ID lookup bypasses scope, never the selected collection.
            expect(page.locator('#filter-summary')).to_have_text('현재 조건에 맞는 0문항')
            expect(page.locator('#practice')).to_be_disabled()
            expect(page.locator('#timed')).to_be_disabled()
            expect(page.locator('#chaos')).to_be_enabled()
            expect(page.locator('#filter-session-help')).to_contain_text('조건에 맞는 문항이 없습니다')
            ok('bookmark, wrong-answer and ID lookup preserve archived access while retaining collection filters and explaining the exception')

            page.locator('#query').fill('')
            page.locator('#collection').select_option('')
            page.locator('#area').select_option(str(first['area']))
            page.locator('#qtype').select_option(first['question_type'])
            expected = {q['question_id'] for q in data['questions'] if q['question_id'] in recommended_ids
                and q['area'] == first['area'] and q['question_type'] == first['question_type']}
            assert set(diag()['filteredIds']) == expected
            assert diag()['filterSummary']['scopeCount'] == len(recommended_ids)
            assert diag()['filterSummary']['matchedCount'] == len(expected)
            expect(page.locator('#filter-exception')).to_be_hidden()
            page.set_viewport_size({'width': 320, 'height': 900})
            page.locator('#filter-examples summary').click()
            expect(page.locator('#filter-example-text')).to_contain_text('다른 필터를 사용하지 않을 때')
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
            page.screenshot(path=str(args.evidence / 'filter-help-mobile.png'), full_page=True)
            page.set_viewport_size({'width': 1440, 'height': 1000})
            ok('area/type filters update the actual count; accessible help and expanded examples fit a 320px viewport')

            # Detailed note -> exact evidence filter -> wrong-answer review -> same note.
            shared_units = {e['unit_id'] for e in first['note_evidence']} & {e['unit_id'] for e in by_id[legacy_id]['note_evidence']}
            assert shared_units
            unit_id = sorted(shared_units)[0]
            note = data['note_practice_index'][unit_id]
            notes_path = 'notes/#chapter/' + note['chapter_id'] + '/' + unit_id
            quiz_before = state()
            page.goto(base + notes_path, wait_until='networkidle')
            expect(page.locator('[data-unit-practice="' + unit_id + '"]')).to_be_visible()
            note_unit = page.locator('#' + unit_id)
            note_unit.locator('[data-save]').click()
            note_unit.locator('[data-read]').click()
            page.locator('[data-unit-practice="' + unit_id + '"]').click()
            expect(page.locator('#note-context')).to_be_visible()
            assert diag()['noteUnit'] == unit_id
            linked = {q['question_id'] for q in data['questions'] if unit_id in {e['unit_id'] for e in q['note_evidence']}}
            assert set(diag()['filteredIds']) == linked & recommended_ids
            expect(page.locator('#note-context-counts')).to_contain_text(f'대표·개정 {note["recommended"]:,}문항')
            for button in ['practice', 'timed']:
                page.locator('#' + button).click()
                assert set(diag()['sessionIds']) <= linked & recommended_ids
                expect(page.locator('#note-clear')).to_be_disabled()
                expect(page.locator('#note-wrong')).to_be_disabled()
                expect(page.locator('#note-return')).to_have_attribute('target', '_blank')
                page.locator('#end-session').click()
            page.locator('#note-wrong').click()
            assert diag()['filteredIds'] == [legacy_id]
            expect(page.locator('#filter-exception')).to_contain_text('오답 복습')
            assert state() == quiz_before
            page.set_viewport_size({'width': 320, 'height': 900})
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
            page.screenshot(path=str(args.evidence / 'note-practice-mobile.png'), full_page=True)
            page.locator('#note-return').click()
            note_unit = page.locator('#' + unit_id)
            expect(note_unit.locator('[data-save]')).to_have_attribute('aria-pressed', 'true')
            expect(note_unit.locator('[data-read]')).to_have_attribute('aria-pressed', 'true')
            assert state() == quiz_before
            page.locator('[data-unit-wrong="' + unit_id + '"]').click()
            expect(page.locator('#note-context')).to_be_visible()
            page.wait_for_function('typeof window.MPJE_DIAGNOSTICS === "function"')
            assert diag()['filteredIds'] == [legacy_id]
            page.locator('#note-clear').click()
            assert diag()['noteUnit'] is None
            expect(page.locator('#note-context')).to_be_hidden()
            assert 'note=' not in page.url
            page.goto(base + 'practice-expansion/?note=unknown-note', wait_until='networkidle')
            assert diag()['filteredIds'] == []
            expect(page.locator('#question')).to_be_hidden()
            expect(page.locator('#note-context-title')).to_contain_text('찾을 수 없습니다')
            outside = next(q for q in new if q['question_id'] not in linked)
            page.goto(base + 'practice-expansion/?bank=rewrite&note=' + unit_id + '#' + outside['question_id'], wait_until='networkidle')
            assert diag()['active'] == outside['question_id']
            assert set(diag()['filteredIds']) == linked & set(revision['new_ids'])
            expect(page.locator('#note-context-help')).to_contain_text('현재 열린 문항은 이 절의 연결 문항이 아닙니다')
            page.locator('#query').fill('no-matching-filter-for-note')
            page.locator('#next').click()
            expect(page.locator('#question')).to_be_hidden()
            expect(page.locator('#locked')).to_contain_text('현재 조건에 맞는 문항이 없습니다')
            page.goto(base + notes_path, wait_until='networkidle')
            page.locator('[data-unit-practice="' + unit_id + '"]').click()
            expect(page.locator('#note-context')).to_be_visible()
            page.go_back(wait_until='networkidle')
            expect(page.locator('#' + unit_id)).to_be_visible()
            page.go_forward(wait_until='networkidle')
            assert diag()['noteUnit'] == unit_id
            assert set(diag()['filteredIds']) == linked & recommended_ids
            page.set_viewport_size({'width': 1440, 'height': 1000})
            ok('notes/practice exact-unit navigation, focused study/exam/wrong-answer filters, 320px layout and both separate progress stores survive round trips; unknown units fail closed')

            page.goto(base + 'practice-expansion/?bank=rewrite', wait_until='networkidle')
            for button, maximum in [('practice', 20), ('timed', 120)]:
                ceiling = min(maximum, len({q['family_id'] for q in new}))
                assert diag()['filterSummary']['standardCeiling' if button == 'practice' else 'timedCeiling'] == ceiling
                page.locator('#' + button).click()
                observed = diag()
                assert 0 < len(observed['sessionIds']) <= ceiling
                assert set(observed['sessionIds']) <= set(revision['new_ids'])
                assert len(observed['sessionFamilies']) == len(set(observed['sessionFamilies']))
                expect(page.locator('#scope')).to_be_disabled()
                expect(page.locator('#collection')).to_be_disabled()
                page.locator('#end-session').click()
                expect(page.locator('#scope')).to_be_enabled()
                expect(page.locator('#collection')).to_be_enabled()
            ok('20/120 modes use the chosen collection intersection and retain diversity and filter locking')

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
            for notice in revision.get('archive_review_notices', []):
                for qid in notice['question_ids']:
                    page.goto(base + 'practice-expansion/#' + qid, wait_until='load')
                    assert diag()['archiveReviewWarning'] is True
                    expect(page.locator('.archive-review-warning')).to_contain_text(notice['reason'])
                    assert qid not in data['quality_selection']['recommended_ids']
            if revision.get('archive_review_notices'):
                ok('identified archive defects show explicit warnings alongside any replacement links without rewriting old answer keys or attempts')
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
            denied = browser.new_context(viewport={'width': 390, 'height': 844})
            denied.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Unavailable','SecurityError')}})")
            denied_page = denied.new_page()
            denied_page.on('pageerror', lambda e: errors.append(str(e)))
            denied_page.goto(base + notes_path, wait_until='networkidle')
            expect(denied_page.locator('#storage-notice')).to_be_visible()
            denied_page.locator('[data-unit-practice="' + unit_id + '"]').click()
            expect(denied_page.locator('#note-context')).to_be_visible()
            denied_page.wait_for_function('typeof window.MPJE_DIAGNOSTICS === "function"')
            assert denied_page.evaluate('MPJE_DIAGNOSTICS().noteUnit') == unit_id
            assert set(denied_page.evaluate('MPJE_DIAGNOSTICS().filteredIds')) == linked & recommended_ids
            expect(denied_page.locator('#storage-msg')).to_contain_text('임시 상태')
            denied_page.locator('#note-wrong').click()
            expect(denied_page.locator('#question')).to_be_hidden()
            expect(denied_page.locator('#locked')).to_contain_text('현재 조건에 맞는 문항이 없습니다')
            denied.close()
            ok('notes/practice cross-navigation stays usable with denied storage and an empty wrong-answer list')
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
