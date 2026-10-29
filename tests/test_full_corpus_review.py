"""Audit coverage and preservation tests; no legal audit is manufactured here."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from build_full_corpus_review import build, validate_review
from notes_revision import load_notes, REVISION
from verify_representative_protected import verify


def test_every_id_is_inventoried_without_inheriting_family_passes():
    outputs = build()
    for path, text in outputs.items():
        assert path.read_text() == text
    rows = [json.loads(s) for s in outputs[ROOT/'reports/full-corpus-review/question-ledger.jsonl'].splitlines()]
    assert len(rows) == len({r['question_id'] for r in rows}) == 2331
    assert sum(r['baseline_member'] for r in rows) == 2328
    assert sum(r['checked_at'] is not None for r in rows) == 19
    assert sum(r['legal_review_status']=='AUTHOR_SOURCE_CHECKED_NOT_INDEPENDENT' for r in rows) == 3
    assert sum(r['legal_review_status']=='HOLD_SOURCE_RELATIONSHIP' for r in rows) == 4
    assert all(r['checked_at'] is None for r in rows if r['question_id'].startswith('MA-REV-'))
    assert not any(r['legal_review_status']=='RELEASED' for r in rows)


def test_stale_review_or_missing_choice_cannot_count_as_reviewed():
    q=json.loads((ROOT/'practice_expansion/2026-10-23/candidates/questions.json').read_text())['questions'][120]
    r=json.loads((ROOT/'reports/full-corpus-review/unit3a-author-review.json').read_text())['records'][0]
    validate_review(q,r)
    q=copy.deepcopy(q); q['stem']+=' New condition.'
    with pytest.raises(ValueError,match='Stale review'): validate_review(q,r)
    r=copy.deepcopy(r); r['choice_by_choice_findings'].pop('A')
    q=json.loads((ROOT/'practice_expansion/2026-10-23/candidates/questions.json').read_text())['questions'][120]
    with pytest.raises(ValueError,match='Missing choice'): validate_review(q,r)


def test_one_unit_revised_and_cross_surface_warning_is_not_a_review_certificate():
    baseline=json.loads((ROOT/'notes/guide.json').read_text())
    effective=load_notes(ROOT)
    old={u['id']:u for c in baseline['chapters'] for u in c['units']}
    new={u['id']:u for c in effective['chapters'] for u in c['units']}
    assert old.keys()==new.keys()
    assert [uid for uid in old if old[uid]!=new[uid]] == ['w1-b-8']
    assert 'OPEN' in new['w1-b-8']['body']
    assert '과거 읽음' in new['w1-b-8']['editor_note']
    assert hashlib.sha256((ROOT/'notes/guide.json').read_bytes()).hexdigest() == '004c2f9f309db00705a3b35ddd2fa1fb360235f4fd0d364a9ccdf8b3c43aa384'
    from build_exam_study import build_payload
    study=build_payload()
    assert 'OPEN' in next(l for l in study['lessons'] if l['id']=='LAW-012')['core']
    from build_refresh import build_payload as refresh
    assert 'OPEN' in next(c for c in refresh()['cards'] if c['id']=='RF-049')['watch']
    assert new['w1-b-8']['body_sha256'] == next(l for l in study['lessons'] if l['id']=='LAW-012')['source_hashes']['w1-b-8']


@pytest.fixture
def protected_copy(tmp_path):
    manifest=json.loads((ROOT/'reports/representative-rewrite/protected-baseline.json').read_text())
    for row in manifest['files']:
        dest=tmp_path/row['path']; dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/row['path'],dest)
    shutil.copytree(ROOT/'revisions',tmp_path/'revisions')
    verify(manifest,tmp_path)
    return tmp_path,manifest


@pytest.mark.parametrize('relative',[
    'notes/guide.json', 'docs/RELEASE_POLICY.md',
    'revisions/baselines/complete-notes-2026-10-23.1.md',
    'site/notes/complete-notes.md', REVISION,
])
def test_protection_rejects_original_or_unapproved_hash_change(protected_copy,relative):
    root,manifest=protected_copy
    with (root/relative).open('ab') as stream: stream.write(b' changed')
    with pytest.raises(ValueError): verify(manifest,root)


def test_migration_cannot_expand_allowlist(protected_copy):
    root,manifest=protected_copy
    path=root/'revisions/notes/protected-migration.json'
    migration=json.loads(path.read_text())
    migration['files'].append(dict(path='notes/guide.json'))
    path.write_text(json.dumps(migration))
    with pytest.raises(ValueError,match='expands protected scope'): verify(manifest,root)
