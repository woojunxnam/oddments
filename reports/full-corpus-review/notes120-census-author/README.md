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

현재 B의 2단원(w3-d-8, w3-d-22)은 실제 native INTEGRATED job에 binding된
single-unit reassessment record를 작성했다. 나머지 7개는 실제 통합 predecessor가
확정되기 전이므로 native record를 만들지 않았다. `finalize-integrated.py`는
현재 HEAD의 실제 native 상태에서 INTEGRATED인 predecessor만 받아들인다.
`proposal-index.json`은 확정된 record와 미확정 단원을 분리해 기록한다.

정확한 scope를 확정하지 못한 신규 명제는 SOURCE_BLOCKED이다. 특히 CPA의
환자 범위에 관한 본문은 community-specific written referral 조건과 모든 setting의
CPA 범위를 혼동할 수 있어, 16.04(1),(2)의 한계를 새 blocker에 명시했다.
재고 1단위 차이의 원인 조사와 nonsterile-source CSP 시설/검증 및 aseptic
observation은 정확한 현행 공식 문언 대조가 추가로 필요하다.

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

최종 source report/omission 문자열이 바뀌면 실제 최종 INTEGRATED 원보고서의
바이트로만 omission SHA를 확정한다. 새 비저자 감사자가 최종 census 전체와 원래
누락을 재검토해야 한다. 원장·큐·loader/guard·문항·생성물은 수정하지 않는다.
