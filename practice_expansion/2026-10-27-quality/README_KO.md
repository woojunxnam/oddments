# 개별 작성 사례·중복 축소 — 2026-10-27

GitHub 적용판. [통합·실행 기록](../../docs/PRACTICE_QUALITY_REVIEW.md)과 [최초 작성 검토](../../docs/PRACTICE_QUALITY_AUTHORING_REVIEW.md)의 범위를 구분한다. 실제 공개 여부는 병합 커밋의 Pages 배포 결과가 기준이다.

## 구성

- `authoring/*.txt`: 개별 작성 96개 사례, 영어 보기·한국어 선택지별 설명.
- `questions.json`: 재현 가능한 결과. 84 SBA + 12 SATA, stable IDs `MA-REV-0001`–`0096`.
- `selection.json`: 기존 대표 선정과 동일 stem/보기 세트 제외 기록. 기본 355+96=451; 전체 2,272 보존.
- `reports/practice-quality/`: 기존 2,615개 구조 검사, 정답 문자열 재사용, 2,711개 근접 이웃과 개정 후 비교.

기존 원고·정답·notes guide·감사·release policy를 바꾸지 않는다. 확인일·OPEN·시행일은 유지한다. `primary_source_read_records`는 작성 당시 선택적으로 읽은 출처이며 모든 항목의 독립 검증을 뜻하지 않는다.

## 재현

```bash
python scripts/audit_practice_quality.py
python scripts/build_quality_questions.py
python scripts/select_quality_representatives.py
python scripts/build_exam_study.py
python scripts/publish_practice.py --output public-site
python -m pytest tests/test_practice_quality.py -q
```

문항을 고치면 해당 검토를 거친 뒤 publication manifest SHA를 갱신해야 한다. 변경된 내용을 확인하지 않고 hash만 바꾸어 통과시키지 않는다. 선택적 근접 문항 탐색 `scripts/audit_practice_similarity.py`에는 NumPy·scikit-learn이 필요하다. 텍스트 유사도는 법적 의미의 판정을 대신하지 않는다.

## 연습 방식

일반20/최대120은 family·stem·전체 보기 세트 반복을 제한한다. 고유 사례가 부족하면 짧은 세트가 된다. Chaos10은 필터와 비율을 무시하고 전체 2,272개에서 복원 추출하므로 같은 family·문항 ID가 반복될 수 있다. 반복 문항은 세트 내 slot별로 채점·검토한다. 영구 문항별 기록은 마지막 시도이며 진행 중 세트의 새로고침 복원은 제공하지 않는다.

새 문항은 작성자 대조·편집 단계이다. 독립적인 법규 감사 완료, 실제 MPJE 난도 동등성 또는 합격 보장을 표시하지 않는다.
