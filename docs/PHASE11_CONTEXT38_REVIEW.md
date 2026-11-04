# D38의 집계 노출과 별도 fresh 검토

이 경로는 이전 체크포인트의 D40 집계가 새 full-history 세션에 전달되어,
명시된 두 예외를 제외한 38문항의 이전 positive 결론을 추론할 수 있었던 문제를
처리한다. 원 보고서의 실제 검토·판정·부정적 finding은 지우지 않는다. 작성자 검토,
노출된 재검토, 실제 fresh 독립 검토와 출시 승인을 서로 구분한다.

`scripts/phase11_context38_metadata.py`는 정확히 EXP0321–0360 중 0338/0339를
제외한 38개만 읽는다. 기존 CASE0401/0441 consumer 및 EXP0338/0339 consumer의
고정 범위와 계약은 변경하지 않는다. 새 고정 경로는 다음과 같다.

- State: `reports/full-corpus-review/phase11-context38-recheck-work-queue.json`
- Header: `phase11_context38_scope`
- Purpose: `FIXED_PHASE11_CONTEXT38_FRESH_SECONDARY_REVIEW_NO_RELEASE_OVERRIDE`
- Native job: `review-independent-legacy-phase11-context38-f2f730cb3b7befe7`
- 실제 새 actor/session: `/root/fresh_d_remaining38`
- Disclosure: `reports/full-corpus-review/resume-20261104/d38-aggregate-exposure-disclosure.json`

소비자는 커밋된 원 checkpoint의 고정 raw SHA, D의 38 KEEP/38 YES·두 예외,
실제 root의 `fork_turns_all` 노출 선언, aware 관찰 시각, 원 report SHA와
각 primary row SHA, 현재 question 객체·collection·assignment hash를 결박한다.
다른 primary finding, 다른 보고서, 임의 38개, 다른 reviewer나 추가 job은 거절한다.
Disclosure의 primary fresh credit과 canonical release credit은 정확히 정수0이다.

새 state가 있으면 `QUEUED`/`LEASED`/`SUBMITTED` 단계에서도 기존 38개의 key는
독립 fresh 정답 판정 집계에서 즉시 제외한다. 원문 실독 수는 그대로다.
`excluded_primary_key_ids`를 사용하는 합집합 helper는 **집계용 복사본**의 key만
NOT_ASSESSED로 처리하고, 원 primary row와 보고서 바이트는 수정하지 않는다.
실제 통합된 별도 fresh 결과 중 NOT_ASSESSED가 아닌 고유 ID만 다시 더한다.
HOLD·AMBIGUOUS도 판정 범위일 수 있으며 법규 PASS가 아니다.

`INTEGRATED` 결과는 원 native controller의 Git/lease/submit/integrate 검사를
통과해야 한다. 소비자는 현재 HEAD의 source·envelope·report 원바이트, 정확38 ID,
실제 actor/session·instance, native assignment 7필드, claim/submit/integrate event와
공식 authority의 raw·text SHA, 조항·검토일·효력일 또는 UNKNOWN 한계를 확인한다.
새 reviewer가 이전 결론에 노출되었다면 그 key는 다시 NOT_ASSESSED로 남는다.
그 row의 PASS도 fresh 현실성 집계에 넣지 않는다. 노출 disclosure를 보존한 채
queue만 삭제해 과거 38개의 credit를 복원하려는 상태 역시 거절한다.

각 원장 row의 `independent_legacy_primary_assessment_limitation`은 원 보고서·row
SHA와 disclosure binding을 남긴다. 실제 fresh 결과가 통합되면 해당 보충 보고서와
envelope 증거 참조를 추가한다. 원 primary의 KEEP/YES와 부정적 법규·현실성 판단,
저자 finding 및 사용자 기록은 그대로 보존한다. 이 경로의 fresh positive만으로
이 38문항을 기본 연습에 복귀시키거나 RELEASED로 승격할 수 없다.

현실성도 context38의 기존 PASS를 fresh PASS 수에서 제외한다. 실제 fresh PASS와
고유 ID 합집합을 계산하되, 원 primary FAIL과 충돌하는 새 PASS는 effective PASS로
승격하지 않는다. 새 PASS 원수·그중 보존된 FAIL과 충돌하는 수·제외한 기존 PASS 수를
별도로 기록하므로 실제 검토 결과를 숨기거나 이전 negative를 지우지 않는다.

Builder의 전체 정답 판정 수는 primary 및 세 별도 consumer의 고유 합집합이다.
기존 두 consumer의 개별 historical progress는 그대로 유지하며, 현재 전체 값은
`independent_legacy_supplementary_review`와
`independent_legacy_context38_supplementary_review`에서 제외 내역을 명시한다.
신원 문자열과 root의 노출 선언은 실제 세션 출처를 결박하는 진술이며 독립성을
수학적으로 인증한다고 표시하지 않는다.

```sh
python -m pytest -q tests/test_phase11_context38_metadata.py \
  tests/test_phase11_secondary_metadata.py tests/test_procedural_secondary_metadata.py
```

Synthetic fixture 통과와 실제 pending-source reader 검증은 fresh 법규 판정이나
전체 후보 QA·배포 완료 증거를 대신하지 않는다.
