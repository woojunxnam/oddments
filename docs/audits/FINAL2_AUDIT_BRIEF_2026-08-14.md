# Expansion Batch 1 final-two audit status

Target questions: `MA-Q-0098`, `MA-Q-0110`.

Repair branch: `repair/mpje-expansion-batch1-final2`.

## Issue #31 independent audit

Issue #31 was completed by fresh auditor instance `GPT-FRESH-EXP1-FINAL2-A` against frozen SHA `6793e3d5a021c20e267c428bcb73ac14f4f6e1c4`.

Canonical audit records:

- `AUDIT-GPT-FRESH-EXP1-FINAL2-A-LEGAL-REAUDIT-2026-08-14`
- `AUDIT-GPT-FRESH-EXP1-FINAL2-A-REALISM-REAUDIT-2026-08-14`

The audit artifacts were merged from PR #32 into this repair branch without modifying canonical question content.

## MA-Q-0098

Frozen/current audit hash: `f33699bb74bd94e73106cb7569deb883de424d4c61538ff3f65c8afc71ec4ecc`.

- Legal: `KEEP`; existing answer `YES`.
- Realism: `KEEP / PASS`.
- Full-bank distinctness: confirmed distinct from `MA-Q-0097`; Q0097 tests third-party/standing-order access, while Q0098 tests OTC-versus-prescription naloxone product/package classification and retail handling.
- Final editor adjudication: `KEEP`.
- Current lifecycle/verification status on this branch: `RELEASED`.

Q0098 has been added to the public preview allowlist after current-hash audit verification and full QA.

## MA-Q-0110

Frozen/current audited version hash: `43cb9fde607a509f022b964ee16c0d73208c4f749d98ac90619b84a125b955a2`.

- Legal: `KEEP`; existing answer `YES`.
- Realism: `MAJOR_REWRITE / FAIL` (Medium).
- Failure reason: near-duplicate pharmacist decision path with released `MA-Q-0111`. Both reduce to identifying a Schedule II/III dispensing, recognizing an enumerated `M.G.L. c.94C §21` pamphlet exception, and concluding that the pamphlet is not required. Substituting morphine/palliative care for buprenorphine-naloxone/OUD does not create a sufficiently distinct decision path.
- Current lifecycle/verification status: `AUDIT_PENDING`.
- Final adjudication: none.
- Public preview: excluded.

Any future Q0110 repair must use a materially different jurisprudence decision path rather than another `§21` pamphlet-exception variant.

## Current release boundary

After Q0098 admission on this branch:

- public preview: **86 questions**
- Expansion Batch 1 released: **39 / 40**
- `MA-Q-0098`: released and included
- `MA-Q-0110`: quarantined and excluded

The Q0098 admission workflow validated the current Issue #31 audit hashes/results, regenerated artifacts, ran `validate_all.py`, ran the full pytest suite, and proved deterministic generated state before committing the admission.
