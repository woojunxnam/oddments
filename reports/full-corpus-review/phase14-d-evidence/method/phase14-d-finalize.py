import json,hashlib
from pathlib import Path
root=Path('/workspace/independent-wave14-d');p=root/'reports/full-corpus-review/independent-phase14-d-review.json';r=json.load(open(p));nearpath=root/'reports/full-corpus-review/phase14-d-evidence/nearest-visible-comparison.json';near=json.load(open(nearpath));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
comparisons={
'MA-Q-0331':'Canonical은 eligible medication의 SC/IM 투여경로를 묻고 본 문항은 IND/ANDA/NDA의 승인 단계·범위를 묻는다. Route라는 어휘는 공유하지만 같은 법적 결정은 아니다.',
'MA-Q-0430':'Canonical은 NDC가 없을 때 generic product 기록의 repacker fallback을 묻는다. 승인증거 또는 nuclear 자격·예외기한과는 다른 의무다.',
'MA-Q-0121':'Canonical은 excepted preparation의 신원·판매량·기록 조건이다. 한정 예외에도 조건이 남는 구조는 공유하지만 DSCSA 면제와 법률·거래 사실이 다르다.',
'MA-Q-0177':'Canonical은 EPT 익명 partner의 별도 profile/label이다. 공급망 거래자료와 공급자 자격·6년 보존은 대상·기록 목적이 다르다.',
'MA-Q-0330':'Canonical은 주사제 administration notation 누락에서 encouraged prescriber contact의 강도를 묻는다. DSCSA 면제나 suspect 조사와 다른 의무이다.',
'MA-Q-0058':'Canonical은 controlled-substance loss의 DEA one-business-day notice/45-calendar-day Form106을 구별한다. 조사완료를 기다리지 않는 구조는 공유하지만 DSCSA illegitimate24시간은 다른 기관·trigger이다.',
'MA-Q-0091':'Canonical은 ClassII lot-specific recall에서 affected/unaffected lot과 환자 추적 행동을 선택한다. 본 family는 법적 recall/stock recovery 또는 분류 전 notice/ClassIII의 범위를 묻는다. 추적·이행 주제는 겹치지만 결정적인 사례 조건이 다르다.',
'MA-Q-0375':'Canonical은 generic product의 NDC 부재 시 manufacturer 우선 fallback이다. Nuclear 자격·환자정보·기록·calibration과는 직접 같은 판단이 아니다.',
'MA-Q-0103':'Canonical은 개인 이름·주소 변경 후 Board14일 업데이트이다. Nuclear의 자격 또는 calibration과는 대상·trigger가 다르다.',
'MA-Q-0175':'Canonical은 Abilify Maintena 투여 후 severe reaction에서 prescriber 즉시통지·administration record를 고른다. 본 family의 QRE/defect 또는 ED serious-injury 범주와 안전 주제를 공유하지만 투여경로·행위·보고 대상이 다르다.',
'MA-Q-0051':'Canonical도 incident log만 있고 원인분석·예방이 없다는 상황에서 complete CQI를 고른다. 본 문항 CaseA와 핵심 판단이 실질적으로 겹치고 CaseB를 추가해도 A만 고르는 결정을 충분히 바꾸지 못한다.',
'MA-Q-0054':'Canonical은 repeated selection errors에서 시스템 원인분석을 생략한 상황이다. 본 문항 CaseB는 이미 변경한 뒤 시행·효과를 검증하지 않은 후속 단계여서 원인분석과 목적은 연결되어도 결정 단계가 다르다.',
'MA-Q-0055':'Canonical은 18개월 교육공백에 연례 CQI 교육을 적용한다. 본 문항은 비난 위주의 분석을 INCORRECT로 찾으며 연례교육은 부가 참 명제라 핵심 결정이 다르다.',
'MA-Q-0115':'Canonical은 warfarin serious injury 사건에서24시간 QRE와7businessdays Board보고의 서로 다른 trigger를 결합한다. 본 문항들은 별도 문서화/ED정의/5년보존/nonresident 범위를 각각 다루며 같은 규정 일부는 겹친다. 신규 독립 사례로 부풀리지 않으며 현재 default에는 이 archived 변형을 추가하지 않는다.',
'MA-Q-0439':'Canonical은 개업 당일 zero-stock controlled inventory의 작성일을 묻는다. 처음의 기록을 미루지 않는 문장 구조는 비슷하지만 QRE의 환자통지·24시간 기록과 법률·trigger는 다르다.'}
for row in r['records']:
 rr=row['realism_review'];d=rr['duplicate_evidence'];cn=d['canonical_nearest'][0]['question_id'];pn=d['public_nearest'][0]['question_id'];qid=row['question_id']
 note=f'{qid}: canonical439/public2349 전체에서 TF-IDF 후보를 측정했다. Nearest canonical {cn}와 public {pn}의 visible stem·보기·key·해설 전문을 실제 읽었다. '+comparisons[cn]+f' Public {pn}는 같은 두 사례와 네 판단의 family 변형이며 prompt 극성·배열 또는 선택 조합만 바뀐다. 현재 문항과 해당 archived family를 새 독립 사례 수로 세지 않는다. 현재 문항 default 포함은 false이다. Family 변형 존재만으로 자동 FAIL하지 않았다.'
 d['semantic_finding_ko']=note;d['evidence_sha256']=sha(nearpath);rr['criterion_findings_ko']['distinct_from_bank']=note
 if qid=='MA-EXP-0981':
  rr['criteria']['distinct_from_bank']=False;rr['finding_ko']+=' Canonical MA-Q-0051과 CaseA의 핵심 사실·결정도 겹쳐 distinct_from_bank 기준을 추가로 충족하지 못한다.'
 if rr['verdict']=='PASS':
  rr['criterion_findings_ko']['wording_not_guessable']=f'{qid}: 오답은 초기기록/조사완료, 환자통지/내부기록, 일반보존/특별보존 또는 nonresident 조항의 적용을 바꾸어 놓았다. 단순 문장 길이보다 실제 trigger·의무 구별을 해야 정답이 유일해진다.'
  rr['criterion_findings_ko']['natural_rule_combination']+=' 실제 한 사건의 후속업무에 한정되어 보기의 각 의무가 별개로 남는 이유를 판단해야 한다.'
assert all((all(x['realism_review']['criteria'].values()))==(x['realism_review']['verdict']=='PASS') for x in r['records'])
p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
# Keep own implementation as transparent evidence of byte bindings and judgments.
for path in ['/tmp/phase14-d-fetch.py','/tmp/phase14-d-fetch2.py','/tmp/phase14-d-fetch3.py','/tmp/phase14-d-fetch4.py','/tmp/phase14-d-fetch5.py','/tmp/phase14-d-nearest.py','/tmp/phase14-d-build.py','/tmp/phase14-d-report.py','/tmp/phase14-d-finalize.py']:
 target=root/'reports/full-corpus-review/phase14-d-evidence/method'/Path(path).name;target.parent.mkdir(exist_ok=True);target.write_bytes(Path(path).read_bytes())
print('final report',sha(p))
