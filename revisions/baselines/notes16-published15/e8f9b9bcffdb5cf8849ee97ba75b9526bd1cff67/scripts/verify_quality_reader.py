#!/usr/bin/env python3
"""Browser verification. --inline explicitly uses simulated storage; no HTTP claim."""
from __future__ import annotations
import argparse,json,re,time
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--html',type=Path,required=True);ap.add_argument('--base-url');ap.add_argument('--inline',action='store_true');ap.add_argument('--browser',default=None);ap.add_argument('--evidence',type=Path,default=ROOT/'test-results/practice-quality');args=ap.parse_args()
 if not args.inline and not args.base_url:ap.error('Use --base-url for real HTTP, or explicit --inline for a constrained runtime.')
 args.evidence.mkdir(parents=True,exist_ok=True);checks=[];errors=[]
 text=args.html.read_text()
 def ok(name,condition=True):
  if not condition:raise AssertionError(name)
  checks.append(name)
 with sync_playwright() as p:
  launch=dict(headless=True)
  if args.browser:launch['executable_path']=args.browser
  b=p.chromium.launch(**launch);ctx=b.new_context(viewport={'width':1280,'height':900},reduced_motion='reduce',accept_downloads=True);page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
  if args.inline:
   # Deliberately simulated; cannot establish real origin or reload persistence.
   page.evaluate("Object.defineProperty(window,'localStorage',{value:{data:{},getItem(k){return this.data[k]||null},setItem(k,v){this.data[k]=String(v)},removeItem(k){delete this.data[k]}}})")
   inline=re.sub(r'<script src="[^\"]+"[^>]*></script>','',text)
   inline=re.sub(r'<link rel="stylesheet"[^>]*>','',inline)
   page.set_content(inline,wait_until='load')
  else:page.goto(args.base_url.rstrip('/')+'/practice-expansion/',wait_until='networkidle')
  page.wait_for_function('typeof window.MPJE_DIAGNOSTICS==="function"')
  diag=lambda:page.evaluate('window.MPJE_DIAGNOSTICS()')
  from publish_practice import build_payload
  payload=build_payload()
  total=payload['published_question_count'];recommended=len(payload['quality_selection']['recommended_ids'])
  first=payload.get('representative_revision',{}).get('new_ids',['MA-REV-0001'])[0]
  ok(f'{total} available; {recommended} default',diag()['total']==total and diag()['filtered']==recommended)
  ok('new individually written case first',diag()['active']==first)
  ok('no topic answer hint before submission',page.locator('#q-title').inner_text()=='법규 적용 사례')
  page.locator('#scope').select_option('all');ok('all variants remain available',diag()['filtered']==total)
  page.locator('#collection').select_option('quality-20261027');ok('96 new cases',diag()['filtered']==96)
  page.locator('#collection').select_option('plus-20261026');ok('1152 old plus unchanged',diag()['filtered']==1152)
  page.locator('#collection').select_option('original-20261023');ok('1024 original unchanged',diag()['filtered']==1024)
  page.locator('#scope').select_option('recommended');page.locator('#collection').select_option('');page.locator('#practice').click();ok('20 family-diverse items',len(diag()['sessionIds'])==20 and len(set(diag()['sessionFamilies']))==20)
  page.locator('#end-session').click()
  page.locator('#timed').click();ok('120 family-diverse items',len(diag()['sessionIds'])==120 and len(set(diag()['sessionFamilies']))==120)
  page.locator('#choices input').first.check();page.locator('#check').click();ok('timed mode conceals explanation',page.locator('#feedback').is_hidden())
  page.locator('#end-session').click();page.locator('#review-submitted').click();ok('timed submitted response can be reviewed',not page.locator('#feedback').is_hidden())
  # Filter to no results: Chaos must still use the entire Q pool, not the filters.
  page.locator('#query').fill('zzzz-no-match');ok('empty filters do not disable chaos',diag()['filtered']==0 and not page.locator('#chaos').is_disabled())
  page.evaluate('()=>{window.MPJEQuality.chaos=(pool,n)=>Array(n).fill(pool[0]);}')
  page.locator('#chaos').click();d=diag();ok('all ten may repeat same exact ID',len(d['sessionIds'])==10 and len(set(d['sessionIds']))==1)
  byid={q['question_id']:q for q in payload['questions']};q=byid[d['sessionIds'][0]]
  keys=q['correct_choice_ids'];wrong=next(c['id'] for c in q['choices'] if c['id'] not in keys)
  for slot in range(10):
   chosen=keys if slot%2==0 else [wrong]
   for k in chosen:page.locator(f'#choices input[value="{k}"]').check()
   page.locator('#check').click()
   # Visible correct letters must correspond to shuffled display positions.
   expected=sorted(diag()['displayLabels'][k] for k in keys)
   ok(f'answer-label mapping at occurrence {slot+1}',', '.join(expected) in page.locator('#answer-heading').inner_text())
   page.locator('#next').click()
  summary=page.locator('#summary').inner_text();ok('ten duplicate occurrences scored independently','10회 제출' in summary and '정답 5회' in summary)
  page.locator('#review-submitted').click();ok('first occurrence preserves correct selection',diag()['reviewSelected']==keys)
  page.locator('#next').click();ok('second occurrence preserves wrong selection',diag()['reviewSelected']==[wrong])
  ok('duplicate occurrence review position',diag()['reviewPosition']==1)
  page.locator('#query').fill('MA-REV-0096');ok('exact-ID lookup includes new cases',diag()['filtered']==1)
  page.locator('#catalog button').first.click();ok('new case loads',diag()['active']=='MA-REV-0096')
  page.locator('#bookmark').click();ok('bookmark storage updated',page.evaluate("JSON.parse(localStorage.getItem('oddments.mpje.practice.v1')).bookmarks.includes('MA-REV-0096')"))
  with page.expect_download() as download:page.locator('#export').click()
  dl=download.value;dl.save_as(str(args.evidence/'progress.json'));backup=json.loads((args.evidence/'progress.json').read_text());ok('backup has stable original IDs',q['question_id'] in backup['attempts'])
  page.locator('#import-file').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':b'{"v":1,"bookmarks":["INVENTED"],"attempts":{}}'})
  page.wait_for_function("document.querySelector('#storage-msg').textContent.includes('가져오기 실패')")
  ok('invalid import rejected', '가져오기 실패' in page.locator('#storage-msg').inner_text())
  page.locator('#import-file').set_input_files(str(args.evidence/'progress.json'));page.wait_for_function("document.querySelector('#storage-msg').textContent.includes('기록을 가져왔습니다')");ok('valid backup import')
  page.locator('#query').fill('');page.locator('#scope').select_option('all');page.locator('#collection').select_option('quality-20261027');page.locator('#qtype').select_option('SATA')
  ok('12 separately authored SATA',diag()['filtered']==12)
  page.locator('#catalog button').first.click();ok('SATA uses checkbox and five options',page.locator('#choices input[type=checkbox]').count()==5)
  page.locator('#qtype').select_option('');page.locator('#query').fill('MA-REV-0081');page.locator('#catalog button').first.click()
  page.set_viewport_size({'width':320,'height':900});page.screenshot(path=str(args.evidence/'quality-mobile.png'),full_page=True)
  ok('320px no document overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
  page.set_viewport_size({'width':1280,'height':900});page.screenshot(path=str(args.evidence/'quality-desktop.png'),full_page=True)
  # Every new case is rendered/answered through UI; no body-level innerHTML shortcuts.
  page.set_viewport_size({'width':320,'height':900})
  previous96=[q for q in payload['questions'] if q['collection_id']=='quality-20261027']
  assert len(previous96)==96
  for q in previous96:
   page.locator('#query').fill(q['question_id']);page.locator('#catalog button').first.click()
   for k in q['correct_choice_ids']:page.locator(f'#choices input[value="{k}"]').check()
   page.locator('#check').click();assert '불일치' not in page.locator('#answer-heading').inner_text()
   assert page.locator('#rationales .rationale').count()==len(q['choices'])
  ok('all96 new cases render, score and explain at320px')
  ok('no uncaught JS errors',not errors)
  report=dict(mode='INLINE_DOM_SIMULATED_STORAGE' if args.inline else 'REAL_HTTP_REAL_ORIGIN',passed=len(checks),checks=checks,errors=errors,limits=['Inline mode does not verify HTTP navigation or real-origin reload persistence.'] if args.inline else [])
  (args.evidence/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
  b.close()
if __name__=='__main__':main()
