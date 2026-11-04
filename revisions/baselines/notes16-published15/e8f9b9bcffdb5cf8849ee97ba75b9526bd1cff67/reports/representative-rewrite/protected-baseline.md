# 대표 문항 재작성: 원본 보호 기준

Repository: `woojunxnam/oddments` · 기준 main commit: `b5bd6b02c7ea8a5c6731871fa6e330ac6795fd36`

이 기준은 현재 파일의 SHA-256을 단순 등록한 것이 아닙니다. 초기 생성 시 실제 main의 GitHub tree/blob 기록과 각 보호 파일의 Git blob SHA-1을 먼저 대조했고, 일치한 바이트의 SHA-256만 저장했습니다.

보호 파일 **1,781개**, 총 **60,969,461 bytes**. 완전한 파일별 경로·Git blob SHA-1·SHA-256은 [protected-baseline.json](protected-baseline.json)에 있습니다.

## 범위

| 최상위 디렉터리 | 보호 파일 수 |
|---|---:|
| audits | 493 |
| data | 1167 |
| docs | 4 |
| notes | 5 |
| practice_expansion | 99 |
| schemas | 12 |
| site | 1 |

보호하는 디렉터리:

- `data/`
- `audits/`
- `notes/`
- `schemas/`
- `practice_expansion/2026-10-23/`
- `practice_expansion/2026-10-26-plus/`
- `practice_expansion/2026-10-27-quality/`

추가 보호 파일:

- `docs/RELEASE_POLICY.md`
- `docs/AUDIT_WORKFLOW.md`
- `docs/QUESTION_AUTHORING_STANDARD.md`
- `docs/SOURCE_USE_POLICY.md`
- `site/notes/complete-notes.md`

## 확인 방식과 한계

- 일반 실행은 파일별 SHA-256·Git blob SHA-1·크기와 보호 범위의 파일 집합을 확인합니다. 보호 원본의 변경·삭제·새 source 파일 추가는 실패합니다.
- Python/test cache는 source inventory에서 제외합니다. 이 제외는 JSON·법규·문항 source 파일을 제외하지 않습니다.
- 허용된 파생 산출물 `site/notes/study-data.js`, `site/notes/study-build.json`은 보호 범위에 넣지 않습니다. 새 대표 재작성 collection과 새 보고서·개발 스크립트도 이 기존 원본 기준의 대상이 아닙니다.
- 검증 실행은 baseline을 자동으로 갱신하지 않습니다. 명시적인 초기 생성도 동일한 기준이 이미 있으면 바이트가 같은 경우에만 허용됩니다.
- 이 기준은 원본 보존 증거입니다. 문항의 법규 정확성, 독립 감사 완료 또는 브라우저의 학습 기록 동작을 판정하지 않습니다.

## 재현 명령

```sh
python scripts/verify_representative_protected.py
```

초기 GitHub tree snapshot SHA-256: `a436936dd1bd648c1982fcf3cfa65094e27b1dfbfcc8b515cb98be73cba2b372`

초기 snapshot은 CI에서 다시 필요하지 않습니다. CI는 저장된 기준의 각 원본 Git blob과 SHA-256을 확인합니다.
