# Independent guarded-admission engineering review

**Not ready for admission.** Reviewed11 files at exact uncommitted hashes anchored to `ea19d9881ec5b6a476f7dfc113cd1a4bc18c92da`. The new targeted20 tests passed in1.10 seconds. The production registry is empty and status remains NO_ENROLLED_ADMISSION.

## Findings

**R1 (P1) — Registered history is not restricted to the exact declared Git delta** — scripts/canonical_admission.py:276

The validator checks protected/data/code/evidence bytes and base→content→HEAD ancestry, but never compares the complete Git tree deltas against an allowlist. site/app.js is outside all compared scope maps. It can differ in content_commit, and can change again after content_commit while the registry/enrollment/data/code bindings remain unchanged. Capturing the resulting HEAD in the token does not establish that its undeclared UI delta was reviewed.

Use a reviewed base that already contains runtime infrastructure. Require base→content to contain exactly approved additions/known changes/public evidence; require content→enrollment HEAD to contain only exact manifest/note-context/enrollment/registry changes. Reject all extra modified/added/deleted/mode-changed paths, including nonprotected UI. Record any separately allowed evidence explicitly.

Probe boundary: Actual synthetic Git trees and current scope/ancestry helpers were exercised. No complete production registration or successful30–40 admission was synthesized or claimed.

**R2 (P2) — A validated handle does not detect newly added unlisted protected files** — scripts/canonical_admission.py:193

require_context rehashes only existing current_seals entries. After a new data/questions file is added, unchanged HEAD/code/known-file seals still pass, and verify_protected returns the old1781 result. The mint-time inventory exactness is not rechecked at consumption.

Recompute the exact protected/source-bound/note inventory using the same scope as minting, compare it with the sealed inventory and reject new/missing/symlink paths before adapters or writes. Keep all content seals and HEAD/code checks.

Probe boundary: The fixture explicitly inserts a synthetic internal token solely to model an already validated state; no actual native success, registry enrollment or1781 execution is represented.

**R3 (P2) — Coverage output path can escape the repository through admission_id** — scripts/canonical_admission.py:324

The only coverage_path check is string concatenation with an unrestricted admission_id. ../../../outside-reviewed-root passes the actual predicate, and artifact_payloads constructs an output outside context.root. The relative_to check is lexical and does not reject the resulting parent components.

Constrain admission IDs to an explicit safe identifier grammar. Validate coverage_path with safe_path and require its resolved parent to be exactly the intended reports/canonical-successor namespace before any producer/output write.

Probe boundary: The exact AST predicate was evaluated and the path resolved. No artifact was generated or written.

**R4 (P3) — Boolean schema versions satisfy the integer-version predicates** — scripts/canonical_admission.py:212

Enrollment, manifest and notes context use schema_version==1, so JSON true is accepted by all three actual version predicates.

Require type(schema_version) is int and schema_version==1 for each document, with a negative boolean fixture.

Probe boundary: Only the actual format predicates were evaluated. No full registration was bypassed.

## Scope and preservation

The registered branch has real native-validation/producer/token machinery and rejects caller PASS objects. It is not an always-false stub, but no successful real30–40 admission has been verified. Full repository-delta and stale-inventory protection must be completed before enabling it. CI routing and historical fixed-count integration also remain unfinished.

Original439/397 and four guard/producer sources are preserved. This checkout contains the older16-hold overlay; the independent c7d source has19, and the new registry floor matches all19 exact hashes. The actual monotone16→19 check passed. This distinction is not a claim that the checkout UI was changed to19.

No source edits, whole native validator, full pytest, original1781 replay, generation, commit, push, admission, audit or release action was performed. The engineer-reported173.89-second base-native run was not repeated or credited as this reviewer’s execution. Existing sealed review/private/verifier artifacts were not edited.

## Exact reviewed hashes

- `scripts/canonical_admission.py`: `40b76782fc139fc344df16371dc11dc7e84280114bd318053d91af51dac92fa0`
- `scripts/canonical_admission_registry.py`: `44ccb9049d76b5e0b5e9a4db2f5a2920d8f10e3a5bf6de439bc699874836e5c0`
- `scripts/canonical_native_view.py`: `37930d45b1183ba7d2f8bc6891ff557c0efd8bc7a3883cf9b3d81616087a897c`
- `scripts/guarded_canonical_admission.py`: `945c7a87c119358b3544f8809ddff2a71c46ff4ad53e1b71750634e0ddd37fbc`
- `scripts/preflight_external_canonical.py`: `40f8c09d955ee9c8eb013140868b5aba5ac3a1773f62ea8a3b94e7f6635f10f7`
- `scripts/prepare_canonical_base_proof.py`: `ec21ff441a7e7fc780c7425b1d49bea221410516c0991417ecd1ca35d18533ca`
- `scripts/qa_common.py`: `999d9b30fab2dd7721ac22165ac993f32cc9b16460766b5b1cb17c0541caccb9`
- `scripts/validate_study_guide.py`: `ce213c2cb9a114a6ce61fc3f073399abb69005fe36eb23468964fc8da161674f`
- `scripts/build_study_guide_data.py`: `c340ca22772699b338a611446a15f601e1a79f6656f15d2d0a92a2dd3a093e46`
- `tests/test_canonical_registered_context.py`: `f07953ad20f24e6ba5baf142fe177346eb20fb6366cb2b0a5efe3c89bb51d80a`
- `docs/CANONICAL_GUARDED_ADMISSION.md`: `2fc665ea35e8fc3f6c5cdf48f08747103b992fc99b6b052753de7238c2928bf0`
