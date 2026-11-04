"""Serialize this session's individually made legal and realism findings.
No prior audit/author report is an input. Truth decisions below were made from
fresh retained official sources; stored keys are used only for comparison.
"""
import collections, datetime, hashlib, json, pathlib, sys
E=pathlib.Path(__file__).resolve().parent
ROOT=E.parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from export_legacy_review_input import digest

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def bind(path):return {'path':str(path.relative_to(ROOT)),'sha256':sha(path)}
def dump(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

packet=json.loads((E/'assigned-visible-input.json').read_bytes())
assignment=json.loads((E/'assignment.json').read_bytes())
loc=json.loads((E/'source-locators.json').read_bytes())
nearest=json.loads((E/'nearest-visible-comparison-input.json').read_bytes())
default_ids=set(json.loads((E/'context/default-ids-at-assignment.json').read_bytes())['recommended_ids'])
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
DATE=NOW[:10]
ACTOR={'actor_id':'/root/independent_wave11_a','session_id':'/root/independent_wave11_a'}
INSTANCE='GPT:/root/independent_wave11_a:20261104'

# Correct repo-relative metadata paths after the first retrieval helper run.
for path in (E/'official').glob('*.meta.json'):
 m=json.loads(path.read_bytes())
 for key in ('evidence_path','text_evidence_path'):
  if m.get(key,'').startswith('independent-phase11-a/'):
   m[key]=m[key][len('independent-phase11-a/'):]
 dump(path,m)

sample_meta=json.loads((E/'official/nabp-sample.meta.json').read_bytes())
sample_memo={
 'source_class':'PUBLIC_OFFICIAL','official_url':sample_meta['official_url'],
 'retrieved_at':sample_meta['retrieved_at'],'http_status':sample_meta['http_status'],
 'raw_sha256':sample_meta['raw_sha256'],'text_sha256':sample_meta['text_sha256'],
 'public_raw_redistribution':False,'retained_content':'Independent comparison memo only; no full NABP raw or extracted text committed.',
 'read_scope':'Public MPJE sample PDF introduction and all three complete sample stems and all answer options read in this actual session. No Pre-MPJE, recalled, protected, or commercial question was opened.',
 'own_observations_ko':[
  '공개 PDF는 SBA, 복수응답, 순서응답 세 형식을 예시한다. 실제 내용영역의 대표성 자료가 아니라고 본문이 명시한다.',
  'SBA 예시는 갱신 시 CE 총량을 묻는 숫자보기들이다. 이 배정의 점검·시정계획·징계·waiver·CDTM 사례와 문장/법적 판단이 다르다.',
  '복수응답 예시는 약물의 schedule 분류를 개별 판단한다. 이 배정 SATA의 기관권한, 조건, 기한 명제와 사실 및 보기 집합이 다르다.',
  '순서응답 예시는 서로 다른 처방의 만료순서를 비교한다. 배정40개에는 그 사건·약물·보기·순서 과제가 재현되지 않는다.',
  'Select ONE/ALL과 같은 기능적 응답지시는 형식상의 공통점이다. 이 비교에서는 보호된 실제시험 내용의 유사성을 주장하거나 추정하지 않았다.'
 ],'used_as_legal_authority':False}
dump(E/'nabp-style-comparison-memo.json',sample_memo)

versions={
 'src-da8a8280d110':'Retained 247 CMR 9 codification bears Mass. Register #1536, 2024-12-06. Exact commencement of each unchanged clause UNKNOWN; no later amendment established by this retrieval.',
 'src-a864a8e398a1':'Retained 247 CMR 10 contains 2025-04-25 publication / effective 2025-01-09 markings for the amended pages; other clauses retain 2013 markings. Exact original commencement of each unchanged clause UNKNOWN.',
 'src-9dd67db872cb':'Retained 247 CMR 14 bears MA Register #1348, 2017-09-22. Exact commencement UNKNOWN. Section 14.01(5) separately fixes the on/before vs after 2013-06-30 grant regimes.',
 'src-351267598b0b':'Retained 247 CMR 16 bears MA Register #1354, 2017-12-15. Exact commencement UNKNOWN. The explicit PharmD grandfather cutoff in 16.02(1)(c)1 is 2017-06-30.',
 'src-29ddff7984dc':'Board advisory adopted 2019-02-07, pages 1-2; no separate effective/expiration date printed. Exact commencement beyond adoption UNKNOWN.',
 'src-7323a3006b2c':'Policy 2024-01 adopted 2024-01-11, revised 2025-02-06; retained current revised public posting.',
 'src-368bb8382bd0':'DCP 26-03-124 dated 2026-03-11 expressly replaces DCP 23-04-118; exact commencement distinct from issue date UNKNOWN.',
 'src-682aabe3c4ae':'DCP 26-08-125 dated 2026-08-25 expressly rescinds/replaces DCP 25-04-124; exact commencement distinct from issue date UNKNOWN.',
 'fda-opill':'FDA approval announcement dated 2023-07-13; product-specific OTC approval, not an independent MA pharmacist prescribing grant.',
 'supremacy':'U.S. Constitution Article VI clause 2, current official Congress/Library of Congress publication; original ratification history not independently researched.',
 'mgl-112-24bhalf-correct':'Current official General Laws page retrieved on review date. Amendment history and exact commencement UNKNOWN; subsection (b)(3) presently prints an unqualified PharmD alternative.'}
coverage={
 'src-da8a8280d110':'247 CMR 9.19(21), 9.24(1),(3), 9.25(1)-(5)',
 'src-a864a8e398a1':'247 CMR 10.02; 10.03(1)(f),(g),(j),(k),(m); 10.04; 10.06(2)-(6),(8)-(9); 10.07; 10.08(1)-(3)',
 'src-9dd67db872cb':'247 CMR 14.01(1), (3), (5)',
 'src-351267598b0b':'247 CMR 16.02(1)(a)-(d), 16.03, 16.04(1),(2)',
 'src-29ddff7984dc':'Educational Equivalency advisory II.A.1-3, II.B, III, pages 1-2',
 'src-7323a3006b2c':'Policy 2024-01 introduction and I.B',
 'src-368bb8382bd0':'DCP 26-03-124, Purpose / Dispensing by Administration (a)-(f), pages 1-2; Administration and Dosing, page 3',
 'src-682aabe3c4ae':'DCP 26-08-125, Purpose, General Prescribing Requirements, Hormonal Contraceptive Patches and Oral Hormonal Contraceptives',
 'fda-opill':'FDA 2023-07-13 announcement, first nonprescription daily oral contraceptive approval',
 'supremacy':'U.S. Constitution Article VI, clause 2',
 'mgl-112-24bhalf-correct':'M.G.L. c.112 §24B½(a), (b)(1)-(4), (c)'}
sources=[]; source_by_id={}
for path in sorted((E/'official').glob('*.meta.json')):
 m=json.loads(path.read_bytes());sid=m['source_id']
 if sid=='nabp-sample':
  s={**m,'evidence_path':str((E/'nabp-style-comparison-memo.json').relative_to(ROOT)),'evidence_sha256':sha(E/'nabp-style-comparison-memo.json'),'public_raw_redistribution':False,'public_evidence_mode':'independent own memo only; full NABP public sample raw not republished','used_as_legal_authority':False,'exact_section':'Public sample introduction, SBA, multiple-response and ordered-response samples, page 1','law_checked_date':DATE,'version_or_effective_date_status':'Public format sample; no legal effective date asserted.'}
 else:
  s={**m,'evidence_sha256':m['raw_sha256'],'raw_path':m['evidence_path'],'source_type':'OFFICIAL_STATUTE' if sid in ('supremacy','mgl-112-24bhalf-correct') else 'OFFICIAL_REGULATION' if sid in ('src-da8a8280d110','src-a864a8e398a1','src-9dd67db872cb','src-351267598b0b','247-cmr-6') else 'OFFICIAL_GOVERNMENT_GUIDANCE','law_checked_date':DATE,'exact_section':coverage.get(sid,'Discovery/reference retrieval only; not a controlling authority for an assessed proposition.'),'version_or_effective_date_status':versions.get(sid,'UNKNOWN: publication/commencement not established; discovery/reference only.'),'used_as_legal_authority':sid in coverage and m['legal_evidence_usable'],'source_class':'PUBLIC_OFFICIAL','public_raw_redistribution':True}
 s['metadata_path']=str(path.relative_to(ROOT));s['metadata_sha256']=sha(path)
 if s.get('http_status')!=200:s['used_as_legal_authority']=False;s['finding_ko']='조회실패 보존. 404/오류페이지는 법적 근거로 쓰지 않음.'
 sources.append(s);source_by_id[sid]=s

def authority(sid,section):
 s=source_by_id[sid]
 assert s['used_as_legal_authority'] and s['http_status']==200
 return {'source_id':sid,'authority':section,'source_type':s['source_type'],'exact_section':section,'official_url':s['official_url'],'citation_url':s['official_url'],'law_checked_date':DATE,'version_or_effective_date_status':s['version_or_effective_date_status'],'evidence_path':s['evidence_path'],'evidence_sha256':s['evidence_sha256'],'raw_path':s['raw_path'],'raw_sha256':s['raw_sha256'],'text_evidence_path':s['text_evidence_path'],'text_sha256':s['text_sha256'],'metadata_path':s['metadata_path'],'metadata_sha256':s['metadata_sha256'],'retrieved_at':s['retrieved_at'],'http_status':200,'tls_verification':True}

rules={}
def rule(text,truth,sid,section,note):rules[text]={'supported':truth,'source_id':sid,'section':section,'finding_ko':note}
def pair(pos,neg,sid,sec,yes,no):rule(pos,True,sid,sec,yes);rule(neg,False,sid,sec,no)
R9='src-da8a8280d110';R10='src-a864a8e398a1';R14='src-9dd67db872cb';R16='src-351267598b0b';EQ='src-29ddff7984dc'
pair('An annual self-inspection does not replace the Board\'s inspection authority.','Annual self-inspection gives the pharmacy immunity from unannounced Board visits.',R9,'247 CMR 9.24(1)','Board는 사전통지 없이 언제든 검사할 수 있다. 연례 자체점검 완료는 권한 제한 사유가 아니다.','사전통지 없는 Board 검사를 연례 자체점검으로 면제하는 예외는 없다.')
pair('The stated self-inspection rule includes review within seven days after specified changes, including MOR change.','Only the annual calendar date can trigger a required self-inspection.',R9,'247 CMR 9.19(21)','MOR 변경·renovation·expansion·relocation 후 7일 이내의 자체점검과 적어도 연 1회 요건이 병존한다.','연간 요건 외 네 가지 사건 후 7일 요건도 있으므로 Only는 틀리다.')
pair('The applicable completed self-inspection tools are retained for at least two years.','Self-inspection forms may be discarded once the next month\'s schedule is posted.',R9,'247 CMR 9.19(21)','완료된 Board 승인 자체점검 도구의 최소 보존기간은 2년이다.','다음 달 근무표와 무관하게 완료 도구를 적어도 2년 보존해야 한다.')
pair('Requested pharmacy documents must be available through the applicable inspection process.','The MOR\'s absence automatically permits refusal of all inspection records.',R9,'247 CMR 9.24(3)','약국은 검사·조사 관련 Board 또는 designee 요청 문서를 제공해야 한다.','MOR 부재가 모든 기록 제공을 거절하게 하는 예외는 없다. 의무의 주체는 약국이다.')
pair('The written plan should address each violation with corrective actions, timing, and responsibility.','A general promise to comply replaces violation-specific corrective planning.',R9,'247 CMR 9.25(2)','각 위반별 조치, 예상 완료 또는 시행일, 책임자를 적어야 한다.','일반적 준수 약속은 각 위반별 조치·날짜·책임자를 대체하지 않는다.')
pair('The stated revised-plan deadline is seven days after an unacceptable plan is returned.','The revised-plan deadline is the date of the next annual inspection.',R9,'247 CMR 9.25(5)','부적합 계획은 약국으로 반환되고 약국은 7일 이내에 수정 계획을 제출해야 한다.','반려된 수정계획의 7일 기한은 다음 연례검사까지 미뤄지지 않는다.')
pair('The initial plan follows the stated 21-day period or the Board-specified timeframe.','Every initial plan has an unchangeable 90-day submission period.',R9,'247 CMR 9.25(1)','최초 계획은 21일 이내 또는 Board 지시 기한에 제출한다.','90일 고정 규칙이 아니다. 21일 또는 Board 지시 timeframe이다.')
pair('Submitting a plan is different from actually correcting the violations.','Submitting a plan automatically establishes that the pharmacy is compliant.',R9,'247 CMR 9.25(2),(4)','계획 서술 의무와 최대한 신속히 실제 법규준수를 달성할 의무는 별개다.','제출 자체가 위반의 실질적 시정을 증명하지 않는다. 9.25(4)의 실제 준수 의무가 남는다.')
pair('Employer approval does not excuse unsafe or impaired professional practice.','An employer\'s permission overrides the Board\'s safe-practice requirements.',R10,'247 CMR 10.03(1)(g),(k)','업무능력 저하 상태의 계속 실무와 공중 위험행위는 징계 사유다. 고용주 허가는 면책조건이 아니다.','고용주가 규정상 impairment·공중 위험 사유를 무효화할 권한은 없다.')
pair('Treatment for a condition must be distinguished from inability to practice safely.','Receiving medical treatment automatically establishes professional impairment.',R10,'247 CMR 10.03(1)(g)','요건은 질환 등에 의해 practice 능력이 impaired된 상태에서의 실무다. 치료받는 사실만으로 해당 능력 저하를 단정하지 않는다.','치료 사실과 능력 저하는 다른 사실이다. 규정은 능력이 impaired된 상태의 실무를 요건으로 한다.')
pair('Aiding unlicensed practice and violating Board orders can be disciplinary grounds.','Only medication dispensing errors can support Board discipline.',R10,'247 CMR 10.03(1)(j),(m)','Board 합의·명령 위반 및 무면허 실무를 knowingly 허용·지원하는 행위도 별도 징계 사유다.','징계 사유는 조제 오류에 한정되지 않는다. 명령 위반과 무면허 지원 등도 명시된다.')
pair('The regulatory meaning of conviction can include listed pleas and dispositions beyond imprisonment.','Conviction means only a final sentence of incarceration for this regulatory purpose.',R10,'247 CMR 10.02, Conviction','유죄평결·충분한 사실의 인정·CWOF·guilty 또는 nolo plea 등을 포함하고 선고 유무를 불문한다.','수감 선고만이라는 정의가 아니다. 수용된 plea와 지정 disposition 등이 포함된다.')
pair('An advisory letter is distinguished from formal disciplinary action.','An advisory letter and a formal reprimand are the same disciplinary category.',R10,'247 CMR 10.06(2),(3)','Advisory letter는 파일에 보존하는 우려 문서이나 formal disciplinary action이 아니다. Reprimand는 formal action이다.','10.06(2)와 (3)이 advisory letter와 formal reprimand를 명시적으로 구분한다.')
pair('The terms of a consent agreement determine its consequences; agreement alone does not make it nondisciplinary.','Every consent agreement is nondisciplinary because the licensee agreed to it.',R10,'247 CMR 10.06(4)-(6)','동의합의로도 probation이나 suspension/surrender 조건을 부과할 수 있다. 합의 여부만으로 비징계가 되지 않는다.','Probation과 suspension 등도 consent agreement를 통해 가능하므로 Every nondisciplinary는 틀리다.')
pair('Probation can permit practice subject to specified Board conditions.','Probation necessarily cancels the license permanently.',R10,'247 CMR 10.06(4)','Probation은 Board가 부과한 조건하에서 일정 기간 실무를 허용하는 징계다.','Probation은 조건부 실무 기간이며 영구 취소와 동일하지 않다.')
pair('An informal investigative conference is not the same as an adjudicatory hearing.','Every investigative conference is already the final merits hearing.',R10,'247 CMR 10.02, Adjudicatory Hearing / Investigative Conference; 10.04','Investigative conference는 비공식 complaint 논의이며 정식 절차 시작 전에도 열 수 있다.','비공식 조사회의를 정식 행정 merits hearing과 같은 절차로 취급할 수 없다.')
pair('Summary action can precede the final hearing when the specified public-threat conditions are met.','The Board must wait for a final merits decision before any summary suspension.',R10,'247 CMR 10.07','선서진술·문서증거에 근거한 immediate or serious threat이면 최종 merits hearing을 기다리지 않고 suspend/refuse renewal 가능하다.','10.07은 최종 hearing 전 suspension을 명시적으로 허용한다.')
pair('The need for the specified cease-and-desist or quarantine action has a separate limited-hearing timeline.','Cease-and-desist and summary-suspension hearings necessarily use the same clock.',R10,'247 CMR 10.07; 10.08(3)','10.07의 summary suspension 필요성 hearing은 7일, 10.08의 notices 필요성 hearing은 15 business days다.','7일과 15 business days는 다른 기한이며 hearing 대상도 다른 조치다.')
pair('The stated limited hearing for summary action is offered within seven days after the action.','The summary-action limited hearing is ordinarily deferred for 90 days.',R10,'247 CMR 10.07','행정조치 필요성에 한정된 hearing을 Board 조치 후 7일 이내 afford해야 한다. 최종 merits 완료 기한을 말하지 않는다.','통상 90일 유예가 아니라 조치 필요성 hearing을 7일 이내 afford해야 한다.')
pair('The described interim cessation or restriction can be nondisciplinary while still binding.','A nondisciplinary interim restriction is optional for the pharmacy to obey.',R10,'247 CMR 10.08(1),(2)','Notice는 비징계 cessation/restriction이지만 rescind/amend 또는 규정상 최종 조치까지 효력이 유지된다.','비징계 분류는 자율 준수를 뜻하지 않는다. 10.08(2)에 의해 효력이 계속된다.')
pair('A pending petition is not a granted waiver and does not itself excuse compliance.','Filing the petition suspends the regulation until the Board responds.',R14,'247 CMR 14.01(1),(4),(5)(c),(d)','Board의 granting과 단순 petition 제출은 구별된다. 후속 petition만으로도 만료 후 준수 의무를 중지하지 못한다.','신청이 아니라 Board가 granting한 waiver가 필요하다. 특히 14.01(5)(d)가 후속 grant 전 준수를 요구한다.')
pair('A state Board regulatory waiver does not independently waive federal law.','A state Board waiver automatically supersedes applicable federal law.',R14,'247 CMR 14.01(1)','권한은 법으로 금지되지 않는 범위에서 247 CMR 규제요건을 waive하는 것이다. 연방법 면제권을 부여하지 않는다.','14.01의 한정된 247 CMR waiver는 연방법을 override하지 않는다. U.S. Const. Art. VI cl.2도 대조했다.')
pair('The stated post-June-2013 waiver framework ordinarily expires on the fifth anniversary of the grant.','A granted waiver lasts for the lifetime of the pharmacy without an expiration review.',R14,'247 CMR 14.01(5)(a)-(d)','2013-06-30 후 grant는 grant 5주년에 만료된다. 이전 grant의 2018-06-30 별도 경로도 구별한다.','규정은 grant 시기에 따라 만료를 명시한다. 평생 효력이라는 명제는 성립하지 않는다.')
rule('Cost savings alone automatically establish all waiver criteria.',False,R14,'247 CMR 14.01(1)(a)-(c),(3)(b)-(d)','비용절감만으로 compelling public interest, impractical AND unduly burdensome, sufficient safeguards의 결합요건을 자동 충족하지 않는다.')
rule('The petition must address compelling public interest, burden or impracticality, and adequate safeguards.',False,R14,'247 CMR 14.01(1)(b),(3)(c)','OR가 실제 결함이다. 원문은 adherence가 impractical AND unduly burdensome이어야 한다. 둘 중 하나만을 적는 요건으로 바꾸면 규정의 결합요건을 약화한다.')
pair('A standing-order dispensing pathway is distinct from patient-specific CDTM authority.','Dispensing under a statewide standing order automatically creates a CDTM agreement.','src-7323a3006b2c','Policy 2024-01 I.B; 247 CMR 16.04(1)','Naloxone은 standing order 또는 patient-specific prescription으로 조제 가능하다. 이것만으로 pharmacist/physician의 서면 CDTM agreement가 생기지 않는다.','Standing order 조제는 CDTM 서면·서명 합의와 환자별 경로를 자동 생성하지 않는다.')
pair('An OTC product\'s purchase pathway does not define a pharmacist\'s independent prescribing scope.','OTC sale of one contraceptive authorizes independent prescribing of all contraceptive formulations.','src-682aabe3c4ae','DCP 26-08-125 Purpose / General Prescribing Requirements (a) / Hormonal Contraceptive Patches and Oral Hormonal Contraceptives (a),(e)','OTC 구매와 MA pharmacist prescribing은 별도 경로다. 현행 지침은 oral/patch 및 정해진 조건·training을 규정하므로 OTC 한 제품 판매가 모든 제형 처방권을 뜻하지 않는다.','허용 제품·screening·training 등 별도 prescribing 조건이 있다. OTC 판매가 주사제·모든 제형 등 포괄 처방권을 부여하지 않는다.')
pair('Medication administration is a separate act from prescribing or dispensing.','Permission to prescribe a product automatically grants permission to administer it by any route.','src-368bb8382bd0','DCP 26-03-124 Dispensing by Administration (a)-(f), pages 1-2; Administration and Dosing, page 3','Administration은 별도 조건의 행위다. 지정 약물·유효처방·연령·training 등과 허용 경로 조건을 확인해야 한다.','해당 지침은 IV를 배제하고 허용 대상과 SC/IM 등 조건을 정한다. 처방권이 any route의 투여권을 자동 부여하지 않는다.')
pair('A CDTM arrangement needs the specified individual, setting, agreement, and patient authorization.','A pharmacy\'s facility license by itself supplies all CDTM authority.',R16,'247 CMR 16.02(1);16.03;16.04(1),(2)(g)','약사 자격, 허용 setting, 서면·서명 합의, setting별 환자 동의 절차를 따로 충족한다. 이 stem의 individualized retail CDTM에서는 referral/consent가 필요하다.','시설 면허만으로 개인자격·CPA·환자별 authorization 등 별도 요건을 대체할 수 없다.')
pair('The CDTM pharmacist needs the specified current unrestricted Massachusetts license in good standing.','An unrestricted license from any state substitutes for Massachusetts CDTM licensure.',R16,'247 CMR 16.02(1)(a)','현행 unrestricted good-standing Massachusetts 약사면허와 현재 MA practice를 요구한다.','다른 주 unrestricted 면허만으로 Commonwealth 면허 요건을 대체하지 못한다.')
pair('The required liability coverage must specifically cover drug-therapy management at the stated minimum.','Any general employer insurance satisfies CDTM liability coverage regardless of its scope.',R16,'247 CMR 16.02(1)(b)','계약기간 중 drug therapy management를 명시적으로 담보하는 occurrence당 최소 $1,000,000 professional liability coverage를 유지한다.','고용주 제공 여부가 아니라 담보 범위·최소액·계약기간 유지가 관건이다. 범위와 무관하게 아무 보험이면 된다는 주장은 틀리다.')
pair('The pharmacist must be engaged in the required Massachusetts pharmacy practice.','A proposed future Massachusetts job alone satisfies the current-practice requirement.',R16,'247 CMR 16.02(1)(a)','현재 Commonwealth에서 pharmacy practice에 종사해야 한다.','미래 고용 제안만으로 currently engaged 요건을 충족하지 않는다.')
pair('Coverage must be maintained during the agreement rather than checked only at hiring.','Insurance is needed only on the day the first agreement is signed.',R16,'247 CMR 16.02(1)(b)','보험은 서명 시점 확인만이 아니라 agreement term 동안 유지할 의무다.','during the term of the agreement라는 명문과 배치된다.')
pair('The dated grandfather provision cannot be newly invoked solely because the applicant now has a PharmD.','A current PharmD degree automatically qualifies every new 2026 CDTM applicant under the grandfather clause.',R16,'247 CMR 16.02(1)(c)1','이 보기는 날짜가 있는 특정 규정상 grandfather clause를 묻는다. PharmD와 2017-06-30 또는 이전 CPA 참여를 함께 요구하므로 새 2026 참여에 그 조항만 원용할 수 없다. 현행 statute의 별도 PharmD 문언에 관한 일반 자격결론과 구별한다.','해당 grandfather clause는 degree만이 아니라 2017-06-30 또는 이전 CPA 참여도 요구한다. 이 조항에 따라 every new 2026 applicant가 자동 적격은 아니다.')
pair('General drug-related employment does not automatically establish the specified licensed-pharmacist experience.','Any drug-company employment automatically counts as licensed pharmacist practice for CDTM.',R16,'247 CMR 16.02(1)(c)','5년의 licensed pharmacist experience와 일반 약물관련 사업 근무는 자동으로 동일하지 않다. 실제 면허약사 경력/인정 equivalency 사실을 확인해야 한다.','Drug-company에서 어떤 업무를 했는지와 무관하게 licensed-pharmacist experience로 자동 계산할 수 없다. 산업 근무가 일률적으로 제외된다는 결론은 아니다.')
pair('Board-recognized equivalent education or residency pathways must meet their own conditions.','An employer may declare any training program legally equivalent without Board criteria.',R16,'247 CMR 16.02(1)(c)2','기타 education/residency의 equivalency는 Board가 정한다. 고용주가 독자적으로 법정 동등성을 만들 수 없다.','문언은 Board determines이다. 고용주의 단독 선언이 Board criteria를 대체하지 않는다.')
pair('The pharmacist\'s practice must include the co-managed therapy area as required.','CDTM qualification is independent of any actual practice in the co-managed therapy area.',R16,'247 CMR 16.02(1)(d)','공동 관리할 defined drug therapy area에 practice 일부를 투입해야 한다.','규정이 therapy area에 portion of practice를 요구하므로 actual practice와 무관하지 않다.')
pair('The PGY-1 pathway includes the specified additional experience or supervised CDTM period.','PGY-1 completion alone necessarily completes the entire stated equivalency pathway.',EQ,'Educational Equivalency advisory II.A.2(i),(ii), page 1','ASHP PGY-1에 더하여 practice 경력 2년 또는 practicing CDTM pharmacist 지휘하 CDTM 12개월 경로가 있다. 별도 II.B도 적용된다.','PGY-1만으로는 II.A.2의 추가 2년 경력/12개월 supervised 경로 및 II.B site program을 충족하지 않는다.')
pair('The supervised route requires the specified monitoring policy and records.','A verbal statement that supervision occurred replaces the required monitoring records.',EQ,'Educational Equivalency advisory II.A.2(ii), page 1; II.A.3(ii), page 2','시설의 monitoring manner를 설명하는 policy/procedure 및 monitoring documentation 보존과 Board 요청 시 제공이 요구된다.','말로 supervision이 있었다고 하는 것만으로 monitoring documentation 보존의 명문 의무를 대체하지 못한다.')
pair('Current BPS certification is a described alternative equivalency route.','An expired BPS certificate is identical to a current certification for this pathway.',EQ,'Educational Equivalency advisory II.A.1, page 1; II.B, page 2','II.A.1은 current BPS certification을 대안으로 명시한다. 이는 II.A의 한 대안이며 II.B site credentialing/training을 면제하지 않는다.','current라는 명문이 있으므로 만료된 과거 certificate만으로 같은 경로를 충족하지 않는다.')
pair('Site credentialing and the other CDTM qualifications remain applicable.','An equivalency pathway waives the separate license, insurance, and site-credentialing requirements.',EQ,'Educational Equivalency advisory II.B, III; 247 CMR 16.02(1)(a),(b)','Advisory는 5년 경력과의 동등성 요건이며 II.B의 site credentialing/training은 must also다. 별도 면허·보험도 규정에 남아 있다.','교육/경력 동등성에 관한 advisory는 면허·보험을 폐지하지 않고 site credentialing/training도 별도로 요구한다.')

group_context=[
 ('DISC03','검사방문/자체점검','7일 사건점검·2년 보존·무통지 검사권','점검을 마쳤다는 이유로 현장검사를 거부하는 실제 약국의 대응','MOR 부재·연례점검과 Board 검사권을 혼동'),
 ('DISC04','시정계획 반려','최초21일/Board지시·반려7일·책임자/조치/시행일','불충분한 시정계획을 제출하고 반려 뒤 대응을 지연하는 약국','계획 제출과 실제 시정, 최초와 수정 기한을 혼동'),
 ('DISC05','impairment/conviction','능력저하 실무와 질환치료의 구별·비수감 disposition','안전하게 검증할 수 없는 약사에게 고용주가 근무를 지시하는 상황','고용주 승인·환자 오류 미발생·질환치료만으로 징계사유를 오인'),
 ('DISC06','Board 조치 분류','advisory·probation·합의·정식 hearing','credentialing에서 advisory와 조건부 합의의 분류를 판단하는 상황','합의이면 비징계·probation이면 영구취소·조사회의이면 최종hearing으로 혼동'),
 ('DISC07','summary 절차','summary7일·notice15 business days·구속력','즉각적 공중위험에 대응하는 별개의 Board 사전조치','필요성 심리와 최종 merits 심리, 비징계와 비구속을 혼동'),
 ('DISC08','regulatory waiver','grant와 신청·결합요건·5주년·연방법 한계','비용절감과 pending petition을 이유로 규정 준수를 중단하려는 약국','신청만으로 면제·만료 전 신청으로 연장·state waiver의 연방법 효력 오인'),
 ('CDTM01','권한의 출처','standing order·OTC·CDTM·prescribe/dispense/administer','naloxone standing order와 OTC contraceptive 판매를 개인 CDTM 권한으로 넓히려는 상황','서로 다른 권한의 출처와 허용 행위를 자동 연결'),
 ('CDTM02','CDTM 면허/보험','MA current practice·unrestricted license·특정담보/계약기간','다른 주 면허와 일반 고용주 보험을 계약 적격성으로 제시하는 상황','시설/고용/미래 일자리와 개인의 현재 면허·보험 의무를 혼동'),
 ('CDTM03','CDTM 경력/경과조항','2017 grandfather 특정경로·licensed experience·Board equivalency·practice area','신규 PharmD와 일반 업계경력을 규정상 특정경로에 대입하는 상황','특정 경과조항과 신규 학위·일반 사업경력, 고용주와 Board 권한을 혼동'),
 ('CDTM04','교육 동등성','PGY1 추가경력/감독실무·current BPS·site program','PGY1 및 감독 CDTM 기록을 검토하는 실제 site credentialing 상황','residency 완료만으로 전요건 완료·구두 감독 주장과 문서 보존을 혼동')]

# Individually assessed wording/reasoning, not an all-family numeric/repetition veto.
fail_wording={
 201:'오답 A의 Only annual, B의 automatically refusal of all records, D의 다음 달 근무표 폐기는 실제 경쟁 규칙을 제시하지 않아 C만 상식적 감독권 설명으로 남는다.',
 202:'D만 사건 후 7일이라는 완결된 규칙이고 A 즉시폐기·B 전면거부·C immunity는 모두 극단적 면책이어서 D를 문장 태도로 골라낼 수 있다.',
 204:'A의 MOR 부재가 모든 기록 거부를 자동 허용한다는 포괄면책만 과도하여, INCORRECT를 법적 예외 검토 없이 추정할 수 있다.',
 205:'B의 조치·시기·책임자만 실무적으로 타당하고 A 다음 연례검사, C 자동 compliance, D 고정90일은 비현실적 절대명제다.',
 206:'C만 구체적 revised-plan 규칙이고 A 자동준수, B unchangeable90일, D 일반약속 대체가 모두 과도하여 7일 규정을 몰라도 남는다.',
 208:'D의 제출=자동 compliance가 유일하게 무조건적 면책이어서, 나머지 구체적 절차를 대조하지 않고 INCORRECT를 고를 수 있다.',
 209:'A만 안전업무 의무를 유지하고 B only dispensing errors, C only incarceration, D treatment automatically impairment는 모두 극단적 범위여서 정답을 추정하기 쉽다.',
 210:'B만 치료와 실제 능력을 구별하고 A employer overrides, C only imprisonment, D only dispensing errors는 모두 포괄적 주장이므로 보기를 읽는 상식으로 B가 남는다.',
 211:'세 오답 A Only errors, B treatment automatically, C employer overrides와 유일한 한정명제 D can include listed pleas가 대비되어 SATA의 D 단독키를 법규 없이 추정하기 쉽다.',
 212:'INCORRECT C의 only incarceration는 조제사례 밖의 극단적 정의이고, 다른 세 보기 모두 can/does not/must distinguish 식의 절제된 문장이라 C가 드러난다.',
 213:'D의 advisory/formal 구별만 제한된 설명이며 A probation permanently cancels, B every conference final, C every agreement nondisciplinary가 모두 절대명제로 과장된다.',
 214:'A만 terms에 따른 조건부 설명이고 B permanently cancels, C every conference final, D same category가 법적 구별을 지우는 단정이어서 A가 두드러진다.',
 215:'A every conference final와 D probation permanently cancels가 과장되고 B/C는 구별·조건을 보존하는 문장으로 짝지어져 BC를 문체로 추정하기 쉽다.',
 216:'B의 Every investigative conference final만 모든 절차 구분을 없애는 문장이어서 10.02/10.04를 몰라도 오류로 보인다.',
 217:'C의 specified conditions만 적절한 조건문이고 A necessarily same clock, B90일 유예, D optional obedience는 과도하여 C가 남는다.',
 218:'D만 별도 절차를 인정하고 A final까지 기다림, B90일, C optional 준수는 명백한 과장이라 실제15 business days를 몰라도 선택된다.',
 220:'A의 optional obedience가 유일하게 행정조치의 구속력을 부인하므로, 7일/15영업일을 구별하지 않고도 INCORRECT를 추정할 수 있다.',
 221:'B만 신청/허가를 구별하고 A cost alone automatically, C automatically supersedes federal, D lifetime without expiration은 일괄 면제 언어라 정답을 드러낸다.',
 222:'C만 관할의 한계를 지키고 A lifetime, B filing suspends, D cost automatically all criteria는 절대적 면제라 문체만으로 C가 드러난다.',
 225:'A의 distinct pathways만 권한을 구별하고 B any route, C facility supplies all, D all formulations는 포괄 확대라 A를 법규 없이 추정하기 쉽다.',
 226:'B만 OTC와 prescribing을 구별하고 A facility all, C automatically any route, D automatically CDTM는 자동 확대 언어라 B가 두드러진다.',
 227:'A/B/D의 automatically/any route/all formulations와 유일한 C specified qualifications가 대조되어 C 단독키가 문체로 노출된다.',
 228:'C의 facility license by itself supplies all만 근거 없는 포괄권한이며 나머지 셋은 서로 구별하라는 문장으로 묶여 오류가 드러난다.',
 229:'D만 specified current MA 자격이고 A only signing day, B any insurance regardless scope, C future job alone는 요건 삭제 언어라 D가 남는다.',
 230:'A만 required specific minimum을 지키고 B any state substitutes, C future job alone, D only first day는 요건을 없애 정답을 길이·태도로 추정하게 한다.',
 232:'B only first day만 기간 의무를 일회 확인으로 바꾸어, 나머지 세 구체적 자격과 대비되어 오류가 노출된다.',
 233:'C의 dated clause 제한만 합리적이고 A any employment automatically, B employer any program, D independent of actual practice는 광범위한 면제로 설계되어 C가 남는다.',
 234:'D의 does not automatically만 범위를 보존하고 A employer any equivalence, B practice independent, C every new applicant automatic은 포괄 단정이라 D가 두드러진다.',
 236:'A의 independent of any actual practice만 요건을 통째로 지우며 B/C/D 모두 조건을 지키는 문장이라 INCORRECT를 문체로 추정하게 한다.',
 237:'B만 specified additional period를 인정하고 A waives separate requirements, C verbal replaces records, D expired identical current는 극단적 대체라 정답이 노출된다.',
 238:'C만 policy and records를 유지하고 A alone necessarily entire, B waives separate, D expired identical current는 전면 면제·동일시여서 C가 남는다.',
 240:'D가 면허·보험·site credentialing을 한꺼번에 면제한다고 말하는 유일한 보기라, equivalency 세부사항 없이 INCORRECT를 추정하기 쉽다.'}

comparison_notes={
 'MA-Q-0222':'relocation 후 사건점검과 최근 연례점검·무통지 Board방문을 한 사례에 결합한다. 배정은 MOR변경을 별도 Case B로 두고 같은 검사/문서 원리를 재사용한다.',
 'MA-RW-0075':'MOR vacation과 접근 가능한 기록, investigator 확인을 구체화한 행동결정이다. 배정은 같은 연례점검/검사거부 혼동을 두 사례와 명제판단으로 제시한다.',
 'MA-Q-0195':'methadone emergency bridge의 반복·연장 여부이다. plan/period 같은 일반단어가 겹칠 뿐 시정계획 사실·보기·결론은 겹치지 않는다.',
 'MA-RW-0076':'Board가 지정한 최초10일과 반려7일, 서명주체, 실제시정을 결합한다. 배정의 vague promise와 반려 후 다음연례검사 대기는 같은 원리이나 사실 수준과 요구행위가 더 단순하다.',
 'MA-Q-0262':'타주 충분사실/CWOF 후 dismiss된 실제 disposition에 conviction 정의를 적용한다. 배정의 주사실은 impaired practice/치료이며 conviction은 관련보기로만 붙는다.',
 'MA-Q-0268':'타주의 reproductive-health 제재에 대한 Massachusetts 보호 carve-out이다. 같은 discipline 영역이나 배정의 impairment/치료·conviction 사실과 법적 결정이 다르다.',
 'MA-Q-0223':'약국 공중위험의 긴급조치를 고르는 사례다. 배정 impairment 문항과는 주체·조치 단계가 다르고, summary 문항과는 별도7일/15영업일의 두 메커니즘 비교가 다르다.',
 'MA-RW-0077':'somnolence·검증불능·오류 미도달·치료 중 능력보존을 특정한다. 배정과 동일한 고용주 승인/치료만으로 impairment 단정이라는 혼동이지만 구체적인 판단사실과 다섯 보기 조합이 다르다.',
 'MA-Q-0211':'advisory letter와 credentialing formal-discipline 질문이 사실상 Case A의 같은 결정이다. 배정은 consent agreement Case B 및 probation/conference 보기까지 추가하지만 A의 결정은 새것이 아니다.',
 'MA-RW-0078':'12개월 감독·monitoring·명시적 disciplinary 분류에 probation을 적용한다. 배정은 advisory letter와 합의만으로 비징계라는 추론을 함께 다룬다.',
 'MA-Q-0269':'urgent prehearing 조치의7일/notice·비징계 구별을 명제로 묻는다. 배정 summary family와 동일한 원리를 공유하되 두 Case와 실제 제한의 구속력 명제를 추가한다.',
 'MA-RW-0079':'같은 날 Board suspension과 President quarantine, 계속효력을 특정하고7일/15영업일을 직접 경쟁시킨다. 배정도 같은 원리지만 notice 기한은 대부분 추상적 separate timeline으로 표현된다.',
 'MA-Q-0123':'전자처방 예외/waiver를 약사가 확인해야 하는지에 관한 다른 105CMR 요건이다. Board의247CMR waiver petition·grant·5주년과 주체/효과가 다르다.',
 'MA-RW-0080':'2021-10-01 grant,2026-09-25 후속 petition,10-02 실제행위에 만료·결합요건을 적용한다. 배정은 비용/pending 및 연방법 효력의 일반 명제여서 실제 날짜 계산이 없다.',
 'MA-Q-0095':'최초 oral contraceptive 처방에서 prior-Rx 유무와 screening을 판단한다. 배정은 OTC 판매에서 모든 제형 처방권을 추론하는 것의 부당성을 묻는다.',
 'MA-REV-0066':'OTC naloxone 현금구매와 standing-order 보험조제를 구별한다. 배정은 naloxone standing order에서 patient-specific CDTM가 생기는지로 권한의 출처를 비교한다.',
 'MA-Q-0081':'statute §24B½(b)의 학위/경력·면허·보험·CE를 그대로 묻는 명제들이다. 배정은 규정16.02의 특정 경과조항 또는 면허/보험 적용사실을 제시한다. statute의 무기한 PharmD 대안은 별도 fresh 원문으로 확인했다.',
 'MA-REV-0019':'CDTM 추가연5시간과 일반20시간을 구별하는 다른 적격성 유지 문제다. 배정 면허/보험은 별도 요건이고 보기·사례가 다르다.',
 'MA-Q-0305':'CDTM statutory 정의 내 허용행위와 diagnosis 제외를 판단한다. 배정은 보험 범위이므로 일반 CDTM 단어 외 결정/보기는 다르다.',
 'MA-REV-0022':'nonresident 약국 shipping의 MA 시설허가를 묻는다. 배정은 개인 CDTM Massachusetts pharmacist 면허여서 MA 허가 혼동 원리만 공통이다.',
 'MA-Q-0297':'CPA/referral/consent 사본의 보관과 original을 구별한다. 배정은 보험·현재실무가 주사실로 문서보관 판단과 다르다.',
 'MA-RW-0030':'facility registration과 individual MCSR, MassHealth attestation을 구별한다. 배정은 개인의 현재 면허/보험 자격으로 다른 등록 판단이다.',
 'MA-REV-0018':'2021 PharmD·2026 최초CPA·5년/동등성 미확립은 배정 CDTM03 Case A와 실질적으로 같은 규정상 문제다. CDTM04와는 equivalency를 실제 충족하는지의 세부조건이 다르다.',
 'MA-Q-0243':'면허시험 전 residency 시작 예정자의 intern license와 supervision이다. 배정의 면허약사 PGY1 이후동등성은 자격단계·행위가 다르다.',
 'MA-RW-0027':'3년 practice+current BPS+site program+BLS의 충족사실을 대입한다. 배정0239는 같은BPS 대안과site요건을 다른PGY1/감독사례의 관련명제로 확인한다.'}

records=[]
for i,r in enumerate(packet['records']):
 q=r['original_visible_content'];qid=q['question_id'];n=int(qid[-4:]);g=(n-201)//4;variant=(n-201)%4
 family,title,determinations,practice,confusion=group_context[g]
 expected=[];findings={};auths={}
 incorrect='INCORRECT' in q['stem']
 for c in q['choices']:
  d=rules[c['text']];sel=(not d['supported']) if incorrect else d['supported']
  if sel:expected.append(c['id'])
  a=authority(d['source_id'],d['section']);auths[(d['source_id'],d['section'])]=a
  extra=[]
  if g==5 and 'federal' in c['text']:
   extra=[authority('supremacy','U.S. Constitution Article VI clause 2')]
  if g==6:
   extra.append(authority(R16,'247 CMR 16.02(1);16.03(5);16.04(1),(2)(g)'))
  if g==9 and ('license' in c['text'] or 'qualifications' in c['text']):extra.append(authority(R16,'247 CMR 16.02(1)(a),(b)'))
  for a2 in extra:auths[(a2['source_id'],a2['exact_section'])]=a2
  original=q['explanation']['choice_analysis'][c['id']]
  exp_status='SUPPORTED'
  exp_note='보기 전문과 원 한국어 판단·교정문을 읽었다. '+d['finding_ko']
  if n in (221,222) and 'burden or impracticality' in original:
   exp_status='INCORRECT_CORRECTION';exp_note='이 오답 자체의 배제는 맞다. 그러나 원 교정문이 burden OR impracticality로 바꾼 것은14.01(1)(b),(3)(c)의 AND 요건과 다르므로 수정해야 한다.'
  if n in (223,224) and 'burden or impracticality' in c['text']:
   exp_status='INCORRECT_OPTION_JUDGMENT';exp_note='원 한국어 해설은 이 명제를 옳다고 분류하지만 원문은 impractical AND unduly burdensome이다. 보기의 OR를 참으로 취급한 해설은 틀리다.'
  findings[c['id']]={'choice_text':c['text'],'choice_text_sha256':hashlib.sha256(c['text'].encode()).hexdigest(),'proposition_supported':d['supported'],'selection_expected':sel,'finding_ko':d['finding_ko'],'authorities':[a,*extra],'original_explanation_text_sha256':hashlib.sha256(original.encode()).hexdigest(),'original_choice_explanation_assessment':exp_status,'original_choice_explanation_finding_ko':exp_note}
 if g==8:auths[('mgl-112-24bhalf-correct','M.G.L. c.112 §24B½(b)(3)')]=authority('mgl-112-24bhalf-correct','M.G.L. c.112 §24B½(b)(3)')
 expected.sort();stored=sorted(q['correct_choice_ids'])
 key_correct='YES' if stored==expected else 'AMBIGUOUS' if q['question_type']=='SBA' and len(expected)!=1 else 'NO'
 verdict='KEEP';finding='원문 조건 범위에서 모든 보기의 법적 명제를 독립 대조했고 저장키와 독립키가 일치한다.';blocker=None
 core_status='SUPPORTED';core_note=f'{determinations}에 관한 core를 원문과 대조했다. 날짜/기산점/주체에 필요한 한정은 보기별 기록에 보존했다.'
 if n in (221,222):verdict='MINOR_EDIT';finding='저장키는 맞으나 잘못된 보기의 교정 해설에서 AND 결합요건을 OR로 바꾸었다.';blocker=finding;core_status='SCOPE_INCOMPLETE';core_note='core의 세요소/충분한 safeguards는 큰 방향이 맞지만 원문은 impractical AND unduly burdensome의 동시 충족을 명시한다. 해당 교정문 OR를 고쳐야 한다.'
 if n==223:verdict='MAJOR_REWRITE';finding='A의 burden OR impracticality는14.01의 AND 요건을 약화해 거짓이다. SATA 저장ABCD는 틀리고 독립 기대키는BCD다.';blocker=finding;core_status='KEY_AND_RATIONALE_DEFECT';core_note='세 요소를 언급하는 core만으로 보기A의 잘못된 OR를 치유하지 못한다. 보기A를 참으로 분류한 해설과 키를 함께 고쳐야 한다.'
 if n==224:verdict='MAJOR_REWRITE';finding='INCORRECT 보기C의 OR명제와 D의 lifetime명제가 모두 틀려 단일정답 유일성이 없다. 저장D만으로는 불충분하다.';blocker=finding;core_status='UNIQUENESS_AND_RATIONALE_DEFECT';core_note='core가 요건 세 개라고만 적고 C를 참으로 처리하여 AND/OR 결함을 놓쳤다. C와D 모두 거짓이라는 법적 판정이 필요하다.'
 if g==8:
  core_status='SUPPORTED_WITH_ROUTE_SCOPE_LIMITATION';core_note='stem/보기는 날짜가 붙은 규정상 grandfather 경로 자체를 묻는다. 그 좁은 명제는16.02(1)(c)1과 맞다. 현행 statute24B½(b)(3)는 unqualified PharmD 대안을 그대로 인쇄한다. 규정을 무효라고 단정하거나 이 문항을 모든 신규 PharmD의 일반 적격성 결론으로 확장하지 않았다. 일반 적격성 안내로 재사용하려면 statute/규정의 관계에 관한 별도 Board 설명을 확보해야 한다.'
 if g==9:
  verdict='MINOR_EDIT';finding='보기 및 저장키는 맞다. 다만 한국어 core의 PGY-1 이후2년은 원 advisory의 additional2years에 없는 필수 선후관계를 덧붙인다.';blocker=finding;core_status='OVERSTATED_SEQUENCE';core_note='II.A.2는 PGY1에 더한 additional2years experience 또는12개월 supervisedCDTM를 요구한다. 경력2년이 반드시 residency 완료 후에만 계산되어야 한다는 시간순서는 원문에 명시되어 있지 않다. 이후를 에 더하여로 고쳐 명시되지 않은 배제를 피해야 한다.'
 for c in findings.values():
  if g==9:c['original_choice_explanation_scope_note_ko']='각 보기 설명 자체는 추가경력/감독실무 요건을 맞게 요약한다. 공통 core의 이후라는 선후관계 추가는 별도 결함으로 분리했다.'
 legal={'existing_answer_correct':key_correct,'stored_key':stored,'independently_expected_key':expected,'question_polarity':'SELECT_INCORRECT' if incorrect else 'SELECT_ALL_TRUE' if q['question_type']=='SATA' else 'SELECT_ONE_TRUE','single_answer_uniqueness':len(expected)==1 if q['question_type']=='SBA' else None,'choice_by_choice_findings':findings,'authorities':list(auths.values()),'verdict':verdict,'finding_ko':finding,'blocker':blocker,'exceptions_deadlines_and_jurisdiction_ko':f'{determinations}. '+('연방/MA 관할한계는14.01과Supremacy Clause를 함께 확인했다.' if g==5 else 'MA 고유 규정/Board 지침 범위이다. 별도 연방규칙을 MA 요건의 대체물로 쓰지 않았다.'),'original_explanation_review':{'core_and_all_choice_explanations_read':True,'explanation_sha256':digest(q['explanation']),'core_assessment':core_status,'core_finding_ko':core_note,'choice_explanations':{cid:{'assessment':v['original_choice_explanation_assessment'],'finding_ko':v['original_choice_explanation_finding_ko'],'original_text_sha256':v['original_explanation_text_sha256']} for cid,v in findings.items()},'learning_boundary_assessment_ko':'4개가 같은 두 사례와 네 판단을 공유하는 변형이라는 공개 고지를 읽었다. 독립 네 임상사례로 취급하지 않는다.'}}
 matches=nearest['matches'][i]
 dup=[]
 for pool in ('canonical','public_default','public_other'):
  for candidate in matches[pool]:
   cid=candidate['question_id']
   if cid.startswith('MA-EXP-'):
    note=f'{cid}의 stem 전문과 모든 보기를 읽었다. 같은 두 Case가 그대로 반복되고 ONE/ALL/INCORRECT 및 보기극성/순서가 바뀐 동일 family의 공개 변형이다. 학습경계 고지와 현재 default 제외를 전제로 archive 연습으로 한정해야 한다.'
   else:note=comparison_notes[cid]
   dup.append({**candidate,'pool':pool,'stem_and_every_choice_read':True,'manual_comparison_ko':note})
 bad_word=n in fail_wording
 # SATA with several independently decidable qualified rules can retain realism.
 reasons={
  'jurisprudence_reasoning':f'{title}에서 {determinations}의 법적 성격을 사실에 적용한다. '+('INCORRECT 극성까지 따로 판정한다.' if incorrect else '각 명제의 성립과 선택 여부를 분리한다.'),
  'practice_plausibility':practice+'이며 약국의 업무/감독 범위에 든다.',
  'authentic_distractors':confusion+'에서 나오는 개념은 관련성이 있다. '+('다만 실제 보기의 과도한 절대어는 다음 criterion의 별도 실패다.' if bad_word else 'SATA는 각 명제의 조건을 따로 확인해야 하며 전부 참인 조합도 그 자체로 금지하지 않았다.'),
  'wording_not_guessable':fail_wording.get(n,'정답 조합을 정하려면 숫자·자격·기간/기관의 조건을 실제 확인해야 한다. Select ALL의 참인 보기들에 서로 독립된 조건이 있어 단일 절대어 제거만으로 전체 조합이 결정되지 않는다.'),
  'reasoning_not_trivia':f'{title}의 주체/조건 구별이 실무 판단이다. '+('이 문항은 사례 밖 conviction 정의도 관련보기로 끼워넣어 자연성은 아래에서 별도 실패시켰다.' if g==2 else '숫자 자체나 family 반복이라는 이유로 실패시키지 않았다.'),
  'natural_rule_combination':f'{determinations}은 {title}의 같은 업무 흐름에서 결합된다.' if g!=2 else '주사실은 능력저하/치료 차이인데 conviction의 정의와 수감만이라는 보기가 별도의 criminal disposition 사실 없이 붙는다. 같은 징계 chapter라는 이유만으로 자연스러운 결합이라고 볼 수 없다.',
  'appropriate_drug_context':'Naloxone standing order와 OTC contraceptive의 법적 판매/처방경로 차이가 판단에 직접 쓰인다.' if g==6 else '특정 약물명은 이 행정·면허·자격 판단의 법적 결과를 바꾸지 않아 생략이 적절하다.',
  'distinct_from_bank':'nearest canonical/public/default 후보의 원문과 모든 보기를 실제 비교했다. 동일 family의 공유문구와 일부 같은 결정은 존재하나 명시적4개 변형 학습고지와 현재default 제외 맥락을 고려하여 archive 변형 자체만으로 자동 실패시키지 않았다. 신규 default 독립문항으로의 승격을 승인한 뜻은 아니다.',
  'not_schedule_flashcard':f'{title}의 기관권한·절차·자격 판단이며 약물 schedule 명칭만 회상하는 문항이 아니다.',
  'public_style_without_copying':'공개 NABP sample의 세 stem과 모든 보기를 직접 읽고 비교했다. 응답지시 형식은 공유하나 CE 숫자·schedule분류·처방만료순서의 예시 사건/보기/문장과 이 문항의 사실·결정은 다르다.'}
 criteria={k:True for k in reasons};criteria['wording_not_guessable']=not bad_word;criteria['natural_rule_combination']=g!=2
 if n in (223,224):
  criteria['authentic_distractors']=False;reasons['authentic_distractors']='OR로 바뀐 waiver 결합요건은 참/거짓 구분의 핵심인데 원 해설이 이를 참으로 분류한다. 의도된 confusion을 검증하는 정상 distractor/key 구조가 아니다.'
 if n==224:
  criteria['wording_not_guessable']=False;reasons['wording_not_guessable']='INCORRECT에서 lifetime D가 눈에 띄지만 C도 AND→OR로 틀리다. 단일오답 형식과 실제 두 거짓명제가 충돌한다.'
 passed=all(criteria.values())
 realism={'verdict':'PASS' if passed else 'FAIL','decision':'KEEP' if passed else 'MAJOR_REWRITE','criteria':criteria,'criterion_findings_ko':reasons,'finding_ko':('10개 기준을 문항별 사실·보기와 실제 비교자료에 대조해 확인했다. Archive 변형 맥락에서의 PASS이며 release 승인 아님.' if passed else '실패 기준: '+', '.join(k for k,v in criteria.items() if not v)+'. '+('문구의 절대면제/포괄권한 대비가 정답을 드러낸다.' if bad_word else '보기의 법적 분류/자연스러운 결합을 수정해야 한다.')),'duplicate_review':{'status':'MANUAL_COMPARISON_COMPLETED','canonical_search_count':nearest['canonical_count'],'public_search_count':nearest['public_count'],'default_context_binding':bind(E/'context/default-ids-at-assignment.json'),'search_input_binding':bind(E/'nearest-visible-comparison-input.json'),'similarity_is_semantic_verdict':False,'candidates':dup,'public_sample_binding':bind(E/'nabp-style-comparison-memo.json'),'in_default_at_assignment':qid in default_ids}}
 disposition='INDEPENDENT_ASSESSED' if verdict=='KEEP' and key_correct=='YES' and passed else 'NEEDS_REMEDIATION'
 fresh=[
  'MOR 교체의 실제 날짜와 최근 연례점검 날짜, 기록 접근 가능성을 정하고 7일 사건점검과 무통지 검사 대응 중 필요한 행동을 고르게 한다.',
  'Board의 최초10일 지시와 반려일을 주고 수정7일 기한·각 위반 책임자/시행일·실제시정 의무를 자연스럽게 결합한다.',
  '검증능력이 저하된 약사와 치료 중이나 능력이 보존된 약사의 구체적 업무상태를 제시하고 가능한 조치를 고르게 한다. conviction은 실제 plea/CWOF 사실이 있는 별도 fresh 사례로 분리한다.',
  '실제 기간·감독조건·Board의 분류가 담긴 합의를 제시하고 advisory/reprimand/probation 중 효과를 판단하게 한다.',
  '같은 날짜의 Board suspension과 President quarantine을 구별하여7일·15 business days 필요성 심리와 계속효력을 실제 행동으로 판단하게 한다.',
  'grant 날짜·후속 신청일·실제 운영일을 정하고 만료 후 원규정 준수 및 impractical AND unduly burdensome·public interest·safeguards를 빠짐없이 적용한다.',
  'OTC contraceptive 구매와 특정 oral/patch 처방 요청 또는 naloxone 보험조제 사실을 구체화하고 해당 행위별 법적 근거를 고르게 한다.',
  '보험증서의 occurrence당 금액·drug-therapy-management 담보·계약기간과 MA 면허/현재 practice 사실을 주고 미충족 조건을 판단하게 한다.',
  'CPA 참여일·licensed practice 기간·Board 인정동등성 사실을 제시한다. 2017 경과조항 자체를 묻는지 현재 일반 자격을 묻는지 명확히 구별한다.',
  'PGY1·추가 practice 기간 또는 감독CDTM 기록·site program/BLS 충족사실을 주고 II.A와II.B를 함께 적용한다. 시간순서를 추가하지 않고 additional 요건을 그대로 표현한다.'
 ][g]
 records.append({'question_id':qid,'record_sha256':r['record_sha256'],'visible_content_sha256':r['visible_content_sha256'],'read_scope':'Original complete stem; every choice; stored key; full Korean core, every distractor/correct-choice explanation and learning_boundary read in this actual session. Hidden truth and previous author/audit conclusions excluded.','family_id':loc['records'][i]['family_id'],'legal_review':legal,'realism_review':realism,'disposition':disposition,'safe_hold_recommended':disposition!='INDEPENDENT_ASSESSED','release_eligible':False,'canonical_release_credit':0,'author_review_credit':0,'required_next_action_ko':('원문 보존. 독립 검토 결과를 root가 통합하되 canonical release 승격 없이 archive 변형으로 유지한다.' if disposition=='INDEPENDENT_ASSESSED' else '원문 직접 수정하지 않음. Editor가 실제 결함을 해결한 새 current hash를 만들고 별도 fresh independent 검토를 받는다. Fresh scenario 제안: '+fresh),'fresh_scenario_followup_proposal_ko':fresh})

profile=json.loads((ROOT/'data/exam_style/mpje_style_profile.json').read_bytes())
blueprint=json.loads((ROOT/'data/blueprint.json').read_bytes())
report={'stage':'independent-legacy','independent_of_authors':True,'auditor':'GPT','auditor_instance':INSTANCE,'actor_provenance':ACTOR,'canonical_audit':False,'canonical_release_credit':0,'author_review_credit':0,'reviewed_at':DATE,'review_completed_at':NOW,'job_id':assignment['job_id'],'question_hashes':assignment['question_hashes'],'input_binding':bind(E/'assigned-visible-input.json'),'assignment_binding':bind(E/'assignment.json'),'source_locator_binding':bind(E/'source-locators.json'),'context':{'progress_report_path':str((E/'context/progress-at-assignment.json').relative_to(ROOT)),'progress_report_sha256':sha(E/'context/progress-at-assignment.json'),'meaning':'Retained assignment-time snapshot only. No alias to live progress and no inherited prior session read methodology.','default_ids':bind(E/'context/default-ids-at-assignment.json')},'policy_bindings':[bind(ROOT/'docs'/f) for f in ['RELEASE_POLICY.md','AUDIT_WORKFLOW.md','SOURCE_USE_POLICY.md','QUESTION_AUTHORING_STANDARD.md','INDEPENDENT_LEGACY_REVIEW_RUNBOOK.md']],'schema_bindings':[bind(ROOT/'schemas'/f) for f in ['audit.schema.json','exam_style_profile.schema.json','blueprint.schema.json']],'style_profile':{'profile_id':profile['profile_id'],'content_version':profile['content_version'],'content_hash':profile['content_hash'],'file_binding':bind(ROOT/'data/exam_style/mpje_style_profile.json')},'blueprint':{'blueprint_id':blueprint['blueprint_id'],'content_version':blueprint['content_version'],'content_hash':blueprint['content_hash'],'file_binding':bind(ROOT/'data/blueprint.json')},'methodology_ko':['실제 새 actor/session에서 정확히 배정된40개 공개 원문을 읽고 공식primary를 직접조회했다. author/old auditor 보고서·hidden truth/conditional fact·whole source dump는 입력하지 않았다.','모든 선택지의 참거짓을 수작업으로 판단한 rules table에서 독립키를 산출하고 그 뒤 stored key와 비교했다. 자동유사도는 검색에만 사용하고 selected58개 공개원문을 실제 읽었다.','정부raw와 extracted text는 보존했다. NABP는 공개sample만 읽고 URL/raw/text SHA와 직접 작성한 메모만 보존한다. 404 두 건은조회실패로 분리하고 근거로 사용하지 않았다.','공식 문서의 알려진 버전/날짜와 확인하지 않은 commencement를 구분했다. UNKNOWN은 정확 시행일의 미확립을 뜻하며 원문 미열람을 숨기기 위한 표기가 아니다.','CDTM statutory PharmD 대안과 규정의 dated grandfather clause를 모두 확보하고, 이 보고서의 좁은 경과조항 판정을 일반 신규자격 판정으로 확대하지 않았다.','배정40개와 retained default IDs의 교집합은0이다. 동일family archived변형만으로 자동FAIL하지 않고 실제 보기·결정·현재default맥락을 별도로 평가했다.'],'sources':sources,'records':records,'summary':{'originals_read':40,'all_choices_and_full_korean_explanations_read':40,'legal_verdicts':dict(collections.Counter(r['legal_review']['verdict'] for r in records)),'key_assessments':dict(collections.Counter(r['legal_review']['existing_answer_correct'] for r in records)),'realism_verdicts':dict(collections.Counter(r['realism_review']['verdict'] for r in records)),'dispositions':dict(collections.Counter(r['disposition'] for r in records)),'default_overlap_ids':sorted(set(assignment['question_hashes'])&default_ids),'canonical_release_credit':0,'author_review_credit':0},'checks':{'native_validation':'PENDING','git_push':'PENDING'}}
dump(ROOT/'reports/full-corpus-review/independent-phase11-a-review.json',report)
print(json.dumps(report['summary'],ensure_ascii=False))
