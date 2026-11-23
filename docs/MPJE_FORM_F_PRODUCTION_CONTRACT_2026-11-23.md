# Massachusetts MPJE — Form F: Applied Pharmacy Law & Operations
**Frozen production contract — November 23, 2026**

## Mission and no-loop rule
Form F is **a NEW, original, 120-item applied-law practice exam**, distinct from Form E Essential Law Mastery. Produce a complete, deployable exam; do not reopen the A–E 600-question legal-review backlog or require A–E signoff to start/finish Form F. A–E are read-only reference data for preventing repetition of the **same legal decision**, not a prerequisite to review old option-level citations. Do not edit old questions, old mocks or saved attempts.

A literally perfect predictor of the secure NABP MPJE is not possible. Form F is rigorously source-checked **educational practice**, never official, psychometrically calibrated, externally pharmacist-certified or a pass guarantee.

## Exactly one blueprint by exam date
The user selected the **pre-March 1, 2027** NABP Competency Statements: Area 1 22%, Area 2 33%, Area 3 24%, Area 4 21%, approximated at 120 items by **26 / 40 / 29 / 25**.
Official: https://nabp.pharmacy/programs/examinations/mpje/competency-statements/
On or after March 1, 2027, the new Content Outline governs; do **not** silently relabel these old Areas as 2027 Domains.
Official: https://nabp.pharmacy/news/blog/mpje-content-outline/

## Final deliverable — 4 self-contained batches, not repeated review cycles
| Batch | IDs | Area 1 | Area 2 | Area 3 | Area 4 | Total |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | F001–F030 | 7 | 10 | 7 | 6 | 30 |
| 2 | F031–F060 | 6 | 10 | 8 | 6 | 30 |
| 3 | F061–F090 | 7 | 10 | 7 | 6 | 30 |
| 4 | F091–F120 | 6 | 10 | 7 | 7 | 30 |
| Total | F001–F120 | **26** | **40** | **29** | **25** | **120** |

Every batch follows **SOURCE → AUTHOR → 5 EXPLANATIONS → VERIFY → SAVE → READBACK**, then continue. No end-of-batch digression into re-auditing A/B/C/D/E. If a candidate has an ambiguity or unverifiable rule, **replace that candidate inside the same batch** rather than shipping a known flawed case or creating a new ongoing hold-list. Record the failed candidate only in editorial notes.

Keep all Form F content in separate files and an isolated git branch/PR. After F120, perform one bounded final **Form F-only** test and release; do not generate another planning phase.

## What distinguishes F from E
- **E:** identifies and recalls the law, schedule, limits, and direct professional duties.
- **F:** picks the lawful **action now** in a new workflow: who may act, what to verify, what must be held, who must be notified, what/when to record, and when the proposed action becomes legal. Present clinically plausible, genuinely competing options.
- 120 unique `legal_decision` IDs, no outcome-equivalent scenario copied from A–E. Reusing a broad statute is acceptable if the determining fact, actor or exception changes.
- Require a materially *outcome-changing* one-fact `counterfactual_flip`, not just paraphrasing the key.
- Most cases test ≥2 relevant conditions, 30% add a second interacting legal authority, **never** invent an unrelated complication to make the stem long.
- Scenario variety: community/chain, hospital/LTCF, mail/remote, sterile/HD, nonresident, emergency/shortage, inspected/incident, team scope. Do not equate a rare setting to an official exam probability.
- Approximately 10% concise direct-application, 60% 1–2-condition reasoning, 30% integrated multi-rule workflows. These are editorial targets, not NABP sampling claims.
- Mix concise, medium, and longer stems; avoid automatic giveaway words such as `always`/ `never` as a substitute for realistic distractors.
- Five A–E options per item with **one** keyed answer for SBA or **2–4** for SATA. SATA cardinality must vary organically. No fixed visible key-position or answer-length cues. The bank's hidden answer distributions should not be stated publicly ahead of a first blind attempt.

## Scenario coverage — cross-tags, NOT additional primary Area quotas
Every item has one genuine legacy primary Area plus secondary scenario tags. The following are *minimum exposure targets* with overlaps allowed:
- Pharmacy personnel/supervision/scope and independent pharmacist judgment: ≥15
- Prescriber authority, authentic prescription, controlled refill/transfer: ≥20
- High-risk DEA inventory, CSOS/222, OUD, theft/loss/disposal: ≥16
- USP <795>/<797>/<800>, sterile/nonsterile/HD workflow, BUD, failed monitoring: ≥20
- Hospital/LTCF/clinic and patient-specific-versus-stock decisions: ≥12
- Cold-chain, failed delivery, storage, pickup and pharmacy automation/downtime: ≥14
- FDA labeling, DSCSA, REMS, returns, recall/product integrity: ≥12
- Board/DPH reporting, inspection, discipline, facility/MOR registration: ≥12
- Counseling, prospective DUR, MassPAT, HIPAA/Part 2, public-health prescribing: ≥12

This gives F broad patient-safety and practice exposure without artificially forcing 35 compounding questions into legacy Area 4's 25 primary slots. Count overlapping clinical contexts through secondary tags.

## Sources and author approval, per F item
Check the **effective law on the item scenario's date**, Massachusetts + federal as applicable, and any stricter governing condition. Core primary sources:
- https://www.mass.gov/lists/laws-and-regulations-of-the-board-of-registration-in-pharmacy
- https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C
- https://www.ecfr.gov/current/title-21/chapter-II
- https://www.deadiversion.usdoj.gov/
- https://www.fda.gov/
- https://www.mass.gov/orgs/department-of-public-health
- USP official FAQ or normative standards when accessible. **Do not certify a numerical USP claim from an unavailable paid chapter; choose a verifiable different rule or explicitly mark the item excluded from active exam.**

Each question must have `id`, `slotId`, `area_2026`, `competency`, `kind`, `topic`, `scenario_tags`, `actor`, `trigger`, `legal_decision`, `critical_exception`, `counterfactual_flip`, `stem`, five `choices[{text,why}]`, `correct`, precise `citation`, `source_urls`, `verified_at`, `law_review_status`, `reviewer_type`, `closest_existing_ids`, and `revision`.
A credible primary citation with a URL is **not** in itself evidence of legal approval. For every option, test why it is right/wrong **under exactly the stated facts**; verify dates, exceptions, state–federal interplay and any numbers. Use `AI_PRIMARY_SOURCE_REVIEWED` only when the author has actually checked the source; never claim independent clinical/legal reviewer signoff that did not occur. The use of an AI-authored practice exam must be disclosed honestly, not used to reopen old-form reviews.

## Structural and release safeguards
1. Every F item must have 5 nonempty option explanations; keys and `Correct./Incorrect.` labels agree, ID F001–F120 unique.
2. Compare F against A–E for **same decision with same outcome**, not just literal identical text. Find/replace genuinely duplicated decision candidates *before* committing each batch.
3. Detect answer-length/key-position cues and easily guessed distractors within each completed batch. Rework only the new F item.
4. Freeze a signature-bound 120-item Form F manifest and keep a fixed one-way 150-minute mock with time expiry, persistence, retakes, wrong-answer review and downloadable result.
5. New localStorage key. No mutation of A–E old question objects, manifests, grading, scores or history. Mobile (390px) + desktop (1280px) automated end-to-end tests, exact SBA and SATA grading, and source-link checks.
6. **One bounded F-only legal/source and usability release gate after F120**, fix defects when found, then publish to Pages and **verify the public page and current branch**. No request for another 600-question audit. If an external qualified human legal audit is unavailable, publish as *source-reviewed educational practice; not independently certified*—never silently claim certified.
7. Preserve the original official blueprint tagging and cite the official sources. The real MPJE uses a 150-minute, 120-item adaptive format; this practice engine is nonadaptive and its raw percentage cannot predict a pass.

## Definition of finished
**F001–F120 authored + option rationales confirmed against cited current sources + no known ambiguous scoring items + fixed manifest + passing browser tests + merged PR + verified public URL.** Do not replace this with a rolling series of additional retrospective audit gates. If changes in law arise later, version the affected Form F item and preserve the user's original attempts.

**Next action:** author **F001–F030 immediately** under this contract, do not create another research/readiness report before the questions.
