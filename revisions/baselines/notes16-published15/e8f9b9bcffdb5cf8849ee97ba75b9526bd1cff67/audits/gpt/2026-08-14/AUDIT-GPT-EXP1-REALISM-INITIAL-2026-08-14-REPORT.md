# GPT Expansion Batch 1 — REALISM_REVIEW Report

- Audit date: 2026-08-14
- Frozen target: `feature/mpje-expansion-batch1 @ 6403868ee78d40fb0ba801d01293c64a41e57828`
- Scope: `MA-Q-0091..MA-Q-0130` (40 questions)
- Style profile: `MPJE-MA-PRE2027` v1 / `293be8fdcd39af2255a22a0423b7123d5cfcf7c0e6c561872eb0ef04e745015c`
- Audit scope: `INITIAL_BATCH`
- Status: `FULLY_ADJUDICATED`
- Canonical question edits: none

## Result

| Metric | Count |
|---|---:|
| PASS | 21 |
| FAIL | 19 |
| KEEP | 21 |
| MINOR_EDIT | 13 |
| MAJOR_REWRITE | 6 |
| DELETE | 0 |

## Bank-level findings

Batch 1 is materially better than the earlier Phase 2 template-heavy bank: many items now use genuine pharmacy encounters, federal/state distinctions, role/scope questions, and multi-step legal triggers. However, 19 items still fail the strict style contract.

The recurring failure modes are:

1. **Requirement-list SATA rather than applied decision making** — especially Q0094, Q0099, Q0110, Q0113.
2. **Direct numeric/deadline retention recall** — Q0107, Q0111, Q0114, Q0116, Q0119, Q0125, Q0126.
3. **Weak or obviously absurd distractors / answer-length leakage** — especially Q0108, Q0118, Q0129.
4. **Schedule/form flashcard behavior** — Q0122, Q0126, Q0128.
5. **Legal instability undermining realism** — Q0105, Q0120, Q0123.

## PASS IDs

MA-Q-0091, MA-Q-0092, MA-Q-0093, MA-Q-0095, MA-Q-0096, MA-Q-0097, MA-Q-0098, MA-Q-0100, MA-Q-0101, MA-Q-0102, MA-Q-0103, MA-Q-0104, MA-Q-0106, MA-Q-0109, MA-Q-0112, MA-Q-0115, MA-Q-0117, MA-Q-0121, MA-Q-0124, MA-Q-0127, MA-Q-0130

## FAIL IDs

MA-Q-0094, MA-Q-0099, MA-Q-0105, MA-Q-0107, MA-Q-0108, MA-Q-0110, MA-Q-0111, MA-Q-0113, MA-Q-0114, MA-Q-0116, MA-Q-0118, MA-Q-0119, MA-Q-0120, MA-Q-0122, MA-Q-0123, MA-Q-0125, MA-Q-0126, MA-Q-0128, MA-Q-0129

### MAJOR_REWRITE
MA-Q-0099, MA-Q-0105, MA-Q-0120, MA-Q-0122, MA-Q-0123, MA-Q-0126

### MINOR_EDIT
MA-Q-0094, MA-Q-0107, MA-Q-0108, MA-Q-0110, MA-Q-0111, MA-Q-0113, MA-Q-0114, MA-Q-0116, MA-Q-0118, MA-Q-0119, MA-Q-0125, MA-Q-0128, MA-Q-0129

## Highest-value examples to preserve as design references

- `MA-Q-0112`: immediate QRE response separates patient notification, corrective directions, and professionally indicated prescriber notification.
- `MA-Q-0117`: returned insulin scenario distinguishes acceptance, quarantine, and disposition.
- `MA-Q-0121`: pregabalin requires schedule classification plus the Massachusetts out-of-state pathway and verification rule.
- `MA-Q-0124`: alprazolam requires schedule classification, an out-of-state oral pathway, and the correct follow-up-record rule.
- `MA-Q-0127`: inventory counting uses both schedule and container-size threshold.
- `MA-Q-0130`: expired oxycodone requires reverse-distribution vs destruction, non-retrievable standard, and Form 41 distinction.

## Batch 2 authoring implications

- Do not treat a new legal fact as a new question family if the item is merely a number/form/schedule flashcard.
- For difficulty 5, require an actual multi-step scenario rather than a list of four statutory requirements.
- Use plausible competing legal rules as distractors, not obviously irrelevant administrative or personal-preference options.
- A drug should materially change the legal path; otherwise remove it.
- Reuse the Q0112/Q0117/Q0121/Q0124/Q0127/Q0130 decision architecture, not their wording.

## Combined GPT quarantine

The union of non-KEEP legal findings and realism failures is:

MA-Q-0094, MA-Q-0099, MA-Q-0105, MA-Q-0107, MA-Q-0108, MA-Q-0110, MA-Q-0111, MA-Q-0113, MA-Q-0114, MA-Q-0115, MA-Q-0116, MA-Q-0118, MA-Q-0119, MA-Q-0120, MA-Q-0122, MA-Q-0123, MA-Q-0125, MA-Q-0126, MA-Q-0128, MA-Q-0129

These 20 IDs should remain out of any preview/release admission until repaired where necessary and re-audited on current hashes. GPT audit alone does not satisfy the repository’s separate Claude legal-audit gate.
