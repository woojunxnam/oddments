#!/usr/bin/env python3
"""Test additive staging and refusal behavior against disposable local repositories."""
from pathlib import Path
import importlib.util,json,hashlib,tempfile,shutil
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('apply_draft',R/'apply_to_repo.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
# Use the exact referenced note snapshot supplied by the local repository argument.
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--guide',required=True,type=Path);a=ap.parse_args()
checks=[]
def snapshot(root):return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
def ok(label):checks.append(label);print('PASS',label)
with tempfile.TemporaryDirectory() as tmp:
 root=Path(tmp)/'oddments';root.mkdir();(root/'notes').mkdir();shutil.copyfile(a.guide,root/'notes/guide.json')
 for p in ['data/original.json','site/index.html','audits/existing.json','local_private/do-not-touch.txt']:
  out=root/p;out.parent.mkdir(exist_ok=True);out.write_text('synthetic original: '+p)
 before=snapshot(root);r=m.apply(root,False);assert snapshot(root)==before and r['action']=='DRY_RUN_NO_WRITES';ok('dry run performs no writes')
 r=m.apply(root,True);after=snapshot(root);assert all(after[k]==v for k,v in before.items());assert all(k in before or k.startswith('practice_expansion/2026-10-23/') for k in after);ok('apply adds only the designated subtree and preserves every original byte')
 assert r['questions_released']==0 and r['commit_created'] is False and r['pushed'] is False;ok('apply does not release, commit or push')
 try:m.apply(root,True);raise AssertionError('overwrite allowed')
 except ValueError:ok('existing destination overwrite refused')
 (root/'notes/guide.json').write_text('{}');changed=snapshot(root)
 try:m.apply(root,False);raise AssertionError('changed guide accepted')
 except ValueError:assert snapshot(root)==changed;ok('changed integrated notes refused without writes')
 root2=Path(tmp)/'symlink-target';root2.mkdir();(root2/'notes').mkdir();shutil.copyfile(a.guide,root2/'notes/guide.json');(root2/'practice_expansion').symlink_to(root,target_is_directory=True)
 try:m.apply(root2,True);raise AssertionError('symlink target accepted')
 except ValueError:ok('symlink destination refused')
(R/'reports/apply-test.json').write_text(json.dumps({'passed':checks,'count':len(checks),'environment':'Disposable local repositories with exact guide snapshot and synthetic sentinel originals','remote_repository_changed':False},indent=2)+'\n')
