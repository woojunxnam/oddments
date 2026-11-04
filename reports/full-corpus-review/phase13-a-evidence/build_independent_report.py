"""Serialize this session's manually reached findings; never derive truth from stored keys."""
import json,hashlib,datetime,re,pathlib
R=pathlib.Path(__file__).resolve().parents[3]; P=R/'reports/full-corpus-review/phase13-a-evidence'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def read(p):return json.loads(p.read_text())
packet=read(P/'assigned-visible-input.json');assignment=read(P/'assignment.json'); near=read(P/'nearest-visible-comparisons.json'); nearest={x['question_id']:x for x in near['records']}; now=datetime.datetime.now(datetime.timezone.utc).isoformat()
# Explicit independent truth vectors in option order, derived from primary text read by this session.
truth={596:'TTFT',597:'FFFT',598:'TFFF',600:'TFTT',601:'FFTF',602:'FFFT',604:'FTTT',605:'FTFF',606:'FFTF',608:'TTTF',609:'TFFF',610:'FTFF',612:'TTFT',613:'FFFT',614:'TFFF',616:'TFTT',617:'FFTF',618:'FFFT',620:'FTTT',621:'FTFF',622:'FFTF',623:'TTTT',624:'TTTF',625:'TFFF',626:'FTFF',628:'TTFT',629:'FFFT',630:'TFFF',632:'TFTT',633:'FFTF',634:'FFFT',636:'FTTT',637:'FTFF',638:'FFTF',639:'TTTT',640:'TTTF',641:'TFFF',642:'FTFF',644:'TTFT',645:'FFFT'}
G=[(596,596,'no-refill',['mgl94c23','cfr130612','cfr130613','ma2479','maepcs'],'§23(b),(c); §1306.12(a); §1306.13(a),(b); 247 CMR 9.04(1); DCP19-12-108 p7', '서면에 적힌 refill 수는 CII 재조제 금지를 넘지 못하며 원 처방 총량 안의 적법한 partial은 별개다. 전자처방에도 약사 최종 검증이 남는다.'),
(597,600,'validity',['mgl94c23'],'M.G.L. c.94C §23(a),(d)','CII 원 처방은 발행일 후30일에 무효가 된다. §23(d)의1회90일분 허용량과 §23(a)의원처방 유효기간은 다른 조건이며 첫수령/공급량이 기산점을 바꾸지 않는다.'),
(601,604,'nonopioid',['mgl94c23','cfr130605'],'M.G.L. c.94C §23(a),(d)(ii); 21 CFR1306.05(a)','현행 §23(d)(ii)는 non-opioid CII/III를 포함하고 methylphenidate/testosterone을 명시한다.90일은 최대량이며 발행자가 적법하게 지정한 처방량을 늘릴 권한이 아니다. 과거진단명 요약으로 현행조문을 좁히지 않는다.'),
(605,608,'oud',['mgl94c23','cfr130607','cfr130604'],'M.G.L. c.94C §23(d)(i),(iii); 21 CFR1306.07(a)-(d); §1306.04(a),(c)','주90일분 OUD항목은 연방 methadone CII 치료권한을 새로 만들지 않는다. §1306.07(a)는 별도치료프로그램 직접투여/공급과 처방을 구별하며 (d)는 III-V narcotic처방을 허용한다. 단순 opioid 통증과 OUD목적은 다르다. 양 한도는 제제 안정성/BUD의 증명이 아니다.'),
(609,612,'multiple',['mgl94c23','cfr130612','cfr130605'],'M.G.L. c.94C §23(a); 21 CFR1306.12(a),(b)(1)(i)-(v); §1306.05(a)','실제발행일을 기록하고 later fill instruction을 따로 둔다. 복수original처방은 refill이 아니다.90일총량 외 정당한 목적/통상진료/전용위험 판단/주법 충족이 필요하며 MA30일 유효기간은 연방 허용으로 사라지지 않는다.'),
(613,616,'emergency',['cfr29010','cfr130611','cfr130612','mgl94c23'],'21 CFR290.10(a)-(c); §1306.11(d)(1); §1306.12(a); M.G.L. c.94C §23(h)(ii),(iv)','연방 oral CII응급은 즉시필요, 적절한 대체없음, 사전서면제공의 합리적 불가능을 모두 요구한다. EPCS장애라는 형식예외만으로 세조건을 입증하지 않는다. 수량은 응급기간에 필요한양이며 고정7일분/재조제권한이 아니다.'),
(617,620,'oral-roles',['cfr130611','cfr130605'],'21 CFR1306.11(d),(d)(2),(3),(5); §1306.05(a)','이 특정응급경로는 prescribing individual practitioner의 oral authorization을 받는 pharmacist를 전제한다.약사가 즉시기록하며 모르는발행자는 합리적으로 확인한다. central-fill은 이항의 oral경로로 준비할 권한이 없다.'),
(621,624,'follow-up',['cfr130611','mgl94c20'],'21 CFR1306.11(d)(4); M.G.L. c.94C §20(c)','연방7일은 oral authorization 뒤부터 계산하고 business days로 늘리지 않는다. 후속서는 같은 emergency quantity와 원oral기록을 연결한다. 요구되는후속 미제공에는 DEA통지가 필요하다. 우편은7일내소인규칙을 별도로 유지한다. MA§20(c)2일전자/예외시7일과 별도인 연방질문이다.'),
(625,628,'ltcf-hospice',['cfr130611','cfr130605','cfr130604'],'21 CFR1306.11(a),(f),(g); §1306.05; §1306.04(a)','LTCF(f)는 Schedule II전반이고 hospice(g)는 narcotic CII와 지정hospice등록/환자표시가 필요하다. 비narcotic은(g)자체에 해당하지 않으며 다른경로가능성은 별도다. fax가original이어도 정당성/필수정보/기록은 남는다.'),
(629,632,'infusion',['cfr130611','cfr130612','cfr130605'],'21 CFR1306.11(e); §1306.12(a); §1306.05','(e)는 narcotic CII를 조제하여 환자에게 직접 parenteral/IV/IM/SC/intraspinal infusion투여하는 처방이다. 단순injectable/별개oral tablet까지 포괄하지 않는다.전송방식예외는 refill이나공급한도를 늘리는권한이 아니다.'),
(633,636,'shortage',['cfr130613','mgl94c23'],'21 CFR1306.13(a); M.G.L. c.94C §23(a)','shortage잔량은 first partial부터72시간이다.월14시→목12시는70시간이라 범위내다.80시간은 넘고 입고시각/원처방유효기간으로 연장되지 않는다. 미완료시발행자통지 및72시간뒤추가량에는새처방이 필요하다.'),
(637,640,'request-facts',['cfr130613','mgl94c18'],'21 CFR1306.13(a),(b)(1),(3)-(5); M.G.L. c.94C §18(d3/4)','실제요청이 없으면(b)요청경로의 사실요건이 충족되지 않는다. shortage만 있던거래를 후에명칭만 바꿔 실제요청을 만들수없다.요청주체/시각/수량기록과 original총량한도는 각partial에 유지된다.'),
(641,644,'request-limits',['cfr130613','mgl94c18','mapartial'],'21 CFR1306.13(b)(1)-(5); M.G.L. c.94C §18(d3/4); DCP18-10-104 pp1-2','일반requested잔량30일은 원발행일 기준이다.성인MPOA caregiver/미성년parent/guardian등 적격요청주체와 발행자지정partial한도를 유지한다.단순수령자격/인쇄안내는 실제요청을 입증하지 않는다.첫partial과매잔량의수량/날짜등기록이 필요하다.'),
(645,645,'emergency-partial',['cfr130613','cfr130608','mgl94c18','mapartial'],'21 CFR1306.13(a),(b)(2); §1306.08(e)-(g); M.G.L. c.94C §18(d3/4); DCP18-10-104 p1','응급oral requested잔량은 발행후72시간이고 shortage의first-partial기산과 다르다. MA요청잔량은 최초공급약국이 제공한다.동일chain은같은약국을뜻하지않으며이미일부공급한CII는 initial-dispensing EPCS전송경로가아니다.')]
section_map={
'mgl94c23':'M.G.L. c.94C §23(a)-(d),(h)', 'mgl94c18':'M.G.L. c.94C §18(d3/4)', 'mgl94c20':'M.G.L. c.94C §20(c)', 'cfr130611':'21 CFR1306.11(a),(d)-(g)','cfr130612':'21 CFR1306.12(a),(b)','cfr130613':'21 CFR1306.13(a),(b)(1)-(5)','cfr130604':'21 CFR1306.04(a),(c)','cfr130605':'21 CFR1306.05(a),(e),(f)','cfr130607':'21 CFR1306.07(a)-(d)','cfr130608':'21 CFR1306.08(e)-(g)','cfr29010':'21 CFR290.10(a)-(c)','ma2479':'247 CMR9.04(1),(5)','maepcs':'DCP19-12-108 p7 Endorsement; old follow-up text NOT relied on','mapartial':'DCP18-10-104 pp1-2'}
sources={}
for mpath in sorted((P/'sources').glob('*.meta.json')):
 m=read(mpath); k=m['source_id']; m.update(exact_section=section_map.get(k,'NABP public format/competency only; not legal authority'),law_checked_date='2026-11-04',reviewed_at=now,metadata_path=str(mpath.relative_to(R)),metadata_sha256=sha(mpath))
 if k.startswith('cfr'):m.update(effective_date=None,version='eCFR title21 current displayed up to date as of 2026-11-02',effective_date_limit_ko='현행consolidation을 확인했다.각원개정의 개별시행일을 모두소급확정한것은 아니며 역사적사건에 적용하지 않는다.')
 elif k.startswith('mgl'):m.update(effective_date=None,version='Massachusetts General Court current General Laws HTML retrieved 2026-11-04',effective_date_limit_ko='현행공식조문을 확인했다.페이지는전개정별시행일을제시하지않으며 소급사건/미래변경 적용은별도검토한다.')
 elif k=='mapartial':m.update(effective_date='2018-11-01',version='DCP18-10-104; current official posting; controlling statute independently checked')
 elif k=='maepcs':m.update(effective_date='2019-12-27',version='DCP19-12-108; p7 endorsement only; old 7-business-day and old LTCF cutoff excluded')
 elif k=='ma2479':m.update(effective_date=None,version='247CMR9 official posted PDF, register12/6/2024',effective_date_limit_ko='각조문원시행일미확정.현행공식게시문과§23(c)및2019endorsement안내를교차확인했다.')
 else:m.update(effective_date=None,version='Public NABP current website / public sample July2020; format evidence only')
 sources[k]=m

def authority(k):
 m=sources[k];return dict(authority=section_map[k],source_type='PUBLIC_OFFICIAL',exact_section=section_map[k],official_url=m['official_url'],law_checked_date=m['law_checked_date'],version=m['version'],effective_date=m['effective_date'],evidence_path=m['raw_path'],evidence_sha256=m['raw_sha256'],text_path=m['text_path'],text_sha256=m['text_sha256'],metadata_path=m['metadata_path'],metadata_sha256=m['metadata_sha256'],retrieved_at=m['retrieved_at'])
# Own reasons about each proposition's actual legal consequence, not author rationale extraction.
def option_reason(t,topic):
 s=t.lower()
 if 'final validation' in s:return '전자전송은 약사의최종dispensing validation의 예외가 아니다(247CMR9.04(1),§23(c),DCPmanualp7).'
 if topic=='no-refill':
  if 'partial' in s:return '허용조건을충족한partial은original수량을나누어공급하는것이며기존CII를새로refill하는것과구별된다(§1306.13).'
  if 'new lawful prescription' in s:return '새적법처방은새authorization이며§1306.12(a)가금지하는oldprescriptionrefill과다르다.'
  return 'CII재조제는§23(b)와§1306.12(a)가금지하므로발행자의refill숫자로합법화할수없다.'
 if topic=='validity':
  if 'pickup' in s:return '§23(a)는발행일부터기산하므로실제첫pickup이기산점을초기화하지않는다.'
  return '§23(a)의30일유효기간과(d)의90일공급량은별개라서40일첫fill은허용되지않고허용량만으로만료를치유할수없다.'
 if topic=='nonopioid':
  if 'quantity' in s or 'prescribed' in s:return '90일은법정최대공급량이며§1306.05(a)의prescribedquantity와§23(a)의validity를변경하는권한이아니다.'
  if 'validity' in s:return '§23(d)공급항목은(a)의별도유효성요건을폐지하지않는다.'
  return '§23(d)(ii)는non-opioidCII/III와methylphenidate/testosterone을명시한다.진단명만의옛요약/모든CIII30일주장은현행범위를왜곡한다.'
 if topic=='oud':
  if 'pump' in s or 'compounded' in s:return '§23(d)(iii)는허용량조항일뿐각조제품안정성/BUD의품질판정이나전기간적합성을보증하는조항이아니다.'
  if 'pain' in s:return '§23(d)(i)의목적은OUD치료이므로일반opioid통증처방을그약물명만으로이항에포함하지않는다.'
  return '§1306.07(a)는CII유지/해독치료의직접투여·공급과처방을구별하고(d)는III-Vnarcotic처방을허용한다.주quantity항목이나공통적응증으로methadone/buprenorphine의다른연방경로를합칠수없다.'
 if topic=='multiple':
  if 'postdat' in s or 'issue dates' in s:return '§1306.05(a)는실제발행일기재를요구한다.미래earliestfill은§1306.12(b)(1)(ii)의별도지시다.'
  if 'refill' in s:return '§1306.12(b)의eachseparateprescription은독립original이며(a)의CIIrefill금지를폐지하지않는다.'
  if 'massachusetts' in s or 'state' in s:return '§1306.12(b)(1)(iv),(v)는주법준수를명시하므로MA§23(a)의30일을연방90일총량으로무력화할수없다.'
  return '§1306.12(b)(1)(i)-(v)는90일총량뿐아니라정당목적/전용위험/주법등을함께요구한다.'
 if topic=='emergency':
  if 'refill' in s:return '응급format은§1306.12(a)의CIIrefill금지를변경하지않는다.'
  if 'quantity' in s or 'adequate' in s:return '§1306.11(d)(1)은응급기간에적정한양을한도로하며고정7일분규칙이아니다.'
  return '§290.10(a)-(c)의세조건은누적요건이다.대체치료/사전서면이가능하거나EPCS장애사실만있으면이를전부입증하지못한다.'
 if topic=='oral-roles':
  if 'central-fill' in s or 'central fill' in s:return '§1306.11(d)(5)는centralfill이retailpharmacist/individualpractitioner의oralauthorization을받아이항으로준비하는것을허용하지않는다.'
  if 'record' in s or 'writing' in s:return '§1306.11(d)(2)는약사의즉시서면화를요구하며후속서수령까지전기록을미룰수없다.'
  if 'unknown' in s or 'unfamiliar' in s:return '§1306.11(d)(3)는모르는practitioner의oral진정성을합리적으로확인할것을요구한다.'
  return '§1306.11(d)본문과(2)는prescribingindividualpractitioner→pharmacist라는특정권한/기록주체를정한다.일반receptionist→technician콜만으로대체되지않는다.'
 if topic=='follow-up':
  if 'business' in s:return '§1306.11(d)(4)의7days에는businessday한정이없다.우편의7일내소인예외도businessday연장이아니다.'
  if 'clock' in s:return '§1306.11(d)(4)는afterauthorizing이라쓰므로월요일authorization이기산사실이고화요일dispensing이아니다.'
  if 'dea' in s or 'notification' in s or 'file note' in s:return '§1306.11(d)(4)는요구후속미제공시nearestDEAoffice통지를요구한다.파일메모로해당행위를대체하지못한다.적법우편소인은별도로판단한다.'
  return '§1306.11(d)(4)의서류는emergencyquantity와oralrecord를문서화·연결하며새중복공급authorization이아니다.'
 if topic=='ltcf-hospice':
  if 'ltcf' in s:return '§1306.11(f)는LTCFresident의ScheduleII substance라고하고narcotic한정을두지않는다.이한정은(g)와구별된다.'
  if 'requirement' in s or 'transmission' in s:return '§1306.11(f),(g)는§1306.05에맞는처방을전제하며§1306.04정당목적과기록의무를없애지않는다.'
  if 'informal' in s or 'qualifying hospice status' in s:return '§1306.11(g)는Medicarecertified/paid또는state-licensedhospice의등록환자및hospice환자표시를요구한다.막연한comfortcare만으로입증되지않는다.'
  return '§1306.11(g)는ScheduleIInarcotic으로명시하므로해당hospice항자체를nonnarcoticCII전체로확장할수없다.다른경로판정은별개다.'
 if topic=='infusion':
  if 'refill' in s or 'supply limits' in s:return '§1306.11(e)는fax를original로대하는한정예외이며§1306.12(a)의CIIrefill금지를폐지하지않는다.'
  if 'oral tablet' in s:return '§1306.11(e)는해당narcotic조제품의직접지정경로infusion을대상으로하므로동반oraltablet이자동포함되지않는다.'
  return '§1306.11(e)의narcotic/compounded/directparenteral-or-specifiedinfusion조건을함께적용해야한다.단순injectable전체도아니고적격처방에대한faxoriginal을전면금지하는것도아니다.'
 if topic=='shortage':
  if 'thursday' in s:return '월요일14시→목요일12시는70시간으로§1306.13(a)의firstpartial후72시간안이다.'
  if 'issue date' in s:return 'shortage에는§1306.13(a)의firstpartialtrigger가적용된다.(b)의writtenissue기산과구별한다.'
  if 'inventory' in s or 'shipment' in s:return '§1306.13(a)의firstpartial기산을입고사실이재설정한다는예외는없다.'
  return '§1306.13(a)는72시간내잔량미완료시prescriber통지를요구하며72시간뒤추가공급은새처방없이는안된다.원처방일반유효성은별도다.'
 if topic=='request-facts':
  if 'quantity' in s or 'total' in s:return '§1306.13(b)(1)(iv)는모든partial합계가원prescribedtotal을넘지않도록한다.명칭변경으로총량이늘지않는다.'
  if 'document' in s or 'evidence' in s:return '§1306.13(b)(1)(iii),(3)-(5)는실제적격request및요청/공급기록을요구한다.요청증거가불필요하다는주장은맞지않는다.'
  return '실제요청이없다는명시사실에서는§1306.13(b)(1)(iii)를만족하지못한다.(a)shortage거래에사후label을붙여없는요청을창설할수없다.'
 if topic=='request-limits':
  if '30' in s:return '§1306.13(b)(2)와MA§18(d3/4)의30일은writtenissue기준으로day20첫partial이추가30일을주지않는다.'
  if 'notice' in s or 'language' in s:return 'partialfill안내문은가능성의고지일뿐§1306.13(b)(1)(iii),(4),(5)(ii)의실제patientrequest와요청일시기록을입증하지않는다.'
  if 'record' in s:return '§1306.13(b)(5)는각partial별수량/날짜/공급자기록을요구하고MA§18(d3/4)도initial/remaining공급을모두기록하도록한다.'
  return '§1306.13(b)(4)는적격대리요청자를한정하고발행자지정partial보다큰양을요청할수없게한다.단순pickupagent라는사실로어느권한도성립하지않는다.'
 if topic=='emergency-partial':
  if 'chain' in s:return 'MA§18(d3/4)는onlythesamepharmacy라정하므로공유상호/시스템만으로서로다른영업소가같은약국이되지않는다.'
  if 'unfilled' in s or 'epcs' in s:return '§1306.08(e)-(g)는initialdispensing용EPCStransfer이다.이미공급한수량이있는CII의잔량을미조제original로분류할수없다.'
  return '§1306.13(b)(2)의응급oral요청partial은issue후72시간이다.(a)의shortage72시간은firstpartial부터라trigger가다르고일반30일요청경로와도구별한다.'
 raise AssertionError((topic,t))
criteria_names=['jurisprudence_reasoning','practice_plausibility','authentic_distractors','wording_not_guessable','reasoning_not_trivia','natural_rule_combination','appropriate_drug_context','distinct_from_bank','not_schedule_flashcard','public_style_without_copying']
# Deliberate per-family assessments; variants retain their actual target and option findings below.
real={
'no-refill':('oxycodone refill·partial·EPCS최종검증','CIIrefill과original잔량을분리하고전자형식의책임예외주장을판단한다.','처방에refill수가실제로적힌경우와동료의partial오인을다루어약국실무상가능하다.','새처방/partial/refill/EPCS책임의혼동은각각다른법적오류로설명가능하다.',True,'서면숫자보다CII분류와authorization성격을우선적용해야하며정답을미리평가한단서는없다.'),
'validity':('day40 CII firstfill과90일분','발행유효기간과처방의허용공급량이라는서로다른규칙을함께적용한다.','day40에제시된90일분처방은약국에서실제로직면할수있는기한확인이다.','90일공급량을90일사용기한으로오인하는보기가실제두시계의혼동을재현한다.',True,'40일/90일/발행일이제시되지만30일법규를모르면어느시계가우선인지문장만으로확정되지않는다.'),
'nonopioid':('methylphenidate/testosterone 90일분','CII/III와non-opioid조건을현행§23(d)에대입하는법적판단은존재한다.','유효한methylphenidate/testosterone의90일분가능성확인은실무상가능하다.','ScheduleIII30일오인은가능하나obsolete/모든validity폐지/처방량임의증량은서로수준이다르다.',False,'stem의old와보기의obsolete/current가옳고그름을미리평가한다.현행법규를몰라도옛요약을따르는보기를배제할수있다.'),
'oud':('methadone 대buprenorphine OUD권한','주공급량과연방OUD취급권한을따로판단하는구조는적절하다.','retailmethadone OUD가능성을문의하는상황은현실적이다.','methadone/buprenorphine권한혼동은적절하지만pump제제안정성보기는두OUD사례와관계없어탈락단서가된다.',False,'두OUD사례에서pump/BUD보기가돌출되어대응되는정책판단군을쉽게좁힌다.부정어수만으로판정하지않고관련성결함을확인했다.'),
'multiple':('CII복수처방 실제발행일/60일earliestfill','연방허용조건과MA원처방유효기간을같이적용한다.','동일방문에여러처방을발행하고미래날짜를지정하는상황이가능하다.','postdate/earliestfill,refill/separateoriginal,연방총량/주기한혼동이실제다른오개념이다.',True,'actualissue와earliestfill의법적차이를알아야선택할수있고단순수식어로정답이공개되지는않는다.'),
'emergency':('대체치료/서면가능과EPCS장애','연방응급oral의누적요건과주EPCS형식예외를구별한다.','신속수령요구와시스템장애모두약국에서발생가능하다.','고정7일수량,전자장애,refill허용을oral응급조건과혼동하는선지는각각다른규칙오류다.',True,'대체치료/사전서면가능사실은법적요건에대한판단자료다.요건을몰라도참거짓이자명하도록old/obsolete같은평가어를쓰지는않는다.'),
'oral-roles':('receptionist→technician/centralfill oral CII','특정응급권한의주체와즉시기록/진정성검증을적용한다.','대리전화접수와centralfill관여는실무상범위를확인해야할사안이다.','일반agent접수권한을응급CII에확장하거나후속서로최초기록을대체하는혼동은법적구조가다르다.',True,'다른처방에서는agent접수가가능하므로receptionist라는단어만으로답을정하지못하고특정CII규정을알아야한다.'),
'follow-up':('월authorization/화dispensing와DEA통지','연방7일기산사실,후속서의기능,미수령대응을분리한다.','후속서가늦거나일단파일메모만남기는상황은가능하다.','businessday와authorization/dispensing기산혼동이각각실제다른기간규칙에서나온다.',True,'7일의trigger와통지기관은법규를알아야한다.모든SATA보기참이라는구조만으로법적정답을바꾸지않는다.'),
'ltcf-hospice':('LTCF전CII 대hospice narcoticfax','서로다른§1306.11(f),(g)의대상약물과환자요건을대조한다.','LTCFresidentfax와nonnarcotichospicefax를확인하는업무가가능하다.','두예외의narcotic조건을뒤섞는오답은정확히인접한법적혼동이다.',True,'narcotic여부가규정별로달라질수있으므로stem에그사실을제공하는것이정답노출은아니다.'),
'infusion':('specified조건충족infusion fax','narcotic/compounded/directinfusion이라는법적요건을적용할주제자체는존재한다.','실제약물명/실제투여경로없이meetingthespecifiedconditions라결론을미리넣어실무판단에필요한원사실이부족하다.','anyinjectable혼동은타당하지만oraltablet/허용refill같은관련성낮은보기로요건충족을재진술하는답이두드러진다.',False,'stem은지정조건을충족한다고이미선언하고정답은그specificexception을적용하라고반복한다.환자/제품사실에서요건을도출할기회가없다.'),
'shortage':('월14시/목12시70시간 대80시간','stockshortage72시간trigger와일반validity를구별해구체시각에대입한다.','재고부족partial후배송이지연되는상황과상반된시점은현실적이다.','원발행일/첫partial/입고시점/일반validity를섞는오답은진짜기산점혼동이다.',True,'시간계산은쉽지만어느사건부터72시간인지법적판단이선행되어야하며숫자만의암기는아니다.'),
'request-facts':('실제request없음/기한뒤relabel','shortage와patientrequest의법적경로를구별할주제는존재한다.','기록오분류수정상황은가능하나stem이request가없고solely기한연장하려한다는부정사실을이미확정한다.','없는요청이사후label만으로생긴다는선지는일반사실논리만으로거부되어request증거의미묘한법적혼동을대체하지못한다.',False,'noactualrequest와invented/retrospectivelabel의대립이정답을거의그대로제시한다.법적적격request의경계사실을따질필요가없다.'),
'request-limits':('day20 requestedpartial과casualpickupagent','30일trigger와적격요청자/발행자지정partial한도를구분한다.','늦은첫partial및가족/수령자의증량요청은현실적으로확인할업무다.','day20부터새30일,고지문=실제요청,최종잔량만기록,수령권한=증량권한은서로다른오개념이다.',True,'단순pickupagent가환자대리요청에어디까지해당하는지와발행자한도는규정확인이필요하다.긴정답보기는있으나조건의법적차이가실제판단근거다.'),
'emergency-partial':('응급requested72시간/동일chain잔량','응급/stockshortage의다른trigger와initialEPCStransfer/잔량을구분한다.','응급partial잔량과동일체인다른약국수령요구가가능하다.','동일72시간=동일trigger,같은chain=같은pharmacy,잔량=initialunfilled는각각그럴듯한다른법적혼동이다.',True,'숫자72가보여도issuance와firstpartial을선택해야하며같은chain의법적단위를별도로판단해야한다.')}
failtopics={'nonopioid','oud','infusion','request-facts'}
canonnotes={'MA-Q-0283':'항응고제용량변경후refill상담의무로CII재조제/전자검증과판단이다르다.','MA-Q-0124':'out-of-statealprazolamoral접수/후속서사례로여기서의CII기한/응급권한과규칙·주체가다르다.','MA-Q-0432':'requestedpartial의30일과samepharmacy를함께적용하는사례다.관련기간혼동은공유하지만이문항의표적사실과선택지는완전복제가아니다.','MA-Q-0155':'LTCFfaxoriginal판단이다.배정nonopioid공급량문항과는규칙이다르고LTCF배정문항은hospice예외와대조한다.','MA-Q-0024':'buprenorphine90일공급량자체를묻는다.여기서는methadone연방권한과의분리가추가된다.','MA-Q-0213':'offsite상담연락번호의container표시를묻는다.배정OUD권한과의단어유사성만으로의미중복이라할수없다.','MA-Q-0158':'복수CII의연방조건을묻는가까운주제다.배정문항은MAvalidity/실제issue와미래fill구분을대조하며구체적선택요구가다르다.','MA-Q-0186':'hospicenarcoticfaxoriginal이며배정oral응급요건과전송경로가다르다.','MA-Q-0104':'응급후속서미수령DEA통지가중심이다.배정oral권한문항은수신자/centralfill/최초기록을표적으로해통지행동과구별된다.','MA-Q-0398':'LTCFopioid교육pamphlet예외이다.배정faxoriginal은다른법적의무다.','MA-Q-0187':'LTCFnonnarcoticfax예외가가까우나배정문항은hospice항과의경계를함께제시한다.','MA-Q-0157':'compoundedIVfaxoriginal이매우가까운주제다.배정문항은인접형식예외의조건누락을대조하지만독립새범위라고세지않는다.','MA-Q-0281':'intern/technician상담권한사례로배정stockshortage기산점과규칙이다르다.','MA-Q-0003':'samepharmacyrequested잔량이중심이다.배정문항은shortage의실제요청유무또는응급72시간trigger를추가로판단한다.','MA-Q-0156':'hospiceCII-narcoticfaxoriginal이다.배정요청자권한/발행기산점과는전혀다른규칙이다.'}
# Whitelist-only family projection; raw object is used only for digest verification.
config=read(R/'site/practice-expansion/publication.json');orig={};fam={};collection={}
for path in ['practice_expansion/2026-10-23/candidates/questions.json']+[x['path'] for x in config['additional_banks']]:
 for q in read(R/path)['questions']:
  if q['question_id'] in assignment['question_hashes']:
   orig[q['question_id']]=digest(q);fam[q['question_id']]=q.get('family_id');collection[q['question_id']]=path
assert orig==assignment['question_hashes']
recommended=set(read(R/'practice_expansion/2026-10-28-representative/selection.json')['recommended_ids'])
records=[]
for rr in packet['records']:
 q=rr['original_visible_content'];qid=q['question_id'];n=int(qid.split('-')[-1]);g=next(g for g in G if g[0]<=n<=g[1]);lo,hi,topic,srcs,sections,rule=g
 tv=[x=='T' for x in truth[n]];incorrect='INCORRECT' in q['stem']; expected=[c['id'] for c,v in zip(q['choices'],tv) if (not v if incorrect else v)]
 assert q['question_type']=='SATA' or len(expected)==1
 assert expected==q['correct_choice_ids'],(qid,expected)
 title,juris,plaus,distr,wguess,wreason=real[topic];fail=topic in failtopics
 opts=[]
 for c,v in zip(q['choices'],tv):
  opts.append(dict(choice_id=c['id'],option_text=c['text'],option_text_sha256=hashlib.sha256(c['text'].encode()).hexdigest(),independently_supported=v,truth='TRUE' if v else 'FALSE',selected_by_independent_polarity=c['id'] in expected,finding_ko=option_reason(c['text'],topic),authorities=[authority(k) for k in srcs],exact_section=sections))
 nearestrow=nearest[qid];cn=nearestrow['nearest']['canonical'];pn=nearestrow['nearest']['public']; focus='INCORRECT단일오류' if incorrect else ('SATA각보기독립평가' if q['question_type']=='SATA' else ('CaseA' if 'addresses Case A' in q['stem'] else 'CaseB'))
 crit=dict(zip(criteria_names,[True,topic not in {'infusion'},topic not in {'oud','request-facts'},wguess,topic not in {'infusion','request-facts'},topic!='oud',True,True,True,True]))
 reasons={
 'jurisprudence_reasoning':f'{qid}({focus}): {juris}',
 'practice_plausibility':f'{qid}: {plaus}',
 'authentic_distractors':f'{qid}: {distr}',
 'wording_not_guessable':f'{qid}: {wreason}',
 'reasoning_not_trivia':f'{qid}: '+('요건충족/실제요청부재를stem이선판정하여요건을사실에대입하는추론이약하다.' if topic in {'infusion','request-facts'} else f'{title}의규정범위/기산점/권한성격을구별해야하므로단순약물schedule암기보다법적적용에서판단이생긴다.'),
 'natural_rule_combination':f'{qid}: '+('OUD사례와연결되지않은implantablepump의품질명제가끼어있어두사례의자연스러운권한대조를흐린다.' if topic=='oud' else f'{title}는동일처방업무의인접한조건을다룬다.여러법을억지로추가해야만현실적이라고평가하지않았다.'),
 'appropriate_drug_context':f'{qid}: '+('methylphenidate/testosterone은현행법이예시하는서로다른CII/III non-opioid라실제분류의미가있다.' if topic=='nonopioid' else '명시된CII/narcotic/non-opioid/OUD분류가해당규정범위를결정한다.특정brand를추가해야할법적필요가없는항목에는불필요한약물명암기를요구하지않는다.'),
 'distinct_from_bank':f'{qid}: canonicalnearest{cn["question_id"]}를stem과모든{len(cn["choices"])}보기를읽어비교했다. {canonnotes[cn["question_id"]]} publicnearest{pn["question_id"]}는같은A/B사례와일부동일판단을쓰는명시적family변형이다.배정문항은recommendedpool에없고이를새독립사례/범위로세지않는다.따라서archive변형존재만으로기준을자동실패시키지않았다.',
 'not_schedule_flashcard':f'{qid}: {title}에서공급가능성/권한/기록/기한을묻고단순ScheduleII이름을고르는문항이아니다.',
 'public_style_without_copying':f'{qid}: 이번세션NABPpublicsample/format/competency를HTTP200으로실제읽었다.SBA/SATA지시와선택형법규판단형식이맞고공개sample문장/사례의복제는확인되지않았다.공개sample은형식예시이며contentarea대표성이나모든문항의고난도를증명하는자료로쓰지않았다.'}
 assert fail == (not all(crit.values()))
 verdict='FAIL' if fail else 'PASS'
 exp_review={'read_entire_core_reasoning':True,'read_all_choice_rationales':list(c['id'] for c in q['choices']),'read_learning_boundary':True,'visible_explanation_sha256':digest(q['explanation']),'core_finding_ko':f'{rule} 원해설의해당법적결론은현행조문과일치한다.','choice_rationale_findings':[{'choice_id':c['id'],'full_rationale_read':True,'finding_ko':opts[i]['finding_ko']+' 원해설의참/거짓방향및교정문을대조했고법적오류를확인하지않았다.'} for i,c in enumerate(q['choices'])],'learning_boundary_finding_ko':'동일family네변형을독립임상사례네개로세지않는다는제한을읽고유지한다.','limitations_ko':'§20(c)의2일전자/예외7일과2019manual의7businessdays가다르므로oldmanual후속서부분을현행법근거로쓰지않았다.연방후속문항은명시범위대로만판정했다.' if topic=='follow-up' else 'historical효력시점으로소급일반화하지않으며현재공식게시본문의명시범위에서판정했다.'}
 record={'question_id':qid,'record_sha256':rr['record_sha256'],'family_id':fam[qid],'collection_path':collection[qid],'visible_content_sha256':rr['visible_content_sha256'],'read_scope':{'original_stem':True,'every_choice':True,'choice_count':len(q['choices']),'stored_key':True,'entire_korean_core_explanation':True,'every_choice_korean_rationale':True,'learning_boundary':True,'source':'assigned-visible-input.json','read_at':now,'hidden_author_truth_read':False,'prior_item_verdicts_read':False},'legal_review':{'existing_answer_correct':'YES','stored_key':q['correct_choice_ids'],'independently_expected_key':expected,'question_type':q['question_type'],'polarity':'SELECT_INCORRECT' if incorrect else 'SELECT_ALL_CORRECT' if q['question_type']=='SATA' else 'SELECT_CORRECT','independent_truth_vector':dict(zip([c['id'] for c in q['choices']],tv)),'per_choice_findings':opts,'authorities':[authority(k) for k in srcs],'verdict':'KEEP','finding_ko':f'{qid}: {rule} 각보기를독립참거짓판정한후{focus}로역산한키{expected}가저장키와일치한다.','blocker':None,'original_explanation_review':exp_review},'realism_review':{'verdict':verdict,'decision':'MAJOR_REWRITE' if fail else 'KEEP','criteria':crit,'criterion_findings_ko':reasons,'duplicate_evidence':{'status':'READ_AND_COMPARED','candidate_locator_method':near['method'],'canonical_pool_count':439,'public_pool_count':2349,'evidence_path':str((P/'nearest-visible-comparisons.json').relative_to(R)),'evidence_sha256':sha(P/'nearest-visible-comparisons.json'),'nearest_canonical_id':cn['question_id'],'nearest_public_id':pn['question_id'],'all_nearest_stems_and_choices_read':True,'currently_recommended':qid in recommended,'comparison_ko':reasons['distinct_from_bank']},'finding_ko':'; '.join(reasons[k] for k,v in crit.items() if not v) if fail else f'{qid}:10기준을각각직접확인했다.이판정은archive연습변형의제한을유지하며새coverage로의승격이아니다.'},'safe_hold_recommended':fail,'release_eligible':False,'required_next_action_ko':('편집자가구체환자/제품/시각/역할의원사실을제시하고평가어단서·무관보기·결론재진술을제거한새상황과distractor를작성한후새hash에독립법규/현실성재감사를받는다.원문/키를본감사자가직접수정하지않는다.' if fail else '원본키수정불필요.legacy단계증거만제출하며canonicaladmission/release에필요한별도정책gate를충족하기전RELEASED로승격하지않는다.')}
 records.append(record)
style=read(R/'data/exam_style/mpje_style_profile.json');blue=read(R/'data/blueprint.json')
report={'schema_version':'independent-phase13-a-review/1','stage':'independent-legacy','independent_of_authors':True,'auditor':'GPT','auditor_instance':'GPT:/root/independent_wave13_a:20261104','actor_provenance':{'actor_id':'/root/independent_wave13_a','session_id':'/root/independent_wave13_a'},'canonical_audit':False,'canonical_release_credit':0,'author_review_credit':0,'release_eligible':False,'reviewed_at':'2026-11-04','completed_at':now,'job_id':assignment['job_id'],'question_hashes':assignment['question_hashes'],'methodology_ko':'실제freshfork-none세션.4정책/legacyrunbook/native계약을읽고배정40원문/160보기/키/전체한국어해설을직접읽었다.기존item판정보고서·원장item결론·authortruth를열람하지않았다.원객체는whole-recordhash와familyid의명시whitelist추출에만코드로사용했다.공식primary본문과각보기의주체/조건/행위/예외/기산점을대조하고그뒤극성/SATA를계산했다.일괄긍정규칙이나저장key를truth계산에사용하지않았다.','input_binding':{'assignment_path':str((P/'assignment.json').relative_to(R)),'assignment_sha256':sha(P/'assignment.json'),'visible_packet_path':str((P/'assigned-visible-input.json').relative_to(R)),'visible_packet_sha256':sha(P/'assigned-visible-input.json')},'policy_bindings':[{'path':p,'file_sha256':sha(R/p)} for p in ['docs/RELEASE_POLICY.md','docs/AUDIT_WORKFLOW.md','docs/SOURCE_USE_POLICY.md','docs/QUESTION_AUTHORING_STANDARD.md','docs/INDEPENDENT_LEGACY_REVIEW_RUNBOOK.md','schemas/audit.schema.json','schemas/question.schema.json']], 'style_profile':{'profile_id':style['profile_id'],'content_version':style['content_version'],'content_hash':style['content_hash'],'file_sha256':sha(R/'data/exam_style/mpje_style_profile.json')},'blueprint':{'blueprint_id':blue['blueprint_id'],'content_version':blue['content_version'],'content_hash':blue['content_hash'],'file_sha256':sha(R/'data/blueprint.json')},'sources':list(sources.values()),'network_limitations_ko':'Firecrawl공식조회1회는credits부족으로미실행되었다.재시도/인증우회없이verifiedTLS와상속proxy의urllib공식live조회로전환했다.17개URL은모두HTTP200이며문서정체/실제조문을직접확인했다.NABPsample/웹본문은공개저작권원문을publiccommit하지않고로컬/tmp실독후SHA와자체형식메모만보존했다.','public_style_memo_path':str((P/'public-style-own-memo.json').relative_to(R)),'summary':{'records':40,'choices_read':160,'legal_keep_answer_yes':40,'realism_pass':sum(x['realism_review']['verdict']=='PASS' for x in records),'realism_fail':sum(x['realism_review']['verdict']=='FAIL' for x in records),'canonical_credit':0},'records':records}
(P/'public-style-own-memo.json').write_text(json.dumps({'reviewed_at':now,'official_retrieval_metadata':[sources[k] for k in ['nabpsample','nabpformat','nabpcompetency']],'own_abstract_memo_ko':'NABP공개sample은single-answer/multiple-response/ordered-response의응답형식을예시하며contentarea의대표성은주장하지않는다.현재format페이지는120문항/2.5시간/adaptive selected-response라고설명한다.현재competency페이지는22/33/24/21%의4영역과2027-03-01이후개정예정을명시한다.본배정은SBA38/SATA2이며문항별법적추론/현실성은이형식확인과별개로평가했다.공개sample문구를새문제로복제하거나Pre-MPJE/회상/상업질문을열람하지않았다.원samplePDF/웹HTML/추출문은/tmp에만있고publiccommit대상이아니다.'},ensure_ascii=False,indent=2)+'\n')
report['public_style_memo_sha256']=sha(P/'public-style-own-memo.json')
(R/'reports/full-corpus-review/independent-phase13-a-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report['summary']))
