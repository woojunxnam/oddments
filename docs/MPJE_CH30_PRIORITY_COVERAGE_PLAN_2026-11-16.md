# Massachusetts MPJE Chapter 30 — Seven-Gap Coverage & Quality Plan

**Baseline verified:** November 16, 2026, 95 original questions across 19 fixed
sets in \`woojunxnam/oddments\`. This is a dated planning snapshot. Re-read
\`site/mpje-side-notes/exam-simulation-30/topic-inventory.json\` and inspect
the latest Set before each future question batch.

**Purpose:** Expand the bank for substantive breadth and realistic legal
judgment, not merely increase question count. This is not a statistical
estimate of real MPJE topic-level frequencies or a promise to reproduce NABP
questions. Original questions only; never use secure, recalled item text.

## Priority coverage matrix

The current 37 topic families track broad labels, not all tested legal
mechanisms. A topic count of 3 or 4 does **not** mean all subskills are covered.
Only create new \`topicKey\` values when a legally distinct recurring family
requires them; update \`topic-catalog.json\` and regenerate the inventory when
questions are actually appended, not pre-emptively.

| Priority | Gap family | Current gap evidence from 95-question inventory | New legal decisions to test | Primary verification path |
| --- | --- | --- | --- | --- |
| **P0: Very high** | **Prescription validity & prescriber authority** | A few controlled-prescription, technician-refill and Rx amendment questions exist, but no systematic independent matrix of prescriber authority or all required original Rx elements | Identify authority and restrictions by prescriber (physician, NP/APRN, PA, dentist, other applicable practitioners); detect missing mandatory elements; distinguish invalid vs pharmacist-correctable errors, required new prescription, legitimate medical purpose, federal versus MA electronic/paper/oral exceptions | M.G.L. c.94C and c.112; 105 CMR 700 and 721; 247 CMR 9.04; Board/DCP policies; DEA 21 CFR 1306 |
| **P0: Very high** | **Drug schedule identification** | Direct classification questions are scarce; gabapentin/PMP and controlled quantities appear, but few cases require recognizing a drug's schedule from its specific formulation | Classify names and combination formulations under BOTH MA and federal law; distinguish Massachusetts Schedule VI from federal unscheduled, additional PMP reporting vs control status, dosage-form/salt/combination exceptions; avoid guessing status from a brand name or class alone | M.G.L. c.94C definitions/schedules; 105 CMR 700; DEA 21 CFR 1308 and current scheduling orders; Massachusetts DPH PMP guidance |
| **P0: Very high** | **USP <797>/<800> practical operations** | Three combined sterile/hazardous cases, three nonsterile and one federal 503A/503B case; isolated examples do not cover full compliance workflow | Category and applicable CSP BUD; PEC/cleanroom placement; airflow/pressure, hand hygiene and garbing, media-fill/gloved-fingertip and other personnel competencies, cleaning/monitoring; hazardous receiving/storage, negative pressure, PPE, assessment of risk where allowed, spill and disposal; compare <795> when relevant | Current USP chapters <795>, <797>, <800>; 247 CMR 9.01 and compounding law/policies; 105 CMR and FDA 503A/503B where applicable; confirm version and incorporation/effective date |
| **P1: High** | **Medication delivery, shipping & storage** | Central-fill destination and a counseling-access question exist, but little direct delivery-chain, cold chain or failed-delivery testing | When is a drug considered dispensed/delivered? courier and third-party responsibilities; temperature excursion and quarantine, security/integrity, delivery failure, counseling access, refrigerated or temperature-sensitive medication handling; nonresident/mail-order special rules | 247 CMR 9.02 and 9.19; Board shipping/storage/shared-service policies; 105 CMR 700; manufacturer/FDA labeling and USP storage standards |
| **P1: High** | **Board discipline, inspection & impairment** | Licensure/CE, MOR vacancy and technician rules exist; no dedicated disciplinary/inspection workflow scenarios | Pharmacist vs pharmacy disciplinary consequences, inspection and access to records, reporting/response duties, restrictions and consent orders, impaired practice and appropriate reporting/assistance; distinguish professional liability, Board policy, laws, and criminal reporting | M.G.L. c.13, c.112, c.94C; 247 CMR 2–6, 8–9 and relevant reporting rules; Massachusetts Board disciplinary and licensing resources |
| **P1: High** | **Drug safety & product integrity** | Return-to-stock, recalls and limited DSCSA appear, but adulteration/misbranding, required FDA patient materials and product-integrity questions are thin | Classify adulteration vs misbranding with real facts, defective/expired/counterfeit stock, manufacturer recall and quarantine, Medication Guides and Patient Package Inserts as separate obligations; lawful vs unlawful acceptance/reuse, DSCSA suspect/illegitimate product vs patient recall, PDMA samples/distribution | FD&C Act 21 U.S.C. 351–352; 21 CFR 7, 203, 208, 310 and DSCSA; FDA product-specific labeling; 247 CMR 9.01, 9.13 and 9.16 |
| **P1: High** | **Institutional pharmacy & specialized facilities** | Few independent institutional cases; LTCF exceptions and a limited central-fill question do not cover hospital authority or special licenses | Hospital drug orders vs outpatient prescriptions; floor stock/controlled records, emergency kits, accountability, pharmacy MOR, institution-specific storage/administration/records; nonresident pharmacy licensure, compounding specialty license and transfer/distribution boundaries | 105 CMR 700, 721 and 722; 247 CMR 6 and 9; M.G.L. c.112 and c.94C; Board facility applications/policies; DEA where applicable |

**Evidence caveat:** Above judgments are editorial comparisons of **tested
mechanisms**, not mere keyword matches. Massachusetts Board's June 11, 2025
MPJE review document includes 247 CMR, 105 CMR 700–722, chapters 13/94C/112,
DEA, PDMA, Medication Guides, recall, adulteration and misbranding sources.
NABP's pre-March-2027 MPJE blueprint explicitly identifies practitioners'
authority, disciplinary actions, patient product conditions, delivery and
compounding. Exact Massachusetts topic-level percentages are not public.

## Area mapping under the established legacy blueprint

Continue to create EACH five-item set with **Area 1×1, Area 2×2,
Area 3×1, Area 4×1** and **3 SBA/2 SATA** under the current user policy,
unless explicitly changed. Map by the legal decision being tested:

- Area 1 (Licensure/Personnel): personal licensure, Board restrictions,
  supervisory authority, personnel impairment and disciplinary requirements
- Area 2 (Pharmacist Practice): prescriber qualifications/scope,
  issuing requirements, medication therapy and patient protection
- Area 3 (Dispensing Requirements): validity at point of dispensing,
  schedule/drug identification, dispensing prohibitions, packaging/labeling
- Area 4 (Pharmacy Operations): USP practice environment, delivery,
  receiving/storage, recall/quarantine operations, licensed facilities
- Some topics cross Areas. Pick the **primary evaluated task**, not a
  guessed tag based on the drug or cited regulation.

## Proposed next five-set sequence (planning only)

These are **candidate topic choices**, not authored questions or legal
conclusions. Research current law first, compare adjacent old stems, and
replace any proposed item if an exact rule cannot be supported.

| Future set | Area 1 idea | Area 2 ideas (two) | Area 3 idea | Area 4 idea |
| --- | --- | --- | --- | --- |
| **Set 20** | Pharmacist license restriction/disciplinary notice | Prescriber (NP/PA) authority; prescription issuance details | MA versus federal schedule classification | USP <797> CSP workflow and BUD |
| **Set 21** | Inspection/discipline of an individual licensee | Prescriber (dentist/other lawful professional) restrictions; legal medication-information duties | Drug schedule of a formulation/combination | USP <800> hazardous competency, storage or handling |
| **Set 22** | Impairment/reporting and safe pharmacy practice | Valid Rx elements vs authorized pharmacy clarifications; pharmacist duty in a product-safety event | Invalid controlled Rx vs permitted correction/new Rx | Failed home delivery or shipping temperature excursion |
| **Set 23** | Relevant staff licensing or restriction case | Institutional patient order / prescriber scope; product integrity or Medication Guide | Drug schedules or dispensing prohibition | Hospital/specialized pharmacy operations under 105 CMR 722 |
| **Set 24** | New nonoverlapping individual disciplinary or licensure situation | Prescriber scope with federal/MA interaction; patient-facing safety materials | Validity of Rx or schedule-sensitive labeling | Nonresident pharmacy, recall supply chain or specialized licensing |

**Editorial goal, not mathematical promise:** Aim for **at least three
distinct high-priority gap mechanisms out of every five**, when compatible
with area quotas and independently verified law. Avoid a cosmetic rewording
of the same rule. Do not pad an Area with an unsupported or artificial
example merely to satisfy the table. Prefer breadth across all seven
families over five near-identical cases from one law section.

Do not append placeholder question records or alter the topic catalog
before writing verified new questions.

## Mandatory question-authoring scorecard

Use the checklist to fail/revise a question **before committing**:

1. **Novelty:** name nearest existing question IDs and articulate what
   *different* authority, exception, patient population, deadline or
   decision is now tested. A topic label alone does not establish novelty.
2. **Authority:** find the actual governing official document, precise
   sections, application/effective date, and any newer amendment or
   Board policy. State MA/federal differences accurately, accounting for
   federal preemption and setting; do not assert that MA is always stricter.
3. **Scenario:** provide enough details to resolve the legal issue without
   inventing extra assumptions; identify who is prescribing, dispensing
   or supervising and which schedule/formulation matters. Keep stems
   clear and vary between short, medium and longer decision scenarios.
4. **SBA/SATA:** re-solve the literal stem independently; SBA must have one
   uniquely defensible answer. Every SATA alternative is assessed
   independently with a fully unambiguous key. For current live UI, use
   four A–D options and 2–3 keyed SATA choices.
5. **Distractors:** all plausible; avoid nonrelevant red-herring laws,
   conspicuously longer correct options, automatic 'always/never' giveaways,
   repeated answer positions and arbitrary verbal tricks.
6. **Rationales:** explain **all four choices**, including why an option
   fails under the applicable authority and what a pharmacist actually
   does next. Link official law, not only a study blog.
7. **Audit & publication:** check schema/IDs/set/Area mix, regenerate and
   verify Topic Inventory with Python, validate JS syntax, preview mobile,
   merge on permitted branch and verify actual public deployment and
   regression for individual Check Answer, SATA, Unanswered First, wrong
   review, saved items and browser-local persistence.
8. **Transparency:** distinguish law/regulation, Board policy, DPH
   circular, FDA guidance and USP standard. Do not claim an external
   review or pass-probability calibration that never occurred.

## Canonical sources to re-check per new question

- Pre-March-2027 NABP MPJE Competency Statements:
  https://nabp.pharmacy/programs/examinations/mpje/competency-statements/
- March-2027 blueprint transition:
  https://nabp.pharmacy/news/blog/mpje-content-outline/
- MA Board MPJE Review Information (revised June 11, 2025):
  https://www.mass.gov/doc/multistate-pharmacy-jurisprudence-examination-mpje-review-information/download
- Massachusetts Board regulations and policies:
  https://www.mass.gov/law-library/247-cmr
  https://www.mass.gov/lists/pharmacy-practice-resources
- Massachusetts DPH implementing regulations:
  https://www.mass.gov/law-library/105-cmr
- Massachusetts General Laws:
  https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C
  https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112
  https://malegislature.gov/Laws/GeneralLaws/PartI/TitleII/Chapter13
- Federal DEA (Parts 1300–1321):
  https://www.ecfr.gov/current/title-21/chapter-II
- FDA rules and public product references:
  https://www.ecfr.gov/current/title-21
  https://www.fda.gov/drugs
- USP current standards: https://www.usp.org/

## Preservation

At this plan-writing step **no new Chapter 30 question is requested or
written**. Keep 95 existing objects, Random 10, bookmarks, wrong answers and
localStorage unchanged. This plan guides future READ → VERIFY → CREATE →
ADVERSARIAL AUDIT → SAVE → DEPLOY → PUBLIC TEST work; the plan itself is
not an added question set or proof of legal accuracy for future items.
