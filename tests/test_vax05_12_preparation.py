"""Check VAX05–12 prep inventory and candidate exercises without treating drafts as released."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(path):
    return json.loads((ROOT/path).read_text())

def hash_record(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def test_36_vax05_12_reviewed_records_are_individually_hash_pinned():
    source=load('reports/full-corpus-review/vax05-12-author-review.json')
    records=source['records']
    assert len(records)==36 and len({x['question_id'] for x in records})==36
    assert sum(len(x['choice_by_choice_findings']) for x in records)==145
    original={q['question_id']:q for q in load('practice_expansion/2026-10-23/candidates/questions.json')['questions']}
    revised={q['question_id']:q for q in load('practice_expansion/2026-10-28-representative/questions.json')['questions']}
    hashes=load('reports/full-corpus-review/baseline-inventory.json')['question_record_hashes']
    ids={f'MA-EXP-{i:04d}' for i in range(305,337)}|{f'MA-RW-{i:04d}' for i in range(45,49)}
    assert {x['question_id'] for x in records}==ids
    for r in records:
        q=(original|revised)[r['question_id']]
        assert r['record_sha256']==hash_record(q)==hashes[r['question_id']]
        assert sorted(r['choice_by_choice_findings'])==sorted(c['id'] for c in q['choices'])
        assert r['answer_key_crosscheck']['matches']
        assert r['reviewer_provenance']['independent'] is False

def test_four_candidate_cases_remain_draft_and_do_not_claim_live_rwid():
    source=load('reports/full-corpus-review/vax09-12-four-case-candidates.json')
    assert source['publication_status']=='DRAFT_ONLY_NOT_IN_ACTIVE_OR_CANONICAL_BANK'
    assert len(source['questions'])==4
    assert {x['family_id'] for x in source['questions']}=={'VAX09','VAX10','VAX11','VAX12'}
    for q in source['questions']:
        assert q['draft_id'].endswith('-CANDIDATE-01')
        assert q['legal_review_status']=='DRAFT_NEEDS_FRESH_INDEPENDENT_LEGAL_AUDIT'
        assert len(q['choices'])==4
        assert len(q['correct_choice_ids'])==1
        assert all(c['rationale_ko'] for c in q['choices'])
    active=load('practice_expansion/2026-10-28-representative/questions.json')['questions']
    assert not any(q['family_id'] in {'VAX09','VAX10','VAX11','VAX12'} for q in active if q['question_id'].startswith('MA-RW-'))

def test_source_linked_preparation_page_has_all_real_links():
    text=(ROOT/'site/notes/vax05-12.html').read_text()
    for i in range(305,337):
        assert '#MA-EXP-'+str(i).zfill(4) in text
    for i in range(45,49):
        assert '#MA-RW-'+str(i).zfill(4) in text
    assert 'learning-tools.css' in text and 'learning-tools.js' in text
    assert text.count('아직 별도 MA-RW 사례형 없음')==4
