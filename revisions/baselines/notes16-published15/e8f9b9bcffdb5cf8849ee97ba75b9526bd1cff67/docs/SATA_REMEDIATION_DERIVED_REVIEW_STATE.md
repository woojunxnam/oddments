# Current-ID derived review state

For MA-RW-0081/0082/0083, the inventory keeps the original
`source_author_review_binding` unchanged. Its `PENDING` fields describe the frozen
draft/engineering source, rather than the current review stage.

After the native current-ID author review is source-bound, the committed
independent-source consumer can provide the exact report path, raw SHA, job,
actor/session, current question hash and individual review-record hash. The
inventory checks those bindings against the assessment it has just applied and
adds:

- `current_id_independent_review_status`: `SOURCE_BOUND_PASS`,
  `SOURCE_BOUND_NOT_PASSED` or `SOURCE_BOUND_INCOMPLETE`.
- `current_id_independent_review_source`: that validated source metadata.
- `next_action`: root QA/publication/default-selection review for a passing
  assessment without another hold, or the actual unresolved blocker otherwise.

Missing source/native-author bindings do not advance this state. Stale hashes or
inconsistent provenance fail the inventory build. Other IDs retain the existing
behavior. These derived fields add no review counts or credits and do not change
candidate objects, original holds, archive/default membership or canonical release.
