# 20개 단원·442개 명제의 독립 census·법규 감사

검토일2026-11-04. 실제 nonauthor auditor는 `GPT:/root/independent_notes101_a:20261104`이며 같은 instance를 유지한다. 작성자 선언이나 이전 독립 판정을 복제하지 않고, 현재 본문20개·명제442개 전량을 읽어 개별 판정을 기록했다. Question/canonical credit는0이다.

현재 본문에서 새로운 census 누락은 발견하지 않아 **COMPLETE20개**다. 법규 상태는 **KEEP12단원 / SOURCE_BLOCKED8단원**, claim은 **KEEP428 / SOURCE_BLOCKED14**다. COMPLETE는 모든 법규의 PASS가 아니다.

| SOURCE_BLOCKED 단원 | 명제 수 | 남은 확인 사항 |
|---|---:|---|
| w3-c-7 | 1 | 105CMR700의 influenza-only와 policy의 influenza/COVID 소아상담 예외 관계 |
| w3-c-8 | 1 | 최소MIIS열거 외 제품 expiry/site 등 추가 clinical record의 상세 근거 |
| w3-c-11 | 4 | 제품별 puncture/in-use/BUD/expiry와 시설·인력 compounding 상세 근거 |
| w3-c-12 | 1 | regulation의 mental-health/SUD와 circular 확장 영역의 전체 법적 관계 |
| w3-c-13 | 2 | doxycycline목록/SC·IM-only 및 OTP-only note/SUD-LAI valid-Rx 경계 |
| w3-c-14 | 3 | 모든 개별 LAI의 실제 reconstitution/dose preparation/observation 세부 원문 |
| w3-d-2 | 1 | 날짜 없는 statute·Medicine regulation과 Pharmacy regulation의 PharmD날짜 적용 관계 |
| w3-d-4 | 1 | 현재 Mandatory Disclosure Form과 과거 CE부족 email자료의 효력 관계 |

공식 Massachusetts 규정·정책·circular, Federal Register12th PREP amendment와 ASPR index, CDC VIS, eCFR 관련 조항을 직접 회수하고 해당 전문/조항을 읽었다. 원 raw/PDF·추출text·HTTP retrieval metadata와SHA를 보존했다. 모든 이번 GET은 실제200이며 cache를 live로 표시하지 않았다. 별도 효력일을 확인하지 못한 문서는 그 한계를 각 authority에 적었다. 추가25번 gabapentinPDF는 scanned 문서로 pdftotext가 빈 페이지를 반환하여 authority에 사용하지 않았다.21번 shared-servicePDF도 이 판정의 authority로 사용하지 않았다.

관련33문항의 stem·모든보기·저장key·전체해설과13derived를 실독했다. 본문의 명시 VAX01범위 추가3문항 및 CDTM 연결HTML도 읽었다. 현재 committed source HEAD와 관련 문항의 실제 visible fields를 대조했다. 문항 자체의 독립 canonical release credit를 부여하지 않는다. Glossary4개는 source_hashes 필드가 없으므로 source-hash-bearing item으로 허위 계산하지 않았다.

Root가 strict native inventory로 effective current body와 claim/census 바인딩을 검증한 packet임을 전달했다. Worker는 이를 실제 본문 입력으로 읽고20body UTF8SHA·census raw·unit record·442claim record·현재 committed ledger binding을 전량 독립 대조했다. 현재 커밋의 원본문/active revision에 동일 body가 있는 source bytes도 대조했다. Sparse immutable preimage를 피하려고 loader·guard·inventory를 우회하거나 변경하지 않았다. Body/census/queue/generated 및 원래 보고서는 수정하지 않았다.

각 개별 판정·정확 조항·URL·검토일·버전/효력일 한계·raw/text/metaSHA는 report.json에 기록했다. 입력 원바이트는 assignment.json, visible-input.json, related-context.json에 보존했다. 요약은 구체적인 개별 blocker를 덮어쓰지 않는다.

## Finding 대응 보완 — 같은 감사의 설명 수정

Root의 spotcheck에서 첫 날짜 명제에 PT자격 묶음 설명이 붙어 날짜 입증 이유가 불명확한 점을 지적했다. 날짜 자체는 retained01.pdf의 모든 페이지 footer에 인쇄된 `Adopted:5/4/23; Revised9/7/23;9/4/25`로 확인했다. 같은 원PDF 1쪽을 렌더링해 육안으로 확인한 PNG를 추가했고, 첫 finding과 exact_section을 footer의 직접 근거로 고쳤다. HTTP회수일·채택일·직전개정일과 마지막 개정일을 구별한다.

기존442개 전체의 finding/source mapping도 같은 auditor가 다시 확인했다. 개별 명제마다 대응하는 retained primary text의 literal excerpt와 textSHA를 추가했으며, 모든 인용문이 실제 보존 text에 있는지를 검사했다. 원문 직접 문구와 조건에서 도출한 제한적 해석, 기존 SOURCE_BLOCKED의 추가 한계를 구분한다. 예를 들어 patient identity/expiry screening은 일률적 법정 questionnaire를 새로 만드는 판단이 아니고, 비용 안내에 별도 숫자deadline을 합성하지 않는다. 상세 mapping은 claim-source-mapping-followup.json에 있다.

이는 같은20단원·442명제의 입증 설명 보완이다. 검토 단원·명제·auditor 인원·법규 KEEP/SOURCE_BLOCKED 수·question/canonical credit를 늘리거나 변경하지 않았다. 기존 커밋은 보존하고 후속 증거 커밋을 추가한다.
