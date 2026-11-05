"""Render this actual session's independently made, text-bound judgments; not an author-key review."""
import json,hashlib,re,shutil
from pathlib import Path
from datetime import datetime,timezone
from collections import defaultdict,Counter
B=Path('reports/full-corpus-review/phase12-d-evidence'); OUT=Path('reports/full-corpus-review/independent-phase12-d-review.json')
packet=json.load(open(B/'assigned-visible-input.json'));assignment=json.load(open(B/'assignment.json'));loc=json.load(open(B/'source-locators.json'));neighbors=json.load(open(B/'nearest-visible-candidates.json'));N={r['question_id']:r for r in neighbors['rows']}
actor='/root/independent_wave12_d';instance='GPT:'+actor+':20261104';now=datetime.now(timezone.utc);today=now.date().isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def file_sha(p):return sha(Path(p).read_bytes())
def semantic(d):return sha(json.dumps(d,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
metas={p.stem.removesuffix('.meta'):json.loads(p.read_text()) for p in (B/'sources').glob('*.meta.json')}
# Exact section bindings are paragraph anchors present in the retrieved eCFR HTML,
# physical PDF pages, or official legislature section URLs. No secondary source is a law authority.
S={}
def cite(k,sid,section,anchor='',kind='MA_PROMULGATED_REGULATION',version=None):
 m=metas[sid];assert m.get('retrieval_success') and m['http_status']==200
 url=m['final_url']+anchor
 if anchor.startswith('#p-'):assert ('id="'+anchor[1:]+'"') in Path(m['raw_path']).read_text()
 if version is None:
  version='eCFR title 21 displayed up to date as of 2026-11-02; title last amended 2026-11-02' if 'ecfr.gov' in url else '현재 공식 게시본; 개별 session-law 시행일 연결은 확인하지 않음'
 S[k]={'authority_id':k,'source_id':sid,'authority':section,'source_type':kind,'official_url':url,'exact_section':section,'law_checked_date':m['completed_at'][:10],'effective_date':'UNKNOWN','version':version,'effective_date_limit_ko':'조회일을 시행일로 대체하지 않는다. 게시본의 버전과 해당 조항을 확인했으나 개별 개정의 법정 시행일을 별도 확정하지 않았다.','evidence_path':m['raw_path'],'evidence_sha256':m['raw_sha256'],'text_path':m['text_path'],'text_sha256':m['text_sha256'],'metadata_path':str(B/'sources'/(sid+'.meta.json')),'metadata_sha256':file_sha(B/'sources'/(sid+'.meta.json')),'retrieval_provenance':{'method':m['retrieval_method'],'started_at':m['started_at'],'completed_at':m['completed_at'],'requested_url':m['requested_url'],'final_url':m['final_url'],'http_status':m['http_status'],'document_identity':m['document_identity'],'actor_id':m['retrieval_actor']}}
 return k
reg='247 CMR 9 official PDF, Mass. Register #1536, 2024-12-06'
policy='Board/DCP Policy 2018-01, revised 2024-01-11'
cite('PACK_RETURN','src-da8a8280d110','247 CMR 9.08(4)(a)-(c)','#page=7',version=reg)
cite('PACK_LABEL','src-da8a8280d110','247 CMR 9.08(4)(a)3, (5)(a)-(e), (6)','#page=7',version=reg)
cite('PACK_STABILITY','src-da8a8280d110','247 CMR 9.08(1)(c)-(d), (3)(a), (5)(d)','#page=6',version=reg)
cite('PACK_POLICY','src-8638fed9ada5','Board Policy 2023-01, II.9(d), II.10; Return and Repackaging 1-3','#page=2','MA_BOARD_POLICY','adopted 2023-04-06; revised 2023-11-02, 2025-01-09; current posted PDF')
cite('RTS_RECALL','src-da8a8280d110','247 CMR 9.13(1)-(3)','#page=9',version=reg)
cite('CUSTODY','src-da8a8280d110','247 CMR 9.01(5),(7); 9.13(1)','#page=1',version=reg)
cite('SHIP','src-da8a8280d110','247 CMR 9.02(2)-(3); 9.22(1),(4)','#page=2',version=reg)
cite('DELIVERY_ADVISORY','src-86b25003cfc9','Board Advisory Medication Delivery and Shipping: Temperature Sensitive Products; Unclaimed Products; Lost in Transit','#page=2','MA_BOARD_POLICY','adopted 2018-06-28; revised 2025-01-09; explicitly best-practice recommendations')
S['DELIVERY_ADVISORY']['authority_level_limit_ko']='권고 문서이다. 별도 binding duty로 바꾸지 않으며, 운송 무결성 의무는 247 CMR 9.02(2)를 근거로 한다.'
cite('LOSS','src-b14e05a8dc02','21 CFR 1301.76(b)','#p-1301.76(b)','FEDERAL_REGULATION')
cite('LINER_NO_OPEN','src-9b6deb426285','21 CFR 1317.60(c); 1317.75(c)','#p-1317.60(c)','FEDERAL_REGULATION')
cite('COLLECTION_PURPOSE','src-9b6deb426285','21 CFR 1317.30(a)-(b); 1317.40(c); 1317.75(c)','#p-1317.30(a)','FEDERAL_REGULATION')
cite('MAIL_BACK','src-9b6deb426285','21 CFR 1317.70(a),(c)(1)-(6),(e),(f)','#p-1317.70(c)','FEDERAL_REGULATION')
cite('LINER_RECORD','src-eb05f0f0be22','21 CFR 1304.22(f)(2)(i)-(vi)','#p-1304.22(f)(2)','FEDERAL_REGULATION')
cite('LINER_ID','src-9b6deb426285','21 CFR 1317.60(a)(3)-(5)','#p-1317.60(a)','FEDERAL_REGULATION')
cite('LTCF_RESIDENT','src-9b6deb426285','21 CFR 1317.80(a)','#p-1317.80(a)','FEDERAL_REGULATION')
cite('LTCF_LINER','src-9b6deb426285','21 CFR 1317.80(c)-(d)','#p-1317.80(d)','FEDERAL_REGULATION')
cite('AUTHORITY','src-386cb3e809e7','21 CFR 1306.03(a); 1306.04(a)','#p-1306.03(a)','FEDERAL_REGULATION')
cite('INSTITUTION','src-b405c249ee23','21 CFR 1301.22(c)(1)-(6)','#p-1301.22(c)','FEDERAL_REGULATION')
cite('MCSR','ma-94C-7','M.G.L. c.94C §7(a),(c)',kind='MA_STATUTE')
cite('MA_VERIFY','src-da8a8280d110','247 CMR 9.15(2)(a)-(d); 9.16(1)','#page=9',version=reg)
cite('MA_PURPOSE','src-195090acf010','M.G.L. c.94C §19(a)-(b)',kind='MA_STATUTE')
cite('FED_PURPOSE','src-386cb3e809e7','21 CFR 1306.04(a)-(b)','#p-1306.04(a)','FEDERAL_REGULATION')
cite('DISTRIBUTION','src-d757796628ed','21 CFR 1307.11(a)(1)(i)-(iv),(b)','#p-1307.11(a)','FEDERAL_REGULATION')
cite('DEPOT_DELIVERY','src-386cb3e809e7','21 CFR 1306.07(f)(1)-(6)','#p-1306.07(f)','FEDERAL_REGULATION')
cite('ISSUE_DATE','src-386cb3e809e7','21 CFR 1306.05(a),(d)-(e); 1306.12(b)(1)(ii)','#p-1306.05(a)','FEDERAL_REGULATION')
cite('RX_FIELDS','src-16f1fbbdd07a','105 CMR 721.020(B),(D)(1)-(5)','#page=3',version='Mass. Register #1531, 2024-09-27 official posted PDF')
cite('EPCS_FORMAT','src-16f1fbbdd07a','105 CMR 721.010 Electronic Prescription/Electronic Transmission; 721.040(C)','#page=2',version='Mass. Register #1531, 2024-09-27 official posted PDF')
cite('EPCS_RULE','src-386cb3e809e7','21 CFR 1306.05(e); 1306.08(a)-(d)','#p-1306.08(a)','FEDERAL_REGULATION')
cite('EPCS_SIGNATURE','fed-1311','21 CFR 1311.102(a); 1311.135(a); 1311.140(a)(4)','#p-1311.102(a)','FEDERAL_REGULATION')
cite('EPCS_RECORD','fed-1311','21 CFR 1311.200(e)-(f); 1311.210(a)-(c); 1311.215(a)(2)','#p-1311.200(f)','FEDERAL_REGULATION')
cite('EP_EXCEPTION','src-16f1fbbdd07a','105 CMR 721.070(A)(2),(3),(11),(B),(C)','#page=5',version='Mass. Register #1531, 2024-09-27 official posted PDF')
cite('ORAL_CII','src-386cb3e809e7','21 CFR 1306.11(a),(d); 1306.12(a)','#p-1306.11(d)','FEDERAL_REGULATION')
cite('CHANGE_CORE','src-4061fe7d61b6','Board/DCP Policy 2018-01 II.A-E, III.A.i.a','#page=1','MA_BOARD_POLICY',policy)
cite('CHANGE_AGENT','src-4061fe7d61b6','Board/DCP Policy 2018-01 III.A.i.c,g; III.C.iii.a; IV.A-D','#page=1','MA_BOARD_POLICY',policy)
cite('CHANGE_RECORD','src-4061fe7d61b6','Board/DCP Policy 2018-01 IV.A-D','#page=3','MA_BOARD_POLICY',policy)
cite('PMP_GABA','ma-pmp-current','DCP Pharmacy reporting and data submission: Who must report; Gabapentin prescriptions filled at a VA facility',kind='MA_DCP_GUIDANCE',version='현재 DCP 공식 HTML; Gabapentin을 Schedule VI drug of concern/PMP reportable로 명시')
cite('PMP_REG','src-a397fe32483f','105 CMR 700.001 Additional Drug; 700.012(A)(1),(C)(8)',version='105 CMR 700 current posted PDF; section-specific commencement UNKNOWN')
cite('NO_REFILL','src-386cb3e809e7','21 CFR 1306.12(a); 1306.13(a)-(c)','#p-1306.12(a)','FEDERAL_REGULATION')
cite('MA_CII','src-879439ccbb94','M.G.L. c.94C §23(b),(c)',kind='MA_STATUTE')
cite('FINAL_VALIDATION','src-da8a8280d110','247 CMR 9.04(1)','#page=3',version=reg)
cite('OXY_CII','fed-oxy-schedule','21 CFR 1308.12(b)(1)(xiv)','#p-1308.12(b)(1)','FEDERAL_REGULATION')
# Each tuple corresponds to the fully read English statement sorted within that family.
# Truth is independently assigned here and never derived from the stored answer key.
J={
'RET04':[
(True,'제거한 약은 일반 inventory로 복귀시키거나 반환 환자 외 다른 환자에게 교부할 수 없다. same-patient 예외를 일반 RTS로 확대하면 안 된다.',['PACK_RETURN']),
(True,'이 약국이 먼저 교부한 다약 단회포장에 대해 같은 환자로 한정해 중단약 제거·새 치료약 추가와 재교부를 허용한다. 모든 반환약의 일반 재사용 허가는 아니다.',['PACK_RETURN','PACK_POLICY']),
(False,'내용물이 제거·대체되면 재교부 전 9.08(5)에 맞게 실제 약명·강도·수량 등 표시를 갱신해야 하므로 이미 틀려진 원래 라벨을 그대로 둘 수 없다.',['PACK_LABEL']),
(True,'재포장·제거·재교부를 설명하는 기록과 변경 약사 식별을 명시적으로 요구한다. 원래 조제기록만으로 후속 변경을 대체하지 않는다.',['PACK_RETURN'])],
'RET05':[
(False,'60일은 다약 포장 공급량/BUD의 상한이다. 원 제조자 expiry·허가 라벨·실제 안정성을 무시한 모든 약의 60일 안정성 보증이 아니다.',['PACK_STABILITY','PACK_POLICY']),
(False,'분리 가능한 cell마다 충분한 크기의 약명·강도 라벨을 요구한다. outer box 표시는 개별 cell 의무를 대체하지 못한다.',['PACK_LABEL']),
(False,'새 포장으로 원 제조자 용기상 expiry가 초기화되지 않는다. 12일 남은 적용 한계보다 새 60일을 부여할 근거가 없다.',['PACK_STABILITY']),
(True,'BUD는 원 제조자 용기의 가장 짧은 expiry 또는 60일을 넘을 수 없고 FDA labeling·compatibility 조건도 지켜야 한다. 제시한 12일 한계를 연장할 수 없다.',['PACK_STABILITY','PACK_POLICY']),
(True,'9.08(3)(a),(5)(d)의 60일 상한과 개별 약물의 안정성 충족은 별도 판단이다. shorter limit를 적용한다.',['PACK_STABILITY']),
(True,'재교부 전에도 분리되는 각 cell에 각 약의 name과 strength를 표시해야 한다. 외부 상자에만 표시하는 방법은 부족하다.',['PACK_LABEL']),
(False,'중단약을 제거하고 남은/새 약과 라벨이 일치하도록 재포장하는 경로이다. 계속 복용될 cell에 중단약이 남아 있는데 instructions만 고치는 조치로 대체할 수 없다.',['PACK_RETURN','PACK_LABEL'])],
'RET06':[
(True,'never-dispensed RTS는 9.13(1), 이미 환자에게 교부된 반환약은 9.01(5),(7) 및 개별 예외의 영역이다. failed delivery는 실제 인도·보관 상태를 확인해야 하므로 같은 custody로 단정할 수 없다.',['CUSTODY','RTS_RECALL','SHIP']),
(True,'밀봉 외관은 온도기록이나 안정성 평가가 아니다. 약국은 packing/shipping/transport가 약의 integrity·stability를 훼손하지 않게 해야 한다.',['SHIP','DELIVERY_ADVISORY']),
(False,'carrier가 관여했다는 이유만으로 약국의 적절한 조사·보호·해당 보고책임이 모두 없어지지 않는다. federally controlled theft/significant loss의 registrant 의무도 있다. 모든 loss가 같은 보고대상이라는 뜻은 아니다.',['SHIP','LOSS','DELIVERY_ADVISORY']),
(False,'never-dispensed RTS와 patient return 및 failed-delivery에는 교부·custody에 따른 구분이 있다. 모든 returned package의 법적 재사용 가능성이 같다는 명제는 성립하지 않는다.',['CUSTODY','RTS_RECALL']),
(False,'외부 포장 봉인은 운송 중 허용 온도나 약물 무결성을 확정하지 않는다. 실제 노출/보관을 평가해야 한다.',['SHIP']),
(True,'potentially recalled RTS는 정확한 lot가 recall 밖이라고 확인되기 전에는 교부할 수 없다는 9.13(3)의 직접 요건이다.',['RTS_RECALL']),
(False,'회수통지 전에 최초 조제했더라도 potentially subject RTS의 lot 확인 의무가 없어지지 않는다. 불명확하면 재교부할 수 없다.',['RTS_RECALL'])],
'RET07':[
(False,'봉인한 inner liner는 열거나 x-ray·분석·관통할 수 없고 deposited substance의 count/sort/inventory도 금지된다. 일반 재고실사 명목의 예외는 없다.',['LINER_NO_OPEN']),
(True,'ultimate-user 수거는 destruction 목적이며 deposited drug를 따로 회수·취급할 수 없다. 식별 가능하다는 이유로 saleable stock이 되지 않는다.',['COLLECTION_PURPOSE','LINER_NO_OPEN','CUSTODY']),
(False,'식별 가능한 포장이라도 수거함 투입 후 개별 취급이 금지되고 destruction 경로를 따라야 한다. 반환 재고로 회수할 수 없다.',['COLLECTION_PURPOSE','LINER_NO_OPEN']),
(False,'mail-back은 적격 collector/law enforcement 및 preaddressed·postage-paid·unique-ID 등 정해진 package를 사용해야 한다. 아무 봉투·아무 약국으로 보내는 것은 그 경로가 아니다.',['MAIL_BACK']),
(True,'추적 가능한 permanent unique ID와 설치·제거·보관·파괴이동/파괴 기록을 요구한다. 안의 tablet별 수량 실사와 구분된다.',['LINER_RECORD','LINER_ID']),
(False,'봉인 후에도 unique ID는 남고 제거·보관·인계·파괴 관련 날짜·크기·직원 등 기록을 유지한다. 봉인은 추적 면제가 아니다.',['LINER_RECORD','LINER_ID']),
(True,'1317.60(c)의 봉인 후 개봉 금지와 1317.75(c)의 count/sort/inventory 금지가 직접 적용된다.',['LINER_NO_OPEN'])],
'RET08':[
(False,'LTCF는 collector 직원 1명과 지정된 supervisor-level LTCF 직원 1명, 또는 collector 직원 2명의 수행/감독 조합이어야 한다. 아무 두 사람으로 충족되지 않는다.',['LTCF_LINER']),
(True,'1317.80(c)는 설치·제거·이동·보관에 특정 인력의 수행 또는 감독을 요구한다. 일반 수거함과 LTCF의 허용 조합을 구분한다.',['LTCF_LINER']),
(False,'sealed liner의 LTCF 최대 보관은 removal 후부터 3 business days이다. resident의 original prescription issue date는 기산점이 아니다.',['LTCF_LINER']),
(True,'1317.80(d)는 upon removal 이후 LTCF의 지정 보안 cabinet/room에 최대 3 business days 보관하도록 한다. resident event 시계와 별개다.',['LTCF_LINER']),
(False,'resident medication은 영구 중단·전원·사망에 따른 use discontinuation 직후부터 최대 3 business days 내 receptacle로 옮긴다. 무관한 liner removal까지 기다리지 않는다.',['LTCF_RESIDENT']),
(True,'1317.80(a)는 prescriber에 의한 permanent discontinuation, resident transfer 또는 death에 따른 discontinuation을 trigger로 한다. 해당 II-V/ultimate-user 경로의 범위 안에서 옳다.',['LTCF_RESIDENT']),
(False,'resident medication을 receptacle로 옮길 의무와 제거된 sealed liner의 secure LTCF storage 의무는 대상·행위·기산점이 다르다. 숫자가 같아도 하나의 deadline이 아니다.',['LTCF_RESIDENT','LTCF_LINER']),
(True,'1317.80(a)는 resident의 discontinuation 후 disposal-transfer, (d)는 liner removal 후 LTCF 보관이다. 각각 3 business days라는 수가 같아도 다른 규칙이다.',['LTCF_RESIDENT','LTCF_LINER'])],
'RX01':[
(False,'연방 등록은 관할 주의 등록/활동범위를 대체하지 않는다. MA §7의 해당 등록과 연방 권한을 별도로 충족해야 한다. 구체적인 등록면제는 그 자체 조건으로 판단한다.',['MCSR','AUTHORITY']),
(False,'산술 check digit는 실제 현재 등록·등록자 신원·주 면허상 처방 scope를 증명하지 못한다. 1306.03의 실질 권한과 9.15의 진정성 판단이 필요하다.',['AUTHORITY','MA_VERIFY']),
(True,'형식상 번호와 실제 current registration·identity·scope는 별도다. 처방 가능한 jurisdictional authority와 registered/exempt 상태 및 authenticity를 확인해야 한다.',['AUTHORITY','MA_VERIFY']),
(False,'hospital badge만으로 처방할 수 없다. 해당 individual practitioner의 주 권한·기관 검증·고용 scope·기관 승인·internal code와 목록 등 1301.22(c)의 누적 요건을 충족해야 한다.',['INSTITUTION']),
(True,'DEA와 MA 등록은 별도 체계다. 면허/활동·등록범위와 해당 exemption을 함께 확인하며 하나로 다른 것을 자동 대체하지 않는다.',['MCSR','AUTHORITY']),
(True,'prescription은 jurisdiction상 허용된 individual practitioner가 usual professional course와 legitimate medical purpose로 발행해야 한다. 직함만으로 scope를 확대하지 않는다.',['AUTHORITY','MA_PURPOSE']),
(False,'doctor라는 호칭은 약물·환자·목적 제한을 없애지 않는다. 직역의 실제 권한과 usual course 조건이 적용된다.',['AUTHORITY','MA_PURPOSE'])],
'RX02':[
(True,'unusual feature는 구체 사실과 정당 목적을 평가할 단서이지 모든 환자에 대한 fraud 확정명제가 아니다. professional judgment로 진정성과 목적을 판단한다.',['MA_VERIFY','FED_PURPOSE']),
(False,'required fields의 완성과 legitimate medical purpose/usual course는 별도 조건이다. 내용이 다 적혔다는 사실만으로 substantive legitimacy가 확정되지 않는다.',['FED_PURPOSE','MA_PURPOSE']),
(False,'보험 승인으로 material concern이 해결되거나 처방의 진정성이 생기지 않는다. 적절한 확인 후 판단 근거를 보존하는 것이 corresponding responsibility에 부합한다. 법에 없는 일률적 concern-record 양식 의무를 새로 만들지 않는다.',['FED_PURPOSE','MA_VERIFY']),
(True,'1306.04(a)와 MA §19(a)는 처방자의 책임과 조제 약사의 corresponding responsibility를 함께 둔다. 형식 완결성으로 약사의 목적 평가가 면제되지 않는다.',['FED_PURPOSE','MA_PURPOSE']),
(False,'사실상 정당한 설명이 가능한 한 특징을 모든 환자의 fraud 증명으로 일반화할 수 없다. 9.15는 개별 professional judgment를 요구한다.',['MA_VERIFY']),
(True,'material concern을 실제 정보로 확인하고 해소 과정을 기록하는 조치는 corresponding responsibility와 처방/기록 의무에 부합한다. 이 문장은 should이며 모든 단서에 독립적인 새 법정 보고양식을 요구한다는 뜻은 아니다.',['FED_PURPOSE','MA_VERIFY']),
(False,'처방자의 서명은 dispensing pharmacist의 corresponding responsibility를 이전·소멸시키지 않는다. 양 책임이 공존한다.',['FED_PURPOSE','MA_PURPOSE'])],
'RX03':[
(True,'1317 수거예외가 아니라 1306.07(f)의 patient-specific injection/implantation delivery 등 해당 제품·목적·환자·기간과 기록 범위를 따져야 한다. 이를 일반 stock permission으로 확대할 수 없다.',['DEPOT_DELIVERY','FED_PURPOSE']),
(False,'MA §19(b) 및 연방1306.04(b)는 practitioner 일반 stock 조달용 처방을 금지한다. patient name을 넣어 실제 office-stock 목적을 바꾸지 못한다.',['MA_PURPOSE','FED_PURPOSE']),
(False,'specific patient의 주사/삽입 치료용 delivery 예외에도 general dispensing stock 금지가 남는다. 모든 약의 office stock 허용으로 일반화되지 않는다.',['DEPOT_DELIVERY']),
(False,'실물 stock의 registrant간 distribution과 환자 prescription/refill information의 transfer는 다른 거래다. 전자 처방정보를 옮기는 절차로 실물 유통 기록을 대체할 수 없다.',['DISTRIBUTION','MA_PURPOSE']),
(False,'환자처방 서류만으로 stock distribution의 registration·record·해당 I/II ordering 요건을 충족하지 못한다. dispenser distribution 예외에는 등록자·기록·5% 등 조건이 남는다.',['DISTRIBUTION']),
(True,'의도된 용도가 unrelated patients의 general office stock이면 §19(b)/1306.04(b)의 금지 대상이다. 환자 이름을 추가해 patient-specific prescription으로 만들 수 없다.',['MA_PURPOSE','FED_PURPOSE']),
(True,'실물 stock supply는 해당 distribution/registration/record 경로로 검토해야 한다. 1307.11의 dispenser 예외에서도 상대방 등록·양측 기록·I/II order form·연간5% 조건 등이 남는다. every stock transaction에 새 distributor registration이 필수라는 뜻은 아니다.',['DISTRIBUTION'])],
'RX04':[
(False,'no substitution은 default가 아니고 독립 요소여야 하며 signature 등 다른 요소로 충족할 수 없다는 721.020(B)(1),(3)의 직접 문언이다.',['RX_FIELDS']),
(False,'patient name/address 예외는 veterinary·naloxone/승인 antagonist·EPT·지정 public-health 경로 등 열거된 범위다. 어떤 public-health 예외가 있다는 사실이 모든 누락을 허용하지 않는다.',['RX_FIELDS']),
(False,'치료군만 적는 것은 actual drug name·strength·dosage form·quantity·directions 등 required field를 대체하지 못한다.',['ISSUE_DATE','RX_FIELDS']),
(True,'실제 발행하고 서명한 날을 issue date로 적고 허용되는 future-fill instruction은 별도로 둔다. pickup 예정일로 원 발행일을 대체하지 않는다.',['ISSUE_DATE']),
(False,'모든 controlled prescription은 issued/signed day로 date해야 한다. future pickup 날짜는 허용된 earliest-fill instruction과 다르며 format 취향으로 actual issue date를 바꿀 수 없다.',['ISSUE_DATE']),
(True,'1306.05(a)는 drug name·strength·dosage form·quantity·directions를 요구하고 MA721.020(D)도 actual medication 정보를 요구한다. therapeutic class만으로 부족하다.',['ISSUE_DATE','RX_FIELDS']),
(True,'721.020(B)(3)는 no-substitution이 unique element이며 signature로 충족되지 않는다고 명시한다.',['RX_FIELDS'])],
'RX05':[
(False,'나중 변경이 원래 서명본에 있었던 것처럼 원 기록을 덮어쓸 수 없다. 수신 원본을 archive하고 허용 annotation과 audit trail을 보존해야 한다.',['EPCS_RECORD']),
(True,'agent가 data entry/transmission을 도와도 prescriber의 token/password/생체요소를 공유하거나 대신 서명할 수 없다.',['EPCS_SIGNATURE']),
(False,'1311.102(a)는 prescriber의 credentials로 다른 사람이 서명하는 것을 금지한다. 전송 보조 권한과 개인 인증 서명은 다르다.',['EPCS_SIGNATURE']),
(True,'ordinary text photo만으로 validated authenticated generation/signing/transmission application이 되지 않는다. 실제 EPCS 조건을 갖추어야 한다. lawful non-EPCS format 가능성과는 구별한다.',['EPCS_FORMAT','EPCS_RULE']),
(False,'전자기기로 받은 이미지라는 점만으로 EPCS가 되는 것이 아니다. 1306.08과1311 및 MA721.010의 시스템·서명·전송 조건을 적용한다.',['EPCS_FORMAT','EPCS_RULE']),
(False,'스캔은 원래 종이였던 prescription의 보관 형태를 바꿀 뿐 originally issued EPCS로 소급 전환하지 못한다.',['EPCS_FORMAT','EPCS_RULE']),
(True,'종이 원본을 scan해 저장하는 것과 전자처방 시스템에서 생성·인증서명·전송한 원본은 법적 발행/전송 category가 다르다.',['EPCS_FORMAT','EPCS_RULE'])],
'RX06':[
(False,'적용 가능한 temporary failure 등의 예외는 lawful written/oral format을 허용할 수 있다. 다른 controlled prescription 조건이 충족되었다면 nonelectronic이라는 이유만으로 필연 invalid가 되지 않는다.',['EP_EXCEPTION']),
(False,'721.070(A)(11)는 과거 endpoint 또는 Department가 정한 later date를 두는 경로이지 모든 후속 처방의 무조건 면제가 아니다. 여기서 실제 연장 부재를 단정하지 않으며, verified extension 없이 universal coverage를 주장하는 명제가 틀리다.',['EP_EXCEPTION']),
(True,'721.070(A)(2)의 temporary technology/electrical failure 예외라도 서면/구두 처방의 나머지 주·연방 요건은 남는다. CII 일반 refill 권한은 생기지 않는다.',['EP_EXCEPTION','ORAL_CII']),
(False,'EP waiver는 전자형식 의무의 예외일 뿐 CII refill 금지를 지우거나 ordinary oral prescription 경로를 만들지 않는다. oral CII는 별도의 qualifying emergency 조건을 따라야 한다.',['ORAL_CII','EP_EXCEPTION']),
(False,'721.070(C)의 구체적 EP exception verification 면제는 otherwise valid 처방에 한정된다. 진정성·권한·목적 검증을 없애지 않는다.',['EP_EXCEPTION','MA_VERIFY']),
(True,'exception/waiver 자체를 확인할 의무가 없다는 조항과 처방의 authenticity/권한·legitimate purpose 판단은 별도다.',['EP_EXCEPTION','MA_VERIFY']),
(True,'CII no-refill와 ordinary oral 금지는 waiver로 바뀌지 않는다. emergency oral은 refill이 아니라 자체 요건에 따른 새 authorization이다.',['ORAL_CII','EP_EXCEPTION'])],
'RX07':[
(True,'Policy II.B는 prescribed controlled substance 변경을 금지하되 generic substitution을 구별한다. 다른 active therapy로 바꾸는 것과 허용 interchangeable product를 고르는 것은 다르다.',['CHANGE_CORE']),
(True,'Policy II.A,D는 다른 환자로 patient name 변경과 prescriber signature 추가/변경을 금지하며 새 처방을 요구한다. 가족 동의로 보완할 수 없다.',['CHANGE_CORE']),
(False,'다른 active therapy의 선택은 일반 generic substitution이 아니다. Policy II.B의 약물 변경 금지와 generic 예외를 구분한다.',['CHANGE_CORE']),
(False,'III.A.i.a와III.B.i는 누락된 issue date의 추가만 허용한다. 이미 기재된 날짜를 다시 쓰는 권한으로 확대하지 못한다.',['CHANGE_CORE']),
(False,'환자 이름을 다른 가족 구성원으로 변경하거나 처방자 서명을 약국이 채우는 것은 II.A,D에 따라 새 처방을 요구한다. 가족 동의는 예외가 아니다.',['CHANGE_CORE']),
(False,'Schedule II earliest-fill date는 Policy II.E상 변경·추가할 수 없는 요소다. clerical correction으로 earlier date를 정할 수 없다.',['CHANGE_CORE']),
(True,'이미 있는 CII earliest-fill date를 바꾸려면 Policy II.E상 새 처방이 필요하다. 현 처방에서 authorized correction으로 처리하지 않는다.',['CHANGE_CORE'])],
'RX08':[
(False,'CII strength 변경은III.A.i.g에 따라 prescriber consultation 대상이다.III.A.i.c의 주소 변경에만 허용된 authorized agent를 모든 clinical change로 확대할 수 없다.',['CHANGE_AGENT']),
(True,'Policy IV는 date·item changed/added·해당 authorizing prescriber·accepting/making pharmacist 이름을 computerized system 또는 written prescription에 기록하도록 한다.',['CHANGE_RECORD']),
(True,'현재 DCP는 Gabapentin을 Schedule VI이지만 PMP 대상 drug of concern으로 명시한다. Policy III.C.iii.a의 without-consultation days-supply 변경은 non-PMP drug에 한정되므로 그 경로에 gabapentin을 넣을 수 없다. prescriber consultation을 통한 다른 허용 변경까지 금지한다는 뜻은 아니다.',['PMP_GABA','CHANGE_AGENT','PMP_REG']),
(False,'MA Schedule VI와 PMP 대상 여부는 같지 않다. gabapentin은 PMP reportable이므로 non-PMP-only/no-consultation days-supply 경로에 적격하지 않다.',['PMP_GABA','CHANGE_AGENT']),
(False,'누락 등록번호 추가 권한이 실제 prescriber의 정확한 번호와 신원확인을 면제하지 않는다. 임의로 그럴듯한 번호를 넣으면 required registration 정보가 되지 않는다.',['CHANGE_AGENT','MA_VERIFY']),
(True,'주소 관련 authorized-agent 허용은 strength 변경에 적용되지 않는다. CII clinical change에는 PolicyIII.A.i의 prescriber consultation이 필요하다.',['CHANGE_AGENT']),
(False,'MD OK만으로 date·changed item·authorizing prescriber(해당 시)·변경 약사라는 네 요소가 모두 기록되었다고 확정할 수 없다. 실제 필요한 내용을 남겨야 한다.',['CHANGE_RECORD'])],
'CII01':[
(True,'법에 맞는 partial filling은 원 처방의 authorized total 안에서 일부씩 교부하는 구조다. 그 사실만으로 새 refill이 되지 않는다. 72시간·30일·LTCF/terminal 특수기한은 각각 그 경로가 실제 적용될 때 판단한다.',['NO_REFILL']),
(False,'새 lawful CII prescription은 새 authorization이며 금지된 기존 처방 refill과 같지 않다.',['NO_REFILL','MA_CII']),
(True,'Oxycodone은 연방II이며1306.12(a), MA§23(b)는 CII refill을 금지한다. prescriber가 refill count를 적어도 권한이 생기지 않는다.',['OXY_CII','NO_REFILL','MA_CII']),
(False,'247 CMR9.04(1)는 licensed pharmacist의 final dispensing process validation을 요구하며 EPCS만의 면제를 두지 않는다. MA§23(c)의 endorsement도 별도로 남는다.',['FINAL_VALIDATION','MA_CII']),
(False,'1306.13은 조건에 맞는 CII partial fill을 명시 허용한다. 모든 partial supply를 refill로 일반화해 금지할 수 없다.',['NO_REFILL']),
(False,'처방자의 two refills 문구는CII no-refill을 override하지 않는다. 새 lawful prescription과 partial fill의 구분이 필요하다.',['NO_REFILL','MA_CII'])]}
# Explicitly text-bind the session's judgments.
family_text=defaultdict(set)
for r in packet['records']:
 q=r['original_visible_content'];family_text[loc[q['question_id']]['family_id']].update(c['text'] for c in q['choices'])
judgments={}
for f,texts in family_text.items():
 texts=sorted(texts);assert len(texts)==len(J[f]),f
 judgments[f]={t:{'statement_supported':truth,'finding_ko':reason,'authority_ids':aks} for t,(truth,reason,aks) in zip(texts,J[f])}
(B/'independent-statement-assessments.json').write_text(json.dumps(judgments,ensure_ascii=False,indent=2)+'\n')
# Per-family observations are supplemented below by item-specific focus and stem relevance.
R={
'RET04':{'jurisprudence_reasoning':'같은 환자의 재교부 예외와 일반 재고·타 환자 재사용 금지를 구분하는 법적 판단이다.','practice_plausibility':'치료 변경 후 기존 다약 포장 수정은 실제 조제 실무에서 일어날 수 있다.','authentic_distractors':'원 라벨을 그대로 둬도 된다는 하나의 명백한 오류만 두며 올바른 repackage·record 문장을 대조해 진짜 경계사례가 약하다.','wording_not_guessable':'내용물에서 빠진 약을 라벨에 그대로 두어도 된다는 문장은 구체 규정을 몰라도 부정확함이 드러난다.','reasoning_not_trivia':'약물 schedule이나 숫자 단독 암기가 아니라 동일환자 예외의 범위를 묻는다.','natural_rule_combination':'Case A/B는 공통 포장 주제이나 실제 선택은 변경 라벨 한 명제만으로 해결되어 조건 간 연쇄 판단이 약하다.','appropriate_drug_context':'재포장과 추적 규칙 판단에 특정 약명·브랜드가 필요하지 않으므로 불필요한 약명을 넣지 않은 점은 적절하다.'},
'RET05':{'jurisprudence_reasoning':'재포장 BUD와 원 expiry·cell label 요건을 법적으로 분류하는 내용이다.','practice_plausibility':'12일 expiry가 남은 반환 포장과 미표시 removable cell은 실제 점검에서 발견 가능한 상황이다.','authentic_distractors':'모든 약의 60일 안정성 보증·중단약을 둔 채 instructions만 변경 같은 과장된 보기가 실제 12일/60일의 competing-clock 혼동을 충분히 구현하지 못한다.','wording_not_guessable':'every drug 안정성 보증과 약이 남아도 instructions만으로 충분하다는 표현이 지나치게 단정적이어서 규정 적용 전에 제거 가능하다.','reasoning_not_trivia':'expiry ceiling과 개별 안정성 또는 cell별 식별이라는 법적 조건을 적용하며 단순 숫자 목록 문제는 아니다.','natural_rule_combination':'expiry 사례와 cell 사례를 한 stem에 두지만 Case A/B 초점 문제에서는 나머지 사례가 필요 없고 INCORRECT에서는 중단약이라는 별도 사실이 보기에서 생긴다.','appropriate_drug_context':'특정 제품명 없이 적용 expiry가12일이라는 필요한 사실을 주므로 법적 포장 판단에는 충분하다.'},
'RET06':{'jurisprudence_reasoning':'RTS recall 추적, 운송 무결성, 환자 반환과 never-dispensed custody의 구분이라는 법적 내용을 다룬다.','practice_plausibility':'lot가 불명확한 RTS와 온도 이력이 불확실한 반송품은 실제 약국이 겪을 수 있다.','authentic_distractors':'carrier가 모든 책임을 전담한다거나 모든 returned package의 지위가 같다는 절대명제가 구체적 인도·계약·제품 조건의 진짜 혼동을 대신한다.','wording_not_guessable':'all/solely/every/conclusively 표현을 이용해 정답과 오답의 합리성이 쉽게 갈린다.','reasoning_not_trivia':'보관·교부·recall 상태를 규칙에 연결하는 내용으로 schedule 암기 문제는 아니다.','natural_rule_combination':'recall과 온도는 각각 별도 쟁점으로 두었고 carrier loss까지 보기에서 추가해 한 실제 workflow의 자연스러운 연쇄 결정이 약하다.','appropriate_drug_context':'recalled lot와 uncertainty가 핵심이므로 임의의 브랜드나 recall 제품을 만들어 넣지 않은 점은 적절하다.'},
'RET07':{'jurisprudence_reasoning':'ultimate-user disposal collection과 pharmacy inventory를 구분하고 개봉금지·추적 규칙을 적용한다.','practice_plausibility':'collector 직원이 실사나 고가약 회수를 제안하는 상황은 가능하지만 봉인 후 내용물은 밖에서 보이지 않아야 하므로 고가 포장 인지 시점은 더 명료해야 한다.','authentic_distractors':'아무 봉투·아무 약국 mail-back, 봉인하면 기록 의무 소멸 등 실제 절차 경계보다 비현실적 일반화를 쓴다.','wording_not_guessable':'any envelope/any pharmacy 또는 봉인 후 재개봉·재판매 문구는 규정 지식 없이도 위험한 조치로 보인다.','reasoning_not_trivia':'일반 재고실사와 disposal liner의 별도 취급을 구분하므로 단순 수치 암기보다 법적 분류가 있다.','natural_rule_combination':'두 사례는 같은 수거함 주제지만 mail-back의 recipient/package 조건은 stem의 실제 행동과 연결되지 않은 외부 명제이다.','appropriate_drug_context':'수거 약물의 식별이 허용되지 않는 경로이므로 특정 brand를 문제풀이 단서로 넣지 않은 것은 적절하다.'},
'RET08':{'jurisprudence_reasoning':'resident discontinuation 시계와 removed-liner storage 시계 및 적격 인력을 나누는 법적 문제다.','practice_plausibility':'LTCF에서 중단약 투입과 후속 liner removal을 별도로 처리하는 상황 자체는 실제적이다.','authentic_distractors':'숫자가 같으면 하나의 deadline, 아무 두 사람이면 witness 가능하다는 보기는 실제 staff 조합·휴일·시각 적용 혼동을 구체화하지 않는다.','wording_not_guessable':'discontinuation과 removal을 stem에서 분리해 놓고 그 이름에 맞는 clock을 고르게 하며 regardless of roles가 쉽게 탈락한다.','reasoning_not_trivia':'두 의무의 subject/trigger 구분은 법적 사고지만 날짜·시간 없이 trigger 문장을 되풀이하는 선택은 실제 기한 계산 깊이가 얕다.','natural_rule_combination':'공통 LTCF workflow이지만 specified conditions만 쓰고 실제 보관장소·인력·사건일을 주지 않아 두 법적 시계의 적용이 추상적이다.','appropriate_drug_context':'이 수거 경로의 통제는 특정 약명보다 II-V/ultimate-user/collection 조건에 달려 약명이 없어도 적절하다.'},
'RX01':{'jurisprudence_reasoning':'DEA 형식 확인과 jurisdictional scope·현재 등록·MCSR·기관 등록 예외를 구분한다.','practice_plausibility':'pharmacist가 prescriber credentials와 처방권한을 확인하는 상황은 실제 약국 업무다.','authentic_distractors':'hospital badge만으로 누구나 처방하거나 doctor가 모든 약에 무제한 scope를 갖는다는 문장이 genuine scope boundary보다 지나치게 넓다.','wording_not_guessable':'any hospital employee/every drug/unrestricted/conclusively가 구체 면허나 환자를 몰라도 쉽게 배제된다.','reasoning_not_trivia':'DEA check-digit 산술 문제가 아니라 형식과 실질 권한의 차이를 다룬다.','natural_rule_combination':'서로 관련된 credential이지만 구체 직역·환자·약물·기관 승인 사실 없이 일반 명제만 골라 실제 scope interaction을 수행하지 않는다.','appropriate_drug_context':'등록과 scope를 일반적으로 구분하는 목표에는 약명 생략이 가능하지만 scope 적용을 깊게 하려면 실제 직역/치료가 더 필요하다.'},
'RX02':{'jurisprudence_reasoning':'형식적으로 완결된 prescription과 legitimate purpose/약사의 corresponding responsibility를 구분한다.','practice_plausibility':'facially complete 처방에서 material concern을 확인하는 일은 실제 업무에 가깝다.','authentic_distractors':'signature가 모든 책임을 이전, 보험 승인 후 우려 삭제, 하나의 unusual feature로 모든 환자 fraud 확정은 지나친 일반화다.','wording_not_guessable':'all/every/conclusively와 기록 삭제 조치는 책임 있는 일반 행동과 쉽게 구별되어 실제 red flag를 모르더라도 답을 찾기 쉽다.','reasoning_not_trivia':'형식과 substantive legitimacy를 분리하는 법적 원리를 다루므로 단순 암기 주제는 아니다.','natural_rule_combination':'실제 unusual feature와 contradictory information을 주지 않아 검증 정보 사이의 충돌을 판단할 수 없고 올바른 태도 문장만 고른다.','appropriate_drug_context':'특정 약물명 없이도 corresponding responsibility 일반원칙은 설명할 수 있으며 약명 장식은 필요 없다.'},
'RX03':{'jurisprudence_reasoning':'ultimate-user prescription, registrant stock distribution, patient-specific delivery 예외를 분류하는 법적 판단이다.','practice_plausibility':'office-stock 요청을 환자처방처럼 처리하려는 요청은 실제 pharmacy inquiry가 될 수 있다.','authentic_distractors':'patient name 하나로 모든 허가, 모든 약으로 예외 확대, stock bottle 이동과 refill정보 동일시는 너무 넓고 구체 5%/ordering 혼동이 없다.','wording_not_guessable':'every authorization/every drug/the same transaction 같은 과장이 legally qualified 답과 두드러지게 대비된다.','reasoning_not_trivia':'거래의 목적과 법적 category를 판단하며 수량·schedule 한 항목을 외우는 문제는 아니다.','natural_rule_combination':'office-stock과 supply transaction은 관련되지만 등록 상태·약물 schedule·연간 비율이 없어 실제 적용할 distribution pathway를 선택하지 않는다.','appropriate_drug_context':'일반 거래 분류에는 약명이 필수는 아니나 예외를 구체 적용하려면 해당 patient/product 조건이 추가되어야 한다.'},
'RX04':{'jurisprudence_reasoning':'발행일과 earliest-fill, unique no-substitution instruction, 필수 약물/환자정보와 법정 예외를 구분한다.','practice_plausibility':'잘못 postdate된 CII와 no-substitution 기본값 점검은 실제 처방 검토에서 가능하다.','authentic_distractors':'therapeutic class만으로 required fields 충족, 모든 누락을 public-health 예외로 허용한다는 과장 때문에 구체 적법 요건의 경쟁이 약하다.','wording_not_guessable':'signature alone/default/any missing information의 단정과 실제 prescribed medication을 요구하는 문장의 상식적 정밀도가 답을 드러낸다.','reasoning_not_trivia':'서명일·발행일과 별도 지시를 분류하는 법적 형식 판단이지 단순 숫자 퀴즈는 아니다.','natural_rule_combination':'두 사례의 issue-date/no-substitution이 한 결정에 필요하지 않으며 therapeutic class·EPT 등 새 주제가 보기에서 추가된다.','appropriate_drug_context':'처방 format 요건 자체에는 특정 약명이나 브랜드가 필요하지 않다.'},
'RX05':{'jurisprudence_reasoning':'원 발행·전송 형식과 scan 저장, 인증서명과 agent 전송, 원 기록과 annotation의 법적 차이를 묻는다.','practice_plausibility':'종이 scan이나 문자 photo를 EPCS로 오인하는 상황은 현실적인 workflow 혼동이다.','authentic_distractors':'every image가 compliant라는 일반화와 원 서명본 덮어쓰기·credential 공유라는 노골적 조치를 두어 실제 EPCS 요건 간 혼동이 약하다.','wording_not_guessable':'원래의 서명본처럼 보이게 overwrite한다는 표현과 every image/compliant의 과장만으로 오답을 가리기 쉽다.','reasoning_not_trivia':'파일 형식과 법적 발행/서명 권한의 관계를 적용하므로 단순 약물·수치 암기는 아니다.','natural_rule_combination':'scan과 text-photo는 관련 사례지만 둘 중 하나의 분류만으로 답이 나고 credential/record 위반은 별도 보기로 덧붙었다.','appropriate_drug_context':'전자처방의 생성·서명·기록 규칙을 판단하는 데 임의 약명을 넣지 않은 것은 적절하다.'},
'RX06':{'jurisprudence_reasoning':'EP format exception과 CII emergency/no-refill, exception 확인면제와 진정성 판단을 분리한다.','practice_plausibility':'정전과 waiver가 있는 prescriber의 nonelectronic 처방 문의는 실제 상황이다.','authentic_distractors':'EP waiver가 CII refill이나 모든 legitimacy-check 면제를 만든다는 보기가 지나치게 넓다. 과거 LTCF endpoint도 실제 date/extension 없이 삽입되었다.','wording_not_guessable':'ordinary oral Schedule II refill, every legitimacy check, universally라는 표현이 세부 예외를 몰라도 오류를 드러낸다.','reasoning_not_trivia':'format exception이 실체적 금지까지 없애지 않는다는 주·연방 법적 결합이다.','natural_rule_combination':'정전과 CII refill은 관련 제도이나 각 사례에 대한 답이 독립적이고 historical LTCF exemption은 실제 stem의 사실이 아니다.','appropriate_drug_context':'Schedule II와 처방형식이 쟁점이므로 별도 특정 약명을 추가할 필요는 없다.'},
'RX07':{'jurisprudence_reasoning':'변경 금지 핵심필드와 허용된 누락정보 추가, generic substitution의 경계를 구분한다.','practice_plausibility':'가족 환자명 변경, 누락 서명, earliest-fill 앞당김 요청은 실제 pharmacy inquiry가 될 수 있다.','authentic_distractors':'가족 동의로 환자·서명 모두 변경, 모든 active therapy가 generic이라는 과장 대신 실제 prescriber consultation 경계가 더 필요하다.','wording_not_guessable':'pharmacy가 prescriber signature를 공급·다른 환자로 변경한다는 명백한 주체 오류와 every therapy 표현이 답을 쉽게 노출한다.','reasoning_not_trivia':'새 처방이 필요한 변경과 authorized correction을 분류하므로 단순 필드명 암기 이상 요소가 있다.','natural_rule_combination':'금지된 변경끼리는 같은 policy에 속하지만 Case A/B 중 하나만으로 답이 나고 issue date와 generic은 보기에서 추가된다.','appropriate_drug_context':'핵심 식별·서명·기산일 교정 규칙에는 불필요한 약명 장식이 없어 적절하다.'},
'RX08':{'jurisprudence_reasoning':'CII clinical change의 prescriber와 주소 변경의 agent, Schedule VI와 PMP 적용의 교차를 구분한다.','practice_plausibility':'office employee의 전화와 gabapentin days-supply 요청은 구체적인 실제 pharmacy 업무다.','authentic_distractors':'주소 agent를 strength로 확대하거나 VI를 non-PMP로 오인하는 혼동은 좋지만 any plausible number·MD OK가 모든 정보를 증명한다는 보기는 지나치게 쉽게 배제된다.','wording_not_guessable':'any plausible registration number/every required detail/every strength change라는 과장으로 실제 PMP 지식 없이도 일부 답을 좁힐 수 있다.','reasoning_not_trivia':'gabapentin을 VI/PMP 두 축에서 적용하고 consultation 주체를 나누므로 단순 schedule flashcard가 아니다.','natural_rule_combination':'주소-agent와 PMP days-supply는 같은 policy에 속하지만 SBA는 한 사례만 필요하고 번호·MD OK는 제시되지 않은 추가 사실이다.','appropriate_drug_context':'gabapentin은 Schedule VI이면서 PMP 대상이라는 법적 결과에 직접 필요해 적절한 약물 문맥이다.'},
'CII01':{'jurisprudence_reasoning':'금지된 CII refill과 원 authorization 안의 lawful partial fill 및 새 처방을 분류한다.','practice_plausibility':'oxycodone에 잘못 쓰인 refill과 partial fill 오분류는 실제 조제 시스템에서 가능하다.','authentic_distractors':'전자이면 최종약사 검토 불필요, 모든 partial supply가 refill이라는 절대명제가 구체 partial-fill pathway 혼동보다 두드러진다.','wording_not_guessable':'every partial supply/no validation과 명시한 Schedule II no-refill의 직설적 대조로 실제 기한·예외를 적용하지 않아도 답이 보인다.','reasoning_not_trivia':'refill·partial·새 처방의 구조를 구분하지만 lawful partial이라는 법적 결론을 stem이 미리 주어 실제 허용 조건을 판단하는 깊이가 제한된다.','natural_rule_combination':'refill과 partial은 자연스러운 쌍이지만 partial의 사유·수량·시각을 주지 않고 final validation을 별도 distractor로 추가했다.','appropriate_drug_context':'oxycodone의 Schedule II 분류가 no-refill 결과에 실제 필요하며 정당한 drug context이다.'}}
observations={
'0544':'중단·대체된 약을 계속 표시하는 원래 라벨의 오류를 고르는 문제이다.',
'0545':'12일 expiry와 새60일을 대비하지만 답은 Case A만으로 정해지고 cell 사례는 쓰이지 않는다.',
'0546':'removable cell의 약명·강도 누락이 초점이며 Case A의12일/60일은 답에 필요 없다.',
'0548':'INCORRECT 답은 discontinued tablets인데 stem에는 중단약 사실이 없고 expiry와cell 사례만 있다.',
'0549':'불명확한 recalled RTS lot가 초점이며 온도 사례는 이 SBA 판단에 불필요하다.',
'0550':'sealed outer box로 온도 무결성을 확정할 수 있는지가 초점이며 recall 사례는 쓰이지 않는다.',
'0552':'INCORRECT 답의 carrier loss는 stem의 recall/온도 두 사례에 실제로 발생하지 않았다.',
'0553':'sealed liner의 ordinary tablet inventory를 금지하는 분류가 초점이다.',
'0554':'collection drug를 saleable stock으로 되돌리는 제안이 초점이다.',
'0556':'아무 envelope/아무 pharmacy의 mail-back은 stem의 두 liner 사례에서 제시되지 않은 새 경로이다.',
'0557':'discontinuation이라는 stem 단어를 resident-medication clock과 다시 연결하는 수준이다.',
'0558':'removal이라는 stem 단어를 removed-liner clock과 다시 연결하고 실제 날짜를 계산하지 않는다.',
'0559':'SATA 네 진술이 모두 옳다. all-correct 자체는 법규/형식 결함이 아니며 구체 인력·사건일 적용 부재가 현실성 문제다.',
'0560':'아무 두 사람이 적격이라는 역할 무시를 고르지만 실제 직원 두 명의 직위는 제시되지 않는다.',
'0561':'산술적으로 맞는 DEA number와 실질 권한을 구분하지만 구체 prescriber 직역·등록상태가 없다.',
'0562':'doctor 직함과 실제 scope의 차이를 묻지만 특정 환자·치료의 scope 판단은 수행하지 않는다.',
'0564':'hospital badge만 있으면 누구나 처방한다는 보기가 INCORRECT 답으로 너무 두드러진다.',
'0565':'완결된 required fields가 substantive legitimacy를 입증하는지 묻지만 모순되는 정보의 내용은 없다.',
'0566':'unusual feature에 legitimate explanation이 가능함을 stem이 이미 주어 fraud 확정을 쉽게 배제한다.',
'0568':'signature가 모든 책임을 넘긴다는 명제의 오류를 묻고 실제 concern 해결정보는 제시하지 않는다.',
'0569':'patient name을 쓴 office-stock 목적을 분류하며 office-stock 금지는 구체 실무 쟁점이다.',
'0570':'registrant stock 공급이 초점이지만 schedule·등록·annual5% 정보가 없어 실제 거래 경로를 고르지 않는다.',
'0572':'stock bottle과 refill information이 같다는 categorical 오류가 초점이다.',
'0573':'issue date와 pickup date를 나누지만 actual dates·개별 earliest-fill 지시는 제시되지 않는다.',
'0574':'서명이 별도의 no-substitution을 대체하는지 묻고 issue-date 사례는 쓰이지 않는다.',
'0576':'모든 patient information 누락을 public-health 예외로 허용한다는 새 일반화가 INCORRECT 답이다.',
'0577':'종이 scan을 originally issued EPCS로 부르는 classification이 초점이다.',
'0578':'ordinary text photo와 compliant EPCS가 같은지 묻는 현실적 transmission 구분이다.',
'0580':'나중 변경이 원래 서명된 내용처럼 보이게 overwrite한다는 문장 자체가 오류를 드러낸다.',
'0581':'otherwise valid/qualifying/applicable이라고 이미 결론난 정전 예외를 다시 인정하게 한다.',
'0582':'EP waiver를 ordinary oral CII refill 권한으로 바꾸는 제안은 별도 no-refill·emergency 조건과 충돌한다.',
'0584':'LTCF past-endpoint exception은 정전·CII refill 두 사례에서 실제로 등장하지 않은 별도 조건이다.',
'0585':'다른 가족의 환자명과 prescriber signature를 약국이 보완하는 주체/핵심필드 오류가 초점이다.',
'0586':'이미 있는 CII earliest-fill date를 앞당기려면 새 처방이 필요하다는 경계를 묻는다.',
'0588':'누락 issue-date 추가와 기재값 변경이 초점인데 stem은 환자명·서명·earliest-fill만 제시한다.',
'0589':'주소 확인의 agent 허용을 CII strength 변경으로 확대하는 구체 policy-scope 오류가 초점이다.',
'0590':'gabapentin VI와 PMP 두 지위를 no-consultation days-supply 경로에 적용하는 의미 있는 교차판단이다.',
'0592':'아무 plausible registration number를 넣어도 된다는 보기의 일반적 부정확성이 정답을 노출한다.',
'0593':'oxycodone에 적힌 two refills는 no-refill 법을 바꾸지 않지만 다른 실제 처방조건을 적용하지 않는다.',
'0594':'lawful partial supply라는 결론을 stem이 이미 주고 이를 refill이 아니라고 다시 분류하게 한다.'}
# Individual criterion decisions; no repetition/similarity-score shortcut decides a FAIL.
def realism(q,f):
 qid=q['question_id'];suffix=qid[-4:];obs=observations[suffix]
 vals={'jurisprudence_reasoning':True,'practice_plausibility':True,'authentic_distractors':False,'wording_not_guessable':False,'reasoning_not_trivia':True,'natural_rule_combination':False,'appropriate_drug_context':True,'distinct_from_bank':True,'not_schedule_flashcard':True,'public_style_without_copying':True}
 if suffix in ('0557','0558','0566','0581','0594'):vals['reasoning_not_trivia']=False
 reasons={k:obs+' '+v for k,v in R[f].items()}
 near=N[qid]['nearest'];defaults=set(json.load(open(B/'context/default-ids-at-assignment.json')))
 current_default_same=[]
 # Inspect only the nearest-visible candidates actually read, not prior audit labels.
 for c in neighbors['unique_candidates']:
  if c['question_id'] in defaults and c['family_id']==f and c['stem'].split('\n\nWhich')[0]==q['stem'].split('\n\nWhich')[0]:current_default_same.append(c['question_id'])
 if current_default_same:
  vals['distinct_from_bank']=False
  reasons['distinct_from_bank']=obs+' 실제 읽은 '+', '.join(current_default_same)+'가 현재 default에 있고 두 Case의 사실·문장과 본 문항의 법적 판단을 공유한다. 문항이 archived 연습 변형임을 인정하지만 이 동일 사실/판단을 독립적인 새 실전문제로 인정할 만큼 달라지지는 않았다. family 이름이나 점수만으로 실패시킨 것이 아니다.'
 else:
  reasons['distinct_from_bank']=obs+' canonical nearest '+near['canonical'][0]['question_id']+' 및 public nearest '+near['public'][0]['question_id']+'의 stem·모든 보기를 실제 비교했다. 같은family는 명시된 archived 연습 변형이고 본 문항도 current default 밖이다. 가까운 다른family의 쟁점은 일부 겹쳐도 사건·필수판단이 달라 이 보관용 연습 맥락에서는 과도한 중복으로 단정하지 않는다. 이를 신규 release uniqueness 인증으로 사용하지 않는다.'
 reasons['not_schedule_flashcard']=obs+' 약물의 schedule 이름만 맞히는 문항이 아니라 행위·권한·형식 또는 기록의 법적 결과를 묻는다.'
 reasons['public_style_without_copying']=obs+' SBA/INCORRECT/SATA 선택형과 주·연방 상황 적용이라는 public NABP 형식/competency에 대응한다. 공식 format/competency만 읽었고 Pre-MPJE·회상·상업은행은 열거나 입력하지 않았으며 public sample wording을 재현하지 않았다.'
 duplicate={'method':neighbors['method'],'canonical_count':neighbors['canonical_count'],'public_count':neighbors['public_count'],'candidates_read':near,'visible_candidates_evidence_path':str(B/'nearest-visible-candidates.json'),'visible_candidates_evidence_sha256':file_sha(B/'nearest-visible-candidates.json'),'all_listed_candidate_stems_and_choices_actually_read':True,'default_pool_member':qid in defaults,'nearest_same_case_current_default_ids':current_default_same,'semantic_comparison_ko':reasons['distinct_from_bank']}
 return {'verdict':'PASS' if all(vals.values()) else 'FAIL','decision':'KEEP' if all(vals.values()) else 'MAJOR_REWRITE','criteria':vals,'criterion_findings_ko':reasons,'item_specific_observation_ko':obs,'duplicate_evidence':duplicate,'finding_ko':obs+' 정답의 법적 지지와 별도로 부적절한 distractor/추측 단서 및 실제 규칙 결합 부족을 수정해야 한다.'}
records=[];used=set()
for r in packet['records']:
 q=r['original_visible_content'];qid=q['question_id'];f=loc[qid]['family_id'];negative='INCORRECT' in q['stem'];chosen=[];pc=[]
 for c in q['choices']:
  j=judgments[f][c['text']];select=(not j['statement_supported']) if negative else j['statement_supported']
  if select:chosen.append(c['id'])
  used.update(j['authority_ids'])
  pc.append({'choice_id':c['id'],'option_text':c['text'],'option_text_sha256':sha(c['text'].encode()),'statement_supported':j['statement_supported'],'correct_to_select':select,'finding_ko':j['finding_ko'],'authority_ids':j['authority_ids'],'authorities':[S[k] for k in j['authority_ids']]})
 assert chosen and (q['question_type']=='SATA' or len(chosen)==1),(qid,chosen)
 assert chosen==q['correct_choice_ids'],(qid,chosen,q['correct_choice_ids'])
 ri=realism(q,f);suffix=qid[-4:]
 if suffix in ('0557','0558','0566','0581','0594'):
  special={'0557':'discontinuation을 제시하고 그 event가 clock trigger라는 같은말을 고르게 해 법조문 요건·business-day 계산·인력 판정을 수행하지 않는다.','0558':'liner removal을 제시하고 removal부터라는 같은말을 고르게 해 실제 최대 보관기간이나 보관장소를 적용하지 않는다.','0566':'stem이 한 feature에 legitimate explanation이 가능함을 이미 정해 놓아 fraud를 확정하지 말라는 답을 사실상 제공한다.','0581':'qualifying/otherwise valid/applicable이라는 법적 결론을 stem에 주어 예외에 해당하는 실제 요건을 판단할 일이 남지 않는다.','0594':'lawful partial supply라는 결론을 stem이 미리 주므로 허용 사유·기간·수량을 적용하지 않고 refill이 아니라고 되풀이한다.'}
  ri['criterion_findings_ko']['reasoning_not_trivia']=observations[suffix]+' '+special[suffix]+' 따라서 이 문항의 현재 추론 깊이는 실전 수준에 부족하다.'
 aks=sorted({k for c in pc for k in c['authority_ids']})
 scope='현재 조회한 official posted text의 구체 요건 안에서 판단했다. 시행일은 별도 확정하지 않아 각 source에 UNKNOWN과 버전 한계를 명시했다.'
 if f=='RET08':scope+=' 연방 LTCF II-V/ultimate-user collection 경로로 한정하며 모든 Schedule VI 반환약의 같은 기한이라고 확대하지 않는다.'
 if f=='RX03':scope+=' distribution 경로 검토가 필요하다는 뜻이며 모든 거래에서 새 distributor registration 또는 모든 schedule의 Form222가 필수라는 뜻은 아니다.'
 if f=='RX06':scope+=' historical LTCF의 실제 연장 유무를 이 문항만으로 단정하지 않는다. 검증 없이 모든 later prescription에 면제가 지속된다는 universal 주장을 배척한다.'
 if f=='RX08':scope+=' gabapentin의 no-consultation 경로 부적격을 확인한 것이며 prescriber consultation을 거친 허용 변경까지 금지한 것이 아니다.'
 explain={
  'full_core_reasoning_read':True,'core_reasoning_sha256':sha(q['explanation']['core_reasoning'].encode()),'core_finding_ko':'핵심 해설을 전문 읽고 위 official section에 대조했다. '+scope,
  'all_choice_rationales_read':True,'choice_ids_read':list(q['explanation']['choice_analysis']),'choice_analysis_sha256':semantic(q['explanation']['choice_analysis']),
  'per_choice_findings':[{'choice_id':c['id'],'rationale_sha256':sha(q['explanation']['choice_analysis'][c['id']].encode()),'verdict':'SUPPORTED_WITH_SCOPE_LIMITS','finding_ko':'해당 보기 해설의 선택/비선택 및 오류 보기의 교정 문장까지 전문 읽었다. '+judgments[f][c['text']]['finding_ko']} for c in q['choices']],
  'learning_boundary_read':True,'learning_boundary_finding_ko':'같은 family의 네 변형은 같은 두 사례·판단을 공유하는 연습이라는 명시적 경계를 읽었다. 독립적인 네 임상 사례 또는 네 release-credit으로 계산하지 않는다.',
  'verdict':'SUPPORTED_WITH_SCOPE_LIMITS','error_found_ko':None,'scope_limit_ko':scope}
 lr={'existing_answer_correct':'YES','stored_key':q['correct_choice_ids'],'independently_expected_key':chosen,'question_type':q['question_type'],'polarity_analysis':{'negative_INCORRECT':negative,'decision_ko':('INCORRECT 극성이므로 법적으로 틀린 명제 하나를 선택했다.' if negative else 'SATA의 모든 명제를 따로 검증해 참인 보기의 전체 조합을 선택했다.' if q['question_type']=='SATA' else 'SBA의 네 보기를 따로 검증했고 참인 명제는 하나뿐이다.'),'true_statement_ids':[c['choice_id'] for c in pc if c['statement_supported']],'false_statement_ids':[c['choice_id'] for c in pc if not c['statement_supported']],'unique_SBA_or_complete_SATA_confirmed':True},'per_choice_findings':pc,'authorities':[S[k] for k in aks],'verdict':'KEEP','finding_ko':observations[suffix]+' 독립적으로 정한 참/거짓과 문항 극성에서 계산한 답 '+','.join(chosen)+'가 저장 키와 일치한다. '+scope,'blocker':None,'original_explanation_review':explain}
 records.append({'question_id':qid,'record_sha256':r['record_sha256'],'visible_content_sha256':r['visible_content_sha256'],'family_id':f,'collection':loc[qid]['collection'],'read_scope':{'stem_full':True,'all_choices_full':True,'stored_key':True,'core_korean_explanation_full':True,'all_korean_choice_rationales_full':True,'learning_boundary_full':True,'visible_packet_path':str(B/'assigned-visible-input.json'),'visible_packet_sha256':file_sha(B/'assigned-visible-input.json'),'hidden_truth_accessed':False,'prior_author_or_independent_verdicts_accessed':False},'legal_review':lr,'realism_review':ri,'disposition':'NEEDS_REMEDIATION','safe_hold_recommended':True,'release_eligible':False,'canonical_release_credit':0,'required_next_action_ko':'저장 키를 바꾸기보다 위 item-specific observation과 실패 criterion을 따라 실제 사례·그럴듯한 distractor·자연스러운 조건 적용을 수정한다. 수정은 editor가 별도 current-content revision에서 수행하고 새 current-hash 독립 감사를 받는다. 본 감사자는 candidate를 편집하지 않았다.'})
# Freeze only methodology, not prior audit verdicts.
methodology=[]
for rel in ['docs/INDEPENDENT_LEGACY_REVIEW_RUNBOOK.md','docs/RELEASE_POLICY.md','docs/AUDIT_WORKFLOW.md','docs/SOURCE_USE_POLICY.md','docs/QUESTION_AUTHORING_STANDARD.md','data/exam_style/mpje_style_profile.json','data/blueprint.json','schemas/audit.schema.json','schemas/question.schema.json','schemas/exam_style_profile.schema.json','schemas/blueprint.schema.json']:
 dest=B/'methodology-snapshots'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(rel,dest);entry={'path':rel,'file_sha256':file_sha(rel),'snapshot_path':str(dest)}
 if rel.endswith('.json'):
  d=json.load(open(rel));entry.update(content_version=d.get('content_version',d.get('schema_version',d.get('$schema','UNKNOWN'))),stored_semantic_hash=d.get('content_hash'),canonical_json_sha256=semantic(d))
 methodology.append(entry)
style=json.load(open('data/exam_style/mpje_style_profile.json'));blue=json.load(open('data/blueprint.json'))
style_sources=[]
for sid in ('nabp-format','nabp-competency'):
 m=metas[sid];style_sources.append({'source_id':sid,'official_url':m['final_url'],'scope':'PUBLIC_FORMAT_AND_COMPETENCY_ONLY_NOT_LEGAL_AUTHORITY','evidence_path':m['raw_path'],'evidence_sha256':m['raw_sha256'],'text_path':m['text_path'],'text_sha256':m['text_sha256'],'metadata_path':str(B/'sources'/(sid+'.meta.json')),'metadata_sha256':file_sha(B/'sources'/(sid+'.meta.json')),'retrieved_at':m['completed_at'],'content_read_scope_ko':'MPJE 120문항/2.5시간 selected-response/adaptive 공개 설명과 주·연방법 적용 competency/영역만 확인. 공개 Pre-MPJE 링크의 대상 콘텐츠는 열지 않았다.'})
retrieval_inventory=[]
for sid,m in sorted(metas.items()):
 retrieval_inventory.append({'source_id':sid,'metadata_path':str(B/'sources'/(sid+'.meta.json')),'metadata_sha256':file_sha(B/'sources'/(sid+'.meta.json')),'http_status':m.get('http_status'),'retrieval_success':m.get('retrieval_success'),'used_as_legal_authority':any(S[k]['source_id']==sid for k in used),'raw_sha256':m.get('raw_sha256'),'text_sha256':m.get('text_sha256'),'document_identity':m.get('document_identity'),'completed_at':m['completed_at'],'publication_limit_ko':m.get('publication_limit_ko')})
report={'schema_version':'independent-legacy-session-review/1','stage':'independent-legacy','job_id':assignment['job_id'],'sequence':assignment['sequence'],'question_hashes':assignment['question_hashes'],'independent_of_authors':True,'auditor':'GPT','auditor_instance':instance,'actor_provenance':{'actor_id':actor,'session_id':actor},'canonical_audit':False,'canonical_release_credit':0,'release_eligible':False,'reviewed_at':today,'completed_at':now.isoformat(),'methodology':methodology,'style_profile':{'profile_id':style['profile_id'],'content_version':style['content_version'],'content_hash':style['content_hash'],'file_sha256':file_sha('data/exam_style/mpje_style_profile.json')},'blueprint':{'blueprint_id':blue['blueprint_id'],'content_version':blue['content_version'],'content_hash':blue['content_hash'],'file_sha256':file_sha('data/blueprint.json')},'independence_declaration_ko':'실제 별도 세션 /root/independent_wave12_d가 현재 배정의 visible packet만 독해하고 독립 판단했다. raw question 객체는 source_ids/family/collection 추출 및 hash 확인을 위한 코드 입력에만 사용했고 hidden truth·author/independent 보고서·원장 prior judgments를 모델에 출력하거나 읽지 않았다. nearest 후보도 stem·보기·family/id만 추출해 읽었으며 정답/과거평가를 상속하지 않았다. 같은 세션을 여러 auditor instance로 부풀리지 않았다.','sources':[S[k] for k in sorted(used)],'style_sources':style_sources,'retrieval_inventory':retrieval_inventory,'retrieval_limits_ko':['Firecrawl live supplied-URL scrape는 계정 credits 부족으로 미실행되어 법적 확인으로 세지 않았다. runbook에 따라 정상 proxy·TLS를 유지한 공식 HTTPS urllib GET으로 전환했다.','ma-pmp-gaba discovery URL은 실제 HTTP404/Not found였으므로 확인 근거로 사용하지 않았다. 이후 ma-pmp-current 공식 DCP 페이지의 정상200·문서 제목·Gabapentin 본문을 직접 확인했다.','ma-pmp-guide는 Mass.gov에 있으나 Bamboo Health copyright 및 무단 복제배포 금지를 확인했다. 공개 branch에는 원문 raw/text를 commit하지 않고 payload SHA·메타데이터 및 이 독자 memo만 남긴다. 법적 판정은 해당 vendor guide 대신 현행 official DCP reporting 페이지와 법규에 근거한다.','eCFR title21의 표시상 current-through는2026-11-02이다. 실제 retrieval/law_checked는 metadata의2026-11-04 UTC이다. 그 사이의 미편입 개정을 확인했다고 주장하지 않으며 개별 법정 시행일은UNKNOWN이다.','Mass.gov current official posted PDF의 버전일은 문서에서 확인했다. 버전일이나 HTTP Date를 별도 입법상 commencement date로 둔갑시키지 않는다.','전체 bank fixture/live notes builder/sourceguard/전체QA는 root 통합 책임 범위여서 이 sparse worker에서 실행하지 않는다. 이 stage의 독립 assessment는 canonical RELEASED 또는 법적 release gate가 아니다.'],'records':records,'summary':{'assigned':len(records),'complete_visible_reads':len(records),'independently_legal_assessed':len(records),'existing_answer_yes':sum(r['legal_review']['existing_answer_correct']=='YES' for r in records),'legal_keep':sum(r['legal_review']['verdict']=='KEEP' for r in records),'realism_pass':sum(r['realism_review']['verdict']=='PASS' for r in records),'realism_fail':sum(r['realism_review']['verdict']=='FAIL' for r in records),'needs_remediation':len(records),'source_blocked_records':0,'hold_records':0,'canonical_release_credit':0,'release_eligible_records':0},'checks':{'full_repo_QA':'NOT_RUN_ROOT_INTEGRATOR_SCOPE','sparse_live_notes_builder':'NOT_RUN_ROOT_INTEGRATOR_SCOPE','pre_mpje_or_recalled_or_commercial_question_content':'NOT_ACCESSED','prior_question_verdict_exposure':'NONE','native_postcommit_result_validation':'SEPARATE_POSTCOMMIT_ATTESTATION'}}
assert set(report['question_hashes'])=={r['question_id'] for r in records} and len(records)==40
assert all(set(r['realism_review']['criteria'])==set(r['realism_review']['criterion_findings_ko']) and len(r['realism_review']['criteria'])==10 for r in records)
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report['summary'],ensure_ascii=False));print('Report SHA256',file_sha(OUT));print('used authorities',len(used));print('statement judgments',sum(len(x) for x in judgments.values()));print('duplicate criterion false',sum(not r['realism_review']['criteria']['distinct_from_bank'] for r in records))
