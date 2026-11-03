# 독립 legacy 감사 실행 계약

목적은 현재 원문에 대한 별도 법규·현실성 판정이다. Author review, queue integration, inventory 및 canonical RELEASED와 구분한다. `/workspace/oddments` 공유 원장/생성물/실제 queue는 root 통합 담당자만 쓴다. 감사자는 지정 worktree에서 독자 보고서·evidence만 commit한다.

## 독립성과 입력

`scripts/export_legacy_review_input.py --assignment <assignment> --output <packet>`으로 현재 원문 전용 packet을 먼저 만든다. Packet은 stem·모든 보기·키·보이는 해설 전체를 보존하며 숨은 truth와 원장의 기존 판정 metadata를 제외한다. 원본 전체 객체는 hash 계산 코드의 입력으로만 사용하고 모델에 전체 출력하지 않는다. Packet은 법적 근거 또는 독립성 인증서가 아니다. 금지된 기존 결론이 우발적으로 노출되면 해당 ID의 노출 한계·NOT_ASSESSED/HOLD를 기록하고 별도 실제 fresh 세션으로 재배정한다. 입력을 나중에 정리했다고 이미 발생한 노출을 지우지 않는다.

- 새 실제 감사 세션의 canonical task 이름을 actor_id/session_id에 정직하게 기록한다. Auditor=GPT, auditor_instance는 그 실제 세션을 구분하는 안정된 label이다. 같은 session을 새 파일마다 여러 독립 instance로 부풀리지 않는다. Author/editor가 자기 current content를 independent로 인증하지 않는다.
- 지정 assignment JSON의 정확한 ID 집합과 record hashes를 사용한다. 모든 원 stem, 모든 보기, 기존 key, core/각 보기 한국어 해설을 직접 읽는다. 보고서나 metadata의 기존 저자 판정을 법적 사실로 사용하지 않는다. 이전 author/independent 보고서 및 후보를 읽어 답을 상속하지 않는다. 필요하면 원 질문 자체의 공식 source URL/authority만 discovery에 사용한다. 원 질문의 `_statement_truth`는 독립 검증 근거가 아니다.
- 기본4정책 RELEASE_POLICY/AUDIT_WORKFLOW/SOURCE_USE_POLICY/QUESTION_AUTHORING_STANDARD 및 current style profile을 읽는다. AGENTS가 있으면 따른다. 공개 Pre-MPJE/회상/상업 bank 질문은 입력하지 않는다. NABP public formats는 style용이며 법률권위 아님.
- hash는 기존 question.content_sha256가 아니라 전체 원 질문 객체를 scripts/review_queue.digest()로 계산한 canonical record SHA다. Collection은 ledger.collection을 따른다. 예외적으로 보기5개도 모두 읽는다.

## 법규·편집 판단

각 선택지의 주체·조건·행위·예외·기한·기산점을 현재 공식 primary source에 대조한다. Allowed/required/prohibited를 구분하고 unstated facts를 보태지 않는다. INCORRECT 극성/SATA 조합/단일정답 유일성, federal vs MA, 기존 설명과 각 distractor 근거를 평가한다. 실제 결함이 없으면 KEEP 가능하며 반복·숫자라는 이유만으로 일괄 실패시키지 않는다. 근거 불명확은 HOLD 또는 SOURCE_BLOCKED, NOT_ASSESSED를 YES로 바꾸지 않는다.

공식 HTTPS URL·exact section·실제 review date·applicable effective date 또는 version/commencement 미확정 한계를 기록한다. 403/404/HTTP200 PageNotFound/크레딧 부족은 실제 확인으로 세지 않는다. Firecrawl 크레딧이 부족하면 정상 proxy/TLS를 유지한 공식 HTTP 직접 조회를 사용한다. 같은날 genuine official raw cache를 다시 읽을 수 있지만 새 live retrieval이라고 쓰지 않는다. Vendor/USP 재배포 제한 자료는 URL·원 payload SHA·정확한 구획·직접 작성한 사실검토 memo로 보존하고 full copyrighted raw를 public commit하지 않는다.

현실성은 current style profile의10기준을 각 문항 사실에 대해 따로 평가한다. criteria: jurisprudence_reasoning, practice_plausibility, authentic_distractors, wording_not_guessable, reasoning_not_trivia, natural_rule_combination, appropriate_drug_context, distinct_from_bank, not_schedule_flashcard, public_style_without_copying. 각 criterion 이유를 한국어로 기록한다. PASS는10개 모두 확인해 true일 때만. 기존 intentionally archived family variants의 존재만으로 자동 FAIL하지 않고, 실제 판단·팩트·공유 wording과 default pool 맥락을 평가한다. Canonical439 및 public bank의 nearest duplicate 후보를 측정한 뒤 실제 가까운 원문을 읽어 비교하며, 자동 similarity 점수를 semantic verdict로 바꾸지 않는다. 미실시 비교는 NOT_RUN으로 기록하고 확인하지 않은 criterion을 PASS로 만들지 않는다.

## 보고서 형식

Top-level 필수값:

```
stage: independent-legacy
independent_of_authors: true
auditor: GPT
auditor_instance: stable actual-session label
actor_provenance: {actor_id: claim worker exact string, session_id: actual canonical task name}
canonical_audit: false
canonical_release_credit: 0
reviewed_at: actual YYYY-MM-DD
sources: [{official_url, exact_section/coverage, law_checked_date, effective_date/version+unknown basis, evidence_path, evidence_sha256, retrieval provenance}]
records: [...]
```

각 record는 question_id, record_sha256, read_scope, family_id를 가진다. legal_review: existing_answer_correct=YES|NO|AMBIGUOUS|NOT_ASSESSED; stored_key; independently_expected_key; per-choice findings(실제 option text 또는 hash, 지원 여부, 한국어 이유, exact section/URL/date/evidence binding); authorities[]; verdict=KEEP|MINOR_EDIT|MAJOR_REWRITE|HOLD|DELETE; finding_ko; blocker(없으면 null); original_explanation_review(core 및 모든 distractor 전문 읽음·오류/범위판정)를 기록한다. realism_review는 verdict=PASS|FAIL|NOT_ASSESSED, decision, criteria10개, criterion_findings_ko와 실제 duplicate evidence를 기록한다. safe_hold_recommended/release_eligible:false/required_next_action_ko도 구분한다. Sourceblocked를 무시하는 positive summary 금지.

Schema/style profile 파일의 version·semantic hash·file SHA를 고정한다. Stage 증거는 canonical admission이나 RELEASED gate가 아니다. 모든 기록은 원문/키/기존 부정감사를 바꾸지 않는다. 보류 source와 editor fix는 별도 후속 작업이며 감사자가 candidate를 직접 고치지 않는다.

## 제출과 재개

원본이나 공유 generated/queue를 수정하지 않는다. 보고서/evidence를 commit하고 root에 worker commit40자리와 report SHA를 전달한다. Manifest JSON은 `/tmp/independent-phase1-LETTER-result.json`처럼 별도 지정 위치에 쓴다:

```
{stage, independent_of_authors:true, auditor, auditor_instance, actor_provenance,
 question_hashes: assignment.question_hashes, worker_commit: exact40sha,
 results:[{question_id, disposition:INDEPENDENT_ASSESSED|HOLD|SOURCE_BLOCKED|NEEDS_REMEDIATION,
 evidence_path: repository-relative report, evidence_sha256: raw report SHA}]}
```

법규 불명확은 HOLD/SOURCE_BLOCKED, 실제 법규/현실성 결함은 NEEDS_REMEDIATION, 확인된 감사 결과는 INDEPENDENT_ASSESSED로 분리한다. 결과를 곧바로 release 승격하지 않는다. Root만 현재 lease/token으로 submit하고 Git 증거를 순차 integrate한 뒤 원장에 독립 assessment를 등록한다. 원장 반영 전 다음 plan은 차단된다. 실제 미실행 검사·network 조회·독립 단계는 NOT_RUN으로 기록한다.
