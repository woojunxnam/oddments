# Fresh reviewer 입력·제출 계약

이 문서는 reviewer 전용이며 기존 판정이나 기대 정답을 제공하지 않습니다. Controller scope, 이전 보고서, 원장, notice, 다른 reviewer 결론 및 숨은 author truth를 모델로 읽지 않습니다. 검증 프로그램이 이 자료를 내부적으로 읽어 hash를 대조할 수 있지만 내용을 출력해서는 안 됩니다. 독립성은 실제 새 세션 provenance와 root의 실제 배정에 기반하며 문자열이나 검증 PASS가 인증하지 않습니다.

입력은 root가 제공한 blinded assignment, visible packet, 네 기본 정책, 현재 style profile입니다. Visible packet의 원 stem·모든 영어 보기·저장 key·보이는 한국어 core/모든 choice rationale/learning boundary를 전부 읽습니다. 수정하지 않습니다. `nearest_visible`은 canonical439/public2349 전체에서 stem token cosine으로 찾은 각 pool의 상위3 후보입니다. 점수는 후보 탐색일 뿐 판정이 아닙니다. 가까운 후보6개의 stem과 모든 보기 원문을 실제로 읽고 구체적으로 비교합니다. 자신이 배정받은 원문과 비교한 실제 사실을 한국어로 기록합니다.

10개 기준은 `jurisprudence_reasoning`, `practice_plausibility`, `authentic_distractors`, `wording_not_guessable`, `reasoning_not_trivia`, `natural_rule_combination`, `appropriate_drug_context`, `distinct_from_bank`, `not_schedule_flashcard`, `public_style_without_copying`입니다. 각 기준은 true/false/null과 개별 한국어 이유를 가집니다. PASS/KEEP는 전부 true이고 실제 공개 형식 확인 및 비교를 완료했을 때만 가능합니다. 실제 결함은 FAIL과 MINOR_EDIT/MAJOR_REWRITE/HOLD/DELETE, 확인하지 못한 기준은 NOT_ASSESSED 또는 HOLD와 명시적 blocker로 남깁니다. 보호된 시험·회상·상용 문항은 열거나 사용하지 않습니다.

`https://nabp.pharmacy/programs/examinations/mpje/take-the-mpje-exam/`의 공개 형식을 직접 확인하고 자신의 추상 memo만 public report에 보존합니다. 원 raw와 추출 text는 public commit하지 않습니다. Metadata는 official_url/final_url, 실제 status, retrieved_at/read_at(UTC aware), 원 raw_sha256/text_sha256, raw_path:null, text_path:null, retention:`PRIVATE_NOT_REDISTRIBUTED`, 실제 대상 형식을 읽었으면 document_identity_status:`OFFICIAL_FORMAT_TARGET_DIRECTLY_READ`를 기록합니다. Memo는 own_abstract_memo_ko, source_is_format_only:true, protected_material_not_used:true, reviewed_at을 기록합니다. 공개 형식은 법률권위가 아닙니다. 조회 실패는 실제 status/한계를 정직하게 기록하고 PASS로 만들지 않습니다.

보고서는 assignment의 `output_prefix` 아래 `report.json`, `format-memo.json`, `format-meta.json`만 작성합니다. `legal_retry_question_hashes`에 명시된 ID가 있을 때만 해당 ID의 별도 법규 재감사를 실제 수행하고 공식 government raw/text/meta를 같은 prefix에 추가합니다. 다른 ID에 법규 판정 필드를 넣지 않습니다. 보고서/근거 외 원본·공유 queue·generated 파일·visible 입력 packet을 worker commit에 넣지 않습니다.

Top-level 필수 필드:

```
purpose: assignment.purpose
stage: independent-legacy
independent_of_authors: true
auditor: GPT
auditor_instance: assignment.auditor_instance
actor_provenance: assignment.actor_provenance
native_assignment_binding: assignment의 job_id/sequence/question_hashes/stage/worker/worker_branch/attempt 정확7필드
scope_raw_sha256: assignment.scope_binding.raw_sha256
question_hashes: assignment.question_hashes
style_profile: assignment.style_profile
canonical_audit: false
canonical_release_credit: 0
legal_audit_credit: 0
key_assessment_credit: 0
new_original_read_credit: 0
release_eligible: false
fresh_session_fork_turns: none
prior_conclusions_read: false
hidden_truth_read: false
reviewed_at: 실제 YYYY-MM-DD
completed_at: 실제 aware timestamp
public_format_evidence: memo_path/memo_sha256/metadata_path/metadata_sha256
records: 모든 배정 ID 각각1행
```

각 row는 question_id, record_sha256, visible_content_sha256(packet의 값), release_eligible:false, read_scope, realism_review를 가집니다. read_scope는 original_stem/stored_key_read/complete_core_reasoning_read/learning_boundary_read:true, all_choices_read/all_choice_explanations_read:실제 보기 ID 순서 전체, prior_question_author_or_independent_verdicts_read/hidden_statement_truth_read:false입니다.

realism_review에는 verdict, decision, criteria10개, criterion_findings_ko10개, finding_ko, 제한 시 blocker, duplicate_evidence를 기록합니다. duplicate_evidence에는 canonical_pool_count:439, public_pool_count:2349, pool_visible_sha256:packet 값, canonical/public 각각 후보3행(question_id, visible_sha256, stem_and_all_choices_read:true, 실제 comparison_ko)이 필요합니다. NOT_ASSESSED/HOLD도 시도한 비교와 확인 한계를 개별 이유에 기록합니다. 읽지 않은 후보에 true를 쓰지 않습니다. 후보 원문에 접근할 수 없으면 controller에 입력 장애를 알리고 완료했다고 제출하지 않습니다.

법규 재감사 ID에만 legal_review를 기록합니다. actual stored_key/independently_expected_key, question_type, CORRECT/INCORRECT polarity, verdict/기존 key의 YES/NO/AMBIGUOUS/NOT_ASSESSED, finding_ko, prior_conclusions_read/hidden_truth_read:false, 원 core/모든 rationale/learning boundary 실독 판정이 필요합니다. 모든 선택지는 choice_id, 정확 option_text_sha256, proposition_supported(bool/null), 한국어 finding, authority_refs를 가집니다. Authorities는 source_id, official government HTTPS URL, exact_section, law_checked_date, effective_date_or_version_basis(별도 효력일 미확정은 명시), raw/text/metadata path와 SHA를 결박합니다. Metadata는 official_url, raw_path/raw_sha256, text_path/text_sha256, status:200, method, 실제 retrieved_at/read_at, document_identity_status:`OFFICIAL_TARGET_PROVISIONS_DIRECTLY_READ`를 가집니다. 자료나 독립성 한계가 있으면 HOLD/NOT_ASSESSED와 빈 expected key를 유지합니다. 공식 문서를 실제로 대조하지 않은 key는 YES/NO로 판정하지 않습니다.

Worker commit 후 scratch의 result envelope는 stage/provenance/zero-credit/release_eligible 필드, question_hashes, worker_commit(정확40SHA), result_path:`output_prefix/result.json`, results:[question_id, disposition, evidence_path:`output_prefix/report.json`, evidence_sha256]입니다. Result 파일은 worker commit에 넣지 않습니다. Read-only post-commit 검증은 controller repository를 --root로 지정하고 `python <controller-root>/scripts/realism_completion_review.py --root <controller-root> validate-worker --job <job-id> --result <scratch-result.json>`으로 실행합니다. 이는 보고서 계약 검증이며 현실성 PASS/법규 PASS를 만들어 내지 않습니다. 실제 원문 실독·조회·개별 판정은 reviewer가 수행합니다.
