"""Explicit registered successor gate. Missing enrollment executes original gates."""
import argparse
import json
from pathlib import Path

from canonical_admission import ROOT,registered_context,verify_protected,validate_withdrawal,artifact_payloads
from canonical_successor import require


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--operation',choices=['status','protected','withdrawal','artifacts'],default='status')
    parser.add_argument('--write',action='store_true');args=parser.parse_args()
    require(not args.write or args.operation=='artifacts','Write is only for exact producer artifacts')
    context=registered_context()
    if args.operation=='status':
        print(json.dumps({'status':'REGISTERED_NATIVE_CONTEXT'if context else'NO_ENROLLED_ADMISSION',
            'activation_allowed':context is not None,'new_eligible_count':len(context.new_questions)if context else 0,
            'actual_legacy_replay_executed':False}));return
    if args.operation=='protected':
        manifest=json.loads((ROOT/'reports/representative-rewrite/protected-baseline.json').read_bytes())
        print(json.dumps(verify_protected(manifest,context=context),sort_keys=True));return
    if args.operation=='withdrawal':
        print(json.dumps({'preserved_preimage_paths':sorted(validate_withdrawal(context=context))}));return
    if context is None:
        from generate_artifacts import artifact_payloads as old
        outputs=old()
    else:outputs=artifact_payloads(context)
    from qa_common import write_json
    for path,value in outputs.items():
        if args.write:write_json(path,value)
        else:require(path.exists()and json.loads(path.read_bytes())==value,'Artifact drift: '+str(path))
    print(json.dumps({'artifacts':len(outputs),'mode':'write'if args.write else'check'}))


if __name__=='__main__':main()
