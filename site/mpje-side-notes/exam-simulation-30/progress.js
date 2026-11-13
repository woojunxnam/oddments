/* Chapter 30 personal practice state: question-level attempts, review queue and bookmarks.
   Stored only in this browser; no server account or cross-device sync. */
(() => {
  'use strict';
  const KEY = 'mpje-side-notes-ch30-question-progress-v1';
  const all = Array.isArray(window.MPJE_CH30_QUESTIONS) ? window.MPJE_CH30_QUESTIONS : [];
  const known = new Map(all.map(q => [q.id, q]));
  const subscribers = new Set();
  const blank = () => ({attempts: 0, wrongCount: 0, needsReview: false, saved: false, lastCorrect: null});
  const fresh = () => ({version: 1, items: {}, migratedFixed: false, migratedRandom: false});
  let state = fresh();
  let storageAvailable = true;
  try {
    const raw = JSON.parse(localStorage.getItem(KEY) || 'null');
    if (raw && raw.version === 1 && raw.items && typeof raw.items === 'object') {
      state = {version: 1, items: raw.items, migratedFixed: !!raw.migratedFixed, migratedRandom: !!raw.migratedRandom};
    }
    localStorage.setItem(KEY, JSON.stringify(state));
  } catch (_) { storageAvailable = false; }

  function item(id) {
    const value = state.items[id];
    if (!value || typeof value !== 'object') return blank();
    return {
      attempts: Number.isInteger(value.attempts) && value.attempts >= 0 ? value.attempts : 0,
      wrongCount: Number.isInteger(value.wrongCount) && value.wrongCount >= 0 ? value.wrongCount : 0,
      needsReview: value.needsReview === true,
      saved: value.saved === true,
      lastCorrect: typeof value.lastCorrect === 'boolean' ? value.lastCorrect : null
    };
  }
  function persist() {
    if (storageAvailable) {
      try { localStorage.setItem(KEY, JSON.stringify(state)); }
      catch (_) { storageAvailable = false; }
    }
  }
  function emit(info) {
    subscribers.forEach(fn => {
      try { fn(info); } catch (_) { /* One subscriber cannot break checking. */ }
    });
    window.dispatchEvent(new CustomEvent('mpje-ch30-progress', {detail: info}));
  }
  function isCorrect(q, choices) {
    const selected = Array.isArray(choices) ? [...new Set(choices)].sort() : [];
    return selected.join(',') === [...q.correct].sort().join(',');
  }
  function record(id, selected, origin = 'quiz') {
    const q = known.get(id);
    if (!q) return null;
    const correct = isCorrect(q, selected);
    const current = item(id);
    current.attempts += 1;
    current.lastCorrect = correct;
    if (correct) {
      current.needsReview = false;
    } else {
      current.wrongCount += 1;
      current.needsReview = true;
      if (current.wrongCount >= 2) current.saved = true;
    }
    state.items[id] = current;
    persist();
    emit({type: 'answer', id, correct, origin});
    return correct;
  }
  function setSaved(id, value) {
    if (!known.has(id)) return false;
    const current = item(id);
    current.saved = !!value;
    state.items[id] = current;
    persist();
    emit({type: 'bookmark', id, saved: current.saved});
    return current.saved;
  }
  function toggleSaved(id) { return setSaved(id, !item(id).saved); }
  function wrongIds() { return all.filter(q => item(q.id).needsReview).map(q => q.id); }
  function savedIds() { return all.filter(q => item(q.id).saved).map(q => q.id); }
  function count() {
    return {wrong: wrongIds().length, saved: savedIds().length,
      attempted: all.filter(q => item(q.id).attempts > 0).length};
  }
  // Migrate old all-at-once submissions once, without re-counting on refresh.
  // Previously reset attempts cannot be reconstructed; no incorrect-history fabrication.
  function migrate() {
    function importSelections(ids, answers) {
      ids.forEach(id => {
        const q = known.get(id);
        const picked = answers?.[id];
        if (!q || !Array.isArray(picked) || !picked.length) return;
        const correct = isCorrect(q, picked);
        const current = item(id);
        current.attempts += 1;
        current.lastCorrect = correct;
        if (!correct) {
          current.wrongCount += 1;
          current.needsReview = true;
          if (current.wrongCount >= 2) current.saved = true;
        } else current.needsReview = false;
        state.items[id] = current;
      });
    }
    if (!state.migratedFixed) {
      try {
        const old = JSON.parse(localStorage.getItem('mpje-side-notes-ch30-v1') || '{}');
        if (old.answers && old.submitted) {
          const ids = all.filter(q => old.submitted[q.set]).map(q => q.id);
          importSelections(ids, old.answers);
        }
      } catch (_) { /* Missing or invalid old data is safe to ignore. */ }
      state.migratedFixed = true;
    }
    if (!state.migratedRandom) {
      try {
        const old = JSON.parse(localStorage.getItem('mpje-side-notes-ch30-random10-v1') || '{}');
        if (old.submitted === true && Array.isArray(old.ids)) {
          importSelections(old.ids, old.answers);
        }
      } catch (_) { /* Missing or invalid old data is safe to ignore. */ }
      state.migratedRandom = true;
    }
    persist();
  }
  migrate();
  window.addEventListener('storage', event => {
    if (event.key !== KEY || !event.newValue) return;
    try {
      const remote = JSON.parse(event.newValue);
      if (!remote || remote.version !== 1 || !remote.items) return;
      state = remote;
      emit({type: 'external'});
    } catch (_) { /* Do not apply corrupt cross-tab data. */ }
  });
  window.MPJE_CH30_PROGRESS = Object.freeze({
    get: item, record, setSaved, toggleSaved, wrongIds, savedIds, count,
    get storageAvailable() { return storageAvailable; },
    subscribe(fn) { subscribers.add(fn); return () => subscribers.delete(fn); }
  });
})();
