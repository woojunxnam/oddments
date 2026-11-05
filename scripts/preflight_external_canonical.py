"""Read-only native QA for a private external proposal; never admission/approval."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from canonical_native_view import NativeView,native_validation
from canonical_successor import ALLOWED_ADDITION,FAMILY,read_current_preimages,require,strict_json


def inspect(root,proposal,base_commit,*,family_file=None):
    root=Path(root).resolve();proposal=Path(proposal).resolve()
    replacements={};input_hashes={}
    for kind in ['questions','audits','rules','drugs']:
        directory=proposal/kind if kind in {'questions','audits'} else proposal/'proposed-registry'/kind
        if not directory.exists():continue
        for path in sorted(directory.glob('*.json')):
            require(not path.is_symlink(),'Private proposal source is a symlink')
            raw=path.read_bytes();record=strict_json(raw)
            rel='data/'+kind+'/'+path.name.lower()
            require(bool(ALLOWED_ADDITION.fullmatch(rel)),'Private proposal path outside native registry')
            require(not (root/rel).exists(),'Private proposal may not overwrite a current registry file')
            require(rel not in replacements,'Duplicate proposed file')
            replacements[rel]=raw;input_hashes[rel]=hashlib.sha256(raw).hexdigest()
    if family_file is not None:
        raw=Path(family_file).read_bytes();strict_json(raw);replacements[FAMILY]=raw;input_hashes[FAMILY]=hashlib.sha256(raw).hexdigest()
    view=NativeView(root,base_commit,replacements)
    report,questions=native_validation(view)
    added=[q for q in questions.values() if q['question_id'].lower()+'.json' in {Path(p).name for p in replacements if p.startswith('data/questions/')}]
    return {'status':'PRIVATE_READ_ONLY_NATIVE_PREFLIGHT_NOT_ADMITTED',
        'base_commit':base_commit,'input_file_sha256':input_hashes,'native_errors':report.errors,'native_warnings':report.warnings,
        'native_validation_ok':report.ok,'proposed_question_count':len(added),
        'proposed_current_hash_audit_references':sum(len(q.get('audits',[]))for q in added),
        'proposed_final_KEEP':sum(q.get('final_adjudication',{}).get('decision')=='KEEP'for q in added if q.get('final_adjudication')),
        'activation_allowed':False,'admission_audit_release_credit':0,
        'limit':'Native preflight is not an official-source review. Missing family approvals, native audits and adjudications remain blockers. Raw errors stay private.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--proposal',type=Path,required=True)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);parser.add_argument('--base-commit')
    parser.add_argument('--family-file',type=Path);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();root=args.root.resolve();output=args.output.resolve()
    require(root not in output.parents,'Private preflight output must remain outside the public repository')
    commit=args.base_commit or subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
    result=inspect(root,args.proposal,commit,family_file=args.family_file)
    require(not output.exists(),'Refusing to overwrite an existing private preflight')
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({key:result[key]for key in ['status','base_commit','native_validation_ok','proposed_question_count','admission_audit_release_credit']}))


if __name__=='__main__':main()
