# Fresh independent auditor handoff — Pre-Batch3 T3 diversity tranche

This file is the ready-to-send task for a **new, isolated auditor session**. The session that
authored `MA-Q-0227` and `MA-Q-0228` must not run it.

Send everything inside the fenced block below as the first message of a brand-new session. Do
not paste any other repository context into that session.

---

````text
You are a fresh independent MPJE audit session for the Massachusetts MPJE question bank at
https://github.com/woojunxnam/oddments

You are NOT the author of the questions you are auditing. You have not seen, and must not seek
out, the author's reasoning. Your independence is the entire value of this audit; if you break
the blind discipline below, the audit is void and the questions cannot be released.

Your auditor identity for every record you produce:
  auditor          = CLAUDE
  auditor_instance = CLAUDE-FRESH-COV-T3-A

## Exact boundary

Repository:                   https://github.com/woojunxnam/oddments
Freeze branch:                freeze/pre-batch3-coverage-t3-v1
                              (verify the package by its immutable blob id below, not by branch tip;
                               the tip may advance with packaging-only commits)
Branch your audit FROM:       36b3ea85229609afb08772a566cca2eb6fbe1be8
                              (head of remediation/pre-batch3-coverage-t3-diversity; it carries the
                               TARGETED_INITIAL_BATCH authorization your records need in order to validate)
Represented candidate SHA:    f13c91c2635ea153a1ea19d9dfb34bcbe12f30c2
                              (the frozen authoring content the blind package represents; this exact value
                               goes in governance_authorization.represented_candidate_sha, NOT the base SHA)
Tranche:                      PRE-BATCH3-COVERAGE-T3-DIVERSITY
Authorizing issue:            86
Questions under audit:        MA-Q-0227, MA-Q-0228   (exactly these two, no others)

Before any substantive work, verify:
  git cat-file -t f13c91c2635ea153a1ea19d9dfb34bcbe12f30c2   # must be: commit
  git merge-base --is-ancestor f13c91c2635ea153a1ea19d9dfb34bcbe12f30c2 36b3ea85229609afb08772a566cca2eb6fbe1be8
  git rev-parse origin/remediation/pre-batch3-coverage-t3-diversity   # must be 36b3ea85229609afb08772a566cca2eb6fbe1be8

The only difference between the candidate SHA and your base SHA is the governance registration of
this tranche in scripts/validate_audits.py plus its tests. Neither question changed: confirm that
yourself in Phase 2 with the hash check below.

Required question content hashes at the represented candidate SHA:
  MA-Q-0227  e4366cb456fcb126e4a96988320d32dcf0258d432acb1df73ecca7bee3c2065e
  MA-Q-0228  bb334d740968d63ec5861ef1713adf672383bf572715daac0eec90f4cf8bead3

Recompute them yourself after Phase 2 with:
  python -c "import sys;sys.path.insert(0,'scripts');from qa_common import DATA,load_json,question_audit_hash;print({q:question_audit_hash(load_json(DATA/'questions'/(q.lower()+'.json'))) for q in ['MA-Q-0227','MA-Q-0228']})"
If either hash differs, STOP and report the mismatch. Do not audit content that has moved.

## HARD BLIND RULE — read this before touching the repository

Until you have committed and pushed your Phase-1 lock file, the ONLY question content you may
read is this sanitized blind package:

  audits/remediation/2026-08-19/T3-BLIND-QUESTIONS-PRE-BATCH3-COVERAGE-T3.json

It contains only question ID, type, stem and choices.

Verify it before reading it, with commands that give the same answer on every platform:
  git rev-parse origin/freeze/pre-batch3-coverage-t3-v1:audits/remediation/2026-08-19/T3-BLIND-QUESTIONS-PRE-BATCH3-COVERAGE-T3.json
    must print  c83757ce2c28cfde9e376c2ba1008771a93a63ed
  git show origin/freeze/pre-batch3-coverage-t3-v1:audits/remediation/2026-08-19/T3-BLIND-QUESTIONS-PRE-BATCH3-COVERAGE-T3.json | sha256sum
    must print  e6f8cc8852d474287384df7718ca8e96096bb741a1e41310631f6cc252d83851

Do NOT hash the working-tree file directly. On a Windows checkout Git rewrites these files to
CRLF, so a raw working-tree hash is platform-dependent and will look like tampering when it is
not. Every sha256 published here is the LF content hash, which is what the two commands above
produce on Linux, macOS and Windows alike.

Before the lock is committed you must NOT open, grep, diff or otherwise read:
  - data/questions/ma-q-0227.json or data/questions/ma-q-0228.json
  - data/rules/ma-bedside-delivery.json or data/rules/ma-central-fill-dispensing-route.json
  - audits/remediation/2026-08-19/PRE-BATCH3-COVERAGE-T3-DIVERSITY-AUTHORING-REPORT.json
  - audits/remediation/2026-08-19/PRE-BATCH3-COVERAGE-T3-V1-POSTLOCK-DEPENDENCIES.json
  - site/generated/questions.json
  - GitHub Issue #86, Issue #83 or any pull request body, comment or commit message
  - git log, git show or any diff touching the two questions or the two new rules

You may freely use current official primary sources on the open web at any time. That is the
point: solve the items the way a candidate would, from the law.

If you accidentally read any sealed item before locking, say so plainly, stop, and report that
the blind phase is compromised. Do not paper over it.

## PHASE 1 — blind solve and immutable lock

1. Read the blind package.
2. For each of MA-Q-0227 and MA-Q-0228, research current official Massachusetts and federal
   authority independently and decide the answer yourself.
   - MA-Q-0227 is single-best-answer: choose exactly one choice ID.
   - MA-Q-0228 is select-all-that-apply: choose every choice ID you believe correct.
3. Write your answers and reasoning to:
     audits/remediation/2026-08-19/CLAUDE-FRESH-COV-T3-A-PHASE1-BLIND-LOCK.json
   using this exact shape:
     {
       "phase": "PHASE_1_BLIND_LOCK",
       "audit_date": "<ISO date>",
       "auditor": "CLAUDE",
       "auditor_instance": "CLAUDE-FRESH-COV-T3-A",
       "tranche_id": "PRE-BATCH3-COVERAGE-T3-DIVERSITY",
       "represented_candidate_sha": "f13c91c2635ea153a1ea19d9dfb34bcbe12f30c2",
       "blind_package_sha256": "e6f8cc8852d474287384df7718ca8e96096bb741a1e41310631f6cc252d83851",
       "blind_package_blob": "c83757ce2c28cfde9e376c2ba1008771a93a63ed",
       "freeze_branch": "freeze/pre-batch3-coverage-t3-v1",
       "freeze_head_observed": "<output of: git rev-parse origin/freeze/pre-batch3-coverage-t3-v1>",
       "audit_base_sha": "36b3ea85229609afb08772a566cca2eb6fbe1be8",
       "questions": [
         {"question_id": "MA-Q-0227", "selected_choice_ids": ["<...>"], "reasoning": "<your own reasoning>",
          "authorities_consulted": ["<official URL>", "..."]},
         {"question_id": "MA-Q-0228", "selected_choice_ids": ["<...>"], "reasoning": "<your own reasoning>",
          "authorities_consulted": ["<official URL>", "..."]}
       ],
       "canonical_key_inspected_before_lock": false,
       "canonical_explanation_inspected_before_lock": false,
       "canonical_rules_inspected_before_lock": false,
       "author_reasoning_inspected_before_lock": false,
       "contamination_status": "CLEAN",
       "attestation": "I solved both items only from the sanitized blind package and current official sources. I did not open the canonical question files, the canonical rule files, the authoring report, the post-lock dependency reveal, the generated site payload, Issue #86, Issue #83, any pull request body or comment, or any git log/diff describing these questions, before writing this lock."
     }

   If any of those four booleans would be true, set "contamination_status": "COMPROMISED",
   state exactly what you read, and stop. Do not continue the audit under this auditor instance.
4. Commit and push it on a new branch:
     git checkout -b audit/pre-batch3-coverage-t3-claude-fresh-cov-t3-a 36b3ea85229609afb08772a566cca2eb6fbe1be8
     git add audits/remediation/2026-08-19/CLAUDE-FRESH-COV-T3-A-PHASE1-BLIND-LOCK.json
     git commit -m "audit: Phase-1 blind lock for Pre-Batch3 T3 (CLAUDE-FRESH-COV-T3-A)"
     git push -u origin audit/pre-batch3-coverage-t3-claude-fresh-cov-t3-a
   Record the resulting commit SHA. Your lock is immutable from this point: never amend,
   rebase or force-push it, and never change a Phase-1 answer after seeing the canonical key.

## PHASE 2 — unseal

Only now may you open the canonical records and the post-lock dependency reveal:
  audits/remediation/2026-08-19/PRE-BATCH3-COVERAGE-T3-V1-POSTLOCK-DEPENDENCIES.json
  data/questions/ma-q-0227.json, data/questions/ma-q-0228.json
  data/rules/*.json, data/blueprint.json, data/exam_style/mpje_style_profile.json

Still do NOT read the authoring report, Issue #86, Issue #83, PR bodies, or commit messages and
diffs explaining why these questions were written. Those carry author reasoning.

Recompute both question hashes and confirm they match the values above.

Your audit contracts, which state every required field:
  audits/remediation/2026-08-19/T3-LEGAL-CONTRACT-PRE-BATCH3-COVERAGE-T3.json
    sha256 c3b4dfc01c19123aabb1fe4c91b6b7d5839ba730d31196705ab72cfb552d73b8
  audits/remediation/2026-08-19/T3-REALISM-CONTRACT-PRE-BATCH3-COVERAGE-T3.json
    sha256 535dcddf0c31f83f40bc99c6a82ac5719be393008e0f6a431ba683a3e80d4eb0
  audits/remediation/2026-08-19/PRE-BATCH3-COVERAGE-T3-CLEAN-FREEZE-V1-MANIFEST.json
    sha256 21e7cdf2a2433686304769b8c5df2a95d4d2870f2544688f18e61464b8ef51ea

## PHASE 3 — LEGAL verification

For each question, verify the keyed answer and the explanation against CURRENT official primary
authority that you locate yourself. Do not rely on the rule record's summary as proof; open the
official source and confirm the proposition is still current.

Write:  data/audits/AUDIT-CLAUDE-FRESH-COV-T3-A-LEGAL-TARGETED-INITIAL-2026-08-19.json

It must validate against schemas/audit.schema.json with:
  audit_id         "AUDIT-CLAUDE-FRESH-COV-T3-A-LEGAL-TARGETED-INITIAL-2026-08-19"
  auditor          "CLAUDE"
  auditor_instance "CLAUDE-FRESH-COV-T3-A"
  audit_date       "<ISO date>"
  audit_scope      "TARGETED_INITIAL_BATCH"        <-- NOT "REAUDIT"
  review_type      "LEGAL_VERIFICATION"
  independent      true
  audit_status     "FULLY_ADJUDICATED"
  governance_authorization {
    "tranche_id": "PRE-BATCH3-COVERAGE-T3-DIVERSITY",
    "authorizing_issue": 86,
    "represented_candidate_sha": "f13c91c2635ea153a1ea19d9dfb34bcbe12f30c2",
    "question_ids": ["MA-Q-0227", "MA-Q-0228"]
  }
  question_ids     ["MA-Q-0227", "MA-Q-0228"]
  question_hashes  the two hashes above
  results          one entry per question with exactly:
                   Question_ID, Verdict, Severity, Existing_Answer_Correct, authorities,
                   Problem, Proposed_Answer, Proposed_Rewrite, Proposed_Explanation

  Verdict                 KEEP | MINOR_EDIT | MAJOR_REWRITE | DELETE
  Severity                Low | Medium | High | Critical
  Existing_Answer_Correct YES | NO | PARTIALLY | NOT_ASSESSED
  Proposed_Answer         a string; for multi-select use comma-joined IDs in order, e.g. "A,B,E"
  Proposed_Rewrite / Proposed_Explanation  empty strings when there is nothing to rewrite
  authorities             at least one per question, each with authority, source_type,
                          exact_section, official_url (https), law_checked_date
  source_type             MA_STATUTE | MA_PROMULGATED_REGULATION | MA_BOARD_POLICY |
                          MA_DCP_GUIDANCE | FEDERAL_STATUTE | FEDERAL_REGULATION |
                          DEA_OFFICIAL | FDA_OFFICIAL | OTHER_OFFICIAL

## PHASE 4 — FULL canonical-bank REALISM review

Compare each question against the ENTIRE canonical bank in data/questions (228 records at the
represented candidate SHA). Do not sample, and do not substitute the existing duplicate report.

Write:  data/audits/AUDIT-CLAUDE-FRESH-COV-T3-A-REALISM-TARGETED-INITIAL-2026-08-19.json

Same identity, governance_authorization, question_ids and question_hashes as the legal record,
plus:
  review_type   "REALISM_REVIEW"
  style_profile {"profile_id": "MPJE-MA-PRE2027", "content_version": 1,
                 "content_hash": "293be8fdcd39af2255a22a0423b7123d5cfcf7c0e6c561872eb0ef04e745015c"}
  results       one entry per question with exactly:
                Question_ID, Verdict, Severity, Realism_Verdict, Reviewed_Date, Criteria, Notes

Criteria must contain all ten booleans, each independently assessed — never defaulted to true
just to satisfy the schema:
  jurisprudence_reasoning, practice_plausibility, authentic_distractors, wording_not_guessable,
  reasoning_not_trivia, natural_rule_combination, appropriate_drug_context, distinct_from_bank,
  not_schedule_flashcard, public_style_without_copying

Realism_Verdict PASS requires every criterion to be true. In Notes, state explicitly which
canonical question IDs are the closest comparisons you found and why the item is or is not
materially distinct from them.

## PHASE 5 — report

Run and report:
  python scripts/validate_all.py
  python -m pytest -q
  python scripts/generate_artifacts.py --write && git diff --exit-code

Commit both audit records on your audit branch, push, and open a pull request into
remediation/pre-batch3-coverage-t3-diversity titled:
  "audit: CLAUDE-FRESH-COV-T3-A independent legal + full-bank realism review (Q0227/Q0228)"

In the PR body state: your Phase-1 lock commit SHA, whether your blind answers matched the
canonical keys, both verdicts per question, the authorities you actually opened, and the closest
comparison IDs.

## What qualifies for release

Each question qualifies only with, on the current content hash:
  LEGAL   Verdict = KEEP and Existing_Answer_Correct = YES
  REALISM Verdict = KEEP and Realism_Verdict = PASS

Do not manufacture a pass. A well-evidenced MINOR_EDIT, MAJOR_REWRITE, DELETE or realism FAIL is
a successful audit and will be acted on by governance. If your blind answer disagrees with the
canonical key, that disagreement is the finding — record it, do not retrofit your Phase-1 lock.

Do not edit the questions, the rules, the schema or any validator. You are the auditor, not the
editor.
````

---

## Notes for governance (not part of the auditor prompt)

- The auditor identity is reserved as `CLAUDE-FRESH-COV-T3-A`. Release policy
  (`data/release_requirements.json`) uses `distinctness_basis: AUDITOR_INSTANCE` with
  `required_auditor_types: []`, so a Claude auditor instance satisfies the gate provided the
  session is genuinely isolated from the authoring session. If governance prefers cross-model
  independence, substitute a GPT instance and change `auditor` to `GPT` and `auditor_instance`
  accordingly; the contracts are otherwise model-neutral.
- The `TARGETED_INITIAL_BATCH` authorization for tranche `PRE-BATCH3-COVERAGE-T3-DIVERSITY`
  is registered in `scripts/validate_audits.py` and covered by five tests in
  `tests/test_targeted_initial_policy.py`. It merged as PR #87 into
  `remediation/pre-batch3-coverage-t3-diversity`, producing the audit base SHA
  `36b3ea85229609afb08772a566cca2eb6fbe1be8`. The audit schema is unchanged and ordinary
  `INITIAL_BATCH` remains 30–40.
- After the audit passes, the Issue #83 controller session resumes to register the evidence,
  guarded-release both questions, and rerun `scripts/prebatch3_final_coverage_gate.py` from the
  exact post-release SHA.
