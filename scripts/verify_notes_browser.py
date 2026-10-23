#!/usr/bin/env python3
"""Exercise the deployed-shaped notes reader on a loopback HTTP server.

Requires Playwright and its Chromium browser. This tests software, not legal accuracy.
The --inline-preview mode renders local content without navigation for constrained
runtimes. It never claims HTTP, real-origin storage or main-page navigation coverage.
"""
from __future__ import annotations
import argparse
from functools import partial
import http.server
import json
import os
from pathlib import Path
import re
import threading
from urllib.parse import quote
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT/'site'
KEY = 'oddments.mpje.ultimate-notes.v1'


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--inline-preview',action='store_true')
    ap.add_argument('--executable-path')
    ap.add_argument('--output',default='test-results/ultimate-notes')
    args=ap.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    checks=[];errors=[];external=[]
    def checked(name):checks.append(name);print('PASS:',name,flush=True)
    server=None
    if not args.inline_preview:
        class Handler(http.server.SimpleHTTPRequestHandler):
            def log_message(self,*args):pass
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(SITE)))
        threading.Thread(target=server.serve_forever,daemon=True).start()
        base=f'http://127.0.0.1:{server.server_port}/'
    else:base=''
    try:
      with sync_playwright() as pw:
        launch={'headless':True}
        if args.executable_path:launch['executable_path']=args.executable_path
        browser=pw.chromium.launch(**launch)
        ctx=browser.new_context(viewport={'width':1440,'height':1000},accept_downloads=True)
        page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('request',lambda r:external.append(r.url) if r.url.startswith(('https://','http://')) and not r.url.startswith(base or 'NOT-HTTP-PREVIEW') else None)
        if args.inline_preview:
            markup=(SITE/'notes/index.html').read_text()
            markup=markup.replace('<link rel="stylesheet" href="notes.css">','<style>'+(SITE/'notes/notes.css').read_text()+'</style>')
            markup=re.sub(r'<script src="[^"]+" defer></script>','',markup)
            page.set_content(markup)
            page.add_script_tag(content=(SITE/'notes/content.js').read_text())
            page.add_script_tag(content=(SITE/'notes/notes.js').read_text())
        else:
            page.goto(base,wait_until='networkidle')
            expect(page.locator('#study-guide-button')).to_be_visible()
            # Styling classes may be reused by other independent entry cards.
            notes_entry=page.locator('a.notes-entry-primary[href="notes/"]')
            expect(notes_entry).to_have_count(1)
            notes_entry.click()
            expect(page).to_have_url(re.compile('/notes/$'))
            checked('main page entry opens independent notes page')
        expect(page.locator('.chapter-card')).to_have_count(33)
        page.screenshot(path=str(out/'home-desktop.png'))
        checked('33 chapter cards render without JavaScript errors')
        page.locator('.skip-link').focus();page.keyboard.press('Enter')
        expect(page.locator('#reader')).to_be_focused()
        expect(page.locator('.chapter-card')).to_have_count(33)
        checked('keyboard skip link focuses content without changing application route')
        def route(hash_):
            page.evaluate('(value)=>{location.hash=value}',hash_)
            page.wait_for_timeout(110)
        route('chapter/refills-transfer/schedule-vi-continuity')
        continuity=page.locator('#schedule-vi-continuity')
        expect(continuity).to_contain_text('14일')
        expect(continuity).to_contain_text('30일')
        expect(continuity).to_contain_text('gabapentin')
        expect(continuity.locator('.badge.warning')).to_be_visible()
        continuity.locator('[data-save]').click()
        continuity.locator('[data-read]').click()
        expect(continuity.locator('[data-save]')).to_have_attribute('aria-pressed','true')
        expect(page.locator('#progress-label')).to_have_text('1 / 306')
        checked('corrected continuity section, OPEN badge, bookmark and manual read state')
        page.locator('[data-font="1"]').click()
        expect(page.locator('#font-size-label')).to_have_text('19px')
        page.locator('#focus-button').click()
        expect(page.locator('body')).to_have_class(re.compile('focus-reading'))
        page.locator('#focus-button').click()
        page.locator('#theme-button').click();page.locator('#theme-button').click()
        expect(page.locator('html')).to_have_attribute('data-theme','dark')
        page.screenshot(path=str(out/'chapter-dark.png'))
        page.locator('#theme-button').click()
        checked('font size, focus reading and light/dark preferences')
        route('saved');expect(page.locator('#saved-count')).to_have_text('1개 절')
        expect(page.locator('.result-card')).to_contain_text('Schedule VI')
        checked('bookmarked section appears in saved view')
        for q in ['gabapentin','재고','247 CMR','72시간']:
            route('search/'+quote(q,safe=''))
            expect(page.locator('.result-card').first).to_be_visible()
        route('search/'+quote('<img src=x onerror=alert(1)>',safe=''))
        expect(page.locator('#reader img')).to_have_count(0)
        checked('English/Korean/legal-number searches and injection-safe query rendering')
        route('search/gabapentin')
        page.locator('#search-flag').select_option('open')
        expect(page.locator('.result-card').first).to_be_visible()
        checked('OPEN filter works with search')
        for q in ['Sublocade','Adderall','naloxone']:
            route('drugs/'+q)
            expect(page.locator('.drug-card').first).to_be_visible()
        route('drugs')
        expect(page.locator('#drug-count')).to_contain_text('127개 항목')
        page.locator('#more-drugs').click();expect(page.locator('.drug-card')).to_have_count(60)
        page.locator('#drug-schedule').select_option('II')
        assert page.locator('.drug-card').count()>0
        checked('127-drug directory, names, schedule filter and pagination')
        route('sources');expect(page.locator('.reference-entry')).to_have_count(248)
        page.locator('#source-query').fill('FDA');assert page.locator('.reference-entry').count()>0
        checked('source registry and filtering')
        # All units must be rendered by one chapter, with valid source disclosure links.
        chapters=page.evaluate('MPJE_NOTES.chapters.map(c=>({id:c.id,units:c.units.map(u=>u.id)}))')
        total=0
        for ch in chapters:
            route('chapter/'+ch['id'])
            expect(page.locator('.reading-unit')).to_have_count(len(ch['units']))
            total+=len(ch['units'])
            assert page.locator('.unit-body script').count()==0
        assert total==306
        checked('all 306 sections render under their topic chapters')
        route('chapter/sterile-compounding')
        assert '<797>' in page.locator('#reader').inner_text()
        assert '&lt;' not in page.locator('#reader').inner_text()
        checked('USP angle-bracket notation is readable, not escaped twice')
        for width in [320,390,768,1440]:
            page.set_viewport_size({'width':width,'height':900})
            route('home')
            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),f'Home overflow {width}'
            route('chapter/refills-transfer')
            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),f'Chapter overflow {width}'
        page.set_viewport_size({'width':390,'height':844});route('home')
        page.locator('#mobile-menu').click();expect(page.locator('#nav-dialog')).to_be_visible()
        page.keyboard.press('Escape');expect(page.locator('#nav-dialog')).not_to_be_visible()
        page.locator('#mobile-menu').click();page.locator('#mobile-nav [href="#drugs"]').click()
        expect(page.locator('#nav-dialog')).not_to_be_visible()
        expect(page.locator('#drug-query')).to_be_visible()
        route('home');page.screenshot(path=str(out/'home-mobile.png'))
        checked('320/390/768/1440 widths, scrollable tables, mobile dialog and Escape')
        page.set_viewport_size({'width':1440,'height':1000})
        if not args.inline_preview:
            page.reload(wait_until='networkidle')
            state=page.evaluate('(k)=>JSON.parse(localStorage.getItem(k))',KEY)
            assert 'schedule-vi-continuity' in state['saved'] and 'schedule-vi-continuity' in state['read'] and state['font']==19
            # Existing application's storage must not be cleared or rewritten.
            page.evaluate("localStorage.setItem('quiz-isolation-canary','untouched')")
            route('chapter/refills-transfer/schedule-vi-continuity')
            with page.expect_download() as dl:
                page.locator('#export-progress').click()
            path=dl.value.path();exported=json.loads(Path(path).read_text())
            assert exported['application']=='oddments-ultimate-notes'
            page.locator('#progress-file').set_input_files({'name':'notes.json','mimeType':'application/json','buffer':json.dumps(exported).encode()})
            expect(page.locator('#toast')).to_contain_text('가져왔습니다')
            assert page.evaluate("localStorage.getItem('quiz-isolation-canary')")=='untouched'
            prior=page.evaluate('(k)=>localStorage.getItem(k)',KEY)
            page.locator('#progress-file').set_input_files({'name':'invalid.json','mimeType':'application/json','buffer':b'{"application":"other"}'})
            expect(page.locator('#toast')).to_contain_text('가져오기 실패')
            assert json.loads(page.evaluate('(k)=>localStorage.getItem(k)',KEY))['saved']==json.loads(prior)['saved']
            checked('real-origin reload persistence, JSON export/import, invalid import and quiz-storage isolation')
            page.locator('.return-link').click();expect(page.locator('#study-guide-button')).to_be_visible()
            checked('return link preserves main-page navigation')
            nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
            plain=nojs.new_page();plain.goto(base+'notes/book.html',wait_until='load')
            expect(plain.locator('.reading-unit')).to_have_count(306)
            plain.screenshot(path=str(out/'book-mobile.png'))
            assert not plain.evaluate('document.documentElement.scrollWidth>innerWidth+1')
            checked('complete static book works without JavaScript')
            nojs.close()
            # Storage-denied environment: fail soft, still browse and mark locally.
            denied=browser.new_context()
            denied.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Unavailable','SecurityError')}})")
            dp=denied.new_page();dp.goto(base+'notes/',wait_until='load')
            expect(dp.locator('.chapter-card')).to_have_count(33)
            expect(dp.locator('#storage-notice')).to_contain_text('저장소')
            checked('storage-disabled fallback remains readable')
            denied.close()
            broken=browser.new_context()
            broken.route('**/notes/content.js',lambda r:r.abort())
            bp=broken.new_page();bp.goto(base+'notes/',wait_until='load')
            expect(bp.locator('#reader')).to_contain_text('전체 본문과 출처 읽기')
            checked('failed data payload has a visible static-book recovery link')
            broken.close()
        assert not errors,errors
        assert not external,external
        checked('no uncaught JS errors or external runtime network requests')
        ctx.close();browser.close()
    finally:
        if server:server.shutdown()
        (out/'report.json').write_text(json.dumps({'mode':'inline-rendering-only' if args.inline_preview else 'http-browser-regression','checks_passed':checks,'page_errors':errors,'external_requests':external,'untested':['iOS/Android physical devices','independent legal completeness'], 'storage_and_navigation_tested':not args.inline_preview},ensure_ascii=False,indent=2))
    print(f'{len(checks)} checks passed.',flush=True)

if __name__=='__main__':main()
