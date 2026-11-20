/* Focused post-exam review for A/B, C and mixed mocks. Does not modify grades or existing exam answers. */
(() => {
  'use strict';
  const complete = document.getElementById('mock-completed');
  const picker = document.getElementById('mock-review-picker');
  const review = document.getElementById('mock-review');
  if (!complete || !picker || !review) return;

  const mixed = !!document.querySelector('script[src="mock-120-mixes.js"]');
  const formC = !mixed && !!document.querySelector('script[src="mock-120-c.js"]');
  const examKey = mixed ? 'mpje-side-notes-ch30-mixed-mock120-v1' :
    formC ? 'mpje-side-notes-ch30-form-c-mock120-v1' : 'mpje-side-notes-ch30-mock120-v1';
  const markerKey = 'mpje-side-notes-ch30-mock-review-markers-v1';
  const manifest = mixed ? window.MPJE_CH30_MIXED_MOCK_FORMS :
    formC ? window.MPJE_CH30_FORM_C_MOCK : window.MPJE_CH30_MOCK_FORMS;
  const questions = mixed ?
    [...(window.MPJE_CH30_QUESTIONS || []), ...(window.MPJE_CH30_FORM_C_QUESTIONS || []),
      ...(window.MPJE_CH30_FORM_D_QUESTIONS || [])] :
    formC ? window.MPJE_CH30_FORM_C_QUESTIONS || [] : window.MPJE_CH30_QUESTIONS || [];
  const byId = new Map(questions.map(q => [q.id, q]));
  if (!manifest || !byId.size) return;
  const $ = id => document.getElementById(id);
  const el = (tag, className, content) => {
    const x = document.createElement(tag);
    if (className) x.className = className;
    if (content !== undefined) x.textContent = content;
    return x;
  };
  const isEqual = (a, b) => Array.isArray(a) && Array.isArray(b) &&
    [...new Set(a)].sort().join(',') === [...new Set(b)].sort().join(',');
  const modeNames = {missed: 'Incorrect + unanswered', incorrect: 'Incorrect only',
    unanswered: 'Unanswered only', pending: 'Not yet reviewed', all: 'All questions'};
  const hub = el('section', 'mock-review-hub');
  hub.setAttribute('aria-label', 'Focused post-exam review');
  hub.innerHTML = '<h4>Focused answer review</h4>' +
    '<p class="exam-muted">Start with incorrect and unanswered questions. Pick an item to see your answer, the correct key, every choice explanation, and the linked legal source below. Marking an item reviewed never changes your exam score.</p>' +
    '<div id="review-hub-summary" class="mock-review-summary" aria-live="polite"></div>' +
    '<div class="mock-review-controls">' +
    '<label>Show <select id="review-hub-filter">' +
    '<option value="missed">Incorrect + unanswered</option>' +
    '<option value="incorrect">Incorrect only</option>' +
    '<option value="unanswered">Unanswered only</option>' +
    '<option value="pending">Not yet reviewed</option>' +
    '<option value="all">All questions</option>' +
    '</select></label>' +
    '<label>Find <input id="review-hub-search" type="search" placeholder="Topic, question ID or word" autocomplete="off"></label>' +
    '</div>' +
    '<p id="review-hub-count" class="exam-muted" aria-live="polite"></p>' +
    '<div id="review-hub-list" class="mock-review-index" role="group" aria-label="Choose a question to review"></div>';
  const pickerLabel = picker.closest('label') || picker.parentNode;
  pickerLabel.parentNode.insertBefore(hub, pickerLabel);
  const nav = el('div', 'mock-review-navigation');
  nav.innerHTML = '<button id="review-hub-prev" type="button">Previous in list</button>' +
    '<button id="review-hub-mark" type="button">Mark reviewed</button>' +
    '<button id="review-hub-next" type="button">Next in list</button>' +
    '<button id="review-hub-export" type="button">Export missed (CSV)</button>';
  review.insertAdjacentElement('afterend', nav);

  let activeToken = null;
  let reviewed = new Set();
  let rows = [];
  let currentMode = 'missed';
  let search = '';

  function readLocal(key) {
    try { return JSON.parse(localStorage.getItem(key) || 'null'); }
    catch (_) { return null; }
  }
  function getCurrent() {
    const exam = readLocal(examKey);
    const session = exam?.current?.[exam.visibleForm];
    if (!session || session.status !== 'completed') return null;
    const ids = manifest.forms?.[session.form];
    if (!Array.isArray(ids) || ids.length !== 120 || !ids.every(id => byId.has(id))) return null;
    return {session, ids};
  }
  function loadReviewMarkers(token) {
    const store = readLocal(markerKey);
    return new Set(Array.isArray(store?.records?.[token]) ? store.records[token] : []);
  }
  function saveReviewMarkers() {
    const old = readLocal(markerKey);
    const store = old && old.version === 1 && old.records && typeof old.records === 'object' ?
      old : {version: 1, records: {}};
    store.records[activeToken] = [...reviewed];
    try { localStorage.setItem(markerKey, JSON.stringify(store)); }
    catch (_) { $('review-hub-count').textContent = 'Browser storage unavailable: review markers may not persist.'; }
  }
  function getRows(data) {
    return data.ids.map((id, index) => {
      const q = byId.get(id);
      const submitted = Object.prototype.hasOwnProperty.call(data.session.submitted || {}, id);
      const yourAnswer = submitted ? data.session.submitted[id] : [];
      const correct = submitted && isEqual(yourAnswer, q.correct);
      return {index, id, q, yourAnswer, correct, unanswered: !submitted,
        missed: !correct, reviewed: reviewed.has(id)};
    });
  }
  function filtered() {
    const text = search.trim().toLowerCase();
    return rows.filter(r => {
      if (currentMode === 'missed' && !r.missed) return false;
      if (currentMode === 'incorrect' && (!r.missed || r.unanswered)) return false;
      if (currentMode === 'unanswered' && !r.unanswered) return false;
      if (currentMode === 'pending' && (!r.missed || r.reviewed)) return false;
      return !text || [r.id, r.q.topic, r.q.stem, String(r.q.area)].join(' ').toLowerCase().includes(text);
    });
  }
  function jump(index, scroll) {
    if (!Number.isInteger(index) || index < 0 || index >= rows.length) return;
    picker.value = String(index);
    picker.dispatchEvent(new Event('change', {bubbles: true}));
    draw();
    if (scroll) review.scrollIntoView({block: 'start', behavior: 'auto'});
  }
  function step(delta) {
    const list = filtered();
    if (!list.length) return;
    const current = Number(picker.value);
    const position = list.findIndex(r => r.index === current);
    const next = position < 0 ? (delta > 0 ? 0 : list.length - 1) :
      (position + delta + list.length) % list.length;
    jump(list[next].index, true);
  }
  function draw() {
    const data = getCurrent();
    if (!data || complete.hidden || picker.options.length !== 120) return;
    const token = examKey + ':' + data.session.attemptId;
    if (activeToken !== token) {
      activeToken = token;
      reviewed = loadReviewMarkers(token);
      rows = getRows(data);
      // On a newly finished exam, prioritize the first mistake instead of forcing a 120-option dropdown search.
      const firstWrong = rows.find(r => r.missed);
      if (firstWrong && picker.value === '0') {
        picker.value = String(firstWrong.index);
        picker.dispatchEvent(new Event('change', {bubbles: true}));
      }
    } else rows = getRows(data);
    const missed = rows.filter(r => r.missed);
    const wrong = missed.filter(r => !r.unanswered);
    const skipped = missed.filter(r => r.unanswered);
    const done = missed.filter(r => r.reviewed);
    const total = rows.length;
    const summary = $('review-hub-summary');
    summary.replaceChildren();
    for (const [n, label] of [[wrong.length,'Incorrect'], [skipped.length,'Unanswered'],
      [done.length+'/'+missed.length,'Missed items reviewed'],
      [total-missed.length,'Correct']]) {
      const cell = el('div', 'mock-review-counter');
      cell.append(el('strong','',String(n)),el('span','',label));
      summary.append(cell);
    }
    const visible = filtered();
    $('review-hub-count').textContent = visible.length ?
      visible.length + ' question(s) in ' + modeNames[currentMode] + ' · Select any question below.' :
      'No questions match this view. Choose another filter or search term.';
    const list = $('review-hub-list');
    list.replaceChildren();
    const index = Number(picker.value);
    visible.forEach(r => {
      const b = el('button','mock-review-item');
      b.type='button';
      b.dataset.index=String(r.index);
      b.setAttribute('aria-current', r.index === index ? 'true' : 'false');
      b.classList.toggle('is-current',r.index===index);
      b.classList.toggle('is-reviewed',r.reviewed);
      b.append(el('strong','', 'Q'+(r.index+1)+' · '+r.id),
        el('span','mock-review-topic',r.q.topic),
        el('small','',r.unanswered ? 'Unanswered' :
          r.correct ? 'Correct' : 'Your: '+(r.yourAnswer.join(', ')||'—')+' · Key: '+r.q.correct.join(', ')));
      if (r.reviewed) b.append(el('span','mock-reviewed-indicator','Reviewed'));
      b.addEventListener('click',()=>jump(r.index,true));
      list.append(b);
    });
    const selected = rows[index];
    const mark = $('review-hub-mark');
    mark.disabled = !selected || !selected.missed;
    mark.textContent = selected?.reviewed ? 'Mark as still to review' : 'Mark reviewed';
    $('review-hub-prev').disabled = !visible.length;
    $('review-hub-next').disabled = !visible.length;
    $('review-hub-export').disabled = !missed.length;
    if (selected) {
      review.setAttribute('data-current-question-id',selected.id);
      // Keep the existing official-source and full explanation renderer intact.
      const h = review.querySelector('.exam-number');
      if (h && !h.textContent.includes(selected.id)) h.textContent += ' · ' + selected.id;
    }
  }
  function exportMissed() {
    const data = getCurrent();
    if (!data) return;
    const miss = getRows(data).filter(r=>r.missed);
    if (!miss.length) return;
    const quote = x => '"' + String(x ?? '').replace(/"/g,'""').replace(/\r?\n/g,' ') + '"';
    const lines = [['Form','Question','Question ID','Area','Topic','Your answer','Correct answer',
      'Status','Reviewed','Citation','Source URL'].map(quote).join(',')];
    miss.forEach(r => lines.push([data.session.form,r.index+1,r.id,r.q.area,r.q.topic,
      r.yourAnswer.join(' ')||'Unanswered',r.q.correct.join(' '),r.unanswered?'Unanswered':'Incorrect',
      r.reviewed?'Yes':'No',r.q.citation,r.q.url].map(quote).join(',')));
    const blob = new Blob(['\uFEFF'+lines.join('\r\n')],{type:'text/csv;charset=utf-8'});
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href=url;
    anchor.download='mpje-'+data.session.form.toLowerCase()+'-missed-'+
      (data.session.completedAt||'results').slice(0,10)+'.csv';
    document.body.append(anchor);
    anchor.click();
    anchor.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  $('review-hub-filter').addEventListener('change',e=>{currentMode=e.target.value;draw();});
  $('review-hub-search').addEventListener('input',e=>{search=e.target.value;draw();});
  $('review-hub-prev').addEventListener('click',()=>step(-1));
  $('review-hub-next').addEventListener('click',()=>step(1));
  $('review-hub-mark').addEventListener('click',()=>{
    const r=rows[Number(picker.value)];
    if (!r?.missed) return;
    if (reviewed.has(r.id)) reviewed.delete(r.id); else reviewed.add(r.id);
    saveReviewMarkers();
    draw();
  });
  $('review-hub-export').addEventListener('click',exportMissed);
  picker.addEventListener('change',()=>draw());
  new MutationObserver(draw).observe(picker,{childList:true});
  new MutationObserver(draw).observe(complete,{attributes:true,attributeFilter:['hidden']});
  window.addEventListener('storage',e=>{
    if (e.key===examKey || e.key===markerKey) {
      if (e.key===markerKey && activeToken) reviewed=loadReviewMarkers(activeToken);
      draw();
    }
  });
  draw();
})();
