# Post-T2 Pre-Batch3 Final Coverage Gate

**Gate:** `PRE_BATCH3_FULL_COMPETENCY_COVERAGE_DEBT_POST_T2` (Issue #40 rerun under controller Issue #83)
**Frozen source:** `remediation/pre-batch3-legacy-salvage-t1` @ `860ec67308772ac63073ed62a7ebdcc565921183`
**Representation:** full from-scratch recomputation, not a projected delta
**Verdict:** **FAIL** — Batch 3 remains **BLOCKED**

## What passed

| Criterion | Required | Measured | Result |
| --- | --- | --- | --- |
| Atomic competency coverage | 46/46 direct release-usable | 46/46 | **PASS** |
| Direct evidence per atomic | ≥ 1 | ≥ 1 for every row | **PASS** |
| Taxonomy mismatches | 0 | 0 unresolved | **PASS** |
| 120-question mock without reuse | assemblable | assembled, 120 items, no reuse | **PASS** |
| Repository validation | PASS | 0 errors, 2 pre-existing warnings | **PASS** |
| Full tests | PASS | 93 passed, 1 skipped | **PASS** |
| Generated-artifact freshness | PASS | clean after regeneration | **PASS** |
| Headline family diversity | ≥ 2 distinct families | **2 headlines have 1** | **FAIL** |

## Release-usable capacity

| Area | Required | Release-usable | Slack |
| --- | --- | --- | --- |
| 1 | 26 | 26 | **0** |
| 2 | 40 | 40 | **0** |
| 3 | 29 | 59 | 30 |
| 4 | 25 | 40 | 15 |
| **Total** | **120** | **165** | 45 |

One blueprint-faithful 26 / 40 / 29 / 25 mock was actually constructed, with no question reused and a
maximum family repeat of 1. Areas 1 and 2 have **zero slack**: the single feasible mock must use every
release-usable Area 1 and Area 2 question.

## Why the gate fails

Two headline competencies now have direct atomic coverage but rest on a **single scenario family**,
against the Issue #40 default minimum of two distinct families.

| Headline | Label | Families | Sole evidence |
| --- | --- | --- | --- |
| 4.3 | Delivery of drugs | 1 | `MA-Q-0215` / `T2_0215_MA_DRUG_DELIVERY` |
| 4.6 | Centralized prescription processing / central fill | 1 | `MA-Q-0220` / `T2_0220_MA_CENTRAL_FILL` |

Both headlines were at zero families before T2, so this debt only became visible once T2 closed their
atomic coverage — the same sequence by which headline 3.2 surfaced after T1 and headlines 2.4 and 4.4
surfaced after the post-T1 rerun.

A legacy-salvage scan over the 61 unreleased canonical questions found **no** candidate for either
headline: nothing unreleased treats central fill, centralized processing, shared pharmacy services or
outsourcing at all, and nothing unreleased has delivery of drugs as its adjudicated subject
(`MA-Q-0023` mentions delivery only peripherally inside an emergency Schedule II scenario). The minimum
remediation is therefore **two newly authored Area 4 questions in two new families**.

Issue #40 permits a written adjudication to justify a narrow family-diversity exception. This controller
does **not** claim one: repository precedent has consistently closed diversity debt by authoring an
additional distinct family, and the controller that would benefit from the exception should not be the
party writing it.

## Post-T2 promotions relative to the frozen baseline

The frozen 46-row baseline matrix (`audits/coverage/2026-08-17/FINAL-PRE-BATCH3-COVERAGE-MATRIX.json`,
git blob `e2490c406b14a540a0b259be8986c90119e760f1`) supplies the atomic definitions. Every row was then
recomputed against the current tree.

- 12 atomic rows are carried solely by T2 evidence: 1.2b, 1.2c, 4.2c, 4.3, 4.5a, 4.5b, 4.5c, 4.5d, 4.6,
  4.7b, 4.7c, 4.7d.
- T2 also added a second family to headlines 2.4 (`MA-Q-0225`) and 4.4 (`MA-Q-0226`), and reinforced
  1.1a (`MA-Q-0224`) and 2.3a (`MA-Q-0213`).
- 6 post-T1 promotions were re-verified: 2.1e, 2.4, 3.2, 3.3a, 4.2e, 4.4.

### From-scratch correction

**2.3b — Documentation of counseling/offer** is recorded as PASS on `MA-Q-0086`, where the frozen
baseline had `FAIL_NO_DIRECT_QUESTION`. `MA-Q-0086` is a released SATA whose entire stem asks which
Massachusetts documentation statements are correct after a patient declines the offer to counsel; its
keyed choices adjudicate recording the failure to accept the offer, the permitted record systems, and the
statutory presumption when no refusal is recorded, and it carries the direct
`MA-COUNSELING-DOCUMENTATION` rule. The baseline listed it only as a 2.3a salvage candidate while it was
still `AUDIT_PENDING`. The independent Auditor-A T2 realism finding separately confirmed that `MA-Q-0086`
"expressly tests the same permitted record locations" — which is precisely why the original `MA-Q-0213`
was failed for distinctness and rewritten.

## Reproduce

```bash
git checkout 860ec67308772ac63073ed62a7ebdcc565921183
python scripts/validate_all.py
python -m pytest -q
python scripts/generate_artifacts.py --write && git diff --exit-code
python scripts/prebatch3_final_coverage_gate.py
```

Artifacts: `POST-T2-PRE-BATCH3-FINAL-COVERAGE-MATRIX.json`,
`POST-T2-PRE-BATCH3-FINAL-GATE-MANIFEST.json`, `POST-T2-PRE-BATCH3-MINIMUM-REMEDIATION-PLAN.json`.
