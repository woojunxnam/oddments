# Massachusetts MPJE — Form E / F / G Authoring Blueprint (360 new questions)

**Updated:** 2026-11-22. **Status:** readiness-first QA/acceptance design; G0 coverage audit and G1 law mapping remain pending; no E/F/G items authored in this change.  
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
- G first-attempt score = a less contaminated new-item study signal, **not** an official NABP pass prediction. The stricter internal criteria and fail-closed stop rules are defined in Section 7 (90%+ first attempt, at least 80% per applicable domain, and no uncorrected high-severity legal errors). These are **not** NABP passing thresholds.
- If the actual exam is soon, prefer targeted E/F drills and one carefully validated G rather than rushing to fill all 360 draft slots; legal quality outranks count.
- 2022–2026 candidate anecdotes about CDTM, staff scope, drug names, partial fills, compounding and delivery can guide focus but are not official item-frequency data or secure exam text. Example: https://www.reddit.com/r/MPJE/comments/1vjf1uo/advice_for_the_ma_mpje/ .

## 7. Readiness Assurance Contract — FAIL CLOSED (2026-11-22)

**Supersedes any implication in earlier plans that 840 questions, repeated high scores, or simply finishing Forms E/F/G establishes MPJE readiness.** We need evidence of accurate law, comprehensive official-blueprint coverage, successful transfer to new situations, and a controlled unexposed assessment. This internal educational judgment is **not** NABP psychometric calibration or a pass guarantee.

### 7.1 Verified retrospective A–D design deficiencies

Direct inspection of the current repository question objects on 2026-11-22 (structural analysis, **not** an item-by-item legal audit):

| Metric | A/B | C | D |
| --- | ---: | ---: | ---: |
| Questions | 240 | 120 | 120 |
| Single-best-answer (SBA) / SATA | 144 / 96 | 88 / 32 | 92 / 28 |
| Correct SBA uniquely the longest option | **109/144 (75.7%)** | **0/88** | **16/92** |
| Stems under 300 characters | 23 | 17 | 92 |

The extreme SBA option-length distribution in **both directions** is a potential test-taking cue. It does **not** prove any learner used the cue. Review option quality and reasoning; **do not mechanically equalize choice lengths**, which the learner has explicitly deprioritized. Topic names and aggregate Area percentages are not evidence of specific legal decision coverage. D's Area-looking labels cannot simply be pooled with the legacy A/B/C taxonomy. **C has residual normative-USP caveats; D is legal-review preview, not finally source-signed-off.** See the [C/D release gate](MPJE_FORM_C_D_LAW_VERIFICATION_RELEASE_GATE_2026-11-22.md).

### 7.2 Gate G0 — audit and classify the current 480 before E authoring

**G0 classification deliverables (2026-11-22):** [480-item structural baseline](MPJE_E_F_G_BASELINE_480_STRUCTURAL_2026-11-22.json), [480-row provisional tested-decision ledger](MPJE_E_F_G_G0_480_DECISION_LEDGER_2026-11-22.json), and [G0 audit report with explicit C/D holds and overlap queue](MPJE_E_F_G_G0_480_DECISION_AUDIT_2026-11-22.md). **All 480 IDs are provisionally classified into 38 decision families with as-authored keyed claims and evidence tier; 10 legacy C/D legalHold flags and 23 lexical-similarity pairs are tracked. This is classification/triage, NOT 480-option legal approval, official subdomain mapping, verified novelty, or G0 final signoff.**

Complete a versioned 480-row semantic/legal baseline ledger, one item per ID, with fields: form, ID, question revision, exam-era blueprint mapping, specific tested legal decision, actor, setting, jurisdiction, Schedule/formulation, trigger, numerical/time condition, critical exception, exact statutory/regulatory source URL/section, source effective date, last source check, related/duplicated IDs, original answer exposure, and legal release status.

Use four dispositions: **APPROVED / NEEDS_EDIT / HOLD / RETIRED**. Label AI author review, separate AI key-blind source verification, and qualified independent human legal review **differently**; never suggest a human review happened if it did not. Existing date-of-verification metadata and a citation alone **do not** certify each option.

Known priority holds: inaccessible full normative USP text where precise numeric claims depend on it, D090's different pharmacy versus MOR-individual reporting obligations (247 CMR 9.23(2)(f) versus 20.05(1),(3)), and C/D's incomplete option-by-option final signoff. Retain A–D learning history and versioned changes. A high-risk unresolved legal question is **excluded from readiness claims** until resolved or explicitly retired, even if the display remains an educational preview.

**G0 completion evidence:** every 480 ID inventoried with a defensible legal status; no assertion that 480/480 are approved until each required review is actually passed. If an A–D item must change, record its key, version, and impact on previous attempts; do not silently revise an old correct answer.

### 7.3 Gate G1 — official-subdomain × Massachusetts law × microdecision coverage

**Two distinct exam eras:** NABP [old Competency Statements](https://nabp.pharmacy/programs/examinations/mpje/competency-statements/) (Areas 1.1–4.7, effective through 2027-02-28, old Area weights 22/33/24/21) and [new detailed MPJE Content Outline](https://nabp.pharmacy/wp-content/uploads/MPJE-Content-Outline.pdf) (on/after 2027-03-01, Domains 1–4 30/30/20/20, explicit 1A/1B1–4/1C–F, 2A1–3/2B1–9/2C, 3A1–2/3B1–6/3C, and 4A–D). Use NABP's [2026 Domain Crosswalk](https://nabp.pharmacy/wp-content/uploads/2026/07/MPJE-Domain-Crosswalk.pdf) without blindly renumbering old Areas.

Cross-check the [MA Board MPJE applicant reference list (2025-06-11)](https://www.mass.gov/doc/multistate-pharmacy-jurisprudence-examination-mpje-review-information/download): 247 CMR, Board policies/DPH circulars, 105 CMR 700–722, MassPAT/PMP, M.G.L. c.13/c.112/c.94C, 21 CFR/DEA, FDCA/FDA/REMS, federal packaging/marketing and applicable USP. The Board explicitly excludes the separately bundled 801 CMR 1.00–3.00. Do not confuse "has a question in this topic" with "tests its important legal decisions and exceptions."

The coverage-matrix unit is **one outcome-determining legal microdecision**, not a broad subject. Record: controlling rule; who acts; in what setting; at what stage; state/federal interaction; timing/amount; exceptions; source status; studied question IDs; fresh-transfer evidence. Every relevant official subdomain must be **explicitly mapped** to verified coverage, or marked as not applicable to MA with defensible evidence. Unmapped = **open gap**, not PASS.

For each **high-priority decision family** require (across A–G) a direct recognition check, a distinct real-world decision with a legally material changed fact/exception, and a fresh first-encounter application test in G where sampled. Lower-priority items need defensible relevant coverage, not arbitrary duplicate quotas. If a high-risk family has no verified material, **block readiness regardless of mock score**. Publication thresholds count legal *decisions*, not question objects.

Sentinel families: brand/generic and formulation-specific federal-vs-MA Schedule recognition; prescriber authorization/MCSR/DEA and out-of-state Rx; Rx validity, emergency CII, EPCS, CII partial fills, CIII–V refills/transfers; MassPAT; CDTM and pharmacist prescribing protocols; technician/intern/pharmacist duties and vaccines; counseling/labels/packaging/PPPA; USP 795/797/800 and NIOSH, HD refrigeration and environmental competency; institutional/hospital/LTCF controlled drugs; delivery/cold chain; DEA orders/POA, inventory, theft/loss, disposal; inspection/MOR/discipline/impairment; HIPAA/42 CFR Part 2; FDA adulteration/misbranding, DSCSA, REMS, recalls, Orange/Purple Book, returns; pharmacy licensure/automation/central-fill/cybersecurity; malpractice/duty to report. These are **coverage risk families**, not statistical claims about actual item frequency.

### 7.4 Revise E and F slots AFTER G1; do not fill quotas by rewording

**E (120):** law-recognition and dispensing-authority transfer. Include realistic short common-drug identification **without telling the examinee the Schedule when classification is tested**, formulation/MA Schedule VI differentiation, legitimate practitioner credentials and authority, pharmacist vs nonpharmacist scope, and exact controlled-Rx exceptions. Use the original category counts as *provisional*, not as a justification to produce redundant items.

**F (120):** end-to-end operational legal decisions. Use original, fictional prescription/transfer records, staffing rosters, MARs, DEA order and inventory logs, shipping/cold-chain excursion records, compounding/environmental-monitoring logs, Board inspection and reporting examples, and FDA product-selection tables. Each question asks a concrete action, actor, location, timing and documentation, not general trivia. Blend straightforward and complex cases; avoid making every item long or rare.

For **each 20-question batch** keep a source-and-novelty acceptance record:
1. Every candidate has a specific new decision/exception, closest earlier IDs, material delta, and why it is not a disguised duplicate; otherwise **REPLACE**.
2. **All four A–D options** have separately checked legal rationales, exact current operative primary citations, proper jurisdiction and dates; author and reviewer must check whether an intended distractor is also legally acceptable.
3. An answer-key-blind adversarial reviewer solves the scenario based only on law and stem, then compares with the author's key; review the **one-fact counterfactual flip** that would alter the legal conclusion. AI second-pass review is not falsely labeled as external independent certification.
4. Check clue-based answering (unrealistic absolutes, length/structure, grammatical cues), implausible distractors and excessive scenario length, **without prioritizing cosmetic equal-length editing**.
5. Resolve source conflicts/effective dates; if current normative USP text cannot be authenticated, **HOLD or replace** the USP-specific numeric assertion. A Board checklist or USP FAQ supports only the narrow text it actually establishes.
6. Report attempted/approved/revised/held/rejected numbers and source proof. **A batch cannot be marked complete with any unresolved HOLD**; 120-item form release requires 120 clean accepted items and clean automated/browser checks.

### 7.5 Form G is a HOLDOUT, not a reward for finishing E/F

G is **120 entirely fresh, separately reviewed, non-reworded items**, authored only after verified G1 coverage and E/F remediation. Preserve multi-setting, prescription/records-based, drug recognition, exceptions and state-federal comparisons with varied stem length and SBA/SATA. Four A–D choices are acceptable for site compatibility; the real exam is adaptive and some NABP public samples use five options. Do not pretend the model reproduces NABP item statistics.

**For exams through 2027-02-28:** 120-item editorial legacy Area allocation **26/40/29/25**. **On/after 2027-03-01:** authentic new Domain allocation **36/36/24/24**. Do not begin G without confirming the exam-era blueprint. These proportions are approximations to the official 100-scored-item domain weights, not a prediction of the real 120-item distribution.

Hold G off the publicly linked study pages and refrain from showing its source, answer keys or topic slots until the first attempt. A client-side GitHub Pages JS app cannot create cryptographic secrecy; call this an **unseen first-attempt holdout**, not a secure psychometrically calibrated test. Freeze IDs, revision/content manifest, version hash, and first-exposure flags. Deliver 120 questions / 150 minutes / forward-only progression / no mid-exam explanation / exact-set SATA scoring / preserved timer on reload / isolated attempt history / post-submission rationale and source review. A retake cannot count as a first-encounter validation.

### 7.6 Two separately required final gates

**A. CONTENT AND DEPLOYMENT GATE — every condition required**

- All 480 legacy IDs accounted for and high-risk unresolved legal assumptions excluded from readiness-counted materials.
- **100% documented disposition for each applicable official exam-era subdomain** and MA Board authority family; **0 unaccounted high-priority decision gaps** (not a claim to have sampled every possible statutory detail).
- E/F/G: **120 accepted unique IDs each**, all four options checked against official sources, **0 disputed keys, 0 outstanding source holds, 0 quota-filler legal duplicates**.
- Legally material source updates rechecked at the examination date; aim to recheck high-risk effective-date-sensitive rules within **14 days before the actual exam** and after changes. Date rule is a study QA target, not a Massachusetts statutory deadline.
- Full release checks: schema, counts, distinct IDs, one-way navigation, score/SATA, timer, answer withholding, history isolation, review export, mobile/desktop browser, successful CI and **actual working published URL**. GitHub merge alone does not prove deployment. Qualified human legal review, if not performed, is disclosed as absent.

**B. LEARNER GATE — author-defined targets, not NABP pass thresholds**

- E and F **at least 90% after study/remediation**, with rule explanations for missed items; separate first attempts from exposed retakes.
- G **first truly unseen unassisted attempt at least 90% overall**, **at least 80% in each applicable Area/Domain**, and complete in **150 minutes**. Domain sample sizes are limited; aggregate score is not a calibrated passing probability.
- Any **high-severity legal misunderstanding** (invalid prescriber, wrongly dispensing controlled medication, reporting clock, unsafe USP/HD action, etc.) requires explicit correction, explanation of MA versus federal law, and a **new fact-pattern transfer check** after remediation (ideally 48–72 hours later). An uncorrected high-severity error blocks the internal readiness decision even with a high G score.
- If G was leaked, previously studied, or did not meet threshold, status = **INSUFFICIENT EVIDENCE**; do not simply retake G and claim readiness. Remediate and use an explicitly newly authored assessment only if needed, transparently outside the original 840-item plan.
- Passing all gates supports a cautious **"ready to sit the Massachusetts MPJE"** study decision. It does **not** certify a pass probability. An official Pre-MPJE, if unavailable to the learner, is **not required**; never copy or process its confidential item content.

### 7.7 Evidence artifacts; stop rules

Before calling E/F/G complete, link dated artifacts in this roadmap: **(1)** audited 480-ID baseline ledger, **(2)** official subdomain × microdecision coverage table with unresolved gaps, **(3)** E/F/G per-choice primary-source law ledgers, **(4)** novelty/key-blind/ambiguity audits, **(5)** tested public page/CI evidence, and **(6)** first-exposure-aware learner readiness report. **Missing artifact = PENDING; no invented signoff.**

**STOP and report the blocker rather than adding more questions** if high-priority subdomains are missing; federal/MA law conflicts; USP source access is insufficient; a choice is defensible under another answer; only cosmetic novelty exists; G is compromised; actual site validation/regression tests fail; or the exam uses a newer official blueprint.

**Primary sources checked on 2026-11-22:** [NABP old blueprint](https://nabp.pharmacy/programs/examinations/mpje/competency-statements/), [NABP new detailed blueprint](https://nabp.pharmacy/wp-content/uploads/MPJE-Content-Outline.pdf), [NABP Domain Crosswalk](https://nabp.pharmacy/wp-content/uploads/2026/07/MPJE-Domain-Crosswalk.pdf), [NABP MPJE administration facts](https://nabp.pharmacy/programs/examinations/mpje/take-the-mpje-exam/), [MA Board reference list](https://www.mass.gov/doc/multistate-pharmacy-jurisprudence-examination-mpje-review-information/download), [existing C/D source audit](MPJE_FORM_C_D_LAW_VERIFICATION_RELEASE_GATE_2026-11-22.md).

## 8. Explicitly out of scope for this roadmap update

No questions authored or published here; no revisions to A/B/C/D keys, text, scores or exam state; no claim that the open C/D source-gate audit is fully complete; no automatic merging of unresolved legal facts.
