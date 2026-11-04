"""Narrow HEAD-only consumer for G's native current-ID review of three candidates.

No old worker commit is resolved here. Native integration validates worker commits;
this derived consumer requires its committed queue/events and retained source bytes.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = 'reports/full-corpus-review/sata-remediation-current-id-author-sources.json'
PREFIX = 'reports/full-corpus-review/sata-remediation-current-id-author/'
BASELINE = 'reports/representative-rewrite/sata-remediation/author-review-consumer-baseline.json'
BASELINE_SHA256 = '96ae6c421a342b64ad25dd863a6bb26464cc66eddb2537498090e1944ef968ea'
QUEUE = 'reports/full-corpus-review/work-queue.json'
SCHEMA = 'sata-remediation-current-id-author-review/1'
STATUS = 'DRAFT_SOURCE_REVIEW_BOUND_NOT_CURRENT_ID_AUDIT'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def digest(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())


def read_head(root, relative):
    path = Path(relative)
    require(not path.is_absolute() and '..' not in path.parts, 'Unsafe native author source path')
    raw = (root / path).read_bytes()
    committed = subprocess.check_output(['git', '-C', str(root), 'show', 'HEAD:' + str(path)], stderr=subprocess.DEVNULL)
    require(raw == committed, 'Native author source must match committed HEAD: ' + str(path))
    return raw


def read_baseline(root):
    raw = (root / BASELINE).read_bytes()
    require(sha(raw) == BASELINE_SHA256, 'Native author consumer baseline changed')
    return json.loads(raw)


def candidate_records(root):
    from build_sata_remediation_candidates import ALLOCATION, BASE, authoring_payload
    baseline = read_baseline(root)
    allocation = json.loads((root / ALLOCATION).read_bytes())
    authored = authoring_payload(root)
    bank = json.loads((root / BASE / 'questions.json').read_bytes())
    rows = allocation['allocations']
    require(len(rows) == 3, 'Native author scope must remain exactly three candidates')
    result = {}
    for row in rows:
        qid = row['question_id']
        matches = [q for q in bank['questions'] if q['question_id'] == qid]
        a = next(a for a in authored['questions'] if a['question_id'] == qid)
        require(len(matches) == 1 and matches[0].get('archive_only_candidate') is True and
                matches[0]['remediation_candidate'] == a['remediation_candidate'], 'Unbound native author candidate')
        require(digest(matches[0]) == baseline['candidate_question_hashes'].get(qid),
                'Native candidate current-record hash changed: ' + qid)
        result[qid] = matches[0]
    require(set(result) == set(baseline['candidate_question_hashes']) and
            expected_actor(result) == baseline['required_author_provenance'], 'Native author candidate/actor baseline changed')
    return result


def expected_actor(questions):
    actors = [q['remediation_candidate']['original_author_provenance'] for q in questions.values()]
    core = {k: actors[0][k] for k in ('actor_id', 'session_id', 'stable_instance')}
    require(all(all(actor.get(k) == v for k, v in core.items()) for actor in actors), 'Ambiguous native author actor')
    return core


def validate_submission(job, result):
    return _validate_submission(job, result, count=3, prefix=PREFIX)


def _validate_submission(job, result, *, count, prefix):
    """Called by native submit only for the explicitly marked candidate author job."""
    ids = job.get('current_id_author_review_required_ids', [])
    require(re.fullmatch(r'[0-9a-f]{40}', result.get('worker_commit', '')) is not None,
            'Exact native author worker commit format required')
    require(job.get('stage', 'author') == 'author' and set(ids) == set(job['question_hashes']) and len(ids) == count,
            'Native candidate author job must contain only its exact registered IDs')
    actor = result.get('actor_provenance', {})
    require(result.get('job_id') == job['job_id'] and result.get('stage') == 'author' and
            actor.get('actor_id') == job.get('worker') == job.get('required_author_actor_id') and
            actor.get('session_id') and actor.get('stable_instance'), 'Actual claimed native author actor required')
    require(result.get('canonical_audit') is False and result.get('canonical_release_credit') == 0 and
            result.get('independent_review_credit') == 0 and result.get('independent_of_authors') is False, 'Author source cannot create independent/canonical credit')
    paths = {row.get('evidence_path') for row in result['results']}
    require(len(paths) == 1 and all(isinstance(p, str) and p.startswith(prefix) and p.endswith('.json') for p in paths),
            'Native candidate author report must use its dedicated prefix')


def validate_report(root, job, result, raw, questions):
    return _validate_report(root, job, result, raw, questions, count=3, schema=SCHEMA)


def _validate_report(root, job, result, raw, questions, *, count, schema):
    from build_full_corpus_review import validate_review
    from build_representative_rewrites import OFFICIAL_HOSTS
    report = json.loads(raw)
    actor = expected_actor(questions)
    require(report.get('schema_version') == schema and report.get('stage') == 'author' and
            report.get('job_id') == job['job_id'], 'Wrong native current-ID author report schema/job')
    require(all(report.get('actor_provenance', {}).get(k) == v for k, v in actor.items()) and
            report['actor_provenance'] == result['actor_provenance'] and job['worker'] == actor['actor_id'],
            'Native author report actor differs from actual content author/claim')
    require(report.get('canonical_audit') is False and report.get('canonical_release_credit') == 0 and
            report.get('independent_of_authors') is False and report.get('independent_review_credit') == 0,
            'Native author report must disclaim independence and release')
    records = report.get('records', [])
    require(len(records) == count and {r.get('question_id') for r in records} == set(questions), 'Native author report scope must be exactly its allocated IDs')
    for review in records:
        q = questions[review['question_id']]
        validate_review(q, review)
        require(review.get('current_ID_stem_all_choices_key_all_Korean_explanations_read') is True and
                review.get('legal_review_status') in {'AUTHOR_SOURCE_CHECKED_NOT_INDEPENDENT', 'AUTHOR_CURRENT_ID_SOURCE_BLOCKED'} and
                review.get('disposition') in {'KEEP', 'HOLD', 'SOURCE_BLOCKED', 'NEEDS_REMEDIATION'} and
                'blocker' in review, 'Incomplete formal current-ID author assessment')
        provenance = review['reviewer_provenance']
        require(provenance.get('independent') is False and
                all(provenance.get(k) == v for k, v in actor.items()), 'Unattributed native author record')
        truths = [review['choice_by_choice_findings'][c['id']].get('expected_true') for c in q['choices']]
        expected_key = None if None in truths else [c['id'] for c in q['choices'] if review['choice_by_choice_findings'][c['id']].get('expected_true') is True]
        require(review.get('author_expected_choice_ids') == expected_key,
                'Native author expected key differs from option findings')
        if review['disposition'] == 'KEEP':
            require(review['legal_review_status'] == 'AUTHOR_SOURCE_CHECKED_NOT_INDEPENDENT' and review['author_expected_choice_ids'] == q['correct_choice_ids'], 'KEEP contradicts stored current key')
        for choice in q['choices']:
            finding = review['choice_by_choice_findings'][choice['id']]
            require(finding.get('original_choice_text') == choice['text'] and
                    (type(finding.get('expected_true')) is bool or (finding.get('expected_true') is None and review['disposition'] in {'HOLD', 'SOURCE_BLOCKED'})) and
                    re.search(r'[가-힣]', finding['finding_ko']) and finding.get('authorities'),
                    'Native author requires each actual option and Korean finding')
            for authority in finding['authorities']:
                url = authority.get('official_url', '')
                require(url.startswith('https://') and (urlparse(url).hostname or '').lower() in OFFICIAL_HOSTS and
                        authority.get('exact_section') and authority.get('law_checked_date') and
                        authority.get('version_or_effective_date_status'),
                        'Native author requires exact current official primary proof')
                require(sha(read_head(root, authority['raw_path'])) == authority.get('raw_sha256'),
                        'Native author primary evidence hash changed')
                meta_raw = read_head(root, authority['retrieval_metadata_path'])
                require(sha(meta_raw) == authority.get('retrieval_metadata_sha256'), 'Native author retrieval metadata changed')
                meta = json.loads(meta_raw)
                require(meta.get('raw_sha256') == authority['raw_sha256'] and
                        meta.get('official_url') == url and meta.get('http_status') == authority.get('http_status'),
                        'Native author primary retrieval binding differs')
                if review['disposition'] == 'KEEP':
                    require(authority.get('used_as_legal_proof') is True, 'KEEP requires actual primary legal proof')
                if authority.get('body_verified_current_primary') is not True or authority.get('http_status') != 200:
                    require(review['disposition'] in {'HOLD', 'SOURCE_BLOCKED'} and review['blocker'] and
                            review['legal_review_status'] == 'AUTHOR_CURRENT_ID_SOURCE_BLOCKED' and
                            authority.get('used_as_legal_proof') is False and authority.get('failure_reason'),
                            'Failed/wrong source cannot prove a legal proposition or KEEP')
    return report


def load_sources(root=ROOT, static_review_files=None):
    """No registry means no new credit. Registered but unintegrated/stale fails."""
    root = Path(root)
    baseline = read_baseline(root)
    if static_review_files is not None:
        require(list(static_review_files) == baseline['static_review_files'], 'Original static author source set changed')
    for relative, expected in baseline['static_source_sha256'].items():
        require(sha((root / relative).read_bytes()) == expected, 'Original static author source bytes changed: ' + relative)
    state = json.loads((root / QUEUE).read_bytes())
    from review_queue import state_stage, validate_result
    require(state_stage(state) == 'author', 'Wrong native author queue stage')
    require([digest(j) for j in state['jobs'][:52]] == baseline['original_52_job_hashes'] and
            [digest(e) for e in state['events'][:len(baseline['original_event_hashes'])]] == baseline['original_event_hashes'],
            'Original 52 author jobs/events changed')
    if not (root / REGISTRY).exists():
        return {}
    read_head(root, BASELINE)
    registry = json.loads(read_head(root, REGISTRY))
    require(registry.get('schema_version') == 'sata-remediation-native-author-sources/1' and
            isinstance(registry.get('sources'), list) and len(registry['sources']) == 1,
            'Only one explicit three-candidate native author source is allowed')
    questions = candidate_records(root)
    from build_sata_remediation_candidates import BASE
    read_head(root, BASE + '/questions.json')
    read_head(root, QUEUE)
    source = registry['sources'][0]
    jobs = [j for j in state['jobs'] if j['job_id'] == source['job_id']]
    require(len(jobs) == 1, 'Unknown/duplicate native author job')
    job = jobs[0]
    require(job['sequence'] == 53 and state['jobs'][52] == job and job['status'] == 'INTEGRATED' and
            all(j['status'] == 'INTEGRATED' for j in state['jobs'][:52]), 'Native author source must be sequentially integrated after original52')
    require(job['question_hashes'] == {qid: digest(q) for qid, q in questions.items()} and
            job['job_id'] == 'review-' + digest(job['question_hashes'])[:16], 'Stale native author job current-record bindings')
    require(job.get('selection_policy') == 'CURRENT_ID_AUTHOR_REVIEW_REQUIRED', 'Unmarked native author job')
    result = job['result']
    validate_result(job, result)
    validate_submission(job, result)
    require(all(row['evidence_path'] == source['report_path'] and row['evidence_sha256'] == source['report_sha256']
                for row in result['results']), 'Native author registry differs from submitted evidence')
    require(source['report_path'].startswith(PREFIX), 'Unsafe native author report scope')
    raw = read_head(root, source['report_path'])
    require(sha(raw) == source['report_sha256'], 'Native author report raw SHA mismatch')
    events = state['events']
    plan = [i for i, e in enumerate(events) if e['kind'] == 'PLAN' and job['job_id'] in e.get('job_ids', [])]
    claims = [i for i, e in enumerate(events) if e['kind'] == 'CLAIM' and e.get('job_id') == job['job_id'] and
              e.get('worker') == job['worker'] and e.get('attempt') == job['attempt']]
    submits = [i for i, e in enumerate(events) if e['kind'] == 'SUBMIT' and e.get('job_id') == job['job_id'] and
               e.get('result_sha256') == digest(result)]
    integrations = [i for i, e in enumerate(events) if e['kind'] == 'INTEGRATE' and e.get('job_id') == job['job_id'] and
                    e.get('commit') == job.get('integrated_commit')]
    require(len(plan) == len(claims) == len(submits) == len(integrations) == 1 and
            plan[0] < claims[0] < submits[0] < integrations[0], 'Missing/invalid native author plan-claim-submit-integration chain')
    require(type(job.get('attempt')) is int and job['attempt'] >= 1, 'Invalid native author lease attempt')
    require(events[plan[0]].get('selection_policy') == 'CURRENT_ID_AUTHOR_REVIEW_REQUIRED_THEN_LEXICAL',
            'Native author PLAN policy missing')
    require(job.get('lease_token') == digest(dict(job=job['job_id'], worker=job['worker'], attempt=job['attempt'], at=events[claims[0]]['at'])) and
            job.get('worker_branch') == 'mission/' + job['job_id'] + '-attempt-' + str(job['attempt']) and
            job.get('created_at') == events[plan[0]]['at'] and job.get('submitted_at') == events[submits[0]]['at'] and
            job.get('integrated_at') == events[integrations[0]]['at'], 'Invalid native author claim/lease/provenance binding')
    from datetime import datetime
    require(datetime.fromisoformat(job['created_at']) <= datetime.fromisoformat(events[claims[0]]['at']) <=
            datetime.fromisoformat(job['submitted_at']) <= datetime.fromisoformat(job['integrated_at']) and
            datetime.fromisoformat(job['submitted_at']) <= datetime.fromisoformat(job['lease_until']),
            'Invalid native author claim/submission/lease times')
    report = validate_report(root, job, result, raw, questions)
    by_id = {r['question_id']: r for r in report['records']}
    for row in result['results']:
        expected = 'AUTHOR_REVIEWED' if by_id[row['question_id']]['disposition'] == 'KEEP' else by_id[row['question_id']]['disposition']
        require(row['disposition'] == expected, 'Native author result disposition differs from report')
    return {source['report_path'].removeprefix('reports/full-corpus-review/'): report}


def apply_review(row, question, root=ROOT):
    sources = load_sources(root)
    for relative, source in sources.items():
        matches = [r for r in source['records'] if r['question_id'] == question['question_id']]
        if not matches:
            continue
        review = matches[0]
        for key in ('disposition', 'legal_review_status', 'choice_by_choice_findings', 'reviewer_provenance', 'checked_at', 'blocker'):
            row[key] = copy.deepcopy(review[key])
        row.update(current_id_author_review_required=False, author_review_increment=1,
            checked_at_scope='FORMAL_NATIVE_CURRENT_ID_AUTHOR_REVIEW',
            native_author_review_job_id=source['job_id'],
            review_evidence=dict(source_path='reports/full-corpus-review/' + relative,
                source_sha256=sha((Path(root) / 'reports/full-corpus-review' / relative).read_bytes()),
                native_author_job_id=source['job_id'], review_record_sha256=digest(review)),
            answer_key_assessment=('NOT_ASSESSED_SOURCE_BLOCKED' if review['author_expected_choice_ids'] is None else 'FORMAL_CURRENT_ID_AUTHOR_EXPECTED_KEY_RECORDED'),
            authority_clauses=[f['exact_authority'] for f in review['choice_by_choice_findings'].values()],
            next_action='Different actual session must audit the compiled current ID independently.',
            independent_review_credit=0, canonical_release_credit=0)
