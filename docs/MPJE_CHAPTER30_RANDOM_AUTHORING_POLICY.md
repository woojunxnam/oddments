# Chapter 30 MPJE practice: authoring and random-quiz policy

Owner preference recorded: November 13, 2026. Applies to new questions for
`site/mpje-side-notes/exam-simulation-30/` unless explicitly changed.

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
- Sample from **all** validated Chapter 30 questions, not just the most recent batch.
  The pool automatically grows as new area-tagged questions are appended.
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
