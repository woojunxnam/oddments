# MPJE 품질 개선 checkpoint

## 최신 구현 snapshot — Discipline/CDTM, 2026-10-30

시작 main: `c4a05c8bf48ecc333e331b3c267607af6590ac40`. Branch: `feat/disc-cdtm-learning-20261030`. 이 절은 현재 source의 구현 상태이며, 아래 과거 checkpoint의 수치·미배포 문장은 당시 snapshot으로 보존한다. PR [#177](https://github.com/woojunxnam/oddments/pull/177), 최초 candidate `09c86f94d37b3fdb9c59748011cd1515a4da5e0b` (로컬 테스트와 동일한 tree `bbc2aedb4761402a59bb985b67fcbf4469bd4440`). 최종 head·merge·production은 이 절의 후속 기록과 해당 PR 실행 결과를 확인한다.

### 실제 검토·수정 범위

- 원본 `MA-EXP-0209`–`0240` 32개·128개 선택지, 이미 공개된 `MA-RW-0025`–`0028` 4개·16개 선택지, 새 `MA-RW-0077`–`0080` 4개·19개 선택지: 합계 **40개 ID·163개 선택지**. 기존 CDTM 4개는 재검토 후 유지했으며 새 문항은 4개뿐이다.
- 원본 32개 판정: `MINOR_EDIT` 23 / `REPLACE` 8 / `MAJOR_REWRITE` 1. 대표 교체 8개 중 CDTM 4개는 이미 구현된 교체이며 이번에 새로 만든 것은 Discipline 4개다. 경미한 개선 원본 23개는 immutable archive에 남아 있으며 편집 완료로 계산하지 않는다.
- `MA-EXP-0223`의 원본 SATA key `A,B,C,D`에는 waiver의 **impractical AND unduly burdensome**을 OR로 잘못 쓴 A가 포함돼 있다. 근거에 맞는 선택은 `B,C,D`다. `0224`는 잘못된 선택지가 C와 D 둘이라 SBA 정답이 모호하다. 원본 key/history를 보존하고 명시적 주의와 새 `MA-RW-0080` 연결로 학습 경로를 교정했다. `0221`–`0222` 해설, `0228`의 범위, `0233`–`0236` 자격 근거 관계까지 이번 주의 표시는 9개 ID다.
- 새 `0077`은 실제 impaired practice와 치료 사실을, `0078`은 Board가 징계로 지정한 probation과 다른 처분을, `0079`는 summary suspension과 quarantine의 절차·기한을, `0080`은 waiver 만료·연장과 두 요건의 결합을 구별한다. 영어 지문·선택지와 한국어 선택지별 해설 및 정확한 공식 조항을 기록했다.
- 40개 ID 각각에 10개 기준·0–5점 편집 평가를 기록했다. 평가 없는 문항은 `null`이며 0점 또는 검증 완료로 바꾸지 않는다. 작성자 및 같은 팀 교차 검토는 독립 canonical 감사가 아니며 새 `RELEASED`는 0개다.

현재 공개 연습판 source는 **2,346 = 원본 2,176 + MA-REV 96 + MA-RW 74**, 기본 목록 438개다. 원래 대표 355개는 재작성 74 / 기존 사례 통합 3 / 보류 10 / 개선 미반영 268이다. 기존 70개 MA-RW 완전한 question record와 75개 source record의 보존 hash를 이번 baseline에 고정했다. 원본·과거 감사·canonical 상태·storage/북마크 ID는 보존한다.

누적 개별 검토 기록 **121개 ID**, 미재검증 **2,225개**. 법규 상태는 작성자 근거 확인 65 / 조건부 확인 46 / 근거 관계 보류 10이다. 이 121개는 모두 정답이 맞거나 독립 감사됐다는 수가 아니다. 원본 1,024개 구조검사와 구분한다. Canonical은 별도 **439개 = RELEASED 398 + AUDIT_PENDING 40 + REVIEW_REQUIRED 1**이며 이번에 재감사하거나 상태를 변경하지 않았다.

### 통합노트와 학습 연결

판본 `2026-10-30.discipline-cdtm.1`은 `w1-c-14`, `w1-c-15`, `w4-d-17`, `w3-d-2`, `w3-d-3`, `authority-paths`의 6개 절을 개정하고, 기존 미해결 사항 색인 `w6-b-17`에 새 OPEN 관계를 연결한다. 장 highlights 2개, 학습 요약 `LAW-016`·`LAW-045`·`LAW-048`, 복습 카드 `RF-011`을 함께 갱신한다. 7번째 절은 색인 갱신이며 내용 전수 법규 검토로 더하지 않는다.

누적 노트 33주제·306절 중 **14개 절의 제한된 claim 검토**, **15개 절의 versioned edit**가 있다. Claim/claim cluster는 **52개 = 작성자 근거 확인 48 + OPEN 4**이며 전체 atomic claim census가 끝난 절은 0개다. 이전 원본·판본·migration을 보존하고 다섯 번째 generated export migration은 `site/notes/complete-notes.md` 한 경로에만 적용한다.

각 상세 절의 관련 문제와 오답 복습은 실제 `note_evidence.unit_id`로 연결한다. `?note=<unit_id>`는 bank·주제·문제형식·검색·오답 필터와 교차 적용한다. 없는 절 ID에는 무관한 문항을 대신 보여주지 않는다. 기존 문제 deep link와 학습 기록은 유지하며 시간 연습 중 노트는 새 탭으로 연다. 저장 차단 환경에서는 모바일·집중 읽기에서도 보이는 임시 저장 안내와 직접 기록 내보내기 버튼을 제공한다. 현재 명시적 문항 연결이 있는 247개 절은 연결 수이며 법규 검토 완료 수가 아니다.

### 계속 OPEN인 법규 관계와 자료 경계

1. `MA-EXP-0233`–`0236`: M.G.L. c.112 §24B½의 PharmD 경로와 247 CMR 16.02(1)(c)1의 2017-06-30 날짜 조건 관계. 공식 조정 근거가 확보되지 않아 자격 결론을 일괄 확정하지 않는다. 기존 `MA-RW-0027`은 BPS 경로다.
2. 247 CMR 10.03과 20.03의 reporting 조건·기한 관계는 공식 근거를 더 확인해야 한다. 7 business days / 30 days / 14 calendar days를 하나의 기한으로 합치지 않는다.
3. 이전 CE email/Form, 1:6 인원 관계, 2/4 intern 관계, PLUS source 자격 문제는 OPEN을 유지한다. 이번 날짜로 전체를 재검증했다고 기록하지 않는다.
4. Castleport·OpenExamPrep·PreMPJE.com은 약관 확인만 수행했고 질문 본문 비교·AI 사용·재배포 permission이 확인되지 않아 Class B/HOLD로 남겼다. 외부 질문을 복제하거나 비율·coverage를 측정하지 않았다. Google Drive 보조 자료는 이번 배치에서 읽거나 canonical에 반영하지 않았다.

수치 정의는 `reports/full-corpus-review/inventory-definitions.json`을 따른다. 2,176은 초기 두 묶음, 2,328은 과거 56개 MA-RW를 포함한 baseline, 226은 과거 canonical 수다. 현재 고유 family ID 480개, 확장 판단 모델 128개, 노트 33주제는 서로 다른 차원이다. 독립 사례·독립 법규 판단 수의 전수 판정은 미완료다.

### 현재 배치 QA·배포 상태

| 항목 | 상태 | 근거 / 후속 |
|---|---|---|
| 최종 로컬 full pytest / validate_all | PASS | 332 tests 통과; validator 오류 0·기존 경고 7. `discipline-cdtm-validation.json` |
| 전체 builder 재현성 / 보호 manifest 검증 | PASS | 대표·ledger·similarity·notes/study/refresh 재현성, 원본 1,781개 보호, canonical 생성물 변경 없음 |
| 실제 HTTP·모바일·storage 브라우저 회귀 | 로컬 NOT RUN | Chromium 실행 파일 없음. 최종 head CI 및 production workflow에서 실행 결과 확인 필요 |
| PR / head CI | PR #177, follow-up CI PENDING | source 수·navigation 검증을 보완했고, 후속 CI에서 모바일 저장 불가 안내가 sidebar에 숨는 실제 문제를 발견해 UI·내보내기를 수정했다. 최종 head의 모든 gate 성공을 확인해야 함 |
| merge / Pages / 공개 origin 검증 | NOT RUN | 배포된 byte와 실제 화면·동작 확인 전 완료로 보고하지 않음 |
| 새 독립 canonical 감사 | NOT RUN | 작성자·같은 팀 검토와 구분, RELEASED 추가 0 |

초기 CI 실패와 보완은 `reports/full-corpus-review/discipline-cdtm-validation.json`의 `first_github_ci_followup`에 남겼다. 노트 출처의 전체 레코드·표시 링크·개수를 effective revision과 대조하고, 실제 페이지 로딩 후 오답/Back 경로를 검사한다. 두 번째 CI의 실제 모바일 경고 문제와 보완은 `second_github_ci_followup`에 기록했다. 실패한 실행을 PASS로 바꾸어 기록하지 않는다.

실행 명령 및 후속 CI: `python scripts/build_full_corpus_review.py --check`, `python scripts/build_quality_status.py --check`, 대표문항 builder·audit ledger·similarity·보호 검사, notes/study/refresh builders `--check`, `python scripts/validate_all.py`, `python -m pytest -q`, `python scripts/publish_practice.py --output public-site`, 기존 HTTP/production workflow. 실행하지 않은 명령은 PASS로 승계하지 않는다.

### 다음 배치 — CDTM05–12, 중복 신설 없이 재검토

먼저 현재 배치의 QA·CI·배포와 공개 origin 확인을 완료한다. 이후 원본 **`MA-EXP-0241`–`0272` 32개**와 이미 존재하는 개정판 **`MA-RW-0029`–`0036` 8개**를 함께 검토한다. 아래 표는 현재 데이터·replacement mapping으로 확인한 대기 목록이며 이번 법규 검토 완료 목록이 아니다.

| Family | 원본 ID 범위 | 기존 대표 → 기존 개정판 | 우선 주제 | 연결 노트 |
|---|---|---|---|---|
| CDTM05 | MA-EXP-0241–0244 | MA-EXP-0243 → MA-RW-0029 | CDTM CE·역량 유지 | w3-d-4, w1-a-8 |
| CDTM06 | MA-EXP-0245–0248 | MA-EXP-0247 → MA-RW-0030 | Prescribing 등록·참여 요건 | w3-d-4 |
| CDTM07 | MA-EXP-0249–0252 | MA-EXP-0251 → MA-RW-0031 | Practice setting 승인 | w3-d-5 |
| CDTM08 | MA-EXP-0253–0256 | MA-EXP-0255 → MA-RW-0032 | Retail 성인 환자·referral | w3-d-6 |
| CDTM09 | MA-EXP-0257–0260 | MA-EXP-0259 → MA-RW-0033 | Consent 사본·communication 기한 | w3-d-6, w3-d-8 |
| CDTM10 | MA-EXP-0261–0264 | MA-EXP-0263 → MA-RW-0034 | Retail 기존 치료 연장 | w3-d-7 |
| CDTM11 | MA-EXP-0265–0268 | MA-EXP-0267 → MA-RW-0035 | Referral 진단에 따른 범위 | w3-d-7 |
| CDTM12 | MA-EXP-0269–0272 | MA-EXP-0271 → MA-RW-0036 | Retail schedule 제한 | w3-d-7, w2-a-2, authority-paths |

기존 개정판이 있다는 이유로 40개를 검토 완료로 계산하지 않으며, 같은 판단을 새 ID로 중복 생성하지 않는다. 0233–0236의 미해결 자격 관계와 이번 23개 minor-edit 원본은 별도의 미완료 항목으로 유지한다. 다음 실행에서는 먼저 실제 main SHA와 이 checkpoint 이후의 변경을 대조한다.

---

## 과거 checkpoint — Unit 3A

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

## MOR 추적표·presence 노트 구현 — 2026-10-30

시작 main a9e18a4e3281e1184cb28c29e166ec56ba661426. PR175의 MA-EXP-0177–0192 작성자 선택지64개 기록을 complete-record hash로 재결합했다. 누적57 ID,미재검증2277. 원본1024개 구조검사는 법규완료수가 아니다. 대표355의62/3/10/280,archive2334/default438은 그대로다. 새문항 draft는 아직 활성화하지 않았다.

w1-c-7 presence trigger(영업 중/무제한접근 각각)와nonresident 예외를 versioned overlay로 구현했다. 원본guide 및 이전2개 revision·export를 보존하고 정확한generated export 한 경로에만 세번째 migration을 추가했다. Anchor/bookmark/읽음기록은 유지하고판본재독 안내를 표시한다. Presence claim1개 추가:전체claims17/author checked15/OPEN2; unit전체 census가 아니다. LAW/RF에서w1-c-7 수동연결은없으며공통source provenance를재생성했다.

새 보호테스트17 PASS,초기 full294 PASS. 최종변경후 full suite와canonical검증은별도 validation기록을 따른다. 로컬Chromium다운로드실패로HTTPbrowser NOT_RUN; CI에서검증해야한다. 독립감사/peer NOT_RUN,RELEASED추가0. Merge/production미확인이다. 다음:노트배포와CI를마친뒤MOR07–09·MOR10 신규사례개정/선택연결을구현하고DISC01–08을개별검토한다. CE통지/인원비율OPEN은유지한다.


## MOR·DISC01–04 구현 checkpoint — 2026-10-30

PR175의 검토자료를 실제 학습판 개정으로 전환했다. 원본0177–0208 32개·128선택지 기록, 새0069–0076 8개·33선택지, 노트w1-c-4/5/7/13와w6-b-8 개정. MOR10 all-correct SATA는 새0072의B,D사례로 연결되며 원본0191과 풀이·북마크를 보존한다. 공식NABP근거로 시설운영 문항의1.2분류를 새판본에서4.x등으로 교정했다. 자세한 범위는docs/MOR_DISCIPLINE_20261030.md.

현재archive2342/default438, 대표355=70재작성+3기존통합+10보류+272미반영. 누적ID검토기록81(보류10포함), 미재검증2261. 제한된노트claims/claimclusters35(33sourcechecked/2OPEN), atomic census미완료. 원본1024구조검사는별도이며canonical439의감사/release상태는변경없다. 같은팀peer와canonical독립감사는구별한다.

이문단은병합전구현snapshot이다. 실제검사결과는reports/full-corpus-review/mor-discipline-validation.json, 병합/Pages/production상태는PR175의최종기록과해당mergeSHAworkflow를확인한다. 배포확인없이완료로보고하지않는다. 다음범위는DISC05–08 원본0209–0224/대표0211,0215,0219,0223 및w1-c-14/15,w4-d-17이다. 이전CE·인원관계OPEN과PLUS source자격을유지한다.
