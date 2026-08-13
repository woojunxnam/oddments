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
4. Final adjudication의 direct rule/drug version/hash snapshot이 현재 canonical dependencies와 정확히 일치함.
5. `SBA`는 1 answer, `SATA`는 1개 이상, `ORDERED_RESPONSE`는 모든 choice의 complete unique order.
6. Placeholder가 없고 모든 choice rationale가 존재하며 중복되지 않음.
7. `duplicate_review_status == CLEAR`.
8. Difficulty/reasoning-step contract를 만족함.
9. 최소 1개 audit ID가 있고 모든 ID가 `data/audits/` record로 resolve됨.
10. Current question hash를 대상으로 한 independent `FULLY_ADJUDICATED` `LEGAL_VERIFICATION` result가 `KEEP`이고 answer가 `YES`.
11. Current question hash를 대상으로 한 independent `FULLY_ADJUDICATED` `REALISM_REVIEW` result가 `KEEP`/`PASS`.
12. 현재 style profile을 사용한 structured `realism` assessment가 있음.
13. `final_adjudication.decision == KEEP`.
14. Full QA와 tracked artifact drift check가 통과함.

`independent_audit_status: PASSED` 같은 summary field만으로는 9-11을 대체할 수 없습니다. `DELETE`, `MAJOR_REWRITE`, `MINOR_EDIT`는 release를 승인하지 않습니다. Edit 후 current content에 대한 재감사와 새 `KEEP` adjudication이 필요합니다.

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
