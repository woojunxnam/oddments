# Architecture

## Canonical boundaries

- `data/rules/`: canonical legal-rule records
- `data/drugs/`: canonical drug records와 rule-backed legal consequences
- `data/questions/`: independently authored questions
- `data/audits/`: release logic이 읽는 machine-readable audit records
- `data/source_manifests/`: research source provenance와 permission decision
- `data/source_signals/`: 허용된 Class B source에서 추상화한 signal만 저장
- `data/exam_style/`: public-source-derived style profile과 family matrix
- `data/study_guide/`: rule dependency를 exact version/hash로 pin하는 structured guide section과 navigation index
- `audits/claude/`, `audits/gpt/`: human-readable reports; 단독으로 release를 승인하지 않음
- `site/generated/`: deterministic derived output; canonical content가 아님

Study Guide의 모든 substantive legal point는 하나 이상의 canonical `rule_id`에 연결됩니다. Section은 직접 참조한 rule 집합과 exact dependency snapshot을 모두 보유하며, rule hash가 바뀌면 validator가 해당 section을 stale로 처리합니다. Controller-authored `AUDIT_PENDING` prose는 canonical registry와 development build에서는 검증할 수 있지만 public `study_guide.json`에는 포함되지 않습니다. Public guide prose는 별도 독립 검증을 거쳐 `VERIFIED`가 된 section만 생성됩니다.

## Dependency integrity

Rule, drug, blueprint, style profile은 `content_version`과 `content_hash`를 가집니다. `content_hash`는 법적·교육적 의미가 있는 allowlisted canonical fields만 SHA-256으로 계산합니다. JSON key 순서, 비의미적 list 순서, 문자열 공백 같은 formatting 차이는 normalize됩니다. Verification/check date와 저장 위치 같은 운영 metadata는 hash에 포함하지 않습니다.

Rule/drug의 semantic content를 변경할 때는 `content_version`을 올리고 `python scripts/update_content_hashes.py`로 hash와 transitive drug snapshots를 갱신해야 합니다. Validator는 저장된 hash와 재계산된 hash가 다르면 실패합니다. Foundation v1 fixture의 one-time migration은 `scripts/migrate_foundation_v2.py`에 보존됩니다.

Drug의 각 `legal_consequences` 항목은 `summary`와 `rule_ids`를 가집니다. `verified_rule_dependencies`는 그 rule 집합의 정확한 version/hash snapshot이어야 합니다. 따라서 rule 변경은 drug를, drug hash 변경은 dependent question을 fail-closed로 무효화합니다.

Final adjudication은 question이 직접 참조한 모든 rule/drug와 applicable blueprint/style profile의 exact version/hash snapshot을 `verified_dependencies`에 저장합니다. `RELEASED` 시 현재 dependency snapshot과 byte-for-byte 동일해야 합니다. 새로운 post-2027 blueprint/profile은 새 versioned ID로 추가하고 역사적 record를 덮어쓰지 않습니다.

## Audit integrity

Audit export hash는 stem, choices, answer, explanation, rule/drug references 등 question의 audit 대상 semantic fields를 고정합니다. Lifecycle, audit link, adjudication, realism score 같은 workflow metadata는 audit hash에서 제외합니다. Question content가 바뀌면 기존 audit hash가 일치하지 않아 release할 수 없습니다.

`INITIAL_BATCH`는 30-40 items이며 new-bank admission의 근거입니다. `REAUDIT`는 1-40 items로 수정된 일부 item을 다시 검토할 수 있습니다. 별도 governance 승인이 validator의 authorization table에 등록된 경우에만 `TARGETED_INITIAL_BATCH`(1-29 items)를 사용할 수 있습니다. Release item은 이 두 initial 경로 중 하나의 valid independent 이력이 필요하므로 one-item re-audit만으로 신규 bank admission을 우회할 수 없습니다. Historical initial audit는 보존하고 question의 `audits`에는 current release evidence를 연결합니다.

Release에는 `data/release_requirements.json`에 따라 서로 분리된 current-content audit가 필요합니다.

```text
INDEPENDENT INSTANCE LEGAL_VERIFICATION: FULLY_ADJUDICATED + KEEP + answer YES
INDEPENDENT INSTANCE REALISM_REVIEW:     FULLY_ADJUDICATED + KEEP + PASS + current profile hash
FINAL_ADJUDICATION:                      HUMAN/EDITOR KEEP + current dependency snapshots
```

Boolean/status summary만으로는 release할 수 없습니다. Question이 참조하는 모든 audit ID가 `data/audits/`의 실제 record로 resolve되어야 합니다.

2026-10-30 대조: `data/release_requirements.json`, `docs/AUDIT_WORKFLOW.md`, `docs/RELEASE_POLICY.md`와 실제 validator는 `AUDITOR_INSTANCE`, minimum passes 1, distinct auditor instances 1을 사용합니다. 같은 독립 세션이 legal과 realism을 별도 record로 제출할 수 있으며 model vendor 두 종류를 필수로 삼지 않습니다. `docs/SOURCE_USE_POLICY.md`의 흐름도와 `docs/QUESTION_AUTHORING_STANDARD.md`의 7번에는 과거 GPT/Claude 조합이 남아 있어 문서 불일치로 추적합니다. 이 작업은 보호된 정책 원본, 실행 설정, canonical audit와 release gate를 변경하지 않습니다.

공개 연습판의 작성자 선택지 검토와 0–5 편집 평가는 위 독립 release gate를 대체하지 않습니다. `reports/full-corpus-review/`는 ID별 원문 hash, 검토 범위, 오류·조건부 판단, 미검토 상태를 별도로 관리합니다. 구조 검사·노트 연결·family 수는 법규 검토 완료 수가 아닙니다.

## Integrated notes revisions

통합노트의 보호된 `notes/guide.json` 위에 `scripts/notes_revision.py`가 `revisions/notes/`의 명시적 순서와 parent hash를 검증하여 개정판을 합성합니다. 법적 설명을 바꿀 때는 새 revision의 정확한 unit 범위와 기존 body hash, source evidence, 연결 summary/card를 기록합니다. 기존 판본과 읽음·북마크 ID를 보존하고, 보호된 Markdown export는 해당 generated file 하나에만 허용된 hash-bound migration으로 갱신합니다. 원본 guide나 이전 overlay를 직접 덮어쓰지 않습니다.

노트→연습 연결은 실제 문항 `note_evidence`의 unit ID에서 생성합니다. 장 이름이나 비슷한 topic 문자열로 연결을 추정하지 않습니다. 각 절의 전체 보관 문항 수와 기본 대표·개정 문항 수를 따로 보여 주며 연결 수는 검토 완료 수가 아닙니다.

## Source and realism flow

허용되는 non-official practice source는 topic/trap/format의 추상 signal만 제공할 수 있습니다. Final question은 official law에서 독립적으로 작성합니다. `mpje_style_profile.json`은 public NABP format·competency·sample 자료에서 item types와 reasoning style을 모델링하며 protected wording을 저장하지 않습니다.

`question_family_matrix.json`은 planned zero-count family를 허용하고 candidate/released count를 별도로 검증합니다. Candidate count가 final cap을 넘는 것은 research 단계 warning이며, released count가 cap을 넘으면 hard failure입니다.

Realism truth는 question JSON에 복제하지 않습니다. Canonical `REALISM_REVIEW` audit가 current question hash와 exact style-profile snapshot을 고정하며, site output이 필요할 때 audit record에서 `realism_reviews`를 파생합니다.

## Release-date guard

Ordinary development validation은 historical work를 막지 않습니다. Release build만 explicit target exam date를 blueprint의 `applies_to_exams_before`, `must_reverify_after`, profile validity와 비교합니다. Default target은 실행일입니다. 2027-03-01 target에는 pre-2027 context를 사용할 수 없지만, explicit pre-transition target은 역사적 재현을 위해 지원됩니다.

## Generated artifacts

이 저장소는 tracked deterministic output 전략을 사용합니다. `scripts/generate_artifacts.py --write`가 세 artifact를 한 번에 재생성하며, `validate_all.py`는 stale content를 실패 처리하고 CI는 재생성 diff가 0인지 확인합니다. Hand edit는 허용되지 않습니다.

## Private boundary

`local_private/`, `private_sources/`, `licensed_sources/`, `*.private.pdf`, `*.licensed.pdf`는 gitignored이며 CI test는 이런 경로가 tracked되지 않았음을 확인합니다. 이 boundary는 Class C 자료의 합법성을 추정하지 않으며 Class D 자료의 저장·AI 처리 경로를 제공하지 않습니다.
