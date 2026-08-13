# Architecture

## Canonical boundaries

- `data/rules/`: canonical legal-rule records
- `data/drugs/`: canonical drug records와 rule-backed legal consequences
- `data/questions/`: independently authored questions
- `data/audits/`: release logic이 읽는 machine-readable audit records
- `data/source_manifests/`: research source provenance와 permission decision
- `data/source_signals/`: 허용된 Class B source에서 추상화한 signal만 저장
- `data/exam_style/`: public-source-derived style profile과 family matrix
- `audits/claude/`, `audits/gpt/`: human-readable reports; 단독으로 release를 승인하지 않음
- `site/generated/`: deterministic derived output; canonical content가 아님

## Dependency integrity

Rule과 drug는 `content_version`과 `content_hash`를 가집니다. `content_hash`는 법적·교육적 의미가 있는 allowlisted canonical fields만 SHA-256으로 계산합니다. JSON key 순서, 비의미적 list 순서, 문자열 공백 같은 formatting 차이는 normalize됩니다. `last_verified`, `verification_notes`, 저장 위치 같은 운영 metadata는 hash에 포함하지 않습니다.

Rule/drug의 semantic content를 변경할 때는 `content_version`을 올리고 `python scripts/update_content_hashes.py`로 hash와 transitive drug snapshots를 갱신해야 합니다. Validator는 저장된 hash와 재계산된 hash가 다르면 실패합니다. Foundation v1 fixture의 one-time migration은 `scripts/migrate_foundation_v2.py`에 보존됩니다.

Drug의 각 `legal_consequences` 항목은 `summary`와 `rule_ids`를 가집니다. `verified_rule_dependencies`는 그 rule 집합의 정확한 version/hash snapshot이어야 합니다. 따라서 rule 변경은 drug를, drug hash 변경은 dependent question을 fail-closed로 무효화합니다.

Final adjudication은 question이 직접 참조한 모든 rule과 drug의 exact version/hash snapshot을 `verified_dependencies`에 저장합니다. `RELEASED` 시 현재 dependency snapshot과 byte-for-byte 동일해야 합니다.

## Audit integrity

Audit export hash는 stem, choices, answer, explanation, rule/drug references 등 question의 audit 대상 semantic fields를 고정합니다. Lifecycle, audit link, adjudication, realism score 같은 workflow metadata는 audit hash에서 제외합니다. Question content가 바뀌면 기존 audit hash가 일치하지 않아 release할 수 없습니다.

Release에는 서로 분리된 현재-content audit가 필요합니다.

```text
LEGAL_VERIFICATION: FULLY_ADJUDICATED + KEEP + answer YES
REALISM_REVIEW:     FULLY_ADJUDICATED + KEEP + realism PASS
FINAL_ADJUDICATION: KEEP + current dependency snapshots
```

Boolean/status summary만으로는 release할 수 없습니다. Question이 참조하는 모든 audit ID가 `data/audits/`의 실제 record로 resolve되어야 합니다.

## Source and realism flow

허용되는 non-official practice source는 topic/trap/format의 추상 signal만 제공할 수 있습니다. Final question은 official law에서 독립적으로 작성합니다. `mpje_style_profile.json`은 public NABP format·competency·sample 자료에서 item types와 reasoning style을 모델링하며 protected wording을 저장하지 않습니다.

`question_family_matrix.json`은 서로 다른 legal reasoning family의 count와 cap을 검증해 같은 아이디어의 drug-name 변형 증식을 막습니다. `RELEASED` question은 현재 profile을 사용한 structured realism assessment가 있어야 합니다.

## Generated artifacts

이 저장소는 tracked deterministic output 전략을 사용합니다. `scripts/generate_artifacts.py --write`가 세 artifact를 한 번에 재생성하며, `validate_all.py`는 stale content를 실패 처리하고 CI는 재생성 diff가 0인지 확인합니다. Hand edit는 허용되지 않습니다.

## Private boundary

`local_private/`, `private_sources/`, `licensed_sources/`, `*.private.pdf`, `*.licensed.pdf`는 gitignored이며 CI test는 이런 경로가 tracked되지 않았음을 확인합니다. 이 boundary는 Class C 자료의 합법성을 추정하지 않으며 Class D 자료의 저장·AI 처리 경로를 제공하지 않습니다.
