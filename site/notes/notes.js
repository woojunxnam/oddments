/* Standalone source-derived reference reader. No network, analytics, account or quiz-bank writes. */
(() => {
  'use strict';
  const D = window.MPJE_NOTES;
  const $ = (s, root = document) => root.querySelector(s);
  const reader = $('#reader');
  $('.skip-link').addEventListener('click', e => { e.preventDefault(); reader.focus(); reader.scrollIntoView({block:'start'}); });
  if (!D || !Array.isArray(D.chapters)) {
    reader.innerHTML = '<h1>학습 화면을 불러오지 못했습니다.</h1><p><a href="book.html">전체 본문과 출처 읽기</a>는 별도로 사용할 수 있습니다.</p>';
    return;
  }
  const KEY = 'oddments.mpje.ultimate-notes.v1';
  const chapters = new Map(D.chapters.map(c => [c.id, c]));
  const units = new Map();
  D.chapters.forEach((c, i) => c.units.forEach(u => units.set(u.id, {...u, chapter: c, chapterIndex: i})));
  const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const safeUrl = value => {
    try { const u = new URL(value); return ['https:', 'http:'].includes(u.protocol) ? u.href : '#'; }
    catch { return '#'; }
  };
  const decode = v => { try { return decodeURIComponent(v); } catch { return ''; } };
  const normalize = v => String(v).normalize('NFKC').toLocaleLowerCase().replace(/[\u200b-\u200d]/g,'').replace(/[^\p{L}\p{N}]+/gu,' ').trim();
  let storageOK = true;
  function validState(x) {
    if (!x || typeof x !== 'object' || Array.isArray(x)) throw new Error('Invalid state');
    const ids = key => Array.isArray(x[key]) ? [...new Set(x[key].filter(id => typeof id === 'string' && units.has(id)))].slice(0, units.size) : [];
    return {version:1, read:ids('read'), saved:ids('saved'), font:Number.isFinite(x.font) ? Math.max(16,Math.min(24,x.font)) : 18,
      theme:['light','dark','system'].includes(x.theme) ? x.theme : 'system', focus: !!x.focus,
      last: typeof x.last === 'string' && units.has(x.last) ? x.last : null};
  }
  let state = validState({});
  try { const raw = localStorage.getItem(KEY); if (raw) state = validState(JSON.parse(raw)); }
  catch { storageOK = false; }
  function save() {
    try { localStorage.setItem(KEY, JSON.stringify(state)); }
    catch { storageOK = false; }
    if (!storageOK) {
      const n = $('#storage-notice'); n.hidden = false;
      n.textContent = '브라우저 저장소를 사용할 수 없습니다. 이번 화면의 기록을 내보내기로 저장하세요.';
    }
  }
  function toast(text) {
    const t = $('#toast'); t.textContent = text; t.classList.add('show');
    clearTimeout(toast.timer); toast.timer = setTimeout(() => t.classList.remove('show'), 2600);
  }
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  function applyPrefs() {
    document.documentElement.dataset.theme = state.theme === 'system' ? (media.matches ? 'dark':'light') : state.theme;
    document.documentElement.style.setProperty('--body-size', state.font+'px');
    document.body.classList.toggle('focus-reading', state.focus);
    const b = $('#theme-button'); b.textContent = {light:'밝게',dark:'어둡게',system:'자동'}[state.theme];
    b.setAttribute('aria-label','화면 테마: '+b.textContent+' · 다음 테마로 변경');
  }
  media.addEventListener?.('change',applyPrefs);
  $('#theme-button').addEventListener('click',() => {
    state.theme = {system:'light',light:'dark',dark:'system'}[state.theme]; applyPrefs(); save();
  });
  function progress() {
    $('#progress-label').textContent = `${state.read.length} / ${units.size}`;
    $('#progress-bar').max = units.size; $('#progress-bar').value = state.read.length;
  }
  function href(u) { return `#chapter/${u.chapter.id}/${u.id}`; }
  const kindLabels = {'source-derived':'기존 노트 재편집','editorial-synthesis':'중복 통합·재서술','new-primary-source-check':'공식 원문 추가 확인'};
  const flagLabels = {open:'적용 경계 확인 필요','date-sensitive':'시행일·현재 상태 확인','interpretation':'편집상 적용 판단','source-gap':'출처 연결 보완 필요'};
  function badges(u) { return (u.flags || []).map(f => `<span class="badge warning">${esc(flagLabels[f] || f)}</span>`).join(''); }
  function chapterNavigation() {
    let part = ''; let html = '';
    D.chapters.forEach((c, i) => {
      if (c.part !== part) { part = c.part; html += `<p class="nav-group">${esc(part)}</p>`; }
      html += `<a class="chapter-nav-link" href="#chapter/${c.id}" data-chapter="${c.id}"><span class="nav-num">${String(i+1).padStart(2,'0')}</span><span>${esc(c.title)}</span></a>`;
    });
    $('#chapter-nav').innerHTML = html;
    $('#mobile-nav').innerHTML = '<a class="nav-home" href="#home">학습 시작</a><a class="nav-item" href="#search">본문 검색</a><a class="nav-item" href="#drugs">Generic · Brand 사전</a><a class="nav-item" href="#saved">북마크 · 다시 읽기</a><a class="nav-item" href="../">메인 · 문제은행 ↗</a>'+html+'<a class="nav-item" href="#sources">출처 · 편집 기록</a><a class="nav-item" href="book.html">전체 읽기 · 인쇄</a>';
  }
  const dialog = $('#nav-dialog');
  $('#mobile-menu').addEventListener('click', () => dialog.showModal());
  $('#close-nav').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click',e => { if (e.target.closest('a')) dialog.close(); });
  document.addEventListener('click',e => { const b = e.target.closest('[data-route]'); if (b) location.hash = b.dataset.route; });
  let observer = null;
  function setToc(ch) {
    const toc = $('#page-toc');
    if (!ch) { toc.innerHTML = '<p class="toc-title">이 교재의 기준</p><p class="toc-note">원문 대조: 2026.10.20–22<br>통합 편집: 2026.10.23<br><br>허용·금지·예외와 출처를 함께 읽습니다. OPEN과 미래 시행을 확정 규칙처럼 외우지 않습니다.</p><a href="#chapter/open-register">미확정 범위 확인 →</a><a href="book.html">전체 본문 · 인쇄 →</a>'; return; }
    toc.innerHTML = `<p class="toc-title">이 장에서 읽을 내용</p>${ch.units.map(u=>`<a href="#chapter/${ch.id}/${u.id}" data-scroll="${u.id}">${esc(u.title)}</a>`).join('')}<p class="toc-note">읽음 표시는 개인 학습 기록입니다. 숙련도·합격 가능성의 측정값이 아닙니다.</p>`;
  }
  function searchBox(id, value='', label='검색', placeholder='예: 72시간, gabapentin, MOR, 247 CMR') {
    return `<div class="search-field"><label for="${id}">${esc(label)}</label><input id="${id}" type="search" value="${esc(value)}" placeholder="${esc(placeholder)}" autocomplete="off" spellcheck="false"></div>`;
  }
  function renderHome() {
    setToc(null);
    const last = state.last && units.get(state.last);
    reader.innerHTML = `<section class="hero"><p class="eyebrow">THE CONNECTED PHARMACY LAW NOTEBOOK</p><h1>Massachusetts MPJE<br>흩어진 규칙을, 한 흐름으로.</h1><p>Week 1–6의 상세 노트를 주제별로 다시 엮었습니다. 핵심 개념부터 적용 조건·예외·약물·공식 근거까지, 같은 주제는 한 곳에서 이어 읽으세요.</p><div class="actions"><a class="primary-button" href="${last ? href(last) : '#chapter/foundations'}">${last ? '마지막 읽은 곳 이어보기':'통합 노트 시작하기'} <span aria-hidden="true">&nbsp;→</span></a><a class="secondary-button" href="#drugs">Generic · Brand 사전</a></div><div class="stats-grid"><div class="stat"><strong>${D.stats.chapters}</strong><span>주제별 장</span></div><div class="stat"><strong>${D.stats.units}</strong><span>상세 읽기 절</span></div><div class="stat"><strong>${D.stats.drugs}</strong><span>약물·제형 항목</span></div><div class="stat"><strong>${D.stats.sources}</strong><span>연결 출처</span></div></div></section>
    <p class="notice"><strong>상세 학습판 · 일부 경계 확인 필요</strong><br>편집일 2026.10.23. 기존 노트의 확인일과 새로 검토한 범위를 구분합니다. 독립 전수 법률감사나 합격 보장이 아닙니다. <a href="#chapter/open-register">남은 OPEN 확인</a></p>
    ${last ? `<a class="resume-card" href="${href(last)}"><span><small>이어서 읽기 · ${esc(last.chapter.title)}</small><strong>${esc(last.title)}</strong></span><span aria-hidden="true">→</span></a>`:''}
    <form id="home-search" class="home-search">${searchBox('home-query')}<p class="search-hint">한국어·English·법규 번호·약 이름으로 전체 본문을 검색합니다. Enter로 검색합니다.</p></form>
    <div class="section-heading"><h2>주제별로 읽기</h2><span>핵심 요약 + 상세 규칙 + 근거</span></div><div id="all-chapter-cards"></div>`;
    let current = ''; let html = ''; let opened = false;
    D.chapters.forEach((c,i) => {
      if(c.part!==current){if(opened)html+='</div>';current=c.part;html+=`<h3 class="part-heading">${esc(current)}</h3><div class="chapter-cards">`;opened=true;}
      const done=c.units.filter(u=>state.read.includes(u.id)).length;
      html+=`<a class="chapter-card" href="#chapter/${c.id}"><div class="card-top"><span>CHAPTER ${String(i+1).padStart(2,'0')}</span><span>${done ? done+' / ':''}${c.units.length}절</span></div><h3>${esc(c.title)}</h3><p>${esc(c.summary)}</p></a>`;
    });
    $('#all-chapter-cards').innerHTML=html+(opened?'</div>':'');
    $('#home-search').addEventListener('submit', e => { e.preventDefault(); location.hash='search/'+encodeURIComponent($('#home-query').value); });
  }
  function sourceLinks(ids) {
    return ids.filter(id=>D.sources[id]).map(id=>{
      const s=D.sources[id];
      return `<li><a href="${esc(safeUrl(s.url))}" target="_blank" rel="noopener noreferrer">${esc(s.title || new URL(s.url).hostname)}</a>${s.checked_at ? `<span class="muted"> · 재확인 ${esc(s.checked_at)}</span>`:''}</li>`;
    }).join('');
  }
  function renderUnit(u) {
    return `<section class="reading-unit" id="${u.id}" data-unit="${u.id}"><div class="unit-top"><h2>${esc(u.title)}</h2><div class="unit-controls"><button type="button" data-save="${u.id}" aria-pressed="${state.saved.includes(u.id)}" aria-label="${esc(u.title)} 북마크">${state.saved.includes(u.id)?'저장됨':'북마크'}</button><button type="button" data-read="${u.id}" aria-pressed="${state.read.includes(u.id)}" aria-label="${esc(u.title)} 읽음 표시">${state.read.includes(u.id)?'읽음 ✓':'읽음 표시'}</button></div></div><p class="unit-meta">${esc(kindLabels[u.kind] || '출처 기반 편집')} · 원문 기준 ${esc(u.source_review_date)}</p>${badges(u)}${u.editor_note?`<p class="editor-note">${esc(u.editor_note)}</p>`:''}<div class="unit-body">${u.html}</div><details class="unit-sources"><summary>공식 근거·편집 출처 ${u.source_ids.length ? '· '+u.source_ids.length+'개':''}</summary><p class="origin">통합 위치: ${esc(u.origins.join(' · ') || '새 공식 원문 보완')}. 원문 확인을 승계한 절은 편집일에 모든 법규를 재검증한 것이 아닙니다.</p>${u.source_ids.length?`<ul>${sourceLinks(u.source_ids)}</ul>`:'<p>이 절은 편집 방법·학습 예시입니다. 관련 법적 규칙의 상세 절과 출처를 함께 확인하세요.</p>'}<a href="book.html#${u.id}" target="_blank" rel="noopener">인쇄 가능한 본문에서 보기 ↗</a></details></section>`;
  }
  function renderChapter(ch, target) {
    setToc(ch);
    const index=D.chapters.indexOf(ch);
    reader.innerHTML=`<header class="chapter-head"><p class="breadcrumb"><a href="#home">통합 노트</a> / ${esc(ch.part)}</p><p class="eyebrow">CHAPTER ${String(index+1).padStart(2,'0')} · ${ch.units.length} SECTIONS</p><h1>${esc(ch.title)}</h1><p class="chapter-lede">${esc(ch.summary)}</p>${ch.highlights.length?`<div class="keypoints"><strong>읽기 전에 구별할 것</strong>${ch.highlights.map(x=>`<p>${esc(x)}</p>`).join('')}</div>`:''}</header>
    <div class="reader-toolbar"><div class="left"><span>글자</span><button class="small-button" type="button" data-font="-1" aria-label="본문 글자 작게">A−</button><span id="font-size-label">${state.font}px</span><button class="small-button" type="button" data-font="1" aria-label="본문 글자 크게">A+</button><button class="small-button" id="focus-button" type="button" aria-pressed="${state.focus}">${state.focus?'목차 보이기':'집중 읽기'}</button></div><div class="right"><button class="small-button" id="print-chapter" type="button">이 장 인쇄</button><a class="small-button" href="book.html#chapter-${ch.id}">전체 본문</a></div></div><div class="chapter-body">${ch.units.map(renderUnit).join('')}</div><nav class="chapter-pagination" aria-label="앞뒤 장">${index>0?`<a href="#chapter/${D.chapters[index-1].id}"><small>← 이전 장</small>${esc(D.chapters[index-1].title)}</a>`:'<a href="#home"><small>← 시작 화면</small>전체 목차</a>'}${index<D.chapters.length-1?`<a href="#chapter/${D.chapters[index+1].id}"><small>다음 장 →</small>${esc(D.chapters[index+1].title)}</a>`:'<a href="#saved"><small>다시 읽기 →</small>저장한 절과 학습 기록</a>'}</nav>`;
    reader.querySelectorAll('[data-font]').forEach(b=>b.addEventListener('click',()=>{
      state.font=Math.max(16,Math.min(24,state.font+Number(b.dataset.font)));applyPrefs();save();$('#font-size-label').textContent=state.font+'px';
    }));
    $('#focus-button').addEventListener('click',e=>{state.focus=!state.focus;applyPrefs();save();e.currentTarget.textContent=state.focus?'목차 보이기':'집중 읽기';e.currentTarget.setAttribute('aria-pressed',String(state.focus));});
    $('#print-chapter').addEventListener('click',()=>window.print());
    if(ch.units.length){state.last=target&&units.has(target)?target:ch.units[0].id;save();}
    observer=new IntersectionObserver(entries=>{
      for(const e of entries){if(e.isIntersecting){state.last=e.target.dataset.unit;save();}}
    },{rootMargin:'-90px 0px -65% 0px',threshold:0});
    reader.querySelectorAll('[data-unit]').forEach(el=>observer.observe(el));
  }
  const aliasGroups=[['cii','c2','schedule ii'],['ciii','c3','schedule iii'],['civ','c4','schedule iv'],['cv','c5','schedule v'],['cvi','c6','schedule vi'],['재고','inventory','reconciliation'],['이관','transfer'],['상담','counseling','counsel'],['모르','mor','manager of record'],['유효기간','validity'],['폐기','disposal','destruction'],['미성년','minor'],['갱신','renewal'],['피임','contraception'],['분실','loss'],['도난','theft'],['부작용','adverse'],['보존','retention'],['부분조제','partial'],['조제','dispensing'],['교육','training','ce'],['라벨','label'],['통지','notification'],['법정','statutory']];
  function terms(query){return normalize(query).split(/\s+/).filter(Boolean).slice(0,12).map(t=>[t,...(aliasGroups.find(g=>g.includes(t))||[])]);}
  function score(text,title,query){const groups=terms(query);if(!groups.length)return 0;let points=0;for(const group of groups){const found=group.filter(t=>text.includes(t));if(!found.length)return -1;points+=found.some(t=>title.includes(t))?25:2;}return points+(title.includes(normalize(query))?60:0);}
  const searchable=[...units.values()].map(u=>({u,text:normalize(u.title+' '+u.text+' '+u.chapter.title+' '+u.origins.join(' ')),title:normalize(u.title)}));
  function snippet(text,query){const ts=terms(query).flat();const lower=text.toLocaleLowerCase();let pos=-1;for(const t of ts){const p=lower.indexOf(t);if(p>=0&&(pos<0||p<pos))pos=p;}const start=Math.max(0,pos-55);return (start?'…':'')+text.slice(start,start+190)+(text.length>start+190?'…':'');}
  function highlight(text,query){const ts=terms(query).flat().filter(x=>x.length>1).sort((a,b)=>b.length-a.length);if(!ts.length)return esc(text);const r=new RegExp('('+ts.map(t=>t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|')+')','giu');return text.split(r).map((x,i)=>i%2?'<mark>'+esc(x)+'</mark>':esc(x)).join('');}
  function resultCard(u,q=''){return `<a class="result-card" href="${href(u)}"><small>${esc(u.chapter.title)}${u.flags.includes('open')?' · 적용 경계 확인 필요':''}</small><h2>${highlight(u.title,q)}</h2><p>${highlight(snippet(u.text,q),q)}</p></a>`;}
  function renderSearch(initial=''){
    setToc(null);
    reader.innerHTML=`<header class="chapter-head"><p class="eyebrow">FIND A RULE</p><h1>전체 본문 검색</h1><p class="chapter-lede">법규 번호, 약 이름, 한국어·English 용어로 상세 설명을 찾습니다.</p></header>${searchBox('search-query',initial)}<div class="search-controls"><select id="search-chapter" aria-label="검색할 장"><option value="">모든 장</option>${D.chapters.map(c=>`<option value="${c.id}">${esc(c.title)}</option>`).join('')}</select><select id="search-flag" aria-label="검토 상태 필터"><option value="">모든 상태</option><option value="open">적용 경계 확인 필요</option><option value="date-sensitive">시행일 확인</option><option value="saved">북마크한 절</option></select></div><p id="result-count" class="results-label" role="status"></p><div id="search-results"></div>`;
    function run(){const q=$('#search-query').value;const cid=$('#search-chapter').value;const flag=$('#search-flag').value;
      const rows=searchable.filter(x=>(!cid||x.u.chapter.id===cid)&&(!flag||(flag==='saved'?state.saved.includes(x.u.id):x.u.flags.includes(flag)))).map(x=>({...x,s:q.trim()?score(x.text,x.title,q):0})).filter(x=>x.s>=0).sort((a,b)=>b.s-a.s);
      $('#result-count').textContent=`${rows.length}개 절${rows.length>150?' · 처음 150개 표시, 검색어나 장을 좁혀 주세요.':''}`;
      $('#search-results').innerHTML=rows.length?rows.slice(0,150).map(x=>resultCard(x.u,q)).join(''):'<p class="empty-state">일치하는 절이 없습니다. 짧은 용어, generic name 또는 다른 법규 번호로 검색해 보세요.</p>';
      history.replaceState(null,'','#search/'+encodeURIComponent(q));
    }
    let timer;$('#search-query').addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(run,100);});
    $('#search-chapter').addEventListener('change',run);$('#search-flag').addEventListener('change',run);run();
  }
  function renderDrugs(initial=''){
    setToc(null);
    reader.innerHTML=`<header class="chapter-head"><p class="eyebrow">GENERIC · BRAND · LEGAL CONTEXT</p><h1>약물 사전</h1><p class="chapter-lede">${D.drugs.length}개 성분·조합·제형 항목. 이름을 법적 분류와 제품별 공급 경로에 연결합니다.</p></header><p class="notice">대표·역사적 브랜드가 포함됩니다. 현재 유통, 임상 용량, 자동 대체 가능성 또는 출제를 보장하지 않습니다. DailyMed 조회 링크와 원본 근거 링크는 구별됩니다.</p>${searchBox('drug-query',initial,'약물 검색','예: Adderall, buprenorphine, Narcan')}<div class="search-controls"><select id="drug-schedule" aria-label="Federal schedule 필터"><option value="">모든 분류</option><option value="II">II</option><option value="III">III</option><option value="IV">IV</option><option value="V">V</option><option value="other">기타 · 비통제 · 제품별</option></select></div><p id="drug-count" class="results-label" role="status"></p><div id="drug-results"></div><button id="more-drugs" class="secondary-button" type="button" hidden>더 보기</button>`;
    let limit=30;
    function run(){const q=normalize($('#drug-query').value);const schedule=$('#drug-schedule').value;
      const rows=D.drugs.filter(d=>(!schedule||(schedule==='other'?!['II','III','IV','V'].includes(d.schedule):d.schedule===schedule))&&q.split(/\s+/).every(t=>normalize(d.name+' '+d.form+' '+d.notes+' '+d.legal_status).includes(t)));
      $('#drug-count').textContent=`${rows.length}개 항목 · ${Math.min(limit,rows.length)}개 표시`;
      $('#drug-results').innerHTML=rows.length?rows.slice(0,limit).map(d=>`<article class="drug-card"><span class="badge">${esc(d.id)} · ${esc(d.schedule)}</span><h2>${esc(d.name)}</h2><dl><dt>제형·역할</dt><dd>${esc(d.form)}</dd><dt>Federal / Massachusetts</dt><dd>${esc(d.legal_status)}</dd></dl><p>${esc(d.notes)}</p><div class="actions"><a href="#chapter/drug-directory/${d.unit}">본문의 분류표 →</a><a href="${esc(d.lookup_url)}" target="_blank" rel="noopener noreferrer">DailyMed 공식 조회 ↗</a></div><details class="unit-sources"><summary>원본 연결 근거 ${d.source_ids.length}개</summary><p class="origin">명칭 색인, 법규, 특정 label의 확인 범위는 서로 다릅니다. 조회 결과의 현재 제품 상태를 다시 확인하세요.</p><ul>${sourceLinks(d.source_ids)}</ul></details></article>`).join(''):'<p class="empty-state">일치하는 항목이 없습니다. Generic 또는 다른 브랜드 명칭으로 검색하세요.</p>';
      $('#more-drugs').hidden=rows.length<=limit;history.replaceState(null,'','#drugs/'+encodeURIComponent($('#drug-query').value));
    }
    let timer;$('#drug-query').addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(()=>{limit=30;run();},100);});
    $('#drug-schedule').addEventListener('change',()=>{limit=30;run();});$('#more-drugs').addEventListener('click',()=>{limit+=30;run();});run();
  }
  function renderSaved(){setToc(null);reader.innerHTML='<header class="chapter-head"><p class="eyebrow">YOUR READING DESK</p><h1>북마크 · 다시 읽기</h1><p class="chapter-lede">이 브라우저의 개인 기록입니다. 다른 기기로 옮기려면 학습 기록을 내보내고 가져오세요.</p></header><div class="saved-tabs"><button class="small-button" data-saved-mode="saved" aria-pressed="true">북마크</button><button class="small-button" data-saved-mode="read" aria-pressed="false">읽은 절</button><button class="small-button" data-saved-mode="unread" aria-pressed="false">아직 읽지 않은 절</button></div><p id="saved-count" class="results-label"></p><div id="saved-results"></div>';
    function show(mode){const list=[...units.values()].filter(u=>mode==='unread'?!state.read.includes(u.id):state[mode].includes(u.id));$('#saved-count').textContent=list.length+'개 절';$('#saved-results').innerHTML=list.length?list.map(u=>resultCard(u)).join(''):'<p class="empty-state">아직 기록이 없습니다. 본문의 북마크·읽음 표시 버튼으로 저장하세요.</p>';reader.querySelectorAll('[data-saved-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.savedMode===mode)));}
    reader.querySelectorAll('[data-saved-mode]').forEach(b=>b.addEventListener('click',()=>show(b.dataset.savedMode)));show('saved');
  }
  function renderSources(){setToc(null);reader.innerHTML=`<header class="chapter-head"><p class="eyebrow">EVIDENCE & EDITORIAL TRAIL</p><h1>출처 · 편집 기록</h1><p class="chapter-lede">무엇을 합쳤고, 무엇을 확인했으며, 무엇이 아직 남아 있는지 구분합니다.</p></header><div class="source-method"><h2>이전 파일을 그대로 올린 페이지가 아닙니다</h2><p>${D.stats.input_documents}개 입력 문서의 ${D.stats.input_sections}개 큰 절을 대조해 ${D.stats.chapters}개 주제로 재배열했습니다. ${D.stats.merged_input_sections}개 입력 절은 다른 본문과 통합했고, ${D.stats.metadata_sections_removed}개 출판 메모·주차별 일정·중복 요약은 공통 안내 또는 상세 장으로 대체했습니다. <strong>이 숫자는 법적 정확성·합격 준비도의 백분율이 아닙니다.</strong></p><h2>이번에 보완한 내용</h2><p>Continuity of Care의 14일/30일과 gabapentin 경계는 한 절에 통합했습니다. CE 미충족 통지 교정을 현재 본문에 반영했고, MOR 장기 부재의 잘못된 6.12 참조를 9.23(5)로 바로잡았습니다. 계산대의 lesser-price 의무를 추가하고, packaging policy의 생략을 금지 폐지로 해석하지 않도록 설명했습니다.</p><p>Week 5 원본 출처 등록부를 복원해 REMS·특수 권한·약물 이름의 링크를 다시 연결했습니다. NLM 명칭 색인과 최신 제품 label, 단순 조회 링크는 서로 다르다고 표시했습니다.</p><h2>검증의 경계</h2><p>${esc(D.legal_review_scope)}</p><p>HIV/STI의 개별 statewide DOCX 전문, 일부 규정·정책의 적용 관계, 특정 기관 bed-table 경계, USP 정본의 모든 전문 예외는 해결된 것으로 표시하지 않았습니다. <a href="#chapter/open-register">OPEN 등록부</a>에서 좁은 미확정 범위를 확인하세요.</p><p>이 노트의 북마크·진도는 개인 기기에 저장됩니다. 기존 문제은행의 RELEASED 상태나 independent audit 기록을 변경하지 않습니다.</p><div class="actions"><a class="secondary-button" href="complete-notes.md" download>전체 본문 다운로드</a><a class="secondary-button" href="https://github.com/woojunxnam/oddments/tree/main/notes" target="_blank" rel="noopener noreferrer">편집 원본 · 변경 기록 ↗</a></div></div><div class="section-heading"><h2>연결 근거 ${D.stats.sources}개</h2><span>절별 인용은 해당 본문 끝</span></div>${searchBox('source-query','','출처 검색','FDA, 247 CMR, USP…')}<div id="source-results"></div>`;
    function run(){const q=normalize($('#source-query').value);$('#source-results').innerHTML=Object.values(D.sources).filter(s=>normalize(s.title+' '+s.url).includes(q)).map(s=>`<div class="reference-entry"><a href="${esc(safeUrl(s.url))}" target="_blank" rel="noopener noreferrer">${esc(s.title)}</a><small>${esc(new URL(s.url).hostname)} · ${s.checked_at?'재확인 '+esc(s.checked_at):'기존 노트의 연결 근거 · 일괄 재검증 아님'}</small>${s.scope_note?`<small>${esc(s.scope_note)}</small>`:''}</div>`).join('');}$('#source-query').addEventListener('input',run);run();
  }
  reader.addEventListener('click',e=>{
    const b=e.target.closest('[data-save],[data-read]');if(!b)return;
    const type=b.dataset.save?'saved':'read';const id=b.dataset.save||b.dataset.read;if(!units.has(id))return;
    const active=state[type].includes(id);state[type]=active?state[type].filter(x=>x!==id):[...state[type],id];save();progress();
    b.setAttribute('aria-pressed',String(!active));b.textContent=type==='saved'?(!active?'저장됨':'북마크'):(!active?'읽음 ✓':'읽음 표시');
    toast(type==='saved'?(!active?'북마크에 저장했습니다.':'북마크를 해제했습니다.'):(!active?'읽은 절로 표시했습니다.':'읽음 표시를 해제했습니다.'));
  });
  function download(name,object){const blob=new Blob([JSON.stringify(object,null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
  $('#export-progress').addEventListener('click',()=>download('mpje-notes-progress.json',{application:'oddments-ultimate-notes',edition:D.edition,exported_at:new Date().toISOString(),...state}));
  $('#import-progress').addEventListener('click',()=>$('#progress-file').click());
  $('#progress-file').addEventListener('change',async e=>{
    const f=e.target.files[0];if(!f)return;
    try{if(f.size>2_000_000)throw new Error('파일이 너무 큽니다.');const x=JSON.parse(await f.text());if(x.application!=='oddments-ultimate-notes')throw new Error('이 교재의 학습 기록 파일이 아닙니다.');const imported=validState(x);state={...state,read:[...new Set([...state.read,...imported.read])],saved:[...new Set([...state.saved,...imported.saved])],last:imported.last||state.last};save();progress();render();toast('기존 기록을 보존하면서 가져왔습니다.');}
    catch(err){toast('가져오기 실패: '+err.message);}finally{e.target.value='';}
  });
  let lastRoute='';
  function render(){const raw=location.hash.slice(1);const seg=raw.split('/');const route=seg[0]||'home';const id=seg[1];const target=seg[2];
    if(observer){observer.disconnect();observer=null;}
    document.querySelectorAll('[data-chapter]').forEach(a=>{if(route==='chapter'&&a.dataset.chapter===id)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
    document.title=(route==='chapter'&&chapters.has(id)?chapters.get(id).title+' · ':'')+'MA MPJE 통합 노트';
    if(route==='chapter'&&chapters.has(id))renderChapter(chapters.get(id),target);
    else if(route==='search')renderSearch(decode(id||''));
    else if(route==='drugs')renderDrugs(decode(id||''));
    else if(route==='saved')renderSaved();
    else if(route==='sources')renderSources();
    else if(route==='home')renderHome();
    else{setToc(null);reader.innerHTML='<h1>이 주소의 절을 찾지 못했습니다.</h1><p>이전 판의 링크일 수 있습니다. <a href="#home">전체 목차</a> 또는 <a href="#search">본문 검색</a>을 사용하세요.</p>';}
    progress();applyPrefs();
    requestAnimationFrame(()=>{
      if(route==='chapter'&&target&&$('#'+CSS.escape(target),reader))$('#'+CSS.escape(target),reader).scrollIntoView({behavior:'instant',block:'start'});
      else if(raw!==lastRoute)window.scrollTo({top:0,behavior:'instant'});
      if(route==='search'&&!decode(id||''))$('#search-query')?.focus();
      lastRoute=raw;
    });
  }
  window.addEventListener('hashchange',render);
  document.addEventListener('keydown',e=>{
    if(e.key==='/'&&!e.ctrlKey&&!e.metaKey&&!e.altKey&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement?.tagName)){
      e.preventDefault();if(location.hash.startsWith('#search'))$('#search-query')?.focus();else location.hash='search';
    }
  });
  window.addEventListener('beforeprint',()=>reader.querySelectorAll('.unit-sources').forEach(d=>{d.dataset.beforePrint=String(d.open);d.open=true;}));
  window.addEventListener('afterprint',()=>reader.querySelectorAll('.unit-sources').forEach(d=>{d.open=d.dataset.beforePrint==='true';delete d.dataset.beforePrint;}));
  chapterNavigation();applyPrefs();progress();render();if(!storageOK)save();
})();
