# Draft expansion repository addition — 2026-10-23

Adds the previously delivered 1,024-question package, as review sources only, under `practice_expansion/2026-10-23/`. The English questions, Korean rationales, exact content hashes and draft states are unchanged. Package README/handoff metadata is updated and the checksum manifest is refreshed. Historical reports are preserved with their limitations.

The main page adds a header link and entry card to a metadata-only status page at `practice-expansion/`. It links to GitHub sources and the local HTML download. It does not load candidates into the production quiz or publish an additional 1,024-item released payload. All existing data, audit records, notes, release policies and quiz scripts remain unchanged.

`tests/test_practice_expansion_integration.py` tests unchanged input notes, unmodified question bytes, draft flags, absence of drafts in the public payload, metadata-only status page, unadjudicated review queues, main navigation and ID isolation. The original 27 structural tests remain separate from any legal/realism audit.

Fresh independent legal/realism review and canonical mapping/adjudication are still required. Existing canonical registry/release policy is authoritative. No pass prediction or legal completeness is asserted.
