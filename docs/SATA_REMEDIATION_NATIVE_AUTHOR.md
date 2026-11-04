# Native current-ID author review: exactly three SATA candidates

The next order is **actual G author review → actual F/C independent review → root
QA/publication**. The unchanged question objects MA-RW-0081/0082/0083 receive no
credit from metadata conversion, the earlier G drafts or E's earlier draft audit.
The source objects and their whole-record hashes do not change in this step.

The derived ledger initially has `current_id_author_review_required: true`,
`checked_at: null`, `author_review_increment: 0`. The original G draft date is kept
separately in `source_author_review_date`. Author planning can select this explicit
three-ID gap, and independent planning excludes it until formal author review is
consumed. The original FIRST cohort and original 52 integrated jobs remain intact.
The old static source list actually has **63 files**, all pinned without changes.

Root controller sequence (workers must not write queue/ledger/registry):

```sh
# Regenerate the authoritative inventory with the new code first.
python scripts/review_queue.py --stage author plan --size 3
python scripts/review_queue.py --stage author claim --worker /root/independent_case_g
```

The sole required actor is the actual content author G. E is the engineer; E does
not perform this legal review. The generated job records its three IDs and exact
current whole-record hashes, `required_author_actor_id`, and
`selection_policy: CURRENT_ID_AUTHOR_REVIEW_REQUIRED`. G is allowed at the author
stage; G and E remain excluded from the later independent job.

G reads the current compiled stem, every option/key and every Korean explanation,
and verifies each tested proposition against current official primary text. If a
wording/legal defect appears, report HOLD/SOURCE_BLOCKED; do not edit the question,
key, G draft, existing source objects or metadata to manufacture agreement.

G commits one report at
`reports/full-corpus-review/sata-remediation-current-id-author/g-review.json`
plus any new retained evidence under that directory's `evidence/` prefix. Existing
retained public G source bytes may be referenced with their actual original
retrieval dates. The report contract is:

- `schema_version: sata-remediation-current-id-author-review/1`, `stage: author`,
  exact `job_id`; `actor_provenance` has G's actual `actor_id`, `session_id` and
  `stable_instance`, matching the original G provenance in each candidate.
- `canonical_audit: false`, `canonical_release_credit: 0`,
  `independent_of_authors: false`, `independent_review_credit: 0`.
- Exactly three `records`, each with `question_id`, assigned `record_sha256`,
  actual `checked_at`, `disposition` (KEEP/HOLD/SOURCE_BLOCKED/NEEDS_REMEDIATION),
  `legal_review_status` (AUTHOR_SOURCE_CHECKED_NOT_INDEPENDENT, or
  AUTHOR_CURRENT_ID_SOURCE_BLOCKED), `blocker`, and
  `current_ID_stem_all_choices_key_all_Korean_explanations_read: true`.
- Each record's `reviewer_provenance` repeats the actual G actor/session/stable
  instance and `independent: false`; `author_expected_choice_ids` records the
  author's expected set. KEEP must agree with the stored key. Unknown source
  truth is `null`, with a null expected set and HOLD/SOURCE_BLOCKED.
- `choice_by_choice_findings` contains every actual choice ID, with exact
  `original_choice_text`, distinct Korean `finding_ko`, `exact_authority`,
  boolean `expected_true` (null only for an unresolved held option), and a
  nonempty `authorities` list.
- Each authority has official HTTPS `official_url`, `exact_section`, actual
  `law_checked_date`, explicit `version_or_effective_date_status`,
  `body_verified_current_primary`, `http_status`, `used_as_legal_proof`, retained
  repository `raw_path`/`raw_sha256`, and retained JSON
  `retrieval_metadata_path`/`retrieval_metadata_sha256`. Metadata's `official_url`,
  `http_status`, and `raw_sha256` must agree. HTTP failure or a wrong 200 body
  cannot support KEEP; held failure evidence must set `used_as_legal_proof:false`,
  a `failure_reason`, and an actual blocker. Unknown effective dates remain unknown.

The record must also pass existing `build_full_corpus_review.validate_review`.
This contract validates provenance/bindings; it is not automatic legal truth or
identity authentication. Root must dispatch the job to the actual G session.

After G commits, G returns an **uncommitted post-commit result envelope** with
`stage: author`, exact `job_id`, `question_hashes`, `worker_commit`, the same actual
`actor_provenance`, and the four zero/false credit declarations above. `results`
contains exactly the three IDs, common `evidence_path` and report raw
`evidence_sha256`, and a native disposition: AUTHOR_REVIEWED for a KEEP record,
otherwise the matching HOLD/SOURCE_BLOCKED/NEEDS_REMEDIATION. No self-referential
worker SHA is added to the committed report.

Root cherry-picks the evidence, uses the normal author `submit` and sequential
`integrate` commands, then commits the integrated queue and this explicit registry:

```json
{
  "schema_version": "sata-remediation-native-author-sources/1",
  "sources": [{
    "job_id": "<actual native author job53 ID>",
    "report_path": "reports/full-corpus-review/sata-remediation-current-id-author/g-review.json",
    "report_sha256": "<actual committed report raw SHA-256>"
  }]
}
```

Registry path:
`reports/full-corpus-review/sata-remediation-current-id-author-sources.json`.
Only this one explicit three-ID source is accepted. Until registry, report, source
bytes and integrated queue all match committed HEAD, the consumer gives no credit
or fails closed. It checks current hashes, required actor, lease binding and the
PLAN→CLAIM→SUBMIT→INTEGRATE event chain. Original 52 jobs/events and all 63 static
review source bytes are immutable. Runtime reads retained HEAD bytes and never
fetches or resolves historical worker commits; native integration retains its
existing fresh worker-commit check.

Regenerate the inventory only after that commit. The actual three author records
then get `current_id_author_review_required:false`, the formal date and exactly
one author review credit per record. Reapplying draft bindings keeps the validated
native review. No independent/canonical credit is created, including for held
source failures. Root can then plan `independent-legacy --size 3` with the existing
`--prioritize-remediation-and-default` option for another actual F/C session.
