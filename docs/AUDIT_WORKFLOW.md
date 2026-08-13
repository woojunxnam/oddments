# Audit Workflow

## Independence and batch size

Each Claude or GPT audit covers 30-40 questions. Auditors read canonical questions and official sources but do not modify canonical question files. They write a separate audit artifact under:

- `audits/claude/YYYY-MM-DD/`
- `audits/gpt/YYYY-MM-DD/`

Human/editor adjudication is stored independently under `audits/adjudication/`.

## Required result fields

Each result contains:

- `Question_ID`
- `Verdict`
- `Severity`
- `Existing_Answer_Correct`
- `Authority`
- `Exact_Section`
- `Official_URL`
- `Law_Checked_Date`
- `Problem`
- `Proposed_Answer`
- `Proposed_Rewrite`
- `Proposed_Explanation`

The JSON contract is `schemas/audit.schema.json`.

## Audit status

- `FULLY_ADJUDICATED`: the item received legal, drug, answer, ambiguity, explanation, and source review.
- `STRUCTURAL_TRIAGE_ONLY`: only structural risk was assessed.

Never interpret `STRUCTURAL_TRIAGE_ONLY` as legal validation. Triage cannot satisfy the independent-audit release gate.

## Procedure

1. Export a stable batch with `scripts/export_audit_batch.py`.
2. Freeze the source question IDs and hashes for that audit.
3. Audit against official current sources and record the check date.
4. Store the independent output without editing canonical data.
5. A human/editor resolves conflicts and records a final decision.
6. Apply approved canonical edits in a separate commit.
7. Re-run all automated QA and re-audit any materially changed item.

## Verdicts and severity

Verdicts are `KEEP`, `MINOR_EDIT`, `MAJOR_REWRITE`, or `DELETE`. Severity is `Low`, `Medium`, `High`, or `Critical`. A rigorous deletion is a successful audit outcome.

