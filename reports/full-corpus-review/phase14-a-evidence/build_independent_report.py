"""Serialize this session's independently authored findings; never read prior audits/truth."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, re, sys
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
PREFIX=str(OUT.relative_to(ROOT));DATE='2026-11-04'
def sha(b):return hashlib.sha256(b).hexdigest()
def digest(v):return sha(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def load(p):return json.loads(Path(p).read_bytes())
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def auth(source,section):
 m=load(OUT/'sources'/f'{source}.meta.json');assert m['status']==200
 result={k:m[k] for k in ['source_id','official_url','law_checked_date','retrieved_at','retrieval_method','raw_path','raw_sha256','evidence_path','evidence_sha256','text_sha256','public_raw_redistribution']}
 result['authority']=section;result['exact_section']=section;result['source_type']='PUBLIC_OFFICIAL'
 meta=OUT/'sources'/f'{source}.meta.json'
 result['metadata_path']=str(meta.relative_to(ROOT));result['metadata_sha256']=sha(meta.read_bytes())
 text=(ROOT/m['evidence_path']).read_text()
 if source.startswith('cfr'):
  currency=re.search(r'Displaying title .*?up to date as of [^\n]+',text)
  result['version']=currency.group(0) if currency else 'eCFR current view retrieved on review date'
  result['effective_date']=None;result['effective_date_limitation_ko']='현행 eCFR 표시본과 조문 연혁을 확인했다. 조문별 모든 개정의 최초 효력일을 별도 Federal Register 문서로 추적하지 않았으며, 조회일과 eCFR currency를 효력일로 바꾸지 않는다.'
 elif source=='ma-policy2026-01':
  result['version']='Policy 2026-01; adopted 2026-03-26; supersedes 2022-01';result['effective_date']='2026-03-26';result['effective_date_limitation_ko']='문서 명시 adoption date이며 별도 commencement 조항은 없다.'
 elif source=='ma-247-9-current':
  result['version']='Mass. Register #1536, 2024-12-06';result['effective_date']='2024-12-06';result['effective_date_limitation_ko']='공식 게시 PDF의 Register/date를 사용한다. 이후 unpublished 개정이나 개별 waiver를 추정하지 않았다.'
 elif source=='ma-105-700':
  result['version']='Mass. Register #1514, 2024-02-02 official posted compilation';result['effective_date']=None;result['effective_date_limitation_ko']='공식 게시본의 compilation 날짜를 확인했지만 700.008의 최초 commencement를 별도 추적하지 않았다.'
 else:
  result['version']='Massachusetts Legislature current General Laws HTML retrieved 2026-11-04';result['effective_date']=None;result['effective_date_limitation_ko']='공식 현행 법문을 확인했다. 페이지에 절별 최신 효력일이 표시되지 않아 특정 commencement 날짜는 미확정이다.'
 return result

# Each independent proposition was compared with the controlling primary text.
# Each entry: phrase fragments identifying one legal proposition, exact authority, Korean application.
CLAIMS={
 797:[
  (['telemedicine','VCPR formation'],[('cfr21-530','21 CFR 530.3(i)(1)-(3), 530.10')],'연방 extralabel VCPR는 수의사의 책임·동물에 대한 충분한 지식·follow-up와 최근 examination 또는 적절한 현장 방문을 요구한다. 최초 원격 접촉 하나가 전부를 충족한다는 보장은 없다.'),
  (["owner","Veterinary scope"],[('ma112-58','M.G.L. c.112 §58'),('ma94c-19','M.G.L. c.94C §19(a)'),('ma-247-9-current','247 CMR 9.15(2)')],'수의 진료의 치료 대상은 동물이다. 수의 면허만으로 사람 소유자의 질환에 대한 전문직 처방 권한이 생기지 않으며 약사는 usual professional practice를 확인해야 한다.'),
  (['dose','species-related'],[('cfr21-530','21 CFR 530.10(a), 530.12(c)'),('ma-247-9-current','247 CMR 9.01(4), 9.17(1)(f),(i)')],'동물의 종·용량·투여 방향은 수의사가 정한 extralabel 지시의 일부이다. 불명확한 방향을 인간용 라벨에서 임의로 만들어 처방을 대체하는 권한은 없다.'),
  (['human drug','human-labeled'],[('cfr21-530','21 CFR 530.1, 530.10, 530.20, 530.30')],'승인 인간용 의약품의 동물 사용 자체는 금지가 아니다. 적법한 수의사 지시·유효 VCPR·해당 동물/식용 여부 등 Part 530 조건을 만족하는 경로가 존재한다.')],
 801:[
  (['withdrawal','food-residue','Food-residue'],[('cfr21-530','21 CFR 530.12(e), 530.20(a)(2)(ii)-(iv)')],'식용 동물의 extralabel 사용은 withdrawal/withholding 표시와 잔류 방지 조치를 유지한다. 동물용이라는 이유로 사람의 식품 안전 의무가 사라지지 않는다.'),
  (['VFD','medicated-feed'],[('cfr21-558-6','21 CFR 558.6(a)(1)-(3), (b)(3)(xii)-(xiii)'),('cfr21-530','21 CFR 530.11(b)')],'VFD는 적법한 수의사 feed 지시이며 extralabel feed 사용은 금지된다. 재주문은 승인/표시가 허용할 때에만 가능하므로 일반 인간 Schedule VI의 자유 refill로 바꿀 수 없다.'),
  (['animal identification','extralabel label'],[('cfr21-530','21 CFR 530.12(c)-(e)')],'표시는 동물 또는 군/종의 식별, 용량·빈도·경로·기간과 주의사항을 포함한다. 인간 환자명 예외를 모든 동물 식별·지시의 생략으로 확대할 수 없다.'),
  (['bulk','AMDUCA'],[('cfr21-530','21 CFR 530.13(a)-(b)')],'Part 530은 승인 인간/동물약으로부터의 조제를 규율하고 bulk drug 조제를 허용하는 것으로 해석하지 말라고 명시한다. AMDUCA가 모든 bulk 성분 조제를 자동 승인한다는 주장은 틀리다.')],
 805:[
  (['samples','resale','retail inventory'],[('ma-247-9-current','247 CMR 9.01(6)')],'약국은 not-for-resale sample을 조제·재포장·재판매 목적으로 수령 또는 매입할 수 없다. 정상 유상 재고에 편입하는 사례는 이 금지에 해당한다.'),
  (['diagnos','prescrib','test result'],[('ma-247-9-current','247 CMR 9.01(4)'),('cfr42-493','42 CFR 493.1, 493.15(e)')],'CLIA는 검사실/검사 체계의 규율이다. 결과 취득만으로 개인 약사의 인정된 practice scope를 무제한 진단·처방으로 늘리지 않는다.'),
  (['certificate','word waived'],[('cfr42-493','42 CFR 493.15(e), 493.35(a), 493.37(a)-(b),(g)')],'waived-only 검사실도 certificate 신청과 제조사 지침 준수 조건이 있다. waived라는 단어가 장소 인증·절차 의무 면제를 뜻하지 않는다.'),
  (['instructions','Changing test'],[('cfr42-493','42 CFR 493.15(e)(1)-(2), 493.17(c)(4), 493.37(g)')],'검체·시간 등 제조사 절차를 바꾼 검사에는 원래 waived 지위를 그대로 전제할 수 없다. 적정 복잡도와 그 검사를 허용하는 certificate를 다시 검토해야 한다.')],
 809:[
  (['single-sheet','triplicate'],[('cfr21-1305','21 CFR 1305.11(a), 1305.12(c)')],'현행 Form 222는 single-sheet이고 한 form에는 한 공급자만 기재한다. 두 공급자의 주문과 과거 triplicate 절차를 결합한 사례는 현행 방식에 맞지 않는다.'),
  (['60-day','completion clock'],[('cfr21-1305','21 CFR 1305.13(b), 1305.22(e)')],'통상 잔량 공급과 form 유효성 60일은 Form 222/order의 실행 날짜에서 센다. 최초 shipment가 새 60일 시계를 열지 않는다. 군 조달 등 명시 예외를 이 일반 약국 사례에 추가하지 않았다.'),
  (['received','receipt','executed copy'],[('cfr21-1305','21 CFR 1305.13(a),(e), 1305.17')],'구매자는 실행 사본을 보관하고 실제 받은 container 수와 수령일을 적는다. 주문 실행은 같은 날 전량 물리적 수령을 입증하는 기록이 아니다.'),
  (['expired','blank forms','unused forms'],[('cfr21-1305','21 CFR 1305.04(a)-(b)')],'해당 약물 registration이 유효한 등록자 명의로만 주문을 실행한다. 미사용 form을 갖고 있다는 사실은 expired registration을 연장하지 않는다.')],
 813:[
  (['MOR','title'],[('cfr21-1305','21 CFR 1305.05(a),(d), 1305.12(d)')],'Form 222 서명자는 등록자 개인/파트너/임원 또는 해당 등록자가 적법하게 POA를 부여한 사람이어야 한다. MOR라는 MA 직책만으로 이 연방 권한이 자동 발생하지 않는다.'),
  (['credentials','Sharing','sharing'],[('cfr21-1311','21 CFR 1311.30(a),(c)')],'CSOS digital certificate/private key는 certificate holder만 접근·사용한다. 동료에게 credential을 나누는 행위는 동료의 적법한 별도 서명 권한을 대신할 수 없다.'),
  (['witness','POA execution','verbal'],[('cfr21-1305','21 CFR 1305.05(c)-(f)')],'적법한 POA의 실행에는 규정상 grantor·grantee·두 witness가 필요하고 전자서명도 가능하다. 구두 지시만으로 대신하지 못한다. 다만 사례에는 POA가 없으므로 “described POA execution”을 이미 완료된 사실로 읽으면 근거 없는 서술이다.'),
  (['CSOS certificate','CSOS stock ordering'],[('cfr21-1305','21 CFR 1305.01, 1305.21(a)'),('cfr21-1311','21 CFR 1311.01, 1311.10, 1311.100')],'CSOS certificate는 등록자 stock order의 전자서명 체계이다. 환자별 EPCS와 별도이고 certificate 자체가 환자 처방의 전문직 권한을 부여하지 않는다.')],
 817:[
  (['first stated ratio'],[('cfr21-1307-11','21 CFR 1307.11(a)(1)(iv)')],'포함 분배량 10,000과 조제량 190,000의 합이 분모 200,000이다. 10,000/200,000=5%이며 조제량만의 190,000을 분모로 삼지 않는다.'),
  (['proposed totals'],[('cfr21-1307-11','21 CFR 1307.11(a)(1)(iv), (b)')],'추가 분배 1,000은 분자와 분모에 모두 더한다. 11,000/201,000=약 5.4726%로 5%를 초과한다. 기존 계산값이 다음 거래에 고정되는 것은 아니다.'),
  (['expected excess','Reasonable expectation'],[('cfr21-1307-11','21 CFR 1307.11(b)')],'연간 초과를 예상할 이유가 있으면 distribute registration을 받아야 한다. 연말 정산까지 무조건 기다리는 경로는 이 사전 예상 조건을 무시한다.'),
  (['Massachusetts','federal exception'],[('cfr21-1307-11','21 CFR 1307.11(a)(1)(i)-(iv), (b)'),('ma94c-1','M.G.L. c.94C §1 (registration/practitioner definitions)')],'5% 예외는 특정 연방 distributor registration 예외이다. 수령자의 등록·거래기록·Schedule I/II order 요건도 남으므로 모든 주법/공급망 의무 면제로 읽을 수 없다.')],
 821:[
  (['Form 106','Form 222 or CSOS'],[('cfr21-1305','21 CFR 1305.03, 1305.21'),('cfr21-1301-76','21 CFR 1301.76(b)')],'Form 222 또는 적법 전자 order는 Schedule II stock 분배의 주문 경로이고 Form 106은 theft/significant loss 보고이다. 두 문서의 목적을 대체할 수 없다.'),
  (['stock return','supplier'],[('cfr21-1317','21 CFR 1317.10(a)-(b)'),('cfr21-1305','21 CFR 1305.03')],'등록자 stock return/recall도 기록을 유지하고 Schedule I/II는 Part 1305 order를 사용한다. 적격 공급자에게 반환한다는 사실이 문서 전체를 면제하지 않는다.'),
  (['patient return','patient return'.title()], [('cfr21-1317','21 CFR 1317.30(a)-(b), 1317.40, 1317.85'),('ma-247-9-current','247 CMR 9.01(5),(7)')],'환자에게 이미 교부한 물건은 registrant의 미교부 stock과 다른 ultimate-user/수거 경로에 있다. 모든 patient return을 stock purchase reversal로 처리할 수 없다.'),
  (['Expiration','Expired stock'],[('ma-247-9-current','247 CMR 9.21(9)-(10)'),('cfr21-1304','21 CFR 1304.11(e)(1)(iv), 1304.21(a)')],'만료/격리/역유통 대기 stock도 보안과 accountability를 유지한다. 유효기간이 지났다는 사실만으로 통제 대상·재고 의무가 즉시 사라지지 않는다.')],
 825:[
  (['initial notice','initial written'],[('cfr21-1301-76','21 CFR 1301.76(b)')],'관할 DEA Field Division에 discovery 후 1 business day 이내 서면 notice를 한다. 조사 완료나 후속 Form 106의 나중 기한으로 초기 통지를 미룰 수 없다.'),
  (['Form 106 clock','states 45'],[('cfr21-1301-76','21 CFR 1301.76(b)')],'실제 이번 현행 본문도 complete and accurate electronic Form 106을 discovery 후 45일 이내 제출하도록 한다. 조사 완료에서 새 45일이 시작되는 것이 아니다.'),
  (['Significance','dollar threshold'],[('cfr21-1301-76','21 CFR 1301.76(b)(1)-(6)')],'significant loss는 업종 대비 수량, 약물, 접근, 반복 pattern, diversion 가능성 등 요소로 평가한다. 보편적인 고정 달러선 하나가 전부를 결정하지 않는다.'),
  (['theft','known theft'],[('cfr21-1301-76','21 CFR 1301.76(b)')],'조문은 theft와 significant loss를 나란히 규정한다. 확인된 theft를 수량이 적다는 이유만으로 보고에서 제외하지 않는다.')],
 829:[
  (['Board','Submitting to DEA'],[('ma-policy2026-01','Board Policy 2026-01 §§I-II')],'resident Board pharmacy/wholesaler는 해당 confirmed loss/theft에 Board RLCS와 applicable Form 106을 7 calendar day 경로로 별도 제출한다. DEA 전송이 자동으로 Board 제출을 대신하지 않는다.'),
  (['DCP','tampering'],[('ma-105-700','105 CMR 700.008')],'DCP registrant는 theft, loss 또는 suspected tampering의 discovery로부터 24시간 이내 지정/승인 form으로 DCP에 보고한다. confirmed theft가 되어야 tampering trigger를 검토하는 것은 아니다.'),
  (['facility','registrations'],[('ma-policy2026-01','Board Policy 2026-01 §I'),('ma-105-700','105 CMR 700.001, 700.004, 700.008'),('cfr21-1301-76','21 CFR 1301.76(b)')],'Board resident pharmacy/wholesaler, DCP registrant, DEA practitioner의 수범자 범위가 다르다. 모든 시설이 동일 등록과 의무를 가진다는 일반화는 할 수 없다.'),
  (['event outside','Not being'],[('ma-policy2026-01','Board Policy 2026-01 §III'),('ma-247-9-current','247 CMR 9.21(8)(c)')],'한 손실보고 범주에서 제외되어도 onsite investigation/insignificant loss log·trend 또는 dispensing error의 CQI 같은 별도 의무가 남을 수 있다. Form 106 비대상이라는 사실만으로 아무 기록도 필요 없다고 단정하지 않는다.')],
 833:[
  (['Deleting','Electronic deletion'],[('cfr21-1317','21 CFR 1317.90(a)-(c)')],'controlled substance 자체를 non-retrievable로 만들어야 한다. 컴퓨터 entry나 라벨 삭제는 물리적 약물을 제거·파괴하지 않으므로 destruction이 아니다.'),
  (['30 days','clock starts'],[('cfr21-1317','21 CFR 1317.15(d)')],'reverse distributor가 destruction 목적으로 수령한 controlled substance의 destruction은 수령 후 30 calendar days 이내이다. 모든 약국 상품의 expiry date 후 30일이라는 일반규칙으로 바꿀 수 없다.'),
  (['witness','two pharmacists'],[('cfr21-1317','21 CFR 1317.95(a)-(d)'),('cfr21-1304','21 CFR 1304.21(e)')],'해당 연방 절차는 운송·loading·직접 destruction 단계에 두 employees와 witness를 정한다. 이를 모든 장소·모든 destruction에 두 pharmacists가 필요하다는 문장으로 바꿀 수 없다.'),
  (['residue','partly used'],[('cfr21-1304','21 CFR 1304.21(e)')],'Form 41 예외는 등록 장소에서 immediate administration 후 더 사용할 수 없는 잔량과 그 적법 기록이다. 일부 사용한 일반 stock bottle 전부가 해당하지 않는다.')],
 837:[
  (['zero-stock','Zero controlled'],[('cfr21-1304','21 CFR 1304.11(b)')],'처음 등록 활동을 시작할 때 controlled stock이 0이어도 그 사실을 initial inventory로 기록한다. 첫 유입/정기 inventory까지 의무가 없어지는 것은 아니다.'),
  (['newly scheduled','next biennial'],[('cfr21-1304','21 CFR 1304.11(d)')],'기존 unscheduled 물질을 새로 schedule하는 rule의 효력일에 보유 registrant가 그 stock을 inventory한다. 다음 정기 biennial count가 효력일 의무를 자동 충족하지 않는다.'),
  (['biennial interval','biennial year-end'],[('cfr21-1304','21 CFR 1304.11(c)')],'새 inventory는 적어도 2년마다 해야 하며 날짜 명칭이 간격을 늘리는 허가는 아니다. 실제 이전 inventory로부터의 기간을 확인한다.'),
  (['head office','Separate registered'],[('cfr21-1304','21 CFR 1304.11(a), 1304.21(b)-(c)')],'원칙적으로 등록 장소와 독립 등록 활동별 inventory/기록이 필요하다. 본사의 합계 추정치가 모든 장소를 항상 대체하지 않으며 조문상 제한된 예외만 따로 적용한다.')],
 841:[
  (['over-1000'],[('cfr21-1304','21 CFR 1304.11(e)(6)(ii)')],'열린 Schedule III-V container의 exact-count 예외는 more than 1,000 tablets/capsules이다. 1,000과 1,001은 경계의 서로 다른 쪽이며 at least 1,000로 바꾸지 않는다.'),
  (['Schedule II'],[('cfr21-1304','21 CFR 1304.11(e)(6)(i)-(ii)')],'Schedule II 열린 container는 1,000 경계와 관계없이 exact count/measure한다. III-V 추정 허용 예외를 II에 옮길 수 없다.'),
  (['strengths','Different strengths'],[('cfr21-1304','21 CFR 1304.11(e)(1)(iii), (e)(6)')],'inventory는 각 finished form·strength·container 또는 quantity 정보를 식별한다. 동일 ingredient의 모든 함량·제형을 의미 없는 한 총량으로 합치는 것으로 충분하지 않다.'),
  (['opening','date alone'],[('cfr21-1304','21 CFR 1304.11(a)')],'날짜와 함께 opening 또는 closing of business 중 어느 시점인지 inventory에 표시한다. 날짜만 있다는 사실이 당일 거래 전후 기준을 대신하지 않는다.')],
 845:[
  (['Daily entries'],[('ma-247-9-current','247 CMR 9.21(8)(a)-(c)')],'daily perpetual entries와 최소 10일마다의 물리 count/record comparison은 함께 요구된다. 3주 동안 대조하지 않은 Case A는 daily entry만으로 충족되지 않는다.'),
  (['expected balance'],[('ma-247-9-current','247 CMR 9.21(8)(b)-(c)')],'100+50−40=110이다. 실제 109라면 1단위 차이이며 MOR 조사 대상이다. 이것이 자동 significant loss라는 뜻은 아니다.'),
  (['employee','adjustment'],[('ma-247-9-current','247 CMR 9.21(8)(c)-(f)')],'차이 조정은 MOR 또는 부재 시 pharmacist designee의 적법 절차로 한다. 직원 누구나 설명 없이 0 처리하는 것은 조사·권한·기록을 충족하지 않는다.'),
  (['one-unit','small discrepancy'],[('ma-247-9-current','247 CMR 9.21(8)(c)'),('ma-policy2026-01','Board Policy 2026-01 §§II-III')],'작은 차이는 조사 없이 제외하지 않으며 theft/유의성/오류를 구분한다. 작은 숫자만으로 significant loss도 아니고 모든 조사·보고 검토에서 면제되는 것도 아니다.')]
}

# Independent literal truth evaluation in A/B/C/D order, not copied from stored keys.
TRUTHS={797:'FTFF',798:'FFTF',799:'TTTT',800:'TTTF',801:'TFFF',802:'FTFF',804:'TTFT',805:'FFFT',806:'TFFF',808:'TFTT',809:'FFTF',810:'FFFT',812:'FTTT',813:'FTFF',814:'FFTF',815:'UTTT',816:'TTUF',817:'TFFF',818:'FTFF',820:'TTFT',821:'FFFT',822:'TFFF',824:'TFTT',825:'FFTF',826:'FFFT',828:'FTTT',829:'FTFF',830:'FFTF',831:'TTTT',832:'TTTF',833:'TFFF',834:'FTFF',836:'TTFT',837:'FFFT',838:'TFFF',840:'TFTT',841:'FFTF',842:'FFFT',844:'FTTT',845:'FTFF'}
GROUPS=[797,801,805,809,813,817,821,825,829,833,837,841,845]
FOCUS={797:'인간용 승인약의 동물 extralabel 경로',798:'수의 면허와 사람 환자 진료의 경계',799:'VCPR·scope·용량확인·extralabel의 복수 법적 조건',800:'초기 원격 VCPR를 모든 조건 충족으로 보는 오류',801:'식용 동물 withdrawal/withholding',802:'VFD와 인간 처방/refill의 구별',804:'AMDUCA를 모든 bulk 조제 승인으로 확대하는 오류',805:'제조사 검사 지침 변경과 waived 지위',806:'not-for-resale sample의 일반 재고 편입',808:'waived라는 이유로 certificate/절차를 면제하는 오류',809:'single-sheet Form 222와 공급자 수',810:'부분 shipment 60일의 기산점',812:'blank form 보유와 유효 registration 구별',813:'MOR 직책과 registrant POA',814:'CSOS credential의 개인적 통제',815:'관련 POA 요건과 사례에 없는 실행의 모호한 지시어',816:'CSOS 처방권한 오해와 POA 실행 지시어',817:'5% 계산에서 분배+조제 분모',818:'추가 분배 후 11,000/201,000 계산',820:'연방 예외를 모든 주법 면제로 보는 오류',821:'Form 222/CSOS와 Form 106의 문서 기능',822:'등록자 stock return의 주문·기록',824:'만료 stock의 accountability',825:'DEA 초기 notice와 조사 완료의 분리',826:'45일 completed Form 106의 discovery trigger',828:'작은 theft와 significant loss의 구별',829:'Board RLCS 별도 제출과 calendar-day 경로',830:'DCP suspected tampering의 24시간 trigger',831:'Board·DCP·연방 및 CQI 병행 의무',832:'Form 106 비대상을 모든 기록 면제로 확대하는 오류',833:'전산 삭제와 non-retrievable destruction 구별',834:'reverse distributor의 receipt 후 30일',836:'immediate-administration residue 예외의 한계',837:'zero-stock initial inventory',838:'newly scheduled 물질의 효력일 inventory',840:'장소별 inventory와 본사 합계의 구별',841:'열린 III container의 1,000/1,001 경계',842:'열린 II container의 무조건 exact count',844:'opening/closing 기준 기록의 생략 오류',845:'10일 physical reconciliation과 daily entries 구별'}

# Deliberate individual realism findings. Pass requires all ten criteria true.
PASS={809,810,812,813,814,817,818,820,825,831,841,842,844}
FAIL_REASON={
 797:'정답은 “not automatically unlawful ... conditions”로 유보하지만 다른 보기는 “alone necessarily”, “freely invent”, 사람 소유자 치료 권한이라는 과장이라 법 적용 없이도 골라낼 단서가 크다.',
 798:'정답 scope 문장은 제한을 설명하지만 다른 보기는 “never”, “alone necessarily”, “freely invent”로 극단화된다. 실제 가능한 동물용 order 결함들 사이의 선택이 아니다.',
 799:'전체 참 SATA 자체는 허용되지만 용량 불명확·최초 원격 접촉은 사례에 실제 제시되지 않고 넓은 관련요건 목록을 고르게 한다. 두 사례에서 필요한 구체적 행동 판단보다 병렬 문장 승인에 가깝다.',
 800:'오류 보기 D만 “initial ... alone necessarily ... every”를 누적하고 나머지는 조건부 주의사항이다. 오류의 범위가 실제 VCPR 예외보다 표현의 과장으로 드러난다.',
 801:'오답이 각각 모든 bulk 자동 승인·모든 식별/지시 생략·무제한 feed 사용으로 과장된다. withdrawal omission에 대한 가까운 오해를 경쟁시키지 않아 표현상 단서가 크다.',
 802:'A의 “eliminates all”, C의 “automatically ... every”, D의 “omitting all”이 유일한 제한적 B와 뚜렷이 대비되어 답을 추측할 수 있다.',
 804:'오류 C의 “automatically ... every ... any bulk”는 다른 세 조건부 법문보다 과도하게 포괄적이다. 특정 bulk 경로/승인 조건과 혼동하는 근접 보기가 필요하다.',
 805:'rapid-test 절차 변경과 sample 재판매는 이 사례에서 법적·인과적으로 연결되지 않는다. 다른 사건을 한 stem에 붙여 놓아 자연스러운 다중규칙 적용이 아니다.',
 806:'Case B sample 유통 판단에 Case A의 specimen/timing 사실이 아무 역할을 하지 않는다. 두 규칙의 연계가 약하고 오답의 “regardless/unrestricted/eliminates any”도 단서가 된다.',
 808:'검사 waived/certificate와 약품 sample 유통은 독립된 사건인데 오류선택에 함께 나열된다. B의 “eliminates any”도 다른 제한적 보기와 대비된다.',
 815:'실제 stem은 POA 없이 서명했다고 하는데 A는 “described POA execution includes ... signatures”라고 완료된 실행을 가리키듯 쓴다. 규범 요건을 묻는 것인지 부존재한 사례 사실을 묻는지 명료하지 않다.',
 816:'C가 stem에 없는 실행을 “described POA execution”으로 지칭한다. 오류선택에서 D 외에 C도 사실관계상 틀리게 읽힐 수 있어 명료한 선택 구조를 해친다.',
 821:'오답이 모두 반환이면 모든 기록 면제·expiry 즉시 모든 책임 소멸·어떤 환자 반환도 stock reversal이라는 과장이다. D만 조건을 보존해 표현으로 정답을 예측하기 쉽다.',
 822:'정답만 “applicable ... requirements”를 보존하고 B/C/D는 즉시 모든 책임 소멸·Form 106 주문·모든 환자 반환 동일처리다. 실제 반환 주문의 주체나 문서 방향을 경쟁시키지 않는다.',
 824:'오류 B만 expiry가 “all ... immediately”를 없앤다고 단정한다. 다른 세 문장은 적절한 구별을 넓게 진술하여 법적 판단보다 전면 면제 표현을 거르는 문제가 된다.',
 826:'정답이 실무 조치 대신 “The retrieved current ... states”라는 저자의 조회 작업을 묘사한다. 실제 사건의 날짜/제출 기한 판단을 보여 주지 않고 조회본 문구 확인을 묻는다.',
 828:'D는 실무 법규 대신 “retrieved current”라는 출처조회 표현이고 A는 작은 theft를 전면 면제한다. 원칙을 실제 날짜·사건에 적용하는 판단으로 다듬어야 한다.',
 829:'오답의 “no ... anywhere”, “Every facility ... exactly the same”, confirmed theft 전제는 지나치게 넓다. 등록자와 수신처의 가까운 선택지보다 전면 면제/동일화 표현이 답을 드러낸다.',
 830:'오답 A/B/D가 각각 아무 기록도 없음·DEA가 모든 Board 제출 대체·모든 시설 동일이라는 전면 일반화이다. C만 제한된 대상/trigger를 유지해 언어적 단서가 크다.',
 832:'오류 D의 “no record or report ... anywhere”가 다른 세 조건부 설명과 극명히 대비된다. RLCS와 DCP의 기한·trigger를 실제 사건별로 혼동하는 근접 오답이 없다.',
 833:'전산 entry 삭제가 약물을 물리 파괴하지 않는 것은 상식으로도 쉽게 보이고 다른 보기 모두 “Every”로 예외를 과도하게 넓힌다. 파괴 방법/증인의 구체적 선택을 비교해야 한다.',
 834:'정답만 reverse distributor receipt trigger를 제한하고 다른 보기는 Every witness, electronic deletion alone, Every partly used bottle로 극단화된다. 답의 유보 정도로 추측할 단서가 있다.',
 836:'오류 C의 “Every partly used inventory bottle”은 다른 보기가 보존하는 “applicable/described” 범위와 대비된다. 투여 후 잔량과 stock의 구체적 사실을 대조하는 보기가 필요하다.',
 837:'“head office ... always”와 “Calling a count ... permits ... longer”는 현실적인 합법 경로와 멀다. zero inventory의 시작 시점과 문서 대체 여부를 가까운 오답으로 만들 필요가 있다.',
 838:'본사 추정이 항상 대체한다거나 count의 이름으로 2년을 넘긴다는 보기는 실무상 법규 혼동보다 비현실적인 포괄 명제이다. 정답만 제한된 시점을 유지한다.',
 840:'오류 B만 “head office ... always replaces”라고 모든 장소를 합계로 대체한다. 다른 세 보기에는 의무와 제한이 그대로 있어 절대적 표현을 찾는 단서가 된다.',
 845:'차이를 누구나 zero-out해도 된다거나 한 단위는 categorically 검토 밖이라는 오답은 지나치게 과장된다. 기록·실사·오차 조사 사이의 실제 업무 선택을 경쟁시키는 근접 오답이 필요하다.'}

def family(n):return max(g for g in GROUPS if g<=n)
def claim_for(g,text):
 candidates=CLAIMS[g]
 if g==805 and ('Changing test' in text or 'A rapid test' in text):candidates=[CLAIMS[g][3]]
 if g==821 and 'patient return' in text.lower():candidates=[CLAIMS[g][2]]
 if g==829 and ('Every facility' in text or 'Different facility' in text):candidates=[CLAIMS[g][2]]
 for terms,refs,note in candidates:
  if any(t.lower() in text.lower() for t in terms):return refs,note
 raise ValueError((g,text))

def main():
 assignment=load(OUT/'assignment.json');packet=load(OUT/'assigned-visible-input.json');nearest=load(OUT/'nearest-candidates.json');near={x['question_id']:x for x in nearest['results']}
 config=load(ROOT/'site/practice-expansion/publication.json');paths=['practice_expansion/2026-10-23/candidates/questions.json']+[x['path'] for x in config['additional_banks']]
 original={q['question_id']:q for p in paths for q in load(ROOT/p)['questions']}
 recommended=set(load(ROOT/'practice_expansion/2026-10-28-representative/selection.json')['recommended_ids'])
 retained_sources={};records=[]
 for row in packet['records']:
  q=row['original_visible_content'];qid=q['question_id'];n=int(qid[-4:]);g=family(n);truth=TRUTHS[n];assert digest(original[qid])==assignment['question_hashes'][qid]
  findings=[];authorities={}
  for i,c in enumerate(q['choices']):
   refs,note=claim_for(g,c['text']);aa=[auth(s,sec) for s,sec in refs]
   for a in aa:authorities[(a['source_id'],a['exact_section'])]=a;retained_sources[a['source_id']]=auth(a['source_id'],'Primary text; see per-choice exact sections')
   supported={'T':True,'F':False,'U':None}[truth[i]]
   findings.append({'choice_id':c['id'],'option_text':c['text'],'option_sha256':sha(c['text'].encode()),'statement_supported':supported,'independent_truth':'TRUE' if supported is True else 'FALSE' if supported is False else 'AMBIGUOUS_REFERENT','finding_ko':('옳은 명제. ' if supported is True else '틀린 명제. ' if supported is False else '해석이 갈리는 명제. ')+note,'authorities':aa})
  polarity='INCORRECT' if 'INCORRECT?' in q['stem'] else 'CORRECT'
  expected=[c['id'] for i,c in enumerate(q['choices']) if truth[i]==('F' if polarity=='INCORRECT' else 'T')]
  ambiguous='U' in truth
  if not ambiguous:
   assert expected==q['correct_choice_ids'],(qid,expected,q['correct_choice_ids'])
   if q['question_type']=='SBA':assert len(expected)==1
  key='AMBIGUOUS' if ambiguous else 'YES'
  av=list(authorities.values());lver='MINOR_EDIT' if ambiguous else 'KEEP'
  explanation={'read_in_full':True,'core_reasoning_read':True,'all_choice_analyses_read':[c['id'] for c in q['choices']],'learning_boundary_read':True,'visible_explanation_sha256':digest(q['explanation']),'core_finding_ko':('POA 실행의 법정 요건 설명은 맞지만 이미 없는 POA의 사례 사실을 뜻하는지 일반 요건인지 해설이 구별하지 않는다.' if ambiguous else 'core reasoning의 법적 방향과 사례 범위를 공식 본문에 대조했다. 아래 각 보기 판단과 모순되는 독립 확인 오류는 발견하지 않았다.'),'choice_analysis_findings_ko':{c['id']:('해설은 이 보기를 옳다고 단정하지만 stem에 “described”의 실행 대상이 없어 사실/요건 해석을 해소해야 한다.' if truth[i]=='U' else '해설의 '+('옳음' if truth[i]=='T' else '틀림')+' 판단 및 '+('오류선택' if polarity=='INCORRECT' else '정답선택')+' 극성은 위 exact primary 조항과 부합한다. '+findings[i]['finding_ko']) for i,c in enumerate(q['choices'])},'scope_limit_ko':'학습경계가 family 네 변형의 동일 사례임을 명시한 사실을 확인했다. 이것을 네 개의 독립 임상 사례로 세지 않았다.'}
  crit={x:True for x in ['jurisprudence_reasoning','practice_plausibility','authentic_distractors','wording_not_guessable','reasoning_not_trivia','natural_rule_combination','appropriate_drug_context','distinct_from_bank','not_schedule_flashcard','public_style_without_copying']}
  if n not in PASS:
   if n in {805,806,808,799}:crit['natural_rule_combination']=False
   else:crit['wording_not_guessable']=False
   if n in {833,837,838}:crit['authentic_distractors']=False
   if n==826:crit['reasoning_not_trivia']=False
  focus=FOCUS[n]
  cf={
   'jurisprudence_reasoning':focus+'에 대해 행위자·조건·기산점 또는 예외를 법규에 적용한다. 법적 적용 요소가 존재한다.',
   'practice_plausibility':q['stem'].split('\n\n')[0]+'라는 업무 상황은 약국의 검토/관리 과정에서 발생할 수 있다. 전제의 적법성은 사례가 명시한 범위까지만 수용했다.',
   'authentic_distractors':'각 보기는 '+focus+'와 관련하여 별도 scope·문서·기한·예외를 섞는 혼동을 제시한다. 법적으로 틀린 선택지는 per-choice 근거와 구별했다.',
   'wording_not_guessable':'정답 '+','.join(q['correct_choice_ids'])+'의 위치·길이만으로 정답을 결정할 단서는 충분하지 않다. 실질적인 '+focus+' 규칙을 알아야 한다.',
   'reasoning_not_trivia':focus+'를 사례에 적용해 법적 결과를 골라야 한다. 숫자가 있는 경우 임의 암기 빈도가 아니라 대상·분모·기산점·계수 방식의 법적 의미를 평가했다.',
   'natural_rule_combination':'같은 '+{797:'수의 처방 검토',801:'식용 동물의 약물 사용',805:'검사와 sample 처리',809:'controlled stock 주문',813:'등록자 주문의 위임과 인증',817:'분배 예외 계산',821:'stock 주문과 반환',825:'손실의 연방 보고',829:'기관별 병행 보고',833:'stock 폐기',837:'등록 활동 inventory',841:'열린 container inventory',845:'Schedule II 재고 대조'}[g]+' 업무의 조건들이 연결된다. 다른 문제로부터 숨은 사실을 보태지 않았다.',
   'appropriate_drug_context':'이 규칙은 특정 brand/generic보다 '+('Schedule II/III와 tablet/capsule container의 구별' if g==841 else '행위자·물품 경로·등록/보안 조건')+'에 의해 결정된다. 무관한 약물명을 억지로 넣지 않은 것이 법적 맥락에 적합하다.',
   'distinct_from_bank':'canonical top2와 public top2의 실제 visible 전문을 읽었다. 아래 duplicate evidence처럼 같은 가족의 보관용 변형은 매우 유사하나 배정 ID는 current recommended pool에 없다. canonical 가까운 문항과도 공유 법규 외의 사례/판단 초점을 비교하여 별도 연습 변형으로만 인정한다.',
   'not_schedule_flashcard':focus+'를 stock/처방/보고 상황에 적용하므로 약물 이름에서 schedule만 답하는 flashcard가 아니다.',
   'public_style_without_copying':'2026-11-04 실제 읽은 NABP 공개 1쪽 sample의 선택 지시 형식과 비교했다. 단일선택/복수선택 지시와 오류선택 극성이 명시되어 있고 공개 sample 문장·약물 배치를 재현하지 않는다. 비공개 Pre-MPJE는 사용하지 않았다.'}
  if n not in PASS:
   for k,v in crit.items():
    if not v:cf[k]=FAIL_REASON[n]
  dup=near[qid].copy();dup.update(actual_visible_read=True,read_packet_path=PREFIX+'/nearest-visible-read-packet.json',read_packet_sha256=sha((OUT/'nearest-visible-read-packet.json').read_bytes()),assigned_in_current_recommended_pool=qid in recommended,semantic_comparison_ko=duplicate_note(g,near[qid]),limitation_ko='unigram cosine는 후보 선정에만 사용했다. public pool에는 archive variants도 포함된다. 추천 여부는 recommended_ids locator만 투영했으며 이전 저자/감사 판정은 읽지 않았다. 단어 유사도가 높은 비관련 canonical도 아래처럼 실제 법적 초점으로 구별했다.')
  records.append({'question_id':qid,'record_sha256':row['record_sha256'],'family_id':original[qid].get('family_id') or original[qid].get('question_family_id'),'read_scope':{'original_stem':True,'all_choices':[c['id'] for c in q['choices']],'stored_key':True,'complete_korean_explanation':True,'core_reasoning':True,'choice_analysis':True,'learning_boundary':True,'source_packet':PREFIX+'/assigned-visible-input.json','visible_content_sha256':row['visible_content_sha256']},'legal_review':{'existing_answer_correct':key,'stored_key':q['correct_choice_ids'],'independently_expected_key':expected if not ambiguous else None,'possible_keys_if_referent_is_normative_requirement':q['correct_choice_ids'] if ambiguous else None,'possible_keys_if_referent_is_completed_case_fact':(['B','C','D'] if n==815 else ['C','D']) if ambiguous else None,'polarity':polarity,'choice_by_choice_findings':findings,'authorities':av,'verdict':lver,'finding_ko':('정답 조합/단일 오류의 유일성이 “described POA execution” 해석에 따라 달라진다. 적법 POA는 ...해야 한다는 규범 문장으로 명확히 수정 후 fresh 재감사한다.' if ambiguous else focus+'에 대해 모든 보기와 해설을 대조했다. '+('INCORRECT 극성을 반전하여 단일 오류를 확인했다.' if polarity=='INCORRECT' else 'SATA의 모든 참 보기를 포함했는지 확인했다.' if q['question_type']=='SATA' else '질문이 겨냥한 Case의 유일하게 옳은 선택지를 확인했다.')),'blocker':'AMBIGUOUS_POA_REFERENT' if ambiguous else None,'original_explanation_review':explanation},'realism_review':{'verdict':'PASS' if all(crit.values()) else 'FAIL','decision':'KEEP' if all(crit.values()) else 'MINOR_EDIT' if n in {815,816,826,828} else 'MAJOR_REWRITE','criteria':crit,'criterion_findings_ko':cf,'finding_ko':'10개 기준을 각각 확인했다.' if all(crit.values()) else FAIL_REASON[n],'duplicate_evidence':dup},'disposition':'INDEPENDENT_ASSESSED' if all(crit.values()) and not ambiguous else 'NEEDS_REMEDIATION','safe_hold_recommended':not all(crit.values()) or ambiguous,'release_eligible':False,'required_next_action_ko':'독립 legacy 결과를 root가 원장에 순차 통합한다. canonical release credit은 0이며 canonical fresh audit/adjudication은 별도이다.' if all(crit.values()) and not ambiguous else '위 개별 모호성/현실성 결함을 editor가 수정하고 새 원문 hash로 fresh 법규·현실성 검토한다. 감사자는 질문을 수정하지 않는다.'})
 for r in records:
  r['legal_review']['correction_ko']=('POA 보기의 described 실행 사실 지시어를 지우고 “A compliant power of attorney must be executed by the required grantor, grantee, and two witnesses.”라는 일반 법정 요건으로 명확히 한다. 원문은 감사자가 수정하지 않았으며 새 hash에 재감사가 필요하다.' if r['legal_review']['existing_answer_correct']=='AMBIGUOUS' else None)
 profile=load(ROOT/'data/exam_style/mpje_style_profile.json');blueprint=load(ROOT/'data/blueprint.json')
 memo=OUT/'nabp-public-style-memo.ko.md';nm=load('/tmp/independent-phase14-a-nabp-meta.json')
 nabp={'source_id':'nabp-public-sample-style','authority':'NABP publicly posted MPJE sample format; not legal authority','source_type':'PUBLIC_OFFICIAL','official_url':nm['official_url'],'exact_section':'One-page public format example; all public sample page read','law_checked_date':DATE,'retrieved_at':nm['retrieved_at'],'retrieval_method':'Python urllib direct HTTPS; normal User-Agent; default TLS/proxy','effective_date':None,'version':'2020/07 public sample PDF retrieved 2026-11-04','effective_date_limitation_ko':'선택 형식만 확인하며 2026 내용영역/난도/시험 전체의 대표성 및 법적 권위로 사용하지 않는다.','evidence_path':str(memo.relative_to(ROOT)),'evidence_sha256':sha(memo.read_bytes()),'raw_sha256':nm['raw_sha256'],'private_text_sha256':nm['text_sha256'],'raw_bytes':nm['raw_bytes'],'public_raw_redistribution':False,'public_evidence_mode':'Retained independently authored memo; copyrighted raw PDF/text private /tmp only, unretained in repository; raw_path omitted'}
 report={'schema_version':'independent-legacy-review/1','stage':'independent-legacy','independent_of_authors':True,'auditor':'GPT','auditor_instance':'GPT:/root/independent_wave14_a:20261104','actor_provenance':{'actor_id':'/root/independent_wave14_a','session_id':'/root/independent_wave14_a'},'canonical_audit':False,'canonical_release_credit':0,'release_eligible':False,'reviewed_at':DATE,'review_completed_at':datetime.now(timezone.utc).isoformat(),'job_id':assignment['job_id'],'source_base_commit':'f4a9661259129a94341712ad44c0f468b687d7d5','scope':{'assigned_question_count':40,'exact_ids':list(assignment['question_hashes']),'assignment_sha256':sha((OUT/'assignment.json').read_bytes()),'visible_packet_sha256':sha((OUT/'assigned-visible-input.json').read_bytes()),'original_choices_read':sum(len(r['original_visible_content']['choices']) for r in packet['records']),'existing_author_or_independent_reports_read':False,'hidden_truth_read':False,'protected_or_commercial_items_processed':False,'nearest_canonical_count':439,'nearest_public_count':2349,'nearest_unique_visible_candidates_read':77,'current_recommended_assigned_count':0},'contracts':{str(p):{'file_sha256':sha((ROOT/p).read_bytes())} for p in map(Path,['docs/RELEASE_POLICY.md','docs/AUDIT_WORKFLOW.md','docs/SOURCE_USE_POLICY.md','docs/QUESTION_AUTHORING_STANDARD.md','docs/INDEPENDENT_LEGACY_REVIEW_RUNBOOK.md','scripts/review_queue.py','scripts/build_full_corpus_review.py'])},'style_profile':{'profile_id':profile['profile_id'],'content_version':profile['content_version'],'semantic_hash':profile['content_hash'],'file_sha256':sha((ROOT/'data/exam_style/mpje_style_profile.json').read_bytes()),'schema_path':'schemas/exam_style_profile.schema.json','schema_file_sha256':sha((ROOT/'schemas/exam_style_profile.schema.json').read_bytes())},'blueprint':{'blueprint_id':blueprint['blueprint_id'],'content_version':blueprint['content_version'],'semantic_hash':blueprint['content_hash'],'file_sha256':sha((ROOT/'data/blueprint.json').read_bytes()),'schema_file_sha256':sha((ROOT/'schemas/blueprint.schema.json').read_bytes())},'sources':list(retained_sources.values())+[nabp],'retrieval_limitations_ko':['Firecrawl 공식 검색은 locator로 사용했으나 scrape는 credit 부족으로 실행되지 않았다. 그 실패는 별도 firecrawl-attempts.json에 보존하고 법적 확인으로 세지 않았다. 이후 직접 공식 HTTPS 조회는 TLS/proxy를 기본 상태로 유지했다.','과거 추정 URL의 247 CMR 9는 404였으며 ma-247-9.meta.json에 실패를 보존했다. 새 공식 professional-practice-standards PDF의 실제 본문으로 대체 확인했다.','eCFR은 조회 당시 title currency가 2026-11-02이다. 11월 3-4일에 아직 편집 반영되지 않은 법변경의 부재를 보장하지 않는다. 각 절별 최초 효력일 재구성은 하지 않았고 source마다 제한을 기록했다.','NABP raw PDF/text는 /tmp에만 남기고 public에는 자체 memo·원본/추출본 SHA·조회 timestamp만 기록했다.','protected full-preimage directory를 제외한 sparse worker tree다. 직접 source/hash/qrow/native 검증을 수행하고 loader/protected 전체 QA는 missing 환경에서 실행하지 않았으며 NOT_RUN이다.'],'summary':{'records':40,'existing_key_yes':sum(r['legal_review']['existing_answer_correct']=='YES' for r in records),'existing_key_ambiguous':sum(r['legal_review']['existing_answer_correct']=='AMBIGUOUS' for r in records),'realism_pass':sum(r['realism_review']['verdict']=='PASS' for r in records),'realism_fail':sum(r['realism_review']['verdict']=='FAIL' for r in records),'source_blocked':0,'canonical_release_credit':0},'records':records}
 write(ROOT/'reports/full-corpus-review/independent-phase14-a-review.json',report)
 print(json.dumps(report['summary'],ensure_ascii=False))

def duplicate_note(g,near):
 canon=[n['question_id'] for n in near['neighbors'] if n['collection']=='canonical439'];pub=[n['question_id'] for n in near['neighbors'] if n['collection']=='public2349']
 notes={797:'MA-Q-0174/0145는 사람에게 약물 투여할 수 있는 indication 범위를 묻고, 이 family는 수의 처방의 치료 대상·VCPR를 묻는다. 그 외 renewal/OTC naloxone은 단어 겹침뿐이다.',801:'canonical 가까운 문항은 인간 Schedule VI 필수정보·customer identifier·counseling/compounded label이다. 이 family는 식용 동물 잔류·VFD·bulk 구별이라 판단 경로가 다르다.',805:'MA-Q-0100과 sample paid inventory라는 Case B 판단은 실질적으로 겹친다. 다만 이 family는 무관한 rapid-test 사례를 더했으며 이를 새 통합 문제의 독창성으로 부풀리지 않았다. 기타 stock integrity/협업검사 문항과 구체 사실은 다르다.',809:'MA-Q-0064는 실행 64일 후 잔량 공급의 만료, MA-Q-0438은 electronic copy와 CSOS 저장 기록을 묻는다. 이 family의 order-date 기산점은 0064와 주제를 공유하지만 two-supplier/current paper 형식·receipt·registration 판단은 별도이다.',813:'MA-Q-0127과 직함만으로 서명 불가/POA라는 법리는 겹친다. 이 family는 MOR의 권한과 CSOS credential 공유를 병렬 검토한다. MA-Q-0068은 전자주문의 certificate 요건 자체라 추가 역할이 다르다.',817:'canonical top의 MA-Q-0061은 Schedule IV container 계수이고 0207은 LTC emergency kit의 총량 cap이다. dosage unit라는 단어만 겹치며 5% distributor registration 계산은 법규·행위가 다르다.',821:'MA-Q-0063과 Form 106/222 주문 문서의 구별이 겹친다. 이 family는 등록자 stock return과 patient return/expiry accountability를 더하며 0438의 전자 저장·0130의 destruction 경로와도 구체 행위가 다르다.',825:'MA-Q-0058과 조사 전 초기 notice 및 45일 후속 Form 106의 두 시계는 크게 겹친다. 이 family는 theft 수량 면제와 significance 판단을 추가하지만 별도 독립 사례로 모두 세어서는 안 된다. 0066은 분실 blank Form 222의 즉시 보고라 대상이 다르다.',829:'MA-Q-0115/0053은 QRE 및 serious patient injury 보고를 묻는다. 이 family는 confirmed drug loss의 RLCS와 DCP tampering 보고로 trigger·수신처·calendar/hour 기산점이 다르다. 0058은 DEA만의 시계이다.',833:'MA-Q-0130과 stock non-retrievable/Form 41은 겹친다. 이 family는 reverse distributor receipt 30일과 immediate administration residue 예외의 적용 범위를 더 묻는다. 0071/0326은 적격 수령자 선택으로 핵심 행동이 다르다.',837:'MA-Q-0059/0439와 zero-stock 초기 inventory는 실질적으로 가까운 법리이다. 이 family는 newly scheduling 효력일과 별도 장소/2년 주기를 덧붙인 보관용 학습 변형이며 신규 독립 사례 수로 확대하지 않는다.',841:'MA-Q-0061/0437과 열린 container Schedule별 exact-count 규칙은 같다. 이 family는 정확히 1,000 대 1,001 경계와 opening/closing·함량 구분에 초점을 둔다. 현재 추천 pool과 별개의 보관용 변형으로만 인정한다.',845:'canonical top은 patient-requested/shortage partial fill이라 “Schedule II, balance” 단어 외의 핵심 판단이 다르다. 이 family는 perpetual inventory·physical comparison·MOR discrepancy 조사이다.'}
 return '실독 canonical '+', '.join(canon)+' / public '+', '.join(pub)+'. '+notes[g]+' public top2는 동일 두 사례와 핵심 보기 문장을 반복하고 질문 대상 또는 극성/선택 형식만 바꾸는 같은 가족이다. 실제 반복을 인정하되 이 ID와 가까운 family가 현행 recommended pool에 함께 편입된 것으로 취급하지 않는다.'

if __name__=='__main__':main()
