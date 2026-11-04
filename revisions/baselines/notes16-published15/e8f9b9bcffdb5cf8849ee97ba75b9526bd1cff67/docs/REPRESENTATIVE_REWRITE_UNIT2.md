# 두 번째 품질 단위와 필터 안내 개선

2026-10-29 · 작업 기준 main: `f112d3578664aa51785ba4596547e8d722fad36c`

## 실제 반영 범위

기존 대표 **12개**를 처리했다. **새 ID로 재작성 10개, 이미 있는 고품질 사례로 통합 2개**다. 새로운 보류는 없으며 이전 보류 7개를 유지한다. 새 10개는 부족 영역에 별도로 추가할 약 120개 목표에 중복 집계하지 않는다.

| 기존 대표 | 반영 문항 | 처리 |
|---|---|---|
| MA-EXP-0099 | MA-REV-0006 | unchanged-refill 판단을 기존 사례로 통합 |
| MA-EXP-0103 | MA-RW-0050 | 현행 certified-technician 자격과 새 oral prescription 수신 |
| MA-EXP-0107 | MA-RW-0051 | Schedule VI 권한과 Schedule IV refill transfer의 수행자 구분 |
| MA-EXP-0111 | MA-REV-0008 | patient-specific 최종 검수 판단을 기존 사례로 통합 |
| MA-EXP-0115 | MA-RW-0053 | 완성된 CII 처방 운반과 raw-stock counting 구분 |
| MA-EXP-0119 | MA-RW-0054 | perpetual count 확인, routine entry, discrepancy adjustment 구분 |
| MA-EXP-0155 | MA-RW-0055 | 개인 약사 면허와 retail 시설면허 구분 |
| MA-EXP-0159 | MA-RW-0056 | 최초 개업 기한과 시설면허 만료일 구분 |
| MA-EXP-0163 | MA-RW-0057 | nonresident 신청 증빙과 inspection의 서로 다른 유효 기간 |
| MA-EXP-0167 | MA-RW-0058 | 만료·반품대기 재고의 보안과 근무 약사의 책임 |
| MA-EXP-0171 | MA-RW-0059 | outgoing MOR의 중병 시 inventory 서명 경로와 신청서 구분 |
| MA-EXP-0175 | MA-RW-0060 | 이미 발생한 명칭 변경과 향후 매각의 filing clocks 구분 |

새 문항은 영어 사례·보기와 **42개 선택지별 한국어 해설·공식 조항**을 포함한다. SBA 8개, SATA 2개다. SBA의 원래 정답 ID는 A/B/C/D 각각 2개이고 실제 화면은 보기 순서를 섞는다. SATA 정답 수는 2/5와 3/5이며 전부 정답인 문제는 없다. 글자수 기준 정답만 유일하게 가장 긴 SBA는 0/8이다. 이는 형식 단서 관찰이며 법규 정확성이나 난도 검증을 대신하지 않는다.

### 누적 처리 상태

| 기존 대표 355개 | 이전 단위 후 | 이번 단위 후 |
|---|---:|---:|
| 새 ID로 재작성 | 46 | 56 |
| 기존 고품질 사례로 통합 | 1 | 3 |
| 기본 목록에서 보류 | 7 | 7 |
| 편집 검토 후 개선 미반영 | 301 | 289 |
| 기본 목록 | 443 | 441 |
| 전체 보존 목록 | 2,318 | 2,328 |

현재 기본 441개 = 기존 대표 289개 + 기존 고품질 96개 + 재작성 56개다. 두 통합 대상은 이미 기본 목록에 있던 문항을 사용하므로 기본 문항 수는 2개 줄었다. 원본이나 기존 풀이 기록을 삭제한 결과가 아니다. 원문 355개의 최초 편집 triage는 여전히 법규 전수 재검증이 아니며 `NOT_REVERIFIED` 상태를 유지한다.

## 학습 범위와 문항 묶음이 다르게 보였던 이유

기존 화면의 `학습 범위`는 대표·개정 문항 또는 모든 변형을 고르는 포함 기준이었다. `문항 묶음`은 질문을 작성·보관한 모음을 고르는 기준이었다. 두 조건은 교집합으로 적용되지만, 모음 선택란에는 보관 총수만 표시되어 실제 출제 대상 수처럼 읽힐 수 있었다.

이번에는 `문항 포함 범위`와 `문항 모음 (선택)`으로 이름을 구분하고, 모음의 **총 보관 수**와 **현재 조건에 맞는 문항 수**를 별도로 표시한다. 검색·영역·유형·복습 조건을 바꾸면 실제 대상 수도 갱신된다. 작은 화면의 조합 예시와 접근성 label/help 연결도 추가했다.

| 문항 모음 | 대표·개정 우선 | 모든 변형 포함 |
|---|---:|---:|
| 모든 모음 | 441 | 2,328 |
| 대표 재작성 | 56 | 56 |
| 기존 개별 작성·개정 사례 | 96 | 96 |
| 사례형 조건 연습 | 93 | 1,152 |
| 기존 변형 연습 | 196 | 1,024 |

위 표는 다른 필터를 사용하지 않을 때다. 북마크·오답·`MA-` ID 검색은 과거 기록에 접근하도록 포함 범위 제한을 확장하지만, 선택한 모음과 나머지 필터는 계속 적용한다. 일반 20문항과 시간제 120문항은 현재 결과에서 사례 family·반복 지문·보기 제한을 적용하므로 후보가 적으면 세트가 더 짧아질 수 있다. **Chaos10은 계속 전체 모음에서 복원추출**하며 이 필터를 적용하지 않는다.

## 교차 검토에서 실제 바꾼 것

- `MA-RW-0052` 초안은 ADD stock 예외를 배경에 넣었지만, 실제 정답 행동은 `MA-REV-0008`과 같은 patient-specific final-verification 판단이었다. 독립적인 새 사례로 세지 않고 원문 `MA-EXP-0111`을 기존 문항으로 통합했다. 0052 번호는 공개 질문으로 생성하지 않는다.
- `MA-RW-0054`의 오답은 MOR의 귀환이 권한 행사에 반드시 필요하다는 잘못된 전제를 명시하도록 수정했다. 조정할 수 있다는 권한 규정에서 확인하지 않은 즉시조정 기한을 추론하지 않는다.
- `MA-RW-0059`에는 incoming MOR와 authorized staff pharmacist가 실제 inventory를 함께 확인했고 incoming MOR가 이미 서명했다는 사실을 명시했다. 이름만 사후 대리 서명해도 된다는 해석을 막기 위한 사례 사실이며 새로운 법정 공동계수 의무를 주장하는 것은 아니다.
- 새 문항은 관련 공개 사례와 canonical 초안도 비교했다. 일부 canonical 문항과 같은 하위 규칙을 공유한다. 이번 성과는 현재 기본 대표의 품질 개선이며, 전체 corpus에 없던 새 법적 판단 10개를 발견했다는 의미가 아니다.

작성자는 현재 공식 자료를 확인하고, 다른 작업 에이전트가 선택지별 법규·답안·현실성을 다시 검토했다. 근거에는 247 CMR 6/8/9, 관련 M.G.L., Board Scope Policy 2020-15, 105 CMR 721 및 해당 eCFR 조항 등이 포함된다. 시설 허가·nonresident application은 현행 pre-2027 competency 4.7과 연결했다. 정확한 URL·조항·열람 방법·확인일은 작성 파일과 peer 기록에 있다.

일부 Mass.gov 문서는 공식 URL의 본문 추출로 읽었다. Policy 2020-15의 두 공식 URL 기반 추출에서 페이지 수 표시가 달랐으므로 사용한 조항을 대조하고, raw PDF의 전체 바이트·최신성 동일성은 입증하지 않았다고 기록했다. 오래된 MOR advisory의 조문·기한을 현행 규정에 섞지 않았다. 기존 MOR 개인 통지기한의 미해소 적용 관계를 이번 문제로 단정하지 않는다.

**같은 팀의 작성자·peer 검토이며 canonical 독립 감사가 아니다.** 새 독립 법규 감사 기록과 `RELEASED` 승격은 0개다. 기존 고품질 96개와 canonical 감사·정책은 변경하지 않았다.

## 보존과 검증 근거

이전 원본 보호 기준 1,781개 파일을 그대로 사용했다. 추가로 실제 병합 commit `f112d357`의 질문 데이터를 읽어, 이미 공개된 **46개 문항 전체 객체와 45개 source 객체, 두 authoring 파일**을 고정했다. 새 배치의 날짜·edition을 추가해도 이전 문항의 내용·확인일을 덮어쓰지 않는다. 기존 저장 키와 원문/개정판의 별도 ID 정책도 유지한다.

같은 source ID의 새 입력이 확인일·열람 경로를 조용히 바꾸는 분기는 거부하도록 강화했다. 원본 문항의 내용이나 확인일을 바꾼 뒤 content hash까지 재계산한 경우도 보존 검사에서 실패한다.

로컬에서는 `test_representative*.py`의 저장·버전·출처·필터 계약을 실행한다. 생성 HTML의 실제 JavaScript 함수를 Node에서 검사하며, builder·355행 ledger·유사도 보고서·법규학습·복습 자료의 결정적 생성과 기존 보호 파일도 확인한다. pytest 전체 suite와 Playwright 실제 HTTP 검사는 CI에서 실행한다. production job은 Pages에 배포된 같은 commit을 대상으로 새로 공개된 누적 문항 전체의 정답·오답, 저장·북마크·백업·가져오기, 두 필터의 모든 조합, 320px, 20/120/Chaos10을 검증한다.

실제 성공·실패와 commit은 [대표 개정 회귀 workflow](https://github.com/woojunxnam/oddments/actions/workflows/representative-quality-qa.yml) 및 해당 PR의 실행 링크로 확인한다. 이 문서의 검사 범위 설명 자체를 CI 완료 증거로 사용하지 않는다. 실제 모바일 기기·Safari·독립 법규 감사·난도 보정은 포함하지 않는다.

### 연결 자료

- [누적 355문항 감사표](../reports/representative-rewrite/audit-ledger.md)
- [질문과 출처 데이터](../practice_expansion/2026-10-28-representative/questions.json)
- [명시적 교체·통합·보류 매핑](../practice_expansion/2026-10-28-representative/selection.json)
- [인력 문항 peer 검토](../reports/representative-rewrite/unit2-personnel-peer-review.json)
- [약국 운영 문항 peer 검토](../reports/representative-rewrite/unit2-operations-peer-review.json)
- [의미 중복 편집 검토](../reports/representative-rewrite/unit2-editorial-semantic-review.json)
- [보존 코드 peer 검토](../reports/representative-rewrite/unit2-code-peer-review.json)
- [후속 작업 계획](../reports/representative-rewrite/followup-plan.md)
