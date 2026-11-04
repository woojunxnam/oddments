from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
B=Path('reports/full-corpus-review/independent-notes/census-wave5-v2-d-evidence')
P=Path('reports/full-corpus-review/independent-notes/census-wave5-v2-d-review.json')
J=json.load(open('/tmp/census-wave5-v2-d-assignment.json'))
V=json.load(open(B/'assigned-visible-input.json'))
A=json.load(open(B/'claim-assessments.json'))
O=json.load(open(B/'option-assessments.json'))
Q=json.load(open(B/'related-practice-visible-input.json'))['records']
D=json.load(open(B/'practice-lossless-reading.json'))
OLD=json.load(open(B/'reassessment-omission-input.json'))
NOW=datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def digest(o):return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def save(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
SCOPES={
 'cmr9':('247 CMR 9.01(5),(7),(8),(12);9.02(1)–(3);9.13(1)–(3);9.19(12);9.21(8)(c),(9)–(12);9.22(1)–(4)','Mass. Register #1536 2024-12-06의 Mass.gov 현행 공개 compilation. 각 최초 시행일은 이 PDF만으로 모두 특정하지 못함.'),
 'policy2023-01':('Policy 2023-01 I;II.1–10;Single-Drug-Single-Dose;Multi-Drug-Single-Dose;Return and Repackaging 1–3, pp.1–4','Adopted 2023-04-06; revised 2023-11-02 and 2025-01-09. 현행 다운로드 전4쪽 실독. 별도 시행 유예일은 문서에서 확인되지 않음.'),
 'cfr1317':('21 CFR 1317.01;1317.05(a),(c);1317.10;1317.15;1317.30;1317.40;1317.75;1317.85;1317.90','현재 eCFR 본문. 개별 최초 효력일과 모든 과거 amendment 이력은 별도 확정하지 못함. Registrant inventory와 ultimate-user collection의 주체·목적을 구별함.'),
 'cmr15':('247 CMR 15.03(1)–(2)','Mass. Register #1536 2024-12-06의 현행 공개 compilation. 연관 practice의 오류 반환 후 별도 QRE 대응에만 사용. 개별 최초 효력일 미확정.'),
 'cfr1700-14':('16 CFR 1700.14(a)(10), especially (i),(ii),(x)','현재 eCFR prescription oral-drug special-packaging 및 specific exemption 문언. 개별 최초 효력일 미확정. 본문 밖 연관 practice의 narrow local alignment만 검토함.'),
 'cfr1700-15':('16 CFR 1700.15(a)–(b)','현재 eCFR packaging 기능/child-resistant effectiveness 기준. 개별 최초 효력일 미확정. Tamper evidence와 child resistance 구분에만 사용.'),
 'cpsc-pppa':('PPPA business guidance: special packaging definition; prescription request paragraph','검토일의 live CPSC 공식 페이지. 최초 게시/시행일은 페이지에서 확정하지 못함. Current federal eCFR와 15 USC 1473(b)의 적용 설명을 cross-check한 자료.'),
 'cpsc-healthcare':('Poison Prevention Packaging: A Guide for Healthcare Professionals, Jan 2023, Part3 Prescribers/Dispensers FAQ, pp.12–13; tamper-evident FAQ','January 2023 CPSC STAFF guidance. 표지에 Commission reviewed/approved 문서가 아니라고 명시되므로 법 자체와 구별한다. Statutory prescription/purchaser request와 eCFR의 해석 보조이며 독자적 법률로 취급하지 않음.'),
 'cpsc-statute':('15 USC 1473(b), agency-hosted PPPA copy','CPSC PDF 표지는 October 14, 2008 Version이다. 구문 비교용 과거 agency copy이며 현재 법적 결론의 단독 근거로 사용하지 않음. 별도 2024 GPO Code와 live CPSC 설명을 확인함.'),
 'usc1473-govinfo':('15 USC 1473(b); statutory source/editorial notes','U.S. Code 2024 Edition, GPO 공식 발행. Source note Pub.L.91-601 §4 (1970-12-30), 92-573 §30(a) (1972-10-27). 2025/2026 모든 개별 제정법을 전수검색한 것은 아니며 live CPSC current request guidance/2023 staff FAQ 및 current eCFR와 cross-check했다.'),
 'cfr1700-5':('16 CFR 1700.5(a)–(b)','현재 eCFR noncomplying retail-package label 문언, source40FR4650(1975-01-31). Prescription-specific request와 retail noncomplying-size 경로를 혼동하지 않는 context 확인에만 사용. 최초 효력일 미확정.')
}
sources={}
for f in sorted(B.glob('*-retrieval.json')):
 m=json.load(open(f));sid=m['source_id'];ok=sid in SCOPES and m['http_status']==200
 m.update(read_at=NOW if ok else None,read_completed_at=NOW if ok else None,document_identity_confirmed=ok,legal_payload_confirmed=ok,actual_read_scope=SCOPES[sid][0] if ok else '404 error body; 법률 증거 아님',version_or_effective_date_status=SCOPES[sid][1] if ok else 'HTTP404; 법적 증거로 사용하지 않음',retrieval_semantics='이번 실제 session에서 verified-TLS network request로 수신한 바이트. 원 server가 proxy/cache를 사용했을 가능성과 origin freshness는 response headers 이상으로 단정하지 않는다. 타 reviewer cache를 복사한 재독이 아니다.')
 save(f,m);memo=B/(sid+'-read-memo.json');save(memo,{'source_id':sid,'read_completed_at':m['read_at'],'scope':m['actual_read_scope'],'version_or_effective_date_status':m['version_or_effective_date_status'],'raw_path':m['raw_path'],'raw_sha256':m['raw_sha256'],'extracted_path':m['text_evidence_path'],'extracted_sha256':m['text_sha256'],'legal_payload_confirmed':ok,'limitation':'지정한 실제 읽은 section의 관련 명제만 검증했으며 문서의 다른 모든 조문을 판정했다는 주장이 아니다.'})
 sources[sid]={**m,'source_type':'PUBLIC_OFFICIAL','metadata_path':str(f),'metadata_sha256':sha(f),'memo_path':str(memo),'memo_sha256':sha(memo),'relied_on_for_current_authorities':ok and sid not in {'cpsc-statute','cfr1700-5'}}
def auth(sid,section):
 s=sources[sid];assert s['legal_payload_confirmed'] and s['http_status']==200
 if sid=='cmr9' and not section.startswith('247'):section='247 CMR '+section
 if sid=='cmr15' and not section.startswith('247'):section='247 CMR '+section
 if sid=='policy2023-01' and not section.startswith('Policy'):section='Policy 2023-01 '+section
 return {'source_id':sid,'source_type':'PUBLIC_OFFICIAL','official_url':s['official_url'],'citation_url':s['final_url'],'exact_section':section,'law_checked_date':NOW[:10],'version_or_effective_date_status':s['version_or_effective_date_status'],'retrieved_at':s['retrieved_at'],'read_at':s['read_at'],'timezone':'Etc/UTC','http_status':s['http_status'],'evidence_path':s['raw_path'],'evidence_sha256':s['raw_sha256'],'text_evidence_path':s['text_evidence_path'],'text_evidence_sha256':s['text_sha256'],'retrieval_metadata_path':s['metadata_path'],'retrieval_metadata_sha256':s['metadata_sha256'],'read_memo_path':s['memo_path'],'read_memo_sha256':s['memo_sha256']}

binding=J['unit_bindings']['return-pathways'];final=json.load(open(binding['census_path']))
assert sha(binding['census_path'])==binding['census_sha256']
assert {c['claim_id']:digest(c) for c in final['claims']}==binding['claim_record_sha256s']
assert digest(next(x for x in final['units'] if x['unit_id']=='return-pathways'))==binding['census_unit_record_sha256']
assert hashlib.sha256(V['body'].encode()).hexdigest()==binding['body_sha256']
assert len(A)==len(V['claims'])==29
claims=[]
for n,(c,(sid,section,finding)) in enumerate(zip(V['claims'],A),1):
 cid=c['claim_id'];inherited=J.get('carried_legal_blockers',{}).get('return-pathways',{}).get(cid,[])
 assert not inherited,'No inherited legal blocker in this exact assignment; do not silently overwrite if changed'
 authorities=[auth(sid,section)]
 if n==13:authorities.append(auth('cmr9','247 CMR 9.19(12);9.21(9)–(10)'))
 if n==26:authorities.append(auth('cmr9','247 CMR 9.01(12);9.13(1)(b)4'))
 claims.append({'claim_id':cid,'claim_record_sha256':binding['claim_record_sha256s'][cid],'statement_ko':c['statement_ko'],'claim_read_completely':True,'read_completed_at':NOW,'legal_status':'KEEP','finding':finding,'authorities':authorities,'author_census_review_status_preserved':c['review_status'],'author_source_blocked_history_preserved':cid in binding['source_blocked_claim_ids'],'inherited_legal_blockers':inherited,'history_distinction':'Assignment의 actual prior independent carried_legal_blockers는 빈 object이다. Author SOURCE_BLOCKED 이력은 원 객체를 고치지 않고 이 필드에 남긴다. 현재 KEEP는 새 공식 primary로 확인한 이 명제의 한정 범위에 대한 판단이다.','question_audit_credit':0})

omission='CRP-D-NEW-O1: 정확 본문 구절 “필요한 label과 removable cell 표시를 다시 합니다.” 중, 반환된 동일 환자 package의 실제 변경 약물 내용에 맞춰 필요한 일반 package label을 다시 하는 명제가 최종 census29에 별도로 열거되어 있지 않다. Claim025는 removable cell의 name/strength 재표시에 한정되고 claim010은 재포장 경로,023은 변경 기록,024는 pharmacist 식별,027은 controlled-substance security/accountability이다. 일반 package label과 개별 removable-cell label은 Policy2023-01 II.9(a)–(e) 및 Return and Repackaging1(c)에서 구별되므로 일반 label 갱신 명제를 추가로 열거해야 한다.'
coverage=[
 ('준비했지만 교부하지 않은 처방',[1]),('Manufacturer stock bottle에 되붓지 않음',[2]),('환자에게 잘못 교부했거나 defective/contaminated 의심',[3,4]),('수령·격리·적법 폐기',[5,6]),('일반 판매 재고로 복귀 금지',[7]),('일반적으로 수령 의무 없음',[8]),('단순 재판매 허가가 아님',[9]),('같은 환자를 위한 재포장·재교부',[10]),('다른 환자나 general stock',[11,12]),('Recall·reverse distribution·collection',[13]),('원 patient container 또는 적합한 별도 용기',[14]),('product name',[15]),('strength/concentration',[16]),('manufacturer/supplier 또는 NDC',[17]),('처음 filling 때 부여한 expiration',[18]),('P&P를 유지',[19]),('해당 lot가 아니라는 것을 확인하기 전',[20]),('discontinued drug를 제거',[21]),('새 therapy를 반영',[22]),('수량·제거·재교부를 추적',[23]),('변경한 pharmacist',[24]),('removable cell 표시',[25]),('새 포장일이 기존 expiry·안정성 기한을 연장하지',[26]),('control accountability',[27]),('실제 storage',[28]),('integrity',[29])]
bodycoverage=[]
for phrase,ns in coverage:
 assert phrase in V['body'],phrase
 bodycoverage.append({'exact_body_phrase':phrase,'claim_ids':[V['claims'][n-1]['claim_id'] for n in ns]})
resolution=[]
for old in OLD['omissions']:
 h=hashlib.sha256(old.encode()).hexdigest();r=next(x for x in J['reassessment_review']['omission_resolutions'] if x['omission_sha256']==h);is_storage='CRP-O1:' in old
 resolution.append({'original_omission':old,'omission_sha256':h,'mapped_claim_ids':r['claim_ids'],'independent_resolution':'RESOLVED_FOR_ORIGINAL_ASSERTION','finding':'신규 ADD-001은 on-duty pharmacist의 proper preservation/storage와 applicable refrigerated/frozen temperature 조건을 직접 열거한다. 이 물리·환경적 보관 의무는 027의 security/accountability와 다른 proposition이며 원래 storage 누락을 해결한다. 모든 약이 냉장 대상이라는 주장이나 새로운 반환 허가로 확대하지 않았다.' if is_storage else '신규 ADD-002는 actual product integrity와 applicable temperature excursion의 integrity assessment를 직접 열거한다. 이는 026의 expiry automatic extension 및 027의 수량/보안 accountability와 다른 품질 proposition이며 원래 integrity 누락을 해결한다.','authorities':[auth('cmr9','247 CMR 9.01(8);9.22(1)' if is_storage else '247 CMR 9.01(12);9.22(1)')]})

local=[];byid={r['question_id']:r for r in D['records']}
for q in Q:
 r=byid[q['question_id']];optrows=[];supported=[]
 for oid,token in r['choices'].items():
  truth,sid,section,finding=O[token[1:]]
  if truth:supported.append(oid)
  aa=[auth(sid,section)]
  if int(token[1:]) in {51,52,56,58}:aa.append(auth('cpsc-healthcare','Part3 Prescribers/Dispensers FAQ: specific patient request; physician standing order, pp.12–13 (staff guidance)'))
  if int(token[1:]) in {55,66}:aa.append(auth('cpsc-healthcare','Part3 FAQ: tamper-evident packaging vs special packaging (staff guidance)'))
  optrows.append({'option_id':oid,'exact_text_token':token,'supported_as_written':truth,'finding':finding,'authorities':aa,'original_ko_distractor_rationale_read':True,'original_ko_explanation_alignment':'CONSISTENT_WITH_SCOPED_PRIMARY_FINDING'})
 incorrect='INCORRECT' in q['stem'];selected=[oid for oid in r['choices'] if oid not in supported] if incorrect else supported
 assert sorted(selected)==sorted(q['correct_choice_ids']),(q['question_id'],selected,q['correct_choice_ids'])
 local.append({'question_id':q['question_id'],'current_record_sha256':q['record_sha256'],'input_path':str(B/'related-practice-visible-input.json'),'input_sha256':sha(B/'related-practice-visible-input.json'),'full_english_stem_read':True,'all_choices_read':True,'stored_key_read':True,'ko_core_and_all_distractors_read':True,'read_completed_at':NOW,'stored_key':q['correct_choice_ids'],'question_type':q['question_type'],'polarity':'INCORRECT' if incorrect else 'SUPPORTED','lossless_stem_token':r['stem'],'lossless_ko_core_token':r['core'],'local_answer_combination_matches_stored_key':True,'options':optrows,'note_alignment':'검토한 반환·RTS·same-patient repackaging·expiry·storage/integrity 명제와 모순되는 정답 또는 KO 해설은 찾지 못했다. 일반 package label을 바꿔야 한다는 관련 문항의 진술은 본문에도 있으나 final census의 별도 누락으로 남긴다.','realism_local_observation':'동일 family의 paired-case/polarity 변형 또는 separate-work-queue 보기 조합이 반복된다. 명백한 always/every/automatically 오류와 긍정된 올바른 업무 진술이 정답 단서를 줄 수 있다. 단일 실제 환자 사례의 신규 법규 credit로 세지 않는다.','scope_limit':'CASE stem의 Schedule VI 전제는 연방 controlled-drug multi-drug conflict를 판정하지 않는 문맥으로 읽었다. Schedule VI가 Massachusetts의 controlled substance 범위에서 제외된다는 결론은 내리지 않는다.','local_alignment_only':True,'canonical_audit':False,'canonical_release_credit':0,'question_audit_credit':0})

row={'unit_id':'return-pathways','title':V['title'],'binding':binding,'body_read_completely':True,'body_read_completed_at':NOW,'visible_input_path':str(B/'assigned-visible-input.json'),'visible_input_sha256':sha(B/'assigned-visible-input.json'),'completeness':'OMISSIONS_FOUND','omissions':[omission],'completeness_method':'원 body의 표 전5행 및 RTS/재포장 전 문장을 실제 읽고, 수령 주체·이미 교부 여부·same patient·용기/식별/expiry·기록·label·물리적 storage/integrity와 보안/accountability를 29개 명제에 각각 대응했다. Hash로 원27개의 무변경과 새2개 추가를 확인했다. 재평가가 요구하는 원 reviewer의 exact omission 두 문자열만 의도적으로 읽었으며 이전 법적 verdict/finding는 재사용하지 않았다. 새 두 atom이 원 storage/integrity 누락을 해결하는지 다시 판단한 뒤, 일반 package label과 removable-cell label을 구별하는 추가 미열거 명제를 발견했다.','body_assertion_coverage':bodycoverage,'omission_evidence':[{'exact_body_phrase':'필요한 label과 removable cell 표시를 다시 합니다.','unlisted_proposition':'수정한 실제 medication 내용에 맞춰 필요한 일반 package label을 다시 표시한다.','closest_census_claim_id':'NOTE-WAVE3-RETURN-PATHWAYS-025','difference':'Claim025는 removable cell의 drug name/strength 재표시에 한정된다. 일반 package 표시 정보는 별도이다.','authorities':[auth('policy2023-01','II.9(a)–(e);II.10;Return and Repackaging1(a)–(c), pp.2–3')]}],'claims':claims,'legal_status':'LEGAL_HOLD','reassessment_review':{**J['reassessment_review'],'final_census_read_completely':True,'all_original_omissions_reassessed':True,'all_original_propositions_preserved':True},'original_omission_resolution_assessments':resolution,'carried_legal_blockers_exact':J['carried_legal_blockers']['return-pathways'],'author_source_blocked_claim_ids_preserved':binding['source_blocked_claim_ids'],'required_followup':['본문은 변경하지 말고, 일반 package label을 실제 변경 약물 내용에 맞춰 갱신한다는 별도 atom을 다음 census 보완본에 열거하고 fresh nonauthor completeness 재평가를 받을 것.','원27개 명제/기존 저자 SB 이력과 본 보고서의 추가 omission을 보존할 것.','본 검토는 제품별 새 BUD나 Schedule II–V returned medication receipt의 포괄 허가를 승인하지 않는다.'],'canonical_audit':False,'canonical_release_credit':0,'question_audit_credit':0}
save(B/'source-index.json',{'created_at':NOW,'timezone':'Etc/UTC','sources':sources,'failed_retrievals_not_legal_evidence':['usc1473'],'historical_context_only':['cpsc-statute'],'context_only':['cfr1700-5']})
report={'schema_version':1,'stage':'independent-notes','job_id':J['job_id'],'assignment_sequence':J['sequence'],'assignment_sha256':sha('/tmp/census-wave5-v2-d-assignment.json'),'assignment_base_commit':J['base_commit'],'reassessment_id':J['reassessment_id'],'actor_provenance':J['actor_provenance'],'auditor':J['auditor'],'auditor_instance':J['auditor_instance'],'independent_of_authors':True,'canonical_audit':False,'canonical_release_credit':0,'question_audit_credit':0,'review_date':NOW[:10],'review_completed_at':NOW,'timezone':'Etc/UTC','scope':'Census-only return-pathways final29 exhaustive independent reassessment. 원27 hashes 무변경, 새storage/integrity2개 검증, 원2개 omission 재검토 및 추가 본문 미열거 탐색. Related42 question local alignment only.','independence_disclosure':{'stable_actual_instance_continued':True,'new_identity_or_session_claimed':False,'actor_is_not_G_author_or_original_C32_reviewer':True,'author_or_editor_of_assigned_body_or_census':False,'previous_complete_atomic_assessor_of_this_unit':False,'authorized_prior_input':'Census-only runbook에 따라 원 C32 report에서 대상 unit의 omission 두 문자열만 SHA-bound 추출해 읽었다. 그것은 재평가 범위 입력이며 이전 claim legal_status/finding/blocker를 열람하거나 판단 근거로 복사하지 않았다. Assignment carried_legal_blockers exact object는 {}이다.','author_sb_history':'원 author SOURCE_BLOCKED 013/026은 원 census 바이트와 각각의 claim history 필드에 유지했다. 이번 새 primary가 지지하는 generic route distinction/no-automatic-extension 범위와 별도이며 특정 거래/제품의 전면 허가로 확대하지 않는다.','earlier_session_incident':'앞선 D40 단계에서 URL discovery rg가 무관한 author verification_notes 일부를 출력한 사건은 root와 당시 보고서에 공개했다. 이번 return-pathways hidden truth/타 reviewer 법적 결론을 재사용하지 않았고 같은 actual instance를 유지한다.','new_credit_limits':'Unit은 추가 omission 때문에 LEGAL_HOLD이며 canonical release/question credit0. 원2개 omission 해소만으로 COMPLETE를 만들지 않음.'},'source_boundaries':'정부 공식 MA/eCFR/GPO/CPSC primary 및 명시한 staff guidance만 취득했다. Commercial/PreMPJE/recalled/protected exam/NABP/USP raw/text ingestion0. 정부 정책의 USP 참조 문구를 보았으나 USP 원문은 취득하지 않았다.','input_binding_checks':{'body_sha256_matches_assignment':True,'new_census_raw_sha256_matches_assignment':True,'new_census_unit_record_sha256_matches_assignment':True,'all29_claim_record_sha256s_match_assignment':True,'original27_claim_hashes_preserved_exactly':OLD['original_27_claim_hashes_unchanged'],'new_census_is_assignment_authority_over_any_older_base_ledger_selection':True},'source_index_path':str(B/'source-index.json'),'source_index_sha256':sha(B/'source-index.json'),'sources':list(sources.values()),'records':[row],'related_practice_alignment':local,'counts':{'units':1,'claims':29,'claim_keep':29,'claim_legal_hold':0,'claim_source_blocked':0,'author_source_blocked_history_preserved':2,'inherited_independent_legal_blockers':0,'original_omissions_reassessed':2,'original_omissions_resolved':2,'new_omissions_found':1,'completeness_complete':0,'completeness_omissions_found':1,'unit_legal_hold':1,'related_questions_read':42,'local_options_read':sum(len(x['options']) for x in local),'new_question_audit_credit':0},'next_actions':row['required_followup']}
save(P,report);print(json.dumps({'report':str(P),'report_sha256':sha(P),'counts':report['counts']},ensure_ascii=False,indent=2))
