# Massachusetts MPJE Chapter 30 — Post-40 Quality Checkpoint

**Date:** 2026-11-17 ET. **Reviewed commit:** `400218a73acb5e2eb62981b616ec9ec9a81c350a`. **Scope:** all 215 original Chapter 30 question objects (43 sets), **author source-linked review + structural and similarity scan**. This is **not independent full legal re-adjudication of 860 choices**, an official NABP item validation, a psychometric pass-prediction, or a record of the user's first-attempt scores.

## Decision

**PAUSE indiscriminate question expansion.** Before adding more items, improve duplicate legal decisions, revisit high-change laws and test unseen first-attempt performance. The 40 new questions have been appended but at least one new case is substantially redundant with an earlier case.

## Structural results (verified from canonical JSON)

- **215** unique IDs, **43** five-question sets; **129 SBA / 86 SATA**; 65 SATA have two correct choices and 21 have three. All 43 sets contain 3 SBA + 2 SATA.
- Legacy Areas 1/2/3/4: **42 / 84 / 43 / 46**. **Sets 6–43** have the current 1/2/1/1 area mix. **Historical Sets 1–5 DO NOT**: see exact counts below. They predate the fixed-area rule; preserve historical answer and user progress rather than silently rewriting them.

| Early set | Area 1 | Area 2 | Area 3 | Area 4 |
| --- | ---: | ---: | ---: | ---: |
| 1 | 2 | 1 | 1 | 1 |
| 2 | 0 | 2 | 3 | 0 |
| 3 | 1 | 1 | 1 | 2 |
| 4 | 1 | 1 | 0 | 3 |
| 5 | 0 | 3 | 0 | 2 |

- All question URLs use HTTPS; **160/160** latest E30-176–215 option explanation prefixes match correct-answer keys. All 215 contain author-attached legal citations/dates. Source metadata **is not proof** of current operative law for every case.
- The 215 entries map to **58** topic families, but **unique authored topic strings do not necessarily equal independently distinct tested legal decisions**.

## 215-item micro-skill and seven-gap coverage ledger

This [JSON ledger](MPJE_CH30_215_MICROSKILL_LEDGER_2026-11-17.json) contains an explicit row for EACH of 215 IDs, case-specific skill, identifying facts, editorial gap, legacy Area, cited official URL, author review date, and overlap/risk flag. Independent option-by-option legal re-adjudication for all 215 is explicitly marked PENDING. Categories below assign one primary editorial focus per case and do not represent real exam topic percentages.

| Priority editorial family | Questions | Families |
| --- | ---: | ---: |
| Prescription and prescriber validity | 35 | 8 |
| Drug schedules, OTC and PMP | 22 | 3 |
| USP and 503A/503B compounding | 22 | 5 |
| Medication delivery and storage | 5 | 3 |
| Board discipline and personnel | 39 | 8 |
| Drug safety and product integrity | 32 | 11 |
| Institutional and special operations | 18 | 4 |
| Cross-cutting public health, privacy and interchange | 42 | 16 |

**Thin one-item families (15):** `controlled-pickup-id`, `hipaa-amendment`, `pharmacy-recordkeeping`, `hipaa-communications`, `patient-package-inserts`, `schedule-ii-fax-exceptions`, `patient-choice-dispensing`, `generic-interchange-emergency`, `hipaa-family-disclosures`, `pharmacist-compounding-duty`, `compliance-packaging`, `professional-ethics-referrals`, `bulk-compounding-eligibility`, `interchange-product-equivalence`, `board-waivers`. An item count of one is a depth signal, not proof that a concept appears more often on the MPJE. Qualitative gaps to verify next: wholesale/PDMA sample control; facility inspection and pharmacist impairment workflows; bedside/courier failed delivery and temperature excursions; hospital floor-stock controls; accurate label exceptions.

## Concrete redundant / high-overlap item findings

**High-confidence substantive duplication: E30-028 vs E30-203.** Both test 2026 **42 CFR Part 2** ordinary TPO consent, separate SUD counseling-notes consent, and protections against use in legal proceedings. E30-203 includes a newer OCR complaint option, but mostly repeats the previously tested decision. Do not count these as 2 independently new mechanisms. Its present answer is not proven legally wrong by this overlap finding.

A verifiably different legal decision is the patient's right under current [42 CFR 2.22(b)(1)(iv)(B),(G)](https://www.ecfr.gov/current/title-42/chapter-I/subchapter-A/part-2/section-2.22) to obtain a health-plan disclosure restriction for a **fully self-paid** service and **opt out** of Part 2 fundraising. The [HHS model Part 2 notice](https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/privacy-practices-part-2/index.html) supports this alternative. Recommend replacing/reworking E30-203 in a **separate version-aware correction PR**; changing an answered question under an unchanged ID can corrupt the meaning of stored browser localStorage history. Do not modify existing answers without a migration plan.

Other nuanced overlaps: E30-062 vs 191 (technician vaccination 500-postlicense-hours tested again, although 191 adds intern and pharmacist-selection duties), E30-041 vs 111 (trainee hours but different under-18 exception), E30-049 vs 179 (different Schedule II partial-fill clocks), and E30-075 vs 202 (same 2026 DSCSA exemption but eligibility vs remaining suspect-product obligations). These are not automatically incorrect; independently assess the distinct tested legal triggers.

| High normalized stem similarity candidate | Cosine-style score | Status |
| --- | ---: | --- |
| E30-028 / E30-203 | 0.587 | **Substantive duplicate flagged** |
| E30-041 / E30-111 | 0.478 | Human legal-delta review needed |
| E30-026 / E30-091 | 0.465 | Human legal-delta review needed |
| E30-003 / E30-137 | 0.433 | Human legal-delta review needed |
| E30-062 / E30-191 | 0.431 | Human legal-delta review needed |
| E30-033 / E30-073 | 0.429 | Human legal-delta review needed |
| E30-015 / E30-080 | 0.409 | Human legal-delta review needed |
| E30-043 / E30-082 | 0.402 | Human legal-delta review needed |

## 32-versus-32 realism comparison (not psychometric)

Sample selection: latest 32 **E30-184–215**; historical comparator 32 questions chosen from the original 175 by `index=floor((i+0.5)*175/32)`, i=0–31. Exact old sample IDs: E30-003, E30-009, E30-014, E30-020, E30-025, E30-031, E30-036, E30-042, E30-047, E30-052, E30-058, E30-063, E30-069, E30-074, E30-080, E30-085, E30-091, E30-096, E30-102, E30-107, E30-113, E30-118, E30-124, E30-129, E30-134, E30-140, E30-145, E30-151, E30-156, E30-162, E30-167, E30-173.

| Measured characteristic | New 32 | Older 32 |
| --- | ---: | ---: |
| Median stem characters | 532 | 452.5 |
| Short stems (<300 chars) | 0 | 3 |
| Long stems (>650 chars) | 2 | 1 |
| 2+ cue-heavy incorrect options | 7 | 4 |
| SBA / SATA | 19/13 | 20/12 |

Full-bank median stem 478 characters; latest 40 median **515.5** versus first 175 median **460**. The newest cases are not consistently shorter, despite earlier realism goals. Across 215, 23 items contain 2+ wrong distractors with cues ('always', 'never', 'automatically', etc); flag for editing rather than assuming a wrong key. Four A–D choices in all 215 also differ from public NABP samples with five A–E choices, and one-question-at-a-time feedback differs from the live exam's one-way timing/CAT design. Real secure item difficulty and candidate item-level distribution are unknown.

## Legal-change risk register — source-first next actions

| Priority | Items | Must verify |
| --- | --- | --- |
| HIGH | E30-028 / 203 | Correct duplicated Part2 concept without corrupting previous history; [HHS 2026 Fact Sheet](https://www.hhs.gov/hipaa/for-professionals/regulatory-initiatives/fact-sheet-42-cfr-part-2-final-rule/index.html), §2.22 |
| HIGH | E30-075 / 202 | FDA Aug6 2026 DSCSA small-dispenser limited relief, effective Nov27 2026; suspect-product quarantine and investigation survive |
| HIGH | E30-049 / 064 / 179 | Current MA CII partial-fill state clocks vs 21 CFR 1306.13 and 105 CMR 721.055; old circular supersession |
| HIGH | E30-189 | Verify precise currently active DEA butalbital NDC exemption after November 9, 2026 final determination |
| HIGH | E30-062 / 191 | Sept2025 Board vaccine technician 500h rule and who assesses/selects vaccine; avoid repeated answer mechanism |
| HIGH | E30-215 | Board Policy 2026-03 ISO5 >15 CFU microbiology result, one-business-day notice, within-BUD recall and mitigation |
| HIGH | E30-206 / 207 / 212 / 213 | 247 CMR 3 pharmacist license transfer, 2026 pharmacist contraception/PrEP and injection authority, and out-state controlled Rx verification |
| MEDIUM | E30-041 /111; E30-026 /091; E30-003 /137 | Similar subjects but distinct personnel and counseling triggers; do not delete automatically |

These are **review priorities, not legal-error verdicts**. Each flagged item requires an exact four-option re-solve from operative state and federal primary sources before assigning independent PASS/FAIL; automated text analysis cannot do that.

## NABP 2027 and Massachusetts regulation timing

- Per [NABP's June 10, 2026 announcement](https://nabp.pharmacy/news/blog/mpje-content-outline/), exams on/after **March 1, 2027** use a **new weighted four-domain outline**: Pharmacy & Pharmacist Practice **30%**, Medication Use Process **30%**, Regulatory Authority & Legal Obligations **20%**, Pharmacy Operations **20%**. The legacy Area 1/2/3/4 in Chapter 30 must **NOT** be treated as the same new four domains or distributions.
- [Massachusetts DPH 105 CMR 700 status](https://www.mass.gov/info-details/105-cmr-700-implementation-of-mgl-c-94c-the-controlled-substances-act) confirms the **Oct. 19, 2026 hearing was for PROPOSED amendments**. Publication of a proposed text is not itself proof of an operative final amendment. Recheck the Massachusetts Register before using new rules.

## Decision and study-readiness evidence

**Stop bulk expansion at 215.** Next deliver a version-safe targeted quality correction for Part2 duplicate and independently readjudicate priority flagged rules. Then use a **fresh, unseen 40-question study session** and categorize first-attempt errors (law/actor, state-v-federal, quantity/deadline, exceptions, interpretation). GitHub does **not** reveal personal same-browser localStorage scores; ask the learner only for a voluntary anonymous score summary. There is no validated probability that passing this bank means passing the real MPJE.

This report is a completed author-driven **population coverage + selected realism + risk screening**, not a completed full legal-audit certification. The 215-item main merge is PR #261 (`400218a73acb5e2eb62981b616ec9ec9a81c350a`); [its GitHub Pages release workflow](https://github.com/woojunxnam/oddments/actions/runs/44118130626) separately tracks deployment and live browser checks. No site files changed in this review PR.
NaN