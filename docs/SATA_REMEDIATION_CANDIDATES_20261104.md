# Three separately identified SATA replacement candidates

This is a lossless engineering adaptation of G's final drafts at
`7a50ba013a5dc271f62f3cd6ffaf39757cb53898`, with the prior independent **draft**
review at `1c540bd3ced12ccfc097486df57c0d71b3b86ef8` bound by exact report SHA.
E is the engineer for this change and receives no new author, legal, realism,
canonical, or release credit. E must not claim a fresh independent review of the
compiled public IDs after this engineering exposure.

The frozen allocation maps MA-EXP-0351/0367/0383 to MA-RW-0081/0082/0083. The
allocation scanned every tracked textual MA-RW reservation in the exact base
`34e38c7b3d2b87ca5b3d9528dff5eb5121c923e4`, including all authoring and drafts.
The six reserved but unpublished numbers through 0080 were retained. Existing
2,346 raw question objects, 74 representative objects and **81** representative
source objects are pinned in `reports/representative-rewrite/sata-remediation/allocation.json`.
The original main bank, keys, attempt IDs, bookmarks and history semantics stay
unchanged. A separately captured actual base publication build pins all 2,346
complete delivered objects, including delivery metadata.

`10_sata_remediation.json` is an authoring-format adapter, not a new legal review.
The final English stem, every choice/key, and every Korean core/choice explanation
and learning boundary are copied exactly. The last double newline supplies a
lossless scenario/lead-in split. Nine G sources use a new `rw7-remediation-*`
namespace; exact per-choice authorities, effective-date unknowns, original
retrieval timestamps and retained raw evidence hashes remain attached. Context
note links do not add inherited note sources to these option proofs.

Original HOLDs, safety HOLDs, replacement mappings and the 298 default IDs remain.
The new `archive_only_replacements` links are informational and are excluded from
default selection. The UI identifies these as separate candidates with current-ID
review pending. PUBLISHED_PRACTICE is delivery metadata, **not** canonical RELEASED.
The publication manifest here is a proposed local build input: neither integration,
publication, default promotion nor deployment was performed by this worker.
The original publication edition/date is retained so the 2,346 delivered objects
remain identical; the three source items carry the legitimate Nov 4 authoring
edition. Root owns any subsequent publication/version decision.

The inventory status `DRAFT_SOURCE_REVIEW_BOUND_NOT_CURRENT_ID_AUDIT` records the
original G source-review date for scheduling only. It gives no new author or
independent credit. A different actual session must review the final compiled IDs
through the main independent queue. These are non-additive remediation variants;
particularly 0367 overlaps existing Q0175/CASE0328 principles and confers no extra
legal-topic coverage certification.

Reproduce the candidate in the dedicated checkout:

```sh
python scripts/build_sata_remediation_candidates.py --check
python scripts/build_representative_rewrites.py --check
python -m pytest -q tests/test_sata_remediation_candidates.py tests/test_representative_rewrites.py
python scripts/publish_practice.py --output /tmp/sata-remediation-candidate-site
```

The allocation initialization command is one-time, explicit and immutable. Ordinary
compilation reads retained snapshots and does not depend on worker Git refs or
private filesystem paths. Root queue state, generated ledgers, deployment and CI
are not written by this worker. Root should regenerate its own inventory after
integration and complete final-ID review before any promotion decision.
