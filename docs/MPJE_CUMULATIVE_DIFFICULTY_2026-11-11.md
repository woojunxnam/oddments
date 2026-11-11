# Massachusetts MPJE — Chapter 28 Difficulty Expansion

**Status date:** 2026-11-11 (America/New_York)
**Scope:** Preserve the 540 original + supplemental questions. Add 10 Moderate and 10 Hard independently written application questions to each of 27 chapters (540 new items; goal 1,080).

**Published main-branch baseline:** 540 questions (270 original + 270 supplemental).
**Branch count after the changes in this PR:** 600 (baseline 540 plus 60 draft source-reviewed difficulty items).
**Remaining:** 480 new items, across 24 chapters.
**Legal review status:** Each newly authored question includes a citation to a primary federal or Massachusetts source and has been checked for one intended answer and four individual rationales. This is a preliminary source-based author review, **not** a completed independent auditor's approval. Source pages and law can change; verify their effective dates before release. Main question-bank canonical audit gates are not bypassed or represented as complete.

| Chapter | Topic | Moderate | Hard | Authored date | Independent legal audit |
|---|---|---:|---:|---|---|
| 01 | [Licensure, Reciprocity & CE](../site/mpje-side-notes/licensure-ce/index.html) | 0/10 | 0/10 | Pending | Pending |
| 02 | [Pharmacy Personnel, Interns, Technicians](../site/mpje-side-notes/personnel/index.html) | 0/10 | 0/10 | Pending | Pending |
| 03 | [Pharmacy Licensure & MOR](../site/mpje-side-notes/pharmacy-mor/index.html) | 0/10 | 0/10 | Pending | Pending |
| 04 | [Drug Schedules & Registration](../site/mpje-side-notes/schedules-registration/index.html) | 0/10 | 0/10 | Pending | Pending |
| 05 | [Prescription Validity, EPCS, Corrections](../site/mpje-side-notes/prescription-validity/index.html) | 10/10 | 10/10 | 2026-11-11 | Pending |
| 06 | [Schedule II Core](../site/mpje-side-notes/cii-core/index.html) | 10/10 | 10/10 | 2026-11-11 | Pending |
| 07 | [CII Partial Fills & Out-of-State](../site/mpje-side-notes/cii-partial-outstate/index.html) | 10/10 | 10/10 | 2026-11-11 | Pending |
| 08 | [Refills & Transfers](../site/mpje-side-notes/refills-transfer/index.html) | 0/10 | 0/10 | Pending | Pending |
| 09 | [MassPAT, Opioid / OUD](../site/mpje-side-notes/pmp-oud/index.html) | 0/10 | 0/10 | Pending | Pending |
| 10 | [Labels & Interchange](../site/mpje-side-notes/label-interchange/index.html) | 0/10 | 0/10 | Pending | Pending |
| 11 | [Counseling & DUR](../site/mpje-side-notes/counseling-dur/index.html) | 0/10 | 0/10 | Pending | Pending |
| 12 | [REMS](../site/mpje-side-notes/rems/index.html) | 0/10 | 0/10 | Pending | Pending |
| 13 | [Privacy](../site/mpje-side-notes/privacy/index.html) | 0/10 | 0/10 | Pending | Pending |
| 14 | [Vaccination & Administration](../site/mpje-side-notes/vaccination-administration/index.html) | 0/10 | 0/10 | Pending | Pending |
| 15 | [CDTM](../site/mpje-side-notes/cdtm/index.html) | 0/10 | 0/10 | Pending | Pending |
| 16 | [Pharmacist Prescribing & Public Health](../site/mpje-side-notes/prescribing-public-health/index.html) | 0/10 | 0/10 | Pending | Pending |
| 17 | [DEA Ordering & Inventory](../site/mpje-side-notes/ordering-inventory/index.html) | 0/10 | 0/10 | Pending | Pending |
| 18 | [Security, Loss, Disposal](../site/mpje-side-notes/security-loss-disposal/index.html) | 0/10 | 0/10 | Pending | Pending |
| 19 | [Storage & Shipping](../site/mpje-side-notes/storage-shipping/index.html) | 0/10 | 0/10 | Pending | Pending |
| 20 | [Shared Services & Automation](../site/mpje-side-notes/shared-automation/index.html) | 0/10 | 0/10 | Pending | Pending |
| 21 | [Nonsterile Compounding](../site/mpje-side-notes/nonsterile-compounding/index.html) | 0/10 | 0/10 | Pending | Pending |
| 22 | [Sterile Compounding](../site/mpje-side-notes/sterile-compounding/index.html) | 0/10 | 0/10 | Pending | Pending |
| 23 | [Hazardous Drugs, 503B, Nuclear](../site/mpje-side-notes/hd-outsourcing-nuclear/index.html) | 0/10 | 0/10 | Pending | Pending |
| 24 | [FDA & Drug Supply Chain](../site/mpje-side-notes/fda-supply-chain/index.html) | 0/10 | 0/10 | Pending | Pending |
| 25 | [Reporting Deadlines & Records](../site/mpje-side-notes/numbers-records/index.html) | 0/10 | 0/10 | Pending | Pending |
| 26 | [Drug Directory](../site/mpje-side-notes/drug-directory/index.html) | 0/10 | 0/10 | Pending | Pending |
| 27 | [Open Legal Register](../site/mpje-side-notes/open-register/index.html) | 0/10 | 0/10 | Pending | Pending |

## Design and quality rules

- Realistic pharmacy decisions; not direct rewrites, answer inversion, or fragments from source questions.
- All new items require four distinct options, a single best answer, four option-specific explanations, and a specific official source URL; cite controlling section.
- Moderate: preferably two legal determinations or an exception. Hard: interacting federal and Massachusetts requirements, multiple clocks, competing responsibilities, or nuanced exceptions.
- Before a release claim: verify question and answer against controlling law, any active Board policy, effective dates; check A–D distribution, duplication, difficulty, and usability. Original guide content and canonical question bank remain untouched.
- The public Chapter 28 page must never advertise the 1,080 final target as already available while any of 480 remaining items are unfinished.

## This branch's new question assets

- `site/mpje-side-notes/difficulty-reviewed-05.js`: Prescription Validity / EPCS (20).
- `site/mpje-side-notes/difficulty-reviewed-06.js`: Schedule II Core (20).
- `site/mpje-side-notes/difficulty-reviewed-07.js`: CII Partial Fills / Out-of-State (20).
- `site/mpje-side-notes/practice-review.js`: Difficulty-tier loading and score sections.
- `site/mpje-side-notes/cumulative-practice/index.html`: UI for separate tiers and accurate count.
- `site/mpje-side-notes/quiz.js`: Chapter labels and 27-chapter selector fix.
- `site/mpje-side-notes/index.html`: Chapter 28 library count and summary.

**Effective-date check:** Source-based author review November 11, 2026. For March 1, 2027 and later MPJE dates, recheck NABP content outline and all current MA/DEA requirements.
