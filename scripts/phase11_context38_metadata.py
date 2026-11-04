"""Exact38 context-conditioned primary exclusion and genuinely fresh supplementary review."""
import copy
import json
import re
from datetime import datetime
from urllib.parse import urlsplit

import review_queue as queue
from procedural_secondary_metadata import (committed_reader, counts, evidence_bindings,
    no_release, principals, require, sha)

STATE = 'reports/full-corpus-review/phase11-context38-recheck-work-queue.json'
PREFIX = 'reports/full-corpus-review/'
IDS = tuple(f'MA-EXP-{i:04d}' for i in range(321,361) if i not in {338,339})
ACTOR = '/root/fresh_d_remaining38'
JOB_ID = 'review-independent-legacy-phase11-context38-f2f730cb3b7befe7'
PURPOSE = 'FIXED_PHASE11_CONTEXT38_FRESH_SECONDARY_REVIEW_NO_RELEASE_OVERRIDE'
PARENTS = {qid: ('recovered-phase11-d-review.json', '/root/recover_d_review',
    'PRIOR_CONCLUSION_EXPOSURE_REQUIRES_GENUINELY_FRESH_SESSION') for qid in IDS}
DISCLOSURE = PREFIX+'resume-20261104/d38-aggregate-exposure-disclosure.json'
CHECKPOINT = PREFIX+'executor-blocked-checkpoint-20261104.json'
CHECKPOINT_SHA = 'd19f2ae49019a14e8b1a90cc0aa947271a7b198e42e83874cd47bd130a8202e9'


def validate_disclosure(read,scope):
    binding = scope.get('exposure_disclosure',{})
    require(binding.get('path') == DISCLOSURE and isinstance(binding.get('raw_sha256'),str) and
            re.fullmatch('[0-9a-f]{64}',binding['raw_sha256']), 'Wrong context exposure disclosure path/hash')
    value = json.loads(read(DISCLOSURE,binding.get('raw_sha256')))
    require(value.get('schema_version') == 1 and
            value.get('purpose') == 'ROOT_ATTESTED_AGGREGATE_PRIOR_CONCLUSION_EXPOSURE_NO_FRESH_CREDIT' and
            value.get('controller_actor') == '/root' and value.get('context_conditioned_actor') == '/root/recover_d_review' and
            value.get('spawn_context') == 'fork_turns_all' and value.get('question_ids') == list(IDS) and
            value.get('actual_new_reviewer') == ACTOR and type(value.get('primary_fresh_key_credit')) is int and
            value['primary_fresh_key_credit'] == 0 and type(value.get('canonical_release_credit')) is int and
            value['canonical_release_credit'] == 0 and isinstance(value.get('reason'),str) and value['reason'].strip(),
            'Actual root aggregate exposure declaration changed')
    require(datetime.fromisoformat(value['observed_at_utc']).tzinfo is not None,
            'Actual aware exposure observation timestamp required')
    require(value.get('checkpoint') == {'path':CHECKPOINT,'raw_sha256':CHECKPOINT_SHA} and
            value.get('parent_report',{}).get('path') == PREFIX+'recovered-phase11-d-review.json' and
            isinstance(value['parent_report'].get('raw_sha256'),str) and
            re.fullmatch('[0-9a-f]{64}',value['parent_report']['raw_sha256']),
            'Actual checkpoint/parent exposure bindings changed')
    old = json.loads(read(CHECKPOINT,CHECKPOINT_SHA))
    previous = [row for row in old['next_question_wave']['workers'] if row['letter'] == 'd']
    require(len(previous) == 1 and previous[0]['actor'] == '/root/independent_wave11_d' and
            previous[0]['ids'] == 'MA-EXP-0321..0360' and previous[0]['legal'] == {'keep':38,'hold':2} and
            previous[0]['keys'] == {'yes':38,'ambiguous':2} and
            previous[0]['ambiguous_ids'] == ['MA-EXP-0338','MA-EXP-0339'] and
            value.get('prior_summary') == dict(assigned_count=40,legal_keep=38,legal_hold=2,key_yes=38,
                key_ambiguous=2,ambiguous_ids=['MA-EXP-0338','MA-EXP-0339']),
            'Prior aggregate evidence no longer supports the exact38 inferred exposure')
    read(value['parent_report']['path'],value['parent_report']['raw_sha256'])
    return value,binding


def combine_metadata(primary,*sources):
    """Exclude disclosed conditioned primary keys; union actual fresh results only."""
    from phase11_secondary_metadata import combine_metadata as combine_unconditioned
    excluded = set()
    for source in sources:
        ids = set(source.get('excluded_primary_key_ids',[]))
        require(not ids or ids == set(IDS), 'Context exclusion scope must be the exact38')
        require(not excluded.intersection(ids), 'Repeated context-conditioned primary exclusions')
        excluded.update(ids)
    adjusted = copy.deepcopy(primary)
    for row in adjusted:
        if row['question_id'] in excluded:
            row['legal_review']['existing_answer_correct'] = 'NOT_ASSESSED'
    result = combine_unconditioned(adjusted,*sources)
    result['excluded_primary_key_ids'] = sorted(excluded)
    original = {row['question_id']:row for row in primary}
    require(excluded <= set(original), 'Excluded primary keys have no original history')
    original_pass = {qid for qid,row in original.items() if row.get('realism_review',{}).get('verdict') == 'PASS'}
    fresh_pass = {row['question_id'] for source in sources for row in source['records']
                  if row['question_id'] in excluded and row['realism_review'].get('verdict') == 'PASS'}
    conflicting = {qid for qid in fresh_pass if original[qid].get('realism_review',{}).get('verdict') == 'FAIL'}
    result['effective_realism_pass'] = len((original_pass-excluded)|(fresh_pass-conflicting))
    if excluded:
        result['progress'].update(raw_primary_key_assessed=sum(
            row['legal_review']['existing_answer_correct'] != 'NOT_ASSESSED' for row in primary),
            excluded_context_conditioned_primary_key_ids=sorted(excluded),
            excluded_context_conditioned_primary_key_count=len(excluded),
            raw_primary_realism_pass=len(original_pass),
            excluded_context_conditioned_primary_realism_pass=len(original_pass&excluded),
            fresh_context38_realism_pass=len(fresh_pass),
            fresh_context38_pass_with_preserved_primary_fail=len(conflicting),
            effective_realism_pass=result['effective_realism_pass'])
    return result


def validate_default_safety(default_ids,metadata):
    require(not set(default_ids).intersection(metadata['excluded_primary_key_ids']),
            'Context-conditioned primary cannot return to default through supplementary evidence')


def validate_reviewer(scope,job,questions,previous_instances=()):
    reviewer = scope.get('fresh_reviewer',{})
    actor = reviewer.get('actor_provenance')
    known = reviewer.get('known_author_ids')
    require(actor == {'actor_id':ACTOR,'session_id':ACTOR} and reviewer.get('auditor') == 'GPT' and
            isinstance(reviewer.get('auditor_instance'),str) and reviewer['auditor_instance'].strip() and
            isinstance(reviewer.get('controller_independence_basis'),str) and reviewer['controller_independence_basis'].strip() and
            isinstance(known,list) and len(known) == len(set(known)) and
            all(isinstance(x,str) and x.strip() for x in known),
            'Root-bound actual fresh actor/session and known-author review required')
    excluded = {'/root',*(parent[1] for parent in PARENTS.values()),*known,*previous_instances}
    for question in questions.values(): excluded.update(principals(question))
    require(not {actor['actor_id'],actor['session_id'],reviewer['auditor_instance']} & excluded and job.get('worker') == ACTOR,
            'Old actor or known author cannot supply a supplementary independent review')
    return reviewer


def load_metadata(root,primary_records,questions,collections):
    """Validate committed fixed-scope evidence; never mutate primary rows or queues.

    `questions` contains actual source objects; `collections` maps IDs to their
    repository collection paths. This avoids using a stale generated ledger.
    Original worker Git validation remains the controller's integration duty.
    """
    result = {'assessments':{},'records':[],'primary_limitations':{},'excluded_primary_key_ids':[],
              'progress':counts(primary_records,[])}
    if not (root/STATE).exists(): return result
    read = committed_reader(root)
    state = json.loads(read(STATE)); queue.state_stage(state,'independent-legacy')
    scope = state.get('phase11_context38_scope',{})
    require(scope.get('schema_version') == 1 and scope.get('purpose') == PURPOSE and
            scope.get('question_ids') == list(IDS) and set(scope.get('previous_evidence',{})) == set(IDS) and
            scope.get('root_actor') == '/root' and type(scope.get('automatic_release_credit')) is int and
            scope['automatic_release_credit'] == 0, 'Fixed context38 retry scope changed')
    disclosure, disclosure_binding = validate_disclosure(read,scope)
    jobs = state['jobs']
    require(len(jobs) == 1 and jobs[0].get('job_id') == JOB_ID and jobs[0].get('sequence') == 1 and
            set(jobs[0]['question_hashes']) == set(IDS) and
            jobs[0]['status'] in {'QUEUED','LEASED','SUBMITTED','INTEGRATED'},
            'Procedural retry queue expanded or changed its exact assignment')
    job = jobs[0]; primary = {r['question_id']:r for r in primary_records}; previous_instances = set()
    for qid in IDS:
        binding = scope['previous_evidence'][qid]; name,old_actor,_ = PARENTS[qid]
        require(binding.get('report_path') == PREFIX+name and binding.get('original_actor') == old_actor and
                binding.get('reason') == 'ROOT_ATTESTED_AGGREGATE_PRIOR_CONCLUSION_EXPOSURE_NOT_FRESH',
                'Wrong procedural parent provenance')
        report = json.loads(read(binding['report_path'],binding['report_sha256']))
        no_release(report)
        require(report.get('stage') == 'independent-legacy' and report.get('independent_of_authors') is True,
                'Original procedural parent is not independent legacy evidence')
        previous_instances.add(report['auditor_instance'])
        rows = [r for r in report['records'] if r['question_id'] == qid]
        require(len(rows) == 1 and queue.digest(rows[0]) == binding['record_sha256'] and
                report['actor_provenance'] == {'actor_id':old_actor,'session_id':old_actor} and
                primary.get(qid) == rows[0], 'Procedural parent row/actor differs from immutable primary history')
        row = rows[0]; legal = row['legal_review']
        require(legal['existing_answer_correct'] == 'YES' and legal['verdict'] == 'KEEP' and
                row.get('release_eligible') is False,
                'Only the disclosed 38 context-conditioned KEEP/YES primary rows are in scope')
        require(binding['report_sha256'] == disclosure['parent_report']['raw_sha256'],
                'Context-conditioned parent differs from actual exposure disclosure')
        result['primary_limitations'][qid] = dict(
            context_conditioned=True, independent_fresh_key_credit=0,
            original_primary_findings_preserved=True, primary_report_path=binding['report_path'],
            primary_report_sha256=binding['report_sha256'],primary_record_sha256=binding['record_sha256'],
            exposure_disclosure=copy.deepcopy(disclosure_binding),
            limitation='Full-history checkpoint aggregate permitted prior positive conclusions to be inferred; requires actual fresh fork-none supplementary review.')
        expected = binding['question_record_sha256']
        require(row['record_sha256'] == expected == job['question_hashes'][qid] == queue.digest(questions[qid]),
                'Procedural retry current question hash changed: '+qid)
        bank = json.loads(read(collections[qid]))
        current = [q for q in bank['questions'] if q['question_id'] == qid]
        require(current == [questions[qid]], 'Question source is not the current committed object: '+qid)
    result['excluded_primary_key_ids'] = list(IDS)
    result['progress'] = combine_metadata(primary_records,result)['progress']
    # A live lease carries no new credit. Validate captured identity when present;
    # old checkpoints need the new header before any integrated result is consumed.
    if scope.get('fresh_reviewer') is not None: validate_reviewer(scope,job,{qid:questions[qid] for qid in IDS},previous_instances)
    if job['status'] != 'INTEGRATED': return result
    reviewer = validate_reviewer(scope,job,{qid:questions[qid] for qid in IDS},previous_instances)
    require(type(job.get('attempt')) is int and job['attempt'] >= 1 and
            job.get('worker_branch') == 'mission/'+job['job_id']+'-attempt-'+str(job['attempt']) and
            re.fullmatch('[0-9a-f]{40}',job.get('integrated_commit','')) and job.get('integrated_at'),
            'Missing captured supplementary worker/integration provenance')
    manifest = job['result']; queue.validate_result(job,manifest); no_release(manifest,required=False)
    expected_provenance = {k:reviewer[k] for k in ('auditor','auditor_instance')}
    actual_actor = manifest.get('actor_provenance',{})
    require({k:actual_actor.get(k) for k in ('actor_id','session_id')} == reviewer['actor_provenance'] and
            all(manifest.get(k) == v for k,v in expected_provenance.items()) and
            re.fullmatch('[0-9a-f]{40}',manifest['worker_commit']), 'Supplementary submitted actor/session or worker commit differs')
    envelope = scope.get('result_envelope',{})
    require(isinstance(envelope.get('path'),str) and envelope['path'].startswith(PREFIX) and
            isinstance(envelope.get('raw_sha256'),str), 'Captured supplementary result envelope raw binding required')
    require(json.loads(read(envelope['path'],envelope['raw_sha256'])) == manifest,
            'Captured supplementary result envelope differs from submitted result')
    require(len({(r['evidence_path'],r['evidence_sha256']) for r in manifest['results']}) == 1,
            'Fixed context38 retry requires one exact38-record report')
    events = state['events']
    require(any(e.get('kind') == 'CLAIM' and e.get('job_id') == job['job_id'] and e.get('worker') == ACTOR and
                e.get('attempt') == job['attempt'] for e in events) and
            any(e.get('kind') == 'SUBMIT' and e.get('job_id') == job['job_id'] and
                e.get('result_sha256') == queue.digest(manifest) for e in events) and
            any(e.get('kind') == 'INTEGRATE' and e.get('job_id') == job['job_id'] and
                e.get('commit') == job['integrated_commit'] for e in events),
            'Supplementary claim/submission/integration event binding changed')
    reports = {}; assessed = []
    for row in manifest['results']:
        path = row['evidence_path']
        require(path.startswith(PREFIX), 'Supplementary report must remain in review evidence scope')
        raw = read(path,row['evidence_sha256'])
        if path not in reports:
            report = json.loads(raw); no_release(report)
            native = report.get('native_assignment_binding',{})
            require(all(native.get(key) == job[key] for key in
                        ('job_id','sequence','question_hashes','stage','worker','worker_branch','attempt')) and
                    ('job_id' not in report or report['job_id'] == job['job_id']),
                    'Supplementary report native assignment binding changed')
            require(report.get('stage') == 'independent-legacy' and
                    report.get('question_hashes') == job['question_hashes'] and
                    len(report['records']) == len(IDS) and {r['question_id'] for r in report['records']} == set(IDS),
                    'Supplementary report must contain exactly the fixed38 current questions')
            for relative,expected in set(evidence_bindings(report)): read(relative,expected)
            reports[path] = report
        report = reports[path]; queue.validate_independent_evidence(job,row,report)
        record = next(r for r in report['records'] if r['question_id'] == row['question_id'])
        legal = record['legal_review']; realism = record['realism_review']
        require(legal.get('existing_answer_correct') in {'YES','NO','AMBIGUOUS','NOT_ASSESSED'} and
                legal.get('verdict') in {'KEEP','MINOR_EDIT','MAJOR_REWRITE','HOLD','DELETE'} and
                realism.get('verdict') in {'PASS','FAIL','NOT_ASSESSED'} and
                record.get('release_eligible') is False, 'Unknown assessment or forbidden supplementary release claim')
        no_release(record,required=False)
        read_scope = record.get('read_scope',{})
        require(isinstance(read_scope,dict) and bool(read_scope), 'Supplementary original read scope required')
        exposed = any(read_scope.get(k) is True for k in ('accidental_hidden_truth_exposure',
            'prior_author_or_independent_conclusions_read','prior_question_author_or_independent_verdicts_read',
            'hidden_statement_truth_read','hidden_truth_used_as_evidence'))
        exposed = exposed or any(isinstance(read_scope.get(k),str) and 'ACCIDENTAL' in read_scope[k].upper()
            for k in ('hidden_truth','prior_assigned_author_or_independent_conclusions'))
        require(not exposed or legal['existing_answer_correct'] == 'NOT_ASSESSED',
                'An exposed or unread supplementary record cannot gain assessed-key credit')
        if legal['existing_answer_correct'] != 'NOT_ASSESSED':
            options = [c['id'] for c in questions[record['question_id']]['choices']]
            require(all(read_scope.get(k) is True for k in ('original_stem','stored_key_read',
                        'complete_core_reasoning_read','learning_boundary_read')) and
                    read_scope.get('all_choices_read') == options and read_scope.get('all_choice_explanations_read') == options,
                    'Assessed supplementary key requires the complete original visible read scope')
        authorities = legal.get('authorities',[])
        require(isinstance(authorities,list) and
                (legal['existing_answer_correct'] == 'NOT_ASSESSED' or bool(authorities)),
                'An assessed supplementary key needs bound official authority')
        for authority in authorities:
            url = urlsplit(authority.get('official_url',''))
            require(url.scheme == 'https' and bool(url.hostname) and
                    all(isinstance(authority.get(k),str) and authority[k].strip() for k in
                        ('exact_section','law_checked_date','version_and_commencement_basis',
                         'evidence_path','evidence_sha256','raw_evidence_path','raw_sha256')),
                    'Incomplete supplementary official authority binding')
            read(authority['evidence_path'],authority['evidence_sha256'])
            read(authority['raw_evidence_path'],authority['raw_sha256'])
        qid = record['question_id']; assessed.append(record)
        result['assessments'][qid] = dict(record=copy.deepcopy(record),previous_evidence=copy.deepcopy(scope['previous_evidence'][qid]),
            report_path=path,report_sha256=row['evidence_sha256'],worker_commit=manifest['worker_commit'],
            submitted_result_sha256=queue.digest(manifest),result_path=envelope['path'],
            result_raw_sha256=envelope['raw_sha256'],actor_provenance=copy.deepcopy(reviewer['actor_provenance']),
            auditor=reviewer['auditor'],auditor_instance=reviewer['auditor_instance'],
            independence_basis='ROOT_ATTESTED_ACTUAL_FRESH_SESSION_NOT_IDENTITY_PROOF',
            controller_independence_basis=reviewer['controller_independence_basis'],
            supplementary_only=True,does_not_override_primary=True,canonical_release_credit=0)
    result['records'] = copy.deepcopy(assessed)
    result['progress'] = combine_metadata(primary_records,result)['progress']
    return result
