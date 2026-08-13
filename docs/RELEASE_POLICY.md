# Release Policy

## Lifecycle

```text
DRAFT
  |
  v
SOURCE_VERIFIED
  |
  v
AUTOMATED_QA_PASS
  |
  v
AUDIT_PENDING
  |
  v
AUDITED
  |
  v
ADJUDICATED
  |
  v
RELEASED
```

If law or official exam structure changes:

```text
RELEASED -> REVIEW_REQUIRED
```

## Release gates

A question may be `RELEASED` only when:

1. Every controlling rule is `CURRENT` and has a verified status, exact section, official URL, and verification date.
2. Every material drug is verified and has a concise authoritative indication.
3. An SBA has exactly one defensible answer.
4. A SATA has at least one answer unless an explicit, approved design says otherwise.
5. Every choice has a unique explanatory rationale.
6. No placeholder exists.
7. Duplicate-family review is resolved as `CLEAR`.
8. Difficulty is supported by `reasoning_steps`.
9. Difficulty `5` normally has at least three meaningful determinations.
10. No controlling authority is `DRAFT`, `SUPERSEDED`, `TEMPORARY`, or `UNCLEAR`.
11. An independent audit has passed.
12. Final adjudication is recorded.
13. Automated QA passes against the exact canonical record being released.

The validators enforce machine-verifiable gates. They do not auto-fix legal content or claim that QA replaces expert adjudication.

## Output policy

Only `RELEASED` questions enter website or future PDF release data. Development fixtures and `AUDIT_PENDING` questions may appear in local development builds only when the UI labels them clearly as not safe to memorize.

## Invalidation

Changing a rule record, authority, verification status, or drug record requires dependent questions to be reviewed. The safe default is exclusion from released output, never grandfathering.

