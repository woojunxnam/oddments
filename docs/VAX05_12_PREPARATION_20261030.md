# VAX05–12 검토·새 사례형 Draft — 준비 브랜치 (NOT MERGED)

2026-10-30. 기준 main: PR #179 배포 판본. 이 문서는 PR #180이 병합되기 전 준비 작업의 정확한 경계다.

## 실제 범위

- `MA-EXP-0305–0336` 원본 **32 ID / 128 선택지**.
- 기존 `MA-RW-0045–0048`은 VAX05–08의 **4 ID / 17 선택지**.
- **합계 36개의 기존 question ID / 145개 선택지**에 원본 full-record hash, choice-by-choice 법규 근거 및 한국어 해설, answer-key crosscheck, 10기준 편집점수 기록을 `reports/full-corpus-review/vax05-12-author-review.json`에 보관한다.
- VAX09–12에는 MA-RW 별도 개정판이 **없다**. MA-RW-0049–0052는 다른 family(일부 PER)에 속하므로 VAX09–12 개정판으로 오인하지 않는다.
- 기존 키의 명백한 충돌을 이번 좁은 공식 규정과의 대조에서 발견하지 않았으나 **법규 독립 감사·psychometrics·재배포 인증은 없다**.
- `MA-EXP-0319` 및 `MA-EXP-0335`의 SATA 전부 정답 구조는 **distractor 부재**로 사례형 major-rewrite 우선 후보. 이 사실이 wrong key 확정을 의미하지 않는다.

## 제안 신규 사례 4개

Draft-only JSON `reports/full-corpus-review/vax09-12-four-case-candidates.json`. 영어 지문·A-D와 선택지별 한국어 설명 포함, 모두 기존 원본과 다른 구체적 상황으로 구성:

| Draft | 주제 | 핵심 판단 |
|---|---|---|
| VAX09-CANDIDATE-01 | VIS prior to administration | 사후 영수증과 함께 VIS를 제공해도 사전제공 의무를 대체하지 못함 |
| VAX10-CANDIDATE-01 | MIIS pre-review / dose report | Flu pre-review exception은 administered dose reporting exemption이 아님 |
| VAX11-CANDIDATE-01 | MIIS clocks | 접종 **72h from administration** vs data-sharing objection **24h from receipt** |
| VAX12-CANDIDATE-01 | MIIS objection / access | Data-sharing objection과 required Department submission 분리, curiosity access 금지 |

**주의:** Draft ID는 released `MA-RW` ID가 아니다. `publication_status=DRAFT_ONLY_NOT_IN_ACTIVE_OR_CANONICAL_BANK`를 유지한다. 독립적 법규·realism 심사, 사례 의미중복 검색, 실제 자료 개정일 확인 후 **새 안정적 ID**와 별도 이력 정책으로만 승격한다.

## 공식 법규

- [DPH/Board Policy 2023-02](https://www.mass.gov/doc/2023-02-vaccine-administration-pdf/download), 2025-09-04 revised: vaccinator CE·training·prescriber standing order·VIS·MIIS
- [105 CMR 222 MIIS](https://www.mass.gov/doc/105-cmr-222-massachusetts-immunization-information-system/download), 2024-08-16: §§222.100, 222.105, 222.205
- [MIIS Mass.gov 설명](https://www.mass.gov/info-details/about-the-massachusetts-immunization-information-system-miis)

## 연결 UI

`site/notes/vax05-12.html`은 실제 원본 32개 및 기존 개정판 4개 링크, 4개 신규 미작성 주제 경고, 공식 출처 링크를 제공하는 정적 보조 페이지다. 아직 배포된 것이 아니며 독립감사/해당 절 전수 법규 검증의 증거가 아니다.

## 후속 release 조건

1. PR #180 통과·main 병합·Pages 실측을 먼저 확인한다.
2. 이 준비 브랜치의 3개 파일과 QA 테스트를 해당 최신 main에서 새 branch에 가져온다. 동시 변경과 provenance hashes를 대조한다.
3. `build_full_corpus_review.py`에 36개 ID만 신규 등재; 예상 누적 201→237 reviewed, 2145→2109 unreviewed. **아직 공식 완료 숫자가 아니다**.
4. New 4 question drafts는 독립 검증 전 공개 연습문항으로 추가하거나 new MA-RW count에 포함하지 않는다.
5. Full CI, 원본 보호, browser/notes QA, 공개 origin 일치 후에만 merge·deploy 완료를 주장한다.
