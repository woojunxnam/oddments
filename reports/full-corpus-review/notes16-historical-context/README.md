# 실제 held-source 재귀 수정과 보존된 검증 결과

실제 actor는 `/root/notes16_engineering`, 수정 commit은 `46a07703`이다.
Root가 실제 SOURCE를 승인한 후 body registration 검증이 historical derived preview를
만들면서 `apply_study_revision`의 metadata 태그를 위해 현재 `load_notes`를 호출해
held-source 검증으로 되돌아갔다. Root는 실제 172줄 stack을 `de737ac5`에 보존했다.

실제 old-effective-notes rawSHA9f549ebe…를 직접 확인했으며 M revision provenance가
완전하게 들어있다. 새 keyword-only `notes_context`는 이와 같이 caller가 rawSHA로
검증한 역사 snapshot의 metadata를 명시적으로 전달하는 용도다. 실제 body validator는
그 검증된 `old_notes`를 전달한다. Authored study/refresh patch scope와 텍스트는 그대로다.
Live builder는 인자를 생략하므로 기존 현재 `load_notes` 검증을 반드시 실행한다.
역사 context에 provenance가 없으면 현재 source로 fallback하지 않고 명확히 실패한다.
Authored card가 없는 최소 fixture에는 가짜 provenance를 만들지 않는다.

실제 authored LAW037/study 및 refresh 파일이 존재하는 regression은 수정 전
`HELD_SOURCE_CURRENT_LOAD_REENTRY`로 실패했다(`reentry-before.log`). 수정 후에는
저장된 derived-preview 두 item의 텍스트와 before/candidate source hashes 전체가
정확히 같았다. 두 kind의 전체 patched data도 실제 pre-activation M context 결과와 같다.
Live guard 유지, missing provenance, 최소 fixture, archived-body tamper를 포함한
빠른10개 검사는 `subset-after.log`에 있다. 관련 historical/body/inactive 전체는
`focused-after.log`의 **101 PASS / 0 FAIL / 0 ERROR,59.24초**다.

추가 emergency 전체 실행은 **123 PASS / 46 ERROR,153.61초**로 실패했다.
`emergency_copy`가 각 case에서 ROOT/revisions 전체를 복제하며 새 published15
full-preimage tree까지 복제해 `/tmp/pytest-of-agent/pytest-35`가 약12GB가 되었다.
관측된 setup 오류는 Errno28이며 디스크가100%가 됐다. 이 실행을 PASS로 재분류하지
않으며 미실행 emergency case의 code defect를 배제하지 않는다.

507KB 원 로그를 `expanded-errno28.log.gz`에 lossless 압축 보존했고 SHA/byte count를
`observation.json`에 기록했다. 압축 해제 bytes와 원 로그가 같은지 확인한 뒤 이 실행의
완료된 합성 pytest35 clone만 삭제해 약12GB를 복구했다. 실제 workspace/증거/worktree는
삭제하지 않았다. Test fixture의 역사 M/원 guard 검증은 실제 승인된 published15
fixed view로 명시적으로 분리하고, 현재 N1/011/source 검증과 실제 full-corpus build는
live 대상으로 유지해야 한다. 큰 full-preimage를 단순 ignore해 검증을 생략하지 않는다.

전역 reentry skip, 캐시, source guard 면제, 본문·preview 수정, 법규/출시 credit는0이다.
실제 현재 N1 builder·final16·전체 QA/CI 결과는 root의 후속 검증이 필요하다.
