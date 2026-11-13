/* Chapter 30: balanced random ten from the growing, area-tagged question bank.
   Uses the pre-March-2027 NABP Competency Statement areas (1:2, 2:3, 3:3, 4:2).
   A fresh click changes the QUESTION SET, not merely its display order.
   This study tool does not represent the exact distribution of any real MPJE exam. */
(() => {
  'use strict';
  const all = Array.isArray(window.MPJE_CH30_QUESTIONS) ? window.MPJE_CH30_QUESTIONS : [];
  const quotas = Object.freeze({1: 2, 2: 3, 3: 3, 4: 2});
  const labels = Object.freeze({
    1: 'Licensure / Personnel',
    2: 'Pharmacist Practice',
    3: 'Dispensing Requirements',
    4: 'Pharmacy Operations'
  });
  const areaIds = Object.keys(quotas);
  const letters = ['A', 'B', 'C', 'D'];
  const storageKey = 'mpje-side-notes-ch30-random10-v1';
  const byId = new Map(all.map(q => [q.id, q]));
  const pool = Object.fromEntries(areaIds.map(a => [a, all.filter(q => q.area === Number(a))]));
  const $ = id => document.getElementById(id);
  const root = $('random-question-grid');
  const summary = $('random-score');
  const progress = $('random-progress');
  const poolInfo = $('random-pool');
  const message = $('random-message');
  const submitButton = $('random-submit');
  const retakeButton = $('random-retake');
  const newButtons = [$('random-new-top'), $('random-new-bottom')];
  if (!root || !summary || !progress || !poolInfo || !message || !submitButton ||
      !retakeButton || newButtons.some(b => !b)) return;

  const make = (tag, cls, value) => {
    const el = document.createElement(tag);
    if (cls) el.className = cls;
    if (value !== undefined) el.textContent = value;
    return el;
  };
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
  function shuffle(source) {
    const values = [...source];
    for (let i = values.length - 1; i > 0; i--) {
      const j = randomIndex(i + 1);
      [values[i], values[j]] = [values[j], values[i]];
    }
    return values;
  }
  function signature(ids) { return [...ids].sort().join('|'); }
  function validIds(ids) {
    if (!Array.isArray(ids) || ids.length !== 10 || new Set(ids).size !== 10) return false;
    if (ids.some(id => !byId.has(id))) return false;
    return areaIds.every(area => ids.filter(id => byId.get(id).area === Number(area)).length === quotas[area]);
  }
  function drawDifferent(previous) {
    const last = validIds(previous) ? signature(previous) : null;
    const draw = () => shuffle(areaIds.flatMap(area =>
      shuffle(pool[area]).slice(0, quotas[area]).map(q => q.id)
    ));
    for (let attempt = 0; attempt < 100; attempt++) {
      const selected = draw();
      if (signature(selected) !== last) return selected;
    }
    // Deterministic fallback: replace one selected ID with an unused ID
    // from its area. This guarantees a different mix whenever one exists.
    const result = draw();
    for (const area of areaIds) {
      const selected = result.filter(id => byId.get(id).area === Number(area));
      const replacement = pool[area].find(q => !selected.includes(q.id));
      if (replacement) {
        const index = result.findIndex(id => byId.get(id).area === Number(area));
        result[index] = replacement.id;
        if (signature(result) !== last) return shuffle(result);
      }
    }
    // If all areas have exactly their quota, there is only one possible mix.
    return result;
  }
  function validQuestion(q) {
    return q && Number.isInteger(q.area) && q.area >= 1 && q.area <= 4 &&
      ['single', 'multi'].includes(q.kind) && Array.isArray(q.choices) &&
      q.choices.length === 4 && q.choices.every(c => c && c.text && c.why) &&
      Array.isArray(q.correct) && q.correct.length >= 1 &&
      q.correct.every(v => letters.includes(v)) && typeof q.url === 'string' &&
      q.url.startsWith('https://');
  }
  if (all.length !== byId.size || all.some(q => !validQuestion(q)) ||
      areaIds.some(area => pool[area].length < quotas[area])) {
    poolInfo.textContent = 'Insufficient validated questions for a 2 / 3 / 3 / 2 random quiz.';
    message.textContent = 'A full ten-question random set is unavailable; no shorter or unbalanced quiz will be substituted.';
    newButtons.forEach(b => { b.disabled = true; });
    submitButton.disabled = true;
    return;
  }
  const distribution = areaIds.map(area =>
    'Area ' + area + ': ' + pool[area].length + ' available'
  ).join(' · ');
  poolInfo.textContent = all.length + ' total original questions · ' + distribution;

  let state = null;
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) || 'null');
    if (saved && validIds(saved.ids) && saved.answers && typeof saved.answers === 'object') {
      state = {
        ids: saved.ids,
        answers: saved.answers,
        submitted: saved.submitted === true,
        number: Number.isInteger(saved.number) && saved.number > 0 ? saved.number : 1
      };
    }
  } catch (_) { /* Browser storage is optional. */ }
  if (!state) state = {ids: drawDifferent(null), answers: {}, submitted: false, number: 1};
  function save() {
    try { localStorage.setItem(storageKey, JSON.stringify(state)); } catch (_) {}
  }
  function currentQuestions() { return state.ids.map(id => byId.get(id)); }
  function selected(q) {
    const current = state.answers[q.id];
    return Array.isArray(current) ? [...new Set(current.filter(letter => letters.includes(letter)))].sort() : [];
  }
  function isRight(q) { return selected(q).join(',') === [...q.correct].sort().join(','); }
  function isComplete(q) { return selected(q).length > 0; }
  function updateProgress() {
    const qs = currentQuestions();
    const answered = qs.filter(isComplete).length;
    progress.textContent = state.submitted
      ? 'Submitted · ' + qs.filter(isRight).length + '/10 correct'
      : 'Random set #' + state.number + ' · ' + answered + '/10 answered';
    submitButton.disabled = state.submitted || answered !== 10;
    submitButton.hidden = state.submitted;
    retakeButton.hidden = !state.submitted;
  }
  function render() {
    root.replaceChildren();
    const qs = currentQuestions();
    const revealed = state.submitted;
    message.textContent = 'Random set #' + state.number + ' · Exactly 2 Area 1, 3 Area 2, 3 Area 3 and 2 Area 4 questions. ' +
      'All ten are different; another generated set may overlap but will not be identical.';
    qs.forEach((q, index) => {
      const card = make('article', 'exam-question random-question');
      card.dataset.questionId = q.id;
      const head = make('div', 'exam-question-head');
      head.append(make('span', 'exam-number', 'QUESTION ' + String(index + 1).padStart(2, '0') + ' / 10'));
      head.append(make('span', 'exam-kind', q.kind === 'multi' ? 'SELECT ALL THAT APPLY' : 'SINGLE BEST ANSWER'));
      head.append(make('span', 'random-area-label', 'AREA ' + q.area + ' · ' + labels[q.area]));
      card.append(head);
      card.append(make('div', 'exam-topic', q.topic));
      card.append(make('h3', 'exam-stem', q.stem));
      const choices = make('fieldset', 'exam-choices');
      choices.append(make('legend', 'sr-only', 'Choices for ' + q.id));
      q.choices.forEach((choice, optionIndex) => {
        const letter = letters[optionIndex];
        const label = make('label', 'exam-choice');
        const input = make('input', 'exam-choice-input');
        input.type = q.kind === 'multi' ? 'checkbox' : 'radio';
        input.value = letter;
        input.name = 'random-' + q.id;
        input.checked = selected(q).includes(letter);
        input.disabled = revealed;
        const marker = make('span', 'exam-letter', letter);
        label.append(input, marker, make('span', 'exam-choice-text', choice.text));
        if (revealed) {
          if (q.correct.includes(letter)) label.classList.add('is-correct');
          else if (input.checked) label.classList.add('is-wrong');
        } else if (input.checked) label.classList.add('is-selected');
        input.addEventListener('change', () => {
          if (state.submitted) return;
          const set = new Set(selected(q));
          if (q.kind === 'single') state.answers[q.id] = [letter];
          else {
            if (input.checked) set.add(letter);
            else set.delete(letter);
            state.answers[q.id] = [...set];
          }
          choices.querySelectorAll('.exam-choice').forEach(option => {
            option.classList.toggle('is-selected', option.querySelector('input').checked);
          });
          save();
          updateProgress();
        });
        choices.append(label);
      });
      card.append(choices);
      if (revealed) {
        const correct = isRight(q);
        const banner = make('div', 'exam-feedback ' + (correct ? 'exam-right' : 'exam-wrong'),
          (correct ? 'Correct. ' : 'Review needed. ') +
          'Correct answer' + (q.correct.length > 1 ? 's' : '') + ': ' + q.correct.join(', ') + '.');
        const explanations = make('div', 'exam-explanations');
        q.choices.forEach((choice, i) => {
          const line = make('p', '', letters[i] + ' — ' + choice.why);
          if (q.correct.includes(letters[i])) line.classList.add('is-keyed');
          explanations.append(line);
        });
        const cite = make('p', 'exam-reference');
        cite.append(make('strong', '', q.citation + ' · '));
        const anchor = make('a', '', 'Official legal source');
        anchor.href = q.url;
        anchor.target = '_blank';
        anchor.rel = 'noopener noreferrer';
        cite.append(anchor);
        card.append(banner, explanations, cite);
      }
      root.append(card);
    });
    summary.hidden = !revealed;
    if (revealed) {
      const areaSummary = areaIds.map(area => {
        const inArea = qs.filter(q => q.area === Number(area));
        return 'Area ' + area + ': ' + inArea.filter(isRight).length + '/' + inArea.length;
      });
      summary.textContent = 'Score: ' + qs.filter(isRight).length + '/10 fully correct · ' + areaSummary.join(' · ') +
        '. SATA earns credit only for an exact match.';
    } else summary.textContent = '';
    updateProgress();
  }
  function newRandom() {
    const previous = state.ids;
    const ids = drawDifferent(previous);
    if (signature(ids) === signature(previous)) {
      message.textContent = 'The current bank does not contain a second distinct ten-question combination.';
      return;
    }
    state = {ids, answers: {}, submitted: false, number: state.number + 1};
    save();
    render();
    $('random-practice').scrollIntoView({block: 'start', behavior: 'auto'});
  }
  function retake() {
    state.answers = {};
    state.submitted = false;
    save();
    render();
    $('random-practice').scrollIntoView({block: 'start', behavior: 'auto'});
  }
  newButtons.forEach(b => b.addEventListener('click', newRandom));
  submitButton.addEventListener('click', () => {
    if (state.submitted || currentQuestions().some(q => !isComplete(q))) return;
    state.submitted = true;
    save();
    render();
    summary.focus();
  });
  retakeButton.addEventListener('click', retake);
  save();
  render();
})();
