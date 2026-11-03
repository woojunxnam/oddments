"""CDTM05–12 source-bound review tests; no independent legal status is asserted."""
import copy
import hashlib
import json
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]

def read(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))

def record_hash(item):
    return hashlib.sha256(json.dumps(item,ensure_ascii=False,sort_keys=True,
        separators=(',', ':')).encode('utf-8')).hexdigest()

def test_review_has_exactly_40_individually_hashed_ids_and_160_options():
    source=read('reports/full-corpus-review/cdtm05-12-author-review.json')
    reviews=source['records']
    assert len(reviews)==40 and len({r['question_id'] for r in reviews})==40
    original={q['question_id']:q for q in read('practice_expansion/2026-10-23/candidates/questions.json')['questions']}
    revised={q['question_id']:q for q in read('practice_expansion/2026-10-28-representative/questions.json')['questions']}
    baseline=read('reports/full-corpus-review/baseline-inventory.json')['question_record_hashes']
    expected={f'MA-EXP-{n:04d}' for n in range(241,273)}|{f'MA-RW-{n:04d}' for n in range(29,37)}
    assert {r['question_id'] for r in reviews}==expected
    assert sum(len(r['choice_by_choice_findings']) for r in reviews)==160
    for r in reviews:
        q=(original|revised)[r['question_id']]
        assert record_hash(q)==r['record_sha256']==baseline[r['question_id']]
        assert set(r['choice_by_choice_findings'])=={c['id'] for c in q['choices']}
        for c in q['choices']:
            finding=r['choice_by_choice_findings'][c['id']]
            assert finding['finding_ko'].strip() and finding['official_url'].startswith('https://')
            assert finding['exact_authority'].strip()
        assert r['answer_key_crosscheck']['stored']==q['correct_choice_ids']
        assert r['answer_key_crosscheck']['expected_from_official_statements']==q['correct_choice_ids']
        assert r['answer_key_crosscheck']['matches'] is True
        assert r['legal_review_status']=='AUTHOR_SOURCE_CHECKED_NOT_INDEPENDENT'
        assert r['reviewer_provenance']['independent'] is False
        assert r['quality_assessment']['independent_audit'] is False
    assert all(x['disposition']=='KEEP' for x in reviews if x['question_id'].startswith('MA-RW-'))
    assert all(x['disposition']=='MINOR_EDIT' for x in reviews if x['question_id'].startswith('MA-EXP-'))

def test_fail_closed_when_a_single_option_or_full_record_changes():
    from sys import path as pythonpath
    import sys
    sys.path.insert(0,str(ROOT/'scripts'))
    from build_full_corpus_review import validate_review
    reviews={r['question_id']:r for r in read('reports/full-corpus-review/cdtm05-12-author-review.json')['records']}
    questions={q['question_id']:q for q in read('practice_expansion/2026-10-23/candidates/questions.json')['questions']}
    q=questions['MA-EXP-0255']
    r=reviews[q['question_id']]
    validate_review(q,r)
    modified=copy.deepcopy(q);modified['choices'][0]['text']+=' (unreviewed)'
    with pytest.raises(ValueError,match='Stale review'):
        validate_review(modified,r)
    cut=copy.deepcopy(r);cut['choice_by_choice_findings'].pop('D')
    with pytest.raises(ValueError,match='Missing choice findings'):
        validate_review(q,cut)

def test_five_explicit_notes_overlay_sections_and_author_claim_scope():
    import sys
    sys.path.insert(0,str(ROOT/'scripts'))
    from notes_revision import load_notes
    from build_cdtm0512_claims import make as make_claims
    old=load_notes(ROOT,revision_id='2026-10-30.discipline-cdtm.1')
    # Keep this test anchored to the exact historical overlay even after future revisions.
    now=load_notes(ROOT,revision_id='2026-10-30.cdtm05-12.1')
    assert now['edition']=='2026-10-30.cdtm05-12.1'
    oldunits={u['id']:u for c in old['chapters'] for u in c['units']}
    units={u['id']:u for c in now['chapters'] for u in c['units']}
    target=['w3-d-4','w3-d-5','w3-d-6','w3-d-7','w3-d-8']
    assert {i for i in units if units[i]['body_sha256']!=oldunits[i]['body_sha256']}==set(target)
    for key in target:
        assert units[key]['content_version']==now['edition']
        assert '독립' in units[key]['editor_note']
    claims=read('reports/full-corpus-review/cdtm05-12-note-claims.json')
    assert len(claims['claims'])==10
    assert {c['unit_id'] for c in claims['claims']}==set(target)
    assert all(c['review_status']=='AUTHOR_SOURCE_CHECKED' for c in claims['claims'])
    assert make_claims()==(ROOT/'reports/full-corpus-review/cdtm05-12-note-claims.json').read_text()

def test_corpus_counts_do_not_inflate_canonical_or_learner_progress():
    progress=read('reports/full-corpus-review/progress.json')
    assert progress['current_questions']==2346
    # Monotonic later review batches may add IDs/claims; do not erase this frozen cohort.
    assert progress['question_ids_with_review_records']>=161
    assert progress['legal_review_counts']['NOT_REVERIFIED_IN_FULL_CORPUS_REVIEW']<=2185
    assert progress['editorial_rubric_assessed_ids']>=80
    assert progress['notes_units_with_partial_claim_review']>=19
    assert progress['notes_units_with_versioned_edits']>=20
    assert progress['reviewed_claims']>=62
    assert progress['source_checked_claims']>=58
    assert progress['open_claims']==4
    assert progress['notes_units_with_complete_atomic_claim_census']==0
    assert progress['canonical_inventory']==439
    assert progress['canonical_reaudits_this_session']==0
    assert progress['canonical_independent_audit_this_session']=='NOT_RUN'
    assert read('reports/full-corpus-review/inventory-definitions.json')['public_practice_questions']==2346
