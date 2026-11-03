"""Only current independently supported note/card content may activate."""
import hashlib
import copy
import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from notes_revision import load_notes, validate_final_note_review, REVISION_H

A = 'revisions/notes/counsel-shield-activation.json'


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode()


def fixture_review(tmp_path):
    activation = json.loads((ROOT/A).read_bytes())
    report = json.loads((ROOT/activation['review_path']).read_bytes())
    paths = [A, activation['review_path'], activation['census_path'], report['prior_review']['path']]
    paths += [source['evidence_path'] for source in report['sources']]
    for path in paths:
        dest = tmp_path/path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT/path, dest)
    raw = (ROOT/REVISION_H).read_bytes()
    return activation, report, raw, json.loads(raw)


def test_revision_preserves_all_other_units_and_verifies_two_current_bodies():
    old = {u['id']:u for c in load_notes(revision_id='2026-10-30.cdtm13-vax04.1')['chapters'] for u in c['units']}
    new = {u['id']:u for c in load_notes(revision_id='2026-11-03.counsel-shield-final.1')['chapters'] for u in c['units']}
    assert set(new) == set(old)
    assert {uid for uid in old if old[uid] != new[uid]} == {'w3-b-1','w3-d-23'}
    assert '9.18(10)' in new['w3-b-1']['body'] and '2026-02' in new['w3-b-1']['body']
    assert all(new[uid]['independent_content_review']['decision'] == 'KEEP' for uid in ['w3-b-1','w3-d-23'])


def test_ce_revision_changes_only_current_disclosure_unit_and_retains_prior_reviews():
    old = {u['id']:u for c in load_notes(revision_id='2026-11-03.counsel-shield-final.1')['chapters'] for u in c['units']}
    new = {u['id']:u for c in load_notes()['chapters'] for u in c['units']}
    assert {uid for uid in old if old[uid] != new[uid]} == {'w1-a-7'}
    assert 'Mandatory Disclosure Form' in new['w1-a-7']['body']
    assert {uid for uid,u in new.items() if 'independent_content_review' in u} == {'w1-a-7','w3-b-1','w3-d-23'}


def test_source_hold_annotation_follows_exact_body_and_never_certifies_unreviewed_units():
    from build_ultimate_notes import census_annotations
    data = {'chapters':[{'units':[{'id':'known','body':'current'}, {'id':'unreviewed','body':'unreviewed'}]}]}
    rows = [dict(unit_id=uid,actual_effective_body_sha256=hashlib.sha256(body.encode()).hexdigest(),
                 atomic_source_blocked_count=count,atomic_census_source='reports/census.json')
            for uid,body,count in [('known','current',2),('unreviewed','unreviewed',0)]]
    raw = ''.join(json.dumps(row)+'\n' for row in rows).encode()
    annotations = census_annotations(data,raw)
    assert set(annotations) == {'known'}
    assert annotations['known']['count'] == 2
    data['chapters'][0]['units'][0]['body'] = 'changed legal claim'
    with pytest.raises(ValueError,match='Stale note census'):
        census_annotations(data,raw)


def test_keep_summary_cannot_override_failed_atomic_claim(tmp_path):
    activation, report, raw, revision = fixture_review(tmp_path)
    validate_final_note_review(tmp_path, raw, revision)
    report['claims'][0]['verdict'] = 'HOLD'
    changed = encoded(report)
    (tmp_path/activation['review_path']).write_bytes(changed)
    activation['review_sha256'] = hashlib.sha256(changed).hexdigest()
    (tmp_path/A).write_bytes(encoded(activation))
    with pytest.raises(ValueError, match='claim lacks current independent evidence'):
        validate_final_note_review(tmp_path, raw, revision)


def test_duplicate_unit_keep_cannot_hide_a_failed_result(tmp_path):
    activation, report, raw, revision = fixture_review(tmp_path)
    failed = copy.deepcopy(report['units'][0])
    failed['verdict'] = 'HOLD'
    failed['fully_supported_in_current_scope'] = False
    report['units'].insert(0,failed)
    changed = encoded(report)
    (tmp_path/activation['review_path']).write_bytes(changed)
    activation['review_sha256'] = hashlib.sha256(changed).hexdigest()
    (tmp_path/A).write_bytes(encoded(activation))
    with pytest.raises(ValueError,match='review unit scope changed'):
        validate_final_note_review(tmp_path, raw, revision)


def test_rebinding_summary_cannot_cover_unreviewed_card_edit(tmp_path):
    activation, report, raw, revision = fixture_review(tmp_path)
    revision['refresh_cards']['RF-034']['plain'] += ' Unreviewed permission.'
    raw = encoded(revision)
    activation['revision_sha256'] = report['candidate_sha256'] = hashlib.sha256(raw).hexdigest()
    report_raw = encoded(report)
    activation['review_sha256'] = hashlib.sha256(report_raw).hexdigest()
    (tmp_path/activation['review_path']).write_bytes(report_raw)
    (tmp_path/A).write_bytes(encoded(activation))
    with pytest.raises(ValueError, match='card evidence stale'):
        validate_final_note_review(tmp_path, raw, revision)
