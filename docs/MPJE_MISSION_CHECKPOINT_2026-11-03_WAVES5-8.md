# MPJE 임무 재개 체크포인트: waves5–8와 최종 노트 수정

이 기록은 PR184/main `3f93165e18af53d8a9dfcfe654805ba61164e303` 이후의 작업이다. 전체 완료 선언이 아니다. 이전 기록과 실패 판정, 보호 원문, 원래 정답과 사용자 기록을 보존한다.

## 현재 통합 상태

- Wave5: MA-CASE-0482–0641, 160개.
- Wave6: MA-CASE-0642–0801, 160개.
- Wave7: MA-CASE-0802–0963 중 이미 검토한0812/0814를 제외한160개.
- Wave8: MA-CASE-0964–1123, 160개.
- 정확한 ID·원문 hash·worker commit·증거 SHA는 각 wave의4개 result manifest와 work-queue에 있다. 각각 별도 작업 branch에서 원문과 모든 보기를 읽고 순차 통합했다. INTEGRATED는 release나 독립 감사 PASS가 아니다.
- 새 640개 중 48개에 실제 모호성·근거 보류·해설 수정 사항을 기록했다. 기존 보류 경고로 이미 안내된5개 외43개에 hash-bound 보관 경고를 추가했다. 해당48개는 현재 기본 추천에 없다. 단순 반복이나 수치라는 이유로 다른 문항을 일괄 실패 처리하지 않았다.
- HIPAA 자발적 동의와 필수 authorization, opened ScheduleIV 용기의 수량 누락, technician medication-history 자격, 상담 designee 자격, CE Form과 email, full USP 접근 제한, CDTM PharmD 조문 관계, LAI/OTP 적용 관계를 구분해 기록했다. 공식 원문을 확인하지 못한 해석은 차단한다.
- CASE0668B/0670B/0671B/0673A의 최초 발행일 정확한 위치를 21CFR1306.25(b)(3)(i)로 정정한 별도 errata를 적용한다. 원 보고서 바이트와 원 답안은 바꾸지 않는다.
- CASE0217의 미조제 EPCS 전송은 MA Policy2023-10 §I의 추가 공식 근거로 작성자 단계 source blocker를 해소했다. 정확한 한 원문에만 적용하며 남은 편집/독립 감사 보류와 이전 판단 이력은 유지한다.

## 실질 노트 개정과 독립 최종 검토

상담 w3-b-1, Shield w3-d-23, CE w1-a-7 세 절을 H/I versioned overlay로 개정했다. LAW-041·LAW-008·RF-034의 해당 파생 내용도 갱신했다. 상담의 inpatient 예외와 Policy2026-02 alternate supervision, Shield의 정확한 label 범위, CE의 Mandatory Disclosure Form+detailed statement를 설명한다.

H의 최초 최종검토 HOLD는 그대로 보존한다. 누락된 alternate-supervision 설명을 고친 다른 본문에 대해 동일한 실제 감사 세션이 R2 KEEP을 했다. 이를 두 독립 감사로 세지 않는다. CE는 다른 작성자가 final body·17개 claim·LAW-008 patch를 별도 검토했다. H55/I17 주장과 카드 patch는 exact SHA로 묶어 활성화하며 summary KEEP만으로 실패한 claim이나 새 카드 수정을 통과시킬 수 없다. 같은 팀/노출 상황은 보고서에 공개하며 blind 감사라고 주장하지 않는다. 이3절이 다른303절의 독립 검증을 뜻하지 않는다.

보호 notes/guide.json과 이전 revision, question objects는 불변이다. protected export migration은 기존 방식으로 site/notes/complete-notes.md 정확한 한 경로만 허용하며 이전 두 snapshot을 보존한다. 현재 본문 해시에 연결된 SOURCE_BLOCKED 수와 검토 링크를 노트 화면·인쇄·Markdown에 표시한다.

## 분리 지표

- 작성자 개별 검토1445/2346=61.59%, 미검토901개.
- 독립 legacy 법규 키 평가196/2346=8.35%; 200개 읽음 중 미평가4개 제외. 이번 신규 canonical 감사/RELEASED 승격0.
- 새 검토1160개에서 신규 문항 재작성·공개0/1160=0%. 안전한 보류·초안은 재작성 완료와 구분한다. 실제 노트 최종 개정3절은 별도로 기록한다.
- 작성자 완전 atomic census92/306=30.07%, 미완료214절. 2743개 현재 주장 중2259개 근거 대조,484개 SOURCE_BLOCKED. 과거16부록 부분 기록728개를 이 수에 더하지 않는다. 명시적 후속 census가 전체본문을 원자분해한 현재 기록만 선택한다.
- 최종 본문에 별도 검토가 있는 노트3/306=0.98%; 독립 전수 열거 완전성은 인증하지 않는다.
- 기본 추천394, 전체2346 유지. 전체 보관 경고418개. 기존 legacy OPEN4개는 historical cluster 기록으로 남아 있으며 새 atomic blockers와 합산하지 않는다.
- 현재 배포 검증 PENDING. 정확한 final head CI와 Pages/공개 바이트를 확인하기 전 PASS로 보고하지 않는다.

## 다음 실행과 영속 상태

Wave9 네40개 작업은 actual claim/token/attempt branch로 LEASED이다. CASE1124–1152와 EXP0001–0011, EXP0012–0051, EXP0052–0091, EXP0092–0120 및0153–0163을 원장이 선정했다. 순차범위 추정으로 빠진 ID를 배정하지 않는다. 별도 노트20절 NOTE-WAVE6, CASE0482–0521 독립 legacy 검토도 진행 중이며 아직 완료 수에 넣지 않는다.

재개 시 remote branch의 최신 commit과 work-queue를 읽고, recover/heartbeat 후 exact job/token을 확인한다. 작업자 결과는 검증 후 순차 통합하고 원장을 재생성한 뒤에만 다음 wave를 plan한다. 공유 generated 파일은 통합 담당자 한 명만 쓴다. 진행하지 않은 감사/테스트/배포는 NOT RUN 또는 PENDING으로 남긴다.
