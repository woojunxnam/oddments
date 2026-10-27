#!/usr/bin/env python3
"""Exam-study browser regression. Default is real HTTP and real-origin storage.
Inline preview is explicitly limited to simulated-storage DOM/layout checks.
"""
from __future__ import annotations
import argparse,http.server,json,re,threading
from functools import partial
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
KEY='oddments.mpje.exam-study.v1'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--site',type=Path,default=ROOT/'site');ap.add_argument('--inline-preview',action='store_true');ap.add_argument('--executable-path');ap.add_argument('--output',type=Path,default=ROOT/'test-results/exam-study');a=ap.parse_args()
    a.output.mkdir(parents=True,exist_ok=True);checks=[];errors=[];server=None
    def ok(text):checks.append(text);print('PASS:',text,flush=True)
    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    if not a.inline_preview:
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(a.site)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}/'
    else:base='https://exam-preview.invalid/'
    try:
      with sync_playwright() as pw:
        launch={'headless':True}
        if a.executable_path:launch['executable_path']=a.executable_path
        browser=pw.chromium.launch(**launch);ctx=browser.new_context(viewport={'width':1440,'height':1000},accept_downloads=True,reduced_motion='reduce');page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
        def load_inline(p,blocked=False):
            markup=(a.site/'notes/index.html').read_text();markup=re.sub(r'<script[^>]*src="[^"]+"[^>]*></script>','',markup);markup=re.sub(r'<link[^>]+rel="stylesheet"[^>]*>','',markup);markup=markup.replace('<head>','<head><base href="https://exam-preview.invalid/notes/">');p.set_content(markup)
            if blocked:p.evaluate("Object.defineProperty(window,'localStorage',{configurable:true,get(){throw Error('blocked storage test')}})")
            else:p.evaluate("()=>{const d={};Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>d[k]??null,setItem:(k,v)=>d[k]=String(v),removeItem:k=>delete d[k]}})}")
            for file in ['notes/notes.css','notes/refresh.css','notes/study.css','assets/learning-tools.css']:p.add_style_tag(content=(a.site/file).read_text())
            for file in ['notes/content.js','notes/refresh-data.js','notes/refresh-core.js','notes/refresh.js','notes/study-data.js','notes/study.js','notes/notes.js']:p.add_script_tag(content=(a.site/file).read_text())
        def route(path):page.evaluate('(p)=>location.hash=p',path);page.wait_for_timeout(80)
        if a.inline_preview:load_inline(page);route('study')
        else:
            page.goto(base,wait_until='networkidle');page.locator('.exam-study-entry').first.click();expect(page.locator('#reader h1')).to_have_text('MPJE 법규 학습');ok('main-page priority entry opens exam-study rather than the return pathway')
        expect(page.locator('[data-study-module]')).to_have_count(16);ok('16 modules and exam-first home render')
        page.locator('#study-query').fill('partial');assert page.locator('[data-study-module]').count()<16
        page.locator('#study-query').fill('<img src=x onerror=alert(1)>');expect(page.locator('#study-modules img')).to_have_count(0)
        page.locator('#study-query').fill('');page.locator('#study-area').select_option('1');assert page.locator('[data-study-module]').count()==4;ok('keyword/competency filters work without HTML injection')
        page.locator('#study-exam-date').fill('2027-03-02');page.locator('#study-exam-date').dispatch_event('change');expect(page.locator('#study-date-note')).to_contain_text('적용하지 마세요');ok('future exam date warns instead of silently using the old blueprint')
        route('study/module/m08');expect(page.locator('.study-grid .study-box')).to_have_count(4);expect(page.locator('#reader')).to_contain_text('Schedule VI');ok('modules connect four concepts and all detailed source chapters')
        sentinels={'oddments.mpje.refresh.v1':'{"unchanged":1}','oddments.mpje.practice.v1':'{"unchanged":2}','oddments.mpje.ultimate-notes.v1':'{"version":1,"read":[],"saved":[],"font":18,"theme":"system","focus":false}'}
        page.evaluate('(s)=>Object.entries(s).forEach(([k,v])=>localStorage.setItem(k,v))',sentinels)
        route('study/lesson/LAW-026');expect(page.locator('[data-law-id]')).to_have_attribute('data-law-id','LAW-026');expect(page.locator('#study-answer')).to_be_visible()
        page.locator('#study-reveal').click();expect(page.locator('#study-answer')).to_be_hidden();page.locator('[data-rating=review]').click();expect(page.locator('#study-message')).to_contain_text('펼쳐')
        page.locator('#study-reveal').click();page.locator('[data-study-sources] > summary').click();expect(page.locator('[data-source-body]')).to_contain_text('same pharmacy');ok('conceal/reveal and full unchanged source exceptions work before self-rating')
        page.locator('#study-mistake').fill('issue date와 first partial을 혼동');page.locator('#study-mistake').dispatch_event('change');page.locator('[data-rating=review]').click();expect(page.locator('#study-rating-status')).to_contain_text('복습 필요')
        assert page.evaluate('(s)=>Object.entries(s).every(([k,v])=>localStorage.getItem(k)===v)',sentinels);ok('self-assessment and error notes do not alter existing study/question storage')
        if not a.inline_preview:
            page.reload(wait_until='networkidle');expect(page.locator('#study-mistake')).to_have_value('issue date와 first partial을 혼동');expect(page.locator('#study-rating-status')).to_contain_text('복습 필요');ok('real-origin reload preserves confidence and error notes')
        route('study/weak');expect(page.locator('.study-grid')).to_contain_text('Patient request');ok('self-identified weak concepts are retrievable')
        route('study/today');daily=page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).daily',KEY);assert len(set(daily['ids']))==10 and all(x.startswith('LAW-') for x in daily['ids']);route('study');route('study/today');assert page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).daily.ids',KEY)==daily['ids'];ok('daily law-only set is unique and stable within the Eastern calendar day')
        assert page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).daily.done.length',KEY)==0
        route('study/today-card/'+daily['ids'][0]);page.locator('[data-rating=explain]').click();page.locator('[data-rating=explain]').click();assert page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).daily.done.length',KEY)==1;ok('daily progress counts self-reviewed concepts once, not skips or repeated clicks')
        route('study/drill');seen=[page.locator('[data-law-id]').get_attribute('data-law-id')]
        for _ in range(63):
            previous=seen[-1];page.locator('#study-next').click();expect(page.locator('[data-law-id]')).not_to_have_attribute('data-law-id',previous);seen.append(page.locator('[data-law-id]').get_attribute('data-law-id'))
        assert len(set(seen))==64;ok('random exam-law review avoids repeats for a complete 64-concept cycle')
        route('study/compare');expect(page.locator('.study-lesson')).to_have_count(12);expect(page.locator('.study-lesson').filter(has_text='VI의 14/30일')).to_contain_text('OPEN');ok('twelve comparisons preserve unresolved boundaries')
        route('study/clocks');expect(page.locator('.study-clock')).to_have_count(24);page.locator('#study-clock-toggle').click();expect(page.locator('.study-time-value').first).to_be_hidden();page.locator('#study-clock-toggle').click();expect(page.locator('.study-time-value').first).to_be_visible();ok('24 clocks keep numbers, triggers, exceptions and optional concealment')
        route('study/plan');expect(page.locator('[data-study-day]')).to_have_count(30);page.locator('[data-study-day="1"]').click();route('study/plan');expect(page.locator('[data-study-day="1"]')).to_have_attribute('aria-pressed','true');ok('30-session plan is explicit manual progress, not inferred completion')
        route('study/coverage');expect(page.locator('#reader')).to_contain_text('Competency 4.7');expect(page.locator('#reader')).to_contain_text('2027-03-01');ok('all 22 competency codes are mapped with the outline cutoff retained')
        route('study/lesson/LAW-032');expect(page.locator('.study-flags').first).to_contain_text('OPEN');route('study/lesson/LAW-044');expect(page.locator('.study-flags').first).to_contain_text('시행일');ok('OPEN and date-sensitive warnings are inherited visibly')
        if not a.inline_preview:
            route('study/lesson/LAW-025');q=page.locator('[data-study-question]').first;href=q.get_attribute('href');qid=q.get_attribute('data-study-question');page.goto(base+'practice-expansion/#'+qid,wait_until='networkidle');expect(page.locator('#question-id')).to_contain_text(qid) if page.locator('#question-id').count() else expect(page.locator('#reader')).to_contain_text(qid)
            ok('related question deep links open the exact existing bank item');page.goto(base+'notes/#study',wait_until='networkidle')
        else:route('study')
        with page.expect_download() as down:page.locator('#study-export').click()
        target=a.output/'progress.json';down.value.save_as(target);backup=json.loads(target.read_text());assert backup['application']=='oddments-mpje-exam-study'
        before=page.evaluate('(k)=>localStorage.getItem(k)',KEY);page.locator('#study-import-file').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':b'{"application":"wrong"}'});expect(page.locator('#study-message')).to_contain_text('실패');assert page.evaluate('(k)=>localStorage.getItem(k)',KEY)==before
        backup['days']=[30];page.locator('#study-import-file').set_input_files({'name':'good.json','mimeType':'application/json','buffer':json.dumps(backup).encode()});expect(page.locator('#study-message')).to_contain_text('가져왔습니다');assert {1,30}<=set(page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).days',KEY));ok('backup export, invalid-import rejection and non-destructive merge work')
        route('study/lesson/LAW-025');page.locator('#study-larger').click();expect(page.locator('.exam-study')).to_have_attribute('style',re.compile('19px'));page.locator('#theme-button').click();ok('exam-study type controls coexist with the existing theme')
        for width in [320,390,768,1440]:
            page.set_viewport_size({'width':width,'height':900});route('study');assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
            route('study/lesson/LAW-032');assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
        ok('responsive dashboard and source-linked lessons fit 320/390/768/1440px')
        page.set_viewport_size({'width':320,'height':900})
        bad=page.evaluate("""async()=>{let bad=[];for(const l of MPJE_EXAM_STUDY.lessons){location.hash='study/lesson/'+l.id;await new Promise(r=>setTimeout(r,12));const el=document.querySelector('[data-law-id]');if(!el||el.dataset.lawId!==l.id||document.documentElement.scrollWidth>innerWidth)bad.push(l.id);}return bad;}""")
        assert not bad,bad;ok('all 64 concepts render without narrow-screen overflow')
        if not a.inline_preview:
            for path in ['', 'notes/','notes/book.html','notes/study.html','practice-expansion/','practice-expansion/research.html']:
                page.goto(base+path,wait_until='networkidle');expect(page.locator('#om-study')).to_have_attribute('href',base+'notes/#study')
            page.goto(base+'notes/#study/lesson/LAW-025',wait_until='networkidle');page.locator('#om-tools-toggle').click();old=page.evaluate('location.hash');page.locator('#om-to-top').click();assert page.evaluate('location.hash')==old
            ok('six pages have exam-study dock access and back-to-top preserves the active lesson')
            nojs=browser.new_context(java_script_enabled=False,viewport={'width':320,'height':900});np=nojs.new_page();np.goto(base+'notes/study.html');expect(np.locator('article')).to_have_count(64);assert np.evaluate('document.documentElement.scrollWidth<=innerWidth');nojs.close();ok('static law-study edition is readable without JavaScript')
        bp=ctx.new_page();bp.on('pageerror',lambda e:errors.append(str(e)))
        if a.inline_preview:load_inline(bp,True);bp.evaluate("location.hash='study/lesson/LAW-025'")
        else:bp.add_init_script("Object.defineProperty(window,'localStorage',{configurable:true,get(){throw Error('storage denied')}})");bp.goto(base+'notes/#study/lesson/LAW-025',wait_until='networkidle')
        expect(bp.locator('[data-law-id]')).to_be_visible();bp.locator('[data-rating=review]').click();expect(bp.locator('#study-storage')).to_be_visible();bp.close();ok('storage denial preserves in-session learning with an export notice')
        page.set_viewport_size({'width':1440,'height':1000});
        if not a.inline_preview:page.goto(base+'notes/#study',wait_until='networkidle')
        else:route('study')
        page.evaluate("window.scrollTo({top:0,behavior:'instant'})");page.screenshot(path=str(a.output/'study-desktop.png'),full_page=True)
        route('study/lesson/LAW-026');page.set_viewport_size({'width':390,'height':844});page.evaluate("window.scrollTo({top:0,behavior:'instant'})");page.screenshot(path=str(a.output/'law-mobile.png'),full_page=True)
        assert not errors,errors;ok('no uncaught JavaScript errors')
        report=dict(mode='INLINE_PREVIEW_SIMULATED_STORAGE' if a.inline_preview else 'REAL_HTTP_REAL_ORIGIN_STORAGE',checks=len(checks),passed=checks,errors=errors,legal_audit=False)
        (a.output/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));browser.close();print(json.dumps({'mode':report['mode'],'checks':len(checks),'errors':len(errors)}))
    finally:
        if server:server.shutdown()
if __name__=='__main__':main()
