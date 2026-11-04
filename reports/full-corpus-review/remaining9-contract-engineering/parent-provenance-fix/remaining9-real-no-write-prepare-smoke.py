from pathlib import Path
import json,sys,subprocess,hashlib,datetime
r=Path('/workspace/remaining9-contract');root=Path('/workspace/oddments')
sys.path.insert(0,str(r/'scripts'))
import remaining9_procedural_metadata as route
from prepare_remaining9_procedural import prepare
actual_path=Path('/workspace/scratch/remaining9-actual-fresh-reviewer.json')
raw_reviewer=actual_path.read_bytes();reviewer=json.loads(raw_reviewer)
root_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
own_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip()
paths=sorted({x['report_path']for x in route.PARENTS.values()}|set(route.AUTHOR_BINDINGS)|{
    'practice_expansion/2026-10-23/candidates/questions.json','reports/full-corpus-review/question-ledger.jsonl'})
rows=[]
for path in paths:
    ownraw=(r/path).read_bytes();rootraw=(root/path).read_bytes()
    assert ownraw==subprocess.check_output(['git','show','HEAD:'+path],cwd=r)
    assert rootraw==subprocess.check_output(['git','show','HEAD:'+path],cwd=root)
    assert ownraw==rootraw
    rows.append({'path':path,'raw_sha256':hashlib.sha256(ownraw).hexdigest(),
        'actual_root_head_and_own_head_and_both_disk_bytes_equal':True})
assert not(r/route.STATE).exists()and not(root/route.STATE).exists()
before=subprocess.check_output(['git','status','--porcelain'],cwd=root)
proposal=prepare(r,reviewer)
assert len(proposal['jobs'])==1 and proposal['jobs'][0]['status']=='QUEUED'
assert proposal['jobs'][0]['attempt']==0 and proposal[route.SCOPE_KEY]['fresh_reviewer']==reviewer
assert not(r/route.STATE).exists()and not(root/route.STATE).exists()
assert before==subprocess.check_output(['git','status','--porcelain'],cwd=root)
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()==root_head
proof={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'purpose':'ACTUAL_FRESH_REVIEWER_NO_WRITE_PREPARE_SMOKE_USING_EXACT_ACTUAL_ROOT_COMMITTED_INPUTS',
    'actual_root_head':root_head,'own_smoke_head':own_head,
    'working_implementation_sha256':hashlib.sha256((r/'scripts/remaining9_procedural_metadata.py').read_bytes()).hexdigest(),
    'reviewer_metadata_path':str(actual_path),'reviewer_metadata_sha256':hashlib.sha256(raw_reviewer).hexdigest(),
    'actual_actor_provenance':reviewer['actor_provenance'],'actual_auditor_instance':reviewer['auditor_instance'],
    'source_inputs_verified':rows,'prepare_result':'PASS','proposal_jobs':1,
    'proposal_attempt':0,'proposal_status':'QUEUED','actual_root_mutation':False,
    'own_or_root_native_state_created':False,'actual_native_registration_or_claim':False,
    'proposal_persisted':False,'canonical_release_credit':0}
Path('/workspace/scratch/remaining9-full-parent-provenance-real-no-write-smoke.json').write_text(
    json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in proof.items()if k!='source_inputs_verified'},ensure_ascii=False))
