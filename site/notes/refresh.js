/* Companion learning layer: no quizzes, no accounts, no clinical decision engine. */
(() => {
  'use strict';
  const D=window.MPJE_REFRESH, N=window.MPJE_NOTES, C=window.MPJE_REFRESH_CORE;
  if(!D||!N||!C)return;
  const $=(s,root=document)=>root.querySelector(s);
  const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const norm=v=>String(v).normalize('NFKC').toLowerCase().replace(/\s+/g,' ').trim();
  const safe=v=>{try{const u=new URL(v);return ['https:','http:'].includes(u.protocol)?u.href:'#';}catch{return '#';}};
  const cards=new Map(D.cards.map(c=>[c.id,c])), units=new Map(), chapters=new Map(N.chapters.map(ch=>[ch.id,ch]));
  N.chapters.forEach(ch=>ch.units.forEach(u=>units.set(u.id,{...u,chapter:ch.id})));
  const ids=[...cards.keys()],fieldIds=D.field_checklist.map(x=>x.id);
  let state=C.cleanState({},ids,fieldIds),storageOK=true,controller=null;
  try{const raw=localStorage.getItem(C.KEY);if(raw)state=C.cleanState(JSON.parse(raw),ids,fieldIds);}catch{storageOK=false;}
  const stageName=id=>D.stages.find(s=>s.id===id)?.title||'장별 개요';
  const warningLabels={open:'OPEN · 적용 관계 미확정','date-sensitive':'시행일·현재 상태 재확인','source-gap':'원문 확인 범위 제한',interpretation:'편집상 해석 구분'};
  const kinds={'notes-summary':'통합노트 요약','learning-synthesis':'노트 기반 학습 설계','learning-example':'가상 계산·학습 예시','external-safety':'공식 안전교육 추가','drug-appendix':'기존 약물 부록 재구성','chapter-overview':'통합노트 장 개요'};
  function save(){try{localStorage.setItem(C.KEY,JSON.stringify(state));}catch{storageOK=false;}storageMessage();}
  function storageMessage(){const el=$('#rf-storage');if(el){el.hidden=storageOK;el.textContent='브라우저에 기록을 저장할 수 없습니다. 이번 화면의 기록은 내보내기로 보관하세요.';}}
  function ensureDaily(){const today=C.dayKey();if(!state.daily||state.daily.date!==today){state.daily={date:today,ids:C.dailyCards(D.cards,state.reviews,today),completed:[]};save();}return state.daily;}
  function notice(text){const el=$('#rf-status');if(el)el.textContent=text;}
  function linkUnit(id){const u=units.get(id);return u?`#chapter/${u.chapter}/${id}`:'#home';}
  function warnings(card){return card.flags.map(f=>`<span class="rf-warning">${esc(warningLabels[f]||f)}</span>`).join('');}
  function provenance(card){
    const external=card.external_sources.map(id=>D.external_sources[id]);
    return `<p class="rf-provenance">${esc(kinds[card.kind])} · 노트 원문 기준 ${esc(card.source_review_dates.join(' / '))}${external.length?' · 추가 안전교육 확인 '+esc(external.map(s=>s.checked_at).join(', ')):''}<br>카드 편집 ${esc(card.edited_at)} · 법규 전수 재검증 표시가 아닙니다.</p>`;
  }
  function sourceLinks(card){
    const links=card.note_units.map(id=>{const u=units.get(id);return `<li><a href="${linkUnit(id)}">${esc(u.title)} →</a></li>`;}).join('');
    const sourceIds=card.source_ids||[...new Set(card.note_units.flatMap(id=>units.get(id).source_ids))];
    const external=card.external_sources.map(id=>{const s=D.external_sources[id];return `<li><a href="${esc(safe(s.url))}" target="_blank" rel="noopener noreferrer">${esc(s.title)} ↗</a><p>${esc(s.scope)} · 확인 ${s.checked_at}</p></li>`;}).join('');
    return `<details class="rf-sources"><summary>관련 노트·출처 확인</summary><ul>${links}${external}</ul><details><summary>기존 노트의 연결 근거 ${sourceIds.length}개</summary><p class="muted">기존 확인 범위를 승계한 링크입니다. 오늘 모든 원문을 다시 검증했다는 뜻은 아닙니다.</p><ul>${sourceIds.map(id=>N.sources[id]?`<li><a href="${esc(safe(N.sources[id].url))}" target="_blank" rel="noopener noreferrer">${esc(N.sources[id].title)}</a></li>`:'').join('')}</ul></details>${card.lookup_url?`<p><a href="${esc(safe(card.lookup_url))}" target="_blank" rel="noopener noreferrer">${esc(card.lookup_label)} ↗</a></p>`:''}</details>`;
  }
  function cleanup(){controller?.abort();controller=null;}
  function listen(el,event,fn){if(el)el.addEventListener(event,fn,{signal:controller.signal});}
  function backup(){const blob=new Blob([JSON.stringify({application:'oddments-refresh',edition:D.edition,exported_at:new Date().toISOString(),...state},null,2)],{type:'application/json'});const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='mpje-refresh-progress.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
  async function importBackup(file){
    if(!file)return;
    try{if(file.size>2_000_000)throw new Error('파일이 너무 큽니다.');const incoming=C.cleanState(JSON.parse(await file.text()),ids,fieldIds,true);state=C.mergeState(state,incoming);save();notice('기존 기록을 보존해 복습 기록을 합쳤습니다.');return true;}
    catch(e){notice('가져오기 실패: '+e.message);return false;}
  }
  function footer(){return `<details class="rf-method"><summary>자료 범위 · 반복 간격 · 기록 관리</summary><p>${esc(D.source_policy)}</p><p>자기평가에 따라 다시 = 1일, 헷갈림 = 3일, 기억남 = 7일 후 복습 대상으로 표시합니다. 학습용 단순 일정이며 기억력 측정·공식 시험 점수·합격 예측이 아닙니다. 날짜는 America/New_York 기준이고, 알림을 전송하거나 백그라운드 작업을 하지 않습니다.</p><p>오늘 10장은 기한 도래 카드를 먼저 최대 3장 배치하고, 나머지는 아직 덜 본 기초 카드를 우선합니다. OPEN·시행일 주의 카드는 오늘의 기본 묶음에서 제외하되 전체·주제 검색으로 열 수 있습니다. 랜덤은 현재 필터 안에서 한 바퀴 돌 때까지 중복을 피합니다.</p><p>기록은 이 브라우저에만 저장됩니다. 기기 간 자동 동기화는 없습니다. 기존 문제은행·노트 진도는 변경하지 않습니다. 환자정보를 입력·저장하는 기능은 없습니다.</p><div class="rf-actions"><button type="button" id="rf-export">카드 기록 내보내기</button><button type="button" id="rf-import">카드 기록 가져오기</button><input type="file" id="rf-file" accept="application/json,.json" hidden></div><p id="rf-storage" class="notice" hidden></p></details>`;}
  function bindFooter(refresh){listen($('#rf-export'),'click',backup);listen($('#rf-import'),'click',()=>$('#rf-file').click());listen($('#rf-file'),'change',async e=>{if(await importBackup(e.target.files[0]))refresh?.();e.target.value='';});storageMessage();}
  function render(host, route, rest=[]){
    cleanup();controller=new AbortController();
    if(route==='return'){renderPath(host);return;}
    if(route==='glossary'){renderGlossary(host,rest.join('/'));return;}
    renderCards(host,rest);
  }
  function renderCards(host,rest){
    ensureDaily();
    let mode=rest[0]==='today'?'today':rest[0]==='due'?'due':rest[0]==='saved'?'saved':rest[0]==='path'?'path':'random';
    let stage=mode==='path'&&D.stages.some(s=>s.id===rest[1])?rest[1]:'';
    const initialChapter=rest[0]==='topic'&&chapters.has(rest[1])?rest[1]:'';
    const direct=rest[0]==='card'&&cards.has(rest[1])?rest[1]:null;
    let current=null,queue=[],queuePos=0,serial=0,shown=false,alreadyRated=false;
    host.innerHTML=`<div id="rf-shell" class="rf-shell" style="--rf-size:${state.font}px"><header class="rf-heading"><p class="eyebrow">DAILY REFRESH · SUPPLEMENTAL REVIEW</p><h1>짧게 읽고, 차이를 이해하기</h1><p>한 줄 핵심을 읽고 → 쉬운 설명과 약국 예시 → 헷갈리는 조건 → 원문으로 연결합니다.</p><div class="rf-links"><a href="#study">MPJE 법규 학습 우선 →</a><a href="#return">합격 후 · RA→약국 복귀</a><a href="#glossary">용어 ${D.stats.terms}개 쉽게 보기</a><a href="#home">상세 통합노트</a></div></header>
      <div class="rf-modebar" role="group" aria-label="복습 방법"><button type="button" data-mode="today">오늘 10장</button><button type="button" data-mode="random">랜덤 주제</button><button type="button" data-mode="due">복습할 카드</button><button type="button" data-mode="saved">저장한 카드</button></div>
      <p id="rf-summary" class="rf-summary"></p>
      <details class="rf-filters" ${initialChapter||direct?'open':''}><summary>주제·카드 종류·검색</summary><div class="rf-filter-grid"><label>카드 종류<select id="rf-deck"><option value="core">기초·실무 ${D.stats.curated}장</option><option value="drugs">Generic·Brand ${D.stats.drugs}장</option><option value="chapters">장별 개요 ${D.stats.chapters}장</option><option value="all">전체 ${D.stats.cards}장</option></select></label><label>노트 주제<select id="rf-topic"><option value="">모든 주제</option>${N.chapters.map(c=>`<option value="${esc(c.id)}">${esc(c.title)}</option>`).join('')}</select></label><label class="rf-search-label">검색<input id="rf-query" type="search" placeholder="예: DUR, refill, BUD, gabapentin" autocomplete="off" spellcheck="false"></label></div><p class="muted">필터 변경은 선택한 복습 방법 안에서 적용됩니다. 새 주제를 자유롭게 보려면 랜덤 주제를 선택하세요.</p></details>
      <div class="rf-options"><label><input type="checkbox" id="rf-recall" ${state.recall?'checked':''}> 핵심을 먼저 가리고 떠올리기</label><div class="rf-actions"><button type="button" id="rf-smaller" aria-label="카드 글자 작게">A−</button><button type="button" id="rf-larger" aria-label="카드 글자 크게">A+</button></div></div>
      <div id="rf-card"></div><p id="rf-status" class="rf-status" role="status" aria-live="polite"></p>${footer()}</div>`;
    $('#rf-deck').value=initialChapter||direct?'all':'core';$('#rf-topic').value=initialChapter;
    function eligible(){
      const deck=$('#rf-deck').value,topic=$('#rf-topic').value,q=norm($('#rf-query').value);
      let pool=D.cards.filter(c=>(deck==='all'||c.deck===deck)&&(!topic||c.chapters.includes(topic))&&(!q||norm([c.id,c.title,c.takeaway,c.plain,c.example,c.watch].join(' ')).includes(q)));
      if(mode==='today'){const today=ensureDaily();pool=pool.filter(c=>today.ids.includes(c.id)).sort((a,b)=>today.ids.indexOf(a.id)-today.ids.indexOf(b.id));}
      if(mode==='due')pool=pool.filter(c=>state.reviews[c.id]&&(state.reviews[c.id].due<=C.dayKey()||state.reviews[c.id].grade!=='good'));
      if(mode==='saved')pool=pool.filter(c=>state.saved.includes(c.id));
      if(mode==='path')pool=pool.filter(c=>c.stage===stage&&c.deck==='core');
      return pool;
    }
    function summary(){
      const daily=ensureDaily(),available=eligible();const due=D.cards.filter(c=>state.reviews[c.id]?.due<=C.dayKey()).length;
      $('#rf-summary').textContent=`${C.dayKey()} · 뉴욕 시간 | ${mode==='today'?`오늘 ${daily.completed.length} / ${daily.ids.length}장 확인`:mode==='path'?stageName(stage):mode==='due'?'기한 도래 + 최근 헷갈림':mode==='saved'?'저장한 카드':'현재 필터에서 섞어 보기'} · 대상 ${available.length}장 · 기한 도래 ${due}장`;
      host.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode===mode)));
    }
    function newQueue(prefer){
      const pool=eligible();queue=mode==='random'?C.shuffled(pool.map(c=>c.id),C.dayKey()+':'+Date.now()+':'+serial++):pool.map(c=>c.id);
      if(prefer&&queue.includes(prefer)){queue=queue.filter(id=>id!==prefer);queue.unshift(prefer);}
      if(!prefer&&queue.length>1&&queue[0]===current){[queue[0],queue[1]]=[queue[1],queue[0]];}
      queuePos=0;next();
    }
    function next(){
      if(queuePos>=queue.length){
        if(mode==='today'||mode==='path'){showFinish();return;}
        if(!eligible().length){showEmpty();return;}
        newQueue();return;
      }
      current=queue[queuePos++];shown=!state.recall;alreadyRated=false;state.last=current;save();draw();summary();
    }
    function showEmpty(){current=null;$('#rf-card').innerHTML='<section class="rf-empty"><h2>이 조건의 카드가 없습니다.</h2><p>검색어·카드 종류·주제를 바꾸거나 랜덤 주제로 돌아가세요. 헷갈림 표시는 카드를 읽은 뒤 직접 남길 수 있습니다.</p><button type="button" id="rf-reset">전체 기초 카드 보기</button></section>';listen($('#rf-reset'),'click',()=>{mode='random';stage='';$('#rf-deck').value='core';$('#rf-topic').value='';$('#rf-query').value='';newQueue();});summary();}
    function showFinish(){
      if(!queue.length){showEmpty();return;}
      const done=mode==='today'?ensureDaily().completed.length:queue.filter(id=>state.reviews[id]).length;
      $('#rf-card').innerHTML=`<section class="rf-empty"><p class="eyebrow">SESSION REVIEW</p><h2>이번 묶음을 둘러봤습니다.</h2><p>표시한 카드 ${done}장. 건너뛴 카드는 완료로 세지 않습니다. 이 수치는 시험 점수나 현장 역량 평가가 아닙니다.</p><div class="rf-actions"><button type="button" id="rf-repeat">같은 묶음 다시 보기</button><button type="button" id="rf-random-after">랜덤 주제로 계속</button><a href="#return">복귀 경로로</a></div></section>`;
      listen($('#rf-repeat'),'click',()=>newQueue());listen($('#rf-random-after'),'click',()=>{mode='random';stage='';newQueue();});summary();
    }
    function draw(){
      const card=cards.get(current);if(!card){showEmpty();return;}
      const drug=card.deck==='drugs';const r=state.reviews[card.id];
      $('#rf-card').innerHTML=`<article class="rf-card" data-card-id="${card.id}"><div class="rf-card-meta"><span>${card.id} · ${esc(card.deck==='core'?stageName(card.stage):drug?'Generic → Brand · 제형·법적 구분':'장별 개요')}</span><button type="button" id="rf-save" aria-pressed="${state.saved.includes(card.id)}">${state.saved.includes(card.id)?'저장됨':'저장'}</button></div><div class="rf-warning-row">${warnings(card)}</div><h2 id="rf-card-title" tabindex="-1">${esc(card.title)}</h2>
        <button type="button" id="rf-reveal" class="primary-button" ${shown?'hidden':''}>핵심·설명 펼치기</button>
        <div id="rf-answer" ${shown?'':'hidden'}><p class="rf-takeaway">${esc(card.takeaway)}</p><div class="rf-explanation"><h3>${drug?'제형·제품 구분':'쉽게 이해하기'}</h3><p>${esc(card.plain).replace(/\n/g,'<br>')}</p><h3>${drug?'함께 기억할 경계':'약국에서는 · 학습 예시'}</h3><p>${esc(card.example)}</p><div class="rf-watch"><strong>${drug?'노트의 법적 분류 · 현재 조건은 원문 확인':'놓치기 쉬운 조건'}</strong><p>${esc(card.watch)}</p></div>${card.ra_bridge?`<details class="rf-bridge"><summary>RA 경험과 연결해서 이해하기</summary><p>${esc(card.ra_bridge)}</p><small>이해를 돕는 비유이며 동일한 법규라는 뜻은 아닙니다.</small></details>`:''}</div></div>
        ${provenance(card)}<div class="rf-note-link"><a href="${linkUnit(card.note_units[0])}">관련 통합노트에서 자세히 →</a><a href="#glossary">낯선 용어 보기</a></div>${sourceLinks(card)}
        <div class="rf-grade" role="group" aria-label="카드 자기평가"><button type="button" data-grade="again" ${!shown||alreadyRated?'disabled':''}>다시 · 1일 후</button><button type="button" data-grade="hard" ${!shown||alreadyRated?'disabled':''}>헷갈림 · 3일 후</button><button type="button" data-grade="good" ${!shown||alreadyRated?'disabled':''}>기억남 · 7일 후</button></div>
        <div class="rf-next-row"><span class="muted">${r?'마지막 표시 '+r.last+' · 다음 복습 '+r.due:'아직 자기평가하지 않은 카드'}<br>${queuePos} / ${queue.length} · 자기평가를 누르지 않으면 건너뛰기</span><button type="button" id="rf-next" class="primary-button">${mode==='random'?'새 주제 ↻':'다음 카드 →'}</button></div></article>`;
      listen($('#rf-reveal'),'click',()=>{shown=true;draw();});
      listen($('#rf-save'),'click',()=>{state.saved=state.saved.includes(card.id)?state.saved.filter(id=>id!==card.id):[...state.saved,card.id];save();draw();notice(state.saved.includes(card.id)?'카드를 저장했습니다.':'저장을 해제했습니다.');});
      host.querySelectorAll('[data-grade]').forEach(b=>listen(b,'click',()=>{
        if(!shown||alreadyRated)return;alreadyRated=true;state.reviews[card.id]=C.gradeReview(state.reviews[card.id],b.dataset.grade,C.dayKey());
        const daily=ensureDaily();if(daily.ids.includes(card.id)&&!daily.completed.includes(card.id))daily.completed.push(card.id);
        save();draw();summary();notice('표시했습니다. 다음 복습 '+state.reviews[card.id].due+' · 새 주제를 누르면 다음 카드로 이동합니다.');
      }));
      listen($('#rf-next'),'click',()=>{notice('');next();$('#rf-card-title')?.focus({preventScroll:true});$('#rf-card').scrollIntoView({block:'start',behavior:'auto'});});
    }
    host.querySelectorAll('[data-mode]').forEach(b=>listen(b,'click',()=>{mode=b.dataset.mode;stage='';$('#rf-topic').value='';$('#rf-query').value='';$('#rf-deck').value=mode==='saved'||mode==='due'?'all':'core';newQueue();notice('');}));
    ['#rf-deck','#rf-topic'].forEach(id=>listen($(id),'change',()=>newQueue()));
    listen($('#rf-query'),'input',()=>newQueue());
    listen($('#rf-recall'),'change',e=>{state.recall=e.target.checked;shown=!state.recall;save();if(current)draw();});
    for(const [selector,delta] of [['#rf-smaller',-1],['#rf-larger',1]])listen($(selector),'click',()=>{state.font=Math.max(16,Math.min(24,state.font+delta));$('#rf-shell').style.setProperty('--rf-size',state.font+'px');save();});
    bindFooter(()=>{summary();if(current)draw();});
    newQueue(direct);
  }
  function renderPath(host){
    host.innerHTML=`<div class="rf-shell"><header class="rf-heading"><p class="eyebrow">RETURN-TO-PRACTICE BRIDGE</p><h1>RA에서 약국으로,<br>기초부터 다시 연결하기</h1><p>제품 정보·문서관리·품질 경험을 출발점으로 삼되, 환자별 판단·상담·현장 수행은 따로 준비합니다. 7단계는 고정 7일 일정이 아니라 학습 순서입니다.</p><div class="rf-links"><a href="#refresh/today">오늘 10장</a><a href="#refresh">랜덤 복습</a><a href="#glossary">기초 용어</a></div></header><section class="rf-map"><h2>먼저 처방 한 건을 따라갑니다</h2><p>접수 → 적법성 → DUR → 제품·label 검수 → 교부·상담 → 기록·인계</p><p class="muted">학습용 흐름입니다. 실제 전산 순서·직원 역할·SOP는 약국마다 확인하세요.</p></section><div class="rf-path-grid">${D.stages.map(s=>{const done=s.card_ids.filter(id=>state.reviews[id]).length;return `<section class="rf-path-card"><p class="eyebrow">STEP ${s.number}</p><h2>${esc(s.title)}</h2><p>${esc(s.description)}</p><p class="rf-practice-note"><strong>현장 연결</strong> ${esc(s.practice)}</p><small>자기평가 기록 ${done} / ${s.card_ids.length}장 · 능력 인증 아님</small><a class="secondary-button" href="#refresh/path/${s.id}">이 단계 순서대로 보기 →</a></section>`;}).join('')}</div><section class="rf-field"><h2>현장 교육 담당자와 확인할 것</h2><p>개인 확인 목록입니다. 체크가 고용주 승인이나 독립 근무 자격을 의미하지 않습니다.</p>${D.field_checklist.map(x=>`<label><input type="checkbox" data-field="${x.id}" ${state.field.includes(x.id)?'checked':''}><span>${esc(x.text)}</span></label>`).join('')}</section><details class="rf-method"><summary>이 자료에서 아직 제공하지 않는 임상 교육</summary><p>질환별 치료 알고리즘, 개별 약물의 전체 용량·상호작용·신기능/간기능 조절, 모든 백신의 최신 시즌 protocol, 실물 기기 technique와 약국 전산 교육은 이 카드의 완결 범위가 아닙니다. 법규 시험 준비와 임상·현장 업무 준비를 따로 관리하세요.</p><p>이 페이지에는 환자 정보를 넣지 않습니다. 실제 사례는 기관의 승인된 교육·보안 환경에서 다루세요.</p></details><p id="rf-status" class="rf-status" role="status"></p>${footer()}</div>`;
    host.querySelectorAll('[data-field]').forEach(el=>listen(el,'change',()=>{state.field=el.checked?[...new Set([...state.field,el.dataset.field])]:state.field.filter(x=>x!==el.dataset.field);save();notice('개인 확인 목록을 저장했습니다.');}));bindFooter(()=>renderPath(host));
  }
  function renderGlossary(host,query=''){
    let initial='';try{initial=decodeURIComponent(query);}catch{}
    host.innerHTML=`<div class="rf-shell"><header class="rf-heading"><p class="eyebrow">PLAIN-LANGUAGE PHARMACY</p><h1>낯선 용어부터 편하게</h1><p>뜻을 먼저 잡고 연결된 노트에서 적용 조건·예외를 확인합니다.</p><div class="rf-links"><a href="#return">복귀 7단계</a><a href="#refresh">복습 카드</a></div></header><label class="rf-glossary-search">용어·뜻 검색<input type="search" id="rf-term-search" placeholder="예: refill, 수량, REMS" value="${esc(initial)}" autocomplete="off"></label><p id="rf-term-count" role="status" class="rf-summary"></p><div id="rf-terms" class="rf-glossary-grid"></div></div>`;
    function run(){const q=norm($('#rf-term-search').value),rows=D.glossary.filter(t=>norm(t.term+' '+t.meaning).includes(q));$('#rf-term-count').textContent=rows.length+'개 용어';$('#rf-terms').innerHTML=rows.length?rows.map(t=>`<article class="rf-term"><h2>${esc(t.term)}</h2><p>${esc(t.meaning)}</p><a href="${linkUnit(t.note_units[0])}">조건·예외 읽기 →</a></article>`).join(''):'<p class="rf-empty">일치하는 용어가 없습니다. 짧은 영문 이름이나 한국어로 검색하세요.</p>';}
    listen($('#rf-term-search'),'input',run);run();
  }
  function mountHome(container){
    if(!container)return;
    const daily=ensureDaily();let pool=C.shuffled(D.cards.filter(c=>c.deck==='core'&&!c.flags.some(f=>['open','date-sensitive','source-gap'].includes(f))),C.dayKey()+':home'),index=0;
    function draw(){const c=pool[index%pool.length];container.innerHTML=`<section class="rf-home"><div><p class="eyebrow">DAILY REFRESH · ${C.dayKey()}</p><h2>오늘의 짧은 복습</h2><p class="rf-home-title">${esc(c.title)}</p><p>${esc(c.takeaway)}</p><small>통합노트·학습 설명 기반. 간단한 핵심 뒤에 조건·예외를 확인하세요.</small><div class="rf-actions"><button type="button" id="rf-home-next">다른 주제 ↻</button><a class="primary-button" href="#refresh/card/${c.id}">쉽게 설명 보기 →</a></div></div><aside><strong>시험 법규부터 학습하기</strong><p>기초·실무 ${D.stats.curated}장<br>약물명 ${D.stats.drugs}장 · 장 개요 ${D.stats.chapters}장</p><a href="#refresh/today">오늘 10장 · ${daily.completed.length}/${daily.ids.length} 확인 →</a><a href="#study/today">MPJE 법규만 오늘 10개 →</a><details><summary>합격 후 실무 복귀</summary><a href="#return">RA→약국 복귀 경로 →</a></details><a href="#glossary">용어 ${D.stats.terms}개 쉽게 보기 →</a></aside></section>`;$('#rf-home-next').onclick=()=>{index++;draw();};}draw();
  }
  window.MPJE_REFRESH_VIEW={render,cleanup,mountHome};
})();
