# Pre-Batch3 T1 full-gate diagnostic

HEAD: 285b39cd605b1ac2297f4a5311bbe27d11cb9211

## preflight
```
preflight PASS: 29 admission candidates; Q0028 quarantined; preview count 167
```
exit_code: 0

## apply
```
guarded T1 admission applied: 29 RELEASED; Q0028 quarantined; preview 167 -> 180 (added 14, removed 1)
```
exit_code: 0

## generate
```
generated duplicate_report.json
generated answer_distribution_report.json
generated structural_pattern_report.json
generated site/generated/questions.json
```
exit_code: 0

## post_verify
```
post-release guard PASS: 29 T1 RELEASED; Q0028 quarantined; preview count 180
```
exit_code: 0

## validate
```
WARNING [all] MA-Q-0190: correct option is materially longer than distractors
ERROR [all] /home/runner/work/oddments/oddments/data/questions/ma-q-0079.json: current realism audit AUDIT-GPT-PHASE2-V3-REALISM-REAUDIT-2026-08-13-B does not pass
ERROR [all] /home/runner/work/oddments/oddments/data/questions/ma-q-0082.json: current realism audit AUDIT-GPT-PHASE2-V3-REALISM-REAUDIT-2026-08-13-B does not pass
ERROR [all] /home/runner/work/oddments/oddments/data/questions/ma-q-0083.json: current realism audit AUDIT-GPT-PHASE2-V3-REALISM-REAUDIT-2026-08-13-B does not pass
ERROR [all] /home/runner/work/oddments/oddments/data/questions/ma-q-0084.json: current legal audit AUDIT-GPT-PHASE2-V3-LEGAL-REAUDIT-2026-08-13-B does not independently pass
ERROR [all] /home/runner/work/oddments/oddments/data/questions/ma-q-0084.json: current realism audit AUDIT-GPT-PHASE2-V3-REALISM-REAUDIT-2026-08-13-B does not pass
all: 5 error(s), 1 warning(s)
```
exit_code: 1

overall_exit_code: 1
