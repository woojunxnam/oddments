# w5-b-11 최종 census 재감사

최종 본문과 18명제를 다시 검토한 결과 COMPLETE / KEEP다. 이는 16개 기존 claim과 2개 추가 claim 전체를 새로 검토한 결과이며, 저자의 추가 등록만으로 원래 omission HOLD를 해제한 것이 아니다.

원래 누락은 본문이 TIRF와 fentanyl transdermal patch 모두의 CII 분류를 전제하면서 기존 census에서 이를 열거하지 않은 점이다. 추가된 017과 018이 각각 이 분류를 명시하며, 새로 회수한 21 CFR 1308.12(a), (c), (c)(9)의 fentanyl 9801 및 salts 문언과 일치한다. 원래 16개 claim object는 변경 없이 보존되어 있다. 이 단위의 `carried_legal_blockers`는 빈 object이며, 기존 claim-level 법규 HOLD 또는 SOURCE_BLOCKED를 해소한 것은 없다.

FDA TIRF 현행 endpoint 원문도 새로 읽었다. 2024-09-30 생산 중단과 신규 등록 중단, NDA/ANDA 승인이 남는 동안 REMS 유지, 남은 공급의 기존 환자 경로, 제품 목록, certification, outpatient registry와 매 처방·조제의 tolerance 확인 및 inpatient policies/procedures가 명제별 판단 근거다. FDA 페이지는 Content current as of 2024-09-19라고 표시한다. 판정은 게시된 조건부 구조와 과거 공지에 대한 것이며, 2026년 특정 제품의 재고나 모든 신청의 현재 승인 상태를 보증하지 않는다.

현재 관련 18문항의 stem·모든 선택지·key·전체 해설과 RF-C-rems derived 1개를 읽었다. 문항의 다른 제품 보기는 이 노트의 근거 또는 별도 질문 감사 credit로 사용하지 않았다. 원래 omission, final census, reassessment record, current body와 각 claim의 SHA를 대조했다. 관련 문항 18개의 전체 record SHA와 visible fields도 Root context가 지정한 실제 Git commit에서 검증했다.

공식 원문 HTML·추출문·retrieval metadata는 `sources/`, 개별 18명제 판정과 정확한 reassessment_review는 `report.json`에 있다. 동일한 실제 auditor/session/instance를 유지했고 canonical release / question audit credit는 0이다. Loader의 missing-preimage guard를 우회하지 않았으며 변경 경로는 이 evidence prefix뿐이다. 실제 postcommit 검증 및 비커밋 result envelope는 별도 임시 파일로 Root에 전달한다.
