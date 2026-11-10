/* English MPJE Side Notes: progressively enhance existing answer-card questions. */
(() => {
  'use strict';

  const LETTERS = 'ABCD';

  function element(tag, className, value) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (value !== undefined) node.textContent = value;
    return node;
  }

  function enhanceQuiz(section, quizIndex) {
    const originalQuestions = Array.from(section.querySelectorAll(':scope > details'));
    if (!originalQuestions.length) return;

    // Validate every source question before changing the page. If an author
    // changes the quiz markup, native <details> remains usable as a fallback.
    const questions = originalQuestions.map((details) => {
      const summary = details.querySelector(':scope > summary');
      const answer = details.querySelector(':scope > .answer');
      const options = answer && Array.from(answer.querySelectorAll(':scope > ol.answers > li'));
      const answerHeading = answer && answer.querySelector('p strong');
      const match = answerHeading && answerHeading.textContent.trim()
        .match(/^Correct(?:\s+answer)?:\s*([A-D])\b/i);

      if (!summary || !answer || !options || options.length !== 4 || !match) return null;
      return { details, prompt: summary.textContent.trim(), options, answer, correct: match[1].toUpperCase() };
    });
    if (questions.some((question) => !question)) return;

    const total = questions.length;
    let checkedCount = 0;
    let correctCount = 0;
    const states = [];

    const overview = element('div', 'mcq-overview');
    const progressText = element('span', 'mcq-progress-text');
    const progress = element('progress', 'mcq-progress');
    progress.max = total;
    progress.value = 0;
    progress.setAttribute('aria-label', 'Questions checked');
    overview.append(progressText, progress);
    section.insertBefore(overview, originalQuestions[0]);

    function updateScore() {
      progress.value = checkedCount;
      progressText.textContent = `${checkedCount} of ${total} checked · ${correctCount} correct`;
      scoreText.textContent = checkedCount === total
        ? `Completed: ${correctCount} / ${total} correct`
        : `Score: ${correctCount} / ${total} · ${total - checkedCount} remaining`;
    }

    questions.forEach((question, questionIndex) => {
      const card = element('fieldset', 'mcq-card');
      const legend = element('legend', 'mcq-question', question.prompt);
      const choices = element('div', 'mcq-choices');
      const labels = [];
      const radios = [];

      const actions = element('div', 'mcq-actions');
      const checkButton = element('button', 'mcq-check', 'Check answer');
      checkButton.type = 'button';
      checkButton.disabled = true;
      actions.append(checkButton);

      const feedback = element('div', 'mcq-feedback');
      feedback.hidden = true;
      const result = element('p', 'mcq-result');
      result.setAttribute('role', 'status');
      question.answer.classList.add('mcq-explanations');
      feedback.append(result, question.answer);

      const state = { checked: false, labels, radios, checkButton, feedback, result };

      question.options.forEach((originalOption, optionIndex) => {
        const letter = LETTERS[optionIndex];
        const label = element('label', 'mcq-choice');
        const radio = element('input', 'mcq-radio');
        radio.type = 'radio';
        radio.name = `mpje-quiz-${quizIndex}-question-${questionIndex}`;
        radio.value = letter;
        const letterBadge = element('span', 'mcq-letter', letter);
        const answerText = element('span', 'mcq-choice-text');
        Array.from(originalOption.childNodes).forEach((node) => answerText.append(node.cloneNode(true)));
        label.append(radio, letterBadge, answerText);

        radio.addEventListener('change', () => {
          if (state.checked) return;
          checkButton.disabled = false;
          labels.forEach((item) => {
            item.classList.toggle('is-selected', item.querySelector('input').checked);
          });
        });
        labels.push(label);
        radios.push(radio);
        choices.append(label);
      });

      checkButton.addEventListener('click', () => {
        if (state.checked) return;
        const selected = radios.find((radio) => radio.checked);
        if (!selected) return;
        state.checked = true;
        checkedCount += 1;
        const isCorrect = selected.value === question.correct;
        if (isCorrect) correctCount += 1;

        labels.forEach((label, index) => {
          label.classList.remove('is-selected');
          label.classList.toggle('is-correct-answer', LETTERS[index] === question.correct);
          label.classList.toggle('is-incorrect-answer', radios[index] === selected && !isCorrect);
        });
        radios.forEach((radio) => { radio.disabled = true; });
        checkButton.hidden = true;
        result.classList.toggle('is-success', isCorrect);
        result.classList.toggle('is-error', !isCorrect);
        result.textContent = isCorrect
          ? `Correct — ${question.correct} is the right answer.`
          : `Not quite. The correct answer is ${question.correct}.`;
        feedback.hidden = false;
        updateScore();
      });

      card.append(legend, choices, actions, feedback);
      question.details.replaceWith(card);
      states.push(state);
    });

    const footer = element('div', 'mcq-footer');
    const scoreText = element('strong', 'mcq-score');
    const reset = element('button', 'mcq-reset', 'Try again');
    reset.type = 'button';
    reset.addEventListener('click', () => {
      checkedCount = 0;
      correctCount = 0;
      states.forEach((state) => {
        state.checked = false;
        state.labels.forEach((label) => label.classList.remove(
          'is-selected', 'is-correct-answer', 'is-incorrect-answer'
        ));
        state.radios.forEach((radio) => {
          radio.checked = false;
          radio.disabled = false;
        });
        state.checkButton.disabled = true;
        state.checkButton.hidden = false;
        state.feedback.hidden = true;
        state.result.textContent = '';
        state.result.classList.remove('is-success', 'is-error');
      });
      updateScore();
      if (states[0]) states[0].radios[0].focus();
    });
    footer.append(scoreText, reset);
    section.append(footer);
    section.classList.add('mcq-ready');
    updateScore();
  }

  // Shared chapter order ensures that every existing page receives Previous/Next
  // links without modifying or duplicating the 27 original study guides.
  const CHAPTERS = [
    { slug: 'licensure-ce', title: 'Licensure / CE' },
    { slug: 'personnel', title: 'Personnel / Supervision' },
    { slug: 'pharmacy-mor', title: 'Pharmacy Licensing / MOR' },
    { slug: 'schedules-registration', title: 'Drug Schedules / Registration' },
    { slug: 'prescription-validity', title: 'Prescription Validity' },
    { slug: 'cii-core', title: 'Schedule II Core' },
    { slug: 'cii-partial-outstate', title: 'CII Partial Fills / Out-of-State' },
    { slug: 'refills-transfer', title: 'Refills / Transfers' },
    { slug: 'pmp-oud', title: 'MassPAT / OUD' },
    { slug: 'label-interchange', title: 'Labels / Substitution' },
    { slug: 'counseling-dur', title: 'Counseling / DUR' },
    { slug: 'rems', title: 'FDA REMS' },
    { slug: 'privacy', title: 'HIPAA / Privacy' },
    { slug: 'vaccination-administration', title: 'Vaccinations / Administration' },
    { slug: 'cdtm', title: 'Collaborative Drug Therapy Management' },
    { slug: 'prescribing-public-health', title: 'Pharmacist Prescribing / Public Health' },
    { slug: 'ordering-inventory', title: 'DEA Ordering / Inventory' },
    { slug: 'security-loss-disposal', title: 'Security / Loss / Disposal' },
    { slug: 'storage-shipping', title: 'Storage / Shipping' },
    { slug: 'shared-automation', title: 'Shared Services / Automation' },
    { slug: 'nonsterile-compounding', title: 'Nonsterile Compounding' },
    { slug: 'sterile-compounding', title: 'Sterile Compounding' },
    { slug: 'hd-outsourcing-nuclear', title: 'Hazardous Drugs / 503B / Nuclear' },
    { slug: 'fda-supply-chain', title: 'FDA / DSCSA / Supply Chain' },
    { slug: 'numbers-records', title: 'Numbers / Record Retention' },
    { slug: 'drug-directory', title: 'Drug Directory' },
    { slug: 'open-register', title: 'Open Legal Register' },
    { slug: 'cumulative-practice', title: 'Cumulative Practice (420 available)' }
  ];
  window.MPJE_CHAPTERS = CHAPTERS.map(chapter => ({ ...chapter }));

  // Make the chapter badge, footer, and cross-chapter link labels agree with
  // the canonical order. Original study HTML and legal/Q&A content remain intact.
  function alignChapterNumbers(index) {
    const shown = String(index + 1).padStart(2, '0');
    function retitle(node, chapterNumber) {
      if (!node) return;
      const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT);
      let child;
      while ((child = walker.nextNode())) {
        child.nodeValue = child.nodeValue.replace(/\bChapter\s+\d+\b/gi, 'Chapter ' + chapterNumber);
      }
    }
    retitle(document.querySelector('.hero .eyebrow'), shown);
    retitle(document.querySelector('body > footer'), shown);
    document.title = document.title.replace(/\bChapter\s+\d+\b/i, 'Chapter ' + shown);
    document.querySelectorAll('a[href^="../"]').forEach(anchor => {
      const path = (anchor.getAttribute('href') || '').match(/^\.\.\/([a-z0-9-]+)\/(?:[#?].*)?$/);
      if (!path || !/\bChapter\s+\d+\b/i.test(anchor.textContent)) return;
      const target = CHAPTERS.findIndex(c => c.slug === path[1]);
      if (target >= 0) retitle(anchor, String(target + 1).padStart(2, '0'));
    });
  }

  function addChapterNavigation() {
    const parts = window.location.pathname.split('/').filter(Boolean);
    const last = parts[parts.length - 1];
    const slug = last === 'index.html' ? parts[parts.length - 2] : last;
    const index = CHAPTERS.findIndex(chapter => chapter.slug === slug);
    if (index < 0) return;
    alignChapterNumbers(index);
    if (document.querySelector('.study-chapter-nav')) return;

    const nav = element('nav', 'study-chapter-nav');
    nav.setAttribute('aria-label', 'Previous and next MPJE chapters');
    function link(href, label, className) {
      const anchor = element('a', className || 'study-nav-link', label);
      anchor.href = href;
      return anchor;
    }
    nav.append(link(index > 0 ? '../' + CHAPTERS[index - 1].slug + '/' : '../',
      index > 0 ? '← Previous: ' + CHAPTERS[index - 1].title : '← All chapters'));
    nav.append(link('../', 'All chapters', 'study-nav-link study-nav-library'));
    nav.append(link(index < CHAPTERS.length - 1 ? '../' + CHAPTERS[index + 1].slug + '/' : '../',
      index < CHAPTERS.length - 1 ? 'Next: ' + CHAPTERS[index + 1].title + ' →' : 'All chapters →'));
    if (slug !== 'cumulative-practice') {
      nav.append(link('../cumulative-practice/?chapter=' + encodeURIComponent(slug),
        'Practice ' + (['licensure-ce', 'personnel', 'pharmacy-mor', 'schedules-registration', 'prescription-validity', 'cii-core', 'cii-partial-outstate', 'refills-transfer', 'pmp-oud', 'label-interchange', 'counseling-dur', 'rems', 'privacy', 'vaccination-administration', 'nonsterile-compounding'].includes(slug) ? '20' : '10') + ' questions for this chapter', 'study-nav-link study-nav-practice'));
    }
    const footer = document.querySelector('body > footer') || document.querySelector('footer');
    if (footer) footer.before(nav);
    else document.body.append(nav);
  }

  // Used by Chapter 28 when a selected chapter's original and supplemental
  // questions have loaded. All existing chapter pages continue to work alone.
  window.MPJE_ENHANCE_QUIZZES = () => {
    document.querySelectorAll('section.quiz').forEach(enhanceQuiz);
  };

  function initialize() {
    window.MPJE_ENHANCE_QUIZZES();
    addChapterNavigation();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize, { once: true });
  } else {
    initialize();
  }
})();
