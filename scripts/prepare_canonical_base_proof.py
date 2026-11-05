"""Prepare an external, unapproved base-proof draft from actual retained evidence.

Never updates a baseline, enrollment or reviewed registry. Reuses a past actual
protected-guard result only when its immutable selected input tree is identical.
"""
import argparse
import json
from pathlib import Path

from canonical_admission import (ROOT,NOTE,HOLDS,BASELINE,OLD_GUARDS,git,git_tree,base_bundle,json_hash,digest)
from canonical_successor import read_committed_preimages,require,strict_json


def prepare(root,base_commit,receipt_path):
    root=Path(root).resolve();tree,parent_raw,parent,paths=base_bundle(root,base_commit)
    raw=read_committed_preimages(root,base_commit,[receipt_path])[receipt_path];receipt=strict_json(raw)
    actual=[r for r in receipt.get('actual_tests',[])if 'verify_representative_protected.py'in r.get('command','')]
    require(len(actual)==1 and actual[0].get('exit_code')==0 and actual[0].get('verified_files')==1781
        and actual[0].get('verified_bytes')==60969461,'Retained receipt has no actual original1781 PASS')
    tested=receipt['source_base_commit'];old_tree,_,old_parent,old_paths=base_bundle(root,tested)
    # Overlay quarantine is a separate monotone delivery guard, not an input that
    # the historical original1781 validator claims to have legally adjudicated.
    guard_paths=paths-{HOLDS};old_guard_paths=old_paths-{HOLDS}
    require(guard_paths==old_guard_paths and all(tree[p]==old_tree[p]for p in guard_paths),
        'Past actual guard inputs differ from proposed immutable base; new real replay required')
    code=read_committed_preimages(root,base_commit,sorted(OLD_GUARDS))
    old_code=read_committed_preimages(root,tested,sorted(OLD_GUARDS))
    require(code==old_code,'Past actual old guard implementation changed; new replay required')
    # The original withdrawal API runs on the real current439 root, never a seal
    # projection. Return bytes are then located by object identity in base Git.
    import canonical_q0012_withdrawal as withdrawal
    originals=withdrawal.validate(root)
    def retained(raw):
        import hashlib
        oid=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        candidates=[p for p,v in tree.items()if v['oid']==oid and v['mode']in {'100644','100755'}]
        require(bool(candidates),'Actual original preimage has no retained base blob')
        path=sorted(candidates,key=lambda p:(not p.startswith('revisions/baselines/'),p))[0]
        return {'path':path,'sha256':digest(raw)}
    baseline=strict_json(read_committed_preimages(root,base_commit,[BASELINE])[BASELINE])
    md_row=next(r for r in baseline['files']if r['path']=='site/notes/complete-notes.md')
    names=[p for p,v in tree.items()if v['oid']==md_row['git_blob_sha1']]
    require(bool(names),'Original1781 Markdown preimage not retained')
    md_path=sorted(names,key=lambda p:(not p.startswith('revisions/baselines/'),p))[0]
    proof={'base_commit':base_commit,'base_tree':git(root,'rev-parse',base_commit+'^{tree}').decode().strip(),
        'input_inventory_sha256':json_hash({p:tree[p]for p in sorted(guard_paths)}),
        'guard_code_sha256':{p:digest(value)for p,value in code.items()},
        'receipt':{'path':receipt_path,'sha256':digest(raw)},
        'protected_result':{'files':1781,'bytes':60969461,'baseline_commit':'b5bd6b02c7ea8a5c6731871fa6e330ac6795fd36'},
        'withdrawal_preimages':{p:retained(value)for p,value in originals.items()},
        'original_markdown':{'path':md_path,'sha256':md_row['sha256']}}
    return {'status':'UNAPPROVED_REVIEW_INPUT_NOT_ENROLLED','candidate_base_guard_proof':proof,
        'past_actual_guard_commit':tested,'actual_current_withdrawal_API_executed':True,
        'past_guard_input_tree_exact_match':True,'new_actual1781_replay_executed':False,
        'source_only_or_synthetic_PASS_used_as_replay':False,'approval_admission_release_credit':0}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--base-commit',required=True)
    parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--receipt',default='reports/coverage336/successor-infrastructure-receipt.json')
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    target=args.output.resolve();require(args.root.resolve()not in target.parents,'Review draft must remain outside public source')
    require(not target.exists(),'Refusing to overwrite a prior base-proof draft')
    result=prepare(args.root,args.base_commit,args.receipt)
    target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'base_commit':args.base_commit,'credit':0}))


if __name__=='__main__':main()
