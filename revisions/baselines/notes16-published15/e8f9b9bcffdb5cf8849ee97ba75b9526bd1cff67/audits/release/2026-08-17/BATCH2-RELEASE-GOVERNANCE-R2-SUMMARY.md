# Batch 2 Round-2 Release Governance Summary

Date: 2026-08-17

## Exact provenance

- Repaired Round-2 source candidate: `f85b650c1b3344184186229ec45bf1d233a4e971`
- Issue #44 fresh re-audit head: `561fcdd97bacd4f694b1f1a827713b1573467755`
- Release adjudication commit: `255f0312620f05ba10f9a4a515ba79fcdbd3a69a`
- Clean governance head after removing the temporary write workflow: see the branch/PR exact head.

## Release result

- Batch 2 scope: `MA-Q-0131` through `MA-Q-0210` (80 questions)
- Released: **80 / 80**
- Unreleased: **0**
- Blocking reasons: **none**

Batch 2 released counts by NABP area:

- Area 1: 12
- Area 2: 15
- Area 3: 30
- Area 4: 23

Total release-usable bank after Batch 2 governance:

- Area 1: 17
- Area 2: 22
- Area 3: 55
- Area 4: 26
- Total: 120

This total of 120 does **not** mean a blueprint-faithful 120-question mock can be assembled. The required 26 / 40 / 29 / 25 area allocation still has deficits of 9 in Area 1 and 18 in Area 2. Issue #40 remains mandatory before Batch 3.

## Audit evidence handling

- Initial independent Batch 2 history from `GPT-FRESH-EXP2-A` is preserved in canonical `data/audits`.
- Issue #39 `GPT-FRESH-EXP2-B` legal re-audit is preserved and used where current.
- The mixed Issue #39 realism artifact is retained as historical raw evidence. It is intentionally not canonicalized into `data/audits` because it contains pre-Round-2 realism failures whose semantic-distinctness context was changed by the Round-2 repairs.
- For Q0145, Q0146, Q0166, Q0171, and Q0196, the unaffected Issue #39 realism PASS results were independently required as an additional support gate by the release adjudicator.
- The Round-2 Impact9 uses the fresh `GPT-FRESH-EXP2-C` Issue #44 legal + realism audits as current release evidence.

## QA

The release workflow completed all pre-commit checks successfully:

- release eligibility: 80 released / 0 blocked
- `python scripts/validate_all.py`: 0 errors; one existing Q0190 answer-length warning
- `python -m pytest -q`: 80 passed
- deterministic artifacts regenerated
- generated-artifact freshness checked after the release commit
- governance write boundary passed

The final clean governance head must also pass the repository's normal QA workflow and the Draft PR merge-context QA before the release boundary is treated as frozen.
