# Source Use Policy

이 정책은 exam realism을 높이면서 confidential/protected material이 canonical question pipeline에 들어오는 것을 막습니다. `schemas/source_manifest.schema.json`은 provenance와 permissions를 명시적으로 기록하며 unknown permission은 `HOLD`와 false permissions로 처리합니다.

## Class A — `PUBLIC_OFFICIAL`

예: Massachusetts statutes, `247 CMR`, `105 CMR`, Board/DCP policy, eCFR, DEA, FDA/DailyMed, NABP public sample items, competency statements, public format information.

Public repository, source registry, rule verification, authoring research, audit, website/PDF output에 사용할 수 있습니다. 다만 NABP format/competency/sample source는 pharmacy-law authority가 아니며 final legal conclusion은 current official law로 독립 검증해야 합니다. Public sample wording도 복제하거나 lightly paraphrase하지 않습니다.

## Class B — `PUBLIC_NON_OFFICIAL`

예: public practice site, public study guide, public discussion of topic families.

허용 범위는 topic discovery, common-confusion discovery, style comparison, coverage-gap research입니다. Legal authority로 사용할 수 없고 source question text나 close paraphrase를 canonical bank에 저장할 수 없습니다.

Permission review가 `VERIFIED`이고 AI/public abstract use가 허용된 경우에만 `data/source_signals/`에 다음 종류의 signal을 저장할 수 있습니다.

```json
{
  "signal_id": "SIGNAL-EXAMPLE",
  "source_id": "SOURCE-EXAMPLE",
  "source_class": "PUBLIC_NON_OFFICIAL",
  "topic": "CII partial fill",
  "observed_trap": "72-hour vs 30-day confusion",
  "format_signal": "multi-rule scenario",
  "used_as_legal_authority": false,
  "contains_question_text": false,
  "notes": ""
}
```

## Class C — `LICENSED_PRIVATE`

Personally purchased bank, licensed study PDF, subscription content는 public repository에 절대 commit하지 않습니다. `local_private/` architecture는 보관 또는 처리 권한을 부여하지 않습니다. License가 intended retention, AI processing, transformation, derived output, publication을 각각 허용하는지 explicit source-use decision이 있어야 합니다.

Unknown permission은 자동으로 false/`HOLD`입니다. 이 foundation은 commercial material을 ingest하거나 transform하는 workflow를 제공하지 않습니다.

## Class D — `CONFIDENTIAL_PROHIBITED`

Recalled actual MPJE questions, Pre-MPJE question text, leaked questions, NDA-protected items, exam dumps, screenshots/transcriptions는 모든 pipeline input에서 금지됩니다.

다음을 하지 않습니다.

- commit, local ingestion, AI processing, transformation, paraphrase, regeneration
- embedding 생성
- derived public question 생성
- Class D용 local-private workflow 생성

NABP는 Pre-MPJE content에 AI를 사용하는 것을 금지한다고 공개적으로 명시합니다. 이 repository는 Pre-MPJE content를 열거나 분석하지 않습니다.

## Permitted transformation model

```text
PERMISSIBLE SOURCE
  -> ABSTRACT TOPIC/STYLE SIGNAL
  -> INDEPENDENTLY VERIFIED OFFICIAL RULE
  -> FRESH SCENARIO DESIGN
  -> FRESH DISTRACTOR DESIGN
  -> LEGAL_VERIFICATION
  -> REALISM_REVIEW
  -> RELEASE
```

다음 모델은 금지됩니다.

```text
COMMERCIAL OR RECALLED QUESTION -> PARAPHRASE -> PUBLIC QUESTION
```

## Manifest decisions

모든 non-canonical research source는 `source_id`, class, publisher, URL, access type, authority level, permission status, 네 permission booleans, notes, review date를 가집니다. Boolean은 추정하지 않습니다. Schema는 `HOLD`/`PROHIBITED`에서 모두 false를 강제하고, `CONFIDENTIAL_PROHIBITED`에 대한 모든 사용을 차단합니다.
