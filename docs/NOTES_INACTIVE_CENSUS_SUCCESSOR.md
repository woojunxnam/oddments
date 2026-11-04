# 비활성 N1 본문의 census 누락 재감사

`INACTIVE_BODY_CENSUS_SUCCESSOR`는 이미 통합된 비활성 본문 감사의 census 누락만
보완하는 별도 controller purpose다. 기존 `CENSUS_ONLY_OMISSION_REASSESSMENT`의
실제 활성 본문 불변 검사는 바꾸지 않는다. `BODY_CORRECTION_REASSESSMENT`처럼
본문을 다시 수정하는 경로도 아니다. 이 구현은 source-only이며 실제 등록·claim·
본문 활성화·공개를 수행하지 않았다. Canonical/question/legal release credit는0이다.

범위는 정확히 C31의 `w3-a-3` N1 후보 `e082d197…`와 원24 census에서 E25로 가는
한 번의 successor다. 원 C31 job/report/envelope/digest, 원 body registration record,
24 claim JSON 전체,42 source 객체,23KEEP/011LEGAL_HOLD, 분류문장 omission SHA와
E packet15파일 raw SHA를 고정한다. 원24 claim 객체는 metadata까지 그대로이고
`NOTE-CENSUS-V2-W3-A-3-ADD-001`만 추가한다. 추가 의미·다른 본문·새 atom·원명제나
source 변경·원 negative 누락은 실패한다. E의 source-only 검토는 독립 PASS가 아니다.

E의 원 source commits `ee74466a…`와 `be8e5a82…`는 새 branch에 원바이트로 보존했다.
그 안의 `validate.py`는 당시 root ledger 등 과거 snapshot을 고정한 원 증거다.
현재의 합법적인 ledger annotation을 그 과거 바이트와 같다고 인증하지 않으며,
원 validator·handoff를 고쳐 현재 등록을 수행한 것처럼 바꾸지 않는다. 새 purpose는
원 packet bytes와 실제 C31, 실제 M 및 등록 시점의 별도 retained ledger를 검증한다.

## 실제 M과 비활성 후보를 따로 결박

Read-only preview는 다음과 같다. 미래 version record나 job을 만들지 않는다.

```sh
python scripts/note_review_queue.py preview-inactive-census
```

실제 활성 M semantic `e1519c02…`, 해당 절의 원 body `16124c09…`와 현재 binding을
유지한다. 새 E25를 공개 ledger에 선택하지 않는다. Preview는 현재 credit0,
HOLD·daily 제외와 실제 source/parent bindings를 반환한다. 다른305절의 등록 당시
claim binding은 실제 M ledger snapshot으로 결박한다. 이 좁은 successor 검토 동안
그 binding이 바뀌면 자동 수용하지 않는다. 별도 실제 근거와 새 bounded 검토가 필요하며
원 record/snapshot을 덮어써서 통과시키지 않는다. Native 독립 annotation만 추가되는
것은 이 author/body binding을 바꾸지 않는다.

등록 record는 실제 활성 M snapshot과 비활성 N1 parent를 동시에 명시한다.
`notes_revision`은 기존 candidate-origin ID를 그대로 사용하며 미래 active N1의
revision·ledger hash를 추측하지 않는다. Record의 `inactive: true`와
`publication_blocker: ROOT_SEPARATE_16_FROM_ACTUALLY_PUBLISHED_15_SNAPSHOT`은 필수다.

## Root의 실행 순서

1. 진행 중인 모든 native note job을 실제 순차 통합한다. 현재 후속32/33 같은
   LEASED job이 있으면 새 등록은 실패하며 새 sequence를 미리 가정하지 않는다.
2. Root controller worktree에서 실제 `notes-unit-ledger.jsonl` 원바이트를 새
   `reports/full-corpus-review/body-corrections/w3-a-3-v1/inactive-census-successor/`
   아래 고유한 immutable snapshot 경로로 복사하고 커밋한다. 다른305 binding과
   현재 target M binding이 실제 inventory와 일치해야 한다.
3. Read-only 제안 helper로 실제 record를 만든다. 명령 출력만으로 등록되지 않는다.

   ```sh
   python scripts/note_review_queue.py propose-inactive-census \
     --id ACTUAL_UNIQUE_INACTIVE_RECORD_ID \
     --ledger-snapshot reports/full-corpus-review/body-corrections/w3-a-3-v1/inactive-census-successor/ACTUAL-M-LEDGER.jsonl
   ```

   결과는 전용 prefix의 새 JSON record로 보존·검토·커밋한다. Helper는 실제
   HEAD-retained snapshot만 읽으며 미래 active N1 version을 생성하지 않는다.
4. 기존 root-only checkpoint로 append 등록한다.

   ```sh
   python scripts/note_review_queue.py --actor /root reassess-inactive-census \
     --record reports/full-corpus-review/body-corrections/w3-a-3-v1/inactive-census-successor/ACTUAL-RECORD.json
   ```

   Queue에 새 purpose와 정확한 binding/author/negative/review 계약을 append한다.
   같은 path·bytes는 멱등적이고 다른 bytes·복제 등록·동시 미완료 wave는 거부한다.
   실패한 명령은 기존 atomic checkpoint를 쓰지 않는다.
5. 원 runbook의 claim/worktree/heartbeat/recover/submit/integrate를 그대로 사용한다.
   R/E와 원 body/source 작성자, C31의 실제 parent reviewer 세션은 새 fresh reviewer로
   재사용할 수 없다. Root가 실제 새 non-author 세션을 지정하고 기존
   controller-attested provenance를 유지한다. Identity 문자열 자체를 인증으로 과장하지 않는다.
6. Worker는 정확한 비활성 body 전문과25개 claim, 원24 객체와42 sources 보존,
   C31 원 omission·011 blocker·원19/24 negative 이력, 관련 derived 입력 및 직접 관련
   question 연결을 실제로 다시 읽는다. 새 authority는 exact section/HTTPS URL,
   시행일 또는 미확정 한계, 실제 retrieval/read/review date와 raw SHA를 남긴다.
   `related_question_ids: []`는 미평가이며 관련 없음의 증거가 아니다.
7. Worker는 기존 허용 evidence 경로만 commit한다. 실제 HEAD 후 envelope를 만들고
   root가 submit→증거 cherry-pick→원 envelope bytes commit→순차 integrate한다.
   Old worker Git 검사는 controller에 유지하고 HEAD-only 공개 reader만 old Git-free다.

## 새 report 계약과 credit

각 row는 기존 note report 전부와 `actual_body_sha256`, 실제 `reviewed_at`, 아래
object 및 각 원 omission의 `original_omission_reassessments`를 가진다.

```python
row['inactive_census_successor_review'] = {
    **job['inactive_census_successor_review'],
    'final_candidate_body_read_completely': True,
    'final_census_read_completely': True,
    'all_original_omissions_reassessed': True,
    'all_original_propositions_preserved': True,
    'all_derived_inputs_read_completely': True,
    'no_current_credit_before_matching_active_binding': True,
}
```

실제로 하지 않은 읽음을 true로 만들지 않는다. 원 omission의 exact SHA별로 실제
finding과 `RESOLVED_BY_FRESH_COMPLETE_BODY_CENSUS_REVIEW` 또는
`UNRESOLVED_REMAINS_OMISSION`을 기록한다. 미해소 원 omission은 현재 omissions에도
남기며 새 누락은 별도로 더한다. KEEP claim의 실제 official source provenance는
BODY review와 같은 LIVE/SAME_DAY_RETAINED_CACHE, HTTP200 문서 정체, 원 payload SHA와
날짜 순서를 검증한다. Access page/403은 증거가 아니다.

011 등 `job.carried_legal_blockers`는 원 finding/blocker/report SHA 및 상속 이력까지
정확히 보존한다. 동일 문장의 HOLD를 새 positive 의견으로 해제할 수 없다.
24개의 과거 KEEP/HOLD도 새25 census에 대한 전수 fresh 검토를 대신하지 않는다.
COMPLETE와 LEGAL_HOLD는 공존하며 새 누락이 있으면 OMISSIONS_FOUND다.

등록·LEASED·SUBMITTED와 실제 M이 활성인 INTEGRATED 결과 모두 현재 completeness/
author/legal/release credit0이다. Metadata는 후보 검토와 원 history를 보존하고
`current_review_valid: false`, HOLD, daily 제외를 유지한다. 새 author census는
M의 선택 census/count에 추가하지 않는다. 실제로 외부16 guard가 N1을 활성화하고
latest25 body+census+claim binding과 통합 결과가 모두 일치할 때만 최신 하나의
처리 coverage를 계산할 수 있다. 그때도011HOLD와 `coverage_is_legal_pass: false`,
canonical/question credit0은 그대로다. Stale N1/24나 부분 binding은 허용하지 않는다.

## 공개 blocker와 검증

이 구현에는 N1 활성화 writer나16 manifest가 없다. 아직 미공개15에 섞지 않는다.
실제15 공개 snapshot의 고정 검증 closure를 확보한 뒤 별도16 held-note activation,
원14/15 guards,1781 보호, derived·daily·현재 source/metadata/fullQA를 검증해야 한다.
기존 positive-only activation을 HOLD 통과용으로 완화하지 않는다.

```sh
python -m pytest -q tests/test_notes_inactive_census_successor.py \
  tests/test_notes_body_reassessment.py tests/test_notes_census_reassessment.py \
  tests/test_note_review_queue.py tests/test_notes_independent_metadata.py
```

테스트의 parent/body/census/authority·HTTP와 미래16 activation은 명시적 synthetic
fixture다. 실제 registry 등록·독립 법규 검토·현재 coverage·출시 증거로 세지 않는다.
