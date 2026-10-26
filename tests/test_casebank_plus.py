"""New bank: data validity, substantive source mapping and truthful publication states."""
from collections import Counter
import hashlib,importlib.util,json,re,runpy
from pathlib import Path
import pytest
R=Path(__file__).resolve().parents[1];P=R/'practice_expansion/2026-10-26-plus'
D=json.loads((P/'questions.json').read_text());Q=D['questions']
G=json.loads((R/'notes/guide.json').read_text());U={u['id']:u for c in G['chapters'] for u in c['units']}

def test_new_total_and_construction():
 assert len(Q)==1152 and len({q['family_id'] for q in Q})==128
 assert set(Counter(q['family_id'] for q in Q).values())=={9}
 assert Counter(q['practice_angle'] for q in Q)=={'single-case':342,'workqueue':450,'multiple-response':360}

def test_original_and_canonical_ids_are_disjoint():
 old=json.loads((R/'practice_expansion/2026-10-23/candidates/questions.json').read_text())['questions']
 existing={q['question_id'] for q in old}|{json.loads(p.read_text())['question_id'] for p in (R/'data/questions').glob('*.json')}
 assert existing.isdisjoint(q['question_id'] for q in Q)
 assert len({q['question_id'] for q in Q})==1152

def test_blueprint_is_current_editorial_allocation():
 assert Counter(q['area'] for q in Q)=={1:252,2:378,3:279,4:243}
 assert 'before March 1, 2027' in D['intended_outline_window']

def test_answer_contract_and_individual_rationales():
 for q in Q:
  ids={c['id'] for c in q['choices']};answers=set(q['correct_choice_ids'])
  assert answers<=ids and len(ids)==len(q['choices'])
  assert len(answers)==1 if q['question_type']=='SBA' else 1<=len(answers)<len(ids)
  assert set(q['explanation']['choice_analysis'])==ids
  assert all(len(x)>25 for x in q['explanation']['choice_analysis'].values())
  assert len(set(c['text'] for c in q['choices']))==len(ids)

def test_sata_does_not_leak_a_fixed_answer_count():
 assert Counter(len(q['correct_choice_ids']) for q in Q if q['question_type']=='SATA')=={1:90,2:90,3:90,4:90}

def test_source_snapshots_and_urls_are_valid():
 assert hashlib.sha256((R/'notes/guide.json').read_bytes()).hexdigest()==D['input_guide_sha256']
 for q in Q:
  assert q['note_evidence'] and q['source_ids']
  for e in q['note_evidence']:
   assert U[e['unit_id']]['body_sha256']==e['body_sha256']
   assert e['url'].endswith('/'+e['unit_id'])
  for sid in q['source_ids']:assert D['sources'][sid]['url'].startswith('https://')

def test_no_private_files_or_signed_urls_in_public_data():
 text=(P/'questions.json').read_text()
 for token in ['docs.google.com','drive.google.com','oaiusercontent.com','/mnt/data/','sk-proj-']:
  assert token not in text

def test_source_reads_are_not_fabricated_independent_audits():
 for q in Q:
  assert q['independent_legal_audit'] is None and q['independent_realism_audit'] is None
  assert q['verification_status']=='NOT_INDEPENDENTLY_REVIEWED'
  assert q['publication_status']=='PUBLISHED_PRACTICE' and q['online_practice_enabled']
  assert q['difficulty_status']=='NOT_CALIBRATED'

def test_additional_rule_is_marked_as_external_expansion():
 qs=[q for q in Q if q['family_id']=='PLUS-SC31']
 assert len(qs)==9 and all(q['additional_primary_evidence'] for q in qs)
 assert all('45 days' in q['additional_primary_evidence'][0]['scope'] for q in qs)

def test_deterministic_authoring_build():
 m=runpy.run_path(str(P/'scripts/build_casebank.py'))
 assert m['build']()==D

def test_content_hashes_cover_substantive_fields():
 keys=['question_id','family_id','stem','choices','correct_choice_ids','explanation','note_evidence','source_ids']
 for q in Q:
  raw=json.dumps({k:q[k] for k in keys},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
  assert hashlib.sha256(raw).hexdigest()==q['content_sha256']

def test_no_exact_question_choice_duplicates():
 def fp(q):return q['stem'].strip().lower(),tuple(sorted(c['text'].strip().lower() for c in q['choices']))
 assert len({fp(q) for q in Q})==len(Q)

def test_threshold_boundaries_have_both_outcomes():
 for fam in ('PLUS-SC32','PLUS-SC33'):
  qs=[q for q in Q if q['family_id']==fam]
  for q in qs:
   f=q['conditional_facts'];a=next(c['text'] for c in q['choices'] if c['id'] in q['correct_choice_ids'])
   assert ('does not exceed' in a)==(f['cfu']<=f['threshold'])

def test_inventory_arithmetic_keys_recompute():
 for q in Q:
  if q['family_id']!='PLUS-SC27':continue
  f=q['conditional_facts'];expected=f['opening']+f['received']-f['dispensed']-f['reverse']
  a=next(c['text'] for c in q['choices'] if c['id'] in q['correct_choice_ids'])
  assert a==f'{expected} tablets'

def test_sba_key_positions_not_concentrated():
 n=Counter(q['correct_choice_ids'][0] for q in Q if q['question_type']=='SBA')
 assert max(n.values())-min(n.values())<=10

def test_fresh_45day_condition_is_not_issue_date():
 for q in Q:
  if q['family_id']!='PLUS-SC31':continue
  f=q['conditional_facts'];a=next(c['text'] for c in q['choices'] if c['id'] in q['correct_choice_ids'])
  if f['days_after_receipt']>45:assert 'expired' in a
  elif not f['named_patient']:assert 'named patient' in a
  elif not f['registered_location']:assert 'location' in a and 'fails' in a
  else:assert 'permit' in a

def test_new_question_ui_has_a_single_defined_lead():
 for q in Q:
  assert q['scenario'] and q['lead_in'] and q['stem']==q['scenario']+'\n\n'+q['lead_in']
  assert 'Case B:' not in q['stem']

def test_public_research_does_not_claim_actual_recent_exams():
 text=(R/'site/practice-expansion/research.html').read_text()
 assert '비공개' in text and '128개 모델' in text and '2027년 3월 1일' in text
 assert '실제 시험과 동일한 난도' in text and '주장할 근거는 없습니다' in text

def test_collection_options_are_real_html_options():
 from html.parser import HTMLParser
 spec=importlib.util.spec_from_file_location('publisher_options',R/'scripts/publish_practice.py')
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 class Options(HTMLParser):
  def __init__(self):super().__init__();self.active=False;self.values=[]
  def handle_starttag(self,tag,attrs):
   a=dict(attrs)
   if tag=='select' and a.get('id')=='collection':self.active=True
   if tag=='option' and self.active:self.values.append(a.get('value'))
  def handle_endtag(self,tag):
   if tag=='select':self.active=False
 p=Options();p.feed(m.render(m.build_payload()))
 assert p.values==['','plus-20261026','original-20261023']
