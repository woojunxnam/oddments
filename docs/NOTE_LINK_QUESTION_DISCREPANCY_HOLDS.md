# 노트 연결 검토에서 발견한 문항 부분 HOLD

`scripts/note_question_discrepancies.py`는 이미 통합된 R3 노트 검토에서 확인한
11개 cashier 보기의 자격 사실/해설 불일치를 소비한다. 이 engineering adapter는
새 법규 판단이나 전체 문항 감사가 아니며 author/question/canonical credit는 0이다.

입력은 기존 `reports/full-corpus-review/note-question-discrepancy-backlog.json`이다.
이 원본의 미완료 `runtime_status` 문자열은 수정하지 않는다. 적용 상태는 derived
progress의 `note_link_question_discrepancy_holds.runtime_status`에 별도로 나타난다.

검증은 현재 HEAD에 커밋된 바이트로만 수행한다. 고정된 R3 보고서/alignment의
경로·raw SHA, note job 20의 INTEGRATED 상태와 claim/submit/integrate event,
result envelope의 raw SHA, 실제 controller가 선언한 actor/session/instance,
독립 노트 stage와 0 credit, 보고서가 가리키는 alignment/source payload를 재검증한다.
이는 controller-attested declaration이며 신원을 암호학적으로 인증하는 절차가 아니다.
옛 worker branch나 Git object 없이 snapshot/shallow checkout에서 동작한다.

11개 ID와 choice의 범위는 고정돼 있다. Backlog row의 canonical SHA, finding,
원문 전체 객체 해시, choice text, stored key의 해당 choice 제외, safe visible
projection의 stem/모든 보기/key/전체 해설을 현재 커밋된 원 bank 객체와 대조한다.
누락·중복·임의 추가, uncommitted/stale 바이트, 출처나 stage/provenance/credit 변조,
전체 정답 감사로의 재분류는 실패한다. 원본 변경을 이 adapter에서 자동 승인하지
않으며, 향후 해소에는 별도 source-bound 보완·독립 감사와 명시적 후속 절차가 필요하다.

`build_full_corpus_review.build()`는 기존 author/independent 판정을 계산한 뒤
부분 HOLD를 적용한다. `before_note_link_discrepancy_hold`에는 그 시점 row 전체를,
`note_link_discrepancy_hold`에는 검증된 부분 지적을 보존한다. 최종 disposition은
`HOLD_FOR_LEGAL_REVIEW`이며, 앞선 `DELETE`/`REPLACE`는 더 강한 조치로 유지한다.
기존 blocker·key opinion·choice finding·author/independent provenance는 삭제하거나
새 전체 감사 결과로 바꾸지 않는다. 기존 또는 새 default selection에 교집합이
있으면 build가 실패하며 자동 default 복귀나 RELEASED 승인은 없다.
Selection은 이 builder의 derived 출력이므로 notice metadata만 재생성된 미커밋 파일은
허용한다. HEAD의 default와 현재 작업 파일·새로 계산한 default를 모두 검사하여 어느
쪽에든 11개 ID가 들어오면 실패한다. 이를 원 backlog/report/alignment/state의
커밋 바이트 검사를 우회하는 예외로 사용하지 않는다.

`build_representative_rewrites.archive_review_notices()`는 기존 notice를 기존
validator로 먼저 검증한 뒤, 전용 `NOTE_LINK_DISCREPANCY_HOLD` 형식으로 경고를
합친다. 기존 5개 notice의 reason/source/history 전체는 `previous_notices`에
남기고 새 6개에도 경고를 만든다. 각 ID는 현재 notice 목록에 한 번만 나타난다.
경고는 cashier의 무면허 사실이 보기에 없는데 해설이 추가한다는 부분 불확정성과
전체 문항 정답은 이번 검토에서 평가하지 않았다는 `NOT_ASSESSED`를 표시한다.
기존 author review를 흉내 내어 validator를 우회하지 않는다.

이 코드 변경은 bank 2,346개, 원문/정답/풀이 이력/bookmark, 원보고서/backlog/queue,
노트 본문, canonical rules/audits를 수정하지 않는다. Controller가 통합한 뒤 기존
전체 재생성 절차로 ledger·selection·공개 payload를 함께 갱신해야 공개 표시에도
반영된다. 이 worker는 generated 파일이나 원 registry를 쓰지 않는다.

검증:

```sh
python -m pytest -q tests/test_note_question_discrepancies.py
```
