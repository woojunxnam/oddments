# Massachusetts MPJE — Form F Batch 2 source and item-release QA (F031–F060)

**Date:** November 23, 2026. **Blueprint:** NABP legacy Competency Statements for an exam **before March 1, 2027**. **GitHub:** Draft [PR #297](https://github.com/woojunxnam/oddments/pull/297).

## Decision and released scope

**BATCH 2 AUTHOR COMPLETE, APPROVED FOR DRAFT BANK ONLY; NOT PUBLICLY RELEASED.** 30 new English law-application items F031–F060, 5 A–E alternatives each, 150 option-level rationales. Previous Form F F001–F030 untouched. Form F is now **60/120 authored**, with 60 questions remaining. Source comparisons are an **AI author review**, not independent lawyer/pharmacist or NABP release certification.

## Quantitative test results (computed on current JSON)

| Check | Result |
|---|---|
| Expected new IDs | F031–F060, 30 unique |
| Area1/Area2/Area3/Area4 within batch | **6 / 10 / 8 / 6**, target met |
| Overall F001–F060 Area counts | **13 / 20 / 15 / 12** |
| SBA / SATA in F031–F060 | **16 / 14** |
| All F001–F060 option/rationale count | **300** |
| SBA key A/B/C/D/E in Batch2 | **1 / 4 / 3 / 4 / 4** |
| SATA 2-correct / 3-correct / 4-correct in Batch2 | **7 / 7 / 0** |
| Correct SBA answer also the longest choice | **1/16** (F040) |
| Option key-vs-rationale mismatches | **0** |
| Invalid SBA/SATA key cardinalities | **0** |
| Missing legal citation, source URL, novelty, actor, counterfactual | **0** |
| Exact normalized stem overlaps with A–D 480 index | **0** |
| Duplicate IDs or exact normalized stems F001–F060 | **0** |

Automated exact-text uniqueness and option-length checks do **not** establish legal correctness, semantic uniqueness or actual NABP predictive validity. Reviewers must still examine actor, applicable dates, exception, action, and distractors. The editorial QA records the closest existing cases in each JSON item.

## Microdecision-by-item source ledger

| ID | Area | Legal decision examined | Regulation / source |
|---|---:|---|---|
| F031 | 1 | Trainee hospital ADD stocking: independently transported CIII–VI versus prohibited CII | Massachusetts Joint Policy 2023-08 §§II(1)–(6), III(1)–(2); 247 CMR 8.00 |
| F032 | 1 | Certified tech inventory-system to ADD exception: ordinary SVI versus gabapentin | Massachusetts Joint Policy 2023-08 §V(1)–(2) (PMP-drug exclusion) |
| F033 | 1 | Retail pharmacy emergency ADD: nurse loading versus uncertified trainee | Joint Policy 2019-02, revised 05/25/2023, §§10(a)–(b), 11–12 |
| F034 | 1 | Former nurse still has hospital ADD permissions: revoke unauthorized access | Joint Policy 2019-02 §§4–6, revised 05/25/2023 |
| F035 | 1 | Cashier detects dispensing QRE: immediately escalate, pharmacist documents within 24 hours | 247 CMR 15.03(1)(a)–(c), (2)(a)–(b) |
| F036 | 1 | Wholesaler temporary warehouse labor untrained in cold-chain inspection | 247 CMR 7.02(9); 7.04(4)(a) |
| F037 | 2 | Liquid outpatient prescription leaves pharmacy without a suitable measuring device | 247 CMR 9.18(5)(b)–(c), (9) |
| F038 | 2 | Hospital discharge prescription greater than 14 days: smallest manufacturer package exception | 105 CMR 722.090(B)(1)–(2) |
| F039 | 2 | Hospital discharge medicine unavailable at retail: full quantity not automatic refill | 105 CMR 722.090(B)–(D) |
| F040 | 2 | Hospital nursing-unit unused Schedule VI portion: registered-nurse waste duty versus SII–V two-witness practice | Massachusetts DPH General Accountability Guidelines for Controlled Substances in Hospitals and Clinics with Pharmacies, Nursing Units — Disposal of unused portions (Schedule VI versus Schedules II–V) |
| F041 | 2 | Clinic pharmacy prescription must be from clinic practitioner for current registered patient | 105 CMR 722.091(A), 722.020 |
| F042 | 2 | Hospital formulary interchange must honor prescriber no-substitution instruction | 105 CMR 722.090(E); 247 CMR 9.05(3)(e) |
| F043 | 2 | Admitted inpatient transferred before overnight still qualifies as hospital inpatient | 105 CMR 722.020 definition of Hospital Inpatient; 722.090(A)–(B) |
| F044 | 2 | Prospective DUR finds age-related contraindication despite insurer authorization | 247 CMR 9.17(1)(j),(2); 247 CMR 9.04(1) |
| F045 | 2 | Mail-order drug packaging not validated for projected temperature exposure | 247 CMR 9.02(1)–(3), with emphasis on (2) |
| F046 | 2 | Hospital controlled-nursing-unit records need weekly QA independent of double lock | DPH General Accountability Guidelines for Controlled Substances in Hospitals/Clinics with Pharmacies, Nursing Units—General; compare 105 CMR 700.000 |
| F047 | 3 | Schedule VI electronic files must be separately retrievable even if not DEA scheduled | 247 CMR 9.16(1),(2)–(4) |
| F048 | 3 | Emergency oral Schedule II written follow-up never arrives: pharmacist must notify DEA | 21 CFR 1306.11(d)(2)–(4); DEA Practitioner's Manual, emergency prescribing |
| F049 | 3 | Prospective DUR identifies probable undertreatment without software warning | 247 CMR 9.17(1)(a),(f),(i),(2) |
| F050 | 3 | Pharmacy purchasing and disposal records: separate retention from serious QRE ledger | 247 CMR 9.16(1), compare 9.21(8)–(10) |
| F051 | 3 | Pharmacy initiates a patient-requested prescription transfer as patient's agent | 247 CMR 9.14(1)–(4) |
| F052 | 3 | Multi-dose adherence packaging must be tamper-evident and not reclosable | 247 CMR 9.08(1)(a)–(g), especially (e) |
| F053 | 3 | DEA Form 222 POA revoked by current registration signer with two witnesses | 21 CFR 1305.05(a)–(c),(e)(1)–(2), as amended March 20, 2026 (91 FR 13499) |
| F054 | 3 | DSCSA formerly illegitimate product: termination notice requires FDA consultation | 21 U.S.C. §360eee-1(d)(4)(B)(iv); FDA 'Notify FDA of Illegitimate Products' termination process |
| F055 | 4 | Massachusetts wholesale druggist licensing is separate for each warehouse location | 247 CMR 7.02(1),(4) |
| F056 | 4 | Wholesaler updated warehouse contact information triggers 30-day Board written update | 247 CMR 7.02(5)(c),(6) |
| F057 | 4 | Wholesaler offsite records electronically unavailable: two working days | 247 CMR 7.04(6)(a)–(c) |
| F058 | 4 | Wholesale return with opened tamper-evident outer seal: quarantine and disposition | 247 CMR 7.04(1)(c),(5)(a)–(c) |
| F059 | 4 | Wholesaler FIFO default permits only appropriate temporary deviation | 247 CMR 7.04(7)(a) |
| F060 | 4 | Nonresident pharmacy explicit exemptions do not waive all Massachusetts dispensing law | 247 CMR 9.19(23) (9.19(11),(16) exceptions); 9.20 |

Each item also carries source links in `source_urls[]`, five rationales, legal decision, critical exception, outcome-changing counterfactual, reviewer type and nearest previous IDs.

## Real corrections made before approval for the draft bank

1. **F040 replaced**: Initial outpatient clinic take-home case was uncomfortably similar to existing E30-112. Final F040 now tests the **hospital unused Schedule VI portion: registered nurse versus two-licensed-staff Schedule II–V witnessing** under the official [DPH hospital/clinic accountability guidance](https://www.mass.gov/info-details/general-accountability-guidelines-for-controlled-substances-in-hospitals-and-clinics-with-pharmacies).
2. **F041 scoped**: Clinic pharmacy specifically has pharmacy services on the facility license; its distinct defect is the outsider prescribing practitioner rather than lack of a facility pharmacy authorization. This separates the legal decision from other clinic dispensing cases.
3. **F045 replaced**: Original hospital employee's unrelated-household adult son case repeated Form E E029. Final asks the **prospective handling of a temperature-sensitive patient shipment without appropriate validated packaging** under 247 CMR 9.02.
4. **F053 modernized**: Corrected the **March 20, 2026 amendment** to DEA Form 222 power-of-attorney revocation to reflect a registrant, partnership partner or corporate officer as authorized signatory, plus two witnesses. Current [21 CFR 1305.05(e)](https://www.law.cornell.edu/cfr/text/21/1305.05) and [March 2026 Federal Register amendment](https://www.govinfo.gov/content/pkg/FR-2026-03-20/html/2026-05482.htm) control; some older DEA FAQ descriptions still refer to the most recent registration application's signer.
5. **F031, F033, F041, F042, F048, F053**: A–E alternatives were scrutinized for independent legally supported actions, and SATA keys adjusted to avoid predictable two-correct distribution. In particular F031 policy §II(5) requires healthcare professional barcode/electronic validation upon removal/administration, while §III limits PTT independently supervised loading to pharmacist-verified Schedule III–VI.
6. **Seven SBA answers shortened without changing their correct legal outcomes**, eliminating a visible answer-length cue. One of 16 SBA correct answers remains the longest.

## Source-specific checks and limits

- The exact training, staff access, dispensing and stocking conditions in 2023 [Massachusetts Joint Policy 2023-08](https://www.mass.gov/policy-statement/use-of-pharmacy-technician-trainees-to-stock-automated-dispensing-devices) and 2023/updated [Joint Policy 2019-02](https://www.mass.gov/policy-statement/automated-dispensing-device-use) were used specifically for hospital vs emergency-kit ADD roles. Different stocking types are not interchangeable.
- Current [DPH hospital/clinic controlled-accountability guidelines](https://www.mass.gov/info-details/general-accountability-guidelines-for-controlled-substances-in-hospitals-and-clinics-with-pharmacies) distinguish Schedules II–V witness/cosign residual waste from Schedule VI disposal by an RN; also require weekly controlled administration QA.
- [105 CMR 722.090](https://www.law.cornell.edu/regulations/massachusetts/105-CMR-722-090) distinguishes ordinary 14-day hospital ED/discharge supply, manufacturer's minimum package >14 days, and genuine retail-unavailable products; [105 CMR 722.091](https://www.law.cornell.edu/regulations/massachusetts/105-CMR-722-091) separately limits clinic practitioner orders and recipients.
- [247 CMR 7](https://www.mass.gov/doc/247-cmr-7-wholesale-druggists/download) governs warehouse-by-warehouse licensure, 30-day contact change, 2-working-day non-retrievable central records, quarantined opened sealed-secondary returns, and temporary appropriate deviation from FIFO. All are **wholesale operations**, not retail pharmacy dispensing.
- [247 CMR 9.17](https://www.law.cornell.edu/regulations/massachusetts/247-CMR-9-17) specifically includes age-related contraindications, under-utilization, and clinically material dose changes; payer approval is irrelevant to that professional DUR duty.
- FDA [DSCSA termination notification](https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/notify-fda-illegitimate-products) requires agency consultation and prompt notice to the immediate trading partners informed under the earlier notification.

**Important:** Links to public Board and DPH policies or statutory text support only their express requirements. No inference of authentication of a subscribed USP normative chapter, no private NABP item access and no independent human expert validation is claimed.

## Next production action under frozen contract

Proceed to **Batch 3 F061–F090** (Area 1/2/3/4 = **7/10/7/6**). Do not reopen the A–E historical audits or redesign Form F; keep A–E questions and score histories unchanged. After all 120 F questions, run one bounded Form F-only final source/option gate, frozen manifest and desktop/mobile test, then public release and live URL verification if the gate passes.
