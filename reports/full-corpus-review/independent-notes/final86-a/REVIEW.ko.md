# final86-a 독립 노트 census·법규 감사

실제 동일 감사자 instance `GPT:/root/independent_notes101_a:20261104`. 배정20단원/432원명제, 관련40문항의 모든보기·정답·전체한국어해설,12derived 전문을 읽었다. 새 감사자 수나 question/canonical credit는 추가하지 않는다.

완전성: COMPLETE 19, OMISSIONS_FOUND 1. 단원 법규: KEEP 6, SOURCE_BLOCKED 13, LEGAL_HOLD 1. 기존432명제: KEEP 333, SOURCE_BLOCKED 99. 이 수치는 census 완전성과 법규 판정을 구별한 결과이며, 누락1원자는432에 추가하여 검토 수를 부풀리지 않았다.

| 단원 | 원명제 | KEEP / SB | 완전성 | 단원 법규 |
|---|---:|---:|---|---|
| w4-b-21 | 45 | 19 / 26 | COMPLETE | SOURCE_BLOCKED |
| w4-b-22 | 21 | 15 / 6 | COMPLETE | SOURCE_BLOCKED |
| w4-b-23 | 23 | 22 / 1 | COMPLETE | SOURCE_BLOCKED |
| w4-b-24 | 24 | 11 / 13 | COMPLETE | SOURCE_BLOCKED |
| w5-a-12 | 16 | 16 / 0 | OMISSIONS_FOUND | LEGAL_HOLD |
| w5-a-11 | 10 | 8 / 2 | COMPLETE | SOURCE_BLOCKED |
| w4-c-1 | 8 | 7 / 1 | COMPLETE | SOURCE_BLOCKED |
| w4-c-2 | 21 | 21 / 0 | COMPLETE | KEEP |
| w4-c-3 | 17 | 17 / 0 | COMPLETE | KEEP |
| w4-c-4 | 20 | 13 / 7 | COMPLETE | SOURCE_BLOCKED |
| w4-c-5 | 28 | 17 / 11 | COMPLETE | SOURCE_BLOCKED |
| w4-c-6 | 19 | 6 / 13 | COMPLETE | SOURCE_BLOCKED |
| w4-c-7 | 25 | 13 / 12 | COMPLETE | SOURCE_BLOCKED |
| w4-c-8 | 24 | 24 / 0 | COMPLETE | KEEP |
| w4-c-9 | 16 | 16 / 0 | COMPLETE | KEEP |
| w4-c-10 | 28 | 28 / 0 | COMPLETE | KEEP |
| w4-c-11 | 23 | 23 / 0 | COMPLETE | KEEP |
| w4-c-12 | 27 | 26 / 1 | COMPLETE | SOURCE_BLOCKED |
| w4-c-13 | 19 | 16 / 3 | COMPLETE | SOURCE_BLOCKED |
| w4-c-14 | 18 | 15 / 3 | COMPLETE | SOURCE_BLOCKED |

## 실제 누락과 법규 한계

- `w5-a-12`: 본문은 medication 외 **비약물 첨가제**까지 실제 체온·pump·전체 infusion 기간의 안정성/호환성 평가대상으로 말한다. 원16명제는 drugs간 호환성, CSP/pump, 온도만 열거한다. 이 별도원자를 census 누락으로 기록했다. 공식 Policy2024-02는 all drugs/CSP/pump를 명시하지만 첨가제를 직접 열거하지 않으므로 누락명제의 법적 범위도 SOURCE_BLOCKED다. 누락을 보완하지 않은 단원은 LEGAL_HOLD다.
- `w4-c-12` claim20: ownership transfer의21.08 사전60일 통지와 officer/director·5%초과ownership 변경의21.09 사후14일 통지는 다르다. 본문의 ownership/control 사전절차 일반화는 범위를 명확히 확인하지 못해 SOURCE_BLOCKED다.
- `w4-c-14` claim7:247CMR13.05(12)(e)는 calibration시점의 activity amount를 요구한다. calibration date/time 자체의 별도인쇄를 이 문구만으로 확인하지 못해 SOURCE_BLOCKED다. inner/outer825세부표시도 별도 보류했다.
- USP797 공개 publisher FAQ(2023-12-11)의 직접 설명으로 확인한 좁은명제만 KEEP다. 전체 현행797/659정본과 Tables12–14 전 요건·800 세부PPE/HVAC/DDCD/spill/교육주기·825전문은 확보하지 못했다. 공개FAQ에서4일CRT/10일냉장 등 직접 확인되는 셀과 나머지 미확인 셀을 구별했다. 2022BUD 요약표를 최신정본으로 대체하지 않았다.
- NIOSH2024는 publication2025-103이고2table이며2025-07-17추가MSHI notice를 실제CDC페이지에서 확인했다. NIOSH2023-130은 occupational guidance로 사용하며 이를 현행USP800 모든 의무의 정본으로 표시하지 않는다.
- 503A/B 법문은 실제GovInfo **2024Edition**을 보존했고 현재FDA공식페이지의503A/B비교·outsourcing 설명과 함께 대조했다. 이를2025/2026 consolidated edition이라고 표시하지 않았다. 이후개정 이력 전체의완결증명을 주장하지 않는다. 연방AE는 실제currenteCFR310.305(g)(1)10년을 확인했으며2015FDAguidance의옛(f)번호와구별했다.

## 회수·입력 경계

- 공식62URL 실제HTTPS회수의raw/text/meta를보존했다. 매응답실제UTC,HTTP상태,raw/text SHA는sources/*.meta.json과source-catalog.json에있다. 유효문서·접근실패·soft404를 분리했다.
- GovInfo2025추정URL3개는HTTP200이나같은Page Not Found문서였다.105CMR120응답은HTTP200/0바이트였고NIOSH구주소는meta-refresh뿐이었다. 이응답들을 법적근거로사용하지않았다. USP403/404를성공회수로표시하거나구독접근을우회하지않았다.
- 검토원본은assignment.json/visible-input.json/related-context.json의원bytes다. input-verification.json은원본scratch사본동일성, root strict inventory 원rawSHA, 배정body/census/claim/ledger binding을실제Git objects로독립재현한다. Worker의sparse누락preimage때문에load_notes를실행하거나모킹하지않았다. 이는fullstrictloader를worker가재실행했다는주장이아니다.

캡처sourceHEAD `eb74b0f4dd71d413d99d61dd7f40406bf6ebfd6e`와 현재관찰rootHEAD `8e0346a2aadead973ab67a5fda7948e356a7653e`를구별했다. 두commit의배정20본문/432census원명제/ledger binding과관련40Q·12derived의모든visiblefields가동일했고fullQ·derivedrecordhash도각40/40,12/12일치했다. 전체rootHEAD가앞섰다는이유로원packet을새currentpacket으로다시명명하지않았다.

## 명제별 직접 근거

review.json의432개claim에는각원statement,원recordSHA,한국어독립이유,명제별exactsection,실제보존원문excerpt와문자·줄범위,URL,검토일,문서효력일또는한계,raw/text/metaSHA가있다. 각KEEP의excerpt는해당보존text의실제부분문자열이다. SOURCE_BLOCKED는그원명제의미확인수치·필드·조건을명시한다. 저자의checked분류·기존감사결론은법적증거로승계하지않았다.

본문의표45명제,sourcecontainer21명제,release23명제,label/accountability24명제,pump16명제,version10명제,HD분류·NIOSH·AOR·containment·PPE·DDCD·spill각명제,503A/B권한·ingredient·label·AE·MA등록및핵약국자격/label/record각명제를개별대조했다. Editorialscope경고나chapteranchor는법적근거로계수하지않았다. 본문추가링크는두chapteranchor뿐이며추가questionID는없었다.

변경은이증거prefix만이다. 본문·census·queue·question·generated·보호장치는수정하지않았다. Native postcommit3검증/commit원bytes·manifest/remote40SHA/clean증명은커밋밖envelope와postcommit proof로제출한다.
