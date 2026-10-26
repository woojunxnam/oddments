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
