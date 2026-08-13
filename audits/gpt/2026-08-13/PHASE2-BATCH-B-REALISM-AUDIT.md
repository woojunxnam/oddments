# Phase 2 Batch B — Realism Audit

- Frozen head: `ffa43e0344c1c08c076bbdaac0323bd20dffefd0`
- Scope: `MA-Q-0051`–`MA-Q-0090` (`INITIAL_BATCH`, 40 items)
- Audit: `AUDIT-GPT-PHASE2-B-REALISM-2026-08-13`
- Style profile: `MPJE-MA-PRE2027` v1 / `293be8fdcd39af2255a22a0423b7123d5cfcf7c0e6c561872eb0ef04e745015c`
- Status: `FULLY_ADJUDICATED`
- Canonical question edits: 없음

## 결과

| Realism | Count |
|---|---:|
| `PASS` | 0 |
| `FAIL` | 40 |

| Required edit | Count |
|---|---:|
| `MINOR_EDIT` | 16 |
| `MAJOR_REWRITE` | 24 |
| `DELETE` | 0 |

## Bank-level discriminator

- `MA-Q-0051`–`MA-Q-0072`: 동일한 generic distractor 세트 반복 — `MAJOR_REWRITE`.
- `MA-Q-0073`–`MA-Q-0088`: 모든 SATA가 canonical key `A/C` — `MINOR_EDIT`.
- `MA-Q-0089`–`MA-Q-0090`: 동일한 `B-D-A-C` ordering template와 timing ambiguity — `MAJOR_REWRITE`.

runtime choice shuffle가 일부 position leakage를 가릴 수는 있지만, canonical export·정적 학습 artifact·회귀 테스트에서 구조가 그대로 노출된다. 또한 SBA distractor는 실제 법적 혼동이 아니라 unrelated template이므로 shuffle로 해결되지 않는다.

## 암기 안전성

`MA-Q-0051`–`MA-Q-0090` 전 문항은 현재 canonical presentation을 그대로 암기하기에 안전하지 않다. Legal key가 맞는 문항도 distractor realism과 answer-pattern 문제가 해결되고 re-audit되기 전까지 release candidate로 취급해서는 안 된다.
