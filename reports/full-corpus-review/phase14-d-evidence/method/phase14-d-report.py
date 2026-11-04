exec(open('/tmp/phase14-d-build.py').read())
packet=json.load(open(out/'assigned-visible-input.json'));assignment=json.load(open(out/'assignment.json'));near=json.load(open(out/'nearest-visible-comparison.json'))
source_by_id=sources
claim_index=json.load(open('/tmp/phase14-d-claims-index.json'));claims={}
def add(i,truth,ids,reason):claims[i]=dict(truth=truth,source_ids=ids.split(),reason_ko=reason)
add(1,True,'fda-applications','BLA는 생물학적 제품을 판매하기 위한 허가 신청 경로이며 약사의 개인 면허가 아니다.')
add(2,True,'fda-orange-preface 247-9','ANDA 승인만으로 다른 투여경로나 IR/ER 등 서로 다른 제형의 제품 전반이 상호대체 가능해지는 것은 아니다. 제품별 pharmaceutical/therapeutic equivalence와 주법상 대체조건이 남는다.')
add(3,False,'fda-applications','NDA 제출은 심사 요청이며 승인이라는 FDA의 후속 결정과 다르다. 제출만으로 판매 승인 상태가 되지 않는다.')
add(4,True,'fda-applications','IND는 임상연구에서 주간 운송 등에 대한 예외 경로이다. 연구 경로를 일반 소매 판매 승인으로 바꿔 읽을 수 없다.')
add(5,False,'fda-eua','EUA는 특정 제품·용도·대상·조건에 한정된다. 승인 대상 인구와 사용 조건을 확인할 필요가 없어지는 경로가 아니다.')
add(6,False,'mgl94c9','Off-label 사용 가능성과 약사의 법적 처방 권한은 별도이다. 주법이 허용한 특정 약사 처방 경로는 있을 수 있지만 off-label이라는 사실이 포괄적 독립 처방권을 만들지는 않는다.')
add(7,False,'fda-otc','FDA는 OTC에 application 및 monograph 두 경로를 설명한다. 모든 OTC가 monograph이고 승인 신청 경로는 없다는 명제는 틀리다.')
add(8,True,'fda-ndc','NDC 부여와 listing에는 미승인 제품도 포함되므로 이 식별·등재 사실만으로 특정 제품의 FDA 승인이 증명되지 않는다.')
add(9,True,'fda-eua','EUA는 무제한 full approval과 구별하여 현재 authorization의 범위와 조건을 확인해야 한다.')
add(10,False,'fda-ndc','NDC와 검색 가능한 label을 함께 갖추어도 승인·미승인 구별을 대신할 수 없다. 승인 기록의 별도 확인이 필요하다.')
add(11,True,'fda-otc','OTC에는 승인 신청 또는 적용 가능한 monograph 경로가 있으며 OTC라는 판매구분만으로 하나로 고정할 수 없다.')
add(12,False,'fda-exemptions','면제 신청 중에도 준수 노력을 계속하도록 FDA가 명시한다. 신청 접수와 현재 효력이 발생한 승인·면제는 서로 다른 상태이다.')
add(13,False,'fda-smallletter fda-dscsa','면제 letter는 특정 조항만 열거하고 다른 §582 의무에는 적용되지 않는다고 명시한다. 문항이 제외하지 않은 공급자 자격·suspect 조사 의무가 소멸하지 않는다.')
add(14,True,'fda-smallletter','기업의 적용대상, 면제 조항, 효력 기간을 각각 확인해야 한다. 장래 연장과 현재 면제도 구별한다.')
add(15,False,'fda-smallletter','Small이라는 자체 명칭으로 eligibility가 확정되지 않는다. 소유 기업 전체의 기준일·대상 직원수 등 실제 요건을 적용해야 한다.')
add(16,False,'fda-smallletter','하나의 한정 면제가 모든 DSCSA 의무를 없애지는 않는다. Letter가 다른 요건의 존속을 명시한다.')
add(17,True,'fda-smallletter fda-dscsa','명시적으로 면제되지 않은 authorized partner 확인과 suspect 제품 격리·조사는 계속 적용된다.')
add(18,True,'fda-smallletter','기업 규모라는 일상적 표현 대신 결정문이 정한 직원·소유기업·기준일을 확인해야 한다.')
add(19,False,'gov-dscsa fda-dscsa','약국 간 판매는 specific patient need 충족 등 거래별 조건을 따로 평가한다. 거래 상대가 약국이라는 이유만으로 포괄 면제가 되지 않는다.')
add(20,True,'gov-dscsa fda-dscsa','제품 identifier와 거래 상대의 허가·등록 상태는 다른 요건이다. 제품 표지만으로 상대 자격이 확인되지 않는다.')
add(21,False,'gov-dscsa 247-9','공급망 tracing 자료는 거래·제품 추적 자료이다. 이를 환자별 처방 또는 처방권자의 적법한 명령으로 갈음할 수 없다.')
add(22,False,'gov-dscsa fda-dscsa','DSCSA 거래정보의 최소 6년 보존은 별도 연방 의무다. 다른 일반 약국 기록의 2년 기준으로 단축할 수 없다.')
add(23,False,'gov-dscsa fda-dscsa','Identifier는 제품 식별 요건이다. Authorized trading partner는 별도의 허가·등록 요건으로, identifier가 상대 자격을 증명하지 않는다.')
add(24,True,'gov-dscsa fda-dscsa','Covered transaction의 거래기록은 거래 이후 최소 6년 보존한다. 문항의 2년 파기는 이 요건을 충족하지 않는다.')
add(25,True,'gov-dscsa 247-9','Lot·serial·expiration 등은 공급망 식별과 추적에 쓰이며 환자별 적법한 처방의 독립 요건을 만들거나 대체하지 않는다.')
add(26,True,'gov-dscsa fda-dscsa','Specific patient need 등 실제 거래의 목적·조건이 충족되는지 확인해야 해당 예외를 적용할 수 있다.')
add(27,True,'gov-dscsa fda-dscsa','Suspect product 판단 시 이미 격리·조사 의무가 발생한다. Illegitimate 최종 확정까지 일반 판매 재고로 두는 방식이 아니다.')
add(28,False,'fda-notify','FDA 3911은 DSCSA illegitimate product 통지에 쓰인다. 기관과 신고 대상이 달라 DEA controlled-drug theft Form 106을 대체하지 않는다.')
add(29,False,'gov-dscsa fda-dscsa','Suspect 제품은 clear 또는 disposition될 때까지 격리한다. 저장 공간 확보만으로 미해결 제품의 격리를 끝낼 수 없다.')
add(30,False,'gov-dscsa fda-notify','24시간은 illegitimate determination부터 시작한다. 월말 정기보고까지 기다리는 것은 그 한계를 충족하지 않는다.')
add(31,True,'gov-dscsa fda-notify','Illegitimate 결정 후 24시간 안에 FDA와 관련 immediate trading partners에 통지한다. 최초 의심일이나 월례 보고일로 바꾸지 않는다.')
add(32,False,'gov-dscsa fda-dscsa','Suspect 단계부터 격리·조사가 필요하므로 최종 illegitimate 확정 전 일상적으로 조제할 수 있다는 주장은 틀리다.')
add(33,True,'fda-notify','FDA 3911과 선호되는 CDER NextGen 3911 platform은 DSCSA 통지를 위한 경로이며 DEA 절도보고와 구별된다.')
add(34,False,'ecfr7-20261102','21 CFR 7.3(h)는 correction을 물리적 다른 장소로의 이동 없이 수리·수정·표지변경·검사 등으로 정의한다.')
add(35,False,'ecfr7-20261102','어떤 lot 부분도 판매·사용을 위해 release되지 않고 전량 직접통제하에 있다는 B 사실은 stock recovery에 부합한다. 환자 단계 recall로 필연 분류되지 않는다.')
add(36,False,'ecfr7-20261102 mgl39d 247-20','연방 recall 범주의 제외는 MA의 결함 조제품 회수·보고나 다른 안전 의무까지 없애는 조항이 아니다. 발생사실별 독립 의무는 남는다.')
add(37,True,'ecfr7-20261102','시장에 나온 제품의 FDA 법적조치 대상 위반이라는 A 사실이 recall 정의에 해당한다. 회사가 붙인 commercial withdrawal 명칭이 법적 조건을 바꾸지 않는다.')
add(38,True,'ecfr7-20261102','전량 직접통제되고 lot 어느 부분도 판매·사용 release되지 않았다는 B의 두 조건이 stock recovery 정의와 맞는다.')
add(39,False,'ecfr7-20261102','분류는 실제 위반·유통·통제 조건으로 결정된다. 회사가 commercial withdrawal이라 부르는 것만으로 recall 해당성이 사라지지 않는다.')
add(40,True,'ecfr7-20261102','Correction은 실제 이동 없는 relabeling·repair·inspection 등을 포함하므로 제품 이동이 필수는 아니다.')
add(41,False,'ecfr7-20261102 fda-recall-enforce','Class III는 위해 가능성 분류이며 recall 취소나 notice 이행 면제가 아니다. 공지된 해당 lot 조치는 별도로 수행한다.')
add(42,False,'ecfr7-20261102 fda-recalls','Class I는 심각한 위해·사망의 합리적 가능성을 뜻한다. 가장 낮은 위해 구분이라는 설명은 Class I/III를 뒤바꾼다.')
add(43,True,'fda-recall-enforce ecfr7-20261102','회사 통지는 FDA classification보다 먼저 가능하다. 분류 대기는 해당 lot을 notice에 반해 계속 조제할 근거가 아니다.')
add(44,False,'fda-recall-enforce','위험도 class만으로 어떤 lot이 누구에게 전달되었는지는 알 수 없다. Lot/code와 분배·조제기록을 추적해야 한다.')
add(45,False,'fda-recall-enforce ecfr7-20261102','Recall 개시·통지와 FDA classification은 별도 사건이다. 분류 완료 전 조제를 계속하라는 결론은 틀리다.')
add(46,True,'ecfr7-20261102 fda-recall-enforce','Class III의 위해 가능성이 낮더라도 notice를 무시할 수 있게 하는 면제가 아니다. Lot-specific 지시를 적용한다.')
add(47,True,'ecfr7-20261102 fda-recalls','21 CFR 7.3(m)(1)이 Class I을 serious adverse health consequences 또는 death의 reasonable probability로 정의한다.')
add(48,False,'247-13','방사능량 표지는 calibration 시점에서의 양과 연결된다. 방사성 약품의 정보가 시점과 무관하게 불변이라는 설명은 틀리다.')
add(49,True,'247-13','일반 약사 등록에 더하여 Board가 인정한 qualified nuclear pharmacist와 해당 시설의 적용 법규 준수가 필요하다. 개인 면허 하나로 시설 권한까지 성립하지 않는다.')
add(50,False,'247-13','13.05(5)의 radiopharmaceutical 취득·처분 기록은 최소 3년이다. 1년만이라는 설명은 이 특별 요건에 반한다.')
add(51,False,'247-13','13.05(6)(d)는 이름이 초기 미상인 경우 조제 후 72시간 내 이름·주소 확보를 요구한다. 영구적인 생략 경로가 아니다.')
add(52,False,'247-13','일반 등록과 nuclear 교육·경험·Board 인정 및 시설 준수는 별도 조건이다. 일반 면허가 이를 자동 확정하지 않는다.')
add(53,True,'247-13','대상 예외에서는 조제 후 72시간 내 환자 이름·주소를 확보한다. 보기의 이름 확보 기한은 맞지만 주소 의무도 별도로 존속한다.')
add(54,True,'247-13','13.05(5)는 취득·처분 상세 기록을 readily retrievable 형태로 최소 3년 유지하도록 한다.')
add(55,True,'247-13','13.05(12)(e)의 radioactivity 양은 calibration 시점을 기준으로 하므로 그 날짜·시간과 함께 해석해야 한다.')
add(56,True,'policy-definitions 247-15','정책 II.F의 QRE는 환자에게 도달한 잘못된 조제이다. 전달 전 차단은 그 정의와 다르지만 안전분석 가치가 없다는 결론은 아니다.')
add(57,False,'ecfr310-20261102','Adverse experience는 전문 실무상 정상 사용 중에도 발생할 수 있다. 정확한 제품 선택·라벨링이 모든 약물 반응을 배제하지 않는다.')
add(58,False,'mgl39d 247-9 247-20','결함 판단·결함 가능성에 따른 격리·회수·보고는 환자상해가 이미 발생했다는 사실을 필수로 하지 않는다.')
add(59,False,'policy-definitions mgl39d 247-20','Untoward event/SADE와 defective preparation은 분류 및 발동요건이 다르다. 모든 경우 동일 범주·동일 trigger라는 주장은 틀리다.')
add(60,False,'policy-definitions','환자가 받은 오류라는 II.F 문구와 도달 전에 차단된 사실이 다르다. Near miss를 그 patient-received QRE와 동일시할 수 없다.')
add(61,True,'policy-definitions mgl39d 247-20','부작용의 결과·preventability와 품질결함 여부는 서로 다른 사실이다. 관련 보고 경로가 겹칠 수 있어도 발동요건은 동일하지 않다.')
add(62,True,'mgl39d 247-9','알려진 결함은 상해가 없더라도 조제할 수 없다. 결함조제품은 즉시 격리·회수 대상이 될 수 있다.')
add(63,False,'247-15','15.03(3)(a)는 workflow·기술·교육·staffing 등 시스템 요인 검토를 명시한다. 비난할 직원만 찾는 프로그램으로 한정할 수 없다.')
add(64,False,'247-15','변경 권고·통지만으로 effectiveness가 입증되지 않는다. CQI 분석과 기간별 standards를 측정하는 indicators를 유지해야 한다.')
add(65,False,'247-15','15.02(1)(f)는 pharmacy personnel에 ongoing CQI education을 최소 연례로 제공하도록 하므로 개설 당시 일회 교육은 부족하다.')
add(66,True,'247-15','직원명 목록만으로 사건 탐지·기록·분석·예방을 위한 written CQI와 원인·기여요인 평가를 대체할 수 없다.')
add(67,True,'247-15','15.03(3)의 분석·개선·측정지표 취지상 변경 시행 여부와 목표한 개선 효과를 평가해야 한다. 이 문항이 특정 법정 staffing 수치를 추가하지는 않는다.')
add(68,False,'247-15','직원 이름 기록 외에 사건 내용, 원인·기여요인 분석 및 예방 프로세스가 요구되므로 명단만으로는 충족되지 않는다.')
add(69,True,'247-15','15.02(1)(f)는 CQI에 관한 pharmacy personnel의 교육을 최소 매년 제공하도록 한다.')
add(70,False,'247-15','15.04(2)는 QRE report일부터 최소 2년 보존을 요구한다. 환자가 수정을 수용했다고 즉시 폐기할 수 없다.')
add(71,False,'247-15','15.03(2)(a)의 initial documentation은 발견·전달 후 24시간 이내이다. 기여요인 조사가 끝날 때까지 전부 보류하는 조건은 없다.')
add(72,True,'247-15','월요일 10시 발견한 경우 initial record clock은 그 발견부터 24시간이다. 금요일 최종 조사완료로 시작점을 늦추지 않는다.')
add(73,False,'247-15','15.03(1)의 환자통지와 15.03(2)의 문서화는 별도 의무이며 어느 하나로 다른 것을 갈음하지 않는다.')
add(74,False,'247-15','24시간 기산점은 pharmacist가 발견했거나 전달받은 때이다. Investigation 완료가 기산점이라는 조항은 없다.')
add(75,True,'247-15','환자와 소통하고 교정해도 최초 기록·분석 및 보존 의무가 남는다.')
add(76,True,'247-15','QRE 기록은 QRE report일로부터 최소 2년이다. 조사 완료일이나 환자 수용일과 구별한다.')
add(77,False,'policy-definitions ecfr310-20261102 fda503b','MA SADE의 preventable 및 열거된 결과 정의와 연방 503B serious-and-unexpected 보고는 별도 요건이다. 둘을 상호교환할 수 없다.')
add(78,True,'policy-definitions','II.I는 ED에서 추가 치료·검사·모니터링을 받는 상해를 포함한다. 입원이 없어도 문항 사실이 serious-injury 범위에 해당할 수 있다.')
add(79,False,'policy-definitions ecfr310-20261102','II.G는 이후 심각한 결과로 발전하는 사건을 고려한다. 처음의 임상 설명이 이후 보고 trigger 재평가를 막지는 않는다.')
add(80,False,'policy-definitions','II.I는 생명 위협, serious disability 및 병원/ED 추가 치료·검사·모니터링을 포함한다. 사망·입원만의 배타적 조건이 아니다.')
add(81,False,'policy-definitions','입원하지 않아도 ED 추가 치료·모니터링이라는 II.I의 경로가 남아 있다. 입원 부재만으로 배제할 수 없다.')
add(82,True,'policy-definitions','관리자는 실제 serious-injury 정의의 각 경로를 적용해야 한다. 사망이나 입원을 유일한 검사로 쓰면 ED 경로 등을 누락한다.')
add(83,True,'policy-definitions ecfr310-20261102','추가 임상정보로 serious 결과가 나타나면 적용 의무를 재평가한다. MA 정의의 진행 가능성과 연방 follow-up 체계도 초기 평가 고정과 맞지 않는다.')
add(84,True,'policy-definitions ecfr310-20261102 fda503b gov353b','MA preventable SADE와 연방 503B의 serious/unexpected 기준은 다른 체계이며 보고의 기관·조건도 따로 평가한다.')
add(85,True,'mgl39d 247-20','39D(b)의 가능한 신속한 보고 및 7 business days 한계와 20.02(1)의 MOR 보고를 함께 적용한다. 이 사례는 오류와 serious injury 발견이 같은 날이므로 두 기산점 차이로 답이 달라지지 않는다.')
add(86,False,'247-20 247-15','20.02(3)은 Board 보고가 CQI에 추가됨을 명시한다. 환자통지와 내부 기록을 없애는 효과가 없다.')
add(87,False,'247-20','20.02(5)의 nonresident 제외만 읽으면 불완전하다. 20.07(3)이 Massachusetts로의 improper dispensing에 대한 별도의 7 business days 보고를 규정한다.')
add(88,False,'247-20','20.02(4)의 심각한 오류·SADE 관련 기록은 Board report filing부터 최소 5년이다. 일반 prescription 기록 2년으로 단축하지 않는다.')
add(89,True,'247-20','해당 improper dispensing 관련 모든 기록은 보고서가 Board에 제출된 날부터 최소 5년 보존하고 readily retrievable해야 한다.')
add(90,False,'247-20 mgl39d','해당 보고 한계는 7 business days이다. 7 calendar days로 단위를 바꿀 수 없다.')
add(91,True,'247-20 247-15','Board 보고는 별도 환자통지·교정·CQI 문서화 의무를 대체하지 않는다. 관련 규정이 병행을 요구한다.')
assert set(claims)==set(range(1,92))
# Current default-pool membership is projected without reading editorial conclusions.
sel_path='practice_expansion/2026-10-28-representative/selection.json';recommended=set(json.load(open(root/sel_path))['recommended_ids'])
style=json.load(open(root/'data/exam_style/mpje_style_profile.json'));blueprint=json.load(open(root/'data/blueprint.json'))
ctype=lambda sid:'MA_PROMULGATED_REGULATION' if sid.startswith('247-') else 'MA_BOARD_POLICY' if sid=='policy-definitions' else 'MA_STATUTE' if sid.startswith('mgl') else 'FEDERAL_STATUTE' if sid.startswith('gov') else 'FEDERAL_REGULATION' if sid.startswith('ecfr') else 'FDA_OFFICIAL'
def auth(sid):
 d=dict(source_by_id[sid]);d.update(authority=sid,source_type=ctype(sid));return d
family_notes={
'FDA01':('IND 연구경로와 ANDA 제품승인의 두 사례는 판매·대체 승인 구별을 다루지만, INCORRECT의 NDA 제출 논점은 별도 사례 사실 없이 추가된다.','NDA 제출/승인 혼동 자체는 법적으로 의미가 있으나 BLA를 약사 개인 면허와 대조하는 설명은 분류 지식 수준이다.','NDA에 관하여 stem 사실이 없고 네 약어의 정의를 병렬로 고르게 해 자연스러운 사례 통합이 약하다.'),
'FDA02':('NDC 등재를 승인으로 오해하는 도매상과 조건 확인 없는 EUA 사용은 실제 승인 확인 업무로 가능하다.','Off-label이면 포괄적 약사 처방권이라는 오답은 승인확인과 직종권한을 크게 건너뛰어 설득력이 낮다.','OTC 경로·약사 처방권은 제시된 두 제품의 사실 없이 함께 끼어들어 하나의 실무 결정을 이루지 못한다.'),
'FDA03':('DSCSA 한정 면제 후 공급자·suspect 의무까지 생략하려는 계획은 면제 적용에서 가능한 오류이다.','면제 신청과 승인, 소규모 자칭과 실제 eligibility는 실제 혼동이다.','면제 scope와 존속 의무는 자연스럽게 연결된다. 다만 stem이 해당 의무는 면제에 없다고 미리 말해 답의 핵심을 제공한다.'),
'FDA04':('공급자 자격 미확인과 거래기록 2년 파기는 입고·보관 실무에서 발생 가능한 점검이다.','제품 identifier를 환자 처방 권한으로 삼는 오답은 제품 추적과 처방을 너무 멀리 연결해 실제 법적 혼동으로 약하다.','공급망 자격·보존은 연결되지만 구체적 환자 거래가 제시되지 않은 예외와 처방권 논점은 부가 목록이다.'),
'FDA05':('Suspect 격리와 illegitimate 확정 후 통지 시점은 같은 제품 조사 흐름으로 자연스럽다.','공간 확보만으로 격리를 해제한다는 오답과 FDA3911을 DEA106으로 바꾸는 오답은 합리적인 조사대안으로 매우 약하다.','의심·조사·확정·통지가 순차적으로 결합되며 서로 다른 clock을 구별하는 것이 적절하다.'),
'FDA06':('출하된 위반품과 직접통제 중인 미출하 lot의 회수 범주는 생산·구매 실무에서 비교 가능하다.','Stock recovery/market withdrawal/correction 구별은 실제 혼동이지만 non-recall이면 모든 안전·보고 의무가 없다는 오답은 과도한 절대명제다.','FDA 분류에 별도 MA의무를 남기는 연결은 타당하나 patient-level로 확정한다는 선택지는 사실의 lot 미출하 조건을 직접 거스른다.'),
'FDA07':('분류 전에 통지된 recall과 ClassIII 공지는 약국 재고 대응에 실제 발생 가능하다.','Recall 위험 class만으로 투약 환자가 특정된다는 선택지는 lot 추적의 의미를 거의 상식으로 제거할 수 있어 약하다.','분류 시점과 notice 이행은 연결되며 ClassI 정의는 사례 결정에 직접 필요하지 않은 추가 지식이다.'),
'NUC01':('핵약국 자격과 이름 미상 처방의 후속 확보는 특수 약국에서 가능한 상황이다.','방사능 정보가 calibration 시점과 무관하게 불변이라는 오답은 법적 오인보다 기초 물리 지식으로 제거된다.','자격·환자 정보 확보는 연결되나 취득·처분기록과 calibration을 같은 결정에 결합할 구체 사실이 없다.'),
'CQI01':('환자 도달 전 강도 오류, 정상조제 후 반응, 상해 없는 결함을 구분하는 상황은 안전 업무에서 가능하다.','정확한 조제가 모든 부작용을 배제한다는 오답은 법률 검토 없이도 제거할 수 있는 과도한 주장이다.','QRE·adverse event·defect의 구분은 자연스럽지만 보고 기관·행동을 고르지 않고 범주 정의만 확인한다.'),
'CQI02':('직원명 목록만 남기고 원인분석이 없거나 개선 후 효과를 확인하지 않는 CQI 문제는 실무상 가능하다.','책임자를 비난하는 것만이 CQI이고 시스템 요인은 밖이라는 오답은 프로그램 명칭만 알아도 제거하기 쉽다.','원인분석과 시행·효과 평가의 연결은 CQI 흐름에 맞고 연례교육은 별도로 존속한다.'),
'CQI03':('월요일 발견 후 금요일 조사완료까지 최초 기록을 미루려는 상황은 QRE 보고 과정의 실제 혼동이다.','조사완료와 초기기록, 환자통지와 내부기록, 환자수용과 보존기한의 혼동이 서로 다른 법적 의무를 시험한다.','같은 QRE의 발견·환자통지·초기기록·보존이 시간순으로 자연스럽게 결합된다.'),
'CQI04':('ED에서 추가치료를 받았지만 입원은 없는 환자는 serious injury 기준을 구별할 현실적인 사례다.','처음 임상설명이 이후 악화에도 영구 고정된다는 오답은 현실의 임상보고 대안으로 약하며 규정 없이도 제거하기 쉽다.','ED serious injury를 판단하면서 SADE와 federal503B의 차이를 보조 확인할 수 있지만 제품유형·preventability 사실은 제시되지 않는다.'),
'CQI05':('Resident MOR가 심각한 오류를 발견한 뒤 보고와 기록보존을 결정하는 연속업무는 현실적이다.','7 calendar/business days, 2년/5년 기록, nonresident 제외조항과 별도조항, CQI 병행은 모두 실제 조문 혼동에 근거한다.','동일 사건의 보고 trigger·담당자·기한·보존·병행 의무가 연결되고 동시 발견 사실이 두 공식 trigger 차이의 불필요한 모호성을 줄인다.')}
# Per-item judgments fixed by this reviewer after reading; not copied from keys.
passids={'MA-EXP-0985','MA-EXP-0986','MA-EXP-0988','MA-EXP-0993','MA-EXP-0994','MA-EXP-0996'}
realism_defects={
948:('natural_rule_combination','NDA 신청 상태는 주어진 IND/ANDA 사례 어디에도 없어 사례 적용보다 약어 정의 확인으로 답한다.'),
949:('authentic_distractors','B의 off-label이 약사 포괄 처방권을 준다는 주장은 NDC 승인 증명과 다른 층으로 멀리 벗어난다.'),
950:('authentic_distractors','B의 NDC 승인, C의 모든 OTC monograph, D의 포괄 처방권은 EUA 조건 판단의 실제 대안으로 충분히 경쟁하지 못한다.'),
952:('natural_rule_combination','INCORRECT 정답인 약사 off-label 처방권이 두 승인 증거 사례 밖의 추가 쟁점으로 놓여 있다.'),
953:('wording_not_guessable','CaseA가 이미 specified requirements와 defined period라고 말해 C의 범위·기간 확인을 거의 그대로 지시한다.'),
954:('wording_not_guessable','Stem이 unrelated supplier/suspect obligations are not among exempted requirements라고 답의 근거를 명시한다.'),
956:('wording_not_guessable','A의 신청=효력은 단계 자체를 같다고 하는 극단 명제이고 나머지는 조건 확인 문구여서 사례 판단 없이 제거하기 쉽다.'),
957:('authentic_distractors','C의 traceability가 처방권자 명령을 대체한다는 주장은 공급자 자격 판단의 실질적 경쟁대안이 아니다.'),
958:('authentic_distractors','A의 추적자료=환자처방권과 B의 identifier=공급자자격은 6년 보존기한 판단에서 너무 멀리 벗어난다.'),
959:('natural_rule_combination','네 보기 모두 옳은 SATA는 허용되지만 B의 처방권과 C의 거래 예외를 적용할 환자·거래별 사실이 없어 관련요건 목록으로 넓어진다.'),
960:('authentic_distractors','D의 모든 약국간 거래가 무조건 면제라는 과잉 일반화만 틀리고 A-C는 제한을 보존하는 문구여서 경쟁력이 약하다.'),
961:('authentic_distractors','저장 공간 확보로 미해결 격리를 끝내거나 FDA3911을 DEA양식으로 보는 선택지가 실제 조사결정의 경쟁안으로 약하다.'),
962:('wording_not_guessable','B만 24시간과 determination을 구체적으로 연결하고 A,C,D는 공간·기관·의심중조제라는 명백한 부적절행위여서 정답이 두드러진다.'),
964:('authentic_distractors','C의 단지 공간을 만들기 위한 격리 해제는 조사 미완료 사실과 정면 충돌하여 법적 예외를 검토할 여지가 없다.'),
965:('authentic_distractors','C의 non-recall이면 어떤 안전·보고 의무도 없다는 주장은 실제 명칭/위반 경계의 경쟁대안으로 너무 넓다.'),
966:('wording_not_guessable','B가 명칭만으로 category 결정, C가 모든 안전의무 삭제, D가 correction은 항상 이동이라는 절대 명제라 A만 신중한 표현으로 드러난다.'),
968:('authentic_distractors','B의 모든 다른 의무가 제거된다는 절대 명제만 틀리고 A,C,D는 각각 제한적인 정의 서술이어서 법규 적용 부담이 작다.'),
969:('authentic_distractors','D의 class만으로 환자식별은 분류와 기록을 지나치게 혼동하며 B는 ClassI 심각도를 완전히 뒤집어 경쟁력이 낮다.'),
970:('authentic_distractors','A의 class만으로 환자식별 및 C의 ClassI가 최저위험이라는 오답은 ClassIII recall이행 판단의 섬세한 대안이 아니다.'),
972:('authentic_distractors','A가 class만으로 환자까지 특정한다고 해 개별lot 추적 사실 없이 상식으로 배제된다.'),
973:('authentic_distractors','A의 방사능 정보 불변과 D의 영구 이름면제는 자격과 허가의 실제 경계보다 과도한 부정확성이다.'),
974:('authentic_distractors','B의 calibration 무관 불변과 A의 일반면허=모든 nuclear권한은 72시간 후속확보와 동등한 경쟁안이 아니다.'),
975:('natural_rule_combination','SATA 전부 정답 자체는 문제가 아니나 자격·기록3년·물리 calibration·이름72시간 네 판단을 연결하는 구체 nuclear조제 사실이 없다.'),
976:('reasoning_not_trivia','D의 calibration 무관 불변을 찾는 데 핵약학 법규 적용보다 방사성 변화라는 일반 지식이 결정적이다.'),
977:('authentic_distractors','B의 정확한 조제는 부작용을 배제, C의 상해가 없으면 결함이 아님은 QRE정의와 경쟁하는 정밀한 법적 해석이 아니다.'),
978:('authentic_distractors','C의 부작용 불가능과 D의 상해 전 결함 불가능은 실제 보고 trigger의 조건을 혼동하는 수준보다 극단적이다.'),
980:('reasoning_not_trivia','INCORRECT C의 정확한 조제라면 부작용 불가라는 주장은 법적 QRE/defect 정의를 적용하지 않고도 임상상식으로 제거된다.'),
981:('authentic_distractors','비난만 해야 한다, 변경만으로 효과가 확정된다, 개설시만 교육한다는 오답이 예방 중심 CQI의 현실적 대안으로 약하다.'),
982:('wording_not_guessable','변경 시행·재발을 전혀 보지 않는다는 stem에 A만 evaluation을 제시하고 다른 보기는 극단적으로 의무를 없애 정답이 쉽게 노출된다.'),
984:('authentic_distractors','B의 시스템요인은 CQI 밖이고 비난만 하라는 명제가 지나치게 명백하여 cause-analysis 조문의 세부 적용이 필요하지 않다.'),
989:('authentic_distractors','C의 초기 설명 영구고정은 ED 추가치료와 serious injury 경계의 경쟁 법률해석으로 약하다.'),
990:('wording_not_guessable','C만 actual definition을 적용하라는 신중한 문구이며 다른 보기는 모든 예외를 배제하거나 두 제도를 같게 해 정답이 추정된다.'),
991:('natural_rule_combination','ED 상해 판단은 의미 있으나 B의 향후 새 정보와 D의 503B를 판단할 후속 경과·outsourcing제품 사실이 없어 요건 목록을 모두 고른다.'),
992:('authentic_distractors','D의 추가 serious outcome이 있어도 보고평가 고정이라는 주장은 실제 follow-up 법률해석으로 설득력이 약하다.')}
criteria_names=['jurisprudence_reasoning','practice_plausibility','authentic_distractors','wording_not_guessable','reasoning_not_trivia','natural_rule_combination','appropriate_drug_context','distinct_from_bank','not_schedule_flashcard','public_style_without_copying']
near_by={r['question_id']:r for r in near['records']};records=[]
for r in packet['records']:
 q=r['original_visible_content'];qid=q['question_id'];nr=near_by[qid];fam=nr['family_id'];inc='INCORRECT' in q['stem'];findings=[];expected=[];sids=set()
 for c in q['choices']:
  v=claims[claim_index[c['text']]];chosen=(not v['truth']) if inc else v['truth']
  if chosen:expected.append(c['id'])
  sids.update(v['source_ids']);findings.append(dict(choice_id=c['id'],option_text=c['text'],option_sha256=hashlib.sha256(c['text'].encode()).hexdigest(),statement_supported=v['truth'],selection_expected=chosen,reason_ko=v['reason_ko'],authorities=[auth(s) for s in v['source_ids']]))
 assert expected==q['correct_choice_ids'],(qid,expected,q['correct_choice_ids'])
 practice,distnote,natural=family_notes[fam];cn=nr['canonical_nearest'][0]['question_id'];pn=nr['public_nearest'][0]['question_id'];default=qid in recommended
 dupnote=f'현재 canonical 439문항 및 public 2349문항 전체를 stem·보기 TF-IDF로 측정한 뒤 nearest canonical {cn} 및 public {pn}의 원문 stem·모든 보기·키·해설을 읽었다. Public 후보는 같은 두 사례와 판단을 재사용한 family 변형이며, canonical 후보는 어휘/주제 유사성이 있어도 사건사실과 판단 경로가 다르다. 현재 문항의 default pool 포함은 {default}이다. Archived family 변형의 존재만으로 distinct criterion을 실패시키지 않았다.'
 criteria={k:True for k in criteria_names};notes={
 'jurisprudence_reasoning':f'{qid}: '+('오류 명제 하나를 찾는 INCORRECT 극성을 유지하며 ' if inc else '각 보기의 조건·행위를 구별하며 ')+f'{fam}의 규정상 범위와 시점을 적용해야 한다.',
 'practice_plausibility':f'{qid}: {practice}',
 'authentic_distractors':f'{qid}: {distnote}',
 'wording_not_guessable':f'{qid}: 단일선택/복수선택 지시와 '+('INCORRECT 부정 극성' if inc else '옳은 결론을 고르는 극성')+'을 명시한다. 보기 순서만으로 정답이 정해지지 않는지 모든 문구를 비교했다.',
 'reasoning_not_trivia':f'{qid}: {fam}의 행위와 예외 또는 기산점을 분리하는 판단은 법적 의미가 있다. 단순 숫자·반복만으로 실패 판정하지 않았다.',
 'natural_rule_combination':f'{qid}: {natural}',
 'appropriate_drug_context':f'{qid}: '+('핵약학 자격·기록 판단에는 radiopharmaceutical이라는 종류가 직접 관련되고 특정 brand는 필요하지 않다.' if fam=='NUC01' else '제품명·brand를 특정하지 않아도 승인상태·공급망·품질/보고라는 이 문항의 법적 판단이 가능하며 불필요한 약명을 장식으로 넣지 않았다.'),
 'distinct_from_bank':f'{qid}: {dupnote}',
 'not_schedule_flashcard':f'{qid}: 스케줄 번호를 외워 고르는 문항이 아니라 {fam}의 '+('보고·보존·병행 의무' if fam.startswith('CQI') else '승인·적용 범위 또는 취급 조건')+'을 묻는다.',
 'public_style_without_copying':f'{qid}: 공개 NABP sample의 선택지 지시·형식만 대조했다. Sample의 CE시간·schedule약물·만료순서 원문과 이 문항의 사례·보기 문구는 다르며 protected Pre-MPJE나 회상문항은 사용하지 않았다.'}
 if qid not in passids:
  crit,reason=realism_defects[int(qid[-4:])];criteria[crit]=False;notes[crit]=f'{qid}: {reason}'
 # Additional observed weaknesses are explicitly judged by family rather than similarity score.
 if fam in {'FDA02','FDA04','NUC01'}:
  criteria['natural_rule_combination']=False;notes['natural_rule_combination']=f'{qid}: {natural}'
 verdict='PASS' if all(criteria.values()) else 'FAIL'
 explanation={
 'read_complete_core_reasoning':True,'read_complete_choice_analysis_ids':[c['id'] for c in q['choices']],'read_complete_learning_boundary':True,
 'core_reasoning_finding_ko':'Core 한국어 해설 전체를 읽고 각 명제를 독립 source에 대조했다. 답과 범위 설명에 법적 오류를 찾지 못했다. '+('Nuclear 이름 기한과 별도로 주소 확보도 필요하며 설명의 이름 강조가 주소 의무를 없애지는 않는다.' if fam=='NUC01' else '공식 규정의 기산점·주체·예외를 이 사례에 한정하여 해석했다.'),
 'per_choice_explanation_findings':[dict(choice_id=c['id'],rationale_sha256=hashlib.sha256(q['explanation']['choice_analysis'][c['id']].encode()).hexdigest(),finding_ko='해당 한국어 보기해설 전문 및 포함된 교정 영문을 읽었다. '+next(x['reason_ko'] for x in findings if x['choice_id']==c['id']),error_found=False) for c in q['choices']],
 'learning_boundary_finding_ko':'동일 family 변형을 독립 사례 수로 세지 말라는 경계를 확인했다. 이를 법적 정답 근거나 현실성 자동 PASS/FAIL로 사용하지 않았다.'}
 rec=dict(question_id=qid,record_sha256=r['record_sha256'],family_id=fam,collection=nr['collection'],read_scope=dict(original_stem=True,all_choices=True,choice_count=len(q['choices']),stored_key=True,full_korean_core=True,full_per_choice_explanations=True,learning_boundary=True,visible_content_sha256=r['visible_content_sha256'],hidden_truth_or_previous_reviews_read=False),
 legal_review=dict(existing_answer_correct='YES',stored_key=q['correct_choice_ids'],independently_expected_key=expected,question_type=q['question_type'],incorrect_polarity=inc,per_choice_findings=findings,authorities=[auth(s) for s in sorted(sids)],verdict='KEEP',finding_ko=f'{qid}: '+('INCORRECT이므로 유일하게 틀린 명제 ' if inc else '각 명제의 지지 여부를 독립 판정하여 ')+','.join(expected)+'를 정답으로 재구성했다. 저장 키와 일치한다. 각 보기는 주체·조건·행위·예외·기간을 공식 자료에 대조했으며 원해설의 답 또는 범위 오류를 확인하지 못했다.',blocker=None,original_explanation_review=explanation,correction_fields=dict(required=False,stem_change=None,key_change=None,explanation_change=None)),
 realism_review=dict(verdict=verdict,decision='KEEP' if verdict=='PASS' else 'MAJOR_REWRITE',criteria=criteria,criterion_findings_ko=notes,finding_ko=f'{qid}: '+('10개 기준을 모두 충족한다. 법적 보고/문서화의 실제 혼동을 구별하는 연습으로 유지 가능하다.' if verdict=='PASS' else '법적 키는 유지 가능하지만 '+', '.join(k for k,v in criteria.items() if not v)+' 기준에 구체 결함이 있다. 해당 오답·사례 연결을 편집 후 새 current hash로 재감사해야 한다.'),duplicate_evidence=dict(status='ACTUAL_TOP1_VISIBLE_FULL_TEXT_READ',canonical_count=439,public_count=2349,canonical_nearest=nr['canonical_nearest'],public_nearest=nr['public_nearest'],top2_scope='discovery scores only; substantive comparison top1',semantic_finding_ko=dupnote,evidence_path=prefix+'nearest-visible-comparison.json',evidence_sha256=sha(out/'nearest-visible-comparison.json'),current_default_pool_member=default)),
 safe_hold_recommended=(verdict!='PASS'),release_eligible=False,required_next_action_ko='Canonical 입학·release 증거가 아닌 독립 legacy assessment로만 순차 통합한다. '+('추가 canonical 감사·adjudication 절차를 별도 수행한다.' if verdict=='PASS' else '지적된 현실성 결함을 editor가 고친 뒤 새 hash에 대해 fresh legal/realism 검토한다.'))
 records.append(rec)
report=dict(stage='independent-legacy',independent_of_authors=True,auditor='GPT',auditor_instance='GPT:/root/independent_wave14_d:20261104',actor_provenance=dict(actor_id='/root/independent_wave14_d',session_id='/root/independent_wave14_d'),canonical_audit=False,canonical_release_credit=0,release_eligible=False,reviewed_at=date,completed_at=now,job_id=assignment['job_id'],question_hashes=assignment['question_hashes'],style_profile=dict(profile_id=style['profile_id'],content_version=style['content_version'],content_hash=style['content_hash'],file_sha256=sha(root/'data/exam_style/mpje_style_profile.json')),blueprint=dict(blueprint_id=blueprint['blueprint_id'],content_version=blueprint['content_version'],content_hash=blueprint['content_hash'],file_sha256=sha(root/'data/blueprint.json')),methodology_evidence_path=prefix+'methodology-manifest.json',methodology_evidence_sha256=sha(out/'methodology-manifest.json'),sources=list(source_by_id.values()),records=records,summary=dict(assigned_count=40,complete_visible_reads=40,choice_reads=160,legal_yes=40,legal_keep=40,realism_pass=sum(r['realism_review']['verdict']=='PASS' for r in records),realism_fail=sum(r['realism_review']['verdict']=='FAIL' for r in records),source_blocked=0,canonical_release_credit=0),limitations_ko=['공식 primary 게시본과 latest issue를 직접 읽은 독립 session이다. 법규의 모든 과거 commencement를 재구성하지 않았고 각 source별 시행일/버전 한계를 명시했다.','403/404/PageNotFound/내용 없는 200과 Firecrawl credit 실패는 법률검증 성공으로 계산하지 않았다.','가장 가까운 canonical/public top1 원문 전체를 비교했으며 top2 점수는 후보발견용이다. 자동 유사도 점수를 semantic verdict로 사용하지 않았다.','공개 NABP sample 외 Pre-MPJE, 회상문항, 상용 무단자료를 열거나 변환하지 않았다. Raw/text는 /tmp 사적 임시파일로만 보존하며 public repository에는 자체 memo/metadata SHA만 남긴다.'])
write(root/'reports/full-corpus-review/independent-phase14-d-review.json',report)
write(out/'independent-claim-adjudications.json',dict(reviewed_at=now,claims=[dict(claim_id=i,text=next(t for t,n in claim_index.items() if n==i),**v) for i,v in claims.items()],purpose='실제 읽은91개 고유 보기명제의 독립 판정; report에는160개 보기별로 다시 결합. 저장키나 authortruth를 truth근거로 사용하지 않음.'))
print(report['summary'])
