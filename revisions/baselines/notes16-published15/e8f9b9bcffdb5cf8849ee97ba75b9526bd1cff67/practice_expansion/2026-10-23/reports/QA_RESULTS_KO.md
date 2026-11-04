# 실행 검증 결과 — 2026-10-23

## 결과 요약

생성: **1,024문항 / 256 family / 512 공유 사례**. 기존 GitHub 기록 수정·commit·PR·배포는 **없음**. 신규 RELEASED는 **0**이다.

구조검사 결과는 **STRUCTURAL_PASS**, 오류 **0개**다. 이 검사는 법률 내용이나 실제 시험의 난도를 판정하지 않는다.

| 점검 | 결과와 한계 |
|---|---|
| 신규 ID·보기·정답집합·해설 매핑 | 구조 통과. SBA 768, SATA 256 |
| 보기 위치 | SBA A/B/C/D 각각 192개. 실제 시험 분포 주장이 아님 |
| 복수선택 | 정답 수 1/2/3/4개 각 64문항. NABP 채점방식 재현 아님 |
| 노트 참조 | 218절의 ID·본문 hash 및 연결 source ID 확인 |
| 동일 normalized stem | 신규 내부 완전일치 0건. Family 내 사례 재사용은 의도적으로 존재 |
| 기존 레코드와 비교 | 439개 snapshot 레코드의 ID 충돌 0·stem 완전일치 0. Semantic 중복 CLEAR 아님 |
| 새 검토 상태 | 전부 DRAFT, 독립 법규·현실성 검토 0, publication_eligible=false |
| UI | Chromium DOM harness 24개 검사 통과, page error 0개 |
| 추가 전용 적용 스크립트 | 로컬 disposable repository 6개 검사 통과 |

## 콘텐츠 품질 검토에 남긴 신호

624문항의 보기에는 absolute-cue 단어가 하나 이상 있다. 모든 단어가 잘못된 것은 아니지만 불필요한 답 힌트가 되는지 검토해야 한다. SBA 768개 중 227개의 정답 보기가 다른 보기보다 단어 수가 엄격히 더 길다. 네 변형이라는 규칙적인 family 구조와 256개의 negative lead-in 문항도 현실성 검토 대상이다. 이 판은 정답률을 높게 보이도록 만든 합격 예측 모형이 아니다.

기존 문항과의 lexical 유사도가 높은 일부 family:

| 새 family | 기존 문항 | TF-IDF cosine |
|---|---|---|
| STO01 | MA-Q-0396 | 0.3613 |
| CII10 | MA-Q-0157 | 0.3418 |
| RET01 | MA-Q-0225 | 0.3284 |
| LAB08 | MA-Q-0433 | 0.2906 |
| DISC03 | MA-Q-0222 | 0.2804 |
| REF06 | MA-Q-0019 | 0.2739 |
| PUB12 | MA-Q-0143 | 0.2523 |
| LIC08 | MA-Q-0278 | 0.2455 |

같은 법규·업무를 다루면 단어가 비슷할 수 있다. 반대로 cosine이 낮아도 같은 판단을 반복할 수 있다. 따라서 이 점수나 0.25 threshold를 semantic 중복 통과 기준으로 사용하지 않는다. 신규 family 사이에도 아래 쌍을 검토 큐에 남겼다.

- PER15 / PER16: 0.3461
- LIC03 / LIC04: 0.3405
- PER06 / PER09: 0.2731
- VAX08 / PUB04: 0.2508

## 브라우저 검사 환경

로컬 HTTP 및 file URL로 접근하려는 시도는 **ERR_BLOCKED_BY_ADMINISTRATOR**로 차단되었다. 이를 우회하거나 실제 origin 검증에 성공했다고 기록하지 않았다. 대신 Chromium `set_content`로 동일 HTML을 렌더링하고 명시적 mock storage를 주입한 제한된 검사 환경을 사용했다.

그 환경에서 모든 1,024문항의 표시, 단일·복수 답안 처리, 선택지별 해설, 한국어·영어·ID 검색, 필터, 20/120 family 중복 없는 세트, 타이머 표시·해설 지연, 제출 답안 검토, 북마크, mock 저장 복원, 기록 export/import·오류 거절, 별도 저장 key, 키보드 skip link, 저장 불가 환경 대응을 확인했다. 320/390/768/1440px에서 가로 overflow가 없었다. Screenshot도 확인했다.

실제 HTTP/file origin의 localStorage 지속성, 파일앱의 JavaScript 지원, 실제 iOS/Android/Safari, GitHub Pages 배포, 사용자 보조공학 환경은 **미검증**이다. 기록 import의 비동기 완료를 테스트가 기다리도록 수정했고, 한국어 검색에 관련 노트 제목을 포함하도록 개선한 뒤 다시 검사했다.

## 적용 스크립트 검사

Dry run은 쓰기 없음. 적용은 지정 subtree에만 추가하며 모든 원래 sentinel 파일 byte를 보존했다. 기존 destination 덮어쓰기, 변경된 guide snapshot, symlink destination은 거절했다. Git commit/push나 release 상태 변경은 실행하지 않는다.

## 법적 내용의 검토 상태

통합노트의 기존 확인 범위와 일부 새 primary-source 점검을 승계했지만, 각 문항을 독립 감사한 것은 아니다. Exact authority·정답의 법적 유일성·모든 distractor의 오답성·canonical dependency mapping을 reviewer가 확인해야 한다. 테스트 통과 수를 법률 정확도나 합격 가능성으로 환산하지 않는다.
