"""AUTHOR's manually enumerated semantic propositions; no sentence/regex claim generation."""
import json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).parent
spec=[]
def add(uid,sid,section,lines,q=None,blocker=None):
 for line in lines.strip().split('\n'):
  assert line.strip();spec.append(dict(unit_id=uid,source_id=sid,authority_clauses=[section],statement_ko=line.strip(),related_question_ids=[q] if q else [],blocker=blocker))
USP='현재 full USP chapter를 확보하지 못했다. 공개FAQ/landing 또는 구형MA inspection template는 현재 조문 전문과 적용조건 대조를 대체하지 않는다. 이 technical proposition은 AUTHOR enumeration만 완료했고 source verification credit은 0이다.'
add('w4-b-22','usp797','USP <797> use of conventionally manufactured products; single-dose containers (exact current clause unavailable)', '''Single-dose container의 첫 puncture/entry에는 ISO Class 5 또는 더 깨끗한 환경이라는 조건이 붙는다.
위 환경에서 single-dose container의 첫 puncture/entry 후 사용 제한은 12시간이라는 본문 주장이다.
12시간보다 짧은 다른 applicable limit가 있으면 더 짧은 기간을 적용한다.
Puncture 후 사용기간 동안 제조사의 보관 조건도 유지해야 한다.
Closure를 제거한 ampoule의 잔량은 보관하여 재사용하는 경로로 사용하지 않는다.''',blocker=USP)
add('w4-b-22','usp797','USP <797> conventionally manufactured multiple-dose containers (current clause unavailable)', '''일반적인 28일 개봉 후 기간은 conventionally manufactured multidose parenteral container에 관한 주장이다.
위 28일의 기산점은 first puncture이다.
제조사가 별도 기간을 정하면 해당 제품 instructions를 확인하는 예외가 있다.
모든 상용 eye drops에 일률적으로 28일을 적용할 수 없다.
모든 개봉 약에 일률적으로 28일을 적용할 수 없다.''',blocker=USP)
add('w4-b-22','usp797','USP <797> compounded multiple-dose CSPs and single-patient topical/ophthalmic CSPs (current clause unavailable)', '''Compounded multidose CSP에는 Category 2 또는 3 조건이 적용된다는 주장이다.
Compounded multidose CSP에는 해당 preservative-effectiveness 조건이 적용된다.
Compounded multidose CSP에는 해당 container 조건이 적용된다.
Compounded multidose CSP에는 해당 labeling 조건이 적용된다.
Compounded multidose CSP의 개봉 후 사용기간과 assigned BUD 중 더 이른 applicable limit를 적용한다.
Single-patient nonpreserved topical/ophthalmic CSP에는 별도 labeling 경로가 있다는 주장이다.
위 특정 경로의 room-temperature 기간은 24시간이라는 주장이다.
위 특정 경로의 refrigerated 기간은 72시간이라는 주장이다.
위 single-patient topical/ophthalmic 경로를 모든 multidose injection으로 확대하지 않는다.
원료 vial의 puncture-time limit와 최종 CSP의 BUD는 별도 값이다.
원료를 puncture-time limit 안에 사용한 사실만으로 최종 CSP의 최대 BUD가 결정되지 않는다.''',blocker=USP)
add('w4-b-23','usp797','USP <797> release inspections / quality assurance (current full text unavailable)', '''CSP는 release 전에 label과 order의 일치 여부를 검사한다.
CSP는 release 전에 필요한 appearance 검사를 한다.
CSP는 release 전에 visible particles를 검사한다.
CSP는 release 전에 cloudiness를 검사한다.
CSP는 release 전에 discoloration을 검사한다.
CSP는 release 전에 container integrity를 검사한다.
조제 당일 교부하지 않고 보관한 CSP는 release 시 다시 확인한다.''',blocker=USP)
add('w4-b-23','defect','Policy 2024-04 pp1–2; MGL c112 §39D(e)', '''Defective preparation은 격리한다.
Defective preparation 발견은 원인조사로 연결한다.
이미 교부한 defective preparation은 해당 recall 의무와 연결한다.
Defective preparation에는 해당 reporting trigger를 별도로 적용한다.''')
add('w4-b-23','rapid','Policy 2025-01 p1 opening Board position; I(A)–(D), II(A)–(C), III(C)', '''Sterility testing이 필요한 CSP는 음성 결과를 받기 전에 dispense하지 않는 것이 Board의 현재 정책 입장이다.
구형 inspection form의 결과 전 release 후 recall 절차 문구는 현재 MA의 일반적인 선교부 허가를 뜻하지 않는다.
Rapid microbial method는 USP <71>와 동등하거나 더 우수한 noninferior alternative임을 validation해야 한다.
Rapid method의 적합성은 CSP formulation별로 확인한다.
Rapid method의 적합성은 실제 농도에 맞게 확인한다.
Method-suitability challenge는 낮은 수준의 bacteria 회수를 확인해야 한다.
Method-suitability challenge는 낮은 수준의 yeast/mold 회수를 확인해야 한다.
Formulation에 의한 false-negative 위험을 검토한다.
Vendor가 rapid test라고 부르는 사실만으로 모든 formula에 적합함이 입증되지 않는다.
Formulation 변경 시 method suitability를 다시 평가한다.
검사법의 검출범위 차이와 한계를 검토한다.
MOR 또는 designated PIC는 받은 suitability 결과를 검토하고 서명·날짜를 기록한다.''',q='MA-EXP-0913')
add('w4-b-24','usp797','USP <797> labeling (current full text unavailable)', '''CSP label에는 적절한 internal identification이 필요하다.
CSP label에는 ingredients 및 amounts 또는 concentration 정보가 필요하다.
CSP label에는 dosage form 정보가 필요하다.
CSP label에는 BUD가 필요하다.
CSP label에는 storage 정보가 필요하다.
CSP label에는 route 정보가 필요하다.
CSP label에는 quantity 또는 volume 정보가 필요하다.
CSP label에는 필요한 handling warnings가 필요하다.''',blocker=USP)
add('w4-b-24','c94cs21','MGL c94C §21 compounded-label and pharmacy-phone paragraphs', '''MA에서는 약국이 만든 compounded preparation임을 container label로 표시해야 한다.
Sterile 또는 complex-nonsterile compounding pharmacy의 연락 전화번호는 해당 법정 조건에서 container에 표시한다.''')
add('w4-b-24','fdaoverview','FDA Understanding the Risks of Compounded Drugs; compounded drugs are not FDA-approved', '''Sterile compounded 표시는 해당 약이 FDA-approved라는 의미가 아니다.''')
add('w4-b-24','c112s39d','MGL c112 §39D(a) accountability documentation; §39D(e) defective log', '''Complaint·adverse event·OOS 조사는 affected batch와 연결하여야 한다.
Affected preparation의 components를 추적할 수 있어야 한다.
Affected preparation의 조제 담당자를 추적할 수 있어야 한다.
Affected preparation의 처방·수령자와 연결되는 accountability가 필요하다.''')
add('w4-b-24','usp797','USP <797> quality assurance / complaint and OOS investigations (current full text unavailable)', '''Complaint·adverse event·OOS 조사는 environment와도 연결한다.
동일 원인으로 다른 lot가 영향받았는지 조사한다.
후속 재검사 한 건이 양호하다는 이유만으로 원래 failure를 삭제할 수 없다.''',blocker=USP)
add('w4-b-24','defect','Policy 2024-04 p2 defective log and destruction/return records; MGL c112 §39D(e)', '''Defective preparation log에는 최소 10년 보존기간이 적용된다.
Defective log의 10년 보존기간을 모든 정상 compounding record의 보존기간으로 일반화하지 않는다.
일반 처방 보존기간을 근거로 defective 자료의 10년 보존 의무를 줄이지 않는다.''')
add('w4-b-24','c94cs23','MGL c94C §23(a) general prescription records; compared with c112 §39D(e)', '''일반 처방의 2년 보존 구조는 defective log의 별도 보존기간과 구별한다.''')
add('w4-b-24','cmr15','247 CMR 15.01–15.04 CQI program and records; c112 §39D(a),(e)', '''Sterile·complex-nonsterile accountability documentation과 일반 처방기록은 구별되는 법정 기록이다.
CQI 기록과 defective log는 별도로 구별한다.''')
add('w4-b-3','503a-code24','21 USC353a(b)(1)(A)(i)–(iii); FDA current compounding statutory provisions', '''503A bulk substance에 적용 가능한 USP/NF monograph가 있으면 그 monograph 및 compounding chapter 조건을 충족하는 경로를 확인한다.
적용 monograph가 없으면 FDA-approved drug의 component인 bulk substance 경로를 확인한다.
Monograph도 없고 approved-drug component도 아니면 적격 503A bulks-list 경로를 확인한다.
503A bulk substance는 FDA-registered establishment에서 제조되어야 한다.
503A bulk substance에는 valid certificate of analysis가 동반되어야 한다.
분말의 외관만으로 503A bulk-substance 자격을 충족하지 않는다.
Supplier의 광고만으로 503A bulk-substance 자격을 충족하지 않는다.
COA의 존재가 다른 자격요건을 충족하지 못한 원료를 합법화하지 않는다.''',q='MA-EXP-0881')
add('w4-b-3','usp795','USP <795> component selection / receiving / COA (current full text unavailable)', '''COA는 원료 identity를 검토하는 자료이다.
COA는 원료 strength를 검토하는 자료이다.
COA는 원료 purity를 검토하는 자료이다.
COA는 시험 specifications를 검토하는 자료이다.
Research-use-only 원료를 해당 인체용 조제에 사용하지 않는다.
Not-for-human-use 원료를 인체용 조제에 사용하지 않는다.
Not-for-injection 원료를 주사용 조제에 사용하지 않는다.
원료의 입고 상태를 확인한다.
사용 전 원료의 상태를 다시 확인한다.
Supplier가 바뀌었다는 사정에서 기존 stability 자료를 자동 승계하지 않는다.
Salt 또는 formulation 변경 시 기존 stability·process validation을 자동 승계하지 않는다.''',blocker=USP)
add('w4-b-3','c112s39d','MGL c112 §39D(a) accountability documentation; scope expressly sterile/complex-nonsterile', '''원료 lot와 expiry는 actual preparation에 추적 가능하게 연결한다.
원료를 사용한 preparation은 실제 작업자에 추적 가능하게 연결한다.
원료를 사용한 preparation은 생성 처방에 추적 가능하게 연결한다.''')
add('w4-b-4','copies','Policy2020-02 entire p1; Policy2023-07 II(C); MGL c112 §39D(a)', '''MA는 commercial product의 편의상 copy compounding을 일반적으로 허용하지 않는다.
환자의 고유 medical need로 유의한 차이를 만드는 경로를 평가해야 한다.
Medical need의 판단과 문서화는 prescribing practitioner와 연결된다.
의료상 dye 제거는 유의한 차이의 예시가 될 수 있다.
환자의 medical need에 따른 strength 변경은 예시가 될 수 있다.
환자의 medical need에 따른 dosage form 변경은 예시가 될 수 있다.
환자의 medical need에 따른 delivery mechanism 변경은 예시가 될 수 있다.
가격이 싸다는 사유만으로 유의한 차이가 성립하지 않는다.''',q='MA-EXP-0885')
add('w4-b-4','copies-fda','FDA 503A essentially copies guidance Jan2018 II–III, commercial availability and shortage listing', '''National FDA drug shortage는 개별 약국의 재고 부족과 다르다.
Shortage를 이유로 한 copy 허용 또는 집행재량은 해당 약물별로 판단해야 한다.
Shortage를 이유로 한 판단에는 해당 시점을 확인해야 한다.
503A와 503B 등 실제 조제 경로에 맞는 shortage 조건을 확인해야 한다.
과거 shortage 사실만으로 현재 모든 copy compounding이 허용되지 않는다.''',q='MA-EXP-0885')
add('w4-b-5','503a-code24','21 USC353a(b)(3)(B)(i)–(ii)', '''503A interstate distribution 조건은 주와 FDA의 MOU에 연결되는 별도 법정 체계이다.
비MOU 주에 대한 statutory limit는 out-of-state compounded products가 총 prescription orders의 5%를 넘지 않는 구조이다.
503A 5%의 분모는 pharmacy/physician이 dispensed 또는 distributed한 total prescription orders이다.''')
add('w4-b-5','mou','FDA MOU page October2022 update; Status of standard MOU published in October2020', '''FDA 현재 게시 안내는 2020 standard MOU를 suspended로 취급한다.
FDA는 관련 final rule의 시행 및 updated standard MOU 게시까지 statutory 5% 집행 개시를 연기한다고 설명한다.
법 조문의 5% 숫자와 FDA의 현재 집행재량 상태는 별도로 읽는다.
현재 안내는 Massachusetts가 새 MOU를 체결했다는 증거가 아니다.''')
add('w4-b-5','dea5','21 CFR1307.11(a)(1)(iv),(b); compared with21USC353a(b)(3)(B)', '''DEA practitioner distribution 예외의 5%는 calendar-year controlled-substance dosage units를 기준으로 한다.
DEA 5% 분모는 같은 해의 controlled-substance distributed 및 dispensed dosage units이다.
503A 5%와 DEA 5%는 분모가 다르다.
503A와 DEA의 대상 거래가 다르다.
503A 5%는 FDA 체계이고 practitioner distribution 5%는 DEA 체계이다.
503A compounding exemption 조건과 DEA distributor registration 예외는 법적 효과가 다르다.''')
add('w4-b-6','policy795','Policy2023-07 I(B),V(A),VII(A)–(C); revised2025-02-06', '''USP <795>의 BUD 기준과 MA simple/moderate/complex 면허 분류는 동일한 표가 아니다.
USP 용어 개정만으로 MA complex-nonsterile specialty license 의무가 사라지지 않는다.
특수 training이 필요한 complex formulation은 MA complex 정의에 포함될 수 있다.
특수 시설·환경 또는 equipment가 필요한 formulation은 complex 정의에 포함될 수 있다.
Elevated risk를 갖는 특수 기법·절차를 사용하는 preparation은 complex 정의에 포함될 수 있다.
복잡한 계산을 사용하는 조제는 policy의 complex 예시이다.
Capsules는 policy의 complex dosage-form 예시이다.
Suppositories는 policy의 complex dosage-form 예시이다.
Troches는 policy의 complex dosage-form 예시이다.
Lollipops는 policy의 complex dosage-form 예시이다.
Transdermal dosage forms는 policy의 complex 예시이다.
Modified-release preparations는 policy의 complex 예시이다.
Systemic-delivery nasal products는 policy의 complex 예시이다.
실제 formulation과 policy의 비포괄적 예시 표현을 함께 적용한다.
Hazardous-drug compounding은 MA complex-nonsterile 경로에 해당할 수 있다.
HD tablet를 crush하여 mixture를 만드는 행위는 intact-tablet counting으로 취급할 수 없다.
HD capsule를 열어 mixture를 만드는 행위는 intact-product counting으로 취급할 수 없다.
해당 complex nonsterile 조제에는 추가 specialty license가 필요하다.
HD compounding에는 해당 containment와 별도 room 조건이 필요하다.
USP <800> risk assessment만으로 모든 HD compounding을 ordinary counter에서 허용하지 않는다.''',q='MA-EXP-0889')
add('w4-b-7','policy795','Policy2023-07 II(B)note,III(A)–(E),VI(C); revised2025-02-06', '''환자 또는 agent가 요청하는 Schedule VI flavoring에는 매번 prescriber의 선요청 없이 수행할 수 있는 policy 경로가 있다.
Flavoring 변경을 필요한 처방·조제 기록에 남겨야 한다.
Flavoring permission을 Schedule II–V 약으로 일반화하지 않는다.
Flavoring permission을 모든 formulation 변경으로 일반화하지 않는다.
Flavoring 추가 후 stability가 유지되는지 확인해야 한다.
Flavoring 추가 후 final concentration이 USP <795> 범위 밖으로 바뀌지 않는지 확인해야 한다.
변경된 준비방법은 제조사 지시 그대로의 단순 reconstitution 예외에 해당하지 않을 수 있다.
맛이 좋아진 사실 자체는 보존제 농도가 유지됨을 입증하지 않는다.
맛이 좋아진 사실 자체는 BUD가 유지됨을 입증하지 않는다.
맛이 좋아진 사실 자체는 균일성이 유지됨을 입증하지 않는다.
비위험 약물의 breaking/splitting은 policy상 compounding으로 보지 않는다.
HD의 splitting/manipulation은 별도 USP <800> 조건을 검토한다.''',q='MA-EXP-0893')
add('w4-b-7','usp795','USP <795> flavoring compatibility / therapeutic intent and specific modified-release product instructions', '''Flavoring이 therapeutic intent에 미치는 영향을 검토한다.
Flavoring compatibility를 검토한다.
Splitting 판단에서 modified-release 제형의 실제 제품지시를 검토한다.
Splitting이라는 이름만으로 실제 manipulation 및 제품지시 검토를 생략하지 않는다.''',blocker=USP)
add('w4-b-8','policy795','Policy2023-07 II(A)note;III–IV;VII(C)', '''Nonsterile designated person는 MOR가 맡을 수 있다.
Nonsterile designated person는 onsite licensed pharmacist가 맡을 수 있다.
조제 유형에 맞는 training과 SOP를 마련해야 한다.
시설·equipment와 QA를 실제 조제 공정에 연결한다.
Compounding area는 청결하게 유지해야 한다.
공간·equipment·materials는 교차오염을 최소화하도록 배치·사용한다.
Compounding area는 water source로부터 분리 또는 보호한다.
10 square feet counter space는 should라는 권고 표현이다.
Complex용 dedicated room의 일반 의무는 policy에 미래형으로 적혀 있다.
HD compounding용 별도 room/containment는 policy상 현재 요구이다.
Noncomplex cleaning/sanitizing enforcement discretion은 조건부이다.
재량을 적용해도 sink·utensils·equipment를 clean/sanitary하게 유지해야 한다.
Noncomplex storage-room temperature monitoring의 집행재량은 실제 USP storage temperatures 유지가 조건이다.
위 집행재량은 적절한 약물 보관 자체를 면제하지 않는다.
Balance는 proper maintenance를 유지해야 한다.
Scale/balance sealing은 최소 매 calendar year 한 번 해야 한다.
Retail pharmacy renovation은 시작 전 승인을 신청해야 한다.
Complex nonsterile에 관여·감독하는 pharmacist에게 calendar-year specialized CE 의무가 있다.''')
add('w4-b-8','usp800advisory','Advisory USP<800> in Community Pharmacies pp1,3 designated person and training', '''USP <800> HD designated person의 자격을 nonsterile onsite-pharmacist designated person와 혼동하지 않는다.
Training과 personnel competency assessment는 구별한다.
CE를 수료한 사실만으로 특정 조제 공정을 수행할 실제 능력이 자동 입증되지 않는다.''')
add('w4-b-8','usp795','USP <795> personnel hygiene and training requirements (current full text unavailable)', '''Nonsterile compounding에서 적절한 손위생을 관리해야 한다.
Board의 집행재량은 실제 환자안전 필요까지 면제하는 것으로 일반화할 수 없다.''',blocker=USP)
add('w4-b-9','policy795','Policy2023-07 III(A),VI(B)–(C)', '''MFR는 매 조제 시 따라야 하는 반복 가능한 formulation sheet이다.
MFR와 각 실제 조제를 기록하는 CR는 기능이 다르다.
Nonsterile preparation마다 CR를 유지해야 한다.
MFR만 보관한다고 각 실제 조제의 기록 의무가 끝나지 않는다.
적격 premeasured kit는 필요한 정보를 포함한 CR가 MFR를 겸하는 log-sheet 경로를 쓸 수 있다.
상용 비무균 제품에 flavoring을 추가하는 경우에도 필요한 정보를 담은 CR가 MFR를 겸할 수 있다.''',q='MA-EXP-0897')
add('w4-b-9','usp795','USP <795> master formulation and compounding record detailed contents (full current chapter unavailable)', '''MFR에는 준비할 components의 identity를 기록한다.
MFR에는 원료별 amount를 기록한다.
MFR에는 목표 strength와 dosage form을 기록한다.
MFR에는 필요한 calculations를 기록한다.
MFR에는 혼합·제조 순서를 기록한다.
MFR에는 container 정보를 기록한다.
MFR에는 storage conditions를 기록한다.
MFR에는 BUD의 근거를 기록한다.
MFR에는 기대되는 appearance를 기록한다.
MFR에는 quality control procedures를 기록한다.
CR에는 actual preparation date/time을 기록한다.
CR에는 내부 preparation number·처방 또는 lot를 연결한다.
CR에는 실제 components와 해당 lot/expiry를 기록한다.
CR에는 actual quantities와 calculations를 기록한다.
CR에는 작업·검수 담당자를 기록한다.
CR에는 실제 yield를 기록한다.
CR에는 assigned BUD를 기록한다.
CR에는 actual quality checks를 기록한다.
CR에는 조제 중 특이사항을 기록한다.''',blocker=USP)
add('w4-b-9','usp797','USP <797> master formulation and compounding records (full current chapter unavailable)', '''Sterile MFR의 trigger에는 여러 환자를 위해 준비하는 경우가 포함된다.
Sterile MFR의 trigger에는 nonsterile ingredients에서 준비하는 경우가 포함된다.
Sterile CR는 Category 1 CSP에도 필요하다.
Sterile CR는 Category 2 CSP에도 필요하다.
Sterile CR는 Category 3 CSP에도 필요하다.''',blocker=USP)
add('w4-b-9','c112s39d','MGL c112 §39D(a) accountability documentation', '''MA의 sterile·complex nonsterile accountability documentation은 USP의 MFR/CR 의무와 함께 별도로 검토해야 한다.''')
add('w4-c-1','niosh-pdf','NIOSH Publication2025-103 2024 List, Introduction and Defining Hazardous Drugs pp1–3; MAUSP800 Advisory p1', '''HD는 취급자의 occupational exposure 및 위해 가능성에 관한 분류이다.
HD 분류와 controlled-substance abuse/diversion schedule은 서로 다른 체계이다.
동일 약물이 HD와 controlled-substance 양 체계에 속할 수 있다.
Federally controlled가 아니라는 사실만으로 HD가 아니라고 할 수 없다.''',q='MA-EXP-0917')
add('w4-c-1','usp797','USP <795>/<797>/<800> scope and simultaneous aseptic/containment controls (full current text unavailable)', '''USP <795>/<797>는 preparation의 품질·오염방지를 다룬다.
USP <800>은 취급자뿐 아니라 환자와 환경의 HD 노출 방지를 다룬다.
Sterile HD 작업은 제품을 보호하는 aseptic environment를 충족해야 한다.
Sterile HD 작업은 외부 노출을 막는 containment도 동시에 충족해야 한다.''',blocker=USP)
add('w4-c-10','503b-code24','21 USC353b(b)(1)(A),(b)(2)(A); 2024 USCode edition', '''FDA outsourcing facility annual renewal window는 매년 10월 1일에 시작한다.
FDA outsourcing facility annual renewal window는 매년 12월 31일에 종료한다.
Outsourcing product report는 initial registration 시 제출한다.
Outsourcing product report는 매년 6월에도 제출한다.
Outsourcing product report는 매년 12월에도 제출한다.
Product report는 직전 6개월 동안 조제한 drugs를 대상으로 한다.
Facility renewal와 product reporting은 서로 다른 제출 의무이다.''',q='MA-EXP-0937')
add('w4-c-10','503b-code24','21 USC353b(a)(10)(A)(i)–(iii), (B)(i)–(iii)', '''503B drug label에는 compounded drug임을 나타내는 해당 statement가 필요하다.
503B drug label에는 outsourcing facility name이 필요하다.
503B drug label에는 outsourcing facility address가 필요하다.
503B drug label에는 outsourcing facility phone number가 필요하다.
503B drug label에는 lot 또는 batch number가 필요하다.
503B drug label에는 drug established name이 필요하다.
503B drug label에는 dosage form과 strength가 필요하다.
503B drug label에는 적절한 quantity 또는 volume이 필요하다.
503B drug label에는 compounding date가 필요하다.
503B drug label에는 expiration date가 필요하다.
503B drug label에는 storage 및 handling instructions가 필요하다.
503B drug label에는 NDC가 있는 경우 그 NDC를 표시한다.
503B labeling에는 active ingredients와 양 또는 비율의 목록이 필요하다.
503B labeling에는 inactive ingredients와 양 또는 비율의 목록이 필요하다.
503B label에는 Not for resale statement가 필요하다.
Identified individual patient prescription 없이 공급하면 Office Use Only statement도 필요하다.
Container에는 법정 adverse-event reporting information이 추가된다.
Container에는 해당 directions for use가 추가된다.
Ingredient 목록의 label 공간이 부족하면 statute가 정한 container 경로를 확인한다.''',q='MA-EXP-0937')
add('w4-c-10','503b-code24','21 USC353b(a)(10)(A)(iii)(VI); MGL c112 §39D(a) BUD definition comparison', '''503B statute의 expiration-date labeling과 pharmacy CSP의 BUD labeling은 출처 확인 없이 동일 용어로 통일하지 않는다.
어떤 제도 아래 조제된 제품인지 먼저 확인하여 해당 labeling 체계를 적용한다.''')
add('w4-c-11','ae','21 CFR310.305(c)(1)(i),(c)(2);503B linkage via353b(b)(5) and FDA2015 guidanceIII(A)–(B)', '''Outsourcing facility는 compounded prescription drug의 serious하고 unexpected한 adverse drug experience를 FDA에 보고해야 한다.
위 initial report는 가능한 한 신속히 제출한다.
위 initial report는 최초 정보를 받은 뒤 15 calendar days를 넘기지 않는다.
New information를 받으면 follow-up을 제출해야 한다.
Follow-up 기한은 new information 수령 후 15 calendar days 이내이다.
FDA가 요청한 follow-up은 그 요청에 따라 제출한다.
필요한 세부사항이 전부 모이지 않았다는 이유로 initial report를 무기한 미루지 않는다.''',q='MA-EXP-1001')
add('w4-c-11','ae','21 CFR310.305(b) serious/unexpected definitions; (g)(1) records;FDA2015guidanceIII(A),IV', '''Serious adverse drug experience에는 death가 포함된다.
Serious adverse drug experience에는 life-threatening experience가 포함된다.
Serious adverse drug experience에는 inpatient hospitalization 또는 그 연장이 포함된다.
Serious adverse drug experience에는 persistent/significant disability가 포함된다.
Serious adverse drug experience에는 congenital anomaly/birth defect가 포함된다.
적절한 의학적 판단상 중대한 결과를 막기 위한 개입이 필요한 중요한 medical event도 serious일 수 있다.
Unexpected는 현재 labeling에 없는 event를 뜻한다.
Labeling의 기존 event보다 더 심각한 event도 unexpected일 수 있다.
Labeling의 기존 event보다 더 구체적인 event도 unexpected일 수 있다.
Unexpected는 보고자 개인이 놀랐다는 뜻이 아니다.
해당 adverse-experience records는 10년 보존한다.''',q='MA-EXP-1001')
add('w4-c-11','sade-definitions','Policy2025-02 II(G), adopted2025-08-07; compared with21CFR310.305(b)', '''MA pharmacy SADE에는 Policy2025-02의 preventable-event 정의를 적용한다.
연방 serious/unexpected 정의와 MA preventable SADE 정의를 합치지 않는다.''')
add('w4-c-11','cmr20','247 CMR20.02(1)–(2),(5),20.07(3);Policy2024-04p2 defective-causedSADE', '''해당 MA reporting trigger에는 7business-day 기한이 별도로 적용될 수 있다.
Defective preparation이 SADE를 일으켰거나 의심되면 해당 immediate Board notification 경로가 있다.
함께 적용되는 MA의 더 빠른 보고기한을 연방 15일을 이유로 무시할 수 없다.''',q='MA-EXP-1001')
add('w4-c-12','cmr21','247 CMR21.02(1),(3)(b),(d)–(e);21.04(1)(c)–(f)', '''Resident outsourcing facility는 MA registration을 확보해야 한다.
Resident outsourcing facility는 applicable Massachusetts controlled-substance registration 조건을 충족해야 한다.
Resident outsourcing facility는 유효한 FDA503B registration 증거를 제출해야 한다.
Resident outsourcing facility 신청의 FDA inspection은 신청 직전 2년 이내여야 한다.
Nonresident outsourcing facility는 FDA503B registration 조건을 충족해야 한다.
Nonresident facility도 신청 직전 2년 이내 FDA inspection 증거를 제출해야 한다.
Home state에서 license/registration을 받는 nonresident facility는 해당 good-standing 증거를 제출해야 한다.
Nonresident facility도 MA approval 경로를 별도로 충족해야 한다.
FDA 공개 목록 등재만으로 MA supply authority가 확정되지 않는다.''',q='MA-EXP-0941')
add('w4-c-12','cmr21','247 CMR21.03(1)–(3),(5);21.05(1)', '''Provisional registration은 직전 2년 FDA inspection을 충족하지 못한 resident 신청인의 제한된 경로이다.
Provisional registration은 nonresident에게 허용되지 않는다.
Provisional facility는 해당 sterile preparations를 조제할 수 있다.
필요한 FDA inspection과 MA full registration 전에는 provisional facility가 distribute할 수 없다.
필요한 FDA inspection과 MA full registration 전에는 provisional facility가 dispense할 수 없다.
신청 중인 상태를 full registration으로 취급하지 않는다.
MA full registration은 발급 후 odd-numbered year의 12월 31일 만료 구조이다.
MA의 위 renewal 구조와 FDA의 annual registration은 별도이다.''',q='MA-EXP-0941')
add('w4-c-12','cmr21','247 CMR21.02(6),21.04(3),21.08(2)–(5),21.09,21.12(1)–(3)', '''Outsourcing registration은 임의 양도할 수 없다.
Ownership transfer에는 해당 notification/application 절차를 적용해야 한다.
Ownership/control 관련 변경에는 실제 변경유형별 절차를 확인한다.
Relocation은 Board 사전 approval을 받아야 한다.
Relocation application은 원칙적으로 희망 이전일의 최소 90일 전에 제출한다.
Board가 달리 승인한 경우의 90일 예외가 있다.
새 장소에서는 FDA inspection 전 sterile preparation을 distribute/dispense할 수 없다.
FDA inspection 발생은 Board에 14일 안에 서면 통지할 사항이다.
FDA Form483 수령은 Board에 14일 안에 서면 통지할 사항이다.
FDA warning letter 수령은 Board에 14일 안에 서면 통지할 사항이다.''')
add('w4-c-13','cmr13','247 CMR13.02 Qualified nuclear pharmacist;13.03;13.05(1)–(3),(16),(22);13.06(1)–(4)', '''Nuclear pharmacist는 MA pharmacist registration을 유지해야 한다.
Nuclear pharmacist는 별도 qualified nuclear pharmacist 자격을 충족해야 한다.
Board가 자격을 인정하는 official letter를 받아야 한다.
Nuclear pharmacy는 해당 facility permit을 받아야 한다.
Nuclear pharmacy에는 applicable radiation authority requirements가 추가된다.
일반 compounding training만으로 radiopharmaceutical acquisition/preparation/dispensing 권한이 성립하지 않는다.
Formal didactic training은 200contact hours가 요구된다.
위 training 중 laboratory hours는 최대 60시간이다.
실무 경로는 최소 3개월 full-time experience 또는 500시간 actual practical experience로 설명된다.
실무는 qualified nuclear pharmacist supervision 또는 해당 Board-approved program 조건과 연결된다.
Education/training/experience에 관한 상세 affidavit를 Board에 제출해야 한다.
Qualified nuclear pharmacist가 현장에 있어 감독하는 조건을 유지해야 한다.
Nuclear pharmacy는 적절한 security 및 접근제한을 유지해야 한다.
Nuclear pharmacy는 radiation shielding을 위한 필요한 equipment를 유지해야 한다.
Nuclear pharmacy는 radiation monitoring equipment를 유지해야 한다.''',q='MA-EXP-0973')
add('w4-c-13','cmr13','247 CMR13.05(1),13.03(4),13.05(12)(e) and applicable radiation licensing (specific radiation license not obtained)', '''Facility의 radioactive-material license를 유지해야 한다.
Nuclear pharmacy의 radiation-specific SOP를 유지해야 한다.''',blocker='247CMR13은 applicable radiation laws 준수를 요구하나 실제 radiation authority license/SOP 조건 전문은 확보하지 않았다. 이 명제의 구체적 license 경로를 법규확정하지 않는다.')
add('w4-c-13','cmr13','247 CMR13.05(12)(e) activity at time of calibration', '''Radiopharmaceutical quantity의 해석에는 radionuclide activity가 필요하다.
Activity는 calibration time과 함께 보아야 한다.''',q='MA-EXP-0973')
add('w4-c-14','cmr13','247 CMR13.05(12)(a)–(h)', '''Radiopharmaceutical outer container에는 radiation symbol이 필요하다.
Outer container에는 Caution–Radioactive Material 경고가 필요하다.
Outer container에는 radionuclide name이 필요하다.
Outer container에는 chemical form 또는 common name이 필요하다.
Outer container에는 radioactive activity at calibration이 필요하다.
Outer container에는 expiration date 또는 time이 필요하다.''')
add('w4-c-14','cmr13','247 CMR13.05(12); other radiation label rules not separately obtained', '''Outer shield에는 calibration date/time 자체도 표시해야 한다는 본문 주장이다.
Inner container와 outer shield의 구체적인 labeling 역할을 구별한다.
Radiation-specific patient-use instructions를 유지한다.''',blocker='247CMR13.05(12)는 activity at calibration을 열거하나 본문의 calibration date/time 자체·inner-container label·patient-use instructions의 추가 방사선 규정 전체를 확보하지 않았다.')
add('w4-c-14','cmr13','247 CMR13.05(5),(6)(d),(9)', '''처방 접수 시 환자 이름이 미상인 한정된 nuclear 경로가 존재한다.
그 경로에서는 dispensing 후 72시간 안에 환자 이름을 확보해야 한다.
Nuclear 경로의 환자 이름 유예를 일반 pharmacy 처방의 유예로 확대하지 않는다.
Nuclear acquisition/disposition records는 최소 3년 보존한다.
Unused radiopharmaceutical을 반환받으면 해당 disposal 경로로 처리하고 기록한다.
반환된 radiopharmaceutical의 폐기 허용은 일반 stock 재판매 허가와 동일하지 않다.
Radioactive material의 return/disposal은 applicable radiation authority rules를 따른다.''',q='MA-EXP-0973')
add('w4-c-14','c94cs23','MGL c94C §23(a) compared with247CMR13.05(5)', '''일반 pharmacy 처방기록의 2년 구조와 nuclear acquisition/disposition의 3년을 구별한다.''')
add('w4-c-14','usp797','USP <825> radiopharmaceutical preparation-specific details / radiation license conditions', '''USP <825>와 방사선 규정의 preparation-specific 상세조건은 별도 검토 대상이다.''',blocker='USP<825> 전문과 시설별 radiation license conditions를 확보하지 않았다. 상세범위 미검증을 본문이 명시한 claim이며 검증credit0.')
add('w4-c-15','cmr7','247 CMR7.02(1),(4);7.04(9)(c)', '''MA 소재 wholesale drug business는 실제 사업 전에 Board license를 받아야 한다.
여러 location에서 wholesale 사업을 하면 location별 license가 필요하다.
State wholesaler license와 Massachusetts controlled-substance registration은 별도이다.
주 registration과 federal DEA registration은 별도이다.
State wholesale license와 DSCSA authorized-trading-partner status는 별도 확인층이다.''')
add('w4-c-15','cmr7','247 CMR7.03(3),7.04(1)–(7)', '''Wholesaler는 적절한 temperature를 관리해야 한다.
Wholesaler는 적절한 humidity를 관리해야 한다.
Wholesaler는 security를 관리해야 한다.
Wholesaler는 quarantine area 및 격리 절차를 유지해야 한다.
입고 shipping container를 검사해야 한다.
출고 product shipment를 검사해야 한다.
Defective/damaged products를 해당 절차로 관리해야 한다.
Expired products를 해당 절차로 관리해야 한다.
Returned products의 적합성과 disposition을 관리해야 한다.
Wholesaler는 recall 절차를 유지해야 한다.
Wholesaler는 disaster/crisis 절차를 유지해야 한다.
Wholesale repackaging/relabeling에는 registered pharmacist의 direct supervision이 필요하다.
위 repackaging/relabeling에는 applicable cGMP 준수가 필요하다.''')
add('w4-c-15','cmr7','247 CMR7.04(6)(a)1–3,(b)–(c)', '''일반 wholesale transaction records에는 source/destination을 기록한다.
일반 wholesale transaction records에는 drug identity를 기록한다.
일반 wholesale transaction records에는 quantity를 기록한다.
일반 wholesale transaction records에는 receipt date를 기록한다.
일반 wholesale transaction records에는 disposition date를 기록한다.
위 state records는 disposition 후 2년 보존한다.
Offsite이며 즉시 electronic retrieval 불가능한 records는 요청 후 2working days 내 inspection에 제공한다.''')
add('w4-c-15','dscsa582-code24','21 USC360eee-1(d)(1)(A)(iii),(d)(1)(B),(d)(3);FDApharmacist guidance', '''적용되는 DSCSA tracing records에는 별도 6년 보존 조건이 있다.
다른 pharmacy에 보내는 거래가 모두 patient dispensing인 것은 아니다.
모든 pharmacy-to-pharmacy transfer가 wholesale/tracing 예외인 것은 아니다.
Specific identified patient need 경로는 실제 조건을 확인하여 적용한다.
공통 ownership/control 경로는 실제 조건을 확인하여 적용한다.
Emergency transfer 경로는 실제 조건을 확인하여 적용한다.
Controlled-substance distribution에는 별도 DEA 경로를 확인한다.
Pharmacy license만으로 모든 wholesale activity가 포괄되는 것은 아니다.''')
add('w4-c-16','dscsa581-code24','21 USC360eee(2),(13),(14),(24);360eee-1(d)(1),(3),(4)', '''DSCSA는 covered prescription-drug supply chain에 적용되는 체계이다.
DSCSA에는 authorized trading partner 조건이 있다.
DSCSA에는 product tracing information 의무가 있다.
DSCSA에는 verification 의무가 있다.
DSCSA에는 suspect/illegitimate product 대응 의무가 있다.
Patient dispensing과 supply-chain ownership transaction은 구별한다.
법상 product exclusions가 별도로 존재한다.
법상 transaction exceptions가 별도로 존재한다.''')
add('w4-c-16','exemption2024','FDA small-dispenser exemption letter2024-07-12 pp1–3', '''2024년에 부여한 small-dispenser exemption의 기간은 2026년 11월 27일까지이다.''')
add('w4-c-16','exemption2027','FDA exemption letter2026-08-06 pp1–3 and footnotes14–17', '''새 extension 결정의 발행일은 2026년 8월 6일이다.
새 extension 면제기간은 2026년 11월 27일 시작한다.
새 extension 면제기간은 2027년 11월 27일까지이다.
본문 기준일 2026년 10월 20일에는 새 기간이 아직 시작되지 않았다.
본문 기준일에는 extension 결정이 이미 공표되어 있다.
새 extension의 employee-size assessment 시점은 2026년 11월 27일이다.
새 extension의 size는 회사 전체 corporate entity 단위로 센다.
합산하는 인원은 full-time licensed pharmacists와 qualified pharmacy technicians이다.
위 합산 인원이 25명 이하여야 한다.
개별 점포의 인원만으로 size를 판단하지 않는다.
모든 종류의 직원을 무차별 합산하는 기준이 아니다.
Full-time은 평균 주30시간 이상의 IRS 기준을 참조한다.
Full-time은 월130시간 이상의 IRS 기준도 참조한다.
이전 면제의 size-assessment date와 새 연장의 date를 혼합하지 않는다.
면제는 해당 small dispenser 및 명시된 적격 trading-partner transaction에 한정된다.
면제는 letter가 열거한 특정 enhanced requirements에 한정된다.
이 범주의 면제를 이용할 때 별도 individual application이 요구되지 않는다.
이 범주의 면제를 이용할 때 FDA에 별도 notification 정보를 제출할 필요가 없다.
모든 큰 wholesaler/manufacturer의 모든 거래를 2027년까지 면제하는 결정이 아니다.''',q='MA-EXP-0953')
add('w4-c-17','dscsapharm','FDA Pharmacists Utilize DSCSA Requirements, Confirm Entities / ReceiveStoreProvide / Investigate sections;360eee-1(d)(1),(3),(4)', '''면제 중에도 authorized trading partner와 거래해야 한다.
면제 중에도 suspect product를 조사해야 한다.
면제 중에도 suspect product를 격리해야 한다.
면제 중에도 illegitimate product를 해당 기관·거래상대에게 통지해야 한다.
기본 product tracing documentation 의무가 모두 사라지는 것은 아니다.
해당 tracing records의 6년 보존 의무를 무시할 수 없다.
실제로 적법한 공급망의 제품인지 확인할 의무가 사라지는 것이 아니다.''',q='MA-EXP-0953')
add('w4-c-17','exemption2027','FDA2026-08-06 letter pp2–3 listed exemptions, footnote17 and implementation admonition', '''Enhanced electronic package-level exchange 면제는 모든 transaction documents 면제를 뜻하지 않는다.
Letter가 제외한 의무의 정확한 범위를 확인해야 한다.
Actual transaction role에 해당하는 면제인지 확인해야 한다.
면제 중에도 enhanced requirements 이행 준비를 계속해야 한다.
Transaction-history 제공·수령 의무는 §582(k)(1) 구조에 따라 2023년 11월 27일부터 종료된다.
현재 TI/TS 의무와 과거 TH 의무를 구별한다.
현재 모든 거래에서 TI·TH·TS가 영구히 동일하게 필수라고 일반화하지 않는다.
TH 제공·수령 종료는 보존해야 하는 과거 기록의 임의 삭제 허가가 아니다.''',q='MA-EXP-0953')
add('w4-c-18','dscsa581-code24','21 USC360eee(2)(A)–(D),(9),(14),(20);FDApharmacists Confirm Entities section', '''Dispenser는 supplier의 적절한 state license를 확인해야 한다.
Dispenser는 supplier에게 적용되는 registration을 확인해야 한다.
Manufacturer/repackager의 authorized status는 해당 federal registration 경로로 확인한다.
Wholesaler의 authorized status는 해당 licensing/reporting 경로로 확인한다.
3PL의 자격확인 경로는 manufacturer/repackager와 구별한다.
Dispenser의 자격확인에는 해당 state licensing이 연결된다.
저가 광고는 authorized status의 대체 증거가 아니다.
배송 속도는 authorized status의 대체 증거가 아니다.
Product identifier의 standardized numerical identifier는 NDC와 serial number 요소를 갖는다.
Product identifier에는 lot number가 포함된다.
Product identifier에는 expiration date가 포함된다.
단순 제품명은 product identifier의 추적 요소를 대체하지 않는다.
일반 invoice만으로 product identifier의 추적 요소가 모두 갖추어지지는 않는다.''')
add('w4-c-18','exemption2027','FDA2026-08-06 letter pp2–3 section582(d)(4) and(g)(1)(A)–(F) exemptions', '''Package-level verification 의무의 적용 경로를 확인해야 한다.
현재 exemption은 명시된 요건과 거래범위 안에서만 적용한다.''')
add('w4-c-18','dscsa582-code24','21 USC360eee-1(d)(1)(A)(iii)–(v), product-tracing record maintenance and third-party arrangement', '''Vendor가 tracing data를 보관해도 pharmacy는 요구된 자료를 제공할 수 있어야 한다.''')
# Final direct reread found separate dose / accuracy / supplier-validation consequences.
add('w4-b-7','policy795','Policy2023-07 III(C) final-concentration limit', '''Flavoring 변경이 실제 투여 dose에 미치는 영향을 검토한다.''')
add('w4-b-8','usp795','USP <795> balances / measurement accuracy (full current text unavailable)', '''Compounding balance는 해당 조제에 적절한 정확성을 유지해야 한다.''',blocker=USP)
add('w4-b-3','usp795','USP <795> component change and process validation (full current text unavailable)', '''Supplier가 바뀌면 기존 process validation을 자동 승계하지 않는다.''',blocker=USP)
# Do not soften original source-scope claims while enumerating them.
for c in spec:
 if c['unit_id']=='w4-c-12' and c['statement_ko'].startswith('Ownership/control 관련'):
  c['statement_ko']='Ownership/control 변경에는 해당 사전 절차를 적용한다는 본문 주장이다.'
  c['blocker']='21.08 ownership transfer는 사전60일 통지와 transfer후60일 신청을 구별하고21.09는 officer/>5%ownership변경의14일 통지이다. 모든control변경을 일괄사전절차로 읽을 수 있는 본문범위는 미해결HOLD.'
 if c['unit_id']=='w4-b-3' and c['source_id']=='c112s39d':
  c['blocker']='c112§39D(a) accountability는 sterile/complex-nonsterile scope이다. 본문 일반nonsterile 원료 추적 전체범위를 이 조항만으로 확인하지 못했고 currentUSP795전문도 미확보이다.'
 if c['unit_id']=='w4-b-23' and c['statement_ko']=='Defective preparation 발견은 원인조사로 연결한다.':
  c['blocker']='Policy2024-04는 recall/segregation/reporting을 확인하지만 모든defect의 investigation 절차 전체는 currentUSP797이 미확보이다.'
 if c['unit_id']=='w4-b-24' and c['statement_ko']=='Complaint·adverse event·OOS 조사는 affected batch와 연결하여야 한다.':
  c['blocker']='c112§39D(a) accountability와 defect log 연결은 확인했으나 complaint/AE/OOS 전유형의 조사절차는 currentUSP797전문 없이 확정하지 않는다.'
 if c['unit_id']=='w4-b-24' and c['statement_ko'].startswith('Sterile 또는 complex-nonsterile compounding pharmacy의 연락'):
  c['statement_ko']='CSP label에는 pharmacy contact가 포함된다는 본문 주장이다.'
  c['blocker']='MAc94C§21전화표시는sterile/complex범위및동일병원inpatient예외가있다.모든CSP의contact표시범위를현재USP797전문없이일괄확인하지않는다.'
 if c['unit_id']=='w4-c-14' and c['statement_ko']=='처방 접수 시 환자 이름이 미상인 한정된 nuclear 경로가 존재한다.':
  c['statement_ko']='Dispensing 때 환자 이름을 확보할 수 없는 한정된 nuclear 경로가 존재한다는 본문 주장이다.'
  c['blocker']='13.05(6)(d)실제trigger는처방접수시nameunknown이다.본문dispensing때라는요약이trigger차이를충분히명확히하는지HOLD.72시간기산점과name/address조건은별도로구별해야한다.'
 if c['source_id']=='c94cs23':c['authority_clauses']=[c['authority_clauses'][0].replace('§23(a)','§23(e)')]
 if c['unit_id']=='w4-c-18' and c['statement_ko'].startswith('Vendor가'):
  c['authority_clauses']=['21 USC360eee-1(g)(2)(A), information-maintenance agreement; dispenser not relieved of obligations']
 if c['unit_id']=='w4-c-15' and c['statement_ko'].startswith(('공통 ownership','Emergency transfer')):
  c['source_id']='dscsa581-code24';c['authority_clauses']=['21 USC360eee(24)(B)(i) common control / (iii) emergency medical reasons transaction exceptions; actual wholesale scope separately applicable']
 if c['unit_id']=='w4-c-15' and c['statement_ko'].startswith('Controlled-substance'):
  c['source_id']='dea5';c['authority_clauses']=['21 CFR1307.11(a)–(b) practitioner distribution registration exception']
 if c['unit_id']=='w4-c-15' and c['statement_ko'].startswith('Pharmacy license만'):
  c['source_id']='cmr7';c['authority_clauses']=['247CMR7.02(1),7.04(9)(c) wholesale licensure and registrations; actual activity controls']
# Source-class/version metadata refer to actual retrieved editions, never failed endpoints.
sources=json.loads((OUT/'sources-manifest.json').read_text())
versions={
 'cmr21':'MA Register1305 dated2016-01-29; official currently posted247CMR21; clause effective dates not separately established',
 'cmr13':'Current official posted247CMR13; PDF contains repeated13.05 layouts, relied on consistently matching stated clauses; individual effective dates not established',
 'cmr7':'Current official posted247CMR7; individual effective/amendment dates not established',
 'cmr20':'MA Register1536 dated2024-12-06; individual clause effective dates not separately established',
 'cmr15':'MA Register1536 dated2024-12-06; individual clause effective dates not separately established',
 'policy795':'Policy2023-07 adopted2023-05-04; latest printed revision2025-02-06; individual effective date not separately established',
 'rapid':'Policy2025-01 adopted2025-05-01; Board position cites draft247CMR17, not represented as final regulation',
 'copies':'Policy2020-02 adopted2020-02-06; latest printed revision2021-10-15',
 'copies-fda':'FDA guidance January2018; guidance scope and statutory conditions distinguished',
 'usp800advisory':'Advisory adopted2019-12-05; revised2022-02-03; does not replace fullUSP800',
 'niosh-pdf':'NIOSH2024List, DHHS(NIOSH)Publication2025-103, December2024; occupational-hazard scope, not DEA authority',
 'defect':'Policy2024-04 adopted2024-09-05',
 'environment':'Policy2026-03 adopted2026-09-03; supersedes2023-09; retrieved only as supplementaryQA context',
 'sade-definitions':'Policy2025-02 Definitions adopted2025-08-07',
 'ae-guidance':'FDA adverse-event outsourcing guidance October2015; cites310.305; report electronic-rule effective2015-06-10/compliance2015-09-08',
 'mou':'FDA currently posted MOU page, content current2022-10-20; suspension and announced enforcement delay are agency position, not statutory repeal',
 'exemption2027':'FDA letter issued2026-08-06; exemption interval2026-11-27 through2027-11-27',
 'exemption2024':'FDA letter issued2024-07-12; existing small-dispenser exemption through2026-11-27',
 'dscsapharm':'FDA pharmacist DSCSA page content-current2024-06-12; read together with2026extensionletter and statutory sunset',
 'exemptionindex':'FDA current official index; actual dates/conditions taken from signed2024/2026 letters',
 'dscsanotify':'FDA current official NotifyFDA ofIllegitimateProducts page; exact transaction role still required',
 'fdaoverview':'FDA currently posted UnderstandingRisksofCompoundedDrugs; compounded products not FDA-approved',
 'fda503a':'FDA currently posted FD&CActProvisionsThatApplytoHumanDrugCompounding; official comparative summary, exact statute separately read',
}
for sid,s in sources.items():
 if sid.endswith('-code24'):s['effective_date_note']='2024 USCode edition freshly retrieved2026-11-03; statutory amendment history/current2025edition not established. CurrentFDA postings corroborate only stated overlapping scope.'
 elif sid in {'ae','dea5'}:s['effective_date_note']='eCFR currentTitle21 display up to date2026-10-30; individual amendment effective dates not separately established'
 elif sid in versions:s['effective_date_note']=versions[sid]
 if sid=='exemption2027':s['effective_date']='2026-11-27'
 if s['retrieval_status']!='RETRIEVED':s['verification_credit']=0
 s['source_version']=s['effective_date_note']
 s['use_limitation']='AUTHOR content comparison against identified official version only; does not certify independent legal correctness, universal applicability, or amendment completeness.'
 s['redistribution_basis']='US government/state official source; USP landing/FAQ not redistributed, onlyURL/rawSHA/self-authoredmemo retained' if sid.startswith('usp') else 'Official public governmental publication; no commercial or protected exam text used'
# The large legacy inspection table is context only, with no claims credited to it.
s=sources['inspection'];memo='AUTHOR factual memo: legacy Massachusetts sterile-compounding inspection template was freshly fetched; original bytes SHA is retained in metadata. This form contains draft references and cannot establish currentUSP compliance or authorize early release against Policy2025-01. No source-check credit derives from this template. Original table/PDF not redistributed in this evidence set.\n'
for f in ('original_file','source_evidence'):

 if f in s:(ROOT/s[f]).unlink(missing_ok=True)
s.pop('original_file',None);(OUT/'inspection-memo.txt').write_text(memo);s['source_evidence']=str(OUT/'inspection-memo.txt');s['source_evidence_sha256']=hashlib.sha256(memo.encode()).hexdigest();s['retrieval_status']='LEGACY_CONTEXT_MEMO_ONLY';s['verification_credit']=0
# Store repository-relative evidence bindings for integration into any worktree.
for sid,s in sources.items():
 s['retrieval_method']='Fresh official HTTPS urllib; PDF pdftotext-layout or PythonHTMLParser text; original bytes SHA retained'
 for key in ('source_evidence','original_file'):
  if key in s and Path(s[key]).is_absolute():s[key]=str(Path(s[key]).relative_to(ROOT))
 if sid.startswith('usp') and sid!='usp800advisory':
  s['redistribution_basis']='USP official standards organization; copyrighted source not redistributed; URL/rawSHA and self-authored factual memo only'
  s['source_version']='USPFAQ updated2023-12-11; not full currentUSP797' if sid=='usp797faq' else 'Current fullUSPchapter not acquired; landing request HTTP403'
  s['effective_date_note']='Not established for full current chapter; technicalscopeSOURCE_BLOCKED'
 if s['retrieval_status']=='SOURCE_BLOCKED' and not sid.startswith('usp'):
  s['source_version']='Requested official target unavailable; no source content verified; raw error/empty response preserved'
  s['effective_date_note']='Not established; HTTP/error/empty content not legal evidence'
# Exact semantic decisions read in public practice, narrowed below. No blanket tag-based links.
links={
 'w4-b-3': {'MA-EXP-0881':[1,2,3,4,5,6,7,8], 'MA-EXP-0882':[13,14,15]},
 'w4-b-4': {'MA-EXP-0885':[1,2,3,4,5,6,7,8], 'MA-EXP-0886':[9,10,11,12,13]},
 'w4-b-6': {'MA-EXP-0889':[1,2,18], 'MA-EXP-0890':[15,16,17,19,20]},
 'w4-b-7': {'MA-EXP-0893':[1,2,3,4,5,6,17], 'MA-EXP-0894':[7]},
 'w4-b-9': {'MA-EXP-0897':[1,2], 'MA-EXP-0898':[3,4,17,18,19,20,21,22,23,24,25]},
 'w4-b-23': {'MA-EXP-0913':[12,13]},
 'w4-c-1': {'MA-EXP-0917':[1,2,3,4]},
 'w4-c-10': {'MA-EXP-0937':[1,2,3,4,5,6,7], 'MA-EXP-0938':[22,23]},
 'w4-c-11': {'MA-EXP-1001':[1,2,3,7], 'MA-EXP-1002':[4,5,6]},
 'w4-c-12': {'MA-EXP-0941':[10,11,12,13,14,15], 'MA-EXP-0942':[5,6,7,8,9]},
 'w4-c-13': {'MA-EXP-0973':[1,2,3,4,5,6]},
 'w4-c-14': {'MA-EXP-0974':[10,11,12]},
 'w4-c-16': {'MA-EXP-0953':[25,26,27,28]},
 'w4-c-17': {'MA-EXP-0954':[1,2,3,4,5,7,8,9,10]},
}
# q0918 was actually read, but no atomic proposition in w4-c-1 explicitly states API containment.
from collections import Counter
index=Counter();claims=[];provenance='AUTHOR_NOTE_WAVE13_CODEX_WORKER_20261103_NOT_INDEPENDENT'
assignment_path=ROOT/'reports/full-corpus-review/note-wave13-assignment.json'
a=json.loads(assignment_path.read_text());bodydata=json.loads((OUT/'actual-current-J-bodies.json').read_text());ub={x['unit']['id']:x['unit'] for x in bodydata['units']}
for original in spec:
 c=dict(original);uid=c['unit_id'];index[uid]+=1;n=index[uid];sid=c['source_id'];s=sources[sid]
 c.update(claim_id='NOTE-WAVE13-'+uid.upper()+'-'+str(n).zfill(3),unit_content_sha256=hashlib.sha256(ub[uid]['body'].encode()).hexdigest(),record_granularity='AUTHOR_ENUMERATED_ATOMIC_PROPOSITION',legal_claim_kind='MATERIAL_NOTE_PROPOSITION',is_complete_atomic_enumeration_evidence=True,review_status='SOURCE_BLOCKED' if c['blocker'] else 'AUTHOR_SOURCE_CHECKED',checked_at='2026-11-03',reviewer_provenance=provenance,actor_role='AUTHOR',independent=False)
 c['related_question_ids']=[qid for qid,ns in links.get(uid,{}).items() if n in ns]
 c['related_question_link_basis']='AUTHOR_READ_EXACT_STEM_EVERY_CHOICE_ACTUAL_DECISION_NOT_TAG_INHERITANCE' if c['related_question_ids'] else 'GAP_NO_DIRECT_MATCH_RECORDED'
 c['question_detail_coverage']='실제읽은 publicpractice의 특정판단 관련성만이다. 모든수치/조건을출제하거나 법적정답/독립감사가완료된뜻이 아니다.' if c['related_question_ids'] else '이atomic명제와 직접맞는practice의 실제판단 연결을 확보하지 못했다. 상속tag로채우지 않는다.'
 for k in ['official_url','source_evidence','source_evidence_sha256','effective_date','effective_date_note','source_version']:c[k]=s.get(k)
 c['authority_effective_date_status']='IDENTIFIED_VERSION_AND_REVIEW_DATE;INDIVIDUAL_EFFECTIVE_DATE_UNCONFIRMED_UNLESS_EXPLICIT'
 c['additional_authorities']=[]
 extra=[]
 if sid=='503a-code24':extra=[('fda503a','CurrentFDA comparative page,503A bulk eligibility and interstate conditions')]
 if sid=='ae':extra=[('503b-code24','21USC353b(b)(5)'),('ae-guidance','FDA2015guidanceIII(A)–(B),IV')]
 if c['unit_id']=='w4-c-11' and sid=='cmr20':extra.append(('defect','Policy2024-04p2 immediateSADEreport'))
 if c['unit_id']=='w4-c-1' and sid=='niosh-pdf':extra.append(('usp800advisory','MAUSP800Advisorypp1–2,HDexampleclonazepam; occupationalhazard not DEA schedule'))
 if c['unit_id']=='w4-c-16' and '이전 면제의' in c['statement_ko']:extra.append(('exemption2024','FDA2024-07-12letter sizeassessment footnote'))
 if c['unit_id']=='w4-c-15' and sid=='dscsa582-code24':extra.append(('dscsapharm','ReceiveStoreProvide and Investigate sections'))
 for extra_sid,section in extra:
  es=sources[extra_sid]
  c['additional_authorities'].append(dict(source_id=extra_sid,exact_section_context=section,official_url=es['official_url'],source_evidence=es['source_evidence'],source_evidence_sha256=es['source_evidence_sha256'],checked_at=es['checked_at'],effective_date_note=es['effective_date_note']))
 claims.append(c)
# Final direct semantic adjustment to ensure numerical extension dates are not treated as covered by generic exemption item.
for c in claims:
 if c['unit_id']=='w4-c-16' and c['statement_ko'].startswith(('이 범주의 면제를 이용할 때 별도','이 범주의 면제를 이용할 때 FDA')):c['related_question_ids']=[];c['related_question_link_basis']='GAP_NO_DIRECT_MATCH_RECORDED'
# Public original question snapshots and hashes are evidence for relationship only.
config=json.loads((ROOT/'site/practice-expansion/publication.json').read_text());qs=[]
for path in ['practice_expansion/2026-10-23/candidates/questions.json']+[b['path'] for b in config['additional_banks']]:
 j=json.loads((ROOT/path).read_text());qs.extend(j['questions'] if isinstance(j,dict) else j)
byid={q['question_id']:q for q in qs}; assert len(byid)==2346
qids=sorted({q for c in claims for q in c['related_question_ids']});records=[]
def h(v):return hashlib.sha256(v).hexdigest()
def rh(v):return h(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
for qid in qids:
 q=byid[qid];cs=[c for c in claims if qid in c['related_question_ids']]
 records.append(dict(question_id=qid,question_record_sha256=rh(q),stem_sha256=h(q['stem'].encode()),choice_text_sha256={c['id']:h(c['text'].encode()) for c in q['choices']},topic=q.get('topic'),reviewed_fields=['original_stem','every_original_choice','actual_case_A_or_B_decision'],actual_lead_in=q['stem'].split('\n')[-1],claim_ids=[c['claim_id'] for c in cs],relevance_finding_ko='실제stem·모든보기·선택한Case판단과 위claim들의 직접관련성을 수동연결했다. 날짜/세부자격은 question이 직접묻지않으면 gap으로남겼다.',link_relevance_status='AUTHOR_REVIEWED_SPECIFIC_DECISION_MATCH',question_answer_or_independent_audit_credit=0))
qpath=OUT/'question-link-review.json';qpath.write_text(json.dumps(dict(reviewed_at='2026-11-03',actor_role='AUTHOR',public_practice_inventory=2346,canonical_439_mapping_reviewed=False,method_ko='23개public original question의stem/모든선택지/CaseA 또는B 실제판단을직접읽었다. 추가로읽은0918은 해당원자명제의directmatch없어검증link를부여하지않았다. 보조읽기를question authorreview또는독립credit로집계하지않는다.',records=records,read_but_not_linked_question_ids=['MA-EXP-0918'],question_answer_review_credit=0,independent_credit=0),ensure_ascii=False,indent=2)+'\n')
(OUT/'linked-public-original-question-snapshots.json').write_text(json.dumps({q:byid[q] for q in sorted(set(qids)|{'MA-EXP-0918'})},ensure_ascii=False,indent=2)+'\n')
findings=[
 dict(finding_id='W13-USP-FULL-TEXT',status='HOLD',unit_ids=sorted({c['unit_id'] for c in claims if c['blocker'] and 'USP' in c['blocker']}),finding_ko='CurrentUSP795/797/800/825전문미확보. 403landing·공개FAQ·구형inspectiontable로technicalclaim을verified승격하지않는다.'),
 dict(finding_id='W13-API-TRACE-SCOPE',status='HOLD',unit_ids=['w4-b-3'],finding_ko='c112§39D의accountability는sterile/complex-nonsterile범위. 일반nonsterile원료추적본문전체는currentUSP795추가대조필요.'),
 dict(finding_id='W13-OWNERSHIP-CONTROL',status='HOLD',unit_ids=['w4-c-12'],finding_ko='사전절차라는본문은21.08 transfer사전60일통지/transfer후60일신청과21.09 officer/>5%interest변경후14일통지를구분하지않고읽힐수있다. 본문을완화하여열거하지않고해당claimSOURCE_BLOCKED.'),
 dict(finding_id='W13-NUCLEAR-LABEL-RADIATION',status='HOLD',unit_ids=['w4-c-13','w4-c-14'],finding_ko='13.05(12)는activity at calibration을확인하지만calibration date/time자체·inner label·specificradiationlicense/SOP는별도authority미확보.13.05(6)(d)의trigger는처방접수시nameunknown이고72시간내name뿐아니라address를요구하며facilityaddress예외도있어본문의name요약만으로조건전체를대체할수없다.'),
 dict(finding_id='W13-KIT-QUALIFICATION',status='HOLD_FOR_SCOPE_REVIEW',unit_ids=['w4-b-7'],finding_ko='Policy2023-07III(E)는pre-measuredcompoundingkit를compounding으로본다.본문의제조사지시변경kit 설명은이와manufacturer-directed simple reconstitution III(B)를더명확히구분할여지가있다.원문미수정.'),
 dict(finding_id='W13-USCODE-VERSION',status='VERSION_LIMITATION_NOT_CURRENT_LEGAL_CERTIFICATE',unit_ids=['w4-b-3','w4-b-4','w4-b-5','w4-c-10','w4-c-15','w4-c-16','w4-c-17','w4-c-18'],finding_ko='2025GovinfoHTML/PDF는200PageNotFound,Houseprelim404로credit0. freshlyretrieved2024USCodePDF와현재FDA게시의실제겹치는범위를대조했다.2025법전/amendment완전성및개별시행일미확정.'),
]
units=[]
for au in a['units']:
 uid=au['unit_id'];u=ub[uid];cs=[c for c in claims if c['unit_id']==uid];blocked=sum(c['review_status']=='SOURCE_BLOCKED' for c in cs)
 units.append(dict(unit_id=uid,title=u['title'],unit_content_sha256=h(u['body'].encode()),stored_metadata_body_sha256=u.get('body_sha256'),claim_count=len(cs),body_read_completely=True,body_read_actor_role='AUTHOR',census_status='COMPLETE_AUTHOR_ENUMERATION_PENDING_INDEPENDENT_COMPLETENESS_CHECK',atomic_claim_census_complete=True,source_checked_claim_count=len(cs)-blocked,source_blocked_claim_count=blocked,independent_verified_claim_count=0,related_question_ids=sorted({q for c in cs for q in c['related_question_ids']}),practice_coverage_gap_claim_ids=[c['claim_id'] for c in cs if not c['related_question_ids']],editorial_nonlegal_inventory=['제목·중복강조·타장링크·다시확인하라는학습지시·현재특정GLP1소송을판정하지않는범위설명은새법적권한명제로부풀리지않았다.'],unresolved_finding_ids=[f['finding_id'] for f in findings if uid in f['unit_ids'] and f['status'].startswith('HOLD')],legal_verification_status='SOURCE_SCOPE_BLOCKED' if blocked else 'AUTHOR_SOURCE_COMPARED_IDENTIFIED_VERSION_NOT_INDEPENDENT_LEGAL_PASS'))
summary=dict(units=len(units),atomic_claims=len(claims),source_checked=sum(c['review_status']=='AUTHOR_SOURCE_CHECKED' for c in claims),source_blocked=sum(c['review_status']=='SOURCE_BLOCKED' for c in claims),independent_verified=0,linked_public_question_ids=len(qids),supplementary_original_questions_read=23,question_author_review_credit=0,canonical_question_audit_credit=0,claims_with_direct_practice_link=sum(bool(c['related_question_ids']) for c in claims),practice_coverage_gap_claims=sum(not c['related_question_ids'] for c in claims))
census=dict(schema_version='note-atomic-claim-census/1',wave_id='NOTE-WAVE13',reviewed_at='2026-11-03',assignment_path=str(assignment_path.relative_to(ROOT)),assignment_sha256=h(assignment_path.read_bytes()),selection_ledger_snapshot=dict(path=str((OUT/'selection-notes-unit-ledger.jsonl').relative_to(ROOT)),sha256=h((OUT/'selection-notes-unit-ledger.jsonl').read_bytes()),origin='/workspace/pr187-final/reports/full-corpus-review/notes-unit-ledger.jsonl',selection_complete_units_at_origin=172,worker_generated_ledger_not_selection_evidence=True),notes_revision=bodydata['revision'],method_ko='20개배정currentJ본문전문을직접읽고숫자·기산점·자격·예외·권한·scope·label/record필드의법적관계를AUTHOR가수동열거했다.자동sentence/tableclause분해는사용하지않았다.완전은authorenumeration만뜻하며독립완전성·현행법전수확정·RELEASEPASS가아니다.',actor_provenance=dict(actor_role='AUTHOR',reviewer_instance=provenance,independent=False,future_self_independent_review_prohibited=True),sources=sources,units=units,claims=claims,discrepancies=findings,question_link_review_path=str(qpath.relative_to(ROOT)),question_link_review_sha256=h(qpath.read_bytes()),summary=summary,failed_optional_retrievals=[dict(source_id=sid,official_url=s['official_url'],http_status=s.get('http_status'),status=s['retrieval_status'],verification_credit=0) for sid,s in sources.items() if s['retrieval_status']=='SOURCE_BLOCKED'],independent_audit='NOT_RUN',all306_complete=False,content_mutated=False,existing_open_claim_registry_unchanged=True,K_whole_HOLD_candidate_applied=False,emergency_M_candidate_applied=False,source_limitations=['Firecrawl credit-exhausted; request not executed. Direct officialHTTPS used.','Failed403/404/HTTP200PageNotFound/emptyresponses verificationcredit0.','FullUSPtechnicalprovisions not acquired; no copyrightUSPchaptertext redistribution.','2024USCodeedition contentcomparison is not proof of2025/2026amendmentcompleteness.','Publicpractice2346links and canonical439scope are separate; canonicalmapping/auditsNOT_RUN.'],next_action_ko='정확한currentbody에대한별도독립completeness/legalreview와USPfulltext/radiationauthority확보가필요하다.이번AUTHOR는20개자기독립감사를하지않고본문수정후보도만들지않았다.')
outpath=ROOT/'reports/full-corpus-review/note-wave13-census.json';outpath.write_text(json.dumps(census,ensure_ascii=False,indent=2)+'\n');(OUT/'sources-manifest.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False,indent=2));print('CENSUS_SHA256',h(outpath.read_bytes()))
