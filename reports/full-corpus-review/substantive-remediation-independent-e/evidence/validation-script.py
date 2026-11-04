import pathlib,json,hashlib,sys,subprocess,copy,datetime
w=pathlib.Path('/workspace/independent-sata-remediation-e');ctl=pathlib.Path('/workspace/oddments');pre='reports/full-corpus-review/substantive-remediation-independent-e/';ep=pre+'evidence';e=w/ep;rel=pre+'review.json';sys.path.insert(0,str(ctl/'scripts'));from build_full_corpus_review import validate_independent_source_bytes
load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();dig=lambda x:hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest();git=lambda root,*a:subprocess.check_output(['git','-C',str(root),*a]);j=load(pathlib.Path('/tmp/sata-remediation-independent-e-assignment.json'));v=load(pathlib.Path('/tmp/sata-remediation-independent-e-visible.json'));d=load(w/rel)
assert d['job_id']==j['job_id']and len(v)==len(d['records'])==3;assert d['actor_provenance']=={'actor_id':j['worker'],'session_id':j['session']}=={'actor_id':'/root/independent_case_e','session_id':'/root/independent_case_e'};assert d['auditor']=='GPT'and d['auditor_instance']==j['auditor_instance']=='gpt-independent-session-root-independent_case_e-20261103';assert d['excluded_author']==j['excluded_author']=='/root/independent_case_g'and d['independent_of_author'];assert d['source_commit']==j['source_commit'];assert d['reviewed_at']=='2026-11-04'==datetime.datetime.now(datetime.timezone.utc).date().isoformat()
for k in ['question_bank_review_credit','question_audit_credit','canonical_credit','canonical_release_credit','author_review_credit','additional_coverage_credit']:assert d[k]==0
for k in ['canonical_audit','formal_canonical_audit_performed','release_eligible','public_IDs_assigned','activation_performed']:assert d[k]is False
assert d['assignment_raw_sha256']==sha(pathlib.Path('/tmp/sata-remediation-independent-e-assignment.json'));assert d['safe_visible_packet_raw_sha256']==j['safe_visible_packet_sha256']==sha(pathlib.Path('/tmp/sata-remediation-independent-e-visible.json'))==sha(e/'safe-visible-input-snapshot.json');assert d['bindings']==j['bindings']
for name,tmp in [('assignment','/tmp/sata-remediation-independent-e-assignment.json'),('visible-input','/tmp/sata-remediation-independent-e-visible.json')]:
 p=pre+name+'.json';assert (ctl/p).read_bytes()==git(ctl,'show','6f98f6d5:'+p)==git(ctl,'show','HEAD:'+p)==pathlib.Path(tmp).read_bytes()
def safe_candidates(x):
 if isinstance(x,dict):
  if all(k in x for k in ['stem','choices','correct_choice_ids','explanation']):yield x
  for z in x.values():yield from safe_candidates(z)
 elif isinstance(x,list):
  for z in x:yield from safe_candidates(z)
expected=[['A','C','D'],['A','C'],['A','C','E']];opts=0;auths=0
for vis,row,key in zip(v,d['records'],expected):
 b=j['bindings'][vis['draft_key']];assert row['draft_key']==vis['draft_key']and row['binding']==b and row['safe_visible_record_sha256']==dig(vis)==b['visible_sha256'];p=b['path'];raw=(w/p).read_bytes();assert hashlib.sha256(raw).hexdigest()==b['source_file_sha256'];assert raw==(ctl/p).read_bytes()==git(ctl,'show','HEAD:'+p)==git(ctl,'show',j['source_commit']+':'+p);safe=[x for x in safe_candidates(json.loads(raw))if x['stem']==vis['stem']];assert len(safe)==1 and all(safe[0][k]==vis[k]for k in ['question_type','topic','stem','choices','correct_choice_ids','explanation'])
 assert row['independently_expected_choice_ids']==row['proposed_choice_ids']==vis['correct_choice_ids']==key and row['proposed_key_correct'];assert row['legal_disposition']==row['overall_draft_content_disposition']=='KEEP';assert row['public_question_id']is None and row['release_eligible']is False and row['activation_performed']is False;assert row['question_bank_review_credit']==row['canonical_release_credit']==0;assert row['stem_all_choices_proposed_key_all_Korean_explanations_read'];assert len(row['option_assessments'])==len(vis['choices'])
 for o,c in zip(row['option_assessments'],vis['choices']):
  assert o['choice_id']==c['id']and o['choice_text']==c['text'];assert o['independent_expected_true']==(c['id']in key);assert o['legal_status']=='KEEP'and o['blocker']is None and o['finding_ko'].strip()and o['korean_distractor_explanation_read_completely'];assert o['korean_explanation_status']=='SUPPORTED_AS_SCOPED'and o['authorities'];opts+=1
  for a in o['authorities']:
   assert a['source_type']=='PUBLIC_OFFICIAL'and a['official_url'].startswith('https://')and a['exact_section']and a['version_or_effective_date_status'];assert a['law_checked_date']=='2026-11-04'and a['retrieved_at_utc'].startswith('2026-11-04');assert a['evidence_path'].startswith(ep+'/');validate_independent_source_bytes(a,w);auths+=1
 assert row['core_explanation_review']['status']=='KEEP'and row['core_explanation_review']['read_completely'];cr=row['realism']['criteria'];assert len(cr)==10 and [x['criterion_id']for x in cr]==list(range(1,11));assert all(x['passed']and x['finding_ko'].strip()for x in cr)and row['realism']['disposition']=='PASS';assert row['novelty_and_coverage']['additional_coverage_credit']==0 and row['novelty_and_coverage']['additional_legal_topic_coverage_certified']is False
assert opts==14 and len(d['sources'])==10
for s in d['sources']:
 assert s['http_status']==200 and s['fresh_live_retrieval']and s['normal_TLS_certificate_verification']and s['retrieved_at_utc'].startswith('2026-11-04');validate_independent_source_bytes(s,w)
 if s['source_id']=='nabp-live':
  assert s['public_raw_redistribution']is False and s['raw_sha256']=='b8544f403990191075747b231c81cde4449c6eb83333cfb1d9f05b5e1273d30d'and s['used_as_law']is False;probe=copy.deepcopy(s);probe['raw_path']='/tmp/no-private-NABP-original-in-CI-remediation-e.pdf';validate_independent_source_bytes(probe,w)
 else:assert sha(w/s['raw_path'])==s['raw_sha256']
assert not(e/'nabp-live.pdf').exists()and not(e/'nabp-live.txt').exists();st=d['style_profile'];assert sha(w/st['path'])==sha(ctl/st['path'])==sha(w/st['snapshot_path'])==st['raw_sha256'];s=load(w/st['path']);assert s['content_hash']==st['stored_content_hash']and s['content_version']==st['content_version']==1;assert st['profile_id']=='MPJE-MA-PRE2027'and d['reviewed_at']<st['valid_for_exams_before']
cfg=load(ctl/'site/practice-expansion/publication.json');bank={}
for path in ['practice_expansion/2026-10-23/candidates/questions.json']+[x['path']for x in cfg['additional_banks']]:
 for q in load(ctl/path)['questions']:bank[q['question_id']]=q
assert len(bank)==2346
for p in sorted((ctl/'data/questions').glob('*.json')):
 q=load(p);bank[q['question_id']]=q
assert len(bank)==2785;cb=load(e/'corpus-inventory-binding.json');observed=[{'collection':'canonical'if qid.startswith('MA-Q-')else'public','question_id':qid,'record_sha256':dig(q)}for qid,q in bank.items()];observed.sort(key=lambda x:(x['collection'],x['question_id']));assert observed==cb['records']and dig(observed)==cb['record_inventory_sha256'];assert sha(e/'corpus-inventory-binding.json')==d['corpus_inventory_binding']['raw_sha256'];near=load(e/'nearest-original-comparison-input.json');assert near['corpus']=={'canonical':439,'public':2346}and len(near['selected_original_comparators'])==23;by={}
for x in near['selected_original_comparators']:
 q=bank[x['question_id']];assert dig(q)==x['record_sha256']and x['stem']==q['stem']and x['choices']==q['choices'];assert set(x)=={'question_id','collection','record_sha256','stem','choices'};by[x['question_id']]={k:x[k]for k in ['question_id','stem','choices']}
cat=load(e/'nearest-exact-text-catalog.json');assert len(cat['catalog'])==131 and len(cat['question_maps'])==23

def de(x):
 if isinstance(x,dict):return cat['catalog'][x['text_ref']]if set(x)=={'text_ref'}else{k:de(z)for k,z in x.items()}
 if isinstance(x,list):return[de(z)for z in x]
 return x
for x in cat['question_maps']:assert de(x['refs'])==by[x['question_id']]
assert sum(len(x['choices'])for x in near['selected_original_comparators'])==106
for row,n in zip(d['records'],near['comparisons']):assert row['realism']['nearest_comparison']==n and row['realism']['nearest_full_stems_all_options_read']and row['realism']['source_input_raw_sha256']==sha(e/'nearest-original-comparison-input.json')
for doc in d['read_methodology_docs']:assert sha(ctl/doc['path'])==sha(w/doc['evidence_path'])==doc['raw_sha256']
b=d['immutable_binding_verification'];assert sha(w/b['path'])==b['raw_sha256']and load(w/b['path'])['source_commit']==j['source_commit']
for line in git(w,'status','--porcelain','--untracked-files=all').decode().splitlines():assert line[3:]==rel or line[3:].startswith(ep+'/'),line
log={'status':'PASS','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'controller_head':git(ctl,'rev-parse','HEAD').decode().strip(),'source_byte_validator_script_sha256':sha(ctl/'scripts/build_full_corpus_review.py'),'checks':{'real_E_identity_session_instance_G_author_exclusion':'PASS','three_immutable_source_fullfileSHA_sourcecommit_currentroot_HEAD':'PASS','6f98permanent_assignment_visiblepacket_exactbytes':'PASS','safe_final_fields_all3visibleSHA':'PASS','14truthvalues_expected_ACD_AC_ACE_primary_sections':'PASS','all14Korean_rationale_strength_scope_clock_conditions':'PASS','all30_individual_realismcriteria_reasons':'PASS','439canonical2346public_search_23nearest106options_fullread':'PASS','131exact_strings23lossless_maps_current_originalhashes':'PASS','0367strong_overlap_disclosed_alladditional_coverage0':'PASS','fresh10official200_actual_expected_documents':'PASS','nine_publicpayloads_NABPstylememo_verified':'PASS','no_NABPsample_reposting_or_private_CI_dependency':'PASS','currentstyleprofile_version_contenthash_rawSHA':'PASS','allcredits0_releaseeligiblefalse_no_activation':'PASS','only_review_json_evidence_owned_paths':'PASS'},'options':opts,'authority_entries':auths,'limits':'No formal canonical audit, public IDs, activation or added coverage. Byte/schema checks do not mechanically establish law or realism. No unrelated full test suite repeated.'}
if '--verify-only'not in sys.argv:(e/'validation-log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','drafts':3,'options':opts,'authority_entries':auths,'realismcriteria':30,'nearest_originals':23,'nearest_options':106,'fresh200':10,'NABP_private_CI_dependency':False},ensure_ascii=False))
