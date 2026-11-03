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
