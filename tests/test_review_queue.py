"""Queue safety: exclusive ownership, crash recovery, and evidence-bound integration."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import review_queue as queue

NOW = '2026-11-03T12:00:00+00:00'
LATER = '2026-11-03T14:00:00+00:00'


def fixture_repo(tmp_path):
    questions = [{'question_id': qid, 'stem': qid} for qid in queue.FIRST + ['MA-EXP-0001', 'MA-EXP-0900']]
    (tmp_path / 'questions.json').write_text(json.dumps({'questions': questions}))
    ledger = {q['question_id']: {'question_id': q['question_id'], 'collection': 'questions.json',
              'content_sha256': queue.digest(q), 'legal_review_status': queue.UNREVIEWED,
              'checked_at': None} for q in questions}
    path = tmp_path / 'reports/full-corpus-review'
    path.mkdir(parents=True)
    (path / 'question-ledger.jsonl').write_text('\n'.join(json.dumps(r) for r in ledger.values()))
    return ledger


def initial(tmp_path):
    ledger = fixture_repo(tmp_path)
    state = queue.empty()
    queue.plan(state, ledger, tmp_path, at=NOW)
    return state, ledger


def test_fixed_first_then_ledger_based_nonsequential_batches(tmp_path):
    state, ledger = initial(tmp_path)
    assert list(state['jobs'][0]['question_hashes']) == queue.FIRST
    assert queue.plan(state, ledger, tmp_path, batches=4, at=NOW) == []
    state['jobs'][0]['status'] = 'INTEGRATED'
    ledger['MA-EXP-0001']['legal_review_status'] = 'AUTHOR_SOURCE_CHECKED_NOT_INDEPENDENT'
    created = queue.plan(state, ledger, tmp_path, batches=4, at=NOW)
    assert len(created) == 1
    assert list(state['jobs'][1]['question_hashes']) == ['MA-EXP-0900']


def test_distinct_workers_receive_disjoint_assignments(tmp_path):
    state, ledger = initial(tmp_path)
    state['jobs'][0]['status'] = 'INTEGRATED'
    queue.plan(state, ledger, tmp_path, batches=4, size=1, at=NOW)
    first = queue.claim(state, 'one', at=NOW)
    second = queue.claim(state, 'two', at=NOW)
    assert not set(first['question_hashes']) & set(second['question_hashes'])
    assert queue.claim(state, 'one', at=NOW) == first
    assert first['worker_branch'] != second['worker_branch']


def test_stale_worker_cannot_submit_after_recovery(tmp_path):
    state, _ = initial(tmp_path)
    job = queue.claim(state, 'crashed', at=NOW)
    old_token = job['lease_token']
    queue.recover(state, LATER)
    job = queue.claim(state, 'replacement', at=LATER)
    assert job['attempt'] == 2
    assert job['lease_token'] != old_token
    with pytest.raises(ValueError, match='Stale'):
        queue.require_lease(job, old_token, LATER)


def result_for(job):
    return {'question_hashes': copy.deepcopy(job['question_hashes']), 'worker_commit': 'a'*40,
            'results': [{'question_id': qid, 'disposition': 'SOURCE_BLOCKED',
                         'evidence_path': 'reports/results.json', 'evidence_sha256': 'b'*64}
                        for qid in job['question_hashes']]}


def test_completion_idempotent_but_conflicts_and_missing_ids_fail(tmp_path):
    state, _ = initial(tmp_path)
    job = queue.claim(state, 'worker', at=NOW)
    result = result_for(job)
    missing = copy.deepcopy(result); missing['results'].pop()
    with pytest.raises(ValueError, match='Every assigned'):
        queue.submit(state, job['job_id'], job['lease_token'], missing, NOW)
    queue.submit(state, job['job_id'], job['lease_token'], result, NOW)
    queue.submit(state, job['job_id'], job['lease_token'], result, NOW)
    changed = copy.deepcopy(result); changed['results'][0]['disposition'] = 'HOLD'
    with pytest.raises(ValueError, match='Conflicting'):
        queue.submit(state, job['job_id'], job['lease_token'], changed, NOW)
    assert len([e for e in state['events'] if e['kind'] == 'SUBMIT']) == 1


def test_expired_lease_and_unsafe_report_paths_fail(tmp_path):
    state, _ = initial(tmp_path)
    job = queue.claim(state, 'worker', at=NOW)
    with pytest.raises(ValueError, match='expired'):
        queue.submit(state, job['job_id'], job['lease_token'], result_for(job), LATER)
    result = result_for(job); result['results'][0]['evidence_path'] = '../outside'
    with pytest.raises(ValueError, match='relative'):
        queue.validate_result(job, result)


def test_stale_generated_ledger_fails_assignment(tmp_path):
    _, ledger = initial(tmp_path)
    bank = json.loads((tmp_path / 'questions.json').read_text())
    bank['questions'][0]['stem'] = 'modified'
    (tmp_path / 'questions.json').write_text(json.dumps(bank))
    with pytest.raises(ValueError, match='Stale ledger'):
        queue.plan(queue.empty(), ledger, tmp_path, at=NOW)


def test_crash_does_not_partially_write_checkpoint(tmp_path):
    path = tmp_path / 'queue.json'
    with queue.checkpoint(path) as state:
        state['events'].append({'first': True})
    before = path.read_bytes()
    with pytest.raises(RuntimeError):
        with queue.checkpoint(path) as state:
            state['events'].append({'uncommitted': True})
            raise RuntimeError('crash')
    assert path.read_bytes() == before


def test_heartbeat_requires_live_owner(tmp_path):
    state, _ = initial(tmp_path)
    job = queue.claim(state, 'worker', at=NOW)
    queue.heartbeat(state, job['job_id'], job['lease_token'], minutes=120, at=NOW)
    assert job['lease_until'] == LATER
    with pytest.raises(ValueError, match='Stale'):
        queue.heartbeat(state, job['job_id'], 'wrong', at=NOW)


def test_integration_requires_committed_exact_worker_evidence(tmp_path):
    state, _ = initial(tmp_path)
    job = queue.claim(state, 'worker', at=NOW)
    report = tmp_path / 'reports/results.json'
    report.write_text('{"blocker":"공식 원문 확인 필요"}\n')
    subprocess.run(['git', 'init', '-q', str(tmp_path)], check=True)
    def git(*args):
        return subprocess.check_output(['git', '-C', str(tmp_path), *args], text=True).strip()
    git('config', 'user.email', 'test@example.test'); git('config', 'user.name', 'Test')
    git('add', '.'); git('commit', '-qm', 'worker evidence')
    result = result_for(job); result['worker_commit'] = git('rev-parse', 'HEAD')
    for row in result['results']:
        row['evidence_sha256'] = hashlib.sha256(report.read_bytes()).hexdigest()
    queue.submit(state, job['job_id'], job['lease_token'], result, NOW)
    report.write_text('changed')
    with pytest.raises(ValueError, match='evidence'):
        queue.integrate(state, job['job_id'], tmp_path, NOW)
    git('checkout', '--', 'reports/results.json')
    queue.integrate(state, job['job_id'], tmp_path, NOW)
    assert job['status'] == 'INTEGRATED'
    queue.integrate(state, job['job_id'], tmp_path, NOW)
    assert len([e for e in state['events'] if e['kind'] == 'INTEGRATE']) == 1


def test_integration_order_guard_and_no_release_credit(tmp_path):
    state, ledger = initial(tmp_path)
    second = copy.deepcopy(state['jobs'][0]); second.update(job_id='second', sequence=2, status='SUBMITTED')
    state['jobs'].append(second)
    with pytest.raises(ValueError, match='assignment order'):
        queue.integrate(state, 'second', tmp_path, NOW)
    status = queue.progress(state, ledger, {'notes_units_with_complete_atomic_claim_census': 0,
                    'notes_units': 306, 'deployment_status': 'NOT_RUN'})
    assert status['author_review']['percent'] == 0
    assert status['independent_legal_audit']['percent'] is None
    assert status['verified_deployment']['status'] == 'NOT_RUN'


def append_checkpoint(path, n):
    with queue.checkpoint(Path(path)) as state:
        state['events'].append({'writer': n})


def test_competing_controller_processes_do_not_lose_updates(tmp_path):
    import multiprocessing
    path = tmp_path / 'queue.json'
    context = multiprocessing.get_context('fork')
    processes = [context.Process(target=append_checkpoint, args=(str(path), n)) for n in range(8)]
    for process in processes:
        process.start()
    for process in processes:
        process.join(10)
        assert process.exitcode == 0
    assert {r['writer'] for r in json.loads(path.read_text())['events']} == set(range(8))


def test_recovered_attempt_uses_a_new_worktree_branch(tmp_path):
    state, _ = initial(tmp_path)
    job = queue.claim(state, 'first', at=NOW)
    original_branch = job['worker_branch']
    queue.recover(state, LATER)
    job = queue.claim(state, 'second', at=LATER)
    assert job['worker_branch'] != original_branch
    assert job['worker_branch'].endswith('-attempt-2')


def test_real_worktree_matches_assigned_branch_and_is_idempotent(tmp_path):
    root = tmp_path / 'repo'; root.mkdir()
    state, _ = initial(root)
    subprocess.run(['git', 'init', '-q', str(root)], check=True)
    queue.git(root, 'config', 'user.email', 'test@example.test')
    queue.git(root, 'config', 'user.name', 'Test')
    queue.git(root, 'add', '.')
    queue.git(root, 'commit', '-qm', 'baseline')
    job = queue.claim(state, 'worker', at=NOW)
    destination = tmp_path / 'worker'
    queue.prepare_worktree(state, job['job_id'], job['lease_token'], root, destination, NOW)
    assert queue.git(destination, 'branch', '--show-current') == job['worker_branch']
    queue.prepare_worktree(state, job['job_id'], job['lease_token'], root, destination, NOW)
    with pytest.raises(ValueError, match='another worker'):
        queue.prepare_worktree(state, job['job_id'], job['lease_token'], root, root, NOW)
