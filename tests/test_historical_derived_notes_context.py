"""Historical card previews must not re-enter an approved current held source."""
import copy
import json
from pathlib import Path

import pytest

import note_review_queue as q
import notes_body_reassessment as body
import notes_revision as revision

ROOT=Path(__file__).resolve().parents[1]
RECORD='reports/full-corpus-review/body-corrections/w3-a-3-v1/record.json'


def actual_inputs():
    record=json.loads((ROOT/RECORD).read_bytes())
    def retained(binding):
        raw=(ROOT/binding['path']).read_bytes()
        assert q.raw_sha(raw)==binding['raw_sha256']
        return json.loads(raw)
    notes=retained(record['archived_parent']['notes'])
    candidate=retained(record['replacement']['revision'])['units'][0]
    preview=retained(record['derived_preview'])
    assert notes['revision_provenance']['id']=='2026-11-03.emergency-kit.1'
    assert json.loads((ROOT/'notes/study/guide.json').read_bytes())['lessons']
    assert json.loads((ROOT/'notes/refresh/guide.json').read_bytes())['cards']
    return record,notes,candidate,preview


def test_actual_archived_authored_cards_match_original_preview_without_current_held_reentry(monkeypatch):
    record,notes,candidate,preview=actual_inputs();original=copy.deepcopy(notes)
    def reentry(*a,**k):raise AssertionError('HELD_SOURCE_CURRENT_LOAD_REENTRY')
    monkeypatch.setattr(revision,'load_notes',reentry)
    actual=body.derived_inputs(ROOT,notes,'w3-a-3',candidate)
    assert actual==preview['items']
    assert {x['collection']for x in actual}=={'study.lessons','refresh.chapter-overview'}
    assert notes==original


@pytest.mark.parametrize('kind,path',[('study','notes/study/guide.json'),('refresh','notes/refresh/guide.json')])
def test_explicit_historical_context_is_exactly_equivalent_to_pre_activation_cards(monkeypatch,kind,path):
    _,notes,_,_=actual_inputs();data=json.loads((ROOT/path).read_bytes())
    monkeypatch.setattr(revision,'load_notes',lambda root:copy.deepcopy(notes))
    previous=revision.apply_study_revision(copy.deepcopy(data),kind,ROOT)
    def reentry(*a,**k):raise AssertionError('HELD_SOURCE_CURRENT_LOAD_REENTRY')
    monkeypatch.setattr(revision,'load_notes',reentry)
    historical=revision.apply_study_revision(copy.deepcopy(data),kind,ROOT,notes_context=notes)
    assert historical==previous
    assert historical['notes_revision']==notes['revision_provenance']
    historical['notes_revision']['id']='mutated-output-only'
    assert notes['revision_provenance']['id']=='2026-11-03.emergency-kit.1'


@pytest.mark.parametrize('kind,field',[('study','lessons'),('refresh','cards')])
def test_default_live_builder_still_runs_current_load_notes_guard(monkeypatch,kind,field):
    monkeypatch.setattr(revision,'revisions',lambda root:[])
    def current_guard(*a,**k):raise ValueError('CURRENT_HELD_SOURCE_MUST_VALIDATE')
    monkeypatch.setattr(revision,'load_notes',current_guard)
    with pytest.raises(ValueError,match='CURRENT_HELD_SOURCE_MUST_VALIDATE'):
        revision.apply_study_revision({field:[]},kind,ROOT)


@pytest.mark.parametrize('context',[{}, {'revision_provenance':{}}, {'revision_provenance':None}])
def test_missing_historical_provenance_never_falls_back_to_current_load(monkeypatch,context):
    def reentry(*a,**k):raise AssertionError('UNEXPECTED_LIVE_FALLBACK')
    monkeypatch.setattr(revision,'load_notes',reentry)
    with pytest.raises(ValueError,match='retained revision provenance'):
        revision.apply_study_revision({'lessons':[]},'study',ROOT,notes_context=context)


def test_minimal_fixture_without_authored_cards_needs_no_invented_provenance(tmp_path,monkeypatch):
    notes={'chapters':[{'units':[{'id':'fixture','body':'Old fixture body'}]}]}
    def reentry(*a,**k):raise AssertionError('UNEXPECTED_LIVE_FALLBACK')
    monkeypatch.setattr(revision,'load_notes',reentry)
    assert body.derived_inputs(tmp_path,notes,'fixture',{'body':'New fixture body'})==[]
