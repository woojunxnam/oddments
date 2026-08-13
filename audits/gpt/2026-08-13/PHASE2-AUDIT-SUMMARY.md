# Phase 2 GPT independent REAUDIT summary

## 최종 audit 결론

| Review | KEEP | MINOR_EDIT | MAJOR_REWRITE | DELETE |
|---|---:|---:|---:|---:|
| `LEGAL_VERIFICATION` | 75 | 3 | 2 | 0 |
| `REALISM_REVIEW` | 29 | 27 | 24 | 0 |

- `REALISM_REVIEW`: `PASS` 29, `FAIL` 51
- frozen target: `repair/mpje-phase2-realism-v2` @ `67464e7a7ff2cfe88285c7c0f0f4164e92df46cd`
- branch: `audit/gpt-phase2-reaudit-v2`
- audit date: `2026-08-13`

## Confirmed legal errors

- `MA-Q-0043`: option B는 M.G.L. c. 94C, § 23의 permissive 90-day pathway를 source에 없는 mandatory-consideration duty로 바꾼다. 현재 key의 B 포함은 지지되지 않는다.
- `MA-Q-0081`: option B는 current 247 CMR 16.02(1)(c)의 five-year/grandfather/equivalent qualification을 생략해 new entrant에게 PharmD alone가 충분한 것처럼 읽힌다.

## Ambiguous items

- `MA-Q-0043`: 'may apply' stem과 'required to be considered' option이 서로 다른 legal modality를 사용한다.
- `MA-Q-0081`: statute shorthand와 stricter current promulgated regulation이 한 compound option에 섞여 있다.

## Realism failures

`MA-Q-0011`, `MA-Q-0013`, `MA-Q-0014`, `MA-Q-0016`, `MA-Q-0018`, `MA-Q-0019`, `MA-Q-0023`, `MA-Q-0025`, `MA-Q-0027`, `MA-Q-0028`, `MA-Q-0029`, `MA-Q-0031`, `MA-Q-0032`, `MA-Q-0034`, `MA-Q-0035`, `MA-Q-0036`, `MA-Q-0037`, `MA-Q-0038`, `MA-Q-0041`, `MA-Q-0042`, `MA-Q-0043`, `MA-Q-0044`, `MA-Q-0045`, `MA-Q-0046`, `MA-Q-0047`, `MA-Q-0048`, `MA-Q-0049`, `MA-Q-0050`, `MA-Q-0052`, `MA-Q-0054`, `MA-Q-0058`, `MA-Q-0066`, `MA-Q-0068`, `MA-Q-0073`, `MA-Q-0074`, `MA-Q-0075`, `MA-Q-0076`, `MA-Q-0077`, `MA-Q-0078`, `MA-Q-0079`, `MA-Q-0080`, `MA-Q-0081`, `MA-Q-0082`, `MA-Q-0083`, `MA-Q-0084`, `MA-Q-0085`, `MA-Q-0086`, `MA-Q-0087`, `MA-Q-0088`, `MA-Q-0089`, `MA-Q-0090`

핵심 원인은 18개의 malformed conditional distractor, 129개의 six-position SATA lead-in, 20-opener cycle, schedule-only flashcard, vague/tautological options이다.

## Drug errors

- `MA-Q-0024`: generic buprenorphine products는 current이나 `Subutex` NDA product는 discontinued이다. related fact는 current generic product와 discontinued legacy brand를 구분해야 한다.
- 그 밖의 39 drug-linked item은 current DailyMed labeling과 21 CFR Part 1308에서 indication·dosage form·schedule의 material mismatch를 확인하지 못했다. `MA-Q-0021`의 discontinued `OPANA` disclosure는 정확했다.

## Authority problems

- `MA-Q-0023`: explanation이 21 CFR 1306.11(d)의 7-day follow-up prescription deadline을 누락한다.
- `MA-Q-0058`: explanation이 1-business-day written notice와 45-calendar-day Form 106 completion을 분리하지 않는다.
- `MA-Q-0081`: statute alone shorthand로는 current 247 CMR 16.02 qualification을 충족하지 못한다.

## Unsafe-to-memorize IDs

Legal non-`KEEP` item은 교정 전 암기 금지로 분류했다: `MA-Q-0023`, `MA-Q-0024`, `MA-Q-0043`, `MA-Q-0058`, `MA-Q-0081`.

Realism `FAIL`은 legal conclusion이 맞는 경우에도 public MPJE-like writing exemplar로 암기하거나 재사용하면 안 된다.

## Frozen input and validation

- initial remote SHA check: `PASS` — `67464e7a7ff2cfe88285c7c0f0f4164e92df46cd`
- pre-publication remote SHA check: `PENDING`
- exact exported `question_hashes`: `PASS` — 네 frozen package에서 output으로 value-preserved
- `python scripts/validate_all.py`: `PASS` — `all: 0 error(s), 0 warning(s)`
- `python -m pytest -q`: `PASS` — `74 passed, 1 skipped in 3.07s`
- canonical question/rule/drug/style/release/validator/schema/test/generated-site edits: 없음

## Publication

- Draft PR: `PENDING`
- base: `repair/mpje-phase2-realism-v2`
- merge: 수행하지 않음
