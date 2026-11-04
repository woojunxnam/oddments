# Tests

Schema, registry, dependency hash, audit integrity, source governance, release gate, duplicate detection, generated output, website shuffle invariant의 Pytest coverage가 이 directory에 있습니다.

`test_emergency_note_activation.py`의 mutation 검사는 역사 M의 12–14번째 activation
guard를 대상으로 한다. 승인·커밋된 16번째 manifest가 있으면 기존
`published15_test_view.published15_root`가 실제 공개15의 exact frozen view를 검증하고
반환한다. 이 모듈의 복사본과 명시적 notes/study 호출은 그 epoch를 사용한다.
현재 revisions 전체에는 공개15의 full preimage가 포함되므로 이를 매 case마다
복제하면 검사 범위와 관계없는 대용량 재귀 복사가 된다. 특정 파일을 ignore하거나
검증을 빼는 대신 역사 검사에 해당하는 원 tree를 복사한다.

`test_full_corpus_review.py`에서는 PR190/14 guard용 `protected_copy` fixture만 같은
frozen source를 사용한다. 모듈의 ROOT와 전체 `build()`·현재 N1·진척·출력 검사는
실제 현재 tree를 유지한다. 현재16·본문·census·보호 검사는 해당 live integration
suite에서도 계속 수행한다. Fixture는 독립된 일반 복사본이므로 mutation이 원본에
전파될 수 있는 hard link를 사용하지 않는다.
검증된 frozen view의 읽기 전용 mode가 mutation fixture에 전파되지 않도록
`mutable_copytree`는 복사가 끝난 **복사본에만** owner-write 권한을 추가한다.
원 view의 바이트·권한·inode는 그대로 두며 기존 tamper/unlink 검사를 모두 실행한다.

최종16이 아직 없으면 helper가 live ROOT를 반환하는 기존 동작은 유지된다.
N1/최종16 준비 중에 이 대용량 역사 fixture들을 미리 실행해 검증 완료로 세지 않는다.
실제 후보의 최종 manifest를 커밋·승인한 다음 전체 pytest를 실행한다. 자원 절약용
`-o tmp_path_retention_policy=failed`는 성공한 임시 fixture의 보존 정책일 뿐 검사를
생략하거나 실패를 통과시키는 옵션이 아니다.

Wave10 completion/context 모듈도 공개15 당시 exact37 job과 역사 receipt를 검사하므로
같은 approved frozen15 view를 사용한다. 이후 native queue의 41개 이상 job을 옛
37개 guard에 허용하도록 생산 규칙을 넓히지 않는다. 현재16/native 검사는 live tree를
계속 대상으로 한다. Frozen view 생성 뒤에는 테스트 helper의 종료 callback을 다시
등록해 TemporaryDirectory finalizer보다 먼저 permission 복원과 정상 cleanup을 마친다.
검증 조건·assertion·테스트 범위는 이 cleanup 순서 변경으로 달라지지 않는다.
