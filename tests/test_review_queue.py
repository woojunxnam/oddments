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
    for qid in queue.FIRST:
        ledger[qid].update(legal_review_status='AUTHOR_SOURCE_CHECKED_NOT_INDEPENDENT', checked_at=NOW)
    ledger['MA-EXP-0001']['legal_review_status'] = 'AUTHOR_SOURCE_CHECKED_NOT_INDEPENDENT'
    created = queue.plan(state, ledger, tmp_path, batches=4, at=NOW)
    assert len(created) == 1
    assert list(state['jobs'][1]['question_hashes']) == ['MA-EXP-0900']


def test_distinct_workers_receive_disjoint_assignments(tmp_path):
    state, ledger = initial(tmp_path)
    state['jobs'][0]['status'] = 'INTEGRATED'
    for qid in queue.FIRST:
        ledger[qid].update(legal_review_status='AUTHOR_SOURCE_CHECKED_NOT_INDEPENDENT', checked_at=NOW)
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
    result = {'question_hashes': copy.deepcopy(job['question_hashes']), 'worker_commit': 'a'*40,
            'results': [{'question_id': qid, 'disposition': 'SOURCE_BLOCKED',
                         'evidence_path': 'reports/results.json', 'evidence_sha256': 'b'*64}
                        for qid in job['question_hashes']]}
    if job.get('stage') == 'independent-legacy':
        result.update(stage='independent-legacy', independent_of_authors=True,
                      auditor='GPT', auditor_instance='actual-independent-session',
                      actor_provenance={'actor_id': job['worker'], 'session_id': 'actual-session-id'})
    return result


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


def test_integrated_manifest_without_authoritative_review_cannot_hide_unreviewed_ids(tmp_path):
    state, ledger = initial(tmp_path)
    state['jobs'][0]['status'] = 'INTEGRATED'
    with pytest.raises(ValueError, match='lack authoritative review credit'):
        queue.plan(state, ledger, tmp_path, batches=4, at=NOW)
    assert len(state['jobs']) == 1


def independent_initial(tmp_path, size=1):
    ledger = fixture_repo(tmp_path)
    for qid in ['MA-EXP-0001', 'MA-EXP-0900']:
        ledger[qid].update(legal_review_status='AUTHOR_SOURCE_CHECKED_NOT_INDEPENDENT', checked_at=NOW)
    state = queue.empty('independent-legacy')
    queue.plan(state, ledger, tmp_path, size=size, at=NOW)
    return state, ledger


def test_author_identifiers_and_state_remain_backward_compatible(tmp_path):
    state, _ = initial(tmp_path)
    assert queue.empty() == {'schema_version': 1,
        'purpose': 'AUTHOR_WORK_SCHEDULER_NOT_RELEASE_CERTIFICATION', 'jobs': [], 'events': []}
    job = state['jobs'][0]
    expected_id = 'review-' + queue.digest(job['question_hashes'])[:16]
    assert job['job_id'] == expected_id
    assert 'stage' not in job
    assert state['events'] == [{'kind': 'PLAN', 'at': NOW, 'job_ids': [expected_id]}]
    job = queue.claim(state, 'existing-worker', at=NOW)
    assert job['lease_token'] == queue.digest({'job': expected_id, 'worker': 'existing-worker',
                                               'attempt': 1, 'at': NOW})


def test_independent_eligibility_is_sorted_from_authoritative_ledger_not_first_cohort(tmp_path):
    ledger = fixture_repo(tmp_path)
    state = queue.empty('independent-legacy')
    assert queue.plan(state, ledger, tmp_path, at=NOW) == []
    for qid in ['MA-EXP-0900', 'MA-EXP-0385', 'MA-EXP-0001']:
        ledger[qid]['checked_at'] = NOW
    ledger['MA-EXP-0385']['independent_legacy_legal_assessment'] = {'existing_answer_correct': 'NO'}
    queue.plan(state, ledger, tmp_path, batches=4, size=1, at=NOW)
    assert [list(j['question_hashes']) for j in state['jobs']] == [['MA-EXP-0001'], ['MA-EXP-0900']]
    assert queue.plan(state, ledger, tmp_path, batches=4, at=NOW) == []
    first = queue.claim(state, 'independent-one', at=NOW)
    second = queue.claim(state, 'independent-two', at=NOW)
    assert not set(first['question_hashes']) & set(second['question_hashes'])
    assert queue.claim(state, 'independent-one', at=NOW) is first


def test_stages_can_assign_same_ids_without_job_or_branch_collision(tmp_path):
    author, ledger = initial(tmp_path)
    for qid in queue.FIRST:
        ledger[qid]['checked_at'] = NOW
    independent = queue.empty('independent-legacy')
    queue.plan(independent, ledger, tmp_path, at=NOW)
    a, i = author['jobs'][0], independent['jobs'][0]
    assert a['question_hashes'] == i['question_hashes']
    assert i['job_id'] == 'review-independent-legacy-' + queue.digest(i['question_hashes'])[:16]
    assert a['job_id'] != i['job_id']
    assert a['worker_branch'] != i['worker_branch']


def test_independent_integrated_job_waits_for_independent_ledger_assessment(tmp_path):
    state, ledger = independent_initial(tmp_path)
    job = state['jobs'][0]
    job['status'] = 'INTEGRATED'
    # Author checked_at alone must never authorize the next independent wave.
    with pytest.raises(ValueError, match='lack authoritative independent legacy assessment'):
        queue.plan(state, ledger, tmp_path, at=NOW)
    assert len(state['jobs']) == 1
    ledger['MA-EXP-0001']['independent_legacy_legal_assessment'] = {'existing_answer_correct': 'NOT_ASSESSED'}
    queue.plan(state, ledger, tmp_path, at=NOW)
    assert list(state['jobs'][1]['question_hashes']) == ['MA-EXP-0900']
    ledger.pop('MA-EXP-0001')
    state['jobs'][1]['status'] = 'INTEGRATED'
    ledger['MA-EXP-0900']['independent_legacy_legal_assessment'] = {'existing_answer_correct': 'YES'}
    with pytest.raises(ValueError, match='lack authoritative independent legacy assessment'):
        queue.plan(state, ledger, tmp_path, at=NOW)


def test_independent_assignment_rejects_stale_current_record(tmp_path):
    state, ledger = independent_initial(tmp_path)
    bank = json.loads((tmp_path / 'questions.json').read_text())
    next(q for q in bank['questions'] if q['question_id'] == 'MA-EXP-0001')['stem'] = 'changed'
    (tmp_path / 'questions.json').write_text(json.dumps(bank))
    with pytest.raises(ValueError, match='Stale ledger'):
        queue.plan(queue.empty('independent-legacy'), ledger, tmp_path, at=NOW)


def test_independent_stale_recovery_fences_old_actor_and_is_idempotent(tmp_path):
    state, _ = independent_initial(tmp_path)
    job = queue.claim(state, 'original-independent-actor', at=NOW)
    token, branch = job['lease_token'], job['worker_branch']
    old_result = result_for(job)
    queue.heartbeat(state, job['job_id'], token, minutes=60, at=NOW)
    assert queue.recover(state, LATER) == [job['job_id']]
    assert queue.recover(state, LATER) == []
    job = queue.claim(state, 'replacement-independent-actor', at=LATER)
    assert job['attempt'] == 2
    assert job['worker_branch'] != branch
    with pytest.raises(ValueError, match='Stale'):
        queue.heartbeat(state, job['job_id'], token, at=LATER)
    result = result_for(job)
    with pytest.raises(ValueError, match='Stale'):
        queue.submit(state, job['job_id'], token, result, LATER)
    with pytest.raises(ValueError, match='actor provenance'):
        queue.submit(state, job['job_id'], job['lease_token'], old_result, LATER)
    queue.submit(state, job['job_id'], job['lease_token'], result, LATER)
    queue.submit(state, job['job_id'], job['lease_token'], result, LATER)
    assert sum(e['kind'] == 'SUBMIT' for e in state['events']) == 1
    assert queue.recover(state, '2026-11-04T14:00:00+00:00') == []


@pytest.mark.parametrize('disposition', sorted(queue.INDEPENDENT_DISPOSITIONS))
def test_independent_uses_own_dispositions_without_author_credit(tmp_path, disposition):
    state, ledger = independent_initial(tmp_path)
    original_ledger = copy.deepcopy(ledger)
    job = queue.claim(state, 'independent-actor', at=NOW)
    result = result_for(job)
    result['results'][0]['disposition'] = disposition
    queue.submit(state, job['job_id'], job['lease_token'], result, NOW)
    assert ledger == original_ledger
    assert not any(r['disposition'] == 'AUTHOR_REVIEWED' for r in job['result']['results'])


@pytest.mark.parametrize('change,match', [
    ({'stage': 'author'}, 'stage'),
    ({'independent_of_authors': False}, 'independent_of_authors'),
    ({'independent_of_authors': 'true'}, 'independent_of_authors'),
    ({'actor_provenance': {}}, 'actor provenance'),
    ({'actor_provenance': {'actor_id': 'somebody-else', 'session_id': 'actual-session'}}, 'actor provenance'),
    ({'auditor_instance': ''}, 'actor provenance'),
    ({'auditor': ''}, 'actor provenance'),
])
def test_independent_submission_rejects_missing_or_conflicting_provenance(tmp_path, change, match):
    state, _ = independent_initial(tmp_path)
    job = queue.claim(state, 'independent-actor', at=NOW)
    result = result_for(job); result.update(change)
    with pytest.raises(ValueError, match=match):
        queue.submit(state, job['job_id'], job['lease_token'], result, NOW)
    assert job['status'] == 'LEASED'


def test_submissions_cannot_cross_stages_or_make_author_classification_independent(tmp_path):
    state, ledger = independent_initial(tmp_path)
    job = queue.claim(state, 'independent-actor', at=NOW)
    result = result_for(job)
    result['results'][0]['disposition'] = 'AUTHOR_REVIEWED'
    with pytest.raises(ValueError, match='disposition'):
        queue.submit(state, job['job_id'], job['lease_token'], result, NOW)
    result = result_for(job); result.pop('stage')
    with pytest.raises(ValueError, match='stage'):
        queue.submit(state, job['job_id'], job['lease_token'], result, NOW)
    author = queue.empty(); queue.plan(author, ledger, tmp_path, at=NOW)
    author_job = queue.claim(author, 'author-actor', at=NOW)
    result = result_for(author_job); result['stage'] = 'independent-legacy'
    with pytest.raises(ValueError, match='stage'):
        queue.submit(author, author_job['job_id'], author_job['lease_token'], result, NOW)


def test_stage_specific_paths_purposes_and_rejection_preserve_checkpoint(tmp_path):
    author = queue.state_path(tmp_path, 'author')
    independent = queue.state_path(tmp_path, 'independent-legacy')
    assert author == tmp_path / 'reports/full-corpus-review/work-queue.json'
    assert independent == tmp_path / 'reports/full-corpus-review/independent-legacy-work-queue.json'
    assert queue.empty('independent-legacy')['purpose'] == 'INDEPENDENT_LEGACY_WORK_SCHEDULER_NOT_RELEASE_CERTIFICATION'
    for stage, wrong_path in [('author', independent), ('independent-legacy', author)]:
        with pytest.raises(ValueError, match='Stage/state path'):
            queue.state_path(tmp_path, stage, wrong_path)
    custom = tmp_path / 'custom.json'
    with queue.checkpoint(custom, 'independent-legacy') as state:
        state['events'].append({'actual': True})
    before = custom.read_bytes()
    with pytest.raises(ValueError, match='Stage/state purpose'):
        with queue.checkpoint(custom):
            pytest.fail('wrong stage must not receive writable checkpoint')
    assert custom.read_bytes() == before
    state = json.loads(before)
    state['jobs'].append({'stage': 'author'})
    with pytest.raises(ValueError, match='Job stage'):
        queue.recover(state, NOW)


def test_cli_stage_defaults_and_wrong_checkpoint_cannot_mutate_state(tmp_path):
    _, ledger = independent_initial(tmp_path)
    ledger_path = tmp_path / 'reports/full-corpus-review/question-ledger.jsonl'
    ledger_path.write_text('\n'.join(json.dumps(row) for row in ledger.values()))
    command = [sys.executable, str(Path(queue.__file__)), '--root', str(tmp_path)]
    run = subprocess.run(command + ['--stage', 'independent-legacy', 'plan', '--size', '1'],
                         text=True, capture_output=True, check=True)
    ids = json.loads(run.stdout)
    independent = queue.state_path(tmp_path, 'independent-legacy')
    state = json.loads(independent.read_text())
    assert ids == [state['jobs'][0]['job_id']]
    assert not queue.state_path(tmp_path, 'author').exists()
    before = independent.read_bytes()
    run = subprocess.run(command + ['--state', str(independent), 'recover'], text=True, capture_output=True)
    assert run.returncode != 0
    assert 'Stage/state path mismatch' in run.stderr
    assert independent.read_bytes() == before
    custom = tmp_path / 'custom.json'; custom.write_bytes(before)
    run = subprocess.run(command + ['--state', str(custom), 'recover'], text=True, capture_output=True)
    assert run.returncode != 0
    assert 'Stage/state purpose mismatch' in run.stderr
    assert custom.read_bytes() == before


def independent_evidence(job):
    manifest = result_for(job)
    return {key: manifest[key] for key in ('independent_of_authors', 'auditor',
            'auditor_instance', 'actor_provenance')} | {
        'canonical_audit': False, 'canonical_release_credit': 0,
        'records': [{'question_id': qid, 'record_sha256': hash_value,
                     'legal_review': {'existing_answer_correct': 'NOT_ASSESSED',
                                      'blocker': 'Current official source unavailable'}}
                    for qid, hash_value in job['question_hashes'].items()]}


@pytest.mark.parametrize('defect', [None, 'no_independence', 'missing_actor', 'different_session',
                                  'wrong_hash', 'missing_record', 'duplicate_record', 'release_claim'])
def test_independent_integration_checks_committed_evidence_provenance_and_record_hashes(tmp_path, defect):
    state, _ = independent_initial(tmp_path)
    job = queue.claim(state, 'actual-independent-actor', at=NOW)
    report = independent_evidence(job)
    if defect == 'no_independence': report['independent_of_authors'] = False
    elif defect == 'missing_actor': report.pop('actor_provenance')
    elif defect == 'different_session': report['auditor_instance'] = 'different-session'
    elif defect == 'wrong_hash': report['records'][0]['record_sha256'] = '0' * 64
    elif defect == 'missing_record': report['records'] = []
    elif defect == 'duplicate_record': report['records'] *= 2
    elif defect == 'release_claim': report['canonical_release_credit'] = 1
    path = tmp_path / 'reports/results.json'; path.write_text(json.dumps(report))
    subprocess.run(['git', 'init', '-q', str(tmp_path)], check=True)
    queue.git(tmp_path, 'config', 'user.email', 'test@example.test')
    queue.git(tmp_path, 'config', 'user.name', 'Test')
    queue.git(tmp_path, 'add', '.'); queue.git(tmp_path, 'commit', '-qm', 'independent source evidence')
    result = result_for(job); result['worker_commit'] = queue.git(tmp_path, 'rev-parse', 'HEAD')
    result['results'][0]['evidence_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    queue.submit(state, job['job_id'], job['lease_token'], result, NOW)
    if defect:
        with pytest.raises(ValueError):
            queue.integrate(state, job['job_id'], tmp_path, NOW)
        assert job['status'] == 'SUBMITTED'
    else:
        queue.integrate(state, job['job_id'], tmp_path, NOW)
        queue.integrate(state, job['job_id'], tmp_path, NOW)
        assert job['status'] == 'INTEGRATED'
        assert sum(e['kind'] == 'INTEGRATE' for e in state['events']) == 1
        with pytest.raises(ValueError, match='lack authoritative independent legacy assessment'):
            queue.plan(state, queue.read_ledger(tmp_path), tmp_path, at=NOW)


def test_independent_integration_stays_sequential(tmp_path):
    ledger = fixture_repo(tmp_path)
    for qid in ['MA-EXP-0001', 'MA-EXP-0900']:
        ledger[qid]['checked_at'] = NOW
    state = queue.empty('independent-legacy')
    queue.plan(state, ledger, tmp_path, batches=2, size=1, at=NOW)
    queue.claim(state, 'first-actor', at=NOW)
    second = queue.claim(state, 'second-actor', at=NOW)
    queue.submit(state, second['job_id'], second['lease_token'], result_for(second), NOW)
    with pytest.raises(ValueError, match='assignment order'):
        queue.integrate(state, second['job_id'], tmp_path, NOW)
