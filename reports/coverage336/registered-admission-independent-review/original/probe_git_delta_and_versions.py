"""Independent scope/predicate probes. No full registration/native replay."""
from pathlib import Path
import ast,json,subprocess,tempfile
import canonical_admission as a
from verify_representative_protected import in_scope
OUT=Path(__file__).resolve().parent;root=Path(tempfile.mkdtemp(prefix='synthetic-git-delta-',dir=OUT))
def git(*args):return subprocess.check_output(['git',*args],cwd=root)
def put(p,raw):
 path=root/p;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
git('init','--quiet');git('config','user.name','Independent Synthetic Reviewer');git('config','user.email','synthetic@example.invalid')
put('data/questions/ma-q-9000.json',b'{"synthetic":"sealed declared data"}\n');put('scripts/runtime.py',b'# unchanged runtime fixture\n');put('site/app.js',b'// immutable base UI fixture\n');git('add','.');git('commit','--quiet','-m','Synthetic base');base=git('rev-parse','HEAD').decode().strip()
put('site/app.js',b'// undeclared UI mutation before content commit\n');git('add','site/app.js');git('commit','--quiet','-m','Synthetic content with undeclared UI delta');content=git('rev-parse','HEAD').decode().strip()
put('site/app.js',b'// second undeclared UI mutation after content commit\n');git('add','site/app.js');git('commit','--quiet','-m','Synthetic later HEAD UI delta');head=git('rev-parse','HEAD').decode().strip()
base_tree=a.git_tree(root,base);content_tree=a.git_tree(root,content);head_tree=a.git_tree(root,head)
data=['data/questions/ma-q-9000.json'];same_declared=(a.read_committed_preimages(root,base,data)==a.read_committed_preimages(root,content,data)==a.read_committed_preimages(root,head,data))
result={'scope':'REAL_SYNTHETIC_GIT_TREE_SCOPE_PROBE_NOT_REGISTERED_END_TO_END',
 'base':base,'content_commit':content,'HEAD':head,'actual_base_to_content_git_delta':git('diff','--name-only',base,content).decode().splitlines(),'actual_content_to_HEAD_git_delta':git('diff','--name-only',content,head).decode().splitlines(),
 'tested_path':'site/app.js','path_is_in_original_protected_scope':in_scope('site/app.js'),'path_is_in_admission_expanded_note_scope':'site/app.js'.startswith('site/notes/'),'path_is_in_exact_special_paths':'site/app.js'in{a.NOTE,a.HOLDS,a.PREVIEW,a.PAYLOAD,a.BASELINE},'path_is_in_runtime_python_code_inventory':'site/app.js'in a.code_bindings(root),'declared_data_bytes_unchanged':same_declared,'base_is_ancestor_of_content':subprocess.run(['git','-C',str(root),'merge-base','--is-ancestor',base,content],capture_output=True).returncode==0,'content_is_ancestor_of_HEAD':subprocess.run(['git','-C',str(root),'merge-base','--is-ancestor',content,head],capture_output=True).returncode==0,'observed_contract_gap':'Only selected protected/data/code/evidence bytes and ancestry are compared. No complete base→content or content→HEAD path allowlist is enforced. Later unrelated UI edits are not pinned in the registered manifest yet can retain the same registry/enrollment/data/code bytes.','full_registered_validation_executed':False,'production_registry_entries':len(a.registry.APPROVED_ADMISSIONS),'actual_admission_release_credit':0}
assert same_declared and all(not result[k]for k in ['path_is_in_original_protected_scope','path_is_in_admission_expanded_note_scope','path_is_in_exact_special_paths','path_is_in_runtime_python_code_inventory'])
(OUT/'undeclared-git-delta-scope-probe.json').write_text(json.dumps(result,indent=2)+'\n')
# Read the exact three equality predicates to show the format boundary only.
source=Path(a.__file__).read_text();tree=ast.parse(source);predicates=[]
for node in ast.walk(tree):
 if isinstance(node,ast.Compare) and isinstance(node.left,ast.Subscript)and isinstance(node.left.value,ast.Name)and isinstance(node.left.slice,ast.Constant)and node.left.slice.value=='schema_version':
  env={node.left.value.id:{'schema_version':True}}
  predicates.append({'actual_source_predicate':ast.unparse(node),'schema_version_true_passes':eval(compile(ast.Expression(body=node),'actual-schema-version-predicate','eval'),env)})
assert len(predicates)==3 and all(p['schema_version_true_passes']for p in predicates)
(OUT/'boolean-schema-version-predicates.json').write_text(json.dumps({'scope':'ACTUAL_FORMAT_PREDICATES_ONLY_NOT_AUTHORIZATION_BYPASS','predicates':predicates,'exact_registry_raw_hash_still_required':True,'production_enrollment':False},indent=2)+'\n')
print(json.dumps({'unlisted_UI_path_outside_all_current_scope_maps':True,'both_ancestry_guards_pass':True,'three_boolean_version_predicates_accept_true':True,'actual_production_activation':False}))
