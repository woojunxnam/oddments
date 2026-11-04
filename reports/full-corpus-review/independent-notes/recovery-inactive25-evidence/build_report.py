from pathlib import Path
import json,hashlib,copy
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[4];BASE=Path(__file__).resolve().parent
REL=BASE.relative_to(ROOT)
def read(p):return json.loads((ROOT/p).read_bytes())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
job=read(REL/'assignment.json');candidate=read('reports/full-corpus-review/body-corrections/w3-a-3-v1/inactive-preview.json');census=read(job['unit_bindings']['w3-a-3']['census_path'])
assert job['actor_provenance']==dict(actor_id='/root/recover_inactive25_review',session_id='/root/recover_inactive25_review')
findings=[
'§21 compounding paragraph는 Board 면허 약국이 compounded, made 또는 formulated한 모든 drug preparation의 container에 sterile 또는 non-sterile compounded 표시를 요구한다. 제조사 제품을 자동으로 compounded로 취급하는 명제는 아니다.',
'§21 마지막 paragraph는 §§39G–39I 면허 sterile/complex non-sterile pharmacy의 환자records 접근 가능한 employed pharmacist와 연락하는 번호를 요구한다. 모든 소매약국에 이 추가 의무를 확장하지 않는다.',
'§21은 전화번호를 drug container의 compounded 표시 옆에 affix하도록 명시한다. 내부 전산기록이나 별도 안내만으로 용기 부착을 대체하지 않는다.',
'§21 전화는 regular hours of operation 동안 every day staffed되어야 한다. 주간 최소시간과 매일 조건을 함께 유지한다.',
'§21의 not less than56hours per week는 최소56시간이다. 전화 staffing 요건이며 최대 영업시간 규정으로 해석하지 않는다.',
'§21 마지막 문장은 §39I institutional pharmacy·sterile preparation·동일 hospital admitted inpatient administration이라는 누적 조건에서 그 paragraph만 예외로 한다.',
'예외 문장의 This paragraph는 전화 paragraph를 지칭한다. outpatient이나 다른 병원 환자에 확대하거나 앞 paragraph의 compounded 표시를 전부 없애지 않는다.',
'§21 compounded 표시, §39D(a) BUD 정의(조제 시점부터 판단), Policy2023-01 II9(d)/247CMR9.08(5)(d)의 packaging BUD와 원 manufacturer expiration은 다른 정보다. 실제 모든 USP 기술기간을 확인한 결과로 확대하지 않는다.',
'§21 large-print paragraph는 elderly(19A14 참조) 또는 visually impaired의 요청에 directions print-size 조건을 둔다. 용어승계에 대한011HOLD는 그대로이며 권리 전체를 부정하지 않는다.',
'현재 공식 §19A14의 Older adult 정의는 individual who is sixty years of age or over이다. 정의 자체를 확인했지만 elderly cross-reference 승계까지 완료했다는 판단은 아니다.',
'실제 §21은 elderly라고 참조하고 현재 §19A14는 Older adult로 게시돼 있다. 두 조문과60세 정의를 새로 읽었으나 변경·승계의 명시적 근거를 이번 범위에서 완결하지 못했다. 원011 finding/blocker와 두 원보고서SHA를 그대로 상속한다.',
'§21 directions는 no more than ten characters per inch이다. 요청 대상과 단위를 유지하며10자를 넘는 인쇄를 허용하는 것으로 읽지 않는다.',
'characters-per-inch와 typographic point는 서로 다른 측정이다. §21은10-point라고 규정하지 않으므로10-point 사용만으로 자동 충족을 주장할 수 없다.',
'§290.5 전문은 federal ScheduleII/III/IV drug를 patient에게 또는 patient를 위해 dispensed할 때 warning을 요구한다. 같은 전문의 blind clinical-investigation 예외도 확인·보존한다. 본문의 해당 patient label은 이 범위로 읽는다.',
'§290.5의 경고 문구는 this drug를 처방받은 환자 이외의 person에게 transfer하는 행위다. 처방정보의 pharmacy간 이전과 객체가 다르다.',
'§1306.08(e)–(i)는 전자처방 initial dispensing transfer, §1306.25는 III–V refill prescription-information transfer를 각각 별도 조건하에 허용한다. 둘 다 State-law 한계를 보존한다. 경고만으로 모든 합법적 약국간 이전을 금지하지 않는다.',
'§290.5는 연방II/III/IV를 열거한다. MA ScheduleVI 분류라는 사실 하나로 연방 경고 의무를 모든VI medicine에 확대할 수 없다.',
'§21 pamphlet paragraph는 Department의 자료 생산·배포와 pharmacist의 명시된 dispensing-trigger 배포를 규정한다. narcotic/opiate 정보 주제와 pharmacist 실제 배포 범위를 구별한다.',
'새 본문과019는 공식 §21의 a narcotic or controlled substance contained in schedule II or III를 그대로 제시한다. 원 opioid/narcotic-only 축소와 실제 수정span을 대조했고 이 literal trigger 주장은 지지된다. 모든IV narcotic의 문법적 범위는 이 판단으로 확정하지 않는다.',
'§21 pamphlet proviso(1)는 c111§227에 따른 outpatient palliative care를 예외로 명시한다. 단순 outpatient 전체로 넓히지 않는다.',
'§21 pamphlet proviso(2)는 long-term care facility resident를 예외로 명시한다. 병원·시설 전체에 일반화하지 않는다.',
'§21 pamphlet proviso(3)는 substance use disorder 또는 opioid dependence 치료를 위해 처방된 경우다. 약 이름만으로 처방목적 조건을 생략하지 않는다.',
'§21의 the pamphlet은 Department가 지정한 주제를 포함하여 produce/distribute하는 선행 자료를 가리킨다. 일반 pharmacy leaflet이라는 사실만으로 해당 요건이 자동 충족됐다고 단정할 수 없다.',
'실제 §21은 controlled substance contained in schedule II or III를 포함한다. 새024의 non-opioid라는 이유만으로II/III를 제외하지 않는다는 좁은 주장은 이 문언으로 지지된다. 실제 예외(1)–(3)와 원019HOLD 이력은 보존하며 전체schedule/setting 의무로 확대하지 않는다.',
'§39D(a) compounding은 packaging/labeling을 포함할 수 있지만 active ingredient·other substances·licensed pharmacist/pharmacy·최종 preparation·(1)–(3)와 상업용 FDA승인제품 제외 및(1) 예외를 함께 읽어야 한다. Policy2023-01 II8/9는 compliance packaging과 prescription에 따른 compounding 및 labeling을 구별한다. 그러므로 용기 변경 하나만으로 모든 법적 분류가 동일하다고 단정하지 않는 한정 명제는 지지되며 모든repackaging 면제는 아니다.'
]
sections={
'mgl94c21':'M.G.L. c.94C §21, large-print paragraph, educational-pamphlet paragraph and proviso(1)–(3), compounding paragraph and final telephone paragraph',
'mgl19a14':'M.G.L. c.19A §14 introductory scope and Older adult definition',
'mgl11239d':'M.G.L. c.112 §39D(a), Beyond-use date and Compounding definitions including clauses(1)–(3) and final commercial/FDA-approved exclusion',
'cfr2905':'21 CFR §290.5 complete warning and blind clinical-investigation exception',
'cfr130608':'21 CFR §1306.08(e)–(i), electronic initial dispensing transfer with State-law limitation',
'cfr130625':'21 CFR §1306.25(a)–(e), pharmacy refill prescription-information transfer with State-law limitation',
'policy2023-01':'Board Policy2023-01 II introductory paragraph and II(8)–(9), especially II(9)(d)',
'cmr9':'247 CMR 9.08(5)(a)–(e), especially (5)(d) packaging BUD',
'act2025c16':'Acts2025 chapter16 §7 and §27 (label-name exception effective2026-01-01)'}
def authority(key):
 mp=REL/(key+'.meta.json');m=read(mp);raw=REL/m['raw_path'];text=REL/m['text_path']
 assert sha(raw)==m['raw_sha256'] and sha(text)==m['text_sha256'] and m['http_status']==200
 return dict(source_type='PUBLIC_OFFICIAL',official_url=m['official_url'],exact_section=sections[key],law_checked_date=m['read_at_utc'][:10],version_or_effective_date_status=('Policy printed adopted2023-04-06; revised2023-11-02 and2025-01-09; separate commencement UNKNOWN; retrieval date is not effective date.' if key=='policy2023-01' else m['version_or_effective_date_status']),evidence_path=str(raw),evidence_sha256=sha(raw),extracted_text_path=str(text),extracted_text_sha256=sha(text),retrieval_metadata_path=str(mp),retrieval_metadata_sha256=sha(mp),source_retrieval=dict(mode='LIVE',http_status=200,transport=m['transport'],document_identity_status=m['document_identity_status'],raw_sha256=sha(raw),retrieved_at_utc=m['retrieved_at_utc'],read_at_utc=m['read_at_utc']))
claims=[]
for i,c in enumerate(census['claims'],1):
 keys=(['mgl94c21'] if i<=9 or 12<=i<=13 or 18<=i<=24 else ['mgl19a14'] if i==10 else ['mgl94c21','mgl19a14'] if i==11 else ['cfr2905'] if i in [14,15,17] else ['cfr2905','cfr130608','cfr130625'] if i==16 else ['mgl11239d','policy2023-01'])
 if i==8:keys=['mgl94c21','mgl11239d','policy2023-01','cmr9']
 row=dict(claim_id=c['claim_id'],claim_record_sha256=job['unit_bindings']['w3-a-3']['claim_record_sha256s'][c['claim_id']],claim_read_completely=True,statement_ko=c['statement_ko'],legal_status='LEGAL_HOLD' if i==11 else 'KEEP',finding=findings[i-1],blocker='두 게시조문 용어 변경의 명시적 승계/적용 관계 추가 확인 필요. 이 한계를 전체 요청자 권리 부정으로 해석하지 않는다.' if i==11 else None,authorities=[authority(k) for k in keys])
 if i==11:row['inherited_legal_blockers']=copy.deepcopy(job['carried_legal_blockers']['w3-a-3'][c['claim_id']])
 claims.append(row)
now=datetime.now(timezone.utc).isoformat()
unit=dict(unit_id='w3-a-3',binding=copy.deepcopy(job['unit_bindings']['w3-a-3']),body_read_completely=True,actual_body_sha256=hashlib.sha256(candidate['unit']['body'].encode()).hexdigest(),reviewed_at=now,completeness='COMPLETE',completeness_method='실제 비활성N1 본문 각문장과 최종25 atom을 양방향 대조했다. Compounded표시·전화/시간/예외, BUD분리, 별도classification한정 ADD001, large-print 단위, drug-warning/처방정보transfer구별, 지정pamphlet trigger/예외를 열거와 대조했다. Week4 링크는 외부전체내용을 이절 법규로 인증하지 않는 편집범위다. C31이 지적한 단순용기변경 classification 문장이ADD001에 원문 그대로 존재하며 원24 object와42source 보존을 실제 비교했다. 관련35원문·보기·저장key·해설과 derived2를 실제 읽었다. No omissions found in the reviewed body/census; completeness is not legal pass.',omissions=[],legal_status='LEGAL_HOLD',claims=claims,inactive_census_successor_review={**copy.deepcopy(job['inactive_census_successor_review']),**{k:True for k in ['final_candidate_body_read_completely','final_census_read_completely','all_original_omissions_reassessed','all_original_propositions_preserved','all_derived_inputs_read_completely','no_current_credit_before_matching_active_binding']}},original_omission_reassessments=[dict(omission_sha256=x['raw_sha256'],decision='RESOLVED_BY_FRESH_COMPLETE_BODY_CENSUS_REVIEW',finding='원 omission의 제조사제품 단순용기변경 classification한정이 ADD001에 정확히 열거됐다. 008 BUD/expiry구분으로 뭉뚱그리지 않고 별도atom로 전문과 대조했다. §39D(a)와 Policy2023-01을 새 실제세션에서 직접 검토했다. 다른24원명제/42source/011HOLD는 그대로이며 N1미활성이라 현재credit0이다.') for x in job['inactive_census_successor_review']['parent_omissions']])
related=read(REL/'related-question-input.json')
report=dict(schema_version='independent-inactive25-recovery-review/1',stage='independent-notes',independent_of_authors=True,actor_provenance=copy.deepcopy(job['actor_provenance']),auditor=job['auditor'],auditor_instance=job['auditor_instance'],canonical_audit=False,canonical_release_credit=0,question_audit_credit=0,reviewed_at=now,records=[unit],sources=[authority(k) for k in sections],summary=dict(unit_completeness='COMPLETE',unit_legal_status='LEGAL_HOLD',claim_keep=24,claim_legal_hold=1,current_coverage_credit=0,body_activated=False),execution_provenance=dict(previous_workspace_material_lost=True,previous_B_draft_not_reused=True,actual_new_session='/root/recover_inactive25_review',preassignment_reading='Substantive read and live primary retrieval began before controller attempt2 claim; actual attempt2 now binds the exact same N1/E25 bytes. No past claim or reading timestamps invented.'),related_question_review=dict(input_path=str(REL/'related-question-input.json'),input_sha256=sha(REL/'related-question-input.json'),question_count=len(related),all_stems_choices_keys_and_explanations_read=True,records=[dict(question_id=x['question_id'],record_sha256=x['record_sha256'],read_scope='Complete stem/all choices/stored key/Korean explanation for note alignment',finding='large-print 단위, compounded표시/BUD, patient-drug-warning/약국간정보이전 구별을 노트범위와 대조했다. generic/biologic·shield·기타 교환요건은 이 노트감사의 whole-key legal판정 대상이 아니며 새question credit0이다.',whole_key_new_independent_credit=0) for x in related]),derived_input_review=dict(path='reports/full-corpus-review/body-corrections/w3-a-3-v1/derived-preview.json',raw_sha256=sha('reports/full-corpus-review/body-corrections/w3-a-3-v1/derived-preview.json'),all_two_items_read_completely=True,finding='LAW-037의 처방/내부기록/patient-label 역할 분리와 chapter overview의 실제 제품/legal equivalence는 N1의 pamphlet수정이나classification한정과 충돌하지 않는다. 본문binding만 후보hash로 바뀌며 text는 불변.011HOLD 및 daily제외는 해제하지 않는다.'),limitations_ko=['실제 N1은 미활성이다. COMPLETE/24KEEP는011HOLD나 별도16보호·fullQA·CI·공개검증을 대체하지 않는다.','공식문서 target provisions를 실제 읽었으며 모든문서의 전체 개정효력일계보를 새로 재구성하지 않았다. UNKNOWN한계를 authority에 명시했다.','관련문항35를 읽었지만 이25명제 밖의 generic/biologic 등 모든선택지법규를 새로 전수판정하지 않았다. question/canonical/release credit0.','§21 pamphlet 문언과 II/III non-opioid 제외불가만 판단하며 모든IV narcotic문법범위를 확정하지 않는다.','USP private/protected 전체자료를 취득하지 않았다. public정책/법규와 다르게 USP 상세전수PASS를 주장하지 않는다.'])
path=Path('reports/full-corpus-review/independent-notes/recovery-inactive25-review.json');(ROOT/path).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(path,sha(path))
