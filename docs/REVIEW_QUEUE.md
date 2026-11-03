# 전체 코퍼스 검토 작업 큐

`scripts/review_queue.py`는 작업 배정과 재개를 관리합니다. 법률 검증, 독립 감사, release gate는 기존 정책과 canonical validator가 담당합니다. 큐의 `INTEGRATED`는 증거 파일을 Git에 통합했다는 뜻이며 검토 합격을 뜻하지 않습니다.

## 단일 작성자와 영속 상태

기본 체크포인트는 `reports/full-corpus-review/work-queue.json`입니다. 통합 담당자만 이 파일을 갱신하고 Git branch에 commit/push합니다. 다음 세션은 해당 branch를 fetch한 뒤 이 파일로 재개합니다. 로컬 advisory lock과 atomic replace는 같은 체크포인트의 동시 로컬 쓰기 및 중간 실패를 방지합니다. **다른 머신의 동시 controller는 지원하지 않습니다.** Git에서 한 명의 통합 담당자를 정하고, 최신 remote 상태를 fetch한 뒤 이어받아야 합니다. non-fast-forward push를 강제 갱신하지 않습니다.

작업자는 각자의 worktree/branch에서 배정된 ID와 별도 결과 보고서만 수정합니다. 공유 `question-ledger.jsonl`, `progress.json`, site payload, generated report를 작업자 branch에서 재생성하지 않습니다. 통합 담당자가 결과를 순서대로 cherry-pick하고 기존 validator와 artifact generator를 실행합니다.

## 첫 배치와 이후 wave

```bash
python scripts/review_queue.py plan
python scripts/review_queue.py claim --worker author-session-1
python scripts/review_queue.py worktree --job JOB --token TOKEN --destination /workspace/review-worker-1
```

첫 배치는 `MA-EXP-0385–0424` 40개입니다. 이미 검토된 ID나 원장 누락을 발견하면 자동으로 다른 ID를 끼워 넣지 않고 실패합니다. 현재 질문 원문 hash도 원장과 대조하므로 stale 원장은 배정을 허용하지 않습니다.

첫 배치의 증거를 통합하고 파이프라인을 검증한 뒤 다음 명령으로 최대 4개 작업을 만듭니다.

```bash
python scripts/review_queue.py plan --batches 4 --size 40
```

이후 ID는 authoritative question ledger의 `NOT_REVERIFIED_IN_FULL_CORPUS_REVIEW` 집합에서 정렬해 선정합니다. 기존 큐에 배정된 ID는 다시 배정하지 않으며, 앞 wave가 전부 통합되기 전에는 새 wave를 만들지 않습니다. 잔여량이 적으면 작은 배치가 생성됩니다. 이 작업 배치 크기는 canonical `INITIAL_BATCH` audit의 30–40개 요건을 변경하지 않습니다.

## 임대 만료와 재시도

claim 기본 임대는 60분이며 `--minutes`로 1–1440분을 지정할 수 있습니다. 재접속한 동일 작업자는 살아 있는 기존 할당을 받습니다. 작업 도중 다음 명령으로 임대를 연장합니다.

```bash
python scripts/review_queue.py heartbeat --job JOB --token TOKEN --minutes 60
python scripts/review_queue.py recover
```

기한이 지난 작업은 `QUEUED`로 돌아갑니다. 다음 claim은 새 attempt와 token을 발급하며 별도 attempt branch를 지정합니다. 만료된 작업자의 token으로 제출할 수 없습니다. 이전 attempt branch는 삭제하지 않고 복구 자료로 보존합니다. `SUBMITTED` 결과는 임대 만료로 자동 재작업되지 않습니다.

## 증거 제출과 순차 통합

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

manifest의 ID와 hash는 배정과 정확히 일치해야 합니다. 각 ID에 `AUTHOR_REVIEWED`, `HOLD`, `SOURCE_BLOCKED`, `NEEDS_REMEDIATION` 중 하나와 증거 참조가 있어야 합니다. 이는 큐 분류이며 기존 보고서의 세부 legal/editorial disposition을 대체하지 않습니다. 검토가 미완료라면 미완료 이유를 증거 보고서에 명시하고 차단 상태를 사용합니다. 큐는 증거의 법률적 충실성을 자동 인증하지 않습니다.

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
