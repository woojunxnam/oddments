"""Explicit controller revocation of a lost worker; never fabricate lease expiry."""
from __future__ import annotations

import copy
from datetime import datetime
import hashlib


def revoke_lost_worker(state, job, token, reason, actor, at):
    if actor != '/root':
        raise ValueError('Only root controller may revoke a lost worker lease')
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError('Lost worker revocation requires an explicit reason')
    if not isinstance(token, str) or not token:
        raise ValueError('Current lease token required')
    instant = datetime.fromisoformat(at)
    if instant.tzinfo is None:
        raise ValueError('Timezone-aware revocation timestamp required')
    token_sha = hashlib.sha256(token.encode()).hexdigest()
    previous = next((event for event in reversed(state['events'])
                     if event.get('job_id') == job['job_id'] and
                     event.get('kind') == 'LEASE_REVOKED'), None)
    if (job['status'] == 'QUEUED' and previous and
            previous['attempt'] == job['attempt'] and previous['lease_token_sha256'] == token_sha):
        if previous['reason'] != reason.strip():
            raise ValueError('Conflicting lost worker revocation')
        return job['job_id']
    if job['status'] != 'LEASED' or job.get('lease_token') != token:
        raise ValueError('Only the current LEASED job token can be revoked')
    # Refuse a backdated event even for direct Python callers. CLI uses current UTC.
    prior = [datetime.fromisoformat(event['at']) for event in state['events']]
    if prior and instant < max(prior):
        raise ValueError('Revocation cannot precede queue history')
    event = {'kind': 'LEASE_REVOKED', 'at': at, 'job_id': job['job_id'],
             'controller_actor': actor, 'reason': reason.strip(),
             'attempt': job['attempt'], 'lease_token_sha256': token_sha,
             'previous_lease': {key: copy.deepcopy(job[key]) for key in
                 ('worker', 'actor_provenance', 'auditor', 'auditor_instance',
                  'worker_branch', 'lease_until', 'controller_independence_basis') if key in job}}
    job['status'] = 'QUEUED'
    del job['lease_token']
    state['events'].append(event)
    return job['job_id']
