# LAW-035 직접 연습 연결

LAW-035는 adult first outpatient opioid와 minor opioid의 7일 처방 제한을
설명한다. 같은 `w2-c-12`를 인용한다는 이유로 MassPAT 계정·조회·데이터 보고
문항을 이 카드의 직접 연습으로 선택하면 내용 범위가 맞지 않는다.

`config/curated-study-practice-links.v1.json`은 이 카드만 제한한다. 허용 후보는
독립 NOTE4-B가 실제 원문·모든 보기·해설을 읽고 §19D/§18B 범위에서 직접
대조한 MA-EXP-0713–0716이다. 모두 PMP07 family이므로 최대 한 문항만 연결한다.
다른 lesson의 기존 후보 순서·세 family 상한은 바꾸지 않는다.

근거는 B worker `a65785fb249438309085095f55e283d8b40a75c7`의 다음 원본이다.

- `fourth-b-review.json`의 raw SHA와 `w2-c-12` body binding
- `fourth-b-evidence/derived-surface-findings.json`의
  `FOURTH-B-DERIVED-001` entry 및 직접 지원 ID/record SHA
- `fourth-b-evidence/question-alignment.json`의 `direct_19d_18b_keychecks`
- 해당 보기별 authority가 인용한 §19D/§18B 공식 원문 raw SHA

설정은 현재 LAW-035의 id/title/core/why/trap/recall/note_units와 실제 유효
노트 본문의 UTF-8 SHA, 네 원 질문 객체 전체 SHA 및 각 직접 검토 entry SHA에
결박된다. Stored note hash만 일치해도 실제 본문이 달라지면 사용할 수 없다.
근거 파일·본문·entry·문항이 달라지거나 후보가 B의 직접 검토 범위 밖이면
builder는 오류로 중단한다. 과거 source report나 revision을 고쳐 맞추지 말고
새 근거 검토와 versioned config 변경으로 갱신해야 한다. 런타임에 오래된 Git
worker object가 있어야 한다는 의존성은 추가하지 않았다.

직접 지원 범위는 추천 자격을 부여하지 않는다. 기존 HOLD와 archive notice
제외, source-gap 제외, 좁은 OPEN 예외의 recommendation/별도 author-review
요건을 그대로 적용한 후 이 후보 집합으로 제한한다. 네 문항이 모두 보류 또는
부적격이면 `practice_links`는 빈 배열이다. 1063·0696·후속 1066 같은 무관한 PMP
문항으로 보충하지 않는다. LAW-035의 curated scope가 누락된 경우도 일반
note-unit fallback을 허용하지 않는다.

이는 내비게이션 교정이다. B의 claim-limited 대조를 전체 question audit 또는
canonical release로 승격하지 않으며 question audit/release credit은 0이다.
원 질문·정답·노트 본문·기존 warning/HOLD 및 공개 edition을 변경하지 않는다.

좁은 검증:

```bash
pytest -q tests/test_curated_study_practice_links.py tests/test_notes_independent_metadata.py
```

테스트는 실제 카드/은행/근거를 읽고 잘못된 링크 재발, 전부 보류 시 fallback,
기존 OPEN/source-gap 필터, 다른 lesson 비간섭, source/body/entry/question SHA
변조 및 입력 불변을 확인한다. 변조는 임시 fixture에만 수행한다.

Engineering 기준 HEAD `51144eb80afecf5ff92881b26d3c8871cc13fe8b`에는 변경 전부터
`Stale representative selection` gate가 있다. 이 수정은 해당 gate를 완화하거나
publication/selection/generated 파일을 덮어쓰지 않는다. Root가 현재 선택 상태를
별도로 통합한 후 전체 재생성·기존 exam-study artifact 검사·QA/CI를 수행한다.
`test_practice_note_links.py`까지 확대한 검사에서는 현재 기준 원본의 추가 은행
publication hash 불일치로 publish 경로의 세 테스트가 중단되었다. 해당 manifest와
은행 바이트도 기준 HEAD와 같으며 이 좁은 수정에서 고치지 않는다.
