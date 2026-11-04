"""Derived scheduling state consumes reviews; these tests grant no review credit."""
import copy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_full_corpus_review import apply_independent_legacy_review, record_hash
from legacy_independent_metadata import integrated_sources
from default_selection_assertions import source_bound_default_delta


@pytest.fixture
def context():
    audit = dict(question_id='MA-RW-0081', record_sha256='a' * 64,
        legal_review=dict(existing_answer_correct='YES', verdict='KEEP', blocker=None,
                          finding_ko='합성 검증용 법규 판정'),
        realism_review=dict(verdict='PASS', finding_ko='합성 검증용 현실성 판정'),
        required_next_action_ko='확인된 문제를 해결한 뒤 새 해시로 재검토한다.')
    row = dict(question_id=audit['question_id'], content_sha256=audit['record_sha256'],
        disposition='KEEP', blocker=None, answer_key_assessment='FORMAL_CURRENT_ID_AUTHOR_EXPECTED_KEY_RECORDED',
        checked_at_scope='FORMAL_NATIVE_CURRENT_ID_AUTHOR_REVIEW', current_id_author_review_required=False,
        native_author_review_job_id='native-author-job',
        review_evidence=dict(native_author_job_id='native-author-job'),
        known_author_editor_actor_ids=['/root/independent_case_g', '/root/independent_case_e'],
        source_author_review_binding=dict(current_id_independent_audit='PENDING',
            original_author_provenance=dict(actor_id='/root/independent_case_g')),
        next_action='Different actual session must audit the compiled current ID independently.',
        implementation_status='ARCHIVE_ONLY_REPLACEMENT_CANDIDATE', publication_status='PRACTICE_CONFIG_ARCHIVE',
        author_review_increment=1, independent_review_credit=0, canonical_release_credit=0)
    binding = dict(question_id=audit['question_id'], source_path='reports/full-corpus-review/synthetic-review.json',
        source_sha256='b' * 64, job_id='native-independent-job', record_sha256=audit['record_sha256'],
        review_record_sha256=record_hash(audit), reviewed_at='2026-11-04',
        auditor_instance='synthetic-independent-session',
        actor_provenance=dict(actor_id='/root/independent_case_f', session_id='/root/independent_case_f'))
    return row, audit, binding


def test_completed_review_replaces_pending_instruction_without_changing_history_or_credit(context):
    row, audit, binding = context
    history = copy.deepcopy(row['source_author_review_binding']); original_audit = copy.deepcopy(audit)
    apply_independent_legacy_review(row, audit, source_binding=binding)
    assert row['current_id_independent_review_status'] == 'SOURCE_BOUND_PASS'
    assert row['current_id_independent_review_source'] == binding
    assert 'root QA, publication and default-selection review remain pending' in row['next_action']
    assert row['source_author_review_binding'] == history and history['current_id_independent_audit'] == 'PENDING'
    assert row['independent_review_credit'] == row['canonical_release_credit'] == 0
    assert row['author_review_increment'] == 1
    assert row['implementation_status'] == 'ARCHIVE_ONLY_REPLACEMENT_CANDIDATE'
    assert row['publication_status'] == 'PRACTICE_CONFIG_ARCHIVE' and audit == original_audit
    binding['actor_provenance']['session_id'] = 'mutated caller'
    assert row['current_id_independent_review_source']['actor_provenance']['session_id'] != 'mutated caller'


@pytest.mark.parametrize('key,legal,realism,expected_status,actual_blocker', [
    ('NO', 'KEEP', 'PASS', 'SOURCE_BOUND_NOT_PASSED', '기존 정답이 공식 조문과 다름'),
    ('YES', 'HOLD', 'PASS', 'SOURCE_BOUND_NOT_PASSED', '필수 적용 조건이 누락됨'),
    ('YES', 'KEEP', 'FAIL', 'SOURCE_BOUND_NOT_PASSED', '오답의 실제 조건을 교정해야 함'),
    ('NOT_ASSESSED', 'HOLD', 'PASS', 'SOURCE_BOUND_INCOMPLETE', '공식 원문 접근이 완료되지 않음'),
    ('YES', 'KEEP', 'NOT_ASSESSED', 'SOURCE_BOUND_INCOMPLETE', '현실성 비교가 미완료임'),
])
def test_failed_or_incomplete_review_surfaces_its_actual_blocker(context, key, legal, realism,
                                                               expected_status, actual_blocker):
    row, audit, binding = context
    audit['legal_review'].update(existing_answer_correct=key, verdict=legal,
                                blocker=actual_blocker if legal != 'KEEP' or key != 'YES' else None)
    audit['realism_review'].update(verdict=realism, finding_ko=actual_blocker)
    audit['required_next_action_ko'] = actual_blocker
    binding['review_record_sha256'] = record_hash(audit)
    apply_independent_legacy_review(row, audit, source_binding=binding)
    assert row['current_id_independent_review_status'] == expected_status
    assert row['next_action'] == actual_blocker and row['disposition'] != 'KEEP'
    assert row['independent_review_credit'] == row['canonical_release_credit'] == 0


def test_positive_independent_review_cannot_clear_an_existing_author_blocker(context):
    row, audit, binding = context
    row.update(disposition='HOLD', blocker='기존 저자 보류가 해결되지 않음')
    apply_independent_legacy_review(row, audit, source_binding=binding)
    assert row['current_id_independent_review_status'] == 'SOURCE_BOUND_PASS'
    assert row['disposition'] == 'HOLD' and row['next_action'] == '기존 저자 보류가 해결되지 않음'


@pytest.mark.parametrize('mutation', ['current_hash', 'audit_hash', 'bound_hash', 'review_digest', 'author_job', 'actor'])
def test_stale_or_unbound_source_cannot_advance_current_state(context, mutation):
    row, audit, binding = context
    if mutation == 'current_hash': row['content_sha256'] = 'c' * 64
    elif mutation == 'audit_hash': audit['record_sha256'] = 'c' * 64
    elif mutation == 'bound_hash': binding['record_sha256'] = 'c' * 64
    elif mutation == 'review_digest': binding['review_record_sha256'] = 'c' * 64
    elif mutation == 'author_job': row['review_evidence']['native_author_job_id'] = 'another-job'
    elif mutation == 'actor': binding['actor_provenance']['actor_id'] = '/root/independent_case_g'
    with pytest.raises(ValueError, match='binding|author review|source provenance'):
        apply_independent_legacy_review(row, audit, source_binding=binding)
    assert 'current_id_independent_review_status' not in row


@pytest.mark.parametrize('missing', ['independent_source', 'native_author'])
def test_absent_validated_source_or_native_author_keeps_pending_instruction(context, missing):
    row, audit, binding = context
    if missing == 'native_author': row['current_id_author_review_required'] = True
    before = row['next_action']
    apply_independent_legacy_review(row, audit, source_binding=None if missing == 'independent_source' else binding)
    assert 'current_id_independent_review_status' not in row and row['next_action'] == before


def test_other_ids_keep_exact_existing_behavior(context):
    row, audit, binding = context
    row['question_id'] = audit['question_id'] = binding['question_id'] = 'MA-RW-0080'
    old_behavior = copy.deepcopy(row)
    apply_independent_legacy_review(old_behavior, audit)
    apply_independent_legacy_review(row, audit, source_binding=binding)
    assert row == old_behavior


def test_real_native_author_and_integrated_independent_sources_bind_only_three_frozen_candidates():
    from build_sata_remediation_candidates import BASE, ALLOCATION, PUBLIC_BANKS, bind_candidate_inventory_row
    qids = {'MA-RW-0081', 'MA-RW-0082', 'MA-RW-0083'}
    questions = {q['question_id']: q for q in json.loads((ROOT / BASE / 'questions.json').read_bytes())['questions']
                 if q['question_id'] in qids}
    frozen = copy.deepcopy(questions)
    bindings = {}
    sources = integrated_sources(ROOT, source_bindings=bindings)
    audits = {r['question_id']: r for s in sources for r in s['records'] if r['question_id'] in qids}
    selection_raw = (ROOT / BASE / 'selection.json').read_bytes()
    selection = json.loads(selection_raw)
    preserved = json.loads((ROOT / ALLOCATION).read_bytes())['preserved_selection']
    by_id = {q['question_id']: q for path in PUBLIC_BANKS
             for q in json.loads((ROOT / path).read_bytes())['questions']}
    source_bound_default_delta(selection, preserved, by_id, ROOT)
    assert not qids.intersection(selection['recommended_ids'])
    for qid, q in questions.items():
        row = dict(question_id=qid, content_sha256=record_hash(q))
        bind_candidate_inventory_row(row, q, ROOT)
        history = copy.deepcopy(row['source_author_review_binding'])
        credits = {k: row[k] for k in ['author_review_increment', 'independent_review_credit', 'canonical_release_credit']}
        apply_independent_legacy_review(row, audits[qid], source_binding=bindings[qid])
        assert row['current_id_independent_review_status'] == 'SOURCE_BOUND_PASS'
        assert row['current_id_independent_review_source']['source_path'] == (
            'reports/full-corpus-review/sata-remediation-current-id-independent/f-review.json')
        assert row['current_id_independent_review_source']['record_sha256'] == record_hash(q)
        assert row['current_id_independent_review_source']['source_sha256'] == (
            '4aa05044a6a5d65f2d0ebffa7e43df8d857de47ed92ccda657f1bd991608a641')
        assert row['source_author_review_binding'] == history
        assert q['remediation_candidate']['current_id_independent_audit'] == 'PENDING'
        assert {k: row[k] for k in credits} == credits
        assert row['implementation_status'] == 'ARCHIVE_ONLY_REPLACEMENT_CANDIDATE'
    assert questions == frozen and (ROOT / BASE / 'selection.json').read_bytes() == selection_raw
