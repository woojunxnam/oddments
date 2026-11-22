#!/usr/bin/env python3
"""Exercise real saved exams across the explicit Batch 3 archive boundary."""
from __future__ import annotations

import argparse
import csv
import io
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright

KEYS = {'c': 'mpje-side-notes-ch30-form-c-mock120-v1',
        'd': 'mpje-side-notes-ch30-form-d-mock120-v1',
        'mixes': 'mpje-side-notes-ch30-mixed-mock120-v1'}
GLOBALS = {'c': 'MPJE_CH30_FORM_C_MOCK', 'd': 'MPJE_CH30_FORM_D_MOCK',
           'mixes': 'MPJE_CH30_MIXED_MOCK_FORMS'}
OLD = {'c': '74d451e6', 'd': '234f9a2a', 'mixes': '48ec9bb4'}
EXCLUDED = {'D016', 'D067'}


def verify(base_url: str) -> dict:
    url = urljoin(base_url.rstrip('/') + '/', 'mpje-side-notes/exam-simulation-30/')
    checks = []
    errors = []
    with sync_playwright() as playwright:
        executable = None if Path(playwright.chromium.executable_path).exists() else shutil.which("chromium")
        browser = playwright.chromium.launch(headless=True, executable_path=executable)
        ctx = browser.new_context(viewport={'width': 390, 'height': 850}, accept_downloads=True)
        page = ctx.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('dialog', lambda dialog: dialog.accept())

        def load(kind):
            page.goto(url + f'mock-120-{kind}.html', wait_until='domcontentloaded')
            page.locator('#mock-dashboard').wait_for(state='attached')
            return page.evaluate('''name => {
                const m=window[name], r=window.MPJE_CH30_BANK_REVISIONS;
                const all=[...(window.MPJE_CH30_QUESTIONS||[]),...(window.MPJE_CH30_FORM_C_QUESTIONS||[]),
                  ...(window.MPJE_CH30_FORM_D_QUESTIONS||[])];
                return {manifest:m,registry:r,questions:all};
            }''', GLOBALS[kind])

        def fixture(data, kind, form, signature=None, active=False, at=None):
            signature = signature or OLD[kind]
            ids = data['manifest']['forms'][form]
            current = {q['id']: q for q in data['questions']}
            target = data['registry']['targets'][data['manifest']['schema']]
            overrides = target.get('snapshotsBySignature', {}).get(signature, {})
            original = dict(current)
            for qid in target['archivedQuestionIds']:
                original[qid] = overrides.get(qid, data['registry']['snapshots'][qid])
            now = datetime.now(timezone.utc).isoformat()
            index = ids.index(at) if active and at else 0 if active else 120
            answered = ids[:index] if active else ids
            session = {'form': form, 'bankSignature': signature, 'version': 1,
                       'attemptId': f'archive-{kind}-{form}-{signature}',
                       'status': 'active' if active else 'completed', 'startedAt': now,
                       'deadlineAt': int(datetime.now(timezone.utc).timestamp()*1000)+3600000,
                       'index': index, 'draft': {},
                       'submitted': {i: original[i]['correct'][:] for i in answered},
                       'exposureAtStart': {i: False for i in ids}, 'syncedIds': [],
                       'completedAt': None if active else now,
                       'finishReason': None if active else 'submitted'}
            state = {'version': 1, 'current': {i: None for i in data['manifest']['forms']},
                     'history': [], 'activeForm': form if active else None, 'visibleForm': form}
            state['current'][form] = session
            return state, original

        def seed(kind, state):
            page.evaluate('([k,v])=>localStorage.setItem(k,JSON.stringify(v))', [KEYS[kind], state])
            page.reload(wait_until='domcontentloaded')

        def stored(kind):
            return page.evaluate('(k)=>JSON.parse(localStorage.getItem(k))', KEYS[kind])

        def export_json():
            with page.expect_download() as download:
                page.locator('#mock-download').click()
            return json.loads(Path(download.value.path()).read_text())

        def pick(data, form, qid):
            index = data['manifest']['forms'][form].index(qid)
            page.locator('#mock-review-picker').select_option(str(index))

        # Previously completed D: use its exact original questions; retain original score and answers.
        d = load('d')
        assert d['registry'], 'Revision archive must exist before running this regression.'
        state, original = fixture(d, 'd', 'D')
        unknown = dict(state['current']['D'], attemptId='unknown-old', bankSignature='unknown-before-batch3')
        state['history'] = [unknown]
        seed('d', state)
        assert page.locator('#mock-error').is_hidden()
        assert '120/120' in page.locator('#mock-score').inner_text()
        assert all(i in page.locator('#mock-result-note').inner_text() for i in EXCLUDED)
        assert 'score not recomputed' in page.locator('#mock-history').inner_text()
        pick(d, 'D', 'D067')
        assert page.locator('#mock-review .exam-stem').inner_text() == original['D067']['stem']
        assert page.locator('#mock-review .mock-current-stem').inner_text() != original['D067']['stem']
        assert 'excluded from readiness' in page.locator('.mock-version-notice').inner_text()
        assert original['D067']['choices'][2]['why'] not in page.locator('.mock-explanations').inner_text()
        result = export_json()
        assert result['bankSignature'] == result['session']['bankSignature'] == OLD['d']
        assert result['stats']['correct'] == 120
        assert set(result['revisionReview']['excludedQuestionIds']) == EXCLUDED
        assert result['session'] == state['current']['D']
        assert stored('d') == state, 'Viewing and exporting must not rewrite saved results.'
        page.locator('#review-hub-filter').select_option('corrections')
        page.locator('#review-hub-search').fill('D067')
        assert page.locator('#review-hub-list button').count() == 1
        with page.expect_download() as download:
            page.locator('#review-hub-export').click()
        rows = list(csv.DictReader(io.StringIO(Path(download.value.path()).read_text(encoding='utf-8-sig'))))
        assert {r['Question ID'] for r in rows} == EXCLUDED
        assert all(r['Original bank signature'] == OLD['d'] and r['Excluded from readiness'] == 'Yes' for r in rows)
        assert next(r for r in rows if r['Question ID']=='D067')['Original question'] == original['D067']['stem']
        checks.append('Old completed D: original raw120/120, original stems and answers, explicit exclusions, JSON/CSV identity')

        # Retake begins on current version, archives the old session byte-for-byte, and allows its later review.
        page.locator('#mock-retake').click()
        after = stored('d')
        assert after['history'][-1] == state['current']['D']
        assert after['current']['D']['bankSignature'] == d['manifest']['bankSignature']
        page.locator('#mock-finish-early').click()
        assert export_json()['revisionReview']['excludedQuestionIds'] == []
        page.locator('#mock-history button').click()
        assert export_json()['session'] == state['current']['D']
        assert '120/120' in page.locator('#mock-score').inner_text()
        assert page.locator('#mock-retake').is_disabled()
        page.locator('#mock-latest-attempt').click()
        assert '0/120' in page.locator('#mock-score').inner_text()
        checks.append('Retake and historical review/export preserve old session; fresh attempt uses current bank')

        # Resume original active D at the corrected inventory question without silently swapping the question.
        state, original = fixture(d, 'd', 'D', active=True, at='D067')
        state['current']['D']['draft']['D067'] = ['B']
        seed('d', state)
        assert page.locator('#mock-question .exam-stem').inner_text() == original['D067']['stem']
        assert page.locator('#mock-question input[value="B"]').is_checked()
        assert page.locator('#mock-completed').is_hidden()
        assert stored('d')['current']['D'] == state['current']['D']
        page.locator('#mock-question input[value="C"]').check()
        page.locator('#mock-next').click()
        active = stored('d')['current']['D']
        assert active['bankSignature'] == OLD['d']
        assert active['submitted']['D067'] == ['C']
        assert active['index'] == state['current']['D']['index']+1
        page.locator('#mock-finish-early').click()
        assert export_json()['stats']['correct'] == active['index']
        checks.append('Old active D resumes original stem and draft, retains signature, and grades original submitted answers')

        # C has a source/metadata correction only. No question is excluded or regraded.
        c = load('c')
        state, original = fixture(c, 'c', 'C')
        seed('c', state)
        pick(c, 'C', 'E30-342')
        assert page.locator('#mock-review .exam-stem').inner_text() == original['E30-342']['stem']
        assert 'Source/explanation updated; original score unchanged' in page.locator('.mock-version-notice').inner_text()
        assert page.locator('#mock-review .exam-reference a').get_attribute('href') == next(q['url'] for q in c['questions'] if q['id']=='E30-342')
        assert 'CURRENT_USP797_NORMATIVE_CHAPTER_UNAVAILABLE_HOLD' not in page.locator('#mock-review').inner_text()
        result = export_json()
        assert result['stats']['correct'] == 120 and result['revisionReview']['excludedQuestionIds'] == []
        assert result['bankSignature'] == OLD['c'] and stored('c') == state
        checks.append('Old C metadata-only result remains120/120 with original question and current source explanation')

        # Every old mixed revision is admitted only explicitly; affected forms get only their own exclusions.
        mixes = load('mixes')
        forms = mixes['manifest']['forms']
        affected = ['CD1'] + [f for f in forms if f.startswith('ALL') and 'D067' in forms[f]]
        for signature in (OLD['mixes'], '77edd81d'):
            for form in affected:
                state, original = fixture(mixes, 'mixes', form, signature=signature)
                seed('mixes', state)
                assert page.locator('#mock-error').is_hidden(), page.locator('#mock-error').inner_text()
                result = export_json()
                expected = EXCLUDED.intersection(forms[form])
                assert result['stats']['correct'] == 120
                assert set(result['revisionReview']['excludedQuestionIds']) == expected
                assert result['bankSignature'] == signature and result['session'] == state['current'][form]
                pick(mixes, form, 'D067')
                assert page.locator('#mock-review .exam-stem').inner_text() == original['D067']['stem']
                assert page.locator('#mock-review .mock-current-stem').count() == 1
                assert stored('mixes') == state
        unaffected = next(f for f in forms if not EXCLUDED.intersection(forms[f]))
        state, _ = fixture(mixes, 'mixes', unaffected)
        seed('mixes', state)
        assert export_json()['revisionReview']['excludedQuestionIds'] == []
        assert '120/120' in page.locator('#mock-score').inner_text()
        checks.append('CD1 and ALL mix retain both known old signatures; exclusions are form-local; unaffected mix scores unchanged')

        # Prior E30-190 typo does not return in learning review under the older mixed signature.
        form = next(f for f in forms if 'E30-190' in forms[f])
        state, original = fixture(mixes, 'mixes', form, signature='77edd81d')
        seed('mixes', state)
        pick(mixes, form, 'E30-190')
        assert 'Table 12' in original['E30-190']['choices'][2]['why']
        current_explanation = page.locator('#mock-review .mock-explanations p').nth(2).inner_text()
        assert 'Table 13' in current_explanation and 'Table 12' not in current_explanation
        checks.append('77edd81d archived E30-190 scores original key but learning review shows corrected Table13')

        # Completing an old active mixed session never syncs corrected question attempts into current practice.
        form = 'CD1'
        state, original = fixture(mixes, 'mixes', form, active=True,
                                  at=forms[form][forms[form].index('D067')+1])
        state['current'][form]['submitted'] = {i: original[i]['correct'] for i in EXCLUDED.intersection(forms[form])}
        unchanged = next(i for i in forms[form] if i not in EXCLUDED)
        state['current'][form]['submitted'][unchanged] = original[unchanged]['correct']
        seed('mixes', state)
        page.locator('#mock-finish-early').click()
        session = stored('mixes')['current'][form]
        assert EXCLUDED.isdisjoint(session['syncedIds'])
        assert unchanged in session['syncedIds']
        checks.append('Old active mixed completion excludes corrected IDs from progress synchronization')

        # Unknown current/completed/active records remain untouched and cannot use current keys.
        d = load('d')
        for active in (False, True):
            state, _ = fixture(d, 'd', 'D', active=active)
            state['current']['D']['bankSignature'] = 'unknown-bank-revision'
            seed('d', state)
            assert page.locator('#mock-error').is_visible()
            assert page.locator('#mock-open-d').is_disabled()
            assert page.locator('#mock-completed').is_hidden()
            page.evaluate("document.getElementById('mock-next').click()")
            assert stored('d') == state
        guard = page.evaluate('''() => {
          const m=window.MPJE_CH30_FORM_D_MOCK, r=window.MPJE_CH30_BANK_REVISIONS,
            q=new Map(window.MPJE_CH30_FORM_D_QUESTIONS.map(x=>[x.id,x]));
          const old={form:'D',bankSignature:'234f9a2a'};
          const future=window.MPJE_CH30_VERSION_HISTORY.create({...m,bankSignature:'future'},q).canUse(old);
          const id=r.targets[m.schema].archivedQuestionIds[0], saved=r.snapshots[id];
          delete r.snapshots[id];
          const incomplete=window.MPJE_CH30_VERSION_HISTORY.create(m,q).canUse(old);
          r.snapshots[id]=saved;
          return {future,incomplete};
        }''')
        assert guard == {'future': False, 'incomplete': False}
        assert not errors, errors
        checks.append('Unknown revisions, future-manifest inheritance, and incomplete archives fail closed without storage reset')
        ctx.close()
        browser.close()
    return {'passed': True, 'checks': checks, 'browser_errors': errors}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-url', default='http://127.0.0.1:8765/')
    parser.add_argument('--output')
    args = parser.parse_args()
    result = verify(args.base_url)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(text+'\n')
    print(text)
