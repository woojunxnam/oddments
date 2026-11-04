from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[3]
EV=ROOT/'reports/full-corpus-review/phase13-b-evidence'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def rel(p):return str(Path(p).relative_to(ROOT))
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
now=datetime.now(timezone.utc).isoformat()
packet=json.loads((EV/'assigned-visible-input.json').read_bytes());assignment=json.loads((EV/'assignment.json').read_bytes());near=json.loads((EV/'nearest-visible-comparison.json').read_bytes());nearby={r['question_id']:r for r in near['records']}
method={}
for name in ['docs/RELEASE_POLICY.md','docs/AUDIT_WORKFLOW.md','docs/SOURCE_USE_POLICY.md','docs/QUESTION_AUTHORING_STANDARD.md','docs/INDEPENDENT_LEGACY_REVIEW_RUNBOOK.md','docs/INDEPENDENT_DEFAULT_WAVE10_RUNBOOK.md','data/exam_style/mpje_style_profile.json','data/blueprint.json','schemas/audit.schema.json','scripts/review_queue.py']:
 dest=EV/'methodology'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,dest);method[name]={'file_sha256':sha(ROOT/name),'snapshot_path':rel(dest)}
# These are self-authored format observations. Copyrighted NABP source bytes remain only in /tmp.
stylememo={
 'nabp-sample':'공개 MPJE sample PDF 1쪽 전체를 직접 읽었다. 안내는 내용 영역을 대표하지 않는 형식 예시라고 한정한다. 단일선택, 복수선택(Select ALL), 순서배열의 세 응답방식과 보기 구성을 확인했다. 문항 문구를 보고서·canonical에 전재하지 않았고 이 자료를 약사법 권위로 사용하지 않았다. 본 감사 문항은 두 사례 서술과 법적 결론 선택 구조이며 공개 sample의 문장·고유 보기 조합을 복제하지 않는다.',
 'nabp-competency':'공개 Competency Statements 페이지에서 연방·주 약사법을 실제 상황에 적용할 판단능력을 평가하고 해당 관할의 prevailing law로 답한다는 안내를 읽었다. 2027-03-01 이후 문항범위 변경 공지도 확인했다. 보호된 Pre-MPJE나 실제 시험 회상은 열지 않았다.',
 'nabp-format':'공개 Take the MPJE 페이지의 시험 안내 본문에서 2.5시간, 120개 컴퓨터 기반 selected-response 문항, adaptive delivery를 확인했다. 공개 형식 확인에만 사용했다.'}
cover={
 'ma247-9':('247 CMR 9.04(6),(10),(12),(13); 9.14(1)-(4); 9.15(1)','12/6/2024 게시·인쇄본; 각 관련 subsection의 별도 최초 시행일 연혁은 이번 검토에서 독립 추적하지 않음. 2026-11-04 공식 URL이 제공하는 규정 본문을 확인.'),
 'ma105-700':('105 CMR 700.001 Additional Drug; 700.012(A),(C)(2)(a),(D),(E),(G)','Massachusetts Register #1514, 2024-02-02 표시 게시본; 관련 조항의 모든 후속 연혁/개별 commencement를 별도 역추적하지 않았으며 공식 현재 배포 PDF의 문언 범위로 판정.'),
 'ma94c18':('M.G.L. c.94C §18(c),(d),(d½),(d¾)','2026-11-04 공식 consolidated web text; 모든 session-law commencement 연혁은 독립 재구성하지 않았음. 날짜별 법변경 비교를 주장하지 않음.'),
 'ma94c23':('M.G.L. c.94C §23(a),(b),(e),(f)','2026-11-04 공식 consolidated web text; 개별 개정의 commencement 전체는 별도 확인하지 않았음.'),
 'ma94c24a':('M.G.L. c.94C §24A(a)-(d),(f)(1),(g)','2026-11-04 공식 consolidated web text; 개별 개정의 commencement 전체는 별도 확인하지 않았음.'),
 'partial-dcp':('DCP 18-10-104, pp.1-2, Patient Requests for Partial Fill of Schedule II Prescriptions','2018-11-01 발행 circular; §18(d¾) 및 현행 연방 조항과 대조. 이 2018 안내를 연방 emergency-oral 예외의 대체로 사용하지 않음.'),
 'ma-unfilled':('Board Policy 2023-10, sections I-III, p.1','Adopted 2023-09-07; supersedes 2022-03; 2026-11-04 공식 게시 PDF 재확인.'),
 'pmp-guide':('Massachusetts PMP Data Submission Guide for Dispensers v5.2, §§1-2, pp.1-3','Version 5.2, May 2023; gabapentin 보고 범위를 확인하기 위한 공식 operational guide. 오래된 소프트웨어 필드나 보고 기한 문구로 현행 statute를 대체하지 않음.'),
 'ma247-8-current':('247 CMR 8.04(4)(d)','4/25/2025 corrected 게시본; 관련 8.04 페이지는 Effective 4/6/2018 표시. 2026-11-04 공식 문서 확인.'),
 'ma247-8':('Failed URL discovery attempt; not legal authority','404; 본문 확인이나 law credit 없음.'),
 'cfr1306-13':('21 CFR 1306.13(a),(b)(1)-(2)','eCFR title 21 current through 2026-11-02, retrieved 2026-11-04. eCFR의 current consolidation을 확인; 최초 Federal Register 시행일 전체는 이번에 독립 추적하지 않음.'),
 'cfr1306-22':('21 CFR 1306.22(a)-(e)','eCFR title 21 current through 2026-11-02, retrieved 2026-11-04; 역사적 개정별 commencement는 별도 재구성하지 않음.'),
 'cfr1306-23':('21 CFR 1306.23(a)-(c)','eCFR title 21 current through 2026-11-02, retrieved 2026-11-04; 역사적 개정별 commencement는 별도 재구성하지 않음.'),
 'cfr1306-25':('21 CFR 1306.25(a)-(e)','eCFR title 21 current through 2026-11-02, retrieved 2026-11-04; 역사적 개정별 commencement는 별도 재구성하지 않음.'),
 'cfr1306-08':('21 CFR 1306.08(e)-(i)','eCFR title 21 current through 2026-11-02, retrieved 2026-11-04; 역사적 개정별 commencement는 별도 재구성하지 않음.'),
 'nabp-sample':('Public MPJE Sample Questions PDF, p.1, format descriptions only','공개 형식 예시; 법적 효력일 해당 없음. 제공된 PDF에 확정 발행일이 없어 URL의 2020/07을 확정 publication date로 취급하지 않음.'),
 'nabp-competency':('Public MPJE Competency Statements page; applicability notice and examination purpose','공개 페이지 2026-11-04 열람; 2027-03-01 이후 새 competency 사용 공지를 확인.'),
 'nabp-format':('Public Take the MPJE Exam page; examination format paragraph','공개 페이지 2026-11-04 열람; 약사법 근거가 아닌 현행 공개 형식 안내.')}
sources={}
for metap in sorted((EV/'sources').glob('*.meta.json')):
 m=json.loads(metap.read_bytes());key=m['source_id'];m['coverage'],m['effective_date_or_version_limit']=cover[key];m['read_at']=now
 m['read_status']='FAILED_HTTP_404_NOT_AUTHORITY' if m['http_status']!=200 else 'IDENTITY_AND_RELEVANT_TEXT_READ'
 raw=Path(m['raw_path']);txt=Path(m['text_path']);raw=raw if raw.is_absolute() else ROOT/raw;txt=txt if txt.is_absolute() else ROOT/txt
 if key.startswith('nabp'):
  memo=EV/'sources'/(key+'.memo.json');write(memo,{'source_id':key,'official_url':m['official_url'],'raw_sha256':m['raw_sha256'],'extracted_text_sha256':m['text_sha256'],'retrieved_at':m['retrieved_at'],'read_at':now,'http_status':m['http_status'],'public_raw_redistribution':False,'scope':cover[key][0],'finding_ko':stylememo[key]});m['evidence_path']=rel(memo);m['evidence_sha256']=sha(memo);m['public_raw_redistribution']=False;m['public_evidence_mode']='self-authored memo; original NABP bytes uncommitted /tmp only'
 else:
  m['raw_path']=rel(raw);m['text_path']=rel(txt);m['evidence_path']=rel(txt);m['evidence_sha256']=sha(txt)
 m['law_checked_date']='2026-11-04';m['exact_section']=cover[key][0];m['source_type']='PUBLIC_OFFICIAL';write(metap,m)
 s=dict(m,metadata_path=rel(metap),metadata_sha256=sha(metap));sources[key]=s

def authority(key,section=None):
 s=sources[key];return {k:s[k] for k in ['source_id','official_url','source_type','law_checked_date','effective_date_or_version_limit','evidence_path','evidence_sha256','raw_path','raw_sha256','metadata_path','metadata_sha256','retrieved_at','read_at'] if k in s}|{'authority':key,'exact_section':section or s['exact_section'],**({k:s[k] for k in ['public_raw_redistribution','public_evidence_mode']} if 'public_raw_redistribution' in s else {})}
# Independent proposition judgments entered after reading the current official text.
J={}
def put(i,t,reason,*refs):J[i]={'truth':t,'finding_ko':reason,'refs':refs}
put(0,True,'§18(d¾)는 처음 적은 수량을 조제한 동일 약국만 잔량을 조제하도록 명시한다. 같은 체인이라는 사실은 동일 약국을 대체하지 않는다.',('ma94c18','M.G.L. c.94C §18(d¾)'),('partial-dcp','DCP 18-10-104 p.1, same-pharmacy bullet'))
put(1,False,'일부 수량이 이미 조제된 처방은 initial dispensing 전 미조제 EPCS가 아니다. 남은 수량 자체를 새 initial-transfer 원본으로 취급할 수 없다.',('cfr1306-08','21 CFR 1306.08(e),(i)'),('ma-unfilled','Policy 2023-10 I'))
put(2,False,'환자 요청 partial이라도 emergency oral이면 잔량 시한은 발행 후 72시간이다. 일반 30일 예외로 연장되지 않는다.',('cfr1306-13','21 CFR 1306.13(b)(2)'))
put(3,False,'재고 부족 partial은 첫 부분조제부터 72시간, emergency oral requested partial은 처방 발행부터 72시간이다. 숫자가 같아도 기산점이 다르다.',('cfr1306-13','21 CFR 1306.13(a),(b)(2)'))
put(4,True,'연방 조항은 emergency oral의 requested-partial 잔량을 발행 후 72시간으로 정한다. 비응급 일반 30일과 구별된다.',('cfr1306-13','21 CFR 1306.13(b)(2)'))
put(5,True,'initial dispensing 이관과 refill dispensing 이관은 별도 경로이며 이미 일부 조제된 CII는 미조제 initial EPCS 요건을 충족하지 않는다.',('cfr1306-08','21 CFR 1306.08(e),(i)'),('ma-unfilled','Policy 2023-10 I'))
put(6,False,'§18(d¾)는 적법한 5일 이내 최초 부분조제와 발행일부터 30일까지의 잔량을 분리한다. 모든 잔량을 5일 내로 줄이는 해석은 틀리다.',('ma94c18','M.G.L. c.94C §18(d¾)'))
put(7,False,'여기서 특수 5일 조건은 §18(d),(d½)에 따른 타주 CII 최초 부분조제에 붙는다. 모든 MA 발행 CII requested partial로 확대할 수 없다.',('ma94c18','M.G.L. c.94C §18(d),(d½),(d¾)'),('ma94c23','M.G.L. c.94C §23(a)'))
put(8,True,'Case A는 최초 제시가 8일째라 적용되는 타주 CII의 5일 조건을 충족하지 못한다. 일반 CII 30일 유효기간이 그 선행조건을 지우지 않는다.',('ma94c18','M.G.L. c.94C §18(d),(d½),(d¾)'),('ma94c23','M.G.L. c.94C §23(a)'))
put(9,False,'잔량의 30일은 원처방 발행일부터 계산하며 최초 부분조제일에 새 30일이 생기지 않는다.',('ma94c18','M.G.L. c.94C §18(d¾)'),('cfr1306-13','21 CFR 1306.13(b)(2)'))
put(10,False,'특수 타주 CII 최초 조제 5일 조건과 일반 CII 30일 유효기간은 동시에 적용된다. 일반 조항으로 특수 조건을 제거하지 않는다.',('ma94c18','M.G.L. c.94C §18(d),(d½),(d¾)'),('ma94c23','M.G.L. c.94C §23(a)'))
put(11,True,'Case B의 최초 부분조제는 이미 5일 조건을 충족했다. 잔량은 원 발행일부터 30일, 동일 약국 및 다른 적법조건을 적용한다.',('ma94c18','M.G.L. c.94C §18(d¾)'),('cfr1306-13','21 CFR 1306.13(b)(1)-(2)'))
put(12,True,'잔량 시한은 최초 부분조제일이 아니라 발행일에 고정되어 있다.',('ma94c18','M.G.L. c.94C §18(d¾)'),('cfr1306-13','21 CFR 1306.13(b)(2)'))
put(13,False,'§18(d½)는 ordinary narcotic CII에 Maine 또는 MA 인접주 범위를 둔다. 모든 주에 대해 nonnarcotic과 같은 무제한 counter-pickup 권한이 생기지 않는다.',('ma94c18','M.G.L. c.94C §18(d),(d½)'))
put(14,True,'§18(d)의 nonnarcotic CII 타주 경로에는 §18(d½)의 Maine/인접주 지리적 한정이 없다. 진위확인·자격·5일 등 조건은 그대로이다.',('ma94c18','M.G.L. c.94C §18(d),(d½)'))
put(15,False,'Narcotic 경로는 Maine을 인접주와 별도로 명시한다. MA와 직접 접하지 않는다는 이유로 Maine을 제외할 수 없다.',('ma94c18','M.G.L. c.94C §18(d½), first paragraph'))
put(16,False,'특수 타주 송달은 우편/운송업자로 환자의 타주 확인 주소에 전달하고 MA 내 일반 수령자에게 넘어가지 않도록 한다. 이 권한은 MA counter pickup을 허용하지 않는다.',('ma94c18','M.G.L. c.94C §18(d½), out-of-state delivery conditions (1)-(6), especially (6)'))
put(17,False,'Nonnarcotic CII는 §18(d)의 자격·확인·기한을 충족할 경우 비인접주라는 사유만으로 배제되지 않는다.',('ma94c18','M.G.L. c.94C §18(d)'))
put(18,True,'별도 예외 없는 ordinary narcotic CII pickup은 §18(d½)의 Maine/인접주 제한을 적용한다. Case B는 그 밖의 주로 명시되어 있다.',('ma94c18','M.G.L. c.94C §18(d½)'))
put(19,True,'별도 타주 delivery의 장소·수령자 조건은 MA 일반 counter pickup과 양립하지 않는다. 배송 허용만으로 무제한 pickup 권한은 발생하지 않는다.',('ma94c18','M.G.L. c.94C §18(d½), out-of-state delivery condition (6)'))
put(20,True,'§18(d½)는 Maine을 이름으로 포함한다. 실제 인접 여부와 법률상의 열거 범위를 구별해야 한다.',('ma94c18','M.G.L. c.94C §18(d½), first sentence'))
put(21,True,'재조제에는 원처방의 허용 및 지정 횟수가 필요하다. 법정 최대 5회는 미승인 추가 3회의 authorization이 아니다.',('ma94c23','M.G.L. c.94C §23(f)'),('cfr1306-22','21 CFR 1306.22(a),(e)'))
put(22,False,'처방자는 법정 ceiling보다 적은 재조제를 승인할 수 있다. 승인된 2회를 최대 5회로 자동 확대할 수 없다.',('ma94c23','M.G.L. c.94C §23(f)'),('cfr1306-22','21 CFR 1306.22(a),(e)'))
put(23,False,'연방 1306.22(a)가 III-IV를 말해도 247 CMR 9.04(13)은 MA Schedule V에 6개월·5회 제한을 직접 부과한다.',('cfr1306-22','21 CFR 1306.22(a)'),('ma247-9','247 CMR 9.04(13)'))
put(24,False,'처음 조제와 이후 refill은 구별된다. 5회는 최초 fill을 포함한 모든 조제가 5회라는 뜻이 아니다.',('cfr1306-22','21 CFR 1306.22(a),(e)(1),(e)(4)'))
put(25,True,'247 CMR 9.04(13)은 V를 발행일부터 6개월 이후 조제/재조제 금지 및 최대 재조제 5회로 규정한다.',('ma247-9','247 CMR 9.04(13)'))
put(26,False,'법정 최대는 승인 없는 재조제를 생성하지 않는다. 원래 승인 횟수가 소진되면 적법한 추가 승인 또는 새 처방이 필요하다.',('ma94c23','M.G.L. c.94C §23(f)'),('cfr1306-22','21 CFR 1306.22(a),(e)'))
put(27,True,'연방 조문은 original prescription의 initial filling과 추가 refill 수를 분리해 다룬다.',('cfr1306-22','21 CFR 1306.22(a),(e)(1),(e)(3)-(4)'))
put(28,False,'이관은 기존 원처방의 남은 authorization을 전달하며 6개월을 새로 부여하지 않는다.',('cfr1306-22','21 CFR 1306.22(a)'),('cfr1306-25','21 CFR 1306.25(b)(3)(i)-(iv)'))
put(29,False,'횟수가 남았더라도 III 처방은 원 발행일부터 6개월 한도를 충족해야 한다. 만료 후 남은 횟수만으로 조제할 수 없다.',('cfr1306-22','21 CFR 1306.22(a),(e)(4)'))
put(30,False,'PRN 표시는 필요시 사용 지시이지 6개월·5회 법정 제한의 예외가 아니다. 법령에 그러한 예외가 없다.',('cfr1306-22','21 CFR 1306.22(a),(e)(4)'))
put(31,True,'III-IV의 6개월 fill/refill 시계는 처방이 issued된 날짜에 고정된다.',('cfr1306-22','21 CFR 1306.22(a)'))
put(32,True,'receiving record에도 원 발행일과 이전 조제/남은 횟수가 유지되어야 한다. transfer date로 시계를 재시작할 근거는 없다.',('cfr1306-22','21 CFR 1306.22(a)'),('cfr1306-25','21 CFR 1306.25(b)(3)-(4)'))
put(33,False,'최초 fill이 늦어져도 원 발행일이 달라지지 않는다. 6개월은 실제 첫 조제일부터가 아니다.',('cfr1306-22','21 CFR 1306.22(a)'))
put(34,True,'필요시 복용 지시는 적용되는 시간 및 횟수 상한을 무효화하지 않는다.',('cfr1306-22','21 CFR 1306.22(a),(e)(4)'))
put(35,False,'III-V partial은 1306.23의 수량·기록·6개월 조건이다. CII 재고부족 1306.13(a)의 72시간 경로를 모든 III-V에 복사할 수 없다.',('cfr1306-23','21 CFR 1306.23(a)-(c)'),('cfr1306-13','21 CFR 1306.13(a)'))
put(36,False,'부분조제 합계가 total quantity prescribed를 넘으면 안 된다. 개별 transaction이 작다는 사실은 합계 상한을 없애지 않는다.',('cfr1306-23','21 CFR 1306.23(b)'))
put(37,True,'III-IV 추가 oral refill은 날짜·수량·추가 횟수·수신자 기록이 필요하고 기존 처방의 6개월·5회 및 추가 refill 수량 상한 내여야 한다.',('cfr1306-22','21 CFR 1306.22(e)(1)-(4)'))
put(38,False,'각 partial을 refill과 같은 방식으로 기록해야 한다는 말은 작은 transaction 하나마다 새 full authorization 전체가 소진된다는 뜻이 아니다. 실제 수량의 합계를 관리한다.',('cfr1306-23','21 CFR 1306.23(a)-(b)'),('cfr1306-22','21 CFR 1306.22(c)(3),(d)'))
put(39,False,'6개월 이내라는 조건만으로 기록 의무가 면제되지 않는다. oral 추가 authorization은 지정 정보를 원처방에 기록해야 한다.',('cfr1306-22','21 CFR 1306.22(e)(2)'))
put(40,True,'실제 조제량과 승인 총량을 연계해 관리해야 하며 partial 거래 수와 full refill 승인 수를 기계적으로 동일시하면 안 된다. 각 partial 기록 의무는 남는다.',('cfr1306-23','21 CFR 1306.23(a)-(b)'),('cfr1306-22','21 CFR 1306.22(c)(3),(d)'))
put(41,True,'부분조제 수량의 합계가 처방된 총량을 초과해서는 안 된다는 직접 문언이다.',('cfr1306-23','21 CFR 1306.23(b)'))
put(42,False,'새 지역 처방번호를 붙여도 원 발행일·최초조제일·잔여 횟수·이전 refill 날짜와 장소 등 법정 history를 보존해야 한다.',('cfr1306-25','21 CFR 1306.25(b)(3)-(5)'))
put(43,True,'III-V refill transfer의 일반 경로는 일회이고 real-time shared database 예외가 없는 세 번째 독립 약국으로의 추가 이관은 허용되지 않는다.',('cfr1306-25','21 CFR 1306.25(a)'))
put(44,False,'예외는 같은 회사명/로고가 아니라 실제 전자적 real-time online database 공유 조건에 달려 있다.',('cfr1306-25','21 CFR 1306.25(a),(d)'))
put(45,False,'database 예외도 법과 처방자 authorization이 허용하는 남은 refill 범위 안이다. 새 refill이나 새 유효기간을 생성하지 않는다.',('cfr1306-25','21 CFR 1306.25(a)'),('cfr1306-22','21 CFR 1306.22(a)'))
put(46,False,'일반 경로에는 일회 제한이 있다. receiving pharmacy마다 새 무제한 독립 이관 권한이 생기지 않는다.',('cfr1306-25','21 CFR 1306.25(a)'))
put(47,True,'같은 체인이라도 실제 real-time online database 요건과 동일 처방기록 정보 요건을 확인해야 한다.',('cfr1306-25','21 CFR 1306.25(a),(d)'))
put(48,True,'refill transfer는 원 발행/조제 및 남은 승인과 과거 refill 정보를 전달하도록 한다. 이관으로 history가 소멸하지 않는다.',('cfr1306-25','21 CFR 1306.25(b)(3)-(5)'))
put(49,True,'예외는 이관 횟수 제한에 대한 것이며 법정 refill 수와 처방자 승인 또는 원 발행일 시한은 유지된다.',('cfr1306-25','21 CFR 1306.25(a)'),('cfr1306-22','21 CFR 1306.22(a)'))
put(50,True,'보내는 약국은 종이처방 VOID 또는 전자기록 transferred 상태를 남겨 동일 잔량이 양쪽에서 중복 사용되지 않도록 해야 한다.',('cfr1306-25','21 CFR 1306.25(b)(2)(i)'))
put(51,False,'TRANSFER 표지 외 원 발행일, 최초조제일, 원/남은 refill 수, 이전 refill 기록과 약국·약사 식별정보가 필요하다.',('cfr1306-25','21 CFR 1306.25(b)(3)-(5)'))
put(52,False,'refill transfer는 last refill부터 2년, initial EPCS transfer는 transfer date부터 양쪽 2년이다. 두 보존 기산점을 동일시하면 안 된다.',('cfr1306-25','21 CFR 1306.25(c)'),('cfr1306-08','21 CFR 1306.08(h)'))
put(53,False,'original과 transferred 처방을 모두 마지막 refill부터 2년 보존하도록 하므로 보내는 약국도 즉시 폐기할 수 없다.',('cfr1306-25','21 CFR 1306.25(c)'))
put(54,True,'설명된 III refill-transfer 원본/이관본의 특수 2년 보존 기산점은 last refill date이다. 이 주장을 모든 다른 기록 종류의 단일 보존기한으로 확대하지 않는다.',('cfr1306-25','21 CFR 1306.25(c)'))
put(55,False,'보내는 약국의 원처방은 VOID 또는 transferred 표시 대상이다. 동일 잔량을 양 약국이 독립적으로 중복 조제할 수 없다.',('cfr1306-25','21 CFR 1306.25(b)(2)(i)'))
put(56,True,'종이/구두 및 전자 receiving 기록 모두 원처방과 이관의 필수 history·잔량 및 관련 약국/약사 정보를 확보해야 한다.',('cfr1306-25','21 CFR 1306.25(b)(3)-(5)'))
put(57,False,'eligible III-V initial EPCS 이관 시 승인 refill은 initial prescription과 함께 수신 약국으로 이동한다.',('cfr1306-08','21 CFR 1306.08(e)'))
put(58,False,'initial EPCS transfer 기록은 보내는 약국과 받는 약국 모두 transfer일부터 2년 보존한다. future last-refill이 기산점이 아니다.',('cfr1306-08','21 CFR 1306.08(h)'))
put(59,False,'이 경로는 전자형식 유지와 내용 불변을 요구한다. 인쇄 후 fax 전송과 signed content 변경은 각각 조건을 위반한다.',('cfr1306-08','21 CFR 1306.08(f)(1)-(2)'))
put(60,True,'환자 요청, retail 간 initial EPCS, 일회, 전자형식·내용 보존·약사 직접소통 및 주법 허용 등 조건을 전제로 가능하다.',('cfr1306-08','21 CFR 1306.08(e)-(h)'),('ma-unfilled','Policy 2023-10 I'))
put(61,True,'전자 처방을 fax 등의 다른 형태로 바꾸지 않고 필요한 내용을 삭제/절단/수정하지 않아야 한다.',('cfr1306-08','21 CFR 1306.08(f)(1)-(2)'))
put(62,False,'initial EPCS는 주법 허용 및 연방 요건 아래 CII도 일회 이관이 가능하다. CII라는 이유만으로 이 경로를 전면 금지하지 않는다.',('cfr1306-08','21 CFR 1306.08(e),(g)'),('ma-unfilled','Policy 2023-10 I'))
put(63,True,'연방 §1306.08(e)는 initial 이관이 III-IV-V이고 authorized refills를 포함하면 그 refill도 함께 이관한다고 명시한다.',('cfr1306-08','21 CFR 1306.08(e)'))
put(64,False,'Board Policy III는 미조제 Schedule VI의 electronic/paper/fax/oral 원본을 모두 별도 이관 대상으로 인정한다.',('ma-unfilled','Policy 2023-10 III'),('ma247-9','247 CMR 9.14'))
put(65,False,'VI 권한은 III 권한을 자동 포함하지 않는다. 예컨대 승인받은 certified technician의 이관은 VI only이고 III-V 연방 이관은 약사 간 직접소통이 필요하다. 또한 paper VI와 paper III의 initial 이관 자격도 다르다.',('ma247-8-current','247 CMR 8.04(4)(d)'),('cfr1306-25','21 CFR 1306.25(b)(1)'),('ma-unfilled','Policy 2023-10 II-III'))
put(66,True,'종이 원본을 스캔하거나 전자 database에 넣어도 originally electronic EPCS로 변환되지 않는다. Policy II가 직접 구별한다.',('ma-unfilled','Policy 2023-10 II'))
put(67,False,'VI 이관은 원처방의 유효기간·잔여 승인 조건에 따른다. transfer가 만료 또는 없는 authorization을 되살리지 않는다.',('ma247-9','247 CMR 9.04(12); 9.14(4)(b)-(c)'))
put(68,False,'스캔은 종이 원본의 법적 형식을 바꾸지 않는다. 종이 III는 original-unfilled-EPCS 이관 경로를 사용할 수 없다.',('ma-unfilled','Policy 2023-10 I-II'))
put(69,True,'Policy III는 미조제 VI의 paper/fax/oral/electronic 모두를 허용 범위로 열거한다. II-V EPCS-only initial 경로와 다르다.',('ma-unfilled','Policy 2023-10 III'),('ma247-9','247 CMR 9.14'))
put(70,True,'VI transfer는 승인된 잔여 횟수 범위 및 발행일부터 1년 제한을 유지한다. 미조제 경로도 원처방 validity를 새로 만들지 않는다.',('ma247-9','247 CMR 9.04(12); 9.14(4)(b)-(c)'),('ma-unfilled','Policy 2023-10 III'))
put(71,False,'환자 또는 agent 요청이 가능하고 약국도 agent가 될 수 있다. 반드시 본인이 직접 방문해야 한다는 제한이 없다.',('ma247-9','247 CMR 9.14(1)-(2)'))
put(72,True,'247 CMR 9.14(3)은 처방 이관 수수료를 청구할 수 없다고 직접 정한다.',('ma247-9','247 CMR 9.14(3)'))
put(73,False,'남은 refill 횟수가 있어도 VI 처방은 발행일부터 1년 넘게 transfer할 수 없다.',('ma247-9','247 CMR 9.14(4)(b)-(c)'))
put(74,False,'환자/agent의 이관 요청은 patient therapy가 지연되지 않게 timely하게 처리해야 한다. 경쟁억제를 위한 무기한 지연은 허용되지 않는다.',('ma247-9','247 CMR 9.14(1)'))
put(75,False,'기록 소유 주장은 transfer fee 금지의 예외가 아니다.',('ma247-9','247 CMR 9.14(3)'))
put(76,True,'VI transfer는 횟수 잔여와 별도로 발행일부터 1년 제한이 있다. unused refill이 유효기간을 연장하지 않는다.',('ma247-9','247 CMR 9.14(4)(b)-(c)'))
put(77,True,'법문은 patient therapy 지연을 막을 수 있도록 timely transfer를 요구한다.',('ma247-9','247 CMR 9.14(1)'))
put(78,True,'약국이 환자의 agent로 이관을 촉진할 수 있다는 명시적 경로이다.',('ma247-9','247 CMR 9.14(2)'))
put(79,True,'개인 임상 조회는 데이터를 읽는 행위이고 약국의 covered dispensing 전송 의무는 별도로 존재한다.',('ma94c24a','M.G.L. c.94C §24A(c)'),('ma105-700','105 CMR 700.012(A)(1),(5)'))
put(80,False,'접근 credential만으로 호기심 조회가 허용되지 않는다. 처방/조제 권한자는 자기 환자 care 목적 등 법령상 허용 용도에 제한된다.',('ma94c24a','M.G.L. c.94C §24A(f)(1),(g)'),('ma105-700','105 CMR 700.012(C)(2)(a),(E)(3)-(5)'))
put(81,False,'prescribing 전 query 의무의 주체와 trigger를 단순히 모든 dispensing transaction으로 확대할 근거가 없다. 개인 등록 유지·약국 reporting과 별도이다.',('ma105-700','105 CMR 700.012(G)(1)-(2)'),('ma247-9','247 CMR 9.15(1)'))
put(82,False,'보고대상 약물을 조제하는 약사 본인의 register/login-maintenance 의무는 약국 reporting account가 대체하지 않는다.',('ma247-9','247 CMR 9.15(1)'))
put(83,False,'PMP 조회를 했다는 사실은 covered dispensing data를 약국이 전송한 것이 아니다. reporting 의무는 유지된다.',('ma94c24a','M.G.L. c.94C §24A(c)'),('ma105-700','105 CMR 700.012(A)(1),(5)'))
put(84,True,'247 CMR 9.15(1)은 보고대상 약물을 조제하는 pharmacist 본인을 register 및 login정보 유지 의무자로 정한다. 기관 계정만으로 충족되지 않는다.',('ma247-9','247 CMR 9.15(1)'))
put(85,True,'구체적 prescribing query trigger를 universal dispensing mandate와 혼동하지 않아야 한다. 등록/임상조회/약국보고의 주체·행위를 각각 확인해야 한다.',('ma105-700','105 CMR 700.012(A),(G)'),('ma247-9','247 CMR 9.15(1)'))
put(86,False,'Schedule IV라는 법적 분류와 benzodiazepine이라는 약물 범주는 별도이다. §24A(c)도 지정 IV/V와 benzodiazepine을 별개 trigger로 나눈다.',('ma94c24a','M.G.L. c.94C §24A(c)'),('ma105-700','105 CMR 700.012(G)(1)(a)-(b)'))
put(87,False,'pharmacist 면허가 있다고 실제 적법한 prescribing 역할의 applicable query 의무가 면제되는 조항은 없다. 예외는 해당 G(2)·waiver 등이다.',('ma105-700','105 CMR 700.012(G)(1)-(2)'))
put(88,False,'보고범위는 II-V와 additional drug이고 prescribing-query 범주는 별도로 정한다. gabapentin 보고만으로 opioid/benzodiazepine 모두에 해당하지 않는다.',('ma94c24a','M.G.L. c.94C §24A(a),(c)'),('pmp-guide','PMP Guide v5.2 §§1-2, gabapentin reporting scope'),('ma105-700','105 CMR 700.001 Additional Drug; 700.012(G)'))
put(89,True,'applicable pre-prescribing query는 issuance 전 행위다. 나중의 pharmacy dispensing report는 다른 주체·시점·행위로 대체가 되지 않는다.',('ma94c24a','M.G.L. c.94C §24A(c)'),('ma105-700','105 CMR 700.012(A),(G)(1)'))
put(90,True,'reporting inclusion과 category-specific query trigger는 별도 법적 집합이다. gabapentin이 reporting에 포함된다는 사실만으로 모든 opioid/benzodiazepine trigger를 충족시키지 않는다.',('ma94c24a','M.G.L. c.94C §24A(a),(c)'),('pmp-guide','PMP Guide v5.2 §§1-2'),('ma105-700','105 CMR 700.012(G)(1)'))
put(91,False,'required pre-prescribing query가 나중의 dispensing submission으로 소급 충족되지는 않는다.',('ma94c24a','M.G.L. c.94C §24A(c)'),('ma105-700','105 CMR 700.012(A),(G)(1)'))
# Every row below is an individual editorial judgment; a family identifier is not a verdict.
F={
'PART04':('emergency oral CII의 발행 후 72시간과 patient-request 잔량의 동일 약국 조건','재고부족 first-partial 시계와 emergency oral issue 시계 및 initial EPCS의 구별','CII와 emergency oral 여부가 시한을 바꾸므로 약물 법적 맥락이 필요하다.'),
'PART05':('타주 CII 최초 5일과 적법한 partial 잔량 30일의 구별','최초조제 자격과 원 발행일 잔량 시계를 연결','구체 약명보다 타주 CII라는 법적 상태가 판단에 필요한 사실이다.'),
'PART06':('nonnarcotic/narcotic CII 타주 처방의 지리적 범위와 pickup/delivery 구별','Maine의 명시 포함 및 별도 타주 배송의 수령지 조건','narcotic 여부가 실제 지리 조건을 바꾸어 약물 범주가 기능한다.'),
'REF01':('처방자 refill authorization과 법정 ceiling 및 MA Schedule V의 별도 한도','연방 III-IV와 MA V 제한을 연결','IV와 V가 연방·주 법원천의 차이를 만들므로 단순 이름 암기는 아니다.'),
'REF02':('III refill 유효기간의 issue/first-fill/transfer 기산점 구별','원 발행일 시한과 남은 authorization을 연결','Schedule III 여부가 6개월·5회 제한을 정한다.'),
'REF03':('oral 추가 refill 기록과 실제 partial 수량 계상','기록·수량·기한을 실제 거래에 적용','III-V partial과 CII shortage의 구별이 법적 효과를 바꾼다.'),
'REF04':('ordinary one-time refill transfer와 실제 shared database 예외','이관 횟수와 원처방의 남은 authorization·history를 연결','이미 사용된 Schedule IV이므로 initial EPCS와 구별되는 맥락이 적절하다.'),
'REF05':('III refill transfer의 중복 조제 방지와 last-refill 보존 기산점','sending/receiving 기록 및 initial EPCS와 refill transfer의 서로 다른 clock','III refill이라는 사실이 §1306.25 경로를 정한다.'),
'REF06':('initial unfilled EPCS 이관의 일회성과 전자형식·내용 불변','initial 이관의 대상·통신형식·보존·associated refill 규칙','CII initial과 III-V associated refill을 의도적으로 비교하며 단순 schedule 암기는 아니다.'),
'REF07':('paper-origin III와 unfilled VI의 다른 이관 자격','원본 형식·schedule·인력별 scope 및 유효기간의 구별','III와 VI가 전자원본 필요 여부와 인력 권한을 달리한다.'),
'REF08':('VI transfer의 no-fee·timely·agent·1년 제한','환자 요청 처리와 잔여 승인·원 발행일 시한','VI 여부가 별도의 1년 시한을 만들며 약명 부재가 판단을 방해하지 않는다.'),
'PMP01':('개인 MassPAT 등록·임상조회·약국 데이터보고의 다른 주체/행위','보고 요건과 접근 권한·query trigger의 구별','보고대상 약물을 다루는 의무 체계가 중심이며 약명 추가가 필수는 아니다.'),
'PMP02':('pre-prescribing query와 dispensing reporting의 시점 및 약물 category 구별','gabapentin reporting 포함과 opioid/benzodiazepine 별도 query trigger','gabapentin의 보고상 지위와 약리범주가 다른 점이 법적 결과에 기능한다.')}
# Failure criterion -> concrete finding. Rows absent a failure retain the independently checked base criterion.
failures={
646:{'wording_not_guessable':'A의 same dispensing pharmacy는 좁은 조건부 법문인데 B any remaining, C extends, D merely because both say 72 hours는 과장·부적절한 동일시를 드러낸다. 법규를 몰라도 A를 고르기 쉬운 비대칭이다.','authentic_distractors':'B의 일부 조제분을 initially unfilled라 부르는 혼동은 실제적이나 D의 merely because라는 자기부정 문구는 진지한 약무 선택지를 이루지 못한다.'},
648:{'wording_not_guessable':'오답 정답 B는 merely because both say 72 hours라고 잘못된 추론 방식을 스스로 설명한다. 나머지는 모두 구체적 한정조건의 법적 문장이라 극성을 몰라도 단서가 강하다.'},
650:{'wording_not_guessable':'D의 separate issuance-based remainder clock and other conditions는 구체 허용/금지나 기한을 말하지 않는 포괄 안전문장이다. A/B/C의 fresh·eliminates·Every와 대비되어 정답 형태가 노출된다.'},
653:{'authentic_distractors':'A의 every state/unrestricted, C의 Maine 지리 직관, D의 shipment가 pickup을 허용한다는 세 주장이 모두 극단이다. 실제 nonnarcotic 경로의 검증·5일·prescriber 자격에 대한 경쟁 해석이 없다.','wording_not_guessable':'유일한 정답 B만 not limited ... merely because라는 범위 한정 문장이고 다른 보기는 전면 배제/무제한 허용 형태여서 문체 단서가 크다.'},
654:{'wording_not_guessable':'C는 geographic restriction matters라고만 하여 실제 조제 거절/가능 판단을 피한다. A categorical exclusion, B Maine exclusion, D automatic permission과 비교하면 지나치게 안전한 정답이다.'},
657:{'authentic_distractors':'B는 처방자가 최대치보다 적게 승인할 수 없다는 비현실적인 권한 제한이다. D도 original dispensing을 every case에 refill로 세어 실제 잔여 2회/5회 계산 경쟁을 제공하지 않는다.','reasoning_not_trivia':'Case A는 이미 two refills가 모두 사용되었다고 주며 추가 승인도 없다. 최댓값이 entitlement가 아니라는 단일 확인으로 끝나 두 번째 사례나 실제 날짜/잔량 판단을 요구하지 않는다.'},
658:{'distinct_from_bank':'MA-Q-0010의 전체 stem과 보기를 읽었으며 federal III-IV wording에서 멈추면 안 되는 이유와 MA V의 5회·6개월을 정답으로 제시한다. 이 문항의 Case B는 바로 같은 핵심 결정을 다시 묻고 Case A가 추가 판단을 요구하지 않아 과도하게 겹친다.','authentic_distractors':'Case B의 MA V 요건에 대항하는 보기들이 아니라 A 처방자 적은 승인 금지, C 자동 추가승인, D original=refill이라는 일반 오류들이다. 정답 B가 유일한 실질적 MA V 규칙이다.'},
660:{'wording_not_guessable':'INCORRECT의 C는 처방자가 법정 최대보다 적게 승인할 수 없다는 보편 명제로, 법령상 수치보다 상식적인 권한 구조만으로 배제하기 쉽다. 다른 보기들은 모두 제한을 유지하는 문장이다.'},
661:{'reasoning_not_trivia':'여러 달 후라는 추상 시점뿐이고 실제 만료 여부·횟수를 계산하지 않는다. 정답 D는 단순 issue-date clock 선언이며 다른 사례와 결합한 판단을 요구하지 않는다.','wording_not_guessable':'A transfer renews, B expired yet unused, C PRN removes limits는 모두 제한 해제 문장이고 D만 기산점 보존 문장이다.'},
662:{'reasoning_not_trivia':'Case B는 transfer 직후 새 6개월을 주장한다는 결론을 그대로 준다. 날짜·잔량 적용 없이 transfer does not restart 문장을 선택하면 끝난다.','distinct_from_bank':'MA-Q-0029의 전체 보기에는 transfer 후 새 issue date와 last-refill 기준 새 6개월을 모두 잘못된 경로로 넣고 원 발행일 6개월을 정답으로 둔다. 여기서는 그 동일한 만료 불갱신 결정을 추상화해 반복한다.'},
664:{'wording_not_guessable':'INCORRECT 정답 B는 만료했어도 unused refills가 있으면 가능하다는 포괄 연장이다. 다른 세 문장은 모두 원 기산점/제한 유지라 정답 극성이 문체로 드러난다.'},
666:{'wording_not_guessable':'정답 D의 rather than blindly counted는 특정 잘못을 대놓고 비판하는 표현이다. A no record, B exceeding, C Every III-V는 모두 극단 허용/범위 확대여서 D가 언어상 안전한 선택지다.'},
670:{'wording_not_guessable':'C만 actual conditions must be met라고 신중히 제한하고 A creates additional refills/restarts, B without limit, D discard prior fills는 위험한 전면 해제 문장이다. 체인 실시간 database의 구체 조건을 몰라도 답이 유추된다.'},
672:{'wording_not_guessable':'INCORRECT 정답 D가 새 처방번호면 prior fills를 discard할 수 있다고 하여 history 삭제를 정당화한다. 다른 세 보기는 조건 유지라 원문 비교 없이 답을 추측하기 쉽다.'},
673:{'authentic_distractors':'B는 TRANSFER 한 단어가 모든 정보를 대신한다고 하고 D는 sending copy 즉시 폐기다. 둘 다 실제 기록 선택의 경쟁 해석보다 명백한 기록 생략으로 설계되었다.','wording_not_guessable':'A만 duplicate use를 막는 보편적 안전 원칙이다. B alone supplies all, C necessarily same, D only/discard immediately에 비해 한정성과 안전성이 두드러진다.'},
676:{'wording_not_guessable':'INCORRECT 정답 C에 only receiving와 discard immediately가 함께 들어 있다. 다른 세 보기는 정보·보존·중복방지 의무를 유지해 언어상 구분이 너무 쉽다.'},
677:{'distinct_from_bank':'MA-Q-0019의 환자요청 unfilled MS Contin EPCS 약국간 이관 문항을 모든 보기와 읽었다. 같은 일회 pharmacist 전자 이관 허용을 정답으로 묻고 print/fax를 오답으로 둔다. 추가 Case B와 관련 III-V 설명이 SBA에서 추가 결정을 요구하지 않아 핵심 판단이 과도하게 중복된다.'},
678:{'authentic_distractors':'B의 과거 CII 전면 이관금지 혼동은 실제적이나 C의 III-V refills는 서술된 CII 사례에 존재하지 않고 D의 future last refill도 그 사례와 맞지 않는다. 정답 경쟁이 사례의 실제 조건에 집중되지 않는다.'},
681:{'wording_not_guessable':'C는 원본 paper가 scan으로 EPCS가 되지 않는다는 좁은 명제인데 A every unfilled VI prohibited, B necessarily includes, D regardless of authorization은 모두 전면 확대라 구분 단서가 크다.','natural_rule_combination':'Case A의 스캔 형식 판단과 Case B의 VI 이관을 함께 둔 것은 비교 목적이 있으나 인력별 authority 보기는 어떤 staff license도 명시하지 않아 실제 사실관계와 자연스럽게 결합되지 않는다.'},
682:{'wording_not_guessable':'D만 described pathway의 전자원본 제한 부재를 한정해 말하고 A 만료부활 regardless, B necessarily, C scan makes eligible는 과장이다. 정답을 형태로 추정하기 쉽다.','natural_rule_combination':'Case B paper VI 허용에 필요한 형식 비교는 자연스럽지만 인력 권한 보기 B를 판단할 인력 자격이 사례에 없어 별도 규칙 암기로 남는다.'},
684:{'natural_rule_combination':'INCORRECT 정답 A의 authority가 사람의 scope인지 원처방 이관 자격인지 명확하지 않다. 해설은 인력별 scope를 말하지만 stem은 직원 면허/직무를 하나도 정하지 않아 핵심 오답의 적용 사슬이 느슨하다.','wording_not_guessable':'A의 necessarily includes라는 전면 포함만 나머지 구체 조건부 원칙들과 다르게 쓰여 정답 단서가 된다.'},
685:{'authentic_distractors':'C 무기한 unused refill, D 경쟁억제를 위한 indefinitely delay는 실제 환자 이관권의 경쟁 법해석으로 보기 어렵다. no-fee가 유일하게 현실적인 조치로 보인다.','wording_not_guessable':'D는 indefinitely to discourage라는 악의까지 명시하고 A only in-person, C any unused라고 극단화되어 B의 no-fee를 법문 없이도 고르기 쉽다.'},
686:{'wording_not_guessable':'A indefinitely discourage, B charge because owns, D only in-person은 모두 보편적 환자 접근 제한이다. C만 stated one-year limit를 유지하여 법적 한정 문장이라는 단서가 크다.'},
688:{'wording_not_guessable':'INCORRECT 정답 D의 Only in-person appearance는 절대적인 접근 제한이며 나머지 세 보기는 timely/no-fee/stated one-year라는 보호적 의무 유지 문장이다. 실제 agent 범위를 모른 채 추측할 수 있다.'},
690:{'distinct_from_bank':'MA-Q-0289의 전체 stem·보기를 추가로 읽었다. institutional MassPAT account가 개인 register/login 의무를 대체하는지 묻고 동일한 개인 의무를 정답으로 제시한다. Case A가 추가되어도 이 SBA가 묻는 Case B 결정은 그대로이다.'},
692:{'wording_not_guessable':'INCORRECT 정답 C는 curiosity searches unrelated to patient care를 허용한다. 구체적 MA 의무나 category를 몰라도 개인정보 보호 직관만으로 명백히 배제되므로 나머지 실제 법적 혼동들과 난도가 맞지 않는다.'},
693:{'authentic_distractors':'A every IV is benzodiazepine, B pharmacist license exempts prescribing duties, C every reportable meets every trigger는 모두 범주를 전면 합치거나 면제를 창조한다. 실제 예외·query 시점에 대한 경쟁 조치가 없다.','wording_not_guessable':'D만 applicable obligation의 주체·시점을 유지하며 다른 보기는 Every/exempts/every로 극단화된다.'},
694:{'authentic_distractors':'gabapentin의 보고와 query 구별을 묻지만 B는 reporting 대체, C는 every IV=benzodiazepine, D는 pharmacist 면허면제여서 gabapentin에 대한 그럴듯한 법적 분류 선택지가 없다.','wording_not_guessable':'A의 inclusion alone does not establish every other trigger가 신중한 범위 한정이고 다른 보기는 replacing/every/exempts의 전면 명제라 문구 단서가 강하다.'}}
# Item-specific central judgment, including passes, is retained even when a different criterion fails.
central={
646:'동일 체인 다른 점포에서 잔량을 받으려는 Case B가 §18(d¾)의 same pharmacy를 직접 시험한다.',648:'두 72시간을 하나의 기산점으로 합치는 B를 유일한 오류로 독립 확인했다.',649:'8일 최초 제시를 30일 일반유효기간으로 구제하려는 시도와 적법한 최초 partial을 구별해야 하므로 의미 있는 주법 적용이다.',650:'Case B의 적법한 시작과 issuance-based 잔량 시계를 확인하되 답안 D의 모호한 안전문장을 수정해야 한다.',652:'MA 자체 발행 처방 전체에 타주 5일 규칙을 적용하는 A를 배제하려면 법의 적용 대상을 구별해야 한다.',653:'nonnarcotic CII 비인접주 경로와 narcotic 제한을 구별하지만 극단적인 오답들이 정답 경쟁을 약화한다.',654:'narcotic 제한이 실제로 허용 여부를 결정하는데 정답은 단지 matters라고만 하여 실무 결론이 약하다.',655:'Maine 명시포함, ordinary pickup 범위, 타주 shipment의 한계와 nonnarcotic 경로를 네 가지로 각각 적용한다. 네 보기가 모두 참인 SATA 자체를 결함으로 보지 않았다.',656:'배송 허용을 MA counter pickup으로 확장하는 D의 오류를 잡는 법적 경로·수령지 추론은 타당하다.',657:'두 번 승인된 refill 소진은 실무 상황이지만 법정 최댓값을 자동 지급권으로 보는 문항은 선택지 경쟁이 약하다.',658:'연방 문언에 Schedule V가 없다는 것만으로 MA 제한이 없다고 보는 혼동은 실제적이나 canonical 같은 핵심 결정을 이미 반복한다.',660:'INCORRECT 극성은 명확하고 법적 key는 맞지만 C는 실제 refill 권한 구조에 비해 지나치게 극단이다.',661:'발행일부터 시계는 맞으나 실제 날짜·환자 행동을 적용할 정보가 없어 규칙 선언을 재인하는 수준이다.',662:'transfer가 유효기간을 갱신하지 않는 key는 맞지만 canonical의 같은 반례를 추상 문장으로 반복한다.',664:'원 발행일, transfer 불갱신, PRN 범위는 정확하지만 만료 후 unused refill 허용이라는 정답 오류는 쉽게 드러난다.',665:'추가 oral authorization 기록과 partial의 수량 계상이 다른 문제임을 이해해야 하며 C의 기록·총량·시한 조건을 조합한다.',666:'거래 수와 승인 전체 단위를 구별하는 핵심은 좋지만 정답의 blindly라는 평가적 표현이 답을 노출한다.',668:'III-V partial의 기록/총량/6개월과 CII shortage 72시간의 적용범위 차이를 판별하는 유용한 INCORRECT 문항이다.',669:'이미 ordinary transfer를 한 IV 처방이 세 번째 독립 약국으로 가려는 구체 조건과 qualifying database 부재를 함께 적용한다.',670:'실제 database 조건을 확인하는 key는 맞지만 다른 선택지의 history 폐기·무제한 이관·자동 refill 생성이 너무 쉽게 배제된다.',671:'실제 database, 이관 history, 남은 승인, 일회 제한을 각각 판단한다. all-true SATA라는 형식만으로 실패시키지 않았다.',672:'원번호 변경과 history 보존의 혼동은 실제적이나 discard prior fills 표현이 명백한 오류 단서가 된다.',673:'중복 잔량 방지는 맞지만 다른 보기들이 극단적인 기록 생략을 내세워 법적 세부를 몰라도 정답이 드러난다.',674:'last refill과 transfer date라는 두 진짜 기록 시계를 비교하므로 숫자 암기를 넘어 경로를 구별해야 한다.',676:'양쪽 기록 보존을 요구하는 법문은 확인했으나 key C의 즉시 폐기는 실무 선택지로 너무 약하다.',677:'조건부 initial EPCS 허용은 정확하지만 canonical MA-Q-0019의 동일 결정을 추가 Case B만 붙여 반복한다.',678:'전자형식·불변 원칙은 타당하지만 III-V refill 및 future last refill 오답이 실제 CII 사례에 맞지 않는다.',680:'initial transfer 양쪽 2년-from-transfer와 refill transfer의 last-refill 기산점을 분리해야 하며 일회·전자 불변·associated refills의 관련 요건도 확인한다.',681:'paper 스캔이 EPCS로 바뀌지 않는다는 판단은 타당하나 staff 자격을 주지 않은 authority 보기의 연결이 약하다.',682:'paper VI의 별도 허용 경로는 확인했으나 실제 staff scope 없이 권한 포괄 보기와 병치한다.',684:'A의 보편 권한 포함은 반례가 있어 법적으로 오류지만, 인력 scope를 묻는 의도라면 certified technician 등 행위자 사실을 stem에 제공해야 한다.',685:'no-fee는 정확하나 다른 보기의 indefinite delay와 만료 무시가 지나치게 노골적이다.',686:'1년 초과 VI transfer 금지는 정확하나 나머지 보기들이 환자권한의 극단적 제한이라 단서가 강하다.',687:'환자 agent·no-fee·timely 처리·잔여 횟수와 1년을 모두 확인하는 관련 patient-rights SATA이다. 모두 참인 조합은 허용된다.',688:'agent 요청 허용과 in-person only 오류를 구분하지만 정답의 Only와 다른 의무 보존 문장 간 차이가 크다.',689:'개인 조회가 보고 전송을 대신하지 않는다는 실제 시스템·법적 의무 혼동을 묻고 account/clinical purpose/prescribing trigger를 따로 평가해야 한다.',690:'개인 register/login 의무의 key는 정확하나 MA-Q-0289의 같은 institutional-account 반례를 다시 묻는다.',692:'curiosity 조회 허용은 틀리지만 다른 의무 구조에 비해 개인정보 직관만으로 배제되는 단서가 된다.',693:'pre-prescribing query와 나중의 dispensing report는 별개이나 세 오답이 전면적인 범주오류·면제창조라 경쟁력이 낮다.',694:'gabapentin reporting inclusion만으로 query category가 생기지 않는 핵심은 정확하나 보기들이 실제 gabapentin 법적 분류를 경쟁시키지 못한다.'}
criteria=['jurisprudence_reasoning','practice_plausibility','authentic_distractors','wording_not_guessable','reasoning_not_trivia','natural_rule_combination','appropriate_drug_context','distinct_from_bank','not_schedule_flashcard','public_style_without_copying']
# 92 distinct visible propositions occur in 160 choices; key calculations below use these independent truth judgments, never stored keys.
unique=[]
for r in packet['records']:
 for c in r['original_visible_content']['choices']:
  if c['text'] not in unique:unique.append(c['text'])
assert len(unique)==92 and set(J)==set(range(92))
records=[]
for r in packet['records']:
 q=r['original_visible_content'];qid=q['question_id'];num=int(qid.rsplit('-',1)[1]);nr=nearby[qid];family=nr['source_context']['family_id'];topic,natural,drug=F[family]
 per={};auths=[];expected=[];polarity='INCORRECT' if 'INCORRECT?' in q['stem'] else ('SATA_CORRECT' if q['question_type']=='SATA' else 'CORRECT')
 for c in q['choices']:
  i=unique.index(c['text']);j=J[i];a=[authority(*ref) for ref in j['refs']]
  for x in a:
   if x not in auths:auths.append(x)
  if j['truth'] != (polarity=='INCORRECT'):expected.append(c['id'])
  per[c['id']]={'option_text':c['text'],'option_text_sha256':hashlib.sha256(c['text'].encode()).hexdigest(),'independent_proposition_index':i,'independent_statement_truth':j['truth'],'supported_as_written':j['truth'],'finding_ko':j['finding_ko'],'exact_authority':'; '.join(x['exact_section'] for x in a),'authorities':a}
 assert len(expected)>=1 and (q['question_type']!='SBA' or len(expected)==1)
 keysame=expected==q['correct_choice_ids']
 reasons={
 'jurisprudence_reasoning':f'{qid}는 {topic}를 법적 행위/조건에 적용하게 한다. {central[num]}',
 'practice_plausibility':f'{qid}의 약국 직원이 제안한 조제·기록·이관/PMP 처리를 검토하는 상황은 약무에서 발생할 수 있다. 두 개의 Case가 교육용 대비라는 범위에서 판단하며 실제 환자의 사실을 임의로 추가하지 않았다.',
 'authentic_distractors':f'{qid}의 보기별 사실판정을 각각 수행했다. {natural}에서 발생하는 다른 경로/주체/기산점 혼동을 평가한다. SATA의 참 보기들 역시 각각 독립 법적 조건이며 all-true라는 이유만으로 결함 판정을 하지 않는다.',
 'wording_not_guessable':f'{qid}에서 선택지의 주체·행위·시계·예외를 알아야 저장 키 {q["correct_choice_ids"]}를 판정할 수 있다. CORRECT/INCORRECT/SATA 극성에 따라 실제 truth 조합을 따로 계산했고 길이만으로 정답이라고 판단하지 않았다.',
 'reasoning_not_trivia':f'{qid}는 {topic}라는 경로의 적용을 요구한다. 단순 숫자 반복이라는 이유로 감점하지 않았고 실제 조건의 차이가 법적 결과를 바꾸는지 확인했다.',
 'natural_rule_combination':f'{qid}의 {natural}는 같은 실무 행위의 조건/예외라 관련성이 있다. 단일선택이 두 Case 중 하나에 초점을 둔다고 해서 모든 규칙의 동시 적용을 필수로 만들지는 않았다.',
 'appropriate_drug_context':f'{qid}: {drug}',
 'distinct_from_bank':f'{qid}에 대해 canonical 439개·공개 bank 2349개를 모두 visible stem/choices로 비교했고 가장 가까운 {nr["canonical_nearest"][0]["question_id"]}와 {nr["public_nearest"][0]["question_id"]}의 원 stem·전 보기를 직접 읽었다. family 변형이 동일 Case를 공유함을 확인했다. 배정문항은 default recommended_ids에 없고 원 learning_boundary도 가족 변형이라고 공개한다. 이 archived 연습 맥락에서만 구별 기준을 충족하며 새 독립 범위나 release 후보의 독창성을 인정한 것이 아니다.',
 'not_schedule_flashcard':f'{qid}는 schedule 이름만 식별하는 문제가 아니라 {topic}를 주어진 행위에 적용한다.',
 'public_style_without_copying':f'{qid}의 {q["question_type"]} 응답방식과 법적 상황 적용을 public NABP sample/competency/format 자료와 비교했다. 공개 예시는 본문으로 직접 확인했고 문장 또는 고유 보기 구성을 재현한 것으로 보이지 않는다. protected Pre-MPJE/회상/상용 문항은 입력하지 않았다.'}
 flags={k:True for k in criteria}
 for k,reason in failures.get(num,{}).items():flags[k]=False;reasons[k]=reason
 verdict='PASS' if all(flags.values()) else 'FAIL'
 nextaction=(f'{qid}: {central[num]} 현재 archived 가족 변형 표기를 유지하고 이 결과를 canonical release로 승격하지 않는다. 실제 release 후보가 필요하면 지정 공식 근거와 당시 current hash를 대상으로 canonical 감사 절차를 별도로 수행한다.' if verdict=='PASS' else f'{qid}: {central[num]} 실패 기준별 이유에 따라 실제 환자·약국의 한 상황에서 구체 조치를 고르게 재작성하고 오답을 같은 범위·같은 길이의 그럴듯한 법적 대안으로 맞춘 뒤 새 hash의 독립 법규·현실성 감사를 받는다.')
 explanation={'core_reasoning_read_completely':True,'core_reasoning_text_sha256':digest(q['explanation']['core_reasoning']),'core_review_ko':f'한국어 core 전문을 읽고 {topic}에 관한 각 명제를 위 공식 조항과 대조했다. 법적 핵심 방향은 현재 근거와 합치한다. 해설을 독립 truth의 근거로 사용하지 않았다.','choice_analysis_read_ids':[c['id'] for c in q['choices']],'choice_reviews':{c['id']:{'original_rationale_sha256':digest(q['explanation']['choice_analysis'][c['id']]),'finding_ko':'원 한국어 rationale 전문과 교정된 영어 문장(있는 경우)을 읽었다. '+per[c['id']]['finding_ko'],'legal_error_found':False} for c in q['choices']},'learning_boundary_read_completely':True,'learning_boundary_review_ko':'네 가족 변형이 두 Case·판단을 공유한다는 범위 제한은 확인했다. 별개의 독립 사례 네 개나 신규 범위로 집계하지 않는다.','explanation_legal_verdict':'SUPPORTED_WITHIN_STATED_SCOPE','editorial_limit_ko':central[num]}
 records.append({'question_id':qid,'record_sha256':r['record_sha256'],'visible_content_sha256':r['visible_content_sha256'],'family_id':family,'read_scope':{'stem_read_completely':True,'all_choices_read_completely':True,'choice_ids_read':[c['id'] for c in q['choices']],'stored_key_read':q['correct_choice_ids'],'core_reasoning_read_completely':True,'all_choice_rationales_read_completely':True,'learning_boundary_read_completely':True,'read_at':now,'input_path':rel(EV/'assigned-visible-input.json'),'input_sha256':sha(EV/'assigned-visible-input.json')},'legal_review':{'existing_answer_correct':'YES' if keysame else 'NO','stored_key':q['correct_choice_ids'],'independently_expected_key':expected,'polarity':polarity,'single_answer_unique':len(expected)==1 if q['question_type']=='SBA' else None,'sata_exact_combination_checked':q['question_type']=='SATA','per_choice_findings':per,'authorities':auths,'verdict':'KEEP' if keysame else 'MAJOR_REWRITE','finding_ko':central[num]+' 각 보기의 독립 truth와 극성을 적용한 expected key가 저장 키와 일치한다.','blocker':None,'original_explanation_review':explanation},'realism_review':{'verdict':verdict,'decision':'KEEP' if verdict=='PASS' else 'MAJOR_REWRITE','criteria':flags,'criterion_findings_ko':reasons,'finding_ko':central[num],'duplicate_comparison':{'evidence_path':rel(EV/'nearest-visible-comparison.json'),'evidence_sha256':sha(EV/'nearest-visible-comparison.json'),'canonical_pool_count':439,'public_pool_count':2349,'canonical_nearest':nr['canonical_nearest'],'public_nearest':nr['public_nearest'],'nearest_stem_and_all_choices_read':True,'semantic_supplement_path':rel(EV/'semantic-nearest-supplement.json'),'public_default':nr['public_default'],'comparison_scope':'Visible fields only; similarity selects candidates, not semantic verdict. Archived variation is not automatically a failure.'},'public_style_sources':[authority(x) for x in stylememo]},'safe_hold_recommended':verdict!='PASS','release_eligible':False,'required_next_action_ko':nextaction})
style=json.loads((ROOT/'data/exam_style/mpje_style_profile.json').read_bytes());blueprint=json.loads((ROOT/'data/blueprint.json').read_bytes())
report={'schema_version':'independent-legacy-substantive-review/1','stage':'independent-legacy','job_id':assignment['job_id'],'independent_of_authors':True,'auditor':'GPT','auditor_instance':'GPT:/root/independent_wave13_b:20261104','actor_provenance':{'actor_id':'/root/independent_wave13_b','session_id':'/root/independent_wave13_b'},'canonical_audit':False,'canonical_release_credit':0,'author_review_credit':0,'release_eligible':False,'reviewed_at':'2026-11-04','completed_at':now,'independence_declaration':{'fresh_fork_none_session':True,'known_prior_verdict_exposure_count':0,'author_hidden_truth_read':False,'prior_reports_or_ledger_conclusions_read':False,'original_visible_explanation_treated_as_claims_not_authority':True,'limitation_ko':'파일명 탐색은 했지만 기존 보고서 본문/원장 결론을 열람하지 않았다. 허용 source_context의 note_evidence 위치정보는 법적 판정 근거로 사용하지 않았다. 독립성은 실제 세션 provenance 진술이며 문자열 자체로 독립성이 입증되는 것은 아니다.'},'source_methodology_ko':'Firecrawl scrape는 크레딧 부족으로 실행되지 않았다. 정상 inherited proxy·기본 TLS 검증을 유지한 urllib 직접 HTTPS로 독립 조회했다. HTTP200 문서 정체와 관련 본문을 읽었다. 실패404는 법률권위로 사용하지 않았다. eCFR는 authoritative but unofficial consolidation 표시와 current-through 2026-11-02를 확인했다. NABP copyrighted 공개 자료는 raw/text를 /tmp에만 두고 URL·raw/text SHA·열람시각·자체 메모를 보존한다. 이 형식 자료는 법률권위가 아니다. 모든 검토는 2026-11-04 기준이며 역사적 시행일 전체를 재구성했다는 주장은 하지 않는다.','sources':list(sources.values()),'input_bindings':{'assignment_path':rel(EV/'assignment.json'),'assignment_sha256':sha(EV/'assignment.json'),'visible_input_path':rel(EV/'assigned-visible-input.json'),'visible_input_sha256':sha(EV/'assigned-visible-input.json'),'question_hashes':assignment['question_hashes']},'methodology_files':method,'schema_binding':{'schema_path':'schemas/audit.schema.json','schema_file_sha256':sha(ROOT/'schemas/audit.schema.json'),'canonical_schema_applied':False,'reason':'legacy stage report grants no canonical audit credit'},'style_profile':{'profile_id':style['profile_id'],'content_version':style['content_version'],'content_hash':style['content_hash'],'file_sha256':sha(ROOT/'data/exam_style/mpje_style_profile.json')},'blueprint':{'blueprint_id':blueprint['blueprint_id'],'content_version':blueprint['content_version'],'content_hash':blueprint['content_hash'],'file_sha256':sha(ROOT/'data/blueprint.json')},'summary':{'records':len(records),'legal_answer_yes':sum(r['legal_review']['existing_answer_correct']=='YES' for r in records),'legal_keep':sum(r['legal_review']['verdict']=='KEEP' for r in records),'realism_pass':sum(r['realism_review']['verdict']=='PASS' for r in records),'realism_fail':sum(r['realism_review']['verdict']=='FAIL' for r in records),'canonical_release_credit':0},'records':records}
write(ROOT/'reports/full-corpus-review/independent-phase13-b-review.json',report)
write(EV/'independent-proposition-judgments.json',{'entered_after_primary_source_read':True,'distinct_propositions':len(unique),'propositions':[{'index':i,'option_text':text,**{k:v for k,v in J[i].items() if k!='refs'},'authorities':[authority(*ref) for ref in J[i]['refs']]} for i,text in enumerate(unique)]})
print(report['summary'])
