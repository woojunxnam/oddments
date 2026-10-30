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

`RELEASED` question은 current-hash independent legal `KEEP`/answer `YES`와 full-bank realism `KEEP`/`PASS` evidence, 그리고 final `KEEP` adjudication을 통과한 항목입니다. 나머지 41개는 release되지 않은 상태입니다. 이번 MOR/Discipline 연습판 개정은 canonical 439개와 기존 감사·release 상태를 변경하지 않습니다. `HOLD` rule은 question 근거로 사용할 수 없습니다.

`MA-Q-0028`은 current-hash realism distinctness failure 이후 quarantine 상태이며 release되지도 preview되지도 않습니다.

## Canonical pipeline

```text
PERMITTED PUBLIC SOURCE
        -> ABSTRACT SIGNAL (optional; no source question text)
        -> VERIFIED OFFICIAL RULE
        -> FRESH SCENARIO + FRESH DISTRACTORS
        -> AUTOMATED QA
        -> GPT LEGAL AUDIT
        -> CLAUDE LEGAL AUDIT
        -> INDEPENDENT REALISM REVIEW
        -> FINAL HUMAN/EDITOR KEEP ADJUDICATION
        -> RELEASED OUTPUT
```

Commercial/recalled question을 paraphrase해 public question으로 만드는 경로는 금지됩니다. 자세한 기준은 [Source Use Policy](docs/SOURCE_USE_POLICY.md)를 참조하십시오.

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

노트 원본과 편집 기록은 [`notes/`](notes/README.md), 생성 스크립트는 `scripts/build_ultimate_notes.py`입니다. 기존 question/rule/drug registry와 release gates는 변경하지 않습니다.

## 온라인 연습문항 — 전체 2,342개, 기본 목록 438개

[웹 연습판](https://woojunxnam.github.io/oddments/practice-expansion/)의 현재 구성은 **원본 2,176 + MA-REV 96 + MA-RW 70 = 2,342문항**입니다. 기본 목록은 438개이며 개정 사례를 우선 연결합니다. [사례형 1,152문항만](https://woojunxnam.github.io/oddments/practice-expansion/?bank=plus) 또는 다른 묶음을 선택할 수 있습니다. 영어 문제와 선택지, 한국어 선택지별 해설, 통합노트 연결, 20문항 연습·120문항 시간 연습·완전 랜덤10·오답·북마크·기록 백업을 지원합니다.

2026-10-30 MOR/Discipline 단위는 원본 32개·128개 선택지의 기록과 별도 ID 사례 8개를 반영합니다. 전체검토 추적표의 누적 기록은 81개 ID(보류 포함), 개별 재검증 미기록은 2,261개입니다. 원본 1,024개 구조검사는 법규 검토 수와 별도입니다. 원래 대표 355개는 새 ID 재작성 70 / 기존 사례 통합 3 / 보류 10 / 개선 미반영 272입니다. [현재 범위](site/practice-expansion/quality-review.html), [검토 진행](reports/full-corpus-review/progress.json), [이번 구현·검증 기록](docs/MOR_DISCIPLINE_20261030.md)을 참조하세요.

새 묶음은 128개 판단 모델을 각각 9개 조건으로 확장한 연습입니다. 1,152개의 독립 법규 또는 실제 기출을 의미하지 않습니다. 공개 NABP 형식 예시와 합법적인 공개 샘플을 비교했으며, 비공개 기출·응시자 복원·Pre-MPJE 문항은 사용하지 않았습니다. [조사·설계 기록](practice_expansion/2026-10-26-plus/research/RESEARCH_KO.md), [신규 원본](practice_expansion/2026-10-26-plus/README_KO.md)을 확인하세요.

`PUBLISHED_PRACTICE`는 온라인 이용 가능 상태입니다. 문항별 독립 법규·현실성 검토 완료를 뜻하지 않으며, canonical `RELEASED`의 감사·판정 기록은 바꾸지 않습니다. 원본 2,176개·MA-REV96개·기존 공개 MA-RW62개의 내용과 학습 기록을 보존했습니다. 통합노트는 보호 원본과 과거 판본을 보존한 versioned overlay로 개정합니다. [공개 정책](docs/PRACTICE_PUBLICATION_POLICY.md).

## Daily Refresh · RA→약국 복귀

[복습 카드](https://woojunxnam.github.io/oddments/notes/#refresh), [오늘 10장](https://woojunxnam.github.io/oddments/notes/#refresh/today), [복귀 학습 7단계](https://woojunxnam.github.io/oddments/notes/#return), [기초 용어](https://woojunxnam.github.io/oddments/notes/#glossary)를 통합노트에 추가했습니다. 기초·실무 72장, 기존 약물 부록 127장, 장별 개요 33장과 용어 45개를 연결합니다. 랜덤·주제별·저장한 카드·자기평가 복습, 기록 백업과 전 페이지 맨 위/홈/복습 카드 이동을 지원합니다.

기존 본문·질문·학습 기록은 보존합니다. 카드 자기평가는 합격 예측이나 임상 역량 인증이 아니며 원문의 미해결·시행일 주의 표시를 유지합니다. [내용·구현·검증 경계](docs/REFRESH_CARDS_REVIEW.md)를 확인하세요.
