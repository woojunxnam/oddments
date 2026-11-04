"""Seal only completed real validation; original draft bytes never change."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
P='reports/full-corpus-review/final19-census-author/w4-b-17-v2/'
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def write(path,obj):(ROOT/path).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
index=json.loads((ROOT/(P+'bundle-final-index.json')).read_bytes());native=json.loads((ROOT/(P+'bundle-native-final-validation.json')).read_bytes());proof=json.loads((ROOT/(P+'bundle-preservation-and-source-proof.json')).read_bytes());guard=json.loads((ROOT/(P+'bundle-own-head-strict-native-inventory-proof.json')).read_bytes());assert guard['source_guard_passed']and len(native['records'])==3 and all(r['native_validate_record']=='PASSED'for r in native['records'])
notes={'w4-b-17':'새2개는 SOURCE_BLOCKED이다. Media-fill 외 해당samplingfailure 뒤 재교육/재자격확인을 열거하되 FAQ53의시설별appropriatecorrectiveaction과MA2022advisory의media-fill한정권고를구별했다.현행section2.2/2.3전문·검사별범위·이후개정불확정한계를유지하며일률적cessation/조제허용을주장하지않는다.', 'w5-a-12':'새1개는지정공개FAQ대조 AUTHOR_SOURCE_CHECKED이다. FAQ166–168의BUD전administration시작경계를infusion지속과구별한다. 공개2023FAQ를현행fullchapter전문·제품규격·MA법규전수의확보증거로승격하지않고016/excipientSB를유지한다.', 'parallel-duties':'새2개는지정primary대조 AUTHOR_SOURCE_CHECKED이다. 24715.04(2),20.02(4),(5),45CFR164.530(j)의서로다른기록대상과기산점을구별한다.모든처방/inventory/CE/DSCSA대상·기산점전수목록을인증하지않고005DSCSASB를유지한다. 원GET완료시각이없는metadata에재독시각을대입하지않았다.'}
childenv=[]
for item,n,p in zip(index['records'],native['records'],proof['records']):
 uid=item['unit_id'];prefix='reports/full-corpus-review/final19-census-author/'+uid+'-v2/';assert uid==n['unit_id']==p['unit_id'];text=f'''# {uid} V2 실제 통합 후 최종 저자 제출

최종등록입력은 final-proposal-index.json / reassessment.json / final-census.json이다.
원초안commit {p['original_draft_commit']}의 파일{len(p['all_original_draft_files_byte_immutable'])}개는
바이트불변으로보존했다. 과거prep의pending/native미수행표시는당시상태그대로이며최종
실제결과는이문서와native-final-validation/final-preservation-and-source-proof에분리했다.
최종census의claim/source는초안과같고최상위stage만최종제출상태로표시했다.

원{item['original_claim_count']}개전체canonical claim/source/body를보존하여최종{item['final_claim_count']}개이다.
{notes[uid]}
원authorSB상태와현재actualindependent법규보류는별개축으로보존했다.
실제상속blocker명제수는{n['carried_legal_blocker_claim_count']}개이며원보고서finding/blocker/hash와
이전상속이력을native carried_legal_blockers에그대로남겼다.

실제INTEGRATEDparent는job{item['sequence']} {item['previous_job_id']}이다.
parentcanonicalSHA {item['previous_job_sha256']}
reportSHA {item['previous_report']['raw_sha256']}
resultSHA {item['previous_result']['raw_sha256']}
이parent는실제통합commit2f41b903ed1ea85bcbe4b7f88ca2555f3704fed0의object와같다.

자체fullcheckout에서root정합commit b19b58cfd56699fc62e0723b9ded621f73c45866를merge한
ownHEAD {guard['own_head']}에서실제q.inventory(root)→load_notes(root)의모든guard를통과했다.
그전체306개inventory SHA {guard['inventory_raw_sha256']}를보존하고자체HEAD의실제선택
ledger/census전량과bindings/bodySHA를재확인했다.공유ROOT의liveHEAD/contextoverride/
임의projection/가짜ledger/guard완화/monkeypatch에의존하지않았다.
커밋한최종record/census를검증HEAD {native['validation_head']}의실제
validate_record와unmodifieddisk_reader로검증하여통과했다.이는구문/바인딩검증이며
독립법규PASS/누락해소확정이아니다. 공식raw/text/meta/timestamp/버전한계를확인하고
PDF재추출이retainedtext와같음및원workercommit→자체HEAD→disk바이트일치를검증했다.
원metadata에없는시각이나개별조항효력일을만들지않았다.

기존A32/B19final·old9/final86·본문/원census/source/report·queue/ledger/generated/guard는
변경하지않았다.등록은전체19wave통합후root가수행한다.저자등록/공유쓰기/독립감사/
법규PASS/문항/canonicalreleasecredit는0이다.새실제비저자가최종census전량과원누락·
상속보류를다시심사해야한다. author-handoff-envelope은저자해시목록이며nativeworkerresult가아니다.
'''
 (ROOT/(prefix+'FINAL_STATUS.md')).write_text(text)
 fs=['final-proposal-index.json','reassessment.json','final-census.json','native-final-validation.json','final-preservation-and-source-proof.json','FINAL_STATUS.md'];env={'purpose':'AUTHOR_HANDOFF_ONLY_NOT_NATIVE_WORKER_RESULT','unit_id':uid,'author_provenance':json.loads((ROOT/(prefix+'preparation-index.json')).read_bytes())['author_provenance'],'actual_previous_job_id':item['previous_job_id'],'actual_previous_job_sha256':item['previous_job_sha256'],'artifacts':[{'path':prefix+f,'raw_sha256':sha(prefix+f)}for f in fs],'own_actual_source_guard_passed':True,'native_validate_record_passed':True,'controller_registration_performed':False,'independent_credit':0,'legal_pass_credit':0,'release_credit':0};write(prefix+'author-handoff-envelope.json',env);childenv.append({'unit_id':uid,'path':prefix+'author-handoff-envelope.json','raw_sha256':sha(prefix+'author-handoff-envelope.json')})
write(P+'bundle-author-handoff-envelope.json',{'purpose':'THREE_UNIT_AUTHOR_HANDOFF_NOT_NATIVE_WORKER_RESULT','child_envelopes':childenv,'bundle_index':{'path':P+'bundle-final-index.json','raw_sha256':sha(P+'bundle-final-index.json')},'bundle_native_validation':{'path':P+'bundle-native-final-validation.json','raw_sha256':sha(P+'bundle-native-final-validation.json')},'bundle_preservation':{'path':P+'bundle-preservation-and-source-proof.json','raw_sha256':sha(P+'bundle-preservation-and-source-proof.json')},'own_actual_source_guard_proof':{'path':P+'bundle-own-head-strict-native-inventory-proof.json','raw_sha256':sha(P+'bundle-own-head-strict-native-inventory-proof.json')},'controller_registration_performed':False,'independent_credit':0,'legal_pass_credit':0,'question_credit':0,'release_credit':0})
m=P+'bundle-artifact-sha256.json';files={}
for item in index['records']:
 prefix='reports/full-corpus-review/final19-census-author/'+item['unit_id']+'-v2/'
 for f in sorted((ROOT/prefix).rglob('*')):
  rel=str(f.relative_to(ROOT))
  if f.is_file()and rel!=m:files[rel]=sha(rel)
write(m,{'files':files,'manifest_excludes_itself':True,'all_original_draft_artifacts_immutable':True,'independent_credit':0,'release_credit':0});print('Sealed',len(files),'artifact hashes')
