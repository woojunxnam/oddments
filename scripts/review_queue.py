"""Single-writer, Git-persisted review scheduling. This is not release evidence."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / 'reports/full-corpus-review/work-queue.json'
UNREVIEWED = 'NOT_REVERIFIED_IN_FULL_CORPUS_REVIEW'
FIRST = [f'MA-EXP-{i:04d}' for i in range(385, 425)]
DISPOSITIONS = {'AUTHOR_REVIEWED', 'HOLD', 'SOURCE_BLOCKED', 'NEEDS_REMEDIATION'}


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def read_ledger(root):
    rows = [json.loads(line) for line in
            (root / 'reports/full-corpus-review/question-ledger.jsonl').read_text().splitlines()]
    if len({r['question_id'] for r in rows}) != len(rows):
        raise ValueError('Duplicate authoritative ledger IDs')
    return {r['question_id']: r for r in rows}


def current_hash(root, row):
    """Check actual collection too; a stale generated ledger cannot authorize work."""
    bank = json.loads((root / row['collection']).read_text())
    found = [q for q in bank['questions'] if q['question_id'] == row['question_id']]
    if len(found) != 1 or digest(found[0]) != row['content_sha256']:
        raise ValueError('Stale ledger content: ' + row['question_id'])
    return row['content_sha256']


def empty():
    return {'schema_version': 1, 'purpose': 'AUTHOR_WORK_SCHEDULER_NOT_RELEASE_CERTIFICATION',
            'jobs': [], 'events': []}


@contextmanager
def checkpoint(path):
    """Controller processes serialize writes; workers never mutate this file directly."""
    path.parent.mkdir(parents=True, exist_ok=True)
    # Lock lives in /tmp, not tracked or regenerated output. Same realpath => same lock.
    lock_path = Path(tempfile.gettempdir()) / ('mpje-queue-' +
        hashlib.sha256(str(path.resolve()).encode()).hexdigest() + '.lock')
    with lock_path.open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        state = json.loads(path.read_text()) if path.exists() else empty()
        original = json.dumps(state, sort_keys=True)
        yield state
        if json.dumps(state, sort_keys=True) != original:
            fd, temporary = tempfile.mkstemp(dir=path.parent, prefix='.queue-')
            try:
                with os.fdopen(fd, 'w') as out:
                    json.dump(state, out, ensure_ascii=False, indent=2)
                    out.write('\n')
                    out.flush()
                    os.fsync(out.fileno())
                os.replace(temporary, path)
            finally:
                if os.path.exists(temporary):
                    os.unlink(temporary)


def event(state, kind, at, **fields):
    state['events'].append({'kind': kind, 'at': at, **fields})


def plan(state, ledger, root, batches=1, size=40, at=None):
    if not 1 <= batches <= 4 or not 1 <= size <= 40:
        raise ValueError('Use 1–4 batches of 1–40 IDs')
    at = at or timestamp()
    if not state['jobs']:
        groups = [FIRST]
        if any(qid not in ledger or ledger[qid]['legal_review_status'] != UNREVIEWED for qid in FIRST):
            raise ValueError('First cohort changed; reconcile ledger rather than assuming missing IDs')
    else:
        if any(j['status'] != 'INTEGRATED' for j in state['jobs']):
            return []  # retrying plan never duplicates outstanding assignments
        assigned = {qid for j in state['jobs'] for qid in j['question_hashes']}
        candidates = sorted(qid for qid, row in ledger.items()
                            if row['legal_review_status'] == UNREVIEWED and qid not in assigned)
        groups = [candidates[i:i+size] for i in range(0, min(len(candidates), batches*size), size)]
    created = []
    for group in groups:
        hashes = {qid: current_hash(root, ledger[qid]) for qid in group}
        job_id = 'review-' + digest(hashes)[:16]
        job = {'job_id': job_id, 'sequence': len(state['jobs']) + 1,
               'question_hashes': hashes, 'status': 'QUEUED', 'attempt': 0,
               'worker_branch': 'mission/' + job_id, 'created_at': at}
        state['jobs'].append(job)
        created.append(job_id)
    if created:
        event(state, 'PLAN', at, job_ids=created)
    return created


def recover(state, at=None):
    at = at or timestamp()
    recovered = []
    for job in state['jobs']:
        if job['status'] == 'LEASED' and datetime.fromisoformat(job['lease_until']) <= datetime.fromisoformat(at):
            job['status'] = 'QUEUED'
            recovered.append(job['job_id'])
            event(state, 'LEASE_EXPIRED', at, job_id=job['job_id'], attempt=job['attempt'])
    return recovered


def claim(state, worker, minutes=60, at=None):
    if not worker.strip() or not 1 <= minutes <= 1440:
        raise ValueError('Worker and 1–1440 lease minutes required')
    at = at or timestamp()
    recover(state, at)
    active = [j for j in state['jobs'] if j['status'] == 'LEASED' and j['worker'] == worker]
    if active:
        return active[0]  # idempotent reconnect, not another assignment
    queued = next((j for j in state['jobs'] if j['status'] == 'QUEUED'), None)
    if queued is None:
        return None
    queued.update(status='LEASED', worker=worker, attempt=queued['attempt'] + 1,
                  lease_until=(datetime.fromisoformat(at) + timedelta(minutes=minutes)).isoformat())
    queued['worker_branch'] = 'mission/' + queued['job_id'] + '-attempt-' + str(queued['attempt'])
    queued['lease_token'] = digest({'job': queued['job_id'], 'worker': worker,
                                    'attempt': queued['attempt'], 'at': at})
    event(state, 'CLAIM', at, job_id=queued['job_id'], worker=worker, attempt=queued['attempt'])
    return queued


def get_job(state, job_id):
    return next(j for j in state['jobs'] if j['job_id'] == job_id)


def require_lease(job, token, at):
    if job['status'] != 'LEASED' or job['lease_token'] != token:
        raise ValueError('Stale or absent lease token')
    if datetime.fromisoformat(job['lease_until']) <= datetime.fromisoformat(at):
        raise ValueError('Lease expired; reclaim before submission')


def heartbeat(state, job_id, token, minutes=60, at=None):
    at = at or timestamp()
    job = get_job(state, job_id)
    require_lease(job, token, at)
    if not 1 <= minutes <= 1440:
        raise ValueError('Use 1–1440 minutes')
    job['lease_until'] = (datetime.fromisoformat(at) + timedelta(minutes=minutes)).isoformat()
    event(state, 'HEARTBEAT', at, job_id=job_id, attempt=job['attempt'])


def prepare_worktree(state, job_id, token, root, destination, at=None):
    job = get_job(state, job_id)
    require_lease(job, token, at or timestamp())
    if destination.exists():
        if git(destination, 'branch', '--show-current') != job['worker_branch']:
            raise ValueError('Destination belongs to another worker branch')
        return str(destination)
    git(root, 'worktree', 'add', '-b', job['worker_branch'], str(destination), 'HEAD')
    return str(destination)


def validate_result(job, result):
    if result.get('question_hashes') != job['question_hashes']:
        raise ValueError('Result IDs/hashes differ from assignment')
    rows = result.get('results', [])
    if len(rows) != len(job['question_hashes']) or {r['question_id'] for r in rows} != set(job['question_hashes']):
        raise ValueError('Every assigned ID requires exactly one disposition')
    for row in rows:
        if row.get('disposition') not in DISPOSITIONS or not row.get('evidence_path') or not row.get('evidence_sha256'):
            raise ValueError('Missing disposition or evidence reference')
        path = Path(row['evidence_path'])
        if path.is_absolute() or '..' in path.parts:
            raise ValueError('Evidence must be repository-relative')
    if not result.get('worker_commit') or len(result['worker_commit']) != 40:
        raise ValueError('Exact worker commit required')


def submit(state, job_id, token, result, at=None):
    at = at or timestamp()
    job = get_job(state, job_id)
    validate_result(job, result)
    if job['status'] in {'SUBMITTED', 'INTEGRATED'}:
        if job.get('lease_token') == token and job['result'] == result:
            return  # identical repeated completion is safe
        raise ValueError('Conflicting completion')
    require_lease(job, token, at)
    job.update(status='SUBMITTED', result=result, submitted_at=at)
    event(state, 'SUBMIT', at, job_id=job_id, result_sha256=digest(result))


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()


def integrate(state, job_id, root, at=None):
    """Only the integrator runs this, after sequential cherry-pick and validation."""
    job = get_job(state, job_id)
    if job['status'] == 'INTEGRATED':
        return
    if job['status'] != 'SUBMITTED':
        raise ValueError('Submit before integration')
    if any(j['sequence'] < job['sequence'] and j['status'] != 'INTEGRATED' for j in state['jobs']):
        raise ValueError('Integrate completed jobs in assignment order')
    ledger = read_ledger(root)
    for qid, expected in job['question_hashes'].items():
        if current_hash(root, ledger[qid]) != expected:
            raise ValueError('Assigned content changed: ' + qid)
    result = job['result']
    # Cherry-picks have different commit IDs; compare immutable report bytes at source and HEAD.
    git(root, 'cat-file', '-e', result['worker_commit'] + '^{commit}')
    for row in result['results']:
        path = row['evidence_path']
        original = subprocess.check_output(['git', '-C', str(root), 'show', result['worker_commit'] + ':' + path])
        current = (root / path).read_bytes()
        if hashlib.sha256(original).hexdigest() != row['evidence_sha256'] or original != current:
            raise ValueError('Missing, changed, or unintegrated evidence: ' + path)
        committed = subprocess.check_output(['git', '-C', str(root), 'show', 'HEAD:' + path])
        if committed != current:
            raise ValueError('Evidence must be committed before checkpoint')
    at = at or timestamp()
    job.update(status='INTEGRATED', integrated_commit=git(root, 'rev-parse', 'HEAD'), integrated_at=at)
    event(state, 'INTEGRATE', at, job_id=job_id, commit=job['integrated_commit'])


def progress(state, ledger, corpus):
    total = len(ledger)
    reviewed = sum(r['checked_at'] is not None for r in ledger.values())
    notes = corpus['notes_units_with_complete_atomic_claim_census']
    return {'queue_jobs': {status: sum(j['status'] == status for j in state['jobs'])
                           for status in ('QUEUED', 'LEASED', 'SUBMITTED', 'INTEGRATED')},
            'author_review': {'count': reviewed, 'total': total, 'percent': round(100*reviewed/total, 2)},
            'note_claim_census': {'count': notes, 'total': corpus['notes_units'],
                                 'percent': round(100*notes/corpus['notes_units'], 2)},
            'independent_legal_audit': {'percent': None, 'status': 'REQUIRES_CANONICAL_AUDIT_VALIDATION'},
            'substantive_remediation': {'percent': None, 'status': 'REQUIRES_DEFECT_DISPOSITION_VALIDATION'},
            'verified_deployment': {'percent': None, 'status': corpus['deployment_status']},
            'warning': 'Queue integration is not author-review credit, independent audit, remediation, or release.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--state', type=Path)
    commands = parser.add_subparsers(dest='command', required=True)
    p = commands.add_parser('plan'); p.add_argument('--batches', type=int, default=1); p.add_argument('--size', type=int, default=40)
    p = commands.add_parser('claim'); p.add_argument('--worker', required=True); p.add_argument('--minutes', type=int, default=60)
    commands.add_parser('recover')
    for name in ('heartbeat', 'submit', 'integrate', 'worktree'):
        p = commands.add_parser(name); p.add_argument('--job', required=True)
        if name != 'integrate': p.add_argument('--token', required=True)
        if name == 'heartbeat': p.add_argument('--minutes', type=int, default=60)
        if name == 'submit': p.add_argument('--result', type=Path, required=True)
        if name == 'worktree': p.add_argument('--destination', type=Path, required=True)
    commands.add_parser('progress')
    args = parser.parse_args()
    root = args.root.resolve()
    path = args.state or root / DEFAULT.relative_to(ROOT)
    with checkpoint(path) as state:
        if args.command == 'plan': output = plan(state, read_ledger(root), root, args.batches, args.size)
        elif args.command == 'claim': output = claim(state, args.worker, args.minutes)
        elif args.command == 'recover': output = recover(state)
        elif args.command == 'heartbeat': output = heartbeat(state, args.job, args.token, args.minutes)
        elif args.command == 'submit': output = submit(state, args.job, args.token, json.loads(args.result.read_text()))
        elif args.command == 'integrate': output = integrate(state, args.job, root)
        elif args.command == 'worktree': output = prepare_worktree(state, args.job, args.token, root, args.destination.resolve())
        else: output = progress(state, read_ledger(root), json.loads((root / 'reports/full-corpus-review/progress.json').read_text()))
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
