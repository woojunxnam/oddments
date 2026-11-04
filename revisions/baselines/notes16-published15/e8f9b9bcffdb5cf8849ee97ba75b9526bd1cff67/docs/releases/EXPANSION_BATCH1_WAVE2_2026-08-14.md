# Expansion Batch 1 — Wave 2 admission (2026-08-14)

This record documents the guarded Wave 2 admission from Expansion Batch 1.

## Independent audit evidence

Issue #27 was completed by fresh independent auditor instance `GPT-FRESH-EXP1-V3-A` on the frozen v3 question hashes.

- Legal verification: 29 KEEP, 29 existing answers YES.
- Realism review: 27 PASS/KEEP, 2 FAIL/MAJOR_REWRITE.
- Realism failures: `MA-Q-0098`, `MA-Q-0110`.
- No legal quarantine, wrong-answer finding, drug-fact problem, or stale dependency finding was reported.

Canonical completed audits:

- `AUDIT-GPT-FRESH-EXP1-V3-A-LEGAL-REAUDIT-2026-08-14`
- `AUDIT-GPT-FRESH-EXP1-V3-A-REALISM-REAUDIT-2026-08-14`

## Admission decision

Wave 2 admits only the 27 questions that received both current-hash legal `KEEP/YES` and realism `KEEP/PASS`.

`MA-Q-0098` and `MA-Q-0110` remain `AUDIT_PENDING` and are excluded from the public preview pending semantic repair and a new current-hash independent audit.

After Wave 2:

- Batch 1 formally RELEASED: 38 of 40.
- Public preview allowlist: 85 questions.
- Quarantined Batch 1 questions: 2.

## Validation

Guarded admission workflow `31839456211` verified audit scope and hashes before mutation, admitted only the 27 passing questions, verified the 85-question preview boundary, committed the admission, regenerated tracked artifacts deterministically, and completed successfully.
