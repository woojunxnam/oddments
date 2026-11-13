/* Chapter 30: five-question exam sessions. All explanations are hidden until submission. */
(() => {
  'use strict';
  const LETTERS = ['A', 'B', 'C', 'D'];
  const batches = window.MPJE_CH30_BATCHES || [];
  const root = document.getElementById('advanced-quiz');
  const picker = document.getElementById('simulation-select');
  const count = document.getElementById('question-count');
  const alert = document.getElementById('quiz-status');

  if (!root || !picker || !count || !alert) return;
  const ids = new Set();
  const valid = batches.length > 0 && batches.every(batch =>
    batch.id && batch.title && Array.isArray(batch.questions) && batch.questions.length === 5 &&
    batch.questions.every(q => {
      if (ids.has(q.id)) return false;
      ids.add(q.id);
      const expected = q.type === 'single' ? 1 : q.type === 'multi' ? 2 : 0;
      return expected > 0 && q.question && Array.isArray(q.choices) && q.choices.length === 4 &&
        q.choices.every(s => typeof s === 'string' && s.length) &&
        Array.isArray(q.feedback) && q.feedback.length === 4 && q.feedback.every(s => typeof s === 'string' && s.length) &&
        Array.isArray(q.correct) && q.correct.length >= expected &&
        q.correct.length <= (q.type === 'single' ? 1 : 3) &&
        new Set(q.correct).size === q.correct.length && q.correct.every(s => LETTERS.includes(s)) &&
        Array.isArray(q.sources) && q.sources.length > 0;
    })
  );
  if (!valid) {
    alert.textContent = 'The question set could not be validated. Please use the chapter library.';
    return;
  }

  const add = (tag, className, text) => {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (text !== undefined) el.textContent = text;
    return el;
  };
  count.textContent = String(batches.reduce((total, batch) => total + batch.questions.length, 0));
  batches.forEach((batch, i) => {
    const opt = document.createElement('option');
    opt.value = batch.id;
    opt.textContent = 'Set ' + (i + 1) + ' · ' + batch.title;
    picker.append(opt);
  });
  const initial = location.hash.substring(1);
  picker.value = batches.some(b => b.id === initial) ? initial : batches[0].id;

  function render() {
    const batch = batches.find(b => b.id === picker.value) || batches[0];
    root.replaceChildren();
    const intro = add('p', 'session-intro', 'Five questions · ' + batch.questions.filter(q => q.type === 'single').length +
      ' single-best-answer · ' + batch.questions.filter(q => q.type === 'multi').length +
      ' select-all-that-apply · Answers unlock only after submitting all five.');
    const form = add('form', 'exam-form');
    form.noValidate = true;
    const states = [];
    const progress = add('p', 'session-progress');
    progress.setAttribute('aria-live', 'polite');

    batch.questions.forEach((q, index) => {
      const card = add('fieldset', 'exam-card');
      const legend = add('legend', 'exam-stem', (index + 1) + '. ' + q.question);
      card.append(legend);
      const type = add('div', 'exam-type', q.type === 'multi' ? 'SELECT ALL THAT APPLY' : 'SINGLE BEST ANSWER');
      card.append(type);
      const options = add('div', 'exam-options');
      const controls = [];
      const labels = [];
      q.choices.forEach((choice, cindex) => {
        const letter = LETTERS[cindex];
        const label = add('label', 'exam-option');
        const input = document.createElement('input');
        input.type = q.type === 'multi' ? 'checkbox' : 'radio';
        input.name = q.id;
        input.value = letter;
        input.setAttribute('aria-label', letter + ': ' + choice);
        const marker = add('span', 'exam-letter', letter);
        const body = add('span', 'exam-option-text', choice);
        label.append(input, marker, body);
        options.append(label);
        controls.push(input);
        labels.push(label);
      });
      card.append(options);
      const feedback = add('section', 'exam-feedback');
      feedback.hidden = true;
      feedback.setAttribute('aria-label', 'Answer and option explanations');
      card.append(feedback);
      form.append(card);
      states.push({q, controls, labels, feedback});
    });

    const footer = add('div', 'exam-controls');
    const submit = add('button', 'exam-submit', 'Submit all 5 answers');
    submit.type = 'submit';
    submit.disabled = true;
    const reset = add('button', 'exam-reset', 'Try this set again');
    reset.type = 'button';
    reset.hidden = true;
    footer.append(submit, reset);
    form.append(footer);
    const result = add('div', 'exam-score');
    result.hidden = true;
    result.setAttribute('role', 'status');
    form.append(result);
    root.append(intro, progress, form);
    let submitted = false;

    function selection(state) {
      return state.controls.filter(c => c.checked).map(c => c.value).sort();
    }
    function updateProgress() {
      const answered = states.filter(s => selection(s).length > 0).length;
      progress.textContent = answered + ' of 5 answered · ' +
        (answered < 5 ? 'Complete all five before submitting.' : 'Ready to submit; answers are still hidden.');
      submit.disabled = answered !== 5 || submitted;
    }
    form.addEventListener('change', () => {
      if (submitted) return;
      states.forEach(s => s.controls.forEach((control, i) => {
        s.labels[i].classList.toggle('is-selected', control.checked);
      }));
      updateProgress();
    });
    function resetSet() {
      submitted = false;
      result.hidden = true;
      result.textContent = '';
      states.forEach(s => {
        s.controls.forEach((control, i) => {
          control.checked = false;
          control.disabled = false;
          s.labels[i].className = 'exam-option';
        });
        s.feedback.replaceChildren();
        s.feedback.hidden = true;
      });
      reset.hidden = true;
      submit.hidden = false;
      updateProgress();
      form.querySelector('input')?.focus();
    }
    reset.addEventListener('click', resetSet);

    form.addEventListener('submit', event => {
      event.preventDefault();
      if (submitted || states.some(s => selection(s).length === 0)) return;
      submitted = true;
      let right = 0;
      states.forEach(s => {
        const picked = selection(s);
        const keys = [...s.q.correct].sort();
        const exact = picked.join(',') === keys.join(',');
        if (exact) right += 1;
        s.controls.forEach((control, i) => {
          control.disabled = true;
          s.labels[i].classList.remove('is-selected');
          s.labels[i].classList.toggle('is-correct-answer', keys.includes(LETTERS[i]));
          s.labels[i].classList.toggle('is-incorrect-selection', control.checked && !keys.includes(LETTERS[i]));
        });
        const verdict = add('p', exact ? 'answer-correct' : 'answer-incorrect',
          (exact ? 'Correct.' : 'Not correct.') + ' Answer: ' + keys.join(', ') + '.');
        s.feedback.append(verdict);
        s.q.feedback.forEach((why, i) => {
          const para = add('p', 'answer-detail', LETTERS[i] + '. ' + why);
          s.feedback.append(para);
        });
        const refs = add('p', 'exam-references', 'Official references: ');
        s.q.sources.forEach((source, i) => {
          if (i) refs.append(document.createTextNode(' · '));
          if (!Array.isArray(source) || !/^https:\/\//.test(source[1])) return;
          const link = add('a', '', source[0]);
          link.href = source[1];
          link.target = '_blank';
          link.rel = 'noopener noreferrer';
          refs.append(link);
        });
        s.feedback.append(refs);
        s.feedback.hidden = false;
      });
      result.hidden = false;
      result.textContent = 'Completed: ' + right + ' / 5 fully correct. Select-all questions count only when the complete answer set is right.';
      progress.textContent = 'All five submitted · ' + right + ' correct.';
      submit.hidden = true;
      reset.hidden = false;
      result.focus({preventScroll:true});
    });
    updateProgress();
    alert.textContent = 'Loaded ' + batch.title + ' — five questions.';
  }

  picker.addEventListener('change', () => {
    history.replaceState(null, '', '#'+ picker.value);
    render();
  });
  render();
})();