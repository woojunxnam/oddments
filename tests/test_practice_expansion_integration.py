"""Repository integration and release separation, not a pharmacy-law audit."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PKG=ROOT/'practice_expansion/2026-10-23'
DATA=json.loads((PKG/'candidates/questions.json').read_text())

def test_package_input_matches_unchanged_notes():
 assert hashlib.sha256((ROOT/'notes/guide.json').read_bytes()).hexdigest()==DATA['input_guide_sha256']

def test_no_draft_questions_in_public_payload():
 text=(ROOT/'site/generated/questions.json').read_text()
 assert 'MA-EXP-' not in text

def test_release_flags_remain_false():
 assert DATA['released_new_questions']==0
 assert all(x['lifecycle_status']=='DRAFT' and x['publication_eligible'] is False for x in DATA['questions'])

def test_main_links_to_status_not_candidate_payload():
 main=(ROOT/'site/index.html').read_text()
 assert main.count('href="practice-expansion/"')==2
 assert 'practice-lab.html' not in main

def test_status_is_metadata_only():
 page=(ROOT/'site/practice-expansion/index.html').read_text()
 assert 'DRAFT' in page and '신규 RELEASED' in page
 assert '<script' not in page and 'MA-EXP-0001' not in page
 assert not (ROOT/'site/practice-expansion/questions.json').exists()

def test_question_bytes_not_rewritten():
 assert hashlib.sha256((PKG/'candidates/questions.json').read_bytes()).hexdigest()=='f2b27d3105f2efab40d3ab943f0f5813bdadd793e5ffa60d262fe5ab4e40a74f'

def test_review_packets_remain_unadjudicated():
 packets=[json.loads(p.read_text()) for p in (PKG/'review').glob('packet-*.json')]
 assert len(packets)==32
 assert all(i['decision'] is None for p in packets for i in p['items'])

def test_draft_ids_dont_collide_with_current_registry():
 ids={json.loads(p.read_text()).get('question_id') for p in (ROOT/'data/questions').glob('*.json')}
 assert ids.isdisjoint(x['question_id'] for x in DATA['questions'])
