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


## 배포 확인 후속 — 2026-10-29

PR #171은 `5bfdeaa8d87d8c18d73c773bcfdd11d5824ca3db`로 main에 병합했고 Pages 배포 run `40920435063`이 성공했다. 위의 draft/미배포 서술 및 question-ledger의 deployment_status는 병합 전 snapshot이다. 현재 배포 이벤트는 `reports/full-corpus-review/unit3a-deployment.json`을 따른다.

최종 candidate `c8196776f69d116a17807ec7f76b23546146215d`의 PR CI 8개 모두 성공. Production 대표 회귀 run `40920503279`, study production `40920503256` 성공. 59개 개정판의 오답/정답 채점, shuffle mapping,320px, 이전 attempt/bookmark, deep links, backup/import,20/120 모드 및 전체 복원추출 Chaos10을 실제 배포 origin에서 통과했다. 브라우저 artifact12918555711의 링크/hash는 배포 기록에 있다.

직접 HTTPS로 공개 practice manifest2331과 노트 build/content.js/book.html/study-data.js/refresh-data.js bytes도 대조했다. 모든 확인한 노트 파일이 로컬 배포본과 일치했다. 독립 법규 감사 및 실제 Safari/device 검증은 미완료다. 수치는59/3/8/285 및2331로 유지한다.

Unit3B를 시작해 PER19 원문4개와0065 복구 원고를 읽고 공식 Policy/247 CMR8 전문 추출문을 재열람했다. 정식 인수 계약이 필요한 것처럼 읽힐 수 있는 조건을 실제 awareness/observation/direction의 부재로 좁힌 미공개 초안을 `reports/full-corpus-review/unit3b-working/MA-RW-0065-draft.json`에 저장했다. 노트 판본,의미중복 대조,예외 검증 및 통합 테스트가 남아 완료/배포 수에 더하지 않는다. 다음 대상은 계속PER19–PER22와 w1-b-9/w1-b-10이며 MOR로 건너뛰지 않는다.


## Unit 3B source checkpoint — 2026-10-29

시작 main `580368073eba947d1484694fef078b413f24c85f` (PR #172 기록 병합). 로컬 exec-server 실패로 이번 변경의 생성·테스트는 feature branch GitHub Actions에서 수행한다. 아직 실행하지 않은 검사와 배포는 PASS로 승계하지 않는다.

PER19–PER22 원문16개를 각각 읽고 선택지별 작성자 기록을 남겼다. 복구 원고0065/0067/0068은 이번 공식 추출문 재열람과 사실조건 보완을 거친 source 후보이며,0066은 생성하지 않고 PER20 대표0143을 보류한다. PLUS 대용량 blob을 읽으려는 연결이 두 번 실패했으므로 PLUS 비교·review 주장은 승계하지 않는다. PLUS0814 등의 추가 default HOLD 여부는 원문을 읽은 뒤 별도 판단해야 한다.

w1-b-9/w1-b-10의 별도 versioned revision을 작성했고, 기존 w1-b-8 revision source와 이전59개 질문 객체는 보존한다. 실제 직접 감독,2명/4명 관계 OPEN,trainer/trainee category,교육일 전 designation,computer-only와 영업·보안의 구분을 설명한다. LAW-012/RF-049와 장 highlights도 같은 revision에서 합성한다. 첫 migration manifest와 원본 export는 유지하며,정확히 같은 generated export 한 경로의 두 번째 migration만 허용한다.

생성된 결과가 검증되기 전 예상 누적62 재작성/3통합/10보류/280미반영 및2334 archive를 완료 실적으로 보고하지 않는다. Canonical 독립 감사와 같은 팀 peer는 이번에도 NOT_RUN. 확인할 새 note claims10개(그중1개 적용 관계 OPEN)는 전체 claim census가 아니다.

다음: Unit3B의 생성 artifacts와 테스트·CI·공개 origin 검증을 먼저 마친다. PER20 source relationship,PLUS 후보 및CE email/Form 충돌을 유지하고 그다음 MOR07–10/DISC01–08로 넘어간다. 전체 2334 ID와306절의 미검토가0개가 될 때까지 전체 완료라고 하지 않는다. 추가 사례·보류는 분모에서 삭제하지 않는다.

Unit3B worker의 첫 생성물은 294 tests를 통과했으나, 그 뒤 확보한 PLUS0109/0812/0814 원문 전체를 읽고 기록을 추가했다. 0814는 기본 대표 추가 보류,0812는 archive 주의 대상으로 연결한다. key 오류를 확정하지 않는다. 이 추가 변경 후의 최종 head CI는 별도 확인한다. 전체 PLUS를 읽었다는 뜻이 아니다.

## Unit 3B materialized checkpoint — 2026-10-29

Branch `feat/unit3b-personnel-20261029`, PR #173. Actual tested generated commit `e98437b6190c4dedc3feee772b7f48e3bda6c93e` (worker source `87d3a9721c32889a5cd54fc7cef943dae268573a`). Worker run40929819513/job123644961317 passed 294 Python tests, deterministic builder checks, JS syntax and publish build2334. Final ordinary PR CI, merge and production checks remain pending at this checkpoint. Temporary branch-only materializer workflow is removed in this checkpoint commit; existing gates remain.

Actual Unit3B review: MA-EXP-0137–0152 plus MA-CASE-0109/0812/0814 (19 original IDs), and MA-RW-0065/0067/0068 (3 new IDs). Raw dispositions: REPLACE3, MINOR_EDIT10, HOLD6. Default holds include PER20 representative0143 and PLUS0814;0812 receives an archive warning. Answer keys of these PLUS records were not adjudicated wrong. New3 are author reviewed practice editions, not independently audited RELEASED questions. PLUS extraction/provenance is stored separately.

Current2334 = original2176 + MA-REV96 + MA-RW62. Representative355: rewritten62/reused3/held10/pending280; default438. Cumulative41 IDs tracked,2293 remain NOT_REVERIFIED in this full-corpus review. Inventory does not imply legal completion. Claims16:14 author-source-checked/2OPEN; w1-b-8/9/10 have partial claim work, no complete atomic census. Same-team peer and independent canonical audit NOT_RUN. Canonical439 are inventory only.

Notes w1-b-9/10, chapter highlights, LAW-012 and RF-049 use the versioned revision. Original guide, Unit3A revision/migration and previous59 complete question objects are preserved. Exact generated-export migration remains narrowly validated. All old IDs/storage/anchors remain; prior reading history is retained with revision notices.

Next work after final Unit3B CI/deployment: MOR07 MA-EXP-0179/w1-c-4; MOR08 0183/w1-c-5; MOR09 0187/w1-c-5; MOR10 0191/w1-c-7; DISC01 0195/w6-b-8; DISC02 0199/w6-b-8; DISC03 0203/w1-c-13; DISC04 0207/w1-c-13; DISC05 0211/w1-c-14; DISC06 0215/w1-c-14; DISC07 0219/w1-c-15; DISC08 0223/w4-d-17. These are queued, not reviewed. Keep intern2/4 relationship, PLUS source qualifications, CE email/Form w1-a-7 conflict OPEN. Commands: build_full_corpus_review.py --check; build_quality_status.py --check; representative builders/checks/protection; notes/study/refresh builders --check; validate_all.py; pytest; existing HTTP/browser CI. No full-corpus completion date is asserted.
