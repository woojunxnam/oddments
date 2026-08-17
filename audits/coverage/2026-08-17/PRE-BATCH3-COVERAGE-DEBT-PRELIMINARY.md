# Pre-Batch3 Full Competency Coverage-Debt Audit — Preliminary

Status: **PRELIMINARY FAIL / FINAL GATE BLOCKED BY ISSUE #39**

This document is analysis only. It does not release, merge, reclassify, or author any canonical question. The final coverage gate must be rerun from the final post-Batch2 release-governance SHA after the fresh independent Impact14 re-audit in Issue #39 passes.

## Source snapshot

- Repaired Batch 2 canonical candidate: `1c85163367a82c06061f3d5be3f7d05c3748bca2`
- Current pre-2027 Massachusetts MPJE blueprint: `MPJE-MA-PRE2027-BLUEPRINT`
- Canonical questions inspected: `MA-Q-0001` through `MA-Q-0210` (210 total)
- Current release-usable questions at this snapshot: 40
- Batch 2 candidate questions: 80 (`MA-Q-0131` through `MA-Q-0210`)

## Gate model

The current NABP competency statements are treated as 46 atomic checks rather than allowing a broad Area 1–4 label to prove coverage. The final gate must distinguish:

1. **Canonical semantic coverage** — a question directly tests the competency, not merely mentions a keyword.
2. **Audit maturity** — the supporting question has passed the required current-hash legal and realism review and final adjudication.
3. **Taxonomy correctness** — the question is mapped to the competency/area it actually tests.
4. **Pool capacity** — the released pool can assemble a 120-question blueprint-faithful mock without reusing questions.

Keyword scans are only candidate discovery; they cannot establish PASS.

## Quantitative findings

### Canonical area distribution

| Area | Canonical count | 210-question weighted reference |
|---|---:|---:|
| 1 | 23 | 46.2 |
| 2 | 38 | 69.3 |
| 3 | 96 | 50.4 |
| 4 | 53 | 44.1 |

The pool is strongly concentrated in Area 3. Pool proportions do not need to mirror exam weights exactly, but an area must contain enough unique questions to assemble a blueprint-faithful mock.

### One 120-question mock capacity

Largest-remainder allocation from the repository blueprint is:

- Area 1: 26
- Area 2: 40
- Area 3: 29
- Area 4: 25

Current canonical pool deficits for one no-reuse mock:

- Area 1: **3 short**
- Area 2: **2 short**
- Area 3: 0 short
- Area 4: 0 short

Current release-usable pool is only 40 questions, distributed 5 / 7 / 25 / 3 across Areas 1–4.

### Projection after a clean Batch 2 release

If, and only if, all 80 Batch 2 questions pass Issue #39 and release governance without further canonical changes, projected release-usable counts become:

- Area 1: 17
- Area 2: 22
- Area 3: 55
- Area 4: 26
- Total: 120

That projected pool still **cannot** build one blueprint-faithful 120-question mock without reuse:

- Area 1 remains **9 short**
- Area 2 remains **18 short**

Therefore a clean Batch 2 release by itself does not clear the pre-Batch3 coverage gate.

## Semantic competency debt found in the preliminary review

### Direct gaps / no adequate semantic evidence identified

The following require direct remediation unless a later manual review identifies a valid existing question:

- **1.2b — Personnel disciplinary classifications/processes.** Automated hit `MA-Q-0128` is a false positive: it concerns revocation of a CSOS digital certificate, not discipline of pharmacy personnel.
- **1.2c — Impairment/inability-to-practice reporting or participation programs.** No candidate found in the full 210-question scan.
- **2.3b — Documentation of counseling/offer to counsel.** `MA-Q-0092` distinguishes Medication Guide distribution from counseling; it does not directly test documenting counseling or the offer.
- **4.2c — Hazardous-drug training, possession, handling, storage, and disposal.** No candidate found.
- **4.5a — Substantive sterile-compounding law.** Existing `MA-Q-0080` tests compounding CE and `MA-Q-0117` tests compounded-product labeling; these are peripheral to substantive sterile-compounding practice requirements.
- **4.5b — Substantive nonsterile-compounding law.** Same limitation as above.
- **4.5c — Hazardous compounding.** No candidate found.
- **4.5d — Non-hazardous compounding.** No candidate found.
- **4.6 — Centralized prescription processing / central fill.** No candidate found.
- **4.7c — Practice-setting inspection requirements.** `MA-Q-0062` is a false positive because it tests controlled-substance record retention and availability for inspection, not pharmacy-facility inspection requirements.
- **4.7d — Practice-setting disciplinary actions.** No candidate found.

### Covered or plausible but taxonomy/maturity debt exists

- **3.3a prospective DUR:** `MA-Q-0085` directly tests prospective review but is currently Area 2 and `AUDIT_PENDING`; NABP places prospective DUR in Area 3.3.
- **2.4 return/reuse:** `MA-Q-0088` directly tests a returned medication, quarantine, and prohibition on return to saleable stock, but is currently Area 4 and `AUDIT_PENDING`; NABP places return/reuse in Area 2.4.
- **4.4 product selection:** `MA-Q-0087` directly tests Massachusetts generic interchange but is currently Area 3 and `AUDIT_PENDING`; NABP places product selection in Area 4.4.
- **3.8b nonprescription labeling:** `MA-Q-0098` gives useful direct/partial evidence through FDA OTC naloxone Drug Facts versus prescription labeling and is already released.
- **3.6 packaging:** Batch 2 compliance-packaging questions provide evidence for packaging restrictions, but coverage is concentrated in a special compliance-packaging context and should be expanded or explicitly adjudicated as sufficient before PASS.
- **2.3a counseling:** only a thin number of direct scenarios exist; depth should be strengthened even if the atomic competency is technically represented.

## Required final PASS criteria

The final gate should not pass unless all of the following are true on the final post-release snapshot:

1. **0 atomic semantic gaps** across the 46-check matrix.
2. Every atomic competency has at least **one direct, current-law, independently audited/release-usable** supporting question. Peripheral mentions do not count.
3. Each NABP headline competency has sufficient scenario diversity; default expectation is at least **two distinct families**, unless a documented adjudication explains why a narrow competency reasonably requires only one.
4. Known taxonomy mismatches are corrected or formally mapped so coverage reports use the competency actually tested rather than the legacy area tag.
5. At least **one 120-question blueprint-faithful mock** can be assembled from release-usable questions without reuse, requiring at minimum 26 / 40 / 29 / 25 usable questions in Areas 1–4 under the current repository blueprint.
6. All evidence is frozen to an exact SHA; the competency matrix, supporting question IDs, question hashes, and dependency hashes are reproducible.
7. Repository QA/tests and generated-artifact freshness checks pass.

## Remediation order if the final gate fails

Do **not** call the next work Batch 3. Use a separate pre-Batch3 coverage-remediation tranche.

1. **Legacy salvage first:** review `MA-Q-0001` through `MA-Q-0090`, especially Area 1/2 and zero/thin competencies. Reclassify/migrate only where semantic review and current law support it; do not assume pending legacy content is correct.
2. Freeze and independently legal/realism audit any legacy questions proposed for admission.
3. Recompute the 46-check matrix and mock capacity.
4. **Targeted authoring only for residual gaps/capacity deficits** that cannot be filled by sound legacy content.
5. Freeze → independent legal + realism audit → adjudication/repair → re-freeze/re-audit → release governance for that remediation tranche.
6. Rerun this full coverage gate. Only a PASS unlocks Batch 3.

## Locked status now

- Issue #39 fresh re-audit: pending.
- Batch 2 release governance: blocked pending #39.
- Final competency coverage-debt gate: blocked pending final post-Batch2 release snapshot.
- Coverage remediation authoring: not started.
- Batch 3 authoring: blocked.
- Merge/public preview/release changes from this analysis branch: prohibited.
