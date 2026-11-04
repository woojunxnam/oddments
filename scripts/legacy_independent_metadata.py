"""Discover only committed, sequentially integrated legacy question evidence.

This read-only consumer does not replace controller integration checks or grant
canonical release credit. Original worker Git objects are unnecessary in CI.
"""
import hashlib
import json
from pathlib import PurePosixPath
import subprocess

import review_queue as queue

STATE = 'reports/full-corpus-review/independent-legacy-work-queue.json'
PREFIX = 'reports/full-corpus-review/'


def integrated_sources(root, *, source_bindings=None):
    """Optionally expose bindings only after all committed sources validate."""
    def require(condition, message):
        if not condition:
            raise ValueError(message)

    def committed(relative, expected=None):
        pure=PurePosixPath(relative)
        require(not pure.is_absolute() and '..' not in pure.parts and str(pure)==relative and
                relative.startswith(PREFIX), 'Unsafe integrated legacy evidence path')
        path=root/relative
        require(root.resolve() in path.resolve().parents and not path.is_symlink(),
                'Unsafe integrated legacy evidence path')
        raw=path.read_bytes()
        stored=subprocess.check_output(['git','-C',str(root),'show','HEAD:'+relative])
        require(raw==stored, 'Uncommitted integrated legacy evidence: '+relative)
        require(expected is None or hashlib.sha256(raw).hexdigest()==expected,
                'Integrated legacy evidence raw SHA changed: '+relative)
        return json.loads(raw)

    state=committed(STATE)
    queue.state_stage(state,'independent-legacy')
    sources={}
    bindings={}
    jobs=state['jobs']
    require([j['sequence'] for j in jobs]==list(range(1,len(jobs)+1)),
            'Integrated legacy sequence changed')
    for job in jobs:
        if job['status']!='INTEGRATED':
            continue
        require(all(j['status']=='INTEGRATED' for j in jobs if j['sequence']<job['sequence']),
                'Integrated legacy evidence has an incomplete predecessor')
        require(job.get('integrated_commit') and job.get('integrated_at') and any(
            e.get('kind')=='INTEGRATE' and e.get('job_id')==job['job_id'] and
            e.get('commit')==job['integrated_commit'] for e in state['events']),
            'Missing captured legacy integration provenance')
        result=job['result']
        queue.validate_result(job,result)
        for row in result['results']:
            relative=row['evidence_path']
            if relative not in sources:
                sources[relative]=committed(relative,row['evidence_sha256'])
            else:
                raw=(root/relative).read_bytes()
                require(hashlib.sha256(raw).hexdigest()==row['evidence_sha256'],
                        'Conflicting integrated legacy evidence bindings')
            report=sources[relative]
            queue.validate_independent_evidence(job,row,report)
            require(len(report['records'])==len(job['question_hashes']) and
                    {r['question_id'] for r in report['records']}==set(job['question_hashes']),
                    'Integrated legacy report assignment differs')
            if source_bindings is not None:
                review=next(r for r in report['records'] if r['question_id']==row['question_id'])
                bindings[row['question_id']]=dict(
                    question_id=row['question_id'], source_path=relative,
                    source_sha256=row['evidence_sha256'], job_id=job['job_id'],
                    record_sha256=job['question_hashes'][row['question_id']],
                    review_record_sha256=queue.digest(review),
                    reviewed_at=report.get('reviewed_at'),
                    auditor_instance=report['auditor_instance'],
                    actor_provenance=dict(report['actor_provenance']))
    if source_bindings is not None:
        source_bindings.update(bindings)
    return list(sources.values())
