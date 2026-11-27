# Form H Batch 4 — authoring and structural review
Date: 2026-11-27
Status: COMPLETE AUTHOR DRAFT — NOT PUBLIC. This is not an independent pharmacist/legal review or NABP validation.

## Scope
- H091–H120: 30 items, five options each, 150 option rationales.
- Entire H: H001–H120, 120 items and 600 option rationales.
- Pre-March 1, 2027 MPJE competency blueprint; all 22 assigned competencies have their planned counts.
- Area distribution: 26 / 40 / 29 / 25; batch 4: 6 / 10 / 7 / 7.
- Item types: 72 SBA / 48 SATA. Cognitive tiers: 36 direct / 60 scenario / 24 integrated.
- This authoring work does not modify published A–G items or exam histories.

## Source-text review
Reviewed the applicable Massachusetts statutes/regulations, federal controlled-substance regulations, and Board policy texts. See each item for pinpoint citations, source URLs, exceptions, and counterfactuals. Key sources include:
- [247 CMR 9](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download), particularly 9.01, 9.08, 9.16–9.19; cross-checks against the Cornell LII versions.
- [247 CMR 4.04(5)](https://www.law.cornell.edu/regulations/massachusetts/247-CMR-4-04).
- [247 CMR 6.13(7)](https://www.law.cornell.edu/regulations/massachusetts/247-CMR-6-13).
- [21 CFR 1306.07(c)](https://www.law.cornell.edu/cfr/text/21/1306.07).
- [Massachusetts Board Policy 2026-03](https://www.mass.gov/doc/2026-03-action-level-environmental-monitoring-results/download).
- [Massachusetts Board Policy 2018-01](https://www.mass.gov/doc/2018-01-permitted-prescription-changes-and-additions-pdf/download).
Some government PDF image retrieval was restricted and source text or current codified copies were used instead. Source URL syntax checks are not universal HTTP availability checks. No human expert certification is claimed.

## Revision review
Nine cases replaced with different legal decisions after review of earlier questions; one case clarified to avoid ambiguity in the permitted action. The audit JSON records identifiers and nearest matches. Repeated high-yield legal domains remain intentional. No exact normalized stem/ID collisions between the new H items and the earlier banks were found; this does not establish complete semantic independence.

## Automated checks
Read and parsed all four H JSON batches and 840 earlier items. F was compared at pinned unmerged commit 4efe3a4fee04dd1a151e0d026e9f631514c870a5 (PR #297); A–E and G comparison baseline 41ce51963809ec6ae8151fa737ed9c41970b6f55. Recomputed nearest-neighbor screening against 930 prior items for batch 4. Verified sequential H identifiers, five options, key/rationale polarity, source-field structure, critical-error flags referring only to incorrect options, area/competency quotas, item types and cognitive tiers. Zero validation errors.
- Short stems (<=25 words excluding SATA instruction): 13/30 batch 4, 45/120 H.
- Explicit legal citation in stems: 0/120 under the audit regex.
- Wrong-only absolute-word cue: 0/120 under the audit regex.
- Correct option uniquely longest: 12/41 SBA with a unique longest option; uniquely shortest: 8/33 SBA with a unique shortest option.
These are descriptive lexical measures, not empirical difficulty or discrimination scores. No live pilot or independent validation was performed.

## Release gate
Before public release: full H legal/ambiguity and distractor review, integrate H exam UI and review/history functionality, verify scoring and mixed-answer behavior, regression and deployment checks. This batch does not implement or deploy the UI. Form F's unmerged PR remains a separate release dependency for the full A–H and EFGH Mix rollout.
