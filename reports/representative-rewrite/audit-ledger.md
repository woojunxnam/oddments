# 기존 대표 355문항: 편집 판정과 실제 반영 원장

기준 main: `b5bd6b02c7ea8a5c6731871fa6e330ac6795fd36` · 현재 selection: `2026-10-29.representative4`

원문 편집 검토일: 2026-10-28 · 구현 상태 갱신일: 2026-10-29

이 문서는 개별 편집 triage와 현재 반영 기록을 결합한 결과입니다. 자동 생성 과정에서 법규를 재검증하거나 독립 감사 기록을 만들지 않습니다.

## 실제 반영 상태

| 상태 | 문항 수 |
|---|---:|
| REWRITTEN_NEW_ID | 62 |
| REUSED_EXISTING_QUALITY | 3 |
| HOLD_FROM_DEFAULT | 9 |
| NOT_YET_IMPLEMENTED | 281 |

기본 목록 439개에는 기존 고품질 96개가 유지됩니다. 별도 작성한 재작성 사례는 62개입니다. 원본의 제자리 수정·삭제 및 새 canonical 독립 감사는 각각 0개입니다.

대표 보류 항목과 관련 변형을 합쳐 원본 29개에 검토 경고가 연결됩니다. 이 수는 대표 355개 중 보류 수와 별개이며 전체 목록·Chaos에서 원본 접근을 없애지 않습니다.

## 최초 편집 판정 보존

| 최초 판정 | 문항 수 |
|---|---:|
| KEEP | 0 |
| MINOR_EDIT | 30 |
| MAJOR_REWRITE | 317 |
| REPLACE | 5 |
| HOLD_FOR_LEGAL_REVIEW | 3 |

원본 법규 상태는 355개 모두 **NOT_REVERIFIED**로 유지됩니다. 새 ID의 작성자 출처 확인과 원본·전체 corpus의 독립 법률 감사를 구별합니다.

- editorial_status는 원본을 읽은 편집자의 최초 판정이다. implementation_status는 현재 파일·selection으로 확인되는 반영 상태이며 서로 덮어쓰지 않는다.
- 원본 355개 모두의 legal_correctness는 기존 triage대로 NOT_REVERIFIED이다. 새 ID에 대한 작성자 출처 검토가 원본의 법규 재검증이나 독립 감사로 소급되지 않는다.
- REWRITTEN_NEW_ID는 별도 새 사례의 작성·반영을 뜻한다. REUSED_EXISTING_QUALITY는 이미 있는 96개 중 한 사례를 재사용한 것이며 신규 작성 수에 넣지 않는다.
- HOLD_FROM_DEFAULT는 기본 목록에서의 보류이다. 원본 파일·정답·기존 학습 기록을 삭제하거나 바꾸지 않는다.
- NOT_YET_IMPLEMENTED는 편집 검토만 완료된 범위이다. 355개 전부가 수정·교체 또는 법규 감사 완료되었다고 해석하면 안 된다.

## 문항별 원장

전체 선택지 분석·출처 관찰·기계적 신호와 기존 triage 원문은 [audit-ledger.json](audit-ledger.json)의 `editorial_triage`에 그대로 보존됩니다.

| 원본 ID | Family | 최초 판정 / 우선순위 | 실제 반영 | 대상 ID | 원본 법규 상태 | 개별 편집 발견사항 |
|---|---|---|---|---|---|---|
| MA-EXP-0003 | LIC01 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0001 | NOT_REVERIFIED | 졸업·18세·FPGEC·internship을 두 지원자에 흩어 놓고 정답 C는 사례 속 장애를 해결하지 않는 일반문장이다. A의 고용제안은 법규 혼동으로서 약하다. |
| MA-EXP-0007 | LIC02 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0002 | NOT_REVERIFIED | 금요일 합격 후 토요일 독립검수는 좋은 갈등이나 Case B와 A/B의 수수료 중복으로 핵심 결정이 희석된다. C는 intern 면허가 명시되지 않은 일반 조건문이다. |
| MA-EXP-0011 | LIC03 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0003 | NOT_REVERIFIED | disciplinary history가 제시되어도 standing 증빙에 어떤 문제가 생기는지 선택지에 적용하지 않는다. A/B는 사례 사실 없이 일반 목록으로 맞힐 수 있다. |
| MA-EXP-0015 | LIC04 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0004 | NOT_REVERIFIED | 4월6일이라는 날짜를 계산에 쓰지 않고 A~D 모두 옳다. 고용주 변경으로 시계를 재시작한다는 Case B는 약한 오개념이다. |
| MA-EXP-0019 | LIC05 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0005 | NOT_REVERIFIED | 개인·Drug Store·compounding 달력을 구분하는 목적은 좋으나 세 종류의 정확한 갱신행동 대신 일반 진위판단이다. A의 pharmacist birthday는 다른 직종 달력과 혼동을 만든다. |
| MA-EXP-0023 | LIC06 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0006 | NOT_REVERIFIED | 75일과 2년 초과의 실질 경로 차이를 보존할 가치가 있다. A/D의 every case는 과장된 절대문구이며, 두 사례를 한 상황의 복구 선택지로 좁힐 수 있다. |
| MA-EXP-0027 | LIC07 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0007 | NOT_REVERIFIED | 장기 징계복구와 현역복무 특례는 독립된 사건인데 한 SATA에 묶였다. A의 경력 중 언제든 복무하면 영구 CE 면제는 쉽게 배제된다. |
| MA-EXP-0031 | LIC08 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0008 | NOT_REVERIFIED | 은퇴 후 paid shift와 분실증 재발견은 서로 원인관계가 없고 모든 보기 정답이다. duplicate 반환은 유용하나 은퇴업무 판단에 기여하지 않는다. |
| MA-EXP-0035 | CE01 | MAJOR_REWRITE / P1 | REWRITTEN_NEW_ID | MA-RW-0009 | NOT_REVERIFIED | 40시간 몰아듣기와 carryover가 지문인데 유일 정답 A는 live law의 중복 category라는 제3의 내용이다. B의 고용주 점검일은 비법적 오답이다. |
| MA-EXP-0039 | CE02 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0010 | NOT_REVERIFIED | 3 live hours와 federal law course가 현실적이나 정답은 사례의 2시간 live 부족을 직접 해결하지 않는다. live/law overlap을 하나의 이수계획 결정으로 통합한다. |
| MA-EXP-0043 | CE03 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0011 | NOT_REVERIFIED | 10시간 하루 수강과 18 home-study/5 live는 실제 수치판단이 가능한데 선택지는 계산을 회피한다. C의 두 배 시간은 이미 CE01과 반복된다. |
| MA-EXP-0047 | CE04 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0012 | NOT_REVERIFIED | 10월12일 transfer가 유용한 결정조건인데 전부 정답이며 Case B가 같은 차이를 다시 설명한다. 기한연장과 졸업연도 면제의 차이를 구체적으로 적용해야 한다. |
| MA-EXP-0051 | CE05 | HOLD_FOR_LEGAL_REVIEW / P0_LEGAL_SOURCE_CONFLICT | HOLD_FROM_DEFAULT | — | NOT_REVERIFIED | CE 미충족 통지를 Board email로 단정하는 해설이 있다. 이번 세션의 ce-deficiency-source-conflict.json은 같은 개정 Policy의 Mandatory Disclosure Form 문구와 기존 노트의 email 사이 차이를 확인했고 현행 원본 binary 일치까지 해결하지 못했다. 일반 waiver 원칙과 별개로 잘못된 제출방법을 학습시킬 위험이 있다. 현재 보류 이유: 기존 통합노트 w1-a-7은 CE 미충족 통지를 2025-09-04 개정 Policy 2021-04의 email 안내로 정정했다고 기록한다. 그러나 이번 공식 URL의 Exa 전체 추출문과 공식 검색 excerpt는 Mandatory Disclosure Form을 명시하고, 검색 excerpt에는 동일 2025-09-04 개정 footer가 있다. 2026-05-12 reporting overview도 CE deficiencies를 20.03(4), 14 calendar days, Mandatory Disclosure Form으로 연결한다. 최신 직접 PDF 원본 또는 Board clarification 없이 어느 제출경로가 단독으로 충분한지 정답화하지 않는다. |
| MA-EXP-0055 | CE06 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0014 | NOT_REVERIFIED | 접종 직접감독과 복수 CDTM 분야가 서로 다른 추가/포함 CE 구조를 묻지만 한 의사결정으로 통합되지 않는다. 초기교육 문장은 해당 기록과 무관하다. |
| MA-EXP-0059 | CE07 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0015 | NOT_REVERIFIED | temporary final verification과 generic USP800 과정은 보존할 가치가 있는 예외 경계다. 서로 다른 직원 대신 한 약사의 실제 업무와 이수 course를 비교하면 판단이 분명해진다. |
| MA-EXP-0063 | CE08 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0016 | NOT_REVERIFIED | CPE Monitor 미등재 증빙과 반복강의 instructor credit은 별개이고 모든 선택지가 정답이다. A와 D는 보존의무를 반복한다. |
| MA-EXP-0067 | PER01 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0017 | NOT_REVERIFIED | state license 없이 시작한다는 Case A와 임의 intern 직함 Case B는 둘 다 employer가 면허를 만들지 못한다는 경로다. A의 final validation까지 추가해 세 가지 업무를 섞는다. |
| MA-EXP-0071 | PER02 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0018 | NOT_REVERIFIED | rotation 시작 전 면허와 졸업후1500시간 재이수,14시간 credit,타주증빙을 한 문항에 나열한다. 14시간 선택지 해설은 credit만 다뤄 근무시간 제한과 혼동 가능성을 남긴다. |
| MA-EXP-0075 | PER03 | MAJOR_REWRITE / P2 | REUSED_EXISTING_QUALITY | MA-REV-0009 | NOT_REVERIFIED | 타주 licensed resident의 MA 권한과 PharmD withdrawal 통지는 서로 다른 대상이다. A의 Pharmacist 명찰은 명백하고 C/D는 같은 졸업후권한 결론을 반복한다. |
| MA-EXP-0079 | PER04 | MAJOR_REWRITE / P1 | REWRITTEN_NEW_ID | MA-RW-0020 | NOT_REVERIFIED | 50문항75% employer 시험은 구체적이지만 D의 MPJE raw score는 지문과 무관한 정답이고 모든 보기가 맞는다. |
| MA-EXP-0083 | PER05 | MAJOR_REWRITE / P1 | REWRITTEN_NEW_ID | MA-RW-0021 | NOT_REVERIFIED | 16세 신입과 성인 trainee 기간이 함께 나오며 유일 정답은 단순 나이 암기다. 실제 1년한도 사건을 해결하는 행동선택으로 전환할 필요가 있다. |
| MA-EXP-0087 | PER06 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0022 | NOT_REVERIFIED | 전화 refill과 dose clarification은 동일 직원 배치로 연결할 수 있다. D의 상담 제공은 사례 밖 제3업무이며 C의 임상판단 위임은 너무 노골적이다. |
| MA-EXP-0091 | PER07 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0023 | NOT_REVERIFIED | 유효 state license와 national lapse의 차이는 실질적이다. A의 자동 revoked는 쉬운 오답이고 B는 정확한 보고대상·기한 없이 specified duty로 회피한다. |
| MA-EXP-0095 | PER08 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0024 | NOT_REVERIFIED | birthday cycle과 만료후 대기는 유용하지만 전부정답이고 D의 2년초과는 제시된 경과와 연결되지 않는다. |
| MA-EXP-0099 | PER09 | MAJOR_REWRITE / P2 | REUSED_EXISTING_QUALITY | MA-REV-0006 | NOT_REVERIFIED | unchanged ScheduleIV와 dose change라는 실제 경계는 보존한다. A의 trainee checklist가 지문 밖이고 유일 정답은 행위 판단보다 schedule 범위 암기다. |
| MA-EXP-0103 | PER10 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0050 | NOT_REVERIFIED | new CIII 수신과 emergency CII의 pharmacist 경계를 다루지만 모든 해당 주법 예외를 item에서 재검증하지 않았다. C의 임상수정 일반문장은 사례 밖이고 A는 이중자격만 반복한다. |
| MA-EXP-0107 | PER11 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0051 | NOT_REVERIFIED | VI와 IV transfer 비교는 실제 행동이 바뀌는 유용한 차이다. B의 새 유효기간과 D의 urgency는 지문에 없는 부가명제다. |
| MA-EXP-0111 | PER12 | MAJOR_REWRITE / P2 | REUSED_EXISTING_QUALITY | MA-REV-0008 | NOT_REVERIFIED | barcode 최종검수와 intern상담·interaction 처리의 다양한 역할을 모두 정답 명제로 나열했다. 실제 pharmacist의 업무 재배치 결정이 없다. |
| MA-EXP-0115 | PER13 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0053 | NOT_REVERIFIED | 완료된 bag 운반과 unprepared stock handling이라는 구별이 좋다. A/B/D가 all/unrestricted 같은 과장으로 틀려 유일 정답 C를 문구만으로 고르기 쉽다. |
| MA-EXP-0119 | PER14 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0054 | NOT_REVERIFIED | 두 CPhT count 이후 discrepancy adjustment는 실제 흐름이다. B의 unlicensed vendor만 entry 가능이라는 오답은 해당 규칙을 몰라도 쉽게 배제된다. |
| MA-EXP-0123 | PER15 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0061 | NOT_REVERIFIED | intern을 ordinary로 교체하면 적격조합이 바뀌어 유용한 판단이다. B의 scope 일반론은 이 staffing 결정과 무관한 정답을 추가한다. |
| MA-EXP-0127 | PER16 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0062 | NOT_REVERIFIED | 3 ordinary에서 intern으로 교체하는 핵심은 좋지만 C의 만료 certification은 사례에 없고 네 보기가 전부정답이다. 1:4와 숫자만 바꾸지 말고 실제 배치결정이 달라져야 한다. |
| MA-EXP-0131 | PER17 | MAJOR_REWRITE / P1 | HOLD_FROM_DEFAULT | — | NOT_REVERIFIED | 6명 배치에서 세 번째 intern이 qualifying group에 들 수 있는지 실질 경계가 있다. 정답 B는 실제 staffing 승인 대신 별도제한 확인이라는 추상문장이고 D의 미래 certification은 쉽다. 현재 보류 이유: 현행 Board Policy 2026-02 I.B는 vaccination services를 제공하는 약국에 자격 구성 조건을 갖춘 최대 1 pharmacist : 6 support personnel 경로를 명시한다. 한편 열람한 247 CMR 8.06(3)(a)는 일반적인 최대4명·3명 경로를 규정한다. 이번 작성자 검토에서는 일반적인 6명 허용에 관해 두 자료의 적용 관계를 확립하는 공식 rulemaking, waiver 또는 이에 준하는 설명을 확보하지 못했다. 따라서 제한 없는 허용을 확정 정답으로 삼는 새 문항 작성은 보류한다. 이는 출처 간 적용 관계가 미해결되었다는 뜻이며, Board 정책이 무효라거나 기존 모든 정답이 잘못되었다는 판정이 아니다. |
| MA-EXP-0135 | PER18 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0064 | NOT_REVERIFIED | 검수된 package 운반과 cashier의 stock selection 차이는 유용하다. C/D는 조건부 제외를 반복하며 B의 게시요건 전면제거는 인위적이다. |
| MA-EXP-0139 | PER19 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0065 | NOT_REVERIFIED | present substitute pharmacist가 실제 해결책이지만 C의4인 clinic과 A의remote-processing은 다른 경로를 끌어온다. |
| MA-EXP-0143 | PER20 | MAJOR_REWRITE / P2 | HOLD_FROM_DEFAULT | — | NOT_REVERIFIED | exclusive clinic에서 retail filling으로 활동이 바뀌는 유용한 조건변화다. 모든 보기가 맞고 non-pharmacy consultation 예외까지 추가돼 판단범위가 넓어진다. 현재 보류 이유: Policy 2026-02 II.A/B describes limited four-intern paths while 247 CMR 8.01(16) states a two-intern cap. Official texts were re-read but their application relationship remains unresolved. This is not a policy-invalidity or universal-waiver finding; no unchanged key is adjudicated wrong merely from the source relationship. |
| MA-EXP-0147 | PER21 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0067 | NOT_REVERIFIED | 기존 CPhT를 dedicated trainee로 배치하면 category가 달라지는 의미 있는 예외다. B의독립작업과 D의사후지정은 쉽게 틀리고 사례와 별개다. |
| MA-EXP-0151 | PER22 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0068 | NOT_REVERIFIED | computer module 전용 제외와 외부 vendor 보안접근은 독립된 업무다. 둘을 묶어 감독규칙을 목록처럼 읽게 한다. |
| MA-EXP-0155 | MOR01 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0055 | NOT_REVERIFIED | 새 storefront의 VI dispensing은 적절한 시설허가 결정이나 A의 institutional license 정의는 지문 밖이다. 약물 schedule과 compounding 활동도 실제 신청서로 묶어야 한다. |
| MA-EXP-0159 | MOR02 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0056 | NOT_REVERIFIED | 늦은 개업과 사업매매는 별개 사건인데 전부 옳은 명제를 묶었다. B는 오해방지 설명 자체가 정답으로 노출된다. |
| MA-EXP-0163 | MOR03 | MAJOR_REWRITE / P1 | REWRITTEN_NEW_ID | MA-RW-0057 | NOT_REVERIFIED | 8개월 good standing과3년 inspection은 판단자료지만 유일 정답 A는 지문에 제시되지 않은 PIC 동일인 여부다. |
| MA-EXP-0167 | MOR04 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0058 | NOT_REVERIFIED | 두 약국30시간 분할과 근무약사 security 책임은 실제 운영갈등이다. B의관리업무목록은 중심결정을 흐린다. inherited OPEN은30/100일 및사임통지 경계이며 이 문항의30시간/동시MOR 명제를 직접 문제삼지는 않는다. |
| MA-EXP-0171 | MOR05 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0059 | NOT_REVERIFIED | 중병으로 outgoing 서명이 불가능하다는 조건은 대체서명 경로를 바꾼다. C의즉시폐기는 약한 오답이고 D의application 서명은 별도 행정문장이다. inherited OPEN의통지기한은 이 key가 시험하지 않는다. |
| MA-EXP-0175 | MOR06 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0060 | NOT_REVERIFIED | 소유권매매의 사전14일과 명칭변경의사후14일이 실제 다른 trigger이나 모두 정답이다. B의재고/환자파일 일반론은 날짜결정과 분리된다. |
| MA-EXP-0179 | MOR07 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 신청과 approval을 구별하는 목표는 좋지만 두 공사를 한꺼번에 묻고 A의sterile control은 사례에 없다. |
| MA-EXP-0183 | MOR08 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 90일 fills로 환자대상을 정하는 실제 운영맥락은 적절하다. D의모든시설 동일 적용은 극단적이며 A의transfer 시점은 별도 일반론이다. |
| MA-EXP-0187 | MOR09 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 도착 몇주후 추정재고와 잔여재고 유지라는 잘못된 계획을 고치게 하는 것은 의미 있다. 한 계획표로 합치고 날짜별재고·10일제출·2년보존을 비교해야 한다. |
| MA-EXP-0191 | MOR10 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 30분/6시간 meal break와12시간근무후8시간휴식은 다른 시계인데 D를 일반명제로 추가했고 모두 정답이다. unreviewed final verification은 쉬운 금지행위다. |
| MA-EXP-0195 | DISC01 | REPLACE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 약국법규 review group의명단퀴즈이며 pharmacist가 수행할 환자·운영 결정이 없다. all13 pharmacist와선거라는 극단오답이 정답을 드러낸다. |
| MA-EXP-0199 | DISC02 | REPLACE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 연속임기와회원경력요건을 두 사람의지식문제로 묶고 D holdover는 지문사실과 무관하다. 다른 대표에서 부족한 실무판단에 기본목록 자리를 배정하는 편이 낫다. |
| MA-EXP-0203 | DISC03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 최근 자체점검이 Board접근을 대체한다는 갈등은 실제적이나 D immunity는 노골적이다. MOR변경7일과기록2년은 별도사례에 나열된다. |
| MA-EXP-0207 | DISC04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | initial21일과반환후7일을 비교할 수 있는데 전부정답이며 날짜계산은 없다. 책임자없는 vague promise는 너무 쉽게 결함으로 보인다. |
| MA-EXP-0211 | DISC05 | REPLACE / P1 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 두 사례는 unsafe practice와치료사실인데 유일 정답 D는 conviction 정의다. key를 찾기 위해 지문을 읽을 필요가 없는 명백한 내용불일치다. |
| MA-EXP-0215 | DISC06 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | credentialing form 작성이라는 실제결정이 있으나 consent agreement 제한내용을 제시하지 않아 일반진위로 남는다. probation 영구취소는 과장오답이다. |
| MA-EXP-0219 | DISC07 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | summary7일과cease/quarantine15businessdays의경로 차이는 유용하다. threat문구의요건은 exact조문 재대조가 필요하고 A의optional 준수는 약하다. |
| MA-EXP-0223 | DISC08 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | cost-only pending과federal waiver의독립성은 연결할 수 있으나 모두정답이고5주년만료는 지문에사실이 없다. |
| MA-EXP-0227 | CDTM01 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0025 | NOT_REVERIFIED | naloxone standing order와OTC피임약이모두무제한처방권으로 확장된다는 과장 사례다. 유일정답 C는적격CDTM일반요건이며 실제환자행동을 정하지 않는다. |
| MA-EXP-0231 | CDTM02 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0026 | NOT_REVERIFIED | 무MA면허와비적격보험이라는서로다른자격결함은실제채용검토로통합가능하다. 미래직장 B는지문밖이며occurrence당보장액이보기보다해설에만있다. |
| MA-EXP-0235 | CDTM03 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0027 | NOT_REVERIFIED | 2026신규CPA에2017grandfather를적용하려는오해는구체적이다. B의모든회사경력과C의Boardequivalency일반론은심화판단을약화한다. |
| MA-EXP-0239 | CDTM04 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0028 | NOT_REVERIFIED | PGY1후추가경험과supervisedmonitoring은의미있는요건이나전부정답이고BPS의대체경로가별도상황없이추가됐다. |
| MA-EXP-0243 | CDTM05 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0029 | NOT_REVERIFIED | 20시간만이수한실제부족과paintraining을결합할수있다. B의모든요건제거,D의즉시증빙폐기는명백한오답이다. |
| MA-EXP-0247 | CDTM06 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0030 | NOT_REVERIFIED | 등록과MassHealthattestation은서로다른시작요건이며D의Board/physician통지는제3주제다. B의retailCII-V는다른대표에서직접다룬다. |
| MA-EXP-0251 | CDTM07 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0031 | NOT_REVERIFIED | 새practice site라는승인trigger는좋지만hospital/LTC승인권자차이를보기에서이름없이specified로회피한다. |
| MA-EXP-0255 | CDTM08 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0032 | NOT_REVERIFIED | 17세와미기재diagnosis가서로다른등록장벽인데모두정답이다. B의별도minorstatute는지문밖의교과서대조다. |
| MA-EXP-0259 | CDTM09 | MAJOR_REWRITE / P1 | REWRITTEN_NEW_ID | MA-RW-0033 | NOT_REVERIFIED | consent전달과처방변경의24시간은유용한서로다른trigger다. B의환자사본을거절해야완료라는오답은비현실적이고유일정답A는보관위치일반론이다. |
| MA-EXP-0263 | CDTM10 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0034 | NOT_REVERIFIED | establishedtherapyextension과일반응급연속조제의경계는보존한다. A/C의unlimited/everypatient가정답을드러내고두번30일의실제계산은없다. |
| MA-EXP-0267 | CDTM11 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0035 | NOT_REVERIFIED | hypertensionCPA와무제한HIVinitiation은자연스럽게연결되지않는다. B/D가같은agreement범위를되풀이하며C는진단권한을노골적으로넘긴다. |
| MA-EXP-0271 | CDTM12 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0036 | NOT_REVERIFIED | testosteroneCIII는opioid여부와schedule을구분하는좋은약물맥락이다. 별개VI/PMP환자를묶고네보기를모두정답으로만들었다. |
| MA-EXP-0275 | CDTM13 | MAJOR_REWRITE / P1 | REWRITTEN_NEW_ID | MA-RW-0037 | NOT_REVERIFIED | 월간batch와급한안전사건이지문인데유일정답D는CPA정보교환조항이다. 기다려야한다는B는명백하며urgentaction을직접고르지않는다. |
| MA-EXP-0279 | CDTM14 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0038 | NOT_REVERIFIED | 서명된빈agreement와technician독립치료권부여는둘다과장돼쉽다. B의neverrenew도문구단서다. |
| MA-EXP-0283 | CDTM15 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0039 | NOT_REVERIFIED | nonrenewal환자의continuation계획과inspection시copy보관은각기실제업무이나한상황의결정은아니다. B의immediateabandonment가유일약한오답이다. |
| MA-EXP-0287 | CDTM16 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0040 | NOT_REVERIFIED | 같은physician고용이라도목적이달라지는의미있는대조다. C/D가A를추상적으로되풀이하고모두정답이라보기비교가없다. |
| MA-EXP-0291 | VAX01 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0041 | NOT_REVERIFIED | trainee와 full technician을 구별하는 실제 배치결정은 좋다. A/B는 독립 임상권한이라는 추가 과장오답이고 둘째 직원의 자격은 구체화되지 않는다. |
| MA-EXP-0295 | VAX02 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0042 | NOT_REVERIFIED | 4세와 제품허가연령 미달의5세는 다른 장애이므로 보존할 대조다. A는 별도 federal 경로 확인이라는 추상정답이고 D는 dose까지 나이로 결정하는 극단오답이다. |
| MA-EXP-0299 | VAX03 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0043 | NOT_REVERIFIED | current recommendation의 실제 제품·대상·문구가 전혀 없어 근거를 적용할 수 없다. personal preference를 Commissioner 권고라 부르는 Case B는 비현실적이다. |
| MA-EXP-0303 | VAX04 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0044 | NOT_REVERIFIED | 20시간 selfstudy만 있는 intern과 CPR만료 pharmacist는 별개 결함이고 전부정답이다. 실제 course구성 판정을 하나의 자격검토로 집중할 수 있다. |
| MA-EXP-0307 | VAX05 | MAJOR_REWRITE / P1 | REWRITTEN_NEW_ID | MA-RW-0045 | NOT_REVERIFIED | annual/biennial 차이가 지문인데 유일정답C는 ACPE approval이다. D의permanently와B의CE로감독대체는 쉽게 배제된다. |
| MA-EXP-0311 | VAX06 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0046 | NOT_REVERIFIED | 600 trainee시간과0 postlicensure시간의 차이가 중요한 결정조건이다. B/D는 같은 자격경로를 반복하고 C의면허없는접종은 다른 대표의 쉬운오답이다. |
| MA-EXP-0315 | VAX07 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0047 | NOT_REVERIFIED | 6시간 course와별도2시간 OJT의 구분은 실질적이다. 두번째직원의 unsupervisedpractice는 명백히 틀려 실제 기록비교로 개선할 수 있다. |
| MA-EXP-0319 | VAX08 | MAJOR_REWRITE / P2 | REWRITTEN_NEW_ID | MA-RW-0048 | NOT_REVERIFIED | vaccine order만 있는 실제 준비결함이 좋으나 unsignedtemplate까지 추가하고 모든보기를맞게했다. 응급약 확보와행동결정이 직접 없다. |
| MA-EXP-0323 | VAX09 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | VIS 사후제공과 allergy미확인은 실제 실수다. 유일정답A는 추상적screening이고 B/C/D가 의무전면생략으로 틀려 쉽게 맞힌다. |
| MA-EXP-0327 | VAX10 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | influenza의조회예외와투여보고는 좋은 구별이나 A/D가 같은 결론이고 B의COVID권고는 지문밖이다. |
| MA-EXP-0331 | VAX11 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Monday10시에서Friday10시의96시간은 실제적이다. D의unnamed newborn은 pharmacy사례에불필요해 pattern상 세정답을 채운다. |
| MA-EXP-0335 | VAX12 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | inter-site sharing반대와Department보고는 중요한 경계다. 이웃호기심조회는 별도 명백한 위반이고 A/B는 같은 구별을 반복하며 모두정답이다. |
| MA-EXP-0339 | VAX13 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 무료stock미사용시 비용정보와wellchildcare counseling이 실무적이지만 D의PCP통지가MIIS대체라는별개오답이끼어든다. |
| MA-EXP-0343 | VAX14 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | reportableevent에인과관계확정이필요한지 묻는핵심은좋다. 표의실제event·interval을주지않고 해당한다고결론을미리제공한다. |
| MA-EXP-0347 | VAX15 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | predraw2시간과temperatureexcursion은별개법적결정이다. D의정상외관만으로사용은너무쉽고A는시설권한일반론이다. |
| MA-EXP-0351 | VAX16 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | technician의LAI와17세IV는세가지부적격사유를한꺼번에던진다. 모두정답이며 단일조건 변화로행동이바뀌는비교가없다. |
| MA-EXP-0355 | VAX17 | MAJOR_REWRITE / P1 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 제품별훈련이목적인데유일정답C는CPR이고지문에는CPR상태가없다. internallychosenCE를법으로부른다는CaseB는편집자설명에가깝다. |
| MA-EXP-0359 | VAX18 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 권고notation과quarterly예시의강제성차이는가치있다. A의consent상담대체는별도사건이며 두사례를하나의처방유효성결정으로정리할수있다. |
| MA-EXP-0363 | VAX19 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 투여자·일시·site누락은실제기록결함이다. 대기실diagnosis공개는관련없는쉬운privacy위반이며 A만잘못되고나머지가일반명제다. |
| MA-EXP-0367 | VAX20 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | ED monitoring을serious분류에적용하는조건은유용하다. 모두정답이고C의응급치료지연금지는상식으로맞힐수있다. |
| MA-EXP-0371 | PUB01 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 다른약국으로보내면singlelocation전제가바뀌는좋은경계다. A의receipt로상담대체,D의NPI교육면제는어색한오답이다. |
| MA-EXP-0375 | PUB02 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | encouraged와CDTMattestation의차이는보존가능하나B는referral일반론,C는genericnote라는약한오답이다. |
| MA-EXP-0379 | PUB03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Opill과EC,ulipristal과levonorgestrel은제품구분에의미가있다. mifepristone을EC대체라하는유일오답은너무멀며B의보험도별도내용이다. |
| MA-EXP-0383 | PUB04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 대리인의standingorder요청은본인assessment조건을바꾸는실제상황이다. 교육필수착각을별도case로넣고모두정답으로만들었다. |
| MA-EXP-0387 | PUB05 | MAJOR_REWRITE / P1 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | minor EC와 naloxone의보고기한복사는독립된사건이다. 유일정답C는다른모든minor의료행위로확장하지말라는지문밖일반론이다. |
| MA-EXP-0391 | PUB06 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 보험benefit와처방권한의차이는중요하지만보험plan조건을주지않아A는추상정답이다. OTC보험청구와처방scope를하나의구매사건에연결할수있다. |
| MA-EXP-0395 | PUB07 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | naloxone제3자구매와naltrexone대체제안은서로다른결정이고A의buprenorphine혼합제는또다른약물이다. |
| MA-EXP-0399 | PUB08 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 이전거절이이번offer를없애는지의미있는사례다. 보험수량제한을별도case로넣고모든보기가옳아행동대안이없다. |
| MA-EXP-0403 | PUB09 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | daily제출을안한약국의annualroute와dose단위는실무적이다. A의patientvisibleprofile은다른명제이고실제dose수를계산할자료가없다. |
| MA-EXP-0407 | PUB10 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 전화만가능한pharmacist라는조건은현장존재판단을바꾼다. unsecurednetwork·volunteer접근·confidentiality면제까지과장된여러결함을겹친다. |
| MA-EXP-0411 | PUB11 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | originalpatient처방으로여러partner를공급하려는것은실제구별이다. C의EPT와독립STI처방동일시는쉽고A/D는경로정의를반복한다. |
| MA-EXP-0415 | PUB12 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | unnamedEPT예외와unavailablepharmacyreferral은실질적이지만모두정답이다. A의신원정보날조금지는정답문구단서가된다. |
| MA-EXP-0419 | COUN01 | REPLACE / P1 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | cashieroffer·supervisedintern상담·technician임상판단은PER12와같은역할구별을다시묻는다. 유일정답C는offer/response기록구분으로사례의업무배치를해결하지않는다. |
| MA-EXP-0423 | COUN02 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 서두르는환자를거절로간주하는실수는현실적이다. A의서명screen은사례밖이며B의refusal을completed로기록하라는오답은너무명백하다. |
| MA-EXP-0427 | COUN03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 작은글자와inhaler기술·언어청각장벽은좋은환자조건이나서로다른두환자를묶었다. C의identicalcontent는극단적오답이다. |
| MA-EXP-0431 | COUN04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | measuringdevice제공과prescriber의도변경은관계가약한두사례이고모두정답이다. A/B/D는측정과사용설명의유사명제를반복한다. |
| MA-EXP-0435 | COUN05 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | stockroom을통과해야하는상담공간은구체적이다. A의모든hospital면제와B의상담전면불가는쉬운부가오답이다. |
| MA-EXP-0439 | COUN06 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 8×10표지와서로다른글자크기는숫자구별로만남는다. 실제최소dimension을직접묻거나환자접근결정과연결하고D의표지로offer대체는빼야한다. |
| MA-EXP-0443 | COUN07 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | documentedallergy와무alert의충돌은좋은전문판단이다. 둘째환자의평가되지않은alert까지섞고B는everyalert자동금지로과장한다. |
| MA-EXP-0447 | COUN08 | REPLACE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | barcode와MassPAT가DUR를대체하지않는다는추상구별을alltrue로반복한다. COUN07의allergy검토와PER12의최종검수에새로운법적허용경로를더하지않는다. |
| MA-EXP-0451 | COUN09 | MAJOR_REWRITE / P1 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | blankallergy라는실제정보결함이유용한데유일정답B는별개REMS기록이다. A/D는관련정보삭제·미검토라는명백오답이다. |
| MA-EXP-0455 | COUN10 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | genericCMI와FDAguide의구별은명확하나실제제품이없고A의VIS는제3문서다. REMS추정과환자정보교부를한제품에묶어야한다. |
| MA-EXP-0459 | COUN11 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | community매package와LTCF최초/30일은setting이행동을바꾸는대조다. A의refillvalidity는지문과무관하다. |
| MA-EXP-0463 | COUN12 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | cashpay환자에게주상담의무가남는지좋은관할구별이다. mailserviceleaflet은별도사례이고모두정답이며B/D가추상명제다. |
| MA-EXP-0467 | PRIV01 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 종이label폐기와들리는diagnosis는실제PHI매체사례이나A/C가같은전자만보호오해를반복하고D의모든약국정보공개는극단적이다. |
| MA-EXP-0471 | PRIV02 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | billingvendor와treatingclinician은BA여부가달라지는좋은관계대조다. C/D의계약이모든금지를없애거나명칭만으로제외라는오답을현실화해야한다. |
| MA-EXP-0475 | PRIV03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 처방확인전화와친구기록호기심조회는다른목적이다. B의login으로treatment전환은노골적이며A/C는허용범위일반론이다. |
| MA-EXP-0479 | PRIV04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | provider간treatment예외와내부workforceaccess는법적적용이달라독립경로가있다. 모두정답이고B/C는주의문구를다시읽는형식이다. |
| MA-EXP-0483 | PRIV05 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | promoter가주는돈과보험payment를구분하는실질문제는있다. A/C/D는사후authorization·모든홍보동의·이름만바꾸기라는극단오답이다. |
| MA-EXP-0487 | PRIV06 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 환자동의로pickup하는가족에게약설명을주는범위는실제업무다. D의allunrelatedrecords와A의broadwrittenauthorization은양극단이다. |
| MA-EXP-0491 | PRIV07 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 구체적minorservice나동의조문을명시하지않아실제personalrepresentative예외를적용할수없다. B의모든치료무제한동의가유일오답이다. |
| MA-EXP-0495 | PRIV08 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | CaseB가올바른분리방법을이미설명하고B/C가같은구별을반복하며모두정답이다. 환자access/amendment는추가일반론이다. |
| MA-EXP-0499 | PRIV09 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | vendor전달12일지연과extension사전서면통지는좋은clock사례다. A의계속연장과D의businessdays는법정혼동으로그럴듯하나두사건을한일정으로통합해야한다. |
| MA-EXP-0503 | PRIV10 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 2년Rx와6년HIPAA문서의분리는유용하나A의audittrail은관련없는고의은폐다. B/C가보존중첩을반복한다. |
| MA-EXP-0507 | PRIV11 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | wrongbag회수는실제breachriskfact다. 누가무엇을봤는지가없어결론이아닌review하라는답만가능하고C의undocumentedassurance는쉽다. |
| MA-EXP-0511 | PRIV12 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 20명breach의개인통지와annualHHSclock는실제다르다. A/D는같은분리를반복하고모두정답이다. |
| MA-EXP-0515 | PRIV13 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 500/501경계는수신기관에따라행동이바뀌는유효한대조다. B의501이500보다크지않다는문장은산술로즉시틀리므로법규distractor가아니다. |
| MA-EXP-0519 | PRIV14 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | buprenorphine약명만으로Part2를판단할수없다는것은중요하나프로그램과자료출처가실제명시되지않는다. B/C는현행경로를전면부정한다. |
| MA-EXP-0523 | PRIV15 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | password만으로모든보호완료라는과장과가상의proposedrule을묶었다. actualproposal을지정하지않아시행여부판단을할수없다. |
| MA-EXP-0527 | PRIV16 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | outage와로그삭제라는별개사건을모두정답상식으로나열했다. 어떤다운타임기록이복구시중복조제를방지하는지구체화할필요가있다. |
| MA-EXP-0531 | RET01 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 약국통제아래미교부와원stockbottle반환의차이는좋다. 유일정답B는분류만말하고실제허용container를고르지않는다. |
| MA-EXP-0535 | RET02 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 잘못교부한약을받아야하지만재판매할수없다는두행동의분리는좋다. C의proveninjury까지기다림은명백오답이다. |
| MA-EXP-0539 | RET03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 정상약불필요반환과DEAcollector등록은다른제도다. B/C가다른대표의반환수령/재고금지를반복한다. |
| MA-EXP-0543 | RET04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 같은환자pack에서중단약제거후재교부는다른return과구별되는유용한경로다. 전부정답이고records와labels가교과서목록이다. |
| MA-EXP-0547 | RET05 | MAJOR_REWRITE / P1 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 12일원expiry는판단자료인데유일정답B는therapychange시내용/지시확인일반론이다. removablecelllabel은별도결함이다. |
| MA-EXP-0551 | RET06 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | recalllot불명확과반송coldchain은각각실제품질판단이다. D의carrier가모든책임은과장이고C의custody분류는추상적이다. |
| MA-EXP-0555 | RET07 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | sealedliner를열어count하거나stock회수하는두사례는같은처분금지를반복한다. D의mailback은지문밖이다. |
| MA-EXP-0559 | RET08 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 두3businessday시계는trigger가달라독립된판단이다. 지문에날짜가없고모두정답이며C의인력조합은구체적으로묻지않는다. |
| MA-EXP-0563 | RX01 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | checkdigit통과후실제등록확인은좋은검증문제다. doctor직함·hospitalbadge만으로무제한처방이라는오답은현실성이낮다. |
| MA-EXP-0567 | RX02 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 자료가treatmentpurpose를반박한다고만쓰고그자료를제시하지않아실제redflag판단을못한다. unusualfeature도특정되지않는다. |
| MA-EXP-0571 | RX03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | patient명목으로office재고를공급하려는구별은실질적이다. C의특수deliveryexception은정확한제품·경로없이추상정답으로추가됐다. |
| MA-EXP-0575 | RX04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | issue날짜와nosubsignature는별개필수요소이고D의EPT/naloxone예외까지확장돼모두정답목록이됐다. |
| MA-EXP-0579 | RX05 | MAJOR_REWRITE / P1 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | paper scan과text사진은전송수단과적법한EPCS발행의차이다. 유일정답C는permittedcorrections기록으로지문이묻는형식결함과무관하다. |
| MA-EXP-0583 | RX06 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | powerfailurepaper와oralCIIrefill은다른법적요건을강조하지만refill자체가너무명백한금지다. A의과거LTCF기한은특정날짜없이삽입됐다. |
| MA-EXP-0587 | RX07 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 환자바꾸기와서명대필은극단적이고D의generic대체는별도주제다. earliestfill을당기는현실적요청에집중할수있다. |
| MA-EXP-0591 | RX08 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | agent주소확인과CIIstrength변경은실제권한차이다. gabapentinVI조정은다른경로인데alltrue로묶어분기를흐린다. |
| MA-EXP-0595 | CII01 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | oxycodone2refills와partial의구별은기본적이지만A의EPCS최종검수면제는멀고C/D도같은no-refill을반복한다. |
| MA-EXP-0599 | CII02 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 90daysupply허용과issue후40일firstfill은행동이바뀌는구체적사례다. CaseB와C가같은오해를되풀이한다. |
| MA-EXP-0603 | CII03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | methylphenidate와testosterone은category를적용할수있는제품이다. 정확한quantity결정없이현재category라말하며B/D는남은조건일반론이다. |
| MA-EXP-0607 | CII04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | state90일과federalmethadoneOUD권한의충돌은중요하다. A의implantablepumpBUD가사례밖이고전부정답이다. |
| MA-EXP-0611 | CII05 | MAJOR_REWRITE / P1 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 60일뒤earliestfill과MAvalidity의충돌은실질적이다. 유일정답C는federal일반조건이라주사례를해결하는행동을직접묻지않는다. |
| MA-EXP-0615 | CII06 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | outage와즉시치료필요는별도이며적절한대체가있는조건은유용하다. C의고정7일분과D의refill전환은쉬운오답이다. |
| MA-EXP-0619 | CII07 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | receptionist→CPhT와centralfill수신은서로다른제한이다. C의unknowncaller주장만으로인증불필요는명백오답이다. |
| MA-EXP-0623 | CII08 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Mondayauthorization와Tuesdaydispense의시계차이는유효하다. alltrue이므로실제후속통지행동의선택지가없고주법통합을명시적으로유보한범위를유지해야한다. |
| MA-EXP-0627 | CII09 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | LTCF는CII전반,hospice특례는narcotic이라는조건차이가가치있다. A의모든요건제거와C의막연comfortcare는쉽다. |
| MA-EXP-0631 | CII10 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | qualifyinginfusion조건을지문에서이미충족한다고말해실제route를분류하지않는다. A의oraltablet,D의refill은너무먼오답이다. |
| MA-EXP-0635 | PART01 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Monday14시→Thursday12시의70시간과80시간은의미있는경계다. A/D는같은trigger를반복해두사례와네명제의부피가과하다. |
| MA-EXP-0639 | PART02 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 사후request날조라는극단행동을모두정답명제로반박한다. 실제request가있었는지모호한현실적기록검토가더좋다. |
| MA-EXP-0643 | PART03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | day20request와casualagent의확대요청은각각유용하나자격있는requester및prescriber량을실제로명시하지않는다. |
| MA-EXP-0647 | PART04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | emergency72시간과samechain다른약국은서로다른장벽이다. C/D는경로구별일반론이며실제remainder제공여부를묻지않는다. |
| MA-EXP-0651 | PART05 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | day8미시작과적법초기partial후잔량은다른상태여서보존할가치가있다. inheritedOPEN은redactedcopy제출채널이며이문항의initial/remainder시계와직접겹치지않는다. |
| MA-EXP-0655 | PART06 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | narcotic여부와MAcounterpickup은행동을바꾸는실질적차이다. 모두정답이고Maine포함을단순목록암기로추가한다. redactedcopyOPEN은별도보존한다. |
| MA-EXP-0659 | REF01 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 2authorizedrefill을5로늘리려는사례는좋다. D는C의반대를단순반복하고ScheduleV주법차이는다른case로끼어든다. |
| MA-EXP-0663 | REF02 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 늦은firstfill과transfer가원issueclock를재시작하지않는다는같은결정을반복한다. A의PRN은지문밖이다. |
| MA-EXP-0667 | REF03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | addedauthorization기록과partial거래수는서로다르다. D의CII72시간은제3경로를끼워넣어명제집합이된다. |
| MA-EXP-0671 | REF04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | independent약국의두번째transfer와logo만같은chain은좋은database예외검토다. B/C는다른transfer대표와동일일반론이고alltrue다. |
| MA-EXP-0675 | REF05 | MAJOR_REWRITE / P1 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 양약국에서동일잔량활성화하는실제위험을제시했으나유일정답B는양쪽보존책임일반론이다. 보존trigger도실제날짜가없다. |
| MA-EXP-0679 | REF06 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 처음미조제EPCS를print/fax하면서내용변경하는결함이명확하다. A의III-Vrefill과D의미래lastrefill은CII사례에직접대응하지않는다. |
| MA-EXP-0683 | REF07 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | paperIII와paperVI가서로다른transfer권한에들어가는좋은대조다. B의인력scope와C의validity일반론이중심형식결정을흐린다. |
| MA-EXP-0687 | REF08 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | fee조건과1년초과는각기transfer장벽이다. 모두정답이고patientagent는추가명제다. inheritedOPEN은VIcontinuation14/30일로이transferkey와직접관련없다. |
| MA-EXP-0691 | PMP01 | MAJOR_REWRITE / P1 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | query·pharmacyupload·개인access는서로다르지만유일정답B는조회목적일반론으로주어진account결함을해결하지않는다. |
| MA-EXP-0695 | PMP02 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | opioidquery와gabapentinreporting은약물목록의목적이달라유용하다. A/D는원칙만말하며정확한prescribing행동시점이없다. |
| MA-EXP-0699 | PMP03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | gabapentinVI가reportable이라는차이는실제적이나B의outstate약국은지문밖이다. 준비일과교부일을구체적시각으로묻지않는다. |
| MA-EXP-0703 | PMP04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 무거래파일과업로드성공/record거절은현실적오류다. 모두정답이며C의waiver는명시적으로없는상황에새예외를추가한다. |
| MA-EXP-0707 | PMP05 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 실제pickupagent의ID를기록하는판단은구체적이다. A의untrackeddelivery와B의gabapentin은별도주제이고SSN선호는너무명백하다. |
| MA-EXP-0711 | PMP06 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | reasonablehardship과대체name/address/signature는실질적예외다. A의양극단아님은시험답같지않고C의naloxone비교는별개다. |
| MA-EXP-0715 | PMP07 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 성인첫처방7일과knownnonopiatedirective는다른trigger다. A의minor한도는제3주제이고actualquantity·exception근거가없다. |
| MA-EXP-0719 | PMP08 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | X번호폐지와3일directdispensing은서로다른연방법경로다. 모두정답이라현재자격을실제적용하는대안이없다. |
| MA-EXP-0723 | LAB01 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | internalrecord에있는directions가label에서빠진상황은실무적이다. technician최종검수와drugclassname은별도약한오답이다. |
| MA-EXP-0727 | LAB02 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | characters/inch와pointsize는특이하지만실제요청에의미있다. compoundedidentity·inpatient예외·BUD가한문항에추가돼결정이분산된다. |
| MA-EXP-0731 | LAB03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 실물전달금지문구와Rx정보transfer는다른행위인데opioidleaflet두개정답이추가돼중심이흐린다. |
| MA-EXP-0735 | LAB04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | protectedcareVI예외와testosteroneCIII는실질조건차이다. exacteligiblecare가제시되지않고모두정답이며B/D는일반론이다. |
| MA-EXP-0739 | LAB05 | MAJOR_REWRITE / P1 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | IR↔ER와wrongreferenceA-rating은서로다른productmatch결함이다. 유일정답D는보험선호라는지문밖일반론이다. |
| MA-EXP-0743 | LAB06 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | less-expensiveavailableproduct가확인된상황은적절하다. C/D는실제제품기록을안한다는같은오답을반복하고A는별도nosub이야기다. |
| MA-EXP-0747 | LAB07 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | generic명처방과authorizedgenericNDA는각기다른판단이다. 보기A/D가availability/match주의만말해정확한선택결정이없다. |
| MA-EXP-0751 | LAB08 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 조건을충족한emergency라고지문이법적판정을미리준다. 전부정답이며routine불편과therapychange일반론이끼어든다. |
| MA-EXP-0755 | LAB09 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 제품별interchangeable분류와MA통지를함께볼수있지만실제제품정보없고다른주5일을단순오답으로삼는다. |
| MA-EXP-0759 | LAB10 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 실제retail가격과costshare액이없어서법정비교를실행할수없다. B/C는paidclaim이항상지배한다는같은오해다. |
| MA-EXP-0763 | PACK01 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | blister의tamperproof와CR성능구별은실제적이나OTC전부면제는과장이고C의childproof정의는별개암기다. |
| MA-EXP-0767 | PACK02 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 요청주체가waiver범위를바꾸는좋은대조다. 모두정답이며D의agealone은지문밖이다. |
| MA-EXP-0771 | PACK03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 21×5mg와 22×5mg은정확한exception경계다. 그러나유일정답B는기타성분조건이고C는21정이라는단위만으로틀린산술오답이다. |
| MA-EXP-0775 | PACK04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | nitrate·potassium·mnemoniccontraceptive를한문항에섞어세제품예외목록을만들었다. 실제threshold값을적용할양은없다. |
| MA-EXP-0779 | PACK05 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 타약국조제약의planner와마모closure는서로다른제한이다. B의supplycap과C의nonCR면제도넓은일반론이다. |
| MA-EXP-0783 | PACK06 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | PRN·짧은안정성·liquidmixing의세결함을겹치고모든보기를맞게했다. 한사례로필수행동을분명히하기어렵다. |
| MA-EXP-0787 | SALE01 | MAJOR_REWRITE / P1 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 2.4+1.5g초과라는판단자료가있는데유일정답A는별도30daywindow다. B의channel혼동도daily거래와무관하다. |
| MA-EXP-0791 | SALE02 | MAJOR_REWRITE / P1 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | openaccess와60mglogbook예외는독립판단이고A/B의교육·2년보존은지문밖정답이다. |
| MA-EXP-0795 | SALE03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | device와약처방권한은분리할필요가있다. B의CVOTC는별도OPEN영역이며A의inventedcap은실무대안이아니다. |
| MA-EXP-0799 | SALE04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 사람약을동물에사용하는것과vet가사람치료하는것은다르지만후자는너무명백하다. A의remoteVCPR은구체적주관할없이추가되고alltrue다. |
| MA-EXP-0803 | SALE05 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | withdrawal지시누락과VFDextralabel금지는다른제품경로다. A의bulkcompounding,D의animalidentifier까지넓게나열된다. |
| MA-EXP-0807 | SALE06 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 검사specimen/timing변경과notforresalesample은연관없는사건이다. B의무제한진단권한은쉬운오답이다. |
| MA-EXP-0811 | ORD01 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 두supplier한form과60일shipmentclock는실무적이지만현재single-sheet·blankform권한까지기초목록을넓힌다. |
| MA-EXP-0815 | ORD02 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | MORtitle과POA는실질적차이다. CSOScredential공유와EPCS정의도추가해alltrue가됐다. |
| MA-EXP-0819 | ORD03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 10000/200000과추가1000은분모가함께변한다는유효산술판단이다. B의모든주법면제는멀고두case를하나의예정거래로합칠수있다. |
| MA-EXP-0823 | ORD04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 106을ordinaryorder로쓴다는오답은단순form암기다. expiration과patientreturn은또다른대조로현재stockreturn결정을희석한다. |
| MA-EXP-0827 | ORD05 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 초기통지를조사종료까지기다리는것은현실적오류다. A는retrievedcurrent라는작성자메타문구이며45일기한은새공식재확인없이승계하지않아야한다. |
| MA-EXP-0831 | ORD06 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Boardresident와DCPfacility라는등록차이는중요하다. 모든보기가맞으며해당하는confirmedreportableevent라고지문이분류를미리준다. inheritedOPEN을모든시계완료로표현하지않는다. |
| MA-EXP-0835 | ORD07 | MAJOR_REWRITE / P1 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 전산삭제로물리파괴완료라는사례는너무명백하다. 유일정답C는별도reversedistributor30일시계이며B/D는다른기록경로다. |
| MA-EXP-0839 | INV01 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | zerostock도initialrecord와newcontrol effective-dayinventory는별도trigger가있다. B의별도location은지문밖이다. |
| MA-EXP-0843 | INV02 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 1000/1001과CIIalwaysactualcount는법적조건에따라방법이바뀌어보존가치가있다. A의opening/closing은주제밖정답이다. |
| MA-EXP-0847 | INV03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 110기대와109실측은조사필요성을판정할수있다. 세주무reconciliation과함께alltrue로묶이며작은차이의significance는자료부족이다. |
| MA-EXP-0851 | STO01 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 제품label이범위외라고만하고실제조건은주지않는다. dormunit에음식까지넣어여러명백결함을추가한다. |
| MA-EXP-0855 | STO02 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 정상복귀후release는실제품질오류다. B의closedday요건과C의기록폐기는다른운영조항이다. |
| MA-EXP-0859 | STO03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | damagedseal수령과coldpack동결shipping은다른custody단계다. B의USPS권한은실제shipping방법없이추가됐다. |
| MA-EXP-0863 | SHR01 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 다른소유pharmacy간contract가가능한지좋은법적경계다. 모든보기가맞고confidentiality·notice·training은추상checklist다. |
| MA-EXP-0867 | SHR02 | MAJOR_REWRITE / P1 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | remote technician의독립검수와타주telepharmacy모델을묻는데유일정답D는centralfillcompounding제한이다. stem과key의결정경로가다르다. |
| MA-EXP-0871 | SHR03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | locker라는명칭으로CII·냉장제제를보관한다는두조건은실제APS분류에필요하다. B의accesscode만으로모든요건대체는약한오답이다. |
| MA-EXP-0875 | SHR04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 같은cell여러lotrecall은구체적이나ADD환자order없음과묶고C가세장치정의암기가됐다. |
| MA-EXP-0879 | CMP01 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | FDAapproved광고와unlimitedofficeproduction은둘다과장된503A오해다. A의insanitary와C의reconstitution은제3·4주제이며alltrue다. |
| MA-EXP-0883 | CMP02 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | COA만으로bulk적격하지않다는좋은경계가있지만유일정답D는RUOpowder외관이라는노골적부적격사례다. |
| MA-EXP-0887 | CMP03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | dyeintolerance의prescriberdocument와localoutofstock가격복제는실질조건차이다. D의shortagetime은변동근거를구체화해야한다. |
| MA-EXP-0891 | CMP04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | intacttabletAOR를crushing에적용하는조건변화는좋다. complex라고결론을미리주고D의USP명칭변경을넓게추가한다. |
| MA-EXP-0895 | CMP05 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | VIflavoring과kit의다른diluent/concentration은서로다른분류결정이다. D의tablesplitting은세번째행위이며alltrue다. |
| MA-EXP-0899 | CMP06 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | recipe와actualbatchlot추적은실무적이고직접연결된다. A/D가같은MFR로CR대체오해를반복하고정답C는추상적traceability다. |
| MA-EXP-0903 | CMP07 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | aw범주와oral/nonoral차이는독립판단이있다. 실제shorterlimit숫자가없고C의frozenonly는어색한조건이다. USP정본/공개근거의정확한범위재확인이필요하다. |
| MA-EXP-0907 | CMP08 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | ISO5hood와unclassifiedSCA는category를바꾸는실제사실이다. Cat3toxicity라는CaseB와D의HD는별도주제다. |
| MA-EXP-0911 | CMP09 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 08:00start12:15admin과4products는정확한시간/개수판단이다. 모두정답이고A의sourcecontainer재사용은지문밖이다. |
| MA-EXP-0915 | CMP10 | MAJOR_REWRITE / P1 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | requiredtestpending과다른qualityattributes는실제release문제다. 유일정답B는다른releasechecks목록으로기다려야하는지직접묻지않는다. |
| MA-EXP-0919 | HD01 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | DEAunscheduled와HD는독립분류로의미있다. C의둘중하나만가능은극단적이며APIcontainment는두번째사건이다. |
| MA-EXP-0923 | HD02 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | nitrile소재만으로chemo성능을확정하지않는구별은좋다. A의designatedperson직종은지문밖이고training과glove를한판단으로연결하지못한다. |
| MA-EXP-0927 | HD03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | alcoholwipe하나로네목적을모두달성했다는것은과장이다. controlledHDwaste는유용한중첩이나별개case이고모두정답이다. |
| MA-EXP-0931 | OUT01 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 503B의cGMP잔존은핵심이지만A의MA허가와D의환자처방까지넓게묻는다. productapproval주장도별도의정의문제다. |
| MA-EXP-0935 | OUT02 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | bulkCOA와thirdpartyresale는독립된503B조건이다. shortage를근거로쓸실제제품·기간은제시되지않는다. |
| MA-EXP-0939 | OUT03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | registration과June/Decemberproductreport는실제다른제출물이다. CaseBlabel과B의lot면제까지섞어두의무를목록화한다. |
| MA-EXP-0943 | OUT04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | provisional에서preparation과distribution을구별하는좋은경계다. C의갱신과D의relocation은사례밖이고alltrue다. |
| MA-EXP-0947 | FDA01 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | IND와routine판매의구별은중요하나A의BLA가약사면허는우스운오답이다. ANDAform대체는LAB05와실질중복이다. |
| MA-EXP-0951 | FDA02 | MAJOR_REWRITE / P1 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | NDC+label검색은approval증거가아니라는구체적오해다. 유일하지않은정답A/B는OTCpathway와offlabelscope로두사례의직접해결이아니다. |
| MA-EXP-0955 | FDA03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 한정exemption의범위를읽는문제는유용하다. 실제exemption요건을본문에주지않고documented라고결론내려특정범위적용은못한다. |
| MA-EXP-0959 | FDA04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 제품identifier와ATP는별도증거라는구별이좋다.6년기록은다른case로묶였고B/C는추상범위주의이며alltrue다. |
| MA-EXP-0963 | FDA05 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | suspect조사와illegitimate판정후24시간은상태변화가행동을바꾼다. B의FDA3911=DEA106은단순기관혼동이며A의공간확보격리해제는비현실적이다. |
| MA-EXP-0967 | FDA06 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | marketed위반제품과미release직접통제lot는정의에따라분류가달라진다. A의남는다른의무는추상적이며D의모든physicaltransport는넓은오답이다. |
| MA-EXP-0971 | FDA07 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | classification전recall은실제workstream이다. B의ClassIII선택준수는쉬우며C의ClassI정의는다른사건이다. |
| MA-EXP-0975 | NUC01 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 추가nuclear권한과patientname72시간은각기실제법규이나3년기록·calibration까지네독립명제로alltrue가됐다. |
| MA-EXP-0979 | CQI01 | MAJOR_REWRITE / P1 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | strength오류가환자도달전에잡힌상태는구체적이지만다른commercialAE와defect를추가했다. 유일정답C는정확조제여도AE가능이라는임상일반론이다. |
| MA-EXP-0983 | CQI02 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 이름목록만있는CQI와평가안한workflow변경은실제품질관리결함이다. B의개업때만교육,D의추가평가불필요는쉽다. |
| MA-EXP-0987 | CQI03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Monday10시발견후Friday까지기록을미루는것은명확한clock사례다. B의2년retention을추가해초기행동결정을흐린다. |
| MA-EXP-0991 | CQI04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | ED추가treatment/monitoring은입원없어도serious정의에들수있는핵심조건이다. CaseB가같은오해를반복하고D의503B는별도기준이며alltrue다. |
| MA-EXP-0995 | CQI05 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 두사실동시인지로OPENtrigger를피한범위는명시적이다. 유일정답C는5년보존이며당장보고행동을직접고르지않는다. B해설의calendar/business차이는유용하다. |
| MA-EXP-0999 | CQI06 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | employee가먼저안사실과MOR3일뒤열람은실제trigger차이다. suspecteddefect의즉시정책중첩은보존하되SADE라고결론을미리주지않아야한다. |
| MA-EXP-1003 | CQI07 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | initial과followup15일은실제두시계이나annualregistration까지기다림은약한오답이다. D의retention전면없음도쉽다. |
| MA-EXP-1007 | CQI08 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | defectidentified와recall시점의차이는유효하며injury전대응도중요하다. 모든정답이고실제두날짜를주지않아시계적용이없다. |
| MA-EXP-1011 | EM01 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | air2와surface정확히3은unit와부등호에따라결과가달라지는실질판단이다. C의clearappearance로무시와D의분모동일시는명백하다. |
| MA-EXP-1015 | EM02 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | m³를L와같게취급하는것은단위상명백하며pass-throughcleanerclass는별도의조건이다. D의종류별threshold일반론이정답이다. |
| MA-EXP-1019 | EM03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 미생물report수령과최종동정의차이는중요하며중간정상결과가repeat를지우는지실제경계다. A/C는보고주체와investigation일반론이다. |
| MA-EXP-1023 | EM04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | nonviable와viableremediation은다른운영결정이다. alltrue이고specificconditions라고미리충족을가정해실제riskassessment를판정하지않는다. |
| MA-CASE-0009 | PLUS-SC01 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 6+8=14 후6시간추가라는단일계산은명확하고보기4시간은10시간전부인정오류를겨냥한다. 그러나모든오답해설이정답계산을그대로복사해각오류를설명하지않는다. |
| MA-CASE-0018 | PLUS-SC02 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 16total/1live에서추가4시간은명확하지만1 are live문법과오답전체가필요량보다많아부족한plan의법적결함을비교하지못한다. |
| MA-CASE-0022 | PLUS-SC03 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 전년22시간과현재18/1law는carryover와category를함께판단하게해유용하다. 1approvedlawhours문법과복제해설이남는다. |
| MA-CASE-0031 | PLUS-SC04 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | actualhour와category중복충족을max계산으로명확히묻는다. 1livehours문법과5/7시간오답의생성논리가설명되지않는다. |
| MA-CASE-0038 | PLUS-SC05 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 2agreements와21total/1related가실질적조건이며9시간오답이agreement별추가를반영한다. agreement(s)와1hours가템플릿흔적이고해설반복이다. |
| MA-CASE-0046 | PLUS-SC06 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 2021졸업2026년1월transfer는면제/lategrace가둘다해당안되는명확한판정이다. Jan05표기는자연스럽게다듬고A해설을이사례의불충족일자에직접연결해야한다. |
| MA-CASE-0055 | PLUS-SC07 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 2026졸업7월면허로graduationyear를직접판정한다. C의오답해설은일반요건을유지한다는문장으로왜면제가우선하는지설명하지못한다. |
| MA-CASE-0071 | PLUS-SC08 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 실제접종이라는role외에결정조건이없어1시간암기문항이다. 제목은workperformed지만directsupervision/temporary역할이없고해설만그조건을언급한다. |
| MA-CASE-0076 | PLUS-SC09 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 갱신일정작성이라는단일운영작업과네자격의달력오답이병렬이다. 단순암기난도이므로높은reasoning문항으로표시하지말아야한다. |
| MA-CASE-0082 | PLUS-SC10 | MAJOR_REWRITE / P0_INTERNAL_ANSWER_AMBIGUITY | HOLD_FROM_DEFAULT | — | NOT_REVERIFIED | 1months문법외에A의Stoppracticeandsatisfyapplicableconditions도넓게참이어서C와상호배타적이지않다. A해설이문구에없는60일초과를가정한다. 현재 보류 이유: 기존 정답 C는 1개월 ordinary lapse에 60일 초과 추가조건 기준이 아직 적용되지 않았다고 설명합니다. 그러나 오답 A의 'Stop practice and satisfy applicable Board reinstatement conditions; MPJE is not automatic from this duration alone'도 일반적인 표현으로는 같은 상황에서 타당하게 읽힙니다. 오답 해설에만 60일 초과 조건을 넣어 A를 배제할 수 없습니다. 정답의 구체성 차이만으로 SBA를 채점하지 않도록 보류합니다. |
| MA-CASE-0093 | PLUS-SC11 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 13+8근무에서credit20을묻고근무합법성판단을명시적으로분리한범위는정직하다. 그러나금지가능한근무를추상숫자exercise로쓰며19오답의법적혼동근거가없다. |
| MA-CASE-0100 | PLUS-SC12 | MAJOR_REWRITE / P0_INTERNAL_ANSWER_AMBIGUITY | HOLD_FROM_DEFAULT | — | NOT_REVERIFIED | 2CPhT+2ordinary는실제적격mix지만C의Fourstaffneedtwopersonmix는일반적으로참이며이사례가그조건을못채웠다는문구가없다. D도다른headcount일반법칙이다. 현재 보류 이유: 4명 중 CPhT 2명인 사례에서 정답 A는 비율과 자격 조합을 충족한다고 설명합니다. 그런데 C의 'Four support staff need the required two-person qualifying mix'도 그 사실과 양립하는 요건 설명이며, D도 별도 3명 조합에 관한 일반 규칙입니다. 해설은 지문에 없는 자격자 부족을 C에 가정합니다. 비교하는 선택지의 적용 조건과 판단을 다시 작성해야 합니다. |
| MA-CASE-0117 | PLUS-SC13 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | trainer와computertrainee가실제filling을겸해count4가되는좋은조건변화다. 0ordinary와1people등템플릿표현·복제해설이품질을낮춘다. |
| MA-CASE-0122 | PLUS-SC14 | MAJOR_REWRITE / P0_INTERNAL_ANSWER_AMBIGUITY | HOLD_FROM_DEFAULT | — | NOT_REVERIFIED | A의Reassigntaskbecausetierdoesnotauthorize와정답B의pharmacist-onlyboundary는같은상황에서둘다타당하다. A해설은전화처방을설명해제시된finalverification과불일치한다. 현재 보류 이유: CPhT에게 final patient-specific prescription verification을 맡기는 사례에서 A의 업무 재배정과 정답 B의 pharmacist-only 경계 적용은 같은 결론입니다. A의 오답 해설은 이 사례와 무관한 전화처방 수신 권한을 설명합니다. 하나의 정답으로 채점하기 어려워 기본 연습에서 보류합니다. |
| MA-CASE-0128 | PLUS-SC15 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 17세만불충족인조건은단일limitingcondition을명확히평가한다. pharmacist투여라면서internsupervision조건을붙인템플릿문장이불필요하다. |
| MA-CASE-0136 | PLUS-SC16 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | currentcertification과10postlicensehours의대조는either/or조건에실질적이다. 질문은무엇을보완하냐인데정답은이미충족이라는문법이맞지않는다. |
| MA-CASE-0145 | PLUS-SC17 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 35세VI서면referral/consent보험까지조건이명확하나모두충족이라고나열해독립시나리오보다eligibilitychecklist다. distractor는각다른미충족변형의잔재다. |
| MA-CASE-0154 | PLUS-SC18 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Sep1issue/earliest와Sep30조제는30일validity만판정하며earliest가같아독립constraint가작동하지않는다. 해설은명확하고보기는비교가능하다. |
| MA-CASE-0163 | PLUS-SC19 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 24시간경과·60중12기조제라서48잔량이라는명확한행동이다. timeline조건은평이하지만공급량과clock를함께적용하며오답별이유도분리되어있다. |
| MA-CASE-0173 | PLUS-SC20 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | day29·남은60·요청30으로authorizedbalance와patientrequest를구별한다. 31정오답은근거없는off-by-one이고모든해설이복제계산이다. |
| MA-CASE-0187 | PLUS-SC21 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 6개월초과이면남은4refill도행사불가라는단일결정이명확하다. refill(s)와have문법및모든오답동일해설이남는다. |
| MA-CASE-0190 | PLUS-SC22 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 한번도transfer안했는데anotherrefilltransfer라는표현이모순적이다. 정답경로는명확하지만A/D해설은이사례에서왜틀린지실제2refill/유효기간을언급하지않는다. |
| MA-CASE-0199 | PLUS-SC23 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | testosterone의nonopioidCIII라는약물조건이적절하나해설은OUD/nonopioid/pump중어느것인지불명확하게or를나열한다. |
| MA-CASE-0208 | PLUS-SC24 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | validID가이미있는데C는obtainacceptableidentifier라는이미완료된행동을제시해일부참이며불필요한hardship기록누락을지문에강조한다. |
| MA-CASE-0217 | PLUS-SC25 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | neverfilled/nevertransferred원EPCS와두DEA약국이구체적이나환자요청등을allotherconditions에숨긴다. 오답들은주로다른transfer유형의명백한혼동이다. |
| MA-CASE-0226 | PLUS-SC26 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | CII25정에exactcount를적용하는명확한기초판단이다. B해설이마치이사례가III-V라고말해오답을설명하지않는다. |
| MA-CASE-0238 | PLUS-SC27 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 85+60−40−5=100은단순산술이고실측도100이라법규상다음행동이바뀌지않는다. 101정오답과0정차이를조사시작점이라설명하는문구가인위적이다. |
| MA-CASE-0244 | PLUS-SC28 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | orderday0·shipmentday3·today10으로시작점을구별할수있다. 제목near expiration과달리10일째이고50day(s)는템플릿잔재다. |
| MA-CASE-0255 | PLUS-SC29 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 250/5000에서한unit추가로5%초과하는경계가실질적이다. 1additionalunits문법과A해설이이경우에도5%이하라고단정하는템플릿오류가있다. |
| MA-CASE-0262 | PLUS-SC30 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 14일microbialcap과8일안정성중짧은8일이라는판단은명확하다. 365/15일오답은불필요하게약하고foranonpreservedaqueous가부자연스럽다. |
| MA-CASE-0271 | PLUS-SC31 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 20일·namedpatient·registeredlocation은해당배송경로조건을명시한다. D의donotredirect는대상이이미samepatient라별도사례템플릿느낌이다. |
| MA-CASE-0282 | PLUS-SC32 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | ISO5surface4CFU와>3은명확한단일threshold판단이다. A해설이현재값을threshold이하라단정해사례와모순된다. |
| MA-CASE-0298 | PLUS-SC34 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | confirmedemployee theft1정VI라는조건은losssignificance와schedule혼동을실제로바꾼다. Board한정범위를명확히한점은좋고inheritedOPEN을자동해결하지않았다. |
| MA-CASE-0307 | PLUS-SC35 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 10월19일09:30에72시간을더하는것은명확하나보고별다른clock를실제로비교하지않는다. 모든해설이같아24/48/96시간오해를가르치지못한다. |
| MA-CASE-0316 | PLUS-SC36 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 구REMSsoftwaregate는현실적이지만D의isotretinoinwindow복사는어색하고정답B가가장길며균형잡힌문구로눈에띈다. |
| MA-CASE-0325 | PLUS-SC37 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | ED추가testing이즉시통지trigger라는구체적사실이있다. A/D는권고notation·reassessment에관한다른사례의정답같은문장이다. |
| MA-CASE-0334 | PLUS-SC38 | MINOR_EDIT / P3 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 105mg와다른coveredsubstance없음이구체적이다. A해설이초과했다고단정하여본사례와모순되고B/D는약한과장오답이다. |
| MA-CASE-0349 | PLUS-WQ01 | HOLD_FOR_LEGAL_REVIEW / P0_LEGAL_SOURCE_CONFLICT | HOLD_FROM_DEFAULT | — | NOT_REVERIFIED | 정답 B의 승인된 타 관할 home-study law 2시간 인정 결론은 이번 보류 사유로 변경하지 않는다. 그러나 core_reasoning과 A의 오답 해설·교정문이 현재 CE 미충족 통지 경로를 Board email로 단정한다. ce-deficiency-source-conflict.json의 Mandatory Disclosure Form/email 출처 충돌이 이 해설에도 적용되므로 현재 제출방법을 확정해서 학습시키지 않도록 HOLD한다. 현재 보류 이유: 정답 B의 law CE 판단과 별개로, core reasoning 및 오답 A 해설이 현행 CE 미이수 통지 경로를 Board email이라고 단정합니다. 현재 공식 Policy 2021-04의 Mandatory Disclosure Form 문구와 충돌하는 해설을 기본 학습에서 제시하지 않도록 보류합니다. 정답 B가 틀렸다고 판정하거나 원본 정답을 바꾸는 조치는 아닙니다. |
| MA-CASE-0352 | PLUS-WQ02 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 허용CIIentry와verbalVI·internfinalcheck·CPhTcounseling은독립업무목록이다. 위임금지세개를배제하면되어단일새시나리오가없다. |
| MA-CASE-0363 | PLUS-WQ03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | dedicatedtrainer제외가정답이지만hospitalintern면허·직함만바꾸기·사후traininglabel은기존대표를그대로동시평가한다. |
| MA-CASE-0377 | PLUS-WQ04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Retired status의 업무 중단이 정답이지만 다른 보기의 compounding 갱신·reciprocity 신청 시계·타주 면허는 서로 다른 의사결정이다. |
| MA-CASE-0385 | PLUS-WQ05 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | One-MOR 원칙과 relocation·remodeling·ownership 사전 승인을 한 지문에 모아 정답이 단순 준수 문장으로 보인다. |
| MA-CASE-0421 | PLUS-WQ09 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Measuring device 제공은 자연스러운 업무지만 상담 위임·Medication Guide refill·변경 치료 상담은 별개의 환자 기록이다. |
| MA-CASE-0426 | PLUS-WQ10 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 30일 접근 시계는 유용하나 이웃 기록 호기심 열람·무관 병력 제공은 너무 명백하고 서로 다른 HIPAA 경로이다. |
| MA-CASE-0433 | PLUS-WQ11 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 정답인 자동 refill 동의는 다른 세 보기의 allergy 확인·downtime 복원·barcode 적법성 검토와 직접 관련이 없다. |
| MA-CASE-0448 | PLUS-WQ12 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | PTT의 접종 불가와 shingles 사전 MIIS 조회·응급약 order·72시간 보고를 한 질문에서 혼합한다. |
| MA-CASE-0452 | PLUS-WQ13 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Ceftriaxone IM 허용이 정답이나 새 약물 교육·methadone OTP·포장 조건은 각기 독립된 규칙의 오답이다. |
| MA-CASE-0466 | PLUS-WQ14 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 새 PharmD의 경험 요건이라는 정답은 retail consent 문서·성인 요건·CPA 갱신 오답과 다른 결정이다. |
| MA-CASE-0473 | PLUS-WQ15 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Contraception 보험 범위와 권한 구별은 추상적이며 naloxone OTC 구매·standing order·구조키트 상담은 서로 다른 경로이다. |
| MA-CASE-0478 | PLUS-WQ16 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Clozapine REMS 제거를 MA-CASE-0316과 다시 묻고 Brixadi·TIRF 제품 식별을 관계없는 오답으로 사용한다. |
| MA-CASE-0493 | PLUS-WQ17 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 정답은 depot product의 여러 항목을 확인한다는 일반론이며 약물·경로·환자 사실이 없어 실제 허용 여부를 판단하지 않는다. |
| MA-CASE-0595 | PLUS-WQ29 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 스캔 처방과 EPCS 구별은 핵심이나 보험 수량 변경·다른 성분 교체는 명백한 별도 오류이며 전자예외 기록과 함께 혼합된다. |
| MA-CASE-0607 | PLUS-WQ30 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Unfilled paper alprazolam을 전산 입력해도 EPCS가 되지 않는다는 정답은 구체적이나 나머지 보기의 기산일·보존·담당자는 다른 transfer 결정이다. |
| MA-CASE-0617 | PLUS-WQ31 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Schedule II라는 지문 아래 CIII testosterone이 오답에 들어가고 hospice fax·central-fill oral·90일 OUD 범주가 따로 논다. |
| MA-CASE-0626 | PLUS-WQ32 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 총 partial 수량이 처방량을 넘지 않는다는 정답은 상식적이며 same-pharmacy·요청자·30일 기산점은 별개의 더 구체적 판단이다. |
| MA-CASE-0631 | PLUS-WQ33 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Transfer history 수집 정답을 묻지만 다른 보기의 무권한 dose change·refill 무허가 생성은 지나치게 분명하다. |
| MA-CASE-0645 | PLUS-WQ34 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Authorized generic의 NDA 관계라는 지식 문장이 emergency written acceptance·보호 진료 label·in-use limit과 섞여 있다. |
| MA-CASE-0650 | PLUS-WQ35 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Patient request와 prednisone·nitroglycerin 예외·tamper evidence를 나열하여 같은 포장 규칙의 실제 충돌 없이 참 문장을 찾게 한다. |
| MA-CASE-0662 | PLUS-WQ36 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Gabapentin의 MA VI/PMP 분류 정답은 이전 PMP 항목과 겹치며 계정·pickup ID·처방 변경은 다른 의무를 열거한다. |
| MA-CASE-0708 | PLUS-WQ41 | MAJOR_REWRITE / P1 | HOLD_FROM_DEFAULT | — | NOT_REVERIFIED | B의 that opened Schedule IV container에는 수량 사실이 없는데 오답 해설은 1000개 초과라고 새 사실을 넣는다. 정답 부족 조사와도 무관하다. 현재 보류 이유: 오답 B는 수량이 제시되지 않은 opened Schedule IV container의 추정 계수를 설명합니다. 해설은 지문에 없는 1,000정 초과 수량을 가정하여 exact count가 필요하다고 단정합니다. 해당 용기의 수량이 빠져 B의 허용 여부를 결정할 수 없으므로 단일 정답 문항으로 사용하지 않습니다. |
| MA-CASE-0713 | PLUS-WQ42 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 정답은 5% 산정 단위를 말할 뿐 실제 수량·다음 거래가 없어 허용 여부를 평가하지 않는다. Form 222·POA는 별도 경로이다. |
| MA-CASE-0722 | PLUS-WQ43 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Recall 회수 허용과 재판매 가능성 구별은 유용하나 stock return·hazardous waste·쓰레기통 폐기는 다른 사건이다. |
| MA-CASE-0736 | PLUS-WQ44 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 반환 배송품의 이력 확인이라는 정답은 일반적이며 interstate 면허·냉동제품 냉장·dorm refrigerator는 독립 규칙이다. |
| MA-CASE-0741 | PLUS-WQ45 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | APS 선택권은 실제 환자 상황 없이 선언되며 PPA final verification·remote staffing은 다른 기기의 법적 경로이다. |
| MA-CASE-0748 | PLUS-WQ46 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Significant difference의 medical need가 정답이지만 recipe 기록·BUD와 validity 혼동·flavoring 처리는 따로 적용되는 규칙이다. |
| MA-CASE-0764 | PLUS-WQ47 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Required sterility test 결과를 기다리는 정답에 대해 외관만으로 category 선택·이동으로 시간 재설정은 약한 오답이다. |
| MA-CASE-0767 | PLUS-WQ48 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 비통제약도 hazardous handling을 평가한다는 추상 정답이며 분쇄·폐기·hood 조건이 실제 작업 없이 나열된다. |
| MA-CASE-0781 | PLUS-WQ49 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Stock recovery 구별이라는 정답에 실제 유통 상태가 없고 recall Class I를 Schedule I로 오인하는 오답은 지나치게 쉬운 언어 혼동이다. |
| MA-CASE-0785 | PLUS-WQ50 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | CQI 기록과 외부 보고가 병행된다는 일반론이 정답이며 defective preparation 회수와 ED harm 정의를 다른 사건으로 섞는다. |
| MA-CASE-0795 | PLUS-MR01 | HOLD_FOR_LEGAL_REVIEW / P0_LEGAL_SOURCE_CONFLICT | HOLD_FROM_DEFAULT | — | NOT_REVERIFIED | 정답 D가 Board email을 현재 CE 미충족 통지 방식으로 직접 확정한다. ce-deficiency-source-conflict.json의 Form/email 출처 충돌이 이 문항에도 그대로 적용된다. 다른 네 CE 보기의 타당성과 별개로 SATA 정답 집합을 확정할 수 없다. 현재 보류 이유: CE 미이수 시 Board에 email로 상세 사유를 보내는 것이 현행 정책의 제출 경로라는 선택지와 해설이 있습니다. 기존 노트의 email 안내와 이번 공식 Policy 2021-04의 Mandatory Disclosure Form 문구가 일치하지 않아, MA-EXP-0051과 같은 출처 충돌로 보류합니다. 다른 보기의 정확성까지 부정한 판정은 아닙니다. |
| MA-CASE-0802 | PLUS-MR02 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Certified inventory entry·intern 상담·pharmacist final check·cashier 업무·vendor 출입이 서로 다른 경계를 나열하며 기존 PER 사례와 겹친다. |
| MA-CASE-0814 | PLUS-MR03 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Trainer·trainee 자격 재분류, 1:3 mix, 4 intern clinic, nonfilling 제외를 한 번에 나열한다. 한 팀의 실제 산정 결과가 없다. |
| MA-CASE-0826 | PLUS-MR04 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 면허 발급·reciprocity·1년 개업·specialty 허가를 같은 employer queue에 모아 독립적인 다섯 참거짓 판단만 요구한다. |
| MA-CASE-0829 | PLUS-MR05 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | MOR의 30시간·handover inventory와 ownership·relocation 규칙이 혼합되며 MA-CASE-0385와 상당한 행동 문구가 반복된다. |
| MA-CASE-0847 | PLUS-MR07 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 다섯 상담 관련 요소 중 certified technician의 임상 상담만 부정하여 네 개를 고르는 구조이다. 액제 장치와 상담 변경은 MA-CASE-0421과 반복된다. |
| MA-CASE-0861 | PLUS-MR08 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 30일 접근·6년 기록 보존은 MA-CASE-0426과 그대로 겹친다. 호기심 열람과 무관 병력 공개는 약한 오답이다. |
| MA-CASE-0867 | PLUS-MR09 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 대부분 정답이 review·verify·clarify·investigate 같은 신중한 동사로 드러나고 유일 오답은 alert를 자동 금지로 삼는 극단이다. |
| MA-CASE-0879 | PLUS-MR10 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | PT experience·selection 권한·MIIS objection·72시간 보고를 묶어 하나의 접종 결정 없이 네 정답을 선택한다. |
| MA-CASE-0883 | PLUS-MR11 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | MA-CASE-0452의 ceftriaxone·OTP·single-dose 문장을 거의 그대로 긍정형으로 반복한다. 기록 항목 추가 외에 새로운 결정 조건이 약하다. |
| MA-CASE-0895 | PLUS-MR12 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 24시간 통지·consent 보관·성인 VI scope·진단 경계를 모아 네 정답을 고르는 checklist이며 MA-CASE-0466의 경로가 재등장한다. |
| MA-CASE-0903 | PLUS-MR13 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Daily norgestrel·ulipristal Rx·levonorgestrel OTC·EC standing order·naloxone 상담을 별도 환자 없이 나열한다. Coverage가 scope를 확장한다는 유일 오답은 반복된다. |
| MA-CASE-0910 | PLUS-MR14 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 서로 다른 다섯 제품의 규칙을 나열하며 MA-CASE-0478의 Brixadi·TIRF 오답이 그대로 반복된다. |
| MA-CASE-0919 | PLUS-MR15 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Methadone indication·X-waiver 제거·stock transfer를 묶고 유일 오답은 schedule 숫자가 DUR를 면제한다는 명백한 오류이다. |
| MA-CASE-1005 | PLUS-MR24 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 스캔 EPCS·수량 변경은 MA-CASE-0595와 반복된다. Forgery와 paper replacement는 의미 있는 다른 경로지만 두 사건을 실제로 연결하지 않는다. |
| MA-CASE-1014 | PLUS-MR25 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Initial CII EPCS와 IV refill transfer를 별도 기록으로 혼합하고 보존·원 issue date 오류는 MA-CASE-0607과 반복된다. |
| MA-CASE-1022 | PLUS-MR26 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 응급 follow-up을 두 번째 공급으로 쓰는 오류와 CII refill 허용은 매우 명백하다. Central-fill·90일 supply·hospice fax는 MA-CASE-0617과 반복된다. |
| MA-CASE-1027 | PLUS-MR27 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Shortage72시간과 요청partial30일을 구분하는 학습 목표는 유용하나 다섯 별도 기록에서 새 stock도착 재시작이라는 쉬운 유일 오답을 찾는다. |
| MA-CASE-1042 | PLUS-MR28 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | MA-CASE-0631의 네 보기 경로를 반복하면서 transfer가 refill을 복원한다는 추가 극단 오답을 붙인다. |
| MA-CASE-1051 | PLUS-MR29 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Biologic substitution 통지·Purple Book·large print 단위·일반 generic label을 한 문제에 혼합한다. Biosimilar 승인만으로 교환한다는 유일 오답은 이미 학습한 규칙이다. |
| MA-CASE-1058 | PLUS-MR30 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Prescriber request 범위는 유용한 차이지만 recall lot·오조제 반품·VI 60일 packaging은 서로 무관한 운영 사건이다. |
| MA-CASE-1063 | PLUS-MR31 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 계정·조회·보고·DUR를 구별한다는 일반 문장이 네 정답이고 실제 collecting agent ID라는 유일 오답은 MA-CASE-0662와 동일하다. |
| MA-CASE-1085 | PLUS-MR33 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 부족 조사·영상 보존은 연결 가능하지만 실제 부족 사건이 없다. 수령 전 입고·2년까지 reconciliation 생략은 약한 오답이다. |
| MA-CASE-1091 | PLUS-MR34 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 서류 이름 구별·dosage unit 산정·등록 확인이 정답이며 60일 시계 재시작만 오답이다. MA-CASE-0713과 동일한 판단이 많다. |
| MA-CASE-1104 | PLUS-MR35 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | SATA이지만 정답은 A 하나이며 MA-CASE-0722와 같은 추상적 recall return 구별이다. 일반봉투·public volunteer·liner 재개봉은 명백한 오답이다. |
| MA-CASE-1111 | PLUS-MR36 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | MA-CASE-0736의 세 행동을 다시 정답으로 쓰며 유일 오답은 manufacturer 통화 뒤 excursion 기록 삭제이다. |
| MA-CASE-1123 | PLUS-MR37 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 상용제품 재구성·flavoring·medical need·patient Rx를 별도 참 문장으로 묶고 hazardous 분쇄를 일반 counting으로 보는 쉬운 오답만 둔다. |
| MA-CASE-1128 | PLUS-MR38 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | SATA 정답 하나이며 source vial limit과 finished CSP BUD를 구별한다는 일반 문장이다. 실제 puncture·preparation·administration 시간이 없다. |
| MA-CASE-1139 | PLUS-MR39 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | Hazardous 분쇄와 503B sourcing·FDA product approval·청소 단계가 별개이며 비통제약이라는 이유의 면제만 오답이다. |
| MA-CASE-1151 | PLUS-MR40 | MAJOR_REWRITE / P2 | NOT_YET_IMPLEMENTED | — | NOT_REVERIFIED | 보고기관·사건 유형 없이 agency clock를 늦추는 오류를 묻는다. 연결 노트는 improper dispensing와 SADE의 trigger가 다름을 설명하므로 어떤 시계인지 더 구체화해야 한다. |

## 재현 입력

| 파일 | SHA-256 |
|---|---|
| reports/representative-rewrite/legacy-editorial-triage.json | `01a319750ea8e092a1a0b48ec3b91285ff3cfabf30b6e4111903580c662e3865` |
| practice_expansion/2026-10-27-quality/selection.json | `3032ad16a4f3044e1cdba4119bafd1e1d142c88ad8aeebe378a5f0be8f1a0e64` |
| practice_expansion/2026-10-28-representative/selection.json | `3b803cdb240ff9fd2834f12be4e49ed191b3294d5e1bfb936780fb4b72bfcfee` |
| practice_expansion/2026-10-28-representative/questions.json | `b59a4685897c8d45035de082d40a36f3e29133df5f0a53fb6b66542b68f58ff4` |

`python scripts/build_representative_audit_ledger.py --check`는 현재 입력과 JSON·Markdown 산출물의 바이트 일치를 확인합니다.
