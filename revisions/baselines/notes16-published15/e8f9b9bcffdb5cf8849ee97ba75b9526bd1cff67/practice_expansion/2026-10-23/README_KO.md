# Massachusetts MPJE — 신규 연습문항 검토 패키지

**1,024문항 초안 / 256개 사례 묶음 / 독립 검토 전 / 저장소 검토용 추가판**

Week 1–6 통합노트 기반의 추가 연습자료다. `practice_expansion/2026-10-23/`에 기존 문제은행과 분리해 보관한다. 메인 페이지의 신규 문항 안내는 이 원고와 검토 상태로 연결하며, 기존 시험 모드에는 미검토 문항을 넣지 않는다. 문항 내용·정답·검토 상태는 원래 초안과 동일하다. 이 패키지의 과거 보고서는 작성 당시의 실행 기록이며, 이번 추가 내역은 [INTEGRATION_KO.md](INTEGRATION_KO.md)를 따른다.

## 먼저 열 파일

`review/practice-lab.html`을 브라우저로 연다. 외부 JavaScript·서버·계정 없이 쓰도록 만든 단일 HTML이다. 첫 화면의 DRAFT 안내를 확인해야 문항이 열린다. 이 파일은 새 GitHub URL이 아니라 로컬 검토판이다. 실제 기기의 파일 미리보기 앱이 JavaScript를 실행하지 않으면 데스크톱 브라우저에서 파일을 열거나 로컬 웹서버로 제공한다.

```bash
python -m http.server 8000 --directory /path/to/mpje_expansion
# 브라우저: http://localhost:8000/review/practice-lab.html
```

이 환경에서는 로컬 HTTP·file URL 이동이 관리자 정책으로 차단되어 실제 origin의 동작은 확인하지 못했다. Chromium에 HTML을 직접 주입한 DOM 테스트에서는 문항·선택·검색·채점·반응형 화면이 동작했으며, 저장 복원 검사는 명시적인 mock storage를 사용했다. 실제 iOS/Android 파일앱과 Safari 동작은 미검증이다.

## 무엇이 포함되어 있나

영어 문제·선택지, 한국어 핵심 해설과 선택지별 해설, 관련 통합노트의 정확한 절 link와 hash, 원래 노트의 확인일·OPEN 표시를 포함한다. 문항 본문은 기존 문제에서 복사하지 않고 새로 작성했으며 기존 ID와 충돌하지 않는다. 같은 개념의 semantic 중복 여부는 독립 검토가 남아 있다.

- 단일선택 768개, 복수선택 256개.
- 256개 family마다 두 사례와 네 판단이 있고, 이를 네 연습각도로 사용한다. 따라서 512개의 공유 사례를 사용하며 1,024개의 독립 vignette라고 세지 않는다.
- 잠정 영역 배분: 면허·인력 224, 약사 업무 336, 조제 228, 운영 236. 정확한 실제 시험 출제비율을 재현하지 않는다.
- 전체 노트 306절 중 218절에 연결하고 관련 참고문헌 168개를 유지한다. 참고문헌 개수는 item-level 법적 검증 수가 아니다.
- 20문항 학습, 120문항·150분 비적응형 시간 연습, 영역·유형·검색·오답·북마크 필터, 글자 크기·밝기, 기록 내보내기/가져오기.
- 세트에서는 family당 최대 1문항만 선택한다. 선택한 필터에 family가 부족하면 가능한 수만 제공한다.

## 파일 구조

`authoring/`: 직접 작성한 256개 family와 true/false 판단·한국어 해설.

`candidates/questions.json`, `.jsonl`: 구체화된 모든 문항과 정답·근거 metadata. 별도 draft schema이며 canonical bank에 바로 복사하지 않는다.

`candidates/complete-practice-draft.md`: 전체 문제·정답·해설의 읽기용 문서.

`review/practice-lab.html`: 단일 파일 학습 화면. `packet-01.json`–`packet-32.json`은 검토 대기 큐이지 완료된 audit가 아니다.

`research/RESEARCH_COMPARISON_KO.md`: NABP·공개 플랫폼 비교, 선택적 primary-source 재확인, 출처·권한 경계.

`research/note_evidence.json`: 문항에 연결한 우리 노트 절의 snapshot. 원문 법령의 신규 독립 감사가 아니다.

`reports/`: 구조검사, lexical 유사도, 작성상 힌트 경고, 브라우저 테스트 및 실제 제한.

`apply_to_repo.py`: dry-run 기본의 추가 전용 적용 스크립트. 사용법은 `REVIEW_HANDOFF_KO.md`.

## 검증 상태를 구분하기

모든 새 문항은 `DRAFT / NOT_INDEPENDENTLY_REVIEWED / publication_eligible=false`다. 독립 legal audit 0건, independent realism audit 0건, 새 RELEASED 0개다. 소프트웨어 테스트가 통과했다고 정답·법률 해석·실제 시험 난도가 검증된 것은 아니다.

현재 원고는 학습용 연습 변형이며 일부 오답은 단순하거나 문장 패턴이 규칙적이다. 문항별 법규 원문 대조, 그럴듯한 오답 보완, semantic 중복 검토와 canonical rule mapping이 필요하다. 관련 경고는 삭제하지 않고 보고서에 남겼다.

공식·공개 sample의 형식만 참고했고 비공개 Pre-MPJE, 복원·유출 기출, 유료 은행의 문항 텍스트는 사용하지 않았다. 법적 근거는 통합노트와 명시한 공식 출처이며 vendor 설명은 법률 authority가 아니다.

## 재생성·검사

Python 3.10 이상. 문항과 HTML 생성은 표준 라이브러리만 사용한다.

```bash
python scripts/build_expansion.py --guide /path/to/oddments/notes/guide.json
python scripts/build_reader.py
python -m pytest tests/test_expansion.py -q
python scripts/validate_expansion.py --existing-questions /path/to/oddments/data/questions
python scripts/verify_reader.py
```

테스트용 추가 패키지는 `requirements-review.txt`에 있다. Chromium 경로는 `CHROMIUM_PATH`로 지정할 수 있다. `DOM_HARNESS=1`은 HTTP/file-origin 검사가 아니라 제한된 DOM 검사용이므로, 그 결과를 실제 파일·웹 배포 통과로 부르지 않는다. 내용·보고서 수정 후 `python scripts/make_manifest.py`로 package checksum manifest를 다시 만든다. Manifest는 파일 무결성 점검이며 trusted publisher signature가 아니다.

**합격 보장, 공식 NABP 점수 환산, CAT 동등성, 전수 법률검증을 제공하지 않는다.** 검토가 끝난 기존 공개 문제은행과 이 원고를 구분해서 사용한다.
