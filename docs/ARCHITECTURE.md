# Architecture

## Canonical pipeline

```text
OFFICIAL SOURCES
        |
        v
VERIFIED RULE REGISTRY
        |
        v
DRUG REGISTRY
        |
        v
ORIGINAL QUESTIONS
        |
        v
AUTOMATED QA
        |
        v
INDEPENDENT LLM AUDITS
        |
        v
HUMAN / EDITOR ADJUDICATION
        |
        v
RELEASED QUESTIONS
       / \
      v   v
QUIZ SITE  PDF
```

The structured JSON records under `data/` are the source of truth. The website, generated site data, and future PDF are deterministic release outputs. They must never be edited as canonical content.

## Repository boundaries

- `data/rules/`: one canonical legal-rule record per JSON file.
- `data/drugs/`: one verified or explicitly held drug record per JSON file.
- `data/questions/`: original question records only.
- `data/audit_status/`: machine-readable audit/adjudication state when introduced.
- `schemas/`: JSON Schema contracts.
- `scripts/`: deterministic validation, analysis, audit export, and site-data build tools.
- `audits/`: immutable independent reports and separate adjudication records.
- `site/generated/`: derived data. Regenerate; do not hand-edit.

## Referential integrity

Questions reference `rule_ids` and optional material `drug_ids`. Validators load registries first, reject unknown IDs, and enforce release eligibility across references. A released question cannot outlive the verification of a controlling rule or material drug.

## Law-change invalidation

When a rule changes, mark the rule `HOLD`, `DRAFT`, `SUPERSEDED`, `TEMPORARY`, or `UNCLEAR` as appropriate. Every referencing question is immediately excluded from released output. Its lifecycle must move to `REVIEW_REQUIRED` before editing the question or regenerating outputs.

## Determinism

Validation and duplicate detection are local and deterministic. Site choice shuffling uses a seeded pure function and preserves the correct-answer mapping. Ordered-response steps are never shuffled.

## Trust boundary

Old PDFs and audits are evidence of failure modes, not canonical legal data. No recalled, leaked, NDA-protected, Pre-MPJE, paid, or commercial question text may enter this repository.

