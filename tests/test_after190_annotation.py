"""Fifteenth wrapper: exact merged baseline, current sources, no new audit credit."""
import copy
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import notes_after190_annotation as annotation
import verify_representative_protected as protected
from build_ultimate_notes import make_outputs


@pytest.fixture(scope='module')
def prepared():
    manifest = annotation.make_manifest(ROOT)
    assert json.loads((ROOT / annotation.MANIFEST).read_bytes()) == manifest
    outputs = make_outputs(root=ROOT)
    return manifest, outputs[ROOT / annotation.EXPORT].encode(), outputs[ROOT / annotation.BUILD].encode()


@pytest.fixture
def overlay(monkeypatch, prepared):
    manifest, markdown, build = prepared
    values = {annotation.MANIFEST: annotation.notes_queue.encoded(manifest), annotation.BUILD: build}
    original = annotation.safe_bytes
    def read(root, relative):
        return values[relative] if relative in values else original(root, relative)
    monkeypatch.setattr(annotation, 'safe_bytes', read)
    return values, manifest, markdown, build


def test_exact_pr190_snapshots_parent_and_unchanged_fourteen_guard_code():
    for path, expected in [(annotation.BASE_MD, annotation.BASE_MD_SHA),
                           (annotation.BASE_BUILD, annotation.BASE_BUILD_SHA),
                           (annotation.PARENT, annotation.PARENT_SHA)]:
        assert annotation.sha((ROOT / path).read_bytes()) == expected
    current = (ROOT / 'scripts/verify_representative_protected.py').read_text()
    anchor = "    fourteenth_path=root/"
    # Pinned against the actual merged PR190 tail; no historical Git object is
    # required by a shallow CI checkout. All fourteen original blocks remain.
    assert annotation.sha(current[current.index(anchor):].encode()) == 'ba8f3ae371b9cacf05e896064ebd3b6c170f151e9a877ca3b09113c6ca250300'


def test_proposal_binds_actual_v4_e3_progress_without_new_credit(prepared):
    manifest, _, _ = prepared
    assert manifest['verified_candidate_commit'] == annotation.CANDIDATE
    assert manifest['merged_pr190_commit'] == annotation.MERGED_PR190
    assert manifest['merged_pr190_tree'] == annotation.MERGED_TREE
    assert 'MERGED_PR190_TREE_MATCHED' in manifest['publication_base_status']
    assert manifest['publication_approval'] == 'NOT_GRANTED_BY_THIS_ENGINEERING_GUARD'
    assert manifest['author_claim_enumeration_count'] == 6985
    progress = manifest['independent_note_review_progress']
    assert 60 <= progress['processed_units'] <= 70
    assert progress['complete_units'] + progress['omissions_found_units'] == progress['processed_units']
    assert progress['coverage_is_legal_pass'] is False
    for key in ['canonical_release_credit','question_audit_credit','new_author_review_credit',
                'new_independent_legal_audit_credit']:
        assert type(manifest[key]) is int and manifest[key] == 0
    delta = manifest['note_delta']
    assert delta['job_id'] == annotation.NOTE_DELTA_JOB
    assert delta['provenance_basis'] == 'CONTROLLER_ATTESTED_DECLARATION_NOT_IDENTITY_PROOF'
    assert delta['report']['raw_sha256'] == '6efec2814cfadc9c1528b0f621448d97c33974a0781c6be5d5fa554fbcd3a582'
    assert len(delta['binding']['claim_record_sha256s']) == 18
    assert delta['binding']['census_path'] == annotation.V4_CENSUS
    assert {r['sequence']:r['job_id'] for r in manifest['phase7_checkpoint']} == annotation.PHASE7


def test_new_export_decodes_to_pr190_then_runs_all_old_guards(overlay):
    _, _, markdown, _ = overlay
    assert annotation.decode(ROOT, annotation.EXPORT, markdown) == (ROOT / annotation.BASE_MD).read_bytes()
    original = (ROOT / 'revisions/baselines/complete-notes-2026-10-23.1.md').read_bytes()
    assert protected.migrated_baseline_bytes(ROOT, annotation.EXPORT, markdown) == original


def test_full_protected_inventory_accepts_only_the_actual_derived_annotation(monkeypatch, overlay):
    _, _, markdown, _ = overlay
    original = protected.safe_file
    class Bytes:
        def read_bytes(self): return markdown
    monkeypatch.setattr(protected, 'safe_file', lambda root,path:
                        Bytes() if path == annotation.EXPORT else original(root,path))
    baseline = json.loads((ROOT / 'reports/representative-rewrite/protected-baseline.json').read_bytes())
    protected.verify(baseline, ROOT)


@pytest.mark.parametrize('field,value', [
    ('path','notes/guide.json'), ('baseline_copy','notes/guide.json'),
    ('merged_pr190_commit','0'*40), ('previous_migration_sha256','0'*64),
    ('semantic_notes_sha256','0'*64), ('edition','invented edition'),
    ('new_sha256','0'*64), ('new_build_sha256','0'*64),
    ('source_bindings',{}), ('author_claim_enumeration_count',6986),
])
def test_manifest_scope_source_semantic_and_output_tamper_cannot_rebind(overlay, field, value):
    values, manifest, markdown, _ = overlay
    changed = copy.deepcopy(manifest); changed[field] = value
    values[annotation.MANIFEST] = annotation.notes_queue.encoded(changed)
    with pytest.raises(ValueError, match='explicitly rebind'):
        annotation.decode(ROOT, annotation.EXPORT, markdown)


@pytest.mark.parametrize('key', ['canonical_release_credit','question_audit_credit',
                                'new_author_review_credit','new_independent_legal_audit_credit'])
def test_credit_inflation_including_boolean_zero_is_rejected(overlay, key):
    values, manifest, markdown, _ = overlay
    changed = copy.deepcopy(manifest); changed[key] = False
    values[annotation.MANIFEST] = annotation.notes_queue.encoded(changed)
    with pytest.raises(ValueError, match='cannot create'):
        annotation.decode(ROOT, annotation.EXPORT, markdown)


@pytest.mark.parametrize('path', [annotation.PARENT, annotation.BASE_MD, annotation.BASE_BUILD])
def test_even_a_rehashed_modified_published_parent_or_snapshot_is_rejected(overlay, path):
    values, manifest, markdown, _ = overlay
    values[path] = (ROOT / path).read_bytes() + b'\n'
    changed = copy.deepcopy(manifest)
    key = {annotation.PARENT:'previous_migration_sha256', annotation.BASE_MD:'old_sha256',
           annotation.BASE_BUILD:'baseline_build_sha256'}[path]
    changed[key] = annotation.sha(values[path])
    values[annotation.MANIFEST] = annotation.notes_queue.encoded(changed)
    with pytest.raises(ValueError, match='fourteenth manifest changed|snapshot changed'):
        annotation.decode(ROOT, annotation.EXPORT, markdown)


def test_injected_annotation_text_cannot_be_accepted_by_refreshing_new_sha(overlay):
    values, manifest, markdown, _ = overlay
    altered = markdown + b'\n> Invented legal approval.\n'
    changed = copy.deepcopy(manifest); changed['new_sha256'] = annotation.sha(altered)
    values[annotation.MANIFEST] = annotation.notes_queue.encoded(changed)
    with pytest.raises(ValueError, match='explicitly rebind'):
        annotation.decode(ROOT, annotation.EXPORT, altered)


def test_stale_current_build_even_with_unchanged_semantics_is_rejected(overlay):
    values, _, markdown, build = overlay
    stale = json.loads(build); stale['source_census_ledger_sha256'] = '0'*64
    values[annotation.BUILD] = annotation.notes_queue.encoded(stale)
    with pytest.raises(ValueError, match='Stale after190'):
        annotation.decode(ROOT, annotation.EXPORT, markdown)


@pytest.mark.parametrize('path', [annotation.V4_CENSUS, annotation.V4_RECORD,
                                 annotation.notes_queue.STATE, annotation.LEGACY_STATE])
def test_current_source_payload_changes_are_not_silently_rebound(overlay, path):
    values, _, markdown, _ = overlay
    values[path] = (ROOT / path).read_bytes() + b'\n'
    with pytest.raises(ValueError, match='Uncommitted after190'):
        annotation.decode(ROOT, annotation.EXPORT, markdown)


def test_actual_semantic_change_cannot_use_annotation_wrapper(monkeypatch, overlay):
    _, _, markdown, _ = overlay
    notes = copy.deepcopy(annotation.load_notes(ROOT)); notes['chapters'][0]['units'][0]['body'] += ' New legal claim.'
    monkeypatch.setattr(annotation, 'load_notes', lambda root: notes)
    with pytest.raises(ValueError, match='cannot authorize semantic'):
        annotation.decode(ROOT, annotation.EXPORT, markdown)


def test_leased_intermediate_note_job_or_pending_manifest_cannot_publish(overlay):
    state = json.loads((ROOT / annotation.notes_queue.STATE).read_bytes())
    job = next(j for j in state['jobs'] if j['job_id'] == annotation.NOTE_DELTA_JOB)
    job['status'] = 'LEASED'
    with pytest.raises(ValueError, match='pending/LEASED'):
        annotation.validate_delta_job(job)
    values, manifest, markdown, _ = overlay
    draft = copy.deepcopy(manifest); draft['annotation_inputs_ready'] = False
    values[annotation.MANIFEST] = annotation.notes_queue.encoded(draft)
    with pytest.raises(ValueError, match='Pending after190'):
        annotation.decode(ROOT, annotation.EXPORT, markdown)


def test_exact_two_pending_followups_have_no_annotation_review_credit(prepared):
    manifest, _, _ = prepared
    followups = manifest['followup_note_checkpoint']
    assert {r['sequence']:(r['job_id'],r['unit_ids']) for r in followups} == annotation.NOTE_FOLLOWUPS
    for row in followups:
        assert row['annotation_question_audit_credit'] == row['annotation_legal_audit_credit'] == 0
        if row['status'] != 'INTEGRATED':
            assert 'evidence' not in row and 'result_path' not in row
    assert manifest['e3_original_artifact_count'] == 42
    assert sum(p.startswith('reports/full-corpus-review/independent-notes/reassessment-e3-')
               for p in manifest['source_bindings']) == 42


@pytest.mark.parametrize('change', ['stage','actor','instance','credit','claim','independence'])
def test_future_integrated_phase7_requires_exact_captured_source_provenance(change):
    # Synthetic metadata-only fixture: no legal question/audit evidence is created.
    actor = {'actor_id':'/root/fixture-reviewer','session_id':'/root/fixture-reviewer'}
    submitted = {'actor_provenance':actor,'auditor':'GPT','auditor_instance':'fixture-instance'}
    job = {'job_id':annotation.PHASE7[21],'worker':actor['actor_id'],'attempt':1,'result':submitted}
    report = {**copy.deepcopy(submitted),'stage':'independent-legacy','independent_of_authors':True,
              'canonical_audit':False,'canonical_release_credit':0}
    events = [{'kind':'CLAIM','job_id':job['job_id'],'worker':job['worker'],'attempt':1}]
    annotation.validate_phase7_report(job, report, events)
    if change == 'stage': report['stage'] = 'author'
    elif change == 'actor': report['actor_provenance']['actor_id'] = '/root/wrong'
    elif change == 'instance': report['auditor_instance'] = 'different instance'
    elif change == 'credit': report['canonical_release_credit'] = False
    elif change == 'claim': events.clear()
    else: report['independent_of_authors'] = False
    with pytest.raises(ValueError): annotation.validate_phase7_report(job, report, events)


def test_exact_wave8_pending_checkpoint_has_no_evidence_or_integrated_credit(prepared):
    manifest, _, _ = prepared
    pending = manifest['pending_legacy_checkpoint']
    assert {r['sequence']:(r['job_id'],annotation.question_queue.digest(r['question_hashes']))
            for r in pending} == annotation.PENDING_LEGACY
    assert all(row['status'] in {'QUEUED','LEASED','SUBMITTED'} and
               row['evidence_credit'] == row['question_audit_credit'] == row['canonical_release_credit'] == 0 and
               'NOT_GRANTED' in row['integration_scope'] and 'evidence_path' not in row for row in pending)
    assert all(row['status'] == 'INTEGRATED' for row in manifest['phase7_checkpoint'])


@pytest.mark.parametrize('change', ['id','hash','count','sequence','stage','integrated','history','extra'])
def test_wave8_scope_or_integration_cannot_be_permitted_by_rebinding(change):
    state = json.loads((ROOT / annotation.LEGACY_STATE).read_bytes())
    job = state['jobs'][24]
    if change == 'id': job['job_id'] += '-invented'
    elif change == 'hash': job['question_hashes']['MA-EXP-0009'] = '0'*64
    elif change == 'count': job['question_hashes'].pop('MA-EXP-0009')
    elif change == 'sequence': job['sequence'] = 29
    elif change == 'stage': job['stage'] = 'author'
    elif change == 'integrated': job['status'] = 'INTEGRATED'
    elif change == 'history':
        state['events'].append({'kind':'INTEGRATE','job_id':job['job_id'],'commit':'0'*40})
    else:
        extra = copy.deepcopy(job); extra['sequence'] = 29; state['jobs'].append(extra)
    with pytest.raises(ValueError, match='scope|outside this guard'):
        annotation.validate_legacy_scope(state)


@pytest.mark.parametrize('status', ['QUEUED','LEASED','SUBMITTED'])
def test_only_exact_pending_wave8_definitions_can_progress_without_integration(status):
    state = json.loads((ROOT / annotation.LEGACY_STATE).read_bytes())
    for job in state['jobs'][24:]: job['status'] = status
    annotation.validate_legacy_scope(state)


def test_committed_different_census_at_equal_count_cannot_be_rebound(monkeypatch):
    original = annotation.committed
    def changed(root, relative, bindings):
        raw = original(root, relative, bindings)
        if relative == annotation.V4_CENSUS:
            # Model an otherwise committed replacement; JSON and claim count
            # remain the same. Only the bounded census raw binding must reject.
            raw += b'\n'; bindings[relative] = annotation.sha(raw)
        return raw
    monkeypatch.setattr(annotation, 'committed', changed)
    with pytest.raises(ValueError, match='selected author census scope changed'):
        annotation.make_manifest(ROOT)


def test_provenance_memo_and_underlying_raw_payload_use_distinct_hashes():
    memo = {'path':'reports/memo.json','sha256':'a'*64,'raw_sha256':'b'*64,
            'payload':{'raw_path':'reports/official.pdf','raw_sha256':'b'*64},
            'input_binding':{'assignment_path':'/tmp/historical-input.json','assignment_sha256':'c'*64}}
    assert set(annotation.retained_evidence_bindings(memo)) == {
        ('reports/memo.json','a'*64),('reports/official.pdf','b'*64)}
