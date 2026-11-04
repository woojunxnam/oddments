# GPT-FRESH-B3-Q0203-V2 evidence

## Scope and immutable phase record

- Auditor instance: `GPT-FRESH-B3-Q0203-V2`
- Represented candidate branch/SHA: `codex/batch3-q0203-v2-repair` at `78a76aa9d9646ed28fdcca678e7e274da2489f7b`
- Freeze branch/SHA: `freeze/batch3-q0203-v2` at `0ca6b25a290c75bcb59ca1c2fad08f8e55845280`
- Auditor branch: `audit/batch3-q0203-v2-gpt-fresh`
- Phase-1 blind-lock commit: `9c75f4d31cc03e53337c74fec9c180a3b4e3c768`
- Phase-1 lock path: `audits/remediation/2026-08-20/GPT-FRESH-B3-Q0203-V2-PHASE1-BLIND-LOCK.json`

2026-08-20에 `git ls-remote`로 remote freeze branch가 정확히 `0ca6b25a290c75bcb59ca1c2fad08f8e55845280`임을 먼저 확인한 뒤, 그 SHA에서 별도 worktree와 auditor branch를 만들었다. controller worktree의 파일은 열지 않았다. Phase-1 lock 전 repository read 범위는 sanitized blind package, governance Phase-0 attestation, 두 audit contract뿐이었다. canonical question/key, rule, drug, audit, post-lock dependency, controller/author record, Issue #91, generated payload 및 MA-Q-0203 관련 Git history/diff/blame는 lock commit/push 전에 열지 않았다. prior auditor와 연락하지 않았고 substantive judgment를 전달받지 않았다.

blind solve는 current official source만으로 수행했고 선택은 `C`였다. lock commit을 remote auditor branch에 push한 뒤에만 canonical material을 unseal했다. canonical key도 `C`였으므로 blind answer와 일치했다.

## Frozen identity and dependency verification

repository의 `question_audit_hash`와 `semantic_content_hash`를 직접 실행한 결과는 contract snapshot과 모두 일치했다.

| Record | Recomputed value | Contract value | Result |
|---|---|---|---|
| `MA-Q-0203` audit hash | `ce251a6a745881352e0dfbc030efd479603cf96c4d43d2a1ae3a3cfed76c335d` | same | `MATCH` |
| `MA-Q-0203` Git blob | `cd71f7bb2a469302ca98b412ef3ef88f9c1eadbd` | same | `MATCH` |
| `MA-COMPLIANCE-PACKAGING` | `98da9e6947a6bb5feee600f1e52ed1324c609442f99cd72828922001d000f91d` | same | `MATCH` |
| `methylphenidate` | `4811f9e9c4762186f029fcbae5fd038dc81759a9e252b252d82ef3f26204b18c` | same | `MATCH` |
| `MPJE-MA-PRE2027-BLUEPRINT` | `4d5e3acaccaa562b16e53740e802a3a05ada5900a09a65585f3e6f94d7827a86` | same | `MATCH` |
| `MPJE-MA-PRE2027` | `293be8fdcd39af2255a22a0423b7123d5cfcf7c0e6c561872eb0ef04e745015c` | same | `MATCH` |

canonical `rule_ids`는 `MA-COMPLIANCE-PACKAGING`, `drug_ids`는 `methylphenidate`이며 visible stem, explanation 및 post-lock reveal과 일치한다.

## Current official sources acquired independently

- [247 CMR 9.00: Professional Practice Standards](https://www.mass.gov/regulations/247-CMR-900-professional-practice-standards)와 [official PDF](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download), 특히 247 CMR 9.08(1), (1)(h), (2), (3), (3)(b), Mass. Register #1536 (12/06/2024). PDF SHA-256은 `9e1f9d1d2813f761ee7d275c83e220f371382a2e81e0f485f2b7aaabcddce22a`였다. PDF page 6/17, printed page `247 CMR - 54`를 text extraction과 2x raster rendering으로 각각 확인했다.
- [Policy 2023-01: Compliance Packaging and Reusable Dose Planners](https://www.mass.gov/doc/2023-01-compliance-packaging-and-reusable-dose-planners-pdf/download), section II와 Single-Drug-Single-Dose 및 Multi-Drug-Single-Dose headings, revised 01/09/2025. PDF SHA-256은 `b3a205bbd29c3eca5e733d08fcef9d79650b00ea0a9dbc156b4eb474200bd548`였고 pages 2-3을 extraction과 rendering으로 확인했다.
- [DailyMed current FDA labeling for Methylphenidate Hydrochloride Oral Solution](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=2cf1b26b-199d-4c7f-ab64-4805a9def2cc), updated 05/11/2026. 이 official label은 oral solution dosage form과 `CII` status를 확인한다.
- [NABP MPJE Competency Statements](https://nabp.pharmacy/programs/examinations/mpje/competency-statements/)와 [public MPJE sample items](https://nabp.pharmacy/wp-content/uploads/2020/07/MPJE-Sample-Questions.pdf). 2026-08-20 현재 2027-03-01 전 시험에는 기존 competency statements가 적용됨을 확인하고 frozen style profile의 범위와 대조했다.

Mass.gov landing page는 current regulation date를 `12/06/2024`로 표시했다. browser open은 HTTP 403이었지만 official download endpoint의 PDF는 직접 확보됐다. source wording과 page layout을 두 방식으로 확인했으며 repository 내부 authority summary만을 source로 삼지 않았다.

## Legal analysis

247 CMR 9.08(1)은 oral-liquid-single-dose, single-drug-single-dose 및 multi-drug-single-dose를 별도의 compliance-packaging types로 열거한다. (1)(h)는 prescription에 따른 compounding이 아닌 경우 oral-liquid-single-dose package 안의 commercially available medication을 하나로 제한한다. facts는 그 제한과 일치하도록 second drug가 없다고 명시한다.

9.08(3)의 heading과 opening sentence는 multi-drug-single-dose packaging을 solid oral dosage forms에 관하여 규율하고, (3)(b)는 Schedule II/III controlled substance가 그 package 안에 들어가는 경우를 금지한다. 따라서 paragraph (3)(b)는 한 measured dose의 methylphenidate oral solution만 든 oral-liquid-single-dose container를 그 자체로 금지하지 않는다. stem은 다른 법적 요건을 별도 검토 대상으로 명시하므로 C는 과도한 일반 허가를 말하지 않는다.

## Full-bank distinctness method and result

`data/questions`의 406 JSON files를 모두 파싱했다. 각 record의 stem과 모든 choice text를 결합하고 lowercase ASCII alphanumeric tokens로 normalize했다. 전체 corpus에서 word unigrams와 adjacent word bigrams에 smoothed IDF를 적용하고 L2 normalize한 뒤 target과 다른 405 records의 cosine을 전부 계산했다. 별도로 token-trigram set Jaccard도 405쌍 전부 계산했다. 자동 상위 항목, same-rule/topic 전 항목 및 같은 family 여부를 rule, facts, decision path, correct proposition과 distractor architecture 차원에서 수동 비교했다. existing duplicate report는 사용하지 않았다.

| Rank basis | Comparison | Score | Manual result |
|---|---|---:|---|
| word TF-IDF 1 | `MA-Q-0202` | `0.259874` | five-drug/two-solid-package SATA matrix다. choice B가 methylphenidate single-drug-single-dose를 포함하지만 oral-liquid category를 판단하지 않는다. |
| word TF-IDF 2 | `MA-Q-0169` | `0.240859` | abstract regulation/policy boundary SATA이며 drug 또는 oral-liquid fact application이 없다. |
| word TF-IDF 3 | `MA-Q-0195` | `0.179382` | recurring methadone emergency pathway로 subject와 rule이 무관하다. generic plan/prohibition wording이 만든 lexical match다. |
| same domain | `MA-Q-0393` | `0.135812` | compliance packaging이지만 247 CMR 9.08(1)(c)의 FDA-labeling conflict를 판단한다. |

token-trigram Jaccard의 substantive top은 `MA-Q-0202` `0.036199`, `MA-Q-0169` `0.033175`였다. `MA-Q-0203`과 동일한 `family_id`를 가진 다른 record는 없었다. choice-level 검토에서도 같은 rule의 일반 명제가 재사용된다는 residual proximity는 확인했지만, 이 item은 bank에서 유일하게 별도로 명명된 oral-liquid-single-dose category를 multi-drug-single-dose prohibition과 구분한다. 이는 단순한 drug 또는 maintenance-status swap이 아니라 규정이 구별하는 packaging type을 적용하는 별도 판단이므로 `distinct_from_bank=true`로 판정했다.

## Realism all-criteria application

| Criterion | Result | Basis |
|---|---|---|
| `jurisprudence_reasoning` | `true` | prohibition의 문언상 scope를 package facts에 적용한다. |
| `practice_plausibility` | `true` | pharmacy의 measured oral-liquid dose packaging은 규정과 current dosage form에 직접 대응한다. |
| `authentic_distractors` | `true` | universal-ban, container-classification, invented authorization/consent errors를 구별한다. |
| `wording_not_guessable` | `true` | key를 고르려면 (3)(b)의 package-specific scope를 알아야 한다. |
| `reasoning_not_trivia` | `true` | schedule 단독 회상이 아니라 legal category와 prohibition scope를 결합한다. |
| `natural_rule_combination` | `true` | 9.08의 category structure와 (3)(b)를 같은 dispensing decision에 자연스럽게 적용한다. |
| `appropriate_drug_context` | `true` | current official label에 실제 oral solution과 CII status가 확인된다. |
| `distinct_from_bank` | `true` | 406-record 비교에서 oral-liquid-single-dose boundary는 고유하다. |
| `not_schedule_flashcard` | `true` | stem이 Schedule II를 제공하고 packaging scope를 묻는다. |
| `public_style_without_copying` | `true` | public SBA structure를 따르되 protected content의 복제 증거가 없다. |

모든 criterion이 `true`이므로 all-criteria rule상 realism 결과는 `PASS`다.

## Prior-defect disposition and side findings

v1의 두 verified defects를 각각 다시 확인했다.

1. `drug_ids=["oxycodone"]`인데 visible scenario는 buprenorphine이었던 dependency mismatch는 v2에서 `drug_ids=["methylphenidate"]`로 바로잡혔고 current visible drug 및 dependency snapshot과 일치한다. `RESOLVED`.
2. v1이 `MA-Q-0202` choice A와 동일한 stable Schedule III buprenorphine multi-drug morning-pouch/maintenance-exception decision을 확장했던 collision은 v2에서 oral-liquid-single-dose category application으로 교체됐다. 같은 rule family의 residual proximity는 남지만 decision category는 material하게 달라졌다. `RESOLVED`.

non-blocking side finding은 `MA-Q-0169`와 `MA-Q-0202`가 같은 rule의 일반 명제와 methylphenidate 예시를 이미 포함한다는 점이다. 따라서 future bank expansion에서는 이 rule을 다시 좁게 변형한 item을 추가하지 않는 편이 좋다. 그러나 current v2는 고유한 oral-liquid category를 묻고 all-criteria threshold를 충족한다.

본 audit은 canonical question, rule, drug, schema, tooling, generated artifact, controller record, release state 및 adjudication을 수정하지 않았다. 변경 범위는 immutable Phase-1 lock, 두 contract audit JSONs 및 이 evidence report뿐이다.

## Validation

- `py scripts/validate_audits.py`: `audits: 0 error(s), 0 warning(s)`.
- `py scripts/validate_all.py`: `all: 0 error(s), 1 warning(s)`. 유일한 warning은 기존 `MA-Q-0190: correct option is materially longer than distractors`였으며 본 audit 변경과 무관하다.
- `py -m pytest -q`: `98 passed, 1 skipped in 6.93s`.
- `git diff --check`: 통과.
