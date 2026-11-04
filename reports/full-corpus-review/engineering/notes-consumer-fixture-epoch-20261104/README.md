# 원래 C/F 소비 fixture의 후속 ancestry 범위 복원

고정 소스 `91a58a12cc5f12a09a0cba3a1a692e8fabfb7687`의 실제 전체 pytest에서 보존된 `test_only_integrated_committed0/repo`를 같은 소스의 `load_notes`와 `load_metadata`로 다시 읽었습니다. 종료 코드 1이며, 원 traceback은 `queue.validate_state → notes_census_reassessment.validate_chain → ValueError: Inactive census successor has no unique append-ordered assignment`입니다.

`actual_reports`는 원래 C/F 두 job만 의도적으로 복사한 합성 소비 checkpoint입니다. 후속 census 및 body reassessment 기록은 이미 제외하지만, 새 inactive census successor만 남겨 그 부모 job이 제거된 모순된 fixture를 만들었습니다. 수정은 같은 fixture에서 이 관련 없는 후속 ancestry를 제외하는 한 줄과 설명 주석입니다. 실제 데이터나 native queue에서 기록을 지우지 않습니다. 생산 ancestry 검증도 그대로 유지합니다.

기준 후보 부모는 시간 예산 변경을 포함한 `6723e0480d4b5e92224b604e0767402eb5411898`입니다. 36개 assertion AST와 fixture 외 모든 테스트 함수 AST가 동일합니다. 첫 live consumer 테스트와 frontend의 현재 ROOT는 그대로입니다. 생산 코드·runtime·데이터 변경은 없습니다. QA91 HEAD 및 파일은 수정하지 않았습니다.

이는 테스트 fixture의 범위 일관성 수정이며 독립 법규 판정·노트 PASS·배포 또는 RELEASED credit을 부여하지 않습니다. 집중 모듈은 실제 종료 코드 0, 12/12 PASS, 848.47초입니다. 원본 로그·JUnit·결과 SHA를 함께 보존합니다.
