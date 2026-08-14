# Release Policy

## Lifecycle

```text
DRAFT -> SOURCE_VERIFIED -> AUTOMATED_QA_PASS -> AUDIT_PENDING
      -> AUDITED -> ADJUDICATED -> RELEASED

RELEASED -> REVIEW_REQUIRED
```

Semantic dependency 변경, question content 변경, stale audit, failed legal/realism review가 있으면 `REVIEW_REQUIRED`로 돌아가야 합니다. Validator는 invalid released record를 자동 수정하지 않고 release output을 실패시킵니다.

## Machine-enforced release gates

`RELEASED` question은 다음을 모두 만족해야 합니다.

1. `verification_status`와 `lifecycle_status`가 모두 `RELEASED`.
2. 모든 direct rule이 `CURRENT`이고 verified이며 schema와 stored semantic hash가 유효함.
3. 모든 drug가 verified이고, legal consequence rule이 존재하며 current/verified이고, drug의 transitive dependency snapshots가 current임.
4. Blueprint와 style profile의 stored semantic hash가 current이며 target exam date가 release window 안에 있음.
5. Final adjudication의 rule/drug/blueprint/style-profile version/hash snapshot이 현재 canonical dependencies와 정확히 일치함.
6. `SBA`는 1 answer, `SATA`는 1개 이상, `ORDERED_RESPONSE`는 모든 choice의 complete unique order.
7. Placeholder가 없고 모든 choice rationale가 존재하며 중복되지 않음.
8. `duplicate_review_status == CLEAR`이고 difficulty/reasoning-step contract를 만족함.
9. Valid independent fully adjudicated legal `INITIAL_BATCH` audit history가 있음.
10. 모든 current evidence audit ID가 `data/audits/` record로 resolve되고 current question hash를 대상으로 함.
11. 현재 policy가 요구하는 independent `FULLY_ADJUDICATED` legal `KEEP`/answer `YES`가 기록되어야 함.
12. Current style-profile version/hash를 사용한 independent realism `KEEP`/`PASS`가 있음.
13. `final_adjudication.decision == KEEP`.
14. Family의 `current_released_count <= max_questions_in_final_bank`.
15. Full QA와 tracked artifact drift check가 통과함.

정확한 pass 수, distinctness 기준, required auditor type은 `data/release_requirements.json`에서 schema-validated configuration으로 관리합니다. 현재 policy는 **1개의 fresh independent auditor instance**가 current question hash에 대해 legal `KEEP`/answer `YES`와 realism `KEEP`/`PASS`를 모두 제공하면 audit-count gate를 충족하도록 설정합니다. Legal과 realism은 별도 canonical audit record로 남길 수 있지만 같은 genuinely independent session의 동일 `auditor_instance`를 사용할 수 있습니다. 특정 model vendor 조합은 강제하지 않습니다.

`auditor`는 model/family provenance이고 `auditor_instance`는 실제 독립 감사 세션 provenance입니다. Author/editor가 자신이 방금 수정한 current content를 independent auditor로 자가 인증할 수 없습니다. 추가 second-opinion audit은 ambiguous authority, conflicting official sources, 또는 editor 판단에 따라 요청할 수 있지만 기본 release gate는 아닙니다. 이미 존재하는 current-hash audit가 `DELETE`, `MAJOR_REWRITE`, `MINOR_EDIT`, wrong-answer 또는 realism `FAIL`을 기록했다면 이를 무시하거나 다른 auditor의 KEEP으로 override해 unchanged question을 release할 수 없습니다. 문제를 수정한 뒤 새 current-hash audit와 새 `KEEP` adjudication이 필요합니다.

`independent_audit_status: PASSED` 같은 summary field나 human override는 canonical audit evidence를 대체할 수 없습니다.

## Output status

- `NO_RELEASED_QUESTIONS`: release build에 question이 0개
- `DEVELOPMENT_ONLY`: `--include-fixtures`로 만든 명시적 local fixture build
- `RELEASE_AVAILABLE`: 1개 이상의 release-eligible question이 포함됨

Question-level `RELEASED`가 권위입니다. 빈 payload를 “safe to memorize”로 표시하지 않습니다.

## Generated artifact policy

Tracked deterministic strategy를 사용합니다. 다음 명령이 모든 report/site payload를 갱신합니다.

```bash
python scripts/generate_artifacts.py --write
```

CI는 재생성한 뒤 git diff가 있으면 실패합니다. Stale generated file은 authoritative하지 않습니다.
