# 기존 대표 355문항 품질 검토와 첫 재작성 단위

검토일: 2026-10-28. 기준 main: `b5bd6b02c7ea8a5c6731871fa6e330ac6795fd36` (PR #168).

## 실제 완료 범위

기존 355개 대표의 지문·보기·해설을 개별 편집 검토하고, 면허·인력·CE 및 CDTM·예방접종에서 먼저 48개 원문을 처리했다. 새로 쓴 46개는 영어 상황·보기, 한국어 선택지별 이유, 공식 조항·확인일, 관련 통합노트, 판단 경로와 기존 문항과의 차이를 갖춘다. 문항 수 목표를 채우기 위한 동일 규칙의 기계적 변형은 만들지 않았다.

| 기존 355개의 실제 구현 상태 | 수 |
|---|---:|
| 새 ID의 개별 사례로 재작성 | 46 |
| 이미 있는 고품질 사례로 통합 | 1 |
| 검토 보류로 기본 출제에서 제외 | 7 |
| 개별 편집 검토 후 아직 구현하지 않음 | 301 |
| 합계 | 355 |

첫 48개 단위는 재작성 46, 재사용 1, CE 근거 충돌 보류 1이다. 나머지 보류 6개는 전체 편집 검토에서 별도로 발견했다. 301개가 아무 수정 없이 검증을 통과했다는 의미는 아니다. 부족한 영역에 약 120개를 추가하는 후속 목표는 아직 달성하지 않았으며 이번 46개를 그 목표의 신규 영역 사례로 중복 계산하지 않는다.

| 편집 triage 판정 — 구현 상태와 별개 | 수 |
|---|---:|
| KEEP | 0 |
| MINOR EDIT | 30 |
| MAJOR REWRITE | 317 |
| REPLACE | 5 |
| HOLD FOR LEGAL REVIEW | 3 |

위 판정은 원문에 필요한 작업을 나타낸다. 법규 재검증을 하지 않은 원문에는 `NOT_REVERIFIED`를 명시했다. 운영상 보류 7개 중 3개는 CE 법규 출처 충돌이고 4개는 복수 정답 가능성·지문에 없는 사실에 의존한 해설 문제다. 따라서 이 두 표의 hold 수가 다른 것은 분류 목적의 차이다.

개별 355행은 [통합 감사표](../reports/representative-rewrite/audit-ledger.md), 상세 8개 축과 자동 관찰은 [원문 편집 검토 JSON](../reports/representative-rewrite/legacy-editorial-triage.json)에 있다. 새 문제와 원문의 연결은 [selection.json](../practice_expansion/2026-10-28-representative/selection.json)에서 확인할 수 있다.

## 이전 작업 복구 결과

main의 2,041개 파일을 GitHub의 Git blob 해시와 대조하여 snapshot을 확인했다. 대표 재작성 branch와 관련 artifact에는 main snapshot과 workflow만 있었고, 보고됐던 48개 완성 초안은 발견하지 못했다. 다른 branch에는 별개의 미완성 96개 텍스트 초안이 있었으나 대표 문항 매핑과 검증된 질문 JSON이 없었다. 이를 기존 고품질 `MA-REV` 96개나 이번 46개로 혼동하지 않았다. branch·commit·파일 근거는 [복구 기록](../reports/representative-rewrite/recovery.json)에 남겼다.

## 문항과 정답 패턴

| 지표 | 이전 기본 451 | 이번 기본 443 | 이번 재작성 46 |
|---|---:|---:|---:|
| SBA | 153 | 190 | 42 |
| SATA | 298 | 253 | 4 |
| Case A / Case B 병렬 구조 | 256 | 208 | 0 |
| 선택지가 모두 정답인 SATA | 64 | 52 | 0 |
| 정규화 지문 완전 중복의 추가 발생 수 | 0 | 0 | 0 |
| 동일 전체 보기 세트를 공유하는 문항 | 0 | 0 | 0 |

기존 대표 355개만 보면 SBA 69, SATA 286이었다. 기존 보고의 약 80개와 달리, **모든 선택지가 정답인 SATA는 64개**였다. 정답이 4개인 SATA 80개와 구분했다. 모든 선택지가 정답이라는 이유만으로 법적 오답으로 판정하지는 않았다.

새 SBA의 원래 정답 ID는 A/B/C/D 각각 10/10/11/11이다. 실제 화면에서는 선택지 순서를 섞고 stable ID로 채점한다. 정답이 유일하게 가장 긴 SBA는 새 42개 중 10개다. 길이는 단서 검사이며 법적 유효성 판정이 아니다. 교차 검토에서 불필요한 사실 반복을 줄이고 조건이 빠져 오답을 단정할 수 없었던 보기를 고쳤다.

전체 보존 목록은 2,272에서 2,318로 늘었다. 기본 목록은 기존 대표 301 + 기존 고품질 96 + 재작성 46 = 443다. 원문을 삭제하지 않았으므로 전체 목록의 지문 중복 추가 발생 748회와 동일 보기 세트 공유 331개는 그대로 남는다. 이를 중복 제거 성과로 보고하지 않는다.

## 정확·유사·의미 중복의 구분

전체 기존 공개 corpus와 canonical 439개, 새 46개를 합친 2,757개에서 동일 vocabulary를 사용하여 TF-IDF word/bigram 유사도를 비교했다. 숫자 token을 보존했다. 0.90 이상 후보 쌍은 공개 전체에서 746 → 746, 기본 목록에서 0 → 0이다. 새 문제마다 가장 가까운 5개 후보와 작성자가 기록한 기존 96개 비교를 [near-candidates.json](../reports/representative-rewrite/near-candidates.json)에 남겼다. 낮은 문구 유사도는 다른 법적 판단이라는 증명이 아니다.

별도의 [의미 검토 기록](../reports/representative-rewrite/semantic-review.json)은 원문 355개 각각의 판단 signature와 47개 쌍의 실제 편집 비교를 담는다. 같은 상황을 공유하는 30개 묶음, 동일 판단 경로 1쌍, 산술만 추가한 같은 법적 경로 3쌍, 부분 겹침과 조건에 따른 다른 판단을 구별했다. 이는 모든 문항 쌍의 수동 검토가 아니다. 전체 corpus 의미 중복의 개선 전후 총수를 추정하거나 0이라고 선언하지 않는다. 이번에는 실제 판단이 겹친 기존 대표 1개를 이미 있는 `MA-REV-0009`로 통합했다.

## 출처와 보류

작성자는 247 CMR 3/4/8/16, M.G.L., Board CE·CDTM·예방접종 정책, 해당 DPH standing order와 제품 labeling 등 각 사례에 필요한 공식 원문을 대조했다. 원문 URL, 정확한 조항, 2026-10-28 확인일, 열람 경로와 범위는 작성 파일과 생성 데이터의 source records에 있다. 일부 Mass.gov 직접 요청이 차단되어 공식 URL의 본문 추출과 공식 검색 결과를 사용했다. 모든 PDF 바이너리의 최신 개정 여부를 직접 다운로드로 입증한 검토는 아니다. 기존 통합노트의 과거 확인일과 OPEN을 새 확인일로 덮지 않았다.

주요 보류·경계는 다음과 같다.

- **CE 미이수 통지:** 기존 노트·문항의 email 지시와 현재 [Policy 2021-04, 2025-09-04 개정](https://www.mass.gov/doc/2021-04-continuing-education-ce-requirements-pdf/download)의 Mandatory Disclosure Form 문구가 다르다. `MA-EXP-0051`, `MA-CASE-0795`, `MA-CASE-0349`는 기본 출제에서 제외했다. 같은 지시가 반복된 원본 17개에도 안내를 연결했다. 원문의 정답을 조용히 바꾸거나 미확인 보고 기한을 새 정답으로 만들지 않았다. [출처 충돌 기록](../reports/representative-rewrite/ce-deficiency-source-conflict.json)
- **정답의 비유일성·누락된 사실:** `MA-CASE-0082`, `0100`, `0122`, `0708`은 넓은 행동과 구체적 행동이 모두 정답이거나 해설이 지문에 없는 수량·조건을 전제한다. 기본 출제에서 제외하고 원문은 남겼다. [보류 근거](../reports/representative-rewrite/default-holds.json)
- **CDTM 자격:** PharmD 경로의 statute/regulation 적용 관계를 단정하는 distractor를 제거했다. 실제 확인한 BPS/PGY2 교육 동등성·현장 credentialing 조건만 묻는다. 과거 grandfather 경계일을 단일 정답으로 만들지 않았다.
- **Technician 예방접종:** 일반 247 CMR 8의 제한과 technician을 명시한 105 CMR 700.004(B)(6), DPH/Board/DCP Policy 2023-02의 특정 경로를 함께 기록했다. 0045–0047은 해당 경로의 자격·교육 요소를 묻고 일반적인 무제한 투여 권한을 승인하지 않는다.

이번 46개는 **작성자 출처 대조 + 같은 작업 팀의 선택지별 교차 검토**를 거쳤다. 이것을 repository의 canonical 독립 법규·현실성 감사로 표현하지 않는다. canonical `RELEASED`와 독립 감사 파일은 변경하지 않았고 새 질문의 독립 감사 값도 null이다.

현재 [NABP Competency Statements](https://nabp.pharmacy/programs/examinations/mpje/competency-statements/)에 따라 2027-03-01 이전 시험용 매핑을 유지했다. 이후 시험에 적용되는 outline은 별도다. 비공개 시험, 응시자 복원 자료, 비공개 Pre-MPJE 문항은 사용하지 않았다.

## 기록 보존과 웹 동작

원본 2,272개와 기존 고품질 96개의 ID·내용·정답·해설·source metadata를 유지한다. 새 46개는 새 ID, `content_version`, `revision_of`와 명시적 history policy를 사용한다. 기존 localStorage key `oddments.mpje.practice.v1`, 답안과 북마크를 지우거나 새 질문으로 이행하지 않는다. 두 판본 사이의 링크는 열람 기능이며 기록 이행이 아니다.

기본 20문항과 120문항 연습은 개정된 기본 목록에서 family 중복을 피한다. Chaos10은 필터와 무관하게 전체 2,318개를 복원추출하고 같은 ID·family를 반복할 수 있다. 검토 보류 원본도 보존 목록·ID 검색·북마크에서 열람할 수 있으며, 기존 채점을 확정적 법규 판단으로 사용하지 않도록 안내한다. 법규학습 연결은 개정 사례를 우선하고 보류와 관련 변형을 제외한다. 노트 본문·법규 학습 및 복습 카드의 기존 저장 key는 유지한다.

## 검증 방법과 실행 증거

새 보존 manifest는 실제 main의 Git blob과 대조한 후 작성했다. CI는 보호 파일의 Git blob/SHA-256, 새 문항 source·hash·선택지 계약, 355행의 구현 매핑, deterministic generation, 기존 학습 계약을 확인한다. 원본을 수정한 뒤 baseline을 자동 갱신하는 기능은 없다.

`representative-quality-qa.yml`은 기존 공개 연습 검사와 새 real-HTTP 브라우저 검사를 실행한다. 새 검사는 기존 기록 seed → 개정판 별도 채점 → reload → bookmark → backup/import, 모든 46개 정답·오답 및 표시된 답안 글자, 320px 레이아웃, 선택지별 조항 링크, 보류 원문, 20/120/Chaos10을 확인한다. 실패한 실행도 완료된 문항 ID만 기록하며 계획된 문항 수를 완료 수로 보고하지 않는다. Pages 성공 후에는 실제 공개 origin에서 같은 검사를 다시 실행한다.

실행 환경의 Python 의존성·Chromium 미설치로 로컬에서 실행하지 못한 검사는 CI 결과로 판정한다. 테스트 목록이 존재하는 것과 실제 통과는 다르다. [해당 workflow 실행 내역](https://github.com/woojunxnam/oddments/actions/workflows/representative-quality-qa.yml)과 [기존 품질 QA](https://github.com/woojunxnam/oddments/actions/workflows/practice-quality-qa.yml)의 commit 및 artifacts를 함께 확인한다. 실제 모바일 기기·Safari, 전 corpus의 독립 법규 감사, MPJE 난도·합격 예측은 검증 대상에 포함하지 않았다.

첫 CI head `63417c79`에서는 새 계약을 포함한 123개 Python 테스트, 공개 문제풀이 22개 브라우저 검사, 새 판본·기록 검사 11개(46개 각각 정답·오답 채점)가 통과했다. 기존 원고 status 페이지 검사만 이미 있던 공통 이동 메뉴 script와 오래된 script-count 0 조건의 불일치로 실패했다. 이 조건은 정확히 `learning-tools.js` 한 개만 허용하면서 inline/question JSON과 문제풀이 runtime이 없는지 검사하도록 수정했다. 원고의 DRAFT·RELEASED 0 경계와 기존 26개 archive reader 검사는 유지했다. 이 최초 실행의 성공 수치를 이후 commit의 전체 CI 성공으로 대신 사용하지 않는다.

## 이어갈 작업

남은 대표 301개는 개별 triage의 우선순위에 따라 30–50개 단위로 처리한다. 재작성 전에 연관된 기존 고품질 사례와 통합할지, 조건이 실제로 결론을 바꾸는 새로운 사례인지 결정한다. 보류 7개는 단순 표현 수정으로 풀 수 있는 항목과 공식 적용 관계를 확인해야 하는 항목을 구별한다. 부족 영역의 추가 사례는 이 작업과 별도로 gap를 입증한 뒤 작성하며, 목표 개수를 채우기 위해 이름·약물·숫자만 바꾼 변형을 만들지 않는다.
