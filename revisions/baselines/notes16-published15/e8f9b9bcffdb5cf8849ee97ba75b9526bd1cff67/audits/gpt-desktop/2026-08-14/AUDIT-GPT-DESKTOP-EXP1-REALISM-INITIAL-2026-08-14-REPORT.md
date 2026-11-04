# GPT Independent Realism Review — Expansion Batch 1 (MA-Q-0091–MA-Q-0130)

## 결론

현 frozen content에서 `PASS`는 Q130 한 문항뿐이다. 나머지 39문항은 최소 한 criterion이 false이므로 전부 `FAIL`이다. Edit verdict는 `KEEP 1`, `MINOR_EDIT 4`, `MAJOR_REWRITE 35`다. 엄격한 KILL은 실패가 아니라 release 전에 문제를 차단한 성공으로 해석했다.

Canonical realism JSON은 `data/audits/AUDIT-GPT-DESKTOP-EXP1-REALISM-INITIAL-2026-08-14.json`이다.

## Frozen style dependency

- `profile_id`: `MPJE-MA-PRE2027`
- `content_version`: `1`
- `content_hash`: `293be8fdcd39af2255a22a0423b7123d5cfcf7c0e6c561872eb0ef04e745015c`
- Review date: `2026-08-14`

NABP는 current pre-2027 MPJE가 state와 federal law를 구분 없이 prevailing jurisdiction law에 적용하는 judgment를 평가한다고 설명한다. [NABP Competency Statements](https://nabp.pharmacy/programs/examinations/mpje/competency-statements/)의 public scope와 [NABP Sample Questions](https://nabp.pharmacy/wp-content/uploads/2020/07/MPJE-Sample-Questions.pdf)의 selected-response format만 style reference로 사용했다. Protected 또는 recalled exam content는 사용하지 않았다.

## 판정 원칙

`PASS`는 아래 10개 criterion이 모두 true일 때만 부여했다.

1. `jurisprudence_reasoning`
2. `practice_plausibility`
3. `authentic_distractors`
4. `wording_not_guessable`
5. `reasoning_not_trivia`
6. `natural_rule_combination`
7. `appropriate_drug_context`
8. `distinct_from_bank`
9. `not_schedule_flashcard`
10. `public_style_without_copying`

Difficulty target은 profile의 `difficulty_3 = 1`, `difficulty_4 = 2`, `difficulty_5 = 3` reasoning step을 적용했다. Choices 수를 reasoning step으로 세지 않았다. 동일 조문 문장을 여러 개 고르는 SATA는 실제 fact classification과 rule interaction이 없으면 3-step으로 인정하지 않았다.

## Full-bank 비교

Frozen canonical bank 130문항 전체를 읽고 Expansion 40문항을 기존 90문항과 비교했다. Stem token overlap, sequence similarity, `rule_ids`, `family_id`, topic, difficulty, answer-length balance 및 실제 decision path를 함께 점검했다.

24문항에서 `distinct_from_bank = false`였다. 대표적 중복은 다음과 같다.

| Expansion | 기존 문항 | 중복 핵심 |
|---|---|---|
| MA-Q-0099 | MA-Q-0081 | CDTM qualifications list |
| MA-Q-0101 | MA-Q-0084 | retail CDTM Schedule VI prescription copy duty |
| MA-Q-0102 | MA-Q-0083 | alprazolam을 이용한 retail CDTM controlled limit |
| MA-Q-0106 | MA-Q-0077 | no-preceptor intern supervision |
| MA-Q-0107 | MA-Q-0078 | 14-hour presence와 12-hour credit cap |
| MA-Q-0111 | MA-Q-0053 | Monday 3 p.m. QRE와 24-hour documentation |
| MA-Q-0114 | MA-Q-0055 | 18-month gap와 annual CQI education |
| MA-Q-0115 | MA-Q-0056 | serious injury와 seven-business-day report |
| MA-Q-0117 | MA-Q-0088 | error return, quarantine, no inventory return, disposal |
| MA-Q-0125 | MA-Q-0059 | first DEA activity와 initial inventory |
| MA-Q-0126 | MA-Q-0060 | biennial inventory interval |
| MA-Q-0128 | MA-Q-0063 | Schedule II procurement using Form 222/CSOS |
| MA-Q-0129 | MA-Q-0067 | Form 222 separate record treatment |

Topic overlap만으로 fail하지는 않았다. Q130은 MA-Q-0069/0070/0071과 disposal topic을 공유하지만 세 rule을 하나의 pharmacy-owned expired-stock decision으로 통합해 `distinct_from_bank = true`로 판단했다.

## 주요 계량 신호

False criterion 빈도는 다음과 같다.

| Criterion | False count |
|---|---:|
| `wording_not_guessable` | 38 |
| `authentic_distractors` | 35 |
| `reasoning_not_trivia` | 32 |
| `distinct_from_bank` | 24 |
| `practice_plausibility` | 10 |
| `jurisprudence_reasoning` | 9 |
| `natural_rule_combination` | 7 |
| `not_schedule_flashcard` | 1 |
| `appropriate_drug_context` | 0 |
| `public_style_without_copying` | 0 |

SBA에서 correct-choice 평균 글자 수와 incorrect-choice 평균 글자 수의 ratio가 특히 큰 예는 Q97 `1.95`, Q111 `1.85`, Q115 `1.95`, Q118 `2.13`, Q119 `2.90`, Q128 `1.87`이었다. 길이만으로 자동 fail하지는 않았지만, 정답이 유일하게 조건부·복합·정교하고 나머지 choices가 extreme이면 `wording_not_guessable = false`로 판정했다.

Difficulty 5인 Q99, Q112, Q113, Q120, Q123, Q127, Q129는 실제 3-step application 대신 qualification list, regulation list 또는 abstract concept recognition에 머물렀다. Q130만 pharmacy-owned stock 분류 → lawful disposition route → destruction/documentation의 독립 3-step을 충족했다.

## `PASS` item

### MA-Q-0130 — `KEEP` / `PASS`

Expired oxycodone가 patient return이 아니라 pharmacy-owned registered inventory라는 사실이 disposition rule을 정한다. Candidate는 reverse distributor transfer, on-site/caused destruction의 non-retrievable standard, Form 41 record를 분리해야 한다. Form 106과 ordinary trash는 purpose 및 destruction-standard 혼동이라는 실제 오개념을 반영한다. Correct choices도 모두 장문인 패턴이 아니어서 단순 length cue가 약하다.

## `MINOR_EDIT` items

| Question_ID | False criterion | 필요한 편집 |
|---|---|---|
| MA-Q-0092 | `authentic_distractors`, `wording_not_guessable` | every/only/automatically polarity를 제거하고 실제 conflict가 있는 choices로 교체 |
| MA-Q-0103 | `authentic_distractors`, `wording_not_guessable` | 정답 길이를 맞추고 plausible technician workflow distractor 추가 |
| MA-Q-0121 | `wording_not_guessable` | B의 복합 문장을 분산하고 다른 choices도 동일 정보 밀도로 조정 |
| MA-Q-0124 | `authentic_distractors`, `wording_not_guessable` | 실제 federal/state oral-prescription timing trap으로 distractor 교체 |

## `MAJOR_REWRITE` items

| Question_ID | 핵심 realism defect |
|---|---|
| MA-Q-0091 | weak/extreme distractors, long key, MA-Q-0086 overlap |
| MA-Q-0093 | statutory default restatement, weak distractors, MA-Q-0087 overlap |
| MA-Q-0094 | no concrete facts, exception list, implausible advertising/package choices |
| MA-Q-0095 | dosage-form authority recall, long composite key |
| MA-Q-0096 | no patient screening facts, abstract protocol list |
| MA-Q-0097 | long key and obvious Schedule II/community-ban distractors |
| MA-Q-0098 | immediate Q97 repetition plus one standing-order fact |
| MA-Q-0099 | MA-Q-0081 duplicate and difficulty-5 list recall |
| MA-Q-0100 | catch-all key E and MA-Q-0082 scope overlap |
| MA-Q-0101 | MA-Q-0084 duplicate 24-hour deadline recall |
| MA-Q-0102 | MA-Q-0083 alprazolam scenario repetition |
| MA-Q-0104 | answer exposed by stem; noncompetitive distractors |
| MA-Q-0105 | personnel category ambiguity prevents fair adjudication |
| MA-Q-0106 | MA-Q-0077 no-supervision repetition |
| MA-Q-0107 | exact MA-Q-0078 14/12-hour repetition |
| MA-Q-0108 | single numeric annual-distribution recall and length cue |
| MA-Q-0109 | MA-Q-0080 compounding CE repetition |
| MA-Q-0110 | abstract CQI purpose list; no QRE facts |
| MA-Q-0111 | MA-Q-0053 Monday/24-hour repetition |
| MA-Q-0112 | difficulty-5 action list; MA-Q-0052 overlap |
| MA-Q-0113 | difficulty-5 systems-factor list; MA-Q-0054 overlap |
| MA-Q-0114 | MA-Q-0055 18-month/annual repetition |
| MA-Q-0115 | MA-Q-0056 deadline repetition plus trigger imprecision |
| MA-Q-0116 | MA-Q-0057 five-year retention repetition |
| MA-Q-0117 | useful insulin context but MA-Q-0088 legal pathway repetition |
| MA-Q-0118 | exhaustive key is 2.13× longer; other choices extreme |
| MA-Q-0119 | direct retention trivia; key is 2.90× longer |
| MA-Q-0120 | circular “applicable requirements” choices and legal error |
| MA-Q-0122 | explicit Schedule VI definition flashcard |
| MA-Q-0123 | abstract exception list, difficulty mismatch, legal error |
| MA-Q-0125 | MA-Q-0059 initial-inventory duplicate |
| MA-Q-0126 | MA-Q-0060 biennial-inventory duplicate |
| MA-Q-0127 | direct regulation statements, not 3-step inventory application |
| MA-Q-0128 | MA-Q-0063 Form 222/CSOS duplicate |
| MA-Q-0129 | MA-Q-0067 Form 222 record overlap and difficulty mismatch |

각 문항의 10개 boolean과 상세 Notes는 realism JSON에 기록했다.

## Recommended remediation sequence

1. Q105, Q120, Q123의 legal defects를 먼저 수정한다.
2. Q115의 report trigger를 정밀하게 분리한다.
3. 기존 bank와 중복되는 24문항은 단순 wording change가 아니라 다른 decision path로 재설계한다.
4. Difficulty 5 문항은 stem fact가 최소 세 개의 독립 법적 판단을 실제로 요구하도록 바꾼다.
5. Extreme/absolute distractor와 유일한 장문 정답을 제거하고, 같은 rule의 인접 exception·wrong schedule·wrong professional scope를 사용한다.
6. 수정된 canonical hash에 대해 legal audit와 affected realism audit를 새로 수행한다.
