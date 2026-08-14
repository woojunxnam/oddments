# Phase 2 Batch B — Legal Audit

- Frozen head: `ffa43e0344c1c08c076bbdaac0323bd20dffefd0`
- Scope: `MA-Q-0051`–`MA-Q-0090` (`INITIAL_BATCH`, 40 items)
- Audit: `AUDIT-GPT-PHASE2-B-LEGAL-2026-08-13`
- Status: `FULLY_ADJUDICATED`
- Canonical question edits: 없음

## 결과

| Verdict | Count |
|---|---:|
| `KEEP` | 37 |
| `MINOR_EDIT` | 2 |
| `MAJOR_REWRITE` | 1 |
| `DELETE` | 0 |

모든 문항을 current official Massachusetts/Federal source로 독립 해결했다. SATA는 A–E 각각을 별도로 판정했고, drug item은 generic/brand, indication, federal schedule, Massachusetts schedule 및 scenario의 legal consequence를 확인했다.

## 수정 또는 재작성 필요

| Question | Verdict | Existing answer | Finding |
|---|---|---|---|
| `MA-Q-0067` | `MINOR_EDIT` | `PARTIALLY` | 21 CFR 1305.17(a)는 paper DEA Form 222를 다른 records와 별도로 보존하도록 요구한다. electronic Form 222 copies는 readily retrievable이면 별도 보존된 것으로 간주되지만, 선택지 B는 paper와 electronic 기준을 'separately or readily retrievable separately'로 합쳐 paper record에도 후자를 대안처럼 보이게 한다. stem의 general invoices는 paper record를 시사한다. |
| `MA-Q-0089` | `MAJOR_REWRITE` | `NO` | 247 CMR 15.03(1)은 discovery 시 patient/representative에 즉시 통지하고 directions를 제공하며, professionally indicated이면 prescriber에도 즉시 통지하도록 한다. 규정은 patient 통지와 prescriber 통지의 상대적 선후를 정하지 않는다. B의 risk assessment는 prudent practice이지만 해당 조항의 명시적 단계가 아니다. 따라서 B-D-A-C라는 유일한 total order는 법적 근거가 없다. |
| `MA-Q-0090` | `MINOR_EDIT` | `PARTIALLY` | B-D-A-C는 high-level planning sequence로는 방어 가능하다. 그러나 A는 patient-file transfer와 controlled-stock disposal/transfer라는 서로 다른 trigger와 timing의 의무를 하나로 묶는다. 247 CMR 6.13은 requested file transfer를 timely하게 처리하도록 하고, 6.13(6)/6.14의 stock disposition 및 post-closure attestation은 별도 절차다. 따라서 하나의 엄격한 chronological slot으로 시험하면 모호하다. |

## 암기 안전성

Legal content만 보면 `KEEP` 문항은 key가 맞지만, 별도 Realism audit가 Batch B 전 문항을 `FAIL`로 판정했다. 따라서 이 batch의 canonical wording/choice pattern을 그대로 암기해서는 안 된다.
