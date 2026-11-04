# GPT Expansion Batch 1 — LEGAL_VERIFICATION Report

- Audit date: 2026-08-14
- Frozen target: `feature/mpje-expansion-batch1 @ 6403868ee78d40fb0ba801d01293c64a41e57828`
- Scope: `MA-Q-0091..MA-Q-0130` (40 questions)
- Audit scope: `INITIAL_BATCH`
- Status: `FULLY_ADJUDICATED`
- Canonical question edits: none

## Result

| Metric | Count |
|---|---:|
| KEEP | 36 |
| MINOR_EDIT | 1 |
| MAJOR_REWRITE | 3 |
| DELETE | 0 |
| Existing answer YES | 37 |
| Existing answer PARTIALLY | 2 |
| Existing answer NO | 1 |

## Material findings

### MA-Q-0105 — MAJOR_REWRITE / PARTIALLY
The stem says only “a technician.” Current 247 CMR 8.05 distinguishes an ordinary pharmacy technician, who may assist with transporting Schedule II substances, from a certified pharmacy technician, who may assist with transporting and handling them under pharmacist approval/supervision and written policy. The keyed E is a generally true abstraction but does not resolve whether the person in the stem may handle the stock bottle. Specify the licensure category.

### MA-Q-0115 — MINOR_EDIT / YES
The seven-business-day deadline is correct, but the answer/explanation merges two different 247 CMR 20.02 triggers. Improper dispensing causing serious injury/death is reported within seven business days of discovery of that serious injury/death; the “knowledge by any pharmacy employee” trigger belongs to the separate serious-adverse-drug-event pathway.

### MA-Q-0120 — MAJOR_REWRITE / NO
The item and canonical `MA-RX-TRANSFER` summary rely on obsolete transfer mechanics. Current 247 CMR 9.14 (effective 2024-12-06) requires timely transfer on patient/agent request, permits the pharmacy to act as patient agent, prohibits a transfer fee, and provides specific Schedule VI rules. It no longer states the keyed pharmacist-to-pharmacist communication and transfer-annotation requirements. Current 247 CMR 8.04 also permits certified technicians, with pharmacist approval, to perform Schedule VI transfers. This is a canonical dependency freshness defect, not merely a distractor issue.

### MA-Q-0123 — MAJOR_REWRITE / PARTIALLY
The general e-prescribing rule and existence of exceptions/waivers are correct, but keyed choice C and the explanation imply that a pharmacist must investigate or verify the prescriber’s exception/waiver. 105 CMR 721.070(C), as explained by DCP 19-12-108, expressly states that a pharmacist receiving an otherwise valid written or oral prescription is not required to verify that the prescription properly falls under an e-prescribing exception or waiver. The pharmacist-facing no-verification rule is also missing from the canonical dependency summary.

## Ambiguity

- `MA-Q-0105` — personnel category is implementation-critical to the legal answer.

## Drug / authority / dependency findings

- No material drug identity, indication, federal schedule, or Massachusetts-status error was found in the other items.
- `MA-RX-TRANSFER` is stale against current 247 CMR 9.14 and requires canonical repair before Q0120 can be re-authored.
- `MA-CONTROLLED-EPRESCRIBE` is incomplete for a pharmacist-facing validity question because it omits 105 CMR 721.070(C)’s no-verification rule.
- Q0115’s explanation should keep 247 CMR 20.02(1) and (2) triggers separate.

## Official-source method

Every question was independently solved against current official primary/official sources as applicable: current MGL, promulgated Massachusetts CMR, DCP/Board official materials, eCFR, DEA, and FDA. Existing keyed answers and canonical rule summaries were treated as claims to verify, not as authority.

## Legal quarantine IDs

`MA-Q-0105`, `MA-Q-0115`, `MA-Q-0120`, `MA-Q-0123`

These four must remain quarantined until repaired and re-audited on their new hashes.
