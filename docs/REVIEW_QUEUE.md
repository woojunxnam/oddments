# 전체 코퍼스 검토 작업 큐

`scripts/review_queue.py`는 작업 배정과 재개를 관리합니다. 법률 검증, 독립 감사, release gate는 기존 정책과 canonical validator가 담당합니다. 큐의 `INTEGRATED`는 증거 파일을 Git에 통합했다는 뜻이며 검토 합격을 뜻하지 않습니다.

## 단일 작성자와 영속 상태

`--stage author|independent-legacy`로 단계를 선택하며 생략하면 기존 `author` 동작을 유지합니다. 각 단계는 별도 체크포인트를 사용합니다.

| stage | 기본 체크포인트 (`reports/full-corpus-review/` 아래) | purpose |
| --- | --- | --- |
| `author` | `work-queue.json` | `AUTHOR_WORK_SCHEDULER_NOT_RELEASE_CERTIFICATION` |
| `independent-legacy` | `independent-legacy-work-queue.json` | `INDEPENDENT_LEGACY_WORK_SCHEDULER_NOT_RELEASE_CERTIFICATION` |

다른 단계의 기본 경로를 `--state`로 지정하면 생성 전에도 실패합니다. 사용자 지정 경로도 저장된 purpose와 stage가 일치해야 하며, 다른 단계의 job이 섞인 체크포인트를 거절합니다. 각 단계에 하나의 권위 체크포인트를 유지해야 합니다. 사용자 지정 경로에 같은 단계의 별도 큐를 복제해 병렬 배정하는 운영은 지원하지 않습니다.

통합 담당자만 체크포인트를 갱신하고 Git branch에 commit/push합니다. 다음 세션은 해당 branch를 fetch한 뒤 이 파일로 재개합니다. 로컬 advisory lock과 atomic replace는 같은 체크포인트의 동시 로컬 쓰기 및 중간 실패를 방지합니다. **다른 머신의 동시 controller는 지원하지 않습니다.** Git에서 한 명의 통합 담당자를 정하고, 최신 remote 상태를 fetch한 뒤 이어받아야 합니다. non-fast-forward push를 강제 갱신하지 않습니다.

작업자는 각자의 worktree/branch에서 배정된 ID와 별도 결과 보고서만 수정합니다. 공유 `question-ledger.jsonl`, `progress.json`, site payload, generated report를 작업자 branch에서 재생성하지 않습니다. 통합 담당자가 결과를 순서대로 cherry-pick하고 기존 validator와 artifact generator를 실행합니다.

## 첫 배치와 이후 wave

```bash
python scripts/review_queue.py plan
python scripts/review_queue.py claim --worker author-session-1
python scripts/review_queue.py worktree --job JOB --token TOKEN --destination /workspace/review-worker-1
```

`author`의 첫 배치는 `MA-EXP-0385–0424` 40개입니다. 이미 검토된 ID나 원장 누락을 발견하면 자동으로 다른 ID를 끼워 넣지 않고 실패합니다. 현재 질문 원문 hash도 원장과 대조하므로 stale 원장은 배정을 허용하지 않습니다.

첫 배치의 증거를 통합하고 파이프라인을 검증한 뒤 다음 명령으로 최대 4개 작업을 만듭니다.

```bash
python scripts/review_queue.py plan --batches 4 --size 40
```

이후 ID는 authoritative question ledger의 `NOT_REVERIFIED_IN_FULL_CORPUS_REVIEW` 집합에서 정렬해 선정합니다. 기존 큐에 배정된 ID는 다시 배정하지 않으며, 앞 wave가 전부 통합되기 전에는 새 wave를 만들지 않습니다. 잔여량이 적으면 작은 배치가 생성됩니다. 이 작업 배치 크기는 canonical `INITIAL_BATCH` audit의 30–40개 요건을 변경하지 않습니다.

독립 legacy 단계는 첫 배치부터 원장의 `checked_at`가 비어 있지 않고 `independent_legacy_legal_assessment`가 없는 ID만 정렬해 선정합니다. `MA-EXP-0385–0424` 특례를 적용하지 않으며, 이미 독립 판정이 있는 ID는 부정적 판정·차단 판정이어도 다시 배정하지 않습니다. 배정 수는 `--batches`·`--size`를 따릅니다.

```bash
python scripts/review_queue.py --stage independent-legacy plan --batches 4 --size 40
python scripts/review_queue.py --stage independent-legacy claim --worker ACTUAL_ACTOR_ID
python scripts/review_queue.py --stage independent-legacy worktree --job JOB --token TOKEN --destination /workspace/independent-worker-1
```

stage는 모든 명령에서 같은 값으로 지정해야 하며 global option이므로 subcommand 앞에 둡니다. 독립 job ID는 `review-independent-legacy-...`를 사용합니다. 기존 author의 `review-...` ID·hash·lease token·이벤트 이력은 바꾸지 않습니다. 같은 ID의 author 배정과 독립 배정은 서로 다른 단계의 작업이므로 허용하지만, 같은 단계 안에서는 중복 배정하지 않습니다. 독립 작업자는 해당 current content의 작성·수정을 하지 않은 실제 별도 actor여야 합니다.

## 임대 만료와 재시도

claim 기본 임대는 60분이며 `--minutes`로 1–1440분을 지정할 수 있습니다. 재접속한 동일 작업자는 살아 있는 기존 할당을 받습니다. 작업 도중 다음 명령으로 임대를 연장합니다.

```bash
python scripts/review_queue.py heartbeat --job JOB --token TOKEN --minutes 60
python scripts/review_queue.py recover
```

기한이 지난 작업은 `QUEUED`로 돌아갑니다. 다음 claim은 새 attempt와 token을 발급하며 별도 attempt branch를 지정합니다. 만료된 작업자의 token으로 제출할 수 없습니다. 이전 attempt branch는 삭제하지 않고 복구 자료로 보존합니다. `SUBMITTED` 결과는 임대 만료로 자동 재작업되지 않습니다.

## 증거 제출과 순차 통합

### 작업자 환경이 사라진 경우의 명시적 임대 회수

아직 만료되지 않은 임대를 만료된 것으로 기록하지 않는다. 작업자 디스크가
실제로 사라졌거나 작업자가 더 이상 제출할 수 없음을 확인한 root controller만
현재 token과 구체적인 사유로 임대를 회수할 수 있다.

```bash
python scripts/review_queue.py --stage independent-legacy --actor /root revoke \
  --job JOB --token CURRENT_TOKEN --reason '기존 작업자 디스크를 복구할 수 없어 새 실제 세션에 재배정'
python scripts/review_queue.py --stage independent-legacy claim --worker ACTUAL_NEW_ACTOR
```

`LEASE_REVOKED` event는 실제 회수 시각, 이전 작업자·branch·임대기한·attempt와
token SHA를 보존한다. 기존 event와 증거를 지우지 않으며 `LEASED`만 `QUEUED`로
되돌린다. 이전 token은 즉시 무효이며 새 claim은 attempt와 branch를 새로 만든다.
원 작업자의 provenance를 새 reviewer의 provenance로 가장하지 않는다. 제출·통합된
결과는 회수할 수 없다. 같은 token/사유로 아직 QUEUED인 동일 attempt에 재요청하면
멱등적이며, 다른 사유나 새 attempt에 대한 옛 token 요청은 거절한다.

노트 큐에도 같은 명령을 사용한다. 실제 controller checkpoint 위치에서 실행하며
기존 본문·census binding, 부모 검토의 HOLD와 author 제외 규칙은 변경하지 않는다.

```bash
python scripts/note_review_queue.py --actor /root revoke \
  --job JOB --token CURRENT_TOKEN --reason '기존 작업자 디스크를 복구할 수 없어 새 실제 세션에 재배정'
```

작업자는 기존 문항별 검토 보고서를 작성하고 commit합니다. controller에 전달할 별도 manifest는 다음 형식입니다. 같은 보고서가 여러 ID를 포함하면 path와 파일 SHA를 각 ID에 반복 참조할 수 있습니다. manifest 자체는 worker commit 뒤에 작성해도 됩니다.

```json
{
  "question_hashes": {"MA-EXP-0385": "배정된 원문 SHA256"},
  "worker_commit": "실제 40자리 worker commit SHA",
  "results": [
    {
      "question_id": "MA-EXP-0385",
      "disposition": "SOURCE_BLOCKED",
      "evidence_path": "reports/full-corpus-review/worker-results.json",
      "evidence_sha256": "보고서 파일 바이트 SHA256"
    }
  ]
}
```

manifest의 ID와 hash는 배정과 정확히 일치해야 합니다. `author` manifest의 각 ID에 `AUTHOR_REVIEWED`, `HOLD`, `SOURCE_BLOCKED`, `NEEDS_REMEDIATION` 중 하나와 증거 참조가 있어야 합니다. 이는 큐 분류이며 기존 보고서의 세부 legal/editorial disposition을 대체하지 않습니다. 검토가 미완료라면 미완료 이유를 증거 보고서에 명시하고 차단 상태를 사용합니다. 큐는 증거의 법률적 충실성을 자동 인증하지 않습니다.

`independent-legacy` manifest에는 다음 top-level 필드를 추가해야 합니다. `actor_id`는 claim의 `--worker`와 일치하는 실제 작업자 출처이며, `session_id`는 실제 실행 세션/스레드 식별자입니다. `auditor_instance`는 실제 감사 세션의 지속적인 provenance입니다. 같은 세션을 새 이름으로 바꿔 독립성을 부풀리지 않습니다.

```json
{
  "stage": "independent-legacy",
  "independent_of_authors": true,
  "auditor": "GPT",
  "auditor_instance": "실제 독립 감사 세션의 기존 식별자",
  "actor_provenance": {
    "actor_id": "ACTUAL_ACTOR_ID",
    "session_id": "실제 실행 세션 또는 스레드 식별자"
  }
}
```

독립 단계의 disposition은 `INDEPENDENT_ASSESSED`, `HOLD`, `SOURCE_BLOCKED`, `NEEDS_REMEDIATION`만 허용합니다. `AUTHOR_REVIEWED`를 허용하거나 author credit을 만들지 않습니다. `INDEPENDENT_ASSESSED`는 근거를 갖춘 독립 판단을 끝냈다는 큐 분류이며 legal KEEP·정답 YES·realism PASS·canonical release의 의미가 아닙니다. 미판정·차단 상태를 완료 판정으로 포장하지 않습니다.

독립 증거 파일은 JSON이며 manifest와 동일한 `independent_of_authors`, `auditor`, `auditor_instance`, `actor_provenance`를 담아야 합니다. `canonical_audit: false`, `canonical_release_credit: 0`도 명시해야 합니다. 문항별 `records[]`에는 해당 ID가 정확히 한 번 있고 `record_sha256`이 배정의 current 원문 hash와 일치해야 합니다. 기존 legacy 보고서 형식의 `legal_review`와 실제 선택지별 근거·차단 사유를 함께 기록합니다. 여러 ID가 같은 보고서를 참조할 수 있습니다. submit에서 배정·분류·provenance 선언을 확인하고, integrate에서 Git에 저장된 보고서 원본 바이트와 그 안의 provenance·문항 hash를 검증합니다.

**실제 독립성은 식별자만으로 증명할 수 없습니다.** Controller는 actor/session 선언의 존재·일관성을 검사하지만, 서로 다른 worker/actor/auditor 이름이 실제로 같은 작성자 세션인지 자동으로 입증하거나 배제하지 못합니다. 통합 담당자는 실제 실행 provenance와 해당 원문의 작성·수정 이력을 대조해 별도 actor인지 확인해야 합니다. 작성자/편집자가 자신이 작성·수정한 current content를 새 이름으로 자가 감사하는 것은 금지되며, 체크포인트 통과가 이를 허용하지 않습니다. 기존 보고서를 인수할 때도 실제 출처를 확인해야 하며 소급해 독립 세션·claim 이력을 만들어서는 안 됩니다.

```bash
python scripts/review_queue.py submit --job JOB --token TOKEN --result /tmp/result-manifest.json
# 통합 담당자: 순서대로 worker commit cherry-pick, 보고서/validator 검토, commit
python scripts/review_queue.py integrate --job JOB
python scripts/review_queue.py progress
```

submit은 동일 token·동일 결과의 반복 제출에 멱등적이며 상충하는 재제출은 거절합니다. integrate는 배정 순서를 강제하고, 실제 원문 hash와 worker commit·현재 HEAD에 있는 증거 바이트 및 SHA를 비교합니다. 통합 후 체크포인트도 commit/push해야 원격 재개가 가능합니다. 보호된 원문을 직접 변경하는 방식의 작업은 해당 hash 검사를 통과하지 않으므로 별도 신규 ID나 기존 governance의 정식 수정 절차를 사용해야 합니다.

진척은 author review와 note census를 원장에서 별도로 계산합니다. 독립 법률 감사·실질 개선·배포는 별도 근거 검증이 필요하므로 이 큐만으로 산출할 수 없으면 `percent: null`과 상태를 보고합니다. 처리한 job 수를 이들 비율로 환산하지 않습니다.

## 최초 도입 기록

2026-11-03 첫 작업에서는 controller가 구현되기 전에 통합 담당자가 검토 작업자들을 먼저 시작했습니다. 이는 영속 큐를 통한 최초 claim이 아니므로 소급하여 claim 시각이나 임대 이력을 만들면 안 됩니다. 실제 controller 도입 시점에 첫 배치를 생성하고, 진행 중 자료의 출처와 Git commit을 보존해 인수하며, 이후 wave부터 worktree/token 절차를 적용합니다. 기존 작업을 인수하는 경우에도 실제 시각의 claim/submission과 정확한 문항 hash·증거 SHA를 기록합니다.

통합 manifest만 있고 권위 원장에 개별 검토 기록이 반영되지 않았다면 다음 plan은 실패한다. 통합된 ID를 단순 제외하여 미검토 문항이 영구히 빠지지 않도록, 보고서 등록과 원장 재생성을 먼저 완료해야 한다.

독립 단계에서는 통합된 모든 ID의 `independent_legacy_legal_assessment`가 권위 원장에 반영되어야 다음 plan이 가능합니다. author의 `checked_at`만으로 이 조건을 충족할 수 없습니다. HOLD·SOURCE_BLOCKED 등도 해당 실제 독립 판단·차단 기록을 등록한 뒤 재생성해야 하며, 이 기록의 존재가 독립 법률 합격 수를 뜻하지는 않습니다. 큐는 원장을 직접 고치지 않습니다. 기존 canonical 독립 감사·현실성·adjudication·release gate는 그대로 적용됩니다.
