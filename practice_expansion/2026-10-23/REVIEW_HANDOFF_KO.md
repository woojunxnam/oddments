# 독립 검토·GitHub 통합 인계

> 저장소 추가판: 파일 추가와 메인 안내 연결은 [INTEGRATION_KO.md](INTEGRATION_KO.md)에 별도로 기록했다. 아래의 쓰기 도구 제한과 미업로드 문장은 최초 작성 당시의 기록이다. 독립 감사·RELEASED 미완료 상태는 그대로 유지한다.

## 작성 당시 완료와 미완료 (저장소 추가 전 기록)

1,024개 문항 초안, 영어 stem/choices, 한국어 선택지별 해설, 노트 절별 link/hash, 로컬 학습 화면, 32개 검토 큐를 생성했다. 기존 GitHub 저장소를 이 세션에서 수정하거나 commit/push/PR/Pages 배포하지 않았다. 현재 연결에 쓰기 action이 없었다.

새 문항은 **DRAFT / NOT_INDEPENDENTLY_REVIEWED / publication_eligible=false**이다. 기존 RELEASED 자료와 섞지 않는다. 이 세션의 작성자 또는 이 자료를 단순 재서술한 작업을 fresh independent audit라고 기록하지 않는다.

## 로컬 저장소에 추가

패키지를 저장소 바깥에 풀고 Python 3.10 이상으로 먼저 dry run한다.

```bash
python /path/to/mpje_expansion/apply_to_repo.py --repo /path/to/oddments
python /path/to/mpje_expansion/apply_to_repo.py --repo /path/to/oddments --apply
```

`notes/guide.json`이 기준 snapshot과 다르면 중단한다. 변경된 노트에 맞춰 evidence와 문항을 먼저 재검토해야 한다. 기존 `practice_expansion/2026-10-23/`가 있으면 덮어쓰지 않는다. 적용 위치는 그 별도 폴더뿐이며 `data/`, `site/`, `audits/`, 기존 노트나 release policy를 수정하지 않는다. Git commit 또는 push도 자동 실행하지 않는다.

일반적인 branch·commit 예시:

```bash
cd /path/to/oddments
git switch -c feat/mpje-expansion-draft-20261023
git add practice_expansion/2026-10-23
git diff --cached --stat
git commit -m "Add segregated notes-derived MPJE practice draft for independent review"
git push -u origin feat/mpje-expansion-draft-20261023
```

이 commit은 검토용 원고 추가일 뿐 공개 문제 release가 아니다. 동일 branch가 이미 있으면 새 branch를 만들거나 기존 작업을 확인하고 진행한다. 강제 reset·force push를 하지 않는다.

## Independent review의 작업 단위

`review/packet-01.json`부터 32개 packet은 각각 32문항의 ID와 current content hash를 가진 **빈 검토 큐**이다. 이 형식 자체가 저장소 canonical initial-batch audit가 되지는 않는다. 실제 저장소의 `docs/RELEASE_POLICY.md`, `docs/AUDIT_WORKFLOW.md`, `data/release_requirements.json`, schemas를 최신 상태로 읽고 합법적인 대상·batch authorization·hash binding 구조에 맞춰 별도 기록해야 한다.

검토자는 각 family의 두 사례와 네 판단을 먼저 검토한 뒤 네 변형 모두의 선택지·정답·negative lead-in·해설을 다시 확인한다. 한 family 검토가 자동으로 그 네 문항의 current-hash independent KEEP 증거를 만드는 것은 아니다.

각 문항의 검토 항목:

- 정확한 statute/regulation/policy section, 적용일과 현재 효력, 사실관계의 부족·예외.
- 정답의 유일성 또는 SATA의 전체 정답 집합, 법적 must와 권고 should의 구별.
- 각 distractor가 정말 틀린지, 더 많은 사실이 주어지면 정답도 가능한지.
- 기존 439개 snapshot 문항 및 신규 family 사이의 semantic 중복; lexical report는 보조자료일 뿐.
- 정답 길이, absolute 단어, fixed pattern, 비현실적인 오답의 힌트.
- 필요한 canonical rule/drug IDs와 current hash/version; 노트 source_ids를 rule_ids처럼 사용하지 않기.
- 최종 목표 응시일의 blueprint, 2027-03-01 이후 버전의 재매핑 여부.

`candidates/questions.json`은 **별도 draft schema**이다. 현재 canonical question schema를 통과한 것으로 표시하지 않는다. Rule/drug mapping, provenance, family matrix, difficulty/reasoning steps, independent legal/realism evidence, final adjudication을 갖춘 뒤 기존 release builder를 통해서만 공개한다. 기존 validators를 느슨하게 만들거나 모든 상태를 일괄 RELEASED로 바꾸지 않는다.

## 실행자에게 전달할 짧은 프롬프트

> oddments 저장소의 기존 지침과 release policy를 먼저 읽고, 첨부 MPJE expansion 패키지를 별도 feature branch의 `practice_expansion/2026-10-23/`에 추가해 주세요. 1,024개는 256개 family의 관련 연습 변형이며 전부 DRAFT입니다. 기존 문제·노트·감사 기록을 보존하고, 우선 packet-01의 32문항을 current official sources 및 통합노트와 독립 검토하세요. 정답의 유일성, 오답 해설, 실제 업무 적합성, 기존 문제와의 semantic 중복을 점검하고 필요한 canonical rule/drug mapping을 만드세요. 실제 fresh independent audit와 repository release gates를 통과한 항목만 공개 문제은행에 편입하고, 미검토 원고를 RELEASED나 합격 보장 자료로 표시하지 마세요. 문항을 고치면 hash와 해당 감사 증거를 갱신하고 테스트 결과·검토 통과 수·보류 수를 구분해 보고하세요.
