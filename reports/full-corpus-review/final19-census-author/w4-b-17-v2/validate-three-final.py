"""Real native validation for three integrated parents; zero independent/release credit."""
import json,subprocess,sys,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT/'scripts'))
import note_review_queue as q
import notes_census_reassessment as nr
P='reports/full-corpus-review/final19-census-author/w4-b-17-v2/'
BASE='b19b58cfd56699fc62e0723b9ded621f73c45866'
EXPECTED={'w4-b-17':(41,43,25,2,0,'89a5658c353d84b6d5f46616b47d35671272c8b5',16),'w5-a-12':(17,18,2,0,1,'8241687fad2a96e21950b3fbfbddae02399d5a65',13),'parallel-duties':(10,12,1,0,2,'8241687fad2a96e21950b3fbfbddae02399d5a65',22)}
def blob(c,p):return subprocess.check_output(['git','show',c+':'+p],cwd=ROOT)
def write(p,obj):(ROOT/p).write_bytes(q.encoded(obj))
paths={}
def read(path,sha=None):
 if path not in paths:
  raw=(ROOT/path).read_bytes();assert raw==blob('HEAD',path);paths[path]=q.raw_sha(raw)
 if sha:assert paths[path]==sha
 return (ROOT/path).read_bytes()
def authority_paths(obj):
 if isinstance(obj,list):
  for c in obj:authority_paths(c)
 elif isinstance(obj,dict):
  for k,v in obj.items():
   if k.endswith('_path')and isinstance(v,str)and obj.get(k[:-5]+'_sha256'):read(v,obj[k[:-5]+'_sha256'])
   if k=='source_evidence'and isinstance(v,str)and obj.get('source_evidence_sha256'):read(v,obj['source_evidence_sha256'])
   if isinstance(v,(list,dict)):authority_paths(v)
index=json.loads(read(P+'bundle-final-index.json'));state=json.loads(read(q.STATE));assert read(q.STATE)==blob(BASE,q.STATE);q.validate_state(state)
guard=json.loads(read(P+'bundle-own-head-strict-native-inventory-proof.json'));assert guard['source_guard_passed']is True
invraw=read(P+'bundle-own-head-strict-native-inventory.json',guard['inventory_raw_sha256']);inv=json.loads(invraw);ledger=read(q.LEDGER,inv['ledger_sha256']);notes=inv['notes'];actual=q.inventory(ROOT,notes,ledger_raw=ledger);assert actual['total_units']==306 and actual['units']==inv['units']
bodies={u['id']:u['body']for ch in notes['chapters']for u in ch['units']};assert len(bodies)==306
for uid,b in inv['units'].items():assert q.raw_sha(bodies[uid].encode())==b['body_sha256'];read(b['census_path'],b['census_sha256'])
out=[];pres=[]
for item in index['records']:
 uid=item['unit_id'];nold,nnew,ncarried,nsb,nchecked,draftcommit,draftcount=EXPECTED[uid];prefix='reports/full-corpus-review/final19-census-author/'+uid+'-v2/'
 rec=json.loads(read(item['record_path'],item['record_sha256']));new=json.loads(read(item['census_path'],item['census_sha256']));draft=json.loads(read(prefix+'census.json'));old=json.loads(read(rec['previous_binding']['census_path'],rec['previous_binding']['census_sha256']));assert len(old['claims'])==nold and len(new['claims'])==nnew and new['claims']==draft['claims']and new['sources']==draft['sources']
 assert all(q.digest(a)==q.digest(b)for a,b in zip(old['claims'],new['claims']))and all(q.digest(s)==q.digest(new['sources'][sid])for sid,s in old['sources'].items());assert rec['changed_claim_ids']==[]and rec['claim_mapping']=={c['claim_id']:[c['claim_id']]for c in old['claims']}
 assert read(prefix+'body.txt')==bodies[uid].encode()and q.raw_sha(bodies[uid].encode())==rec['body_sha256']
 appended=new['claims'][nold:];assert sum(c['review_status']=='SOURCE_BLOCKED'for c in appended)==nsb and sum(c['review_status']=='AUTHOR_SOURCE_CHECKED'for c in appended)==nchecked
 job=next(j for j in state['jobs']if j['job_id']==rec['previous_job_id']);report=json.loads(read(rec['previous_report']['path'],rec['previous_report']['raw_sha256']));read(rec['previous_result']['path'],rec['previous_result']['raw_sha256'])
 for path,sha in q.validate_evidence(job,job['result'],report):read(path,sha)
 authority_paths(new);authority_paths(report)
 dpaths=subprocess.check_output(['git','ls-tree','-r','--name-only',draftcommit,'--',prefix],cwd=ROOT,text=True).splitlines();assert len(dpaths)==draftcount
 for path in dpaths:assert read(path)==blob(draftcommit,path)
 sp=[]
 for key,s in json.loads(read(prefix+'retained-primary-source-manifest.json')).items():
  raw=read(s['source_evidence'],s['source_evidence_sha256']);text=read(s['text_evidence_path'],s['text_evidence_sha256']);metaraw=read(s['retrieval_metadata_path'],s['retrieval_metadata_sha256']);meta=json.loads(metaraw)
  assert q.raw_sha(raw)==meta.get('raw_sha256',meta.get('response_sha256'))and meta.get('status_code',meta.get('http_status',meta.get('status')))==200
  ext=s['retained_raw_extension'];pdf=raw.startswith(b'%PDF-')
  if pdf:assert subprocess.check_output(['pdftotext','-layout','-','-'],input=raw)==text
  for suffix,current in [(ext,raw),('.txt',text),('.meta.json',metaraw)]:assert current==blob(s['retained_from_commit'],s['retained_original_base']+suffix)==read(s['retained_original_base']+suffix)
  start=meta.get('requested_at_utc',meta.get('request_started_at',meta.get('attempted_at')));end=meta.get('completed_at_utc',meta.get('retrieved_at'));assert start and (not end or start<=end)
  if s.get('original_auditor_reread_metadata_path'):
   rr=read(s['original_auditor_reread_metadata_path'],s['original_auditor_reread_metadata_sha256']);assert rr==blob(s['retained_from_commit'],s['retained_original_base']+'.reread.json')
  sp.append({'source_key':key,'official_url':s['official_url'],'exact_section':s['exact_section'],'raw_sha256':q.raw_sha(raw),'text_sha256':q.raw_sha(text),'metadata_sha256':q.raw_sha(metaraw),'original_get_started_at_utc':start,'original_get_completed_at_utc':end,'missing_completed_timestamp_not_replaced_with_reread':end is None,'raw_pdf_reextraction_equals_saved_text':True if pdf else None,'raw_format':'PDF'if pdf else'OFFICIAL_HTML','original_worker_commit_equals_own_HEAD_equals_disk':True,'author_read_date':s['author_read_date'],'version_or_effective_date_status':s['version_or_effective_date_status'],'new_retrieval':False})
 binding,carried=nr.validate_record(state,rec,ROOT,notes,nr.disk_reader(ROOT));assert len(binding['claim_record_sha256s'])==nnew and len(carried)==ncarried and rec['author_provenance']['actor_id']in binding['known_author_ids']
 row=next(r for r in report['records']if r['unit_id']==uid);assert set(carried)=={c['claim_id']for c in row['claims']if c['legal_status']!='KEEP'}and len(row['omissions'])==len(rec['omission_resolutions'])
 for i,(o,res)in enumerate(zip(row['omissions'],rec['omission_resolutions'])):assert q.raw_sha(o.encode())==res['omission_sha256']and res['claim_ids']==[appended[i]['claim_id']]
 out.append({'unit_id':uid,'native_validate_record':'PASSED','real_disk_reader_used':True,'replacement_binding':binding,'carried_legal_blockers':carried,'carried_legal_blocker_claim_count':len(carried),'original_author_source_blocked_ids':[c['claim_id']for c in old['claims']if c['review_status']=='SOURCE_BLOCKED'],'new_author_source_blocked_ids':[c['claim_id']for c in new['claims']if c['review_status']=='SOURCE_BLOCKED'],'expected_registration_exclusion_union':sorted(set(job['known_author_ids'])|set(rec['previous_binding']['known_author_ids'])|set(binding['known_author_ids']))})
 pres.append({'unit_id':uid,'original_claim_count':nold,'final_claim_count':nnew,'added_source_blocked':nsb,'added_author_source_checked':nchecked,'all_original_claim_canonical_sha256s':{c['claim_id']:q.digest(c)for c in old['claims']},'all_original_source_canonical_sha256s':{k:q.digest(s)for k,s in old['sources'].items()},'all_original_claims_sources_body_preserved':True,'body_sha256':rec['body_sha256'],'original_draft_commit':draftcommit,'all_original_draft_files_byte_immutable':dpaths,'changed_claim_ids':[],'exact_original_omission_mapping_verified':True,'author_status_and_independent_legal_blockers_are_separate_axes':True,'source_checks':sp})
changed=subprocess.check_output(['git','diff','--name-only',BASE,'HEAD'],cwd=ROOT,text=True).splitlines();assert changed and all(any(path.startswith('reports/full-corpus-review/final19-census-author/'+u+'-v2/')for u in EXPECTED)for path in changed)
assert subprocess.check_output(['git','diff','--name-only','89a5658c','HEAD','--','reports/full-corpus-review/final19-census-author/w3-d-22-v2/','reports/full-corpus-review/final19-census-author/w4-a-9-v2/','reports/full-corpus-review/notes120-census-author/','reports/full-corpus-review/final86-census-author/'],cwd=ROOT)==b''
head=q.git(ROOT,'rev-parse','HEAD');at=datetime.datetime.now(datetime.timezone.utc).isoformat()
for item,native,proof in zip(index['records'],out,pres):
 prefix='reports/full-corpus-review/final19-census-author/'+item['unit_id']+'-v2/'
 write(prefix+'native-final-validation.json',{'validation_head':head,'validated_at_utc':at,**native,'own_actual_source_guard_passed':True,'full306_native_inventory_recomputed':True,'own_guard_inventory_sha256':q.raw_sha(invraw),'controller_registration_performed':False,'independent_credit':0,'legal_pass_credit':0,'release_credit':0})
 write(prefix+'final-preservation-and-source-proof.json',{'validation_head':head,'validated_at_utc':at,**proof,'controller_registration_performed':False,'independent_credit':0,'release_credit':0})
write(P+'bundle-native-final-validation.json',{'validation_head':head,'validated_at_utc':at,'root_state_commit':BASE,'own_actual_source_guard_proof':P+'bundle-own-head-strict-native-inventory-proof.json','own_full_native_inventory_raw_sha256':q.raw_sha(invraw),'all306_body_hashes_reconfirmed':True,'method_ko':'자체전체checkout의actualq.inventory(root)→load_notes(root)전체guard를통과한306notes/inventory를보존했다.그notes와자체HEAD실제ledger/census전량으로inventory를재확인하고실제validate_record+unmodifieddisk_reader를호출했다. liveROOT/contextoverride/guard완화/모킹/등록없음.','records':out,'controller_registration_performed':False,'independent_credit':0,'legal_pass_credit':0,'release_credit':0})
write(P+'bundle-preservation-and-source-proof.json',{'validation_head':head,'validated_at_utc':at,'records':pres,'all_reference_HEAD_equals_disk':True,'reference_count':len(paths),'reference_path_sha256s':paths,'all_authored_paths_in_three_unique_prefixes':changed,'original_A32_B19_old9_final86_byte_immutable':True,'shared_queue_ledger_body_oldcensus_report_generated_guard_mutations':0,'controller_registration_performed':False,'independent_credit':0,'release_credit':0})
print([(r['unit_id'],r['native_validate_record'],r['carried_legal_blocker_claim_count'])for r in out],len(paths),'HEAD==disk')
