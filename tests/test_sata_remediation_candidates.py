"""Meaningful boundaries of the draft-to-archive adapter; no legal self-audit."""
import copy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_sata_remediation_candidates as adapter
import build_representative_rewrites as compiler


@pytest.fixture(scope='module')
def compiled():
    return compiler.build()


def test_frozen_allocation_includes_reserved_unpublished_numbers():
    manifest = json.loads((ROOT / adapter.ALLOCATION).read_text())
    assert manifest['base_commit'] == '34e38c7b3d2b87ca5b3d9528dff5eb5121c923e4'
    assert len(manifest['public_question_record_hashes']) == 2346
    assert len(manifest['representative_question_hashes']) == 74
    assert len(manifest['representative_source_hashes']) == 81
    assert len(manifest['reserved_ids']) == 80  # six IDs were reserved but not published
    assert [r['question_id'] for r in manifest['allocations']] == adapter.next_rewrite_ids(manifest['reserved_ids'], 3)
    assert all('/authoring/' in p or 'draft' in p.lower()
               for p in manifest['authoring_and_draft_file_sha256'])
    assert adapter.next_rewrite_ids(['MA-RW-0001', 'MA-RW-0090'], 3) == ['MA-RW-0091', 'MA-RW-0092', 'MA-RW-0093']
    with pytest.raises(ValueError, match='exhausted'):
        adapter.next_rewrite_ids(['MA-RW-9999'], 1)


def test_actual_compiler_preserves_every_old_object_and_reviewed_character(compiled):
    bank = compiled[compiler.BASE / 'questions.json']
    adapter.validate_preservation(bank)
    assert len(bank['questions']) == 77
    assert len(bank['sources']) == 90
    manifest = json.loads((ROOT / adapter.ALLOCATION).read_text())
    for path in adapter.PUBLIC_BANKS[:-1]:
        for q in json.loads((ROOT / path).read_text())['questions']:
            assert adapter.record_sha(q) == manifest['public_question_record_hashes'][q['question_id']]
    for q in bank['questions']:
        assert compiler.content_hash(q) == q['content_sha256']


def test_existing_source_metadata_and_korean_wording_mutations_fail(compiled):
    bank = compiled[compiler.BASE / 'questions.json']
    changed = copy.deepcopy(bank)
    changed['sources'][next(iter(changed['sources']))]['metadata_was_changed'] = True
    with pytest.raises(ValueError, match='Existing source object changed'):
        adapter.validate_preservation(changed)
    changed = copy.deepcopy(bank)
    changed['questions'][-1]['explanation']['learning_boundary'] += ' '
    with pytest.raises(ValueError, match='Reviewed Korean explanation changed'):
        adapter.validate_preservation(changed)
    changed = copy.deepcopy(bank)
    changed['questions'][0]['history_policy'] = 'MIGRATE'
    with pytest.raises(ValueError, match='Existing representative object changed'):
        adapter.validate_preservation(changed)


def test_every_option_retains_exact_G_proof_and_raw_payload_binding(compiled):
    source = adapter.authoring_payload()
    checked = 0
    for a in source['questions']:
        draft = adapter.load_draft(ROOT, dict(draft_key=a['remediation_candidate']['draft_key']))[2]
        assert a['scenario'] + '\n\n' + a['lead_in'] == draft['stem']
        for c in a['choices']:
            proof = next(p for p in draft['option_proofs'] if p['choice_id'] == c['id'])
            for converted, original in zip(c['authority_refs'], proof['authorities'], strict=True):
                expected = {**original, 'source_id': adapter.NAMESPACE + original['source_id']}
                assert converted == expected
                s = source['sources'][converted['source_id']]
                assert converted['raw_sha256'] == s['raw_sha256']
                assert converted['official_url'] == s['official_url']
                assert converted['law_checked_date'] == s['checked_at'] == '2026-11-04'
                assert converted['effective_date_status'] == s['effective_date_status']
            checked += 1
    assert checked == 14
    broken = copy.deepcopy(next(iter(json.loads((ROOT / adapter.REGISTER).read_text())['sources'])))
    broken['http_status'] = 404
    with pytest.raises(ValueError, match='cannot be proof'):
        adapter.validate_retained_source(ROOT, broken)
    broken['http_status'] = 200
    broken['raw_sha256'] = '0' * 64
    with pytest.raises(ValueError, match='payload hash mismatch'):
        adapter.validate_retained_source(ROOT, broken)


def test_original_holds_defaults_and_history_are_not_bypassed(compiled):
    bank = compiled[compiler.BASE / 'questions.json']
    selection = compiled[compiler.BASE / 'selection.json']
    manifest = json.loads((ROOT / adapter.ALLOCATION).read_text())
    old = manifest['preserved_selection']
    assert selection['recommended_ids'] == old['recommended_ids']
    assert selection['holds'] == old['holds']
    assert selection['replacements'] == old['replacements']
    assert selection['safety_holds'] == old['safety_holds']
    candidate_ids = {r['question_id'] for r in manifest['allocations']}
    assert not candidate_ids & set(selection['recommended_ids'])
    assert {r['replacement_question_id'] for r in selection['archive_only_replacements']} == candidate_ids
    original = json.loads((ROOT / compiler.ORIGINAL_SELECTION).read_text())
    by_id = {q['question_id']: q for p in adapter.PUBLIC_BANKS[:-1]
             for q in json.loads((ROOT / p).read_text())['questions']}
    by_id.update({q['question_id']: q for q in bank['questions']})
    compiler.validate_nonlegacy_selection(selection, original, by_id, ROOT)
    invalid = copy.deepcopy(selection)
    invalid['recommended_ids'].append(next(iter(candidate_ids)))
    with pytest.raises(ValueError, match='Default IDs differ'):
        compiler.validate_nonlegacy_selection(invalid, original, by_id, ROOT)


def test_inventory_binding_is_not_new_author_or_independent_credit(compiled):
    q = compiled[compiler.BASE / 'questions.json']['questions'][-1]
    row = {}
    adapter.bind_candidate_inventory_row(row, q)
    assert row['legal_review_status'] == 'DRAFT_SOURCE_REVIEW_BOUND_NOT_CURRENT_ID_AUDIT'
    assert row['checked_at_scope'] == 'ORIGINAL_G_DRAFT_SOURCE_REVIEW_DATE_ONLY'
    assert row['author_review_increment'] == row['independent_review_credit'] == row['canonical_release_credit'] == 0
    assert q['publication_status'] == 'PUBLISHED_PRACTICE'
    assert q['verification_status'] == 'NOT_INDEPENDENTLY_REVIEWED'
    assert q['remediation_candidate']['release_eligible'] is False
    changed = copy.deepcopy(q)
    changed['correct_choice_ids'] = ['A']
    with pytest.raises(ValueError, match='Stale remediation inventory binding'):
        adapter.bind_candidate_inventory_row({}, changed)


def test_actual_publication_preserves_all_2346_delivered_objects_and_archive_UI(compiled):
    from publish_practice import build_payload, render
    data = build_payload()
    frozen = json.loads((ROOT / adapter.OUT / 'published-record-baseline.json').read_text())
    by_id = {q['question_id']: q for q in data['questions']}
    assert len(by_id) == 2349
    assert frozen['question_count'] == 2346
    for qid, expected in frozen['record_hashes'].items():
        assert adapter.record_sha(by_id[qid]) == expected, qid
    assert data['canonical_released_question_count'] == 0
    text = render(data)
    assert '별도 대체 후보 · 기본 목록에서 제외' in text
    assert '최종 ID 문항의 독립 검토가 남아 있습니다.' in text
    assert "KEY='oddments.mpje.practice.v1'" in text
    assert 'ARCHIVE_ONLY_REPLACEMENT_CANDIDATE' in text


def test_compiler_blocks_authority_only_drift_even_when_visible_wording_is_equal(monkeypatch):
    original = compiler.read
    def changed(path):
        value = original(path)
        if path.name == '10_sata_remediation.json':
            value['questions'][0]['choices'][0]['authority_refs'][0]['exact_section'] = 'Unverified section'
        return value
    monkeypatch.setattr(compiler, 'read', changed)
    with pytest.raises(ValueError, match='Lossless remediation authoring/proof drift'):
        compiler.build()


def test_missing_original_independent_artifact_blocks_ordinary_compilation(tmp_path):
    (tmp_path / adapter.ALLOCATION).parent.mkdir(parents=True)
    (tmp_path / adapter.ALLOCATION).write_bytes((ROOT / adapter.ALLOCATION).read_bytes())
    report = tmp_path / adapter.REVIEW_PATH
    report.parent.mkdir(parents=True)
    report.write_bytes((ROOT / adapter.REVIEW_PATH).read_bytes())
    with pytest.raises(FileNotFoundError):
        adapter.validate_independent_binding(tmp_path)


def test_delivered_metadata_changes_are_detected_without_touching_answer_keys():
    from publish_practice import build_payload
    data = build_payload()
    data['questions'][0]['edition'] = 'changed delivery metadata'
    with pytest.raises(ValueError, match='Existing delivered object changed'):
        adapter.validate_published_preservation(data)
