# Massachusetts MPJE — Form E / F / G Authoring Blueprint (360 new questions)

**Updated:** 2026-11-22. **Status:** approved research blueprint proposal / no E-F-G items authored in this change.  
**Existing preserved bank:** A/B 240, C 120, D 120. **Proposed** E/F/G 120 each → 840 total unique question IDs if the full plan is completed.
**User priorities:** Maximize Massachusetts MPJE learning and new decision-making practice. Four A–D options and existing stem/choice-length conventions remain acceptable. Do not spend effort normalizing answer length or expanding to A–E; prioritize precise law and nuanced applicability.

## 1. Blueprint and exam-date versioning

- **Before March 1, 2027:** Use NABP pre-2027 Competency Statements and their Areas 1–4, respectively **22%, 33%, 24%, 21%**. Official: https://nabp.pharmacy/programs/examinations/mpje/competency-statements/
- **On/after March 1, 2027:** Use the new NABP Content Outline Domains 1–4, respectively **30%, 30%, 20%, 20%**. Official: https://nabp.pharmacy/news/blog/mpje-content-outline/
- **Do not treat the old Area numbers as matching new Domain numbers**. Tag every question against its genuine source-defined subdomain (eg `area_2026` and separately `domain_2027` when independently mapped). Display analytics only for an applicable, verified mapping.
- Assume user is preparing for a 2026/pre-March-2027 MA exam for initial build; when the examination date is known, adjust Form G's content blueprint *before writing G*. Do not silently reinterpret Form D's 2027 domain counts as old 2026 areas.

## 2. Three intentionally different forms

Every form is **120 original questions / 150 minutes / one-way navigation / four choices A–D / SBA and SATA / answer explanations only after submission**. Practice mode may provide immediate feedback only outside timed mocks. No publication until all 120 IDs and source gates for the form are ready.

### Form E — Essential Law Mastery (120)

**Purpose:** Quickly recognize what is legal, which personnel/prescribers can act, correct drug schedule, and the applicable federal–Massachusetts rule. Prioritize direct recognition and short-to-medium realistic cases over repeating long existing fact patterns.

| Micro-skill family | Target |
|---|---:|
| Brand/generic ↔ federal and MA Schedule I–VI, formulation/NDC-specific exemptions, MassPAT-trigger distinction | 25 |
| Authorized prescriber and scope (NP, PA, physician, dentist, podiatrist, veterinarian, optometrist, resident), out-of-state RX, required RX fields | 25 |
| CII/CIII–V validity, issue/fill dates, emergency orders, partial fills, refills, EPCS, transfers, PMP and corresponding responsibility | 30 |
| Pharmacist/intern/certified/noncertified technician/trainee scope, CDTM, vaccines, pharmacist prescribing pathways | 25 |
| Counseling, records, labeling and packaging, OTC/pseudoephedrine, patient communication | 15 |
| **TOTAL** | **120** |

**High-priority novelty:** drug *name recognition* without pre-supplying its schedule, schedule-vs-formulation traps, agent vs prescriber signatures, out-of-state distinctions, CDTM scope and technician/intern limits. Do not recreate E30-114, E30-139 or E30-331 with different wording but the same legal answer.

**Editorial mix:** roughly 25% direct recall, 50% routine application, 25% exceptions/complex application (targets only; not measured psychometric difficulty).

### Form F — Applied Pharmacy Law and Operations (120)

**Purpose:** End-to-end legal choices at a working pharmacy or hospital, especially fewer-covered and complex workflows.

| Micro-skill family | Target |
|---|---:|
| USP <795>/<797>/<800>, Category 1/2/3, BUD, C-SCA vs classified suite, HD handling/NIOSH/OSHA, staff/environmental competency | 35 |
| Hospital, clinic and LTCF: nursing unit stock, partial-dose waste, inventory, DPH notification, special dispensing | 20 |
| Delivery, shipping, cold chain, shared processing/central fill, automation, downtime and custody/security incidents | 20 |
| Drug integrity: DSCSA, FDA adulteration/misbranding, recalls, REMS, Orange/Purple Book, biosimilar substitution | 15 |
| DEA Form 222/CSOS/POA, controlled inventory, returns/destruction, registered collector, reverse distributor | 15 |
| Board inspection/discipline/QRE, pharmacy closure/MOR notices, HIPAA/Part 2, adverse incident reporting | 15 |
| **TOTAL** | **120** |

**High-priority novelty:** identify **who** does **what**, **where**, and **by when**, and distinguish independent record/notification obligations for the same event; use fictional independent scenario/record/table data, not copy commercial exam items. Include separate tasks for initial DEA notice, Form 106, MA report, warehouse/cold-chain disposition.

**USP evidence gate:** When direct normative USP text is unavailable, use an official MA Board tool/policy only for claims it directly supports and mark unresolved USP-specific BUD/numeric claims **HOLD**, not verified. No invented USP text.

**Editorial mix:** roughly 15% direct, 55% application, 30% complex workflows.

### Form G — Final Blind 120 (do not preview until first attempt)

**Purpose:** Unseen, integrated readiness rehearsal after E and F learning is completed. G is **new questions**, not a remix of 600 old questions. Avoid posting a public topic-by-topic answer key before first attempt.

**Before 2027-03-01:** Approximate the official old-area distribution on a 120-item mock:
- Area 1 Licensure / Personnel: **26**
- Area 2 Pharmacist Practice: **40**
- Area 3 Dispensing Requirements: **29**
- Area 4 Pharmacy Operations: **25**
- Total **120**. These are editorial approximations, not the exact variable NABP scoring item counts.

**On/after 2027-03-01:** Re-blueprint to new Domain totals **36/36/24/24**, using true new-domain mapping rather than relabeling old Areas.

**Case families:** combined state and federal legal decisions, multi-actor and multi-clock institutional/patient/Board cases, unfamiliar prescribers or products, practical pharmacist action, direct scheduling recall, current Board policies and sensitive privacy situations. Do **not** make every item artificially long or obscure; blend straightforward and multi-rule cases. No official exam item replication or candidate recall copying.

**G reserved status:** Draft on a branch while preparing; merge and expose only when user is ready for the first timed attempt. This is a **practice blind exam**, not a psychometrically validated or genuinely secure official exam. Public static JS may expose answers; avoid visiting or studying the G source before the test.

## 3. Evidence first: source and option-specific law gate

Massachusetts Board's published MPJE review reference sheet: https://www.mass.gov/doc/multistate-pharmacy-jurisprudence-examination-mpje-review-information/download

For every *new* E/F/G question require:
1. Stable `E001…E120`, `F001…F120`, `G001…G120` question IDs; `micro_skill_id`, `legal_decision`, `actor`, `jurisdiction`, `trigger`, `critical_exception`, `correct`, `choices[{text,why}]`, `source_urls[]`, `verified_at`, `law_status`, `revision`, and authentic `area_2026`/`domain_2027` tags.
2. Current operative primary source in 247 CMR, MGL c.94C/c.112, 105 CMR 700–722, MA Board policies, DPH circulars, 21 CFR, FDA, DEA, HHS, and applicable USP where the precise claim requires it.
3. Verify **each of the four** choices (not merely the correct letter): role, schedule, exact form/NDC, 24h/7 day/14 day type, effective date, exception, state/federal difference.
4. **Four decisions:** `SOURCE_PASS`, `SOURCE_HOLD`, `NEEDS_EDIT`, `REJECT`. Do not count a mere provided citation as law approval; don't promote holds to verified to satisfy quotas.
5. Record full exact section/URL and as-of date in a per-option ledger. Preserve known legal conflicts (eg MOR personal 10 day vs 14 calendar day) with separate actors and explicit scope; refer to legal reviewer or authoritative Board clarification if necessary.
6. For C/D original bank: refer to `docs/MPJE_FORM_C_D_LAW_VERIFICATION_RELEASE_GATE_2026-11-22.md`. Its unresolved holds cannot become E/F/G source assertions without independent verification.

## 4. Novelty against ALL prior questions

Before authoring each 20-question batch, create a 480+ question *decision inventory* of what is tested, not just text. Match candidate against old A/B/C/D plus approved new E/F questions on `legal_decision + actor + context + fact changed + outcome`. Exact/semantic stem similarity helps triage but does not prove novelty.

An item may test the same legal section *only if a materially distinct decision* is required (eg new actor, institution, dispensing step, legitimate exception, different federal-vs-MA intersection). No repeat/reworded correct rule with mere patient/drug name swaps.

## 5. Execution and release

- Author **E in six batches × 20**. For each batch: gather official law → write questions in clear English → A–D rationale law gate → novelty screen → record source dates → submit source ledger and only release verified batch.
- Repeat **F six batches × 20**, after using E's skill coverage to correct gaps. Select USP questions only when normatively sourced.
- **G six batches × 20** after E/F coverage mapping; keep withheld from the public site until user chooses the first attempt. Version fixed ID manifest and signing hash.
- Each released form: complete 120 IDs, exact scoring/SATA, 150-minute timer, stop/backtracking protections, retake/history, review filters/CSV, mobile/desktop Playwright, old A/B/C/D history preserved, no invalid links, CI success and actual GitHub Pages URL verified.
- After every attempt generate a helpful study report: first-try correct/incorrect by verified **exam-era** Area/Domain, previously seen vs new, governing rule and source for every incorrect, high-priority weak subskills. Do not infer official MPJE scaled score from raw result.

## 6. Readiness interpretation

- E/F scores = learning and remediation signals; repeated perfect scores on seen items are not a calibrated pass predictor.
- G first-attempt score = less contaminated new-item practice signal, **not** an official NABP pass prediction. An internal study target such as 85%+ with no severely weak high-yield area can guide additional revision, but must never be called the official passing threshold.
- If the actual exam is soon, prefer targeted E/F drills and one carefully validated G rather than rushing to fill all 360 draft slots; legal quality outranks count.
- 2022–2026 candidate anecdotes about CDTM, staff scope, drug names, partial fills, compounding and delivery can guide focus but are not official item-frequency data or secure exam text. Example: https://www.reddit.com/r/MPJE/comments/1vjf1uo/advice_for_the_ma_mpje/ .

## 7. Explicitly out of scope for this roadmap update

No questions authored or published here; no revisions to A/B/C/D keys, text, scores or exam state; no claim that the open C/D source-gate audit is fully complete; no automatic merging of unresolved legal facts.
