"""Exact three recovered-source legal retries; original HOLDs and all prior scopes remain unchanged."""
import copy
import json
import re
import review_queue as queue
from procedural_secondary_metadata import (committed_reader, counts, evidence_bindings,
    no_release, principals, require, retained_result, sha)
from remaining9_procedural_metadata import (moment, nonempty, validate_parent_identity,
    validate_legal as validate_base_legal)

STATE = 'reports/full-corpus-review/source3-recovered-legal-work-queue.json'
PREFIX = 'reports/full-corpus-review/'
IDS = ('MA-CASE-0785','MA-CASE-0786','MA-CASE-0790')
PURPOSE = 'EXACT_THREE_SOURCE_RECOVERY_FRESH_LEGAL_SUPPLEMENT_NO_RELEASE_OVERRIDE'
SCOPE_KEY = 'source3_recovered_legal_scope'
ENGINEER = '/root/remaining9_contract_engineering'
POLICY_URL = 'https://www.mass.gov/doc/2025-02-definitions-pdf/download'
POLICY_SOURCE_KIND = 'OFFICIAL_ADOPTED_BOARD_POLICY_NOT_CMR'
DRAFT_URL = 'https://www.mass.gov/doc/247-cmr-200-definitions-and-severability-0/download'
RECOVERY_REPORT = 'reports/full-corpus-review/remaining-source3-availability/source-only-report.json'
RECOVERY_REPORT_SHA = '9ccd05dcf2cecaa4fc7fea67fd2a52e82952de543379d071b77c91620f12f9ec'
PARENTS = {'MA-CASE-0785': {'exposure_limitations': None,
                  'legal_blocker': 'ED추가monitoring의specificserious-injury정의또는patient-received로한정한QRE정의의current공식raw를확인못했다.',
                  'original_actor': '/root/independent_case_c',
                  'original_actor_provenance': {'actor_id': '/root/independent_case_c',
                                                'session_id': '/root/independent_case_c'},
                  'original_auditor_instance': 'GPT:/root/independent_case_c:independent-legacy-20261103',
                  'original_expected_key_representation': None,
                  'original_release_eligibility': {'release_eligible': False},
                  'original_session': '/root/independent_case_c',
                  'parent_key_status': 'NOT_ASSESSED',
                  'parent_verdict': 'HOLD',
                  'question_record_sha256': '0ce3c42841324562ca6ffac94c11f6f23bd44923c291d3e5cb5c2837fce7292c',
                  'read_scope_exposure': {'hidden_statement_truth_exposed_or_used': False,
                                          'prior_author_or_independent_verdicts_read': False},
                  'record_sha256': '9853bf50bc18f0d0b33ca0474a2e45352852aceb1b48883c73f448bcb5e029c7',
                  'report_path': 'reports/full-corpus-review/independent-phase5-c-review.json',
                  'report_sha256': 'b488a042566368b096240f6cd671bccee3bc9aba51347ecda8ee3c7db6e38f68'},
 'MA-CASE-0786': {'exposure_limitations': None,
                  'legal_blocker': 'ED추가monitoring의specificserious-injury정의또는patient-received로한정한QRE정의의current공식raw를확인못했다.',
                  'original_actor': '/root/independent_case_c',
                  'original_actor_provenance': {'actor_id': '/root/independent_case_c',
                                                'session_id': '/root/independent_case_c'},
                  'original_auditor_instance': 'GPT:/root/independent_case_c:independent-legacy-20261103',
                  'original_expected_key_representation': None,
                  'original_release_eligibility': {'release_eligible': False},
                  'original_session': '/root/independent_case_c',
                  'parent_key_status': 'NOT_ASSESSED',
                  'parent_verdict': 'HOLD',
                  'question_record_sha256': '031c2100b17ac8b9209d5c3862a4dd6cbcefe432aeecd8a8557f677458224a0f',
                  'read_scope_exposure': {'hidden_statement_truth_exposed_or_used': False,
                                          'prior_author_or_independent_verdicts_read': False},
                  'record_sha256': '670a5700c8d352c775213ecc4a14900770eae5bdbededecaf08e4626fb8faf8f',
                  'report_path': 'reports/full-corpus-review/independent-phase5-c-review.json',
                  'report_sha256': 'b488a042566368b096240f6cd671bccee3bc9aba51347ecda8ee3c7db6e38f68'},
 'MA-CASE-0790': {'exposure_limitations': None,
                  'legal_blocker': 'ED추가monitoring의specificserious-injury정의또는patient-received로한정한QRE정의의current공식raw를확인못했다.',
                  'original_actor': '/root/independent_case_c',
                  'original_actor_provenance': {'actor_id': '/root/independent_case_c',
                                                'session_id': '/root/independent_case_c'},
                  'original_auditor_instance': 'GPT:/root/independent_case_c:independent-legacy-20261103',
                  'original_expected_key_representation': None,
                  'original_release_eligibility': {'release_eligible': False},
                  'original_session': '/root/independent_case_c',
                  'parent_key_status': 'NOT_ASSESSED',
                  'parent_verdict': 'HOLD',
                  'question_record_sha256': '1aeb88b4d0823bed4140b878e441926185603983999a45e6d2d6c428191227c6',
                  'read_scope_exposure': {'hidden_statement_truth_exposed_or_used': False,
                                          'prior_author_or_independent_verdicts_read': False},
                  'record_sha256': '59a2a3277d9e389a4f5f6197fbdbd50b8df3e24301612ad1fcbbf3062467cb4f',
                  'report_path': 'reports/full-corpus-review/independent-phase5-c-review.json',
                  'report_sha256': 'b488a042566368b096240f6cd671bccee3bc9aba51347ecda8ee3c7db6e38f68'}}
AUTHOR_BINDINGS = {'reports/full-corpus-review/wave6-4-author-review.json': {'known_principals': ['20261103-wave6-4'],
                                                           'raw_sha256': '8b68cf420b33d868cff4881f5d38d8415575387711a16d6bb200ef5699cf5bd9'}}
JOB_ID = 'review-independent-legacy-source3-' + queue.digest({qid:PARENTS[qid]['question_record_sha256']for qid in IDS})[:16]
REVIEW_KIND = 'SOURCE3_RECOVERED_LEGAL'
STYLE_OVERLAP_ID = 'MA-CASE-0790'

def validate_reviewer(scope, job, questions):
    reviewer = scope.get('fresh_reviewer', {})
    actor = reviewer.get('actor_provenance', {})
    known = reviewer.get('known_author_ids')
    require(isinstance(actor.get('actor_id'), str) and actor['actor_id'].strip() and
            actor == {'actor_id': actor['actor_id'], 'session_id': actor['actor_id']} and
            reviewer.get('auditor') == 'GPT' and nonempty(reviewer.get('auditor_instance')) and
            nonempty(reviewer.get('controller_independence_basis')) and
            isinstance(known, list) and len(known) == len(set(known)) and
            all(nonempty(value) for value in known),
            'Actual root-captured fresh actor/session and author-history review required')
    required_known = {person for binding in AUTHOR_BINDINGS.values() for person in binding['known_principals']}
    require(required_known <= set(known), 'Known original author history was omitted')
    excluded = {'/root', ENGINEER, *known}
    for binding in PARENTS.values():
        excluded.update((binding['original_actor'], binding['original_session'], binding['original_auditor_instance']))
    for question in questions.values():
        excluded.update(principals(question))
    require(not {actor['actor_id'], actor['session_id'], reviewer['auditor_instance']} & excluded and
            (job.get('worker') is None or job['worker'] == actor['actor_id']),
            'Old actual reviewer, root, engineer or known author cannot provide fresh legal credit')
    require(set(job.get('excluded_worker_actor_ids', [])) >= excluded,
            'Native claim must exclude all captured original principals')
    require(reviewer.get('target_question_ids') == list(IDS) and
            reviewer.get('current_target_prior_conclusions_read') is False and
            reviewer.get('current_target_author_or_editor') is False and
            type(reviewer.get('new_independent_person_credit')) is int and
            reviewer['new_independent_person_credit'] == 0,
            'Root must attest this exact target remains unseen/nonauthored; session reuse is not a new person')
    return reviewer


def validate_parent(read, qid, primary_row, question, binding):
    expected = PARENTS[qid]
    require(binding == expected, 'Exact source-missing parent metadata changed')
    report = json.loads(read(expected['report_path'], expected['report_sha256']))
    no_release(report)
    validate_parent_identity(report, expected)
    rows = [row for row in report['records'] if row['question_id'] == qid]
    require(len(rows) == 1 and queue.digest(rows[0]) == expected['record_sha256'] and
            rows[0] == primary_row, 'Immutable original primary row changed')
    row = rows[0]
    legal = row['legal_review']
    require(legal.get('existing_answer_correct') == 'NOT_ASSESSED' and legal.get('verdict') == 'HOLD' and
            legal.get('blocker') == expected['legal_blocker'] and
            legal.get('independently_expected_key') == expected['original_expected_key_representation'] and
            {k: row[k] for k in ('release_eligible',) if k in row} == expected['original_release_eligibility'] and
            row.get('exposure_limitations') == expected['exposure_limitations'] and
            {k: v for k, v in row.get('read_scope', {}).items()
             if any(s in k for s in ('hidden', 'prior', 'exposure'))} == expected['read_scope_exposure'],
            'Only the exact unchanged source-missing HOLD is eligible; substantive findings cannot be relabelled')
    require(queue.digest(question) == row['record_sha256'] == expected['question_record_sha256'],
            'Source-recovery retry current whole-record hash changed')


def validate_completed_report(job, scope, manifest, report, questions, read):
    """Pure worker/controller check, not a claim/submission/integration or new credit."""
    require(job.get('job_id') == JOB_ID and job.get('question_hashes') ==
            {uid: PARENTS[uid]['question_record_sha256'] for uid in IDS}, 'Exact actual native assignment required')
    queue.validate_result(job, manifest)
    reviewer = validate_reviewer(scope, job, questions)
    require(manifest.get('actor_provenance') == reviewer['actor_provenance'] and
            all(manifest.get(k) == reviewer[k] for k in ('auditor', 'auditor_instance')),
            'Actual fresh manifest provenance changed')
    no_release(manifest, required=False)
    no_release(report)
    require(all(type(report.get(k)) is int and report[k] == 0 for k in
                ('new_independent_people_credit', 'new_unique_original_question_credit', 'new_realism_pass_credit')),
            'Source recovery cannot invent people, unique originals or realism credit')
    prefix = PREFIX + 'source3-independent/' + JOB_ID + '/'
    require(report.get('stage') == 'independent-legacy' and report.get('purpose') == PURPOSE and
            re.fullmatch('[0-9a-f]{40}', manifest.get('worker_commit', '')) and
            report.get('question_hashes') == job['question_hashes'] and
            len(report.get('records', [])) == len(IDS) and {r['question_id'] for r in report['records']} == set(IDS) and
            all(report.get('native_assignment_binding', {}).get(k) == job[k] for k in
                ('job_id', 'sequence', 'question_hashes', 'stage', 'worker', 'worker_branch', 'attempt')),
            'Report must bind the complete actual native three-question assignment')
    started, completed = moment(report['review_started_at']), moment(report['review_completed_at'])
    require(started <= completed and report.get('reviewed_at') == completed.date().isoformat(), 'Actual review chronology/date changed')
    for relative, expected in set(evidence_bindings(report)):
        read(relative, expected)
    bound_job = dict(job, result=manifest)
    by_id = {row['question_id']: row for row in report['records']}
    for reference in manifest['results']:
        require(reference['evidence_path'] == prefix + 'report.json', 'Exact own-prefix report path required')
        queue.validate_independent_evidence(bound_job, reference, report)
        row = by_id[reference['question_id']]
        require(row.get('release_eligible') is False, 'Supplementary retry cannot release a question')
        no_release(row, required=False)
        validate_legal(row, questions[row['question_id']], read, prefix, started, completed)


def load_metadata(root, primary_records, questions, collections, *, source_bindings=None):
    result = {'assessments': {}, 'records': [], 'progress': counts(primary_records, [])}
    if not (root / STATE).exists():
        return result
    retained = {}
    read = committed_reader(root, source_bindings=retained)
    state = json.loads(read(STATE))
    queue.state_stage(state, 'independent-legacy')
    scope = state.get(SCOPE_KEY, {})
    require(scope.get('schema_version') == 1 and scope.get('purpose') == PURPOSE and
            scope.get('question_ids') == list(IDS) and scope.get('previous_evidence') == PARENTS and
            scope.get('root_actor') == '/root' and type(scope.get('automatic_release_credit')) is int and
            scope['automatic_release_credit'] == 0, 'Exact three source-recovery scope changed')
    validate_recovery_source(read, scope.get('recovered_source_reference'))
    jobs = state['jobs']
    require(len(jobs) == 1 and jobs[0].get('job_id') == JOB_ID and jobs[0].get('sequence') == 1 and
            jobs[0].get('question_hashes') == {qid: PARENTS[qid]['question_record_sha256'] for qid in IDS} and
            jobs[0].get('status') in {'QUEUED', 'LEASED', 'SUBMITTED', 'INTEGRATED'},
            'Native retry assignment must remain exactly the fixed three')
    job = jobs[0]
    primary = {row['question_id']: row for row in primary_records}
    require(len(primary) == len(primary_records), 'Duplicate primary records')
    for relative, binding in AUTHOR_BINDINGS.items():
        original_author = json.loads(read(relative, binding['raw_sha256']))
        require(sorted(principals(original_author)) == binding['known_principals'], 'Original author history changed')
    for qid in IDS:
        validate_parent(read, qid, primary.get(qid), questions[qid], scope['previous_evidence'][qid])
        bank = json.loads(read(collections[qid]))
        require([q for q in bank['questions'] if q['question_id'] == qid] == [questions[qid]],
                'Question source must be the actual committed current object')
    reviewer = validate_reviewer(scope, job, {qid: questions[qid] for qid in IDS})
    if job['status'] != 'INTEGRATED':
        return retained_result(result, retained, source_bindings)
    manifest = job['result']
    queue.validate_result(job, manifest)
    no_release(manifest, required=False)
    require(manifest.get('actor_provenance') == reviewer['actor_provenance'] and
            all(manifest.get(k) == reviewer[k] for k in ('auditor', 'auditor_instance')) and
            re.fullmatch('[0-9a-f]{40}', manifest.get('worker_commit', '')) and
            type(job.get('attempt')) is int and job['attempt'] >= 1 and
            job.get('worker_branch') == 'mission/' + JOB_ID + '-attempt-' + str(job['attempt']) and
            re.fullmatch('[0-9a-f]{40}', job.get('integrated_commit', '')) and moment(job['integrated_at']),
            'Actual captured native worker/integration provenance changed')
    envelope = scope.get('result_envelope', {})
    require(envelope.get('path') == PREFIX + 'source3-independent/' + JOB_ID + '/result.json' and
            re.fullmatch('[0-9a-f]{64}', envelope.get('raw_sha256', '')) and
            json.loads(read(envelope['path'], envelope.get('raw_sha256'))) == manifest,
            'Exact committed original submission envelope required')
    for kind, pairs in [('CLAIM', {'worker': reviewer['actor_provenance']['actor_id'], 'attempt': job['attempt']}),
                        ('SUBMIT', {'result_sha256': queue.digest(manifest)}),
                        ('INTEGRATE', {'commit': job['integrated_commit']})]:
        require(any(e.get('kind') == kind and e.get('job_id') == JOB_ID and
                    all(e.get(k) == v for k, v in pairs.items()) for e in state['events']),
                'Missing actual native ' + kind + ' event')
    prefix = PREFIX + 'source3-independent/' + JOB_ID + '/'
    require({(row['evidence_path'], row['evidence_sha256']) for row in manifest['results']} ==
            {(prefix + 'report.json', manifest['results'][0]['evidence_sha256'])}, 'One exact bounded own-prefix report required')
    report = json.loads(read(prefix + 'report.json', manifest['results'][0]['evidence_sha256']))
    validate_completed_report(job, scope, manifest, report, {uid: questions[uid] for uid in IDS}, read)
    actual_claims = [e for e in state['events'] if e.get('kind') == 'CLAIM' and e.get('job_id') == JOB_ID and
                     e.get('worker') == job['worker'] and e.get('attempt') == job['attempt']]
    require(len(actual_claims) == 1, 'Exactly one actual claim event for the current attempt required')
    claimed = moment(actual_claims[0].get('at'))
    require(claimed <= moment(report['review_started_at']), 'Review cannot precede the actual native claim')
    submits = [e for e in state['events'] if e.get('kind') == 'SUBMIT' and e.get('job_id') == JOB_ID]
    integrates = [e for e in state['events'] if e.get('kind') == 'INTEGRATE' and e.get('job_id') == JOB_ID]
    require(len(submits) == len(integrates) == 1 and submits[0].get('at') == job.get('submitted_at') and
            integrates[0].get('at') == job.get('integrated_at') and
            moment(report['review_completed_at']) <= moment(submits[0].get('at')) <= moment(integrates[0].get('at')),
            'Actual completed review, native submission and integration chronology changed')
    for record in report['records']:
        for authority in record['legal_review']['authorities']:
            metadata = json.loads(read(authority['metadata_path'], authority['metadata_sha256']))
            require(claimed <= moment(metadata['retrieved_at']) <= moment(metadata['read_at']),
                    'Fresh retry authority retrieval/read must follow the actual native claim')
    by_id = {row['question_id']: row for row in report['records']}
    for reference in manifest['results']:
        row = by_id[reference['question_id']]
        uid = row['question_id']
        result['assessments'][uid] = dict(record=copy.deepcopy(row), previous_evidence=copy.deepcopy(PARENTS[uid]),
            report_path=prefix + 'report.json', report_sha256=reference['evidence_sha256'],
            worker_commit=manifest['worker_commit'], submitted_result_sha256=queue.digest(manifest),
            result_path=envelope['path'], result_raw_sha256=envelope['raw_sha256'],
            actor_provenance=copy.deepcopy(reviewer['actor_provenance']), auditor=reviewer['auditor'],
            auditor_instance=reviewer['auditor_instance'], controller_independence_basis=reviewer['controller_independence_basis'],
            reviewed_at=report['reviewed_at'],
            independence_basis='ROOT_ATTESTED_ACTUAL_FRESH_SESSION_NOT_IDENTITY_PROOF',
            supplementary_only=True, does_not_override_primary=True, canonical_release_credit=0)
    result['records'] = copy.deepcopy(report['records'])
    result['progress'] = counts(primary_records, result['records'])
    return retained_result(result, retained, source_bindings)


def validate_recovery_source(read, binding):
    """Retain the actual source-only discovery; it supplies no legal verdict."""
    require(binding == {'path': RECOVERY_REPORT, 'raw_sha256': RECOVERY_REPORT_SHA},
            'Actual recovered-source discovery reference changed')
    report = json.loads(read(RECOVERY_REPORT, RECOVERY_REPORT_SHA))
    require(report.get('purpose') == 'SOURCE_ONLY_AVAILABILITY_CHECK_NO_LEGAL_KEY_OR_RELEASE_CREDIT' and
            report.get('source_only') is True and report.get('target_question_ids') == list(IDS) and
            report.get('new_legal_key_assessment_credit') == report.get('canonical_release_credit') == 0 and
            report.get('original_hold_or_sourceblocked_disposition_changed') is False,
            'Discovery cannot supply or override an original legal judgment')
    recovered = report['new_source']
    for key in ('policy_metadata', 'official_current_policy_list'):
        source = recovered[key]
        for pathkey, hashkey in [('metadata_path', 'metadata_sha256'), ('raw_path', 'raw_sha256'),
                                 ('text_path', 'text_sha256')]:
            read(source[pathkey], source[hashkey])
        meta = json.loads(read(source['metadata_path'], source['metadata_sha256']))
        require(meta.get('status') == 200 and meta.get('tls_verification') is True and
                all(meta.get(k) == source[k] for k in ('raw_path', 'raw_sha256', 'text_path', 'text_sha256')),
                'Recovered source-only raw/text/meta binding changed')
    policy = recovered['policy_metadata']
    listing = recovered['official_current_policy_list']
    text = read(policy['text_path'], policy['text_sha256']).decode()
    require(policy['official_url'] == POLICY_URL and 'Policy 2025-02: Definitions' in text and
            'Adopted: 8/7/25' in text and 'DRAFT' not in text,
            'Recovered document must remain the actual adopted policy, not a draft regulation')
    require(POLICY_URL in json.loads(read(listing['links_path'], listing['links_sha256'])),
            'Retained official index lost its exact policy download link')


def validate_legal(record, question, read, prefix, started, completed):
    """Reuse existing complete legal checks; classify agency policy separately."""
    validate_base_legal(record, question, read, prefix, started, completed)
    legal = record['legal_review']
    require(nonempty(legal.get('source_scope_limitation_ko')),
            'Policy/CMR distinction and application limits require an explicit Korean finding')
    for authority in legal.get('authorities', []):
        url = authority['official_url']
        require(url != DRAFT_URL, 'The explicitly proposed2024 draft is not current primary regulation')
        kind = authority.get('source_kind')
        require(kind in {POLICY_SOURCE_KIND, 'OFFICIAL_REGULATION', 'OFFICIAL_STATUTE'},
                'Every authority must identify its actual primary-source kind')
        meta = json.loads(read(authority['metadata_path'], authority['metadata_sha256']))
        require(meta.get('source_kind') == kind, 'Source-kind metadata and authority differ')
        if url == POLICY_URL:
            text = read(authority['text_path'], authority['text_sha256']).decode()
            require(kind == POLICY_SOURCE_KIND and 'Policy 2025-02: Definitions' in text and
                    'Adopted: 8/7/25' in text and 'DRAFT' not in text,
                    'Board policy must remain an actual adopted agency policy, not enacted CMR')
        if '/doc/247-cmr-' in url:
            text = read(authority['text_path'], authority['text_sha256']).decode()
            require(kind == 'OFFICIAL_REGULATION' and 'DRAFT' not in text,
                    'A proposed CMR draft cannot be labelled an operative regulation')


def merge_validated_style_source(qid, legal, style):
    """Join only the exact0790 outputs of two already-validated consumers."""
    from realism_completion_review import IDS as style_ids, PREFIX as style_prefix
    require(set(IDS) & set(style_ids) == {STYLE_OVERLAP_ID} and qid == STYLE_OVERLAP_ID and
            legal.get('review_kind') == REVIEW_KIND and style.get('review_kind') == 'REALISM_COMPLETION' and
            legal.get('source_path') == PREFIX + 'source3-independent/' + JOB_ID + '/report.json' and
            isinstance(style.get('source_path'), str) and style['source_path'].startswith(style_prefix) and
            style['source_path'].endswith('/report.json') and
            legal.get('record_sha256') == style.get('record_sha256') == PARENTS[qid]['question_record_sha256'] and
            all(re.fullmatch('[0-9a-f]{64}', item.get('source_sha256', '')) and
                type(item.get('negative')) is bool and item.get('canonical_release_credit') == 0 and
                item.get('supplementary_only') is True and item.get('does_not_override_primary') is True
                for item in (legal, style)),
            'Only the exact current0790 legal3/realism146 validated-source overlap is permitted')
    require('realism_completion_source' not in legal, 'Repeated style/legal source merge')
    # Keep each source's own negative flag. A style negative must never turn
    # the legal KEEP report into a fictitious negative, or be erased by KEEP.
    return {**copy.deepcopy(legal), 'realism_completion_source': copy.deepcopy(style)}


def negative_notice_source(qid, notice, binding):
    """Resolve a notice's exact negative path/SHA within the validated0790 pair."""
    if qid != STYLE_OVERLAP_ID or not binding or binding.get('review_kind') != REVIEW_KIND:
        return binding
    style = binding.get('realism_completion_source')
    if style is not None:
        merge_validated_style_source(qid, {k:v for k,v in binding.items() if k != 'realism_completion_source'}, style)
    matches = [source for source in (binding, style) if source is not None and
               source.get('negative') is True and
               source.get('source_path') == notice.get('review_source') and
               source.get('source_sha256') == notice.get('review_source_sha256') and
               source.get('record_sha256') == notice.get('question_record_hashes', {}).get(qid)]
    require(len(matches) <= 1, 'Repeated exact0790 negative source')
    return matches[0] if matches else None


def validate_notice_bindings(notices, sources):
    """Every actual new-law or paired-style negative keeps its exact visible history."""
    def matches(notice,qid,source):
        return ((qid in notice.get('question_ids',[]) and
                 notice.get('issue_type') == 'INDEPENDENT_REVIEW_FINDING' and
                 notice.get('review_source') == source['source_path'] and
                 notice.get('review_source_sha256') == source['source_sha256'] and
                 notice.get('question_record_hashes',{}).get(qid) == source['record_sha256'] and
                 notice.get('checked_at') == str(source['reviewed_at'])[:10]) or
                any(matches(prior,qid,source) for prior in notice.get('previous_notices',[])))
    for qid,binding in sources.items():
        if binding.get('review_kind') != REVIEW_KIND:
            continue
        require(qid in IDS, 'Recovered-law source expanded beyond its actual three IDs')
        style=binding.get('realism_completion_source')
        if style is not None:
            merge_validated_style_source(qid,{k:v for k,v in binding.items()if k!='realism_completion_source'},style)
        for source in (binding,style):
            if source is not None and source['negative']:
                require(any(matches(notice,qid,source) for notice in notices),
                        'Actual source3/legal or paired realism negative lost its source-bound archive history: '+qid)


def validate_archived_legal_sources(selection,metadata):
    require(not set(selection['recommended_ids']) & set(IDS),
            'The exact recovered-source three cannot return to default through supplementary credit')
    sources={}
    for qid,proof in metadata['assessments'].items():
        legal=proof['record']['legal_review']
        sources[qid]=dict(review_kind=REVIEW_KIND,source_path=proof['report_path'],
            source_sha256=proof['report_sha256'],record_sha256=proof['record']['record_sha256'],
            reviewed_at=proof['reviewed_at'],negative=legal['verdict']in{'MINOR_EDIT','MAJOR_REWRITE','HOLD','DELETE'}or
                legal['existing_answer_correct']in{'NO','AMBIGUOUS','NOT_ASSESSED'})
    validate_notice_bindings(selection['archive_review_notices'],sources)

