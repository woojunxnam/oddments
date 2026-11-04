# Phase 2 Batch A — Legal Audit

- Frozen head: `ffa43e0344c1c08c076bbdaac0323bd20dffefd0`
- Scope: `MA-Q-0011`–`MA-Q-0050` (`INITIAL_BATCH`, 40 items)
- Audit: `AUDIT-GPT-PHASE2-A-LEGAL-2026-08-13`
- Status: `FULLY_ADJUDICATED`
- Canonical question edits: 없음

## 결과

| Verdict | Count |
|---|---:|
| `KEEP` | 38 |
| `MINOR_EDIT` | 1 |
| `MAJOR_REWRITE` | 1 |
| `DELETE` | 0 |

모든 문항을 current official Massachusetts/Federal source로 독립 해결했다. SATA는 A–E 각각을 별도로 판정했고, drug item은 generic/brand, indication, federal schedule, Massachusetts schedule 및 scenario의 legal consequence를 확인했다.

## 수정 또는 재작성 필요

| Question | Verdict | Existing answer | Finding |
|---|---|---|---|
| `MA-Q-0021` | `MINOR_EDIT` | `YES` | 정답 A와 Schedule II patient-requested partial-fill 결론은 맞다. 다만 해설은 discontinued brand인 OPANA를 현재 brand token처럼 제시한다. FDA의 현행 자료는 OPANA와 OPANA ER이 discontinued 상태이며 generic oxymorphone 제품은 별도로 존재함을 구분한다. 이는 answer key가 아니라 drug fact의 시의성 결함이다. |
| `MA-Q-0033` | `MAJOR_REWRITE` | `PARTIALLY` | 21 CFR 1306.22(a)는 Schedule III/IV 처방을 issue date로부터 'more than six months' 후에는 refill할 수 없다고 규정한다. stem의 'reaches six months after issue'는 정확히 6개월째인지 6개월을 초과했는지 불명확하므로 C가 유일한 정답이라고 확정할 수 없다. |

## 암기 안전성

Legal content만 보면 `KEEP` 문항은 key가 맞지만, 별도 Realism audit가 Batch A 전 문항을 `FAIL`로 판정했다. 따라서 이 batch의 canonical wording/choice pattern을 그대로 암기해서는 안 된다.
