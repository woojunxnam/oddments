#!/usr/bin/env python3
"""Check withdrawn content and preserved local user data over real HTTP."""
import argparse
import functools
import http.server
import json
import os
from pathlib import Path
import subprocess
import threading

from playwright.sync_api import sync_playwright, expect
from canonical_q0012_withdrawal import QUESTION, QID, AUDIT_HASH, validate

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=Path, default=ROOT/'public-site')
    parser.add_argument('--base-url')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    before = json.loads(validate(ROOT)[QUESTION])
    before['question_content_hash'] = AUDIT_HASH
    server = None
    if args.base_url:
        base = args.base_url.rstrip('/')+'/'
    else:
        class Quiet(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *args): pass
        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0),
            functools.partial(Quiet, directory=str(args.site)))
        threading.Thread(target=server.serve_forever, daemon=True).start()
        base = f'http://127.0.0.1:{server.server_port}/'
    errors = []
    try:
        with sync_playwright() as p:
            executable = os.environ.get('CHROMIUM_PATH')
            browser = p.chromium.launch(headless=True,
                **({'executable_path': executable} if executable else {}))
            page = browser.new_page()
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(base, wait_until='load')
            page.wait_for_function('state.payload && state.guide')
            stored = page.evaluate('''async question => {
                const record = MpjeSessions.buildCompletedSession({
                    sessionId: 'withdrawal-retained-history', examType: 'TOPIC_QUIZ',
                    sessionSeed: 'withdrawal-browser-check', startedAt: '2026-11-03T00:00:00Z',
                    completedAt: '2026-11-03T00:01:00Z', queue: [question],
                    responses: [{answered: true, selected: ['B'], correct: true}]
                });
                await MpjeStorage.saveSession(record);
                const progress = MpjeStorage.loadProgress();
                for (const field of ['wrong', 'bookmarks', 'completed']) progress[field] = [question.question_id];
                MpjeStorage.saveProgress(progress);
                return record;
            }''', before)
            page.reload(wait_until='load')
            page.wait_for_function('state.payload && state.guide')
            data = page.evaluate('''async () => ({
                count: state.payload.questions.length,
                ids: state.payload.questions.map(q => q.question_id),
                sections: state.guide.sections.map(s => s.section_id),
                reverse: state.guide.question_to_sections,
                exported: await MpjeStorage.exportData()
            })''')
            assert data['count'] == 397 and QID not in data['ids']
            assert len(data['sections']) == 40 and 'SG-CII-LIFECYCLE' not in data['sections']
            assert QID not in data['reverse']
            exported = data['exported']
            assert exported['exam_history'] == [stored]
            assert exported['exam_history'][0]['question_content_hashes'][QID] == AUDIT_HASH
            for field in ('wrong', 'bookmarks', 'completed'):
                assert exported['progress'][field] == [QID]
            page.locator('#history-button').click()
            page.locator('[data-history-id="withdrawal-retained-history"]').click()
            expect(page.locator('#history-detail')).to_contain_text(AUDIT_HASH)
            assert not errors, errors
            page.screenshot(path=str(args.output/'retained-history.png'))
            browser.close()
        report = {'status': 'PASS', 'base_url': base,
            'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
            'question_id': QID, 'current_canonical_questions': 397, 'current_guide_sections': 40,
            'withdrawn_question_excluded': True, 'linked_guide_excluded': True,
            'stored_session_answers_hash_and_score_preserved': True,
            'bookmarks_wrong_and_completed_preserved': True, 'javascript_errors': errors,
            'canonical_audit_credit': 0}
        (args.output/'report.json').write_text(json.dumps(report, indent=2)+'\n')
        print(json.dumps(report))
    finally:
        if server: server.shutdown()


if __name__ == '__main__':
    main()
