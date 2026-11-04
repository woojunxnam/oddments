# w4-a-9 두 번째 census 누락 보완 — 통합 전 저자 초안

실제 저자 `/root/notes101_omission_census_author`, 실제 세션
`notes101-omission-census-author-actual-20261104`의 source-only 보완이다.
독립/법규 PASS/문항/canonical release credit는0이며 기존 보류를 해제하지 않는다.

실제 worker commit `0f7270ae9c099eafd69e28d5d10759dbf262ccb3`의 보고서 raw SHA는
`55ff9ea9dd7fc07d88091abedbcfc1fbc6596ed105deeb594e4e9117e1385ec4`이다.
보고서의 정확한 원 omission 문자열2개를 읽고 각 새 claim ID에 SHA로 연결했다.
실제 본문3문단과 현재30개 명제 전량을 읽어 전체 claim/source object를 canonical
그대로 두고 반품·폐기 판단/처리 근거 기록2개만 append했다. census 합계는32개다.
원본문은 수정하지 않았으며 `body.txt`의 UTF-8 SHA는 원 binding과 같다.

반품 근거 기록은 013의 사용 가능 confirmation/evidence,014의 제조사 consultation,
015의 재입고 근거 조회가능성과 별개이다. 폐기 근거 기록도 active inventory 제거와
별개이다. 두 새 명제는 선택한 온도 excursion 대응의 판단·처리 근거 기록만 다루며,
제품의 반품·폐기를 무조건 허용하거나 적법한 권한/절차가 충족됐다고 인증하지 않는다.

공식 Policy2020-05 전문과 247 CMR9.22(4) 및 문맥을 직접 읽었다. 규정은 온도
out-of-range 대응 actions 문서화를 직접 요구하며, 정책 XV.2–5는 평가·제조사 확인·
active inventory 제거와 복귀를 구별한다. 두 원문은 반품·폐기 판단/처리의 '근거'를
독립 필수 data field로 직접 열거하지 않는다. 따라서 본문 명제를 목록에는 추가하되
그 정확한 법적 범위를 확정하지 못한 한계를 각 새 blocker에 남겨 둘 다 SOURCE_BLOCKED로
작성했다. 모든 제품·setting의 동일 법정 근거 field나 새 기한을 만들지 않았다.

원30개 census에는 author SOURCE_BLOCKED9개가 있고, 이번 실제 독립 보고서는
22KEEP/8SOURCE_BLOCKED이다. 두 상태 축은 서로 다르며 원census의 status도 수정하지
않았다. 특히017–020,024와 lot/quantity/repeated-exposure의 기존 보류를 보존했고,
보고서가 KEEP한 AFFECTED-PRODUCT의 원 authorSB metadata도 canonical 그대로 남겼다.
신규2개를 더한 census는23 AUTHOR_SOURCE_CHECKED/11SOURCE_BLOCKED이며 법규 PASS가 아니다.

`sources/`는 실제 감사자의 Policy2020-05 및 CMR9 PDF/text/meta6개 원바이트이다.
PDF raw에서 pdftotext-layout으로 다시 추출한 결과가 retained text와 동일한지,
raw/text/meta SHA와 GET 시작/완료 timestamp를 확인했다. 새 retrieval이라고 표시하지
않는다. Policy adopted2020-06-26/revised2020-10-23, CMR9 Register1536/2024-12-06
표시는 각 조항의 최초 시행일 또는 모든 후속 개정 이력으로 확대하지 않았다.

현재 Job60의 실제 INTEGRATED가 확인되지 않았으므로 native predecessor record,
previousjob/resultdigest를 만들거나 validate_record PASS를 주장하지 않았다.
preparation-index와 proof에 미수행 상태를 명시했다. 실제 통합 통보 후 그 committed
queue/ledger/report/result를 기준으로 최종 versionrecord와 native 검증을 수행한다.
등록은 기존19개 wave 모두 통합된 후 root가 별도 수행한다.

본 branch는 격리된 기존 author tree/commit e2c8502d에서 작성했다. 기존 B19 최종
proposal 및 notes120/final86 prefix를 수정하지 않았고 root/shared queue·ledger·본문·
원census·report·generated·guard도 변경하지 않았다. 새 실제 비저자가 최종32개 전량과
원누락2개 및 상속 법규 보류를 다시 검토해야 한다.
