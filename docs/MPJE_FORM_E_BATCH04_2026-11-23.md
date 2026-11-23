# Massachusetts MPJE Form E — Batch 4 authoring, legal-source and quality report

**Verified/reviewed:** November 23, 2026. **GitHub:** [Draft PR #296](https://github.com/woojunxnam/oddments/pull/296). **Exam era:** NABP [legacy MPJE Competency Statements](https://nabp.pharmacy/programs/examinations/mpje/competency-statements/) used **through February 28, 2027**. The new March 1, 2027 outline has NOT been substituted.

## Completion and release status

- Completed **E061–E080 (20 questions)** and **100 five-choice explanations**. 11 single-best-answer and 9 select-all-that-apply.
- **Form E now 80/120 (66.7%)**; **400** question choices/explanations. **40** items left to write.
- **A–D 480** existing questions preserved unchanged. Total authored mock questions across A–D plus Form E Draft: **560**, but only A–D remain publicly available.
- Files committed **only to Draft PR branch** `mpje/form-e-legacy-2026-batch01`, not merged/deployed. Do **not** deploy or portray Form E as a complete exam.

## Legacy blueprint allocation

| NABP Legacy area | Previous E001–E060 | Added E061–E080 | Total E | Goal | Remaining |
|---|---:|---:|---:|---:|---:|
| Area 1 | 12 | 5 | 17 | 26 | 9 |
| Area 2 | 21 | 7 | 28 | 40 | 12 |
| Area 3 | 15 | 4 | 19 | 29 | 10 |
| Area 4 | 12 | 4 | 16 | 25 | 9 |
| **Total** | **60** | **20** | **80** | **120** | **40** |

## Structural and authoring QC

| Test | Observed |
|---|---:|
| 4 batch JSON files, expected 20 each | 4 of 4 |
| New batch unique IDs E061–E080 | 20 of 20 |
| New batch 5 choices + individual rationales | 100 of 100 |
| Inferred rationale-key contradiction across E001–E080 | 0 |
| New batch missing sources / novelty / counterfactual metadata | 0 |
| Combined 480 legacy IDs + 80 E IDs duplicate IDs | 0 |
| Normalized duplicate stem strings across source index + E JSON | 0 (algorithmic exact-text screen; not semantic proof) |
| Total E single-best / SATA | 45 / 35 |
| Single-best correct letters A/B/C/D/E | 8 / 8 / 10 / 9 / 10 |
| Single-best correct option strictly tied for longest by character | 9/45 (20.0%) |
| New-batch single-best key longest | 2/11 (18.2%) |
| SATA with 2/3/4 correct options | 8 / 21 / 6 |

**Interpretation:** These are code-verified *editorial* metrics. The 480-question source index is a corpus index, not a live production-bank integrity test. A semantic duplicate review was also performed for each specific legal decision, but zero exact duplicate text does not imply zero conceptual overlap. Some new items deliberately build a distinct exception on an existing broad topic (e.g., pentobarbital vs phenobarbital; 2026 injectable administration vs older prescribing items).

## Batch 4 item-level legal decision ledger

| ID | Area / competency | Tested rule, including critical distinction | Citations |
|---|---|---|---|
| E061 | 1 / 1.1 | Active-duty military pharmacist: registration and CE cycle — Earlier items concern expiration and ordinary CE; this examines a military-service validity extension and cycle-specific exemption. | 247 CMR 4.02(8); M.G.L. c.112 §1B(c) |
| E062 | 1 / 1.1 | Reinstatement after more than two years of disciplinary suspension — Different legal trigger from ordinary late renewal: disciplinary suspension longer than two years makes MPJE compulsory but NAPLEX only possible. | 247 CMR 4.02(6)–(7) |
| E063 | 1 / 1.1 | Retired pharmacist license: status and discipline — Tests the legal effect of an approved nondisciplinary retired status and retained disciplinary jurisdiction, not ordinary renewal or license suspension. | 247 CMR 3.04(1)–(4) |
| E064 | 1 / 1.1 | Massachusetts exam-score pairing after a failed examination — Examination pairing for initial licensure rather than NABP reciprocity application validity or an inactive license. | 247 CMR 3.01(6)–(7) |
| E065 | 1 / 1.1 | Pharmacist CE credit for repeated teaching — Separately addresses instructor-credit frequency, not general CE totals, carryover, or record retention. | 247 CMR 4.07 |
| E066 | 2 / 2.1 | Reyvow lasmiditan versus Imitrex sumatriptan schedules — New migraine-specific controlled drug lasmiditan vs ordinary unscheduled triptan, not repeated hypnotic or seizure drug schedules. | 21 CFR 1308.15(e)(6); 105 CMR 700.002 |
| E067 | 2 / 2.1 | Viberzi eluxadoline and Bentyl dicyclomine schedules — Controlled gastrointestinal agent eluxadoline contrasted with nonscheduled antispasmodic; no equivalent drug-class decision in old bank. | 21 CFR 1308.14(g)(3); 105 CMR 700.002 |
| E068 | 2 / 2.1 | Different barbiturate schedules: pentobarbital and phenobarbital — Tests high-risk Schedule II barbiturate pentobarbital; old test addressed phenobarbital only in a different three-drug classification. | 21 CFR 1308.12(e)(3); 21 CFR 1308.14(c)(49); 105 CMR 700.002 |
| E069 | 2 / 2.1 | Sonata zaleplon versus Desyrel trazodone schedules — New hypnotic zaleplon versus off-label sedating antidepressant; previous insomnia items asked zolpidem, suvorexant and ramelteon. | 21 CFR 1308.14(c)(58); 105 CMR 700.002 |
| E070 | 2 / 2.1 | Ztalmy ganaxolone versus Lamictal lamotrigine schedule and brand recognition — Adds ganaxolone Schedule V and specific CDKL5 seizure-brand recognition; other prior antiepileptic items covered lacosamide, cenobamate and brivaracetam. | 21 CFR 1308.15(e)(4); 105 CMR 700.002; FDA Ztalmy 2025 prescribing information |
| E071 | 2 / 2.3 | 2026 pharmacist STI prevention and treatment training: activity-specific — Tests prevention-versus-treatment education specifically under Aug 2026 circular, not previously tested STI diagnosis or EPT scope. | DPH Circular DCP 26-08-125 (Aug. 25, 2026), Sexually Transmitted Infection Prevention and Treatment; M.G.L. c.94C §19F |
| E072 | 2 / 2.3 | 2026 pharmacist administration: lenacapavir, age, route and training — 2026 expansion to lenacapavir and explicit route, age and administration record, rather than old cabotegravir dispensing-vs-prescribing question. | DPH Circular DCP 26-03-124 (Mar. 11, 2026), pp.1–4 |
| E073 | 3 / 3.1 | Patient profile: required reasonable collection, medication history and exceptions — Tests contents of confidential patient profiles and the institutional sterile compounding exclusion, distinct from ransomware downtime. | 247 CMR 9.16(7)–(8) |
| E074 | 3 / 3.1 | Electronic prescription readability and image printout — Printability of eRx and scanned prescription images, not their segregation, retention, or DEA retrieval format. | 247 CMR 9.16(5)–(6) |
| E075 | 3 / 3.3 | 2026 DEA patient-specific injectable OUD medication delivery to prescriber — New current federal patient-specific office delivery provision and 45-day administration clock, rather than prohibited general office stock. | 21 CFR 1306.07(f)(1)–(6), amended in 2026 |
| E076 | 3 / 3.3 | Gabapentin Schedule VI as an additional MassPAT drug: pickup identification — Earlier questions recognized gabapentin's PMP-reporting status or Schedule II-V hardship; this adds the independent pickup-ID consequence of MA additional-drug designation. | 247 CMR 9.04(14)(b)–(d); 105 CMR 700.012(A)(1),(3); DPH Gabapentin circular BHPL-DCP 17-5-101 |
| E077 | 4 / 4.1 | Board approval before pharmacy remodeling and sterile control replacement — Advance permission for layout/secondary-engineering-control work; old D and E items treated relocation, equipment qualification and USP sterile performance rather than approval before construction. | 247 CMR 6.15(1)–(4) |
| E078 | 4 / 4.1 | Special provisional pharmacy license: expiration and extension — Covers time-limited nonrenewable provisional pharmacy license rather than full/nonresident license combinations. | 247 CMR 6.17(1)–(4) |
| E079 | 4 / 4.3 | Controlled stock transfer inventory signature when transferor MOR unavailable — Emergency transferor-MOR signature substitution with notice; D096 tested ten-day inventory attestation after both MORs sign. | 247 CMR 6.14(2)(a)–(d) |
| E080 | 4 / 4.1 | Pharmacy operating-name change notification separate from ownership — Distinct pharmacy operating-name change, rather than ownership transfer, MOR change or relocation. | 247 CMR 6.12 |

Each question's JSON record stores the complete English scenario, five authored choices, rationale for **each** choice, correct-letter array, explicit primary regulation and URL, legal decision, actor, jurisdiction, trigger, critical exception, nearest historical IDs, outcome-flipping counterfactual, and editorial review status.

## Primary-source links actually used

- [Massachusetts pharmacist licensure / reciprocity / retirement — 247 CMR 3.00](https://www.mass.gov/doc/247-cmr-3-pharmacist-licensure-requirements/download)
- [Pharmacist personal registration and CE — 247 CMR 4.00](https://www.mass.gov/doc/247-cmr-4-personal-registration-renewal-continuing-education-requirement/download)
- [Facility licensure — 247 CMR 6.00](https://www.mass.gov/doc/247-cmr-6-licensure-of-pharmacies/download)
- [Professional practice — 247 CMR 9.00](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download)
- [Controlled substances and PMP — 105 CMR 700.000](https://www.mass.gov/doc/105-cmr-700-implementation-of-mgl-c94c-0/download)
- [2026 pharmacist prescribing — DCP 26-08-125](https://www.mass.gov/doc/pharmacist-prescribing-of-certain-medications/download)
- [2026 pharmacist administration — DCP 26-03-124](https://www.mass.gov/doc/pharmacist-administration-of-medications-pdf/download)
- [DEA Schedule II](https://www.ecfr.gov/current/title-21/section-1308.12)
- [DEA Schedule IV](https://www.ecfr.gov/current/title-21/section-1308.14)
- [DEA Schedule V](https://www.ecfr.gov/current/title-21/section-1308.15)
- [DEA practitioner delivery of patient-specific narcotic treatment — 21 CFR 1306.07(f)](https://www.ecfr.gov/current/title-21/section-1306.07)

Supporting FDA brand identity / approval checks for [ZTALMY ganaxolone (2025 label)](https://www.accessdata.fda.gov/drugsatfda_docs/label/2025/215904s011s013lbl.pdf), [REYVOW lasmiditan](https://www.accessdata.fda.gov/drugsatfda_docs/appletter/2020/211280Orig1s001ltr.pdf) and [Viberzi eluxadoline](https://www.accessdata.fda.gov/drugsatfda_docs/label/2020/206940s007lbl.pdf) are separately recorded in the question JSON.

**Point-in-time caution:** Official regulations, DPH circulars, and eCFR were consulted as available November 23, 2026; federal eCFR content was marked updated to November 19, 2026. No prediction is made that no law will change before February 28, 2027. Reverify policy and rule effective dates before final exam publication.

## Meaningful novelty and exam traps

- **Registration vs rights:** Active-military license-extension and CE exemption are *time-qualified*, unlike a suspended/revoked license or retired status.
- **Exam status:** The initial-licensure failed-exam one-year rule is different from the already-tested NABP reciprocity application one-year period.
- **Controlled-drug identity:** Reyvow V, Viberzi IV, pentobarbital II, zaleplon IV, ganaxolone V; familiar therapeutic classes do not imply all products share a schedule.
- **2026 DPH clinical updates:** Prevention and treatment training are activity-specific, and lenacapavir administration requires the circular's permitted routes and age/record conditions.
- **Dispensing and medical records:** The written patient profile, required eRx image print capability, new 21 CFR 1306.07(f) patient-specific 45-day OUD injection use, and gabapentin's special *additional drug* pickup-ID rule each present different mechanisms.
- **Facility permissions:** Prior Board approval for sterile secondary-control work differs from name-change notice within 14 days, nonrenewable provisional licensure, and a Board-notified alternative inventory signer when transferor MOR is unavailable.

## Status of legal review and next steps

**Completed:** primary-source text cross-check; line-by-line editorial author rationale for 100 options; mechanical key consistency; ID and exact-stem checks; measured answer-position and SATA cardinality distribution.

**Not completed:** licensed Massachusetts pharmacy-law counsel/expert signoff; independent professional review; a guaranteed predictive estimate of actual MPJE performance; full legal revalidation at exam day. The `law_status: SOURCE_PASS` label means **AI editor verified the claimed rule against a linked primary-source text**, not external Board or professional approval. Some readings or new DPH guidance remain subject to future amendment.

**Next:** E081–E100 (Batch 5) and E101–E120 (Batch 6). The remaining target allocation is Area 1 **9**, Area 2 **12**, Area 3 **10**, Area 4 **9**. Preserve A–D and retain Draft PR #296 until 120/120, end-to-end curriculum gap audit, and release checks are complete.
