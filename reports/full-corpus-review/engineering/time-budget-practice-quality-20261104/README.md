# Practice quality CI 시간 예산 조정 근거

기준 소스는 `91a58a12cc5f12a09a0cba3a1a692e8fabfb7687`입니다. 실제 GitHub run `41864566412`, job `126695337141`은 2026-11-04 16:20:13Z부터 16:35:30Z까지 실행 후 취소됐으며, 원 annotation에 `The job has exceeded the maximum execution time of 15m0s`가 기록되어 있습니다. 원 API 응답과 전체 로그를 그대로 보존했습니다. 원 실행의 브라우저 두 단계는 SKIPPED입니다.

후보 변경은 `.github/workflows/practice-quality-qa.yml`의 해당 job 제한 시간 15분을 120분으로 바꾸는 한 줄입니다. 원본 바이트에서 정확한 단일 치환으로 검증했으며, 검사 단계·명령·assertion·조건·path filter·권한·의존성 버전은 동일합니다. runtime/test/data 파일 변경은 0개입니다.

고정 QA 작업 트리와 HEAD는 변경하지 않았습니다. 이 근거는 시간 예산 조정의 동일성 검사이며, 새 GitHub CI의 성공이나 배포 검증을 주장하지 않습니다. 후보 HEAD의 GitHub 전체 CI는 아직 미실행입니다.
