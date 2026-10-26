#!/usr/bin/env python3
"""Exercise the online practice edition over HTTP; this is not a pharmacy-law audit."""
from __future__ import annotations
import argparse
import functools
import http.server
import json
import os
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright, expect

ROOT=Path(__file__).resolve().parents[1]
KEY='oddments.mpje.practice.v1'

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--site',type=Path,default=ROOT/'public-site')
    ap.add_argument('--base-url',help='Check an already-deployed site instead of loopback.')
    ap.add_argument('--output',type=Path,default=ROOT/'test-results/public-practice')
    args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    data=json.loads((ROOT/'practice_expansion/2026-10-23/candidates/questions.json').read_text())
    by={q['question_id']:q for q in data['questions']}
    server=None
    if args.base_url: base=args.base_url.rstrip('/')+'/'
    else:
        class Quiet(http.server.SimpleHTTPRequestHandler):
            def log_message(self,*args): pass
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(args.site)))
        threading.Thread(target=server.serve_forever,daemon=True).start()
        base=f'http://127.0.0.1:{server.server_port}/'
    checks=[];errors=[]
    def ok(name): checks.append(name);print('PASS:',name,flush=True)
    try:
      with sync_playwright() as p:
        exe=os.environ.get('CHROMIUM_PATH')
        browser=p.chromium.launch(headless=True,**({'executable_path':exe} if exe else {}))
        ctx=browser.new_context(viewport={'width':1440,'height':1000},accept_downloads=True)
        page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(base,wait_until='load')
        expect(page.locator('a[href="practice-expansion/"]')).to_have_count(2)
        page.locator('a[href="practice-expansion/"]').first.click()
        expect(page.locator('#question')).to_be_visible()
        expect(page.locator('#ack')).to_have_count(0)
        expect(page.locator('#practice')).to_be_enabled()
        assert page.evaluate('MPJE_DIAGNOSTICS().status')=='PUBLISHED_PRACTICE'
        ok('main button opens active first question without a draft gate')
        expect(page.locator('.choice')).to_have_count(4)
        page.locator('#check').click();expect(page.locator('#answer-msg')).to_contain_text('먼저')
        q=by[page.evaluate('MPJE_DIAGNOSTICS().active')]
        for a in q['correct_choice_ids']:page.locator('#choice-'+a).check()
        page.locator('#check').click()
        expect(page.locator('#feedback')).to_be_visible()
        expect(page.locator('.rationale')).to_have_count(4)
        expect(page.locator('#answered-count')).to_have_text('1')
        ok('SBA answer validation, Korean explanations and answered counter')
        assert page.locator('#notes a').first.get_attribute('href').startswith('https://woojunxnam.github.io/oddments/notes/#chapter/')
        ok('explanations link to the exact integrated-note section')
        page.locator('#bookmark').click();page.reload()
        expect(page.locator('#bookmark')).to_have_attribute('aria-pressed','true')
        expect(page.locator('#question')).to_be_visible()
        ok('real-origin bookmark and progress persist after reload')
        for value in ('부분','partial','MA-EXP-0003'):
            page.locator('#query').fill(value)
            assert page.evaluate('MPJE_DIAGNOSTICS().filtered')>0
        page.locator('#catalog button').click();q=by['MA-EXP-0003']
        expect(page.locator('input[type=checkbox][name=answer]')).to_have_count(4)
        for a in q['correct_choice_ids']:page.locator('#choice-'+a).check()
        page.locator('#check').click();expect(page.locator('#answer-heading')).to_contain_text('정답과 일치')
        ok('Korean/English/ID search and exact-match SATA scoring')
        page.locator('#query').fill('<img src=x onerror="window.injected=true">')
        assert page.evaluate('MPJE_DIAGNOSTICS().filtered')==0 and not page.evaluate('Boolean(window.injected)')
        ok('search content cannot inject HTML')
        page.locator('#query').fill('');page.locator('#area').select_option('4');page.locator('#qtype').select_option('SATA')
        assert page.evaluate('MPJE_DIAGNOSTICS().filtered')==59
        page.locator('#area').select_option('');page.locator('#qtype').select_option('')
        page.locator('#saved').select_option('bookmarks');assert page.evaluate('MPJE_DIAGNOSTICS().filtered')==1
        page.locator('#saved').select_option('')
        ok('area/type/bookmark filters')
        page.locator('#practice').click();diag=page.evaluate('MPJE_DIAGNOSTICS()')
        assert len(diag['sessionIds'])==20 and len(set(diag['sessionFamilies']))==20
        q=by[diag['active']]
        for a in q['correct_choice_ids']:page.locator('#choice-'+a).check()
        page.locator('#check').click();page.locator('#next').click()
        assert page.evaluate('MPJE_DIAGNOSTICS().active')!=q['question_id']
        page.locator('#end-session').click();expect(page.locator('#summary')).to_be_visible()
        ok('20-question practice uses unique families and a usable result view')
        page.locator('#timed').click();diag=page.evaluate('MPJE_DIAGNOSTICS()')
        assert len(diag['sessionIds'])==120 and len(set(diag['sessionFamilies']))==120
        assert ':' in page.locator('#clock').inner_text()
        for a in by[diag['active']]['correct_choice_ids']:page.locator('#choice-'+a).check()
        page.locator('#check').click();expect(page.locator('#feedback')).to_be_hidden()
        page.locator('#end-session').click();page.locator('#summary button').click()
        expect(page.locator('#feedback')).to_be_visible()
        ok('120-question timed practice defers explanations until review')
        page.locator('#theme').click();expect(page.locator('body')).to_have_class('dark')
        page.locator('#font').click();assert page.locator('#reader').get_attribute('style')
        page.locator('#theme').click();page.locator('#font').click()
        ok('theme and font preferences')
        page.evaluate("localStorage.setItem('existing-quiz-canary','unchanged')")
        with page.expect_download() as dl:page.locator('#export').click()
        saved=Path(dl.value.path()).read_bytes()
        page.locator('#import-file').set_input_files({'name':'progress.json','mimeType':'application/json','buffer':saved})
        expect(page.locator('#storage-msg')).to_contain_text('가져왔')
        page.locator('#import-file').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':b'{"v":1,"bookmarks":["INVALID"],"attempts":{}}'})
        expect(page.locator('#storage-msg')).to_contain_text('실패')
        assert page.evaluate("localStorage.getItem('existing-quiz-canary')")=='unchanged'
        assert page.evaluate('MPJE_DIAGNOSTICS().storageKey')==KEY
        ok('JSON backup/import rejection and storage isolation')
        page.screenshot(path=str(args.output/'desktop.png'))
        for width in (320,390,768,1440):
            page.set_viewport_size({'width':width,'height':1000})
            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),width
            if width==390:
                page.locator('#reader').scroll_into_view_if_needed();page.screenshot(path=str(args.output/'mobile.png'))
        ok('responsive layouts at 320/390/768/1440 pixels')
        ids=list(by)
        rendered=page.evaluate("""ids=>{for(const id of ids){const q=document.querySelector('#query');q.value=id;q.dispatchEvent(new Event('input'));document.querySelector('#catalog button').click();if(MPJE_DIAGNOSTICS().active!==id||document.querySelectorAll('.choice').length!==4)throw Error(id);}return ids.length;}""",ids)
        assert rendered==1024
        page.set_viewport_size({'width':320,'height':1000})
        maximum=page.evaluate("""ids=>{let max=0;for(const id of ids){const q=document.querySelector('#query');q.value=id;q.dispatchEvent(new Event('input'));document.querySelector('#catalog button').click();max=Math.max(max,document.documentElement.scrollWidth-innerWidth);}return max;}""",ids)
        assert maximum<=1,maximum
        ok('all 1024 questions render and fit the narrowest mobile viewport')
        page.goto(base+'practice-expansion/#MA-EXP-0512');expect(page.locator('#q-meta')).to_contain_text('MA-EXP-0512')
        page.locator('#controls-link').click();expect(page.locator('#query')).to_be_focused()
        ok('deep links and mobile settings navigation')
        denied=browser.new_context();denied.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked')}})")
        dp=denied.new_page();dp.goto(base+'practice-expansion/')
        expect(dp.locator('#question')).to_be_visible();dp.locator('#bookmark').click()
        expect(dp.locator('#storage-msg')).to_contain_text('차단');denied.close()
        ok('questions remain usable when browser storage is disabled')
        page.locator('#return-main').click();expect(page.locator('#study-guide-button')).to_be_visible()
        ok('return to original question bank')
        assert not errors,errors
        ok('no uncaught JavaScript errors')
        browser.close()
    finally:
        if server:server.shutdown()
        (args.output/'report.json').write_text(json.dumps({'checks':checks,'passed':len(checks),'page_errors':errors,'environment':'production HTTP' if args.base_url else 'loopback HTTP','legal_review':False,'physical_device_testing':False},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
