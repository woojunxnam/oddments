# Massachusetts MPJE Form E — Batch 6 completion and legal/option QA checkpoint

**As of:** November 23, 2026. **Draft PR:** [#296](https://github.com/woojunxnam/oddments/pull/296). **Exam era:** NABP legacy MPJE Competency Statements for tests **through February 28, 2027**.

## Authoring result — 120/120; NOT a legal release

- Completed **E101–E120**, 20 new five-option English items (**8 single-best-answer, 12 select-all-that-apply**), with **100 option-specific explanations** and official-source URLs.
- Six separate draft JSON batches: batch01 E001–E020; batch02 E021–E040; batch03 E041–E060; batch04 E061–E080; batch05 E081–E100; batch06 E101–E120.
- **Form E is fully authored at 120/120 (100%); 600 individual choices and explanations.**
- Existing **480 A–D questions** and scoring/history code have **not been changed**. Total 600 distinct authored A–E IDs across the old bank and new Form E, pending subsequent publication of E.
- Only the **draft branch mpje/form-e-legacy-2026-batch01** has been changed; **no merge and no public GitHub Pages deployment**. Full legal approval, renderer/manifest integration, exam scoring and browser release checks remain OPEN.

## NABP legacy Area target attainment

| Area | E001–E100 | Batch 6 | Final Form E | Target | Remaining |
|---|---:|---:|---:|---:|---:|
| 1 | 21 | 5 | 26 | 26 | 0 |
| 2 | 34 | 6 | 40 | 40 | 0 |
| 3 | 24 | 5 | 29 | 29 | 0 |
| 4 | 21 | 4 | 25 | 25 | 0 |
| **Total** | **100** | **20** | **120** | **120** | **0** |

These are legacy blueprint *authoring* totals, not actual NABP exam scored item counts. The **2027-03-01 new Content Outline must be mapped separately** if the actual test occurs on/after that date.

## Verification and quality controls

| Automated/editorial check | Result |
|---|---|
| Form E files / each expected count | 20, 20, 20, 20, 20, 20 — PASS |
| E001–E120 count and unique IDs | 120 questions / 120 unique — PASS |
| Unique normalized E stems | 120 / 120 — PASS |
| Total choices plus per-option explanations | 600 / 600 — PASS |
| Answer-key versus Correct./Incorrect. rationales | 0 contradictions — PASS |
| Missing Batch 6 primary URL, citation, novelty, counterfactual, legal decision | 0 — PASS |
| Overall single-best-answer / SATA | 64 / 56 |
| Single-best-answer keys A/B/C/D/E | 11 / 12 / 14 / 14 / 13 |
| Keyed SBA answer tied for longest, overall | 12/64 (18.8%) |
| Keyed SBA answer tied for longest in Batch 6 | 1/8 (12.5%) |
| SATA with 2 / 3 / 4 correct choices | 16 / 34 / 6 |

**Novelty screening:** A side-by-side indexed review of old A–D (480) and E001–E100 treated legal `actor/exception/outcome` as more important than matching topics. New decisions cover FPGEC reciprocity, 10.08 non-disciplinary emergency notice, supervised vendor entrance, nuclear pharmacist onsite, DoxyPEP daily-limit, cipepofol vs propofol, conditional federal §1306.26 nonprescription privileges, and MA 2026 patient label shielding. A code-based cross-bank **exact-stem and ID check** found no duplicate E101–E120 among the 480 review-index records. This does **not** constitute a comprehensive expert-certified semantic novelty or accuracy determination.

## Item-level decisions and primary authorities

| ID | Area / competency | New microdecision | Primary legal citations |
|---|---|---|---|
| E101 | 1 / 1.2 | Foreign-school pharmacist reciprocity: required FPGEC and internship | 247 CMR 3.02(1)(b),(3)(a)1–4 |
| E102 | 1 / 1.2 | Summary cease-and-desist and quarantine versus suspension hearing deadline | 247 CMR 10.06(8)–(9), 10.07, 10.08(1)–(3) |
| E103 | 1 / 1.1 | Unlicensed vendor entering prescription area versus handling unbagged stock | Board Policy 2020-15 §§I–II, revised 11/06/2025 |
| E104 | 1 / 1.1 | CDTM mandatory supervision-gap and urgent communication agreement clauses | 247 CMR 16.04(2)(h),(3); 247 CMR 8.02(6) |
| E105 | 1 / 1.1 | Qualified nuclear pharmacist: Board recognition and on-premises presence | 247 CMR 13.02 (Qualified nuclear pharmacist); 13.05(2)–(3),(16) |
| E106 | 2 / 2.1 | Klonopin clonazepam versus BuSpar buspirone schedules | 21 CFR 1308.14(c)(13); M.G.L. c.94C §§2–3 |
| E107 | 2 / 2.1 | Talwin pentazocine versus Nubain nalbuphine scheduling | 21 CFR 1308.14(g)(1); 1308.12(b)(1) nalbuphine exclusion; M.G.L. c.94C §2 |
| E108 | 2 / 2.1 | Pharmacist DoxyPEP: prevention, exposure window and protocol | M.G.L. c.94C §19F; DPH Circular DCP 26-08-125; DPH DoxyPEP statewide guidance (2026) |
| E109 | 2 / 2.1 | 2026 DEA anesthesia drug: cipepofol versus propofol | 21 CFR 1308.14(c)(11); DEA Cipepofol final rule 91 FR 55264 (08/27/2026); DEA Propofol Drug & Chemical of Concern (04/2026) |
| E110 | 2 / 2.2 | 2026 pharmacist administration: long-acting injectable and OTP exception | DPH Circular DCP 26-03-124 (03/11/2026), pp.1–3; 105 CMR 700.004(B)(9) |
| E111 | 2 / 2.1 | First opioid prescription: OUD-treatment exception to Massachusetts seven-day limit | M.G.L. c.94C §19D(a),(c) |
| E112 | 3 / 3.8 | Federal conditional nonprescription Schedule V dispensing limits and professional responsibility | 21 CFR 1306.26 introductory paragraph, (a),(c)–(g), including state-law preservation |
| E113 | 3 / 3.3 | Schedule II opioid dispensing: risk information and antagonist offer | M.G.L. c.94C §18D(b), distinguish §18D(a) prescriber duty |
| E114 | 3 / 3.5 | 2026 reproductive and gender-affirming prescription label shielding: Schedule VI only | Acts 2025, c.16, §7 (effective 2026-01-01), amending M.G.L. c.94C §21; Massachusetts Board Advisory: Prescription Labeling for Reproductive and Gender-Affirming Medications (2025) |
| E115 | 3 / 3.5 | Prescriber personally dispensing controlled medication: MGL §22 label rather than pharmacist label | M.G.L. c.94C §22(b), distinguish §21 pharmacist labeling |
| E116 | 3 / 3.1 | Long-acting non-abuse-deterrent opioid: prescriber assessment and pain-management agreement | M.G.L. c.94C §18A(a)–(b) |
| E117 | 4 / 4.7 | Facility pharmacy licensing cycles: ordinary drug store versus sterile and complex nonsterile | 247 CMR 6.05(2), 6.06(3)(a), 6.07(3)(a) |
| E118 | 4 / 4.7 | New pharmacy must open within one year after application approval | 247 CMR 6.04(7) |
| E119 | 4 / 4.7 | Specialty pharmacy licensure requires satisfactory pre-issuance inspection | 247 CMR 6.04(4), 6.06(2)(b), 6.07(2)(b) |
| E120 | 4 / 4.7 | Facility renewal attestation of all mandatory 247 CMR 20 reporting | 247 CMR 6.04(9)(c); 247 CMR 20.00 |

Each JSON item includes a five-choice English question, choice-specific correct/incorrect legal reasons, a legal decision, actor, critical exception, material difference from nearest existing problem, one-fact outcome-changing counterfactual, and primary-source links.

## High-risk source and effective-date issues inspected

1. **E102 — different clocks:** 247 CMR 10.07 has seven-day hearing for summary license suspension; 10.08(3) allows **15 business days** for the distinct cease-and-desist/quarantine notice, not a final disciplinary revocation.
2. **E109 — new federal Schedule:** The [DEA August 27, 2026 federal rule](https://www.govinfo.gov/content/pkg/FR-2026-08-27/html/2026-17536.htm) added cipepofol to **21 CFR 1308.14(c)(11)**, unlike federally unscheduled propofol. Confirm future scheduling before test.
3. **E112 — conditional federal nonprescription rule:** §1306.26(a) requires the pharmacist, (c) age 18, (e) bound purchaser record, (f) preservation of other state/federal prescription restrictions. No implied Massachusetts permission for actual Rx-only codeine or other preparations.
4. **E114 — current law text reconciliation:** 2025 MA c.16 **§7** amended §21 effective **January 1, 2026** per **§27**. The [December 18, 2025 Board/DPH advisory](https://www.mass.gov/doc/prescription-labeling-for-reproductive-and-gender-affirming-medications-pdf/download) explains the **Schedule VI** practice-name option on prescriber request, preserving practitioner identification in the record and continuing that request for qualifying refills. Some publicly accessible consolidated M.G.L. c.94C §21 displays may omit this operative session-law paragraph; the **signed session law controls**. Federal Schedule III drug labeling is not automatically overridden.
5. **E116 — precise §18A claim:** The law requires initial prescriber assessment of condition/risk/history and **informing and documenting medical appropriateness**; it separately requires a **written pain-management treatment agreement** for long-term ER/LA opioid management. The option rationale was narrowed to the actual text rather than adding an unsupported universal alternatives-counseling element.
6. **E117–E120 — separate pharmacy facility duties:** ordinary Drug Store Pharmacy biennial/odd-year license vs annual sterile/complex nonsterile licenses, specialty pre-issuance Board inspections, one-year opening deadline with written Board permission exception, and renewal attestation of compliance with mandatory 247 CMR 20 reports.

## Sources used for this batch

- [NABP legacy MPJE Competency Statements through February 28, 2027](https://nabp.pharmacy/programs/examinations/mpje/competency-statements/)
- [247 CMR 3 — Pharmacist licensure](https://www.mass.gov/doc/247-cmr-3-pharmacist-licensure-requirements/download)
- [247 CMR 6 — Pharmacy facility licenses](https://www.mass.gov/doc/247-cmr-6-licensure-of-pharmacies/download)
- [247 CMR 8 — Pharmacy personnel](https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download)
- [247 CMR 10 — Disciplinary proceedings, emergency notice](https://www.mass.gov/doc/247-cmr-10-disciplinary-proceedings/download)
- [247 CMR 13 — Nuclear pharmacy](https://www.mass.gov/doc/247-cmr-13-registration-requirements-and-minimal-professional-standards-for-nuclear-pharmacies/download)
- [247 CMR 16 — Collaborative drug therapy management](https://www.mass.gov/doc/247-cmr-16-collaborative-drug-therapy-management/download)
- [Massachusetts Board Policy 2020-15 (updated November 6, 2025)](https://www.mass.gov/doc/2020-15-scope-of-practice-pdf/download)
- [Massachusetts DPH Circular DCP 26-03-124 — pharmacist medication administration](https://www.mass.gov/doc/pharmacist-administration-of-medications-pdf/download)
- [Massachusetts DPH Circular DCP 26-08-125 — pharmacist prescribed STI prevention](https://www.mass.gov/doc/pharmacist-prescribing-of-certain-medications/download)
- [Massachusetts DoxyPEP guidance](https://www.mass.gov/info-details/doxycycline-post-exposure-prophylaxis-doxy-pep-for-bacterial-sti-prevention)
- [M.G.L. c.94C §18A — ER/LA opioid prescribing](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18A)
- [M.G.L. c.94C §18D — opioid antagonist offer](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section18D)
- [M.G.L. c.94C §19D — opioid prescription supply](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section19D)
- [M.G.L. c.94C §22 — prescriber direct-dispensing label](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section22)
- [2025 MA c.16 §7 and §27, 2026-01-01 effective date](https://malegislature.gov/Laws/SessionLaws/Acts/2025/Chapter16)
- [2025 DPH Advisory — reproductive/gender-affirming Schedule VI labeling](https://www.mass.gov/doc/prescription-labeling-for-reproductive-and-gender-affirming-medications-pdf/download)
- [21 CFR 1306.26 — conditional nonprescription dispensing](https://www.law.cornell.edu/cfr/text/21/1306.26)
- [21 CFR 1308.12 — federal Schedule II exclusions](https://www.law.cornell.edu/cfr/text/21/1308.12)
- [21 CFR 1308.14 — federal Schedule IV](https://www.law.cornell.edu/cfr/text/21/1308.14)
- [DEA Final Rule Cipepofol Schedule IV, Aug. 27, 2026](https://www.govinfo.gov/content/pkg/FR-2026-08-27/html/2026-17536.htm)

**Quality status, not external validation:** The 20 new questions underwent AI author review against current cited primary text with all 100 authored rationales, and automated schema/key/format auditing; this is **NOT independent pharmacist or legal-counsel signoff**, secure official NABP question verification, an exam score predictor, or a guarantee of later legislative stability. The official text could change before February 28, 2027.

## Next release gates (NOT performed by this batch)

1. **Full E001–E120 source/effective-date and ambiguity final signoff**, including comparison of older batches with updated state/federal regulations, and final semantic novelty review against A–D.
2. Build immutable **120 question manifest**, integrate Form E five-option SBA/SATA rendering with correct score policy, 150-minute mock, retakes, review and old A–D score-history preservation.
3. Automated tests / browser/mobile testing / link validation, confirmed deployment on GitHub Pages. Keep this PR **DRAFT** and **do not merge/deploy until those gates pass**.
