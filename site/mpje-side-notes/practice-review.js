/* Cumulative practice, Chapter 28. Loads the source chapter quizzes unchanged.\n   Automatically synthesized error-analysis exercises were withdrawn after a\n   quality review; only separately authored supplemental cases remain. */
(() => {
  'use strict';
  const letters = 'ABCD';
  const select = document.getElementById('practice-chapter');
  const status = document.getElementById('review-status');
  const chapterTitle = document.getElementById('review-chapter-title');
  const original = document.getElementById('review-original');
  const extra = document.getElementById('review-extra');
  const moderate = document.getElementById('review-moderate');
  const hard = document.getElementById('review-hard');
  const prev = document.getElementById('review-prev');
  const next = document.getElementById('review-next');
  const guide = document.getElementById('review-source');
  const chapters = (window.MPJE_CHAPTERS || []).filter(c => c.slug !== 'cumulative-practice' && c.slug !== 'drug-memorization');
  let request = 0;

  if (!chapters.length || !select || !original || !extra || !moderate || !hard) {
    if (status) status.textContent = 'The practice chapter list could not load. Open the individual guides.';
    return;
  }
  chapters.forEach((c, i) => {
    const option = document.createElement('option');
    option.value = c.slug;
    option.textContent = String(i + 1).padStart(2, '0') + '. ' + c.title;
    select.append(option);
  });

  const manuallyAuthored = [
    {
      question: 'A pharmacist follows manufacturer directions to reconstitute an antibiotic but then adds a patient-specific flavoring. How should the additional step be evaluated?',
      choices: ['All flavoring is automatically FDA-approved dispensing', 'The manufacturer-directed reconstitution is distinct from additional compounding, which must satisfy applicable rules', 'The entire preparation is exempt from MA law because water was added first', 'Adding flavoring always qualifies as sterile compounding'],
      answer: 'B',
      explanations: ['Adding an extra formulation step does not make it an FDA-approved manufacturer product.', 'Correct. The additional flavoring is separately evaluated as compounding.', 'Manufacturer directions do not waive rules on later alterations.', 'A nonsterile product does not become sterile merely because of flavoring.']
    },
    {
      question: 'A bulk active ingredient is offered to a compounding pharmacy without a reliable certificate of analysis. What is the correct first response?',
      choices: ['Use it because a website calls the powder 100% pure', 'Dispense a compounded preparation if the prescriber approves its price', 'Require an eligible ingredient source and the proper documentation before compounding', 'Assume every bulk ingredient is FDA-approved for the finished indication'],
      answer: 'C',
      explanations: ['A purity claim alone does not establish lawful source or quality.', 'Price and prescriber approval do not replace bulk-substance safeguards.', 'Correct. A proper COA/source and other conditions are needed.', 'FDA facility registration or ingredient status is not finished-drug approval.']
    },
    {
      question: 'A pharmacy is out of stock of a commercially marketed drug and wants to routinely compound copies for all patients. Which statement is safest?',
      choices: ['A local stockout alone is not automatic authority to compound copies; check actual patient differences, current shortage status, and federal/MA restrictions', 'Any local stockout permanently exempts the pharmacy from 503A', 'Copies are always allowed if they cost less', 'An FDA shortage announcement makes a compound FDA-approved'],
      answer: 'A',
      explanations: ['Correct. Source-specific exceptions and patient needs matter.', 'A local shortage does not erase federal and state conditions.', 'Cost alone is not sufficient under the MA copies policy.', 'Compounded preparations are not thereby FDA-approved.']
    },
    {
      question: 'A pharmacy produces an anticipatory nonsterile preparation based on its prior patient-prescription history. Can it dispense that preparation without a valid patient-specific prescription?',
      choices: ['Yes, because anticipation means unlimited office stock', 'Yes, whenever the ingredients are from an authorized wholesaler', 'Yes, provided the product does not have a REMS', 'No; eligible anticipatory preparation and lawful patient-specific dispensing are distinct requirements'],
      answer: 'D',
      explanations: ['Anticipatory preparation does not create unrestricted office-use authority.', 'Supply source is not a patient-specific dispensing authorization.', 'REMS status is unrelated to the patient-specific prescription condition.', 'Correct. The intended patient still needs the legally required prescription before dispensing.']
    },
    {
      question: 'A compounded drug preparation was made under the federal 503A pathway. What does meeting the pathway generally mean?',
      choices: ['The FDA approved that particular compounded preparation', 'Certain conditional exemptions may apply; federal and Massachusetts compounding requirements remain', 'The product may be sold to any wholesaler without restrictions', 'All quality and patient-safety duties are waived'],
      answer: 'B',
      explanations: ['503A eligibility is not individual FDA finished-drug approval.', 'Correct. 503A is a conditional statutory exemption framework.', 'Wholesale/office-use distribution is not automatically permitted.', '503A does not eliminate applicable compounding quality requirements.']
    },
    {
      question: 'A pharmacist confuses two separate federal “5%” limits involving compounded drugs and controlled stock. What is the critical distinction?',
      choices: ['The percentages always use identical prescription denominators', 'They apply only to prescription naloxone', 'The FDA 503A interstate measure and the DEA practitioner distribution measure use different activities and denominators', 'Either limit is automatically waived when a drug is Schedule II'],
      answer: 'C',
      explanations: ['The sources use different denominators and activities.', 'Neither is a naloxone-specific exception.', 'Correct. Do not use DEA dosage-unit calculations for the FDA compounded-prescription measure.', 'Controlled classification does not automatically waive either rule.']
    },
    {
      question: 'An MA retail pharmacy proposes complex nonsterile compounding. Which licensing distinction matters?',
      choices: ['The complex nonsterile pharmacy license may be an additional requirement beyond the Drug Store license', 'A retail pharmacist’s individual license substitutes for all facility licenses', 'Any nonsterile reconstitution is automatically complex compounding', 'A federal 503B outsourcing registration is always mandatory for every simple nonsterile recipe'],
      answer: 'A',
      explanations: ['Correct. Complex nonsterile activity has a separate MA facility license category.', 'Facility licensure and personal licensure are not interchangeable.', 'The category depends on preparation, not merely adding diluent per manufacturer directions.', 'Ordinary 503A pharmacy compounding does not automatically require 503B registration.']
    },
    {
      question: 'A pharmacy receives a manufacturer-premeasured kit for patient-specific compounding. Which statement applies?',
      choices: ['Every kit is legally exempt from all USP compounding standards', 'A commercial kit automatically counts as FDA approval of the newly mixed preparation', 'A pharmacist never needs to assess components because they are premeasured', 'Use of a kit does not itself remove applicable compounding and patient-safety duties'],
      answer: 'D',
      explanations: ['Kits do not create universal USP exemptions.', 'A compounded finished product is not automatically FDA-approved.', 'Ingredients and preparation still require assessment.', 'Correct. Kit-based preparations must meet applicable professional requirements.']
    },
    {
      question: 'A prescriber documents a clinically meaningful dye intolerance and orders a dye-free preparation of an otherwise available medicine. What is the strongest legal argument?',
      choices: ['A lower compound price is always sufficient', 'The documented patient-specific significant difference may fit a conditional copy exception, subject to all remaining legal requirements', 'The prescription may be dispensed without verifying its validity', 'A different flavor or color is always enough without documentation'],
      answer: 'B',
      explanations: ['Cost alone does not justify compounding a copy.', 'Correct. A clinically significant patient-specific difference can be important under the copy rule.', 'The original prescription must still be valid.', 'The professional determination and documentation matter.']
    },
    {
      question: 'A pharmacy employee says “FDA-registered ingredient manufacturer” means every finished preparation is FDA-approved. Which correction is correct?',
      choices: ['FDA registration automatically authorizes every finished compounded drug', 'The pharmacist may omit stability and concentration checks', 'Ingredient source requirements and FDA approval of a final drug product are different determinations', 'A national professional credential removes state compounding rules'],
      answer: 'C',
      explanations: ['Registration does not equal product approval.', 'Quality checks remain relevant.', 'Correct. Regulatory categories must be kept distinct.', 'Professional credentials do not override pharmacy practice law.']
    }
  ];

  function textNode(node) {
    return (node ? node.textContent : '').replace(/\s+/g, ' ').trim();
  }
  function parseAnswer(q) {
    const heading = q.querySelector('.answer p strong');
    const match = textNode(heading).match(/^Correct(?:\s+answer)?:\s*([A-D])\b/i);
    if (!match) throw new Error('A source question has no A–D answer.');
    return match[1].toUpperCase();
  }
  function makeDetails(prompt, choices, answer, explanations, sourceSlug, originIndex, citation, sourceUrl) {
    const details = document.createElement('details');
    const summary = document.createElement('summary');
    summary.textContent = prompt;
    const body = document.createElement('div');
    body.className = 'answer';
    const ol = document.createElement('ol');
    ol.className = 'answers';
    choices.forEach(choice => {
      const li = document.createElement('li');
      li.textContent = choice;
      ol.append(li);
    });
    const verdict = document.createElement('p');
    const strong = document.createElement('strong');
    strong.textContent = 'Correct answer: ' + answer + '.';
    verdict.append(strong);
    body.append(ol, verdict);
    explanations.forEach((why, i) => {
      const p = document.createElement('p');
      const label = document.createElement('strong');
      label.textContent = letters[i] + ':';
      p.append(label, ' ' + why);
      body.append(p);
    });
    const attribution = document.createElement('p');
    attribution.className = 'refline';
    const anchor = document.createElement('a');
    anchor.href = '../' + sourceSlug + '/#quiz';
    anchor.textContent = 'Read the original study guide and legal references';
    attribution.append(anchor);
    if (citation && sourceUrl) {
      const separator = document.createTextNode(' · Legal reference: ');
      const official = document.createElement('a');
      official.href = sourceUrl;
      official.target = '_blank';
      official.rel = 'noopener noreferrer';
      official.textContent = citation;
      attribution.append(separator, official);
    }
    body.append(attribution);
    details.append(summary, body);
    return details;
  }
  // The previous algorithm manufactured 260 extra "questions" by turning
  // answers to other options into choices. That is not a valid substitute for
  // independently written MPJE scenarios and sometimes produces fragments
  // such as "Correct." or "Not the policy." as purported answers.
  // Keep those unreviewed items out of scored practice rather than expose
  // misleading answer keys. Preserve the ten manually written exercises.
  function supplementalQuestions(slug) {
    const reviewed = window.MPJE_SUPPLEMENTAL_VERIFIED?.[slug];
    if (Array.isArray(reviewed) && reviewed.length) {
      return reviewed.map((q, i) => makeDetails(
        'Supplemental question ' + (i + 1) + '. ' + q.question,
        q.choices, q.answer, q.explanations, slug, i, q.citation, q.sourceUrl
      ));
    }
    if (slug !== 'nonsterile-compounding') return [];
    return manuallyAuthored.map((q, i) => makeDetails(
      'Supplemental question ' + (i + 1) + '. ' + q.question,
      q.choices, q.answer, q.explanations, slug, i
    ));
  }

  const difficultyChapters = new Set(['prescription-validity', 'cii-core', 'cii-partial-outstate', 'refills-transfer', 'pmp-oud', 'label-interchange', 'counseling-dur', 'rems', 'privacy', 'vaccination-administration', 'cdtm', 'prescribing-public-health']);
  function difficultyQuestions(slug, level) {
    const set = window.MPJE_DIFFICULTY_REVIEWED?.[slug]?.[level];
    if (!set) return [];
    if (!Array.isArray(set) || set.length !== 10) throw new Error('Expected 10 ' + level + ' questions for ' + slug);
    return set.map((q, i) => {
      if (!q.question || !Array.isArray(q.choices) || q.choices.length !== 4 ||
          !Array.isArray(q.explanations) || q.explanations.length !== 4 ||
          !letters.includes(q.answer) || !q.citation || !/^https:\/\//.test(q.sourceUrl || '')) {
        throw new Error('Invalid ' + level + ' question ' + (i + 1) + ' for ' + slug);
      }
      return makeDetails(level[0].toUpperCase() + level.slice(1) + ' question ' + (i + 1) + '. ' + q.question,
        q.choices, q.answer, q.explanations, slug, i, q.citation, q.sourceUrl);
    });
  }

  function sectionTitle(el, name, description) {
    el.replaceChildren();
    const title = document.createElement('h2');
    title.textContent = name;
    const p = document.createElement('p');
    p.textContent = description;
    el.append(title, p);
  }
  function updateNav(index) {
    const hasPrev = index > 0, hasNext = index < chapters.length - 1;
    prev.disabled = !hasPrev;
    next.disabled = !hasNext;
    prev.textContent = hasPrev ? 'Previous: ' + chapters[index - 1].title : 'First chapter';
    next.textContent = hasNext ? 'Next: ' + chapters[index + 1].title : 'Last chapter';
  }
  async function loadChapter(slug) {
    const index = chapters.findIndex(c => c.slug === slug);
    if (index < 0) return;
    const key = ++request;
    select.value = slug;
    updateNav(index);
    status.textContent = 'Loading source questions for Chapter ' + (index + 1) + '…';
    original.hidden = true;
    extra.hidden = true;
    moderate.hidden = true;
    hard.hidden = true;
    chapterTitle.textContent = 'Chapter ' + (index + 1) + ': ' + chapters[index].title;
    guide.href = '../' + slug + '/';
    try {
      const response = await fetch('../' + slug + '/index.html', { credentials: 'same-origin' });
      if (!response.ok) throw new Error('HTTP ' + response.status);
      const doc = new DOMParser().parseFromString(await response.text(), 'text/html');
      if (key !== request) return;
      const sourceQs = Array.from(doc.querySelectorAll('section.quiz > details'));
      if (sourceQs.length !== 10) throw new Error('Expected 10 original source questions; found ' + sourceQs.length);
      sourceQs.forEach(q => {
        if (q.querySelectorAll('.answer ol.answers > li').length !== 4) throw new Error('Source option count changed.');
        parseAnswer(q);
      });
      const additional = supplementalQuestions(slug);
      const moderateCases = difficultyQuestions(slug, 'moderate');
      const hardCases = difficultyQuestions(slug, 'hard');
      if (difficultyChapters.has(slug) && (moderateCases.length !== 10 || hardCases.length !== 10)) {
        throw new Error('Difficulty expansion is incomplete for ' + slug);
      }
      sectionTitle(original, '10 original chapter questions', 'These questions and answer keys are inherited from the existing study guide; this consolidation did not independently certify their legal accuracy.');
      sourceQs.forEach(q => original.append(document.importNode(q, true)));
      sectionTitle(extra, '10 supplemental ' + (slug === 'nonsterile-compounding' ? 'nonsterile-compounding' : 'reviewed') + ' cases',
        slug === 'nonsterile-compounding'
          ? 'Separately authored applications of the linked chapter. An independent end-to-end legal audit is still needed.'
          : 'Individually authored pharmacist-decision scenarios; each has a specific official-source citation and explanations for every answer choice. Reviewed November 10, 2026.');
      additional.forEach(q => extra.append(q));
      sectionTitle(moderate, '10 Moderate application questions',
        'Apply two connected rules or realistic exceptions. Source-reviewed November 11, 2026; independent legal audit remains pending.');
      moderateCases.forEach(q => moderate.append(q));
      sectionTitle(hard, '10 Hard multi-rule questions',
        'Work through interacting federal and Massachusetts rules, exceptions, and deadlines. Source-reviewed November 11, 2026; independent legal audit remains pending.');
      hardCases.forEach(q => hard.append(q));
      original.hidden = false;
      extra.hidden = additional.length === 0;
      moderate.hidden = moderateCases.length === 0;
      hard.hidden = hardCases.length === 0;
      window.MPJE_ENHANCE_QUIZZES?.();
      const count = sourceQs.length + additional.length + moderateCases.length + hardCases.length;
      status.textContent = count + ' questions available for Chapter ' + (index + 1) + ': 10 original'
        + (additional.length ? ' + ' + additional.length + ' supplemental' : '')
        + (moderateCases.length ? ' + ' + moderateCases.length + ' moderate' : '')
        + (hardCases.length ? ' + ' + hardCases.length + ' hard' : '')
        + '. Chapter ' + (index + 1) + ' of ' + chapters.length + '.'
        + (count === 20 ? ' Additional difficulty sets for this topic are not yet published.' : '');
      history.replaceState(null, '', '?chapter=' + encodeURIComponent(slug));
    } catch (err) {
      if (key !== request) return;
      status.textContent = 'Could not load Chapter ' + (index + 1) + ': ' + String(err.message || err) + '. Open the source guide instead.';
    }
  }
  select.addEventListener('change', () => loadChapter(select.value));
  prev.addEventListener('click', () => {
    const i = chapters.findIndex(c => c.slug === select.value);
    if (i > 0) loadChapter(chapters[i - 1].slug);
  });
  next.addEventListener('click', () => {
    const i = chapters.findIndex(c => c.slug === select.value);
    if (i >= 0 && i < chapters.length - 1) loadChapter(chapters[i + 1].slug);
  });
  document.getElementById('review-library')?.addEventListener('click', () => {
    window.location.href = '../';
  });
  const initial = new URLSearchParams(window.location.search).get('chapter');
  loadChapter(chapters.find(c => c.slug === initial)?.slug || chapters[0].slug);
})();