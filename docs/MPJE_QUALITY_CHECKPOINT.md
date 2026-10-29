# MPJE 품질 개선 checkpoint — Unit 3A

시작 main: `9f3fed116792b33c65cad35da77a8d68aab58c06` (PR #170). Branch: `feat/unit3-corpus-personnel-review-20261029`. GitHub PR: https://github.com/woojunxnam/oddments/pull/171. 첫 code snapshot: `88985ebcbd57163dc6879e56a1f504c28ad48b1c` (local tree-equivalent commit `101a6621f6d71bb9599e3f97d5170b1fefffa044`, tree `eefc2f9aea843d0d3fdf17184a58e99fda9e48eb`). 후속 checkpoint/evidence 강화 커밋의 최종 head는 PR head 또는 `git rev-parse HEAD`로 확인한다. 아직 merge/production 완료로 간주하지 않는다.

## 실제 반영 후보

- 이전 workspace의 Unit 3 JSON 두 개를 복구했다. 정확한 원고 hash와 출처는 recovery.json, 원문은 recovered-drafts/에 있다. 이전 peer·테스트 주장은 승계하지 않았다.
- PER15–PER18 원문 `MA-EXP-0121`–`0136` 16개를 ID별로 읽고 모든 선택지에 작성자 기록을 남겼다. 3개 대표(`0123`,`0127`,`0135`)는 새 `MA-RW-0061`,`0062`,`0064`로 분리했다. `0131`은 보류했고 PER17 변형4개에 같은 미해결 관계의 안내를 연결했다. 다른 family나 PLUS 후보를 자동 통과시키지 않았다.
- 원문 판정은 REPLACE 3 / MINOR_EDIT 9 / HOLD 4, 새 개정판은 작성자 KEEP 3이다. 원문 12개의 근거 확인에는 일반경로 조건부라는 한계가 있다. KEEP/검토완료로 일괄 해석하지 않는다. 개정판은 독립 감사 전 연습판 상태다.
- 노트 w1-b-8, personnel highlights, LAW-012, RF-049를 합성 개정했다. 주요 claim6개 중5개 작성자 근거 확인,1개 OPEN. unit 전체 claim census나306절 전수 법규 감사는 미완료다.
- 보존: 원본2,328 ID/내용, canonical439 records와 감사·release policy, 기존 풀이·bookmark/storage·anchor. 의미 변경은 새 ID. 보호 범위의 generated export 한 경로만 manifest로 migration한다.

## 중복 없는 범위

전체 보관2331 = 원본2176 + MA-REV96 + MA-RW59. 원래355 cohort: 재작성59 / 기존 사례 통합3 / 보류8 / 개선 미반영285. 구현상 연결62는 신규 재작성62가 아니며 독립 감사 수가 아니다. 기본 우선목록440. 신규 gap 목표에 replacement3개를 더하지 않는다.

전체2331 ID, canonical439, notes33장/306절을 인벤토리화했다. 이는 법규 확인 수가 아니다. 이번19 ID(원문16+개정3) 외에는 새 전수 검증일을 부여하지 않았다. canonical439는 별도 재감사하지 않았다. 목록·본문에 다른 embedded 사례가 있는지에 대한 전면 census는 아직 미완료다.

동일 TF-IDF 방법/고정 shared vocabulary로 main 2328개→2331개에서 archive near-text 후보745→745, 기본목록441개→440개에서0→0. 기존 archive 중복을 지운 것이 아니다. 전체 의미중복 판정은 미완료. 선택지/정답 분포는 pattern-metrics.json에 기록하며 법규 타당성 점수로 쓰지 않는다.

## 검증과 제한

로컬 full pytest 290 PASS, validate_all 오류0/기존 warning7, 보호1,781개 및 deterministic builders PASS. 실행 상세는 reports/full-corpus-review/validation.json과 PR의 정확한 head CI를 확인한다. 첫 code SHA의 실제 HTTP CI 성공은 first-code-ci.json에 기록하며 최종 head CI와 혼동하지 않는다. 작성자 검토와 자동검사만 수행했으며 이번 세션의 새 동일 팀 peer 및 독립 canonical 감사는 NOT_RUN이다. Chromium 다운로드 오류로 로컬 실제 HTTP 브라우저 검사는 미실행이다. CI 성공 전 merge/배포 완료로 보고하지 않는다. 실제 기기·Safari·psychometric 검증은 미실행.

## 다음 작업 — Unit 3B부터

1. PER19–PER22: `MA-EXP-0139`, `0143`, `0147`, `0151`; 원문 family 변형 각각과 `w1-b-9`, `w1-b-10`. 복구된0065/0067/0068 원고는 미반영이며 최신 근거·선택지별 재검토가 필요하다. 0063/0066은 보류 예약번호로 생성하지 않는다.
2. 2-intern 규정과 조건부4-intern policy의 적용 관계, 직접 감독·전담교육·computer training을 좁은 setting에서 검토한다. MOR/Discipline으로 건너뛰지 않는다.
3. source-conflicts.json의 CE email/Form(`w1-a-7`; 0051/0795/0349), 1:6 적용 관계, PLUS 후보를 개별 검토한다. 보류를 해결 수로 세지 않는다.
4. `python scripts/build_full_corpus_review.py --check`; 위 세 builder와 보호 검사; full pytest/validate_all 및 workflows의 실제 HTTP 회귀검사. 새 판본의 파일 hash와 정확한 PR head를 고정한 뒤에만 다음 상태로 진행한다.
