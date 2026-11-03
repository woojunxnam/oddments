"""Emergency boundary fixes activate only with exact body/source/audit evidence."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from notes_revision import PATHS, load_notes, apply_study_revision
from notes_emergency_activation import (
    ACTIVATION, CENSUS, REVIEW, REVISION_M, UNIT_IDS, SOURCE_IDS,
    official_url, validate_emergency_note_review, validate_review_contents,
)
from verify_representative_protected import migrated_baseline_bytes

MIGRATION = 'revisions/notes/protected-migration-emergency-kit.json'


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


@pytest.fixture
def emergency_copy(tmp_path):
    shutil.copytree(ROOT/'revisions', tmp_path/'revisions')
    shutil.copytree(ROOT/'notes', tmp_path/'notes')
    evidence = 'reports/full-corpus-review/evidence/emergency-kit-final-independent-20261103'
    shutil.copytree(ROOT/evidence, tmp_path/evidence)
    paths = {'site/notes/build.json', 'site/notes/complete-notes.md',
             'reports/full-corpus-review/note-wave8-census.json',
             'reports/full-corpus-review/note-wave9-census.json'}
    for activation_path in (ROOT/'revisions/notes').glob('*-activation.json'):
        activation = json.loads(activation_path.read_bytes())
        report = json.loads((ROOT/activation['review_path']).read_bytes())
        paths.update([activation['review_path'], activation['census_path']])
        paths.update(s['evidence_path'] for s in report['sources'])
        if report.get('prior_review'):
            paths.add(report['prior_review']['path'])
    for path in paths:
        destination = tmp_path/path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT/path, destination)
    return tmp_path


def contents(root):
    return [json.loads((root/path).read_bytes()) for path in [REVISION_M, REVIEW, CENSUS]]


def test_emergency_activation_changes_only_two_bodies_adds_exact_sources_and_preserves_other_notes():
    before = load_notes(revision_id='2026-11-03.refill-cancer.1')
    after = load_notes()
    old = {u['id']:u for c in before['chapters'] for u in c['units']}
    new = {u['id']:u for c in after['chapters'] for u in c['units']}
    assert set(old) == set(new)
    assert {uid for uid in old if old[uid] != new[uid]} == UNIT_IDS
    assert set(after['sources']) - set(before['sources']) == SOURCE_IDS
    assert all(after['sources'][sid] == source for sid,source in before['sources'].items())
    assert '≤50 beds' in new['w4-a-19']['body']
    assert '≤10 beds, 11–20 beds, ≥21 beds' in new['w4-a-20']['body']
    assert 'Max number of units per facility' in new['w4-a-20']['body']
    assert all(new[uid]['independent_content_review']['decision'] == 'KEEP' for uid in UNIT_IDS)
    assert '2026-11-03-packaging-pamphlet-final.json' not in repr(PATHS)
    for a,b in zip(before['chapters'],after['chapters']):
        assert {k:v for k,v in a.items() if k != 'units'} == {k:v for k,v in b.items() if k != 'units'}
    assert json.loads((ROOT/REVISION_M).read_bytes())['status'] == 'AUDIT_PENDING_NOT_APPLIED'
    assert json.loads((ROOT/REVISION_M).read_bytes())['activation'] is False


def test_four_related_cards_retain_full_source_records_without_new_patch_credit():
    for kind,path,field,ids in [
        ('study','notes/study/guide.json','lessons',{'LAW-053','LAW-054'}),
        ('refresh','notes/refresh/guide.json','cards',{'RF-054','RF-056'}),
    ]:
        source = json.loads((ROOT/path).read_bytes())
        revised = apply_study_revision(copy.deepcopy(source), kind)
        assert [r for r in source[field] if r['id'] in ids] == [r for r in revised[field] if r['id'] in ids]
    report = json.loads((ROOT/REVIEW).read_bytes())
    assert report['historical_canonical_four_holds_resolved'] == report['question_audit_credit'] == 0
    assert report['derived_patches'] == []


@pytest.mark.parametrize('url',[
    'https://www.mass.gov.evil.invalid/doc/source', 'https://www.mass.gov@evil.invalid/source',
    'http://www.mass.gov/doc/source', 'https://www.mass.gov:444/doc/source',
])
def test_official_hostname_whitelist_rejects_lookalikes_and_credentials(url):
    assert not official_url(url)


@pytest.mark.parametrize('path', [REVISION_M, REVIEW, CENSUS])
def test_rebinding_changed_candidate_or_audit_hashes_does_not_authorize_activation(emergency_copy,path):
    root = emergency_copy
    value = json.loads((root/path).read_bytes())
    value['unreviewed_change'] = True
    (root/path).write_bytes(encoded(value))
    activation = json.loads((root/ACTIVATION).read_bytes())
    field = {REVISION_M:'revision_sha256', REVIEW:'review_sha256', CENSUS:'census_sha256'}[path]
    activation[field] = sha((root/path).read_bytes())
    (root/ACTIVATION).write_bytes(encoded(activation))
    raw = (root/REVISION_M).read_bytes()
    with pytest.raises(ValueError,match='activation binding changed'):
        validate_emergency_note_review(root,raw,json.loads(raw))


def test_duplicate_keep_cannot_hide_a_failed_atomic_claim(emergency_copy):
    revision,review,census = contents(emergency_copy)
    failed = copy.deepcopy(review['claims'][0]); failed['verdict'] = 'HOLD'
    review['claims'].insert(0,failed)
    with pytest.raises(ValueError,match='atomic claim coverage changed'):
        validate_review_contents(emergency_copy,revision,review,census)


def test_keep_summary_cannot_override_failed_body_or_claim(emergency_copy):
    revision,review,census = contents(emergency_copy)
    review['units'][0]['body_read_completely'] = False
    with pytest.raises(ValueError,match='body lacks current independent evidence'):
        validate_review_contents(emergency_copy,revision,review,census)
    revision,review,census = contents(emergency_copy)
    review['claims'][0]['verdict'] = 'HOLD'
    with pytest.raises(ValueError,match='claim lacks current independent evidence'):
        validate_review_contents(emergency_copy,revision,review,census)


def test_unchanged_patch_summary_cannot_cover_unreviewed_card(emergency_copy):
    revision,review,census = contents(emergency_copy)
    revision['study_lessons']['LAW-054'] = {'core':'Unreviewed changed legal rule'}
    with pytest.raises(ValueError,match='requested derived scope changed'):
        validate_review_contents(emergency_copy,revision,review,census)


def test_source_addition_and_visual_table_inspection_are_exact_requirements(emergency_copy):
    revision,review,census = contents(emergency_copy)
    revision['sources']['src-unreviewed'] = {'id':'src-unreviewed','url':'https://www.mass.gov/doc/unreviewed'}
    with pytest.raises(ValueError,match='revised source scope changed'):
        validate_review_contents(emergency_copy,revision,review,census)
    revision,review,census = contents(emergency_copy)
    review['visual_table_review']['hospice']['actually_viewed_by_auditor'] = False
    with pytest.raises(ValueError,match='visual table evidence missing'):
        validate_review_contents(emergency_copy,revision,review,census)


@pytest.mark.parametrize('relative',[
    'reports/full-corpus-review/evidence/emergency-kit-final-independent-20261103/kits-page3.png',
    'reports/full-corpus-review/evidence/emergency-kit-final-independent-20261103/hospice.pdf',
    'reports/full-corpus-review/evidence/emergency-kit-final-independent-20261103/unchanged-derived-cards-and-summaries.json',
    'notes/study/guide.json',
])
def test_live_primary_visual_and_unchanged_card_bytes_are_bound(emergency_copy,relative):
    path = emergency_copy/relative
    path.write_bytes(path.read_bytes()+b' tampered')
    raw = (emergency_copy/REVISION_M).read_bytes()
    with pytest.raises(ValueError,match='evidence changed'):
        validate_emergency_note_review(emergency_copy,raw,json.loads(raw))


def test_semantic_migration_decodes_j_export_and_j_build_context(emergency_copy):
    path = emergency_copy/'site/notes/complete-notes.md'
    original = (ROOT/'revisions/baselines/complete-notes-2026-10-23.1.md').read_bytes()
    assert migrated_baseline_bytes(emergency_copy,'site/notes/complete-notes.md',path.read_bytes()) == original
    (emergency_copy/MIGRATION).unlink()
    # The unchanged 11th migration still rejects M semantics on its own.
    with pytest.raises(ValueError,match='cannot authorize a semantic note edit'):
        migrated_baseline_bytes(emergency_copy,'site/notes/complete-notes.md',path.read_bytes())


@pytest.mark.parametrize('change,expected',[
    ('current_semantic','current semantic build changed'),
    ('scope','expands protected scope'),
    ('historical_build','Historical J census build changed'),
    ('historical_export','Historical J census export changed'),
    ('previous_guard','Previous census annotation migration changed'),
])
def test_semantic_migration_cannot_weaken_old_guards_or_rebind_context(emergency_copy,change,expected):
    root = emergency_copy
    metadata = json.loads((root/MIGRATION).read_bytes())
    if change == 'current_semantic':
        path = root/'site/notes/build.json'; build = json.loads(path.read_bytes())
        build['content_sha256'] = metadata['semantic_notes_sha256'] = '0'*64
        path.write_bytes(encoded(build))
    elif change == 'scope':
        metadata['path'] = 'notes/guide.json'
    elif change == 'historical_build':
        path = root/metadata['baseline_build_copy']; build = json.loads(path.read_bytes())
        build['content_sha256'] = metadata['semantic_notes_sha256']
        path.write_bytes(encoded(build)); metadata['baseline_build_sha256'] = sha(path.read_bytes())
    elif change == 'historical_export':
        path = root/metadata['baseline_copy']; path.write_bytes(path.read_bytes()+b' changed')
        metadata['old_sha256'] = sha(path.read_bytes())
    else:
        path = root/metadata['previous_migration_path']; parent = json.loads(path.read_bytes())
        parent['semantic_notes_sha256'] = metadata['semantic_notes_sha256']
        path.write_bytes(encoded(parent)); metadata['previous_migration_sha256'] = sha(path.read_bytes())
    (root/MIGRATION).write_bytes(encoded(metadata))
    with pytest.raises(ValueError,match=expected):
        migrated_baseline_bytes(root,'site/notes/complete-notes.md',(root/'site/notes/complete-notes.md').read_bytes())
