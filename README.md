# Massachusetts MPJE Study System

이 저장소는 Massachusetts MPJE 학습·감사 시스템의 canonical source of truth입니다. 웹사이트와 향후 PDF는 `data/`에서 생성되는 output이며 독립적인 권위가 아닙니다.

## Content status

아래 수치는 현재 canonical tree에서 직접 계산한 실측값입니다.

- semantic version/hash가 있는 rule 128개(verified 123개, `HOLD` 5개)와 drug 66개(전부 verified)
- version/hash가 고정된 pre-2027 blueprint와 `MPJE-MA-PRE2027` style profile
- canonical question 226개: `RELEASED` 165개, `AUDIT_PENDING` candidate 61개
- `RELEASED` question의 Area 분포: Area 1 = 26, Area 2 = 40, Area 3 = 59, Area 4 = 40
- question family matrix 296개(실제 candidate가 있는 family 226개 + planned family 70개)
- public preview allowlist 196개
- fail-closed schema·validator·audit·release gate
- question-family matrix와 source-governance boundary
- deterministic static quiz-site skeleton

`RELEASED` question은 current-hash independent legal `KEEP`/answer `YES`와 full-bank realism `KEEP`/`PASS` evidence, 그리고 final `KEEP` adjudication을 통과한 항목입니다. 나머지 61개 candidate는 아직 audit/adjudication 전이므로 암기 안전성이 확인된 자료가 아닙니다. `HOLD` rule은 question 근거로 사용할 수 없습니다.

`MA-Q-0028`은 current-hash realism distinctness failure 이후 quarantine 상태이며 release되지도 preview되지도 않습니다.

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
