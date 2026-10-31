"""Proof of 40 distinct IDs/161 choices and author-only source provenance for CDTM/VAX."""
import copy,hashlib,json,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from build_full_corpus_review import validate_review,record_hash
from notes_revision import load_notes

def read(p):return json.loads((ROOT/p).read_text())

def test_all_reviewed_options_bind_to_preserved_source_records():
    records=read('reports/full-corpus-review/cdtm-vax-author-review.json')['records']
    assert len(records)==40
    assert len({x['question_id'] for x in records})==40
    assert sum(len(x['choice_by_choice_findings']) for x in records)==161
    original={q['question_id']:q for q in read('practice_expansion/2026-10-23/candidates/questions.json')['questions']}
    revised={q['question_id']:q for q in read('practice_expansion/2026-10-28-representative/questions.json')['questions']}
    baseline=read('reports/full-corpus-review/baseline-inventory.json')['question_record_hashes']
    expected={f'MA-EXP-{i:04d}' for i in range(273,305)}|{f'MA-RW-{i:04d}' for i in range(37,45)}
    assert {r['question_id'] for r in records}==expected
    for r in records:
        q=(original|revised)[r['question_id']]
        assert record_hash(q)==r['record_sha256']==baseline[r['question_id']]
        validate_review(q,r)
        assert r['reviewer_provenance']['independent'] is False
        assert r['answer_key_crosscheck']['matches']
        assert r['answer_key_crosscheck']['stored']==q['correct_choice_ids']
        assert r['quality_assessment']['independent_audit'] is False
        for c in q['choices']:
            f=r['choice_by_choice_findings'][c['id']]
            assert f['finding_ko'] and f['exact_authority'] and f['official_url'].startswith('https://')
    for id in ['MA-EXP-0287','MA-EXP-0303']:
        assert original[id]['correct_choice_ids']==['A','B','C','D']

def test_stale_record_and_stale_choice_findings_fail_closed():
    records={r['question_id']:r for r in read('reports/full-corpus-review/cdtm-vax-author-review.json')['records']}
    q=next(q for q in read('practice_expansion/2026-10-23/candidates/questions.json')['questions'] if q['question_id']=='MA-EXP-0303')
    r=records[q['question_id']]
    validate_review(q,r)
    old=copy.deepcopy(q);old['choices'][0]['text']+=' (unverified change)'
    with pytest.raises(ValueError,match='Stale review'):validate_review(old,r)
    old=copy.deepcopy(r);old['choice_by_choice_findings'].pop('A')
    with pytest.raises(ValueError,match='Missing choice findings'):validate_review(q,old)

def test_note_revision_six_target_units_and_claims_are_not_census():
    old=load_notes(ROOT,revision_id='2026-10-30.cdtm05-12.1')
    latest=load_notes(ROOT)
    assert latest['edition']=='2026-10-30.cdtm13-vax04.1'
    byid=lambda v:{u['id']:u for c in v['chapters'] for u in c['units']}
    a,b=byid(old),byid(latest)
    wanted={'w3-d-9','w3-d-10','w3-c-1','w3-c-2','w3-c-3','w3-c-4'}
    assert {id for id in a if a[id]['body_sha256']!=b[id]['body_sha256']}==wanted
    assert all(b[id]['content_version']==latest['edition'] for id in wanted)
    claims=read('reports/full-corpus-review/cdtm-vax-note-claims.json')['claims']
    assert len(claims)==13
    assert {c['unit_id'] for c in claims}==wanted
    assert all(c['review_status']=='AUTHOR_SOURCE_CHECKED' for c in claims)

def test_review_counts_and_released_canonical_separated():
    p=read('reports/full-corpus-review/progress.json')
    assert p['question_ids_with_review_records']==201
    assert p['legal_review_counts']['NOT_REVERIFIED_IN_FULL_CORPUS_REVIEW']==2145
    assert p['editorial_rubric_assessed_ids']==120
    assert p['reviewed_claims']==75 and p['source_checked_claims']==71 and p['open_claims']==4
    assert p['notes_units_with_versioned_edits']==26
    assert p['notes_units_with_partial_claim_review']==25
    assert p['canonical_inventory']==439 and p['canonical_reaudits_this_session']==0
    assert p['notes_units_with_complete_atomic_claim_census']==0

def test_practice_navigation_link_keeps_40_question_destinations():
    page=(ROOT/'site/notes/cdtm13-16-vax01-04.html').read_text()
    index=(ROOT/'site/notes/index.html').read_text()
    assert 'href="cdtm13-16-vax01-04.html"' in index
    for i in range(273,305):
        assert '#MA-EXP-'+str(i).zfill(4) in page
    for i in range(37,45):
        assert '#MA-RW-'+str(i).zfill(4) in page
    assert 'learning-tools.js' in page and 'learning-tools.css' in page
