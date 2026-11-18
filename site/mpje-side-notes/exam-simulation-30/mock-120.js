/* Dedicated Chapter 30 120-question timed mocks.
   Fixed, nonadaptive forms; no answers or explanations until completed.
   Existing fixed/random progress keys and question objects are not modified. */
(() => {
  'use strict';
  const KEY = 'mpje-side-notes-ch30-mock120-v1';
  const LETTERS = ['A', 'B', 'C', 'D'];
  const AREA_NAMES = {1: 'Licensure / Personnel', 2: 'Pharmacist Practice',
    3: 'Dispensing Requirements', 4: 'Pharmacy Operations'};
  const questions = Array.isArray(window.MPJE_CH30_QUESTIONS) ? window.MPJE_CH30_QUESTIONS : [];
  const manifest = window.MPJE_CH30_MOCK_FORMS;
  const progress = window.MPJE_CH30_PROGRESS;
  const byId = new Map(questions.map(q => [q.id, q]));
  const $ = id => document.getElementById(id);
  const el = (tag, className, value) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (value !== undefined) node.textContent = value;
    return node;
  };
  const own = (object, key) => Object.prototype.hasOwnProperty.call(object || {}, key);
  const exact = (a, b) => Array.isArray(a) && Array.isArray(b) &&
    [...new Set(a)].sort().join(',') === [...new Set(b)].sort().join(',');
  function fingerprint(input) {
    let hash = 2166136261;
    for (let i = 0; i < input.length; i += 1) hash = Math.imul(hash ^ input.charCodeAt(i), 16777619);
    return (hash >>> 0).toString(16).padStart(8, '0');
  }
  function validateBank() {
    if (!manifest || manifest.schema !== 'MPJE_CH30_FIXED_MOCK_FORMS' ||
        manifest.version !== 1 || manifest.minutes !== 150 ||
        questions.length !== 240 || byId.size !== 240) return 'The 240-question mock bank is not available.';
    if (fingerprint(JSON.stringify(questions)) !== manifest.bankSignature) {
      return 'The question bank differs from the approved mock manifest. Regenerate and review both forms before use.';
    }
    const a = manifest.forms && manifest.forms.A, b = manifest.forms && manifest.forms.B;
    if (!Array.isArray(a) || !Array.isArray(b) || a.length !== 120 || b.length !== 120 ||
        new Set([...a, ...b]).size !== 240 || [...a, ...b].some(id => !byId.has(id))) {
      return 'Mock forms must partition all 240 questions without overlap.';
    }
    for (const ids of [a, b]) {
      const pool = ids.map(id => byId.get(id));
      if (pool.filter(q => q.kind === 'single').length !== 72 ||
          pool.filter(q => q.kind === 'multi').length !== 48 ||
          pool.some(q => !Array.isArray(q.choices) || q.choices.length !== 4 ||
            !Array.isArray(q.correct) || !q.correct.length ||
            q.correct.some(letter => !LETTERS.includes(letter)) ||
            (q.kind === 'single' && q.correct.length !== 1))) {
        return 'Mock form question-type or answer-key validation failed.';
      }
    }
    return '';
  }

  function fresh() { return {version: 1, current: {A: null, B: null}, history: [], activeForm: null, visibleForm: null}; }
  let state = fresh();
  let storageOK = true;
  try {
    localStorage.setItem(KEY + ':probe', '1');
    localStorage.removeItem(KEY + ':probe');
    const value = JSON.parse(localStorage.getItem(KEY) || 'null');
    if (value && value.version === 1 && value.current && Array.isArray(value.history)) {
      state = {...fresh(), ...value, current: {A: value.current.A || null, B: value.current.B || null}};
    }
  } catch (_) { storageOK = false; }
  function save() {
    if (!storageOK) return false;
    try { localStorage.setItem(KEY, JSON.stringify(state)); return true; }
    catch (_) {
      storageOK = false;
      $('mock-running-note').textContent = 'Browser storage failed: changes may be lost. Check storage settings before continuing.';
      return false;
    }
  }
  function idsFor(form) { return manifest.forms[form]; }
  function activeSession() {
    const s = state.current[state.activeForm];
    return s && s.status === 'active' ? s : null;
  }
  function stale(s) { return s && s.bankSignature !== manifest.bankSignature; }
  function formatSeconds(n) {
    n = Math.max(0, Math.ceil(n));
    return Math.floor(n / 3600) + ':' + String(Math.floor(n % 3600 / 60)).padStart(2, '0') +
      ':' + String(n % 60).padStart(2, '0');
  }
  function numberText(n, singular, plural) { return n + ' ' + (n === 1 ? singular : plural); }
  function priorMockExposure() {
    const seen = new Set();
    const completed = [...state.history, ...Object.values(state.current).filter(Boolean)];
    completed.forEach(s => {
      if (s.status !== 'completed') return;
      Object.keys(s.submitted || {}).forEach(id => seen.add(id));
    });
    return seen;
  }
  function newSession(form) {
    const seenInMocks = priorMockExposure();
    const before = {};
    idsFor(form).forEach(id => { before[id] = (progress?.get(id).attempts || 0) > 0 || seenInMocks.has(id); });
    return {form, bankSignature: manifest.bankSignature, version: 1,
      attemptId: form + '-' + Date.now() + '-' + Math.random().toString(36).slice(2, 8),
      status: 'active', startedAt: new Date().toISOString(), deadlineAt: Date.now() + 150 * 60 * 1000,
      index: 0, draft: {}, submitted: {}, exposureAtStart: before, syncedIds: [],
      completedAt: null, finishReason: null};
  }
  function statsFor(s) {
    const ids = idsFor(s.form);
    const groups = Object.fromEntries([1, 2, 3, 4].map(area =>
      [area, {total: 0, submitted: 0, correct: 0}]));
    const seen = {total: 0, submitted: 0, correct: 0};
    const unseen = {total: 0, submitted: 0, correct: 0};
    const wrongTopics = {};
    let correct = 0, submittedCount = 0, skipped = 0;
    ids.forEach(id => {
      const q = byId.get(id);
      const group = groups[q.area], exposure = s.exposureAtStart[id] ? seen : unseen;
      group.total += 1;
      exposure.total += 1;
      if (own(s.submitted, id)) {
        submittedCount += 1; group.submitted += 1; exposure.submitted += 1;
        if (!s.submitted[id].length) skipped += 1;
      }
      if (own(s.submitted, id) && exact(s.submitted[id], q.correct)) {
        correct += 1; group.correct += 1; exposure.correct += 1;
      } else {
        wrongTopics[q.topic] = (wrongTopics[q.topic] || 0) + 1;
      }
    });
    return {correct, total: 120, submittedCount, skipped, unanswered: 120 - submittedCount,
      percentage: Math.round(100 * correct / 120), groups, seen, unseen,
      wrongTopics: Object.entries(wrongTopics).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))};
  }
  function syncProgress(s) {
    if (!progress || typeof progress.record !== 'function') return;
    const previouslySynced = new Set(s.syncedIds || []);
    // Only questions actually submitted by Next are added to global practice progress.
    idsFor(s.form).forEach(id => {
      if (!own(s.submitted, id) || previouslySynced.has(id)) return;
      s.syncedIds ||= [];
      s.syncedIds.push(id);
      previouslySynced.add(id);
      save(); // Mark first so a reload cannot double-count a completed mock answer.
      progress.record(id, s.submitted[id], 'mock-' + s.form);
    });
  }
  function finish(s, reason) {
    if (!s || s.status !== 'active') return;
    s.status = 'completed';
    s.completedAt = new Date().toISOString();
    s.finishReason = reason;
    state.activeForm = null;
    state.visibleForm = s.form;
    save();
    syncProgress(s);
    render();
  }
  function remaining(s) { return Math.max(0, Math.ceil((s.deadlineAt - Date.now()) / 1000)); }
  function checkExpiry() {
    const s = activeSession();
    if (!s) return false;
    if (stale(s)) return false;
    if (s.index >= 120 || remaining(s) === 0) {
      finish(s, s.index >= 120 ? 'submitted' : 'time-expired');
      return true;
    }
    return false;
  }
  function updateTimer() {
    if (checkExpiry()) return;
    const s = activeSession();
    if (!s) return;
    const left = remaining(s);
    $('mock-timer').textContent = formatSeconds(left);
    $('mock-timer').setAttribute('aria-label', formatSeconds(left) + ' remaining');
    $('mock-timer').parentElement.classList.toggle('is-urgent', left <= 5 * 60);
  }
  function statusText(form) {
    const s = state.current[form];
    if (!s) return 'Not started · 120 questions, 150 minutes';
    if (stale(s)) return 'Saved attempt uses a previous question-bank revision · review required';
    if (s.status === 'active') return 'In progress · question ' + Math.min(s.index + 1, 120) +
      ' of 120 · timer continues';
    const stats = statsFor(s);
    return 'Completed · ' + stats.correct + '/120 (' + stats.percentage + '% raw) · ' +
      new Date(s.completedAt).toLocaleDateString();
  }
  function updateDashboard() {
    for (const form of ['A', 'B']) {
      const s = state.current[form], button = $('mock-open-' + form.toLowerCase());
      $('mock-status-' + form.toLowerCase()).textContent = statusText(form);
      button.textContent = !s ? 'Start Exam ' + form :
        s.status === 'completed' ? 'View Exam ' + form + ' results' : 'Resume Exam ' + form;
      button.disabled = !storageOK || (activeSession() && state.activeForm !== form) || !!stale(s);
    }
  }
  function renderRunning(s) {
    $('mock-running-name').textContent = 'Mock Exam ' + s.form + ' · Fixed form';
    $('mock-progress-bar').value = s.index;
    $('mock-position').textContent = 'Question ' + (s.index + 1) + ' of 120';
    $('mock-next').textContent = s.index === 119 ? 'Submit final answer & finish' : 'Submit answer & Next';
    const q = byId.get(idsFor(s.form)[s.index]);
    const card = el('article', 'exam-question mock-exam-card');
    const head = el('div', 'exam-question-head');
    head.append(el('span', 'exam-number', 'QUESTION ' + (s.index + 1) + ' / 120'),
      el('span', 'exam-kind', q.kind === 'multi' ? 'SELECT ALL THAT APPLY' : 'SINGLE BEST ANSWER'));
    card.append(head, el('p', 'exam-topic', 'Area ' + q.area + ' · ' + q.topic),
      el('h3', 'exam-stem', q.stem));
    const fieldset = el('fieldset', 'exam-choices');
    fieldset.append(el('legend', 'sr-only', 'Choose answer to question ' + (s.index + 1)));
    const selected = Array.isArray(s.draft[q.id]) ? s.draft[q.id] : [];
    q.choices.forEach((choice, i) => {
      const letter = LETTERS[i], label = el('label', 'exam-choice');
      const input = el('input', 'exam-choice-input');
      input.type = q.kind === 'multi' ? 'checkbox' : 'radio';
      input.name = 'mock-answer';
      input.value = letter;
      input.checked = selected.includes(letter);
      if (input.checked) label.classList.add('is-selected');
      label.append(input, el('span', 'exam-letter', letter),
        el('span', 'exam-choice-text', choice.text));
      input.addEventListener('change', () => {
        if (!activeSession() || activeSession().attemptId !== s.attemptId ||
            remaining(s) <= 0) { checkExpiry(); return; }
        const answers = [...fieldset.querySelectorAll('input:checked')].map(x => x.value).sort();
        s.draft[q.id] = answers;
        fieldset.querySelectorAll('.exam-choice').forEach(l =>
          l.classList.toggle('is-selected', l.querySelector('input').checked));
        save();
      });
      fieldset.append(label);
    });
    card.append(fieldset);
    $('mock-question').replaceChildren(card);
    $('mock-running-note').textContent = '';
    updateTimer();
  }
  function nextQuestion() {
    const s = activeSession();
    if (!s || checkExpiry()) return;
    const id = idsFor(s.form)[s.index], selected = (s.draft[id] || []).filter(letter => LETTERS.includes(letter));
    if (!selected.length) {
      $('mock-running-note').textContent = 'Select an answer before continuing. The MPJE does not allow skipping.';
      return;
    }
    if (checkExpiry()) return;
    s.submitted[id] = [...new Set(selected)].sort();
    delete s.draft[id];
    s.index += 1;
    save();
    if (s.index === 120) finish(s, 'submitted');
    else {
      render();
      $('mock-running-title').scrollIntoView({block: 'start', behavior: 'auto'});
    }
  }
  function reviewQuestion(s, index) {
    const id = idsFor(s.form)[index], q = byId.get(id);
    const answer = own(s.submitted, id) ? s.submitted[id] : [];
    const checked = own(s.submitted, id);
    const card = el('article', 'exam-question mock-review-card');
    const head = el('div', 'exam-question-head');
    head.append(el('span', 'exam-number', 'QUESTION ' + (index + 1) + ' / 120'),
      el('span', 'exam-kind', q.kind === 'multi' ? 'SELECT ALL THAT APPLY' : 'SINGLE BEST ANSWER'));
    card.append(head, el('p', 'exam-topic', 'Area ' + q.area + ' · ' + q.topic),
      el('h3', 'exam-stem', q.stem));
    card.append(el('p', 'exam-feedback ' + (checked && exact(answer, q.correct) ? 'exam-right' : 'exam-wrong'),
      (checked && exact(answer, q.correct) ? 'Correct' : 'Incorrect or unanswered') +
      ' · Your submitted answer: ' + (answer.length ? answer.join(', ') : 'None') +
      ' · Key: ' + q.correct.join(', ')));
    const choices = el('div', 'exam-choices');
    q.choices.forEach((choice, i) => {
      const letter = LETTERS[i], line = el('div', 'exam-choice');
      if (q.correct.includes(letter)) line.classList.add('is-correct');
      else if (answer.includes(letter)) line.classList.add('is-wrong');
      line.append(el('span', 'exam-letter', letter), el('span', 'exam-choice-text', choice.text));
      // Use a third content column but no live input when reviewing a locked exam.
      line.style.gridTemplateColumns = '25px minmax(0,1fr)';
      choices.append(line);
    });
    card.append(choices);
    const details = el('div', 'mock-explanations');
    details.append(el('h4', '', 'A–D explanations'));
    q.choices.forEach((choice, i) => details.append(el('p', '', LETTERS[i] + ' — ' + choice.why)));
    if (q.note) details.append(el('p', 'exam-editor-note', 'Editorial note: ' + q.note));
    const source = el('p', 'exam-reference', q.citation + ' · Verified: ' + (q.verified || 'date not listed') + ' · ');
    const link = el('a', '', 'Official/primary source');
    link.href = q.url; link.rel = 'noopener noreferrer'; link.target = '_blank';
    source.append(link);
    card.append(details, source);
    $('mock-review').replaceChildren(card);
  }
  function scoreItem(value, label) {
    const div = el('div', 'mock-score-item');
    div.append(el('strong', '', String(value)), el('span', '', label));
    return div;
  }
  function renderResults(s) {
    const summary = statsFor(s);
    $('mock-results-heading').textContent = 'Mock Exam ' + s.form + ' · Results';
    const start = new Date(s.startedAt).getTime(), end = new Date(s.completedAt).getTime();
    const elapsed = Math.max(0, Math.min(9000, Math.round((end - start) / 1000)));
    $('mock-score').replaceChildren(scoreItem(summary.correct + '/120', 'Correct answers'),
      scoreItem(summary.percentage + '%', 'Raw practice score'),
      scoreItem(formatSeconds(elapsed), 'Time elapsed'));
    $('mock-result-note').textContent =
      (s.finishReason === 'time-expired' ? 'The 150-minute timer expired. ' :
       s.finishReason === 'early' ? 'You ended this attempt early. ' : 'All 120 questions were reached. ') +
      summary.submittedCount + '/120 submitted · ' +
      summary.unanswered + ' unanswered when the exam ended. Every unsubmitted answer counts as incorrect. ' +
      'NABP does not calculate an MPJE pass/fail result from this raw percentage.';
    const areaList = el('div', 'mock-area-list');
    for (const area of [1, 2, 3, 4]) {
      const g = summary.groups[area], line = el('div', 'mock-area-line');
      const percentage = Math.round(100 * g.correct / g.total);
      line.append(el('strong', '', 'Area ' + area + ' · ' + AREA_NAMES[area]),
        el('span', '', g.correct + '/' + g.total));
      const bar = el('progress');
      bar.max = g.total; bar.value = g.correct;
      bar.setAttribute('aria-label', 'Area ' + area + ' ' + percentage + '%');
      line.append(bar); areaList.append(line);
    }
    $('mock-area-results').replaceChildren(areaList);
    const exposure = el('div', 'mock-exposure-grid');
    for (const [key, label] of [['unseen', 'Not previously checked in this browser'], ['seen', 'Previously checked in this browser']]) {
      const g = summary[key], box = el('div');
      box.append(el('strong', '', g.correct + '/' + g.submitted),
        el('span', '', label + ' · ' + g.total + ' assigned · ' +
          g.submitted + ' submitted · ' +
          (g.submitted ? Math.round(100 * g.correct / g.submitted) + '% correct' : 'no submitted answers')));
      exposure.append(box);
    }
    $('mock-exposure-results').replaceChildren(exposure);
    $('mock-weak-topics').textContent = summary.wrongTopics.length ?
      summary.wrongTopics.slice(0, 7).map(([topic, n]) => topic + ' (' + n + ')').join(' · ') :
      'No incorrect answers.';
    const picker = $('mock-review-picker');
    picker.replaceChildren();
    idsFor(s.form).forEach((id, i) => {
      const q = byId.get(id), option = el('option', '', (i + 1) + ' · ' + q.topic +
        (own(s.submitted, id) && exact(s.submitted[id], q.correct) ? ' · correct' : ' · review'));
      option.value = String(i);
      picker.append(option);
    });
    picker.value = '0';
    reviewQuestion(s, 0);
    const past = state.history.filter(x => x.form === s.form && x.status === 'completed');
    const rows = past.map(old => {
      const score = statsFor(old);
      return el('p', '', new Date(old.completedAt).toLocaleString() +
        ' · ' + score.correct + '/120 (' + score.percentage + '% raw) · ' + old.finishReason);
    });
    $('mock-history').replaceChildren(...(rows.length ? rows :
      [el('p', '', 'No older saved attempts for this form.')]));
  }
  function render() {
    updateDashboard();
    const bankError = validateBank();
    const s = activeSession();
    if (s && !stale(s) && remaining(s) <= 0) { finish(s, 'time-expired'); return; }
    const visible = state.visibleForm && state.current[state.visibleForm];
    const isRunning = !!s && !stale(s);
    const isDone = !isRunning && !!visible && visible.status === 'completed' && !stale(visible);
    $('mock-dashboard').hidden = isRunning;
    $('mock-running').hidden = !isRunning;
    $('mock-completed').hidden = !isDone;
    if (bankError || !storageOK || (s && stale(s))) {
      $('mock-error').hidden = false;
      $('mock-error').textContent = bankError || (!storageOK ?
        'This browser cannot persist exam answers. Enable site storage to use full-length timed exams.' :
        'The saved in-progress exam has a different bank revision. Do not submit it against changed answer keys.');
      return;
    }
    $('mock-error').hidden = true;
    if (isRunning) renderRunning(s);
    if (isDone) renderResults(visible);
    const active = activeSession();
    $('mock-message').textContent = active ?
      'Mock Exam ' + active.form + ' is active. Finish it before starting the other form; its timer continues even if you leave this page.' :
      'Exam A and Exam B have no repeated question IDs. Completed results remain in this browser.';
  }
  function openForm(form) {
    if (validateBank() || !storageOK) return;
    const active = activeSession();
    if (active && active.form !== form) return;
    const current = state.current[form];
    if (stale(current)) return;
    if (current && current.status === 'completed') {
      state.visibleForm = form; save(); render(); return;
    }
    if (!current) {
      if (!window.confirm('Start Mock Exam ' + form + '? You will have 150 continuous minutes. No backtracking or in-exam explanations.')) return;
      state.current[form] = newSession(form);
    }
    state.activeForm = form;
    state.visibleForm = form;
    save(); render();
    $('mock-running-title').scrollIntoView({block: 'start', behavior: 'auto'});
  }
  function retake() {
    const form = state.visibleForm, session = state.current[form];
    if (!session || session.status !== 'completed' || activeSession()) return;
    if (!window.confirm('Retake Exam ' + form + '? Your completed attempt is saved in history. The new 150-minute clock starts immediately.')) return;
    state.history.push(JSON.parse(JSON.stringify(session)));
    state.current[form] = newSession(form);
    state.activeForm = form;
    state.visibleForm = form;
    save(); render();
  }
  function downloadResult() {
    const session = state.current[state.visibleForm];
    if (!session || session.status !== 'completed') return;
    const payload = {schema: 'MA_MPJE_CH30_MOCK120_RESULT', version: 1, exportedAt: new Date().toISOString(),
      manifestVersion: manifest.version, bankSignature: manifest.bankSignature,
      session: JSON.parse(JSON.stringify(session)), stats: statsFor(session),
      note: 'Original nonadaptive practice, raw score only; not official NABP scoring.'};
    const blob = new Blob([JSON.stringify(payload, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'mpje-ch30-mock-' + session.form + '-' +
      session.completedAt.slice(0, 10) + '.json';
    document.body.append(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  $('mock-open-a').addEventListener('click', () => openForm('A'));
  $('mock-open-b').addEventListener('click', () => openForm('B'));
  $('mock-next').addEventListener('click', nextQuestion);
  $('mock-finish-early').addEventListener('click', () => {
    const s = activeSession();
    if (s && window.confirm('Finish now? Unsubmitted questions will count as incorrect. This attempt cannot be resumed.')) {
      finish(s, 'early');
    }
  });
  $('mock-retake').addEventListener('click', retake);
  $('mock-download').addEventListener('click', downloadResult);
  $('mock-review-picker').addEventListener('change', () => {
    const session = state.current[state.visibleForm];
    if (session && session.status === 'completed') reviewQuestion(session, Number($('mock-review-picker').value));
  });
  window.addEventListener('storage', event => {
    if (event.key !== KEY || !event.newValue) return;
    try {
      const next = JSON.parse(event.newValue);
      if (next && next.version === 1 && next.current) { state = next; render(); }
    } catch (_) {}
  });
  // A saved active session cannot be silently replaced by a new form.
  if (!state.activeForm) {
    for (const form of ['A', 'B']) {
      if (state.current[form]?.status === 'active') { state.activeForm = form; state.visibleForm = form; break; }
    }
  }
  if (validateBank()) {
    $('mock-error').hidden = false;
    $('mock-error').textContent = validateBank();
    $('mock-open-a').disabled = $('mock-open-b').disabled = true;
  } else {
    render();
    setInterval(updateTimer, 1000);
    const wanted = new URLSearchParams(window.location.search).get('form');
    if ((wanted === 'A' || wanted === 'B') && !activeSession() && !state.current[wanted]) {
      $('mock-open-' + wanted.toLowerCase()).focus({preventScroll: true});
    }
  }
})();