"""Source fidelity / generation / integration, not an independent clinical or legal audit."""
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path
from html.parser import HTMLParser

class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.assets=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if "data-oddments-tools" in a:self.assets.append((tag,a))

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('refresh_builder',ROOT/'scripts/build_refresh.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
D=m.build_payload()
N=__import__('notes_revision').load_notes(ROOT)
U={u['id']:u for c in N['chapters'] for u in c['units']}


def test_inventory_and_unique_ids():
    assert D['stats']=={'cards':232,'curated':72,'drugs':127,'chapters':33,'terms':45,'stages':7}
    assert len({c['id'] for c in D['cards']})==232
    assert all(re.fullmatch(r'[A-Za-z0-9-]+',c['id']) for c in D['cards'])


def test_summary_content_has_terms_examples_and_boundaries():
    for c in D['cards']:
        assert all(isinstance(c[k],str) and c[k].strip() for k in ['title','takeaway','plain','example','watch'])
        assert c['review_status']=='SOURCE_DERIVED_NOT_INDEPENDENTLY_AUDITED'
        assert c['note_units'] and all(uid in U for uid in c['note_units'])


def test_all_reference_dates_hashes_and_flags_are_inherited():
    for c in D['cards']:
        assert c['source_hashes']=={uid:U[uid]['body_sha256'] for uid in c['note_units']}
        assert c['source_review_dates']==list(dict.fromkeys(U[uid]['source_review_date'] for uid in c['note_units']))
        assert c['flags']==sorted({f for uid in c['note_units'] for f in U[uid]['flags']})
    assert D['notes_sha256']==hashlib.sha256((ROOT/'notes/guide.json').read_bytes()).hexdigest()


def test_open_and_future_boundaries_not_silently_closed():
    cs=[c for c in D['cards'] if 'schedule-vi-continuity' in c['note_units']]
    assert cs and all('open' in c['flags'] for c in cs)
    assert all('date-sensitive' in c['flags'] for c in D['cards'] if 'ipledge-transition' in c['note_units'])
    assert '전수 재검증일이 아닙니다' in D['source_policy']


def test_existing_drug_values_preserved_without_new_clinical_doses():
    lookup={c['id']:c for c in D['cards']}
    for drug in N['drugs']:
        c=lookup['RF-D-'+drug['id']]
        assert (c['title'],c['plain'],c['example'],c['watch'])==(drug['generic'],drug['form'],drug['notes'],drug['legal_status'])
        assert c['source_ids']==drug['source_ids']
        assert c['lookup_label']==drug['lookup_label']


def test_math_examples_are_explicitly_not_patient_dosing():
    examples=[c for c in D['cards'] if c['kind']=='learning-example']
    assert len(examples)==3
    assert all('예시' in (c['plain']+c['example']) or '가상' in c['plain'] for c in examples)
    assert 60/2==30 and 8/(20/5)==2 and 2*10==20


def test_external_safety_sources_are_separately_identified():
    assert set(D['external_sources'])=={'ahrq-teachback','ahrq-brown-bag','fda-pharmacist'}
    for c in D['cards']:
        assert all(sid in D['external_sources'] for sid in c['external_sources'])
        if c['kind']=='external-safety':assert c['external_sources']
    assert all(s['checked_at']=='2026-10-27' and s['scope'] for s in D['external_sources'].values())


def test_seven_stages_cover_curated_cards_once():
    allids=[cid for s in D['stages'] for cid in s['card_ids']]
    assert len(allids)==len(set(allids))==72
    assert set(allids)=={c['id'] for c in D['cards'] if c['deck']=='core'}


def test_glossary_has_valid_links_and_no_empty_definitions():
    assert len({x['term'] for x in D['glossary']})==45
    assert all(x['meaning'] and all(uid in U for uid in x['note_units']) for x in D['glossary'])


def test_generated_files_are_current():
    for p,s in m.outputs().items():assert p.read_text(encoding='utf-8')==s
    js=(ROOT/'site/notes/refresh-data.js').read_text()
    assert '</script' not in js.lower()


def test_all_static_html_pages_load_global_dock_once():
    for p in (ROOT/'site').rglob('*.html'):
        doc=AssetParser();doc.feed(p.read_text())
        scripts=[a for tag,a in doc.assets if tag=='script']
        links=[a for tag,a in doc.assets if tag=='link']
        assert len(scripts)==len(links)==1,p
        assert (p.parent/scripts[0]['src']).resolve().is_file(),p
        assert (p.parent/links[0]['href']).resolve().is_file(),p


def test_main_notes_routes_are_additive_and_keyboard_top_is_route_safe():
    text=(ROOT/'site/notes/notes.js').read_text()
    assert 'MPJE_REFRESH_VIEW.render' in text and 'mountHome' in text
    for route in ['refresh','return','glossary']:assert route in text
    dock=(ROOT/'site/assets/learning-tools.js').read_text()
    assert 'window.scrollTo' in dock and not re.search(r'location\.hash\s*=',dock)
    assert 'localStorage' not in dock


def test_refresh_storage_is_isolated_and_no_network_calls():
    ui=(ROOT/'site/notes/refresh.js').read_text();core=(ROOT/'site/notes/refresh-core.js').read_text()
    assert "oddments.mpje.refresh.v1" in core
    assert 'localStorage.clear' not in ui and 'localStorage.removeItem' not in ui
    assert not re.search(r'\bfetch\s*\(',ui)
    assert 'application' in ui and 'oddments-refresh' in ui


def test_pure_browser_helpers_node_contract():
    subprocess.run(['node',str(ROOT/'tests/browser/refresh-core.test.cjs')],cwd=ROOT,check=True,capture_output=True,text=True)
