# 절차적 미판정 9문항의 실제 fresh 법규 재감사

이 경로는 `MA-EXP-0153..0160`, `MA-EXP-0823`만 대상으로 한다. 앞의 8개는
같은 실제 세션의 선행 current-hash 정답 판정, 나머지 1개는 숨은 truth 우발 노출로
원 판정이 `NOT_ASSESSED/HOLD`인 경우다. 부모 보고서·row·현재 문항·저자 기록의
실제 SHA는 `remaining9_procedural_metadata.py`에 고정한다. 다른 출처 차단·실질적
법적 모호성·편집 결함을 이 절차적 사유로 바꾸지 않는다.

원 primary 보고서·HOLD·정답·본문·이력·기존 현실성 판정은 바꾸지 않는다. 새
supplementary 판정은 고유한 current-hash 정답 판정 집계만 추가할 수 있다.
canonical RELEASED·새 원문 실독 인원·새 현실성 PASS·기본 연습 복귀 credit는 0이다.
새 `NO/AMBIGUOUS/NOT_ASSESSED/HOLD`도 허용하며, 불명확한 출처에서 YES를 만들지 않는다.

## Root 등록과 실제 배정

공유 queue는 root 단일 writer다. 실제 새 세션을 만든 후 actor/session·stable
auditor_instance·known_author_ids·controller_independence_basis를 JSON에 기록한다.
`actor_id==session_id`로 실제 세션 이름을 보존하며 vendor/인스턴스 문자열이
독립성 증명이라고 주장하지 않는다. 원 부모 2세션·root·계약 engineer·원 저자
session 및 실제 추가 저자/편집자와 겹치지 않는지 root가 확인한다. 자동 확인되는
저자 session은 `20261103-wave9-4`, `20261103-wave12-3`이며 추가 실제 이력도 조사한다.

```bash
python scripts/prepare_remaining9_procedural.py --actor /root \
  --reviewer "$actual_reviewer_json" --output "$new_external_proposal"
```

이 명령은 외부 proposal만 만든다. root는 실제 결과·원 SHA와 세션을 검토하고
`reports/full-corpus-review/remaining9-procedural-work-queue.json`에 보존·커밋한 뒤
기존 `review_queue.py --stage independent-legacy --state ... claim`을 실행한다.
별도 원 작업 branch/worktree를 사용하고 실제 lease·attempt·token·event를 보존한다.
동일한 native claim 재연결, heartbeat, expiry/recovery, submit idempotence와 순차
integration 규칙은 기존 `review_queue.py`를 그대로 사용한다. 새 queue 재등록으로
기존 claim/history를 지우지 않는다. prepare는 기존 state가 있으면 실패한다.

실제 claim assignment를 다음 기존 exporter에 전달한다.

```bash
python scripts/export_legacy_review_input.py --assignment "$actual_assignment" \
  --output "$actual_visible_packet"
```

Worker에는 이 visible packet·실제 native assignment·필요한 계약만 전달한다.
이전 보고서·저자 판정·`_statement_truth`는 전달하지 않는다. 원 stem, 보기 전부,
stored key, 한국어 core/각 choice analysis/learning boundary를 실제로 읽는다.

## Worker 보고서 계약

출력 prefix는 `reports/full-corpus-review/remaining9-independent/<actual-job-id>/`이며
보고서는 `report.json`, 제출 envelope은 `result.json`으로 보존한다. 현재 계약의
완전한 합성 예시는 `tests/test_remaining9_procedural_metadata.py`에 있다. 합성 예시의
시각·identity·source bytes·판정을 실제 보고서에 복사하지 않는다.

보고서에는 `stage: independent-legacy`, `purpose`(모듈의 PURPOSE), 실제
actor_provenance/auditor/auditor_instance, `independent_of_authors: true`,
`canonical_audit: false`, `canonical_release_credit: 0`, 전체 `question_hashes`가 필요하다.
`native_assignment_binding`은 실제 job_id/sequence/question_hashes/stage/worker/
worker_branch/attempt와 같아야 한다. `review_started_at`, `review_completed_at`은 실제
aware ISO timestamp이고 `reviewed_at`은 실제 완료일이다. 시작은 실제 CLAIM.at 이후다.

각 9개 record에는 실제 question_id/record_sha256/visible_content_sha256,
`release_eligible: false`, `legal_review`, `realism_review`가 필요하다. legal_review에는:

- `existing_answer_correct`: YES/NO/AMBIGUOUS/NOT_ASSESSED, `verdict`:
  KEEP/MINOR_EDIT/MAJOR_REWRITE/HOLD/DELETE, `stored_key`, `independently_expected_key`,
  실제 question_type과 CORRECT/INCORRECT polarity, 구체적 한국어 finding.
- `polarity_and_sata_combination_checked`, `exceptions_and_federal_state_scope_checked`는
  실제 검토했을 때만 true. `prior_conclusions_read`, `hidden_truth_read`는 실제 false여야 한다.
  노출됐다면 root에 보고하고 이 경로에서 정답 credit를 얻지 않는다.
- `original_explanation_review`: core_reasoning/learning_boundary의 원 UTF8 SHA,
  두 필드의 `*_read: true`, 한국어 finding, 모든 보기별 choice_rationales에 choice_id,
  실제 read, 원 rationale_sha256, 개별 한국어 finding.
- 모든 원 보기의 per_choice_findings: choice_id, 원 option_text_sha256,
  한국어 finding, proposition_supported(bool/null), selected_by_independent_polarity(bool),
  해당 정확한 official authority_refs. SATA는 전체 명제 truth와 INCORRECT 극성까지
  조합해야 한다. SBA는 사례 적용과 일반적 명제 truth를 구분해 하나의 정답을 설명한다.
- 불명확한 키는 명시적인 HOLD/blocker로 남기며 NOT_ASSESSED의 예상 key는 빈 배열이다.

이 경로는 법규 전용이다. `realism_review`는 verdict `NOT_ASSESSED`, blocker
`BOUND_LEGAL_ONLY_RETRY_PRESERVE_PRIMARY_REALISM`, 구체적인 한국어 범위 설명으로
원 현실성 판정 보존을 알린다. 새로운 PASS를 만들지 않는다.

각 authority에는 source_id, 정확한 Massachusetts/연방 공식 정부 HTTPS URL,
exact_section, effective_date_or_version_basis(확인 못한 시행일 한계 포함), 실제
law_checked_date, own-prefix raw_path/raw_sha256, text_path/text_sha256,
metadata_path/metadata_sha256이 필요하다. metadata에는 같은 official_url/raw/text 경로와
SHA, 실제 retrieved_at/read_at, status200, 실제 method, 실제 정본 해당 조항을 읽었을
때만 `document_identity_status: OFFICIAL_TARGET_PROVISIONS_DIRECTLY_READ`를 기록한다.
실제 시작≤조회≤실독≤완료 순서를 검증한다. law_checked_date는 해당 read_at의 실제
날짜다. 자정을 넘기는 실제 검토는 허용하며 조회·실독 시각을 다시 붙이지 않는다.
403·404·잘못된 locator는 시도 증거로 별도 보존하고 성공 authority로 사용하지 않는다.
출처를 못 확인하면 NOT_ASSESSED/HOLD와 구체적 blocker를 남긴다.

## 검증·제출·통합

Worker는 own-prefix만 커밋·push한 뒤 전체 40자리 worker SHA와 보고서 raw SHA를
native envelope에 기록한다. `queue.validate_result`와
`remaining9_procedural_metadata.validate_completed_report`를 실제 assignment/scope,
원 visible questions, 보고서와 실제 retained-byte reader로 검사한다. 뒤 함수는
순수한 보고서 검사이며 claim/submit/integrate나 PASS credit가 아니다.

Root는 worker commit의 raw/text/meta/report가 disk/HEAD와 같고 원격 exact SHA인지
검사한 뒤 native submit, 원 worker commit cherry-pick, 원 envelope raw bytes 결박
(`scope.result_envelope.path/raw_sha256`), native integrate를 순서대로 실행한다.
완료 후 consumer의 load_metadata가 부모·저자·현재 source·native 세 event·실제
claim 이후 chronology·원 envelope·raw/text/meta를 모두 확인해야 집계된다.

새 negative가 발견되면 기존 archive notice 경로가 legal verdict 또는 key-negative를
인식한다. `supplementary_checkpoint_bindings.validated_sources`가 실제 native9
consumer를 통해 report/Qhash/원 SHA를 검증한 후 negative source를 반환한다.
Root는 실제 새 이유와 현재 source만 안내하고 기존 previous_notices를 정확히 보존한다.
이 경로를 위해 ordinary 법규 guard나 protected publication guard를 완화하지 않는다.
최신 queue/결과는 같은 successful committed-byte read trace를 통해 final16 migration에
결박된다. 완료된 과거 PR의 QA를 새 후보 QA로 사용하지 않는다.
