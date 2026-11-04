# Refresh learning layer — execution evidence (2026-10-27)

Base main: `4b389b14dd0fee47f4112eb8b7cb5f07d1b0ea66`. Additive implementation branch: `feat/notes-refresh-20261027`.

## Completed hosted checks

[Import and real-browser run 40523508168](https://github.com/woojunxnam/oddments/actions/runs/40523508168) executed:

- **84 focused Python tests**, including the Node scheduling/import contract, passed.
- Both source-derived builders' exact-output checks passed. Original notes source, both expansion archives, canonical data, audits, generated canonical questions and release rules were unchanged.
- **22 refresh HTTP checks** passed with real-origin storage/reload: daily queue, random uniqueness, ratings, backups, source warnings, glossary, seven steps, all 232 mobile card renders, and top/home/cards on all five pages.
- **19 existing notes HTTP checks** passed, including all 306 sections, original progress storage, mobile navigation, no-JavaScript full book and load-failure recovery.
- **22 existing practice HTTP checks** passed, including all 2,176 questions, both collections, scoring, saved state and timed practice.
- No uncaught JavaScript errors were reported by these suites. Artifact `refresh-http-evidence` (12742587220) contains actual reports and screenshots.

## Local evidence and limitations

The constrained local runtime's 19 inline DOM checks used explicitly simulated storage, not HTTP/reload evidence. That limitation was resolved for navigation/storage coverage by the hosted real-HTTP run above. A separate full local `pytest` run reached its runtime timeout before a final result; it is **not** counted as a complete pass. Full repository CI remains separate and its current workflow status is authoritative.

Some interaction screenshots captured while CSS smooth scrolling was in flight had sticky-header offsets. A separate fresh-context layout capture uses reduced motion and settled positions for visual review; it does not replace or relax the default-motion interaction tests.

The permanent read-only refresh QA reruns the new and existing browser suites. The Pages workflow checks the actual published refresh assets byte-for-byte and confirms shared navigation on all pages after deployment. A successful import run alone is not a production-deployment claim.

Software tests do not independently verify every legal/clinical statement. Physical iPhone/Android/Safari, formal accessibility certification, clinical competence and exam pass calibration are not claimed. See [content review](REFRESH_CARDS_REVIEW.md).
