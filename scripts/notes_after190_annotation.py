"""Fifteenth annotation-only wrapper over the exact merged PR190 payloads.

This is release-gate engineering, not a new legal or question review. Preparation
and verification are read-only unless the explicit writer CLI is invoked.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess

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
# Exact selected census path/raw-SHA map at controller source f2eb58b3. A
# different author enumeration needs another bounded review, even at equal count.
CENSUS_BINDINGS_SHA = '10ed514a4f2af318274b38fae714e50319bd21b061d8f0e171149b85df7aa052'
NOTE_FOLLOWUPS = {
    24: ('review-independent-notes-9ef0ae660e8bc055',
         ['w2-c-7','w2-c-8','w2-c-9','w2-c-10','w2-c-11']),
    25: ('review-independent-notes-1a27fcbc5afaebf5',
         ['w2-c-12','w2-c-13','w2-c-14','w2-c-15','w2-c-17']),
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
# Explicit pending definitions supplied by the controller at f2eb58b3. They may
# progress through submission, but this guard grants no integrated scope to them.
PENDING_LEGACY = {
    25: ('review-independent-legacy-ff9c4b960dd7395f',
         'ff9c4b960dd7395fbd87a79a3b21e6000fe1af522ced6a9291f8670dbe693c65'),
    26: ('review-independent-legacy-fa06bb98482969e9',
         'fa06bb98482969e9ef9685e4e72f440021e50990a96ea77d6a547b0305ea4606'),
    27: ('review-independent-legacy-f1e95ede99682885',
         'f1e95ede99682885476b714756f2524450930343431b7afa9e833def2c1ae956'),
    28: ('review-independent-legacy-69f7982833d308b0',
         '69f7982833d308b0cd6c08b08407a93118bed7701224a10028950572f5f1cd87'),
}


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
    """Four approved integrations plus four exact pending definitions only."""
    jobs = state['jobs']
    expected = dict(PHASE7)
    expected.update({sequence: value[0] for sequence, value in PENDING_LEGACY.items()})
    require([j['sequence'] for j in jobs] == list(range(1,29)) and
            {j['sequence']:j['job_id'] for j in jobs if j['sequence'] >= 21} == expected,
            'After190 legacy job scope expanded; explicit new guard review required')
    for job in jobs:
        sequence = job['sequence']
        if sequence < 21:
            continue
        expected_sha = PHASE7_HASHES.get(sequence) or PENDING_LEGACY[sequence][1]
        require(job.get('stage') == 'independent-legacy' and
                len(job['question_hashes']) == 40 and
                question_queue.digest(job['question_hashes']) == expected_sha,
                'After190 exact legacy question scope changed')
        if sequence in PENDING_LEGACY:
            require(job['status'] in {'QUEUED','LEASED','SUBMITTED'} and
                    not job.get('integrated_commit') and not job.get('integrated_at') and
                    not any(e.get('kind') == 'INTEGRATE' and e.get('job_id') == job['job_id']
                            for e in state['events']),
                    'After190 wave8 integration is outside this guard; new bounded approval required')


def retained_evidence_bindings(value):
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
                    yield path, value[hash_key]
                    break
        for child in value.values():
            yield from retained_evidence_bindings(child)
    elif isinstance(value, list):
        for child in value:
            yield from retained_evidence_bindings(child)


def zero_credit(value):
    require(value.get('canonical_audit') is False and
            all(type(value.get(k)) is int and value[k] == 0
                for k in ('canonical_release_credit', 'question_audit_credit', 'new_author_review_credit',
                          'new_independent_legal_audit_credit')),
            'After190 annotation cannot create legal/author/question/release credit')


def make_manifest(root=ROOT):
    """Derive an exact proposal from current attested sources; never refresh old guards.

    Later E3/phase7 source changes require rerunning this explicit preparation and
    review, not a permissive wildcard. Semantic edits require another pathway.
    """
    root = Path(root); bindings = {}
    require(sha(safe_bytes(root, PARENT)) == PARENT_SHA,
            'Published PR190 fourteenth manifest changed; do not rebind a modified parent')
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
    require(len(state['jobs']) == 25 and
            {j['sequence']: (j['job_id'],j['unit_ids']) for j in state['jobs'] if j['sequence'] >= 24} == NOTE_FOLLOWUPS,
            'After190 note job scope expanded; explicit new guard review required')
    job = next(j for j in state['jobs'] if j['job_id'] == NOTE_DELTA_JOB)
    validate_delta_job(job)
    ledger = safe_bytes(root, notes_queue.LEDGER)
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
    # Only the already allocated four phase7 jobs may extend this checkpoint.
    # Pending jobs grant no new evidence; integrated reports must be current,
    # controller-attested independent-legacy records with preserved envelopes.
    legacy_state = json.loads(committed(root, LEGACY_STATE, bindings))
    validate_legacy_scope(legacy_state)
    integrated_sources(root)
    phase7 = []
    for current in legacy_state['jobs']:
        if current['sequence'] not in PHASE7:
            continue
        entry = dict(job_id=current['job_id'], sequence=current['sequence'], status=current['status'],
                     new_question_audit_credit=0, new_canonical_release_credit=0)
        if current['status'] == 'INTEGRATED':
            submitted = current['result']; actor = submitted.get('actor_provenance', {})
            require(actor.get('actor_id') == current.get('worker') and actor.get('session_id') and
                    submitted.get('auditor_instance') and any(
                        e.get('kind') == 'CLAIM' and e.get('job_id') == current['job_id'] and
                        e.get('worker') == current['worker'] and e.get('attempt') == current['attempt']
                        for e in legacy_state['events']),
                    'After190 phase7 lacks controller-captured claim provenance')
            evidence = {(r['evidence_path'], r['evidence_sha256']) for r in current['result']['results']}
            require(len(evidence) == 1, 'After190 phase7 requires one source-bound report per job')
            path, expected = next(iter(evidence))
            report = json.loads(committed(root, path, bindings))
            require(sha(safe_bytes(root, path)) == expected and report['actor_provenance'] == actor and
                    report.get('stage') == 'independent-legacy' and report.get('canonical_audit') is False and
                    type(report.get('canonical_release_credit')) is int and report['canonical_release_credit'] == 0,
                    'After190 phase7 source identity/credit/raw binding changed')
            validate_phase7_report(current, report, legacy_state['events'])
            from build_full_corpus_review import validate_independent_source_bytes
            for authority in report.get('sources', []):
                validate_independent_source_bytes(authority, root)
            private_payloads = {(a.get('raw_path'),a.get('raw_sha256')) for a in report.get('sources', [])
                                if a.get('public_raw_redistribution') is False and
                                'memo' in a.get('public_evidence_mode','').lower()}
            for source_path, source_sha in set(retained_evidence_bindings(report)):
                # A declared private copyrighted raw payload was already handled
                # by the existing validator; only retained repository bytes bind.
                if PurePosixPath(source_path).is_absolute():
                    require((source_path,source_sha) in private_payloads,
                            'After190 unexpected unretained absolute evidence path')
                    continue
                require(sha(committed(root, source_path, bindings)) == source_sha,
                        'After190 phase7 retained source payload changed: ' + source_path)
            require(path.startswith('reports/full-corpus-review/independent-phase7-') and
                    path.endswith('-review.json'), 'After190 phase7 report path expanded')
            result_path = path[:-len('-review.json')] + '-result.json'
            result_raw = committed(root, result_path, bindings)
            require(json.loads(result_raw) == submitted and any(
                        e.get('kind') == 'SUBMIT' and e.get('job_id') == current['job_id'] and
                        e.get('result_sha256') == notes_queue.digest(submitted)
                        for e in legacy_state['events']),
                    'After190 phase7 envelope/submission binding changed')
            entry.update(actor_provenance=actor, auditor_instance=submitted['auditor_instance'],
                         evidence_path=path, evidence_sha256=expected,
                         result_path=result_path, result_raw_sha256=sha(result_raw),
                         provenance_basis='CONTROLLER_CAPTURED_CLAIM_NOT_IDENTITY_PROOF')
        phase7.append(entry)
    pending_legacy = [dict(job_id=j['job_id'], sequence=j['sequence'], status=j['status'],
                           question_hashes=j['question_hashes'],
                           evidence_credit=0, question_audit_credit=0, canonical_release_credit=0,
                           integration_scope='NOT_GRANTED_REQUIRES_NEW_BOUNDED_GUARD_REVIEW')
                      for j in legacy_state['jobs'] if j['sequence'] in PENDING_LEGACY]
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
    require(len(rows) == len(selected) == 306 and census_claim_count == 6985,
            'After190 author census scope changed beyond the actual v4 addition')
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
        phase7_checkpoint=phase7, pending_legacy_checkpoint=pending_legacy,
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
