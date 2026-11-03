# 후속 통제 배치 재개 기록

이 기록은 PR183 이후 작업이다. 전체 임무 완료 선언이 아니다. 앞선 배포 증거는 `reports/full-corpus-review/pr183-deployment.json`에 보존했다. PR183은 CI16개 성공 후 merge되었고 Pages run41645177536이 성공했으며 공개 HTML/manifest/품질페이지3개가 로컬 검증본과 byte-for-byte 일치했다.

## 실제 추가 작업

- Wave3: MA-CASE-0162–0321,160문항/640보기.
- Wave4: MA-CASE-0322–0481,160문항/640보기.
- 각각 원장 hash로 배정하고 독립 branch/worktree에서 원문·모든 선택지·기존 한국어 해설을 읽고 공식 자료를 확인한 뒤 순차 통합했다. 정확한 IDs·원문 hash·worker commit·증거 digest는 wave3/4 각4개 result manifest와 work-queue에 있다.
- 작성자 KEEP과 실제 해설 결함·모호한 키·SOURCE_BLOCKED를 구분했다. 반복 또는 수치 문제라는 이유만으로 실패 처리하지 않았다. 신규 문항/정답 덮어쓰기/RELEASED 승격은 없다.
- 별도 독립 세션이 wave2 원문160개/640보기를 읽고132 YES,24 AMBIGUOUS,4 NOT_ASSESSED로 판정했다. 실제 키평가는156개만 집계한다. 요약 노출과 저자 보고서 파일 미열람을 독립성 한계로 공개했으며 blinded라고 주장하지 않는다. Canonical 감사 등록이나 realism PASS로 인정하지 않는다.

## 구체적 판정

- CII partial-fill72시간/30일,5회·6개월 refill, MA VI 이전1년,90일 non-opioid, single-dispense caps, ID/hardship, initial EPCS transfer 및 inventory를 exact clause별로 확인했다.
- MA-CASE0212–0216은 넓은 미래 교정 행동끼리 겹쳐 단일정답이 모호하다.0217의 연방 first-fill CII transfer와 Massachusetts 허용 관계는 SOURCE_BLOCKED이다.
-0262–0270은 공개 government-hosted USP2022 표를 읽었으나 현행 full USP795 접근403으로 적용 전체를 인증하지 않았다.
-0307–0315의 기존 네 보기 해설은 정답 기한만 반복하여 '일찍 제출 가능'과 '가장 늦은 답'을 구별하지 못했다. 문항별 보고서에는 각각의 차이를 설명했다. 기존 해설은 덮어쓰지 않았다.
-0329/0333은 minor reaction의 즉시 소통과24시간 권고가 양립할 수 있어 HOLD.0346 등 CE email-only와 현행 Mandatory Disclosure Form·statement 관계는 원문과 별도 기록했다.
-0405는 technician 자격 tier가 불명확하고0428은 HIPAA의 선택적 치료 동의와 법적 의무가 혼동되어 HOLD. 관련 보관 문항에 hash-bound 경고도 추가했다.
-0415/0417/0418/0419/0420/0423은 outpatient와 hospital PPI 예외 설정을 명확히 해야 한다.
- Clozapine REMS 제거와 prescriber ANC monitoring을 구분하고 약사의 조제전 ANC gate를 다시 만들지 않았다. iPLEDGE2026-11-15 변경은 현재 기준 미래 시행임을 구분했다. FDA/REMS/SPL의 제품별 제형·현재 Rx상태를 확인한 문항은 작성자 KEEP을 허용했다.
- 독립 후속 검토가 추가한0125와0157/0158/0159/0161의 ambiguity/단일EPCS 직접근거 미확인도 보류에 반영했다. 이전 실패/보류를 다른 KEEP으로 override하지 않았다.

## 노트: 완료와 부분 기록 분리

추가40유닛을 읽었다. 먼저 약물 부록16절·산문4절에서772개 기록을 만들었지만 부록의728개는 추가 원자분해가 필요한 부분 기록이다.4절의44개 주장만 완전 열거에 포함했다. 이후 다른20절323개 주장을 열거했다.

누적 author census는36/306절(11.76%),완료유닛 주장537개 중454개 공식 근거대조·83개 SOURCE_BLOCKED이다. 부분 부록728개는 이537개에서 제외한다. 독립 completeness 또는 전체 법규 PASS가 아니다. 저장 body hash와 실제 UTF8 본문 hash를 함께 보여주고 실제 본문으로만 census freshness를 검증한다. 부분 clause를 COMPLETE로 바꾸면 validator가 실패한다.

공식 HIV/STI DOCX4개(PrEP/PEP/STI/DoxyPEP)를 확보했다. 과거 접근불가 note는 현재 수정 필요로 표시했지만 임상 알고리즘 전체를 자동 인증하지 않았다. oral2일/7business days,VI14/30일,학교 자격AND/OR,예방접종CE annual/biennial 관계도 해당 보고서에서 차단했다. 기존 OPEN4개를 임의로 닫지 않았다.

상담/Shield2절·카드 candidate는 독립 최종검토 HOLD 그대로 미적용이다. 본문 개정 완료로 세지 않는다.

## 분리 지표와 다음 작업

- 작성자 검토805/2346=34.31%,미검토1541개.
- 독립 legacy 법규 키평가196/2346=8.35%;읽음200개 중 미평가4개는 제외. Canonical release 감사 충족/승격0개.
- 이번520개의 실질 새ID 재작성·출판0/520=0%. 기본 추천에서 새로 보류한44개는 재작성과 구분한다. 전체 기본 추천438→394,전체 보관2346 유지.
- 노트 작성자 완전 열거36/306=11.76%,미완료270절(부분 부록16절 포함). 독립 전수 완료0개.
- 배포 검증은 정확한 commit의 Pages/공개 응답으로 별도 확인한다. 이 기록만으로 후속 배포를 인증하지 않는다.

큐에는 다음4×40,MA-CASE0482–0641이 QUEUED 상태다. 이후에도 `recover`→`claim`→attempt branch/worktree→문항별 검토→제출→순차통합→원장재생성→다음계획 순서로 진행한다. 아직 필요한 새 사례 작성·독립 final-hash 감사·270절 census를 생략하고 숫자만 채워 완료 선언하지 않는다.

QA 실행 결과와 정확한 최종head CI는 후속 PR을 확인한다. 보호 입력과 release/governance 정책은 유지했다. 미실행 검사는 NOT RUN으로 남긴다.
