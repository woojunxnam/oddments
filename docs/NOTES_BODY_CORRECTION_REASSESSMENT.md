# 비활성 본문 교정 후보의 새 독립 재감사

`BODY_CORRECTION_REASSESSMENT`는 실제 법적 문장이 바뀌는 경우에만 쓰는 별도
purpose다. [기존 census-only 경로](NOTES_CENSUS_REASSESSMENT.md)의 본문 변경 금지와
기존 법규 HOLD·SOURCE_BLOCKED 해소 금지는 그대로다. 기존 경로의 예외가 아니다.
이 구현은 후보를 등록·배정·검토할 수 있게 하지만 활성 본문을 바꾸거나 공개를
승인하지 않는다. Canonical/question credit는 항상 0이다.

## 고정하는 원본과 실제 delta

먼저 저자가 새 경로에 단일 unit의 비활성 versioned body와 최종 author census를
작성한다. `record.json`은 정확한 통합 parent job digest, 원 body/census/unit/claim
binding, 원 report·envelope raw SHA, 원 ledger fields와 full body snapshot을 결박한다.
Parent job과 모든 해당 event의 snapshot, 원 census JSON, 원 report·envelope는
현재 HEAD의 보존 파일로 읽는다. 기존 파일을 고치거나 옛 판정을 새 본문에 옮기지 않는다.
원 body의 `independent_content_review`는 후보에서 제거하며 원 snapshot에만 남긴다.

모든 원 claim ID는 중복 없이 새 claim에 대응한다. 새 ID도 정확히 열거한다.
`edit_spans`의 원문·수정문과 각각의 raw SHA를 적용한 결과가 새 전문과 정확히
같아야 한다. 변경 claim은 실제 수정 span에 있는 새 문장이어야 한다. 공백·명시적 source
확인 날짜만 바뀐 본문, 같은 명제의 ID 변경, 누락 mapping, 범위 밖 unit 수정은 거부한다.
법의 효력일·업무 기한은 명제이므로 source metadata처럼 지우지 않는다.
이 문자열 검사는 법적 의미의 충분성을 인증하지 않는다. 실제 reviewer가 별도로 판단한다.
등록 시 원 snapshot과 현재 선택 unit 전체가 같고, 나머지 unit 전체와 claim binding의
fingerprint도 같아야 한다. 이후 다른 명시적 version의 등록까지 과거 snapshot에 묶지는 않는다.
후보 작성 후 다른 unit의 합법적인 census version이 먼저 선택됐다면 원 record를 덮어쓰거나
검사를 생략하지 않는다. Root가 최신 inventory를 확인하고 새 immutable registration
record 경로·ID와 나머지-unit fingerprint를 재결박해야 한다. 원 후보·원 record는 보존한다.

바뀌지 않은 명제의 원 `LEGAL_HOLD`·`SOURCE_BLOCKED`는 finding, blocker,
원 report SHA, 더 오래된 inherited blockers까지 정확히 `carried_legal_blockers`로 남긴다.
HOLD는 HOLD로, BLOCKED는 BLOCKED 또는 HOLD로만 제출할 수 있다. 본문 일부가
바뀌었다는 이유로 다른 명제의 negative를 해소하지 못한다.

실제 수정된 명제의 negative만 `reconsidered_legal_negatives`로 분리한다. 새 독립
reviewer가 원 negative 전체, 수정 span과 새 명제를 명시적으로 재판단해야 한다.
같은 body/statement hash에 새 긍정 판정을 붙이는 경로는 없다. 과거 body hash의 재등장과
과거 negative의 원문 명제를 변경 claim으로 재도입하는 등록도 거부한다. 저자의 source 확인,
날짜 변경, 저자 census의 COMPLETE 열거 상태는 독립 법규 PASS가 아니다.

## Root와 worker의 순서

1. 저자가 원본 archive, 새 body/census, mapping, 실제 primary retrieval/raw SHA,
   관련 study/card의 실제 입력·후보 source hashes를 먼저 커밋한다. 새 본문은
   `notes_revision.PATHS`, active/default notes 또는 published export에 넣지 않는다.
2. Root는 현재 note wave를 통합한 뒤 원본·새 후보·parent를 확인한다. Read-only preview:

   ```sh
   python scripts/note_review_queue.py --root /ABS/CONTROLLER preview-body \
     --record reports/full-corpus-review/body-corrections/UNIT-VERSION/record.json
   ```

   Preview는 원장·본문·생성물을 쓰지 않으며 `inactive`, `LEGAL_HOLD`,
   `current_review_valid: false`, `daily_eligible: false`, credit 0을 반환한다.

3. Controller의 기존 root-only checkpoint로 등록하고 원장 바이트를 커밋한다.

   ```sh
   python scripts/note_review_queue.py --root /ABS/CONTROLLER --actor /root reassess-body \
     --record reports/full-corpus-review/body-corrections/UNIT-VERSION/record.json
   ```

   새 `body_reassessments` entry와 한 unit job을 append한다. 같은 경로·바이트 재등록은
   멱등적이다. 복제 job, 다른 purpose 혼합, 가장 최근 parent가 아닌 등록, 진행 중 wave에
   무단 추가는 실패한다. 서로 다른 unit의 최초 QUEUED/attempt0 후보는 함께 등록할 수 있다.
   같은 unit의 다음 body 후보는 이전 후보가 실제 활성 binding이 된 뒤에만 새 parent가 된다.

4. 기존 [독립 notes runbook](INDEPENDENT_NOTES_REVIEW_RUNBOOK.md)의 `claim`, `worktree`,
   heartbeat/recover, submit, evidence cherry-pick, envelope 원바이트 commit, 순차 integrate를
   그대로 쓴다. Stage는 `independent-notes`, job purpose는 `BODY_CORRECTION_REASSESSMENT`다.
   후보 body/census 저자와 원 body/source 저자의 actor/session/instance는 claim할 수 없다.
   알려지지 않은 별칭은 root가 기존 `--known-author`로 등록한다. 문자열 provenance는
   실제 controller의 attestation이며 외부 신원 인증을 주장하지 않는다.
5. Worker는 job이 지정한 inactive revision 전문, 최종 census의 모든 claim, 원 negative와
   원 omissions, 관련 derived 입력 전체를 직접 읽는다. Active body가 아직 원본인 것은
   정상이다. Census-only 경로처럼 inactive body를 공개 ledger로 먼저 선택하지 않는다.
   Worker의 쓰기 범위는 기존 `reports/full-corpus-review/independent-notes/`뿐이다.
   본문·census·원장·기존 보고서를 worker가 수정하지 않는다.

등록 즉시 old KEEP의 현재 credit를 제거하고 HOLD·daily 제외 경고를 표시한다.
원 batch의 다른 unit은 그대로다. SUBMITTED는 새 현재 credit가 아니다. INTEGRATED여도
활성 body+census+claim binding이 후보와 다르면 `candidate_review_valid: true`만 남기고
`current_review_valid: false`와 안전 HOLD를 유지한다. 이력에는 원 판정·원 body hash를 남긴다.
활성 binding이 나중에 정확히 일치하면 가장 최근 통합 결과 하나만 현재 처리 수에 반영한다.
법규 HOLD/SOURCE_BLOCKED 결과도 처리 coverage이며 legal KEEP나 release 승인이 아니다.

## 새 보고서의 추가 계약

각 unit row는 기존 runbook 필드 외에 다음을 포함한다. 확인하지 않은 항목은 true로 만들지 않는다.

```python
row['actual_body_sha256'] = job['unit_bindings'][uid]['body_sha256']
row['reviewed_at'] = '실제 timezone-aware UTC timestamp'
row['body_correction_review'] = {
    **job['body_correction_review'],
    'final_body_read_completely': True,
    'final_census_read_completely': True,
    'all_parent_negatives_explicitly_reassessed': True,
    'all_parent_omissions_explicitly_reassessed': True,
    'all_derived_inputs_read_completely': True,
    'no_current_credit_before_matching_active_binding': True,
}
row['original_omission_reassessments'] = []  # 원 omissions가 없을 때만 빈 목록
claim['inherited_legal_blockers'] = job['carried_legal_blockers'][uid][cid]  # 해당 claim만
claim['original_legal_negatives'] = job['reconsidered_legal_negatives'][uid][cid]  # 수정된 negative만
claim['body_negative_reassessment'] = {
    'original_negatives_sha256': queue.digest(claim['original_legal_negatives']),
    'changed_statement_sha256': job['body_correction_review']['changed_statement_sha256s'][cid],
    'edit_span_sha256s': job['body_correction_review']['edit_span_sha256s'],
    'original_negative_read_completely': True,
    'corrected_statement_read_completely': True,
    'finding': '원 negative와 실제 수정 내용 및 primary 근거를 비교한 독립 판단',
    'decision': 'UNRESOLVED_REMAINS_HELD',
}
```

원 omission이 있으면 `job['body_correction_review']['parent_omissions']`의 각 정확한
raw SHA에 대해 `omission_sha256`, 실제 `finding`, decision을 하나씩 기록한다.
Decision은 `RESOLVED_BY_FRESH_COMPLETE_BODY_CENSUS_REVIEW` 또는
`UNRESOLVED_REMAINS_OMISSION`이다. 미해소 원 omission 문자열은 현재 `omissions`에도
그대로 남겨야 한다. 새 누락도 별도로 열거하며 COMPLETE를 강제하지 않는다.

수정 명제의 KEEP은 `RESOLVED_BY_CHANGED_BODY_AND_PROPOSITION` decision과 현재
공식 primary authority가 있어야 한다. 모든 KEEP authority는 기존 exact section,
HTTPS URL, 시행일/미확정 한계, evidence path/raw SHA와 함께 다음 실제 확보 이력을 넣는다.

```json
{
  "source_retrieval": {
    "mode": "LIVE",
    "http_status": 200,
    "transport": "실제 검증 TLS/proxy/도구 경로",
    "document_identity_status": "OFFICIAL_DOCUMENT_TARGET_PROVISIONS_DIRECTLY_READ",
    "raw_sha256": "authority.evidence_sha256와 같은 실제 확보 payload SHA",
    "retrieved_at_utc": "실제 최초 확보 timestamp",
    "read_at_utc": "실제 문서 확인 timestamp"
  }
}
```

같은 날의 진짜 보존 payload 재독이면 mode는 `SAME_DAY_RETAINED_CACHE`이고 최초
retrieved timestamp를 유지한다. 새 live 요청으로 표시하지 않는다. Read date는
`law_checked_date`와 같아야 하며 retrieval ≤ read ≤ reviewed 순서와 동일한 source day를
검사한다. HTTP403/404/200 access page는 문서 확인이 아니다. 실제 근거를 못 확보하면
SOURCE_BLOCKED/HOLD로 남긴다. 효력일을 retrieval date로 대신하지 않는다.
이 계약은 controller-attested reading/provenance와 커밋 바이트 결박을 검증하며,
문서를 실제로 읽었다는 인간/actor의 주장을 암호학적으로 증명하지는 않는다.

## Builder·shallow reader와 공개 blocker

공개 metadata reader는 HEAD에 보존한 raw snapshot/report/envelope/source만 검증한다.
옛 worker Git object는 필요 없다. Root의 submit/integrate는 기존 worker branch·정확 HEAD·
allowed path·token 검사를 계속 요구한다. 원 census-only 이력은 명시적으로 보존된 old
body snapshot으로만 검증하며, 일반 census-only body 금지 검사를 완화하지 않는다.

`registered_specs`는 독립 결과가 통합되고 실제 effective body가 정확히 후보와 일치할
때에만 새 census를 builder에 제공한다. 후보 revision을 `load_notes`로 활성화하지 않는다.
잘못된 spec, 미통합 활성 body, raw source 변조는 실패한다. Census/body successors는
원장 순서대로 explicit supersedence를 적용한다. 마지막 선택 census의 body SHA는
실제 effective body와 같아야 한다.

**공개 body migration은 구현하지 않았다.** 모든 후보와 job contract의 blocker는
`ROOT_SEPARATE_16_FROM_ACTUALLY_PUBLISHED_15_SNAPSHOT`이다. 아직 공개되지 않은
15번째 annotation guard로 body 교정을 통과시키지 않는다. Root는 실제 15번째 출시
snapshot을 확보한 후 별도 16번째 decoder/manifest 및 공개·derived 재검증을 해야 한다.
Full published builder 실행도 현재 후보에는 `NOT_RUN_INACTIVE_BODY_PUBLICATION_REQUIRES_SEPARATE_16`이다.

## 최초 실제 후보 w3-a-3

`revisions/notes/candidates/2026-11-04-w3-a-3-pamphlet-scope-v1.json`과
`reports/full-corpus-review/body-corrections/w3-a-3-v1/record.json`이 R 저자 후보다.
원 C fifth-c의 85 claims/보고서·원 target23 claims·omissions[]·HOLD011/019를 보존했다.
§21의 pamphlet trigger가 opioid/narcotic만인 것처럼 좁혀진 마지막 단락만 교정했다.
새 census24 claims에서 원22 statements는 그대로이며019를 고치고024를 분리했다.
원011은 mandatory HOLD, 수정019/024는 fresh independent 재판단 전 SOURCE_BLOCKED다.

2026-11-04 검증 TLS로 실제 확보·직접 읽은 Massachusetts 공식 §21과 Act2025c16
§§7/27의 payload와 raw SHA를 evidence에 보존했다. Act §7의 보호 의료 제공자 요청 시
label-name 예외는 §27에 따라2026-01-01 시행이며 pamphlet trigger amendment로
취급하지 않는다. Consolidated §21의 첫 label paragraph와 해당 session-law 반영 차이,
나이 용어 승계와 general IV narcotic 문법 해석, pamphlet 개별 시행일 한계는 남긴다.
다른 단락의 새 전체 source review date나 독립 PASS를 만들지 않았다. R는 이 새
body/census의 저자이므로 이 후보를 독립 reviewer로 claim할 수 없다.

검증:

```sh
python -m pytest -q tests/test_notes_body_reassessment.py tests/test_note_review_queue.py \
  tests/test_notes_census_reassessment.py tests/test_notes_independent_metadata.py
```

테스트의 작은 Git repo, authority·HTTP/source payload 및 미래16 activation은 명시적
synthetic fixture다. 실제 원장 등록·법규 감사·출시 증거로 사용하지 않는다.
