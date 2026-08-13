# Massachusetts MPJE Study System

This repository is the canonical source of truth for an original Massachusetts MPJE study and audit system.

## Goals

- Maintain current Massachusetts and federal pharmacy-law rules.
- Keep exact source sections and verification dates.
- Maintain generic, brand, indication, and legal-status drug data.
- Generate original questions from verified rules.
- Detect duplicates, ambiguity, placeholders, and answer leakage automatically.
- Support Claude and GPT independent batch audits.
- Generate both a GitHub Pages quiz website and PDF from identical released data.

The website and PDF are outputs, not source-of-truth documents. Structured repository data is the canonical source.

## Public repository content policy

This repository is public. Do not store:

- Pre-MPJE questions;
- recalled MPJE questions;
- leaked questions;
- NDA-protected material;
- paid or commercial question-bank text.

Only original, source-first study content may enter the canonical data pipeline.

## Foundation status

This phase contains the canonical schemas, fail-closed QA tools, a small set of verified rule and drug fixtures, ten original `AUDIT_PENDING` development questions, and a static quiz-site skeleton. The sample questions are not declared safe to memorize.

## Local validation

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_all.py
python -m pytest -q
```

Build the local development fixture data explicitly:

```bash
python scripts/build_site_data.py --include-fixtures
python -m http.server 8000 --directory site
```

Omit `--include-fixtures` for a release build. Only fully `RELEASED` and currently eligible questions may enter release output; any invalidated rule or drug causes the build to fail closed.

See [Architecture](docs/ARCHITECTURE.md), [Question Authoring Standard](docs/QUESTION_AUTHORING_STANDARD.md), [Audit Workflow](docs/AUDIT_WORKFLOW.md), and [Release Policy](docs/RELEASE_POLICY.md).
