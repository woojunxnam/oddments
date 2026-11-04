#!/usr/bin/env python3
"""Exercise the refresh experience and shared navigation. No legal/clinical audit.

Default: actual HTTP/real-origin storage. --inline-preview: constrained-runtime DOM
checks with explicitly simulated storage; navigation/reload checks are skipped.
"""
from __future__ import annotations
import argparse
from functools import partial
import http.server
import json
from pathlib import Path
import re
import threading
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parents[1]
KEY='oddments.mpje.refresh.v1'


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--site',type=Path,default=ROOT/'site');ap.add_argument('--inline-preview',action='store_true');ap.add_argument('--executable-path');ap.add_argument('--output',type=Path,default=ROOT/'test-results/refresh');a=ap.parse_args()
    out=a.output;out.mkdir(parents=True,exist_ok=True)
    checks=[];errors=[];server=None
    def passed(text):checks.append(text);print('PASS:',text,flush=True)
    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    if not a.inline_preview:
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(a.site)))
        threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
    else:base='https://refresh-preview.invalid/'
    try:
      with sync_playwright() as pw:
        launch={'headless':True}
        if a.executable_path:launch['executable_path']=a.executable_path
        browser=pw.chromium.launch(**launch);ctx=browser.new_context(viewport={'width':1440,'height':1000},accept_downloads=True)
        page=ctx.new_page();page.on('pageerror',lambda err:errors.append(str(err)))
        def inline_load(target,blocked=False):
            markup=(a.site/'notes/index.html').read_text()
            markup=re.sub(r'<script[^>]*src="[^"]+"[^>]*></script>','',markup)
            markup=re.sub(r'<link[^>]+rel="stylesheet"[^>]*>','',markup)
            markup=markup.replace('<head>','<head><base href="https://refresh-preview.invalid/">')
            target.set_content(markup)
            if not blocked:
                target.evaluate("""()=>{const data={};Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>data[k]??null,setItem:(k,v)=>{data[k]=String(v)},removeItem:k=>{delete data[k]}}});}""")
            else:target.evaluate("()=>Object.defineProperty(window,'localStorage',{configurable:true,get(){throw new Error('Blocked test storage')}})")
            for name in ['notes/notes.css','notes/refresh.css','assets/learning-tools.css']:target.add_style_tag(content=(a.site/name).read_text())
            for name in ['notes/content.js','notes/refresh-data.js','notes/refresh-core.js','notes/refresh.js','notes/notes.js','assets/learning-tools.js']:target.add_script_tag(content=(a.site/name).read_text())
        if a.inline_preview:inline_load(page)
        else:page.goto(base+'notes/',wait_until='networkidle')
        def route(path):
            page.evaluate('(x)=>{location.hash=x}',path);page.wait_for_timeout(70)
        expect(page.locator('#refresh-home .rf-home')).to_be_visible()
        first=page.locator('.rf-home-title').inner_text();page.locator('#rf-home-next').click();assert page.locator('.rf-home-title').inner_text()!=first
        passed('notes home has a working non-repeating quick-info refresher')
        notes_before='{"version":1,"read":["legal-reasoning"],"saved":[],"font":18,"theme":"system","focus":false,"last":null}'
        page.evaluate('(s)=>{localStorage.setItem("oddments.mpje.ultimate-notes.v1",s);localStorage.setItem("oddments.mpje.practice.v1","{\\"sentinel\\":true}");}',notes_before)
        route('refresh/card/RF-001');expect(page.locator('.rf-card')).to_have_attribute('data-card-id','RF-001')
        expect(page.locator('#rf-answer')).to_be_visible();expect(page.locator('#rf-card')).to_contain_text('RA')
        passed('curated card shows concise explanation, example, boundary and note link')
        page.locator('#rf-recall').check();expect(page.locator('#rf-answer')).to_be_hidden();expect(page.locator('[data-grade=good]')).to_be_disabled()
        page.locator('#rf-reveal').click();expect(page.locator('#rf-answer')).to_be_visible();page.locator('[data-grade=hard]').click()
        r=page.evaluate('(key)=>JSON.parse(localStorage.getItem(key)).reviews["RF-001"]',KEY);assert r['grade']=='hard' and r['count']==1
        expect(page.locator('[data-grade=hard]')).to_be_disabled()
        passed('optional recall hides content until reveal and prevents duplicate self-rating')
        page.locator('#rf-save').click();expect(page.locator('#rf-save')).to_have_attribute('aria-pressed','true')
        assert page.evaluate('localStorage.getItem("oddments.mpje.ultimate-notes.v1")')==notes_before
        assert page.evaluate('localStorage.getItem("oddments.mpje.practice.v1")')=='{"sentinel":true}'
        passed('refresh state leaves existing notes and practice storage untouched')
        if not a.inline_preview:
            page.reload(wait_until='networkidle');expect(page.locator('#rf-save')).to_have_attribute('aria-pressed','true');assert page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).reviews["RF-001"].count',KEY)==1
            passed('real-origin card bookmark and review schedule persist after reload')
        page.locator('#rf-recall').uncheck()
        route('refresh/today');expect(page.locator('[data-mode=today]')).to_have_attribute('aria-pressed','true')
        daily=page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).daily',KEY);assert len(daily['ids'])==10 and len(set(daily['ids']))==10
        used=[]
        for i in range(10):
            cid=page.locator('.rf-card').get_attribute('data-card-id');used.append(cid);page.locator('[data-grade=good]').click();page.locator('#rf-next').click()
        assert used==daily['ids'];expect(page.locator('.rf-empty')).to_contain_text('이번 묶음')
        assert len(page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).daily.completed',KEY))==10
        passed('ten-card daily set is stable, unique, completable and does not count skips')
        route('refresh/path/product');expect(page.locator('.rf-card')).to_have_attribute('data-card-id','RF-013');page.locator('#rf-next').click();expect(page.locator('.rf-card')).to_have_attribute('data-card-id','RF-014')
        passed('return-to-practice steps use authored order rather than random repetition')
        route('refresh/topic/refills-transfer');expect(page.locator('#rf-topic')).to_have_value('refills-transfer')
        assert page.locator('.rf-card').count()==1
        route('refresh');page.locator('[data-mode=random]').click();page.locator('.rf-filters summary').click();page.locator('#rf-deck').select_option('drugs');page.locator('#rf-query').fill('Adderall')
        expect(page.locator('#rf-card')).to_contain_text('Adderall');expect(page.locator('#rf-card')).to_contain_text('기존 약물 부록')
        page.locator('#rf-query').fill('<img src=x onerror=alert(1)>');expect(page.locator('.rf-empty')).to_be_visible();expect(page.locator('#reader img')).to_have_count(0)
        passed('chapter/drug/search filters work and search input cannot inject markup')
        page.locator('#rf-reset').click();seen=[]
        for _ in range(20):seen.append(page.locator('.rf-card').get_attribute('data-card-id'));page.locator('#rf-next').click()
        assert len(set(seen))==20
        passed('random refresh avoids repeats before exhausting the eligible deck')
        route('refresh/card/RF-040');expect(page.locator('.rf-warning-row')).to_contain_text('OPEN');expect(page.locator('#rf-card')).to_contain_text('14일')
        route('refresh/card/RF-062');expect(page.locator('.rf-warning-row')).to_contain_text('시행일')
        passed('unresolved law and date-sensitive cards retain prominent warnings')
        route('refresh/card/RF-026');expect(page.locator('.rf-provenance')).to_contain_text('추가 안전교육 확인 2026-10-27')
        page.locator('.rf-sources>summary').click();expect(page.locator('a[href*="ahrq.gov/health-literacy/improve/precautions/tool5.html"]')).to_have_count(1)
        passed('fresh safety references and inherited note review dates are separate')
        route('glossary');expect(page.locator('.rf-term')).to_have_count(45);page.locator('#rf-term-search').fill('BUD');expect(page.locator('.rf-term')).to_have_count(1)
        page.locator('#rf-term-search').fill('refill');expect(page.locator('.rf-term').first).to_contain_text('Refill');page.locator('#rf-term-search').fill('<svg onload=alert(1)>');expect(page.locator('#rf-terms svg')).to_have_count(0)
        passed('45 plain-language terms support Korean/English search and linked source reading')
        route('return');expect(page.locator('.rf-path-card')).to_have_count(7);page.locator('[data-field=license]').check()
        assert 'license' in page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).field',KEY)
        expect(page.locator('.rf-field')).to_contain_text('고용주 승인')
        page.evaluate('scrollTo(0,0)');page.wait_for_timeout(150)
        page.screenshot(path=str(out/'return-path-desktop.png'),full_page=True)
        passed('seven-step return path and explicitly non-certifying onsite checklist work')
        route('refresh/card/RF-001');page.locator('.rf-method>summary').click()
        with page.expect_download() as down:page.locator('#rf-export').click()
        dest=out/'progress-export.json';down.value.save_as(dest);exported=json.loads(dest.read_text());assert exported['application']=='oddments-refresh' and 'RF-001' in exported['saved']
        old=page.evaluate('(k)=>localStorage.getItem(k)',KEY)
        page.locator('#rf-file').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':b'{"application":"wrong"}'})
        expect(page.locator('#rf-status')).to_contain_text('가져오기 실패');assert page.evaluate('(k)=>localStorage.getItem(k)',KEY)==old
        page.locator('#rf-file').set_input_files({'name':'safe.json','mimeType':'application/json','buffer':json.dumps({'application':'oddments-refresh','version':1,'saved':['RF-002'],'reviews':{},'field':[]}).encode()})
        expect(page.locator('#rf-status')).to_contain_text('합쳤습니다');saved=page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).saved',KEY);assert {'RF-001','RF-002'}<=set(saved)
        passed('backup download, malformed-import rejection and non-destructive merging work')
        route('refresh/card/RF-013');page.locator('#rf-larger').click();expect(page.locator('#rf-shell')).to_have_attribute('style',re.compile('19px'))
        page.locator('#theme-button').click();page.locator('#theme-button').click();expect(page.locator('html')).to_have_attribute('data-theme','dark')
        page.evaluate('scrollTo(0,0)');page.wait_for_timeout(150)
        page.screenshot(path=str(out/'card-desktop-dark.png'))
        page.locator('#theme-button').click()
        for width in [320,390,768,1440]:
            page.set_viewport_size({'width':width,'height':880});page.wait_for_timeout(60)
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),width
        passed('card text-size/theme controls and 320/390/768/1440 responsive layouts work')
        page.set_viewport_size({'width':390,'height':844});page.evaluate("scrollTo(0,document.querySelector('#rf-card').getBoundingClientRect().top+scrollY-90)");page.wait_for_timeout(150);page.screenshot(path=str(out/'card-mobile.png'))
        expect(page.locator('#om-tools-toggle')).to_be_visible();page.locator('#om-tools-toggle').click();expect(page.locator('#om-to-top')).to_be_visible();page.keyboard.press('Escape');expect(page.locator('#om-tools-menu')).to_be_hidden()
        passed('mobile side navigation expands, closes with Escape and remains touch-accessible')
        page.set_viewport_size({'width':1440,'height':1000});page.evaluate('scrollTo(0,800)');oldhash=page.evaluate('location.hash');page.locator('#om-to-top').click();page.wait_for_function('scrollY < 5');assert page.evaluate('location.hash')==oldhash
        passed('back-to-top preserves notes route/card ID rather than overwriting the hash')
        page.set_viewport_size({'width':320,'height':880})
        failures=page.evaluate("""async()=>{let fails=[];for(const c of MPJE_REFRESH.cards){location.hash='refresh/card/'+c.id;await new Promise(r=>setTimeout(r,8));const el=document.querySelector('.rf-card');if(!el||el.dataset.cardId!==c.id||document.documentElement.scrollWidth>innerWidth)fails.push(c.id);}return fails;}""")
        assert not failures,failures
        passed('all 232 cards render with no horizontal overflow at 320px')
        if not a.inline_preview:
            page.set_viewport_size({'width':1440,'height':1000})
            for path in ['', 'notes/','notes/book.html','practice-expansion/','practice-expansion/research.html']:
                page.goto(base+path,wait_until='networkidle');expect(page.locator('#oddments-tools')).to_have_count(1);expect(page.locator('#om-home')).to_have_attribute('href',base);expect(page.locator('#om-cards')).to_have_attribute('href',base+'notes/#refresh')
                oldhash=page.evaluate('location.hash');page.evaluate('scrollTo(0,1200)');page.locator('#om-to-top').click();page.wait_for_function('scrollY < 5');assert page.evaluate('location.hash')==oldhash
            page.goto(base,wait_until='networkidle');page.locator('a[href="notes/#refresh"]').first.click();expect(page.locator('.rf-card')).to_be_visible()
            passed('all five published pages have exactly one working dock and main-page flashcard entry')
            page.goto(base+'notes/#chapter/refills-transfer',wait_until='networkidle');page.locator('a[href="#refresh/topic/refills-transfer"]').click();expect(page.locator('#rf-topic')).to_have_value('refills-transfer')
            passed('full chapter → related cards navigation works over real HTTP')
        blocked=browser.new_context(viewport={'width':390,'height':844});blocked.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('Blocked test storage')}})")
        bp=blocked.new_page();bp.on('pageerror',lambda err:errors.append(str(err)))
        if a.inline_preview:inline_load(bp,True);bp.evaluate("location.hash='refresh'");bp.wait_for_timeout(100)
        else:bp.goto(base+'notes/#refresh',wait_until='networkidle')
        expect(bp.locator('.rf-card')).to_be_visible();bp.locator('#rf-next').click();expect(bp.locator('.rf-card')).to_be_visible();bp.locator('.rf-method>summary').click();expect(bp.locator('#rf-storage')).to_be_visible()
        passed('blocked storage degrades to in-session learning with an explicit export notice')
        assert not errors,errors
        passed('no uncaught JavaScript errors')
        browser.close()
    finally:
        if server:server.shutdown();server.server_close()
        report={'mode':'INLINE_PREVIEW_SIMULATED_STORAGE' if a.inline_preview else 'REAL_HTTP_REAL_ORIGIN_STORAGE','passed_checks':checks,'count':len(checks),'errors':errors,'legal_audit':False}
        (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'mode':report['mode'],'checks':len(checks),'errors':len(errors)},ensure_ascii=False))

if __name__=='__main__':main()
