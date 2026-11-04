"""Synthetic native-author lifecycle tests; these fixtures are not legal reviews."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import remediation_author_reviews as native
import review_queue as queue
import build_sata_remediation_candidates as adapter

G = '/root/independent_case_g'
E = '/root/independent_case_e'
NOW = '2026-11-04T05:00:00+00:00'
Q = {q['question_id']: q for q in json.loads((ROOT / adapter.BASE / 'questions.json').read_text())['questions'] if q.get('archive_only_candidate')}
AUTHORING = adapter.authoring_payload(ROOT)
REAL_CANDIDATE_RECORDS = native.candidate_records


def write(root, path, value):
    p = root / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.DEVNULL, text=True).strip()


def commit(root):
    git(root, 'add', '.')
    git(root, 'commit', '-qm', 'synthetic lifecycle fixture')
    return git(root, 'rev-parse', 'HEAD')


@pytest.fixture
def repo(tmp_path, monkeypatch):
    state = json.loads((ROOT / native.QUEUE).read_text())
    assert len(state['jobs']) == 52
    write(tmp_path, native.QUEUE, state)
    static = ['synthetic-old-a.json', 'synthetic-old-b.json']
    for f in static: write(tmp_path, 'reports/full-corpus-review/' + f, {'fixture': f})
    baseline = dict(candidate_question_hashes={qid: native.digest(q) for qid, q in Q.items()},
        required_author_provenance=native.expected_actor(Q), static_review_files=static,
        static_source_sha256={'reports/full-corpus-review/' + f: hashlib.sha256((tmp_path / 'reports/full-corpus-review' / f).read_bytes()).hexdigest() for f in static},
        original_52_job_hashes=[native.digest(j) for j in state['jobs']],
        original_event_hashes=[native.digest(e) for e in state['events']])
    write(tmp_path, native.BASELINE, baseline)
    monkeypatch.setattr(native, 'BASELINE_SHA256', hashlib.sha256((tmp_path / native.BASELINE).read_bytes()).hexdigest())
    monkeypatch.setattr(native, 'candidate_records', lambda root: copy.deepcopy(Q))
    monkeypatch.setattr(adapter, 'authoring_payload', lambda root=ROOT: copy.deepcopy(AUTHORING))
    write(tmp_path, adapter.ALLOCATION, json.loads((ROOT / adapter.ALLOCATION).read_bytes()))
    write(tmp_path, adapter.BASE + '/questions.json', {'questions': list(Q.values())})
    raw_path = native.PREFIX + 'evidence/synthetic-primary.txt'
    (tmp_path / raw_path).parent.mkdir(parents=True)
    (tmp_path / raw_path).write_text('Synthetic fixture bytes, never a real legal assessment.\n')
    primary_sha = hashlib.sha256((tmp_path / raw_path).read_bytes()).hexdigest()
    metadata_path = native.PREFIX + 'evidence/synthetic-retrieval.json'
    url = 'https://www.mass.gov/doc/synthetic-test-source/download'
    write(tmp_path, metadata_path, dict(official_url=url, raw_sha256=primary_sha, http_status=200))
    authority = dict(official_url=url, exact_section='Synthetic test section', law_checked_date='2026-11-04',
        version_or_effective_date_status='SYNTHETIC_TEST_ONLY_NOT_LEGAL_EVIDENCE', body_verified_current_primary=True,
        http_status=200, used_as_legal_proof=True, raw_path=raw_path, raw_sha256=primary_sha,
        retrieval_metadata_path=metadata_path, retrieval_metadata_sha256=hashlib.sha256((tmp_path / metadata_path).read_bytes()).hexdigest())
    ledger = queue.read_ledger(ROOT)
    for qid, q in Q.items():
        ledger[qid] = dict(question_id=qid, content_sha256=queue.digest(q), collection=adapter.BASE + '/questions.json',
            legal_review_status=native.STATUS, current_id_author_review_required=True, checked_at=None,
            author_review_increment=0, known_author_editor_actor_ids=[G, E])
    (tmp_path / 'reports/full-corpus-review/question-ledger.jsonl').write_text('\n'.join(json.dumps(r) for r in ledger.values()) + '\n')
    git(tmp_path, 'init', '-q')
    git(tmp_path, 'config', 'user.email', 'fixture@example.test')
    git(tmp_path, 'config', 'user.name', 'Synthetic Fixture')
    commit(tmp_path)
    return tmp_path, state, ledger, authority, static


def complete_author_job(repo, register=True):
    root, state, ledger, authority, static = repo
    queue.plan(state, ledger, root, size=3, at=NOW)
    job = queue.claim(state, G, at=NOW)
    actor = native.expected_actor(Q)
    records = []
    for qid, q in Q.items():
        records.append(dict(question_id=qid, record_sha256=queue.digest(q), checked_at='2026-11-04',
            disposition='KEEP', legal_review_status='AUTHOR_SOURCE_CHECKED_NOT_INDEPENDENT', blocker='',
            current_ID_stem_all_choices_key_all_Korean_explanations_read=True,
            author_expected_choice_ids=q['correct_choice_ids'], reviewer_provenance={**actor, 'independent': False},
            choice_by_choice_findings={c['id']: dict(original_choice_text=c['text'], expected_true=c['id'] in q['correct_choice_ids'],
                finding_ko='합성 테스트의 선택지별 판단이며 실제 법률 감사 자료가 아니다.', exact_authority='Synthetic test section',
                authorities=[copy.deepcopy(authority)]) for c in q['choices']}))
    report = dict(schema_version=native.SCHEMA, stage='author', job_id=job['job_id'], actor_provenance=actor,
        canonical_audit=False, canonical_release_credit=0, independent_of_authors=False, independent_review_credit=0,
        records=records)
    path = native.PREFIX + 'g-review.json'
    write(root, path, report)
    worker_commit = commit(root)
    report_sha = hashlib.sha256((root / path).read_bytes()).hexdigest()
    result = dict(stage='author', job_id=job['job_id'], actor_provenance=actor,
        canonical_audit=False, canonical_release_credit=0, independent_review_credit=0, independent_of_authors=False,
        question_hashes=job['question_hashes'], worker_commit=worker_commit,
        results=[dict(question_id=qid, disposition='AUTHOR_REVIEWED', evidence_path=path, evidence_sha256=report_sha) for qid in Q])
    queue.submit(state, job['job_id'], job['lease_token'], result, at=NOW)
    queue.integrate(state, job['job_id'], root, at=NOW)
    write(root, native.QUEUE, state)
    if register:
        write(root, native.REGISTRY, dict(schema_version='sata-remediation-native-author-sources/1',
            sources=[dict(job_id=job['job_id'], report_path=path, report_sha256=report_sha)]))
    commit(root)
    return job, report, path


def replace_report(repo, job, report, path):
    root, state, *_ = repo
    write(root, path, report)
    sha = hashlib.sha256((root / path).read_bytes()).hexdigest()
    for row in job['result']['results']: row['evidence_sha256'] = sha
    for event in state['events']:
        if event['kind'] == 'SUBMIT' and event.get('job_id') == job['job_id']:
            event['result_sha256'] = queue.digest(job['result'])
    write(root, native.QUEUE, state)
    write(root, native.REGISTRY, dict(schema_version='sata-remediation-native-author-sources/1',
        sources=[dict(job_id=job['job_id'], report_path=path, report_sha256=sha)]))
    commit(root)


def test_pending_candidates_are_author_only_credit_zero_and_G_can_claim(repo):
    root, state, ledger, _, static = repo
    assert native.load_sources(root, static) == {}
    assert queue.plan(state, ledger, root, size=3, at=NOW)
    assert list(state['jobs'][-1]['question_hashes']) == list(Q)
    assert state['jobs'][-1]['sequence'] == 53
    assert queue.plan(state, ledger, root, at=NOW) == []
    with pytest.raises(ValueError, match='Required content author'):
        queue.claim(state, E, at=NOW)
    assert queue.claim(state, G, at=NOW)['required_author_actor_id'] == G
    independent = queue.empty('independent-legacy')
    assert queue.plan(independent, {k: ledger[k] for k in Q}, root, size=3, at=NOW) == []
    for q in Q.values():
        row = {}
        adapter.bind_candidate_inventory_row(row, q, root)
        assert row['current_id_author_review_required'] and row['checked_at'] is None and row['author_review_increment'] == 0


def test_only_native_integrated_current_G_evidence_credits_and_rebind_keeps_it(repo):
    root, state, ledger, _, static = repo
    job, _, _ = complete_author_job(repo)
    sources = native.load_sources(root, static)
    assert len(sources) == 1
    reviewed = {}
    for qid, q in Q.items():
        row = dict(question_id=qid, collection=adapter.BASE + '/questions.json', content_sha256=queue.digest(q))
        adapter.bind_candidate_inventory_row(row, q, root)
        adapter.bind_candidate_inventory_row(row, q, root)
        assert row['author_review_increment'] == 1 and not row['current_id_author_review_required']
        assert row['checked_at_scope'] == 'FORMAL_NATIVE_CURRENT_ID_AUTHOR_REVIEW'
        assert row['independent_review_credit'] == row['canonical_release_credit'] == 0
        reviewed[qid] = row
    # Same author planner cannot reassign an integrated, credited ID.
    ledger.update(reviewed)
    assert queue.plan(state, ledger, root, at=NOW) == []
    independent = queue.empty('independent-legacy')
    queue.plan(independent, reviewed, root, size=3, at=NOW)
    for actor in (G, E):
        with pytest.raises(ValueError, match='author/editor cannot independently claim'):
            queue.claim(independent, actor, at=NOW)


def test_head_only_consumer_works_without_native_worker_commit_in_shallow_clone(repo, tmp_path):
    root, _, _, _, static = repo
    job, _, _ = complete_author_job(repo)
    clone = root.parent / (root.name + '-shallow')
    subprocess.run(['git', 'clone', '-q', '--depth', '1', root.as_uri(), str(clone)], check=True)
    assert subprocess.run(['git', '-C', str(clone), 'cat-file', '-e', job['result']['worker_commit'] + '^{commit}'], capture_output=True).returncode != 0
    assert len(native.load_sources(clone, static)) == 1


@pytest.mark.parametrize('mutation', ['not_integrated', 'no_claim_event', 'no_submit_event', 'old_job_changed'])
def test_unintegrated_or_missing_native_chain_cannot_credit(repo, mutation):
    root, state, _, _, static = repo
    job, _, _ = complete_author_job(repo)
    if mutation == 'not_integrated': job['status'] = 'SUBMITTED'
    elif mutation == 'old_job_changed': state['jobs'][0]['worker'] = 'invented'
    else:
        kind = 'CLAIM' if mutation == 'no_claim_event' else 'SUBMIT'
        state['events'] = [e for e in state['events'] if not (e['kind'] == kind and e.get('job_id') == job['job_id'])]
    write(root, native.QUEUE, state)
    commit(root)
    with pytest.raises(ValueError): native.load_sources(root, static)


@pytest.mark.parametrize('mutation', ['other_id', 'fake_actor', 'bad_current_hash', 'no_author_read', 'missing_choice', 'false_independence'])
def test_narrow_consumer_refuses_report_injection_or_metadata_only_confirmation(repo, mutation):
    root, _, _, _, static = repo
    job, report, path = complete_author_job(repo)
    if mutation == 'other_id': report['records'][0]['question_id'] = 'MA-EXP-0001'
    elif mutation == 'fake_actor': report['actor_provenance']['actor_id'] = E
    elif mutation == 'bad_current_hash': report['records'][0]['record_sha256'] = '0' * 64
    elif mutation == 'no_author_read': report['records'][0]['current_ID_stem_all_choices_key_all_Korean_explanations_read'] = False
    elif mutation == 'missing_choice': report['records'][0]['choice_by_choice_findings'].pop('A')
    else: report['independent_of_authors'] = True
    replace_report(repo, job, report, path)
    with pytest.raises(ValueError): native.load_sources(root, static)


def test_old_source_and_uncommitted_source_changes_fail(repo):
    root, _, _, _, static = repo
    complete_author_job(repo)
    old = root / 'reports/full-corpus-review' / static[0]
    old.write_text('{}')
    with pytest.raises(ValueError, match='Original static author source bytes changed'):
        native.load_sources(root, static)


@pytest.mark.parametrize('mutation', ['wrong_document_200', 'http403'])
def test_failed_or_wrong_document_never_supports_KEEP(repo, mutation):
    root, _, _, _, static = repo
    job, report, path = complete_author_job(repo)
    for review in report['records']:
        for finding in review['choice_by_choice_findings'].values():
            for authority in finding['authorities']:
                if mutation == 'wrong_document_200': authority['body_verified_current_primary'] = False
                else:
                    authority['http_status'] = 403
                    write(root, authority['retrieval_metadata_path'], dict(official_url=authority['official_url'], raw_sha256=authority['raw_sha256'], http_status=403))
                    authority['retrieval_metadata_sha256'] = hashlib.sha256((root / authority['retrieval_metadata_path']).read_bytes()).hexdigest()
    replace_report(repo, job, report, path)
    with pytest.raises(ValueError, match='Failed/wrong source cannot prove'):
        native.load_sources(root, static)


def test_held_failed_source_records_read_review_without_legal_PASS_or_key_certification(repo):
    root, _, _, _, static = repo
    job, report, path = complete_author_job(repo)
    for record in report['records']:
        record.update(disposition='SOURCE_BLOCKED', legal_review_status='AUTHOR_CURRENT_ID_SOURCE_BLOCKED',
                      blocker='합성 fixture의 실패 원문을 법적 proof로 쓰지 않는다.', author_expected_choice_ids=None)
        for finding in record['choice_by_choice_findings'].values():
            finding['expected_true'] = None
            for authority in finding['authorities']:
                authority.update(http_status=403, body_verified_current_primary=False,
                                 used_as_legal_proof=False, failure_reason='Synthetic fixture HTTP403')
                write(root, authority['retrieval_metadata_path'], dict(official_url=authority['official_url'],
                    raw_sha256=authority['raw_sha256'], http_status=403))
                authority['retrieval_metadata_sha256'] = hashlib.sha256((root / authority['retrieval_metadata_path']).read_bytes()).hexdigest()
    for row in job['result']['results']: row['disposition'] = 'SOURCE_BLOCKED'
    replace_report(repo, job, report, path)
    sources = native.load_sources(root, static)
    row = {}
    native.apply_review(row, next(iter(Q.values())), root)
    assert row['disposition'] == 'SOURCE_BLOCKED'
    assert row['answer_key_assessment'] == 'NOT_ASSESSED_SOURCE_BLOCKED'
    assert row['author_review_increment'] == 1
    assert row['independent_review_credit'] == row['canonical_release_credit'] == 0


def test_author_required_flag_cannot_inject_an_unallocated_fourth_ID(repo):
    root, state, ledger, *_ = repo
    ledger['MA-RW-0099'] = {**ledger['MA-RW-0081'], 'question_id': 'MA-RW-0099'}
    with pytest.raises(ValueError, match='exactly the three allocated candidates'):
        queue.plan(state, ledger, root, size=3, at=NOW)


def test_actual_compiled_candidate_object_cannot_change_under_allocated_ID(repo, monkeypatch):
    root, *_ = repo
    monkeypatch.setattr(native, 'candidate_records', REAL_CANDIDATE_RECORDS)
    assert set(native.candidate_records(root)) == set(Q)
    bank = json.loads((root / adapter.BASE / 'questions.json').read_bytes())
    bank['questions'][0]['stem'] += ' Changed material fact.'
    write(root, adapter.BASE + '/questions.json', bank)
    with pytest.raises(ValueError, match='current-record hash changed'):
        native.candidate_records(root)
