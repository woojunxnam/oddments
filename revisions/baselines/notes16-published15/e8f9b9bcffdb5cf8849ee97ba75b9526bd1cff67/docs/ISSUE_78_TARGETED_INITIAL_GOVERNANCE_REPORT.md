# Issue 78 Targeted-Initial Governance Report

## Source guard

- Source branch: `repair/pre-batch3-coverage-t2-r1`
- Required source HEAD: `e8b42047f2579f0b83822bc15dcc640c5e9ba236`
- The source branch was verified identical to the required HEAD before the policy branch was created and again immediately before the first repository mutation.

## Authorized targeted tranche

`TARGETED_INITIAL_BATCH` is limited by explicit validator governance metadata. The currently authorized tranche is:

- `tranche_id`: `PRE-BATCH3-COVERAGE-T2`
- `authorizing_issue`: `68`
- `represented_candidate_sha`: `b849159ef18d37618ca6badf886e465502436e1b`
- exact question-ID set: `MA-Q-0211` through `MA-Q-0226`

The authorization question-ID set must exactly equal the audit record question-ID set. The represented candidate SHA must be a 40-character lowercase Git SHA and must exactly match the governed value.

## Preserved safeguards

- Ordinary `INITIAL_BATCH` remains subject to its existing minimum of 30 questions.
- `REAUDIT` behavior is unchanged.
- A targeted initial audit must be independent and `FULLY_ADJUDICATED` and remains subject to the ordinary legal-authority validation rules.
- Initial-history presence may be satisfied by a valid ordinary `INITIAL_BATCH` or a valid governance-authorized `TARGETED_INITIAL_BATCH`.
- Current-hash LEGAL and REALISM release admission gates are unchanged.
- Failed fully adjudicated current-hash audits remain visible to the release validator and cannot be hidden by omitting them from selected release evidence.
- Historical initial evidence may remain historical after later semantic repair; it does not substitute for current-hash release evidence.

## Scope exclusions

This policy change does not add canonical T2 audit records, release any T2 question, alter T2 question content, alter release requirements, alter rules or drugs, alter blueprint or style-profile data, alter coverage, or begin Batch 3. `MA-Q-0028` remains quarantined/non-released.

Batch 3 remains BLOCKED.
