#!/usr/bin/env python3
"""Exercise the LOCAL draft reader in Chromium. Not production deployment validation."""
from __future__ import annotations
import functools, http.server, json, os, threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/browser';OUT.mkdir(exist_ok=True)
D=json.loads((ROOT/'candidates/questions.json').read_text());by={q['question_id']:q for q in D['questions']}
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start();url=f'http://127.0.0.1:{server.server_port}/review/practice-lab.html'
passes=[];errors=[]
def ok(name):passes.append(name);print('PASS',name)
try:
 with sync_playwright() as p:
  exe=os.environ.get('CHROMIUM_PATH')
  if not exe and Path('/usr/bin/chromium').is_file():exe='/usr/bin/chromium'
  browser=p.chromium.launch(headless=True,executable_path=exe,args=['--no-sandbox'])
  ctx=browser.new_context(viewport={'width':1440,'height':1100},accept_downloads=True)
  page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
  harness=os.environ.get('DOM_HARNESS')=='1'
  saved={}
  def load(pg, storage=None):
   if not harness:pg.goto(url);return
   pg.goto('about:blank')
   pg.evaluate('''(seed)=>{const mem={...seed};Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>Object.prototype.hasOwnProperty.call(mem,k)?mem[k]:null,setItem:(k,v)=>{mem[k]=String(v)},removeItem:k=>{delete mem[k]},clear:()=>{for(const k of Object.keys(mem))delete mem[k]},key:i=>Object.keys(mem)[i]??null,get length(){return Object.keys(mem).length}}});window.__testStore=mem;}''',storage or {})
   pg.set_content((ROOT/'review/practice-lab.html').read_text(),wait_until='load')
  load(page)
  assert page.locator('#question').is_hidden() and page.locator('#practice').is_disabled();ok('draft acknowledgement blocks question access')
  page.locator('#ack').check();assert page.locator('#question').is_visible();assert page.locator('.choice').count()==4;ok('English cases and four choices load')
  page.locator('#check').click();assert '먼저' in page.locator('#answer-msg').inner_text();ok('empty answer rejected')
  q=by[page.evaluate('MPJE_DIAGNOSTICS().active')]
  for a in q['correct_choice_ids']:page.locator('#choice-'+a).check()
  page.locator('#check').click();assert page.locator('#feedback').is_visible() and page.locator('.rationale').count()==4;ok('SBA scoring and four Korean choice rationales')
  assert page.locator('#notes a').first.get_attribute('href').startswith('https://woojunxnam.github.io/oddments/notes/#chapter/');ok('deep links to exact integrated-note units')
  page.locator('#bookmark').click();assert page.locator('#bookmark').get_attribute('aria-pressed')=='true'
  if harness:
   saved=page.evaluate('window.__testStore');page.close();page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));load(page,saved)
  else:page.reload()
  page.locator('#ack').check();assert page.locator('#bookmark').get_attribute('aria-pressed')=='true';ok('bookmark restore via mocked storage across document replacement' if harness else 'bookmark survives HTTP-origin reload')
  page.locator('#query').fill('부분');assert page.evaluate('MPJE_DIAGNOSTICS().filtered')>0
  page.locator('#query').fill('partial');assert page.evaluate('MPJE_DIAGNOSTICS().filtered')>0
  page.locator('#query').fill('MA-EXP-0003');assert page.evaluate('MPJE_DIAGNOSTICS().filtered')==1;ok('Korean, English and exact-ID search')
  page.locator('#catalog button').click();q=by['MA-EXP-0003'];assert page.locator('input[type=checkbox][name=answer]').count()==4
  for a in q['correct_choice_ids']:page.locator('#choice-'+a).check()
  page.locator('#check').click();assert '일치' in page.locator('#answer-heading').inner_text();ok('SATA answer mapping and exact-match scoring')
  page.locator('#query').fill('<img src=x onerror="window.injected=true">');assert page.evaluate('MPJE_DIAGNOSTICS().filtered')==0 and not page.evaluate('Boolean(window.injected)');ok('search query is not interpreted as HTML')
  page.locator('#query').fill('');page.locator('#area').select_option('4');page.locator('#qtype').select_option('SATA');assert page.evaluate('MPJE_DIAGNOSTICS().filtered')==59;ok('area and type combined filtering')
  page.locator('#area').select_option('');page.locator('#qtype').select_option('');page.locator('#saved').select_option('bookmarks');assert page.evaluate('MPJE_DIAGNOSTICS().filtered')==1;ok('saved-only filter')
  page.locator('#saved').select_option('');page.locator('#practice').click();diag=page.evaluate('MPJE_DIAGNOSTICS()');assert len(diag['sessionIds'])==20 and len(set(diag['sessionFamilies']))==20;ok('20-item practice has one question per family')
  q=by[diag['active']];page.locator('#choice-'+q['correct_choice_ids'][0]).check();page.locator('#check').click();page.locator('#next').click();assert page.evaluate('MPJE_DIAGNOSTICS().active')!=q['question_id'];page.locator('#end-session').click();assert page.locator('#summary').is_visible();ok('session navigation and partial-session summary')
  page.locator('#timed').click();diag=page.evaluate('MPJE_DIAGNOSTICS()');assert len(diag['sessionIds'])==120 and len(set(diag['sessionFamilies']))==120 and ':' in page.locator('#clock').inner_text();q=by[diag['active']]
  for a in q['correct_choice_ids']:page.locator('#choice-'+a).check()
  page.locator('#check').click();assert page.locator('#feedback').is_hidden();ok('120-item nonadaptive timed drill with deferred feedback')
  page.locator('#end-session').click();page.locator('#summary button').click();assert page.locator('#feedback').is_visible();ok('submitted response can be reviewed after timed session')
  page.locator('#theme').click();assert page.locator('body').get_attribute('class')=='dark';page.locator('#font').click();assert page.locator('#reader').get_attribute('style');page.locator('#theme').click();page.locator('#font').click();ok('theme and text-size preferences')
  with page.expect_download() as dl:page.locator('#export').click()
  dl.value.save_as(str(OUT/'test-progress.json'))
  page.locator('#import-file').set_input_files(str(OUT/'test-progress.json'));page.wait_for_function("document.querySelector('#storage-msg').textContent.includes('가져왔')");assert '가져왔' in page.locator('#storage-msg').inner_text();ok('progress export and valid import')
  bad=OUT/'invalid-progress.json';bad.write_text('{"v":1,"bookmarks":["INVALID"],"attempts":{}}')
  page.locator('#import-file').set_input_files(str(bad));page.wait_for_function("document.querySelector('#storage-msg').textContent.includes('실패')");assert '실패' in page.locator('#storage-msg').inner_text();ok('invalid progress import rejected')
  assert page.evaluate("Array.from({length:localStorage.length},(_,i)=>localStorage.key(i)).every(k=>k==='oddments.mpje.expansion.draft1')");ok('storage isolated from existing quiz and notes keys')
  page.screenshot(path=str(OUT/'desktop.png'),full_page=False)
  for w in [320,390,768,1440]:
   page.set_viewport_size({'width':w,'height':1000});assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+1'),w
   if w==390:
    page.locator('#reader').scroll_into_view_if_needed();page.screenshot(path=str(OUT/'mobile.png'),full_page=False)
  ok('no horizontal overflow at 320, 390, 768 and 1440 pixels')
  # Confirm all 1,024 payload records can render; sampling based on a payload count alone is insufficient.
  page.set_viewport_size({'width':1440,'height':1000})
  rendered=page.evaluate("""(ids)=>{let n=0;for(const id of ids){const x=document.querySelector('#query');x.value=id;x.dispatchEvent(new Event('input'));const b=document.querySelector('#catalog button');if(!b)throw Error('Missing '+id);b.click();if(MPJE_DIAGNOSTICS().active!==id||document.querySelectorAll('#choices .choice').length!==4)throw Error('Render '+id);n++;}return n;}""",[q['question_id'] for q in D['questions']])
  assert rendered==1024
  page.set_viewport_size({'width':320,'height':1000})
  worst=page.evaluate("""(ids)=>{let worst=0,bad='';for(const id of ids){const x=document.querySelector('#query');x.value=id;x.dispatchEvent(new Event('input'));document.querySelector('#catalog button').click();const over=document.documentElement.scrollWidth-innerWidth;if(over>worst){worst=over;bad=id;}}return {worst,bad};}""",[q['question_id'] for q in D['questions']])
  assert worst['worst']<=1,worst
  page.set_viewport_size({'width':1440,'height':1000})
  ok('all 1,024 question views fit a 320-pixel viewport')
  ok('all 1,024 materialized questions render')
  page.close();page=ctx.new_page();load(page);page.keyboard.press('Tab');assert page.locator('.skip').evaluate('(e)=>e===document.activeElement');ok('keyboard skip link reachable')
  off=browser.new_context();op=off.new_page();op.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked')}})");
  if harness:
   op.goto('about:blank');op.set_content((ROOT/'review/practice-lab.html').read_text(),wait_until='load')
  else:op.goto(url)
  op.locator('#ack').check();op.locator('#bookmark').click();assert '차단' in op.locator('#storage-msg').inner_text();off.close();ok('storage-disabled fallback remains usable')
  if not harness:
   filepage=ctx.new_page();filepage.goto((ROOT/'review/practice-lab.html').as_uri());filepage.locator('#ack').check();assert filepage.locator('.choice').count()==4;ok('standalone file URL loads without a server')
  assert not errors,errors;ok('no JavaScript page errors')
  browser.close()
finally:
 server.shutdown()
 (OUT/'report.json').write_text(json.dumps({'environment':'Local Chromium DOM-injection harness with explicitly mocked storage; HTTP/file navigation blocked by administrator' if os.environ.get('DOM_HARNESS')=='1' else 'Local Chromium HTTP/file navigation', 'not_tested':['Production Pages deployment','Physical iOS/Android devices','Real HTTP/file-origin persistence'] if os.environ.get('DOM_HARNESS')=='1' else ['Production Pages deployment','Physical devices'],'passed':passes,'page_errors':errors,'count':len(passes),'legal_review':False},ensure_ascii=False,indent=2)+'\n')
