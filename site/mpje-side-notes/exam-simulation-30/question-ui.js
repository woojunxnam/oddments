/* Shared question card: independently check one SBA/SATA, show four explanations,
   bookmark from any mode, and retry without reloading the page. */
(() => {
  'use strict';
  const progress = window.MPJE_CH30_PROGRESS;
  if (!progress) return;
  const LETTERS = ['A', 'B', 'C', 'D'];
  const areaNames = {
    1: 'Licensure / Personnel',
    2: 'Pharmacist Practice',
    3: 'Dispensing Requirements',
    4: 'Pharmacy Operations'
  };
  const el = (tag, cls, content) => {
    const element = document.createElement(tag);
    if (cls) element.className = cls;
    if (content !== undefined) element.textContent = content;
    return element;
  };
  function selectedFor(options) {
    const values = options.getSelected();
    return Array.isArray(values) ? [...new Set(values)].filter(v => LETTERS.includes(v)).sort() : [];
  }
  function isCorrect(q, selected) {
    return [...selected].sort().join(',') === [...q.correct].sort().join(',');
  }
  function updateBookmarks(id) {
    document.querySelectorAll('[data-ch30-bookmark]').forEach(button => {
      if (button.dataset.ch30Bookmark !== id) return;
      const saved = progress.get(id).saved;
      button.textContent = saved ? '★ Saved' : '☆ Save question';
      button.setAttribute('aria-pressed', String(saved));
      button.setAttribute('aria-label', (saved ? 'Remove from saved questions: ' : 'Save question: ') + id);
      button.classList.toggle('is-saved', saved);
    });
  }
  function renderCard(q, options) {
    const chosen = selectedFor(options);
    const checked = !!options.isChecked();
    const card = el('article', 'exam-question ch30-question');
    card.dataset.questionId = q.id;
    card.dataset.area = q.area;
    const header = el('div', 'exam-question-head');
    header.append(el('span', 'exam-number',
      'QUESTION ' + String(options.index + 1).padStart(2, '0') +
      ' / ' + String(options.total).padStart(2, '0')));
    header.append(el('span', 'exam-kind', q.kind === 'multi' ? 'SELECT ALL THAT APPLY' : 'SINGLE BEST ANSWER'));
    if (options.showArea !== false && areaNames[q.area]) {
      header.append(el('span', 'random-area-label', 'AREA ' + q.area + ' · ' + areaNames[q.area]));
    }
    const bookmark = el('button', 'ch30-bookmark');
    bookmark.type = 'button';
    bookmark.dataset.ch30Bookmark = q.id;
    bookmark.addEventListener('click', () => {
      progress.toggleSaved(q.id);
      updateBookmarks(q.id);
    });
    header.append(bookmark);
    card.append(header, el('div', 'exam-topic', q.topic), el('h3', 'exam-stem', q.stem));
    const choiceGroup = el('fieldset', 'exam-choices');
    choiceGroup.append(el('legend', 'sr-only', 'Answer choices for ' + q.id));
    const inputs = [];
    function paint() {
      const picked = selectedFor(options);
      choiceGroup.querySelectorAll('.exam-choice').forEach(label => {
        const input = label.querySelector('input');
        input.checked = picked.includes(input.value);
        label.classList.toggle('is-selected', !checked && input.checked);
      });
      if (checkButton) checkButton.disabled = checked || picked.length === 0;
    }
    q.choices.forEach((choice, i) => {
      const letter = LETTERS[i];
      const label = el('label', 'exam-choice');
      const input = el('input', 'exam-choice-input');
      input.type = q.kind === 'multi' ? 'checkbox' : 'radio';
      input.name = (options.group || 'ch30') + '-' + q.id;
      input.value = letter;
      input.checked = chosen.includes(letter);
      input.disabled = checked;
      label.append(input, el('span', 'exam-letter', letter), el('span', 'exam-choice-text', choice.text));
      if (checked) {
        if (q.correct.includes(letter)) label.classList.add('is-correct');
        else if (input.checked) label.classList.add('is-wrong');
      } else if (input.checked) label.classList.add('is-selected');
      input.addEventListener('change', () => {
        if (options.isChecked()) return;
        const current = new Set(selectedFor(options));
        if (q.kind === 'single') options.onSelect([letter]);
        else {
          if (input.checked) current.add(letter);
          else current.delete(letter);
          options.onSelect([...current]);
        }
        paint();
      });
      choiceGroup.append(label);
      inputs.push(input);
    });
    card.append(choiceGroup);

    let checkButton = null;
    function replaceCard(focusSelector) {
      const replacement = renderCard(q, options);
      card.replaceWith(replacement);
      replacement.querySelector(focusSelector)?.focus({preventScroll: true});
    }
    const actions = el('div', 'exam-actions ch30-question-actions');
    if (!checked) {
      checkButton = el('button', 'primary ch30-check', 'Check this answer');
      checkButton.type = 'button';
      checkButton.disabled = chosen.length === 0;
      checkButton.addEventListener('click', () => {
        if (options.isChecked()) return;
        const selected = selectedFor(options);
        if (!selected.length) return;
        options.onCheck(selected);
        replaceCard('.exam-feedback');
      });
      actions.append(checkButton);
    } else {
      const retry = el('button', 'ch30-retry', 'Try this question again');
      retry.type = 'button';
      retry.addEventListener('click', () => {
        options.onRetry();
        replaceCard('.exam-choice-input');
      });
      actions.append(retry);
      const correct = isCorrect(q, chosen);
      const banner = el('div', 'exam-feedback ' + (correct ? 'exam-right' : 'exam-wrong'),
        (correct ? 'Correct.' : 'Review needed.') + ' Correct answer' +
        (q.correct.length > 1 ? 's' : '') + ': ' + q.correct.join(', ') + '.');
      banner.tabIndex = -1;
      const details = el('div', 'exam-explanations');
      q.choices.forEach((choice, i) => {
        const letter = LETTERS[i];
        const line = el('p', '', letter + ' — ' + choice.why);
        if (q.correct.includes(letter)) line.classList.add('is-keyed');
        details.append(line);
      });
      const reference = el('p', 'exam-reference');
      reference.append(el('strong', '', q.citation + ' · '));
      const link = el('a', '', 'Official legal source');
      link.href = q.url;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      reference.append(link);
      if (q.note) details.append(el('p', 'exam-editor-note', 'Editorial note: ' + q.note));
      card.append(banner, details, reference);
    }
    card.append(actions);
    const record = progress.get(q.id);
    if (record.wrongCount > 0) {
      const history = el('p', 'exam-history', 'Incorrect attempts: ' + record.wrongCount +
        (record.needsReview ? ' · In wrong-answer review' : ' · Reviewed correctly'));
      card.append(history);
    }
    updateBookmarkButton();
    function updateBookmarkButton() {
      const saved = progress.get(q.id).saved;
      bookmark.textContent = saved ? '★ Saved' : '☆ Save question';
      bookmark.classList.toggle('is-saved', saved);
      bookmark.setAttribute('aria-pressed', String(saved));
      bookmark.setAttribute('aria-label', (saved ? 'Remove from saved questions: ' : 'Save question: ') + q.id);
    }
    return card;
  }
  window.MPJE_CH30_VIEW = Object.freeze({renderCard, updateBookmarks, areaNames});
})();
