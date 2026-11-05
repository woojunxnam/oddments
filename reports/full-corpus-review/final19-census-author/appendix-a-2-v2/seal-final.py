"""Seal only completed actual native A96 validation; not an audit result."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];P='reports/full-corpus-review/final19-census-author/appendix-a-2-v2/'
def raw(path):return (ROOT/path).read_bytes()
def sha(path):return hashlib.sha256(raw(path)).hexdigest()
def write(path,obj):(ROOT/path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
i=json.loads(raw(P+'final-proposal-index.json'));n=json.loads(raw(P+'native-final-validation.json'));p=json.loads(raw(P+'final-preservation-and-source-proof.json'));g=json.loads(raw(P+'own-head-strict-native-inventory-proof.json'));assert n['native_validate_record']=='PASSED'and n['carried_legal_blocker_claim_count']==29 and g['source_guard_passed']is True
text=f'''# appendix-a-2 V2 실제 Job69 통합 후 최종 저자 제출

최종입력은 final-proposal-index.json / reassessment.json / final-census.json이다.
원40136a50의초안16개파일은그대로보존했다.8393b0f9와40136a50의문서수정이력도각
commit별원SHA로구별해남겼으며그사이claim/source/body는같다.과거prep의pending과
native미수행표시는당시상태이다.최종census의93원명제+새3개와sources는초안그대로며,
최상위stage만최종제출로표시했다.이문서와새native/proof파일이실제최종검증결과이다.

A012methadone,A014TIRF행fentanyl,A017단일codeine의MAII편입효과3개만append했다.
105CMR700.002(B)의실제편입문과21CFR1308.12(c)(15),(c)(9),(b)(1)(i)의정확성분
entry를함께대조했다.연방분류만MA근거로대체하지않고,정확brandmapping·route·현재공급·
TIRFREMS·OTP/pain처방권한또는주별법전수의확인으로확대하지않는다.원authorstatus와
실제독립29SB는별개축으로보존했다.29개finding/blocker/원reportSHA및상속이력은
실제native carried_legal_blockers에그대로남겼다.원93개전체canonical claim/source/
body를그대로보존해96개이며,new3AUTHOR_SOURCE_CHECKED는독립법규KEEP가아니다.

실제parent는Job69 {i['previous_job_id']}이다.
parentcanonicalSHA {i['previous_job_sha256']}
reportSHA {i['previous_report']['raw_sha256']}
resultSHA {i['previous_result']['raw_sha256']}
이는95ef5df81a5118fc22d83b08478f84a68373ab95의실제INTEGRATEDobject와같다.
선택ledger는여전히원93개binding이며이author는등록하지않았다.

자체fullcheckout의정합rootbase b8cf09fad15fec320b1361652ae755e0d65725bb를merge한
ownHEAD {g['own_head']}에서actualq.inventory(root)→notes_revision.load_notes(root)
전체guard를통과했다.자체전체306개inventorySHA {g['inventory_raw_sha256']}를보존하고
실제committedledger/census전량의bindings/bodySHA를다시확인했다.공유ROOTlivecontext/
임의projection/가짜ledger/guard완화/monkeypatch에의존하지않았다.
커밋한최종record/census를검증HEAD {n['validation_head']}의실제
validate_record와unmodifieddisk_reader로검증하여통과했다.구문/바인딩검증을독립감사나
법규PASS/누락해소확정으로계산하지않는다.참조{p['reference_count']}개HEAD==disk와
원401초안/이전f842bundle/A32/B19/old9/final86불변도확인했다.

MA PDF및eCFRHTML의원raw/text/meta6개는원workercommit→자체HEAD→disk가같다.
MA PDF재추출text는savedtext와같고HTML의지정성분원문도읽었다.원GET시작/완료
시각·각SHA·검토일·버전/효력일한계를보존했다.MA통합PDF Register1514/2024-02-02와
eCFRtitle21 current2026-11-02표시를개별조항최초효력일/후속개정전수로승격하지않는다.

기존본문/source/census/report/queue/ledger/generated/guard및공유ROOT변경은0이다.
등록은현재마지막3개wave를모두통합한후root가6개V2를대상으로수행한다.독립감사/
법규PASS/문항/canonicalreleasecredit는0이다.새실제비저자가최종96개전량과원누락3개/
상속SB를다시심사한다.author-handoff-envelope은저자해시목록이며nativeworkerresult가아니다.
'''
(ROOT/(P+'FINAL_STATUS.md')).write_text(text)
fs=['final-proposal-index.json','reassessment.json','final-census.json','native-final-validation.json','final-preservation-and-source-proof.json','own-head-strict-native-inventory-proof.json','FINAL_STATUS.md'];write(P+'author-handoff-envelope.json',{'purpose':'AUTHOR_HANDOFF_ONLY_NOT_NATIVE_WORKER_RESULT','author_provenance':i['author_provenance'],'previous_job_id':i['previous_job_id'],'previous_job_sha256':i['previous_job_sha256'],'artifacts':[{'path':P+f,'raw_sha256':sha(P+f)}for f in fs],'own_actual_source_guard_passed':True,'native_validate_record_passed':True,'controller_registration_performed':False,'independent_credit':0,'legal_pass_credit':0,'question_credit':0,'release_credit':0})
m=P+'final-artifact-sha256.json';files={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest()for f in sorted((ROOT/P).rglob('*'))if f.is_file()and str(f.relative_to(ROOT))!=m};write(m,{'files':files,'manifest_excludes_itself':True,'original_draft_bytes_and_remote_history_preserved':True,'independent_credit':0,'release_credit':0});print('Sealed',len(files),'A96 artifact hashes')
