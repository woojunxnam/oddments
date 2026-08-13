# Canonical Audit Records

Store machine-readable independent audit records here. A released question must reference records in this directory; prose reports under `audits/claude/` and `audits/gpt/` do not independently satisfy release gates.

Each record must validate against `schemas/audit.schema.json`, exactly cover its declared `question_ids`, and preserve the exported `question_hashes`. `LEGAL_VERIFICATION` and `REALISM_REVIEW` are separate audit types.
