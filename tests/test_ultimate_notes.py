"""Content/renderer checks; these are not independent legal adjudications."""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
GUIDE = json.loads((ROOT / 'notes/guide.json').read_text(encoding='utf-8'))
LEDGER = json.loads((ROOT / 'notes/editorial-map.json').read_text(encoding='utf-8'))
CHAPTERS = {c['id']: c for c in GUIDE['chapters']}
UNITS = {u['id']: u for c in GUIDE['chapters'] for u in c['units']}
SOURCES = GUIDE['sources']


def test_notes_inventory_and_stable_unique_ids():
    assert len(CHAPTERS) == 33
    assert sum(len(c['units']) for c in GUIDE['chapters']) == len(UNITS) == 306
    assert len(GUIDE['drugs']) == 127
    assert len({d['id'] for d in GUIDE['drugs']}) == 127
    assert len(GUIDE['inputs']) == 22
    for key in [*CHAPTERS, *UNITS]:
        assert re.fullmatch(r'[a-z0-9-]+', key), key
    for unit in UNITS.values():
        assert len(unit['body'].strip()) >= 50
        assert unit['title'].strip()
        assert unit['source_review_date']
        assert unit['kind'] in {'source-derived', 'editorial-synthesis', 'new-primary-source-check'}


def test_every_input_section_has_an_editorial_disposition():
    assert LEDGER['input_sections'] == len(LEDGER['decisions']) == 391
    for origin, item in LEDGER['decisions'].items():
        assert origin
        assert item['decision']
        if item.get('chapter'):
            assert item['chapter'] in CHAPTERS, (origin, item)
        if item.get('unit'):
            assert item['unit'] in UNITS, (origin, item)
    assert sum('merged' in d['decision'] for d in LEDGER['decisions'].values()) == 56


def test_all_sources_resolve_and_are_public_http_references():
    for sid, source in SOURCES.items():
        assert sid == source['id']
        url = source['url']
        parsed = urlparse(url)
        assert parsed.scheme in {'http', 'https'} and parsed.netloc, (sid, url)
        assert not any(x in url for x in ['\\', ' ', 'oaiusercontent', 'docs.google.com', 'drive.google.com', 'sandbox:'])
    for unit in UNITS.values():
        assert unit['source_ids'], unit['id']
        assert all(s in SOURCES for s in unit['source_ids']), unit['id']
    for drug in GUIDE['drugs']:
        assert drug['unit'] in UNITS
        assert drug['source_ids']
        assert all(s in SOURCES for s in drug['source_ids'])
        assert urlparse(drug['lookup_url']).netloc == 'dailymed.nlm.nih.gov'


def test_crosslinks_and_no_export_placeholders():
    for unit in UNITS.values():
        for chapter, sub in re.findall(r'\]\(#chapter/([a-z0-9-]+)(?:/([a-z0-9-]+))?\)', unit['body']):
            assert chapter in CHAPTERS, (unit['id'], chapter)
            if sub:
                assert sub in UNITS
        assert '[VENDOR_TABLE]' not in unit['body']
        assert '[BLUEPRINT_TABLE]' not in unit['body']
        assert 'docs.google.com' not in unit['body']
        assert 'drive.google.com' not in unit['body']
        assert not re.search(r'W[1-6]-[A-D]', unit['body']), unit['id']


def test_material_corrections_and_open_boundaries_are_retained():
    continuity = UNITS['schedule-vi-continuity']
    assert '14일' in continuity['body'] and '30일' in continuity['body']
    assert 'gabapentin' in continuity['body']
    assert 'open' in continuity['flags']
    body = '\n'.join(u['body'] for u in UNITS.values())
    assert '9.23(5)' in body and '21C' in body
    assert 'email' in body and '2021-04' in body
    assert '2026-11-15' in body and '2027-03-01' in body
    assert 'HIV' in body and 'DOCX' in body and 'OPEN' in body
    assert '독립 전수' in GUIDE['legal_review_scope']


def test_renderer_escapes_html_and_preserves_usp_and_tables():
    spec = importlib.util.spec_from_file_location('notes_builder', ROOT/'scripts/build_ultimate_notes.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    text = 'USP <795> and <797>\n\n<script>alert(1)</script>\n\n| A | B |\n| --- | --- |\n| x | y |\n'
    out = module.render_markdown(text)
    assert '<script>' not in out
    assert '&lt;795&gt;' in out and '&lt;797&gt;' in out
    assert 'table-scroll' in out and '<table>' in out


def test_generated_notes_match_canonical_inputs():
    spec = importlib.util.spec_from_file_location('notes_builder_check', ROOT/'scripts/build_ultimate_notes.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for path, generated in module.make_outputs().items():
        assert path.read_text(encoding='utf-8') == generated, str(path)
    build = json.loads((ROOT/'site/notes/build.json').read_text())
    assert build['baseline_content_sha256'] == hashlib.sha256((ROOT/'notes/guide.json').read_bytes()).hexdigest()
    from notes_revision import load_notes
    effective=load_notes(ROOT)
    assert build['content_sha256'] == hashlib.sha256(json.dumps(effective,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
    assert build['revision_provenance'] == effective['revision_provenance']
    assert build['stats']['drugs'] == 127


def test_main_entry_and_existing_application_contracts_preserved():
    text = (ROOT/'site/index.html').read_text()
    assert text.count('href="notes/"') >= 2
    for element in ['study-guide-button', 'history-button', 'bookmark-button', 'mode-heading',
                    'question-panel', 'guide-sections', 'choice-form', 'export-study-data']:
        assert f'id="{element}"' in text
    js = (ROOT/'site/notes/notes.js').read_text()
    assert 'oddments.mpje.ultimate-notes.v1' in js
    assert 'localStorage.clear' not in js
    assert 'localStorage.removeItem' not in js
    assert not re.search(r'\bfetch\s*\(', js)
    assert 'application' in js and 'oddments-ultimate-notes' in js


def test_static_book_unit_links_and_revision_header_match_actual_export():
    book=(ROOT/'site/notes/book.html').read_text()
    identifiers=set(re.findall(r'id="([^"]+)"',book))
    for fragment in re.findall(r'href="#([^"]+)"',book):
        assert fragment in identifiers, fragment
    assert '#chapter/cdtm/w3-d-2' not in book
    assert 'href="#w3-d-2"' in book
    from notes_revision import load_notes
    assert load_notes(ROOT)['edition'] in book
