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
LIVE_MAKE_MANIFEST=annotation.make_manifest


@pytest.fixture(scope='module')
def prepared():
    try:
        manifest = annotation.make_manifest(ROOT)
    except ValueError as error:
        if any(s in str(error)for s in ['exact jobs1-30','pending/LEASED','not yet bound','not yet pinned','requires the merged strict']):
            pytest.skip('NOT_RUN: final committed release inputs unavailable: '+str(error))
        raise
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
    # The module fixture derives this expected proposal from the real complete
    # current source graph once. Wrapper mutation cases isolate decode/equality;
    # source/semantic mutation cases below explicitly restore the live derivation.
    monkeypatch.setattr(annotation,'make_manifest',lambda root=ROOT:copy.deepcopy(manifest))
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
    assert manifest['author_claim_enumeration_count'] == 6989
    progress = manifest['independent_note_review_progress']
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
    assert len(manifest['wave8_checkpoint'])==4 and len(manifest['native_legacy_checkpoint'])==1
    assert manifest['inactive_body_checkpoint']['current_credit']==0
    assert manifest['inactive_body_checkpoint']['current_review_valid']is False
    assert manifest['native_author_checkpoint']['before_default_count']==298
    assert manifest['native_author_checkpoint']['default_count']<=298


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
    ('source_bindings',{}), ('author_claim_enumeration_count',6990),
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
def test_even_a_rehashed_modified_published_parent_or_snapshot_is_rejected(monkeypatch,overlay,path):
    values, manifest, markdown, _ = overlay
    values[path] = (ROOT / path).read_bytes() + b'\n'
    changed = copy.deepcopy(manifest)
    key = {annotation.PARENT:'previous_migration_sha256', annotation.BASE_MD:'old_sha256',
           annotation.BASE_BUILD:'baseline_build_sha256'}[path]
    changed[key] = annotation.sha(values[path])
    values[annotation.MANIFEST] = annotation.notes_queue.encoded(changed)
    monkeypatch.setattr(annotation,'make_manifest',LIVE_MAKE_MANIFEST)
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
def test_current_source_payload_changes_are_not_silently_rebound(monkeypatch,overlay,path):
    values, _, markdown, _ = overlay
    values[path] = (ROOT / path).read_bytes() + b'\n'
    # Explicit live source proof, rather than the wrapper's cached expectation.
    monkeypatch.setattr(annotation,'make_manifest',LIVE_MAKE_MANIFEST)
    with pytest.raises(ValueError, match='Uncommitted after190'):
        annotation.decode(ROOT, annotation.EXPORT, markdown)


def test_actual_semantic_change_cannot_use_annotation_wrapper(monkeypatch, overlay):
    _, _, markdown, _ = overlay
    notes = copy.deepcopy(annotation.load_notes(ROOT)); notes['chapters'][0]['units'][0]['body'] += ' New legal claim.'
    monkeypatch.setattr(annotation, 'load_notes', lambda root: notes)
    monkeypatch.setattr(annotation,'make_manifest',LIVE_MAKE_MANIFEST)
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


def test_exact_wave8_and_native_checkpoint_require_actual_integrated_sources(prepared):
    manifest, _, _ = prepared
    rows=manifest['wave8_checkpoint']+manifest['native_legacy_checkpoint']
    assert [r['sequence']for r in rows]==list(range(25,30))
    assert all(r['status']=='INTEGRATED'and r['result_raw_sha256']and r['evidence_sha256']for r in rows)
    assert all(r['new_question_audit_credit']==r['new_canonical_release_credit']==0 for r in rows)
    assert all(row['status'] == 'INTEGRATED' for row in manifest['phase7_checkpoint'])


@pytest.mark.parametrize('change', ['id','hash','count','sequence','stage','pending','history','extra','fake_ig'])
def test_final_legacy_scope_or_missing_integration_cannot_be_permitted_by_rebinding(change):
    state = json.loads((ROOT / annotation.LEGACY_STATE).read_bytes())
    job = state['jobs'][24]
    if change == 'id': job['job_id'] += '-invented'
    elif change == 'hash': job['question_hashes']['MA-EXP-0009'] = '0'*64
    elif change == 'count': job['question_hashes'].pop('MA-EXP-0009')
    elif change == 'sequence': job['sequence'] = 29
    elif change == 'stage': job['stage'] = 'author'
    elif change == 'pending': job['status'] = 'LEASED'
    elif change == 'history':
        state['events']=[e for e in state['events']if not(e.get('kind')=='INTEGRATE'and e.get('job_id')==job['job_id'])]
    elif change=='fake_ig':
        state['jobs'][-1]['status']='INTEGRATED';state['jobs'][-1].pop('result',None)
    else:
        extra = copy.deepcopy(job); extra['sequence'] = 29; state['jobs'].append(extra)
    with pytest.raises(ValueError, match='scope|pending|integration'):
        annotation.validate_legacy_scope(state)


@pytest.mark.parametrize('status', ['QUEUED','LEASED','SUBMITTED'])
def test_even_exact_pending_definitions_cannot_prepare_final_release(status):
    state = json.loads((ROOT / annotation.LEGACY_STATE).read_bytes())
    for job in state['jobs'][24:]: job['status'] = status
    with pytest.raises(ValueError,match='pending/LEASED|scope'):annotation.validate_legacy_scope(state)


def test_committed_different_census_at_equal_count_cannot_be_rebound(monkeypatch,prepared):
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


def test_known_scope_definitions_are_exact_current_receipts_not_predicted_results():
    state=json.loads((ROOT/annotation.notes_queue.STATE).read_bytes())
    projection=[dict(sequence=j['sequence'],job_id=j['job_id'],unit_bindings=j['unit_bindings'])for j in state['jobs'][:30]]
    assert annotation.notes_queue.digest(projection)==annotation.NOTE_SCOPE_SHA
    legacy=json.loads((ROOT/annotation.LEGACY_STATE).read_bytes())
    projection=[dict(sequence=j['sequence'],job_id=j['job_id'],stage=j['stage'],question_hashes=j['question_hashes'])for j in legacy['jobs'][:29]]
    assert annotation.question_queue.digest(projection)==annotation.LEGACY_SCOPE_SHA
    assert annotation.CENSUS_COUNT==6989
    assert annotation.SCOPE_DEFINITION_COMMIT=='e78af1cd5ccdd749c3599aa4f36a217af4d06552'


def test_actual_incomplete_final_input_is_rejected_without_writing_any_publication_bytes():
    paths=[annotation.MANIFEST,annotation.EXPORT,annotation.BUILD,annotation.PARENT]
    before={p:(ROOT/p).read_bytes()for p in paths}
    state=json.loads((ROOT/annotation.notes_queue.STATE).read_bytes())
    legacy=json.loads((ROOT/annotation.LEGACY_STATE).read_bytes())
    if len(state['jobs'])==31 and all(j['status']=='INTEGRATED'for j in state['jobs'][:30]+legacy['jobs']):
        # Actual receipts are now complete; exercise the pending negative on an
        # in-memory copy rather than inventing or writing a pending checkpoint.
        pending=copy.deepcopy(legacy);pending['jobs'][-1]['status']='LEASED'
        with pytest.raises(ValueError,match='pending/LEASED'):annotation.validate_legacy_scope(pending)
    else:
        with pytest.raises(ValueError,match='exact jobs1-30|pending/LEASED|not yet bound'):annotation.make_manifest(ROOT)
    assert all((ROOT/p).read_bytes()==raw for p,raw in before.items())


@pytest.fixture
def scope_only_body_metadata(monkeypatch):
    """Synthetic shape fixture; no actual report/result is created or certified."""
    state=json.loads((ROOT/annotation.notes_queue.STATE).read_bytes())
    state['jobs']=state['jobs'][:30]
    for j in state['jobs']:
        if j['status']=='INTEGRATED':continue
        j.update(status='INTEGRATED',result={'SYNTHETIC_SCOPE_SHAPE_ONLY':True},integrated_commit='1'*40,integrated_at='2026-11-04T00:00:00+00:00')
        state['events'].append(dict(kind='INTEGRATE',job_id=j['job_id'],commit=j['integrated_commit']))
    path='reports/full-corpus-review/body-corrections/w3-a-3-v1/registrations/SYNTHETIC_NOT_CREATED.json'
    monkeypatch.setattr(annotation,'BODY_REGISTRATION_RECORD',path);monkeypatch.setattr(annotation,'BODY_REGISTRATION_SHA','a'*64)
    monkeypatch.setattr(annotation,'BODY_JOB_ID','synthetic-body-job31')
    record={'body_reassessment_id':'synthetic-body-correction'}
    state['body_reassessments']=[{'record_path':path,'raw_sha256':'a'*64,'record':record}]
    state['jobs'].append(dict(job_id='synthetic-body-job31',sequence=31,purpose='BODY_CORRECTION_REASSESSMENT',
        stage='independent-notes',status='QUEUED',unit_ids=['w3-a-3'],
        body_reassessment_id=record['body_reassessment_id'],body_reassessment_record_sha256='a'*64))
    return state


@pytest.mark.parametrize('defect',['id','unit','purpose','mixed','duplicate','record_sha','original_binding','extra_job','pending_old','missing_ig'])
def test_only_one_exact_inactive_body_slot_can_follow_the_original30(scope_only_body_metadata,defect):
    state=scope_only_body_metadata;job=state['jobs'][-1]
    assert annotation.validate_note_scope(state)==job
    if defect=='id':job['job_id']+='-other'
    elif defect=='unit':job['unit_ids']=['w3-a-4']
    elif defect=='purpose':job['purpose']='CENSUS_ONLY_OMISSION_REASSESSMENT'
    elif defect=='mixed':job['reassessment_id']='unrelated-census'
    elif defect=='duplicate':state['body_reassessments']*=2
    elif defect=='record_sha':job['body_reassessment_record_sha256']='b'*64
    elif defect=='original_binding':state['jobs'][0]['unit_bindings']['w1-a-2']['body_sha256']='b'*64
    elif defect=='extra_job':state['jobs'].append(dict(job,sequence=32))
    elif defect=='pending_old':state['jobs'][29]['status']='LEASED'
    else:state['events']=[e for e in state['events']if not(e.get('kind')=='INTEGRATE'and e.get('job_id')==state['jobs'][29]['job_id'])]
    with pytest.raises(ValueError):annotation.validate_note_scope(state)


def test_scope_shape_without_actual_registration_raw_bytes_cannot_publish(scope_only_body_metadata):
    state=scope_only_body_metadata;job=annotation.validate_note_scope(state)
    with pytest.raises(ValueError,match='Missing or unsafe'):annotation.bind_inactive_body(ROOT,state,job,{}, {})


@pytest.fixture(scope='module')
def actual_inactive_body():
    state=json.loads((ROOT/annotation.notes_queue.STATE).read_bytes())
    job=annotation.validate_note_scope(state);metadata=annotation.note_metadata(ROOT)
    return state,job,metadata


def test_actual_root_reregistration_preserves_candidate_negatives_and_only_three_sibling_bindings(actual_inactive_body):
    state,job,metadata=actual_inactive_body;bindings={}
    row=annotation.bind_inactive_body(ROOT,state,job,metadata,bindings)
    assert row['job_id']=='review-independent-notes-body-4c3229fb7bfb76b6'
    assert row['record_raw_sha256']=='945e120c2676793b7f6649d0eaa5a3cb4eb22b3f2e85fd56d273331a0730dd1c'
    assert row['current_credit']==0 and row['current_review_valid']is False
    assert len(row['binding']['claim_record_sha256s'])==24
    assert metadata['units']['w3-a-3']['requires_review'] and metadata['units']['w3-a-3']['legal_status']=='LEGAL_HOLD'
    assert metadata['progress']['inactive_body_candidate_units']==1
    assert annotation.BODY_ORIGINAL_RECORD in bindings and len(bindings)>8


@pytest.mark.parametrize('defect',['body_field','target_parent','mapping','fingerprint','sibling_scope','sibling_hash','credit','extra_field','current_credit'])
def test_rehashed_body_registration_cannot_expand_or_erase_preserved_source_scope(actual_inactive_body,monkeypatch,defect):
    state,job,metadata=copy.deepcopy(actual_inactive_body)
    record=state['body_reassessments'][0]['record']
    if defect=='body_field':record['change_basis']='Changed source body outside original record'
    elif defect=='target_parent':record['previous_binding']['body_sha256']='0'*64
    elif defect=='mapping':record['claim_mapping'].pop(next(iter(record['claim_mapping'])))
    elif defect=='fingerprint':record['other_current_bindings_sha256']='0'*64
    elif defect=='sibling_scope':record['registration_rebinding']['changed_sibling_census_units']=['w3-a-6']
    elif defect=='sibling_hash':record['registration_rebinding']['changed_sibling_binding_hashes']['w3-a-6']['after']='0'*64
    elif defect=='credit':record['registration_rebinding']['independent_credit']=True
    elif defect=='extra_field':record['skip_preservation_check']=True
    else:metadata['units']['w3-a-3']['current_review_valid']=True
    raw=annotation.notes_queue.encoded(record);monkeypatch.setattr(annotation,'BODY_REGISTRATION_SHA',annotation.sha(raw))
    original=annotation.committed
    def substituted(root,path,bindings):
        if path==annotation.BODY_REGISTRATION_RECORD:
            bindings[path]=annotation.sha(raw);return raw  # synthetic otherwise-committed altered record
        return original(root,path,bindings)
    monkeypatch.setattr(annotation,'committed',substituted)
    with pytest.raises(ValueError):annotation.bind_inactive_body(ROOT,state,job,metadata,{})


def test_actual_native_author_is_bound_as_author_only_and_preserves_archive_and_default():
    bindings={};row=annotation.bind_native_author(ROOT,bindings)
    assert row['sequence']==53 and row['static_source_count']==63 and row['status']=='INTEGRATED'
    assert row['independent_review_credit']==row['canonical_release_credit']==0
    assert row['archive_question_count']==2349 and row['before_default_count']==298 and row['default_count']<=298
    assert row['report_path']=='reports/full-corpus-review/sata-remediation-current-id-author/g-review.json'
    assert row['report_raw_sha256']==annotation.sha((ROOT/row['report_path']).read_bytes())
    assert set(row['candidate_question_hashes'])=={'MA-RW-0081','MA-RW-0082','MA-RW-0083'}
    assert len(bindings)>63


def test_actual_native_independent_receipt_has_exact_committed_report_envelope_and_primary_payloads():
    state=json.loads((ROOT/annotation.LEGACY_STATE).read_bytes());job=state['jobs'][28]
    assert job['status']=='INTEGRATED'
    bindings={};row=annotation.bind_legacy_checkpoint(ROOT,job,state,bindings)
    assert row['sequence']==29 and row['actor_provenance']['actor_id']=='/root/independent_case_f'
    assert row['evidence_path']==annotation.NATIVE_LEGACY_REPORT and row['result_path']==annotation.NATIVE_LEGACY_RESULT
    assert row['new_question_audit_credit']==row['new_canonical_release_credit']==0
    assert len(bindings)>10


def test_native_candidate_cannot_be_restored_to_default_by_rebinding(monkeypatch):
    original=annotation.committed
    def changed(root,path,bindings):
        raw=original(root,path,bindings)
        if path=='practice_expansion/2026-10-28-representative/selection.json':
            payload=json.loads(raw);payload['recommended_ids'].append('MA-RW-0081');raw=annotation.notes_queue.encoded(payload)
            bindings[path]=annotation.sha(raw)
        return raw
    monkeypatch.setattr(annotation,'committed',changed)
    with pytest.raises(ValueError,match='Default IDs|restore|archive'):annotation.bind_native_author(ROOT,{})


def test_old_fourteen_decoder_is_unchanged_under_the_new_wrapper_interface(monkeypatch):
    # Isolate the old decoder with its actual PR190 preimage; the new final
    # source gate is independently tested and may legitimately still be pending.
    raw=(ROOT/annotation.BASE_MD).read_bytes()
    monkeypatch.setattr(annotation,'decode',lambda root,relative,current:raw)
    original=(ROOT/'revisions/baselines/complete-notes-2026-10-23.1.md').read_bytes()
    assert protected.migrated_baseline_bytes(ROOT,annotation.EXPORT,b'Synthetic current wrapper')==original


def test_strict_canonical_withdrawal_composes_without_routing_protected_data_through_note_annotation(monkeypatch):
    import canonical_q0012_withdrawal as withdrawal
    bindings={};row=annotation.bind_canonical_withdrawal(ROOT,bindings)
    preimages=withdrawal.validate(ROOT)
    assert row['canonical_release_credit']==0 and row['manifest_raw_sha256']==withdrawal.MANIFEST_SHA
    def forbidden(*args):pytest.fail('Canonical protected data entered note annotation decoder')
    monkeypatch.setattr(annotation,'decode',forbidden)
    for path in withdrawal.PATHS:
        assert protected.migrated_baseline_bytes(ROOT,path,(ROOT/path).read_bytes())==preimages[path]


@pytest.mark.parametrize('defect',[None,'unknown_actor','changed_hash','extra_job','partial_ig'])
def test_only_exact_wave9_current_default_assignments_are_in_scope_and_pending_is_not_evidence(defect):
    state=json.loads((ROOT/annotation.LEGACY_STATE).read_bytes())
    assert len(state['jobs'])==37
    for j in state['jobs'][29:33]:
        assert(j['job_id'],annotation.question_queue.digest(j['question_hashes']),j['worker'])==annotation.WAVE9[j['sequence']]
    if defect=='unknown_actor':state['jobs'][29]['worker']='/root/unapproved-reviewer'
    elif defect=='changed_hash':state['jobs'][30]['question_hashes'][next(iter(state['jobs'][30]['question_hashes']))]='0'*64
    elif defect=='extra_job':state['jobs'].append(dict(state['jobs'][32],sequence=34))
    elif defect=='partial_ig':
        for j in state['jobs'][29:]:
            j['status']='INTEGRATED';j.pop('result',None)  # status-only without actual receipt
    if defect is None:
        # The preserved wave9 receipts are real, but the four newly allocated
        # wave10 jobs at this source checkpoint still have no source receipts.
        if all(j['status']=='INTEGRATED'for j in state['jobs']):
            annotation.validate_legacy_scope(state)
        else:
            with pytest.raises(ValueError,match='pending/LEASED'):
                annotation.validate_legacy_scope(state)
        return
    with pytest.raises(ValueError,match='scope|pending|integration'):annotation.validate_legacy_scope(state)


@pytest.mark.parametrize('defect',[None,'restore','arbitrary_drop','unreviewed','history','wrong_hold','duplicate'])
def test_final_default_can_shrink_for_actual_negatives_without_a_fixed_count_or_old_history_loss(defect):
    # Synthetic metadata-only shape test; source/primary validation is a separate
    # mandatory step in bind_native_author and is never bypassed by this helper.
    before=dict(recommended_ids=['a','b','c'],holds=[{'legacy_question_id':'old','reason':'preserved'}],safety_holds=[])
    after=copy.deepcopy(before);after['recommended_ids']=['a','c'];after['holds'].append({'legacy_question_id':'b','reason':'fresh bound negative'})
    negatives={'b'}
    if defect=='restore':after['recommended_ids'].append('new-id')
    elif defect=='arbitrary_drop':after['holds'].pop()
    elif defect=='unreviewed':negatives=set()
    elif defect=='history':after['holds'][0]['reason']='rewritten old history'
    elif defect=='wrong_hold':after['holds'][-1]['legacy_question_id']='c'
    elif defect=='duplicate':after['recommended_ids'].append('a')
    if defect:
        with pytest.raises(ValueError):annotation.validate_selection_delta(after,before,negatives)
    else:annotation.validate_selection_delta(after,before,negatives)
