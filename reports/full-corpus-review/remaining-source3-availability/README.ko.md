# ED/QRE 정의 자료의 접근 가능성 확인

2026-11-05 UTC에 MA-CASE-0785, MA-CASE-0786, MA-CASE-0790의 기존 출처 차단
사유와 공식 자료 locator만 확인했다. 원 stem·선택지·정답·숨은 truth를 읽거나
문항의 법규 판정을 하지 않았다. 기준 원장 SHA는
`2a82ae4e43d77159b6a334d22efd84afca0a64c86278b1156423a36b8d9644a6`다.

**새 공식 원문을 확보했다.** Massachusetts Board of Registration in Pharmacy의
[Policy 2025-02: Definitions](https://www.mass.gov/doc/2025-02-definitions-pdf/download)는
실제 TLS 검증을 유지한 GET에서 200과 3쪽 PDF를 반환했다. 원바이트 SHA는
`6f40a43aa04a9aa528d719b500e8e7995ccfbf7a3ea953062a125fb6a66816cb`이며,
문서에는 `Adopted: 8/7/25`가 인쇄돼 있다. §II.F(2쪽)는 QRE, §II.H(2쪽)는
Serious Disability, §II.I(3쪽)는 Serious Injury 정의를 담고 있다.

[공식 Pharmacy Practice Resources](https://www.mass.gov/lists/pharmacy-practice-resources)의
현재 관찰된 `Policies and Circular Letters` 목록에도 동일한 `2025-02: Definitions`
PDF 링크가 있다. 정책의 채택일과 개별 조항의 법적 시행일은 구분하며, 별도의
시행일·효력·폐지 이력이나 원문항에 대한 적용은 이번 확인에서 판정하지 않았다.

버전 혼동도 보존했다. `247-cmr-200-definitions-and-severability-0` PDF는 200을
반환하지만 모든 쪽에 `DRAFT` 및 `Board review: 4/4/24`가 표시되어 현행 규정으로
쓰지 않았다. 현재 공식 landing이 연결하는 CMR 15 PDF에는 15.02~15.04만 있고
15.01 정의가 없다. 공식 CMR 2 landing은 2013-02-01 문서를 연결한다. 잘못 추정한
목록 URL 2개의 실제 404 응답도 원문·추출문·metadata와 함께 보존했다.

12건의 직접 GET에 대해 raw/text SHA, 실제 조회·실독 시각, HTTP 상태와 문서
구분을 기록했다. 원자료와 범위는 `source-only-report.json` 및 각 `.meta.json`에 있다.

이 결과는 **새 자료의 확보 사실**이다. 기존 세 문항의 HOLD·미판정·출처 차단은
변경하지 않았고, 정답 판정·canonical RELEASED·새 전체 문항 실독 credit는 0이다.
Root가 필요성을 판단한 뒤 별도 실제 fresh 세션에서 원문 전체와 모든 보기·극성·
예외·한국어 해설을 감사해야 한다. 기존 공유 원장·queue·consumer·gate는 수정하지 않았다.
