"""Actual correction author: append-only censuses, never independent adjudication."""
import copy,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'scripts'))
import note_review_queue as q
P='reports/full-corpus-review/final86-census-author/'
AUTHOR={'actor_id':'/root/notes101_omission_census_author','session_id':'notes101-omission-census-author-actual-20261104'}
BASE='d692cd63'
def blob(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)
def write(path,obj):
 dst=ROOT/path;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(q.encoded(obj));return q.raw_sha(dst.read_bytes())
sources={}
def retain(key,ab,name,ext,section,version):
 base=f'reports/full-corpus-review/independent-notes/final86-{ab}/sources/{name}'
 meta=json.loads(blob(base+'.meta.json'));saved={}
 for label,suffix in [('raw',ext),('text','.txt'),('metadata','.meta.json')]:
  raw=blob(base+suffix);dst=P+'sources/'+key+suffix;(ROOT/dst).parent.mkdir(parents=True,exist_ok=True);(ROOT/dst).write_bytes(raw);saved[label+'_path']=dst;saved[label+'_sha256']=q.raw_sha(raw)
 # All retained evidence bytes are original committed primary files, including raw response.
 if meta.get('raw_sha256'):assert saved['raw_sha256']==meta['raw_sha256']
 if meta.get('text_sha256'):assert saved['text_sha256']==meta['text_sha256']
 if meta.get('response_sha256'):assert saved['raw_sha256']==meta['response_sha256']
 url=meta.get('official_url',meta.get('requested_url',meta.get('url',meta.get('retrieval_url'))))
 assert url and url.startswith('https://'),meta
 s={'source_id':'final86-author-'+key,'source_type':'PUBLIC_OFFICIAL','official_url':url,'source_evidence':saved['raw_path'],'source_evidence_sha256':saved['raw_sha256'],'text_evidence_path':saved['text_path'],'text_evidence_sha256':saved['text_sha256'],'retrieval_metadata_path':saved['metadata_path'],'retrieval_metadata_sha256':saved['metadata_sha256'],'retained_from_commit':BASE,'retained_original_base':base,'law_checked_date':'2026-11-04','author_read_date':'2026-11-04','exact_section':section,'version_or_effective_date_status':version,'retrieval_scope_ko':'실제 감사자의 공식 raw/text/meta 원바이트를 보존하고 저자가 지정 원문을 대조했다. 새 회수나 독립 판정이 아니다.','source_use_manifest':{'source_id':'final86-author-'+key,'source_class':'PUBLIC_OFFICIAL','publisher':'미국 연방 공식기관 또는 Massachusetts DPH/Board','url':url,'access_type':'PUBLIC','authority_level':'PRIMARY_OFFICIAL','permission_status':'VERIFIED','legal_authority_allowed':True,'question_text_storage_allowed':False,'ai_processing_allowed':True,'public_repo_allowed':True,'notes':'SOURCE_USE_POLICY Class A; public official primary bytes; no question text.','last_reviewed':'2026-11-04'}}
 sources[key]=s
retain('pump','a','11','.pdf','Policy2024-02 첫 단락 및 due-diligence 항목','Adopted2024-10-17. 별도 excipient 명문과 독립 효력일은 확인하지 못했다. 2026-11-04 저자 대조.')
retain('recall','b','recall','.html','21 CFR7.3(g)–(n), 특히(l),(m)','eCFR 표시 currency2026-11-02; 2026-11-04 저자 대조. 조항별 최초 효력일 별도 미확정.')
retain('enforcement','b','enforcement','.html','FDA Enforcement Reports: Important Note;pending classification;categorization','FDA page Content current as of2024-05-06. 2026-11-04 저자 대조. 안내 페이지 날짜는 법적 시행일이 아니다.')
retain('qre','c','853b2c5f4d9e57de','.response','247 CMR15.03(2)(a),(b)','Mass.Register1536/2024-12-06 표시; 2026-11-04 저자 대조. 개별 조항 최초 시행일 별도 미확정.')
retain('discipline','c','a864a8e398a1d0b7','.response','247 CMR10.03(1) opening,(g),(k);10.06','Register1546/2025-04-25;10.03(3) 시행표시2025-01-09와 구별. 새 명제 대상(g),(k) 개별 시행일 별도 미확정;2026-11-04 대조.')
retain('ma700','e','a397fe32483f69ac','.raw','105 CMR700.002(B),(C),(D)','공식 통합 PDF에는 Register1514/2024-02-02 등이 있다. 2026-11-04 지정 조항 대조. 각 편입 조항 최초 시행일 별도 미확정.')
for key,name,section in [('cii','b95308609ca5bd38','21 CFR1308.12(b)(1)(i),(vi),(vii),(ix),(xiv);(c)(9),(19),(29);(f)(1)'),('ciii','518d30bed444e571','21 CFR1308.13(b)(2),(6);(c)(11)'),('civ','80f2617da63c92a7','21 CFR1308.14(c)(2),(12),(13),(14),(34),(55),(57)')]:retain(key,'d',name,'.html',section,'eCFR current 표시2026-11-02,2026-11-04 저자 대조. 조항별 최초 효력일 별도 미확정; 정확한 성분·제형 범위만 확인.')
for key,name,date in [('maintena','917a6de9eec0ebef','2026-03-24'),('asimtufii','1470308e6221d464','2025-04-04'),('consta','03a5a2a27731c92e','2025-11-05')]:retain(key,'e',name,'.raw','FDA SPL sections3 Dosage Forms and Strengths;11 Description','FDA SPL effective_time='+date+'; query ≤20261104. 2026-11-04 저자 대조; current marketing/interchangeability 인증 아님.')
for key,name,date in [('perseris','30686d2e83d857bd','2025-01-28'),('uzedy','e0484cb06333674b','2025-10-31')]:retain(key,'e',name,'.raw','NLM DailyMed SPL3 Dosage Forms and Strengths;11 Description','공식 NLM SPL effectiveTime='+date+';2026-11-04 저자 대조. current marketing 또는 제품간 interchangeability 인증 아님.')
retain('vaccine','e','6251c99ae2dd3d1a','.raw','Policy2023-02 IV.A–B','Adopted2023-05-04,revised2025-09-04. 2026-11-04 저자 대조; 별도 최초 시행일 미추정.')
C={};groups={}
def add(uid,suffix,text,keys,section,blocker=None,omission=0):
 C.setdefault(uid,[]).append((suffix,text,keys,section,blocker));groups.setdefault(uid,{}).setdefault(omission,[]).append('FINAL86-CENSUS-'+uid.upper()+'-'+suffix)
add('w5-a-12','EXCIPIENT-ASSESSMENT','Implantable pump의 비약물 첨가제도 실제 체온 환경과 전체 infusion 기간에 대한 안정성·호환성 평가 대상이라는 본문 명제를 별도로 열거한다.',['pump'],'Policy2024-02 첫 단락 및 due-diligence 항목','정책은 drugs/CSP/pump와 온도·전체 infusion을 명시하지만 excipient를 별도 명문으로 열거하지 않는다. 첨가제별 정확한 근거·법적 범위 미확정으로 SOURCE_BLOCKED이며 기존 HOLD를 해제하지 않는다.')
U='recall-classification'
recallblock='본문 학습용 workflow/범위 제한을 독립 열거했다. 21CFR7.3 및 FDA 안내는 일반 정의·분류와 분류 전 개시를 설명하지만 모든 recall의 동일 약국 행위·기한을 명문 의무로 확정하지 않는다. 실제 제품 회수지시·setting·적용법의 추가 대조가 필요하여 SOURCE_BLOCKED. 기존 법규 HOLD/SB를 해제하지 않는다.'
add(U,'CLASSIII-ACTION','Class III라는 이유만으로 해당 회수 통지를 무시하거나 대응을 생략하지 않는다는 본문 행동 명제를 열거한다.',['recall'],'21CFR7.3(m)(3);본문 행동 범위 미확정',recallblock,0)
add(U,'PRECLASSIFICATION-ACTION','FDA가 class를 정하기 전에도 업체의 회수 통지를 방치하지 않는다는 본문 대응 명제를 열거한다.',['enforcement'],'FDA Enforcement Reports Important Note/pending classification',recallblock,1)
for suffix,text in [('LOT-DISTINCTION','Recall class와 affected lot는 서로 다른 정보이다.'),('PROGRESS-DISTINCTION','Recall class와 회수 진행 상태는 서로 다른 정보이다.'),('ACTUAL-HARM-DISTINCTION','Recall class의 위해 가능성과 환자에게 실제 harm이 발생했는지는 서로 다른 정보이다.')]:add(U,suffix,text,['recall','enforcement'],'21CFR7.3(l),(m);FDA Enforcement Reports categorization',None,2)
for suffix,text in [('IDENTIFY-PRODUCT','회수 대상 product를 실제 stock과 대조한다.'),('IDENTIFY-STRENGTH','회수 대상 strength를 실제 stock과 대조한다.'),('IDENTIFY-FORM','회수 대상 dosage form을 실제 stock과 대조한다.'),('IDENTIFY-LOT','회수 대상 lot를 실제 stock과 대조한다.'),('IDENTIFY-EXPIRY','회수 대상 expiry를 실제 stock과 대조한다.'),('QUARANTINE','회수 대상 stock을 격리한다.'),('COMPUTER-BLOCK','회수 대상 stock의 전산 교부를 차단한다.')]:add(U,suffix,'본문의 학습용 recall workflow에서는 '+text,['recall'],'21CFR7.3(l);개별 recall instruction 미확정',recallblock,3)
for suffix,text in [('TRACE-PATIENT','이미 교부된 환자를 추적한다.'),('TRACE-FACILITY','이미 교부된 시설을 추적한다.'),('TRACE-SHIPMENT','이미 배송된 회수 대상 제품을 추적한다.'),('CONTACT','회수 지시에 따라 필요한 연락을 한다.'),('RETURN','회수 지시에 따라 제품 반환을 진행한다.'),('ALTERNATIVE-THERAPY','회수 지시에 따른 대체 치료를 지원한다.'),('RECONCILE','대상 제품 수량을 reconciliation한다.'),('RECORD','회수 대응 과정을 기록한다.'),('BOARD-TRIGGER','해당 Board 의무의 별도 trigger를 검토한다.'),('FDA-TRIGGER','해당 FDA 의무의 별도 trigger를 검토한다.'),('DSCSA-TRIGGER','해당 DSCSA 의무의 별도 trigger를 검토한다.'),('NO-UNIVERSAL-DEADLINE','이 workflow는 모든 recall에 동일한 환자 연락 deadline을 새로 부과하지 않는다.')]:add(U,suffix,'본문의 학습용 recall workflow에서는 '+text,['recall','enforcement'],'21CFR7.3(l);개별 instruction/적용법 추가 대조 필요',recallblock,4)
add('parallel-duties','CREATE-QRE-RECORD','해당 QRE를 발견했거나 통지받은 약사는 내부 QRE record를 작성해야 하며, 같은 사건의 다른 통지·보고·제품 disposition과 병렬로 적용될 수 있다.',['qre'],'247 CMR15.03(2)(a),(b)')
add('w1-c-14','EMPLOYER-NO-IMMUNITY','실제 업무 능력이 손상되거나 안전하지 않은 practice를 고용주가 승인했다는 사실이 247 CMR10.03(1)(g),(k)의 징계 사유를 면제하지 않는다.',['discipline'],'247 CMR10.03(1) opening,(g),(k);10.06')
Drows={
 'appendix-a-2':[(6,'Hydrocodone 단일성분 Hysingla ER','II','cii','21CFR1308.12(b)(1)(vi)'),(7,'Hydrocodone/acetaminophen Norco·Vicodin·Lortab','II','cii','21CFR1308.12(b)(1)(vi)'),(8,'Oxycodone OxyContin·Roxicodone','II','cii','21CFR1308.12(b)(1)(xiv)'),(9,'Oxycodone/acetaminophen Percocet','II','cii','21CFR1308.12(b)(1)(xiv)'),(10,'Morphine MS Contin·Roxanol','II','cii','21CFR1308.12(b)(1)(ix)'),(11,'Hydromorphone Dilaudid','II','cii','21CFR1308.12(b)(1)(vii)'),(13,'Fentanyl transdermal Duragesic','II','cii','21CFR1308.12(c)(9)'),(15,'Meperidine Demerol','II','cii','21CFR1308.12(c)(19)'),(16,'Tapentadol Nucynta·Nucynta ER','II','cii','21CFR1308.12(c)(29)')],
 'appendix-a-3':[(19,'Nabilone Cesamet','II','cii','21CFR1308.12(f)(1)')],
 'appendix-a-5':[(33,'Perampanel Fycompa','III','ciii','21CFR1308.13(c)(11)'),(34,'Benzphetamine Didrex','III','ciii','21CFR1308.13(b)(2)'),(35,'Phendimetrazine Bontril','III','ciii','21CFR1308.13(b)(6)')],
 'appendix-a-7':[(39,'Alprazolam Xanax','IV','civ','21CFR1308.14(c)(2)'),(40,'Clonazepam Klonopin','IV','civ','21CFR1308.14(c)(13)'),(42,'Lorazepam Ativan','IV','civ','21CFR1308.14(c)(34)'),(44,'Temazepam Restoril','IV','civ','21CFR1308.14(c)(55)'),(45,'Triazolam Halcion','IV','civ','21CFR1308.14(c)(57)'),(47,'Clorazepate Tranxene','IV','civ','21CFR1308.14(c)(14)'),(48,'Clobazam Onfi·Sympazan','IV','civ','21CFR1308.14(c)(12)')]}
for uid,rows in Drows.items():
 for oi,(n,drug,sched,key,clause) in enumerate(rows):add(uid,f'A{n:03}-MA-SCHEDULE',f'A{n:03}의 {drug} 해당 제품은 MA Schedule {sched}에 편입되는 분류이다.',['ma700',key],'105CMR700.002('+{'II':'B','III':'C','IV':'D'}[sched]+');'+clause,None,oi)
add('appendix-a-2','A017-FEDERAL-CII','A017 단일성분 codeine의 연방 schedule은 II이다. 적격 복합제의 별도 schedule 조건을 단일성분에 적용하지 않는다.',['cii'],'21CFR1308.12(b)(1)(i)',None,9)
add('appendix-b-5','B035-FORMULATION','B035의 Abilify Maintena와 Abilify Asimtufii는 서로 다른 formulation의 LAI 제품이므로 구별해야 한다.',['maintena','asimtufii'],'각 FDA SPL3 Dosage Forms and Strengths;11 Description',None,0)
add('appendix-b-5','B038-LAI','B038의 Risperdal Consta·Perseris·Uzedy는 risperidone long-acting injectable 제품들을 다루는 행이다.',['consta','perseris','uzedy'],'각 FDA/NLM SPL3/11의 extended-release/long-acting injectable 제형',None,1)
add('appendix-b-6','B047-ACTUAL-ORDER','백신 접종 후 adverse event를 관리하기 위해 epinephrine 등 emergency medication을 실제 투여하려면 그 약에 대한 prescription 또는 standing order가 필요하다.',['vaccine'],'Policy2023-02 IV.B')
packets={ab:json.loads(Path('/workspace/scratch/notes-final86-'+ab+'-visible-input.json').read_bytes())for ab in 'abcde'}
inputs={x['unit']['id']:x for d in packets.values()for x in d['units']};index=[]
for uid,adds in C.items():
 x=inputs[uid];b=x['binding'];raw=blob(b['census_path']);assert q.raw_sha(raw)==b['census_sha256'];old=json.loads(raw)
 oldclaims=[c for c in old['claims']if c['unit_id']==uid];assert oldclaims==x['claims'];assert {c['claim_id']:q.digest(c)for c in oldclaims}==b['claim_record_sha256s'];assert q.raw_sha(x['unit']['body'].encode())==b['body_sha256']
 oldunit=next(u for u in old['units']if u['unit_id']==uid);assert q.digest(oldunit)==b['census_unit_record_sha256']
 claims=copy.deepcopy(oldclaims);ss=copy.deepcopy(old['sources']);added=[]
 for suffix,text,keys,section,blocker in adds:
  cid='FINAL86-CENSUS-'+uid.upper()+'-'+suffix;added.append(cid)
  source=copy.deepcopy(sources[keys[0]])
  claim={'claim_id':cid,'unit_id':uid,'unit_content_sha256':b['body_sha256'],'statement_ko':text,'record_granularity':'AUTHOR_ENUMERATED_ATOMIC_PROPOSITION','legal_claim_kind':'MATERIAL_NOTE_PROPOSITION','is_complete_atomic_enumeration_evidence':True,'review_status':'SOURCE_BLOCKED'if blocker else'AUTHOR_SOURCE_CHECKED','source_id':source['source_id'],'authority_clauses':[section],'checked_at':'2026-11-04','related_question_ids':[],'blocker':blocker,'author_provenance':AUTHOR,'independent':False,'verification_scope_ko':'누락 명제의 저자 열거 및 지정 1차 조항 대조이며 독립 법규 PASS·question·release 근거가 아니다.','supporting_source_ids':[sources[k]['source_id']for k in keys],'supporting_authorities':[copy.deepcopy(sources[k])for k in keys]}
  for k in keys:ss[sources[k]['source_id']]=copy.deepcopy(sources[k])
  for key in ['official_url','source_evidence','source_evidence_sha256','text_evidence_path','text_evidence_sha256','retrieval_metadata_path','retrieval_metadata_sha256','law_checked_date','version_or_effective_date_status']:claim[key]=source[key]
  claims.append(claim)
 newunit=copy.deepcopy(oldunit);newunit.update(claim_count=len(claims),source_checked_claim_count=sum(c['review_status']=='AUTHOR_SOURCE_CHECKED'for c in claims),source_blocked_claim_count=sum(c['review_status']=='SOURCE_BLOCKED'for c in claims),independent_verified_claim_count=0,independent_completeness_status='PENDING')
 census={'schema_version':1,'purpose':'CENSUS_ONLY_OMISSION_REASSESSMENT','stage':'AUTHOR_PROPOSAL_PENDING_INDEPENDENT_REASSESSMENT','author_provenance':AUTHOR,'reviewed_at':'2026-11-04','independent_audit':False,'canonical_release_credit':0,'question_audit_credit':0,'body_mutated':False,'sources':ss,'units':[newunit],'claims':claims}
 cp=P+uid+'-census.json';csha=write(cp,census)
 assert all(q.digest(c)==q.digest(claims[i])for i,c in enumerate(oldclaims));assert all(q.digest(v)==q.digest(ss[k])for k,v in old['sources'].items())
 assert all(' '.join(c['statement_ko'].split())not in {' '.join(z['statement_ko'].split())for z in oldclaims}for c in claims[len(oldclaims):])
 dst=ROOT/(P+'bodies/'+uid+'.txt');dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(x['unit']['body'].encode())
 index.append({'unit_id':uid,'body_sha256':b['body_sha256'],'original_binding':b,'original_claim_count':len(oldclaims),'proposed_claim_count':len(claims),'added_claim_ids':added,'omission_claim_groups':[groups[uid][i]for i in sorted(groups[uid])],'changed_claim_ids':[],'original_claims_canonical_preserved':True,'all_original_sources_canonical_preserved':True,'census_path':cp,'census_sha256':csha})
write(P+'preparation-index.json',{'author_provenance':AUTHOR,'canonical_release_credit':0,'question_audit_credit':0,'independent_audit_credit':0,'original_claim_count':sum(r['original_claim_count']for r in index),'proposed_claim_count':sum(r['proposed_claim_count']for r in index),'records':index,'packet_sha256s':{ab:q.raw_sha(Path('/workspace/scratch/notes-final86-'+ab+'-visible-input.json').read_bytes())for ab in 'abcde'}})
write(P+'retained-primary-source-manifest.json',sources)
print([(r['unit_id'],r['original_claim_count'],r['proposed_claim_count'])for r in index])
