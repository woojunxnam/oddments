# 본문을 유지하는 census 누락 보완과 새 독립 감사

이 경로는 이미 통합된 독립 감사의 `OMISSIONS_FOUND`를 저자가 보완한 뒤,
수정 census 전체를 새 독립 감사에 배정하는 engineering 도구다. 등록 자체는
누락 해소나 법규 KEEP의 증거가 아니다. Question/canonical release credit는 0이다.
본문 변경과 기존 독립 법규 HOLD·SOURCE_BLOCKED의 해소는 이 경로의 범위 밖이다.
기존 controller의 root-only checkpoint, lease/token, worker Git 범위·정확 commit,
source raw SHA, actor/session, 제출·순차 통합 검사는 계속 적용된다.

## 보존과 현재 credit

원래 multi-unit job, 보고서, result envelope, census와 공식 증거 바이트는
수정하거나 삭제하지 않는다. 새 version record는 이전 통합 job 전체 canonical
SHA와 해당 절의 body/census/unit/claim binding, 보고서·result raw SHA를 고정한다.
큐에는 `reassessments` 항목과 한 절짜리 새 job만 append한다. 재등록은 같은
record 경로·바이트일 때 멱등적이며 같은 절을 일반 `plan`으로 중복 배정할 수 없다.
다음 보완본은 가장 최근 통합 job을 parent로 삼고 실제 새 delta가 있어야 한다.
다른 절의 보완본들은 모두 최초 QUEUED 상태인 동안 함께 등록할 수 있다.
Claim이 시작된 뒤에는 해당 wave 통합을 끝내고 추가 등록한다.

등록 직후 수정 절은 `PENDING_REASSESSMENT / LEGAL_HOLD`,
`current_review_valid: false`, `requires_review: true`가 된다. 공개 notes와 derived
adapter의 경고·daily 제외가 유지된다. 이전의 COMPLETE/KEEP를 승계하지 않는다.
원래 batch의 다른 절은 binding이 같으면 현재 credit를 유지한다. 새 결과가
SUBMITTED인 동안도 현재 credit는 0이며, INTEGRATED 후 최신 버전 하나만 센다.
기존 7개 body content KEEP는 계속 별도 metric이다.

공개 metadata의 `review_history`는 원래 누락·법규 보류·근거 링크를 남긴다.
`pending_census_reassessment_units`와 `historical_review_records`는 현재 처리 수와
분리된다. Pending의 안전 HOLD는 현재 독립 감사 법규 HOLD 수로 세지 않는다.
공개 consumer는 현재 HEAD의 커밋된 원본 파일과 캡처한 raw SHA를 검증하므로
옛 worker branch/Git object가 없는 shallow checkout에서도 이력을 읽는다.
Controller의 통합 검사는 원래 worker branch와 Git object를 계속 필요로 한다.

## Root의 version record

Root는 현재 wave를 모두 통합한 후, **원래 census를 보존하면서** 새 경로의
single-unit census를 작성한다. 해당 unit 실제 body SHA가 모든 단계에서 같아야 한다.
본문 snapshot은 원래 ledger의 `atomic_census_notes_revision`을 그대로 사용한다.
새 census 최상위 `author_provenance`는 실제 correction author의
`{"actor_id": "...", "session_id": "..."}`이며 version record와 정확히 같아야 한다.
원본과 수정본의 알려진 body/source 작성자를 모두 새 job의 제외 이력에 남긴다.
별칭은 root가 기존 claim 명령의 `--known-author`로 추가한다.

새 JSON record는 다음 필드를 가진다. 경로들은 repository-relative이다.
이 문서는 실제 audit/job/census record를 생성하지 않는다.

```json
{
  "schema_version": 1,
  "purpose": "CENSUS_ONLY_OMISSION_REASSESSMENT",
  "reassessment_id": "고유한-version-id",
  "unit_id": "대상-unit",
  "body_sha256": "원래 실제 body SHA",
  "previous_job_id": "가장 최근 통합 job",
  "previous_job_sha256": "queue.digest(previous_job)",
  "previous_binding": "previous_job.unit_bindings[unit_id]의 전체 object",
  "previous_result": {"path": "원래 result_path", "raw_sha256": "원래 result_sha256"},
  "previous_report": {"path": "원래 evidence.path", "raw_sha256": "원래 evidence.raw_sha256"},
  "previous_ledger_fields": "아래의 원래 ledger fields 전체 object",
  "replacement": {
    "census_path": "새 immutable census 경로",
    "census_sha256": "새 census raw SHA",
    "notes_revision": "원래 atomic_census_notes_revision"
  },
  "author_provenance": {"actor_id": "실제 작성자", "session_id": "실제 작성 세션"},
  "change_basis": "실제 독립 누락 지적을 보완한 설명",
  "claim_mapping": {"모든 원래 claim ID": ["수정본의 대응 claim ID"]},
  "added_claim_ids": ["mapping 밖의 정확한 신규 claim ID"],
  "changed_claim_ids": ["mapped record가 원래 record와 달라진 수정본 ID, 정렬 순서"],
  "omission_resolutions": [{
    "omission_sha256": "각 원래 omission 문자열 UTF-8 바이트 SHA",
    "claim_ids": ["실제 새 proposition을 가진 claim ID"],
    "explanation": "해당 누락을 어떻게 열거했는지 설명"
  }]
}
```

설명용 문자열인 `previous_binding`과 `previous_ledger_fields`에는 실제 object를 넣는다.
Ledger fields는 `notes_census_reassessment.LEDGER_FIELDS`의 정확한 키 집합이다.
즉 unit/chapter/body SHA, atomic complete/status/source/revision/claim IDs/blocked count다.

Mapping은 모든 원명제를 빠짐없이 보존하고 수정본 ID를 중복 없이 포괄한다.
각 원래 statement는 공백 정규화 후 mapped claim 중 적어도 하나에 그대로 남아야 한다.
원문 뜻을 다른 명제로 교체하는 경로가 아니다. 분리·추가한 새 proposition이 있더라도
원래 proposition을 지울 수 없다. ID·raw whitespace·출처 metadata만 바꾼 등록은
실제 delta로 인정하지 않는다. 새 claim이 원래 proposition을 그대로 반복해도 거부한다.
모든 omission의 정확한 SHA를 실제 새/변경 proposition과 연결해야 한다. 설명만으로
의미적 충분성을 증명할 수 없으므로 fresh auditor가 전문과 최종 census를 다시 읽는다.

원래 claim의 LEGAL_HOLD 또는 SOURCE_BLOCKED는 mapping 대상마다 원래 finding,
blocker, 원보고서 SHA와 함께 새 job의 `carried_legal_blockers`에 남는다. 법규 상태를
KEEP으로 올릴 수 없다. HOLD는 HOLD로, BLOCKED는 BLOCKED 또는 HOLD로만 제출된다.
순수 누락 HOLD이고 모든 기존 claim이 KEEP였던 절은 fresh audit 후에만 KEEP 가능하다.

## Root의 가동 순서

1. 기존 wave를 전부 통합한다. 원래 queue와 census·보고서·공식 증거를 보존한다.
2. 새 single-unit census와 version record를 새 경로에 작성하고 커밋한다.
   이 단계에서는 기존 ledger 선택을 그대로 둔다.
3. Controller worktree에서 다음 명령을 실행하고 변경된 queue를 커밋한다.

   ```sh
   python scripts/note_review_queue.py --actor /root reassess --record reports/full-corpus-review/NEW-VERSION.json
   ```

4. 기존 전체 재생성 절차를 실행한다. `registered_specs(root, effective_notes)`가
   명시적 per-unit supersedence를 builder에 추가하고, freshly computed ledger를
   metadata 검증에 전달하므로 두 번 빌드할 필요가 없다. 기존 보호 annotation
   migration의 raw export SHA 갱신 등 기존 root release 절차를 따른다.
   생성물·선택된 새 ledger를 커밋한 후 claim한다. 새 census 바이트는 이미
   registration의 `base_commit`에 있으므로 worker가 정확한 최종 census를 읽는다.
5. 기존 runbook대로 새 실제 actor/session을 claim하고 worktree를 만든다.
   Census correction author와 원래 body/source author는 claim할 수 없다.
   새 reviewer는 최종 census 전부와 원래 omission을 재검토한다.
6. 기존 submit → worker evidence cherry-pick → envelope 원바이트 commit → 순차
   integrate → checkpoint commit → regen 절차를 따른다. Lease 회복과 멱등성도 같다.

Claim은 실제 선택 ledger가 새 binding과 같을 때만 가능하다. 등록 직후 최초
QUEUED 상태에는 빌드 전의 정확한 parent binding도 읽기용으로 허용해 PENDING
경고를 먼저 표시한다. 한 번이라도 claim한 뒤에는 parent census로 되돌아간
ledger를 허용하지 않는다. 본문 변경, 임의 제3 census, 기존 증거/record 변조는 실패한다.

새 보고서의 각 record에는 기존 필드 외에 아래 object가 필요하다.

```python
record['reassessment_review'] = {
    **job['reassessment_review'],
    'final_census_read_completely': True,
    'all_original_omissions_reassessed': True,
    'all_original_propositions_preserved': True,
}
# carried blocker가 있는 각 claim은 정확한 원래 목록을 포함한다.
claim['inherited_legal_blockers'] = job['carried_legal_blockers'][unit_id][claim_id]
```

확인하지 않은 경우 true를 만들지 않는다. 누락이 남으면 기존 규약대로
OMISSIONS_FOUND와 구체적인 omissions를 남긴다. 완전성 COMPLETE와 기존 법규
HOLD/BLOCKED는 공존할 수 있으며 처리 coverage는 법규 PASS가 아니다.

검증 명령:

```sh
python -m pytest -q tests/test_notes_census_reassessment.py tests/test_note_review_queue.py tests/test_notes_independent_metadata.py
```
