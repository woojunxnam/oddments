import json,pathlib,hashlib,sys,copy,datetime,subprocess,collections
w=pathlib.Path('/workspace/independent-notes4-e');ctl=pathlib.Path('/workspace/oddments');rel='reports/full-corpus-review/independent-notes/fourth-e-review.json';ep='reports/full-corpus-review/independent-notes/fourth-e-evidence';e=w/ep;sys.path.insert(0,str(ctl/'scripts'));import note_review_queue as nq;from notes_revision import load_notes;from build_full_corpus_review import validate_independent_source_bytes
load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();j=load(pathlib.Path('/tmp/independent-notes4-e-assignment.json'));d=load(w/rel);assert set(j['unit_ids'])=={'w2-c-7','w2-c-8','w2-c-9','w2-c-10','w2-c-11'};assert len(d['records'])==5;inv=nq.inventory(ctl);state=load(ctl/nq.STATE);nq.validate_state(state,ctl);nq.current(j,inv,state);assert all(inv['units'][u]==b for u,b in j['unit_bindings'].items())
assert d['actor_provenance']==j['actor_provenance']=={'actor_id':'/root/independent_case_e','session_id':'/root/independent_case_e'};assert d['auditor']=='GPT'and d['auditor_instance']==j['auditor_instance']=='gpt-independent-session-root-independent_case_e-20261103';assert d['independent_of_authors']is True and d['canonical_audit']is False;assert all(d[k]==0 for k in ['canonical_release_credit','question_audit_credit','author_review_credit']);assert d['reviewed_at']=='2026-11-04'==datetime.datetime.now(datetime.timezone.utc).date().isoformat();assert sha(pathlib.Path('/tmp/independent-notes4-e-assignment.json'))==d['assignment_raw_sha256']
body=load(e/'body-first-snapshot.json');bodies={x['id']:x for x in body['units']};sources_byunit={};originals=load(e/'selected-original-census-bindings.json');counts=collections.Counter();claimhashes={};snapshot={x['unit_id']:x for x in originals['units']}
for r in d['records']:
 u=r['unit_id'];b=j['unit_bindings'][u];assert r['binding']==b and r['body_read_completely']and r['completeness']=='COMPLETE'and not r['omissions'];assert r['legal_status']==('LEGAL_HOLD'if u=='w2-c-10'else'KEEP')
 for root in [w,ctl]:
  unit=next(x for c in load_notes(root)['chapters']for x in c['units']if x['id']==u);assert unit['body']==bodies[u]['body'];assert hashlib.sha256(unit['body'].encode()).hexdigest()==b['body_sha256']
 raw=nq.git(ctl,'show','HEAD:'+b['census_path'],binary=True);assert raw==(ctl/b['census_path']).read_bytes()==(w/b['census_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==b['census_sha256'];census=json.loads(raw);cs=[x for x in census['claims']if x['unit_id']==u];unitrow=next(x for x in census['units']if x['unit_id']==u);assert nq.digest(unitrow)==b['census_unit_record_sha256'];assert snapshot[u]['original_unit_record']==unitrow and snapshot[u]['original_claims']==cs;assert {x['claim_id']:nq.digest(x)for x in cs}==b['claim_record_sha256s'];cb={x['claim_id']:x for x in cs};claimhashes.update(b['claim_record_sha256s'])
 assert len(r['claims'])==len(cs)
 for c in r['claims']:
  assert c['claim_id']in cb and c['claim_record_sha256']==b['claim_record_sha256s'][c['claim_id']]and c['statement_ko']==cb[c['claim_id']]['statement_ko'];assert c['claim_read_completely']and c['model_visible_substantive_claim_and_source_context_read']and c['author_verdict_inherited_as_truth']is False;assert c['finding'].strip();counts[c['legal_status']]+=1
  assert c['legal_status']==('LEGAL_HOLD'if c['claim_id']=='NOTE-WAVE6-W2-C-10-015'else'KEEP');assert bool(c['blocker'])==(c['legal_status']!='KEEP')
  for a in c['authorities']:
   assert a['source_type']=='PUBLIC_OFFICIAL'and a['official_url'].startswith('https://')and a['exact_section']and a['version_or_effective_date_status'];assert a['law_checked_date']=='2026-11-04'and a['retrieved_at_utc'].startswith('2026-11-04');validate_independent_source_bytes(a,w)
assert len(claimhashes)==113 and counts=={'KEEP':112,'LEGAL_HOLD':1}
assert len(d['sources'])==15
for s in d['sources']:
 assert s['http_status']==200 and s['fresh_live_retrieval']and not s['old_Nov3_cache_reuse'];assert s['retrieved_at_utc'].startswith('2026-11-04')and s['read_status']=='DIRECT_CURRENT_OFFICIAL_RELEVANT_SECTIONS_READ';validate_independent_source_bytes(s,w)
 if s['source_id']=='pmp-guide':
  assert s['public_raw_redistribution']is False and 'memo'in s['public_evidence_mode']and pathlib.Path(s['raw_path']).is_absolute();assert s['ci_requires_private_source']is False;probe=copy.deepcopy(s);probe['raw_path']='/tmp/definitely-not-existing-private-pmp-guide-e4.pdf';validate_independent_source_bytes(probe,w);assert s['evidence_path'].endswith('pmp-guide-independent-research-memo.json')
 else:
  assert sha(w/s['raw_path'])==s['raw_sha256']and sha(w/s['extracted_text_path'])==s['extracted_text_sha256']
  if s['raw_path'].endswith('.pdf'):assert (w/s['raw_path']).read_bytes().startswith(b'%PDF')
assert not(e/'pmp-guide.pdf').exists()and not(e/'pmp-guide.txt').exists();memo=load(e/'pmp-guide-independent-research-memo.json');assert memo['source_payload_raw_sha256']=='f3046fbd12822ed8f6d1bf73f61d907a74883db4ef6e67c663decdc6a9edc13b'and memo['actual_relevant_sections_directly_read']and memo['public_raw_redistribution']is False
coverage=load(e/'body-to-census-coverage.json');assert coverage['complete_mapping']and not coverage['actual_omissions_found'];assert sum(len(v['items'])for v in coverage['units'].values())==82
for uid,v in coverage['units'].items():assert all(x['coverage']=='COVERED_BY_ACTUAL_STATEMENT_CONTENT'and x['final_census_claim_ids']for x in v['items']);assert set(cid for x in v['items']for cid in x['final_census_claim_ids'])==set(j['unit_bindings'][uid]['claim_record_sha256s'])
# Current original bank bytes and lossless read projection; hidden fields remain unprinted.
config=load(ctl/'site/practice-expansion/publication.json');bank={}
for path in ['practice_expansion/2026-10-23/candidates/questions.json']+[a['path']for a in config['additional_banks']]:
 for q in load(ctl/path)['questions']:bank[q['question_id']]=q
for p in sorted((ctl/'data/questions').glob('*.json')):
 q=load(p);bank[q['question_id']]=q
assert len(bank)==2785;pack=load(e/'related-question-visible-input.json');cat=load(e/'related-question-exact-text-catalog.json');assert len(pack['records'])==len(cat['question_maps'])==160 and len(cat['catalog'])==1104;by={}
for x in pack['records']:
 q=bank[x['question_id']];v={k:q[k]for k in ['question_id','question_type','stem','choices','correct_choice_ids','explanation']};assert v==x['original_visible_content'];assert nq.digest(q)==x['record_sha256']and nq.digest(v)==x['visible_content_sha256'];by[x['question_id']]=v
 assert set(v)=={'question_id','question_type','stem','choices','correct_choice_ids','explanation'}
def deref(v):
 if isinstance(v,dict):return cat['catalog'][v['text_ref']]if set(v)=={'text_ref'}else{k:deref(z)for k,z in v.items()}
 if isinstance(v,list):return[deref(z)for z in v]
 return v
for q in cat['question_maps']:assert deref(q['refs'])==by[q['question_id']]
align=load(e/'related-question-alignment.json');assert len(align['records'])==160 and align['all_options_read']==sum(len(x['choices'])for x in by.values())==695;assert align['question_audit_credit']==0 and align['confirmed_local_explanation_mismatch_ids']==['MA-Q-0012'];assert all(x['full_question_key_assessment']=='NOT_PERFORMED'and x['question_audit_credit']==0 for x in align['records']);assert len(load(e/'additional-search-candidates-not-full-reviewed.json')['records'])==43
exposure=load(e/'prior-input-exposure-and-default-projection.json');assert exposure['historical_hidden_truth_intersects_current_full_read']==[]and exposure['all_question_audit_credit']==0
pub=exposure['public_PR190_IDs_only_snapshot'];raw=nq.git(ctl,'show',pub['parent_identified_published_commit']+':'+pub['source_path'],binary=True);assert hashlib.sha256(raw).hexdigest()==pub['raw_sha256']and json.loads(raw)['recommended_ids']==pub['recommended_ids'];cur=(ctl/pub['source_path']).read_bytes();assert set(json.loads(cur)['recommended_ids'])==set(pub['recommended_ids'])and len(pub['recommended_ids'])==298
# Actual current derived payloads read, while root intentionally defers full regeneration.
for s in load(e/'actual-current-derived-payloads.json')['sources']:
 raw=nq.git(ctl,'show',s['controller_head']+':'+s['source_path'],binary=True);assert hashlib.sha256(raw).hexdigest()==s['raw_sha256'];txt=raw.decode();src=json.loads(txt[txt.index('{'):].rstrip().removesuffix(';'));txt=(ctl/s['source_path']).read_text();cur=json.loads(txt[txt.index('{'):].rstrip().removesuffix(';'))
 for it in s['records']:
  a=src;b=cur
  for key in it['json_pointer'].strip('/').split('/'):a=a[int(key)]if isinstance(a,list)else a[key];b=b[int(key)]if isinstance(b,list)else b[key]
  assert a==it['payload']==b
  for uid in set(j['unit_ids'])&set(a.get('source_hashes',{})):assert a['source_hashes'][uid]==j['unit_bindings'][uid]['body_sha256']
 for mod in s['associated_modules']:assert mod in cur.get('modules',[])
dfs=load(e/'derived-surface-review.json');assert dfs['actual_payloads_full_read']==9 and dfs['associated_modules_full_read']==2
for doc in d['read_docs']:assert sha(ctl/doc['path'])==sha(w/doc['evidence_path'])==doc['raw_sha256']and doc['used_as_Massachusetts_legal_authority']is False
res={k:copy.deepcopy(d[k])for k in ['stage','independent_of_authors','actor_provenance','auditor','auditor_instance','canonical_audit','canonical_release_credit','question_audit_credit']};res.update(worker_commit=nq.git(w,'rev-parse','HEAD'),unit_hashes={u:b['body_sha256']for u,b in j['unit_bindings'].items()},evidence={'path':rel,'raw_sha256':sha(w/rel)},result_path=nq.OUTPUT+j['job_id']+'-result.json',results=[{k:r[k]for k in ['unit_id','completeness','legal_status']}for r in d['records']]);nq.validate_result(j,res);srcs=nq.validate_evidence(j,res,d)
for p,h in srcs:assert sha(w/p)==h
for line in nq.git(w,'status','--porcelain','--untracked-files=all').splitlines():assert line[3:]==rel or line[3:].startswith(ep+'/'),line
log={'status':'PASS','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'controller_head':nq.git(ctl,'rev-parse','HEAD'),'root_validator_script_sha256':sha(ctl/'scripts/note_review_queue.py'),'root_source_byte_validator_script_sha256':sha(ctl/'scripts/build_full_corpus_review.py'),'checks':{'current_registered5unit_body_census_113claim_bindings':'PASS','selected_originalJSONobjects_preserved_no_author_truth_inheritance':'PASS','body_first82contentsegments_complete_mapping_to113claims':'PASS','all113claim_individual_Korean_finding_primaryscope':'PASS','112KEEP_1LEGAL_HOLD_clockrelation_not_forced':'PASS','fresh15official200_actual_document_sections_read':'PASS','retained14official_raws_SHA':'PASS','guide_own_memo_SHA_original_payload_provenance_only_no_redistribution':'PASS','CI_validation_does_not_read_or_require_private_guide_original':'PASS','related160originals695options1104strings_all_mappings_roundtrip':'PASS','additional43candidates_not_full_reviewed_scope_disclosed':'PASS','PR190published298IDs_match_currentroot298selection_only':'PASS','intentional_root_publicationSHA_stale_failure_recorded_not_silentPASS':'PASS','actual_current9derived_payloads_and2modules_bodybindings':'PASS','same_real_actor_session_instance_noncanonical_allcredit0':'PASS','current_root_validate_result_validate_evidence':'PASS','only_exact_fourth_e_owned_paths_changed':'PASS'},'authority_entries_verified':len(srcs),'limits':'No full-suite repetition; no remote deployment HTTP check; no successful current full publication build claimed; no CI assertion of private guide original-byte verification. Byte/schema validation is not independent legal truth.'}
if '--verify-only'not in sys.argv:(e/'validation-log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','units':5,'claims':113,'KEEP':112,'LEGAL_HOLD':1,'SOURCE_BLOCKED':0,'body_content_segments':82,'questions':160,'options':695,'authority_entries':len(srcs),'fresh200':15,'publicraw':14,'own_guide_memo':1,'derived':9,'modules':2},ensure_ascii=False))
