# Massachusetts MPJE Form E — Batch 5 authoring and source-audit checkpoint

**As of:** November 23, 2026. **Draft PR:** [#296](https://github.com/woojunxnam/oddments/pull/296). **Exam era:** NABP legacy [Competency Statements](https://nabp.pharmacy/programs/examinations/mpje/competency-statements/), valid for tests **through February 28, 2027**. The post-March 1, 2027 domain blueprint must not be substituted.

## Result / safe deployment state

- Authored **E081–E100 (20 new original items)**: 11 single-best-answer (SBA), nine select-all-that-apply (SATA), **100 A–E choices with 100 separate option explanations** and citations.
- **Form E cumulative: 100/120 (83.3%)**, 500 choices with rationales. **20 remaining**.
- **Previously released A–D 480 questions unchanged.** Form E is confined to PR #296's source-draft branch; **NOT merged or publicly deployed**, and the exam renderer/manifests/history code are untouched.
- Explicit `law_status` is AI source check with final review pending. **Not Board endorsement, psychometric exam authentication, qualified independent human legal approval, or proof of future unchanged law.**

## NABP legacy Area allocation

| Legacy Area | E001–E080 | Batch 5 | E001–E100 | Editorial goal | Needed in Batch 6 |
|---|---:|---:|---:|---:|---:|
| 1 | 17 | 4 | 21 | 26 | 5 |
| 2 | 28 | 6 | 34 | 40 | 6 |
| 3 | 19 | 5 | 24 | 29 | 5 |
| 4 | 16 | 5 | 21 | 25 | 4 |
| **Total** | **80** | **20** | **100** | **120** | **20** |

## Quality audit (computed from draft JSONs and 480-question legacy review index)

| Validation | Result |
|---|---|
| All Form E IDs in sequence, E001–E100 | PASS — 100 items |
| Existing A–D 480 review-index IDs + new 100 IDs | 580 unique out of 580 |
| Normalized exact stem duplicates across old 480 review-index stems + E001–E100 | 0 |
| New choice text, keyed letters, separate rationales | 100/100 choices; zero key/rationale status mismatches |
| Batch 5 missing citation, source, novelty or counterfactual fields | 0 |
| All E SBA / SATA | 56 / 44 |
| All E SBA key letters A/B/C/D/E | 9 / 11 / 12 / 12 / 12 |
| Batch 5 SBA correct answer tied for longest | 2/11 (18.2%) |
| All E SBA correct answer tied for longest | 11/56 (19.6%) |
| All E SATA with exactly 2 / 3 / 4 correct choices | 12 / 26 / 6 |

These are automated structural and editorial checks. **An exact-text nonduplicate finding is not proof of absence of semantic overlap**. In a manual review of legal decisions against existing indexed source items, three initial repeated-case concepts were specifically replaced (described below), and item-level nearest cases are preserved in the JSON for later inspection.

## Batch 5 legal decision inventory

| ID | Legacy area | Legal decision | Current cited section(s) |
|---|---|---|---|
| E081 | 1 / 1.1 | Traditional internship 1,000/500-hour route | 247 CMR 8.01(1)(a)1–2 |
| E082 | 1 / 1.2 | Board-recognized technician training program categories | 247 CMR 8.02(3)(e)3.a, 8.02(4)(a)–(d) |
| E083 | 1 / 1.2 | Intern application before first professional year | 247 CMR 8.01(2)(a)–(c),(6)(e) |
| E084 | 1 / 1.2 | Pharmacist immunization continuing education clock | 247 CMR 4.03(4)(a),(e) |
| E085 | 2 / 2.1 | No-substitution prescription interface formatting | 105 CMR 721.020(B)(1)–(3) |
| E086 | 2 / 2.1 | Official-duty military prescriber federal DEA exemption | 21 CFR 1301.23(a); 21 CFR 1306.05(h) |
| E087 | 2 / 2.1 | State ePrescribing exceptions and pharmacist verification limits | 105 CMR 721.070(A)(6),(9),(C); 247 CMR 9.15(2) |
| E088 | 2 / 2.1 | MCSR schedule authorization versus DEA registration scope | M.G.L. c. 94C §7; 105 CMR 700.004; 21 CFR 1306.03(a) |
| E089 | 2 / 2.1 | Qsymia versus Wegovy drug scheduling and formulation | 21 CFR 1308.14(f)(10) (renumbered effective Nov. 12, 2026); FDA Qsymia 2026 label; FDA Wegovy 2026 label; M.G.L. c.94C §2(a) |
| E090 | 2 / 2.1 | Valid physical written prescription under ePrescribing exception | 105 CMR 721.020(A),(F)(1)–(2); 105 CMR 721.040; M.G.L. c.94C §23(i) |
| E091 | 3 / 3.1 | Routine Schedule IV fax as original versus Schedule II fax limitation | 21 CFR 1306.21(a); 21 CFR 1306.11(a),(e)–(g); 105 CMR 721.020(F), 721.070(A)(3) |
| E092 | 3 / 3.4 | Federal Schedule II label exception for institutional administration | 21 CFR 1306.14(a),(c)(1)–(4) |
| E093 | 3 / 3.3 | Clinical DUR: drug-disease contraindication with no software alert | 247 CMR 9.17(1)(c),(2) |
| E094 | 3 / 3.1 | Massachusetts Schedule VI refill record fields | 247 CMR 9.04(6)(a)–(c), 9.04(12) |
| E095 | 3 / 3.6 | Multi-drug compliance pouch beyond-use and contents labeling | 247 CMR 9.08(5)(a)–(e) |
| E096 | 4 / 4.1 | Separate Massachusetts controlled-substance registrations by principal location | 247 CMR 11.01(1)–(2); 11.05 |
| E097 | 4 / 4.1 | MCSR renewal dates for wholesale druggist versus pharmacy | 247 CMR 11.06(1),(3), 11.07(2)(a),(c) |
| E098 | 4 / 4.1 | Automatic MCSR termination after business sale | 247 CMR 11.08(1)(c),(3)–(4); 11.09 |
| E099 | 4 / 4.7 | Controlled-stock pharmacy transfer: date-of-transfer inventory and custody | 247 CMR 6.14(1), (2)(a),(c)–(f) |
| E100 | 4 / 4.5 | Resident versus nonresident pharmacy serious-event Board-reporting scope | 247 CMR 20.02(1),(3),(5); compare 247 CMR 20.07 and other applicable state/federal requirements |

Every E081–E100 JSON item also records actor, jurisdiction, micro-skill, five explanations, exact source links, nearest historical IDs, a legally material novelty statement, and a one-fact counterfactual that would change the analysis.

## Editorial duplicates replaced before this checkpoint

- **E091 original draft withdrawn:** original-quantity Schedule IV partial-fill clock duplicated existing E30-054. Replaced with a *different* legal decision: ordinary Schedule IV **fax may be the prescription** under 21 CFR 1306.21(a), contrasted with routine Schedule II **fax is not the original** absent a §1306.11(e)–(g) exception. Scenario expressly assumes a valid Massachusetts ePrescribing waiver.
- **E099 original draft withdrawn:** resident-pharmacy closure's 90-day patient / 14-day notice rule repeated E30-017. Replaced with **247 CMR 6.14(2)**: inventory on transfer date covers Schedules II–V plus PMP-reportable Schedule VI, transferee receives records the same day, and transferor cannot retain controlled stock after the transfer.
- **E100 original draft withdrawn:** five-year serious-injury reporting-record retention duplicated D083. Replaced with the **247 CMR 20.02(5) nonresident-pharmacy scope exclusion**, expressly without suggesting other state/federal reporting duties disappear.
- **E089 legal cite corrected:** A new DEA rule published November 12, 2026 added Schedule IV oveporexton and renumbered §1308.14(f). Phentermine is now **§1308.14(f)(10)** (not older (f)(9), and not (e)(1), which lists lorcaserin). The answer's Qsymia Schedule IV determination is unchanged.
- Several other initially considered topics were excluded at the planning stage due to previously authored microdecisions: hospital multiple-drug Rx records E30-118; independent NP missing supervisor identifier E30-098; anticoagulant therapy-switch DUR E30-087.

## Official and independent source cross-check references

- [NABP legacy MPJE Competency Statements (valid before 2027-03-01)](https://nabp.pharmacy/programs/examinations/mpje/competency-statements/)
- [247 CMR 8 — Pharmacy interns / technicians](https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download)
- [247 CMR 4 — Pharmacist registration and CE](https://www.mass.gov/doc/247-cmr-4-personal-registration-renewal-continuing-education-requirement/download)
- [247 CMR 6 — Pharmacy facilities](https://www.mass.gov/doc/247-cmr-6-licensure-of-pharmacies/download)
- [247 CMR 9 — Pharmacy practice](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download)
- [247 CMR 11 — Facility controlled-substance registration](https://www.mass.gov/doc/247-cmr-11-registration-under-the-controlled-substances-act-mgl-c94c/download)
- [247 CMR 20 — Reporting and scope exemptions](https://www.mass.gov/doc/247-cmr-20-reporting/download)
- [105 CMR 721 — Prescription format and electronic exception](https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download)
- [21 CFR 1306.05 — Exempt official prescription ID](https://www.ecfr.gov/current/title-21/section-1306.05)
- [21 CFR 1306.11 / 1306.21 — Schedule II and III–V fax](https://www.ecfr.gov/current/title-21/section-1306.21)
- [21 CFR 1306.14 — CII institutional labeling](https://www.ecfr.gov/current/title-21/section-1306.14)
- [21 CFR 1308.14 — Schedule IV](https://www.ecfr.gov/current/title-21/section-1308.14)
- [Nov. 12, 2026 DEA oveporexton Schedule IV / paragraph renumbering](https://www.govinfo.gov/content/pkg/FR-2026-11-12/html/2026-23075.htm)

**Scope:** These sources support the cited clauses and option-level author rationales. Not every URL's live version will remain frozen on test day. Recheck revised §1308.14 numbering and state/regulatory effective dates before promoting to final verified release. For safety the remaining independent professional legal/ambiguity gate is OPEN.

## Unfinished gates and Batch 6

- E101–E120: **20 more questions**, suggested allocation Areas **5 / 6 / 5 / 4** (same legacy blueprint; not 2027 domain relabeling).
- Final legal/option re-verification and semantic novelty review across A–E; complete fixed 120 question Form E manifest; A–E renderer supporting 5-option keys; 150-min timed testing, retake and protected historic score storage; CI/browser checks; staged verification of public site.
- **Do not merge or deploy Draft PR #296 yet.** Preserve A–D and existing answer histories.
