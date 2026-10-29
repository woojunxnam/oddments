# 다음 품질 단위와 추가 독립 사례의 우선순위

검토일: 2026-10-28. 기준 main: `b5bd6b02c7ea8a5c6731871fa6e330ac6795fd36`.

이번 신규 **46개는 기존 대표의 replacement**이다. 기존 고품질 문항 재사용 1개와 CE 출처 충돌 보류 1개를 포함해 첫 48개 대상의 처리 경로를 정한 것이다. 이를 별도 목표인 **부족 영역 신규 독립 사례 약 120개를 채운 것으로 집계하지 않는다.** 기존 355개는 개별 편집 triage를 마쳤지만 355개 전체 재작성이나 법규 전수 재검증이 끝난 상태가 아니다.

## 2026-10-29 후속 반영

두 번째 단위에서 **PER09–PER14, MOR01–MOR06의 12개**를 처리했다. 신규 사례 10개, 기존 고품질 사례 재사용 2개이며 추가 보류는 없다. 누적 **56 재작성 / 3 통합 / 7 보류 / 289 개선 미반영**이다. MA-EXP-0099는 MA-REV-0006, MA-EXP-0111은 MA-REV-0008로 통합했다. 이 10개도 부족 영역 약 120개 추가 목표로 중복 계산하지 않는다.

다음 작은 단위는 **PER15–PER22의 8개**를 우선해 실제 업무에 따른 ratio·직접 감독·전담 교육 인력·computer training의 경계를 확인한다. 그다음 MOR07–MOR10과 DISC01–DISC08을 처리한다. 수를 채우기보다 기존 사례 통합과 공식 적용 관계의 보류를 먼저 판단한다. 아래 32개 목록은 최초 계획이며 이 단락에 기록한 12개는 완료 범위다.

상세 변경과 필터 안내: [두 번째 단위 보고서](../../docs/REPRESENTATIVE_REWRITE_UNIT2.md).

## 먼저 처리할 기존 문제

[legacy-editorial-triage.json](legacy-editorial-triage.json)의 판정은 MINOR EDIT 30, MAJOR REWRITE 317, REPLACE 5, HOLD FOR LEGAL REVIEW 3이다. 모든 기존 문항의 법규 상태는 `NOT_REVERIFIED`이다. [answer-ambiguities.json](answer-ambiguities.json)의 세 SBA와 `MA-CASE-0708`의 수량 누락은 확정 답을 연습시키기 전에 해결한다. CE notification의 Form/email 출처 차이는 `MA-EXP-0051`, `MA-CASE-0795`의 정답 D, `MA-CASE-0349`의 core reasoning·A 해설에도 적용한다. `MA-CASE-0349`의 보류는 해설의 현행 제출경로 충돌 때문이며 정답 B의 law-credit 판단 오류를 뜻하지 않는다.

다음 재작성 단위는 아래 순서가 적절하다. 기존 ID는 보존하고 의미나 정답이 바뀐 사례에 새 ID를 부여한다.

1. **PER09–PER22, MOR01–MOR10, DISC01–DISC08: 32개.** 남은 인력 권한, 실제 업무에 따른 ratio 산정, MOR 업무·시설 승인, 보고 주체를 다룬다. Board 인원·임기 퀴즈인 `MA-EXP-0195`, `MA-EXP-0199`는 실무 판단으로 교체한다. MOR 보고 기한의 서로 다른 trigger는 원문을 해결하기 전까지 합치지 않는다.
2. **RX01–RX08, CII01–CII10, PART01–PART06, REF01–REF08, PMP01–PMP08: 40개.** Original EPCS와 스캔 문서, 응급 oral, partial 사유별 기산점, authorization와 법정 refill 상한, prescribing query와 dispensing submission을 실제 거래에 적용한다. `MA-REV-0025–0038`, `0045–0048`과 같은 결론만 반복하는 초안은 합치거나 다른 조건을 요구한다.
3. **30개 MINOR EDIT 중 해설이 지문과 반대인 사례를 우선 정정.** 예를 들어 `MA-CASE-0255`의 5% 초과 사례에서 A 해설이 5% 이하라고 말하는 문제는 계산 정답과 별개의 설명 오류다. 오답마다 실제 조건이 왜 그 결론을 배제하는지 설명한다. 단순 문법 수정과 의미 변경을 구분해 기록 migration 필요 여부를 결정한다.

## 추가 사례 후보의 우선순위

아래는 **작성 후보**이며 정답이나 법규 적용을 확정한 목록이 아니다. 355개 개별 decision signature, 기존 96개 지문, 이번 46개 decision signature를 비교했다. 기존 2,272개 전체의 지문·보기에도 별도 어휘 탐색을 수행했다. 단어 검색 결과는 의미상 부재의 증명이 아니므로 후보별 전체 corpus 비교를 다시 수행한다. 같은 주제에 기존 문항이 있어도 새로운 사실이 필수 행동을 바꾸면 별도 사례가 될 수 있다.

| 우선 영역 | 확인한 기존 범위 | 새 사례가 되려면 필요한 차이 |
|---|---|---|
| LTCF·terminal illness의 CII partial 경로 | 대표 `MA-EXP-0627`과 `MA-REV-0031`은 fax-as-original 중심이다. PLUS-SC19/20의 LTCF 언급은 해당 예외를 **배제**하는 문장이다. 전체 baseline의 지문·보기에서 `terminally ill`은 발견되지 않았다. 이번 `MA-RW-0031`은 CDTM setting 승인으로 다른 경로이다. | 환자·시설의 적격성, 각 partial 기록, 해당 경로의 기간과 MA overlay 때문에 잔량 공급 결과가 달라지는 사건. 먼저 적용 경계를 공식 DEA/eCFR·MA 근거로 해결한다. |
| DSCSA 의심 제품의 실제 처리 | `MA-EXP-0955/0959/0963`에 exemption·trading partner·suspect/illegitimate 판단이 있지만 paired-case 묶음이다. 기존 96개에는 DSCSA가 직접 명시된 지문·보기가 없다. | 아직 suspect인 단계와 illegitimate 판정 뒤 단계, 실제 공급자·상품식별 정보, 적용 가능한 exemption의 범위가 격리·검증·보고·release 결정을 바꾸는 사건. 시험일의 FDA 시행·유예 상태를 먼저 고정한다. |
| 비거주 약국·central fill·remote processing | `MA-EXP-0163/0867/0995`, `MA-REV-0022/0086`은 허가 및 역할 구별을 다룬다. | 두 시설의 실제 담당 업무·기록 연계·수령 장소·MA 환자 피해 발생을 주고 누가 어떤 조치를 해야 하는지 바뀌는 사례. Patient-requested transfer와 다른 계약·기록 경로를 유지한다. |
| Privacy breach와 접근 요청의 후속 행동 | `MA-EXP-0507/0511/0515/0527`은 breach 관련 paired 사례이다. 기존 96개는 access extension·family pickup·login·문서 보존에 집중한다. | 공개된 정보의 성격·수신자·접근 여부·인지일이 risk assessment와 필요한 통지 경로를 실제로 바꾸는 사건. HIPAA 허용 disclosure와 breach를 같은 뜻으로 다루지 않는다. |
| CQI·serious error·defective preparation의 병렬 의무 | `MA-EXP-0987–1007`, `MA-REV-0094–0096`이 기록·recall 기본 경로를 다룬다. `MA-CASE-1151`은 reporting agency와 사건 종류가 불명확하다. | 환자에게 도달한 오류인지, 추가 ED 관찰인지, 정확 조제된 자체 제조품의 SADE인지, 누가 언제 알았는지에 따라 다른 의무가 작동하는 하나의 사건. 법·규정 trigger 차이를 해결하거나 문제 조건에서 명확하게 분리한다. |
| Compounding·hazardous handling의 실제 중단/출고 판단 | `MA-EXP-0907/0911/0915/0919/0923`, `MA-REV-0090–0093`이 category·시험·BUD·AOR 경계를 다룬다. | source-vial in-use와 finished CSP의 시간, 시험 결과와 사용 전체 기간, 작업 변경 전후 containment가 다음 조치를 달리하는 사례. 숫자만 바꾼 BUD 산술은 새 독립 경로로 세지 않는다. |
| Schedule VI continuation·새 statewide prescribing protocol | 대표에는 보통 refill/transfer와 CDTM 경로가 있으며 기존 `MA-REV-0068`은 minor consent가 모든 제품·protocol 요건을 대체하지 않는다는 일반 경계이다. | 14일 regulation/30일 policy의 적용 관계, 약물 제외, 실제 HIV/STI protocol 대상·검사·follow-up·제품 제한이 공식 자료로 해결된 후에만 작성한다. 미해결 상태를 억지로 하나의 정답으로 만들지 않는다. |

## 약 120개 목표의 집계·검증 방식

먼저 우선 후보 12–18개를 법규 검토까지 마친 작은 단위로 만든다. 각 후보에 `nearest_existing_ids`, `changed_condition`, `changed_required_action`, `exact_authority`, `source_checked_at`, `notes_link`를 기록한다. 기존 사례와 다른 이름·약물·수량만으로는 독립 사례로 채택하지 않는다. [semantic-review.json](semantic-review.json)의 `MA-CASE-0316 ↔ MA-REV-0053`처럼 같은 clozapine 결정을 반복하거나, daily credit cap에 덧셈만 추가한 경우는 새 gap 사례 수에서 제외한다.

정답·모든 오답·한국어 해설을 공식 1차 자료에 연결한 뒤, 별도 reviewer가 동결된 문항 hash를 검토한다. 이 편집·peer 검토와 canonical 독립 감사의 조건은 계속 분리한다. `MPJE-MA-PRE2027`을 적용하고, 2027-03-01 이후 outline은 별도 시험일 버전으로 둔다. 각 배치의 count와 실제 도입된 독립 판단 수를 함께 보고하며 120을 채우기 위한 기계적 변형은 만들지 않는다.
