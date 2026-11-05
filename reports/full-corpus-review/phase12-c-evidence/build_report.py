"""Reproducible serialization of this actor's independently authored findings.
No hidden truth, previous review, ledger verdict, or author answer is read by this file.
Stored keys are compared only after independently classified option propositions.
"""
from pathlib import Path
import json,hashlib,re,datetime,collections
ROOT=Path(__file__).resolve().parents[3]
BASE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
read=lambda p:json.loads(p.read_text())
packet=read(BASE/'assigned-visible-input.json');assignment=read(BASE/'assignment.json');loc=read(BASE/'locator-metadata.json');nearest=read(BASE/'nearest-visible.json')
ACTOR='/root/independent_wave12_c';INSTANCE='GPT:/root/independent_wave12_c:20261104'
# Manually authored proposition assessments, grouped by the legal decision being reviewed.
# Every pattern is evaluated against the actual English option; no key determines truth.
F={
'PRIV08':dict(topic='NPP 수령 확인과 특정 공개 authorization 및 개인 권리',sources=['ecfr45-164-web'],section='45 CFR 164.520(c)(2)(i)-(ii); 164.508(a)(1), (c); 164.522(b); 164.524(a); 164.526(a); 164.530(h)',core='수령 확인은 고지 제공의 증명이다. 사용·공개의 유효한 authorization과 개인 권리의 포괄적 포기는 별개이므로 기존 핵심 설명은 이 범위에서 맞다. Emergency 예외 및 확인서 취득 실패의 good-faith 문서화 조건은 applicable 절차에 포함된다.',rules=[
('Patient access, amendment, and confidential',True,'개인에게는 접근·수정·합리적인 confidential communication 요청의 별도 권리가 있다. NPP 수령 서명으로 이 권리들이 소멸하지 않는다.','164.522(b), 164.524(a), 164.526(a), 164.530(h)'),
('Separating the acknowledgment',True,'수령 확인과 필요한 개별 authorization을 구별하는 것은 164.520의 고지 절차와 164.508의 유효한 authorization 요건을 혼동하지 않는 처리이다.','164.520(c)(2)(ii), 164.508(a)(1), (c)'),
('Acknowledgment of the notice is not',True,'NPP 서명은 수령 확인이며 모든 후속 공개를 허용하는 무제한 authorization의 요건을 충족하지 않는다.','164.520(c)(2)(ii), 164.508(a)(1), (c)'),
('The direct-treatment provider follows',True,'직접 진료 관계가 있는 covered provider는 최초 제공 및 해당 good-faith acknowledgment 절차를 따른다. 응급 진료 예외가 있으므로 applicable라는 한정을 유지한다.','164.520(c)(2)(i)-(ii)'),
('Signing the notice waives all',False,'수령 서명은 접근·수정·비밀 연락권을 전부 포기하는 동의가 아니다. Covered entity는 치료 등의 조건으로 이 권리의 포기를 요구할 수도 없다.','164.522(b), 164.524(a), 164.526(a), 164.530(h)')]),
'PRIV09':dict(topic='HIPAA 접근 요청의 접수 시계와 연장',sources=['ecfr45-164-web','hipaa-access-original-faq'],section='45 CFR 164.524(b)(2)(i)-(ii); HHS access timeliness FAQ, answer paragraphs 1-2',core='초기 접수일부터 30 calendar days이고, 원래 기한 내 서면 사유·완료 예정일을 알리면 최대 30일을 한 번 연장할 수 있다. 이 Case A는 약국이 먼저 접수했으므로 vendor 인계가 시계를 초기화하지 않는다. HHS가 설명하는 BA 직접 접수 경로와 구분된다.',rules=[
('The vendor handoff does not restart',True,'약국이 이미 접수한 뒤 12일 후 BA에게 넘겨도 약국의 접수일부터 시계가 진행된다. HHS FAQ가 BA 인계 지연은 할당 시간을 소모한다고 직접 명시한다.','164.524(b)(2)(i); HHS FAQ answer paragraphs 1-2'),
('The ordinary HIPAA access period is 30 business',False,'일반 접근 기한은 30 business days가 아니라 30 calendar days이다.','164.524(b)(2)(i); HHS FAQ answer paragraph 1'),
('The ordinary access period is measured in calendar',True,'HHS의 해당 조항 공식 설명은 ordinary access 기간을 calendar days로 명시한다.','164.524(b)(2)(i); HHS FAQ answer paragraph 1'),
('The pharmacy may keep adding',False,'같은 접근 요청에 반복해서 연장하는 경로는 없다. 법문은 최대 추가 30일이며 한 번만 허용한다.','164.524(b)(2)(ii)(B)'),
('The described extension is one additional',True,'허용된 연장은 한 번이며 그 길이는 최대 30일이다.','164.524(b)(2)(ii)'),
('The extension can be established',False,'원래 기한이 지난 뒤 서면 통지를 보내는 것은 원래 기한 내 사유·완료일 통지 조건을 충족하지 않는다.','164.524(b)(2)(ii)(A)'),
('The allowed extension requires',True,'추가 기간을 쓰려면 초기 30일 안에 지연 사유와 완료 예정일을 서면으로 알려야 한다.','164.524(b)(2)(ii)(A)'),
('Forwarding the request to the vendor restarts',False,'Case A의 원 접수는 약국에서 일어났다. 내부·BA 전달은 새 접수가 아니므로 새 30일을 만들지 않는다.','164.524(b)(2)(i); HHS FAQ answer paragraph 2')]),
'PRIV10':dict(topic='HIPAA 문서 보존과 일반 처방 기록·수정 이력',sources=['ecfr45-164-web','ma-94c23'],section='45 CFR 164.530(j)(1)-(2), 164.526(c)(1), (d)(4); M.G.L. c.94C §23(e)',core='HIPAA-required documentation은 creation 또는 last in effect 중 늦은 날부터 6년을 보존한다. 일반 처방 기록의 2년 최소와 전혀 같은 대상·시계가 아니다. 6년은 모든 의료기록의 일괄 파기일도 아니다. 수정은 관련 기록을 식별하고 append/link하므로 원 사실을 감추기 위한 삭제를 허용하지 않는다. 기존 설명의 방향은 맞지만 기산점은 이 검토의 정확한 한정을 함께 읽어야 한다.',rules=[
("HIPAA's documentation rule creates",False,'164.530(j)는 정해진 HIPAA 문서의 최소 보존을 규정한다. 모든 medical record를 정확히 6년째 파기하라는 보편적 명령이 아니다.','164.530(j)(1)-(2)'),
('A pharmacy can choose the shortest',False,'동일 자료에 적용되는 의무를 임의로 가장 짧은 기간 하나로 대체할 수 없다. HIPAA 문서에 대한 6년 의무는 처방 기록 최소가 더 짧다는 이유로 없어지지 않는다.','164.530(j)(1)-(2); M.G.L. c.94C §23(e)'),
('An amendment request authorizes deletion',False,'수정 요청은 은폐 목적의 audit trail 삭제를 허용하지 않는다. 승인 수정은 영향받는 기록을 식별하고 수정 내용을 append 또는 link한다.','164.526(c)(1), (d)(4)'),
('The general prescription-record period does not replace',True,'일반 controlled-prescription 2년 보존과 HIPAA-required documentation의 6년 보존은 각 대상에 별도로 적용된다.','164.530(j)(1)-(2); M.G.L. c.94C §23(e)'),
('A minimum documentation-retention rule is not',True,'최소 문서 보존 기간을 모든 종류의 의료기록에 적용되는 정확한 파기 시점으로 바꿀 수 없다.','164.530(j)(1)-(2)'),
('The general two-year prescription period is sufficient',False,'HIPAA가 요구하는 문서에 일반 처방 기록의 2년만 적용하면 연방 문서 보존 의무를 충족하지 못한다.','164.530(j)(1)-(2); M.G.L. c.94C §23(e)'),
('Overlapping requirements must be met',True,'각 기록이 두 의무 모두의 대상이면 각각을 충족해야 한다. 짧은 일반 최소만 선택하는 예외는 여기에 없다.','164.530(j)(1)-(2); M.G.L. c.94C §23(e)')]),
'PRIV11':dict(topic='오교부에 수반된 PHI 침해 위험 평가',sources=['ecfr45-164-web'],section='45 CFR 164.402 breach definition (1)-(2), 164.414(b)',core='실수라고 해서 breach framework에서 자동 제외되지 않는다. 예외나 low probability of compromise가 입증되는지, 정보의 성질·수령자·실제 취득/열람·mitigation을 따져야 한다. 회수는 mitigation에 해당하지만 모든 요건의 증명은 아니며, CQI 기록은 이 독립된 privacy 분석을 대신하지 않는다.',rules=[
('Recovering the bag conclusively',False,'회수는 완화 조치라는 한 요소다. 수령자가 실제 보았는지·보유할 수 있었는지 등 다른 요소를 단독으로 확정하지 않는다.','164.402(1)(iii), (2)(i)-(iv)'),
('An undocumented assurance',False,'법문은 예외 또는 위험평가에 따른 낮은 정보 침해 확률을 입증하도록 한다. 문서 없는 무해 추측은 compromise 평가와 입증을 대체하지 않는다.','164.402(2), 164.414(b)'),
('An impermissible disclosure is evaluated',True,'허용되지 않는 공개가 실수였어도 정의상 예외와 위험평가를 검토해야 한다. 무조건 reportable이라고 결론내리는 문장도 아니다.','164.402(1)-(2)'),
('Opening a CQI record automatically',False,'164.402의 예외·정보 침해 확률 평가는 별도 요구다. CQI 기록을 열었다는 사실만으로 breach 분석이 완료되지 않는다.','164.402(1)-(2), 164.414(b)'),
('Accidental disclosures are categorically',False,'일부 예외에는 good-faith·scope·추가 공개 금지 등 구체 조건이 있다. accidental이라는 단어 하나는 모든 공개를 일괄 면제하지 않는다.','164.402(1)-(2)'),
('Retrieval is relevant mitigation',True,'회수는 mitigation으로 고려되지만 실제 열람 여부 등 나머지 요소도 평가해야 한다. 예외가 충족된다면 그 경로도 검토한다.','164.402(1)(iii), (2)(i)-(iv)'),
('An applicable exception or documented low probability',True,'notification이 필요 없다고 하려면 적용되는 예외 또는 low probability 결론의 근거를 뒷받침해야 한다.','164.402(1)-(2), 164.414(b)')]),
'PRIV12':dict(topic='소규모 침해의 개별 통지와 HHS 보고 시계',sources=['ecfr45-164-web'],section='45 CFR 164.404(a)-(b), 164.408(c), 164.412 exception referenced',core='개인 통지는 발견 후 불합리한 지연 없이 최대 60 calendar days 이내이고, 500명 미만 HHS 보고는 발견 연도가 끝난 뒤 최대 60일 이내의 별도 경로다. Case B는 허용된 지연이 없다고 명시하므로 outer limit까지 통상 기다릴 수 없다.',rules=[
('The 60-day outer limit permits',False,'60일은 최대 한도이며 without unreasonable delay라는 독립 조건도 충족해야 한다. Case B는 허용된 지연도 배제했다.','164.404(b)'),
('The small-breach annual HHS route does not postpone',True,'500명 미만의 HHS 연간 보고는 수신자가 다른 별도 의무다. 개인 통지의 발견 후 기한을 연말까지 늦추지 않는다.','164.404(a)-(b), 164.408(c)'),
('The small-breach HHS clock starts 60 days after',False,'기산점은 환자의 다음 방문이 아니라 침해 발견이 속한 calendar year의 끝이다.','164.408(c)'),
('One regulator filing necessarily',False,'개인과 HHS는 별도의 통지 대상이다. HHS 제출 한 번이 자동으로 각 개인 통지를 충족하지 않는다.','164.404(a)-(d), 164.408(a), (c)'),
('A breach affecting fewer than 500 people permits',False,'500명 미만 경로는 HHS 보고 시점에 관한 예외이며 개인 통지 연기의 일반 허가가 아니다.','164.404(b), 164.408(c)'),
('Notice must be provided without unreasonable delay',True,'Case B에서 더 이른 통지가 가능한데도 최대 한도까지 관행적으로 기다리면 불합리한 지연 금지와 맞지 않는다.','164.404(b)'),
('Individual and regulator notifications have',True,'164.404는 개인, 164.408은 Secretary를 수신자로 하며 소규모 침해의 보고 시계는 다르다.','164.404(a)-(b), 164.408(c)'),
('The small-breach HHS deadline is within',True,'발견 연도 중 발생한 500명 미만 침해는 그 calendar year가 끝난 뒤 늦어도 60일 안에 보고한다.','164.408(c)')]),
'PRIV13':dict(topic='HHS 500명 이상과 media 500명 초과 경계',sources=['ecfr45-164-web'],section='45 CFR 164.404(a), 164.406(a)-(b), 164.408(b)-(c)',core='정확히 500명은 HHS 500 or more 경로에 해당한다. 특정 주·관할 residents more than 500인 media 경로는 정확히 500명만으로 충족하지 않는다. Case B의 501명은 후자에 해당하며 media 통지는 개인 통지를 대신하지 않는다.',rules=[
('The first breach meets the 500-or-more',True,'Case A의 정확히 500명은 500 or more에 포함되므로 HHS의 해당 경로다.','164.408(b)'),
('A required media notice replaces',False,'media 의무는 164.404(a)의 각 개인 통지와 함께 적용된다. 하나를 다른 하나의 대체물로 바꿀 수 없다.','164.404(a), 164.406(a)'),
('The second breach fails the media threshold',False,'501은 500보다 크다. 동일 주의 501 residents는 media 인원 기준에 해당한다.','164.406(a)'),
('The first breach meets the more-than-500',False,'정확히 500이라는 수는 more than 500이 아니다. 다른 media trigger가 없다는 사실도 명시되어 있다.','164.406(a)'),
('The second breach meets the more-than-500',True,'Case B는 한 주 주민 501명이므로 500명 초과 media 기준을 충족한다.','164.406(a)'),
('The first breach falls into the fewer-than-500',False,'정확히 500명은 less than 500이 아니므로 annual small-breach 경로에 들어가지 않는다.','164.408(b)-(c)'),
('Exactly 500 residents do not meet',True,'법문의 엄격한 >500 경계 때문에 정확히 500 residents만으로 media 인원 기준에 해당하지 않는다.','164.406(a)')]),
'PRIV14':dict(topic='Part 2 적용 주체·출처와 TPO consent의 범위',sources=['ecfr42-2-web','part2-final-rule','part2-fact-sheet'],section='42 CFR 2.11 program/records/SUD counseling notes; 2.12(a),(b),(d); 2.13(a); 2.31(a),(b),(d); 2.33(a)-(b); 89 FR 12472 effective/compliance dates',core='Part 2 program·record의 출처·수신자 지위를 따져야 하며 부프레노르핀이라는 약명만으로 모든 pharmacy record가 같은 program record가 되지 않는다. 현행 single future TPO consent 경로가 있지만 별도 상담 노트 consent와 환자 상대 절차 보호는 남는다. 2024 final rule 효력일 2024-04-16, 준수일 2026-02-16을 확인했다.',rules=[
('The current Part 2 framework has no possible',False,'2.31과 2.33은 모든 future TPO 사용·공개에 대한 single consent 경로를 명시적으로 허용한다.','2.31(a)(4)(i), (a)(5)(ii), 2.33(a)(2)'),
('SUD counseling notes and all general',False,'분리 보관되는 정의상 SUD counseling notes에는 2.31(b)의 별도 consent와 제한적 예외가 있다. 일반 기록과 consent 처리가 전부 같다는 말은 틀리다.','2.11 SUD counseling notes; 2.31(b)'),
('Alignment with HIPAA makes all',False,'HIPAA 조정 후에도 환자 상대 민사·형사·행정·입법 절차에 대한 사용·공개 보호가 남는다. 무제한 증거 사용은 허용되지 않는다.','2.12(d)(1), 2.13(a), 2.31(d), 2.33(b)(1)'),
("The record's source",True,'정의상 program 및 federally assisted 여부, 기록 출처와 수신자에 대한 적용을 따져야 한다. 약명은 그 조건들을 모두 증명하지 않는다.','2.11 program/records; 2.12(a),(b),(d)'),
('The permitted single TPO consent',True,'허용된 경로에도 consent의 요소·범위·취소와 수신자의 지위 등 조건이 있다. broad TPO consent로 모든 별도 보호가 없어지는 것은 아니다.','2.31(a)-(b), 2.33(a)-(b)'),
('Any buprenorphine prescription makes',False,'약물 이름만으로 모든 기록이 program record가 되지 않는다. 규칙의 program·record·federal assistance·recipient 조건을 별도로 적용한다.','2.11 program/records; 2.12(a),(b),(d)'),
('Legal-proceeding protections are not eliminated',True,'현행 TPO 연계 후에도 환자 상대 절차의 consent/court-order 보호와 separate consent 조건이 남는다.','2.12(d)(1), 2.13(a), 2.31(d), 2.33(b)(1)')]),
'PRIV15':dict(topic='ePHI 보호조치와 제안·현행 법규 구별',sources=['ecfr45-164-web','hipaa-security'],section='45 CFR 164.306(a)-(d), 164.308(a)(3)-(5), 164.310(b)-(c), 164.312(a),(d); current official compilation and HHS Security Rule overview',core='Covered entity/BA의 ePHI 보호에는 관리·물리·기술 조치가 함께 적용된다. flexibility 및 required/addressable 구분 때문에 유용한 기술 하나가 모두에게 특정 방식으로 의무화되는 것은 아니다. 제안의 단순 게시와 실제 효력 있는 법규는 구별해야 한다. 이름 없는 제안의 내용이나 효력일을 이 문항에서 추정하지 않는다.',rules=[
('Any useful security feature is automatically',False,'164.306(b),(d)는 유연한 접근과 required/addressable을 구별한다. 모든 유용한 기능이 모든 pharmacy에 동일한 특정 구현 의무가 되는 것은 아니다.','164.306(b)-(d)'),
('Security concerns confidentiality only',False,'법문은 confidentiality뿐 아니라 integrity와 availability도 함께 요구한다.','164.306(a)(1)'),
('Passwords do not substitute',True,'password management는 한 항목이다. 접근권 관리·훈련·workstation security 등 다른 적용 표준을 대체하지 않는다.','164.308(a)(3)-(5), 164.310(b)-(c), 164.312(a),(d)'),
('A proposed rule becomes binding merely',False,'온라인 게시 그 자체를 적용 의무와 동일시할 수 없다. 이 검토는 실제 현행 eCFR 표준을 사용했으며, 이름 없는 proposed text의 binding status를 인정하지 않는다. 이 문장은 절차적 판단 원칙이며 특정 제안의 내용에 관한 법적 판정은 아니다.','164.306(c)-(d); current official eCFR compilation status'),
('Strong passwords alone satisfy',False,'관리·물리·기술 safeguard의 적용 표준을 strong password 하나로 충족할 수 없다.','164.306(c), 164.308(a)(3)-(5), 164.310(c), 164.312(a)'),
("The proposal's status and effective requirements",True,'실제 현재 적용되는 표준과 제안 문서를 구별하고 효력을 확인해야 한다는 절차 원칙은 맞다. 특정 cybersecurity proposal이 현재 유효하다는 사실을 새로 보태지 않는다.','164.306(c)-(d); current official eCFR compilation status'),
('Availability and integrity are',True,'164.306(a)(1)은 세 목표를 병렬적으로 명시한다.','164.306(a)(1)')]),
'PRIV16':dict(topic='computer downtime과 incident 기록·평가',sources=['ecfr45-164-web','ma-247cmr9'],section='247 CMR 9.04(1), 9.16, 9.17, 9.19(22); 45 CFR 164.308(a)(1)(ii)(D),(6)-(7), 164.312(b)-(d), 164.402, 164.414(b)',core='MA downtime P&P는 조제·복구 후 computerized profile 기록·continuity·appropriate DUR을 포함해야 한다. 시스템 장애는 일반 면제가 아니며, incident 대응·기록·mitigation과 reportable breach 판정은 분리한다. relevant logs 보존은 audit review/incident documentation/integrity를 이행하는 방법이며 모든 로그의 무조건 동일 기간 보존이라는 새 의무를 만들지 않는다.',rules=[
('Every suspected incident automatically',False,'suspected incident에는 대응·문서화 의무가 있지만 모든 사건이 같은 외부 보고 결과를 갖지는 않는다. unsecured PHI breach 등 해당 trigger와 예외를 별도로 평가한다.','164.308(a)(6), 164.402, 164.414(b)'),
('An outage does not create',True,'downtime에도 별도 filling process·appropriate DUR·복구 후 profile 기록이 요구된다. 일반 면제 조항이 아니며 해당 ePHI authentication도 계속 적용된다.','247 CMR 9.04(1), 9.17, 9.19(22); 164.312(d)'),
('Restoring the computer eliminates',False,'MA는 시스템 복구 시 downtime 처방을 computerized medication profile에 기록하는 절차를 명시한다. 복구 자체가 후속 기록 확인을 없애지 않는다.','247 CMR 9.19(22)(b)'),
('Deleting the incident logs is a substitute',False,'사건 대응·결과 문서화, 시스템 activity review 및 정보 integrity와 상충한다. 로그 삭제는 해당 의무 이행의 대체물일 수 없다.','164.308(a)(1)(ii)(D), (a)(6)(ii); 164.312(b)-(c)'),
('Loss of electronic access authorizes',False,'MA의 별도 downtime 절차와 DUR 요구를 무시하고 identity·duplicate controls를 일괄 우회할 수 없다.','247 CMR 9.04(1), 9.17, 9.19(22); 164.312(d)'),
('Incident response should preserve',True,'조사에 필요한 증거 보존은 required activity review·incident response/outcome documentation 및 improper destruction 방지와 일치한다. 새 일률적 로그 보존 기간을 뜻하지는 않는다.','164.308(a)(1)(ii)(D), (a)(6)(ii); 164.312(b)-(c)'),
('A suspected incident must be assessed',True,'사건 대응·문서화를 하고, 관련 침해 정의·예외·보고 의무 적용 여부를 별도로 따진다. incident와 reportable breach는 같은 단어가 아니다.','164.308(a)(6), 164.402, 164.414(b)'),
('Restoration should include reconciliation',True,'복구 시 downtime 조제를 computerized profile에 반영하는 MA 명시 절차를 준수하기 위한 적절한 기록 대조다.','247 CMR 9.19(22)(b),(d)')]),
'RET01':dict(topic='미교부 처방 return-to-stock 용기와 기록',sources=['ma-247cmr9'],section='247 CMR 9.13(1)(a)-(b), (2); 9.01(5),(7)',core='아직 교부되지 않은 처방은 조건에 따라 RTS가 가능하나 manufacturer stock bottle에 넣을 수 없다. patient container 또는 적절한 용기에 product/strength/manufacturer-supplier-NDC/처음 filling 때 부여한 expiry를 표시하고 P&P가 있어야 한다. 이미 patient에게 교부된 약은 이 same RTS의 사실 요건과 다르다.',rules=[
("The uncollected tablets must not be returned",True,'미교부 처방 RTS에서도 manufacturer stock bottle 재투입은 명시적으로 금지된다.','247 CMR 9.13(1)(a)'),
('Medicine returned by a patient is automatically',False,'9.13은 준비했으나 아직 dispensed되지 않은 약의 경로다. patient에게 교부 후 돌아온 약에는 9.01(5),(7)과 다른 적법한 예외를 검토해야 하므로 자동 동일 경로가 아니다.','247 CMR 9.13(1); 9.01(5),(7)'),
('A new RTS container permits removal',False,'적절한 RTS 용기에도 법정 identification과 initial filling에 부여된 expiration date를 표시해야 한다. 새 용기 자체가 새 만료일을 주지 않는다.','247 CMR 9.13(1)(b)1-4'),
('An occasional RTS transaction is exempt',False,'P&P 의무에 가끔 한 번만 RTS하면 면제한다는 예외가 없다.','247 CMR 9.13(2)'),
("Uncollected tablets may be poured",False,'약국 통제 밖으로 나가지 않았다는 사실은 RTS 가능성과 관련될 뿐 manufacturer bottle 금지를 없애지 않는다.','247 CMR 9.13(1)(a)'),
('An eligible RTS container must retain',True,'법문은 제품명·강도/농도·제조사/공급자/NDC 및 initial filling expiry를 요구한다.','247 CMR 9.13(1)(b)1-4'),
('The pharmacy needs an RTS policy',True,'9.13(2)는 RTS policy and procedure 유지를 명시한다.','247 CMR 9.13(2)')]),
'RET02':dict(topic='오조제·defective 반품 수령과 재고 금지',sources=['ma-247cmr9'],section='247 CMR 9.01(5),(7); separate duties remain conditional, no report deadline asserted',core='자신이 잘못 교부했거나 defective/contaminated로 의심되는 약은 받아야 한다. 받은 약은 재고 복귀하지 않고 격리·적법 폐기한다. proven injury가 수령 조건은 아니다. 수령의무 이행이 다른 적용 의무까지 면제하는 내용은 없다. controlled ultimate-user collection과 일반 inventory 혼입 경로를 만들지 않는다.',rules=[
('Receiving the medication finishes',False,'반품을 받았다는 사실은 9.01(7)의 수령 단계일 뿐 다른 조건부 오류 대응·보고 의무를 완료하거나 면제하지 않는다. 특정 외부 보고가 반드시 발생한다고 보태지는 않는다.','247 CMR 9.01(7)'),
('The pharmacy must wait for proven',False,'suspected defective or contaminated가 조건이다. 손해 확정이나 injury 입증 후까지 기다리는 요건은 없다.','247 CMR 9.01(7)(b)'),
('Acceptance of the error return authorizes',False,'같은 항은 재고 복귀를 금지하고 격리·적법 처분을 요구한다. 수령은 다른 환자 재판매의 허가가 아니다.','247 CMR 9.01(7)'),
('The described Massachusetts rule requires',True,'이 pharmacy가 이전에 patient에게 error로 dispensed한 약이므로 수령 의무가 적용된다. 카운터를 넘어갔다는 이유로 거절할 수 없다.','247 CMR 9.01(7)(a)'),
('The accepted medication must be quarantined',True,'9.01(7)에 따라 수령한 약은 inventory로 돌아갈 수 없고 quarantined and properly disposed되어야 한다.','247 CMR 9.01(7)'),
('Crossing the counter eliminates',False,'이 pharmacy의 error dispensing은 이미 patient에게 교부한 약을 전제로도 명시적으로 수령하도록 규정되어 있다.','247 CMR 9.01(7)(a)'),
('A suspected defect or contamination can trigger',True,'조문은 suspected라는 기준을 사용한다. 다만 해당 pharmacy가 이전에 dispensed한 약이라는 문맥을 유지한다.','247 CMR 9.01(7)(b)')]),
'RET03':dict(topic='자발적 환자 반품 collection과 DEA collector authorization',sources=['ma-247cmr9','ecfr21-1317-web'],section='247 CMR 9.01(5),(7); 21 CFR 1317.30(a), 1317.40(a)-(c), 1317.75(a)-(c)',core='정상·비결함 단순 불필요 반품을 모두 받아야 한다는 MA 일반 의무는 아니다. 별도 자발적 collection은 허용 경로·등록 변경·방법 조건을 충족해야 하며 collected controlled drugs는 파기 목적이지 saleable stock이 아니다. error-return 의무와 모든 약국의 public collection 의무를 동일시하지 않는다.',rules=[
('The error-return duty requires every',False,'특정 error/defect 반품의 수령 의무가 모든 약국의 public collection program 운영 명령으로 확장되지는 않는다. DEA도 desire to be collectors인 registrants의 authorization을 별도로 규정한다.','247 CMR 9.01(7); 21 CFR 1317.40(a)'),
('An ordinary DEA pharmacy registration by itself',False,'retail pharmacy도 collector가 되려면 1301.51에 따라 registration을 modify하여 authorization을 받아야 한다.','21 CFR 1317.40(a)'),
('The described state rule does not generally',True,'MA는 properly dispensed and not defective at dispensing인 medication을 patient에게서 받아야 하는 일반 의무가 없음을 명시한다.','247 CMR 9.01(7)'),
('Operating a take-back service permits',False,'controlled collection은 destruction 목적이고, receptacle 입고 후 개별 sorting/handling도 금지된다. 반품을 재판매 재고로 바꾸는 권한이 아니다.','21 CFR 1317.30(a), 1317.75(c); 247 CMR 9.01(5),(7)'),
('The dispensing pharmacy must accept every nondefective',False,'정상 교부·비결함 약의 모든 단순 반품을 error-return와 동일하게 의무 수령하는 조문은 아니다.','247 CMR 9.01(7)'),
('General controlled-drug collection requires',True,'collector modification/authorization과 등록 위치 및 collection method 조건을 별도로 충족해야 한다.','21 CFR 1317.30(a), 1317.40(a)-(c), 1317.75'),
('A voluntary disposal-collection service does not turn',True,'수거는 파기 목적의 경로이며 다른 환자에게 재고로 다시 교부하는 경로가 아니다.','21 CFR 1317.30(a), 1317.75(c); 247 CMR 9.01(5),(7)')]),
'RET04':dict(topic='자체 multidrug-single-dose package 동일 환자 재포장',sources=['ma-policy2023-01','ma-247cmr9'],section='MA Board Policy 2023-01 revised 2025-01-09, II.9-10 and Return and Repackaging of Multi-Drug-Single-Dose Packaging 1(a)-(d),2-3 (PDF pp.2-4); 247 CMR 9.01(5)',core='공식 정책의 해당 경로는 이 pharmacy가 이전에 dispensed한 multi-drug-single-dose package를 same patient에게 조건부로 repack/re-dispense하는 것이다. unless otherwise prohibited를 유지해야 하며, 제거약의 general inventory/다른 patient 사용은 불가하다. 변경된 각 cell의 name/strength 및 label·방향·변경 기록과 변경 약사 identification을 유지한다. 원문의 multidrug package는 정확한 포장 유형을 명시하면 더 좋지만 appropriate/pathway라는 한정을 무조건 허용으로 읽지는 않았다.',rules=[
('Identifiable removed tablets may be assigned',False,'약이 식별 가능해도 제거한 약을 inventory로 돌리거나 다른 patient에게 dispense할 수 없다는 정책 2번의 금지는 사라지지 않는다.','Policy 2023-01 Return and Repackaging 2'),
('The described pathway permits appropriate',True,'정책은 unless otherwise prohibited라는 조건 아래 자신이 이전에 교부한 multi-drug-single-dose package를 same patient에게 재포장·재교부하는 경로를 명시한다. 모든 multidrug 포장이나 controlled-drug 예외를 일괄 허용한다는 뜻으로 확대하지 않는다.','Policy 2023-01 Return and Repackaging 1(a)-(d); 247 CMR 9.01(5)'),
('The original label can remain unchanged',False,'내용물이 바뀐 후 원 label이 실제 medication과 맞지 않으면 label 요구를 충족하지 않는다. removable cell도 name/strength로 re-label해야 한다.','Policy 2023-01 II.9-10; Return and Repackaging 1(c)'),
('The original dispensing record alone accounts',False,'정책은 모든 repackaging/removal/re-dispensing과 변경 담당 약사를 별도로 추적하는 기록을 요구한다. 원 dispensing만 남기는 것으로는 부족하다.','Policy 2023-01 Return and Repackaging 3'),
('Any therapy change requires discarding every',False,'정책은 해당 조건 아래 중단약 제거 또는 새 약 추가 후 같은 patient에게 남은 약을 재교부할 수 있게 한다. 모든 약의 무조건 폐기만이 유일한 경로는 아니다.','Policy 2023-01 Return and Repackaging 1(a)-(b)'),
('Removed medication may not be transferred',True,'제거약의 inventory 복귀와 반환 patient 외 다른 patient 교부를 정책이 명시적으로 금지한다.','Policy 2023-01 Return and Repackaging 2'),
('The revised labels and directions must match',True,'label에 포함되는 약의 정보와 실제 포장·removable cell의 name/strength가 일치해야 한다. 변경 전 정보를 그대로 두는 경로가 아니다.','Policy 2023-01 II.9-10; Return and Repackaging 1(c)'),
('The pharmacy must record the repackaging',True,'정책 3번은 변경·제거·재교부를 account/document하고 변경 약사를 식별하도록 한다.','Policy 2023-01 Return and Repackaging 3')])
}
# Specific realism findings. A false criterion is a substantive finding, never inferred from a count.
REALISM={
'0495':{'jurisprudence_reasoning':'A의 own applicable analysis와 D의 applicable procedure는 구체 권리 행사·첫 제공·응급 여부를 판단하지 않아 사례 사실 없이도 고를 수 있는 메타 문장이다.','authentic_distractors':'네 보기 모두 해당 분석을 하라는 안전한 문장으로, NPP와 authorization을 혼동하는 구체 대안과 경쟁하지 않는다.','wording_not_guessable':'all applicable analysis/procedure 및 distinct purposes 표현만으로 전부 선택하는 경향이 강해 법적 조건 지식의 필요성이 낮다.','reasoning_not_trivia':'각 권리의 적용 사실이나 authorization 요소를 주지 않아 실질적인 법 적용보다 용어 구분에 머문다.'},
'0496':{'wording_not_guessable':'오답으로 고르게 한 D의 waives all access, amendment, and confidential-communication rights가 포괄적 권리 박탈을 주장하고 다른 세 보기는 모두 신중하게 한정되어 있다.','authentic_distractors':'NPP 서명이 모든 권리를 소멸시킨다는 극단적 설명은 실제로 혼동하기 쉬운 특정 authorization 범위·목적과 경쟁하지 못한다.'},
'0501':{'wording_not_guessable':'A의 every medical record exact destruction, B의 shortest minimum, C의 conceal the correction과 달리 D만 합리적인 한정을 유지해 키를 문체로 추측하기 쉽다.','authentic_distractors':'C의 conceal은 보존기간 혼동이 아니라 은폐를 명시한 행동으로, 진짜 retention·amendment 혼동을 측정하지 않는다.','natural_rule_combination':'보존기간 사례에 amendment audit trail 은폐 보기를 붙였지만 사례에는 수정 요청이 없어 자연스러운 결합이 약하다.'},
'0502':{'wording_not_guessable':'키 A만 minimum의 범위를 신중히 한정하고 B는 conceal, C는 choose shortest, D는 every document를 주장해 법규를 몰라도 배제하기 쉽다.','authentic_distractors':'수정 은폐를 허용한다는 B는 원래의 일괄 파기 주장과 실무적으로 경쟁하는 대안이 아니다.','natural_rule_combination':'두 사례 모두 보존을 묻는데 amendment 은폐까지 같은 정답 세트에 섞어 불필요한 주제 전환을 만든다.'},
'0504':{'wording_not_guessable':'유일한 INCORRECT 키 B가 to conceal the correction을 노골적으로 포함해 관련 보존·수정 조문을 몰라도 고를 수 있다.','authentic_distractors':'나머지 세 보기는 모두 최소·대상 범위를 정확히 한정하는 반면 은폐 허용만 극단적이어서 실제 법규 혼동에서 나온 경쟁력이 낮다.'},
'0505':{'wording_not_guessable':'키 C만 평가한다는 신중한 표현이고 A는 conclusively, B는 undocumented assurance, D는 automatically completes로 단독 해결을 주장한다.','authentic_distractors':'B의 문서 없는 확신과 D의 CQI 자동 완료는 실제 4-factor risk assessment의 잘못된 적용보다 상식적으로 배제하기 쉬운 대안이다.'},
'0506':{'wording_not_guessable':'D의 mitigation but not by itself와 달리 A의 categorically, B의 undocumented assurance, C의 automatically completes가 정답 신호를 만든다.','authentic_distractors':'검토할 실제 정보·수령자·보유 능력을 구체적으로 달리한 대안이 없어 회수 후 exception 판단과 경쟁하지 못한다.'},
'0508':{'wording_not_guessable':'INCORRECT 키 A의 automatically completes all privacy breach analysis가 나머지 조건부 보기에 비해 지나치게 절대적이다.'},
'0509':{'authentic_distractors':'C의 각 환자 다음 방문 60일이라는 기산점은 이 HIPAA breach 절차에서 경쟁하는 실무 기한이 아니어서 다른 수신자·발견 연도 혼동보다 약하다.'},
'0510':{'authentic_distractors':'A의 다음 방문 후 60일은 발견일·연말 보고와 혼동할 법한 실제 deadline이 아니라 임의의 방문 사건을 끼워 넣은 대안이다.'},
'0512':{'wording_not_guessable':'INCORRECT 키 D만 one filing necessarily all individuals라는 일괄 대체를 주장하고 다른 보기는 숫자·대상별 한정을 갖춰 법규보다 표현 차이로 고르기 쉽다.'},
'0513':{'authentic_distractors':'C의 501 is not more than 500은 법적 threshold 혼동이 아니라 산술 자체를 부정하는 보기여서 genuine legal distractor가 아니다.'},
'0517':{'wording_not_guessable':'D의 source/status must be examined가 신중한 키이고 A의 no possible, B의 no distinct treatment, C의 all unrestricted evidence가 모두 절대적이다.','authentic_distractors':'program 해당 여부의 실제 차이를 구체화하지 않고 전면 부정·무제한 증거 허용을 택하게 하여 적용 경계 판단력이 약하다.'},
'0518':{'wording_not_guessable':'A만 conditions and scope를 유지한다. B의 모든 기록 동일, C의 any buprenorphine every record, D의 all unrestricted가 함께 오답 신호를 준다.'},
'0520':{'wording_not_guessable':'B만 counseling notes와 all general records의 차이가 전혀 없다고 단정하고 나머지는 source examination/conditions/protections를 유지해 세부 Part 2 법규 없이 고르기 쉽다.'},
'0521':{'wording_not_guessable':'키 C만 passwords do not substitute라는 합리적 한정이다. A의 any useful automatically every pharmacy, B의 confidentiality only, D의 merely posted가 노골적이다.','authentic_distractors':'온라인 게시만으로 효력이 생긴다는 D는 효력일·준수일 혼동 같은 실제 법적 선택과 경쟁하지 않는다.'},
'0522':{'jurisprudence_reasoning':'어떤 제안인지·최종 여부·효력일을 주지 않아 D의 status must be checked라는 일반 확인 원칙만 선택한다. 구체 규칙을 적용하지 않는다.','wording_not_guessable':'D만 status/effective requirements를 확인하는 신중한 처리이고 다른 보기는 any useful automatically, passwords alone entire, confidentiality only이다.','reasoning_not_trivia':'법적 효력에 관한 실제 날짜나 문서 상태 판단보다 일반 문서 확인 태도 선택에 머문다.'},
'0524':{'jurisprudence_reasoning':'키 A의 any useful feature automatically mandate every pharmacy는 구체 구현 기준·addressable 판단을 전혀 주지 않아 추상적 법규/권고 구분만 묻는다.','wording_not_guessable':'A만 보편 자동 의무를 주장하고 나머지 세 보기는 모두 제한을 유지해 INCORRECT 선택이 문체로 드러난다.'},
'0525':{'wording_not_guessable':'키 B의 does not create a general exemption과 달리 A는 every identical, C는 restoration eliminates, D는 deleting as substitute여서 정답이 상식적 안전 표현으로 드러난다.'},
'0526':{'wording_not_guessable':'로그를 지우지 말고 보존하라는 C는 나머지 전면 우회·복구 후 후속 확인 폐지·매번 동일 보고보다 상식적으로 안전한 유일 보기다.','authentic_distractors':'로그 보존의 실제 범위·security incident와 reportable breach의 조건을 제시하지 않아 법규 혼동 대신 무조건적인 극단을 고르게 한다.'},
'0527':{'wording_not_guessable':'네 보기가 모두 면제 없음·증거 보존·적용 평가·적절한 기록 대조라는 안전한 절차 문장이라 특정 MA downtime 의무를 몰라도 전부 선택하기 쉽다.'},
'0528':{'wording_not_guessable':'D만 every suspected incident automatically identical reporting이라고 일괄 결과를 주장하고 다른 세 보기는 조건부 안전 조치여서 부정 극성의 키가 드러난다.'},
'0529':{'distinct_from_bank':'canonical MA-Q-0225와 미교부 약·약국 통제·manufacturer bottle에 되붓기라는 핵심 사실과 금지 판단이 같다. 추가 Case B가 있어도 Case A만 묻는 이 문항에서는 독립된 판단 차이를 만들지 않는다.'},
'0533':{'distinct_from_bank':'canonical MA-Q-0088 역시 해당 약국이 error로 dispensed한 intact bottle의 의무 수령을 포함한다. wrong person이라는 표현 변화는 같은 수령 결론을 바꾸는 새 예외가 아니다.','authentic_distractors':'B의 proven injury까지 대기와 A의 모든 후속 의무 종료는 실제 수령 범위·defect 의심을 경쟁시키기보다 극단적 허용을 넣었다.'},
'0534':{'distinct_from_bank':'canonical MA-Q-0088이 이미 error-return의 inventory 금지·quarantine을 같은 판단으로 묻는다. Case B의 ordinary inventory 제안은 새 적용 경계가 아니다.','authentic_distractors':'C의 proven injury 대기는 격리·처분 경로에 관한 실무적 선택지가 아니며 D의 모든 후속 의무 완료도 지나치게 포괄적이다.'},
'0536':{'wording_not_guessable':'INCORRECT 키 B만 finishes all otherwise applicable duties라며 단독 단계가 모든 의무를 끝낸다고 단정한다. 다른 세 보기는 조건·대상에 한정된다.'},
'0537':{'authentic_distractors':'A는 특정 error-return 수령 의무를 모든 약국의 public collection 운영으로 비약한다. 단순 반품 수령 범위에 관한 실제 경쟁 해석보다 약하다.','wording_not_guessable':'키 C만 does not generally require로 범위를 제한하고 A every pharmacy, B every receptacle, D reuse stock은 넓은 허용·의무를 주장한다.'},
'0538':{'wording_not_guessable':'D만 applicable authorization and method conditions를 확인하는 제한적 표현이고 A resale, B every nondefective, C every pharmacy public program은 전면적 주장이다.'},
'0540':{'wording_not_guessable':'키 A만 error-return에서 every pharmacy public program으로 무리하게 확장하고 나머지 세 보기는 범위 한정을 유지하여 INCORRECT가 드러난다.'},
'0541':{'wording_not_guessable':'키 B만 described pathway/appropriate/same patient의 조건을 남기는 반면 A는 다른 환자 재고, C는 label unchanged, D는 original record alone으로 조건을 제거한다.'},
}
F['RET04']['sources'].append('ma-94c21')
F['RET04']['rules']=[(a,b,c,d+'; M.G.L. c.94C §21 first paragraph' if a in ['The original label can remain unchanged','The revised labels and directions must match'] else d) for a,b,c,d in F['RET04']['rules']]
CRITERIA=['jurisprudence_reasoning','practice_plausibility','authentic_distractors','wording_not_guessable','reasoning_not_trivia','natural_rule_combination','appropriate_drug_context','distinct_from_bank','not_schedule_flashcard','public_style_without_copying']

def source_entry(k):
 m=read(BASE/'official'/f'{k}.meta.json')
 assert m.get('status')==200 and '/error' not in m['final_url']
 effective='UNKNOWN';version='official posted document retrieved 2026-11-04; distinct commencement not independently established'
 if k.startswith('ecfr'):
  version='eCFR displayed current-through 2026-11-02; title amendment date differs from individual provision commencement'
 elif k=='ma-247cmr9':version='Mass. Register #1536, 12/6/2024 posted PDF; separate commencement not established'
 elif k=='ma-policy2023-01':version='Policy adopted 2023-04-06; revised 2023-11-02 and 2025-01-09; separate commencement not stated in retrieved PDF'
 elif k in ['part2-final-rule','part2-fact-sheet']:
  effective='2024-04-16';version='2024 final rule; compliance 2026-02-16; HHS fact sheet updated 2026-01-30'
 elif k=='hipaa-access-original-faq':version='Official HHS timely-access FAQ, first answer and BA handoff paragraph, cites 164.524(b)(2)'
 coverage={
 'ecfr45-164-web':['45 CFR 164.306(a)-(d), 164.308(a), 164.310, 164.312; 164.402, 164.404, 164.406, 164.408, 164.414; 164.508, 164.520(c)(2), 164.522(b), 164.524(b)(2), 164.526(c)(1),(d)(4), 164.530(h),(j)'],
 'ecfr42-2-web':['42 CFR 2.11 program/records/SUD counseling notes definitions; 2.12(a),(b),(d); 2.13(a); 2.31(a),(b),(d); 2.33(a),(b)'],
 'ecfr21-1317-web':['21 CFR 1317.30(a), 1317.40(a)-(c), 1317.75(a)-(c)'],
 'ma-247cmr9':['247 CMR 9.01(5),(7); 9.04(1); 9.13(1)-(2); 9.16; 9.17; 9.19(22)'],
 'ma-policy2023-01':['Policy 2023-01 II.9-10; Return and Repackaging of Multi-Drug-Single-Dose Packaging 1(a)-(d),2-3; PDF pages 2-4'],
 'ma-94c23':['M.G.L. c.94C §23(e)'],
 'ma-94c21':['M.G.L. c.94C §21 first paragraph, prescription label directions for use'],
 'hipaa-access-original-faq':['HHS FAQ answer first paragraph and BA handoff paragraph; 164.524(b)(2) explanation'],
 'hipaa-security':['HHS Summary of the HIPAA Security Rule: General Rules/Administrative/Physical/Technical Safeguards; corroboration only'],
 'part2-final-rule':['89 FR 12472; DATES: effective 2024-04-16, compliance 2026-02-16'],
 'part2-fact-sheet':['Patient Consent; SUD Counseling Notes; Legal Proceedings; compliance date section; corroboration only'],
 }[k]
 return dict(source_id=k,authority=({'ma-247cmr9':'Massachusetts Board 247 CMR 9','ma-policy2023-01':'Massachusetts Board Policy 2023-01','ma-94c23':'Massachusetts General Laws c.94C §23','ma-94c21':'Massachusetts General Laws c.94C §21','ecfr45-164-web':'45 CFR Part 164','ecfr42-2-web':'42 CFR Part 2','ecfr21-1317-web':'21 CFR Part 1317'}.get(k,'HHS official publication')),source_type=('MA_PROMULGATED_REGULATION' if k=='ma-247cmr9' else 'MA_BOARD_POLICY' if k=='ma-policy2023-01' else 'MA_STATUTE' if k in ['ma-94c23','ma-94c21'] else 'FEDERAL_REGULATION' if k.startswith('ecfr') or k=='part2-final-rule' else 'OTHER_OFFICIAL'),official_url=m['requested_url'],exact_section='; '.join(coverage),law_checked_date='2026-11-04',effective_date=effective,version=version,evidence_path=m['raw_path'],evidence_sha256=m['raw_sha256'],text_path=m['text_path'],text_sha256=m['text_sha256'],retrieval_provenance_path=str((BASE/'official'/f'{k}.meta.json').relative_to(ROOT)),retrieval_provenance_sha256=sha((BASE/'official'/f'{k}.meta.json').read_bytes()),retrieval=m,document_identity_verified=True,limits_ko='HTTP 200만으로 인정하지 않고 제목·조항 본문·문서 버전을 확인했다. eCFR는 표시된 11월 2일 이후 변경까지 증명하지 않으며 UNKNOWN 효력일을 추정하지 않았다.')

sourcekeys=sorted({k for f in F.values() for k in f['sources']})
sources={k:source_entry(k) for k in sourcekeys}
bynear={r['question_id']:r for r in nearest['nearest']};candidates={r['question_id']:r for r in nearest['visible_candidates']}
defaultids=set(read(BASE/'context/default-ids-at-assignment.json'))
records=[]
for r in packet['records']:
 q=r['original_visible_content'];qid=r['question_id'];family=loc[qid]['family_id'];f=F[family];findings=[];trueids=[]
 for c in q['choices']:
  matches=[x for x in f['rules'] if c['text'].startswith(x[0])]
  assert len(matches)==1,(qid,c,matches)
  _,truth,reason,sections=matches[0]
  if truth:trueids.append(c['id'])
  bindings=[]
  for k in f['sources']:
   if k in ['part2-final-rule','part2-fact-sheet','hipaa-security']: continue
   if k=='ma-94c23' and 'M.G.L.' not in sections: continue
   if k=='ma-94c21' and '§21' not in sections: continue
   if k=='hipaa-access-original-faq' and 'HHS FAQ' not in sections: continue
   if k=='ma-247cmr9' and '247 CMR' not in sections: continue
   if k=='ecfr21-1317-web' and '1317.' not in sections: continue
   if k=='ecfr45-164-web' and not re.search(r'164\.\d+', sections): continue
   if k=='ma-policy2023-01' and 'Policy 2023-01' not in sections: continue
   src=sources[k];url=src['official_url']
   if k.startswith('ecfr'):
    nums=re.findall(r'(?<!\d)(164\.\d+|2\.\d+|1317\.\d+)',sections)
    if nums:url=url.split('#')[0]+'#'+nums[0]
   parts=sections.split(';')
   local=';'.join(part.strip() for part in parts if ('247 CMR' in part if k=='ma-247cmr9' else 'M.G.L.' in part if k in ['ma-94c23','ma-94c21'] else 'Policy 2023-01' in part if k=='ma-policy2023-01' else 'HHS FAQ' in part if k=='hipaa-access-original-faq' else '1317.' in part if k=='ecfr21-1317-web' else '164.' in part or 'current official' in part if k=='ecfr45-164-web' else True))
   assert local,(qid,k,sections)
   bindings.append(dict(source_id=k,official_url=url,exact_section=local,law_checked_date='2026-11-04',evidence_path=src['evidence_path'],evidence_sha256=src['evidence_sha256']))
  findings.append(dict(choice_id=c['id'],option_text=c['text'],option_sha256=sha(c['text'].encode()),proposition_supported=truth,finding_ko=reason,authorities=bindings))
 incorrect='INCORRECT' in q['stem'];expected=[c['id'] for c in q['choices'] if (c['id'] not in trueids if incorrect else c['id'] in trueids)]
 assert q['question_type']=='SATA' or len(expected)==1,(qid,expected)
 assert expected==q['correct_choice_ids'],(qid,expected,q['correct_choice_ids'])
 criteria={k:True for k in CRITERIA};criteria['public_style_without_copying']=None
 close=bynear[qid];canon=close['canonical'][0]['question_id'];pub=close['public'][0]['question_id'];different=close['public_different_family'][0]['question_id']
 target='INCORRECT 단일 선택' if incorrect else '전체 참 조합 선택' if q['question_type']=='SATA' else 'Case A의 단일 결론' if 'addresses Case A' in q['stem'] else 'Case B의 단일 결론'
 explanations={
 'jurisprudence_reasoning':f"{f['topic']}에 관한 {target}을 결정한다. 구체 주체·조건·별도 의무의 적용이 있어 법적 판단이 존재한다.",
 'practice_plausibility':f"사례의 약국 업무({q['stem'].split(': ',1)[1].split(';',1)[0]})는 {f['topic']} 검토를 실제로 일으킬 수 있어 실무 상황 자체는 타당하다.",
 'authentic_distractors':f"{target}에서 대안들은 {f['topic']}의 대상·범위·기산점 또는 예외를 바꾸어 경쟁한다. 아래 개별 false finding이 있으면 그 결함을 우선한다.",
 'wording_not_guessable':f"{target}에 대한 정답은 {f['topic']}의 실제 적용을 구분해야 한다. 아래 별도 giveaway 지적이 없는 한 숫자나 반복 형식 자체를 결함으로 간주하지 않았다.",
 'reasoning_not_trivia':f"약명·번호의 단순 회상이 아니라 {f['topic']}의 허용/의무/금지 또는 수신자별 조건을 적용한다.",
 'natural_rule_combination':f"두 사례가 {f['topic']}라는 같은 업무 경로를 공유하여 조건별 결론을 비교할 수 있다. 아래 별도 지적이 없는 한 두 사례 형식만으로 실패시키지 않았다.",
 'appropriate_drug_context':('buprenorphine은 SUD 기록 적용을 약명으로 단정하는 오류를 보여주기 위한 것으로, 특정 약물의 치료 적응증이나 schedule만 외우게 하지 않는다.' if family=='PRIV14' else '이 문제의 법적 결과는 특정 상품의 약리나 브랜드에 좌우되지 않는다. 이름 없는 medication/PHI/기록 문맥은 필요한 판단을 방해하지 않는다.'),
 'distinct_from_bank':f"canonical {canon}, public nearest {pub}, 다른 family의 public {different} 보이는 stem과 모든 보기를 실제로 비교했다. same-family 변형은 같은 사례임을 밝힌 archive 연습이며 assigned ID는 현재 default pool에 없다. 그 존재만으로 실패시키지 않았고 구체 동일 판단이 있으면 아래 별도 지적했다.",
 'not_schedule_flashcard':f"{qid}는 {f['topic']}의 상황 적용 문항이다. 약물 schedule 단독 분류를 묻지 않는다.",
 'public_style_without_copying':'현재 public style profile의 scenario/selected-response 구조와 원문은 비교했으며 보호된 Pre-MPJE·회상·상용 문항은 사용하지 않았다. 하지만 NABP public sample PDF 및 format/competency page의 이번 직접 조회가 403이므로 공개 원문 wording 직접 대조를 완료했다고 주장하지 않는다. 이 criterion은 NOT_ASSESSED다.'}
 for criterion,reason in REALISM.get(qid[-4:],{}).items():criteria[criterion]=False;explanations[criterion]=reason
 hasfail=any(v is False for v in criteria.values())
 rv='FAIL' if hasfail else 'NOT_ASSESSED';disposition='NEEDS_REMEDIATION' if hasfail else 'SOURCE_BLOCKED'
 duplication=[]
 for kind in ['canonical','public','public_different_family']:
  for neighbor in close[kind]:
   candidate=candidates[neighbor['question_id']]
   own_read='stem 및 모든 보기 실제 읽음; 키·해설·기존 판단은 입력하지 않음'
   if kind=='public' and neighbor['same_family']:
    comparison='같은 두 사례와 판단을 공유하는 family 변형이다. 원문 learning_boundary와 default 제외 맥락을 고려하였으며 자동 FAIL 근거로 쓰지 않았다.'
   elif (family=='RET01' and candidate['question_id']=='MA-Q-0225'):
    comparison='미교부·약국 통제·manufacturer bottle 금지 판단이 직접 겹친다. Case A만 묻는 0529는 같은 판단이며, 0530의 label/initial-expiry·0532의 이미 patient에게 dispensed된 약과의 경계는 별도 범위를 평가했다.'
   elif (family=='RET02' and candidate['question_id']=='MA-Q-0088'):
    comparison='error return 수령·inventory 제외·quarantine 판단이 직접 겹친다. 0533/0534는 같은 핵심 결정이고, 0536은 수령 후 남는 다른 의무를 묻는 차이를 평가했다.'
   else:
    comparison=f"후보의 문제는 {candidate['stem'][:135]}라는 사실로 시작한다. {f['topic']}와 일부 법규·업무 단어가 겹치지만 그 후보의 실제 결론·사실 차이를 확인했으며 lexical score를 semantic duplicate 결론으로 바꾸지 않았다."
   duplication.append(dict(corpus=kind,**neighbor,candidate_default=neighbor['question_id'] in defaultids,read_scope=own_read,visible_candidate_sha256=sha(json.dumps(candidate,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()),comparison_ko=comparison))
 choicesreview=[]
 for c in q['choices']:
  old=q['explanation']['choice_analysis'][c['id']]
  finding=next(x for x in findings if x['choice_id']==c['id'])
  selected=c['id'] in expected
  choicesreview.append(dict(choice_id=c['id'],complete_rationale_read=True,original_rationale_sha256=sha(old.encode()),assessment_ko=f"원문 보기 {c['id']} 해설 전문을 읽었다. 이 명제의 독립 판단은 {'참' if finding['proposition_supported'] else '거짓'}이며, {target}의 극성에 따라 {'선택' if selected else '비선택'}하는 기존 설명과 일치한다. "+finding['finding_ko']))
 legal=dict(existing_answer_correct='YES',stored_key=q['correct_choice_ids'],independently_expected_key=expected,polarity='INCORRECT' if incorrect else 'CORRECT',question_type=q['question_type'],per_choice_findings=findings,authorities=[{k:sources[s][k] for k in ['source_id','authority','source_type','official_url','exact_section','law_checked_date','effective_date','version','evidence_path','evidence_sha256']} for s in f['sources']],verdict='KEEP',finding_ko=f['core'],blocker=None,original_explanation_review=dict(core_read_in_full=True,core_sha256=sha(q['explanation']['core_reasoning'].encode()),core_assessment_ko=f['core'],all_choice_rationales_read_in_full=True,choice_reviews=choicesreview,learning_boundary_read=True,limits_ko='원 해설은 검토 대상이지 법률권위가 아니다. 키는 독립 명제 판정 뒤 비교했다. related requirements는 해당 조건이 있을 때에만 적용하며 모든 사건이 모든 보고 의무를 일으킨다고 확대하지 않는다.'),ma_federal_boundary_ko='연방 HIPAA/Part 2/DEA 요건과 MA의 독립 처방·반품·downtime 의무는 별도다. 한 체계의 허용이 다른 적용 제한을 없애지 않는다. 이 stem의 묻는 범위를 넘어 특별 MA consent 또는 예외를 보태지 않았다.',uniqueness_or_combination_review_ko=f"각 보기의 명제 참/거짓을 먼저 독립 판정했다. {target}의 도출 키는 {','.join(expected)}이며 저장 키와 같다. "+('네 보기가 모두 참인 SATA 조합을 실제로 확인했으며 all-true 형식만으로 오류로 판정하지 않았다.' if q['question_type']=='SATA' else '단일 정답 유일성을 확인했다.'))
 record=dict(question_id=qid,record_sha256=r['record_sha256'],visible_content_sha256=r['visible_content_sha256'],family_id=family,read_scope=dict(stem='FULL',all_choices=[c['id'] for c in q['choices']],stored_key=True,core_reasoning='FULL',all_choice_rationales=[c['id'] for c in q['choices']],learning_boundary='FULL',hidden_statement_truth='NOT_ACCESSED',prior_author_or_independent_judgments='NOT_ACCESSED'),legal_review=legal,realism_review=dict(verdict=rv,decision='MAJOR_REWRITE' if hasfail else 'HOLD',criteria=criteria,criterion_findings_ko=explanations,duplicate_evidence=duplication,duplicate_measurement_path=str((BASE/'nearest-visible.json').relative_to(ROOT)),public_style_blocker='NABP official sample/format/competency direct HTTP 403; no successful direct public-source wording comparison',default_pool_member=False),safe_hold_recommended=True,release_eligible=False,canonical_release_credit=0,disposition=disposition,required_next_action_ko=('지적한 실제 realism 결함을 편집자가 수정하거나 기존 archive에만 유지하는 목적을 명확히 하고 새 current-hash fresh 검토를 받는다. NABP 공개 원문의 접근 실패도 해소한다.' if hasfail else 'NABP 허용 공개 style 원문으로 미완료 criterion을 별도 확인한다. 현재 결과는 realism PASS나 release 승인으로 사용할 수 없다.'))
 records.append(record)

files=['docs/INDEPENDENT_LEGACY_REVIEW_RUNBOOK.md','docs/RELEASE_POLICY.md','docs/AUDIT_WORKFLOW.md','docs/SOURCE_USE_POLICY.md','docs/QUESTION_AUTHORING_STANDARD.md','data/exam_style/mpje_style_profile.json','data/blueprint.json','schemas/audit.schema.json','schemas/question.schema.json','schemas/blueprint.schema.json','schemas/exam_style_profile.schema.json']
context={p:dict(file_sha256=sha((ROOT/p).read_bytes())) for p in files}
for p in ['data/exam_style/mpje_style_profile.json','data/blueprint.json']:
 o=read(ROOT/p);context[p].update(content_version=o['content_version'],semantic_hash=o['content_hash'])
retrievals=[]
for p in sorted((BASE/'official').glob('*.meta.json')):
 m=read(p);identity=m.get('status')==200 and '/error' not in m.get('final_url','')
 m['document_identity_verified']=identity
 m['used_as_legal_authority']=m['source_id'] in sources
 if not identity:m['law_checked_date']=None
 retrievals.append(m)
report=dict(schema_version='independent-legacy-full-review/1',stage='independent-legacy',job_id=assignment['job_id'],independent_of_authors=True,auditor='GPT',auditor_instance=INSTANCE,actor_provenance=dict(actor_id=ACTOR,session_id=ACTOR),canonical_audit=False,canonical_release_credit=0,release_eligible=False,reviewed_at='2026-11-04',report_generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),assignment_path=str((BASE/'assignment.json').relative_to(ROOT)),assignment_sha256=sha((BASE/'assignment.json').read_bytes()),visible_packet_path=str((BASE/'assigned-visible-input.json').relative_to(ROOT)),visible_packet_sha256=sha((BASE/'assigned-visible-input.json').read_bytes()),question_hashes=assignment['question_hashes'],methodology=context,style_profile={k:read(ROOT/'data/exam_style/mpje_style_profile.json')[k] for k in ['profile_id','content_version','content_hash']},blueprint_snapshot={k:read(ROOT/'data/blueprint.json')[k] for k in ['blueprint_id','content_version','content_hash']},sources=list(sources.values()),retrieval_attempts=retrievals,independence_ko='실제 actor/session을 하나의 stable instance로 기록했다. 원문·보기·키·보이는 한국어 해설을 먼저 full read하고 공식 current primary를 직접 조회했다. 원본은 프로그램에서 locator/family metadata만 projection했으며 hidden statement truth, author/independent report, ledger prior verdict를 모델에 출력하지 않았다. canonical/public 비교도 stem/choices/family만 projection했다. 질문·저장키·공유원장·생성물은 변경하지 않는다.',scope_limits_ko=['eCFR 표시 current-through는 2026-11-02다. 실제 조회 2026-11-04와 혼동하지 않는다. 별도 commencement 미확정 조항은 UNKNOWN이다.','NABP 공개 sample·format·competency 원문의 403을 확인 완료로 바꾸지 않았다. 해당 criterion은 null/NOT_ASSESSED이므로 realism PASS는 없다.','Firecrawl는 크레딧 부족으로 실행되지 않았다. proxy와 TLS 검증을 유지한 urllib 직접 공식 조회를 사용했다.','HTTP 200 GovInfo Page Not Found는 문서 identity 실패이며 APA legal authority로 사용하지 않았다.','순수 독립 legacy 단계다. canonical audit admission, canonical RELEASED credit 또는 완전한 release check가 아니다.','nearest cosine은 후보 검색만을 위한 것이며 semantic 판정은 실제 읽은 원문·법적 결정과 현재 default 제외 맥락을 따로 평가했다.'],duplicate_method=dict(canonical_count=nearest['canonical_count'],public_count=nearest['public_count'],candidate_visible_records_read=len(nearest['visible_candidates']),assigned_default_ids=nearest['assigned_default_ids'],method=nearest['method'],evidence_path=str((BASE/'nearest-visible.json').relative_to(ROOT)),evidence_sha256=sha((BASE/'nearest-visible.json').read_bytes())),records=records,summary=dict(records=len(records),legal_existing_answer_correct=dict(collections.Counter(r['legal_review']['existing_answer_correct'] for r in records)),legal_verdicts=dict(collections.Counter(r['legal_review']['verdict'] for r in records)),realism_verdicts=dict(collections.Counter(r['realism_review']['verdict'] for r in records)),dispositions=dict(collections.Counter(r['disposition'] for r in records)),canonical_release_credit=0,release_eligible=False),checks_not_run=['canonical release admission','shared queue submission/integration','full repository QA and live notes builder/source guard','protected or commercial exam comparison'])
output=ROOT/'reports/full-corpus-review/independent-phase12-c-review.json';output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(report=str(output.relative_to(ROOT)),report_sha256=sha(output.read_bytes()),summary=report['summary']),ensure_ascii=False))
