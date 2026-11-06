"""Public draft practice has its own grading and backup boundaries."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def test_public_draft_javascript_contracts():
    result = subprocess.run(['node', '--test', 'tests/test_draft_practice.cjs'], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_public_draft_content_and_source_boundary():
    raw = (ROOT / 'site/draft-practice/questions.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '32f8505a2bfc7ca70e2124427cdfbd5263cdfa581efb72708e7f93665f0ddba5'
    text = raw.decode()
    assert not re.search(r'IMG_\d|/workspace/|drive\.google\.com|docs\.google\.com|MA-PRIVATE|source_version|evidence_file|actual_author_session', text)
    data = json.loads(text)
    assert len(data['questions']) == 33
    assert all(re.search(r'[가-힣]', q['core_ko']) and all(re.search(r'[가-힣]', v) for v in q['analysis_ko'].values()) for q in data['questions'])
    assert all(not re.search(r'[가-힣]', q['stem']) and all(not re.search(r'[가-힣]', c['text']) for c in q['choices']) for q in data['questions'])


def test_public_draft_navigation_and_no_acknowledgement_gate():
    html = (ROOT / 'site/draft-practice/index.html').read_text()
    main = (ROOT / 'site/index.html').read_text()
    topics = (ROOT / 'site/verified-law/index.html').read_text()
    assert 'href="draft-practice/"' in main and 'href="../draft-practice/"' in topics
    assert 'id="ack"' not in html and 'type="checkbox"' not in html
    assert 'questions.json' in html and 'HOLD 1개' in html
    assert 'mpje.draft33.practice.v1' in (ROOT / 'site/draft-practice/app.js').read_text()
