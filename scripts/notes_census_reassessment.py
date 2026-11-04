"""Append-only census-only omission remediation; no legal blocker closure or release credit."""
import json

import note_review_queue as queue

PURPOSE = 'CENSUS_ONLY_OMISSION_REASSESSMENT'
LEDGER_FIELDS = ('unit_id','chapter_id','actual_effective_body_sha256',
    'atomic_claim_census_complete','atomic_claim_census_status','atomic_census_source',
    'atomic_census_notes_revision','atomic_claim_ids','atomic_source_blocked_count')


def latest_jobs(state):
    return {uid:job for job in state['jobs'] for uid in job['unit_ids']}


def validate_chain(state):
    """Only an explicitly pinned integrated predecessor may repeat a unit."""
    records = state.get('reassessments',[])
    queue.require(isinstance(records,list) and len({r['record']['reassessment_id'] for r in records}) == len(records),
                  'Duplicate census reassessment')
    by_id = {r['record']['reassessment_id']:r for r in records}
    latest = {}; used = set(); used_bodies=set()
    for job in state['jobs']:
        queue.require(job.get('purpose')!='BODY_CORRECTION_REASSESSMENT'or job.get('body_reassessment_id'),
                      'Body purpose requires an explicit body correction record')
        queue.require(len(job['unit_ids']) == len(set(job['unit_ids'])) and
                      set(job['unit_ids']) == set(job['unit_bindings']), 'Invalid note job unit scope')
        rid = job.get('reassessment_id')
        if job.get('body_reassessment_id'):
            from notes_body_reassessment import chain_link
            chain_link(state,job,latest,used_bodies)
        elif rid is not None:
            queue.require(rid in by_id and rid not in used and len(job['unit_ids']) == 1,
                          'Unknown/duplicate reassessment assignment')
            entry = by_id[rid]; record = entry['record']; uid = record['unit_id']
            previous = latest.get(uid)
            queue.require(job['unit_ids'] == [uid] and previous is not None and
                          previous['status'] == 'INTEGRATED' and previous['job_id'] == record['previous_job_id'] and
                          queue.digest(previous) == record['previous_job_sha256'] and
                          previous['unit_bindings'][uid] == record['previous_binding'] and
                          job['reassessment_record_sha256'] == entry['raw_sha256'],
                          'Reassessment predecessor/history changed')
            used.add(rid)
        else:
            queue.require(not set(job['unit_ids']) & set(latest), 'Repeated note unit without reassessment')
        latest.update({uid:job for uid in job['unit_ids']})
    queue.require(used == set(by_id) and
                  [j['reassessment_id'] for j in state['jobs'] if j.get('reassessment_id')] ==
                  [r['record']['reassessment_id'] for r in records],
                  'Reassessment has no unique append-ordered assignment')
    body_records=state.get('body_reassessments',[])
    queue.require(isinstance(body_records,list) and
                  len(body_records)==len({e['record']['body_reassessment_id']for e in body_records}) and
                  used_bodies=={e['record']['body_reassessment_id']for e in body_records} and
                  [j['body_reassessment_id']for j in state['jobs']if j.get('body_reassessment_id')]==
                  [e['record']['body_reassessment_id']for e in body_records],
                  'Body correction has no unique append-ordered assignment')
    # A multi-unit job appears repeatedly in latest.values(); deduplicate jobs first.
    owners = {j['job_id']:j for j in latest.values()}
    claims = [cid for j in owners.values() for uid,b in j['unit_bindings'].items()
              if latest[uid] is j for cid in b['claim_record_sha256s']]
    queue.require(len(claims) == len(set(claims)), 'Duplicate current claim ID across note units')


def disk_reader(root):
    def read(path,sha):
        raw = queue.safe_path(root,path).read_bytes()
        queue.require(queue.raw_sha(raw) == sha and queue.git(root,'show','HEAD:'+path,binary=True) == raw,
                      'Uncommitted or changed reassessment snapshot: '+path)
        return raw
    return read


def selected_record(root, uid, binding, read):
    census = json.loads(read(binding['census_path'],binding['census_sha256']))
    units = [u for u in census['units'] if u['unit_id'] == uid]
    claims = [c for c in census['claims'] if c['unit_id'] == uid]
    queue.require(len(units) == 1 and queue.digest(units[0]) == binding['census_unit_record_sha256'] and
                  units[0]['unit_content_sha256'] == binding['body_sha256'] and
                  len(claims) == len(binding['claim_record_sha256s']) and
                  {c['claim_id']:queue.digest(c) for c in claims} == binding['claim_record_sha256s'],
                  'Historical census unit/claim binding changed')
    return census,claims


def replacement_row(record,census):
    uid = record['unit_id']; unit = census['units'][0]; claims = census['claims']
    row = dict(record['previous_ledger_fields'])
    row.update(atomic_census_source=record['replacement']['census_path'],
               atomic_census_notes_revision=record['replacement']['notes_revision'],
               atomic_claim_census_status=unit['census_status'],atomic_claim_census_complete=True,
               atomic_claim_ids=[c['claim_id'] for c in claims],
               atomic_source_blocked_count=sum(c['review_status'] == 'SOURCE_BLOCKED' for c in claims))
    return row


def validate_record(state,record,root,notes,read):
    queue.require(record.get('schema_version') == 1 and record.get('purpose') == PURPOSE and
                  isinstance(record.get('reassessment_id'),str) and bool(record['reassessment_id'].strip()) and
                  isinstance(record.get('change_basis'),str) and bool(record['change_basis'].strip()),
                  'Explicit versioned census-only reassessment required')
    uid = record['unit_id']; previous = next((j for j in state['jobs'] if j['job_id'] == record['previous_job_id']),None)
    queue.require(previous is not None and previous['status'] == 'INTEGRATED' and
                  queue.digest(previous) == record['previous_job_sha256'] and
                  previous['unit_bindings'].get(uid) == record['previous_binding'],
                  'Reassessment must pin immutable integrated predecessor')
    binding = record['previous_binding']; result = previous['result']; queue.validate_result(previous,result)
    queue.require(record['body_sha256'] == binding['body_sha256'] and
                  record['previous_result'] == {'path':result['result_path'],'raw_sha256':previous['result_sha256']} and
                  record['previous_report'] == result['evidence'], 'Reassessment original raw bindings differ')
    queue.require(json.loads(read(result['result_path'],previous['result_sha256'])) == result,
                  'Reassessment original result differs')
    report = json.loads(read(result['evidence']['path'],result['evidence']['raw_sha256']))
    for path,sha in queue.validate_evidence(previous,result,report): read(path,sha)
    row = next(r for r in report['records'] if r['unit_id'] == uid)
    queue.require(row['completeness'] == 'OMISSIONS_FOUND', 'Census-only remediation requires independently identified omissions')
    actual = [u for c in notes['chapters'] for u in c['units'] if u['id'] == uid]
    queue.require(len(actual) == 1 and queue.raw_sha(actual[0]['body'].encode()) == binding['body_sha256'],
                  'Body changes are outside census-only reassessment')
    fields = record['previous_ledger_fields']
    queue.require(set(fields) == set(LEDGER_FIELDS) and fields['unit_id'] == uid and
                  queue.digest(fields) == binding['ledger_binding_sha256'], 'Original ledger binding differs')
    _,old_claims = selected_record(root,uid,binding,read)
    replacement = record['replacement']; raw = read(replacement['census_path'],replacement['census_sha256'])
    census = json.loads(raw)
    queue.require(replacement['census_path'] != binding['census_path'] and
                  replacement['census_sha256'] != binding['census_sha256'] and
                  replacement.get('notes_revision') == fields['atomic_census_notes_revision'] and
                  [u['unit_id'] for u in census['units']] == [uid] and
                  all(c['unit_id'] == uid for c in census['claims']), 'Replacement must be a versioned single-unit census')
    author = record.get('author_provenance',{})
    queue.require(set(author) == {'actor_id','session_id'} and
                  all(isinstance(v,str) and v.strip() for v in author.values()) and
                  census.get('author_provenance') == author, 'Known census author actor/session required')
    queue.require(census['units'][0]['census_status'] ==
                  'COMPLETE_AUTHOR_ENUMERATION_PENDING_INDEPENDENT_COMPLETENESS_CHECK',
                  'Replacement census cannot claim independent completion')
    for source in census.get('sources',{}).values():
        queue.require(source['official_url'].startswith('https://'), 'Replacement source must be official HTTPS')
        read(source['source_evidence'],source['source_evidence_sha256'])
    new_row = replacement_row(record,census)
    inv = queue.inventory(root,{'chapters':[{'units':actual}]},ledger_raw=(json.dumps(new_row)+'\n').encode())
    new_binding = inv['units'][uid]
    old = {c['claim_id']:c for c in old_claims}; new = {c['claim_id']:c for c in census['claims']}
    mapping = record['claim_mapping']; added = record['added_claim_ids']
    mapped = [cid for ids in mapping.values() for cid in ids]
    queue.require(set(mapping) == set(old) and all(isinstance(ids,list) and ids for ids in mapping.values()) and
                  len(mapped) == len(set(mapped)) and len(added) == len(set(added)) and
                  not set(mapped) & set(added) and set(mapped+added) == set(new),
                  'Every original claim must map exactly once; exact replacement claim delta required')
    normalize = lambda c:' '.join(c['statement_ko'].split())
    queue.require(all(normalize(c) for c in new.values()), 'Empty replacement proposition')
    queue.require(all(any(normalize(new[cid]) == normalize(claim) for cid in mapping[old_id])
                      for old_id,claim in old.items()),
                  'Census-only mapping must preserve every original proposition verbatim')
    changed = sorted(cid for old_id,ids in mapping.items() for cid in ids if queue.digest(new[cid]) != queue.digest(old[old_id]))
    proposition_delta = {cid for old_id,ids in mapping.items() for cid in ids if normalize(new[cid]) != normalize(old[old_id])}
    old_statements = {normalize(c) for c in old.values()}
    queue.require(all(normalize(new[cid]) not in old_statements for cid in added), 'Added claim merely repeats an original proposition')
    delta = proposition_delta | set(added)
    queue.require(record['changed_claim_ids'] == changed and bool(delta), 'No actual proposition delta or inaccurate claim delta')
    omissions = {queue.raw_sha(x.encode()):x for x in row['omissions']}
    resolutions = record['omission_resolutions']
    queue.require(len(resolutions) == len(omissions) and {r['omission_sha256'] for r in resolutions} == set(omissions) and
                  all(isinstance(r.get('explanation'),str) and r['explanation'].strip() and
                      isinstance(r.get('claim_ids'),list) and r['claim_ids'] and
                      len(r['claim_ids']) == len(set(r['claim_ids'])) and set(r['claim_ids']) <= delta for r in resolutions),
                  'Every exact original omission needs an actual changed/new proposition and explanation')
    carried = {}
    for claim in row['claims']:
        if claim['legal_status'] != 'KEEP':
            for cid in mapping[claim['claim_id']]:
                blockers = [*claim.get('inherited_legal_blockers',[]),dict(original_claim_id=claim['claim_id'],
                    legal_status=claim['legal_status'],finding=claim['finding'],blocker=claim['blocker'],
                    original_report_sha256=result['evidence']['raw_sha256'])]
                target = carried.setdefault(cid,[])
                for blocker in blockers:
                    if blocker not in target: target.append(blocker)
    return new_binding,carried


def validate_registered(state,root,notes,read=None):
    read = read or disk_reader(root); records = []
    for entry in state.get('reassessments',[]):
        record = json.loads(read(entry['record_path'],entry['raw_sha256']))
        queue.require(record == entry['record'], 'Captured reassessment differs from immutable record')
        context=notes
        if state.get('body_reassessments'):
            from notes_body_reassessment import historical_notes
            context=historical_notes(state,record['unit_id'],record['body_sha256'],notes,read)
        binding,carried = validate_record(state,record,root,context,read)
        job = next(j for j in state['jobs'] if j.get('reassessment_id') == record['reassessment_id'])
        previous = next(j for j in state['jobs'] if j['job_id'] == record['previous_job_id'])
        original_authors = set(previous.get('known_author_ids',[])) | set(record['previous_binding']['known_author_ids'])
        queue.require(original_authors <= set(job.get('known_author_ids',[])),
                      'Original body/source author provenance cannot be dropped')
        queue.require(job['unit_bindings'] == {record['unit_id']:binding} and
                      job.get('carried_legal_blockers') == {record['unit_id']:carried} and
                      job.get('reassessment_review') == {'reassessment_id':record['reassessment_id'],
                          'record_sha256':entry['raw_sha256'],'omission_resolutions':record['omission_resolutions']},
                      'Reassessment assignment bindings/blockers changed')
        queue.require(any(e.get('kind') == 'REGISTER_CENSUS_REASSESSMENT' and
                          e.get('job_id') == job['job_id'] and e.get('reassessment_id') == record['reassessment_id'] and
                          e.get('record_sha256') == entry['raw_sha256'] for e in state['events']),
                      'Missing captured reassessment registration provenance')
        records.append(record)
    return records


def registered_specs(root,notes):
    """Builder hook: committed registration selects the future census in one pass."""
    path = queue.safe_path(root,queue.STATE)
    if not path.exists(): return []
    state = json.loads(path.read_bytes()); queue.validate_state(state)
    if not state.get('reassessments'): return []
    read = disk_reader(root); read(queue.STATE,queue.raw_sha(path.read_bytes()))
    return [dict(path=r['replacement']['census_path'],notes_revision=r['replacement']['notes_revision'],
                 supersedes={r['unit_id']:r['previous_binding']['census_path']})
            for r in validate_registered(state,root,notes,read)]


def register(state,inv,root,record_path,notes=None,at=None):
    """Root checkpoint mutation; never authors a census or reviews it."""
    from notes_revision import load_notes
    queue.validate_state(state,root); notes = notes if notes is not None else load_notes(root)
    read = disk_reader(root); raw = queue.safe_path(root,record_path).read_bytes(); sha = queue.raw_sha(raw)
    record = json.loads(read(record_path,sha)); rid = record['reassessment_id']
    existing = next((e for e in state.get('reassessments',[]) if e['record']['reassessment_id'] == rid),None)
    if existing:
        for job in state['jobs']: queue.current(job,inv,state,allow_pending=True)
        queue.require(existing == {'record_path':record_path,'raw_sha256':sha,'record':record}, 'Conflicting reassessment registration')
        validate_registered(state,root,notes,read)
        return next(j['job_id'] for j in state['jobs'] if j.get('reassessment_id') == rid)
    queue.require(all(j['status'] == 'INTEGRATED' or
                      (j.get('reassessment_id') and j['status'] == 'QUEUED' and j['attempt'] == 0)
                      for j in state['jobs']), 'Finish current wave before reassessment registration')
    for job in state['jobs']: queue.current(job,inv,state,allow_pending=True)
    validate_registered(state,root,notes,read)
    previous = latest_jobs(state).get(record['unit_id'])
    queue.require(previous is not None and previous['job_id'] == record['previous_job_id'], 'Reassessment predecessor is not current')
    # Preserve original worker Git/actor/commit checks in controller operations.
    queue.integrate(state,previous['job_id'],root,inv)
    binding,carried = validate_record(state,record,root,notes,read)
    other_claims = {cid for uid,b in inv['units'].items() if uid != record['unit_id'] for cid in b['claim_record_sha256s']}
    other_claims.update(cid for uid,j in latest_jobs(state).items() if uid != record['unit_id']
                        for cid in j['unit_bindings'][uid]['claim_record_sha256s'])
    queue.require(not set(binding['claim_record_sha256s']) & other_claims, 'Replacement claim ID belongs to another unit')
    at = at or queue.timestamp(); uid = record['unit_id']
    identifier = 'review-independent-notes-reassessment-'+queue.digest({'record_sha256':sha})[:16]
    state.setdefault('reassessments',[]).append({'record_path':record_path,'raw_sha256':sha,'record':record})
    state['jobs'].append(dict(job_id=identifier,stage=queue.STAGE,sequence=len(state['jobs'])+1,
        unit_bindings={uid:binding},unit_ids=[uid],status='QUEUED',attempt=0,base_commit=queue.git(root,'rev-parse','HEAD'),
        inventory_ledger_sha256=inv['ledger_sha256'],created_at=at,reassessment_id=rid,
        reassessment_record_sha256=sha,carried_legal_blockers={uid:carried},
        known_author_ids=sorted(set(previous.get('known_author_ids',[])) |
                                set(record['previous_binding']['known_author_ids']) | set(binding['known_author_ids'])),
        reassessment_review={'reassessment_id':rid,'record_sha256':sha,'omission_resolutions':record['omission_resolutions']}))
    queue.event(state,'REGISTER_CENSUS_REASSESSMENT',at,job_id=identifier,reassessment_id=rid,record_sha256=sha)
    queue.validate_state(state,root)
    return identifier
