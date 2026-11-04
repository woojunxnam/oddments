from pathlib import Path
from datetime import datetime, timezone
import json, hashlib

B=Path('reports/full-corpus-review/independent-notes/wave10-followup-d-evidence')
P=Path('reports/full-corpus-review/independent-notes/wave10-followup-d-review.json')
J=json.load(open('/tmp/independent-notes5-d-assignment.json'))
V=json.load(open(B/'assigned-visible-input.json'))['records']
Q=json.load(open(B/'related-practice-visible-input.json'))['records']
M=json.load(open(B/'assessment-memos.json'))
NOW=datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

SCOPES={
 'cmr9':('247 CMR 9.01(16),(21);9.04(1),(4);9.15(1);9.16(1),(7)–(8);9.17(1)–(3);9.18(1)–(10);9.19(11)', 'Massachusetts Register #1536, 2024-12-06의 공개 현행 compilation. 개별 원시 효력일은 이 PDF만으로 모두 특정하지 못함.'),
 'policy2018-01':('Policy 2018-01 II–IV, pp.1–3','Adopted 2018-03-01; revised 2019-08-01 and 2024-01-11. 별도 시행 유예는 문서에서 확인되지 않음.'),
 'hipaa164-530':('45 CFR 164.530(c), (j)','현재 eCFR 수록 본문. 이 조항의 최초 효력일은 이번 검토에서 별도 Federal Register 이력으로 확정하지 못함.'),
 'cmr15':('247 CMR 15.02–15.04, pp.73–74','공개 compilation: Mass. Register #1536, 2024-12-06. 개별 원시 효력일은 미확정.'),
 'cmr700':('105 CMR 700.012(A)(1)–(2)','Mass.gov 현행 공개 compilation. 해당 paragraph의 개별 시행일은 이 PDF만으로 미확정. PMP reporting 범위 비교에만 사용.'),
 'cfr208':('21 CFR 208.1;208.3;208.20;208.24;208.26','현재 eCFR 본문. Part source 63 FR 66396 (1998-12-01); 각 조항의 최초 효력일은 별도 확정하지 못함.'),
 'cfr310-501':('21 CFR 310.501(a),(b)(1)–(2)','현재 eCFR 본문; source note 54 FR 22587 (1989-05-25), amendment 74 FR 13113 (2009-03-26). 최초 효력일 별도 미확정.'),
 'cfr310-515':('21 CFR 310.515(a),(b)(1)–(3),(e)','현재 eCFR 본문. 개별 조항 최초 효력일은 이번 검토에서 별도 확정하지 못함.'),
 'cfr456-705':('42 CFR 456.705(a)–(d)','현재 eCFR 본문; source 57 FR 49408 (1992-11-02), amended 59 FR 48824 (1994-09-23). 개별 최초 효력일 미확정.'),
 'fda-medicines':('Learn About Your Medicines: patient labeling descriptions','FDA page content current 2018-01-08. 문서 종류 설명용이며 제품별 현행 REMS 존재 증거로 사용하지 않음.'),
 'fda-medication-guides':('Patient Labeling Resources: Types of patient labeling; Medication Guides; Patient Package Inserts','요청 URL은 FDA 현행 Patient Labeling Resources 페이지로 redirect됨. CMI/MG 구분의 실제 공개 본문을 읽었으며 개별 규정 효력일을 페이지 날짜로 대체하지 않음.'),
 'cdc-vis':('About VISs: What is a VIS?; VISs are required by law; Ways to give a VIS; documentation','CDC 2024-08-02 공개 페이지. 적용 백신별 VIS edition/effective requirement는 해당 백신 자료에서 별도 확인해야 하며 이 검토는 문서 종류와 제공 시점 범위.'),
 'fda-rems':('Risk Evaluation and Mitigation Strategies: introductory definition','FDA content current 2025-05-20; 과거 사례의 모든 현재 제품별 조건을 이 overview만으로 확정하지 않음.'),
 'fda-rems-components':("What's in a REMS?: Types of REMS Requirements; Communicating to Patients; Required Activities; Current REMS", 'FDA overview content current 2018-01-26. 일반 구조 설명과 개별 현행 program document를 구분함.'),
 'fda-rems-roles':('Roles of Different Participants: opening; prescriber roles; monitoring; supply restrictions','FDA 공개 role overview. 제품별 조건은 변경될 수 있으므로 이 일반 자료를 개별 최신 enrollment gate로 사용하지 않음. 최초 효력일 해당 없음.'),
 'fda-clozapine':('Drug Safety Communication: What is FDA announcing?; What should health care professionals do?; patient information','REMS removal effective 2025-06-13; notice 2025-08-27; current FDA page 2026-04-03. Notice date와 효력일을 분리함.'),
 'fda-mifepristone':('Questions and Answers: REMS requirements; pharmacy certification; January 2023 modification; OTC; Litigation and Other Legal Issues','FDA content current 2026-04-08. 2023-01-03 modified REMS를 설명하며 safety study가 장래 변경을 검토할 수 있다고 하지만 현재 변경으로 단정하지 않음.'),
 'fda-mifepristone-rems':('Mifepristone 200 mg shared-system REMS I; II.A.1(a)–(c); II.A.2(a), pp.1–4','Initial shared REMS 2019-04; most recent modification 2023-01 (FDA Q&A: 2023-01-03). Reference ID 5103833. 구체 숫자 record-retention 기간은 확인되지 않음.'),
 'policy2023-05':('Policy 2023-05 pp.1–2: supply, valid-prescription timely-access alternatives, refusal','Effective date 2023-03-22, 문서 양 페이지에 명시.'),
 'cfr1306-04':('21 CFR 1306.04(a)','현재 eCFR 본문; timeline에 2026-07-09/2026-06-09 변경 이력이 보이나 이번 검토는 (a) legitimate purpose/corresponding responsibility에 한정. 최초 효력일 별도 미확정.'),
 'src-183e44eb17e3':('SPRAVATO Prescribing Information 2.1;5.5','DailyMed 현행 label의 supervision·monitoring·certified setting/pharmacy route를 읽음. Label revision과 REMS 자체의 최초 시행일은 동일 개념이 아니며 최초 시행일 미확정.'),
 'src-cfe1b43dedfd':('SUBLOCADE Prescribing Information 2.6;5.2','DailyMed 현행 label의 certified pharmacy/setting 및 direct-to-healthcare-provider, no-patient-dispensing 조건을 읽음. 최초 REMS 시행일 별도 미확정.'),
 'src-21b44f50aa9a':('BRIXADI Prescribing Information 2.1;3','DailyMed 현행 label의 weekly/monthly formulations 구분을 읽음. 2024 FDA PDF보다 현행 label을 우선하며 개별 label 최초 효력일 미확정.'),
 'src-fbe5bf39e310':('BUTRANS Prescribing Information 5.5','DailyMed 현행 pain-patch Opioid Analgesic REMS 교육/안내 구조를 읽음. Depot-injection certification과 동일한 것으로 단정하지 않음. 최초 시행일 미확정.'),
 'src-720ba645b994':('BELBUCA Prescribing Information 5.5','DailyMed 현행 buccal-film Opioid Analgesic REMS 교육/안내 구조를 읽음. Depot-injection REMS와 별도임. 최초 시행일 미확정.'),
 'src-6e55d86582d8':('TIRF Medicines: discontinuation notice; About TIRF; modified REMS requirements','FDA 공개 현행 notice: marketing discontinuation 후 신규 enrollment 중단, 기존 supply 치료 및 approval 존속 중 REMS 존속. Transdermal patch로 TIRF 조건을 복사하지 않는 구분에만 사용.')
}
UNUSED={'src-d2938ae709e7','src-3fa760b2f2a5','src-3c3ba8951204'}
FAILED={'usc355-1','usc355-1-govinfo'}
sources={}
for f in sorted(B.glob('*-retrieval.json')):
 m=json.load(open(f));sid=m['source_id'];good=sid in SCOPES
 m.update(document_identity_confirmed=good, legal_payload_confirmed=good, read_at=NOW if good else None,
   actual_read_scope=SCOPES[sid][0] if good else ('실패: 404 또는 200 Page Not Found; 법적 증거 아님' if sid in FAILED else 'Locator 확보 후 제품명이 배정 명제/실제 보기와 무관함을 확인; 전문 미독, 판정 근거 아님'),
   version_or_effective_date_status=SCOPES[sid][1] if good else '판정 근거로 사용하지 않음')
 save(f,m)
 memo=B/(sid+'-read-memo.json');save(memo,{'source_id':sid,'official_url':m['official_url'],'final_url':m['final_url'],'read_at':m['read_at'],'scope':m['actual_read_scope'],'version_or_effective_date_status':m['version_or_effective_date_status'],'legal_evidence_usable':good,'raw_path':m['raw_path'],'raw_sha256':m['raw_sha256'],'text_path':m['text_evidence_path'],'text_sha256':m['text_sha256'],'limitation':'문서 전체 모든 조문에 대한 독립 판정이 아니라 명시한 실제 읽은 관련 section의 증거이다.'})
 sources[sid]={**m,'metadata_path':str(f),'metadata_sha256':sha(f),'memo_path':str(memo),'memo_sha256':sha(memo),'source_type':'PUBLIC_OFFICIAL','legal_evidence_usable':good}

def authority(sid,section):
 s=sources[sid];assert s['legal_evidence_usable'] and s['http_status']==200
 return {'source_id':sid,'source_type':'PUBLIC_OFFICIAL','official_url':s['official_url'],'citation_url':s['final_url'],'exact_section':section,'law_checked_date':NOW[:10],'version_or_effective_date_status':s['version_or_effective_date_status'],'retrieved_at':s['retrieved_at'],'read_at':s['read_at'],'timezone':'Etc/UTC','http_status':s['http_status'],'evidence_path':s['raw_path'],'evidence_sha256':s['raw_sha256'],'text_evidence_path':s['text_evidence_path'],'text_evidence_sha256':s['text_sha256'],'retrieval_metadata_path':s['metadata_path'],'retrieval_metadata_sha256':s['metadata_sha256'],'read_memo_path':s['memo_path'],'read_memo_sha256':s['memo_sha256']}

EXTRAS={
 ('w3-b-2',13):[('hipaa164-530','45 CFR 164.530(c)')],
 ('w3-b-4',14):[('cfr1306-04','21 CFR 1306.04(a)')],
 ('w3-b-4',15):[('cmr700','105 CMR 700.012(A)(1)–(2)')],
 ('w3-b-4',16):[('cmr9','247 CMR 9.15(1);9.04(1)')],
 ('w3-b-5',9):[('fda-mifepristone-rems','II.A.2(a)(iv)(2)(i)–(k)')],
 ('w3-b-5',10):[('cmr700','105 CMR 700.012(A)(1)–(2)')],
 ('w3-b-5',11):[('cmr15','247 CMR 15.04'),('hipaa164-530','45 CFR 164.530(j)')],
 ('w3-b-6',8):[('cfr310-515','21 CFR 310.515(a)–(b),(e)')],
 ('w3-b-7',10):[('cfr310-515','21 CFR 310.515(b)(3)')],
 ('w3-b-7',11):[('cfr310-501','21 CFR 310.501(b)(2)'),('cfr208','21 CFR 208.1(a)')],
 ('w6-a-10',18):[('cfr208','21 CFR 208.24(e)')],
 ('w6-a-10',19):[('cmr9','247 CMR 9.18(1)')],
 ('w3-b-8',4):[('fda-clozapine','Drug Safety Communication: REMS removal and continuing labeling')],
 ('w3-b-8',8):[('cmr9','247 CMR 9.01(21)')],
 ('w3-b-11',21):[('fda-mifepristone-rems','II.A.2(a)'),('policy2023-05','pp.1–2 supply/timely access')],
 ('w3-b-11',22):[('fda-mifepristone-rems','I;II.A.1–2')]
}
PRIMARY_SECTIONS={('w3-b-4',15):'247 CMR 9.17(1)(f)–(g)',('w3-b-4',16):'21 CFR 1306.04(a)',('w3-b-5',9):'247 CMR 9.01(21);9.16;9.18',('w3-b-5',10):'247 CMR 15.02;15.04(2)–(4)',('w3-b-5',11):'247 CMR 9.16(1),(7);9.17(2)',('w3-b-6',8):'21 CFR 310.501(a)–(b)',('w3-b-7',10):'21 CFR 310.501(b)(2)',('w3-b-7',11):'21 CFR 310.515(b)(3)',('w6-a-10',18):'247 CMR 9.17;9.18(1)–(5)',('w6-a-10',19):'42 CFR 456.705(c)(2)(ii)–(iii)',('w3-b-8',8):'Mifepristone REMS II.A.2(a)(i)–(iv)',('w3-b-11',21):'247 CMR 9.01(21)',('w3-b-11',22):'Policy 2023-05 pp.1–2 supply/timely access'}

# Literal body anchors and manual assertion-to-census mapping. No legal assertion is inferred from a title.
COVER={
 'w3-b-2':[('Drug name·description·indication',list(range(1,10))),('Inhaler, injection, suspension',[10]),('Label의 tsp/mL 또는 unit 표현',[14,15]),('Liquid medication',[11]),('patient language·시각·청각·인지적 필요',[12]),('민감한 diagnosis',[13])],
 'w3-b-3':[('visual·auditory confidentiality',[1]),('stockroom나 prescription dispensing area',[3]),('해당 표지를 게시',[2]),('pharmacy business hours',[4]),('높이 11 inches × 너비 14 inches',[5,6]),('1/2 inch',[7]),('MOR-name sign의 1-inch',[8]),('Inpatient setting',[9]),('hospital discharge prescription, outpatient pickup',[10]),('다른 법의 patient-education',[11])],
 'w3-b-4':[('dispense 또는 deliver하기 전에',[1]),('Over/under-utilization',[2]),('therapeutic duplication',[3]),('drug-disease·drug-drug/food',[4]),('dose·duration',[5]),('allergy',[6]),('abuse/misuse',[7]),('clinically significant changes, age-related contraindications',[8]),('Computer alert가 없다는 사실',[9]),('alert가 있다는 사실',[10]),('중요성을 판단',[11]),('prescriber 또는 patient/agent',[12]),('대응 내용을 기록',[13]),('Prescription authenticity, corresponding responsibility',[14]),('PMP report',[15]),('정확한 tablet',[16])],
 'w3-b-5':[('Confidential patient profile',[1]),('즉시 검색',[2]),('name·contact·DOB/age',[3]),('allergy/adverse reaction',[4]),('조제한 약물·관련 기기',[5]),('pharmacist comments',[6]),("'알레르기 없음'",[7]),('Prescription record, patient profile',[8]),('counseling/refusal record, REMS authorization',[9]),('PMP transmission, CQI record',[10]),('하나의 electronic chart',[11])],
 'w3-b-6':[('FDA가 특정 위험에 대해 승인',[1]),('dispense할 때',[2,6]),('refill을 포함',[3]),('제조사/배포자의 공급 의무',[4,5]),('generic computer leaflet',[7]),('Patient Package Insert',[8]),('Consumer Medication Information',[9]),('Vaccine Information Statement',[10,11]),('현재 REMS에 enrollment나 dispensing authorization',[12]),('REMS가 제거되어도',[13])],
 'w3-b-7':[('각 dispensed package',[1]),('Acute-care hospital 또는 LTCF',[2]),('이후 30일마다',[3]),('Estrogen products',[4]),('bulk package',[5]),('multidose injectable',[6]),('Hospital/LTCF의 first administration',[7,8]),('Estrogen-progestogen oral contraceptives',[9]),('처방의 refill validity',[10]),('모든 medication leaflet',[11])],
 'w6-a-10':[('조제·교부 전 약물치료 검토',[1]),('환자 profile',[2]),('상담 기준이 연결',[3]),('duplication',[4]),('contraindication',[5]),('interaction',[6]),('dose·duration',[7,8]),('allergy',[9]),('abuse/misuse',[10]),('Offer와 실제 counseling',[11]),('수행·거절·기록',[13]),('우편 조제',[14]),('독립적인 DUR',[15]),('현금 환자나 일반 보험 환자',[16]),('Offer to counsel, counseling itself',[17]),('Patient refusal, 단순히 환자를 만나지 못한 경우',[12]),('직원이 먼저 거절',[19]),('Printed information나 Medication Guide',[18])],
 'w3-b-8':[('benefits가 risks를 넘도록',[1]),('Medication Guide, communication plan',[2]),('모든 REMS가 똑같은',[3]),('prescriber·patient·pharmacy certification',[5]),('lab/clinical criteria, dispensing authorization',[6]),('patient information, supply·window',[7]),('shipping·administration restrictions',[8]),('Black box warning',[4]),('현재 버전과 시행일',[9]),('옛 교재',[10])],
 'w3-b-9':[('2025-06-13',[1]),('mandatory REMS enrollment',[2]),('REMS authorization',[3]),('severe neutropenia 위험',[4]),('ANC monitoring',[5]),('REMS 시스템에 특정 값',[6]),('patient counseling',[7]),('적법한 prescription',[8]),('dose·interaction review, patient-specific safety assessment',[9]),('검사나 주의사항 전부 불필요',[10])],
 'w3-b-11':[('certified prescriber',[1]),('patient agreement',[2,3]),('patient information',[4]),('certified pharmacy 또는 적격 prescriber-supervised',[5]),('authorized representative',[6]),('agreement 수령·보존',[7,8,9]),('timely dispensing',[10]),('tracking 가능한 shipping capability',[11]),('in-person dispensing만',[12]),('mail dispensing',[13]),('OTC',[14]),('continuous sufficient supply',[15]),('timely access 책임',[16]),('stock 보충',[17]),('alternative를 prescriber와 협의',[18]),('다른 pharmacy로 transfer',[19]),('mail/central-fill',[20]),('federal REMS certification를 생략',[21]),('접근을 일률적으로 막는',[22])]
}

records=[]
for v in V:
 uid=v['unit_id'];bind=J['unit_bindings'][uid];claims=[]
 assert len(v['claims'])==len(M[uid])
 for n,(c,mm) in enumerate(zip(v['claims'],M[uid]),1):
  sid,section,finding=mm;cid=c['claim_id'];blocked=cid in bind['source_blocked_claim_ids']
  auth=[authority(sid,PRIMARY_SECTIONS.get((uid,n),section))]+[authority(s,x) for s,x in EXTRAS.get((uid,n),[])]
  claims.append({'claim_id':cid,'claim_record_sha256':bind['claim_record_sha256s'][cid],'statement_ko':c['statement_ko'],'read':True,'claim_read_completely':True,'actual_read_completed_at':NOW,'legal_status':'SOURCE_BLOCKED' if blocked else 'KEEP','finding':finding,'blocker':'원 census가 말하는 구체 보존조건 전체의 범위·기간·형식 불특정. 일반 유지 의무는 새 primary로 확인했으나 포괄 명제 전부의 검증으로 확대하지 않는다.' if blocked else None,'prior_author_source_blocked_preserved':blocked,'authorities':auth,'related_question_ids':c.get('related_question_ids',[]),'local_question_audit_credit':0})
 coverage=[]
 for anchor,nums in COVER[uid]:
  assert anchor in v['body'],(uid,anchor)
  coverage.append({'exact_body_phrase':anchor,'census_claim_ids':[v['claims'][n-1]['claim_id'] for n in nums]})
 assert set(n for a,ns in COVER[uid] for n in ns)==set(range(1,len(claims)+1))
 records.append({'unit_id':uid,'title':v['title'],'binding':bind,'body_read_completely':True,'body_read_completed_at':NOW,'body_input_path':str(B/'assigned-visible-input.json'),'body_input_sha256':sha(B/'assigned-visible-input.json'),'completeness':'COMPLETE','omissions':[],'completeness_method':'원문 전체를 bounded reading에서 읽고, 아래 exact phrase별 수치·시점·주체/면허·의무/가능·문서·설정·예외·MA/연방 범위를 저자 census와 수동 대조했다. 외부 법규의 추가 세부사항이 본문 자체에 없다는 사실과 본문에 있지만 census가 빠뜨린 명제를 구별했다. 본문에서 추가 누락 명제는 발견하지 못했다.','body_assertion_coverage':coverage,'claims':claims,'legal_status':'SOURCE_BLOCKED' if any(c['legal_status']=='SOURCE_BLOCKED' for c in claims) else 'KEEP','required_followup':['NOTE-WAVE8-W3-B-11-008의 불특정 보존조건을 구체 대상·기간·형식별 명제로 나눠 새 author census를 만들고 다시 검토할 것. 기존 negative를 제거하지 말 것.'] if uid=='w3-b-11' else (['9.16(8)의 institutional sterile compounding pharmacy 제외를 적용 범위 설명에 덧붙이면 교육적으로 더 명확하다. 이 일반 profile 문장을 모든 면허/setting에 절대 적용하는 데 사용하지 말 것.'] if uid=='w3-b-5' else []),'canonical_audit':False,'canonical_release_credit':0,'question_audit_credit':0})

# Read every question's actual stem/options/stored key/core/all distractors. Literal dictionary only removes exact duplicate display text.
D=json.load(open(B/'mifepristone-practice-lossless-reading.json'))
TRUE_C={1,8,9,12,14,15,17,18,19,20}
CFIND={1:('fda-clozapine','Removed enrollment gate is no longer required.'),2:('fda-clozapine','Label-based ANC monitoring remains.'),3:('src-21b44f50aa9a','Weekly/monthly formulations cannot be assumed interchangeable.'),4:('src-6e55d86582d8','TIRF product scope does not include a transdermal patch.'),5:('fda-rems','Boxed warning alone does not establish enrollment.'),6:('fda-rems-components','A future implementation is not current simply because announced.'),7:('fda-clozapine','Removed enrollment cannot be restored as a prerequisite.'),8:('src-183e44eb17e3','Certified setting, observed administration, monitoring are required.'),9:('src-6e55d86582d8','Product/route distinction is required; note current discontinued marketing/new enrollment limits.'),10:('fda-mifepristone-rems','State access does not remove federal pharmacy certification.'),11:('src-cfe1b43dedfd','The dose must go directly to a healthcare provider, not patient take-home.'),12:('fda-clozapine','Neutropenia risk/PI monitoring remains after REMS removal.'),13:('src-fbe5bf39e310','Pain-patch opioid analgesic REMS differs from depot certification.'),14:('src-720ba645b994','Form/route-specific programs cannot be copied across buprenorphine products.'),15:('fda-rems','Check a current product-specific REMS rather than infer it from warning.'),16:('src-183e44eb17e3','Spravato is not routine take-home administration.'),17:('src-cfe1b43dedfd','Certified direct-to-provider pathway is supported.'),18:('src-21b44f50aa9a','Weekly and monthly BRIXADI are different formulations.'),19:('fda-rems-components','A workflow must use the applicable effective version; no named future iPLEDGE date is asserted.'),20:('fda-mifepristone-rems','Certified pharmacy route still needs certified-prescriber valid prescription.')}
local=[];special={r['question_id']:r for r in D['records']}
NON={
'MA-CASE-0316':('B','fda-clozapine','폐지 enrollment 요구를 제거하고 PI monitoring/DUR를 유지한다. A는 ANC 필요성 부정, C는 폐지 gate 복원, D는 다른 제품의 window를 복사하므로 원 core·전 distractor 구분이 타당하다.'),
'MA-EXP-0425':('C','cmr9','기기 사용법을 환자 상황에 맞게 설명한다. 공개 진단 발설·동일 대본·환자 필요 무시라는 A/B/D를 9.18(5)–(6) 및 confidentiality와 대조했다.'),
'MA-EXP-0429':('B','cmr9','액상약 proper measuring device를 dispense OR recommend한다. Household utensil 강제·시범 배제·무단 dose 변경 보기의 배제를 확인했다.'),
'MA-EXP-0433':('A','cmr9','Stockroom/dispensing area 통과 경로가 위반이다. 병원 전체 면제·특정 시간 상담 배제·auditory privacy 불필요라는 나머지 보기를 9.18(6),(8),(10)과 대조했다.'),
'MA-EXP-0437':('D','cmr9','8×10 rights sign은 최소 11×14에 미달한다. 게시가 offer를 대체하지 않으며 직원 폴더는 적절한 게시가 아니고 MOR 1-inch와 rights 1/2-inch는 다르다는 전 해설을 확인했다.'),
'MA-EXP-0441':('C','cmr9','No-alert가 allergy review 완료 증명은 아니다. 배송 후 DUR·모든 alert 금지·문서화 생략이라는 다른 보기는 9.17(1)–(2)와 맞지 않는다.'),
'MA-EXP-0445':('B','cmr9','Product/count와 therapeutic duplication은 별도다. PMP가 allergy를 완료·profile 검색 불필요·count가 authenticity 증명이라는 다른 보기의 배제가 타당하다.'),
'MA-EXP-0449':('A','cmr9','Blank allergy와 확인된 음성 병력은 다르다. REMS가 모든 기록 대체·comments 제거·미검토 profile 허용이라는 나머지 해설도 원문 전체와 대조했다.'),
'MA-EXP-0453':('D','fda-medication-guides','Generic CMI를 approved MG와 동일시할 수 없다. MG=등록 증명·VIS=일반 leaflet·refill Guide 불요라는 다른 보기는 실제 문서별 trigger와 맞지 않는다.'),
'MA-EXP-0457':('C','cfr310-501','Oral contraceptive each-package PPI가 맞다. Estrogen 경로 동일시·30일 refill validity·institution first/30-day 의무 부정은 310.501/515와 맞지 않는다.'),
'MA-EXP-0461':('B','cmr9','Cash/private payment는 MA 상담을 자동 면제하지 않는다. Offer·actual counsel·refusal의 동일시, leaflet 또는 DUR로 모든 의무 완료라는 보기를 배제한 원 해설이 타당하다.'),
'MA-EXP-0462':('C','cfr456-705','Mail special situations와 toll-free 접근 요건 때문에 인쇄물만으로 모든 counseling 기준이 끝나지 않는다. 나머지 보기의 offer/refusal 혼동·DUR 자동면제·cash 면제를 배제했다.'),
'MA-EXP-0463':('ABCD','cfr456-705','SATA A/B/C/D는 각각 MA payment-independent duty, offer/counsel/refusal 구분, mail의 별도 접근 조건, DUR와 정보/상담 구분으로 모두 지지된다. 저장 키 네 개의 정확 조합과 전 해설을 확인했다.'),
'MA-EXP-0464':('D','cfr456-705','INCORRECT를 묻는다. D의 DUR로 모든 patient information 면제는 거짓이고 다른 세 구분은 참이다. Polarity와 저장 키를 함께 확인했다.'),
'MA-REV-0050':('D','cmr9','MA cash outpatient new prescription은 DUR 이전 수행이며 무경고가 면제는 아니다. Prescriber request·첫 refill까지 유예·product label로 clinical review 대체라는 보기를 배제했다.'),
'MA-REV-0070':('C','fda-rems','Boxed warning alone으로 enrollment를 추론하지 않는다. 무조건 enrollment·DEA waiver 또는 warning이 있으면 MG 생략이라는 다른 보기는 지지되지 않는다.')}
NONOPT={
'MA-CASE-0316':['FDA는 ANC clinical monitoring 지속을 권고하므로 removal과 검사 불필요는 다르다.','폐지 access gate 제거와 남아 있는 label-based monitoring을 함께 반영한다.','2025-06-13 폐지된 enrollment/authorization 복원은 현행 전제가 아니다.','다른 제품 iPLEDGE window는 clozapine에 자동 적용되지 않는다.'],
'MA-EXP-0425':['공개 대기줄의 큰 소리는 9.18(6)의 auditory privacy를 충족하는 대체 수단이 아니다.','9.18(5)는 필요한 내용을 professional judgment로 정하므로 동일 내용 강제는 틀리다.','9.18(5)(b)–(e)의 실제 투여/사용 설명을 환자 의사소통 필요에 맞춘다.','약국 표준 대본이라는 이유만으로 개별 환자에게 필요한 정보 전달이 증명되지 않는다.'],
'MA-EXP-0429':['Any household utensil의 무조건 적합성은 proper measuring device 기준과 다르다.','9.18(9)의 dispense OR recommend 문언과 일치한다.','9.18(5)(c)는 administration/use 설명을 허용하며 written directions만 인정하는 규칙이 아니다.','Policy 2018-01 III.A(i)/III.B(v)의 directions consultation과 IV 기록 요건은 label rewrite로 사라지지 않는다.'],
'MA-EXP-0433':['Stockroom/dispensing area 통과를 요구하는 사례 경로는 9.18(6)에 맞지 않는다.','9.18(10)은 inpatient practice의 특정 제외이며 hospital에서 얻는 모든 처방 면제가 아니다.','9.18(8)은 business-open hours 전 시간 상담 이용 가능을 요구한다.','표지 자체로 9.18(6)의 confidential auditory counseling 요건이 충족되지는 않는다.'],
'MA-EXP-0437':['9.18(7)의 sign과 9.18(1)의 offer는 별도 의무다.','직원 전용 폴더는 9.18(7)의 conspicuous/adjacent 게시와 다르다.','9.18(7)의 1/2 inch와 9.19(11)의 MOR 1 inch는 동일하지 않다.','사례의 8×10은 높이11×폭14 minimum에 미달한다.'],
'MA-EXP-0441':['9.17(1)은 dispensing/delivery 전을 요구하므로 사후만 review는 늦다.','9.17(2)는 appropriate measures를 요구하며 모든 alert의 일률 금지가 아니다.','9.17(1)(g)의 allergy 검토는 무경고로 대체되지 않는다.','9.17(2)의 measures documentation은 구두 해결 뒤에도 남는다.'],
'MA-EXP-0445':['MassPAT는 9.17(1)의 allergy/directions 검토 완료를 자동 입증하지 않는다.','정확 product/count와 9.17(1)(b)의 duplication 검토는 다르다.','9.16(7)은 dispensing 시 immediate retrieval을 요구한다.','Count의 정확성은 9.15(1)의 legitimate-purpose/authenticity를 입증하지 않는다.'],
'MA-EXP-0449':['Blank allergy field는 missing information이며 확인된 no-allergy와 다르다.','9.01(21)의 REMS 준수는 9.16/9.18 기록·상담을 자동 면제하지 않는다.','9.16(7)(d)는 therapy-relevant comments를 유지하는 profile을 요구한다.','Relevant fields를 고의로 미검토하는 것은 9.16(7)의 reasonable effort로 볼 수 없다.'],
'MA-EXP-0453':['FDA는 모든 MG 중 일부만 REMS에 속한다고 설명하므로 MG가 enrollment를 증명하지 않는다.','VIS는 CDC vaccine benefit/risk 문서로 일반 prescription CMI와 다르다.','208.1(a)는 new AND refill prescriptions를 포함한다.','FDA 미승인 CMI가 승인 required MG의 자동 대체물은 아니다.'],
'MA-EXP-0457':['310.515(e)는 estrogen-progestogen OC를 310.501로 구별하므로 모든 estrogen 동일 경로는 거짓이다.','30일은 institution ongoing-therapy labeling interval이며 refill validity가 아니다.','310.501(a)의 each-package PPI와 일치한다.','310.501(b)(2)/310.515(b)(3)에 first administration 전 및 ongoing every30days가 있다.'],
'MA-EXP-0461':['Offer·actual counseling·refusal는 456.705(c)에서 따로 다룬다.','9.18은 Medicaid payment만을 대상으로 한 문언이 아니다.','456.705(c)(2)(i)의 mail-order toll-free access는 leaflet만으로 충족되지 않는다.','9.17/9.18과 208.24(e)의 별도 의무가 DUR 완료로 소멸하지 않는다.'],
'MA-EXP-0462':['Offer·counseling·refusal는 서로 다른 사건이다.','DUR는 상담·Guide 등 다른 의무의 자동 면제가 아니다.','456.705(c)의 mail special-situation/toll-free 접근 의무 때문에 written information만으로 모두 완료가 아니다.','Massachusetts 9.18의 의무는 cash라는 이유로 자동 사라지지 않는다.'],
'MA-EXP-0463':['9.18은 payment-independent MA duty이다.','456.705(c)는 offer·actual counsel·refusal를 구별한다.','Mail special situations 및 toll-free access는 written material만으로 충족된다고 볼 수 없다.','DUR·patient information·counseling은 별도 trigger를 충족해야 한다.'],
'MA-EXP-0464':['Payment 여부가 MA9.18 자동 제외 사유는 아니다.','Written-only가 모든 mail counseling 조건을 충족했다는 충분 증거는 아니다.','Offer·counseling·refusal의 구별은 456.705(c)에 맞다.','거짓 명제: prospective DUR가 모든 patient-information/counseling duty를 제거하지 않는다. INCORRECT 질문이므로 D를 고른다.'],
'MA-REV-0050':['9.17(1)은 prescriber의 나중 요청을 trigger로 두지 않는다.','New prescription 이전 DUR를 첫 refill까지 미룰 수 없다.','9.04(1)의 final validation과 9.17의 clinical DUR는 다르다.','사례의 outpatient new prescription은 dispensing 이전 DUR 대상이다.'],
'MA-REV-0070':['Warning alone만으로 every refill enrollment record를 만들 의무가 생기지 않는다.','Boxed warning의 존재가 DEA waiver 요건이라는 근거가 아니다.','FDA labeling risk와 operational REMS enrollment는 별도 사실이다.','REMS enrollment가 없어도 208.24(e)의 required MG 전달은 남을 수 있다.']}
NONAUTH={('MA-EXP-0429','D'):('policy2018-01','Policy 2018-01 III.A(i);III.B(v);IV'),('MA-EXP-0453','A'):('fda-rems-components','Communicating to Patients'),('MA-EXP-0453','B'):('cdc-vis','About VISs: definition; timing'),('MA-EXP-0453','C'):('cfr208','21 CFR 208.1(a)'),('MA-EXP-0457','A'):('cfr310-515','21 CFR 310.515(e)'),('MA-EXP-0457','D'):('cfr310-515','21 CFR 310.515(b)(3)'),('MA-EXP-0461','A'):('cfr456-705','42 CFR 456.705(c)(1)–(2)'),('MA-EXP-0461','C'):('cfr456-705','42 CFR 456.705(c)(1),(2)(i)'),('MA-EXP-0462','D'):('cmr9','247 CMR 9.18(1)–(5)'),('MA-EXP-0463','A'):('cmr9','247 CMR 9.18(1)–(5)'),('MA-EXP-0464','A'):('cmr9','247 CMR 9.18(1)–(5)'),('MA-REV-0070','D'):('cfr208','21 CFR 208.24(e)')}
for q in Q:
 qid=q['question_id'];opts=[]
 if qid in special:
  r=special[qid];expected=[]
  for opt,token in r['choices'].items():
   n=int(token[1:]);truth=n in TRUE_C;sid,finding=CFIND[n]
   if truth:expected.append(opt)
   opts.append({'option_id':opt,'supported':truth,'finding':finding,'authorities':[authority(sid,SCOPES[sid][0])],'original_ko_rationale_read':True,'rationale_alignment':'CONSISTENT','exact_text_token':token})
  assert sorted(expected)==sorted(q['correct_choice_ids']),(qid,expected,q['correct_choice_ids'])
  finding='원 stem의 각 option은 서로 별도 work-queue record라는 전제를 읽었다. 모든 option 및 core/개별 해설의 literal text를 lossless dictionary와 질문별 mapping으로 실독하고 제품별 근거에 대조했다. Note scope와 관련된 clozapine/REMS/mifepristone 구분에 모순을 찾지 못했다. 공통 stem·도덕적으로 명백한 업무 오류·반복 permutation은 사실적인 단일 환자 사례와 별도인 연습 변형이라는 한계를 갖는다.'
 else:
  expected,sid,finding=NON[qid];assert sorted(list(expected))==sorted(q['correct_choice_ids'])
  for i,opt in enumerate(q['choices']):
   oid=opt['choice_id'] if 'choice_id' in opt else opt.get('id');asrc,asection=NONAUTH.get((qid,oid),(sid,SCOPES[sid][0]));supported=oid in list(expected)
   if qid=='MA-EXP-0464':supported=not supported
   opts.append({'option_id':oid,'supported':supported,'selected_in_stored_key':oid in list(expected),'finding':NONOPT[qid][i],'authorities':[authority(asrc,asection)],'original_ko_rationale_read':True,'rationale_alignment':'CONSISTENT'})
 local.append({'question_id':qid,'current_record_sha256':q['record_sha256'],'full_stem_read':True,'all_options_read':True,'stored_key_read':True,'ko_core_and_all_distractors_read':True,'read_completed_at':NOW,'input_path':str(B/'related-practice-visible-input.json'),'input_sha256':sha(B/'related-practice-visible-input.json'),'stored_correct_choice_ids':q['correct_choice_ids'],'local_alignment':'CONSISTENT_WITH_REVIEWED_NOTE_CLAIMS','finding':finding,'options':opts,'local_only':True,'whole_key_canonical_audit':False,'canonical_release_credit':0,'question_audit_credit':0})

report={'schema_version':1,'stage':J['stage'],'job_id':J['job_id'],'assignment_sequence':J['sequence'],'assignment_base_commit':J['base_commit'],'assignment_sha256':sha('/tmp/independent-notes5-d-assignment.json'),'actor_provenance':J['actor_provenance'],'auditor':J['auditor'],'auditor_instance':J['auditor_instance'],'independent_of_authors':True,'canonical_audit':False,'canonical_release_credit':0,'question_audit_credit':0,'review_date':NOW[:10],'review_completed_at':NOW,'timezone':'Etc/UTC','language':'ko','scope':'10개 notes 본문 completeness/138 atomic legal claims independent review. Related 52 practice records are local alignment only; canonical release/whole-key/additional question credit 0. Initial D40 question report/commit remains separate.','independence_disclosure':{'stable_actual_instance_continued':True,'new_session_claimed':False,'not_author_or_editor_or_prior_complete_atomic_assessor_of_assigned_units':True,'source_locator_fields_used':['source_id','url','official_url','exact_section','authority','publisher'],'prior_task_incident':'같은 agent의 앞선 D40 단계에서 URL discovery rg가 무관한 author verification_notes 일부를 출력한 일을 root와 당시 보고서에 공개했다. 이번 배정 notes의 hidden truth/타 reviewer 판정은 읽지 않았다. 새 identity로 credit을 우회하지 않는다.','this_task_visible_prior_status':'배정 census의 NOTE-WAVE8-W3-B-11-008 statement 자체 및 assignment source_blocked_claim_ids에 기존 SOURCE_BLOCKED가 명시되어 있어 이를 읽었다. 이는 검토할 author 주장/이력이며 법적 증거로 사용하지 않았고 기존 상태를 보존한다.','affected_new_credit_block':'원 SOURCE_BLOCKED claim008을 KEEP로 승격하지 않음. 본문 author/editor/이전 complete assessment 역할에 해당하지 않음.'},'copyright_boundary':'상용·PreMPJE·회상/보호 시험문항·USP/NABP raw/text를 가져오지 않았다. 저장한 법적 증거는 공식 정부 규정·정책·FDA labeling/REMS·CDC 공개 문서이다. 연관 문제는 이 저장소가 제공한 original practice 입력이다.','source_index_path':str(B/'source-index.json'),'sources':list(sources.values()),'records':records,'related_practice_alignment':local,'counts':{'units':len(records),'claims':sum(len(r['claims']) for r in records),'completeness_complete':len(records),'omissions_found':0,'claim_keep':sum(c['legal_status']=='KEEP' for r in records for c in r['claims']),'claim_source_blocked':sum(c['legal_status']=='SOURCE_BLOCKED' for r in records for c in r['claims']),'unit_keep':sum(r['legal_status']=='KEEP' for r in records),'unit_source_blocked':sum(r['legal_status']=='SOURCE_BLOCKED' for r in records),'related_questions_read':len(local),'new_question_audit_credit':0},'required_next_actions':['Root만 assignment 순서로 submit/integrate한다. 이 산출물을 canonical release로 승격하지 않는다.','w3-b-11의 기존 불특정 보존조건 SOURCE_BLOCKED를 유지한다. 새 primary가 증명하는 일반 forms/dispensing/shipping record 유지와 구체 retention 전체 미확인을 구분한다.','Profile 9.16(8), inpatient counseling 9.18(10), Medicaid 456.703 참조 예외 및 MG 208.26 예외를 제품/setting별 사용 때 유지한다.','미래 제품 변경을 승인일만으로 조기 적용하지 말고 해당 current effective program document를 확인한다.']}
save(B/'source-index.json',{'created_at':NOW,'timezone':'Etc/UTC','sources':sources,'failures_not_legal_evidence':sorted(FAILED),'locator_only_not_used':sorted(UNUSED)})
report['source_index_sha256']=sha(B/'source-index.json')
save(P,report)
print(json.dumps({'report':str(P),'sha256':sha(P),'counts':report['counts']},ensure_ascii=False))
