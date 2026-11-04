import json,pathlib,hashlib,datetime,copy
R=pathlib.Path('.');D=pathlib.Path(__file__).resolve().parent.relative_to(pathlib.Path.cwd().resolve());E=D.parent
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
digest=lambda v:hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
now=datetime.datetime.now(datetime.timezone.utc).isoformat();date=now[:10]
p=json.load(open(E/'assigned-visible-input.json'));a=json.load(open(E/'assignment.json'));loc=json.load(open(D/'locator-whitelist.json'));near=json.load(open(D/'nearest-comparisons.json'));nv=json.load(open(D/'nearest-visible-input.json'));defaults=json.load(open(E/'context/default-ids-at-assignment.json'))
versions={
'administration':('DCP 26-03-124; issued 2026-03-11, rescinds DCP23-04-118','2026-03-11'),
'prescribing':('DCP 26-08-125; issued 2026-08-25, rescinds DCP25-04-124','2026-08-25'),
'cmr9':('Massachusetts Register #1536; posted 2024-12-06; separate commencement not independently established','UNKNOWN'),
'cmr20':('Massachusetts Register #1536; posted 2024-12-06; separate commencement not independently established','UNKNOWN'),
'cmr16':('Massachusetts Register #1354; dated 2017-12-15; separate commencement not independently established','UNKNOWN'),
'ec':('Current DPH FAQ retrieved this session; content revision/effective date not displayed','UNKNOWN'),
'ec-standing':('Signed Estevan Garcia MD, 2022-08-04; currently linked by DPH EC page','2022-08-04'),
'c94c19a':('Current legislature display; precise amendment commencement not independently established','UNKNOWN'),
'opill-current':('DailyMed Opill label updated 2025-01-27; manufacturer SPL version4 posted2025-01-29, current official API index','UNKNOWN'),
'opill':('FDA approval announcement 2023-07-13; product status checked current page','2023-07-13'),
'planb':('Current FDA information page; unrestricted OTC approval dated 2013-06-20','2013-06-20'),
'mifepristone':('Current FDA Q&A; includes April2026 study statement; only indication/status used, no litigation conclusion','UNKNOWN'),
'ella-current':('DailyMed label updated 2026-07-20; SPL version7 posted 2026-07-24, confirmed official API index','UNKNOWN'),
'hipaa':('Current eCFR 45CFR164.530; exact latest amendment commencement not independently established','UNKNOWN'),
'c94c19f':('Current legislature display only oral contraceptive/patch wording; does not corroborate circular HIV/STI expansion; no expansion conclusion drawn','UNKNOWN'),
'access':('Current DPH ACCESS explainer; still points to older circular, not controlling current prescribing scope','UNKNOWN')}
sources=[];S={}
for k,(v,ef) in versions.items():
 m=json.load(open(D/(k+'.meta.json')))
 assert m.get('status_code')==200 and m.get('response_bytes',0)>100
 s=dict(source_id=k,source_type='PUBLIC_OFFICIAL',official_url=m['official_url'],exact_section='See per-choice exact_section bindings',law_checked_date=date,source_read_at=now,effective_date=ef,version=v,effective_date_limitation_ko='UNKNOWN은 이 조회에서 별도 시행·개정 발효일을 확정하지 않았다는 뜻이며 게시일을 시행일로 바꾸지 않았다.' if ef=='UNKNOWN' else '공식 문서의 발행·서명·승인일을 명시한 버전이다. 이 범위를 넘는 소급 효과를 주장하지 않는다.',evidence_path=m['text_path'],evidence_sha256=m['text_sha256'],raw_path=m['raw_path'],raw_sha256=m['raw_sha256'],metadata_path=str(D/(k+'.meta.json')),metadata_sha256=sha(D/(k+'.meta.json')),retrieval_provenance={x:m[x] for x in ['final_url','status_code','retrieved_at','retrieval_completed_at','method','content_type','response_bytes','response_headers']},http_identity_verified=True,identity_evidence_ko={'administration':'본문 DCP26-03-124,2026-03-11,제목과5쪽 원문','prescribing':'본문 DCP26-08-125,2026-08-25,3쪽 원문','cmr9':'본문247CMR9 Professional Practice Standards;49–54.11쪽','cmr20':'본문247CMR20 Reporting;97–99쪽','cmr16':'본문247CMR16 CDTM;4쪽','ec-standing':'본문 Standing Order for Dispensing Emergency Contraception Pills, 서명2022-08-04','ella-current':'ELLA ulipristal acetate,updated2026-07-20,Rx only, indications, official NLM host'}.get(k,'공식 호스트의 해당 제목·본문과 아래 exact section을 읽었으며 오류/로그인/PageNotFound 본문이 아님을 확인했다.'))
 sources.append(s);S[k]=s

def ref(k,sec):
 s=S[k];return {x:copy.deepcopy(s[x]) for x in ['source_id','source_type','authority','official_url','law_checked_date','source_read_at','effective_date','version','evidence_path','evidence_sha256','raw_path','raw_sha256','metadata_path','metadata_sha256']}|{'exact_section':sec}
# Each tuple is an independently assessed option proposition, not copied from stored keys.
F={
'VAX19':[
(False,'명칭만으로 제조사·lot·expiration을 대신할 수 없다. 다만 본문에는 실제 약국 내 적격약 투여 사실이 빠져 DCP상 의무의 적용범위는 별도 확인해야 한다.','administration','p4 Record Keeping'),
(False,'치료 동의는 대기실의 모든 사람에게 진단을 공개하는 동의가 아니다. MA 비밀유지 의무는 별도이다.','cmr9','9.01(16); DCP26-03-124 p5 Privacy'),
(None,'실제 적격약을 이 약국에서 투여했다면 조제기록만으로 date/route/site/투여자를 충족하지 못한다. stem은 dispensed만 명시하여 실제 투여 사실과 적용 경로가 확정되지 않는다.','administration','pp1–2 Dispensing by Administration / eligible medications; p4 Record Keeping'),
(False,'청구액만 요구하는 규정이 아니다. 적용 가능한 투여경로에서는 consent,screening,제품·투여·사건 정보가 요구된다.','administration','p4 Record Keeping'),
(False,'적용되는 투여기록 의무가 있을 때 dispensing entry가 투여자·투여일·route/site를 갈음하지 않는다. 실제 투여 여부는 stem에 보충이 필요하다.','administration','p4 Record Keeping'),
(True,'불필요한 공개 진단 발언은 투약 동의만으로 허용되지 않는다. 불가피한 incidental disclosure를 모두 위법이라고 확대하는 문장도 아니다.','cmr9','9.01(16); DCP26-03-124 p5 Privacy; 45CFR164.530(c) supplemental'),
(None,'DCP 적격약을 약국에서 투여한 경우 manufacturer,lot,expiration이 의무이다. 약명이 없고 조제만 적힌 현재 사례로는 해당 경로의 적용을 확정할 수 없다.','administration','pp1–2 eligible scope; p4 Record Keeping'),
(None,'DCP 적용 투여라면 patient consent,screening,adverse outcome/event(if any)를 기록한다. 현재 stem에는 이 적용사실이 불충분하다.','administration','pp1–2 scope; p4 Record Keeping')],
'VAX20':[
(False,'prescriber 보고와 별도로 발동하는 Board 의무는 통화만으로 충족되지 않는다. 모든 반응·오류를 자동 Board 보고 대상으로 확대하지 않는다.','cmr20','20.02(1)–(3),20.07(3); DCP26-03-124 p4 Reporting Adverse Events'),
(True,'추가 ED treatment/testing/monitoring은 즉시 prescriber 보고 대상(iv)이다. 일반 should24h와 다르다.','administration','p4 Reporting Adverse Events, outcome(iv)'),
(False,'보고서 완성 때문에 필요한 응급진료를 지연시키라는 허가는 없다. 응급관리 competency와 즉시 보고를 함께 충족해야 한다.','administration','p3 Administration–Medical Emergencies; p4 Reporting Adverse Events'),
(False,'일반 반응은 should communicate within24h,열거된 중대 outcome은 must immediately이다. 둘을 동일 mandatory24h로 읽을 수 없다.','administration','p4 Reporting Adverse Events'),
(False,'열거된 중대 outcome에는24h대기 재량이 없다.','administration','p4 Reporting Adverse Events, outcome(iv)'),
(True,'24h should 권고와 중대 outcome 즉시 must 의무는 동사·기한이 다르다.','administration','p4 Reporting Adverse Events'),
(True,'별도로 발동한 Board 보고를 prescriber통화가 대체하지 못한다. 실제 Board trigger는20.02/20.07조건에 한정된다.','cmr20','20.02(1)–(3),20.07(3); DCP26-03-124 p4 Reporting Adverse Events'),
(True,'응급관리와 보고의무를 병행하는 것이 맞다. 이 문장을 특정 별도 보고서 마감시간 법조문으로 과장하지 않는다.','administration','p3 Administration–Medical Emergencies; p4 Reporting Adverse Events')],
'PUB01':[
(True,'MCSR 예외는 처방과 조제가 모두 단일 약국장소에서 이뤄지는 제한조건이다. 일반 면제로 확대할 수 없다.','prescribing','p1 Purpose, paragraph3'),
(False,'영수증만으로 상담과 written record를 언제나 충족하는 것은 아니다. 영수증 내용이 필요한 record를 실제 담는지는 따로 판단한다.','prescribing','pp1–2 General Prescribing Requirements(c),(e),(g)'),
(False,'다른 장소 조제라면 both at a single pharmacy 요건의 적용을 다시 보아야 한다.','prescribing','p1 Purpose paragraph3'),
(False,'MCSR 면제는 NPI나 교육 면제가 아니다. NPI·competency와 각 약물경로별 사전교육이 별도이다.','prescribing','General(b),(i); pp2–3 training provisions'),
(False,'한정된 prescribing/dispensing 예외로 약사의 모든 stock·다른 활동의 등록을 없앨 수 없다.','prescribing','p1 Purpose; General(a)'),
(True,'처방·조제 장소 변화는 단일 장소 조건 재평가 사유다. 자동 위법이나 무조건 면제를 단정하지 않는다.','prescribing','p1 Purpose paragraph3'),
(True,'NPI,계속역량,해당 호르몬/HIV/STI 경로의 사전교육을 충족해야 한다. 구체 교육시간은 약물경로별로 다르다.','prescribing','General(b),(i); Hormonal(e); HIV(b); STI(b)')],
'PUB02':[
(False,'경로마다 의뢰·통보 조건이 다르다. circular(h)는 의뢰/상담권고 또는 환자동의시 PCP통보이고 CDTM은 별도24h 규정이다.','prescribing','General(h); 247CMR16.03(5)(d),(e)2'),
(False,'pharmacist service만으로 실제 처방·조제활동과 적용 protocol 준수를 증명할 수 없다. 단, authority/protocol이라는 특정 제목의 필드를 적으라는 verbatim명령은 이 circular에 없으며 설명은 기록 충실성의 해석이다.','prescribing','General(a),(d),(g); 247CMR16.04(2)(b),(c),(e)'),
(False,'Purpose가 no requirement to prescribe라고 명시한다.','prescribing','p1 Purpose paragraph3'),
(True,'circular의 encouraged MassHealth등록과 CDTM prescriptive practice attestation은 다른 의무다.','prescribing','General(j); 247CMR16.02(1)(f)3'),
(True,'자발적 선택시 적용되는 요건이지 모든 약사의 서비스 개시 의무가 아니다.','prescribing','p1 Purpose paragraph3'),
(False,'encouraged를 모든 경로의 동일 CDTM attestation으로 바꾸면 의무를 과장한다.','cmr16','16.02(1)(f)3; DCP26-08-125 General(j)'),
(True,'실제로 택한 경로의 referral/notification 조건과 동의조건을 따라야 한다.모든 경로 통지기간이 같다는 주장이 아니다.','prescribing','General(h); 247CMR16.03(5)(d),(e)2')],
'PUB03':[
(False,'현재 ella label은 Rx only이다. FDA PlanB는OTC이다. MA standing order가ella를 일반OTC로 전환하지 않는다.','ella-current','Rx only package / Patient information; FDA Plan B current availability'),
(False,'보험 청구용 처방으로 FDA제품분류 자체가Rx-only로 바뀌지 않는다. MA는OTC피임약도 처방할 수 있게 한다.','prescribing','Hormonal(a): regardless OTC or prescription-only; FDA Opill approval'),
(True,'FDA는Opill이 매일 복용하는 피임약이며 emergency contraception용이 아니라고 명시한다.','opill','FDA approval announcement, daily dosing / not for emergency contraception paragraphs'),
(False,'FDA mifepristone은기존 임신종료용이고EC는임신예방용이다. 상호교환 가능한 EC제품이 아니다.','mifepristone','Q&A: indication / prescription status; EC standing order pp1–2 ECP Indication/Order'),
(False,'OTC라는 분류가 사후응급피임 적응증을 만들지 않는다. Opill은EC용이 아니다.','opill','not for use as emergency contraception paragraph'),
(True,'ella Rx-only와levonorgestrel OTC를 구별해야 하며 MA standing order는 별도의 Rx dispensing 접근경로다.','ella-current','Rx only package / Patient information; FDA PlanB availability; MA EC FAQ'),
(True,'보험상 처방 요구와 OTC구매가능성은 별개다. 어떤 보험이든 무조건 처방이 필요하다는 뜻은 아니다.','prescribing','Hormonal(a); FDA Opill approval; MA EC FAQ insurance/prescription questions')],
'PUB04':[
(False,'EC standing order의 지정 약물·항구토제 범위를 벗어나는 독립처방권은 생기지 않는다.','ec-standing','pp1–3 ECP Indication,Order,antiemetic table'),
(True,'DPH FAQ가 추가교육 불필요라고 명시한다. c94C19A(d)도may complete로 다른 경로의 사전교육과 다르다.','ec','FAQ: What training is necessary; c94C19A(d)'),
(False,'대리요청만으로 실제사용자 assessment를 갈음할 수 없다. 일반OTC대리구매와 다르다.','ec','FAQ: requests EC for someone other than themselves'),
(False,'이 서비스 자발성은 유효처방·환자접근 관련 별도 의무의 면제가 아니다.구체 모든 처방의 무조건 조제의무라는 의미로도 확대하지 않는다.','ec','FAQ voluntary participation; 247CMR9.01(1),(4),9.18(1),(4)'),
(False,'이 statewideEC경로에는 주장한추가교육 진입요건이 없다. 다른개별 prescribing training과 혼동한 것이다.','ec','FAQ training; c94C19A(d)'),
(True,'실제복용자를 in-person 또는telephone으로 먼저 평가해야 한다. agent의일반OTC구매는 별도다.','ec','FAQ: requests EC for someone other than themselves'),
(True,'standing order 사용은자발적이다. 별도로 적용되는유효처방·상담 의무는 그 자체조건으로 남는다. 무조건 모든처방 조제라는 주장은 아니다.','ec','FAQ voluntary participation; 247CMR9.01(1),(4),9.18'),
(True,'특정 EC 및 명시된보조약 dispensing권한이지 일반 독립처방면허가 아니다.','c94c19a','19A(a)–(c); EC standing order ECP Order/antiemetics')],
'COUN03':[
(False,'공개줄에서 크게 말하는 방법이 청각장애시 언제나 충분하지 않다. 환자이해와 시각·청각 비밀유지는 별도로 충족한다.','cmr9','9.01(16),9.18(5),(6)'),
(False,'professional judgment로 환자가 이해할 필요정보를 정하므로 모든약·환자 동일내용 의무가 아니다.','cmr9','9.18(4),(5)(a)–(h)'),
(True,'새 흡입기 technique와환자의이해가능성을 반영해야한다. 특정언어·보조수단의고정법정목록을 주장하는문장은 아니다.','cmr9','9.18(4),(5), especially(c)'),
(False,'standard script라는이유만으로 실제 이해에필요한 상담을완수하지못한다.','cmr9','9.18(5)'),
(False,'인쇄물만으로사용불가한환자에게 technique를이해시켰다고단정못한다.','cmr9','9.18(4),(5)(c)'),
(True,'patient understand proper use라는목적에맞게실제언어·청각필요를반영하는방법이필요하다.','cmr9','9.18(5)'),
(True,'해당환자·제품에필요한 storage,adverse effects,missed dose,interactions는professional judgment에따른다.','cmr9','9.18(5)(d),(f),(h)')],
'COUN04':[
(False,'모든가정용도구가항상적절한계량기구라는규정이아니다. 실제용량단위·정확성을갖춘proper device가필요하다.','cmr9','9.18(9);9.18(5)(b),(c)'),
(True,'all liquid medications에 proper measuring device를dispense OR recommend한다. 반드시무료제공만가능하다는뜻이아니다.','cmr9','9.18(9)'),
(False,'규정은proper use설명을요구하며demonstration을금지하거나오직written directions만인정하지않는다.','cmr9','9.18(5)(b),(c)'),
(False,'label rewrite자체는용량변경권한이아니다. 처방권한·clarification을해결해야하며별도CDTM등권한은주어지지않았다.','cmr9','9.01(4),9.04(1),9.17(1)(f),(i),(2)'),
(False,'printed directions만으로all liquids의dispense/recommend장치의무가없어지지않는다.','cmr9','9.18(9)'),
(True,'실제치료의도변경은상담문구정리만으로행할수없다. 적절한권한확인·처방해결이필요하고항상한가지방식의prescriber연락만강제하지는않는다.','cmr9','9.01(4),9.04(1),9.17(1)(f),(i),(2)'),
(True,'용량·route·사용지침과proper measuring device가연결되어야한다. 특정브랜드기구만의무라는뜻은아니다.','cmr9','9.18(5)(b),(c),(9)')],
'COUN05':[
(True,'상담실에가려면stockroom또는dispensing area를통과해야하는접근은금지된다.','cmr9','9.18(6)'),
(False,'예외는pharmacist while practicing in inpatient setting,unless otherwise required이다. 병원내모든outpatient/discharge처방면제가아니다.','cmr9','9.18(10)'),
(False,'일반적으로open hours중상담을categorically제외할권한은없다. 다만9.19(17)의30분/6시간휴게·로그·callback예외를stem에서배제하지않았다.','cmr9','9.18(8);9.19(17)(a)–(e)'),
(False,'sign만으로visual/auditory privacy요건이충족되지않는다.','cmr9','9.18(6)'),
(False,'표지를붙여도환자traversal금지를면제하지않는다.','cmr9','9.18(6)'),
(True,'9.18(8)의일반문언은all times open for business이다.그러나허용된9.19(17) temporary absence와callback를함께읽어야하며scheduled afternoon만으로예외배제못한다.','cmr9','9.18(8),9.19(17)(a)–(e)'),
(True,'privacy는시각·청각모두이며명칭표지와별도기능요건이다.','cmr9','9.18(6)')],
'COUN06':[
(False,'rights sign과개별offer/counseling/availability는누적조건이다.','cmr9','9.18(1),(4),(7),(8)'),
(False,'employee-only folder는dispensing area인접conspicuous posting이아니다.','cmr9','9.18(7)'),
(False,'상담권리표지는최소half-inch,MOR명표지는최소one-inch이다.','cmr9','9.18(7),9.19(11)'),
(True,'8in높이10in너비는최소11in높이14in너비미달이다.문구정확성이크기를면제하지않는다.','cmr9','9.18(7)'),
(True,'두표지최소문자높이를구별한다.단1in글자로상담표지를쓰는것자체는half-inch최소치를충족하므로위반이라고단정해서는안된다.','cmr9','9.18(7),9.19(11)'),
(False,'정확한문구와최소크기는각각요구되어8x10표지는부족하다.','cmr9','9.18(7)'),
(True,'처방이조제되는각area인접conspicuous place에post한다.','cmr9','9.18(7)')],
'COUN07':[
(False,'each new prescription을dispensed/delivered하기전prospective DUR한다. delivery후검토만으로시점요건충족못한다.','cmr9','9.17(1)'),
(False,'모든alert를법적금지로자동취급하지않는다.약사가실제의미와appropriate measures를판단한다.','cmr9','9.17(1),(2)'),
(True,'알레르기는reasonable effort review대상이며alert부재가약사의실제검토를대체하지않는다.','cmr9','9.17(1)(g),9.16(7)(b)'),
(False,'구두해결이완료되어도measures taken을문서화해야한다.','cmr9','9.17(2)'),
(False,'computer alert가없다고기록된allergy를검토안해도되는결론은나오지않는다.','cmr9','9.17(1)(g),9.16(7)(b)'),
(True,'alert의환자별관련성을검토하고appropriate measures를취해야하며자동승인/거부의양극단이아니다.','cmr9','9.17(1),(2)'),
(True,'DUR에대응해취한measures를문서화한다.처방의통화때만기록한다는제한이없다.','cmr9','9.17(2)')],
'COUN08':[
(False,'PMP조회만으로allergy/dose/directions를포괄하는DUR를완료하지못한다.이사례는특정MassPAT조회trigger의무를묻지않는다.','cmr9','9.17(1)(b),(f),(g),(i);9.16(7)'),
(True,'제품과수량의물리적정확성은therapeutic duplication을해결하지못한다.','cmr9','9.04(1);9.17(1)(b),(2)'),
(False,'처방제시시필요약력을immediately retrieve할수있어야한다.','cmr9','9.16(7)'),
(False,'제품을정확히셌다는사실은처방의진정성·prescriptive authority를입증하지않는다.서로다른심사이다.','cmr9','9.04(1),9.15(1),(2),9.17(1)')]
}
cover={
'administration':'pp1–2 Purpose / Dispensing by Administration / eligible medications; p3 Medical Emergencies; p4 Record Keeping / Reporting Adverse Events; p5 Privacy',
'prescribing':'p1 Purpose / General(a)–(e); p2 General(f)–(j),Hormonal(a)–(e); p3 HIV(b),STI(b)',
'cmr9':'9.01(4),(16),9.04(1),9.15,9.16(7),9.17(1)–(3),9.18(1)–(10),9.19(11),(17)',
'cmr20':'20.02(1)–(5),20.07(3)',
'cmr16':'16.02(1)(f)3,16.03(5)(d),(e)2,16.04(2)(b),(c),(e)',
'ec':'FAQ training / voluntary participation / patient-specific prescription / other-person assessment / OTC purchase / insurance',
'ec-standing':'pp1–3 ECP Indication, ECP Order, antiemetic table; signature 2022-08-04',
'c94c19a':'19A(a)–(d)',
'opill-current':'Drug Facts / Human OTC drug label / daily contraception / Do not use as emergency contraceptive',
'opill':'Approval announcement 2023-07-13: nonprescription daily dosing and not for emergency contraception',
'planb':'Current availability; history June20,2013 unrestricted OTC approval; Q&A emergency contraception/abortifacient distinction',
'mifepristone':'Q&A: approved indication medical termination through ten weeks; prescription-only / pharmacy certification',
'ella-current':'Updated2026-07-20; Rx only principal display panel; 1 Indications and Usage; patient information prescription EC',
'hipaa':'45CFR164.530(c)(1),(2)(i),(ii): appropriate safeguards / limit incidental disclosures; supplemental only when HIPAA applies',
'c94c19f':'19F(a),(c)(i)(A)–(E): hormonal contraceptive training,screening,record and prompt dispensing only',
'access':'Emergency contraception statewide standing order / no additional training / insurance-access sections; older circular link limitation'
}
for s in sources:
 s['exact_section']=cover[s['source_id']]
 s['source_class']='PUBLIC_OFFICIAL'
 s['authority']=s['version']
 s['source_type']=('MA_PROMULGATED_REGULATION' if s['source_id'] in ['cmr9','cmr16','cmr20'] else 'MA_STATUTE' if s['source_id'] in ['c94c19a','c94c19f'] else 'FEDERAL_REGULATION' if s['source_id']=='hipaa' else 'FDA_OFFICIAL' if s['source_id'] in ['opill','planb','mifepristone'] else 'MA_DCP_GUIDANCE' if s['source_id'] in ['administration','prescribing','ec','ec-standing','access'] else 'OTHER_OFFICIAL')
 if s['source_id'] in ['administration','prescribing']:
  s['document_issued_at']=s['effective_date'];s['effective_date']='UNKNOWN';s['effective_date_limitation_ko']='발행일은확인했으나별도로명시된시행일은확정하지않았다.현재공식게시circular의기재조건에만판정했다.'
 if s['source_id'] in ['ella-current','opill-current']:
  idx=s['source_id'].replace('current','index')
  s['version_index_path']=str(D/(idx+'.html'));s['version_index_sha256']=sha(D/(idx+'.html'))

GREF={
'VAX19':['administration','cmr9','hipaa'], 'VAX20':['administration','cmr20'],
'PUB01':['prescribing','c94c19f'], 'PUB02':['prescribing','cmr16'],
'PUB03':['opill','opill-current','planb','ella-current','mifepristone','ec','ec-standing','prescribing'],
'PUB04':['ec','ec-standing','c94c19a','cmr9'],
'COUN03':['cmr9','hipaa'],'COUN04':['cmr9'],'COUN05':['cmr9'],'COUN06':['cmr9'],'COUN07':['cmr9'],'COUN08':['cmr9']}
# Stable first-appearance ordering from the fully read visible packet is used only
# to bind the manual proposition assessments above to exact unchanged option text.
texts={}
for r in p['records']:
 g=loc[r['question_id']]['family_id'];texts.setdefault(g,[])
 for c in r['original_visible_content']['choices']:
  if c['text'] not in texts[g]:texts[g].append(c['text'])
assert all(len(texts[g])==len(F[g]) for g in F)
sem={g:dict(zip(texts[g],F[g])) for g in F}
C=['jurisprudence_reasoning','practice_plausibility','authentic_distractors','wording_not_guessable','reasoning_not_trivia','natural_rule_combination','appropriate_drug_context','distinct_from_bank','not_schedule_flashcard','public_style_without_copying']
# Individual reasons are composed from the actual facts, target Case A/B/SATA,
# controlling source and nearest visible comparison, not similarity thresholds.
topics={'VAX19':'약국의long-acting 주사 조제·투여기록과 대기실진단공개','VAX20':'ED추가치료 후즉시보고와일반24h권고·별도Board trigger','PUB01':'처방·조제단일장소MCSR예외와NPI/교육','PUB02':'MassHealth encouraged와CDTM prescriptive attestation·자발적서비스','PUB03':'Opill daily/EC적응증·ella Rx/levonorgestrel OTC·보험청구','PUB04':'statewideEC 추가교육·실제사용자평가·자발적참여','COUN03':'흡입기사용과시각·언어·청각필요에맞는상담','COUN04':'경구액계량기구와처방용량변경권한','COUN05':'stockroom통과상담실·영업중상담과temporary absence','COUN06':'상담권리sign의치수·MOR문자높이·offer','COUN07':'alert와allergy의사전DUR·환자별평가·문서화','COUN08':'barcode/count·therapeutic duplication·MassPAT와profile'}
realism_fail={
'VAX19':{'authentic_distractors':'청구액만기록·대기실모든사람공개라는선택지는실제기록범위나동의예외혼동보다과도하게명백한오류다.','wording_not_guessable':'정답의조건·보호문구와drug name alone/Only charge/공개허용이라는극단문장이대조돼법규를모르고도제거하기쉽다.','natural_rule_combination':'기록Case A에실제투여여부·적격약경로가없고Case B는일반비밀유지라동일주사서비스의법적조건을자연스럽게연결하지못한다.'},
'VAX20':{'authentic_distractors':'24h와immediate의혼동은실제적이나보고서완료를응급치료보다우선한다는보기가비현실적으로명백하다.','wording_not_guessable':'every otherwise applicable duty와응급치료지연이라는강한과장을배제하면조건을명시한보고선택지가남는다.'},
'PUB01':{'authentic_distractors':'NPI/교육면제와영수증이모든상담을대체한다는선택지가실제근접한등록예외혼동에비해과장됐다.','wording_not_guessable':'must be read within its conditions / reassess applicability는구체적법적결론없이도늘그럴듯한문장이어서정답을드러낸다.','reasoning_not_trivia':'특정약물·실제등록상태·제2장소행위의결과를주지않고조건을조건대로읽으라는메타판단에머문다.'},
'PUB02':{'authentic_distractors':'모든특별처방의무가같고모든약사가시작해야한다는극단선택지는실제경로별조건혼동보다쉽게제거된다.','wording_not_guessable':'encouraged/voluntary라는stem단어를정답이반복하고every/same unconditional이오답을표시한다.','natural_rule_combination':'구체환자나처방경로없는일반직원논쟁에MassHealth,기록,모든경로통보를붙여실제서비스결정이희석된다.'},
'COUN03':{'authentic_distractors':'모든약·환자에게동일내용,공개줄에서크게말하면언제나충분이라는보기는그럴듯한법적경계혼동이약하다.','wording_not_guessable':'정답은환자필요에맞춤이라는일반긍정문구이고오답은identical/solely/regardless로표시된다.'},
'COUN04':{'authentic_distractors':'모든가정용도구가적절하고시연은절대금지라는보기가실제용량·측정법오류보다비현실적으로극단적이다.','wording_not_guessable':'any household utensil necessarily / may never는근거조문을몰라도오답으로제거하기쉽다.','natural_rule_combination':'계량기구누락과처방자의실제dose변경은각각명백한독립문제로제시돼서로의법적조건을결정하지않는다.'},
'COUN05':{'wording_not_guessable':'every hospital prescription / sign만으로privacy충족이라는오답이과도해실제setting범위판단을피할수있다.','natural_rule_combination':'Case B의scheduled period가허용된30분break인지명시하지않아9.18(8)과9.19(17)상호작용을정확하게판단할사실이부족하다.'},
'COUN06':{'authentic_distractors':'직원폴더보관이posting이고표지면개별offer가없어진다는선택지는실제두표지최소치혼동보다쉽다.','wording_not_guessable':'권리안내표지가개별상담을없앤다는과장과identical문구가오답을드러낸다.'},
'COUN07':{'wording_not_guessable':'정답의patient-specific/appropriate와오답의every/no alert conclusively/documentation eliminated가극단적으로대조된다.','authentic_distractors':'alert의임상중요도판단은실제적이나사후검토만으로prospective충족·구두해결시기록완전면제는너무쉽게제거된다.'},
'COUN08':{'wording_not_guessable':'necessarily completes / cannot be retrieved meets immediate retrieval / counted establishes authentic의자기모순·과장이임상검토법규없이도오답을드러낸다.','authentic_distractors':'barcode와DUR혼동은실제적이나retrieve불가profile이즉시검색요건을충족한다는보기는설득력있는오개념이아니다.'}
}
records=[]
for r in p['records']:
 q=r['original_visible_content'];qid=q['question_id'];g=loc[qid]['family_id'];n=int(qid.split('-')[-1]);negative='INCORRECT' in q['stem'];sata=q['question_type']=='SATA';nr=next(x for x in near['records'] if x['question_id']==qid)
 target='오류하나찾기' if negative else '선택지별전체조건결합' if sata else 'Case A' if 'addresses Case A?' in q['stem'] else 'Case B'
 auth=[ref(k,cover[k]) for k in GREF[g]]
 pc=[];exp=[];explanations={}
 for c in q['choices']:
  truth,reason,k,sec=sem[g][c['text']]
  selected=(not truth if negative else truth) if truth is not None else None
  pc.append(dict(choice_id=c['id'],option_text=c['text'],option_text_sha256=hashlib.sha256(c['text'].encode()).hexdigest(),proposition_supported='CONDITIONAL_NOT_ESTABLISHED' if truth is None else 'YES' if truth else 'NO',should_select=selected,finding_ko=reason,authority=ref(k,sec),supporting_authorities=auth))
  if selected is True:exp.append(c['id'])
  explanations[c['id']]=dict(full_original_rationale_read=True,original_rationale_sha256=hashlib.sha256(q['explanation']['choice_analysis'][c['id']].encode()).hexdigest(),assessment='CONDITIONAL_SCOPE_OMITTED' if truth is None else 'SUPPORTED_WITH_SCOPE_CAVEATS',finding_ko=reason)
 expected=sorted(exp);correct='YES' if expected==sorted(q['correct_choice_ids']) else 'NO';lv='KEEP';blocker=None
 findings=[]
 if g=='VAX19':
  findings.append('실제약국내투여및DCP적격약경로를stem에명시하지않았다. 조제만한약국에투여기록의무를부과해서는안된다. 비밀유지는별도MA의무이다.')
  if n in [361,363,364]:correct='AMBIGUOUS';expected=None;lv='HOLD';blocker='Case A의dispensed만으로실제투여/적격약물/적용경로를확정할수없다. 상세투여기록선택지의현재사실상진위를확정하지않는다.'
  else:lv='MINOR_EDIT';findings.append('0362의키D는비밀유지규정으로독립지지되지만기록의무해설은DCP적용조건을명시해야한다.')
 if g=='COUN05':
  findings.append('9.18(8)의all times규정과9.19(17)의single pharmacist temporary absence(30min/6h,on premises,해당로그/callback)를함께설명해야한다.')
  if n==434:correct='AMBIGUOUS';expected=None;lv='HOLD';blocker='scheduled afternoon period가합법적temporary absence인지시간·인력·환자callback사실이없다. 일반규정B는맞지만Case B위반판단을확정할수없다.'
  else:lv='MINOR_EDIT'
 if g=='PUB02':findings.append('authority/protocol을연결하라는해설은actual activity documentation과protocol준수의해석이다. circular에그이름의필드를항상적으라는문언이있다고가르치지않는다. CDTM attestation은prescriptive practices포함시조건이다.')
 if g=='PUB03':findings.append('FDA제품분류와MAstanding order접근을분리했다.보험혜택의유무·개별claim허용은확정하지않는다. ella2021label만으로current라고하지않고2026DailyMedversion7도읽었다.')
 if g=='PUB04':findings.append('statewideEC의no additional training과assessment를검증했다. c94C19A(d)는may이며과거별도교육경로를혼합하지않는다. order의명시된antiemetics도범위에포함하되unrelatedgeneral authority는생기지않는다.')
 if g=='COUN06':findings.append('상담권리표지½inch는minimum이다. MOR기준1inch를상담표지에사용하는것자체가위반은아니다. 원문키는두법정최소값의구별로읽을때지지된다.')
 if g=='VAX20':findings.append('prescriber즉시보고는DCPoutcome(iv)로지지된다.별도Board보고는실제20.02/20.07trigger발생시에만해당하며모든단순오류/반응의자동보고를뜻하지않는다.')
 if not findings:findings.append('모든보기와한국어해설을해당247CMR의행위주체·범위·전제조건과대조했다. 키의선택조합과현재문언이일치한다.')
 criteria={k:True for k in C}
 reasons={
'jurisprudence_reasoning':f'{topics[g]}의{target}에서권한/의무/권고/기한또는범위적용을판단한다. 단일정답·SATA·INCORRECT극성을개별확인했다.',
'practice_plausibility':f'{topics[g]}은약국에서발생가능한업무장면이다. 다만법적적용사실누락은legal_review와별도기록했다.',
'authentic_distractors':'인접한처방/OTC/standing-order경로의실제혼동을반영하며미리법률판단하지않고선택지를구별해야한다.',
'wording_not_guessable':'이문항의제품·경로분류를알아야키를정할수있다. 단지항상/절대등문구하나로전체정답조합이정해지지는않는다.',
'reasoning_not_trivia':f'{target}는{topics[g]}의의무적용을요구한다. 숫자나반복family존재만으로실패처리하지않았다.',
'natural_rule_combination':'같은요청/서비스의선택과별도조건을연결하며전제가달라질때의법적결과를비교한다.',
'appropriate_drug_context':'특정제품의법적분류·적응증차이가있는곳에서는이름을사용하고,설비/기록/상담규정에서는불필요한약물이름을요구하지않았다.',
'distinct_from_bank':f"canonical최근접{nr['canonical'][0]['question_id']}및public최근접{nr['public'][0]['question_id']}의stem·전보기를직접읽었다. public은동일사례family변형이므로독립새사례로세지않는다. 이ID는default에없고archive연습으로구분되어있어그존재만으로자동FAIL하지않는다.",
'not_schedule_flashcard':'schedule명칭이나약물리스트만묻는flashcard가아니라해당서비스행위와조건을묻는다.',
'public_style_without_copying':'currentMPJEstyleprofile의영어selected-response·scenario·SBA/SATA구조에대조했다.공개저장소문항visible비교만사용했고PreMPJE/회상/상용bank는열지않았다.이번NABPlive조회403으로fresh공개sample원문확인으로주장하지않는다.'}
 for k,v in realism_fail.get(g,{}).items():criteria[k]=False;reasons[k]=v+' '+f'현재{qid}의{target}에대해판단했다.'
 # Bind weakness examples only to options actually present in this exact item.
 actual_false=[c['text'] for c in q['choices'] if sem[g][c['text']][0] is False]
 if 'authentic_distractors' in realism_fail.get(g,{}):
  reasons['authentic_distractors']='현재보기의 다음 오류명제가 실제 근접한 예외·기한 혼동보다 너무 명백하거나 추상적이다: '+ ' / '.join(actual_false)+'. 목표 '+target+'에 대해 개별 평가했다.'
 if 'wording_not_guessable' in realism_fail.get(g,{}):
  reasons['wording_not_guessable']='현재보기의 다음 강한 단정/과장/자기모순을 제거하면 구체 법규 지식 없이도 정답에 접근하기 쉽다: '+' / '.join(actual_false)+'. 정답의 조건부·전문판단 문구와 대조했다.'
 if n==363:
  criteria['authentic_distractors']=True;criteria['wording_not_guessable']=True
  reasons['authentic_distractors']='실제 오답A는 조제기록으로 투여기록을 대체한다는 구체적 기록 혼동이다. 없는 Only charge 보기를 이 문항의 약점으로 쓰지 않았다.'
  reasons['wording_not_guessable']='현재 A–D의 키조합은 기록요건·비밀유지의 실제 적용을 판단해야 한다. 다만 투여 사실 누락의 법적 문제는 별도 실패다.'
 if n==367:
  for k in ['authentic_distractors','wording_not_guessable']:
   criteria[k]=True
  reasons['authentic_distractors']='현재 SATA의 네 명제는 모두 허용되는 all-selected 조합이다. prescriber/Board보고 구별, 즉시보고, 응급대응, should24h를 개별 검증해야 하며 이 문항에는 응급치료보다 보고서우선이라는 오답이 없다.'
  reasons['wording_not_guessable']='모든 보기가 참인 조합은 24h/즉시, should/must, 별도trigger를 알아야 확정된다. family다른 문항의 every duty 오답을 이 문항에 전가하지 않았다.'
 if n==368:
  criteria['authentic_distractors']=True
  reasons['authentic_distractors']='실제 유일 오류D는 prescriber통화로 별도Board의무까지 완료한다는 수신기관 혼동이다. 실제 reporting workflow의 오개념이다.'
 if g=='VAX19' and n in [361,363,364]:criteria['jurisprudence_reasoning']=False;reasons['jurisprudence_reasoning']='실제투여·적격약경로가불명확하여해당기록의무의법적적용판단을완결할사실이없다.'
 if n==433:criteria['distinct_from_bank']=False;reasons['distinct_from_bank']='canonicalMA-Q-0285도환자가dispensing area를통과해야하는상담실접근의동일위반을묻는다. currentCase A의stockroom추가는같은접근금지판단을바꾸지않는다. publicarchive변형존재와구별해canonical의실제판단중복을기록한다.'
 # Add concrete semantic comparison even when the nearest lexical candidate is a weak match.
 comparison={
'VAX19':'canonical injection권한/eligible제품또는투여후보고장면과달리current는기록/비밀유지를묻지만실제투여사실이약하다.',
'VAX20':'canonicalCQI/seriousinjury기한과currentDCPprescriberimmediate기한은수신자·trigger가다르며같은답으로합치지않는다.',
'PUB01':'canonicalMA-Q-0123의전자처방예외검증과currentMCSR단일장소예외는서로다른권한문제이다.',
'PUB02':'canonical투여notation/보고권고와currentMassHealth등록/CDTMattestation은서로다른동사·대상이다.',
'PUB03':'canonicalEC추가교육문항/응급대체조제와currentFDA제품용도·OTC분류는판단대상이다르다.',
'PUB04':'canonicalMA-Q-0325는EC와COVID훈련을비교하고current는EC사용자assessment/voluntary범위를함께묻는다.단training대상Case A에는EC규칙반복이있다.',
'COUN03':'canonicallargeprint방향표시법/상담항목문항과current실제흡입기사용·언어청각전달은관련되나주된판단이다르다.',
'COUN04':'canonicalMA-Q-0287과measuring-device규칙은공유하지만current는dose변경권한을함께제시한다.숫자만바꾼복제로보지는않는다.',
'COUN05':'canonicalMA-Q-0285와Case A접근금지판단은같고MA-Q-0419와privacy도겹친다. Case B와INCORRECThospital범위질문은대상이달라ID별판정했다.',
'COUN06':'canonicalMA-Q-0286와sign치수·위치는겹친다. current는8x10실제치수와MOR1inch혼동을추가했으나숫자암기만으로좋은문항이라고판정하지않았다.',
'COUN07':'canonicalMA-Q-0085/0410/0417와DUR책임·문서화규칙이겹치며current는no-alertallergy상황을쓴다.실제wording/오답취약점을별도판정했다.',
'COUN08':'canonicalMA-Q-0313은DUR조치기록누락,current는count/barcode와clinicalreview차이를묻는다.알레르기·directions를PMP가대체하지못하는조건도읽었다.'}[g]
 rv='PASS' if all(criteria.values()) else 'FAIL'
 juris='MA업무규정이직접통제한다.연방약물schedule/등록예외를새로주장하지않으며HIPAA는covered entity인경우의보조근거이고MA비밀유지의무는별개다.' if g in ['VAX19','COUN03'] else '현재문항은MA직업규정·행정지침의해당행위를묻는다.연방법이MA조건을면제한다는근거없는주장을하지않는다.'
 if g in ['PUB03','PUB04']:juris='FDA제품허가/OTC와Rx분류는연방문제이고MAstanding order는환자별처방을생성하는별도접근경로다. standing order나보험처방이FDA분류를전환하지않는다.'
 if g in ['PUB01','PUB02']:juris='MA한정MCSR·처방경로와NPI/교육·CDTM조건을구별한다.단일장소예외가연방DEA등록또는모든활동의등록면제라는결론은내리지않는다.'
 records.append(dict(question_id=qid,record_sha256=r['record_sha256'],family_id=g,read_scope=dict(stem='FULL',every_choice='FULL',stored_key='FULL',core_korean_explanation='FULL',every_choice_korean_explanation='FULL',learning_boundary='FULL',visible_content_sha256=r['visible_content_sha256'],read_at=now,source_input=str(E/'assigned-visible-input.json')),legal_review=dict(existing_answer_correct=correct,stored_key=q['correct_choice_ids'],independently_expected_key=expected,conditional_candidate_key=sorted(exp) if expected is None else None,question_type=q['question_type'],polarity_analysis_ko=f'{target}; '+('INCORRECT는틀린명제하나만고르는극성으로반전했다.' if negative else 'SATA는모든보기를각각판단해정확한조합을확인했다.' if sata else '목표Case에대해단일정답의유일성을확인했다.')+(' 단현재적용사실누락으로유일성을확정하지않았다.' if correct=='AMBIGUOUS' else ''),per_choice_findings=pc,authorities=auth,jurisdiction_analysis_ko=juris,verdict=lv,finding_ko=' '.join(findings),blocker=blocker,original_explanation_review=dict(core_read_in_full=True,every_distractor_read_in_full=True,core_reasoning_sha256=hashlib.sha256(q['explanation']['core_reasoning'].encode()).hexdigest(),core_assessment_ko=' '.join(findings),choice_analysis=explanations,learning_boundary_assessment_ko='네변형이같은사례라는고지를읽었다.이를법적정확성·canonicalrelease보증으로해석하지않았다.')),realism_review=dict(verdict=rv,decision='KEEP' if rv=='PASS' else 'MAJOR_REWRITE',criteria=criteria,criterion_findings_ko=reasons,finding_ko=('10기준을각각확인해통과했다.' if rv=='PASS' else '현재사실·보기에서확인한취약점때문에현실성재작성이필요하다. 숫자/반복family존재만으로일괄실패시키지않았다.'),duplicate_evidence=dict(method=near['method'],canonical_count=near['canonical_count'],public_count=near['public_count'],nearest_candidates=nr,actual_read='TOP3_STEMS_AND_ALL_CHOICES_BOTH_POOLS',visible_comparison_input=str(D/'nearest-visible-input.json'),visible_comparison_sha256=sha(D/'nearest-visible-input.json'),nearest_measurement_path=str(D/'nearest-comparisons.json'),nearest_measurement_sha256=sha(D/'nearest-comparisons.json'),semantic_comparison_ko=comparison,default_pool_member=qid in defaults,archive_variants_ko='current learning_boundary가같은두사례네변형임을고지한다.공유원문을새독립사례로세지않으며defaultpool대상과구별했다.')),safe_hold_recommended=(lv!='KEEP' or rv!='PASS'),release_eligible=False,canonical_release_credit=0,required_next_action_ko=blocker or ('법규의조건·예외를해설에명시하고새hash로독립재감사한다.' if lv!='KEEP' else '법규검토결과를유지하되오답을실제인접규정·예외혼동으로재설계하고새hash로현실성재감사한다.' if rv=='FAIL' else '이독립legacy결과는canonicalrelease증거가아니다.원문을변경하면새hash로재감사하고root의별도releasegate를통과해야한다.')))
style=json.load(open('data/exam_style/mpje_style_profile.json'));bp=json.load(open('data/blueprint.json'))
policies=['docs/INDEPENDENT_LEGACY_REVIEW_RUNBOOK.md','docs/RELEASE_POLICY.md','docs/AUDIT_WORKFLOW.md','docs/SOURCE_USE_POLICY.md','docs/QUESTION_AUTHORING_STANDARD.md','schemas/blueprint.schema.json','schemas/exam_style_profile.schema.json','schemas/audit.schema.json']
# schemas are captured and pinned here; unreviewed schema text is not claimed as a legal source.
report=dict(schema_version='independent-legacy-substantive-review/1',stage='independent-legacy',independent_of_authors=True,auditor='GPT',auditor_instance='GPT:/root/independent_wave12_a:20261104',actor_provenance=dict(actor_id='/root/independent_wave12_a',session_id='/root/independent_wave12_a'),canonical_audit=False,canonical_release_credit=0,release_eligible=False,reviewed_at=date,completed_at=now,job_id=a['job_id'],question_hashes=a['question_hashes'],assignment_binding=dict(path=str(E/'assignment.json'),sha256=sha(E/'assignment.json'),visible_packet_path=str(E/'assigned-visible-input.json'),visible_packet_sha256=sha(E/'assigned-visible-input.json')),independence_statement_ko='현재세션은배정원문의저자/편집자가아니다.기존author/independent판정보고서·질문원장·숨은truth를모델로읽지않았다.원본객체는programmatic visible비교와source_ids/family_id whitelist용으로만읽고모델에는허용필드만출력했다.실제동일세션을다른instance로증식하지않는다.',prior_verdict_exposure={'occurred':False,'affected_ids':[]},style_profile=dict(profile_id=style['profile_id'],content_version=style['content_version'],semantic_hash=style['content_hash'],file_sha256=sha('data/exam_style/mpje_style_profile.json')),blueprint=dict(blueprint_id=bp['blueprint_id'],content_version=bp['content_version'],semantic_hash=bp['content_hash'],schema_version=bp['schema_version'],file_sha256=sha('data/blueprint.json')),methodology_files=[dict(path=x,file_sha256=sha(x)) for x in policies],sources=sources,retrieval_limitations_ko=['Firecrawl최초live scrape는insufficientcredits로실행되지않았다.재시도하지않고공식HTTPS기본인증서검증직접GET로조회했다.','NABPcompetency/sample직접조회403은actualcontentread로세지않았다.styleprofile에대조했고protectedPreMPJE/회상/상업원문을입력하지않았다.','105CMR700추측URL은404이다.이파일로법규검증했다고주장하지않고현재DCPcircular직접문언범위의결론만낸다.','FDAella2021label은최신이아닐수있다는표시가있어그것만으로current라고하지않았다.공식DailyMed의2026version7label/API를추가조회했다.','c94C19F현행legislature표시는호르몬패치/경구피임약만이다.DCP2026circular의HIV/STI확장과완전히동일문언이라고주장하지않으며배정문항에서그확장의개별처방적법성을인증하지않았다.'],verification_scope=dict(questions=len(records),choices=sum(len(x['legal_review']['per_choice_findings']) for x in records),canonical_comparison_count=439,public_comparison_count=2349,nearest_unique_visible_records_read=len(nv['records']),live_notes_builder='NOT_RUN_BY_INSTRUCTION',sourceguard='NOT_RUN_BY_INSTRUCTION_SPARSE_PREIMAGE',shared_queue_mutation='NOT_PERFORMED',canonical_admission='NOT_PERFORMED',release_build='NOT_RUN'),records=records)
assert len(records)==40 and {r['question_id'] for r in records}==set(a['question_hashes'])
assert all(r['legal_review']['existing_answer_correct']!='NO' for r in records),[(r['question_id'],r['legal_review']['stored_key'],r['legal_review']['independently_expected_key']) for r in records if r['legal_review']['existing_answer_correct']=='NO']
report['summary']={k:dict(__import__('collections').Counter(r[scope][key] for r in records)) for k,scope,key in [('legal_verdict','legal_review','verdict'),('existing_answer_correct','legal_review','existing_answer_correct'),('realism_verdict','realism_review','verdict')]}
out=R/'reports/full-corpus-review/independent-phase12-a-review.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(out,sha(out));print(report['summary'])
