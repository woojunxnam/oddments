# Batch 3 — controller handoff to GPT Desktop

**Created** 2026-08-20 · **Repository** `woojunxnam/oddments` · **Authorizing issue** #91 · **Controller issue** #83

> **GitHub is authoritative.** The machine-readable handoff at
> [`audits/controller/BATCH3-GPT-DESKTOP-HANDOFF.json`](../audits/controller/BATCH3-GPT-DESKTOP-HANDOFF.json)
> is the canonical record. This page is a summary of it. If this page and git state disagree, **git state wins**.
> Verify `main_sha` against live `origin/main`. If it has advanced, that alone does not make these
> numbers stale — this handoff branch is merged to main right after it is written. Run
> `git diff --name-only 79e14172d339fa1211e0eca849a72c38cc79f064 origin/main -- data/`; empty output
> means no canonical record changed and every count below is still exact.

---

## A. What Batch 3 is trying to achieve

Bring the Massachusetts MPJE bank to a released pool that can seat **three distinct 120-question mock exams**
with no question reused across them. Each exam takes 26 Area 1, 40 Area 2, 29 Area 3 and 25 Area 4, so the
minima are that allocation times three:

| | Area 1 | Area 2 | Area 3 | Area 4 | Total |
|---|---|---|---|---|---|
| **Minimum** | 78 | 120 | 87 | 75 | ≥ 360 |

These are **question** counts, not family counts. They are fixed — do not re-open blueprint reallocation.

---

## B. Exact current canonical state

Measured from `origin/main` at `79e14172d339fa1211e0eca849a72c38cc79f064`:

| | Area 1 | Area 2 | Area 3 | Area 4 | Total |
|---|---|---|---|---|---|
| **Released** | 78 | 81 | 71 | 61 | **291** |
| Canonical | 78 | 124 | 122 | 82 | 406 |
| **Deficit to minimum** | 0 | **−39** | **−16** | **−14** | **−69** |

Lifecycle: 291 RELEASED, 114 AUDIT_PENDING, 1 REVIEW_REQUIRED (MA-Q-0172). Highest ID `MA-Q-0406`;
next free `MA-Q-0407`.

---

## C. What is already safely released

| Tranche | IDs | Released | Held |
|---|---|---|---|
| B3-A | 0229–0261 | 33 | 0 |
| B3-B | 0262–0294 | 33 | 0 |
| B3-C | 0295–0327 | **28** | 5 |

B3-C's five held items and why:

- **MA-Q-0309 / 0310 / 0313** — realism FAIL, MAJOR_REWRITE, `distinct_from_bank` against
  MA-Q-0213, MA-Q-0086 and MA-Q-0085 respectively. Legally sound; not repaired.
- **MA-Q-0311 / 0322** — passed the B3-C audit, then the SATA correct-count correction moved their
  hashes. They were re-audited inside the `CLAUDE-FRESH-B3D-V3` package and **are** in its qualifying set.

> Do not repeat the older narrative counts of 31 / 30 / 28. Recompute from the records.

---

## D. Authored, audited, **not yet released**

All three outstanding audits are **COMPLETE** with committed LEGAL and REALISM records. None has been
released — this handoff arrived before the release step.

| Package | IDs | n | Auditor | PR | Qualifying | Not qualifying |
|---|---|---|---|---|---|---|
| **B3-D v3** | 0328–0360 + 0311, 0322 | 35 | `CLAUDE-FRESH-B3D-V3` | [#109](https://github.com/woojunxnam/oddments/pull/109) | **31** (all A2) | 0340, 0348, 0350, 0359 |
| **B3-E v3** | 0361–0390 | 30 | `CLAUDE-FRESH-B3E-V3` | [#110](https://github.com/woojunxnam/oddments/pull/110) | **27** (A2 4 / A3 9 / A4 14) | 0365, 0377, 0389 |
| **B3-F** | 0391–0406 | 16 | `CLAUDE-FRESH-B3F` | [#108](https://github.com/woojunxnam/oddments/pull/108) | **13** (all A3) | 0393, 0398, 0404 |

---

## E. Audit state of every tranche

| Tranche | Freeze branch | Freeze SHA | Auditor instance | State |
|---|---|---|---|---|
| B3-C | `freeze/batch3-b3c-v1` | `136d2fea` | `CLAUDE-FRESH-B3C` | COMPLETE, released |
| B3-D v1 | `freeze/batch3-b3d-v1` | `e3fd5a36` | `CLAUDE-FRESH-B3D` | SUPERSEDED |
| B3-D v2 | `freeze/batch3-b3d-v2` | `0047fadb` | `CLAUDE-FRESH-B3D-V2` | SUPERSEDED, no evidence committed |
| **B3-D v3** | `freeze/batch3-b3d-v3` | `0f7e076c` | `CLAUDE-FRESH-B3D-V3` | **COMPLETE** |
| B3-S3 v1 | `freeze/batch3-s3-v1` | `6343e472` | `CLAUDE-FRESH-B3S3` | SUPERSEDED |
| B3-S3 v2 | `freeze/batch3-s3-v2` | `1072516f` | `CLAUDE-FRESH-B3S3-V2` | COMPLETE — **0 usable** |
| B3-E v1 | `freeze/batch3-b3e-v1` | `14481dcf` | `CLAUDE-FRESH-B3E` | SUPERSEDED |
| B3-E v2 | `freeze/batch3-b3e-v2` | `0b3a156f` | `CLAUDE-FRESH-B3E-V2` | SUPERSEDED, never started |
| **B3-E v3** | `freeze/batch3-b3e-v3` | `36ffd43f` | `CLAUDE-FRESH-B3E-V3` | **COMPLETE** |
| **B3-F** | `freeze/batch3-b3f-v1` | `f798d3e2` | `CLAUDE-FRESH-B3F` | **COMPLETE** |
| Q0172 | `freeze/auth-review-0172-v1` | `8379585e` | — | NOT_STARTED |

Every freeze branch is **immutable**. Never use a freeze commit as the authoring base for a later tranche.
All three completed audits committed a Phase-1 blind lock **before** unsealing, with
`contamination_status: CLEAN` and all four not-inspected-before-lock flags `false`.

---

## F. What failed and why

**B3-S3 v2 — the legacy salvage returned nothing.** All eight questions failed realism (7 MAJOR_REWRITE,
1 DELETE) as near-clones of released items, bare number recall, or options recoverable from their own
wording. LEGAL was fine. This is why B3-F exists.

**Two keying errors this controller made, caught by independent audit:**

- **MA-Q-0404** — option B ("the pharmacy is the party federally restricted to 3.6 g per purchaser per
  day") is a *true* statement of 21 CFR 1314.20(a) read with the `regulated seller` definition in
  21 CFR 1300.02, and the stem asks which statements are correct. It was authored as a distractor on an
  incompleteness rationale. Proposed key **B, C, D**.
- **MA-Q-0340 and MA-Q-0348** — each omits a correct option on a reading that adds a condition the option
  does not contain. The auditor flagged this as possibly **systematic** and suggested the rest of B3-D be
  checked for the same shape.

None of these was repaired: the handoff freeze arrived first.

---

## G. What was superseded and why

The v1/v2 packages exist because of two corrections, both preserved:

1. **A one-time clean lineage cure.** Early freezes were built on lineages carrying another tranche's
   sealed package, which would have leaked post-lock material into an auditor's worktree. The v2/v3
   lineage is cut from a content-only commit.
2. **The SATA correct-count correction.** Seven questions changed from four-correct to three-correct,
   moving their hashes and invalidating the packages that described them.

No superseded freeze was rewritten, force-moved or deleted. `CLAUDE-FRESH-B3D-V2` produced no evidence
(its branch tip *is* the freeze commit); no branch was ever created for `CLAUDE-FRESH-B3E-V2`.

---

## H. Arithmetic to 360

Releasing every qualifying question from the three completed audits — 31 + 27 + 13 = 71:

| | Area 1 | Area 2 | Area 3 | Area 4 | Total |
|---|---|---|---|---|---|
| Projected | 78 | **116** | 93 | 75 | **362** |
| Minimum | 78 | 120 | 87 | 75 | 360 |
| Margin | **0** | **−4** | +6 | **0** | +2 |

**Area 2 finishes four short.** Areas 1 and 4 land exactly on their minima with no margin, so neither can
absorb a later withdrawal.

Seven Area-2 repair candidates exist for the four needed:

- from B3-C: **MA-Q-0309, 0310, 0313** — legally sound, fail `distinct_from_bank`
- from B3-D v3: **MA-Q-0340, 0348** (keyed wrong — need a key correction, not only a rewrite),
  **MA-Q-0350, 0359** (legally sound, realism only)

---

## I. Final-gate status at `79e1417`

| Gate | Result |
|---|---|
| `validate_all.py` | PASS — 0 errors, 1 pre-existing warning (MA-Q-0190) |
| `pytest -q` | PASS — 98 passed, 1 skipped |
| duplicate detector | PASS — 0 over 406 questions |
| structural detector | PASS — 0 |
| answer distribution | PASS — chi-square 0.418972 |
| tranche pattern gate | PASS — 0 errors |
| atomic coverage | PASS — 46/46 |
| headline family diversity | PASS — no debt |
| taxonomy | PASS — none unresolved |
| generated artifact freshness | PASS |
| single 120-question mock | PASS — no reuse |
| **three-exam construction** | **FAIL** — exams 1 and 2 assemble at 120 each with every question from a distinct family; exam 3 reaches 51, short 39/16/14 |

The three-exam failure is exactly the outstanding deficit of 69. It closes when the releases land and the
Area-2 gap is closed.

> **Caveat.** These are *main's* gates. Landing the B3-F audit records makes `validate_all` **FAIL with
> 2 errors** until `BATCH3-B3F` is authorized — see below.

---

## J. Shortest quality-preserving path to completion

1. **Authorize `BATCH3-B3F`** in `TARGETED_INITIAL_BATCH_AUTHORIZATIONS` in `scripts/validate_audits.py`,
   following the Issue #86 precedent, then land PR #108. The scope cannot be `INITIAL_BATCH` (which needs
   30+ results; B3-F has 16). `CLAUDE-FRESH-B3F` correctly refused to amend the allowlist itself and
   confirmed by read-only diagnostic that both records validate at 0 errors once authorized.
2. **Land PR #109** and guarded-release B3-D v3's **31**.
3. **Land PR #110** and guarded-release B3-E v3's **27**.
4. **Release B3-F's 13.**
5. **Recompute all four area counts.** Expect 362 with Area 2 at 116.
6. **Repair exactly four Area-2 questions** from the seven candidates, then have a **fresh auditor
   instance** reaudit them. Do not self-certify.
7. **Re-run every gate**, including `scripts/check_three_exam_construction.py`, then declare
   `BATCH3_COMPLETE`.

---

## K. What NOT to do

- Do not self-audit anything you author or repair.
- Do not continue a partially-unsealed audit under the same `auditor_instance`.
- Do not weaken a validator, schema or test to make a gate pass. Authorizing `BATCH3-B3F` in the
  allowlist is a *governance authorization* with an Issue #86 precedent — nothing else in that file may
  be loosened.
- Do not rewrite, force-move or delete any freeze branch or any failed audit record.
- Do not relabel Area 3 or Area 4 content as Area 2 to close the Area-2 gap.
- Do not restore **MA-Q-0028** (quarantined) or **MA-Q-0172** (contained). Batch 3 is completable without
  either: the headline 2.2 family-diversity debt MA-Q-0172 used to carry was closed by promoting
  **MA-Q-0174** through the existing promotion registry.
- Do not re-apply the two deferred citation corrections without reading `CITATION-FIX-PROPAGATION` in the
  handoff JSON first. Running `scripts/update_content_hashes.py` after editing those rule records
  propagates through 62 drug records and breaks the `final_adjudication` pins of released questions.
- Do not re-derive an Area-2 exhaustion conclusion from family counts. Family caps run 1/2/3; count
  question slots, not families.

---

## L. Verify these first

```bash
git fetch --all --prune
git rev-parse origin/main                      # expect 79e14172d339fa1211e0eca849a72c38cc79f064
git log --oneline origin/main -3
git branch -r | grep -E 'audit/batch3|freeze/batch3'
for r in 0f7e076c 36ffd43f f798d3e2 136d2fea; do git cat-file -t $r; done
gh pr view 108 --json state,title
gh pr view 109 --json state,title
gh pr view 110 --json state,title
python scripts/validate_all.py
python -m pytest -q
python scripts/prebatch3_final_coverage_gate.py
python scripts/check_three_exam_construction.py
python scripts/check_tranche_key_patterns.py
python scripts/batch3_inventory.py
```

Then read, in this order:

1. `audits/controller/BATCH3-GPT-DESKTOP-HANDOFF.json` — canonical
2. `audits/controller/BATCH3-SATA-PATTERN-CORRECTION.json`
3. `audits/controller/B3S3-V2-AUDITOR-SIDE-FINDINGS-VERIFICATION.json`
4. `audits/controller/BATCH3-AREA3-TOPUP-DETERMINATION.json`
5. `audits/remediation/2026-08-20/B3C-AUDIT-VERIFICATION-NOTES.json`

---

## Open findings the next controller should weigh

Reported by independent auditors and **not** verified by this controller before the freeze. A comparable
S3 finding about MA-Q-0014 was checked and **refuted**, so verify before acting.

1. **`MA-COMPLIANCE-PACKAGING` conflict — highest priority.** `CLAUDE-FRESH-B3F` reports that this rule and
   the **released** questions MA-Q-0169, MA-Q-0202 and MA-Q-0203 assert a Schedule II/III maintenance
   allowance for multi-drug-single-dose packaging that **247 CMR 9.08(3)(b)** (Mass. Register #1536,
   12/6/2024) prohibits. If confirmed, that is a legal defect in three released questions.
2. **Bank-wide SBA answer-length leakage.** `CLAUDE-FRESH-B3E-V3` measured the longest option as the key in
   153 of 234 SBA items outside its tranche — 65.4% against a 20% baseline. The existing
   `SBA_ANSWER_LENGTH_LEAKAGE` detector tests per-item outliers and misses the aggregate tendency. Not a
   completion blocker under the current gate set, but consequential.
