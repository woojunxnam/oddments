# Final86 census 누락 별도 저자 보완

작성자는 `/root/notes101_omission_census_author`, 실제 세션은
`notes101-omission-census-author-actual-20261104`로 기존 notes101/notes120 보완과 같다.
이 자료는 저자 열거·지정 출처 대조이며 독립 감사·법규 PASS·등록·누락 해소 확정이 아니다.
독립/문항/canonical release credit는 모두 0이고 기존 HOLD/SOURCE_BLOCKED는 보존한다.

실제 Final86 A–E의 10개 누락 단원 본문 전문과 기존 471개 명제를 대조하여
51개 명제만 append했다. 새 전체 census 합계는 522개이다. 기존 claim의 ID,
statement 및 source metadata를 포함한 전체 canonical object와 기존 sources 전체를
보존했다. 원본문을 수정하지 않았고 `bodies/`의 UTF-8 바이트는 원 binding과 같다.

| 단원 | 원명제 | 추가 | 보완 내용 |
|---|---:|---:|---|
| w5-a-12 | 16 | 1 | 비약물 첨가제 평가, SOURCE_BLOCKED |
| recall-classification | 19 | 24 | 행동·분류와 lot/진행상태/실제 위해의 구별·workflow·범위 한계 |
| parallel-duties | 9 | 1 | 해당 QRE 내부 기록의 적극 작성 의무 |
| w1-c-14 | 52 | 1 | 실제 impaired/unsafe practice의 고용주 승인 비면책 |
| appendix-a-2 | 83 | 10 | 명시된 MA CII 9개 및 단일 codeine 연방 CII |
| appendix-a-3 | 17 | 1 | Nabilone MA CII |
| appendix-a-5 | 56 | 3 | 명시된 MA CIII 3개 |
| appendix-a-7 | 79 | 7 | 명시된 MA CIV 7개 |
| appendix-b-5 | 51 | 2 | 두 Abilify LAI formulation 구별·risperidone LAI 행 |
| appendix-b-6 | 89 | 1 | 백신 adverse event용 emergency medication 실제 order 전제 |

신규 51개 중 29개는 AUTHOR_SOURCE_CHECKED, 22개는 SOURCE_BLOCKED이다.
저자 source checked는 법규 KEEP가 아니다. 실제 비저자가 원문 전문과 최종 census
전량, 원래 누락과 carried blockers를 다시 검토해야 한다.

회수 보고서의 5개 omission 문자열은 그대로 SHA로 고정하되 24개 명제로 분해했다.
제품·strength·form·lot·expiry 대조, 격리·전산 차단, 환자·시설·배송 추적,
회수지시에 따른 연락·반환·대체치료, 수량 reconciliation·기록 및 Board/FDA/DSCSA
trigger 검토를 각각 열거했다. 본문은 학습용 workflow이며 모든 recall에 동일 환자
연락 deadline을 부과하지 않는다. 정의 조항과 FDA 안내만으로 이 모든 행위의
보편적 법적 의무를 확정하지 못하여 workflow/action 및 기한 범위 명제는 SB이다.
위험 분류와 lot·진행상태·실제 harm의 구별 3개는 21 CFR7.3(l),(m)과 FDA의
분류·code information 변경 설명을 대조한 개념 구별이다. 환자 위해의 실제 발생을
분류의 전제로 새로 요구하지 않으며 새 시간·기한을 만들지 않았다.

Policy2024-02는 CSP/drugs/pump, 정상 체온·fever 및 전체 infusion의 stability와
compatibility를 명시하나 excipient를 별도 명문으로 열거하지 않는다. 해당 첨가제
명제는 SB로 남겼다. 247 CMR15.03(2)(a),(b)는 QRE의 적극 기록 의무를 직접 정한다.
조문에 있는 24시간 숫자는 해당 본문에 없으므로 새 누락 명제로 덧붙이지 않았다.
247 CMR10.03(1) opening,(g),(k)와 10.06의 Board 권한을 대조해 고용주 승인으로
규정의 사유가 사라지지 않는 경계를 열거했다. 보고기한 OPEN 및 보호조항 HOLD를
수정하거나 해결하지 않았다.

105 CMR700.002(B),(C),(D)의 연방 일정 편입을 각 성분의 21 CFR1308.12/.13/.14
정확 entry와 대조했다. 표에 MA CII/CIII/CIV를 직접 표현한 20개 행만 추가했다.
단일 codeine은 1308.12(b)(1)(i)의 긍정 CII 지정이며 적격 복합제 예외를 복사하지
않는다. 성분 분류가 제품의 현재 공급·자동 대체·모든 administration 권한을 증명하는
뜻은 아니고, 제품별 기존 legal blocker를 해제하지 않는다.

FDA SPL3/11을 직접 대조하여 Maintena의 재구성용 lyophilized powder와 Asimtufii의
prefilled aqueous suspension을 구별했다. 원문에 없는 용량·주기를 새 명제로 만들지
않았다. Risperdal Consta의 Long-Acting Injection/extended-release microspheres 및
공식 NLM Perseris·Uzedy의 extended-release injectable 제형을 대조했다.
Policy2023-02 IV.B는 백신 후 adverse event 관리용 emergency medication의 별도
prescription/standing order를 요구한다. 이를 모든 setting의 emergency 약물에
조건 없이 확대하지 않는다.

`retained-primary-source-manifest.json`과 `sources/`에는 실제 A–E 감사자가 회수한
공식 raw/text/meta를 원바이트로 보존했다. 원 commit/경로, HTTPS URL, 각 SHA,
정확 조항과 2026-11-04 저자 검토일, 개정·효력일 또는 미확정 한계를 기록했다.
새 retrieval이라고 표시하지 않는다. 규정 PDF 인쇄 Register 날짜, SPL effectiveTime,
안내 페이지의 날짜와 개별 법조항 시행일을 구별한다.

`proposal-index.json`은 실제 INTEGRATED jobs51–55의 10개 native predecessor를
바인딩하며 pending은 없다. `combined-index.json`은 기존 notes120 9개 index entry를
canonical-identical하게 보존한 뒤 새 10개만 append한다. 이전 9개 전체 prefix는
commit12e3bb68에서 바이트 불변이며 이전 index SHA는
`ba56186a5d5786004555d92b979c0c0506ce6627b3dcbe9cc1a07de23c8a2f2a`이다.
합친 19개는 기존650개+66개추가=716개 명제이며 신규35 checked/31 SB이다.

`validate-integrated.py`는 root에서 실제 strict 검증한 전체306단원 notes inventory를
명시 API 인자로 사용하고 모든 body SHA를 재확인한다. 실제 validate_record와
변경하지 않은 disk_reader를 사용하며 known-author와 carried blockers를 확인한다.
`check-preservation.py`는 원 claim/source 전량 canonical 보존, omission SHA,
원문 바이트 및 source/report/result/census의 disk==HEAD를 검증한다. 이 author는
queue/ledger/원본문/문항/생성물/loader/guard를 수정하지 않고 register를 호출하지 않는다.

최종 검증에서 19개 모두 native validate_record/disk_reader를 통과했다. 기존650개
canonical 원명제와 모든 기존 source object, 원본문, old9 prefix가 보존됐고 참조
1,746개 파일의 disk==HEAD가 확인됐다. `known-authors-and-carried-blockers.json`은
실제 replacement의 author 제외 이력과 원 author union, carried blocker 수를 남긴다.
`retained-original-byte-check.json`은 새로 보존한 16개 출처의 48개 raw/text/meta가
원래 통합 commit·현재 HEAD 원경로·저자 snapshot 사이에 완전히 같음을 확인한다.
전체306개 body는 notes120 및 Final86의 실제 strict notes snapshot 사이에서도
UTF-8 바이트가 동일하다. 기존 source-only 보고서나 index는 갱신하지 않았다.
