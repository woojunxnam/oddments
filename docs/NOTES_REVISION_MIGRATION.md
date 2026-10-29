# Personnel note revision and immutable baseline

사용자가 2026-10-29 전체 문제은행과 노트의 개선을 요청했다. 원본 보호 검사를 삭제하거나 notes/ 전체를 제외하지 않는다.

- `notes/guide.json`, study/refresh 원본, 기존 질문 2,328개와 canonical data/audits는 그대로 유지한다.
- 현재 화면의 편집 원본은 `revisions/notes/2026-10-29-personnel-ratios.json`이다. `scripts/notes_revision.py`가 고정된 guide hash 위에 w1-b-8 한 unit, personnel highlights, LAW-012, RF-049를 합성한다.
- 세 builder가 합성된 unit hash를 사용한다. Question archive는 기존 note snapshot을 보존한다. 새 질문만 별도 notes_revision hash를 기록한다. baseline hash와 현재 표시 내용 hash를 구별한다.
- 이전 `site/notes/complete-notes.md` bytes는 `revisions/baselines/complete-notes-2026-10-23.1.md`에 보존한다. `protected-migration.json`이 old/new hash, 정확히 한 허용 경로, revision source hash를 명시한다. 기존 protected-baseline.json은 바꾸지 않는다.
- verifier는 baseline 원본 1,781개를 계속 검사한다. 정확한 generated export에만 migration을 적용하며 이전 copy는 원래 baseline과 다시 대조한다. 다른 경로 추가, guide/policy/원문 변경, stale revision/current export hash는 실패한다. 음성 회귀시험은 tests/test_full_corpus_review.py에 있다.
- 모든 chapter/unit anchor와 browser storage key는 유지한다. 읽음·북마크를 지우거나 새 판본 숙련으로 승격하지 않는다. editor note가 과거 읽음의 의미와 새 판본을 표시한다. 옛 노트 복원은 revision을 적용하기 전 커밋 및 보존된 guide/export로 가능하다.
- 이 개정은 작성자 확인이며 독립 법규 감사가 아니다. 1:6 정책/규정 적용 관계는 OPEN. 법규학습 및 복습카드에서도 같은 주의를 표시한다.

재현: `python scripts/build_ultimate_notes.py --check`, `python scripts/build_exam_study.py --check`, `python scripts/build_refresh.py --check`, `python scripts/verify_representative_protected.py`, `python -m pytest tests/test_full_corpus_review.py -q`.
