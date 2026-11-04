# N1 held-note의16번째 source gate — 아직 비활성

이 코드는 실제15 공개와 실제 B의25개 claim 전수 검토가 없으면 차단된다.
`APPROVED_CLOSURES`, `APPROVED_ACTIVATION_SOURCES`, `APPROVED_MIGRATIONS`는 모두 빈
목록이다. 실제 source/activation/migration JSON은 작성하지 않았다. 새 loader hook은
승인된 source 파일이 없으면 기존 M을 그대로 반환한다. PR192의 미공개15에 이
engineering을 섞거나 root queue/generated/body를 worker가 수정하는 작업이 아니다.

## 역사305와 적법한 sibling 진화

기존 C31 body의 `validate_registered`는 등록 당시305 binding을 과거 증거로 보존하고
현재 sibling census와 매번 같도록 요구하지 않는다. 원687 inactive successor의
`current305 == registration305` 검사는 실제로 후속 적법 version도 막았다.
3절을 먼저 통합한 후 최신 실제 ledger snapshot으로25를 등록하면 당장은 해결된다.
하지만 앞으로의 전수 보완도 가능해야 하므로 forward native chain을 별도로 증명한다.

원 snapshot·C31/parent·원 claim/source/hash/negative는 그대로 둔다. 다른 절의 변화는
실제 등록된 `CENSUS_ONLY_OMISSION_REASSESSMENT` record에서 원 binding→현재 binding으로
이어지고 body SHA가 같을 때만 허용한다. 모든 원명제·carry·source bytes·등록 event를
재검증한다. 미통합 author version은 처리 credit0이며 INTEGRATED는 실제 HEAD의
report/envelope/authority bytes와 통합 event도 검증한다. Claim 이후 과거 binding으로
되돌리거나 임의 row/census/source/body를 바꾸면 실패한다. 역사 body record를 지우거나
305 원 snapshot을 새 수치로 덮을 필요가 없다. Synthetic 실제 controller 시뮬레이션은
3절→25와25→3절 두 순서 모두 검증했다. 이는 실제 등록·법규 감사 실적이 아니다.

## 실제 공개15 closure

`notes_published15_closure.py`의 preparation만 과거 Git blob을 읽는다. 실제 main merge
commit과 tested tree가 같고, 커밋된 원 GitHub PR/commit/QA/Pages JSON 및 공개 asset
payload가 있어야 한다. QA는 실제 tested와 main SHA에서 success여야 하고 Pages는
실제 main SHA에서 success여야 한다. 적어도 공개 Markdown/build의 실제 HTTPS200
payload SHA가 그 published tree와 같아야 한다. Proposed 후보나200 error page,
실패한 CI, 다른 tree/URL/TLS 선언은 근거가 아니다. Controller의 보존·출처 선언과
바이트 결박을 확인하는 것이며 원격 신원/실독을 암호학적으로 인증한다는 뜻은 아니다.

Receipt는 `reports/full-corpus-review/notes16-publication/` 아래 새 경로에 둔다.
최상위는 schema1/status `ACTUAL_PUBLISHED_VERIFIED`/controller `/root`/repository
`woojunxnam/oddments`, 실제 published/tested commit와 tree, pull_number 및 원 payload
bindings를 가진다. `pull`, `published_commit_payload`, `tested_commit_payload`,
`ci_runs[]`, `pages_run`, `public_assets[].payload` 각각의 binding은 다음 정확한 키다.

```text
path, raw_sha256, official_url, http_status, tls_verified, retrieved_at_utc
```

모든 payload는 원바이트로 먼저 보존·커밋한다. Wrapper는 실제 확보한 상태·TLS·UTC
timestamp만 기록한다. GitHub JSON은 공식 `api.github.com/repos/woojunxnam/oddments/`
endpoint의 실제 PR/commit/actions run이며 assets는 실제 GitHub Pages origin이다.
Receipt 자체는 `{path, raw_sha256}`로 결박한다. 실제 값이 없으면 template의 가상값으로
채우지 말고 BLOCKED로 둔다. 이 branch에는 실제 receipt를 만들지 않았다.

Preparation은 전체 published tracked tree의 각 path/mode/Git-blob/SHA256과 original1781
현재 raw SHA를 pin한다. 현재 HEAD 바이트가 같으면 이를 재사용하고 달라졌거나
없어진 path만 `revisions/baselines/notes16-published15/<actual-published-commit>/<old-path>`에
원 Git blob 그대로 보존한다. 기존 snapshot을 다른 바이트로 덮지 않는다.

```sh
python scripts/notes_published15_closure.py --actor /root --prepare \
  --published-commit ACTUAL_MERGED_40SHA \
  --receipt reports/full-corpus-review/notes16-publication/ACTUAL/receipt.json \
  --output revisions/notes/published15-closures/ACTUAL-v1.json
```

실제 root controller worktree와 커밋된 실제 receipt가 필요하다. 결과는 승인 전 source
보존 proposal이며 activation이 아니다. 새 파일을 검토·커밋한 후 실제 path/rawSHA와
published commit/tree를 코드의 explicit closure 목록에 고정한다. 공개 후 source가 더
변해 새 old-preimage가 필요하면 실제 pub blob에서 새 immutable closure revision을
준비한다. 원 closure/preimage는 보존한다. Runtime은 누락 preimage를 current 파일로
대체하거나 원 Git object에서 몰래 보충하지 않고 SOURCE_BLOCKED로 실패한다.

필요하면 preparation에 `--retain-all`을 추가해 현재 같은 파일까지 실제 published
Git blob 원바이트로 전부 보존할 수 있다. Python API는 `prepare(..., retain_all=True)`와
`write_preparation(..., retain_all=True)`를 제공하며 기본값은 기존 changed-only 동작이다.
이 옵션도 기존 경로의 서로 다른 snapshot을 덮지 않으므로 새 closure output 경로가
필요하다. Root controller·실제 publication receipt·현재 같은 바이트의 HEAD 검증을
계속 요구한다. 나중에 적법하게 변경한 helper/test의 과거 바이트를 복원할 때 유용하지만,
live1781·원14/15·4정책·bank wrapper의 기존 narrow guard는 그대로 적용한다.
전체 preimage 보존은 closure 승인·N1 활성화·현재 검증 면제나 출시 승인이 아니다.

Runtime은 현재 HEAD와 보존 preimage만으로 전체 원 tree를 임시 read-only view에
재구성하고 Git tree SHA가 실제 published tree와 같은지 확인한다. 임시 새 HEAD는
바이트 조회용이며 원 published commit을 위조하거나 옛 Git object를 요구하지 않는다.
원 old verifier/old scripts를 그 view의 별도 Python process에서 실행한다. 따라서 old15/14가
현재 N1·현재 code·현재 notes state를 읽지 않는다. Source SHA를 임의 alias하지 않는다.
원14/15 manifest·baseline·4정책·1780개 live 보호 파일과 원 source report는 live에서도
그대로여야 한다. 원 public bank raw도 보존하며 dynamic queue/counter/selector는 별도
현재 검증을 거친다. 원1781 목록을 바꾸거나 historical view로 current 검사를 대체할 수 없다.

```sh
python scripts/notes_published15_closure.py --binding revisions/notes/published15-closures/ACTUAL-v1.json --verify-old
```

## Held builder source와 최종 public gate의 분리

공개된 source closure가 고정된 뒤 root가 G3 actual native 재평가와 별도 actual B의
inactive25 재감사를 마친다. 최신25 row는 반드시 COMPLETE/omissions[]이어야 하며
011의 원 inherited LEGAL_HOLD는 영구 보존한다. 다른 source-block/hold와 G3의 실제
결과를 KEEP/COMPLETE로 강제하지 않는다. R/E 및 C31 parent 실제 세션을 새 reviewer로
재사용하지 않는다. 실제 report/envelope/authorities/claim/integrate가 모두 필요하다.

Read-only source 제안:

```sh
python scripts/notes_held_sixteenth.py --propose-source --closure revisions/notes/published15-closures/ACTUAL-v1.json
```

제안을 실제 `revisions/notes/held-n1-activation.json`으로 검토·커밋하고 source rawSHA,
actual closure와 actual reviewer receipt를 explicit 목록에 고정한다. 그러면 loader는
원 M16124…→정확한 N1e082… 한 unit만 바꿀 수 있다. 다른305 unit record와 원 guide,
원 census/report/negative는 그대로다. `independent_content_review: KEEP`을 옮기지 않고
provenance는 `HELD_COMPLETE_CENSUS_NOT_LEGAL_PASS`다. 이것은 빌더의 held source이며
게시 승인이 아니다. SOURCE 파일 하나를 만들거나 self-declared status를 넣어도 승인
목록·실제 pub/actual25 검사를 통과하지 못하면 실패한다.

Root는 실제 N1을 선택한 미공개 branch에서 full-corpus ledger를 먼저 재생성·커밋하고
notes/study/refresh와 current progress를 순서대로 재생성한다. Source는 body를 따로
쓰는 writer를 제공하지 않으며 승인된 loader 입력만 합성한다. 실제 latest25 body/
census/claim binding이 맞을 때만 current 처리 coverage가 생긴다. 011 HOLD, public
unit warning, `requires_review`, daily 제외, canonical/question/legal release credit0은
그대로다. 79/96/99/100 같은 미래 수를 고정하지 않고 실제 source에서 다시 계산한다.

최종 read-only manifest 제안:

```sh
python scripts/notes_held_sixteenth.py --propose-migration --closure revisions/notes/published15-closures/ACTUAL-final.json
```

현재 HEAD export/build가 실제 builder 결과와 같고 최신 notes evidence·sibling evolution·
현재 progress/default safety가 유효해야 제안이 나온다. Final closure는 source closure와
동일한 실제 published15 commit/tree/manifest여야 한다. 더 늦은 preimage 보완 revision도
정확히 explicit 승인된 것만 허용한다. 원 native job/event prefix는 append-only로 보존한다.
실제 source/output manifest를 `protected-migration-held-n1.json`에 새로 고정·커밋하고
별도 explicit approval을 해야16 decoder가 작동한다. Source 승인으로 public gate를
건너뛰지 않는다. Manifest가 없으면 기존 old15 guard가 N1을 거부하고, 있지만 승인되지
않았거나 stale이면16이 거부한다. 최종16은 frozen old15→14→…→original1781 검증을
실행한 뒤 원 Markdown bytes로 normalize하므로 live N1에 old guard를 적용하지 않는다.

```sh
python scripts/notes_held_sixteenth.py --check
```

현재 이 명령은 실제 pub closure, actual B25, 최종 current N1 manifest가 없어 BLOCKED다.
실제 published15 full-closure verification, actual B25 재감사, 실제 N1 build 및 full release
QA/CI/Pages는 NOT_RUN이다. Synthetic GitHub/HTTP/activation fixtures의 통과를 그 실제
단계의 PASS로 보고하지 않는다. 정책·원14/15·root state/generated/active body 변경은0이다.

2026-11-04 handoff 시점에 root는 실제 PR192 main `e8f9b9bcffdb5cf8849ee97ba75b9526bd1cff67`,
tested `4c6380f14b516e6486c8ce8e8fdfcf75eb9ce7aa`의 동일 tree와 Pages41806902060 및
11개 workflow 성공을 보존했다. 실제 공개가 없다는 뜻으로 BLOCKED를 쓰지 않는다.
아직 이 코드의 normalized receipt/전체 preimage closure/explicit approval에는 결박하지
않았다는 뜻이다. 원 `pr192-publication-evidence/closure.json` 집계 기록은 보존하며,
그 값을 실제 원 PR/commit/run/asset payload의 정확한 binding으로 연결하는 새 wrapper가
필요하다. 원 집계 JSON을 이 receipt인 것처럼 이름만 바꾸거나 재구성하지 않는다.

최종16은 현재 Q queue 원바이트와 모든 실제 통합 report, notes queue/ledger/evidence를
다시 결박한다. Q38–41 등 미완료 job 정의는0 credit이며 이후 상태·source가 바뀌면
기존16 manifest를 재사용할 수 없다. 미래 Q/notes 수나 결과를 승인 값으로 고정하지 않는다.
