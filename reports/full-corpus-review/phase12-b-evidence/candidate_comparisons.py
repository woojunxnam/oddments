"""Manual semantic comparison notes from the actually read nearest-visible packet."""
TOPICS={
'MA-Q-0313':'해결한 therapeutic duplication에 대한 prescriber 통화·조치의 문서화 누락',
'MA-Q-0042':'phentermine refill 기간·횟수와 MassPAT 보고',
'MA-Q-0417':'DUR alert를 technician이 독자 해소할 수 있는지와 약사 조치 문서화',
'MA-Q-0163':'controlled prescription red flags와 EPCS 인증·corresponding responsibility',
'MA-Q-0370':'overnight batch 때문에 과거 투약정보를 즉시 검색하지 못하는 전산 시스템',
'MA-Q-0143':'EPT 익명 partner의 profile·label 식별자',
'MA-Q-0416':'community CDTM referral의 known allergy·written consent 누락과 hospital 경로 비교',
'MA-Q-0320':'세 차례 질문 거절과 바쁜 이유로 전혀 질문하지 않은 reasonable effort의 차이',
'MA-Q-0199':'naloxone PMP 제출과 MassPAT profile 표시 차이',
'MA-Q-0109':'2026 clozapine의 폐지된 REMS gate와 임상 monitoring',
'MA-Q-0092':'Medication Guide 수령과 verbal counseling 거절의 별도 요건',
'MA-Q-0403':'환자 대리인 pickup 때 Medication Guide를 나중에 주는 관행',
'MA-Q-0402':'처방자의 Guide 생략 지시에도 환자가 정보를 요청한 예외',
'MA-Q-0095':'이전 contraceptive 처방이 없는 성인의 pharmacist prescribing 적격성',
'MA-Q-0094':'재고 부족 CII partial fill의 72시간 잔량 기한',
'MA-Q-0164':'for pain으로 적힌 methadone과 실제 OUD maintenance 목적의 충돌',
'MA-Q-0014':'환자 요청 Dexedrine partial fill의 발행일 기준 30일 잔량',
'MA-Q-0165':'OUD referral 중 emergency narcotic dispense와 prescription의 차이',
'MA-Q-0283':'최근 dose change가 있는 anticoagulant refill 상담의 중요성',
'MA-Q-0017':'minor Norco의 반복 opiate 처방에도 적용되는 7일 원칙',
'MA-Q-0086':'offer 거절의 기록 위치·무기록 상담 추정과 technician 상담 권한',
'MA-Q-0284':'새 inhaled therapy의 상담 내용',
'MA-Q-0308':'CDTM referral의 indelible pencil 및 전송 이미지 readable/retrievable 조건',
'MA-Q-0305':'CDTM 업무 범위와 독자 진단의 한계',
'MA-Q-0438':'전자 Form222 사본과 CSOS 원본 주문 기록의 별도 요건',
'MA-Q-0030':'unfilled electronic Librium의 2회차 initial EPCS transfer 금지',
'MA-Q-0067':'종이 Form222의 별도 filing·2년 보존',
'MA-Q-0180':'hospital trainee의 ADD stocking schedule 범위',
'MA-Q-0220':'별도 소유 pharmacy 간 shared services written agreement',
'MA-Q-0290':'nursing home referral·business를 위한 무료 catering',
'MA-Q-0413':'cashier가 처방 data entry를 시작할 때 technician ratio 변화',
'MA-Q-0228':'central-fill 목적지·Schedule VI PMP reportable drug·MA license',
'MA-Q-0421':'암호화해도 employer에게 무권한 profile을 공개하는 confidentiality 위반',
'MA-Q-0167':'practitioner MCSR와 DEA schedule별 등록',
'MA-Q-0304':'hospital consultation과 community signed referral의 차이',
'MA-Q-0087':'valid no-substitution 지시와 저가 interchangeable product',
'MA-Q-0056':'serious dispensing injury의 Board 보고 기한',
'MA-Q-0409':'ACPE CE provider의 current approval·good standing 경로',
'MA-Q-0016':'adult first opiate 7일 원칙의 문서화된 acute-condition 예외',
'MA-Q-0395':'licensed health care facility가 아닌 그룹의료실의 ADD 설치',
'MA-Q-0137':'routine ADD의 장전·등록·기록·보안 요건',
'MA-Q-0344':'CPA의 vaccine 권한과 Commissioner order·eligible medication 경로',
'MA-Q-0131':'onsite pharmacy 없는 MA facility의 ADD licensing-body approval',
'MA-Q-0301':'retail pharmacy의 physician QA 고용과 CPA 체결 고용 구분',
'MA-Q-0400':'minor CII opioid 조제 시 부모에게 opioid antagonist offer',
'MA-Q-0420':'hospital employee spouse의 별거와 institutional dispensing 범위',
'MA-Q-0303':'CDTM referral·consent를 pharmacist와 physician 양쪽 기록에 보존',
'MA-Q-0012':'issue 31일째 Vyvanse 처방 유효기간',
'MA-Q-0133':'ADD 재고가 있어도 patient-specific valid order가 필요',
'MA-Q-0021':'generic oxymorphone 환자요청 partial fill의 30일 기한',
'MA-REV-0050':'cash 환자의 no-alert new prescription도 DUR가 필요함',
'MA-REV-0039':'원 controlled prescription의 DEA 번호와 container label·dispensing record 요건 구분',
'MA-EXP-0539':'오류 반환 의무와 비불량 반환·DEA take-back collector 권한 구분',
'MA-REV-0033':'paper prescription scan은 initial EPCS transfer 대상이 아님',
'MA-EXP-0583':'전자처방 예외 power failure와 보통 oral CII refill 금지',
'MA-REV-0054':'treating physician interaction call의 minimum-necessary 예외와 authorization·curiosity access 혼동',
'MA-EXP-0519':'buprenorphine 약명만으로 Part2 적용을 단정하지 않고 program/record source·single TPO consent 검토',
'MA-EXP-0587':'controlled Rx의 patient identity·prescriber signature 변경 및 CII earliest-fill date 변경 경계',
'MA-REV-0055':'NPP와 별도로 개인 login·role permissions·access log를 두는 전자 safeguards',
}
def comparisons(near,family,reason):
 out=[]
 for collection in ['canonical_nearest','public_nearest','default_nearest']:
  for row in near[collection]:
   qid=row['question_id']
   if collection=='public_nearest':
    finding='실제 stem 두 사례와 네 판단이 같고 보기 극성·질문 초점·조합을 바꾼 family drill이다. wording·사실·법적 결론의 중복을 확인했고, 원문 learning_boundary와 현재 default 제외 맥락에서 보관형 변형으로만 인정한다. 독립 새 사례 또는 mock 다양성으로 세지 않는다.'
   elif collection=='canonical_nearest':
    finding='실제 후보는 '+TOPICS[qid]+'을 판단한다. 이 문항의 '+reason+'와 비교했다. 일부 같은 법이나 record/환자 용어는 공유하지만 이 두 사례·보기 판단 전체를 재현한 canonical 문항으로 보지는 않았다.'
   elif qid in ['MA-EXP-0455','MA-EXP-0459']:
    finding='default 후보와 동일한 두 사례·대부분의 판단 문구를 공유하는 다른 극성/질문형식의 보관용 변형이다. 같은 mock에 넣어 새 독립 문항 수를 늘리면 안 된다. 현재 본 ID는 default에 없어 이 중복만으로 archive FAIL을 부여하지 않는다.'
   elif qid=='MA-REV-0054' and family in ['PRIV03','PRIV04']:
    finding='default 후보는 '+TOPICS[qid]+'이다. 치료 provider 소통·별도 authorization 오해·친구/무관 조회라는 사실·결론이 상당히 겹친다. 본 ID를 새 고유 시험 사례로 세지 않으며 보관형 범위에서만 distinct criterion을 판단했다.'
   else:
    finding='default 후보는 '+TOPICS[qid]+'을 다룬다. 이 문항의 '+reason+'와 비교하면 일부 원칙·명칭은 같아도 핵심 사실과 결정하는 의무가 다르다. 유사도 수치만으로 semantic duplicate로 판정하지 않았다.'
   out.append(row|{'collection':collection,'stem_and_all_choices_read':True,'finding_ko':finding})
 return out
