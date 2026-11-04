"""Evidence consistency verifier; qualitative legal/realism findings require the recorded actual readings."""
import collections,datetime,gzip,hashlib,json,subprocess,sys
from pathlib import Path
assert Path.cwd()==Path('/workspace/independent-phase8-c')
sys.path.insert(0,'/workspace/oddments/scripts')
from review_queue import validate_result,validate_independent_evidence
from export_legacy_review_input import export
from qa_common import semantic_content_hash
from jsonschema import Draft202012Validator
A=json.load(open('/tmp/independent-phase8-c-assignment.json'));PACK=json.load(open('/tmp/independent-phase8-c-visible.json'));FAM=json.load(open('/tmp/independent-phase8-c-family-only.json'))
E=Path('reports/full-corpus-review/evidence/independent-phase8-c');P=Path('reports/full-corpus-review/independent-phase8-c-review.json');D=json.load(open(P));checks=[]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
tsha=lambda s:hashlib.sha256(s.encode()).hexdigest()
def bound(x):
 p=Path(x['evidence_path']);assert not p.is_absolute() and '..' not in p.parts and str(p).startswith(str(E)+'/')
 assert p.is_file() and sha(p)==x['evidence_sha256'],str(p)
def ok(s):checks.append(s)
assert set(A['question_hashes'])=={f'MA-EXP-{n:04d}'for n in range(9,49)}
assert D['question_hashes']==PACK['question_hashes']==A['question_hashes'] and D['assignment_job_id']==A['job_id']
assert D['actor_provenance']=={'actor_id':'/root/independent_case_c','session_id':'/root/independent_case_c'} and A['worker']==D['actor_provenance']['actor_id']
assert D['auditor']=='GPT' and D['auditor_instance']=='GPT:/root/independent_case_c:independent-legacy-20261103' and D['reviewed_at']=='2026-11-04'
assert D['stage']=='independent-legacy' and D['independent_of_authors']is True and D['canonical_audit']is False and D['canonical_release_credit']==D['additional_auditor_instances_created']==0
for root in [Path.cwd(),Path('/workspace/oddments')]:assert export(A,root)['records']==PACK['records']
for line in Path('/workspace/oddments/reports/full-corpus-review/question-ledger.jsonl').read_text().splitlines():
 row=json.loads(line);qid=row['question_id']
 if qid in A['question_hashes']:assert row['collection']==FAM[qid]['collection'] and row['content_sha256']==A['question_hashes'][qid]
# Whole source records/ledger are hash/projection inputs only, never model-visible judgments.
ok('Exact40 assigned current whole-record hashes match worker AND current root safe export; ledger only machine ID/collection/SHA projection; same actual C actor/session/instance; zero new canonical credit.')
for k in ['input_provenance','prior_exposure_check','independent_option_findings','source_attempt_log','source_coverage']:
 x=D[k];assert sha(x['path'])==x['sha256']
exposure=json.load(open(D['prior_exposure_check']['path']));assert exposure['matching_assigned_ids']==[] and exposure['same_actual_instance']is True
facts=json.load(open(D['independent_option_findings']['path']))['propositions'];fact={x['option_text']:x for x in facts};assert len(fact)==77
Q={r['question_id']:r['original_visible_content']for r in PACK['records']};assert len(D['records'])==40 and {r['question_id']for r in D['records']}==set(Q)
CR={'jurisprudence_reasoning','practice_plausibility','authentic_distractors','wording_not_guessable','reasoning_not_trivia','natural_rule_combination','appropriate_drug_context','distinct_from_bank','not_schedule_flashcard','public_style_without_copying'}
counts=collections.Counter();unique=set()
sources={s['source_id']:s for s in D['sources']}
for r in D['records']:
 q=Q[r['question_id']];l=r['legal_review'];rr=r['realism_review'];meta=FAM[r['question_id']]
 assert r['record_sha256']==meta['record_sha256']==A['question_hashes'][r['question_id']] and r['family_id']==meta['family_id'] and r['collection']==meta['collection']
 assert r['stem']==q['stem'] and r['stem_sha256']==tsha(q['stem']) and l['stored_key']==q['correct_choice_ids']
 negative='INCORRECT'in q['stem'];expected=[]
 assert l['polarity']==('INCORRECT_SINGLE'if negative else'AFFIRMATIVE_SATA'if q['question_type']=='SATA'else'AFFIRMATIVE_SINGLE')
 assert len(l['per_choice_findings'])==len(q['choices'])==4
 for c,f in zip(q['choices'],l['per_choice_findings']):
  assert (c['id'],c['text'])==(f['choice_id'],f['option_text']) and f['option_text_sha256']==tsha(c['text'])
  assert f['independent_supported']==fact[c['text']]['independent_supported'] and f['finding_ko']==fact[c['text']]['finding_ko']
  assert f['support_status']==('SUPPORTED'if f['independent_supported']else'UNSUPPORTED') and f['authority_bindings']
  if (not f['independent_supported']if negative else f['independent_supported']):expected.append(c['id'])
  for a in f['authority_bindings']:
   bound(a);s=sources[a['source_id']]
   assert a['official_url']==s['official_url'] and a['raw_payload_sha256']==s['raw_payload_sha256'] and a['evidence_sha256']==s['evidence_sha256']
   assert a['source_type']=='PUBLIC_OFFICIAL' and a['official_url'].startswith('https://') and a['exact_section'] and a['law_checked_date']=='2026-11-04' and a['version_or_effective_date_status'] and a['http_status']==200
  x=l['original_explanation_review']['choices'][c['id']]
  assert x['read_full']is True and x['original_text']==q['explanation']['choice_analysis'][c['id']] and x['sha256']==tsha(x['original_text']) and x['finding_ko']
  counts['choices']+=1;counts['choice_explanations']+=1;unique.add(c['text'])
 assert expected==l['independently_expected_key']==l['stored_key'] and l['existing_answer_correct']=='YES' and l['verdict']=='KEEP' and l['blocker']is None
 assert q['question_type']=='SATA' or len(expected)==1
 for key,original in [('core',q['explanation']['core_reasoning']),('learning_boundary',q['explanation']['learning_boundary'])]:
  x=l['original_explanation_review'][key];assert x['read_full']is True and x['original_text']==original and x['sha256']==tsha(original) and x['finding_ko'];counts[key]+=1
 assert all(r['read_scope'][k]is True for k in ['original_stem','every_choice','stored_key','korean_core_explanation','every_choice_explanation','learning_boundary','input_packet_only','ledger_metadata_only_machine_check'])
 assert all(r['read_scope'][k]is False for k in ['prior_author_independent_editor_verdict_read','hidden_statement_truth_exposed_or_used','ledger_prior_verdict_read','ledger_full_record_model_read','prior_same_id_exposure_found'])
 assert set(rr['criteria'])==set(rr['criterion_findings_ko'])==CR and all(type(v)is bool for v in rr['criteria'].values())
 assert all(isinstance(v,str) and len(v)>60 and r['question_id']in v for v in rr['criterion_findings_ko'].values())
 verdict='PASS'if all(rr['criteria'].values())else'FAIL';assert rr['verdict']==verdict and rr['decision']==('KEEP'if verdict=='PASS'else'MAJOR_REWRITE')
 assert r['disposition']==('INDEPENDENT_ASSESSED'if verdict=='PASS'else'NEEDS_REMEDIATION') and r['safe_hold_recommended']==(verdict!='PASS') and r['release_eligible']is False and r['canonical_release_credit']==0
 bound(rr['duplicate_evidence']);bound({'evidence_path':rr['public_style_evidence_path'],'evidence_sha256':rr['public_style_evidence_sha256']})
 counts[q['question_type']]+=1;counts['negative']+=negative
assert counts=={'choices':160,'choice_explanations':160,'core':40,'learning_boundary':40,'SBA':30,'SATA':10,'negative':10} and len(unique)==77
ok('All40 literal stems/160 options/40 keys/40 cores/160 option explanations/boundaries bound; independent77 propositions reproduce exact SATA/SBA/INCORRECT key sets, all unique single answers.')
ok('400 individual actual-question criterion findings; PASS iff all10 true; editorial needs-remediation scope separate from legal KEEP; actual archive/nearest comparisons, no numeric or archive automatic failure.')
log=json.load(open(E/'retrieval-log.json'));assert len(log)==11 and len(sources)==8
for r in log:
 if r['evidence_path']:
  bound(r);raw=Path(r['evidence_path']).read_bytes()
  if r['evidence_path'].endswith('.gz'):raw=gzip.decompress(raw)
 else:raw=Path(r['private_response_path']).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==r['raw_sha256'] and len(raw)==r['bytes'] and r['retrieved_at'].startswith('2026-11-04') and r['http_status']==200
 assert b'Page Not Found'not in raw and b'Access Denied'not in raw
 if r['payload_type']=='PDF':assert raw.startswith(b'%PDF-')
for s in sources.values():
 bound(s);r=next(x for x in log if x['source_id']==s['source_id']);assert r['verification_status']=='VERIFIED_TARGETED_PRIMARY_TEXT_READ' and s['raw_payload_sha256']==r['raw_sha256'] and s['retrieved_at']==r['retrieved_at']
assert sum(x['verification_status']=='OFFICIAL_CONTEXT_TARGET_READ'for x in log)==3
style_memo=json.load(open(E/'public-style-review-memo.json'));raw=Path('/tmp/independent-phase7-c-nabp-sample.pdf').read_bytes()
assert hashlib.sha256(raw).hexdigest()==style_memo['raw_payload_sha256']=='b8544f403990191075747b231c81cde4449c6eb83333cfb1d9f05b5e1273d30d'
oldlog=json.load(open('/workspace/oddments/reports/full-corpus-review/evidence/independent-phase7-c/retrieval-log.json'));origin=next(x for x in oldlog if x['source_id']=='nabp-public-style')
assert style_memo['original_retrieved_at']==origin['retrieved_at'] and style_memo['original_http_status']==origin['http_status']==200 and style_memo['sample_wording_reproduced']is False and style_memo['used_as_legal_authority']is False
assert not(E/'nabp-eltp.html.gz').exists() and not(E/'nabp-eltp.txt').exists()
ok('11 genuine Nov4 official HTTP200 captures/8 used primary/3 context; every raw payload SHA verified; adoption/version/unknown commencement separate. NABP licensing raw private; sample same-day cache original timestamp/SHA preserved, style only.')
style=json.load(open('data/exam_style/mpje_style_profile.json'));Draft202012Validator(json.load(open('schemas/exam_style_profile.schema.json'))).validate(style)
assert style['content_hash']==semantic_content_hash(style,'style_profile')==D['style_profile']['semantic_hash'] and sha('data/exam_style/mpje_style_profile.json')==D['style_profile']['file_sha256']
for x in D['governance']:assert sha(x['path'])==x['sha256']
for x in D['governing_schema_snapshots']:assert sha(x['path'])==x['file_sha256']
ok('4 governance policies/runbook/current style profile semantic+raw SHA/schema snapshots verified; no AGENTS files discovered in applicable paths.')
N=json.load(open(E/'nearest-candidates.json'));config=json.load(open('site/practice-expansion/publication.json'));paths=['practice_expansion/2026-10-23/candidates/questions.json']+[x['path']for x in config['additional_banks']]
project=lambda q:{k:q[k]for k in ['question_id','stem','choices']}
public={q['question_id']:project(q)for p in paths for q in json.load(open(p))['questions']};canonical={q['question_id']:project(q)for p in Path('data/questions').glob('*.json')for q in [json.load(open(p))]}
assert len(canonical)==N['canonical_count']==439 and len(public)==N['public_count']==2346 and sha(N['selection_path'])==N['selection_sha256']
selected=set(json.load(open(N['selection_path']))['recommended_ids']);assert N['assigned_recommended']==[] and not(set(Q)&selected)
reads=set()
for n in N['records']:
 for kind in ['canonical_top3','public_top3','current_default_top1']:
  for near in n[kind]:
   q=near['question'];assert set(q)=={'question_id','stem','choices'} and q==(canonical if kind=='canonical_top3'else public)[q['question_id']] and q['question_id']!=n['question_id'] and 0<=near['score']<=1
   if kind=='current_default_top1':assert q['question_id']in selected
  reads.add(n[kind][0]['question']['question_id'])
scope=json.load(open(E/'nearest-read-scope.json'));assert set(scope['actual_read_question_ids'])==reads and len(reads)==55 and len(reads-set(Q))==25 and sum(x.startswith('MA-Q-')for x in reads)==12 and scope['all_top3_read']is False
assert 'MA-Q-0278'in reads # Extra semantic comparison for EXP0030 was actually read as another item's top1.
ok('Canonical439/public2346 safe projections literally match source banks; actual top1 canonical/public/default55 distinct25 outside/12 canonical; all40 default membership absent; all-top3 reading not claimed; scores not verdicts.')
for k,values in [('existing_answer_correct',[r['legal_review']['existing_answer_correct']for r in D['records']]),('legal_verdicts',[r['legal_review']['verdict']for r in D['records']]),('realism_verdicts',[r['realism_review']['verdict']for r in D['records']]),('dispositions',[r['disposition']for r in D['records']])]:assert dict(collections.Counter(values))==D['summary'][k]
assert D['summary']['realism_verdicts']=={'FAIL':28,'PASS':12}
M={k:D[k]for k in ['stage','independent_of_authors','auditor','auditor_instance','actor_provenance','canonical_audit','canonical_release_credit']};M.update(question_hashes=A['question_hashes'],worker_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),results=[dict(question_id=r['question_id'],disposition=r['disposition'],evidence_path=str(P),evidence_sha256=sha(P))for r in D['records']])
validate_result(A,M)
for r in M['results']:validate_independent_evidence({**A,'result':M},r,D)
ok('Current ROOT validate_result + validate_independent_evidence40 precommit PASS; recomputed counters; exact postcommit envelope deliberately not committed.')
for p in E.glob('*.txt'):p.write_text('\n'.join(x.rstrip()for x in p.read_text().splitlines()).strip()+'\n')
for line in subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],text=True).splitlines():assert line[3:]==str(P)or line[3:].startswith(str(E)+'/'),line
subprocess.run(['git','diff','--check'],check=True)
ok('Dedicated report/evidence prefixes only; no original/key/source-bank/ledger/queue/shared-generated edits; convenience text whitespace normalized without changing official raw captures.')
out=E/'validation.json';v=dict(status='PASS',checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),validator_path=str(Path(__file__).relative_to(Path.cwd())),validator_sha256=sha(__file__),checks=checks,not_run=['Full repository/browser QA: evidence-only task','Canonical admission/release validator: independent-legacy credit0','Queue submit/integrate/builders: root only'],scope='Machine consistency checks do not substitute for recorded actual raw primary/stem/options/explanation readings and independent qualitative judgments.')
out.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n');D['completed_at']=v['checked_at'];D['validation']=dict(status='PASS',evidence_path=str(out),evidence_sha256=sha(out),full_repository_QA='NOT_RUN:evidence-only',canonical_release_validator='NOT_RUN:independent-legacy credit0');P.write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status='PASS',checks=len(checks),summary=D['summary'],report_sha256=sha(P)),ensure_ascii=False,indent=2))
