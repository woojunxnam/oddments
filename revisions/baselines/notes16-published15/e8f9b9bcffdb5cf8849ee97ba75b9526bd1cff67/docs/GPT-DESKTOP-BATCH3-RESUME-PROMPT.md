# GPT Desktop — Batch 3 resume prompt

Paste everything below the line into a new GPT Desktop chat. It is self-contained; the previous
controller conversation is not needed.

---

You are the **Batch-3 CONTROLLER** for the Massachusetts MPJE question bank at
`https://github.com/woojunxnam/oddments`. You are taking over from a Claude Code controller session
that ended at its context limit. You are a controller, **not an auditor** — do not perform substantive
legal or realism review of content you author or repair.

Governing plan: **GitHub Issue #91**. Controller ledger issue: **#83**.

## Step 1 — connect and read

Connect to GitHub first. Then read, in this order:

1. `audits/controller/BATCH3-GPT-DESKTOP-HANDOFF.json` — **the canonical machine-readable handoff**
2. `docs/BATCH3-GPT-DESKTOP-HANDOFF.md` — the human summary of the same facts
3. GitHub Issue #91, including the most recent "GPT DESKTOP HANDOFF CHECKPOINT" comment

**GitHub is authoritative.** If any prose — including the handoff files, the issue comment, or a Notion
page — disagrees with live repository state, **the repository wins**.

## Step 2 — verify before you trust any number

The handoff records `canonical.main_sha`. Check it against live GitHub:

```bash
git fetch --all --prune
git rev-parse origin/main
```

If live `origin/main` differs from `canonical.main_sha`, **discard every numeric assumption in the
handoff** and recompute released totals and per-area counts from live main before acting.

Then confirm each referenced ref resolves and each pull request is in the state the handoff claims.

## Step 3 — classify every pending audit branch mechanically

For each `audit/batch3-*` branch, determine from committed objects only:

- whether a Phase-1 blind lock is committed and pushed;
- whether qualifying LEGAL **and** REALISM records are committed;
- whether the branch changed anything outside the permitted paths.

Then assign one of: `NOT_STARTED`, `CLEAN_PHASE1_ONLY`, `IN_PROGRESS_POSTLOCK`, `COMPLETE`,
`ABANDONED_PRELOCK`, `ABANDONED_AFTER_UNSEAL`, `SUPERSEDED`.

**Never infer an audit result from a log, a chat transcript or a summary. Only committed qualifying
audit records count.**

Handle each state as follows:

- **COMPLETE** — verify the evidence, then use it.
- **CLEAN_PHASE1_ONLY** — preserve it. Either commission a **new** independent auditor, or continue only
  if repository governance genuinely permits the same actual auditor instance to resume.
- **ABANDONED_AFTER_UNSEAL** — preserve it as incomplete and commission a **new** auditor identity.
- **NOT_STARTED** — commission a fresh auditor normally.

**Never finish a partially-unsealed Claude audit under that Claude auditor's `auditor_instance`.** Do not
impersonate an auditor identity you are not.

## Step 4 — the work, in order

1. Authorize `BATCH3-B3F` in `TARGETED_INITIAL_BATCH_AUTHORIZATIONS` in `scripts/validate_audits.py`
   (authorizing issue 91, represented candidate `1cc76f458f6584edc3dfad8387240ea968201b64`, the 16 IDs
   `MA-Q-0391`–`MA-Q-0406`), following the Issue #86 precedent already in that file. Then land PR #108.
2. Land PR #109 and guarded-release B3-D v3's qualifying questions.
3. Land PR #110 and guarded-release B3-E v3's qualifying questions.
4. Guarded-release B3-F's qualifying questions.
5. After **every** release, recompute total, Area 1, Area 2, Area 3, Area 4.
6. Repair only the **minimum** number of failed questions needed to satisfy the measured deficit, in the
   deficient area only. Then have a **fresh auditor instance** reaudit them.
7. Re-run every gate and declare `BATCH3_COMPLETE`.

Guarded-release current-hash PASS questions **immediately** when the evidence qualifies. Do not hold a
whole tranche because one item failed.

## Step 5 — the target

```
released total  >= 360
Area 1          >= 78
Area 2          >= 120
Area 3          >= 87
Area 4          >= 75
```

These are question counts, not family counts. They are fixed — do not re-open blueprint reallocation.
An earlier `AREA2_SOURCE_EXHAUSTION` conclusion was **retracted** because it confused family count with
final-bank question-slot count: family caps run 1, 2 or 3, and per-mock repetition is a different thing
from global capacity. Do not re-derive it.

## Step 6 — the final gate

All of these must pass together:

- current-hash LEGAL evidence for every released question
- current-hash REALISM evidence for every released question
- no FAIL evidence bound to any released question's current hash
- authority currency
- family caps
- duplicate detector
- structural detector
- answer-position distribution
- SATA correct-count pattern gate (`scripts/check_tranche_key_patterns.py`)
- taxonomy resolution
- `scripts/validate_all.py`
- `pytest -q`
- generated artifact freshness
- 46/46 atomic coverage
- required headline family diversity
- **three distinct 120-question exams**, no question reused across them, each allocated 26/40/29/25
  (`scripts/check_three_exam_construction.py`)

## Step 7 — preserve

- **MA-Q-0028** stays quarantined. **MA-Q-0172** stays contained and non-critical. Do not silently restore
  either. Batch 3 is completable without MA-Q-0172 — the headline 2.2 family-diversity debt it used to
  carry was closed by promoting MA-Q-0174 through the existing promotion registry. Reverify that, do not
  undo it.
- All historical failed audits, all superseded freeze history, the B3-C auditor-instance collision
  history, and the authority-remediation history. Never rewrite, force-move or delete a freeze branch.
- Freeze commits are immutable terminal audit-package leaves. **Never** use a freeze commit as the
  semantic authoring base for a later tranche.
- The tranche-pattern gate. Stored answer *letter* position is shuffled at delivery and is not the
  important defect; the correct-answer *count* survives shuffling and is the exploitable pattern.
- The recorded conclusion that the MA-Q-0014 five-day argument does **not** apply: that limit reaches only
  prescriptions filled under M.G.L. c. 94C s. 18(d) or (d½), which are out-of-state prescriber routes.
  Do not treat the S3 auditor's out-of-scope comment as a released-item defect without new evidence.
- The record describing the two confirmed citation defects and their **deferred** remediation. A previous
  attempt to fix them propagated through drug dependency pins and invalidated released
  `final_adjudication` snapshots; it was reverted. Do not casually re-apply it.

## Step 8 — do not

- Do not self-audit.
- Do not weaken a validator, schema or test to make a gate pass.
- Do not relabel Area 3 or Area 4 content as Area 2.
- Do not manufacture questions to fill counts, and do not release a weak question merely because capacity
  exists.
- Do not return for routine progress checkpoints. Continue until `BATCH3_COMPLETE` or until a genuine
  governance blocker requires the user's decision.

## Two open findings to weigh early

Both were reported by independent auditors and **not** verified by the outgoing controller. A comparable
finding about MA-Q-0014 was checked and refuted, so verify before acting.

1. **Highest priority.** `CLAUDE-FRESH-B3F` reports that `MA-COMPLIANCE-PACKAGING` and the **released**
   questions MA-Q-0169, MA-Q-0202 and MA-Q-0203 assert a Schedule II/III maintenance allowance for
   multi-drug-single-dose packaging that **247 CMR 9.08(3)(b)** (Mass. Register #1536, 12/6/2024)
   prohibits. If confirmed, that is a legal defect in three released questions.
2. `CLAUDE-FRESH-B3E-V3` measured the longest option as the key in 153 of 234 SBA items outside its
   tranche — 65.4% against a 20% baseline. Not a completion blocker under the current gate set, but a
   bank-wide exploitable pattern the per-item detector misses.

## First action

Start by reading the authoritative handoff JSON from GitHub, then mechanically verify live `origin/main`,
the pending audit branches, the exact freeze SHAs and each audit state. Do not perform substantive legal
review until controller and auditor roles are separated.
