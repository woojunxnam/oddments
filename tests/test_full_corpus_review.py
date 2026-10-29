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
    assert len(rows) == len({r['question_id'] for r in rows}) == 2334
    assert sum(r['baseline_member'] for r in rows) == 2328
    assert sum(r['checked_at'] is not None for r in rows) == 41
    assert sum(r['legal_review_status']=='AUTHOR_SOURCE_CHECKED_NOT_INDEPENDENT' for r in rows) == 6
    assert sum(r['legal_review_status']=='HOLD_SOURCE_RELATIONSHIP' for r in rows) == 10
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
    assert [uid for uid in old if old[uid]!=new[uid]] == ['w1-b-8','w1-b-9','w1-b-10']
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


@pytest.mark.parametrize('field', ['unit_content_sha256', 'source_evidence_sha256'])
def test_stale_claim_evidence_is_rejected(field):
    from build_full_corpus_review import validate_claim
    claim=json.loads((ROOT/'reports/full-corpus-review/unit3a-claims.json').read_text())['claims'][0]
    units={u['id']:u for c in load_notes(ROOT)['chapters'] for u in c['units']}
    validate_claim(claim,units,ROOT)
    claim=copy.deepcopy(claim); claim[field]='0'*64
    with pytest.raises(ValueError,match='Stale claim'): validate_claim(claim,units,ROOT)


def test_published_unit3a_revision_snapshot_remains_reproducible():
    from notes_revision import IDS
    old=load_notes(ROOT,revision_id=IDS[0])
    now=load_notes(ROOT)
    assert old['revision_provenance']['id']==IDS[0]
    old_units={u['id']:u for c in old['chapters'] for u in c['units']}
    new_units={u['id']:u for c in now['chapters'] for u in c['units']}
    assert old_units['w1-b-8']==new_units['w1-b-8']
    assert old_units['w1-b-9']!=new_units['w1-b-9']
    assert '정식 인수 계약' in new_units['w1-b-9']['body']
    assert '교육일 당일 이전' in new_units['w1-b-10']['body']


@pytest.mark.parametrize('relative',[
    'revisions/notes/2026-10-29-personnel-supervision-training.json',
    'revisions/baselines/complete-notes-unit3a.md',
])
def test_followup_protection_rejects_source_or_previous_export_changes(protected_copy,relative):
    root,manifest=protected_copy
    with (root/relative).open('ab') as stream: stream.write(b' changed')
    with pytest.raises(ValueError): verify(manifest,root)


def test_visible_quality_status_and_previous59_snapshot_are_current():
    from build_quality_status import output
    path, rendered=output()
    assert path.read_text()==rendered
    assert '2,334' in rendered and '438' in rendered
    snapshot=json.loads((ROOT/'reports/full-corpus-review/unit3b-preservation.json').read_text())
    from build_full_corpus_review import record_hash
    bank=json.loads((ROOT/'practice_expansion/2026-10-28-representative/questions.json').read_text())
    by_id={q['question_id']:q for q in bank['questions']}
    assert len(snapshot['previous_question_record_hashes'])==59
    assert all(record_hash(by_id[qid])==expected for qid,expected in snapshot['previous_question_record_hashes'].items())
    assert snapshot['new_question_ids']==['MA-RW-0065','MA-RW-0067','MA-RW-0068']
