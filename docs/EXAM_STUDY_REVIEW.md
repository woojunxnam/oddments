# MPJE exam-first learning layer — 2026-10-27

## User priority and scope

The immediate objective is passing the Massachusetts MPJE, not completing a return-to-pharmacy clinical curriculum. The primary entry, sidebar, notes-home calls to action and shared navigation now lead to `notes/#study`. The existing RA-to-practice pathway remains available under a secondary, collapsible section; it is not a prerequisite for exam study.

The new layer supplies 16 law-learning modules, 64 concise concepts, 12 contrast groups, 24 time/trigger reminders, 30 manual study sessions and links covering the 22 pre-March-2027 competency codes. All 33 existing detailed chapters remain connected. Four concepts per module are entry points, not replacements for the detailed source chapters. No claim that these summaries cover every tested exception is made.

## Source and legal boundaries

`notes/guide.json` remains the substantive source. Each concept, contrast and clock identifies the exact source units and inherits their hashes, source IDs, original review dates and OPEN/date-sensitive/source-gap flags. The full source text and exceptions are expandable inside lessons and link back to the detailed reader. Source gaps are not filled from model memory or another state's rule. This edition does not silently resolve regulation/policy differences or independently re-audit every legal statement.

The official NABP competency and preparation pages were checked on 2026-10-27:
- https://nabp.pharmacy/programs/examinations/mpje/competency-statements/
- https://nabp.pharmacy/programs/examinations/mpje/prepare-for-the-exam/

The current 22/33/24/21 area percentages and 22 competency codes apply before 2027-03-01. An exam date on or after that cutoff displays a warning rather than silently treating the old blueprint as current. The 16-module organization, recall prompts, comparisons, 30-session sequence and 1/3-day self-rating intervals are editorial learning design, not official recent-item frequency, a validated spaced-repetition algorithm, or a pass predictor. No private or recalled exam content was used.

## Practice connection

166 distinct existing question IDs are linked across concepts. Each connection shares an exact `note_evidence.unit_id`; within a concept, the maximum three linked questions come from distinct families. Items explicitly carrying OPEN/source-gap evidence are not selected. This is a navigation filter, not a new independent audit or a release-status promotion. The existing public practice explanation explicitly retains its independent-review and difficulty-calibration limitations. All 2,176 question texts, answer keys, IDs and archived source bytes remain unchanged.

## User experience

- `#study`: exam-first learning dashboard, unit search, competency-area filter, optional exam date and resume.
- `#study/module/m01` … `m16`: four concepts plus all linked full chapters.
- `#study/lesson/LAW-001` … `LAW-064`: core rule, why the distinction matters, boundary, optional conceal/reveal, unchanged full sources, practice connections and personal error notes.
- `#study/today`: stable ten-concept set for each America/New_York calendar day. Uses only exam-law concepts, preferring due review and unseen material while diversifying modules. Skips do not count as completion.
- `#study/drill`: shuffled non-repeating cycle through the 64 law concepts.
- `#study/compare`, `#study/clocks`: contrast review and numbers with trigger/qualifications, not isolated unsupported answers.
- `#study/plan`: 30 manually marked sessions; missing a day does not automatically skip material.
- `#study/weak`: self-identified review-needed concepts and personal reasons; it does not infer weakness from bank scores.
- `#study/coverage`: all 22 competency connections and the date boundary.
- `notes/study.html`: static, no-JavaScript reading/printing edition.

## Persistence and existing functionality

The namespace is `oddments.mpje.exam-study.v1`; old notes, refresh and practice namespaces are not modified by the study module. Backups use a separate application marker, validate their structure and merge newer concept records plus completed sessions without deleting existing entries. Storage-denied sessions remain usable and display an export reminder. No account, telemetry, notifications or cross-device sync is added.

The common dock adds MPJE study while preserving top/home/cards; back-to-top does not replace the active hash. The old detailed reader, 232 refresh cards, 45-term glossary, seven return-to-practice steps and 2,176-question practice remain accessible.

## Verification status

The local focused suite completed with 98 passes (14 new study tests plus 84 existing relevant tests). Exact builds and JavaScript syntax checks passed. A local inline Chromium preview completed 21 checks with **explicitly simulated storage**; this alone is not proof of HTTP navigation, actual-origin persistence or a production deployment. Screenshots were visually inspected at desktop and 390px widths, and all 64 concepts were checked at 320px.

One initial inline test found relative-history routing incompatible with an inline base URL. The history replacement now preserves the document's own URL; the full random-cycle test was rerun rather than bypassed. The new static edition initially lacked the common navigation marker; the builder was corrected and the existing six-page structural contract was rerun successfully.

Hosted HTTP and production execution results are recorded in the pull request and workflow logs, not inferred from local preview. The permanent workflow runs the new browser suite plus the three existing browser suites, and separately checks actual deployed files byte-for-byte after a successful Pages deployment.

Physical iPhone/Android/Safari, formal accessibility certification, independent legal review, psychometric calibration and an MPJE pass guarantee are not claimed.
