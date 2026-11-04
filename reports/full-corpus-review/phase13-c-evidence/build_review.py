import json,hashlib,copy,re
from pathlib import Path
from datetime import datetime,timezone
E=Path(__file__).resolve().parent;R=E.parents[2];PREFIX=E.relative_to(R).as_posix();now=datetime.now(timezone.utc).isoformat();date=now[:10]
def H(b):return hashlib.sha256(b).hexdigest()
def D(o):return H(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def load(p):return json.loads((R/p).read_text())
def save(p,o):(R/p).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
p=load(PREFIX+'/assigned-visible-input.json');a=load(PREFIX+'/assignment.json');ctx={q['question_id']:q for q in load(PREFIX+'/assigned-context.json')};near=load(PREFIX+'/nearest-visible.json');nears={r['question_id']:r for r in near['records']}
# Every truth judgement below is authored in this actual session after visible text and official text review.
u=sorted({c['text'] for r in p['records'] for c in r['original_visible_content']['choices']});assert len(u)==94
TRUE={1,3,8,11,18,19,21,24,25,26,34,35,41,42,43,45,47,48,49,52,57,58,59,60,61,63,64,65,66,67,69,70,71,73,75,78,82,83,85,86,89,90}
S={
'query':[('src-a397fe32483f','105 CMR 700.012(G)(1)–(2), (A)(1)'),('src-8614174367a6','M.G.L. c.94C §24A(c)')],
'report':[('src-a397fe32483f','105 CMR 700.012(A)(1),(5); Additional Drug definition'),('src-deef2ce4e7c3','Who must report; What must be reported; Gabapentin paragraphs'),('src-b2350e40af92','v5.2 §§1–2, Appendix B DSP17 and deliveries pp67–69')],
'zero':[('src-b2350e40af92','v5.2 §2.1, §4.4, §§5–6.2, Appendix E and F pp80–82'),('src-a397fe32483f','105 CMR 700.012(A)(1),(4)–(6)')],
'id':[('src-a397fe32483f','105 CMR 700.012(A)(1),(3)'),('src-b2350e40af92','v5.2 Appendix B AIR03–05, Exceptions and Deliveries pp67–69')],
'hardship':[('src-a397fe32483f','105 CMR 700.012(A)(3)'),('src-b2350e40af92','v5.2 Appendix B customer-ID hardship exception pp67–69'),('src-deef2ce4e7c3','Reporting Naloxone Dispensations, updated October 5, 2022')],
'opioid':[('src-ab1d7b3de5ad','M.G.L. c.94C §19D(a)–(c)'),('src-178a92a2b64d','M.G.L. c.94C §18B(a),(c)')],
'oud':[('src-7965e55e6e8c','DEA January 12, 2023 letter: DATA-Waiver removal and state-law reservation'),('src-93c05bdb2764','MATE FAQ: one-time attestation, first applicable registration June27 2023'),('cfr1306','21 CFR 1306.07(b),(d), 1306.03(a)')],
'label':[('src-4b5f3e5e6f00','M.G.L. c.94C §21 first paragraph'),('src-da8a8280d110','247 CMR 9.04(1),(3),(6)–(7)'),('cfr1306','21 CFR 1306.05(a),1306.14(a),1306.24(a)')],
'large':[('src-4b5f3e5e6f00','M.G.L. c.94C §21 large-print, compounded-identification, contact-phone paragraphs'),('ma11239d','M.G.L. c.112 §39D definition of Beyond-use date'),('cfr1306','21 CFR 1306.14(c),1306.24(c) institutional conditions')],
'warning':[('cfr2905','21 CFR 290.5'),('cfr1306','21 CFR 1306.08(e)–(f),1306.25'),('src-4b5f3e5e6f00','M.G.L. c.94C §21 Department pamphlet paragraph')],
'shield':[('act2025c16','Acts 2025 Chapter16 §§7,27; §7 effective January1 2026'),('shield-guidance','DPH/BHPL/BORIM September2025 memorandum, Prescription Labels'),('cfr1308','21 CFR 1308.13(f)(84) testosterone'),('cfr1306','21 CFR 1306.05(a),1306.24(a),(d)')],
'interchange':[('src-5ae56622aa3c','105 CMR720.020,720.050,720.060'),('fda-orange-preface','Orange Book Preface §1.2 pharmaceutical alternatives/equivalents and therapeutic equivalents; §1.8 TE code pairing')],
'selection':[('src-eb2292f04d83','M.G.L. c.112 §12D no-substitution, required selection, actual-product label paragraphs'),('src-da8a8280d110','247 CMR9.04(6)–(7);9.05(1)–(3)'),('src-16f1fbbdd07a','105 CMR721.020 prescription no-substitution format')],
'generic':[('src-da8a8280d110','247 CMR9.05(2)'),('src-a8947630c051','FDA authorized generic explanatory page; NDA marketing and quarterly listing, updated October5 2026'),('src-0a51fd50980a','DCP22-01-112 authorized-generic interchange and verification paragraphs')]
}
GROUPS={'query':[26,37,41,52],'report':[9,34,36,46,49,50,85],'zero':[7,10,11,24,30,54,65,90],'id':[1,4,35,53,56,58,77],'hardship':[18,33,40,44,63,68,69],'opioid':[6,20,39,64,70,75,93],'oud':[13,25,27,51,61,83,88,89],'label':[3,5,17,23,32,47,57],'large':[0,12,19,21,22,60,62],'warning':[15,28,31,42,74,78,86],'shield':[8,55,66,67,80,91,92],'interchange':[14,43,48,72,82,84,87],'selection':[38,45,59,73,76,79,81],'generic':[2,16,29,71]}
G={i:g for g,ii in GROUPS.items() for i in ii};assert set(G)==set(range(94))
reason={
0:'10 point는 글자 높이 단위이고 §21은 요청 시 inch당 최대10문자라는 가로 밀도 기준이다. point 수치만으로 준수를 입증하지 못한다.',
1:'안내서 Appendix B는 실제 customer의 정부발급ID를 확인하도록 하고 SSN을 customer ID로 제출하지 않도록 명시한다. notes라는 외부 지칭은 문항 내 규칙으로 바꾸어야 한다.',
2:'authorized generic은 특정 NDA 제품과의 실제 대응관계이다. 동일 회사라는 사실은 다른 두 제품의 대응관계를 입증하지 않는다. DCP는 불명확하면 제조·유통자에게 확인하도록 한다.',
3:'§21은 환자 용기 자체에 directions를 요구한다. 내부기록의 정확성은 라벨 표시 의무를 대체하지 않는다.',
4:'안내서 배송 예외는 customer-ID 수집·보고에 한정되고 내부 배송 추적을 유지하도록 한다. 임의 수령인에게 추적 없이 전달하는 권한이 아니다.',
5:'§21의 drug name 의무 및 실제 제품 식별은 약효군 이름만으로 충족되지 않는다. 서로 다른 strength/form을 한 계열명으로 구별할 수 없다.',
6:'§19D(a)는 미성년자의 opiate 처방을 at any time으로 다룬다. 재처방이라는 사실만으로 면제되지 않으며 (b),(c) 예외를 따로 본다.',
7:'waiver는 승인 범위에 관한 예외다. 실제 reportable dispensing을 무조건 숨길 권한을 주지 않는다.',
8:'라벨에서 practice명을 쓰는 §7 예외는 prescription의 실제 prescriber 권한·신원을 없애는 규정이 아니다. 1306.05의 원처방 이름 의무와 구별한다.',
9:'700.012(A)(1)은 MA 수령인에게 대상약을 전달하는 타주 약국을 명시한다. 타주 소재만으로 면제되지 않는다.',
10:'파일 수신과 개별 레코드 import는 다르다. §6.2의 error record는 수정돼야 import되므로 rejection을 성공 upload로 덮을 수 없다.',
11:'Appendix E의 waiver 사유와 실제 활동을 대조해야 한다. 약을 조제하지 않는다는 조건으로 받은 예외가 조제 사실까지 자동 포괄하지 않는다.',
12:'§21의 inpatient 예외는 특정 compounded-product 연락전화 문단에 한정되고 연방 label 예외에도 별도 조건이 있다. 모든 외래처방에 확대할 수 없다.',
13:'DEA는 2022-12-29 DATA-Waiver 폐지 후 표준 DEA번호를 사용한다고 명시한다. 옛 소프트웨어 칸은 현행 X번호 의무를 만들지 않는다.',
14:'720.050은 실제 TE관계와 MA 목록을 본다. 같은 성분의 모든 제품이 임의 A-rating 하나로 서로 동등해지는 것은 아니다.',
15:'§21은 Department가 만든 자료와 특정 내용·배포 조건을 규정한다. 아무 leaflet이나 자동 충족하는 구조가 아니다.',
16:'FDA 목록은 NDA holder 보고에 따른 분기별 데이터이고 실시간 재고 증명서가 아니다. 등재로 현재 유통·재고까지 보장된다는 추론은 허용되지 않는다.',
17:'247 CMR9.04(1)은 final dispensing validation 책임을 licensed pharmacist에게 둔다. technician이 라벨을 붙였다고 책임이 이동하지 않는다.',
18:'700.012(A)(3)의 serious-hardship 판단·사유기록·대체 신원정보를 적용해야 한다. ID 부재만으로 일괄 허용하거나 일괄 금지하는 것은 그 예외를 제대로 적용하지 않은 것이다.',
19:'§39D는 BUD를 compounding 시점부터 결정한다고 정의한다. 원제품의 제조사 expiration과 같은 출발점이나 보증조건이 아니다.',
20:'§19D(a)는 실제 adult first outpatient 상황에 적용된다. staff가 refill이라고 부르는 명칭으로 실제 사실이 바뀌지 않는다.',
21:'§21의 characters/inch는 가로 문자 밀도이고 point size는 다른 단위다. 두 값을 동일시하면 안 된다.',
22:'§21은 pharmacy가 compounded/made/formulated한 preparation의 sterile/nonsterile 식별을 요구한다. 승인 성분을 쓴다고 그 준비 경로가 없어지지 않는다.',
23:'§21은 용기에 directions를 표시하게 한다. 내부에만 directions가 있으면 환자 라벨 의무가 남는다.',
24:'Appendix F는 fatal unaccepted record의 new 재제출과 accepted record의 revise/void를 구별한다. 항상 둘째 활성기록을 추가하는 방식은 중복·정정 오류를 낳는다.',
25:'X-waiver 폐지는 추가 등록요건 폐지다. DEA 표준 등록과 주법상 허용범위는 별도로 남는다고 DEA가 명시한다.',
26:'700.012(G)는 II/III opioid 및 benzodiazepine이라는 범주를 사용한다. Schedule 숫자와 약리·법적 계열 사실을 각각 확인해야 한다.',
27:'MATE는 첫 해당 등록/갱신에서 일회 attestation이며 인정되는 교육 경로도 여러 가지다. 매 갱신 새 X-waiver와 새8시간 교육이라는 주장은 틀리다.',
28:'290.5는 연방 II·III·IV에 적용한다. MA VI라는 주 분류만으로 해당 연방 warning 의무가 생기지 않는다.',
29:'FDA는 authorized generic을 brand NDA로 판매한다고 설명한다. 별도 ANDA가 반드시 있다는 주장은 규제 경로를 혼동한다.',
30:'Appendix F의 accepted revise/void와 unaccepted new 재제출 절차에 반한다. 기존 상태를 무시하고 두번째 활성기록을 만드는 것은 적절한 공통 정정법이 아니다.',
31:'§21은 대상 약물 범주·기관 제외·palliative/LTC/SUD 예외를 구체적으로 둔다. 모든 schedule 모든 약에 동일 의무가 있는 것은 아니다.',
32:'1306.05의 원처방은 DEA번호 등 항목을 요구하지만 §21·1306.14/.24의 환자 라벨 목록은 별도다. 원처방 항목 전부를 자동 인쇄하도록 하지 않는다.',
33:'700.012(A)(3)은 ID 없는 각 수령인의 serious hardship과 사유기록 등 조건을 검토하게 한다. 모든 ID 부재 상황을 동일 처리할 수 없다.',
34:'DCP 현행 reporting page가 gabapentin을 MA VI drug of concern으로 명시한다. 비연방 scheduled라는 이유만으로 PMP보고에서 제외되지 않는다.',
35:'700.012(A)(3)은 추가 지정약에도 identifier를 적용하고 안내서가 gabapentin을 명시한다.',
36:'Additional Drug 지정은 특정 약의 추가 적용이다. MA VI 전체가 같은 보고대상이 되었다는 결론은 A(1)의 범위를 넘는다.',
37:'실제 legally prescribing하는 practitioner의 G(1) 의무를 적용한다. pharmacist 면허를 보유한다는 이유만으로 다른 합법적 역할의 의무가 사라지지 않는다.',
38:'§12D의 요건을 충족한 경우 inventory preference는 열거된 no-substitution 또는 documented medical emergency를 대신하지 않는다.',
39:'§18B(c)의 유효 추정에는 knowingly against directive 예외가 명시된다. 서면처방만 있으면 실제 지식을 무시해도 된다는 주장은 틀리다.',
40:'700.012(A)(3)은 serious hardship에 대한 reason과 documentation 및 대체정보를 요구한다. ID 부재 하나로 모든 요건을 충족하지 않는다.',
41:'G(1)의 pre-prescribing query와 A의 pharmacy dispensing report는 의무자·시점·행위가 다르다. 사후보고로 사전조회가 이행되지 않는다.',
42:'연방290.5의 범위는 II–IV다. MA VI 지위만으로 연방 warning을 강제할 수 없다.',
43:'FDA Preface1.2는 IR 대비 ER을 pharmaceutical alternative로 구별한다. 성분명 일치만으로 formulation 간 interchange가 확정되지 않는다.',
44:'DCP는 naloxone 제출을 data collection으로 다루고 patient-ID 불요라고 명시한다. gabapentin의 AIR customer-ID 경로와 동일하다고 볼 수 없다.',
45:'§12D는 signature로 prescription을 validate하는 것과 no substitution을 따로 둔다. no-substitution이 default여서는 안 된다고 명시한다.',
46:'700.012(A)(1) 및 DCP현행 페이지가 Additional Drug/gabapentin을 포함한다. federally scheduled인 약만 보고한다는 주장은 틀리다.',
47:'1306.05 원처방 내용과 §21 환자 라벨의 항목을 각기 확인해야 한다. 두 문서의 필수정보는 동일 집합이 아니다.',
48:'720.020 및 FDA Preface1.2는 pharmaceutical equivalent와 bioequivalence 등을 추가한 therapeutic equivalent를 별도 정의한다.',
49:'안내서 Appendix B의 DSP17은 실제 sold/delivered event를 다룬다. 준비일은 수령인에게 실제 인도된 사실과 같지 않다.',
50:'DSP17의 실제 판매·인도 시점과 preparation은 다르다. 준비만 했는데 sold/delivered라고 기록할 근거가 없다.',
51:'DEA는 X-waiver폐지가 state law에 영향을 주지 않으며 표준등록이 필요하다고 명시한다. 모든 등록·주 권한 면제라는 주장은 틀리다.',
52:'보고 지정의 법적 근거(A)와 prescribing query trigger(G)는 별개다. 보고 포함 사실만으로 모든 query category 해당을 도출하지 않는다.',
53:'700.012(A)(3)은 Additional Drug를 포함하고 현행 guide가 gabapentin을 명시한다. MA VI라는 사실만으로 면제되지 않는다.',
54:'§2.1과4.4는 해당 기간 거래가 없어도 zero report를 제출하도록 한다. 무제출은 승인 waiver 없는 zero report가 아니다.',
55:'Acts2025c16§7은 federal law를 유보한 patient label 변경이다. testosterone은 CIII여서1306.24의 prescriber name 의무가 남고 원처방 prescriber 기록도 삭제할 수 없다.',
56:'Appendix B는 SSN을 customer identifier로 제출하지 못한다고 명시한다. 우선 대체값이 아니다.',
57:'§21의 controlled substance 이름 및 실제 제품 식별과9.04 검증 책임을 함께 본다. drug/strength/form을 식별하는 적정 정보가 필요하다는 일반 설명은 지지된다. 특정 예외 없는 모든 label에 모든 field가 있다는 뜻으로 확대하지 않는다.',
58:'customer는 ultimate user 또는 agent로 실제 받는 사람이다. 안내서는 매번 그 수령인과 일치하는 현재 유효ID를 확인하도록 한다.',
59:'§12D의 applicable less-expensive interchangeable selection rule은 편의로 생략할 수 없다. no-substitution 및9.05(1)의 의료응급 예외는 별도로 본다.',
60:'§21은 compounded product에 sterile/nonsterile compounded preparation 식별을 요구한다. 본문이 적절한 경우라는 범위를 유지한다.',
61:'DEA 현행 MATE FAQ는 일회 attestation과 과거 X-waiver폐지를 구별한다. 이수 인정 경로도 있으므로 반복 X-waiver가 아니다.',
62:'§39D의 BUD 출발점은 compounding 일시다. 모든 preparation BUD가 원료 제조사 만료일과 같다는 주장은 법적 정의와 맞지 않는다.',
63:'700.012(A)(3)은 serious hardship 합리적 사유와 사유기록을 요구한다. 단순 ID 부재와 다르다.',
64:'§18B(c)은 knowingly against directive를 보호의 예외로 둔다. 유효성 추정이 고의적 무시를 포괄하는 면책은 아니다.',
65:'안내서§2.1과4.4상 waiver 없는 resident 약국은 해당 기간 zero report를 제출해야 한다. 아무 것도 보내지 않는 것으로 대신하지 못한다.',
66:'Acts2025c16§7·27에 따라2026-01-01부터 protected-care prescription은 provider 요청 시 federal law가 허용하는 범위에서 practice명 라벨을 쓴다. eligible VI라는 stem조건에서 이 경로를 적용한다.',
67:'testosterone은1308.13(f)(84)의 CIII이고1306.24(a)는 practitioner명을 요구한다. §7은 federal law 유보가 있고 patient label 예외로 원처방 기록을 없애지 않는다.',
68:'700.012(A)(3)은 이름·주소·서명과 required reporting fields를 명시한다. hardship은 신원·보고정보 전부를 비워도 되는 예외가 아니다.',
69:'hardship 예외도 대체 이름·주소·서명 및 지정 reporting field를 제공해야 한다. Appendix B는 cust signed rx를 안내한다.',
70:'§19D(a)는 adult first outpatient opiate를7일 원칙으로 다루고(b)의 clinical judgment·의무기록·nonopiate 부적절성 조건을 본다.',
71:'9.05(2)는 generic명이고 제조사 미지정이면 prescriber intent와 professional judgment에 따라 legally marketed product를 선택하는 별도 경로를 둔다.',
72:'보험 청구 지급은720.020/.050의 동등성 판단이나 MA interchange 법적 요건을 대신하지 않는다.',
73:'§12D와9.05(3)은 실제 dispensed generic+manufacturer 또는 dispensed brand로 interchange표시를 요구한다. 원래 브랜드만 기록해서 실제 제품을 숨길 수 없다.',
74:'290.5는 physical drug를 다른 환자에게 주는 경고다.1306.08 및.25가 허용한 prescription-information transfer를 전면 금지하지 않는다.',
75:'§19D(a)의 minor 규칙은 at any time이다. 첫 처방으로만 한정하는 성인 trigger와 구별한다.',
76:'§12D와9.05(3)의 actual-product 식별을 충족해야 한다. 원브랜드는 추가표시될 수 있으나 실제 dispensed product를 숨기는 단독표시는 불충분하다.',
77:'안내서 Appendix B는 과거 저장ID를 자동 대입하지 말고 실제 customer의 매번 유효ID를 확인하도록 한다. 환자의 과거ID는 agent의 현재ID 대체가 아니다.',
78:'290.5의 drug transfer와1306.08/.25의 prescription information transfer는 법적 대상 행위가 다르다. otherwise lawful이라는 stem조건을 존중한다.',
79:'9.04(6)–(7)의 실제 dispensing data/NDC 및9.05(3)의 실제 product 식별이 필요하다. 편의로 다른 제품을 기록할 수 없다.',
80:'§7은 protected-care provider 요청과 federal law유보를 둔다. 모든 라벨에서 아무 조건 없이 prescriber명을 지우도록 허용하지 않는다.',
81:'§12D에서 signature는 처방 유효화에 관한 것이고 no-substitution은 별도 표시다. 서명만으로 interchange를 취소하지 않는다.',
82:'720.050의 최신 FDA TE 및 MA addition/exclusion 체계와 실제 reference/code를 대조해야 한다. Preface의 AB+숫자 설명도 공통code를 본다.',
83:'2022-12-29 DATA-Waiver폐지 후 DEA 표준번호를 쓴다. 옛 field 존재만으로 X번호 요구를 되살릴 수 없다.',
84:'FDA Preface1.2는 ER과IR을 pharmaceutical alternatives로 구별한다. 성분명 하나만으로 자동 대체하지 못한다.',
85:'700.012(A)(1)은 II–V 또는 지정 Additional Drug다. 지정약 추가를 모든 VI 동일보고로 확대하지 않는다.',
86:'§21의 환자정보자료는 범주·기관·palliative/LTC/SUD 예외가 따로 있다. 특정 opioid/narcotic 관련 의무의 적용조건을 구별한다는 설명은 지지된다. 법문상 II/III controlled substance 문구도 누락하지 않아야 한다.',
87:'720.020은 pharmaceutical equivalence와 therapeutic equivalence에 서로 다른 요건을 둔다. 구별이 전혀 없다는 주장은 틀리다.',
88:'1306.07(b)는 dispensing but not prescribing이며 최대3일 공급, referral을 마련하는 동안, renewed/extended불가를 명시한다.',
89:'1306.07(b)는 제한된 direct dispensing 경로이고 처방·갱신·연장의 근거가 아니다. 별도의.07(d)상 합법적 buprenorphine prescribing과 혼동하지 않는다.',
90:'§6.2는 record errors 및 import를 따로 다룬다. upload 성공만으로 rejected records까지 수리됐다고 할 수 없다.',
91:'성별확정 진료라는 적응증이 법적 schedule을 정하지 않는다. testosterone은1308.13(f)(84) CIII다.',
92:'§7은 환자 label표시만 바꾼다. 실제 prescriber 신원·권한 확인과1306.05 원처방 정보의무는 그대로 검토한다.',
93:'§19D(b)는 professional medical judgment, medical record에 상태기록, nonopiate alternative부적절성 표시를 요구한다. 진단명 한 줄만으로 모든 조건을 충족하지 않는다.'}
assert set(reason)==set(range(94))
# Source bindings retain original retrieval timestamps and the exact bytes or authored restricted-source memo.
sources={}
for mp in sorted(E.glob('*.meta.json')):
 m=json.loads(mp.read_text());sid=m['id'];rp=Path(m['raw_path']);tp=Path(m['text_path']);restricted=m.get('public_raw_redistribution') is False
 ev=Path(m['memo_path']) if restricted else tp
 def rel(path):
  try:return path.relative_to(R).as_posix()
  except ValueError:return str(path)
 assert H(rp.read_bytes())==m['raw_sha256'];assert H(tp.read_bytes())==m['text_sha256']
 sources[sid]={'source_id':sid,'authority':m['title'],'source_type':'PUBLIC_OFFICIAL','official_url':m['url'],'law_checked_date':date,'effective_date':('2026-01-01' if sid=='act2025c16' else '2022-12-29' if sid=='src-7965e55e6e8c' else '2023-06-27' if sid in ['src-93c05bdb2764','src-607e95c04a30'] else None),'version_or_effective_date_limit_ko':('§7 라벨 개정의 시행일은§27에서 직접 확인함. 통합§21 웹본문에는 이 개정이 빠져 있어 session law를 우선함.' if sid=='act2025c16' else '현재 공식 게시원문을 실제 검토했다. 개별 조항의 최초 시행일·모든 중간 개정 이력은 이 감사에서 확정하지 않았다. guide는v5.2 May2023,9CMR는12/6/24게시본, FDAauthorized는10/5/2026페이지이며 현재DCP게시 경로와 함께 확인했다.'),'retrieved_at':m['requested_at'],'retrieval_completed_at':m['completed_at'],'read_at':now,'retrieval_provenance':m['retrieval'],'http_status':m['http_status'],'document_identity_confirmed':m['http_status']==200,'raw_path':rel(rp),'raw_sha256':m['raw_sha256'],'evidence_path':rel(ev),'evidence_sha256':H(ev.read_bytes()),'metadata_path':mp.relative_to(R).as_posix(),'metadata_sha256':H(mp.read_bytes()),'text_sha256':m['text_sha256'],'public_raw_redistribution':not restricted,'public_evidence_mode':m.get('public_evidence_mode','official government raw plus extracted text'),'legal_authority_used':sid in {x[0] for group in S.values() for x in group}}
 if restricted:sources[sid]['private_text_path']=str(tp)
 else:sources[sid]['text_path']=rel(tp)
 if m['http_status']!=200:sources[sid].update(document_identity_confirmed=False,legal_authority_used=False,access_status='SOURCE_BLOCKED',limitation_ko='404는 법규 확인으로 세지 않았다. BUD는 별도MGL112§39D로 확인했다.')
for sid,src in sources.items():
 src['coverage']='; '.join(sorted({section for group in S.values() for k,section in group if k==sid})) or ('공개형식·competency만 확인;법률권위아님' if sid.startswith('nabp-') else '조회시도·문서탐색기록;최종명제법률권위로미채택')

def authorities(g):
 return [dict(copy.deepcopy(sources[sid]),exact_section=section) for sid,section in S[g]]
# Individual item focus used in each of the ten criterion findings below.
focus={
'PMP02':('사전조회와 사후보고의 의무자·시점을 분리','CII opioid와gabapentin의 서로 다른 trigger','면허 보유만으로 의무가 사라진다는 오답','같은 환자 처방 판단이 아니라 두 직원의 일반 의견이 병렬로 제시된다'),
'PMP03':('gabapentin의 추가 보고대상 및 actual delivery기록을 판단','비연방 scheduled약과 실제 판매·인도일','타주 소재·모든VI·준비즉인도라는 오답','보고대상과 배송일은 같은 PMP 작업에 속하지만 SBA에서는 다른 사례가 답에 쓰이지 않는다'),
'PMP04':('zero report와 file/record acceptance를 분리','거래 없는 기간·waiver부재·rejected record','무제출을zero로 보거나상태무시 재제출하는 혼동','같은 reporting workflow의 제출·검증·정정을 연결한다'),
'PMP05':('환자와 실제 수령agent의 현재ID를 구별','agent수령과SSN입력','저장환자ID·SSN·배송예외의 과잉확장','수령 workflow에서 신원·예외·추적을 자연스럽게 함께 본다'),
'PMP06':('serious hardship의 판단·기록·대체정보를 적용','ID없는환자와대체서명절차','ID부재자동면제·모든정보blank·naloxone혼동','예외의 발동과 대체절차는 연결되나naloxone은별도 거래 없이 보기로 추가된다'),
'PMP07':('adultfirst/minoranytime 및 knowingly directive를 구별','첫 외래opioid와이미아는directive','재처방명칭·진단명한줄·지식무시','공급제한과directive는 별도의 두사례로 나열되고 같은 dispensing결론으로 합쳐지지 않는다'),
'PMP08':('X-waiver폐지와표준등록·MATE·3일경로를 구별','buprenorphine과응급OUD직접공급','옛Xfield·반복교육·dispense와prescribe혼동','OUD치료 허용경로의 연방조건을 비교한다'),
'LAB01':('원처방·내부기록·환자라벨 의무를 구별','directions누락과DEA번호자동인쇄주장','내부기록대체·technician책임이전','문서종류의구별은 관련되나SBA에서묻지않은두번째사례가불필요하다'),
'LAB02':('큰글씨의단위와compounded준비식별 의무를 판단','노인/시각장애적격요청 및조제준비물라벨','point/CPI동일시·BUD/expiration·inpatient확대','큰글자단위와compounded식별은 독립사례여서 한임상결정의연결추론이아니다'),
'LAB03':('physicaldrug전달경고와Rx정보전달·연방범위를 구별','federalII–IV warning과MA VI','모든transfer금지·모든VI적용·아무leaflet','경고해석과범위는관련되나opioid자료는사례밖별도주제다'),
'LAB04':('protected-care practice명label과federalprescriber/원기록 의무를 구별','eligibleVI와testosterone CIII','성별확정진료=VI·라벨예외=기록삭제','같은label예외의주법과연방법경계를 비교한다'),
'LAB05':('제품쌍별TE와제형차이를 평가','IR/ER와A-rating/code','같은성분·아무A·보험지급의과잉추론','성분·제형·TE관계는 하나의productselection결정에연결된다'),
'LAB06':('기본interchange선택과actualproduct표시·기록을 적용','유효no-substitution없고저렴한제품합리적가용','서명=거부·원브랜드만표시·편의상다른제품기록','제품선택 후표시·기록은 자연스러운연속단계다'),
'LAB07':('generic명제조사미지정처방의별도selection경로를 적용','generic명Rx와NDAauthorizedgeneric','모든ANDA·동일제조사자동관계·등재=재고','genericname pathway와authorizedgeneric확인은서로다른두케이스다')}
records=[]
for row in p['records']:
 q=row['original_visible_content'];qid=q['question_id'];family=ctx[qid]['family_id'];f=focus[family];incorrect='INCORRECT' in q['stem'];sata=q['question_type']=='SATA';findings=[]
 for c in q['choices']:
  i=u.index(c['text']);truth=i in TRUE;g=G[i]
  findings.append({'choice_id':c['id'],'option_text':c['text'],'option_text_sha256':H(c['text'].encode()),'statement_supported':truth,'truth_assessment':'TRUE' if truth else 'FALSE','selected_under_polarity':truth if not incorrect else not truth,'finding_ko':reason[i], 'authorities':authorities(g)})
 expected=[x['choice_id'] for x in findings if x['selected_under_polarity']];assert sata or len(expected)==1,(qid,expected)
 keyok=set(expected)==set(q['correct_choice_ids']);assert keyok,(qid,expected)
 edit=qid in ['MA-EXP-0706','MA-EXP-0708'];legalverdict='MINOR_EDIT' if edit else 'KEEP'
 groups=sorted({G[u.index(c['text'])] for c in q['choices']});auth=[]
 for g in groups:
  for x in authorities(g):
   if not any(y['source_id']==x['source_id'] and y['exact_section']==x['exact_section'] for y in auth):auth.append(x)
 # Visible near candidates have been read, including all choices. Archival siblings are deliberately grouped and do not alone fail distinctness.
 nr=nears[qid];can=nr['canonical'][0];pub=nr['public'][0]
 integrated=family in ['PMP04','PMP05','PMP08','LAB04','LAB05','LAB06'];passitem=qid in ['MA-EXP-0703','MA-EXP-0719']
 criteria=dict(jurisprudence_reasoning=True,practice_plausibility=True,authentic_distractors=True,wording_not_guessable=passitem,reasoning_not_trivia=True,natural_rule_combination=integrated or passitem,appropriate_drug_context=True,distinct_from_bank=True,not_schedule_flashcard=True,public_style_without_copying=True)
 cf={
'jurisprudence_reasoning':f'{qid}는 {f[0]}해야 하므로 법률상 행위·조건 구별이 있다.',
'practice_plausibility':f'{qid}의 {f[1]} 상황은 실제 약국 업무에서 생길 수 있다. 다만 일반 직원 주장보다 구체적 거래 사실을 더 주면 좋다.',
'authentic_distractors':f'{qid}는 {f[2]}이라는 실제 개념 혼동을 평가한다.'+('SATA의 네보기가 모두 참이어도 각 명제를 따로 평가했고 무조건 오답보기를 넣어야 한다고 가정하지 않았다.' if sata else ''),
'wording_not_guessable':(f'{qid}의SATA는4개 명제를 각각검토해야 하고 alltrue조합 자체가 정답단서라고 간주하지 않았다. file/record 또는등록/응급공급의 실질조건을 안 뒤모두선택해야 한다.' if passitem else f'{qid}의 보기에서는 '+(', '.join(sorted({w for c in q['choices'] for w in ['every','automatically','solely','necessarily','any recipient','untracked'] if w in c['text'].lower()})) or '근거 없이 의무가 없어진다고 단정하는 표현')+f'와 조건을 검토하라는 신중한 표현이 대비된다. {expected} 선택은 구체 법규보다 이러한 표현으로도 쉽게 유도된다.'),
'reasoning_not_trivia':f'{qid}는 {f[0]}라는 판단을 묻는다. 단순 숫자·약명 암기가 전부인 문항으로 처리하지 않았다. 다만 정답의 추상적 재진술로 난도가 낮아진다.',
'natural_rule_combination':f'{qid}: {f[3]}. '+('관련된 작업 단계와 권한경로를 비교하므로 이기준은 충족한다.' if criteria['natural_rule_combination'] else '두사례를 동시에 주는 것만으로 연결추론이 생기지 않아 이기준은 충족하지 못한다.'),
'appropriate_drug_context':f'{qid}의 {f[1]}가 법적 범위 구별에 관련된다. 약명이 없는 부분도 특정 제품을 임의 추가하지 않고 그 행위의 법적 조건을 평가했다.',
'distinct_from_bank':f'canonical {can["visible"]["question_id"]}와 public {pub["visible"]["question_id"]}의 stem/전체보기를 직접 읽었다. public 후보는 같은 두사례를 쓰는 명시적 family연습변형이다. 새로운 독립 임상사례로 세지 않는다. canonical 후보는 주제 또는 낱말이 겹쳐도 다른 사실·요건·판단을 요구한다. archive형제의 존재만으로 이기준을 자동실패시키지 않았다.',
'not_schedule_flashcard':f'{qid}는 {f[0]}를 묻고schedule이 등장하더라도 그분류가 보고·표시·처방행위에 주는 결과를 적용한다. 순수schedule명암기카드는 아니다.',
'public_style_without_copying':f'{qid}의 '+('SATA' if sata else 'SBA')+'선택형은 실제확인한NABP공개sample형식과 양립한다. 공개문구를 복제하지 않았다. source는이번조회200으로본문확인했고Pre-MPJE/회상/상용bank를 열지 않았다.'}
 rv='PASS' if all(criteria.values()) else 'FAIL';assert (rv=='PASS')==passitem
 explanation={'core_reasoning_read':True,'every_choice_rationale_read':True,'learning_boundary_read':True,'original_explanation_sha256':D(q['explanation']),'core_assessment_ko':f'{qid}의 core_reasoning 전문을 공식원문과 대조했다. {f[0]}라는 중심 설명은 지지된다. '+('notes 지칭은 문항 외부 의존이어서 고쳐야 한다.' if edit else '해설이 선언한family연습변형 한계를 유지해야 한다.'),'choice_assessments':[{'choice_id':c['id'],'rationale_sha256':H(q['explanation']['choice_analysis'][c['id']].encode()),'read_full':True,'finding_ko':reason[u.index(c['text'])],'assessment':'SUBSTANTIVELY_SUPPORTED_WITH_WORDING_EDIT' if edit and u.index(c['text'])==1 else 'SUBSTANTIVELY_SUPPORTED'} for c in q['choices']],'scope_limit_ko':'핵심·모든보기·learning_boundary를읽었으며숨은저자truth나기존판정은사용하지않았다. 약물계열/법적분류 및allowed/required/prohibited를구별했다. LAB03의환자자료의무는§21실제II/III범위·예외를따로확인했다.'}
 records.append({'question_id':qid,'record_sha256':row['record_sha256'],'visible_content_sha256':row['visible_content_sha256'],'family_id':family,'read_scope':{'stem':True,'all_choices':True,'stored_key':True,'question_type':True,'incorrect_polarity':incorrect,'sata_combination':sata,'complete_korean_core_reasoning':True,'complete_each_choice_rationale':True,'learning_boundary':True,'read_at':now,'prior_verdict_exposure_count':0},'legal_review':{'existing_answer_correct':'YES','stored_key':q['correct_choice_ids'],'independently_expected_key':expected,'polarity':'SELECT_FALSE' if incorrect else 'SELECT_ALL_TRUE' if sata else 'SELECT_ONE_TRUE','single_answer_uniqueness_checked':not sata,'sata_all_options_evaluated':sata,'per_choice_findings':findings,'authorities':auth,'verdict':legalverdict,'finding_ko':f'{qid}: 원문조건에서 {expected}가 '+('유일한거짓명제' if incorrect else '참인전체명제조합' if sata else '유일하게올바른결론')+'이다. '+('보기와해설의 notes를실제PMP규칙으로바꾸는경미한편집이필요하다.' if edit else '저장키는공식원문과일치한다. 다른보기의과잉일반화·행위자·시점혼동을별도로검토했다.'),'blocker':None,'original_explanation_review':explanation},'realism_review':{'verdict':rv,'decision':'KEEP' if rv=='PASS' else 'MAJOR_REWRITE','criteria':criteria,'criterion_findings_ko':cf,'finding_ko':f'{qid}: '+('10기준을모두검토해충족한다. 동일family변형을독립새상황으로세지않는다.' if rv=='PASS' else '표현만으로추측할수있는단서'+('와서로독립적인사례병렬' if not criteria['natural_rule_combination'] else '')+'때문에현실성전체PASS를주지않는다.'),'duplicate_review':{'status':'RUN_AND_VISIBLE_NEAREST_READ','method':near['method'],'canonical_pool_count':near['canonical_count'],'public_pool_count':near['public_count'],'canonical_nearest':can,'public_nearest':pub,'evidence_path':PREFIX+'/nearest-visible.json','evidence_sha256':H((E/'nearest-visible.json').read_bytes()),'semantic_finding_ko':cf['distinct_from_bank']},'style_source_ids':['nabp-sample','nabp-format','nabp-competency']},'safe_hold_recommended':rv!='PASS' or edit,'release_eligible':False,'canonical_release_credit':0,'required_next_action_ko':('Root가본독립assessment를순차통합하고별도canonical초기감사·adjudication·releasegate를수행해야한다.' if rv=='PASS' and not edit else f'{qid}의정답과원기록을그대로보존한채editor가 '+('notes외부지칭을고치고 ' if edit else '')+'하나의구체거래에필요한사실을제시하고정답·오답의단정성및길이를균형있게재작성한뒤새hash에fresh법규·현실성감사를받아야한다. 기존부정결과를다른KEEP으로덮지않는다.')})
method_files=['docs/RELEASE_POLICY.md','docs/AUDIT_WORKFLOW.md','docs/SOURCE_USE_POLICY.md','docs/QUESTION_AUTHORING_STANDARD.md','docs/INDEPENDENT_LEGACY_REVIEW_RUNBOOK.md','data/exam_style/mpje_style_profile.json','data/blueprint.json','schemas/audit.schema.json']
method={x:{'file_sha256':H((R/x).read_bytes())} for x in method_files}
method['schemas/audit.schema.json'].update(schema_dialect=load('schemas/audit.schema.json')['$schema'],schema_id=load('schemas/audit.schema.json')['$id'],declared_version=None,version_limit_ko='이파일에별도version필드가없어정확한fileSHA와schemaURI를고정했다.')
style=load('data/exam_style/mpje_style_profile.json');bp=load('data/blueprint.json')
for path,obj in [('data/exam_style/mpje_style_profile.json',style),('data/blueprint.json',bp)]:method[path].update(content_version=obj['content_version'],semantic_hash=obj['content_hash'])
report={'stage':'independent-legacy','independent_of_authors':True,'auditor':'GPT','auditor_instance':'GPT:/root/independent_wave13_c:20261104','actor_provenance':{'actor_id':'/root/independent_wave13_c','session_id':'/root/independent_wave13_c'},'canonical_audit':False,'canonical_release_credit':0,'author_review_credit':0,'release_eligible':False,'reviewed_at':date,'completed_at':now,'job_id':a['job_id'],'question_hashes':a['question_hashes'],'input_bindings':{n:H((E/n).read_bytes()) for n in ['assignment.json','assigned-visible-input.json','assigned-context.json']},'methodology_bindings':method,'style_profile':{'id':style['profile_id'],'version':style['content_version'],'semantic_hash':style['content_hash'],'file_sha256':H((R/'data/exam_style/mpje_style_profile.json').read_bytes())},'independence':{'actual_fork_none_new_session':True,'prior_verdict_content_exposure_count':0,'author_truth_content_exposure_count':0,'not_author_or_editor_of_assigned_content':True,'incidental_exposure_limit_ko':'배정전파일명검색에서기존report경로명만보였다. 초기source locator명령이guide.sources의checked/access/scope_note까지출력했으나문항의기존판정이나저자truth는없었다. 이후id/title/url만명시projection했다. source의원래검토주장을독립검증근거로채택하지않았다.'},'sources':list(sources.values()),'source_review_limits_ko':['MGLc94C§21통합웹본문은2025Shield개정이누락되어Acts2025c16§§7,27및공식DPH안내로직접보완했다. 해당라벨개정시행일은2026-01-01이다.','PMPguidev5.2는현재DCP가연결하는행정제출문서다. 오래된XDEAfield를법적요건으로쓰지않았다. Bamboo및NABP저작권원문·추출문은publiccommit에서제외하고SHA와직접작성memo를보존했다.','잘못추정한247CMR17다운로드URL은404로실패했다. 이를법적근거로쓰지않고BUD정의는MGL112§39D에서확인했다.','나머지조항의최초시행일과모든개정이력을확정했다고주장하지않는다.2026-11-04실제공식게시원문검토를기록했다.','보호된Pre-MPJE/실제시험회상/상용무단자료를읽거나처리하지않았다. NABP공개sample은200으로실제열람하고형식만활용했다.'],'records':records,'summary':{'assigned_originals_read':len(records),'key_yes':sum(r['legal_review']['existing_answer_correct']=='YES' for r in records),'legal_keep':sum(r['legal_review']['verdict']=='KEEP' for r in records),'legal_minor_edit':sum(r['legal_review']['verdict']=='MINOR_EDIT' for r in records),'realism_pass':sum(r['realism_review']['verdict']=='PASS' for r in records),'realism_fail':sum(r['realism_review']['verdict']=='FAIL' for r in records),'canonical_credit':0}}
save('reports/full-corpus-review/independent-phase13-c-review.json',report)
print(json.dumps(report['summary']))
