# Actual reviewer-authored findings. This is not a source of law and does not import prior verdicts.
ASSESSMENTS = {}
def add(n,key,findings,refs,legal,practice,juris,distractors,cue,combination,dup,action,failed=(),drug='특정 약명이나 schedule 암기보다 이 사례의 법적 행위가 핵심이며 불필요한 약물을 추가하지 않았다.',depth=None):
 ASSESSMENTS[f'MA-EXP-{n:04d}']=dict(expected_key=list(key),findings=findings,refs=refs,legal=legal,practice=practice,juris=juris,distractors=distractors,cue=cue,combination=combination,dup=dup,action=action,failed=list(failed),drug=drug,depth=depth or juris)
add(427,'ABD',[
'민감한 정보의 상담에서도 환자 비밀정보 보호 의무가 유지된다. 접근성 필요가 이를 없애지 않는다.',
'환자가 처방을 적절히 이해하도록 필요한 정보를 제공해야 하므로 언어·청각적 이해 가능성을 고려한다. 특정 통역 방식이 언제나 의무라고 확대하지 않았다.',
'상담 내용은 환자·처방에 대한 전문적 판단으로 정한다. 모든 약에 동일 내용을 기계적으로 요구하는 문구는 틀리다.',
'새 흡입기의 준비·투여·사용 지시와 해당 환자가 이해할 수 있는 전달이 필요하다. 인쇄물만으로 자동 충족되지 않는다.'
],['cmr247_9@9.01(16), 9.18(6)','cmr247_9@9.18(4)–(5)','cmr247_9@9.18(5)(a)–(h)','cmr247_9@9.18(4)–(5)(b)–(c)'],
'저장 ABD를 독립적으로 재산출했다. 개인정보 보호와 환자의 이해를 위한 상담은 함께 적용되며 획일적인 내용 의무는 없다.',
'저시력 환자의 흡입기 수령과 언어·청각 장벽은 실제 상담 상황이다.',
'법령 배경은 있지만 구체적인 서비스 선택·거부·예외 판단 대신 적절한 의사소통 일반론을 고르는 데 머문다.',
'C의 모든 약에 identical content라는 극단만 비선택 보기이며 실제로 혼동할 합법적인 대안이 없다.',
'ABD는 모두 신중한 환자중심 문구이고 C만 regardless of the patient라고 하여 문장 태도로 답이 노출된다.',
'두 사례는 접근성이라는 한 문제로 연결되지만 privacy 보기는 구체적인 공개 상황 없이 덧붙었다.',
'Archive 0425는 같은 사례 변형이다. 현재 default 0611과 canonical 0381은 각각 CII 날짜·요청 시 라벨 확대라는 다른 판단이다.',
'새 흡입기 사용 시 실제로 가능한 상담 방식 두 가지를 제시하고, 환자의 동의·프라이버시·이해 가능성을 함께 따져 선택하게 재작성한다.',
failed=('jurisprudence_reasoning','authentic_distractors','wording_not_guessable','reasoning_not_trivia'),drug='흡입기는 사용 기술 설명의 필요를 만드는 관련 맥락이다.')
add(431,'ABCD',[
'측정 장치의 사용법은 처방 용량·투여법과 맞아야 한다. 단순히 장치를 주었다는 사실만으로 올바른 사용 설명이 끝나지 않는다.',
'모든 liquid medications에 적절한 measuring device를 조제하거나 권고해야 한다. 소아만의 의무가 아니다.',
'상담이나 라벨 표현을 고친다는 이유로 처방 치료 의도를 임의 변경할 수 없다. 적용되는 처방 변경 승인 경로를 확인한다.',
'필요한 투여 기술의 시연은 처방 준비·투여·사용 지시를 환자가 이해하도록 설명하는 방법에 포함될 수 있다.'
],['cmr247_9@9.18(5)(b)–(c), (9)','cmr247_9@9.18(9)','policy2018_01@II.B, III.A.i.e–h, III.B.v–viii, IV','cmr247_9@9.18(5)(b)–(c)'],
'ABCD가 모두 참이다. measuring device 제공 또는 권고 의무와 치료 변경의 승인 요건을 구분했다.',
'액상약의 측정 장치 누락과 라벨 수정 중 용량 변경은 약국에서 발생할 수 있다.',
'B의 명시적 device 의무와 C의 처방 변경 권한은 법적 판단을 요구한다.',
'네 보기 모두 신중한 설명이며 A와 D는 같은 기기 사용 설명을 반복한다. 실제 경쟁하는 잘못된 조치가 제시되지 않는다.',
'모든 보기가 적절한 설명을 권하는 방향이어서 허용 범위를 가르는 구체적 혼동이 부족하다.',
'A/D의 기기 설명 중복과 사례 밖의 일반적 시연 문장이 별개의 판단 수를 늘리지는 않는다.',
'Archive 0429와 같은 사례 변형이다. canonical 0287의 성인 액상약 device 의무와 겹치지만 이 문항에는 dose 변경 권한이 추가된다.',
'액상약의 실제 처방 단위와 측정기 눈금을 제시하고, 라벨 표현 수정과 승인 필요한 용량 변경을 구분하는 경쟁 조치를 설계한다.',
failed=('authentic_distractors','wording_not_guessable','natural_rule_combination'),drug='액상제형은 measuring device 의무를 직접 발생시키므로 적절하다.')
add(435,'C',[
'9.18(10)의 예외는 inpatient setting에서 실무하는 약사에 관한 것이며 병원에서 얻는 모든 처방을 예외로 만들지 않는다.',
'약국이 영업 중인 모든 시간에 상담 이용 가능성을 확보해야 한다. 일반적인 상담 불가 시간대를 지정할 권한은 제시되지 않았다.',
'환자가 stockroom 또는 dispensing area를 통과하지 않고 consultation area에 접근할 수 있어야 한다. 제시된 유일한 경로는 충족하지 못한다.',
'표지뿐 아니라 시각·청각상의 비밀 상담을 위한 충분한 privacy가 필요하므로 줄에 민감한 대화가 들리는 공간은 충족하지 못한다.'
],['cmr247_9@9.18(10)','cmr247_9@9.18(8); 9.19(17)의 제한적 temporary absence와 구별','cmr247_9@9.18(6)','cmr247_9@9.18(6)'],
'정답 C를 재산출했다. 일반 영업시간의 categorical unavailability와 특정 temporary-absence 절차를 혼동하지 않는다.',
'상담실 접근 동선과 상담 가능 시간은 운영 점검으로 타당하다.',
'접근 경로·privacy·setting 예외의 구체적 규정을 적용한다.',
'A의 hospital anywhere, B의 categorically unavailable, D의 sensitive conversation plainly audible은 허용 범위를 과장한다.',
'C만 객관적 동선 결함을 진술하고 다른 보기들은 과도한 면제를 주장한다.',
'공간과 availability는 상담 접근이라는 자연스러운 운영 주제로 연결된다.',
'Archive 0433은 동일 사례/동일 choice text 집합이다. canonical 0419와 privacy·동선 규칙은 겹치나 이 문항은 영업시간과 inpatient 예외를 추가한다. default 0939는 다른 outsourcing 주제다.',
'정상적인 상담실 두 배치와 실제 temporary-absence 절차를 제시하여 동선·privacy·상담 제공 시점을 비교하게 재작성한다.',failed=('authentic_distractors','wording_not_guessable'))
add(439,'AB',[
'상담권 안내 표지는 글자 높이 최소 1/2 inch, MOR명 표지는 최소 1 inch로 서로 다르다.',
'상담권 안내 표지는 처방을 조제하여 교부하는 각 구역 옆 눈에 잘 띄는 곳에 게시해야 한다.',
'문구가 맞아도 최소 11-inch height ×14-inch width를 충족해야 한다. 8×10 inch는 부족하다.',
'표지 의무와 각 처방약 수령인에 대한 상담 offer 및 상담 제공 의무는 별개다.'
],['cmr247_9@9.18(7), 9.19(11)','cmr247_9@9.18(7)','cmr247_9@9.18(7)','cmr247_9@9.18(1), (4), (7)–(8)'],
'AB가 정확하다. 최소 표지 크기, 표지별 글자 크기와 offer 의무를 각각 확인했다.',
'관리자가 두 종류의 표지를 점검하는 장면은 구체적이고 가능하다.',
'8×10 표지와 상담권/MOR의 서로 다른 수치 기준을 실제 공간 조건에 적용한다.',
'C의 문구만 맞으면 크기는 충분하다는 오해와 두 표지의 크기 혼동은 실무상 가능한 준수 오류다. D는 쉬운 distractor이나 유일한 판별 근거가 아니다.',
'AB를 선택하려면 두 규정의 수치와 위치를 알아야 하며 모든 답이 태도만으로 결정되지는 않는다.',
'물리적 표지 크기와 offer 의무를 같은 상담 접근 점검에서 구분한다.',
'Archive 0437은 같은 가족의 표지 사례 변형이다. canonical 0419는 상담 공간의 privacy와 표지 문구로, 크기 비교 결론과는 다르며 default 0823은 ordering 주제다.',
'현재 내용의 법규·현실성 별도 검토 결과를 보존한다. canonical admission/release를 원하면 해당 절차의 새 감사를 받는다.')
add(443,'ACD',[
'새 처방 또는 medication order를 환자/대리인에게 조제·전달하기 전에 prospective DUR를 수행한다.',
'전산 alert는 검토 자료이며 그 자체가 relevance와 무관한 일률적 조제 금지 명령은 아니다. 문제를 평가하고 적절한 조치를 한다.',
'DUR에 대응하여 취한 조치를 약사가 문서화해야 한다.',
'약물-알레르기 상호작용은 합리적으로 파악할 DUR 항목이다. 전산 alert가 없다고 약사의 검토 책임이 사라지지 않는다.'
],['cmr247_9@9.17(1)','cmr247_9@9.17(1)–(2)','cmr247_9@9.17(2)','cmr247_9@9.17(1)(g)'],
'ACD가 참이고 B는 거짓이다. alert의 존재와 실제 임상적 의미 평가·조치 기록을 구분했다.',
'알레르기 정보와 전산 alert를 검토하는 상황은 실제 업무다.',
'검토 시점과 문제 대응 기록은 구체적인 법적 의무이다.',
'유일한 비선택 보기 B는 Every alert/ regardless of relevance라는 극단이다. 실제로 합리적으로 보이는 다른 조치가 없다.',
'ACD는 책임 유지, B만 전산의 무조건적 금지 권한으로 표현되어 단어만으로 제외하기 쉽다.',
'알레르기·전산검토·조치 기록은 한 DUR 흐름으로 자연스럽다.',
'Archive 0441은 같은 사례, default 0451은 profile 정보 수집, canonical 0410은 technician의 unresolved alert 판단 권한으로 다르다.',
'상충하는 alert의 실제 내용과 prescriber 회신을 넣고, 조제 전 해결·기록·위임 가능한 객관 자료수집을 가르는 조치 보기를 만든다.',failed=('authentic_distractors','wording_not_guessable'))
add(447,'ABCD',[
'MassPAT는 다른 약물 정보 검토와 목적이 다르다. allergy·dose·directions 등 적용되는 DUR를 대신하지 않는다.',
'처방의 legitimate purpose·환자관계·authenticity 판단과 final dispensing process validation은 서로 다른 규정상 책임이다.',
'정확한 바코드와 수량은 therapeutic duplication 우려에 대한 적절한 조치를 대신하지 못한다.',
'confidential patient profile은 처방 제시 시 기존 조제약 등 필요한 정보의 immediate retrieval을 지원해야 한다.'
],['cmr247_9@9.15(1), 9.17(1)(b),(f),(g),(i)','cmr247_9@9.04(1), 9.15(2)','cmr247_9@9.17(1)(b), (2)','cmr247_9@9.16(7)'],
'네 보기 모두 참이다. 제품 검증·PMP·DUR·진정성 책임을 하나의 작업으로 합치지 않는다.',
'barcode 확인, 중복 치료, MassPAT 확인은 실제 약국 업무다.',
'각 검토의 목적을 법적으로 구분할 수는 있으나 구체적인 치료 정보나 해결 조치는 제시하지 않는다.',
'모든 보기는 다른 검토를 대체하지 않는다는 일반론이다. 서로 경쟁하는 허용 행위가 없다.',
'ABCD가 모두 책임 유지와 정보 접근을 지지하는 당연한 문장으로 구성된다.',
'B의 진정성 판단은 두 사례에서 문제 된 사실 없이 추가되었고 네 검토의 이름을 나열한 것만으로 새 판단이 생기지 않는다.',
'Archive 0445는 같은 사례 변형이다. default 0691은 PMP query/reporting 관계, canonical 0313은 DUR 대응 기록으로 추가 법적 판단이 다르다.',
'중복 처방의 실제 약·처방자 회신·patient profile 정보를 제시하고, 제품 검증 후에도 남는 특정 조치와 기록을 고르게 재작성한다.',failed=('authentic_distractors','wording_not_guessable','natural_rule_combination'))
add(451,'B',[
'환자 약물치료와 관련된 pharmacist comments를 확보·유지해야 한다. 단일 거래가 끝났다고 관련 우려를 일률 삭제하는 것은 맞지 않는다.',
'REMS 의무 준수와 prescription record·patient profile 등 별도로 적용되는 기록은 다르다. 단일 REMS 허가가 모든 기록을 대체하지 않는다.',
'known allergy/history를 합리적으로 확보·기록·유지해야 하므로 빈 칸은 확인된 negative allergy history가 아니다.',
'관련 profile 정보를 obtain, record, maintain하기 위한 reasonable effort가 필요하다. 의도적인 미검토는 그 요건을 충족하지 못한다.'
],['cmr247_9@9.16(7)(d)','cmr247_9@9.01(21), 9.16(1),(7); 9.18의 적용 의무와 구별','cmr247_9@9.16(7)(b)','cmr247_9@9.16(7)(a)–(d)'],
'B만 참이다. 모든 상담에 별도의 특정 양식이 항상 의무라고 읽지 않고, 실제로 적용되는 각 기록 의무가 REMS와 다르다는 한도로 확인했다.',
'빈 알레르기 칸과 한 전산 차트에서 여러 기록을 관리하는 상황은 타당하다.',
'합리적 정보 확보와 기록 보존이라는 법적 기준이 배경이다.',
'A의 정보 삭제, C의 blank=없음, D의 deliberately unexamined는 실제 합법 대안처럼 보이지 않는다.',
'B만 기록 목적 구별을 권하고 나머지는 정보를 지우거나 무시하게 하여 정답이 노출된다.',
'profile과 REMS 기록은 같은 차트에서 구분할 수 있지만 구체적 REMS·기록 상황이 없어 깊이가 제한된다.',
'Archive 0449는 같은 사례, default 0567은 legitimate purpose, canonical 0284는 흡입제 상담 내용으로 다르다.',
'확인된 allergy history와 확인 불가능한 정보의 기록 방식을 비교하고, 실제 REMS 기록 및 일반 Rx/profile 필드를 제시하여 빠진 기록을 고르게 한다.',failed=('authentic_distractors','wording_not_guessable'))
add(455,'BC',[
'VIS는 특정 예방접종 전에 제공하는 백신 위험·편익 정보로 일반 처방약 CMI와 동일 문서가 아니다.',
'규정은 FDA-approved Medication Guide의 제공을 요구한다. 일반 software leaflet이 자동으로 그 문서를 대신하지 않는다.',
'요구되는 guide는 제품이 환자/대리인에게 dispensed될 때 제공하며 적용 예외를 별도로 본다. 적격 refill도 포함될 수 있다.',
'Medication Guide 제공 규정과 FDA가 정한 개별 REMS/등록 요건은 별개이다. Guide 존재만으로 active enrollment 요건을 단정할 수 없다.'
],['cdc_vis@What is a VIS?; VISs are required by law (42 USC300aa-26)','cfr21_208@208.24(a),(d)–(e)','cfr21_208@208.24(e), 208.26','cfr21_208@208.1, 208.24; fda_rems@How does FDA determine that a medication needs a REMS?; Are REMS permanent?'],
'BC를 독립 산출했다. Guide와 일반 CMI, VIS, 제품별 REMS를 구별하고 refill 제공에는 적용 예외를 인정한다.',
'환자정보 출력을 software CMI로 대체하거나 guide와 REMS를 혼동하는 것은 실제 가능한 업무 오류다.',
'FDA-approved 문서의 제공 시점과 REMS의 별도 제품 요건을 구분해야 한다.',
'CMI/Guide/VIS의 문서 혼동과 REMS 등록 추정은 실제로 생길 수 있는 오해다. A는 쉬우나 유일한 오답 판별은 아니다.',
'Guide의 승인 상태와 refill 적용을 알아야 BC 조합을 결정할 수 있다.',
'동일한 dispensing 때 어떤 환자정보 문서가 필요한지라는 자연스러운 주제이다.',
'Archive 0453은 같은 사례 변형이다. canonical 0403은 agent에 대한 Guide 교부 시점, default 0747은 generic product selection으로 결론이 다르다.',
'현재 검토 결과를 보존한다. 특정 약의 active REMS를 묻는 새 문항을 만들면 그 제품의 현행 REMS를 별도 검증한다.')
add(459,'ABD',[
'PPI 정보 제공 시점은 환자정보 제공에 관한 규정이다. 처방의 refill 유효기간을 바꾸는 규정은 아니다.',
'acute-care hospital/LTCF에서는 첫 투여 전 및 치료 지속 중 30일마다 제공하는 경로가 있다.',
'estrogen-progestogen oral contraceptive는 310.515의 일반 estrogen 경로에서 제외하고 310.501을 적용한다. 모든 estrogen 제품을 한 조항으로 취급하지 않는다.',
'oral contraceptive PPI는 환자에게 조제하는 각 package에 넣거나 함께 교부해야 한다.'
],['cfr21_310@310.501(a),(b)(2), 310.515(b)(3)','cfr21_310@310.501(b)(2), 310.515(b)(3)','cfr21_310@310.515(e), 310.501','cfr21_310@310.501(a)'],
'ABD가 참이다. community 각 package와 institutional first administration/30일 경로 및 제품 범위 예외를 따로 적용했다.',
'community oral contraceptive 교부와 LTCF 계속 치료를 비교하는 장면은 타당하다.',
'제품별 조항과 setting별 환자정보 시점을 적용해야 한다.',
'C는 같은 estrogen이라는 이유로 OC 예외를 놓치는 실제 혼동을 제시한다. refill clock과 PPI clock의 구분도 유의미하다.',
'기관의 30일 주기와 각 package 요건을 알아야 정확한 조합을 고를 수 있다.',
'같은 patient information 의무가 setting에 따라 달라지는 자연스러운 비교이다.',
'Archive 0457은 가족 변형이다. default REV0052도 OC package PPI를 묻지만 MG/VIS 문서 대응이 중심이며 이 문항의 LTCF 30일/310.515(e) 적용은 추가 판단이다. canonical 0169는 compliance packaging이다.',
'현재 검토 결과를 보존하되 REV0052와 공유하는 package-PPI 범위를 신규 학습범위로 중복 계산하지 않는다.',drug='oral contraceptive/estrogen 제품 구분이 규정 적용에 직접 필요하다.')
add(467,'B',[
'PHI는 전자 형식뿐 아니라 종이로 보관·전달되는 identifiable health information도 포함한다. 종이라는 이유의 배제는 틀리다.',
'Security Rule의 ePHI 대상과 Privacy Rule의 보다 넓은 PHI 대상은 구별된다.',
'oral identifiable health information도 privacy 대상일 수 있다. 이메일 동시 전송은 전제가 아니다.',
'거래 종료가 정보 공개 권한을 창설하지 않는다. 해당 정보가 PHI인지 및 허용 사용·공개 근거를 판단한다.'
],['cfr45_160@160.103 definitions Health information/Protected health information; cfr45_164@164.502(a)','cfr45_164@164.302, 164.306(a), 164.500–164.502; cfr45_160@160.103','cfr45_160@160.103 Health information/Protected health information; cfr45_164@164.502(a)','cfr45_164@164.502(a), 164.530(c)'],
'B만 참이다. PHI 매체와 Security/Privacy의 적용 범위를 나누어 검증했다.',
'종이 라벨 폐기와 대기줄에서의 환자정보 대화는 실제 개인정보 보호 상황이다.',
'PHI의 매체 범위는 법적 정의를 적용하는 판단이다.',
'A와 C는 종이·말을 보호에서 통째로 배제하고 D는 모든 약국 정보를 거래 후 public이라고 하여 비현실적으로 넓다.',
'B만 범위를 신중하게 구별하고 세 오답은 매체 배제/모든 정보 공개라는 극단을 쓴다.',
'종이·구두·전자 매체 구별은 같은 privacy 범위의 자연스러운 비교이다.',
'Archive 0465는 같은 사례 변형이다. default 0583과 canonical 0413은 eRx exception과 personnel ratio로 중복되지 않는다.',
'익명화된 라벨, 최소 공개, 우발적 부수 공개 등 실제 경계 사례를 제시하고 매체 자체가 아닌 정보 내용·사용 목적을 판단하게 한다.',failed=('authentic_distractors','wording_not_guessable'))
add(471,'AB',[
'Business associate는 covered entity를 대신하여 billing/claims 등의 PHI 업무를 하는 실제 기능으로 정한다. vendor의 마케팅 이름이 결정하지 않는다.',
'환자의 치료를 위해 정보를 받는 다른 health care provider는 그 치료 공개만으로 BA가 되지 않는다.',
'BA 계약은 covered entity가 하면 금지되는 사용·공개를 일반적으로 허용할 수 없다. 계약은 법보다 넓은 무제한 사용 허가가 아니다.',
'billing은 BA 정의에 명시된 기능이다. billing support라는 명칭을 쓴다는 이유의 배제는 없다.'
],['cfr45_160@160.103 Business associate(1)(i)–(ii)','cfr45_160@160.103 Business associate(4)(i)','cfr45_164@164.504(e)(2)(i)–(ii)','cfr45_160@160.103 Business associate(1)(i)'],
'AB를 재산출했다. BA의 기능과 치료 provider 예외 및 BAA 사용 제한을 별도로 확인했다.',
'보험청구 vendor와 환자를 치료하는 임상가의 역할 구분은 현실적인 계약 점검이다.',
'같은 PHI 공유라도 실제 기능에 따라 BA 계약 요건이 달라진다.',
'C의 any otherwise prohibited use와 D의 vendor 자칭만으로 면제되는 구조는 실제 경계보다 훨씬 과장되어 있다.',
'AB는 기능과 목적을 신중하게 보라는 문장이고 CD는 계약/명칭의 무제한 면제를 주장하여 표현이 답을 드러낸다.',
'외부 업무위탁과 다른 provider의 치료 공개는 자연스러운 PHI 관계 비교다.',
'Archive 0469는 같은 사례 변형이다. current default 0499는 access clock, canonical 0340은 CDTM scope로 다른 결정이다.',
'구체적인 PHI 기능을 하는 두 vendor와 치료 provider를 제시하고 BA 여부 및 필요한 계약 조항을 실제로 구분하게 한다.',failed=('authentic_distractors','wording_not_guessable'))
add(475,'ACD',[
'TPO는 164.501의 정의와 164.506의 허용 범위에 따른다. 단순한 업무 명칭이 임의 활동을 합법화하지 않는다.',
'친구의 기록에 대한 업무 목적 없는 호기심 접근은 기술적 로그인 권한만으로 treatment가 되지 않는다.',
'허용된 treatment 공개에도 적절한 administrative/technical/physical privacy safeguards가 유지된다.',
'실제 treating prescriber와의 처방 명확화는 일반적으로 164.506(c)(2)의 치료 공개로 별도 authorization를 요구하지 않는다. 특별 보호 규정을 무시하는 결론은 아니다.'
],['cfr45_164@164.501 Treatment/Payment/Health care operations, 164.506(a),(c)','cfr45_164@164.502(a), 164.506(c), 164.530(c)','cfr45_164@164.530(c)','cfr45_164@164.506(a),(c)(2)'],
'ACD가 참이다. ordinary permitted treatment communication이라는 범위를 유지하며 호기심 접근과 구분했다.',
'처방자와 clarification 통화 및 직원의 부적절한 조회는 현실적이다.',
'치료 목적 허용 공개와 목적 없는 내부 접근의 근거를 구별한다.',
'유일한 비선택 B가 친구를 궁금해서 조회해도 login이면 treatment라는 노골적인 위반 주장이다.',
'ACD는 허용 범위·보호의 유지라는 신중한 문구이고 B만 curiosity를 합법화하여 key가 보인다.',
'두 사례 모두 같은 시스템의 purpose limitation을 비교한다.',
'Archive 0473은 같은 사례 변형이다. default 0691은 PMP reporting/access, canonical 0370은 profile immediate retrieval을 묻는다.',
'실제 치료팀·billing·직원 품질개선 접근을 함께 제시하고 각 목적과 역할별 허용 데이터 범위를 판별하게 재작성한다.',failed=('authentic_distractors','wording_not_guessable'))
add(483,'B',[
'해당 authorization가 필요한 공개는 유효한 authorization와 허용 범위를 먼저 갖춰야 한다. promoter가 사용한 뒤 사후 결정하는 방안은 맞지 않는다.',
'PHI 매매의 대가와 진료비 청구·보험 지급인 payment는 다르다. promoter의 지급만으로 TPO payment가 되지 않는다.',
'진료 수령 consent는 authorization가 필요한 unrelated marketing에 필요한 동의를 대체하지 못한다.',
'marketing의 실제 목적·금전 관계·적용 예외를 검토한다. treatment support라는 이름만으로 치료 공개가 성립하지 않는다.'
],['cfr45_164@164.508(a)(1),(3)–(4)','cfr45_164@164.501 Payment/Sale of protected health information, 164.508(a)(4)','cfr45_164@164.506(b)(2), 164.508(a)(3)–(4)','cfr45_164@164.501 Marketing, 164.508(a)(3)'],
'B만 참이다. care consent, TPO payment, marketing/sale authorization를 구분했다.',
'외부 promoter가 환자 목록을 요청하고 대가를 제시하는 장면은 가능하다.',
'목적과 remuneration에 따른 authorization 적용은 실제 법적 판단이다.',
'A의 먼저 공개 후 검토, C의 every unrelated promotional use, D의 이름만으로 treatment 성립은 합법적 대안으로 보기 어렵다.',
'B만 지급 개념을 구별하고 나머지가 무제한 또는 사후 허가를 주장해 표현으로 정답을 고를 수 있다.',
'목록 공개와 금전 지급은 같은 거래를 두 측면에서 다룬다.',
'Archive 0481은 같은 사례 변형이다. default 0519는 Part2 consent이고 canonical 0344는 vaccine administration scope다.',
'refill reminder에 드는 합리적 비용 보상과 대가성 제품 판촉을 구체적으로 대비하여 marketing 예외와 authorization 내용을 판단하게 한다.',failed=('authentic_distractors','wording_not_guessable'))
add(487,'BC',[
'환자의 동의 또는 적용되는 164.510(b) 경로로 care에 직접 관련된 정보를 가족에게 제공할 수 있다. 별도의 broad written authorization가 언제나 전제는 아니다.',
'공개 범위는 그 사람이 care/payment에 실제 관여하는 데 직접 관련된 PHI에 한정한다.',
'환자가 있는 경우 agreement/objection/합리적 inference를 검토한다. 가족관계가 환자의 의사를 일률적으로 무효화하지 않는다.',
'단일 Rx pickup 및 가족 신분만으로 무관한 모든 health records 접근권을 얻지 않는다. 다른 personal-representative 권한은 별도 사실이 필요하다.'
],['cfr45_164@164.510(b)(1)–(3)','cfr45_164@164.510(b)(1)(i),(3)','cfr45_164@164.510(b)(2)–(3)','cfr45_164@164.510(b)(1)(i); 164.502(g)의 별도 representative 지위와 구별'],
'BC를 재산출했다. 환자 동의하의 관련 정보 공개와 가족에게 무제한 기록을 제공하는 주장을 구분한다.',
'가족이 처방약을 수령하고 추가 정보를 요청하는 상황은 타당하다.',
'동의와 실제 관여 범위를 적용해야 한다.',
'A는 관련 설명을 모두 막고 D는 모든 무관 기록을 허용하는 양 극단으로 현실적 중간 대안이 없다.',
'BC는 실제 관여와 환자 의사를 존중하는 문장이고 AD만 broad/unrestricted 성격이다.',
'수령에 필요한 정보와 별도 기록 요청은 하나의 encounter에서 자연스럽게 연결된다.',
'Archive 0485는 같은 사례 변형이다. default 0587은 처방의 patient 변경 권한, canonical 0246은 name tag로 법적 결론이 다르다.',
'어떤 가족이 어떤 투약을 돕는지와 환자의 제한적 동의를 특정하고, 요청 데이터별 공개 범위를 고르게 재작성한다.',failed=('authentic_distractors','wording_not_guessable'))
add(499,'B',[
'초기 30일 내 notice 조건으로 최대 추가 30일 한 차례만 연장할 수 있다. vendor가 바쁘다는 이유로 반복 연장하지 못한다.',
'의무 주체인 covered entity가 request를 받은 날 기준이다. 12일 후 BA에게 보낸 시점은 새 ordinary clock의 시작이 아니다.',
'written reasons 및 완료 예정일을 initial 30-day period 안에 제공해야 한다. 기간 경과 후 통지는 허용 연장 조건을 충족하지 못한다.',
'규정은 30 days after receipt를 규정한다. business days라는 추가 한정은 없으며 허용 연장의 30일도 달력일이다.'
],['cfr45_164@164.524(b)(2)(ii)(A)–(B)','cfr45_164@164.524(b)(2)(i); 164.504(e)(2)(ii)(E),(H)','cfr45_164@164.524(b)(2)(ii)(A)','cfr45_164@164.524(b)(2)(i)–(ii)'],
'B가 정확하다. current eCFR는 access 30일, initial period 내 이유·완료일 통지, 추가 최대30일 한 차례를 유지한다.',
'외주 record vendor에게 요청을 늦게 전달하는 실제 행정 지연 상황이다.',
'receipt clock·notice 시점·연장 횟수·business/calendar를 구분하는 실질적 법적 판단이다.',
'vendor handoff와 연장 통지 지연은 그럴듯한 실제 실수이다. 다른 기간 단위를 끌어오는 distractor도 가능하다.',
'30일 규정과 연장 조건을 알아야 B만 선택할 수 있다.',
'외주 전달 지연과 연장 통지는 동일한 access 요청 흐름이다.',
'현재 default MA-REV-0056은 초기30일, 사유·완료일 통지, vendor가 clock을 재시작할 수 없음이라는 동일한 네 결론을 묻는다. 12일 전달 사실만으로 새 결정이 생기지 않는다. canonical 0094는 CII shortage로 다른 주제다.',
'법적 내용은 유지하되 REV0056과 기본 노출을 통합하거나, 요청 범위/부분 거절/접근 방식 등 실제 다른 법적 판단을 요구하는 새 사실로 재작성한다.',failed=('distinct_from_bank',))
add(503,'BC',[
'수정은 affected record를 식별하고 amendment를 append/link하는 방식이다. 원 audit trail을 지워 correction을 숨기는 권한이 아니다.',
'일반 Rx/구매/반환 등 2년 최소 보존과 HIPAA-required documentation의 6년은 각각 적용한다.',
'동일 기록에 여러 의무가 적용되면 모두 충족해야 한다. 짧은 기간 하나를 골라 다른 적용 요건을 없애지 못한다.',
'164.530(j)는 해당 documentation의 최소 보존이며 creation 또는 last in effect 중 늦은 날부터 6년이다. 모든 medical record를 정확히6년째 폐기하는 명령이 아니다.'
],['cfr45_164@164.526(c)(1)','cmr247_9@9.16(1); cfr45_164@164.530(j)(1)–(2)','cmr247_9@9.16(1); cfr45_164@164.530(j)(1)–(2)','cfr45_164@164.530(j)(1)–(2)'],
'BC가 참이다. 6년 기산점은 creation/last in effect 중 늦은 날이며 원 해설의 최소 기간·문서 종류 구분은 이와 모순되지 않는다.',
'약국의 하나의 retention 설정을 모든 문서에 적용하는 실수는 타당하다.',
'기록 종류와 두 최소 보존기간을 구별하는 실제 준수 판단이다.',
'2년/6년 및 최소 보존/정확한 폐기일 혼동이 실제 경계이다. A는 지나치게 쉬운 오답이지만 나머지의 규칙 구분이 있다.',
'BC를 확정하려면 HIPAA-required documentation 범위와 일반 Rx 기록 요건을 알아야 한다.',
'보존과 amendment 추적성은 문서 관리의 인접 주제이다.',
'현재 default MA-REV-0071의 pharmacy retention policy는 일반2년을 HIPAA policy/authorization에 적용하고 six-year documentation으로 교정하는 동일 사실·결론이다. canonical 0424는 out-of-state Rx로 별개다.',
'REV0071과 기본 노출을 통합하거나, 정책 폐지일과 생성일이 다른 자료·부분 amendment 등 새로운 기산점 판단을 요구하는 사실로 바꾼다.',failed=('distinct_from_bank',))
add(507,'ABD',[
'허용되지 않은 PHI 공개는 accidental이라는 이유만으로 breach 검토에서 제외되지 않는다. 정의의 예외 또는 low probability of compromise를 확인한다.',
'bag 회수는 mitigation에 관련되지만 정보의 실제 열람·보유 가능성·수령인 등 다른 risk factors를 자동 증명하지 않는다.',
'규정상 예외 또는 최소 네 요인을 고려한 low probability 근거와 burden-of-proof documentation이 필요하다. 해가 없었다는 미기록 확신으로 대체하지 않는다.',
'PHI breach 대응과 medication error가 QRE에 해당하는 경우의 CQI 통지·기록은 별개 의무이다. 하나의 기록으로 다른 법적 검토가 자동 완료되지 않는다.'
],['cfr45_164@164.402 Breach(1)–(2)','cfr45_164@164.402 Breach(2)(i)–(iv)','cfr45_164@164.402 Breach(2), 164.414(b), 164.530(j)','cfr45_164@164.402–164.414; cmr247_15@15.02(1), 15.03(1)–(2)'],
'ABD를 재산출했다. 사고/회수만으로 breach를 긍정 또는 부정하지 않고 실제 exceptions 및 risk assessment를 남겨야 한다.',
'잘못된 bag 교부와 회수는 실제 patient-safety/privacy 동시 사건이다.',
'breach 정의의 추정·예외·risk assessment와 CQI를 구분한다.',
'C의 undocumented assurance가 assessment를 대체한다는 주장은 그럴듯한 허용 경로가 아니다. 네 요인별 실제 결과나 예외 후보가 없다.',
'ABD는 조심스럽게 평가하라는 문장이고 C만 미기록 확신으로 책임을 끝내려 하여 표현이 답을 노출한다.',
'같은 사건의 privacy와 CQI는 자연스럽게 연결되나 사실적 risk 결과가 빠져 구체적 결론이 요구되지 않는다.',
'Archive 0505는 동일 사례 변형이다. default 0535는 medication return acceptance, canonical 0052는 harm minimization 우선순위로 구분된다.',
'수령인의 역할, 봉투 개봉 여부, 라벨 식별정보와 회수 시점을 넣고 실제 breach exception/low-compromise 평가에 따른 다음 조치를 고르게 한다.',failed=('authentic_distractors','wording_not_guessable'))
add(515,'D',[
'media의 threshold는 한 State/jurisdiction residents가 more than500이다. 정확히500명만으로는 해당 count threshold를 넘지 않는다.',
'501명은 more than500 residents이므로 media threshold를 충족한다. 그 수가500을 넘지 않는다는 문구가 틀리다.',
'개인 통지는 164.404의 별도 의무이며 media 통지는 164.406의 추가 의무이다. media가 individual notices를 대체하지 않는다.',
'Secretary의 contemporaneous reporting route는 500 or more individuals이다. 정확히500도 포함한다.'
],['cfr45_164@164.406(a)','cfr45_164@164.406(a)','cfr45_164@164.404(a),(b), 164.406(a)–(b)','cfr45_164@164.408(b)'],
'D만 참이다. HHS ≥500 individuals와 media >500 residents의 주체·경계가 서로 다름을 확인했다.',
'500명과501명이 한 주에 거주하는 reportable breach는 가능한 사실이다.',
'규정상 경계는 의미 있지만 현재 보기 자체가 threshold를 알려주어 500/501의 산술 비교만으로 상당 부분 답을 고를 수 있다.',
'B의 501 is not more than500은 법적 오해가 아니라 명백한 산술 모순이다. A도 exactly500을 more than500으로 부르는 방식이다.',
'정확히500/501와 more than500/500or more를 보기 자체가 명시하여 법을 몰라도 배제·선택하기 쉽다.',
'HHS·media·individual 통지를 비교하는 주제 자체는 자연스럽다.',
'Archive 0513은 동일 사실과 동일 choice text 집합이다. default 0507은 breach 평가, canonical 0189는 CII partial-fill setting으로 다르다.',
'500명 중 여러 주에 나뉜 거주자 수와 구체적 발견일을 제공하고 각 수신자·기한·범위를 선택하게 하되 보기에 threshold 자체의 산술 답을 쓰지 않는다.',failed=('jurisprudence_reasoning','authentic_distractors','wording_not_guessable','reasoning_not_trivia'))
add(519,'AD',[
'Part2 program/records/lawful holder 정의와 record의 출처를 본다. 약 이름 buprenorphine만으로 모든 pharmacy record가 동일한 Part2 program record가 되지는 않는다.',
'현행2.31(a)(4)(i),(5)(ii) 및2.33(a)(2)는 적격 single consent for all future TPO uses/disclosures를 허용한다. 없다는 주장은 틀리다.',
'SUD counseling notes는 일반 record와 별도 정의·동의 요건이 있다. broad TPO consent와 같은 처리를 단정하지 않는다.',
'TPO 수신자의 HIPAA redisclosure 허용에도 patient에 대한 civil/criminal/administrative/legislative proceedings 이용은 별도 보호가 유지된다.'
],['cfr42_2@2.11 Program/Part2 program/Records/Lawful holder, 2.12(a)','cfr42_2@2.31(a)(4)(i),(5)(ii), 2.33(a)(2)','cfr42_2@2.11 SUD counseling notes, 2.31(b)(1)–(2)','cfr42_2@2.31(a)(4)(iii),(d), 2.33(b)(1)'],
'AD가 참이다. HHS가 명시한 2026-02-16 compliance 이후 현행 텍스트를 적용했다. single TPO consent와 counseling notes/proceedings 보호를 구분한다.',
'community pharmacy의 buprenorphine 처방과 federally assisted SUD program의 record 공유를 비교하는 실제 적용 상황이다.',
'program 지위·record 출처·TPO 동의·별도 notes/proceedings 보호의 현행 법규를 연결한다.',
'B는 과거 제한적 동의 인식을 현행 단일 동의에도 적용하는 오해이고 C는 HIPAA 정렬을 모든 record 동의 통합으로 확대하는 실제 혼동이다.',
'AD 조합은 단일 TPO consent의 허용과 별도 보호를 동시에 알아야 하므로 단순한 긍정/부정 어조로 결정되지 않는다.',
'두 사례는 record 생성·수령 지위에 따른 개인정보 보호 경로 차이를 자연스럽게 비교한다.',
'Archive 0517은 같은 사례 변형이다. default 0483은 HIPAA marketing, canonical 0134는 ADD records로 다른 결정이다.',
'현재 검토 결과를 보존한다. Part2의 소스/지위 판단을 실제 약국이 언제나 program이라는 일반론으로 축소하지 않는다.',drug='buprenorphine은 Part2 자동 적용이라는 실제 오해를 유발하는 적절한 맥락이다.')
add(523,'BCD',[
'current Security Rule은 standards와 required/addressable specifications 및 flexibility를 구분한다. 유용한 모든 feature가 모든 약국의 동일한 구체적 의무라는 뜻은 아니다.',
'보안의 general requirements는 ePHI의 confidentiality, integrity, availability를 모두 포함한다.',
'제안과 시행 중인 규정을 구분해야 한다. HHS current summary도 현행 rule과 별도의 proposed modifications를 분리한다.',
'password만으로 164.308 administrative,164.310 physical,164.312 technical safeguards 전부를 충족했다고 할 수 없다.'
],['cfr45_164@164.306(b)–(d)','cfr45_164@164.306(a)(1)','hhs_security@Summary introduction: current rule and separate HIPAA Security Rule NPRM; cfr45_164@164.306–164.316 current text','cfr45_164@164.308(a)(3)–(5), 164.310, 164.312'],
'BCD가 참이다. proposed rule을 현행 법으로 인용하지 않았으며 required/addressable 구별을 유지했다.',
'password만으로 보안이 끝났다고 생각하는 manager 점검은 가능하다.',
'구체적인 risk assessment나 control 선택 없이 암호 외 다른 safeguards도 필요하고 proposal 효력을 확인하라는 일반 원칙을 고르게 한다.',
'A의 any useful feature automatically mandate for every pharmacy는 과도한 오답이고 BCD는 누구나 신중한 관리 방향으로 고를 수 있다.',
'유일 오답만 any/automatically/every를 쓰고 참 보기는 모두 균형 잡힌 원칙이다.',
'접근·교육·물리 보안은 자연스러운 결합이지만 proposal은 특정 조항·시행일 없이 일반론으로 덧붙었다.',
'Archive 0521은 같은 사례 변형이다. default 0691의 PMP 계정과 canonical 0422의 administration scope는 다른 판단이다.',
'특정 규모 약국의 위험평가 결과와 required/addressable control 후보를 제시하여 어떤 구현·대체조치·문서화가 필요한지 판단하게 한다.',failed=('jurisprudence_reasoning','authentic_distractors','wording_not_guessable','reasoning_not_trivia'))
add(531,'B',[
'미교부 처방약의 RTS는 허용될 수 있지만 manufacturer stock bottle에 되돌리는 것은 금지된다.',
'준비만 하고 교부되지 않은 약은9.13의 RTS 경로이고, 환자에게 이미 조제한 약의 재교부는9.01(5)의 별도 제한을 받는다.',
'RTS container에는 제품명·strength·manufacturer/supplier 또는NDC 및 최초 filling 때 지정한 expiration을 유지한다. 새 container가 이를 제거하거나 expiry를 재설정하지 않는다.',
'RTS에 관한 policy and procedure 의무에는 occasional transaction이라는 면제가 제시되지 않는다.'
],['cmr247_9@9.13(1)(a)','cmr247_9@9.13(1), 9.01(5)','cmr247_9@9.13(1)(b)1–4','cmr247_9@9.13(2)'],
'B가 정확하다. uncollected/never-dispensed와 patient return의 구별, manufacturer bottle 금지 및 원 expiry 유지의 동시 적용을 확인했다.',
'미수령 처방을 RTS하며 container를 고르는 상황은 실제적이다.',
'제조사 bottle 금지와 허용되는 별도 RTS container를 적용하는 명시적 법규 판단이다.',
'A는 약국 통제를 벗어나지 않았으니 제조사 bottle에 되부어도 된다는 실제 혼동이고 D는 소량/비정기 업무 P&P 면제 오해다.',
'B의 custody 구분을 확정하려면 never-dispensed와 previously-dispensed 법적 경로를 알아야 한다.',
'custody·RTS container·label/expiration·P&P는 하나의 작업에 자연스럽게 연결된다.',
'canonical MA-Q-0225는 patient never picked up, medication never left pharmacy control, manufacturer stock bottle에 되붓기라는 같은 사실과 동일한 금지/적정 RTS container 결론이다. 전 choices를 읽었으며 새로운 상황 차이는 충분하지 않다. archive0529는 같은 family 변형, default0843은 inventory count다.',
'canonical0225와 실질 중복을 해소하도록 단순 container RTS 대신 mixed lot recall traceability 등 다른 법적 결정을 요구하는 새 사실로 재작성하거나 대표 한 문항으로 노출을 통합한다.',failed=('distinct_from_bank',))
add(535,'AB',[
'반환 수령 의무와 QRE의 즉시 환자보호·통지·24시간 내 기록 등 별도로 적용되는 오류 대응은 각각 검토한다.',
'자기 약국이 환자에게 오류로 조제한 약은 수령해야 한다. counter를 건넜다는 사실만으로 수령을 거부하지 못한다.',
'자기 약국이 조제한 약이 defective/contaminated로 의심되는 경우도 수령 대상이다. 확정된 patient injury가 전제는 아니다.',
'해당 수령 약은 inventory에 되돌리지 않고 격리·적정 폐기해야 한다. 수령이 resale 허가는 아니다.'
],['cmr247_9@9.01(7); cmr247_15@15.03(1)–(2)','cmr247_9@9.01(7)(a)','cmr247_9@9.01(7)(b)','cmr247_9@9.01(7) 후단'],
'AB가 참이다. error/의심 defect 수령과 quarantine/disposal, 별도의 QRE 대응을 구분했다.',
'잘못 교부된 약을 환자가 가져오고 직원이 반환 금지 원칙을 잘못 적용하는 상황은 타당하다.',
'일반 재조제 제한의 오류 수령 의무 및 수령 후 inventory 금지를 함께 적용한다.',
'crossed-counter이면 무조건 수령 금지라는 오해와 수령 후 RTS가 가능하다는 오해는 실제 서로 다른 경로 혼동이다. injury 보기 C는 쉬우나 핵심 판별이 이것만은 아니다.',
'AB를 결정하려면 수령이 의무인 경우와 resale 금지를 모두 알아야 한다.',
'한 error event의 수령·격리·후속 대응이 자연스러운 순서를 이룬다.',
'Archive0533은 같은 사례 변형이다. default0539는 정상 비결함 반환/collector authorization, canonical0052는 즉시 harm-minimization 우선순위로 결론이 다르다.',
'현재 검토를 보존한다. 오류 약 수령을 general patient drug recycling 허가로 확장하지 않는다.')
add(539,'ABC',[
'일반 controlled-drug receptacle collection은 registration을 collector로 modify하고 허용 장소·방법을 따라야 한다. ordinary pharmacy DEA 등록만으로 충족하지 않는다.',
'9.01(7)의 error/의심 defect 수령과 general collection program 운영은 별도 경로이다. 모든 약국의 public collection 운영을 요구하는 조항이 아니다.',
'collection은 적법 폐기를 위한 경로이며 반환 약의 inventory/재조제 금지 및 collector disposal 요건이 유지된다.',
'properly dispensed and nondefective at dispensing인 약은 동일 조항상 일반 수령 의무가 없다. 해당 error-return 의무를 확대하지 않는다.'
],['cfr21_1317@1317.40(a)–(c), 1317.75','cmr247_9@9.01(7); cfr21_1317@1317.40(a)','cmr247_9@9.01(5),(7); cfr21_1317@1317.40(c)(3), 1317.05(c)(2)','cmr247_9@9.01(7) 후단'],
'ABC가 참이다. state의 특정 수령 의무, 비결함 반환, federal collector authorization를 구분했다.',
'환자의 불필요해진 약 반환 요청과 약국의 receptacle 설치 검토는 실제적이다.',
'주법의 수령 범위와 federal registration modification·collection 방법을 함께 적용한다.',
'error return 규칙을 모든 정상 반환으로 넓히거나 보통 DEA 등록을 collector 권한으로 오인하는 실제 경계가 제시된다.',
'일반 수령 의무 유무와 별도 collector 권한을 구별해야 정확한 조합을 선택한다.',
'환자 반환 요청을 다루는 장소가 public collection을 운영하려는 흐름으로 자연스럽다.',
'Archive0537은 같은 사례 변형이다. default0535는 오류 약 수령/격리, canonical0427은 never-dispensed RTS이므로 서로 다른 custody 경로다.',
'현재 검토를 보존한다. collection 운영 여부와 error-return 수령 의무를 별개로 유지한다.')
add(547,'B',[
'60일은 multi-drug-single-dose package의 최대 공급/BUD 상한이며 각 약의 실제 안정성이나 더 짧은 원 expiration을 보장하지 않는다.',
'치료 변경으로 약을 제거·추가하여 동일 환자에게 재교부할 때 package label을 갱신하고 변경 사항 및 pharmacist를 기록하는 적용 요건이 있다.',
'새 포장은 original manufacturer의 더 짧은 expiration을 연장하지 못한다. 제시된 12일 만료 약에 새60일을 부여할 수 없다.',
'removable cells 각각에 drug name/strength를 식별하는 충분한 label이 필요하다. outer-box만으로 대체하지 못한다.'
],['cmr247_9@9.08(1)(c)–(d),(3)(a),(5)(d)','cmr247_9@9.08(4)(a)2–3,(c),(5); policy2023_01@Return and Repackaging1.b–c,3','cmr247_9@9.08(5)(d); policy2023_01@II.9.d','cmr247_9@9.08(6); policy2023_01@II.10, Return and Repackaging1.c'],
'B가 참이다. 모든 포장에 일률적60일 안정성을 부여하지 않고 원 expiration/적용 stability 제한을 유지한다.',
'같은 환자의 pack repackaging, 짧은 expiry, removable cell label은 실제 compliance-pack 점검이다.',
'BUD 상한과 원 expiry 및 cell 식별 규칙을 적용할 법적 배경이 있다.',
'정답 B는 일반적인 내용·지시 확인이고 A/C는 포장만 바꾸면 약의 안정성이 새로 생긴다는 극단, D는 cell 식별 생략이다. 실제로 경쟁하는 BUD/label 조치가 없다.',
'유일 정답은 안전한 확인 문장이고 오답은 stability 보장/초기화·식별 불필요를 단정한다.',
'CaseA/B는 BUD와 label이지만 B는 stem에 명시되지 않은 therapy change 일반론이라 주어진 12일·cell 사실에 대한 실제 처리 결정을 하지 않아도 선택된다.',
'Archive0545는 같은 사례 변형이다. default0459의30일은PPI이고 canonical0169는CII/III packaging eligibility여서 같은 규칙이 아니다.',
'두 약의 실제 expiry와 pack 변경일을 주고 가능한 BUD와 각 cell label/기록 조치를 구체적으로 선택하게 새 상황을 설계한다.',failed=('authentic_distractors','wording_not_guessable','natural_rule_combination'))
add(551,'BC',[
'sealed outer package만으로 temperature excursion이 없거나 integrity가 유지되었다는 증명이 되지 않는다. 실제 보관·운송의 안정성을 평가한다.',
'potentially recalled RTS는 specific lot가 recall에 포함되지 않는다고 확인할 때까지 조제할 수 없다.',
'never-dispensed RTS, 환자에게 이미 조제된 반환, 배송/반송은 각각 실제 custody와 처방 교부 상태를 확인해야 한다. 모두 같은 재사용 권한이 아니다.',
'common carrier가 관여해도 pharmacy의 포장·운송 안정성 의무 등이 모두 없어지지 않는다. loss 상황의 실제 단계와 적용 신고를 별도로 검토한다.'
],['cmr247_9@9.02(2), 9.01(12); delivery@Refrigerated/Frozen/Other Temperature Sensitive Products (best-practice advisory)','cmr247_9@9.13(3)','cmr247_9@9.01(5),(7), 9.02(1)–(3), 9.13(1)','cmr247_9@9.02(2)–(3); delivery@Lost in Transit (advisory, not a new blanket mandate)'],
'BC가 참이다. advisory의 권고를 일률적 binding 신고 의무로 바꾸지 않고 9.02의 실제 안정성 책임과 구별했다.',
'lot 불명 RTS와 온도 이력이 불명확한 반송은 실제 product-quality 상황이다.',
'9.13(3)의 확인 전 recall RTS 금지와 custody 경로를 구분한다.',
'A의 sealed packaging conclusively temperature와 D의 any loss solely carrier라는 절대 명제는 실제 합법적 선택으로 보기 어렵다.',
'BC만 조건을 확인하라는 신중한 진술이며 AD는 증거·책임을 무조건 단정한다.',
'두 사례 모두 재조제 적합성이나 D는 stem에 없는 carrier loss에 대한 일반 책임 문장으로 별개 상황을 끼워 넣는다.',
'Archive0549는 같은 사례 변형이다. default0859도온도/운송 integrity를 묻지만 본 문항은 RTS specific-lot recall 확인 의무가 추가되어 완전 중복은 아니다. canonical0091은 확인된 ClassII lot recall 처리다.',
'실제 lot 증거, 온도기록·유통 custody, 인도 실패 시점을 제시하고 어떤 물품을 격리/교부할지 또는 추가 증거가 필요한지 판단하게 한다.',failed=('authentic_distractors','wording_not_guessable','natural_rule_combination'))
add(555,'ACD',[
'inner liner는 두 직원이 제거 즉시 봉인하고 봉인한 liner를 열거나 x-ray/analyze/penetrate할 수 없다. tablet count를 위한 개봉도 금지 범위다.',
'봉인 뒤에도 permanent unique identification과 설치·제거·storage/파괴이전 transfer 등 collector 기록 의무가 있다.',
'collection은 적법 폐기를 위한 경로이며 이미 dispensed된 patient medication을 pharmacy saleable inventory로 복구하는 권한이 아니다.',
'mail-back은 적격 law enforcement/collector, 허용 장소·파괴 방법, preaddressed/postage paid/unique package 등 요건을 따라야 한다. 임의 약국 주소·봉투로 대체하지 않는다.'
],['cfr21_1317@1317.60(a)(2),(a)(5),(c)','cfr21_1317@1317.60(a)(5); cfr21_1304@1304.21(a),(c),1304.22(f)(2)','cfr21_1317@1317.40(c)(3),1317.60(c); cmr247_9@9.01(5),(7)','cfr21_1317@1317.40(c)(1),1317.70(a),(c),(e)–(f)'],
'ACD가 참이다. 약국 재고의 약별 count와 수거 liner의 봉인·unique-ID/이동기록을 구분해 확인했다.',
'collector가 liner를 교체하며 inventory나 고가약 회수를 제안하는 상황은 폐기 프로그램의 실제 통제 문제이다.',
'controlled stock inventory와 collection liner의 다른 보안·기록 단위를 적용해야 한다.',
'통상 약별 재고수량을 세는 관행을 liner에 가져오는 오해는 구체적이다. mail-back 수신·package 요건도 별도로 알아야 한다.',
'봉인 후 개봉 금지와 unique liner 기록을 모르고 일반 재고 점검 절차로 추정하면 답이 달라진다.',
'수거 과정의 보안·재고 오해·적법 폐기 방법이 자연스럽게 연결된다.',
'Archive0553은 가족 변형이다. default0839의 initial/biennial inventory 및 canonical0169의packaging 자격은 liner 취급과 다른 결정이다.',
'현재 검토를 보존한다. liner 단위 기록과 약별 재고를 혼합하지 않는다.')
add(563,'B',[
'DEA check digit의 수학적 일치로 current registration·state scope·identity·약사 처방 유효성 판단이 증명되지는 않는다.',
'federal registration/면제와 Commonwealth의 registration 체계는 각각 고려한다. ScheduleVI-only의 DEA 불필요 가능성도 별도로 본다.',
'institutional registration 사용은 적격 individual practitioner의 state authority, 기관 확인, 고용 scope, 기관 승인 및 specific internal code 등 조건을 갖춰야 한다. badge만으로 모든 employee에게 처방권이 생기지 않는다.',
'prescriber는 해당 관할이 허용하는 professional scope와 registration/면제를 충족해야 한다. doctor라는 호칭은 unrestricted drug/patient purpose 권한이 아니다.'
],['cfr21_1306@1306.03(a),1306.04(a); cmr247_9@9.15(2)','cfr21_1306@1306.03(a); mgl94c7@94C§7(a),(f)–(g)','cfr21_1301@1301.22(c)(1)–(6)','cfr21_1306@1306.03(a),1306.04(a); cmr247_9@9.15(2)'],
'B만 참이다. 형식상 유효해 보이는 번호와 실제 연방/주 권한·기관 예외를 구분했다.',
'DEA 번호 검증 및 prescriber scope 확인은 실제 업무이나 badge/doctor만으로 무제한 처방권을 주장하는 확대는 매우 과장되어 있다.',
'각 등록과 scope를 검토할 법적 배경은 있으나 실제 practitioner 직종·등록 상태·치료 행위가 없어 구체적 권한 결론은 요구되지 않는다.',
'any hospital employee merely badge 및 doctor unrestricted는 진짜 자격 경계 사례보다 노골적인 오답이다.',
'B만 서로 다른 체계를 고려하라는 문장이고 A/C/D는 conclusively/any/unrestricted로 범위를 과장한다.',
'번호 진위·주 등록·기관 예외·scope는 관련되나 실제 practitioner 자료가 없어 이름만 열거된다.',
'Archive0561은 같은 사례 변형이다. canonical0168은 구체적 MCSR-VI-only와 DEA 없음의 유효성, default0691은 PMP 계정으로 다른 결정이다.',
'직종·주 면허·MCSR schedule·DEA 또는 기관 code를 실제로 주고 특정 약/환자 목적에 발행 가능한지 비교하게 한다.',failed=('authentic_distractors','wording_not_guessable','reasoning_not_trivia'))
add(567,'BC',[
'보험 승인만으로 legitimate-purpose 우려를 해결하지 않으며 관련 판단·조치의 기록을 지워서는 안 된다.',
'유별난 feature 하나는 legitimate explanation 가능성을 평가할 신호이지 그 자체로 fraud의 확정 증거가 아니다.',
'prescriber의 proper prescribing 책임과 filling pharmacist의 corresponding responsibility가 함께 존재한다.',
'필수 fields가 모두 있어도 usual professional practice/legitimate medical purpose 요건을 별도로 충족해야 한다. 형식만으로 충분하지 않다.'
],['cmr247_9@9.15(2),9.16(7)(d),9.17(2); cfr21_1306@1306.04(a)','cfr21_1306@1306.04(a); cmr247_9@9.15(2)','cfr21_1306@1306.04(a); mgl94c19@94C§19(a)','cfr21_1306@1306.04(a),1306.05(a); cmr247_9@9.15(2)'],
'BC가 참이다. 보험·문서 형식과 legitimate purpose 및 corresponding responsibility를 구분하고 단일 특징으로 환자를 사기라고 확정하지 않았다.',
'형식은 완전하지만 legitimate-purpose concern이 남는 처방은 실제 업무 상황이다.',
'처방의 외형과 실질 유효성은 별도 법적 판단이다.',
'A의 concern 삭제와 D의 모든 fields면 conclusively legitimate은 극단이며 B/C만 신중한 확인을 권한다.',
'기록 삭제·외형만으로 확정하는 오답 표현이 정답 두 문장을 쉽게 드러낸다.',
'두 사례는 legitimacy 우려의 강도와 평가를 비교하지만 실제 red flag 내용이 없어 다음 조치는 추상적이다.',
'현재 default REV0047 및 canonical0162는 facially complete controlled Rx의 unresolved legitimate-purpose evidence를 처방 형식/보험 승인으로 해결하려는 동일 결정이다. CaseB의 unspecified unusual feature만으로 새로운 법적 상황이 충분히 만들어지지 않았다. archive0565도 동일사례다.',
'구체적 환자·처방자·확인 결과를 넣어 해결된 우려와 남은 우려를 구별하고 REV0047/0162와 다른 실제 follow-up 결정을 요구하게 한다.',failed=('authentic_distractors','wording_not_guessable','distinct_from_bank'))
add(571,'ACD',[
'환자 처방 조제, 처방정보 transfer, registrant 간 stock distribution은 목적과 요건이 다른 행위이다.',
'general office stock을 위한 controlled substance는 patient prescription으로 발행할 수 없다. 환자명을 추가해도 목적이 변하지 않는다.',
'환자별 injectable/implant OUD 제품 delivery와 같은 특정 예외는 해당 약·환자·registered location·기록 등 범위 내에서만 적용한다. 일반 office stock 허가는 아니다.',
'registrant 간 공급은 receiving registration, distribution records, 해당 schedule order form 및 활동/수량 조건을 따르는 별도 pathway가 필요하다.'
],['cfr21_1306@1306.04(b),(d); cfr21_1307@1307.11(a)','cfr21_1306@1306.04(b),(d)','cfr21_1306@1306.04(d),1306.07(f)(1)–(6)','cfr21_1307@1307.11(a)(1)(i)–(iv),(b); cfr21_1305@1305.03 introductory requirement; cfr21_1304@1304.22(c)'],
'ACD를 재산출했다. 이름뿐인 patient Rx와 stock 목적의 거래를 구별하고 환자별 delivery 예외를 일반 공급 허가로 넓히지 않았다.',
'진료실 재고를 환자 처방으로 주문하는 요청은 실제 약국의 거래 분류 문제이다.',
'ultimate-user dispensing과 stock distribution의 법적 경로는 구별해야 한다.',
'B의 any patient name이면 office stock이 lawful Rx가 된다는 오답은 과장되어 있고 A/C/D는 별도 요건을 확인하라는 일반 문장이다.',
'세 참 문장은 거래를 구분하고 applicable pathway를 보라는 형태여서 구체적 요건을 몰라도 선택하기 쉽다.',
'C는 어떤 patient-product exception인지 밝히지 않아 실제 사실을 적용하는 대신 예외는 자체 범위라는 동어반복에 가깝다.',
'현재 default REV0073도 physician의 office oxycodone stock을 환자명 Rx로 요청한 후 registration/ordering/record stock transfer를 적용하는 동일 결정이다. specific exception을 특정하지 않은 C는 충분한 새 판단이 아니다. canonical0127은 Form222 POA로 다르다.',
'REV0073과 중복 노출을 줄이고 실제 registrant의 연간 distribution/dispensing units 또는 특정 injectable patient-delivery 조건을 제시해 별도의 거래 허용 결정을 요구한다.',failed=('authentic_distractors','wording_not_guessable','natural_rule_combination','distinct_from_bank'))
add(575,'ABCD',[
'controlled Rx는 drug name/strength/dosage form/quantity/directions 등 필요한 사항을 식별해야 한다. 약물군 이름만으로 대체하는 결론이 아니다.',
'no substitution은 default가 아닌 unique element이며 signature 등 다른 요소로 충족하지 않는다.',
'controlled prescription은 실제 issue/sign 날짜를 쓰고, federal multiple-Rx의 earliest-fill instruction은 별도로 둔다. pickup 날짜로 issue date를 바꾸지 않는다.',
'721.020(D)(4)의 naloxone·EPT 및 지정 public-health 경로의 patient identifier 예외는 특정 요건의 예외이며 일반 필수항목 누락을 무조건 허용하지 않는다.'
],['cfr21_1306@1306.05(a); cmr105_721@721.020(C)–(D)','cmr105_721@721.020(B)(1)–(3)','cfr21_1306@1306.05(a),1306.12(b)(1)(ii); cmr105_721@721.020(D)(2)','cmr105_721@721.020(D)(4),721.070(A)(7),(12)'],
'ABCD가 모두 참이다. 발행일·earliest fill·독립 no-substitution 항목·patient identifier 예외를 각각 확인했다.',
'잘못된 issue date 및 signature를 no-substitution으로 취급하는 두 사례는 가능하다.',
'날짜와 고유 no-substitution field의 실제 규정 적용이 필요하다.',
'네 보기는 모두 올바른 확인 원칙으로 구성되며 D의 구체적 public-health exception조차 예외는 일반 누락과 다르다는 일반 진술이다.',
'모든 문장이 필수정보·독립지시·날짜구별·예외검토를 지지하여 실제 위법하거나 허용되는 대안과 경쟁하지 않는다.',
'D의 EPT/naloxone 예외는 두 사례에 관련 사실이 없으며 actual drug fields도 stem의 문제로 제시되지 않아 별개의 facts를 덧붙인다.',
'Archive0573은 같은 사례 변형이다. default0755는 biologic substitution, canonical0137은 ADD 요건으로 다른 판단이다.',
'실제 처방 record 한 개에 issue date/earliest date/signature/no-substitution/patient identifier를 제시하고 수정 가능한 필드와 새 처방 필요 항목을 고르게 재작성한다.',failed=('authentic_distractors','wording_not_guessable','natural_rule_combination'))
add(579,'C',[
'practitioner는 token/password/biometric을 단독 보유·사용하며 다른 사람이 credentials로 처방을 sign하도록 허용할 수 없다. agent의 준비·전송 역할은 prescriber 서명과 다르다.',
'paper prescription을 scan한 storage image는 처음부터 compliant application으로 생성·서명·전송한 EPCS가 아니다.',
'허용된 변경은 original record와 변경·날짜·authorizing prescriber(해당 시)·responsible pharmacist의 추적성을 유지해야 한다.',
'전자 기기로 받은 모든 image가1311 요건의 EPCS인 것은 아니다. ordinary text-message photo가 자동 충족하지 않는다.'
],['cfr21_1311@1311.102(a),(k); cfr21_1306@1306.05(e)–(f)','cmr105_721@721.010 Electronic Prescription/Electronic Transmission,721.040(C); cfr21_1306@1306.05(e)','policy2018_01@IV.A–D; cfr21_1311@1311.205,1311.210의 기록·전자처방 무결성 요건','cfr21_1306@1306.05(e); cfr21_1311@1311.100(a)–(c); cmr105_721@721.010,721.040(C)'],
'C만 참이다. original transmission category·prescriber signing·permitted changes의 기록을 구분했다.',
'종이 scan 및 text photo를 전자처방과 혼동하는 실제 업무상 수신 상황이다.',
'EPCS 생성·서명·전송 요건과 보관 image는 법적으로 다르다.',
'A의 prescriber credential 대리 사용, B의 retroactively original, D의 every image compliant는 너무 넓은 오답이며 실제 compliant/noncompliant 전송 경계가 없다.',
'C만 원기록·승인 trail을 보존하는 신중한 문장이고 나머지는 무조건 EPCS로 인정하거나 credential을 공유한다.',
'C의 permitted corrections는 실제 correction 사실이 없는 stem에 끼워 넣은 일반 원칙이다.',
'Archive0577은 같은 사례 변형이다. default0583은 format exception, canonical0382는 oral follow-up/caller verification으로 다른 결정이다. canonical0382의 key·현행 적합성은 본 배치에서 평가하지 않았다.',
'전자 수신기록의 인증·서명·전송 정보와 허용 correction 항목을 구체적으로 제공하고 어떤 record가 lawful original인지 판별하게 한다.',failed=('authentic_distractors','wording_not_guessable','natural_rule_combination'))
add(583,'BC',[
'721.070(A)(11)의 문구는 2025-01-01 전 또는 Department가 정하는 후속일이다. past endpoint만으로 영구·보편적 예외를 주장할 수 없으며 실제 연장·다른 예외를 확인해야 한다.',
'전자처방 waiver는 별도 CII no-refill/응급 oral 요건을 없애지 않는다. ordinary oral ScheduleII refill authority는 생기지 않는다.',
'otherwise valid written/oral Rx에 대한 exception-verification relief는 처방 authenticity·legitimate purpose·prescriber authority 판단 면제가 아니다.',
'qualifying temporary technological/electrical failure 예외가 있으면 다른 요건을 충족한 paper Rx가 허용될 수 있다. paper라는 이유만으로 necessarily invalid는 틀리다.'
],['cmr105_721@721.070(A)(11)','cmr105_721@721.070(A)(3),(B),721.060; cfr21_1306@1306.11(d),1306.12(a); mgl94c23@94C§23(b)','cmr105_721@721.070(C); cmr247_9@9.15(2)','cmr105_721@721.020(A),(F),721.070(A)(2); mgl94c23@94C§23(h)(ii)'],
'BC를 재산출했다. A는 현재 LTCF 연장이 실제 없다고 단정한 문장이 아니라 과거 endpoint를 확인 없이 universal exception으로 삼는 명제가 거짓이라는 한도로 확인했다. 현행 extended-date를 새로 인증하지 않는다.',
'outage의 paper 처방과 waiver를 가진 prescriber의 부적절한 CII refill 제안은 실제 format 검토 상황이다.',
'format 예외·CII no-refill·pharmacist의 verification relief와 legitimacy 책임을 서로 구별해야 한다.',
'eRx 예외가 다른 CII 조건까지 없애는지와 exception verification 면제를 처방 전체 확인 면제로 오인하는 것은 구체적인 법적 혼동이다. A는 쉬운 문구이나 핵심 BC 판별만을 대체하지 않는다.',
'BC는 waiver/verification relief의 정확한 범위를 알아야 한다. 단순히 paper면 무효라는 규칙으로 고르면 틀린다.',
'두 사례 모두 eRx 원칙에서 벗어나는 format과 남는 처방 요건의 관계를 묻는다.',
'Archive0581은 같은 사례 변형이다. default0619는 emergency oral의 practitioner→pharmacist 및 central-fill 제한, canonical0068은CSOS ordering으로 다른 판단이다.',
'현재 검토를 보존한다. 실제 LTCF 현행 종료일을 묻는 후속 문항은 Department의 실제 연장 자료를 별도로 확인해야 하며 이 판정을 날짜 인증으로 사용하지 않는다.')
add(587,'BCD',[
'policy는 issue date가 누락된 경우만 add를 허용한다. 이미 적힌 issue date 변경 허가는 아니다.',
'ScheduleII earliest-date-to-be-filled 변경은 policy II.E상 새 처방이 필요하다. pharmacy correction으로 앞당기지 못한다.',
'환자를 다른 사람으로 바꾸거나 prescriber signature를 pharmacy가 추가하는 것은 policy의 never changed/added 항목이다.',
'controlled substance 변경 금지의 generic substitution 예외는 동일한 적법 interchange와 관계된다. 다른 치료 약물로 교체하는 일반 권한이 아니다.'
],['policy2018_01@III.A.i.a,III.B.i','policy2018_01@II.E','policy2018_01@II.A,II.D','policy2018_01@II.B; cmr247_9@9.05'],
'BCD가 참이다. missing issue date의 add와 existing date 변경, earliest-fill 새 처방, patient/signature 변경 금지를 각각 확인했다.',
'가족 환자명 변경·signature 누락 보완·CII 조기수령 요청은 실제 처방 변경 문의이다.',
'정책의 never-change 항목과 허용 add의 예외를 적용한다.',
'누락 날짜 추가와 이미 적힌 날짜 변경 혼동, generic substitution과 therapeutic switch 혼동은 실제 좁은 권한 경계이다.',
'BCD를 확정하려면 허용 correction 목록과 new-Rx 항목을 알아야 한다.',
'모든 선택지가 처방 핵심 필드의 변경 권한이라는 한 작업에 연결된다.',
'Archive0585는 같은 사례 변형이다. default0487은 family PHI disclosure, canonical0383은 CII filing/endorsement로 구별된다.',
'현재 검토 결과를 보존한다. patient 이름 오타의 동일인 정정과 다른 환자로 교체를 혼동하지 않도록 본 문항의 different-family-member 사실을 유지한다.')
add(591,'ABCD',[
'CII strength의 변경은 prescriber consultation 목록에 있다. patient-address 변경에서 prescriber or authorized agent를 허용하는 특정 문구를 strength로 확대하지 않는다.',
'gabapentin은 MA ScheduleVI이나 PMP reporting 대상이다. policy의 non-PMP ScheduleVI-only days-supply 무상담 변경 경로에 넣을 수 없다.',
'모든 change/add에는 날짜, 변경 항목, 해당 시 authorizing prescriber, accepting/making pharmacist의 이름을 기록한다.',
'허용된 missing DEA/MCSR number add는 실제 practitioner를 정확히 식별하는 처방 요건을 없애지 않는다. 임의로 번호를 만들거나 다른 사람의 번호를 쓸 수 없다.'
],['policy2018_01@III.A.i.c.ii,III.A.i.g','policy2018_01@III.C.iii.a; pmp_reporting@Who must report?; Gabapentin prescriptions filled at a VA facility; cmr105_700@700.012(A)(1),(C)(8)','policy2018_01@IV.A–D','policy2018_01@III.A.i.d,III.B.iv,III.C.i; cmr247_9@9.15(2)'],
'ABCD가 참이다. CII 임상필드와 agent의 주소 확인 범위를 따로 적용하고 gabapentin의 ScheduleVI/PMP 두 지위를 함께 확인했다.',
'office employee에게 strength를 확인하고 gabapentin days-supply를 늘리려는 업무는 실제 가능한 요청이다.',
'동일 정책 안에서 prescriber/agent 권한이 필드별로 다르고 non-PMP 예외가 있다는 좁은 경계를 적용한다.',
'비선택 보기가 없다는 이유만으로 자동 실패시키지 않았다. 각 명제는 CII agent 권한·VI PMP 배제·실제 prescriber 확인이라는 오해 가능한 구체적 경계를 요구한다.',
'네 보기 모두 참이어도 agent가 모든 CII 변경을 승인하거나 ScheduleVI면 전부 non-PMP라는 지식으로는 key를 얻지 못한다.',
'변경 요청의 승인 주체·drug reporting 지위·변경 기록이 한 workflow에 자연스럽게 연결된다.',
'Archive0589는 같은 사례 변형이다. default0735는 protected-care label identity, canonical0122는 MA VI에 federal controls를 잘못 수입하는 문제라서 본 문항의 no-consultation days-supply 경계와 다르다.',
'현재 검토를 보존한다. gabapentin의 federal unscheduled/MA VI/PMP 대상이라는 서로 다른 분류를 하나로 합치지 않는다.',drug='gabapentin의 PMP 지위가 예외 적용을 실제로 바꾸므로 약물 선택이 법적 판단에 중요하다.')
add(595,'B',[
'전자처방이라도 final dispensing process validation은 licensed pharmacist의 책임이다.',
'lawful partial fill은 original authorized quantity의 일부를 공급하는 구조이다. 별도 refill authority를 새로 창설하지 않는다.',
'새로운 적법한 ScheduleII prescription은 old Rx refill과 다른 authorization다. 이를 같은 거래로 취급할 수 없다.',
'ScheduleII refill은 금지되며 prescriber가 two refills를 적어도 금지가 없어지지 않는다.'
],['cmr247_9@9.04(1)','cfr21_1306@1306.12(a),1306.13(a),(b)(1)–(2)','cfr21_1306@1306.12(a)–(b); mgl94c23@94C§23(b)','cfr21_1306@1306.12(a); mgl94c23@94C§23(b)'],
'B만 참이다. original partial quantity·new prescription·refill을 구별하고 EPCS에서도 final validation 책임을 유지한다.',
'oxycodone 처방의 refill 표기와 partial fill의 전산 분류 혼동은 실제 약국 업무다.',
'CII no-refill 원칙을 실제 prescriber 표기 및 부분 공급 분류에 적용한다.',
'처방자 refill 수가 법을 대체하는지, partial을 refill로 차감하는지, 새 처방을 refill로 부르는 혼동은 실제 시스템·용어에서 생길 수 있다.',
'B를 확정하려면 partial supply의 original authorization와 CII no-refill 구조를 알아야 한다. 단순 drug schedule 명칭 퀴즈가 아니다.',
'처방 표기·공급 단위·최종 검증은 한 CII 처방 처리 흐름이다.',
'Archive0593은 같은 사례 변형이다. default0667은 ScheduleIV later refills/partial record, canonical0032는ScheduleIV oral refill addition으로 서로 다른 법적 허용 범위다.',
'현재 검토 결과를 보존한다. partial fill을 실제로 허용하는 구체적 요건과 기간은 해당 pathway 문항에서 따로 검증한다.',drug='oxycodone의 CII 지위가 refill 금지를 실제 결정한다.')
add(599,'AB',[
'90-day quantity가 허용되는 category라도 prescription 자체가 유효해야 한다. 별도 validity 조건을 치유하지 않는다.',
'written/electronic ScheduleII Rx는 issuance 후30일에 invalid해진다. alternative order pathway가 없는40일 첫 제시는 이 한도를 넘는다.',
'23(d)의90-day supply와23(a)의30-day validity는 다른 조건이다. quantity allowance가 validity를90일로 늘리지 않는다.',
'validity는 date of issuance에 연결된다. 첫 pickup 시도일이 새30일 기산점이 아니다.'
],['mgl94c23@94C§23(a),(d)','mgl94c23@94C§23(a); cmr247_9@9.04(10)','mgl94c23@94C§23(a),(d)','mgl94c23@94C§23(a); cmr247_9@9.04(10)'],
'AB가 참이다.40일은 day-count 경계와 무관하게30일을 초과하며 quantity와 validity를 분리했다.',
'오래된 CII 처방으로90일분을 처음 받으려는 환자와 staff의 양/기간 혼동은 실제적이다.',
'주법의 별도 supply·validity 시계를 동시에 적용한다.',
'90-day supply를90-day fill window로 옮기는 오해와 첫 pickup에서 clock을 재시작하는 오해는 실제 기산점 혼동이다.',
'30일 rule을 알아야40일 첫 조제 proposal을 판정할 수 있으며 supply category만으로 답할 수 없다.',
'모든 명제가 동일 prescription의 quantity·validity 조건에 연결된다.',
'Archive0597은 같은 사례 변형이다. default0651은 out-of-state initial5일/partial remainder30일, canonical0041은 testosterone quantity/III refill로 다른 clock·scope다.',
'현재 검토 결과를 보존한다.일반30일 validity를 out-of-state initial fill의 특수 기한에 그대로 대입하지 않는다.')
add(603,'BCD',[
'ScheduleIII라는 사실만으로 모든 처방이30일 한도인 것은 아니다. current23(d)는 non-opioid II/III 및 지정 category에 최대90일을 허용한다.',
'90일은 법적 최대치이며 prescriber가 authorization하지 않은 추가 수량을 약국이 마음대로 공급할 권한이 아니다.',
'current non-opioid category는 methylphenidate 등 모든 해당II/III non-opioid로 넓어졌으며 옛 ADD/ADHD/narcolepsy diagnosis 확인 요약에 한정되지 않는다.',
'90-day supply category가 충족되어도 CII validity나 연방III refill 제한 등 해당 처방의 다른 요건은 따로 남는다.'
],['mgl94c23@94C§23(d); policy2024_05@items1–3 and all other II/III max30-day paragraph','mgl94c23@94C§23(d); cfr21_1306@1306.05(a),1306.13(b)(1)(iv)','mgl94c23@94C§23(d)(ii); policy2024_05@item2; no longer verify diagnoses paragraph','mgl94c23@94C§23(a),(d); cfr21_1306@1306.22(a)'],
'BCD가 참이다. 실제 현행 statute의 non-opioid category와2024-05의 진단 확인 불필요 문구를 대조했다.',
'methylphenidate90일 처방과 testosterone의 ScheduleIII quantity 문의는 실제 조제 문의다.',
'과거 diagnosis-specific summary와 current non-opioid category·prescriber-authorized quantity를 구분한다.',
'ScheduleIII면 일률30일이라는 오해와 quantity cap이 authorization를 대신한다는 오해는 실제 규정 변화·단위 혼동이다.',
'현행 category 및90일 최대와 처방 수량의 관계를 알아야 BCD를 선택할 수 있다.',
'같은 II/III single-fill limit를 두 제품에서 비교하고 나머지 validity를 유지하는 자연스러운 구성이다.',
'default REV0048도90일 category를 묻고 canonical0041도testosterone90일을 다룬다. 공유되는 category를 신규 범위로 세지 않으나 여기서는 오래된 diagnosis 조건의 폐기와 prescriber 수량 경계를 추가로 적용한다. archive0601은 같은 사례 변형이다.',
'현재 검토를 보존하되REV0048/0041과 겹치는90일 category 자체를 별도 새 학습범위로 계산하지 않는다.',drug='methylphenidate와testosterone의 non-opioid II/III 지위가 quantity rule 적용을 직접 바꾼다.')
add(607,'ABCD',[
'23(d)의 implantable-infusion-pump90-day quantity 허용은 개별 preparation의 expiration/stability 또는 품질을 증명하는 규정이 아니다.',
'state의90일 OUD quantity category는 federal methadone OUD의 narcotic-treatment-program 및 제한된 별도 dispensing framework를 대신하지 않는다. routine retail OUD prescription dispensing 권한을 창설하지 않는다.',
'일반 opioid pain Rx는 치료 목적이 다르므로 opioid라는 이유만으로 OUD-treatment90일 category가 되지 않는다.',
'federal1306.07(a)–(d)는 ScheduleII narcotic OUD와III–V OUD의 허용 경로를 구별한다. buprenorphine과 methadone을 같은 retail 권한으로 합치지 않는다.'
],['mgl94c23@94C§23(d)(iii); cmr247_9@9.01(3),(12)','mgl94c23@94C§23(d)(i); cfr21_1306@1306.04(c),1306.07(a)–(d)','mgl94c23@94C§23(d)(i) and all-other II/III30-day sentence','cfr21_1306@1306.04(c),1306.07(a)–(d)'],
'ABCD가 참이다. state supply category와 federal OUD authority 및 개별 preparation 적합성을 분리했다. 특정 compounded product의BUD를 이 문항에서 수치 인증하지 않는다.',
'methadone OUD와 buprenorphine 처방을 비교하는 것은 실제 federal/state 경계이다.',
'주 quantity allowance가 federal treatment authority를 대신하지 않는다는 실질적 법적 판단이 배경이다.',
'B와D는 서로 다른 federal pathway를 보라는 같은 결론을 반복하며 A/C는 구체적 제품·환자 없이 일반 한계 문장만 제시한다.',
'모든 보기가 허용 범위를 과장하지 말라는 방향으로 쓰여 구체적 합법 대안 없이 신중한 문장을 전부 고르게 된다.',
'A의 implantable pump 안정성과 C의 일반 pain category는 두 OUD 사례에 관련 사실 없이 추가되었다. state category와 federal authority 결정을 더 선명하게 만들어야 한다.',
'canonical0196도buprenorphine/methadone federal OUD 경로를 묻는다. 본 문항의state90일과의 관계는 추가 적용이나 vague pump 사실은 별도 신규 학습범위를 만들지 않는다. default0599는validity clock으로 다르며 archive0605는 같은 사례 변형이다.',
'구체적인 methadone OUD retail prescription과 buprenorphine treatment order를 제시해 각각 어떤 행위를 할 수 있는지 선택하게 하고, 관련 없는 pump/stability 보기는 제거한 새 판단으로 설계한다.',failed=('authentic_distractors','wording_not_guessable','natural_rule_combination'),drug='methadone과buprenorphine의 연방 treatment 경로 차이는 적절하나 pump 제품이 구체화되지 않았다.')
add(611,'C',[
'controlled Rx는 실제 발행·서명한 날로 date해야 한다. later pickup을 위해 issue date 자체를 postdate할 수 없다.',
'federal multiple-Rx 허용은 state law 및 추가요건 준수를 조건으로 한다. Massachusetts CII30일 validity를 없애지 않으므로 issue60일 뒤 earliest fill은 해당 scenario에서 사용할 수 없다.',
'각 Rx의 legitimate purpose/usual practice, 적절한 earliest-fill instructions, diversion-risk 판단, state-law 허용 및 모든 추가요건 준수가 필요하다.',
'multiple separate original prescriptions은 금지된CII refill을 허용한 것이 아니다.'
],['cfr21_1306@1306.05(a),1306.12(b)(1)(ii)','cfr21_1306@1306.12(b)(1)(iv)–(v); mgl94c23@94C§23(a)','cfr21_1306@1306.12(b)(1)(i)–(v)','cfr21_1306@1306.12(a)–(b)'],
'C만 참이다. actual issue date, separate earliest fill, federal 총량/조건, Massachusetts30일을 함께 적용했다.',
'한 방문에 여러CII Rx를 발행하고 뒤의 처방을60일 후 쓰려는 요청은 실제 비교 상황이다.',
'연방multiple prescription 허용과 주validity를 동시에 적용해야 한다.',
'postdating으로 주의 유효기간을 우회하려는 오해, 총90일 permission을 state override로 읽는 오해, multiple originals를 refill로 부르는 혼동이 구체적이다.',
'C 선택은 state condition과 federal issuance rules를 알아야 하며 단순 숫자 암기만으로 모든 결론이 나오지 않는다.',
'실제issue date와 delayed-use instructions의 차이가 바로 state validity와 충돌하므로 규칙 결합이 자연스럽다.',
'defaultREV0026와 canonical0158도 actual issue/earliest date를 다룬다. 그 공유 범위를 새학습범위로 세지 않지만 본 문항은60일 earliest와Massachusetts30일 validity의 추가 충돌을 실질적으로 적용한다. archive0609는 같은 사례 변형이다.',
'현재 검토를 보존한다. federal90일이MA validity를 덮지 않는다는 추가 판단과 기존 날짜 구분 범위를 구분하여 중복 학습수 집계를 피한다.')
add(615,'AB',[
'electronic outage는 주eRx format exception의 사실일 수 있으나 federal emergency oral의 즉시 필요·적절한 대체 없음·written을 미리 줄 합리적 불가능이라는 세 조건을 모두 증명하지 않는다.',
'제시된 CaseA는 적절한 대체 치료 및 사전written 제공이 가능하다. 빨리 받고 싶다는 편의만으로290.10의 결합 조건을 충족하지 못한다.',
'federal emergency oral quantity는 emergency period를 치료하는 데 적절한 양으로 제한된다. follow-up7일과 고정7-day supply는 다른 개념이다.',
'emergency oral format은CII refill 금지를 없애지 않는다.'
],['cfr21_290@290.10(a)–(c); cmr105_721@721.070(A)(2),721.060','cfr21_290@290.10(a)–(c)','cfr21_1306@1306.11(d)(1),(4)','cfr21_1306@1306.12(a),1306.11(d)'],
'AB가 참이다. federal의 세 조건, state format exception, adequate emergency quantity와follow-up deadline을 각각 대조했다.',
'급히 약을 원하는 환자와system outage는 실제 상황이다.',
'대체 치료 가능/사전written 가능이라는 구체적 사실에 federal emergency의 결합 요건을 적용한다.',
'C의7일 quantity와follow-up deadline 혼동 및 outage=emergency 혼동은 실제 가능한 서로 다른 법적 시계·경로 오류다.',
'AB는290.10의 세 조건을 알아야 한다. 무조건outage로 충분하다는 추정으로는 답하지 못한다.',
'outage의format 예외와emergency oral의 더 좁은 기준을 같은CII 업무에서 자연스럽게 비교한다.',
'Archive0613은 같은 사례 변형이다. default0731은controlled label warning/information, canonical0423은administration record guidance여서 다른 결정이다.',
'보기B의 described in the notes를 삭제하고 이 문항 자체의CaseA 사실과federal 기준에 직접 연결되는 표현으로 고친 후 새 현행 hash 검토를 받는다.',failed=('public_style_without_copying',),drug='CII 약의 emergency oral 허용과no-refill 법적 경로가 핵심이며 특정 약명을 추가해야만 하는 상황은 아니다.')
