# Canonical guarded admission: 등록 context 구현과 현재 차단 상태

이 단계는 `ea19d9881ec5b6a476f7dfc113cd1a4bc18c92da`의 별도 branch에서 진행했습니다. 실제 canonical·rule·drug·audit 원문을 추가하거나 승격하지 않았습니다. `APPROVED_ADMISSIONS`와 `APPROVED_BASE_GUARD_PROOFS`는 비어 있습니다. 현재 명령의 결과는 `NO_ENROLLED_ADMISSION`이며 임의 `approved:true`·PASS JSON·빈 enrollment는 거부합니다. enrollment/manifest/context는 정확한 HEAD regular blob과 디스크 바이트가 같아야 합니다.

## 실제 구현

- `canonical_native_view.py`: immutable Git blob의 원 data/schema와 정확한 제안 파일을 읽는 메모리 view입니다. 원문을 새 worktree나 공개 경로에 복제하지 않습니다. native schema/rule/drug/audit/question/governance/guide·source permission·중복·출제 패턴·시행일 검사를 실제 원 함수로 실행합니다. `qa_common`의 기본 disk 함수는 유지하고 scoped reader에서만 교체하며, 해당 scope의 writer는 거부합니다.
- `canonical_admission.py`: reviewed constant registry가 결박한 enrollment/manifest/source-only note context만 해석합니다. 기존 전체 보호 inventory와 Git blob identity를 대조하고 additions는 신규 question/audit/rule/drug의 정확한 직접 JSON 경로로 제한합니다. 기존 변경은 family append/count·preview append·generated question append·delivery HOLD 증가 및 고정4개 native 분석 report의 정확한 before/after에 한정합니다. 해당4개는 duplicate/answer-distribution/structural-pattern/SBA-length report이며 실제 producer의 재계산 값과 같아야 합니다. 원439 ID/body/key/이력/status와 원397 membership 및 격리2개를 유지합니다.
- source-only note context는 원 notes16 raw manifest와 기존 source bindings를 유지하고 전체 note 출력/claim ledger를 바꾸지 않습니다. 새 native source delta는 별도로 결박합니다. 기존306단위/7086 claim이 새 rule을 검토했다고 계산하지 않습니다.
- current runtime Python source 전체는 이미 trusted base에 존재해야 하며 content commit과 manifest에 결박합니다. base→content 전체 Git delta는 선언된 data/고정 출력/HOLD 근거에만, content→최종 HEAD는 manifest/context/enrollment/registry/그 ID의 계산 coverage에만 한정합니다. 소비 시 전체 보호 inventory를 다시 열거하고 dirty tracked source도 거부합니다. 새 계산coverage 외의 untracked source를 거부하며, Pages에 포함될 수 있는 ignored 파일까지 site 전체 disk/HEAD inventory로 대조합니다. 각 공개 파일은 HEAD의 실제 regular blob 바이트와도 직접 비교하므로 assume-unchanged/skip-worktree Git index 플래그가 본문 변경이나 외부 symlink를 감추지 못합니다. reviewed trust-root registry만 별도로 두어 자기 hash 순환을 피합니다. `base/code → content → manifest → notes context → enrollment/registry` 순서이며 content commit에는 자기 manifest/context/enrollment/coverage가 없어야 합니다. 새coverage는 manifest/context hash만 사용하는 계산 출력으로 그 뒤 생성할 수 있고, 존재하면 항상 실제 native 계산과 일치해야 합니다. manifest가 coverage의 미래 SHA를 요구하는 자기참조는 없습니다. ID와 resolved 출력 namespace 및 symlink를 검사합니다.
- 성공 분기는 모든 실제 native 검사가 통과한 뒤에만 usable context를 만듭니다. 외부에서 만든 context 객체나 `verify_withheld_reference() == True` 객체로 guide의 기존 철회 보호를 우회할 수 없습니다. 소비 시 파일과 code seal을 다시 확인합니다. 새 초기 audit는 새 ID만 다루고 author/session과 달라야 하며, 새31의 예전 private full-record PASS를 native audit로 옮기지 않습니다.
- 원1781/withdrawal/note decoder/default coverage API는 수정하지 않습니다. 별도의 adapter는 기본 호출에서 원 함수를 그대로 실행하고, 명시적인 registered context에서만 실제 guard 결과에 결박된 reviewed base-proof를 사용합니다. 이 결과를 이번 실행의 legacy replay로 표시하지 않습니다. 원 withdrawal의 preview를 포함한 4개 preimage 반환값도 보존합니다.
- root 인자가 없는 기존397 coverage API는 그대로입니다. registered producer는 원397 object와 preview 순서/감사 이력을 유지하며 실제 native producer 출력만 허용합니다. 공개 coverage adapter는 count만 확인하지 않고 검증 때 실제 producer가 만든 전체 coverage/guide/payload와 caller 입력이 같아야 합니다. 현재 coverage는 기존 historical 파일을 덮지 않는 별도 `reports/canonical-successor/<id>-coverage.json`으로 반환합니다.

## Delivery HOLD와 별도 안전 철회

기존16을 상한으로 두지 않습니다. 전달받은 실제 공개 UI commit `c7d5162fa8deb75d61f17ec02159e69634ffcbd7`의19 HOLD를 ID/current-hash floor로 결박했습니다. 원 overlay SHA는 `75cc99ba2bff3df34f6cc96a0b85ba63383baf7d14588076fad92d3efd18d376`입니다. 새 등록 context는19개를 모두 보호하고, base의 원 HOLD 배열/판정/출처를 제거하거나 바꾸지 못합니다. 이후 추가 HOLD도 같은 방식으로 보존해야 합니다. 이것은 canonical status를 변경한 것이 아닙니다.

`APPEND_CANONICAL_INITIAL`은 원397 status·old-ID audit history를 유지합니다. 실제 native REAUDIT19에 근거한 metadata-only safety withdrawal은 별도 context kind와 정확한 status/audit-append transaction이 필요하며 이번 경로에서 허용하지 않습니다. 그때 raw payload에서 제외된 held ID와 runtime overlay를 연결하는 별도 계약도 필요합니다. 이를 무시하거나 old397 보호 수를 일괄 낮추지 않습니다.

## 실제 실행과 미완료 범위

실제 private working31-v2를 native 함수로 읽기 전용 검사했습니다. 현재9 errors/9 warnings, audit refs0/final KEEP0이며 미완성 drug·family 등의 원 blocker를 유지했습니다. 보고서는 private 폴더에만 있습니다. 실제 immutable ea19 원439에 대한 native 검사는 통과했으나 이것은 새 admission·법규 감사·승격이 아닙니다.

`prepare_canonical_base_proof.py`는 과거 실제1781 PASS의 선택된 immutable 입력 tree가 현재 base와 정확히 같은지 비교하고, 원 withdrawal API의 실제4 preimage를 Git blob identity로 찾는 미승인 검토 초안을 만듭니다. 원 baseline이나 registry를 갱신하지 않습니다. 과거 결과와 다른 입력이면 실제 재검증이 필요합니다.

현재 production 등록이 없어 **완전한 신규30–40 등록의 성공 분기는 실제 candidate로 실행하지 않았습니다**. 현재 계약은 첫 ordinary INITIAL append용이며, 이후 source-only 코드 변경·다음 append·안전 철회의 버전된 context lifecycle도 production 등록 전에 더 구현·검증해야 합니다. 승인된 최초 등록 뒤 무관한 변경을 조용히 허용하는 방식으로 완화하지 않습니다. 또한 CI의 기존 직접 verifier/generator 호출과 역사적439/397 고정 테스트를 새 adapter에 연결하는 통합은 아직 완료하지 않았습니다. 기존 직접 호출은 실제 새 data가 생기면 계속 실패하며 이것을 skip하거나 PASS로 바꾸지 않았습니다. 따라서 아직 production admission을 활성화할 수 없습니다.

다음이 실제로 필요합니다: 최종 native hash의 nonauthor legal/realism·family/duplicate·source-use 검토와 final KEEP, 검증된 새 dependencies, 검토된 base-proof 및 exact enrollment 등록, 역사적 assertion을 원 실제 base에 결박하는 CI/test routing, 실제 전체 QA/artifact drift/독립 코드 검토. private31의 HOLD를 해제하거나 synthetic 테스트를 실제 release로 계산하지 않습니다.

```sh
python scripts/guarded_canonical_admission.py --operation status
python scripts/preflight_external_canonical.py --proposal /private/proposal --output /private/result.json
```

새 wrapper의 `protected`, `withdrawal`, `artifacts` operation은 등록이 없으면 원 strict 경로를 사용합니다. `artifacts --write`는 명시적인 실제 artifact 생성 명령이며 이번 단계에서는 실행하지 않았습니다. UI 후보의 CI/배포 결과와 이 branch의 QA는 분리합니다.

## 정당한 targeted initial 정책과 향후 별도 지원

현재 `APPEND_CANONICAL_INITIAL`과 새 ID helper는 ordinary30–40 전용입니다. 기존 정책의 `TARGETED_INITIAL_BATCH`1–29를 폐지하거나 ordinary 최소치를 낮춘 것이 아닙니다. `validate_audits.py`의 기존3 authorization entries는 불변이며, 정식 등록 없는 focused11은 계속 거부합니다. preflight는 원 native audit validator로 해당 정책을 검사하지만 새 registered adapter의 targeted 경로는 아직 구현하지 않았습니다.

향후 지원에는 actual authorizing Issue·정확 tranche·선행 S0·exact ID set을 source-bound authorization에 등록하고 원 `is_valid_targeted_initial_audit()`와 일치시켜야 합니다. raw caller field나 `approved:true`로 등록하지 않습니다. 수를 맞춘 filler도 만들지 않습니다. S0는 private 문항 본문을 공개하지 않는 후보 ID/native-hash/dependency lock만 담는 선행 commit으로 만들 수 있으며 자기 commit SHA를 payload에 넣지 않습니다. 그 다음 Issue/authorization code를 확정해 trusted engine base에 포함하고, content/M/N/enrollment를 뒤에 만듭니다. 권한 표가 미래 자신의 source hash를 요구하지 않도록 합니다.

S0의 initial history와 최종 current-hash legal/realism 검사는 구분해야 합니다. 수정 뒤의 정당한 REAUDIT는 원 release policy의 절차로 다루되 이전 private PASS를 새 native hash에 옮기지 않습니다. 이 설명은11개 tranche의 실제 승인·등록이 아니며, 현재 source/family/감사 HOLD를 해제하지 않습니다.
