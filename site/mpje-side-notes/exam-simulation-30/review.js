/* Chapter 30: wrong-answer review and saved-question review.
   Both are interactive and reuse the same per-question checking UI. */
(() => {
  'use strict';
  const progress = window.MPJE_CH30_PROGRESS;
  const view = window.MPJE_CH30_VIEW;
  const all = Array.isArray(window.MPJE_CH30_QUESTIONS) ? window.MPJE_CH30_QUESTIONS : [];
  if (!progress || !view) return;
  const byId = new Map(all.map(q => [q.id, q]));
  const $ = id => document.getElementById(id);
  const views = {
    wrong: {container: $('wrong-question-grid'), count: $('wrong-count'), refresh: $('wrong-refresh'), tries: {}},
    saved: {container: $('saved-question-grid'), count: $('saved-count'), refresh: $('saved-refresh'), tries: {}}
  };
  if (Object.values(views).some(v => !v.container || !v.count || !v.refresh)) return;
  const node = (tag, cls, text) => {
    const element = document.createElement(tag);
    if (cls) element.className = cls;
    if (text !== undefined) element.textContent = text;
    return element;
  };
  function orderedIds(mode) {
    const ids = mode === 'wrong' ? progress.wrongIds() : progress.savedIds();
    return [...ids].sort((a, b) =>
      progress.get(b).wrongCount - progress.get(a).wrongCount ||
      a.localeCompare(b)
    );
  }
  function labelCounts() {
    const counts = progress.count();
    views.wrong.count.textContent = counts.wrong + ' question' + (counts.wrong === 1 ? '' : 's') +
      ' to retry · A correct reattempt removes a question from the active wrong-answer queue.';
    views.saved.count.textContent = counts.saved + ' saved question' + (counts.saved === 1 ? '' : 's') +
      ' · Manually bookmarked items and questions missed at least twice.';
    const badge = $('review-nav-count');
    if (badge) badge.textContent = counts.wrong + ' wrong · ' + counts.saved + ' saved';
    const note = $('ch30-storage-note');
    if (note) note.textContent = progress.storageAvailable ?
      'Review history and bookmarks are stored in this browser (localStorage), not synced to another device.' :
      'Browser storage is unavailable. Review history and bookmarks may disappear when this page closes.';
  }
  function renderList(mode) {
    const current = views[mode];
    const ids = orderedIds(mode);
    const root = current.container;
    root.replaceChildren();
    labelCounts();
    if (!ids.length) {
      root.append(node('p', 'exam-muted ch30-empty', mode === 'wrong' ?
        'No incorrect answers awaiting review. Wrong answers will appear here immediately after you check them.' :
        'No saved questions yet. Use “Save question” in any quiz, or miss a question twice to auto-save it.'));
      return;
    }
    ids.forEach((id, index) => {
      const q = byId.get(id);
      if (!q) return;
      if (!current.tries[id]) current.tries[id] = {selected: [], checked: false};
      const attempt = current.tries[id];
      root.append(view.renderCard(q, {
        index, total: ids.length, group: mode + '-review', showArea: true,
        getSelected: () => attempt.selected,
        isChecked: () => attempt.checked,
        onSelect: picks => { attempt.selected = picks; },
        onCheck: picks => {
          if (attempt.checked) return;
          attempt.selected = picks;
          attempt.checked = true;
          progress.record(q.id, picks, 'review');
          labelCounts();
        },
        onRetry: () => { attempt.checked = false; attempt.selected = []; }
      }));
    });
  }
  views.wrong.refresh.addEventListener('click', () => renderList('wrong'));
  views.saved.refresh.addEventListener('click', () => renderList('saved'));
  progress.subscribe(event => {
    labelCounts();
    if (event.type === 'bookmark') {
      // Changes to a bookmarked card should be reflected in the saved list immediately.
      renderList('saved');
      return;
    }
    if (event.type === 'external') {
      renderList('wrong');
      renderList('saved');
      return;
    }
    if (event.type === 'answer' && event.origin !== 'review') {
      renderList('wrong');
      renderList('saved');
    }
    // During a review attempt, leave the checked card visible so its
    // explanations can be studied before clicking Refresh review list.
  });
  renderList('wrong');
  renderList('saved');
})();
