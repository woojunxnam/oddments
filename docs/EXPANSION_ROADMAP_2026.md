# Massachusetts MPJE Expansion Roadmap — 2026

## Purpose

Expand the canonical Massachusetts MPJE bank from 90 to approximately 210 candidate questions in three 40-question expansion batches while preserving source-first authoring, distinct reasoning families, current-law dependencies, and fail-closed audit/release gates.

This roadmap plans all three batches now, but authoring and audit proceed one batch at a time so findings from each batch can improve the next one.

## Global rules for all expansion batches

- Every item must be original and must not reproduce recalled, confidential, commercial, Pre-MPJE, or protected exam content.
- Author from a verified canonical rule/drug dependency, not from memory or a practice-question template.
- Prefer one distinct legal reasoning target per new item. A drug-name substitution alone does not create a new family.
- Difficulty target remains 3–5 only; difficulty should come from legal reasoning, exceptions, jurisdiction, timing, or scope rather than trivia.
- Maintain approximately 60–65% SBA, 30–35% SATA, and no more than 5% ordered response. Ordered response is used only when current authority establishes a unique sequence.
- Drug-integrated items should use a clinically plausible drug context and verify generic/brand/indication/schedule/status when material.
- Do not test a HOLD, DRAFT, superseded, or unclear rule.
- New questions remain `AUDIT_PENDING` until independent audit/adjudication requirements are satisfied.
- New items are not added to the public preview merely because automated QA passes.

---

## Expansion Batch 1 — MA-Q-0091..MA-Q-0130

**Status:** authored on `feature/mpje-expansion-batch1`; automated QA passed. Independent INITIAL_BATCH audit remains required.

### Primary objective

Fill high-value gaps that already have stable verified canonical authority, especially pharmacist practice scope, personnel, CQI/reporting, prescription mechanics, controlled-substance operations, and federal inventory/disposal duties.

### Coverage groups

| Group | IDs | Core reasoning targets |
|---|---:|---|
| Counseling / patient information | Q0091–Q0092 | MA counseling offer; federal Medication Guide vs pharmacist counseling duty |
| Interchange | Q0093–Q0094 | default interchange; valid no-substitution/exception logic |
| Pharmacist prescribing | Q0095–Q0098 | hormonal contraception scope/protocol; naloxone third-party/access pathway |
| CDTM | Q0099–Q0102 | qualifications; retail scope; Schedule VI prescribing/documentation; Schedule II–V boundary |
| Personnel | Q0103–Q0107 | technician judgment boundary; technician CII handling; intern supervision; 12-hour internship-credit limit |
| Continuing education | Q0108–Q0109 | annual pharmacist CE distribution; additional compounding CE trigger |
| CQI / QRE | Q0110–Q0114 | CQI program; 24-hour documentation; immediate response; systems analysis; annual education |
| Serious events | Q0115–Q0116 | reporting clock; record retention |
| Product/Rx operations | Q0117–Q0124 | quarantine; Rx required elements; record retention; transfer; out-of-state III–VI; MA Schedule VI; e-prescribing; oral III–V follow-up |
| Federal controlled-substance operations | Q0125–Q0130 | initial/biennial inventory; exact vs estimated count; Form 222/CSOS; Form 222 records; reverse distributor; non-retrievable destruction/Form 41 |

### Batch 1 source exclusions

The batch intentionally does **not** test unresolved HOLD topics such as draft/unclear USP <795>/<797>/<800> implementation, remote/central processing, or LTCF/hospice emergency-kit rules. It also avoids using the stale MassPAT Guide 5.1 dependency until the canonical reporting rule is deliberately migrated to the current source version.

---

## Expansion Batch 2 — planned MA-Q-0131..MA-Q-0170

**Author only after Batch 1 audit findings are reviewed.**

### Primary objective

Increase drug-integrated applied reasoning and Massachusetts-vs-federal interaction without repeating the Batch 1 families.

### Planned allocation

| Planned family group | Target count | Examples of distinct reasoning targets |
|---|---:|---|
| Schedule II lifecycle | 8 | emergency oral issuance/follow-up; shortage partial fill; patient-request partial fill; remainder deadlines; no refills; MA issue-date limits; out-of-state CII distinctions; multiple-prescription/future-fill concepts where current authority supports them |
| Schedule III–V lifecycle | 6 | federal/MA refill limits; transfer rules; oral authorization/follow-up; out-of-state verification; schedule-specific record consequences |
| Opioid / OUD pathways | 5 | initial outpatient opioid limits; statutory exceptions; OUD treatment distinctions; quantity-policy exceptions; product/indication context |
| Massachusetts Schedule VI practice | 5 | validity, refill/transfer, practitioner authorization, state-vs-federal classification, special drug exceptions where current authority is explicit |
| MassPAT / reporting | 4 | only after canonical source migration to the current Massachusetts reporting guide; distinguish reporting status from federal schedule and from query requirements |
| Drug interchange / product substitution | 4 | generic/interchangeable product decisions, prescriber direction, price/availability, biologic/interchangeability only if exact current MA authority is verified |
| Pharmacist services | 4 | vaccination, naloxone, contraception, CDTM or other pharmacist-authorized services using nonduplicative scope/eligibility/documentation scenarios |
| Mixed federal/MA applied cases | 4 | choose the controlling stricter/applicable rule when jurisdiction, schedule, timing, and documentation interact |

### Batch 2 design constraint

At least half of the items should contain a real drug context, but the drug must change the legal analysis rather than serve as decoration. Avoid making the answer recoverable from the drug schedule alone when the intended skill is a multi-rule interaction.

---

## Expansion Batch 3 — planned MA-Q-0171..MA-Q-0210

**Author only after Batch 2 audit findings are reviewed.**

### Primary objective

Fill remaining blueprint/operations gaps and add harder multi-step jurisprudence scenarios while keeping each family distinct from the first 170 questions.

### Planned allocation

| Planned family group | Target count | Examples of distinct reasoning targets |
|---|---:|---|
| Pharmacy licensure / operations | 8 | pharmacy permits, manager-of-record duties, pharmacy area/security, temporary pharmacist absence, closure/records/stock duties, hours/coverage rules, change-of-ownership/location only where current authority is explicit |
| Controlled-substance security / records | 7 | theft/loss timelines, DEA vs MA reporting, inventories, ordering/receiving, destruction, record segregation/retrievability, practitioner/pharmacy registration interactions |
| CQI / error / serious-event synthesis | 5 | distinguish QRE documentation, notification, analysis, annual education, serious-event reporting, and retention without forcing unsupported total chronology |
| Personnel / delegation | 5 | pharmacist, intern, certified technician, technician trainee, supervision, judgment vs nondiscretionary tasks, work-hour limits |
| Patient protection / dispensing standards | 5 | counseling, labeling, packaging/PPPA where verified, prospective review, return/reuse/quarantine, substitution communication/documentation |
| Needles/syringes and other MA-specific public-health rules | 3 | only from current promulgated/official sources and only if the exact pharmacy-practice consequence is verified |
| Facility-specific / special settings | up to 4 | LTCF, hospice, emergency kit, central fill/processing only after existing HOLD dependencies are resolved; otherwise reallocate to verified topics |
| Compounding / USP implementation | up to 3 | include only if Massachusetts current promulgated authority and incorporated USP requirements are fully verified; draft rules remain excluded |

### Batch 3 hard-item target

Use more difficulty-5 items here, but require explicit multi-step reasoning such as jurisdiction → role/schedule classification → trigger/exception → timing/documentation consequence. Do not create difficulty merely by hiding obscure numbers.

---

## Batch promotion workflow

```text
Coverage/family plan
  -> current official source verification
  -> canonical rule/drug dependency check
  -> 40 original AUDIT_PENDING questions
  -> automated schema/duplicate/pattern/answer-distribution QA
  -> INITIAL_BATCH audit package (30–40; here 40)
  -> independent GPT legal + realism audit
  -> independent Claude legal audit
  -> adjudicate findings
  -> semantic fixes only to failed/edited items
  -> targeted current-hash REAUDIT for changed items
  -> final KEEP adjudication
  -> RELEASED if every machine gate passes
  -> main merge / site regeneration
```

For development preview admission, use an explicit allowlist and never expose an item with a current legal/realism failure. Preview status is not equivalent to formal `RELEASED` status.

## Stop conditions

Pause a batch rather than forcing quota completion when:

- a required authority is draft, superseded, unavailable, or materially ambiguous;
- a new question would duplicate an existing reasoning family without a genuinely different trigger/exception/consequence;
- a drug scenario is clinically implausible or adds no legal reasoning value;
- structural QA identifies answer-length leakage, predictable SATA key concentration, repeated templates, or near-duplicate stems;
- an audit finds more than one defensible answer.
