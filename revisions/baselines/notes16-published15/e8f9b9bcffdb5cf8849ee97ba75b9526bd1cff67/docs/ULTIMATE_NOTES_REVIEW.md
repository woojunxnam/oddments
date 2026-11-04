# Ultimate Notes integration review — 2026-10-23

## Scope

Adds an independent Korean/English Massachusetts MPJE notes reader under `site/notes/`, linked from the existing main page. The existing question bank, old Study Guide, canonical rule registries, audit records, release statuses and quiz application scripts are unchanged. This review covers the implemented notes edition, not independent adjudication of all pharmacy law.

## Editorial accounting

- 22 Week 1–6 input documents; 391 numbered source sections accounted for in `notes/editorial-map.json`.
- 33 topic chapters, 306 reading sections, 127 drug/form entries and 248 linked public references.
- 56 input sections integrated into other topic units; 46 repeated summaries, publication notes and weekly schedules consolidated into common guidance.
- Important distinctions, conditions and exceptions are retained rather than collapsing competing authorities into a convenient single number.
- Source-derived editing, editorial synthesis and narrowly rechecked official-source additions have separate unit metadata.
- Private Drive links and local input paths are not part of the public reader.

Specific improvements include the combined Schedule VI continuity comparison, current CE email correction, corrected MOR absence citation to 247 CMR 9.23(5), the added M.G.L. c.94C §21C lesser-price topic, merged inventory/returns/counseling/REMS explanations, and restored drug-appendix reference connections. MedlinePlus name indexes and DailyMed lookup links are not represented as product-label verification.

## Tests actually executed

- Full local pytest suite: 156 passed, including 8 new notes tests.
- Existing registry validator: 0 errors, 7 inherited warnings; no question-bank data was changed to suppress them.
- Four deterministic notes artifacts match the canonical notes input; JavaScript syntax and diff whitespace checks passed.
- GitHub-hosted HTTP browser regression passed on the implementation import run: https://github.com/woojunxnam/oddments/actions/runs/39996817600
- Real HTTP checks cover main-to-notes and return navigation, all chapters/sections, Korean/English/legal-number search, query escaping, OPEN filtering, drug directory, source registry, bookmarks/read state, reload persistence, JSON export/import and invalid-import rejection, quiz-storage isolation, typography/theme/focus preferences, keyboard skip link, responsive layouts at 320/390/768/1440 pixels, mobile dialog/Escape, no-JavaScript book, unavailable-storage handling and missing-content recovery.
- The first HTTP run exposed overflow in the no-JavaScript book. The static book's long compound terms now wrap; the same regression was rerun successfully, not removed.
- A double-escaping issue with USP <795>/<797> was fixed and covered by renderer/browser tests.

The permanent `Ultimate notes reader QA` workflow repeats source/build and HTTP browser checks for relevant changes. Existing QA and Pages workflows remain in place. Temporary import/research workflows were removed before integration.

## Limits

Physical iOS/Android devices, assistive-technology user testing, every printer/page-break combination and independent legal completeness were not verified. Core law-source review dates remain 2026-10-20–22; only selected items were rechecked on 2026-10-23. HIV/STI statewide clinical DOCX details, some authority overlaps/institutional boundaries and all subscription USP specialty exceptions remain explicitly incomplete. Neither software tests nor reading progress imply Board approval, legal certainty or a guaranteed MPJE pass.

Publication to the production Pages URL is a separate deployment step; the successful import run alone is not evidence of a production deployment.
