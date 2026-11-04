# notes120-c 실제 독립 원자·법규 검토

실제 검토자는 `/root/independent_notes120_c`, 세션도 같은 값이며 auditor instance는 `GPT:/root/independent_notes120_c:20261104`이다. 배정 branch/job은 assignment.json에 고정했다. 본문·census·ledger·queue·generated·guard를 변경하지 않았고, 이 증거 디렉터리만 작성했다. Canonical release credit와 question audit credit는 각각 0이다.

배정된 현행 본문 20개와 원자 326개 전부를 읽었다. 관련 현재 문항 120개의 stem, 모든 보기, 전체 해설 및 파생 항목 18개의 표시 본문도 전부 읽었다. 실독 목록은 read-log.json, 실제 body/census/claim 결합 및 관련 source file 446개의 git-object raw SHA 대조는 input-verification.json에 남겼다. Sparse tree에 full-source의 이전 preimage가 없어 load_notes를 우회하거나 고친 적이 없다. Controller가 strict native inventory로 검증한 실제 current body packet을 사용했고, 모든 body UTF-8 SHA와 census raw/canonical SHA, 전체 claim canonical SHA를 직접 재대조했다.

완전성은 COMPLETE 19개, OMISSIONS_FOUND 1개이다. 법규 상태는 KEEP 17개, SOURCE_BLOCKED 2개, LEGAL_HOLD 1개이다. 원자 상태는 KEEP 322개와 SOURCE_BLOCKED 4개이다. Inventory 예시의 기존 원자 5개는 모두 독립적으로 KEEP이지만, 본문에 명시된 차이 원인 조사 의무가 목록에 없어 단위는 OMISSIONS_FOUND/LEGAL_HOLD이다. 이 의무를 정의나 significance 평가 원자에 숨기지 않았다. 예시 산술 100+50−40=110, 110−109=1 및 400/10,000=4%도 직접 확인했다.

각 원자 이유는 현재 공식 원문에서 해당 주장에 직접 대응하는 한국어 설명으로 작성했다. 작성자의 AUTHOR_SOURCE_CHECKED 또는 기존 census-complete 표시는 법규 KEEP으로 복제하지 않았다. 숫자·기한·주체·trigger·예외·권한·scope·시계를 문장별로 비교했다. 1304.11의 현행 dispenser count는 (e)(6)이므로 원자 목록의 (e)(3) 인용을 근거에서 바로잡았다. 1317.95의 transfer-for-destruction에는 (a)를 포함해 인용했다. 원래 body/census 자체는 수정하지 않았다.

공식 출처는 2026-11-04에 새 direct GET으로 받은 raw response, 추출 text, metadata를 함께 보존했다. Source-index.json은 URL, final URL, 실제 HTTP status, UTC 조회시각, raw/text SHA를 갖는다. 34건 중 일부는 DailyMed 검색목록으로서 label 발견에만 사용했고 법규 근거로 인정하지 않았다. 실제 cited authorities는 원문 label/공식 법규·정책·기관 안내이다. Retained cache를 live200으로 재표현한 자료는 없다. eCFR의 정확 section URL은 근거에, 실제 조회한 통합 part URL은 retrieval_url에 각각 표시했다. PDF 추출은 pdftotext이며 시각적 PDF 검사는 별도로 시행했다고 주장하지 않는다.

Cloud runtime 및 network skill을 읽고 실제 환경 상태를 확인했다. Firecrawl scrape는 첫 시도에서 Insufficient credits로 실행되지 않았으므로 결과를 증거로 사용하지 않았다. 이후 urllib direct GET을 사용했다. 런타임은 running, filesystem/network unrestricted, VPN false, secret/identity 없음으로 보고되었다.

SOURCE_BLOCKED를 유지한 원자는 five-percent-example의 MA wholesaler 체계·DSCSA·503A interstate/MOU 비교 3개와 w2-d-11의 기관별 DCP/DIR 절차 통합 1개이다. 전자는 해당 별도 법체계의 현행 primary-source 연결고리를 충분히 확보·분석하지 못한 한계이다. 후자는 현재 제공되는 24시간 form 규정과 immediate telephone/7일 written 행정 안내의 모든 기관별 관계를 확정하지 못한 한계이다. 확인한 federal denominator나 직접적인 24시간 의무를 지우지 않으면서 미확인 부분을 통과시키지 않았다.

## 기존 metadata 노출 공개

초기 packet 구조 확인 중 첫 단위 `w3-d-23`의 전체 unit 객체를 출력하면서 JSON pointer `/units/0/unit/independent_content_review`가 함께 노출되었고, 그 안의 기존 KEEP metadata를 보았다. 이전 independent report 원문은 열지 않았다. 이 노출은 controller에게 즉시 알렸다. 정확한 tool 출력시각과 전체 출력 범위가 compaction 이후 현재 기록에 남아 있지 않으므로 정확 시각·모든 subfield를 안다고 주장하지 않는다. 확실한 범위는 첫 unit의 위 metadata 노출이다. 참고할 수 있는 시각은 배정 lease 시각2026-11-04T17:43:08.441321Z와 raw packet 사본 보존 시각2026-11-04T18:02:19.279051796Z이다. 그러나 정확 노출 tool 시각이 보존되지 않아 이 두 시각을 노출의 확정된 상·하한이라고 주장하지 않는다. 사본 보존 시각은 노출 시각 자체가 아니다. `prior_exposure=NONE`이라고 주장하지 않는다.

이후 본문 읽기는 id/title/body와 현재 claim statement/authority/blocker만 투영하여 기존 unit verdict와 reviewer conclusion을 제외했다. 현재 법규 결론은 새 공식 GET의 직접 조항 검토로 작성했다. Raw input packet은 요청대로 보존하되 그 안의 기존 metadata를 새 독립 PASS의 근거로 사용하지 않았다. 원자별 이유와 출처를 독립적으로 다시 작성한 점과 이 노출 한계를 함께 검토해야 한다.

## 관련 문항·파생 항목의 제한

관련 자료는 본문 이해와 누락 탐지를 위해 전부 읽었으며, canonical/question audit를 완료한 것으로 세지 않는다. 정확 record SHA·본문 SHA·해설 인용 및 영향 범위는 collateral-findings.json에 남긴다. MA-EXP-0413–0416은 w3-d-22와 w3-d-23을 모두 연결하며, 주제명만으로 오링크라고 할 수 있다는 초기 추정은 철회했다. 현재 w3-d-23의 protected-care label/family-planning access를 EPT-specific 명명의 독립 법적 근거로 바꾸지 않았다. 그 문항의 EPT 법규 자체에 새 PASS를 부여하지 않는다. 단위 원자와 문항/파생 항목의 상태는 서로 대체되지 않는다.
