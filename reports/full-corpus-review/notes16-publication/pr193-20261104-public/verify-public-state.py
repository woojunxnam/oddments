"""Read-only public state binding; existing HOLD is observed, not re-judged."""
from datetime import datetime,timezone
import hashlib,json,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright,expect

ROOT=Path('/workspace/mpje-pr193-public')
OUT=ROOT/'reports/full-corpus-review/notes16-publication/pr193-20261104-public/public-state'
BASE='https://woojunxnam.github.io/oddments/'
OUT.mkdir(exist_ok=True)
errors=[];requests=[];checks=[]
with sync_playwright()as p:
    browser=p.chromium.launch(headless=True)
    context=browser.new_context(viewport={'width':1440,'height':1000})
    page=context.new_page();page.on('pageerror',lambda error:errors.append(str(error)))
    page.on('request',lambda request:requests.append({'method':request.method,'url':request.url}))
    page.goto(BASE+'practice-expansion/quality-review.html',wait_until='networkidle')
    expect(page.locator('tr').filter(has_text='독립 legacy 정답 평가')).to_contain_text('1793/2349')
    expect(page.locator('tr').filter(has_text='독립 노트 열거 완전성 확인')).to_contain_text('100/306')
    quality_rows=page.locator('tr').all_inner_texts()
    page.screenshot(path=str(OUT/'quality-status-desktop.png'),full_page=True)
    checks.append('Public quality status retains published question-key1793 and independent-note100 values')
    page.goto(BASE+'practice-expansion/',wait_until='networkidle')
    diag=page.evaluate('MPJE_DIAGNOSTICS()')
    assert diag['filtered']==202 and diag['total']==2349,diag
    checks.append('Public default selection remains202 of2349')
    page.goto(BASE+'notes/',wait_until='networkidle')
    actual=page.evaluate("""()=>{
      const d=window.MPJE_NOTES,c=d.chapters.find(c=>c.units.some(u=>u.id==='w3-a-3'));
      const u=c.units.find(u=>u.id==='w3-a-3');
      return {edition:d.edition,progress:d.independent_note_review_progress,
        chapter_id:c.id,unit_id:u.id,body_sha256:u.body_sha256,review:u.independent_atomic_census_review};
    }""")
    assert actual['progress']['complete_units']==100
    review=actual['review']
    assert review['completeness']=='COMPLETE'and review['legal_status']=='LEGAL_HOLD'
    assert review['requires_review']is True and review['current_review_valid']is True
    assert any(f['claim_id']=='NOTE-WAVE8-W3-A-3-011'and f['legal_status']=='LEGAL_HOLD'and f.get('blocker')for f in review['findings'])
    assert review['canonical_release_credit']==review['question_audit_credit']==0
    assert review['review_history']
    page.goto(BASE+'notes/#chapter/'+actual['chapter_id']+'/w3-a-3',wait_until='networkidle')
    unit=page.locator('#w3-a-3')
    expect(unit).to_contain_text('보류')
    page.screenshot(path=str(OUT/'n1-preserved-hold-desktop.png'),full_page=True)
    checks.append('Public N1 retains current COMPLETE/LEGAL_HOLD, original011 blocker and review history with zero release credit')
    assert not errors,errors
    assert all(r['method']=='GET'for r in requests),requests
    browser.close()
report=dict(observed_at_utc=datetime.now(timezone.utc).isoformat(),base_url=BASE,
    source_head=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),
    status='PASS',checks=checks,quality_rows=quality_rows,practice_diagnostics=diag,n1_public_state=actual,
    javascript_errors=errors,requests=requests,isolated_context=True,real_user_profile_used=False,
    legal_audit=False,physical_device_test=False)
(OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':len(checks),'javascript_errors':len(errors)}),flush=True)
