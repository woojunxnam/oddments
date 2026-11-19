# Massachusetts MPJE — Part D Gap-First 120-Question Research Roadmap

> **최신 Wave 3 종료 (2026-11-18)** — **Part D 60/120 영어 초안 작성**, 이번 **D041–D060 20문항은 공식 법령의 저자 검토·A–D 80개 선택지 확인 후 `AUTHOR_LEGAL_ACCEPTED` 처리**. W1/W2 이전 40개는 아직 저자 최종 법령 승인이 아닌 1차 출처 검토 단계. **Public exam 법령 frozen 승인 0/120, GitHub Pages 배포 0**. A/B/C 360문항 실지문과 W1/W2 40문항 대비 중복 지문 0개이나 의미적 중복 자체의 독립 보증은 아님. [W3 전체 법령·신규성 보고서](part-d/w3-source-and-legal-approval-review-2026-11-18.md) · [20문항 법령 승인대장](part-d/w3-author-legal-approval-2026-11-18.json) · [QA](part-d/w3-author-qa-2026-11-18.json).


> **최신 현황 — 2026-11-18 Wave 2 종료:** Part D **40/120 신규 초안 작성**, W2 D021–D040 **20문항·80개 해설, 공식 출처 1차 검토 및 360문항+W1 중복 검사 완료**. **최종 법령 frozen 승인 0/120, 공개 배포 0.** [W2 상세 보고서](part-d/w2-source-and-novelty-review-2026-11-18.md) · [W2 QA](part-d/w2-author-qa-2026-11-18.json) · [선택지별 법령 검토 대장](part-d/w2-per-option-source-gates-2026-11-18.json). 아래 초기 설계 당시의 0/120 및 W1의 20/120 표기는 당시 시점의 기록으로만 해석한다.


> **Wave 1 작성 현황 — 2026-11-18**: 연구 계획을 실행해 **D001–D020 20문항 초안, 선택지 80개 해설, 공식 1차 출처 검토, 구조 QA**를 저장함. **Part D 20/120 작성, 0/120 법령 최종 frozen 승인, 0 배포.** 가장 중요한 반복 위험이었던 `D016`은 개인반입/재판매 문제에서 **상업용 FDA import entry notice + bond**로 대체. [W1 검토 보고서](part-d/w1-source-and-novelty-review-2026-11-18.md) · [W1 QA](part-d/w1-author-qa-2026-11-18.json) · [W1 선택지별 법령 근거](part-d/w1-per-option-source-gates-2026-11-18.json). 아래 기존 '0문항' 설명은 로드맵 작성 당시의 역사적 기준임. 시험 기능에는 추가되지 않았음.


**작성일:** 2026-11-18 · **자료:** `main`의 기존 A/B 240문항 + Draft PR #281의 Form C 120문항 초안, 공식 NABP 2027 outline 및 Massachusetts/DEA/FDA 자료.  
**상태:** **로드맵만 작성. Part D 실제 문제 0/120, 법령별 최종 정답 승인 0/120, 배포 0/120.**  
**사용자 지시:** A/B/C와 같은 스타일·동일 결론을 반복하지 않고, **새로운 법률 판단과 미검증·취약 규정을 최대한 많이** 시험한다.

## 결정

**Part D는 NABP의 대표 비율을 복제하는 모의시험이 아니라 `Gap Stress Test`로 정의한다.** 이 설계는 강점 재시험을 최소화하고, 상대적으로 적게 검토한 법령의 위험을 의도적으로 증폭한다. 이 때문에 D 점수 85~90%를 표준 MPJE 합격 예측률로 해석하지 않는다.

- 2027 공식 scored-domain 비중: **30/30/20/20** (120문항 교육용 단순비례 시 36/36/24/24). 이 120은 실제 MPJE에서 전부 채점되는 문항이라는 뜻이 아니다.
- Part D 의도적 결손 집중: **32/24/36/28**, D3 법령·DEA 및 D4 운영을 추가 배정. 시험일이 **2027-03-01 이전이면** 새 outline이 아닌 종전 Competency Statements에 매핑을 다시 해야 한다.
- **120개 개별 법적 판단 슬롯(D001–D120)**: 30개의 미세 주제 × 4개의 다른 법적 결론 후보. 아직 시험문항/정답은 아니다.
- 목표: **최소 96/120**이 A/B/C에서 직접 평가하지 않은 규칙, 예외 또는 새로운 legally decisive condition. 나머지 최대 24문항도 연방·주법 충돌 또는 기존 결론을 바꾸는 실질적 transfer이어야 한다. 단순 약물명·장소·날짜 변경, 같은 정답의 반복은 **0** 허용. 96/120은 **목표**이며 현재 검증 성과가 아니다.
- 원칙: 기존 문제에 법률적 결론이 겹치거나 최신 원문에서 단독 정답이 확인되지 않으면 우선 슬롯을 대체한다. 문항 수 목표 때문에 근거 부족 문제를 포함시키지 않는다.

## 360문항 기초조사 — 근거 수준 구분

- A/B: 총 **240문항**, `questions.js` 본문 확인.
- C: Draft PR #281의 17개 파일에서 **120개 초안 슬롯** 확인; **0개 최종 법령 승인**.
- 신규 D120: 실제 360개 기존 지문+선택지와 **lexical nearest-neighbor** 비교 수행, 후보별 가까운 4개 기존 ID를 matrix에 기록. 이는 **최종 의미·법률 중복 검사가 아니다**.
- 이전 전체 지문·보기의 용어 검색에서 **counterfeit/EUA/importation 0**, adulterated/misbranded 2, cyber/ransomware 1, DEA Form 222/CSOS/POA 약 6, 환경 모니터링 관련 4 정도가 나왔으나, 이는 *term match*이지 교육 내용의 의미적 0개라는 결론이 아니다. 최종 작성 전에 기존 360문항의 **법적 판단 (actor/action/setting/timing/exception)**을 일일이 비교해야 한다.

### 분야별 배분

| 2027 Domain | 새 outline 비례 120 환산 | D 집중 배분 | 추가·취약 방향 |
|---|---:|---:|---|
| 1 | 36 | **32** | 제품상태/EUA/DSCSA/수입, USP 797/800 운영, 자동 비멸균조제 |
| 2 | 36 | **24** | 낯선 Rx 기록, 새로운 drug schedule/formulation, Orange/Purple Book, repackaging, administration·AE |
| 3 | 24 | **36** | DEA POA·Form222·CSOS, inventory, theft/loss, disposal, DPH/Board/DEA reporting |
| 4 | 24 | **28** | 시설 양도/폐업/비거주·503B, EPCS·cyber, automated dispensing, cold chain·shipping |
| **합계** | **120** | **120** | 실제 출제비율을 추정하려는 배분이 아님 |

### 30개 세부 주제와 확정 연구 슬롯

**중요:** 아래는 **문제 소재·법적 판단 후보**, 정답 승인·법령 적용 확정이 아니다. 상세 각 120개의 질문 목표, 기존 근접 ID, 공식-source leads는 [Part D 120-slot JSON](MPJE_PART_D_GAP_FIRST_120_SLOTS_2026-11-18.json)에 보존했다.

| # | Domain | Subdomain | 새로 조사할 세부 쟁점 | Slots | 우선도 |
|---:|---:|---|---|---|---|
| 01 | 1 | 1.C | Adulteration and misbranding boundaries | D001, D002, D003, D004 | CRITICAL |
| 02 | 1 | 1.C | DSCSA suspect and illegitimate product decisions | D005, D006, D007, D008 | CRITICAL |
| 03 | 1 | 1.C | FDA EUA status and authorized use | D009, D010, D011, D012 | HIGH |
| 04 | 1 | 1.C | Importation and unapproved products | D013, D014, D015, D016 | HIGH |
| 05 | 1 | 1.D | NIOSH OSHA and regulatory standard hierarchy | D017, D018, D019, D020 | HIGH |
| 06 | 1 | 1.E | USP 797 environmental monitoring action levels | D021, D022, D023, D024 | CRITICAL |
| 07 | 1 | 1.E | USP 800 hazardous-material edge operations | D025, D026, D027, D028 | CRITICAL |
| 08 | 1 | 1.D/1.E | Automated 503A nonsterile compounding quality | D029, D030, D031, D032 | CRITICAL |
| 09 | 2 | 2.A.1-3 | Unfamiliar prescription-document defects | D033, D034, D035, D036 | HIGH |
| 10 | 2 | 2.B.3/2.B.7 | Formulation-specific real-drug classification | D037, D038, D039, D040 | HIGH |
| 11 | 2 | 2.B.9 | Orange Book and biologic evidence extraction | D041, D042, D043, D044 | HIGH |
| 12 | 2 | 2.B.1/2.B.4 | Manufacturer labeling and repackaging | D045, D046, D047, D048 | HIGH |
| 13 | 2 | 2.B.8 | Special return and donation pathways | D049, D050, D051, D052 | HIGH |
| 14 | 2 | 2.C | Medication administration and adverse-event reporting | D053, D054, D055, D056 | CRITICAL |
| 15 | 3 | 3.B.4 | DEA registration and Power of Attorney | D057, D058, D059, D060 | CRITICAL |
| 16 | 3 | 3.B.3 | DEA Form 222 and CSOS ordering | D061, D062, D063, D064 | CRITICAL |
| 17 | 3 | 3.B.1/2 | Controlled inventory discrepancy and recordkeeping | D065, D066, D067, D068 | HIGH |
| 18 | 3 | 3.B.5 | Theft loss: federal MA and DCP workflows | D069, D070, D071, D072 | CRITICAL |
| 19 | 3 | 3.B.6 | Controlled medication disposal and reverse distribution | D073, D074, D075, D076 | HIGH |
| 20 | 3 | 3.A.1-2 | Agency powers and inspection responses | D077, D078, D079, D080 | HIGH |
| 21 | 3 | 3.C | Malpractice reporting and discipline edge cases | D081, D082, D083, D084 | HIGH |
| 22 | 3 | 3.B.1-2 | Institutional controlled-substance accountability | D085, D086, D087, D088 | HIGH |
| 23 | 3 | 3.A/3.C | Policy versioning and reporting-jurisdiction conflicts | D089, D090, D091, D092 | HIGH |
| 24 | 4 | 4.A | Pharmacy ownership relocation and closure | D093, D094, D095, D096 | CRITICAL |
| 25 | 4 | 4.A | Nonresident, wholesale and outsourcing facility licenses | D097, D098, D099, D100 | HIGH |
| 26 | 4 | 4.B | Cybersecurity, EPCS and privacy incident response | D101, D102, D103, D104 | CRITICAL |
| 27 | 4 | 4.B | Automation shared service and audit-trail failures | D105, D106, D107, D108 | HIGH |
| 28 | 4 | 4.C | Cold-chain storage and physical product integrity | D109, D110, D111, D112 | HIGH |
| 29 | 4 | 4.D | Delivery custody and failed shipment evidence | D113, D114, D115, D116 | HIGH |
| 30 | 4 | 4.C | Facility access records and disaster recovery | D117, D118, D119, D120 | HIGH |

## 제작 순서: 6개 연구 배치 ×20문항

| Batch | 슬롯 | 후보 수 | 연구 축 |
|---|---|---:|---|
| D-W1 | D001–D020 | 20 | FDA adulteration/misbranding, DSCSA suspect/illegitimate, EUA, importation, NIOSH/OSHA |
| D-W2 | D021–D040 | 20 | USP 797 EM policy 2026-03, USP 800, automated nonsterile devices, unfamiliar prescription and drug schedules |
| D-W3 | D041–D060 | 20 | Orange/Purple Book tables, repackaging, return/repository, administration/adverse reporting, DEA power of attorney |
| D-W4 | D061–D080 | 20 | Form 222/CSOS, perpetual inventory, theft/loss, disposal, inspectors |
| D-W5 | D081–D100 | 20 | malpractice and Board reporting, institutional controlled accounts, proposed vs effective rules, ownership and outsourcing |
| D-W6 | D101–D120 | 20 | EPCS credential incidents, automation, cold-chain logs, delivery custody, facility access/disaster recovery |

**매 배치마다** `READ 360 comparator IDs → CURRENT official law & effective date → WRITE decision → DRAFT four choices → AUDIT all A-D rationales → SEMANTIC DEDUP → HOLD/REPLACE → STRUCTURE QA` 순서로 진행한다. 다른 20개를 먼저 쓰고 검증을 미루는 작업을 금지한다. Batch 순서는 출처 리서치 효율을 위한 것이며 **최종 시험 응시 순서가 아니다**.

## 질문 작성 계약

1. **법적 판단 단위:** `actor + legal action + schedule/product + setting + time + exception + exact authority`를 기록. 변경한 사실이 정답의 법적 결론을 바꾸지 않는다면 원칙적으로 중복으로 폐기.
2. **단일정답/SATA:** 법적 근거가 각 선택지를 지지할 때만 확정. 네 보기의 길이·절대어·정답 위치·장문 전문용어를 자동 검사. 단순 텍스트를 길게 늘려 MPJE 난이도를 흉내 내지 않는다.
3. **증거 자료 중심:** 실제 형식의 처방전, Form 222·POA, inventory ledger, lot/expiry label, FDA Orange/Purple Book, facility inspection CAPA, EM trend, courier receipt, breach log를 활용하되 원문을 과도하게 복제하거나 유료/비공개 시험 문제를 복원하지 않는다.
4. **문항 형식 다양화:** 25% 내외 짧은 사실형, 25% 표/원문 자료 판독, 25% 예외 판정, 25% 복수법률 판정 (제작 목표일 뿐 실전 비율 주장 아님). 문제 제목/Domain/주요 법률 힌트는 응시 전 숨긴다.
5. **모든 해설:** 왜 정답인지, 왜 각 오답이 오답인지, 이 결론을 바꿀 수 있는 decisive fact 한 가지, 연방법/MA authority, 적용 기준일.
6. **특수 source gate:** 원본 현행 USP <795>/<797>/<800>에 접근할 수 없으면 원문이 필요한 BUD 숫자·시설 requirement를 확정하지 않는다. Board 정책만으로 충분한 좁은 주장으로 다시 쓰거나 HOLD.
7. **2026-2027 날짜 gate:** MA Policy **2026-03** EM (adopted 2026-09-03); Policy **2026-01** loss/theft (adopted 2026-03-26); **105 CMR 700 October 2026 proposed amendment is NOT assumed effective**; FDA COVID drug EUA 종료 예정 **2027-06-29**는 실제 시험일에 효력 재확인; DSCSA small dispenser exemption의 **scope/date/eligible entity** 확인.
8. **실제 Form D 별도 풀:** A/B/C manifest, 답 기록, 세트 수, 난이도 분포를 건드리지 않고 별도 versioned pool에서 D 첫 응시 완료 후에만 문항별 답/해설 노출. 기존 Form C 첫 응시 전에 D의 상당수 내용을 공부하면 C의 독립성이 훼손될 수 있으므로 공개 학습 노출 시점을 관리.

## 120개 중복 승인 게이트 (필수)

For every candidate:
- **PRIOR BANK COMPARATOR**: nearest IDs from A/B/C, plus a manual content scan of same regulation; no lexical-only approval.
- **NEW DECISIVE FACT**: old decision versus proposed decision in two short sentences.
- **EXACT SOURCE**: controlling text, provision number, source date, actor/setting, applicable effective date, explicit exception.
- **OPTION VALIDATION**: four choices with primary-source notes; ambiguity check before marking accepted.
- **NOVELTY CLASS**: `NET_NEW_RULE`, `UNTESTED_EXCEPTION`, `MULTI_LAW_TRANSFER`, or `DUPLICATE_REJECTED`.
- **SOURCE STATUS**: `SOURCE_LEAD`, `SOURCE_VERIFIED`, `HOLD`; never label draft as legally frozen.
- **FRESHNESS CHECK**: check 105 CMR updates, Board 2026/2027 changes, FDA/DEA effective dates before any mock release.

If a targeted weak topic is not legally active in Massachusetts or not meaningfully assessable, **replace** it in the same domain with the next verified under-tested 2027 outline item. Do not create imaginary charitable-drug-repository exceptions or infer that a proposed regulation has taken effect.

## Delivery criterion / how to interpret scores

- **Before D:** Complete C120 source signoff, correct the 16 earlier C source/scope holds and B4 C098 hold; keep A/B content and storage stable.
- **D authoring:** 120 uniquely defensible items, 0 duplicate legal decisions, 0 material source holds, no sign-of-answer cues, checked against full 360 bank.
- **D mock use:** 120 questions / 150 minutes may be retained, but its intentional weak-area oversampling means a D score is **not a statistically representative MPJE readiness probability**. Use D **per-skill error diagnosis**, not a standalone percentage.
- **After:** cross-check D misses against official MA/DEA/FDA/USP provisions and targeted remediation; a prior high A/B/C score and D weak-domain diagnostics jointly inform readiness, but never guarantee passing.

## Official sources (starting points, not approval of all 120 claims)

- [NABP 2027 MPJE Content Outline](https://nabp.pharmacy/wp-content/uploads/MPJE-Content-Outline.pdf)
- [NABP MPJE Domain Crosswalk](https://nabp.pharmacy/wp-content/uploads/2026/07/MPJE-Domain-Crosswalk.pdf)
- [Massachusetts 247 CMR code index](https://www.mass.gov/law-library/247-cmr)
- [MA Board Pharmacy Practice Resources](https://www.mass.gov/lists/pharmacy-practice-resources)
- [Board Policy 2026-03: Action Level Environmental Monitoring Results](https://www.mass.gov/doc/2026-03-action-level-environmental-monitoring-results/download)
- [Board Policy 2026-01: Loss or Theft of Controlled Substances](https://www.mass.gov/doc/2026-01-loss-or-theft-of-controlled-substances-pdf/download)
- [Board November 2025 automated nonsterile compounding memorandum](https://www.mass.gov/doc/automated-non-sterile-compounding-devices-pdf/download)
- [247 CMR 6: Licensure of Pharmacies](https://www.mass.gov/doc/247-cmr-6-licensure-of-pharmacies/download)
- [247 CMR 21: Registration of Outsourcing Facilities](https://www.mass.gov/regulations/247-CMR-2100-registration-of-outsourcing-facilities)
- [DEA 21 CFR Part 1305 Order Forms & POA](https://www.ecfr.gov/current/title-21/chapter-II/part-1305)
- [FDA DSCSA for pharmacists](https://www.fda.gov/drugs/drug-supply-chain-security-act-dscsa/pharmacists-utilize-dscsa-requirements-protect-your-patients)
- [FDA EUA drug/nonvaccine biological products and planned termination](https://www.fda.gov/drugs/emergency-preparedness-drugs/emergency-use-authorizations-drugs-and-non-vaccine-biological-products)
- [FDA Orange Book Preface (AB1/AB2 and related ratings)](https://www.fda.gov/drugs/development-approval-process-drugs/orange-book-preface)
- [HHS October 2026 cybersecurity newsletter](https://www.hhs.gov/hipaa/for-professionals/security/guidance/cybersecurity-newsletter-october-2026/index.html)
- [105 CMR 700 — proposal status page](https://www.mass.gov/info-details/105-cmr-700-implementation-of-mgl-c-94c-the-controlled-substances-act)

**Repository action:** Planning documents only. No new executable questions, no merge or GitHub Pages publication. Separate PR deliberately keeps Form C #281 draft and live A/B untouched.


## Wave 1 (D001–D020) 체크포인트 — 2026-11-18

- 신규 FDA/DSCSA/EUA/Importation/NIOSH·OSHA 문항 20개를 GitHub Draft PR에 저장: `docs/part-d/w1-draft-items-001-010-2026-11-18.json`, `w1-draft-items-011-020-2026-11-18.json`.
- 14 SBA + 6 SATA; 정답 A/B/C/D = 4/3/4/3; 지문 300자 미만 14개; 정답이 유일하게 최장 또는 최단인 SBA 0개; 80개 정답·오답 해설 marker 구조 확인; 잘못된 절대표현 shortcut 0개 (구조 QA 기준).
- 특히 E30-108의 일반 adulteration/misbranding, E30-030의 suspect/illegitimate 일반 신고, E30-075의 small dispenser 인원조건, E30-187의 API 성분 적격성 내용과 같은 결정은 반복하지 않도록 설계를 교체했다.
- FDA 2027-06-29 예정 COVID-drug EUA termination은 미래 시행 예정일로만 취급하고, 2026-11-18 현재 즉시 종료로 해석하지 않았다. Part D exam date별 재검증 필수.
- `AUTHOR_SOURCE_CHECK`는 저자 1차 공식자료 검증이지 최종 출제·법령 승인이나 독립적 자문을 의미하지 않는다. 여전히 Part D 문항은 공개 모의시험에 노출되지 않으며 A/B/C 파일은 보존되어 있다.
- **다음:** Wave 2 D021–D040의 Massachusetts 2026 Policy 2026-03 compounding EM, 2025 automated nonsterile device memo, prescription evidence, formulation schedule을 먼저 출처로 확인한 뒤 새 문항 작성. D 전체 완성 후 법률과 보안/저장/채점 시뮬레이션 검사를 거쳐 별도 배포한다.


## Wave 2 (D021–D040) checkpoint — 2026-11-18

- Official source-backed **20 original English questions** added in `docs/part-d/w2-draft-items-021-030-2026-11-18.json` and `w2-draft-items-031-040-2026-11-18.json`.
- Domain 1 **12**, Domain 2 **8**; **13 SBA + 7 SATA**; 13 brief stems (<300 chars); 80 choice explanations; zero single-answer unique-longest or unique-shortest hints and zero wrong-choice absolute cue flags.
- Existing A/B 240, Form C draft 120, W1 20 compared. Full `w2-semantic-nearest-audit-2026-11-18.json` screens exact stems and lexical nearest. **3 substantive duplicate topic changes**: D022=60-day repeat EM + microbiologist (not E30-160 reporting time); D024=pass-through cleaner-space threshold (not nonviable suspension); D033=NDC not federal required vs dosage form required (not E30-199 DEA-number correction).
- Actual regulatory focus: MA Policy 2026-03 environmental monitoring; Board USP <800> community advisory; 2025 Board automated nonsterile memo; 21 CFR 1306/1311; 2026 federal temporary O-DSMT Schedule I; actual products AUVELITY, LIBRAX, VIVITROL/BRIXADI and current state/federal treatment. Full current subscription USP chapter original not separately authenticated, so no claim of entire current USP signoff.
- **Form D is still not playable** and no result history/scoring code is changed. W2 final law signoff pending; C form source approval pending separately.
- **Next** D041–D060 focuses on Orange/Purple Book evidence, product labeling/repackaging, drug return scenarios, medication administration adverse reporting and DEA POA/ordering.


## Wave 3 D041–D060 completion and author legal approval — 2026-11-18

- D041–D060 **20 new English questions** + **80 A–D specific explanations**, official sources checked and `AUTHOR_LEGAL_ACCEPTED` by this author (not independent state Board/legal-professional certification). **Cumulative Part D: 60/120 drafted, 20/120 author legally accepted, 0/120 editorial frozen/published**.
- D2: 16 items, D3: 4; 12 SBA / 8 SATA; 13 brief stems <300 characters; single answer keys A/B/C/D = 2/4/2/4; no uniquely longest/shortest correct, no wrong absolute-word cue or key/rationale alignment error.
- [W3 detailed legal review](part-d/w3-source-and-legal-approval-review-2026-11-18.md), [choice-level ledger](part-d/w3-author-legal-approval-2026-11-18.json), [QA](part-d/w3-author-qa-2026-11-18.json), [full source-bank actual-stem scan](part-d/w3-complete-question-bank-screen-2026-11-18.json) and two draft JSON files under `docs/part-d/`.
- Replaced overlapping decisions (Unithroid multiple AB codes, NDA authorized-generic reporting, Purple Book package details, LTCF PPI exception, MassHealth nursing facility unit-dose returns, reverse distributor 30-day destruction, electronically executed DEA POA). The actual current federal DEA 2026-03-20 POA amendment replaces outdated applicant-signer guidance; incorrectly linked Federal Register PDF was repaired.
- **Important exception**: 2020 FDA 6-month/25% unit-dose repackaging dating is nonbinding enforcement-discretion guidance limited to qualified commercial repackagers. It is not a state pharmacy or compounding BUD. DPH 2026 non-vaccine injection advice distinguishes immediate prescriber communication from circumstance-specific Board reporting.
- Next D061–D080: DEA Form 222/CSOS, controlled inventory records, theft/loss reports, reverse distribution/disposal, inspection. **No Part D public test yet.**
