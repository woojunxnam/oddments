# 독립 노트 완전성·법규 감사 큐

`scripts/note_review_queue.py`는 노트 단위를 독립 감사자에게 배정하고 제출과
Git 통합을 재개하기 위한 별도 도구다. 질문 큐, 저자 census, 노트 본문,
생성 산출물과 canonical release 상태를 수정하지 않는다. 기본 상태 파일은
`reports/full-corpus-review/independent-notes-work-queue.json`이며 다른 큐를
고르는 `--state` 옵션은 없다. 도구 설치만으로 실제 작업을 생성하지 않는다.

## 입력과 배정

Root는 현재 저자 census와 ledger, 활성화 원본을 먼저 커밋한다. 도구는
`notes-unit-ledger.jsonl`의 순서대로 기본 5절씩 배정한다. `load_notes()`가
합성한 실제 모든 단원과 ledger의 단원 집합·actual body SHA를 대조한다.
아직 `atomic_claim_census_complete`가 true가 아닌 단원은 배정하지 않는다.

각 배정은 본문 SHA, census 경로/raw SHA, census unit record SHA,
선택된 ledger binding fields의 SHA, 모든 claim의 canonical record SHA,
기존 source-blocked claim IDs와 알려진 작성자 식별자를 보존한다. Source-blocked
명제도 감사 대상이다. Census 전체의 중복·orphan claim과 알 수 없는 단원,
선택 단원의 누락·중복 claim을 거부한다.

Ledger raw SHA도 배정 당시 provenance로 남긴다. 다른 단원의 새 census 등록이나
관련 없는 ledger annotation은 선택 단원의 binding이 그대로면 진행 중 배정을
무효화하지 않는다. 선택 단원의 body/census/claim/ledger binding 변경은 거부한다.
저자 수정을 독립 감사 결과에 자동 승계하지 않는다. 본문이 그대로이고 통합된
독립 감사에서 발견한 census 누락만 보완할 때는
[append-only 재감사 절차](NOTES_CENSUS_REASSESSMENT.md)를 따른다.
원래 해시·보고서는 보존하고 해당 절의 현재 credit를 즉시 PENDING/HOLD로 내린다.
본문 변경과 기존 법규 보류 해소는 그 경로에서도 허용하지 않는다.

H/I/J/M의 기존 current-body content KEEP는 별도 통계다. 기존 7개 KEEP를
이번 독립 완전성 감사 완료로 세지 않는다. 새 큐의 완료 수는 0에서 시작한다.

`w6-b-16` 같은 0 legal claim 절은 다음 저자 증거가 모두 있을 때만 배정된다:
unit의 `nonlegal_inventory_only: true`, 전문 읽음, 명시적 nonlegal 법규 상태,
최상위 `editorial_nonlegal_inventory[unit_id]`의 분류·항목 목록·0개 확인·완료 근거.
임의의 빈 census는 완료로 인정하지 않는다. 독립 감사자는 이 분류와 법적
누락 여부를 다시 확인해야 한다.

## Root만 수행하는 상태 변경

`--actor /root`와 checkpoint에 고정된 controller worktree가 필요하다. 파일
잠금과 atomic replace로 동시에 실행된 controller 프로세스의 업데이트를
직렬화하며, 실패한 명령은 checkpoint를 쓰지 않는다. Worker는 자신의
브랜치에서 감사 증거만 작성하고 root 상태 파일을 직접 수정하지 않는다.

Actor 문자열이나 `independent_of_authors: true` 자체는 신원·독립성의 증명이
아니다. Root가 실제 새 actor/session을 배정하고 알려진 작성 이력을 확인한
근거를 `--independence-basis`에 남긴다. 도구는 이 root 등록값과 이후 제출의
actor/session/auditor instance가 정확히 같은지 확인한다. 알려진 census/body/source
작성자와 같은 actor·session·instance는 거부한다. 파일에 없는 작성자 별칭은
root가 `--known-author`로 추가한다. 독립성 표시는
`CONTROLLER_ATTESTED_DECLARATION_NOT_IDENTITY_PROOF`로 유지한다.

```sh
# Root의 controller worktree에서만 실행한다. 상태 변경 후 상태 JSON을 커밋한다.
python scripts/note_review_queue.py --actor /root plan --batches 4
python scripts/note_review_queue.py --actor /root claim \
  --worker /root/fresh_note_auditor --session actual-fresh-session-id \
  --auditor GPT --auditor-instance actual-fresh-auditor-instance \
  --known-author /root/original_note_author \
  --independence-basis '실제 새 세션을 배정하고 해당 절의 작성 이력과 대조함'
python scripts/note_review_queue.py --actor /root worktree \
  --job JOB --token TOKEN --destination /workspace/notes-audit-worker
python scripts/note_review_queue.py --actor /root heartbeat --job JOB --token TOKEN
python scripts/note_review_queue.py --actor /root recover
python scripts/note_review_queue.py progress
```

Claim 출력의 job object를 해당 worker에게 전달한다. Worktree는 배정 시
고정한 `base_commit`에서 만들어지고 정확한 attempt branch를 사용한다.
재접속은 같은 branch/session으로 멱등 처리한다. Lease 만료 후 recover하면
새 token과 attempt branch가 필요하다. 오래된 token은 heartbeat·worktree·submit에
사용할 수 없다. Root는 resume 시 저장된 상태와 실제 세션을 대조하며
중단을 완료로 추정하지 않는다.

## Worker 감사 증거

Worker는 배정된 실제 본문 전체와 census의 모든 claim을 읽고, 누락 여부와
각 claim의 현재 공식 근거를 각각 판단한다. 법규 판단을 하지 못한 항목도
삭제하지 않고 이유와 함께 `SOURCE_BLOCKED` 또는 `LEGAL_HOLD`로 기록한다.

Worker의 모든 커밋 경로는
`reports/full-corpus-review/independent-notes/` 아래에 둔다. 새 공식 원문,
retrieval 기록과 감사 보고서를 이 경로에 보존한다. 기존 본문·census·loader·
질문·queue·frontend·generated file을 수정하지 않는다. Controller는 worker의
전체 commit range를 확인하므로 금지 경로를 수정했다가 되돌린 이력도 거부한다.

감사 보고서 JSON의 필수 구조:

```json
{
  "stage": "independent-notes",
  "independent_of_authors": true,
  "actor_provenance": {"actor_id": "ROOT가 등록한 actor", "session_id": "등록한 session"},
  "auditor": "GPT",
  "auditor_instance": "등록한 instance",
  "canonical_audit": false,
  "canonical_release_credit": 0,
  "question_audit_credit": 0,
  "records": [{
    "unit_id": "배정된 unit",
    "binding": "job.unit_bindings[unit_id]의 전체 object를 그대로 사용",
    "body_read_completely": true,
    "completeness": "COMPLETE",
    "completeness_method": "전문과 모든 열거 명제를 읽고 누락을 찾은 실제 방법",
    "omissions": [],
    "legal_status": "SOURCE_BLOCKED",
    "claims": [{
      "claim_id": "배정된 claim",
      "claim_record_sha256": "배정된 canonical record SHA",
      "claim_read_completely": true,
      "legal_status": "SOURCE_BLOCKED",
      "finding": "이 명제에 대해 실제 확인한 결과",
      "blocker": "확정할 수 없는 근거와 범위",
      "authorities": []
    }]
  }]
}
```

예시의 `binding` 문자열은 설명용이다. 실제 보고서에는 배정된 object를 넣는다.
모든 unit과 claim은 누락·중복·추가 없이 정확히 한 번씩 있어야 한다.
`KEEP` claim은 `PUBLIC_OFFICIAL`, HTTPS `official_url`, `exact_section`,
`law_checked_date`, `version_or_effective_date_status`, 로컬 `evidence_path`와
그 원문 바이트 `evidence_sha256`를 가진 authority가 필요하다. 개별 시행일이
미확정이면 그 한계를 상태 문자열에 명시한다. 근거·verdict를 모르는 항목에
임의의 PASS를 만들지 않는다.

누락을 찾으면 `completeness: OMISSIONS_FOUND`와 구체적인 `omissions`를
기록하고 unit은 `LEGAL_HOLD`로 둔다. 기존 claim이 전부 KEEP여도 누락을
감출 수 없다. 누락 명제를 author census에 직접 추가하거나 기존 hash를 바꾸지
않는다. Unit 법규 요약은 claim들 중 HOLD, SOURCE_BLOCKED 여부에서 계산된다.

0 claim 절은 `claims: []`와 함께
`nonlegal_classification_review: {"confirmed": true, "finding": "독립적으로 확인한 이유"}`를
기록해야 한다. 분류를 확인하고 누락이 없으면 unit 법규 상태는
`NOT_APPLICABLE_NONLEGAL`이며 법규 KEEP로 세지 않는다. 법률 명제를 찾으면
분류를 `confirmed: false`로 두고 `OMISSIONS_FOUND/LEGAL_HOLD`로 기록한다.

## 제출·순차 통합

먼저 worker branch에서 원문·보고서를 커밋하고 그 정확한 HEAD SHA를 구한다.
그 다음 아래 result envelope를 만든다. 자기 commit SHA를 자기 바이트 안에
넣을 수 없으므로 envelope는 **worker branch에서 추가 커밋하지 않는다**.
Root가 제출 시 raw SHA를 checkpoint에 보존하고 통합 시 같은 바이트를 커밋한다.

Envelope는 보고서와 동일한 stage/provenance/독립성/credit 필드와 다음을 가진다:

- `worker_commit`: 방금 만든 evidence commit의 40자리 SHA. 실제 worker branch
  HEAD와 같아야 한다.
- `unit_hashes`: 배정된 모든 `unit_id → body_sha256`의 정확한 object.
- `evidence`: `{"path": ".../감사보고서.json", "raw_sha256": "보고서 raw SHA"}`.
- `result_path`: `reports/full-corpus-review/independent-notes/JOB-result.json`.
- `results`: 정확한 단원 집합의 `{unit_id, completeness, legal_status}` 목록.
  상세 보고서의 요약과 정확히 같아야 한다.

```sh
python scripts/note_review_queue.py --actor /root submit \
  --job JOB --token TOKEN --result /workspace/notes-audit-worker/result-envelope.json
# 검토한 evidence commit을 root가 순서대로 cherry-pick한다.
# envelope 원본을 result_path로 복사하고 그 바이트를 root에서 커밋한다.
python scripts/note_review_queue.py --actor /root integrate --job JOB
python scripts/note_review_queue.py progress
# 변경된 independent-notes-work-queue.json을 커밋한다.
```

Submit은 worker commit의 보고서·공식 증거 raw SHA, 모든 claim/body/census binding과
provenance를 먼저 검사한다. Integrate는 assignment sequence를 지키며 root HEAD에
동일 증거와 result envelope 바이트가 실제 커밋됐는지 다시 확인한다. 충돌 없는
동일 raw 제출과 동일 통합의 재실행은 이벤트·credit를 중복 생성하지 않는다.
다른 바이트로 재제출하면 의미가 같아도 거부한다. 제출 후에는 worker branch
HEAD와 증거를 보존한다. 다음 wave plan은 현재 wave 전체가 통합된 후 가능하다.

## Root가 나중에 등록할 인터페이스

이 변경은 `build_full_corpus_review.py`, node/frontend와 generated files를
연결하거나 바꾸지 않는다. Root는 별도 변경으로
`inventory(root)` → `progress(state, inventory, root)`를 호출할 수 있다.
`validate_state(state, root)`와 실제 Git 증거 재검증을 건너뛰고 `INTEGRATED`
문자열만 세면 안 된다. CLI의 read-only progress는 이 검증을 수행한다.

보고서는 전체 단원 수, 저자 열거 수, 미열거 수, 기존 content KEEP 수,
독립 completeness/legal 처리 수, COMPLETE/OMISSIONS_FOUND 및 KEEP/HOLD/
SOURCE_BLOCKED/NONLEGAL 수를 따로 제공한다. 처리 coverage는 법규 PASS가
아니며 question/canonical credit는 항상 0이다. Root가 ledger에 별도 독립
노트 감사 metadata를 연결할 때 원래 author binding fields는 덮어쓰지 않는다.

검증: `python -m pytest -q tests/test_note_review_queue.py tests/test_review_queue.py`.
테스트는 임시 Git 저장소·worktree에서만 큐를 만들며 실제 root의 notes 작업을
plan하거나 claim하지 않는다.
