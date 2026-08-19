# Batch 2 Pre-Authoring Coverage-Gap / Decision-Path Map

Date: 2026-08-14
Base main SHA: `67626815564062bd7f7bfec5b3667ba0deb03454`
Authoring branch: `author/mpje-expansion-batch2`
Planned IDs: `MA-Q-0131` through `MA-Q-0210`

## Scope and method

This map was produced before Batch 2 canonical question files were authored. The full current canonical bank (MA-Q-0001 through MA-Q-0130), current rule/drug records, current question-family map, release/audit governance, and current official Massachusetts/federal authorities were reviewed. Current canonical question files control over stale repair-spec counts.

Semantic duplicate definition used here: **same practical pharmacist decision + same controlling legal fork**, even when the drug, patient, quantity, answer order, or cosmetic setting changes.

## Current-bank saturation findings

### Strong / overrepresented

1. Schedule II no-refill, validity, patient-requested partial fill, stock-short partial fill, and emergency oral follow-up mechanics.
2. Schedule III/IV refill clocks and common controlled-prescription refill questions.
3. Out-of-state controlled-prescription validity and verification.
4. Basic prescription-transfer rules, including one-time unfilled EPCS transfer.
5. Federal DEA inventory basics and two-year record retention.
6. Form 222 / CSOS ordering, defects, loss, power of attorney, certificate validation, cancellation, and recordkeeping.
7. Basic CQI/QRE duties and serious-event reporting.
8. Disposal / reverse-distributor / Form 41 pathways.
9. Baseline counseling, DUR, generic interchange, closure, technician/intern, CE, and CDTM qualifications/scope.
10. Basic pseudoephedrine, naloxone, mifepristone REMS, clozapine REMS removal, Schedule VI classification, and opioid-information duties.

These areas are not excluded categorically, but Batch 2 may use them only when a genuinely different practical fork exists.

## Underrepresented / high-value gaps

### Massachusetts operations and scope

- Automated Dispensing Device (ADD) facility approval, pharmacy ownership of contents, patient-specific order requirement, event records, package integrity, emergency-kit loading, routine-dispensing registration/video requirements.
- Credential-specific ADD stocking: pharmacy technician trainee vs licensed technician vs nationally certified licensed technician.
- Expedited Partner Therapy (EPT): chlamydia-only scope, anonymous partner prescription construction, profile/label workflow, referral when unable/unwilling to fill.
- Pharmacist / pharmacy-intern administration of medications: current Massachusetts statutory categories and mental-health/SUD product-specific administration pathway.
- Long-term-care emergency-kit limits, single-dose/tamper-evident packaging, Schedule VI handling, and ADD substitution.
- Inpatient hospice acute-use medication supply, bed-capacity limits, ADD security, pharmacy ownership/reconciliation.
- Compliance packaging: current allowance for Schedule II/III **maintenance** medications, with maintenance status—not schedule alone—as the controlling fork.
- Prescriber registration interaction: Massachusetts MCSR vs DEA requirements for Schedule II-V compared with Schedule VI.

### Federal controlled-substance special settings

- Schedule II fax-as-original exceptions for LTCF residents, hospice narcotics, and qualifying narcotic compounded parenteral/infusion preparations.
- Multiple Schedule II prescriptions totaling up to a 90-day supply, including earliest-fill instructions without postdating.
- Schedule II partial filling for LTCF residents / terminally ill patients and the 60-day framework.
- Corresponding responsibility and legitimate-medical-purpose review as a pharmacist action, rather than passive acceptance of a prescription.
- Methadone OUD vs pain: OTP pathway, non-OTP emergency dispensing limits, and distinction from buprenorphine pathways.

### Drug-triggered gaps

- Drug + indication changes the legal pathway (testosterone gender-affirming administration; methadone pain vs OUD).
- Product-specific pharmacist administration for listed LAI antipsychotics and extended-release naltrexone.
- Schedule/PMP status changes ADD stocking authority (especially gabapentin as Schedule VI but PMP-reportable).
- C-II drug + setting changes fax-as-original and LTCF/terminal partial-fill consequences.
- Real-drug matrices for Massachusetts MCSR/DEA consequences.
- Current iPLEDGE pharmacy certification/authorization pathway without prematurely applying the delayed November 15, 2026 modifications.
- Mixed restricted-distribution/REMS recognition using current products rather than a single-obvious-product flashcard.

## Full-bank duplicate boundaries carried forward

Batch 2 must not recreate these existing practical forks by changing only a drug or patient:

- Q0001-Q0050: common schedule/refill/partial/transfer/quantity/MassPAT matrices already cover the ordinary controlled-prescription mechanics.
- Q0051-Q0074: CQI, serious-event, inventory, Form 222/CSOS, destruction, and closure basics are already occupied.
- Q0075-Q0090: technician/intern baseline scope, CE, CDTM, counseling/DUR/interchange, return quarantine, QRE, closure are already occupied.
- Q0091 recall lot action.
- Q0092 counseling vs Medication Guide.
- Q0093 storage excursion -> adulteration decision.
- Q0094 stock-short C-II 72-hour remainder.
- Q0095-Q0096 hormonal-contraception pharmacist prescribing.
- Q0097-Q0098 naloxone third-party / OTC-vs-Rx status.
- Q0099 CIII-V partial filling.
- Q0100 PDMA samples.
- Q0101 lesser C-II quantity.
- Q0102 controlled-stock security.
- Q0103 14-day licensee change reporting.
- Q0104 emergency C-II missing follow-up.
- Q0105 CSOS credential sharing.
- Q0106 mifepristone REMS certified pathway.
- Q0107-Q0108 pseudoephedrine ID/log/self-certification.
- Q0109 clozapine REMS removal.
- Q0110-Q0112 opioid antagonist/pamphlet/lockbox duties.
- Q0113 lesser cash price.
- Q0114 hypodermic authorized-seller scope.
- Q0115 serious-event vs QRE deadlines.
- Q0116 oral Schedule VI documentation.
- Q0117 outpatient compounded sterile label/contact information.
- Q0118 prescription required elements.
- Q0119 controlled-prescription retention vs refill clock.
- Q0120 Schedule VI transfer + certified-technician authority.
- Q0121 excepted preparation retail controls.
- Q0122 Schedule VI vs federal schedule / gabapentin distinction.
- Q0123 pharmacist need not verify e-prescribing exception/waiver.
- Q0124 out-of-state oral III-V follow-up.
- Q0125-Q0129 Form 222 defects/loss/POA/CSOS/cancellation.
- Q0130 reverse distribution + non-retrievable destruction + Form 41.

## Batch 2 architecture

- Part A Core: MA-Q-0131 through MA-Q-0170 (40 items).
- Part B Drug-Triggered: MA-Q-0171 through MA-Q-0210 (40 items).
- New items start as `AUDIT_PENDING`, `development_fixture: true`, and remain excluded from public preview.
- Core uses SBA/SATA according to the natural decision task; no arbitrary quota.
- Drug 40 target: 30 SATA / 10 SBA, mostly five-option SATA with 2-4 independently correct selections.
- Drug 40 target difficulty: D3=12, D4=20, D5=8.
- One independently fresh session must later perform both LEGAL_VERIFICATION and REALISM_REVIEW, stored as separate audit artifacts.
- Initial audit batch maximum is 40 questions, so Batch 2 will be frozen into two 40-question audit packages per review type.

## Current-official authority set for new pathways

Massachusetts authority is limited to current Mass.gov / Massachusetts Legislature / promulgated CMR material. Federal authority is limited to current eCFR / DEA / FDA official material. Key new source families include:

- Massachusetts Board/DCP Policy 2019-02 Automated Dispensing Device Use.
- Massachusetts Board/DCP/BHCSQ Policy 2023-08 Pharmacy Technician Stocking of ADDs.
- Massachusetts Board/DCP Policy 2020-08 Expedited Partner Therapy Prescriptions.
- Current Massachusetts Pharmacist Administration of Medications guidance and M.G.L. c. 94C administration authority.
- DHCQ 18-6-679 LTCF emergency kits.
- DHCQ 20-3-700 inpatient hospice acute-use medications.
- Policy 2023-01 Compliance Packaging and Reusable Dose Planners.
- Current Massachusetts MCSR / controlled-substance registration requirements.
- 21 CFR 1306.04, 1306.07, 1306.11, 1306.12, and 1306.13.
- FDA current iPLEDGE REMS material; February 2026 modifications are not treated as implemented before the announced November 15, 2026 implementation date.

## Pre-authoring release gate

No Batch 2 question may be released merely because it is schema-valid. Before freezing, each item must pass:

1. current-source legal verification by the authoring session,
2. full-bank semantic duplicate review,
3. structural-pattern / answer-leakage checks,
4. smart-guess resistance review,
5. generated-artifact freshness,
6. repository automated QA/tests.

Final release still requires a genuinely fresh independent Legal + Realism audit on the exact frozen current question hashes.
