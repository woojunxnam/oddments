"""Root-only exact-nine registration proposal; no claim or file mutation of shared state."""
import argparse
import copy
import json
from pathlib import Path

import review_queue as queue
import remaining9_procedural_metadata as route
from procedural_secondary_metadata import committed_reader


def prepare(root, reviewer):
    route.require(not (root / route.STATE).exists(), 'Existing native state must be reused/recovered; never re-register it')
    source_head = queue.git(root, 'rev-parse', 'HEAD')
    read = committed_reader(root)
    read('reports/full-corpus-review/question-ledger.jsonl')
    ledger = queue.read_ledger(root)
    questions = {uid: queue.current_record(root, ledger[uid]) for uid in route.IDS}
    for uid in route.IDS:
        bank = json.loads(read(ledger[uid]['collection']))
        route.require([q for q in bank['questions'] if q['question_id'] == uid] == [questions[uid]],
                      'Actual committed collection differs from current ledger input')
    primary = {}
    for uid in route.IDS:
        binding = route.PARENTS[uid]
        source = json.loads(read(binding['report_path'], binding['report_sha256']))
        rows = [row for row in source['records'] if row['question_id'] == uid]
        route.require(len(rows) == 1, 'Exact parent row absent')
        primary[uid] = rows[0]
        route.validate_parent(read, uid, rows[0], questions[uid], binding)
    known = {p for b in route.AUTHOR_BINDINGS.values() for p in b['known_principals']}
    for path, binding in route.AUTHOR_BINDINGS.items():
        source = json.loads(read(path, binding['raw_sha256']))
        route.require(sorted(route.principals(source)) == binding['known_principals'], 'Author history changed')
    excluded = {'/root', route.ENGINEER, *reviewer['known_author_ids'], *known}
    for binding in route.PARENTS.values():
        excluded.update((binding['original_actor'], binding['original_session'], binding['original_auditor_instance']))
    for question in questions.values():
        excluded.update(route.principals(question))
    state = queue.empty('independent-legacy')
    state[route.SCOPE_KEY] = dict(schema_version=1, purpose=route.PURPOSE, question_ids=list(route.IDS),
        previous_evidence=copy.deepcopy(route.PARENTS), root_actor='/root', automatic_release_credit=0,
        fresh_reviewer=copy.deepcopy(reviewer), prepared_source_head=source_head)
    hashes = {uid: queue.digest(questions[uid]) for uid in route.IDS}
    at = queue.timestamp()
    state['jobs'] = [dict(job_id=route.JOB_ID, sequence=1, question_hashes=hashes, status='QUEUED', attempt=0,
        worker_branch='mission/' + route.JOB_ID, created_at=at, stage='independent-legacy',
        excluded_worker_actor_ids=sorted(excluded))]
    route.validate_reviewer(state[route.SCOPE_KEY], state['jobs'][0], questions)
    queue.event(state, 'PLAN', at, job_ids=[route.JOB_ID],
                selection_policy='FIXED_NINE_PROCEDURAL_ONLY_NO_PRIMARY_OVERRIDE')
    route.require(queue.git(root, 'rev-parse', 'HEAD') == source_head, 'Source HEAD changed during actual registration proposal')
    return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--actor', required=True, choices=['/root'])
    parser.add_argument('--reviewer', required=True, type=Path,
                        help='Actual captured actor/session, auditor, instance, author IDs and independence basis JSON')
    parser.add_argument('--output', required=True, type=Path,
                        help='New external proposal path; root must review/commit before native claim')
    args = parser.parse_args()
    route.require(not args.output.exists(), 'Never overwrite an existing registration or draft')
    root = args.root.resolve()
    route.require(args.output.resolve() != (root / route.STATE).resolve(), 'Proposal must not overwrite native state')
    state = prepare(root, json.loads(args.reviewer.read_bytes()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
    print('Prepared exact-nine external native registration proposal; no actual claim/review/release credit.')


if __name__ == '__main__':
    main()
