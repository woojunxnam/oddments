import json,hashlib,subprocess,sys,re,shutil,collections
from pathlib import Path
sys.path.insert(0,'scripts');import note_review_queue as q
B=Path('reports/full-corpus-review/independent-notes/notes120-b');job=json.load(open(B/'assignment.json'));packet=json.load(open(B/'visible-input.json'));context=json.load(open(B/'related-context.json'));sha=lambda b:hashlib.sha256(b).hexdigest();assert packet['job']==job
assert sha((B/'related-context.json').read_bytes())=='9a13e9bff521c97a9e63cd047be690546b59f6c071146c41087c741a0ff333ab'
checks=[]
for u in packet['units']:
 uid=u['unit']['id'];b=job['unit_bindings'][uid];assert u['binding']==b and sha(u['unit']['body'].encode())==b['body_sha256'];raw=subprocess.check_output(['git','show','HEAD:'+b['census_path']]);assert sha(raw)==b['census_sha256'];c=json.loads(raw);cu=next(z for z in c['units'] if z['unit_id']==uid);cc=[z for z in c['claims'] if z['unit_id']==uid];assert cu==u['census_unit'] and cc==u['claims'];assert q.digest(cu)==b['census_unit_record_sha256'];assert {z['claim_id']:q.digest(z) for z in cc}==b['claim_record_sha256s'];checks.append({'unit_id':uid,'body_utf8_sha256':b['body_sha256'],'census_raw_sha256':sha(raw),'unit_record_sha256':q.digest(cu),'claim_count':len(cc),'all_claim_record_hashes_match':True})
assert len(checks)==20 and sum(x['claim_count'] for x in checks)==372
cache={}
def source_json(path,js=False):
 if path not in cache:
  raw=subprocess.check_output(['git','show',context['source_head']+':'+path]);assert sha(raw)==context['source_files'][path];cache[path]=json.JSONDecoder().raw_decode(raw.decode().split('=',1)[1].lstrip())[0] if js else json.loads(raw)
 return cache[path]
for z in context['questions']:
 data=source_json(z['source_path']);qs=data if isinstance(data,list) else data['questions'];orig=next(x for x in qs if x['question_id']==z['question']['question_id']);assert q.digest(orig)==z['complete_record_sha256']
for z in context['derived']:
 data=source_json(z['source_path'],True);v=z['visible_item'];orig=next(x for x in data[z['collection']] if x.get('id',x.get('term'))==v.get('id',v.get('term')));assert q.digest(orig)==z['complete_record_sha256']
assert len(context['questions'])==78 and len(context['derived'])==9 and not context['missing_related_ids']
(B/'input-validation.json').write_text(json.dumps({'unit_checks':checks,'related_questions_committed_records_verified':78,'derived_committed_records_verified':9,'additional_body_questions_read':['MA-EXP-0278','MA-EXP-0279','MA-EXP-0280'],'root_strict_inventory_observation':'Root actualstrictinventory currentbody/census/claimSHA검증결과의rawprojection을입력으로사용했다. Worker는missingpreimageguard를우회하거나load_notes를모킹하지않았다. 위해시검사는독립법규KEEP가아니다.'},ensure_ascii=False,indent=2)+'\n')
# Each range below was selected after reading the entire body, its claims, original question content, and primary clauses.
spec={}
def add(uid,a,b,keys,section,finding):
 for n in range(a,b+1):
  assert (uid,n) not in spec;spec[(uid,n)]=(keys.split(','),section,finding)
add('w3-d-8',1,8,'cdtm','247 CMR16.03(5)(d)2 and (e)2','Retail의 issuance 후24시간 사본전달, 더긴급한 상황의조기통지, action기록과physiciancustody사본을 직접확인했다. Consent사본 physician→pharmacist24시간과 행위주체·시작점을 분리했다. 월말일괄송부가새Rx의시계를대체하지않는다.')
add('w3-d-8',9,22,'cdtm','247 CMR16.04(2)(a)–(j)','모든setting CPA필수내용을원문항목별로읽었다. Disease/primary-co-morbid, specificprescribing, protocols,risk,permanentrecord,outcomes,setting맞는consent, 전달방식/기간,urgent절차,감독/부재시절차와양측attestation이다. 한요소나서명으로다른요소를대체하지않았다.')
add('w3-d-8',23,24,'cdtm,intern','247 CMR16.04(3);8.02(6)(d);8.04(4)(e)','Delegation은허용/불허duties와when/how/duration/scope를CPA에명시하며intern/technician규정에종속된다. Technician의DUR/clinicalconflict/therapyclarification/modify금지를직접확인했다.')
add('w3-d-8',25,26,'cdtm','247 CMR16.04(4)','Authorized pharmacist와supervising physician(s)가적어도2년마다review와renew를모두수행한다. 최초서명으로영구유효하거나자동2년해지라는문언은아니다.')
add('w3-d-8',27,29,'cdtm','247 CMR16.04(5)','종료/미갱신전 uninterruptedcontinuation을arrange하고종료/미갱신시환자에게termination과continuation절차를서면안내하는두단계를직접확인했다.')
add('w3-d-8',30,33,'cdtm','247 CMR16.04(6)','현재CPA/referral/consent의사본은약사primarypractice setting에두고두Board요청시readilyretrievable,원본은physiciancustodypatientrecord에두는분담을확인했다.')
add('w3-d-8',34,34,'cdtm','247 CMR16.04(2)(h);16.03(5)(e)2','All-setting urgent identification/transmission절차와retail의moreurgentnotification예외를직접읽었다. §16.04(2)(h)는모든urgentcommunication의독립된일률적immediate시계를쓰지않는다. 본문의즉시가운영권고인지별도법적시한인지명확하지않다.')
add('w3-d-9',1,17,'cdtm','247 CMR16.04(1),(2)(a)–(j)','서명된writtenCPA와physicianscope한계및각필수내용을직접확인했다. 표의빈협약/포괄처방/label대체/무monitoring/PRN한문구는명시적protocol·record·transfer·attestation요건을대체하지못한다.')
add('w3-d-9',18,25,'cdtm,intern','247 CMR16.04(3);8.01;8.02(6)(d);8.04(4)(e)','위임가능/불가능업무,시점·방법·기간·범위를각각명시하고실제지원업무도247CMR8의독립적scope를지킨다. 서명자재량이나사후검토로technicianclinicaljudgment를확장하지못한다.')
add('w3-d-9',26,28,'cdtm','247 CMR16.04(4)','at least everytwoyears의review-and-renew를직접확인했다. 이규정은2년자동종료도영구무검토도아니다.')
add('w3-d-10',1,5,'cdtm','247 CMR16.04(5)','종료와nonrenewal모두사전치료연속성조치,환자서면통지의대상이다. 통지에는사실과후속절차를포함하며직원간구두통보만으로서면을대체하지않는다.')
add('w3-d-10',6,16,'cdtm','247 CMR16.04(1),(6)','약사측currentCPA/referral/consent사본의localretrievability와의사측원본custody를직접대조했다. 전자파일에도현재서명된문서·검색가능성요건이적용되지만별도전자서명기술기준까지인증하지않았다.')
add('w3-d-10',17,17,'cdtm,conduct','247 CMR16.01;16.04(6);9.01(16)','§16.01은purpose이고§16.04(6)는현재사본/원본과retrievability다. 일반confidentiality는9.01(16)에있지만본문이16.01을전자기밀기술근거로지목한부분의정확한적용관계는확정하지않았다.')
add('w3-d-10',18,26,'cdtm,cdtmlaw','247 CMR16.04(7)(a)–(c);M.G.L.c112§24B½(e)','Physician/group의qualifiedpharmacist고용,communitypharmacy의QA용physician/medicalpractitioner고용허용과CPAmaintain/establish/enter목적physician고용금지를직접확인했다. 금지기준은실제목적이므로직함·정액급여가면제조건이되지않는다.')
add('authority-paths',1,6,'cdtm,cdtmlaw','247 CMR16.01–16.04(1);M.G.L.c112§24B½(a),(c)(5)','개인자격·허용setting·서명CPA와retailpatientreferral/consent가별도요건임을확인했다. 시설면허나일반약제공사실이이요건을대체하지않는다.')
add('authority-paths',7,9,'prescribing','DCP26-08-125 Purpose;General(a)–(j),NOTE;Hormonal(a),(e)','지정oral/patch제품,교육·assessment·NPI·label/guidance조건과administrationcircular별도확인NOTE를직접읽었다. 지정경로를모든contraceptive제형또는모든행위의권한으로일반화하지않았다.')
add('authority-paths',10,11,'naloxone,naloxoneorder,cdtm','Policy2024-01 I(B);statewide naloxone order;247CMR16.04(1)','실제naloxonestandingorder는해당dispensing을허용하고CPA는별도written-signedagreement를요구한다. standingorder거래하나로CPA서명관계가성립하지않는다.')
add('authority-paths',12,12,'opill,planb','FDA Opill2023-07-13;PlanB OTC history/current Q&A','회수한개별Opill/PlanB의OTC상태는확인했다. 이일반명제의각OTC제품·제형별판매조건전량은현재감사에서확정하지않아범용OTC규칙의sourceblock를유지한다.')
add('authority-paths',13,14,'prescribing,opill','DCP26-08-125 Hormonal(a);FDA Opill approval','Circular는OTC/Rx-only에관계없이지정oral/patch를대상으로한다. OTC제품판매자체와그조건부처방경로를구별하고다른제형처방권을만들지않는다.')
add('authority-paths',15,17,'administration','DCP26-03-124 Dispensing by Administration(a)–(f);Administration and Dosing','유효처방·성인·training등별도조건,non-IV제한,SC/IM및label/REMS를직접확인했다. 목록의doxycycline와SC/IM간세부적용OPEN을이일반구분으로해소하지않는다.')
add('authority-paths',18,18,'definition','M.G.L.c94C§1 definition of Dispense','법정Dispense정의가prescribing와administering를포함한다고직접명시한다. 실무권한구분을모든법에서배타적단어정의라는명제로바꾸지않았다.')
add('authority-paths',19,23,'cdtmlaw','M.G.L.c112§24B½(a),CDTM definition','Drugtherapy직접관련lab의ordering/evaluating는physiciansupervision또는directconsultation과approvedsettingprotocol에연결되고diagnosticcomponent를배제한다. 약물모니터링과새진단을분리했다.')
add('authority-paths',24,25,'cdtmlaw,prescribing','M.G.L.c112§24B½(c)(5);DCP26-08-125 Hormonal(a)','RetailCDTM의18세·질환·CII–V금지/VI조건을확인했다. 별도contraceptioncircular는anyage를명시하므로retailCDTM한계를그대로이식하지않는다.')
add('w3-d-12',1,7,'prescribing','DCP26-08-125 Date,footnote1,Purpose','2026-08-25와25-04-124대체각주,Massachusettslicensedpharmacist대상,oral/patch/HIV/STI열거와no requirement to prescribe를직접확인했다. 문서의게시된설명과모든상위법권한관계의완결판정을구별한다.')
add('w3-d-12',8,17,'prescribing','DCP26-08-125 General(a)–(g),(i)','NPI,FDA-approved대상약,label또는statewideguidance,counseling의properuse/risks/sideeffects,환자writtenrecord,as-soon-as-practicable조제,documented/readilyavailable,continuedcompetency를각문장으로직접대조했다.')
add('w3-d-12',18,19,'prescribing','DCP26-08-125 General(h)','Referral또는clinicalprovider상담권고와환자consent가있는PCP통지라는대안을직접읽었다. 이명제는해당경로를따라야하는구조안의행위이며어느대안도전부생략가능하다는인증이아니다.')
add('w3-d-12',20,21,'prescribing','DCP26-08-125 Purpose final sentence','별도MCSR불필요는prescribing와dispensing가singlepharmacylocation에서모두발생하는조건이다. 다른약국전송/별도office재고의포괄면제로확대하지않았다.')
add('w3-d-12',22,22,'prescribing','DCP26-08-125 Purpose final sentence','개인MCSR한정면제만확인된다. 약국자체허가·등록의종류/예외/적용전량을이문서가정하지않으므로별도시설등록전체인증은보류한다.')
add('w3-d-12',23,25,'prescribing,cdtm','DCP26-08-125 General(j);247 CMR16.02(1)(f)3','Circular의MassHealthenrollment는encouraged이고CDTM의prescriptivepractice에는participates/appliedattestation이명시되어있음을현재직접대조했다. 권한과reimbursement를분리하며교육·면허자격만으로지급을보증하지않는다.')
add('w3-d-13',1,18,'prescribing,prescribinglaw','DCP26-08-125 Hormonal(a)–(e);M.G.L.c94C§19F(a),(c)','Anyage,oral/patch범위,patientselfscreening/currentUSMEC,최대12monthRx,appointment강제금지와교육을직접읽었다. 다른제형·시술·보험지급·제품expiry면제는이문서가부여하지않는다. Assessment는단순checkbox작성과같지않다.')
add('w3-d-13',19,19,'prescribing,prescribinglaw','DCP26-08-125 Hormonal(c);M.G.L.c94C§19F(b),(c)(ii)(B)','Circular의lackclinicalvisit/refills문언과현재§19F의후속clinicalvisit/timeframe규칙을직접대조했다. 실제timeframe구현규정과개정관계미확정이라무제한refill허용으로인증할수없다.')
add('w3-d-14',1,14,'prescribing','DCP26-08-125 Hormonal(e)(i)–(v);HIV Prevention(b)','처방전training및5교육목표,ACPE/IPCErecommended와증빙요청제공을직접확인했다. Contraceptionparagraph의고정2시간부재를HIV최소2시간과분리했다.')
add('w3-d-14',15,20,'prescribing','DCP26-08-125 General(c),(e),(g),(h)','Assessment/product/supply/counseling/writtenrecord와referral또는consentedPCP통지의연결을document/readilyavailable요건과대조했다. 일반판매영수증하나로모든활동기록을대체하지않는다.')
add('w5-b-2',1,6,'ecfaq,ecorder,eclaw','EC FAQ Statewide standing order,training,participation;M.G.L.c94C§19A(b)–(d);signed order pp1–3','Ulipristal/levonorgestrel대상,추가교육비필수,maycomplete와자발적참여/모든직원참여비필수를현재공식문언으로직접확인했다. 서명order의제품·평가범위를우선한다.')
add('w5-b-2',7,7,'ecfaq','EC FAQ voluntary participation','FAQ의자발성만으로광범위한모든reproductive-healthstock/access/대안의무의현행상위규정전량을검증할수없다. 별도의무가남는다는범위에대한추가원문adjudication이미완이다.')
add('w5-b-2',8,12,'ecfaq,ecorder,eclaw','M.G.L.c94C§19A(b),(c);EC FAQ how to dispense,third-party request','EC지정dispensing이며환자를대면/전화평가하고patient-specificRx를generate/fill/label한다. 일반독립처방면허나타인요청만으로환자평가를대체하는경로는아니다.')
add('w5-b-2',13,13,'ecfaq,conduct','EC FAQ how to dispense;247CMR9.16(1),(7)','Patient-specificRx생성뿐아니라일반처방기록·환자profile유지규정9.16을이번에직접읽어본문의한정된기록유지명제를확인했다. 이판정은ECannualreport의다른조건을자동인증하지않는다.')
add('w5-b-2',14,14,'ecorder','Signed EC order pp1–3;authorizing physician signature2022-08-04','현재FAQ가연결하는실제서명order를회수해제품·환자평가·금기·patientinstructions와서명일을읽었다. 양식또는index만을실제서명order로대체하지않는다.')
add('w5-b-3',1,6,'ecfaq','EC FAQ third-party request,parental consent','실제복용자의대면/전화평가,타인용OTC구매와구별,minorEC부모동의불필수를직접확인했다. 그좁은예외를다른모든minor치료동의권으로확대하지않는다.')
add('w5-b-3',7,10,'ecfaq,ecorder','EC FAQ anti-nausea medication,vomiting,advance supply;EC order4–5 and antiemetic table','FAQ의order범위antiemetic/2–3hour재투여/advance supply조건과서명order를직접읽었다. 별도현재임상알고리즘전체를노트가제시한다는판정은하지않았고order의범위를유지한다.')
add('w5-b-3',11,12,'ecfaq','EC FAQ sexual assault','문언은ECdispensing후rapecrisiscenter/hospitalED적절한referral이다. Referral를모든EC제공의자동선행지연조건으로바꾸지않는다.')
add('w5-b-3',13,13,'conduct','247CMR9.01(16)','Licensee가patientconfidentiality를유지하고confidentialinformation을보호해야한다는직접문언을읽었다. MinorEC접근허용이privacy의무를없애지않는다.')
add('w5-b-4',1,6,'ecfaq','EC FAQ how to dispense,reporting,prescriber prescription','환자별generate/fill/label,January1–December31해당EC보고,email양식링크요청,별도OTC구매를확인했다. 이EC안내에는naloxoneJanuary15시한이없으므로일반annual이라는이유로복사하지않는다.')
add('w5-b-4',7,7,'planb','FDA PlanB One-Step Q&A,What is PlanB and generics question','FDA현행페이지에서PlanBOne-Step의levonorgestrel1.5mg,동일referencegeneric상태/labeling을직접확인했다. 이정확한성분·함량명제를위해제조사판매문구를사용하지않았다.')
add('w5-b-4',8,9,'ecorder,ella','EC order3;DailyMed ELLA label1 and HUMAN PRESCRIPTION DRUG LABEL','ECsignedorder의UPA/ella와현재DailyMed의ulipristalacetate,ECindication,Rxcategory를직접대조했다. Levonorgestrel의OTC를ella에복사하지않는다.')
add('w5-b-4',10,11,'opill,opillorder','FDA Opill approval2023-07-13;MassHealth OTC order Oral Administration,Protocol5(a)','Norgestrel0.075mg제품과dailyuse/EC사용금지를FDA원문과MassHealth실제서명order에서확인했다. 보험order와OTC분류는별도이다.')
add('w5-b-4',12,13,'mifepristone','FDA mifepristone Q&A,General Information and REMS restrictions','FDA는Mifeprex와approvedgeneric의mifepristone성분·medicationabortion적응증,공유REMS의certifiedprescriber/pharmacy와patientinformation을직접명시한다. 별도제품조건이있다는본문의한정된명제를확인했다.')
add('w5-b-4',14,15,'medindexC,mifepristone','MedlinePlus C index,Cytotec;FDA mifepristone REMS scope','Cytotec→misoprostol매핑과FDA의mifepristone/misoprostol별개약물및drug-specificREMS범위를직접대조했다. 이름유사성만으로mifepristoneREMS를모든약에부과하지않는다는한정판정이다.')
add('w5-b-4',16,16,'conduct','247CMR9.16(1),(7)','Rx기록과confidentialpatientprofile의유지규정으로ECstandingorder개별거래기록을확인했다. annualaggregate제출이일반환자기록을대체하지않는다.')
add('w5-b-4',17,17,'mifepristone,planb','FDA mifepristone Q&A General Information;PlanB Q&A abortifacient','FDA에서mifepristone의기존임신termination과PlanB의pregnancyprevention/기존임신비termination을직접대조했다. 두범주는교환가능한EC목록이아니다.')
add('w5-b-5',1,4,'access','ACCESS Q&A,Does law apply all plans;12-month supply limitations','MAissuedfullyinsured와self-funded면제,동일피임약trial후12month조건및oral/patch/injectable/ring범위를직접읽었다. 모든보험또는새method첫fill에무조건적용하지않는다.')
add('w5-b-5',5,6,'prescribing,ecorder','DCP26-08-125 Purpose;EC signed order','보험의대상제형과oral/patchstatutoryprescribing및ECorder의지정경로를직접대조했다. coverage는처방권한을늘리지않는다.')
add('w5-b-5',7,9,'birthcontrol,opillorder,opill','DPH Birth control supply;MassHealth OTC order Protocol1–7,Records;FDA Opill approval','DPH의March2025도입안내와실제서명order의Jan27,2025,MassHealth/HSN대상·assessment·patientprofilerecord를구별해읽었다. Order는보험경로이며일반OTC구매에보편적Rx필수라는뜻이아니다.')
add('w3-d-15',1,4,'opill','FDA Opill approval2023-07-13','FDA의norgestrel,firstnonprescriptiondailyoralcontraceptive와다른oral제형Rx유지,notforEC를직접확인했다. 동일contraceptive라는이름으로purpose를교환하지않는다.')
add('w3-d-15',5,9,'planb','FDA PlanB One-Step Q&A,current status/history/mechanism','Levonorgestrel1.5mgEC,2013-06-20이후OTCwithoutagerestrictions와과거17/18세이력을구별했다. 현행Q&A는기존임신을종료하지않음을설명한다.')
add('w3-d-15',10,13,'ella,prescribing,ecorder','DailyMed ELLA label1,Rx category;DCP26-08-125 scope;EC order3','현재DailyMed의ellaRx-only/EC를확인했다. Oral/patchcircular또는다른EC의OTC상태로모든EC무조건처방권한을추론하지않고실제order/protocol을지정한다.')
add('w3-d-15',14,15,'access,opillorder,opill','ACCESS Q&A emergency contraception;MassHealth OTC order;FDA Opill approval','현재공식ACCESS와MassHealthorder는보험용Rx/order경로가존재함을보이지만모든payer조건전량을확정하지않았다. FDA의OTCstatus는보험문서요건으로자동Rx-only가되지않는다.')
add('w3-d-16',1,3,'oralprep,pep','Statewide Oral PrEP guidance1,3–5;PEP guidance1,4–5','PrEP의노출전위험감소와PEP의노출후예방을직접읽었다. Confirmed/suspectedHIV는예방protocol의제외대상이며establishedHIV의완전치료와같지않다.')
add('w3-d-16',4,16,'prescribing,prescribinglaw','DCP26-08-125 HIV Prevention(a),(b);M.G.L.c94C§19F current text','HIV예방circular의statewideguidance·사전최소2시간·구체교육목표·pharmacology-only불충분·증빙요건을직접읽었다. 현재게시§19F는contraception만기술하고circular/index는HIV/STI권한을인용한다. 개정관계와ICPE/IPCE철자관계의미확정은그대로남긴다.')
add('w3-d-16',17,23,'hivindex,prescribing','DPH HIV/STI index;DCP26-08-125 STI Prevention and Treatment(a),(b)','현재index는chlamydia/gonorrhea치료와DoxyPEP의별도DOCX를연결한다. STItraining과guidance준수문언을확인하되HIV2시간을STI전체의고정최소/최대로복사하지않았다.')
add('w3-d-16',24,28,'oralprep,pep,sti,doxypep','Oral PrEP4–6;PEP4–6;STI and DoxyPEP Patients paragraphs','네DOCX전문과appendix를새로읽어연령/체중/임신/증상/검사/allergy/상호작용의서로다른조건을확인했다. 목록만으로모든환자를적격으로간주할수없다. 다만STI가참조하는별도DPHtreatmentregimen원문전체와권한개정관계/임상일관성전체인증은완료하지않았으므로기존임상scopeblock를자동해제하지않는다.')
add('hiv-protocol-open',1,6,'prescribing','DCP26-08-125 Purpose;General(b),(c),(e),(g);HIV(b),STI(b)','NPI/해당training/counseling/writtenrecord/documentation과single-locationMCSR조건을원문으로직접확인했다. 공통조건이개별supply/refill권한을정하지않는다.')
add('hiv-protocol-open',7,9,'hivindex,prescribing','DPH HIV/STI index document list;DCP26-08-125 General(d),HIV(a),STI(a)','OralPrEP/PEP/STI/DoxyPEP는현재index에서별도문서로연결되며각해당guidance에따라야한다. 일반circular조건충족만으로임의기간공급권한을만들지않는다.')
add('hiv-protocol-open',10,10,'oralprep,pep','Oral PrEP6.2,Appendix5;PEP6.3,Appendix2','이번회수PrEP본문/consent는60일norefills지만PEP6.3최대30일과Appendix2의28일문구가함께존재한다. 다른주의숫자로채울수없고현행권한개정/참조clinicalalgorithm관계도확정하지않아기존supplyscopeblock를유지한다.')
add('hiv-protocol-open',11,13,'prescribing','DCP26-08-125 General(c),(g)','Risk/sideeffect상담과문서화활동readilyavailable문언을직접확인했다. 과거접근실패의한계서술과현재네DOCX회수성공을구별해기록한다.')
add('w5-b-8',1,2,'truvada','MedlinePlus Emtricitabine and Tenofovir disoproxil fumarate,drug name and brand names','NLM공식명칭과Truvada브랜드연결로emtricitabine/TDF두성분을직접대조했다. 이매핑을두제품전체대체규칙인증으로확대하지않는다.')
add('w5-b-8',3,4,'medindexD','MedlinePlus D drug index,Descovy','현재NLMindex의Descovy→Emtricitabine andTenofoviralafenamide매핑을직접읽었다. 이름매핑과모든현재label의strength/population대조는구별한다.')
add('w5-b-8',5,7,'oralprep','MA Oral PrEP guidance3,Appendix1','MAguidance는TDF/FTC와TAF/FTC의다른함량/성노출범위/renal조건을보인다. 그러나이claim의currentFDA두제품label전문과모든대체조건을각각검토한것은아니라그전체label/대체법규인증을보류한다.')
add('w5-b-8',8,8,'medindexA','MedlinePlus A drug index,Apretude','NLMindex의Apretude→CabotegravirInjection매핑을직접확인했다. 예방적응증전체의독립FDAlabel검증과구별한다.')
add('w5-b-8',9,9,'medindexC','MedlinePlus C drug index,Cabenuva','NLMindex의Cabenuva→Cabotegravir andRilpivirineInjection매핑을직접읽어두성분조합을확인했다.')
add('w5-b-8',10,11,'medindexA,medindexC','NLM Apretude/Cabenuva name mapping only;FDA indication/approval records not obtained','브랜드/성분매핑은직접확인했지만FDAcurrent제품별indication또는Yeztugoapproval/application문서를확보해독립대조하지못했다. 제조사발표로공식법규권한을대체하지않는다.')
add('w5-b-8',12,12,'medindexS','MedlinePlus S drug index,Sunlenca','NLMindex의Sunlenca→Lenacapavir및LenacapavirInjection매핑을직접읽었다. Treatmentcombination·prevention전체적응증은별도검증대상이다.')
add('w5-b-8',13,19,'medindexS','NLM lenacapavir name mapping only;FDA approval/application and MA substitution scope not fully adjudicated','동일성분의제품/적응증·approval과application의구분필요성은타당하지만Sunlenca/Yeztugo의currentFDAlabel/신청상태및MA대체법전체를현재공식1차문서로확정하지못했다. 제조사발표를approval/legalauthority로승격하지않고기존block를유지한다.')
add('w3-d-18',1,5,'naloxone,naloxoneorder,naloxonelaw','Policy2024-01 opening,I(B);M.G.L.c94C§19B(b),(c),(e),(g)','현재정책은일부OTC에도보험standingorder경로가남고타인용구매를허용함을명시한다. Patient-specificRx와statewideorder두경로를직접대조하고구매자본인환자조건을만들지않는다.')
add('w3-d-18',6,7,'naloxone,naloxonelaw','Policy2024-01 opening;M.G.L.c94C§19B(g)','Apparentopioid-relatedoverdose의good-faithadministration과면책문언을직접읽었다. 이조건을모든약의무처방투여또는모든bad-faith/negligent행위포괄면책으로확대하지않는다.')
add('w3-d-19',1,4,'naloxone','Policy2024-01 opening,I(C)','Communityneeds에맞는continuoussufficientsupply와wheneverScheduleIIopioid가dispense될때offer를직접확인했다. 과거거절이이후offer를면제하거나환자구매를강제하거나CIIstimulant를opioid로만들지않는다.')
add('w3-d-19',5,5,'naloxone,naloxonelaw','Policy2024-01 I(D);M.G.L.c94C§19B(e)','정책I(D)의reasonableeffort문언을읽었으나상위법§19B(e)는purchaser가out-of-pocket지불을요청한경우예외를명시한다. 현재본문과claim은보험확인의무를조건없이서술하여현금결제요청에도일률강제하는것으로읽힐수있다. 이예외누락의법적범위를정리하기전KEEP할수없다.')
add('w3-d-19',6,13,'naloxone','Policy2024-01 I(A),(E)–(G)','Insurancebilling구매자거래와NaloxoneRescueKitprofile/label표기,regulatoryquantity와보험limit구별,unitexpiry,counseling/pamphlet를직접확인했다. OTC승인으로이특정dispensingworkflow조건을없애지않는다.')
add('w3-d-20',1,3,'naloxone','Policy2024-01 II(A)','선호dailyPMP경로,data-collection목적,patientPMPprofile에미표시라는세문구를직접확인했다. 일반controlleddrug남용기록의근거로바꾸지않는다.')
add('w3-d-20',4,12,'naloxone','Policy2024-01 II(B)(1)–(3)','PMP미선택시직전calendar-year January15email보고와pharmacyname/ZIP,totaldoses/insurance-paiddoses필수항목을읽었다. Rx건수나manufacturerunit수를dose로동일시하지않는다.')
add('w3-d-20',13,17,'naloxone','Policy2024-01 II(B)(4)(i)–(iv),II(A)–(B)','Event별dose/date/recipientZIP/insurance는notrequired/encouraged로명시된다. 계정보유와실제naloxonedata전송은다르며아무경로도제출하지않는것은허용되지않는다.')
add('w3-d-21',1,5,'naloxone','Policy2024-01 III(A)','MAlicensedpharmacist가MAlicensedpharmacy와연계되고naloxonestored/dispensed인모든시간현장존재해야하는직접문언이다. 전화연락가능으로대체하지않는다.')
add('w3-d-21',6,12,'naloxone','Policy2024-01 III(B)–(E)','HIPAAprivacy,secure/encrypted/privateconnection,securestorage/constantobservation/licensedpersonnelaccess를각각직접대조했다. 장소변경으로이조건을없애지않는다.')
add('w3-d-21',13,14,'naloxone','Policy2024-01 III heading and III(A);opening paragraphs','이외부공간경로는naloxonepursuanttostandingorder에한정된다. 모든Rx행사장배포나technician-only행위의일반허가가아니고OTC제품일반retail과도구분한다.')
add('w3-d-22',1,10,'ept','Policy2020-08 opening,I(A)–(B),II(A)','Chlamydia진단자의partner를개별exam/testing없이치료하는한정경로와별도Rx,named또는EPT대체표기/profile/label을직접읽었다. 모든STI또는원환자Rx분할로확대하지않는다.')
add('w3-d-22',11,11,'conduct','247CMR9.01(9)','Fraudulent/deceptiveact금지를직접확인했다. 소프트웨어필드충족을위해모르는partnerDOB/주소를만들어내는것을EPT표기예외가허용하지않는다.')
add('w3-d-22',12,14,'ept','Policy2020-08 I(B),II(A)–(B)','Unable또는unwillingfill이면alternatepharmacyreferral이필수이며지정EPTidentifier는ordinaryname/address의명시적예외다. 일반이름부재만으로예외를무시하지않는다.')
add('w3-d-22',15,15,'conduct','247CMR9.17(1)–(2)','새Rx조제전DUR와reasonableeffort로drug/allergy/dose/directions등위험확인및적절조치규정을직접읽었다. EPT는가능한안전확인을전부면제하지않는다.')
add('w3-d-22',16,16,'ept,prescribing','Policy2020-08 opening and I;DCP26-08-125 STI(a)','진단된원환자의partner용처방을조제하는EPT와약사가직접평가한환자에게guidance로STI약을처방하는경로는대상·진단/처방주체가다르다.')
versions={
'cdtm':'PDF MA Register1354 dated2017-12-15; 조항별별도시행일미확정.',
'intern':'PDF4/25/25;8.01표시Effective1/9/25,8.02–8.04 correctedEffective4/6/18;세부개정최초효력일미확정.',
'conduct':'PDF Mass.Register1536 dated2024-12-06;조항별시행일미확정.',
'prescribing':'DCP26-08-125 dated2026-08-25; rescinds/replaces25-04-124;상위법개정관계모두확정한것아님.',
'administration':'DCP26-03-124 dated2026-03-11; replaces23-04-118.',
'ecorder':'현재FAQ가연결하는서명PDF;authorizingphysician2022-08-04. 별도갱신/expiry표시없음.',
'naloxone':'Policy2024-01 adopted2024-01-11,revised2025-02-06.',
'ept':'Policy2020-08 adopted2020-07-31.',
'opillorder':'현재DPH페이지는March2025경로로안내;실제order서명일2025-01-27.',
'opill':'FDAapprovalannouncement/contentcurrent2023-07-13;원approval은해당날짜. 최신개별label전문대조는아님.',
'planb':'FDA contentcurrent2022-12-23;OTCwithoutagerestrictionsapproval2013-06-20. 과거연령제한과구별.',
'ella':'DailyMed ELLA updated2026-07-20;initialUSapproval2010;labelrecentmajorchanges06/2021. 게시본효력범위만확인.',
'mifepristone':'FDA contentcurrent2026-04-08;REMSmodifiedJanuary2023;이번판정은회수된현재FDA설명한정.',
'oralprep':'현재index8-2026문서;본문/appendix전문회수. 별도법적시행일미확정.',
'pep':'현재index9-2026문서;본문/appendix전문회수. §6.3최대30일과Appendix2 28일문구불일치존재;별도법적시행일미확정.',
'sti':'현재index8-2026문서;별도법적시행일미확정.',
'doxypep':'현재index8-2026문서;별도법적시행일미확정.',
 'truvada':'MedlinePlus lastrevised2025-07-15;brand/ingredient매핑에한정하며별도법적효력일미확정.'}
metas={p.stem.removesuffix('.meta'):json.loads(p.read_bytes()) for p in (B/'sources').glob('*.meta.json') if 'raw_path' in json.loads(p.read_bytes())}
def authority(key,section):
 m=metas[key];return {'source_type':'PUBLIC_OFFICIAL','official_url':m['official_url'],'exact_section':section,'law_checked_date':'2026-11-04','version_or_effective_date_status':'2026-11-04 실제HTTPS GET200 회수. '+versions.get(key,'현재공식게시본문검토;페이지의별도효력일/조항최초시행일은확정하지않음.'),'evidence_path':m['raw_path'],'evidence_sha256':m['raw_sha256'],'text_path':m['text_path'],'text_sha256':m['text_sha256'],'retrieval_metadata_path':str(B/'sources'/(key+'.meta.json')),'retrieval_metadata_sha256':sha((B/'sources'/(key+'.meta.json')).read_bytes())}
resolved={('w3-d-12',24),('w5-b-2',13),*[('w5-b-4',n) for n in [7,9,13,15,17]]}
block_reasons={
'w3-d-8':'All-setting urgent절차가모든상황에일률적immediate법정clock을만드는지미확정;본문즉시의법적범위명료화필요.',
'w3-d-10':'16.01자체는purpose다. 전자CPAconfidentiality의본문인용근거/기술기준적용을확정하지않음.',
'authority-paths':'회수한Opill/PlanB외모든OTCproduct/form의판매조건전량은미검증.',
'w3-d-12':'개인MCSR한정면제와약국자체시설허가/등록전체는별개이며후자의current적용전량미대조.',
'w3-d-13':'현재§19F의후속clinicalvisit/timeframe금지조건과circularlackvisit/refills문구관계미해결.',
'w5-b-2':'VoluntaryECparticipation과모든reproductive-healthstock/access/대안의무의현재별도원문전체관계미검증.',
'w5-b-3':'이번EC경로의핵심과signedorder표를읽었지만제품별현행임상사용/반복간격전체알고리즘을별도확정하지않음.',
'w3-d-15':'공식ACCESS/MassHealth의일부보험용order존재는확인했으나payer별일반coverage조건전량을확정하지않음.',
'w3-d-16':'현재§19F권한확장개정관계/ICPE철자관계또는참조clinicalalgorithm의전체적용은미해결. 아래finding에claim별확인한범위를기록함.',
'hiv-protocol-open':'PEPcurrent본문최대30일과consent28일이일치하지않고fullcurrentauthority/참조clinicalalgorithm관계미확정;타주숫자대입금지.',
'w5-b-8':'현재FDA제품label/approval/applicationstatus또는MA대체법전체의추가공식1차대조필요. 제조사발표를법규authority로사용하지않음.'}
omissions={
'w3-d-8':['본문은 “약사는 CPA에 해당 환자의 범위와 구체적 delegation 규칙을 명시해야” 한다고 서술한다. Census009의 disease state/primary–co-morbid와023의 delegated duties 범위는 각각 질환과 직원 업무 위임을 열거하지만, CPA에 명시할 해당 환자의 범위라는 별도의 법적 내용을 직접 열거하지 않는다. 환자별 referral/consent와 일반 delegation scope는 동일 명제가 아니므로 해당 본문 명제의 정확한 환자 범위/setting 조건을 별도 열거·대조해야 한다.'],
'w3-d-22':['본문은 EPT에서도 “약물·지시·진정성·allergy concerns 등 가능한 안전 확인”을 유지한다고 명시한다. Census015는 drug/allergy 안전 검토를 열거하지만 prescription authenticity 확인이라는 별도의 조제 전 판단을 열거하지 않는다. Census011의 모르는 DOB/주소를 만들지 않는 의무도 처방 자체의 진정성 판단과 다르다. 현행247CMR9.15(2)(c)는 prescription authentic 판단을 직접 요구하므로 본문의 이 명제를 별도 열거해야 한다.']}
methods={
'w3-d-8':'본문의두24시간시계·actor/action·urgent조건,CPA(a)–(j),delegation,2년갱신,종료/기록·예시를전문대조했다. 환자범위와직원delegation범위를별도로추적했다.',
'w3-d-9':'표의10행·오답열을모두읽고written/signature/scope와위임가능불가능/언제방법기간범위,2년review-renew의부정예시를모든28claim과대조했다.',
'w3-d-10':'종료/미갱신의사전조치·서면통지,표의약사사본/의사원본과두Board접근,전자문맥,QA/CPA고용예시를모든26claim과대조했다.',
'authority-paths':'권한표5행·실제적용예시·prescribe/administer·lab/diagnosis·나이/질환/VI경계의전문을모든25명제와대조했다.',
'w3-d-12':'5문단의대체circular/대상/선택성,일반(a)–(j),single-locationMCSR와시설조건,MassHealthencouraged를모든25명제와대조했다.',
'w3-d-13':'5문단의age/product/form,selfscreening/currentMEC,12month/보험/expiry,lackvisit/refills,appointment와safety를19명제와대조했다.',
'w3-d-14':'Training5목표와권고accreditation/증빙,고정2시간부재,assessment부터record/referral까지20명제와대조했다.',
'w5-b-2':'세문단의EC2성분·교육·자발성·다른접근의무·환자별평가/Rx/fill/label/records와signedorder범위를14명제와대조했다.',
'w5-b-3':'환자평가/thirdparty/OTC,minorconsent,privacy/communication,antiemetic/구토/advance와sexualassaultreferral를13명제와대조했다.',
'w5-b-4':'연간보고문단·5행제품표·보험과OTC/REMS/다른성분경계를17명제와대조했다. 표의성분과법적status를별도공식문서로대조했다.',
'w5-b-5':'3문단의trial/동일약/보험유형,제형coverage와처방권한,Opill보험order와assessment/record층을9명제와대조했다.',
'w3-d-15':'4문단의Opilldaily/PlanBOTC연령/EC와abortion/ellaRx와보험경로를15명제와대조했다.',
'w3-d-16':'5문단의PrEP/PEP목적,교육목표/2시간/accreditation철자와증빙,STI별guidance와patienteligibility주의를28명제와대조했다.',
'hiv-protocol-open':'본문의실제확인범위와과거403한계·공통요건·protocol별검사/공급숫자추정금지를13명제와대조했다. 이번네DOCX신규회수사실은과거작성시점한계와구별했다.',
'w5-b-8':'세문단의브랜드별성분/제형/indication,치료와예방,weeklyapplication과loading/bridging/approval상태를19명제와대조했다.',
'w3-d-18':'OTC와보험order,thirdparty/patient-specific/order,apparentoverdose면책한계를7명제와대조했다.',
'w3-d-19':'4문단의stock/offertrigger,insurance·profile/label,quantity와insurance,expiry/counseling/pamphlet를13명제와대조했다. 보험확인의무는별도상위법현금요청예외까지대조했다.',
'w3-d-20':'4문단의daily/annual대안·January15/전년도·dose와Rx/package·필수필드/encouragedevent필드·계정보유와실제제출을17명제와대조했다.',
'w3-d-21':'3문단의remote현장/연계면허,privacy/technology3조건,securestorage/observation/handling,OTC와특정exception를14명제와대조했다.',
'w3-d-22':'5문단의chlamydia/partner/exam/test,별도Rx,named/unnamed/profile/label,허위신원/referral/safety와directSTIprescribing구별을16명제와대조했다. Drug/allergy와Rxauthenticity의서로다른의무를분리했다.'}
records=[];resolution_log=[]
for u in packet['units']:
 uid=u['unit']['id'];bind=job['unit_bindings'][uid];claims=[]
 for c in u['claims']:
  n=int(c['claim_id'].rsplit('-',1)[1]);keys,section,finding=spec[(uid,n)];status='SOURCE_BLOCKED' if c['review_status']=='SOURCE_BLOCKED' and (uid,n) not in resolved else 'KEEP'
  if uid=='w3-d-19' and n==5:status='LEGAL_HOLD'
  if uid=='w3-d-12' and n in [5,6]:status='SOURCE_BLOCKED';finding+=' 이두개별claim은HIV/STI의실제처방경로라는법적내용이므로§19F권한확장개정관계미해결을같이SOURCE_BLOCKED로반영한다.'
  e={'claim_id':c['claim_id'],'claim_record_sha256':bind['claim_record_sha256s'][c['claim_id']],'claim_read_completely':True,'statement_reviewed_ko':c['statement_ko'],'legal_status':status,'finding':finding+' 개별대조명제: '+c['statement_ko'],'authorities':[authority(k,section) for k in keys]}
  if status!='KEEP':e['blocker']=('M.G.L.c94C§19B(e)의purchaser-requestedout-of-pocket예외를본문·명제에반영하는법규adjudication필요.' if status=='LEGAL_HOLD' else block_reasons[uid])
  if uid=='w3-d-12' and n in [5,6]:e['blocker']='Circular/index는HIV/STI처방권한을§19F에귀속하지만현재게시§19F는contraception만기술한다. 추가sessionlaw/위임/개정관계의공식원문대조전법적처방경로를확정하지않음.'
  if (uid,n) in resolved:
   e['author_source_block_independent_reassessment']='저자SOURCE_BLOCKED표시를자동승계또는자동해제하지않고이번실제회수공식원문과개별명제를직접대조해이한정명제의근거를확인했다. 기존독립감사carriedlegalblocker해제가아니다.';resolution_log.append(c['claim_id'])
  claims.append(e)
 om=omissions.get(uid,[]);status='LEGAL_HOLD' if om or any(c['legal_status']=='LEGAL_HOLD' for c in claims) else 'SOURCE_BLOCKED' if any(c['legal_status']=='SOURCE_BLOCKED' for c in claims) else 'KEEP'
 records.append({'unit_id':uid,'binding':bind,'body_read_completely':True,'completeness':'OMISSIONS_FOUND' if om else 'COMPLETE','completeness_method':methods[uid]+' 법적주체·행위·시작점·수치·예외·부정문·표각행을현재본문과census양방향으로추적했다. 관련81문항전체stem/선택지/key/전체해설과9derived의가시문구를읽었으며문항의추가가정으로본문누락을메우지않았다.','omissions':om,'legal_status':status,'claims':claims,'related_question_ids_read':sorted({qid for c in u['claims'] for qid in c.get('related_question_ids',[])}),'independent_unit_finding':methods[uid]})
prov={k:job[k] for k in ['stage','actor_provenance','auditor','auditor_instance']};prov.update(independent_of_authors=True,canonical_audit=False,canonical_release_credit=0,question_audit_credit=0)
report={**prov,'checked_at':'2026-11-04','records':records,'input_provenance':{'source_head':packet['source_head'],'body_and_census_hash_checks':'input-validation.json','root_strict_inventory_projection_is_not_legal_pass':True,'loader_guard_bypass':False},'related_surface_review':{'assigned_question_count':78,'body_additional_question_count':3,'total_original_questions_read':81,'all_stems_choices_keys_full_explanations_read':True,'derived_count':9,'all_derived_visible_text_read':True,'finding':'문항들의public-healthworkqueue/casefamily구조와추가가정을읽었다. Related연결은specificdecisionfamily관련성이지모든claim의각숫자/예외를직접출제한다는증거가아니다. RW0026/0029/0041등타주제보기도읽었지만별도법규독립인증이나questioncredit를이감사에추가하지않았다. 9derived는overview/contrast/recall한계를유지하며HIV/STIOPEN을대체하지않는다.','source_context_raw_sha256':sha((B/'related-context.json').read_bytes())},'author_source_blocks_independently_supported_by_new_primary_reading':resolution_log,'current_primary_limitations':['현재네HIVDOCX는모두실제HTTPS200으로회수해본문/표/appendix를읽었다. 과거본문의2026-10-23 403기록을현재실패라고다시주장하지않는다. 새회수만으로기존권한개정관계/clinicalalgorithm전체OPEN을해제하지않았다.','PEP§6.3 maximum30days와Appendix2 28days가동시에게시되어있다. 타주숫자또는일반CDC권고로한숫자를임의확정하지않는다.','제조사Gilead발표를공식legalauthority로사용하지않았다. FDA제품별approval/applicationstatus미확정은SOURCE_BLOCKED로남는다.','모든본작업source는이번실제HTTPSGET이다. 내부same-daycache를fresh로표시하지않았다. 처음잘못된247CMR9URL의404attempt도별도metadata에보존했다.','본문/census/queue/ledger/loader/생성물/원보고서수정과question/canonicalreleasecredit는없다.']}
(B/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');result={**prov,'worker_commit':'0'*40,'unit_hashes':{uid:b['body_sha256'] for uid,b in job['unit_bindings'].items()},'evidence':{'path':str(B/'report.json'),'raw_sha256':sha((B/'report.json').read_bytes())},'result_path':q.OUTPUT+job['job_id']+'-result.json','results':[{k:r[k] for k in ['unit_id','completeness','legal_status']} for r in records]};q.validate_result(job,result);q.validate_evidence(job,result,report);Path('/tmp/notes120-b-precommit-envelope.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
counts={'units':dict(collections.Counter(r['legal_status'] for r in records)),'completeness':dict(collections.Counter(r['completeness'] for r in records)),'claims':dict(collections.Counter(c['legal_status'] for r in records for c in r['claims']))};(B/'review-counts.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2)+'\n');print(json.dumps(counts,ensure_ascii=False));print('native validate_result/evidence PASS')
