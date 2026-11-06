"""Actual clean-workspace helper versus mutable Git index flags; no enrollment."""
from pathlib import Path
import json,subprocess,tempfile
import canonical_admission as a
OUT=Path(__file__).resolve().parent
results=[]
for flag in ['--assume-unchanged','--skip-worktree']:
 root=Path(tempfile.mkdtemp(prefix='git-index-',dir=OUT))
 def git(*args):return subprocess.check_output(['git',*args],cwd=root)
 git('init','--quiet');git('config','user.name','Independent Synthetic Reviewer');git('config','user.email','synthetic@example.invalid');(root/'site').mkdir();(root/'site/app.js').write_bytes(b'// exact committed safe source\n');git('add','.');git('commit','--quiet','-m','Synthetic committed publishable source');head=git('rev-parse','HEAD').decode().strip();coverage='reports/canonical-successor/SAFE-coverage.json';a.require_clean_delivery_workspace(root,head,coverage)
 git('update-index',flag,'site/app.js');(root/'site/app.js').write_bytes(b'// unreviewed disk mutation hidden by index flag\n')
 assert git('diff','--name-only','HEAD')==b''
 a.require_clean_delivery_workspace(root,head,coverage)
 committed=a.read_committed_preimages(root,head,['site/app.js'])['site/app.js'];disk=(root/'site/app.js').read_bytes();assert disk!=committed
 row={'index_flag':flag,'tracked_git_diff_empty':True,'workspace_guard_accepts_changed_UI_bytes':True,'actual_HEAD_blob_differs_from_disk':True,'source_path':'site/app.js','fixture_root':str(root),'production_enrollment':False}
 if flag=='--skip-worktree':
  external=Path(tempfile.mkdtemp(prefix='outside-publishable-',dir=OUT))/'external.js';external.write_bytes(b'// synthetic external target\n');(root/'site/app.js').unlink();(root/'site/app.js').symlink_to(external)
  assert git('diff','--name-only','HEAD')==b'';a.require_clean_delivery_workspace(root,head,coverage)
  row['workspace_guard_accepts_tracked_UI_replaced_with_symlink']=True
  row['symlink_target_is_outside_fixture_root']=True
 results.append(row)
(OUT/'git-index-hidden-UI-mutation-probe.json').write_text(json.dumps({'scope':'REAL_GIT_INDEX_AND_ACTUAL_WORKSPACE_HELPER_ONLY_NOT_NATIVE_REGISTRATION_OR_PUBLICATION','results':results,'actual_native_or_admission_credit':0,'recommendation':'Compare every published regular disk preimage directly with immutable HEAD blob bytes/mode and reject symlinks in every component; do not rely on Git index dirty reporting for source integrity.'},indent=2)+'\n')
print(json.dumps({'assume_unchanged_accepts_UI_mutation':True,'skip_worktree_accepts_UI_mutation_and_symlink':True,'actual_enrollment_or_publication':False}))
