"""Audit coverage and preservation tests; no legal audit is manufactured here."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from build_full_corpus_review import build, validate_review, validate_authored_record
from notes_revision import load_notes, REVISION
from verify_representative_protected import verify


def test_every_id_is_inventoried_without_inheriting_family_passes():
    outputs = build()
    for path, text in outputs.items():
        assert path.read_text() == text
    rows = [json.loads(s) for s in outputs[ROOT/'reports/full-corpus-review/question-ledger.jsonl'].splitlines()]
    assert len(rows) == len({r['question_id'] for r in rows}) == 2346
    assert sum(r['baseline_member'] for r in rows) == 2328
    assert sum(r['checked_at'] is not None for r in rows) == 161
    assert sum(r['legal_review_status']=='AUTHOR_SOURCE_CHECKED_NOT_INDEPENDENT' for r in rows) == 105
    assert sum(r['implementation_status']=='NEW_DISTINCT_ID' for r in rows) == 18
    assert sum(r['legal_review_status']=='HOLD_SOURCE_RELATIONSHIP' for r in rows) == 10
    assert sum(r['legal_review_status']=='NOT_REVERIFIED_IN_FULL_CORPUS_REVIEW' for r in rows) == 2185
    assert all(r['checked_at'] is None for r in rows if r['question_id'].startswith('MA-REV-'))
    assert not any(r['legal_review_status']=='RELEASED' for r in rows)
    assert all(r['deployment_status']=='CURRENT_BUILD_PUBLICATION_NOT_ASSERTED' for r in rows)
    assert {r['question_id'] for r in rows if r['historical_deployment_evidence']} == {
        'MA-RW-0061', 'MA-RW-0062', 'MA-RW-0064',
    }
    progress = json.loads(outputs[ROOT/'reports/full-corpus-review/progress.json'])
    assert progress['new_questions'] == 18
    assert progress['inventory_is_legal_review'] is False
    assert progress['canonical_independent_audit_this_session'] == 'NOT_RUN'


@pytest.mark.parametrize('review_file,qid', [
    ('unit3a-author-review.json', 'MA-EXP-0121'),
    ('mor-author-review.json', 'MA-EXP-0177'),
    ('mor-author-review.json', 'MA-EXP-0191'),
    ('discipline-author-review.json', 'MA-EXP-0193'),
    ('discipline-author-review.json', 'MA-EXP-0208'),
    ('discipline-procedures-author-review.json', 'MA-EXP-0223'),
    ('discipline-procedures-author-review.json', 'MA-EXP-0224'),
    ('cdtm-author-review.json', 'MA-EXP-0235'),
])
def test_stale_review_or_missing_choice_cannot_count_as_reviewed(review_file,qid):
    bank=json.loads((ROOT/'practice_expansion/2026-10-23/candidates/questions.json').read_text())
    q=next(q for q in bank['questions'] if q['question_id']==qid)
    reviews=json.loads((ROOT/'reports/full-corpus-review'/review_file).read_text())['records']
    r=next(r for r in reviews if r['question_id']==qid)
    validate_review(q,r)
    stale=copy.deepcopy(q); stale['stem']+=' New condition.'
    with pytest.raises(ValueError,match='Stale review'): validate_review(stale,r)
    missing=copy.deepcopy(r); missing['choice_by_choice_findings'].pop('A')
    with pytest.raises(ValueError,match='Missing choice'): validate_review(q,missing)
    empty=copy.deepcopy(r); empty['choice_by_choice_findings']['A']['exact_authority']=''
    with pytest.raises(ValueError,match='Empty choice'): validate_review(q,empty)


@pytest.mark.parametrize('source_file,qid', [
    ('07_mor_operations.json', 'MA-RW-0069'),
    ('07_mor_operations.json', 'MA-RW-0072'),
    ('08_discipline_reporting.json', 'MA-RW-0073'),
    ('08_discipline_reporting.json', 'MA-RW-0076'),
    ('09_discipline_procedures.json', 'MA-RW-0077'),
    ('09_discipline_procedures.json', 'MA-RW-0080'),
])
def test_new_review_credit_requires_current_authored_choices_and_date(source_file,qid):
    from build_representative_rewrites import content_hash
    base=ROOT/'practice_expansion/2026-10-28-representative'
    source=json.loads((base/'authoring'/source_file).read_text())
    authored=next(q for q in source['questions'] if q['question_id']==qid)
    bank=json.loads((base/'questions.json').read_text())
    q=next(q for q in bank['questions'] if q['question_id']==qid)
    validate_authored_record(q,authored,source)
    stale=copy.deepcopy(q); stale['choices'][0]['text']+=' A changed condition.'
    with pytest.raises(ValueError,match='Stale authored content hash'):
        validate_authored_record(stale,authored,source)
    stale['content_sha256']=content_hash(stale)
    with pytest.raises(ValueError,match='Stale authored review binding'):
        validate_authored_record(stale,authored,source)
    missing=copy.deepcopy(q); missing['explanation']['choice_analysis'].pop('A')
    missing['content_sha256']=content_hash(missing)
    with pytest.raises(ValueError,match='Stale authored choice findings'):
        validate_authored_record(missing,authored,source)
    stale_date=copy.deepcopy(q); stale_date['authored_at']='2026-10-29'
    stale_date['content_sha256']=content_hash(stale_date)
    with pytest.raises(ValueError,match='Stale authored review binding'):
        validate_authored_record(stale_date,authored,source)
    wrong_mapping=copy.deepcopy(q); wrong_mapping['competency_codes']=['1.2']
    wrong_mapping['content_sha256']=content_hash(wrong_mapping)
    with pytest.raises(ValueError,match='Stale authored review binding'):
        validate_authored_record(wrong_mapping,authored,source)
    wrong_note=copy.deepcopy(q); wrong_note['note_evidence'][0]['unit_id']='w1-a-1'
    wrong_note['content_sha256']=content_hash(wrong_note)
    with pytest.raises(ValueError,match='Stale authored note mapping'):
        validate_authored_record(wrong_note,authored,source)
    stale_revision=copy.deepcopy(q); stale_revision['notes_revision']['sha256']='0'*64
    stale_revision['content_sha256']=content_hash(stale_revision)
    with pytest.raises(ValueError,match='Stale authored notes revision'):
        validate_authored_record(stale_revision,authored,source)


def test_author_provenance_uses_each_source_and_never_inherits_family_review():
    outputs=build()
    rows={r['question_id']:r for r in map(json.loads,outputs[ROOT/'reports/full-corpus-review/question-ledger.jsonl'].splitlines())}
    for source_file in ['05_personnel_ratios.json','06_personnel_training.json',
                        '07_mor_operations.json','08_discipline_reporting.json','09_discipline_procedures.json']:
        relative='practice_expansion/2026-10-28-representative/authoring/'+source_file
        raw=(ROOT/relative).read_bytes(); source=json.loads(raw)
        for q in source['questions']:
            row=rows[q['question_id']]
            assert row['checked_at']==source['authored_at']
            assert row['reviewer_provenance']['authoring_source']==relative
            assert row['reviewer_provenance']['authoring_source_sha256']==hashlib.sha256(raw).hexdigest()
            assert row['reviewer_provenance']['independent']=='NOT_RUN'
    # The explicitly audited CDTM05 family is now source-scoped author-reviewed.
    for index in range(241,245):
        row=rows[f'MA-EXP-{index:04d}']
        assert row['checked_at']=='2026-10-30'
        assert row['legal_review_status']=='AUTHOR_SOURCE_CHECKED_NOT_INDEPENDENT'
        assert row['reviewer_provenance']['independent'] is False
    # Next unreviewed CDTM family must still NOT inherit a review by proximity.
    for index in range(305,309):
        row=rows[f'MA-EXP-{index:04d}']
        assert row['checked_at'] is None
        assert row['legal_review_status']=='NOT_REVERIFIED_IN_FULL_CORPUS_REVIEW'


def test_revised_units_preserve_cross_surface_warning_without_review_certificate():
    baseline=json.loads((ROOT/'notes/guide.json').read_text())
    effective=load_notes(ROOT)
    old={u['id']:u for c in baseline['chapters'] for u in c['units']}
    new={u['id']:u for c in effective['chapters'] for u in c['units']}
    assert old.keys()==new.keys()
    assert {uid for uid in old if old[uid]!=new[uid]} == {
        'w1-b-8','w1-b-9','w1-b-10','w1-c-4','w1-c-5','w1-c-7','w6-b-8','w1-c-13',
        'w1-c-14','w1-c-15','w4-d-17','w3-d-2','w3-d-3','authority-paths','w6-b-17',
        'w3-d-4','w3-d-5','w3-d-6','w3-d-7','w3-d-8',
    }
    assert 'OPEN' in new['w1-b-8']['body']
    assert '과거 읽음' in new['w1-b-8']['editor_note']
    assert hashlib.sha256((ROOT/'notes/guide.json').read_bytes()).hexdigest() == '004c2f9f309db00705a3b35ddd2fa1fb360235f4fd0d364a9ccdf8b3c43aa384'
    from build_exam_study import build_payload
    study=build_payload()
    assert 'OPEN' in next(l for l in study['lessons'] if l['id']=='LAW-012')['core']
    from build_refresh import build_payload as refresh
    assert 'OPEN' in next(c for c in refresh()['cards'] if c['id']=='RF-049')['watch']
    assert new['w1-b-8']['body_sha256'] == next(l for l in study['lessons'] if l['id']=='LAW-012')['source_hashes']['w1-b-8']


@pytest.fixture
def protected_copy(tmp_path):
    manifest=json.loads((ROOT/'reports/representative-rewrite/protected-baseline.json').read_text())
    for row in manifest['files']:
        dest=tmp_path/row['path']; dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(ROOT/row['path'],dest)
    shutil.copytree(ROOT/'revisions',tmp_path/'revisions')
    verify(manifest,tmp_path)
    return tmp_path,manifest


@pytest.mark.parametrize('relative',[
    'notes/guide.json', 'docs/RELEASE_POLICY.md',
    'revisions/baselines/complete-notes-2026-10-23.1.md',
    'site/notes/complete-notes.md', REVISION,
])
def test_protection_rejects_original_or_unapproved_hash_change(protected_copy,relative):
    root,manifest=protected_copy
    with (root/relative).open('ab') as stream: stream.write(b' changed')
    with pytest.raises(ValueError): verify(manifest,root)


def test_migration_cannot_expand_allowlist(protected_copy):
    root,manifest=protected_copy
    path=root/'revisions/notes/protected-migration.json'
    migration=json.loads(path.read_text())
    migration['files'].append(dict(path='notes/guide.json'))
    path.write_text(json.dumps(migration))
    with pytest.raises(ValueError,match='expands protected scope'): verify(manifest,root)


def test_mor_discipline_migration_cannot_redirect_to_an_immutable_source(protected_copy):
    root,manifest=protected_copy
    path=root/'revisions/notes/protected-migration-mor-discipline.json'
    migration=json.loads(path.read_text())
    migration['path']='notes/guide.json'
    path.write_text(json.dumps(migration))
    # Even rebinding the later migration to tampered parent bytes must not
    # permit the earlier migration to expand its one-file scope.
    later_path=root/'revisions/notes/protected-migration-discipline-cdtm.json'
    later=json.loads(later_path.read_text())
    later['previous_migration_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    later_path.write_text(json.dumps(later))
    with pytest.raises(ValueError,match='MOR discipline migration expands scope|Previous CDTM migration manifest mutated'):
        verify(manifest,root)


@pytest.mark.parametrize('field', ['unit_content_sha256', 'source_evidence_sha256'])
def test_stale_claim_evidence_is_rejected(field):
    from build_full_corpus_review import validate_claim
    claim=json.loads((ROOT/'reports/full-corpus-review/unit3a-claims.json').read_text())['claims'][0]
    units={u['id']:u for c in load_notes(ROOT)['chapters'] for u in c['units']}
    validate_claim(claim,units,ROOT)
    claim=copy.deepcopy(claim); claim[field]='0'*64
    with pytest.raises(ValueError,match='Stale claim'): validate_claim(claim,units,ROOT)


def test_published_unit3a_revision_snapshot_remains_reproducible():
    from notes_revision import IDS
    old=load_notes(ROOT,revision_id=IDS[0])
    now=load_notes(ROOT)
    assert old['revision_provenance']['id']==IDS[0]
    old_units={u['id']:u for c in old['chapters'] for u in c['units']}
    new_units={u['id']:u for c in now['chapters'] for u in c['units']}
    assert old_units['w1-b-8']==new_units['w1-b-8']
    assert old_units['w1-b-9']!=new_units['w1-b-9']
    assert '정식 인수 계약' in new_units['w1-b-9']['body']
    assert '교육일 당일 이전' in new_units['w1-b-10']['body']


@pytest.mark.parametrize('relative',[
    'revisions/notes/2026-10-29-personnel-supervision-training.json',
    'revisions/baselines/complete-notes-unit3a.md',
    'revisions/baselines/complete-notes-unit3b.md',
    'revisions/notes/2026-10-30-mor-presence.json',
    'revisions/baselines/complete-notes-mor-presence.md',
    'revisions/notes/2026-10-30-mor-discipline.json',
    'revisions/baselines/complete-notes-mor-discipline.md',
    'revisions/notes/2026-10-30-discipline-cdtm.json',
    'revisions/notes/2026-10-30-cdtm0512.json',
    'revisions/baselines/complete-notes-discipline-cdtm.md',
])
def test_followup_protection_rejects_source_or_previous_export_changes(protected_copy,relative):
    root,manifest=protected_copy
    with (root/relative).open('ab') as stream: stream.write(b' changed')
    with pytest.raises(ValueError): verify(manifest,root)


def test_visible_quality_status_and_previous59_snapshot_are_current():
    from build_quality_status import output
    path, rendered=output()
    assert path.read_text()==rendered
    assert '2,346' in rendered and '438' in rendered
    snapshot=json.loads((ROOT/'reports/full-corpus-review/unit3b-preservation.json').read_text())
    from build_full_corpus_review import record_hash
    bank=json.loads((ROOT/'practice_expansion/2026-10-28-representative/questions.json').read_text())
    by_id={q['question_id']:q for q in bank['questions']}
    assert len(snapshot['previous_question_record_hashes'])==59
    assert all(record_hash(by_id[qid])==expected for qid,expected in snapshot['previous_question_record_hashes'].items())
    assert snapshot['new_question_ids']==['MA-RW-0065','MA-RW-0067','MA-RW-0068']


def test_mor_discipline_preserves_all_previous62_questions_and_source_records():
    from build_full_corpus_review import record_hash
    snapshot=json.loads((ROOT/'reports/full-corpus-review/mor-discipline-preservation.json').read_text())
    assert snapshot['base_main_commit']=='a9e18a4e3281e1184cb28c29e166ec56ba661426'
    assert snapshot['canonical_independent_audit_created'] is False
    bank=json.loads((ROOT/'practice_expansion/2026-10-28-representative/questions.json').read_text())
    by_id={q['question_id']:q for q in bank['questions']}
    previous=snapshot['previous_question_record_hashes']
    assert len(previous)==62
    assert all(record_hash(by_id[qid])==expected for qid,expected in previous.items())
    previous_sources=snapshot['previous_source_record_hashes']
    assert len(previous_sources)==68
    assert all(record_hash(bank['sources'][sid])==expected for sid,expected in previous_sources.items())
    new_ids=[f'MA-RW-{index:04d}' for index in range(69,77)]
    assert snapshot['new_question_ids']==new_ids
    assert set(previous)|set(new_ids) <= set(by_id)
    for qid in new_ids:
        assert by_id[qid]['verification_status']=='NOT_INDEPENDENTLY_REVIEWED'
        assert by_id[qid]['independent_legal_audit'] is None
        assert by_id[qid]['independent_realism_audit'] is None


def test_discipline_cdtm_preserves_previous70_and_reuses_existing_cdtm_cases():
    from build_full_corpus_review import record_hash
    snapshot=json.loads((ROOT/'reports/full-corpus-review/discipline-cdtm-preservation.json').read_text())
    bank=json.loads((ROOT/'practice_expansion/2026-10-28-representative/questions.json').read_text())
    by_id={q['question_id']:q for q in bank['questions']}
    assert snapshot['base_main_commit']=='c4a05c8bf48ecc333e331b3c267607af6590ac40'
    assert len(snapshot['previous_question_record_hashes'])==70
    assert len(snapshot['previous_source_record_hashes'])==75
    assert all(record_hash(by_id[qid])==value for qid,value in snapshot['previous_question_record_hashes'].items())
    assert all(record_hash(bank['sources'][sid])==value for sid,value in snapshot['previous_source_record_hashes'].items())
    assert set(by_id)==set(snapshot['previous_question_record_hashes'])|set(snapshot['new_question_ids'])
    assert snapshot['new_question_ids']==[f'MA-RW-{i:04d}' for i in range(77,81)]
    reviewed=json.loads((ROOT/'reports/full-corpus-review/cdtm-author-review.json').read_text())['records']
    for qid in ['MA-RW-0025','MA-RW-0026','MA-RW-0027','MA-RW-0028']:
        validate_review(by_id[qid],next(r for r in reviewed if r['question_id']==qid))
    assert not any(int(qid.rsplit('-',1)[1])>80 for qid in by_id)


def test_known_key_defects_and_conditional_reviews_are_not_counted_as_correct():
    outputs=build()
    rows={r['question_id']:r for r in map(json.loads,outputs[ROOT/'reports/full-corpus-review/question-ledger.jsonl'].splitlines())}
    assert rows['MA-EXP-0223']['answer_key_assessment']=='INCORRECT_KEY'
    assert rows['MA-EXP-0224']['answer_key_assessment']=='AMBIGUOUS_KEY'
    assert rows['MA-EXP-0224']['disposition']=='MAJOR_REWRITE'
    assert rows['MA-EXP-0223']['answer_key_crosscheck']['matches'] is False
    assert rows['MA-EXP-0224']['answer_key_crosscheck']['sba_unique'] is False
    for qid in ['MA-EXP-0228',*[f'MA-EXP-{i:04d}' for i in range(233,237)]]:
        assert rows[qid]['legal_review_status']=='AUTHOR_CONDITIONAL_SOURCE_CHECK_NOT_INDEPENDENT'
    selection=json.loads((ROOT/'practice_expansion/2026-10-28-representative/selection.json').read_text())
    notices={qid for n in selection['archive_review_notices'] for qid in n['question_ids']}
    assert notices=={f'MA-EXP-{i:04d}' for i in [221,222,223,224,228,233,234,235,236]}
    assert not notices.intersection(selection['recommended_ids'])
    # Review metadata must not rewrite the preserved incorrect key or old history.
    archive=json.loads((ROOT/'practice_expansion/2026-10-23/candidates/questions.json').read_text())
    old=next(q for q in archive['questions'] if q['question_id']=='MA-EXP-0223')
    assert old['correct_choice_ids']==['A','B','C','D']


def test_editorial_rubric_is_explicit_bounded_and_not_an_automatic_release_score():
    from build_full_corpus_review import QUALITY_CRITERIA, validate_editorial_assessment
    rubric=json.loads((ROOT/'reports/full-corpus-review/editorial-rubric.json').read_text())
    assert set(rubric['criteria'])==QUALITY_CRITERIA
    assert rubric['unassessed_value'] is None and rubric['composite_score']=='NOT_COMPUTED'
    rows=[json.loads(x) for x in build()[ROOT/'reports/full-corpus-review/question-ledger.jsonl'].splitlines()]
    assert sum(r['editorial_quality_assessment'] is not None for r in rows)==80
    assert all(r['editorial_quality_assessment'] is None for r in rows if r['checked_at'] is None)
    assessed=copy.deepcopy(next(r['editorial_quality_assessment'] for r in rows if r['editorial_quality_assessment']))
    assessed['scores']['legal_accuracy']=6
    with pytest.raises(ValueError,match='Invalid editorial score'):
        validate_editorial_assessment(assessed,'test')


def test_new_effective_note_evidence_cannot_be_rehashed_to_an_old_note():
    from build_representative_rewrites import content_hash
    base=ROOT/'practice_expansion/2026-10-28-representative'
    source=json.loads((base/'authoring/09_discipline_procedures.json').read_text())
    authored=source['questions'][0]
    q=copy.deepcopy(next(q for q in json.loads((base/'questions.json').read_text())['questions'] if q['question_id']==authored['question_id']))
    validate_authored_record(q,authored,source)
    q['note_evidence'][0]['body_sha256']='0'*64
    q['content_sha256']=content_hash(q)
    with pytest.raises(ValueError,match='Stale effective note evidence'):
        validate_authored_record(q,authored,source)


def test_new_claim_open_status_is_counted_and_unknown_status_fails_closed():
    from build_full_corpus_review import validate_claim
    claims=json.loads((ROOT/'reports/full-corpus-review/cdtm-claims.json').read_text())['claims']
    open_claim=copy.deepcopy(next(c for c in claims if c['claim_id']=='CDTM-QUAL-002'))
    units={u['id']:u for c in load_notes(ROOT)['chapters'] for u in c['units']}
    validate_claim(open_claim,units)
    assert open_claim['review_status']=='HOLD_FOR_LEGAL_REVIEW'
    progress=json.loads(build()[ROOT/'reports/full-corpus-review/progress.json'])
    assert progress['open_claims']==4 and progress['source_checked_claims']==58
    open_claim['review_status']='OPEN_BUT_NOT_COUNTED'
    with pytest.raises(ValueError,match='Unclassified claim'):
        validate_claim(open_claim,units)


def test_latest_migration_cannot_expand_scope_or_change_parent(protected_copy):
    root,manifest=protected_copy
    path=root/'revisions/notes/protected-migration-discipline-cdtm.json'
    original=json.loads(path.read_text())
    changed=copy.deepcopy(original);changed['path']='notes/guide.json'
    path.write_text(json.dumps(changed))
    with pytest.raises(ValueError,match='Discipline CDTM migration expands scope|Previous CDTM migration manifest mutated'):verify(manifest,root)
    changed=copy.deepcopy(original);changed['previous_migration_sha256']='0'*64
    path.write_text(json.dumps(changed))
    with pytest.raises(ValueError,match='Prior MOR discipline migration changed|Previous CDTM migration manifest mutated'):verify(manifest,root)


def test_permission_research_does_not_admit_unapproved_publisher_question_material():
    from jsonschema import Draft202012Validator
    schema=json.loads((ROOT/'schemas/source_manifest.schema.json').read_text())
    report=json.loads((ROOT/'reports/full-corpus-review/external-source-review.json').read_text())
    assert report['question_content_comparison']=='NOT_RUN_PERMISSION_NOT_VERIFIED'
    assert report['source_signals_created']==0
    for source in report['sources']:
        Draft202012Validator(schema).validate(source)
        assert source['permission_status']=='HOLD'
        assert not any(source[k] for k in ['legal_authority_allowed','question_text_storage_allowed','ai_processing_allowed','public_repo_allowed'])
