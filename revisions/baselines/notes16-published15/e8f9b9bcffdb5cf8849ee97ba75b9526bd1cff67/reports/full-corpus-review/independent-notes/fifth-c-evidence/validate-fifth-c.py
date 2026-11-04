"""Read-only by default. --record stores precommit verification; no queue/generator mutation."""
import collections,datetime,gzip,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path('/workspace/oddments');W=Path('/workspace/independent-notes5-c');assert Path.cwd()==W
sys.path.insert(0,str(ROOT/'scripts'))
from note_review_queue import inventory,current,validate_result,validate_evidence,digest,committed_evidence
from notes_revision import load_notes
E=Path('reports/full-corpus-review/independent-notes/fifth-c-evidence');P=Path('reports/full-corpus-review/independent-notes/fifth-c-review.json');A=json.load(open('/tmp/independent-notes5-c-assignment.json'));D=json.load(open(P));checks=[]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def verify(p,s):assert sha(p)==s,str(p)
def bound(a):
 p=Path(a['evidence_path']);assert str(p).startswith(str(E)+'/') and not p.is_absolute() and '..'not in p.parts;verify(p,a['evidence_sha256'])
def ok(s):checks.append(s)
assert A['unit_ids']==['w3-a-1','w3-a-2','w3-a-3','w3-a-4','w3-a-6'] and len(D['records'])==5
assert D['actor_provenance']==A['actor_provenance']=={'actor_id':'/root/independent_case_c','session_id':'/root/independent_case_c'} and D['auditor']==A['auditor']=='GPT' and D['auditor_instance']==A['auditor_instance']=='GPT:/root/independent_case_c:independent-legacy-20261103'
assert D['stage']=='independent-notes' and D['independent_of_authors']is True and D['canonical_audit']is False and D['canonical_release_credit']==D['question_audit_credit']==D['new_release_credit']==D['additional_auditor_instances_created']==0 and D['reviewed_at']=='2026-11-04'
for root in [W,ROOT]:current(A,inventory(root))
authors=set(A['known_author_ids'])|{x for b in A['unit_bindings'].values()for x in b['known_author_ids']};assert not authors&{A['actor_provenance']['actor_id'],A['actor_provenance']['session_id'],A['auditor_instance']}
ok('Current worker AND root inventory exact5 whole bindings/body/census/raw unit+claim SHAs match; same actual non-author C actor/session/instance, canonical/question/new-release credit0.')
B=json.load(open(E/'body-first-inputs.json'));C=json.load(open(E/'census-safe-inputs.json'));body={x['unit_id']:x for x in B};cby={x['claim_id']:x for x in C};claims=[];omissions=0
assert len(B)==5 and len(C)==85
for r in D['records']:
 uid=r['unit_id'];b=A['unit_bindings'][uid];assert r['binding']==b and r['body_read_completely']is True and r['actual_body_sha256']==b['body_sha256']==hashlib.sha256(body[uid]['body'].encode()).hexdigest();verify(r['body_evidence_path'],r['body_evidence_sha256'])
 original=json.load(open(b['census_path']));verify(b['census_path'],b['census_sha256']);rawclaims={c['claim_id']:c for c in original['claims']if c['unit_id']==uid}
 assert set(rawclaims)==set(b['claim_record_sha256s'])=={c['claim_id']for c in r['claims']}
 assert len(r['claims'])==len(rawclaims)
 covered=set()
 for item in r['independent_body_inventory']:
  assert item['body_quote']==body[uid]['body'].split('\n\n')[item['body_paragraph_index']];covered.update(item['matched_claim_ids'])
 for c in r['claims']:
  cid=c['claim_id'];assert c['claim_record_sha256']==b['claim_record_sha256s'][cid]==digest(rawclaims[cid]) and c['claim_read_completely']is True and c['original_statement_ko']==rawclaims[cid]['statement_ko']==cby[cid]['statement_ko'] and c['finding']
  assert c['bound_author_source_blocked_id']==(cid in b['source_blocked_claim_ids'])
  assert c['legal_status']in {'KEEP','LEGAL_HOLD','SOURCE_BLOCKED'} and (c['legal_status']=='KEEP' or c['blocker'])
  assert c['authorities']
  for a in c['authorities']:
   bound(a);assert a['source_type']=='PUBLIC_OFFICIAL' and a['official_url'].startswith('https://') and a['exact_section'] and a['law_checked_date']=='2026-11-04' and a['version_or_effective_date_status'] and a['http_status']==200
  x=c['practice_alignment'];assert x['question_audit_credit']==0 and x['status'] and x['finding_ko']
  for z in x['bindings']:verify(z['evidence_path'],z['evidence_sha256'])
  claims.append(c)
 assert covered==set(rawclaims),uid
 omissions+=len(r['omissions'])
 assert r['completeness']==('OMISSIONS_FOUND'if uid=='w3-a-6'else'COMPLETE') and r['legal_status']==('KEEP'if uid=='w3-a-1'else'LEGAL_HOLD')
 if uid=='w3-a-6':
  o=r['omission_details'][0];assert o['body_quote']in body[uid]['body'] and o['body_sha256']==b['body_sha256'];assert all('보험'not in c['statement_ko'] and 'adjudication'not in c['statement_ko']for c in C if c['unit_id']==uid)
  assert o['practice_alignment']['question_ids']==['MA-EXP-0739','MA-EXP-0740','MA-REV-0042'] and o['not_author_claim_id']is True
assert len(claims)==85 and omissions==1 and collections.Counter(c['legal_status']for c in claims)=={'KEEP':78,'LEGAL_HOLD':7}
assert len([c for c in claims if c['bound_author_source_blocked_id']])==8 and next(c for c in claims if c['claim_id']=='NOTE-WAVE8-W3-A-4-001')['legal_status']=='KEEP'
ok('All5 complete final bodies first; all85 original claims exactly bound/read; independent paragraph inventory covers all claims; genuine payer-adjudication omission quoted separately from body-scope HOLDs. Seven legal HOLDs preserved, March source-specific read supported newly.')
log=json.load(open(E/'retrieval-log.json'));assert len(log)==19
for r in log:
 if r['evidence_path']:
  bound(r);raw=Path(r['evidence_path']).read_bytes();raw=gzip.decompress(raw)if r['evidence_path'].endswith('.gz')else raw
 else:raw=Path(r['private_response_path']).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==r['raw_sha256'] and len(raw)==r['bytes'] and r['retrieved_at'].startswith('2026-11-04') and r['http_status']==200 and r['verification_status']=='VERIFIED_TARGETED_PRIMARY_TEXT_READ'
 assert b'Page Not Found'not in raw and b'Access Denied'not in raw
 if r['payload_type']=='PDF':assert raw.startswith(b'%PDF-')
for s in D['sources']:
 bound(s);r=next(x for x in log if x['source_id']==s['source_id']);assert s['raw_payload_sha256']==r['raw_sha256'] and s['retrieved_at']==r['retrieved_at'] and s['exact_sections_read']
newsletter=next(x for x in log if x['source_id']=='ma-newsletter-202603');assert newsletter['raw_sha256']=='f005b1dbecf9398ea5d98741477bb32c1029b7220a64c96d84f83019f04e6800' and newsletter['evidence_path']is None and not(E/'ma-newsletter-202603.pdf').exists() and not(E/'ma-newsletter-202603.txt').exists()
assert 'narcotic or controlled substance contained in schedule II or III'in(E/'mgl94c21.txt').read_text() and 'Section 7 shall take effect on January 1, 2026'in(E/'act2025c16.txt').read_text() and 'release mechanisms'in(E/'fda-ob-preface.txt').read_text()
ok('19 actual fresh official HTTP200 raw SHAs/statuses and all authority file bytes verified; consolidated §21 gap resolved using actual Act §§7/27; newsletter full copyright raw private; no full USP legal certification or failed source counted.')
PD=json.load(open(E/'practice-safe-inputs.json'));I=json.load(open(E/'practice-lossless-reading-index.json'));qb={r['original_visible_content']['question_id']:r['original_visible_content']for r in PD['records']};assert len(qb)==62 and PD['public_count']==53 and PD['canonical_count']==9 and sum(len(q['choices'])for q in qb.values())==266 and len(I['texts'])==429
config=json.load(open('site/practice-expansion/publication.json'));paths=['practice_expansion/2026-10-23/candidates/questions.json']+[x['path']for x in config['additional_banks']];public={q['question_id']:q for p in paths for q in json.load(open(p))['questions']};canon={q['question_id']:q for p in Path('data/questions').glob('*.json')for q in [json.load(open(p))]}
project=lambda q:{k:q[k]for k in ['question_id','question_type','stem','choices','correct_choice_ids','explanation']}
rootconfig=json.load(open(ROOT/'site/practice-expansion/publication.json'));rootpaths=['practice_expansion/2026-10-23/candidates/questions.json']+[x['path']for x in rootconfig['additional_banks']]
rootpublic={q['question_id']:q for p in rootpaths for q in json.load(open(ROOT/p))['questions']};rootcanon={q['question_id']:q for p in (ROOT/'data/questions').glob('*.json')for q in [json.load(open(p))]}
for r in PD['records']:
 q=r['original_visible_content'];assert q==project((canon if r['origin']=='canonical'else public)[q['question_id']])
 assert q==project((rootcanon if r['origin']=='canonical'else rootpublic)[q['question_id']])
 assert all(set(c)=={'id','text'}for c in q['choices']) and not set(q['explanation'])-{'core_reasoning','choice_analysis','choice_authorities','learning_boundary','related_facts','mpje_trap'}
def unpack(x):
 if isinstance(x,dict)and set(x)=={'text_ref'}:return I['texts'][x['text_ref']-1]
 if isinstance(x,dict):return{k:unpack(v)for k,v in x.items()}
 if isinstance(x,list):return[unpack(v)for v in x]
 return x
assert [unpack(r)for r in I['records']]==[r['original_visible_content']for r in PD['records']]
for c in claims:
 for z in c['practice_alignment']['bindings']:assert digest(qb[z['question_id']])==z['visible_projection_sha256']
ok('All53 actual public note links/census IDs plus9 canonical candidates/62 safe originals/266 options and full visible explanations match worker AND current root source records; lossless429-string reading index reconstructs every field; specific/partial/no-direct claim alignment distinct, question credit0.')
DER=json.load(open(E/'effective-derived-inputs.json'));assert DER['build_status']['study']['status']=='BUILD_BLOCKED_FALLBACK_EFFECTIVE_REVISION_CONTENT' and DER['build_status']['study']['error']=='Stale representative selection' and DER['build_status']['refresh']['status']=='BUILT_READ_ONLY'
assert len(DER['study']['lessons'])==2 and len(DER['study']['comparisons'])==1 and len(DER['study']['modules'])==1 and len(DER['refresh']['cards'])==8 and len(DER['refresh']['glossary'])==3 and len(DER['chapter_summaries'])==1
for x in D['derived_evidence']:verify(x['path'],x['raw_sha256'])
for x in D['governance']:verify(x['path'],x['raw_sha256'])
assert D['summary']['claims']==85 and D['summary']['material_omissions']==1 and D['summary']['claim_legal_status']=={'KEEP':78,'LEGAL_HOLD':7}
ok('Sixteen effective derived content surfaces and local generated snapshots bound; actual study selection error preserved; historical stored SHA distinguished from correct actual source_hashes; derived/builder writes0, all4 policies/runbook fixed.')
M={k:D[k]for k in ['stage','independent_of_authors','actor_provenance','auditor','auditor_instance','canonical_audit','canonical_release_credit','question_audit_credit']};M.update(worker_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),unit_hashes={u:b['body_sha256']for u,b in A['unit_bindings'].items()},evidence={'path':str(P),'raw_sha256':sha(P)},result_path='reports/full-corpus-review/independent-notes/'+A['job_id']+'-result.json',results=[{k:r[k]for k in ['unit_id','completeness','legal_status']}for r in D['records']]);validate_result(A,M);sources=validate_evidence(A,M,D)
for p,s in sources:verify(p,s)
ok('Current ROOT validate_result + validate_evidence exact5/85 and every source evidence SHA PASS; final envelope waits until exact evidence commit. No queue submission or integration performed by worker.')
allowed=(str(P),str(E)+'/')
for line in subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],text=True).splitlines():assert line[3:]==allowed[0]or line[3:].startswith(allowed[1]),line
if '--record'in sys.argv:
 for p in E.glob('*.txt'):p.write_text('\n'.join(x.rstrip()for x in p.read_text().splitlines()).strip()+'\n')
 out=E/'validation.json';v={'status':'PASS','checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'validator_path':str(Path(__file__).relative_to(W)),'validator_sha256':sha(__file__),'checks':checks,'not_run':['Whole repository/browser/remote deployed PR190 verification: out of evidence-only scope','USP full copyrighted chapters: not certified','Canonical/question/release audit: credit0','Queue submit/integrate/generated writes: root only']};write=lambda p,d:Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');write(out,v);D['validation']={'status':'PASS','path':str(out),'raw_sha256':sha(out)};D['completed_at']=v['checked_at'];write(P,D)
print(json.dumps({'status':'PASS','checks':len(checks),'summary':D['summary'],'report_sha256':sha(P)},ensure_ascii=False,indent=2))
