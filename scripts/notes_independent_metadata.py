"""Read committed, integrated note review metadata without granting release credit.

The controller retains its original worker-commit/branch and actor checks. This
consumer revalidates current committed bytes and captured bindings, so a shallow
checkout does not need the controller's local worker branches or old Git objects.
"""
from collections import Counter
import json
import re

import note_review_queue as queue


def notice_for(completeness, legal_status, omission_count):
    parts = []
    if completeness == 'OMISSIONS_FOUND':
        parts.append(f'독립 검토에서 본문의 법적 주장에 대한 census 누락 지적 {omission_count}건이 나왔습니다. 이 절의 주장 목록은 보완이 필요합니다.')
    if legal_status == 'LEGAL_HOLD':
        parts.append('독립 법규 검토가 보류 상태입니다. 확정된 법규 판단으로 암기하지 말고 보류 사유를 확인하세요.')
    elif legal_status == 'SOURCE_BLOCKED':
        parts.append('독립 검토에서도 근거를 확인하지 못한 법적 주장이 있습니다. 해당 주장은 확인 보류 상태입니다.')
    return ' '.join(parts) or None


def evidence_bindings(value):
    """Include every authority payload/text and other bound review evidence."""
    if isinstance(value,dict):
        for key,path in value.items():
            if not isinstance(path,str): continue
            if key.endswith('_path'):
                sha_key = key[:-5]+'_sha256'
                if sha_key in value and (path.startswith(queue.OUTPUT) or key in {'evidence_path','extracted_text_path'}):
                    yield path,value[sha_key]
            elif key == 'path' and path.startswith(queue.OUTPUT):
                for sha_key in ('raw_sha256','sha256'):
                    if sha_key in value: yield path,value[sha_key]
        for child in value.values(): yield from evidence_bindings(child)
    elif isinstance(value,list):
        for child in value: yield from evidence_bindings(child)


def load_metadata(root, notes=None, ledger_raw=None, source_bindings=None):
    """Return current integrated reviews and pending safety markers without mutation."""
    inv = queue.inventory(root,notes,ledger_raw=ledger_raw)
    result = {'units':{},'progress':{
        'total_units':inv['total_units'],'author_enumerated_units':len(inv['units']),
        'existing_current_body_content_keep_units':inv['existing_content_keep_units'],
        'processed_units':0,'complete_units':0,'omissions_found_units':0,
        'legal_keep_units':0,'legal_hold_units':0,'source_blocked_units':0,
        'assessed_claims':0,'claim_keep_count':0,'claim_legal_hold_count':0,'claim_source_blocked_count':0,
        'not_applicable_nonlegal_units':0,'question_audit_credit':0,'canonical_release_credit':0,
        'coverage_is_legal_pass':False,'existing_content_keep_is_completeness_credit':False,
        'basis':'COMMITTED_INTEGRATED_CURRENT_BINDINGS_CONTROLLER_ATTESTED_NOT_NEW_IDENTITY_PROOF'}}
    path = queue.safe_path(root,queue.STATE)
    if not path.exists(): return result
    cache = {}
    def committed(relative,sha=None,output=False):
        queue.safe_path(root,relative,output=output)
        if relative not in cache:
            raw = queue.safe_path(root,relative).read_bytes()
            queue.require(queue.git(root,'show','HEAD:'+relative,binary=True) == raw,
                          'Uncommitted independent note metadata/evidence: '+relative)
            cache[relative] = raw
        raw = cache[relative]
        queue.require(sha is None or queue.raw_sha(raw) == sha,
                      'Independent note metadata/evidence raw SHA changed: '+relative)
        return raw
    state = json.loads(committed(queue.STATE))
    # Publication copies retain the controller's original absolute root string.
    queue.validate_state(state)
    from notes_census_reassessment import validate_registered, latest_jobs
    if state.get('reassessments'):
        validate_registered(state,root,inv['notes'],committed)
    if state.get('body_reassessments'):
        from notes_body_reassessment import validate_registered as validate_bodies
        validate_bodies(state,root,inv['notes'],committed)
    if state.get('inactive_census_successors'):
        from notes_inactive_census_successor import validate_registered as validate_inactive
        validate_inactive(state,root,inv['notes'],committed)
    latest = latest_jobs(state)
    revised_units = {e['record']['unit_id'] for e in state.get('reassessments',[])}
    body_units={e['record']['unit_id']for e in state.get('body_reassessments',[])}
    revised_units |= body_units
    for job in state['jobs']:
        if job['status'] != 'INTEGRATED': continue
        queue.require(all(j['status'] == 'INTEGRATED' for j in state['jobs'] if j['sequence'] < job['sequence']),
                      'Integrated note publication sequence differs from controller order')
        queue.require(re.fullmatch('[0-9a-f]{40}',job.get('integrated_commit','')) and job.get('integrated_at') and
                      any(e.get('kind') == 'INTEGRATE' and e.get('job_id') == job['job_id'] and
                          e.get('commit') == job['integrated_commit'] and e.get('result_sha256') == job.get('result_sha256')
                          for e in state['events']), 'Missing captured note integration provenance')
        queue.current(job,inv,state,allow_pending=True)
        authors = set(job.get('known_author_ids',())) | {
            a for b in job['unit_bindings'].values() for a in b['known_author_ids']}
        actor = job.get('actor_provenance',{})
        queue.require(isinstance(job.get('controller_independence_basis'),str) and job['controller_independence_basis'].strip() and
                      not {actor.get('actor_id'),actor.get('session_id'),job.get('auditor_instance')} & authors,
                      'Missing controller independence basis or known author self-review')
        envelope = job['result']; queue.validate_result(job,envelope)
        raw = committed(envelope['result_path'],job['result_sha256'],output=True)
        queue.require(json.loads(raw) == envelope, 'Captured independent note result differs from envelope')
        report_binding = envelope['evidence']
        report = json.loads(committed(report_binding['path'],report_binding['raw_sha256'],output=True))
        sources = queue.validate_evidence(job,envelope,report)
        for relative,sha in set(sources) | set(evidence_bindings(report)):
            committed(relative,sha,output=True)
        for uid,binding in job['unit_bindings'].items():
            committed(binding['census_path'],binding['census_sha256'])
        for record in report['records']:
            uid = record['unit_id']; counts = Counter(c['legal_status'] for c in record['claims'])
            findings = [dict(claim_id=c['claim_id'],legal_status=c['legal_status'],
                             finding=c['finding'],blocker=c.get('blocker'))
                        for c in record['claims'] if c['legal_status'] != 'KEEP']
            notice = notice_for(record['completeness'],record['legal_status'],len(record['omissions']))
            history = []
            if uid in result['units']:
                previous = result['units'][uid]
                history = previous.pop('review_history',[]) + [{**previous,'current_review_valid':False}]
            result['units'][uid] = dict(
                completeness=record['completeness'],legal_status=record['legal_status'],
                omission_count=len(record['omissions']),omissions=record['omissions'],findings=findings,
                claim_counts={status:counts[status] for status in sorted(queue.LEGAL)},
                requires_review=notice is not None,notice=notice,
                report_path=report_binding['path'],report_sha256=report_binding['raw_sha256'],
                result_path=envelope['result_path'],result_sha256=job['result_sha256'],
                body_sha256=job['unit_bindings'][uid]['body_sha256'],
                census_sha256=job['unit_bindings'][uid]['census_sha256'],
                actor_provenance=actor,auditor_instance=job['auditor_instance'],
                basis='INTEGRATED_CURRENT_BINDING_CONTROLLER_ATTESTED_DECLARATION',
                question_audit_credit=0,canonical_release_credit=0)
            if uid in revised_units:
                result['units'][uid].update(current_review_valid=True,job_id=job['job_id'],review_history=history)
            if job.get('body_reassessment_id')or job.get('inactive_census_successor_id'):
                from notes_body_reassessment import selected_is_current, BLOCKER
                target=result['units'][uid]
                target.update(candidate_review_valid=True,body_reassessment_id=job.get('body_reassessment_id'),
                              publication_blocker=BLOCKER)
                if job.get('inactive_census_successor_id'):
                    target.pop('body_reassessment_id',None)
                    target['inactive_census_successor_id']=job['inactive_census_successor_id']
                if not selected_is_current(job,inv):
                    target.update(current_review_valid=False,candidate_legal_status=record['legal_status'],
                        legal_status='LEGAL_HOLD',requires_review=True,
                        basis='INACTIVE_BODY_CANDIDATE_INDEPENDENTLY_REVIEWED_NOT_CURRENT_OR_PUBLISHED',
                        notice='교정 후보의 독립 검토는 보존됐지만 활성 본문과 아직 결박되지 않았습니다. 기존 본문·새 후보 모두 현재 credit를 승계하지 않으며 별도 공개 body migration까지 검토 보류합니다.')
    for uid,job in latest.items():
        queue.current(job,inv,state,allow_pending=True)
        if not (job.get('reassessment_id')or job.get('body_reassessment_id')or job.get('inactive_census_successor_id')) or job['status'] == 'INTEGRATED': continue
        previous = result['units'][uid]
        history = previous.pop('review_history',[]) + [{**previous,'current_review_valid':False}]
        result['units'][uid] = dict(previous,current_review_valid=False,review_history=history,
            job_id=job['job_id'],completeness='PENDING_REASSESSMENT',legal_status='LEGAL_HOLD',
            claim_counts={s:0 for s in sorted(queue.LEGAL)},requires_review=True,
            census_sha256=job['unit_bindings'][uid]['census_sha256'],
            basis='CENSUS_ONLY_REASSESSMENT_PENDING_FRESH_INDEPENDENT_REVIEW',
            notice='census 누락 보완본의 새 독립 완전성 검토가 대기 중입니다. 기존 누락 지적과 미해결 법규 보류는 이력에 보존되며, 이 절은 검토 보류 상태입니다.')
        if job.get('body_reassessment_id'):
            from notes_body_reassessment import BLOCKER
            result['units'][uid].update(completeness='PENDING_BODY_CORRECTION_REASSESSMENT',
                body_sha256=job['unit_bindings'][uid]['body_sha256'],candidate_review_valid=False,
                publication_blocker=BLOCKER,basis='BODY_CORRECTION_PENDING_FULL_FRESH_NON_AUTHOR_REVIEW',
                notice='본문 교정 후보의 전문·모든 claim·기존 법규 negative·관련 derived 자료에 대한 새 non-author 검토가 대기 중입니다. 원래 KEEP는 승계하지 않으며 이 절은 daily 학습에서 제외되는 검토 보류 상태입니다.')
        if job.get('inactive_census_successor_id'):
            from notes_body_reassessment import BLOCKER
            result['units'][uid].update(completeness='PENDING_INACTIVE_BODY_CENSUS_SUCCESSOR',
                body_sha256=job['unit_bindings'][uid]['body_sha256'],candidate_review_valid=False,
                inactive_census_successor_id=job['inactive_census_successor_id'],publication_blocker=BLOCKER,
                basis='INACTIVE_BODY_CENSUS_PENDING_FULL_FRESH_REVIEW_NOT_ACTIVE',
                notice='비활성 교정 본문의 25개 주장 목록에 대한 새 독립 검토가 대기 중입니다. 활성 M 본문은 그대로이며, 기존 누락과 법적 보류를 보존하고 현재 credit 없이 daily 학습에서 제외합니다.')
    rows = [r for r in result['units'].values() if r.get('current_review_valid',True)]; p = result['progress']
    if revised_units:
        p['pending_census_reassessment_units'] = sum(not r.get('current_review_valid',True)for uid,r in result['units'].items()if uid not in body_units)
        p['historical_review_records'] = sum(len(j['unit_ids']) for j in state['jobs'] if j['status'] == 'INTEGRATED')
    if body_units:
        from notes_body_reassessment import current_content_keep_count, selected_is_current
        p['existing_current_body_content_keep_units']=current_content_keep_count(state,inv)
        p['pending_census_reassessment_units']=sum(bool(j.get('reassessment_id'))and j['status']!='INTEGRATED'for j in latest.values())
        p['pending_body_reassessment_units']=sum(bool(latest[uid].get('body_reassessment_id'))and latest[uid]['status']!='INTEGRATED'for uid in body_units)
        if state.get('inactive_census_successors'):
            p['pending_inactive_census_successor_units']=sum(bool(j.get('inactive_census_successor_id'))and j['status']!='INTEGRATED'for j in latest.values())
        p['inactive_body_candidate_units']=sum(bool(latest[uid].get('body_reassessment_id')or latest[uid].get('inactive_census_successor_id'))and not selected_is_current(latest[uid],inv)for uid in body_units)
        p['reviewed_body_candidates_not_current_credit']=sum(bool(latest[uid].get('body_reassessment_id')or latest[uid].get('inactive_census_successor_id'))and result['units'][uid].get('candidate_review_valid',False)and
                                                            not result['units'][uid]['current_review_valid']for uid in body_units)
    p.update(processed_units=len(rows),complete_units=sum(r['completeness'] == 'COMPLETE' for r in rows),
             omissions_found_units=sum(r['completeness'] == 'OMISSIONS_FOUND' for r in rows),
             legal_keep_units=sum(r['legal_status'] == 'KEEP' for r in rows),
             legal_hold_units=sum(r['legal_status'] == 'LEGAL_HOLD' for r in rows),
             source_blocked_units=sum(r['legal_status'] == 'SOURCE_BLOCKED' for r in rows),
             not_applicable_nonlegal_units=sum(r['legal_status'] == 'NOT_APPLICABLE_NONLEGAL' for r in rows))
    p.update(assessed_claims=sum(sum(r['claim_counts'].values()) for r in rows),
             claim_keep_count=sum(r['claim_counts']['KEEP'] for r in rows),
             claim_legal_hold_count=sum(r['claim_counts']['LEGAL_HOLD'] for r in rows),
             claim_source_blocked_count=sum(r['claim_counts']['SOURCE_BLOCKED'] for r in rows))
    if source_bindings is not None:
        source_bindings.update({relative:queue.raw_sha(raw)for relative,raw in cache.items()})
    return result


def notices_for_units(unit_ids, reviews):
    """Small rendering adapter for study/refresh records linked to note units."""
    return [dict(unit_id=uid,notice=reviews[uid]['notice'],report_path=reviews[uid]['report_path'],
                 completeness=reviews[uid]['completeness'],legal_status=reviews[uid]['legal_status'])
            for uid in dict.fromkeys(unit_ids) if uid in reviews and reviews[uid]['requires_review']]
