# B4-B recalculation inputs

Measurement only. This document and its JSON companion measure the bank so the controller can lock the
B4-B allocation. **No slot map is proposed here, nothing was authored, and no existing record was edited.**

| | |
|---|---|
| Measured at commit | `2235bb5b3e63e6e856da1b020a9891e10cb05140` — the tip of `main`, pinned explicitly (see §8) |
| Recorded on | 2026-09-10 |
| Machine-readable companion | `audits/coverage/2026-09-10/B4-B-RECALCULATION-INPUTS.json` |
| Tranche in question | B4-B, reserved `MA-Q-0440..MA-Q-0472`, 33 slots, none authored |

---

## 1. Verified counts

Every figure in the supplied context reproduced exactly.

| Area | RELEASED | Four-mock target | Deficit |
|---|---|---|---|
| A1 Licensure / Personnel | 87 | 104 | 17 |
| A2 Pharmacist Practice | 131 | 160 | 29 |
| A3 Dispensing Requirements | 100 | 116 | 16 |
| A4 Pharmacy Operations | 80 | 100 | 20 |
| **Total** | **398** | **480** | **82** |

Also measured:

- 439 question files exist; 398 RELEASED, 40 `AUDIT_PENDING`, 1 `REVIEW_REQUIRED` (`MA-Q-0172`).
- Highest existing id is `MA-Q-0439`. The reserved range `MA-Q-0440..MA-Q-0472` is empty, and there are no
  gaps anywhere in `MA-Q-0001..MA-Q-0439`.
- 276 rule files at the measured commit: 271 canonical (`CURRENT` plus an accepted verification status) and 5 `UNCLEAR`/`HOLD`.
- 455 families in the matrix. Its `current_candidate_count` and `current_released_count` were recomputed from
  `data/questions/` and matched for **all 455**; no family exceeds its cap.
- The provisional 8 / 11 / 8 / 6 allocation is confirmed `PROVISIONAL_NOT_AUTHORIZED` in both controller
  artifacts.

Two small notes where the repository differs from the framing:

- The per-Area four-mock target **is not stored in `blueprint.json`**. The blueprint carries only Area weights
  (22 / 33 / 24 / 21 percent of a 120-item mock), which across four mocks imply 105.6 / 158.4 / 115.2 / 100.8.
  The figure 104 / 160 / 116 / 100 lives only in `audits/controller/BATCH4-POST-B4A-CHECKPOINT-2026-09-04.json`.
  It totals 480 and each Area rounds within 1.6 items of its weight, so it is consistent — but it is a planning
  figure, not a blueprint field.
- The measured commit is six commits past the sha recorded in that checkpoint. No question lifecycle status
  changed in the interval; the census is unmoved.

---

## 2. Room per Area

Family headroom is `max_questions_in_final_bank - current_candidate_count`, summed per Area, with families
whose rule dependencies are blocked excluded.

| Area | Deficit | Usable headroom | Ratio | Families | At cap | Blocked | Untested canonical rules |
|---|---|---|---|---|---|---|---|
| A1 | 17 | 92 | 5.4x | 86 | 12 (14%) | 0 | **0** |
| A2 | 29 | 92 | 3.2x | 114 | 34 (30%) | 7 | 2 |
| A3 | 16 | 177 | **11.1x** | 144 | 26 (18%) | 0 | 7 |
| A4 | 20 | 158 | 7.9x | 111 | 2 (2%) | 0 | 4 |
| **Total** | **82** | **519** | 6.3x | 455 | 74 | 7 | 13 |

**Most room: Area 3**, then Area 4. A3 has the smallest deficit and the largest headroom; 59 of its 118 open
families have two or more slots free. A4 has almost nothing at cap (2 of 111).

**Least room: Area 2.** It carries the largest deficit (29), the tightest headroom ratio (3.2x), the highest
at-cap share (34 of 114 families), and the only blocked families in the bank — seven Pharmacist administration
families depending on `MA-MH-SUD-ADMIN`, which lock 14 otherwise-usable slots. Its densest topic,
Collaborative practice, already holds 37 released items with 12 of its 33 families at cap.

Family caps are nevertheless **not the binding constraint anywhere**. Every Area has at least three times its
deficit in room, and the bank has 519 usable slots against an 82-item shortfall. See section 3 for what
actually binds.

---

## 3. The largest untested blocks of canonical law — and the surprise

There are almost none.

**Only 13 of 271 canonical rules have zero RELEASED citations**, and the largest single (area, topic) block is
**two rules**. The full list:

| Area | Topic | Untested rules |
|---|---|---|
| A3 | Partial filling | `MA-CII-PARTIAL-PATIENT`, `MA-CII-REMAINDER-30D` |
| A4 | Pharmacy licensure | `MA-MOR-CHANGE-INVENTORY`, `MA-PHARMACY-CLOSURE-PATIENTS` |
| A2 | Controlled prescriptions | `MA-ORAL-CS-FOLLOWUP-TIMING` |
| A2 | Prescription format | `MA-CII-OPIOID-PARTIAL-FILL-NOTATION` |
| A3 | Controlled prescriptions | `FED-CII-EMERGENCY-ORAL` |
| A3 | Dispensing | `MA-COMPLIANCE-PACKAGING-STANDARDS` |
| A3 | Dispensing requirements | `MA-RX-DATE-COUNTING` |
| A3 | Prescription transfer | `FED-CS-TRANSFER-REFILL` |
| A3 | Prescription validity | `MA-SCHEDULE-VI-VALIDITY` |
| A4 | Quality assurance | `MA-QRE-ANALYSIS` |
| A4 | Wholesale distribution | `MA-WHOLESALE-CHANGE-AND-QUALIFICATION` |

It gets tighter. **Nine of those 13 are already carried by an `AUDIT_PENDING` candidate**, so authoring a B4-B
item onto them would collide with work already in the pipeline. Only **four canonical rules are cited by no
question at all**, released or pending:

- `MA-ORAL-CS-FOLLOWUP-TIMING` (A2) — M.G.L. c. 94C ss. 20(c), 23(h); 105 CMR 721.070(B)
- `MA-CII-OPIOID-PARTIAL-FILL-NOTATION` (A2) — M.G.L. c. 94C s. 22(c)
- `FED-CS-TRANSFER-REFILL` (A3) — 21 CFR 1306.25(a), (b), (e)
- `MA-SCHEDULE-VI-VALIDITY` (A3) — 247 CMR 9.04(12), (15)

**Area 1 has zero untested canonical rules.** All 60 of its canonical rules are already cited by a released
question, yet it still owes 17 items.

**The real constraint is proposition novelty, not caps and not new law.** With untested law effectively
exhausted, nearly every B4-B slot must carry a materially new proposition drawn from a rule the released bank
already cites. The workable seam is the thin tail: **146 canonical rules are cited exactly once** (A1 40,
A2 38, A3 33, A4 35) and 226 are cited once or twice. *That is a citation count, not a finding that any given
rule still holds an unexercised proposition — that judgement remains the author's and the controller's.*

Saturation is otherwise mild: one rule exceeds 10 released citations (`FED-CS-SCHEDULES`, 32), 8 sit in the
6–10 band, 23 in 3–5.

Separately, all five `UNCLEAR`/`HOLD` rules are **Area 4** — USP 795 / 797 / 800, the LTCF kit rule, and the
remote/central processing rule. No family in the matrix depends on them, so they do not block any family; they
simply mean that named slice of Area 4 law has no canonical home to author into.

---

## 4. Question-type balance

| Scope | SBA | SATA | SATA share |
|---|---|---|---|
| RELEASED overall | 248 | 150 | 37.7% |
| A1 | 47 | 40 | 46.0% |
| A2 | 82 | 49 | 37.4% |
| A3 | 69 | 31 | **31.0%** |
| A4 | 50 | 30 | 37.5% |
| Tranche `MA-Q-0407..0439` (all 33) | 19 | 14 | 42.4% |
| Tranche, released only (32) | 18 | 14 | 43.8% |

`MA-Q-0426` is the one tranche item still unreleased.

Two things worth carrying into the plan:

- The B4-A tranche ran 4.7 points richer in SATA than the bank average, and the bank average has been drifting
  up because of it. A3 is the outlier at 31% SATA.
- Among released SATA items the **3-correct-of-5 key is 74 of 150 (49.3%)**. The whole-bank structural gate
  caps any single correct-count at 55% and currently measures 49.4%. A B4-B SATA block weighted toward
  3-correct would push that gate. It passes today with zero findings; the margin is about five points.

---

## 5. Authority-risk carry-over — nothing survives

The nine flagged slots (`MA-Q-0453`, `0454`, `0456`, `0459`, `0460`, `0461`, `0465`, `0468`, `0469`) and the
duplicate-risk candidate `MA-Q-0457` were searched for across all of `audits/`, every id in the reserved range.

**No provisional proposition map for `MA-Q-0440..MA-Q-0472` survives anywhere.** Those ten ids appear only as
bare id lists inside two controller artifacts:

- `audits/controller/BATCH4-CLAUDE-HANDOFF-2026-09-02.json`
- `audits/controller/BATCH4-POST-B4A-CHECKPOINT-2026-09-04.json`

Neither records a rule, topic, family, area, or proposition for any of them. Of the 33 ids in the range, 21 are
mentioned nowhere at all; the remaining two mentions are just the range endpoints in `BATCH4-PLAN-V1.json`. Git
history contains no deleted B4-B map. The only per-slot map in the repository is
`audits/coverage/2026-09-01/B4-A-PROPOSITION-MAP-FINAL.json`, covering `MA-Q-0407..MA-Q-0439` only.

*Investigation flag, not a conclusion:* because the propositions those slots were meant to carry are not
recoverable, the recorded authority risk cannot be re-verified as such. The flag is an artifact of slot
position under a superseded allocation; under a recalculated allocation the same ordinals will carry different
propositions. What does carry forward is that the prior planner expected roughly 27% of a 33-slot tranche to
need live authority recheck.

One thing to clean up: **`scripts/batch4_baseline.py` line 37 still hardcodes the unauthorized 8 / 11 / 8 / 6
tranche table** against the superseded 366-released baseline. It is a reporting script, not a gate, but
anything regenerated from it would reproduce the allocation the checkpoint forbids.

---

## 6. Duplication risk

`duplicate_report.json` reports **zero findings across all 439 candidates** at fuzzy threshold 0.82.
`structural_pattern_report.json` reports **zero findings, severity PASS**. There is no duplicate to repair; the
risk is entirely prospective.

Density does not appear at subtopic granularity — the densest single subtopic in the released bank is
A2 / Opioid prescribing / Initial supply at **4 items**, and none reaches 5. It appears at topic and family-cap
granularity:

| Area | Topic | Released | Families | At cap | Remaining headroom |
|---|---|---|---|---|---|
| A2 | Patient care | 18 | 16 | 6 (38%) | 11 |
| A3 | Dispensing requirements | 10 | 8 | 3 (38%) | 5 |
| A2 | Collaborative practice | 37 | 33 | 12 (36%) | 29 |
| A2 | Public health | 10 | 8 | 2 (25%) | 6 |

*Inferred, not measured:* density is a signal about future authoring, not a duplicate finding. Three of the
four flagged topics are in Area 2 — the same Area that is already tightest on headroom.

---

## 7. What would surprise someone planning this tranche

1. **Untested canonical law is essentially gone.** 13 rules bank-wide, largest block two, and only four
   untouched by any question. A plan built on "author into the coverage gaps" has roughly four gaps to work
   with, not 33.
2. **Area 1 has no untested law at all** yet still owes 17 items — every A1 slot must re-cut a cited rule.
3. **Nine of the 13 untested rules are already claimed by pending candidates**, so the apparent gap is smaller
   than it first reads.
4. **Area 2 is the pinch point on every measure at once** — biggest deficit, tightest ratio, most families at
   cap, the only blocked families, and three of the four density-flagged topics.
5. **The nine authority-risk slots carry no recoverable content.** They are id positions, not propositions.
6. **The SATA 3-of-5 share sits about five points below its structural gate**, and the last tranche ran
   SATA-rich.
7. **`data/rules/` was being written to while this was measured.** See below.

---

## 8. Concurrent-write warning

The working tree was **not clean and was changing during measurement**. Between 11:32 and 11:50 local time on
2026-09-10 the parallel Study Guide lane added three files and modified six more, then committed all of it as
`fc65c8e` ("Narrow the transfer section, split out oral prescriptions, repair the V4 findings") onto branch
`claude/sg-repair-v5-scope-split`, leaving the checkout on that branch.

Two of the added files are **new canonical rules**:

- `data/rules/ma-rx-failover-oral.json` — `MA-RX-FAILOVER-ORAL`, Area 2 / Prescription format
- `data/rules/ma-rx-written-format.json` — `MA-RX-WRITTEN-FORMAT`, Area 2 / Prescription format

Both read `status: CURRENT` and `verification_status: PRIMARY_VERIFIED` — and both say in their own
`verification_notes` that an independent audit is still required. **They pass the canonical filter on their
face.**

How this measurement handled it:

- Rules were read from the **pinned commit** `2235bb5` via `git show`, never from disk, so every figure here is
  reproducible against the release line.
- `fc65c8e` is a direct descendant of `2235bb5`, and **`2235bb5` is still the tip of `main`**. The two rules
  exist only on the feature branch.
- **Nothing in `fc65c8e` touches `data/questions/` or `data/exam_style/question_family_matrix.json`.** The
  census, the deficits, the family headroom and the type balance are unaffected by that commit either way.

Why this matters for the plan: had the rules been measured from the working tree, the canonical count would
have read 273 and the **Area 2 / Prescription format untested block would have tripled from 1 rule to 3** —
treating not-yet-independently-audited law as canonical authoring headroom, in the one Area that has the least
room. When `claude/sg-repair-v5-scope-split` merges to `main`, that becomes real headroom and this section
should be re-read. Until then it is not.

---

## 9. Validation

`py -X utf8 scripts/validate_all.py` was run twice.

| Run | Result |
|---|---|
| Live repository (includes Lane B's uncommitted work) | **0 errors**, 7 warnings, exit 0 |
| Isolated `git worktree` at HEAD `2235bb5` plus only these two artifacts | **0 errors**, 6 warnings, exit 0 |

The isolated run exists to attribute the result. All six of its warnings are pre-existing at HEAD and are
already named in the post-B4A checkpoint's `preserved_blockers`: `MA-Q-0190` answer length, `MA-Q-0426`
polarity cue, the three unpublished Study Guide sections, and the inherited SBA answer-length debt at 149/230.
The live run's extra seventh warning is Lane B's new `SG-MA-ORAL-PRESCRIPTIONS` section, not these artifacts.

Adding this analysis introduced no error and no new warning. No validator reads
`audits/coverage/2026-09-10/` — the only path under `audits/coverage/` that `scripts/generate_artifacts.py`
checks is `audits/coverage/2026-09-01/BATCH4-STUDY-GUIDE-COVERAGE.json`.
