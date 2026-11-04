from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,copy
BASE=Path('reports/full-corpus-review/phase10-d-evidence')
REPORT=Path('reports/full-corpus-review/independent-phase10-d-review.json')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def write(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
packet_path=BASE/'assigned-visible-input.json'; packet=json.loads(packet_path.read_text())
assignment=json.load(open('/tmp/independent-phase10-d-assignment.json'))
SPECS={}
def add(qid,key,overview,options,next_action,legal='KEEP',realism='FAIL',realism_finding=None):
 SPECS[qid]={'key':key,'overview':overview,'options':options,'next':next_action,'legal':legal,'realism':realism,'realism_finding':realism_finding}
def O(truth,sid,section,finding):return {'truth':truth,'sid':sid,'section':section,'finding':finding}
T=True;F=False
# Each option below is a manually adjudicated proposition after reading its visible text and the retained controlling primary text.
add('MA-RW-0073',['C'],'9개 점포와 22명 full-time pharmacist를 두 독립 요건에 각각 대입했다. 점포 조건은 충족하지만 고용인원 조건을 넘으므로 지정된 independent seat 요건만 불충족이다. 다른 Board seat 전반의 부적격으로 확대하지 않는 원해설도 타당하다.',[
 O(F,'c13s22','M.G.L. c.13 §22(c)','점포 9개는 상한 안이지만 independent 정의는 20명 이하 full-time pharmacist 조건도 AND로 요구한다. 22명을 무시하는 A는 거짓이다.'),
 O(F,'c13s22','M.G.L. c.13 §22(c)–(d)','고용 약사가 20명을 넘는다는 사실은 chain 정의의 10개 이상 Massachusetts 점포를 대체하지 못한다. 이 조직은 9개 점포다.'),
 O(T,'c13s22','M.G.L. c.13 §22(c)','조직이 full-time pharmacist 22명을 고용하므로 20명 이하 조건을 넘는다. C가 지정 independent seat의 employer-setting 결과를 정확히 제한한다.'),
 O(F,'c13s22','M.G.L. c.13 §22(b)–(c)','개인의 경력·현재 practice 자격과 employer-setting 정의는 병존한다. 다른 개인 요건 충족이 조직 규모 요건을 없애지 않는다.')],
 '현재 키 C와 범위를 유지한다. 임명 검토 시 점포 수와 full-time 인원 수를 따로 확인하도록 하며 다른 seat 자격으로 확장하지 않는다.',realism='PASS',realism_finding='임명 후보의 실제 setting 적격성 결정을 요구한다. 9개/22명이라는 교차 사실로 AND 조건과 chain 별도 정의를 적용하며, A·B·D는 각각 점포만 보기·chain 자동 전환·개인 경력으로 대체라는 그럴듯한 혼동이다. MA-EXP-0193의 단순 구성 암기와 달리 특정 employer 판정을 요구하므로 중복 사례로 보지 않는다.')
add('MA-RW-0074',['A'],'임기 종료 뒤 holdover와 새로운 임기 reappointment를 나눴다. §22(n)은 successor 임명까지 계속 재직과 연속 두 임기 제한을 함께 규정하며 재임명 전 적어도 한 임기의 공백을 요구한다. 원해설은 이 구별을 정확히 유지한다.',[
 O(T,'c13s22','M.G.L. c.13 §22(n)','successor가 없으면 계속 office를 유지하지만 세 번째 연속 term을 새로 부여할 수 없다. A는 holdover와 재임명을 분리한다.'),
 O(F,'c13s22','M.G.L. c.13 §22(n)','즉시 퇴임한다는 부분은 holdover 문구에 반한다. 재임명 전 공백도 1년이 아니라 적어도 1 term이고 법정 term은 3년이다.'),
 O(F,'c13s22','M.G.L. c.13 §22(n)','successor 출현 시 종료하는 조건을 붙여도 세 번째 연속 appointment라는 성질이 달라지지 않는다. holdover를 새 임기로 전환하는 예외는 없다.'),
 O(F,'c13s22','M.G.L. c.13 §22(n)','결원이 있으면 연속 임기 제한이 정지된다는 조항은 없다. 계속 재직 사실만으로 즉시 새 term을 받을 수 없다.')],
 '키 A를 유지한다. 후속 학습에서는 holdover 기간을 새로운 세 번째 임기나 한 임기 공백으로 계산하지 않도록 문구를 보존한다.',realism='PASS',realism_finding='행정 담당자가 제안한 세 번째 appointment를 실제로 승인할 수 있는지 판단한다. MA-EXP-0197의 추상적 연속 임기 암기와 달리 successor 부재가 holdover를 촉발한다. 잘못된 1년 공백과 조건부 재임명은 실제 절차 혼동을 검사하고 정답만 특별히 길지 않다.')
add('MA-RW-0075',['D'],'Board investigator 신원 확인·관련 records·근무약사 접근 가능이라는 사실을 모두 확인했다. 최근 self-inspection 완료와 MOR 휴가가 inspection 기록 접근 의무를 대체하지 않는다. core와 A–D의 기록·사전 통지·보존 설명이 원문에 부합한다.',[
 O(F,'cmr9','247 CMR 9.19(16)(b)6; 9.24(3)','근무 약사는 모든 pharmacy records에 접근하고 요청 기록을 제공할 수 있어야 한다. 접근 가능한 기록을 MOR 복귀까지 일률적으로 미루는 A는 의무와 맞지 않는다.'),
 O(F,'cmr9','247 CMR 9.19(21); 9.24(3)','self-inspection 완료 진술은 실제 요청 documents 제공을 대체하지 못한다. 완료 tool은 적어도 2년 보존하므로 최근 완료가 면제 근거가 아니다.'),
 O(F,'cmr9','247 CMR 9.24(1), (3)','Board/designee는 사전 통지 없이 방문할 수 있다. 신원 확인된 investigator의 이번 요청에 새 advance notice를 선행조건으로 요구할 수 없다.'),
 O(T,'cmr9','247 CMR 9.19(16)(b)6; 9.24(1), (3)','근무약사에게 기록 접근·제공 능력을 요구하고 약국에 요청 자료 제공 의무가 있다. D가 현재 가능한 적법한 response다.')],
 '키 D와 resident·identified investigator·접근 가능 사실을 유지한다. self-inspection tool 자체와 완료 진술을 바꾸어 취급하지 않는다.',realism='PASS',realism_finding='inspection 현장에서 MOR 부재라는 실무 압박 아래 on-duty pharmacist의 조치를 고르게 한다. MA-EXP-0201의 annual review 대 inspection 비교와 연결되지만 이번 결정은 누가 지금 기록을 제공하는지다. 세 오답은 지연·대체·사전 통지 요구로 균형 잡혔다.')
add('MA-RW-0076',['A','C','D'],'최초 Board 지정 10일, 통상 21일, 반려 후 7일을 분리했다. 실제 supervising licensee가 지문에 있으므로 MOR와 그 사람 모두 서명한다. 위반별 조치·시기·책임자와 신속한 compliance에 관한 전체 한국어 설명도 조문과 일치한다.',[
 O(T,'cmr9','247 CMR 9.25(2)','각 violation의 corrective action, 예상 완료 또는 시행일, 각 조치의 책임자가 계획에 필요하다. 기존 vague training 약속을 이 요소로 구체화하는 A는 옳다.'),
 O(F,'cmr9','247 CMR 9.25(1), (5)','21일은 최초 plan의 기본 기간이고 Board가 이를 달리 지정할 수 있다. unacceptable plan 반려 후에는 별도 revised-plan 7일이므로 새 21일이 시작되지 않는다.'),
 O(T,'cmr9','247 CMR 9.25(3)','MOR와 그 practice를 감독하는 licensee가 있는 경우 그 licensee의 서명이 필요하다. 지문은 이 감독자를 명시하므로 두 서명이 맞다.'),
 O(T,'cmr9','247 CMR 9.25(5)','unacceptable plan을 pharmacy에 반환하면 revised plan은 7일 이내 제출해야 한다. 다른 revised deadline이 없는 이 사례에서 D를 선택한다.'),
 O(F,'cmr9','247 CMR 9.25(4)','법규 준수를 가능한 한 신속하게 달성해야 한다. 승인과 follow-up inspection까지 모든 corrective work를 유예하는 E는 허용되지 않는다.')],
 '정확 조합 A,C,D를 유지한다. 최초 기한과 수정 기한, 해당하는 경우의 supervisor 서명 조건을 함께 보존한다.',realism='PASS',realism_finding='반려된 실제 계획을 다시 작성하는 의사결정이다. MA-EXP-0205의 vague plan보다 Board 지정 10일·반려 7일·감독자 서명이라는 연결된 사실이 추가되어 독립 적용을 요구한다. 그럴듯한 21일 재시작과 승인 대기를 오답으로 사용한다.')
add('MA-RW-0077',['B','E'],'투약에 따른 L의 실제 verification 능력 저하와 M의 치료 중 안전한 practice 능력을 구분했다. impairment 또는 public-risk capacity가 있으면 실제 피해가 없어도 사유가 될 수 있으며 revocation은 자동 결과가 아니다. 원해설은 상태와 처분을 분리한다.',[
 O(F,'cmr10','247 CMR 10.03(1)(g), (k)','고용주의 승인이나 대체 인력 부족은 impaired practice 또는 위험 가능성을 제거하지 않는다. 실제 verification 능력이 손상된 L을 계속 근무시키는 사정을 면제로 볼 수 없다.'),
 O(T,'cmr10','247 CMR 10.03(1)(g), (k)','L은 능력이 impaired된 상태에서 practice를 지속한다. (k)는 capacity 또는 potential risk도 포함하므로 환자에게 error가 도달해야만 징계 사유가 생기는 것은 아니다.'),
 O(F,'cmr10','247 CMR 10.03(1)(g)','치료 사실 자체와 ability to practice의 impairment는 다르다. M은 안전한 practice 능력을 유지한다고 지문이 고정하므로 동일한 사유를 자동 확정할 수 없다.'),
 O(F,'cmr10','247 CMR 10.03(1); 10.06(1)–(6)','Board는 사유에 따라 disciplinary action을 부과할 수 있으며 여러 조치가 열거된다. impairment 확인만으로 반드시 revoke해야 한다는 D는 거짓이다.'),
 O(T,'cmr10','247 CMR 10.03(1)(g), (k)','능력 저하가 있는 L과 능력이 보존된 M은 impairment 판단에서 다르게 다뤄야 한다. 이는 실제 안전한 업무 능력에 대한 법적 구별이다.')],
 'B,E를 유지한다. 치료 이력만으로 impairment를 낙인찍거나 실제 error가 없다는 이유로 L의 업무 위험을 무시하지 않도록 범위를 유지한다.',realism='PASS',realism_finding='근무 대체 여부를 고민하는 소매약국에서 L과 M의 기능을 비교하는 현실적인 상황이다. MA-EXP-0209의 추상적 impaired-practice 설명을 medication somnolence·verification·대체 약사로 구체화했다. B와 E는 각각 피해 선행 필요성, 개인별 능력 판단을 검사하며 고용주 면제·자동 revocation도 실무 혼동이다.')
add('MA-RW-0078',['D'],'동의에 의한 해결 방식만으로 advisory 또는 nondisciplinary라고 분류할 수 없다. 12개월 조건부 practice는 10.06(4)의 disciplinary probation이고 과거 advisory letter와 별개다. 원해설의 hearing·조건부 practice·reprimand 구별이 정확하다.',[
 O(F,'cmr10','247 CMR 10.06(2), (4), (6)','과거 advisory letter는 formal discipline이 아니지만 현재 agreement의 성격을 결정하지 않는다. probation은 consent agreement로도 부과할 수 있어 hearing 부재가 advisory 전환 사유가 아니다.'),
 O(F,'cmr10','247 CMR 10.06(4)–(5)','weekly supervision 아래 practice가 허용되는 기간은 probation의 정의다. 독립 업무에 조건이 붙었다는 이유로 practice suspension과 같게 볼 수 없다.'),
 O(F,'cmr10','247 CMR 10.06(3)–(4)','reprimand도 formal disciplinary action이지만 지문의 핵심은 12개월 동안 조건부 practice 허용이다. 파일 보관·계속 업무만으로 reprimand라 분류할 수 없다.'),
 O(T,'cmr10','247 CMR 10.06(4), (6)','probation은 Board 조건하에 practice하는 기간이고 hearing 또는 consent agreement로 부과된다. D가 이 12개월 arrangement의 내용과 법적 분류에 맞다.')],
 'D를 유지한다. credentialing 공개 여부까지 이 문항의 분류 결론으로 대신 결정하지 않는 기존 learning 범위를 보존한다.',realism='PASS',realism_finding='합의문을 실제 내용으로 분류하는 면허 관련 법적 판단이다. MA-EXP-0213은 advisory letter 정의를 묻지만 이번 문항은 별도 현재의 기간·supervision·monitoring을 적용한다. disciplinary라는 표현은 reprimand도 가능한 배경이며 정답을 결정하는 추가 사실은 조건부 practice 기간이다.')
add('MA-RW-0079',['A','C','E'],'summary suspension과 Board President quarantine의 limited necessity hearing을 서로 다른 clock으로 계산했다. 7일과 15영업일은 merits 완료기한이 아니며 단순 hearing 요청은 notice를 해제하지 않는다. 전체 해설의 주체·기간·효력 구별은 원문과 맞는다.',[
 O(T,'cmr10','247 CMR 10.07','summary action 필요성에 한정된 hearing은 Board action 후 seven days 이내 제공해야 한다. business days나 최종 merits 완료로 바꾸지 않은 A가 옳다.'),
 O(F,'cmr10','247 CMR 10.07; 10.08(3)','15 business days는 specified notice hearing이고 summary suspension hearing은 7일이다. 두 조치가 모두 위험 대응이라는 공통점은 clock을 합치지 않는다.'),
 O(T,'cmr10','247 CMR 10.08(1), (3)','Board President도 quarantine을 내릴 수 있고 그 necessity hearing은 action 후 15영업일 이내다. pharmacy를 licensee로 적용한 C는 옳다.'),
 O(F,'cmr10','247 CMR 10.08(3)','15영업일의 대상은 interim notice의 necessity hearing이다. 모든 merits와 최종 disciplinary decision까지 그 안에 완료하라는 조문이 아니다.'),
 O(T,'cmr10','247 CMR 10.08(2)','notice는 rescind/amend 또는 관련 complaint의 final action 및 final decision까지 효력을 유지한다. 그런 사건이 없는 지문에서 hearing 요청만으로 약품 사용은 허용되지 않는다.')],
 'A,C,E를 유지한다. seven days와 fifteen business days, limited necessity와 merits, Board와 President를 바꾸지 않는다.',realism='PASS',realism_finding='같은 날 발생한 개인 면허정지와 약국 quarantine을 비교하여 올바른 대응 기한과 약품 사용 여부를 정한다. MA-EXP-0217의 일반적 summary 가능성보다 실제 clock과 존속효력을 연결한다. 경쟁 기간과 limited hearing 오해는 현실적이며 각 option이 서로 다른 결론을 검사한다.')
add('MA-RW-0080',['B','D'],'2021-10-01 grant는 2026-10-01 5주년에 만료되며 9월의 subsequent filing은 새 grant가 아니다. public interest·impractical AND unduly burdensome·safeguards를 모두 요구한다. 원해설의 날짜 계산·신청/승인·AND 구별이 조문에 부합한다.',[
 O(F,'cmr14','247 CMR 14.01(5)(b)–(d)','만료 전후 subsequent petition을 낼 수 있지만 접수에 자동 연장 효력을 부여하지 않는다. 2026-10-02 현재 grant가 없어 former waiver는 유지되지 않는다.'),
 O(T,'cmr14','247 CMR 14.01(5)(b), (d)','5주년 후에는 subsequent waiver가 granted되지 않았다면 원래 247 CMR requirements를 준수해야 한다. 과거 waiver나 owner의 계속 운영 제안은 예외가 아니다.'),
 O(F,'cmr14','247 CMR 14.01(1), (3), (5)(c)','비용 자료가 burden 설명에 관련될 수 있어도 compelling public interest와 충분한 safeguards를 대신하지 못한다. subsequent petition도 (1)–(4)를 충족해야 한다.'),
 O(T,'cmr14','247 CMR 14.01(1)(a)–(c), (3)(b)–(d), (5)(c)','impractical과 unduly burdensome은 AND이고 public interest와 safeguards도 별도 기준이다. D는 모두 설명해야 함을 정확히 나타낸다.'),
 O(F,'cmr14','247 CMR 14.01(2), (5)(b)–(d)','MOR의 서명은 petition 제출 요건일 뿐 grant가 아니다. 새 5년은 Board가 waiver를 grant한 날을 기준으로 하므로 서명일에 시작되지 않는다.')],
 'B,D와 실제 grant·만료 날짜를 유지한다. 비용 부담을 OR 요건이나 자동 연장으로 바꾸지 않으며 future grant 여부는 새 사실이 있어야 판단한다.',realism='PASS',realism_finding='만료 직후 대체 절차를 계속할 수 있는지 운영 결정을 요구한다. MA-EXP-0221의 단순 pending waiver와 달리 이전 grant, 5주년, 선접수, 후속 미승인이라는 날짜 관계가 있다. 자동 연장·비용 대체·MOR 서명 clock은 그럴듯한 절차 혼동이며 특정 option만 qualified하지 않다.')
# MOR05: independent readings of each rotated instance, including incorrect polarity.
add('MA-EXP-0169',['C'],'Case A의 Schedule II만 세겠다는 계획은 6.10(2)(a)의 II–V 및 PMP-reportable VI 범위를 누락한다. 원core는 정확하지만 Case B가 선택 판단에 불필요하고 generic 대체서명 설명은 허용 조건과 통지 시점을 구체화해야 한다.',[
 O(F,'cmr6','247 CMR 6.10(2)(a)','사망·중병·termination 때문에 outgoing MOR가 없는 경우 staff pharmacist 서명이 허용될 수 있지만 application 제출 시 Board에 이유를 통지해야 한다. 이유 생략은 허용되지 않는다.'),
 O(F,'cmr6','247 CMR 6.10(2)(a)','inventory report는 pharmacy controlled-substance records와 함께 file해야 한다. application 제출이 폐기 허가가 아니므로 B는 거짓이다.'),
 O(T,'cmr6','247 CMR 6.10(2)(a)','handover attestation은 모든 II–V와 PMP에 보고할 VI의 inventory를 확인한다. C가 Case A의 Schedule II-only 제안을 바로잡는다.'),
 O(F,'cmr6','247 CMR 6.10(1)–(2)','MOR 변경에는 Board approval을 위한 별도 application과 licensee/권한 있는 대표 및 proposed MOR의 서명 등이 필요하다. inventory 하나로 전부를 대신하지 못한다.')],
 'C는 법적 지지를 받는다. MOR 변경 당일의 실제 재고 확인 사례 하나로 다시 쓰고 Case B는 별도 의사결정으로 분리하며 통지 시점을 application 제출 시로 명시한다.')
add('MA-EXP-0170',['D'],'Case B의 serious illness는 대체 서명 허용 사유에 해당하지만 Board notice와 authorization 조건을 충족해야 한다. D의 추상적인 applicable conditions를 원해설에서 실제 조건과 제출 시점으로 밝혀야 한다. A–C는 application·보존·범위를 각각 잘못 바꾼다.',[
 O(F,'cmr6','247 CMR 6.10(1)–(2)','inventory 외에도 change-of-MOR application, 소정 서명, original license, fee 등 요구 항목이 있다. inventory alone이라는 A는 거짓이다.'),
 O(F,'cmr6','247 CMR 6.10(2)(a)','보고서는 pharmacy controlled-substance records에 file해야 한다. application과 함께 attestation을 낸 뒤 inventory를 버리는 것은 맞지 않는다.'),
 O(F,'cmr6','247 CMR 6.10(2)(a)','MOR handover 범위는 II만이 아니라 II–V 및 PMP-reportable VI다. Case A의 제한 제안을 사실로 채택한 C는 거짓이다.'),
 O(T,'cmr6','247 CMR 6.10(2)(a)','serious illness로 outgoing MOR가 unavailable이면 staff pharmacist가 authorized되어 inventory report에 서명할 수 있다. Board는 application 제출 시 대체 이유를 통지받아야 하므로 D의 조건부 경로가 옳다.')],
 'D의 법적 판단은 유지하되 serious illness·대체 서명권 부여·application 제출 시 이유 통지라는 실제 기록 검토 하나로 새 사례를 작성한다.')
add('MA-EXP-0171',['A','B','D'],'SATA는 inventory 범위, 대체서명 조건, application 서명을 각각 평가해 A,B,D가 남는다. 원core와 C 교정은 정확하다. D의 designated licensee 표현은 법령의 licensee 또는 duly authorized representative까지 설명하도록 보강할 가치가 있다.',[
 O(T,'cmr6','247 CMR 6.10(2)(a)','II–V와 PMP-reportable VI를 inventory에 포함한다. 비보고 VI 전체까지 뜻하는 것은 아니며 II-only도 아니다.'),
 O(T,'cmr6','247 CMR 6.10(2)(a)','질병으로 outgoing MOR가 unavailable인 Case B는 대체서명 경로를 사용할 수 있으나 자동 무조건 서명이 아니다. application과 함께 Board에 이유를 알려야 한다.'),
 O(F,'cmr6','247 CMR 6.10(2)(a)','attestation 제출과 실제 inventory report의 controlled-substance records 보관은 별도다. 제출 후 폐기하는 C는 거짓이다.'),
 O(T,'cmr6','247 CMR 6.10(2)','change application에는 licensee 또는 duly authorized representative와 proposed new MOR가 서명한다. D의 designated licensee는 해당 서명 주체를 뜻하는 범위에서 옳으며 대표자 대체도 허용된다.')],
 'A,B,D 조합의 법적 근거는 보존하되 D 서명 주체를 법령대로 풀어 적는다. 동시 재고·서명·application 중 실제 결함을 가진 단일 handover 사례로 재작성한다.')
add('MA-EXP-0172',['A'],'INCORRECT 극성을 따로 계산했다. B·C·D는 6.10(2)(a)에 맞고 inventory가 application 전체를 대신한다는 A만 거짓이다. 원해설은 error 선택과 true distractor를 올바르게 구별하지만 동일 사례 반복을 학습 범위로 늘려서는 안 된다.',[
 O(F,'cmr6','247 CMR 6.10(1)–(2)','inventory는 application의 일부이며 change approval application 자체를 대체하지 못한다. 따라서 거짓 문장을 고르는 이 문항의 선택은 A다.'),
 O(T,'cmr6','247 CMR 6.10(2)(a)','II–V와 PMP-reportable VI의 handover inventory라는 B는 참이므로 INCORRECT 정답에 포함하지 않는다.'),
 O(T,'cmr6','247 CMR 6.10(2)(a)','대체서명은 지정 사유와 authorization 및 application 제출 시 이유 통지를 수반한다. 조건부 경로를 말하는 C는 참이다.'),
 O(T,'cmr6','247 CMR 6.10(2)(a)','inventory report를 controlled-substance records와 함께 file한다는 D는 참이다. Board 제출 attestation과 보관 의무를 혼동하지 않는다.')],
 '법적 오류 선택 A는 유지한다. 다른 세 변형과 합쳐 새 학습 범위로 세지 말고 실제 누락된 application 서명을 발견하는 단일 시나리오로 대체한다.')
# MOR06
add('MA-EXP-0173',['B'],'소유권 이전은 outgoing Board notice와 incoming license application이 각각 적어도 14일 전이다. name change는 별도 사후 14일 통지다. 원core는 이 구별을 지지하지만 Case B의 only name change와 new owner를 한데 둔 문장은 사건 경계를 혼란스럽게 한다.',[
 O(F,'cmr6','247 CMR 6.11(2)–(3); 6.13(5); 6.14','사업 매매 자체로 재고 inventory·Board 절차나 patient-file transfer가 완료되지 않는다. 재고·파일·facility application이 별도 요구라는 A의 반대가 맞다.'),
 O(T,'cmr6','247 CMR 6.11(1)','현재 licensee는 proposed transfer 적어도 14일 전에 Board에 알려야 한다. closing 당일 통지는 이 기간을 충족하지 않으므로 B가 Case A에 맞다.'),
 O(F,'cmr6','247 CMR 6.11(2); 6.12','명칭 변경 통지는 새 owner의 operating license application을 대신하지 않는다. 기존 license가 name-change notice로 자동 이전되는 C는 거짓이다.'),
 O(F,'cmr6','247 CMR 6.11(1)–(3)','seller notice 외에 proposed new licensee가 적어도 14일 전 소정 application을 낸다. outgoing 절차가 incoming application을 대체하지 못한다.')],
 'B의 사전 14일은 유지한다. closing 예정일과 seller notice 접수일이 있는 소유권 이전 한 사건으로 바꾸고 name-only 변경은 다른 사례로 분리한다.')
add('MA-EXP-0174',['C'],'Case B의 이름만 변경하는 사건에는 6.12의 서면 통지·14일·authorizing documentation이 맞다. 다만 지문은 new owner가 있다고도 읽혀 ownership change와 충돌하므로 실전 사례로는 정리해야 한다. 키 C의 법적 명제 자체는 지지된다.',[
 O(F,'cmr6','247 CMR 6.11(1)–(3)','seller의 통지와 buyer의 신규 운영 license application은 별개다. 전자가 후자를 대체한다는 A는 거짓이다.'),
 O(F,'cmr6','247 CMR 6.11(3); 6.13(5); 6.14','매매가 완료됐다는 사실은 controlled stock 및 patient-file 이전 절차의 자동 완료가 아니다. B는 별도 법적 행위를 생략한다.'),
 O(T,'cmr6','247 CMR 6.12','운영명 변경은 14일 이내 서면 통지와 적절한 authorizing documentation을 요구한다. C는 name-only 사건의 규칙에 맞다.'),
 O(F,'cmr6','247 CMR 6.11(1)','ownership transfer notice는 closing 14일 후가 아니라 적어도 14일 전이다. D는 같은 숫자의 방향을 뒤집는다.')],
 'C를 지지하되 동일 owner가 상호만 바꿨다는 사실을 명시해 새 시나리오를 작성한다. 사전 14일 ownership과 사후 14일 name notice의 주체를 분리한다.')
add('MA-EXP-0175',['A','B','C','D'],'네 명제를 각각 current 6.11·6.12·6.13·6.14에 대조한 결과 모두 참이다. all-four SATA도 허용되지만 반복된 Case A/B와 추상적 related requirements 때문에 실제 네 개의 새로운 판단 사례가 되는 것은 아니다.',[
 O(T,'cmr6','247 CMR 6.11(1)','transfer 전에 outgoing licensee가 적어도 14일 사전 Board notice를 한다. Case A의 closing-day 통지를 올바르게 교정한다.'),
 O(T,'cmr6','247 CMR 6.11(3)(b)–(c); 6.13(5); 6.14','controlled stock의 inventory/transfer 절차와 환자 파일의 timely transfer는 사업 소유권 변경과 별개로 평가한다. 매매만으로 양쪽이 완료되지는 않는다.'),
 O(T,'cmr6','247 CMR 6.12','operating-name change에는 14일 이내 서면 통지 및 supporting authorizing documentation이 필요하다. ownership 이전 clock과 다르다.'),
 O(T,'cmr6','247 CMR 6.11(2)–(3)','proposed new licensee는 transfer 적어도 14일 전 적용되는 pharmacy license application을 제출한다. notice만으로 새 license가 생기지 않는다.')],
 '정확 조합 A,B,C,D를 기록하되 all-true 여부를 조정하기 위한 단순 option 반전은 하지 않는다. 새 owner application과 재고·파일 인계가 함께 필요한 실제 transaction 사례로 재설계한다.')
add('MA-EXP-0176',['D'],'INCORRECT 문항에서 A·B·C는 각각 seller advance notice·name change·buyer application 규칙에 맞다. 사업 매매가 stock/file 절차까지 자동 충족한다는 D만 거짓이다. 원해설은 극성을 맞게 설명한다.',[
 O(T,'cmr6','247 CMR 6.11(1)','ownership 이전 최소 14일 전 Board notice라는 A는 참이며 오류 선택 대상이 아니다.'),
 O(T,'cmr6','247 CMR 6.12','name change의 14일 이내 서면 notice와 자료라는 B는 참이다. 별도 신규 owner licensing을 대신한다는 뜻으로 확장하지 않는다.'),
 O(T,'cmr6','247 CMR 6.11(2)–(3)','proposed new licensee의 advance application 의무가 있으므로 C는 참이다. 이 사건에서는 적어도 14일 전이 기준이다.'),
 O(F,'cmr6','247 CMR 6.11(3); 6.13(5); 6.14','매매 완료와 stock inventory/transfer·patient-file 처리는 별도다. 따라서 D가 유일한 거짓 명제다.')],
 'D의 오류 판단을 보존하되 앞의 세 변형과 동일한 사례·보기 문장을 반복 배치하지 않는다. stock 이전 또는 환자 파일 지연이라는 실제 미완료 행위를 제시한다.')
# MOR07
add('MA-EXP-0177',['A'],'6.15(1)의 적용 시설은 공사 착수 전 approval이 필요하고 6.16은 relocation 전 approval 및 원칙 90일 전 application을 요구한다. A의 applicable 한정과 원해설의 해당 경계는 타당하나 지문의 pharmacy license category를 구체화하면 더 명료하다.',[
 O(T,'cmr6','247 CMR 6.15(1)','열거된 적용 pharmacy가 configuration/remodeling을 하려면 Board approval 전 공사 착수를 할 수 없다. A의 applicable 변경이라는 범위에서 참이다.'),
 O(F,'cmr6','247 CMR 6.16','90일 application 기간은 희망 relocation date 전으로 계산한다. 이동 후 기간이라는 B는 거짓이다.'),
 O(F,'cmr6','247 CMR 6.16','application이 제때 제출되어도 approval을 받기 전에는 relocation할 수 없다. 접수를 허가로 바꾸는 C는 거짓이다.'),
 O(F,'cmr6','247 CMR 6.15(2)','적용 sterile compounding pharmacy의 secondary engineering control 교체도 사전 approval 대상이다. 주소가 같다는 이유로 면제되지 않는다.')],
 'A를 지지한다. resident Drug Store Pharmacy와 구체적인 공사 착수일·미승인 상태를 제시하는 단일 사례로 재작성하고 license category를 명시한다.')
add('MA-EXP-0178',['B'],'Case B의 90일 전 application은 신청 시기를 충족할 수 있지만 move approval이 아니다. B를 선택한다. 원core의 90일 예외·secondary control 별도절차는 원문과 일치하며 직접 연결되지 않은 Case A를 제거할 수 있다.',[
 O(F,'cmr6','247 CMR 6.16','ordinary 90일은 desired relocation 전에 application을 내는 기간이다. 이미 이전한 후의 대기기간이 아니다.'),
 O(T,'cmr6','247 CMR 6.16','약국은 새 주소로 relocation하기 전에 Board approval을 받아야 하고 application 제출만으로 이동할 수 없다. B가 Case B의 잘못된 가정을 교정한다.'),
 O(F,'cmr6','247 CMR 6.15(2)','secondary engineering control 교체는 해당 sterile 시설에서 사전 Board approval을 요구한다. 기존 주소라는 사실은 이를 면제하지 않는다.'),
 O(F,'cmr6','247 CMR 6.15(1)','적용 remodeling은 construction work를 시작하기 전에 approval을 받아야 한다. 완공 후 inspection에서 보통 받아도 된다는 D는 거짓이다.')],
 'B를 유지하되 application 접수와 실제 approval 통지 날짜가 다른 relocation 사건으로 새로 구성한다. remodeling 사례를 불필요하게 함께 붙이지 않는다.')
add('MA-EXP-0179',['D'],'SATA의 A·B·C를 각각 secondary control 면제, 신청=승인, 사후 remodeling approval이라는 거짓으로 평가했다. D만 90일 전 원칙과 Board-approved 예외를 모두 맞춘다. 단일정답 SATA의 법적 조합은 D다.',[
 O(F,'cmr6','247 CMR 6.15(2)','secondary engineering control을 교체하는 적용 sterile 시설은 같은 주소여도 사전 approval이 필요하다. 면제를 주장하는 A는 거짓이다.'),
 O(F,'cmr6','247 CMR 6.16','timely application은 approval과 다르다. Board decision 전에 자동으로 move할 수 있다는 B는 거짓이다.'),
 O(F,'cmr6','247 CMR 6.15(1)','applicable remodeling은 approval이 construction 시작보다 앞서야 한다. 완공 후에 ordinarily 받는다는 C는 반대다.'),
 O(T,'cmr6','247 CMR 6.16','desired relocation date 적어도 90일 전 application이 원칙이고 Board가 달리 승인할 수 있다. D만 참이므로 SATA의 한 개 조합은 D다.')],
 'D만이라는 정확 조합을 보존한다. 세 형식 변형의 반대 문장을 다시 쓰기보다 relocation application과 시작 허용 여부가 갈리는 새 날짜 사례로 대체한다.')
add('MA-EXP-0180',['C'],'INCORRECT 극성에서 A·B·D는 각각 relocation 승인·remodeling 사전승인·90일 전 신청 규칙에 맞다. 주소 불변이면 secondary control을 자유롭게 교체한다는 C만 거짓이다. 원해설은 이 경계를 올바르게 설명한다.',[
 O(T,'cmr6','247 CMR 6.16','application만으로 Board approval이 되지 않으므로 A는 참이다. 오류 선택에 넣지 않는다.'),
 O(T,'cmr6','247 CMR 6.15(1)','applicable remodeling/configuration 변경은 착수 전 approval을 받는다. B의 사전 요구는 참이다.'),
 O(F,'cmr6','247 CMR 6.15(2)','sterile secondary engineering control을 moving/adding/modifying/removing/replacing하기 전 approval이 필요하다. 주소가 같다는 이유만의 면제는 없어 C가 오류다.'),
 O(T,'cmr6','247 CMR 6.16','desired date 최소 90일 전이 원칙이고 Board-approved 예외가 있다. D는 정확하다.')],
 'C의 오류 판단을 유지한다. 실제 cleanroom secondary-control 교체가 계획된 해당 license category 사례로 좁혀 구성하고 다른 세 변형과 교차 노출을 막는다.')
# MOR08: precise, unresolved institutional exemption in the actual stem.
add('MA-EXP-0181',None,'일반 resident Drug Store Pharmacy라면 D가 맞다. 그러나 지문의 resident pharmacy는 institutional sterile compounding pharmacy를 배제하지 않고 6.13(7)은 그 시설의 (3),(4)를 면제한다. 원core 마지막의 예외를 확인하라는 문장은 이 누락 사실을 보충하지 못한다.',[
 O(F,'cmr6','247 CMR 6.13(1)–(7)','nonresident의 (6) 제외와 institutional sterile의 (3),(4) 제외가 명시되어 있다. 모든 license category에 똑같다는 A는 거짓이다.'),
 O(F,'cmr6','247 CMR 6.13(4), (7)','적용되는 환자 통지 그룹은 intended closure 전 90일 내 fill한 환자다. final-day pickup 대기자로만 제한하는 B는 그 규칙과 맞지 않는다.'),
 O(F,'cmr6','247 CMR 6.13(5)','환자 요청 또는 법/계약에 따른 file transfer는 patient needs를 맞추는 timely 방식이어야 한다. 모든 transfer를 재고 청산까지 미루는 C는 허용되지 않는다.'),
 O('CONDITIONAL','cmr6','247 CMR 6.13(1), (4), (7)','일반 resident 약국에는 Board advance notice와 patient notice가 필요해 D가 참이다. institutional sterile이면 (4) 환자 통지가 면제되므로 현재 stem만으로 D의 법적 의무 결론을 확정할 수 없다.')],
 'HOLD. resident Drug Store Pharmacy이며 institutional sterile compounding pharmacy가 아니라는 사실을 넣고 14일 전 notice·개별 통지 시도·게시를 새 사례로 재검토한다.',legal='HOLD')
add('MA-EXP-0182',None,'A의 90일 환자선정 및 최소 14일 전 통지 시도는 6.13(4)의 정확한 규칙이다. 다만 resident만으로 institutional sterile 예외(7)를 배제하지 못한다. 원해설은 일반 원칙과 예외를 언급하지만 이 Case B가 어느 시설인지 고정하지 않아 whole-key는 모호하다.',[
 O('CONDITIONAL','cmr6','247 CMR 6.13(4), (7)','(4) 적용 약국에서는 closure 전 90일 내 fill한 각 환자에 최소 14일 전 통지를 시도하므로 A가 참이다. institutional sterile은 이 의무가 제외되어 지문의 법적 적용이 확정되지 않는다.'),
 O(F,'cmr6','247 CMR 6.13(5)','file transfers를 inventory liquidation까지 일괄 연기할 수 없다. 환자 필요에 맞춰 timely 처리해야 한다.'),
 O(F,'cmr6','247 CMR 6.13(2), (6)–(7)','license categories별로 별도 요건·제외가 있으므로 every provision identical이라는 C는 거짓이다.'),
 O(F,'cmr6','247 CMR 6.13(1), (4)','마지막 날 게시 하나는 적용되는 Board advance notice와 환자별 사전 통지 시도를 대체하지 못한다. 기관 면제가 없는 경로에서 D는 명백히 거짓이다.')],
 'HOLD. 환자가 처방을 수령한 일반 resident retail Drug Store Pharmacy로 Case B를 명시하고 closure 예정일과 notice 발송일을 제시하여 A의 적용·기한을 새로 판단한다.',legal='HOLD')
add('MA-EXP-0183',None,'A는 환자 필요에 맞는 timely transfer라 참이고 B·D는 거짓이다. C의 patient notification은 일반 resident 약국에서 참이지만 institutional sterile에는 6.13(7) 예외가 있다. 따라서 현재 SATA A,C는 시설 범위를 정하기 전까지 유일 조합으로 확정할 수 없다.',[
 O(T,'cmr6','247 CMR 6.13(5)','환자 요청으로 file을 다른 약국에 넘길 때 timely manner로 patient needs를 충족해야 한다. institutional 예외(7)는 (5)를 제외하지 않아 A는 지지된다.'),
 O(F,'cmr6','247 CMR 6.13(4), (7)','적용 통지대상은 final-day pickup만이 아니라 closure 전 90일의 fills다. B는 올바른 대상 범위를 틀리게 줄인다.'),
 O('CONDITIONAL','cmr6','247 CMR 6.13(1), (4), (7)','Board 사전 통지는 resident에 적용되지만 patient-notification efforts는 institutional sterile의 경우 (4) 제외다. stem에 license category가 없어 C 선택이 조건부다.'),
 O(F,'cmr6','247 CMR 6.13(6)–(7)','nonresident와 institutional sterile의 명시적 예외가 있으므로 모든 license category의 closure provisions가 동일하다는 D는 거짓이다.')],
 'HOLD. institutional sterile이 아닌 resident retail facility로 고정한 뒤 A,C 조합을 다시 검토한다. 환자 transfer 요청일과 폐업·통지 날짜를 자연스럽게 결합한 단일 사례로 교체한다.',legal='HOLD')
add('MA-EXP-0184',None,'오류를 고르는 문항이지만 B 외 A와 D의 적용도 시설에 좌우된다. 일반 resident 약국이면 B만 거짓이나 institutional sterile이면 (4)의 통지 의무가 제외되어 같은 단일 오류 조합을 보장할 수 없다. 원해설은 오류 극성은 맞지만 범위 결함을 남긴다.',[
 O('CONDITIONAL','cmr6','247 CMR 6.13(1), (4), (7)','일반 resident의 Board·patient advance notice라는 A는 참이다. institutional sterile은 patient-notice (4)가 제외되므로 현재 사실만으로 true distractor라고 확정할 수 없다.'),
 O(F,'cmr6','247 CMR 6.13(2), (6)–(7)','모든 license category가 동일하다는 B는 명시 예외와 충돌한다. B 자체는 분명한 오류지만 그것만 유일한 오류인지는 시설 범위가 필요하다.'),
 O(T,'cmr6','247 CMR 6.13(5)','환자 요청 file transfer는 patient needs에 맞춰 timely 처리한다. (7)은 (5)를 제외하지 않으므로 C는 참이다.'),
 O('CONDITIONAL','cmr6','247 CMR 6.13(4), (7)','일반 resident에는 90일 fills로 환자를 정하고 최소 14일 전 통지를 시도한다. institutional sterile이면 이 patient notice 의무 자체가 제외되어 D의 적용이 조건부다.')],
 'HOLD. pharmacy license category를 일반 resident retail로 명시한 뒤 INCORRECT의 유일성이 B인지 새로 검토한다. 현재 B만 정답이라는 확정 학습을 차단한다.',legal='HOLD')
# MOR09
add('MA-EXP-0185',['C'],'closure transfer의 inventory는 실제 transfer date에 해야 하고 양 MOR 서명이 원칙이다. C의 complete는 법령상 요구 범위 II–V/PMP-reportable VI의 완전한 inventory로 읽었다. 연방도 그 날 complete inventory를 요구하며 수주 뒤 estimate는 대체하지 못한다.',[
 O(F,'cmr6','247 CMR 6.14(2)(d)','양 약국의 inventory attestation은 transfer 후 10일 이내 Board에 제출한다. 다음 routine renewal까지 미루는 A는 거짓이다.'),
 O(F,'cmr6','247 CMR 6.14(2)(f)','이 closure transfer 뒤 transferor는 controlled substances를 possess할 수 없다. 추가 authority 없이 일부 잔여 stock을 보유하는 B는 허용되지 않는다.'),
 O(T,'cmr6','247 CMR 6.14(2)(a)–(b); 21 CFR 1301.52(e)(1)','transfer date에 요구 범위 inventory를 하고 transferor/transferee MOR가 서명한다. 지정 unavailable 사유에는 staff 대체 경로가 있으며 수주 뒤 estimate로 대체할 수 없어 C가 참이다.'),
 O(F,'cmr6','247 CMR 6.14(2)(c), (e)','양쪽 약국 모두 inventory copy를 최소 2년 또는 다른 법정 기간 보관해야 한다. receiving pharmacy만이라는 D는 거짓이다.')],
 'C는 지지된다. transfer 당일 실제 계수·양 MOR 서명·대체서명 유무를 검토하는 한 사건으로 재작성하고 complete inventory의 schedule 범위를 명시한다.')
add('MA-EXP-0186',['D'],'Case B의 잔여 controlled stock 보유는 6.14(2)(f)에 반한다. 원해설은 closure/ownership transfer 경계에서 이 결과를 제한하므로 일반 pharmacy 간 모든 이동에 확대하지 않는다. 보존 주체와 attestation 기한도 따로 확인했다.',[
 O(F,'cmr6','247 CMR 6.14(2)(a)–(b)','실제 transfer date의 inventory와 소정 서명을 수주 뒤 estimate가 대신하지 못한다. A는 날짜·완전성 모두 잘못 바꾼다.'),
 O(F,'cmr6','247 CMR 6.14(2)(d)','attestation은 transfer 후 10일 이내이며 routine renewal까지 연기하는 B는 거짓이다.'),
 O(F,'cmr6','247 CMR 6.14(2)(c)','transferor와 transferee 양쪽이 inventory report copy를 최소 2년 또는 다른 법정기간 보존한다. receiving pharmacy만 보관한다는 C는 거짓이다.'),
 O(T,'cmr6','247 CMR 6.14(2)(f)','이 closure-transfer 절차에서는 transfer date 후 transferor가 controlled substances를 보유할 수 없다. D의 경계는 해당 절차로 제한되어 옳다.')],
 'D를 유지한다. 실제 transfer 후 발견된 잔여 병의 처리와 보존된 재고표 확인으로 새 상황을 만들고 다른 세 문항의 동일 Case A를 반복하지 않는다.')
add('MA-EXP-0187',['A','B','C'],'각 명제의 주체와 날짜를 재계산했다. 양쪽 inventory 보존, transfer-date inventory/서명, 10일 내 attestation은 모두 참이고 잔여 stock 보유 D는 거짓이므로 A,B,C다. 원core의 최소 2년은 다른 법률의 더 긴 기간을 배제하지 않는다.',[
 O(T,'cmr6','247 CMR 6.14(2)(c)','양 약국이 inventory copy를 적어도 2년 또는 법이 더 요구하는 기간 보관하며 readily retrievable해야 한다. at least라는 A의 제한이 맞다.'),
 O(T,'cmr6','247 CMR 6.14(2)(a)–(b)','transfer 당일 II–V와 PMP-reportable VI inventory를 하고 소정 MOR 서명을 받는다. lawful alternative signature를 포함한 required signatures라는 B는 참이다.'),
 O(T,'cmr6','247 CMR 6.14(2)(d)','Board inventory attestation은 transfer 후 10일 내 양 약국이 file한다. C는 renewal 시점과 다르다.'),
 O(F,'cmr6','247 CMR 6.14(2)(f)','closure-transfer date 이후 transferor의 controlled-substance 보유는 금지된다. without further authority라고 한 D는 허용 경로를 제공하지 않는다.')],
 'A,B,C 조합을 보존한다. 양 약국 중 한쪽의 10일 내 미제출과 기록 인계를 실제로 검토하는 새 사례로 구성하고 보존 기간의 다른 법률 조건을 남긴다.')
add('MA-EXP-0188',['A'],'INCORRECT 문항에서 attestation을 renewal까지 미룬다는 A가 거짓이고 B·C·D는 closure-transfer 규칙에 맞다. 원해설은 극성에 맞게 true distractor를 제외했다. 재고 서명과 Board attestation은 서로 다른 문서 행위다.',[
 O(F,'cmr6','247 CMR 6.14(2)(d)','attestation은 controlled inventory를 확인하여 transfer 후 10일 내 file한다. renewal까지 defer한다는 A가 오류 선택이다.'),
 O(T,'cmr6','247 CMR 6.14(2)(f)','해당 closure-transfer 뒤 transferor가 controlled substances를 남기지 못한다는 B는 참이다.'),
 O(T,'cmr6','247 CMR 6.14(2)(c)','양 약국에 최소 2년 또는 다른 법정기간의 inventory copy 보존 의무가 있어 C는 참이다.'),
 O(T,'cmr6','247 CMR 6.14(2)(a)–(b)','법정 inventory는 실제 transfer date에 소정 서명과 함께 완성한다. 수주 뒤 estimate로 대체할 수 없으므로 D는 참이다.')],
 '오류 선택 A를 보존한다. 실제 transfer date와 Board attestation 제출일을 주어 기한 위반을 결정하는 사례로 교체하고 renewal이라는 절대적 지연만으로 정답을 드러내지 않는다.')
# MOR10
add('MA-EXP-0189',['B'],'단독 약사의 이 경로는 prescription area 밖으로 잠시 나갈 수 있게 하지만 premises를 떠나도록 하지 않는다. 30분/6시간과 12시간/24시간 뒤 연속 8시간 rest는 서로 다르다. 원core의 구분과 final verification 불양도 설명은 조문에 맞는다.',[
 O(F,'cmr9','247 CMR 9.01(17)','일반 meal break는 연속 8시간 휴식이 아니다. 24시간 중 12시간 초과 practice의 rest 규칙을 30분 break로 대신할 수 없다.'),
 O(T,'cmr9','247 CMR 9.19(17)(a)','single-pharmacist의 permitted temporary absence는 prescription area에서의 부재이며 pharmacist는 premises에 남아야 한다. B는 이 경계를 정확히 설명한다.'),
 O(F,'cmr9','247 CMR 9.19(17)(a)','ordinary temporary absence 상한은 6시간당 30분이다. 45분으로 늘린 C는 거짓이다.'),
 O(F,'cmr9','247 CMR 9.19(17)(b)–(c)','support staff는 nondiscretionary duties를 할 수 있으나 pharmacist review가 필요하고 미검토 final verification 권한을 break 때문에 얻지 않는다. D는 거짓이다.')],
 'B를 지지한다. break 동안 새 조제약과 사전 검토 refill의 인계가 다른 실제 pickup 상황으로 재작성하고 premises 조건을 유지한다.')
add('MA-EXP-0190',['C'],'Case B의 45분 제안은 30분/6시간 상한을 넘는다. C가 맞고 sole pharmacist의 premises 이탈·8시간 rest 대체·staff final verification 부여는 각각 틀리다. 원해설은 세 법적 경계를 혼동하지 않는다.',[
 O(F,'cmr9','247 CMR 9.19(16)(a), (17)(a)','single pharmacist break 경로는 pharmacist가 premises에 남는 조건이다. 약국을 열어두고 premises를 떠나도 된다는 A는 거짓이다.'),
 O(F,'cmr9','247 CMR 9.01(17)','ordinary meal break는 extended practice 뒤 필요한 연속 8시간 rest를 충족하지 않는다. 예외를 주장하려면 extenuating circumstance와 최소 초과·기록 조건이 필요하다.'),
 O(T,'cmr9','247 CMR 9.19(17)(a)','단독 약사의 temporary absence는 6시간당 30분을 넘을 수 없다. C가 45분 제안을 교정한다.'),
 O(F,'cmr9','247 CMR 9.19(17)(b)–(c)','break가 staff의 scope를 넓히지 않는다. nondiscretionary work도 복귀 후 review 대상이며 unreviewed pharmacist final verification 권한은 생기지 않는다.')],
 'C를 지지하되 연속 근무 시작·break 분량·검토된 처방 여부를 가진 단일 사건으로 재작성한다. 이 문항의 휴식 경로를 비거주 pharmacy에 일반화하지 않는다.')
add('MA-EXP-0191',['A','B','C','D'],'네 SATA 문장을 각각 법문과 대조해 모두 참으로 계산했다. 특히 D는 extenuating exception을 명시한 일반 rest 규칙이고 A의 임시 부재와 별도다. 원해설은 이 차이를 정확히 설명하지만 반복 family의 all-true 변형 자체는 현실성 문제다.',[
 O(T,'cmr9','247 CMR 9.19(17)(a)','ordinary temporary absence는 6시간당 30분 이하라는 A가 참이다. 45분 제안은 이 상한을 넘는다.'),
 O(T,'cmr9','247 CMR 9.19(17)(a)','prescription area를 잠시 벗어나는 허용과 premises를 떠나는 것은 다르다. pharmacist는 premises에 남는다.'),
 O(T,'cmr9','247 CMR 9.19(17)(b)–(c)','support staff는 nondiscretionary duties를 수행할 뿐 break가 final pharmacist verification 권한을 이전하지 않는다. C는 참이다.'),
 O(T,'cmr9','247 CMR 9.01(17)','24시간 중 12시간을 넘겨 practice하기 전 연속 8시간 rest가 원칙이고, 환자 최선이익의 extenuating circumstance에는 최소 초과와 사유 기록이 필요하다. D는 해당 documented exception을 남겨 옳다.')],
 '정확 조합 A,B,C,D를 유지하며 all-true 사실을 숨기기 위한 기계적 반전은 하지 않는다. 한 pharmacist의 시간표와 실제 pickup 업무를 연결하는 새로운 판단 사례로 대체한다.')
add('MA-EXP-0192',['D'],'INCORRECT를 선택하므로 일반 meal break가 8시간 연속 rest를 대신한다는 D가 정답이다. A·B·C는 각각 premises,30분/6시간,final verification scope를 정확히 설명한다. 원해설도 이 극성을 유지한다.',[
 O(T,'cmr9','247 CMR 9.19(17)(a)','permitted area absence가 premises 이탈을 허용하지 않는다는 A는 참이므로 오류가 아니다.'),
 O(T,'cmr9','247 CMR 9.19(17)(a)','30분/6시간 상한을 제시한 B는 참이다. 단독 약사의 ordinary temporary-absence 경로에 한정한다.'),
 O(T,'cmr9','247 CMR 9.19(17)(b)–(c)','break로 staff에게 pharmacist final verification 권한이 생기지 않는다. C는 참이다.'),
 O(F,'cmr9','247 CMR 9.01(17)','30분 정도의 일반 식사휴식과 연속 8시간 rest는 별도다. extended practice의 rest 요건을 meal break가 충족한다는 D는 거짓이다.')],
 '오류 D를 보존한다. 실제 근무 누적시간·8시간 미휴식·환자상 예외 기록을 가진 사례로 교체해 단순 30분과 8시간 비교를 넘는 판단을 요구한다.')
# MOR11
add('MA-EXP-0193',['A'],'법정 Board 구성은 Massachusetts 주민 13명의 governor appointment이고 8명 pharmacist 외 5개 별도 seat가 있다. vacancy는 법정 배분을 변경하지 않는다. 원core와 모든 오답 교정은 현행 §22(a),(j),(n)에 맞는다.',[
 O(T,'c13s22','M.G.L. c.13 §22(a)','governor가 13명을 appoint하고 members는 Commonwealth 주민이다. pharmacy owner election이 아니므로 A가 Case A를 교정한다.'),
 O(F,'c13s22','M.G.L. c.13 §22(a), (j)','pharmacy technician 1석이 법정 구성에 포함되어 있다. 회의 참석만 가능하고 seat를 차지할 수 없다는 B는 거짓이다.'),
 O(F,'c13s22','M.G.L. c.13 §22(a), (n)','현재 occupied seats 수가 법정 13석 및 분류를 영구 재정의하지 않는다. 결원이나 holdover는 법정 allocation 변경이 아니다.'),
 O(F,'c13s22','M.G.L. c.13 §22(a)','13석 전부 pharmacist가 아니라 8 registered pharmacist와 technician/public/physician/nurse/patient-safety expert 각 1명이다. D는 거짓이다.')],
 'A의 법적 사실은 보존하되 review group의 암기 확인 대신 특정 seat에 실제 후보가 자격을 갖추는지 심사하는 새 상황으로 작성한다.')
add('MA-EXP-0194',['B'],'Case B의 실제 재직 수와 statutory allocation을 구분하면 B가 옳다. 원해설의 13명·governor·8 pharmacist·technician seat는 모두 §22(a)에 맞지만 현재 vacant seat 사실을 주지 않는 chart 준비는 실질 reasoning이 약하다.',[
 O(F,'c13s22','M.G.L. c.13 §22(a), (j)','technician이 statutory Board seat를 차지할 수 없다는 A는 technician 1석 및 경험 자격 조항에 반한다.'),
 O(T,'c13s22','M.G.L. c.13 §22(a), (n)','현재 vacancy는 13명 법정 구성과 seat allocation을 변경하지 않는다. B는 현원과 정원을 정확히 구별한다.'),
 O(F,'c13s22','M.G.L. c.13 §22(a)','all 13 pharmacist라는 C는 8 pharmacist 외 다섯 종류 seat를 삭제하므로 거짓이다.'),
 O(F,'c13s22','M.G.L. c.13 §22(a)','pharmacy owners가 13 pharmacists를 선출하는 구조가 아니라 governor가 13 residents를 appoint한다. D는 주체와 구성을 모두 틀렸다.')],
 'B는 유지할 수 있으나 실제 결원과 임명 후보의 setting을 준 구체적 행정 파일 검토로 바꾼다. 모호한 chart preparation만으로 별도 실전 사례를 세지 않는다.')
add('MA-EXP-0195',['B'],'SATA 각 명제를 대조하면 governor-appointed 13 residents인 B만 참이다. 13명 전부 pharmacist·technician 금지·현원에 따른 정원 재정의는 모두 거짓이다. 원해설의 한 개 선택 조합은 법적으로 맞다.',[
 O(F,'c13s22','M.G.L. c.13 §22(a)','13석 중 8석만 registered pharmacist다. A의 전석 pharmacist 주장은 법정 비약사 seat와 충돌한다.'),
 O(T,'c13s22','M.G.L. c.13 §22(a)','13 Massachusetts residents를 governor가 appoint한다. B는 이 문장의 주체·인원·거주 요건을 모두 맞춘다.'),
 O(F,'c13s22','M.G.L. c.13 §22(a), (j)','technician은 법정 구성 1석이고 별도 경험 자격이 있다. 참석만 가능하다는 C는 거짓이다.'),
 O(F,'c13s22','M.G.L. c.13 §22(a), (n)','현원이 줄어도 statute의 정원과 배분은 바뀌지 않는다. D의 permanent redefinition은 근거가 없다.')],
 'B만의 조합을 기록한다. 다른 세 변형과 같은 네 명제의 순서·극성 전환을 중단하고 실제 후보의 statutory seat 적격성 결정을 묻는 새 item으로 대체한다.')
add('MA-EXP-0196',['C'],'INCORRECT 극성에서 technician seat 부정을 담은 C만 거짓이다. 13 governor-appointed residents·8 pharmacist seats·vacancy 불변이라는 A,B,D는 참이다. 원해설은 극성을 정확히 분리한다.',[
 O(T,'c13s22','M.G.L. c.13 §22(a)','13 Massachusetts resident members를 governor가 appoint한다는 A는 참이다.'),
 O(T,'c13s22','M.G.L. c.13 §22(a)–(b)','8 registered pharmacist seats가 명시되어 B는 참이다. 나머지 5석까지 pharmacist로 제한하는 의미는 아니다.'),
 O(F,'c13s22','M.G.L. c.13 §22(a), (j)','technician 1석이 명시되어 있다. seat를 occupy할 수 없다는 C가 오류 선택이다.'),
 O(T,'c13s22','M.G.L. c.13 §22(a), (n)','current vacancies가 statutory allocation을 바꾸지 않는다는 D는 참이다. 현원 조사와 법정 구성은 별도다.')],
 '오류 C는 법적으로 유지한다. 실제 technician 후보의 실무경력과 현재 업무 여부를 평가하는 새 사례로 바꾸고 review-group 암기 형식을 반복하지 않는다.')
# MOR12
add('MA-EXP-0197',['D'],'두 연속 term 이후 즉시 세 번째 appointment는 안 된다. 원해설은 3년 term·두 연속 상한·한 term 이상 공백과 holdover를 모두 구별하므로 D의 service limit는 새 임기를 뜻하는 범위에서 맞다. 계속 office 유지까지 금지한다는 뜻으로 확대하지 않는다.',[
 O(F,'c13s22','M.G.L. c.13 §22(n)','term 만료자는 successor가 appointed될 때까지 계속 office에 남는다. 만료 즉시 모든 seat가 legally vacant라는 A는 거짓이다.'),
 O(F,'c13s22','M.G.L. c.13 §22(c)–(i)','independent·chain 각 2와 hospital·LTC·sterile·academic 등 지정 allocation이 있다. 하나 setting으로 무시해 채운다는 B는 거짓이다.'),
 O(F,'c13s22','M.G.L. c.13 §22(b), (c)–(h)','과거 어느 때든 license를 보유했다는 사실만으로 충분하지 않다. 7 consecutive years practice와 appointment/reappointment 때의 현재 Massachusetts practice 및 seat별 자격이 필요하다.'),
 O(T,'c13s22','M.G.L. c.13 §22(n)','3년 term 연속 최대 2회이고 최대 횟수 뒤 재임명은 적어도 1 term 비재직 후 가능하다. D는 Case A의 새 appointment를 제한하는 규칙이며 holdover는 별도다.')],
 'D를 지지하되 service limit 표현을 새 연속 appointment 제한으로 명료화한다. successor 유무와 종료일을 주는 실제 reappointment 파일로 재작성한다.')
add('MA-EXP-0198',['A'],'Case B의 past license만으로는 pharmacist-member 자격이 충족되지 않는다. 현재 practice와 최소 연속 경력, setting별 요건을 확인해야 한다. A는 맞지만 specified pathway라는 추상어 대신 구체적 후보 경력을 주어야 한다.',[
 O(T,'c13s22','M.G.L. c.13 §22(b); (c)–(h)','8 pharmacist members는 최소 7 consecutive years 경험 및 appointment/reappointment 때 Commonwealth practice 고용이 필요하고 seat별 조건도 있다. A의 추가 자격 요구는 참이다.'),
 O(F,'c13s22','M.G.L. c.13 §22(n)','term은 3년이나 연속 두 term 상한이 있다. unlimited consecutive terms라는 B는 거짓이다.'),
 O(F,'c13s22','M.G.L. c.13 §22(c)–(i)','pharmacist seats는 지정 settings에 배분되어 있다. 모든 seat를 한 setting에서 채워도 된다는 C는 거짓이다.'),
 O(F,'c13s22','M.G.L. c.13 §22(n)','successor가 아직 없으면 만료 member는 계속 office에 남는다. 즉시 모든 seat가 legally vacant라는 D는 holdover와 충돌한다.')],
 'A를 지지한다. past license만 가진 후보가 실제 최근 practice·연속 7년·setting 중 무엇을 충족하는지 수치·날짜가 있는 새 임명 사례로 바꾼다.')
add('MA-EXP-0199',['A','D'],'SATA의 A와 D는 모순이 아니다. A는 새 연속 임기 상한과 재임명 공백이고 D는 successor까지 기존 office를 유지하는 holdover다. B의 setting 무시와 C의 과거 license만 충분은 거짓이므로 원키 A,D가 지지된다.',[
 O(T,'c13s22','M.G.L. c.13 §22(n)','연속 term 최대 2회 후 새 appointment에는 적어도 1 term 비재직이 필요하다. A는 새 임기 기준으로 참이며 successor까지 holdover는 이를 새 term으로 만들지 않는다.'),
 O(F,'c13s22','M.G.L. c.13 §22(c)–(i)','지정 setting allocation을 무시해 모든 pharmacist seats를 한 setting으로 채울 수 없다. B는 거짓이다.'),
 O(F,'c13s22','M.G.L. c.13 §22(b), (c)–(h)','과거 pharmacist license만으로 경력·현재 Massachusetts practice·seat 자격이 자동 충족되지 않는다. C는 거짓이다.'),
 O(T,'c13s22','M.G.L. c.13 §22(n)','만료 member가 successor appointment까지 계속 office에 있을 수 있다. D의 holdover는 A의 새 연속 term 제한과 구별되는 참 명제다.')],
 'A,D의 조합을 유지한다. 새 appointment와 holdover를 명확히 다른 행위로 쓰고 actual successor 부재·재임명 요청일이 있는 단일 상황으로 대체한다.')
add('MA-EXP-0200',['B'],'INCORRECT 문항에서 모든 seat가 term 종료 즉시 legally vacant라는 B가 거짓이다. A의 setting allocation,C의 경력·현재 practice,D의 새 term 상한은 참이다. 원해설은 한 term 공백과 holdover를 함께 설명하여 법적 차이를 보존한다.',[
 O(T,'c13s22','M.G.L. c.13 §22(c)–(i)','pharmacist seats가 specified practice settings에 배분된다는 A는 참이다.'),
 O(F,'c13s22','M.G.L. c.13 §22(n)','term 종료 후 successor가 appointed될 때까지 member는 계속 office에 남는다. every seat instantly vacant라는 B가 오류다.'),
 O(T,'c13s22','M.G.L. c.13 §22(b)','minimum 7 consecutive years experience와 appointment/reappointment 시 Commonwealth의 현재 practice 고용 조건이 있다. C는 참이다.'),
 O(T,'c13s22','M.G.L. c.13 §22(n)','연속 두 term과 최대 횟수 뒤 적어도 한 term 비재직 후 재임명이라는 D는 새 term 제한으로 참이다. holdover를 third appointment로 세지 않는다.')],
 '오류 B를 기록한다. 현재 기본 문항 RW0074처럼 successor 부재와 proposed reappointment라는 실제 결정이 필요한 새 사건을 만들고 기존 wording을 단순 재배열하지 않는다.')
assert set(SPECS)==set(assignment['question_hashes'])
reviewed_at=now()
versions={
'c13s22':('M.G.L. c.13 §22, Board membership and terms','OFFICIAL_STATE_STATUTE','Current Massachusetts General Laws online text on review date',None,'현재 법령 본문에는 개별 개정/최초 시행일이 표시되지 않아 그 날짜는 미확정이다. current posted text를 현 시점의 임명·재임명 사실에 적용했으며 prospective amendment나 당시 과거 law를 추정하지 않았다.','§22(a)–(p)'),
'cmr6':('247 CMR 6.00 Licensure of Pharmacies','OFFICIAL_STATE_REGULATION','Mass. Register #1546, 2025-04-25 compilation; regulation landing page Date 04/25/2025',None,'2025-04-25 현재 게시 compilation과 그 본문을 확인했다. 이 검토의 6.10–6.16 각 조항의 최초 시행일은 이 문서에서 특정되지 않아 미확정이며 게시일을 시행일로 바꾸지 않았다. 현재 거래에 적용하는 게시 원문은 확보했다.','6.10(1)–(2); 6.11; 6.12; 6.13; 6.14; 6.15; 6.16'),
'cmr9':('247 CMR 9.00 Professional Practice Standards','OFFICIAL_STATE_REGULATION','2024-12-06 compilation; regulation landing page Date 12/06/2024',None,'PDF와 regulation page의 2024-12-06 게시본을 확인했다. 각 검토 조항의 최초 시행일을 별도로 확인하지 못했으며 그 사실을 숨기지 않는다. 게시본의 현행 의무·예외를 현재 사건에 적용했다.','9.01(17); 9.19(16)–(17), (21), (23)–(24); 9.24; 9.25'),
'cmr10':('247 CMR 10.00 Disciplinary Proceedings','OFFICIAL_STATE_REGULATION','Mass. Register #1546, 2025-04-25; PDF footer 4/25/25 (Effective 1/9/25)','2025-01-09','current PDF footer는 4/25/25 (Effective 1/9/25)라고 표시한다. 그 compilation/version 효력 표시는 확인했으며 모든 변경 전 조항이 1/9/25에 처음 생겼다고 추정하지 않는다.','10.01–10.08, especially 10.03(1)(g),(k), 10.06(2)–(6), 10.07, 10.08'),
'cmr14':('247 CMR 14.00 Petition for Waiver','OFFICIAL_STATE_REGULATION','Mass. Register #1348, Dated 2017-09-22; landing page Date 09/22/2017',None,'current PDF와 2017-09-22 게시 버전을 확인했다. 게시 날짜와 최초 시행일은 구분한다. 14.01(5)의 명시적 2013-06-30 경계 및 grant 5주년 만료를 직접 적용했으며 retrospective waiver rule을 새로 추정하지 않았다.','14.01(1)–(5)'),
'policy2022-02':('Board Policy 2022-02 Extended Absence or Departure of MOR or Designated PIC','OFFICIAL_BOARD_POLICY','Adopted 2022-03-03; revised 2022-10-13, 2023-03-02, 2024-08-28, 2025-05-01','2025-05-01','현재 PDF의 revised 5/1/25 표기를 확인했다. 정책은 interim absence/departure를 설명하는 보조 범위이며 6.10의 permanent change application·attestation을 대체하는 법적 근거로 쓰지 않았다.','I–II; used only as scope comparison'),
'federal1301-52':('21 CFR 1301.52 Termination and transfer of registration; discontinuance of business','OFFICIAL_FEDERAL_REGULATION','Current government eCFR section retrieved on review date',None,'eCFR은 정부의 current editorial compilation이고 공식 인쇄 legal edition과 구별된다고 스스로 표시한다. 조문의 historical effective date를 따로 확정하지 못했으며 review date 현재 section text와 source note를 보존했다. Massachusetts Board notice와 DEA notice를 합치지 않았다.','1301.52(a)–(e), especially (b), (d), (e)(1)–(2)'),
'federal1304-11':('21 CFR 1304.11 Inventory requirements','OFFICIAL_FEDERAL_REGULATION','Current government eCFR section retrieved on review date',None,'현재 eCFR 본문을 확인했다. 개별 paragraph의 최초 효력일은 별도 미확정이며 current requirement의 complete and accurate inventory와 date 조건만 사용했다. federal schedule와 Massachusetts VI를 혼동하지 않는다.','1304.11(a)–(c); (e)(6)')}
sources=[]
for sid,(title,typ,version,effective,limitation,scope) in versions.items():
 mp=BASE/(sid+'-retrieval.json');meta=json.loads(mp.read_text())
 meta.update(read_at=reviewed_at,read_scope=scope,read_method='Assistant directly read retained extracted primary text in this fresh session; no prior reviewer legal conclusion used',document_identity_confirmed=True,legal_payload_confirmed=True,document_title=title,document_version=version,effective_date=effective,effective_date_limit_ko=limitation)
 write(mp,meta)
 sources.append({'source_id':sid,'authority':title,'source_type':typ,'official_url':meta['official_url'],'citation_url':meta['official_url'],'exact_section':scope,'law_checked_date':'2026-11-04','review_date':'2026-11-04','retrieved_at':meta['retrieved_at'],'read_at':reviewed_at,'timezone':'Etc/UTC','http_status':meta['http_status'],'document_identity_confirmed':True,'document_title':title,'document_version':version,'effective_date':effective,'effective_date_limit_ko':limitation,'raw_path':meta['raw_path'],'raw_sha256':meta['raw_sha256'],'evidence_path':meta['raw_path'],'evidence_sha256':meta['raw_sha256'],'text_evidence_path':meta['text_evidence_path'],'text_sha256':meta['text_sha256'],'metadata_path':str(mp),'metadata_sha256':sha(mp),'public_raw_redistribution':True,'used_as_legal_authority':sid!='policy2022-02','read_scope':scope})
# Current government regulation landing pages establish compilation identity, not substantive law by themselves.
for sid in ['cmr6-page','cmr9-page','cmr10-page','cmr14-page']:
 mp=BASE/(sid+'-retrieval.json');m=json.loads(mp.read_text());m.update(read_at=reviewed_at,read_scope='Regulation title, Date, Board organization and document download identification only',document_identity_confirmed=True,is_legal_evidence=False);write(mp,m)
 sources.append({'source_id':sid,'authority':sid+' government regulation landing page','source_type':'OFFICIAL_STATE_PUBLICATION_METADATA','official_url':m['official_url'],'citation_url':m['official_url'],'exact_section':'Regulation heading / Date / Board of Registration in Pharmacy','law_checked_date':'2026-11-04','retrieved_at':m['retrieved_at'],'read_at':reviewed_at,'timezone':'Etc/UTC','http_status':m['http_status'],'raw_path':m['raw_path'],'raw_sha256':m['raw_sha256'],'evidence_path':m['raw_path'],'evidence_sha256':m['raw_sha256'],'text_evidence_path':m['text_evidence_path'],'text_sha256':m['text_sha256'],'metadata_path':str(mp),'metadata_sha256':sha(mp),'used_as_legal_authority':False,'public_raw_redistribution':True,'finding_ko':'정상 government regulation page의 title/date를 확인했다. 이 metadata만으로 문항의 정답을 판단하지 않았다.'})
style_memo={'auditor':'GPT','auditor_instance':'GPT:/root/independent_wave10_d:20261104','read_at':reviewed_at,'review_date':'2026-11-04','timezone':'Etc/UTC','copyright_boundary_ko':'NABP의 보호된 exam/recalled/Pre-MPJE/commercial 문항은 접근·복제하지 않았다. 허용 public 안내의 URL/SHA와 자체 memo만 repo에 남긴다. 공개 sample의 문항 wording을 repo·보고서에 복제하지 않았고 법적 정답의 authority로 쓰지 않았다.','profile':{'path':'data/exam_style/mpje_style_profile.json','raw_sha256':sha('data/exam_style/mpje_style_profile.json'),'profile_id':'MPJE-MA-PRE2027','content_hash':'293be8fdcd39af2255a22a0423b7123d5cfcf7c0e6c561872eb0ef04e745015c'},'blueprint':{'path':'data/blueprint.json','raw_sha256':sha('data/blueprint.json'),'content_hash':'4d5e3acaccaa562b16e53740e802a3a05ada5900a09a65585f3e6f94d7827a86'},'observations_ko':['NABP current Take the MPJE 안내의 본문에서 2.5시간·120 computer-based questions·adaptive selected response를 확인했다. 난도나 실제 시험 문항의 표현을 인증하는 자료는 아니다.','Competency 페이지는 2027-03-01부터 바뀐 outline 사용을 안내한다. 현재 pre-2027 profile의 영역 22/33/24/21과 일치하는 공개 비율 및 국가/주법을 prevailing state law로 적용한다는 구조를 확인했다.','공개 sample PDF는 한 페이지 문서의 public item-format 표제·선택 지시의 존재만 확인했다. SBA/multiple response/ordered response 형식 참고이며 문항 content를 독립 법규 근거나 보호된 시험의 유사성 증거로 평가하지 않았다.','근접 bank 문항은 자체 visible projection의 실제 stem과 전 options를 직접 읽었다. 문자열 유사도는 탐색 후보에만 사용했고 final realism은 실제 역할·행위·법적 결정·distractor plausibility·answer cue·반복을 개별 평가했다.'],'source_reads':[]}
for sid in ['nabp-format','nabp-competency','nabp-sample']:
 mp=BASE/(sid+'-retrieval.json');m=json.loads(mp.read_text());m.update(read_at=reviewed_at,used_as_legal_authority=False,public_evidence_mode='URL/SHA/self-authored memo only; copyrighted raw/text not retained in repository',public_raw_redistribution=False,read_scope='Public format headings/instructions only; no question wording reproduced' if sid=='nabp-sample' else 'Public exam format / current competency outline and pre-2027 transition notice')
 # Do not carry temporary protected-payload locations forward as public evidence paths.
 m.pop('temporary_raw_path',None);m.pop('temporary_text_path',None);m.pop('text_sha256',None);write(mp,m)
 style_memo['source_reads'].append({k:m[k] for k in ('source_id','official_url','final_url','http_status','retrieved_at','read_at','raw_sha256','read_scope')})
write(BASE/'public-style-memo.json',style_memo)
for sid in ['nabp-format','nabp-competency','nabp-sample']:
 mp=BASE/(sid+'-retrieval.json');m=json.loads(mp.read_text())
 sources.append({'source_id':sid,'authority':'NABP public format reference: '+sid,'source_type':'PUBLIC_OFFICIAL_FORMAT_ONLY','official_url':m['official_url'],'citation_url':m['official_url'],'exact_section':m['read_scope'],'law_checked_date':None,'retrieved_at':m['retrieved_at'],'read_at':m['read_at'],'http_status':m['http_status'],'raw_sha256':m['raw_sha256'],'evidence_path':str(BASE/'public-style-memo.json'),'evidence_sha256':sha(BASE/'public-style-memo.json'),'metadata_path':str(mp),'metadata_sha256':sha(mp),'used_as_legal_authority':False,'public_raw_redistribution':False,'public_evidence_mode':m['public_evidence_mode']})
source_index={s['source_id']:s for s in sources}
write(BASE/'source-index.json',source_index)
# Actual records whose original option text was read as comparison candidates. Bank-internal conclusions and keys are absent from the projection.
near=json.loads((BASE/'nearby-visible-candidates.json').read_text())
topic_near=json.loads((BASE/'topic-nearby-visible-input.json').read_text())
read_bindings=[{'path':str(BASE/'nearby-visible-candidates.json'),'raw_sha256':sha(BASE/'nearby-visible-candidates.json')},{'path':str(BASE/'topic-nearby-visible-input.json'),'raw_sha256':sha(BASE/'topic-nearby-visible-input.json')},{'path':str(packet_path),'raw_sha256':sha(packet_path)}]
nearby_by_rw={'MA-RW-0073':['MA-EXP-0193','MA-EXP-0195'],'MA-RW-0074':['MA-EXP-0197','MA-EXP-0199'],'MA-RW-0075':['MA-EXP-0201','MA-EXP-0204'],'MA-RW-0076':['MA-EXP-0205'],'MA-RW-0077':['MA-EXP-0209'],'MA-RW-0078':['MA-EXP-0213'],'MA-RW-0079':['MA-EXP-0217'],'MA-RW-0080':['MA-EXP-0221']}
family_realism={
'MOR05':('incoming/outgoing MOR의 실제 handover는 실무적이다. 하지만 Case A/B가 모든 네 변형에 동일하고, A-only 또는 B-only 질문에도 나머지 case와 관계없는 false options를 붙인다. only/alone/discard 같은 과도한 행위와 correct option의 specified/applicable 자격어가 정답을 쉽게 드러낸다. scope·서명·보존을 결합하는 소재는 유용하나 네 개 독립 상황의 새 coverage로 볼 수 없다.', 'inventory의 scope 또는 application omission을 실제 date·서명·문서로 판단하는 한 사건'),
'MOR06':('소유권 이전·상호 변경은 현실적인 운영 주제다. 그러나 only operating name과 new owner라는 Case B의 서술이 사건을 혼합하고 동일 두 case·네 규칙의 순서와 극성만 바뀐다. 자동 이전·all stock/file procedures라는 과도한 오답이 law 적용 없이 제거될 수 있으며 all-true SATA도 앞 변형의 key 회상에 의존한다.', '동일 owner의 name-only 변경 또는 실제 buyer의 advance license application 중 하나'),
'MOR07':('공사와 relocation의 사전 approval은 현실적이지만 동일 Case A/B가 네 번 반복되고 별개의 secondary-control 행위는 stem에 없다. generic applicable/specified 문구와 자동 허가·사후 신청·주소만 같으면 면제라는 극단적 오답이 cue다. 실제 시설 종류·공사 범위·approval일이 있어야 자연스러운 결정이 된다.', 'license category와 공사 또는 이동 날짜가 있는 승인 전 행위 결정'),
'MOR08':('폐업의 환자 continuity는 실무성이 높다. 그러나 resident만으로 institutional sterile 예외를 배제하지 못하고 반복 Case A/B는 final-day sign과 all provisions identical 같은 과도한 오답에 의존한다. 선행 형식의 정답이 다음 SATA/INCORRECT에 그대로 노출되어 독립 실전 사례 네 개로 볼 수 없다.', '일반 resident retail의 환자 notice·file transfer 날짜가 특정된 폐업 사건'),
'MOR09':('closure stock transfer와 MOR inventory는 실제 업무다. 하지만 같은 수주 뒤 estimate·leftover bottles·discard의 Case A/B가 네 번 재사용되어 다른 변형을 본 뒤 답을 회상하기 쉽다. only receiving pharmacy와 routine renewal까지 defer 같은 오답이 지나치게 약하다. 실제 양 MOR의 서명·10일 제출·기록 인계를 자연스럽게 묻는 새 상황이 필요하다.', 'transfer 당일 계수·서명 및 이후 Board attestation의 실제 기록 검토'),
'MOR10':('단독 약사의 break와 support staff 업무는 실무 소재다. 그러나 동일 두 case에 30분·45분·8시간을 네 형식으로만 돌리고, final verification 권한 획득이라는 극단적 오답을 반복한다. 실제 환자 pickup·사전 pharmacist 검토 여부 없이 premises와 숫자를 회상하는 비중이 크다.', 'break 동안 사전 검토 refill 또는 새 처방 pickup과 실제 근무시간의 판단'),
'MOR11':('review group이 membership chart를 만든다는 설정은 실제 pharmacy action보다 statute 회상에 가깝다. 13 pharmacists/owner election/technician 금지 같은 극단적 오답과 동일 case 반복이 정답 cue다. 임명 후보에 특정 seat 요건을 적용하는 사례가 더 적절하다.', '실제 Board seat candidate의 setting·경력·현재 practice 적격성 판단'),
'MOR12':('임기·holdover·후보 자격은 유용한 jurisprudence 주제다. 그러나 actual successor·임명일·후보 경력을 주지 않고 같은 두 추상 case와 specified pathway 문장을 네 형식으로 재사용한다. all/automatically/unlimited/every 같은 약한 오답과 앞 변형의 정답 재노출이 독립적인 reasoning을 줄인다.', 'successor 부재 또는 구체적 후보 경력의 새 appointment 결정')}
# Individual focus notes distinguish each actual rotation and polarity.
individual_realism={
'MA-EXP-0169':'Case A만 물어 Case B를 쓰지 않으며 C의 상세 schedule 범위가 다른 과도한 오답과 대조된다.',
'MA-EXP-0170':'Case B만 묻지만 C의 Case A schedule과 A의 전체 application을 끼워 넣는다. D의 applicable conditions가 실제 결정을 추상화한다.',
'MA-EXP-0171':'세 참 명제 A,B,D는 바로 앞 두 SBA에서 노출된 결론이며 새 사실이 없다. C의 폐기 문장만 제거하면 된다.',
'MA-EXP-0172':'동일 inventory 내용의 polarity만 INCORRECT로 바뀌어 A의 alone이 강한 cue이고 새 판단 사건이 없다.',
'MA-EXP-0173':'Case A의 closing-day notice 판단에는 Case B가 필요 없고 B의 정밀한 14일이 극단적 자동 충족 오답과 대조된다.',
'MA-EXP-0174':'Case B의 only name/new owner 혼합을 해결하지 않은 채 C의 고립된 notice 규칙을 회상하게 한다.',
'MA-EXP-0175':'A,B,C,D가 모두 앞 SBA의 교정문 그대로여서 all-true 조합도 새 transaction facts 없이 재사용된다.',
'MA-EXP-0176':'D의 all stock and prescription procedures 자동 충족이 유일한 과도한 명제여서 동일 사례의 오류형 변형이다.',
'MA-EXP-0177':'A-only 판단과 무관한 relocation Case B 및 stem 밖 secondary control을 distractor로만 사용한다.',
'MA-EXP-0178':'B-only 판단에서 Case A 공사는 활용되지 않는다. timely application과 automatic permission의 단순 대비가 중심이다.',
'MA-EXP-0179':'SATA라고 하지만 앞의 거짓 문장 세 개와 이미 배운 90일 rule 한 개를 조합한다. secondary-control 실제 행위는 없다.',
'MA-EXP-0180':'주소 불변이면 exempt라는 C만 절대적 오답이며 앞 remodeling/relocation 변형을 본 뒤 key를 재인식하게 된다.',
'MA-EXP-0181':'D는 일반 advance notice 원칙이고 다른 옵션은 every/limited/all이라는 약한 절대어다. facility 예외를 stem이 고정하지 않는다.',
'MA-EXP-0182':'A에 90일/14일 정밀 규칙을 몰고 다른 옵션은 all/every/replaces로 쉽게 배제한다. 실제 notice 날짜는 없다.',
'MA-EXP-0183':'A,C는 앞 SBA 교정의 반복이고 B,D의 제한·전면 동일 문구는 과도하다. 환자 transfer의 실제 시점을 묻지 않는다.',
'MA-EXP-0184':'B의 every provision identical이 눈에 띄는 오류 cue이고 앞 변형의 참 문장을 나머지 보기로 옮겼다. facility ambiguity도 남는다.',
'MA-EXP-0185':'Case A의 estimate 문제에 비해 D의 only receiving과 A의 next renewal은 매우 약하다. Case B는 정답에 필요 없다.',
'MA-EXP-0186':'D는 Case B stock 보유 문제를 고치지만 앞 C를 A로 뒤집고 동일 서명을 다시 회상한다.',
'MA-EXP-0187':'A,B,C는 앞 두 SBA의 교정문이며 새 schedule·날짜·인계 조건이 없다. D만 극단적 잔여 보유 문장이다.',
'MA-EXP-0188':'A의 renewal까지 일괄 defer가 분명한 false cue이며 나머지는 같은 family의 이미 노출된 문장이다.',
'MA-EXP-0189':'Case A에 맞는 B와 완전히 다른 8시간 rest를 대비하고 실제 환자 medication release 행위는 주지 않는다.',
'MA-EXP-0190':'Case B에 45분을 미리 제시해 C의 30분으로 고치는 숫자 비교가 중심이고 독립 scope 상황이 없다.',
'MA-EXP-0191':'네 option 모두 앞 설명의 참 문장으로서 all-true를 결정할 새로운 practice facts가 없다.',
'MA-EXP-0192':'D의 짧은 meal break=8시간 rest는 상식상도 약한 오답이며 단순 INCORRECT 회전이다.',
'MA-EXP-0193':'review group의 명백히 틀린 owner election 가정만 교정하는 문항이고 개별 후보의 seat 적격성은 묻지 않는다.',
'MA-EXP-0194':'실제 현원·결원 수조차 주지 않아 B의 vacancy 일반론을 고른다. 나머지 기술자 금지·13 pharmacist 오답은 반복된다.',
'MA-EXP-0195':'SATA 하나 정답 B는 앞 SBA A의 동일 사실이고 다른 세 명제는 모두 극단적이다.',
'MA-EXP-0196':'C의 technician seat 부정만 찾으면 되며 새 membership chart나 후보 사실 없이 polarity를 전환했다.',
'MA-EXP-0197':'Case A는 second consecutive term 사실만 있고 successor 유무는 없어 statutory limit 회상에 그친다.',
'MA-EXP-0198':'Case B의 actual practice years·고용 상태를 주지 않고 A의 specified pathway 일반론을 고르게 한다.',
'MA-EXP-0199':'A,D의 term/holdover 구별 소재는 유용하나 실제 임명·successor 날짜가 없고 반복된 네 명제만 SATA로 묶는다.',
'MA-EXP-0200':'B의 every seat immediately vacant를 오류로 반전했을 뿐 다른 변형과 같은 case·scope·정답 내용을 재사용한다.'}
records=[]
for q in packet['records']:
 qid=q['question_id'];s=SPECS[qid];opts=s['options'];assert len(opts)==len(q['choices'])
 incorrect='INCORRECT' in q['stem'];truth_expected=[];option_reviews=[]
 for c,o in zip(q['choices'],opts):
  a=copy.deepcopy(source_index[o['sid']]);a['exact_section']=o['section'].split('; 21 CFR')[0]
  if o['sid'].startswith('federal'):
   a['citation_url']=a['official_url']+'#p-'+('1301.52' if o['sid']=='federal1301-52' else '1304.11')
  auth=[a]
  if (qid,c['id']) in {('MA-EXP-0173','A'),('MA-EXP-0174','B'),('MA-EXP-0175','B'),('MA-EXP-0176','D'),('MA-EXP-0185','C'),('MA-EXP-0186','A'),('MA-EXP-0187','B'),('MA-EXP-0188','D')}:
   f=copy.deepcopy(source_index['federal1301-52']);f['exact_section']='21 CFR 1301.52(b), (d), (e)(1)–(2)';f['citation_url']=f['official_url']+'#p-1301.52(e)';auth.append(f)
   if qid>='MA-EXP-0185':
    f=copy.deepcopy(source_index['federal1304-11']);f['exact_section']='21 CFR 1304.11(a)';f['citation_url']=f['official_url']+'#p-1304.11(a)';auth.append(f)
  if isinstance(o['truth'],bool) and o['truth']!=incorrect:truth_expected.append(c['id'])
  choice_rationale=q['explanation']['choice_analysis'][c['id']]
  option_reviews.append({'choice_id':c['id'],'text':c['text'],'statement_truth':'TRUE' if o['truth'] is True else 'FALSE' if o['truth'] is False else 'CONDITIONAL_ON_FACILITY_CLASS','support':'SUPPORTED_TRUE' if o['truth'] is True else 'CONTRADICTED_FALSE' if o['truth'] is False else 'AMBIGUOUS_APPLICATION_OF_VERIFIED_RULE','selected_in_stored_key':c['id'] in q['correct_choice_ids'],'finding_ko':o['finding'],'authorities':auth,'existing_ko_rationale':choice_rationale,'existing_ko_rationale_review_ko':o['finding'],'explanation_assessment':'SCOPE_AMBIGUITY_NOT_RESOLVED' if o['truth']=='CONDITIONAL' else 'SUPPORTED_IN_STATED_RULE_SCOPE'})
 if s['key'] is not None:
  assert s['key']==truth_expected,(qid,s['key'],truth_expected)
  answer='YES' if s['key']==q['correct_choice_ids'] else 'NO'
 else:answer='AMBIGUOUS'
 family={'DISC01':'MOR11','DISC02':'MOR12'}.get(q['family_id'],q['family_id']);near_ids=nearby_by_rw[qid] if qid.startswith('MA-RW') else [z['question_id'] for z in next(r for r in near['records'] if r['target']==qid)['nearest_candidates']]
 if s['realism']=='PASS':rfind=s['realism_finding']
 else:rfind=family_realism[family][0]+' '+individual_realism[qid]
 allauth={json.dumps(a,sort_keys=True,ensure_ascii=False):a for x in option_reviews for a in x['authorities']}
 legal={'existing_answer_correct':answer,'verdict':s['legal'],'stored_choice_ids':q['correct_choice_ids'],'expected_choice_ids':s['key'],'polarity':'SELECT_INCORRECT_SINGLE' if incorrect else 'SELECT_ALL_TRUE' if q['question_type']=='SATA' else 'SELECT_CORRECT_SINGLE','polarity_finding_ko':('거짓 명제를 고르는 INCORRECT를 별도 적용했다.' if incorrect else '모든 참 명제를 포함하는 정확 조합을 별도 계산했다.' if q['question_type']=='SATA' else '단일 참 명제와 지문이 지정한 Case의 연결을 확인했다.'),'finding_ko':s['overview'],'option_reviews':option_reviews,'authorities':list(allauth.values()),'existing_explanation_review':{'core_reasoning_read':q['explanation']['core_reasoning'],'core_finding_ko':s['overview'],'all_choice_rationales_read':True,'choice_review_ids':[c['id'] for c in q['choices']],'learning_boundary_read':q['explanation'].get('learning_boundary'),'learning_boundary_finding_ko':'작성자 출처 대조/편집 검토와 독립 감사가 다르다는 원문 경계를 확인했다. 이번 별도 세션의 검토도 canonical release credit는 0이다.' if qid.startswith('MA-RW') else '네 변형이 동일 두 사례와 네 판단을 공유한다는 원문 경계가 실제 stem·전 options 비교와 맞는다. 이 고지가 중복·약한 distractor·시설 범위 누락을 해결하는 것은 아니다.'},'blocker':None if s['legal']=='KEEP' else s['overview'],'state_federal_boundary_ko':'이 판단은 Massachusetts Board 구성·면허·discipline·운영 요건을 적용한다. 같은 숫자·정의의 연방 일반 규칙으로 대체하지 않았다.'}
 if qid in {'MA-EXP-0173','MA-EXP-0174','MA-EXP-0175','MA-EXP-0176','MA-EXP-0185','MA-EXP-0186','MA-EXP-0187','MA-EXP-0188'}:
  legal['state_federal_boundary_ko']='Massachusetts 6.11/6.14의 Board notice·license application·inventory attestation과 federal 1301.52의 DEA registration/stock transfer가 별도다. MA 14일 Board notice가 DEA 14일 notice를 자동 충족하지 않으며 business sale로 어느 절차도 자동 완료되지 않는다. VI 범위는 Massachusetts 규칙이다.'
 if s['key'] is None:
  legal['conditional_expected_choice_ids']={'ordinary_resident_drug_store_pharmacy':q['correct_choice_ids'],'institutional_sterile_compounding_pharmacy':'현재 지문의 intended patient-notice 의무를 적용할 수 없으므로 단일 key/조합을 확정하지 않음; 6.13(7) 범위를 명시해야 함'}
  legal['source_blocked']=False
 checks={'jurisprudence_reasoning':s['realism']=='PASS','plausible_pharmacy_practice':True if qid.startswith('MA-RW') or family not in {'MOR11','MOR12'} else False,'genuine_legal_confusion_distractors':s['realism']=='PASS','wording_does_not_supply_key':s['realism']=='PASS','reasoning_not_trivia':s['realism']=='PASS','rules_naturally_combined':s['realism']=='PASS','drug_context_appropriate_or_not_needed':True,'not_excessively_similar':s['realism']=='PASS','not_schedule_flashcard':True,'public_format_without_protected_copying':True}
 records.append({'question_id':qid,'record_sha256':assignment['question_hashes'][qid],'default_selected':q['default_selected'],'reviewed_at':reviewed_at,'review_date':'2026-11-04','new_independent_whole_key_assessment_credit':1,'prior_authorship_or_whole_key_review_this_actual_session':False,'original_reading':{'input_path':str(packet_path),'input_sha256':sha(packet_path),'read_at':reviewed_at,'stem_read_in_full':True,'all_choice_ids_read':[c['id'] for c in q['choices']],'stored_key_read':q['correct_choice_ids'],'core_and_all_distractor_explanations_read':True,'learning_boundary_read':True,'allowed_context_fields_used':['source_ids','note_evidence','family_id','topic','area'],'hidden_statement_truth_or_past_reviewer_conclusion_used':False},'legal_review':legal,'realism_review':{'verdict':s['realism'],'finding_ko':rfind,'criteria':checks,'current_style_profile':style_memo['profile'],'current_blueprint':style_memo['blueprint'],'nearby_items_directly_read_stem_and_all_choices':near_ids,'comparison_evidence_bindings':read_bindings,'individual_focus_ko':s['realism_finding'] if s['realism']=='PASS' else individual_realism[qid],'limitation_ko':'공개 format와 current profile 및 bank 내부 실독 비교에 근거한 독립 realism 판단이다. 실제 MPJE 문항의 wording·난도·비공개 유사성은 인증하지 않는다.'},'required_next_action_ko':s['next']})
assert len(records)==40
report={'schema_version':1,'stage':'independent-legacy','job_id':assignment['job_id'],'assignment_sequence':37,'actor_provenance':{'actor_id':'/root/independent_wave10_d','session_id':'fresh-agent-session:/root/independent_wave10_d:2026-11-04','basis':'실제 fresh delegated agent task /root/independent_wave10_d; 해당 세션은 visible packet으로 시작했고 원문 author/editor 또는 이전 whole-key reviewer로 활동하지 않았다.'},'auditor':'GPT','auditor_instance':'GPT:/root/independent_wave10_d:20261104','independent_of_authors':True,'canonical_audit':False,'canonical_release_credit':0,'author_review_credit':0,'review_date':'2026-11-04','reviewed_at':reviewed_at,'timezone':'Etc/UTC','question_hashes':assignment['question_hashes'],'input_binding':{'path':str(packet_path),'raw_sha256':sha(packet_path),'whole_record_hashes_are_assignment_current_records':True,'visible_input_is_question_text_not_legal_proof':True},'independence_and_source_use_disclosures':{'whole_key_exposure':False,'hidden_author_truth_exposure':False,'previous_reviewer_report_read':False,'authored_or_edited_current_questions':False,'source_discovery_incident_ko':'한 차례 source locator 검색에서 data/rules의 URL와 verification_notes 일부가 출력되었다. 내용은 주로 배정 밖 CDTM/약물 administration의 과거 source 확인 문구였고, 배정 문항의 whole-key/숨은 truth/독립 reviewer 결론은 노출되지 않았다. 해당 탐색 경로를 즉시 중단했고 root에 공개했다. 배정된 proposition의 판단 근거로 사용하지 않았다. 이후 notes/guide.sources의 id/title/url만 명시 whitelist로 추출했다.','incident_affected_assigned_question_ids':[],'incident_new_key_credit_blocked_ids':[],'incident_credit_basis_ko':'해당 incident에는 배정 질문의 whole-key 또는 controlling proposition에 대한 과거 결론이 없으므로 영향을 받은 배정 ID는 없다. 새 identity로 세션을 교체하거나 provenance를 숨기지 않았다.','nonlegal_locator_output_paths':['data/rules/ma-admin-eligible-list-bases.json','data/rules/ma-admin-pre-administration-counseling.json','data/rules/ma-admin-training-cpr-competency.json','data/rules/ma-biologic-substitution-notice-and-record.json','data/rules/ma-board-report-manner-and-format.json','data/rules/ma-cdtm-community-schedule-limits.json'],'protected_content_ko':'상업/Pre-MPJE/회상/유출 문항을 반입·복제하지 않았다. NABP public format payload는 URL/SHA/자체 memo로만 남겼고 USP source는 가져오지 않았다.'},'source_index':source_index,'source_index_binding':{'path':str(BASE/'source-index.json'),'raw_sha256':sha(BASE/'source-index.json')},'sources':sources,'style_evidence':{'path':str(BASE/'public-style-memo.json'),'raw_sha256':sha(BASE/'public-style-memo.json')},'records':records,'summary_ko':'정확 40개를 실독·보기별 법규 대조했다. 기본 RW 8개는 legal KEEP 및 realism PASS다. archive 32개는 반복/약한 distractor/추상 사례로 realism FAIL이며, 그중 폐업 0181–0184는 institutional sterile 예외를 배제하지 못해 key AMBIGUOUS/HOLD다. legal key 판단과 현실성, canonical release는 별도다.','counts':{'records':40,'legal_KEEP':36,'legal_HOLD':4,'existing_answer_correct_YES':36,'existing_answer_correct_AMBIGUOUS':4,'realism_PASS':8,'realism_FAIL':32,'canonical_release_credit':0,'author_review_credit':0},'integration_scope_ko':'이 보고서는 future queue37의 independent legacy evidence다. PR192 frozen candidate7ea50249의 canonical release 또는 current publication/annotation15 승인으로 승격하지 않는다. root만 assignment 순서로 submit/integrate하며 공유 queue·ledger·generated·원문·정책은 수정하지 않았다.'}
write(REPORT,report)
print(json.dumps({'report':str(REPORT),'report_sha256':sha(REPORT),'records':len(records),'sources':len(sources),'reviewed_at':reviewed_at,'counts':report['counts']},ensure_ascii=False))
