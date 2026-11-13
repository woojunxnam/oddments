/* Chapter 30 fixed five-question sets: individual Check/Retry, shared progress. */
(() => {
  'use strict';
  const all = Array.isArray(window.MPJE_CH30_QUESTIONS) ? window.MPJE_CH30_QUESTIONS : [];
  const view = window.MPJE_CH30_VIEW;
  const progress = window.MPJE_CH30_PROGRESS;
  if (!view || !progress) return;
  const sets = [...new Set(all.map(q => q.set))].sort((a,b) => a-b);
  const key = 'mpje-side-notes-ch30-v1';
  const $ = id => document.getElementById(id);
  const node = (tag, cls, text) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined) n.textContent = text;
    return n;
  };
  let state = {set: sets[0] || 1, answers: {}, checked: {}, submitted: {}};
  try {
    const raw = JSON.parse(localStorage.getItem(key) || '{}');
    if (raw && raw.answers && typeof raw.answers === 'object') {
      state = {
        set: sets.includes(Number(raw.set)) ? Number(raw.set) : sets[0],
        answers: raw.answers,
        checked: raw.checked && typeof raw.checked === 'object' ? raw.checked : {},
        submitted: raw.submitted && typeof raw.submitted === 'object' ? raw.submitted : {}
      };
    }
  } catch (_) { /* Optional browser storage */ }
  // Preserve previously submitted all-five sets without re-counting attempts.
  all.forEach(q => { if (state.submitted[q.set]) state.checked[q.id] = true; });
  const requestedSet = Number(new URLSearchParams(window.location.search).get('set'));
  if (sets.includes(requestedSet)) state.set = requestedSet;
  function save() { try { localStorage.setItem(key, JSON.stringify(state)); } catch (_) {} }
  function questions() { return all.filter(q => q.set === state.set); }
  function selected(q) {
    const values = state.answers[q.id];
    return Array.isArray(values) ? values.filter(x => ['A','B','C','D'].includes(x)) : [];
  }
  function checked(q) { return !!state.checked[q.id]; }
  function correct(q) {
    return selected(q).slice().sort().join(',') === q.correct.slice().sort().join(',');
  }
  function updateStatus() {
    const qs = questions();
    const completed = qs.filter(checked);
    const right = completed.filter(correct).length;
    $('set-progress').textContent = completed.length + '/' + qs.length + ' checked';
    const result = $('score-announcement');
    result.hidden = completed.length === 0;
    if (completed.length) result.textContent =
      'Checked ' + completed.length + ' of ' + qs.length + ' · ' + right +
      ' correct so far. SATA scores only when every correct choice is selected.';
    $('retake-set').hidden = !qs.some(q => checked(q) || selected(q).length > 0);
  }
  function renderTabs() {
    const root = $('set-tabs');
    root.replaceChildren();
    sets.forEach(s => {
      const qs = all.filter(q => q.set === s);
      const count = qs.filter(checked).length;
      const button = node('button', 'exam-tab' + (s === state.set ? ' is-active' : ''),
        'Set ' + s + ' · 5 questions');
      button.type = 'button';
      button.setAttribute('aria-pressed', String(s === state.set));
      button.append(node('small', 'exam-tab-status', count + '/5 checked'));
      button.addEventListener('click', () => switchSet(s));
      root.append(button);
    });
  }
  function renderQuestions() {
    const root = $('question-grid');
    root.replaceChildren();
    const qs = questions();
    $('set-heading').textContent = 'Practice Set ' + state.set;
    $('set-desc').textContent =
      'Check each answer separately, or skip and return later. The key and A–D explanations appear only for the question you check.';
    qs.forEach((q, i) => {
      root.append(view.renderCard(q, {
        index: i, total: qs.length, group: 'fixed', showArea: true,
        getSelected: () => selected(q),
        isChecked: () => checked(q),
        onSelect: answers => { state.answers[q.id] = answers; save(); updateStatus(); },
        onCheck: answers => {
          if (checked(q)) return;
          state.answers[q.id] = answers;
          state.checked[q.id] = true;
          save();
          progress.record(q.id, answers, 'fixed');
          renderTabs();
          updateStatus();
        },
        onRetry: () => {
          delete state.checked[q.id];
          delete state.answers[q.id];
          delete state.submitted[q.set];
          save();
          renderTabs();
          updateStatus();
        }
      }));
    });
    $('prev-set').disabled = state.set === sets[0];
    $('next-set').disabled = state.set === sets[sets.length - 1];
    updateStatus();
  }
  function render() { renderTabs(); renderQuestions(); }
  function switchSet(set) {
    state.set = set;
    save();
    const url = new URL(window.location.href);
    url.searchParams.set('set', String(set));
    window.history.replaceState(null, '', url);
    render();
    $('set-heading').focus();
  }
  $('retake-set').addEventListener('click', () => {
    questions().forEach(q => {
      delete state.checked[q.id];
      delete state.answers[q.id];
    });
    delete state.submitted[state.set];
    save();
    render();
    $('set-heading').focus();
  });
  $('prev-set').addEventListener('click', () => switchSet(sets[Math.max(sets.indexOf(state.set) - 1, 0)]));
  $('next-set').addEventListener('click', () => switchSet(sets[Math.min(sets.indexOf(state.set) + 1, sets.length - 1)]));
  if (!all.length || all.length % 5 !== 0 || sets.length !== all.length / 5 ||
    sets.some(s => {
      const qs = all.filter(q => q.set === s);
      return qs.length !== 5 || qs.filter(q => q.kind === 'single').length !== 3 ||
        qs.filter(q => q.kind === 'multi').length !== 2 ||
        qs.some(q => !q.id || !q.url || q.choices.length !== 4 || !q.correct.length);
    })) {
    $('set-desc').textContent = 'Question data could not be validated; use the chapter library.';
    return;
  }
  save();
  render();
})();
