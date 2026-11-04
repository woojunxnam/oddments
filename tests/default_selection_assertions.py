"""Source-derived default snapshot assertions; never an author/legal review."""
import copy
import hashlib
import json
from functools import lru_cache
from pathlib import Path

from legacy_independent_metadata import integrated_sources

CLARIFIER = 'reports/full-corpus-review/phase9-d-evidence/source-citation-retention-clarification.json'
CLARIFIER_SHA = '6a2dde8e04baf983e972fb8fe86d6f51cf593963b11a9321ec54a38b2fd6688b'
ORIGINAL_D = 'reports/full-corpus-review/independent-phase9-d-review.json'
ORIGINAL_D_SHA = 'd6571f097d57da4aed2ba824f624a842ef96aade83b700209feecd85702a3d4c'


def raw_sha(raw):
    return hashlib.sha256(raw).hexdigest()


@lru_cache(maxsize=None)
def native_reviews(root):
    bindings = {}
    sources = integrated_sources(root, source_bindings=bindings)
    return {r['question_id']: r for s in sources for r in s['records']}, bindings


def source_bound_default_delta(selection, preserved, by_id, root):
    """Require unchanged old objects and explain every removal by a native failure."""
    assert len(preserved['recommended_ids']) == 298
    assert len(preserved['holds']) == 147 and len(preserved['safety_holds']) == 3
    assert len(preserved['replacements']) == 77
    return source_bound_selection_delta(selection, preserved, by_id, root)


def source_bound_selection_delta(selection, preserved, by_id, root):
    """Same strict source-bound transition for a separately pinned historical snapshot."""
    root = Path(root)
    assert selection['replacements'] == preserved['replacements']
    added = []
    counts = {}
    for field, id_field in [('holds', 'legacy_question_id'), ('safety_holds', 'question_id')]:
        old = {r[id_field]: r for r in preserved[field]}
        current = {r[id_field]: r for r in selection[field]}
        assert len(old) == len(preserved[field]) and len(current) == len(selection[field])
        assert all(current.get(qid) == record for qid, record in old.items()), 'Old hold object changed'
        added.extend((qid, row) for qid, row in current.items() if qid not in old)
        counts[field] = len(current) - len(old)
    removed = {qid for qid, _ in added}
    assert len(removed) == len(added)
    # Equality forbids an unsupported deletion, restored negative, or new default ID.
    assert selection['recommended_ids'] == [qid for qid in preserved['recommended_ids'] if qid not in removed]
    assert len(selection['recommended_ids']) == len(preserved['recommended_ids']) - len(removed)
    assert selection['stats']['recommended'] == len(selection['recommended_ids'])
    assert selection['stats']['held_from_default'] == len(selection['holds'])
    assert selection['stats']['nonlegacy_safety_held_from_default'] == len(selection['safety_holds'])
    reviews, bindings = native_reviews(root)
    for qid, hold in added:
        assert qid in preserved['recommended_ids'] and qid in bindings
        binding, review = bindings[qid], reviews[qid]
        actual = raw_sha(json.dumps(by_id[qid], ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
        assert hold['question_record_sha256'] == binding['record_sha256'] == review['record_sha256'] == actual
        path = hold.get('evidence_report', hold.get('review_source'))
        expected = hold.get('evidence_report_sha256', hold.get('review_source_sha256'))
        assert raw_sha((root / path).read_bytes()) == expected
        if path == CLARIFIER:
            assert expected == CLARIFIER_SHA
            clarification = json.loads((root / path).read_bytes())
            assert binding['source_path'] == clarification['original_review']['report_path'] == ORIGINAL_D
            assert binding['source_sha256'] == clarification['original_review']['report_raw_sha256'] == ORIGINAL_D_SHA
            assert binding['job_id'] == clarification['original_review']['job_id']
            assert clarification['allowed_uses'] == ['SAFETY_HOLD_SOURCE_BINDING_ONLY']
            assert clarification['not_a_new_review'] is True
        else:
            assert path == binding['source_path'] and expected == binding['source_sha256']
        legal, realism = review['legal_review'], review['realism_review']
        assert (legal['verdict'] != 'KEEP' or legal['existing_answer_correct'] != 'YES'
                or realism['verdict'] != 'PASS'), 'A positive review cannot remove a default'
    return dict(default_count=len(selection['recommended_ids']), removed_ids=removed,
                new_original_holds=counts['holds'], new_nonlegacy_holds=counts['safety_holds'])


def assert_clarifier_only_changes_source_url_metadata(root):
    """Reverse the enumerated URL-only delta and compare entire original records."""
    root = Path(root)
    raw = (root / CLARIFIER).read_bytes()
    assert raw_sha(raw) == CLARIFIER_SHA
    original_raw = (root / ORIGINAL_D).read_bytes()
    assert raw_sha(original_raw) == ORIGINAL_D_SHA
    clarification, original = json.loads(raw), json.loads(original_raw)
    assert clarification['sources'] == original['sources']
    assert clarification['actor_provenance'] == original['actor_provenance']
    for key in ['canonical_release_credit', 'author_review_credit', 'new_independent_audit_credit', 'independent_legal_credit', 'question_audit_credit']:
        assert clarification[key] == 0
    restored = {r['question_id']: copy.deepcopy(r) for r in clarification['records']}
    assert set(restored) == {'MA-REV-0026', 'MA-REV-0027'}
    for change in clarification['citation_metadata_changes']:
        node = restored[change['question_id']]
        # Report indices describe the two-record clarification, not original job ordering.
        for part in change['object_path'].strip('/').split('/')[2:]:
            node = node[int(part)] if isinstance(node, list) else node[part]
        assert node['official_url'] == change['official_url']
        assert node.pop('citation_url') == change['old_official_url'] == change['citation_url']
        node['official_url'] = change['old_official_url']
    original_by_id = {r['question_id']: r for r in original['records']}
    assert all(row == original_by_id[qid] for qid, row in restored.items())
    proof = root / clarification['retained_body_proof_path']
    assert raw_sha(proof.read_bytes()) == clarification['retained_body_proof_sha256']


PHASE10_BEFORE = 'reports/phase10-default-qa-e/before-phase10-selection.json'
PHASE10_BEFORE_SHA = 'b6c8600f059626bec1a6f3903aae81c56acd72f7f843b4bb0acde7b9716891b5'
PHASE10_BINDINGS = 'reports/phase10-default-qa-e/phase10-job-bindings.json'
PHASE10_BINDINGS_SHA = '9a1cfa36b6c3f44924ee5ddbccbbc298b3e2106eb31a97811170242ae64e413b'


def phase10_snapshot(root):
    root = Path(root)
    raw = (root / PHASE10_BEFORE).read_bytes()
    assert raw_sha(raw) == PHASE10_BEFORE_SHA, 'Before-phase10 selector bytes changed'
    before = json.loads(raw)
    assert len(before['recommended_ids']) == 229
    assert len(before['holds']) == 211 and len(before['safety_holds']) == 8
    assert before['stats']['rewrite_default'] == 74
    raw = (root / PHASE10_BINDINGS).read_bytes()
    assert raw_sha(raw) == PHASE10_BINDINGS_SHA, 'Phase10 assigned definitions changed'
    return before, json.loads(raw)['job_definitions']


def source_bound_phase10_delta(selection, by_id, root):
    """A pending wave is an explicit rejection, never a completed QA/positive result."""
    root = Path(root)
    before, expected = phase10_snapshot(root)
    state = json.loads((root / 'reports/full-corpus-review/independent-legacy-work-queue.json').read_bytes())
    jobs = [j for j in state['jobs'] if 34 <= j['sequence'] <= 37]
    assert [{k: j[k] for k in ('sequence', 'job_id', 'stage', 'question_hashes')} for j in jobs] == expected
    if any(j['status'] != 'INTEGRATED' for j in jobs):
        raise ValueError('PHASE10_NOT_INTEGRATED: no complete transition or review credit asserted')
    result = source_bound_selection_delta(selection, before, by_id, root)
    reviews, bindings = native_reviews(root)
    assigned = {j['job_id']: j['question_hashes'] for j in expected}
    for qid in result['removed_ids']:
        binding = bindings[qid]
        assert binding['job_id'] in assigned, 'Removal is outside the exact four phase10 jobs'
        assert assigned[binding['job_id']][qid] == binding['record_sha256']
    assigned_ids = set().union(*(set(ids) for ids in assigned.values()))
    expected_removed = {qid for qid in set(before['recommended_ids']) & assigned_ids
        if reviews[qid]['legal_review']['verdict'] != 'KEEP'
        or reviews[qid]['legal_review']['existing_answer_correct'] != 'YES'
        or reviews[qid]['realism_review']['verdict'] != 'PASS'}
    assert result['removed_ids'] == expected_removed, 'Uncontained current phase10 finding or unsupported removal'
    for qid in selection['recommended_ids']:
        assert qid in bindings and qid in reviews, 'Current default lacks an actual native assessment'
        actual = raw_sha(json.dumps(by_id[qid], ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
        assert bindings[qid]['record_sha256'] == reviews[qid]['record_sha256'] == actual
        assert reviews[qid]['legal_review']['verdict'] == 'KEEP'
        assert reviews[qid]['legal_review']['existing_answer_correct'] == 'YES'
        assert reviews[qid]['realism_review']['verdict'] == 'PASS'
    # Incomplete key assessment remains a procedural/source limitation, not an invented wrong key.
    result['key_not_assessed_removed_ids'] = {qid for qid in result['removed_ids']
        if reviews[qid]['legal_review']['existing_answer_correct'] == 'NOT_ASSESSED'}
    result['wrong_key_removed_ids'] = {qid for qid in result['removed_ids']
        if reviews[qid]['legal_review']['existing_answer_correct'] == 'NO'}
    return result
