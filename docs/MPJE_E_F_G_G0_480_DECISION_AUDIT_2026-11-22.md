# MPJE G0 — A/B/C/D 480-Item Legal-Decision Classification and Evidence Triage

**Date:** 2026-11-22 (America/New_York)  
**Scope:** existing four mock forms only; no authored question, key, student attempt, or frontend code changed.  
**Result:** **480/480 question IDs have a provisional legal-decision family, verbatim tested scenario and current keyed legal conclusion, source citation, jurisdiction indicators, and review disposition.**  
**CRITICAL QUALIFICATION:** **G0 legal signoff is NOT complete**. This is a reproducible classification/triage ledger, not a claim that all 1,920 choice explanations have been freshly verified against operative legal text. **No G1 official subdomain mapping or all-domain coverage claim has been made.**

## 1. Deliverables and exact counters

- Browsable [480-row G0 review CSV](MPJE_E_F_G_G0_480_REVIEW_INDEX_2026-11-22.csv), alongside the machine-readable [480-row G0 legal-decision ledger](docs/MPJE_E_F_G_G0_480_DECISION_LEDGER_2026-11-22.json) — one row per ID containing question/source path, original scenario, questioned action, as-authored keyed legal conclusion, topic, authority citations, existing legal review status, separate risk/hold flags, and similarity nearest neighbor.
- Previous [480-row structural baseline](MPJE_E_F_G_BASELINE_480_STRUCTURAL_2026-11-22.json) remains intact.
- **IDs: 480 unique / 480 scanned** — A/B 240, C 120, D 120.
- **38 provisional decision families** rather than relying solely on the four broad old exam Areas.
- **10 items with an explicit prior C/D legalHold field**: 9 from C, 1 from D. This is **not** the number of proven erroneous keys or the complete set of unresolved concerns.
- **53 heuristic normative-USP/source-recheck flags** (broad screening for USP-bearing questions; not 53 legal errors).
- **53 heuristic numerical time/deadline flags** (regex-generated; not an exhaustive census of numbers).
- **23 lexical similarity candidates** at TF-IDF cosine >=0.30 within a provisional family. Independent of those scores, a separate **AI editorial first pass** found 3 repeated core legal decisions, 3 partial overlaps, and 17 materially distinct applications. This is not legal key verification or an external human review.
- All 480 carry a prior author's dated `verified` string; this is **not** independent source confirmation.
- Original A/B/C/D have 4 choices and 4 as-authored explanations per question according to a structural read, but those explanations require legal accuracy assessment. **Additional reproducible cross-file integrity check passed**: 480 source objects matched 480 ledger rows, distinct IDs 480, complete authored keys, source URLs/citations/hold fields matched, and no byte-identical normalized stems were found. This checks data consistency, not truth of law.

## 2. Why this review changes E/F/G authoring

Question counts from the *provisional* families show that high-count headings can still conceal repeated microdecisions. **No category total below is an official NABP content-domain count** and no family is certified sufficiently covered until an official-subdomain × legal-decision G1 crosswalk is complete.

| Provisional legal-decision family | A/B | C | D | Total |
| --- | ---: | ---: | ---: | ---: |
| RX_VALIDITY_EPCS | 21 | 7 | 4 | **32** |
| TECH_SCOPE | 18 | 9 | 0 | **27** |
| DRUG_SCHEDULE_ID | 16 | 3 | 4 | **23** |
| DEA_INVENTORY_LOSS | 10 | 0 | 11 | **21** |
| DSCSA_PRODUCT_INTEGRITY | 8 | 2 | 9 | **19** |
| CDTM | 7 | 10 | 0 | **17** |
| USP_HAZARDOUS | 7 | 2 | 8 | **17** |
| LABEL_PACKAGING | 9 | 4 | 4 | **17** |
| USP_STERILE | 8 | 5 | 4 | **17** |
| PRESCRIBER_AUTHORITY | 10 | 7 | 0 | **17** |
| PHARMACIST_PRESCRIBING | 11 | 4 | 0 | **15** |
| BOARD_INSPECTION_REPORTS | 6 | 1 | 7 | **14** |
| MOR_LICENSURE | 2 | 2 | 10 | **14** |
| RETURN_CQI | 6 | 5 | 2 | **13** |
| PHARM_LICENSURE_CE | 9 | 4 | 0 | **13** |
| IMMUNIZATION | 6 | 3 | 4 | **13** |
| BOARD_DISCIPLINE | 7 | 6 | 0 | **13** |
| DELIVERY_COLD | 3 | 2 | 8 | **13** |
| RX_TRANSFER_REFILL | 6 | 6 | 0 | **12** |
| USP_NONSTERILE | 5 | 3 | 4 | **12** |
| PMP_DUR | 4 | 7 | 0 | **11** |
| PHARMACY_GOVERNANCE | 7 | 0 | 4 | **11** |
| COUNSELING | 6 | 4 | 0 | **10** |
| INTERCHANGE | 4 | 2 | 4 | **10** |
| REMS | 5 | 4 | 0 | **9** |
| HOSPITAL_LTCF | 4 | 1 | 4 | **9** |
| DEA_DISPOSAL | 0 | 4 | 5 | **9** |
| HIPAA_PRIVACY | 6 | 2 | 0 | **8** |
| AUTOMATION | 2 | 2 | 4 | **8** |
| DEA_ORDERS | 0 | 0 | 8 | **8** |
| RX_PARTIAL | 4 | 3 | 0 | **7** |
| INTERN_SCOPE | 5 | 2 | 0 | **7** |
| HIPAA_BREACH | 3 | 0 | 4 | **7** |
| FDA_IMPORT_EUA | 0 | 0 | 7 | **7** |
| OTC_PSEUDOEPHEDRINE | 3 | 3 | 0 | **6** |
| OPIOID_OUD | 5 | 0 | 0 | **5** |
| PART2 | 4 | 1 | 0 | **5** |
| FDA_COMPOUNDING | 3 | 0 | 1 | **4** |

Old blueprint metadata: A/B source Area counts **47/94/48/51**; C source Area counts **26/40/29/25**. **Do not combine the numeric D `area` values with these numbers**: D uses a different draft blueprint-era coding. A/B+C legacy Area counts are **73/134/77/76** (360 items), *as-authored* and not independently remapped. The actual G1 must follow the candidate's exam-date version of the NABP blueprint.

## 3. Explicit C/D review flags: separate factual correctness from unclosed evidence

The following summarizes the **previous source reconciliation** and the as-authored hold fields. The descriptions are not newly performed 40-choice source certification:

| ID | Issue | Current action |
| --- | --- | --- |
| E30-277 | Original issuance date vs earliest-fill instruction | Narrow C/D reconciliation supports original issuance-date rule; exact complete option signoff remains pending. |
| E30-286 | Community CDTM scope of protocol | Narrow 247 CMR 16 corroboration recorded; full 4-option review pending. |
| E30-290 | Patient consent withdrawal under CDTM | Narrow 247 CMR 16 corroboration recorded; broader duty context remains for review. |
| E30-313 | CIII–V refill transfer | Narrow 21 CFR 1306.25 / 247 CMR 9.14 corroboration recorded; transfer chain must be checked per fact pattern. |
| E30-335 | Schedule-specific refill validity, federal product exemption | Timing partly corroborated; product/formulation exemption and NDC not independently checked. |
| E30-337 | USP 795 master formulation vs batch record | MA Board inspection text corroborates; subscribed normative USP 795 wording not directly authenticated. |
| E30-338 | USP 795 equipment balance and measurements | MA Board equipment expectation corroborates; complete normative USP 795 wording not authenticated. |
| E30-342 | USP 797 PEC relocation and Category 2 BUD | **Active normative-source HOLD**: exact USP 797 text not authenticated. |
| E30-350 | Hospital controlled drug return/waste | Agency guideline summary corroborates; full underlying primary guideline page retrieval previously limited. |
| D090 | Change of MOR notices | Pharmacy's 14-calendar-day 247 CMR 20.05(1) is directly supported; MOR individual's 9.23(2)(f) 10-day vs 20.05(3) 14-calendar-day overlap must not be answered categorically. |

**D090 scoped primary-source spot check in this session:**
- [247 CMR 20.05(1)](https://www.mass.gov/doc/247-cmr-20-reporting/download): a **Massachusetts pharmacy** notifies the Board of MOR change within **14 calendar days**.
- [247 CMR 20.05(3)](https://www.mass.gov/doc/247-cmr-20-reporting/download): the **individual MOR** notifies within **14 calendar days**.
- [247 CMR 9.23(2)(f)](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download): the **individual MOR's** responsibilities separately mention written notice within **ten days**. Both texts are publicly displayed as operative; unresolved overlap must remain visible. D090 asks only for the **pharmacy** notice and is *not* established incorrect on its own.
- **Do not change any key merely due to this conflict.** Prefer narrow questions about the pharmacy duty; do not teach an unsupported single MOR-personal deadline until clarified.

Additional high-risk **historical scope** flags: **E30-058** (ordinary oral order/failover clock conflict), **E30-116** (differing Board reporting triggers) and **E30-190** (USP 797 Category 2 table reference). Earlier author revisions narrowed these questions; source caveats are not erased by revisions.

## 4. Substantive comparison of 23 high-similarity pairs — AI editorial first pass

Original scenarios and keyed conclusions were read side-by-side for **all 23** flagged pairs. The editorial review concluded **3 likely repeated core legal decisions, 3 partial overlaps, and 17 materially distinct exceptions/actors/workflows**. These are editorial assessments, **not a qualified independent human review or confirmation that either key is legally correct**. Any future removal or score exclusion requires a separate version-controlled decision.

| Existing pair | Editorial disposition | Why |
| --- | --- | --- |
| E30-013 / E30-130 | PARTIAL OVERLAP | Repeats the nonpreserved aqueous 14-day BUD but adds preserved aqueous 35-day categorization and other contrasts. |
| E30-044 / E30-094 | DISTINCT MATERIAL EXCEPTION | Mobile vendor special 30-day limit vs ordinary in-person retailer daily/rolling limit. |
| D029 / D030 | DISTINCT MATERIAL EXCEPTION | Device approval/manufacturer validation vs ingredient-specific FDA API/IND compatibility. |
| E30-233 / D102 | DISTINCT MATERIAL EXCEPTION | Part 2 under-500 breach vs HIPAA 500+ HHS notice: different record regime and reporting clock. |
| E30-023 / E30-127 | CORE LEGAL DECISION REPEATED | Both ask 247 CMR 9.01 return of improperly dispensed medication versus properly dispensed unwanted drug; second adds suspected contamination already encompassed in the same mandatory-return rule. |
| E30-115 / D095 | CORE LEGAL DECISION REPEATED | Separate MA nonresident complex nonsterile license already explicitly tested within earlier E30-115 licensure-combination SATA. |
| E30-026 / E30-091 | DISTINCT MATERIAL EXCEPTION | Training-personnel exclusion and trainee counting differ from baseline 1:4 technician ratio choice. |
| E30-018 / D072 | PARTIAL OVERLAP | Repeats initial DEA and MA theft-report clocks but distinctly tests the DEA Form 106 45-day completion clock. |
| E30-233 / D101 | PARTIAL OVERLAP | Same under-500 HHS reporting clock but differs by HIPAA-covered pharmacy versus Part 2 records and application. |
| E30-188 / E30-358 | DISTINCT MATERIAL EXCEPTION | AB1 match and dosage-form interchange contrasted with multi-code AB distinctions rather than the same simple interchange. |
| E30-091 / E30-250 | DISTINCT MATERIAL EXCEPTION | Trainer begins independently filling; formerly excludable trainer now counts and changes staffing conclusion. |
| E30-349 / D073 | DISTINCT MATERIAL EXCEPTION | Patient direct deposit versus staff counting/handling adds legally material actor and custody rule. |
| E30-029 / E30-322 | DISTINCT MATERIAL EXCEPTION | Prescriber-directed conventional packaging on transferred Rx versus patient-specific request for a separate prescription. |
| E30-037 / E30-293 | DISTINCT MATERIAL EXCEPTION | MIIS objection combined with VIS/pre-administration lookup vs timing and processing of MIIS objection reporting. |
| E30-034 / E30-313 | DISTINCT MATERIAL EXCEPTION | Outside transfer after shared database moves with one-time outside federal allowance; contrasted with ordinary shared-database exception. |
| D021 / D024 | DISTINCT MATERIAL EXCEPTION | Pass-through cleaner-side classification rather than mere numerical ISO environmental action table. |
| E30-358 / D041 | DISTINCT MATERIAL EXCEPTION | Multiple Orange Book AB codes on one RLD and multi-code matching rather than simple AB1-vs-AB2 equivalence. |
| E30-129 / E30-331 | CORE LEGAL DECISION REPEATED | Suboxone buprenorphine/naloxone Schedule III is already expressly a correct identification in E30-129's three-drug classification. |
| E30-208 / E30-238 | DISTINCT MATERIAL EXCEPTION | Schedule III veterinarian with only Schedule VI MCSR/no DEA, contrasted with valid SVI veterinary non-DEA prescription. |
| E30-094 / E30-333 | DISTINCT MATERIAL EXCEPTION | Retailer self-certification and training vs quantity and mobile vendor purchase limits. |
| E30-016 / E30-248 | DISTINCT MATERIAL EXCEPTION | Unchecked new Rx during pharmacist break must be held; earlier case is prechecked and releasable with follow-up. |
| E30-023 / E30-298 | DISTINCT MATERIAL EXCEPTION | Undispensed return-to-stock vs already-dispensed contaminated return, not just acceptance of dispensed error. |
| E30-117 / E30-267 | DISTINCT MATERIAL EXCEPTION | Hospital DEA registration/suffix permitted in hospital practice but cannot authorize unrelated private-office practice. |

**Priority novelty fixes for Form E/F/G:** **E30-023 / E30-127**, **E30-115 / D095**, **E30-129 / E30-331**. Do not create another question merely replicating these same underlying legal conclusions. Do **not** silently delete or edit the current A–D questions, keys, or users' old attempts.

## 5. Readiness source-audit status, by population

| Form | What is established | What is not established |
| --- | --- | --- |
| A/B (240) | 240 existing items, author date/source, previous AI-supported rechecks including 215-item audit plus subsequent additions | Current fresh 960-option independent final legal signoff; external qualified human review; all-source normative USP access |
| C (120) | 120 item draft/published pool, 9 tracked source questions with previous narrow source reconciliation | All 480 choices newly verified and frozen; exact USP norm and one hospital DPH retrieval caveat resolved |
| D (120) | 120 drafted items, earlier author source reviews, specific high-risk groups spot-checked | Full 480-choice legal release signoff; D still `legal-review preview`; D090 MOR-personal conflict resolved |

**Classification count = 480/480. G0 legal release gate = NOT PASSED.** Do not use these records to proclaim that A–G already covers all actual MPJE rules, or that a given mock score predicts an actual pass.

## 6. Exact decision to make before the next new E batch

1. **Adjudicate the 10 explicit C/D hold/caveat items**, and the historical E30-058/E30-116/E30-190 issues, against directly effective primary sources. Where full normative USP text is needed but not accessed: **HOLD/replace the specific assertion**, not silently approve.
2. **Resolve the 3 core-decision repetitions and 3 partial-overlap candidates** from the AI editorial comparison at a separately approved novelty gate before generating E/F items. Repeated *topics* can be necessary; repeated *decisions* without new reasoning are not.
3. **For each 480 question, validate the provisional decision-family tag** using full stem and keyed conclusion, then record explicit `official_2026_subdomain` / `official_2027_subdomain` based on the actual new/old NABP source only in **G1**. Do not auto-relabel the D numbers.
4. For final legal source approval, independently verify each relevant choice against actual statutes, regulations, Board policy/DPH guidance and applicable current USP; verify dates, exceptions, patient and practitioner scope. Legacy author `verified` strings are not a substitute.
5. When deciding E/F quotas, use **uncovered legal decision tuples** (actor + context + trigger + rule + exception + action), not just the category totals in this report. Hold Form G until E/F actual learning is complete.

## 7. Primary authorities for spot checks and the next source gate

- [NABP 2026 MPJE Competency Statements](https://nabp.pharmacy/programs/examinations/mpje/competency-statements/) — exams before March 1, 2027.
- [NABP Content Outline change effective 2027-03-01](https://nabp.pharmacy/news/blog/mpje-content-outline/) — do not interpret old Areas as new Domains.
- [Massachusetts Board MPJE review reference list](https://www.mass.gov/doc/multistate-pharmacy-jurisprudence-examination-mpje-review-information/download) — 247 CMR, 105 CMR, official Board policies/circulars, Mass. statutes, federal law.
- [MA 247 CMR 9 professional practice standards](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download) and [MA 247 CMR 20 reporting](https://www.mass.gov/doc/247-cmr-20-reporting/download).
- [Prior C/D targeted legal recheck](MPJE_FORM_C_D_LAW_VERIFICATION_RELEASE_GATE_2026-11-22.md), [earlier 215 audit](MPJE_CH30_215_REVIEW_ROLLUP_2026-11-17.md), and [A/B/C assessment-bias audit](MPJE_CH30_330_READINESS_GAP_AUDIT_LAST39_2026-11-18_KO.md).

**Do not modify original A/B/C/D question text or learning history as part of this classification report.** If a key is eventually proven legally incorrect, make a separately reviewed versioned correction and preserve archived attempts.
