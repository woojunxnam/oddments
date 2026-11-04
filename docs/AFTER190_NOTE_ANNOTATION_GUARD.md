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
report/envelope/source raw SHA를 결박한다. 현재 6,985개는 author enumeration 수이며
새 author source check나 independent legal audit credit로 바꾸지 않는다. 독립 노트
consumer가 현재 body/census/claim·원 blocker·실제 controller가 선언한 actor/session과
source를 다시 검증하고 처리 수·KEEP/HOLD/SOURCE_BLOCKED를 계산한다. 신원 문자열은
controller-attested declaration이며 암호학적인 신원 인증이 아니다.
선택된 29개 census의 path/raw SHA 전체도 controller source
`f2eb58b3a3e387a94a34cef8f970ed93f5dbce8a`의 고정 map digest와 대조한다.
claim 수가 같아도 다른 census로 바꿔 `--write`하는 방식으로 범위를 넓힐 수 없다.
E3 원 envelope에 선언된 42개 artifact를 모두 현재 커밋의 원바이트로 대조한다.

중간 LEASED/pending 23번 결과로 manifest를 준비하면 명시적으로 실패한다.
추가로 15번째 manifest 자체의 `annotation_inputs_ready`가 false이면 게시 검증은
실패한다. source 변경 후 옛 pending manifest를 그대로 출시할 수 없다.

Phase 7은 이미 배정된 legacy job 21–24의 정확한 ID 범위만 checkpoint에 기록한다.
Pending job은 근거 실적으로 취급하지 않는다. 노트 후속 job 24–25도 root가
지정한 정확한 10개 unit 범위만 허용하며 LEASED 상태의 새 credit는 0이다.
해당 job이 실제 통합되면 동일한 노트 consumer로 원 report/envelope/actor를 검증한다. INTEGRATED 결과가 생기면 현재
커밋된 report, 원 result envelope, submit/claim/integrate 연결과 actor/session 및
0 canonical credit를 검사한다. 이 metadata가 바뀌면 manifest를 명시적으로
재결박해야 하며 임의의 다른 report나 새 job 범위는 허용하지 않는다.

원장 자동 연속 배정을 위해 controller가 같은 source에서 명시한 wave 8의
job 25–28 네 정의만 추가로 허용한다. `MA-EXP-0009`–`0168`의 네 40문항 묶음이며,
정확한 job ID와 전체 `question_hashes` map digest를 코드에 고정한다. QUEUED,
LEASED, SUBMITTED 동안 새 evidence/review credit는 0이다. 어느 하나라도
INTEGRATED이거나 integration 이력이 있으면 이 guard는 실패한다. 실제 후속
통합을 반영하려면 다음 bounded guard 검토가 필요하다. 새 job 29 등은 허용하지 않는다.

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
