# 기본 연습 문항의 실제 별도 세션 검토 — wave9

Root가 현재 authoritative ledger와 publication/selection SHA에 따라 독립 미검토
기본 문항 160개를 40개씩 배정했다. 연속 번호를 가정하지 않는다. 네 job의
sequence는 30–33이며 `independent-legacy-work-queue.json`에 고정되어 있다.
각 worker는 자신의 assignment와 visible packet만으로 시작하는 실제 새 세션이다.
이 문서는 법적 정답이나 이전 검토자 판정을 제공하지 않는다.

먼저 `docs/RELEASE_POLICY.md`, `docs/AUDIT_WORKFLOW.md`,
`docs/SOURCE_USE_POLICY.md`, `docs/QUESTION_AUTHORING_STANDARD.md`, 현재
`reports/full-corpus-review/progress.json`과 자신의 assignment를 읽는다.
보고·검토 근거는 한국어, 원문 문항은 영어다. 원문·키·기존 해설·hash·history를
worker가 수정하지 않는다. 다른 reviewer의 보고서나 author의 숨은 truth 배열을
법적 근거 또는 독립 판단 대신 읽지 않는다.

각자의 입력은 `reports/full-corpus-review/phase9-LETTER-evidence/assigned-visible-input.json`이다.
Root가 정확한 current whole-record hash와 원래 stem·모든 choices·저장 key·전체
한국어 explanation을 추출했다. 법규 근거가 아니라 검토할 원문이다. 필요한 원
source/notes 링크는 해당 원 bank에서 찾되 hidden author judgement를 가져오지 않는다.

모든 stem과 모든 option을 읽고, 각 proposition을 current Massachusetts/federal
공식 primary 원문과 대조한다. 수치·기한·주체·면허·예외·의무/권고·연방/주 차이를
구별한다. CORRECT/INCORRECT 극성과 SATA의 정확한 조합을 별도로 계산한다.
한국어 core와 모든 distractor rationale 및 learning boundary도 읽는다.
공식 URL, exact section, 적용 시행일/버전 또는 실제 미확정 한계, 실제 review date와
timezone-aware retrieval/read timestamp, 실제 HTTP 상태·문서 정체·raw SHA를 기록한다.

정상 검증 TLS를 쓰는 urllib 등으로 공식 자료를 확보할 수 있다. 검색 도구 실패를
법적 근거로 쓰지 않는다. HTTP403/404나 200 access/error page는 원문 확인이 아니다.
확보한 공식 정부 문서의 원 payload·추출문·retrieval metadata를 자기 evidence 경로에
보존한다. 같은 날 실제 official retained bytes를 재독했다면 원 retrieval timestamp와
cache 재독임을 밝힌다. 미확인·모순·중요 시행일 미확정은 HOLD/SOURCE_BLOCKED와
정확한 blocker로 남긴다. citation·effective date·read assertion을 만들어내지 않는다.

현재 style profile/blueprint를 읽고 현실성도 별도로 판단한다. 공개 허가된 NABP
sample/blueprint 안내로 공개 형식만 확인하며 보호된 exam/recalled/Pre-MPJE/commercial
item을 복사하지 않는다. 저작권 raw는 repo에 새로 공개하지 않고 실제 확인 URL·SHA·
최소 scope와 자체 작성한 memo만 보존한다. 각 문항의 실제 상황, 역할/행동/법적
결정, distractor plausibility, answer cue/복제/내용 없는 문구를 직접 평가한다.
유사도 도구는 후보 찾기 용도이며 최종 판정을 대신하지 않는다. 가까운 stem과
전 choices를 직접 읽어 중복/맥락을 평가한다. 새로운 학습범위를 허위로 주장하지 않는다.

자기 실제 세션이 이전에 해당 원문의 whole-key 결론을 평가했거나 author/editor였다면
그 이력을 기록하고 새 독립 key 판단으로 세지 않는다. 새 identity 문자열로 우회하지 않는다.
Source가 검증돼도 결함이 있으면 KEEP을 강제하지 않는다. 잘못된 키, 모호한 범위,
해설 오류, 현실성 문제를 구별하고 구체적인 후속 조치와 필요한 새 상황을 제안한다.
현재 default에 포함된 문항에서 부정·모호·차단 판정을 발견하면 root에 즉시 ID,
보기, 공식 근거와 결함을 알린다. 최종 batch 완성을 기다려 알려진 결함을 숨기지 않는다.

보고서 경로는 `reports/full-corpus-review/independent-phase9-LETTER-review.json`,
자기 evidence는 위 `phase9-LETTER-evidence/` 아래 새 파일만 사용한다.
보고서는 `stage: independent-legacy`, 실제 actor/session과 `auditor: GPT`, 실제 새
`auditor_instance`, `independent_of_authors: true`, `canonical_audit: false`,
`canonical_release_credit: 0`, `author_review_credit: 0`, 실제 review date를 가진다.
정확히 배정된 40 records 각각은 question_id/current record_sha256, 원문 실독 scope,
legal_review(existing_answer_correct, verdict, stored/expected keys, polarity,
모든 option별 원문·truth/support·한국어 finding·exact primary authorities,
전체 원해설 검토·blocker), realism_review(verdict·실제 근거),
구체적인 required_next_action_ko를 포함한다. 판정은 서로 다른 질문에 자동 복제하지 않는다.
Root의 current source validator가 요구하는 raw/input/evidence bindings도 포함한다.

Worker는 공유 queue, ledger, generated, release 정책, 원 questions/sources를 쓰지 않는다.
자기 branch에서 보고서·새 evidence만 commit/push하고 native validator로 exact scope,
hash, 실제 actor와 source bytes를 확인한다. 잘못된 기존 generated를 수정하거나 QA를
완화하지 않는다. 전체 repo QA·통합·배포는 root가 맡는다.

커밋 후 자기 `/tmp/independent-phase9-LETTER-result.json`에 미커밋 envelope를 만든다.
stage/실제 actor/auditor/instance/independence 선언과 canonical credit0, exact
question_hashes, 실제 40자 worker_commit, 40 results(question_id,
INDEPENDENT_LEGACY_ASSESSED 또는 실제 native 허용 disposition,
evidence_path/evidence_sha256)를 제공한다. `scripts/review_queue.py`의 실제 계약을
확인한다. Commit 안에 자기 SHA를 넣지 않는다. Root만 submit→증거 통합→원 envelope
보존→sequence 순서 integrate한다. 보고서 완료/원장 통합은 canonical RELEASED가 아니다.
