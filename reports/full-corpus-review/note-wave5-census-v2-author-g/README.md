# C32의 누락 4개를 보완하는 저자 source packet

이 파일들은 `/root/independent_case_g`가 같은 실제 세션에서 작성한 census-only 보완안이다. 대상은 `w3-a-15`, `w3-a-16`, `return-pathways` 세 절뿐이다. 원 본문·기존 66개 claim 전체 JSON·모든 기존 source 객체·원 보고서와 검토 이력은 변경하지 않았다. 새 4개를 추가해 14/27/29개, 총 70개가 되었다.

`parent-inputs/*.json`은 실제 native version record나 registry가 아니다. Root가 현재 metadata를 확인하여 version record를 만들 때 필요한 부모 job/result/report/body/census/ledger binding, 원 claim의 identity mapping, 추가 ID와 정확한 omission SHA를 담는다. 기존 author SOURCE_BLOCKED 7개와 C32 실제 SOURCE_BLOCKED 3개·LEGAL_HOLD 1개는 별도로 보존한다. 반환경로의 C32 claim KEEP 이력과 과거 author SOURCE_BLOCKED 상태를 혼동해 덮어쓰지 않는다.

공식 PDF 세 건은 2026-11-04 08:22 UTC에 normal TLS로 새로 받았고 적용 문장을 직접 읽었다. Printed adoption/revision/publication은 기록했지만 별도 조항의 최초 시행일은 UNKNOWN이다. 이번 새 법규 확인은 누락 4개에 한정하며, 기존 66개를 전부 새로 재감사하거나 모든 제품 stability·USP technical 조건·CII/CIII 포장 허용관계를 해결한 것은 아니다. 연결 질문은 이번 작업에서 NOT_ASSESSED이며 새 claim의 related IDs는 비워 두었다.

`validate_source_packet.py`는 보존 바이트/JSON·정확한 추가분·source SHA와 실제 body를 검사하고, native `validate_record`를 임시 메모리 object에만 호출한다. 등록이나 현재 review credit를 만들지 않는다. G는 이 보완본의 저자이므로 후속 독립 감사에서 제외되어야 한다. Root의 실제 등록 후 다른 실제 reviewer가 전체 본문·전체 70 claim·원 누락·승계 blocker를 재검토하기 전까지 새 COMPLETE/법규 PASS/current credit는 0이다. 보호 16본문·기존 M, PR192의 source37/note31 출판 범위, queue/generated는 변경하지 않았다.
