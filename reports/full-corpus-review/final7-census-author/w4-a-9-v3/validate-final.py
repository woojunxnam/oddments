"""Actual W4-A-9 V3 native validation with immutable author and independent-status axes."""
import json,subprocess,sys,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT/'scripts'))
import note_review_queue as q
import notes_census_reassessment as nr
P='reports/full-corpus-review/final7-census-author/w4-a-9-v3/'
BASE='f543edaae39f8bb64f29ff2bac16e23f84e90a13';DRAFT='8e72e87a'
def blob(c,p):return subprocess.check_output(['git','show',c+':'+p],cwd=ROOT)
def write(p,o):(ROOT/p).write_bytes(q.encoded(o))
paths={}
def read(path,sha=None):
 if path not in paths:
  raw=(ROOT/path).read_bytes();assert raw==blob('HEAD',path);paths[path]=q.raw_sha(raw)
 if sha:assert paths[path]==sha
 return (ROOT/path).read_bytes()
def auth(obj):
 if isinstance(obj,list):
  for v in obj:auth(v)
 elif isinstance(obj,dict):
  for k,v in obj.items():
   if k.endswith('_path')and isinstance(v,str)and obj.get(k[:-5]+'_sha256'):read(v,obj[k[:-5]+'_sha256'])
   if k=='source_evidence'and isinstance(v,str)and obj.get('source_evidence_sha256'):read(v,obj['source_evidence_sha256'])
   if isinstance(v,(dict,list)):auth(v)
index=json.loads(read(P+'final-proposal-index.json'));rec=json.loads(read(index['record_path'],index['record_sha256']));state=json.loads(read(q.STATE));assert read(q.STATE)==blob(BASE,q.STATE);q.validate_state(state)
g=json.loads(read(P+'own-head-strict-native-inventory-proof.json'));assert g['source_guard_passed']is True
raw=read(P+'own-head-strict-native-inventory.json',g['inventory_raw_sha256']);inv=json.loads(raw);ledger=read(q.LEDGER,inv['ledger_sha256']);notes=inv['notes'];current=q.inventory(ROOT,notes,ledger_raw=ledger);assert current['total_units']==306 and current['units']==inv['units']
bodies={u['id']:u['body']for ch in notes['chapters']for u in ch['units']};assert len(bodies)==306
for uid,b in inv['units'].items():assert q.raw_sha(bodies[uid].encode())==b['body_sha256'];read(b['census_path'],b['census_sha256'])
old=json.loads(read(rec['previous_binding']['census_path'],rec['previous_binding']['census_sha256']));new=json.loads(read(index['census_path'],index['census_sha256']));draft=json.loads(read(P+'census.json'));assert len(old['claims'])==32 and len(new['claims'])==34 and new['claims']==draft['claims']and new['sources']==draft['sources'];assert all(q.digest(a)==q.digest(b)for a,b in zip(old['claims'],new['claims']))and all(q.digest(s)==q.digest(new['sources'][sid])for sid,s in old['sources'].items());assert rec['changed_claim_ids']==[]and rec['claim_mapping']=={c['claim_id']:[c['claim_id']]for c in old['claims']}
assert read(P+'body.txt')==bodies['w4-a-9'].encode()and q.raw_sha(bodies['w4-a-9'].encode())==rec['body_sha256'];assert all(c['review_status']=='SOURCE_BLOCKED'for c in new['claims'][32:])
job=next(j for j in state['jobs']if j['job_id']==rec['previous_job_id']);assert job['sequence']==76 and job['status']=='INTEGRATED';report=json.loads(read(rec['previous_report']['path'],rec['previous_report']['raw_sha256']));read(rec['previous_result']['path'],rec['previous_result']['raw_sha256'])
for p,sha in q.validate_evidence(job,job['result'],report):read(p,sha)
auth(new);auth(report)
dpaths=subprocess.check_output(['git','ls-tree','-r','--name-only',DRAFT,'--',P],cwd=ROOT,text=True).splitlines();assert len(dpaths)==16
for p in dpaths:assert read(p)==blob(DRAFT,p)
sourceproof=[]
for key,s in json.loads(read(P+'retained-primary-source-manifest.json')).items():
 rr=read(s['source_evidence'],s['source_evidence_sha256']);tt=read(s['text_evidence_path'],s['text_evidence_sha256']);mm=read(s['retrieval_metadata_path'],s['retrieval_metadata_sha256']);m=json.loads(mm);assert m['raw_sha256']==q.raw_sha(rr)and m['status_code']==200 and m['requested_at_utc']<=m['completed_at_utc']
 pdf=rr.startswith(b'%PDF-')
 if pdf:assert subprocess.check_output(['pdftotext','-layout','-','-'],input=rr)==tt
 else:assert all(z in rr for z in [b'Methadone',b'Fentanyl',b'Codeine'])
 for ext,bb in [('.raw',rr),('.txt',tt),('.meta.json',mm)]:assert bb==blob(s['retained_from_commit'],s['retained_original_base']+ext)==read(s['retained_original_base']+ext)
 sourceproof.append({'source_key':key,'official_url':s['official_url'],'exact_section':s['exact_section'],'raw_sha256':q.raw_sha(rr),'text_sha256':q.raw_sha(tt),'metadata_sha256':q.raw_sha(mm),'raw_format':'PDF'if pdf else'OFFICIAL_HTML','raw_pdf_reextracted_text_equals_saved_text':True if pdf else None,'original_get_started_at_utc':m['requested_at_utc'],'original_get_completed_at_utc':m['completed_at_utc'],'author_read_date':s['author_read_date'],'version_or_effective_date_status':s['version_or_effective_date_status'],'original_worker_commit_equals_own_HEAD_equals_disk':True,'new_retrieval':False})
binding,carried=nr.validate_record(state,rec,ROOT,notes,nr.disk_reader(ROOT));assert len(binding['claim_record_sha256s'])==34 and len(carried)==10 and rec['author_provenance']['actor_id']in binding['known_author_ids']
row=next(r for r in report['records']if r['unit_id']=='w4-a-9');assert len(row['omissions'])==2 and set(carried)=={c['claim_id']for c in row['claims']if c['legal_status']!='KEEP'}
for i,(om,res)in enumerate(zip(row['omissions'],rec['omission_resolutions'])):assert q.raw_sha(om.encode())==res['omission_sha256']and res['claim_ids']==[new['claims'][32+i]['claim_id']]
newbase=g['own_head'];changed=subprocess.check_output(['git','diff','--name-only',newbase,'HEAD'],cwd=ROOT,text=True).splitlines();assert changed and all(p.startswith(P)for p in changed)
branchdiff=subprocess.check_output(['git','diff','--name-only',BASE,'HEAD'],cwd=ROOT,text=True).splitlines();historical=[p for p in branchdiff if not p.startswith(P)]
for p in historical:assert any(p.startswith(prefix)for prefix in ['reports/full-corpus-review/final19-census-author/','reports/full-corpus-review/notes120-census-author/','reports/full-corpus-review/final86-census-author/'])and read(p)==blob(DRAFT,p)
prior=[p for p in subprocess.check_output(['git','diff','--name-only',DRAFT,'HEAD','--','reports/full-corpus-review/final19-census-author/','reports/full-corpus-review/notes120-census-author/','reports/full-corpus-review/final86-census-author/'],cwd=ROOT,text=True).splitlines()if not p.startswith(P)];assert not prior
head=q.git(ROOT,'rev-parse','HEAD');at=datetime.datetime.now(datetime.timezone.utc).isoformat()
write(P+'native-final-validation.json',{'validation_head':head,'validated_at_utc':at,'native_validate_record':'PASSED','real_disk_reader_used':True,'root_state_commit':BASE,'own_actual_source_guard_passed':True,'own_guard_head':g['own_head'],'own_full_native_inventory_raw_sha256':q.raw_sha(raw),'full306_native_inventory_recomputed':True,'all306_body_hashes_reconfirmed':True,'method_ko':'자체fullcheckout의actualq.inventory(root)→load_notes(root)전체guard를통과했다.해당306notes/inventory를커밋보존하고자체실제ledger/census로전량재확인한뒤실제validate_record+unmodifieddisk_reader를실행했다. rootlivecontext/임의projection/가짜ledger/guard완화/모킹/등록없음.','replacement_binding':binding,'carried_legal_blockers':carried,'carried_legal_blocker_claim_count':10,'original_author_source_blocked_ids':[c['claim_id']for c in old['claims']if c['review_status']=='SOURCE_BLOCKED'],'new_author_source_blocked_ids':[c['claim_id']for c in new['claims']if c['review_status']=='SOURCE_BLOCKED'],'expected_registration_exclusion_union':sorted(set(job['known_author_ids'])|set(rec['previous_binding']['known_author_ids'])|set(binding['known_author_ids'])),'controller_registration_performed':False,'independent_credit':0,'legal_pass_credit':0,'release_credit':0})
write(P+'final-preservation-and-source-proof.json',{'validation_head':head,'validated_at_utc':at,'all32_original_claims_canonical_preserved':True,'original_claim_canonical_sha256s':{c['claim_id']:q.digest(c)for c in old['claims']},'all_original_sources_canonical_preserved':True,'original_source_canonical_sha256s':{k:q.digest(s)for k,s in old['sources'].items()},'body_bytes_preserved':True,'body_sha256':rec['body_sha256'],'original_claim_count':32,'final_claim_count':34,'added_author_source_checked':0,'added_source_blocked':2,'changed_claim_ids':[],'all8e72_draft16_files_byte_immutable':dpaths,'two_original_omission_sha_to_two_new_directional_atoms_verified':True,'author_source_status_and_actual_10_independent_blockers_separate':True,'source_checks':sourceproof,'all_reference_HEAD_equals_disk':True,'reference_count':len(paths),'reference_path_sha256s':paths,'new_author_scope_base':newbase,'new_authored_paths_all_unique_prefix':changed,'branch_difference_from_root_base':branchdiff,'unchanged_carried_prior_author_history_paths':historical,'all_prior_seven_V2_and_older_census_source_histories_byte_immutable':True,'shared_queue_ledger_body_oldcensus_report_generated_guard_mutations':0,'controller_registration_performed':False,'independent_credit':0,'legal_pass_credit':0,'release_credit':0})
print('W4-A-9 V3 actualnative PASSED; inherited10 retained; references',len(paths),'HEAD==disk; priorauthorhistory unchanged')
