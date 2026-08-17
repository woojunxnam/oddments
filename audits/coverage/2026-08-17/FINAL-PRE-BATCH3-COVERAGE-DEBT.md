# Final Pre-Batch3 Competency Coverage-Debt Gate

- Exact post-Batch2 source SHA: `beeb96d71768b9fb275bdb0005d9cd012e0d1328`
- Verdict: **FAIL — Batch 3 remains blocked**
- Atomic competency result: **28/46 PASS; 18/46 FAIL**
- Failed atoms: 1.2b, 1.2c, 2.1e, 2.3b, 2.4, 3.3a, 4.2c, 4.2e, 4.3, 4.4, 4.5a, 4.5b, 4.5c, 4.5d, 4.6, 4.7b, 4.7c, 4.7d
- Release-usable Area counts: 17/22/55/26
- Required 120-question Area allocation: 26/40/29/25
- Capacity deficits: 9/18/0/0

## Why the gate fails

The bank now contains 120 released questions, but question count alone is insufficient. Area 1 and Area 2 remain below the blueprint allocation, and 18 atomic competencies still lack a direct current-law, independently audited, release-usable question.

## Failed atomic competencies

- **1.2b — Personnel disciplinary classifications/processes**: FAIL_NO_DIRECT_QUESTION. No canonical question directly tests classifications/processes of discipline against an individual pharmacist/technician. Keyword hits such as a revoked CSOS certificate are not personnel discipline.
- **1.2c — Impairment/inability-to-practice reporting or participation programs**: FAIL_NO_DIRECT_QUESTION. No canonical question directly tests reporting/participation in the current impairment/recovery framework (URAMP).
- **2.1e — Practitioner refill-authorization limits**: FAIL_NOT_RELEASE_USABLE. Direct legacy questions test the federal refill-count ceiling, but they are AUDIT_PENDING and therefore cannot satisfy the release-usable gate.
- **2.3b — Documentation of counseling/offer**: FAIL_NO_DIRECT_QUESTION. No canonical question directly adjudicates whether/how counseling or the offer/refusal must be documented. Generic documentation references do not qualify.
- **2.4 — Returning or reusing drugs**: FAIL_NOT_RELEASE_USABLE. Q0088 directly tests return/quarantine/no-reuse but remains AUDIT_PENDING; Q0098 is about naloxone product status and is not a return/reuse substitute.
- **3.3a — Prospective drug utilization review**: FAIL_NOT_RELEASE_USABLE. Q0085 directly tests prospective DUR but is AUDIT_PENDING and is currently tagged Area 2 rather than NABP Area 3.
- **4.2c — Hazardous-drug training/possession/handling/storage/disposal**: FAIL_NO_DIRECT_QUESTION. No canonical question directly tests hazardous-drug training, possession, handling, storage, or disposal. Generic controlled-substance security is not equivalent.
- **4.2e — Controlled-substance inventories**: FAIL_NOT_RELEASE_USABLE. Direct initial/biennial controlled-inventory questions exist but remain AUDIT_PENDING; ADD accountability is not a substitute for the required registrant inventory event.
- **4.3 — Delivery of drugs**: FAIL_NO_DIRECT_QUESTION. Q0209 merely assumes later pharmacy delivery as part of a hospice bridge; it does not test delivery/shipping requirements. No direct release-usable delivery item exists.
- **4.4 — Permitted/mandated product selection**: FAIL_NOT_RELEASE_USABLE. Q0087 directly tests Massachusetts interchangeable-product selection but remains AUDIT_PENDING and is currently tagged Area 3; Q0209 is not a substitution/product-selection question.
- **4.5a — Sterile compounding**: FAIL_NO_DIRECT_QUESTION. Q0117 tests compounded-product labeling, not substantive sterile-compounding practice. No direct substantive sterile-compounding item exists.
- **4.5b — Nonsterile compounding**: FAIL_NO_DIRECT_QUESTION. No direct substantive nonsterile-compounding practice item exists.
- **4.5c — Hazardous compounding**: FAIL_NO_DIRECT_QUESTION. No direct hazardous-compounding practice item exists.
- **4.5d — Non-hazardous compounding**: FAIL_NO_DIRECT_QUESTION. No direct non-hazardous compounding practice item exists.
- **4.6 — Centralized prescription processing / central fill**: FAIL_NO_DIRECT_QUESTION. No canonical question directly tests the Board's shared-pharmacy-service/central-fill pathway.
- **4.7b — Practice-setting license/registration renewal or reinstatement**: FAIL_NO_DIRECT_QUESTION. No canonical question directly tests pharmacy/practice-setting renewal or reinstatement; personal pharmacist renewal is a different competency.
- **4.7c — Practice-setting inspection requirements**: FAIL_NO_DIRECT_QUESTION. The legacy phrase 'available for inspection' in Q0062 concerns record availability, not requirements for inspection of a licensed practice setting.
- **4.7d — Practice-setting disciplinary actions**: FAIL_NO_DIRECT_QUESTION. No canonical question directly tests classifications/processes of disciplinary action against a pharmacy or other practice-setting license.

## Legacy-first consequence

Legacy Q0001–Q0090 contains exactly 6 Area-1 and 16 Area-2 questions. To minimize new authoring, all 22 must be attempted for salvage. Even perfect salvage raises Area 1 only to 23 and Area 2 only to 38, so at least 3 new Area-1 and 2 new Area-2 questions are mathematically unavoidable.

## Taxonomy / diversity debt

Formal cross-area evidence mappings are recorded in the JSON matrix rather than silently rewriting canonical question areas. Headline competency 3.2 currently has only one released direct family and therefore also needs a second distinct transfer family; Q0030/Q0036 are legacy candidates.

## Next locked action

Create a separately named pre-Batch3 coverage-remediation tranche. Salvage legacy content first, beginning with all Area-1/Area-2 legacy questions and the specific semantic salvage targets. Do not author Batch 3. Only after legacy salvage is audited/released and the matrix is recomputed should targeted new coverage questions be authored.

