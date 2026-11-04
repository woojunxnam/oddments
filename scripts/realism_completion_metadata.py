"""Committed-only exact146 realism and exact4 legal supplements; no primary edits."""
import copy
import json
import re

import review_queue as q
import realism_completion_review as route
from realism_completion_legal4 import LEGAL_IDS
from notes_published15_closure import snapshotted


@snapshotted
def load_metadata(root,primary_records,public,*,source_bindings=None):
    result={'assessments':{},'records':[],'legal_assessments':{},'legal_records':[],
        'source_bindings':{},'prior_realism_negative_ids':[],'prior_realism_pass_ids':[],'progress':dict(scope_units=146,integrated_units=0,pending_units=146,
        fresh_realism_pass=0,fresh_realism_fail=0,fresh_realism_not_assessed=0,fresh_realism_hold=0,
        new_legal_key_assessed=0,canonical_release_credit=0,new_original_read_credit=0)}
    if not(root/route.STATE).exists():
        route.require(not(root/route.SCOPE).exists(),'A retained realism scope cannot lose its queue')
        return result
    retained={}
    def read(path,expected=None):
        raw=route.disk_read(root,path,expected)
        route.require(path not in retained or retained[path]==route.sha(raw),'Conflicting retained source bytes')
        retained[path]=route.sha(raw);return raw
    state=route.read_json(read,route.STATE);scope=route.read_json(read,route.SCOPE,state['realism_completion_scope']['raw_sha256'])
    primary={r['question_id']:r for r in primary_records};route.require(len(primary)==len(primary_records),'Duplicate primary reviews')
    route.validate_state(state,scope)
    current,collections,canonical=route.questions(root,read)
    prior=route.prior_supplementary(root,primary_records,public,collections)
    route.validate_scope(scope,primary,public,read,prior)
    result['prior_realism_negative_ids']=sorted(uid for uid,proofs in prior.items()if any(p['realism_verdict']in {'FAIL','HOLD','MINOR_EDIT','MAJOR_REWRITE'}for p in proofs))
    result['prior_realism_pass_ids']=sorted(uid for uid,proofs in prior.items()if any(p['realism_verdict']=='PASS'for p in proofs))
    route.require(all(current[uid]==public[uid]for uid in route.IDS),'Builder/current question source mismatch')
    inputs=route.read_json(read,route.INPUTS,scope['nearest_inputs']['raw_sha256'])
    route.require(inputs==route.nearest_inputs(current,canonical),'Current439/2349 nearest comparison inventory changed')
    for job in state['jobs']:
        if job['status']!='INTEGRATED':continue
        route.require(all(j['status']=='INTEGRATED'for j in state['jobs']if j['sequence']<job['sequence']),'Incomplete native predecessor')
        route.require(re.fullmatch('[0-9a-f]{40}',job.get('integrated_commit',''))and
            route.moment(job['integrated_at'])and any(e.get('kind')=='INTEGRATE'and
                e.get('job_id')==job['job_id']and e.get('commit')==job['integrated_commit']for e in state['events']),
            'Missing captured actual native integration')
        envelope=job['result'];q.validate_result(job,envelope);route.no_credit(envelope)
        route.require(envelope.get('actor_provenance')==job['actor_provenance']and
            envelope.get('auditor_instance')==job['auditor_instance'],'Actual envelope actor changed')
        route.require(any(e.get('kind')=='SUBMIT'and e.get('job_id')==job['job_id']and
            e.get('result_sha256')==q.digest(envelope)for e in state['events']),'Missing native submission event')
        route.require(envelope.get('result_path')==job['output_prefix']+'result.json'and
            route.read_json(read,envelope['result_path'],job['result_raw_sha256'])==envelope,'Committed envelope changed')
        report_paths={r['evidence_path']for r in envelope['results']}
        route.require(report_paths=={job['output_prefix']+'report.json'},'Own bounded report path required')
        for reference in envelope['results']:
            report=route.read_json(read,reference['evidence_path'],reference['evidence_sha256'])
            q.validate_independent_evidence(job,reference,report)
        route.validate_report(job,scope,report,read,inputs,public)
        for row in report['records']:
            uid=row['question_id'];route.require(uid not in result['assessments'],'Original realism cannot count twice')
            proof=dict(record=copy.deepcopy(row),report_path=reference['evidence_path'],report_sha256=reference['evidence_sha256'],
                result_path=envelope['result_path'],result_raw_sha256=job['result_raw_sha256'],
                actor_provenance=copy.deepcopy(report['actor_provenance']),auditor_instance=report['auditor_instance'],
                supplementary_only=True,does_not_override_primary=True,canonical_release_credit=0)
            result['assessments'][uid]=proof;result['records'].append(copy.deepcopy(row))
            if uid in LEGAL_IDS:
                result['legal_assessments'][uid]=copy.deepcopy(proof);result['legal_records'].append(copy.deepcopy(row))
    rows=result['records'];p=result['progress'];p.update(integrated_units=len(rows),pending_units=146-len(rows),
        fresh_realism_pass=sum(r['realism_review']['verdict']=='PASS'for r in rows),
        fresh_realism_fail=sum(r['realism_review']['verdict']=='FAIL'for r in rows),
        fresh_realism_not_assessed=sum(r['realism_review']['verdict']=='NOT_ASSESSED'for r in rows),
        fresh_realism_hold=sum(r['realism_review']['verdict']=='HOLD'for r in rows),
        new_legal_key_assessed=sum(r['legal_review']['existing_answer_correct']!='NOT_ASSESSED'for r in result['legal_records']))
    result['source_bindings']=retained
    if source_bindings is not None:
        route.require(all(source_bindings.get(p,h)==h for p,h in retained.items()),'Conflicting realism source binding')
        source_bindings.update(retained)
    return result


def apply_metadata(rows,primary,supplement,base_realism_pass):
    """Separate annotations; positive reviews never restore a default or erase HOLD."""
    original={r['question_id']:r for r in primary}
    passed={uid for uid,p in original.items()if p['realism_review']['verdict']=='PASS'}
    fresh_pass={uid for uid,p in supplement['assessments'].items()if p['record']['realism_review']['verdict']=='PASS'}
    route.require(not{uid for uid in fresh_pass if original[uid]['realism_review']['verdict']=='FAIL'},'Prior FAIL cannot be overridden')
    for row in rows:
        proof=supplement['assessments'].get(row['question_id'])
        if proof is not None:
            row['independent_legacy_realism_supplementary_assessment']=copy.deepcopy(proof)
            # The original verdict, disposition, key, notices and publication
            # fields intentionally remain authoritative and unchanged.
    primary_blocked={uid for uid in fresh_pass if original[uid]['realism_review']['verdict']in {'HOLD','MINOR_EDIT','MAJOR_REWRITE','FAIL'}}
    secondary_blocked=fresh_pass&set(supplement['prior_realism_negative_ids'])
    blocked=primary_blocked|secondary_blocked
    passed.update(supplement['prior_realism_pass_ids'])
    return dict(raw_primary_realism_pass=sum(p['realism_review']['verdict']=='PASS'for p in primary),
        previous_effective_realism_pass=base_realism_pass,
        effective_realism_pass=base_realism_pass+len(fresh_pass-passed-blocked),
        effective_realism_pass_basis='EXISTING_EFFECTIVE_UNION_NEW_VERIFIED_ELIGIBLE_PASS_NOT_NEGATIVE_OVERRIDE_OR_CANONICAL_RELEASE',
        fresh_pass_with_preserved_primary_realism_hold=len(primary_blocked),
        fresh_pass_with_preserved_existing_supplementary_negative=len(secondary_blocked),
        previously_counted_realism_pass_not_recounted=len(fresh_pass&passed),
        **supplement['progress'])


def original_records(root,read):
    from legacy_independent_metadata import integrated_sources
    reports=integrated_sources(root)
    for name in ('pub05-14-independent-review.json','wave2-independent-review.json','wave5-independent-review.json'):
        reports.append(json.loads(read('reports/full-corpus-review/'+name)))
    return [row for report in reports for row in report['records']]


def validate_archive_containment(selection,supplement):
    """A new realism FAIL needs its actual source warning; pending is no FAIL."""
    route.require(not set(selection['recommended_ids'])&set(route.IDS),
                  'The bounded completion tranche cannot return to default practice')
    def matches(notice,uid,proof):
        if (uid in notice.get('question_ids',[])and notice.get('issue_type')=='INDEPENDENT_REVIEW_FINDING'and
            notice.get('review_source')==proof['report_path']and notice.get('review_source_sha256')==proof['report_sha256']and
            notice.get('question_record_hashes',{}).get(uid)==proof['record']['record_sha256']):return True
        return any(matches(previous,uid,proof)for previous in notice.get('previous_notices',[]))
    for uid,proof in supplement['assessments'].items():
        if proof['record']['realism_review']['verdict']!='FAIL':continue
        if uid in LEGAL_IDS:
            route.require(any(h['question_id']==uid for h in selection.get('safety_holds',[])),
                          'Fixed4 must retain its original nonlegacy safety hold')
        else:
            route.require(any(matches(n,uid,proof)for n in selection['archive_review_notices']),
                          'Fresh realism FAIL requires an actual source-bound archive notice: '+uid)
