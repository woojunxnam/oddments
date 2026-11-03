"""Edited note bodies cannot inherit stale atomic-census credit."""
import copy
import sys
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from build_full_corpus_review import compose_note_censuses
from notes_revision import load_notes

G = '2026-10-30.cdtm13-vax04.1'
FIRST = 'reports/full-corpus-review/pub05-14-note-census.json'


def inputs():
    units = {u['id']: u for c in load_notes(revision_id=G)['chapters'] for u in c['units']}
    ids = {json.loads(line)['question_id']: None for line in
           (ROOT/'reports/full-corpus-review/question-ledger.jsonl').read_text().splitlines()}
    return units, ids


def test_historical_census_cannot_follow_edited_current_body():
    units, ids = inputs()
    spec = [dict(path=FIRST, notes_revision=G)]
    selected, claims = compose_note_censuses(spec, units, ids)
    assert len(selected) == 12 and len(claims) == 170
    edited = copy.deepcopy(units)
    edited['w3-b-1']['body'] += '\nNew legal claim without a fresh census.'
    with pytest.raises(ValueError, match='Current note requires a new census'):
        compose_note_censuses(spec, edited, ids)


def test_overlap_requires_explicit_exact_parent_and_does_not_double_credit():
    units, ids = inputs()
    spec = dict(path=FIRST, notes_revision=G)
    with pytest.raises(ValueError, match='Undeclared census supersedence'):
        compose_note_censuses([spec, spec], units, ids)
    second = dict(spec, supersedes={unit['unit_id']: 'wrong-parent.json' for unit in
                  json.loads((ROOT/FIRST).read_text())['units']})
    with pytest.raises(ValueError, match='Wrong census supersedence parent'):
        compose_note_censuses([spec, second], units, ids)
