# MPJE 독립 검토와 census 보완 재감사 체크포인트

PR: https://github.com/woojunxnam/oddments/pull/190 (Draft)

이 문서는 2026-11-04T00:24:13.493358+00:00 기준 재개 기록이다.
이 변경의 최종 고정 head 전체 QA·CI·게시 검증은 아직 NOT RUN이며 PR189의 성공을 승계하지 않는다.
PR189는 merge172d712e3e45781f4360cc75c43f46bfd0c358cf, Pages41741216556에서 게시됐으며
공개10파일 SHA와 후속2개 workflow 성공을 reports/full-corpus-review/pr189-deployment.json에 보존했다.

| 별도 지표 | 현 체크포인트 | 한계 |
|---|---:|---|
| 저자 개별 검토 | 2346/2346, 100% | 독립 법규 PASS 아님 |
| 독립 legacy 정답 평가 | 843/2346, 35.93% | 원문880개, primary841+고정 보충2, 유효 미평가37; 모호성·보류 포함 |
| PR182 이후 실제 질문 내용 재작성 | 0/2346, 0% | 보호 원문·키·전체 객체 보존, 과거 별도ID 재작성74개는 별도 |
| 노트 저자 열거 | 306/306, 100% | 6978명제, 저자 근거확인 6094/BLOCKED 884; 독립 완전성 아님 |
| 현재 독립 완전성 확인 | 53/306, 17.32% | 현재 처리53절, census보완7절은 새 감사 대기라 처리 수 제외 |
| 현재 독립 노트 법규 | KEEP39/HOLD8/BLOCKED6 | 과거60절/1441claim 검토 이력과7개 누락 지적 모두 보존 |
| 공개 배포 검증 | 이전 PR189 10/10, 100% | PR190 NOT RUN |

## 통합된 증거와 별도 재감사

MA-CASE-0681–0840의160개를 원문/모든보기/전체보이는해설까지 독립 검토했다.
특히 YES 키라도 법규 HOLD 또는 해설 MINOR_EDIT가 있으면 원장의 KEEP로 남지 않도록
consumer를 고쳤다. 원래 저자·독립 보고서와 부정 판정은 바꾸지 않는다.
아카이브에는 새106개 실제 개별 부정·미확정 결과를 현재 question/report SHA에 결박한 안내를 더했다.

MA-CASE-0401/0441은 기존 절차 노출·NOT_ASSESSED를 지우지 않고 실제 새 fork_none 세션의
보충 결과를 별도 field로 보존했다. 고유 정답 평가만2개 늘고 원문 읽음은880개로 유지한다.
보충KEEP는 원래 HOLD/FAIL·기본제외·canonical gate를 해제하지 않는다.

노트 job9–12의20절/427명제 보고서는 모두 순차 통합됐다. 처음60절의 독립 결과는
완전성53/누락7, 법규KEEP39/HOLD15/BLOCKED6, claimKEEP1413/HOLD18/BLOCKED10이다.
보완등록 후7절은 현재 credit에서 제외하고 원래 보고서는 review_history에 남겼다.

보완7절: w1-a-2,w1-a-4,w1-b-1,w1-c-1,w1-c-3,w2-a-2,w2-c-6.
실제 author H가 원228개 claim JSON을 그대로 보존하고18개 atomic proposition을 추가했다.
복귀 inventory 서명은 새 SOURCE_BLOCKED, codeine027과 모든 기존 독립 법규 blocker는 승계한다.
본문·판본M·원래 census·원보고서·이전13 migration은 불변이다. 새14번째 annotation guard는
PR189 Markdown/build snapshot과 네 wave3 report의 exact SHA·범위·credit0을 결박한다.
7개 append-only version records는 커밋 바이트/원 job/claim mapping/omission SHA를 검증했다.
등록 자체는 독립 확인이 아니며 actual correctionauthor H는 이7개 새 감사에서 제외한다.

## 다음 작업과 재개 방법

Root만 /workspace/oddments의 queue/generated 파일에 쓴다. 별도 실제 reviewer session은
전용 branch/worktree에서 증거만 작성하고 root가 submit→증거cherry-pick→envelope 원바이트commit→
순차integrate→checkpointcommit→regen한다. lease가 stale이면 기존recover 경로를 쓰며 같은
actor/session을 새 instance로 재명명하지 않는다. 세션 이름의20261103은 안정된 식별자이지
새 조회일이 아니다. 새11/4 확인과 기존11/3 cache 날짜를 분리한다.

- 질문 job17–20: 원장에서 자동선정한 MA-CASE-0841–1000, 4개40문항 병렬작업 B/E/F/G.
  배정 /tmp/independent-phase6-LETTER-assignment.json, 안전원문 ...-visible.json,
  family/default-only projections는 기존 결론을 노출하지 않는다. /workspace/independent-phase6-LETTER.
- 노트 재감사 job13–19: 위7절을 한절씩 새 version binding으로 배정한다.
  C 첫단위 w1-a-2: /tmp/census-reassessment-c1-assignment.json, /workspace/census-reassessment-c1.
  procedural_retry 첫단위 w1-a-4: /tmp/census-reassessment-r1-assignment.json, /workspace/census-reassessment-r1.
  후속은 현재QUEUED 원장에서 claim한다. actual H 및 모든 알려진 원작성자 제외.
- 새 default 결함0861/0867/0879/0883/0895/0903/0919는 worker 최종 증거를 결박해
  다음 통합에서 안전제외한다. 현 공개판에는 아직 미반영이므로 새 배포 전 안전해졌다고 보고하지 않는다.
  0847/0910도 실제 법규·현실성 최종 결과를 확인하며 임의 PASS로 승계하지 않는다.
- 다음 wave도 통합 원장을 재생성·커밋한 뒤 미검토 IDs에서 자동 plan한다.
- 실제 state: reports/full-corpus-review/{independent-legacy-work-queue,independent-notes-work-queue,
  procedural-recheck-work-queue}.json. source/report/envelope 원바이트는 GitHub branch에 보존한다.
- 원 worker 원본은 checkpoints/mpje-audit-workers-20261103 branch를 fetch해 복구한다.
  worker-history-checkpoint.json의 정확한 원commit/head만 복구하고 존재하는 branch는 덮지 않는다.

## 검증과 완료 기준

primary disposition containment12 PASS, supplementary/controller 통합114 PASS,
수정한 historical note consumer12 PASS. 구 노트 suite70PASS/1FAIL은 전역40절 상수를
역사8job의 불변 evidence 검사로 고쳐 해결했다. 새7개등록 뒤의 전체 관련 suite와
최종 frozen head fullpytest/validators/9개 drift 및 보호검사/HTTPbrowser/GitHubCI는 별도 확인한다.
이전 head의 stale generated CI 실패를 최종 성공으로 숨기지 않는다.

audit-ledger와 near-candidates도 반드시 재생성한다. publication.json은 실제 현bank/selection
raw SHA를 결박해야 한다. 새14번째 manifest의 아직 미게시된 new_sha만 새annotation에 맞추고
기존13개 manifest는 절대 바꾸지 않는다. 모든 QA가 통과해야 merge/deploy하며 Pages 실패를
근거없이 성공으로 기록하지 않는다. 공개원점 실제파일 SHA까지 확인한다.

이 임무는 미완료다. 원문1466개와 노트246절의 최초 독립 검토, 보완본 새독립 감사,
개별 결함의 실제 수정 또는 안전보류, 정식 canonical gate와 해당변경의 게시 확인이 남아있다.
기존 OPEN4건 및 새 source/authority 불일치는 모두 명시적 보류한다. 물리기기/Safari/
psychometric 검사는 실행하지 않았다면 NOT RUN이다.
