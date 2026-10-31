"""Deterministic inventory, not a bulk legal-review certification."""
import argparse
import hashlib
import json
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/full-corpus-review'
REVIEW_FILES = (
    'unit3a-author-review.json', 'unit3b-author-review.json',
    'mor-author-review.json', 'discipline-author-review.json',
    'discipline-procedures-author-review.json', 'cdtm-author-review.json',
    'cdtm05-12-author-review.json',
)
AUTHORING_FILES = (
    '05_personnel_ratios.json', '06_personnel_training.json',
    '07_mor_operations.json', '08_discipline_reporting.json',
    '09_discipline_procedures.json',
)
CLAIM_FILES = (
    'unit3a-claims.json', 'unit3b-claims.json',
    'mor-claims.json', 'discipline-claims.json',
    'discipline-procedures-note-claims.json', 'cdtm-claims.json',
    'cdtm05-12-note-claims.json',
)
QUALITY_CRITERIA = {
    'legal_accuracy', 'state_federal_interaction', 'answer_uniqueness',
    'distractor_quality', 'practice_realism', 'reasoning_depth',
    'explanation_quality', 'citation_accuracy', 'duplication', 'exam_relevance',
}


def validate_editorial_assessment(assessment, qid):
    if assessment is None:
        return
    if set(assessment.get('scores', {})) != QUALITY_CRITERIA:
        raise ValueError('Incomplete editorial rubric: ' + qid)
    if any(type(score) is not int or not 0 <= score <= 5 for score in assessment['scores'].values()):
        raise ValueError('Invalid editorial score: ' + qid)
    if assessment.get('method') != 'INDIVIDUAL_AUTHOR_EDITORIAL_JUDGMENT_NOT_AUTOMATED_LEGAL_CERTIFICATION':
        raise ValueError('Unsupported editorial review claim: ' + qid)
    if not assessment.get('limitation'):
        raise ValueError('Missing editorial review limitations: ' + qid)


def record_hash(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                   separators=(',', ':')).encode()).hexdigest()


def read(path):
    return json.loads((ROOT / path).read_text())


def validate_review(q, review):
    if review['record_sha256'] != record_hash(q):
        raise ValueError('Stale review hash: ' + q['question_id'])
    if set(review['choice_by_choice_findings']) != {c['id'] for c in q['choices']}:
        raise ValueError('Missing choice findings: ' + q['question_id'])
    if any(not finding.get('finding_ko') or not finding.get('exact_authority')
           for finding in review['choice_by_choice_findings'].values()):
        raise ValueError('Empty choice finding or authority: ' + q['question_id'])
    if not review.get('reviewer_provenance') or not review.get('checked_at'):
        raise ValueError('Unattributed review: ' + q['question_id'])
    validate_editorial_assessment(review.get('quality_assessment'), q['question_id'])


def validate_claim(claim, effective_units, root=ROOT):
    if claim['review_status'] not in {'AUTHOR_SOURCE_CHECKED', 'HOLD_FOR_LEGAL_REVIEW'}:
        raise ValueError('Unclassified claim review status: ' + claim['claim_id'])
    if claim['unit_content_sha256'] != effective_units[claim['unit_id']]['body_sha256']:
        raise ValueError('Stale claim unit hash: ' + claim['claim_id'])
    if hashlib.sha256((root/claim['source_evidence']).read_bytes()).hexdigest() != claim['source_evidence_sha256']:
        raise ValueError('Stale claim evidence hash: ' + claim['claim_id'])


def validate_authored_record(question, authored, source, root=ROOT):
    """Do not credit a source review to a stale or differently keyed public item."""
    from build_representative_rewrites import content_hash
    qid = question['question_id']
    validate_editorial_assessment(authored.get('quality_assessment'), qid)
    if content_hash(question) != question.get('content_sha256'):
        raise ValueError('Stale authored content hash: ' + qid)
    expected_choices = [{'id': c['id'], 'text': c['text']} for c in authored['choices']]
    expected_key = [c['id'] for c in authored['choices'] if c['correct']]
    expected_rationales = {c['id']: c['rationale_ko'] for c in authored['choices']}
    expected_authorities = {c['id']: c['authority_refs'] for c in authored['choices']}
    fields = {
        'question_id': authored['question_id'],
        'revision_of': authored['legacy_question_id'],
        'scenario': authored['scenario'],
        'lead_in': authored['lead_in'],
        'stem': authored['scenario'] + '\n\n' + authored['lead_in'],
        'question_type': authored['question_type'],
        'decision_signature': authored['decision_signature'],
        'decision_path': authored['decision_path'],
        'choices': expected_choices,
        'correct_choice_ids': expected_key,
        'authored_at': source['authored_at'],
        'edition': source['edition'],
    }
    for field in ['topic', 'area', 'competency_codes', 'competency_rationale',
                  'exam_outline', 'valid_for_exams_before',
                  'difference_from_legacy', 'comparison_with_existing_quality']:
        fields[field] = authored[field]
    if any(question.get(field) != value for field, value in fields.items()):
        raise ValueError('Stale authored review binding: ' + qid)
    explanation = question.get('explanation', {})
    if (explanation.get('core_reasoning') != authored['core_reasoning_ko'] or
            explanation.get('choice_analysis') != expected_rationales or
            explanation.get('choice_authorities') != expected_authorities):
        raise ValueError('Stale authored choice findings: ' + qid)
    if [e['unit_id'] for e in question.get('note_evidence', [])] != authored['note_unit_ids']:
        raise ValueError('Stale authored note mapping: ' + qid)
    if authored.get('notes_revision'):
        from notes_revision import load_notes
        revised_notes = load_notes(root, revision_id=authored['notes_revision'])
        expected_revision = revised_notes['revision_provenance']
        if question.get('notes_revision') != expected_revision:
            raise ValueError('Stale authored notes revision: ' + qid)
        if authored.get('note_evidence_basis') == 'EFFECTIVE_REVISION':
            units = {u['id']: u for c in revised_notes['chapters'] for u in c['units']}
            for evidence in question['note_evidence']:
                unit = units[evidence['unit_id']]
                if (evidence['body_sha256'] != unit['body_sha256'] or
                        evidence['inherited_note_review_date'] != unit['source_review_date'] or
                        evidence['inherited_flags'] != unit['flags']):
                    raise ValueError('Stale effective note evidence: ' + qid)
    elif question.get('notes_revision') is not None:
        raise ValueError('Unexpected authored notes revision: ' + qid)


def build():
    config = read('site/practice-expansion/publication.json')
    paths = ['practice_expansion/2026-10-23/candidates/questions.json'] + [a['path'] for a in config['additional_banks']]
    baseline = read('reports/full-corpus-review/baseline-inventory.json')
    assert baseline['question_count'] == len(baseline['question_record_hashes']) == 2328
    review_sources = {name: read('reports/full-corpus-review/'+name) for name in REVIEW_FILES}
    review_records = [r for source in review_sources.values() for r in source['records']]
    assert len({r['question_id'] for r in review_records}) == len(review_records)
    reviews = {r['question_id']:r for r in review_records}
    selection = read('practice_expansion/2026-10-28-representative/selection.json')
    replacements = {x['legacy_question_id']: x['replacement_question_id'] for x in selection['replacements']}
    holds = {x['legacy_question_id'] for x in selection['holds']}
    authoring = {}
    author_metadata = {}
    new_author = {}
    for name in AUTHORING_FILES:
        relative = 'practice_expansion/2026-10-28-representative/authoring/'+name
        raw = (ROOT/relative).read_bytes()
        source = json.loads(raw)
        date.fromisoformat(source['authored_at'])
        if source['review_status'] != 'AUTHOR_SOURCE_REVIEW_NOT_INDEPENDENT_AUDIT':
            raise ValueError('Unexpected author review status: ' + relative)
        authoring[name] = source
        for question in source['questions']:
            qid = question['question_id']
            if qid in new_author or qid in reviews:
                raise ValueError('Duplicate review credit: ' + qid)
            new_author[qid] = question
            author_metadata[qid] = dict(
                source=source, source_path=relative,
                source_sha256=hashlib.sha256(raw).hexdigest(),
            )
    unit3a_ids = {q['question_id'] for q in authoring['05_personnel_ratios.json']['questions']}
    unit3b_ids = {q['question_id'] for q in authoring['06_personnel_training.json']['questions']}
    result = []
    all_questions = []
    for collection in paths:
        bank = read(collection)
        for q in bank['questions']:
            all_questions.append(q)
            qid = q['question_id']
            row = dict(question_id=qid, content_version=q.get('content_version', q.get('edition')),
                       content_sha256=record_hash(q), hash_method='sha256-complete-record-canonical-json',
                       collection=collection, family_id=q.get('family_id'), decision_signature=q.get('decision_signature'),
                       notes_unit_ids=[x['unit_id'] for x in q.get('note_evidence', [])],
                       authority_clauses=[], choice_by_choice_findings={}, disposition='UNREVIEWED',
                       legal_review_status='NOT_REVERIFIED_IN_FULL_CORPUS_REVIEW', reviewer_provenance=None,
                       replacement_or_duplicate_of=replacements.get(qid),
                       implementation_status='PRESERVED_BASELINE', publication_status='ARCHIVE_OR_DEFAULT_PRACTICE',
                       checked_at=None, blocker='Individual legal review pending.', next_action='Read this ID and every choice against applicable authority.',
                       answer_key_assessment='NOT_ASSESSED_IN_THIS_REVIEW',
                       answer_key_crosscheck=None,
                       editorial_quality_assessment=None,
                       baseline_member=qid in baseline['question_record_hashes'])
            if row['baseline_member'] and row['content_sha256'] != baseline['question_record_hashes'][qid]:
                raise ValueError('Baseline record changed: ' + qid)
            if qid in replacements:
                row['implementation_status'] = 'LINKED_TO_DISTINCT_REPLACEMENT'
                row['disposition'] = 'ARCHIVED_SUPERSEDED'
            if qid in holds:
                row['implementation_status'] = 'HELD_FROM_DEFAULT_PRESERVED_IN_ARCHIVE'
                row['disposition'] = 'HOLD_FOR_LEGAL_REVIEW'
            if qid in reviews:
                review = reviews[qid]
                validate_review(q, review)
                for k in ['disposition', 'legal_review_status', 'choice_by_choice_findings', 'reviewer_provenance', 'checked_at', 'blocker']:
                    row[k] = review[k]
                row['authority_clauses'] = sorted({v['exact_authority'] for v in review['choice_by_choice_findings'].values()})
                row['answer_key_assessment'] = review.get('original_answer_status', 'NOT_SEPARATELY_CLASSIFIED')
                row['answer_key_crosscheck'] = review.get('answer_key_crosscheck')
                row['editorial_quality_assessment'] = review.get('quality_assessment')
                row['review_evidence'] = {
                    'source_path': 'reports/full-corpus-review/' + next(
                        name for name, source in review_sources.items() if review in source['records']),
                    'review_record_sha256': record_hash(review),
                }
                row['next_action'] = 'Resolve stated blocker; no independent release claim.'
            if qid in new_author:
                a = new_author[qid]
                metadata = author_metadata[qid]
                source = metadata['source']
                validate_authored_record(q, a, source, ROOT)
                row.update(disposition='KEEP', legal_review_status='AUTHOR_SOURCE_CHECKED_NOT_INDEPENDENT',
                           decision_signature=a['decision_signature'], checked_at=source['authored_at'],
                           reviewer_provenance=dict(
                               author_session=source.get('author_session', 'NOT_RECORDED_IN_AUTHORING_SOURCE'),
                               authoring_source=metadata['source_path'],
                               authoring_source_sha256=metadata['source_sha256'],
                               authored_at=source['authored_at'], authoring_edition=source['edition'],
                               peer='NOT_CERTIFIED_BY_THIS_INVENTORY', independent='NOT_RUN'),
                           implementation_status='NEW_DISTINCT_ID', blocker='Independent audit not performed.',
                           answer_key_assessment='AUTHOR_AUTHORED_KEY_NOT_INDEPENDENT',
                           editorial_quality_assessment=a.get('quality_assessment'),
                           next_action='Review frozen current hash independently before canonical release.')
                row['choice_by_choice_findings'] = {c['id']: dict(finding_ko=c['rationale_ko'], authorities=c['authority_refs']) for c in a['choices']}
                row['authority_clauses'] = [r for c in a['choices'] for r in c['authority_refs']]
            row['deployment_status'] = 'CURRENT_BUILD_PUBLICATION_NOT_ASSERTED'
            row['historical_deployment_evidence'] = (
                ['reports/full-corpus-review/unit3a-deployment.json'] if qid in unit3a_ids else []
            )
            row['publication_status'] = ('PRACTICE_CONFIG_DEFAULT' if qid in selection['recommended_ids'] else 'PRACTICE_CONFIG_ARCHIVE')
            result.append(row)
    ids = [r['question_id'] for r in result]
    assert len(ids) == len(set(ids)) == config['published_total']
    assert set(baseline['question_record_hashes']) <= set(ids)
    assert set(reviews) <= set(ids)
    assert set(new_author) <= set(ids)
    by_id = {q['question_id']: q for q in all_questions}
    for qid, authored in new_author.items():
        legacy_id = authored['legacy_question_id']
        if legacy_id not in by_id or by_id[qid]['family_id'] != by_id[legacy_id]['family_id']:
            raise ValueError('Stale authored family mapping: ' + qid)
    notes = read('notes/guide.json')
    claims = [c for name in CLAIM_FILES for c in read('reports/full-corpus-review/'+name)['claims']]
    assert len({c['claim_id'] for c in claims}) == len(claims)
    from notes_revision import load_notes
    effective = {u['id']: u for c in load_notes(ROOT)['chapters'] for u in c['units']}
    for claim in claims:
        validate_claim(claim, effective, ROOT)
    reviewed_units = {c['unit_id'] for c in claims}
    open_units = {c['unit_id'] for c in claims if c['review_status'] == 'HOLD_FOR_LEGAL_REVIEW'}
    units = [dict(unit_id=u['id'], chapter_id=c['id'], baseline_body_sha256=u['body_sha256'],
                  effective_body_sha256=effective[u['id']]['body_sha256'],
                  editorial_update_status='VERSIONED_REVISION_APPLIED' if effective[u['id']].get('content_version') else 'PRESERVED_INPUT',
                  inventory_status='INVENTORIED_NOT_CLAIM_CENSUS',
                  reviewed_claim_ids=[x['claim_id'] for x in claims if x['unit_id'] == u['id']],
                  legal_review_status='PARTIAL_AUTHOR_REVIEW_WITH_OPEN_CLAIM' if u['id'] in open_units else ('PARTIAL_AUTHOR_REVIEW_NOT_CENSUS' if u['id'] in reviewed_units else 'UNREVIEWED'),
                  atomic_claim_census_complete=False) for c in notes['chapters'] for u in c['units']]
    canonical = []
    for path in sorted((ROOT/'data/questions').glob('*.json')):
        q = json.loads(path.read_text())
        canonical.append(dict(question_id=q['question_id'], path=str(path.relative_to(ROOT)), content_sha256=record_hash(q),
                              inventory_status='INVENTORIED_NOT_REAUDITED', existing_lifecycle_status=q.get('lifecycle_status'),
                              existing_audit_evidence_preserved=True))
    coverage = dict(outline='MPJE-MA-PRE2027', mapping_status='INVENTORY_PLUS_PARTIAL_CLAIM_REVIEWS_NOT_FULL_DECISION_PATH_COVERAGE',
                    units=units, reviewed_claims=claims, inferred_family_passes=0)
    progress = dict(baseline_commit=baseline['base_commit'], baseline_questions=2328, new_questions=len(new_author),
                    current_questions=len(result), original_2176_inventory=sum(r['question_id'].startswith(('MA-EXP-', 'MA-CASE-')) for r in result),
                    prior_MA_REV_inventory=96, current_MA_RW_inventory=len(read(paths[-1])['questions']),
                    representative_355_implementation=selection['stats'],
                    question_ids_read_this_session=len(reviews)+len(new_author),
                    review_count_scope='CUMULATIVE_EXPLICIT_ID_RECORDS_NOT_ONE_SESSION',
                    question_ids_with_review_records=len(reviews)+len(new_author),
                    unit3b_question_ids_reviewed=len(review_sources['unit3b-author-review.json']['records'])+len(unit3b_ids),
                    author_review_records_by_file={name:len(source['records']) for name,source in review_sources.items()},
                    new_author_review_records_by_file={name:len(source['questions']) for name,source in authoring.items()},
                    legal_review_counts=dict(Counter(r['legal_review_status'] for r in result)),
                    answer_key_assessment_counts=dict(Counter(r['answer_key_assessment'] for r in result)),
                    editorial_rubric_assessed_ids=sum(r['editorial_quality_assessment'] is not None for r in result),
                    editorial_rubric_is_release_certificate=False,
                    canonical_inventory=len(canonical), canonical_reaudits_this_session=0,
                    notes_chapters=len(notes['chapters']), notes_units=len(units),
                    notes_units_with_partial_claim_review=len(reviewed_units),
                    notes_units_with_versioned_edits=sum(u['editorial_update_status']=='VERSIONED_REVISION_APPLIED' for u in units),
                    notes_units_with_complete_atomic_claim_census=0,
                    reviewed_claims=len(claims), source_checked_claims=sum(x['review_status']=='AUTHOR_SOURCE_CHECKED' for x in claims),
                    open_claims=sum(x['review_status']=='HOLD_FOR_LEGAL_REVIEW' for x in claims), atomic_claim_census_complete=False,
                    inventory_is_legal_review=False,
                    same_team_peer_this_session='NOT_CERTIFIED_BY_THIS_INVENTORY',
                    canonical_independent_audit_this_session='NOT_RUN',
                    deployment_status='CURRENT_BUILD_PUBLICATION_NOT_ASSERTED')
    inventory = dict(
        basis='Actual current source records; collection/family/topic/notes/review are different dimensions.',
        collections=[dict(path=path, questions=len(read(path)['questions']),
                          family_ids=len({q['family_id'] for q in read(path)['questions']}),
                          topic_labels=len({q['topic'] for q in read(path)['questions']}),
                          question_types=dict(Counter(q['question_type'] for q in read(path)['questions'])))
                     for path in paths],
        public_practice_questions=len(result), default_selected_questions=len(selection['recommended_ids']),
        unique_family_ids=len({q['family_id'] for q in all_questions}),
        family_ids_are_independent_legal_principles=False,
        original_paired_case_families=len({q['family_id'] for q in read(paths[0])['questions']}),
        additional_conditional_models=len({q['family_id'] for q in read(paths[1])['questions']}),
        independent_case_or_legal_principle_census='NOT_PERFORMED',
        notes_topics=len(notes['chapters']), notes_sections=len(units),
        canonical_questions=len(canonical),
        canonical_statuses=dict(Counter(q['existing_lifecycle_status'] for q in canonical)),
        canonical_and_public_practice_counts_are_separate=True,
        historical_counts={
            '2176': 'Original 1024 plus conditional-model bank 1152; excludes later MA-REV/MA-RW.',
            '2328': '2176 original plus96 MA-REV plus56 MA-RW at baseline9f3fed1.',
            '226': 'Historical canonical count; not the current canonical tree or a public-practice total.',
        },
        automatic_inventory_is_legal_review=False,
    )
    from build_representative_rewrites import pattern_metrics
    comparison = dict(method='Same stored question objects, same pattern_metrics function; baseline main IDs fixed.',
                      before_main_sha=baseline['base_commit'],
                      before_archive=pattern_metrics([by_id[i] for i in baseline['question_record_hashes']]),
                      after_archive=pattern_metrics(all_questions),
                      before_default=pattern_metrics([by_id[i] for i in baseline['recommended_ids']]),
                      after_default=pattern_metrics([by_id[i] for i in selection['recommended_ids']]),
                      semantic_duplicate_verdict='NOT_INFERRED_FROM_PATTERNS')
    def pretty(x): return json.dumps(x, ensure_ascii=False, indent=2)+'\n'
    def jsonl(xs): return ''.join(json.dumps(x, ensure_ascii=False, separators=(',', ':'))+'\n' for x in xs)
    return {OUT/'inventory-definitions.json': pretty(inventory), OUT/'pattern-comparison.json': pretty(comparison), OUT/'question-ledger.jsonl': jsonl(result), OUT/'notes-unit-ledger.jsonl': jsonl(units),
            OUT/'notes-claim-ledger.jsonl': jsonl(claims), OUT/'canonical-inventory.json': pretty(canonical),
            OUT/'coverage-matrix.json': pretty(coverage), OUT/'progress.json': pretty(progress)}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--check', action='store_true'); args=parser.parse_args()
    for path, text in build().items():
        if args.check:
            if not path.exists() or path.read_text()!=text: raise SystemExit('Stale corpus inventory: '+str(path))
        else: path.write_text(text)
    print('Full corpus inventory checked; inventory does not confer legal verification.')
