# Notes120 누락 census 별도 저자 보완

실제 작성 actor/session은 이전 notes101 보완과 동일하다.
`/root/notes101_omission_census_author` /
`notes101-omission-census-author-actual-20261104`.
이 자료는 독립 감사·법규 PASS·누락 해소 확정·controller 등록이 아니며
독립/문항/canonical release credit는 모두 0이다.

9개 실제 단원의 본문 전문과 원자명제 179개를 읽어 15개만 append했다.
원문 본문은 변경하지 않았고 `bodies/`는 원래 UTF-8 body SHA와 동일하다.
각 기존 claim의 ID/statement/source metadata 전체와 모든 기존 source object의
canonical 내용은 그대로 보존했다. 기존 HOLD/SOURCE_BLOCKED의 해소 권한은 없다.
기존 claim metadata는 필드별 고유값과 각 claim 위치의 인덱스를 사용한
무손실 확장으로도 전량 읽었다. 신규 명제를 원래 명제의 반복으로 만들지 않았다.

`preparation-index.json`은 원래 9개 binding, 원/신규 수, 원명제 보존 확인,
현재 새 census 경로/raw SHA를 기록한다. `prepare.py`는 packet의 body/원자,
HEAD 원 census raw SHA, unit/claim canonical SHA, 기존 source object 보존,
실제 신규 proposition delta를 검증한다. 원자 상태를 추정해 KEEP으로 만들지 않는다.

9단원 모두 실제 native INTEGRATED job47–50의 원보고서·result envelope·binding에
고정한 single-unit reassessment record를 작성했다. `finalize-integrated.py`는
현재 HEAD의 실제 native 상태에서 INTEGRATED인 predecessor만 받아들인다.
`proposal-index.json`은 각 record/census의 정확한 경로와 raw SHA 및
predecessor canonical SHA를 기록하며 pending 목록은 비어 있다.
D의 6개 omission과 E의 2개 omission은 각각의 실제 새 명제와 1:1로 연결했다.
새 전체 census는 합계194개 원자로서 179개 보존과 15개 append로 구성된다.
신규15개 중6개는 AUTHOR_SOURCE_CHECKED,9개는 SOURCE_BLOCKED이며 독립 verdict가 아니다.

정확한 scope를 확정하지 못한 신규 명제는 SOURCE_BLOCKED이다. 특히 CPA의
환자 범위에 관한 본문은 community-specific written referral 조건과 모든 setting의
CPA 범위를 혼동할 수 있어, 16.04(1),(2)의 한계를 새 blocker에 명시했다.
재고 1단위 차이의 원인 조사는 247 CMR9.21(8)(c)의 MOR/ScheduleII perpetual
inventory 의무와 대조했으나, 본문의 숫자 예시가 주체·setting을 특정하지 않은 한계를
SB로 남긴다. 해당 주 규정의 non-resident 및 institutional sterile compounding
범위도 구별했다. 공개 USPFAQ8,87,95,142,44–52,61의 지정 문언을 직접 읽고
새 시설·검증·observation 명제에 raw/text/metadata SHA를 기록했으나
현행 정본 전체의 정확한 기술조건·이후 amendment까지 인증하지 않아 SB를 유지한다.

D의 refrigeration/shipping 원문은 실제 D worker commit의 공식 PDF/text/metadata
원바이트를 보존하고 지정 조항을 다시 읽었다. B의 247 CMR9/16도 실제 감사자의
공식 회수 원바이트이다. 이는 새 retrieval이 아니다. manifest에 원 commit/경로,
HTTPS URL, raw/text/metadata SHA, 조항, 검토일, 효력일 또는 그 한계를 기록했다.

Auto-defrost의 positive duty만 별도 열거하고 기존 예외/Board-approval blocker는
그대로 둔다. 온도 excursion의 제품/lot/수량/반복 노출은 기존의 ‘미검토’ 설명과
구별해 확인 행위 자체를 새 명제로 적고, 정책이 독립 data field를 명시하지 않은
범위 및 개별 제품 안정성 자료의 부재를 SOURCE_BLOCKED로 남겼다. 투여→환자와
교부→provider 통지는 XV.6의 기존 두 교차 누락을 보완한다. 배송 상담은 advisory
권고이며 강행 규정으로 승격하지 않는다. PPA의 accuracy/performance는
247 CMR9.19(3)의 명시 의무를 별도로 열거했다.

최종 source report/omission 문자열은 실제 INTEGRATED 원보고서 원바이트로
SHA를 확정했다. `native-validation.json`은9개 actual `validate_record`와
수정하지 않은 `disk_reader`를 통한 성공 및 carried legal blockers를 기록한다.
원 strict inventory SHA를 다시 검증하고306개 body SHA를 전량 재확인했다.
`historical-byte-check.json`은 모든 native source와 원보고서/envelope/census의
HEAD==disk raw 검증을, `preservation-and-scope-check.json`은179개 원자와 모든
원 source object 보존 및 ownprefix 바깥의 authored diff0을 기록한다.
현재 다음86단위 job이 LEASED이므로 native register의 wave-completion 요건에
따라 root가 해당 wave 완료까지 등록을 기다린다. 이 저자는 register를 호출하지 않았다. 새 비저자 감사자가 최종 census 전체와 원래
누락을 재검토해야 한다. 원장·큐·loader/guard·문항·생성물은 수정하지 않는다.
