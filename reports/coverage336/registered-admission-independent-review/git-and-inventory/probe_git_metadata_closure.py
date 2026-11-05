"""Whole tracked-delta hardening and metadata-commit closure unit probes."""
from pathlib import Path
import json,subprocess,tempfile
import canonical_admission as a
OUT=Path(__file__).resolve().parent;root=Path(tempfile.mkdtemp(prefix='git-metadata-',dir=OUT))
def git(*args):return subprocess.check_output(['git',*args],cwd=root)
def put(p,text):
 path=root/p;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
git('init','--quiet');git('config','user.name','Independent Synthetic Reviewer');git('config','user.email','synthetic@example.invalid');put('data/item.json','{}');put('site/app.js','original');put(a.REGISTRY,'# initial fixture');git('add','.');git('commit','--quiet','-m','Synthetic trusted base');base=git('rev-parse','HEAD').decode().strip();put('data/item.json','{"new":true}');git('add','.');git('commit','--quiet','-m','Synthetic exact content');content=git('rev-parse','HEAD').decode().strip();put(a.REGISTRY,'# reviewed constant registry fixture');git('add',a.REGISTRY);git('commit','--quiet','-m','Synthetic registry only');head=git('rev-parse','HEAD').decode().strip()
metadata=[a.ACTIVATION_PATH,'revisions/canonical/SAFE_31-manifest.json','revisions/canonical/SAFE_31-notes.json'];allowed_post=set(metadata)|{a.REGISTRY,'reports/canonical-successor/SAFE_31-coverage.json'}
# These exact JSON bytes are present but untracked; only registry is committed.
for path in metadata:put(path,'{"synthetic":"exact pinned metadata fixture"}')
a.verify_git_delta(root,base,content,head,{'data/item.json'},allowed_post)
current=a.read_current_preimages(root,metadata);committed={}
for path in metadata:
 result=subprocess.run(['git','-C',str(root),'cat-file','-e',head+':'+path],capture_output=True);committed[path]=result.returncode==0
assert not any(committed.values()) and git('diff','--name-only','HEAD')==b''
(OUT/'uncommitted-metadata-closure-probe.json').write_text(json.dumps({'scope':'ACTUAL_DELTA_AND_SOURCE_READER_HELPERS_ONLY_NOT_FULL_REGISTRATION','actual_base_to_content':git('diff','--name-only',base,content).decode().splitlines(),'actual_content_to_HEAD':git('diff','--name-only',content,head).decode().splitlines(),'allowed_metadata_paths':metadata,'metadata_current_files_exist_and_can_be_exactly_sealed':set(current)==set(metadata),'metadata_present_in_HEAD':committed,'whole_delta_guard_accepts_registry_only_HEAD':True,'dirty_tracked_guard_accepts':True,'limit':'The production registry is empty. This probe does not mint a registered token. Static full-code reading finds no later HEAD-blob requirement for M/N/E.','production_registry_entries':len(a.registry.APPROVED_ADMISSIONS),'actual_admission_or_native_validation':False},indent=2)+'\n')
# The original undeclared tracked-UI case is now rejected on each boundary.
put('site/app.js','unlisted post-content');git('add','site/app.js');git('commit','--quiet','-m','Synthetic unrelated UI')
checks=[]
for label,bc,cc,hh in [('POST',base,content,'HEAD'),('CONTENT',base,'HEAD','HEAD')]:
 try:a.verify_git_delta(root,bc,cc,hh,{'data/item.json'},allowed_post);raise AssertionError('UI delta accepted')
 except a.BoundaryViolation as e:checks.append({'check':label,'rejected':True,'error':str(e)})
(OUT/'original-R1-tracked-UI-now-rejected.json').write_text(json.dumps({'scope':'SYNTHETIC_TRACKED_GIT_DELTA_REGRESSION_ONLY','checks':checks,'full_registered_E2E':False},indent=2)+'\n')
print(json.dumps({'original_R1_tracked_UI_rejected':True,'missing_committed_MNE_is_not_rejected_by_delta_or_current_reader_guards':True,'production_enrollment_performed':False}))
