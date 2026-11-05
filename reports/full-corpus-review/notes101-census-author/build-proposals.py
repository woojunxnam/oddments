"""Source-only author preparation. Does not register or edit shared state."""
import copy, hashlib, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
import note_review_queue as q
import notes_census_reassessment as nr
P='reports/full-corpus-review/notes101-census-author/'
author={'actor_id':'/root/notes101_omission_census_author','session_id':'notes101-omission-census-author-actual-20261104'}
def sha(raw):return hashlib.sha256(raw).hexdigest()
def readj(p):return json.loads(Path(p).read_bytes())
def write(p,d):
 path=ROOT/p;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(q.encoded(d));return sha(path.read_bytes())
state=readj(ROOT/q.STATE)
inv=readj('/workspace/scratch/notes101-validated-inventory.json')
packets=[readj('/workspace/scratch/notes101-'+x+'-visible-input.json') for x in ['a','b']]
allunits={u['id']:u for ch in inv['notes']['chapters'] for u in ch['units']}
assert len(allunits)==306
for uid,b in inv['units'].items():assert sha(allunits[uid]['body'].encode())==b['body_sha256']
inputs={x['unit']['id']:x for p in packets for x in p['units']}
configs={
 'ipledge-transition':('a','26','FDA iPLEDGE Q&A Q3, Q4, Q7; participant requirements established, prescription-specific authorization not established','FDA content current2026-06-16; announced modification implementation2026-11-15 is future at author review2026-11-04. Current pharmacy-guide authorization conditions and deadlines not retained.',[
  ('IPLEDGE-017','Isotretinoin 조제 시 participant 등록·자격과 별도로 이번 처방의 iPLEDGE dispensing authorization을 확인해야 한다.','SOURCE_BLOCKED')]),
 'w5-b-11':('a','37','21 CFR1308.12(a),(c) introductory text,(c)(9) Fentanyl (9801)','eCFR current page retrieved2026-11-04; fentanyl clause read2026-11-04; individual original commencement date not separately established.',[
  ('TIRF-017','TIRF에 포함된 fentanyl은 연방 Schedule II 통제물질이다.','AUTHOR_SOURCE_CHECKED'),
  ('TIRF-018','Fentanyl transdermal patch의 fentanyl도 연방 Schedule II 통제물질이다.','AUTHOR_SOURCE_CHECKED')]),
 'w3-c-1':('b','6251c99ae2dd3d1a','Policy2023-02 III.C.2(c),(g), III.D.4 and IX Appendix inclusion/exclusion criteria before administration','Policy adopted2023-05-04; revised2023-09-07 and2025-09-04; PDF prints no separate effective date; retained official PDF reviewed2026-11-04.',[
  ('SCREENING-024','Pharmacist의 vaccine 업무에는 투여 전 patient screening으로 indications·contraindications 및 applicable standing-order inclusion/exclusion criteria를 평가하는 임상 판단이 포함된다.','AUTHOR_SOURCE_CHECKED')]),
 'w1-a-10':('b','ee1d8475c5e7a5b0','247 CMR3.05 Legally Protected Health Care Activity; complaint and criminal charge','PDF footer:4/25/25 (Effective1/9/25), Mass.Register1546; §3.05 official retained text reviewed2026-11-04.',[
  ('COMPLAINT-008','Massachusetts에서 적법하고 good professional practice standards에 맞는 reproductive 또는 gender-affirming care의 제공·지원·관련 약 조제로 생긴 complaint를 이유로 initial licensure를 거부하지 않는다.','AUTHOR_SOURCE_CHECKED'),
  ('COMPLAINT-009','Massachusetts에서 적법하고 good professional practice standards에 맞는 reproductive 또는 gender-affirming care의 제공·지원·관련 약 조제로 생긴 complaint를 이유로 renewal을 거부하지 않는다.','AUTHOR_SOURCE_CHECKED'),
  ('CHARGE-010','Massachusetts에서 적법하고 good professional practice standards에 맞는 reproductive 또는 gender-affirming care의 제공·지원·관련 약 조제로 생긴 criminal charge를 이유로 initial licensure를 거부하지 않는다.','AUTHOR_SOURCE_CHECKED'),
  ('CHARGE-011','Massachusetts에서 적법하고 good professional practice standards에 맞는 reproductive 또는 gender-affirming care의 제공·지원·관련 약 조제로 생긴 criminal charge를 이유로 renewal을 거부하지 않는다.','AUTHOR_SOURCE_CHECKED')])}
manifest=[];summary=[]
for uid,(ab,key,section,version,adds) in configs.items():
 x=inputs[uid]; oldbinding=x['binding']; old=readj(ROOT/oldbinding['census_path'])
 assert q.raw_sha((ROOT/oldbinding['census_path']).read_bytes())==oldbinding['census_sha256']
 assert x['unit']['body']==allunits[uid]['body']
 assert x['claims']==[c for c in old['claims'] if c['unit_id']==uid]
 assert all(q.digest(c)==oldbinding['claim_record_sha256s'][c['claim_id']] for c in x['claims'])
 prefix=f'reports/full-corpus-review/independent-notes/notes101-{ab}/sources/'
 ext='raw' if ab=='a' else 'pdf'
 originals={'raw':prefix+key+'.'+ext,'text':prefix+key+('.txt' if ab=='a' else '.read.txt'),'retrieval_metadata':prefix+key+'.meta.json'}
 saved={}
 for kind,path in originals.items():
  dst=P+'sources/'+uid+'.'+{'raw':ext,'text':'txt','retrieval_metadata':'meta.json'}[kind]
  raw=(ROOT/path).read_bytes();(ROOT/dst).parent.mkdir(parents=True,exist_ok=True);(ROOT/dst).write_bytes(raw)
  saved[kind+'_path']=dst;saved[kind+'_sha256']=sha(raw)
 meta=readj(ROOT/originals['retrieval_metadata']);url=meta.get('official_url',meta.get('url'))
 assert meta['raw_sha256']==saved['raw_sha256']
 source_id='notes101-author-'+uid
 src={'source_id':source_id,'source_type':'PUBLIC_OFFICIAL','official_url':url,'exact_section':section,'law_checked_date':'2026-11-04','checked_at':'2026-11-04','version_or_effective_date_status':version,'source_evidence':saved['raw_path'],'source_evidence_sha256':saved['raw_sha256'],'text_evidence_path':saved['text_path'],'text_evidence_sha256':saved['text_sha256'],'retrieval_metadata_path':saved['retrieval_metadata_path'],'retrieval_metadata_sha256':saved['retrieval_metadata_sha256'],'retention_provenance':'Unchanged retained official primary bytes from actual independent session; correction author personally read designated provisions. This is not a fresh retrieval or an independent verdict.','author_read_date':'2026-11-04','source_use_manifest':{'source_id':source_id,'source_class':'PUBLIC_OFFICIAL','publisher':'FDA' if uid=='ipledge-transition' else ('eCFR/DEA' if uid=='w5-b-11' else 'Massachusetts Department of Public Health / Board of Registration in Pharmacy'),'url':url,'access_type':'PUBLIC','authority_level':'PRIMARY_OFFICIAL','permission_status':'VERIFIED','legal_authority_allowed':True,'question_text_storage_allowed':False,'ai_processing_allowed':True,'public_repo_allowed':True,'notes':'SOURCE_USE_POLICY Class A official primary authority; no question content.','last_reviewed':'2026-11-04'}}
 sources=copy.deepcopy(old['sources']);assert source_id not in sources;sources[source_id]=src
 claims=copy.deepcopy(x['claims']); added=[]
 for suffix,statement,status in adds:
  cid='NOTE101-CENSUS-'+uid.upper()+'-'+suffix;added.append(cid)
  c={'claim_id':cid,'unit_id':uid,'unit_content_sha256':oldbinding['body_sha256'],'statement_ko':statement,'record_granularity':'AUTHOR_ENUMERATED_ATOMIC_PROPOSITION','legal_claim_kind':'MATERIAL_NOTE_PROPOSITION','is_complete_atomic_enumeration_evidence':True,'review_status':status,'source_id':source_id,'authority_clauses':[section],'official_url':url,'source_evidence':saved['raw_path'],'source_evidence_sha256':saved['raw_sha256'],'text_evidence_path':saved['text_path'],'text_evidence_sha256':saved['text_sha256'],'retrieval_metadata_path':saved['retrieval_metadata_path'],'retrieval_metadata_sha256':saved['retrieval_metadata_sha256'],'checked_at':'2026-11-04','law_checked_date':'2026-11-04','effective_date':None,'version_or_effective_date_status':version,'related_question_ids':[],'practice_link_status':'NO_NEW_QUESTION_LINK_CLAIMED','blocker':None,'author_provenance':author,'independent':False,'verification_scope_ko':'실제 단원 본문 누락의 저자 열거·공식 원문 대조일 뿐 독립 법규 PASS 또는 release 증거가 아니다.'}
  if status=='SOURCE_BLOCKED': c['blocker']='Retained FDA Q&A Q3 establishes enrollment and Q4/Q7 direct to current iPLEDGE instructions; it does not state prescription-specific dispensing authorization conditions or validity deadline. Current approved pharmacy guide not retained/read; no numeric deadline inferred. Body proposition explicitly enumerated pending source verification.'
  claims.append(c)
 unit=copy.deepcopy(x['census_unit']);unit.update(claim_count=len(claims),source_checked_claim_count=sum(c['review_status']=='AUTHOR_SOURCE_CHECKED' for c in claims),source_blocked_claim_count=sum(c['review_status']=='SOURCE_BLOCKED' for c in claims),independent_verified_claim_count=0,independent_completeness_status='PENDING')
 census={'schema_version':1,'purpose':nr.PURPOSE,'wave_id':'notes101-omission-census-author-'+uid,'reviewed_at':'2026-11-04','author_provenance':author,'independent_audit':False,'canonical_release_credit':0,'question_audit_credit':0,'content_mutated':False,'method_ko':'원 단원 전문과 원 claim 전량을 실제 읽고 독립 누락지적을 새 원자명제로만 append. 모든 기존 claim/source object canonical 내용을 그대로 보존. 법규 HOLD/SOURCE_BLOCKED 해소 없음.','sources':sources,'units':[unit],'claims':claims}
 cp=P+uid+'-census.json';csha=write(cp,census)
 previous=next(j for j in state['jobs'] if uid in j['unit_ids'] and j['job_id']==next(p['job']['job_id'] for p in packets if any(z['unit']['id']==uid for z in p['units'])))
 assert previous['status']=='INTEGRATED' and previous['unit_bindings'][uid]==oldbinding
 report=readj(ROOT/previous['result']['evidence']['path']);row=next(r for r in report['records'] if r['unit_id']==uid)
 ledger=next(json.loads(l) for l in (ROOT/q.LEDGER).read_text().splitlines() if json.loads(l)['unit_id']==uid)
 fields={k:ledger[k] for k in nr.LEDGER_FIELDS}; assert q.digest(fields)==oldbinding['ledger_binding_sha256']
 rec={'schema_version':1,'purpose':nr.PURPOSE,'reassessment_id':'notes101-census-omission-'+uid+'-v1','unit_id':uid,'body_sha256':oldbinding['body_sha256'],'previous_job_id':previous['job_id'],'previous_job_sha256':q.digest(previous),'previous_binding':oldbinding,'previous_result':{'path':previous['result']['result_path'],'raw_sha256':previous['result_sha256']},'previous_report':previous['result']['evidence'],'previous_ledger_fields':fields,'replacement':{'census_path':cp,'census_sha256':csha,'notes_revision':fields['atomic_census_notes_revision']},'author_provenance':author,'change_basis':'Actual integrated independent notes101-'+ab+' finding: '+ ' / '.join(row['omissions'])+'; append-only author proposal, not registration or legal adjudication.','claim_mapping':{c['claim_id']:[c['claim_id']] for c in x['claims']},'added_claim_ids':added,'changed_claim_ids':[],'omission_resolutions':[{'omission_sha256':sha(o.encode()),'claim_ids':added,'explanation':'본문에서 빠진 명제를 별도 원자 claim으로 append했다. 기존 명제·source 바이트와 모든 기존 blocker를 보존한다. iPLEDGE authorization의 미확보 상세는 새 claim SOURCE_BLOCKED로 명시한다.' if uid=='ipledge-transition' else '본문의 누락된 법적 주체·행위·단계를 새 원자명제로 명시했고 지정 공식 1차 조항과 대조했다. 기존 명제·source object와 기존 법규 blocker를 보존한다.'} for o in row['omissions']]}
 rp=P+uid+'-reassessment.json';rsha=write(rp,rec)
 (ROOT/(P+'bodies/'+uid+'.txt')).parent.mkdir(parents=True,exist_ok=True);(ROOT/(P+'bodies/'+uid+'.txt')).write_bytes(x['unit']['body'].encode())
 manifest.append({'unit_id':uid,'retained_originals':originals,**saved,'official_url':url,'exact_section':section,'version_or_effective_date_status':version,'author_read_date':'2026-11-04'})
 summary.append({'unit_id':uid,'old_claim_count':len(x['claims']),'new_claim_count':len(claims),'added_claim_ids':added,'changed_claim_ids':[],'census_path':cp,'census_sha256':csha,'record_path':rp,'record_sha256':rsha,'body_sha256':oldbinding['body_sha256'],'original_claims_canonical_preserved':all(q.digest(a)==q.digest(b) for a,b in zip(x['claims'],claims)),'all_original_source_objects_canonical_preserved':all(q.digest(sources[k])==q.digest(v) for k,v in old['sources'].items())})
write(P+'source-manifest.json',manifest)
write(P+'proposal-index.json',{'purpose':nr.PURPOSE,'author_provenance':author,'independent_audit':False,'canonical_release_credit':0,'question_audit_credit':0,'inventory_notes_body_hashes_reconfirmed':len(allunits),'validated_source_head':packets[0]['validated_source_head'],'inventory_raw_sha256':sha(Path('/workspace/scratch/notes101-validated-inventory.json').read_bytes()),'packets':[{'path':'/workspace/scratch/notes101-'+ab+'-visible-input.json','sha256':sha(Path('/workspace/scratch/notes101-'+ab+'-visible-input.json').read_bytes())}for ab in ['a','b']],'proposals':summary})
print(json.dumps(summary,ensure_ascii=False,indent=2))
