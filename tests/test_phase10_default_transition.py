"""Exact before229 -> committed native phase10 safety transition; no legal review."""
import copy
import json
from pathlib import Path

import pytest

import build_representative_rewrites as builder
import build_sata_remediation_candidates as adapter
from default_selection_assertions import (phase10_snapshot, source_bound_phase10_delta,
    source_bound_selection_delta)

ROOT = Path(__file__).resolve().parents[1]


def raw_questions():
    return {q['question_id']: q for path in adapter.PUBLIC_BANKS
            for q in json.loads((ROOT / path).read_bytes())['questions']}


def test_phase10_before_snapshot_keeps_real_original_history_and_archive_candidates():
    before, definitions = phase10_snapshot(ROOT)
    assert [j['sequence'] for j in definitions] == [34, 35, 36, 37]
    assert sum(len(j['question_hashes']) for j in definitions) == 160
    manifest = json.loads((ROOT / adapter.ALLOCATION).read_bytes())
    assert len(manifest['public_question_record_hashes']) == 2346
    assert len(manifest['representative_question_hashes']) == 74
    assert len(manifest['representative_source_hashes']) == 81
    candidates = {r['question_id'] for r in manifest['allocations']}
    assert len(candidates) == 3 and not candidates & set(before['recommended_ids'])
    assert len(before['recommended_ids']) == len(set(before['recommended_ids'])) == 229


def test_actual_phase10_transition_requires_all_four_native_integrations_and_exact_negative_sources():
    selection = json.loads((ROOT / adapter.BASE / 'selection.json').read_bytes())
    state = json.loads((ROOT / 'reports/full-corpus-review/independent-legacy-work-queue.json').read_bytes())
    pending = any(j['status'] != 'INTEGRATED' for j in state['jobs'] if 34 <= j['sequence'] <= 37)
    if pending:
        # This tests the pending rejection; it is not a completed-wave PASS or a skip.
        with pytest.raises(ValueError, match='PHASE10_NOT_INTEGRATED'):
            source_bound_phase10_delta(selection, raw_questions(), ROOT)
        return
    before, _ = phase10_snapshot(ROOT)
    delta = source_bound_phase10_delta(selection, raw_questions(), ROOT)
    assert selection['recommended_ids'] == [qid for qid in before['recommended_ids']
                                            if qid not in delta['removed_ids']]
    assert not delta['key_not_assessed_removed_ids'] & delta['wrong_key_removed_ids']
    builder.validate_nonlegacy_selection(selection, json.loads(builder.ORIGINAL_SELECTION.read_bytes()),
                                         raw_questions(), ROOT)
    if delta['removed_ids']:
        # Remove one real new containment, restore its ID in original order, and update
        # the three count fields checked by the common helper. The actual native
        # negative must still reject this otherwise self-consistent restoration.
        qid = sorted(delta['removed_ids'])[0]
        invalid = copy.deepcopy(selection)
        for field, id_field in [('holds', 'legacy_question_id'), ('safety_holds', 'question_id')]:
            invalid[field] = [h for h in invalid[field] if h[id_field] != qid]
        still_removed = delta['removed_ids'] - {qid}
        invalid['recommended_ids'] = [x for x in before['recommended_ids'] if x not in still_removed]
        invalid['stats']['recommended'] = len(invalid['recommended_ids'])
        invalid['stats']['held_from_default'] = len(invalid['holds'])
        invalid['stats']['nonlegacy_safety_held_from_default'] = len(invalid['safety_holds'])
        with pytest.raises(AssertionError, match='Uncontained current phase10 finding'):
            source_bound_phase10_delta(invalid, raw_questions(), ROOT)


@pytest.mark.parametrize('mutation', ['restored_negative', 'unsupported_removal', 'old_hold', 'replacement'])
def test_phase10_snapshot_cannot_hide_default_or_original_history_mutations(mutation):
    before, _ = phase10_snapshot(ROOT)
    changed = copy.deepcopy(before)
    if mutation == 'restored_negative':
        changed['recommended_ids'].append(before['safety_holds'][0]['question_id'])
    elif mutation == 'unsupported_removal':
        changed['recommended_ids'].pop()
    elif mutation == 'old_hold':
        changed['holds'][0]['reason'] += ' changed'
    else:
        changed['replacements'][0]['replacement_question_id'] = 'MA-RW-9999'
    with pytest.raises(AssertionError):
        source_bound_selection_delta(changed, before, raw_questions(), ROOT)


def test_phase10_preserves_355_historical_statuses_question_objects_and_M_source():
    import hashlib
    import build_representative_audit_ledger as ledger
    from notes_revision import load_notes
    raw = (ROOT / 'reports/phase10-default-qa-e/original-history-and-M-snapshot.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '0a65d1c60c53d68f463562590553a1e8f39fee7c508a3906ef6bcb301355e171'
    before = json.loads(raw)
    digest = lambda value: hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    actual = ledger.build_ledger()
    assert actual['counts']['implementation_statuses'] == before['original355_implementation_statuses']
    assert {r['question_id']: dict(implementation_status=r['implementation_status'],
        editorial_triage_sha256=digest(r['editorial_triage'])) for r in actual['questions']} == before['original355']
    bank = json.loads((ROOT / adapter.BASE / 'questions.json').read_bytes())
    allocation = adapter.validate_preservation(bank, ROOT)
    by_id = raw_questions()
    assert all(adapter.record_sha(by_id[qid]) == expected
               for qid, expected in allocation['public_question_record_hashes'].items())
    for row in actual['questions']:
        replacement = row['implementation']['replacement_question_id']
        if replacement is None:
            continue
        hold = row['implementation']['replacement_default_safety_hold']
        assert row['implementation']['replacement_is_in_current_default'] is (hold is None)
        if hold:
            assert hold['question_id'] == replacement
            # The original remains a historical implemented rewrite when its replacement is held.
            if replacement.startswith('MA-RW-'):
                assert row['implementation_status'] == 'REWRITTEN_NEW_ID'
    notes = load_notes(ROOT)
    assert hashlib.sha256(json.dumps(notes, ensure_ascii=False, sort_keys=True).encode()).hexdigest() == before['effective_notes_semantic_sha256']
    m = next(u for c in notes['chapters'] for u in c['units'] if u['id'] == 'w3-a-3')
    assert hashlib.sha256(m['body'].encode()).hexdigest() == before['M_unit']['actual_body_sha256']
    unit = next(json.loads(line) for line in (ROOT / 'reports/full-corpus-review/notes-unit-ledger.jsonl').read_text().splitlines()
                if json.loads(line)['unit_id'] == 'w3-a-3')
    assert unit['atomic_census_source'] == before['M_unit']['selected_census_path']
    assert unit['atomic_claim_ids'] == before['M_unit']['atomic_claim_ids']
    assert hashlib.sha256((ROOT / unit['atomic_census_source']).read_bytes()).hexdigest() == before['M_unit']['selected_census_raw_sha256']


def test_phase10_archive_notice_splits_preserve_whole_previous_groups_and_exact_sources():
    from default_selection_assertions import phase10_archive_history
    state = json.loads((ROOT / 'reports/full-corpus-review/independent-legacy-work-queue.json').read_bytes())
    if any(j['status'] != 'INTEGRATED' for j in state['jobs'] if 34 <= j['sequence'] <= 37):
        with pytest.raises(ValueError, match='PHASE10_NOT_INTEGRATED'):
            phase10_archive_history(ROOT)
        return
    result = phase10_archive_history(ROOT)
    assert result['native_notice_ids'] == result['replaced_prior_ids'] | result['newly_notified_ids']
    assert not result['replaced_prior_ids'] & result['newly_notified_ids']
    current = json.loads((ROOT / 'reports/representative-rewrite/archive-review-notices.json').read_bytes())['notices']
    if result['replaced_prior_ids']:
        bad = copy.deepcopy(current)
        qid = sorted(result['replaced_prior_ids'])[0]
        row = next(n for n in bad if qid in n['question_ids'])
        row['previous_notices'][0]['reason'] += ' altered prior history'
        with pytest.raises(AssertionError, match='Full original notice group/history changed'):
            phase10_archive_history(ROOT, bad)
    bad = copy.deepcopy(current)
    bad.append(copy.deepcopy(bad[0]))
    with pytest.raises(AssertionError, match='Duplicate current archive notice ID'):
        phase10_archive_history(ROOT, bad)
