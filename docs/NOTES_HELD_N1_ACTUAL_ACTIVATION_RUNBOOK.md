# 실제 N1 held 활성화의 root 실행 순서

이 문서는 `/root/notes16_engineering`의 read-only 사전점검과 실행 안내다.
활성화 source나 migration manifest를 생성·승인하지 않는다. 필드는 실제 helper의
성공 출력에서만 얻으며, 이 문서의 이름이나 예시로 실제 결과를 대신하지 않는다.

## 확인된 실제 입력과 현재 blocker

사전점검 HEAD는 `858c9edef81e51656fd2d3cfd9db934833d9f504`다. 대응 원증거는
`reports/full-corpus-review/notes16-activation-preflight/actual-source-preflight-858c9ede.json`에 있다.

- Native37의 실제 fresh25는 INTEGRATED/COMPLETE/LEGAL_HOLD,25 claim/omissions0이다.
  원011의 LEGAL_HOLD와 상속 blocker가 실제 queue/report/envelope에 그대로 있다.
- Native34 `w3-a-15`는 COMPLETE/SOURCE_BLOCKED,14 claim이다.
- Native35 `w3-a-16`은 COMPLETE/LEGAL_HOLD,27 claim이다.
- Return-pathways의 latest38은 당시 LEASED다. 이후 실제 감사가 발견한 추가 누락과
  법규 차단을 새 author census와 별도 fresh 감사로 처리한 최종 job이 필요하다.
  이 문서는 미래 job ID·최종 claim수·COMPLETE를 예측하지 않는다.
- 활성 edition은 M(`2026-11-03.emergency-kit.1`)이며 source/manifest 파일과 해당 승인표는 비어 있다.
  진단 전후 queue/ledger/guide/공개 Markdown/원14·15 SHA는 같았다.
- Root의 published15 verify-v2는 `docs/REVIEW_QUEUE.md`의 old preimage가 빠져
  SOURCE_BLOCKED로 종료했다. 기존 closure를 넓게 허용하지 말고 실제 공개 blob을
  보존하는 새 immutable closure revision을 준비해야 한다.

## 1. 실제 최종 native source를 먼저 확정

Root는 pending note job을 계약에 따라 통합하고 return-pathways의 실제 최신
census/report/envelope/공식 근거를 확정한다. `census.latest_jobs(state)`가 선택한
네 단위 모두 INTEGRATED이고 `validate_job`을 통과해야 한다. Return의 실제
OMISSIONS_FOUND/LEGAL_HOLD/SOURCE_BLOCKED를 긍정 판정으로 바꾸지 않는다.
N1/25 자체는 COMPLETE/omissions0이어야 하고011은 반드시 LEGAL_HOLD여야 한다.

원장을 현재 M 상태에서 재생성하고 warning/selection도 현재 결과에 맞게 갱신한다.
각 단계의 source/generated 변경을 검토·커밋한다. 공유 파일은 root만 갱신한다.
`build_representative_rewrites.py`는 현재 archive-warning sourceSHA를 wrapper의
단 하나의 허용 입력에 결박한다. 모든 question/key/source/다른 metadata는 원본과 같다.

## 2. Source용 실제 공개15 closure를 새 revision으로 보존

아래 `notes16_source_closure` 변수는 root가 새로 선택한 **고유한 실제 출력 경로**다.
기존 closure를 덮어쓰지 않는다. 파일명을 정했다는 사실은 승인이나 검증이 아니다.
`notes16_final_closure`도 뒤 단계에서 별도 실제 고유 경로를 정한다.

```bash
/workspace/mpje-venv/bin/python scripts/notes_published15_closure.py \
  --actor /root --prepare \
  --published-commit e8f9b9bcffdb5cf8849ee97ba75b9526bd1cff67 \
  --receipt reports/full-corpus-review/notes16-publication/pr192-20261104-resume/receipt-root-verified.json \
  --output "$notes16_source_closure"
```

Root는 생성된 full-source manifest와 모든 old preimage를 검토·커밋한다. 실제
path/rawSHA 및 공개 commit/tree를 `notes_published15_closure.APPROVED_CLOSURES`에
고정·커밋한 뒤 아래 실제 검사를 통과해야 한다. 실행 중 source HEAD를 바꾸지 않는다.

```bash
/workspace/mpje-venv/bin/python scripts/notes_published15_closure.py \
  --binding "$notes16_source_closure" --verify-old
```

이 검사는 원 공개15 전체 tree를 원바이트로 재구성해 원14·15와1781 보호를 실행한다.
새 파일이 이후 바뀌어 old preimage가 더 필요하면 새로운 revision을 준비한다.

## 3. 실제 source proposal을 검토하고 별도로 결박

`--propose-source`에는 actor option이 없고 read-only다. 실제 latest native job과
승인된 공개 closure를 읽어 계약을 검증한다. 성공 출력만 별도 임시 파일로 보존한다.

```bash
/workspace/mpje-venv/bin/python scripts/notes_held_sixteenth.py \
  --propose-source --closure "$notes16_source_closure" \
  > /workspace/scratch/held-n1-source-proposal.json
```

Root는 실제 출력의 N37 report/envelope/actor, latest G3 IDs, source closure와
zero-credit 필드를 확인한다. 성공 출력으로만 `revisions/notes/held-n1-activation.json`을
만든다. 실제 source path/rawSHA를 키로 하는 `APPROVED_ACTIVATION_SOURCES`의 값은
이 출력의 **실제** `closure`와 `review`다. Source 파일과 해당 explicit binding을
함께 검토·커밋한다. 작성 중 불완전한 source 파일을 둔 채 generator를 실행하지 않는다.
허용표만 미리 추가하거나 다른 시점의 proposal/미래 job으로 채우지 않는다.

이 승인으로 loader가 정확히 M의 `w3-a-3` 한 단위를 N1으로 합성할 수 있지만,
이는 법규 PASS나 공개 승인이 아니다. 원 `notes/guide.json` 또는 M 역사파일을
수정하지 않는다. SOURCE가 없을 때 기존 M을 반환하고, unapproved/stale source는 실패한다.

## 4. 실제 held 결과를 순서대로 재생성·커밋

```bash
/workspace/mpje-venv/bin/python scripts/build_full_corpus_review.py
```

먼저 새 ledger/current bindings를 검토·커밋한다. 새 활성 N1/25와 실제 통합 보고서의
body/census/claim binding이 일치할 때만 해당 completeness가 계산된다. 그 후:

```bash
/workspace/mpje-venv/bin/python scripts/build_ultimate_notes.py
/workspace/mpje-venv/bin/python scripts/build_exam_study.py
/workspace/mpje-venv/bin/python scripts/build_refresh.py
```

Root는 실제 Markdown/build와 기타 생성물을 검토·커밋한다. `w3-a-3`의
`LEGAL_HOLD`, `requires_review`, notice, daily 제외와 original011 blocker를 확인한다.
다른305 본문 record, 원 질문/정답/이력, 원14·15 및 보호정책을 보존한다.

## 5. Final output용 closure와 실제 migration을 별도로 결박

N1 출력/진척/카드/등록원장 변경 후에는 source closure에 없던 old preimage가 생길 수 있다.
2단계와 같은 실제 published commit·receipt로 `notes16_final_closure`를 새로 prepare하고,
preimages/manifest를 커밋·명시 결박·verify-old 한다. Source closure와 공개 commit/tree/15 SHA가
같아야 한다. 원 source closure는 보존하며 새 final closure로 덮어쓰지 않는다.

```bash
/workspace/mpje-venv/bin/python scripts/notes_held_sixteenth.py \
  --propose-migration --closure "$notes16_final_closure" \
  > /workspace/scratch/held-n1-migration-proposal.json
```

이 helper는 실제 current N1 생성물, 최신25·G3·Q queue, current counters와 모든 sourceSHA를
검사한다. 성공 출력만 `revisions/notes/protected-migration-held-n1.json`으로 보존하고
실제 path/rawSHA와 출력의 실제 `closure`를 `APPROVED_MIGRATIONS`에 고정·커밋한다.
Source 승인만으로 이 단계를 대체할 수 없다. 미래 결과를 manifest skeleton으로 채우지 않는다.

```bash
/workspace/mpje-venv/bin/python scripts/notes_held_sixteenth.py --check
/workspace/mpje-venv/bin/python scripts/verify_representative_protected.py --check
```

이후 관련 validators, full pytest, 정규 artifact 생성과 재생성 diff0, exact-head GitHub CI를
현재 후보에 대해 실행한다. 테스트 fixture PASS는 실제 source/output/publication 검증을
대신하지 않는다. 새 note/Q 결과나 source 변경으로 source binding이 바뀌면 기존16을
재사용하지 않고 다시 실제 결과에 결박한다. 모든 release gate 통과 전 병합·배포하지 않는다.

## 현재 사전점검의 한계

이 문서와 JSON은 HEAD858c9ede의 실제 source read-only 확인이다. 최종 return census
감사, N1 활성화, final16, full QA/CI 및 새 Pages 검증은 수행하지 않았다. 현재 활성 M과
public Markdown은 그대로다. 원011 HOLD와 sibling HOLD/SOURCE_BLOCKED를 유지한다.
