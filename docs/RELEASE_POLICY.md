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
11. GPT와 Claude가 각각 independent `FULLY_ADJUDICATED` legal `KEEP` 및 answer `YES`를 기록함.
12. Current style-profile version/hash를 사용한 independent realism `KEEP`/`PASS`가 있음.
13. `final_adjudication.decision == KEEP`.
14. Family의 `current_released_count <= max_questions_in_final_bank`.
15. Full QA와 tracked artifact drift check가 통과함.

정확한 pass/distinct-auditor/required-model 수는 `data/release_requirements.json`에서 schema-validated configuration으로 관리합니다. 현재 policy는 GPT+Claude legal passes 2개와 distinct auditor 2개를 요구합니다. `independent_audit_status: PASSED` 같은 summary field나 human override는 audit evidence를 대체할 수 없습니다. `DELETE`, `MAJOR_REWRITE`, `MINOR_EDIT` 또는 wrong-answer finding 후에는 current content에 대한 재감사와 새 `KEEP` adjudication이 필요합니다.

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
