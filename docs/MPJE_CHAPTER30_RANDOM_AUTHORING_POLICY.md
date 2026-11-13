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
- Add question objects to `questions.js` with new stable `E30-###` IDs, a new
  numbered fixed `set`, and **`area: 1|2|3|4`**. Existing questions/IDs/keys
  are preserved; check duplication before writing or publishing.
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
- Answers and individual rationales remain hidden until all ten are submitted.
  SATA scoring requires the exact complete set. Do not affect saved fixed-set work.
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
- Chapter 30 page and styles: `index.html`, `exam.css`
- Chapter library: `site/mpje-side-notes/index.html`

The area tag is the item's **editorially assigned primary tested area**;
some pharmacy-law fact patterns may span multiple NABP areas. Check the
specific question's main reasoning task and avoid inferring area solely from
its drug or statute name.
