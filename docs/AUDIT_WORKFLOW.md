# Audit Workflow

## Canonical audit records

Export와 prose report는 `audits/<auditor>/...`에 둘 수 있지만 release logic은 `data/audits/*.json`만 읽습니다. Canonical audit는 `schemas/audit.schema.json`을 통과해야 합니다.

- `INITIAL_BATCH`: 30-40 unique questions. 신규 item의 bank-admission 이력을 만듭니다.
- `REAUDIT`: 1-40 unique questions. Semantic edit로 hash가 바뀐 일부 item의 focused review에 사용합니다.

Release item은 valid independent fully adjudicated legal `INITIAL_BATCH` 이력이 있어야 합니다. `REAUDIT`만으로 신규 item을 하나씩 release하는 것은 불가능합니다.

각 batch에서 다음 세 집합은 정확히 같아야 합니다.

```text
set(question_ids)
== set(question_hashes.keys())
== set(results[].Question_ID)
```

Duplicate, missing, extra, unknown Question_ID는 모두 오류입니다.

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

1. `scripts/export_audit_batch.py --audit-scope INITIAL_BATCH|REAUDIT --review-type ...`로 stable batch와 question hashes를 export합니다.
2. Auditor는 canonical questions를 수정하지 않고 current official sources 또는 public style profile을 검토합니다.
3. Completed record를 `data/audits/`에 저장하고 exact set validation을 통과시킵니다.
4. Editor가 결과를 adjudicate합니다.
5. `MINOR_EDIT`/`MAJOR_REWRITE`이면 canonical question을 수정하고 GPT/Claude legal audit와 affected realism audit를 current hash에 대해 다시 수행합니다.
6. `DELETE`이면 release하지 않습니다.
7. GPT와 Claude가 모두 current hash에 `KEEP`/answer `YES`, realism이 current profile에 PASS일 때만 final human/editor `KEEP`을 기록합니다.

GPT와 Claude가 불일치하면 release는 실패합니다. Human/editor는 추가 research와 edit를 수행할 수 있지만 failed current audits를 override해 unchanged question을 release할 수 없습니다.

Rigorous `DELETE`는 audit 성공이며 억지로 positive result를 만들지 않습니다.
