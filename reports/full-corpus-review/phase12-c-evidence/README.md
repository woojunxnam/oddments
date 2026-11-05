# Phase12-C 독립 legacy 검토 증거

실제 actor/session: `/root/independent_wave12_c`  
안정된 instance: `GPT:/root/independent_wave12_c:20261104`

지정된 40개 원문 stem, 160개 보기, 저장 키, 한국어 core 및 각 보기 해설을 전문으로 읽었다. 공식 현재 eCFR와 Massachusetts PDF/법령을 직접 수신한 뒤 보기를 독립적으로 참/거짓 판정하고 극성·SATA 조합을 적용하여 저장 키와 비교했다. 원 해설은 권위가 아니라 검토 대상이다. `_statement_truth`, 기존 저자·독립 보고서 및 원장의 기존 판정을 모델에 입력하지 않았다.

보고서: `reports/full-corpus-review/independent-phase12-c-review.json`.

- `official/`: 실제 공식 HTTP 응답 raw, 추출 text, 요청·최종 URL/응답 상태/aware 시각/headers/SHA가 있는 metadata. 실패한 요청과 HTTP200 PageNotFound는 성공한 법규 확인으로 계산하지 않았다.
- `nearest-visible.json`: canonical439/public2349의 stem·보기만 투영한 unigram/bigram TF-IDF 검색. 40개 각각 canonical 최근접, public 최근접 및 다른 family 최근접의 실제 원문·모든 보기를 읽었다. 고유 후보76개에는 이미 배정받아 읽은25개가 포함된다. 점수는 의미상 중복 결론이 아니다.
- `locator-metadata.json`: 원본에서 programmatic projection한 family/source ID만 있다. 기존 판정·숨은 truth를 담지 않는다.
- `build_report.py`: 독립적으로 작성한 명제별 한국어 판정과 criterion별 사실을 직렬화한다. 저장 키는 독립 판정 후 비교한다.
- `measure_nearest.py`: 보이는 질문만 이용한 최근접 후보 측정 코드다.
- `validate_submission.py`: 공유 큐를 쓰지 않는 native post-commit 검증 및 `/tmp/independent-phase12-c-result.json` 생성 코드다.

법규 판단은 40개 YES/KEEP이다. 현실성 결함을 확인한30개는 FAIL/NEEDS_REMEDIATION이며, 나머지10개는 NABP 공개 원문의403 때문에 public-style criterion이 NOT_ASSESSED/SOURCE_BLOCKED다. 전체40개에서 이 미확인 criterion을 PASS로 바꾸지 않았다. eCFR 표시 current-through는2026-11-02이고 실제 조회일은2026-11-04다. MA posted version의 별도 commencement 미확정 한계도 보고서에 남겼다.

원문·키·공유 원장·생성물을 바꾸지 않았다. Canonical audit가 아니며 canonical release credit은0, release eligible은false다. Full repository QA·live notes/source guard·release admission은 실행하지 않았다.
