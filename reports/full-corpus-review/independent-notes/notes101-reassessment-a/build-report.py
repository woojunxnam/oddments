import sys,json,hashlib,subprocess
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'scripts'))
import note_review_queue as q
from notes_census_reassessment import replacement_row
OUT=Path(__file__).resolve().parent; ROOT=Path.cwd(); PREFIX=OUT.relative_to(ROOT).as_posix()
def read(p):return json.loads(Path(p).read_text())
def sha(p):return q.raw_sha(Path(p).read_bytes())
def write(n,d):(OUT/n).write_bytes(q.encoded(d))
j=read(OUT/'assignment.json');p=read(OUT/'visible-input.json');u=p['units'][0];uid=u['unit']['id'];b=j['unit_bindings'][uid];ctx=read(OUT/'related-context.json')
assert p['job']==j and u['binding']==b
assert sha(OUT/'related-context.json')=='1c3c2abf4e74af30eaf823bb6fe162c7f04209069cabe1dda6d57bb9f758f33e'
assert q.raw_sha(u['unit']['body'].encode())==b['body_sha256']
census=read(b['census_path']);assert sha(b['census_path'])==b['census_sha256']
assert census['claims']==u['claims'] and census['units'][0]==u['census_unit'] and q.digest(u['census_unit'])==b['census_unit_record_sha256']
assert {c['claim_id']:q.digest(c) for c in u['claims']}==b['claim_record_sha256s']
notes=read('notes/guide.json');actual=[x for c in notes['chapters'] for x in c['units'] if x['id']==uid];assert len(actual)==1 and actual[0]['body']==u['unit']['body']
rr=read('reports/full-corpus-review/notes101-census-author/ipledge-transition-reassessment.json');assert sha('reports/full-corpus-review/notes101-census-author/ipledge-transition-reassessment.json')==j['reassessment_record_sha256']
assert q.digest(replacement_row(rr,census))==b['ledger_binding_sha256']
oldraw=subprocess.check_output(['git','show',j['base_commit']+':'+rr['previous_binding']['census_path']]);assert q.raw_sha(oldraw)==rr['previous_binding']['census_sha256'];old=json.loads(oldraw);oldclaims=[c for c in old['claims'] if c['unit_id']==uid];assert oldclaims==u['claims'][:16]
oldreport=read(rr['previous_report']['path']);assert sha(rr['previous_report']['path'])==rr['previous_report']['raw_sha256']
oldrow=next(r for r in oldreport['records'] if r['unit_id']==uid);assert len(oldrow['omissions'])==1
assert q.raw_sha(oldrow['omissions'][0].encode())==j['reassessment_review']['omission_resolutions'][0]['omission_sha256']
assert ctx['related_ids']==ctx['missing_related_ids']==ctx['questions']==[] and len(ctx['derived'])==4
for d in ctx['derived']:
 assert d['visible_item']['source_hashes'][uid]==b['body_sha256']
# Source HEAD file bytes are checked against retained root projection; no notes loader/guard bypass.
for f in ['site/notes/study-data.js','site/notes/refresh-data.js']:
 raw=subprocess.check_output(['git','show',ctx['source_head']+':'+f]);assert q.raw_sha(raw)==ctx['source_files'][f]
manifest=[]
for f in sorted(OUT.rglob('*')):
 if f.is_file() and f.name not in ['report.json','input-source-verification.json','source-manifest.json']:
  manifest.append({'path':f.relative_to(ROOT).as_posix(),'raw_sha256':sha(f)})
write('source-manifest.json',manifest)
write('input-source-verification.json',{'assignment_packet_matches':True,'body_current_notes_guide_matches':True,'body_sha256':b['body_sha256'],'census_raw_sha256':b['census_sha256'],'census_unit_and_all_17_claim_hashes_match':True,'native_replacement_row_binding_matches':True,'committed_global_ledger_status':'Base committed ledger retains old census binding; this reassessment uses root native registered replacement projection. No global progress or release credit claimed.','original_16_records_preserved_exactly':True,'original_report_sha256':sha(rr['previous_report']['path']),'original_omission_sha256':q.raw_sha(oldrow['omissions'][0].encode()),'related_questions':0,'derived_read':4,'source_head_committed_derived_file_hashes_match':True,'strict_current_inventory':'Root-provided strict current inventory observation in packet; worker checks exact body/census/claim hashes. Sparse immutable preimages excluded; no worker load_notes or guard changes.','canonical_release_credit':0,'question_audit_credit':0})
def authority(name,section):
 meta=read(OUT/'sources'/f'{name}.meta.json');a={'source_type':'PUBLIC_OFFICIAL','official_url':meta['official_url'],'exact_section':section,'law_checked_date':'2026-11-04','version_or_effective_date_status':('ZENATANE label revised09/2026; DailyMed displayed updated2026-09-20, search API published2026-10-09. Current retrieved2026-11-04; cited only authorization requirement, not numeric validity or future implementation workflow.' if name=='zenatane-current' else 'FDA content current2026-06-16; modification approved2026-02-09, planned implementation2026-11-15 remains future on review2026-11-04. Oct2023 testing enforcement discretion continues until full implementation; no actual future implementation asserted.'),'evidence_path':PREFIX+'/sources/'+name+'.raw','evidence_sha256':sha(OUT/'sources'/f'{name}.raw'),'text_evidence_path':PREFIX+'/sources/'+name+'.txt','text_evidence_sha256':sha(OUT/'sources'/f'{name}.txt'),'retrieval_metadata_path':PREFIX+'/sources/'+name+'.meta.json','retrieval_metadata_sha256':sha(OUT/'sources'/f'{name}.meta.json')};return a
findings={
1:('FDA2월9일 update는 해당 날짜의 modification 승인 사실을 명시한다. 시행과 구분하여 지지한다.','fda-ipledge','iPLEDGE Update: FDA approves iPLEDGE REMS modification (February9,2026), opening paragraph'),
2:('FDA6월16일 update는 implementation delay를 명시한다.','fda-ipledge','Implementation for iPLEDGE REMS Modifications Delayed Until November (June16,2026), first paragraph'),
3:('같은 최신 update의 planned implementation date는2026-11-15이다. 11월4일 현재 미래 예정일로만 판정한다.','fda-ipledge','June16,2026 update, first paragraph (planned implementation date November15,2026)'),
4:('6월 update는 full implementation까지 Oct2023 pregnancy-testing enforcement discretion을 계속한다고 명시한다. 승인·전면시행과 별개다.','fda-ipledge','June16,2026 update, third paragraph; October13,2023 update, enforcement-discretion bullets'),
5:('Q3는 healthcare professionals의 등록을 isotretinoin 처방 요건으로 명시한다. 구체적 자격 전부를 추가 추론하지 않는다.','fda-ipledge-qa','Q3/A3, first paragraph'),
6:('Q3는 환자의 enrollment와 모든 REMS requirements 준수를 명시한다.','fda-ipledge-qa','Q3/A3, second paragraph'),
7:('Q3는 약국 등록을 dispensing의 요건으로 명시한다.','fda-ipledge-qa','Q3/A3, first paragraph'),
8:('Q3는 환자 category에 따라 requirements가 달라진다고 명시한다.','fda-ipledge-qa','Q3/A3, second paragraph'),
9:('FDA는 shared system이 모든 승인 isotretinoin을 포함한다고 한다. 다른 retinoid들의 product-specific REMS 전체 대조는 하지 못했다. 원래 보류를 유지한다.','fda-ipledge','iPLEDGE REMS for Isotretinoin Products, shared-system paragraph'),
10:('Q6 및 Oct2023/Feb2026 문단은 모든 pretreatment pregnancy tests의 medical setting을 요구한다.','fda-ipledge-qa','Q6/A6; FDA iPLEDGE October13,2023 and February9,2026 pretreatment requirements'),
11:('2월 update와 Oct2023 discretion은 during/after home testing과 pretreatment medical setting을 분리한다. home-testing 허용을 최초검사로 확대하지 않는다.','fda-ipledge','February9,2026 update, pregnancy-testing bullets; October13,2023 update, final paragraph'),
12:('2월 update pharmacy 첫 bullet은 cannot-get-pregnant 환자의30-day prescription window 제거를 명시한다. 아직 전면 시행중이라고 하지 않는다.','fda-ipledge','February9,2026 update, Important changes for pharmacies, first bullet'),
13:('2월 update prescriber counseling bullet은 enrollment counseling 유지와 cannot-get-pregnant 환자의 monthly documentation 제거를 명시한다.','fda-ipledge','February9,2026 update, Important changes for health care professionals who prescribe, third bullet'),
14:('2월 update의 pregnancy-testing 변경은 home during/after 및 반복검사 waiting-period 변경을 포함한다. 현재 discretion과 미래 modification을 구분한다.','fda-ipledge','February9,2026 update, Important changes for patients / prescribers'),
15:('2월 update는 annual staff training과 authorized representative의 completion records 보존을 명시한다. 그러나 현재 approved pharmacy training package 상세 미확보라는 inherited blocker를 이 census-only 재감사에서 해제하지 않는다.','fda-ipledge','February9,2026 update, Important changes for pharmacies, second bullet'),
16:('2월 FDA update의 window 제거와 별개로 fresh ZENATANE §5.2는 최대30-day supply를 명시한다. 추가 라벨 근거는 기록하되 원래 pharmacy-guide 미확보 blocker 및 SOURCE_BLOCKED 상태를 규약대로 유지한다.','zenatane-current','Full Prescribing Information §5.2 iPLEDGE REMS, pharmacy requirements (maximum30-day supply)'),
17:('새 명제는 enrollment/participant 자격과 별개인 이번 dispensing authorization을 독립 열거하여 원래 누락을 해소한다. Fresh ZENATANE §5.2는 pharmacy certification 외에 obtain authorization to dispense 및 authorized patient에게만 dispense를 별도 의무로 규정한다. FDA 현행 페이지의2021-10-08 pharmacy update도 prior-to-dispensing RMA를 명시한다. 본문과 새 명제의 최소 authorization 확인 의무만 KEEP; 현재 guide 미확보로 숫자 validity deadline이나 상세 운영조건은 승인하지 않는다.','zenatane-current','Full Prescribing Information §5.2 iPLEDGE REMS, pharmacy requirements (obtain authorization to dispense; only authorized patients)')}
claims=[]
for n,c in enumerate(u['claims'],1):
 finding,name,section=findings[n];cid=c['claim_id'];r={'claim_id':cid,'claim_record_sha256':b['claim_record_sha256s'][cid],'claim_read_completely':True,'statement_ko':c['statement_ko'],'legal_status':'SOURCE_BLOCKED' if n in [9,15,16] else 'KEEP','finding':finding,'authorities':[authority(name,section)]}
 inherited=j['carried_legal_blockers'].get(uid,{}).get(cid)
 if inherited:r['inherited_legal_blockers']=inherited;r['blocker']=inherited[0]['blocker']
 if n in [10]:r['authorities'].append(authority('fda-ipledge','October13,2023 update, final paragraph (all pre-treatment tests in medical setting)'))
 if n==17:r['authorities'].append(authority('fda-ipledge','October8,2021 update, Important changes for Pharmacies (all pharmacists need RMA prior to dispensing); February9,2026 pharmacy changes (reverse authorization if not picked up)'))
 claims.append(r)
row={'unit_id':uid,'binding':b,'body_read_completely':True,'completeness':'COMPLETE','omissions':[],'completeness_method':'변경없는 본문 네 단락과 최종17명제 전문을 문장/조건별 대조했다. 001–004는 승인·delay·예정일·discretion 구분,005–009와017은 participant/category/retinoid 및 독립 dispensing authorization,010–011은 pretreatment와 during/after 검사,012–016은 window·counseling·검사변경·training·supply를 포괄한다. 편집일과11월15일 이후 재확인 권고는 editorial inventory다. 원래 omission 정확문자열과 SHA를 다시 읽었고 새017이 그 실질 명제를 별도 열거한다. 새 명제에 없는 숫자기한을 본문이 주장하지 않으므로 새 누락으로 만들지 않는다. 원16개 claim record가 바이트동등 object로 보존됨도 확인했다.','legal_status':'SOURCE_BLOCKED','claims':claims,'reassessment_review':{**j['reassessment_review'],'final_census_read_completely':True,'all_original_omissions_reassessed':True,'all_original_propositions_preserved':True},'original_omission_reassessment':[{'original_omission':oldrow['omissions'][0],'omission_sha256':q.raw_sha(oldrow['omissions'][0].encode()),'resolution':'RESOLVED_IN_CENSUS','claim_ids':[u['claims'][-1]['claim_id']],'finding':'017이 별도 authorization 명제를 실제 추가했다. 법규 상세 미확보 선언을 PASS로 승계하지 않고 fresh label 및 FDA 현행 페이지에서 최소 명제만 직접 확인했다.'}],'related_context_review':{'related_question_ids':[],'body_direct_question_links':[],'derived_read_completely':True,'derived_ids':[x['visible_item']['id'] for x in ctx['derived']],'finding':'LAW-044와RF-009/RF-062/RF-C-rems 전문을 읽었다. iPLEDGE에 해당하는 문구는 current workflow 확인과 승인/시행 구분을 가르치고 숫자 authorization 기한을 추가하지 않는다. 나머지 단원 전체 법규 또는 question 정답은 이 배정의 PASS가 아니다.'}}
report={k:j[k] for k in ['stage','actor_provenance','auditor','auditor_instance']};report.update({'independent_of_authors':True,'canonical_audit':False,'canonical_release_credit':0,'question_audit_credit':0,'reviewed_at':'2026-11-04','records':[row],'limitations_ko':'기존 009/015/016 SOURCE_BLOCKED는 inherited blocker와 함께 유지한다. COMPLETE는 census 누락 해소이고 법규 전체 PASS가 아니다. 같은 실제 auditor instance를 유지했으며 인원 credit 추가가 없다.'});write('report.json',report)
print('report written',sha(OUT/'report.json'),'KEEP',sum(c['legal_status']=='KEEP' for c in claims),'SOURCE_BLOCKED',sum(c['legal_status']=='SOURCE_BLOCKED' for c in claims))
