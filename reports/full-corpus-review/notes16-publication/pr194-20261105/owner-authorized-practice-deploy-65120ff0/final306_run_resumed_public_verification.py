from pathlib import Path
import json,sys,hashlib,traceback
import final306_owner_exception_public_verifier_v2 as module
PRIOR=Path('/workspace/scratch/final306-pr194-actual-public-verification')
class ResumeExactSuccessfulBuild(module.Verification):
    def rebuild_expected_bytes(self):
        self.stable()
        raw=(PRIOR/'source-bound-publish-rebuild.json').read_bytes();receipt=json.loads(raw)
        actual={p.relative_to(PRIOR/'source-bound-publish-rebuild').as_posix():module.sha(p.read_bytes()) for p in (PRIOR/'source-bound-publish-rebuild').rglob('*') if p.is_file()}
        module.require(receipt['source_head']==self.a.merge_sha and receipt['exit_code']==0 and receipt['matches_new_expected_manifest'] is True and receipt['all_file_sha256']==actual==self.expected,'Prior actual same-merge successful build bytes mismatch')
        self.write('source-bound-publish-rebuild-reuse.json',{'observed_at':module.now(),'purpose':'REUSE_ACTUAL_SUCCESSFUL_EXACT_MERGE_BUILD_NOT_REEXECUTED','original_receipt':str(PRIOR/'source-bound-publish-rebuild.json'),'original_receipt_raw_sha256':module.sha(raw),'source_head':self.a.merge_sha,'actual_disk_40_sha256_verified':True,'original_actual_execution':receipt,'new_execution_credit':0})
        self.stable()
a=module.parser().parse_args();v=None
try:
    v=ResumeExactSuccessfulBuild(a)
    (v.out/'executed-resume-driver.py').write_bytes(Path(__file__).read_bytes())
    (v.out/'owner-authorization.source.json').write_bytes(a.owner_exception.read_bytes())
    result=v.run();v.finish_manifest()
    print(json.dumps({'public_software_checks_status':'PASS','postmerge_whole_CI_status':result,'overall_full_quality_completion_asserted':False,'evidence':str(v.out)}),flush=True)
except Exception as e:
    if v:
        v.write('failure.json',{'observed_at':module.now(),'status':'FAIL','error':repr(e),'no_release_or_audit_credit':True});v.finish_manifest()
    traceback.print_exc();sys.exit(1)
