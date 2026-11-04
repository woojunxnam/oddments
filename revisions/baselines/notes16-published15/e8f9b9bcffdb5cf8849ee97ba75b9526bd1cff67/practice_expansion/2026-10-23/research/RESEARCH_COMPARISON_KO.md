# 외부 형식·학습설계 비교와 출처 경계

검토일: 2026-10-23. 이 문서는 질문 본문을 수집한 데이터셋이 아니라, 공개된 시험 안내와 학습제품의 구조를 비교한 기록이다. 유료 문제은행 전체·응시자 복원문항·Pre-MPJE 시험 내용은 열람·복제하지 않았다. 실제 MPJE의 비공개 난이도·보정모수·문항별 정답을 확보했다는 주장이 아니다.

## 1. 확인한 공개 자료와 반영 범위

| 자료 | 확인 범위 | 이 패키지의 설계 판단 | 확인하지 않은 것 |
|---|---|---|---|
| NABP MPJE 시험 안내 | 120문항, 2.5시간, adaptive selected-response 및 pass/fail 안내 | 120문항·150분의 비적응형 시간 연습 제공 | CAT·공식 채점·난도 동등성 |
| NABP 공개 Sample Items | 공개된 예시 PDF의 문항 형식. 1페이지 시각 확인 | 단일선택과 복수선택 UI, 명확한 선택 지시 | 예시 문구를 복사하거나 살짝 바꾼 문항 |
| NABP Competency Statements | 현재 네 영역과 세부 범위, 2027-03-01 전환 안내 | 잠정 area/competency 태그 및 주요 범위 배분 | 세부 매핑의 독립 감사·모든 세부 범위의 완전성 |
| UWorld / RxPrep | 공개 제품 안내·sample 페이지의 형식과 기능 설명 | 노트→문제→해설의 연결, 주제 선택·복습 | 구독 문항 전체, 개인별 합격률, 문항 난도 모수 |
| PharmLaw Massachusetts | 공개 course/curriculum 안내 | Federal/state, compounding, drug identification 범위 점검 | 유료 강의·문제은행. 후속 재접속은 fetch 오류였으므로 새 내용 확인으로 세지 않음 |
| PharmacyExam / RxExam Massachusetts | 공개 상품 설명·기존 공개 학습계획 안내 | 답과 해설, 원문 연결, 반복 복습 구조 | 비공개 온라인 시험 전체·상업 문항의 재생성 |
| NABP Pre-MPJE 안내 | 공개 제품·이용조건 안내만 | 비공개 실제 연습시험 문항을 자료로 사용하지 않는 경계 확인 | Pre-MPJE의 문항·정답·스크린샷·전사본 |

이런 일반적인 기능·형식의 관찰은 특정 제품의 정답·법규 내용이 옳다는 근거가 아니다. 새 문항의 직접 출발점은 사용자의 통합노트이며, 선택적인 공식 출처 재확인은 아래에서 따로 기록했다. Vendor의 마케팅 주장이나 출판 문항 수를 품질의 증거로 사용하지 않았다. 상업 문항 텍스트, close paraphrase, embeddings, source-signals 레코드를 canonical 저장소에 만들지 않았다.

공개 비교 URL:
- https://nabp.pharmacy/programs/examinations/mpje/take-the-mpje-exam/
- https://nabp.pharmacy/wp-content/uploads/2020/07/MPJE-Sample-Questions-1.pdf
- https://nabp.pharmacy/programs/examinations/mpje/competency-statements/
- https://nabp.pharmacy/programs/practice-exams/pre-mpje/
- https://pharmacy.uworld.com/mpje/
- https://pharmacy.uworld.com/mpje/sample-questions/
- https://www.pharmlaw.com/courses/massachusetts-mpje-prep
- https://www.pharmacyexam.com/index.cfm/product/62/massachusetts-pharmacy-law-test-online-access.cfm

## 2. 원자료와 새로 만든 부분

**원자료에서 승계:** 통합노트 edition 2026-10-23.1의 규칙 설명, 예외·미확정 경계, source IDs, 각 절의 기존 확인일. 전체 306절 중 218절을 문항에 연결했다. 이 수치는 시험 범위 71% 같은 법적 coverage 점수로 환산하지 않는다. 노트의 참고문헌은 장·절 단위로 연결된 문헌이며 모든 문항 선택지의 exact authority를 이번 작업에서 독립 검증한 기록은 아니다.

**이번에 새로 작성:** 256개의 두-사례 family, family당 네 쌍의 옳은 설명/그럴듯한 오해, 한국어 구분 해설. 이를 Case A 판단, Case B 판단, 복수 조건 판단, 오류 식별의 네 연습으로 구체화했다. 총 1,024문항이지만 1,024개의 독립 vignette나 1,024개의 별도 법규를 의미하지 않는다. 같은 family의 4문항은 동일한 두 사례를 공유한다. 단순 이름·숫자 무작위 교체로 사례 수를 늘리지 않았다.

**편집적 선택:** 3 SBA + 1 SATA의 family 구성, 보기 위치 균형, local exact-match 채점, family당 최대 한 문항인 연습 세트. 이는 NABP가 공개한 실제 문항유형 비율·scoring algorithm이 아니다. 영역별 작성량은 잠정 태그 기준 224/336/228/236이며, 실제 시험 비율을 정확히 복제한 배분도 아니다.

## 3. 선택적으로 다시 읽은 공식 출처

아래는 좁은 주제의 재확인이지 1,024문항 전수 법률감사가 아니다. Massachusetts PDF는 추출 텍스트를 읽었으며 직접 PDF 시각 접근이 차단된 자료를 시각검수 완료로 표시하지 않는다. eCFR 편집본의 표시 날짜와 이 자료의 검토일도 구별한다.

| 공식 출처 | 실제로 점검한 경계 |
|---|---|
| MA Policy 2026-02 | support-personnel ratio, 전담 trainer/trainee, intern supervision |
| MA Policy 2020-15 | 인력별 업무범위. 오래된 administration 참조는 후속 2026 circular와 구별 |
| MA Policy 2021-04, 2025-09-04 개정 | CE annual/live/law, specialized CE, 미충족 사유 email |
| MA Policy 2023-02, 2025-09-04 개정 | 백신 인력·교육·연령·주문·MIIS·predrawing 조건 |
| MA DCP 26-03-124, 2026-03-11 | 일반 약물 투여: 18세 이상, non-IV, 제품·훈련·CPR·기록·serious-event communication |
| HHS HIPAA breach guidance | HHS 보고의 500명 이상, 언론 통지의 한 주/관할 주민 500명 초과, 개별 통지 시계 |
| HHS access FAQ | 수령 후 30 calendar days, 한 번의 30일 연장 조건, BA 보관으로 시계 리셋 불가 |
| HHS 42 CFR Part 2 fact sheet | 관련 2026 compliance, 동의·TPO·법적 절차의 구별 |
| eCFR 21 CFR 1306.13 | CII 재고부족 72시간과 요청 partial의 다른 시작점·기한 |
| DEA EPCS transfer 안내/FAQ | 최초 미조제 전자처방의 한정 transfer와 원래 paper/fax의 차이 |
| MA Policy 2024-05 공개 안내 | CII/CIII의 해당 OUD·non-opioid·implantable-pump 공급량 경로 |
| eCFR 16 CFR 1700.14 | PPPA의 제품·제형·함량·포장수량별 예외 |
| eCFR 21 CFR 1301.76 | 도난·significant loss, 1 business day 초기 통지, 현재 읽은 게시본의 완료 Form 106 45일 문구 |

접근 URL:
- https://www.mass.gov/doc/2026-02-ratios-supervision-and-dedicated-training-personnel/download
- https://www.mass.gov/doc/2020-15-scope-of-practice-pdf/download
- https://www.mass.gov/doc/2021-04-continuing-education-ce-requirements-pdf/download
- https://www.mass.gov/doc/2023-02-vaccine-administration-pdf/download
- https://www.mass.gov/doc/pharmacist-administration-of-medications-pdf/download
- https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html
- https://www.hhs.gov/hipaa/for-professionals/breach-notification/breach-reporting/index.html
- https://www.hhs.gov/hipaa/for-professionals/faq/how-timely-must-a-covered-entity-be/index.html
- https://www.hhs.gov/hipaa/for-professionals/regulatory-initiatives/fact-sheet-42-cfr-part-2-final-rule/index.html
- https://www.ecfr.gov/current/title-21/chapter-II/part-1306/section-1306.13
- https://www.deadiversion.usdoj.gov/faq/epcs-faq.html
- https://www.dea.gov/stories/2023/2023-09/2023-09-01/revised-regulation-allows-dea-registered-pharmacies-transfer
- https://www.mass.gov/news/policy-2024-05-schedules-ii-and-iii-quantity-limits
- https://www.ecfr.gov/current/title-16/chapter-II/subchapter-E/part-1700/section-1700.14
- https://www.ecfr.gov/current/title-21/chapter-II/part-1301/section-1301.76

추가로 PREP Act 12th Amendment의 공개 HTML 일부를 읽었지만, 전체 기간·모든 경로의 재판정을 마쳤다고 표시하지 않았다. 새 문제에서는 미래의 모든 백신 권한을 일반화하지 않는다.

## 4. 이번 정답에서 확정하지 않은 쟁점

Schedule VI emergency continuation의 14일/30일 통합 적용, MOR의 정확히 30일/100일 경계, 서로 다른 oral follow-up 규정의 통합 해석, CII/CIII multi-drug packaging의 문서 간 관계, 아직 읽지 못한 HIV/STI statewide clinical DOCX의 상세 용량·공급기간, 특별기관 bed-capacity 표의 빈 경계, 변동하는 cannabis 분류·임시 telemedicine 효력은 새 확정 정답으로 만들지 않았다.

OPEN 표시가 있는 큰 절의 좁은 비논쟁 부분만 이용한 경우에도 inherited flag를 유지했다. 예를 들어 일반 VI transfer의 no-fee·one-year 조건을 다루면서 emergency continuation의 14/30일을 결정하지 않는다. 이는 해당 전체 노트를 CLOSED로 변경한 것이 아니다.

## 5. 현실성 개선과 남은 작업

현실적인 혼동 축은 사람·업무·장소·제품·권한·시계·후속 기록으로 설계했다. 재고 entry와 adjustment, first fill과 refill, issue date와 partial-fill date, prescribing과 administration, reporting과 clinical query, source-vial 시간과 final BUD 등을 분리했다.

다만 현재 네 변형의 형식은 규칙적이며, 일부 distractor에는 absolute 표현이나 명백한 일반화가 있다. 자동 점검에서 624문항에 always/never/automatically/every/all/only 중 하나 이상이 있고, SBA 768개 중 227개는 정답 보기가 다른 보기보다 단어 수가 엄격히 더 길었다. 이런 수치는 자동 탈락 판정도, 현실성 통과 판정도 아니다. 불필요한 힌트인지 실제 법적 범위 표현인지 독립 reviewer가 문항별로 판단해야 한다.

따라서 이 판을 상업 문제은행과 동등한 품질 또는 실제 시험과 동등한 난도의 완성본이라고 소개하지 않는다. 모든 새 문항은 DRAFT이며, 법규·현실성·semantic duplicate 검토와 canonical rule mapping이 남아 있다.
