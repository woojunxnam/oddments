# Massachusetts MPJE — CDTM13–16 / VAX01–04 40-ID 품질 개선 검토

검토일: 2026-10-30. 적용 대상: `MA-EXP-0273–0304` (32원본) 및 기존 `MA-RW-0037–0044` (8개정).

## 데이터 집계 바로잡기

이 구간은 **CDTM13–20이 아니다**. 원본 0273–0288은 **CDTM13–16** 네 family이고, 0289–0304는 **VAX01–04** 네 family다. Family는 같은 두 사례와 네 판단을 재배열한 교육용 문항 묶음이어서 40개 ID는 40개의 독립 법적 원칙이 아니다.

원본 32개 = 128선택지, 개정판 8개 = 33선택지. 전체 **40개 ID / 161개 선택지**에 대해 원본 complete-record hash, 보기별 법률적 근거·한국어 해설과 저장된 정답을 다시 비교했다. 공식 자료의 해당 조항에 한정된 **작성자 출처 검토**이며 제3자 독립 법규 감사, 실제 난이도 교정 또는 시험 문제 복제를 의미하지 않는다. 개정판 추가 생성, 원본 ID·정답·attempt 기록 변경, canonical RELEASED 변경 없음.

## 주제별 개선 목록

| Family | 원본 | 기존 개정판 | 핵심 근거 | 품질상 주의 |
|---|---|---|---|---|
| CDTM13 | 0273–0276 | MA-RW-0037 | 247 CMR 16.03(5)(e)2;16.04(2)(h) | 24시간은 maximum; urgent communication coverage를 먼저 실행 |
| CDTM14 | 0277–0280 | MA-RW-0038 | 247 CMR 16.04(1)–(4) | CPA의 위임 가능·금지 업무와 조건을 별도 기재 |
| CDTM15 | 0281–0284 | MA-RW-0039 | 247 CMR 16.04(5)–(6) | 종료 전 transition, 현재 원본/사본 보존 |
| CDTM16 | 0285–0288 | MA-RW-0040 | 247 CMR 16.04(7) | QA 목적 physician 고용과 CPA 유지 목적 고용 구분; 0287 all-correct SATA |
| VAX01 | 0289–0292 | MA-RW-0041 | Policy 2023-02 intro/III | PTT 제외; qualified immunizer direct supervision |
| VAX02 | 0293–0296 | MA-RW-0042 | Policy 2023-02 I–II; FDA GARDASIL 9 | State age5 ≠ individual product 9–45 indication |
| VAX03 | 0297–0300 | MA-RW-0043 | DPH Standing Order 2026-06 | Immune-suppressed solid-organ transplant 18–64 exception 좁게 적용 |
| VAX04 | 0301–0304 | MA-RW-0044 | Policy 2023-02 III.C | ACPE 12 self-study + 8 live + IM/SC hands-on; 0303 all-correct SATA |

원본 **MA-EXP-0287**, **MA-EXP-0303**은 모든 선택지가 정답으로 저장된 SATA다. 현재 제한된 법규 범위에서는 키 오류를 확정하지 않았으나, distractor가 없어 변별력이 부족하다. 원본을 보존하면서 기존 MA-RW-0040/0044 사례형을 우선 노출하는 이유다. 다른 원본 또한 한 family의 반복 문구를 공유한다.

## 실제 새 공식 원문 조회

- [247 CMR16, Massachusetts Board](https://www.mass.gov/doc/247-cmr-16-collaborative-drug-therapy-management/download) §§16.03–16.04; 공식 규정 표기일 2017-12-15
- [DPH Policy 2023-02 Vaccine Administration](https://www.mass.gov/doc/2023-02-vaccine-administration-pdf/download); 공식 PDF 개정일 **2025-09-04**
- [DPH pharmacy influenza order 2026–27](https://www.mass.gov/doc/standing-order-for-pharmacies-administration-of-influenza-vaccine-2026-27/download); **2026-09-30** signed. Procedure 1(b)·5의 organ transplant recipient 예외 범위
- [FDA GARDASIL 9 indication](https://www.fda.gov/vaccines-blood-biologics/vaccines/gardasil-9) (FDA 9–45세 indication)
- [M.G.L. c112 §24G intern vaccination](https://malegislature.gov/Laws/GeneralLaws/PartI/TitleXVI/Chapter112/Section24G)

공식 PDF는 웹 색인된 본문을 직접 조회했지만 화면 screenshot 요청은 사이트에서 403을 반환했다. 캡처로 재검증했다고 과장하지 않는다. source relationship OPEN, 시험 psychometric calibration, 개별 환자의 임상적 예외·기타 federal PREP Act 경로는 전수 재검증되지 않았다.

## 통합노트 개정

`revisions/notes/2026-10-30-cdtm13-vax04.json`은 CDTM `w3-d-9`·`w3-d-10`, 예방접종 `w3-c-1`–`w3-c-4` 총 **6개 절**을 실제 상세 사례형으로 보강하는 versioned overlay다. 원본 `notes/guide.json`와 과거 overlay, reader storage, original questions는 그대로 둔다. 관련 13개의 핵심 법규 주장만 `reports/full-corpus-review/cdtm-vax-note-claims.json`에 기록하며 모든 절의 모든 atomic claim 검토 완료와 구별한다.

정적 학습 페이지 `site/notes/cdtm13-16-vax01-04.html`에서 8개 주제 → 통합노트 절 → 기존 MA-RW 개정 사례 → 원본 32개 deep link를 연결한다. 새 파일은 기존 global learning dock CSS/JS를 유지한다.

## 배포 및 진행률의 엄격한 분리

기준 checkpoint는 앞 배치의 161개 explicit author review / 2,185개 미재검증 / 누적 62개 claim clusters(58 checked,4 OPEN) / 통합노트 20 versioned units이다. 이번 40개 리뷰와 13 claim을 정식 생성물로 반영하면 **예상** 201 reviewed/2,145 not reverified, 75 claim clusters(71 checked/4 OPEN), 26 versioned units, 25 partial-claim units가 된다. **CI가 정확한 HEAD에서 PASS·PR 병합·Pages 배포를 확인하기 전에는 예상 수치를 배포 완료로 표시하지 않는다.**

지금 범위에서 공식 본문과 저장된 key의 명백한 충돌은 발견하지 않았으나 독립 검증자는 별도이다. 향후 배치는 **MA-EXP-0305–0336 및 MA-RW-0045–0052** 실제 family를 다시 확인한 뒤 진행한다.
