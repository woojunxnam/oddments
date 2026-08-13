# Phase 2 Batch B LEGAL_VERIFICATION

## 결론

| Verdict | Count |
|---|---:|
| `KEEP` | 38 |
| `MINOR_EDIT` | 1 |
| `MAJOR_REWRITE` | 1 |
| `DELETE` | 0 |

- `audit_status`: `FULLY_ADJUDICATED`
- frozen SHA: `67464e7a7ff2cfe88285c7c0f0f4164e92df46cd`
- non-`KEEP`: `MA-Q-0058`, `MA-Q-0081`
- 모든 SATA option은 proposition별로 별도 판정했고, drug-linked item은 current DailyMed labeling과 21 CFR Part 1308 schedule을 교차 확인했다.

## Item-by-item adjudication

| Question_ID | Verdict | Existing_Answer_Correct | Proposed_Answer | Finding |
|---|---|---|---|---|
| `MA-Q-0051` | `KEEP` | `YES` | A: A complete CQI program that detects, documents, assesses, and prevents quality-related events. | key 일치; `MA-CQI-PROGRAM`의 current trigger·deadline·scope 확인 |
| `MA-Q-0052` | `KEEP` | `YES` | B: Notify the patient or representative, give correction and harm-minimization directions, and contact the prescriber when professionally indicated. | key 일치; `MA-QRE-NOTIFY`의 current trigger·deadline·scope 확인 |
| `MA-Q-0053` | `KEEP` | `YES` | C: Within 24 hours after the pharmacist discovered or was told of the event. | key 일치; `MA-QRE-DOCUMENT-24H`의 current trigger·deadline·scope 확인 |
| `MA-Q-0054` | `KEEP` | `YES` | D: Analyze causes and contributing system factors and use the findings to improve the process. | key 일치; `MA-QRE-ANALYSIS`의 current trigger·deadline·scope 확인 |
| `MA-Q-0055` | `KEEP` | `YES` | E: Provide ongoing CQI education to pharmacy personnel at least annually. | key 일치; `MA-QRE-ANNUAL-ED`의 current trigger·deadline·scope 확인 |
| `MA-Q-0056` | `KEEP` | `YES` | A: Report the qualifying event to the Board within seven business days of discovery. | key 일치; `MA-SERIOUS-EVENT-REPORT`의 current trigger·deadline·scope 확인 |
| `MA-Q-0057` | `KEEP` | `YES` | B: Retain the readily retrievable supporting records for at least five years from filing. | key 일치; `MA-SERIOUS-EVENT-RECORDS`의 current trigger·deadline·scope 확인 |
| `MA-Q-0058` | `MINOR_EDIT` | `YES` | C: Provide written notice to the responsible DEA field division within one business day and complete the required Form 106 process. | key C는 correct이지만 explanation이 current 21 CFR 1301.74(c)의 두 시계를 분리하지 않는다. written field-division notice는 1 business day이고, electronic DEA Form 106 completion은 discovery부터 45 calendar days이다. |
| `MA-Q-0059` | `KEEP` | `YES` | D: Take an initial inventory of controlled substances on the date controlled-substance activity begins. | key 일치; `FED-INVENTORY-INITIAL`의 current trigger·deadline·scope 확인 |
| `MA-Q-0060` | `KEEP` | `YES` | E: The federal biennial inventory interval has been exceeded. | key 일치; `FED-INVENTORY-BIENNIAL`의 current trigger·deadline·scope 확인 |
| `MA-Q-0061` | `KEEP` | `YES` | E: Use an exact count because the opened container holds more than 1,000 dosage units. | key 일치; `FED-INVENTORY-COUNT`의 current trigger·deadline·scope 확인 |
| `MA-Q-0062` | `KEEP` | `YES` | E: Maintain the DEA-required records for at least two years and keep them available for inspection. | key 일치; `FED-CS-RECORDS-2Y`의 current trigger·deadline·scope 확인 |
| `MA-Q-0063` | `KEEP` | `YES` | C: Use a DEA Form 222 or compliant digitally signed electronic order unless a specific exception applies. | key 일치; `FED-FORM222-ORDER`의 current trigger·deadline·scope 확인 |
| `MA-Q-0064` | `KEEP` | `YES` | D: The ordinary 60-day Form 222 validity and partial-shipment window has expired. | key 일치; `FED-FORM222-60DAY`의 current trigger·deadline·scope 확인 |
| `MA-Q-0065` | `KEEP` | `YES` | E: Reject and return the defective form; it cannot be corrected and must be replaced. | key 일치; `FED-FORM222-DEFECT`의 current trigger·deadline·scope 확인 |
| `MA-Q-0066` | `KEEP` | `YES` | A: Immediately report the loss to the responsible DEA Special Agent in Charge with available form details. | key 일치; `FED-FORM222-LOSS`의 current trigger·deadline·scope 확인 |
| `MA-Q-0067` | `KEEP` | `YES` | B: Maintain the executed paper Form 222 copies separately from other records for at least two years. | key 일치; `FED-FORM222-RECORDS`의 current trigger·deadline·scope 확인 |
| `MA-Q-0068` | `KEEP` | `YES` | C: Use CSOS-enabled software and a valid DEA-issued digital certificate for a compliant electronic order. | key 일치; `FED-CSOS`의 current trigger·deadline·scope 확인 |
| `MA-Q-0069` | `KEEP` | `YES` | D: Maintain the complete destruction record, including drug, quantity, method, date, place, and required witnesses. | key 일치; `FED-FORM41`의 current trigger·deadline·scope 확인 |
| `MA-Q-0070` | `KEEP` | `YES` | E: Registrant destruction must render the controlled substances permanently non-retrievable. | key 일치; `FED-DISPOSAL-NONRETRIEVABLE`의 current trigger·deadline·scope 확인 |
| `MA-Q-0071` | `KEEP` | `YES` | A: Verify the recipient is appropriately DEA-registered as a reverse distributor and follow the transfer records. | key 일치; `FED-REVERSE-DISTRIBUTOR`의 current trigger·deadline·scope 확인 |
| `MA-Q-0072` | `KEEP` | `YES` | B: The ordinary rule calls for certified written Board notice at least 14 days before closure. | key 일치; `MA-PHARMACY-CLOSURE-NOTICE`의 current trigger·deadline·scope 확인 |
| `MA-Q-0073` | `KEEP` | `YES` | A: Under these facts, identify patients who received prescriptions in the preceding 90 days.; C: In this setting, attempt notice at least 14 days before closure and post conspicuous notice.; D: Requested patient-file transfers is required to be handled timely so therapy is not delayed. | key 일치; `MA-PHARMACY-CLOSURE-PATIENTS`의 current trigger·deadline·scope 확인 |
| `MA-Q-0074` | `KEEP` | `YES` | B: Submit original licenses and the controlled-substance registration inside 14 days.; C: At this stage, attest to lawful controlled-substance disposal or transfer.; E: Given the described event, the post-closure submission deadline is 14 days after the pharmacy closes. | key 일치; `MA-PHARMACY-CLOSURE-CS`의 current trigger·deadline·scope 확인 |
| `MA-Q-0075` | `KEEP` | `YES` | D: At this stage, the trainee may perform only duties allowed for that category under pharmacist supervision.; E: Given the described event, professional judgment functions remain with the pharmacist. | key 일치; `MA-TECH-SCOPE`의 current trigger·deadline·scope 확인 |
| `MA-Q-0076` | `KEEP` | `YES` | A: The personnel category is required to be authorized by 247 CMR 8.05 for the assigned handling step.; C: On this record, the pharmacist remains responsible for required supervision and final professional functions. | key 일치; `MA-TECH-CII`의 current trigger·deadline·scope 확인 |
| `MA-Q-0077` | `KEEP` | `YES` | B: On this record, the intern must work under direct supervision of a registered pharmacist preceptor.; D: For this scenario, intern status does not authorize independent pharmacist practice.; E: Under these facts, the pharmacist preceptor remains responsible for the direct-supervision relationship. | key 일치; `MA-INTERN-SUPERVISION`의 current trigger·deadline·scope 확인 |
| `MA-Q-0078` | `KEEP` | `YES` | B: For this scenario, no more than 12 hours may be credited for that day.; D: Under these facts, the remaining work time does not override the daily internship-credit cap. | key 일치; `MA-INTERN-12H`의 current trigger·deadline·scope 확인 |
| `MA-Q-0079` | `KEEP` | `YES` | A: Under these facts, complete at least 20 contact hours in each calendar year of the cycle.; B: In this setting, include at least two contact hours of pharmacy law in each calendar year.; C: At this stage, no more than 15 contact hours in a calendar year may ordinarily be satisfied through home study.; E: Given the described event, unused annual continuing-education hours do not carry into the next calendar year. | key 일치; `MA-PHARMACIST-CE`의 current trigger·deadline·scope 확인 |
| `MA-Q-0080` | `KEEP` | `YES` | A: In this setting, the applicable sterile-compounding CE requirement must be met annually.; C: At this stage, the applicable complex-nonsterile compounding CE requirement must also be assessed.; E: Given the described event, sterile and complex-nonsterile compounding duties are cumulative when both activities are supervised. | key 일치; `MA-CE-COMPOUNDING`의 current trigger·deadline·scope 확인 |
| `MA-Q-0081` | `MAJOR_REWRITE` | `PARTIALLY` | A, D; B는 현재 문구로는 제외하고 아래와 같이 수정한 뒤 포함 | option B의 'degree-or-experience'는 statute만 요약해 current entrant에게 PharmD alone가 충분한 것처럼 읽힌다. 현행 247 CMR 16.02(1)(c)는 five years of licensed experience, pre-6/30/2017 PharmD agreement grandfather, 또는 Board-equivalent education/residency pathway를 요구한다. stem은 지금 agreement에 들어가려는 pharmacist이므로 stricter current regulation을 빼면 answer가 unsafe하다. |
| `MA-Q-0082` | `KEEP` | `YES` | A: Given the described event, the patient must receive notice and consent to the retail collaboration.; B: On this record, actions must stay within the agreement, referral, disease states, and statutory retail scope.; C: The collaboration is required to be established through the written agreement and supervising-physician framework required by statute. | key 일치; `MA-CDTM-RETAIL-SCOPE`의 current trigger·deadline·scope 확인 |
| `MA-Q-0083` | `KEEP` | `YES` | C: On this record, the agreement cannot authorize retail pharmacist prescribing of Schedule II through V substances.; D: For this scenario, the controlled-substance limitation applies even if the supervising physician signs the agreement.; E: Schedule VI prescribing can be authorized only within the separate statutory retail CDTM limits. | key 일치; `MA-CDTM-CONTROLLED-LIMIT`의 current trigger·deadline·scope 확인 |
| `MA-Q-0084` | `KEEP` | `YES` | B: For this scenario, keep the prescription within the diagnosis and agreement scope.; C: Under these facts, send a copy of the prescription to the supervising physician within 24 hours.; E: In this setting, the pharmacist must document the authorized Schedule VI prescription within the patient-specific collaborative workflow. | key 일치; `MA-CDTM-SVI-RX`의 current trigger·deadline·scope 확인 |
| `MA-Q-0085` | `KEEP` | `YES` | C: Under these facts, use professional judgment to evaluate and resolve the issue before dispensing.; E: In this setting, communicate with the prescriber or patient when needed to resolve the concern. | key 일치; `MA-PRODUR`의 current trigger·deadline·scope 확인 |
| `MA-Q-0086` | `KEEP` | `YES` | A: In this setting, provide the meaningful counseling opportunity required by 247 CMR 9.18.; D: At this stage, use pharmacist judgment and patient-specific information rather than a purely mechanical signature. | key 일치; `MA-COUNSELING`의 current trigger·deadline·scope 확인 |
| `MA-Q-0087` | `KEEP` | `YES` | A: At this stage, determine whether the prescriber validly indicated no substitution.; B: Given the described event, confirm the product is listed as interchangeable under Massachusetts standards.; D: On this record, the substitute must be reasonably available at a lower retail price.; E: For this scenario, a valid prescriber direction against substitution prevents automatic interchange. | key 일치; `MA-INTERCHANGE`의 current trigger·deadline·scope 확인 |
| `MA-Q-0088` | `KEEP` | `YES` | A: Given the described event, accept the returned medication under the error pathway.; C: On this record, quarantine it and arrange proper disposal rather than returning it to saleable inventory.; D: For this scenario, returned erroneous medication must not be restored to saleable inventory.; E: Under these facts, the pharmacy remains responsible for proper disposition after quarantine. | key 일치; `MA-RETURN-QUARANTINE`의 current trigger·deadline·scope 확인 |
| `MA-Q-0089` | `KEEP` | `YES` | A: On this record, immediately notify the patient or representative and provide directions intended to correct the error and minimize harm.; D: For this scenario, immediately notify the prescriber when professional judgment indicates that prescriber notice is warranted.; E: Under these facts, complete the initial quality-related-event documentation within 24 hours after discovery or notification. | key 일치; `MA-QRE-NOTIFY`, `MA-QRE-DOCUMENT-24H`의 current trigger·deadline·scope 확인 |
| `MA-Q-0090` | `KEEP` | `YES` | B: For this scenario, send the Board's required certified written notice at least 14 days before the intended closure date.; C: Under these facts, identify patients served during the preceding 90 days and attempt patient notice at least 14 days before closure.; D: In this setting, handle requested patient-file transfers timely so the closure does not delay therapy.; E: At this stage, within 14 days after closure, submit original credentials and the controlled-substance disposition attestation. | key 일치; `MA-PHARMACY-CLOSURE-NOTICE`, `MA-PHARMACY-CLOSURE-PATIENTS`, `MA-PHARMACY-CLOSURE-CS`의 current trigger·deadline·scope 확인 |

## Authority record

아래 official sources를 2026-08-13에 확인했다. 각 item의 exact source set은 machine-readable audit의 `authorities`에 보존했다.

- [Annual CQI education](https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download) — `247 CMR 15.02(1)(f)`
- [Biennial controlled-substance inventory](https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.11) — `21 CFR 1304.11(c)`
- [Board Policy 2025-02 Definitions](https://www.mass.gov/doc/2025-02-definitions-pdf/download) — `Serious Injury definition, adopted 8/7/2025`
- [Collaborative drug therapy management pharmacist qualifications](https://www.mass.gov/doc/247-cmr-16-collaborative-drug-therapy-management/download) — `247 CMR 16.02(1)`
- [Compounding continuing education](https://www.mass.gov/doc/2021-04-continuing-education-ce-requirements-pdf/download) — `Policy 2021-04, revised 9/4/2025`
- [Continuous quality improvement program](https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download) — `247 CMR 15.02`
- [Controlled Substance Ordering System](https://www.ecfr.gov/current/title-21/chapter-II/part-1311) — `21 CFR 1305 Subpart C; 21 CFR 1311.30, 1311.55, 1311.60`
- [Controlled-substance destruction records](https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.21) — `21 CFR 1304.21(e); 21 CFR 1317.95`
- [Controlled-substance inventory count method](https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.11) — `21 CFR 1304.11(e)(6)`
- [Controlled-substance record retention](https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.04) — `21 CFR 1304.04(a)`
- [DEA Form 222 partial shipments and validity](https://www.ecfr.gov/current/title-21/chapter-II/part-1305/section-1305.13) — `21 CFR 1305.13(b)`
- [DEA Form 222 record maintenance](https://www.ecfr.gov/current/title-21/chapter-II/part-1305/section-1305.17) — `21 CFR 1305.17(a), (c), and (e)`
- [Initial controlled-substance inventory](https://www.ecfr.gov/current/title-21/chapter-II/part-1304/section-1304.11) — `21 CFR 1304.11(b)`
- [Interchangeable drug products](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section12D) — `M.G.L. c. 112, § 12D`
- [Lost or stolen DEA Forms 222](https://www.ecfr.gov/current/title-21/chapter-II/part-1305/section-1305.16) — `21 CFR 1305.16`
- [Non-retrievable controlled-substance destruction](https://www.ecfr.gov/current/title-21/chapter-II/part-1317) — `21 CFR 1317.90 and 1317.95`
- [Patient counseling](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download) — `247 CMR 9.18`
- [Pharmacist collaborative practice agreements](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section24B1~2) — `M.G.L. c. 112, § 24B1/2(b)`
- [Pharmacist continuing education](https://www.mass.gov/doc/247-cmr-4-personal-registration-renewal-continuing-education-requirement/download) — `247 CMR 4.03`
- [Pharmacy intern direct supervision](https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download) — `247 CMR 8.01(2)`
- [Pharmacy internship daily credit cap](https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download) — `247 CMR 8.01(3)`
- [Pharmacy technician and trainee scope](https://www.mass.gov/doc/2020-15-scope-of-practice-pdf/download) — `Policy 2020-15, revised 11/6/2025`
- [Prospective drug utilization review](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download) — `247 CMR 9.17`
- [Quality-related event immediate response](https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download) — `247 CMR 15.03(1)`
- [Quality-related event initial documentation](https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download) — `247 CMR 15.03(2)`
- [Quality-related event systems analysis](https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download) — `247 CMR 15.03(3)`
- [Resident pharmacy closure notice](https://www.mass.gov/doc/247-cmr-6-pharmacy-licensure/download) — `247 CMR 6.13(1)`
- [Resident pharmacy closure patient notice and records transfer](https://www.mass.gov/doc/247-cmr-6-pharmacy-licensure/download) — `247 CMR 6.13(2)-(4)`
- [Resident pharmacy post-closure controlled-substance duties](https://www.mass.gov/doc/247-cmr-6-pharmacy-licensure/download) — `247 CMR 6.13(5) and 6.14`
- [Retail CDTM Schedule II-V prescribing prohibition](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section24B1~2) — `M.G.L. c. 112, § 24B1/2(c)`
- [Retail CDTM Schedule VI prescription duties](https://www.mass.gov/doc/247-cmr-16-collaborative-drug-therapy-management/download) — `247 CMR 16.03(5)(e)`
- [Retail collaborative drug therapy management scope](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section24B1~2) — `M.G.L. c. 112, § 24B1/2(c)`
- [Returned erroneous or defective medication](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download) — `247 CMR 9.01(7)`
- [Reverse-distributor registration and transfer](https://www.ecfr.gov/current/title-21/chapter-II/part-1317) — `21 CFR 1317.05 and 1317.15`
- [Schedule I and II ordering requirements](https://www.ecfr.gov/current/title-21/chapter-II/part-1305/section-1305.03) — `21 CFR 1305.03`
- [Schedule II handling by pharmacy support personnel](https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download) — `247 CMR 8.05`
- [Serious improper-dispensing event report](https://www.mass.gov/doc/247-cmr-20-reporting/download) — `247 CMR 20.02(1)-(3); Policy 2025-02 Serious Injury definition`
- [Serious-event supporting records](https://www.mass.gov/doc/247-cmr-20-reporting/download) — `247 CMR 20.02(4)`
- [Theft and significant loss reporting](https://www.ecfr.gov/current/title-21/chapter-II/part-1301/section-1301.74) — `21 CFR 1301.74(c)`
- [Unaccepted and defective DEA Forms 222](https://www.ecfr.gov/current/title-21/chapter-II/part-1305/section-1305.15) — `21 CFR 1305.15`

## 독립성 및 hash 보존

각 item은 key를 보기 전에 stem·choices만으로 먼저 풀었고, 그 뒤 frozen key와 비교했다. `question_ids`와 `question_hashes`는 supplied `Batch B` input에서 byte-for-byte value copy했고 canonical question/rule/drug files는 수정하지 않았다.
