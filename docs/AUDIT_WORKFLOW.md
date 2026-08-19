# Audit Workflow

## Canonical audit records

Export와 prose report는 `audits/<auditor>/...`에 둘 수 있지만 release logic은 `data/audits/*.json`만 읽습니다. Canonical audit는 `schemas/audit.schema.json`을 통과해야 합니다.

- `INITIAL_BATCH`: 30-40 unique questions. 신규 item의 bank-admission 이력을 만듭니다. 이 30-40 범위는 그대로 유지됩니다.
- `TARGETED_INITIAL_BATCH`: 1-29 unique questions. Governance가 명시적으로 승인한 targeted tranche 전용이며 ordinary `INITIAL_BATCH`의 최소치를 낮추지 않습니다. Record에 `governance_authorization`(`tranche_id`, `authorizing_issue`, `represented_candidate_sha`, exact `question_ids`)이 필요하고 `independent: true`와 `audit_status: FULLY_ADJUDICATED`가 요구되며, `scripts/validate_audits.py`의 authorization table에 등록된 tranche만 유효합니다. 근거는 [Issue 78 Targeted-Initial Governance Report](ISSUE_78_TARGETED_INITIAL_GOVERNANCE_REPORT.md)를 참조하십시오.
- `REAUDIT`: 1-40 unique questions. Semantic edit로 hash가 바뀐 일부 item의 focused review에 사용합니다.

Release item은 valid independent fully adjudicated legal initial 이력이 있어야 하며, 이는 ordinary `INITIAL_BATCH` 또는 governance가 승인한 `TARGETED_INITIAL_BATCH` 중 하나로 충족됩니다. `REAUDIT`만으로 신규 item을 하나씩 release하는 것은 불가능합니다.

각 batch에서 다음 세 집합은 정확히 같아야 합니다.

```text
set(question_ids)
== set(question_hashes.keys())
== set(results[].Question_ID)
```

Duplicate, missing, extra, unknown Question_ID는 모두 오류입니다.

## Auditor provenance and independence

- `auditor`는 model/family provenance입니다: `GPT`, `CLAUDE`, `HUMAN`.
- `auditor_instance`는 실제 독립 감사 세션/instance provenance입니다.
- Release distinctness는 `data/release_requirements.json`의 `distinctness_basis`에 따라 계산합니다.
- 현재 policy는 `AUDITOR_INSTANCE` 기준으로 **1개의 fresh independent current-hash auditor instance**를 요구합니다.
- 동일한 independent session이 별도 `LEGAL_VERIFICATION` record와 `REALISM_REVIEW` record를 제출할 수 있으며 두 record에 같은 `auditor_instance`를 기록합니다.
- 같은 audit session을 여러 파일이나 여러 instance 이름으로 쪼개어 독립 audit 수를 부풀리면 안 됩니다.
- Author/editor가 자신이 방금 수정한 current content를 별도 independent auditor로 자가 인증하면 안 됩니다.
- 두 번째 independent legal opinion은 기본 release requirement가 아닙니다. Authority conflict, ambiguity 또는 editor 판단이 있을 때 추가로 요청할 수 있습니다.

## Separate reviews

### LEGAL_VERIFICATION

`FULLY_ADJUDICATED`이면 모든 result에 다음이 필요합니다.

- `Existing_Answer_Correct != NOT_ASSESSED`
- 하나 이상의 `authorities[]`
- 각 authority의 nonempty `authority`, official-only `source_type`, `exact_section`
- 각 authority의 HTTPS `official_url`과 non-null `law_checked_date`
- verdict와 correction fields

### REALISM_REVIEW

Legal accuracy와 분리해 다음을 평가합니다.

- actual jurisprudence reasoning을 요구하는가
- pharmacy practice stem이 plausible한가
- distractor가 genuine legal confusion에서 나오는가
- wording만으로 정답을 추측할 수 없는가
- difficulty가 trivia가 아니라 reasoning에서 나오는가
- rules가 자연스럽게 결합되는가
- drug context가 적절한가
- canonical bank의 다른 item과 과도하게 유사하지 않은가
- 단순 schedule flashcard가 아닌가
- public NABP style을 따르되 wording을 재현하지 않는가

`PASS`는 모든 criterion이 true일 때만 가능합니다. Audit top-level `style_profile`은 사용한 profile ID/version/hash를 고정합니다. Question JSON에는 realism result를 복제하지 않습니다.

## Triage

`STRUCTURAL_TRIAGE_ONLY`는 legal fields를 `NOT_ASSESSED`로 둘 수 있지만 release gate를 만족하지 않습니다. Triage를 legal verification 또는 realism pass로 해석하지 않습니다.

## Procedure

1. `scripts/export_audit_batch.py --audit-scope INITIAL_BATCH|REAUDIT --review-type ... --auditor-instance ...`로 stable batch와 question hashes를 export합니다.
2. Fresh independent auditor는 canonical questions를 수정하지 않고 current official sources와 public style profile을 검토합니다.
3. 같은 independent session에서 completed legal record와 realism record를 `data/audits/`에 저장할 수 있습니다. 두 record는 동일한 `auditor_instance` provenance를 사용합니다.
4. Editor가 결과를 adjudicate합니다.
5. `MINOR_EDIT`/`MAJOR_REWRITE`이면 canonical question을 수정하고 affected legal/realism evidence를 새 current hash에 대해 다시 수행합니다.
6. `DELETE`이면 release하지 않습니다.
7. Required current-hash legal evidence가 `KEEP`/answer `YES`, realism이 current profile에 `KEEP`/`PASS`일 때만 final human/editor `KEEP`을 기록합니다.

Current-hash audit가 ambiguity, `MINOR_EDIT`, `MAJOR_REWRITE`, `DELETE`, wrong answer 또는 realism `FAIL`을 기록하면 unchanged question을 다른 opinion으로 override하여 release하지 않습니다. Editor는 추가 research나 optional second opinion을 요청할 수 있지만, release하려면 defect를 해결한 current content에 대한 유효한 fresh audit evidence가 필요합니다.

Rigorous `DELETE`는 audit 성공이며 억지로 positive result를 만들지 않습니다.
