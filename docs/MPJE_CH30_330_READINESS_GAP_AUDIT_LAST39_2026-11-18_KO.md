# Massachusetts MPJE — 330문항 준비도 감사 및 마지막 39문항 보강안

> **최신 정정 (2026-11-18): 39는 요청자의 오타로 확인됨. 실제 추가 분량은 정확히 30문항이며, 별도 9문항 진단시험은 제작하지 않음.** 아래 원문 39문항 계획은 당시 연구의 이력으로만 남겨 두며, Section 5의 30+9 제안과 그 관련 권고사항은 더 이상 유효하지 않다. Draft PR #281의 B4 30문항이 작성되어 현재 C120/120 초안이고, 최종 법령 승인 및 배포는 0/120 상태다. 최신 기록은 [B4 법령 검토](form-c/b4-source-review-2026-11-18.md), [구조 검증](form-c/b4-author-structural-audit-2026-11-18.json), [Form C 계획 §14](MPJE_CH30_FORM_C_PLAN_2026-11-18.md)에 있다.


**작성일:** 2026-11-18 (America/New_York)  
**대상:** `main`의 기존 A/B 240문항 + Form C Draft PR #281의 B1–B3 90문항.  
**결론:** 기존 문제를 모두 맞혀도 합격을 보장하거나 검증된 readiness threshold를 충족했다고 단정할 수 없다. **실제 낯선 사실관계를 구분하는 능력, 원문 법령 근거, 정답 힌트 제거, 현재 규정 및 exam date에 맞는 blueprint 적용**이 별도로 필요하다.  
**보안:** 모든 새 사례는 독창적이며 실제 비공개 MPJE/Pre-MPJE 문항을 재구성하거나 옮기지 않는다. 공개된 응시자 후기에서는 주제와 체감 난이도만 추출한다.

## 1. 데이터로 확인한 현재 상태

| 지표 | 기존 A/B | Form C B1–B3 | 총계 |
|---|---:|---:|---:|
| 실제 코드상의 질문 객체 | 240 | 90 | 330 |
| SBA | 144 | 66 | 210 |
| SATA | 96 | 24 | 120 |
| Area 1 / 2 / 3 / 4 | 47/94/48/51 | 20/30/22/18 | 67/124/70/69 |
| Stem 길이 중앙값(문자·공백 포함) | 460 | 450 | 455 |
| Stem 300자 미만 | 23 | **1** | 24 |
| SBA 정답이 유일하게 가장 긴 보기 | **109/144 (75.7%)** | **0/66** | 109/210 |
| Form C 최종 법령 승인 | — | **0/90** | — |

- 두 A/B는 120+120 비중복 설계이지만 학습 과정에서 노출된 문제이며, 현재 두 모의고사는 150분 fixed-form이므로 실제 120문항/150분 adaptive MPJE와 동일한 psychometric 점수가 아니다.
- Form C 90개는 작성된 **Draft**이다. B1/B2/B3의 검증 예외 목록이 각각 4/4/8개로 **16개 연구상 보류·추가 검토 후보**이며, 개별 실체적 법률 오류/중복이 추가로 있을 수 있다. 약간의 교정은 있었지만 전체 A–D 360개에 대한 최종 source signoff는 없다.
- 전체 330문항의 472개 keyed-correct choices 중 `always|never|automatically|regardless`가 **8개(1.7%)**, 848개 keyed-incorrect choices 중 **146개(17.2%)**를 차지한다. 이는 전수 텍스트 스캔으로 발견한 선택지-작성 편향이자 test-wiseness cue이며 법률상 절대 표현이 반드시 틀리다는 뜻이 아니다.
- 기존 240문항의 `topicKey=drug-schedule-identification`은 **16개**. Form C B1–B3의 대부분은 drug schedule을 사전에 가정하거나 다른 합법적 행동을 묻는다. 약물을 **이름·함량·제형만 보고 연방법/MA Schedule로 분류하는 직접 인출**을 새 Form C가 충분히 추가했다고 보기는 어렵다.
- 새 C 90개 중 300자 미만 지문은 **단 한 개**. NABP의 공식 공개 예시는 매우 짧은 CE 숫자 인지, 약물 직접 Schedule 분류 사례도 있다. 모든 문항을 긴 다중사실 시나리오로 만들면 현실성을 높이기보다 중복 정보/정답 힌트로 과적합될 수 있다.
- 2026 NABP legacy competency areas 배분은 **22/33/24/21%**, 2027-03-01부터 새 domain **30/30/20/20%**. 구버전 Area 숫자를 신버전 domain으로 이름만 바꾸면 안 된다.

## 2. 공식 근거와 외부 도구 비교: 답이 다른 '문제수'가 아니다

- **NABP** [현재 MPJE competencies](https://nabp.pharmacy/programs/examinations/mpje/competency-statements/), [2027 새 content outline](https://nabp.pharmacy/news/blog/mpje-content-outline/), [공식 시험 구조](https://nabp.pharmacy/programs/examinations/mpje/take-the-mpje-exam/), [공개 MPJE sample PDF](https://nabp.pharmacy/wp-content/uploads/2020/07/MPJE-Sample-Questions-1.pdf). 공식 2026 MPJE는 120문항, 2.5시간 adaptive, 2024 NABP fact sheet에 100 operational/20 pretest로 제시. 정답 형식으로 SBA/SATA와 역사적 K-type을 구별한다. sample PDF 자체는 실제 출제영역 비중을 보여주는 자료가 아니라고 명시한다.
- **NABP Pre-MPJE:** [공식 안내](https://nabp.pharmacy/programs/practice-exams/pre-mpje/). MA jurisdiction-specific 40문항/50분/$90/연 1회, 구매 후 7일 내 응시. 실제 NABP 문제은행에서 만든 practice인 점에서 외부 형식 참조로 가치가 있으나 합격 확률의 검증된 calibration은 아니다. 이용약관상 AI 사용, 문항/답/스크린샷 공유·분석이 금지된다. **사용자가 스스로 응시하고 총점·약점의 자기평가만 활용해야 한다.**
- **UWorld/RxPrep:** [무료 sample 6개](https://pharmacy.uworld.com/mpje/sample-questions/)에 무서명 Ritalin Rx, DEA 개인등록 예외, 보관실사, **실제 다중 AB code Orange Book 표**, misbranding 및 controlled stock이 있다. 이중 '짧은 질문'과 '표/기록 판독'이 우리 C90의 긴 case 일변도와 다르다. [MPJE 상품](https://pharmacy.uworld.com/mpje)에는 225+ Q, 90-item practice exam이라고 소개되며 공개 sample footer는 300+라고 표현하여 버전/패키지 차이를 단정하지 않는다. 유료 원본 전체는 감사하지 못했다.
- **PharmLaw:** [MA 2026 과정](https://www.pharmlaw.com/courses/massachusetts-mpje-prep)에 기본 200문항, compounding 및 federal bonus 50문항씩, drug schedule flashcards/guide가 명시됨. [FAQ](https://www.pharmlaw.com/pages/frequently-asked-questions)의 90% 추천은 **판매자 학습 가이드**, 공식 MPJE 통과 예측식이나 근거 기반 cutoff가 아니다.
- **PharmacyExam:** [MA 과정](https://www.pharmacyexam.com/massachusetts-mpje)에 341개의 MA 문제(2026-10-18 업데이트 표시), 별도 federal 534문항, sterile/HD 210문항으로 소개됨. 숫자만으로 적합성이나 답의 정확성을 입증할 수 없다. 반대로 210 compounding은 그 주제의 충분한 practice depth가 시장에서 별도로 제공된다는 신호다.
- **Exam Master:** [MA MPJE course](https://shop.exammaster.com/massachusetts-mpje-study-resources)에 120문항 mock, 103페이지 compendium, competency map을 제시하지만 페이지의 자체 '2023 Competency Statements' 표현을 포함해 2027 blueprint 갱신 여부를 꼭 확인해야 한다. 유료 QBank 내부와 최신 법령은 검증 불가.
- **tl;dr Pharmacy:** [MA Cheat Sheet](https://shop.tldrpharmacy.com/products/mpje-cheat-sheet-massachusetts)는 압축 복습 자료이고 객관적인 독립 문제 검증의 대체물이 아니다.

### 객관적인 예측 한계

[2022 AJPE 연구](https://pubmed.ncbi.nlm.nih.gov/34785499/)에서 분석 대상 136명의 Pre-MPJE와 첫 MPJE pass/fail/실제 scaled score 사이에 통계적으로 유의한 상관이 없었다. 이는 표본과 시기의 한계가 있지만, NABP 공식 연습점수조차 합격 확률로 변환해서는 안 된다는 근거다. [2026 AJPE blueprints 연구](https://pubmed.ncbi.nlm.nih.gov/42637086/)는 2013–25 통과율을 비교하며 잦은 blueprint 변경/합격률 동향을 살폈다. 옛 시험의 암기형 문항수를 늘리는 것보다 출제기준 변화에 대한 대비가 중요하다.

## 3. 2022–2026 firsthand report: 서로 모순되는 경험도 증거다

게시물은 자기보고이며 시험 출제비율/객관적 합격률/실제 secure wording을 입증하지 못한다. **주제·실전 처리 방식만 인용**, 실제 문항 재현은 하지 않는다.

| 날짜 | 공공 응시자 보고 및 실무 함의 |
|---|---|
| **Nov 2022** | [MA 두 번 불합격](https://www.reddit.com/r/PharmacySchool/comments/yl6xl4/) — RxPrep federal, PharmacyExam, Pre-NABP, MA 책 등 다양한 학습자료에도 실패. 양이 충분조건이 아니다. |
| **Aug 2023** | [MA 재응시 후기](https://www.reddit.com/r/NAPLEX_Prep/comments/164ul4l/) — 외부 문제은행 평균 95–100%, Pre-MPJE 79라고 주장하면서 heavy compounding에 매우 당황; 뒤늦게 합격 확인. 암기 점수가 실제 난이도 체감과 동일하지 않다. |
| **Sep 2023** | [합격자의 공부 후기](https://www.reddit.com/r/NAPLEX_Prep/comments/16ddq8g) — 247 CMR, Board policies, DEA와 sterile compounding. MC/SATA mix였으며 K-type 없음이라고 서술. |
| **Aug/Sep 2024** | [실제 MA 상담/technician/partial fills](https://www.reddit.com/r/NAPLEX_Prep/comments/1f2vo96/)와 [MA 합격 분석](https://www.reddit.com/r/NAPLEX_Prep/comments/1fl4nc8/) — 직원 업무, 상담의 정확한 문서화, Rx label, 약사간 transfer의 필수 필드. Sep 합격자는 상당수는 짧은 **사실 인식** 문제였다고 회상. |
| **Oct 2024** | [비슷한 응시에서도 SATA mix 차이](https://www.reddit.com/r/NAPLEX_Prep/comments/1fxnhis) — 어떤 응시자는 SATA가 거의 없었다고 함. 새로운 C에 모든 질문을 SATA로 넣는 정책을 피할 근거. |
| **Mar/Nov 2025** | [2025 Mar HD/USP 강조](https://www.reddit.com/r/NAPLEX_Prep/comments/1jeu2lq), [Nov 범위 나열](https://www.reddit.com/r/NAPLEX_Prep/comments/1p2xhc4/) — CDTM, 인턴·technician 역할, labels/Rx validity, drug schedules, HD/training, 배송. |
| **Jun/Jul 2026** | [책/문제집과 실전 스타일 괴리](https://www.reddit.com/r/MPJE/comments/1txs7il/) 및 [실패 경험](https://www.reddit.com/r/MPJE/comments/1u2d3m7/) — 여러 유료 자료를 썼다고 합격을 보장하지 못함. [Jul MA 후기](https://www.reddit.com/r/MPJE/comments/1vb05g4/) USP 797/800와 복잡한 SATA를 강조. |
| **Aug 2026** | [같은 사람의 첫 번째와 두 번째 MA 시험 체감 차이](https://www.reddit.com/r/NAPLEX_Prep/comments/1vthrm3/), 이후 합격 답글. 이전 회차 기억만으로 시험 mix를 추정할 수 없다. |
| **Nov 2026** | [최신 MA 후보·합격자 댓글](https://www.reddit.com/r/MPJE/comments/1xmfq5h/)은 MA CMR과 DEA 원문의 최신 버전 비교를 강조. |

독립 표본 아님. 서로 다른 시기의 커뮤니티 응시담을 하나의 '표본의 과반이 USP 질문을 받았다'는 식으로 통계화하지 않는다. 2022·2023에 현재 2026 법을 역적용하거나 타 주 MPJE 경험을 MA로 일반화하지 않는다.

## 4. 실제로 개선이 필요한 8가지 근본 문제

1. **Source certainty:** Form C 90은 **0 final source signoff**. B1 4, B2 4, B3 8의 **16개 known scope/interpretation holds**. 추가적인 불확실성도 있을 수 있다. 법령 오류가 있으면 맞히는 것 자체가 잘못된 학습일 수 있음.
2. **A/B answer-length cue:** old 144 SBA 중 109개가 correct choice uniquely longest. A/B 고득점은 실제 reasoning의 분리 측정이 필요함. Bank rewrite는 storage/signature/version migration과 함께.
3. **Absolute-word cue:** all 330의 choices에서 `always/never/automatically/regardless`: 8/472 right vs 146/848 wrong. 단어만 제거하면 맞히는 간접 학습을 피해야 함.
4. **Format length homogeneity:** C 90개 중 1개만 stem < 300 chars; 공식 NABP sample과 일부 실제 2024 후기에는 단문/fact-recognition 문항도 존재함. 늘 길거나 법령을 명시해 주는 문장을 줄일 것.
5. **Drug schedule retrieval:** A/B topicKey direct 16, 추가 C90은 표준적으로 'Schedule IV' 등 답을 앞서 알려주는 적용형이 다수. drug names, formulations, state-vs-federal classification를 **바로 떠올리는** 1–2-rule 마이크로 퀴즈 보강.
6. **Evidence/data extraction:** 실제 표 형식 Orange Book AB-code (제품의 다중 AB code), transfer record, mislabeled bottle, controlled inventory snapshot, pharmacy manpower roster, compounding inspection data를 이용한 1-2 minute decision이 부족. Free UWorld sample의 실제 다중 AB 표를 벤치마크하되 복제는 금지.
7. **Uncommon-but-in-blueprint micro-rules:** FD&C adulterated vs misbranded, product supply integrity, institution/delivery chain, pharmacy ownership/change/inspection; '법령의 누구/무엇/언제/어디' 분리. 현 330 stem에서 `adulterat|misbrand` 직접 검색은 **0건**이나 choices/notes를 포함한 의미적 제로라고 단정해서는 안 됨.
8. **Readiness measurement:** A/B를 반복해서 맞히는 것은 memory contamination; C source 공개형 Draft PR도 절대 비공개가 아님. 첫 응시 150분, 한 문제씩/이전으로 돌아가기 불가, 문제 제목·답 유추 신호 없음, Area별 보고서, 첫 시도 vs 재시도 분리, 설명을 스스로 할 수 있는지 확인할 것.

## 5. 마지막 '39개'의 목적과 구조

**숫자 정합성:** 기존 240 + 현재 C90 = 330. 사용자가 요청한 39 추가라면 **369개의 전체 original question**이 된다. 그러나 C는 정확히 120문항이어야 함. 가장 생산적인 설계는 **30개를 C의 B4로 채워 120문항 Form C 완성** + **9개를 별도 Unseen Calibration / Gap Diagnostic micro-quiz**로 만드는 것. 추가 9개를 C에 넣으면 C129가 되어 계획과 충돌. 9개는 A/B/C의 초기 exam 풀에 섞지 않음.

### B4: 기존 reserved 30 slots / 6·10·7·7을 유지하되 법적 결정을 강화

- **Area 1 (6):** C004 실제 환자 약력 수집 vs pharmacist DUR; C008 lunch/break and patient release; C013 Board가 인정한 CDTM 학력 등가 예외 (**E30-001 동일 결론이면 교체**); C017 official Board-issued practice authority (**E30-206 반복이면 다른 licensure decision으로 교체**); C021 실제 impaired practice vs lawful medication use; C025 technician applicant criminal disposition / truthful disclosures.
- **Area 2 (10):** C029 out-of-state prescriber, controlled class, dispensing decision; C033 veterinary prescriber and owner/animal identity; C038 opioid initiation exception with age/context; C043 treatment disclosure vs third-party HIPAA; C047 new referral/protocol boundary (**E30-222 중복이면 다른 actor/authority 상황으로 교체**); C051 hospital vs community CDTM; C055 pharmacist may administer a prescribed non-vaccine vs independently prescribe; C059 verified institutional return/reuse exception **only if operative law exists**; C063 current iPLEDGE exact program status; C066 currently active vs terminated FDA REMS with actual decision.
- **Area 3 (7):** C070 Schedule VI continuity after closure/lack of usual pharmacy, source conflict carefully scoped; C074 missing specific required transfer record fields, concise tabular scenario; C078 prescriber-authorized correction vs impermissible new Rx, concise; **C083 change from generic recall to adulterated-vs-misbranded/product-integrity hold** (B3 C114 already tests recall); C087 new DUR vs insurer authorization vs counseling refusal; C091 listed OTC precursor, exact dosage/form and state-vs-federal sale conditions; C094 OTC naloxone sales vs payer-prescription dispensing records.
- **Area 4 (7):** C098 scale/calibration/incomplete compounding record; C103 HD intact dosage form vs crushing/splitting and exposure controls; C107 controlled inventory time boundary and reconciliation; C111 courier recipient/custody/failed delivery; C115 facility inspection corrective plan distinct from individual discipline; C119 FDA biosimilar vs **interchangeable** biologic with current Massachusetts substitution requirements; C120 emergency patient-specific pharmacy-to-pharmacy acquisition vs DSCSA/general-stock distribution and CSA order rules.

**B4 format target (editorial, not an official frequency):** approx 12–16 very short law-fact / record-decisions, 10–14 medium scenarios, 4–6 integrated cases; avoid artificial 5-item 3:2 repeating template. Keep source/effective-date and formulation checks for every key. If old C90 long vignettes dominate the final mock, trim another 10–15 without changing legally deciding facts, keeping source approval status explicit.

### Additional 9 — separate no-hint diagnostic mini-form, not part of 120

| ID | Distinct decision to test | Direct rationale |
|---|---|---|
| X01 | Real brand/generic name → current **federal** schedule (short direct) | NABP public multi-response sample tests direct schedule identification |
| X02 | Formulation-specific federal exemption vs other strength/formulation | Controlled combination products should not be memorized as ingredient-only |
| X03 | **Massachusetts** schedule difference and MassPAT-reportable medicine given actual name | State-federal precedence, especially MA Schedule VI vs federal classification |
| X04 | Realistic new Rx with omitted/altered field → may correct vs must obtain a new Rx | Shorter Rx validity rather than a pre-labeled legal exception |
| X05 | Transferred prescription / container label record table with one missing field | Case must require inspecting actual data, not spotting 'always' |
| X06 | USP <795> BUD / component stability or formulation comparison **only with verified applicable text** | Depth check without invented normative limits |
| X07 | USP <797>/<800> practical garbing/HD control/EM response with current primary law/policy | Recent firsthand heavier practical compounding, chapter original gate |
| X08 | FD&C **adulterated vs misbranded** decision with held product | NABP's public course sample and official law: direct stem gap |
| X09 | Orange Book **multiple AB codes** or biosimilar reference/interchangeable FDA evidence table | Data extraction and product substitution rather than made-up single-code pair |

All 39 items must be genuinely original and the 9 diagnostic questions should be created ONLY after independent retention of the C-120 unseen condition; if adding nine exposes the same law decision in Form C, re-scope the 9 to transfer knowledge instead of duplicating a test. No prescriber issued examples from secure exam memories.

## 6. Readiness decision process

1. **Current law first:** clear all 16 known C holds; all B4 and extra nine have per-option official support, current effective date, prescriber/setting/protocol exceptions and no competing keys. Existing A/B high-risk items need targeted re-audit. Incorrect option rationales are more dangerous than low scores.
2. **Remove hints:** before treating A/B scores as diagnostic, reduce 109 uniquely longest correct SBA and eliminate answer-based absolute-term shortcuts using case-specific false alternatives. Update manifest fingerprint and preserve previous attempts. Do not change old A/B without a version/history migration.
3. **Three-stage evidence:** A/B scores = mastery and legal explanation practice; NEW first-attempt C120 = retention/transfer and timing; outside NABP public sample or official Pre-MPJE (personally taken by learner, without AI during exam) = different item-writing style. A/B seen bank is never an unbiased final readiness exam.
4. **Clinical judgment:** ensure candidate can explain **why each distractor is false**, what factual edit reverses the key, and federal vs MA governing source, without looking at explanations; compute actual weak subdomain counts.
5. **Quantitative goals (NOT validated pass predictions):** fresh C120 about **85–90% overall raw**, each major Area at least ~80%, no persistent high-risk source errors, 150 minutes with fully completed submissions, and successful unfamiliar transfer cases. These are conservative *study targets* only. A/B retakes may aim for 90%+ with reasoning, but are not proof.
6. **2027 date gate:** if actual exam date is March 1, 2027 or later, re-map every item to the **new official** outline (30/30/20/20). The old 22/33/24/21 by Area does not automatically translate; no user's exam date was supplied.
7. **Stopping rule:** When all core skills have correct sources, the fresh exam is completed without exploitation of cues and remaining errors are narrow/repaired, further 10–20 redundant questions are lower-value than targeted study of official Board regulations, policies, DEA manual and USP provisions.

**Recommendation:** Do not claim 330/330 or 369/369 implies a 100% probability of passing. Appropriately written, source-verified practice questions can be the **primary learning vehicle** for this user, but a small amount of direct law reading and unfamiliar external sample-style calibration is needed to establish readiness. The issue is not a raw question-count deficit; it is legal accuracy, test-wiseness cues, short fact-recall and fresh transfer assessment.

## 7. Main source links

- NABP [current competencies](https://nabp.pharmacy/programs/examinations/mpje/competency-statements/), [new 2027 outline](https://nabp.pharmacy/news/blog/mpje-content-outline/), [official Pre-MPJE](https://nabp.pharmacy/programs/practice-exams/pre-mpje/), [MPJE sample questions](https://nabp.pharmacy/wp-content/uploads/2020/07/MPJE-Sample-Questions-1.pdf), [2024 psychometric fact sheet](https://nabp.pharmacy/wp-content/uploads/2024/08/MPJE-Fact-Sheet.pdf).
- MA [Board licensure/practice resources](https://www.mass.gov/lists/pharmacy-practice-resources), [247 CMR 9](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download), [2026 Board policy list](https://www.mass.gov/lists/pharmacy-board-policies), [Mass General Laws c.94C](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXV/Chapter94C).
- External public comparison: [UWorld sample](https://pharmacy.uworld.com/mpje/sample-questions/), [PharmLaw MA](https://www.pharmlaw.com/courses/massachusetts-mpje-prep), [PharmacyExam MA](https://www.pharmacyexam.com/massachusetts-mpje), [Exam Master MA](https://shop.exammaster.com/massachusetts-mpje-study-resources).
- Independent research: [AJPE Pre-MPJE predictor](https://pubmed.ncbi.nlm.nih.gov/34785499/); [MPJE blueprint trends 2026](https://pubmed.ncbi.nlm.nih.gov/42637086/).

*Research-level recommendations based on sources accessible November 18, 2026; no psychometric validation, live legal-professional certification or ability-to-pass guarantee.*
