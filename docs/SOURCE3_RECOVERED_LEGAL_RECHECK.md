# 공식 원문을 회수한 3문항의 별도 법규 재감사

대상은 **MA-CASE-0785, MA-CASE-0786, MA-CASE-0790**뿐이다. 원 primary 보고서는
`independent-phase5-c-review.json`의 SHA
`b488a042566368b096240f6cd671bccee3bc9aba51347ecda8ee3c7db6e38f68`이며 세 원
record의 `NOT_ASSESSED/HOLD`와 정확한 출처 차단 사유를 그대로 보존한다. 별도
source3 consumer는 실제 보고서 전체 provenance, 원 row/current question SHA,
원 release 필드 존재·값, 원 expected-key 표현, exposure metadata와 저자 이력을
고정한다. 기존 9개 절차적 재감사 scope·상수·queue·검증 함수는 확장하지 않는다.

## 회수 자료의 범위

`remaining-source3-availability/source-only-report.json`의 원 SHA와 실제 정책·현재
공식 목록의 raw/text/meta/link SHA를 native scope에 결박한다. 이 문서는 자료 확보
사실만 기록하며 정답·법규 판정을 제공하지 않는다.

회수된 문서는 Board의 **Policy 2025-02: Definitions**, `Adopted: 8/7/25`다.
§I의 범위, §II.F(QRE), §II.H(Serious Disability), §II.I(Serious Injury)를 실제로
읽고 원문항의 모든 보기·극성·예외·주/연방 구분·한국어 해설과 대조한다. 현재
공식 CMR 2 PDF와 별개의 보충 정책이다. 정책을 정식 CMR 개정으로 표현하지 않는다.
`247-cmr-200-definitions-and-severability-0` PDF는 명시적 DRAFT이며 현행 규정으로
쓰지 않는다. 인쇄된 채택일을 별도 법적 시행일로 단정하지 않는다.

## Root의 실제 세션 확인과 등록

기존 실제 세션을 재사용할 수 있으나 이 세 문항의 저자·편집자·기존 판정자와
다른 실제 세션이어야 하고, 이 세 문항의 과거 결론이나 숨은 truth를 보지 않았는지
root가 실제로 확인한다. 기존 실제 actor/session/instance를 새 날짜나 이름으로
바꾸어 새 사람으로 세지 않는다. Root 작성 reviewer JSON에는 기존 계약의
actor_provenance, auditor, auditor_instance, known_author_ids,
controller_independence_basis에 다음을 추가한다.

- `target_question_ids`: 위 세 ID의 순서 있는 배열.
- `current_target_prior_conclusions_read: false`.
- `current_target_author_or_editor: false`.
- `new_independent_person_credit: 0`.

자동 결박된 원 actual actor/session은 `/root/independent_case_c`, instance는
`GPT:/root/independent_case_c:independent-legacy-20261103`이다. 원 저자 보고서는
`wave6-4-author-review.json`이며 실제 기록된 author_session `20261103-wave6-4`를
포함한다. Root·계약 engineer·원 판정자·원 저자/편집자를 native claim에서 제외한다.
문자열만으로 실제 독립성을 증명한다고 주장하지 않는다.

```bash
python scripts/prepare_source3_recovered_legal.py --actor /root \
  --reviewer "$actual_source3_reviewer_json" --output "$new_external_proposal"
```

prepare는 실제 HEAD에 결박된 원자료와 현재 hash를 검사하고 외부 proposal만
작성한다. 기존 native state가 있으면 실패하며 이를 초기화하지 않는다. Root가
proposal을 검토·커밋한 뒤 기존 `review_queue.py`의 independent-legacy stage와
명시적 `--state reports/full-corpus-review/source3-recovered-legal-work-queue.json`을
사용해 실제 CLAIM한다. Lease/token/heartbeat/recovery/재연결/순차 submit·integrate는
기존 native 구현을 그대로 사용한다.

실제 assignment를 `export_legacy_review_input.py`에 넘겨 원 stem·전체 보기·stored
key·한국어 core/각 choice analysis/learning boundary만 worker에 전달한다. 원
primary·저자 보고서·원 판정·숨은 truth를 worker에게 전달하지 않는다. 실제 CLAIM
전에는 정답 감사를 시작하지 않는다.

## Worker 계약과 검증

출력 prefix는 `reports/full-corpus-review/source3-independent/<actual-job-id>/`이며
`report.json`, `result.json`을 보존한다. 기존 9개 경로의 순수 `validate_legal`을
그대로 재사용하므로 [법규 record의 모든 기존 필드](REMAINING9_PROCEDURAL_RECHECK.md)를
충족해야 한다. source3의 PURPOSE/native binding·정확한 세 ID/current hash를 사용한다.
그 계약의 source나 판정 예시를 실제 사실로 복사하지 않는다.

추가로 report에는 `new_independent_people_credit`, `new_unique_original_question_credit`,
`new_realism_pass_credit`를 각각 정수 0으로 명시한다. 각 legal_review에는 정책/CMR의
종류와 적용 범위·한계를 설명하는 한국어 `source_scope_limitation_ko`가 필요하다.
각 authority와 그 metadata에는 같은 `source_kind`를 기록한다.

- 채택된 Board 정책: `OFFICIAL_ADOPTED_BOARD_POLICY_NOT_CMR`.
- 정식 규정: `OFFICIAL_REGULATION`.
- 법률: `OFFICIAL_STATUTE`.

Policy 2025-02의 정확한 공식 URL을 사용하면 실제 추출문에 정책 제목·인쇄된 채택일이
있고 DRAFT가 없어야 한다. CMR URL에 명시적 DRAFT가 있으면 정식 규정으로 통과하지
않는다. 실제 full document identity 확인은 별도 필수다. source_kind와 제목 확인만으로
문항 정답을 만들지 않는다.

모든 현재 보기별 한국어 판정, 원 option/rationale SHA, stored/independent key,
SATA 전체 조합·INCORRECT 극성·SBA 사례 적용, 원 해설 전체 검토와 공식 정부 자료의
raw/text/meta SHA가 필요하다. 실제 시작≤조회≤실독≤완료 및 CLAIM≤시작≤완료≤
native SUBMIT≤INTEGRATE를 검증한다. 날짜를 바꾸지 않고 자정을 넘기는 실제 검토를
허용하며 law_checked_date는 각 자료의 실제 read_at 날짜다.

KEEP/YES를 예측하지 않는다. NO, AMBIGUOUS, NOT_ASSESSED 또는 HOLD도 유효한 결과다.
출처·범위·추가 사실이 불명확하면 HOLD/blocker를 구체적으로 남긴다. 이 경로의
realism은 `NOT_ASSESSED` 및 기존 명시적 법규전용 blocker로 남기며 새 PASS를 만들지
않는다. 새 record는 `release_eligible: false`가 필수다.

Worker는 자기 prefix만 커밋하고 실제 전체 SHA로 envelope을 작성·push한다.
`queue.validate_result` 및 `source3_recovered_legal_metadata.validate_completed_report`로
실제 report와 retained-byte를 검사한다. Root는 별도로 원 worker SHA/HEAD/disk/
원격 일치와 source evidence를 확인한 후 native submit → cherry-pick → 원 envelope
raw binding → 순차 integrate를 실행한다.

## 집계와 보호

소비자는 INTEGRATED 상태와 세 native event, 원 envelope, 부모·현재 문항·저자·
자료 SHA를 모두 확인한 뒤 고유 current-hash 정답 판정만 합집합에 더한다. 원
primary HOLD·현실성·정답·본문·이력·기본 연습 제외는 그대로다. Canonical release,
새 고유 원문 수, 새 독립 인원, 새 realism PASS credit는 0이다.

새 negative는 기존 source-bound archive notice 경로로 안내하고 기존 previous_notices를
원형 보존한다. `supplementary_checkpoint_bindings`가 실제 성공한 committed-byte
trace를 source3에도 적용하므로 final16은 새로운 queue·회수 근거·보고서·자료를
정확히 결박한다. 기존 guard를 완화하지 않는다. 현재 후보의 validators·결정적
재생성·전체 pytest·exact-head CI·공개 검증을 별도로 완료해야 한다.
