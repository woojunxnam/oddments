"""Fifteenth annotation-only wrapper over the exact merged PR190 payloads.

This is release-gate engineering, not a new legal or question review. Preparation
and verification are read-only unless the explicit writer CLI is invoked.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys

import note_review_queue as notes_queue
import review_queue as question_queue
from notes_revision import load_notes
from notes_independent_metadata import load_metadata as note_metadata
from legacy_independent_metadata import integrated_sources

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'revisions/notes/protected-migration-after190.json'
EXPORT = 'site/notes/complete-notes.md'
BUILD = 'site/notes/build.json'
PARENT = 'revisions/notes/protected-migration-independent-notes-wave3.json'
PARENT_SHA = '53537abd57b56bc8a839901a766de916c7a06b4275beba8bd2ebf435adf0353e'
CANDIDATE = '205c8feb08e463fac30c8162a124875befa0ae62'
MERGED_PR190 = 'f8ec04a028e38288aa9cbf539fa12244f2cd49a4'
MERGED_TREE = '0d0eac7ee844f6db721041d9764b26c8acd1bde1'
BASE_MD = 'revisions/baselines/complete-notes-pr190.md'
BASE_MD_SHA = 'c3bd223ff1774917388986a3b4a4e46b2f995e9d702d671309edeb92dd489d16'
BASE_BUILD = 'revisions/baselines/notes-build-pr190.json'
BASE_BUILD_SHA = 'd23f20169980cb5c94b24624776f652a233ff3e992c7e91fb940d3edfe8b419b'
SEMANTIC = 'e1519c0290ff220eb8251307e26340d76d394a7ec1f3e651194d4495a03f1824'
EDITION = '2026-11-03.emergency-kit.1'
NOTE_DELTA_JOB = 'review-independent-notes-reassessment-69894308052fd423'
NOTE_DELTA_UNIT = 'w1-b-1'
V4_CENSUS = 'reports/full-corpus-review/census-corrections/v4/census/w1-b-1-census-v4.json'
V4_RECORD = 'reports/full-corpus-review/census-corrections/v4/record/w1-b-1-census-v4-record.json'
LEGACY_STATE = 'reports/full-corpus-review/independent-legacy-work-queue.json'
# Exact already-committed definitions at e78af1cd, not future result receipts.
# make_manifest still requires actual integrated results and the one explicit
# inactive body registration before preparing any final source/export pins.
SCOPE_DEFINITION_COMMIT = 'e78af1cd5ccdd749c3599aa4f36a217af4d06552'
CENSUS_BINDINGS_SHA = 'e9fa1f3aea3cd7b7a7ce727424454572f4a28a062ba6b85b449ff2afe3b73f7b'
CENSUS_COUNT = 6989
NOTE_SCOPE_SHA = '6c630c76c38a33a8adaf32013d1666f363d6f3a3ac836565adfcf2e289a60008'
LEGACY_SCOPE_SHA = 'b223b853c533c24a60b05708d64809734c1063da914f52955632ec3edfb0fdb5'
BEFORE_DEFAULT_IDS_SHA = '6101485e9abfa7639343e44e07b9f35d37fde175708595c0976ac89545c89e02'
ALLOCATION_SHA = 'b4869303714843dc3f86d0de3984478fe94b375562fa84a8ebf8dde9e70ef938'
BODY_ORIGINAL_RECORD = 'reports/full-corpus-review/body-corrections/w3-a-3-v1/record.json'
BODY_ORIGINAL_SHA = 'cfe060fb2bb2a06769d02f712899ca7de8b24e5f3538b82a0744a125d8c5722d'
BODY_REGISTRATION_RECORD = 'reports/full-corpus-review/body-corrections/w3-a-3-v1/registrations/after-census-v2.json'
BODY_REGISTRATION_SHA = '945e120c2676793b7f6649d0eaa5a3cb4eb22b3f2e85fd56d273331a0730dd1c'
BODY_JOB_ID = 'review-independent-notes-body-4c3229fb7bfb76b6'
BODY_REGISTRATION_ID = 'body-w3-a-3-pamphlet-scope-v1-after-census-v2'
BODY_REGISTRATION_CHECKPOINT = '847d3ea688ffa2495eb628b411b44026c61a0b9b'
NATIVE_LEGACY_REPORT = 'reports/full-corpus-review/sata-remediation-current-id-independent/f-review.json'
NATIVE_LEGACY_RESULT = 'reports/full-corpus-review/sata-remediation-current-id-independent/f-result.json'
NOTE_FOLLOWUPS = {
    24: ('review-independent-notes-9ef0ae660e8bc055',
         ['w2-c-7','w2-c-8','w2-c-9','w2-c-10','w2-c-11']),
    25: ('review-independent-notes-1a27fcbc5afaebf5',
         ['w2-c-12','w2-c-13','w2-c-14','w2-c-15','w2-c-17']),
    26: ('review-independent-notes-3412f11d8110cc8f',
         ['w3-a-1','w3-a-2','w3-a-3','w3-a-4','w3-a-6']),
    27: ('review-independent-notes-771c735e22eb9a0a',
         ['w3-a-7','w3-a-8','w3-a-9','w3-a-10','point-of-sale-price']),
    28: ('review-independent-notes-reassessment-9db4b084482d44bf',['w2-c-12']),
    29: ('review-independent-notes-reassessment-ea21ac3262b9db89',['w3-a-6']),
    30: ('review-independent-notes-reassessment-a9bea3c4426a21be',['w3-a-7']),
}
PHASE7 = {
    21: 'review-independent-legacy-a3bec3528521ade0',
    22: 'review-independent-legacy-dae9a3d81d32c17b',
    23: 'review-independent-legacy-49b99543bb088e14',
    24: 'review-independent-legacy-56ad670d4fad09fa',
}
PHASE7_HASHES = {
    21: 'a3bec3528521ade0f229ff477c2059648800d23ba5494bec7e3d30448fa2202b',
    22: 'dae9a3d81d32c17b6916830f8c273f41bf8fb72d2cd7820f62cbcf643bb3c15e',
    23: '49b99543bb088e14385c3c670f3ecff5f79bf3bd7ecdf535f416454aed681297',
    24: '56ad670d4fad09fa4187ccc72bf7931f4322eeeff2a9a07c2b85d7acae9c8b65',
}
# Exact phase8 definitions; actual committed integrated receipts are now required.
WAVE8 = {
    25: ('review-independent-legacy-ff9c4b960dd7395f',
         'ff9c4b960dd7395fbd87a79a3b21e6000fe1af522ced6a9291f8670dbe693c65'),
    26: ('review-independent-legacy-fa06bb98482969e9',
         'fa06bb98482969e9ef9685e4e72f440021e50990a96ea77d6a547b0305ea4606'),
    27: ('review-independent-legacy-f1e95ede99682885',
         'f1e95ede99682885476b714756f2524450930343431b7afa9e833def2c1ae956'),
    28: ('review-independent-legacy-69f7982833d308b0',
         '69f7982833d308b0cd6c08b08407a93118bed7701224a10028950572f5f1cd87'),
}
LEGACY_REPORTS = {
    21:'reports/full-corpus-review/independent-phase7-c-review.json',
    22:'reports/full-corpus-review/independent-phase7-b-review.json',
    23:'reports/full-corpus-review/independent-phase7-g-review.json',
    24:'reports/full-corpus-review/independent-phase7-f-review.json',
    25:'reports/full-corpus-review/independent-phase8-c-review.json',
    26:'reports/full-corpus-review/independent-phase8-f-review.json',
    27:'reports/full-corpus-review/independent-phase8-g-review.json',
    28:'reports/full-corpus-review/independent-phase8-b-review.json',
}
# Root explicitly allocated these exact CURRENT DEFAULT jobs at 804178fd.
# Their pending definitions confer no evidence; all four need actual IG before
# final preparation. New jobs or different actors need another bounded review.
WAVE9 = {
    30:('review-independent-legacy-1ccd0d652abebe82','1ccd0d652abebe8220fa9bf063bb31d2cbc44f230d6e535dea51bb7af14abe5c','/root/independent_wave9_a'),
    31:('review-independent-legacy-3f7eb071e35ba44e','3f7eb071e35ba44e77f029a47dc32d3166bf2f716f5bd32be597e6cd72aaf136','/root/independent_wave9_b'),
    32:('review-independent-legacy-a159c90daad5e611','a159c90daad5e611a195f5a8a7547e86ac6789f3f2ffe66d12835c0db25f045f','/root/independent_wave9_c'),
    33:('review-independent-legacy-2afb2b3095530da6','2afb2b3095530da62bea10a0a096c5474c99549a5caad4c73f97797c75e416a3','/root/independent_wave9_d'),
}
# Output contract in INDEPENDENT_DEFAULT_WAVE9_RUNBOOK.md, not an assertion that
# these files/results exist. Raw source hashes are derived only after every IG.
WAVE9_REPORTS = {sequence:'reports/full-corpus-review/independent-phase9-'+letter+'-review.json'
                 for sequence,letter in zip(WAVE9,'abcd')}
WAVE9_RESULTS = {sequence:'reports/full-corpus-review/independent-phase9-'+letter+'-result.json'
                 for sequence,letter in zip(WAVE9,'abcd')}
# This fifteenth layer has never been published. The next exact allocation is
# captured from the real 08a417e2 checkpoint, not inferred from report filenames.
# 128 were current defaults and 32 were archive items; neither that before count
# nor a worker's future outcome is a final recommendation or audit assertion.
WAVE10_DEFINITION_COMMIT = '08a417e2e53e83501e2756792cda0168fe4ae8a7'
PRIOR_LEGACY_RECEIPTS_SHA = 'db890633bdf6af62cb7cbac313f92666d4d0d39f8e0f30ff29f8a05552c0db69'
WAVE10_PRIORITY_SOURCES_SHA = 'c55ffe1fbf0a0e59bd7a8605cadf075b7a03d6e5f483c7802c92f01a7ec245c4'
WAVE10 = {
    34:('review-independent-legacy-c20f4ee0cf56468b','c20f4ee0cf56468be09bd6192bce9baf299bc87d5376e1617fccec336b6b6b6a','/root/independent_wave10_a'),
    35:('review-independent-legacy-4bd888eabbe06366','4bd888eabbe063660aae7b675b2fa1f7570f1755136e67df48fb977666cbf5fb','/root/independent_wave10_b'),
    36:('review-independent-legacy-0c4182784eafa73d','0c4182784eafa73d0204ea09743d5eb2c28f666d8bcce69e3d4960c2e9c692d1','/root/independent_wave10_c'),
    37:('review-independent-legacy-d0710f4ed5346fe2','d0710f4ed5346fe20bd5b52585ecfbe010697b237bfe2e1bbe730b391a625140','/root/independent_wave10_d'),
}
WAVE10_REPORTS = {sequence:'reports/full-corpus-review/independent-phase10-'+letter+'-review.json'
                  for sequence,letter in zip(WAVE10,'abcd')}
WAVE10_RESULTS = {sequence:'reports/full-corpus-review/independent-phase10-'+letter+'-result.json'
                  for sequence,letter in zip(WAVE10,'abcd')}
WAVE10_NO_KEY_CREDIT = frozenset({'MA-RW-0051','MA-RW-0061','MA-RW-0062','MA-RW-0064'})


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def safe_bytes(root, relative):
    pure = PurePosixPath(relative)
    require(not pure.is_absolute() and '..' not in pure.parts and str(pure) == relative,
            'After190 annotation expands protected scope')
    path = root / relative
    require(root.resolve() in path.resolve().parents and path.is_file() and not path.is_symlink(),
            'Missing or unsafe after190 annotation input: ' + relative)
    return path.read_bytes()


def committed(root, relative, bindings):
    raw = safe_bytes(root, relative)
    require(subprocess.check_output(['git', '-C', str(root), 'show', 'HEAD:' + relative]) == raw,
            'Uncommitted after190 attested source: ' + relative)
    bindings[relative] = sha(raw)
    return raw


def validate_delta_job(job):
    require(job.get('job_id') == NOTE_DELTA_JOB and job.get('sequence') == 23 and
            job.get('unit_ids') == [NOTE_DELTA_UNIT] and
            set(job.get('unit_bindings', {})) == {NOTE_DELTA_UNIT},
            'After190 note delta scope changed')
    require(job.get('status') == 'INTEGRATED',
            'After190 note delta is pending/LEASED; integrate and explicitly rebind before publication')
    require(job['unit_bindings'][NOTE_DELTA_UNIT]['census_path'] == V4_CENSUS,
            'After190 v4 census selection changed')


def validate_phase7_report(job, report, events):
    """Validate captured reviewer declarations without claiming identity proof."""
    question_queue.validate_independent_provenance(job, report)
    submitted = job['result']; actor = submitted['actor_provenance']
    require(report.get('stage') == 'independent-legacy' and
            report.get('actor_provenance') == actor and
            all(report.get(k) == submitted.get(k) for k in ('auditor','auditor_instance')) and
            report.get('canonical_audit') is False and
            type(report.get('canonical_release_credit')) is int and report['canonical_release_credit'] == 0 and
            any(e.get('kind') == 'CLAIM' and e.get('job_id') == job['job_id'] and
                e.get('worker') == job['worker'] and e.get('attempt') == job['attempt'] for e in events),
            'After190 phase7 source stage/provenance/credit differs from controller claim')


def validate_legacy_scope(state):
    """Exact jobs1-37; allocation/pending status is never a source receipt."""
    jobs = state['jobs']
    projection=[dict(sequence=j['sequence'],job_id=j['job_id'],stage=j.get('stage'),
                     question_hashes=j['question_hashes'])for j in jobs[:29]]
    require([j['sequence'] for j in jobs] == list(range(1,38)) and
            question_queue.digest(projection)==LEGACY_SCOPE_SHA,
            'After190 legacy job scope expanded; explicit new guard review required')
    require(question_queue.digest(jobs[:33])==PRIOR_LEGACY_RECEIPTS_SHA,
            'After190 prior1-33 integrated scope/receipt/history changed')
    for job in jobs:
        if job['sequence'] in WAVE9 or job['sequence'] in WAVE10:
            expected=(WAVE9|WAVE10)[job['sequence']]
            require((job['job_id'],question_queue.digest(job['question_hashes']),job.get('worker'))==expected and
                    len(job['question_hashes'])==40 and job.get('stage')=='independent-legacy',
                    'After190 exact wave9/wave10 scope/current actor changed')
            if job['sequence'] in WAVE10:
                require(job.get('selection_policy')=='REMEDIATION_THEN_SOURCE_DEFAULT_THEN_LEXICAL' and
                        question_queue.digest(job.get('priority_source_sha256'))==WAVE10_PRIORITY_SOURCES_SHA,
                        'After190 exact wave10 allocation priority provenance changed')
    current_default_ids=[qid for j in jobs if j['sequence'] in WAVE9 for qid in j['question_hashes']]
    require(len(current_default_ids)==len(set(current_default_ids))==160,'Wave9 is not exactly160 distinct default questions')
    next_ids=[qid for j in jobs if j['sequence'] in WAVE10 for qid in j['question_hashes']]
    require(len(next_ids)==len(set(next_ids))==160 and not set(next_ids)&set(current_default_ids),
            'Wave10 is not the exact160 distinct new assigned questions')
    for job in jobs:
        require(job['status']=='INTEGRATED' and job.get('result') and job.get('integrated_commit') and
                job.get('integrated_at') and any(e.get('kind')=='INTEGRATE'and
                    e.get('job_id')==job['job_id']and e.get('commit')==job['integrated_commit']for e in state['events']),
                'After190 legacy result pending/LEASED or lacks actual captured integration; integrate/rebind first')


def validate_wave10_key_limits(job,report):
    """Retain the actual C source-context exposure boundary, without new credit.

    This consumes the controller's reported findings. It does not certify the
    unseen primary law, restore any default or turn the remaining36 into PASS.
    """
    if job['sequence'] != 36:
        return
    rows={row['question_id']:row for row in report['records']}
    blocked=report.get('whole_key_credit_blocked_ids')
    require(isinstance(blocked,list) and len(blocked)==len(WAVE10_NO_KEY_CREDIT) and
            set(blocked)==WAVE10_NO_KEY_CREDIT and WAVE10_NO_KEY_CREDIT <= set(rows) and all(
            rows[qid]['legal_review'].get('existing_answer_correct')=='NOT_ASSESSED' and
            rows[qid]['legal_review'].get('verdict') in {'HOLD','MINOR_EDIT','MAJOR_REWRITE','DELETE'} and
            all(type(rows[qid]['legal_review'].get(key)) is int and
                rows[qid]['legal_review'][key]==0 for key in
                ('whole_key_assessment_credit','fresh_whole_key_credit')) and
            str(rows[qid]['legal_review'].get('blocker','')).startswith(
                'PROCEDURAL_PRIOR_SOURCE_CONCLUSION_EXPOSURE:') and
            rows[qid].get('safe_hold_recommended',True) is True
            for qid in WAVE10_NO_KEY_CREDIT),
            'Wave10 C source-context exposure IDs must retain NOT_ASSESSED/safety hold and zero fresh whole-key credit')


def validate_wave10_default_holds(selection):
    require(WAVE10_NO_KEY_CREDIT <= {row['question_id'] for row in selection.get('safety_holds',[])} and
            not WAVE10_NO_KEY_CREDIT & set(selection['recommended_ids']),
            'Wave10 C procedural holds must remain explicit and excluded from current defaults')


def validate_note_scope(state):
    jobs=state['jobs'];original=jobs[:30]
    projection=[dict(sequence=j['sequence'],job_id=j['job_id'],unit_bindings=j['unit_bindings'])for j in original]
    require(len(jobs)==31 and [j['sequence']for j in jobs]==list(range(1,32)) and
            notes_queue.digest(projection)==NOTE_SCOPE_SHA and
            {j['sequence']:(j['job_id'],j['unit_ids'])for j in original if j['sequence']>=24}==NOTE_FOLLOWUPS,
            'After190 note scope needs exact jobs1-30 plus the committed inactive body job31')
    require(all(j['status']=='INTEGRATED'and j.get('result')and j.get('integrated_commit')and j.get('integrated_at')and
                any(e.get('kind')=='INTEGRATE'and e.get('job_id')==j['job_id']and e.get('commit')==j['integrated_commit']for e in state['events'])
                for j in original),'After190 note result pending/LEASED; integrate/rebind jobs1-30 first')
    require(BODY_REGISTRATION_RECORD and BODY_REGISTRATION_SHA and BODY_JOB_ID,
            'After190 exact root body registration is not yet bound; no future receipt is assumed')
    job=jobs[30]
    require(job['job_id']==BODY_JOB_ID and job.get('purpose')=='BODY_CORRECTION_REASSESSMENT' and
            job['unit_ids']==['w3-a-3'] and not job.get('reassessment_id') and
            len(state.get('body_reassessments',[]))==1,
            'After190 inactive body correction scope expanded or mixed with census-only review')
    entry=state['body_reassessments'][0]
    require(entry['record_path']==BODY_REGISTRATION_RECORD and entry['raw_sha256']==BODY_REGISTRATION_SHA and
            job['body_reassessment_record_sha256']==BODY_REGISTRATION_SHA and
            job['body_reassessment_id']==entry['record']['body_reassessment_id'],
            'After190 root body registration path/raw SHA differs')
    return job


def retained_evidence_references(value,pointer=''):
    """Pair retained bytes with their own SHA, not an underlying remote raw SHA.

    A provenance memo's `path`/`sha256` may also describe the fetched payload's
    `raw_sha256`. That payload has a separate raw_path; its hash is not the memo's.
    """
    if isinstance(value, dict):
        for key, path in value.items():
            if not isinstance(path, str):
                continue
            # Historical worker input receipt, not retained legal evidence.
            # Exact assigned question hashes are independently checked above.
            if key == 'assignment_path':
                continue
            candidates = []
            if key.endswith('_path'):
                candidates.append(key[:-5] + '_sha256')
                if key in {'raw_evidence_path','payload_path'}:
                    candidates.append('raw_sha256')
            elif key == 'source_evidence':
                candidates.append('source_evidence_sha256')
            elif key == 'path':
                candidates.extend(('sha256','raw_sha256','file_sha256'))
            for hash_key in candidates:
                if hash_key in value:
                    yield path, value[hash_key], pointer+'/'+key.replace('~','~0').replace('/','~1')
                    break
        for key,child in value.items():
            yield from retained_evidence_references(child,pointer+'/'+key.replace('~','~0').replace('/','~1'))
    elif isinstance(value, list):
        for index,child in enumerate(value):
            yield from retained_evidence_references(child,pointer+'/'+str(index))


def retained_evidence_bindings(value):
    for path,expected,_ in retained_evidence_references(value):yield path,expected


def bind_current_review_context(root,bindings):
    """Historical receipts cannot stand in for current counters/instructions."""
    from after190_historical_context import PROGRESS,RUNBOOK
    committed(root,RUNBOOK,bindings)
    selection=committed(root,'practice_expansion/2026-10-28-representative/selection.json',bindings)
    validate_wave10_default_holds(json.loads(selection))
    current=committed(root,PROGRESS,bindings)
    # Isolated import keeps a caller's alternate/shallow root independent of this
    # interpreter's module globals. build() returns payloads and writes nothing.
    code=('import sys;sys.path.insert(0,sys.argv[1]);import build_full_corpus_review as b;'
          'sys.stdout.write(b.build()[b.OUT/"progress.json"])')
    expected=subprocess.check_output([sys.executable,'-c',code,str(root/'scripts')],cwd=root)
    require(current==expected,'Current progress differs from actual source builder; historical receipts cannot replace counters')


def zero_credit(value):
    require(value.get('canonical_audit') is False and
            all(type(value.get(k)) is int and value[k] == 0
                for k in ('canonical_release_credit', 'question_audit_credit', 'new_author_review_credit',
                          'new_independent_legal_audit_credit')),
            'After190 annotation cannot create legal/author/question/release credit')


def bind_inactive_body(root,state,job,independent,bindings):
    """One exact root re-registration; never an active body/credit exception."""
    original=json.loads(committed(root,BODY_ORIGINAL_RECORD,bindings))
    require(bindings[BODY_ORIGINAL_RECORD]==BODY_ORIGINAL_SHA,'Original inactive body record changed')
    record=json.loads(committed(root,BODY_REGISTRATION_RECORD,bindings))
    require(bindings[BODY_REGISTRATION_RECORD]==BODY_REGISTRATION_SHA and
            record==state['body_reassessments'][0]['record'] and
            set(record)==set(original)|{'registration_rebinding'} and
            record['body_reassessment_id']==BODY_REGISTRATION_ID and
            all(record.get(k)==v for k,v in original.items()if k not in
                {'body_reassessment_id','other_current_bindings_sha256'}),
            'Body re-registration changed candidate, parent, mapping, law evidence or original negatives')
    rebinding=record['registration_rebinding']
    require(set(rebinding)=={'purpose','controller_actor','parent_record','root_checkpoint','previous_ledger_snapshot',
                            'changed_sibling_census_units','changed_sibling_binding_hashes','all_306_active_bodies_unchanged',
                            'body_census_parent_claims_and_negatives_unchanged','independent_credit'} and
            rebinding['purpose']=='CONTROLLER_OPERATIONAL_FINGERPRINT_REBIND_NOT_BODY_OR_CENSUS_EDIT'and
            rebinding['controller_actor']=='/root'and
            rebinding['parent_record']=={'path':BODY_ORIGINAL_RECORD,'raw_sha256':BODY_ORIGINAL_SHA}and
            rebinding['root_checkpoint']==BODY_REGISTRATION_CHECKPOINT and
            rebinding['all_306_active_bodies_unchanged']is True and
            rebinding['body_census_parent_claims_and_negatives_unchanged']is True and
            type(rebinding['independent_credit'])is int and rebinding['independent_credit']==0,
            'Body operational re-registration provenance/scope changed')
    snapshot=rebinding['previous_ledger_snapshot'];old_raw=committed(root,snapshot['path'],bindings)
    require(sha(old_raw)==snapshot['raw_sha256'],'Previous retained census ledger changed')
    current=notes_queue.inventory(root);previous=notes_queue.inventory(root,current['notes'],ledger_raw=old_raw);uid='w3-a-3'
    changed=sorted(k for k,b in previous['units'].items()if current['units'].get(k)!=b)
    require(changed==rebinding['changed_sibling_census_units']==['w2-c-12','w3-a-6','w3-a-7']and
            rebinding['changed_sibling_binding_hashes']=={k:{'before':notes_queue.digest(previous['units'][k]),
                'after':notes_queue.digest(current['units'][k])}for k in changed} and
            current['units'][uid]==previous['units'][uid]==original['previous_binding']and
            all(b['body_sha256']==current['units'][k]['body_sha256']for k,b in previous['units'].items())and
            notes_queue.digest({k:b for k,b in previous['units'].items()if k!=uid})==original['other_current_bindings_sha256']and
            notes_queue.digest({k:b for k,b in current['units'].items()if k!=uid})==record['other_current_bindings_sha256'],
            'Body registration must change only the exact three sibling census bindings, not any body or target claim')
    row=independent['units']['w3-a-3']
    require(row.get('current_review_valid')is False and row.get('requires_review')is True and
            row.get('legal_status')=='LEGAL_HOLD' and
            job['unit_bindings']['w3-a-3']['body_sha256']!=original['previous_binding']['body_sha256'],
            'Inactive body candidate cannot inherit old KEEP or current legal/release credit')
    for payload in (record,json.loads(safe_bytes(root,record['replacement']['census_path'])),
                    json.loads(safe_bytes(root,record['primary_retrieval']['path']))):
        for path,expected in set(retained_evidence_bindings(payload)):
            require(sha(committed(root,path,bindings))==expected,'Inactive body retained source raw SHA changed: '+path)
    return dict(job_id=job['job_id'],sequence=31,status=job['status'],unit_id='w3-a-3',
        record_path=BODY_REGISTRATION_RECORD,record_raw_sha256=BODY_REGISTRATION_SHA,
        original_record_path=BODY_ORIGINAL_RECORD,original_record_raw_sha256=BODY_ORIGINAL_SHA,
        binding=job['unit_bindings']['w3-a-3'],current_review_valid=False,
        candidate_review_valid=row.get('candidate_review_valid',False),current_credit=0,
        publication_blocker=record['publication_blocker'])


def validate_selection_delta(selection,before,negative_ids):
    """Only explicit, reviewed unsafe removals; retain the before snapshot/history."""
    final_ids=selection['recommended_ids']
    require(len(final_ids)==len(set(final_ids))and set(final_ids)<=set(before['recommended_ids'])and
            final_ids==[qid for qid in before['recommended_ids']if qid in set(final_ids)],
            'After190 cannot restore or invent defaults; final selection may only remove source-bound unsafe items')
    for collection,key in [('holds','legacy_question_id'),('safety_holds','question_id')]:
        after={h[key]:h for h in selection[collection]}
        require(len(after)==len(selection[collection])and all(after.get(h[key])==h for h in before[collection]),
                'Original default hold/history changed')
    added_holds=({h['legacy_question_id']for h in selection['holds']}-{h['legacy_question_id']for h in before['holds']})|(
        {h['question_id']for h in selection['safety_holds']}-{h['question_id']for h in before['safety_holds']})
    require(set(before['recommended_ids'])-set(final_ids)==added_holds and added_holds<=set(negative_ids),
            'Final default removals differ from explicit current source-bound negative findings')


def bind_native_author(root,bindings):
    from build_full_corpus_review import REVIEW_FILES
    import remediation_author_reviews as native
    from build_sata_remediation_candidates import BASE,PUBLIC_BANKS,PUBLISHED_BASELINE,ALLOCATION,validate_preservation
    sources=native.load_sources(root,REVIEW_FILES)
    baseline=native.read_baseline(root)
    state=json.loads(committed(root,native.QUEUE,bindings))
    require(len(REVIEW_FILES)==63 and len(state['jobs'])==53 and len(sources)==1,
            'After190 author scope must remain original63 static sources plus actual native job53')
    for path in (native.BASELINE,native.REGISTRY,*baseline['static_source_sha256']):committed(root,path,bindings)
    job=state['jobs'][52];result=job['result']
    report_path='reports/full-corpus-review/'+next(iter(sources))
    report=sources[report_path.removeprefix('reports/full-corpus-review/')]
    for relative,expected in set(retained_evidence_bindings(report)):
        require(sha(committed(root,relative,bindings))==expected,'Native author retained payload changed')
    committed(root,report_path,bindings)
    result_path=report_path.removesuffix('-review.json')+'-result.json'
    require(json.loads(committed(root,result_path,bindings))==result,'Native author original envelope changed')
    selection_path='practice_expansion/2026-10-28-representative/selection.json'
    selection=json.loads(committed(root,selection_path,bindings))
    allocation_raw=committed(root,ALLOCATION,bindings)
    require(sha(allocation_raw)==ALLOCATION_SHA,'Original native allocation/preservation snapshot changed')
    allocation=json.loads(allocation_raw);before=allocation['preserved_selection']
    require(len(before['recommended_ids'])==298 and notes_queue.digest(before['recommended_ids'])==BEFORE_DEFAULT_IDS_SHA,
            'After190 before-default298 snapshot changed')
    legacy_state=json.loads(safe_bytes(root,LEGACY_STATE))
    require(all(set(j['question_hashes'])<=set(before['recommended_ids'])for j in legacy_state['jobs']if j['sequence'] in WAVE9),
            'Wave9 scope is not the exact original current-default cohort')
    final_ids=selection['recommended_ids']
    bank=json.loads(committed(root,BASE+'/questions.json',bindings));validate_preservation(bank,root)
    public=[q for p in PUBLIC_BANKS for q in json.loads(committed(root,p,bindings))['questions']]
    public_by_id={q['question_id']:q for q in public}
    require(len(public)==len(public_by_id)==2349,
            'After190 archive scope must remain the original2346 plus exactly three native candidates')
    require(all(notes_queue.digest(public_by_id[qid])==expected for qid,expected in allocation['public_question_record_hashes'].items())and
            len(allocation['public_question_record_hashes'])==2346,'Original2346 stored question objects changed')
    from build_representative_rewrites import validate_nonlegacy_selection
    baseline_selection=json.loads(committed(root,'practice_expansion/2026-10-27-quality/selection.json',bindings))
    validate_nonlegacy_selection(selection,baseline_selection,public_by_id,root)
    from build_full_corpus_review import validate_default_review_safety,validate_independent_archive_safety,ACTIONABLE_AUTHOR_DISPOSITIONS
    from procedural_secondary_metadata import load_metadata as secondary_metadata
    static=[json.loads(committed(root,'reports/full-corpus-review/'+p,bindings))for p in REVIEW_FILES]
    static+=list(sources.values())
    reviews={r['question_id']:r for source in static for r in source['records']}
    reports=[json.loads(committed(root,'reports/full-corpus-review/'+p,bindings))for p in
             ('pub05-14-independent-review.json','wave2-independent-review.json','wave5-independent-review.json')]+integrated_sources(root)
    records=[r for report in reports for r in report['records']]
    require(len(records)==len({r['question_id']for r in records})and
            all(r['record_sha256']==notes_queue.digest(public_by_id[r['question_id']])for r in records),
            'Default safety review references stale current question objects')
    collections={q['question_id']:p for p in PUBLIC_BANKS for q in json.loads(safe_bytes(root,p))['questions']}
    secondary=secondary_metadata(root,records,public_by_id,collections)
    negatives={qid for qid,r in reviews.items()if r['disposition'] in ACTIONABLE_AUTHOR_DISPOSITIONS}
    negatives.update(r['question_id']for r in records+secondary['records']if
                     r['legal_review'].get('verdict')!='KEEP'or r['legal_review'].get('existing_answer_correct')!='YES'or
                     r['realism_review'].get('verdict')!='PASS')
    validate_selection_delta(selection,before,negatives)
    validate_default_review_safety(final_ids,reviews,records+secondary['records'])
    validate_independent_archive_safety(selection,records+secondary['records'])
    for path in ('reports/representative-rewrite/default-holds.json','reports/representative-rewrite/nonlegacy-default-holds.json'):
        committed(root,path,bindings)
    for path in (PUBLISHED_BASELINE,ALLOCATION,'site/practice-expansion/publication.json'):committed(root,path,bindings)
    candidates=native.candidate_records(root)
    require(not set(candidates)&set(selection['recommended_ids']) and all(q['archive_only_candidate']is True for q in candidates.values()),
            'Native candidates must remain archive-only, outside default practice')
    return dict(job_id=job['job_id'],sequence=53,status='INTEGRATED',static_source_count=63,
        candidate_question_hashes=job['question_hashes'],actor_provenance=result['actor_provenance'],
        report_path=report_path,report_raw_sha256=bindings[report_path],result_path=result_path,
        result_raw_sha256=bindings[result_path],independent_review_credit=0,canonical_release_credit=0,
        archive_question_count=2349,before_default_count=298,before_default_ids_sha256=BEFORE_DEFAULT_IDS_SHA,
        default_count=len(final_ids),default_ids_sha256=notes_queue.digest(final_ids),
        provenance_basis='CONTROLLER_CAPTURED_NATIVE_AUTHOR_NOT_INDEPENDENT_REVIEW')


def bind_canonical_withdrawal(root,bindings):
    try:
        import canonical_q0012_withdrawal as withdrawal
    except ImportError as error:
        raise ValueError('After190 final gate requires the merged strict Q0012/linked-guide withdrawal decoder')from error
    withdrawal.validate(root)
    committed(root,withdrawal.MANIFEST,bindings)
    for path in (*withdrawal.PATHS,withdrawal.PREVIEW):committed(root,path,bindings)
    return dict(manifest_path=withdrawal.MANIFEST,manifest_raw_sha256=bindings[withdrawal.MANIFEST],
        current_protected_path_sha256s={p:bindings[p]for p in withdrawal.PATHS},
        verification='EXACT_WITHDRAWAL_CAUSE_PACKAGE_AND_METADATA_ONLY_DECODE',canonical_release_credit=0)


def bind_legacy_checkpoint(root,current,legacy_state,bindings):
    """Validate one exact actual source receipt; this helper creates no audit.

    make_manifest separately requires the complete approved scope to be IG.
    """
    require(current['status']=='INTEGRATED','Legacy source receipt is not actually integrated')
    question_queue.validate_result(current,current['result'])
    entry = dict(job_id=current['job_id'], sequence=current['sequence'], status=current['status'],
                 new_question_audit_credit=0, new_canonical_release_credit=0)
    if current['status'] == 'INTEGRATED':
        submitted = current['result']; actor = submitted.get('actor_provenance', {})
        require(actor.get('actor_id') == current.get('worker') and actor.get('session_id') and
                submitted.get('auditor_instance') and any(
                    e.get('kind') == 'CLAIM' and e.get('job_id') == current['job_id'] and
                    e.get('worker') == current['worker'] and e.get('attempt') == current['attempt']
                    for e in legacy_state['events']),
                'After190 legacy source lacks controller-captured claim provenance')
        evidence = {(r['evidence_path'], r['evidence_sha256']) for r in current['result']['results']}
        require(len(evidence) == 1, 'After190 requires one source-bound report per legacy job')
        path, expected = next(iter(evidence))
        report = json.loads(committed(root, path, bindings))
        require(len(report.get('records',[]))==len(current['question_hashes'])and
                {r.get('question_id')for r in report['records']}==set(current['question_hashes']),
                'Legacy report row scope changed')
        for row in submitted['results']:question_queue.validate_independent_evidence(current,row,report)
        require(sha(safe_bytes(root, path)) == expected and report['actor_provenance'] == actor and
                report.get('stage') == 'independent-legacy' and report.get('canonical_audit') is False and
                type(report.get('canonical_release_credit')) is int and report['canonical_release_credit'] == 0,
                'After190 legacy source identity/credit/raw binding changed')
        validate_phase7_report(current, report, legacy_state['events'])
        validate_wave10_key_limits(current,report)
        from build_full_corpus_review import validate_independent_source_bytes
        for authority in report.get('sources', []):
            validate_independent_source_bytes(authority, root)
        private_payloads = {(a.get('raw_path'),a.get('raw_sha256')) for a in report.get('sources', [])
                            if a.get('public_raw_redistribution') is False and
                            'memo' in a.get('public_evidence_mode','').lower()}
        references={}
        for source_path,source_sha,pointer in retained_evidence_references(report):
            references.setdefault((source_path,source_sha),set()).add(pointer)
        historical=[];private_extracted=[]
        from after190_historical_context import resolve as resolve_historical,resolve_private
        for (source_path,source_sha),pointers in references.items():
            # A declared private copyrighted raw payload was already handled
            # by the existing validator; only retained repository bytes bind.
            if PurePosixPath(source_path).is_absolute():
                descriptor=resolve_private(root,current,path,expected,report,source_path,source_sha,pointers,bindings,committed)
                if descriptor:
                    private_extracted.append(descriptor)
                    continue
                require((source_path,source_sha) in private_payloads,
                        'After190 unexpected unretained absolute evidence path')
                continue
            receipt=resolve_historical(root,current,path,expected,source_path,source_sha,pointers,bindings,committed)
            if receipt:
                historical.append(receipt)
                continue
            require(sha(committed(root, source_path, bindings)) == source_sha,
                    'After190 legacy retained source payload changed: ' + source_path)
        sequence=current['sequence']
        expected_path=(WAVE10_REPORTS[sequence]if sequence in WAVE10 else
                       WAVE9_REPORTS[sequence]if sequence in WAVE9 else
                       LEGACY_REPORTS.get(sequence)or NATIVE_LEGACY_REPORT)
        require(expected_path and path==expected_path,'After190 exact integrated report not yet pinned or changed')
        result_path=(WAVE10_RESULTS[sequence]if sequence in WAVE10 else
                     WAVE9_RESULTS[sequence]if sequence in WAVE9 else
                     NATIVE_LEGACY_RESULT if sequence==29 else path[:-len('-review.json')]+'-result.json')
        require(result_path,'After190 exact integrated envelope not yet pinned')
        result_raw = committed(root, result_path, bindings)
        require(json.loads(result_raw) == submitted and any(
                    e.get('kind') == 'SUBMIT' and e.get('job_id') == current['job_id'] and
                    e.get('result_sha256') == notes_queue.digest(submitted)
                    for e in legacy_state['events']),
                'After190 legacy envelope/submission binding changed')
        entry.update(actor_provenance=actor, auditor_instance=submitted['auditor_instance'],
                     evidence_path=path, evidence_sha256=expected,
                     result_path=result_path, result_raw_sha256=sha(result_raw),
                     provenance_basis='CONTROLLER_CAPTURED_CLAIM_NOT_IDENTITY_PROOF')
        if historical:entry['historical_context_receipts']=historical
        if private_extracted:entry['unretained_private_extracted_descriptors']=private_extracted
        if sequence==36:
            entry['source_context_exposure_no_fresh_key_credit_ids']=sorted(WAVE10_NO_KEY_CREDIT)
    return entry


def make_manifest(root=ROOT):
    """Derive an exact proposal from current attested sources; never refresh old guards.

    Actual source changes require rerunning this explicit preparation and
    review, not a permissive wildcard. Semantic edits require another pathway.
    """
    root = Path(root); bindings = {}; source_head=notes_queue.git(root,'rev-parse','HEAD')
    require(sha(safe_bytes(root, PARENT)) == PARENT_SHA,
            'Published PR190 fourteenth manifest changed; do not rebind a modified parent')
    # Fail before expensive rendering/current counters while any exact assigned
    # job is pending. An old unpublished33-job manifest is not a release receipt.
    legacy_state = json.loads(committed(root, LEGACY_STATE, bindings))
    validate_legacy_scope(legacy_state)
    baseline_md = safe_bytes(root, BASE_MD); baseline_build_raw = safe_bytes(root, BASE_BUILD)
    require(sha(baseline_md) == BASE_MD_SHA and sha(baseline_build_raw) == BASE_BUILD_SHA,
            'Published PR190 Markdown/build snapshot changed')
    baseline = json.loads(baseline_build_raw)
    notes = load_notes(root)
    semantic = sha(json.dumps(notes, ensure_ascii=False, sort_keys=True).encode())
    require(semantic == SEMANTIC == baseline['content_sha256'] and notes['edition'] == baseline['edition'] == EDITION and
            notes['revision_provenance'] == baseline['revision_provenance'],
            'After190 annotation cannot authorize semantic/edition/provenance changes')
    state = json.loads(committed(root, notes_queue.STATE, bindings)); notes_queue.validate_state(state)
    body_job=validate_note_scope(state)
    job = next(j for j in state['jobs'] if j['job_id'] == NOTE_DELTA_JOB)
    validate_delta_job(job)
    ledger = committed(root, notes_queue.LEDGER,bindings)
    rows = [json.loads(line) for line in ledger.decode().splitlines()]
    selected = {r['unit_id']: r for r in rows}
    require(selected[NOTE_DELTA_UNIT]['atomic_census_source'] == V4_CENSUS,
            'After190 current ledger does not select the actual v4 census')
    census_paths = sorted({r['atomic_census_source'] for r in rows})
    for path in census_paths:
        require(path.startswith('reports/full-corpus-review/') and path.endswith('.json'),
                'Unexpected after190 census input path')
        committed(root, path, bindings)
    require(question_queue.digest({path:bindings[path] for path in census_paths}) == CENSUS_BINDINGS_SHA,
            'After190 selected author census scope changed; explicit bounded review required')
    record_raw = committed(root, V4_RECORD, bindings)
    require(sha(record_raw) == job['reassessment_record_sha256'], 'After190 v4 version record changed')
    # Existing consumer validates the current committed report/envelope/authority
    # graph, controller-attested actor, exact bindings, pending credit and history.
    independent = note_metadata(root, notes, ledger_raw=ledger)
    delta = independent['units'][NOTE_DELTA_UNIT]
    require(delta.get('job_id') == NOTE_DELTA_JOB and delta.get('current_review_valid') is True,
            'After190 final E3 result is not the current attested note review')
    for path, expected in [(job['result']['evidence']['path'], job['result']['evidence']['raw_sha256']),
                           (job['result']['result_path'], job['result_sha256'])]:
        require(sha(committed(root, path, bindings)) == expected,
                'After190 E3 result/report raw binding changed')
    artifacts = job['result'].get('post_commit_validation', {}).get('artifacts', [])
    require(len(artifacts) == len({a['path'] for a in artifacts}) == 42,
            'After190 E3 original artifact scope changed')
    for artifact in artifacts:
        path = artifact['path']
        require(path.startswith('reports/full-corpus-review/independent-notes/reassessment-e3-') and
                sha(committed(root, path, bindings)) == artifact['raw_sha256'],
                'After190 E3 original artifact raw payload changed')
    body_checkpoint=bind_inactive_body(root,state,body_job,independent,bindings)
    # Bind every original/integrated note source, including retained authorities.
    from notes_independent_metadata import evidence_bindings
    for note_job in state['jobs']:
        if note_job['status']!='INTEGRATED':continue
        result=note_job['result']
        for path,expected in [(result['evidence']['path'],result['evidence']['raw_sha256']),
                              (result['result_path'],note_job['result_sha256'])]:
            require(sha(committed(root,path,bindings))==expected,'Integrated note report/envelope changed')
        report=json.loads(safe_bytes(root,result['evidence']['path']))
        for path,expected in set(notes_queue.validate_evidence(note_job,result,report))|set(evidence_bindings(report)):
            require(sha(committed(root,path,bindings))==expected,'Integrated note retained source changed')
    followups = []
    for followup in state['jobs']:
        if followup['sequence'] not in NOTE_FOLLOWUPS:
            continue
        descriptor = dict(job_id=followup['job_id'], sequence=followup['sequence'],
                          unit_ids=followup['unit_ids'], status=followup['status'],
                          annotation_question_audit_credit=0, annotation_legal_audit_credit=0)
        if followup['status'] == 'INTEGRATED':
            submitted = followup['result']
            for path, expected in [(submitted['evidence']['path'], submitted['evidence']['raw_sha256']),
                                   (submitted['result_path'], followup['result_sha256'])]:
                require(sha(committed(root, path, bindings)) == expected,
                        'After190 followup note report/envelope changed')
            descriptor.update(actor_provenance=followup['actor_provenance'],
                              auditor_instance=followup['auditor_instance'], evidence=submitted['evidence'],
                              result_path=submitted['result_path'], result_raw_sha256=followup['result_sha256'],
                              controller_independence_basis=followup['controller_independence_basis'],
                              provenance_basis='CONTROLLER_ATTESTED_DECLARATION_NOT_IDENTITY_PROOF')
        followups.append(descriptor)
    require(independent['progress']['question_audit_credit'] == independent['progress']['canonical_release_credit'] == 0 and
            independent['progress']['coverage_is_legal_pass'] is False,
            'After190 review processing is not legal/release credit')
    # All37 exact allocated jobs must have actual committed source receipts.
    integrated_sources(root)
    phase7=[bind_legacy_checkpoint(root,current,legacy_state,bindings)
            for current in legacy_state['jobs']if current['sequence']>=21]
    native_author_checkpoint=bind_native_author(root,bindings)
    bind_current_review_context(root,bindings)
    canonical_withdrawal_checkpoint=bind_canonical_withdrawal(root,bindings)
    from build_ultimate_notes import make_outputs
    outputs = make_outputs(root=root)
    expected_md = outputs[root / EXPORT].encode(); expected_build = outputs[root / BUILD].encode()
    built = json.loads(expected_build)
    semantic_fields = {k: v for k, v in built.items()
                       if k not in {'source_census_ledger_sha256', 'independent_note_review_progress'}}
    require(semantic_fields == {k: v for k, v in baseline.items()
                                if k not in {'source_census_ledger_sha256', 'independent_note_review_progress'}},
            'After190 generated build changed fields beyond census/review annotations')
    require(built['source_census_ledger_sha256'] == sha(ledger) and
            built['independent_note_review_progress'] == independent['progress'],
            'After190 generated annotation metadata differs from current source derivation')
    census_claim_count = sum(len(r['atomic_claim_ids']) for r in rows)
    require(len(rows) == len(selected) == 306 and census_claim_count == CENSUS_COUNT,
            'After190 author census scope changed beyond the exact v4/F3v2 selection')
    require(notes_queue.git(root,'rev-parse','HEAD')==source_head,
            'After190 source HEAD advanced during preparation; freeze the checkpoint and rerun')
    return dict(schema_version='notes-protected-after190-annotation-migration/1',
        purpose='FIFTEENTH_ANNOTATION_LAYER_NOT_SEMANTIC_OR_AUDIT_APPROVAL',
        publication_base_status='MERGED_PR190_TREE_MATCHED_PUBLIC_ORIGIN_NOT_ATTESTED_BY_THIS_GUARD',
        merged_pr190_commit=MERGED_PR190, merged_pr190_tree=MERGED_TREE, verified_candidate_commit=CANDIDATE, annotation_inputs_ready=True,
        publication_approval='NOT_GRANTED_BY_THIS_ENGINEERING_GUARD',
        path=EXPORT, baseline_copy=BASE_MD, baseline_build_copy=BASE_BUILD,
        old_sha256=BASE_MD_SHA, baseline_build_sha256=BASE_BUILD_SHA,
        previous_migration_path=PARENT, previous_migration_sha256=PARENT_SHA,
        semantic_notes_sha256=SEMANTIC, edition=EDITION,
        revision_provenance=notes['revision_provenance'], new_sha256=sha(expected_md),
        new_build_sha256=sha(expected_build), census_ledger_path=notes_queue.LEDGER,
        census_ledger_sha256=sha(ledger), author_claim_enumeration_count=census_claim_count,
        selected_author_census_bindings_sha256=CENSUS_BINDINGS_SHA,
        independent_note_review_progress=independent['progress'],
        note_delta=dict(job_id=NOTE_DELTA_JOB, unit_id=NOTE_DELTA_UNIT,
                        actor_provenance=job['actor_provenance'], auditor=job['auditor'],
                        auditor_instance=job['auditor_instance'],
                        controller_independence_basis=job['controller_independence_basis'],
                        provenance_basis='CONTROLLER_ATTESTED_DECLARATION_NOT_IDENTITY_PROOF',
                        report=job['result']['evidence'], result_path=job['result']['result_path'],
                        result_raw_sha256=job['result_sha256'], binding=job['unit_bindings'][NOTE_DELTA_UNIT]),
        followup_note_checkpoint=followups, e3_original_artifact_count=42,
        phase7_checkpoint=[e for e in phase7 if e['sequence'] in PHASE7],
        wave8_checkpoint=[e for e in phase7 if e['sequence'] in WAVE8],
        native_legacy_checkpoint=[e for e in phase7 if e['sequence']==29],
        wave9_checkpoint=[e for e in phase7 if e['sequence'] in WAVE9],
        wave10_checkpoint=[e for e in phase7 if e['sequence'] in WAVE10],
        inactive_body_checkpoint=body_checkpoint,native_author_checkpoint=native_author_checkpoint,
        canonical_withdrawal_checkpoint=canonical_withdrawal_checkpoint,
        scope_definition_commit=SCOPE_DEFINITION_COMMIT,
        wave10_scope_definition_commit=WAVE10_DEFINITION_COMMIT,
        source_bindings=dict(sorted(bindings.items())),
        canonical_audit=False, canonical_release_credit=0, question_audit_credit=0,
        new_author_review_credit=0, new_independent_legal_audit_credit=0)


def decode(root, relative, current):
    require(relative == EXPORT, 'After190 annotation expands protected export scope')
    metadata = json.loads(safe_bytes(root, MANIFEST)); zero_credit(metadata)
    require(metadata.get('annotation_inputs_ready') is True,
            'Pending after190 annotation proposal cannot be published; integrate/rebind/recheck')
    expected = make_manifest(root)
    require(metadata == expected, 'After190 annotation source/manifest changed; explicitly rebind and recheck')
    require(sha(current) == expected['new_sha256'] and
            sha(safe_bytes(root, BUILD)) == expected['new_build_sha256'],
            'Stale after190 annotation export/build; regenerate and explicitly rebind')
    # The caller now runs the original fourteen blocks against these exact bytes.
    return safe_bytes(root, BASE_MD)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Explicitly prepare this unpublished proposal only')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    expected = notes_queue.encoded(make_manifest())
    path = ROOT / MANIFEST
    if args.write:
        path.write_bytes(expected)
        print('Prepared after190 annotation proposal over merged PR190 snapshots; source changes require rebinding and QA.')
    elif args.check:
        require(path.read_bytes() == expected, 'After190 manifest requires explicit rebinding')
        print('Checked current source-bound after190 proposal; no release or audit approval granted.')
    else:
        print(expected.decode(), end='')


if __name__ == '__main__':
    main()
