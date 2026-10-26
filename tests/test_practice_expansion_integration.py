"""Archived evidence stays immutable; the owner-authorized practice channel is live."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import pytest

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / 'practice_expansion/2026-10-23'
DATA = json.loads((PKG / 'candidates/questions.json').read_text())
spec = importlib.util.spec_from_file_location('publish_practice', ROOT/'scripts/publish_practice.py')
publisher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publisher)

@pytest.fixture(scope='module')
def public():
    return publisher.build_payload()

@pytest.fixture(scope='module')
def rendered(public):
    return publisher.render(public)

def test_package_input_matches_unchanged_notes():
    assert hashlib.sha256((ROOT/'notes/guide.json').read_bytes()).hexdigest() == DATA['input_guide_sha256']

def test_no_expansion_in_canonical_audited_payload():
    assert 'MA-EXP-' not in (ROOT/'site/generated/questions.json').read_text()

def test_archived_release_evidence_is_not_fabricated():
    assert DATA['released_new_questions'] == 0
    assert all(q['lifecycle_status']=='DRAFT' and q['publication_eligible'] is False for q in DATA['questions'])

def test_source_question_bytes_not_rewritten():
    assert hashlib.sha256((PKG/'candidates/questions.json').read_bytes()).hexdigest() == 'f2b27d3105f2efab40d3ab943f0f5813bdadd793e5ffa60d262fe5ab4e40a74f'

def test_review_packets_remain_unadjudicated():
    packets=[json.loads(p.read_text()) for p in (PKG/'review').glob('packet-*.json')]
    assert len(packets)==32
    assert all(i['decision'] is None for p in packets for i in p['items'])

def test_ids_do_not_collide_with_canonical_registry():
    ids={json.loads(p.read_text()).get('question_id') for p in (ROOT/'data/questions').glob('*.json')}
    assert ids.isdisjoint(q['question_id'] for q in DATA['questions'])

def test_all_1024_are_online_published(public):
    assert public['status']=='PUBLISHED_PRACTICE'
    assert public['published_question_count']==1024
    assert all(q['online_practice_enabled'] and q['publication_status']=='PUBLISHED_PRACTICE' for q in public['questions'])

def test_publication_does_not_claim_independent_review(public):
    assert public['independent_review_status']=='NOT_INDEPENDENTLY_REVIEWED'
    assert public['canonical_released_question_count']==0
    assert all(q['verification_status']=='NOT_INDEPENDENTLY_REVIEWED' and q['independent_legal_audit'] is None and q['independent_realism_audit'] is None for q in public['questions'])

def test_questions_answers_explanations_and_source_links_preserved(public):
    for old,new in zip(DATA['questions'],public['questions'],strict=True):
        for field in ('question_id','family_id','stem','choices','correct_choice_ids','explanation','note_evidence','source_ids','source_boundary','content_sha256'):
            assert old[field]==new[field],(old['question_id'],field)

def test_no_draft_gate_in_public_ui(rendered):
    visible=re.sub(r'<script.*?</script>','',rendered,flags=re.S)
    assert 'DRAFT' not in visible and 'id="ack"' not in rendered and "$('#ack')" not in rendered
    assert '온라인 연습' in visible and '독립 법규 검토' in visible
    assert 'openQuestion(byId.get(location.hash.slice(1))||Q[0])' in rendered

def test_payload_escapes_script_close(rendered):
    payload=re.search(r'<script id="payload" type="application/json">(.*?)</script>',rendered,re.S).group(1)
    assert '<' not in payload
    assert len(json.loads(payload)['questions'])==1024

def test_independent_browser_storage_namespace(rendered):
    assert "KEY='oddments.mpje.practice.v1'" in rendered
    assert "localStorage.getItem('oddments.mpje.expansion.draft1')" in rendered
    assert 'localStorage.clear' not in rendered

def test_build_is_deterministic(public):
    assert publisher.render(public)==publisher.render(public)

def test_destination_guard():
    with pytest.raises(ValueError):
        publisher.prepare(ROOT/'site')

def test_build_updates_main_navigation_without_changing_tracked_site(tmp_path):
    prior={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'site').rglob('*') if p.is_file()}
    out=tmp_path/'public'
    result=publisher.prepare(out)
    main=(out/'index.html').read_text()
    assert main.count('href="practice-expansion/"')==2
    assert '1,024문항 연습 시작' in main and '원고·검토 상태 보기' not in main
    assert result['published_question_count']==1024
    assert json.loads((out/'practice-expansion/build.json').read_text())['status']=='PUBLISHED_PRACTICE'
    assert prior=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'site').rglob('*') if p.is_file()}
    assert (out/'generated/questions.json').read_bytes()==(ROOT/'site/generated/questions.json').read_bytes()

def test_missing_config_or_template_anchor_is_not_silently_accepted():
    with pytest.raises(ValueError):
        publisher.replace_exact('missing','anchor','new')
