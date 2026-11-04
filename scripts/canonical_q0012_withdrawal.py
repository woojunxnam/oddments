"""Exact safety withdrawal of MA-Q-0012; no content edit or audit credit.

This decoder is independent of note publication guards and live review queues.
Its retained cause package records an actual local explanation mismatch, not a
fresh whole-question audit or cryptographic proof of reviewer identity.
"""
import copy
import hashlib
import json
from pathlib import Path, PurePosixPath

from qa_common import QUESTION_AUDIT_FIELDS, question_audit_hash

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'reports/full-corpus-review/canonical-q0012-withdrawal/'
MANIFEST = PREFIX + 'protected-migration.json'
MANIFEST_SHA = '29510b19ca7b4bd89fd4d1f7b8574d76144c45070c0d06a58b43b9b679881563'
PREVIOUS_MANIFEST_SHA = '27eb1bd5a867a450bacab76f494d6da83d5ae7e37386b5207fe6ae7b31682b6d'
BASELINE = 'reports/representative-rewrite/protected-baseline.json'
BASELINE_SHA = 'a4f25cd55d3377b088bcb27c63a75a9c4f52b88c4197900cf43bf8456d5c0f57'
QUESTION = 'data/questions/ma-q-0012.json'
FAMILY = 'data/exam_style/question_family_matrix.json'
PREVIEW = 'site/generated/preview_allowlist.json'
GUIDE = 'data/study_guide/sections/sg-cii-lifecycle.json'
GUIDE_ID = 'SG-CII-LIFECYCLE'
GUIDE_HASH = '0a89087ba5869e6692864fd5496f11f80801e7c927584cdcca093e90a83b5a4a'
PATHS = (QUESTION, FAMILY, GUIDE)
CURRENT_COVERAGE = PREFIX + 'current-study-guide-coverage.json'
HISTORICAL_COVERAGE = 'audits/coverage/2026-09-01/BATCH4-STUDY-GUIDE-COVERAGE.json'
HISTORICAL_COVERAGE_SHA = '8fcac3472225879bb0f133612eda35bad6370bcd784ca2822e3d87288969c47e'
QID = 'MA-Q-0012'
FAMILY_ID = 'P2_0012_MA_CII_VALIDITY_30D'
AUDIT_HASH = '218f8940f7ffbc3671f6a49499105caa44ed9a2fe4ec4b84c3289b2253b3f81d'
AUDIT_FIELDS = ('question_id','family_id','area','topic','subtopic','difficulty',
                'question_type','provenance','source_signal_ids','stem','choices',
                'correct_choice_ids','explanation','rule_ids','drug_ids','reasoning_steps')
ACTOR = {'actor_id':'/root/independent_case_e','session_id':'/root/independent_case_e'}
INSTANCE = 'gpt-independent-session-root-independent_case_e-20261103'
JOB_ID = 'review-independent-notes-9ef0ae660e8bc055'
JOB_SHA = '8d05f5df2bb10666e38ec8af32aa4e858c1cfd66cb8490eed399666b46fb0eb0'
ALIGNMENT_ROW_SHA = '4eb050332662eb36827e31f52744541f2e33e2f80a061cdc57ab46ce10304c76'
CAUSE_HASHES = {
    'report':'d098b2b49d851fe53fca3e1c70941d6aa5c54fb726e14c766f75b9fa18a071dc',
    'alignment':'b66b605e07708734b77d1fdb353ff5922b24676d07d17c057f488777adfdb155',
    'result':'fb081fa57e9817eb95466e981a9e34e773773d962d7a9b65090bd897ac6cf7d7',
    'visible_packet':'d537ef43c3104096375dca4fa92e92c964f3566f65967fcc643f7e9880672f14',
}
ORIGINAL_REPORT = 'reports/full-corpus-review/independent-notes/fourth-e-review.json'
ORIGINAL_ALIGNMENT = 'reports/full-corpus-review/independent-notes/fourth-e-evidence/related-question-alignment.json'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def digest(value):
    return sha(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())


def read(root, relative, expected=None):
    pure = PurePosixPath(relative)
    require(not pure.is_absolute() and '..' not in pure.parts and str(pure) == relative,
            'Unsafe canonical withdrawal input path')
    path = root / relative
    require(root.resolve() in path.resolve().parents and path.is_file() and not path.is_symlink(),
            'Missing or unsafe canonical withdrawal input: ' + relative)
    raw = path.read_bytes()
    require(expected is None or sha(raw) == expected,
            'Canonical withdrawal raw SHA changed: ' + relative)
    return raw


def no_credit(value):
    require(value.get('canonical_audit') is False and all(
        type(value.get(k)) is int and value[k] == 0 for k in
        ('canonical_release_credit','question_audit_credit','author_review_credit')),
        'Canonical withdrawal cannot create audit or release credit')


def validate_question(before, after):
    require(tuple(QUESTION_AUDIT_FIELDS) == AUDIT_FIELDS,
            'Canonical withdrawal audit field contract changed')
    require(before.get('question_id') == after.get('question_id') == QID and
            before.get('family_id') == after.get('family_id') == FAMILY_ID and
            before.get('verification_status') == before.get('lifecycle_status') == 'RELEASED',
            'Wrong canonical withdrawal preimage/question/family')
    require(after.get('verification_status') == 'HOLD' and
            after.get('lifecycle_status') == 'REVIEW_REQUIRED',
            'Known Q0012 defect must remain HOLD/REVIEW_REQUIRED; unchanged hash cannot be re-released')
    expected = copy.deepcopy(before)
    expected.update(verification_status='HOLD',lifecycle_status='REVIEW_REQUIRED')
    require(digest(after) == digest(expected), 'Canonical withdrawal changed content, key, audits, history, or other fields')
    require(question_audit_hash(before) == question_audit_hash(after) == AUDIT_HASH and
            before['correct_choice_ids'] == after['correct_choice_ids'] == ['B'] and
            after.get('independent_audit_status') == 'PASSED' and after.get('audits') and
            after.get('final_adjudication') == before.get('final_adjudication'),
            'Canonical withdrawal changed original audit hash/key/PASSED history')


def validate_family(before, after):
    expected = copy.deepcopy(before)
    found = [r for r in expected['families'] if r['family_id'] == FAMILY_ID]
    require(len(found) == 1 and type(found[0]['current_released_count']) is int and
            found[0]['current_released_count'] == 1, 'Wrong canonical withdrawal family preimage')
    found[0]['current_released_count'] = 0
    require(digest(after) == digest(expected) and
            sum(r['current_released_count'] for r in before['families']) == 398 and
            sum(r['current_released_count'] for r in after['families']) == 397,
            'Canonical withdrawal may only decrement the exact family released count by one')


def validate_preview(before, after, config):
    require(len(before['question_ids']) == len(set(before['question_ids'])) == 398 and
            before['question_ids'].count(QID) == 1 and 'MA-Q-0028' not in before['question_ids'],
            'Wrong canonical withdrawal preview preimage')
    expected = copy.deepcopy(before)
    expected['question_ids'] = [qid for qid in before['question_ids'] if qid != QID]
    expected['generated_date'] = config['withdrawal_date']
    expected['notice'] = config['preview_notice']
    require(digest(after) == digest(expected) and len(after['question_ids']) == 397 and
            QID not in after['question_ids'] and 'MA-Q-0028' not in after['question_ids'],
            'Canonical withdrawal preview may remove Q0012 only; no restored or added release')


def validate_guide(before,after):
    from study_guide_common import study_guide_content_hash
    require(before.get('section_id') == after.get('section_id') == GUIDE_ID and
            before.get('verification_status') == 'VERIFIED' and
            after.get('verification_status') == 'REVIEW_REQUIRED',
            'Linked guide must remain REVIEW_REQUIRED; old VERIFIED status cannot be restored')
    expected=copy.deepcopy(before);expected['verification_status']='REVIEW_REQUIRED'
    require(digest(after) == digest(expected) and
            before.get('content_version') == after.get('content_version') == 6 and
            before.get('content_hash') == after.get('content_hash') == study_guide_content_hash(after) == GUIDE_HASH and
            len(after['practice_question_ids']) == 8 and QID in after['practice_question_ids'],
            'Linked guide withdrawal changed prose, references, content hash/version, or historical audit')


def validate(root=ROOT):
    """Verify the fixed cause package and the one exact withdrawal transition."""
    root = Path(root)
    spec = json.loads(read(root,MANIFEST,MANIFEST_SHA))
    no_credit(spec)
    previous=spec['previous_manifest']
    require(previous['raw_sha256'] == PREVIOUS_MANIFEST_SHA,
            'Linked guide cannot replace original Q0012 withdrawal manifest')
    old=json.loads(read(root,previous['path'],PREVIOUS_MANIFEST_SHA))
    require(all(digest(spec[k]) == digest(v) for k,v in old.items() if k not in {'protected_paths','changes'}) and
            all(spec['changes'][p] == b for p,b in old['changes'].items()) and
            old['protected_paths'] == [QUESTION,FAMILY],
            'Linked guide changed original question/family/preview/cause bindings')
    require(spec['schema_version'] == 'canonical-q0012-safety-withdrawal/1' and
            spec['question_id'] == QID and spec['family_id'] == FAMILY_ID and
            tuple(spec['protected_paths']) == PATHS and
            spec['same_hash_release_restoration_allowed'] is False,
            'Canonical withdrawal manifest expands scope or restores unsafe release')
    require(set(spec['changes']) == {*PATHS,PREVIEW}, 'Canonical withdrawal change set expanded')
    baseline = json.loads(read(root,BASELINE,BASELINE_SHA))
    require(baseline['counts']['files'] == len(baseline['files']) == 1781,
            'Canonical withdrawal cannot replace or expand the 1781-file baseline')
    originals = {r['path']:r for r in baseline['files']}
    preimages = {}; current = {}
    for path in (*PATHS,PREVIEW):
        binding = spec['changes'][path]
        raw = read(root,binding['preimage_path'],binding['before_raw_sha256'])
        if path in PATHS:
            row = originals[path]
            require(sha(raw) == row['sha256'] and len(raw) == row['bytes'] and
                    hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == row['git_blob_sha1'],
                    'Canonical withdrawal preimage differs from actual protected main blob')
        preimages[path] = raw; current[path] = read(root,path)
    config = json.loads(read(root,spec['config']['path'],spec['config']['raw_sha256']))
    no_credit(config)
    require(config['question_ids'] == [QID] and config['expected_hashes'] == {QID:AUDIT_HASH},
            'Canonical withdrawal configuration changed target/audit hash')
    before_q = json.loads(preimages[QUESTION]); after_q = json.loads(current[QUESTION])
    validate_question(before_q,after_q)
    validate_family(json.loads(preimages[FAMILY]),json.loads(current[FAMILY]))
    validate_preview(json.loads(preimages[PREVIEW]),json.loads(current[PREVIEW]),config)
    validate_guide(json.loads(preimages[GUIDE]),json.loads(current[GUIDE]))
    for path,raw in current.items():
        require(sha(raw) == spec['changes'][path]['after_raw_sha256'],
                'Canonical withdrawal current bytes differ from exact authorized transition: '+path)
    canonical_rows = {p:r for p,r in originals.items() if p.startswith('data/questions/') and p.endswith('.json')}
    directory_rows = {p:r for p,r in originals.items() if p.startswith('data/questions/')}
    actual_paths = {p.relative_to(root).as_posix() for p in (root/'data/questions').rglob('*') if p.is_file() or p.is_symlink()}
    require(len(canonical_rows) == 439 and actual_paths == set(directory_rows),
            'Canonical withdrawal cannot add or remove canonical question files')
    for path,row in directory_rows.items():
        if path not in canonical_rows:
            read(root,path,row['sha256'])
    questions = {}
    for path,row in canonical_rows.items():
        raw = current[QUESTION] if path == QUESTION else read(root,path,row['sha256'])
        q = json.loads(raw); questions[q['question_id']] = q
    require(len(questions) == 439 and
            sum(q.get('verification_status') == q.get('lifecycle_status') == 'RELEASED'
                for q in questions.values()) == 397 and
            questions['MA-Q-0028']['verification_status'] != 'RELEASED',
            'Canonical withdrawal released set or Q0028 quarantine changed')
    validate_cause(root,spec,before_q)
    validate_report(root,spec,before_q,after_q)
    binding=spec['linked_guide_withdrawal_report']
    linked=json.loads(read(root,binding['path'],binding['raw_sha256']));no_credit(linked)
    require(linked.get('report_type') == 'LINKED_GUIDE_SAFETY_WITHDRAWAL_NOT_NEW_AUDIT' and
            linked.get('section_id') == GUIDE_ID and linked.get('section_content_hash') == GUIDE_HASH and
            linked.get('status_after') == 'REVIEW_REQUIRED' and linked.get('question_id') == QID and
            linked.get('question_audit_hash') == AUDIT_HASH and
            linked.get('same_hash_verified_restoration_allowed') is False and
            linked.get('all_prose_refs_hash_and_audit_fields_preserved') is True and
            type(linked.get('guide_audit_credit')) is int and linked['guide_audit_credit'] == 0 and
            linked.get('before_raw_sha256') == sha(preimages[GUIDE]) and
            linked.get('after_raw_sha256') == sha(current[GUIDE]),
            'Linked guide withdrawal report differs from exact private source pair')
    require(spec['coverage'] == {'historical_path':HISTORICAL_COVERAGE,
            'historical_raw_sha256':HISTORICAL_COVERAGE_SHA,'current_path':CURRENT_COVERAGE},
            'Linked guide coverage scope changed')
    read(root,HISTORICAL_COVERAGE,HISTORICAL_COVERAGE_SHA)
    return preimages


def preserved_withheld_reference(root,section,question):
    """Only this exact private section/question pair may retain its old mapping."""
    root=Path(root)
    require(section.get('section_id') == GUIDE_ID and question.get('question_id') == QID,
            'Preserved private guide reference cannot expand to another section or question')
    validate(root)
    require(digest(section) == digest(json.loads(read(root,GUIDE))) and
            digest(question) == digest(json.loads(read(root,QUESTION))),
            'Preserved private guide reference differs from actual guarded canonical sources')
    return True


def current_coverage_path(root):
    """Keep the protected historical report immutable; never fall back on failure."""
    validate(root)
    return Path(root)/CURRENT_COVERAGE


def coverage_snapshot(coverage,questions,guide):
    public=guide['sections'];public_ids={s['section_id'] for s in public}
    public_rules={rid for s in public for rid in s['rule_ids']}
    require(len(questions['questions']) == 397 and
            QID not in {q['question_id'] for q in questions['questions']} and
            GUIDE_ID not in public_ids and QID not in guide['question_to_sections'] and
            GUIDE_ID not in {sid for ids in guide['question_to_sections'].values() for sid in ids} and
            coverage['sections']['by_status']['VERIFIED'] == len(public) == guide['meta']['public_verified_section_count'] and
            coverage['canonical_rules']['covered_by_verified_public_section'] == len(public_rules),
            'Current linked-guide coverage differs from actual public release payloads')
    result=copy.deepcopy(coverage)
    result['safety_withdrawal']={
        'question_id':QID,'withheld_section_id':GUIDE_ID,'canonical_released_question_count':397,
        'public_verified_section_count':len(public),'public_rule_count':len(public_rules),
        'guard_manifest_raw_sha256':MANIFEST_SHA,'historical_coverage_path':HISTORICAL_COVERAGE,
        'historical_coverage_raw_sha256':HISTORICAL_COVERAGE_SHA,
        'canonical_audit':False,'canonical_release_credit':0,'question_audit_credit':0,'guide_audit_credit':0}
    return result


def validate_cause(root,spec,before_question):
    """Exact retained archive package, independent of the live note checkpoint."""
    cause = spec['cause']; loaded = {}
    keys = ('report','alignment','result','visible_packet','attestation','local_projection')
    for key in keys:
        binding = cause[key]
        require(binding['path'].startswith(PREFIX+'source/') and
                binding['raw_sha256'] == spec['source_bindings'][binding['path']],
                'Canonical withdrawal cause package path/hash changed')
        raw = read(root,binding['path'],binding['raw_sha256'])
        require(key not in CAUSE_HASHES or sha(raw) == CAUSE_HASHES[key],
                'Canonical withdrawal original E evidence replaced')
        loaded[key] = json.loads(raw)
    validate_cause_contents(loaded['attestation'],loaded['result'],loaded['report'],
                            loaded['alignment'],loaded['visible_packet'],before_question)
    row = next(r for r in loaded['alignment']['records'] if r['question_id'] == QID)
    projection = loaded['local_projection']; no_credit(projection)
    require(projection.get('source_alignment_record') == row and
            projection.get('source_alignment_record_sha256') == digest(row) == ALIGNMENT_ROW_SHA and
            projection.get('source_finding') == row['findings'][0] and
            projection.get('source_finding_sha256') == digest(row['findings'][0]) and
            projection.get('question_audit_hash') == AUDIT_HASH and
            projection.get('original_choice') == next(c for c in before_question['choices'] if c['id'] == 'D') and
            projection.get('original_choice_explanation') == before_question['explanation']['choice_analysis']['D'] and
            projection.get('original_stored_key') == ['B'] and
            projection.get('not_contained_as_defects') == ['MA-CASE-0193','MA-CASE-0196'],
            'Canonical withdrawal local cause projection changed original text/key/finding scope')
    authority_bindings = cause['authorities']
    require(len(authority_bindings) == 2 and
            {b['original_path']:b['raw_sha256'] for b in authority_bindings} ==
            {a['evidence_path']:a['evidence_sha256'] for a in row['findings'][0]['authorities']},
            'Canonical withdrawal local authority payload scope changed')
    for binding in authority_bindings:
        require(binding['path'].startswith(PREFIX+'source/') and
                binding['raw_sha256'] == spec['source_bindings'][binding['path']],
                'Canonical withdrawal authority retained path/hash changed')
        require(read(root,binding['path'],binding['raw_sha256']).startswith(b'%PDF-'),
                'Canonical withdrawal retained authority is not the actual PDF payload')
    require(set(spec['source_bindings']) == {b['path'] for b in authority_bindings} |
            {cause[k]['path'] for k in keys},
            'Canonical withdrawal cause package source scope expanded')
    binding = spec['source_manifest']
    source_manifest = json.loads(read(root,binding['path'],binding['raw_sha256'])); no_credit(source_manifest)
    require(source_manifest['retained_source_files'] == spec['source_bindings'] and
            source_manifest.get('source_job_id') == JOB_ID and source_manifest.get('source_job_status') == 'INTEGRATED' and
            source_manifest.get('source_actor_provenance') == ACTOR and
            source_manifest.get('current_main_note_queue_dependency') is False,
            'Canonical withdrawal retained source manifest grants live-queue scope or changes bindings')
    binding = spec['controller_safety_scope']
    memo = json.loads(read(root,binding['path'],binding['raw_sha256'])); no_credit(memo)
    require(memo.get('question_id') == QID and memo.get('restoration_of_unchanged_error_hash_allowed') is False and
            memo.get('withdrawal_config') == spec['config'] and memo.get('original_script_report') == spec['withdrawal_report'] and
            memo.get('main_live_note_queue_registration_or_positive_credit_added') is False and
            memo.get('new_canonical_or_legal_audit_created') is False,
            'Canonical withdrawal controller memo cannot authorize unchanged-hash restoration or positive credit')


def validate_cause_contents(snapshot,result,report,alignment,packet,before_question):
    """Check controller-captured declarations, without claiming identity proof."""
    job = snapshot['job']; events = snapshot['events']
    require(snapshot.get('source_root_commit') == 'da73e8c3505a15034c96302294f6dedaf7f0f229' and
            snapshot.get('source_checkpoint_path') == 'reports/full-corpus-review/independent-notes-work-queue.json' and
            snapshot.get('source_checkpoint_raw_sha256') == 'c9451f521f94a564a2c1b53f0d44a337c16df2e8508589e962a516d7f72dbd46',
            'Canonical withdrawal archived controller source receipt changed')
    require(digest(job) == JOB_SHA and job.get('job_id') == JOB_ID and
            job.get('sequence') == 24 and job.get('status') == 'INTEGRATED' and
            job.get('actor_provenance') == ACTOR and job.get('auditor') == 'GPT' and
            job.get('auditor_instance') == INSTANCE and
            job.get('controller_independence_basis'),
            'Canonical withdrawal source lacks exact controller-attested E job24 provenance')
    no_credit(result); no_credit(report)
    require(result == job['result'] and job['result_sha256'] == CAUSE_HASHES['result'] and
            report.get('job_id') == JOB_ID and
            result.get('stage') == report.get('stage') == 'independent-notes' and
            report.get('independent_of_authors') is True and
            result.get('actor_provenance') == report.get('actor_provenance') == ACTOR and
            result.get('auditor') == report.get('auditor') == 'GPT' and
            result.get('auditor_instance') == report.get('auditor_instance') == INSTANCE and
            result['evidence'] == {'path':ORIGINAL_REPORT,'raw_sha256':CAUSE_HASHES['report']},
            'Canonical withdrawal original source stage/envelope/actor/credit changed')
    require(len(events) == 3 and {e.get('kind') for e in events} == {'CLAIM','SUBMIT','INTEGRATE'} and
            all(e.get('job_id') == JOB_ID for e in events) and
            any(e['kind'] == 'CLAIM' and e.get('actor') == ACTOR and
                e.get('attempt') == job['attempt'] for e in events) and
            any(e['kind'] == 'SUBMIT' and e.get('result_sha256') == job['result_sha256'] and
                e.get('worker_commit') == result['worker_commit'] for e in events) and
            any(e['kind'] == 'INTEGRATE' and e.get('result_sha256') == job['result_sha256'] and
                e.get('commit') == job['integrated_commit'] for e in events),
            'Canonical withdrawal source claim/submission/integration events changed')
    require(len(report['records']) == 5 and {r['unit_id'] for r in report['records']} == set(job['unit_ids']) and
            all(r.get('binding') == job['unit_bindings'][r['unit_id']] and
                r.get('related_question_alignment_path') == ORIGINAL_ALIGNMENT and
                r.get('related_question_alignment_raw_sha256') == CAUSE_HASHES['alignment']
                for r in report['records']), 'Canonical withdrawal E report no longer binds original alignment')
    require(alignment.get('confirmed_local_explanation_mismatch_ids') == [QID] and
            type(alignment.get('question_audit_credit')) is int and alignment['question_audit_credit'] == 0 and
            alignment.get('no_new_question_audit_or_canonical_credit') is True,
            'Canonical withdrawal local finding was expanded into a question audit')
    rows = [r for r in alignment['records'] if r.get('question_id') == QID]
    require(len(rows) == 1 and digest(rows[0]) == ALIGNMENT_ROW_SHA,
            'Canonical withdrawal exact E local alignment row changed')
    row = rows[0]
    require(row.get('record_sha256') == digest(before_question) and row.get('collection') == QUESTION and
            row.get('stored_key') == before_question['correct_choice_ids'] == ['B'] and
            row.get('full_question_key_assessment') == 'NOT_PERFORMED' and
            type(row.get('question_audit_credit')) is int and row['question_audit_credit'] == 0 and
            all(row.get(k) is True for k in ('original_full_stem_read','all_options_read',
                                           'stored_key_read','entire_visible_explanation_read')) and
            len(row['findings']) == 1 and row['findings'][0].get('kind') == 'EXPLANATION_LOGIC_MISMATCH' and
            row['findings'][0].get('option_id') == 'D',
            'Canonical withdrawal finding does not match preserved original D explanation/key scope')
    visible = [r for r in packet['records'] if r.get('question_id') == QID]
    require(len(visible) == 1 and visible[0]['record_sha256'] == digest(before_question) and
            visible[0]['original_visible_content'] == {k:before_question[k] for k in
                ('question_id','question_type','stem','choices','correct_choice_ids','explanation')} and
            visible[0]['visible_content_sha256'] == row['visible_content_sha256'],
            'Canonical withdrawal original question read evidence differs from protected preimage')


def validate_report(root,spec,before_question,after_question):
    binding = spec['withdrawal_report']
    report = json.loads(read(root,binding['path'],binding['raw_sha256']))
    require(report.get('report_type') == 'GUARDED_TEMPORARY_WITHDRAWAL' and
            report.get('question_ids') == [QID] and report.get('hashes_preserved') == {QID:AUDIT_HASH} and
            report.get('status_before') == {QID:{'verification_status':'RELEASED','lifecycle_status':'RELEASED'}} and
            report.get('status_after') == {QID:{'verification_status':'HOLD','lifecycle_status':'REVIEW_REQUIRED'}} and
            report.get('released_count') == {'before':398,'after':397} and
            report.get('preview') == {'before_count':398,'after_count':397,'removed':[QID]} and
            report.get('audit_history_preserved') == {QID:before_question['audits']} and
            report.get('final_adjudication_preserved') == {QID:True} and
            report.get('family_matrix_changes') == {FAMILY_ID:{'current_candidate_count':[1,1],
                                                           'current_released_count':[1,0]}} and
            report.get('problems') == [] and isinstance(report.get('assertions'),dict) and
            all(report['assertions'].get(k) is True for k in
                ('hash_unchanged','audit_history_intact','no_unrelated_question_changed',
                 'q0028_quarantine_intact','schema_enums_only')),
            'Canonical withdrawal report assertions differ from actual bounded transition')


def decode(root,relative,current):
    require(relative in PATHS, 'Canonical withdrawal decoder expands protected scope')
    originals = validate(root)
    require(current == read(Path(root),relative), 'Canonical withdrawal decoder received different current bytes')
    return originals[relative]


if __name__ == '__main__':
    validate()
    print('Verified exact Q0012 safety withdrawal; original protected bytes and audit history preserved; no new audit/release credit.')
