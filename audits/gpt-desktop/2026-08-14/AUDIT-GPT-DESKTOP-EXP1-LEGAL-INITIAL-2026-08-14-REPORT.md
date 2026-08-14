# GPT Independent Legal Audit — Expansion Batch 1 (MA-Q-0091–MA-Q-0130)

## 결론

이 batch는 현 상태로 release할 수 없다. 40문항 중 `KEEP` 36개, `MINOR_EDIT` 1개, `MAJOR_REWRITE` 3개로 판정했다. 핵심 blocker는 Q105의 personnel-category ambiguity, Q120의 Schedule VI transfer personnel 오류, Q123의 e-prescribing exception verification 오류다. Q115는 seven-business-day 결론 자체는 맞지만 서로 다른 report category의 trigger를 한 문장에 합친 정밀도 결함이 있다.

Canonical question, rule 및 drug record는 수정하지 않았다. 이 보고서와 canonical audit JSON만 산출했다.

## Scope와 독립성

- Frozen target branch: `feature/mpje-expansion-batch1`
- Frozen target SHA: `6403868ee78d40fb0ba801d01293c64a41e57828`
- Audit branch: `audit/gpt-desktop-exp1-q0091-0130-2026-08-14`
- Scope: `MA-Q-0091`–`MA-Q-0130`, 정확히 40문항
- Auditor: `GPT`
- Audit status: `FULLY_ADJUDICATED`
- Legal JSON: `data/audits/AUDIT-GPT-DESKTOP-EXP1-LEGAL-INITIAL-2026-08-14.json`

`CLAUDE-LEGAL-EXP1-Q0091-0130.json`은 question payload와 frozen hash를 얻는 structural input으로만 사용했다. 그 파일에는 legal result가 없었다. 이전 GPT audit, prior audit branch, PR #19 및 Issue #17의 이전 GPT finding은 열람하지 않았다.

## Freeze와 hash 검증

Remote의 `refs/heads/feature/mpje-expansion-batch1`와 `refs/pull/16/head`가 모두 frozen SHA와 일치함을 확인했다. `scripts/qa_common.py::question_audit_hash`로 다음 세 집합을 검증했다.

- Requested ID set = package ID set = canonical ID set: `40/40`
- Package embedded question hash mismatch: `0`
- Current canonical question hash mismatch: `0`

따라서 stale payload나 target drift 없이 audit를 진행했다.

## 검토 방법

먼저 40개 stem과 choices만 읽고 각 문항을 독립적으로 풀었다. 그 뒤 2026-08-14 현재의 Massachusetts Legislature, Mass.gov Board/DPH regulation, eCFR, DEA 및 FDA DailyMed source를 확인했다. 독립 결론을 고정한 다음에만 existing key와 explanation을 열어 다음을 대조했다.

1. stem의 사실이 적용 조문을 충분히 특정하는지
2. 각 choice가 해당 사실관계에서 true/false인지
3. key set이 완전하고 과포함되지 않았는지
4. explanation이 choice마다 정확한 rule과 trigger를 가르치는지
5. drug identity, federal schedule, Massachusetts Schedule VI status 또는 storage fact가 결론에 중요할 때 별도 공식 source와 일치하는지

주요 current source는 [247 CMR 8.00](https://www.mass.gov/doc/247-cmr-8-pharmacy-interns-and-technicians/download), [247 CMR 9.00](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download), [247 CMR 15.00](https://www.mass.gov/doc/247-cmr-15-continuous-quality-improvement-program/download), [247 CMR 20.00](https://www.mass.gov/doc/247-cmr-20-reporting/download), [105 CMR 721.000](https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download), Massachusetts General Laws 및 current eCFR이다.

## Release-blocking legal findings

### MA-Q-0105 — `MAJOR_REWRITE`

Stem은 정의된 category인 “technician”이 Adderall stock bottle을 “handle”한다고 명시한다. 그러나 `247 CMR 8.05(2)(a)`는 ordinary pharmacy technician에게 Schedule II의 `transporting` assist만 허용하고, `8.05(2)(b)`는 `certified pharmacy technician`에게만 pharmacist supervision·approval·written P&P 아래 `transporting and handling`을 허용한다. Existing E는 “personnel category에 따라 다르다”는 일반론으로는 맞지만 이미 주어진 ordinary category의 권한을 답하지 않는다.

현 choices에는 완전한 정답이 없다. Rewrite에서는 category를 명확히 하고 `transporting`과 `handling`을 분리해야 한다. Adderall은 FDA DailyMed상 mixed amphetamine salts이며 `DEA Schedule CII`이다: [DailyMed Adderall label](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=f22635fe-821d-4cde-aa12-419f8b53db81).

### MA-Q-0120 — `MAJOR_REWRITE`

Warfarin은 prescription drug로서 Massachusetts Schedule VI에 해당한다. `247 CMR 9.14(4)`는 Schedule VI prescription을 Schedule III–V와 같은 manner로 transfer하도록 하면서 remaining refills와 one-year limit를 둔다. 동시에 `247 CMR 8.04(4)(d)`는 pharmacist approval 아래 `certified pharmacy technician`이 Schedule VI transfer를 수행할 수 있게 한다.

따라서 A의 “pharmacist-to-pharmacist communication requirements”를 이 warfarin scenario의 보편 정답으로 채점하는 것은 부정확하다. Federal `21 CFR 1306.25`의 direct licensed-pharmacist rule은 federal Schedule III–V refill transfer rule이다. Proposed key는 `B, D`이며, rewrite에서는 authorized personnel, remaining refills 및 one-year limit를 구체적으로 물어야 한다.

### MA-Q-0123 — `MAJOR_REWRITE`

`M.G.L. c. 94C, § 23(g)-(h)`와 `105 CMR 721.070(A)`는 electronic prescribing general rule과 exceptions를 둔다. 하지만 `105 CMR 721.070(C)`는 otherwise valid written/oral prescription을 받은 pharmacist가 그 prescription이 exception 또는 waiver에 적절히 해당하는지를 verify할 의무가 없다고 명시한다. [Current regulation text](https://www.mass.gov/doc/105-cmr-721-standards-for-prescription-format-and-security-in-massachusetts/download).

Existing C는 pharmacist가 exception pathway를 평가해야 한다고 가르쳐 이 조문과 충돌한다. Proposed key는 `A, B`이다. 또한 `721.070(A)(9)`는 Schedule VI prescription을 electronic-prescribing requirement에서 제외하므로 rewrite에서 tested schedule을 명시해야 한다.

### MA-Q-0115 — `MINOR_EDIT`

Seven-business-day 결론은 맞다. 다만 `247 CMR 20.02(1)`의 improper dispensing은 related serious injury/death의 discovery를 trigger로 하고, `20.02(2)`의 pharmacy-manufactured/produced/compounded product serious adverse event는 any employee knowledge를 trigger로 한다. Existing D와 explanation은 이를 “discovery or employee knowledge”로 합쳐 썼다. 이 stem에는 전자만 적용되므로 trigger 문구를 분리해야 한다. [247 CMR 20.02](https://www.mass.gov/doc/247-cmr-20-reporting/download).

## Drug identity와 schedule 검증

| Drug context | 확인 결과 | 공식 근거 |
|---|---|---|
| Vyvanse | `lisdexamfetamine dimesylate`, `CII` | [FDA DailyMed](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=704e4378-ca83-445c-8b45-3cfa51c1ecad), `21 CFR 1308.12(d)` |
| Adderall | mixed amphetamine salts, `CII` | [FDA DailyMed](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=f22635fe-821d-4cde-aa12-419f8b53db81), `21 CFR 1308.12(d)(1)` |
| Alprazolam | benzodiazepine, `CIV` | [FDA DailyMed](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=f6dd8005-1d50-41bc-e053-6394a90ac45b), `21 CFR 1308.14(c)(2)` |
| Pregabalin | `CV` | [FDA DailyMed](https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=fd01590e-5b90-4a77-ad5f-76adabf3c32e), `21 CFR 1308.15(e)(7)` |
| Methylphenidate | `CII` | `21 CFR 1308.12(d)(4)` |
| Oxycodone | `CII` | `21 CFR 1308.12(b)(1)(xiv)` |
| Warfarin, insulin glargine, gabapentin | federal Schedule I–V가 아닌 prescription drugs이므로 Massachusetts Schedule VI | `M.G.L. c. 94C, § 2(a)`; `105 CMR 700.002(F)` |
| Insulin glargine storage | temperature-sensitive; frozen/overheated product는 사용하지 않도록 label이 지시 | [FDA DailyMed](https://dailymed.nlm.nih.gov/dailymed/fda/fdaDrugXsl.cfm?setid=9835904f-64f5-42b3-9ac9-89e4aaa5182a) |

## Question-by-question adjudication

| Question_ID | Verdict | Existing_Answer_Correct | Proposed_Answer | 주된 법적 결론 |
|---|---|---:|---|---|
| MA-Q-0091 | KEEP | YES | B | `247 CMR 9.18` counseling offer |
| MA-Q-0092 | KEEP | YES | A, C | `21 CFR 208.24(e)`와 state counseling은 별도 의무 |
| MA-Q-0093 | KEEP | YES | D | `M.G.L. c. 112, § 12D` interchange default |
| MA-Q-0094 | KEEP | YES | B, D, E | no-substitution, availability, exception |
| MA-Q-0095 | KEEP | YES | A | patch 및 self-administered oral hormonal contraceptive |
| MA-Q-0096 | KEEP | YES | A, C | screening, protocol, labeling |
| MA-Q-0097 | KEEP | YES | C | third-party opioid-antagonist access |
| MA-Q-0098 | KEEP | YES | B, D | third party 및 standing order |
| MA-Q-0099 | KEEP | YES | A, B, D, E | CDTM qualification bundle |
| MA-Q-0100 | KEEP | YES | E | retail CDTM adult/referral/consent/scope |
| MA-Q-0101 | KEEP | YES | B | Schedule VI prescription copy within 24 hours |
| MA-Q-0102 | KEEP | YES | D | retail CDTM cannot authorize Schedule II–V prescribing |
| MA-Q-0103 | KEEP | YES | A | technician에게 clinical judgment 위임 불가 |
| MA-Q-0104 | KEEP | YES | C | employer policy는 trainee scope를 확장하지 못함 |
| MA-Q-0105 | MAJOR_REWRITE | PARTIALLY | No complete existing choice | ordinary technician과 certified technician 권한 혼동 |
| MA-Q-0106 | KEEP | YES | B | intern direct supervision |
| MA-Q-0107 | KEEP | YES | D | daily internship credit maximum 12 hours |
| MA-Q-0108 | KEEP | YES | A | 20 contact hours per calendar year |
| MA-Q-0109 | KEEP | YES | C | compounding-specific additional CE |
| MA-Q-0110 | KEEP | YES | B, C, D | CQI detect/document/assess/prevent |
| MA-Q-0111 | KEEP | YES | E | initial QRE documentation within 24 hours |
| MA-Q-0112 | KEEP | YES | A, D, E | immediate patient response 및 conditional prescriber notice |
| MA-Q-0113 | KEEP | YES | A, C, D | workflow/technology/training/staffing analysis |
| MA-Q-0114 | KEEP | YES | B | CQI education at least annually |
| MA-Q-0115 | MINOR_EDIT | YES | D, trigger wording 수정 | report-category trigger 분리 |
| MA-Q-0116 | KEEP | YES | A | five years from report filing |
| MA-Q-0117 | KEEP | YES | B, C, D | accept, quarantine, no inventory return, dispose |
| MA-Q-0118 | KEEP | YES | C | Schedule VI prescription required elements |
| MA-Q-0119 | KEEP | YES | E | controlled prescription retention two years |
| MA-Q-0120 | MAJOR_REWRITE | PARTIALLY | B, D | Schedule VI transfer authorized personnel 오류 |
| MA-Q-0121 | KEEP | YES | B | out-of-state Schedule III–VI 30-day rule; III–V verification |
| MA-Q-0122 | KEEP | YES | D | Massachusetts Schedule VI definition |
| MA-Q-0123 | MAJOR_REWRITE | PARTIALLY | A, B | pharmacist need not verify exception/waiver |
| MA-Q-0124 | KEEP | YES | A | out-of-state oral III–V follow-up request |
| MA-Q-0125 | KEEP | YES | C | initial inventory on first controlled activity date |
| MA-Q-0126 | KEEP | YES | E | inventory at least every two years |
| MA-Q-0127 | KEEP | YES | C, D, E | exact/estimated count and 1,000-unit threshold |
| MA-Q-0128 | KEEP | YES | C | Form 222 or CSOS for Schedule II procurement |
| MA-Q-0129 | KEEP | YES | A, B, D | paper/electronic Form 222 record treatment |
| MA-Q-0130 | KEEP | YES | A, C, E | reverse distributor, non-retrievable, Form 41 |

각 행의 exact section, official URL, `law_checked_date`, `Problem`, `Proposed_Rewrite` 및 `Proposed_Explanation`은 canonical legal JSON에 완전하게 기록했다.

## Release consequence

`MINOR_EDIT` 또는 `MAJOR_REWRITE`가 하나라도 있으면 current question hash에 대한 legal pass가 아니다. 따라서 Q105, Q115, Q120, Q123을 canonical에서 수정한 뒤 새 hash에 대해 GPT와 Claude legal re-audit가 필요하다. 별도 realism audit도 Q130을 제외한 39문항을 `FAIL`로 판정했으므로 batch 전체는 현 상태로 release gate를 통과하지 못한다.
