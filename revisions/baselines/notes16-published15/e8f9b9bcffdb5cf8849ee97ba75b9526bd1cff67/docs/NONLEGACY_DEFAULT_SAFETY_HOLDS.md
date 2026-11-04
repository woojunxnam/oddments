# MA-REV·MA-RW 기본 연습 안전 보류

이 경로는 현재 공개 연습판의 MA-REV 96개 및 MA-RW 개정판에서 발견된 결함을 기본 추천에서 잠시 제외하는 포함 범위 조치입니다. 법적 정답의 자동 판정, 독립 감사, canonical 입학 또는 RELEASED 승인이 아닙니다. 원본 355개 처리·감사 원장과 `holds` 수는 변경하지 않습니다. 원본 355개에는 기존 `holds` 경로를 사용합니다.

편집자는 `reports/representative-rewrite/nonlegacy-default-holds.json`에 다음 구조로 실제 검토 근거를 등록합니다. 아래 값은 형식 설명이며 유효한 보류 증거가 아닙니다.

```json
{
  "schema_version": "nonlegacy-default-safety-holds/1",
  "holds": [
    {
      "question_id": "MA-REV-0058",
      "question_record_sha256": "현재 raw 문항 객체의 SHA-256",
      "review_source": "reports/full-corpus-review/검토보고서.json",
      "review_source_sha256": "검토보고서 파일 전체 raw bytes의 SHA-256",
      "reason": "실제 검토가 확인한 개별 결함과 학습 시 주의할 점",
      "next_action": "필요한 수정 또는 새 ID 작성과 후속 검토"
    }
  ]
}
```

문항 hash는 출판용 delivery metadata를 덧붙이기 전 `questions.json`의 전체 개별 객체에 대해 `json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()`의 SHA-256입니다. `content_sha256` 필드를 제외하는 개정판 content hash와 다릅니다. 기존 ID 아래의 원문·정답·해설·기록은 변경하지 않습니다.

빌드와 공개 payload 결합 단계가 다음을 모두 확인합니다.

- 실제 기본 후보인 알려진 MA-REV·MA-RW ID이고 중복이 없어야 합니다. 원본 355개·알 수 없는 ID·임의의 다른 보관 문항을 제외하는 용도로 사용할 수 없습니다.
- 현재 raw 객체 hash, 검토 파일 raw hash, `records[].question_id` 및 `records[].record_sha256`가 정확히 일치해야 합니다. 같은 검토 보고서의 중복 ID도 거부합니다.
- 검토 경로는 저장소 안의 `reports/full-corpus-review/` JSON이어야 합니다. 경로 이탈과 다른 위치의 요약 파일을 허용하지 않습니다.
- 작성자 경로는 명시적 `reviewer_provenance.independent: false`, `author_session`, `checked_at`와 실제 `disposition`이 필요합니다. 허용되는 비유지 판정은 `MINOR_EDIT`, `MAJOR_REWRITE`, `HOLD`, `HOLD_FOR_LEGAL_REVIEW`, `DELETE`, `REPLACE`입니다. 전 선택지의 개별 발견사항과 공식 authority가 있어야 합니다.
- 독립 경로는 `independent_of_authors: true`, 실제 `auditor_instance`, `canonical_audit: false`, `canonical_release_credit: 0`가 필요합니다. 법규/현실성 검토의 비유지·FAIL 또는 명시적 wrong answer가 필요하며, KEEP/PASS나 자동 QA 요약만으로는 보류할 수 없습니다. 검토 보고서의 schema 이름 하나로 독립성을 추정하지 않습니다.
- 실제 검토의 authority는 공식 HTTPS 도메인, exact section, 확인일 및 같은 보고서의 공식 source register와 연결되어야 합니다. 작성자 source register는 ID별 객체 또는 `source_id` 배열 구조를 지원합니다.
- 비어 있지 않은 `reason`과 `next_action`이 필요합니다.

생성 selection의 `safety_holds`는 이 입력에서만 파생됩니다. `previous_quality_ids`는 보류 여부와 관계없이 이전 96개 전체를 보존합니다. `recommended_ids`는 원래 대표 목록에 명시적 원본 교체/보류와 검증된 안전 보류를 적용한 정확한 집합이어야 합니다. 별도 증거 없이 이전96개를 빼거나, 보류 문항을 추천에 다시 넣으면 검증이 실패합니다.

통계의 `held_from_default`·`legacy_representatives_remaining`는 계속 원본355개만 집계합니다. `original355_default`·`original355_held_from_default`는 그 범위를 명시합니다. `previous_quality`는 보관 수, `previous_quality_default`·`previous_quality_safety_held`는 이전96개의 기본 포함·안전 보류 수입니다. `newly_authored_replacements`는 모든 MA-RW 보관 수이며 `rewrite_default`·`rewrite_safety_held`가 실제 기본 포함·안전 보류를 구분합니다. `nonlegacy_safety_held_from_default`는 이 별도 경로의 보류 합계입니다.

모든 보류 ID는 전체 목록, Chaos10, 기존 풀이·북마크·deep link에서 계속 열립니다. 보류 이유와 다음 조치를 화면에 표시하며 원래 채점 결과를 확정된 법규 판단으로 사용하지 않도록 안내합니다. MA-RW도 기존 원본 링크와 함께 같은 보류 안내를 표시합니다. 자동 생성은 통합 담당자가 수행하며, 개별 검토자가 임의로 원본·보호 baseline·canonical 감사/규칙/문항을 바꾸지 않습니다.
