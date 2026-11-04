import json,pathlib,hashlib,sys,subprocess,datetime,copy,collections
w=pathlib.Path('/workspace/census-reassessment-e2');ctl=pathlib.Path('/workspace/oddments');pre='reports/full-corpus-review/independent-notes/reassessment-e2-';ep=pre+'evidence';e=w/ep;rel=pre+'review.json';sys.path.insert(0,str(ctl/'scripts'));import note_review_queue as nq;from notes_revision import load_notes
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text())
j=load(pathlib.Path('/tmp/census-reassessment-e2-assignment.json'));d=load(w/rel);assert j['unit_ids']==['w1-c-1'];r=d['records'][0];b=j['unit_bindings']['w1-c-1'];assert r['binding']==b
inv=nq.inventory(ctl);state=load(ctl/nq.STATE);nq.validate_state(state,ctl);nq.current(j,inv,state);nq.validate_reassessments(state,inv,ctl);assert inv['units']['w1-c-1']==b
assert nq.git(ctl,'show','HEAD:'+b['census_path'],binary=True)==(ctl/b['census_path']).read_bytes()
assert sha(ctl/b['census_path'])==sha(w/b['census_path'])==sha(e/'final-census-source-snapshot.json')==b['census_sha256']
census=load(w/b['census_path']);assert len(census['claims'])==34 and nq.digest(census['units'][0])==b['census_unit_record_sha256'];assert {c['claim_id']:nq.digest(c)for c in census['claims']}==b['claim_record_sha256s']
for root in [w,ctl]:
 unit=next(u for c in load_notes(root)['chapters']for u in c['units']if u['id']=='w1-c-1');assert hashlib.sha256(unit['body'].encode()).hexdigest()==b['body_sha256']
body=load(e/'body-first-snapshot.json');assert body['unit']['body']==unit['body'] and body['body_sha256']==b['body_sha256']
assert d['actor_provenance']==j['actor_provenance']=={'actor_id':'/root/independent_case_e','session_id':'/root/independent_case_e'}
assert d['auditor']==j['auditor']=='GPT' and d['auditor_instance']==j['auditor_instance']=='gpt-independent-session-root-independent_case_e-20261103'
assert all(d[k]==0 for k in ['canonical_release_credit','question_audit_credit','author_review_credit']) and d['canonical_audit']is False
assert d['reviewed_at']==datetime.datetime.now(datetime.timezone.utc).date().isoformat()=='2026-11-04'
assert r['reassessment_review']=={**j['reassessment_review'],'final_census_read_completely':True,'all_original_omissions_reassessed':True,'all_original_propositions_preserved':True}
vr=load(e/'version-record-source-snapshot.json');assert sha(e/'version-record-source-snapshot.json')==j['reassessment_record_sha256'];assert nq.git(ctl,'show','HEAD:reports/full-corpus-review/census-corrections/v3/record/w1-c-1-census-v3-record.json',binary=True)==(e/'version-record-source-snapshot.json').read_bytes()
old=load(ctl/vr['previous_binding']['census_path']);oldclaims={x['claim_id']:x for x in old['claims']if x['unit_id']=='w1-c-1'};newclaims={x['claim_id']:x for x in census['claims']};assert len(oldclaims)==32
for cid,c in oldclaims.items():assert newclaims[cid]==c and vr['claim_mapping'][cid]==[cid]
assert set(newclaims)-set(oldclaims)==set(vr['added_claim_ids']) and not vr['changed_claim_ids']
originalverification=load(e/'final-binding-and-original-omission-verification.json');assert sha(ctl/vr['previous_report']['path'])==vr['previous_report']['raw_sha256'];assert sha(ctl/vr['previous_result']['path'])==vr['previous_result']['raw_sha256'];assert sha(ctl/vr['previous_binding']['census_path'])==vr['previous_binding']['census_sha256']
assert originalverification['carried_legal_blockers_exact']==j['carried_legal_blockers']=={'w1-c-1':{}}
assert {x['sha256']for x in originalverification['original_omissions']}=={x['omission_sha256']for x in j['reassessment_review']['omission_resolutions']}
for o in originalverification['original_omissions']:assert hashlib.sha256(o['text'].encode()).hexdigest()==o['sha256']
assert r['completeness']=='COMPLETE' and r['omissions']==[] and r['legal_status']=='KEEP';assert len(r['claims'])==34
used=set()
for c in r['claims']:
 assert c['claim_record_sha256']==b['claim_record_sha256s'][c['claim_id']] and c['statement_ko']==newclaims[c['claim_id']]['statement_ko']
 assert c['claim_read_completely']and c['entire_final_claim_json_read'] and c['legal_status']=='KEEP'and c['blocker']is None
 assert c['inherited_legal_blockers']==j['carried_legal_blockers']['w1-c-1'].get(c['claim_id'],[])
 for a in c['authorities']:
  assert a['source_type']=='PUBLIC_OFFICIAL'and a['official_url'].startswith('https://')and a['exact_section']and a['version_or_effective_date_status']
  assert a['law_checked_date']=='2026-11-04'and a['retrieved_at_utc'].startswith('2026-11-04')
  assert a['evidence_path'].startswith(ep+'/')and sha(w/a['evidence_path'])==a['evidence_sha256'];used.add(a['evidence_path'])
assert {c['claim_id']for c in r['claims']if c['historical_author_status']=='SOURCE_BLOCKED'}==set(b['source_blocked_claim_ids'])
assert not any('mgl94c-31' in p for p in used)
assert len(used)==7
assert len(d['sources'])==9 and all(s['http_status']==200 and s['fresh_live_retrieval']and not s['same_day_cache_reuse']and not s['old_Nov3_cache_reuse']for s in d['sources'])
for s in d['sources']:
 assert sha(w/s['raw_path'])==s['raw_sha256']and sha(w/s['extracted_text_path'])==s['extracted_text_sha256']
 assert s['retrieved_at_utc'].startswith('2026-11-04')
 if s['raw_path'].endswith('.pdf'):assert (w/s['raw_path']).read_bytes().startswith(b'%PDF')
coverage=load(e/'body-to-final-census-coverage.json');assert coverage['inventory_count']==len(coverage['items'])==40 and coverage['final_inventory_mapping_complete']
assert set(cid for x in coverage['items']for cid in x['final_census_claim_ids'])==set(newclaims)
assert all(x['coverage']=='COVERED_AS_STATED_OR_COMPOUND_CONTENT'and x['final_census_claim_ids']for x in coverage['items']) and not coverage['actual_new_omissions_found']
# Original question payloads are current and whitelisted; only unit alignment is assessed.
pack=load(e/'related-question-visible-input.json');cat=load(e/'related-question-exact-text-catalog.json');assert len(pack['records'])==len(cat['question_maps'])==80 and len(cat['catalog'])==648
config=load(ctl/'site/practice-expansion/publication.json');ps=['practice_expansion/2026-10-23/candidates/questions.json']+[x['path']for x in config['additional_banks']];bank={}
for p in ps:
 for q in load(ctl/p)['questions']:bank[q['question_id']]=q
for p in sorted((ctl/'data/questions').glob('*.json')):
 q=load(p);bank[q['question_id']]=q
assert len(bank)==439+2346
by={}
for x in pack['records']:
 q=bank[x['question_id']];v={k:q[k]for k in ['question_id','question_type','stem','choices','correct_choice_ids','explanation']};assert v==x['original_visible_content'];assert nq.digest(v)==x['visible_content_sha256']and nq.digest(q)==x['record_sha256'];by[x['question_id']]=v
 assert not(set(v)&{'_statement_truth','independent_legal_audit','independent_realism_audit','primary_source_verification'})
def deref(x,cat):
 if isinstance(x,dict):return cat[x['text_ref']]if set(x)=={'text_ref'}else{k:deref(v,cat)for k,v in x.items()}
 if isinstance(x,list):return[deref(v,cat)for v in x]
 return x
for m in cat['question_maps']:assert deref(m['refs'],cat['catalog'])==by[m['question_id']]
align=load(e/'related-question-alignment.json');assert len(align['records'])==80 and align['all_options_read']==341 and align['question_audit_credit']==0
assert set(x['question_id']for x in align['records'])==set(by);assert align['added_claim_alignment'][0]['direct_question_ids']==[f'MA-EXP-{n:04d}'for n in range(153,157)];assert align['added_claim_alignment'][1]['direct_question_ids']==['MA-Q-0287','MA-Q-0370','MA-Q-0385','MA-Q-0399']
for src in load(e/'actual-current-derived-payloads.json')['sources']:
 raw=nq.git(ctl,'show',src['controller_head']+':'+src['source_path'],binary=True);assert hashlib.sha256(raw).hexdigest()==src['raw_sha256'];s=raw.decode();payload=json.loads(s[s.index('{'):].rstrip().removesuffix(';'))
 for it in src['records']:
  v=payload
  for k in it['json_pointer'].strip('/').split('/'):v=v[int(k)]if isinstance(v,list)else v[k]
  assert v==it['payload'] and v['source_hashes']['w1-c-1']==b['body_sha256']
assert len(r['derived_surface_findings'])==3
for doc in d['read_docs']:assert sha(ctl/doc['path'])==sha(w/doc['evidence_path'])==doc['raw_sha256']and doc['used_as_Massachusetts_legal_authority']is False
res={k:copy.deepcopy(d[k])for k in ['stage','independent_of_authors','actor_provenance','auditor','auditor_instance','canonical_audit','canonical_release_credit','question_audit_credit']};res.update(worker_commit=nq.git(w,'rev-parse','HEAD'),unit_hashes={u:x['body_sha256']for u,x in j['unit_bindings'].items()},evidence={'path':rel,'raw_sha256':sha(w/rel)},result_path=nq.OUTPUT+j['job_id']+'-result.json',results=[{'unit_id':r['unit_id'],'completeness':r['completeness'],'legal_status':r['legal_status']}])
nq.validate_result(j,res);sources=nq.validate_evidence(j,res,d)
for p,h in sources:assert sha(w/p)==h
for line in subprocess.check_output(['git','-C',str(w),'status','--porcelain','--untracked-files=all'],text=True).splitlines():assert line[3:].startswith(pre),line
log={'status':'PASS','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'root_note_review_queue_script_sha256':sha(ctl/'scripts/note_review_queue.py'),'root_notes_census_reassessment_script_sha256':sha(ctl/'scripts/notes_census_reassessment.py'),'checks':{'current_root_inventory_current_registered_reassessment':'PASS','committed_final_census_body_unit_and_all34_claim_bindings':'PASS','old32_canonical_JSON_exact_preservation_and_mapping':'PASS','original_omission_exactSHA_and_new_actor_claims':'PASS','carried_blockers_exact_empty_no_release_of_old_legal_blocker':'PASS','all34_claims_current_primary_rawSHA_URL_section_dates':'PASS','fresh9_official_responses_normalTLS_and_no_oldcache':'PASS','independent40_body_inventory_complete_content_mapping':'PASS','related80_original_stem_options_key_all_explanations_roundtrip_341options':'PASS','actual_current_connected_derived_payloads2_and_module1':'PASS','same_actual_session_provenance_credit0':'PASS','current_root_validate_result_and_validate_evidence':'PASS','only_reassessment_e1_report_evidence_prefix_changed':'PASS'},'limits':'Hash/schema validation binds the written evidence and reported scope; it does not independently establish legal correctness or identity. No root mutation, original revision, or canonical/question credit.'}
if '--verify-only'not in sys.argv:(e/'validation-log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','units':1,'claims':34,'body_inventory':40,'original_omissions_resolved':1,'new_omissions':0,'related_questions':80,'options':341,'derived_payloads':3,'primary_unit_documents':7,'fresh_official_responses':9},ensure_ascii=False))
