# Canonical Audit Records

Store machine-readable independent audit records here. A released question must reference records in this directory; prose reports under `audits/claude/` and `audits/gpt/` do not independently satisfy release gates.

Each record must validate against `schemas/audit.schema.json`, exactly cover its declared `question_ids`, and preserve the exported `question_hashes`. `INITIAL_BATCH` contains 30-40 items; `REAUDIT` contains 1-40. `LEGAL_VERIFICATION` and `REALISM_REVIEW` are separate audit types. Realism records bind the exact style-profile version/hash; legal results store one or more structured official authorities.
