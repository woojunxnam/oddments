# Phase 2 GPT Audit Summary

- Frozen target: `feature/mpje-content-phase2 @ ffa43e0344c1c08c076bbdaac0323bd20dffefd0`
- Batch A: `MA-Q-0011`–`MA-Q-0050`
- Batch B: `MA-Q-0051`–`MA-Q-0090`
- Audit date: `2026-08-13`
- Canonical question edits: 없음

## Legal verdicts

| Verdict | Batch A | Batch B | Total |
|---|---:|---:|---:|
| `KEEP` | 38 | 37 | 75 |
| `MINOR_EDIT` | 1 | 2 | 3 |
| `MAJOR_REWRITE` | 1 | 1 | 2 |
| `DELETE` | 0 | 0 | 0 |

- Confirmed legal errors: 2 (`MA-Q-0067`, `MA-Q-0089`)
- Ambiguous items: 2 (`MA-Q-0033`, `MA-Q-0090`)
- Drug errors: 1 (`MA-Q-0021` — discontinued `OPANA` brand presentation)
- Authority problems: 0

## Realism verdicts

| Result | Batch A | Batch B | Total |
|---|---:|---:|---:|
| `PASS` | 0 | 0 | 0 |
| `FAIL` | 40 | 40 | 80 |
| `MINOR_EDIT` | 10 | 16 | 26 |
| `MAJOR_REWRITE` | 30 | 24 | 54 |

주된 원인은 52개 SBA의 unrelated generic distractor 반복, 26개 SATA의 고정 `A/C` key pattern, 2개 ORDERED_RESPONSE의 동일 `B-D-A-C` template 및 timing ambiguity다.

## 암기 금지 목록

- Legal content correction 전 특히 암기 금지: `MA-Q-0021`, `MA-Q-0033`, `MA-Q-0067`, `MA-Q-0089`, `MA-Q-0090`.
- Realism/release 관점에서 암기 금지: `MA-Q-0011`–`MA-Q-0090` 전체.

각 canonical JSON은 frozen question hash를 보존하며 `FULLY_ADJUDICATED`로 기록된다. 이 audit는 release 또는 merge 승인이 아니며, editor correction 후 changed hash에 대한 re-audit가 필요하다.

## Verification

- `python scripts/validate_all.py`: `0 error(s), 0 warning(s)`.
- `pytest`: `70 passed, 1 skipped, 1 failed`.
- 실패한 `tests/test_schemas.py::test_valid_question_fixture_passes_registry_validation`은 임시 단일-question fixture가 실제 `data/audits/`를 계속 읽어 80개 audit ID를 `unknown question ID`로 판정하는 기존 test-isolation 결함이다. Audit schema/content validation은 통과했으며, issue의 audit-outputs-only 범위를 지키기 위해 validator 또는 test는 변경하지 않았다.
