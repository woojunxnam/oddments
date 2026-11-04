# GPT-FRESH-B3-PACKAGING-CONFLICT-V1 Evidence Note

## Scope and provenance

- Auditor instance: `GPT-FRESH-B3-PACKAGING-CONFLICT-V1`
- Review type: `LEGAL_VERIFICATION`
- Audit scope: `REAUDIT`
- Review date: `2026-08-20`
- Exact scope: `MA-Q-0169`, `MA-Q-0202`, `MA-Q-0203`
- Repository: `https://github.com/woojunxnam/oddments.git`
- Live base: `origin/main` at `c45a47c0d5be558f3017803e95a1367a38b4e5f9` after PR #113

이 기록은 이미 `RELEASED`인 문항에서 공식 authority와 canonical content 간 충돌이 발견되어 수행한 defect-triggered legal re-review다. Initial admission audit가 아니므로 Phase-1 blind lock을 만들거나 주장하지 않았다. Author/editor reasoning은 consult하지 않았고, 기존 audit/adjudication narrative도 substantive legal input으로 사용하지 않았다. `RELEASED`, `PASSED`, `KEEP` 같은 administrative status label만 기계적으로 기록했다. 판단 근거는 canonical question text/key, rule metadata와 아래 current official sources뿐이다.

## Current official authorities

1. Mass.gov regulation page: https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards
2. Current regulation PDF: https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download
3. Current Board resource list: https://www.mass.gov/lists/pharmacy-practice-resources
4. Current Policy 2023-01 PDF: https://www.mass.gov/doc/2023-01-compliance-packaging-and-reusable-dose-planners-pdf/download

Mass.gov의 247 CMR 9.00 page는 current version date를 `12/06/2024`로 표시한다. 연결된 PDF의 subject는 Mass. Register #1536을 식별하며, PDF p.6/CMR p.54의 247 CMR 9.08(3)(b)는 다음과 같다: “A licensee may not dispense Schedules II or III controlled substances in a multi-drug-single-dose package.”

현재 Policy 2023-01은 `Adopted: 4/6/23; revised: 11/2/23; 1/9/25`이다. 전체 4 pages를 확인했다. p.3 `Multi-Drug-Single-Dose Packaging`은 `Unless otherwise prohibited`를 전제로 60-day 및 PRN restrictions를 두지만 Schedule II/III maintenance allowance를 두지 않는다. 따라서 Policy는 247 CMR 9.08(3)(b)의 금지를 override하지 않는다.

## Exact canonical conflict

`data/rules/ma-compliance-packaging.json`의 `rule_summary`는 current Board policy가 qualifying Schedule II/III maintenance medication을 multi-drug-single-dose package에 허용한다고 단정한다. `MA-Q-0169`, `MA-Q-0202`, `MA-Q-0203`은 같은 allowance를 stem, key 또는 explanation의 핵심 전제로 사용한다. 이는 maintenance exception 없이 Schedule II/III를 금지하는 247 CMR 9.08(3)(b)와 정면으로 충돌한다.

영향은 다음과 같다.

- `MA-Q-0169`: key `B,C,D,E` 및 core reasoning이 current law와 불일치한다.
- `MA-Q-0202`: keyed `A,D,E`는 모두 Schedule II/III examples이므로 current law상 허용될 수 없다.
- `MA-Q-0203`: keyed `B`의 결론 `No`는 맞지만 rationale가 틀리고, `D`는 prohibition을 `all compliance packaging`으로 과도하게 확대하므로 fully correct choice가 없다.

## Mechanical repository evidence

| Artifact | `question_audit_hash` / rule `content_hash` | Git blob at live base | Current status |
|---|---|---|---|
| `MA-COMPLIANCE-PACKAGING` | `ba79ae42fa51d3af30f7a4aa109233a07c127cbd83334bcd7247db0c25ef55d1` | `c76d5f1fc6463c551b6c0e5b454d008a1a5a1ee5` | `CURRENT`; `OFFICIAL_POLICY_VERIFIED` |
| `MA-Q-0169` | `505770da1a192bc506905b2fe88ac8e6ac5425c8d04565c7d2d144cc25120539` | `621a01d8cbdd51ad489f245663fcbaf856ed93dc` | `RELEASED`; `PASSED`; final `KEEP` |
| `MA-Q-0202` | `a3c658d418f93ee9174a51fe68151bd47738fb529912efe5963be6169bca289a` | `c010282f4ab720b6ccd141498f1ef126f105ca60` | `RELEASED`; `PASSED`; final `KEEP` |
| `MA-Q-0203` | `a5f2a0ac6bcbc1296c833f40d80ff7cfd219f328611f0d3253227f72f8d81acd` | `9d9301ce461e1a679b70fead7b4df6b947af126c` | `RELEASED`; `PASSED`; final `KEEP` |

세 question은 모두 `verified_dependencies.rules.MA-COMPLIANCE-PACKAGING.content_hash`로 위의 stale rule hash를 고정한다. Exact rule ID/hash scan에서 `data/questions/`의 dependents는 이 세 문항만 확인됐다. Target files는 live base와 auditor worktree에서 byte-identical했고 audit 작성 전 clean이었다.

## Disposition

세 문항 모두 `MAJOR_REWRITE`, `Critical`, `Existing_Answer_Correct: NO`다. Controller는 현 상태의 release를 중단하고, rule과 문항을 247 CMR 9.08(3)(b)에 맞게 수정한 뒤 changed hashes에 대해 fresh legal evidence를 받아야 한다. 금지 범위는 `multi-drug-single-dose packaging`이며 모든 compliance packaging으로 확대해서는 안 된다.
