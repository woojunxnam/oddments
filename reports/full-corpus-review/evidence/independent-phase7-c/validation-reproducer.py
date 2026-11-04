import collections,datetime,gzip,hashlib,json,subprocess,sys
from pathlib import Path
assert Path.cwd()==Path('/workspace/independent-phase7-c')
sys.path.insert(0,'/workspace/oddments/scripts')
from review_queue import digest,validate_result,validate_independent_evidence
from export_legacy_review_input import export
from qa_common import semantic_content_hash
from jsonschema import Draft202012Validator
A=json.load(open('/tmp/independent-phase7-c-assignment.json'));PACK=json.load(open('/tmp/independent-phase7-c-visible.json'));FAM=json.load(open('/tmp/independent-phase7-c-family-only.json'))
P=Path('reports/full-corpus-review/independent-phase7-c-review.json');E=Path('reports/full-corpus-review/evidence/independent-phase7-c');D=json.load(open(P));checks=[]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def tsha(s):return hashlib.sha256(s.encode()).hexdigest()
def bound(x):
 p=Path(x['evidence_path']);assert not p.is_absolute()and'..'not in p.parts and str(p).startswith(str(E)+'/')
 assert p.is_file()and sha(p)==x['evidence_sha256'],str(p)
def ok(s):checks.append(s)
assert len(A['question_hashes'])==40 and set(A['question_hashes'])=={f'MA-CASE-{n:04d}'for n in range(1001,1041)}
assert D['question_hashes']==PACK['question_hashes']==A['question_hashes']and D['assignment_job_id']==A['job_id']
assert D['actor_provenance']=={'actor_id':'/root/independent_case_c','session_id':'/root/independent_case_c'}and A['worker']==D['actor_provenance']['actor_id']
assert D['auditor']=='GPT'and D['auditor_instance']=='GPT:/root/independent_case_c:independent-legacy-20261103'and D['reviewed_at']=='2026-11-04'
assert D['stage']=='independent-legacy'and D['independent_of_authors']is True and D['canonical_audit']is False and D['canonical_release_credit']==0
for root in [Path.cwd(),Path('/workspace/oddments')]:assert export(A,root)['records']==PACK['records']
ok('Exact40assignment/currentwhole-recordcanonicalhashes/completevisiblepacketmatchworkerANDcurrentROOT; sameactualactor/session/stableinstance; noledger/hiddentruthmodelinput')

Q={r['question_id']:r['original_visible_content']for r in PACK['records']};assert len(D['records'])==40 and {r['question_id']for r in D['records']}==set(Q)
CR={'jurisprudence_reasoning','practice_plausibility','authentic_distractors','wording_not_guessable','reasoning_not_trivia','natural_rule_combination','appropriate_drug_context','distinct_from_bank','not_schedule_flashcard','public_style_without_copying'}
choice_count=core_count=explanation_count=0;unique=set()
for r in D['records']:
 q=Q[r['question_id']];l=r['legal_review'];rr=r['realism_review'];meta=FAM[r['question_id']]
 assert r['record_sha256']==meta['record_sha256']==A['question_hashes'][r['question_id']]and r['record_sha256']is not None
 assert r['family_id']==meta['family_id']and r['collection']==meta['collection']
 assert r['stem']==q['stem']and r['stem_sha256']==tsha(q['stem'])and q['question_type']=='SATA'
 assert l['stored_key']==q['correct_choice_ids']and len(q['choices'])==5
 assert len(l['per_choice_findings'])==5
 selected=[]
 for c,f in zip(q['choices'],l['per_choice_findings']):
  assert (c['id'],c['text'])==(f['choice_id'],f['option_text'])and f['option_text_sha256']==tsha(c['text'])
  assert f['support_status']==('SUPPORTED'if f['independent_supported']else'UNSUPPORTED')and f['finding_ko']and f['authority_bindings']
  if f['independent_supported']:selected.append(c['id'])
  for a in f['authority_bindings']:
   bound(a);assert a['source_type']=='PUBLIC_OFFICIAL'and a['official_url'].startswith('https://')and a['exact_section']and a['law_checked_date']=='2026-11-04'and a['version_or_effective_date_status']and a['http_status']==200
  x=l['original_explanation_review']['choices'][c['id']]
  assert x['read_full']is True and x['original_text']==q['explanation']['choice_analysis'][c['id']]and x['sha256']==tsha(x['original_text'])and x['finding_ko']
  choice_count+=1;explanation_count+=1;unique.add(c['text'])
 assert selected==l['independently_expected_key']==l['stored_key']and l['existing_answer_correct']=='YES'and l['verdict']=='KEEP'
 x=l['original_explanation_review']['core'];assert x['read_full']is True and x['original_text']==q['explanation']['core_reasoning']and x['sha256']==tsha(x['original_text'])and x['finding_ko'];core_count+=1
 b=l['original_explanation_review']['learning_boundary'];assert b['read_full']is True and b['original_text']==q['explanation']['learning_boundary']and b['sha256']==tsha(b['original_text'])
 if int(r['question_id'][-4:])in [1018,1019,1023]:assert x['verdict']=='SUPPORTED_FEDERAL_RULE_WITH_STATE_SCOPE_NOTE'and 'exception'in x['finding_ko']
 assert all(r['read_scope'][k]is True for k in ['original_stem','every_choice','stored_key','korean_core_explanation','every_choice_explanation','input_packet_only'])
 assert all(r['read_scope'][k]is False for k in ['prior_author_independent_editor_verdict_read','hidden_statement_truth_exposed_or_used','ledger_read'])
 assert set(rr['criteria'])==set(rr['criterion_findings_ko'])==CR and all(type(v)is bool for v in rr['criteria'].values())
 assert all(isinstance(t,str)and len(t)>60 for t in rr['criterion_findings_ko'].values())
 expected='PASS'if all(rr['criteria'].values())else'FAIL';assert rr['verdict']==expected
 assert r['disposition']==('INDEPENDENT_ASSESSED'if expected=='PASS'else'NEEDS_REMEDIATION')
 assert r['safe_hold_recommended']==(r['disposition']!='INDEPENDENT_ASSESSED')and r['release_eligible']is False and r['canonical_release_credit']==0
 bound(rr['duplicate_evidence']);bound({'evidence_path':rr['public_style_evidence_path'],'evidence_sha256':rr['public_style_evidence_sha256']})
assert choice_count==explanation_count==200 and core_count==40 and len(unique)==89
ok('All40literalstems/200options/40keys/40cores/200choiceexplanations/learningboundariesbound; independent89propositiontable=>all40SATAkeysets; allowed/required/conditionsfederalMAfindings')
ok('400individualcriterionvalues/findings; PASSiffall10true; wordingandimplausiblerecorddefectsindividual; archivepatternaloneisnotfailure; allreleasecredit0')

log=json.load(open(E/'retrieval-log.json'));assert len(log)==30 and len(D['sources'])==24
for r in log:
 if r['evidence_path']:
  bound(r);raw=Path(r['evidence_path']).read_bytes()
  if r['evidence_path'].endswith('.gz'):raw=gzip.decompress(raw)
 else:raw=Path(r['private_response_path']).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==r['raw_sha256']and len(raw)==r['bytes']and r['retrieved_at'].startswith('2026-11-04')
 if r['payload_type']=='PDF':assert raw.startswith(b'%PDF-')
 if r['source_id']=='supply-policy-guess':assert r['http_status']==404 and r['verification_status']=='HTTP_FAILURE_NOT_VERIFIED'
 if r['verification_status']=='VERIFIED_TARGETED_PRIMARY_TEXT_READ':assert r['http_status']==200 and b'Page Not Found'not in raw and b'Access Denied'not in raw
for s in D['sources']:
 bound(s);r=next(r for r in log if r['source_id']==s['source_id']);assert r['verification_status']=='VERIFIED_TARGETED_PRIMARY_TEXT_READ'and s['raw_payload_sha256']==r['raw_sha256']and s['retrieved_at']==r['retrieved_at']and s['law_checked_date']=='2026-11-04'
pm=next(r for r in log if r['source_id']=='ma-pmp-fields');st=next(r for r in log if r['source_id']=='nabp-public-style')
assert pm['evidence_path']is None and st['evidence_path']is None
assert st['raw_sha256']=='b8544f403990191075747b231c81cde4449c6eb83333cfb1d9f05b5e1273d30d'
assert all(sha(p)not in {pm['raw_sha256'],st['raw_sha256']}for p in E.glob('*.pdf'))
memo=json.load(open(E/'pmp-field-review-memo.json'));assert memo['raw_payload_sha256']==pm['raw_sha256']and '69-70'in memo['exact_section']
assert memo['current_link_evidence_sha256']==sha(memo['current_link_evidence_path'])
ok('All30actualHTTPpayloadrawSHAs/statuses; 24usedprimarysourcebindings; guessed404excluded; copyrightedPMP/publicsampleprivateandownmemoonly; Nov4notoldcache/effectivedateinference')

style=json.load(open('data/exam_style/mpje_style_profile.json'));Draft202012Validator(json.load(open('schemas/exam_style_profile.schema.json'))).validate(style)
assert style['content_hash']==semantic_content_hash(style,'style_profile')==D['style_profile']['semantic_hash']and sha('data/exam_style/mpje_style_profile.json')==D['style_profile']['file_sha256']
for x in D['governance']:assert sha(x['path'])==x['sha256']
for x in D['governing_schema_snapshots']:assert sha(x['path'])==x['file_sha256']
ok('4governance/runbook/styleversion+semanticHash/schemafileSHAs/currentstyleschemavalid; genuinefreshpublicformatPDFreadmemo')

N=json.load(open(E/'nearest-candidates.json'));config=json.load(open('site/practice-expansion/publication.json'));paths=['practice_expansion/2026-10-23/candidates/questions.json']+[x['path']for x in config['additional_banks']]
def project(q):return{k:q[k]for k in ['question_id','stem','choices']}
public={q['question_id']:project(q)for p in paths for q in json.load(open(p))['questions']};canonical={q['question_id']:project(q)for p in Path('data/questions').glob('*.json')for q in [json.load(open(p))]}
assert len(canonical)==N['canonical_count']==439 and len(public)==N['public_count']==2346
assert sha(N['selection_path'])==N['selection_sha256'];selected=set(json.load(open(N['selection_path']))['recommended_ids'])
assert set(N['assigned_recommended'])==set(Q)&selected==set(json.load(open('/tmp/independent-phase7-c-default-only.json'))['recommended_ids'])
reads=set()
for n in N['records']:
 for kind in ['canonical_top3','public_top3','current_default_top1']:
  for near in n[kind]:
   q=near['question'];assert set(q)=={'question_id','stem','choices'}and q==(canonical if kind=='canonical_top3'else public)[q['question_id']]
   assert q['question_id']!=n['question_id']and 0<=near['score']<=1
   if kind=='current_default_top1':assert q['question_id']in selected
  reads.add(n[kind][0]['question']['question_id'])
scope=json.load(open(E/'nearest-read-scope.json'));assert set(scope['actual_read_question_ids'])==reads and len(reads)==53 and len(reads-set(Q))==37
assert scope['all_top3_read']is False and scope['hidden_truth_or_prior_verdicts_exposed']is False
ok('Canonical439/public2346fullsafeprojectionliteralcomparison; actualtop1canonical/public/default53distinct37outside/15canonical; selectionpointintimeSHA; noanswers/truth/verdictinprojection')

for k,values in [('existing_answer_correct',[r['legal_review']['existing_answer_correct']for r in D['records']]),('legal_verdicts',[r['legal_review']['verdict']for r in D['records']]),('realism_verdicts',[r['realism_review']['verdict']for r in D['records']]),('dispositions',[r['disposition']for r in D['records']])]:assert dict(collections.Counter(values))==D['summary'][k]
assert D['summary']['realism_verdicts']=={'FAIL':30,'PASS':10}
test={k:D[k]for k in ['stage','independent_of_authors','auditor','auditor_instance','actor_provenance','canonical_audit','canonical_release_credit']};test.update(question_hashes=A['question_hashes'],worker_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),results=[dict(question_id=r['question_id'],disposition=r['disposition'],evidence_path=str(P),evidence_sha256=sha(P))for r in D['records']])
validate_result(A,test)
for r in test['results']:validate_independent_evidence({**A,'result':test},r,D)
ok('Summarycomputedfrom40individualrecords; currentROOTvalidate_result+validate_independent_evidence40precommitcontractPASS; exactHEADenvelopeonlyafterevidencecommit')

for p in E.glob('*.txt'):p.write_text('\n'.join(x.rstrip()for x in p.read_text().splitlines()).strip()+'\n')
for line in subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],text=True).splitlines():assert line[3:]==str(P)or line[3:].startswith(str(E)+'/'),line
subprocess.run(['git','diff','--check'],check=True)
ok('Dedicatedreport/evidenceprefixonly; nooriginal/key/ledger/queue/generatedwrites; whitespacenormalizedextractionswithoutchangingrawcaptures')
out=E/'validation.json';v=dict(status='PASS',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),validator_path=str(Path(__file__).relative_to(Path.cwd())),validator_sha256=sha(__file__),checks=checks,not_run=['Fullrepository/browserQA:evidenceonly','Canonicalaudit/releasevalidator:independentlegacyonly','Queue-submit/integrate:rootcontrolleronly'],scope='Computerconsistency/hashchecksareseparatefromactualprimary/stem/options/explanationreadingsandindependentqualitativelegal/realismjudgments.')
out.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');D['completed_at']=v['checked_at'];D['validation']=dict(status='PASS',evidence_path=str(out),evidence_sha256=sha(out),full_repository_QA='NOT_RUN:evidenceonly',canonical_audit_validator='NOT_RUN:independentlegacyonly');P.write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':len(checks),'summary':D['summary'],'report_sha256':sha(P)},ensure_ascii=False,indent=2))
