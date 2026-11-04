# GitHub 추가 기록 — 2026-10-23

## 이번 작업

1,024문항 초안과 256개 family, 32개 검토 큐 및 로컬 reader를 별도 subtree에 추가한다. 작성 원고·정답·해설·source snapshots·content hashes는 최초 제공 ZIP과 동일하다. README와 인계서의 저장소 반영 상태만 구별하고, 이 기록을 추가했다.

## 공개 사이트와 원고의 경계

메인 페이지의 **1,024문항 · 검토 원고** 버튼은 `site/practice-expansion/`의 상태 안내로 연결된다. 이 안내 페이지에는 문항이나 정답 payload가 없으며, GitHub의 검토 원고·다운로드 파일·검토 큐로 연결한다. 기존 시험 모드와 `site/generated/questions.json`에는 신규 draft가 추가되지 않는다.

원래 패키지는 256개 두-사례 family의 네 변형이며, 1,024개의 독립 vignette가 아니다. 신규 RELEASED는 0이다. 기존 문제와 semantic 중복 검토 및 독립 legal/realism audit는 여전히 남아 있다. 소프트웨어 테스트는 법률 내용의 독립 검증이 아니다.

## 보존

기존 `data/`, `audits/`, `notes/`, `site/generated/`, quiz scripts 및 release policy는 바꾸지 않는다. 기존 기록 저장소도 건드리지 않는다. 작성 당시 QA 보고서는 과거 테스트의 제한을 포함해 그대로 보존한다. 이번 CI 출력은 GitHub Actions 로그에서 별도로 확인한다.

## 다음 검토 단계

현재 저장소의 `docs/RELEASE_POLICY.md`와 `data/release_requirements.json`이 기준이다. 패키지의 과거 vendor별 감사 설명이 다르다면 현행 repository policy를 따른다. 이번 추가 작업은 independent audit가 아니며, canonical release evidence를 생성하지 않는다. Fresh reviewer가 packet별 exact authority·선택지·정답·중복을 검토하고 적법한 current-hash evidence 및 final adjudication을 갖춘 문항만 공개 builder를 거쳐 반영한다.

## 표시 수정

실제 HTTP 브라우저 검사에서 320px 폭의 가로 넘침이 발견되어 reader의 긴 토큰·버튼·badge 줄바꿈과 축소를 보완했다. 문항 payload와 정답은 변경하지 않았다. 기존 DOM-only 통과 기록은 실제 HTTP 검증과 구별해 보존한다.
