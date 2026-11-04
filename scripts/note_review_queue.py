"""Root-owned resumable note completeness/legal review; never question credit."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
STATE = 'reports/full-corpus-review/independent-notes-work-queue.json'
LEDGER = 'reports/full-corpus-review/notes-unit-ledger.jsonl'
OUTPUT = 'reports/full-corpus-review/independent-notes/'
STAGE = 'independent-notes'
PURPOSE = 'INDEPENDENT_NOTES_COMPLETENESS_AND_LEGAL_SCHEDULER_NOT_RELEASE_EVIDENCE'
CONTROLLER = '/root'
LEGAL = {'KEEP', 'LEGAL_HOLD', 'SOURCE_BLOCKED'}
UNIT_LEGAL = LEGAL | {'NOT_APPLICABLE_NONLEGAL'}
COMPLETE = {'COMPLETE', 'OMISSIONS_FOUND'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def raw_sha(raw):
    return hashlib.sha256(raw).hexdigest()


def digest(value):
    return raw_sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode()


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def instant(value):
    parsed = datetime.fromisoformat(value)
    require(parsed.tzinfo is not None, 'Timezone-aware timestamp required')
    return parsed


def safe_path(root, relative, output=False):
    pure = PurePosixPath(relative)
    require(not pure.is_absolute() and '..' not in pure.parts and str(pure) == relative and
            (not output or relative.startswith(OUTPUT)), 'Unsafe repository-relative review path')
    path = root/relative
    require(root.resolve() in path.resolve().parents and not path.is_symlink(), 'Review path escapes repository')
    return path


def git(root, *args, binary=False):
    output = subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.PIPE)
    return output if binary else output.decode().strip()


def provenance_ids(value):
    """Preserve known author principals; descriptive labels do not identify unknown people."""
    result = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {'actor_id','actual_worker','worker','session_id','author_id','auditor_instance',
                       'reviewer_provenance','author_provenance'} and isinstance(child,str) and child.strip():
                result.add(child)
            result.update(provenance_ids(child))
    elif isinstance(value,list):
        for child in value:
            result.update(provenance_ids(child))
    return result


def inventory(root, notes=None, ledger_raw=None):
    if notes is None:
        from notes_revision import load_notes
        notes = load_notes(root)
    actual = {u['id']:u for c in notes['chapters'] for u in c['units']}
    # A generator may validate its freshly computed ledger without reading the
    # previous generated file. Annotation-only fields are outside the binding.
    raw = safe_path(root,LEDGER).read_bytes() if ledger_raw is None else ledger_raw
    require(isinstance(raw,bytes), 'Note ledger input must be raw bytes')
    rows = [json.loads(line) for line in raw.decode().splitlines()]
    require(len(actual) == sum(len(c['units']) for c in notes['chapters']) and
            len(rows) == len({r['unit_id'] for r in rows}) and
            {r['unit_id'] for r in rows} == set(actual), 'Duplicate or incomplete note ledger inventory')
    eligible, censuses = {}, {}
    for row in rows:  # authoritative ledger order, never lexical ID sorting
        uid = row['unit_id']; unit = actual[uid]; body_sha = raw_sha(unit['body'].encode())
        require(row['actual_effective_body_sha256'] == body_sha, 'Stale ledger/current body: '+uid)
        if row.get('atomic_claim_census_complete') is not True:
            continue
        path = row.get('atomic_census_source')
        require(isinstance(path,str) and bool(path), 'Enumerated unit lacks census source: '+uid)
        if path not in censuses:
            census_raw = safe_path(root,path).read_bytes(); census = json.loads(census_raw)
            claims = census['claims']; units = census['units']
            require(len(claims) == len({c['claim_id'] for c in claims}) and
                    len(units) == len({u['unit_id'] for u in units}) and
                    {u['unit_id'] for u in units} <= set(actual) and
                    {c['unit_id'] for c in claims} <= {u['unit_id'] for u in units},
                    'Duplicate or orphan census claim/unit')
            censuses[path] = (census_raw,census)
        census_raw,census = censuses[path]
        found = [u for u in census['units'] if u['unit_id'] == uid]
        require(len(found) == 1, 'Missing or extra selected census unit: '+uid)
        counted = found[0]; claims = [c for c in census['claims'] if c['unit_id'] == uid]
        nonlegal = None
        if not claims:
            nonlegal_inventory = census.get('editorial_nonlegal_inventory',{})
            nonlegal = nonlegal_inventory.get(uid) if isinstance(nonlegal_inventory,dict) else None
            require(counted.get('nonlegal_inventory_only') is True and
                    counted.get('legal_verification_status') == 'NOT_APPLICABLE_EDITORIAL_METHOD_NO_LEGAL_CLAIMS' and
                    isinstance(nonlegal,dict) and nonlegal.get('body_read_completely') is True and
                    type(nonlegal.get('legal_claim_count')) is int and nonlegal['legal_claim_count'] == 0 and
                    all(isinstance(nonlegal.get(k),str) and nonlegal[k].strip() for k in
                        ('classification','census_completion_basis_ko')) and
                    isinstance(nonlegal.get('items'),list) and bool(nonlegal['items']),
                    'Empty census needs explicit reviewed nonlegal classification: '+uid)
        require(counted['unit_content_sha256'] == body_sha and counted['body_read_completely'] is True and
                counted['claim_count'] == len(claims) and
                [c['claim_id'] for c in claims] == row['atomic_claim_ids'], 'Stale census/claim scope: '+uid)
        require(all(c['unit_content_sha256'] == body_sha and
                    c['review_status'] in {'AUTHOR_SOURCE_CHECKED','SOURCE_BLOCKED'} for c in claims) and
                sum(c['review_status'] == 'SOURCE_BLOCKED' for c in claims) == row['atomic_source_blocked_count'],
                'Stale or unsupported census claim: '+uid)
        ledger_binding = {k:row.get(k) for k in ('unit_id','chapter_id','actual_effective_body_sha256',
            'atomic_claim_census_complete','atomic_claim_census_status','atomic_census_source',
            'atomic_census_notes_revision','atomic_claim_ids','atomic_source_blocked_count')}
        eligible[uid] = {'body_sha256':body_sha, 'census_path':path, 'census_sha256':raw_sha(census_raw),
            'census_unit_record_sha256':digest(counted), 'ledger_binding_sha256':digest(ledger_binding),
            'claim_record_sha256s':{c['claim_id']:digest(c) for c in claims},
            'source_blocked_claim_ids':[c['claim_id'] for c in claims if c['review_status'] == 'SOURCE_BLOCKED'],
            'author_nonlegal_classification':nonlegal,
            'known_author_ids':sorted(provenance_ids(census.get('reviewer_provenance')) |
                provenance_ids({'reviewer_provenance':census.get('reviewer_provenance')}) |
                provenance_ids(census.get('author_provenance',{})) |
                provenance_ids(counted) | provenance_ids(claims) | provenance_ids(unit.get('author_provenance',{})))}
    return {'root':str(root),'ledger_sha256':raw_sha(raw), 'total_units':len(rows), 'units':eligible,
            'notes':notes, 'existing_content_keep_units':sum(u.get('independent_content_review',{}).get('decision') == 'KEEP'
                                              for u in actual.values())}


def empty(root):
    return {'schema_version':1, 'stage':STAGE, 'purpose':PURPOSE, 'controller_actor':CONTROLLER,
            'controller_root':str(root.resolve()), 'jobs':[], 'events':[]}


def validate_state(state, root=None):
    require(state.get('schema_version') == 1 and state.get('stage') == STAGE and
            state.get('purpose') == PURPOSE and state.get('controller_actor') == CONTROLLER,
            'Wrong note queue/controller purpose')
    if root is not None:
        require(state['controller_root'] == str(root.resolve()), 'Controller worktree differs from note checkpoint')
    jobs = state['jobs']
    require(len({j['job_id'] for j in jobs}) == len(jobs) and
            [j['sequence'] for j in jobs] == list(range(1,len(jobs)+1)) and
            all(j['stage'] == STAGE and j['status'] in {'QUEUED','LEASED','SUBMITTED','INTEGRATED'} for j in jobs),
            'Invalid note assignment sequence/scope')
    from notes_census_reassessment import validate_chain
    validate_chain(state)


@contextmanager
def checkpoint(root, actor):
    require(actor == CONTROLLER, 'Only root controller may write note checkpoint')
    path = safe_path(root,STATE); path.parent.mkdir(parents=True,exist_ok=True)
    lock = Path(tempfile.gettempdir())/('mpje-notes-'+raw_sha(str(path.resolve()).encode())+'.lock')
    with lock.open('a') as stream:
        fcntl.flock(stream,fcntl.LOCK_EX)
        state = json.loads(path.read_bytes()) if path.exists() else empty(root)
        validate_state(state,root); before = encoded(state)
        yield state
        validate_state(state,root)
        if encoded(state) != before:
            fd, temporary = tempfile.mkstemp(dir=path.parent,prefix='.notes-queue-')
            try:
                with os.fdopen(fd,'wb') as out:
                    out.write(encoded(state)); out.flush(); os.fsync(out.fileno())
                os.replace(temporary,path)
            finally:
                if os.path.exists(temporary): os.unlink(temporary)


def event(state, kind, at, **fields):
    state['events'].append({'kind':kind,'at':at,**fields})


def job_for(state, identifier):
    validate_state(state)
    found = [j for j in state['jobs'] if j['job_id'] == identifier]
    require(len(found) == 1, 'Unknown note job')
    return found[0]


def current(job, inv, state=None, allow_pending=False):
    body_handled=set()
    if state is not None and state.get('body_reassessments'):
        from notes_body_reassessment import current as body_current
        body_handled=body_current(job,inv,state,allow_pending)
    from notes_census_reassessment import latest_jobs
    latest = latest_jobs(state) if state is not None else {}
    for uid,binding in job['unit_bindings'].items():
        if uid in body_handled:continue
        selected = inv['units'].get(uid)
        owner = latest.get(uid,job)
        if owner['job_id'] != job['job_id']:
            require(selected is not None and selected['body_sha256'] == binding['body_sha256'],
                    'Historical reassessment body changed: '+uid)
            continue
        if allow_pending and owner.get('reassessment_id') and owner['status'] == 'QUEUED' and owner['attempt'] == 0:
            entry = next(e['record'] for e in state['reassessments']
                         if e['record']['reassessment_id'] == owner['reassessment_id'])
            if selected == entry['previous_binding']: continue
        require(selected == binding, 'Assigned ledger/census/body changed: '+uid)


def validate_reassessments(state, inv, root):
    if state.get('reassessments'):
        from notes_census_reassessment import validate_registered
        validate_registered(state,root,inv['notes'])
    if state.get('body_reassessments'):
        from notes_body_reassessment import validate_registered as validate_bodies
        validate_bodies(state,root,inv['notes'],inv=inv)


def plan(state, inv, root, batches=1, size=5, at=None):
    validate_state(state,root)
    require(1 <= batches <= 20 and 1 <= size <= 20, 'Use 1–20 batches of 1–20 note units')
    validate_reassessments(state,inv,root)
    for job in state['jobs']: current(job,inv,state,allow_pending=True)
    if any(j['status'] != 'INTEGRATED' for j in state['jobs']): return []
    assigned = {uid for j in state['jobs'] for uid in j['unit_bindings']}
    pending = [uid for uid in inv['units'] if uid not in assigned]
    created = []; at = at or timestamp(); base = git(root,'rev-parse','HEAD')
    require(raw_sha(git(root,'show','HEAD:'+LEDGER,binary=True)) == inv['ledger_sha256'],
            'Commit current note ledger before planning worker snapshots')
    require(not git(root,'diff','--name-only','HEAD','--','notes/guide.json','revisions/notes',
                    'scripts/notes_revision.py','scripts/notes_emergency_activation.py'),
            'Commit current note body/activation inputs before planning')
    for uid in pending[:batches*size]:
        binding = inv['units'][uid]
        require(raw_sha(git(root,'show','HEAD:'+binding['census_path'],binary=True)) == binding['census_sha256'],
                'Commit current note census before planning: '+uid)
    for start in range(0,min(len(pending),batches*size),size):
        ids = pending[start:start+size]; bindings = {uid:inv['units'][uid] for uid in ids}
        identifier = 'review-independent-notes-'+digest(bindings)[:16]
        state['jobs'].append({'job_id':identifier,'stage':STAGE,'sequence':len(state['jobs'])+1,
            'unit_bindings':bindings,'unit_ids':ids,'status':'QUEUED','attempt':0,'base_commit':base,
            'inventory_ledger_sha256':inv['ledger_sha256'],'created_at':at})
        created.append(identifier)
    if created: event(state,'PLAN',at,job_ids=created)
    return created


def recover(state, at=None):
    validate_state(state); at = at or timestamp(); recovered = []
    for job in state['jobs']:
        if job['status'] == 'LEASED' and instant(job['lease_until']) <= instant(at):
            job['status'] = 'QUEUED'; recovered.append(job['job_id'])
            event(state,'LEASE_EXPIRED',at,job_id=job['job_id'],attempt=job['attempt'])
    return recovered


def claim(state, inv, worker, session, independence_basis, auditor='GPT', auditor_instance=None,
          known_authors=(), minutes=60, at=None):
    require(all(isinstance(x,str) and x.strip() for x in (worker,session,independence_basis,auditor)) and
            worker != CONTROLLER and 1 <= minutes <= 1440, 'Fresh worker/session and controller independence basis required')
    if state.get('body_reassessments'):validate_reassessments(state,inv,Path(inv['root']))
    auditor_instance = auditor_instance or session; at = at or timestamp(); recover(state,at)
    provenance = {'actor_id':worker,'session_id':session}
    active = next((j for j in state['jobs'] if j['status'] == 'LEASED' and j['actor_provenance']['actor_id'] == worker),None)
    if active:
        require(active['actor_provenance'] == provenance and active['auditor'] == auditor and
                active['auditor_instance'] == auditor_instance, 'Active actor session differs')
        current(active,inv,state); return active
    job = next((j for j in state['jobs'] if j['status'] == 'QUEUED'),None)
    if job is None: return None
    current(job,inv,state)
    authors = set(job.get('known_author_ids',())) | set(known_authors) | {
        a for b in job['unit_bindings'].values() for a in b['known_author_ids']}
    require(not {worker,session,auditor_instance} & authors, 'Known body/source author cannot self-audit')
    job.update(status='LEASED',attempt=job['attempt']+1,actor_provenance=provenance,auditor=auditor,
        auditor_instance=auditor_instance,controller_independence_basis=independence_basis,
        known_author_ids=sorted(authors),lease_until=(instant(at)+timedelta(minutes=minutes)).isoformat())
    job['worker_branch'] = 'mission/'+job['job_id']+'-attempt-'+str(job['attempt'])
    job['lease_token'] = digest({'job':job['job_id'],'actor':provenance,'attempt':job['attempt'],'at':at})
    event(state,'CLAIM',at,job_id=job['job_id'],actor=provenance,attempt=job['attempt'])
    return job


def require_lease(job, token, at):
    require(job['status'] == 'LEASED' and job.get('lease_token') == token, 'Stale or absent note lease token')
    require(instant(job['lease_until']) > instant(at), 'Note lease expired')


def heartbeat(state, identifier, token, inv, minutes=60, at=None):
    at = at or timestamp(); job = job_for(state,identifier); require_lease(job,token,at); current(job,inv,state)
    require(1 <= minutes <= 1440, 'Use 1–1440 lease minutes')
    job['lease_until'] = (instant(at)+timedelta(minutes=minutes)).isoformat()
    event(state,'HEARTBEAT',at,job_id=identifier,attempt=job['attempt'])


def prepare_worktree(state, identifier, token, inv, root, destination, at=None):
    job = job_for(state,identifier); require_lease(job,token,at or timestamp()); current(job,inv,state)
    validate_reassessments(state,inv,root)
    destination = destination.resolve()
    if destination.exists():
        require(git(destination,'branch','--show-current') == job['worker_branch'] and
                Path(git(destination,'rev-parse','--show-toplevel')).resolve() == destination and
                git(destination,'rev-parse','--path-format=absolute','--git-common-dir') ==
                git(root,'rev-parse','--path-format=absolute','--git-common-dir'), 'Wrong worker worktree/branch')
    else:
        git(root,'worktree','add','-b',job['worker_branch'],str(destination),job['base_commit'])
    return str(destination)


def provenance(job, value):
    require(value.get('stage') == STAGE and value.get('independent_of_authors') is True,
            'Independent note stage/declaration required')
    require(all(value.get(k) == job[k] for k in ('actor_provenance','auditor','auditor_instance')),
            'Forged or inconsistent note actor/session provenance')
    require(value.get('canonical_audit') is False and type(value.get('canonical_release_credit')) is int and
            value['canonical_release_credit'] == 0 and type(value.get('question_audit_credit')) is int and
            value['question_audit_credit'] == 0, 'Note review cannot claim canonical/question credit')


def validate_evidence(job, result, report):
    provenance(job,report); rows = report.get('records',[])
    require(len(rows) == len(job['unit_ids']) and {r.get('unit_id') for r in rows} == set(job['unit_ids']),
            'Evidence requires exactly assigned note units')
    summaries = {r['unit_id']:r for r in result['results']}
    sources = []
    for row in rows:
        uid = row['unit_id']; binding = job['unit_bindings'][uid]
        require(row.get('binding') == binding and row.get('body_read_completely') is True,
                'Stale note evidence binding/body read: '+uid)
        completeness = row.get('completeness'); omissions = row.get('omissions')
        require(completeness in COMPLETE and isinstance(omissions,list) and
                ((completeness == 'COMPLETE' and not omissions) or
                 (completeness == 'OMISSIONS_FOUND' and omissions and all(isinstance(x,str) and x.strip() for x in omissions))) and
                isinstance(row.get('completeness_method'),str) and bool(row['completeness_method'].strip()),
                'Incomplete completeness assessment: '+uid)
        claims = row.get('claims',[]); expected = binding['claim_record_sha256s']
        require(len(claims) == len(expected) and {c.get('claim_id') for c in claims} == set(expected),
                'Missing, duplicate, or extra claim assessment: '+uid)
        if job.get('reassessment_id'):
            require(row.get('reassessment_review') == {**job['reassessment_review'],
                    'final_census_read_completely':True,'all_original_omissions_reassessed':True,
                    'all_original_propositions_preserved':True},
                    'Fresh final-census assessment of every original omission required')
        if job.get('body_reassessment_id'):
            from notes_body_reassessment import validate_review
            validate_review(job,row)
        for c in claims:
            inherited = job.get('carried_legal_blockers',{}).get(uid,{}).get(c.get('claim_id'),[])
            if inherited:
                require(c.get('inherited_legal_blockers') == inherited and
                        c.get('legal_status') in ({'LEGAL_HOLD'} if any(x['legal_status'] == 'LEGAL_HOLD' for x in inherited)
                                                  else {'SOURCE_BLOCKED','LEGAL_HOLD'}),
                        'Census-only reassessment cannot close inherited legal blockers')
            require(c.get('claim_record_sha256') == expected[c['claim_id']] and c.get('legal_status') in LEGAL and
                    c.get('claim_read_completely') is True and
                    isinstance(c.get('finding'),str) and bool(c['finding'].strip()), 'Stale/unknown claim verdict')
            if c['legal_status'] != 'KEEP':
                require(isinstance(c.get('blocker'),str) and bool(c['blocker'].strip()), 'Legal HOLD/source block requires reason')
            authorities = c.get('authorities',[])
            require(isinstance(authorities,list) and (c['legal_status'] != 'KEEP' or authorities),
                    'KEEP requires current official authority')
            for a in authorities:
                url = urlsplit(a.get('official_url',''))
                require(a.get('source_type') == 'PUBLIC_OFFICIAL' and url.scheme == 'https' and bool(url.hostname) and
                        all(isinstance(a.get(k),str) and a[k].strip() for k in
                            ('exact_section','law_checked_date','version_or_effective_date_status','evidence_path','evidence_sha256')),
                        'Incomplete current official authority')
                sources.append((a['evidence_path'],a['evidence_sha256']))
        if binding['author_nonlegal_classification'] is not None:
            classification = row.get('nonlegal_classification_review',{})
            require(type(classification.get('confirmed')) is bool and
                    isinstance(classification.get('finding'),str) and classification['finding'].strip() and
                    (classification['confirmed'] is True or completeness == 'OMISSIONS_FOUND'),
                    'Independent assessment of author nonlegal classification required')
        status = ('LEGAL_HOLD' if omissions or any(c['legal_status'] == 'LEGAL_HOLD' for c in claims) else
                  'SOURCE_BLOCKED' if any(c['legal_status'] == 'SOURCE_BLOCKED' for c in claims) else 'KEEP')
        if not claims and not omissions: status = 'NOT_APPLICABLE_NONLEGAL'
        require(row.get('legal_status') == status and summaries[uid] ==
                {'unit_id':uid,'completeness':completeness,'legal_status':status},
                'Unit summary cannot override claim/completeness findings')
    return sources


def validate_result(job, result):
    provenance(job,result)
    require(result.get('unit_hashes') == {uid:b['body_sha256'] for uid,b in job['unit_bindings'].items()},
            'Result note IDs/body hashes differ from assignment')
    rows = result.get('results',[])
    require(len(rows) == len(job['unit_ids']) and {r.get('unit_id') for r in rows} == set(job['unit_ids']),
            'Result requires exactly assigned note units')
    require(isinstance(result.get('worker_commit'),str) and re.fullmatch('[0-9a-f]{40}',result['worker_commit']),
            'Exact worker commit required')
    require(result.get('result_path') == OUTPUT+job['job_id']+'-result.json', 'Wrong result manifest path')
    evidence = result.get('evidence',{})
    require(isinstance(evidence.get('path'),str) and evidence['path'].startswith(OUTPUT) and
            isinstance(evidence.get('raw_sha256'),str) and re.fullmatch('[0-9a-f]{64}',evidence['raw_sha256']),
            'Bound note evidence required')


def committed_evidence(job, result, root, integrated=False):
    commit = result['worker_commit']; git(root,'cat-file','-e',commit+'^{commit}')
    git(root,'merge-base','--is-ancestor',job['base_commit'],commit)
    require(git(root,'rev-parse','refs/heads/'+job['worker_branch']) == commit, 'Worker branch/commit mismatch')
    changed = [p for p in git(root,'log','--format=','--name-only',job['base_commit']+'..'+commit).splitlines() if p]
    require(changed and all(p.startswith(OUTPUT) for p in changed), 'Worker commit changes outside note evidence scope')
    evidence = result['evidence']; path = evidence['path']; safe_path(root,path,output=True)
    original = git(root,'show',commit+':'+path,binary=True)
    require(raw_sha(original) == evidence['raw_sha256'], 'Worker evidence SHA mismatch')
    report = json.loads(original); sources = validate_evidence(job,result,report)
    for relative,sha in [(path,evidence['raw_sha256']),*sources]:
        safe_path(root,relative,output=True)
        original = git(root,'show',commit+':'+relative,binary=True)
        require(raw_sha(original) == sha, 'Worker source/evidence SHA mismatch')
        if integrated:
            require(safe_path(root,relative).read_bytes() == original and
                    git(root,'show','HEAD:'+relative,binary=True) == original, 'Uncommitted or unintegrated note evidence')
    return report


def submit(state, identifier, token, result_raw, root, inv, at=None):
    at = at or timestamp(); job = job_for(state,identifier); result = json.loads(result_raw)
    validate_result(job,result); current(job,inv,state); validate_reassessments(state,inv,root); sha = raw_sha(result_raw)
    if job['status'] in {'SUBMITTED','INTEGRATED'}:
        require(job.get('lease_token') == token and job['result'] == result and job['result_sha256'] == sha,
                'Conflicting note completion')
        return
    require_lease(job,token,at)
    committed_evidence(job,result,root)
    job.update(status='SUBMITTED',result=result,result_sha256=sha,submitted_at=at)
    event(state,'SUBMIT',at,job_id=identifier,result_sha256=sha,worker_commit=result['worker_commit'])


def integrate(state, identifier, root, inv, at=None):
    job = job_for(state,identifier); current(job,inv,state,allow_pending=True)
    validate_reassessments(state,inv,root)
    require(job['status'] in {'SUBMITTED','INTEGRATED'}, 'Submit valid evidence before integration')
    require(not any(j['sequence'] < job['sequence'] and j['status'] != 'INTEGRATED' for j in state['jobs']),
            'Integrate note jobs in assignment order')
    result = job['result']; validate_result(job,result); committed_evidence(job,result,root,integrated=True)
    raw = safe_path(root,result['result_path'],output=True).read_bytes()
    require(raw_sha(raw) == job['result_sha256'] and json.loads(raw) == result and
            git(root,'show','HEAD:'+result['result_path'],binary=True) == raw, 'Result SHA/committed manifest mismatch')
    if job['status'] == 'INTEGRATED': return
    at = at or timestamp(); job.update(status='INTEGRATED',integrated_commit=git(root,'rev-parse','HEAD'),integrated_at=at)
    event(state,'INTEGRATE',at,job_id=identifier,commit=job['integrated_commit'],result_sha256=job['result_sha256'])


def progress(state, inv, root=None):
    validate_state(state)
    if root is not None: validate_reassessments(state,inv,root)
    for job in state['jobs']:
        current(job,inv,state,allow_pending=True)
        if root is not None and job['status'] == 'INTEGRATED':
            integrate(state,job['job_id'],root,inv)
    from notes_census_reassessment import latest_jobs
    latest = latest_jobs(state)
    from notes_body_reassessment import selected_is_current, current_content_keep_count
    rows = [r for uid,j in latest.items() if j['status'] == 'INTEGRATED' and
            (not j.get('body_reassessment_id') or selected_is_current(j,inv))
            for r in j['result']['results'] if r['unit_id'] == uid]
    return {'total_note_units':inv['total_units'],'author_enumerated_units':len(inv['units']),
        'not_enumerated_units':inv['total_units']-len(inv['units']),
        'existing_current_body_content_keep_units':current_content_keep_count(state,inv),
        'independent_completeness_legal_processed_units':len(rows),
        'pending_census_reassessment_units':sum(bool(j.get('reassessment_id')) and j['status'] != 'INTEGRATED'
                                               for j in latest.values()),
        'pending_body_reassessment_units':sum(bool(j.get('body_reassessment_id')) and j['status']!='INTEGRATED'for j in latest.values()),
        'inactive_body_candidate_units':sum(bool(j.get('body_reassessment_id'))and not selected_is_current(j,inv)for j in latest.values()),
        'completeness':{s:sum(r['completeness'] == s for r in rows) for s in sorted(COMPLETE)},
        'legal':{s:sum(r['legal_status'] == s for r in rows) for s in sorted(UNIT_LEGAL)},
        'queue_jobs':{s:sum(j['status'] == s for j in state['jobs']) for s in ('QUEUED','LEASED','SUBMITTED','INTEGRATED')},
        'independence_status':'CONTROLLER_ATTESTED_DECLARATION_NOT_IDENTITY_PROOF',
        'question_audit_credit':0,'canonical_release_credit':0,
        'coverage_is_pass':False,'existing_content_keep_is_completeness_credit':False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--actor',help='Actual controller identity; mutations require /root')
    commands = parser.add_subparsers(dest='command',required=True)
    p = commands.add_parser('plan'); p.add_argument('--batches',type=int,default=1); p.add_argument('--size',type=int,default=5)
    p = commands.add_parser('claim')
    for name in ('worker','session','independence-basis'): p.add_argument('--'+name,required=True)
    p.add_argument('--auditor',default='GPT'); p.add_argument('--auditor-instance')
    p.add_argument('--known-author',action='append',default=[]); p.add_argument('--minutes',type=int,default=60)
    commands.add_parser('recover'); commands.add_parser('progress')
    p = commands.add_parser('reassess'); p.add_argument('--record',required=True)
    p = commands.add_parser('reassess-body'); p.add_argument('--record',required=True)
    p = commands.add_parser('preview-body'); p.add_argument('--record',required=True)
    for name in ('heartbeat','worktree','submit','integrate'):
        p = commands.add_parser(name); p.add_argument('--job',required=True)
        if name != 'integrate': p.add_argument('--token',required=True)
        if name == 'heartbeat': p.add_argument('--minutes',type=int,default=60)
        if name == 'worktree': p.add_argument('--destination',type=Path,required=True)
        if name == 'submit': p.add_argument('--result',type=Path,required=True)
    args = parser.parse_args(); root = args.root.resolve(); inv = inventory(root)
    if args.command == 'preview-body':
        from notes_body_reassessment import preview
        output=preview(root,args.record)
    elif args.command == 'progress':
        path = safe_path(root,STATE); state = json.loads(path.read_bytes()) if path.exists() else empty(root)
        validate_state(state,root); output = progress(state,inv,root)
    else:
        with checkpoint(root,args.actor) as state:
            validate_reassessments(state,inv,root)
            if args.command == 'reassess':
                from notes_census_reassessment import register
                output = register(state,inv,root,args.record)
            elif args.command == 'reassess-body':
                from notes_body_reassessment import register as register_body
                output=register_body(state,inv,root,args.record)
            elif args.command == 'plan': output = plan(state,inv,root,args.batches,args.size)
            elif args.command == 'claim': output = claim(state,inv,args.worker,args.session,args.independence_basis,
                args.auditor,args.auditor_instance,args.known_author,args.minutes)
            elif args.command == 'recover': output = recover(state)
            elif args.command == 'heartbeat': output = heartbeat(state,args.job,args.token,inv,args.minutes)
            elif args.command == 'worktree': output = prepare_worktree(state,args.job,args.token,inv,root,args.destination)
            elif args.command == 'submit': output = submit(state,args.job,args.token,args.result.read_bytes(),root,inv)
            else: output = integrate(state,args.job,root,inv)
    print(json.dumps(output,ensure_ascii=False,indent=2))


if __name__ == '__main__': main()
