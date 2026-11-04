# 고정 146개 현실성 보충 감사 — root controller

실제 전체 원장의 현실성 미완료142개(17 NOT_ASSESSED/97 EDITORIAL_REVIEW_REQUIRED/28 HOLD)와 별도 고정4 RW 법규 재감사를 ID와 원 report raw/row SHA, 현재 객체 hash 및 style SHA로 고정합니다. 이전 archive-only 부분진단95는 전체 현실성 census가 아니었습니다. 기존 raw 자료는 보존하며 이 정정을 별도 증거에 기록합니다. 4 RW는 이미 nonlegacy safety hold로 안내돼 있었으므로 알려진 negative 안내 누락으로 세지 않습니다.

이 경로는 기존 fixed2/38 handler와 native engine을 확장하지 않습니다. `review_queue`의 unchanged independent-legacy lease/token/submit/ordered integration을 별도 wrapper/state에서 사용합니다. 실제 별도 fresh actor/session은 `/root/realism95_a`부터 `_d`, auditor_instance는 `GPT:<actor>:20261104`입니다. 실제 세션 생성 전에는 claim하지 않습니다. 배정은40/40/40/26이며 동일 세션을 여러 instance로 세지 않습니다.

Root만 다음 변경 작업을 실행합니다. 공통 인수는 `python scripts/realism_completion_review.py --root <controller-root> --controller-actor /root ...`입니다.

1. `plan`: `reports/full-corpus-review/realism-completion-v1/`의 work-queue.json/controller-scope.json/nearest-visible-input.json을 만듭니다. 기존 증거 덮어쓰기 없이 같은 plan은 idempotent합니다. root가 커밋합니다. 실제 리뷰는0개입니다.
2. 실제 fresh 세션 생성 후 `claim --actor <actual-actor> --session-id <same-actor> --auditor-instance <stable-instance> --actual-fresh-session-created --output <scratch-assignment>`을 실행하고 queue를 커밋합니다. Assignment는 old report/verdict/actor/exposure 이유를 포함하지 않습니다. 모델에 controller scope를 전달하지 않습니다.
3. `prepare-worker --job <id> --token <token> --destination <isolated-worktree>`는 assignment.base_commit에서 지정 branch를 만듭니다. claim 후의 queue commit을 worker diff에 섞지 않습니다. 같은 branch의 destination은 재사용합니다. Worker checkout은 정책4개·current style·worker contract·own output prefix로 제한하며 controller scope/원장/이전 보고서/hidden 질문 원본은 checkout하지 않습니다. Worker는 원본/공유 state를 수정하지 않습니다.
4. Read-only `export-input --assignment <scratch-assignment> --output <scratch-visible-packet>`은 --controller-actor 없이 실행할 수 있습니다. 모델에 이 packet과 별도 WORKER_CONTRACT, 정책, current style만 제공합니다. 프로그램은 내부적으로 controller hash를 읽되 이전 결론은 출력하지 않습니다.
5. Worker는 자기 prefix의 report/own memo/metadata만 commit합니다. 고정4 법규 근거만 추가로 허용합니다. Scratch result manifest와 exact40 worker SHA로 read-only `validate-worker --job ... --result ...`를 실행합니다. Worker commit은 실제 branch tip이어야 하고 base 이후 변경 파일 집합은 참조된 own-prefix 근거와 정확히 같아야 합니다.
6. Root가 순서대로 worker commit을 가져와 cherry-pick하고, exact result bytes를 own-prefix result.json에 둡니다. `submit --job --token --result <same-manifest>` 후 queue/result를 커밋합니다. root만 `integrate --job`하고 queue를 다시 커밋합니다. 원 commit/현재 HEAD의 모든 report/memo/meta/공식 source bytes를 비교합니다. CI의 얕은 clone consumer는 실제 통합 receipt를 재검증하며 옛 worker Git object를 요구하지 않습니다.
7. 실제 fresh FAIL만 source-bound archive warning으로 안내합니다. 고정4의 이전 nonlegacy hold는 그대로 유지하며 새 결과를 별도 history/next evidence로 연결합니다. HOLD28이나 기존 fixed2의 FAIL은 fresh PASS로 override하지 않습니다. 두 fixed2 ID의 기존 negative source도 controller scope에 고정합니다. Queue/근거 삭제·변조·stale content/style/누락·중복은 fail closed입니다.
8. `heartbeat --job --token`은 실제 lease를 연장합니다. 실제 worker 소실 시 `revoke --job --token --reason`은 append-only 기존 revoke를 사용합니다. 소급 시각/old actor 사칭 없이 새 attempt/token으로 다시 배정합니다. 동일 submit/integrate는 idempotent하며 결과가 다른 재제출은 거부합니다.

원 primary report/grade/key, author·법규 negative, 질문 본문/사용자 기록/default 선택은 바뀌지 않습니다. 새 source grade와 proof를 별도로 추가합니다. Raw primary PASS를 보존하고 effective PASS는 기존 PASS와 유효한 신규 PASS의 unique union입니다. 기존 realism HOLD/FAIL을 덮어쓰거나 이미 집계한 보충 PASS를 다시 세지 않습니다. 고정4 외 법규/key credit은0, 전체146의 새 원문-read/author/canonical RELEASED credit은0입니다. 고정4도 실제 current-hash 독립 key 판정만 최대4개 합집합에 추가합니다. Native 통합 전에는 pending이며 report 파일 존재만으로 진척을 올리지 않습니다.
