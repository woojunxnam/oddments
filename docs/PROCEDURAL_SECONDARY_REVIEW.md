# 고정된 두 절차 재검토의 read-only 소비

`scripts/procedural_secondary_metadata.py`는 `MA-CASE-0401`과 `MA-CASE-0441`의
보충 독립 결과만 읽는다. 원래 E/F 보고서의 절차적 노출·NOT_ASSESSED/HOLD와
모든 기존 primary 부정 판정은 그대로 보존한다. 이 문서와 원래 판정은 fresh
감사자의 입력 packet이 아니다. 도구는 새 배정·원문·보고서·queue를 작성하지 않는다.

표준 `review_queue.py --stage independent-legacy --state
reports/full-corpus-review/procedural-recheck-work-queue.json`의 기존
lease/recovery/submit/integrate를 그대로 사용한다. 공통 controller의 검사나
canonical release 정책을 바꾸지 않는다. 별도 state를 일반 `plan`으로 확장해도
소비자는 **job 하나와 exact 두 ID**를 벗어나는 전체 state를 거부한다. 추가 job이
미통합이어도 거부하며 예상 밖 작업에는 credit를 주지 않는다.

## 고정 범위와 독립성 binding

`procedural_recheck_scope`의 version/purpose/root와 exact IDs를 검사하고 각
`previous_evidence`가 지정된 원래 E/F 보고서 경로·actor·절차 blocker를 가리키는지
확인한다. 원래 report raw SHA, 해당 row canonical SHA, question canonical record
SHA를 검증한다. 다른 NOT_ASSESSED나 실질 법규 HOLD를 절차적 사유로 재분류할 수 없다.
현재 primary row는 원래 보고서 row 전체와 같아야 한다. 실제 질문 collection도
HEAD에 커밋된 바이트이고 현재 객체가 원래 hash와 같아야 한다.

Root는 고정 실제 fresh task에 다음 정보를 header로 등록한다. 문자열은 실제
root 배정 선언을 결박하며 독립 신원의 수학적 증명으로 표시하지 않는다.

```json
"fresh_reviewer": {
  "actor_provenance": {
    "actor_id": "/root/independent_procedural_retry",
    "session_id": "/root/independent_procedural_retry"
  },
  "auditor": "GPT",
  "auditor_instance": "실제 안정된 instance label",
  "controller_independence_basis": "실제 새 fork_none 세션과 작성 이력 확인 근거",
  "known_author_ids": ["알려진 실제 author/editor actor 또는 session 별칭"]
},
"result_envelope": {
  "path": "reports/full-corpus-review/보존한-result-envelope.json",
  "raw_sha256": "실제 envelope 원바이트 SHA"
}
```

고정 actor/session, 원래 E/F actor 제외, 알려진 author/editor 제외와 lease worker를
검사한다. Header는 핵심 actor/session을 결박하고, report와 result의 전체 provenance는
표준 controller 검사를 통해 정확히 같아야 한다. 설명용 `identity_basis` 같은
추가 provenance는 actor나 session을 바꿀 수 없다. 날짜·instance를 새 날짜로 소급
교체하지 않는다.

## 통합·바이트 증거

QUEUED/LEASED/SUBMITTED 결과는 새 credit 0이며 fresh report를 읽지 않는다.
INTEGRATED 결과만 다음을 모두 검증한다.

- 현재 HEAD의 queue/header, original reports, 실제 question collection,
  result envelope, fresh report와 연결된 source/evidence 원바이트.
- 고정한 envelope raw SHA와 `job.result`의 정확한 JSON 일치. 표준 SUBMIT event의
  canonical result SHA, CLAIM worker/attempt, INTEGRATE commit/event 일치.
- 정확한 40자리 worker commit, attempt branch label, root에 등록한 actor/session/instance.
- 단일 report의 exact 두 ID와 현재 hashes. 각 공식 authority의 HTTPS URL·section·
  review date·evidence raw binding, raw payload와 extracted text의 개별 path/hash.
- Report의 canonical audit false/credit 0, record의 release_eligible false.
  표준 envelope는 canonical 필드가 없을 수 있으나 명시한 positive release claim은 거부한다.

공통 controller가 수행한 실제 worker Git object와 통합 검사는 그대로 남는다.
소비자는 HEAD의 커밋된 파일과 캡처된 SHA를 읽으므로 shallow CI에 옛 worker
branch/object가 없어도 동작한다. 이를 새 신원 인증이나 법규 PASS로 과장하지 않는다.
공개 저장하지 않은 vendor style payload는 로컬 임시 경로를 raw 검증했다고 하지
않으며, 저장한 자체 memo의 바이트만 검증한다. 법규 authority의 바이트는 필수다.

## 공개 원장과 진행률

`build_full_corpus_review.py`는 별도
`independent_legacy_supplementary_assessment`에 fresh record, parent bindings,
report/envelope SHA, actor 정보를 남긴다. 기존
`independent_legacy_legal_assessment`와 `independent_legacy_realism_assessment`,
primary blocker·disposition·history는 새 KEEP로 덮지 않는다. 기존 부정 판정의
보류 해제·기본 목록 복귀·unchanged current-hash RELEASE_REQUIRED 해제·canonical
credit를 만드는 경로는 없다. 기본 containment 검사는 원래 결과와 보충 결과를
함께 확인하며 원문 수정 없이 기존 부정 결과를 override하지 않는다.

유효 key-assessed 수는 primary에서 NOT_ASSESSED가 아닌 고유 IDs와 유효 통합
보충 결과에서 NOT_ASSESSED가 아닌 IDs의 합집합이다. HOLD·AMBIGUOUS도 평가
범위일 수 있으며 법규 PASS가 아니다. 보충도 NOT_ASSESSED면 새 key credit는 0이다.
원문 읽음은 primary의 고유 ID 수로 유지하여 두 번 더하지 않는다. 실제 records로
계산하며 과거의 특정 원문 수·미평가 수를 상수로 두지 않는다.

`independent_legacy_procedural_supplementary_review`는 primary 수, 보충 기여,
현재 유효 assessed/unassessed 수와 보충 legal verdict 분포를 분리한다.
공개 quality report도 원래 HOLD/FAIL 보존과 법규 PASS·release 승인이 아님을 밝힌다.
보충 통합이 없는 상태에서는 기존 생성 출력이 바뀌지 않는다.

## Root 통합과 확인

1. 구현 commit만 cherry-pick한다. 실제 source/report/state는 root가 별도로 통합·보존한다.
2. 실제 fresh reviewer와 envelope bindings를 포함한 custom queue를 커밋한다.
   공통 controller의 submit/integrate를 생략하지 않는다.
3. 기존 artifact 재생성 절차를 실행한다. 모든 primary 부정 판정과 보충 record가
   별도 필드에 남고, key-assessed 기여·고유 원문 수가 실제 records와 같은지 확인한다.
4. 기존 canonical/default/보호/전체 QA 절차를 수행한다. 이 engineering commit은
   실제 보고서·원문·queue·생성물·거버넌스를 수정하지 않는다.

```sh
python -m pytest -q tests/test_procedural_secondary_metadata.py tests/test_legacy_independent_metadata.py tests/test_review_queue.py tests/test_full_corpus_review.py
```
