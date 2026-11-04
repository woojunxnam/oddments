"""Exact nine procedural retries; primary negatives and source history remain authoritative."""
import copy
import json
import re
from datetime import datetime
from urllib.parse import urlsplit

import review_queue as queue
from procedural_secondary_metadata import (committed_reader, counts, evidence_bindings,
    no_release, principals, require, retained_result, sha)

STATE = 'reports/full-corpus-review/remaining9-procedural-work-queue.json'
PREFIX = 'reports/full-corpus-review/'
IDS = tuple(f'MA-EXP-{i:04d}' for i in range(153,161)) + ('MA-EXP-0823',)
PURPOSE = 'EXACT_NINE_PROCEDURAL_FRESH_LEGAL_SUPPLEMENT_NO_RELEASE_OVERRIDE'
SCOPE_KEY = 'remaining9_procedural_scope'
ENGINEER = '/root/remaining9_contract_engineering'
PARENTS = {'MA-EXP-0153': {'exposure_limitations': None,
                 'legal_blocker': '같은actualB세션의과거current-hash specific key assessment이력. 새로운fresh실제세션으로재배정이필요하다.',
                 'original_actor': '/root/independent_case_b',
                 'original_auditor_instance': 'GPT-independent-legacy-root-independent_case_b-20261103',
                 'original_session': '/root/independent_case_b',
                 'parent_key_status': 'NOT_ASSESSED',
                 'parent_verdict': 'HOLD',
                 'question_record_sha256': '1d1adff74b94732bb70d6fd8ec83822f9de7cd07c6faa4b53598a488b83d0d1e',
                 'read_scope_exposure': {'hidden_statement_truth_read_or_used': False,
                                         'same_session_prior_specific_key_exposure': True},
                 'record_sha256': 'a3a0b51eee29f9463bf45213aa9de49f2a5cbfb13f12cb189d62e23f5a43b360',
                 'report_path': 'reports/full-corpus-review/independent-phase8-b-review.json',
                 'report_sha256': '0d7168bea8c2a15f1ec6d1cd0fe891a0a5b96c162dfd12c540a821dbc2247a34'},
 'MA-EXP-0154': {'exposure_limitations': None,
                 'legal_blocker': '같은actualB세션의과거current-hash specific key assessment이력. 새로운fresh실제세션으로재배정이필요하다.',
                 'original_actor': '/root/independent_case_b',
                 'original_auditor_instance': 'GPT-independent-legacy-root-independent_case_b-20261103',
                 'original_session': '/root/independent_case_b',
                 'parent_key_status': 'NOT_ASSESSED',
                 'parent_verdict': 'HOLD',
                 'question_record_sha256': '52c7f987ee396c57629122d3168564d4050f14d2b3d31871d50bfdf72b36c67f',
                 'read_scope_exposure': {'hidden_statement_truth_read_or_used': False,
                                         'same_session_prior_specific_key_exposure': True},
                 'record_sha256': 'b85a41cb5915053fab1cb1b0da3662de1ce5f8db00a4848020dcabdf3e728d21',
                 'report_path': 'reports/full-corpus-review/independent-phase8-b-review.json',
                 'report_sha256': '0d7168bea8c2a15f1ec6d1cd0fe891a0a5b96c162dfd12c540a821dbc2247a34'},
 'MA-EXP-0155': {'exposure_limitations': None,
                 'legal_blocker': '같은actualB세션의과거current-hash specific key assessment이력. 새로운fresh실제세션으로재배정이필요하다.',
                 'original_actor': '/root/independent_case_b',
                 'original_auditor_instance': 'GPT-independent-legacy-root-independent_case_b-20261103',
                 'original_session': '/root/independent_case_b',
                 'parent_key_status': 'NOT_ASSESSED',
                 'parent_verdict': 'HOLD',
                 'question_record_sha256': 'c454a5ddac2de4940943b7fc749f29f877e2340e7d5524dd1471eb201ad0b0bd',
                 'read_scope_exposure': {'hidden_statement_truth_read_or_used': False,
                                         'same_session_prior_specific_key_exposure': True},
                 'record_sha256': '0d89b6667c64d93e2d6458e97189900b0cc676eb1c88bd4265857b4518c99074',
                 'report_path': 'reports/full-corpus-review/independent-phase8-b-review.json',
                 'report_sha256': '0d7168bea8c2a15f1ec6d1cd0fe891a0a5b96c162dfd12c540a821dbc2247a34'},
 'MA-EXP-0156': {'exposure_limitations': None,
                 'legal_blocker': '같은actualB세션의과거current-hash specific key assessment이력. 새로운fresh실제세션으로재배정이필요하다.',
                 'original_actor': '/root/independent_case_b',
                 'original_auditor_instance': 'GPT-independent-legacy-root-independent_case_b-20261103',
                 'original_session': '/root/independent_case_b',
                 'parent_key_status': 'NOT_ASSESSED',
                 'parent_verdict': 'HOLD',
                 'question_record_sha256': '90863070e8b74a6b0c41e15813485b796e6f9105dab9143dbe20ce80ee9f3b81',
                 'read_scope_exposure': {'hidden_statement_truth_read_or_used': False,
                                         'same_session_prior_specific_key_exposure': True},
                 'record_sha256': '87f36f4c13c4f41ec75f7f6b3bc673b31c9d814b0239244beb2a7cf6d5596fc2',
                 'report_path': 'reports/full-corpus-review/independent-phase8-b-review.json',
                 'report_sha256': '0d7168bea8c2a15f1ec6d1cd0fe891a0a5b96c162dfd12c540a821dbc2247a34'},
 'MA-EXP-0157': {'exposure_limitations': None,
                 'legal_blocker': '같은actualB세션의과거current-hash specific key assessment이력. 새로운fresh실제세션으로재배정이필요하다.',
                 'original_actor': '/root/independent_case_b',
                 'original_auditor_instance': 'GPT-independent-legacy-root-independent_case_b-20261103',
                 'original_session': '/root/independent_case_b',
                 'parent_key_status': 'NOT_ASSESSED',
                 'parent_verdict': 'HOLD',
                 'question_record_sha256': '06c9c1868c71b45f3e834a975e10df8f9dbfe9716c48db2029f3927cb3ab0656',
                 'read_scope_exposure': {'hidden_statement_truth_read_or_used': False,
                                         'same_session_prior_specific_key_exposure': True},
                 'record_sha256': '95e07b27e7447bfe5cfd0e615d1732f909e5e19f252ee5cf0220e344eedc7ad6',
                 'report_path': 'reports/full-corpus-review/independent-phase8-b-review.json',
                 'report_sha256': '0d7168bea8c2a15f1ec6d1cd0fe891a0a5b96c162dfd12c540a821dbc2247a34'},
 'MA-EXP-0158': {'exposure_limitations': None,
                 'legal_blocker': '같은actualB세션의과거current-hash specific key assessment이력. 새로운fresh실제세션으로재배정이필요하다.',
                 'original_actor': '/root/independent_case_b',
                 'original_auditor_instance': 'GPT-independent-legacy-root-independent_case_b-20261103',
                 'original_session': '/root/independent_case_b',
                 'parent_key_status': 'NOT_ASSESSED',
                 'parent_verdict': 'HOLD',
                 'question_record_sha256': '9b6717540a777de5fa8362d64e998ef8f465e95a352f55dac938e78e1dfeeaa8',
                 'read_scope_exposure': {'hidden_statement_truth_read_or_used': False,
                                         'same_session_prior_specific_key_exposure': True},
                 'record_sha256': 'a91886c79264829ef8579be8afb242af0b56968aba3bf821c756719f55648c03',
                 'report_path': 'reports/full-corpus-review/independent-phase8-b-review.json',
                 'report_sha256': '0d7168bea8c2a15f1ec6d1cd0fe891a0a5b96c162dfd12c540a821dbc2247a34'},
 'MA-EXP-0159': {'exposure_limitations': None,
                 'legal_blocker': '같은actualB세션의과거current-hash specific key assessment이력. 새로운fresh실제세션으로재배정이필요하다.',
                 'original_actor': '/root/independent_case_b',
                 'original_auditor_instance': 'GPT-independent-legacy-root-independent_case_b-20261103',
                 'original_session': '/root/independent_case_b',
                 'parent_key_status': 'NOT_ASSESSED',
                 'parent_verdict': 'HOLD',
                 'question_record_sha256': '009e99454aaafca5e59462b0fb32d04ab9f124177a9237e66860615e10610930',
                 'read_scope_exposure': {'hidden_statement_truth_read_or_used': False,
                                         'same_session_prior_specific_key_exposure': True},
                 'record_sha256': 'b735b2d8efdaaa14b28bfb533cb48b9cc08d49e186828c554756af34f67d3420',
                 'report_path': 'reports/full-corpus-review/independent-phase8-b-review.json',
                 'report_sha256': '0d7168bea8c2a15f1ec6d1cd0fe891a0a5b96c162dfd12c540a821dbc2247a34'},
 'MA-EXP-0160': {'exposure_limitations': None,
                 'legal_blocker': '같은actualB세션의과거current-hash specific key assessment이력. 새로운fresh실제세션으로재배정이필요하다.',
                 'original_actor': '/root/independent_case_b',
                 'original_auditor_instance': 'GPT-independent-legacy-root-independent_case_b-20261103',
                 'original_session': '/root/independent_case_b',
                 'parent_key_status': 'NOT_ASSESSED',
                 'parent_verdict': 'HOLD',
                 'question_record_sha256': 'a75267ee55fa6836dad3010d389f4c3be2977f979f3704167191d23484b468df',
                 'read_scope_exposure': {'hidden_statement_truth_read_or_used': False,
                                         'same_session_prior_specific_key_exposure': True},
                 'record_sha256': 'b5456972c7120fd1cbb45dd79073d443a98295716658eff9b6522085b14be157',
                 'report_path': 'reports/full-corpus-review/independent-phase8-b-review.json',
                 'report_sha256': '0d7168bea8c2a15f1ec6d1cd0fe891a0a5b96c162dfd12c540a821dbc2247a34'},
 'MA-EXP-0823': {'exposure_limitations': None,
                 'legal_blocker': 'PROCEDURAL_INDEPENDENCE_EXPOSURE: MA-EXP-0823 _statement_truth accidentally '
                                  'displayed during source metadata inspection; not used as law authority; fresh '
                                  'whole-key credit0.',
                 'original_actor': '/root/independent_wave9_c',
                 'original_auditor_instance': 'GPT:/root/independent_wave9_c:20261104',
                 'original_session': '/root/independent_wave9_c',
                 'parent_key_status': 'NOT_ASSESSED',
                 'parent_verdict': 'HOLD',
                 'question_record_sha256': 'fae381687c20f1d0b74363545c44da7dc868b63d5e0466c66208bca32d0d2fae',
                 'read_scope_exposure': {},
                 'record_sha256': '192b6353209cda63e6df86a10a4c713014c37f56134c834a3047384f8edb96e4',
                 'report_path': 'reports/full-corpus-review/independent-phase9-c-review.json',
                 'report_sha256': 'f3d4fd169f2125f10509f521b79e25d68b5f461801bfce1027de6c879de4ac1a'}}
AUTHOR_BINDINGS = {'reports/full-corpus-review/wave12-3-author-review.json': {'known_principals': ['20261103-wave12-3'],
                                                            'raw_sha256': 'bbe273df47ec63f3fe95b4485a8d2fa1dff00bc50555f55680f637e93cd3858b'},
 'reports/full-corpus-review/wave9-4-author-review.json': {'known_principals': ['20261103-wave9-4'],
                                                           'raw_sha256': '8a5d985eeabeeb5561872035effe75707cd52c748786688cdd8c5b1843d37cdd'}}
JOB_ID = 'review-independent-legacy-remaining9-' + queue.digest({qid:PARENTS[qid]['question_record_sha256'] for qid in IDS})[:16]


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
    return reviewer


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def moment(value):
    require(nonempty(value), 'Actual source/review time string required')
    parsed = datetime.fromisoformat(value)
    require(parsed.tzinfo is not None, 'Actual timezone-aware source/review time required')
    return parsed


def validate_parent(read, qid, primary_row, question, binding):
    expected = PARENTS[qid]
    require(binding == expected, 'Exact procedural parent metadata changed')
    report = json.loads(read(expected['report_path'], expected['report_sha256']))
    no_release(report)
    require(report.get('stage') == 'independent-legacy' and report.get('independent_of_authors') is True and
            report.get('actor_provenance') == {'actor_id': expected['original_actor'],
                                                'session_id': expected['original_session']} and
            report.get('auditor_instance') == expected['original_auditor_instance'],
            'Actual original parent identity changed')
    rows = [row for row in report['records'] if row['question_id'] == qid]
    require(len(rows) == 1 and queue.digest(rows[0]) == expected['record_sha256'] and
            rows[0] == primary_row, 'Immutable original primary row changed')
    row = rows[0]
    legal = row['legal_review']
    require(legal.get('existing_answer_correct') == 'NOT_ASSESSED' and legal.get('verdict') == 'HOLD' and
            legal.get('blocker') == expected['legal_blocker'] and
            legal.get('independently_expected_key') in (None, []) and row.get('release_eligible') is False and
            row.get('exposure_limitations') == expected['exposure_limitations'] and
            {k: v for k, v in row.get('read_scope', {}).items()
             if any(s in k for s in ('hidden', 'prior', 'exposure'))} == expected['read_scope_exposure'],
            'Only the exact unchanged procedural HOLD is eligible; substantive holds cannot be relabelled')
    require(queue.digest(question) == row['record_sha256'] == expected['question_record_sha256'],
            'Procedural retry current whole-record hash changed')


def validate_legal(record, question, read, prefix, started, completed):
    """Require every visible option/rationale and linked official raw/text/meta."""
    legal = record.get('legal_review', {})
    key = legal.get('existing_answer_correct')
    verdict = legal.get('verdict')
    require(key in {'YES', 'NO', 'AMBIGUOUS', 'NOT_ASSESSED'} and
            verdict in {'KEEP', 'MINOR_EDIT', 'MAJOR_REWRITE', 'HOLD', 'DELETE'}, 'Unknown legal disposition')
    require(legal.get('stored_key') == question['correct_choice_ids'] and
            legal.get('question_type') == question['question_type'] and
            legal.get('polarity') in {'CORRECT', 'INCORRECT'} and
            legal.get('polarity_and_sata_combination_checked') is True and
            legal.get('exceptions_and_federal_state_scope_checked') is True and
            legal.get('prior_conclusions_read') is False and legal.get('hidden_truth_read') is False and
            nonempty(legal.get('finding_ko')), 'Original key/type/polarity/scope and unexposed read required')
    lead = question['stem'].rsplit('\n\n', 1)[-1]
    polarity = 'INCORRECT' if re.search(r'\b(?:incorrect|except|not|least)\b', lead, re.I) else 'CORRECT'
    require(legal['polarity'] == polarity, 'Current original lead polarity differs')
    options = {choice['id']: choice for choice in question['choices']}
    expected = legal.get('independently_expected_key')
    require(isinstance(expected, list) and len(expected) == len(set(expected)) and
            set(expected) <= set(options), 'Independent key must use actual unique options')
    require(verdict != 'KEEP' or key == 'YES', 'KEEP requires assessed correct key')
    require(key not in {'AMBIGUOUS', 'NOT_ASSESSED'} or
            (verdict == 'HOLD' and nonempty(legal.get('blocker'))), 'Incomplete key must retain explicit HOLD')
    require(key != 'YES' or expected == question['correct_choice_ids'], 'YES requires original complete stored combination')
    require(key != 'NO' or expected != question['correct_choice_ids'], 'NO requires a distinct expected combination')
    require(key != 'NOT_ASSESSED' or expected == [], 'Unassessed must not invent an expected key')
    explanation = question['explanation']
    from export_legacy_review_input import CORE_FIELDS
    require(record.get('visible_content_sha256') == queue.digest({k: question[k] for k in CORE_FIELDS}),
            'Actual complete original visible-content hash changed')
    reviewed = legal.get('original_explanation_review', {})
    require(reviewed.get('core_reasoning_sha256') == sha(explanation['core_reasoning'].encode()) and
            reviewed.get('learning_boundary_sha256') == sha(explanation['learning_boundary'].encode()) and
            reviewed.get('core_reasoning_read') is True and reviewed.get('learning_boundary_read') is True and
            nonempty(reviewed.get('finding_ko')), 'Exact full Korean core and learning boundary read required')
    analyses = reviewed.get('choice_rationales', [])
    require(len(analyses) == len(options) and {x['choice_id'] for x in analyses} == set(options) and
            all(x.get('read') is True and nonempty(x.get('finding_ko')) and
                x.get('rationale_sha256') == sha(explanation['choice_analysis'][x['choice_id']].encode())
                for x in analyses), 'Every exact original choice rationale requires an individual Korean finding')
    authorities = legal.get('authorities', [])
    require(isinstance(authorities, list) and (key == 'NOT_ASSESSED' or bool(authorities)),
            'Assessed key requires current official primary authorities')
    source_ids = set()
    for authority in authorities:
        sid = authority.get('source_id')
        require(nonempty(sid) and sid not in source_ids, 'Unique legal source identifiers required')
        source_ids.add(sid)
        url = urlsplit(authority.get('official_url', ''))
        require(url.scheme == 'https' and url.hostname and
                (url.hostname.endswith('.gov') or url.hostname == 'mass.gov') and
                nonempty(authority.get('exact_section')) and
                nonempty(authority.get('effective_date_or_version_basis')),
                'Official government primary URL, exact clause and effective-date/version limits required')
        for pathkey, hashkey in [('raw_path', 'raw_sha256'), ('text_path', 'text_sha256'),
                                 ('metadata_path', 'metadata_sha256')]:
            require(isinstance(authority.get(pathkey), str) and authority[pathkey].startswith(prefix) and
                    re.fullmatch('[0-9a-f]{64}', authority.get(hashkey, '')),
                    'Retained own-prefix official raw/text/meta SHA required')
            read(authority[pathkey], authority[hashkey])
        meta = json.loads(read(authority['metadata_path'], authority['metadata_sha256']))
        require(all(meta.get(k) == authority[k] for k in
                    ('official_url', 'raw_path', 'raw_sha256', 'text_path', 'text_sha256')) and
                meta.get('status') == 200 and nonempty(meta.get('method')) and
                meta.get('document_identity_status') == 'OFFICIAL_TARGET_PROVISIONS_DIRECTLY_READ',
                'Successful official target document metadata must bind the actual retained bytes')
        fetched, reread = moment(meta['retrieved_at']), moment(meta['read_at'])
        require(started <= fetched <= reread <= completed and
                authority.get('law_checked_date') == reread.date().isoformat(),
                'Actual retrieval/read/review chronology and read-date binding required; do not retime old cache')
    findings = legal.get('per_choice_findings', [])
    require(len(findings) == len(options) and {x['choice_id'] for x in findings} == set(options),
            'Every original option requires its own legal finding')
    for finding in findings:
        require(finding.get('option_text_sha256') == sha(options[finding['choice_id']]['text'].encode()) and
                nonempty(finding.get('finding_ko')) and
                (finding.get('proposition_supported') is None or type(finding['proposition_supported']) is bool) and
                type(finding.get('selected_by_independent_polarity')) is bool and
                isinstance(finding.get('authority_refs'), list) and
                set(finding['authority_refs']) <= source_ids and
                (key == 'NOT_ASSESSED' or bool(finding['authority_refs'])),
                'Exact original option, Korean finding, selection and official references required')
    if key in {'YES', 'NO'}:
        require(all(type(x.get('proposition_supported')) is bool for x in findings) and
                set(expected) == {x['choice_id'] for x in findings if x['selected_by_independent_polarity']} and
                bool(expected) and (question['question_type'] != 'SBA' or len(expected) == 1),
                'Complete independent polarity-adjusted selection differs from expected key')
        if question['question_type'] == 'SATA':
            require(all(type(x.get('proposition_supported')) is bool and
                        x['selected_by_independent_polarity'] == (x['proposition_supported'] is (polarity == 'CORRECT'))
                        for x in findings), 'SATA complete truth combination and negative polarity must agree')
    style = record.get('realism_review', {})
    require(style.get('verdict') == 'NOT_ASSESSED' and
            style.get('blocker') == 'BOUND_LEGAL_ONLY_RETRY_PRESERVE_PRIMARY_REALISM' and
            nonempty(style.get('finding_ko')), 'Legal-only retry cannot invent new realism credit')


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
    prefix = PREFIX + 'remaining9-independent/' + JOB_ID + '/'
    require(report.get('stage') == 'independent-legacy' and report.get('purpose') == PURPOSE and
            re.fullmatch('[0-9a-f]{40}', manifest.get('worker_commit', '')) and
            report.get('question_hashes') == job['question_hashes'] and
            len(report.get('records', [])) == len(IDS) and {r['question_id'] for r in report['records']} == set(IDS) and
            all(report.get('native_assignment_binding', {}).get(k) == job[k] for k in
                ('job_id', 'sequence', 'question_hashes', 'stage', 'worker', 'worker_branch', 'attempt')),
            'Report must bind the complete actual native nine-question assignment')
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
            scope['automatic_release_credit'] == 0, 'Exact nine procedural scope changed')
    jobs = state['jobs']
    require(len(jobs) == 1 and jobs[0].get('job_id') == JOB_ID and jobs[0].get('sequence') == 1 and
            jobs[0].get('question_hashes') == {qid: PARENTS[qid]['question_record_sha256'] for qid in IDS} and
            jobs[0].get('status') in {'QUEUED', 'LEASED', 'SUBMITTED', 'INTEGRATED'},
            'Native retry assignment must remain exactly the fixed nine')
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
    require(envelope.get('path') == PREFIX + 'remaining9-independent/' + JOB_ID + '/result.json' and
            re.fullmatch('[0-9a-f]{64}', envelope.get('raw_sha256', '')) and
            json.loads(read(envelope['path'], envelope.get('raw_sha256'))) == manifest,
            'Exact committed original submission envelope required')
    for kind, pairs in [('CLAIM', {'worker': reviewer['actor_provenance']['actor_id'], 'attempt': job['attempt']}),
                        ('SUBMIT', {'result_sha256': queue.digest(manifest)}),
                        ('INTEGRATE', {'commit': job['integrated_commit']})]:
        require(any(e.get('kind') == kind and e.get('job_id') == JOB_ID and
                    all(e.get(k) == v for k, v in pairs.items()) for e in state['events']),
                'Missing actual native ' + kind + ' event')
    prefix = PREFIX + 'remaining9-independent/' + JOB_ID + '/'
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
            independence_basis='ROOT_ATTESTED_ACTUAL_FRESH_SESSION_NOT_IDENTITY_PROOF',
            supplementary_only=True, does_not_override_primary=True, canonical_release_credit=0)
    result['records'] = copy.deepcopy(report['records'])
    result['progress'] = counts(primary_records, result['records'])
    return retained_result(result, retained, source_bindings)
