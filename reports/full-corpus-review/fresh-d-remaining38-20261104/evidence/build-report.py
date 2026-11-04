"""Actual reviewer-authored findings; this script formats them, never infers truth from key."""
import json, hashlib, datetime, shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
BASE=Path(__file__).resolve().parent.parent
E=BASE/'evidence'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rel(p): return str(Path(p).relative_to(ROOT))
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
packet=json.load(open(E/'postassignment-visible-input.json'))
assignment=json.load(open(E/'native-assignment.json'))
locators=json.load(open(E/'source-locators.json'))
family={r['question_id']:r['family_id'] for r in locators['records']}
comparisons=json.load(open(E/'nearest-visible-comparisons.json'))
nearest={r['question_id']:r for r in comparisons['records']}
choice_texts=list(dict.fromkeys(c['text'] for r in packet['records'] for c in r['original_visible_content']['choices']))
TRUE={0,4,6,7,11,12,14,15,18,21,22,23,25,29,30,31,32,36,37,41,42,44,47,50,51,52,54,58,59,60,61,65,67,71,72,74}
# Exact proposition-level findings independently written after actual primary reading.
F={
0:('적용 대상 VIS는 투여 전에 수령자 또는 법정대리인에게 제공해야 한다. 사후 영수증 동봉은 그 선행 의무를 충족하지 않는다. 특정 VIS가 필요한 백신이라는 stem 조건을 유지한다.','uscode-vis','§300aa-26(d)'),
1:('일반 약국 leaflet은 CDC가 정한 해당 VIS나 제품에 필요한 FDA/CDC fact sheet를 당연히 대체하지 못한다. 추가 설명은 가능하지만 요구 문서 자체의 제공을 없애지 않는다.','uscode-vis','§300aa-26(a),(d)'),
2:('나이만으로 screening을 마칠 수 없다. MA standing order는 투여 전 inclusion/exclusion criteria를 정하고 연령 등에 따른 용량·경로를 적용하게 한다. 알레르기·이전 반응·이전 투여에 관한 관련성 있는 정보가 빠진 Case B는 충분하지 않다.','src-6251c99ae2dd','III.C.2(c),(g); IX Appendix'),
3:('정책은 환자·백신의 inclusion/exclusion, 용량·경로를 다루도록 요구한다. 모든 환자와 모든 제품에 동일한 고정 문진표를 정했다는 규정은 없다.','src-6251c99ae2dd','III.C.2(c),(g); IX Appendix'),
4:('연령 확인과 투여 적격성 screening은 다른 판단이다. 연령을 맞췄다는 사실로 알레르기·반응·필요한 선행 용량 확인을 생략할 수 없다.','src-6251c99ae2dd','III.C.2(c),(g); IX Appendix'),
5:('VIS의 prior-to-administration 의무이므로 주사 뒤 제공은 같은 의무의 적법한 이행이 아니다.','uscode-vis','§300aa-26(d)'),
6:('연령과 기타 요인에 따른 timing/route/dose 및 inclusion/exclusion criteria를 실제 대상에 적용해야 한다. 새로운 보편 문진항목을 창설하는 뜻은 아니다.','src-6251c99ae2dd','IX Appendix; III.C.2(c),(g)'),
7:('105 CMR의 VIS 정의는 CDC risk/benefit 문서와 필요한 FDA/CDC 정보까지 구별해 포괄한다. 일반 leaflet을 해당 공식 제품 정보와 같다고 할 수 없다.','src-ec307e03cb52','222.003 VIS definition'),
8:('조회 행위는 새 투여 정보를 GUI 또는 data exchange로 보고하는 행위와 다르다. 자동 보고되었다는 사실은 stem에 없다.','src-ec307e03cb52','222.100(A),(C)'),
9:('인플루엔자·COVID 사전조회 예외는 Policy IV.E의 범위이다. IV.G와 222.100(A)의 새 투여 보고는 그대로 남는다.','src-6251c99ae2dd','IV.E,G; 105 CMR 222.100(A)'),
10:('COVID 권고에는 과거 formulation과 각 투여일 확인이 포함된다. 한번이라도 투여했는지만 묻는 것으로 축소하지 않는다. 권고를 의무로 바꾸지도 않는다.','src-6251c99ae2dd','IV.F'),
11:('인플루엔자/COVID 이외 백신의 MIIS 사전 확인을 단골 환자라는 이유로 면제하는 문구가 없다. 다른 제공자의 투여 여부도 확인하는 제도이다.','src-6251c99ae2dd','IV.E'),
12:('인플루엔자의 사전조회 예외와 모든 새 투여의 보고는 별개의 행위·규정이다. 따라서 Case B의 추론은 성립하지 않는다.','src-6251c99ae2dd','IV.E,G; 105 CMR 222.100(A)'),
13:('단골이라는 사정은 IV.E에 적힌 백신별 예외가 아니다. 이 첫 백신은 예외 대상이 아니므로 MIIS를 검토해야 한다.','src-6251c99ae2dd','IV.E'),
14:('기존 기록의 query만으로 오늘의 제조사·lot·투여일 등 새 자료가 보고되지 않는다. 조회와 제출은 구별해야 한다.','src-ec307e03cb52','222.100(A),(C)'),
15:('권고 원문에 prior formulation과 dates가 함께 명시된다. 약국 기록/EHR/MIIS/카드 등 확인 경로도 허용하며 이를 오직 MIIS 의무라고 확대하지 않는다.','src-6251c99ae2dd','IV.F'),
16:('필수 자료는 실제 immunization administration date이다. 더 늦은 업로드 일시는 그 날짜를 대체하지 못한다.','src-ec307e03cb52','222.100(C)(1)'),
17:('이름 없는 신생아의 birth dose는 이름이 정해진 뒤 24시간 경로이다. 일반 약국 새 투여를 다음 방문까지 미룰 수 있다는 포괄 예외가 아니다.','src-ec307e03cb52','222.100(A)'),
18:('월요일10시부터 금요일10시까지 96시간이다. 일반 72시간 기산점은 투여이며 특별 예외가 없으므로 목요일10시까지 보고해야 한다.','src-ec307e03cb52','222.100(A)'),
19:('이의서를 직접 받은 제공자는 수령 후 24시간 안에 Department에 반환해야 한다. 투여 후72시간 clock을 전용할 수 없다.','src-ec307e03cb52','222.105(B)(2)'),
20:('96시간인 금요일 계획은 투여 후72시간을 초과한다. 평일·영업일이라는 별도 조건은 이 조문에 없다.','src-ec307e03cb52','222.100(A)'),
21:('별도 기산점은 이의서 수령이고 기한은24시간이다. 예방접종 투여 시점의72시간과 다르다. GUI 상태변경 의무도 별도로 남는다.','src-ec307e03cb52','222.105(B)(2)'),
22:('최소 보고자료에 실제 투여일이 명시된다. 나중의 업로드 시각만으로는 해당 항목을 대신하지 못한다.','src-ec307e03cb52','222.100(C)(1)'),
23:('특례는 birth dose 당시 health record에 이름이 없는 신생아에 한하며 이름이 정해진 뒤24시간이다. 일반 약국 보고에 대한 다음방문 예외가 아니다.','src-ec307e03cb52','222.100(A)'),
24:('종이 보관만으로 이행되지 않는다. Department 반환과 GUI sharing status 변경이 모두 명시된다.','src-ec307e03cb52','222.105(B)(1),(2)'),
25:('data-sharing objection 정의는 Department 접근·사용을 제한하지 않으며, 새 투여 보고 의무도 존속한다. 다른 site와 공유하지 않는 것과 Department에 보고하지 않는 것은 다르다.','src-ec307e03cb52','222.003; 222.100(A); 222.105(B)(3)'),
26:('No 상태의 기록은 입력 site와 Department가 계속 접근할 수 있다. 삭제·말소라는 효과를 정한 조항이 아니다.','src-ec307e03cb52','222.105(B)(3),(4)'),
27:('로그인 자격은 목적 제한을 없애지 않는다. 직접 진료 등 열거된 목적만 허용되며 호기심으로 이웃 기록을 보는 것은 해당하지 않는다.','src-ec307e03cb52','222.200(C); 222.205(A),(B)'),
28:('공유 이의는 모든 새 투여의 Department 보고를 취소하지 않는다. 이의가 있는 사람도 시스템에 추가하고 No로 설정하는 규정과도 모순된다.','src-ec307e03cb52','222.003; 222.100(A); 222.105(B)(4)'),
29:('현 사용자의 유효한 로그인과 특정 환자정보에 접근할 법적 목적은 별개의 조건이다. 이웃에 대한 단순 호기심은 허용 목적이 아니다.','src-ec307e03cb52','222.200(C); 222.205(A),(B)'),
30:('No 상태여도 입력 site와 Department의 접근이 남는다. 타 site간 sharing을 제한하는 구조와 구별된다.','src-ec307e03cb52','222.105(B)(3)'),
31:('이의서 처리에는 Department에24시간 내 반환과 GUI status 변경이 함께 필요하다. 단지 종이를 보관한다는 것으로 끝나지 않는다.','src-ec307e03cb52','222.105(B)(1),(2)'),
32:('무료 소아 백신을 이용하지 않는 약국은19세 미만의 부모/보호자에게 잠재 비용과 PCP의 무료백신 옵션을 알려야 한다. 단순한 권고로 낮추지 않는다.','src-6251c99ae2dd','V.A; VI.B'),
33:('PCP에게 기록을 주라는 VI.A의 should와 MIIS에 보고해야 하는 IV.G의 must는 별개다. PCP 통지만으로 MIIS가 대체되지 않는다.','src-6251c99ae2dd','IV.G; VI.A'),
34:('인플루엔자/COVID 외 소아 예방접종 방문에는 지속적 pediatric/family practice 및 well-child care 관계의 중요성을 상담해야 한다. 접종 자체가 지속 진료의 대체재라는 뜻이 아니다.','src-6251c99ae2dd','VI.C'),
35:('정책 V.A는 백신 공급 자체를 무료로 제공한다는 내용이다. 모든 투여료·보험급여·가능한 비용까지 0이라고 결정하는 조항은 아니므로 이 보편 명제는 성립하지 않는다.','src-6251c99ae2dd','V.A; VI.B'),
36:('명시된 방문은 VI.C의 인플루엔자/COVID 제외 조건을 충족한다. 지속적 primary/well-child care에 대한 상담이 필요하고 필요시 지역 PCP 정보도 제공한다.','src-6251c99ae2dd','VI.C'),
37:('무료 공급과 투여행위 비용·개별 보험 지급은 동일한 주장으로 취급할 수 없다. 이 보기는 특정 수수료 부과 허가를 새로 주장하는 내용이 아니다.','src-6251c99ae2dd','V.A; VI.B'),
38:('제조사가 추가 투여 금기로 정한 adverse event는 명시적 보고범주에 들어간다. 제외라는 말은 정책과 연방 보고범주를 뒤집는다.','src-6251c99ae2dd','VII.A; 42 USC 300aa-25(b)(1)(B)'),
39:('MIIS는 투여 정보이고 VAERS는 이상사건 보고이다. 한 시스템의 dose 기록이 다른 시스템의 제출을 완료한다는 조항은 없다.','src-6251c99ae2dd','IV.G; VII.A,B; 105 CMR 222.100(A)'),
40:('VAERS 제출은 응급처치나 별도로 발동하는 Board 보고의 면제가 아니다. stem은 Board trigger가 발생했다는 사실을 추가하지 않으며 any otherwise required라는 제한을 유지한다.','src-6251c99ae2dd','IX emergency procedures; VII; 247 CMR 20.02(1)-(3)'),
41:('해당 table의 사건·기간 조건이 충족된 상황에서 인과관계 확정은 보고의 추가 선행조건이 아니다. VAERS 공식 안내도 불확실한 인과관계 상태의 보고를 명시한다.','vaers','Healthcare providers required by law; reporting even if unsure vaccine caused event'),
42:('MIIS dose 보고 의무와 VAERS reportable event 보고 의무가 병존한다. MIIS를 입력했어도 해당 VAERS 제출은 남는다.','src-6251c99ae2dd','IV.G; VII.A,B'),
43:('정해진 사건·기간의 보고 의무에 causation proof를 더하면 보고를 부당하게 미룬다. 현 stem은 reportable event라는 조건을 이미 준다.','vaers','Healthcare providers required by law; uncertain causation reporting'),
44:('제조사가 추가 용량의 금기로 명시한 adverse event는 Policy VII.A와 연방 statute의 보고범주에 해당한다.','src-6251c99ae2dd','VII.A; 42 USC 300aa-25(b)(1)(B)'),
45:('CDC는 외관이 적정 보관의 신뢰할 지표가 아니라고 명시한다. 시간·온도·제품 정보를 평가하지 않고 정상 외관만으로 사용가능하다고 할 수 없다.','cdc-storage','Section One p5; Section Three p15 Temperature Excursions'),
46:('약국이 미리 뽑는 행위와 제조사가 충전한 완제품은 같은 조제 상황이 아니다. MA의 greater-than-1-hour predrawing 조항은 약국의 미래사용 준비에 적용된다.','src-6251c99ae2dd','VIII.B'),
47:('2025개정 공식 MA 정책은 미래사용을 위한1시간 초과 drawing을 sterile compounding으로 정하고 sterile conditions/USP797 준수를 요구한다. 다른 USP immediate-use 숫자로 이 정책문언을 바꾸지 않는다.','src-6251c99ae2dd','VIII.B'),
48:('예방접종 교육 이수만으로 retail sterile compounding의 별도 법정 license나 적용되는 환경·기술 요건이 면제되지 않는다.','ma-sterile-license','MGL c112 §39G(a)(1),(4); Policy VIII.B'),
49:('백신이라는 이유만으로 정책 VIII.B의 대상에서 빠지지 않는다.2시간은 명시된1시간 초과 조건에 든다.','src-6251c99ae2dd','VIII.B'),
50:('정상 외관은 안정성·potency 보장의 근거가 아니다. 노출 제품을 표시·분리하고 제조사/프로그램에 시간·온도자료로 문의해야 한다는 CDC 지침과 일치한다.','cdc-storage','Section One p5; Section Three p15 Temperature Excursions'),
51:('투여자격은 sterile-compounding 시설 license·작업능력의 대체물이 아니다. 법은 retail sterile license를 다른 license에 추가해 요구한다. 요구되는 경우라는 보기의 한정을 보존한다.','ma-sterile-license','MGL c112 §39G(a)(1),(4); Policy VIII.B'),
52:('제조사의 prefilled product와 약국에서 미래사용을 위해 drawn syringe를 동일한 준비행위로 취급하면 VIII.B의 별도 규제를 지운다.','src-6251c99ae2dd','VIII.B'),
53:('circular의 이 경로는18세 이상이며 IV는 금지된다. 목록 약물이라는 사실만으로17세/정맥투여의 두 결함을 치유하지 않는다.','src-368bb8382bd0','Dispensing by Administration pp1-2 (b)-(f); Administration and Dosing p3'),
54:('circular는 pharmacist 또는 pharmacy intern을 행위자로 열거한다. 백신정책의 technician 권한을 일반 약물투여 경로로 자동 확장할 수 없다.','src-368bb8382bd0','Purpose; Dispensing by Administration pp1-2'),
55:('약물목록에 드는 것은 한 조건이다. valid Rx, single-dose packaging 및 single-dose prescription 조건이 추가로 명시된다.','src-368bb8382bd0','Dispensing by Administration (b),(d)'),
56:('MCSR 없이 투여할 수 있는 주체는 조건부 pharmacist/intern이다. 그 제한된 행위 면제를 약국 store registration 전체 면제로 확장할 근거가 없으며 c112 §39의 시설 등록 체계가 별도로 있다.','ma-facility','MGL c112 §39; Circular Dispensing by Administration pp1-2'),
57:('백신 technician 요건을 충족해도 이 circular의 pharmacist/intern이라는 행위자 제한에 technician이 추가되지 않는다.','src-368bb8382bd0','Purpose; Dispensing by Administration pp1-2'),
58:('17세는18세 이상 조건을 못 맞추고 IV는 명시적 금지 및 SC/IM 제한에 어긋난다. 다른 예외 경로까지 보편 금지라고 확대하지 않는 이 경로 한정 결론이다.','src-368bb8382bd0','Dispensing by Administration pp1-2; Administration and Dosing p3'),
59:('개인의 조건부 MCSR 예외와 약국의 별도 시설 registration은 행위자와 목적이 다르다. 전자를 시설의 모든 등록의무 면제로 읽을 수 없다.','ma-facility','MGL c112 §39; Circular Dispensing by Administration pp1-2'),
60:('목록 적격성과 별개로 valid Rx 및 single-dose packaging/prescribed single doses 요건이 남는다. refill 자체는 허용되어 single-dose와 단1회 처방을 혼동하지 않는다.','src-368bb8382bd0','Dispensing by Administration (b),(d)'),
61:('먼저 해당 약물·환자집단에 적합한 accredited training을 받고 지속 competence를 유지해야 한다. 낯선 LAI에 대해 vaccine course만으로 보편 숙련을 추정할 수 없다.','src-368bb8382bd0','Training; Continued Competency p3'),
62:('교육 이수와 manufacturer labeling/해당 REMS 준수는 병행 조건이다. 훈련으로 제품별 제약을 override할 수 없다.','src-368bb8382bd0','Administration and Dosing—Manufacturers Instructions p3'),
63:('현재 CPR certification은 독립적으로 must maintain이라 규정된다. 약물 competence가 있다는 것으로 대체되지 않는다.','src-368bb8382bd0','CPR Certification p3'),
64:('continued competence 조항은 CE를 가능한 한 방법으로 들며 임의의 고정 연간 CE 숫자를 법으로 정하지 않는다. 내부 정책 숫자를 circular 원문이라고 부를 수 없다.','src-368bb8382bd0','Continued Competency p3'),
65:('이 circular에는 injector용 보편 고정 연간 CE 숫자가 없다. 다른 pharmacy renewal/vaccine CE 의무가 없다는 뜻은 아니며 내부 기준과 이 circular의 요구를 구별한 보기이다.','src-368bb8382bd0','Training; Continued Competency p3'),
66:('훈련은 실제 medication/population에 적합해야 하고 competence도 유지해야 한다. vaccine course가 모든 LAI preparation/observation/REMS 숙련을 conclusively 증명한다는 결론은 과도하다.','src-368bb8382bd0','Training; Continued Competency; Administration and Dosing p3'),
67:('약사/intern의 이 활동에 현재 CPR certification을 계속 유지할 의무가 따로 명시된다.','src-368bb8382bd0','CPR Certification p3'),
68:('권고 notation이라는 점은 실제 의미 있는 의도상 의문을 무시할 근거가 아니다. 원문은 전문판단에 따른 prescriber contact를 encouraged로 두며 이를 보편적인 법정 전화 의무로 올리지 않는다.','src-368bb8382bd0','Pharmacist-Prescriber Communication pp4-5'),
69:('quarterly는 such as의 예시이고 간격은 prescriber가 정한다. 적정 refill prescription을 막지 않는다고 명시하므로 정확90일마다 새처방이라는 보편 명령은 아니다.','src-368bb8382bd0','Prescriber Assessment p3; Dispensing by Administration (e)'),
70:('환자 consent 기록과 투여 전 customary counseling은 별개의 요구다. 서명만으로 상담 행위를 했다고 할 수 없다.','src-368bb8382bd0','Pre-administration Patient Counseling p3; Record Keeping p4'),
71:('notation은 should include이고 없는 처방에 대한 contact도 encouraged/전문판단 조건이다. 이 누락만으로 유효한 적격 처방을 자동 무효화하는 조항은 없다.','src-368bb8382bd0','Pharmacist-Prescriber Communication pp4-5'),
72:('quarterly는 예시이며 prescriber가 적정 interval을 정한다. 유효 처방의 refill 허용과 양립하고 보편90일 새처방 clock을 만들지 않는다.','src-368bb8382bd0','Prescriber Assessment p3'),
73:('recommended notation을 absolute validity condition으로 바꾸면 should/encouraged를 must로 오독한다. 처방 유효성의 다른 조건을 면제하는 결론도 아니다.','src-368bb8382bd0','Pharmacist-Prescriber Communication pp4-5'),
74:('실제 중요한 의도상 불확실성은 전문판단으로 적절히 확인하는 것이 타당하다. should appropriately는 모든 notation 누락마다 반드시 전화하라는 주장과 다르며 circular는 contact를 encourages한다.','src-368bb8382bd0','Pharmacist-Prescriber Communication pp4-5')}
assert set(F)==set(range(75)) and len(choice_texts)==75

source_sections={
'src-368bb8382bd0':('DCP 26-03-124: pp1-5, especially eligibility, training/CPR/competency, counseling, reassessment and communication','2026-03-11 circular; replaces DCP23-04-118 explicitly. Separate legal commencement date is not printed; UNKNOWN rather than assumed.'),
'src-6251c99ae2dd':('Policy2023-02: III.C; IV.D-G; V; VI; VII; VIII; IX','Adopted2023-05-04; revised2023-09-07 and2025-09-04 printed. Separate commencement date UNKNOWN; current official download retrieved2026-11-04.'),
'src-ec307e03cb52':('105 CMR222.003,222.100(A),(C),222.105(B),222.200(C),222.205(A),(B)','Mass.Register1528,2024-08-16 printed edition. Separate commencement/history beyond that edition UNKNOWN; current official download retrieved2026-11-04.'),
'src-aea01b105528':('247 CMR20.02(1)-(3),20.07','Mass.Register1536,2024-12-06 printed edition; exact commencement apart from edition UNKNOWN; Board duty cited only if independently triggered.'),
'uscode-vis':('42 USC300aa-26(a),(d)','Official2024 USCode edition; last listed amendment1993. Prior-administration duty corroborated by current live CDC page. Secretary-specific historical initial distribution date UNKNOWN; no universal all-vaccine claim made.'),
'uscode-vaers':('42 USC300aa-25(b)(1)(A),(B)','Official2024 USCode edition; effective-date note1987-12-22 and reporting beginning90days thereafter. Current live VAERS page corroborates report categories; exhaustive2025-26 legislation census NOT_RUN.'),
'cdc-vis':('VISs are required by law; Ways to give a VIS','Page dated2024-08-02; current live official agency guidance retrieved2026-11-04. Guidance does not supply a new statutory effective date.'),
'vaers':('Healthcare providers required by law; reportable events and uncertainty about causation','Live official VAERS reporting page retrieved2026-11-04. Specific version/effective date not printed in retrieved body: UNKNOWN; underlying law separately bound.'),
'cdc-storage':('March2024 Toolkit: SectionOne printedp5; SectionThree printedp15 TemperatureExcursions','Toolkit cover March29,2024. Clinical recommendations, not a new generally binding statute. Current official served PDF; no later edition census or manufacturer-specific product disposition determined.'),
'ma-facility':('MGLc112§39 registration/permit of retail drug business','Current official legislature section retrieved2026-11-04; amendment/commencement date not printed in section: UNKNOWN. Used only to distinguish facility registration from individual administration exception.'),
'ma-sterile-license':('MGLc112§39G(a)(1),(4)','Current official legislature section retrieved2026-11-04; specific amendment commencement not printed: UNKNOWN. No full USP copyrighted text retrieved or republished.')}
sources=[]
for sid,(section,version) in source_sections.items():
 m=json.load(open(E/(sid+'.meta.json'))); assert m['http_status']==200
 raw=E/(sid+'.raw'); txt=E/(sid+'.txt'); meta=E/(sid+'.meta.json')
 sources.append({'source_id':sid,'authority':sid,'source_type':'PUBLIC_OFFICIAL','official_url':m['official_url'],'exact_section':section,'coverage':section,'law_checked_date':'2026-11-04','effective_date':None,'version_and_commencement_basis':version,'evidence_path':rel(txt),'evidence_sha256':sha(txt),'raw_evidence_path':rel(raw),'raw_sha256':sha(raw),'text_evidence_path':rel(txt),'text_sha256':sha(txt),'metadata_path':rel(meta),'metadata_sha256':sha(meta),'retrieval_provenance':m,'retrieved_at':m['retrieved_at']})
S={s['source_id']:s for s in sources}

context={
'VAX09':'VIS 선행 제공과 실제 투여 전 screening',
'VAX10':'백신별 MIIS 사전조회 예외와 모든 새 투여의 보고',
'VAX11':'월요일10시 투여의72시간 및 이의서 수령의24시간',
'VAX12':'MIIS 공유 이의 처리·Department 접근·목적 제한',
'VAX13':'무료 소아백신 미사용 비용고지와 ongoing primary care',
'VAX14':'VAERS 사건/기간 조건·인과관계 불확실성과 별도 MIIS',
'VAX15':'2시간 predrawing·sterile 조건과 온도이탈 제품 평가',
'VAX16':'백신 technician과 일반 약물투여자·18세/경로/포장/등록',
'VAX17':'제품별 교육·competence·CPR와 존재하지 않는 고정CE 숫자',
'VAX18':'권고 notation·prescriber가 정하는 reassessment·사전상담'}
# These are item-specific editorial findings, not family-count failures.
realism_fail={
321:'Case A의 VIS 시간을 묻는데 다른 보기는 screening·모든 제품 공통표를 말한다. 법규를 몰라도 사례 일치와 necessarily라는 과장으로 답이 드러난다.',
322:'Case B를 묻는 유일한 현실적 screening 답과, 사후VIS/일반leaflet/동일문진표를 섞었다. 실제 competing interpretation보다 주제 매칭이 정답 단서다.',
323:'세 오답이 사후VIS로 선행의무 충족·나이만 screening·일반leaflet의 모든문서 대체이다. 단일 참 SATA 자체는 허용되나 세 오답이 과장되어 진짜 혼동을 충분히 만들지 못한다.',
324:'모든 백신·모든 환자에게 동일표를 정했다는 보기가 유독 절대적이다. 실제 법규 예외 판단 없이 범용화 문장만 제거할 수 있다.',
325:'Case A를 묻는 답만 단골의 MIIS 조회 예외를 직접 다루고 나머지는 투여기록·인플루엔자·COVID 권고다. 사례 매칭으로 유일 답을 찾기 쉽다.',
326:'Case B의 influenza reporting을 직접 반박하는 보기만 관련 있고 나머지는 단골/조회자동기록/COVID다. 법규상 옳지만 단서가 과하다.',
329:'Case A의 Monday-Friday 기간을 직접 다룬 유일 보기가 정답이다. 다른 세 보기는 업로드날짜·newborn·이의서이므로72시간을 몰라도 주제를 맞출 수 있다.',
330:'Case B의 이의서 전달을 다루는 유일 보기가 정답이다. 다른 보기들은 별개 신규 투여 clock·newborn·업로드일이므로 답이 범위로 드러난다.',
333:'Case A의 Department reporting을 다루는 유일 적절한 보기에 대하여 다른 보기는 GUI처리/기록삭제/이웃조회다. 대상사례와 보기의 직접 연결이 단서이다.',
334:'Case B의 이웃 호기심 접근에 답하는 보기가 하나뿐이다. 나머지 보기의 공유이의/삭제/서류처리는 그 질문에 응답하지 않는다.',
337:'Case A의 비용고지라는 정답만 그 사례의 직접 행위를 다룬다. 다른 보기들은 PCP통지/지속진료/모든수수료0이라는 뚜렷한 과장이다.',
341:'Case A의 causation proof를 직접 다루는 보기만 정답이다. 다른 보기들의 제조사 범주/MIIS 대체/응급처치 면제는 다른 주제여서 주제 매칭으로 풀린다.',
342:'Case B의 MIIS와VAERS 대체관계를 직접 말하는 보기가 유일하다. causation proof/제조사범주/응급면제를 분리해 놓아 실제 경쟁하는 처리결정이 약하다.',
343:'SATA의 인과관계·제조사 금기 범주는 실제 판단 대상이지만, VAERS 제출이 즉각적 환자처치를 면제한다는 B는 지나치게 비현실적이다. 부정극성 문항344에서 같은 명제에 적용한 distractor 기준을 일관되게 적용한다.',
344:'VAERS를 내면 즉각적 환자처치까지 불필요하다는 보기는 지나치게 비현실적이다. 오류선택 극성은 맞지만 법규를 모르는 수험자에게도 드러나는 오답이다.',
345:'Case A를 직접 다루는1시간 기준 보기에 비해 나머지는 외관/제조충전상태/교육면제이다. 시간기준을 몰라도 주제와 가장 구체적 문구로 답이 드러난다.',
346:'Case B의 외관·온도이탈에 답하는 보기가 하나뿐이고 다른 보기는 전부compounding이다. 문제는 실제 약제 disposition 결정까지 요구하지 않는다.',
349:'Case A technician의 general pathway 포함 여부에 답하는 유일 보기가 정답이다. 다른 보기는17세IV/포장/시설등록으로 사례선택 단서가 크다.',
350:'Case B의17세IV라는 두 조건에 맞춘 유일 보기가 정답이고 나머지는 technician/포장/등록이다. 최소 하나라도 부적격인 나이와경로를 동시에 명시해 실제 예외분석이 약하다.',
353:'Case A의 낯선LAI 훈련에 맞춘 정답과 교육이REMS를override/competence가CPR대체/임의CE를법이라고 부르는 극단적 오답이다. 진짜 교육범위 경쟁이 부족하다.',
354:'Case B가 숫자가circular에 없다고 이미 단정하고 답도 unstated라는 사실을 되풀이한다. 원문을 읽지 않아도 결론이 주어진다.',
355:'CPR 이외 세 보기는 임의숫자를법으로 귀속·훈련으로REMSoverride·vaccinecourse가모든LAI를conclusively인증하는 과장이다. SATA 선택을 위한 법규 판단부담이 낮다.',
356:'training overrides manufacturer/REMS라는 극단적 보기가 유일 오류이다. 적격교육의 구체 조건이나 실제제품 관찰조건을 적용할 수 없다.',
357:'Case A가 valid eligible prescription이라고 이미 전제하고 recommended notation만 누락했다고 써 자동무효가 아니라는 답을 제공한다. 다른 보기들은 무시/90일/동의대체의 극단이다.',
358:'Case B가 example을 mandatory90일로 바꿨다고 직접 서술해 그 추론이오류임을 알려준다. 다른 보기는 별개 상담/의도/notation이므로 문구로 답을 추측할 수 있다.',
359:'SATA라도 stem이 valid eligible prescription과 recommended notation을 명시해 D의 참을 제공하고 quarterly를 예시라고 명시해 B의 거짓을 제공한다. 보기 일부의 답을 stem의 평가용 표현이 미리 알려 주므로 wording 기준을 충족하지 못한다.'}

records=[]
for row in packet['records']:
 q=row['original_visible_content'];qid=row['question_id'];num=int(qid.split('-')[-1]);fam=family[qid];topic=context[fam]
 choices=[]
 for c in q['choices']:
  idx=choice_texts.index(c['text']);reason,sid,section=F[idx];auth=dict(S[sid]);auth['exact_section']=section
  extra=[]
  if fam in ('VAX09',):extra=['src-6251c99ae2dd','src-ec307e03cb52','uscode-vis','cdc-vis']
  if fam in ('VAX10','VAX11','VAX12'):extra=['src-6251c99ae2dd','src-ec307e03cb52']
  if fam=='VAX14':extra=['src-6251c99ae2dd','uscode-vaers','vaers','src-aea01b105528']
  if fam=='VAX15':extra=['src-6251c99ae2dd','cdc-storage','ma-sterile-license']
  if fam=='VAX16':extra=['src-368bb8382bd0','ma-facility']
  choices.append({'choice_id':c['id'],'option_text':c['text'],'option_sha256':hashlib.sha256(c['text'].encode()).hexdigest(),'statement_supported':idx in TRUE,'selected_under_question_polarity':None,'finding_ko':reason,'authority':auth,'supporting_authorities':[S[k] for k in extra if k!=sid]})
 incorrect='INCORRECT' in q['stem']; expected=[c['choice_id'] for c in choices if c['statement_supported'] != incorrect]
 assert expected==q['correct_choice_ids'],(qid,expected,q['correct_choice_ids'])
 assert len(expected)>=1 and (q['question_type']=='SATA' or len(expected)==1)
 for c in choices:c['selected_under_question_polarity']=c['choice_id'] in expected
 scope={'original_stem':True,'stored_key_read':True,'complete_core_reasoning_read':True,'learning_boundary_read':True,'all_choices_read':[c['id'] for c in q['choices']],'all_choice_explanations_read':list(q['explanation']['choice_analysis']),'hidden_statement_truth_read':False,'prior_question_author_or_independent_verdicts_read':False,'preassignment_full_visible_read':True,'postassignment_current_hash_binding':True,'visible_input_path':rel(E/'postassignment-visible-input.json'),'visible_input_sha256':sha(E/'postassignment-visible-input.json')}
 explanation_findings={c['choice_id']:{'read_completely':True,'original_explanation_text':q['explanation']['choice_analysis'][c['choice_id']],'assessment':'ACCURATE_WITH_SCOPE_LIMITS','finding_ko':c['finding_ko']} for c in choices}
 auths={c['authority']['source_id']:S[c['authority']['source_id']] for c in choices}
 for c in choices:
  for a in c['supporting_authorities']:auths[a['source_id']]=a
 if fam=='VAX13':auths['src-6251c99ae2dd']=S['src-6251c99ae2dd']
 legal={'existing_answer_correct':'YES','stored_key':q['correct_choice_ids'],'independently_expected_key':expected,'question_polarity':'SELECT_INCORRECT' if incorrect else 'SELECT_TRUE_STATEMENTS' if q['question_type']=='SATA' else 'SELECT_ONE_CORRECT','key_uniqueness_ko':('INCORRECT 극성에서 거짓 명제만 선택한다. 참인 나머지 보기를 오답으로 뒤집지 않았다.' if incorrect else 'SATA는 모든 보기를 독립 판단한 참 집합과 키가 정확히 같다. 전부참/참1개도 허용 형식이며 조합을 누락하지 않았다.' if q['question_type']=='SATA' else '사례가 묻는 행위와 모든 보기의 참거짓을 대조했고 참인 보기는 하나로 유일하다.'),'per_choice_findings':choices,'authorities':list(auths.values()),'verdict':'KEEP','finding_ko':topic+'에 관한 원문 조건과 예외를 유지하면 기존 키와 한국어 해설은 맞다. 법규 KEEP은 별도 현실성 결함을 없애는 판정이 아니다.','exception_scope_ko':('적용VIS가필요한 백신이라는 전제이며 모든백신에동일문서를요구하지않는다.' if fam=='VAX09' else '인플루엔자/COVID 사전조회 예외를 새투여보고 면제로 확대하지않는다.' if fam=='VAX10' else '이름없는신생아birthdose의특수기산점을 일반약국지연으로 확대하지않는다.' if fam=='VAX11' else '공유거부가Department 접근이나 법정보고를 없애지않는다. 로그인은 목적제한을해제하지않는다.' if fam=='VAX12' else '19세미만·무료stock미사용 및 influenza/COVID제외 childhoodvisit이라는 각각의 조건을 유지한다.' if fam=='VAX13' else '해당 reportable event와기간조건이충족된다는전제; 모든이상사건을법적의무라고일괄확장하지않고Board trigger도추가추정하지않는다.' if fam=='VAX14' else 'MA정책의1시간초과문언을USP의다른숫자로대체하지않으며제품의실제사용가능판정은별도평가한다.' if fam=='VAX15' else '이circular의성인·nonIV/SCIM·주체·포장/Rx한정이며다른별도권한까지금지한다고확장하지않는다.' if fam=='VAX16' else 'circular에없는고정CE숫자와별도의vaccine/일반갱신CE를구별한다.' if fam=='VAX17' else 'quarterly는예시, notation은권고, contact는전문판단에따른encouraged이며모든누락에법정의무전화라고격상하지않는다.'),'ma_federal_relationship_ko':('연방의해당VIS 선행제공 의무와MA의screening·standingorder 요건은병행한다.' if fam=='VAX09' else 'MIIS의기한·공유·목적제한은MA규정이다. 연방VIS또는VAERS보고가이를대체하지않는다.' if fam in ('VAX10','VAX11','VAX12','VAX13') else 'MA정책은연방보고범주와연결된VAERS를요구하며MIIS·응급처치·별도Board보고는각각병존한다.' if fam=='VAX14' else '이판정의1시간은MA정책문언이며CDC보관권고를새연방법정기한으로취급하지않는다.' if fam=='VAX15' else '이투여권한은MA의제한된경로이며FDA승인표시·적용REMS준수가조건이다. 연방승인만으로MA주체/연령/경로제약이면제되지않는다.'),'blocker':None,'original_explanation_review':{'core_reasoning_read_completely':True,'core_reasoning_text':q['explanation']['core_reasoning'],'core_assessment':'ACCURATE_WITH_SCOPE_LIMITS','core_finding_ko':topic+'에 대한 핵심 설명을 전부 읽었다. 보기별 아래 근거와 일치하며 학습경계를 다른 독립사례로 과장하지 않았다. 권고/의무와 조건은 위 exception_scope에 한정한다.','all_choice_explanations_read':True,'choice_findings':explanation_findings,'learning_boundary_read_completely':True,'learning_boundary_text':q['explanation']['learning_boundary'],'learning_boundary_assessment_ko':'같은family의공유사례변형이라는설명은원문과일치한다. 이존재만으로독립성/현실성을일괄FAIL하지않았다.'}}
 fail=num in realism_fail
 criteria={k:True for k in ('jurisprudence_reasoning','practice_plausibility','authentic_distractors','wording_not_guessable','reasoning_not_trivia','natural_rule_combination','appropriate_drug_context','distinct_from_bank','not_schedule_flashcard','public_style_without_copying')}
 findings={
 'jurisprudence_reasoning':topic+'에서 허용/의무와 요건 적용을 구별하므로 최소한의 법적 판단은 있다.',
 'practice_plausibility':topic+'는 약국의 실제 투여/보고/상담 흐름에서 일어날 수 있다. 두사례의 개별행위 자체는 현실적이다.',
 'authentic_distractors':'보기별 근거와 같이 '+topic+'에 관한 주체·예외·의무혼동을 검토한다. SATA에서 모든보기가 참이어도 명제별 판단이 필요해 형식만으로 실패시키지 않는다.',
 'wording_not_guessable':('SATA의모든보기를판단하고참집합을골라야하며특정사례만직접대답하는유일보기문제가없다.' if q['question_type']=='SATA' else 'INCORRECT극성의모든보기를읽고실제오류명제를구별해야한다. 부정극성이라는사실자체를실패사유로삼지않았다.'),
 'reasoning_not_trivia':topic+'에서 제도/행위의 범위와 예외를 적용하는 문제이며 약물번호나 명칭을 고립 암기하는 문제가 아니다.',
 'natural_rule_combination':topic+'에 관한 두규칙은 같은백신/주사서비스의 업무에서 만난다. 별개의Case A/B를 한환자에서 발생한 사실로 덧붙이지 않았다.',
 'appropriate_drug_context':'약물명보다 '+topic+'의 절차/권한이 결정적이다. 특정브랜드·용량을 추가하지 않아도 이법적 판단이 가능하고 불필요한 brandtrivia가 없다.',
 'distinct_from_bank':'canonical439와공개2349에서측정해가장가까운원문stem/모든보기를실제읽었다. canonical최근접은아래비교처럼다른판단/상황이다. 공개최근접은같은family공유사례변형이며learning_boundary와공개landing의family당세트1개맥락상존재만으로실패시키지않았다. 별개의새사례로숫자를부풀려표현해서는안된다.',
 'not_schedule_flashcard':topic+'의 투여·상담·보고 요건을 적용하며 schedule 이름만 묻지 않는다.',
 'public_style_without_copying':'SBA/SATA/INCORRECT의공개selected-response구조로판단했다. 상용bank/PreMPJE/회상/유출문항은열지않았으며공개NABP표본의문구대조나복제는하지않았다. 이criterion은검토세션의허용스타일사용판정이고모든저작물에대한독립유래증명은아니다.'}
 if fail:
  criteria['wording_not_guessable']=False;findings['wording_not_guessable']=realism_fail[num]
  if num in (323,324,344,353,354,355,356,357,358):criteria['authentic_distractors']=False;findings['authentic_distractors']=realism_fail[num]
  if num in (354,358):criteria['reasoning_not_trivia']=False;findings['reasoning_not_trivia']='stem이원문에없거나단지예시라고이미서술한내용을되풀이하는답이므로실제법규판단이탈락한다.'
  if num==343:
   criteria['wording_not_guessable']=True
   criteria['authentic_distractors']=False
   findings['wording_not_guessable']='두 참 명제인 인과관계 불확실성과 제조사 금기를 모두 고르려면 단순한 주제 매칭 이상의 판단이 필요하다. FAIL 원인은 별도의 비현실적인 환자처치 면제 distractor이다.'
   findings['authentic_distractors']=realism_fail[num]
 comparison=nearest[qid]; can,pub=comparison['candidates']
 duplicate={'method':comparison['metric'],'candidate_pools':comparisons['pool_counts'],'evidence_path':rel(E/'nearest-visible-comparisons.json'),'evidence_sha256':sha(E/'nearest-visible-comparisons.json'),'nearest_candidates':[{'pool':c['pool'],'question_id':c['visible']['question_id'],'score':c['score'],'stem_and_all_choices_actually_read':True} for c in comparison['candidates']],'canonical_comparison_ko':f"{can['visible']['question_id']}의원문을읽었다: {can['visible']['stem']} / 본문항은 {topic}를묻는다. 공유일반단어가검색순위를올리지만같은factpattern/정답행위의복제는아니다.",'public_comparison_ko':f"{pub['visible']['question_id']}는원문두Case와많은판단을공유한다. 원문stem/모든보기를읽고질문극성/목표사례차이를확인했다. 독립적인새임상사례로세지않는family연습변형이다. 공개landing은한세트에family당1개를말하며미검토payload를공개시험모드에넣지않는다고설명한다. 실제defaultUI실행검사는NOT_RUN이며가까운문항의존재만으로FAIL하지않았다.",'semantic_verdict':'INTENTIONAL_SHARED_CASE_VARIANT; CANONICAL_NEAREST_DIFFERENT_DECISION','default_pool_runtime_test':'NOT_RUN; landing/context read only; no default bank mutation'}
 realism={'verdict':'FAIL' if fail else 'PASS','decision':'MAJOR_REWRITE' if fail else 'KEEP','criteria':criteria,'criterion_findings_ko':findings,'finding_ko':realism_fail.get(num,topic+'의선택지별조건과예외를실제대조해야하고공개최근접family변형은독립새사례로계수하지않는다는한계에서10기준을충족한다.'),'duplicate_review':duplicate}
 records.append({'question_id':qid,'record_sha256':row['record_sha256'],'family_id':fam,'read_scope':scope,'legal_review':legal,'realism_review':realism,'safe_hold_recommended':fail,'release_eligible':False,'required_next_action_ko':('보기의직접사례매칭/과장단서를줄이고실제경쟁하는적법업무선택으로editor가고친뒤새currenthash독립감사한다.' if fail else '이artifact는legacy독립검토일뿐이다. canonical초기감사·adjudication·release gates를별도로충족하기전release하지않는다.')})

profile=ROOT/'data/exam_style/mpje_style_profile.json';style=json.load(open(profile))
bound_at=datetime.datetime.now(datetime.timezone.utc).isoformat()
policies={}
for path in ('docs/INDEPENDENT_LEGACY_REVIEW_RUNBOOK.md','docs/RELEASE_POLICY.md','docs/AUDIT_WORKFLOW.md','docs/SOURCE_USE_POLICY.md','docs/QUESTION_AUTHORING_STANDARD.md','schemas/question.schema.json','schemas/audit.schema.json','schemas/exam_style_profile.schema.json'):
 policies[path]={'file_sha256':sha(ROOT/path),'actually_read':path.startswith('docs/')}
out={'schema_version':'independent-legacy-full-visible-review/1','stage':'independent-legacy','job_id':assignment['job_id'],'independent_of_authors':True,'auditor':'GPT','auditor_instance':'GPT:/root/fresh_d_remaining38:20261104','actor_provenance':{'actor_id':'/root/fresh_d_remaining38','session_id':'/root/fresh_d_remaining38'},'canonical_audit':False,'canonical_release_credit':0,'release_eligible':False,'reviewed_at':'2026-11-04','postassignment_bound_at':bound_at,'native_assignment_binding':{k:assignment[k] for k in ('job_id','sequence','question_hashes','stage','worker','worker_branch','attempt')},'question_hashes':assignment['question_hashes'],'input_provenance':{'preassignment_path':rel(E/'preassignment-visible-input.json'),'preassignment_sha256':sha(E/'preassignment-visible-input.json'),'postassignment_path':rel(E/'postassignment-visible-input.json'),'postassignment_sha256':sha(E/'postassignment-visible-input.json'),'postassignment_export_matches_preassignment_visible_content':json.load(open(E/'preassignment-visible-input.json'))['records']==packet['records'],'chronology_ko':'실제세션은nativeclaim전원문읽기를시작했다. 이읽기는preassignment로구분한다. root가actualexact38nativeclaim을만든뒤공식exporter를실행해38개전체recordhash를검증하고current원문과독립판정을묶었다. 과거읽기를소급해native배정후새읽기라고부르지않는다. 이전author/independent보고서·ledgerpriorverdict·숨은_truth는읽지않았다. 가까운bank비교는visible필드만추출했다. publication에는전체미검토상태집계가우발적으로보였으나개별기존판정/결론은노출되지않았고판정근거로사용하지않았다.'},'policies_and_schemas':policies,'style_profile':{'profile_id':style['profile_id'],'version':style['content_version'],'semantic_hash':style['content_hash'],'file_sha256':sha(profile),'valid_for_exams_before':style['valid_for_exams_before']},'sources':sources,'retrieval_failures':[{'source_id':sid,'metadata_path':rel(E/(sid+'.meta.json')),'metadata_sha256':sha(E/(sid+'.meta.json')),'counted_as_authority':False,'reason':'Actual404; alternate official evidence obtained, failed body not treated as law.'} for sid in ('federal-vis','federal-vaers','ma-sterile')],'network_provenance':{'cloud_skill':'cloud-environment-runtime; networking reference read','network_policy':'unrestricted/enforced; vpn_configured false','firecrawl':'Actual insufficient-credit failure; not retried. Official HTTPS via inherited proxy and normal TLS used.','fresh_cache_reuse':False},'limitations_ko':['canonicalcredit0/releasefalse. positivelegacy판정은RELEASED승격이아니다.','공식served현재문서는확보했지만모든연혁·gazette·2025-26미반영연방법률을전수조사했다고주장하지않으며version/commencement의UNKNOWN을source별로명시했다.','ClassD/상용문항/USP전문은입력하지않았다.법적으로서로다른활동의예외를임의결합하지않았다.','실제defaultUI실행검사는NOT_RUN이다.공개landing의family당세트1개맥락과원문학습경계및nearest원문을읽어distinctness를한정판정했다.'],'records':records,'summary':{'records':len(records),'legal_KEEP_answer_YES':len(records),'realism_PASS':sum(r['realism_review']['verdict']=='PASS' for r in records),'realism_FAIL':sum(r['realism_review']['verdict']=='FAIL' for r in records),'canonical_release_credit':0}}
assert len(records)==38 and set(assignment['question_hashes'])=={r['question_id'] for r in records}
assert out['input_provenance']['postassignment_export_matches_preassignment_visible_content']
dump(BASE/'report.json',out)
print(out['summary']);print('REPORT_SHA256',sha(BASE/'report.json'))
