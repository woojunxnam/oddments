/* Chapter 30 Random 10: legacy-area-balanced sampling with independent question checks.
   Each New Random 10 changes the question combination, with no within-set repetition. */
(() => {
  'use strict';
  const all = Array.isArray(window.MPJE_CH30_QUESTIONS) ? window.MPJE_CH30_QUESTIONS : [];
  const view = window.MPJE_CH30_VIEW;
  const progressStore = window.MPJE_CH30_PROGRESS;
  if (!view || !progressStore) return;
  const quotas = Object.freeze({1: 2, 2: 3, 3: 3, 4: 2});
  const areaIds = Object.keys(quotas);
  const letters = ['A','B','C','D'];
  const storageKey = 'mpje-side-notes-ch30-random10-v1';
  const byId = new Map(all.map(q => [q.id, q]));
  const pool = Object.fromEntries(areaIds.map(a => [a, all.filter(q => q.area === Number(a))]));
  const $ = id => document.getElementById(id);
  const root = $('random-question-grid');
  const summary = $('random-score');
  const progress = $('random-progress');
  const poolInfo = $('random-pool');
  const message = $('random-message');
  const retakeButton = $('random-retake');
  const newButtons = [$('random-new-top'), $('random-new-bottom')];
  if (!root || !summary || !progress || !poolInfo || !message ||
      !retakeButton || newButtons.some(b => !b)) return;

  function randomIndex(length) {
    if (length < 1) throw new Error('Empty random sampling pool');
    if (window.crypto && typeof window.crypto.getRandomValues === 'function') {
      const value = new Uint32Array(1);
      const range = 4294967296;
      const limit = Math.floor(range / length) * length;
      do { window.crypto.getRandomValues(value); } while (value[0] >= limit);
      return value[0] % length;
    }
    return Math.floor(Math.random() * length);
  }
  function shuffle(values) {
    const result = [...values];
    for (let i = result.length - 1; i > 0; i--) {
      const j = randomIndex(i + 1);
      [result[i], result[j]] = [result[j], result[i]];
    }
    return result;
  }
  function signature(ids) { return [...ids].sort().join('|'); }
  function validIds(ids) {
    if (!Array.isArray(ids) || ids.length !== 10 || new Set(ids).size !== 10) return false;
    if (ids.some(id => !byId.has(id))) return false;
    return areaIds.every(a => ids.filter(id => byId.get(id).area === Number(a)).length === quotas[a]);
  }
  function drawDifferent(previous) {
    const last = validIds(previous) ? signature(previous) : null;
    const draw = () => shuffle(areaIds.flatMap(a =>
      shuffle(pool[a]).slice(0, quotas[a]).map(q => q.id)
    ));
    for (let i = 0; i < 100; i++) {
      const ids = draw();
      if (signature(ids) !== last) return ids;
    }
    const ids = draw();
    for (const area of areaIds) {
      const selected = ids.filter(id => byId.get(id).area === Number(area));
      const alternative = pool[area].find(q => !selected.includes(q.id));
      if (alternative) {
        const index = ids.findIndex(id => byId.get(id).area === Number(area));
        ids[index] = alternative.id;
        if (signature(ids) !== last) return shuffle(ids);
      }
    }
    return ids; // Only when no other possible combination exists.
  }
  function validQuestion(q) {
    return q && Number.isInteger(q.area) && q.area >= 1 && q.area <= 4 &&
      ['single','multi'].includes(q.kind) && Array.isArray(q.choices) &&
      q.choices.length === 4 && q.choices.every(c => c && c.text && c.why) &&
      Array.isArray(q.correct) && q.correct.length >= (q.kind === 'single' ? 1 : 2) &&
      q.correct.length <= (q.kind === 'single' ? 1 : 3) &&
      new Set(q.correct).size === q.correct.length &&
      q.correct.every(v => letters.includes(v)) &&
      typeof q.url === 'string' && q.url.startsWith('https://');
  }
  if (all.length !== byId.size || all.some(q => !validQuestion(q)) ||
    areaIds.some(a => pool[a].length < quotas[a])) {
    poolInfo.textContent = 'Insufficient validated questions for Area 1/2/3/4 = 2/3/3/2.';
    message.textContent = 'An unbalanced or repeated-question set will not be substituted.';
    newButtons.forEach(b => { b.disabled = true; });
    return;
  }
  poolInfo.textContent = all.length + ' total original questions · ' + areaIds.map(a =>
    'Area ' + a + ': ' + pool[a].length + ' available').join(' · ');

  let state = null;
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) || 'null');
    if (saved && validIds(saved.ids) && saved.answers && typeof saved.answers === 'object') {
      state = {
        ids: saved.ids, answers: saved.answers,
        checked: saved.checked && typeof saved.checked === 'object' ? saved.checked : {},
        number: Number.isInteger(saved.number) && saved.number > 0 ? saved.number : 1,
        submitted: !!saved.submitted
      };
    }
  } catch (_) { /* Local storage optional. */ }
  if (!state) state = {ids: drawDifferent(null), answers: {}, checked: {}, submitted: false, number: 1};
  if (state.submitted) state.ids.forEach(id => { state.checked[id] = true; });
  function save() { try { localStorage.setItem(storageKey, JSON.stringify(state)); } catch (_) {} }
  function questions() { return state.ids.map(id => byId.get(id)); }
  function selected(q) {
    const values = state.answers[q.id];
    return Array.isArray(values) ? [...new Set(values.filter(v => letters.includes(v)))].sort() : [];
  }
  function checked(q) { return !!state.checked[q.id]; }
  function correct(q) { return selected(q).join(',') === [...q.correct].sort().join(','); }
  function updateProgress() {
    const qs = questions();
    const finished = qs.filter(checked);
    const right = finished.filter(correct).length;
    progress.textContent = 'Random set #' + state.number + ' · ' + finished.length + '/10 checked';
    retakeButton.hidden = !qs.some(q => checked(q) || selected(q).length > 0);
    summary.hidden = finished.length === 0;
    if (finished.length) {
      const areaScores = areaIds.map(a => {
        const attempted = finished.filter(q => q.area === Number(a));
        return 'Area ' + a + ': ' + attempted.filter(correct).length + '/' + attempted.length + ' checked';
      });
      summary.textContent = 'Checked ' + finished.length + '/10 · ' + right +
        ' correct · ' + areaScores.join(' · ') +
        '. Only individually checked questions contribute to this score.';
    } else summary.textContent = '';
  }
  function render() {
    root.replaceChildren();
    const qs = questions();
    message.textContent = 'Random set #' + state.number +
      ' · 2 Area 1, 3 Area 2, 3 Area 3 and 2 Area 4 questions. Check one question at a time; new mixes may share individual questions.';
    qs.forEach((q, index) => {
      root.append(view.renderCard(q, {
        index, total: qs.length, group: 'random', showArea: true,
        getSelected: () => selected(q),
        isChecked: () => checked(q),
        onSelect: picks => { state.answers[q.id] = picks; save(); updateProgress(); },
        onCheck: picks => {
          if (checked(q)) return;
          state.answers[q.id] = picks;
          state.checked[q.id] = true;
          save();
          progressStore.record(q.id, picks, 'random');
          updateProgress();
        },
        onRetry: () => {
          delete state.answers[q.id];
          delete state.checked[q.id];
          state.submitted = false;
          save();
          updateProgress();
        }
      }));
    });
    updateProgress();
  }
  function newRandom() {
    const ids = drawDifferent(state.ids);
    if (signature(ids) === signature(state.ids)) {
      message.textContent = 'No other unique ten-question combination is available yet.';
      return;
    }
    state = {ids, answers: {}, checked: {}, submitted: false, number: state.number + 1};
    save();
    render();
    $('random-practice').scrollIntoView({block: 'start', behavior: 'auto'});
  }
  function retake() {
    state.answers = {};
    state.checked = {};
    state.submitted = false;
    save();
    render();
    $('random-practice').scrollIntoView({block: 'start', behavior: 'auto'});
  }
  newButtons.forEach(button => button.addEventListener('click', newRandom));
  retakeButton.addEventListener('click', retake);
  save();
  render();
})();
