# Fresh independent auditor handoff — Batch 3 tranche B3-A

Send everything inside the fenced block below as the first message of a **brand-new, isolated
Claude Code session**. The session that authored `MA-Q-0229`–`MA-Q-0261` must not run it, and no
other repository context may be pasted into it.

---

````text
You are a fresh independent MPJE audit session for the Massachusetts MPJE question bank at
https://github.com/woojunxnam/oddments

You are NOT the author of the questions you are auditing. You have not seen, and must not seek
out, the author's reasoning. Your independence is the entire value of this audit; if you break
the blind discipline below, the audit is void and the questions cannot be released.

Your auditor identity for every record you produce:
  auditor          = CLAUDE
  auditor_instance = CLAUDE-FRESH-B3A

## Exact boundary

Repository:                 https://github.com/woojunxnam/oddments
Branch your audit FROM:     520303fe457fb4320601bd2400afe1f51c32e63a
                            (the frozen authoring candidate; this exact commit, not a branch tip)
Freeze branch:              freeze/batch3-b3a-v1
                            (verify the package by its immutable blob id below, not by branch tip)
Tranche:                    BATCH3-B3A
Authorizing issue:          91
Audit scope:                INITIAL_BATCH   (33 questions, ordinary scope, no governance_authorization)
Questions under audit:      MA-Q-0229 through MA-Q-0261 inclusive — exactly 33, no others

Before any substantive work, verify:
  git fetch origin
  git cat-file -t 520303fe457fb4320601bd2400afe1f51c32e63a      # must be: commit
  git merge-base --is-ancestor 520303fe457fb4320601bd2400afe1f51c32e63a origin/freeze/batch3-b3a-v1

## HARD BLIND RULE — read this before touching the repository

Until you have committed and pushed your Phase-1 lock, the ONLY question content you may read is
the sanitized blind package. It lives on the freeze branch, so read it without checking that
branch out:

  git show origin/freeze/batch3-b3a-v1:audits/remediation/2026-08-19/B3A-BLIND-QUESTIONS.json

Verify it first, with commands that agree on every platform:
  git rev-parse origin/freeze/batch3-b3a-v1:audits/remediation/2026-08-19/B3A-BLIND-QUESTIONS.json
    must print  f72d246dedfd69b1c16797105545788f44ef5694
  git show origin/freeze/batch3-b3a-v1:audits/remediation/2026-08-19/B3A-BLIND-QUESTIONS.json | sha256sum
    must print  10554a021a9dad7af05a1d30adaa93d26c9973311bab6a21451e362da46c1d4e

Do NOT hash the working-tree file directly. A Windows checkout rewrites these files to CRLF, so a
raw working-tree hash is platform-dependent and will look like tampering when it is not. Every
sha256 published here is the LF content hash.

That single `git show` of the blind package is the one permitted exception to the no-git-show rule
below; it reveals no key, explanation, rule or taxonomy.

Before the lock is committed you must NOT open, grep, diff or otherwise read:
  - data/questions/ma-q-0229.json through data/questions/ma-q-0261.json
  - any data/rules/*.json
  - audits/remediation/2026-08-19/BATCH3-B3A-AUTHORING-REPORT.json
  - audits/remediation/2026-08-19/B3A-POSTLOCK-DEPENDENCIES.json
  - audits/controller/ISSUE-83-CONTROLLER-LEDGER.json
  - audits/coverage/2026-08-19/BATCH3-PLAN-V1.json
  - site/generated/questions.json
  - data/exam_style/question_family_matrix.json
  - GitHub Issue #91, Issue #83, or any pull request body, comment or commit message
  - git log, git show or any diff touching these questions or their rules
  - anything else on the freeze branch besides the blind package

You may freely use current official primary sources on the open web at any time. That is the
point: solve the items the way a candidate would, from the law.

If you accidentally read any sealed item before locking, say so plainly, stop, and report that the
blind phase is compromised. Do not paper over it.

## PHASE 1 — blind solve and immutable lock

1. Read the blind package.
2. For each of the 33 items, research current official Massachusetts and federal authority
   independently and decide the answer yourself.
   - SBA items: choose exactly one choice ID.
   - SATA items: choose every choice ID you believe correct.
3. Write your answers and reasoning to:
     audits/remediation/2026-08-19/CLAUDE-FRESH-B3A-PHASE1-BLIND-LOCK.json
   with this shape:
     {
       "phase": "PHASE_1_BLIND_LOCK",
       "audit_date": "<ISO date>",
       "auditor": "CLAUDE",
       "auditor_instance": "CLAUDE-FRESH-B3A",
       "tranche": "BATCH3-B3A",
       "represented_candidate_sha": "520303fe457fb4320601bd2400afe1f51c32e63a",
       "blind_package_sha256": "10554a021a9dad7af05a1d30adaa93d26c9973311bab6a21451e362da46c1d4e",
       "blind_package_blob": "f72d246dedfd69b1c16797105545788f44ef5694",
       "freeze_branch": "freeze/batch3-b3a-v1",
       "freeze_head_observed": "<output of: git rev-parse origin/freeze/batch3-b3a-v1>",
       "questions": [
         {"question_id": "MA-Q-0229", "selected_choice_ids": ["<...>"],
          "reasoning": "<your own reasoning>", "authorities_consulted": ["<official URL>", "..."]}
         /* ... one entry per question, all 33 ... */
       ],
       "canonical_key_inspected_before_lock": false,
       "canonical_explanation_inspected_before_lock": false,
       "canonical_rules_inspected_before_lock": false,
       "author_reasoning_inspected_before_lock": false,
       "contamination_status": "CLEAN",
       "attestation": "I solved all 33 items only from the sanitized blind package and current official sources, and opened none of the sealed items before writing this lock."
     }

   If any of those four booleans would be true, set "contamination_status": "COMPROMISED", state
   exactly what you read, and stop. Do not continue under this auditor instance.
4. Commit and push it on a new branch:
     git checkout -b audit/batch3-b3a-claude-fresh-b3a 520303fe457fb4320601bd2400afe1f51c32e63a
     git add audits/remediation/2026-08-19/CLAUDE-FRESH-B3A-PHASE1-BLIND-LOCK.json
     git commit -m "audit: Phase-1 blind lock for Batch 3 B3-A (CLAUDE-FRESH-B3A)"
     git push -u origin audit/batch3-b3a-claude-fresh-b3a
   Your lock is immutable from this point: never amend, rebase or force-push it, and never change a
   Phase-1 answer after seeing the canonical key.

## PHASE 2 — unseal

Only now may you open the canonical records, the whole bank for comparison, and:
  git show origin/freeze/batch3-b3a-v1:audits/remediation/2026-08-19/B3A-POSTLOCK-DEPENDENCIES.json
  git show origin/freeze/batch3-b3a-v1:audits/remediation/2026-08-19/B3A-LEGAL-CONTRACT.json
    sha256 bf72ddadf3dbe874ccbdbb0b01879d9382c8417724b38f2255d9d425cd8a1103
  git show origin/freeze/batch3-b3a-v1:audits/remediation/2026-08-19/B3A-REALISM-CONTRACT.json
    sha256 7c12e52860342b6ae17b4ec66e7c11d00ec0843025bb963872ea865d533b2876
  git show origin/freeze/batch3-b3a-v1:audits/remediation/2026-08-19/B3A-CLEAN-FREEZE-MANIFEST.json
    sha256 0c4432146a513ecca854b82868c94b0be34e700643e5d603143583a58fb14a6b

Still do NOT read the authoring report, the controller ledger, the plan artifact, Issue #91,
Issue #83, PR bodies, or commit messages and diffs explaining why these questions were written.

Recompute every question hash and confirm each matches the manifest:
  python -c "import sys;sys.path.insert(0,'scripts');from qa_common import DATA,load_json,question_audit_hash;print({('MA-Q-%04d'%n):question_audit_hash(load_json(DATA/'questions'/('ma-q-%04d.json'%n))) for n in range(229,262)})"
If any hash differs from the manifest, STOP and report STALE INPUT.

## PHASE 3 — LEGAL verification

For every question verify the keyed answer and the explanation against CURRENT official primary
authority that you locate yourself. Do not rely on a rule record's summary as proof; open the
official source and confirm the proposition is still current. Verify every SATA option
individually, and verify the exact actor, duty, condition and exception each item turns on.

Write:  data/audits/AUDIT-CLAUDE-FRESH-B3A-LEGAL-INITIAL-2026-08-19.json

It must validate against schemas/audit.schema.json with:
  audit_id         "AUDIT-CLAUDE-FRESH-B3A-LEGAL-INITIAL-2026-08-19"
  auditor          "CLAUDE"
  auditor_instance "CLAUDE-FRESH-B3A"
  audit_date       "<ISO date>"
  audit_scope      "INITIAL_BATCH"      <-- ordinary scope; do NOT add governance_authorization
  review_type      "LEGAL_VERIFICATION"
  independent      true
  audit_status     "FULLY_ADJUDICATED"
  question_ids     all 33, MA-Q-0229 through MA-Q-0261
  question_hashes  the 33 hashes you recomputed
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

Compare each question against the ENTIRE canonical bank in data/questions (261 records at the
represented candidate). Do not sample, and do not substitute the existing duplicate report.

Write:  data/audits/AUDIT-CLAUDE-FRESH-B3A-REALISM-INITIAL-2026-08-19.json

Same identity, question_ids and question_hashes as the legal record, plus:
  review_type   "REALISM_REVIEW"
  audit_scope   "INITIAL_BATCH"
  style_profile {"profile_id": "MPJE-MA-PRE2027", "content_version": 1,
                 "content_hash": "293be8fdcd39af2255a22a0423b7123d5cfcf7c0e6c561872eb0ef04e745015c"}
  results       one entry per question with exactly:
                Question_ID, Verdict, Severity, Realism_Verdict, Reviewed_Date, Criteria, Notes

Criteria must contain all ten booleans, each independently assessed — never defaulted to true just
to satisfy the schema:
  jurisprudence_reasoning, practice_plausibility, authentic_distractors, wording_not_guessable,
  reasoning_not_trivia, natural_rule_combination, appropriate_drug_context, distinct_from_bank,
  not_schedule_flashcard, public_style_without_copying

Realism_Verdict PASS requires every criterion true. In Notes, name the closest comparison question
IDs you found and say why the item is or is not materially distinct. These items are Area 1
licensure, personnel and continuing education content, so pay particular attention to the existing
technician-scope and prescriber-authority families.

## PHASE 5 — report

Run and report:
  python scripts/validate_all.py
  python -m pytest -q
  python scripts/generate_artifacts.py --write && git diff --exit-code

Your audit branch must contain ONLY the Phase-1 lock, the two canonical audit records, and any
minimal provenance note. Do not edit questions, rules, the family matrix, generated content,
release state, the preview allowlist, validators, the schema, or MA-Q-0028.

Open a DRAFT pull request into batch3/b3a-author titled:
  "audit: CLAUDE-FRESH-B3A independent legal + full-bank realism review (MA-Q-0229..MA-Q-0261)"

Then report back and STOP. Do not release the questions; governance does that separately.

Report exactly: audit branch and HEAD SHA; Draft PR URL; Phase-1 lock commit SHA and blob id; per
question whether your blind answer matched the canonical key; LEGAL Verdict and
Existing_Answer_Correct per question; REALISM Verdict, Realism_Verdict and the ten criteria per
question; closest comparison IDs; the official sources you actually opened; validate_all, pytest
and freshness results; and contamination status.

## What qualifies for release

Each question qualifies only with, on its current content hash:
  LEGAL   Verdict = KEEP and Existing_Answer_Correct = YES
  REALISM Verdict = KEEP and Realism_Verdict = PASS with all ten criteria true

Do not manufacture a pass. A well-evidenced MINOR_EDIT, MAJOR_REWRITE, DELETE or realism FAIL is a
successful audit and will be acted on by governance: only the failing items are repaired and
re-audited, so a finding does not cost the tranche. If your blind answer disagrees with the
canonical key, that disagreement is the finding — record it, do not retrofit your Phase-1 lock.

Do not edit the questions, the rules, the schema or any validator. You are the auditor, not the
editor.
````

---

## Notes for governance (not part of the auditor prompt)

- B3-A uses ordinary `INITIAL_BATCH`. At 33 questions it sits inside the 30–40 band, so **no**
  `TARGETED_INITIAL_BATCH` registration is required and the auditor branches directly from the
  candidate SHA.
- Reserved auditor instance `CLAUDE-FRESH-B3A`. Release policy uses
  `distinctness_basis: AUDITOR_INSTANCE` with no required auditor type, so one isolated instance
  completing both reviews satisfies the gate.
- While B3-A is being audited, the controller continues authoring B3-B (`MA-Q-0262`–`MA-Q-0294`).
