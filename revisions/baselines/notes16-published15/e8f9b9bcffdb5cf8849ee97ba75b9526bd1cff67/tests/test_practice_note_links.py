"""Cross-navigation follows explicit evidence and leaves review status/history alone."""
import copy
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from practice_note_links import build_note_practice_index
from publish_practice import build_payload, render
from build_exam_study import build_payload as build_study


def test_note_counts_distinguish_versions_and_do_not_infer_links_from_topic():
    notes = {'chapters': [{'id': 'chapter', 'units': [{'id': 'note-a', 'title': 'A'}, {'id': 'note-b', 'title': 'B'}]}]}
    questions = [
        {'question_id': 'old', 'family_id': 'shared', 'topic': 'B', 'note_evidence': [{'unit_id': 'note-a'}, {'unit_id': 'note-a'}]},
        {'question_id': 'new', 'family_id': 'shared', 'topic': 'B', 'note_evidence': [{'unit_id': 'note-a'}]},
    ]
    before = copy.deepcopy(questions)
    index = build_note_practice_index(questions, ['new'], notes)
    assert index['note-a']['total'] == 2
    assert index['note-a']['recommended'] == 1
    assert index['note-a']['families'] == index['note-a']['recommended_families'] == 1
    assert index['note-b']['total'] == index['note-b']['recommended'] == 0
    assert questions == before
    with pytest.raises(ValueError, match='Duplicate question ID'):
        build_note_practice_index(questions + [questions[0]], ['new'], notes)
    with pytest.raises(ValueError, match='Unknown recommendation'):
        build_note_practice_index(questions, ['unknown'], notes)
    questions[0]['note_evidence'] = [{'unit_id': 'unknown'}]
    with pytest.raises(ValueError, match='Unknown note unit'):
        build_note_practice_index(questions, ['new'], notes)


def test_practice_and_full_notes_publish_the_same_exact_evidence_index():
    practice, study = build_payload(), build_study()
    assert practice['note_practice_index'] == study['note_practice_index']
    recommended = set(practice['quality_selection']['recommended_ids'])
    for uid, entry in practice['note_practice_index'].items():
        linked = [q for q in practice['questions'] if uid in {e['unit_id'] for e in q['note_evidence']}]
        assert entry['total'] == len(linked)
        assert entry['recommended'] == sum(q['question_id'] in recommended for q in linked)
        assert entry['families'] == len({q['family_id'] for q in linked})
        assert entry['practice_url'] == '../practice-expansion/?note=' + uid
        assert entry['note_url'].endswith('/' + uid)


def test_notes_links_are_safe_and_zero_or_unavailable_data_stays_readable():
    js = (ROOT / 'site/notes/notes.js').read_text()
    function = js[js.index('  function unitPractice('):js.index('  function renderUnit(')]
    harness = r'''
const assert=require('assert/strict');
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const window={};
assert.equal(unitPractice({id:'note-a'}),'');
window.MPJE_EXAM_STUDY={note_practice_index:{'note-a':{total:3,recommended:1,practice_url:'../practice-expansion/?note=note-a'}}};
let html=unitPractice({id:'note-a',title:'A <test>'});
assert.match(html,/대표·개정 1문항 풀기/);assert.match(html,/note=note-a&amp;review=wrong/);
assert.match(html,/A &lt;test&gt;/);assert.doesNotMatch(html,/scope=all/);
window.MPJE_EXAM_STUDY.note_practice_index['note-a'].recommended=0;
html=unitPractice({id:'note-a',title:'A'});assert.match(html,/scope=all/);assert.match(html,/검토 보류/);
window.MPJE_EXAM_STUDY.note_practice_index['note-a'].total=0;
assert.equal(unitPractice({id:'note-a'}),'');
'''
    result = subprocess.run(['node', '-e', function + harness], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_published_javascript_is_syntactically_valid(tmp_path):
    html = render(build_payload())
    # The payload and application are the last inline script in the reader.
    scripts = __import__('re').findall(r'<script>(.*?)</script>', html, __import__('re').S)
    assert scripts
    script = tmp_path / 'practice.js'
    script.write_text('\n'.join(scripts))
    result = subprocess.run(['node', '--check', str(script)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_note_context_explains_outside_deep_links_and_preserves_live_session_navigation():
    html = render(build_payload())
    function = next(line for line in html.splitlines() if line.startswith('function updateNoteContext('))
    harness = r'''
const assert=require('assert/strict');
const controls={};const $=id=>controls[id]??(controls[id]={});
const D={note_practice_index:{'note-a':{title:'A',recommended:1,total:4,note_url:'../notes/#chapter/test/note-a'}}};
let selectedNoteId='note-a',session=null,active={note_evidence:[{unit_id:'note-a'}]};
updateNoteContext();assert.equal($('#note-context').hidden,false);assert.equal($('#note-return').target,'_self');
assert.doesNotMatch($('#note-context-help').textContent,/연결 문항이 아닙니다/);
active={note_evidence:[{unit_id:'other'}]};updateNoteContext();
assert.match($('#note-context-help').textContent,/연결 문항이 아닙니다/);
session={timed:true};updateNoteContext();
assert.equal($('#note-return').target,'_blank');assert.equal($('#note-clear').disabled,true);
assert.equal($('#note-wrong').disabled,true);assert.match($('#note-context-help').textContent,/시계는 계속/);
selectedNoteId='unknown';session=null;updateNoteContext();
assert.equal($('#note-return').hidden,true);assert.equal($('#note-wrong').disabled,true);
selectedNoteId='';updateNoteContext();assert.equal($('#note-context').hidden,true);
'''
    result = subprocess.run(['node', '-e', function + harness], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
