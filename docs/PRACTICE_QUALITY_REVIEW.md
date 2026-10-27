# Practice quality and Chaos10 — integration review

Updated 2026-10-27. This is the GitHub integration of the previously prepared quality package, not a new independent legal audit.

## Applied behavior

- Default pool: 451 items, comprising 355 selected legacy representatives and 96 individually authored additions (`MA-REV-0001` through `MA-REV-0096`).
- All 2,272 items remain available. Both old collections, stable IDs, answers, note evidence, bookmarks and existing progress storage are preserved.
- Standard 20-item and up-to-120-item sets prevent repeated families, normalized stems and complete option sets; they do not backfill clones when insufficient distinct items exist.
- Chaos10 samples ten times independently **with replacement from the entire 2,272-item pool**. Filters, blueprint quotas, family caps and previous attempts do not restrict it. The exact same question can appear more than once.
- Session answers are stored by occurrence slot, so repeated IDs cannot overwrite earlier answers. Each occurrence can be reviewed separately. The existing persistent per-question history still records the most recent attempt; in-progress session restoration was not added.
- Options shuffle using stable IDs. Displayed letters and choice-specific explanations map to the shown order. Topic labels are hidden before feedback.

## Repetition evidence

The original structural review covered 2,615 stored records: 2,176 online expansion items and 439 canonical records, not necessarily all released. Within the online expansion there were 1,428 normalized unique stems, 748 repeated occurrences beyond the first, and 331 items sharing a full option set with another item. The 451-item default pool has no exact normalized stem or complete-option-set duplicates. These are lexical checks, not proof that every legal decision is semantically independent.

The 96 additions consist of 84 SBA and 12 SATA items. They are source-linked author-written cases, not recalled exam content, official NABP items or independently audited questions. No further 1,000-item templated expansion was created.

## Execution evidence

[Hosted application and real-browser run](https://github.com/woojunxnam/oddments/actions/runs/40584747052) completed successfully:

- 110 focused Python/Node tests passed; source-linked notes, refresh and exam-study deterministic builds passed.
- 127 real-HTTP browser checks passed: quality/Chaos 38, existing practice 22, exam study 26, refresh 22, notes 19.
- All 2,272 question displays were checked at narrow mobile width, and each of the 96 new cases was answered through the UI with option-specific explanations.
- Real-origin storage/reload, original progress preservation, backup rejection/import, exact question deep links, repeated-ID scoring (ten occurrences, five correct), no-JavaScript notes and storage-denied behavior were tested.
- Downloaded browser evidence was inspected. No uncaught JavaScript errors were reported.

The first application attempt stopped on a stale base hash for `verify_exam_study_production.py` before writing changes. The exact repository version was compared; its existing navigation assertion was retained and only the count check was made publication-config-driven. All other package base/protected hashes matched. Protected notes, archives, canonical data, audits and release-policy files were checked byte-for-byte (1,665 files).

Permanent read-only quality QA and Pages content/manifest verification are included. The Pages job compares the live practice HTML and quality assets with the built version, including all three collection counts and the Chaos button. A successful application run is not by itself proof of production deployment; the Pages run for the merged commit is authoritative.

## Preserved history and limits

[Original detailed authoring report](PRACTICE_QUALITY_AUTHORING_REVIEW.md) retains the initial duplicate analysis, source-use scope, item-design rationale and the earlier inline-only test limitations. Its initial 'not published' status describes that earlier authoring session, not the current integration.

Physical iOS/Android/Safari, full independent legal adjudication, psychometric equivalence and guaranteed exam outcomes are unverified. Structural and browser tests do not certify legal answers. Canonical release policy and independent-review status are unchanged.
