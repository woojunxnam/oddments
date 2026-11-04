# Online practice publication — 2026-10-26

The owner explicitly requested that the 1,024 additional questions be usable directly on the website rather than left behind a draft/download gate. This authorization supersedes the metadata-only delivery restriction in the historical `PRACTICE_EXPANSION_ADDITION.md` for this specific bank.

## Separate publication and review states

- `PUBLISHED_PRACTICE`: all 1,024 archived items are published as a working online practice edition at `/practice-expansion/`, without an acknowledgement checkbox or download requirement.
- `NOT_INDEPENDENTLY_REVIEWED`: accurate independent-review status remains visible in a non-blocking disclosure and explanations.
- Canonical question-bank `RELEASED` retains its existing independent audit requirements. No audit record, rule verification, adjudication, answer key, or canonical question flag is fabricated or overwritten.

The archival source remains immutable for provenance. Public delivery metadata is generated separately; public records are enabled for online practice, not falsely labeled as independently audited. Source-derived questions, choices, answers, Korean rationales, and source links are preserved without new legal conclusions. This is neither a recalled exam bank nor a readiness/pass predictor.

## Build and deployment

`python scripts/publish_practice.py --output public-site` copies `site/`, generates the interactive page and build manifest, and changes the two main-page entry labels in the output only. The Pages workflow publishes that built output rather than the source-only status page. This is a scoped deployment-generated artifact exception; canonical tracked question-bank artifacts still follow `docs/RELEASE_POLICY.md`.

The build pins the original question SHA-256 and checks the note snapshot. Unexpected source/template drift fails visibly. Runtime assets are embedded; answers/progress are not sent to a server. The public reader has its own localStorage namespace and can import earlier local-reader progress.

## Checks and limits

Focused structural tests check all 1,024 enabled records, unchanged substantive content, no fake audit, no draft access gate, isolated storage, deterministic rendering, and unchanged canonical data. The public HTTP browser suite exercises main navigation, scoring, explanation links, search, unique-family sets, timed review, persistence, backup/import, all 1,024 desktop/mobile renders, and blocked-storage fallback. Software QA does not constitute independent legal review. Physical mobile devices and official exam difficulty/scoring calibration remain untested.

## Additional casebank edition — 2026-10-26

The owner's follow-up request authorizes 1,000+ additional online practice exercises using the existing readable public edition. `2026-10-26.practice2` adds 1,152 items from `practice_expansion/2026-10-26-plus/` to the unchanged 1,024-item archive. All 2,176 can be answered online. A collection filter supports new-only, original-only, and mixed practice without changing the existing localStorage namespace.

The added bank comprises 128 decision models with nine substantive condition/action variants each (342 single-case SBA, 450 work-queue SBA, 360 five-choice SATA). Related decisions recur deliberately. The count is not a claim of 1,152 independent vignettes or principles. Public style examples inform structure; current official sources and the linked note snapshot support substance. Some sources were inherited rather than freshly read in full, and original source review dates are retained. Author review is not independent legal/realism adjudication.

The publisher pins both question-file hashes, rejects ID/source collisions, retains the old archive and substantive fields, and validates links into the immutable note snapshot. Generated publication metadata remains separate from the canonical audited release system. Selection uses at most one item from each model per set; it is neither adaptive nor psychometrically calibrated.

Research provenance, source boundaries, known repetition, exclusions and cue diagnostics are documented in the new package. Unresolved authority overlaps and inaccessible HIV/STI algorithms were not silently converted to definitive answers. Existing official sample items and publisher questions were not reproduced.
