import collections,datetime,gzip,hashlib,json,pathlib,sys
ROOT=pathlib.Path('/workspace/independent-phase3-g')
BASE=ROOT/'reports/full-corpus-review/evidence/independent-phase3-g'
REPORT=ROOT/'reports/full-corpus-review/independent-phase3-g-review.json'
INPUT=pathlib.Path('/workspace/oddments/reports/full-corpus-review/independent-phase3-g-visible-input.json')
ASSIGN=json.load(open('/tmp/independent-phase3-g-assignment.json'))
PACKET=json.load(open(INPUT))
ACTOR='/root/independent_case_g'
INSTANCE='gpt-independent-phase3-g-root-independent_case_g-20261103'
DATE='2026-11-03'
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def objsha(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def write(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

# Sources are authored from the official raw bodies directly read in this session.
# Every source includes a selected-provision read scope, not a claim to have read
# all label sections or to have established a commencement date from retrieval.
SOURCE_DETAILS={
 'practice':('247 CMR 9.00, Professional Practice Standards','OFFICIAL_REGULATION','9.06(3)-(5); 9.15(2); 9.16(7); 9.17(1)-(2); 9.19(13)','Official PDF footer 12/6/2024',None,'환자 profile의 reasonable effort, 처방 적법성의 별도 판단, 교부 전 DUR 및 자동재조제 동의는 독립 의무이다. 9.06의 상담·정보지·미보유 시 가장 가까운 재고처 안내도 직접 확인했다.'),
 'vaccine':('MA DPH/Board Policy 2023-02 Vaccine Administration','OFFICIAL_BOARD_POLICY','Personnel definition pp.1; III(A), III(D)(1)-(4); IV(A)-(G), pp.2-4','Adopted 2023-05-04; revised 2025-09-04',None,'PTT는 제외되고 PT 적격성은 전국인증 또는 full PT licensure 후 500시간이다. 현재 CPR, 교육, 약사의 선택·상담, 별도 응급약 order와 influenza/COVID 외 사전 MIIS 확인을 확인했다.'),
 'miis':('105 CMR 222.000 Massachusetts Immunization Information System','OFFICIAL_REGULATION','222.003 Data Sharing Objection; 222.100(A); 222.105(A)-(B)','Mass. Register #1528, 2024-08-16',None,'새 접종 후 72시간 보고와 이름 미정 신생아 예외를 구분했다. sharing objection은 Department 접근·이용을 제한하지 않으며 보고 거부권이 아니다. 문항은 routine vaccine이므로 신생아 예외를 보태지 않는다.'),
 'vis':('CDC About VISs','OFFICIAL_AGENCY_GUIDANCE','VISs are required by law; 42 U.S.C. 300aa-26 reference','Current official CDC page retrieved 2026-11-03; publication/commencement not independently established',None,'적용되는 VIS는 각 접종 전에 환자/법정대리인에게 제공한다. 문항은 applicable VIS를 명시하며 모든 제품에 VIS가 있다는 주장을 하지 않는다.'),
 'administration':('DCP Circular Letter 26-03-124 Pharmacist Administration of Medications','OFFICIAL_AGENCY_GUIDANCE','Purpose and Dispensing by Administration pp.1-2(a)-(f); OTP note; eligible list; Training/CPR/Continued Competency/Manufacturers Instructions p.3; Record Keeping/Reporting Adverse Events p.4','Circular dated 2026-03-11; replaces DCP 23-04-118',None,'약사·intern, 18세 이상, valid prescription, 비-IV, single-dose packaging 및 prescribed single doses를 확인했다. Ceftriaxone은 IM, 임상 적절 교육·현행 CPR·REMS·기록·ED monitoring 사건 즉시 prescriber 보고를 확인했다. Addiction medication OTP note와 별도 buprenorphine eligible list가 함께 존재하므로 단순 REMS 준수를 일반 retail 투여 허가로 확대하지 않는다.'),
 'personnel':('247 CMR 8.00 Pharmacy Interns and Technicians','OFFICIAL_REGULATION','8.01(3) direct supervision by registered pharmacist preceptor','Mass. Register #1546 2025-04-25; footer Effective 2025-01-09','2025-01-09','Qualified intern의 약사 감독은 일반 intern 규정에도 근거한다. 기술자 백신 권한을 비백신 LAI 투여 권한으로 옮기지 않는다.'),
 'cdtm':('247 CMR 16.00 Collaborative Drug Therapy Management','OFFICIAL_REGULATION','16.02(1)(b)-(c); 16.03(5)(a),(c)-(e); 16.04(1),(4)-(6)','Official PDF MA REG #1354 dated 2017-12-15',None,'보험은 건당 100만 달러 이상의 CDTM 전문배상 담보이고, retail은 성인·환자별 referral/consent·Schedule VI 권한·24시간 copy 전송을 구분한다. 2년 갱신 및 치료 연속성·서면 종료 통지를 확인했다. PharmD grandfather 문구는 statutory degree 대안보다 좁으므로 해당 설명은 별도 보류한다.'),
 'cdtm-statute':('M.G.L. c.112 §24B½','OFFICIAL_STATUTE','24B½(a) definitions; (b)(3) pharmacist education/experience; (c) retail limits','Current consolidated official legislature page, checked 2026-11-03',None,'정의상 laboratory evaluation은 diagnostic component를 포함하지 않는다. Retail II-V prescribing 금지와 Schedule VI/환자 referral/24시간 copy 조건을 확인했다. (b)(3)은 PharmD 또는 5년/동등경험을 열거하여 247 CMR16의 grandfather와 문언 차이가 남는다. 이 차이를 감추지 않는다.'),
 'cdtm-equivalency':('MA Board Advisory Educational Equivalency for CDTM Agreements','OFFICIAL_BOARD_POLICY','II(A)(1)-(3), II(B), III petition','Adopted 2019-02-07',None,'BPS, PGY1/2와 추가 실무 또는 감독 CDTM 경로, clinical-site credentialing 및 petition 절차를 직접 읽었다. 새 PharmD만의 statutory 권리가 배제되는지 이 advisory만으로 해결되었다고 주장하지 않는다.'),
 'ec-order':('DPH Statewide Standing Order for Dispensing Emergency Contraception Pills','OFFICIAL_STANDING_ORDER','ECP Indication; Emergency Contraception Pills Order steps 1-5; authorizing physician signature','Signed Estevan Garcia MD, 2022-08-04',None,'실제 서명된 order의 지정 UPA/LNG와 환자 assessment·screening·instruction 범위를 읽었다. 빈 model template은 이 문서처럼 발행된 order가 아니다. EC order를 모든 reproductive-health 약의 일반 처방권한으로 확대하지 않는다.'),
 'ec-pharmacy':('MA DPH Emergency contraception information for pharmacies','OFFICIAL_AGENCY_GUIDANCE','Reporting requirement; FAQ How should pharmacist dispense EC; Can pharmacist dispense for someone other than themselves?','Current official DPH page retrieved 2026-11-03; update date not stated',None,'standing order EC는 patient-specific prescription으로 조제하고 연간 보고하며 사용자를 대면 또는 전화로 평가한다. OTC 제3자 구매와 구별한다. 별도 file system이 강제된다고 주장하지 않고 별도 보고에 필요한 추적 기록을 말한다.'),
 'ec-statute-19a':('M.G.L. c.94C §19A Emergency contraception','OFFICIAL_STATUTE','19A(a)-(c),(e)','Current consolidated official legislature page checked 2026-11-03',None,'EC 정의 및 standing order 범위와 연간 EC 조제 횟수 보고를 직접 확인했다. 일반 PMP 전송은 이 조항의 보고 의무를 자동 충족한다는 근거가 없다.'),
 'contraception-law':('M.G.L. c.94C §19F','OFFICIAL_STATUTE','19F(a)-(c) pharmacist hormonal contraceptive authority','Current consolidated official legislature page checked 2026-11-03',None,'이 조항의 약사 권한은 hormonal patches 및 self-administered oral contraceptives이다. 보험 급여라는 사실에서 injection 등 추가 prescribing authority가 생기지 않는다. CDTM의 성인 제한을 이 별도 경로로 제거하지 않는다.'),
 'naloxone-policy':('MA Board Policy 2024-01 Naloxone Dispensing','OFFICIAL_BOARD_POLICY','Introduction; I(A)-(G); II(A)-(B)','Adopted 2024-01-11; revised 2025-02-06',None,'OTC 제품과 insurance용 standing order를 구분하고, rescue kit expiration label 외 상담 및 정보지 의무를 확인했다. Naloxone의 PMP 선호 보고방식을 EC 보고에 확대하지 않는다.'),
 'opioid-antagonist-law':('M.G.L. c.94C §19B','OFFICIAL_STATUTE','19B(a)-(c),(e),(g)','Current consolidated official legislature page checked 2026-11-03',None,'실제 statewide standing order 및 insurance billing의 prescription 취급을 확인했다. 구입자와 최종 사용자가 다를 수 있으나 OTC 법적 구매자격이 insurance workflow로 바뀌지 않는다.'),
 'naloxone-otc':('MA DPH Memorandum Over the Counter Naloxone','OFFICIAL_AGENCY_GUIDANCE','Access options; Cost and coverage; Placement of OTC naloxone','Memorandum dated 2023-12-20',None,'OTC 표시 제품의 일반 소매 구매와 처방/standing order 경로가 병존한다. anonymous shelf access는 이 memo의 should 권고이며 must로 전환하지 않았다. 현금 OTC 구매에 insurance용 처방 요건을 복사하는 근거가 없다.'),
 'planb':('FDA Plan B One-Step Information','OFFICIAL_AGENCY_GUIDANCE','Opening product status; 2013 OTC approval history; What is emergency contraception?','Official page current-as-of 2022-12-23',None,'LNG Plan B One-Step은 OTC이며 2013년부터 연령 제한 없는 nonprescription 승인이다. UPA의 별도 Rx status와 구별한다.'),
 'opill':('FDA Approves First Nonprescription Daily Oral Contraceptive','OFFICIAL_AGENCY_GUIDANCE','Daily norgestrel approval; Opill is not for use as emergency contraception','FDA announcement 2023-07-13','2023-07-13','Opill은 daily norgestrel contraceptive이고 EC가 아니다. 같은 피임 목적만으로 사용경로·상담 없이 EC 요청을 대체할 근거가 없다.'),
 'ella-current':('DailyMed ELLA ulipristal acetate tablet, PMI Branded Pharmaceuticals','OFFICIAL_PRODUCT_LABEL','Product category HUMAN PRESCRIPTION DRUG; carton Rx only; section 1','Label revised 2025-01; DailyMed updated 2026-07-20, API published 2026-07-24',None,'올바른 setid와 ulipristal acetate 30mg, NDA022474 및 Rx only를 직접 확인했다. 처음 조회한 다른 setid는 DailyMed home으로 redirect되어 배제했다. 2021 historical FDA label을 현행 버전으로 인증하지 않는다.'),
 'clozapine':('FDA Removes Clozapine REMS','OFFICIAL_AGENCY_GUIDANCE','What Is FDA Announcing; What Is FDA Doing; What Should Health Care Professionals Do','Content current as of 2026-04-03; REMS removal effective 2025-06-13','2025-06-13','REMS enrollment/ANC reporting dispensing gate 제거와 label-based ANC monitoring을 구별했다. 폐지 이후 위험 및 monitoring 권고가 소멸했다는 설명은 틀리다.'),
 'boxed-rems-faq':('FDA Frequently Asked Questions about REMS','OFFICIAL_AGENCY_GUIDANCE','How FDA determines REMS need; Current REMS; Are REMS permanent?','Content current as of 2018-01-26; currently served by FDA',None,'REMS는 labeling을 넘어 추가 조치가 필요한지 FDA가 결정하며 프로그램은 약물별로 존재·변경·제거된다. Boxed warning 자체에서 enrollment를 추론하지 않는다. Current clozapine 원문은 warning이 남아도 REMS가 제거된 실제 반례이다.'),
 'isotretinoin':('FDA iPLEDGE Risk Evaluation and Mitigation Strategy','OFFICIAL_AGENCY_GUIDANCE','Implementation delayed until November (June 16, 2026); February 9, 2026 approval update','Content current as of 2026-06-16; planned implementation 2026-11-15','2026-11-15','Oct26 및 조회일 Nov3에는 Nov15 modification을 미리 적용하지 않는다. 승인일과 시행일을 구분하며 이 문항의 일반 window 문구를 모든 프로그램의 조기변경 절대금지 법리로 확대하지 않는다.'),
 'sublocade':('DailyMed SUBLOCADE buprenorphine extended-release injection','OFFICIAL_PRODUCT_LABEL','2.6 Limits on Distribution; 5.2 REMS','Label revised 2025-02; DailyMed updated 2026-07-27',None,'certified healthcare settings/pharmacies는 provider에게 직접 공급하고 환자에게 take-home dose를 조제하지 않는다. 유효 처방만으로 공급경로 제한이 사라지지 않는다.'),
 'mifepristone':('FDA Questions and Answers on Mifepristone','OFFICIAL_AGENCY_GUIDANCE','The Mifepristone REMS Program: restrictions on prescribing and dispensing','Content current as of 2026-04-08; January 2023 REMS modification discussed',None,'약국과 prescriber certification 및 REMS requirements는 federal product-specific 요건이다. 주 접근 보호가 certified pharmacy 조건을 제거했다는 문항의 전제를 지지하지 않는다.'),
 'spravato':('DailyMed SPRAVATO esketamine nasal spray','OFFICIAL_PRODUCT_LABEL','2.1 respiratory assessment; 5.5 SPRAVATO REMS','Label revised 2026-03; DailyMed updated 2026-09-22',None,'certified setting 내 조제·투여, provider 직접 관찰, 적어도 2시간 monitoring 및 certified setting으로만 약국 공급을 확인했다. 일반 take-home nasal spray 관행을 적용할 수 없다.'),
 'brixadi':('DailyMed BRIXADI buprenorphine extended-release injection','OFFICIAL_PRODUCT_LABEL','2.1 Important Dosage/Administration; 2.3 recommended dosing and weekly/monthly transition; 5.2 REMS','Label revised 2025-12; DailyMed updated 2025-12-31',None,'weekly와 monthly는 두 제형이며 weekly doses를 합쳐 monthly로 만들 수 없다. 전환은 명시된 임상 판단·용량표에 따른다. 동일 성분만으로 처방된 제형을 확인 없이 교환한다는 근거가 아니다.'),
 'tirf':('FDA Transmucosal Immediate-Release Fentanyl Medicines','OFFICIAL_AGENCY_GUIDANCE','September 16, 2024 notice; list of TIRF dosage forms and REMS scope','Content current as of 2024-09-19; production discontinued 2024-09-30','2024-09-30','열거된 TIRF는 transmucosal immediate-release 제형이며 patch가 아니다. 현재 new enrollment 중단 공지를 읽었고 신규 TIRF 등록이 열려 있다고 쓰지 않았다. Patch에 이 프로그램을 복사하는 것은 지지되지 않는다.'),
 'schedule4-ecfr':('21 CFR 1308.14 Schedule IV, eCFR','OFFICIAL_REGULATION','1308.14(a),(c)(2) Alprazolam, DEA code 2882','eCFR title21 up to date 2026-10-30; selected provision read 2026-11-03',None,'실제 eCFR 본문 (c)(2)에 Alprazolam이 Schedule IV로 열거되어 있음을 직접 확인했다. eCFR는 continuously updated이지만 official legal print edition은 아니라는 자체 한계도 읽었다. GovInfo 2026 잘못된 경로의 HTTP200 PageNotFound는 배제했다.'),
 'alprazolam-current':('DailyMed XANAX alprazolam tablet, Viatris Specialty LLC','OFFICIAL_PRODUCT_LABEL','9.1 Controlled Substance; product DEA Schedule CIV','Label revised 2024-04; updated 2024-04-15; API publication 2026-10-12',None,'올바른 XANAX setid의 본문 9.1에 alprazolam Schedule IV가 명시되어 eCFR classification과 대조했다. Product category와 실제 active ingredient를 직접 읽었고 guessed setid가 home으로 향한 실패를 따로 남겼다.'),
}

sources=[]
for sid,(authority,stype,section,version,effective,memo) in SOURCE_DETAILS.items():
 meta=json.load(open(BASE/(sid+'-retrieval.json')))
 assert meta['http_status']==200 and meta.get('raw_sha256')
 meta['body_verification']='IDENTITY_AND_LISTED_PROVISIONS_DIRECTLY_READ_IN_THIS_ACTUAL_SESSION'
 meta['read_scope']=section
 meta['independent_read_memo_ko']=memo
 write(BASE/(sid+'-retrieval.json'),meta)
 sources.append(dict(source_id=sid,authority=authority,source_type=stype,source_class='PUBLIC_OFFICIAL',official_url=meta['resolved_url'],requested_official_url=meta['official_url'],exact_section=section,law_checked_date=DATE,effective_date=effective,version=version,effective_date_limitation_ko='조회일은 시행일이 아니다. 별도 commencement를 원문에서 확정하지 못한 경우 null이며 위 version/공표·개정 정보를 적용 범위로 고정한다.' if effective is None else '명시된 특정 사건/조항/시행 예정일이며 문서 전체의 최초 효력일로 일반화하지 않는다.',evidence_path=meta['raw_evidence_path'],evidence_sha256=sha(ROOT/meta['raw_evidence_path']),raw_sha256=meta['raw_sha256'],text_evidence_path=meta['text_evidence_path'],text_evidence_sha256=meta['text_sha256'],retrieval_provenance=meta,review_memo_ko=memo))
SOURCES={s['source_id']:s for s in sources}
def ref(sid,section):
 s=SOURCES[sid]
 return dict(source_id=sid,authority=s['authority'],source_type=s['source_type'],exact_section=section,official_url=s['official_url'],law_checked_date=DATE,effective_date=s['effective_date'],version=s['version'],evidence_path=s['evidence_path'],evidence_sha256=s['evidence_sha256'],raw_sha256=s['raw_sha256'])

# Indices follow first appearance in the fully read visible packet. Text is never
# edited. These conclusions were made from the sources above, not hidden truth.
P={}
def prop(i,yes,topic,reason,*refs):P[i]=dict(supported='YES' if yes else 'NO',topic_ko=topic,finding_ko=reason,authorities=[ref(*r) for r in refs])
prop(1,True,'clozapine REMS 폐지','폐지된 enrollment는 현행 dispensing prerequisite가 아니다. Label 기반 모니터링과 구분한다.',('clozapine','What Is FDA Announcing; What Should Health Care Professionals Do'))
prop(2,False,'boxed warning과 REMS','Boxed warning만으로 특정 enrollment program 존재를 단정하지 않는다. Clozapine은 warning 위험이 남아도 REMS가 제거되었다.',('boxed-rems-faq','How FDA determines need; Current REMS'),('clozapine','What Is FDA Doing'))
prop(3,False,'승인일과 시행일','명시된 future implementation을 현재로 끌어오지 않는다. iPLEDGE 2026 modification은 Nov15로 연기되었고 Oct26 문맥에서 미시행이다.',('isotretinoin','June 16 2026 delay notice'))
prop(4,False,'Sublocade 공급경로','유효 처방과 별개로 certified pharmacy는 provider에게 직접 공급하며 patient take-home 조제는 REMS 경로가 아니다.',('sublocade','2.6; 5.2'))
prop(5,False,'미확인 알레르기','빈 imported field를 확인된 NKA로 기록할 근거가 없다. 알려진 allergy history를 얻고 기록하는 reasonable effort가 요구된다.',('practice','9.16(7)(b)'))
prop(6,False,'자동재조제 동의','Claim 성공은 환자/agent의 enrollment consent 자체가 아니다. Enrollment 전에 동의를 얻고 기록해야 한다.',('practice','9.19(13)'))
prop(7,False,'바코드와 처방 적법성','제품 일치 검사는 legitimate purpose·usual course·authentic prescription의 전문적 판단을 대체하지 않는다.',('practice','9.15(2)(a)-(d)'))
prop(8,True,'교부 전 allergy DUR','New prescription을 환자나 agent에게 dispensing/delivery하기 전 DUR에 allergy interaction을 포함해 합리적으로 검토한다.',('practice','9.17(1),(1)(g)'))
prop(9,True,'접종 전 VIS','적용되는 VIS는 접종 전에 환자/법정대리인에게 제공한다. Receipt 후 제공으로 바꾸지 않는다.',('vis','VISs are required by law'),('vaccine','IV(D)'))
prop(10,False,'MIIS 조회 예외 범위','Influenza/COVID 제외를 shingles에 확대할 수 없다. State policy에 따른 다른 백신은 투여 전에 MIIS를 확인한다.',('vaccine','IV(E)-(F)'))
prop(11,False,'현재 CPR','초기 vaccine course 완료는 현행 CPR 유지 요건을 대신하지 않는다.',('vaccine','III(A)-(B)'))
prop(12,False,'기술자의 임상 역할','약사가 상담하고 vaccine을 선택한 후 적격 PT가 physical preparation/administration을 수행한다. 독립 선택·임상 상담을 PT에 부여하지 않는다.',('vaccine','III(D)(4)'))
prop(13,False,'PT 인증과 추가 요건','National certification은 PT 적격성의 대안 중 하나일 뿐, training·current CPR·약사 승인 및 직접 감독을 대체하지 않는다.',('vaccine','Personnel pp.1; III(A); III(D)(1)-(4)'))
prop(14,False,'500시간 기산점','경험 경로는 full Pharmacy Technician license 후의 500시간이다. PTT로 일한 시간만을 이 경로에 넣을 수 없다.',('vaccine','III(D)(1)(b)'))
prop(15,True,'PTT 투여 제외','주 정책의 administering pharmacy personnel은 PTT를 제외한다. 문항은 PTT의 비주사 허용 업무를 일반적으로 말하며 구체 임상 업무를 새로 허용하지 않는다.',('vaccine','Personnel definition p.1; III(D)(1)'))
prop(16,True,'현재 CPR','실제 백신 투여자는 현행 CPR certification을 유지한다. 별도 training 등은 stem의 all other prerequisites 조건이다.',('vaccine','III(A)'))
prop(17,False,'응급약 order','백신 order와 별개로 adverse event 관리용 emergency medication에도 prescription/standing order가 필요하다. 해당 약을 포괄하는 order가 없다고 명시되어 있다.',('vaccine','IV(A)-(C)'))
prop(18,True,'shingles 전 MIIS','Shingles는 influenza/COVID 사전 조회 예외에 해당하지 않으므로 투여 전 MIIS 확인이 지지된다.',('vaccine','IV(E)'))
prop(19,False,'MIIS 보고 시한','월말 청구 일정이 일반 접종 후 72시간 보고 의무를 연장하지 않는다. Newborn naming 예외를 routine 문항에 넣지 않는다.',('miis','222.100(A)'))
prop(20,False,'sharing objection과 보고','Sharing objection은 다른 MIIS 이용자 간 공유를 제한하며 Department의 접근·이용 또는 필수 보고를 삭제하지 않는다.',('miis','222.003 Data Sharing Objection; 222.105(B)'))
prop(21,True,'MIIS 72시간 보고','Routine administration은 72시간 이내 GUI 또는 data exchange로 보고한다. Stem의 routine facts에서 특별 기산점 예외는 제시되지 않았다.',('miis','222.100(A)'))
prop(22,True,'약사 선택·상담과 PT 투여','약사가 선택·상담하고 적격 PT가 준비·투여하는 역할 분리가 명시된 state policy와 일치한다.',('vaccine','III(D)(4)'))
prop(23,False,'VIS 시점','투여가 끝난 후 receipt와 함께 최초 VIS를 주는 것은 접종 전 제공 의무를 충족하지 않는다.',('vis','VISs are required by law'),('vaccine','IV(D)'))
prop(24,True,'PT licensure 후 경험','비인증 full PT는 licensure 이후 적어도 500시간 경험 경로를 이용할 수 있다. 다른 교육·감독·CPR 요건은 생략되지 않는다.',('vaccine','III(D)(1)(b); III(D)(2)-(4)'))
prop(25,False,'methadone OTP 경로','Circular의 addiction treatment including methadone order 경로는 registered OTP로 제한한다. Stem은 ordinary retail이며 별도 OTP authority를 제외했다.',('administration','Dispensing by Administration OTP note p.2'))
prop(26,False,'투여 고유 기록','보험청구만으로 consent·screening·제조사·lot·expiry·route/site·투여자 등 명시 항목을 모두 대체할 수 없다.',('administration','Record Keeping p.4'))
prop(27,False,'ceftriaxone IM/IV','Circular는 IV를 제외하고 ceftriaxone을 IM으로 열거한다. IM 권한으로 IV를 투여할 수 없다.',('administration','Dispensing (c); Eligible STI Medications p.2; Manufacturers Instructions p.3'))
prop(28,True,'single-dose 조건','Eligible medication은 single-dose packaging이고 single doses로 처방되어야 하며 refills 유무는 별도 조건이다.',('administration','Dispensing by Administration (d)'))
prop(29,False,'비백신 투여 인력','Circular의 수권 대상은 pharmacist와 pharmacy intern이다. Certified technician의 백신 권한을 LAI antipsychotic으로 확장하지 않는다.',('administration','Purpose; Dispensing by Administration pp.1-2'))
prop(30,False,'약물에 적합한 훈련','대상 약물·환자군·주사기술에 맞는 훈련과 continued competency가 요구된다. 오래된 vaccine course를 이유로 appropriate training 없이 시작할 근거가 없다.',('administration','Training; Continued Competency p.3'))
prop(31,True,'methadone OTP 제한 인식','Circular가 ordinary retail OUD methadone administration 권한을 새로 만들지 않는다는 범위 인식은 p.2의 OTP note와 일치한다.',('administration','OTP note p.2'))
prop(32,False,'주 eligible list와 REMS','주 eligible ingredient 목록은 specific medication의 manufacturer labeling 및 applicable REMS 준수를 면제하지 않는다.',('administration','Administration and Dosing Manufacturers Instructions p.3'))
prop(33,False,'투여와 독립 처방','이 circular는 valid prescription을 전제로 하는 administration 권한이다. Prescriber footnote도 별도 prescribing guidance를 지칭하며 투여 허가 자체가 독립 처방의 근거가 되지 않는다.',('administration','Purpose; Dispensing (b); footnote 1 p.1'))
prop(34,True,'적격 intern 투여','Circular는 적격 intern의 eligible adult IM medication administration을 허용한다. General intern supervision도 별도 적용된다.',('administration','Purpose; Dispensing pp.1-2; Training p.3'),('personnel','8.01(3)'))
prop(35,False,'serious adverse event 통지','Hospital/ED에서 추가 treatment/testing/monitoring이 필요한 outcome은 prescriber에게 즉시 보고해야 한다. Routine progress report까지 미루지 않는다.',('administration','Reporting Adverse Events (iv) p.4'))
prop(36,True,'buprenorphine 제품 조건','Eligible product의 labeling·applicable REMS를 따르는 것은 명시적 의무이다. 이 문구만으로 non-OTP에서 모든 OUD 투여가 허용된다고 결론 내리지 않는다.',('administration','Eligible SUD list p.2; Manufacturers Instructions p.3'),('sublocade','5.2'),('brixadi','5.2'))
prop(37,False,'일반 투여 연령','이 circular의 dispensing-by-administration 대상은 18세 이상이며 다른 lawful authority가 없다고 명시되었다. 16세 사례에 그대로 적용할 수 없다.',('administration','Dispensing by Administration p.1'))
prop(38,True,'administration/prescribing 구분','Valid prescription을 전제로 하는 투여 권한과 별도 independent prescribing 범위를 구별한다. 모든 HIV prevention regimen 처방권한을 이 circular에서 추론하지 않는다.',('administration','Purpose; Dispensing (b); footnote 1 p.1'))
prop(39,True,'ceftriaxone IM 투여','Eligible ceftriaxone IM route는 열거되어 있으며 SC/IM manufacturer instructions와 다른 stated conditions를 충족한다는 문항 사실에서 지지된다.',('administration','Eligible STI Medications p.2; Manufacturers Instructions p.3'))
prop(40,False,'single-dose 포장','Multidose supply라는 이유로 circular의 single-dose packaging 및 prescribed single doses 조건을 bypass할 수 없다.',('administration','Dispensing (d) p.2'))
prop(41,False,'CDTM 배상보험','모든 employer general-liability policy를 자동으로 충분하다고 볼 수 없다. CDTM을 특정 보장하는 professional liability가 건당 최소 100만 달러 필요하다.',('cdtm','16.02(1)(b)'))
prop(42,False,'CDTM 종료','연속 약물치료와 서면 환자 통지 없이 협업을 끝내는 것은 termination 조항에 맞지 않는다.',('cdtm','16.04(5)'))
prop(43,True,'retail 환자별 referral','Supervising physician의 written patient referral 및 primary/secondary diagnoses 정보는 retail CDTM 요건이다.',('cdtm','16.03(5)(c)(1)-(4); 16.04(1)'))
prop(44,False,'CPA 갱신','첫 서명으로 영구 면제되지 않는다. 약사·감독의사는 적어도 2년마다 review/renew 해야 한다.',('cdtm','16.04(4)'),('cdtm-statute','24B½(a) Collaborative practice agreement'))
prop(45,False,'동의·referral 보관','구두로 동의가 있다고 말하는 것은 양쪽 환자기록의 written referral/consent 및 copy 전달·보관을 대체하지 않는다.',('cdtm','16.03(5)(c)-(d); 16.04(6)'))
prop(46,False,'PharmD grandfather 경로','명시된 16.02 grandfather는 2017-06-30 이전 CPA 진입이 조건이므로 새 졸업자의 새 agreement에는 그 경로가 맞지 않는다. 다만 statute의 PharmD 대안과 규정 차이 때문에 해설의 일반 자격 결론은 HOLD한다.',('cdtm','16.02(1)(c)(1)-(2)'),('cdtm-statute','24B½(b)(3)'),('cdtm-equivalency','II; III'))
prop(47,True,'retail CDTM 성인','이 retail CDTM 경로는 18세 이상 환자이다. 별도 statewide prescribing 경로를 이 stem에 보태지 않는다.',('cdtm','16.03(5)(a)'),('cdtm-statute','24B½(c)'))
prop(48,False,'retail controlled prescribing 금지','Retail CPA는 Schedule II-V prescribing을 허용할 수 없다. Alprazolam은 Schedule IV이며 계약에 넣었다는 것만으로 제한을 해제하지 않는다.',('cdtm','16.03(5)(e)(3)-(4)'),('cdtm-statute','24B½(c)'),('schedule4-ecfr','1308.14(c)(2)'),('alprazolam-current','9.1 Controlled Substance'))
prop(49,True,'CDTM 전용 보험','CPA 기간에 drug therapy management를 특정 보장하는 professional liability를 건당 적어도 100만 달러 유지하는 것은 규정과 일치한다.',('cdtm','16.02(1)(b)'))
prop(50,False,'환자별 24시간 통지','Initial prescription/수정/중단 copy는 24시간 이내, 더 긴급하면 더 빨리 보낸다. 2년 CPA 갱신 때까지 기다리는 경로가 아니다.',('cdtm','16.03(5)(e)(2)'))
prop(51,False,'별도 contraception과 CDTM','Contraception prescribing의 별도 범위를 CDTM 성인 요건의 면제로 옮기지 않는다. Stem은 retail CDTM 경로로 제한되어 있다.',('cdtm','16.03(5)(a)'),('contraception-law','19F(a)-(c)'))
prop(52,False,'monitoring과 diagnosis','CDTM은 drug therapy 관련 laboratory evaluation을 포함할 수 있지만 독립 diagnostic component를 포함하지 않는다.',('cdtm-statute','24B½(a) Collaborative drug therapy management'))
prop(53,True,'치료 연속성과 종료 통지','종료 전 uninterrupted continuation을 마련하고 종료/비갱신 시 환자에게 서면으로 절차를 알린다. 사전에 서면통지까지 준비하는 행위는 지지되며 더 늦은 notice가 허용된다고 가르치지 않는다.',('cdtm','16.04(5)'))
prop(54,False,'환자별 referral 대체 금지','매장 일반 signup은 supervising physician의 특정 환자에 대한 written referral·diagnosis를 대신하지 못한다.',('cdtm','16.03(5)(c); 16.04(1)'))
prop(55,True,'adult referral Schedule VI 범위','Adult referred patient를 current signed CPA 및 authorized Schedule VI 범위에서 관리한다는 제한된 행위는 지지된다. 모든 진단·약물을 포괄한다고 확대하지 않는다.',('cdtm','16.03(5)(a),(c)-(e); 16.04(1)'))
prop(56,True,'consent 원본·사본','Physician이 original consent를 보관하고 pharmacist가 요구 사본을 받아 보관하는 record 경로와 일치한다.',('cdtm','16.03(5)(d)(1)-(3); 16.04(6)'))
prop(57,True,'24시간 내 prescription copy','Initial prescription/therapy modification을 supervising physician에게 24시간 내 전송하고 더 긴급하면 앞당기는 것은 규정에 맞는다. Copy 및 medical-record 요구는 all other prerequisites로 남는다.',('cdtm','16.03(5)(e)(2)'))
prop(58,True,'약물 관련 검사 범위','Drug-therapy-linked lab monitoring을 정의하고 독립 diagnosis를 부여하지 않는 경계가 statutory definition과 일치한다.',('cdtm-statute','24B½(a) Collaborative drug therapy management'))
prop(59,False,'보험과 처방 권한','Plan coverage는 해당 법률의 약사 처방 범위를 확장하지 않는다. 19F의 oral/patch 권한만으로 injection 처방권한이 생기지 않는다.',('contraception-law','19F(a)-(c)'))
prop(60,False,'EC 별도 연간 보고','일반 controlled-prescription PMP file 전송으로 standing-order EC 연간 보고를 생략할 수 없다. EC는 별도 annual count requirement이다.',('ec-statute-19a','19A(e)'),('ec-pharmacy','Reporting requirement'))
prop(61,False,'EC standing order 한계','Standing order가 지정한 EC 및 assessment/dispensing 경로를 모든 reproductive-health drug의 independent prescribing으로 확대하지 않는다.',('ec-order','ECP Order steps 1-5'),('ec-statute-19a','19A(a)-(c)'))
prop(62,True,'실제 EC 사용자 평가','이 statewide order 이용 시 사용자 본인을 in-person 또는 phone으로 평가한다. OTC EC를 제3자가 구매하는 별도 경로와 구분된다.',('ec-pharmacy','FAQ dispense EC for someone other than themselves'),('ec-order','Order steps 1-2'))
prop(63,False,'rescue kit 상담·정보지','Label은 9.06(3)의 counseling 및 information pamphlet을 대체하지 않는다. Outer label/expiry는 별도 9.06(5) 조건이다.',('practice','9.06(3),(5)'),('naloxone-policy','I(A),(G)'))
prop(64,False,'OTC와 insurance','OTC-labeled naloxone은 일반 소매 경로가 있으며 insurance billing의 prescription 취급을 현금 OTC 법적 구매 조건으로 옮길 근거가 없다. 판매자 일반 재량까지 판단하지 않는다.',('naloxone-otc','Access options; Cost and coverage'),('opioid-antagonist-law','19B(e)'),('naloxone-policy','Introduction'))
prop(65,True,'UPA Rx와 LNG OTC','현재 ella label은 HUMAN PRESCRIPTION DRUG/Rx only이고 Plan B One-Step은 OTC이다. 목적만 같다고 status를 옮기지 않는다.',('ella-current','Product Information; Rx only carton'),('planb','Opening product status; 2013 OTC approval'))
prop(66,False,'빈 template과 발행 order','아무 prescriber도 서명하지 않은 model은 실제 발행된 standing order가 아니다. 문항이 특정 statewide order 자체를 부정하는 것으로 읽지 않는다.',('ec-order','Authorizing Physician signature; Order steps 1-5'),('opioid-antagonist-law','19B(b)-(c)'))
prop(67,True,'EC annual tracking','EC 연간 보고에 필요한 추적 기록과 일반 dispensing 기록을 구별해 유지하는 행위는 지지된다. 법이 독립 database나 중복 종이 장부를 필수로 한다는 뜻은 아니다.',('ec-statute-19a','19A(e)'),('ec-pharmacy','Reporting requirement; patient-specific prescription FAQ'),('practice','9.16(1)'))
prop(68,False,'UPA 무처방 판매','현재 Rx-only ella를 LNG OTC status만을 이유로 order 없이 판매할 수 없다. 유효 statewide standing order 경로도 여기서는 사용하지 않았다고 명시했다.',('ella-current','Product Information; Rx only carton'),('planb','Opening product status'))
prop(69,False,'EC 사용자 assessment 누락','Standing-order patient-specific prescription은 실제 사용자 assessment가 선행되어야 한다. Absent user에 대해 필수 평가 없이 생성하는 행위는 지지되지 않는다.',('ec-pharmacy','FAQ dispensing for another person'),('ec-order','Order steps 1-2'))
prop(70,False,'daily Opill과 EC','Opill은 daily norgestrel이며 FDA가 EC 사용이 아니라고 명시한다. 사용 목적 확인 없이 EC 요청에 자동 대체하지 않는다.',('opill','Opill is not for use as emergency contraception'))
prop(71,True,'coverage와 modality 구분','보험 covered-product 범위와 법적으로 허용된 prescribing modality를 별개로 판단한다. 특정 plan의 구체 보장 범위를 이 문항에서 새로 확정하지 않는다.',('contraception-law','19F(a)-(c)'),('ec-pharmacy','FAQ insurance coverage'))
prop(72,True,'재고 미보유 referral','요청 시 stock이 없으면 해당 opioid antagonist가 실제 준비된 가장 가까운 곳으로 안내한다. Continuous stocking obligation을 면제한다는 의미는 아니다.',('practice','9.06(4)'))
prop(73,False,'access referral 누락','요청 약을 보유하지 않은 pharmacy는 nearest-available location referral을 해야 하므로 아무 안내 없이 encounter를 끝내는 것은 맞지 않는다.',('practice','9.06(4)'))
prop(74,True,'standing order 확인','해당 patient-specific dispensing pathway에 실제 적용되는 standing order를 확인한다. Blank template와 실제 signed order를 동일시하지 않는다.',('ec-order','Authorizing Physician signature; Order steps 1-5'),('opioid-antagonist-law','19B(b)-(c)'))
prop(75,True,'current product REMS 확인','REMS 유무·현행 요건은 개별 프로그램을 확인한다. Boxed warning 자체는 enrollment program 존재와 같지 않다.',('boxed-rems-faq','How FDA determines need; Current REMS'),('clozapine','What Is FDA Doing'))
prop(76,False,'mifepristone federal certification','State access protection으로 federal REMS pharmacy certification을 자동 제거할 수 없다. FDA current pathway는 certified pharmacy/prescriber 조건을 유지한다.',('mifepristone','The Mifepristone REMS Program prescribing/dispensing restrictions'))
prop(77,False,'REMS 폐지와 ANC','REMS 행정 enrollment/reporting 제거는 clozapine neutropenia 위험 또는 label-based ANC monitoring 권고 제거가 아니다. Pharmacist의 REMS ANC verification 의무가 남았다는 주장도 하지 않는다.',('clozapine','What Is FDA Doing; What Should Health Care Professionals Do'))
prop(78,False,'Spravato setting','Nasal route의 일반 self-administration 관행은 certified setting·direct observation·monitoring의 REMS 요건을 대체하지 않는다.',('spravato','5.5; 2.1'))
prop(79,False,'Brixadi formulation','Weekly/monthly는 서로 다른 formulation·interval이다. Label상 임상 판단에 따른 용량 전환표가 있으며 active ingredient 동일성만으로 ordered formulation을 확인 없이 교환할 수 없다.',('brixadi','2.1; 2.3 weekly/monthly transitions'))
prop(80,False,'TIRF와 patch','TIRF 범위는 특정 transmucosal immediate-release 제품이며 fentanyl patch가 아니다. 더구나 신규 enrollment 중단이 공지되어 있으므로 현재 신규등록 절차가 열려 있다고 전제하지 않는다.',('tirf','September 16 2024 notice; TIRF product list'))

texts=[]
for r in PACKET['records']:
 for c in r['original_visible_content']['choices']:
  if c['text'] not in texts:texts.append(c['text'])
assert len(texts)==80 and set(P)==set(range(1,81))
PROPS={t:dict(proposition_id=f'G-P{i:03}',option_text=t,**P[i]) for i,t in enumerate(texts,1)}
write(BASE/'independent-proposition-findings.json',dict(actual_actor=ACTOR,reviewed_at=DATE,method_ko='80개 고유 보기를 안전 packet에서 그대로 식별하고 이 실제 세션에서 공식 원문에 독립 대조했다. 번호는 첫 출현 순서일 뿐 기존 truth나 저자 결론에서 추출하지 않았다.',propositions=list(PROPS.values())))

nearest=json.load(open(BASE/'nearest-comparisons.json'))
NEAR={r['question_id']:r for r in nearest['comparisons']}
family=json.load(open(BASE/'assigned-family-map.json'))
selection_path='practice_expansion/2026-10-28-representative/selection.json'
recommended=set(json.load(open(ROOT/selection_path))['recommended_ids'])
assert not recommended & set(ASSIGN['question_hashes'])

policy_names=['INDEPENDENT_LEGACY_REVIEW_RUNBOOK','RELEASE_POLICY','AUDIT_WORKFLOW','SOURCE_USE_POLICY','QUESTION_AUTHORING_STANDARD']
policy_snapshot=[]
for name in policy_names:
 f=pathlib.Path('docs')/(name+'.md')
 assert (ROOT/f).read_bytes()==(pathlib.Path('/workspace/oddments')/f).read_bytes()
 policy_snapshot.append(dict(path=str(f),file_sha256=sha(ROOT/f),root_copy_same_bytes=True))
sys.path.insert(0,str(ROOT/'scripts'))
from qa_common import semantic_content_hash
sp_path='data/exam_style/mpje_style_profile.json';sp=json.load(open(ROOT/sp_path))
style=dict(path=sp_path,profile_id=sp['profile_id'],content_version=sp['content_version'],semantic_hash=semantic_content_hash(sp,'style_profile'),stored_semantic_hash=sp['content_hash'],file_sha256=sha(ROOT/sp_path),schema_path='schemas/exam_style_profile.schema.json',schema_file_sha256=sha(ROOT/'schemas/exam_style_profile.schema.json'))
assert style['semantic_hash']==style['stored_semantic_hash']

# An individualized wording example is chosen from the actual four options in
# each question. FAIL is grounded in those words and independent work records,
# not item count, numbers, similarity score, or archived variants alone.
CUES={
 'MA-CASE-0481':('B','프로그램 존재도 확인하기 전 enrollment를 요구한다'),
 'MA-CASE-0522':('A','빈 allergy field를 문의 없이 NKA로 확정한다'),
 'MA-CASE-0523':('B','required MIIS check를 다른 백신 예외로 생략한다고 직접 쓴다'),
 'MA-CASE-0524':('C','trainee 시간으로 post-licensure 경로를 충족한다는 문언 자체가 모순이다'),
 'MA-CASE-0525':('B','national certification 하나가 training·CPR·supervision을 대체한다고 쓴다'),
 'MA-CASE-0526':('B','응급약을 포괄하는 order가 없는데 투약한다고 직접 명시한다'),
 'MA-CASE-0527':('B','정기 보고를 monthly billing까지 미룬다고 명시한다'),
 'MA-CASE-0528':('B','환자의 공유 이의 때문에 reporting obligation을 삭제한다고 쓴다'),
 'MA-CASE-0529':('C','expired CPR를 유지한 채 초기 교육만 의존한다고 쓴다'),
 'MA-CASE-0530':('C','해당 emergency medication order가 없다고 직접 밝힌다'),
 'MA-CASE-0531':('A','접종이 끝난 후에만 VIS를 준다고 쓴다'),
 'MA-CASE-0532':('B','보험청구만 남기고 administration-specific records를 omits한다고 쓴다'),
 'MA-CASE-0533':('D','applicable REMS를 ignores한다고 직접 쓴다'),
 'MA-CASE-0534':('C','administration-specific records를 omits한다고 쓴다'),
 'MA-CASE-0535':('A','ED monitoring 사건 후에도 다음 routine report까지 기다린다고 쓴다'),
 'MA-CASE-0536':('B','applicable REMS를 ignores한다고 직접 쓴다'),
 'MA-CASE-0537':('A','medication-appropriate training 없이 투여를 시작한다고 쓴다'),
 'MA-CASE-0538':('C','applicable REMS를 ignores한다고 직접 쓴다'),
 'MA-CASE-0539':('D','single-dose requirement를 bypassing한다고 직접 쓴다'),
 'MA-CASE-0540':('B','single-dose packaging requirement를 bypassing한다고 쓴다'),
 'MA-CASE-0541':('B','치료에 의존하는 환자를 알리지 않고 종료한다고 쓴다'),
 'MA-CASE-0542':('A','required referral/consent records 대신 verbal statement만 둔다'),
 'MA-CASE-0543':('C','required records를 verbal statement로 대체한다고 쓴다'),
 'MA-CASE-0544':('B','unrestricted authority로 independent diagnoses를 부여한다고 쓴다'),
 'MA-CASE-0545':('C','환자 치료변경 통지를 next biennial review까지 미룬다고 쓴다'),
 'MA-CASE-0546':('B','환자를 알리지 않고 collaboration을 끝낸다고 쓴다'),
 'MA-CASE-0547':('D','initial signatures 이후 no later renewal이라고 직접 쓴다'),
 'MA-CASE-0548':('A','required consent records를 verbal statement로 대체한다고 쓴다'),
 'MA-CASE-0549':('B','CPA가 permanent하며 no later renewal이라고 직접 쓴다'),
 'MA-CASE-0550':('C','EC 참여를 any reproductive-health drug의 일반 처방권한으로 쓴다'),
 'MA-CASE-0551':('D','blank template를 signed order로 취급한다고 직접 쓴다'),
 'MA-CASE-0552':('B','prescription-only 제품을 without an order로 판매한다고 명시한다'),
 'MA-CASE-0553':('C','required patient assessment 없이 생성한다고 명시한다'),
 'MA-CASE-0554':('B','blank template를 signed order로 취급한다고 명시한다'),
 'MA-CASE-0555':('C','required access referral 없이 끝낸다고 명시한다'),
 'MA-CASE-0556':('D','prescription-only 제품을 without an order로 판매한다고 명시한다'),
 'MA-CASE-0557':('C','required patient assessment 없이 생성한다고 명시한다'),
 'MA-CASE-0558':('B','required patient assessment 없이 생성한다고 명시한다'),
 'MA-CASE-0559':('C','REMS 제거가 label-based monitoring 필요도 제거했다고 단정한다'),
 'MA-CASE-0560':('C','두 formulation을 성분만 같다는 이유로 without clarification 교환한다고 쓴다'),
}
records=[]
for row in PACKET['records']:
 q=row['original_visible_content'];qid=row['question_id']
 assert row['record_sha256']==ASSIGN['question_hashes'][qid]
 choices=[]
 for c in q['choices']:
  pp=PROPS[c['text']]
  choices.append(dict(choice_id=c['id'],option_text=c['text'],option_text_sha256=hashlib.sha256(c['text'].encode()).hexdigest(),proposition_id=pp['proposition_id'],supported=pp['supported'],assessment_status='ASSESSED_NAMED_ACTION_AND_STATED_PATHWAY',subject_condition_exception_review_ko=pp['finding_ko'],authorities=pp['authorities'],original_rationale_read=True,original_rationale_sha256=hashlib.sha256(q['explanation']['choice_analysis'][c['id']].encode()).hexdigest(),original_rationale_assessment='AMBIGUOUS_GENERAL_QUALIFICATION_STATEMENT' if pp['proposition_id']=='G-P046' else 'CONSISTENT_WITH_STATED_SCOPE',original_rationale_finding_ko=pp['finding_ko']))
 expected=[c['choice_id'] for c in choices if c['supported']=='YES']
 assert len(expected)==1 and expected==q['correct_choice_ids']
 auth=[];seen=set()
 for c in choices:
  for a in c['authorities']:
   key=(a['source_id'],a['exact_section'])
   if key not in seen:auth.append(a);seen.add(key)
 topics=[PROPS[c['text']]['topic_ko'] for c in q['choices']]
 correct=next(c for c in q['choices'] if c['id']==expected[0])
 ci,cue=CUES[qid]
 cue_option=next(c['text'] for c in q['choices'] if c['id']==ci)
 n=NEAR[qid];can=n['canonical_nearest'];pub=n['public_nearest'];other=n['public_nearest_other_family']
 own_set={c['text'] for c in q['choices']}
 pub_set={c['text'] for c in pub['full_stem_and_all_options']['choices']}
 shared=sorted(own_set&pub_set)
 # Distinctness is a constrained YES for archive practice: nearest comparisons
 # were actually read, and none of these assigned IDs is in the default pool.
 # Their clause reuse is recorded, not treated as independently novel coverage.
 duplicate=dict(status='RUN_AND_MANUALLY_READ',evidence_path=str((BASE/'nearest-comparisons.json').relative_to(ROOT)),evidence_sha256=sha(BASE/'nearest-comparisons.json'),canonical_count=439,public_count=2346,canonical_nearest={k:can[k] for k in ['question_id','family_id','cosine']},public_nearest={k:pub[k] for k in ['question_id','family_id','cosine']},public_nearest_other_family={k:other[k] for k in ['question_id','family_id','cosine']},canonical_full_stem_and_all_options_read=True,public_full_stem_and_all_options_read=True,public_other_family_full_stem_and_all_options_read=True,shared_verbatim_option_count=len(shared),shared_verbatim_options=shared,default_pool_member=False,comparison_finding_ko=f"Canonical 최근접 {can['question_id']}의 전체 stem와 모든 보기를 읽었다. 그 문항은 '{can['full_stem_and_all_options']['stem'][:155]}'라는 구체 질문이며 본 문항은 {', '.join(topics)}를 별도 기록으로 판별한다. Public 최근접 {pub['question_id']}와 실제 보기 문장 {len(shared)}개를 공유하고, 다른 family 최근접 {other['question_id']}도 읽었다. 점수나 archived 변형 존재만으로 FAIL하지 않았다. 기본 추천에 포함되지 않는 연습 변형으로서 동일 조항 반복을 명시해 허용하되 독립 coverage나 새 법규라고 세지 않는다. 현재 FAIL 근거는 아래의 실제 문언 cue 및 비결합 판단 구조이다.")
 criteria=dict(jurisprudence_reasoning=True,practice_plausibility=True,authentic_distractors=True,wording_not_guessable=False,reasoning_not_trivia=True,natural_rule_combination=False,appropriate_drug_context=True,distinct_from_bank=True,not_schedule_flashcard=True,public_style_without_copying=True)
 criteria_reasons=dict(
  jurisprudence_reasoning=f"{', '.join(topics)}에서 주체·시점·법적 경로 중 적어도 하나의 실제 법규 판단은 필요하다. 단일정답 {expected[0]}의 행위는 공식 조항에 대조했다.",
  practice_plausibility=f"Pharmacy service의 compliance/work-queue 확인이라는 운영 상황 자체는 가능하다. {PROPS[correct['text']]['topic_ko']}를 확인하는 실제 약사 업무에 연결되지만 개별 환자의 수치·약력 사례는 주어지지 않았다.",
  authentic_distractors=f"{', '.join(topics)}의 혼동은 실제 교육·권한·절차를 혼동하는 유형으로 식별된다. 다만 아래의 노골적 표현은 난이도를 떨어뜨리므로 distractor 주제의 진정성만 인정한다.",
  wording_not_guessable=f"보기 {ci}는 {cue}. 실제 문장: {cue_option} 정답 {expected[0]} '{correct['text']}'는 조건 확인·규정 준수 행위로 대비되어, 모르는 조항을 계산하기 전에도 안전한 문장 태도를 통해 고르기 쉽다.",
  reasoning_not_trivia=f"{PROPS[correct['text']]['topic_ko']}는 실제 permitted/required 범위를 가르는 최소 1개 jurisprudence determination이다. 숫자 유무 또는 짧은 조항 확인만으로 trivia FAIL을 주지 않았다. 다만 문언 cue가 그 판단의 측정력을 약화한다.",
  natural_rule_combination=f"Stem이 각 보기를 separate work-queue record로 선언한다. {', '.join(topics)}는 같은 한 사례의 선행조건·예외·결과로 연결되지 않고 각자 참/거짓을 독립 결정한다. 같은 서비스 주제라는 공통점만으로 rule interaction이 확인되었다고 보지 않는다.",
  appropriate_drug_context=f"{', '.join(topics)}에 쓰인 약물·백신·제도 이름은 해당 권한/제품 경로를 판별하는 데 연결된다. 약물이 구체적으로 없는 보기는 인력·서류·보고 의무를 직접 다루므로 불필요한 약명 장식을 요구하지 않는다.",
  distinct_from_bank=f"{can['question_id']}, {pub['question_id']}, {other['question_id']}의 실제 전체 문항을 비교했다. Public 최근접과 literal 보기 {len(shared)}개를 공유하지만 이 ID는 현재 default pool 밖이며 learning_boundary가 연습 변형임을 명시한다. 이 제한된 archive 연습 맥락에서 반복 자체로 FAIL하지 않았다. 독립 새 법규/독립 문제 coverage로 인정하는 판정은 아니다.",
  not_schedule_flashcard=f"{', '.join(topics)}에 대한 업무 처리의 적법성 질문이며 단순 약물 schedule 이름만 묻는 문항이 아니다.",
  public_style_without_copying="지정 NABP public sample PDF의 실제 raw SHA를 확인하고 전 페이지 text와 세 응답 형식을 직접 읽었다. 이 문항은 SBA 한 개 선택 형식이며 sample 질문의 stem·보기 wording을 복제하지 않았다. Sample은 내용 대표성/법률 근거가 아니라 형식만 제시한다고 명시한다. Private Pre-MPJE·recall·commercial bank는 사용하지 않았다.")
 hold=qid in {'MA-CASE-0542','MA-CASE-0545'}
 conflict='247 CMR16.02(1)(c)의 pre-2017 PharmD grandfather와 현행 c.112 §24B½(b)(3)의 더 넓은 PharmD 대안 사이의 법적 관계가 원문만으로 해결되지 않았다. 명시된 grandfather 경로는 맞지 않지만 원래 한국어 해설의 새 졸업자 일반 자격 제한까지 확정하지 않는다.' if hold else None
 core_find='Core와 A-D 해설을 전문 읽고 해당 보기에 배정된 조항 및 문항에 명시된 pathway에 대조했다. 별도 기록의 단일정답 조합은 유지된다. 허용 행위를 필수 전체 workflow라고 확대하거나 원문에 없는 예외를 보태지 않았다.'
 if hold:core_find+=' '+conflict
 if qid in {'MA-CASE-0535','MA-CASE-0537'}:core_find+=' Buprenorphine 보기는 labeling/REMS 준수라는 좁은 행위만 인정한다. Circular의 eligible list와 OTP note 사이 문언을 일반 retail OUD administration 허가로 확대하지 않았다.'
 if qid in {'MA-CASE-0550','MA-CASE-0552','MA-CASE-0554','MA-CASE-0555','MA-CASE-0557','MA-CASE-0558'}:core_find+=' EC의 separate records는 별도 annual-report tracking을 말하며 별도 database/중복 장부가 법적으로 강제된다는 뜻으로 읽지 않았다.'
 records.append(dict(question_id=qid,record_sha256=row['record_sha256'],visible_content_sha256=row['visible_content_sha256'],family_id=family[qid],collection='plus-20261026',read_scope=dict(input_path=str(INPUT),input_raw_sha256=sha(INPUT),original_stem_read_in_full=True,all_choices_read_in_full=True,choice_count=len(q['choices']),stored_key_read=True,complete_core_korean_explanation_read=True,all_choice_korean_explanations_read=True,learning_boundary_read=True,hidden_truth_or_prior_decision_read=False),legal_review=dict(existing_answer_correct='YES',stored_key=q['correct_choice_ids'],independently_expected_key=expected,polarity='SUPPORTED_ACTION_SBA',sata_combination='NOT_APPLICABLE_SBA',uniqueness_review_ko=f"보이는 네 선택지의 stated action을 따로 검증했다. 지지되는 항목은 {expected[0]} 하나이고 원래 key와 일치한다. INCORRECT 극성이 아니며 SATA 조합 문제가 아니다.",per_choice_findings=choices,authorities=auth,verdict='HOLD' if hold else 'KEEP',finding_ko=core_find,blocker=conflict,original_explanation_review=dict(core_read_in_full=True,core_sha256=hashlib.sha256(q['explanation']['core_reasoning'].encode()).hexdigest(),core_assessment='AMBIGUOUS' if hold else 'CONSISTENT_WITH_STATED_SCOPE',all_choice_explanations_read_in_full=True,all_choice_assessments=[dict(choice_id=c['choice_id'],rationale_sha256=c['original_rationale_sha256'],assessment=c['original_rationale_assessment'],finding_ko=c['original_rationale_finding_ko']) for c in choices],learning_boundary_assessment_ko='전체 learning_boundary를 읽었다. 9개 조건·기록 연습 변형이고 실제 기출/9개 독립 법규로 세지 않는다는 편집 한계를 유지한다.',finding_ko=core_find)),realism_review=dict(verdict='FAIL',decision='MAJOR_REWRITE',criteria=criteria,criterion_findings_ko=criteria_reasons,duplicate_evidence=duplicate,finding_ko=f"보기 {ci}의 '{cue}'라는 실제 표현이 정답의 안전한 태도를 드러내고, separate records는 조항들을 하나의 사건 판단으로 결합하지 않는다. 숫자·archived variant·자동 similarity만으로 실패시킨 결과가 아니다."),safe_hold_recommended=True,release_eligible=False,required_next_action_ko=('현재 원문은 보류한다. 자격 설명의 statute/regulation 관계를 공식 Board clarification 또는 적법한 별도 검토로 해결하고, 실제 동일 환자/업무 기록의 조건·예외가 상호작용하도록 편집한 새 hash를 fresh 감사한다.' if hold else '현재 원문을 release 근거로 쓰지 않는다. 정답·오답을 드러내는 생략/무시 표현을 실제 경쟁 법규 판단으로 바꾸고, 조건이 상호작용하는 한 사례로 편집한 새 hash를 fresh 감사한다.'),canonical_audit=False,canonical_release_credit=0))

assert set(r['question_id'] for r in records)==set(ASSIGN['question_hashes'])
excluded=[]
for sid,reason in [('boxed-rems','공식 URL 직접 조회가 read timeout으로 완료되지 않았다. 올바른 FDA FAQ와 clozapine 문서로 대체했으며 timeout을 verification으로 세지 않는다.'),('ella','HTTP200이지만 DailyMed home/index로 redirect되어 요청 제품 라벨이 아니다. WRONG_DOCUMENT로 거부하고 공식 API로 발견한 현재 ELLA setid를 직접 조회·본문 확인했다.'),('ec-statute','HTTP200의 유효한 c94C §19D 원문이지만 opiate 7-day supply 조항으로 EC report 근거가 아니다. IRRELEVANT_WRONG_SECTION으로 거부하고 정확한 §19A를 새로 읽었다.'),('ella-label','2021 FDA archived label은 제품 identity만 참고했다. 문서 자체가 최신 label이 아닐 수 있다고 명시하므로 현행 Rx status 근거에는 2026 DailyMed current label을 사용했다.'),('alprazolam-schedule','GovInfo는 HTTP200이지만 Page Not Found 본문이었다. §1308.14 확인으로 세지 않고 올바른 eCFR current와 현재 Xanax label로 교체했다.'),('schedule4-api','eCFR API는 HTTP406으로 실패했다. 성공한 public current eCFR 원문을 별도로 직접 읽었다.'),('alprazolam-label','추측한 setid는 HTTP200 DailyMed home으로 redirect되어 요청 라벨이 아니었다. 성공으로 세지 않고 official API에서 찾은 XANAX setid로 새로 읽었다.')]:
 m=json.load(open(BASE/(sid+'-retrieval.json')));m['used_for_legal_verification']=False;m['rejection_reason_ko']=reason;write(BASE/(sid+'-retrieval.json'),m);excluded.append(m)
source_register=dict(actor_id=ACTOR,session_id=ACTOR,checked_date=DATE,network_ko='Cloud environment status는 unrestricted/enforced였다. 환경 networking skill을 읽고 /etc/codex/network-policy.json을 확인했다. urllib는 상속된 proxy와 기본 TLS 검증을 유지했다. 성공 status만으로 verified라 선언하지 않고 각 문서 제목·약물/조항과 선택된 본문을 직접 읽었다.',firecrawl_attempt=dict(status='NOT_RUN_INSUFFICIENT_CREDITS',query='site.mass.gov "26-03-124" "pharmacist"',error_ko='Connected-app search가 daily/team credit 부족으로 실행되지 않았으며 같은 call을 반복하지 않았다. 공식 직접 HTTP 조회로 이어갔다.'),sources=sources,excluded_attempts=excluded,nabp_style=json.load(open(BASE/'nabp-style-reread.json')),source_limitations_ko=['문서 전체의 최초 시행일 또는 모든 amendment history를 확정하지 않았다. 각 selected provision의 version과 null commencement 한계를 기록했다.','Nov3 live snapshots를 Oct26 REMS stem에 적용할 때 해당 제품 label update와 공표일이 Oct26 이전인지 확인했다. iPLEDGE Nov15 future modification은 적용하지 않았다.','NABP live403은 유지하고, 지정된 same-day raw PDF 재독을 새 live retrieval로 쓰지 않았다.',f'{len(sources)}개 selected source의 원문 판독은 실제 이 actor/session의 업무 이력이다. independent_of_authors Boolean 하나가 독립성을 증명한다고 주장하지 않는다.','USP private full raw나 commercial/recall/Pre-MPJE는 열람·보관·공개하지 않았다.'])
write(BASE/'source-register.json',source_register)
counter=dict(total=40,complete_visible_reads=40,legal_answer_yes=sum(r['legal_review']['existing_answer_correct']=='YES' for r in records),legal_verdict=dict(collections.Counter(r['legal_review']['verdict'] for r in records)),realism_verdict=dict(collections.Counter(r['realism_review']['verdict'] for r in records)),safe_hold_recommended=40,release_eligible=0,canonical_release_credit=0,unique_option_propositions=80,official_sources_used=len(sources),assigned_in_default_pool=0)
report=dict(schema_version='independent-legacy-review/1',stage='independent-legacy',independent_of_authors=True,auditor='GPT',auditor_instance=INSTANCE,actor_provenance=dict(actor_id=ACTOR,session_id=ACTOR,actual_session_continuity_ko='Capacity 재개 요청 후 같은 canonical task/session에서 계속했다. 파일마다 새 독립 instance를 만들지 않았다.'),canonical_audit=False,canonical_release_credit=0,reviewed_at=DATE,question_hashes=ASSIGN['question_hashes'],input_evidence=dict(path=str(INPUT),raw_sha256=sha(INPUT),scope='Only original_visible_content plus assigned binding hashes; no hidden statement truth, ledger rows or prior author/independent conclusions were opened.'),independence_history_ko='이 실제 fresh session은 지정 안전 packet의 원문 stem·모든 보기·key·core와 모든 한국어 해설을 직접 읽었다. Root가 제공한 운영 계약 및 sample cache provenance 외 기존 평가 결론을 상속하지 않았다. 원본 전체 객체는 hash·safe projection 코드 입력으로만 처리했고 전체 출력/숨은 truth/원장 행은 보지 않았다. Comparison candidates는 full stem/all options만 safe projection으로 읽었다.',policy_snapshot=policy_snapshot,style_profile=style,default_pool_snapshot=dict(path=selection_path,file_sha256=sha(ROOT/selection_path),checked_fields_only=['recommended_ids'],assigned_in_recommended=[],finding_ko='현재 기본추천 ID 집합과 지정40의 교집합은 0이다. 기존 holds/archive review notices의 판정은 열지 않았다.'),sources=sources,source_register_path=str((BASE/'source-register.json').relative_to(ROOT)),source_register_sha256=sha(BASE/'source-register.json'),excluded_source_attempts=excluded,counters=counter,records=records,limitations_ko=['이 보고서는 independent legacy assessment이며 canonical audit 또는 RELEASED admission이 아니다.','정답 key 일치와 해설 전체의 법적 확정은 별개이다. 0542/0545의 자격 설명은 현행 statute/regulation 문언 차이 때문에 HOLD다.','현실성 40 FAIL은 실제 보기 문언 cue와 별도-record 구조에 근거한다. 반복·숫자·archived variant 존재 또는 similarity 수치만으로 실패시키지 않았다.','Rule interaction을 요구하는 current style profile에 따른 판단이다. NABP 공개 sample은 응답 형식만 참고했으며 실제 시험의 내용/난이도를 인증하지 않는다.','원문·key·notes·data·governance·공유 queue/generated를 수정하지 않았다. Root가 실제 manifest submit/integration을 수행해야 한다.'])
report['schema_snapshot']=[dict(path=f,schema_id=json.load(open(ROOT/f)).get('$id'),json_schema_dialect=json.load(open(ROOT/f)).get('$schema'),file_sha256=sha(ROOT/f),usage='Context snapshot only; this report is not a canonical audit/question record and does not claim canonical schema admission') for f in ['schemas/audit.schema.json','schemas/question.schema.json','schemas/exam_style_profile.schema.json']]
write(REPORT,report)
print(json.dumps(dict(report=str(REPORT),report_sha256=sha(REPORT),counters=counter),ensure_ascii=False,indent=2))
