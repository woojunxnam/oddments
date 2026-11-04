# MA-Q-0012 안전 철회의 좁은 원본 보호 예외

이 guard는 현재 알려진 D 보기 해설의 논리 불일치 때문에 MA-Q-0012를 안전 보류한다.
새 법규·realism·canonical 감사나 정답 변경, release 승인을 제공하지 않는다.
기존 `RELEASE_POLICY.md`의 `RELEASED -> REVIEW_REQUIRED` 경로와
`withdraw_from_release.py`를 사용한 철회만 검증한다. 정책·감사 기준은 바꾸지 않는다.

기준은 실제 main PR190 merge `f8ec04a028e38288aa9cbf539fa12244f2cd49a4`다.
별도 after190 note 15번째 guard, 현재 note queue의 job24 존재, 이전 worker Git object가
필요하지 않다. 원 E report/alignment/visible input/result와 두 공식 PDF, root가 보존한
job24 INTEGRATED object·CLAIM/SUBMIT/INTEGRATE event를 unprotected archive에서 읽는다.
이를 현재 main의 note 감사 실적으로 소급하지 않는다. Actor/session 문자열은 실제
controller가 포착한 선언의 보존이며 암호학적인 신원 인증이 아니다.

`reports/full-corpus-review/canonical-q0012-withdrawal/protected-migration.json`의
원바이트 SHA를 코드에 고정한다. 자동 재결박·일반 data 예외·새 경로 허용 기능은 없다.
원 1,781개 파일의 baseline JSON, SHA·Git blob 기록 및 기존 note guard 14개는 보존한다.
보호 verifier에는 정확한 다음 두 path에 대한 decoder만 추가한다.

- `data/questions/ma-q-0012.json`: `verification_status`는 `RELEASED -> HOLD`,
  `lifecycle_status`는 `RELEASED -> REVIEW_REQUIRED`만 허용한다.
- `data/exam_style/question_family_matrix.json`: 정확한
  `P2_0012_MA_CII_VALIDITY_30D.current_released_count`만 `1 -> 0`으로 바꾼다.

두 현재 파일은 `revisions/baselines/canonical-q0012-withdrawal/`의 원 preimage로
decode하고, 기존 baseline의 크기·SHA-256·원 Git blob SHA-1을 그대로 검증한다.
preimage 자체를 변경하거나 새 baseline을 만드는 방식은 허용하지 않는다.
나머지 438개 canonical question은 원바이트가 같아야 하고, 전체 file 집합도 439개다.

철회 뒤 canonical RELEASED 수와 family 합계는 397이다. Preview는 원 398개 순서에서
MA-Q-0012 하나만 제거하며, 날짜·안내문 변경은 정확한 withdrawal config와 일치해야 한다.
source audit 목록 등 나머지 preview 정보는 보존한다. MA-Q-0028의 원 상태와 preview
제외도 유지한다. 현재 question의 모든 본문·보기·저장 key B·해설·QUESTION_AUDIT_FIELDS·
audit hash·과거 audit·adjudication 및 `independent_audit_status: PASSED` 기록은 그대로다.
이 과거 PASSED 요약은 현재 HOLD를 해제하지 않는다.

원 E finding은 D 해설의 국소적인 논리 불일치이며, 전체 문항 key 판단은
`NOT_PERFORMED`, question audit credit는 0이다. Guard는 원 finding의 row/record/visible
hash와 현재 보존된 원문을 대조하고, 그 의미를 fresh whole-question 감사로 바꾸지 않는다.

이 guard가 설치되면 Q0012 또는 family가 과거 baseline 바이트와 같아졌더라도 decoder는
항상 실행된다. 따라서 같은 오류 hash를 옛 `RELEASED`로 복원하거나 preview에 재반입하면
실패한다. Generic withdrawal report의 reversal 안내는 이 unchanged known-error hash를
복원할 권한이 아니다. 추가 KEEP 기록으로 기존 문제를 덮어쓰는 것도 허용하지 않는다.
실제 내용 수정·새 독립 감사·별도 명시 guard 승인이 필요한 후속 경로는 이번 범위 밖이다.

검사:

```sh
python scripts/canonical_q0012_withdrawal.py
python scripts/verify_representative_protected.py
python -m pytest -q tests/test_canonical_q0012_withdrawal.py
```

Root가 별도로 artifacts를 재생성하고 main 기반 고정 QA·CI·배포를 검사한다.
이 decoder를 통과했다는 사실만으로 게시하거나 전체 MPJE 품질 mission을 완료하지 않는다.
