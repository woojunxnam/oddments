"""Structural/content-mapping tests, NOT an independent pharmacy-law audit."""
from pathlib import Path
import collections, hashlib, importlib.util, json, re
import pytest
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'candidates/questions.json').read_text());Q=D['questions']

def test_materialized_count(): assert len(Q)==1024

def test_unique_ids(): assert len({q['question_id'] for q in Q})==1024

def test_family_sizes(): assert collections.Counter(collections.Counter(q['family_id'] for q in Q).values())=={4:256}

def test_type_counts(): assert collections.Counter(q['question_type'] for q in Q)=={'SBA':768,'SATA':256}

def test_all_draft(): assert all(q['lifecycle_status']=='DRAFT' and not q['publication_eligible'] for q in Q)

def test_no_fabricated_independent_review(): assert all(q['independent_legal_audit'] is None and q['independent_realism_audit'] is None for q in Q)

def test_distinct_choices(): assert all(len({c['text'] for c in q['choices']})==4 for q in Q)

def test_answer_contract(): assert all(len(q['correct_choice_ids'])==1 if q['question_type']=='SBA' else 1<=len(q['correct_choice_ids'])<=4 for q in Q)

def test_truth_mapping():
 for q in Q:
  expected={k for k,v in q['_statement_truth'].items() if (not v if q['negative_lead_in'] else v)}
  assert expected==set(q['correct_choice_ids'])

def test_choice_rationales(): assert all(set(q['explanation']['choice_analysis'])==set('ABCD') and len(set(q['explanation']['choice_analysis'].values()))==4 for q in Q)

def test_content_hashes():
 for q in Q:
  raw=json.dumps({k:v for k,v in q.items() if k!='content_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
  assert hashlib.sha256(raw).hexdigest()==q['content_sha256']

def test_evidence_exists(): assert all(q['note_evidence'] and q['source_ids'] for q in Q)

def test_source_ids_resolve(): assert all(s in D['sources'] for q in Q for s in q['source_ids'])

def test_note_link_hash_shape(): assert all(re.fullmatch('[0-9a-f]{64}',e['body_sha256']) and '/notes/#chapter/' in e['url'] for q in Q for e in q['note_evidence'])

def test_note_snapshot_matches():
 snap=json.loads((ROOT/'research/note_evidence.json').read_text());units={u['id']:u for u in snap['units']}
 for q in Q:
  for e in q['note_evidence']:assert hashlib.sha256(units[e['unit_id']]['body'].encode()).hexdigest()==e['body_sha256']

def test_area_mapping_consistent(): assert all(str(q['area'])==q['competency_provisional'].split('.')[0] for q in Q)

def test_answer_balance(): assert collections.Counter(q['correct_choice_ids'][0] for q in Q if q['question_type']=='SBA')==dict.fromkeys('ABCD',192)

def test_sata_cardinality_variation(): assert collections.Counter(len(q['correct_choice_ids']) for q in Q if q['question_type']=='SATA')=={1:64,2:64,3:64,4:64}

def test_jsonl_matches(): assert [json.loads(x) for x in (ROOT/'candidates/questions.jsonl').read_text().splitlines()]==Q

def test_packets_do_not_forge_audits():
 p=[json.loads(x.read_text()) for x in sorted((ROOT/'review').glob('packet-*.json'))]
 assert len(p)==32 and all(len(x['items'])==32 for x in p)
 assert all(i['decision'] is None for x in p for i in x['items'])
 assert {i['question_id'] for x in p for i in x['items']}=={q['question_id'] for q in Q}

def test_no_private_drive_in_public_data():
 for p in [ROOT/'candidates/questions.json',ROOT/'research/note_evidence.json']:
  assert not any(s in p.read_text() for s in ['docs.google.com','drive.google.com','woojunxnam@gmail.com'])

def test_reader_payload_matches():
 s=(ROOT/'review/practice-lab.html').read_text();raw=s.split('<script id="payload" type="application/json">',1)[1].split('</script>',1)[0]
 assert json.loads(raw)==D

def test_no_fake_pass_prediction(): assert 'not NABP' in D['scoring'] and D['released_new_questions']==0

def test_semantic_review_not_asserted(): assert all(q['duplicate_review_status']=='SEMANTIC_REVIEW_PENDING' for q in Q)

def test_45_day_source_preservation():
 fam=next(f for f in json.loads((ROOT/'authoring/families.json').read_text()) if f['family_id']=='ORD05')
 assert '45' in json.dumps(fam) # source-derived current figure, not a new statutory verification test

def test_open_boundaries_visible():
 assert all('source_boundary' in q and len(q['source_boundary'])>35 for q in Q if q['inherited_flags'])

def test_manifest_checksums():
 p=ROOT/'MANIFEST.json'
 if not p.exists():pytest.skip('Manifest generated after final reports')
 for name,h in json.loads(p.read_text())['files'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h
