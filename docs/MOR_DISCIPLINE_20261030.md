# MOR·Discipline 문항과 통합노트 개정 — 2026-10-30

시작 main: `a9e18a4e3281e1184cb28c29e166ec56ba661426`. 작업 PR: [#175](https://github.com/woojunxnam/oddments/pull/175).

이 문서는 구현·검토 범위를 고정한 기록이다. 병합과 공개 배포의 실제 상태는 PR의 최종 head, Pages workflow, 해당 merge commit의 production 회귀 결과를 확인한다. 생성된 `PUBLISHED_PRACTICE` 설정만으로 배포 성공을 주장하지 않는다.

## 실제 변경

| 원본 대표 | 새 ID | 새 판단 사례 | 정답 |
|---|---|---|---|
| MA-EXP-0179 | MA-RW-0069 | 같은 주소·면적의 sterile secondary engineering control 교체와 사전승인 | B |
| MA-EXP-0183 | MA-RW-0070 | 최근 조제했지만 refill이 없는 환자의 폐업 통지 | A |
| MA-EXP-0187 | MA-RW-0071 | Inventory 대상과 closure-transfer 후 stock 보유금지 범위의 차이 | D |
| MA-EXP-0191 | MA-RW-0072 | 현장 약사 휴식 중 unchecked refill·checked new Rx·기술업무 | B, D |
| MA-EXP-0195 | MA-RW-0073 | Independent Board seat의 점포 수와 full-time pharmacist 수 조건 | C |
| MA-EXP-0199 | MA-RW-0074 | 두 연속 임기 후 successor 전 계속 재직과 새 appointment | A |
| MA-EXP-0203 | MA-RW-0075 | MOR 부재 중 on-duty pharmacist의 조사 기록 제공 | D |
| MA-EXP-0207 | MA-RW-0076 | 초기 POC·반려 후7일·서명·실제 시정의 구별 | A, C, D |

원본 MOR07–10의 16개 ID/64선택지와 DISC01–04의 16개 ID/64선택지에 개별 공식 근거 기록을 남겼다. 원본 정답을 오류로 판정하지 않았으며, 적용 setting의 불명확성·반복형·전부 정답 SATA 등의 문제를 별도 사례로 개선했다. 원본 32개 판정은 REPLACE 8 / MINOR_EDIT 24다. 아직 편집하지 않은 archive 변형을 새 사례와 동일하게 완성된 것으로 계산하지 않는다.

새 문항은 영어 지문·선택지, 한국어 선택지별 해설, 정확 조항과 기존 사례의 판단 차이를 포함한다. 같은 family를 유지하여 일반 세트에서 원본·개정판이 함께 중복되지 않게 하고, 기존 답안·북마크를 새 ID에 복사하거나 삭제하지 않는다.

## 연결 노트와 학습 화면

`2026-10-30.mor-discipline.1` overlay는 다음 5개 절을 개정한다.

- `w1-c-4`: 6.15의 적용 면허 종류·secondary control trigger, 신청과 실제 approval의 차이.
- `w1-c-5`: 환자군90일, 사전14일, 사후14일, stock-transfer attestation10일을 분리한 표. Institutional sterile/nonresident 예외, 대체 서명 조건과 inventory/보유금지 범위 구분.
- `w1-c-7`: 영업 중·staff unrestricted access의 각각의 presence trigger, nonresident 예외, 30분/6시간, new-Rx pickup·phone log·복귀 후 상담, 12시간/8시간 및 intern credit 근거 분리.
- `w6-b-8`: 법정 Board 구성, independent/chain 정의, seat별 자격·10년 징계이력 조건, 임기·holdover 구별.
- `w1-c-13`: Self-inspection 9.19(21), Board inspection 9.24, on-duty 기록제공, POC 9.25를 분리.

LAW-015 요약, 관련 두 장의 highlights와 자동 생성되는 복습카드·공식출처/본문 hash·노트·연습 링크를 함께 재생성했다. 기존 anchor와 읽음·북마크를 유지하되 개정판 재독 안내를 표시한다. `notes/guide.json`과 과거 revision은 보존하고 정확한 `site/notes/complete-notes.md` 한 경로만 네 번째 migration으로 연결한다.

## 출제영역 교정

[현재 NABP competency statements](https://nabp.pharmacy/programs/examinations/mpje/competency-statements/)에서 1.2는 개인 licensure/discipline이고 시설 운영 전체를 뜻하지 않는다. 새0069/70은4.7,0071은4.1/4.2,0072는1.1,0073/74는agency 관련2.5,0075/76은시설 inspection/discipline의4.7에 연결했다. 0075에는4.2/1.1 보조 연결도 있다. Board seat 숫자가 반드시 시험된다는 주장이 아니라 공개 blueprint에 맞춘 편집적 분류다. 2027-03-01 전/후 outline 전환은 유지한다.

## 검토 수의 경계

| 지표 | 현재 |
|---|---:|
| 전체 보관 문항 | 2,342 |
| 원본 EXP + CASE | 2,176 |
| 이전 MA-REV | 96 |
| 누적 별도 ID MA-RW | 70 |
| 기본 목록 | 438 |
| 이번 전체검토 추적표의 누적 기록 | 81 ID, 보류 포함 |
| 개별 재검증 기록 없음 | 2,261 |
| 구조 검사 | 원본1,024개, 법규 검토와 별도 |
| 제한된 노트 claim 또는 claim 묶음 | 35, source checked33 / OPEN2 |
| Canonical 재감사·release 상태 변경 | 0 |

대표355는 재작성70 / 기존 사례 통합3 / 보류10 / 개선 미반영272다. 전체검토 추적표의 81개는 과거 모든 작업의 독립감사 총계가 아니라 Unit3A/B·MOR·DISC의 명시적 ID 기록이다. 세부 status는 conditional41 / HOLD10 / author source checked30이다. 전체2334 또는2342문항과306절의 법규 검토 완료를 의미하지 않는다.

## 근거와 peer 검토

[247 CMR6](https://www.mass.gov/doc/247-cmr-6-licensure-of-pharmacies/download), [247 CMR9](https://www.mass.gov/doc/247-cmr-9-professional-practice-standards/download), [M.G.L. c.13 §22](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleII/Chapter13/Section22)의 공식 URL 본문을 2026-10-30에 재조회했다. PDF의 모든 쪽 추출문을 보존했으며 origin binary identity와 포괄적 supersession audit을 인증한 것은 아니다.

MOR는 별도 same-team peer가 원본16개와 새4개/노트3절을 교차 검토했다. DISC는 별도 작성자가 원본16개·새4개를 검토·작성하고 root가 공식 본문과 새17선택지/노트2절을 다시 대조했다. 같은 팀 교차 검토를 외부 독립 legal/realism audit로 승격하지 않는다. 새 문항의 `verification_status=NOT_INDEPENDENTLY_REVIEWED`와 null independent audit fields를 유지했다.

보고서 경로:

- `reports/full-corpus-review/mor-author-review.json`, `discipline-author-review.json`: 원본 ID별 기록.
- `mor-original16-peer-review.json`, `mor-new4-notes-peer-review.json`, `discipline-peer-review.json`: 범위와 hash가 고정된 same-team 검토.
- `mor-discipline-preservation.json`: 실제 시작 main에서 가져온 기존 공개62개 및68개 출처의 완전한 객체 해시.
- `mor-discipline-validation.json`: 이번 실제 실행 결과. 자동검사는 법규 판단을 대신하지 않는다.
- `progress.json`, `question-ledger.jsonl`, `notes-claim-ledger.jsonl`: 재현 가능한 누적 집계와 미완료 경계.

## 다음 작업

DISC05–08의 `MA-EXP-0209`–`0224`와 `w1-c-14`, `w1-c-15`, `w4-d-17`을 같은 방식으로 검토한다. 대표는0211/0215/0219/0223이다. 이 다음16개는 이번 검토 상태를 상속하지 않는다. CE email/Form, intern2/4·1:6 관계의 OPEN 및 PLUS source qualification은 유지한다. 미검토 문항을 분모에서 삭제하거나 구조 검사를 법규 검토로 합산하지 않는다.
