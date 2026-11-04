import json,hashlib,datetime,shutil,inspect,sys
from pathlib import Path
root=Path('/workspace/independent-wave14-d');out=root/'reports/full-corpus-review/phase14-d-evidence';prefix=out.relative_to(root).as_posix()+'/'
now=datetime.datetime.now(datetime.timezone.utc).isoformat();date=now[:10]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
source_notes={
'247-13':('247 CMR 13.02 (qualified nuclear pharmacist), 13.03, 13.05(1)-(6),(12)(e), 13.06','핵약학 자격은 Board letter와 추가 교육·경험을 요구한다. 취득·처분 기록은 최소 3년이며 환자 이름이 처음 미상인 예외는 조제 후72시간 내 이름·주소 확보를 요구한다. 표지의 방사능량은 calibration시점과 연결된다.','공식 게시 PDF에 시행·최종개정일을 확인할 수 없어 특정 시행일 미확정. 2026-11-04 현재 게시 바이트를 검토했으며 USP825 전체 실무나 별도 radiation license 충족 여부를 인증하지 않는다.'),
'247-15':('247 CMR 15.02(1)(a)-(f); 15.03(1),(2)(a)-(b),(3)(a)-(b); 15.04(1)-(3)','CQI는 탐지·기록·평가·예방과 연례 교육을 요구한다. 원인·시스템 요인 분석과 측정지표가 필요하다. QRE 최초 기록은 발견/전달 후24시간이며 환자통지와 별도이다. QRE기록은 보고일부터 최소2년이다.','Mass. Register1536, 12/6/2024 게시 통합본; 조문별 최초 시행일 재구성은 하지 않았다.'),
'247-20':('247 CMR 20.02(1)-(5), 20.06(2)-(3), 20.07(3)','Resident MOR의 심각한 부상·사망 관련 부적절 조제보고는 해당 부상·사망 발견 후7businessdays이며 CQI와 병행한다. 관련기록은 Board보고부터5년이다. Nonresident는20.02제외와20.07(3)별도 보고를 함께 읽어야 한다. 결함조제품 보고는 환자상해와 다른 발동요건이다.','Mass. Register1536, 12/6/2024 게시본. statute39D(b)의 prompt 및 발견기준과 규정20.02(1)의 seriousinjury 발견기준 차이는0993/94/96사실상 동시 발견으로 해소된다.'),
'policy-definitions':('Board Policy 2025-02 II.F (QRE), II.G (SADE), II.H (Serious Disability), II.I (Serious Injury), pp.2-3','QRE는 환자가 받은 잘못된 조제이며 사전 차단 near miss와 구분된다. SADE는 preventable 및 열거된 중대한 결과를 갖는다. Seriousinjury는 병원/ED에서 추가치료·검사·모니터링도 포함하여 입원·사망만의 기준이 아니다.','Adopted8/7/2025. Board정책 정의이며 법률/규정과 동일한 권위라고 표시하지 않는다.'),
'247-9':('247 CMR 9.01(12); 9.04; 9.05','결함·오염·adulterated등 약품의 조제·배포 금지가 환자상해 후에만 적용되는 것은 아니다. 대체조제에는 제품특성과 관련 주 규정 판단이 남는다.','Mass. Register1536,12/6/2024 게시본; 검토 범위는 명시한 조항으로 제한.'),
'mgl39d':('M.G.L. c.112 §39D(b),(c),(e)','심각한 부상·사망을 초래한 부적절 조제는 합리적·실무상 가능한 즉시, 최대7businessdays내 보고한다. 결함/결함가능 조제품은 상해 발생을 기다리지 않고 즉시 회수·격리한다.','공식 현재 법률웹페이지 확인; 개별 개정법 commencement 일자 별도 확정하지 않음.'),
'mgl94c9':('M.G.L. c.94C §9(a),(b), pharmacist limitations by c.112 §24B½ and c.94C §7(g)','법은 약사 행위를 특정 주법상 범위로 한정한다. 승인품 offlabel사용이 직종에 포괄적 독립처방권을 부여한다는 결론은 나오지 않는다.','현재 공식 조문; 예외별 약사처방 경로 전체를 부정하지 않으며 offlabel이라는 사실만의 권한발생을 부정한다.'),
'fda-applications':('Types of Applications: IND, NDA, ANDA, Biologic License Application headings','IND는 연구를 위한 주간운송 승인요건 예외 경로이며 일반 판매승인과 다르다. NDA제출과 승인 구별, ANDA generic제품 승인, BLA생물제품 허가경로를 확인했다.','FDA페이지 contentcurrent10/23/2014; 현재 게시 페이지의 일반 경로 설명이며 특정 제품승인을 확인한 것은 아니다.'),
'fda-otc':('Drug Application Process for Nonprescription Drugs: introductory two pathways; Drug Application Process','OTC는 application(NDA/ANDA)와 OTCmonograph 두 경로가 있으며 application경로에서는 FDA승인 전 판매할 수 없다.','Content current05/21/2026; 개별 OTC제품 monograph 적합성은 검토하지 않았다.'),
'fda-ndc':('National Drug Code Directory: About the NDC directory','NDC directory는 승인/미승인제품을 함께 포함하며 NDC부여나 등재만으로 FDA승인을 뜻하지 않는다.','Contentcurrent03/04/2026; 개별 제품의 approval record를 조회한 것은 아니다.'),
'fda-eua':('About Emergency Use Authorizations (EUAs); conditions and letter-specific declaration references','EUA는 미승인제품 또는 승인품 미승인용도에 적용될 수 있는 별도 긴급경로이다. 대상과 조건·현재 authorization을 확인해야 하며 무제한 fullapproval과 같지 않다.','현재공식페이지. 제품별 EUA 및 장래 종료 공고의 적용 여부를 판정하지 않았고 일반적 법적 구별만 검토.'),
'fda-dscsa':('DSCSA Requirements for Pharmacists: Confirm Entities; Receive Store Provide Tracing; Investigate Handle Suspect/Illegitimate','공급자 자격 확인, tracing정보6년보존, specificpatientneed 거래조건, suspect제품 격리·조사와 illegitimate 통지를 확인했다.','Contentcurrent06/12/2024; 일반 설명은2026면제결정과 함께 읽으며 거래history 종료와 구체적 면제범위를 무시하지 않는다.'),
'fda-exemptions':('FDA Grants Exemptions to Small Dispensers; Requesting Waiver or Exemption; What to Include','Small eligibility는 법정/결정상 기업인원 기준으로 판단하고 개별신청만으로 승인된 면제효과가 생기지 않는다. 면제종류·기간을 구별해야 한다.','Contentcurrent08/26/2026;2026letter와 현재적용 시작일을 구별. 문항은 날짜 계산을 묻지 않음.'),
'fda-notify':('Notify FDA within 24 Hours; Notifying FDA; Terminating a Notification','Illegitimate 결정후24시간 내 FDA와 적절한 immediatepartners통지. FDA3911은 이 통지용이고 DEA106대체양식이 아니다. 격리는 임의의 공간확보 목적 해제할 수 없다.','Contentcurrent06/12/2024;3911platformpreferred/emailForm3911대안이므로 paper3911만 의무라고 해석하지 않는다.'),
'fda-recalls':('Class I, Class II, Class III recall; Market withdrawal','ClassI는 seriousadversehealthconsequence/death의 합리적 가능성, III는 위해가능성 낮은 단계이다. 시장철수는 FDA법적조치 대상이 아닌 경미한위반/비위반과 구분한다.','Contentcurrent03/20/2026; 특정 recall notice 내용은 문항가정만 검토.'),
'fda-recall-enforce':('Important Note; report label definitions: Classification, Code Information, Distribution Pattern, Recall Initiation Date','Recall은 FDA분류보다 먼저 개시될 수 있고 분류게시를 기다리는 이유가 되지 않는다. 위험class와 lotcode·distribution은 서로 다른 정보다.','Contentcurrent02/14/2025; 주어진notice를 따르는 결론이며 임의 환자중단을 권하지 않는다.'),
'gov-dscsa':('21 U.S.C. §360eee-1(d)(1)(A)(ii)-(iii),(d)(2)-(4),(g),(k)','Dispensertracing기록6년, authorizedpartner, suspect격리·조사, illegitimate결정후24시간통지가 각각 독립된 의무임을 원문으로 읽었다.','2024UnitedStatesCode판;2026FDA현재설명/면제letter로보완. 이후 모든 개정 여부를 annual판만으로 인증하지 않는다.'),
'gov353b':('21 U.S.C. §353b(b)(5)','Outsourcingfacility adverseevent보고는21CFR310.305형식/내용에 따라야 하는 별도 연방경로이다.','2024USCode판;currenteCFR310.305및FDA503Bguidance로보완.'),
'fda503b':('Adverse Event Reporting for Outsourcing Facilities Under Section503B: II.B; III.A, pp.3-5','연방503B에서는 serious와unexpected를 함께 평가한다. MApreventableSADE정의와 동일하지 않으며 FDA는 더넓은 seriousevent보고를권고하지만 의무와구분한다.','FDA최종guidanceNovember2015;2026-11-02eCFR310.305현재본과대조.'),
'fda-orange-preface':('Orange Book Preface 46th Edition §§1.2 Pharmaceutical Equivalents/Alternatives/Therapeutic Equivalents;1.5;1.6','TE는 동일active·dosageform·route등 제품기준을 요구하고 ER/IR은 pharmaceuticalalternatives가 될수있다. ANDA승인 하나가 unrelatedroute/form 전체대체허가가 아니다.','FortysixthEdition현재게시preface;개별제품TE코드는 조회하지 않았으며 MA대체조제조건을 대체하지 않는다.'),
'fda-smallletter':('FDA letter issued2026-08-06 pp.1-3; limited sections582(d)(4),582(g)(1), eligibility footnotes14-16','2026-11-27부터2027-11-27까지 특정요건을 면제하며 다른582의무에는 적용되지 않는다. 회사전체25이하fulltimepharmacists/technicians와기준일을 분리하고 예전면제의2026-11-27까지적용도확인했다.','Issued2026-08-06,extensioncommences2026-11-27;검토일11/04에는장래연장을현재시행으로표시하지않음.'),
'ecfr7-20261102':('21 CFR7.3(g),(h),(j),(k),(m);7.42(a)(2);7.49','Recall/marketwithdrawal/stockrecovery는 실제유통·통제·위반조건으로나뉜다. Correction은물리이동없이가능하다. Class는위험도이며전달된notice조치를지연할근거가아니다.','eCFRlatestissue2026-11-02;11/04요청은futureissue404였으며latest11/02로재조회. 조문개별시행일은history에의해다를수있다.'),
'ecfr310-20261102':('21 CFR310.305(a),(b),(c)(1)-(2)','Adverseexperience는 정상professionaluse중에도발생가능하다. Serious와unexpected는별도정의이고15dayalert조건이다.새정보에대한followup도있어처음의clinicaldescription으로평가가고정되지않는다.','eCFRlatestissue2026-11-02;새로운11/04issue를확인했다고주장하지않음.'),
'nabp-sample':('Public MPJE Sample Questions: format introduction; multiple choice, multiple response, ordered response','공개sample은형식예시이며내용영역대표표본이아니다. 단일선택·복수선택지시의명료성과동일판단구조의신규표현을비교했으며보호된PreMPJE는열지않았다.','Publicsample2020/07URL;styleonly,legalcredit0,publicrepository에는자체요약만보존.'),
'nabp-competency':('MPJE Competency Statements: pre2027notice;areas1-4,especially2.5,3.7,4.1,4.2','Pre2027영역비중22/33/24/21과연방·주법상황적용목표를확인했다.2027-03-01새outline경계를유지한다.','현재페이지2026-11-04조회;시험범위이해용,법률권위아님.'),
'nabp-format':('Take the MPJE Exam: 2.5hour,120computerbasedquestions,adaptiveselectedresponse;SampleItems','120문항150분과selectedresponse형식을확인했다. 이페이지의PreMPJE링크를열지않았으며공개sample만비교했다.','현재페이지2026-11-04조회;styleonly,lawcredit0.')}
failed={k for k in ['21usc360eee1','21usc353b','cfr7-3','cfr314-80','ecfr7','govcfr7-3','govcfr310-305','ecfr7-current','ecfr310-current']}
sources={}
for p in sorted((out/'sources').glob('*.meta.json')):
 m=json.load(open(p));sid=m['source_id'];ok=sid not in failed
 if ok:section,note,version=source_notes[sid]
 else:section='Failed retrieval; no substantive authority coverage';note='조회실패 또는HTTP200지만조문없음/PageNotFound여서법적확인으로세지않았다. 성공한공식대체경로와별도구별.';version='NOT_VERIFIED_THIS_ATTEMPT'
 raw=Path('/tmp/phase14-d-private')/(sid+'.raw');txt=raw.with_suffix('.txt')
 assert sha(raw)==m['raw_sha256'] and sha(txt)==m['text_sha256']
 memo=dict(source_id=sid,reviewed_at=now,official_url=m['official_url'],exact_section=section,own_fact_check_memo_ko=note,effective_date_or_version=version,substantive_content_verified=ok,retrieval_metadata=m,public_raw_redistribution=False,retention_note='원payload및추출text는/tmp사적임시파일만존재;repository에는이자체memo와metadata만보존. raw/textSHA는조회식별자이며공개retainedbytes검증은memo/metadata에한함.')
 mp=out/'sources'/(sid+'.memo.json');write(mp,memo)
 d=dict(m,exact_section=section,law_checked_date=date,effective_date_or_version=version,substantive_content_verified=ok,evidence_path=mp.relative_to(root).as_posix(),evidence_sha256=sha(mp),metadata_path=p.relative_to(root).as_posix(),metadata_sha256=sha(p),public_evidence_mode='RETAINED_OWN_FACT_CHECK_MEMO_AND_METADATA_ONLY',limitation_ko=version)
 sources[sid]=d
# Exact retained methodology snapshots, without historical reviews.
context=[]
for rel in ['docs/RELEASE_POLICY.md','docs/AUDIT_WORKFLOW.md','docs/SOURCE_USE_POLICY.md','docs/QUESTION_AUTHORING_STANDARD.md','docs/INDEPENDENT_LEGACY_REVIEW_RUNBOOK.md','data/exam_style/mpje_style_profile.json','data/blueprint.json','schemas/exam_style_profile.schema.json','schemas/blueprint.schema.json']:
 target=out/'methodology'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/rel,target);context.append(dict(original_path=rel,evidence_path=target.relative_to(root).as_posix(),evidence_sha256=sha(target)))
write(out/'methodology-manifest.json',dict(reviewed_at=now,actor='/root/independent_wave14_d',files=context,cloud_runtime_skill_read=True,environment_status='observations_current true; network unrestricted/enforced; VPN false',firecrawl_search_attempt='insufficientcredits;noqueryrun;normalproxyTLSofficialurllibfallback',forbidden_material_read=False))
write(out/'source-descriptors.json',list(sources.values()))
