# 개별 작성 사례·중복 축소 — 2026-10-27

작성·로컬 실행 패키지. GitHub 게시 미실행. `docs/PRACTICE_QUALITY_REVIEW.md`의 검증 경계를 먼저 읽는다.

## 파일

- `authoring/*.txt`: 개별 작성 96개 사례, 영어 보기·한국어 선택지별 설명. 무관한 새 법규 96개가 아니다.
- `questions.json`: 재현 가능한 빌드 결과. 84 SBA +12 SATA, 새 stable IDs `MA-REV-0001`–`0096`.
- `selection.json`: 기존 family 대표 선정과 동일 stem/보기 세트 제외 기록. 기본 목록355+96=451, 전체보존2272.
- `reports/practice-quality/`: 기존2615개 구조 ledger, 정답 텍스트 재사용,2711개 near-neighbor, 개정후 비교.

기존 archives/정답/notes guide/audits를 덮어쓰지 않는다. 노트의 확인일·OPEN·시행일은 유지한다. 추가 official-source reads는 문항의 `primary_source_read_records`에 구분했다. 실제 MPJE·독립법규검토·합격가능성 보정 자료가 아니다.

## 재현

```bash
python scripts/audit_practice_quality.py
python scripts/build_quality_questions.py
python scripts/select_quality_representatives.py
python scripts/build_exam_study.py
python scripts/publish_practice.py --output public-site
python -m pytest tests/test_practice_quality.py -q
```

`questions.json`을 변경하면 publication manifest SHA도 해당 검토판에 맞춰 갱신해야 한다. 이전 파일이 변했는데 hash만 편의상 바꾸어 통과시키면 안 된다.

근접문항 탐색은 별도 선택 작업이다: `python scripts/audit_practice_similarity.py`. NumPy와 scikit-learn이 추가로 필요하다. 문자열 유사도는 법적 의미의 중복 판정이 아니므로 threshold만으로 독립감사를 완료했다고 표시하지 않는다.

## 화면

일반20/최대120은 family·stem·전체보기세트를 제한한다. 특정 collection의 고유 사례가 부족하면 짧은 세트가 된다. Chaos10은 전체2272에서 복원추출하여 같은 family·같은 ID를 허용한다. 세트 내 동일 ID는 slot별로 채점하며 문항별 저장 기록은 마지막 시도이다. 진행 중 세트의 새로고침 복원은 제공하지 않는다.
