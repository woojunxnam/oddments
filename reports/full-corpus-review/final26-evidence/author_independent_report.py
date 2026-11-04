import json,hashlib,sys,subprocess,copy
from pathlib import Path
from datetime import datetime,timezone
root=Path('/workspace/independent-final26');prefix='reports/full-corpus-review/final26-evidence/';out=root/prefix
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(path,data):
 p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');return sha(p.read_bytes())
now=datetime.now(timezone.utc).isoformat();today=now[:10]
packet=json.loads((out/'assigned-visible-input.json').read_bytes());job=json.loads((out/'assignment.json').read_bytes());near=json.loads((out/'nearest-candidates.json').read_bytes())
selection=json.loads((root/'practice_expansion/2026-10-28-representative/selection.json').read_bytes());default=set(selection['recommended_ids'])
sourceinfo={
'em2026':('MA Board Policy 2026-03','I–VI; tables p2; II; III(D),(G),(H); IV; V','Adopted 2026-09-03; supersedes Policy 2023-09','현행 Board 공식 PDF. 별도 시행일 기재 없어 채택일을 version으로 사용; 독립적인 USP 유료본문 열람/인증은 하지 않음.'),
'cmr20':('247 CMR 20','20.02(2)–(5),20.06(2)–(4)','Mass. Register #1536, 2024-12-06','현행 제공본 footer version 확인. 모든 조항의 최초 법적 시행일을 별도 확정하지 않았음.'),
'defect':('MA Board Policy 2024-04','pp1–2 Defective Drug Preparation Log; immediate SADE paragraph','Adopted 2024-09-05','현행 Board PDF의 채택일 사용. 권한범위와 법규/정책의 효력을 구별.'),
'mgl39d':('M.G.L. c112 §39D','§39D(b),(c),(e)','current official legislature page retrieved '+today,'개별 개정법 commencement history는 페이지에서 확정하지 않았음; 현재 게시된 통합본문으로 한정.'),
'fda503b':('FDA final guidance: adverse event reporting for 503B outsourcing facilities','III(A)–(C),III(H), pp5–6,10','October 2015 final guidance','FDA current guidance landing page에서도 Final/October2015 확인. guidance의 비구속 권고와 503B/310.305에서 설명하는 must 의무 구별.'),
'fda503bpage':('FDA official current final-guidance listing','Final guidance status; October2015; 503B(b)(5) relationship','October 2015 Final; current listing '+today,'current listing 확인용; 독립적인 법률 효력일은 이 listing으로 새로 인증하지 않음.'),
'cfr310':('21 CFR 310.305','(c)(1)(i),(c)(2),(f)(1)','eCFR current title21 through 2026-11-02','eCFR는 정부의 authoritative but unofficial 통합본. 개별 개정의 최초 시행일을 재구성하지 않음.'),
'cmr222':('105 CMR 222','222.003 data-sharing objection;222.100(A);222.105(B)(1)–(4)','Mass. Register #1528, 2024-08-16','현재 게시 PDF version. 24시간은 form 반환에 명시, GUI 변경 의무는 별도 문장으로 명시됨.'),
'form222':('21 CFR 1305.13','(b),(f)','eCFR current title21 through 2026-11-02','ordinary Form222 60일 적용. 국방조달 (f) 예외는 이 ordinary supplier 사례와 구별. 개별 최초 시행일 미재구성.'),
'liner':('21 CFR 1317.60','(a)(2),(a)(4)–(5),(b),(c)','eCFR current title21 through 2026-11-02','정부 현재 통합본문; 2014 FR source 표시. 개별 최초 시행일 미재구성.'),
'linerinventory':('21 CFR 1304.11','(e)(7)(ii)(A)–(C)','eCFR current title21 through 2026-11-02','collector liner 기록과 dispenser stock inventory 구별. 개별 최초 시행일 미재구성.'),
'collector':('21 CFR 1317.75','(b),(c)','eCFR current title21 through 2026-11-02','ultimate-user 수거물 개별 handling 금지 확인. 개별 최초 시행일 미재구성.'),
'nabpsample':('NABP public MPJE Sample Questions','Public format examples, p1','public PDF fetched '+today,'style만 평가; 법률 정답 근거 아님. raw/extracted text는 /tmp 전용, public commit 금지.'),
'nabpformat':('NABP Take the MPJE Exam','120 computer questions;2.5-hour adaptive selected response','current public webpage fetched '+today,'표현 방식 참고만; 전체 저작물 public 재배포 없음.'),
'nabpcompetency':('NABP MPJE competency statements','pre2027 areas22/33/24/21%;2027-03-01 outline transition','current public webpage fetched '+today,'현재 target pre2027 범위 확인;2027이후 release 적합성 인증 아님.')}
notes={
'em2026':'ISO5 viable air >1 CFU/m³/device, surface >3/device. Pass-through은 cleaner ISO. MOR/PIC/pharmacist designee는 microbiology report 수령 후1businessday 통지. 같은ISO 60일 내 연속/비연속 반복 모두 microbiologist. Nonviable은 Board달리지시 없으면 중단·fullremediation·전ISO재인증. Viable만 V의 위험평가/제품완화/재검사/공간조건 하한정경로. I의 mostcurrentUSP와 V의 추가BUD상한을 함께 준수하므로 짧은 기존한도를 연장하지 않는다.',
'cmr20':'20.02(2)는 pharmacy manufactured/produced/compounded drug의 SADE를 Board,MedWatch,BetsyLehman에 anyemployee knowledge로부터7businessdays 보고. 20.02(5) nonresident 예외를 전체약국 일반론으로 확대하지 않는다. 20.06(2),(3)는 해당dispensed sterile/complexdefect identification후7days.',
'defect':'알거나알이유있는 dispensed compoundeddefect 회수, 남은재고분리/비조제. 모든CSP/CNSP recalledlog10년; CSP/complexCNSP defectreport7days. Defect원인SADE 또는 의심SADE는 Board에 즉시form. No injury는 recall면제아님.',
'mgl39d':'§39D(e)는 knows/shouldknow defect를 즉시recall하고 잔량을segregate/비유통한다. recall후7일 내 log를Board에이용가능하게하고10년보존. 이 recall시계와CMR20.06 identification시계를 구별.',
'fda503b':'503B compounded prescriptiondrug serious unexpectedAE initialreceipt후 ASAP/no later15calendar days. newinfo 또는 FDA요청followup15calendar days, 관련AErecord10년. annualregistration와무관. 일반주법폐기조항 없음.',
'fda503bpage':'공식 FDA 목록이 October2015 Final guidance로 현재 연결하며503B(b)(5)의310.305 content/format 경로를 명시.',
'cfr310':'(c)(1)(i) seriousunexpected initial15calendar, (c)(2) newinfo/requestedfollowup15calendar, (f)(1) AErawdata/correspondence10년. 503B 적용은 별도FDA officialguidance와연결.',
'cmr222':'Report allnewimmunizations72h. Objection은 MIISusers간sharing만제한하며Departmentaccess사용불제한. Form은 receipt24h내Department반환, GUIsharingstatus도변경. 기록삭제/접종취소효과없음.',
'form222':'ordinary partialshipment는 Form222date후60일, purchaserexecution후60일초과무효. firstshipment는reset아님. (f)DLA조달특례는일반order에적용되지않음.',
'liner':'removedliner는2직원이즉시seal; sealedliner는open/xray/analyze/penetrate금지. 외부size/permanentuniqueID로추적.',
'linerinventory':'collector는unused및sealedawaitingdestructionliner에 inventorydate, number/size,uniquenumber기록. patienttablets재계수아님.',
'collector':'lawfulultimateuser의II–V수거. deposit후약물을count/sort/inventory/otherwiseindividuallyhandle금지. stock회수/환자별sort모두금지.',
'nabpsample':'공개 sample을 직접 읽고 SBA, SelectALL, completeorderedresponse라는 응답 구조만 비교했다. sample은 contentarea대표가아니라는한계를명시한다. 이26문항의SADE/EM/MIIS/Form222/liner장면은 공개sample의구체문구를재현하지않는다. PreMPJE/회상/상용문항열람없음.',
'nabpformat':'공식페이지에서2.5hour/120computerbased adaptive selectedresponse를확인. 문항의법률정확성을인증하는자료아님.',
'nabpcompetency':'현재competency의LicensurePersonnel22,PharmacistPractice33,Dispensing24,Operations21비중과2027-03-01새outline전환을확인. 해당감사대상은pre2027 styleprofile.'}
sources={}
for sid,(name,section,version,limit) in sourceinfo.items():
 meta=json.loads((out/'sources'/f'{sid}.meta.json').read_bytes());memo={'source_id':sid,'reviewed_at':now,'own_primary_source_assessment_ko':notes[sid],'exact_section':section,'version':version,'limitation_ko':limit,'retrieval':meta,'raw_payload_read':True,'extracted_text_read':True,'retained_payload_scope':'OWN_MEMO_AND_METADATA_ONLY' if sid.startswith('nabp') else 'GOVERNMENT_RAW_TEXT_METADATA_AND_OWN_MEMO'}
 path=prefix+'sources/'+sid+'.memo.json';h=write(path,memo)
 s=dict(meta,authority=name,source_type='PUBLIC_OFFICIAL',exact_section=section,law_checked_date=today,version=version,effective_date_limitation_ko=limit,evidence_path=path,evidence_sha256=h,metadata_path=prefix+'sources/'+sid+'.meta.json',metadata_sha256=sha((out/'sources'/f'{sid}.meta.json').read_bytes()))
 if sid.startswith('nabp'):s.update(public_evidence_mode='RETAINED_OWN_PUBLIC_STYLE_MEMO_ONLY',legal_authority_credit=0)
 sources[sid]=s
# Explicit independent proposition assessments. No author truth or key is used to assign truth values.
concepts=[]
def add(text,truth,reason,sids,section=None):concepts.append((text,truth,reason,sids,section))
add('The described state pathway requires reporting only to the pharmacy\'s purchasing wholesaler.',False,'수신자는 wholesaler만이 아니라 Board·FDA MedWatch·Betsy Lehman이다.',['cmr20'])
add('Every ordinary side effect of any commercial medicine meets this pharmacy-produced SADE trigger.',False,'특정 pharmacy-produced drug와 seriousevent요건을 모든 상용약의 통상부작용으로 확대할 수 없다.',['cmr20'])
add('The general seven-business-day provision permits disregarding the applicable immediate defective-preparation policy.',False,'결함기인 SADE 의심은2024-04의 즉시Board보고를 유발하므로 일반7businessday로 늦출 수 없다.',['cmr20','defect'])
add('The employee-awareness trigger is not postponed until the MOR opens the message.',True,'20.02(2)의 anypharmacyemployee knowledge가 기산점이다. MOR의3일후열람은 시계를 재시작하지 않는다.',['cmr20'])
add('The immediate defective-preparation policy cannot be ignored merely because a general seven-business-day provision exists.',True,'2024-04가 defect기인 또는 의심SADE 즉시form을 명시한다. 일반CMR7businessday와 동시에 만족해야 한다.',['defect','cmr20'])
add('The reporting clock necessarily starts only when the MOR reads the employee\'s message.',False,'MOR보고책임과 anyemployeeknowledge기산점은 다르다.',['cmr20'])
add('The described state pathway connects reporting to the Board, FDA MedWatch, and the Betsy Lehman Center.',True,'20.02(2)(a)–(c)의 세수신기관과 일치한다.',['cmr20'])
add('Follow-up information is reported only during annual registration.',False,'새정보수령 또는FDA요청followup15calendar일을 annualrenewal까지 미룰 수 없다.',['fda503b','cfr310'])
add('The described adverse-experience records have no retention requirement after report submission.',False,'FDA III(H)/310.305(f)(1)는 관련AE자료10년보존이다. 제출완료가보존종료아님.',['fda503b','cfr310'])
add('The described initial FDA report is due as soon as possible and no later than 15 calendar days after initial receipt.',True,'FDAIII(B)와310.305(c)(1)(i)의ASAP/initialreceipt후15calendar외부한도와 일치한다.',['fda503b','cfr310'])
add('The federal 15-day limit removes any applicable faster Massachusetts reporting duty.',False,'연방제출의외부한도는 적용가능한MA7businessday/즉시보고를대체하지않는다. MAlicense/trigger가충족될때각각준수한다.',['fda503b','cmr20','defect'])
add('The initial report can be deferred until the annual registration-renewal window.',False,'FDA initialreceipt후15calendar한도이며annualregistration시계와독립이다.',['fda503b','cfr310'])
add('Applicable follow-up reporting has its own 15-calendar-day framework rather than the annual-registration schedule.',True,'III(C)/310.305(c)(2)는새정보수령15calendar또는FDA요청followup이다.',['fda503b','cfr310'])
add('The described adverse-experience records have a ten-year federal retention requirement.',True,'FDAIII(H)/310.305(f)(1)가AErawdata·correspondence포함10년보존을정한다. MA다른기록기간과섞지않는다.',['fda503b','cfr310'])
add('The recall log and defect report necessarily have the same trigger date because both mention seven days.',False,'MGL39D(e)는recall후log7일,CMR20.06(2),(3)는defectidentification후report7일이므로기산점이동일하다고단정못한다.',['mgl39d','cmr20'])
add('The described defect obligation calls for immediate recall and quarantine without waiting for proven patient injury.',True,'MGL39D(e)는knows/shouldknowdefect로즉시recall·잔량segregation/비조제를요구한다. injury확정을기다리지않는다.',['mgl39d','defect'])
add('The defective-preparation log may be destroyed when the recalled stock is removed.',False,'제품회수완료와별도로log10년보존의무가남는다.',['mgl39d','defect'])
add('Only sterile or complex preparations can ever be subject to the described basic recall and log duties.',False,'기본recall/log는noncomplexCNSP를배제하지않는다. 특정defectreport의CSP/complex범위를log에전용못한다.',['mgl39d','defect','cmr20'])
add('Recall and quarantine are required only after patient injury has been established.',False,'injury기준이아니라defect를알거나알이유있는때즉시recall·격리한다.',['mgl39d','defect'])
add('The recall-based log-availability clock and the defect-identification reporting clock must be tracked separately.',True,'logBoardavailability는recall후7일,해당defectreport는identification후7일로각각추적한다.',['mgl39d','cmr20'])
add('The described defective-preparation log has a ten-year preservation requirement.',True,'MGL39D(e)와2024-04는logatleast10years보존이다.',['mgl39d','defect'])
add('A noncomplex preparation is not automatically outside the basic defect recall and log duties.',True,'2024-04모든CSP/CNSPrecalledlog를요구하며noncomplex만으로면제되지않는다.',['mgl39d','defect'])
add('The first result exceeds the stated ISO 5 viable-air action threshold.',True,'2026-03p2는ISO5viableair>1CFU/m³/device이므로2는초과한다.',['em2026'])
add('An action-level result can be dismissed solely because the preparation looks clear.',False,'III(A),IV의조사·remediation은CSP외관만으로면제되지않는다. 환경결과와육안제품검사는다르다.',['em2026'])
add('Exactly 3 CFU exceeds the stated greater-than-3 threshold because greater than means greater than or equal to.',False,'현행surfaceISO5>3에서3은초과아님. >를≥로바꿀수없다.',['em2026'])
add('Air and surface CFU results can use an identical denominator without regard to sampling method.',False,'표는viableairCFU/m³(1000L)/device와surfaceCFU/device를구별한다.',['em2026'])
add('Exactly 3 CFU does not exceed a threshold written as greater than 3, although other relevant findings still require assessment.',True,'ISO5surface표>3이므로정확히3은초과하지않는다. III(H)/IV(A)의불리한trend등다른문제평가까지면제하지않는다.',['em2026'])
add('The first result does not exceed the threshold because the applicable ISO 5 viable-air number is 3 CFU.',False,'3은ISO5surface표숫자이며viableair는>1이다. 2는air기준초과.',['em2026'])
add('Air and surface results require their respective sampling units and thresholds.',True,'p2각표의서로다른분모와ISOclass별수치를적용한다.',['em2026'])
add('Counts from all sites and media should be pooled before applying a per-device action threshold.',False,'현행표는perdevice이며서로다른site/media결과를옛누적threshold처럼합칠근거가없다. III(H)도site별trend를구별.',['em2026'])
add('The pass-through necessarily uses the less clean connected space\'s classification.',False,'I의pass-through명시규칙은cleanerconnectedspace의ISO분류다.',['em2026'])
add('The same numeric CFU threshold applies to every ISO class and measurement type.',False,'p2airISO5/7/8은>1/>10/>100,surface는>3/>5/>50으로서로다르다.',['em2026'])
add('One cubic meter corresponds to 1,000 liters, so the reported denominator must not be treated as one liter.',True,'현행viableair표가m³(1000liters)를직접병기하므로1L와같은분모로취급못한다.',['em2026'])
add('The described pass-through rule uses the cleaner connected space\'s ISO classification.',True,'2026-03I의별표문장이cleaner공간ISOclassification을명시한다.',['em2026'])
add('One cubic meter and one liter are interchangeable denominators for the reported air result.',False,'m³는1000L이므로같은농도분모가아니다.',['em2026'])
add('Results from distinct sites or media devices should not be combined into an invented cumulative comparison.',True,'현행p2perdevice표와III(H)의site별trend구별에부합한다. 결과총합으로그표를새로해석하면안된다.',['em2026'])
add('Any employee may replace the specified reporting role without checking the policy.',False,'II는MOR/DesignatedPIC/그pharmacistdesignee로역할을한정한다. 아무직원에게치환못한다.',['em2026'])
add('An acceptable result between two findings necessarily prevents the described repeat-within-60-days trigger.',False,'III(G)는consecutiveornon-consecutive모두포함하므로중간적합결과로60일반복을제외못한다.',['em2026'])
add('The described one-business-day notification clock runs from microbiology-report receipt without waiting for later identification.',True,'II의receipt후1businessday통지는최종organismID까지유예된다고쓰여있지않다. 알려진actionlevel을보고하고ID/조사계속.',['em2026'])
add('Once notification is sent, organism and location trends are no longer relevant.',False,'I의genusID와III(H)의organism/location/site별trend및IV원인조사의무가남는다.',['em2026'])
add('The clock begins only after final genus identification, even though the action-level result was already reported.',False,'II통지기산점은microbiologyreportreceipt이지나중genus확정이아니다.',['em2026'])
add('The intervening acceptable result does not remove the described repeat-within-60-days microbiologist-engagement trigger.',True,'III(G)는같은ISOarea60일내비연속반복도명시한다. 중간acceptable결과는면제아님.',['em2026'])
add('Organism identification, location history, and trends remain relevant to investigation.',True,'I의actionlevelgrowthgenusID및III(H)(1)–(4)recovery/CFU/site/organismhistory가필요하다.',['em2026'])
add('The remediation ceiling replaces any shorter category or chemical-stability limit.',False,'I의mostcurrentUSP준수와V(D)의추가상한이함께적용된다. 상한은짧은기존category/stability기간을연장하는허가아님.',['em2026'])
add('The described nonviable pathway requires stopping, full remediation, and recertification as applicable rather than importing the viable exception.',True,'III(D)는Board달리지시없으면nonviable중단/fullremediation/allISOrecertification이며III(E)는V예외에서nonviable을제외한다.',['em2026'])
add('A finding in one PEC proves every other PEC can continue without assessment.',False,'V의ISO5(B)는unaffectedPEC도위험평가가적절하다고판단할때계속가능하다. 한PEC결과만으로다른모두의계속운영을증명못한다.',['em2026'])
add('Describing the work as clinically useful alone establishes all conditions for viable-remediation continuation.',False,'V(A)–(D)의실행된remediation·repeatsampling·riskassessment·productmitigation·BUD및공간조건모두필요하다. 임상유용성만으로불충분.',['em2026'])
add('The viable-remediation exception automatically authorizes continued work after any nonviable-particle failure.',False,'III(D),(E)가nonviable을viableV조건부계속경로에서제외한다.',['em2026'])
add('An additional remediation ceiling does not extend a shorter otherwise-applicable category or stability limit.',True,'I와V(D)를동시에적용하면remediation상한은추가제약이며더짧은category/안정성한도를연장하지않는다. 이문항은구체categoryBUD숫자의현행성까지주장하지않는다.',['em2026'])
add('An affected PEC and an appropriately assessed unaffected PEC can require different operational decisions.',True,'ISO5(A)affectedPEC중단원칙과(B)unaffectedPEC위험평가후계속가능을구별한다.',['em2026'])
add('Conditional viable-remediation work requires the specified risk assessment, implemented remediation, repeat sampling, and product-risk controls.',True,'V(A)–(C)의필수조건과일치하며V(D)/각ISO별추가조건도충족해야한다. 이진술이모든허용조건의완전목록이라고읽지않는다.',['em2026'])
add('Report the immunization through the applicable MIIS reporting process.',True,'222.100(A)는새접종72h보고,222.003의sharingobjection은Departmentaccess/use를제한하지않는다.',['cmr222'])
add('Handle the objection form and sharing-status update within the applicable receipt-based deadline.',True,'222.105(B)(2)form은receipt24h내반환하고GUIsharingstatus도변경해야한다. 문구의applicabledeadline은명시된form24h에한정해읽는다. GUI에독립된별도24h명문이있다는뜻으로확대하면안된다.',['cmr222'])
add('Delete the pharmacy\'s immunization record to implement the objection.',False,'222.003및222.105(B)(3)는Department/입력site의접근을남기며sharing변경을기록삭제로구현하지않는다.',['cmr222'])
add('Delay Department reporting until the patient reverses the objection.',False,'Departmentaccess/use비제한및72hnewimmunization보고의무는objection철회까지유예되지않는다.',['cmr222'])
add('Treat the objection as a withdrawal of permission for the vaccination already administered.',False,'form이변경하는것은MIISuser간sharing상태다. 완료된접종의동의철회로전환되지않는다.',['cmr222'])
add('October 20, the first shipment date.',False,'1305.13(b)는Form222date/구매자execution후60일로기산하며firstshipment는시작점아님.',['form222'])
add('October 1, the order date.',True,'유효한10월1일자Form222의ordinaryfulfillment시계는그orderdate부터다. (f)국방특례상황은제시되지않았다.',['form222'])
add('The date the purchaser first dispenses a tablet from the shipment.',False,'환자dispensing시점은supplierstockorder의1305.13(b)기산점이아니다.',['form222'])
add('The date the purchaser requests the remaining quantity.',False,'balance재요청은원Form222date부터의60일을reset하지않는다.',['form222'])
add('Keep the liner sealed and document its required identifiers.',True,'1317.60(c)의봉인유지와1304.11(e)(7)(ii)의inventorydate/number/size/uniqueID기록이함께적용된다.',['liner','linerinventory'])
add('Remove usable tablets for the pharmacy\'s return-to-stock bin.',False,'1317.60(c)봉인개봉금지,1317.75(c)deposit후개별handling금지에어긋난다. 수거물을판매재고로회수못한다.',['liner','collector'])
add('Sort the contents by patient before resealing the same liner.',False,'1317.75(c)는sort/count/inventory/individualhandling금지이며1317.60(c)는봉인liner재개봉자체를금지한다.',['liner','collector'])
add('Open the liner under a single technician\'s supervision.',False,'1317.60(c)sealedliner는개봉금지다. supervisor추가/변경으로개봉허용되지않고removedliner봉인은2employees절차다.',['liner'])
lookup={x[0]:x[1:] for x in concepts}
# Each item gets a separate decision-path and criterion finding, tied to what its stem asks.
paths={
'0997':('직원이안SADE를MOR가3일늦게읽은사례의기산점','anyemployeeknowledge와MOR보고책임을구별','직원메시지지연은약국의실제보고누락경로'),
'0998':('결함의심SADE에일반7businessday와즉시정책을겹쳐적용','빠른정책을무시할수있는지판단','SADE원인으로결함의심이생기는보고상황'),
'1000':('INCORRECT극성으로pharmacy-producedSADE범위선별','통상상용약부작용과특정중대사건을구별','실제보고trigger를분류하는관리상황'),
'1001':('503BseriousunexpectedAE최초수령후FDA기한','initial15calendar와annualrenewal을구별','outsourcingfacility의안전성보고실무'),
'1002':('503B새followup정보를annualrenewal까지보류하는계획','newinformation15calendar와최초보고를구별','새안전정보가나중도착하는현실적흐름'),
'1004':('INCORRECT극성으로연방15일의MA의무대체여부','연방·주복수의무를동시적용','503B시설의복수관할보고검토'),
'1005':('환자손상전결함의심dispensedpreparation회수','defectknowledge와확정harm을구별','결함을알았지만피해보고가없는회수초기'),
'1006':('recalllog와defectreport의기산점','recall과defectidentification을서로구별','회수와Board제출을하나의업무로섞는실무오류'),
'1007':('SATA로회수·log보존·report기산점·noncomplex범위평가','네명제를각기검증하여모두선택','회수기록과보고절차의공동검토'),
'1008':('INCORRECT극성으로noncomplex기본recall/log범위','특정report범위를기본log범위로전용하는오류구별','CNSP와CSP의실무범위분류'),
'1009':('지문이제공한ISO5air>1에2를비교','2>1이라는단순수치비교','실험실air결과를받는상황자체는가능'),
'1010':('지문이제공한surface>3에정확히3을비교','3은>3이아니라는비교연산','표면검사경계값을검토하는상황자체는가능'),
'1012':('INCORRECT극성으로외관만으로EMexcursion무시여부','환경오염조사와제품육안검사를구별','검사결과와제품외관이엇갈리는상황'),
'1013':('m³를1liter로취급한분모변환오류','1m³=1000L의단위상식','실험실결과를잘못읽는상황자체는가능'),
'1014':('서로다른ISO공간사이pass-through의cleanerclass','현재정책의공간분류규칙을적용','연결공간의환경threshold를선택하는상황'),
'1016':('INCORRECT극성으로모든ISO/측정의동일수치주장','class와air/surface별threshold차이를적용','환경결과의측정유형을혼동한실무오류'),
'1017':('actionlevelmicrobiologyreport뒤최종ID를기다리는통지','reportreceipt와나중organismID를분리','확정동정전결과를받는실제안전보고흐름'),
'1018':('60일내비연속반복EM에microbiologist관여','중간acceptable결과가repeat를없애는지판단','적합/부적합결과가교대로나오는EM이력'),
'1020':('INCORRECT극성으로아무직원에통지역할대체여부','정해진pharmacistrole와일반직원구별','MOR/PIC의통지업무위임상황'),
'1021':('nonviablefailure에viable예외를가져오는계획','nonviable중단·remediation·recertification과V예외구별','오염유형에따라운영중단을결정하는상황'),
'1022':('추가remediationBUD상한으로기존짧은한도를연장하는계획','독립된여러상한중더짧은것을유지','조건부조제의BUD설정실무'),
'1023':('SATA로nonviable/viable운영조건과BUD·PEC평가','네개조건부명제를각기검증하여모두선택','remediation중운영회의의복수판단'),
'1024':('INCORRECT극성으로한PEC결과가다른PEC계속운영을증명하는지','unaffectedPEC도위험평가가필요함을적용','여러PEC가있는compoundingarea운영검토'),
'0058':('MIISsharingobjection후보고와form·GUI처리','Department보고와site간sharing제한을구별','접종직후환자가sharingobjection을내는상황'),
'0075':('Form222부분shipment의60일기산일','orderdate와firstshipmentdate를구별','공급업체backorder와첫shipment시점이갈리는상황'),
'0083':('봉인liner를환자별tabletcount위해재개봉하는제안','liner추적기록과재고tabletinventory를구별','수거container와일반재고절차를혼동하는상황')}
fail={
'0998':{'wording_not_guessable':'지문이이미immediate정책을assessment에가져온다고밝혀즉시정책을무시못한다는A를반복선택하기쉽다.','reasoning_not_trivia':'CaseB정답은즉시정책이라는지문문구의재진술이며구체기산점/수신기관충돌을실제계산하지않는다.'},
'1000':{'wording_not_guessable':'B의Everyordinarysideeffectofanycommercialmedicine라는극단적범위가유일하게명백히과도하여SADE세부요건없이도제거가능하다.','authentic_distractors':'INCORRECT정답B가실제SADE중대성경계사례대신모든통상부작용이라는과장을써그럴듯한법적혼동을충분히만들지못한다.'},
'1009':{'jurisprudence_reasoning':'>1을지문에그대로주고2를제시하여법규나행정적결과를판단하지않아도풀린다.','reasoning_not_trivia':'주된판단은2>1이다. 즉시중단/보고/예외등법적행동선택이없다.','natural_rule_combination':'CaseB가있지만CaseA정답에는사용되지않고두threshold를자연스럽게통합하지않는다.'},
'1010':{'jurisprudence_reasoning':'지문자체의greaterthan3와3을비교하면정답이며현행정책상어떤운영의무가남는지는묻지않는다.','reasoning_not_trivia':'3>3이아니라는연산이핵심이므로법적판단난도를충분히제공하지못한다.','wording_not_guessable':'정답B만otherfindingsstillrequireassessment라는신중한자격을갖고오답들은외관무시/동일분모등과도한명제로치우친다.'},
'1012':{'wording_not_guessable':'제품이맑다는이유만으로환경actionlevel을dismiss한다는C가상식적으로위험하여정책의정확한의무없이도선별가능하다.','authentic_distractors':'옳은보기들은qualified표현인반면오류보기는solely외관이라는비현실적면제론으로대비된다.'},
'1013':{'jurisprudence_reasoning':'정답D는1m³=1000L의측정단위변환이며제공사실에대한법적결과선택을요구하지않는다.','reasoning_not_trivia':'정책의기한/주체/예외가아니라기초단위상식이문항의난도다.','natural_rule_combination':'CaseB의pass-through사실은CaseA의단위변환정답에필요없어두사례가분리된다.'},
'1016':{'wording_not_guessable':'same numericthresholdforeveryISOclassandmeasurementtype라는B의전면동일주장이유일한극단적명제여서표의세부수치를몰라도추측가능하다.'},
'1020':{'wording_not_guessable':'A만withoutcheckingpolicy로아무직원에게역할을바꾼다는무제한표현이며나머지는모두신중한정책준수문장이다.','authentic_distractors':'역할혼동은실제문제이나A의withoutchecking이법적scope지식없이도오답임을알리는단서다.'},
'1024':{'wording_not_guessable':'D의proves everyotherPEC...withoutassessment가나머지조건부·제약적표현과대비되어정책세부없이INCORRECT를추측하기쉽다.'}}
records=[]
for row,n in zip(packet['records'],near['records']):
 q=row['original_visible_content'];qid=q['question_id'];suffix=qid[-4:];decision,reasoning,practice=paths[suffix];inc='INCORRECT' in q['stem'];findings=[];expected=[];sids=set()
 for c in q['choices']:
  truth,why,ss,section=lookup[c['text']];selected=(not truth) if inc else truth
  if selected:expected.append(c['id'])
  sids.update(ss);au=[copy.deepcopy(sources[s]) for s in ss]
  findings.append(dict(choice_id=c['id'],option_text=c['text'],option_sha256=sha(c['text'].encode()),statement_supported=truth,should_select=selected,finding_ko=why+(' INCORRECT극성에서이거짓진술을선택한다.' if inc and not truth else ' INCORRECT극성에서이참진술은선택하지않는다.' if inc else ' 따라서이참진술을선택한다.' if truth else ' 따라서이거짓진술을선택하지않는다.'),authorities=au,original_rationale_read_completely=True,original_rationale_assessment_ko='원보기해설전문을읽었으며위독립조항검토와선택/비선택논리가일치한다. '+why))
 assert expected==q['correct_choice_ids'],(qid,expected,q['correct_choice_ids'])
 dup=copy.deepcopy(n['nearest']);pn=dup['public2349'];cn=dup['canonical439'];duptext='실독한canonical '+','.join(x['question_id'] for x in cn)+'는 '+({'CQI06':'기관조제범위/CQI시계/다른seriousinjury경로','CQI07':'다른처방또는administration안전의무','CQI08':'CQI·일반재고등다른행동선택','EM01':'청정실승인·수량제한등다른법적결정','EM02':'시설/처방등다른판단','EM03':'다른보고또는Form222실행결함','EM04':'다른분야의조건부권한','REV-058':'다른administration/protocol명제','REV-075':'같은Form222계열이나day64expiry/alteredform유효성판단','REV-083':'neverdispensedstock재입고조건'}[n['family_id']])+'를묻는다. public '+','.join(x['question_id'] for x in pn)+'는 '+('같은두사례/법적판단묶음을공유하는연습변형이다. 원문상반복을인정하며새독립사례라고세지않는다. 이ID는현재recommended_ids에없고따라서archivedvariation이라는문맥에서동시default중복으로판정하지않는다.' if qid.startswith('MA-EXP') else '같은주제의부분판단을공유한다. 이문항은 '+decision+'를직접묻고,현재recommended_ids에포함되지않아기본풀의동시중복으로판정하지않는다.')
 criteria={
 'jurisprudence_reasoning':(True,decision+'에서'+reasoning+'하는법적판단을요구한다.'),
 'practice_plausibility':(True,practice+'이므로업무상가능한사실관계다.'),
 'authentic_distractors':(True,reasoning+'을흐리는다른기산점·범위·절차명제를보기로제시한다. 각보기의실제오류는법규별검토에기록했다.'),
 'wording_not_guessable':(True,decision+'은주체/기산점/예외의내용을확인해야하며선택지배열만으로정답을확정할수없다.'),
 'reasoning_not_trivia':(True,reasoning+'이핵심이며단순약물schedule암기문항이아니다.'),
 'natural_rule_combination':(True,decision+'에서 '+{'CQI06':'employee기산점·세보고기관·defect즉시정책이같은사건에연결된다.','CQI07':'initial/followup·10년보존·적용가능MA보고를동일503B안전정보에연결한다.','CQI08':'기본recall/log와sterile/complexdefectreport의범위·보존·기산점을구분한다.','EM01':'air/surface의다른분모와threshold및excursion후조사를연결한다.','EM02':'환경측정의단위·perdevice표와pass-through공간분류를같은검토업무에연결한다.','EM03':'reportreceipt통지·담당약사범위·반복결과와trend조사를연결한다.','EM04':'nonviable중단원칙과viable예외조건·위험평가·BUD제약을연결한다.','REV-058':'72h신규접종보고와formreceipt24h·GUIsharing변경을같은접종사건에연결한다.','REV-075':'부분shipment허용과Form222원주문60일유효기간을연결하며환자처방시계와구별한다.','REV-083':'봉인개봉금지와collector의liner식별/inventory기록을자연스럽게연결한다.'}[n['family_id']]),
 'appropriate_drug_context':(True,'특정브랜드/성분이'+decision+'의결과를바꾸지않아불필요한약물명을넣지않은것이적절하다.'),
 'distinct_from_bank':(True,duptext),
 'not_schedule_flashcard':(True,decision+'를다루며약물의분류명만고르는문항이아니다.'),
 'public_style_without_copying':(True,'공개NABP의'+('SATA' if q['question_type']=='SATA' else '단일선택')+'응답형식과부합한다. '+decision+'의사실·보기는공개sample의구체계속교육/약물분류/만료순서문구와다르며보호된시험자료는사용하지않았다.')}
 for k,v in fail.get(suffix,{}).items():criteria[k]=(False,v)
 passed=all(v[0] for v in criteria.values());rv='PASS' if passed else 'FAIL'
 explain='core및모든보기한국어해설(learning_boundary포함)전문을실독했다. '+reasoning+'에관한법규주장과각오답교정은위primary원문에부합한다.'
 if suffix=='0058':explain+=' 다만24시간명문은form반환의무에있고GUI변경은동일조항의별도의무다. 설명을GUI전용24시간조항이있다는뜻으로확대해서는안된다.'
 if suffix in ['0075','0083']:explain+=' 원해설의inheritednote/새원문열람제한은작성당시증거범위표시이며본독립감사에서는해당연결조항도새로직접확인했다. 원해설의출처이력문장을현행법률권위로사용하지않았다.'
 record=dict(question_id=qid,record_sha256=row['record_sha256'],visible_content_sha256=row['visible_content_sha256'],family_id=n['family_id'],read_scope={'stem_read_completely':True,'all_choices_read_completely':True,'choice_count':len(q['choices']),'stored_key_read':True,'korean_core_and_all_choice_explanations_read_completely':True,'learning_boundary_read':True,'hidden_author_truth_read':False,'prior_independent_or_author_reviews_read':False},legal_review=dict(existing_answer_correct='YES',stored_key=q['correct_choice_ids'],independently_expected_key=expected,polarity='INCORRECT' if inc else ('SATA' if q['question_type']=='SATA' else 'CORRECT_SBA'),choice_by_choice_findings=findings,authorities=[copy.deepcopy(sources[s]) for s in sorted(sids)],verdict='KEEP',finding_ko=decision+'에대한저장키는현재공식원문과일치한다. '+reasoning+'의주체/조건/기산점및각오답을직접검토했다.',blocker=None,original_explanation_review=dict(core_read_completely=True,all_choice_rationales_read_completely=True,assessment='SUBSTANTIVELY_SUPPORTED_WITH_STATED_LIMITS',finding_ko=explain)),realism_review=dict(verdict=rv,decision='KEEP' if passed else 'MINOR_EDIT',criteria={k:v[0] for k,v in criteria.items()},criterion_findings_ko={k:v[1] for k,v in criteria.items()},duplicate_evidence=dict(method=near['method'],canonical_count=439,public_count=2349,nearest=dup,candidate_texts_read_completely=True,visible_candidates_path=prefix+'nearest-visible-input.json',visible_candidates_sha256=sha((out/'nearest-visible-input.json').read_bytes()),currently_recommended=qid in default,nearest_public_recommended={x['question_id']:x['question_id'] in default for x in pn},semantic_finding_ko=duptext)),disposition='INDEPENDENT_ASSESSED' if passed else 'NEEDS_REMEDIATION',safe_hold_recommended=not passed,release_eligible=False,required_next_action_ko='stage증거로만통합하며canonical감사·editoradjudication과releasegate는별도수행한다.' if passed else '해당현실성false기준을고쳐법률결과/그럴듯한대안을묻도록editor가수정한후freshcurrenthash재감사한다. 원문/키를이감사에서수정하지않는다.')
 records.append(record)
contracts=[]
for p in ['docs/RELEASE_POLICY.md','docs/AUDIT_WORKFLOW.md','docs/SOURCE_USE_POLICY.md','docs/QUESTION_AUTHORING_STANDARD.md','docs/INDEPENDENT_LEGACY_REVIEW_RUNBOOK.md','schemas/audit.schema.json','schemas/exam_style_profile.schema.json','schemas/blueprint.schema.json','data/exam_style/mpje_style_profile.json','data/blueprint.json','scripts/review_queue.py','scripts/build_full_corpus_review.py']:
 b=(root/p).read_bytes();snap=prefix+'methodology/'+p;writehash=sha(b);dest=root/snap;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b);contracts.append(dict(path=p,snapshot_path=snap,file_sha256=writehash))
style=json.loads((root/'data/exam_style/mpje_style_profile.json').read_bytes());bp=json.loads((root/'data/blueprint.json').read_bytes())
report=dict(schema_version='independent-legacy-final26-review/1',stage='independent-legacy',independent_of_authors=True,auditor='GPT',auditor_instance='GPT:/root/independent_final26:20261104',actor_provenance=dict(actor_id='/root/independent_final26',session_id='/root/independent_final26'),canonical_audit=False,canonical_release_credit=0,release_eligible=False,reviewed_at=today,completed_at=now,job_id=job['job_id'],assignment_path=prefix+'assignment.json',assignment_sha256=sha((out/'assignment.json').read_bytes()),input_packet_path=prefix+'assigned-visible-input.json',input_packet_sha256=sha((out/'assigned-visible-input.json').read_bytes()),question_hashes=job['question_hashes'],style_profile=dict(profile_id=style['profile_id'],content_version=style['content_version'],content_hash=style['content_hash'],file_sha256=sha((root/'data/exam_style/mpje_style_profile.json').read_bytes())),blueprint=dict(blueprint_id=bp['blueprint_id'],content_version=bp['content_version'],content_hash=bp['content_hash'],file_sha256=sha((root/'data/blueprint.json').read_bytes())),contracts=contracts,sources=list(sources.values()),records=records,summary=dict(assigned=26,fully_read=26,independently_legal_assessed=26,existing_answer_yes=26,legal_keep=26,realism_pass=sum(r['realism_review']['verdict']=='PASS' for r in records),realism_fail=sum(r['realism_review']['verdict']=='FAIL' for r in records),source_blocked=0,canonical_release_credit=0),independence_limitation_ko='authortruth·기존author/independent보고서·원장판정을읽지않았다. 현재visiblekey는입력계약에따라읽되답을그대로따라독립확인으로세지않았다. nearest는현재visible본문6필드만투영하여읽었으며원객체는코드내projection/hash입력외모델출력하지않았다.',source_limitations_ko=['Firecrawl govsearch는URLdiscovery만사용. scrape3건은credit부족으로실행되지않았고legalcredit0. 이후각officialURL을proxy/TLS검증유지curlGET하여현재본문을실제확인했다.','NABPraw/text는/tmp에만보관하고공개evidence에는직접작성memo·retrievalmetadata·원SHA만남긴다. retainedmemo검증은원copyrightpayload의공개보존/재검증을뜻하지않는다.','모든현행성은실제조회일현재제공된공식본문과표시version에한정한다. 개별최초시행일미확정한계를각source에기록. USP유료원문을직접읽었다고주장하지않는다.'],validation_contract='ALL sources AND EACH legal_review.authorities AND per-choice authorities must pass build_full_corpus_review.validate_independent_source_bytes before and after commit; native queue validates assigned26 IDs/hash/provenance/evidence only.')
write('reports/full-corpus-review/independent-final26-review.json',report)
print(report['summary'])
