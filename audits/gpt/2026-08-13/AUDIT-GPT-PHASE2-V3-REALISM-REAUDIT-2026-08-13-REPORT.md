# GPT Phase 2 v3 REALISM re-audit — 2026-08-13

## 결론

- 독립 검토 범위: frozen target `a3dd4cd9e0372dd4ff7c872a2ae3c3c851157363`의 changed 52 questions만 검토했다.
- 입력 검증: REALISM A `40`, REALISM B `12`; LEGAL scope와 정확히 같은 52 IDs이고 frozen hashes가 모두 일치했다.
- 판정: `PASS=21`, `FAIL=31`.
- edit verdict: `KEEP=21`, `MINOR_EDIT=11`, `MAJOR_REWRITE=20`, `DELETE=0`.
- `PASS`는 10 criteria가 모두 true인 경우에만 부여했다.

## 검토 기준과 비교 방법

[NABP current MPJE competency statements](https://nabp.pharmacy/programs/examinations/mpje/competency-statements/)의 prevailing-law application 목적과 [NABP sample-item access page](https://nabp.pharmacy/programs/examinations/mpje/take-the-mpje-exam/)의 selected-response format을 기준으로 삼았다. 각 문항을 full canonical bank 90 questions와 비교하여 drug-name substitution, deadline/count template, 동일 closure/EPCS family 반복을 별도로 확인했다. 비공개 시험문항은 사용하지 않았다.

## Failure groups

- clinical/product context: `MA-Q-0016`, `MA-Q-0045`
- refill/transfer repetition: `MA-Q-0032`, `MA-Q-0035`, `MA-Q-0036`, `MA-Q-0038`
- schedule/reporting checklist family: `MA-Q-0041`, `MA-Q-0042`, `MA-Q-0043`, `MA-Q-0044`, `MA-Q-0045`, `MA-Q-0046`, `MA-Q-0047`, `MA-Q-0048`, `MA-Q-0049`, `MA-Q-0050`
- closure repetition: `MA-Q-0073`, `MA-Q-0090`
- weak or guessable distractors / trivia: `MA-Q-0023`, `MA-Q-0029`, `MA-Q-0054`, `MA-Q-0066`, `MA-Q-0068`, `MA-Q-0076`, `MA-Q-0078`, `MA-Q-0079`, `MA-Q-0081`, `MA-Q-0082`, `MA-Q-0083`, `MA-Q-0084`, `MA-Q-0085`, `MA-Q-0086`

## Failed-criterion counts

- `jurisprudence_reasoning`: 1
- `practice_plausibility`: 2
- `authentic_distractors`: 18
- `wording_not_guessable`: 12
- `reasoning_not_trivia`: 20
- `natural_rule_combination`: 1
- `appropriate_drug_context`: 2
- `distinct_from_bank`: 15
- `not_schedule_flashcard`: 9

## `FAIL` IDs

`MA-Q-0016`, `MA-Q-0023`, `MA-Q-0029`, `MA-Q-0032`, `MA-Q-0035`, `MA-Q-0036`, `MA-Q-0038`, `MA-Q-0041`, `MA-Q-0042`, `MA-Q-0043`, `MA-Q-0044`, `MA-Q-0045`, `MA-Q-0046`, `MA-Q-0047`, `MA-Q-0048`, `MA-Q-0049`, `MA-Q-0050`, `MA-Q-0054`, `MA-Q-0066`, `MA-Q-0068`, `MA-Q-0073`, `MA-Q-0076`, `MA-Q-0078`, `MA-Q-0079`, `MA-Q-0081`, `MA-Q-0082`, `MA-Q-0083`, `MA-Q-0084`, `MA-Q-0085`, `MA-Q-0086`, `MA-Q-0090`

## Do not memorize / release-gate hold

LEGAL edit IDs와 REALISM `FAIL`의 합집합은 다음과 같다. 이 IDs는 현재 상태를 학습 정답으로 암기하거나 release-ready로 취급하면 안 된다.

`MA-Q-0014`, `MA-Q-0016`, `MA-Q-0018`, `MA-Q-0023`, `MA-Q-0029`, `MA-Q-0032`, `MA-Q-0035`, `MA-Q-0036`, `MA-Q-0038`, `MA-Q-0041`, `MA-Q-0042`, `MA-Q-0043`, `MA-Q-0044`, `MA-Q-0045`, `MA-Q-0046`, `MA-Q-0047`, `MA-Q-0048`, `MA-Q-0049`, `MA-Q-0050`, `MA-Q-0054`, `MA-Q-0066`, `MA-Q-0068`, `MA-Q-0073`, `MA-Q-0076`, `MA-Q-0078`, `MA-Q-0079`, `MA-Q-0081`, `MA-Q-0082`, `MA-Q-0083`, `MA-Q-0084`, `MA-Q-0085`, `MA-Q-0086`, `MA-Q-0090`

Canonical questions는 수정하지 않았고 audit findings만 기록했다.
