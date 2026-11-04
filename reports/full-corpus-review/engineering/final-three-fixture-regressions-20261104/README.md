# Frozen91 전체 실패와 남은 세 fixture 회귀의 분리

실제 전체 pytest 소스는 `91a58a12cc5f12a09a0cba3a1a692e8fabfb7687`입니다. 원본 전체 로그와 JUnit을 그대로 보존했습니다. 결과는 **1498건 중 1489 PASS / 9 FAIL, 7255.85초**이며 전체 PASS가 아닙니다. `6723e0480d4b5e92224b604e0767402eb5411898`은 이 소스에서 practice quality job의 시간 예산만 15→120분으로 바꾼 후속 커밋이고, runtime/test/data 차이는 0개입니다.

첫 여섯 실패는 원래 두 job으로 줄인 notes 소비 fixture에 후속 inactive ancestry가 남았기 때문입니다. 이 문제의 수정·실패 traceback·집중 12/12 PASS는 별도 커밋 `46cec6c3fe2ea255b4fd3de7b7b71d6a2519c591`과 `../notes-consumer-fixture-epoch-20261104/`에 있습니다.

이번 남은 세 실패는 다음과 같습니다.

- `test_phase10_preserves_355_historical_statuses_question_objects_and_M_source`: 정확 phase10/M 스냅샷의 semantic SHA `e1519c...`와 후속 N1의 현재 SHA `29da00...`를 비교했습니다. 제목과 고정 snapshot hash가 정의한 역사 계약을 유지하기 위해 이 테스트 모듈의 ROOT를 기존 승인 검증 helper `published15_root`로 지정했습니다. assertion과 기대 hash는 그대로입니다.
- `test_phase10_archive_notice_splits_preserve_whole_previous_groups_and_exact_sources`: 현재 phase11 notice 변경을 phase10 전용 원래그룹 비교에 대입했습니다. 현재 120개 원래 ID의 notice가 phase10 밖의 후속 source를 가리키며, 원래 notice 전체는 현재 history에 정확히 보존돼 있습니다. 같은 역사 ROOT 지정으로 정확 phase10 입력을 복원합니다. notice나 생산 validator는 수정하지 않습니다.
- `test_builder_exposes_secondary_separately_and_keeps_all_primary_and_publication_fields`: builder direct-call을 synthetic retry로 치환하는 테스트 대역이 source closure의 keyword `source_bindings` 호출까지 가로챘습니다. 실제 retained-source 검증 호출은 동일 keyword와 실제 repository/질문/collections를 원래 loader에 전달합니다. synthetic 대역과 union-count 캡처는 builder direct-call에만 적용합니다. 실제 closure 검증을 실행하며, 새 출처를 생략하거나 guard를 완화하지 않습니다.

두 모듈의 assertion AST 총 59개는 동일합니다. phase10의 모든 테스트 함수 AST도 동일합니다. procedural 모듈은 해당 한 테스트의 대역 signature와 capture 범위만 바꿉니다. 모든 생산 코드·질문·답·노트·원장·queue는 그대로이며, QA91 HEAD/파일을 수정하지 않았습니다. 새 전체 pytest나 GitHub CI PASS는 아직 주장하지 않습니다. 관련 두 모듈은 실제 종료 코드 0, **53/53 PASS, 253.09초**입니다. 로그·JUnit·SHA를 보존했습니다. 누적 변경 테스트 세 파일의 assertion 95개 모두 source91과 동일하며, 다른 테스트 파일은 바뀌지 않았습니다.
