# GPT-FRESH-B3-MINIMUM-REPAIRS-V1 evidence

## Scope and immutable phase record

- Auditor instance: `GPT-FRESH-B3-MINIMUM-REPAIRS-V1`
- Represented candidate branch/SHA: `codex/batch3-minimum-repairs` at `dc72971f710056a5bdc2732809ead132b69fff4a`
- Freeze branch/SHA: `freeze/batch3-minimum-repairs-v1` at `8eca91617380ec07783253d6a3d194f66f3bbe1c`
- Auditor branch: `audit/batch3-minimum-repairs-gpt-fresh-v1`
- Phase-1 blind-lock commit: `af71dea436e9f6d1a1fdc024938f871dac5e2049`
- Phase-1 lock path: `audits/remediation/2026-08-20/GPT-FRESH-B3-MINIMUM-REPAIRS-V1-PHASE1-BLIND-LOCK.json`

The remote freeze branch and represented candidate branch were independently checked with `git ls-remote` on 2026-08-20 and matched the SHAs above. The auditor worktree was created from the freeze SHA without inspecting the controller worktree. Before the Phase-1 lock was committed and pushed, the only repository content read was the sanitized blind package and safe Phase-0 attestation; no canonical key, rule, drug, audit, post-lock dependency, controller record, author report, Issue #91 content, generated payload, or question-touching Git history was opened.

The blind selections were `MA-Q-0169: B,C,E`; `MA-Q-0202: B,C,E`; `MA-Q-0203: B`; `MA-Q-0340: A,C,E`; `MA-Q-0348: B,D,E`; `MA-Q-0350: A,C,E`; and `MA-Q-0359: B,C,D`. All seven matched the frozen canonical keys after unsealing.

## Frozen identity verification

The repository's `question_audit_hash` function reproduced every contract hash, and `git hash-object` reproduced every frozen question blob:

| Question | Audit hash | Git blob |
|---|---|---|
| `MA-Q-0169` | `51aff0d420fbd6c6ce19fc3caeaa50ac4b0a5b4f85a996e11aa7e48f40363a72` | `d8583fc67e73d0e5667ccc8e16e8936b2986e66c` |
| `MA-Q-0202` | `4da17f404c67b1551065b818d8829d91cb81773e6d9ff056c44483613b027bdd` | `8174eca380577315f190942442d97c8f925153e6` |
| `MA-Q-0203` | `107a7f63b2d39141ecd1a17da6cbe8ecf704f059aa7b2aad2b956e08d9f79488` | `49a68c650fcb37c39bb3c929b9975a4bd8fd898e` |
| `MA-Q-0340` | `5e7f32103eb904bd6a33c0594ed5d389a1d5c107a0f3a4928563fe207f63fb4b` | `2ba40c31c05a4c9a7e21d72dabd85e6e03865631` |
| `MA-Q-0348` | `049b79cf22e587663c0c4feed378295785b5df77e5c8fb87c98964eecfef8b03` | `bb523aea51df0b42fcca608041a1d35e2d50631e` |
| `MA-Q-0350` | `d0a069e8e1fc13c6867afb9128f2276d50aa45fd904374aa608cef45829ed0e9` | `be30745315075d8f7473af864634e9bb7590ebd1` |
| `MA-Q-0359` | `9c5b2ca17af3b73ff7ce3816c232d9a7be6fc64320aa655e34c3f85c0ef3e286` | `d673e7bb429e21f5afd14badc26913460a11b695` |

## Current official sources checked on 2026-08-20

- [247 CMR 9.00: Professional Practice Standards](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download), especially 247 CMR 9.08(2) and 9.08(3)(b), Mass. Register #1536 (12/06/2024).
- [Policy 2023-01: Compliance Packaging and Reusable Dose Planners](https://www.mass.gov/doc/2023-01-compliance-packaging-and-reusable-dose-planners-pdf/download), Multi-Drug-Single-Dose Packaging, revised 01/09/2025.
- [105 CMR 700.00: Implementation of M.G.L. c.94C](https://www.mass.gov/doc/105-cmr-700-implementation-of-mgl-c94c-0/download), especially 700.002 and 700.003(F), Mass. Register #1514 (02/02/2024).
- [M.G.L. c. 112, s. 24B1/2](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section24B%201~2), especially subsection (c)(5).
- [M.G.L. c. 94C, s. 1](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C/Section1), definition of `Administer`, clause (c)(i)-(iii).
- [21 CFR Part 1308](https://www.ecfr.gov/current/title-21/chapter-II/part-1308), controlled-substance schedules used by 105 CMR 700.002.

The immutable Phase-1 lock labels the emergency-vaccine provisions as 105 CMR 700.003(H), reflecting a legacy official PDF/search rendering retrieved before unsealing. A fresh check of the current 02/02/2024 compilation after the lock confirmed that the same substantive provisions are currently numbered 105 CMR 700.003(F). This numbering correction does not change any Phase-1 selection; the final legal records use the current `F` citations.

## Full-bank distinctness method and result

All 406 files in `data/questions` were parsed, not sampled. For each record, the stem and all choice texts were concatenated, lowercased, and tokenized to ASCII alphanumeric terms. Word unigrams and adjacent word bigrams were weighted with corpus-level smoothed IDF, L2-normalized, and compared by cosine against every other record. A second token-trigram set Jaccard score was calculated. The top automated matches were then manually compared by rule, fact pattern, decision, and distractor structure; same-family and prior-audit comparisons were also inspected even when not in the top three.

| Question | Closest automated comparisons (TF-IDF cosine) | Manual distinctness result |
|---|---|---|
| `MA-Q-0169` | `MA-Q-0202` 0.438458; `MA-Q-0203` 0.360200; `MA-Q-0135` 0.172380 | PASS: regulation/policy and packaging-boundary reconciliation is distinct from the named-drug matrix and single-drug application. |
| `MA-Q-0202` | `MA-Q-0203` 0.444334; `MA-Q-0169` 0.438458; `MA-Q-0135` 0.179777 | PASS: five-drug/two-package matrix is a broader applied classification task. |
| `MA-Q-0203` | `MA-Q-0202` 0.444334; `MA-Q-0169` 0.360200; `MA-Q-0393` 0.140115 | **FAIL**: `MA-Q-0202` choice A already contains the same stable Schedule III buprenorphine, same morning multi-drug pouch, and same maintenance-exception issue. |
| `MA-Q-0340` | `MA-Q-0337` 0.186265; `MA-Q-0321` 0.179332; `MA-Q-0341` 0.164661 | PASS: set-level retail powers remain distinct from isolated discontinuation, competence, and continuation questions. |
| `MA-Q-0348` | `MA-Q-0344` 0.181325; `MA-Q-0349` 0.161410; `MA-Q-0350` 0.099121 | PASS: cumulative Commissioner/practitioner gate is distinct from collaborative authority, student supervision, and protocol subjects. |
| `MA-Q-0350` | `MA-Q-0344` 0.134473; `MA-Q-0348` 0.099121; `MA-Q-0393` 0.070457 | PASS: express protocol-subject discrimination is distinct, and the repaired distractors are plausible adjacent duties. |
| `MA-Q-0359` | `MA-Q-0328` 0.159249; `MA-Q-0331` 0.146543; `MA-Q-0145` 0.146500 | PASS: clause-specific statutory gates are distinct from eligible-product, route, and category-membership questions. |

## Adjudication and side findings

| Question | Legal | Realism |
|---|---|---|
| `MA-Q-0169` | `KEEP` / `YES` | `KEEP` / `PASS` |
| `MA-Q-0202` | `KEEP` / `YES` | `KEEP` / `PASS` |
| `MA-Q-0203` | `MINOR_EDIT` / `YES` | `MAJOR_REWRITE` / `FAIL` |
| `MA-Q-0340` | `KEEP` / `YES` | `KEEP` / `PASS` |
| `MA-Q-0348` | `KEEP` / `YES` | `KEEP` / `PASS` |
| `MA-Q-0350` | `KEEP` / `YES` | `KEEP` / `PASS` |
| `MA-Q-0359` | `KEEP` / `YES` | `KEEP` / `PASS` |

`MA-Q-0203` has two independent defects. First, its canonical `drug_ids` is `["oxycodone"]` while the visible item and all substantive explanation fields concern buprenorphine. Second, it is not distinct from `MA-Q-0202` choice A. The answer `B` is nevertheless legally correct. The legal record therefore calls for a dependency-only minor edit, while the realism record applies the all-criteria rule and requires a major rewrite for distinctness. No canonical question, rule, drug, schema, tool, generated artifact, controller record, release status, or adjudication was modified by this audit.
