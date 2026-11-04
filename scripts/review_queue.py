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
STAGES = {
    'author': {'purpose': 'AUTHOR_WORK_SCHEDULER_NOT_RELEASE_CERTIFICATION',
               'state': DEFAULT.relative_to(ROOT)},
    'independent-legacy': {
        'purpose': 'INDEPENDENT_LEGACY_WORK_SCHEDULER_NOT_RELEASE_CERTIFICATION',
        'state': Path('reports/full-corpus-review/independent-legacy-work-queue.json')},
}
UNREVIEWED = 'NOT_REVERIFIED_IN_FULL_CORPUS_REVIEW'
FIRST = [f'MA-EXP-{i:04d}' for i in range(385, 425)]
DISPOSITIONS = {'AUTHOR_REVIEWED', 'HOLD', 'SOURCE_BLOCKED', 'NEEDS_REMEDIATION'}
INDEPENDENT_DISPOSITIONS = {'INDEPENDENT_ASSESSED', 'HOLD', 'SOURCE_BLOCKED', 'NEEDS_REMEDIATION'}


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


def current_record(root, row):
    """Check actual collection too; a stale generated ledger cannot authorize work."""
    bank = json.loads((root / row['collection']).read_text())
    found = [q for q in bank['questions'] if q['question_id'] == row['question_id']]
    if len(found) != 1 or digest(found[0]) != row['content_sha256']:
        raise ValueError('Stale ledger content: ' + row['question_id'])
    return found[0]


def current_hash(root, row):
    current_record(root, row)
    return row['content_sha256']


def empty(stage='author'):
    return {'schema_version': 1, 'purpose': STAGES[stage]['purpose'],
            'jobs': [], 'events': []}


def state_stage(state, expected=None):
    stage = next((name for name, spec in STAGES.items() if state.get('purpose') == spec['purpose']), None)
    if stage is None or (expected is not None and stage != expected):
        raise ValueError('Stage/state purpose mismatch')
    if any(job.get('stage', 'author') != stage for job in state['jobs']):
        raise ValueError('Job stage differs from checkpoint purpose')
    return stage


def state_path(root, stage, explicit=None):
    path = (explicit or root / STAGES[stage]['state']).resolve()
    if any(name != stage and path == (root / spec['state']).resolve()
           for name, spec in STAGES.items()):
        raise ValueError('Stage/state path mismatch')
    return path


@contextmanager
def checkpoint(path, stage='author'):
    """Controller processes serialize writes; workers never mutate this file directly."""
    path.parent.mkdir(parents=True, exist_ok=True)
    # Lock lives in /tmp, not tracked or regenerated output. Same realpath => same lock.
    lock_path = Path(tempfile.gettempdir()) / ('mpje-queue-' +
        hashlib.sha256(str(path.resolve()).encode()).hexdigest() + '.lock')
    with lock_path.open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        state = json.loads(path.read_text()) if path.exists() else empty(stage)
        state_stage(state, stage)
        original = json.dumps(state, sort_keys=True)
        yield state
        state_stage(state, stage)
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


def remediation_default_priority(root, ledger, candidates):
    """Read current source bindings; caller has already applied all ledger gates."""
    from build_sata_remediation_candidates import ALLOCATION
    allocation_path = root / ALLOCATION
    allocation_raw = allocation_path.read_bytes()
    allocation = json.loads(allocation_raw)
    if allocation.get('schema_version') != 'sata-remediation-allocation/1':
        raise ValueError('Unsupported remediation allocation priority source')
    rows = allocation.get('allocations', [])
    remediation = [row['question_id'] for row in rows]
    if len(remediation) != 3 or len(set(remediation)) != 3:
        raise ValueError('Invalid remediation priority allocation')
    if not set(remediation) <= set(ledger):
        raise ValueError('Remediation priority missing authoritative ledger IDs; regenerate inventory')
    banks = {}
    for allocation_row in rows:
        qid = allocation_row['question_id']
        row = ledger[qid]
        collection = row['collection']
        relative = Path(collection)
        if relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Unsafe remediation priority collection')
        if collection not in banks:
            banks[collection] = json.loads((root / collection).read_bytes())
        matching = [q for q in banks[collection]['questions'] if q['question_id'] == qid]
        if (len(matching) != 1 or digest(matching[0]) != row['content_sha256'] or
                not matching[0].get('archive_only_candidate') or
                matching[0].get('revision_of') != allocation_row['original_question_id'] or
                matching[0].get('remediation_candidate', {}).get('draft_key') != allocation_row['draft_key'] or
                matching[0]['remediation_candidate'].get('current_id_independent_audit') != 'PENDING'):
            raise ValueError('Stale/unbound remediation priority content: ' + qid)
    config_path = root / 'site/practice-expansion/publication.json'
    config_raw = config_path.read_bytes()
    selection_binding = json.loads(config_raw)['representative_selection']
    relative = Path(selection_binding['path'])
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError('Unsafe default priority source path')
    raw = (root / relative).read_bytes()
    if hashlib.sha256(raw).hexdigest() != selection_binding['sha256']:
        raise ValueError('Stale source-derived default priority selection')
    defaults = json.loads(raw)['recommended_ids']
    if len(defaults) != len(set(defaults)) or not set(defaults) <= set(ledger):
        raise ValueError('Invalid source-derived default priority IDs; regenerate inventory')
    eligible = set(candidates)
    ordered = sorted(eligible & set(remediation))
    ordered += sorted((eligible & set(defaults)) - set(ordered))
    ordered += sorted(eligible - set(ordered))
    bindings = {ALLOCATION: hashlib.sha256(allocation_raw).hexdigest(),
                str(config_path.relative_to(root)): hashlib.sha256(config_raw).hexdigest(),
                str(relative): hashlib.sha256(raw).hexdigest()}
    return ordered, bindings


def plan(state, ledger, root, batches=1, size=40, at=None, prioritize_remediation_defaults=False):
    if not 1 <= batches <= 4 or not 1 <= size <= 40:
        raise ValueError('Use 1–4 batches of 1–40 IDs')
    at = at or timestamp()
    stage = state_stage(state)
    if prioritize_remediation_defaults and stage != 'independent-legacy':
        raise ValueError('Remediation/default priority is only available for independent-legacy planning')
    priority_bindings = None
    if not state['jobs'] and stage == 'author':
        groups = [FIRST]
        if any(qid not in ledger or ledger[qid]['legal_review_status'] != UNREVIEWED for qid in FIRST):
            raise ValueError('First cohort changed; reconcile ledger rather than assuming missing IDs')
    else:
        if any(j['status'] != 'INTEGRATED' for j in state['jobs']):
            return []  # retrying plan never duplicates outstanding assignments
        assigned = {qid for j in state['jobs'] for qid in j['question_hashes']}
        uncredited = sorted(qid for qid in assigned if qid not in ledger or
                            (stage == 'author' and
                             (ledger[qid]['legal_review_status'] == UNREVIEWED or
                              ledger[qid].get('current_id_author_review_required') is True or
                              ledger[qid].get('checked_at') is None)) or
                            (stage == 'independent-legacy' and
                             ledger[qid].get('independent_legacy_legal_assessment') is None))
        if uncredited:
            kind = 'review credit' if stage == 'author' else 'independent legacy assessment'
            raise ValueError('Integrated jobs lack authoritative ' + kind + '; register and regenerate ledger: ' +
                             ', '.join(uncredited))
        candidates = sorted(qid for qid, row in ledger.items()
                            if qid not in assigned and
                            ((stage == 'author' and (row['legal_review_status'] == UNREVIEWED or
                             row.get('current_id_author_review_required') is True)) or
                             (stage == 'independent-legacy' and row.get('checked_at') and
                              row.get('author_review_increment', 1) != 0 and
                              row.get('current_id_author_review_required') is not True and
                              row.get('independent_legacy_legal_assessment') is None)))
        if prioritize_remediation_defaults:
            candidates, priority_bindings = remediation_default_priority(root, ledger, candidates)
        required = [qid for qid in candidates if ledger[qid].get('current_id_author_review_required') is True] if stage == 'author' else []
        if required:
            from remediation_author_reviews import candidate_records
            if set(required) != set(candidate_records(root)) or size < 3:
                raise ValueError('Native current-ID author scope requires exactly the three allocated candidates and size >=3')
            remainder = [qid for qid in candidates if qid not in required]
            groups = [required] + [remainder[i:i+size] for i in range(0, min(len(remainder), (batches-1)*size), size)]
        else:
            groups = [candidates[i:i+size] for i in range(0, min(len(candidates), batches*size), size)]
    created = []
    for group in groups:
        records = {qid: current_record(root, ledger[qid]) for qid in group}
        hashes = {qid: ledger[qid]['content_sha256'] for qid in group}
        known_actors = {}
        if stage == 'independent-legacy':
            for qid, record in records.items():
                actual = record.get('remediation_candidate', {}).get('known_author_editor_actor_ids', [])
                if (not isinstance(actual, list) or
                        any(not isinstance(actor, str) or not actor.strip() for actor in actual) or
                        len(actual) != len(set(actual)) or
                        ledger[qid].get('known_author_editor_actor_ids', []) != actual):
                    raise ValueError('Stale known author/editor actor binding: ' + qid)
                if actual:
                    known_actors[qid] = actual
        prefix = 'review-' if stage == 'author' else 'review-independent-legacy-'
        job_id = prefix + digest(hashes)[:16]
        job = {'job_id': job_id, 'sequence': len(state['jobs']) + 1,
               'question_hashes': hashes, 'status': 'QUEUED', 'attempt': 0,
               'worker_branch': 'mission/' + job_id, 'created_at': at}
        if stage == 'author' and any(ledger[qid].get('current_id_author_review_required') is True for qid in group):
            from remediation_author_reviews import expected_actor
            if not all(ledger[qid].get('current_id_author_review_required') is True for qid in group):
                raise ValueError('Current-ID author job cannot mix other IDs')
            job['current_id_author_review_required_ids'] = list(group)
            job['required_author_actor_id'] = expected_actor(records)['actor_id']
            job['selection_policy'] = 'CURRENT_ID_AUTHOR_REVIEW_REQUIRED'
        if stage != 'author':
            job['stage'] = stage
        if known_actors:
            job['known_author_editor_actor_ids_by_question'] = known_actors
            job['excluded_worker_actor_ids'] = sorted({actor for actors in known_actors.values() for actor in actors})
        if priority_bindings is not None:
            job['selection_policy'] = 'REMEDIATION_THEN_SOURCE_DEFAULT_THEN_LEXICAL'
            job['priority_source_sha256'] = priority_bindings
        state['jobs'].append(job)
        created.append(job_id)
    if created:
        details = {} if priority_bindings is None else dict(
            selection_policy='REMEDIATION_THEN_SOURCE_DEFAULT_THEN_LEXICAL',
            priority_source_sha256=priority_bindings)
        if any(j.get('current_id_author_review_required_ids') for j in state['jobs'] if j['job_id'] in created):
            details['selection_policy'] = 'CURRENT_ID_AUTHOR_REVIEW_REQUIRED_THEN_LEXICAL'
        event(state, 'PLAN', at, job_ids=created, **details)
    return created


def recover(state, at=None):
    state_stage(state)
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
        if active[0].get('required_author_actor_id') and worker != active[0]['required_author_actor_id']:
            raise ValueError('Required content author must claim current-ID author job')
        if worker in active[0].get('excluded_worker_actor_ids', []):
            raise ValueError('Known content author/editor cannot independently claim: ' + worker)
        return active[0]  # idempotent reconnect, not another assignment
    queued = next((j for j in state['jobs'] if j['status'] == 'QUEUED'), None)
    if queued is None:
        return None
    if queued.get('required_author_actor_id') and worker != queued['required_author_actor_id']:
        raise ValueError('Required content author must claim current-ID author job')
    if worker in queued.get('excluded_worker_actor_ids', []):
        raise ValueError('Known content author/editor cannot independently claim: ' + worker)
    queued.update(status='LEASED', worker=worker, attempt=queued['attempt'] + 1,
                  lease_until=(datetime.fromisoformat(at) + timedelta(minutes=minutes)).isoformat())
    queued['worker_branch'] = 'mission/' + queued['job_id'] + '-attempt-' + str(queued['attempt'])
    queued['lease_token'] = digest({'job': queued['job_id'], 'worker': worker,
                                    'attempt': queued['attempt'], 'at': at})
    event(state, 'CLAIM', at, job_id=queued['job_id'], worker=worker, attempt=queued['attempt'])
    return queued


def get_job(state, job_id):
    state_stage(state)
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
    stage = job.get('stage', 'author')
    if result.get('stage', 'author') != stage:
        raise ValueError('Result stage differs from assignment')
    if result.get('question_hashes') != job['question_hashes']:
        raise ValueError('Result IDs/hashes differ from assignment')
    rows = result.get('results', [])
    if len(rows) != len(job['question_hashes']) or {r['question_id'] for r in rows} != set(job['question_hashes']):
        raise ValueError('Every assigned ID requires exactly one disposition')
    for row in rows:
        dispositions = DISPOSITIONS if stage == 'author' else INDEPENDENT_DISPOSITIONS
        if row.get('disposition') not in dispositions or not row.get('evidence_path') or not row.get('evidence_sha256'):
            raise ValueError('Missing disposition or evidence reference')
        path = Path(row['evidence_path'])
        if path.is_absolute() or '..' in path.parts:
            raise ValueError('Evidence must be repository-relative')
    if not result.get('worker_commit') or len(result['worker_commit']) != 40:
        raise ValueError('Exact worker commit required')
    if stage == 'independent-legacy':
        validate_independent_provenance(job, result)
    elif job.get('current_id_author_review_required_ids'):
        from remediation_author_reviews import validate_submission
        validate_submission(job, result)


def validate_independent_provenance(job, evidence):
    """Require accountable declarations; identity strings cannot prove actual independence."""
    if evidence.get('independent_of_authors') is not True:
        raise ValueError('Independent evidence requires independent_of_authors: true')
    actor = evidence.get('actor_provenance')
    if (not isinstance(actor, dict) or actor.get('actor_id') != job.get('worker') or
            not isinstance(actor.get('session_id'), str) or not actor['session_id'].strip() or
            any(not isinstance(evidence.get(k), str) or not evidence[k].strip()
                for k in ('auditor', 'auditor_instance'))):
        raise ValueError('Actual actor provenance and auditor session required; actor_id must match claim worker')


def validate_independent_evidence(job, row, evidence):
    validate_independent_provenance(job, evidence)
    for key in ('auditor', 'auditor_instance', 'actor_provenance'):
        if evidence[key] != job['result'][key]:
            raise ValueError('Evidence actor provenance differs from submission')
    if evidence.get('canonical_audit') is not False or evidence.get('canonical_release_credit') != 0:
        raise ValueError('Independent legacy evidence must explicitly disclaim canonical release credit')
    records = evidence.get('records', [])
    matches = [r for r in records if r.get('question_id') == row['question_id']]
    if len(matches) != 1 or matches[0].get('record_sha256') != job['question_hashes'][row['question_id']]:
        raise ValueError('Independent evidence must bind each ID to its assigned current record hash')


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
        if job.get('stage') == 'independent-legacy':
            validate_independent_evidence(job, row, json.loads(current))
        elif job.get('current_id_author_review_required_ids'):
            from remediation_author_reviews import candidate_records, validate_report
            validate_report(root, job, result, current, candidate_records(root))
    at = at or timestamp()
    job.update(status='INTEGRATED', integrated_commit=git(root, 'rev-parse', 'HEAD'), integrated_at=at)
    event(state, 'INTEGRATE', at, job_id=job_id, commit=job['integrated_commit'])


def progress(state, ledger, corpus):
    state_stage(state)
    total = len(ledger)
    reviewed = sum(r['checked_at'] is not None and r.get('author_review_increment', 1) != 0
                   for r in ledger.values())
    notes = corpus['notes_units_with_complete_atomic_claim_census']
    return {'queue_jobs': {status: sum(j['status'] == status for j in state['jobs'])
                           for status in ('QUEUED', 'LEASED', 'SUBMITTED', 'INTEGRATED')},
            'author_review': {'count': reviewed, 'total': total, 'percent': round(100*reviewed/total, 2)},
            'note_claim_census': {'count': notes, 'total': corpus['notes_units'],
                                 'percent': round(100*notes/corpus['notes_units'], 2)},
            'independent_legal_audit': {'count': corpus.get('independent_legacy_legal_assessed', 0), 'total': total,
                'percent': (round(100*corpus['independent_legacy_legal_assessed']/total, 2) if 'independent_legacy_legal_assessed' in corpus else None),
                'status': 'LEGACY_SOURCE_ASSESSMENT_NOT_CANONICAL_RELEASE_EVIDENCE'},
            'substantive_remediation': {'percent': None, 'status': 'REQUIRES_DEFECT_DISPOSITION_VALIDATION'},
            'verified_deployment': {'percent': None, 'status': corpus['deployment_status']},
            'warning': 'Queue integration is not author-review credit, independent audit, remediation, or release.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--state', type=Path)
    parser.add_argument('--stage', choices=STAGES, default='author')
    commands = parser.add_subparsers(dest='command', required=True)
    p = commands.add_parser('plan'); p.add_argument('--batches', type=int, default=1); p.add_argument('--size', type=int, default=40)
    p.add_argument('--prioritize-remediation-and-default', action='store_true',
                   help='Independent stage only: eligible remediation IDs, then current source-bound defaults, then lexical remainder.')
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
    path = state_path(root, args.stage, args.state)
    with checkpoint(path, args.stage) as state:
        if args.command == 'plan': output = plan(state, read_ledger(root), root, args.batches, args.size,
                                                        prioritize_remediation_defaults=args.prioritize_remediation_and_default)
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
