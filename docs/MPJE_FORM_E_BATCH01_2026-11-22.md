# Massachusetts MPJE — Form E Batch 1 Author Review (2026 legacy blueprint)

**Date:** 2026-11-22  
**Scope:** Draft only. **20 of 120** original Form E slots; not in GitHub Pages exam simulation and not a released test.  
**Applicable official NABP reference:** [MPJE Competency Statements](https://nabp.pharmacy/programs/examinations/mpje/competency-statements/) through **February 28, 2027**, not the new March 2027 Content Outline.

## Count and quality checks

| Metric | Observed |
| --- | ---: |
| New stable IDs | E001–E020 (**20**) |
| Answer alternatives with individual explanations | **100** |
| Five alternatives per question | **20/20** |
| Single-best-answer | **11** |
| Select-all-that-apply | **9** |
| SATA count by correct-answer cardinality | **2 correct: 1, 3 correct: 6, 4 correct: 2** |
| Legacy 2026 Area 1 / 2 / 3 / 4 in this batch | **4 / 7 / 5 / 4** |
| Target 120-item legacy area blueprint | **26 / 40 / 29 / 25** |
| Remaining across legacy areas | **22 / 33 / 24 / 21** |
| Original A–D IDs crosschecked | **480** |
| Unique IDs among old + new | **500** |
| Single-best-answer letter counts A/B/C/D/E | **2 / 3 / 2 / 2 / 2** |
| Correct answer is one of the longest options (characters) | **2/11** |
| Key/option-rationale conflicts | **0** |
| Exact duplicate source stem found | **NO** |

**QA result:** STRUCTURAL + KEY/RATIONALE CHECKS PASS.

## Law-source verification scope

These 20 authored scenarios have source-linked editorial answer rationales for all 100 choices. Each answer key is justified against the cited operative legal provision. This is an **AI first-pass official-source review**, not a separate human pharmacist-law review or a psychometrically calibrated measure. Some cross-jurisdiction application and source currency still require routine recheck before release.

Notable operative primary legal authorities:
- [247 CMR 8.00 (interns, technicians, name badges, training credit)](https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download)
- [247 CMR 9.00 (day counting, generic emergency exception, pharmacy stock labels, stock delivery)](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download)
- [21 CFR 1306.05 (agent preparation vs prescriber signature)](https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.05)
- [21 CFR 1311.140 (EPCS two-factor signing)](https://www.ecfr.gov/current/title-21/chapter-II/part-1311/section-1311.140)
- [21 CFR 1308.14 (zuranolone and clonazepam Schedule IV)](https://www.ecfr.gov/current/title-21/chapter-II/part-1308/section-1308.14)
- [FDA DailyMed: Zurzuvae / zuranolone drug label, controlled status](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=f18e53b0-d0bb-422d-8de7-ab64b7292b29)
- [21 CFR 1306.22 (CIII–IV refill authorization and documentation)](https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.22)
- [45 CFR 164.508 (HIPAA paid marketing)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.508)
- [HHS Nov 19, 2026 Privacy Final Rule (effective Jan 19, 2027, compliance Jul 19, 2027)](https://www.govinfo.gov/content/pkg/FR-2026-11-19/html/2026-23429.htm)
- [MGL c.112 §12D (MassHealth transplant narrow-therapeutic-index immunosuppressant)](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section12d)
- [21 CFR 1314.100 (mail-order pseudoephedrine limit)](https://www.ecfr.gov/current/title-21/chapter-II/part-1314/section-1314.100)
- [21 CFR 1304.04 (DEA central recordkeeping exception)](https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.04)
- [21 CFR 1305.13 (received containers/dates on purchaser Form 222)](https://www.ecfr.gov/current/title-21/chapter-II/part-1305/section-1305.13)

## Novelty and exam realism

The draft was screened against all 480 existing A/B/C/D original question stems and examined for similar legal decisions. One initial draft about Soma/carisoprodol versus baclofen was **replaced** after finding that existing E30-169 already tested essentially that recognition. Its replacement tests **Zurzuvae/zuranolone** (not previously present by name in A/B/C/D).

**Related but materially different:** E016's emergency brand dispensing is the *reverse branch* of E30-153 (generic dispensing despite a 'no substitution' order). It is not approved simply because of different wording: the difference is that the normal interchange mandate is temporarily displaced because the cheaper generic is unavailable.

See `drafts/mpje/form-e/form-e-batch01.json` for each case's `closest_existing_ids`, `material_novelty` and `counterfactual_flip`.

## Nearest-neighbor lexical screen (triage only)

| New ID | Nearest old ID | Jaccard of stem tokens |
| --- | --- | ---: |
| E001 | E30-031 | 0.173 |
| E002 | D029 | 0.121 |
| E003 | E30-076 | 0.17 |
| E004 | E30-009 | 0.135 |
| E005 | D036 | 0.238 |
| E006 | E30-271 | 0.125 |
| E007 | E30-319 | 0.135 |
| E008 | E30-169 | 0.103 |
| E009 | E30-054 | 0.241 |
| E010 | D103 | 0.111 |
| E011 | E30-048 | 0.22 |
| E012 | D067 | 0.115 |
| E013 | D033 | 0.178 |
| E014 | E30-229 | 0.156 |
| E015 | E30-044 | 0.143 |
| E016 | E30-153 | 0.304 |
| E017 | E30-024 | 0.15 |
| E018 | D061 | 0.171 |
| E019 | E30-024 | 0.158 |
| E020 | E30-132 | 0.157 |

This lexical score is **not** a semantic novelty certificate and does not independently verify the legal answer. New cases must still be vetted for duplicate *legal conclusions* in later editorial review.

## Not yet done / release conditions

- **100 new questions remain**. Do not claim E is 120/120 or that a public E exam is available.
- **No E/F/G frontend is yet deployed**. A–D existing exam code, question banks, manifests, historical attempts and public URLs were untouched.
- A five-answer A–E renderer, 120-item fixed manifest, forward-only timer/review/history compatibility and mobile/browser checks are needed before publishing E.
- Verify remaining legal cautions, effective-date changes, final novelty, and source-to-answer choice signoff per 20-item batch. **Form E release requires 120 legally accepted original items, not 20 drafts**.
- E/F/G remains an author-built educational assessment, not the secure NABP MPJE/Pre-MPJE, and raw scores cannot be converted to a calibrated MPJE passing probability.
