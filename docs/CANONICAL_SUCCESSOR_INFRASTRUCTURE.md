# Canonical successor 비활성 인프라

이 변경은 새 canonical 문항을 받기 위한 경계 검사와 한국어 QA 정규화 수정입니다. 현재 문항·규정·감사·가족 행렬·통합노트·생성 payload는 바꾸지 않습니다. 기존 보호 verifier와 release gate도 수정하지 않습니다. 신규 admission·법규 감사·현실성 감사·RELEASED·배포 credit은 모두 0입니다.

## 구현 범위

`scripts/canonical_successor.py`는 실제 regular file과 immutable Git commit의 blob preimage를 읽습니다. Git 조회는 checkout, clone, baseline 등록 없이 수행합니다. source reader는 누락·중복·경로 이탈·symlink를 거부합니다. Git commit과 파일 목록은 별도로 신뢰할 수 있는 manifest에서 공급해야 하며, reader가 임의 commit을 승인하지 않습니다.

경계 검사는 frozen inventory와 기대 바이트를 재등록하지 않고 원본 파일을 대조합니다. 추가 파일은 `data/questions/`, `data/audits/`, `data/rules/`, `data/drugs/`의 정확한 직접 JSON 경로·크기·SHA에 한정합니다. 기존 canonical 질문과 family의 semantic 입력도 실제 봉인된 원문 바이트에 결박합니다. 기존 family의 의미·규정·cap·순서를 유지하고 실제 registry 개수만 반영하며, 새 행은 실제 새 질문에 사용되어야 합니다. ordinary INITIAL 후보는 기존 규정대로 30–40개입니다.

이 검사는 native JSON schema, transitive dependency, 공식 법규, 독립성, near duplicate, 실제 native audit와 final adjudication 검사를 대체하지 않습니다. `verify_proposal()` 통과는 **경계만 확인한 미승인 제안**입니다. 질문의 새 ID·family로 기존 본문을 재등장시키는 정확 중복도 거부하지만, 별도 독립 중복·현실성 감사가 계속 필요합니다.

원 published16 manifest·기존 source bindings·note MD/build/내용·claim ledger를 그대로 둔 source-only context와 manifest/context/enrollment의 비순환 해시 관계를 검사합니다. 출력 전체 키와 각 SHA는 별도 필수 `trusted_output_seals`에 정확히 결박합니다. 이 Seal map은 호출자가 별도 신뢰된 immutable commit/blob에서 읽어야 하며, before/after에 같은 임의 SHA를 쓰는 것만으로는 `content.js`를 바꿀 수 없습니다. Seal map의 신뢰·승인을 이 순수 함수가 자체 인증하지 않으며 호출자가 만든 map은 admission 승인이나 실제 replay 근거가 아닙니다. `legacy_seal_projection_only()`는 바이트 경계가 맞는 원본 뷰의 모델일 뿐 실제 legacy replay를 실행하지 않습니다. 실제 실행 credit을 만들지 않습니다.

## 기본 거부

```sh
python scripts/canonical_successor.py
```

결과는 `INFRASTRUCTURE_INACTIVE`, `activation_allowed: false`입니다. 아직 지원하지 않는 `revisions/canonical/active-admission.json`이 존재하거나 symlink이면 실패합니다. `approved:true`, 호출자가 공급한 PASS receipt, 임의 keyword로 활성화할 수 없습니다. 적용·등록·승격 API가 없습니다.

기존 verifier는 이 모듈로 dispatch하지 않으며 신규 data source와 원본 변경을 계속 거부합니다. 원래 1,781 preimage baseline, 439개 canonical, 397개 RELEASED membership, Q0012/Q0028 격리, 현재 delivery hold 16개를 해제하지 않습니다. 새 module에 법규 판정을 재구현하여 기존 native gate와 경쟁시키지 않습니다.

## 한국어 정규화

기존 `qa_common.normalize_text()`는 ASCII 외 문자를 지워 서로 다른 순한글 설명을 같은 빈 문자열로 만들었습니다. NFC와 Unicode 문자·숫자·결합문자 보존으로 수정합니다. 동일 한국어의 중복 검사는 유지하며 영어 삽입이나 중복 검사 생략을 하지 않습니다. ASCII 결과·숫자 masking·기존 `<num>` placeholder 동작을 유지합니다. `question_audit_hash()` 및 semantic hash 구현은 바꾸지 않습니다.

공개 테스트는 원본 비공개 후보를 포함하지 않습니다. 합성 한국어 사례, 402개 ASCII 입력의 두 masking 모드, 실제 기존 397개 payload의 audit hash, 원 guard/생성기 바이트, 기존 439/397 및 hold hash를 검사합니다.

## 기준과 보존 증거

이 worktree의 시작 commit은 `2880a4537137d90a6bb6a300bdecb955fab415fd`입니다. 이전 scratch preimage 캡처는 `8c3a34c8369761bfcc09825361f1942f2af7b78c`에서 수행됐습니다. 그 이후 2880까지 바뀐 것은 UI 안내 1파일·CI workflow 1파일·CI 복구 보고서 6파일입니다. canonical/data/notes와 원 보호 verifier는 바뀌지 않았습니다. 이전 원1781 Git blob archive·6487 seal 증거를 새 기준으로 덮어쓰지 않습니다. 이번 저장소에는 비공개 원문·31개 후보·원본 이미지·Drive 링크를 추가하지 않습니다.

## 활성화 전에 남은 구현과 입력

- 실제 최종 native 질문·규정·drug·audit 원문, 선택한 family append와 정확한 승인 delta가 필요합니다. 새 native hash에 대한 실제 nonauthor INITIAL legal 및 realism 감사·duplicate CLEAR·final KEEP과 current dependency snapshot이 필요합니다.
- generic approval enrollment와 엄격한 dispatch는 아직 구현하지 않았습니다. source context가 원 published16을 참조하되 원 manifest나 해시를 바꾸지 않아야 합니다. 해시는 `content/base/guard → manifest → note context → enrollment → final HEAD` 방향으로만 결박해야 합니다.
- 실제 immutable base의 별도 read-only filesystem에서 원 guard를 실행하고, current candidate 전체 경계를 먼저 검사한 사실과 연결해야 합니다. projection을 replay PASS로 계산하거나 실패한 원 guard를 무시하면 안 됩니다. 원 API의 기본 439/397 동작·기존 반환값을 유지해야 합니다.
- 실제 release는 preview와 generated payload에도 새 항목을 추가하므로 별도 정확한 semantic append 계약이 필요합니다. 기존397 object·ID·key·audit history·순서를 유지하고 Q0012/Q0028 및 기존16 delivery holds를 계속 보호해야 합니다. 현재 경계 함수는 그 기존 출력 변경을 거부합니다.
- root 인자가 없는 기존 `coverage_snapshot()`의 고정397 API를 일괄 숫자 변경하지 말고 명시적으로 검증된 successor context와 별도 coverage artifact를 연결해야 합니다. 기존306단위/7086 claim의 census가 새 rule까지 검토했다고 집계하지 않습니다.
- 실제 전체 native QA·artifact drift·독립 코드 검토·CI·배포는 해당 활성화 후보가 존재할 때 수행해야 합니다. 이번 단계는 활성화를 시도하지 않습니다.
