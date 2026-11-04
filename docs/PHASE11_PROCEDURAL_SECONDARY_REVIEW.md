# Phase11의 노출된 두 정답에 대한 별도 보충 검토

`scripts/phase11_secondary_metadata.py`는 정확히 `MA-EXP-0338`과
`MA-EXP-0339`만 읽는 추가 소비자다. 기존 `procedural_secondary_metadata.py`의
CASE0401/0441 계약·허용 범위는 변경하지 않는다. 공통 reader·source SHA·provenance
검사 helper만 재사용한다. 이 코드는 실제 보고서·배정·원장·공개 결과를 만들지 않는다.

고정 state는 `reports/full-corpus-review/phase11-procedural-recheck-work-queue.json`,
scope header는 `phase11_fresh_two_scope`이며 purpose는
`FIXED_PHASE11_TWO_PRIOR_EXPOSURE_SECONDARY_REVIEW_NO_RELEASE_OVERRIDE`다.
표준 independent-legacy 큐의 native claim/submit/integrate를 사용하되 단 하나의
job과 이 두 ID를 벗어난 state는 미통합 추가 job까지 전부 거절한다.

부모는 `reports/full-corpus-review/recovered-phase11-d-review.json`의 실제
`/root/recover_d_review` 세션이다. 두 row는 `HOLD`/`NOT_ASSESSED`, blocker
`PRIOR_CONCLUSION_EXPOSURE_REQUIRES_GENUINELY_FRESH_SESSION`와
`release_eligible: false`를 유지해야 한다. `independently_expected_key`는 미판정
빈 배열이고 `exposure_limitations.prior_item_conclusion_seen: true`,
`fresh_whole_key_credit: 0`도 그대로여야 한다. 다른 실질 법규 보류나 임의 미평가를
이 절차적 재검토로 재분류하지 못한다. Root는 각 `previous_evidence`에 다음을
실제 커밋 바이트로 결박한다.

- `report_path`, `report_sha256`: 위 부모 보고서와 raw SHA.
- `record_sha256`: 원 row 전체의 canonical SHA.
- `question_record_sha256`: 실제 현재 question 객체의 canonical SHA.
- `original_actor`: `/root/recover_d_review`.
- `reason`: `ROOT_ATTESTED_PRIOR_PROCEDURAL_EXPOSURE_NOT_A_SUBSTANTIVE_LEGAL_VERDICT`.

새 실제 세션은 `/root/fresh_two_keys`이며 actor와 session 모두 이 값이어야 한다.
`fresh_reviewer`와 `result_envelope`의 구조는 기존 bounded consumer runbook
[PROCEDURAL_SECONDARY_REVIEW.md](PROCEDURAL_SECONDARY_REVIEW.md)와 같다.
이름만으로 독립성을 입증한다고 하지 않는다. Root의 실제 fresh 세션·작성자 이력
확인이 필요하며 원 reviewer instance, known authors, 원문에 기록된 작성자 신원을
새 auditor로 사용할 수 없다.

`QUEUED`/`LEASED`/`SUBMITTED`는 보충 credit0이다. `INTEGRATED`일 때만 현재 HEAD에
커밋된 원 report/row/현재 question/envelope/fresh report/official raw·text SHA와
native claim·submit·integrate event를 확인한다. 실제 worker commit 검증은 원
controller에 유지하며 소비자는 shallow CI에서도 HEAD 바이트로 검증한다.
재노출된 fresh row는 `NOT_ASSESSED`를 유지하고 key credit를 얻지 못한다.

Builder는 원 primary legal/realism/history/HOLD를 그대로 두고
`independent_legacy_supplementary_assessment`에 별도 결과를 기록한다. 기본 연습
containment는 primary와 두 consumer의 결과 모두에 적용한다. 추가 KEEP는 원
negative를 덮거나 원문을 RELEASED로 승격하지 못한다.

원장 집계는 primary 및 두 별도 보충 consumer에서 정답을 평가한 **고유 ID 합집합**이다.
원문 실독 수는 primary의 고유 수를 유지하고 두 번 더하지 않는다. 기존
`independent_legacy_procedural_supplementary_review`는 원 bounded2의 값 그대로이며
새 `independent_legacy_phase11_supplementary_review`는 새 두 결과만 기록한다.
둘의 합집합은 `independent_legacy_supplementary_review`에 별도로 나타난다.
HOLD/AMBIGUOUS를 포함한 정답 판정 범위이며 법규 PASS나 canonical release 비율이 아니다.

```sh
python -m pytest -q tests/test_phase11_secondary_metadata.py \
  tests/test_procedural_secondary_metadata.py tests/test_legacy_independent_metadata.py \
  tests/test_review_queue.py tests/test_full_corpus_review.py
```

Fixture 통과는 실제 보고서·독립 법규 감사·배포 증거를 대체하지 않는다.
