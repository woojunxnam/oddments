# Question Authoring Standard

## Source-first independent authoring

1. `docs/SOURCE_USE_POLICY.md`에 따라 source class와 permissions를 확정합니다.
2. Official source에서 controlling rule을 검증하고 exact section·URL·date를 기록합니다.
3. Material drug consequence가 있으면 source rule IDs와 verified dependency snapshot을 기록합니다.
4. 허용된 Class B research가 있다면 source text가 아닌 abstract signal만 저장합니다.
5. Official rule에서 fresh scenario와 fresh distractors를 독립적으로 설계합니다.
6. `question_family_matrix.json`에서 family cap과 중복을 확인합니다.
7. Automated QA, GPT legal audit, Claude legal audit, independent `REALISM_REVIEW`, final human/editor `KEEP` 전에는 `AUDIT_PENDING`을 유지합니다.

Raw-source question -> paraphrase -> public question 변환은 금지됩니다.

## Item contract

- `SBA`: 정확히 1개 answer
- `SATA`: 최소 1개 answer; zero-answer design은 schema 차원에서 불가능
- `ORDERED_RESPONSE`: 모든 choice를 정확히 한 번 사용한 unique complete order
- “정답 없음”을 의도하면 `None of the above.` 같은 explicit choice를 사용
- 모든 choice에는 서로 다른 rationale 필요
- stem에는 판단에 필요한 사실만 포함
- `always`, `never`, `only`, `all`, `none`은 법적 필요 없이 giveaway로 사용하지 않음
- correct option만 길거나 qualified하게 만들지 않음

## Difficulty and realism

- `3`: 의미 있는 legal determination 1개
- `4`: 연결된 determination 2개 또는 realistic exception/interaction
- `5`: 통상 3개 이상의 distinct reasoning steps; schema도 최소 3개를 요구

Realism은 문장 복제 정도가 아니라 jurisprudence reasoning의 종류로 평가합니다. 높은 score는 plausible practice scenario, genuine legal confusion 기반 distractor, federal-state interaction, competing deadlines, exceptions, personnel scope, natural multi-rule application에서 나옵니다.

Realism metadata는 question JSON에 기록하지 않습니다. Canonical `REALISM_REVIEW` audit가 current question hash, exact style-profile version/hash, criteria, reviewer/auditor, date를 단일 source of truth로 보존합니다. Derived website metadata도 이 audit에서 생성합니다.

Question family는 matrix에 먼저 계획할 수 있으며 `current_candidate_count: 0`, `current_released_count: 0`을 가질 수 있습니다. Candidate를 final cap보다 많이 연구할 수 있지만 released count는 `max_questions_in_final_bank`를 넘을 수 없습니다.

## Familiarity target

다음 구조를 반복 학습하게 합니다.

- realistic stem structure와 distractor logic
- federal-vs-Massachusetts conflicts
- generic/brand recognition이 법적 판단에 실제로 필요한 경우
- deadlines와 competing clocks
- exceptions와 personnel-scope distinctions
- multi-step legal application
- mixed-subject mock exams와 timed 120-question simulation

목표는 새 MPJE question의 decision structure가 익숙해지는 것입니다. Protected question을 사실상 미리 보게 만드는 것이 아닙니다.

## Prohibited content

Pre-MPJE content, recalled/leaked/NDA-protected items, exam dumps, screenshots/transcriptions, unlicensed commercial text, close paraphrases, embeddings와 그 derived questions는 canonical pipeline에 들어갈 수 없습니다.
