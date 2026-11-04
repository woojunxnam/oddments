"""Prepare append-only single-unit censuses; never fabricate integration bindings."""
import copy,json,hashlib,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
import note_review_queue as q
P='reports/full-corpus-review/notes120-census-author/'
AUTHOR={'actor_id':'/root/notes101_omission_census_author','session_id':'notes101-omission-census-author-actual-20261104'}
def blob(commit,path):return subprocess.check_output(['git','show',commit+':'+path],cwd=ROOT)
def write(path,obj):
 dst=ROOT/path;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(q.encoded(obj));return q.raw_sha(dst.read_bytes())
def retain(key,commit,original_base):
 meta_path=original_base+'.meta.json';meta=json.loads(blob(commit,meta_path)); url=meta['official_url']; saved={}
 for label,suffix in [('raw','.pdf'),('text','.txt'),('metadata','.meta.json')]:
  src=original_base+suffix;raw=blob(commit,src);dst=P+'sources/'+key+suffix
  (ROOT/dst).parent.mkdir(parents=True,exist_ok=True);(ROOT/dst).write_bytes(raw)
  saved[label+'_path']=dst;saved[label+'_sha256']=q.raw_sha(raw)
 assert saved['raw_sha256']==meta['raw_sha256'] and saved['text_sha256']==meta['text_sha256']
 return {'source_id':'notes120-author-'+key,'source_type':'PUBLIC_OFFICIAL','official_url':url,'source_evidence':saved['raw_path'],'source_evidence_sha256':saved['raw_sha256'],'text_evidence_path':saved['text_path'],'text_evidence_sha256':saved['text_sha256'],'retrieval_metadata_path':saved['metadata_path'],'retrieval_metadata_sha256':saved['metadata_sha256'],'retained_from_commit':commit,'retained_original_base':original_base,'law_checked_date':'2026-11-04','author_read_date':'2026-11-04','retrieval_scope_ko':'실제 감사자가 회수한 공식 원문 바이트를 변경 없이 보존하고 보완 저자가 지정 조항을 다시 읽었다. 새 회수 또는 독립 판정이라는 뜻이 아니다.'}
sources={
 'cdtm':retain('cdtm','606ecc3d','reports/full-corpus-review/independent-notes/notes120-b/sources/cdtm'),
 'cmr9':retain('cmr9','606ecc3d','reports/full-corpus-review/independent-notes/notes120-b/sources/conduct'),
 'storage':retain('storage','a1953187e9b46d7f2eac020f1d91c2d19f6047d9','reports/full-corpus-review/independent-notes/notes120-d/sources/3cc436f60a831369'),
 'shipping':retain('shipping','a1953187e9b46d7f2eac020f1d91c2d19f6047d9','reports/full-corpus-review/independent-notes/notes120-d/sources/86b25003cfc915eb')}
VERSIONS={'cdtm':'PDF는 Mass.Register1354,2017-12-15를 표시한다. 개별 조항의 별도 시행일은 확정하지 않았다. 2026-11-04 지정 원문 저자 재검토.','cmr9':'PDF는 Mass.Register1536,2024-12-06를 표시한다. 개별 조항의 별도 시행일은 확정하지 않았다. 2026-11-04 지정 원문 저자 재검토.','storage':'Policy2020-05: adopted2020-06-26,revised2020-10-23. 별도 시행일 표시는 확인되지 않았다. 2026-11-04 저자 재검토.','shipping':'Advisory adopted2018-06-28,revised2025-01-09. Best-practice recommendation이며 규정 의무로 승격하지 않는다. 2026-11-04 저자 재검토.'}
for key,s in sources.items():
 s['version_or_effective_date_status']=VERSIONS[key]
 s['source_use_manifest']={'source_id':s['source_id'],'source_class':'PUBLIC_OFFICIAL','publisher':'Massachusetts Department of Public Health / Board of Registration in Pharmacy','url':s['official_url'],'access_type':'PUBLIC','authority_level':'PRIMARY_OFFICIAL','permission_status':'VERIFIED','legal_authority_allowed':True,'question_text_storage_allowed':False,'ai_processing_allowed':True,'public_repo_allowed':True,'notes':'SOURCE_USE_POLICY Class A; retained public official primary bytes, no question content.','last_reviewed':'2026-11-04'}
 s['exact_section']={'cdtm':'247 CMR16.04(1),(2);16.03(5)(c)–(d)','cmr9':'247 CMR9.15(2)(c),9.19(3),9.22(2)','storage':'Policy2020-05 VI,XV.1–6','shipping':'Medication Delivery and Shipping advisory:Counseling;Delivery to Alternative Locations'}[key]
# A source may demonstrate the limit of a proposition while that proposition remains blocked.
C={
'w3-d-8': [('CPA-PATIENT-SCOPE','약사는 CPA에 해당 환자의 범위를 명시해야 한다.','cdtm','247 CMR16.04(1),(2);16.03(5)(c)–(d)','16.04(1)은 community pharmacy setting에서 특정 환자의 written referral와 consent를 요구하지만, 모든 setting의 CPA에 동일한 독립 patient-scope 항목을 적도록 하는 본문 문구의 정확한 범위는 이 조항만으로 확정하지 못했다. Disease-state 목록이나 staff delegation 범위와 환자 범위를 같은 것으로 대체하지 않는다.')],
'w3-d-22':[('AUTHENTICITY','약사는 EPT prescription을 조제하기 전에도 professional judgment로 처방 자체가 진정한지 판단해야 한다.','cmr9','247 CMR9.15(2)(c)',None)],
'inventory-working-example':[('INVESTIGATE-ONE-UNIT','시작100·입고50·교부40으로 예상110인 재고의 실물이109이면 1단위 차이의 원인을 조사한다.',None,'본문의 재고 예시; 적용 inventory/reconciliation 조사근거 추가 대조 필요','수량 예시의 차이 원인 조사라는 독립 본문 명제를 열거했다. 실제 1단위 불일치에 대한 주체·setting·통제물질별 조사 의무의 정확한 공식 조항을 아직 확정하지 않았으며, significant-loss 여부나 통지시계를 이 명제로 결정하지 않는다.')],
'w4-a-8':[('AUTO-DEFROST-DUTY','약국의 freezer는 Board가 달리 승인하지 않는 한 frost-free 및 automatic defrost cycle을 갖추어야 한다.','cmr9','247 CMR9.22(2);Policy2020-05 VI와의 예외관계는 기존 blocker 유지',None)],
'w4-a-9':[
 ('AFFECTED-PRODUCT','온도 excursion 평가에서는 영향을 받은 제품을 확인해야 한다.','storage','Policy2020-05 XV.1–5','정책은 excursion 평가와 제품별 제조사 안전·유효성 확인을 정한다. 본문에 열거된 product별 확인 단계 전체의 정확한 자료·범위 및 해당 제품 원문을 확정하지 못했다. 기존017의 미완료 설명은 그대로 보존한다.'),
 ('AFFECTED-LOT','온도 excursion 평가에서는 영향을 받은 lot를 확인해야 한다.','storage','Policy2020-05 XV.1–5','정책 XV.1–5에는 lot라는 독립 필수 data field가 직접 열거되지 않는다. 본문 lot 확인을 operational assessment 단계로 열거하지만 모든 제품에 동일한 별도 법정 lot field 의무라고 인증하지 않는다. 기존018 보류를 유지한다.'),
 ('AFFECTED-QUANTITY','온도 excursion 평가에서는 영향을 받은 수량을 확인해야 한다.','storage','Policy2020-05 XV.1–5','정책 XV.1–5에는 quantity라는 독립 필수 data field가 직접 열거되지 않는다. 본문 수량 확인 단계는 열거하지만 모든 제품에 동일한 별도 법정 수량 field 의무라고 인증하지 않는다. 기존019 보류를 유지한다.'),
 ('REPEATED-EXPOSURE','온도 excursion 평가에서는 해당 제품의 반복 노출 여부를 확인해야 한다.','storage','Policy2020-05 XV.1–5','정책 XV.1–5는 length/magnitude 평가와 제조사 확인을 정하지만 본문의 반복 노출별 요건 전체를 직접 열거하지 않는다. 개별 제품의 반복노출 안정성 자료가 없으며 기존020 보류를 유지한다.'),
 ('ADMINISTERED-PATIENT-NOTICE','안전하지 않거나 유효하지 않은 제품을 이미 환자에게 투여했다면 그 환자에게 통지해야 한다.','storage','Policy2020-05 XV.6',None),
 ('DISPENSED-PROVIDER-NOTICE','안전하지 않거나 유효하지 않은 제품을 이미 환자에게 교부했다면 그 환자의 health care provider에게 통지해야 한다.','storage','Policy2020-05 XV.6',None)],
'w4-a-11':[('COUNSELING-CHANNEL','Specialty-to-retail pickup을 포함한 배송의 상담 경로에서는 서면 약물정보와 질문할 전화번호를 제공하라는 Board advisory 권고를 확인한다.','shipping','Medication Delivery and Shipping advisory:Counseling;Delivery to Alternative Locations',None)],
'w4-a-16':[('ACCURACY-PERFORMANCE','약국은 고형제 전자계수기와 다른 전자측정장치의 정확성과 성능을 보장해야 한다.','cmr9','247 CMR9.19(3)',None)],
'w4-b-12':[
 ('NONSTERILE-CSP-FACILITY','Nonsterile ingredients에서 sterile CSP를 만드는 경로에서는 적절한 시설 조건을 충족해야 한다.',None,'USP797 nonsterile starting components의 시설 조건; current official text 추가 대조 필요','원문 본문의 시설 전제를 열거했으나 현행 USP-NF 해당 전문·시설별 적용조건·2026 개정 여부를 아직 취득·확정하지 않았다. Category 일반 시설명제010만으로 이 별도 경로의 조건이 입증되지는 않는다.'),
 ('NONSTERILE-CSP-VALIDATION','Nonsterile ingredients에서 sterile CSP를 만드는 경로에서는 적절한 검증 조건을 충족해야 한다.',None,'USP797 nonsterile starting components의 검증 조건; current official text 추가 대조 필요','원문 본문의 검증 전제를 열거했으나 sterilization validation 등의 현행 정확한 검증 항목과 적용조건·2026 개정 여부를 아직 취득·확정하지 않았다. 기존 sterilization·endotoxin 명제를 바꾸지 않는다.')],
'w4-b-17':[('ASEPTIC-OBSERVATION','Aseptic manipulation competency 평가에는 실제 무균조작의 observation이 포함된다.',None,'USP797 personnel aseptic manipulation competency observation; current official text 추가 대조 필요','본문의 observation을 media-fill 및 sampling과 구별해 독립 열거했다. 현행 USP-NF exact observation 요건·평가자·주기·2026 개정 여부를 아직 취득·확정하지 않았으며 기존 source-blocked technical 조건을 해제하지 않는다.')]
}
packets={ab:json.loads(Path('/workspace/scratch/notes120-'+ab+'-visible-input.json').read_bytes())for ab in 'bcde'}
inputs={x['unit']['id']:x for d in packets.values() for x in d['units']}
index=[]
for uid,adds in C.items():
 x=inputs[uid];b=x['binding'];raw=blob('HEAD',b['census_path']);assert q.raw_sha(raw)==b['census_sha256'];old=json.loads(raw)
 oldclaims=[c for c in old['claims']if c['unit_id']==uid];assert oldclaims==x['claims'];assert {c['claim_id']:q.digest(c)for c in oldclaims}==b['claim_record_sha256s']
 assert q.raw_sha(x['unit']['body'].encode())==b['body_sha256']
 oldunit=next(u for u in old['units']if u['unit_id']==uid);assert q.digest(oldunit)==b['census_unit_record_sha256']
 claims=copy.deepcopy(oldclaims);ss=copy.deepcopy(old['sources']);added=[]
 for suffix,text,src,section,blocker in adds:
  cid='NOTE120-CENSUS-'+uid.upper()+'-'+suffix;added.append(cid)
  claim={'claim_id':cid,'unit_id':uid,'unit_content_sha256':b['body_sha256'],'statement_ko':text,'record_granularity':'AUTHOR_ENUMERATED_ATOMIC_PROPOSITION','legal_claim_kind':'MATERIAL_NOTE_PROPOSITION','is_complete_atomic_enumeration_evidence':True,'review_status':'SOURCE_BLOCKED'if blocker else'AUTHOR_SOURCE_CHECKED','source_id':sources[src]['source_id']if src else None,'authority_clauses':[section],'checked_at':'2026-11-04','related_question_ids':[],'blocker':blocker,'author_provenance':AUTHOR,'independent':False,'verification_scope_ko':'누락 명제의 저자 열거 및 지정 1차 조항 대조이며 독립 법규 PASS·question·release 근거가 아니다.'}
  if src:
   source=copy.deepcopy(sources[src]);ss[source['source_id']]=source
   for key in ['official_url','source_evidence','source_evidence_sha256','text_evidence_path','text_evidence_sha256','retrieval_metadata_path','retrieval_metadata_sha256','law_checked_date','version_or_effective_date_status']:claim[key]=source[key]
  claims.append(claim)
 newunit=copy.deepcopy(oldunit);newunit.update(claim_count=len(claims),source_checked_claim_count=sum(c['review_status']=='AUTHOR_SOURCE_CHECKED'for c in claims),source_blocked_claim_count=sum(c['review_status']=='SOURCE_BLOCKED'for c in claims),independent_verified_claim_count=0,independent_completeness_status='PENDING')
 census={'schema_version':1,'purpose':'CENSUS_ONLY_OMISSION_REASSESSMENT','stage':'AUTHOR_PREPARATION_PENDING_FINAL_NATIVE_PREDECESSOR','author_provenance':AUTHOR,'reviewed_at':'2026-11-04','independent_audit':False,'canonical_release_credit':0,'question_audit_credit':0,'body_mutated':False,'sources':ss,'units':[newunit],'claims':claims}
 cp=P+uid+'-census.json';csha=write(cp,census)
 assert all(q.digest(c)==q.digest(claims[i])for i,c in enumerate(oldclaims));assert all(q.digest(v)==q.digest(ss[k])for k,v in old['sources'].items())
 assert all(' '.join(c['statement_ko'].split())not in {' '.join(z['statement_ko'].split())for z in oldclaims}for c in claims[len(oldclaims):])
 (ROOT/(P+'bodies/'+uid+'.txt')).parent.mkdir(parents=True,exist_ok=True);(ROOT/(P+'bodies/'+uid+'.txt')).write_bytes(x['unit']['body'].encode())
 index.append({'unit_id':uid,'body_sha256':b['body_sha256'],'original_binding':b,'original_claim_count':len(oldclaims),'proposed_claim_count':len(claims),'added_claim_ids':added,'changed_claim_ids':[],'original_claims_canonical_preserved':True,'all_original_sources_canonical_preserved':True,'census_path':cp,'census_sha256':csha,'final_integrated_predecessor_record':'PENDING_DO_NOT_INFER_FROM_PACKET'})
write(P+'preparation-index.json',{'author_provenance':AUTHOR,'canonical_release_credit':0,'question_audit_credit':0,'independent_audit_credit':0,'original_claim_count':sum(r['original_claim_count']for r in index),'proposed_claim_count':sum(r['proposed_claim_count']for r in index),'records':index,'packet_sha256s':{ab:q.raw_sha(Path('/workspace/scratch/notes120-'+ab+'-visible-input.json').read_bytes())for ab in 'bcde'}})
write(P+'retained-primary-source-manifest.json',sources)
print([(r['unit_id'],r['original_claim_count'],r['proposed_claim_count'])for r in index])
