"""Deterministic inventory, not a bulk legal-review certification."""
import argparse
import copy
import gzip
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
    'cdtm05-12-author-review.json', 'cdtm-vax-author-review.json',
    'vax05-14-author-review.json',
    'vax15-pub04-author-review.json',
    'pub05-09-author-review.json', 'pub10-14-author-review.json',
    'wave2-1-author-review.json', 'wave2-2-author-review.json',
    'wave2-3-author-review.json', 'wave2-4-author-review.json',
    'wave3-1-author-review.json', 'wave3-2-author-review.json',
    'wave3-3-author-review.json', 'wave3-4-author-review.json',
    'wave4-1-author-review.json', 'wave4-2-author-review.json',
    'wave4-3-author-review.json', 'wave4-4-author-review.json',
    'wave5-1-author-review.json', 'wave5-2-author-review.json',
    'wave5-3-author-review.json', 'wave5-4-author-review.json',
    'wave6-1-author-review.json', 'wave6-2-author-review.json',
    'wave6-3-author-review.json', 'wave6-4-author-review.json',
    'wave7-1-author-review.json', 'wave7-2-author-review.json',
    'wave7-3-author-review.json', 'wave7-4-author-review.json',
    'wave8-1-author-review.json', 'wave8-2-author-review.json',
    'wave8-3-author-review.json', 'wave8-4-author-review.json',
    'wave9-1-author-review.json', 'wave9-2-author-review.json',
    'wave9-3-author-review.json', 'wave9-4-author-review.json',
    'wave10-1-author-review.json', 'wave10-2-author-review.json',
    'wave10-3-author-review.json', 'wave10-4-author-review.json',
    'wave11-1-author-review.json', 'wave11-2-author-review.json',
    'wave11-3-author-review.json', 'wave11-4-author-review.json',
    'wave12-1-author-review.json', 'wave12-2-author-review.json',
    'wave12-3-author-review.json', 'wave12-4-author-review.json',
    'wave13-1-author-review.json', 'wave13-2-author-review.json',
    'wave13-3-author-review.json', 'wave13-4-author-review.json',
    'wave14-1-author-review.json', 'wave14-2-author-review.json',
    'wave14-3-author-review.json',
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
    'cdtm05-12-note-claims.json', 'cdtm-vax-note-claims.json',
)
QUALITY_CRITERIA = {
    'legal_accuracy', 'state_federal_interaction', 'answer_uniqueness',
    'distractor_quality', 'practice_realism', 'reasoning_depth',
    'explanation_quality', 'citation_accuracy', 'duplication', 'exam_relevance',
}
ACTIONABLE_AUTHOR_DISPOSITIONS = {
    'MINOR_EDIT', 'MAJOR_REWRITE', 'HOLD', 'HOLD_FOR_LEGAL_REVIEW',
    'DELETE', 'REPLACE',
    'HOLD_SOURCE_RELATIONSHIP',
}


def validate_default_review_safety(default_ids, reviews, independent_records):
    """Known current-content failures must have explicit default containment."""
    defaults = set(default_ids)
    for qid, review in reviews.items():
        if qid in defaults and review['disposition'] in ACTIONABLE_AUTHOR_DISPOSITIONS:
            raise ValueError('Uncontained author finding in default practice: ' + qid)
    for review in independent_records:
        if review['question_id'] not in defaults:
            continue
        legal = review['legal_review']
        realism = review['realism_review']
        if (legal.get('verdict') != 'KEEP' or
                legal.get('existing_answer_correct') != 'YES' or
                realism.get('verdict') != 'PASS'):
            raise ValueError('Uncontained independent finding in default practice: ' + review['question_id'])


def validate_independent_archive_safety(selection, independent_records):
    """A retained negative finding needs a visible, source-bound archive warning."""
    visible = {qid for notice in selection['archive_review_notices']
               for qid in notice['question_ids']}
    visible.update(hold['legacy_question_id'] for hold in selection['holds'])
    visible.update(hold['question_id'] for hold in selection.get('safety_holds', []))
    for review in independent_records:
        legal, realism = review['legal_review'], review['realism_review']
        negative = (legal.get('verdict') in {
                        'MINOR_EDIT', 'MAJOR_REWRITE', 'HOLD', 'DELETE', 'REPLACE'} or
                    legal.get('existing_answer_correct') in {'NO', 'AMBIGUOUS', 'NOT_ASSESSED'} or
                    realism.get('verdict') in {'FAIL', 'MINOR_EDIT', 'MAJOR_REWRITE'})
        if negative and review['question_id'] not in visible:
            raise ValueError('Unsurfaced independent archive finding: ' + review['question_id'])


def apply_current_id_independent_state(row, audit_row, source_binding):
    """Describe the three native candidates' validated assessment, without credit.

    Frozen source_author_review_binding remains historical draft/engineering
    context. This separate state uses only the committed consumer's binding.
    """
    if (row.get('question_id') not in {'MA-RW-0081', 'MA-RW-0082', 'MA-RW-0083'} or
            row.get('checked_at_scope') != 'FORMAL_NATIVE_CURRENT_ID_AUTHOR_REVIEW' or
            row.get('current_id_author_review_required') is not False or source_binding is None):
        return
    author_job=row.get('native_author_review_job_id')
    if (not author_job or row.get('review_evidence', {}).get('native_author_job_id') != author_job):
        raise ValueError('Unbound native current-ID author review')
    if (source_binding.get('question_id') != row['question_id'] or
            audit_row['question_id'] != row['question_id'] or
            source_binding.get('record_sha256') != row['content_sha256'] or
            audit_row['record_sha256'] != row['content_sha256'] or
            source_binding.get('review_record_sha256') != record_hash(audit_row) or
            row.get('independent_legacy_legal_assessment') != audit_row['legal_review'] or
            row.get('independent_legacy_realism_assessment') != audit_row['realism_review']):
        raise ValueError('Stale current-ID independent review binding')
    path=Path(source_binding.get('source_path', ''))
    if (path.is_absolute() or '..' in path.parts or
            not str(path).startswith('reports/full-corpus-review/') or
            not source_binding.get('source_sha256') or not source_binding.get('job_id') or
            source_binding.get('actor_provenance', {}).get('actor_id') in
            row.get('known_author_editor_actor_ids', [])):
        raise ValueError('Invalid current-ID independent source provenance')
    legal=audit_row['legal_review']; realism=audit_row['realism_review']
    passed=(legal.get('verdict')=='KEEP' and legal.get('existing_answer_correct')=='YES' and
            realism.get('verdict')=='PASS')
    incomplete=(legal.get('existing_answer_correct')=='NOT_ASSESSED' or
                realism.get('verdict')=='NOT_ASSESSED')
    row['current_id_independent_review_status']=(
        'SOURCE_BOUND_PASS' if passed else 'SOURCE_BOUND_INCOMPLETE' if incomplete else 'SOURCE_BOUND_NOT_PASSED')
    row['current_id_independent_review_source']=copy.deepcopy(source_binding)
    if passed and row['disposition']=='KEEP':
        row['next_action']='Current-ID independent review passed; root QA, publication and default-selection review remain pending. Candidate remains archive-only.'
    else:
        row['next_action']=(row.get('blocker') or legal.get('blocker') or
                            audit_row.get('required_next_action_ko') or
                            realism.get('finding_ko') or legal.get('finding_ko') or
                            'Complete the unresolved current-ID independent assessment before root release review.')


def apply_independent_legacy_review(row, audit_row, *, source_binding=None):
    """A supported key does not erase an unresolved law or explanation finding."""
    previous=row['disposition']; previous_blocker=row['blocker']
    legal=audit_row['legal_review']; realism=audit_row['realism_review']
    row['author_disposition']=previous
    row['independent_legacy_legal_assessment']=legal
    row['independent_legacy_realism_assessment']=realism
    row['independent_legacy_is_canonical_release_evidence']=False
    key=legal['existing_answer_correct']; verdict=legal.get('verdict')
    blocker=None
    strong={'HOLD','HOLD_FOR_LEGAL_REVIEW','HOLD_SOURCE_RELATIONSHIP','DELETE','REPLACE'}
    if key in {'AMBIGUOUS','NOT_ASSESSED','NO'}:
        row['author_answer_key_assessment']=row['answer_key_assessment']
        row['answer_key_assessment']='INDEPENDENT_LEGACY_'+key
        disposition='HOLD_FOR_LEGAL_REVIEW'
        blocker=legal.get('blocker') or legal.get('finding_ko')
    elif verdict not in {'KEEP','MINOR_EDIT','MAJOR_REWRITE','DELETE'}:
        disposition='HOLD_FOR_LEGAL_REVIEW'
        blocker=legal.get('blocker') or legal.get('finding_ko')
    elif previous in strong:
        disposition=previous
    elif verdict=='DELETE':
        disposition='DELETE'; blocker=legal.get('blocker') or legal.get('finding_ko')
    elif realism.get('verdict')=='FAIL':
        disposition='MAJOR_REWRITE'; blocker=audit_row['required_next_action_ko']
    elif realism.get('verdict')!='PASS':
        disposition='HOLD'; blocker=realism.get('finding_ko') or audit_row['required_next_action_ko']
    elif verdict in {'MINOR_EDIT','MAJOR_REWRITE'}:
        disposition='MAJOR_REWRITE' if previous=='MAJOR_REWRITE' else verdict
        blocker=legal.get('blocker') or legal.get('finding_ko')
    else:
        disposition=previous
    row['disposition']=disposition
    if blocker:
        row['author_review_blocker']=previous_blocker
        row['blocker']=blocker
    apply_current_id_independent_state(row, audit_row, source_binding)


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


def validate_independent_source_bytes(authority, root=ROOT):
    """Verify captured bytes, including failed attempts; this grants no law credit."""
    pairs=[]
    for path_key,sha_key in [('evidence_path','evidence_sha256'),('raw_path','raw_sha256')]:
        # Historical sources may retain extracted text/memo and only the SHA
        # of an unretained original payload. Do not claim to verify that raw
        # payload; every actual retained path still requires its matching SHA.
        if path_key in authority or (path_key=='evidence_path' and sha_key in authority):
            path=authority.get(path_key);sha=authority.get(sha_key)
            if not isinstance(path,str) or not isinstance(sha,str):
                raise ValueError('Incomplete independent source evidence binding')
            relative=Path(path)
            if (path_key=='raw_path' and relative.is_absolute() and pairs and
                    authority.get('public_raw_redistribution') is False and
                    'memo' in authority.get('public_evidence_mode','').lower()):
                # A declared private copyrighted original is not a repository
                # payload. Verify the retained memo, never claim the raw read.
                continue
            if relative.is_absolute() or '..' in relative.parts:
                raise ValueError('Unsafe independent source evidence path')
            pairs.append((relative,sha))
    if not pairs:
        raise ValueError('Missing independent source evidence binding')
    for relative,sha in pairs:
        if hashlib.sha256((root/relative).read_bytes()).hexdigest()!=sha:
            raise ValueError('Stale independent source evidence')


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


def verified_nonlegal_census(census, unit, effective, root=ROOT):
    """A reviewed method-only body may have zero legal claims, never a legal PASS.

    This exact body was independently classified after the author's zero-claim
    census failed the former nonempty-only validator. Other units and changed
    bodies still require their substantive claims to be enumerated.
    """
    uid = unit['unit_id']
    body_hash = '7e0131b82b6ac6ee0936fdf4a368fc6e494a2ab6712be43882fd851b47651e29'
    if uid != 'w6-b-16' or unit['unit_content_sha256'] != body_hash:
        return False
    evidence = census.get('editorial_nonlegal_inventory', {}).get(uid, {})
    if not (unit.get('nonlegal_inventory_only') is True and unit['claim_count'] == 0 and
            unit.get('legal_verification_status') == 'NOT_APPLICABLE_EDITORIAL_METHOD_NO_LEGAL_CLAIMS' and
            unit.get('independent_completeness_status') == 'PENDING' and
            evidence.get('body_read_completely') is True and evidence.get('legal_claim_count') == 0 and
            evidence.get('classification') == 'EDITORIAL_EVIDENCE_MANAGEMENT_NOT_SUBSTANTIVE_LEGAL_RULE' and
            evidence.get('census_completion_basis_ko') and
            {r.get('item') for r in evidence.get('items', [])} == {'해석 차이','접근 미완료','미래 시행','범위 경계'} and
            all(r.get('finding_ko') for r in evidence.get('items', []))):
        return False
    author_path = root/'reports/full-corpus-review/note-wave16-census.json'
    raw = author_path.read_bytes()
    if (hashlib.sha256(raw).hexdigest() != '4746d3764f54927444cb8994a0b59f277f1c83f6c02d62d68fb34661d2f4ba9b' or
            record_hash(json.loads(raw)) != record_hash(census)):
        raise ValueError('Nonlegal census author evidence changed')
    path = root/'reports/full-corpus-review/nonlegal-w6-b-16-independent-classification.json'
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != '273fab0250b87627af94266d71dae30d898e7d8a702f08cdffe48bb93960b2f7':
        raise ValueError('Nonlegal census independent classification changed')
    review = json.loads(raw)
    paragraphs = effective['body'].split('\n\n')
    if not (review['unit_id'] == uid and review['source_unit_body_sha256'] == body_hash and
            review['independent_of_authors'] is True and review['canonical_audit'] is False and
            review['canonical_release_credit'] == review['question_audit_credit'] == 0 and
            review['classification'] == 'NOT_APPLICABLE_NONLEGAL' and
            review['substantive_legal_atomic_claim_count'] == 0 and not review['omissions_found'] and
            [r['original_paragraph'] for r in review['paragraph_reviews']] == paragraphs and
            all(r['classification'] == 'NOT_APPLICABLE_NONLEGAL' and
                r['substantive_legal_atomic_claim_count'] == 0 for r in review['paragraph_reviews'])):
        raise ValueError('Nonlegal census classification scope changed')
    for relative, expected in review['read_docs_sha256'].items():
        if hashlib.sha256((root/relative).read_bytes()).hexdigest() != expected:
            raise ValueError('Nonlegal census methodology context changed')
    snapshot = root/unit['body_snapshot_path']
    raw = snapshot.read_bytes()
    if (hashlib.sha256(raw).hexdigest() != unit['body_snapshot_sha256'] or
            gzip.decompress(raw).decode() != effective['body']):
        raise ValueError('Nonlegal census body snapshot changed')
    return True


def validate_note_census(census, effective, by_id, root=ROOT):
    """Enumeration is author evidence, not independent legal certification."""
    claims = census['claims']
    if len({c['claim_id'] for c in claims}) != len(claims):
        raise ValueError('Duplicate census claim')
    for source in census['sources'].values():
        if not source['official_url'].startswith('https://'):
            raise ValueError('Non-HTTPS census source')
        if hashlib.sha256((root/source['source_evidence']).read_bytes()).hexdigest() != source['source_evidence_sha256']:
            raise ValueError('Stale census evidence')
    units = {}
    for unit in census['units']:
        uid = unit['unit_id']
        if uid in units or uid not in effective:
            raise ValueError('Duplicate or unknown census unit')
        if unit['unit_content_sha256'] != hashlib.sha256(effective[uid]['body'].encode()).hexdigest():
            raise ValueError('Stale census unit: ' + uid)
        entries = [c for c in claims if c['unit_id'] == uid]
        if (len(entries) != unit['claim_count'] or not unit['body_read_completely'] or
                (not entries and not verified_nonlegal_census(census, unit, effective[uid], root))):
            raise ValueError('Incomplete census enumeration: ' + uid)
        if unit['census_status'] == 'COMPLETE_AUTHOR_ENUMERATION_PENDING_INDEPENDENT_COMPLETENESS_CHECK':
            if any(c.get('is_complete_atomic_enumeration_evidence') is False or
                   c.get('record_granularity') == 'PARTIAL_COMPOSITE_CLAUSE' for c in entries):
                raise ValueError('Partial clauses cannot certify complete census: ' + uid)
        for claim in entries:
            if claim['unit_content_sha256'] != unit['unit_content_sha256']:
                raise ValueError('Stale atomic claim')
            if claim['review_status'] not in {'AUTHOR_SOURCE_CHECKED', 'SOURCE_BLOCKED'}:
                raise ValueError('Unsupported census status')
            if (not claim['statement_ko'] or (claim['review_status'] == 'AUTHOR_SOURCE_CHECKED' and
                    (not claim['authority_clauses'] or claim['source_id'] not in census['sources']))):
                raise ValueError('Unattributed atomic claim')
            if not set(claim['related_question_ids']) <= set(by_id):
                raise ValueError('Unknown related question')
            if claim['review_status'] == 'SOURCE_BLOCKED' and not claim['blocker']:
                raise ValueError('Missing claim blocker')
        units[uid] = unit
    if not {c['unit_id'] for c in claims} <= set(units):
        raise ValueError('Orphan census claim')
    return units


def compose_note_censuses(specs, effective, by_id, root=ROOT):
    """Validate historical snapshots, then require explicit per-unit supersedence.

    A changed note must have a current-body census; old review credit never follows
    an edited body. Old reports and revision snapshots remain verifiable history.
    """
    from notes_revision import load_notes
    selected = {}
    for spec in specs:
        path = root / spec['path']
        census = json.loads(path.read_text())
        if 'body_correction_record' in spec or 'body_correction_history' in spec:
            from notes_body_reassessment import census_snapshot
            snapshot = census_snapshot(root,spec,{'chapters':[{'units':list(effective.values())}]})
        else:
            snapshot = {u['id']: u for c in load_notes(root, revision_id=spec['notes_revision'])['chapters']
                        for u in c['units']}
        source_units = validate_note_census(census, snapshot, by_id, root)
        overlap = set(source_units) & set(selected)
        if set(spec.get('supersedes', {})) != overlap:
            raise ValueError('Undeclared census supersedence')
        for uid, unit in source_units.items():
            if uid in overlap and spec['supersedes'][uid] != selected[uid]['source']:
                raise ValueError('Wrong census supersedence parent: ' + uid)
            selected[uid] = dict(unit=unit, source=spec['path'],
                                 notes_revision=spec['notes_revision'],
                                 claims=[c for c in census['claims'] if c['unit_id'] == uid])
    for uid, entry in selected.items():
        if entry['unit']['unit_content_sha256'] != hashlib.sha256(effective[uid]['body'].encode()).hexdigest():
            raise ValueError('Current note requires a new census: ' + uid)
    units = {uid: dict(entry['unit'], census_source=entry['source'],
                        notes_revision=entry['notes_revision']) for uid, entry in selected.items()}
    claims = [claim for entry in selected.values() for claim in entry['claims']]
    return units, claims


CITATION_ERRATA_FILES = ('wave6-1-citation-errata.json', 'wave10-1-citation-errata.json')


def apply_citation_errata(rows, root=ROOT):
    """Correct only bound citation leaves; never rewrite reports or answer history."""
    import copy
    by_id = {r['question_id']: r for r in rows}
    for name in CITATION_ERRATA_FILES:
        path = root/'reports/full-corpus-review'/name
        raw = path.read_bytes()
        correction = json.loads(raw)
        if correction['legal_truth_changed'] or correction['answer_keys_changed']:
            raise ValueError('Citation errata cannot change legal truth or answer keys')
        original_raw = (root/correction['original_report_path']).read_bytes()
        if hashlib.sha256(original_raw).hexdigest() != correction['original_report_sha256']:
            raise ValueError('Stale citation errata evidence')
        for authority in [correction['official_authority']] + correction.get('supplemental_official_authorities', []):
            if hashlib.sha256((root/authority['source_evidence_path']).read_bytes()).hexdigest() != authority['source_evidence_sha256']:
                raise ValueError('Stale citation errata evidence')
            if authority.get('retrieval_metadata_path') and hashlib.sha256((root/authority['retrieval_metadata_path']).read_bytes()).hexdigest() != authority['retrieval_metadata_sha256']:
                raise ValueError('Stale citation retrieval metadata')
        original_records = json.loads(original_raw)['records']
        for patch in correction['errata']:
            row = by_id[patch['question_id']]
            choice = patch['choice_id']
            segments = patch.get('field_path_segments', ['choice_by_choice_findings', choice, patch['field']])
            top = segments == ['choice_by_choice_findings', choice, 'exact_authority']
            nested = (len(segments) == 5 and segments[:3] == ['choice_by_choice_findings', choice, 'authorities']
                      and type(segments[3]) is int and segments[3] >= 0 and segments[4] == 'exact_section')
            if (not (top or nested) or patch['field'] != segments[-1] or
                    patch['field_path'] != '.'.join(map(str,segments)) or
                    row['content_sha256'] != patch['question_record_sha256'] or
                    row.get('review_evidence',{}).get('source_path') != correction['original_report_path']):
                raise ValueError('Citation errata scope or question binding changed')
            positions = [i for i,r in enumerate(original_records) if r['question_id'] == patch['question_id']]
            if len(positions) != 1 or original_records[positions[0]]['record_sha256'] != patch['question_record_sha256']:
                raise ValueError('Citation original record binding changed')
            pointer = '/records/'+str(positions[0])+'/'+('/'.join(map(str,segments)))
            if patch.get('report_json_pointer',pointer) != pointer:
                raise ValueError('Citation original field pointer changed')
            row['choice_by_choice_findings'] = copy.deepcopy(row['choice_by_choice_findings'])
            target = row['choice_by_choice_findings'][choice]
            original_target = original_records[positions[0]]['choice_by_choice_findings'][choice]
            if nested:
                target = target['authorities'][segments[3]]
                original_target = original_target['authorities'][segments[3]]
            field = segments[-1]
            if target[field] != patch['original_field_value'] or original_target[field] != patch['original_field_value']:
                raise ValueError('Citation errata precondition changed')
            target[field] = patch['corrected_field_value']
            row['authority_clauses'] = sorted({v['exact_authority'] for v in row['choice_by_choice_findings'].values()})
            row['review_evidence'].setdefault('citation_errata', []).append(dict(
                path=str(path.relative_to(root)), sha256=hashlib.sha256(raw).hexdigest(),
                field_path=patch['field_path'], previous=patch['original_field_value'], current=patch['corrected_field_value']))


def apply_case0217_reconciliation(rows, questions, root=ROOT):
    """Additional primary research updates one author assessment, not release."""
    import copy
    path = root/'reports/full-corpus-review/case0217-source-reconciliation.json'
    raw = path.read_bytes()
    update = json.loads(raw)
    qid = update['question_id']
    question = questions[qid]
    row = next(r for r in rows if r['question_id'] == qid)
    binding = update['prior_review_binding']
    original_raw = (root/binding['report_path']).read_bytes()
    original = next(r for r in json.loads(original_raw)['records'] if r['question_id'] == qid)
    if (qid != 'MA-CASE-0217' or update['record_sha256'] != record_hash(question) or
            record_hash(original) != binding['prior_record_sha256'] or
            hashlib.sha256(original_raw).hexdigest() != binding['report_sha256']):
        raise ValueError('Source reconciliation binding changed')
    findings = update['choice_by_choice_findings']
    if set(findings) != {c['id'] for c in question['choices']}:
        raise ValueError('Reconciliation choice coverage changed')
    for choice in question['choices']:
        finding = findings[choice['id']]
        if (finding['original_option_text'] != choice['text'] or
                hashlib.sha256((root/finding['source_evidence']).read_bytes()).hexdigest() != finding['source_evidence_sha256']):
            raise ValueError('Reconciliation choice or primary evidence changed')
    expected = [c['id'] for c in question['choices'] if findings[c['id']]['statement_supported']]
    if expected != question['correct_choice_ids'] or update['reviewer_provenance']['independent']:
        raise ValueError('Reconciliation is not matching author evidence')
    row['historical_author_assessment'] = dict(answer_key_assessment=row['answer_key_assessment'],
        legal_review_status=row['legal_review_status'], blocker=row['blocker'],
        reviewer_provenance=copy.deepcopy(row['reviewer_provenance']), review_evidence=copy.deepcopy(row['review_evidence']))
    row.update(legal_review_status='AUTHOR_SOURCE_CHECKED_NOT_INDEPENDENT',
        reviewer_provenance=update['reviewer_provenance'],
        answer_key_assessment='CORRECT', answer_key_crosscheck=update['answer_key_crosscheck'],
        choice_by_choice_findings=copy.deepcopy(findings),
        authority_clauses=sorted({f['exact_authority'] for f in findings.values()}),
        disposition='MAJOR_REWRITE', blocker=' '.join(update['remaining_blockers']))
    row['review_evidence']['source_reconciliation'] = dict(path=str(path.relative_to(root)),
        sha256=hashlib.sha256(raw).hexdigest(), status=update['source_blocker_resolution']['status'],
        scope='ONE_EXACT_ORIGINAL_HASH_AUTHOR_RESEARCH_ONLY_NOT_RELEASE')


def build():
    config = read('site/practice-expansion/publication.json')
    paths = ['practice_expansion/2026-10-23/candidates/questions.json'] + [a['path'] for a in config['additional_banks']]
    baseline = read('reports/full-corpus-review/baseline-inventory.json')
    assert baseline['question_count'] == len(baseline['question_record_hashes']) == 2328
    review_sources = {name: read('reports/full-corpus-review/'+name) for name in REVIEW_FILES}
    from remediation_author_reviews import load_sources
    review_sources.update(load_sources(ROOT, REVIEW_FILES))
    review_records = [r for source in review_sources.values() for r in source['records']]
    assert len({r['question_id'] for r in review_records}) == len(review_records)
    reviews = {r['question_id']:r for r in review_records}
    selection = read('practice_expansion/2026-10-28-representative/selection.json')
    replacements = {x['legacy_question_id']: x['replacement_question_id'] for x in selection['replacements']}
    holds = {x['legacy_question_id']:x for x in selection['holds']}
    safety_holds = {x['question_id']: x for x in selection.get('safety_holds', [])}
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
            if qid in safety_holds:
                row['implementation_status'] = 'HELD_FROM_DEFAULT_PRESERVED_IN_ARCHIVE'
                row['default_safety_hold'] = safety_holds[qid]
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
            if q.get('archive_only_candidate'):
                from build_sata_remediation_candidates import bind_candidate_inventory_row
                bind_candidate_inventory_row(row, q, ROOT)
            row['deployment_status'] = 'CURRENT_BUILD_PUBLICATION_NOT_ASSERTED'
            row['historical_deployment_evidence'] = (
                ['reports/full-corpus-review/unit3a-deployment.json'] if qid in unit3a_ids else []
            )
            row['publication_status'] = ('PRACTICE_CONFIG_DEFAULT' if qid in selection['recommended_ids'] else 'PRACTICE_CONFIG_ARCHIVE')
            result.append(row)
    apply_citation_errata(result)
    apply_case0217_reconciliation(result, {q['question_id']: q for q in all_questions})
    from legacy_independent_metadata import integrated_sources
    independent_source_bindings = {}
    independent_sources = [read('reports/full-corpus-review/' + name) for name in (
        'pub05-14-independent-review.json', 'wave2-independent-review.json',
        'wave5-independent-review.json')]+integrated_sources(ROOT,source_bindings=independent_source_bindings)
    independent_records = [r for source in independent_sources for r in source['records']]
    if (any(not source['independent_of_authors'] for source in independent_sources) or
            len({r['question_id'] for r in independent_records}) != len(independent_records)):
        raise ValueError('Invalid independent legacy provenance')
    public_by_id = {q['question_id']: q for q in all_questions}
    for audit_row in independent_records:
        if audit_row['record_sha256'] != record_hash(public_by_id[audit_row['question_id']]):
            raise ValueError('Stale independent legacy review')
    from independent_public_style_bindings import validation_sources
    for source in independent_sources:
        for authority in validation_sources(ROOT,source,source_bindings=independent_source_bindings):
            validate_independent_source_bytes(authority,ROOT)
    from procedural_secondary_metadata import load_metadata as load_procedural_secondary
    from phase11_secondary_metadata import load_metadata as load_phase11_secondary
    from phase11_context38_metadata import (load_metadata as load_context38_secondary,
        combine_metadata, validate_default_safety as validate_context_default_safety)
    secondary_collections = {r['question_id']:r['collection'] for r in result}
    procedural_secondary = load_procedural_secondary(ROOT,independent_records,public_by_id,secondary_collections)
    phase11_secondary = load_phase11_secondary(ROOT,independent_records,public_by_id,secondary_collections)
    context38_secondary = load_context38_secondary(ROOT,independent_records,public_by_id,secondary_collections)
    from realism_completion_metadata import load_metadata as load_realism_completion, apply_metadata as apply_realism_completion
    realism_completion_bindings = {}
    realism_completion = load_realism_completion(ROOT,independent_records,public_by_id,source_bindings=realism_completion_bindings)
    realism_completion_legal = {'assessments':realism_completion['legal_assessments'],'records':realism_completion['legal_records']}
    from remaining9_procedural_metadata import load_metadata as load_remaining9_secondary
    remaining9_bindings = {}
    remaining9_secondary = load_remaining9_secondary(ROOT,independent_records,public_by_id,secondary_collections,
                                                    source_bindings=remaining9_bindings)
    from source3_recovered_legal_metadata import load_metadata as load_source3_secondary
    source3_bindings = {}
    source3_secondary = load_source3_secondary(ROOT,independent_records,public_by_id,secondary_collections,
                                              source_bindings=source3_bindings)
    from source3_recovered_legal_metadata import validate_archived_legal_sources
    validate_archived_legal_sources(selection,source3_secondary)
    secondary = combine_metadata(independent_records,procedural_secondary,phase11_secondary,context38_secondary,realism_completion_legal,remaining9_secondary,source3_secondary)
    realism_completion_progress = apply_realism_completion(result,independent_records,realism_completion,secondary['effective_realism_pass'])
    validate_context_default_safety(selection['recommended_ids'],context38_secondary)
    validate_default_review_safety(selection['recommended_ids'], reviews, independent_records+secondary['records'])
    validate_independent_archive_safety(selection, independent_records+secondary['records'])
    from realism_completion_metadata import validate_archive_containment as validate_realism_completion_containment
    if realism_completion_bindings:
        validate_realism_completion_containment(selection,realism_completion)
    independent_by_id = {r['question_id']: r for r in independent_records}
    for row in result:
        supplementary = secondary['assessments'].get(row['question_id'])
        if supplementary is not None:
            row['independent_legacy_supplementary_assessment'] = supplementary
        audit_row = independent_by_id.get(row['question_id'])
        if audit_row:
            apply_independent_legacy_review(row,audit_row,
                source_binding=independent_source_bindings.get(row['question_id']))
        limitation = context38_secondary['primary_limitations'].get(row['question_id'])
        if limitation is not None:
            row['independent_legacy_primary_assessment_limitation'] = copy.deepcopy(limitation)
            if supplementary is not None:
                row['independent_legacy_primary_assessment_limitation']['fresh_supplementary_evidence'] = {
                    key:copy.deepcopy(supplementary[key]) for key in
                    ('report_path','report_sha256','result_path','result_raw_sha256','actor_provenance','auditor_instance')}
        hold=holds.get(row['question_id']) or safety_holds.get(row['question_id'])
        if hold:
            row['default_practice_hold']=hold
            # Legal/realism opinions remain separate. A positive opinion must
            # not erase an unresolved, unchanged-content editorial hold.
            if row['disposition']=='KEEP':
                row['disposition_before_default_hold']=row['disposition']
                row['blocker_before_default_hold']=row['blocker']
                row.update(disposition='HOLD',blocker=hold['reason'])

    from note_question_discrepancies import load_metadata as load_note_links, apply_holds as apply_note_link_holds
    note_links = load_note_links(ROOT, public_by_id, selection['recommended_ids'])
    apply_note_link_holds(result, note_links)

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
    effective_notes = load_notes(ROOT)
    effective = {u['id']: u for c in effective_notes['chapters'] for u in c['units']}
    for claim in claims:
        validate_claim(claim, effective, ROOT)
    census_specs = [dict(path='reports/full-corpus-review/' + name,
                         notes_revision='2026-10-30.cdtm13-vax04.1') for name in (
        'pub05-14-note-census.json', 'note-wave2-census.json', 'note-wave3-census.json', 'note-wave4-census.json', 'note-wave5-census.json')]
    census_specs.append(dict(path='reports/full-corpus-review/counsel-shield-final-census.json',
        notes_revision='2026-11-03.counsel-shield-final.1', supersedes={
            'w3-b-1': 'reports/full-corpus-review/pub05-14-note-census.json',
            'w3-d-23': 'reports/full-corpus-review/pub05-14-note-census.json'}))
    appendix_a_ids = ['appendix-a-1','appendix-a-10','appendix-a-2','appendix-a-3',
                      'appendix-a-4','appendix-a-5','appendix-a-6','appendix-a-7']
    census_specs.append(dict(path='reports/full-corpus-review/appendix-atoms-a-census.json',
        notes_revision='2026-10-30.cdtm13-vax04.1', supersedes={
            uid: 'reports/full-corpus-review/note-wave2-census.json' for uid in appendix_a_ids}))
    census_specs.append(dict(path='reports/full-corpus-review/ce-disclosure-final-census.json',
        notes_revision='2026-11-03.ce-disclosure.1', supersedes={
            'w1-a-7': 'reports/full-corpus-review/note-wave4-census.json'}))
    appendix_b_ids = ['appendix-a-8','appendix-a-9'] + ['appendix-b-'+str(i) for i in range(1,7)]
    census_specs.append(dict(path='reports/full-corpus-review/appendix-atoms-b-census.json',
        notes_revision='2026-10-30.cdtm13-vax04.1', supersedes={
            uid: 'reports/full-corpus-review/note-wave2-census.json' for uid in appendix_b_ids}))
    for name in ('note-wave6-census.json', 'note-wave7-census.json',
                 'note-wave8-census.json', 'note-wave9-census.json',
                 'note-wave10-census.json', 'note-wave11-census.json',
                 'note-wave12-census.json', 'note-wave13-census.json',
                 'note-wave14-census.json', 'note-wave15-census.json',
                 'note-wave16-census.json'):
        census_specs.append(dict(path='reports/full-corpus-review/'+name,
            notes_revision='2026-10-30.cdtm13-vax04.1'))
    census_specs.append(dict(path='reports/full-corpus-review/refill-cancer-final-census.json',
        notes_revision='2026-11-03.refill-cancer.1', supersedes={
            uid:'reports/full-corpus-review/note-wave6-census.json' for uid in ('w2-c-1','w2-c-12')}))
    census_specs.append(dict(path='reports/full-corpus-review/emergency-kit-final-census.json',
        notes_revision='2026-11-03.emergency-kit.1', supersedes={
            'w4-a-19': 'reports/full-corpus-review/note-wave11-census.json',
            'w4-a-20': 'reports/full-corpus-review/note-wave12-census.json'}))
    from notes_census_reassessment import registered_specs
    from notes_body_reassessment import registered_specs as registered_body_specs, ordered_specs
    from notes_inactive_census_successor import registered_specs as registered_inactive_specs
    census_specs.extend(ordered_specs(ROOT,registered_specs(ROOT,effective_notes)+registered_body_specs(ROOT,effective_notes)+registered_inactive_specs(ROOT,effective_notes)))
    census_units, census_claims = compose_note_censuses(census_specs, effective, by_id, ROOT)
    complete_census_units = {uid for uid, unit in census_units.items() if
        unit['census_status'] == 'COMPLETE_AUTHOR_ENUMERATION_PENDING_INDEPENDENT_COMPLETENESS_CHECK'}
    census = {'claims': census_claims}
    if len({c['claim_id'] for c in census['claims']}) != len(census['claims']):
        raise ValueError('Duplicate cross-census claim')
    complete_census_claims = [c for c in census['claims'] if c['unit_id'] in complete_census_units]
    reviewed_units = {c['unit_id'] for c in claims}
    open_units = {c['unit_id'] for c in claims if c['review_status'] == 'HOLD_FOR_LEGAL_REVIEW'}
    units = [dict(unit_id=u['id'], chapter_id=c['id'], baseline_body_sha256=u['body_sha256'],
                  effective_body_sha256=effective[u['id']]['body_sha256'],
                  actual_effective_body_sha256=hashlib.sha256(effective[u['id']]['body'].encode()).hexdigest(),
                  stored_effective_hash_matches_body=effective[u['id']]['body_sha256']==hashlib.sha256(effective[u['id']]['body'].encode()).hexdigest(),
                  editorial_update_status='VERSIONED_REVISION_APPLIED' if effective[u['id']].get('content_version') else 'PRESERVED_INPUT',
                  inventory_status='INVENTORIED_NOT_CLAIM_CENSUS',
                  reviewed_claim_ids=[x['claim_id'] for x in claims if x['unit_id'] == u['id']],
                  legal_review_status='PARTIAL_AUTHOR_REVIEW_WITH_OPEN_CLAIM' if u['id'] in open_units else ('PARTIAL_AUTHOR_REVIEW_NOT_CENSUS' if u['id'] in reviewed_units else 'UNREVIEWED'),
                  atomic_claim_census_complete=u['id'] in complete_census_units,
                  atomic_claim_census_status=census_units.get(u['id'], {}).get('census_status', 'NOT_ENUMERATED'),
                  atomic_census_source=census_units.get(u['id'], {}).get('census_source'),
                  atomic_census_notes_revision=census_units.get(u['id'], {}).get('notes_revision'),
                  atomic_source_blocked_count=sum(x['review_status']=='SOURCE_BLOCKED' for x in census['claims'] if x['unit_id']==u['id']),
                  atomic_claim_ids=[x['claim_id'] for x in census['claims'] if x['unit_id'] == u['id']]) for c in notes['chapters'] for u in c['units']]
    from notes_independent_metadata import load_metadata
    computed_ledger = ''.join(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n' for row in units).encode()
    independent_notes = load_metadata(ROOT,effective_notes,ledger_raw=computed_ledger)
    for row in units:
        row['independent_atomic_census_review'] = independent_notes['units'].get(row['unit_id'])
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
                    legal_review_counts={
                        'NOT_REVERIFIED_IN_FULL_CORPUS_REVIEW': 0,
                        **dict(Counter(r['legal_review_status'] for r in result))},
                    answer_key_assessment_counts=dict(Counter(r['answer_key_assessment'] for r in result)),
                    editorial_rubric_assessed_ids=sum(r['editorial_quality_assessment'] is not None for r in result),
                    editorial_rubric_is_release_certificate=False,
                    canonical_inventory=len(canonical), canonical_reaudits_this_session=0,
                    independent_legacy_legal_assessed=secondary['progress']['effective_key_assessed'],
                    independent_legacy_originals_read=secondary['progress']['unique_originals_read'],
                    independent_legacy_keys_unassessed=secondary['progress']['effective_keys_unassessed'],
                    independent_legacy_realism_pass=realism_completion_progress['effective_realism_pass'],
                    independent_legacy_review_is_canonical_release_evidence=False,
                    notes_chapters=len(notes['chapters']), notes_units=len(units),
                    notes_units_with_partial_claim_review=len(reviewed_units),
                    notes_units_with_versioned_edits=sum(u['editorial_update_status']=='VERSIONED_REVISION_APPLIED' for u in units),
                    notes_units_with_independent_final_content_review=sum('independent_content_review' in u for u in effective.values()),
                    independent_note_completeness_legal_review=independent_notes['progress'],
                    notes_units_with_author_atomic_claim_enumeration_records=len(complete_census_units),
                    notes_units_with_complete_atomic_claim_census=independent_notes['progress']['complete_units'],
                    complete_atomic_census_units_basis='CURRENT_INTEGRATED_INDEPENDENT_COMPLETENESS_NOT_LEGAL_PASS',
                    notes_units_with_atomic_claim_records=len(census_units),
                    partial_census_claim_or_clause_records=len(census['claims'])-len(complete_census_claims),
                    atomic_claim_census_basis='AUTHOR_ENUMERATION_NOT_INDEPENDENT_COMPLETENESS_OR_LEGAL_PASS',
                    atomic_claims_enumerated=len(complete_census_claims),
                    atomic_claims_source_checked=sum(c['review_status']=='AUTHOR_SOURCE_CHECKED' for c in complete_census_claims),
                    atomic_claims_source_blocked=sum(c['review_status']=='SOURCE_BLOCKED' for c in complete_census_claims),
                    reviewed_claims=len(claims), source_checked_claims=sum(x['review_status']=='AUTHOR_SOURCE_CHECKED' for x in claims),
                    open_claims=sum(x['review_status']=='HOLD_FOR_LEGAL_REVIEW' for x in claims),
                    author_atomic_claim_enumeration_complete=len(complete_census_units)==len(units),
                    atomic_claim_census_complete=independent_notes['progress']['complete_units']==len(units),
                    inventory_is_legal_review=False,
                    same_team_peer_this_session='NOT_CERTIFIED_BY_THIS_INVENTORY',
                    canonical_independent_audit_this_session='NOT_RUN',
                    deployment_status='CURRENT_BUILD_PUBLICATION_NOT_ASSERTED')
    progress['note_link_question_discrepancy_holds'] = note_links['summary']
    if realism_completion_bindings:
        progress['independent_legacy_realism_completion_supplementary_review'] = {**realism_completion_progress,'source_bindings':dict(sorted(realism_completion_bindings.items()))}
        progress['independent_legacy_raw_primary_realism_pass'] = realism_completion_progress['raw_primary_realism_pass']
    if procedural_secondary['assessments']:
        progress['independent_legacy_procedural_supplementary_review'] = procedural_secondary['progress']
    if phase11_secondary['assessments']:
        progress['independent_legacy_phase11_supplementary_review'] = phase11_secondary['progress']
        progress['independent_legacy_supplementary_review'] = secondary['progress']
    if context38_secondary['excluded_primary_key_ids']:
        progress['independent_legacy_context38_supplementary_review'] = context38_secondary['progress']
        progress['independent_legacy_supplementary_review'] = secondary['progress']
    if remaining9_bindings:
        progress['independent_legacy_remaining9_procedural_review'] = {
            **remaining9_secondary['progress'], 'source_bindings': dict(sorted(remaining9_bindings.items())),
            'scope': 'EXACT_NINE_LEGAL_ONLY_NO_PRIMARY_NEGATIVE_OR_REALISM_OVERRIDE'}
    if source3_bindings:
        progress['independent_legacy_source3_recovered_legal_review'] = {
            **source3_secondary['progress'], 'source_bindings': dict(sorted(source3_bindings.items())),
            'scope': 'EXACT_THREE_RECOVERED_SOURCE_LEGAL_ONLY_NO_PRIMARY_NEGATIVE_OR_REALISM_OVERRIDE',
            'new_independent_people_credit': 0, 'new_realism_pass_credit': 0}
        progress['independent_legacy_supplementary_review'] = secondary['progress']
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
