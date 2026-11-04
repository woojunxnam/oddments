"""Consume the fixed, integrated R3 local findings; grant no question audit credit.

Only current HEAD payloads are required. Worker branches/old Git objects remain
controller evidence, not a publication dependency or an identity proof.
"""
import copy
import hashlib
import json
from pathlib import PurePosixPath
import re
import subprocess

import note_review_queue as queue
from notes_independent_metadata import evidence_bindings

BACKLOG = 'reports/full-corpus-review/note-question-discrepancy-backlog.json'
REPORT = {'path': 'reports/full-corpus-review/independent-notes/reassessment-r3-review.json',
          'raw_sha256': '102c2b83c43c6b6f2a0341d9a986e7498c90c9dc90b486d11be0cd6effb230b1'}
ALIGNMENT = {'path': 'reports/full-corpus-review/independent-notes/reassessment-r3-evidence/claim-practice-alignment.json',
             'raw_sha256': 'bff59a326b5f19f668be10a0f261d503099784496b3bbf858ed590ffee93b51f'}
SELECTION = 'practice_expansion/2026-10-28-representative/selection.json'
JOB_ID = 'review-independent-notes-reassessment-f81941202344cc03'
UNIT_ID = 'w1-b-1'
ACTOR = '/root/independent_procedural_retry'
INSTANCE = 'GPT:/root/independent_procedural_retry:20261103'
ISSUE = 'NOTE_LINK_DISCREPANCY_HOLD'
SCOPE = 'LOCAL_CREDENTIAL_FACT_AND_STORED_CHOICE_EXCLUSION_ONLY'
CONTRADICTION = 'EXPLANATION_ADDS_UNLICENSED_FACT_NOT_STATED_IN_CHOICE'
LOCAL = ('LOCAL_STORED_CHOICE_EXCLUSION_AMBIGUOUS; '
         'EXPLANATION_INSERTS_UNSTATED_UNLICENSED_FACT; NOT_WHOLE_QUESTION_VERDICT')
CHOICE_TEXT = ('A trained cashier selects an unfilled prescription stock bottle '
               'and counts tablets before ringing up the sale.')
CHOICES = dict(zip(('MA-CASE-0354','MA-CASE-0355','MA-CASE-0360','MA-CASE-0400',
                   'MA-CASE-0401','MA-CASE-0402','MA-CASE-0802','MA-CASE-0810',
                   'MA-CASE-0844','MA-CASE-0845','MA-CASE-0846'),
                  ('B','B','D','A','D','A','C','C','E','C','A')))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def no_credit(value, *keys):
    require(all(type(value.get(k)) is int and value[k] == 0 for k in keys),
            'Note-link evidence cannot grant audit/release credit')


def committed_reader(root, bindings):
    cache = {}
    def read(relative, expected=None):
        require(isinstance(relative, str), 'Note-link evidence path must be a string')
        pure = PurePosixPath(relative)
        require(not pure.is_absolute() and '..' not in pure.parts and str(pure) == relative,
                'Unsafe note-link evidence path')
        path = root / relative
        require(root.resolve() in path.resolve().parents and not path.is_symlink(),
                'Note-link evidence path escapes repository')
        if relative not in cache:
            require(path.is_file(), 'Missing note-link evidence: ' + relative)
            raw = path.read_bytes()
            stored = subprocess.check_output(['git', '-C', str(root), 'show', 'HEAD:' + relative])
            require(raw == stored, 'Uncommitted note-link evidence: ' + relative)
            cache[relative] = raw
        raw = cache[relative]
        actual = hashlib.sha256(raw).hexdigest()
        require(expected is None or (isinstance(expected, str) and
                re.fullmatch('[0-9a-f]{64}', expected) and actual == expected),
                'Stale note-link evidence raw SHA: ' + relative)
        bindings[relative] = actual
        return raw
    return read


def validate_rows(backlog, alignment, questions):
    """Check exact local scope and original choice/key/text, never infer a full verdict."""
    require(backlog.get('schema_version') == 1 and backlog.get('purpose') ==
            'NOTE_ALIGNMENT_LOCAL_QUESTION_DISCREPANCY_BACKLOG_NOT_FULL_QUESTION_AUDIT' and
            backlog.get('reconciliation_by') == '/root' and backlog.get('actual_note_reviewer') == ACTOR,
            'Unexpected note-link backlog purpose/controller/reviewer')
    no_credit(backlog, 'question_audit_credit', 'canonical_release_credit', 'author_review_increment')
    no_credit(alignment, 'question_audit_credit', 'canonical_release_credit')
    require(alignment.get('unit_id') == UNIT_ID, 'Wrong note-link alignment unit')
    entries = [r for r in alignment['direct_matching_option_evidence']
               if r.get('scope_contradiction') == CONTRADICTION]
    require(len(entries) == len(CHOICES) and
            {r.get('question_id'): r.get('choice_id') for r in entries} == CHOICES,
            'Note-link local source scope expanded, missing, or duplicated')
    rows = backlog['records']
    require(len(rows) == len(CHOICES) and {r.get('question_id') for r in rows} == set(CHOICES),
            'Note-link backlog requires exactly eleven distinct source IDs')
    by_id = {r['question_id']: r for r in entries}
    for row in rows:
        qid = row['question_id']; original = questions[qid]; source = by_id[qid]
        require(row.get('disposition') == 'HOLD' and row.get('scope') == SCOPE and
                row.get('whole_question_existing_answer_correct') == 'NOT_ASSESSED' and
                row.get('current_default') is False and row.get('required_next_action_ko'),
                'Note-link backlog changed local HOLD/NOT_ASSESSED scope: ' + qid)
        require(source.get('link_type') ==
                    'DIRECT_UNFINISHED_HANDLING_SCENARIO_WITH_ACTOR_CREDENTIAL_AMBIGUITY' and
                source.get('local_legal_key_and_explanation_assessment') == LOCAL and
                source.get('whole_question_existing_answer_correct') == 'NOT_ASSESSED' and
                source.get('choice_in_stored_key') is False,
                'Note-link local ambiguity was replaced by a whole-question assessment: ' + qid)
        no_credit(source, 'full_question_audit_credit')
        require(queue.digest(source) == row.get('source_alignment_record_sha256') and
                row.get('finding_ko') == source.get('finding_ko') and source.get('finding_ko'),
                'Note-link source row/finding SHA changed: ' + qid)
        require(row.get('record_sha256') == source.get('question_record_sha256') == queue.digest(original),
                'Stale note-link current question record: ' + qid)
        choices = [c for c in original['choices'] if c['id'] == row.get('affected_choice_id')]
        require(len(choices) == 1 and row['affected_choice_id'] == source.get('choice_id') == CHOICES[qid] and
                choices[0]['text'] == source.get('choice_text') == CHOICE_TEXT and
                source.get('stored_key') == original['correct_choice_ids'] and
                row['affected_choice_id'] not in original['correct_choice_ids'],
                'Stale note-link choice text/key/exclusion: ' + qid)
    return by_id


def load_metadata(root, questions, default_ids=()):
    """Validate committed source graph; a missing/stale input fails closed.

    Fixed source hashes deliberately prevent using a changed note report to
    silently clear or expand this particular eleven-question containment.
    """
    bindings = {}; read = committed_reader(root, bindings)
    backlog = json.loads(read(BACKLOG))
    require(backlog.get('source_report') == REPORT and backlog.get('source_alignment') == ALIGNMENT,
            'Fixed note-link report/alignment binding changed')
    state = json.loads(read(queue.STATE)); queue.validate_state(state)
    found = [j for j in state['jobs'] if j['job_id'] == JOB_ID]
    require(len(found) == 1, 'Missing unique integrated note-link job')
    job = found[0]
    require(job['sequence'] == 20 and job['status'] == 'INTEGRATED' and
            job['unit_ids'] == [UNIT_ID] and set(job['unit_bindings']) == {UNIT_ID} and
            all(j['status'] == 'INTEGRATED' for j in state['jobs'] if j['sequence'] < 20),
            'Note-link source job is not sequentially integrated')
    actor = {'actor_id': ACTOR, 'session_id': ACTOR}
    excluded = set(job.get('known_author_ids', [])) | set(job['unit_bindings'][UNIT_ID]['known_author_ids'])
    require(job.get('actor_provenance') == actor and job.get('auditor') == 'GPT' and
            job.get('auditor_instance') == INSTANCE and not {ACTOR, INSTANCE} & excluded and
            isinstance(job.get('controller_independence_basis'), str) and
            bool(job['controller_independence_basis'].strip()),
            'Missing controller-attested note-link reviewer provenance')
    envelope = job['result']; queue.validate_result(job, envelope)
    require(envelope['evidence'] == REPORT, 'Wrong integrated note-link report')
    raw = read(envelope['result_path'], job['result_sha256'])
    require(json.loads(raw) == envelope, 'Note-link integrated envelope differs from checkpoint')
    require(re.fullmatch('[0-9a-f]{40}', job.get('integrated_commit', '')) and job.get('integrated_at') and
            re.fullmatch('[0-9a-f]{40}', envelope['worker_commit']) and
            any(e.get('kind') == 'CLAIM' and e.get('job_id') == JOB_ID and
                e.get('actor') == actor and e.get('attempt') == job['attempt'] for e in state['events']) and
            any(e.get('kind') == 'SUBMIT' and e.get('job_id') == JOB_ID and
                e.get('result_sha256') == job['result_sha256'] and
                e.get('worker_commit') == envelope['worker_commit'] for e in state['events']) and
            any(e.get('kind') == 'INTEGRATE' and e.get('job_id') == JOB_ID and
                e.get('commit') == job['integrated_commit'] and
                e.get('result_sha256') == job['result_sha256'] for e in state['events']),
            'Missing note-link claim/submission/integration event binding')
    report = json.loads(read(REPORT['path'], REPORT['raw_sha256']))
    require(report.get('job_id') == JOB_ID, 'Wrong note-link report job')
    sources = queue.validate_evidence(job, envelope, report)
    for path, sha in set(sources) | set(evidence_bindings(report)):
        read(path, sha)
    record = report['records'][0]
    require(record['practice_question_alignment']['path'] == ALIGNMENT['path'] and
            record['practice_question_alignment']['raw_sha256'] == ALIGNMENT['raw_sha256'],
            'Note-link alignment is not bound by its integrated report')
    alignment = json.loads(read(ALIGNMENT['path'], ALIGNMENT['raw_sha256']))
    for path, sha in set(evidence_bindings(alignment)):
        read(path, sha)
    visible = alignment['safe_visible_projection']
    projection = json.loads(read(visible['path'], visible['raw_sha256']))
    originals = projection['records']
    require(len(originals) == len({r['visible']['question_id'] for r in originals}),
            'Duplicate note-link original visible projection')
    original_by_id = {r['visible']['question_id']: r for r in originals}
    banks = {}
    for qid in CHOICES:
        require(qid in original_by_id and qid in questions, 'Missing note-linked original: ' + qid)
        original = original_by_id[qid]; collection = original['collection']
        require(collection.startswith('practice_expansion/') and collection.endswith('/questions.json'),
                'Unsafe note-link source question collection')
        if collection not in banks:
            bank = json.loads(read(collection))['questions']
            require(len(bank) == len({q['question_id'] for q in bank}), 'Duplicate current source question ID')
            banks[collection] = {q['question_id']: q for q in bank}
        require(banks[collection].get(qid) == questions[qid] and
                original['record_sha256'] == queue.digest(questions[qid]) and
                original['visible'] == {k: questions[qid][k] for k in
                    ('question_id','question_type','stem','choices','correct_choice_ids','explanation')},
                'Note-link question differs from committed original text/key/explanation: ' + qid)
    matches = validate_rows(backlog, alignment, questions)
    # Selection is a derived output of the notice builder itself. Compare
    # both HEAD defaults and the proposed/working defaults, while allowing
    # notice-only regeneration before the controller commits generated files.
    selection_path = queue.safe_path(root, SELECTION)
    selected_raw = subprocess.check_output(['git', '-C', str(root), 'show', 'HEAD:' + SELECTION])
    bindings[SELECTION] = hashlib.sha256(selected_raw).hexdigest()
    committed_selection = json.loads(selected_raw)
    working_selection = json.loads(selection_path.read_bytes())
    require(not set(CHOICES) & (set(default_ids) | set(committed_selection['recommended_ids']) |
                               set(working_selection['recommended_ids'])),
            'Note-linked local legal HOLD cannot be restored to default practice')
    records = {}
    for row in backlog['records']:
        qid = row['question_id']; source = matches[qid]; original = questions[qid]
        records[qid] = dict(
            issue_type=ISSUE, disposition='HOLD_FOR_LEGAL_REVIEW', question_id=qid,
            record_sha256=row['record_sha256'], affected_choice_id=row['affected_choice_id'],
            scope=SCOPE, scope_contradiction=CONTRADICTION,
            local_legal_key_and_explanation_assessment=LOCAL,
            whole_question_existing_answer_correct='NOT_ASSESSED',
            finding_ko=row['finding_ko'], required_next_action_ko=row['required_next_action_ko'],
            original_stem_sha256=queue.digest(original['stem']),
            original_choice_sha256=queue.digest(next(c for c in original['choices'] if c['id'] == row['affected_choice_id'])),
            original_stored_key_sha256=queue.digest(original['correct_choice_ids']),
            original_explanation_sha256=queue.digest(original['explanation']),
            source_alignment_record_sha256=queue.digest(source),
            source_report=copy.deepcopy(REPORT), source_alignment=copy.deepcopy(ALIGNMENT),
            source_backlog={'path': BACKLOG, 'raw_sha256': bindings[BACKLOG]},
            source_state={'path': queue.STATE, 'raw_sha256': bindings[queue.STATE]},
            source_result={'path': envelope['result_path'], 'raw_sha256': job['result_sha256']},
            source_job_id=JOB_ID, actor_provenance=copy.deepcopy(actor),
            auditor=job['auditor'], auditor_instance=INSTANCE,
            independence_basis='CONTROLLER_ATTESTED_DECLARATION_NOT_IDENTITY_PROOF',
            controller_independence_basis=job['controller_independence_basis'],
            checked_at=report['reviewed_at'], canonical_audit=False,
            question_audit_credit=0, canonical_release_credit=0, author_review_increment=0)
    return dict(records=records, input_bindings=bindings, summary=dict(
        runtime_status='SOURCE_BOUND_LOCAL_HOLDS_APPLIED_TO_DERIVED_LEDGER_AND_ARCHIVE_NOTICES',
        question_count=len(records), question_audit_credit=0, canonical_release_credit=0,
        author_review_increment=0, whole_question_existing_answer_correct='NOT_ASSESSED'))


def apply_holds(rows, metadata):
    """Preserve every earlier opinion/blocker; only change derived containment."""
    ids = [r['question_id'] for r in rows]
    require(len(ids) == len(set(ids)) and set(metadata['records']) <= set(ids),
            'Derived ledger lacks exact note-linked question rows')
    for row in rows:
        hold = metadata['records'].get(row['question_id'])
        if hold is None:
            continue
        if 'note_link_discrepancy_hold' in row:
            require(row['note_link_discrepancy_hold'] == hold, 'Conflicting derived note-link HOLD')
            continue
        row['before_note_link_discrepancy_hold'] = copy.deepcopy(row)
        row['note_link_discrepancy_hold'] = copy.deepcopy(hold)
        if row['disposition'] not in {'DELETE', 'REPLACE'}:
            row['disposition'] = 'HOLD_FOR_LEGAL_REVIEW'
        row['blocker'] = ' '.join(filter(None, (row.get('blocker'), hold['finding_ko'])))
        row['next_action'] = hold['required_next_action_ko']


def archive_notices(previous, metadata):
    """Dedicated format: never disguise local note findings as author reviews."""
    previous = copy.deepcopy(previous)
    ids = [qid for n in previous for qid in n['question_ids']]
    require(len(ids) == len(set(ids)), 'Repeated original archive notice ID')
    held = set(metadata['records']); result = []
    for notice in previous:
        remaining = [qid for qid in notice['question_ids'] if qid not in held]
        if remaining:
            if remaining != notice['question_ids']:
                notice = copy.deepcopy(notice)
                notice['question_ids'] = remaining
                notice['question_record_hashes'] = {qid: notice['question_record_hashes'][qid] for qid in remaining}
            result.append(notice)
    for qid, hold in metadata['records'].items():
        result.append(dict(
            question_ids=[qid], issue_type=ISSUE,
            reason=("연결 노트 검토에서 미완성 약을 선택·계수하는 cashier 보기의 자격 사실과 해설이 일치하지 않아 "
                    "해당 보기의 정답 제외를 확정하지 못했습니다. 보기에는 'trained cashier'만 있고 "
                    "해설은 무면허를 전제합니다. 전체 문항 정답은 이번 검토에서 평가하지 않았습니다 "
                    "(NOT_ASSESSED). 확정된 정답으로 암기하지 말고 부분 보류 사유를 확인하세요."),
            checked_at=hold['checked_at'], question_record_hashes={qid: hold['record_sha256']},
            review_source=REPORT['path'], review_source_sha256=REPORT['raw_sha256'],
            note_link_discrepancy_hold=copy.deepcopy(hold),
            previous_notices=[copy.deepcopy(n) for n in previous if qid in n['question_ids']]))
    ids = [qid for n in result for qid in n['question_ids']]
    require(len(ids) == len(set(ids)), 'Repeated derived archive notice ID')
    return result
