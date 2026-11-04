20개 단원·1,084개 명제를 같은 실제 GPT 감사 인스턴스가 전부 읽고 개별 판정했습니다. 관련 8문항의 stem·모든 선택지·정답·전체 해설과 118개 파생자료도 전문을 대조했습니다. 이 수는 새로운 감사 인원수나 문항 감사 credit이 아닙니다.

명제 판정은 KEEP 780개, SOURCE_BLOCKED 301개, LEGAL_HOLD 3개입니다. 단원은 KEEP 4개, SOURCE_BLOCKED 10개, LEGAL_HOLD 6개입니다. 4개 단원에서 누락 원자 21개를 발견해 본문 행과 근접 claim ID를 completeness-omission-map.json에 기록했습니다. MA 분류 편입 20개와 단일 codeine의 긍정적 연방II 분류 1개이며, 기존 모든 claim을 KEEP해도 누락을 숨기지 않는 별도 완전성 판정입니다.

법규와 제품 라벨의 범위를 구별했습니다. 현재 성분 schedule은 직접 CFR 조항과 MA700.002 편입 조항을 대조했고, 제형·성분·브랜드는 실제 확보한 제품별 현재 라벨 구획을 읽었습니다. 다른 제품의 비교 PK·상호작용·abuse 경로 설명은 허가된 해당 제품 route의 직접 근거로 대신 쓰지 않았습니다. 정확한 현재 라벨 조회가 실패했거나 법적효과를 뒷받침하지 못하면 보류했습니다. author의 source-checked/census-complete 및 자동 색인 연결은 법규 판단 근거가 아닙니다.

공식 원문의 raw/text/meta와 SHA·실제 수집시각을 보존했습니다. 같은 날 원 GET을 retained한 경우 원 metadata와 시각을 유지했습니다. NLM XML URL에서 HTML이 반환된 경우 실제 형식을 source-integrity-review.json에 명시했으며, HTTP200을 법적 정확성으로 해석하지 않았습니다. 과거 Sonata/Ultracet 라벨은 현재 제품 근거로 사용하지 않았습니다. 시행일을 확인하지 못한 일반 문서는 검토일을 시행일로 바꾸지 않고 한계를 남겼습니다.

전체 보고서는 audit-report.json, 표 형태의 명제 판단은 claim-review-table.json, 관련 자료의 개별 대조는 related-material-review.json에 있습니다. 확정되지 않은 MOR/면적 적용 관계, Butrans/Belbuca 적응증 비교와 현재 제품/권한 범위는 보류 사유를 명시했습니다. 원문·census·ledger·shared queue·generated·guard는 수정하지 않았고 canonical/question credit은 0입니다. 전체 법규 통과나 출시 승인은 아닙니다.
