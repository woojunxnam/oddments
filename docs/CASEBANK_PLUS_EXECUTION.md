# Additional casebank: executed software verification — 2026-10-26

Successful hosted import and HTTP browser execution:
https://github.com/woojunxnam/oddments/actions/runs/40367815284

## Completed

- 70 focused tests passed locally and in GitHub Actions. Tests cover the new bank, source hashes, conditions, answer keys, all choice rationales, original archive, publication separation, notes, and HTML collection option validity.
- Deterministic authoring and publication build passed; original canonical data, audits, notes, old practice archive and canonical release policy were byte-preserved.
- 22 public-practice HTTP checks passed, including all 2,176 renders at desktop and 320px; main entry; original/new/mixed filters; SBA and five-choice SATA with E; old/new progress coexistence after real-origin reload; JSON import/export and invalid choice rejection; family-capped 20/120 sets; timed feedback; new-only/deep links; mobile research page; blocked storage; navigation; no uncaught JS errors.
- The existing integrated-notes HTTP regression also passed all 19 checks, including all 306 sections and static no-JavaScript book. No notes content was changed.
- Hosted evidence artifact contains both reports and screenshots. Physical iOS/Android devices and Safari were not tested.

## Failure and correction retained

The first import run (40367243653) failed the new-only collection assertion because of a malformed option tag. The underlying HTML was repaired and a parser regression added; the original failing HTTP assertion was retained. The second run above passed. No question keys or legal conclusions were altered to make the software check pass.

## What these results do not establish

Software tests are not independent legal or item-realism audits, official scoring calibration, complete semantic novelty, or proof of equivalence to recent confidential exams. The new 1,152 exercises are 128 models with nine condition variants each. Author review, source provenance and selected fresh official-source reads remain distinct from independent review.

The temporary snapshot/import workflows are removed before integration. Permanent read-only online-practice QA repeats the build and browser checks. Production publication is verified separately by the Pages workflow after merge, not inferred from this feature-branch success. Repository-wide QA is separate from the focused results listed here.
