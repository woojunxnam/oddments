import json,pathlib,hashlib,sys,importlib.util,collections,subprocess
R=pathlib.Path('/workspace/independent-notes3-g');ROOT=pathlib.Path('/workspace/oddments');P=R/'reports/full-corpus-review/independent-notes/third-g-review.json';E=R/'reports/full-corpus-review/independent-notes/third-g-evidence';a=json.load(open('/tmp/independent-notes3-g-assignment.json'));r=json.load(open(P));sys.path.insert(0,str(ROOT/'scripts'))
def sha(b):return hashlib.sha256(b).hexdigest()
def dh(x):return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
sp=importlib.util.spec_from_file_location('current_note_review_queue',ROOT/'scripts/note_review_queue.py');rq=importlib.util.module_from_spec(sp);sp.loader.exec_module(rq);inv=rq.inventory(ROOT);rq.current(a,inv)
assert r['actor_provenance']==a['actor_provenance'] and r['auditor_instance']==a['auditor_instance'] and r['question_audit_credit']==r['canonical_release_credit']==0 and not r['canonical_audit'];assert len(r['records'])==5
for row in r['records']:
 uid=row['unit_id'];assert row['binding']==a['unit_bindings'][uid];cs=json.load(open(ROOT/row['binding']['census_path']))['claims'];cs={c['claim_id']:c for c in cs if c['unit_id']==uid};assert len(row['claims'])==len(cs)
 for c in row['claims']:
  assert c['claim_record_sha256']==dh(cs[c['claim_id']])==row['binding']['claim_record_sha256s'][c['claim_id']];assert c['original_statement_ko']==cs[c['claim_id']]['statement_ko']
  for au in c['authorities']:
   assert au['source_type']=='PUBLIC_OFFICIAL' and au['official_url'].startswith('https://') and au['exact_section'] and au['version_or_effective_date_status'];assert sha((R/au['evidence_path']).read_bytes())==au['evidence_sha256']==au['raw_sha256'];assert au['evidence_path'].startswith('reports/full-corpus-review/independent-notes/third-g-evidence/')
 assert row['body_read_completely'] and row['completeness']=='COMPLETE' and not row['omissions'];mapped={cid for g in row['independent_inventory'] for cid in g['matched_author_claim_ids']};assert mapped==set(cs)
for s in r['sources']:
 assert sha((R/s['evidence_path']).read_bytes())==s['evidence_sha256']==s['raw_sha256'];assert sha((R/s['text_evidence_path']).read_bytes())==s['text_evidence_sha256'];assert sha((R/s['retrieval_metadata_path']).read_bytes())==s['retrieval_metadata_sha256'];m=json.load(open(R/s['retrieval_metadata_path']));assert m['http_status']==200 and m['body_verification']=='APPLICABLE_OFFICIAL_BODY_DIRECTLY_READ'
assert sha((R/r['source_register_path']).read_bytes())==r['source_register_sha256']
for pk,hk in [('actual_load_notes_body_snapshot_path','actual_load_notes_body_snapshot_sha256'),('selected_census_records_path','selected_census_records_sha256')]:assert sha((R/r['input_bindings'][pk]).read_bytes())==r['input_bindings'][hk]
for section in ['independent_inventory_evidence','related_question_comparison','derived_comparison','direct_read_history','inventory_snapshot']:
 z=r[section];assert sha((R/z['path']).read_bytes())==z['raw_sha256']
for x in r['policy_snapshot']:assert sha((R/x['path']).read_bytes())==x['raw_sha256']
q=json.load(open(E/'related-questions-visible.json'));com=json.load(open(E/'related-question-comparison.json'));assert len(q)==len(com['records'])==55
originals={}
for path in {x['collection'] for x in q}:
 for x in json.load(open(ROOT/path))['questions']:originals[x['question_id']]=x
for v,c in zip(q,com['records']):
 orig=originals[v['question_id']];assert dh(orig)==v['record_sha256']==c['record_sha256'];safe={k:orig[k] for k in ['question_id','question_type','stem','choices','correct_choice_ids','explanation']};assert safe==v['original_visible_content'];assert dh(safe)==c['visible_content_sha256'];assert c['stored_key']==c['independently_expected_key']==safe['correct_choice_ids'];assert len(c['per_choice_findings'])==len(safe['choices'])
 for choice,full in zip(c['per_choice_findings'],safe['choices']):assert choice['option_text']==full['text'] and choice['option_text_sha256']==sha(full['text'].encode()) and choice['original_choice_korean_rationale_sha256']==sha(safe['explanation']['choice_analysis'][full['id']].encode())
assert r['counts']['claim_legal_status']=={'KEEP':106,'SOURCE_BLOCKED':3,'LEGAL_HOLD':2}
out={k:r[k] for k in ['stage','independent_of_authors','actor_provenance','auditor','auditor_instance','canonical_audit','canonical_release_credit','question_audit_credit']};out.update(worker_commit=subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD'],text=True).strip(),unit_hashes={u:b['body_sha256'] for u,b in a['unit_bindings'].items()},evidence={'path':str(P.relative_to(R)),'raw_sha256':sha(P.read_bytes())},result_path='reports/full-corpus-review/independent-notes/'+a['job_id']+'-result.json',results=[{k:x[k] for k in ['unit_id','completeness','legal_status']} for x in r['records']]);rq.validate_result(a,out);refs=rq.validate_evidence(a,out,r)
for p,h in refs:assert sha((R/p).read_bytes())==h
if '--write-envelope' in sys.argv:
 assert subprocess.check_output(['git','-C',str(R),'show','HEAD:'+str(P.relative_to(R))])==P.read_bytes();rq.committed_evidence(a,out,R);pathlib.Path('/tmp/independent-notes3-g-result.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','current_root_bindings':5,'body_and_census_claims':111,'primary_source_raw_bindings':len(r['sources']),'related_question_full_record_and_visible_hashes':55,'related_choice_and_rationale_bindings':230,'derived_visible_records':10,'claim_legal_status':r['counts']['claim_legal_status'],'unit_legal_status':r['counts']['unit_legal_status'],'current_root_note_queue_validate_result':'PASS','current_root_validate_evidence':'PASS','committed_evidence':'PASS' if '--write-envelope' in sys.argv else 'NOT_RUN_BEFORE_COMMIT','report_sha256':sha(P.read_bytes()),'worker_commit':out['worker_commit'],'envelope_written':'--write-envelope' in sys.argv,'queue_submit_or_integrate':'NOT_RUN_ROOT_ONLY'},indent=2))
