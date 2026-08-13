# Massachusetts MPJE Study System

이 저장소는 Massachusetts MPJE 학습·감사 시스템의 canonical source of truth입니다. 웹사이트와 향후 PDF는 `data/`에서 생성되는 output이며 독립적인 권위가 아닙니다.

## Content status

현재 Phase 2 candidate expansion에는 다음 항목이 있습니다.

- semantic version/hash가 있는 rule 80개(verified 75개, `HOLD` 5개)와 drug 60개
- version/hash가 고정된 pre-2027 blueprint와 style profile
- `AUDIT_PENDING`인 development candidate 90개(foundation 10개 + Phase 2 신규 80개)
- 실제 candidate 90개와 planned 40개를 합한 question family 130개
- fail-closed schema·validator·audit·release gate
- 공개 NABP 자료만 사용한 `MPJE-MA-PRE2027` style profile
- question-family matrix와 source-governance boundary
- deterministic static quiz-site skeleton

현재 `RELEASED` question은 0개입니다. 모든 candidate는 독립적인 legal/realism audit와 최종 adjudication 전이므로 암기 안전성이 확인된 자료가 아닙니다. `HOLD` rule은 question 근거로 사용할 수 없습니다.

## Canonical pipeline

```text
PERMITTED PUBLIC SOURCE
        -> ABSTRACT SIGNAL (optional; no source question text)
        -> VERIFIED OFFICIAL RULE
        -> FRESH SCENARIO + FRESH DISTRACTORS
        -> AUTOMATED QA
        -> GPT LEGAL AUDIT
        -> CLAUDE LEGAL AUDIT
        -> INDEPENDENT REALISM REVIEW
        -> FINAL HUMAN/EDITOR KEEP ADJUDICATION
        -> RELEASED OUTPUT
```

Commercial/recalled question을 paraphrase해 public question으로 만드는 경로는 금지됩니다. 자세한 기준은 [Source Use Policy](docs/SOURCE_USE_POLICY.md)를 참조하십시오.

## Local validation

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_all.py
python -m pytest -q
```

tracked generated artifact를 갱신하려면 다음 명령을 사용합니다.

```bash
python scripts/generate_artifacts.py --write
```

CI는 재생성 후 `git diff --exit-code`를 실행하므로 `duplicate_report.json`, `answer_distribution_report.json`, `site/generated/questions.json`의 drift를 허용하지 않습니다.

development fixture site data는 명시적으로만 생성합니다.

```bash
python scripts/build_site_data.py --include-fixtures
python -m http.server 8000 --directory site
```

`--include-fixtures`를 생략한 release build에는 모든 release gate를 통과한 `RELEASED` question만 포함됩니다. 빈 release payload는 `NO_RELEASED_QUESTIONS`이며 안전하다는 뜻으로 표시되지 않습니다.

Release build는 기본적으로 실행일을 target exam date로 사용합니다. Historical pre-2027 output을 의도적으로 검증할 때만 `--target-exam-date YYYY-MM-DD`를 지정할 수 있습니다. 2027-03-01 이후 target에 pre-2027 blueprint/profile을 사용하면 `BLUEPRINT_REVIEW_REQUIRED`로 실패합니다.

관련 문서: [Architecture](docs/ARCHITECTURE.md), [Question Authoring Standard](docs/QUESTION_AUTHORING_STANDARD.md), [Audit Workflow](docs/AUDIT_WORKFLOW.md), [Release Policy](docs/RELEASE_POLICY.md).
