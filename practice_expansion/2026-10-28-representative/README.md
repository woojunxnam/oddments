# Representative revisions — cumulative authoring units

2026-10-29 후속 단위: 기존 대표 12개 중 신규 10개 + 기존 사례 재사용 2개. 누적 신규 56개, 재사용 3개, 보류 7개, 후속 개선 289개다. 기본 441개, 전체 2,328개이며 [두 번째 단위 보고서](../../docs/REPRESENTATIVE_REWRITE_UNIT2.md)에 필터 안내 개선과 실제 검토 범위를 기록했다.

## 첫 단위의 작성 이력

2026-10-28 · baseline main `b5bd6b02c7ea8a5c6731871fa6e330ac6795fd36`

이 묶음은 기존 대표 355개 전체의 재작성 완료판이 아니다. 먼저 면허·인력·CE와 CDTM·예방접종의 기존 대표 48개를 개별 검토하여, 새 사례 46개를 작성하고 기존 고품질 사례 1개를 재사용했으며 CE 출처 충돌 1개를 보류했다. 다른 대표 문항에서 발견한 6개 문제도 기본 목록의 보류 기록에 포함한다.

## 파일

- `authoring/01_personnel.json`: 24개 원문에 대한 22개 새 사례, 1개 재사용, 1개 보류. 각 선택지의 정오·한국어 이유·정확한 공식 조항을 함께 작성했다.
- `authoring/02_clinical_authority.json`: CDTM 16개와 예방접종 8개. 신규 참여 경로·의뢰·동의·처방 권한·기록·교육 요건을 개별 상황으로 묻는다.
- `authoring/03_personnel_scope.json`: 두 번째 단위의 인력 업무 범위 새 사례 4개와 재사용 2개.
- `authoring/04_pharmacy_operations.json`: 두 번째 단위의 시설면허·MOR·운영 변경 새 사례 6개.
- `questions.json`: 위 작성 파일에서 생성하는 누적 공개 연습 데이터. 첫 단위의 46개와 두 번째 단위의 10개를 포함한다. `MA-RW-0013`, `0019`, `0049`, `0052`는 보류·재사용에 따라 생성하지 않은 번호다.
- `selection.json`: 원본에서 개정 사례로 이어지는 명시적 매핑, 보류 이유, 기본 목록, 출처 파일 해시.
- `../../reports/representative-rewrite/`: 355개 편집 감사표, 선택지 교차 검토, 출처 충돌, 중복·정답 패턴, 원문 보존 검사.

## 학습 기록과 공개 상태

정답과 의미가 달라진 문제에 이전 문항 ID를 재사용하지 않는다. 원본의 ID·정답·해설은 보존하고 개정 사례에는 별도 ID와 `revision_of`를 부여한다. 원본과 개정 사례의 family는 유지하여 일반 연습에서 둘을 같은 세트에 넣지 않는다. 북마크와 답안은 새 ID로 복사하거나 지우지 않는다. Chaos10은 원본과 개정 사례를 포함한 전체에서 복원추출한다.

`PUBLISHED_PRACTICE`는 웹 연습 공개 상태다. 작성자의 공식 본문 대조 및 같은 작업 팀의 교차 검토를 canonical 독립 법규 감사로 승격하지 않는다. `NOT_INDEPENDENTLY_REVIEWED`, null independent audit fields와 기존 release gate를 유지한다.

## 재현

```bash
python scripts/build_representative_rewrites.py --check
python scripts/build_representative_audit_ledger.py --check
python scripts/audit_representative_similarity.py --check
python scripts/verify_representative_protected.py
python -m unittest discover -s tests -p 'test_representative_rewrites.py'
```

문항 작성 파일을 수정하면 builder를 다시 실행한 후 publication의 bank/selection SHA-256을 갱신하고, `build_exam_study.py`로 관련 사례 링크를 재생성해야 한다. 의미가 달라진 공개 문항을 수정할 때는 다시 새 ID 또는 명시적 기록 이행 정책을 검토해야 한다. 이 최초 공개 전 편집 기록은 reports에 보존했다.

새 작성 단위는 별도 authoring 파일에 실제 `authored_at`·`edition`·공식 source 확인일을 기록한다. 이미 공개된 46개는 `published-unit1-baseline.json`이 전체 질문·출처 객체를 고정하므로, 새 날짜를 이전 사례에 일괄 덮어쓰면 빌드가 실패한다. 기준 해시는 실제 이전 main Git 객체에서 만들었으며 일반 빌드가 자동 갱신하지 않는다.

현재 출제 기준은 2027-03-01 이전 Massachusetts MPJE Competency Statements다. 미래 outline을 현재 시험에 적용하지 않는다. 이 사례들의 법규 내용 자체가 해당 날짜에 자동 만료된다는 의미는 아니다.
