"""Independent current J1 replay, real synthetic Git/helper, no admission."""
from pathlib import Path
import json,subprocess,tempfile
import canonical_admission as a
OUT=Path(__file__).resolve().parent;checks=[]
for flag in ['--assume-unchanged','--skip-worktree']:
 for replacement in ['bytes','external-symlink']:
  root=Path(tempfile.mkdtemp(prefix='HEAD-preimage-',dir=OUT))
  def git(*args):return subprocess.check_output(['git',*args],cwd=root)
  git('init','--quiet');git('config','user.name','Independent Synthetic Reviewer');git('config','user.email','synthetic@example.invalid');(root/'site').mkdir();path=root/'site/app.js';path.write_bytes(b'// original committed source\n');git('add','.');git('commit','--quiet','-m','Synthetic current HEAD preimage')
  head=git('rev-parse','HEAD').decode().strip();coverage='reports/canonical-successor/SAFE-coverage.json';a.require_clean_delivery_workspace(root,head,coverage);git('update-index',flag,'site/app.js');a.require_clean_delivery_workspace(root,head,coverage)
  if replacement=='bytes':path.write_bytes(b'// hidden changed body\n')
  else:
   target=Path(tempfile.mkdtemp(prefix='outside-',dir=OUT))/'target.js';target.write_bytes(b'// synthetic outside target\n');path.unlink();path.symlink_to(target)
  assert git('diff','--name-only','HEAD')==b''
  try:a.require_clean_delivery_workspace(root,head,coverage);raise AssertionError('J1 still accepted')
  except a.BoundaryViolation as e:checks.append({'index_flag':flag,'replacement':replacement,'git_diff_still_empty':True,'actual_current_workspace_helper_rejects':True,'error':str(e),'unchanged_bytes_with_same_index_flag_were_accepted':True})
result={'scope':'REAL_SYNTHETIC_GIT_AND_ACTUAL_CURRENT_HELPER_J1_REGRESSION_NOT_NATIVE_REGISTRATION','module_sha256':a.digest(Path(a.__file__).read_bytes()),'checks':checks,'J1_variants_rejected':len(checks),'production_registry_empty':not a.registry.APPROVED_ADMISSIONS,'actual_enrollment_native_or_publication_credit':0}
(OUT/'J1-direct-preimage-probes.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'current_module':result['module_sha256'],'J1_variants_rejected':len(checks),'production_activation':False}))
