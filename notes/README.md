# Massachusetts MPJE 통합 노트

Week 1–6의 상세 노트를 **주차가 아닌 주제별로 재편집한 독립적인 학습판**입니다. 문제은행의 `data/`, RELEASED 판정 또는 독립 감사 기록을 변경하거나 대신하지 않습니다.

## 읽기

메인 페이지의 **Ultimate Notes · 통합 노트** 또는 **통합 노트 읽기** 버튼에서 엽니다. `site/notes/`가 독립 읽기 화면이고, `book.html`은 JavaScript 없이 읽고 인쇄하는 전체 본문입니다. `complete-notes.md`는 같은 데이터에서 생성된 다운로드판입니다.

현재 편집판은 33개 주제, 306개 상세 절, 127개 성분·제형 항목으로 구성됩니다. 검색, 북마크, 수동 읽음 표시, 이어 읽기, 글자 크기, 밝기, 집중 모드, 모바일 목차, 기록 내보내기/가져오기를 지원합니다. 기록은 `oddments.mpje.ultimate-notes.v1` 키로 해당 브라우저에만 저장합니다. 기존 문제은행 기록을 읽거나 삭제하지 않습니다.

## 내용의 기준과 한계

`guide.json`이 이 **노트 편집판**의 source of truth입니다. 기존 2026-10-20–22 원문 대조를 승계하며, 2026-10-23에는 일부 항목만 다시 검토했습니다. 22개 입력 문서의 391개 번호 있는 큰 절을 `editorial-map.json`에 대응시켰습니다. 56개 입력 절은 다른 본문과 통합하고, 46개 반복 요약·출판 메모·주차별 일정을 공통 안내로 정리했습니다. 나머지 고유 상세 설명은 주제별로 재배치했습니다. 이 수치는 법률 정확성이나 합격 준비도의 점수가 아닙니다.

단순 파일 합치기가 아니라 CE, Continuity of Care, MOR, 재고, 반환, 약사 권한 경로, 제품 식별, REMS의 겹치는 설명을 연결하고 재서술했습니다. 서로 다른 법의 조건·예외·시계는 병합하지 않았습니다. 일반 개념의 요약이 각 장의 상세 조건을 대체하지 않습니다.

### 이번 보완

- Schedule VI 14일 regulation과 30일 policy, gabapentin 제외 및 prescriber 진료 중단 경로를 하나의 상세 절로 통합했습니다. 겹치는 적용 관계의 OPEN은 유지합니다.
- CE 미충족 시 Board email 안내를 현재 본문에 반영했습니다.
- MOR 장기 부재에 관한 과거 247 CMR 6.12 참조를 9.23(5)로 교정했습니다. 6.12는 약국 이름 변경 통지입니다.
- M.G.L. c.94C §21C의 point-of-sale lesser-price 규칙을 추가했습니다.
- Multi-drug packaging policy의 “unless otherwise prohibited”를 설명했습니다. 정책에서 문구가 생략됐다는 사실을 CII/CIII 금지의 폐지로 추정하지 않습니다. 이 적용 설명은 편집적 판단이지 새 Board 회신이 아닙니다.
- Week 5 원본의 출처 등록부를 복원해 약물 사전과 개별 법규·제품 자료를 연결했습니다. MedlinePlus 명칭 색인, 개별 label, DailyMed 검색 링크의 확인 범위를 구별했습니다.

각 절은 기존 원문 재편집, 중복 통합·재서술, 좁은 공식 원문 추가 확인을 구별합니다. **HIV/STI statewide DOCX 전문, 일부 보고·공급·기관 경계, USP 정본의 모든 전문 예외는 미완료**입니다. 미확정 경계와 미래 시행을 확정 암기사항으로 만들지 않았습니다. 공개 원문 링크의 존재가 당일 원문 전체 열람 또는 전 페이지 시각검수를 의미하지 않습니다.

**독립 전수 법률감사·Board 승인·합격 보장 자료가 아닙니다.** 이 노트의 읽음 표시가 시험 합격 확률이나 숙련도를 나타내지 않습니다. 규정·제품별 지시가 변경될 수 있으므로 실제 시험일의 authority가 최종 기준입니다.

## 유지보수

```bash
python -m pip install -r requirements-dev.txt
python scripts/build_ultimate_notes.py
python scripts/build_ultimate_notes.py --check
python -m pytest tests/test_ultimate_notes.py -q
```

`site/notes/content.js`, `book.html`, `complete-notes.md`, `build.json`은 생성물입니다. 직접 수정하지 말고 `guide.json`을 수정한 뒤 재생성하세요. UI는 `site/notes/notes.js`, `notes.css`, `index.html`에서 관리합니다.

브라우저 회귀 검사:

```bash
python -m pip install playwright==1.57.0
python -m playwright install chromium
python scripts/verify_notes_browser.py
```

`--inline-preview --executable-path /usr/bin/chromium`은 네트워크 탐색이 차단된 환경의 로컬 렌더링 검사입니다. 실제 HTTP 탐색·origin 기반 저장·reload·main 이동의 검증으로 표시하지 않습니다. 정규 CI는 기본 HTTP 모드로 검사합니다. 소프트웨어 검사는 법적 정확성에 대한 independent audit가 아닙니다.

원본의 개인 Drive 링크와 개인 파일 경로는 게시하지 않습니다. 주차·절 번호와 입력 hash는 내용 계보를 추적하기 위해 유지합니다. 상업 교재 원문·기출 복원 문항은 포함하지 않습니다.
