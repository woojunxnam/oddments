# Chapter 30 MPJE practice: authoring and random-quiz policy

Owner preference recorded: November 13, 2026. Applies to new questions for
`site/mpje-side-notes/exam-simulation-30/` unless explicitly changed.

## Required priority-coverage reference

Before selecting topics for the next five-question set, read
[the seven-gap coverage and quality plan](MPJE_CH30_PRIORITY_COVERAGE_PLAN_2026-11-16.md)
alongside the latest `topic-inventory.json` and the NABP public-source realism
audit. The coverage plan is a dated editorial snapshot, not a replacement for
checking live laws, official exam scopes, or the newest question IDs.

For the **next eight planned Sets 36–43** (not yet authored), also follow
[the 40-question source-first micro-skill roadmap](MPJE_CH30_SETS36-43_40Q_ROADMAP_2026-11-17.md).
It reserves candidate decisions E30-176–215 only while the current main count
remains 175; verify the actual latest main before assigning IDs. Each candidate
must still pass current-law, non-duplication and independent-answer review,
and may be replaced when its legal premise cannot be verified. After all 40
are actually published and browser-verified, perform the roadmap's formal
coverage, legal-error and exam-realism re-evaluation **before further expansion**.

## Authoring each requested five-question batch

- Exactly **one Area 1 (Licensure/Personnel)** question.
- Exactly **two Area 2 (Pharmacist Practice)** questions.
- Exactly **one Area 3 (Dispensing Requirements)** question.
- Exactly **one Area 4 (Pharmacy Operations)** question.
- Maintain three difficult single-best-answer (SBA) and two select-all-that-apply (SATA)
  cases per five-question batch unless the owner requests a different mix.
- Write original, case-based Massachusetts MPJE-style questions. Do **not**
  reproduce secure NABP examination items or imply these are actual exam questions.
- Verify legal requirements, exceptions, dates and corresponding federal/MA
  authorities using primary sources. Document a governing citation and official
  link for each question, with an independent explanation for choices A through D.
- Before drafting, read **`site/mpje-side-notes/exam-simulation-30/topic-inventory.json`**
  (fast, small Area/topic summary), not every historical question. Select
  varied **topic families within each Area**: favor frequently emphasized,
  high-yield topics, but first cover underrepresented families in that Area.
  Individual stems, tested exceptions and fact patterns must be original.
  The per-topic real-exam frequency is NOT public; do not invent topic weights.
- Add question objects to `questions.js` with new stable `E30-###` IDs, a new
  numbered fixed `set`, **`area: 1|2|3|4`**, and a stable **`topicKey`**
  from `topic-catalog.json`. Add a new catalog family only when materially distinct.
  Preserve prior IDs, stems, keys and rationales; check new-question duplication
  and adjacent topics before accepting the set.
- Regenerate Area/topic counts with
  `python scripts/update_ch30_topic_inventory.py --write`; verify with
  `python scripts/update_ch30_topic_inventory.py --check`. Commit the
  updated `topic-inventory.json` with the question batch. This is a fast
  deterministic inventory update, not a substitute for a source-based legal audit.
- Link and retain all previous fixed sets, publish to GitHub Pages, and verify
  public content plus answer-hiding/scoring behavior.

## Random ten-question practice

- Draw **2 Area 1 + 3 Area 2 + 3 Area 3 + 2 Area 4**.
- Offer two selection modes over **all** validated Chapter 30 questions, not just the most recent batch:
  **Unanswered first** (default for new sessions) randomly selects as many
  never-checked questions as available within each Area before filling that
  Area's remaining quota with previously checked questions. **All questions**
  uses uniform random sampling within each Area, independent of attempt
  history. With fixed 2/3/3/2 Area quotas, questions in different Areas do not have
  an identical selection probability across different Areas.
  If a single unseen-only mix is possible, allowing one previously checked
  question is acceptable to avoid exactly repeating the previous mix. The
  bank automatically grows as new area-tagged questions are appended.
- "Unanswered" means zero submitted *Check Answer* attempts across fixed,
  random and review modes in this browser, not merely a question being viewed.
  Count tracked question-level attempts without resetting wrong counts,
  bookmarks or other study history. Changing the mode must not discard
  current answers until New Random 10 is deliberately clicked.
- Do not display a cumulative Random set number; it has no scoring or study
  meaning. Preserve legacy localStorage question sessions and interpret
  older sessions without a mode as uniform (all).
- **No repeated question within a set.** Every New Random 10 action must result
  in a different question combination from the immediately preceding mix while
  another composition is mathematically possible. Different sets may share some
  individual questions.
- **Every question is checked individually** in fixed five-question sets,
  Random 10 and both review collections. Only the checked question reveals its
  key and A–D rationales. SATA scores only for the exact complete selection.
- Incorrect answers enter the wrong-answer review queue. A correct reattempt
  clears the active wrong-answer flag but preserves the total wrong count.
  Users can bookmark any item manually; two or more incorrect attempts
  automatically bookmark it. Bookmarks remain until explicitly removed.
  The collections can be used to retake individual questions.
- Progress is persisted in same-browser `localStorage`, not to a cloud
  account. Prior all-at-once submissions are migrated once where recoverable.
  Random and fixed question-session state remain independent.
- If an area lacks the required number of tagged questions, show an explanatory
  error rather than silently substituting another area or duplicating questions.

## Area taxonomy and effective date

For this legacy-area study design, follow NABP's *MPJE Competency Statements*
for examinations before **March 1, 2027**:

1. Licensure / Personnel
2. Pharmacist Practice
3. Dispensing Requirements
4. Pharmacy Operations

Official source:
https://nabp.pharmacy/programs/examinations/mpje/competency-statements/

For exams administered **March 1, 2027 or later**, NABP uses a different
four-domain Content Outline. The above owner-requested legacy-area sampling
scheme is a custom learning tool; it is not the official 2027 blueprint, nor
the exact current-exam percentage distribution. Do not silently reinterpret
numeric area tags as the 2027 domains. Discuss a migration plan when requested.

Official transition notice:
https://nabp.pharmacy/news/blog/mpje-content-outline/

## Implementation details

- Canonical practice objects: `site/mpje-side-notes/exam-simulation-30/questions.js`
- Fixed sets: `study.js` (retain existing behavior)
- Random set: `random-quiz.js`, independent local-storage namespace
- Shared individual-check renderer: `question-ui.js`
- Personal history/bookmarks: `progress.js` (per-question browser storage)
- Wrong / saved review lists: `review.js`
- Topic taxonomy: `topic-catalog.json` and question `topicKey`
- Generated count ledger: `topic-inventory.json`; generator in `scripts/update_ch30_topic_inventory.py`
- Chapter 30 page and styles: `index.html`, `exam.css`
- Chapter library: `site/mpje-side-notes/index.html`

The area tag is the item's **editorially assigned primary tested area**;
some pharmacy-law fact patterns may span multiple NABP areas. Check the
specific question's main reasoning task and avoid inferring area solely from
its drug or statute name.

## Topic-mix editorial rule

Keep the owner's fixed 1/2/1/1 Area quota for each new five-question batch. Within those slots, compare the concise inventory and choose **different tested topic families and legal mechanisms**, using high-priority topics more often over time but not repeating the same rule under cosmetic name changes. Review source law and the nearest overlapping existing question(s) when a candidate topic is already represented. The catalog's high/medium priorities are qualitative editorial labels inferred from the syllabus and public study reports—not measured Massachusetts exam-item frequencies.

The inventory is a count/coverage aid; source verification, distractor uniqueness, historical-date checking and review of substantive overlap remain compulsory for every new item.

## NABP style calibration for future sets (reviewed November 16, 2026)

Read [Chapter 30's public-source realism audit](MPJE_CH30_REALISM_AUDIT_2026-11-16.md)
before new authoring work or mock-exam UX changes. The audit is a historical
snapshot; topic inventory and latest primary law override its old totals.

- Use only NABP's **public** sample items, current Candidate Bulletin/tutorial,
  current MA Board review list, enacted laws/policies and non-confidential,
  firsthand reports **about exam difficulty and broad topic categories**.
  Do NOT request, collect, reproduce, or reverse-engineer recalled secured
  MPJE/Pre-MPJE items, exact stems, keyed choices or private practice-exam content;
  NABP expressly prohibits AI interaction with the confidential Pre-MPJE.
- Do not optimize every item for length. Vary short direct lawful/unlawful
  judgment, medium case application, and complex multi-rule scenarios.
  Each stem must be no longer than necessary to distinguish one defensible
  answer and identify its governing jurisdiction and effective date.
  Contrasts such as MAY versus MUST, dispense versus administer, initial
  versus refill, pharmacist versus intern, and MA versus federal must emerge
  from the legal scenario, not arbitrary wording tricks.
- No invented 'real exam' SATA percentage, exact topic frequency, or question
  length distribution. One public 2025 candidate described mostly multiple
  choice; another reported many SATA. Both are anecdotal. Maintain the
  existing owner-specified per-five set 3 SBA/2 SATA and 1/2/1/1 Areas
  unless the owner changes it. A separate realistic mock should avoid
  predictable five-item templates and report only internal practice results,
  not an NABP passing probability or scaled score.
- Current Chapter 30 rendering and validation assume exactly FOUR choices
  and every SATA has multiple correct choices. The free public NABP examples
  show FIVE choices and explain that multiple-response may have ONE OR MORE
  correct answers. These are **known compatibility gaps**, not authorization
  to silently add a fifth choice or a one-key SATA to the live bank.
  Before introducing these richer formats, extend question-ui.js, fixed/random
  validation, score calculation, inventory checks and Playwright tests
  in a dedicated backwards-compatible PR. Do not rewrite old questions.
- Prioritize currently under-tested Board-review topics before producing more
  lookalike scenarios: prescriber authority and valid prescription elements,
  Massachusetts versus federal drug scheduling, delivery/shipping/storage,
  advanced USP <795>/<797>/<800>, 105 CMR 700–722, recalls, adulteration/
  misbranding, Medication Guides, PDMA, and institutional pharmacy duties.
  Compare nearest existing stems and original notes; verify applicable rules
  from primary legal sources and explicit effective dates.
- For every newly authored choice, re-solve the case without seeing the
  intended key. Reject an item with another defensible answer, unsupported
  deadlines/exemptions, length cues, 'always/never' throwaway distractors
  unrelated to the tested authority, or obvious A–D answer-position patterns.
  Keep detailed legal explanations visible only AFTER practice submission.
- Future **free timed simulation** proposal (not yet implemented): 40 original
  questions / 50 minutes (Pre-MPJE-style pacing), followed if useful by
  120 / 150 minutes (MPJE pacing). Show one item at a time; no back navigation
  after submission; hide all solutions until session completion; then provide
  source-linked review. Use a fresh unseen pool and preserve the current
  independent learning/review modes. Do not claim to reproduce NABP's
  confidential item pool, CAT algorithm, psychometric scoring, or Pre-MPJE.

## Seven-gap selection and legal-quality gates (from November 16, 2026)

Apply the seven subject families defined in
[the coverage plan](MPJE_CH30_PRIORITY_COVERAGE_PLAN_2026-11-16.md):
(1) prescription validity/prescriber scope; (2) drug schedule identification;
(3) practical USP <795>/<797>/<800>; (4) shipping/delivery/storage;
(5) Board discipline/inspections/impairment; (6) drug integrity and required
patient-facing information; (7) institutional/specialty/nonresident practice.

- **Default topic selection:** Target at least three of the next five items
  at the highest-priority unresolved subskills, consistent with the existing
  one Area 1/two Area 2/one Area 3/one Area 4 quota. Prefer an untested legal
  mechanism to a fourth variation of the same exception. If an Area has no
  verified candidate in that gap, do not invent a rule to satisfy a quota.
  Document the reason in editorial review.
- **No numerical quota claimed for the real MPJE.** The seven categories,
  their ordering, and proposed five-set roadmap are a study editorial decision,
  not NABP frequency or candidate-item statistics.
- **Label each new item:** primary Area, topicKey, specific legal decision,
  distinct exception/deadline/scope issue, official authority and effective
  date, neighboring existing question IDs, plus why the correct choice is
  uniquely defensible. Record outside the question object if the current
  site schema does not support a field. Do not leak answers in public stems.
- **Source-first decision:** identify controlling Massachusetts statute/
  247 CMR/105 CMR/Board policy and relevant federal authority; check which is
  enforceable, more restrictive, or preemptive as appropriate. Confirm date
  and status (enacted vs proposed vs guidance), setting (community vs LTCF/
  hospital vs nonresident), actors, drug, schedule, patient and exception.
  If a source is paywalled, missing, conflicting, or outdated, replace
  the problem or flag unresolved; do not guess citations.
- **Choice-level adversarial check:** independently solve the literal case
  afresh, then verify EACH option against exact operative text. Single-best-
  answer must have exactly one defensible key; SATA must have its complete
  defensible set, with no alternate interpretation. Keep plausible nearby
  distractors and remove accidental cues from option length, repeated
  "always"/"never", grammar, or key-position patterns.
- **Teaching test:** explain A–D individually in clear English and include
  a practical what-the-pharmacist-does-next interpretation. Each wrong answer
  must say precisely which law, assumption, or exception makes it wrong.
- **Coverage test:** compare closest existing problem(s) before publication,
  including the actual legal mechanism, not merely matching topic titles.
  Preserve all old items, IDs, quiz records, bookmarked questions and
  localStorage behavior. Validate fixed 5 and Random 10 regressions.
- **Format fidelity:** maintain the owner's current 3 SBA/2 SATA and four
  choices until a *separate tested schema/UI change* is approved. Vary
  realistic stem length and cognitive task without pretending to match exact
  confidential NABP item ratios. No secure exam recollections or keys.

Review new-law or new-policy issues again on each batch date; when the
test date is March 1, 2027 or later, explicitly reassess the blueprint
rather than quietly reclassifying legacy numeric Area codes.
