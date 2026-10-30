# Massachusetts MPJE Study System

이 저장소는 Massachusetts MPJE 학습·감사 시스템의 canonical source of truth입니다. 웹사이트와 향후 PDF는 `data/`에서 생성되는 output이며 독립적인 권위가 아닙니다.

## Content status

아래 수치는 현재 canonical tree에서 직접 계산한 실측값입니다.

- semantic version/hash가 있는 rule 528개(공식 근거 verified 523개, `HOLD` 5개)와 drug 66개
- version/hash가 고정된 pre-2027 blueprint와 `MPJE-MA-PRE2027` style profile
- canonical question 439개: `RELEASED` 398개, `AUDIT_PENDING` 40개, `REVIEW_REQUIRED` 1개
- `RELEASED` question의 Area 분포: Area 1 = 87, Area 2 = 131, Area 3 = 100, Area 4 = 80
- question family matrix와 별도로 관리하는 candidate·planned family
- public preview allowlist와 release gate
- fail-closed schema·validator·audit·release gate
- question-family matrix와 source-governance boundary
- deterministic static quiz-site skeleton

`RELEASED` question은 current-hash independent legal `KEEP`/answer `YES`와 full-bank realism `KEEP`/`PASS` evidence, 그리고 final `KEEP` adjudication을 통과한 항목입니다. 나머지 41개는 release되지 않은 상태입니다. 이번 Discipline/CDTM 연습판 개정은 canonical 439개와 기존 감사·release 상태를 변경하지 않습니다. `HOLD` rule은 question 근거로 사용할 수 없습니다.

`MA-Q-0028`은 current-hash realism distinctness failure 이후 quarantine 상태이며 release되지도 preview되지도 않습니다.

## Canonical pipeline

```text
PERMITTED PUBLIC SOURCE
        -> ABSTRACT SIGNAL (optional; no source question text)
        -> VERIFIED OFFICIAL RULE
        -> FRESH SCENARIO + FRESH DISTRACTORS
        -> AUTOMATED QA
        -> FRESH INDEPENDENT INSTANCE: LEGAL VERIFICATION
        -> INDEPENDENT REALISM REVIEW
        -> FINAL HUMAN/EDITOR KEEP ADJUDICATION
        -> RELEASED OUTPUT
```

Commercial/recalled question을 paraphrase해 public question으로 만드는 경로는 금지됩니다. 자세한 기준은 [Source Use Policy](docs/SOURCE_USE_POLICY.md)를 참조하십시오.

현재 실행 설정은 독립 auditor instance 1개의 current-hash 법률·현실성 감사와 최종 adjudication을 요구하며 특정 model vendor 조합을 강제하지 않습니다. `SOURCE_USE_POLICY.md`와 `QUESTION_AUTHORING_STANDARD.md`의 역사적 GPT/Claude 도식은 이 설정과 다릅니다. [현재 적용 기준과 문서 충돌](docs/ARCHITECTURE.md#audit-integrity)을 확인하세요. 작성자·같은 팀의 교차 검토를 독립 감사로 계산하지 않습니다.

## Local validation

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_all.py
python -m pytest -q
```

tracked generated artifact를 갱신하려면 다음 명령을 사용합니다.

```bash
python scripts/generate_artifacts.py --write
```

CI는 재생성 후 `git diff --exit-code`를 실행하므로 `duplicate_report.json`, `answer_distribution_report.json`, `site/generated/questions.json`의 drift를 허용하지 않습니다.

development fixture site data는 명시적으로만 생성합니다.

```bash
python scripts/build_site_data.py --include-fixtures
python -m http.server 8000 --directory site
```

`--include-fixtures`를 생략한 release build에는 모든 release gate를 통과한 `RELEASED` question만 포함됩니다. 빈 release payload는 `NO_RELEASED_QUESTIONS`이며 안전하다는 뜻으로 표시되지 않습니다.

Release build는 기본적으로 실행일을 target exam date로 사용합니다. Historical pre-2027 output을 의도적으로 검증할 때만 `--target-exam-date YYYY-MM-DD`를 지정할 수 있습니다. 2027-03-01 이후 target에 pre-2027 blueprint/profile을 사용하면 `BLUEPRINT_REVIEW_REQUIRED`로 실패합니다.

관련 문서: [Architecture](docs/ARCHITECTURE.md), [Question Authoring Standard](docs/QUESTION_AUTHORING_STANDARD.md), [Audit Workflow](docs/AUDIT_WORKFLOW.md), [Release Policy](docs/RELEASE_POLICY.md).

## Week 1–6 통합 노트

메인 페이지의 **Ultimate Notes · 통합 노트** 버튼에서 한국어 주제별 상세 학습판을 읽을 수 있습니다. 33개 주제·306개 상세 절·127개 약물/제형 항목, 검색·북마크·읽음 표시·이어 읽기·모바일·인쇄를 지원합니다. 출처의 확인일, 편집적 통합, 미해결 경계는 구별합니다. 독립 감사된 RELEASED question과 동일한 검증 상태로 표시하지 않습니다.

2026-10-30 Discipline/CDTM 개정은 `w1-c-14`, `w1-c-15`, `w4-d-17`, `w3-d-2`, `w3-d-3`, `authority-paths`의 6개 절과 미해결 사항 색인 `w6-b-17`을 반영합니다. 징계 사유·절차, waiver, CDTM 자격·권한 경로의 조건과 예외를 설명하고 학습 요약 3개와 복습 카드 1개를 함께 갱신했습니다. 상세 절에서 **관련 문제 풀기 / 이 절의 오답 복습**으로 이동할 수 있으며 문항의 실제 `note_evidence` 절 ID로 연결합니다. 연결이 있다는 사실은 해당 절 또는 문항의 법규 검증 완료를 뜻하지 않습니다.

누적 14개 절에서 제한된 claim 검토를 기록했고, 15개 절에 versioned edit가 있습니다. 확인한 claim/claim cluster는 52개(작성자 근거 확인 48, 미해결 4)이며 306개 절의 전체 법률 주장 전수 검토는 미완료입니다. 노트 원본과 편집 기록은 [`notes/`](notes/README.md), 생성 스크립트는 `scripts/build_ultimate_notes.py`입니다. 기존 question/rule/drug registry와 release gates는 변경하지 않습니다.

## 온라인 연습문항 — 전체 2,346개, 기본 목록 438개

[웹 연습판](https://woojunxnam.github.io/oddments/practice-expansion/)의 현재 source 구성은 **원본 2,176 + MA-REV 96 + MA-RW 74 = 2,346문항**입니다. 기본 목록은 438개이며 개정 사례를 우선 연결합니다. [사례형 확장 묶음 1,152문항](https://woojunxnam.github.io/oddments/practice-expansion/?bank=plus) 또는 다른 묶음을 선택할 수 있습니다. 영어 문제와 선택지, 한국어 선택지별 해설, 통합노트 연결, 20문항 연습·120문항 시간 연습·완전 랜덤10·오답·북마크·기록 백업을 지원합니다. 시간 연습은 공식 adaptive scoring이나 합격 예측을 재현하지 않습니다.

### 수치의 정의

| 수치 | 의미 |
|---|---|
| 2,176 | 기존 1,024개 + 128개 판단 모델을 9개 조건으로 확장한 1,152개; 후속 MA-REV/MA-RW 제외 |
| 2,328 | 과거 baseline `9f3fed1`의 2,176 + MA-REV 96 + 당시 MA-RW 56 |
| 2,346 | 현재 공개 연습판 source 전체 ID 수; 기본 우선 목록 438개는 이 안의 부분집합 |
| 480 | 현재 전체 연습판에서 고유한 family ID 수; 독립 법규 또는 독립 사례의 수가 아님 |
| 33 / 306 | 통합노트의 주제 / 상세 절 수; 문항묶음이나 family 수와 다른 차원 |
| 439 / 398 | 별도 canonical corpus의 전체 / `RELEASED`; 공개 연습문항 합계와 합산하지 않음 |
| 226 | 과거 canonical corpus의 수치; 현재 canonical 수나 공개 연습문항 총수가 아님 |

1,152개 확장 문항은 1,152개의 독립 법규 또는 실제 기출을 뜻하지 않습니다. 전체의 독립 사례·독립 법규 판단 수에 대한 전수 판정은 아직 수행하지 않았습니다. 실제 파일별 집계는 [inventory definitions](reports/full-corpus-review/inventory-definitions.json)를 확인하세요.

### 현재 품질 개선 범위

2026-10-30 Discipline/CDTM 배치는 **40개 ID·163개 선택지**를 검토했습니다. 원본 `MA-EXP-0209`–`0240` 32개, 이미 공개된 `MA-RW-0025`–`0028` 4개, 새 사례 `MA-RW-0077`–`0080` 4개를 구분합니다. 기존 CDTM 개정판 4개는 재검토해 유지했으며 새 문항으로 중복 계산하지 않습니다. 원본 32개 판정은 경미한 편집 개선 23, 대표 교체 8(기존 CDTM 교체 4 포함), 대폭 재작성 필요 1입니다. 경미한 개선 대상으로 분류한 원본 23개는 아직 수정 완료가 아닙니다.

Waiver 원본 `MA-EXP-0223`의 잘못된 정답과 `0224`의 단일 정답 모호성을 기록하고, 관련 해설·적용 관계 문제가 있는 원본을 포함해 이번 배치 9개 ID에 주의를 표시합니다. 기본 목록에서는 검토된 개정 사례를 연결하며 원본 ID와 기록은 보존합니다. 모든 선택지를 검토한 기록은 정답이 모두 정확하다는 인증이 아닙니다.

전체 추적표의 누적 검토 기록은 **121개 ID**(조건부·보류 포함), 개별 재검증 미기록은 **2,225개**입니다. 법규 상태는 작성자 근거 확인 65 / 조건부 확인 46 / 근거 관계 보류 10으로 구분합니다. 이번 40개 ID에는 10개 기준의 편집 평가를 남겼지만 점수로 독립 감사나 release를 인증하지 않습니다. 원본 1,024개 구조검사는 법규 검토 수와 별도입니다. 원래 대표 355개는 새 ID 재작성 74 / 기존 사례 통합 3 / 보류 10 / 개선 미반영 268입니다.

[공개 품질 현황](https://woojunxnam.github.io/oddments/practice-expansion/quality-review.html), [검토 진행](reports/full-corpus-review/progress.json), [최신 구현·QA·배포 checkpoint](docs/MPJE_QUALITY_CHECKPOINT.md)를 참조하세요. PR/CI/배포 상태는 정확한 commit과 실행 결과가 확인된 checkpoint를 따릅니다.

외부 학습 사이트는 source-use permission을 먼저 확인합니다. 이번 Castleport·OpenExamPrep·PreMPJE.com 조사는 약관 확인 단계이며 질문 본문 비교, 문항 복제, AI 입력 사용 허용은 확인되지 않아 `HOLD`로 남겼습니다. 이 사이트들의 문항 비율·coverage를 분석 완료했다고 계산하지 않습니다. NABP의 비공개 Pre-MPJE·실제 기출·응시자 복원 문항은 사용하지 않습니다. [이번 외부 자료 확인 범위](reports/full-corpus-review/external-source-review.json), [기존 확장 묶음 설계 기록](practice_expansion/2026-10-26-plus/research/RESEARCH_KO.md)을 확인하세요.

`PUBLISHED_PRACTICE`는 온라인 이용 가능 상태입니다. 문항별 독립 법규·현실성 검토 완료를 뜻하지 않으며 canonical `RELEASED`의 감사·판정 기록은 바꾸지 않습니다. 이번 배치는 원본 2,176개·MA-REV 96개·기존 공개 MA-RW 70개의 내용과 학습 기록을 보존했습니다. 통합노트는 보호 원본과 과거 판본을 보존한 versioned overlay로 개정합니다. [공개 정책](docs/PRACTICE_PUBLICATION_POLICY.md).

## Daily Refresh · RA→약국 복귀

[복습 카드](https://woojunxnam.github.io/oddments/notes/#refresh), [오늘 10장](https://woojunxnam.github.io/oddments/notes/#refresh/today), [복귀 학습 7단계](https://woojunxnam.github.io/oddments/notes/#return), [기초 용어](https://woojunxnam.github.io/oddments/notes/#glossary)를 통합노트에 추가했습니다. 기초·실무 72장, 기존 약물 부록 127장, 장별 개요 33장과 용어 45개를 연결합니다. 랜덤·주제별·저장한 카드·자기평가 복습, 기록 백업과 전 페이지 맨 위/홈/복습 카드 이동을 지원합니다.

기존 본문·질문·학습 기록은 보존합니다. 카드 자기평가는 합격 예측이나 임상 역량 인증이 아니며 원문의 미해결·시행일 주의 표시를 유지합니다. [내용·구현·검증 경계](docs/REFRESH_CARDS_REVIEW.md)를 확인하세요.
