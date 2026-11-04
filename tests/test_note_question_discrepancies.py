"""Source-bound local containment without rewriting questions or review history."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import note_question_discrepancies as links
import note_review_queue as queue
from notes_independent_metadata import evidence_bindings

BANK = 'practice_expansion/2026-10-26-plus/questions.json'


def write(root, path, value):
    target = root / path; target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(queue.encoded(value))


def commit(root):
    queue.git(root, 'add', '.')
    queue.git(root, 'commit', '-qm', 'Source-bound note-link fixture')


@pytest.fixture
def fixture(tmp_path):
    root = tmp_path / 'repo'; root.mkdir()
    subprocess.run(['git', 'init', '-q', '-b', 'main', str(root)], check=True)
    queue.git(root, 'config', 'user.name', 'Fixture')
    queue.git(root, 'config', 'user.email', 'fixture@example.invalid')
    state = json.loads((ROOT / queue.STATE).read_bytes())
    job = next(j for j in state['jobs'] if j['job_id'] == links.JOB_ID)
    report = json.loads((ROOT / links.REPORT['path']).read_bytes())
    paths = {links.BACKLOG, queue.STATE, links.REPORT['path'], links.ALIGNMENT['path'],
             links.SELECTION, job['result']['result_path']}
    paths.update(p for p, _ in evidence_bindings(report))
    alignment = json.loads((ROOT / links.ALIGNMENT['path']).read_bytes())
    paths.update(p for p, _ in evidence_bindings(alignment))
    paths.update(p for p, _ in queue.validate_evidence(job, job['result'], report))
    for path in paths:
        target = root / path; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / path, target)
    questions = {q['question_id']: q for q in json.loads((ROOT / BANK).read_bytes())['questions']
                 if q['question_id'] in links.CHOICES}
    write(root, BANK, {'questions': list(questions.values())})
    commit(root)
    return root, questions


def test_snapshot_only_consumer_needs_no_worker_history_or_identity_claim(fixture):
    root, questions = fixture
    assert queue.git(root, 'rev-list', '--all', '--count') == '1'
    assert subprocess.run(['git', '-C', str(root), 'cat-file', '-e',
                           '26b6ad2ce6b72ccdaa824f8886f41eec4caea026'],
                          capture_output=True).returncode != 0
    metadata = links.load_metadata(root, questions)
    assert set(metadata['records']) == set(links.CHOICES)
    assert metadata['input_bindings'][links.REPORT['path']] == links.REPORT['raw_sha256']
    assert metadata['input_bindings'][links.ALIGNMENT['path']] == links.ALIGNMENT['raw_sha256']
    for path, sha in metadata['input_bindings'].items():
        assert queue.raw_sha((root / path).read_bytes()) == sha
    for record in metadata['records'].values():
        assert record['whole_question_existing_answer_correct'] == 'NOT_ASSESSED'
        assert record['independence_basis'] == 'CONTROLLER_ATTESTED_DECLARATION_NOT_IDENTITY_PROOF'
        assert record['canonical_audit'] is False
        assert record['question_audit_credit'] == record['canonical_release_credit'] == 0


@pytest.mark.parametrize('path', [links.BACKLOG, links.REPORT['path'], links.ALIGNMENT['path'],
                                 queue.STATE, BANK])
def test_uncommitted_source_payload_is_rejected(fixture, path):
    root, questions = fixture
    with (root / path).open('ab') as stream:
        stream.write(b'\n')
    with pytest.raises(ValueError, match='Uncommitted note-link'):
        links.load_metadata(root, questions)


@pytest.mark.parametrize('path', [links.REPORT['path'], links.ALIGNMENT['path']])
def test_committed_but_changed_fixed_raw_payload_is_rejected(fixture, path):
    root, questions = fixture
    with (root / path).open('ab') as stream:
        stream.write(b'\n')
    commit(root)
    with pytest.raises(ValueError, match='raw SHA'):
        links.load_metadata(root, questions)


@pytest.mark.parametrize('change', ['missing', 'duplicate', 'extra', 'finding', 'row_hash',
                                   'choice', 'credit', 'scope', 'whole_key', 'source_path'])
def test_committed_backlog_cannot_drop_expand_or_relabel_source_rows(fixture, change):
    root, questions = fixture
    payload = json.loads((root / links.BACKLOG).read_bytes())
    row = payload['records'][0]
    if change == 'missing': payload['records'].pop()
    elif change == 'duplicate': payload['records'][-1] = copy.deepcopy(row)
    elif change == 'extra': payload['records'].append({**row, 'question_id': 'MA-CASE-0803'})
    elif change == 'finding': row['finding_ko'] = 'Changed local conclusion'
    elif change == 'row_hash': row['source_alignment_record_sha256'] = '0' * 64
    elif change == 'choice': row['affected_choice_id'] = 'A'
    elif change == 'credit': payload['question_audit_credit'] = True
    elif change == 'scope': row['scope'] = 'WHOLE_QUESTION_AUDIT'
    elif change == 'whole_key': row['whole_question_existing_answer_correct'] = 'YES'
    elif change == 'source_path': payload['source_alignment']['path'] = '../different.json'
    write(root, links.BACKLOG, payload); commit(root)
    with pytest.raises(ValueError): links.load_metadata(root, questions)


@pytest.mark.parametrize('change', ['stage', 'status', 'actor', 'instance', 'credit', 'event', 'envelope'])
def test_committed_note_provenance_and_credit_gate_cannot_be_bypassed(fixture, change):
    root, questions = fixture
    state = json.loads((root / queue.STATE).read_bytes())
    job = next(j for j in state['jobs'] if j['job_id'] == links.JOB_ID)
    if change == 'stage': state['stage'] = 'independent-legacy'
    elif change == 'status': job['status'] = 'SUBMITTED'
    elif change == 'actor': job['actor_provenance']['actor_id'] = '/root'
    elif change == 'instance': job['auditor_instance'] = 'invented new identity'
    elif change == 'credit': job['result']['canonical_release_credit'] = 1
    elif change == 'event': state['events'] = [e for e in state['events']
        if not (e.get('job_id') == links.JOB_ID and e['kind'] == 'INTEGRATE')]
    elif change == 'envelope': job['result']['evidence']['raw_sha256'] = '0' * 64
    write(root, queue.STATE, state); commit(root)
    with pytest.raises(ValueError): links.load_metadata(root, questions)


@pytest.mark.parametrize('field', ['stem', 'choices', 'correct_choice_ids', 'explanation'])
def test_changed_current_original_stem_choice_key_or_explanation_is_rejected(fixture, field):
    root, questions = fixture
    altered = copy.deepcopy(questions); qid = next(iter(links.CHOICES)); question = altered[qid]
    if field == 'stem': question['stem'] += ' Extra fact.'
    elif field == 'choices': question['choices'][0]['text'] += ' New condition.'
    elif field == 'correct_choice_ids': question['correct_choice_ids'] = ['B']
    else: question['explanation']['core_reasoning'] += ' Different reasoning.'
    write(root, BANK, {'questions': list(altered.values())}); commit(root)
    with pytest.raises(ValueError, match='committed original'):
        links.load_metadata(root, altered)


@pytest.mark.parametrize('field,value', [
    ('scope_contradiction', 'NO_CONTRADICTION'),
    ('local_legal_key_and_explanation_assessment', 'KEEP'),
    ('whole_question_existing_answer_correct', 'YES'),
    ('full_question_audit_credit', 1), ('choice_text', 'A licensed technician...'),
    ('stored_key', ['B']), ('choice_in_stored_key', True),
])
def test_even_rehashed_alignment_row_cannot_change_local_scope(fixture, field, value):
    root, questions = fixture
    backlog = json.loads((root / links.BACKLOG).read_bytes())
    alignment = json.loads((root / links.ALIGNMENT['path']).read_bytes())
    row = backlog['records'][0]
    source = next(r for r in alignment['direct_matching_option_evidence']
                  if r['question_id'] == row['question_id'])
    source[field] = value
    row['source_alignment_record_sha256'] = queue.digest(source)
    with pytest.raises(ValueError): links.validate_rows(backlog, alignment, questions)


def test_default_restoration_fails_closed_for_current_or_proposed_selection(fixture):
    root, questions = fixture
    qid = next(iter(links.CHOICES))
    with pytest.raises(ValueError, match='restored to default'):
        links.load_metadata(root, questions, default_ids=[qid])
    selection = json.loads((root / links.SELECTION).read_bytes())
    selection['recommended_ids'].append(qid)
    write(root, links.SELECTION, selection); commit(root)
    with pytest.raises(ValueError, match='restored to default'):
        links.load_metadata(root, questions)


@pytest.fixture(scope='module')
def actual_outputs():
    import build_full_corpus_review as corpus
    import build_representative_rewrites as rewrites
    full = corpus.build()
    rows = {r['question_id']: r for r in map(json.loads, full[corpus.OUT / 'question-ledger.jsonl'].splitlines())}
    rewritten = rewrites.build()
    # Notice-only metadata must not change the representative bank, including
    # its source-authoring metadata, or introduce a selection self-hash cycle.
    assert rewrites.encoded(rewritten[rewrites.BASE / 'questions.json']) == (rewrites.BASE / 'questions.json').read_bytes()
    selection = rewritten[rewrites.BASE / 'selection.json']
    assert links.SELECTION not in selection['input_hashes']
    return rows, selection


def test_all_eleven_derived_holds_preserve_actual_old_keep_and_negative_opinions(actual_outputs):
    rows, selection = actual_outputs
    baseline = {r['question_id']: r for r in map(json.loads,
        (ROOT / 'reports/full-corpus-review/question-ledger.jsonl').read_text().splitlines())}
    from build_sata_remediation_candidates import ALLOCATION
    allocation = json.loads((ROOT / ALLOCATION).read_bytes())
    preserved_ids = set(allocation['public_question_record_hashes'])
    candidate_ids = {r['question_id'] for r in allocation['allocations']}
    assert len(preserved_ids) == 2346 and len(candidate_ids) == 3
    assert set(rows) == set(baseline) == preserved_ids | candidate_ids
    assert sum(rows[qid]['before_note_link_discrepancy_hold']['disposition'] == 'KEEP'
               for qid in links.CHOICES) == 6
    for qid, old in baseline.items():
        row = rows[qid]
        if qid not in links.CHOICES:
            assert row == old
            continue
        assert row['disposition'] == 'HOLD_FOR_LEGAL_REVIEW'
        # Regeneration is idempotent after these holds have already been published.
        if 'before_note_link_discrepancy_hold' in old:
            assert row == old
        original = old.get('before_note_link_discrepancy_hold', old)
        assert row['before_note_link_discrepancy_hold'] == original
        for field in ('author_disposition', 'independent_legacy_legal_assessment',
                      'independent_legacy_realism_assessment', 'reviewer_provenance',
                      'answer_key_assessment', 'choice_by_choice_findings'):
            if field in original: assert row[field] == original[field]
        assert row['note_link_discrepancy_hold']['question_audit_credit'] == 0
    assert not set(links.CHOICES) & set(selection['recommended_ids'])


def test_stronger_delete_replace_and_every_prior_blocker_survive(fixture):
    root, questions = fixture
    metadata = links.load_metadata(root, questions)
    original = [dict(question_id=qid, disposition='KEEP', blocker='Original blocker',
                     answer_key_assessment='OLD_OPINION', independent_legacy_legal_assessment={'verdict': 'DELETE'})
                for qid in links.CHOICES]
    original[0]['disposition'] = 'DELETE'; original[1]['disposition'] = 'REPLACE'
    rows = copy.deepcopy(original); inputs = copy.deepcopy(metadata)
    links.apply_holds(rows, metadata)
    assert metadata == inputs
    for before, row in zip(original, rows):
        assert row['before_note_link_discrepancy_hold'] == before
        assert row['disposition'] == (before['disposition'] if before['disposition'] in {'DELETE','REPLACE'}
                                      else 'HOLD_FOR_LEGAL_REVIEW')
        assert before['blocker'] in row['blocker']
        assert row['independent_legacy_legal_assessment'] == before['independent_legacy_legal_assessment']
    snapshot = copy.deepcopy(rows); links.apply_holds(rows, metadata)
    assert rows == snapshot


def test_six_new_archive_warnings_and_five_exact_prior_notice_histories(actual_outputs):
    _, selection = actual_outputs
    previous = json.loads((ROOT / 'reports/representative-rewrite/archive-review-notices.json').read_bytes())['notices']
    old_by_id = {qid: n for n in previous for qid in n['question_ids']}
    notices = selection['archive_review_notices']
    ids = [qid for n in notices for qid in n['question_ids']]
    assert len(ids) == len(set(ids))
    held = {n['question_ids'][0]: n for n in notices if n['issue_type'] == links.ISSUE}
    assert set(held) == set(links.CHOICES)
    assert sum(bool(n['previous_notices']) for n in held.values()) == 5
    assert sum(not n['previous_notices'] for n in held.values()) == 6
    for qid, notice in held.items():
        assert notice['previous_notices'] == ([old_by_id[qid]] if qid in old_by_id else [])
        assert 'trained cashier' in notice['reason'] and '무면허' in notice['reason']
        assert 'NOT_ASSESSED' in notice['reason'] and '평가하지 않았' in notice['reason']
        assert notice['note_link_discrepancy_hold']['local_legal_key_and_explanation_assessment'] == links.LOCAL
        assert 'original_author_blocker' not in notice
    unaffected = [n for n in previous if not set(n['question_ids']) & set(links.CHOICES)]
    assert [n for n in notices if n['issue_type'] != links.ISSUE] == unaffected


def test_archive_adapter_never_mutates_old_notice_and_rejects_duplicate_ids(fixture):
    root, questions = fixture; metadata = links.load_metadata(root, questions)
    old = [{'question_ids': ['MA-CASE-0354', 'unrelated'], 'issue_type': 'INDEPENDENT_REVIEW_FINDING',
            'reason': 'Original negative reason', 'review_source': 'original-source',
            'question_record_hashes': {'MA-CASE-0354': 'original-hash', 'unrelated': 'another-hash'}}]
    snapshot = copy.deepcopy(old); result = links.archive_notices(old, metadata)
    assert old == snapshot
    assert result[0]['question_ids'] == ['unrelated']
    held = next(n for n in result if n['question_ids'] == ['MA-CASE-0354'])
    assert held['previous_notices'] == snapshot
    with pytest.raises(ValueError, match='Repeated original'):
        links.archive_notices(old + copy.deepcopy(old), metadata)


def test_actual_shallow_clone_needs_only_head_payloads(fixture):
    root, questions = fixture; shallow = root.parent / 'shallow'
    subprocess.run(['git', 'clone', '-q', '--depth=1', root.as_uri(), str(shallow)], check=True)
    assert queue.git(shallow, 'rev-parse', '--is-shallow-repository') == 'true'
    assert set(links.load_metadata(shallow, questions)['records']) == set(links.CHOICES)


def test_retained_official_payload_corruption_is_rejected_even_when_committed(fixture):
    root, questions = fixture
    report = json.loads((root / links.REPORT['path']).read_bytes())
    path = report['sources'][0]['evidence_path']
    with (root / path).open('ab') as stream: stream.write(b'changed raw source')
    commit(root)
    with pytest.raises(ValueError, match='raw SHA'):
        links.load_metadata(root, questions)


@pytest.mark.parametrize('field,value', [
    ('stage', 'independent-legacy'), ('independent_of_authors', False),
    ('canonical_audit', True), ('question_audit_credit', 1),
])
def test_report_provenance_and_credit_cannot_change_under_captured_raw_binding(fixture, field, value):
    root, questions = fixture
    report = json.loads((root / links.REPORT['path']).read_bytes())
    report[field] = value
    write(root, links.REPORT['path'], report); commit(root)
    with pytest.raises(ValueError, match='raw SHA'):
        links.load_metadata(root, questions)


def test_derived_selection_does_not_create_a_self_hash_or_change_warning_inputs(fixture):
    root, questions = fixture
    first = links.load_metadata(root, questions)
    selection = json.loads((root / links.SELECTION).read_bytes())
    selection['archive_review_notices'] = links.archive_notices([], first)
    write(root, links.SELECTION, selection); commit(root)
    second = links.load_metadata(root, questions)
    assert first['records'] == second['records']
    assert links.archive_notices([], first) == links.archive_notices([], second)
    assert first['input_bindings'][links.SELECTION] != second['input_bindings'][links.SELECTION]


def test_notice_only_dirty_derived_selection_can_regenerate_without_default_restore(fixture):
    root, questions = fixture
    first = links.load_metadata(root, questions)
    selection = json.loads((root / links.SELECTION).read_bytes())
    selection['archive_review_notices'] = links.archive_notices([], first)
    write(root, links.SELECTION, selection)  # Simulate the preceding builder output, without a commit.
    assert links.load_metadata(root, questions)['records'] == first['records']
    selection['recommended_ids'].append(next(iter(links.CHOICES)))
    write(root, links.SELECTION, selection)
    with pytest.raises(ValueError, match='restored to default'):
        links.load_metadata(root, questions)
