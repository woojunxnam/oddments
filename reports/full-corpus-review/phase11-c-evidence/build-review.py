"""Serialize this session's independently read, statement-specific findings.

No previous review, hidden statement truth or author conclusion is input.
"""
from pathlib import Path
import copy
import datetime
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
BASE = Path('reports/full-corpus-review/phase11-c-evidence')
sys.path.insert(0, str(ROOT/'scripts'))
from export_legacy_review_input import export, digest

def read(p): return json.loads((ROOT/p).read_bytes())
def sha(p): return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def write(p, obj): (ROOT/p).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')

assignment = read(BASE/'assignment.json')
packet = read(BASE/'assigned-visible-input.json')
assert packet == export(assignment)
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
review_date = now[:10]
actor = '/root/independent_wave11_c'
instance = 'GPT:/root/independent_wave11_c:20261104'
locators = {r['question_id']:r for r in read(BASE/'source-locators.json')['records']}

source_specs = {
 'src-351267598b0b': ('247 CMR 16.00', '16.03(5)(d); 16.04(1), (5), (6), (7)', 'MA Register #1354, dated 2017-12-15', 'UNKNOWN: 표기된 Register 일자와 별도 법적 시행일을 동일시하지 않았다.'),
 'src-6251c99ae2dd': ('DPH/Board/DCP Policy 2023-02', 'Introduction; I.A-B; II; III.A-D; IV.A-C; IX Appendix', 'Adopted 2023-05-04; revised 2023-09-07 and 2025-09-04', 'UNKNOWN: 현 게시 개정일은 2025-09-04이며 별도 commencement 문구는 확인되지 않는다.'),
 'src-40e00d06b90b': ('247 CMR 4.00', '4.03(4)(e)', 'MA Register #1330, dated 2017-01-13', 'UNKNOWN: Register 일자는 보존했으나 별도 commencement는 확정하지 않았다.'),
 'src-7470f2e1235b': ('Board Policy 2021-04', 'I; III', 'Adopted 2021-10-01; latest printed revision 2025-09-04', 'UNKNOWN: 게시 개정일과 별도 법적 시행일은 구분하였다.'),
 'src-a397fe32483f': ('105 CMR 700', '700.004(B)(6)(a)-(d)', 'Mass. Register #1514, 2024-02-02', 'UNKNOWN: 2024-02-02 Register 표시는 확인했으나 별도 시행일은 확정하지 않았다.'),
 'federal-prep-govinfo': ('42 USC 247d-6d', '(a)(3); (b)(1)-(2); (i)(8)', '2024 official US Code edition', 'UNKNOWN: 2024 법전은 선언의 조건부 구조 확인에만 사용. 2026의 모든 법개정 또는 모든 vaccine 예외를 이 판본만으로 확정하지 않았다.'),
 'prep-twelfth-amendment': ('HHS Twelfth Amendment to COVID-19 PREP Act Declaration', 'DATES; V(d)(i)-(xii); XII(i)(i)-(iv)', 'Published 2024-12-11; effective 2025-01-01', '2025-01-01'),
 'hhs-prep-index': ('HHS ASPR PREP Act official index', 'COVID-19 PREP Act declarations; link to Twelfth Amendment', 'Current official index retrieved '+review_date, 'UNKNOWN: index 자체는 새 법률·포괄적 투여권한이 아니다.'),
 'federal-prep-act': ('US Code attempted lookup', '247d-6d attempted locator only', 'HTTP 404', 'UNKNOWN: 실패한 조회를 법률 확인으로 사용하지 않는다.'),
 'mgl-112-24bhalf': ('MGL attempted unspaced section locator', '24B½ attempted locator only', 'HTTP 404', 'UNKNOWN: 실패한 조회를 법률 확인으로 사용하지 않는다.'),
 'mgl-112-24bhalf-current': ('M.G.L. c.112, §24B½', '(e)', 'Current Massachusetts General Court section retrieved '+review_date, 'UNKNOWN: current consolidated section은 별도 commencement 날짜를 표시하지 않는다.'),
}
sources = {}
for sid, (authority, section, version, effective) in source_specs.items():
 m = read(BASE/'official'/f'{sid}.meta.json')
 sources[sid] = dict(source_id=sid, authority=authority, source_type='OFFICIAL_STATUTE' if sid=='federal-prep-govinfo' else 'OFFICIAL_REGULATION' if sid.startswith('src-') and sid in {'src-351267598b0b','src-40e00d06b90b','src-a397fe32483f'} else 'OFFICIAL_POLICY', exact_section=section, official_url=m['official_url'], citation_url=m['official_url'], law_checked_date=review_date, version=version, effective_date=effective if effective=='2025-01-01' else 'UNKNOWN', effective_date_basis=effective, evidence_path=m['text_path'], evidence_sha256=m['text_sha256'], raw_path=m['raw_path'], raw_sha256=m['raw_sha256'], retrieval_metadata_path=str(BASE/'official'/f'{sid}.meta.json'), retrieval_metadata_sha256=sha(BASE/'official'/f'{sid}.meta.json'), retrieved_at=m['retrieved_at'], http_status=m['status'], tls_verification=True, provenance='This actual session retrieved official HTTPS bytes through inherited proxy with certificate validation; no earlier audit cache used.', legal_authority_used=m['status']==200 and sid not in {'hhs-prep-index'})
 if sid=='mgl-112-24bhalf-current': sources[sid]['source_type']='OFFICIAL_STATUTE'

facts = {}
def pair(family, yes, no, section, yes_reason, no_reason, ids=None):
 if ids is None: ids=['src-351267598b0b','mgl-112-24bhalf-current'] if family=='CDTM16' else ['src-351267598b0b'] if family=='CDTM15' else ['src-6251c99ae2dd']
 for text, truth, reason in [(yes,True,yes_reason),(no,False,no_reason)]:
  assert text not in facts
  facts[text]=dict(family_id=family, statement_supported=truth, finding_ko=reason, exact_section=section, source_ids=ids)

pair('CDTM15','Therapy continuation must be arranged before termination or nonrenewal as required.','Nonrenewal permits immediate abandonment of ongoing therapy without a transition plan.','247 CMR 16.04(5)', '종료 또는 미갱신 전에 약사와 감독의사가 협약에 따른 중단 없는 약물치료 지속을 마련해야 한다. 이는 권고가 아니라 shall 의무다.', '미갱신도 사전 치료 지속 조치의 대상이다. 즉시 진료를 끊어도 된다는 예외는 없으며 Case A는 이 의무를 위반한다.')
pair('CDTM15','The pharmacist keeps the current agreement and required referral or consent copies readily retrievable at the primary setting.',"The physician's records eliminate the pharmacist's local CPA and copy-access responsibilities.",'247 CMR 16.04(6); 16.03(5)(d)', '약사는 primary practice setting에 현재 CPA·현 환자 의뢰·동의 사본을 readily retrievable하게 유지한다. 의사의 원본 보관과 병존하는 별도 의무다. or는 필요한 기록의 일부를 선택하여 생략할 권한으로 읽지 않았다.', '의사가 원본을 갖는다는 사실은 약사의 현재 사본 및 검색 가능성 의무를 면제하지 않는다. 두 주체의 기록 책임을 합칠 수 없다.')
pair('CDTM15','The patient receives written notice and information about continuing therapy.','Telling only pharmacy employees satisfies patient termination notice.','247 CMR 16.04(5)', '협약이 갱신되지 않거나 CDTM이 끝나면 환자에게 종료와 치료 지속 절차를 서면으로 알린다.', '통지 상대는 직원이 아니라 환자이며 서면 통지가 필요하다. 내부 전달만으로 환자 통지 의무를 충족하지 못한다.')
pair('CDTM15','Electronic storage must preserve access and the applicable current version.','Any old electronic draft substitutes for the current signed agreement.','247 CMR 16.04(1), (6)', '매체가 전자라는 이유로 현재 서명된 협약 및 현재 의뢰·동의 사본을 요청 시 제시할 의무가 달라지지 않는다. 전자 저장을 별도 의무나 새 허가로 만들지 않은 기능적 해석이다.', '규정은 written and signed 및 current agreement를 요구한다. 오래된 초안은 현재 서명본 사본이 아니므로 전자 형식만으로 요건을 충족하지 않는다.')

pair('CDTM16','The stated restriction distinguishes hiring to establish a CPA from a permitted quality-assurance relationship.','A community pharmacy may hire a physician for the purpose of establishing its CPAs without the stated restriction.','247 CMR 16.04(7)(b)-(c)', 'community pharmacy의 QA review 목적 고용은 허용되나 CPA 유지·수립·체결 목적 의사 고용은 금지된다. 고용 목적을 나누어 판단한다.', 'CPA를 수립하기 위해 의사를 고용하는 것은 명시적으로 금지된다. QA 고용 허용에서 CPA 고용 허용을 도출할 수 없다.')
pair('CDTM16','A qualifying quality-assurance review relationship is not the same as purchasing prescribing authority.','Every physician quality-assurance contract automatically creates a CPA for all patients.','247 CMR 16.04(1), (7)(b)-(c)', 'QA review를 위한 고용 허용은 환자별 CDTM 협약이나 처방권한의 자동 부여가 아니다. purchasing라는 수사는 법적 용어가 아니며 16.04(1)의 별도 협약 조건으로 해석했다.', 'QA 계약만으로 signed CPA나 community 환자별 referral·consent가 생기지 않는다. every/all patients라는 자동 확대는 근거가 없다.')
pair('CDTM16','A physician or physician group may employ a qualified pharmacist for CDTM within the applicable framework.','CDTM pharmacists may never be employed by a physician group.','247 CMR 16.04(7)(a)', '의사 또는 의사집단은 그 환자의 CDTM을 위해 qualified pharmacist를 고용할 수 있다. pharmacy가 의사를 고용하는 반대 방향의 제한과 다르다.', '16.04(7)(a)는 의사 또는 physician group의 qualified pharmacist 고용 경로를 명시한다. never라는 전면 금지는 틀리다.')
pair('CDTM16',"The purpose and terms of the employment arrangement matter to the legal assessment.","Changing the contract's title alone removes the restriction on its actual purpose.",'247 CMR 16.04(7)(b)-(c)', '규정은 for the purpose of라는 실제 목적을 기준으로 QA review와 CPA 수립·유지 고용을 구분한다.', '명칭 변경이 실제 CPA 수립·유지 목적을 없애지 않는다. 고용 명칭을 근거로 규정의 목적 제한을 우회할 수 없다.')

pair('VAX01','Completing an injection course does not make a technician trainee eligible under the state vaccination policy.','An injection course makes a licensed technician trainee eligible to vaccinate under the state policy.','Policy 2023-02 Introduction; III.D.1', '주 정책의 pharmacy personnel에는 pharmacist·intern·PT만 포함되고 PTT는 명시적으로 제외된다. 주사 교육 수료가 면허 단계 제한을 바꾸지 않는다.', '정책은 PTT may NOT vaccinate라고 명시한다. PTT 면허나 course 수료를 full PT 자격으로 전환할 수 없다.')
pair('VAX01',"An eligible technician still needs the on-duty pharmacist's approval and direct supervision by a qualified immunizing pharmacist.","A qualified technician's training certificate replaces on-duty approval and direct pharmacist supervision.",'Policy 2023-02 Introduction', 'intern과 PT 모두 근무 중 licensed pharmacist의 승인 및 정책의 모든 immunizer 요건을 충족하는 약사의 직접 감독을 받아야 한다.', '교육 자격과 근무 시 승인·직접 감독은 별도 누적 조건이다. 자격증으로 승인이나 감독을 대체할 수 없다.')
pair('VAX01','The pharmacist retains vaccine selection and counseling duties before technician administration.',"A technician's permission to inject includes independent vaccine selection and patient counseling.",'Policy 2023-02 III.D.4', '약사가 상담하고 백신을 선택한 다음 PT는 물리적 준비·투여 및 standing order에 따른 응급약 제공만 수행한다.', 'PT 허용은 physical act에 제한된다. 백신 선택과 환자 상담을 독립적으로 수행할 권한으로 확대할 수 없다.')
pair('VAX01','The intern pathway also requires the specified supervision rather than independent practice.',"An intern's vaccination training creates an independent pharmacist practice privilege.",'Policy 2023-02 Introduction; III.C', 'intern도 교육 이수 외에 on-duty 약사 승인과 적격 약사의 직접 감독이 필요하다.', 'intern의 교육 수료는 독립 pharmacist 면허나 감독 면제가 아니다. Introduction의 intern 감독 조건을 삭제할 수 없다.')

pair('VAX02',"The four-year-old does not meet the state policy's five-year minimum for this pathway.","The state policy's five-year minimum can be waived by the pharmacist solely because a parent consents.",'Policy 2023-02 II; 105 CMR 700.004(B)(6)', '지문은 주 경로만 사용한다고 한정한다. 이 경로는 5세 이상이므로 4세는 해당하지 않으며 부모 동의만의 연령 면제는 없다.', '동의는 별도 절차이지 주 경로의 five years or older 기준을 약사가 임의로 바꿀 권한이 아니다. 다른 연방 경로까지 금지한다는 결론은 아니다.', ['src-6251c99ae2dd','src-a397fe32483f'])
pair('VAX02','Meeting the pharmacy-policy age floor does not establish eligibility for that particular vaccine product.','A five-year-old is eligible for every vaccine once the pharmacy-policy minimum is met.','Policy 2023-02 I.A-B; II; IV.A; IX Appendix', '일반 5세 기준과 제품·대상군·actual order의 포함/제외 조건은 별도다. Appendix는 연령 등에 따른 용량·경로와 대상 조건을 요구한다. 이 답은 의사의 모든 off-label 사용을 금지한다는 뜻이 아니다.', '주 경로 최소 나이 하나로 모든 제품·대상군·용량이 허용되지는 않는다. 실제 order와 해당 Commissioner 권고의 적용 범위를 확인해야 한다.')
pair('VAX02','A distinct federal authorization must be evaluated on its own conditions rather than presumed.','The state policy itself establishes all conditions of every federal vaccination exception.','Policy 2023-02 II; Twelfth PREP Declaration V(d), XII(i); 42 USC 247d-6d(a)(3), (b)(1)-(2)', '주 정책만으로 연방 예외의 인력·제품·대상·기간을 확정하지 않는다. 직접 읽은 PREP 선언도 자체 감독·교육·CPR·제품 및 기간 조건을 둔다. 이 문항은 어느 4세 환자의 실제 PREP 적격성을 선언하지 않는다.', 'MA 정책은 모든 연방 예외의 조건을 수립하는 문서가 아니다. PREP의 qualified persons와 유효기간 등은 해당 연방 문서에서 따로 확인해야 한다.', ['src-6251c99ae2dd','federal-prep-govinfo','prep-twelfth-amendment'])
pair('VAX02','The route, dose, patient population, and applicable recommendation remain relevant to administration.','The pharmacy-policy age floor determines dose and route without reference to the product.','Policy 2023-02 I.A-B; IX Appendix', 'standing order는 백신별 timing·route·specific dose를 연령과 기타 요인에 맞게 정하고 inclusion/exclusion을 포함해야 한다.', '주 경로 최소 나이는 제품별 dose·route를 정하지 않는다. Appendix의 제품별 투여 및 대상 조건을 누락한 설명이다.')

pair('VAX03','The policy recognizes the applicable current Commissioner recommendation for the specified use.',"The policy prevents following any Commissioner recommendation that differs from original labeling.",'Policy 2023-02 I.B', 'DPH Commissioner가 원 FDA 표시와 다른 population 또는 schedule을 권고하면 qualified personnel은 해당 current recommendation에 따라 투여할 수 있다. may 허용이며 반드시 투여하라는 의무는 아니다.', 'I.B는 표시와 다른 Commissioner 권고를 따르는 경로를 명시적으로 허용한다. 모든 차이를 금지한다는 주장은 반대다.')
pair('VAX03',"An immunizer's personal preference is not the same authority as an issued Commissioner recommendation.","An immunizer may label a personally selected schedule as a Commissioner recommendation.",'Policy 2023-02 I.B', 'I.B의 주체는 DPH Commissioner이며 실제 발행된 current recommendation이다. 개인 선호를 그 권고로 대체할 수 없다.', '개인이 선호하는 schedule을 Commissioner 권고라고 부르는 것만으로 I.B의 발행 주체·실제 권고 조건을 충족하지 못한다.')
pair('VAX03','The recommendation must match the vaccine, population, and use being considered.','A recommendation for one vaccine population supplies authority for unrelated products and populations.','Policy 2023-02 I.A-B; IV.A; IX Appendix', 'I.B의 those vaccines와 in accordance with 조건은 해당 권고의 백신·population·schedule 범위 내 적용을 뜻한다.', '특정 population에 대한 권고를 무관한 제품이나 population으로 일반화할 근거가 없다. actual order의 포함 조건도 확인해야 한다.')
pair('VAX03','The remaining personnel, training, order, and reporting requirements still apply.',"Following a Commissioner recommendation removes the policy's training and reporting conditions.",'Policy 2023-02 Introduction; III; IV.A-B, G', 'I.B의 제품 사용 허용이 정책의 personnel·교육·CPR·order·MIIS 보고 요건을 면제하지 않는다. 개별 요건은 그대로 별도 확인한다.', 'I.B에는 교육이나 reporting을 없애는 예외가 없다. current recommendation을 따르는 사실만으로 나머지 정책 의무를 삭제할 수 없다.')

pair('VAX04','Twenty hours of self-study alone do not meet the specified initial course composition.','Any 20 hours of self-study satisfy the course even without live instruction or hands-on assessment.','Policy 2023-02 III.C.1(a)-(c)', '약사·intern 초기 ACPE 과정은 12시간 self-study와 8시간 live seminar 및 연령에 적합한 IM/SC hands-on 평가를 누적 요구한다. 총 20시간 self-study는 live·실기 결손을 보충하지 못한다.', '총시간만으로 구성 요건을 대체할 수 없다. III.C.1은 self-study, live seminar, hands-on을 and로 연결한다.')
pair('VAX04','The pharmacist must maintain current CPR certification before performing vaccination.','Completion of the initial vaccination course makes subsequent CPR expiration irrelevant.','Policy 2023-02 III.A, C', '예방접종을 수행하는 모든 pharmacy personnel은 current CPR이어야 한다. 과거 초기 course 수료와 별개의 현재 조건이다.', '초기 course 수료가 현재 CPR 요건의 예외를 만들지 않는다. Case B의 만료 CPR로 이 경로의 투여를 진행할 수 없다.')
pair('VAX04',"The injection assessment must address age-appropriate intramuscular and subcutaneous techniques.",'Written knowledge assessment alone substitutes for the required injection-technique assessment.','Policy 2023-02 III.C.1(c)', 'hands-on 평가는 환자 연령에 적합한 IM와 SC 기법을 다뤄야 한다. 두 경로를 모두 명시한 요건이다.', '서면 지식 시험과 hands-on injection 평가는 별도 구성이다. 서면시험만으로 실기평가를 대신하지 못한다.')
pair('VAX04','Training and CPR evidence must be maintained at the pharmacy as required.',"An undocumented verbal assurance of training is the policy's required evidence.",'Policy 2023-02 III.B', '교육 및 CPR certification 증빙은 약국에 on file로 보관해야 한다. 특정 종이 매체만을 필수라고 추가하지 않았다.', '정책은 proof kept on file을 요구한다. 기록 없는 구두 보증은 그 증빙 보관 의무가 아니다.')

pair('VAX05','The pharmacist must meet the applicable annual immunization CE requirement separately from initial training.','A prior initial immunization course permanently replaces annual immunization CE.','Policy 2023-02 III.C.3; Policy 2021-04 III; compare 247 CMR 4.03(4)(e)', '현재 두 정책은 매 calendar year ACPE immunization CE 최소 1시간을 요구한다. 247 CMR의 biennial 최소 문구와 구분하여 정책 연간 요건으로 판단했다. 지난해 초기 교육은 올해 이수를 대신하지 않는다.', '초기 ACPE 자격 과정과 매 calendar year 유지 CE는 별개다. permanently 대체한다는 예외는 어느 정책에도 없다.', ['src-6251c99ae2dd','src-7470f2e1235b','src-40e00d06b90b'])
pair('VAX05',"The technician's stated maintenance requirement is at least two immunization-related hours every two years.","The technician follows the pharmacist's one-hour-per-calendar-year rule instead of the technician rule.",'Policy 2023-02 III.D.5; III.C.3', 'PT는 2년마다 immunization 관련 CE/updated training 최소 2시간이 필요하다. 약사의 연간 1시간과 같은 규칙으로 바꾸지 않는다.', 'III.D.5의 직종별 2년 요건을 pharmacist III.C.3의 calendar-year 규칙으로 대체할 수 없다.')
pair('VAX05',"The pharmacist's immunization CE must be ACPE-approved under the policy.",'Any informal discussion about vaccines necessarily counts as the required pharmacist immunization CE.','Policy 2023-02 III.C.3; Policy 2021-04 III', '두 정책의 immunization CE 조항은 약사의 해당 1시간에 ACPE-approved를 명시한다. 일반 CE의 더 넓은 승인유형을 그대로 이 특별 요건에 적용하지 않는다.', '비공식 대화라는 사실만으로 ACPE-approved immunization CE가 되지 않는다. 내용·승인·해당 연도 credit을 확인해야 한다.', ['src-6251c99ae2dd','src-7470f2e1235b'])
pair('VAX05','Current CPR and required supervision remain necessary alongside continuing education.','Completing maintenance education replaces current CPR and required supervision.','Policy 2023-02 Introduction; III.A, C.3, D.5', '유지 CE를 마쳐도 current CPR과 intern/PT 감독·승인 조건은 남는다. 약사가 늘 다른 약사의 감독을 받는다는 주장은 하지 않은 required supervision 표현이다.', '교육 시간과 CPR·직종별 감독은 서로 다른 요건이다. CE 완료를 근거로 다른 요건을 면제할 수 없다.')

pair('VAX06','Trainee hours alone do not satisfy the alternative requiring 500 hours after full technician licensure.','Six hundred trainee hours satisfy the alternative requiring 500 post-licensure technician hours.','Policy 2023-02 III.D.1(b)', '500시간은 PT로 licensed된 뒤 근무한 시간이다. Case A의 trainee 600시간과 full PT 후 0시간은 해당 경로를 충족하지 않는다.', '600이 500보다 많아도 기산점이 다르다. PTT 경력과 full PT 면허 후 경력을 섞어 계산할 수 없다.')
pair('VAX06','National certification does not eliminate the separate vaccination-training requirements.','PTCB certification alone replaces vaccination-specific training and skills assessment.','Policy 2023-02 III.D.1(a), D.2-3; III.A', 'national certification은 full PT 면허와 함께 쓰는 자격 대안의 한 갈래일 뿐이다. vaccination course·OJT·skills·CPR 등이 별도로 남는다.', 'PTCB는 III.D.1(a)의 credential이며 III.D.2-3의 백신 교육·skills를 대신한다는 문구가 없다.')
pair('VAX06','The national-certification and post-licensure-experience options are alternative qualifying routes.','The policy requires both national certification and 500 post-licensure hours in every case.','Policy 2023-02 III.D.1(a)-(b)', '공통 full PT 면허에 either national certification or 500 postlicensure hours를 더한다. AND와 OR의 적용 위치를 구분한다.', 'either/or를 두 자격 모두의 누적 의무로 바꾼 설명이다. 국가 인증 경로에 추가 500시간을 일괄 요구하지 않는다.')
pair('VAX06','Full Massachusetts technician licensure is still required for either qualifying route.','National certification permits vaccination without the required Massachusetts technician license.','Policy 2023-02 III.D.1; Introduction', 'Must be licensed as a PT는 certification·experience 두 대안에 공통이다. national certificate가 MA full technician 면허를 대체하지 않는다.', '주 PT 면허는 공통 전제이며 PTT도 제외된다. national certification만으로 주 면허 요건을 제거할 수 없다.')

pair('VAX07','The six-hour course does not replace the additional two hours of documented on-the-job training.','The six-hour course includes and eliminates the separate additional on-the-job requirement.','Policy 2023-02 III.D.2-3', '6시간 ACPE 과정 외에 적어도 2시간의 documented OJT가 additional로 요구된다. 시간 합산으로 별도 요소를 삭제하지 않는다.', 'III.D.3은 최소 2시간 OJT를 additional로 정한다. 6시간 과정 안에 자동 포함되어 없어지는 조건이 아니다.')
pair('VAX07','The course must include the specified live instruction and hands-on technique assessment.','An entirely recorded course with unsupervised practice satisfies the live and hands-on components.','Policy 2023-02 III.D.2(a)', '6시간 과정에는 live training 최소 2시간과 환자 연령에 적합한 IM/SC hands-on assessment가 포함되어야 한다.', '전부 녹화형 과정과 평가자 없는 개인 연습은 요구된 live instruction 및 hands-on assessment를 충족한 것으로 볼 수 없다.')
pair('VAX07','On-the-job training requires an experienced certified immunizer and documented skills assessment.',"Any coworker's undocumented observation satisfies the stated on-the-job pathway.",'Policy 2023-02 III.D.3', 'OJT는 experienced certified immunizer와 함께 최소 2시간 문서화하고 Skills Checklist for Vaccine Administration 또는 유사 도구를 완료한다.', '아무 coworker의 미기록 관찰은 경험 있는 certified immunizer·documented OJT·skills checklist 요건을 충족하지 않는다.')
pair('VAX07','Recognition and management of vaccine reactions are part of the required training.','Technician training may omit vaccine-reaction recognition if the pharmacist is present.','Policy 2023-02 III.D.2(b)', 'PT 과정의 필수 내용에는 vaccine reaction recognition과 management가 포함된다.', '약사가 현장에 있다는 사실은 III.D.2(b)의 교육 내용을 면제하지 않는다. 감독과 교육은 누적 조건이다.')

pair('VAX08','The vaccine order does not itself replace the required emergency-medication prescription or standing order.','A vaccine standing order necessarily authorizes every emergency medication without another order.','Policy 2023-02 IV.A-B; IX Appendix', '백신 투여와 이상반응 대응 응급약 투여 모두 prescription 또는 standing-order 권한이 필요하다. 한 문서가 둘을 포함할 수 있으며 반드시 별도 종이 두 장을 요구하는 뜻이 아니다.', '백신 명령만으로 모든 응급약 투여 권한이 자동 생기지 않는다. Case A는 emergency medication을 covering하는 실제 권한이 없다고 명시한다.')
pair('VAX08','An unsigned model template is not an issued standing order from an authorized prescriber.','Downloading a model template makes it an operative standing order without prescriber authorization.','Policy 2023-02 IV.B-C; IX Appendix (prescriber signature)', '공개 모델은 작성 도구이며 actual standing order에는 duly authorized prescriber의 서명이 필요하다. 지문은 서명 없는 모델만 있다고 한다.', '다운로드는 처방자의 발행·서명이 아니다. IV.C의 모델 제공을 실제 투여 명령으로 혼동한 설명이다.')
pair('VAX08','An operative order must identify its authorized vaccines, recipients, administration instructions, and required procedures.','A standing order that lists a vaccine name needs no recipient or administration instructions.','Policy 2023-02 IX Appendix', 'Appendix의 minimum에는 백신명, 연령·기타 요인별 timing/route/dose, inclusion/exclusion, 관찰·기록·보고·동의·투여 주체·서명이 포함된다.', '백신명만으로 Appendix의 대상 기준 및 투여 절차가 충족되지 않는다. 나머지 최소 내용을 누락할 수 없다.')
pair('VAX08','Emergency instructions include medication details and a process for obtaining emergency assistance.',"The policy's emergency component is satisfied by a generic statement to address reactions later.",'Policy 2023-02 IX Appendix (emergency treatment procedures)', 'emergency procedures는 투여할 약물의 dose/route와 계속 진료 지원(예:911 연락)을 구체화해야 한다.', '나중에 반응을 처리하겠다는 추상적 약속은 응급약·용량·경로·계속 진료 지원 절차가 아니다.')

# The expected key was solved from the statements and the actual question polarity,
# before serializing. This table is deliberately not copied from the stored keys.
expected_keys = ['C','D','ACD','A','B','C','ABCD','D','A','B','D','C','D','A','AC','B','C','D','ABD','A','B','C','ABCD','D','A','B','C','C','D','A','BD','B','C','D','ACD','A','B','C','ABCD','D']
assert len(expected_keys)==40

core_notes = {
 'CDTM15':'치료 지속을 종료 전에 마련하는 의무와 종료 시 환자 서면 통지, 약사 current copy·의사 원본 책임의 구분은 16.04(5)-(6)과 일치한다. 전자 version consistency는 current signed copy 요건의 해석이지 별도 전자문서 법령의 인용이 아니다.',
 'CDTM16':'고용 방향, QA 목적 허용, CPA 수립·유지 목적 금지를 정확히 구분한다. purchasing prescribing authority는 수사적 표현이므로 법정 용어로 암기하게 하기보다 16.04(1),(7)의 실제 조건을 제시하는 편집이 유용하다. 키를 바꾸는 법적 오류는 없다.',
 'VAX01':'PTT 제외, intern/PT 승인·직접 감독, 약사의 선택·상담 책임을 정확히 나눈다. state policy 경로에 한정해 해설하며 모든 PREP 경로를 이 정책만으로 판정하지 않았다.',
 'VAX02':'주 경로만 지정한 4세 사례의 한계와 제품·대상·dose/route의 별도 심사를 설명한다. 5세 기준을 모든 연방 예외의 금지로 확대하지 않았고, 특정 federal 경로의 완전한 적격성이나 모든 의사 off-label 진료 금지를 주장하지 않는다.',
 'VAX03':'실제 Commissioner 권고에 따른 허용과 개인 선호, 적용 범위, 나머지 자격·명령·보고 조건을 구분한다. 허용(may)을 투여 의무로 바꾸지 않는다. 다만 사례·오답 표현은 시험 설계 측면에서 추상적이다.',
 'VAX04':'12시간 self-study +8시간 live +IM/SC hands-on 및 current CPR·증빙 보관을 정확히 설명한다. 총시간과 교육유형·현재 자격을 분리한 해설이다.',
 'VAX05':'초기 교육, 약사의 calendar-year ACPE 1시간, PT의 2년 2시간, CPR·감독을 구분한다. 본문의 숫자는 현 정책과 일치한다. 247 CMR 4.03(4)(e)의 biennial 문구와 정책의 annual 요구가 다르다는 명시가 없어 학습상 보강이 유익하지만 정책 기준의 키를 바꾸는 오류는 아니다.',
 'VAX06':'full PT license + (national certificate OR postlicensure 500 hours)와 별도 백신 과정·skills·CPR 구조를 정확히 풀이한다. 600 trainee hours는 기산점이 달라 인정되지 않는다.',
 'VAX07':'6시간 ACPE 과정 안의 최소 2시간 live/실기와 additional 최소 2시간 documented OJT·checklist를 나누고 reaction 교육을 필수로 설명한다.',
 'VAX08':'백신과 응급약 각각의 실제 order authority, 미서명 모델의 한계, Appendix 내용을 정확히 설명한다. 두 권한을 한 서명 문서가 포함할 수 있으며 별도 물리적 문서 두 장이라는 조건을 추가하지 않았다.',
}

# Concrete item-level realism defects. Two all/partial-true SATA sets are retained
# as passes after applying the same ten criteria; all-true SATA is not prohibited.
defects = {
 281:'Case A의 치료 지속을 묻는데 A는 any old electronic draft, B는 physician records, D는 직원 통지다. C만 치료 지속 조치여서 실제 조문보다 주제 일치만으로 고르기 쉽다.',
 282:'D만 현재 사본·primary setting·retrievable을 모두 갖춘 상세한 문장이고 A는 any old draft, B는 immediate abandonment, C는 telling only employees다. 사례 B와 무관한 극단적 오답이 많다.',
 283:'SATA의 유일한 거짓 B가 immediate abandonment without a transition plan이라고 노골적으로 표현되어, current-copy 및 서면 통지의 세부요건을 몰라도 배제하기 쉽다.',
 284:'INCORRECT의 유일한 오류 A에 Any old electronic draft라는 신호가 있다. B-D는 차분하게 필수요건을 기술해 표현만으로 오류가 드러난다.',
 285:'오답은 every contract automatically, title alone, may never로 과장되고 정답 B는 the stated restriction이라고 안전하게 한정된다. 실제 금지 목적을 적용하는 경쟁 보기로 구성되지 않았다.',
 286:'A never, B without the stated restriction, D title alone과 C의 도덕적 purchasing prescribing authority 표현이 대비된다. Case B에 필요한 실제 허용 조건보다 수사로 답이 드러난다.',
 287:'A·C·D가 목적 제한의 의미를 서로 바꾸어 반복하며 C의 purpose and terms matter와 D의 not purchasing authority는 구체적 법적 행동을 겨루지 않는다. 모두 참 SATA 자체가 실패 사유는 아니다.',
 288:'D만 Changing the contract title alone으로 우회를 주장한다. 나머지 세 보기는 within applicable framework와 qualifying처럼 안전한 한정어여서 목적 조항을 몰라도 D를 추측하기 쉽다.',
 289:'Case A의 trainee 자격을 묻지만 B는 independent selection/counseling, C는 intern independent pharmacist privilege, D는 감독 면제다. A만 trainee 교육이라는 주제를 직접 답한다.',
 290:'B는 자격·on-duty approval·qualified direct supervision을 상세히 결합하고 나머지는 independent 권한 또는 injection course만의 trainee 허용이다. 현실의 승인자·감독자 혼동보다 포괄적 권한 확대가 오답이다.',
 291:'D만 구체적 승인·감독 조건을 갖추고 A-B는 independent practice라는 과장, C는 trainee 단독 course이다. 지문에 없는 intern privilege도 끼어 있어 관련 조건을 겨루는 밀도가 낮다.',
 292:'C의 independent pharmacist practice privilege는 intern을 완전한 약사로 만드는 주장이다. A·B·D는 모두 구체적인 제한을 기술하여 INCORRECT를 법적 세부사항 없이 추측하기 쉽다.',
 293:'D는 네 살과 다섯 살을 그대로 비교한다. A는 all conditions of every federal exception, B는 제품 없이 dose/route 결정, C는 every vaccine이라 정답 외 보기가 극단적이다.',
 294:'A의 does not establish eligibility와 달리 B는 consent solely waiver, C는 every federal exception, D는 product 없이 dose/route 결정이다. 제품 이름·실제 order 없이 일반적 주의 문장만 정답이 된다.',
 295:'A의 조건을 따로 평가하라는 일반론과 C의 4<5 외에 B·D는 모든 제품 허용 또는 나이만으로 용량·경로 확정이다. 실제 제품별 연령·order 조건의 혼동을 겨루지 않는다.',
 296:'B가 나이 하나로 제품 없이 dose와 route를 정한다고 한다. A·C는 조건 확인을 강조하고 D는 4<5여서 INCORRECT가 과장 표현으로 드러난다.',
 297:'C의 applicable current recommendation과 대조되는 오답은 unrelated products, personal schedule을 official이라고 호칭, training/reporting 삭제이다. 특정 백신·대상·명령을 적용하는 선택지가 없다.',
 298:'개인 선호가 발행된 Commissioner 권고가 아니라는 D는 별도 법률 지식 없이 언어상 참이다. 다른 보기도 훈련 면제·무관 제품 확대·모든 표시 차이 금지라 실제 업무 판단의 긴장이 약하다.',
 299:'B의 personal preference is not issued recommendation은 상식적 동어반복이고 유일한 거짓 C는 unrelated products and populations로 과장된다. 실제 권고 범위의 경계 사례가 없다.',
 300:'A만 권고를 따른다고 training/reporting이 제거된다고 한다. B-D는 일반적 범위 주의여서 INCORRECT가 내용의 극단성으로 쉽게 드러난다.',
 301:'B의 course 구성 판단은 실제적이지만 오답 A가 undocumented verbal assurance, C가 CPR expiration irrelevant, D가 written assessment alone이다. 사례의 교육 총시간과 구성에 관한 유사 대안이 부족하다.',
 302:'C의 current CPR과 달리 A는 any 20 self-study, B는 undocumented verbal assurance, D는 written alone이다. 만료 자격을 어떤 합리적 절차로 보완할지 겨루는 대안이 없다.',
 304:'오류 D는 undocumented verbal assurance를 required evidence라고 한다. 교육기록 파일의 허용 형식·보관 위치 차이를 묻는 것이 아니라 모순적인 표현으로 정답이 드러난다.',
 305:'A는 applicable annual CE라는 신중한 문장인 반면 C는 any informal discussion necessarily counts, D는 CE가 CPR·감독을 대체한다는 과장이다. B의 직종별 시계 혼동 외에는 경쟁력이 약하다.',
 306:'B는 숫자와 주기를 직접 제시하고 A는 permanently replaces, C는 CPR·감독 대체, D는 informal necessarily counts이다. 직종별 두 시간 시계의 적용을 실제 기록으로 비교하지 않는다.',
 307:'유일한 참 C는 ACPE 승인이라는 구체적 요건이며 D는 permanently replaces, B는 CE가 CPR·감독을 대체한다. 내용이 아니라 과장어를 지우는 전략이 지나치게 유효하다.',
 308:'C만 CE가 CPR 및 감독을 replaces한다고 주장한다. 나머지 보기의 annual/ACPE/two-year는 제한적 진술이어서 INCORRECT가 일반적 교육 독립성만으로 드러난다.',
 309:'실제 trainee/postlicensure 기산점은 의미 있지만 A는 PTCB만으로 전 교육 대체, C는 state license 없이 투여, B는 in every case라 D 외 보기의 권한 확대가 두드러진다.',
 310:'Case B의 별도 교육 결손에 답하는 A와 달리 B는 both in every case, C는 state license 없이 투여, D는 다른 사례의 trainee 시간이다. 사실 적용 대신 주제와 절대어로 답하기 쉽다.',
 312:'B만 national certification이 state license를 없앤다고 한다. 나머지는 alternative routes 또는 separate requirements 같은 안전한 한정 문장이라 INCORRECT가 쉽게 구별된다.',
 313:'Case A의 additional OJT에 답하는 C와 달리 A는 any coworker undocumented, B는 reaction 교육 생략, D는 entirely recorded unsupervised이다. 실제 OJT 증빙·교사의 경력 경계를 겨루지 않는다.',
 314:'D만 specified live and hands-on이라는 제한을 보존한다. A는 separate requirement eliminates, B는 reaction 생략, C는 any coworker undocumented라 의미 있는 대안이 적다.',
 315:'지문이 separate documented OJT를 명시하는데 유일한 거짓 B가 course includes and eliminates the separate requirement라고 한다. 조문 적용보다 지문 문구의 직접 부정으로 배제하기 쉽다.',
 316:'A의 pharmacist가 있으면 vaccine-reaction recognition을 omit한다는 주장은 다른 B-D의 특정 추가 요건과 대비된다. INCORRECT가 대체·면제 수사에 집중된다.',
 317:'B만 Case A의 emergency-medication authority를 직접 답한다. A 다운로드 자동 명령, C 나중에 대응, D vaccine name만으로 충분이라는 과장 때문에 다른 현실적 보완 조치와 경쟁하지 않는다.',
 318:'서명 없는 template이 issued order가 아니라는 C는 지문에서 거의 되풀이된다. A·B·D는 각각 막연한 대응·모든 응급약 자동 승인·백신명만의 문서로 과장되어 있다.',
 319:'모든 참 SATA 구성 자체는 적법하고 네 요건도 실무적이다. 다만 default MA-RW-0048과 signed vaccine order/unsigned emergency model/구체적 응급지시라는 사실·판단이 사실상 같아 독립적인 새 항목으로는 중복이다.',
 320:'D의 generic statement to address reactions later만 명백히 불충분하다. 나머지는 요건을 정리한 문장이라 실제 emergency dose/route·order 범위 차이를 판별하지 않고도 오류를 찾기 쉽다.',
}

focuses = ['Case A의 종료 전 치료 지속','Case B의 약사 기록 의무','두 사례 및 관련 기록·통지 요건의 SATA','전자 초안에 관한 INCORRECT', 'Case A의 CPA 목적 의사 고용','Case B의 QA 목적 고용','고용 방향·목적 관련 SATA','고용 명칭에 관한 INCORRECT', 'Case A의 PTT 투여 제한','Case B의 on-duty 승인·직접 감독','직종별 권한 SATA','intern 독립권한 INCORRECT', 'Case A의 주 경로 4세 제한','Case B의 제품별 적격성','주/연방·연령 경로 SATA','dose/route 기준 INCORRECT', 'Case A의 Commissioner 권고 경로','Case B의 개인 선호와 발행 주체','권고 범위와 나머지 요건 SATA','권고에 따른 교육·보고 면제 INCORRECT', 'Case A의 초기 과정 구성','Case B의 current CPR','과정 구성·실기·증빙·CPR SATA','구두 증빙 INCORRECT', 'Case A의 calendar-year CE','Case B의 technician 2년 주기','CE 승인·직종·대체 불가 SATA','CE로 CPR/감독 대체 INCORRECT', 'Case A의 postlicensure 기산점','Case B의 certification과 교육','공통 면허 및 OR 자격 경로 SATA','national certificate의 주 면허 대체 INCORRECT', 'Case A의 additional OJT','Case B의 live/실기 구성','live·reaction·OJT SATA','reaction 교육 생략 INCORRECT', 'Case A의 응급약 order authority','Case B의 미서명 모델','실제 order·응급절차 SATA','막연한 응급지시 INCORRECT']

canonical_comparisons = {
 'MA-Q-0297':'canonical 문항은 CDTM inspection에서 current agreement/referral/consent 사본·primary setting·retrievability를 여러 보기로 나눈다. 배정의 기록 중심 항목과 같은 핵심 판단이며 종료 전 continuation 판단은 다룰 수 없다.',
 'MA-Q-0301':'canonical 문항도 community pharmacy의 physician 고용을 QA review 목적과 CPA 체결 목적으로 나눠 허용/금지를 묻는다. 주체·고용 목적·결론이 실질적으로 같다.',
 'MA-Q-0182':'canonical 문항은 gabapentin ADD stocking에서 certified PT/PTT와 pharmacist-verified stock·electronic validation을 구분한다. 인력 용어는 겹치지만 vaccination qualification/clinical scope와 사실·행위·근거가 다르다.',
 'MA-Q-0172':'canonical은 MH/SUD single-dose·first-dose·성인·patient-specific prescription의 허용 조합이다. 연령 및 별도 조건이라는 구조는 비슷하나 백신 state minimum/product 기준과 다른 투여 경로다.',
 'MA-Q-0348':'canonical은 700.003(F)의 emergency designation·인력 부족 판단·Commissioner order 및 practitioner instrument를 누적 요구한다. 배정은 Policy I.B의 표시와 다른 routine-vaccine 권고 경로로서 Commissioner 용어만으로 같은 권한이라 볼 수 없다.',
 'MA-Q-0407':'canonical은 일반 CE의 20시간·법률 2시간·home-study cap 계산이다. 배정의 초기 vaccination course 12+8+hands-on과 CPR 요건은 다른 자격 심사다.',
 'MA-Q-0173':'canonical은 Vivitrol repeat dose의 약물·처방 조건이 충족되어도 expired CPR이 남는 MH/SUD 사례다. CPR 독립 게이트는 공통이지만 배정은 vaccine course composition/evidence까지 묻는 백신 정책 경로다.',
 'MA-Q-0079':'canonical은 연간 CE 24+16시간과 carry-over 불가의 4시간 결손을 묻는다. 배정은 약사 immunization annual hour와 PT biennial maintenance의 다른 인력별 시계다.',
 'MA-Q-0237':'canonical은 PTT의 전화 처방 수신 금지를 묻고 500 trainee hours가 그 금지를 해제하지 않는다고 한다. 배정은 PT license 이후 500시간 또는 national certification이라는 백신 자격 경로다.',
 'MA-Q-0274':'canonical은 general PT training의 120 theory+120 practical 및 OJT guidelines 제출이다. 배정은 vaccine-specific 6시간 course·2시간 live·추가2시간 OJT로 다른 교육 목적·숫자·증빙이다.',
 'MA-Q-0325':'canonical은 emergency contraception may training과 COVID-drug shall training의 차이다. 배정은 vaccine/emergency medication 실제 standing order 및 unsigned model의 효력으로 다른 행위·권한이다.',
 'MA-Q-0128':'canonical은 revoked CSOS certificate로 oxycodone 주문을 공급할 수 있는지다. 서명/valid order 용어만 겹치며 백신 응급약 standing order의 대상·prescriber signature와 법적 체계가 다르다.',
}
default_comparisons = {
 'MA-REV-0065':'default는 CPA renewal 및 종료 continuity·written notice와 위임 제한을 한 사례에 적용한다. 배정은 두 사례 중 종료 또는 records를 표적으로 삼는 명시된 archive variant이며 추가 default 독립 사례로 세지 않는다.',
 'MA-RW-0039':'default는 superseded agreement 및 closed physician office 때문에 현재 사본을 pharmacy에서 못 내는 inspection 사례다. 배정의 Case B와 핵심 current-copy obligation이 겹치며 archive variant로만 이해해야 한다.',
 'MA-RW-0040':'default는 QA Director라는 직함 속에 CPA duties를 섞은 고용 목적 사례다. 배정의 고용 목적·명칭·QA 분리 판단과 같고 canonical MA-Q-0301도 같은 결정을 다룬다.',
 'MA-RW-0068':'default는 잠긴 약국 밖의 scheduled computer-only PTT training 감독 예외다. 배정의 PTT vaccine administration 금지와는 실제 행위 및 예외 경로가 다르다.',
 'MA-RW-0022':'default는 unchanged Schedule VI refill telephone authorization에서 full PT와 PTT를 나눈다. 배정은 vaccine administration 승인·supervision이므로 자격 명칭 외 법적 결정이 다르다.',
 'MA-RW-0041':'default는 CPR 만료 on-duty pharmacist와 off-site MOR 전화승인 아래 intern 투여다. 배정은 PTT 제외와 qualified PT의 on-duty approval 부재라 관련 감독 영역이나 결손 사실이 다르다.',
 'MA-RW-0042':'default는 8세 Gardasil 9 환자가 signed order의 9세 이상 범위 밖인 구체 사례다. 배정은 4세 주 경로와 5세 제품 범위를 일반화한 archive variant로 실제 제품과 order 조건을 더 제공하지 않는다.',
 'MA-EXP-0951':'default는 NDC/listing의 승인 증명 한계 및 EUA와 full approval 차이다. 배정은 actual Commissioner recommendation과 개인 선호의 구분이므로 추상적 scope 어휘 외 같지 않다.',
 'MA-RW-0043':'default는 54세 이식환자 Fluzone High-Dose를 현재 DPH order와 FDA65세 label 사이에 적용한다. 배정은 제품·대상·order 없이 Commissioner 권고 원칙을 묻는 archive variant다.',
 'MA-RW-0044':'default는 self-study16/live4지만 실기·시험·CPR은 갖춘 course 파일이다. 배정은 self-study20/live0/실기0와 별도 expired CPR 사례라 결손 구성 및 SATA 범위에 차이가 있다.',
 'MA-RW-0014':'default는 2026 직접 감독 약사의 2025 credit와 current CPR을 제시해 annual CE 1시간을 정한다. 배정은 실제 접종 약사와 PT의 다른 maintenance 시계를 함께 대조한다.',
 'MA-RW-0046':'default는 ExCPT full PT의 postlicensure100시간으로 OR 경로를 검증한다. 배정은 trainee600/full PT0와 PTCB 있으나 vaccine training 없음으로 기산점·credential·별도 training의 다른 결손을 함께 판단한다.',
 'MA-RW-0047':'default는 recorded6시간 course와 이미 완료한 documented OJT의 결합을 검토한다. 배정은 OJT 미완 및 별도 all-recorded/unsupervised 사례로 결손을 나누며 동일 archive 교육 family다.',
 'MA-RW-0048':'default는 signed vaccine order에 emergency instructions가 없고 unsigned model을 가진 clinic을 고친다. 배정도 실제 emergency authority, 미서명 모델, dose/route/EMS 절차라는 같은 사실과 결론을 반복한다.',
}

dup = {r['question_id']:r for r in read(BASE/'duplicate-measurement.json')['records']}
records=[]
duplicate_fail = {282,284,285,286,287,288,317,318,319,320}
for idx, r in enumerate(packet['records']):
 q=r['original_visible_content'];qid=q['question_id'];num=int(qid.rsplit('-',1)[1]);family=locators[qid]['family_id'];expected=list(expected_keys[idx]);stored=q['correct_choice_ids']
 assert expected==stored, (qid,expected,stored)
 choices=[];used=set();expl={}
 for c in q['choices']:
  f=copy.deepcopy(facts[c['text']]);assert f['family_id']==family
  used.update(f['source_ids']);authorities=[]
  for sid in f['source_ids']:
   a=copy.deepcopy(sources[sid]);a['exact_section']='M.G.L. c.112, §24B½(e)' if sid=='mgl-112-24bhalf-current' else f['exact_section'];authorities.append(a)
  choice=dict(choice_id=c['id'],option_text=c['text'],option_text_sha256=hashlib.sha256(c['text'].encode()).hexdigest(),statement_supported=f['statement_supported'],expected_selected=c['id'] in expected,finding_ko=f['finding_ko'],authorities=authorities)
  choices.append(choice)
  expl[c['id']]=dict(read_in_full=True,explanation_sha256=digest(q['explanation']['choice_analysis'][c['id']]),assessment='SUPPORTED',finding_ko='선택/비선택 및 INCORRECT 극성을 실제 키와 별도로 대조했다. '+f['finding_ko'])
 recdup=copy.deepcopy(dup[qid]);canon=recdup['canonical']['question_id'];default=recdup['default_public']['question_id'];sibling=recdup['public']['question_id']
 recdup['canonical']['comparison_ko']=canonical_comparisons[canon]
 recdup['default_public']['comparison_ko']=default_comparisons[default]
 recdup['public']['comparison_ko']=f'{sibling}의 stem·모든 보기·키·보이는 해설을 직접 읽었다. 같은 두 사례와 법적 명제를 공유하고 prompt/정답극성/일부 보기만 바꾼 명시적 연습 변형이다. 네 독립 clinical scenario로 세지 않는다. 이 사실만으로 자동 FAIL시키지 않았다.'
 recdup.update(status='RUN_AND_VISIBLE_COMPARATORS_READ', evidence_path=str(BASE/'nearest-visible-input.json'),evidence_sha256=sha(BASE/'nearest-visible-input.json'),measurement_path=str(BASE/'duplicate-measurement.json'),measurement_sha256=sha(BASE/'duplicate-measurement.json'), assigned_is_default=False, semantic_method='측정점수는 후보 탐색에만 사용. 위에 보존한 실제 fact/decision/wording 및 assignment default 맥락으로 별도 판단.')
 focus=focuses[idx];pass_item=num in {303,311}
 criteria=dict(jurisprudence_reasoning=num!=298,practice_plausibility=num not in {298,299,300},authentic_distractors=pass_item or num==319,wording_not_guessable=pass_item or num==319,reasoning_not_trivia=num!=298,natural_rule_combination=num not in {287,298},appropriate_drug_context=True,distinct_from_bank=num not in duplicate_fail,not_schedule_flashcard=True,public_style_without_copying=True)
 reasons={
  'jurisprudence_reasoning':f'{qid}는 {focus}에 대해 '+('개인 선호와 official 권고가 다르다는 문장 자체의 참을 묻는 데 치우쳐 법규 적용이 실질적으로 부족하다.' if num==298 else '직종·조건·권한 또는 의무를 해당 사실에 적용해야 한다. 법규 주제 자체는 실질적이다.'),
  'practice_plausibility':f'{qid}: '+('개인 선호 schedule을 Commissioner recommendation이라고 호칭한다는 Case B는 실제 처방·공문 확인 절차가 없는 작위적인 잘못이다.' if num in {298,299,300} else focus+'의 기록 검토·임상 배정·고용 또는 order 확인은 실제 약국에서 발생할 수 있다. 두 case 형식의 불필요성은 별도로 평가했다.'),
  'authentic_distractors':f'{qid}: '+('SATA의 모든 참 구성이 금지되는 것은 아니다. course composition/IM-SC 실기/file proof/current CPR라는 실제 독립 qualification gates를 각각 평가하게 한다.' if num==303 else '600 trainee와 500 postlicensure 시간의 기산점, 공통 PT 면허와 certification OR 경험, 별도 vaccination training을 혼동하는 실제적인 대안을 배치한다.' if num==311 else '네 보기 모두 실제 order/응급절차의 별도 필수요건이며 all-true SATA라는 이유로 오답 부족 판정을 내리지 않았다.' if num==319 else defects[num]),
  'wording_not_guessable':f'{qid}: '+('실기·증빙·초기 구성·CPR 네 보기의 길이와 한정 정도가 크게 치우치지 않고, 각각의 요건을 확인해야 선택 조합을 정할 수 있다.' if num==303 else '경력 기산점과 credential/교육의 서로 다른 조건을 확인해야 B,D를 남길 수 있다. 숫자 크기만으로 600시간 보기를 판단할 수 없다.' if num==311 else '각 보기가 구체적인 authority·내용·signature 요건을 진술하며 all-true 조합을 표현만으로 확정할 특별 신호는 없다.' if num==319 else defects[num]),
  'reasoning_not_trivia':f'{qid}: '+('개인 선호가 공식 발행 권고가 아니라는 언어상의 구분이 중심이라 법적 사실을 아는 깊이를 충분히 시험하지 않는다.' if num==298 else focus+'은 실제 결손 조건 또는 권한의 경계를 사례에 적용한다. 숫자가 있다는 이유만으로 trivia로 판정하지 않았다.'),
  'natural_rule_combination':f'{qid}: '+('A,C,D가 목적 제한을 세 가지 추상 문장으로 반복하므로 독립 규칙을 자연스럽게 조합하는 효과가 작다.' if num==287 else '실제 권고 범위·order·인력 조건을 서로 적용하기보다 개인 선호를 공식 권고로 부를 수 없다는 동어반복에 머문다.' if num==298 else focus+'에 연결된 조건을 같은 업무 흐름에서 검토한다. SBA의 단일 결정 자체를 다중 규칙 부족으로 실패시키지 않았다.'),
  'appropriate_drug_context':f'{qid}: '+('CDTM 종료·고용·기록 의무는 특정 약물명 없이도 판단 가능하므로 불필요한 상품명을 넣지 않은 것이 적절하다.' if family.startswith('CDTM') else '예방접종 업무가 법적 요건에 직접 관련된다. 이 질문의 자격·교육·연령/권고·명령 원칙을 판단하는 데 특정 브랜드를 더 알아야 하는 전제를 보태지 않았다.'),
  'distinct_from_bank':f'{qid}: '+(('canonical '+canon+' 또는 default '+default+'와 실제 행위·핵심 사실·필수 결론이 같은 부분이 있어 독립 새 문항으로서의 구별성이 부족하다. archive sibling 존재만으로 실패시킨 것은 아니다. ' if num in duplicate_fail else '가까운 comparator와 주제가 일부 겹치지만 target facts·authority pathway·선택 조합의 차이를 확인했다. 배정 item은 default에 없고 명시적 archive family variant이므로 sibling 존재만으로 실패시키지 않았다. ')+canonical_comparisons[canon]+' '+default_comparisons[default]),
  'not_schedule_flashcard':f'{qid}: 이 항목은 '+focus+'을 묻는다. 약물명만 보고 schedule을 분류하는 flashcard가 아니다.',
  'public_style_without_copying':f'{qid}: 직접 읽은 NABP public sample은 SBA/SATA/ordered-response 형식 설명으로만 사용했다. 이 stem·보기의 CDTM/백신 사례는 공개 sample의 CE 숫자 선택·Schedule II 목록·처방 만료순서 wording을 복제하지 않는다. Pre-MPJE/회상/상업 문항은 입력하지 않았다.',
 }
 realism_pass=all(criteria.values());assert realism_pass==pass_item
 legal=dict(existing_answer_correct='YES',stored_key=stored,independently_expected_key=expected,key_calculation_ko=(f'INCORRECT의 거짓 명제만 고른 결과 {expected}.' if 'INCORRECT' in q['stem'] else f'SATA에서 현재 근거로 참인 명제를 모두 고른 결과 {expected}.' if q['question_type']=='SATA' else f'요청된 사례에 옳게 적용되는 유일한 보기 {expected}.'),per_choice_findings=choices,authorities=[copy.deepcopy(sources[sid]) for sid in sorted(used)],verdict='KEEP',finding_ko=f'{focus}: 저장 키와 독립 계산 키가 일치한다. 모든 보기를 현재 공식 문서의 주체·조건·허용/의무·예외 및 범위와 대조했다. '+core_notes[family],blocker=None,original_explanation_review=dict(core_read_in_full=True,all_choice_rationales_read_in_full=True,learning_boundary_read=True,core_explanation_sha256=digest(q['explanation']['core_reasoning']),assessment='SUPPORTED_WITH_SCOPE_NOTES',core_finding_ko=core_notes[family],choice_analysis=expl),law_checked_date=review_date)
 realism=dict(verdict='PASS' if realism_pass else 'FAIL',decision='KEEP' if realism_pass else 'MAJOR_REWRITE',criteria=criteria,criterion_findings_ko=reasons,duplicate_review=recdup,finding_ko=('열 개 기준을 각각 확인했으며 전부 충족한다. 모두 참인 SATA도 실제 별도 요건을 검토하는 경우 허용된다.' if realism_pass else defects[num]),score_used_as_verdict=False)
 records.append(dict(question_id=qid,record_sha256=r['record_sha256'],visible_content_sha256=r['visible_content_sha256'],family_id=family,read_scope=dict(original_stem=True,every_choice=True,choice_count=len(q['choices']),stored_key=True,korean_core_reasoning=True,every_korean_distractor_rationale=True,learning_boundary=True,hidden_author_truth=False,prior_author_or_independent_reports=False,input_path=str(BASE/'assigned-visible-input.json'),input_sha256=sha(BASE/'assigned-visible-input.json')),legal_review=legal,realism_review=realism,safe_hold_recommended=not realism_pass,release_eligible=False,canonical_release_credit=0,author_review_credit=0,required_next_action_ko=('이 legacy 독립 평가만으로 canonical admission/release를 승인하지 않는다. 향후 편입 시 canonical workflow를 별도로 수행한다.' if realism_pass else '현재 키와 원문은 보존한다. 현실성 결함을 해결한 별도 candidate를 editor가 작성하고 새 current hash에서 fresh independent 검토를 받기 전 시험형 default 추천에 넣지 않는다.'),checked_at=now))

read_docs=[]
for p in sorted((ROOT/BASE/'context'/'review-methodology').iterdir()):
 read_docs.append(dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),read_by_this_session=True))
for name in ['progress-at-assignment.json','default-ids-at-assignment.json','provenance.json']:
 p=BASE/'context'/name;read_docs.append(dict(path=str(p),sha256=sha(p),read_by_this_session=True,historical_assignment_snapshot=True,legal_authority=False))
style=read('data/exam_style/mpje_style_profile.json');blueprint=read('data/blueprint.json')
style_memo=dict(reviewed_at=now,reviewer=actor,scope='Public NABP format/competency only. No legal authority and no Pre-MPJE/commercial/recalled input.',sources=read(BASE/'public-style-retrieval.json'),observations_ko=['공개 sample의 SBA·SATA·ordered-response 형식과 select all/one 구분을 직접 읽었다. sample은 시험 영역 대표 표본이 아니라 형식 예시라고 설명한다.','현 공식 exam page는 adaptive selected-response 120문항/2.5시간을 설명하고 competency page는 2027-03-01부터 새 outline 적용을 고지한다. 현 배정 profile의 pre2027 창과 일치한다.','공개 sample wording을 질문 또는 해설로 재배포하지 않으며 URL·payload SHA 및 이 직접 작성한 메모만 repository에 보존한다.'])
write(BASE/'public-style-memo.json',style_memo)
report=dict(schema_version='independent-legacy-review/1',stage='independent-legacy',job_id=assignment['job_id'],independent_of_authors=True,auditor='GPT',auditor_instance=instance,actor_provenance=dict(actor_id=actor,session_id=actor),canonical_audit=False,canonical_release_credit=0,author_review_credit=0,reviewed_at=review_date,reviewed_at_aware=now,question_hashes=assignment['question_hashes'],context=dict(read_docs=read_docs,AGENTS_search='No AGENTS.md found in this worktree or /workspace during initial file discovery.',assignment_path=str(BASE/'assignment.json'),assignment_sha256=sha(BASE/'assignment.json'),visible_input_path=str(BASE/'assigned-visible-input.json'),visible_input_sha256=sha(BASE/'assigned-visible-input.json'),input_integrity='Re-exported through native visible whitelist in memory and compared exact packet; digest verifies all 40 whole canonical record hashes without printing hidden original objects.',independence_statement_ko='이 실제 새 session은 원저자·기존 감사 보고서 및 hidden_statement_truth/conditional facts/proposed_action_supported를 읽지 않았다. source-locators는 URL 발견용으로만 사용하고 공식 PDF 본문에서 모든 법적 명제를 독립 판정했다.'),style_profile=dict(profile_id=style['profile_id'],content_version=style['content_version'],content_hash=style['content_hash'],file_path=str(BASE/'context/review-methodology/mpje_style_profile.json'),file_sha256=sha(BASE/'context/review-methodology/mpje_style_profile.json'),schema_path=str(BASE/'context/review-methodology/exam_style_profile.schema.json'),schema_sha256=sha(BASE/'context/review-methodology/exam_style_profile.schema.json'),public_read_memo_path=str(BASE/'public-style-memo.json'),public_read_memo_sha256=sha(BASE/'public-style-memo.json')),blueprint=dict(blueprint_id=blueprint['blueprint_id'],content_version=blueprint['content_version'],content_hash=blueprint['content_hash'],file_path=str(BASE/'context/review-methodology/blueprint.json'),file_sha256=sha(BASE/'context/review-methodology/blueprint.json'),schema_path=str(BASE/'context/review-methodology/blueprint.schema.json'),schema_sha256=sha(BASE/'context/review-methodology/blueprint.schema.json')),sources=list(sources.values()),records=records,summary=dict(assigned=40,originals_read=40,choices_directly_read=160,legal_keys_assessed=40,legal_KEEP=40,existing_answer_correct_YES=40,realism_PASS=sum(r['realism_review']['verdict']=='PASS' for r in records),realism_FAIL=sum(r['realism_review']['verdict']=='FAIL' for r in records),canonical_release_credit=0,author_review_credit=0,default_assigned_ids=0,default_negative_ids=[],positive_summary_is_release_approval=False),limitations_ko=['현재 공식 게시본을 실제 읽은 날짜와 printed Register/개정일을 구분했다. 별도 commencement가 없는 source는 effective_date UNKNOWN이며 미래 변경을 보증하지 않는다.','US Code 첫 URL과 공백을 빠뜨린 MGL section URL은 HTTP404였다. 둘 다 법률 확인으로 세지 않았다. US Code는 별도 govinfo 공식 법전 및 현 HHS index가 연결한 Twelfth Declaration을 실제 읽었고, MGL은 chapter index에서 공백이 포함된 실제 section URL을 찾아 §24B½(e)의 현재 공식 본문으로 고용 규정을 확인했다. US Code 2024판은 조건부 구조의 보조 근거이지 2026의 모든 개정·연방 예외의 독립 완전 검증이 아니다.','NABP raw/text는 /tmp에만 있고 public commit에는 URL·SHA·직접 작성 memo만 있다. Pre-MPJE 페이지나 문항은 열지 않았다.','archive family 변형은 변형임을 인정하고 default 맥락을 확인했다. duplicate 점수는 후보 찾기용으로만 사용했다.','모든 키가 법적 근거와 일치하더라도 38개 현실성 실패를 긍정 요약으로 덮지 않는다. 현재 검토는 canonical audit 또는 release가 아니다.'])
report_path=Path('reports/full-corpus-review/independent-phase11-c-review.json')
write(report_path,report)
print(json.dumps(report['summary'],ensure_ascii=False))
print(str(report_path),sha(report_path))
