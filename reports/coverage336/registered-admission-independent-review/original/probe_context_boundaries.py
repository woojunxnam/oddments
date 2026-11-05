"""Synthetic post-validation-state probes. Never production enrollment or native PASS."""
from pathlib import Path
import ast,hashlib,json,subprocess,tempfile
import canonical_admission as a
OUT=Path(__file__).resolve().parent
root=Path(tempfile.mkdtemp(prefix='synthetic-token-state-',dir=OUT))
def git(*args):return subprocess.check_output(['git',*args],cwd=root)
def put(relative,raw):
 p=root/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
 return raw
put(a.REGISTRY,b'APPROVED_ADMISSIONS = {}\nAPPROVED_BASE_GUARD_PROOFS = {}\n')
old=put('data/questions/ma-q-9000.json',b'{"synthetic":"original"}\n')
baseline=put(a.BASELINE,b'{}\n')
git('init','--quiet');git('config','user.name','Independent Synthetic Reviewer');git('config','user.email','synthetic@example.invalid');git('add','.');git('commit','--quiet','-m','Synthetic read-only consumer fixture')
commit=git('rev-parse','HEAD').decode().strip()
context=a.AdmissionContext(root,{'code_sha256':a.code_bindings(root)},None,
 {'protected_result':{'files':1781,'bytes':60969461,'baseline_commit':'b5bd6b02c7ea8a5c6731871fa6e330ac6795fd36'}},None,{a.BASELINE:baseline},{})
context._native_ok=True;context._source_head=commit
context._registry_sha256=a.digest((root/a.REGISTRY).read_bytes())
context._current_seals={'data/questions/ma-q-9000.json':a.seal(old),a.BASELINE:a.seal(baseline)}
# Explicit test-only setup models a handle already minted by validation.
# It is NOT a way to obtain one from the empty production registry.
a._TOKENS.add(context)
try:
 assert a.require_context(context)is context
 unexpected=put('data/questions/ma-q-9999.json',b'{"synthetic":"unlisted post-validation addition"}\n')
 accepted=a.require_context(context)is context
 returned=a.verify_protected({},root,context=context)
 result={'scope':'SYNTHETIC_POST_VALIDATION_CONSUMER_RECHECK_ONLY_NOT_PRODUCTION_TOKEN_MINT',
  'test_only_internal_token_setup':True,'actual_production_registry_entries':len(a.registry.APPROVED_ADMISSIONS),
  'unlisted_protected_file_added_after_fixture_sealing':'data/questions/ma-q-9999.json',
  'existing_sealed_bytes_unchanged':True,'source_HEAD_unchanged':git('rev-parse','HEAD').decode().strip()==commit,
  'require_context_accepted_after_unlisted_addition':accepted,'verify_protected_adapter_returned':returned,
  'actual_native_validation_or_1781_replay_run':False,'admission_approval_release_credit':0}
 (OUT/'unlisted-file-stale-context-probe.json').write_text(json.dumps(result,indent=2)+'\n')
finally:a._TOKENS.discard(context)
# Evaluate the actual coverage_path require predicate, without executing the
# validator or producing/writing any artifact.
source=Path(a.__file__).read_text();tree=ast.parse(source);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='_validate_registered_sources')
call=next(n for n in ast.walk(fn)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='require'and any(isinstance(arg,ast.Constant)and arg.value=='Successor coverage must use a separate exact path'for arg in n.args))
malicious_id='../../../outside-reviewed-root';manifest={'admission_id':malicious_id,'coverage_path':'reports/canonical-successor/'+malicious_id+'-coverage.json'}
predicate=eval(compile(ast.Expression(body=call.args[0]),'actual-coverage-path-predicate','eval'),{'m':manifest});derived=(root/manifest['coverage_path']).resolve()
path_result={'scope':'ACTUAL_COVERAGE_PATH_PREDICATE_UNIT_PROBE_NO_ARTIFACT_WRITE',
 'manifest_admission_id':malicious_id,'coverage_path':manifest['coverage_path'],
 'actual_validator_path_predicate_accepts':predicate,'derived_absolute_output':str(derived),
 'derived_path_escapes_context_root':root not in derived.parents,
 'requires_reviewed_registry_entry_before_this_predicate_in_real_flow':True,
 'actual_production_registry_entries':len(a.registry.APPROVED_ADMISSIONS),
 'write_or_admission_performed':False}
assert predicate and path_result['derived_path_escapes_context_root']
(OUT/'coverage-path-namespace-probe.json').write_text(json.dumps(path_result,indent=2)+'\n')
print(json.dumps({'unlisted_addition_accepted':accepted,'adapter_returned':returned,'coverage_escape_predicate_accepted':predicate,'production_registry_still_empty':not a.registry.APPROVED_ADMISSIONS}))
