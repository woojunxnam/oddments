# Optional remediation and current-default review priority

The existing queue order is unchanged unless `plan` receives
`--prioritize-remediation-and-default` in the `independent-legacy` stage. The
existing author FIRST cohort, uncredited-ledger gate, incomplete-wave refusal,
lease recovery, idempotent submit and sequential evidence-bound integration keep
their existing behavior.

With the option, eligible ledger IDs are ordered deterministically:

1. The three frozen, source-bound remediation IDs.
2. Other current default IDs from the publication manifest's hash-bound selection.
3. The remaining IDs in lexical order.

Eligibility still requires an existing source-review date and no independent
legacy assessment, and excludes every ID assigned in an earlier job. Missing or
stale source/ledger/default bindings fail. Jobs already assigned are not changed.
The selected policy and source SHA bindings are recorded in each new job and its
PLAN event. A plan made while any prior job is incomplete returns no new jobs.

New candidates explicitly identify G as content author and E as engineer. Their
actual actor IDs pass unchanged through source, ledger and job; claim rejects a
known author/editor for that job. Existing unknown actor identities are not
inferred. Claim's worker string must be the actual actor ID, as required by the
independent workflow; this guard is not an identity authentication service.
Original G draft dates add zero author-review credit. Pending candidates first
require G's native current-ID author job and its HEAD-bound registered evidence;
see [the author-review contract](SATA_REMEDIATION_NATIVE_AUTHOR.md).

After root integrates, completes G's native author job and regenerates its
authoritative inventory, it may plan these three for another actual session,
then later plan the next waves:

```sh
python scripts/review_queue.py --stage independent-legacy plan --size 3 --prioritize-remediation-and-default
# Root completes, registers and integrates this wave before planning again.
python scripts/review_queue.py --stage independent-legacy plan --batches 4 --size 40 --prioritize-remediation-and-default
```

These are controller examples only. The engineering worker did not execute them
against shared queue state and did not assign itself or any other actor a job.
