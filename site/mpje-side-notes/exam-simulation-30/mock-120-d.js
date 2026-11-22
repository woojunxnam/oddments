/* Isolated Form D timed mock. New exam key; preserve A/B/C results and study progress. */
/* Dedicated Chapter 30 120-question timed mocks.
   Fixed, nonadaptive forms; no answers or explanations until completed.
   Existing fixed/random progress keys and question objects are not modified. */
(() => {
  'use strict';
  const KEY = 'mpje-side-notes-ch30-form-d-mock120-v1';
  const LETTERS = ['A', 'B', 'C', 'D'];
  const AREA_NAMES = {1: 'Pharmacy and Pharmacist Practice', 2: 'Medication Use Process',
    3: 'Regulatory Authority and Legal Obligations', 4: 'Pharmacy Operations'};
  const questions = Array.isArray(window.MPJE_CH30_FORM_D_QUESTIONS) ? window.MPJE_CH30_FORM_D_QUESTIONS : [];
  const manifest = window.MPJE_CH30_FORM_D_MOCK;
  const progress = null; // Do not touch existing A/B question progress.
  const byId = new Map(questions.map(q => [q.id, q]));
  const versions = window.MPJE_CH30_VERSION_HISTORY?.create(manifest, byId);
  const questionFor = (session, id) => versions ? versions.question(session, id) :
    session?.bankSignature === manifest?.bankSignature ? byId.get(id) : null;
  const excludedIds = session => versions?.excludedIds(session) || [];
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
    if (!manifest || manifest.schema !== 'MPJE_CH30_FORM_D_MOCK' ||
        manifest.version !== 1 || manifest.minutes !== 150 ||
        questions.length !== 120 || byId.size !== 120 ||
        manifest.bankSize !== 120) return 'Form D 120-question bank is not available.';
    if (fingerprint(JSON.stringify(questions)) !== manifest.bankSignature) {
      return 'Form D question content differs from its fixed-form manifest. Do not score a changed bank.';
    }
    const c = manifest.forms && manifest.forms.D;
    if (!Array.isArray(c) || c.length !== 120 || new Set(c).size !== 120 ||
        c.some(id => !byId.has(id)) || new Set(c).size !== byId.size) {
      return 'Form D must contain exactly 120 unique known question IDs.';
    }
    for (const q of questions) {
      if (![1,2,3,4].includes(q.area) || !['single','multi'].includes(q.kind) ||
          !Array.isArray(q.choices) || q.choices.length !== 4 ||
          q.choices.some(x => !x || typeof x.text !== 'string' || !x.why) ||
          !Array.isArray(q.correct) || !q.correct.length ||
          q.correct.some(letter => !LETTERS.includes(letter)) ||
          new Set(q.correct).size !== q.correct.length ||
          (q.kind === 'single' && q.correct.length !== 1) ||
          !q.citation || !/^https:\/\//.test(q.url)) {
        return 'Form D item schema or keyed answer validation failed.';
      }
    }
    return '';
  }

  function fresh() { return {version: 1, current: {D: null}, history: [], activeForm: null, visibleForm: null}; }
  let state = fresh();
  let storageOK = true;
  try {
    localStorage.setItem(KEY + ':probe', '1');
    localStorage.removeItem(KEY + ':probe');
    const value = JSON.parse(localStorage.getItem(KEY) || 'null');
    if (value && value.version === 1 && value.current && Array.isArray(value.history)) {
      state = {...fresh(), ...value, current: {D: value.current.D || null}};
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
  function visibleSession() {
    return state.visibleAttemptId ? state.history.find(s => s.attemptId === state.visibleAttemptId &&
      s.form === state.visibleForm) : state.current[state.visibleForm];
  }

  function activeSession() {
    const s = state.current[state.activeForm];
    return s && s.status === 'active' ? s : null;
  }
  function stale(s) { return !!s && !(versions ? versions.canUse(s) : s.bankSignature === manifest.bankSignature); }
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
    if (stale(s)) return null;
    const ids = idsFor(s.form);
    const groups = Object.fromEntries([1, 2, 3, 4].map(area =>
      [area, {total: 0, submitted: 0, correct: 0}]));
    const seen = {total: 0, submitted: 0, correct: 0};
    const unseen = {total: 0, submitted: 0, correct: 0};
    const wrongTopics = {};
    let correct = 0, submittedCount = 0, skipped = 0;
    ids.forEach(id => {
      const q = questionFor(s, id);
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
      excludedQuestionIds: excludedIds(s), readinessEligibleTotal: 120 - excludedIds(s).length,
      wrongTopics: Object.entries(wrongTopics).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))};
  }
  function syncProgress(s) {
    if (!progress || typeof progress.record !== 'function' || stale(s)) return;
    const previouslySynced = new Set(s.syncedIds || []);
    // Only questions actually submitted by Next are added to global practice progress.
    idsFor(s.form).forEach(id => {
      if (!own(s.submitted, id) || previouslySynced.has(id) || excludedIds(s).includes(id)) return;
      s.syncedIds ||= [];
      s.syncedIds.push(id);
      previouslySynced.add(id);
      save(); // Mark first so a reload cannot double-count a completed mock answer.
      progress.record(id, s.submitted[id], 'mock-' + s.form);
    });
  }
  function finish(s, reason) {
    if (!s || s.status !== 'active' || stale(s)) return;
    s.status = 'completed';
    s.completedAt = new Date().toISOString();
    s.finishReason = reason;
    state.activeForm = null;
    state.visibleForm = s.form;
    state.visibleAttemptId = null;
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
    if (!s || stale(s)) return;
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
    for (const form of ['D']) {
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
    const q = questionFor(s, idsFor(s.form)[s.index]);
    const card = el('article', 'exam-question mock-exam-card');
    const head = el('div', 'exam-question-head');
    head.append(el('span', 'exam-number', 'QUESTION ' + (s.index + 1) + ' / 120'),
      el('span', 'exam-kind', q.kind === 'multi' ? 'SELECT ALL THAT APPLY' : 'SINGLE BEST ANSWER'));
    // Topic labels can contain the rule being tested; reveal them only in review.
    card.append(head, el('h3', 'exam-stem', q.stem.replace(/\*\*/g, '')));
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
        if (stale(s) || !activeSession() || activeSession().attemptId !== s.attemptId ||
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
    $('mock-running-note').textContent = versions?.isHistorical(s) ?
      'Resuming the original saved question version. Your answers and timer are preserved; corrected questions will be identified after submission.' : '';
    updateTimer();
  }
  function nextQuestion() {
    const s = activeSession();
    if (!s || stale(s) || checkExpiry()) return;
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
    if (stale(s)) return;
    const id = idsFor(s.form)[index], q = questionFor(s, id);
    const answer = own(s.submitted, id) ? s.submitted[id] : [];
    const checked = own(s.submitted, id);
    const excluded = excludedIds(s).includes(id);
    const changed = versions?.changed(s, id);
    const learningQuestion = changed ? byId.get(id) : q;
    const card = el('article', 'exam-question mock-review-card');
    const head = el('div', 'exam-question-head');
    head.append(el('span', 'exam-number', 'QUESTION ' + (index + 1) + ' / 120'),
      el('span', 'exam-kind', q.kind === 'multi' ? 'SELECT ALL THAT APPLY' : 'SINGLE BEST ANSWER'));
    card.append(head, el('p', 'exam-topic', '2027 Domain ' + q.area + ' · ' + q.topic),
      el('h3', 'exam-stem', q.stem.replace(/\*\*/g, '')));
    if (changed) card.append(el('p', 'exam-editor-note mock-version-notice', excluded ?
      'Historical question — original raw grade retained; excluded from readiness evidence. ' + versions.reason(s, id) :
      'Source/explanation updated; original score unchanged. The original question and answers are retained above.'));
    card.append(el('p', 'exam-feedback ' + (checked && exact(answer, q.correct) ? 'exam-right' : 'exam-wrong'),
      (excluded ? 'Original raw grade: ' : '') +
      (checked && exact(answer, q.correct) ? 'Correct' : 'Incorrect or unanswered') +
      ' · Your submitted answer: ' + (answer.length ? answer.join(', ') : 'None') +
      (versions?.isHistorical(s) ? ' · Original key: ' : ' · Key: ') + q.correct.join(', ')));
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
    if (excluded) {
      details.append(el('h4', '', 'Current corrected study version'),
        el('p', 'mock-current-stem', learningQuestion.stem.replace(/\*\*/g, '')));
      learningQuestion.choices.forEach((choice, i) => details.append(
        el('p', 'mock-current-choice', LETTERS[i] + ' — ' + choice.text)));
      details.append(el('p', '', 'Current key: ' + learningQuestion.correct.join(', ') +
        '. This corrected study version does not change your original raw grade.'));
    }
    details.append(el('h4', '', changed ? 'Current A–D explanations' : 'A–D explanations'));
    learningQuestion.choices.forEach((choice, i) => details.append(el('p', '', LETTERS[i] + ' — ' + choice.why)));
    if (learningQuestion.note) details.append(el('p', 'exam-editor-note', 'Editorial note: ' + learningQuestion.note));
    if (learningQuestion.legalHold) details.append(el('p', 'exam-editor-note',
      'Legal source/scope review remains pending: ' + learningQuestion.legalHold));
    const source = el('p', 'exam-reference', learningQuestion.citation + ' · Source noted: ' +
      (learningQuestion.verified || 'date not listed') + ' · ');
    const link = el('a', '', 'Linked legal source');
    link.href = learningQuestion.url; link.rel = 'noopener noreferrer'; link.target = '_blank';
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
    if (!summary) return;
    $('mock-retake').disabled = !!state.visibleAttemptId;
    $('mock-latest-attempt').hidden = !state.visibleAttemptId;
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
    if (versions?.isHistorical(s)) {
      $('mock-result-note').textContent += ' Original raw score preserved from the saved exam version.';
      if (summary.excludedQuestionIds.length) $('mock-result-note').textContent +=
        ' Excluded from readiness evidence: ' + summary.excludedQuestionIds.join(', ') +
        '. Use the corrected study versions in review.';
    }
    const areaList = el('div', 'mock-area-list');
    for (const area of [1, 2, 3, 4]) {
      const g = summary.groups[area], line = el('div', 'mock-area-line');
      const percentage = Math.round(100 * g.correct / g.total);
      line.append(el('strong', '', '2027 Domain ' + area + ' · ' + AREA_NAMES[area]),
        el('span', '', g.correct + '/' + g.total));
      const bar = el('progress');
      bar.max = g.total; bar.value = g.correct;
      bar.setAttribute('aria-label', '2027 Domain ' + area + ' ' + percentage + '%');
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
      const q = questionFor(s, id), option = el('option', '', (i + 1) + ' · ' + q.topic +
        (own(s.submitted, id) && exact(s.submitted[id], q.correct) ? ' · correct' : ' · review'));
      option.value = String(i);
      picker.append(option);
    });
    picker.value = '0';
    reviewQuestion(s, 0);
    const past = state.history.filter(x => x.form === s.form && x.status === 'completed');
    const rows = past.map(old => {
      const row = el('p');
      const score = statsFor(old);
      row.append(el('span', '', new Date(old.completedAt).toLocaleString() + (score ?
        ' · ' + score.correct + '/120 (' + score.percentage + '% original raw) · ' + old.finishReason :
        ' · Original question version unavailable; score not recomputed.')));
      if (score) {
        if (score.excludedQuestionIds.length) row.append(el('span', '',
          ' · Excluded from readiness evidence: ' + score.excludedQuestionIds.join(', ') + '. '));
        const open = el('button', 'mock-secondary', 'Review saved attempt');
        open.type = 'button';
        open.addEventListener('click', () => {
          state.visibleAttemptId = old.attemptId;
          state.visibleForm = old.form;
          save(); render();
        });
        row.append(open);
      }
      return row;
    });
    $('mock-history').replaceChildren(...(rows.length ? rows :
      [el('p', '', 'No older saved attempts for this form.')]));
  }
  function render() {
    updateDashboard();
    const bankError = validateBank();
    const s = activeSession();
    if (s && !stale(s) && remaining(s) <= 0) { finish(s, 'time-expired'); return; }
    const visible = visibleSession();
    const isRunning = !!s && !stale(s);
    const isDone = !isRunning && !!visible && visible.status === 'completed' && !stale(visible);
    $('mock-dashboard').hidden = isRunning;
    $('mock-running').hidden = !isRunning;
    $('mock-completed').hidden = !isDone;
    if (bankError || !storageOK || (s && stale(s)) || (visible && stale(visible))) {
      $('mock-error').hidden = false;
      $('mock-error').textContent = bankError || (!storageOK ?
        'This browser cannot persist exam answers. Enable site storage to use full-length timed exams.' :
        'The saved exam has an unrecognized question version. Its answers are preserved; scoring and review are blocked to prevent using changed questions.');
      return;
    }
    $('mock-error').hidden = true;
    if (isRunning) renderRunning(s);
    if (isDone) renderResults(visible);
    const active = activeSession();
    $('mock-message').textContent = active ?
      'Mock Exam ' + active.form + ' is active. Finish it before starting the other form; its timer continues even if you leave this page.' :
      'Form D contains 120 new question IDs; its history is saved separately from Exams A/B.';
  }
  function openForm(form) {
    if (validateBank() || !storageOK) return;
    const active = activeSession();
    if (active && active.form !== form) return;
    const current = state.current[form];
    if (stale(current)) return;
    state.visibleAttemptId = null;
    if (current && current.status === 'completed') {
      state.visibleForm = form; save(); render(); return;
    }
    if (!current) {
      if (!window.confirm('Start Mock Exam ' + form + '? You will have 150 continuous minutes. No backtracking or in-exam explanations.')) return;
      state.current[form] = newSession(form);
    }
    state.activeForm = form;
    state.visibleForm = form;
    state.visibleAttemptId = null;
    save(); render();
    $('mock-running-title').scrollIntoView({block: 'start', behavior: 'auto'});
  }
  function retake() {
    const form = state.visibleForm, session = state.current[form];
    if (!session || session.status !== 'completed' || activeSession() || stale(session) || state.visibleAttemptId) return;
    if (!window.confirm('Retake Exam ' + form + '? Your completed attempt is saved in history. The new 150-minute clock starts immediately.')) return;
    state.history.push(JSON.parse(JSON.stringify(session)));
    state.current[form] = newSession(form);
    state.activeForm = form;
    state.visibleForm = form;
    state.visibleAttemptId = null;
    save(); render();
  }
  function downloadResult() {
    const session = visibleSession();
    if (!session || session.status !== 'completed' || stale(session)) return;
    const payload = {schema: 'MA_MPJE_CH30_MOCK120_RESULT', version: 1, exportedAt: new Date().toISOString(),
      manifestVersion: manifest.version, bankSignature: session.bankSignature,
      revisionReview: versions?.describe(session) || {bankSignature: session.bankSignature, excludedQuestionIds: []},
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
  $('mock-open-d').addEventListener('click', () => openForm('D'));
  $('mock-next').addEventListener('click', nextQuestion);
  $('mock-finish-early').addEventListener('click', () => {
    const s = activeSession();
    if (s && window.confirm('Finish now? Unsubmitted questions will count as incorrect. This attempt cannot be resumed.')) {
      finish(s, 'early');
    }
  });
  $('mock-latest-attempt').addEventListener('click', () => {
    state.visibleAttemptId = null; save(); render();
  });
  $('mock-retake').addEventListener('click', retake);
  $('mock-download').addEventListener('click', downloadResult);
  $('mock-review-picker').addEventListener('change', () => {
    const session = visibleSession();
    if (session && session.status === 'completed' && !stale(session)) reviewQuestion(session, Number($('mock-review-picker').value));
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
    for (const form of ['D']) {
      if (state.current[form]?.status === 'active') { state.activeForm = form; state.visibleForm = form; break; }
    }
  }
  if (validateBank()) {
    $('mock-error').hidden = false;
    $('mock-error').textContent = validateBank();
    $('mock-open-d').disabled = true;
  } else {
    render();
    setInterval(updateTimer, 1000);
    const wanted = new URLSearchParams(window.location.search).get('form');
    if (wanted === 'D' && !activeSession() && !state.current[wanted]) {
      $('mock-open-' + wanted.toLowerCase()).focus({preventScroll: true});
    }
  }
})();
