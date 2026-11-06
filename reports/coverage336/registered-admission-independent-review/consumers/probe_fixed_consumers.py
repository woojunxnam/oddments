"""Current H1/H2/H3 regressions; synthetic post-native handle only, no enrollment."""
from pathlib import Path
import copy,json,subprocess,tempfile
import canonical_admission as a
from verify_representative_protected import EXACT_FILES,PREFIXES
OUT=Path(__file__).resolve().parent;root=Path(tempfile.mkdtemp(prefix='fixed-consumer-',dir=OUT))
def put(p,raw=b'{}\n'):
 path=root/p;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
def git(*args):return subprocess.check_output(['git',*args],cwd=root)
for prefix in PREFIXES:(root/prefix).mkdir(parents=True,exist_ok=True)
for p in set(EXACT_FILES)|{a.NOTE,a.HOLDS,a.PREVIEW,a.PAYLOAD,a.BASELINE}|a.DERIVED:put(p)
put(a.REGISTRY,b'# synthetic committed registry fixture\n');put('site/app.js',b'// tracked source\n');put('.gitignore',b'site/ignored/\n')
metadata={a.ACTIVATION_PATH:b'{"synthetic":"E"}', 'revisions/canonical/SAFE-M.json':b'{"synthetic":"M"}', 'revisions/canonical/SAFE-N.json':b'{"synthetic":"N"}'}
for p,raw in metadata.items():put(p,raw)
git('init','--quiet');git('config','user.name','Independent Synthetic Reviewer');git('config','user.email','synthetic@example.invalid');git('add','.');git('commit','--quiet','-m','Synthetic committed consumer source');head=git('rev-parse','HEAD').decode().strip();checks=[]
def reject(label,fn):
 try:fn();raise AssertionError('Accepted '+label)
 except a.BoundaryViolation as e:checks.append({'check':label,'rejected':True,'error':str(e)})
a.require_committed_sources(root,head,metadata);checks.append({'check':'EXACT_COMMITTED_MNE_BYTES','accepted':True})
put('revisions/canonical/untracked-M.json',metadata['revisions/canonical/SAFE-M.json']);reject('H2_IDENTICAL_BUT_UNTRACKED_METADATA',lambda:a.require_committed_sources(root,head,{'revisions/canonical/untracked-M.json':metadata['revisions/canonical/SAFE-M.json']}));(root/'revisions/canonical/untracked-M.json').unlink()
reject('H2_WRONG_COMMITTED_METADATA_BYTES',lambda:a.require_committed_sources(root,head,{a.ACTIVATION_PATH:b'changed'}))
kpath='reports/canonical-successor/SAFE-coverage.json';a.require_clean_delivery_workspace(root,head,kpath)
put('site/verified-law/untracked.js',b'// untracked\n');reject('H1_UNTRACKED_PUBLISHABLE_FILE',lambda:a.require_clean_delivery_workspace(root,head,kpath));(root/'site/verified-law/untracked.js').unlink()
put('site/ignored/private.html',b'synthetic ignored material');reject('H1_IGNORED_PUBLISHABLE_FILE',lambda:a.require_clean_delivery_workspace(root,head,kpath));(root/'site/ignored/private.html').unlink()
q={'questions':[{'question_id':'SYNTHETIC','stem':'exact source fixture'}]};g={'sections':[],'marker':'exact guide fixture'};cov={'counts':{'VERIFIED':1},'uncovered_rule_ids':['RULE']}
class ReadView:
 def read(self,path):return json.dumps(q).encode()
m={'admission_id':'SAFE','coverage_path':kpath,'code_sha256':a.code_bindings(root)};parent={'source_bindings':{}};ctx=a.AdmissionContext(root,m,ReadView(),{},parent,{},{});ctx._source_head=head;ctx._registry_sha256=a.digest((root/a.REGISTRY).read_bytes());ctx._scope_paths=frozenset(a.current_inventory(root,parent));ctx._current_seals={p:a.seal((root/p).read_bytes())for p in ctx._scope_paths};ctx._native_ok=True;ctx._expected_guide=copy.deepcopy(g);ctx._expected_coverage={'current_native_coverage':copy.deepcopy(cov),'synthetic_only':True}
a._TOKENS.add(ctx)
try:
 answer=a.coverage_snapshot(cov,q,g,context=ctx);assert answer==ctx._expected_coverage;answer['synthetic_only']=False;assert ctx._expected_coverage['synthetic_only']is True;checks.append({'check':'H3_EXACT_NATIVE_VALUES_AND_DEEPCOPY','accepted':True})
 bad=copy.deepcopy(cov);bad['caller_supplied_PASS']=True;reject('H3_EQUAL_COUNTS_ARBITRARY_COVERAGE',lambda:a.coverage_snapshot(bad,q,g,context=ctx))
 badq=copy.deepcopy(q);badq['questions'][0]['stem']='altered';reject('H3_EQUAL_COUNT_ALTERED_QUESTION',lambda:a.coverage_snapshot(cov,badq,g,context=ctx))
 badg=copy.deepcopy(g);badg['marker']='altered';reject('H3_EQUAL_COUNT_ALTERED_GUIDE',lambda:a.coverage_snapshot(cov,q,badg,context=ctx))
 put(kpath,json.dumps(ctx._expected_coverage).encode());assert a.require_context(ctx)is ctx;checks.append({'check':'EXACT_CALCULATED_UNTRACKED_K_EXCEPTION','accepted':True})
 put(kpath,b'{"caller_supplied_PASS":true}');reject('K_TAMPERED_VALUE',lambda:a.require_context(ctx))
finally:a._TOKENS.discard(ctx)
(OUT/'H1-H3-current-consumer-probes.json').write_text(json.dumps({'scope':'SYNTHETIC_POST_NATIVE_CONSUMER_FIXTURES_NOT_REGISTRY_AUTHORIZATION_OR_NATIVE_SUCCESS','checks':checks,'production_registry_empty':not a.registry.APPROVED_ADMISSIONS,'actual_native1781_generation_or_admission_runs':0},indent=2)+'\n');print(json.dumps({'fixed_H1_H2_H3_predicates_confirmed':True,'checks':len(checks),'production_admission_credit':0}))
