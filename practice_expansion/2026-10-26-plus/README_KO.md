# MA MPJE Casebank Plus — 2026-10-26

**신규 1,152문항 · 기존 1,024문항 보존 · 온라인 합계 2,176문항**

[신규 묶음만 풀기](https://woojunxnam.github.io/oddments/practice-expansion/?bank=plus) · [전체 연습](https://woojunxnam.github.io/oddments/practice-expansion/)

## 실제 구성과 의미

| 구성 | 모델 | 모델당 변형 | 문항 |
|---|---:|---:|---:|
| 단일 사례·기록·기한 계산 | 38 | 9 | 342 |
| 독립 업무 기록 중 적절한 행동 하나 고르기 | 50 | 9 | 450 |
| 복수선택: 각 행동의 조건을 독립 판단 | 40 | 9 | 360 |
| 합계 | 128 | 9 | 1,152 |

792 SBA와 360 SATA이다. **1,152개의 서로 무관한 법규·독립 사례 또는 실제 기출을 뜻하지 않는다.** 동일 모델의 숫자·기한·행동 조건을 바꾸는 반복 학습이 포함된다. 업무 기록형 문항에서는 질문 안내가 반복되며 실제 판단 사실은 선택지에 있다. 세트는 모델(family)당 한 문항을 선택하지만 같은 주제의 다른 모델까지 배제하는 것은 아니다.

기존의 Case A/Case B를 함께 보여주고 한 사례만 묻는 구조 대신, 새 문항은 한 사례를 적용하거나 동일 업무 영역의 별도 행동들을 판단한다. 영어 문제·선택지, 한국어 핵심·선택지별 해설, 정확한 통합노트 절과 public source links를 유지한다.

## 범위

현재 2027-03-01 이전 MPJE 영역에 잠정 배정: 면허·인력252, 약사 업무378, 조제279, 운영243. 이는 편집상 배분이며 최근 시험의 실제 빈도나 NABP의 문항 형식 비율이 아니다. 2027 새 outline 및 UMPJE와 구분한다.

38개 단일 사례 모델에는 CE·scope·renewal·CDTM·투약 자격·처방기간·부분조제·refill·EPCS·재고·stock ordering·PPPA·MIIS·CQI 및 최근 확인된 공급/EM 규칙이 포함된다. 320개 source-linked 행동쌍을 이용해 업무 기록형/복수선택의 조합을 생성한다. 이름만 바꾸거나 보기 순서만 바꾼 것을 새 문항으로 세지 않는다. 반복되는 원리 자체를 새로운 법규라고 주장하지 않는다.

## 출처와 검토 경계

통합노트 `notes/guide.json`의200개 절, 관련161개 참고문헌을 연결한다. 노트 확인일을 오늘로 덮어쓰지 않았다. 오늘 다시 읽은 primary source의 범위는 `primary_source_read_records`에 따로 기록하며, 문항별 독립 검토 증명서가 아니다. 새로 확인한 §1306.07(f)의45일 direct-delivery 조건은 추가 primary evidence로 구별한다.

비공개 actual exam·Pre-MPJE·응시자 복원·덤프·유료 문제은행 원문은 사용하지 않았다. 현재 연결된 NABP 공개 sample은 형식 예시이지 최근 시험 출제내역이 아니다. 공개 UWorld 샘플에서는 추상적 구조만 비교했다. 원문→바꿔쓰기 방식으로 새 문항을 생성하지 않았다.

미확인 HIV/STI clinical DOCX의 세부 알고리즘, 충돌하는14/30일 emergency-continuity 경계, 일부MOR/보고/packaging 경계값, 미래 시행 프로그램의 세부 workflow는 임의의 확정 정답으로 채우지 않는다. 연결된 장의 OPEN이 보이더라도 이 작업이 그 장 전체를 재검증했다는 뜻은 아니다.

`PUBLISHED_PRACTICE`는 사용자 요청에 따른 온라인 학습 공개 상태이다. `NOT_INDEPENDENTLY_REVIEWED`와 미보정 난도 상태는 그대로 유지한다. 기존 canonical `RELEASED`·감사·adjudication을 위조하거나 바꾸지 않는다. 합격 보장이나 공식 CAT·scaled score가 아니다.

## 재생성·검사

```bash
python practice_expansion/2026-10-26-plus/scripts/build_casebank.py --check
python -m pytest tests/test_casebank_plus.py tests/test_practice_expansion_integration.py -q
python scripts/publish_practice.py --output public-site
python scripts/verify_public_practice.py --site public-site
```

`authoring/atoms.py`와`authoring/cases.py`는 작성 원천, `questions.json`은 deterministic output이다. `research/RESEARCH_KO.md`는 조사 범위와 제외 사항, `reports/quality-diagnostics.json`은 자동 품질 진단이다. 정확한 question+choices 중복검사는 의미상 전수 감사와 다르며, lexical similarity 점수는 실전 난도·정확성 점수가 아니다.
