# w3-d-22 두 번째 census 누락 보완 — 실제 parent 통합 전 초안

실제 보완 저자는 `/root/notes101_omission_census_author`, 세션은
`notes101-omission-census-author-actual-20261104`로 기존 보완과 동일하다.
독립/법규 PASS/문항/canonical release credit는 0이다.

실제 비저자 `/root/notes_final_census_b`의 commit
`bf49d56fc5cfd7501a5570696fc97a4d5e929152`에 있는 최종 보고서를 읽었다.
보고서 SHA는 `ce94efe674a296f6da2fc43ea018bc4fef1414169355a0711819fe9a6bc2bbdf`이다.
보고서는 원 17개 명제 모두 KEEP로 판정했지만 다른 두 본문 명제의 미열거 때문에
단원은 OMISSIONS_FOUND/LEGAL_HOLD로 남겼다. 이 저자 초안이 그 상태를 해제하지 않는다.

5문단 본문 전문과 현재17개 claim의 전체 ID/statement/metadata를 읽고,
명제 및 source 객체를 canonical-identical하게 보존한 뒤 2개만 append했다.
`census.json`의 원자수는19이며 원본문은 변경하지 않았다. `body.txt`는 원래
UTF-8 body SHA `3d9bd52beb9e56765c5bcecc5478226dd78ffcc811a6a1797ad63f8e33a84f3a`와 같다.
원 notes120/final86 census·record·index·증거 경로는 수정하지 않았다.

1. 원 환자 이름을 다른 파트너 신원인 것처럼 사용하는 행위는 모르는 DOB·주소를
   창작하는 행위와 별개로 열거했다. 247 CMR9.01(9)의 사기·기만 금지,
   9.16(7)(a)의 처방 대상 환자 profile 및 Policy2020-08 I(A)–(B),II(A)의
   named/unnamed 파트너 경로를 대조했다. 허용된 EPT 표기 자체를 허위로
   취급하지 않으며 9.16(8)의 institutional sterile compounding 예외를 없애지 않는다.
2. EPT에서도 가능한 약물 지시의 안전 검토를 유지하는 명제를 열거했다.
   247 CMR9.17(1) opening,(f),(i),(2)의 reasonable effort에 따른 용량·치료기간 및
   drug/dose/directions 유의한 변경 검토를 대조했다. 모든 지시를 변경해야 한다는
   새 의무나 별도 상담 규칙·시간·수치를 추가하지 않았다.

두 새 명제는 AUTHOR_SOURCE_CHECKED이며 저자 지정 출처 대조를 뜻한다.
원 보고서의 정확한 omission 문자열2개는 각각의 새 claim ID와 SHA로 연결했다.
새 비저자 감사자가 최종19개 전량과 원 누락2개를 다시 검토해야 한다.

`sources/`의 공식 CMR9 및 EPT PDF raw/text/meta6개는 실제 감사자의 원바이트를
보존한 것이다. EPT PDF 전문과 CMR9의 지정 조항·문맥, metadata를 직접 읽었다.
새 retrieval이나 독립 재감사라고 표시하지 않는다. EPT adopted2020-07-31과
CMR9 Mass.Register1536/2024-12-06 표시는 각 조항의 최초 시행일로 추정하지 않았다.
각 URL·정확 조항·raw/text/meta SHA·검토일·효력일 한계는 source manifest에 있다.

현재 실제 job57은 아직 통합되었다고 확인되지 않았다. 따라서 이 초안에는
native reassessment record와 previous job/result digest가 없으며 validate_record를
호출하거나 PASS를 주장하지 않았다. preparation-index와 preservation proof의
통합 확인·native 검증·등록 필드는 false이다. 실제 INTEGRATED parent 통보 후
그 committed 원장·result·report 바이트로 최종 record를 만들고 native 검증한다.
다음 등록도 root가 현재19개 wave 통합을 모두 끝낸 뒤 수행한다.
