import pathlib,json,hashlib,copy,re,datetime,subprocess,sys,urllib.parse
R=pathlib.Path('/workspace/phase9-remediation-author-g');ROOT=pathlib.Path('/workspace/oddments');P=R/'reports/full-corpus-review/phase9-remediation-author-g';E=P/'evidence';RP=P/'editorial-report-v1.json'
report=json.load(open(RP));targets=json.load(open(E/'original-targets-and-native-findings.json'))['targets'];expected={'MA-REV-0002','MA-REV-0005','MA-REV-0020','MA-REV-0026','MA-REV-0027','MA-EXP-0515','MA-EXP-0615','MA-EXP-0735','MA-EXP-0827','MA-EXP-0851'}
def sha(b):return hashlib.sha256(b).hexdigest()
def dh(x):return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def git(*args):return subprocess.check_output(['git','-C',str(R),*args])
def require(x,msg):
 if not x:raise ValueError(msg)
visiblekeys=['draft_key','question_type','stem','choices','correct_choice_ids','explanation'];actor={'actor_id':'/root/independent_case_g','session_id':'/root/independent_case_g','stable_instance':'gpt-independent-phase3-g-root-independent_case_g-20261103'}
def validate(d):
 require('question_id' not in d and d['draft_key']=='P9-REPAIR-'+d['original_question_id'].removeprefix('MA-'),'No public ID allocation')
 require(all(d['author_provenance'].get(k)==v for k,v in actor.items()),'Actual unchanged author provenance')
 require(d['canonical_audit'] is False and d['independent_of_authors'] is False and d['public_activation'] is False and d['release_eligible'] is False,'Draft cannot release')
 require(all(d[k]==0 for k in ['canonical_release_credit','independent_review_credit','author_review_credit','additional_coverage_credit']),'Draft cannot create credit')
 require(d['visible_content_sha256']==dh({k:d[k] for k in visiblekeys}),'Stale visible hash')
 require(len(d['choices']) in {4,5} and len({c['id'] for c in d['choices']})==len(d['choices']),'Choice structure')
 require(set(d['explanation']['choice_analysis'])=={c['id'] for c in d['choices']},'Every Korean rationale')
 require(len(set(d['explanation']['choice_analysis'].values()))==len(d['choices']) and all(re.search('[가-힣]',v) and len(v)>60 for v in d['explanation']['choice_analysis'].values()),'Distinct detailed Korean rationales')
 learnertext=d['stem']+' '+' '.join(c['text'] for c in d['choices'])
 require(not re.search(r'\b(notes|retrieved|metadata|source.checked|correct option|incorrect option)\b',learnertext,re.I),'Learner-facing helper/source wording')
 require(len({c['text'].strip().lower() for c in d['choices']})==len(d['choices']),'Duplicate options')
 require(set(p['choice_id'] for p in d['option_proofs'])=={c['id'] for c in d['choices']},'Every option proof')
 yes=[]
 for c in d['choices']:
  f=next(p for p in d['option_proofs'] if p['choice_id']==c['id'])
  require(f['option_text_sha256']==sha(c['text'].encode()) and f['rationale_sha256']==sha(d['explanation']['choice_analysis'][c['id']].encode()),'Choice or rationale changed')
  require(f['author_supported'] in {'YES','NO'},'Unknown truth must HOLD, not certify a key')
  if f['author_supported']=='YES':yes.append(c['id'])
  require(bool(f['authorities']),'Missing authority')
 for a in [a for p in d['option_proofs'] for a in p['authorities']]+d['scenario_fact_authorities']:
  require(a['official_url'].startswith('https://') and urllib.parse.urlparse(a['official_url']).hostname in {'www.mass.gov','malegislature.gov','www.ecfr.gov','dailymed.nlm.nih.gov'},'Official primary URL')
  require(a['exact_section'] and a['law_checked_date']=='2026-11-04' and a['version_or_effective_date_status'] and a['effective_date_status'],'Section/version/date')
  require(a['body_verified_current_primary'] is True and a['http_status']==200 and a['used_as_legal_proof'] is True,'Failed/wrong body cannot prove choice')
  require(sha((R/a['raw_path']).read_bytes())==a['raw_sha256'],'Raw primary hash changed')
  require(sha((R/a['retrieval_metadata_path']).read_bytes())==a['retrieval_metadata_sha256'],'Retrieval metadata hash changed')
  m=json.load(open(R/a['retrieval_metadata_path']));require(m['raw_sha256']==a['raw_sha256'] and m['official_url']==a['official_url'] and m['http_status']==200,'Source retrieval differs')
  require(m['retrieved_at'].startswith('2026-11-04') and m['tls_verification'] is True and m['retrieval_method']=='LIVE_OFFICIAL_HTTPS_urllib' and m['used_as_legal_proof'] is True,'Honest fresh normal TLS retrieval')
  require(sha((R/a['text_path']).read_bytes())==a['text_sha256'],'Extracted source changed')
 require(yes==d['correct_choice_ids'],'Key contradicts option findings')
 require(len(yes)==1 if d['question_type']=='SBA' else 2<=len(yes)<len(d['choices']),'SBA uniqueness or mixed SATA')
 require(d['source_review_status']=='AUTHOR_SOURCE_CHECKED_DRAFT_NOT_INDEPENDENT' and d['source_blocker'] is None,'Current source status')
 require(d['nearby_comparison']['comparison_record']['draft_visible_content_sha256']==d['visible_content_sha256'],'Nearest bound to stale draft')
 return True
records=report['records'];require(len(records)==10 and {x['original_question_id'] for x in records}==expected,'Exact ten targets')
byid={}
for collection in {x['collection'] for x in targets}:
 for q in json.load(open(R/collection))['questions']:
  if q['question_id'] in expected:byid[q['question_id']]=q
rootbyid={}
for collection in {x['collection'] for x in targets}:
 for q in json.load(open(ROOT/collection))['questions']:
  if q['question_id'] in expected:rootbyid[q['question_id']]=q
for x in targets:
 qid=x['question_id'];require(dh(byid[qid])==dh(rootbyid[qid])==x['original_record_sha256']==report['original_question_hashes'][qid],'Original current whole-record changed')
 require({k:byid[qid][k] for k in ['question_id','question_type','stem','choices','correct_choice_ids','explanation']}==x['visible'],'Original full visible differs')
 n=x['native_finding'];require(sha((R/n['path']).read_bytes())==n['raw_sha256'],'Native report SHA changed')
 require(n['record']['record_sha256']==x['original_record_sha256'],'Native finding original binding')
drafts=[]
for row in records:
 p=R/row['draft_path'];require(sha(p.read_bytes())==row['draft_raw_sha256'],'Draft raw hash changed');d=json.load(open(p));validate(d);drafts.append(d)
 require(d['visible_content_sha256']==row['visible_content_sha256'] and d['original_record_sha256']==row['original_record_sha256'],'Editorial mapping changed')
require(sum(len(d['choices']) for d in drafts)==40,'All40 options')
require(sum(d['question_type']=='SBA' for d in drafts)==sum(d['question_type']=='SATA' for d in drafts)==5,'Types5/5')
reg=json.load(open(R/report['source_register_path']));require(sha((R/report['source_register_path']).read_bytes())==report['source_register_sha256'],'Source register SHA')
require(len(reg['sources'])==27 and reg['failed_or_wrong_body_proof_credit']==0,'Controlling source counts')
for s in reg['unused_discovery_or_diagnostic_sources']:
 m=json.load(open(R/s['retrieval_metadata_path']));require(m['used_as_legal_proof'] is False and m['body_verified_current_primary'] is False,'Discovery/wrong compiled text cannot prove current law')
 require(sha((R/s['raw_path']).read_bytes())==s['raw_sha256'] and sha((R/s['retrieval_metadata_path']).read_bytes())==s['retrieval_metadata_sha256'],'Excluded payload provenance')
def norm(s):return re.sub('[^a-z0-9]','',s.lower())
anchors={'ce':'may not earn more than eight contact hours','vax':'at least 2 additional hours of documented on-the-job training','ma23':'the treatment of opioid use disorder','1306-13':'Authorized by Practitioner to Partial Fill','hipaa406':'more than 500 residents of a State or jurisdiction','hipaa408':'contemporaneously with the notice','290-10':'not reasonably possible','act16':'Section 7 shall take effect on January 1 2026','loss':'within 45 days after discovery','lantus':'Room temperature only Do not refrigerate','butrans':'partial opioid agonist','estradiol':'DEA Schedule None','ma3':'Said prescription drug has not been included in Schedules I through V'}
for sid,phrase in anchors.items():require(norm(phrase) in norm((E/(sid+'.txt')).read_text()),'Required read section anchor missing: '+sid)
nearest=json.load(open(E/'nearest-comparisons.json'));require((nearest['canonical_count'],nearest['public_count'],nearest['source_defined_remaining_default_count'])==(439,2349,229),'Actual comparison pools')
current=json.load(open(E/'nearest-visible.json'));discarded=json.load(open(E/'redesign-context-visible.json'))['records'];history=json.load(open(E/'direct-read-history.json'));require(len(current)==32 and len({x['question_id'] for x in current+discarded})==35,'Actual full-read nearest counts')
require(set(history['nearest_read_ids'])=={x['question_id'] for x in current+discarded},'Read history differs')
for d in drafts:
 z=d['nearby_comparison'];require(sha((R/z['evidence_path']).read_bytes())==z['evidence_sha256'] and z['finding_ko'],'Actual per-draft comparison')
 for k in ['nearest_canonical','nearest_public','nearest_public_excluding_original','nearest_current_default']:
  v=z['comparison_record'][k]['full_stem_and_all_options'];require(v['stem'] and len(v['choices'])>=4,'Nearest complete visible')
style=json.load(open(R/report['public_style_memo_path']));require(style['live_attempt_http_status']==403 and style['cached_raw_sha256']=='b8544f403990191075747b231c81cde4449c6eb83333cfb1d9f05b5e1273d30d' and style['new_public_raw_copy'] is False,'NABP failure/cache limits')
require(not list(P.rglob('*nabp*.pdf')) and not list(P.rglob('*nabp*.txt')),'No new copyrighted sample raw')
for p in report['policy_snapshots']:require(sha((R/p['path']).read_bytes())==p['raw_sha256'],'Policy snapshot differs')
require(report['independent_of_authors'] is False and report['canonical_audit'] is False and report['author_review_credit']==report['independent_review_credit']==report['canonical_release_credit']==report['additional_coverage_credit']==0,'No author/self independence credit')
require((datetime.date(2026,11,6)+datetime.timedelta(days=45))==datetime.date(2026,12,21),'Form106 date arithmetic')
negative=[]
for mutation in ['visible','rationale','key','unknown_truth','primary_hash','wrong_body','all_correct_sata','helper_wording']:
 d=copy.deepcopy(next(x for x in drafts if x['question_type']=='SATA') if mutation=='all_correct_sata' else drafts[0])
 if mutation=='visible':d['stem']+=' changed'
 elif mutation=='rationale':
  d['explanation']['choice_analysis']['A']+=' 추가';d['visible_content_sha256']=dh({k:d[k] for k in visiblekeys})
 elif mutation=='key':d['correct_choice_ids']=['D'];d['visible_content_sha256']=dh({k:d[k] for k in visiblekeys})
 elif mutation=='unknown_truth':d['option_proofs'][0]['author_supported']='UNKNOWN'
 elif mutation=='primary_hash':d['option_proofs'][0]['authorities'][0]['raw_sha256']='0'*64
 elif mutation=='wrong_body':d['option_proofs'][0]['authorities'][0]['body_verified_current_primary']=False
 elif mutation=='all_correct_sata':
  for p in d['option_proofs']:p['author_supported']='YES'
  d['correct_choice_ids']=[c['id'] for c in d['choices']];d['visible_content_sha256']=dh({k:d[k] for k in visiblekeys})
 elif mutation=='helper_wording':d['stem']+=' Use the notes.';d['visible_content_sha256']=dh({k:d[k] for k in visiblekeys})
 try:validate(d)
 except ValueError:negative.append(mutation)
 else:raise ValueError('Mutation did not fail: '+mutation)
summary={'status':'PASS','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_root_worker_full_record_and_visible_bindings':10,'native_finding_report_bindings':10,'new_drafts':10,'choices_and_distinct_complete_korean_rationales':40,'types':{'SBA':5,'mixed_SATA':5},'all_correct_sata':0,'fresh_controlling_official_sources':27,'source_raw_text_retrieval_bindings':'PASS_ALL_OPTION_AND_SCENARIO_AUTHORITIES','critical_source_section_anchors':len(anchors),'nearest_final_full_stem_all_options_read':32,'nearest_full_read_including_discarded_design':35,'negative_mutations_rejected':negative,'new_public_IDs':0,'source_blocked_drafts':0,'canonical_independent_author_coverage_credit':0,'full_repository_QA':'NOT_RUN_AUTHOR_ARTIFACT_SCOPE_ONLY','publication_compile_activation_root_integration':'NOT_RUN_ROOT_ONLY','report_sha256':sha(RP.read_bytes()),'worker_commit_at_check':git('rev-parse','HEAD').decode().strip()}
if '--receipt' in sys.argv:writepath=E/'validation-receipt.json';writepath.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
