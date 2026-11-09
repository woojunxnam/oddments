"""Current-hash tiny probes. Synthetic token models post-validation state only."""
from pathlib import Path
import json,subprocess,tempfile
import canonical_admission as a
from verify_representative_protected import EXACT_FILES,PREFIXES
OUT=Path(__file__).resolve().parent;root=Path(tempfile.mkdtemp(prefix='postmint-',dir=OUT))
def put(p,raw=b'{}\n'):
 path=root/p;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
def git(*args):return subprocess.check_output(['git',*args],cwd=root)
for prefix in PREFIXES:(root/prefix).mkdir(parents=True,exist_ok=True)
for p in set(EXACT_FILES)|{a.NOTE,a.HOLDS,a.PREVIEW,a.PAYLOAD,a.BASELINE}|a.DERIVED:put(p)
put('data/questions/original.json');put(a.REGISTRY,b'# synthetic committed trust-root fixture\n');put('site/app.js',b'// original\n')
git('init','--quiet');git('config','user.name','Independent Synthetic Reviewer');git('config','user.email','synthetic@example.invalid');git('add','.');git('commit','--quiet','-m','Synthetic hardened post-mint fixture')
parent={'source_bindings':{}};m={'admission_id':'SAFE_31','coverage_path':'reports/canonical-successor/SAFE_31-coverage.json','code_sha256':a.code_bindings(root)};c=a.AdmissionContext(root,m,None,{},parent,{},{});c._scope_paths=frozenset(a.current_inventory(root,parent));c._current_seals={p:a.seal((root/p).read_bytes())for p in c._scope_paths};c._source_head=git('rev-parse','HEAD').decode().strip();c._registry_sha256=a.digest((root/a.REGISTRY).read_bytes());c._native_ok=True;c._expected_coverage={'synthetic':'actual computed output fixture'}
a._TOKENS.add(c);checks=[]
def reject(label,fn):
 try:fn();raise AssertionError('Accepted '+label)
 except a.BoundaryViolation as e:checks.append({'check':label,'rejected':True,'error':str(e)})
try:
 assert a.require_context(c)is c
 put('data/questions/unlisted.json');reject('R2_NEW_UNLISTED_PROTECTED_FILE',lambda:a.require_context(c));(root/'data/questions/unlisted.json').unlink()
 put('site/app.js',b'// dirty tracked UI\n');reject('DIRTY_TRACKED_UI',lambda:a.require_context(c));put('site/app.js',b'// original\n')
 k=a.coverage_destination(root,m['admission_id'],m['coverage_path']);k.parent.mkdir(parents=True,exist_ok=True);k.write_text(json.dumps(c._expected_coverage));assert a.require_context(c)is c;checks.append({'check':'EXACT_COMPUTED_K_ACCEPTED','accepted':True})
 k.write_text('{"synthetic":"caller PASS"}');reject('FORGED_K_NOT_ACTUAL_COMPUTED_OUTPUT',lambda:a.require_context(c));k.unlink()
 # New source outside the enumerated protected/runtime maps remains untracked.
 put('site/verified-law/unlisted.js',b'// unlisted publishable UI fixture\n');untracked_accepted=a.require_context(c)is c
 (OUT/'postmint-untracked-ui-probe.json').write_text(json.dumps({'scope':'SYNTHETIC_ALREADY_VALIDATED_TOKEN_CONSUMER_ONLY_NOT_REAL_ENROLLMENT','new_untracked_publishable_path':'site/verified-law/unlisted.js','require_context_accepts':untracked_accepted,'tracked_git_diff_empty':git('diff','--name-only','HEAD')==b'','actual_Git_status':git('status','--porcelain').decode(),'production_registry_entries':len(a.registry.APPROVED_ADMISSIONS),'no_publication_or_admission_performed':True},indent=2)+'\n')
finally:a._TOKENS.discard(c)
for value in [True,False,1.0,'1',None,0,2]:reject('R4_VERSION_'+repr(value),lambda v=value:a.protocol_version(v))
a.protocol_version(1)
for uid in ['../../../outside-reviewed-root','bad/id','bad\\id','bad id','',None]:reject('R3_ID_'+repr(uid),lambda v=uid:a.coverage_destination(root,v,'reports/canonical-successor/'+str(v)+'-coverage.json'))
symlink_root=Path(tempfile.mkdtemp(prefix='coverage-symlink-',dir=OUT));(symlink_root/'reports').mkdir();(symlink_root/'reports/canonical-successor').symlink_to(root,target_is_directory=True);reject('R3_SYMLINK_NAMESPACE',lambda:a.coverage_destination(symlink_root,'SAFE','reports/canonical-successor/SAFE-coverage.json'))
(OUT/'resolved-boundaries-and-K-probes.json').write_text(json.dumps({'scope':'TINY_SYNTHETIC_BOUNDARY_PROBES_NOT_NATIVE_SUCCESS','checks':checks,'original_R2_R3_R4_predicates_now_reject':True,'actual_K_value_checked_on_consumption':True,'production_registry_empty':not a.registry.APPROVED_ADMISSIONS,'full_native_or1781_runs':0},indent=2)+'\n')
print(json.dumps({'R2_R3_R4_rejected':True,'K_wrong_value_rejected':True,'untracked_publishable_UI_still_accepted':untracked_accepted}))
