# 독립 노트 감사의 공개 표시

`notes_independent_metadata.load_metadata(root, notes=None, ledger_raw=None)`는
읽기 전용 publication bridge다. 실제 `INTEGRATED` job만 읽으며
`SUBMITTED`, `LEASED`, `QUEUED`는 처리·완료 credit 0이다. 기존 H/I/J/M의
7개 content KEEP와 새 atomic census 완전성 감사는 별도 통계다. 저자 census
열거가 100%여도 독립 감사의 완료나 법규 KEEP를 뜻하지 않는다.

Controller의 `submit`/`integrate`, 원래 worker commit/branch 범위 검사와
actor/session 검사는 그대로다. 소비 측은 현재 HEAD에 커밋된 checkpoint,
result envelope, report와 모든 authority payload/text의 실제 바이트를 captured
raw SHA와 대조한다. 본문·선택 census·unit/claim record binding과 실제 감사
요약, actor/session 선언 및 root의 알려진 작성자·독립 배정 근거도 다시 확인한다.
Capture된 integration event가 없거나 순서가 맞지 않으면 거부한다.

소비 측은 과거 worker Git object나 local branch를 요구하지 않아 shallow CI
checkout에서도 읽을 수 있다. 이 경로는 controller가 수행한 과거 검사를
대체하거나 새 독립성 증명을 만들지 않는다. 현재 파일이 미커밋이거나 raw SHA,
선택 본문/census/claim 바인딩이 달라지면 실패한다. 보류를 KEEP로 승계하거나
stale 경고를 조용히 누락하지 않는다.

반환값은 `{'units': {unit_id: metadata}, 'progress': {...}}`다. 단원 metadata는
`completeness`, `legal_status`, `omissions`, 보류 claim의 `findings`, 원래 report와
result 경로/SHA, `notice`, `requires_review`를 제공한다. Progress는 processed,
COMPLETE/OMISSIONS와 KEEP/HOLD/BLOCKED/NONLEGAL를 따로 센다. 명시적인
method-only 0 claim 분류도 기존 queue의 독립 재확인 guard를 거친다.
Question/canonical credit는 항상 0이며 coverage를 법규 PASS로 표시하지 않는다.

`build_full_corpus_review.py`는 새 ledger를 계산한 바로 그 bytes를 helper에
전달하고 각 row의 `independent_atomic_census_review`와 progress의
`independent_note_completeness_legal_review`에 연결한다. `inventory(...,
ledger_raw=bytes)`는 이 읽기 전용 입력만 추가한 것이다. 추가 annotation는
기존 선택 단위 binding 대상이 아니므로 두 번 재생성해야 하는 순환이 없다.

`build_ultimate_notes.py`는 의미 데이터와 별도인 payload copy에 metadata를
붙인다. 본문, loaded flags, loader, 의미 해시 `e1519c0290ff220eb8251307e26340d76d394a7ec1f3e651194d4495a03f1824`는
유지한다. HTML·동적 reader·다운로드 Markdown에는 저자 source-blocked notice와
독립 누락·법규 보류를 구분해 표시하며 원래 감사 기록과 실제 지적을 연결한다.

Study/refresh 연결 API:

```python
from notes_independent_metadata import load_metadata, notices_for_units

metadata = load_metadata(ROOT, notes, ledger_raw=current_ledger_bytes)
item['independent_atomic_census_reviews'] = notices_for_units(
    item['note_units'], metadata['units'])
```

이 adapter는 경고 있는 절만 중복 없이 돌려준다. 카드 본문·원래 flags를
바꾸지 말고 표시용 notice와 report 링크로 렌더한다. 일반적인 새 법규 면책문이나
독립 PASS 배지를 만들지 않는다. Root가 study/refresh builder와 UI를 별도로 연결한다.

Root 가동 순서:

1. Controller가 순차 integrate한 checkpoint와 증거/result envelope를 커밋한다.
2. 전체 corpus ledger를 한 번 재생성한 후 notes/study/refresh를 재생성한다.
3. 새로운 protected migration의 `new_sha256`만 최종 Markdown raw SHA로
   갱신한다. 이전 migration와 원본·의미 해시는 바꾸지 않는다.
4. Corpus/builder drift 검사, 보호 검증 및 전체 QA를 수행한다.

핵심 검사:

```sh
python -m pytest -q tests/test_notes_independent_metadata.py tests/test_note_review_queue.py tests/test_review_queue.py
python -m py_compile scripts/notes_independent_metadata.py scripts/build_full_corpus_review.py scripts/build_ultimate_notes.py
node --check site/notes/notes.js
```

Fixture는 실제 C/F 보고서 바이트로 미통합 0 credit, 누락·ratio/intern HOLD
보존, envelope/원문 SHA·actor 변조 거부, stale binding 거부, shallow checkout,
계산된 ledger의 재생성 멱등성과 HTML/Markdown/동적 경고를 검증한다.

## Wave3 annotation wrapper 준비

14번째 wrapper는 `revisions/notes/protected-migration-independent-notes-wave3.json`이
있을 때만 동작한다. 준비 변경에는 이 실제 manifest를 만들지 않는다. Controller가
네 job을 모두 순차 통합하고 최종 산출물을 재생성한 뒤에만 root가 manifest를
작성한다. 이 wrapper 자체는 독립 법규 감사나 question/canonical credit를 만들지
않으며, 기존 publication consumer의 integration·본문·claim 검증을 대신하지 않는다.

고정 기준은 PR189의 `f4ecea13a31b4c8dbdb7ef460b8caee54b571b27`이다.
`git show COMMIT:PATH`의 원바이트를 다음 snapshot으로 보존한다.

| Snapshot | SHA-256 |
|---|---|
| `revisions/baselines/complete-notes-pr189.md` | `f4ebbad48aaea4575c123533878d59a90fc12a19391e2a3b49e13666f8a93440` |
| `revisions/baselines/notes-build-pr189.json` | `d4f24c8c32745d3b4c4d8d411fd3e07dbc94bbcbdad55fe028bccf9479a3ad2e` |

Markdown snapshot에는 원래 발행본의 후행 공백도 보존한다. Snapshot을 포함한
`git diff --check`의 기존 공백 경고를 없애려고 원바이트를 정리하지 않는다.
새 코드·테스트·문서의 공백 검사는 이 raw snapshot과 구분한다.

Manifest는 기존 annotation schema인 `notes-protected-annotation-migration/1`을
사용하며 `baseline_commit`은 위 PR189 commit, `path`는
`site/notes/complete-notes.md`, `baseline_copy`와 `baseline_build_copy`는 위 두
snapshot이다. `old_sha256`·`baseline_build_sha256`는 위 raw SHA로 고정된다.
`previous_migration_path`는 `revisions/notes/protected-migration-independent-notes-wave2.json`,
그 `previous_migration_sha256`은
`8573eced55fdd94dd9fa23ede6da19fa7049b93026200a27096cd73d503e3e8b`다.
`canonical_release_credit`는 0이어야 한다.

`semantic_notes_sha256`은 계속
`e1519c0290ff220eb8251307e26340d76d394a7ec1f3e651194d4495a03f1824`다.
실제 `load_notes(root)` 결과와 PR189/current build의 의미 해시, edition
`2026-11-03.emergency-kit.1`, 전체 `revision_provenance`가 일치해야 한다.
Current build의 추가 표시 metadata는 허용하지만 의미 변경은 허용하지 않는다.

`independent_reviews`는 아래 네 repository-relative 경로를 key로, 각 최종 보고서의
원바이트 SHA-256을 value로 가진다. 각 보고서는 `stage: independent-notes`,
`canonical_audit: false`, `canonical_release_credit: 0`, `question_audit_credit: 0`과
정확한 중복 없는 unit 집합을 가져야 한다.

| `reports/full-corpus-review/independent-notes/` 아래 보고서 | 정확한 unit 집합 |
|---|---|
| `third-b-review.json` | `oral-followup`, `w2-b-1`–`w2-b-4` |
| `third-e-review.json` | `w2-b-5`–`w2-b-9` |
| `third-g-review.json` | `w2-b-10`–`w2-b-13`, `w2-c-1` |
| `third-f-review.json` | `w2-c-2`, `schedule-vi-continuity`, `w2-c-4`–`w2-c-6` |

`new_sha256`은 통합·재생성이 끝난 실제 Markdown 원바이트 SHA다. Wrapper는 이를
확인한 다음 PR189 Markdown snapshot으로 decode하여 기존 13개 guard를 그대로
평가한다. 이전 manifest의 기대 hash를 갱신하거나 과거 guard를 제거하지 않는다.

집중 검증은 다음과 같다. Wave3 fixture의 보고서는 합성 engineering 데이터이며
실제 법규 감사·배정·통합 증거가 아니다. 실제 manifest가 없는 동안 기존 13단계
경로가 유지되는 것, 원본·부모 hash·snapshot·build·실제 의미·허용 경로·보고서 범위와
credit·출력 변조 거부를 검사한다. Historical emergency fixture는 13·14번째 layer를
제거하고 PR188 Markdown/build를 복원하여 원래 12단계 context를 유지한다.

```sh
python scripts/verify_representative_protected.py
python -m pytest -q tests/test_emergency_note_activation.py
python -m pytest -q tests/test_full_corpus_review.py -k 'protection or migration'
```

새 보고서가 먼저 통합되고 생성물이 아직 이전 상태인 작업 시점에는 전체 corpus
snapshot 비교를 이 준비 변경의 검증으로 사용하지 않는다. Root가 최종 보고서들을
통합하고 전체 재생성·drift 검사·QA를 수행한다.
