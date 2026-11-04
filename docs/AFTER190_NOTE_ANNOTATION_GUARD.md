# PR190 뒤의 15번째 노트 annotation guard

이 변경은 법규·독립 감사 실적이나 게시 승인이 없는 release-gate engineering이다.
기준은 PR190의 실제 main merge **`f8ec04a028e38288aa9cbf539fa12244f2cd49a4`**다.
Root는 corrected candidate `205c8feb08e463fac30c8162a124875befa0ae62`와
tree `0d0eac7ee844f6db721041d9764b26c8acd1bde1`이 같음을 확인했다. 이 guard는
공개 origin의 바이트 대조나 게시 검증 승인을 제공하지 않는다. 이후 실제 원본이
다르면 root가 다시 확보해 명시적으로 재결박·검사해야 한다.
`annotation_inputs_ready`는 source 결박의 준비 상태이며 게시 승인이 아니다.

고정 원본은 다음과 같다.

- `revisions/baselines/complete-notes-pr190.md`:
  `c3bd223ff1774917388986a3b4a4e46b2f995e9d702d671309edeb92dd489d16`
- `revisions/baselines/notes-build-pr190.json`:
  `d23f20169980cb5c94b24624776f652a233ff3e992c7e91fb940d3edfe8b419b`
- 14번째 `protected-migration-independent-notes-wave3.json`은 main의 정확한 원바이트
  `53537abd57b56bc8a839901a766de916c7a06b4275beba8bd2ebf435adf0353e`로 복원한다.
  현재 export를 통과시키려고 이 parent의 `new_sha256`을 다시 바꾸지 않는다.

새 manifest는 `revisions/notes/protected-migration-after190.json`이며,
`scripts/notes_after190_annotation.py`가 명시적으로 준비·검증한다. 범위는 한 export와
그 build metadata뿐이다. 원래 M semantic
`e1519c0290ff220eb8251307e26340d76d394a7ec1f3e651194d4495a03f1824`,
edition, revision provenance와 build의 의미 필드를 PR190와 대조한다. census ledger
해시와 독립 노트 review progress 이외의 build 변경은 허용하지 않는다.

최종 v4 census, version record, 실제 23번 E3 job의 INTEGRATED 상태와 현재
report/envelope/source raw SHA를 결박한다. 현재 6,989개는 author enumeration 수이며
새 author source check나 independent legal audit credit로 바꾸지 않는다. 독립 노트
consumer가 현재 body/census/claim·원 blocker·실제 controller가 선언한 actor/session과
source를 다시 검증하고 처리 수·KEEP/HOLD/SOURCE_BLOCKED를 계산한다. 신원 문자열은
controller-attested declaration이며 암호학적인 신원 인증이 아니다.
선택된 32개 census의 path/raw SHA 전체도 controller source
`e78af1cd5ccdd749c3599aa4f36a217af4d06552`의 고정 map digest와 대조한다.
claim 수가 같아도 다른 census로 바꿔 `--write`하는 방식으로 범위를 넓힐 수 없다.
E3 원 envelope에 선언된 42개 artifact를 모두 현재 커밋의 원바이트로 대조한다.

중간 LEASED/pending 23번 결과로 manifest를 준비하면 명시적으로 실패한다.
추가로 15번째 manifest 자체의 `annotation_inputs_ready`가 false이면 게시 검증은
실패한다. source 변경 후 옛 pending manifest를 그대로 출시할 수 없다.

이 미출시 15번째 guard의 최종 범위는 다음과 같다. 배정 정의를 고정한 것은
미래 결과를 인증한 것이 아니다. 실제 원장·원 report·envelope·보존 primary bytes와
claim/submit/integrate 연결을 현재 HEAD에서 확인한 뒤에만 final manifest를 준비한다.

- Legacy question job1–29와 root가 `804178fd`에 실제 배정한 CURRENT DEFAULT wave9의
  30–33까지 정확한 sequence/ID/stage/question-hash map. 30–33은 각각40문항이며 실제
  fresh actor `/root/independent_wave9_a`–`d`도 고정한다. 모두 실제 INTEGRATED여야 한다.
  Phase7의21–24, wave8의25–28, native 현재ID 세 문항의29와 wave9의160문항을 각각
  결박한다. QUEUED/LEASED/SUBMITTED 또는 status만 조작한 IG는 실패한다.
- Notes job1–30의 정확한 ID/unit-binding map과 실제 INTEGRATED 결과. 28–30의 F 작성
  immutable v2 census 보완도 기존 negative/history를 그대로 검증한다.
- 오직 하나의31번 `BODY_CORRECTION_REASSESSMENT`: w3-a-3의 R 작성 후보를 root가 새
  immutable record에 재등록한 정확한 경로·raw SHA·job ID. 원 record, candidate revision,
  24-claim census, 원26번 parent/report/envelope, mapping, 011 HOLD와019/024의 원 negative는
  그대로여야 한다. 현재 M 본문·선택6989 census에는 새 후보를 넣지 않는다.
  QUEUED/LEASED/SUBMITTED/INTEGRATED 어느 상태에서도 inactive/current credit0이며
  metadata의 `current_review_valid:false`, `LEGAL_HOLD`, review 경고를 요구한다.
- Author job53의 실제 G 세 문항 current-ID source review와 원63개 static source.
  기존 consumer의 original52 job/event와 모든 static raw SHA 검사를 유지한다.
  Author 결과를 독립 감사로 바꾸지 않는다. 원2346 question objects와 추가 native3의
  archive-only 상태를 보존한다. Allocation의 default298은 before snapshot이다.
  최종 default 수를298로 강제하지 않는다. 실제 현재 hash에 결박된 부정 finding의
  명시적 safety hold로만 default를 줄일 수 있으며, 원 hold/history를 보존한다.
  기존 selection/default-review/archive-warning safety validator로 현재 미보류 negative를
  차단한다. 새 failed default를 KEEP으로 덮거나 이전298 밖의 ID를 추가할 수 없다.

31의 실제 재등록 record는 `.../w3-a-3-v1/registrations/after-census-v2.json`,
raw SHA `945e120c2676793b7f6649d0eaa5a3cb4eb22b3f2e85fd56d273331a0730dd1c`,
job `review-independent-notes-body-4c3229fb7bfb76b6`이다. Root checkpoint847d의 명시적
재결박이며, 보존 ledger와 현재 ledger를 직접 비교해 target 불변·전체306 body 불변과
정확히 `[w2-c-12,w3-a-6,w3-a-7]`의 sibling census 차이만 확인한다. 현재 처리 수는
실제 최신 binding에서 계산한다. 비활성31 때문에 원 current credit 하나가 제외되며,
이전80을 새 현재 수로 고정하거나 N 활성화를 이미 한 것으로 취급하지 않는다.
29의 실제 F report/envelope 경로도 실제 통합 후에만 고정했다. Wave9는 실제 runbook의
`independent-phase9-[a-d]-review.json`과 같은 basename의 `-result.json`만 출력 계약으로
허용한다. 이는 파일 존재나 review 완료의 증거가 아니다. 그 실제 source raw SHA와
최종 manifest는 아래의 미공개 wave10 확장을 포함한 모든37 job의 실제 통합과
known-negative containment 후에만 계산한다.
미래 IG나 임의 source prefix/추가 job을 허용하지 않는다.
새 note32/question38/author54는 pending이어도 범위 밖이며 별도 검토가 필요하다.
기존15 manifest의 old25-job/6985 상태를 현재 source의 final proof로 사용할 수 없다.

### 공개 전 wave10 completion bridge

15는 아직 한 번도 공개하지 않았다. `7ea50249`의 33-job 후보 및 실패한 QA는
과거 checkpoint로 보존하며 실제 공개 baseline으로 쓰지 않는다. 공개된14의 원
manifest·MD/build snapshot·기존 decoder는 그대로다. 이 변경은16 body 활성화가 아니다.

실제 `08a417e2e53e83501e2756792cda0168fe4ae8a7`의34–37 할당만 추가한다.
각40개 whole-record hash와 actual `/root/independent_wave10_[a-d]` actor, 원
priority-source map digest를 코드에 정확히 결박한다. 총160개 중 할당 당시128개는
현재 default,32개는 archive였다. 160개 전부 default라고 주장하거나 최종 default
수를229/298 등으로 강제하지 않는다. 기존33개 job의 ID/hash/actor/원source 검증을
유지한다. 원1–33의 실제 통합 job 전체 digest도08a의 exact 값으로 고정해 과거
report/negative/envelope receipt를 함께 재작성하는 우회를 막는다. 새 네 job도
실제 INTEGRATED event, report와 원 envelope, 전 row/hash,
primary raw bytes 및 controller-attested provenance를 검증해야 한다.

새 출력 계약은 `independent-phase10-[a-d]-review.json`과 같은 basename의
`-result.json`이다. 파일명 허용은 파일 존재나 감사 완료의 주장이 아니다.
QUEUED/LEASED/SUBMITTED나 status-only IG는 manifest 생성을 명시적으로 실패시킨다.
이전 미공개 manifest의 `annotation_inputs_ready: true`도 이 검사를 건너뛸 수 없다.
실제37개 source가 커밋되고 기존69개 부정 및 새 실제 부정이 source-bound hold로
격리된 후에만 root가 새 manifest를 생성·재결박하고 전체 QA를 수행한다.

C36의 실제 source-context 노출 경계는 `MA-RW-0051/0061/0062/0064` 네 개다.
이 네 row의 `existing_answer_correct: NOT_ASSESSED`, `safe_hold_recommended: true`와
HOLD 또는 더 강한 MINOR_EDIT/MAJOR_REWRITE/DELETE verdict를 유지해야 한다.
더 강한 실제 negative를 HOLD로 낮추도록 강제하지 않는다. 원 노출 로그와 잠정40개0 기록은
history로 보존한다. B40/C나머지36은 실제 fresh primary 판단 대상일 뿐 자동
YES/PASS가 아니다. 이 annotation은 C4 whole-key credit를 만들거나 기존 negative를
새 KEEP으로 덮지 않는다. 현재 progress는 current builder와 따로 대조한다.

notes31·author53·census6989·M semantic은 그대로다. private/historical context의
기존 exact 예외만 유지하며 wave10에 새 예외를 자동 생성하지 않는다. 실제 새
mismatch가 있으면 원 job/report/origin/raw SHA의 증거부터 확인하고 별도 bounded
검토를 받아야 한다. runtime 검증에는 HEAD-retained bytes만 필요하며 옛 worker
Git object를 요구하지 않는다. 이 bridge의 canonical/question/legal 새 credit는0이다.

Canonical Q0012와 연결 SG-CII-LIFECYCLE의 철회는 별도 strict decoder가 담당한다.
최종15 준비 시 그 decoder와 exact retained cause/metadata-only package가 실제로
존재하고 검증되어야 한다. Notes annotation이 canonical RELEASED 복귀나 guide VERIFIED
복귀를 허용하지 않는다. 기존1781 protected inventory·공개14 manifest와 decoder를
바꾸지 않으며, root가 실제 hotfix를 병합한 뒤 두 경로의 합성 검사를 수행한다.

새 candidate 본문 공개는 이 annotation guard 범위 밖이다. 실제15 출시 snapshot을
기준으로 root가 별도16번째 body migration을 만들어 검증해야 한다. 이31의 독립
후보 검토도 활성 본문과 일치하기 전에는 현재 credit를 얻지 않는다.

검증은 먼저 현재 source로 export/build를 메모리에서 재생성하여 manifest의
예상 바이트와 대조한다. `new_sha256`만 바꿔 임의의 annotation이나 법규 승인을
삽입할 수 없다. 그 후 export를 정확한 PR190 Markdown으로 decode하고 기존
14개 guard를 원래 코드·원본·parent hash로 차례로 실행한다. 기존 source·semantic
보호를 새 annotation으로 우회하지 않는다.

Root의 후속 절차는 다음과 같다.

1. 고정된 실제 PR190 merge와 게시 원본을 확인한다. 다른 원본이면 먼저 재결박한다.
2. E3/Phase 7 등 실제 통합 source와 checkpoint를 커밋한다.
3. 기존 재생성 순서로 ledger 및 notes 산출물을 갱신한다. 이 worker는 root/shared
   generated 파일을 쓰지 않는다.
4. 최종 ledger/raw source 기준으로 아래 명령을 실행하고 새 15번째 manifest만
   검토·커밋한다. 14번째와 PR190 snapshot은 그대로 둔다.
5. protected guard, 전체 재생성 확인, 동결 QA와 CI를 새 tree에서 수행한다.

```sh
python scripts/notes_after190_annotation.py --write
python scripts/notes_after190_annotation.py --check
python scripts/verify_representative_protected.py
```

`--write`는 제안을 준비할 뿐이며 release 승인이 아니다. 현재 generated 파일이
그 결박과 다르면 protected guard는 실패한다. 이 guard가 허용하는 semantic 범위를
넓히거나 이전 manifest를 수정하는 방식으로 해결하지 않는다.

범위 검증:

```sh
python -m pytest -q tests/test_after190_annotation.py tests/test_emergency_note_activation.py
```

실제 최종 source가 미완료인 동안 준비된 final manifest가 필요한 integration fixture는
`NOT_RUN` 사유로 skip한다. 범위·tamper·원14 보존·실제 author source 검증은 별도로 실행한다.
Skip을 final gate PASS로 보고하지 않는다. Root는 모든 실제 source와15 manifest를 고정한
tree에서 전체 검증·CI·배포 검사를 다시 수행한다.

## 과거 입력 receipt와 현재 source의 구별

일부 immutable wave9 report는 읽기 당시의 progress, 운영 runbook, nearest-default
selection 원본 SHA를 기록했다. 이를 현재229 selector나 현재 progress와 같은 바이트로
취급하지 않는다. `after190_historical_context.py`와
`reports/full-corpus-review/after190-historical-context/registry-v2.json`은 실제 job/report
raw SHA, 원 path+SHA, 정확한 report JSON pointer와 retained path+동일 SHA를 결박한다.
허용은 A30 progress·당시 운영 runbook, B31의40 nearest-default context와 D33 input
selection의 정확4개뿐이다. RELEASE/AUDIT/SOURCE_USE/QUESTION_AUTHORING 정책,
style/blueprint, primary authority, question이나 current ledger에는 alias를 제공하지 않는다.

과거 progress와 당시 운영 runbook은 준비 때 알려진 실제 worker/root Git blob에서
선언된 SHA를 확인해 원 바이트를 보존했다. Selection은 이미 HEAD에 있던
`phase9-before-selection.json`의 정확한 원 바이트를 재사용한다. Runtime은 HEAD의
보존본만 검증하며 옛 worker Git object를 요구하지 않는다. 현재 운영 runbook은
별도로 HEAD와 대조하고, 현재 progress는 현재 실제 builder의 읽기 전용 결과와
동일해야 한다. 현재 selector/default safety·원2346 object·primary 검사도 그대로 실행한다.

B31의 sources[8,12,39,40]에는 copyright-restricted memo-only source의 private
`extracted_path/SHA`가 있다. 이 정확4개는 원 report·source index/id·path/hash·공개
금지 선언과 해당 relative retained memo를 결박한 **비보존 설명값**이다. CI가 private
원문/추출문 바이트를 검증했다고 주장하지 않는다. 원 raw와 text는 repo에 반입하지 않는다.
Retained memo의 HEAD 바이트·SHA 검사는 계속하며 다른 absolute/public/미선언 경로는
거부한다. Registry의 원 v1·원 보고서·envelope·기존14 manifest와 decoder는 보존한다.
이 보존 작업은 새 법규 판단·현재 counter 변경·감사 또는 release credit를 만들지 않는다.
