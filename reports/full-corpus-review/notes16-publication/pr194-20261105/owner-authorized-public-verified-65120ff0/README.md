# PR #194 공개 연습판 배포 검증

사용자 승인 “배포 진행해”에 따라 전체 CI 완료 대기에만 예외를 적용했습니다. HOLD·SOURCE_BLOCKED·기존 부정 이력과 기본 연습 202개를 유지했고, 새 canonical RELEASED는 0입니다.

- 후보: `bbb5daa9c88612c080661bd93f080afd3663495d`
- 실제 병합: `65120ff0bace38f561240c5e0b6bb322d33243a5` (후보와 tree 동일)
- [실제 Pages 실행 42043966552](https://github.com/woojunxnam/oddments/actions/runs/42043966552): 성공
- [연습문항](https://woojunxnam.github.io/oddments/practice-expansion/) · [통합 노트](https://woojunxnam.github.io/oddments/notes/)
- canonical 공개 파일 첫/마지막 대조 각각 40/40, 핵심 14개 포함. query/cachebuster 없이 실제 HTTP 원문 SHA를 검증했습니다.
- 실제 공개 브라우저 5종 모두 PASS: 연습문항, 노트, refresh, Q0012 철회 이력, 대체 문항 77개. 사용자 프로필 대신 별도 합성 저장소를 사용했으며 풀이·북마크 보존과 N1 HOLD/daily 제외를 확인했습니다.
- 실제 배포 후 native planner 4×40의 결과는 `[]`; 9개 큐 198건 INTEGRATED이며 모든 원장 바이트가 그대로입니다. 이는 보류 37문항의 법규 판정 완료나 추가 검토 credit를 뜻하지 않습니다.

전체 main CI는 검증 시점 PENDING입니다. 직전 전체 pytest 1,788 PASS·1 FAIL, fixture 수정 후 개별/관련 모듈 PASS와 현재 후보의 HTTP 30분 시간 초과를 보존했습니다. 전체 QA PASS 또는 프로젝트 전체 품질 완료로 표시하지 않습니다.

추가 배포 검증기의 잘못된 stored/actual body hash 비교 실패도 보존했습니다. 실제 native publication 계약에 맞게 저장된 metadata hash는 원장의 effective hash와, 독립 검토 hash는 actual body hash와 각각 비교했습니다(각 306개). 서비스 코드·데이터와 native validator는 수정하지 않았습니다. 수정 전 실패, 실행 소스, 실제 merge의 성공한 40파일 재생성, 첫/마지막 HTTP 원문, 브라우저 결과·화면, raw API 응답은 `evidence.tar.gz`에 있습니다. `evidence.manifest.json`의 599개 원 SHA로 검증할 수 있습니다.

이 증거 전용 commit의 `[skip ci]`는 보존용 브랜치에서 이전 baseline 검사를 중복 실행하지 않기 위한 것입니다. 실제 main·candidate·Pages workflow 조건이나 명령을 바꾸지 않았습니다.
