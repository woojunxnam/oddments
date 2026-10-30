"""Deterministic inventory, not a bulk legal-review certification."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'reports/full-corpus-review'


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
    if not review.get('reviewer_provenance') or not review.get('checked_at'):
        raise ValueError('Unattributed review: ' + q['question_id'])


def validate_claim(claim, effective_units, root=ROOT):
    if claim['unit_content_sha256'] != effective_units[claim['unit_id']]['body_sha256']:
        raise ValueError('Stale claim unit hash: ' + claim['claim_id'])
    if hashlib.sha256((root/claim['source_evidence']).read_bytes()).hexdigest() != claim['source_evidence_sha256']:
        raise ValueError('Stale claim evidence hash: ' + claim['claim_id'])


def build():
    config = read('site/practice-expansion/publication.json')
    paths = ['practice_expansion/2026-10-23/candidates/questions.json'] + [a['path'] for a in config['additional_banks']]
    baseline = read('reports/full-corpus-review/baseline-inventory.json')
    assert baseline['question_count'] == len(baseline['question_record_hashes']) == 2328
    review_records = [r for name in ['unit3a-author-review.json','unit3b-author-review.json','mor-author-review.json'] for r in read('reports/full-corpus-review/'+name)['records']]
    assert len({r['question_id'] for r in review_records}) == len(review_records)
    reviews = {r['question_id']:r for r in review_records}
    selection = read('practice_expansion/2026-10-28-representative/selection.json')
    replacements = {x['legacy_question_id']: x['replacement_question_id'] for x in selection['replacements']}
    holds = {x['legacy_question_id'] for x in selection['holds']}
    authoring = [read('practice_expansion/2026-10-28-representative/authoring/'+name) for name in ['05_personnel_ratios.json','06_personnel_training.json']]
    new_author = {q['question_id']:q for source in authoring for q in source['questions']}
    unit3b_ids = {q['question_id'] for q in authoring[-1]['questions']}
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
                row['next_action'] = 'Resolve stated blocker; no independent release claim.'
            if qid in new_author:
                a = new_author[qid]
                row.update(disposition='KEEP', legal_review_status='AUTHOR_SOURCE_CHECKED_NOT_INDEPENDENT',
                           decision_signature=a['decision_signature'], checked_at='2026-10-29',
                           reviewer_provenance=dict(author_session='20261029-unit3b-root' if qid in unit3b_ids else '20261029-unit3a-root', peer='NOT_RUN_THIS_SESSION', independent='NOT_RUN'),
                           implementation_status='NEW_DISTINCT_ID', blocker='Independent audit not performed.',
                           next_action='Review frozen current hash independently before canonical release.')
                row['choice_by_choice_findings'] = {c['id']: dict(finding_ko=c['rationale_ko'], authorities=c['authority_refs']) for c in a['choices']}
                row['authority_clauses'] = [r for c in a['choices'] for r in c['authority_refs']]
            row['deployment_status'] = 'BRANCH_CANDIDATE_NOT_DEPLOYED' if qid in unit3b_ids else 'UNIT3A_BASELINE_DEPLOYED_SEE_DEPLOYMENT_EVENT'
            row['publication_status'] = ('PRACTICE_CONFIG_DEFAULT' if qid in selection['recommended_ids'] else 'PRACTICE_CONFIG_ARCHIVE')
            result.append(row)
    ids = [r['question_id'] for r in result]
    assert len(ids) == len(set(ids)) == config['published_total']
    assert set(baseline['question_record_hashes']) <= set(ids)
    assert set(reviews) <= set(ids)
    notes = read('notes/guide.json')
    claims = [c for name in ['unit3a-claims.json','unit3b-claims.json','mor-claims.json'] for c in read('reports/full-corpus-review/'+name)['claims']]
    from notes_revision import load_notes
    effective = {u['id']: u for c in load_notes(ROOT)['chapters'] for u in c['units']}
    for claim in claims:
        validate_claim(claim, effective, ROOT)
    units = [dict(unit_id=u['id'], chapter_id=c['id'], baseline_body_sha256=u['body_sha256'],
                  inventory_status='INVENTORIED_NOT_CLAIM_CENSUS',
                  reviewed_claim_ids=[x['claim_id'] for x in claims if x['unit_id'] == u['id']],
                  legal_review_status='PARTIAL_AUTHOR_REVIEW_WITH_OPEN_CLAIM' if u['id'] in {'w1-b-8','w1-b-9'} else ('PARTIAL_AUTHOR_REVIEW_NOT_CENSUS' if u['id'] in {'w1-b-10','w1-c-7'} else 'UNREVIEWED'),
                  atomic_claim_census_complete=False) for c in notes['chapters'] for u in c['units']]
    canonical = []
    for path in sorted((ROOT/'data/questions').glob('*.json')):
        q = json.loads(path.read_text())
        canonical.append(dict(question_id=q['question_id'], path=str(path.relative_to(ROOT)), content_sha256=record_hash(q),
                              inventory_status='INVENTORIED_NOT_REAUDITED', existing_lifecycle_status=q.get('lifecycle_status'),
                              existing_audit_evidence_preserved=True))
    coverage = dict(outline='MPJE-MA-PRE2027', mapping_status='INVENTORY_PLUS_FOUR_PARTIAL_UNITS_NOT_FULL_DECISION_PATH_COVERAGE',
                    units=units, reviewed_claims=claims, inferred_family_passes=0)
    progress = dict(baseline_commit=baseline['base_commit'], baseline_questions=2328, new_questions=len(new_author),
                    current_questions=len(result), original_2176_inventory=sum(r['question_id'].startswith(('MA-EXP-', 'MA-CASE-')) for r in result),
                    prior_MA_REV_inventory=96, current_MA_RW_inventory=len(read(paths[-1])['questions']),
                    representative_355_implementation=selection['stats'],
                    question_ids_read_this_session=len(reviews)+len(new_author), review_count_scope='CUMULATIVE_UNIT3A_UNIT3B_AND_MOR_NOT_ONE_SESSION', unit3b_question_ids_reviewed=22,
                    legal_review_counts=dict(Counter(r['legal_review_status'] for r in result)),
                    canonical_inventory=len(canonical), canonical_reaudits_this_session=0,
                    notes_chapters=len(notes['chapters']), notes_units=len(units),
                    reviewed_claims=len(claims), source_checked_claims=sum(x['review_status']=='AUTHOR_SOURCE_CHECKED' for x in claims),
                    open_claims=sum(x['review_status']=='HOLD_FOR_LEGAL_REVIEW' for x in claims), atomic_claim_census_complete=False,
                    inventory_is_legal_review=False, same_team_peer_this_session='NOT_RUN', canonical_independent_audit_this_session='NOT_RUN')
    from build_representative_rewrites import pattern_metrics
    by_id = {q['question_id']: q for q in all_questions}
    comparison = dict(method='Same stored question objects, same pattern_metrics function; baseline main IDs fixed.',
                      before_main_sha=baseline['base_commit'],
                      before_archive=pattern_metrics([by_id[i] for i in baseline['question_record_hashes']]),
                      after_archive=pattern_metrics(all_questions),
                      before_default=pattern_metrics([by_id[i] for i in baseline['recommended_ids']]),
                      after_default=pattern_metrics([by_id[i] for i in selection['recommended_ids']]),
                      semantic_duplicate_verdict='NOT_INFERRED_FROM_PATTERNS')
    def pretty(x): return json.dumps(x, ensure_ascii=False, indent=2)+'\n'
    def jsonl(xs): return ''.join(json.dumps(x, ensure_ascii=False, separators=(',', ':'))+'\n' for x in xs)
    return {OUT/'pattern-comparison.json': pretty(comparison), OUT/'question-ledger.jsonl': jsonl(result), OUT/'notes-unit-ledger.jsonl': jsonl(units),
            OUT/'notes-claim-ledger.jsonl': jsonl(claims), OUT/'canonical-inventory.json': pretty(canonical),
            OUT/'coverage-matrix.json': pretty(coverage), OUT/'progress.json': pretty(progress)}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--check', action='store_true'); args=parser.parse_args()
    for path, text in build().items():
        if args.check:
            if not path.exists() or path.read_text()!=text: raise SystemExit('Stale corpus inventory: '+str(path))
        else: path.write_text(text)
    print('Full corpus inventory checked; inventory does not confer legal verification.')
