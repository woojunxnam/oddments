# notes120-e 독립 노트 완전성·법규 검토

Actual actor/session `/root/independent_notes120_e`, instance `GPT:/root/independent_notes120_e:20261104`의 동일 세션이다. 이전 계약 독서 대기를 새로운 감사자로 부풀리지 않았다. 20개 실제 본문과 428개 원자명제를 전부 읽고 본문 문장·표의 주체, 행위, 수치, 시점, 예외 및 독립 전제를 census에 대조하였다. Q29의 stem, 모든 보기, 정답, 한국어 해설 전체와 derived15 visible 전문을 읽었다. 상세 claim 판단은 `audit-report.json`, 실제 읽은 내용은 `read-input.json`과 `reviewed-context.json`에 있다.

단원 완전성은 COMPLETE18, OMISSIONS_FOUND2이다. b12의 비무균 출발원료 CSP 시설 전제와 검증 전제, b17의 aseptic competency observation이 열거에서 빠져 있다. 가까운 기존 claim을 정확히 지목하고 차이를 omission_mapping에 남겼다. 누락 명제의 법규 정확성은 별도의 current-source 문제이므로 열거 누락을 찾았다고 법규 PASS로 처리하지 않았다.

428 claim 중 KEEP159, SOURCE_BLOCKED269이다. 단원 요약은 KEEP5, SOURCE_BLOCKED13, LEGAL_HOLD2이다. 각 KEEP에는 직접 GET한 공식 원문, exact section, 조회일, 효력일 또는 게시본의 한계, raw/text/meta SHA와 실제 retrieval timestamp가 결박된다. SOURCE_BLOCKED의 개별 문구는 확인하지 못한 명제 범위를 명시한다. 관련 문항을 읽었다는 사실로 canonical/question credit를 부여하지 않으며 둘 다0이다.

공식 MA §39D, 2023-07(2025-02-06 개정), 2020-02, 2023-02(2025-09-04 개정), HD advisory, 2022 media-fill advisory, 2026-03 및 FDA/eCFR 자료를 직접 대조했다. 2026-03은 2023-09를 대체하며 2026-09-03 adopted이다. MA inspection template는 일부 draft/구정책을 인용하므로 현행 법규 정본으로 승격하지 않았다. USP2023 FAQ는 관련 부분을 직접 읽었으나 current795/797 정본 landing GET이403이어서 전체조건·예외·후속개정을 확인하지 못한 명제를 SOURCE_BLOCKED로 두었다.

2025 USC URL은 HTTP200이지만 실제 본문이 Page Not Found인 soft404였다. 최초 진척 메시지의 성공 표현을 즉시 정정하고 이 응답을 법적 권위에서 제외했다. House preliminary URL은 실제404였다. 두 오류와 USP403은 raw/text/meta로 보존했다. 실제 조문이 있는2024 USC edition은 해당 edition 이후 변동을 전부 보증하지 않는 한계를 명시하고 현재 FDA 게시 설명과 교차대조했다. HTTP 성공 상태 자체를 법률 원문 확보로 세지 않았다.

우발 metadata 노출은 audit-report의 review_scope에 개별 Q/derived ID와 필드를 기록하였다. 최초 구조 확인의 exact UTC 시각을 당시 별도 기록하지 않아 미확정이다. 최초 source GET18:15Z 이전 사건임을 명시하였다. 기존 독립감사 report/verdict 값을 읽지 않았으며 일부 날짜·빈 flags·추가 metadata 키 이름을 출력한 사실을 숨기지 않았다. 이후 full original은 프로그램 hash/동등성 계산에만 넣고 metadata 값을 모델에 출력하지 않았다.

Root packet original source8e07b8b8과 current source084336d1을 각각 재현했다. Source-file446개 중 publication.json1개의 실제 byte가 달라졌으며 두 버전을 bindings에 보존했다. Q29 complete-original hash/모든 visible 값, derived15 complete-original hash/모든 visible 값, 관련 ID는 동일하다. Current084336d1의 committed bytes와 일치함을 본인이 확인한 뒤 root HEAD 고정을 해제했다. 이후 다른 감사 증거 commit으로 HEAD가 변해도 검증시점 snapshot을 다른 byte와 같다고 간주하지 않는다.

Sparse worker에서는 누락된 preimage의 full native load_notes를 우회하지 않았다. Root가 strict 검증한 실제 inventory의 raw SHA, 모든 assigned unit binding, base commit의 census 원문·claim canonical SHA, 본문 SHA를 자체 재현하였다. Native validate_result/validate_evidence/committed_evidence는 원래 함수를 그대로 사용한다. 최종 envelope는 실제 evidence commit 이후 /tmp에 작성하며 evidence commit 안에 자기 commit SHA를 넣지 않는다.
