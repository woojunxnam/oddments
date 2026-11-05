import copy,datetime,hashlib,json,pathlib,shutil
B=pathlib.Path(__file__).resolve().parent;R=B.parents[2];P=B.relative_to(R).as_posix()
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
packet=json.load(open(B/'assigned-visible-input.json'));assignment=json.load(open(B/'assignment.json'));nearest=json.load(open(B/'nearest-visible.json'))
# Explicit reviewer-authored proposition assessment, indexed only by first visible occurrence.
# No stored key, hidden truth, author finding or earlier report is consulted to derive these values.
texts=[]
for row in packet['records']:
 for c in row['original_visible_content']['choices']:
  if c['text'] not in texts:texts.append(c['text'])
findings=[
(False,'247 CMR 9.05(2)는 generic-name/no-manufacturer 주문에 별도의 legally marketed 선택 경로를 둔다. Brand 지정 주문의 조건을 그대로 전부 이식할 수 없다.','ma2479','247 CMR 9.05(2)'),
(False,'같은 회사라는 정보만으로 특정 brand와 authorized generic의 제품 동일성이 확정되지 않는다. DCP는 FDA 목록으로 결정할 수 없으면 제조·유통·재포장 업체에 확인하도록 한다.','agdcp','DCP 22-01-112: final substantive paragraph'),
(False,'FDA 목록은 NDA 보유자의 보고 제품을 집계한다. 등재라는 사실은 그 약국의 현재 재고나 실시간 유통 사실을 증명하지 않는다.','agfda','Listing of Authorized Generic Drugs'),
(True,'FDA는 authorized generic이 원 brand의 NDA 아래 판매되어 별도 ANDA가 없을 수 있다고 명시한다. Case B의 ANDA 부재만을 이유로 한 배제는 성립하지 않는다.','agfda','How Is an Authorized Generic Drug Different: NDA paragraph'),
(True,'제품 대응 관계를 실제 확인해야 한다. 회사명만의 추정 대신 FDA listing과 필요한 경우 업체 확인을 사용하는 DCP 안내에 부합한다.','agdcp','DCP 22-01-112: final substantive paragraph'),
(True,'제조사가 지정되지 않은 generic-name 처방에서는 prescriber intent와 전문적 판단에 따라 legally marketed 제품을 고르는 별도 규칙을 적용한다.','ma2479','247 CMR 9.05(2)'),
(False,'응급 예외에서도 일자·시각·응급 성격 기록과 구매자의 서면 수락을 요구하는 9.05(1)(b)는 없어지지 않는다.','ma2479','247 CMR 9.05(1)(a)-(b)'),
(True,'Brand 재고 부재 등 조건이 충족된 medical emergency에서만 no-substitution 처방의 특별 대체 경로를 사용할 수 있다. 일반적인 지시 무시는 허용하지 않는다.','ma2479','247 CMR 9.05(1)(a)'),
(False,'규칙은 medical emergency와 재고 조건을 별도로 요구한다. 재고 부족 하나가 medical emergency를 자동 성립시키지 않는다.','ma2479','247 CMR 9.05(1)(a)'),
(False,'예외는 Massachusetts List상 interchangeable 제품에 관한 것이다. 같은 치료계열이라는 사실만으로 다른 약물로 변경하는 권한이 생기지 않는다.','ma2479','247 CMR 9.05(1)(a); M.G.L. c.112 §12D definition'),
(False,'9.05(1)(a)에 실제 emergency interchange 경로가 존재한다. Case A의 충족 조건을 전제로 그 경로 자체를 부정할 수 없다.','ma2479','247 CMR 9.05(1)(a)'),
(True,'날짜·시각·응급 성격 기록 및 구매자의 서면 수락은 9.05(1)(b)의 명문 조건이다. Case B의 누락은 이 조건을 충족하지 못한다.','ma2479','247 CMR 9.05(1)(b)'),
(True,'통상적 재고 편의는 조문이 요구하는 medical emergency와 구별된다. 이 문장은 응급 조건을 지워 버리지 않는다.','ma2479','247 CMR 9.05(1)(a)'),
(True,'§12EE(a)-(c)는 FDA가 interchangeable로 판단한 제품을 요건으로 한다. 단순 biosimilar 승인만으로 그 요건이 충족되는 것은 아니다.','ma12ee','M.G.L. c.112 §12EE(a)-(c)'),
(False,'Massachusetts §12EE(d)는 reasonable time이라고 규정한다. 다른 주의 5-business-day 숫자를 Massachusetts 법정기한으로 채택할 수 없다.','ma12ee','M.G.L. c.112 §12EE(d)'),
(False,'대체 허용과 표시·통지 의무는 별개다. §12EE(e)의 서면 환자 통지와 §21의 실제 약물명 label 의무는 대체에 의해 없어지지 않는다.','ma12ee','M.G.L. c.112 §12EE(e); c.94C §21 opening paragraph'),
(False,'§12EE(f)는 마지막 profile entry부터 최소1년 보존을 정하면서 Board professional standards의 적용을 제한하지 않는다고 명시한다. 다른 적용 보존법을 무시할 수 없다.','ma12ee','M.G.L. c.112 §12EE(f)'),
(True,'현행 §12EE(d)의 표현은 reasonable time이다. 근거 없는 다른 주 숫자로 이를 대체하지 않는 판단이 맞다.','ma12ee','M.G.L. c.112 §12EE(d)'),
(False,'§12EE(a)의 interchangeable 정의를 충족해야 하므로 모든 biosimilar가 자동으로 약사 대체 대상이라는 주장은 과도하다.','ma12ee','M.G.L. c.112 §12EE(a)-(c)'),
(True,'환자 서면 통지(§12EE(e))와 실제 조제약 명칭 표시(§21 opening paragraph)는 남는다. 불필요한 별도 고정기한을 추가하지 않은 표현이다.','ma12ee','M.G.L. c.112 §12EE(e); c.94C §21 opening paragraph'),
(False,'Pharmacy retail price는 바로 그 약국에서 바로 그 처방약을 보험·할인 없이 사는 가격이다. 무관한 제품의 광고가격으로 대체할 수 없다.','ma21c','M.G.L. c.94C §21C(a)-(b)'),
(False,'§21C는 해당 거래에서 cost-sharing와 pharmacy retail price 중 작은 금액을 청구하게 한다. 모든 상품·모든 보험 가격이 동일하다는 보장은 아니다.','ma21c','M.G.L. c.94C §21C(a)-(d)'),
(False,'보험 claim 승인 자체는 §21C(b)의 두 금액 비교를 증명하지 않는다. 더 낮은 retail price가 있는지 별도로 적용해야 한다.','ma21c','M.G.L. c.94C §21C(b)'),
(True,'적용 cost-share가 retail price보다 높으면 point of sale에서 더 낮은 retail price를 청구해야 한다. Case A의 비교에 맞는 결론이다.','ma21c','M.G.L. c.94C §21C(b)'),
(True,'보험 승인과 법률이 요구하는 청구액 결정은 별개다. §21C(b),(d)는 보험 거래 및 PBM 계약이 lesser-price 의무를 없애지 못하게 한다.','ma21c','M.G.L. c.94C §21C(b),(d)'),
(False,'보험 표시액이 더 높아도 §21C(b)의 lesser-price 의무가 적용된다. 표시액에 언제나 우선권을 주는 주장은 그 의무에 반한다.','ma21c','M.G.L. c.94C §21C(b)-(c)'),
(True,'법정 retail price 정의는 실제 해당 처방약·약국·거래를 가리킨다. 이 비교금액을 사용해야 한다.','ma21c','M.G.L. c.94C §21C(a)-(b)'),
(False,'16 CFR 1700.14에는 aspirin·acetaminophen 등 OTC에도 적용되는 성분·수량별 항목이 있다. OTC라는 사실만으로 일괄 면제되지 않는다.','cfr170014','16 CFR 1700.14(a)(1),(16),(20),(25)'),
(False,'Special packaging의 정의 자체가 모든 어린이가 열지 못하는 포장을 뜻하지 않는다고 명시한다. 절대적인 childproof 보장은 아니다.','cfr17001','16 CFR 1700.1(b)(4); 1700.15(b)(1)'),
(True,'Tamper evidence는 개봉 흔적, child resistance는 시험된 어린이 개봉 저항성이다. 211.132(b)(1)와 1700.1(b)(4)는 다른 성능을 규정한다.','cfr211132','21 CFR 211.132(b)(1); 16 CFR 1700.1(b)(4)'),
(False,'포장 요건은 성분·형태·수량·용도와 해당 예외로 결정한다. 진열 선반 위치만으로 결정하는 기준은 1700.14에 없다.','cfr170014','16 CFR 1700.14(a)'),
(False,'Tamper-evident 구조가 언제나 child-resistance 시험 요건을 충족하지는 않는다. CPSC는 두 기능이 구별됨을 설명한다.','cpscguide','January 2023 guide p.17: FDA tamper-evident question'),
(True,'OTC에도 1700.14의 개별 물질·수량 요건이 적용될 수 있으므로 OTC라는 지위만으로 면제를 확정할 수 없다.','cfr170014','16 CFR 1700.14(a)(1),(16),(20),(25)'),
(True,'1700.1(b)(4)는 모든 어린이가 열 수 없는 포장이라는 뜻이 아니라고 직접 규정한다.','cfr17001','16 CFR 1700.1(b)(4)'),
(False,'환자의 한 처방에 대한 요청에서 이후 모든 처방에 대한 무제한 요청을 추정할 수 없다는 CPSC 설명에 반한다. 서면은 일반적 법정 필수라기보다 많은 약국이 선택하는 입증 방식이다.','cpscguide','January 2023 guide p.12: individual request Q&A'),
(True,'환자는 자신의 모든 약을 conventional packaging에 담아 달라고 구체적으로 요청할 수 있다. 한 처방만의 요청과 범위가 다르다.','cpscguide','January 2023 guide p.12: individual request Q&A'),
(False,'고령이라는 사실만으로 환자의 실제 요청을 대체할 수 없다. 고객 또는 처방자의 구체적 선택이 필요하다.','cpscguide','January 2023 guide p.12: customer preference Q&A'),
(False,'처방자의 packaging 지시는 그 처방과 refill에 적용된다. 다른 처방까지 포괄하는 무제한 면제가 되지 않는다.','cpscguide','January 2023 guide p.12: physician standing order Q&A'),
(False,'CPSC는 환자가 자신의 모든 처방에 대한 구체적 요청을 할 수 있다고 명시한다. 이를 절대 금지하는 주장은 틀리다.','cpscguide','January 2023 guide p.12: individual request Q&A'),
(True,'처방자 요청은 해당 처방과 그 refill 범위이며 미래의 무관한 처방 전체로 확장되지 않는다.','cpscguide','January 2023 guide p.12: physician standing order Q&A'),
(True,'연령은 명시적 요청과 다르다. 약사가 선호를 안다고 해도 고객의 구체적 요청 없이 포장을 바꿀 수 없다는 안내에 부합한다.','cpscguide','January 2023 guide p.12: customer preference Q&A'),
(True,'21정×5mg=105mg이다. Prednisone tablet의 package total이105mg 이하이고 다른 해당 물질이 없으므로 명시된 제품 예외를 충족한다.','cfr170014','16 CFR 1700.14(a)(10)(x)'),
(False,'제품별105mg 예외를 충족하지 않는 것과 환자·처방자의 구체적 conventional-packaging 요청 가능성은 별개다. 전자가 후자를 자동 배제하지 않는다.','cpscguide','January 2023 guide pp.10,12; 16 CFR 1700.14(a)(10)(x)'),
(False,'22정×5mg=110mg이므로 개별 정제 강도5mg만으로105mg package-total 예외를 충족할 수 없다.','cfr170014','16 CFR 1700.14(a)(10)(x)'),
(False,'105mg 이하뿐 아니라 다른 1700.14(a)(10) 대상 물질을 포함하지 않아야 한다는 명문 조건도 지켜야 한다.','cfr170014','16 CFR 1700.14(a)(10)(x)'),
(True,'22정×5mg=110mg으로105mg 이하 조건을 넘는다. 이 제품 예외는 충족되지 않지만 다른 적법한 요청 경로까지 부정하는 것은 아니다.','cfr170014','16 CFR 1700.14(a)(10)(x)'),
(False,'21정이라는 수 자체가 배제 기준이 아니다. 총량105mg은 no more than105mg 조건에 포함된다.','cfr170014','16 CFR 1700.14(a)(10)(x)'),
(True,'Prednisone 예외에는 다른 해당 prescription-drug 물질이 없어야 한다는 조성 조건이 함께 있다.','cfr170014','16 CFR 1700.14(a)(10)(x)'),
(False,'Isosorbide dinitrate 예외는 sublingual 또는 chewable 제형이며10mg 이하 강도이다. 모든 제형·함량을 면제하지 않는다.','cfr170014','16 CFR 1700.14(a)(10)(ii)'),
(False,'제조사 mnemonic/dispenser package라는 조건이 붙은 예외를 임의 재포장에 자동 적용할 수 없다. 정확한 각 항목 조건을 다시 확인해야 한다.','cfr170014','16 CFR 1700.14(a)(10)(iv),(viii),(xvii),(xviii)'),
(False,'Potassium supplement 예외는 unit dose이며 dose당50mEq 이하이다. 임의 bulk bottle 전체를 함량과 무관하게 면제하지 않는다.','cfr170014','16 CFR 1700.14(a)(10)(vi)'),
(True,'Nitroglycerin의 명명된 예외는 sublingual dosage form이다. Nitrate 계열의 모든 제형으로 확장되지 않는다.','cfr170014','16 CFR 1700.14(a)(10)(i)-(ii)'),
(True,'Unit-dose 형태 및 단위당50mEq 이하라는 두 조건을 모두 유지하는 설명이다.','cfr170014','16 CFR 1700.14(a)(10)(vi)'),
(False,'Sublingual nitroglycerin이라는 특정 예외가 모든 nitrate formulation을 면제하지 않는다.','cfr170014','16 CFR 1700.14(a)(10)(i)-(ii)'),
(True,'Isosorbide dinitrate의 sublingual/chewable 및10mg 이하 강도라는 실제 범위를 보존한다.','cfr170014','16 CFR 1700.14(a)(10)(ii)'),
(False,'기계적으로 닫힌다는 사실은 CR 시험 성능과 내용약 안정성·상용성을 증명하지 않는다. 포장과 물질 접촉 후 성능도 따져야 한다.','cfr170015','16 CFR 1700.15(a)-(c); Policy 2023-01 I.3,I.5'),
(False,'CR 요청 예외는 광·습기 등 제품 보호 조건을 포괄적으로 면제하지 않는다. 포장은 제품 FDA labeling 및 상용성 조건을 계속 충족해야 한다.','packpolicy','Policy 2023-01 II.3-II.4; 247 CMR 9.08(1)(c)-(d)'),
(True,'다른 약국이 이미 조제한 약을 이 pharmacy reusable planner 경로로 채우는 행위는 명시적으로 금지된다.','ma2479','247 CMR 9.07(1); Policy 2023-01 I.1'),
(False,'60일 supply ceiling은 모든 약의 안정성을60일 보장하지 않는다. FDA labeling과 상용성·container integrity 요구를 함께 만족해야 한다.','packpolicy','Policy 2023-01 I.3,I.5-I.6; II.3-II.4'),
(False,'환자 요청은 planner 사용의 출발 조건이지만 다른 약국의 조제약 사용 금지를 해제하지 않는다.','ma2479','247 CMR 9.07 opening paragraph and (1)'),
(True,'닫힘 소리만으로 CR 및 안정성 검증이 되지 않는다. 1700.15(a)의 실물 접촉·재개폐 성능과 Board integrity/compatibility 조건이 별도로 남는다.','cfr170015','16 CFR 1700.15(a)-(c); Policy 2023-01 I.3,I.5'),
(True,'Non-CR 요청은 포장 안정성 보호까지 포기한다는 뜻이 아니다. 환자가 요청해도 적용 제품·포장 보호조건은 계속 검토한다.','packpolicy','Policy 2023-01 I.3,I.5; II.3-II.4'),
(False,'정확한 약명만으로 상용성·용량·봉인·식별 조건이 모두 충족되지는 않는다. 조문이 각각의 별도 요건을 둔다.','ma2479','247 CMR 9.08(1)(c)-(g),(5)-(6)'),
(True,'Multi-drug-single-dose package에 as-needed 약을 넣는 것은 명시적으로 금지된다. Scheduled 약이 함께 있다는 사정은 예외가 아니다.','ma2479','247 CMR 9.08(3)(c); Policy 2023-01 Multi-Drug item2'),
(False,'포장 supply 최대60일은 처방 수량이나 별도 schedule 한도를 늘리는 새로운 조제권한이 아니다. Packaging 규칙은 적법한 약의 담는 방식에 관한 것이다.','ma2479','247 CMR 9.08(3)(a); 9.01(1)-(2)'),
(False,'60일 상한은 더 짧은 안정성·제조사 expiration을 무시하지 못하며 상업용액 혼합은 prescription에 따른 compounding 조건이 필요하다.','ma2479','247 CMR 9.08(1)(c),(h),(5)(d)'),
(False,'PRN 제외는 maintenance 약과 함께 넣어도 적용된다. 공동 포장이 금지된 PRN을 허용하는 예외를 만들지 않는다.','ma2479','247 CMR 9.08(3)(c)'),
(True,'BUD는60일과 더 짧은 manufacturer expiration·제품 labeling 조건을 지키며 상업용액 둘 이상 혼합은 prescription에 따른 compounding을 요구한다.','ma2479','247 CMR 9.08(1)(c),(h),(5)(d)'),
(True,'상용성·용기 용량·약물 식별·tamper evidence는 각각 명시된 계속 적용 요건이다.','ma2479','247 CMR 9.08(1)(c)-(g),(5)-(6)'),
(True,'포장에60일을 넘게 넣지 못한다는 규정은 별도 처방 수량·기한 제한을 지우는 권한 부여가 아니다.','ma2479','247 CMR 9.08(3)(a); 9.01(1)-(2)'),
(None,'2.4+1.5=3.9g 계산은 맞다. 그러나1314.20(a)는 한 regulated seller의 하루 판매 합계 제한이다. 이전2.4g이 같은 seller의 판매인지 stem이 명시하지 않아 법적 초과 결론에는 추가 사실이 필요하다.','cfr131420','21 CFR 1314.20(a)'),
(False,'Mobile retail vendor의30일7.5g(1314.20(b))과 일반 purchaser30일9g(DEA 설명의21USC844(a)) 등 경로별 범위를 구별한다. 모든 채널에 동일한 한도가 있지 않다.','cfr131420','21 CFR 1314.20(b); DEA CMEA General Information: effective April8 and September30,2006'),
(False,'1314.20(a)는 ephedrine/pseudoephedrine/PPA base를 특정한다. 비활성 성분까지 포함한 정제 총중량은 이 한도의 기준이 아니다.','cfr131420','21 CFR 1314.20(a)'),
(False,'30-day period는 새 달 첫날마다 일괄 초기화하는 calendar month와 다르다. DEA가 설명하는 purchaser30일 제한을 그렇게 바꿀 수 없다.','deacmea','CMEA General Information: restrictions on quantity purchased during30-day period (21USC844(a))'),
(True,'1314.20(a)의 수량은 named base chemical 양이다. Salt 또는 tablet의 총중량과 구분하는 설명은 맞다.','cfr131420','21 CFR 1314.20(a)'),
(False,'3.9g이3.6g 안이라는 서술은 산술적으로 틀리다. 같은 seller가 앞서 판매했다면 거래를 쪼개도 합계 제한을 넘고, 타 seller였다면 새로운 판매자 범위를 별도로 봐야 한다.','cfr131420','21 CFR 1314.20(a)'),
(True,'DEA의 개인 retail purchase 제한은30-day period이다. 단순 calendar-month reset으로 읽지 않는 설명이 맞다. 직접 USC 페이지 조회는 실패했으며 이 명제는 실제 읽은 공식 DEA 설명 범위로 확인했다.','deacmea','CMEA General Information: restrictions on quantity purchased during30-day period (21USC844(a))'),
(False,'60mg single-package 예외는1314.30(a)의 좁은 거래기록 경로다.1314.20의 수량 및1314.25의 접근·인도 조건까지 없애지 않는다.','cfr131430','21 CFR 1314.30(a); 1314.20; 1314.25'),
(False,'각 logbook entry는 작성일부터 최소2년 보존해야 한다. 다음 구매가 보존 종료 시점이 아니다.','cfr131430','21 CFR 1314.30(e)'),
(False,'Pharmacy 면허는1314.35 교육과1314.40 seller self-certification을 대체하지 않는다. 각 사업장에 별도의 준수가 필요하다.','cfr131435','21 CFR 1314.35(a)-(b); 1314.40(a)-(c)'),
(True,'1314.25(b)-(c)는 고객 직접 접근 차단 또는 locked cabinet과 seller의 직접 인도를 요구한다. Case A의 공개 self-service는 그 조건을 충족하지 않는다.','cfr131425','21 CFR 1314.25(b)-(c)'),
(True,'좁은 logbook 예외를 적용해도 다른 수량·접근·판매자 교육·인증 요건을 별도로 충족해야 한다.','cfr131430','21 CFR 1314.30(a); 1314.20; 1314.25; 1314.35-.40'),
(False,'공개 self-service는 sale전 고객 직접 접근을 막아야 한다는 조건과 반대다.','cfr131425','21 CFR 1314.25(b)-(c)'),
(True,'1314.30(e)는 entry 작성일부터 not fewer than two years를 명시한다. 다음 구매일 기준이 아니다.','cfr131430','21 CFR 1314.30(e)'),
(False,'Board advisory는 수량 제한이 없음을 설명하고 사용·폐기 정보 제공을 허용한다. 정보 제공을 새 statutory 수량상한으로 바꾸지 않는다.','syringe','Advisory revised October4,2018: substantive paragraphs1-2 and Recommended Action'),
(False,'Massachusetts §17(c)는 Schedule III-VI의 처방 조제 틀을 둔다. 연방 ScheduleV 분류만으로 모든 제품의 OTC 판매가 허용되는 것은 아니다.','ma17','M.G.L. c.94C §17(c)'),
(True,'실제 Board advisory는 any person of any age에게 처방·신분증 없이 syringe/needle 판매가 가능하다고 명시한다. §27은 판매자 범위를 정한다.','syringe','Advisory revised October4,2018: first substantive paragraph; M.G.L. c.94C §27'),
(False,'기기의 판매 허용은 별개 약물의 prescription 요건을 없애지 않는다. §17(c)와§19의 약물·처방 요건을 별도로 충족해야 한다.','ma17','M.G.L. c.94C §17(c); §19(a)'),
(False,'현재 advisory의 내용은 처방과ID가 필요 없다는 것이다. 둘 다 매번 필수라고 한 주장은 반대다.','syringe','Advisory revised October4,2018: first substantive paragraph'),
(True,'기기 접근과 약물 조제권한은 별개다. 처방약에 필요한 처방 없이 약을 살 권한은 syringe 구매로 생기지 않는다.','ma17','M.G.L. c.94C §17(c); §19(a)'),
(True,'사용·폐기 정보는 advisory상 제공 가능한 안내이며 별도의 새 수량상한이 아니다. advisory는 quantity/type 제한이 없다고 명시한다.','syringe','Advisory revised October4,2018: Recommended Action')
]
assert len(findings)==len(texts),(len(findings),len(texts))
propositions={t:dict(truth=x[0],finding_ko=x[1],source_id=x[2],exact_section=x[3]) for t,x in zip(texts,findings)}
save(B/'independent-proposition-assessments.json',propositions)
# Public NABP copyrighted pages were read only for public format/competency comparison.
# Keep their original payload SHA and our own memo; do not publish the source item text.
style_memos={
'nabpsample':('Public MPJE Sample Questions PDF, one page; format headings and all public sample formats read','공개 PDF는 multiple-choice, multiple-response, ordered-response 형식을 설명한다. 표본은 내용영역 대표가 아니라 형식 친숙화를 위한 것이라고 밝힌다. 본 배정의 Select ONE/ALL 지시는 공개 형식과 양립한다. 공개 문항 wording을 복제하거나 가볍게 바꾼 대응 관계는 발견하지 않았다. 이 자료만으로 높은 reasoning 난도를 주장하지 않는다.'),
'nabpcompetency':('Current MPJE Competency Statements: introductory scope, federal/state note, area headings, March2027 transition','현재 공개 안내는 연방·주 법규를 적용해 상황을 평가하는 지식·판단·능력을 설명한다.2027-03-01 이후에는 새 outline을 사용하게 된다. 보호된 Pre-MPJE 질문이나 링크 목적지는 열지 않았다. 공개 형식과 이 배정의 조제·판매·포장 법률 판단 구조만 비교했다.'),
'nabpformat':('Take the MPJE page: exam format and public resources paragraphs','공개 안내에서2.5시간·120 computer-based selected-response 및 adaptive delivery를 확인했다. 공개 Sample Items 링크 목적지만 방문했고 Pre-MPJE는 방문하지 않았다. 이 정보는 style용이며 Massachusetts 법률 결론의 근거로 사용하지 않았다.')}
private=pathlib.Path('/tmp/phase13-d-nabp-public-source-bytes');private.mkdir(exist_ok=True)
for k,(scope,memo) in style_memos.items():
 for ext in ['raw','txt']:
  src=B/(k+'.'+ext)
  if src.exists():shutil.move(str(src),str(private/src.name))
 save(B/(k+'.read-memo.json'),{'source_id':k,'read_scope':scope,'direct_review_ko':memo,'read_at':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'read_timestamp_meaning':'Review completion recorded after direct source read; not an invented earlier start time','source_payload_retention':'Full public copyrighted payload retained outside Git; SHA in retrieval metadata. Only this reviewer-authored memo is published.','protected_material_accessed':False})
coverage={
'ma2479':'247 CMR 9.01(1)-(3),9.04(7),9.05(1)-(3),9.07(1),9.08(1),(3),(5)-(6)',
'packpolicy':'Policy2023-01 revised1/9/2025: I.1,I.3,I.5-I.6; II.3-II.10; Multi-Drug items1-2',
'ma12d':'M.G.L. c.112 §12D: interchangeable definition, no-substitution, generic interchange framework',
'ma12ee':'M.G.L. c.112 §12EE(a)-(f)',
'ma21c':'M.G.L. c.94C §21C(a)-(d)',
'agdcp':'DCP22-01-112 datedJanuary14,2022: AG definition, substitution and product-verification paragraphs',
'agfda':'Authorized generic NDA vsANDA description; reported list and quarterly update; updatedOctober5,2026',
'purple':'Purple Book introductory description: separately licensed biosimilar and interchangeable products; no product-specific status claim',
'cpscguide':'January2023 guide pp.10,12-15,17: explicit requests, patient blanket scope, prescriber scope, reuse and tamper-evidence comparison',
'cfr17001':'16 CFR1700.1(b)(4)',
'cfr170014':'16 CFR1700.14(a)(1),(10)(i)-(x),(xvii)-(xviii),(16),(20),(25)',
'cfr170015':'16 CFR1700.15(a)-(c)',
'cfr211132':'21 CFR211.132(a)-(b)(1)',
'deacmea':'CMEA General Information: sales limits, purchaser30-day9g, carrier7.5g, effective April8/September30,2006, self-certification/training',
'cfr131420':'21 CFR1314.20(a)-(b)',
'cfr131425':'21 CFR1314.25(a)-(c)',
'cfr131430':'21 CFR1314.30(a),(b),(e)-(h)',
'cfr131435':'21 CFR1314.35(a)-(b)',
'cfr131440':'21 CFR1314.40(a)-(c)',
'syringe':'Board Sale of hypodermic syringes & needles advisory adoptedDecember6,2016/revisedOctober4,2018: all substantive and Recommended Action paragraphs',
'ma27':'M.G.L. c.94C §27 full substantive section',
'ma17':'M.G.L. c.94C §17(a)-(c)',
'ma19':'M.G.L. c.94C §19(a)',
'ma21':'M.G.L. c.94C §21 opening label paragraph',
'ma9':'M.G.L. c.94C §9(a)-(b); retrieved for background, not a sole controlling citation',
'cpscinfo':'Retrieved only; no independent legal proposition credited',
'fdacmea':'Retrieved only; no independent legal proposition credited',
}
sources=[];by_source={}
for mf in sorted(B.glob('*.meta.json')):
 meta=json.load(open(mf));k=meta['source_id'];available=meta.get('document_available',False)
 x=copy.deepcopy(meta);x.update(source_type='PUBLIC_OFFICIAL',law_checked_date='2026-11-04',exact_section=coverage.get(k,style_memos.get(k,('Failed retrieval; no law credit',))[0]),effective_date=None,read_at=datetime.datetime.now(datetime.timezone.utc).isoformat(), read_timestamp_meaning='Review completion recorded after direct substantive section read',metadata_path=(mf.relative_to(R)).as_posix(),metadata_sha256=sha(mf))
 x['coverage']=x['exact_section'];x['authority']=x['exact_section']
 if k in style_memos:
  ep=B/(k+'.read-memo.json');x.update(evidence_path=ep.relative_to(R).as_posix(),evidence_sha256=sha(ep),public_raw_redistribution=False,public_evidence_mode='reviewer-authored memo with original raw/text SHA',used_as_legal_authority=False,version='Public page/PDF retrieved2026-11-04; style only',effective_date_limitation_ko='법규 시행일 자료가 아닌 공개 형식 자료이다.')
 else:
  ep=B/(k+'.txt');raw=B/(k+'.raw');x.update(evidence_path=ep.relative_to(R).as_posix(),evidence_sha256=sha(ep),raw_path=raw.relative_to(R).as_posix(),raw_sha256=sha(raw),used_as_legal_authority=available and k not in ['cpscinfo','fdacmea','ma9'])
  txt=ep.read_text()
  if k=='ma2479':version='Official PDF revision footer12/6/2024'
  elif k=='packpolicy':version='Adopted4/6/2023; revised11/2/2023,1/9/2025'
  elif k=='cpscguide':version='January2023 official CPSC healthcare-professional guide'
  elif k=='agdcp':version='Circular datedJanuary14,2022; page1/19/2022'
  elif k=='syringe':version='AdoptedDecember6,2016; revisedOctober4,2018'
  elif k=='agfda':version='FDA page updatedOctober5,2026'
  elif k.startswith('cfr'):
   import re
   mt=re.search(r'Displaying title[^\n]+',txt);version=mt.group(0) if mt else 'Current eCFR section retrieved2026-11-04'
  elif k.startswith('ma'):version='Live current consolidated Massachusetts General Laws page retrieved2026-11-04'
  elif not available:version='HTTP/error response only, not applicable law'
  else:version='Live official agency page retrieved2026-11-04'
  x.update(version=version,effective_date_limitation_ko='현재 공식 게시본과 명시 버전을 검토했다. 개별 조문 최초 시행·모든 후속 개정 commencement는 별도 입법연혁으로 확정하지 않았다. 과거 거래시점을 가정하지 않으며 이 한계를 현재 게시 원문 확인으로 대체하지 않는다.' if available else '원문을 확보하지 못했다. 해당 실패 payload에 법규 확인 credit을 부여하지 않는다.')
  if k in ['cpscinfo','fdacmea']:x['read_scope']='RETRIEVED_NOT_SUBSTANTIVELY_READ_NOT_USED'
 sources.append(x);by_source[k]=x
# Snapshot actual methodology/profile/schema bytes used by this session.
method_paths=['docs/RELEASE_POLICY.md','docs/AUDIT_WORKFLOW.md','docs/SOURCE_USE_POLICY.md','docs/QUESTION_AUTHORING_STANDARD.md','docs/INDEPENDENT_LEGACY_REVIEW_RUNBOOK.md','data/exam_style/mpje_style_profile.json','data/blueprint.json','schemas/audit.schema.json','schemas/source_manifest.schema.json']
method=[]
for p in method_paths:
 dest=B/'methodology'/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/p,dest);obj=json.load(open(dest)) if p.endswith('.json') else {}
 method.append({'original_path':p,'snapshot_path':dest.relative_to(R).as_posix(),'file_sha256':sha(dest),'content_version':obj.get('content_version'),'semantic_hash':obj.get('content_hash'),'schema_id':obj.get('$id')})
save(B/'source-manifest.json',sources)
family_notes={
'LAB07':('generic-name 처방과 authorized generic의NDA 경로','ANDA 부재·동일 제조사·현재 재고를 혼동하는 상황은 있을 수 있다. 다만 사례B의 답은 승인경로 지식만 회상해도 고를 수 있다.','NDA 사실을 약사가 어떤 제품을 선택·확인할지 결정하는 새 거래로 바꾸고 실제 제품검증에 가까운 오답을 구성한다.'),
'LAB08':('의료응급 no-substitution 예외와 서면 수락','재고 부족과 진짜 medical emergency를 구별하고 기록·서면수락을 확인하는 것은 실무상 가능하다. 하지만 같은 치료계열 모든 약·모든 품절 자동응급 같은 극단 보기가 결정을 지나치게 쉽게 만든다.','응급의 구체적 사실·재고·구매자 수락을 제시하고 허용 여부와 누락된 후속행동 중 실제로 경합하는 선택을 묻는다.'),
'LAB09':('biosimilar의 interchangeability와MA 통지·보존','FDA 승인구분과MA 후속통지·보존은 자연스럽게 연결된다. 다른 주5일 기준도 실제 혼동 대상이다. 그러나 모든 보존규칙 무시나 환자통지 소멸 같은 선택은 과도하다.','실제 substitute 상태·처방자 금지·사용 가능한 통지방식을 제시하고 reasonable-time와 기록방법을 경쟁시키는 보기를 쓴다.'),
'LAB10':('보험 cost-sharing와pharmacy retail price 비교','보험승인액과 법정 청구액 비교는 실제 계산대 결정이다. 무관한 상품가격이나 모든 상품 가격동일 보장은 실질적 경쟁 오답이 아니다.','실제 같은 처방의 두 가격과 보험조건을 주고 청구액·claim처리의 적법한 다음 행동을 묻는다.'),
'PACK01':('tamper evidence·child resistance·OTC 적용범위','두 포장기능과OTC 성분규칙을 혼동할 수 있다. 그러나 진열 선반만으로 규제가 결정되거나 어떤 어린이도 절대 못 연다는 주장은 법규를 몰라도 배제하기 쉽다.','실제 제품 성분·양·제형 및 포장 시험정보를 주고 적용되는 기능과 추가 검증행동을 판단하게 한다.'),
'PACK02':('환자 blanket 요청과처방자 단일처방 요청','환자와처방자의 요청범위 차이는 실무상 중요한 역할·범위 판단이다. 고령자 자동요청·모든 미래처방 자동면제 같은 과장 보기가 단서를 준다.','요청자·요청날짜·구체적 범위·refill 여부를 기록한 사례에서 서로 혼동하기 쉬운 범위 선택을 제시한다.'),
'PACK03':('prednisone105mg package-total 예외','21정과22정의 총량 및 다른 성분 조건은 제품예외 적용이다. 다만 제시된105mg 계산과 절대적 다른예외 부정으로 정답을 추정할 여지가 크다.','다른 규제성분 유무 또는 환자요청을 실제 분기 사실로 주고 단순 곱셈 이외의 포장결정을 묻는다.'),
'PACK04':('제형별nitrate·unit-dose potassium 포장예외','Nitrate 약리계열과특정제형·unit-dose 함량을 구별하는 판단은 적절하다. 그러나 모든 nitrate나임의 재포장에 자동면제라는 과장 보기는 약하다.','구체적 nitrate 제형·강도 또는potassium unit dose·bulk포장을 제시하고 임계조건이 비슷한 대안을 비교한다.'),
'PACK05':('다른약국 조제약의planner 사용과포장성능','다른 약국에서 받은 약을planner로 옮기려는 요청은 현실적이다. 닫힘 소리만으로CR·모든 안정성을 보장한다는 오답은 지나치게 노골적이다.','실제 조제약 출처·환자 요청·용기검사·제품 안정성 자료를 주고 pharmacy packaging 경로에서 가능한 조치를 묻는다.'),
'PACK06':('PRN·60일상한·안정성·액상혼합의compliance packaging','포장 검토 중PRN 포함과짧은 안정성·상업용액 혼합을 함께 검토하는 구조는 가능하다. 이 네 요구는 하나의 packaging workflow에 속한다.','PRN·제품기한·혼합권한을 실제포장 계획에 적용하되 모든 다른조건을 지운다는 극단 오답을 실제 경합 조건으로 바꾼다.'),
'SALE01':('CMEA base 양과seller daily·purchaser30일 한도','수량계산과base 환산은 실제 판매결정이다. 그러나 chemical명이 없고 선구매 판매자가 특정되지 않아 실무 적용범위가 충분히 고정되지 않았다.','Scheduled listed chemical product의성분과동일seller 선구매를 명시하고seller 일일한도와개인30일한도를 구별한다.'),
'SALE02':('CMEA 접근제한·60mg예외·logbook·seller요건','60mg예외를 판매조건 전체로 과잉확대하는 혼동은 현실적이다. 즉시기록폐기·면허만으로전체인증대체 같은 표현은 쉽게 배제된다.','구체적 제품총량·보관형태·직원행위·교육인증상태를 제시하고 좁은예외 이후 남는 의무를 묻는다.'),
'SALE03':('syringe 접근과별도처방약 조제권한','처방·ID 없는syringe판매와그안에넣는약의처방은 다른법적 대상이다. 처분안내가새수량상한을 만든다는 보기 등은 실무적 경쟁성이 약하다.','장치판매 거절사유와별도약물 주문상태를 제시하고각거래에 적용되는 적법한행동을 묻는다.')}
criteria_names=['jurisprudence_reasoning','practice_plausibility','authentic_distractors','wording_not_guessable','reasoning_not_trivia','natural_rule_combination','appropriate_drug_context','distinct_from_bank','not_schedule_flashcard','public_style_without_copying']
# Per-family substantive assessment; each final record additionally binds actual lead-in,
# actual choices, actual nearest items and its own polarity/type. Archive siblings alone
# never cause a failure or inflate distinct-case coverage.
base_criteria={
'LAB07':[False,True,False,False,False,False,True,True,True,True],
'LAB08':[True,True,False,False,True,False,True,True,True,True],
'LAB09':[True,True,True,False,True,True,True,True,True,True],
'LAB10':[True,True,False,False,False,False,True,True,True,True],
'PACK01':[False,True,False,False,False,False,True,True,True,True],
'PACK02':[True,True,True,False,True,True,True,True,True,True],
'PACK03':[True,True,True,False,True,True,True,True,True,True],
'PACK04':[True,True,True,False,True,True,True,True,True,True],
'PACK05':[True,True,False,False,True,False,True,True,True,True],
'PACK06':[True,True,False,False,True,True,True,True,True,True],
'SALE01':[True,True,False,False,False,True,False,True,True,True],
'SALE02':[True,True,True,False,True,True,True,True,True,True],
'SALE03':[True,True,False,False,False,False,True,True,True,True]}
family_by_id={};topic_by_id={};collections={}
pubcfg=json.load(open(R/'site/practice-expansion/publication.json'))
bankpaths=['practice_expansion/2026-10-23/candidates/questions.json']+[a['path'] for a in pubcfg['additional_banks']]
for path in bankpaths:
 for q in json.load(open(R/path))['questions']:
  if q['question_id'] in assignment['question_hashes']:
   qid=q['question_id'];assert digest(q)==assignment['question_hashes'][qid]
   family_by_id[qid]=q.get('family_id');topic_by_id[qid]=q.get('topic');collections[qid]=path
selection_path='practice_expansion/2026-10-28-representative/selection.json'
default_ids=set(json.load(open(R/selection_path))['recommended_ids'])
nearest_by_id={q['question_id']:q for q in nearest['records']}
# Material official-source bindings for each family, beyond the primary choice citation.
family_sources={'LAB07':['ma2479','agdcp','agfda'],'LAB08':['ma2479','ma12d'],'LAB09':['ma12ee','purple','ma21','ma2479'],'LAB10':['ma21c'],'PACK01':['cfr17001','cfr170014','cfr170015','cfr211132','cpscguide'],'PACK02':['cpscguide'],'PACK03':['cfr170014','cpscguide'],'PACK04':['cfr170014'],'PACK05':['ma2479','packpolicy','cfr170015','cpscguide'],'PACK06':['ma2479','packpolicy'],'SALE01':['cfr131420','deacmea'],'SALE02':['cfr131420','cfr131425','cfr131430','cfr131435','cfr131440'],'SALE03':['syringe','ma27','ma17','ma19']}
records=[]
for inp in packet['records']:
 q=inp['original_visible_content'];qid=q['question_id'];family=family_by_id[qid];topic,context,nextstep=family_notes[family]
 incorrect='INCORRECT' in q['stem'];sata=q['question_type']=='SATA';target=q['stem'].split('\n\n')[-1]
 findings_by_choice={}
 for c in q['choices']:
  p=propositions[c['text']];auth=copy.deepcopy(by_source[p['source_id']]);auth['exact_section']=p['exact_section'];auth['authority']=p['exact_section']
  findings_by_choice[c['id']]={'option_text':c['text'],'option_text_sha256':hashlib.sha256(c['text'].encode()).hexdigest(),'statement_true':p['truth'],'support_status':'AMBIGUOUS_UNSTATED_SELLER' if p['truth'] is None else ('SUPPORTED' if p['truth'] else 'REFUTED'),'finding_ko':p['finding_ko'],'selected_under_polarity':None if p['truth'] is None else (not p['truth'] if incorrect else p['truth']),'authorities':[auth],'law_checked_date':'2026-11-04'}
 expected=[i for i,f in findings_by_choice.items() if f['selected_under_polarity'] is True]
 ambiguous=any(f['statement_true'] is None for f in findings_by_choice.values())
 answer='AMBIGUOUS' if ambiguous else ('YES' if sorted(expected)==sorted(q['correct_choice_ids']) else 'NO')
 verdict='HOLD' if ambiguous else ('MINOR_EDIT' if qid in ['MA-EXP-0786','MA-EXP-0787'] else ('KEEP' if answer=='YES' else 'MAJOR_REWRITE'))
 conditional=None
 if ambiguous:conditional={'additional_fact_required':'2.4g was sold earlier today by this same regulated seller; named SLCP base chemical','key_if_additional_fact_true':['A'] if qid=='MA-EXP-0785' else ['C'],'unconditional_unique_key_not_established':True}
 legal_finding=(f'{target}를 기준으로 각 명제의 참/거짓을 독립 산출했다. '+('SATA의 모든 보기 조합을 대조했다. ' if sata else 'INCORRECT 극성을 반전해 단일 오류를 확인했다. ' if incorrect else '옳은 명제의 단일성을 확인했다. '))
 if ambiguous:legal_finding+='3.9g 산술은 맞지만 선구매가 같은seller였다는 사실이 없어1314.20(a)의seller daily 초과를 확정할 수 없다. 저장 키를 무조건 YES로 인증하지 않는다.'
 elif qid in ['MA-EXP-0786','MA-EXP-0787']:legal_finding+='저장 키는 지지된다. 다만 공통 core의 daily-total 설명은 같은seller 판매 합계를 명시하고named base chemical을 제시하도록 보완해야 한다.'
 else:legal_finding+='현재 공식 원문의 적용 범위에서 저장 키와 일치하며 새 법적 사실을 보태지 않았다.'
 vals=base_criteria[family][:]
 if qid=='MA-EXP-0783':vals=[True]*10
 criteria=dict(zip(criteria_names,vals));near=nearest_by_id[qid]
 cand=near['canonical'];pub=near['public'];canonical_q=cand['visible'];pub_q=pub['visible']
 sibling_archived=pub_q['question_id'] not in default_ids
 # Specific wording evidence is the actual maximal/absolute phrase in THIS option set.
 cue_choices=[c for c in q['choices'] if any(t in c['text'].lower() for t in ['every ','all ','any ','always','automatically','guarantee','alone','only','immediately','necessarily','without regard','ignores','removes'])]
 cue='; '.join(c['id']+': '+c['text'] for c in cue_choices[:2]) or '; '.join(c['id']+': '+c['text'] for c in q['choices'][:2])
 reasons={
'jurisprudence_reasoning':f'{qid}의 판단대상은 {topic}이다. '+('역할·조건·법적 결과를 구별해 적용해야 한다.' if criteria['jurisprudence_reasoning'] else '현재 lead-in은 구체적 처분행동보다 정의·승인경로 자체를 회상하는 수준이다.'),
'practice_plausibility':f'{target}에서 다루는 직원의 검토 오류는 일어날 수 있다. {context}',
'authentic_distractors':('0783은 SATA로 네 명제 각각의PRN·기한·혼합·상용성 조건을 평가한다. 전부참이라는 사실만으로 결함으로 취급하지 않는다.' if qid=='MA-EXP-0783' else (f'이 문항의 선택지는 {topic}의 실제 경계 혼동을 포함한다. {context}' if criteria['authentic_distractors'] else f'실제 보기 {cue}는 극단적 일반화 또는무관한 판단이어서 실제 법규 혼동의 경쟁성이 충분하지 않다. {context}')),
'wording_not_guessable':('0783의A-D는 각각 적용조건을 제시하며 일부만 유일하게 상세하거나 반대가 명백한 극단 문장을 두지 않는다. ALL형에서 각명제의 규칙 적용이 필요하다.' if qid=='MA-EXP-0783' else f'현재 문항의 {cue}처럼 절대적·과도한 표현을 배제하면 법규 경계를 충분히 몰라도 답을 좁힐 수 있다. '+('INCORRECT라 단 하나의 과장문구가 특히 단서가 된다.' if incorrect else '정답에만 남겨 둔 제한적 표현이 상대적 단서가 된다.')),
'reasoning_not_trivia':f'{target}는 '+('조건의범위·예외·기산 또는상호제약을 적용하는 결정을 포함한다. '+topic if criteria['reasoning_not_trivia'] else '주어진일반원칙·산술·정의 확인에서 답이 크게 결정되어추가 법적 추론이 충분하지 않다. '+topic),
'natural_rule_combination':f'{qid}: '+('한 거래의'+topic+' 검토에 필요한규칙이 함께 작동한다.' if criteria['natural_rule_combination'] else '두Case를 반복하지만 이lead-in에서는 한Case만 직접묻거나무관한명제가섞여 있어 규칙결합의 필연성이약하다.'),
'appropriate_drug_context':f'{qid}: '+('여기서는'+topic+'의규제경계를묻기때문에 명시된제형·제품종류 또는일반약물맥락이충분하다. 불필요한brand정보를 요구하지 않는다.' if criteria['appropriate_drug_context'] else 'CMEA대상성분명을제시하지않고regulated base chemical이라고만 해 어떤제품에그한도가적용되는지 고정하지 못한다.'),
'distinct_from_bank':f'Canonical439개와public2349개의stem/전보기를project한후tokenJaccard최근접 {canonical_q["question_id"]}({cand["jaccard_token_score"]}), {pub_q["question_id"]}({pub["jaccard_token_score"]})의stem과모든보기를직접읽었다. public최근접은같은두Case를공유하는연습변형이며원learning_boundary가이를공개한다. 배정문항은default가아니고최근접public도'+('archive이다.' if sibling_archived else 'default이다.')+' canonical최근접은별도상황·법적분기이며동일문항재사용으로확정하지않는다. disclosed archive변형만을이유로자동FAIL하지않고새독립casecoverage로도세지않는다.',
'not_schedule_flashcard':f'{qid}는 {topic}을 묻는다. 약물schedule을단독으로암기해답하는flashcard가아니다.',
'public_style_without_copying':f'{qid}의'+('SATA Select ALL' if sata else 'SBA Select ONE')+' 지시와보기형식은실제읽은NABP공개sample의selected-response형식과양립한다. 공개sample/competency/format만확인했고보호된Pre-MPJE·회상·상용문항을열지않았다. 공개sample문장과의복제대응을발견하지않았다.'}
 if qid in ['MA-EXP-0749','MA-EXP-0750','MA-EXP-0752','MA-EXP-0753','MA-EXP-0757','MA-EXP-0785']:
  criteria['distinct_from_bank']=False
  reasons['distinct_from_bank']=f'직접 읽은 canonical최근접 {canonical_q["question_id"]}는 '+('동일한 medical-emergency 대체 및 기록·수락 법적 분기를 이미 다룬다.' if family=='LAB08' else 'biosimilar 승인과interchangeability의 동일한 구분을 이미 적용한다.' if family=='LAB09' else '동일처방 cost-share와retail price 중 작은 금액을 고르는 동일한 법적 결정을 이미 다룬다.' if family=='LAB10' else '동일한3.6g seller daily limit 초과를 수량만 다르게 적용한다.')+' '+f'현재 {qid}의 추가Case 또는 숫자 변경만으로 그 판단과 충분히 구별되지 않는다. public최근접 '+pub_q['question_id']+'의 공개된archive변형이라는 사실 자체를 실패이유로 삼지는 않았다. 실제 canonical/public stem과전보기를 비교한 의미적 판단이다.'
 realism_verdict='PASS' if all(criteria.values()) else 'FAIL'
 original=q['explanation']
 explanation_ko=('core의2.4+1.5 계산은맞지만seller범위와성분명이누락됐다. patient30일규칙과seller하루규칙의주체를명시해야한다.' if family=='SALE01' else f'core전체를읽고 {topic}의적용경계를공식원문과대조했다. 확인한범위에서key를뒤집는해설오류는발견하지않았다.')
 explanation_review={'complete_original_explanation_read':True,'original_explanation_sha256':digest(original),'core_reasoning':{'read':True,'text_sha256':hashlib.sha256(original['core_reasoning'].encode()).hexdigest(),'finding_ko':explanation_ko},'choice_analysis':{c['id']:{'read':True,'text_sha256':hashlib.sha256(original['choice_analysis'][c['id']].encode()).hexdigest(),'finding_ko':findings_by_choice[c['id']]['finding_ko'],'assessment':'SCOPE_CORRECTION_REQUIRED' if family=='SALE01' else 'CONSISTENT_WITH_INDEPENDENT_FINDING'} for c in q['choices']},'learning_boundary':{'read':True,'text_sha256':hashlib.sha256(original.get('learning_boundary','').encode()).hexdigest(),'finding_ko':'같은family네변형이같은두Case와네판단을공유한다는범위를읽었다. 독립네case로세지않으며archive변형존재만으로현실성을자동실패시키지않았다.'}}
 record={'question_id':qid,'record_sha256':inp['record_sha256'],'family_id':family,'topic':topic_by_id[qid],'collection':collections[qid],'read_scope':{'original_stem':True,'all_choice_ids':[c['id'] for c in q['choices']],'stored_key':True,'complete_korean_core_and_all_choice_rationales':True,'learning_boundary':True,'visible_content_sha256':inp['visible_content_sha256'],'input_path':P+'/assigned-visible-input.json','input_file_sha256':sha(B/'assigned-visible-input.json'),'read_completion_recorded_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'hidden_author_truth_read':False,'prior_verdict_exposure_count':0},'legal_review':{'existing_answer_correct':answer,'stored_key':q['correct_choice_ids'],'independently_expected_key':None if ambiguous else expected,'conditional_key_analysis':conditional,'polarity':'SELECT_INCORRECT' if incorrect else 'SELECT_ALL_TRUE' if sata else 'SELECT_ONE_TRUE','choice_by_choice_findings':findings_by_choice,'authorities':[copy.deepcopy(by_source[k]) for k in family_sources[family]],'verdict':verdict,'finding_ko':legal_finding,'blocker':('동일seller선구매및namedCMEA성분이명시되지않아일일한도초과와단일key를확정하지못함.' if ambiguous else None),'correction_required_ko':('동일seller선구매사실과ephedrine/pseudoephedrine/PPA중해당base를명시하고key·해설을재검증한다.' if family=='SALE01' else None),'original_explanation_review':explanation_review},'realism_review':{'verdict':realism_verdict,'decision':'KEEP' if realism_verdict=='PASS' else 'MAJOR_REWRITE','criteria':criteria,'criterion_findings_ko':reasons,'finding_ko':('구체적포장계획의네개요건을함께검토하며공개형식·법적추론·실무맥락을충족한다.' if realism_verdict=='PASS' else context+' '+nextstep),'duplicate_review':{'status':'DIRECT_VISIBLE_COMPARISON_COMPLETED','method':'Token Jaccard candidate search followed by direct full stem/all choices reading; no score-derived semantic verdict','evidence_path':P+'/nearest-visible.json','evidence_sha256':sha(B/'nearest-visible.json'),'canonical_candidate_id':canonical_q['question_id'],'public_candidate_id':pub_q['question_id'],'canonical_candidate_visible_sha256':cand['visible_sha256'],'public_candidate_visible_sha256':pub['visible_sha256'],'assigned_is_default':qid in default_ids,'public_candidate_is_default':pub_q['question_id'] in default_ids,'selection_path':selection_path,'selection_sha256':sha(R/selection_path),'semantic_finding_ko':reasons['distinct_from_bank']}},'safe_hold_recommended':verdict!='KEEP' or realism_verdict!='PASS','release_eligible':False,'required_next_action_ko':('선구매seller·CMEA성분누락을먼저해소하고currenthash에대해fresh재감사한다. '+nextstep if family=='SALE01' else '법규key는유지가능하나현실성보기를편집후새hash로감사한다. '+nextstep if realism_verdict=='FAIL' else '현재독립legacy평가를root가순차통합한다. canonicalaudit·adjudication·releasegate는별도이며이보고서만으로release하지않는다.')}
 records.append(record)
profile=json.load(open(R/'data/exam_style/mpje_style_profile.json'))
report={'schema_version':'independent-legacy-review/phase13-d-v1','stage':'independent-legacy','job_id':assignment['job_id'],'independent_of_authors':True,'auditor':'GPT','auditor_instance':'GPT:/root/independent_wave13_d:20261104','actor_provenance':{'actor_id':'/root/independent_wave13_d','session_id':'/root/independent_wave13_d'},'actual_session_independence':{'fresh_session':True,'author_or_editor_of_assigned_content':False,'prior_verdict_exposure_count':0,'hidden_truth_exposure_count':0,'session_identity_not_relabelled':True},'canonical_audit':False,'canonical_release_credit':0,'author_review_credit':0,'release_eligible':False,'reviewed_at':'2026-11-04','review_completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'question_hashes':assignment['question_hashes'],'style_profile':{'profile_id':profile['profile_id'],'content_version':profile['content_version'],'semantic_hash':profile['content_hash'],'file_sha256':sha(R/'data/exam_style/mpje_style_profile.json')},'methodology_and_schema_snapshots':method,'source_policy':{'protected_or_recalled_content_used':False,'commercial_question_material_used':False,'public_official_sources_only_for_legal_findings':True,'nabp_used_for_style_only':True,'prior_reports_or_ledger_conclusions_read':False,'raw_usc_failures_not_counted_as_law_verification':True},'limitations_ko':['USCodeHouse의21USC844/15USC1473시도는404,govinfo2025시도는HTTP200error페이지였다.실패를법규원문확인으로세지않았다.30일개인한도는실제로읽은공식DEA설명,환자요청범위는실제로읽은CPSC공식guide에한정해확인했다.','공식현재게시본의시행범위를평가했으나모든개정의별도commencement입법연혁을확정하지않았다.각source에버전·실제검토일·이한계를기록했다.','Canonical439개/public2349개를visible필드만비교하고실제최근접원문을읽었다.token점수는후보발견용이며semantic판정을자동화하지않았다.','공개NABPsample원문은직접읽었지만저작권raw/text를publicGit에복제하지않았다.원payloadSHA·retrievalmetadata및자체작성stylememo를보존했다.'], 'sources':sources,'records':records,'summary':{'assigned_count':len(records),'all_original_visible_records_read':True,'legal_existing_answer_correct':{k:sum(r['legal_review']['existing_answer_correct']==k for r in records) for k in ['YES','NO','AMBIGUOUS','NOT_ASSESSED']},'legal_verdicts':{k:sum(r['legal_review']['verdict']==k for r in records) for k in ['KEEP','MINOR_EDIT','MAJOR_REWRITE','HOLD','DELETE']},'realism_verdicts':{k:sum(r['realism_review']['verdict']==k for r in records) for k in ['PASS','FAIL','NOT_ASSESSED']},'canonical_release_credit':0}}
save(R/'reports/full-corpus-review/independent-phase13-d-review.json',report)
print(json.dumps(report['summary'],ensure_ascii=False))
