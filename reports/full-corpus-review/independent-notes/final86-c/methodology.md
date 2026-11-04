# final86-c 실제 독립 원자·법규 검토

Actor와 session은 `/root/independent_notes120_c`, auditor instance는 `GPT:/root/independent_notes120_c:20261104`로 고정했다. 새 독립 인원을 추가한 것이 아니라 같은 실제 nonauthor 세션을 재사용했다. Job53은 `review-independent-notes-abd680775260cd87`이고 배정은 assignment.json에 원본 그대로 보존했다. Canonical release credit와 question audit credit는 모두0이다. RELEASED 또는 question audit PASS를 주장하지 않는다.

배정된 현행 본문20개와 원자455개를 모두 실제 읽었다. 관련114문항의 원 stem, 모든 보기, key와 전체 해설을 모두 읽었고, 파생8개 표시 본문도 전부 읽었다. 출력이 잘린 곳은 해당 원문을 다시 읽었다. 본문에 명시된 RW0077–0080 및 EXP0223/0224도 포함한다. `w5-a-13`의 추가 `#chapter/counseling-dur` 연결은 strict inventory에서 해당 장의 id/title/body만 추출하여8개 본문 전문을 읽었고 additional-body-link-context.json에 보존했다. 추가 문맥 읽기를 다른 단위의 법규 감사 credit로 세지 않는다.

검토 시점 source HEAD는 `eb74b0f4dd71d413d99d61dd7f40406bf6ebfd6e`이다. 원래 input packet과 related context를 변경하지 않았다. 현재 body UTF-8 SHA, raw census SHA, census unit canonical SHA와455개 claim canonical SHA를 배정 binding에 대조했다. Controller의 실제 strict native inventory raw SHA도 직접 확인했다. Sparse tree에서 과거 full-source preimage가 없다고 load_notes를 우회하거나 수정하지 않았다.

관련 context의 원본 full-record SHA와 표시용 projection SHA는 서로 다른 대상이다. 질문114개 및 파생8개의 원본 모델은 해시 계산에만 사용하고 모델 전체나 기존 grading을 출력하지 않았다. Git object의 실제 full record canonical SHA를 검증한 다음, 표시 projection을 현재 actual body SHA 변환까지 포함하여 재현했다. 관련 source file446개의 review-point raw SHA도 모두 확인했다. 증거는 input-verification.json에 있다.

Root의 증거 작업으로 HEAD가 움직인 사실은 검토 시점을 덮어쓰는 이유가 아니다. 고정된 controller HEAD `8e0346a2aadead973ab67a5fda7948e356a7653e`와 비교하여445개 source file은 실제 bytes/SHA가 같음을 확인했다. 달라진1개는 `site/practice-expansion/publication.json`이고, JSON의 유일한 차이는 `/representative_selection/sha256`이다. 나머지 publication 필드는 같다. 이 차이는 current-context-delta.json에 원래·현재 raw SHA 및 두 selection SHA와 함께 기록했다. 전체446파일이 byte-equal이라고 주장하거나 원래 manifest SHA를 바꾸지 않았다. 본문·문항 표시내용 동등성과 manifest bytes 차이는 별도 사실이다.

완전성은 COMPLETE18개, OMISSIONS_FOUND2개이다. 법규 상태는 KEEP11개, SOURCE_BLOCKED6개, LEGAL_HOLD3개이다. 원자 상태는 KEEP423개, SOURCE_BLOCKED31개, LEGAL_HOLD1개이다. 완전성 판정 자체를 법규 KEEP으로 복제하지 않았다.

새 누락은 parallel-duties의 명시적 내부 QRE 기록 작성 의무와 w1-c-14의 고용주 승인 비면책 경계이다. 각 본문의 정확 인용, 기존 원자에 무엇이 있고 무엇이 없는지, 직접 조항을 review.json의 omissions와 omission_authorities에 기록했다. 본문에 없는24시간이라는 숫자를 새 누락으로 만들어 넣지는 않았다. 기존 명확한 개별 원자의 KEEP도 그대로 분리했다.

`w5-a-13-011`의 경우 현재 본문은 CMEA baseline을 counseling-dur 장에 유지한다고 하지만 실제 연결 장8본문은 상담/DUR/PPI/OBRA이며 CMEA가 없다. Strict inventory에서 현재 `w3-b-19`는 `restricted-sales` 장에 있음을 확인했다. CMEA 법규 자체의 검토와 이 잘못된 현재 cross-reference 명제를 분리하여 후자를 LEGAL_HOLD로 기록했다. 원래 body/link를 수정하지 않았다.

## 공식 자료와 한계

신규 direct GET52건을 실제 수행했다. HTTP200은43건이지만 그중2025 GPO§844 주소는 `Page Not Found`를 반환하는 soft404였으므로 법규 근거에서 배제했다. 실제 내용이 있는 신규200응답은42건, 실패는9건이다. 실패에는 USP 원문/FAQ 두 주소의403이 포함된다. 단순200 또는 inspection template 발견만으로 해당 USP 전문을 읽었다고 주장하지 않는다. 원래 실패 endpoint에 접근통제를 우회하는 방식은 사용하지 않았다.

§844는 실제 내용이 있는2024 USCODE와 현재 제공되는 DEA CMEA 안내를 새 GET으로 확보하여 대조했다.2024판을2026 통합 법전이라고 표현하지 않았다. DSCSA는 다른 실제 worker가2026-11-04T18:37:26.088934Z에 GET한2024 USCODE PDF의 정확 raw/text SHA를 확인하여 같은 날 cache로 보존했다. 이1건은 SAME_DAY_RETAINED_CACHE_NOT_NEW_GET이며 새 조회나2026 현재 통합법전 인증으로 세지 않는다.2026의 모든 DSCSA 적용·예외는 SOURCE_BLOCKED이다.

원래 OOS URL은2006 guidance를 반환했다. 후속 May2022 Revision1 원문을 별도 새 GET으로 확보하고, CGMP chemistry testing 및 비구속적 권고의 범위를 직접 읽었다. 이 제조 guidance를 모든 MA CSP 실패에 자동 이식하는 직접 compendial 적용범위11개는 SOURCE_BLOCKED로 분리했다. 반면 FDA aseptic guidance의 endotoxin control, sterility-test sampling 한계, 별도 potency/container 검사는 실제 해당 문단을 읽어 그 한정된 시험학적 경계의 근거로 사용했다. 이 자료를 current USP 정본이나 모든 약국에 대한 무조건 CGMP 의무로 표현하지 않았다.

현행 Policy2026-03의6쪽 전체, Policy2025-01, 관련 MGL13 및 CMR9/10/14/15/20, CMEA, veterinary, VFD, CLIA, samples의 관련 직접 조항을 읽었다. 날짜·기산점·OR/AND·> 부등호·권고/의무·actor·예외를 원자별 한국어 이유에 직접 대응시켰다. VFD reorder는558.6(b)(3)(xii), extralabel feed 금지는(a)(3)으로 인용을 바로잡았다. 현재 census 자체를 수정하지 않았다.

Source-index.json 및 source별 meta는 실제 URL/final URL, UTC 시각, raw response와 추출 text SHA, 판본·효력일 또는 그 한계, 내용 검증 결과를 기록한다. 새 GET과 보존 cache를 구별한다. PDF text는pdftotext로 추출했으며 별도 시각 PDF 검사를 완료했다고 주장하지 않는다. 사용하지 않은 발견용/과거 문건과 실패/soft404도 그대로 보존했다.

Cloud runtime skill의 기존 지침을 유지하고 이번 작업에서도 실제 environment_status를 확인했다. Running/connected, 현재 observations, unrestricted/enforced networking, secrets/identities 없음으로 보고되었다. 이전 작업에서 Firecrawl credits 부족을 확인했기 때문에 이번 공식 GET은urllib를 사용했다.

## 노출과 독립성 공개

이번20단위에서는 unit의 legacy grading, claim review_status와 independent verdict를 모델에 출력하지 않았다. 그러나 초기 claim 투영에 statement/authority와 함께 census `blocker` 문자열도 출력했다. Nonnull34개이며 일부에는 작성자의 `SOURCE_BLOCKED 유지` 같은 표현이 있었다. 정확한34claim ID와 field 범위는 exposure-disclosure.json에 남겼다. 해당34개는 원census의 author source-gap 체크리스트이며, 본 범위에서 이전 실제 independent 현재원자 verdict의 인용은 없었다. 이는 실제 old independent report 원문 열람과는 다르지만, 완전한 blind/no-prior-exposure라고 주장하지 않는다. 정확한 tool 출력시각은 보존되지 않아 추정하지 않았다.

이전 notes120-c 작업에서는 첫w3-d-23의 unit.independent_content_review KEEP metadata 노출이 있었고 그 이전 methodology에 공개했다. 현재20단위와는 별개이나 같은 실제 세션을 재사용한다는 사실과 함께 숨기지 않는다. 이번 판단은 작성자 status를 복제한 것이 아니라 새 공식 응답, 정확 조항과 적용범위, 전수 누락 대조로 새로 작성했다. 실제로 새 근거로 해결한 기존 source gap과, 기존 source-checked였더라도 직접 적용범위가 불충분해 새로 남긴 source block을 구별했다.

## 변경 범위

커밋 증거는 `reports/full-corpus-review/independent-notes/final86-c/`에만 작성한다. 본문·census·ledger·shared queue·기존 reports·generated·guard는 변경하지 않았다. Native result envelope와 실제 postcommit 검증 기록은/tmp에 두어 worker commit을 자기참조로 왜곡하지 않는다. Native3종, 모든 artifact/source raw/text/meta SHA, full commit range, exact remote40SHA와 clean 상태는 실제 커밋 후 별도로 검사한다.
