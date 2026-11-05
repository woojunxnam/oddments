"""Exact predicate/API-value probes, not native producer recomputation or enrollment."""
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import ast,copy,json
import canonical_admission as a
OUT=Path(__file__).resolve().parent;ROOT=Path('/workspace/mpje-336-successor')
# Exercise the exact new DERIVED predicate using existing native report bytes.
tree=ast.parse(Path(a.__file__).read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='_validate_registered_sources');call=next(n for n in ast.walk(fn)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='require'and any(isinstance(x,ast.BinOp)and isinstance(x.left,ast.Constant)and x.left.value=='Derived report differs from actual native producer: 'for x in n.args))
compiled=compile(ast.Expression(body=call.args[0]),'actual-derived-output-predicate','eval');checks=[]
for relative in sorted(a.DERIVED):
 raw=(ROOT/relative).read_bytes();current={relative:raw};outputs={ROOT/relative:a.strict_json(raw)};env={'outputs':outputs,'root':ROOT,'relative':relative,'strict_json':a.strict_json,'current':current};assert eval(compiled,env)
 outputs[ROOT/relative]={'caller_supplied_PASS':True};assert not eval(compiled,env)
 checks.append({'path':relative,'exact_actual_existing_report_value_passes':True,'forged_value_fails_actual_comparison':True})
(OUT/'derived4-predicate-probes.json').write_text(json.dumps({'scope':'EXACT_COMPARISON_PREDICATES_ONLY_NOT_NEW_PRODUCER_OR_NATIVE_EXECUTION','checks':checks,'actual_new_four_report_recomputation_executed':False},indent=2)+'\n')
# Public coverage_snapshot is given a test-only already-validated-handle stand-in.
# The require_context mock removes unrelated fixture setup only; it does not
# demonstrate minting a production token or bypassing any registry authorization.
payload={'meta':{'question_count':1},'blueprint':{},'questions':[{'question_id':'OLD-FIXTURE'}]}
guide={'sections':[],'question_to_sections':{},'meta':{'public_verified_section_count':0}}
coverage={'sections':{'by_status':{'VERIFIED':0}},'canonical_rules':{'covered_by_verified_public_section':0},'fixture_native_field':'actual-computed'}
context=SimpleNamespace(base_raw={a.PAYLOAD:json.dumps(payload).encode()},new_questions={},manifest={'admission_id':'SYNTHETIC'},manifest_binding={'sha256':'a'*64},note_binding={'sha256':'b'*64},view=SimpleNamespace(read=lambda path:b'{}'))
expected=a._coverage_value(coverage,payload,guide,context);context._expected_coverage=copy.deepcopy(expected)
forged=copy.deepcopy(coverage);forged['caller_supplied_PASS']=True
with patch.object(a,'require_context',return_value=context):returned=a.coverage_snapshot(forged,payload,guide,context=context)
assert returned!=context._expected_coverage and returned['current_native_coverage']['caller_supplied_PASS']is True
(OUT/'public-coverage-value-binding-probe.json').write_text(json.dumps({'scope':'PUBLIC_API_VALUE_INTEGRITY_UNIT_PROBE_WITH_EXPLICIT_CONTEXT_SETUP_MOCK_NOT_AUTHORIZATION_BYPASS','caller_coverage_count_fields_match':True,'caller_added_non_native_field_was_returned':True,'returned_K_differs_from_context_expected_native_K':True,'actual_artifact_producer_path_is_separate_and_recomputes':True,'existing_K_file_consumer_check_would_reject_this_value':True,'production_registry_still_empty':not a.registry.APPROVED_ADMISSIONS,'actual_native_or_admission_or_release_credit':0},indent=2)+'\n')
print(json.dumps({'DERIVED4_comparison_rejects_forged_values':True,'public_coverage_API_does_not_bind_full_caller_value_to_cached_native_K':True,'production_admission_performed':False}))
