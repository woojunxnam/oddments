# Phase 2 Batch B REALISM_REVIEW

## 결론

| Verdict | Count |
|---|---:|
| `KEEP` | 17 |
| `MINOR_EDIT` | 15 |
| `MAJOR_REWRITE` | 8 |
| `DELETE` | 0 |

- `PASS`: 17
- `FAIL`: 23
- realism-failure IDs: `MA-Q-0052`, `MA-Q-0054`, `MA-Q-0058`, `MA-Q-0066`, `MA-Q-0068`, `MA-Q-0073`, `MA-Q-0074`, `MA-Q-0075`, `MA-Q-0076`, `MA-Q-0077`, `MA-Q-0078`, `MA-Q-0079`, `MA-Q-0080`, `MA-Q-0081`, `MA-Q-0082`, `MA-Q-0083`, `MA-Q-0084`, `MA-Q-0085`, `MA-Q-0086`, `MA-Q-0087`, `MA-Q-0088`, `MA-Q-0089`, `MA-Q-0090`

## Bank-level discriminator

공식 [NABP public MPJE sample items](https://nabp.pharmacy/wp-content/uploads/2020/07/MPJE-Sample-Questions.pdf), [pre-2027 competency statements](https://nabp.pharmacy/wp-content/uploads/2020/04/MPJE-Competency-Statements-Sample-Questions.pdf), [current exam preparation page](https://nabp.pharmacy/programs/examinations/mpje/prepare-for-the-exam/)만 style comparator로 사용했다. Protected 또는 recalled item은 사용하지 않았다.

전체 80-item frozen bank에서 stock four-word stem opener는 28개뿐이고, 20개 주요 opener가 cycle로 반복됐다. Choices에는 `if its alternate trigger can be documented`가 8회, `after documenting whether`가 10회, six fixed SATA lead-ins가 합계 129회 나타났다. 이 반복은 item 단위 문법 결함뿐 아니라 `distinct_from_bank`와 `public_style_without_copying` 판정에 반영했다.

## Item-by-item adjudication

| Question_ID | Verdict | Realism_Verdict | Failed criteria | Notes |
|---|---|---|---|---|
| `MA-Q-0051` | `KEEP` | `PASS` | — | MA-CQI-PROGRAM의 trigger를 pharmacy decision에 적용하게 하며, 공식 public MPJE sample의 selected-response 구조와 양립한다. material ambiguity나 bank-level wording leakage를 확인하지 못했다. |
| `MA-Q-0052` | `MINOR_EDIT` | `FAIL` | `authentic_distractors`, `wording_not_guessable`, `distinct_from_bank`, `public_style_without_copying` | distractor에 반복 삽입된 'if its alternate trigger can be documented' 또는 'after documenting whether ...' 문구가 문법과 meaning을 훼손하고 generator template을 노출한다. core legal scenario는 살릴 수 있으나 distractor를 자연스러운 competing rule로 다시 써야 한다. |
| `MA-Q-0053` | `KEEP` | `PASS` | — | MA-QRE-DOCUMENT-24H의 trigger를 pharmacy decision에 적용하게 하며, 공식 public MPJE sample의 selected-response 구조와 양립한다. material ambiguity나 bank-level wording leakage를 확인하지 못했다. |
| `MA-Q-0054` | `MINOR_EDIT` | `FAIL` | `authentic_distractors`, `wording_not_guessable`, `distinct_from_bank`, `public_style_without_copying` | distractor에 반복 삽입된 'if its alternate trigger can be documented' 또는 'after documenting whether ...' 문구가 문법과 meaning을 훼손하고 generator template을 노출한다. core legal scenario는 살릴 수 있으나 distractor를 자연스러운 competing rule로 다시 써야 한다. |
| `MA-Q-0055` | `KEEP` | `PASS` | — | MA-QRE-ANNUAL-ED의 trigger를 pharmacy decision에 적용하게 하며, 공식 public MPJE sample의 selected-response 구조와 양립한다. material ambiguity나 bank-level wording leakage를 확인하지 못했다. |
| `MA-Q-0056` | `KEEP` | `PASS` | — | MA-SERIOUS-EVENT-REPORT의 trigger를 pharmacy decision에 적용하게 하며, 공식 public MPJE sample의 selected-response 구조와 양립한다. material ambiguity나 bank-level wording leakage를 확인하지 못했다. |
| `MA-Q-0057` | `KEEP` | `PASS` | — | MA-SERIOUS-EVENT-RECORDS의 trigger를 pharmacy decision에 적용하게 하며, 공식 public MPJE sample의 selected-response 구조와 양립한다. material ambiguity나 bank-level wording leakage를 확인하지 못했다. |
| `MA-Q-0058` | `MINOR_EDIT` | `FAIL` | `authentic_distractors`, `wording_not_guessable`, `distinct_from_bank`, `public_style_without_copying` | distractor에 반복 삽입된 'if its alternate trigger can be documented' 또는 'after documenting whether ...' 문구가 문법과 meaning을 훼손하고 generator template을 노출한다. core legal scenario는 살릴 수 있으나 distractor를 자연스러운 competing rule로 다시 써야 한다. |
| `MA-Q-0059` | `KEEP` | `PASS` | — | FED-INVENTORY-INITIAL의 trigger를 pharmacy decision에 적용하게 하며, 공식 public MPJE sample의 selected-response 구조와 양립한다. material ambiguity나 bank-level wording leakage를 확인하지 못했다. |
| `MA-Q-0060` | `KEEP` | `PASS` | — | FED-INVENTORY-BIENNIAL의 trigger를 pharmacy decision에 적용하게 하며, 공식 public MPJE sample의 selected-response 구조와 양립한다. material ambiguity나 bank-level wording leakage를 확인하지 못했다. |
| `MA-Q-0061` | `KEEP` | `PASS` | — | FED-INVENTORY-COUNT의 trigger를 pharmacy decision에 적용하게 하며, 공식 public MPJE sample의 selected-response 구조와 양립한다. material ambiguity나 bank-level wording leakage를 확인하지 못했다. |
| `MA-Q-0062` | `KEEP` | `PASS` | — | FED-CS-RECORDS-2Y의 trigger를 pharmacy decision에 적용하게 하며, 공식 public MPJE sample의 selected-response 구조와 양립한다. material ambiguity나 bank-level wording leakage를 확인하지 못했다. |
| `MA-Q-0063` | `KEEP` | `PASS` | — | FED-FORM222-ORDER의 trigger를 pharmacy decision에 적용하게 하며, 공식 public MPJE sample의 selected-response 구조와 양립한다. material ambiguity나 bank-level wording leakage를 확인하지 못했다. |
| `MA-Q-0064` | `KEEP` | `PASS` | — | FED-FORM222-60DAY의 trigger를 pharmacy decision에 적용하게 하며, 공식 public MPJE sample의 selected-response 구조와 양립한다. material ambiguity나 bank-level wording leakage를 확인하지 못했다. |
| `MA-Q-0065` | `KEEP` | `PASS` | — | FED-FORM222-DEFECT의 trigger를 pharmacy decision에 적용하게 하며, 공식 public MPJE sample의 selected-response 구조와 양립한다. material ambiguity나 bank-level wording leakage를 확인하지 못했다. |
| `MA-Q-0066` | `MINOR_EDIT` | `FAIL` | `authentic_distractors`, `wording_not_guessable`, `distinct_from_bank`, `public_style_without_copying` | distractor에 반복 삽입된 'if its alternate trigger can be documented' 또는 'after documenting whether ...' 문구가 문법과 meaning을 훼손하고 generator template을 노출한다. core legal scenario는 살릴 수 있으나 distractor를 자연스러운 competing rule로 다시 써야 한다. |
| `MA-Q-0067` | `KEEP` | `PASS` | — | FED-FORM222-RECORDS의 trigger를 pharmacy decision에 적용하게 하며, 공식 public MPJE sample의 selected-response 구조와 양립한다. material ambiguity나 bank-level wording leakage를 확인하지 못했다. |
| `MA-Q-0068` | `MINOR_EDIT` | `FAIL` | `authentic_distractors`, `wording_not_guessable`, `distinct_from_bank`, `public_style_without_copying` | distractor에 반복 삽입된 'if its alternate trigger can be documented' 또는 'after documenting whether ...' 문구가 문법과 meaning을 훼손하고 generator template을 노출한다. core legal scenario는 살릴 수 있으나 distractor를 자연스러운 competing rule로 다시 써야 한다. |
| `MA-Q-0069` | `KEEP` | `PASS` | — | FED-FORM41의 trigger를 pharmacy decision에 적용하게 하며, 공식 public MPJE sample의 selected-response 구조와 양립한다. material ambiguity나 bank-level wording leakage를 확인하지 못했다. |
| `MA-Q-0070` | `KEEP` | `PASS` | — | FED-DISPOSAL-NONRETRIEVABLE의 trigger를 pharmacy decision에 적용하게 하며, 공식 public MPJE sample의 selected-response 구조와 양립한다. material ambiguity나 bank-level wording leakage를 확인하지 못했다. |
| `MA-Q-0071` | `KEEP` | `PASS` | — | FED-REVERSE-DISTRIBUTOR의 trigger를 pharmacy decision에 적용하게 하며, 공식 public MPJE sample의 selected-response 구조와 양립한다. material ambiguity나 bank-level wording leakage를 확인하지 못했다. |
| `MA-Q-0072` | `KEEP` | `PASS` | — | MA-PHARMACY-CLOSURE-NOTICE의 trigger를 pharmacy decision에 적용하게 하며, 공식 public MPJE sample의 selected-response 구조와 양립한다. material ambiguity나 bank-level wording leakage를 확인하지 못했다. |
| `MA-Q-0073` | `MAJOR_REWRITE` | `FAIL` | `jurisprudence_reasoning`, `authentic_distractors`, `wording_not_guessable`, `reasoning_not_trivia`, `natural_rule_combination`, `distinct_from_bank`, `public_style_without_copying` | 고정 position lead-ins뿐 아니라 options가 구체적 task 없이 rule을 재진술하거나 tautology로 구성되어 있다. candidate가 실제 pharmacy fact를 비교하지 않아도 문장 tone만으로 답을 고를 수 있으므로 scenario와 distractor를 전면 재작성해야 한다. option D의 subject-verb 오류('transfers is required')도 의미를 훼손한다. |
| `MA-Q-0074` | `MINOR_EDIT` | `FAIL` | `authentic_distractors`, `wording_not_guessable`, `distinct_from_bank`, `public_style_without_copying` | 법적 scenario는 usable하지만 options가 bank 전반의 고정 position lead-ins를 반복한다. lead-ins를 제거하고 distractor마다 실제 competing legal premise를 부여해야 public MPJE-like item으로 보인다. |
| `MA-Q-0075` | `MAJOR_REWRITE` | `FAIL` | `jurisprudence_reasoning`, `authentic_distractors`, `wording_not_guessable`, `reasoning_not_trivia`, `natural_rule_combination`, `distinct_from_bank`, `public_style_without_copying` | 고정 position lead-ins뿐 아니라 options가 구체적 task 없이 rule을 재진술하거나 tautology로 구성되어 있다. candidate가 실제 pharmacy fact를 비교하지 않아도 문장 tone만으로 답을 고를 수 있으므로 scenario와 distractor를 전면 재작성해야 한다. |
| `MA-Q-0076` | `MAJOR_REWRITE` | `FAIL` | `jurisprudence_reasoning`, `authentic_distractors`, `wording_not_guessable`, `reasoning_not_trivia`, `natural_rule_combination`, `distinct_from_bank`, `public_style_without_copying` | 고정 position lead-ins뿐 아니라 options가 구체적 task 없이 rule을 재진술하거나 tautology로 구성되어 있다. candidate가 실제 pharmacy fact를 비교하지 않아도 문장 tone만으로 답을 고를 수 있으므로 scenario와 distractor를 전면 재작성해야 한다. |
| `MA-Q-0077` | `MINOR_EDIT` | `FAIL` | `authentic_distractors`, `wording_not_guessable`, `distinct_from_bank`, `public_style_without_copying` | 법적 scenario는 usable하지만 options가 bank 전반의 고정 position lead-ins를 반복한다. lead-ins를 제거하고 distractor마다 실제 competing legal premise를 부여해야 public MPJE-like item으로 보인다. |
| `MA-Q-0078` | `MINOR_EDIT` | `FAIL` | `authentic_distractors`, `wording_not_guessable`, `distinct_from_bank`, `public_style_without_copying` | 법적 scenario는 usable하지만 options가 bank 전반의 고정 position lead-ins를 반복한다. lead-ins를 제거하고 distractor마다 실제 competing legal premise를 부여해야 public MPJE-like item으로 보인다. |
| `MA-Q-0079` | `MINOR_EDIT` | `FAIL` | `authentic_distractors`, `wording_not_guessable`, `distinct_from_bank`, `public_style_without_copying` | 법적 scenario는 usable하지만 options가 bank 전반의 고정 position lead-ins를 반복한다. lead-ins를 제거하고 distractor마다 실제 competing legal premise를 부여해야 public MPJE-like item으로 보인다. |
| `MA-Q-0080` | `MINOR_EDIT` | `FAIL` | `authentic_distractors`, `wording_not_guessable`, `distinct_from_bank`, `public_style_without_copying` | 법적 scenario는 usable하지만 options가 bank 전반의 고정 position lead-ins를 반복한다. lead-ins를 제거하고 distractor마다 실제 competing legal premise를 부여해야 public MPJE-like item으로 보인다. |
| `MA-Q-0081` | `MAJOR_REWRITE` | `FAIL` | `jurisprudence_reasoning`, `authentic_distractors`, `wording_not_guessable`, `reasoning_not_trivia`, `natural_rule_combination`, `distinct_from_bank`, `public_style_without_copying` | 고정 position lead-ins뿐 아니라 options가 구체적 task 없이 rule을 재진술하거나 tautology로 구성되어 있다. candidate가 실제 pharmacy fact를 비교하지 않아도 문장 tone만으로 답을 고를 수 있으므로 scenario와 distractor를 전면 재작성해야 한다. option B는 current 247 CMR 16.02 qualification을 충분히 표현하지 못한다. |
| `MA-Q-0082` | `MAJOR_REWRITE` | `FAIL` | `jurisprudence_reasoning`, `authentic_distractors`, `wording_not_guessable`, `reasoning_not_trivia`, `natural_rule_combination`, `distinct_from_bank`, `public_style_without_copying` | 고정 position lead-ins뿐 아니라 options가 구체적 task 없이 rule을 재진술하거나 tautology로 구성되어 있다. candidate가 실제 pharmacy fact를 비교하지 않아도 문장 tone만으로 답을 고를 수 있으므로 scenario와 distractor를 전면 재작성해야 한다. |
| `MA-Q-0083` | `MINOR_EDIT` | `FAIL` | `authentic_distractors`, `wording_not_guessable`, `distinct_from_bank`, `public_style_without_copying` | 법적 scenario는 usable하지만 options가 bank 전반의 고정 position lead-ins를 반복한다. lead-ins를 제거하고 distractor마다 실제 competing legal premise를 부여해야 public MPJE-like item으로 보인다. |
| `MA-Q-0084` | `MAJOR_REWRITE` | `FAIL` | `jurisprudence_reasoning`, `authentic_distractors`, `wording_not_guessable`, `reasoning_not_trivia`, `natural_rule_combination`, `distinct_from_bank`, `public_style_without_copying` | 고정 position lead-ins뿐 아니라 options가 구체적 task 없이 rule을 재진술하거나 tautology로 구성되어 있다. candidate가 실제 pharmacy fact를 비교하지 않아도 문장 tone만으로 답을 고를 수 있으므로 scenario와 distractor를 전면 재작성해야 한다. option E의 'patient-specific collaborative workflow'는 legally testable action이 아니라 vague label이다. |
| `MA-Q-0085` | `MAJOR_REWRITE` | `FAIL` | `jurisprudence_reasoning`, `authentic_distractors`, `wording_not_guessable`, `reasoning_not_trivia`, `natural_rule_combination`, `distinct_from_bank`, `public_style_without_copying` | 고정 position lead-ins뿐 아니라 options가 구체적 task 없이 rule을 재진술하거나 tautology로 구성되어 있다. candidate가 실제 pharmacy fact를 비교하지 않아도 문장 tone만으로 답을 고를 수 있으므로 scenario와 distractor를 전면 재작성해야 한다. |
| `MA-Q-0086` | `MAJOR_REWRITE` | `FAIL` | `jurisprudence_reasoning`, `authentic_distractors`, `wording_not_guessable`, `reasoning_not_trivia`, `natural_rule_combination`, `distinct_from_bank`, `public_style_without_copying` | 고정 position lead-ins뿐 아니라 options가 구체적 task 없이 rule을 재진술하거나 tautology로 구성되어 있다. candidate가 실제 pharmacy fact를 비교하지 않아도 문장 tone만으로 답을 고를 수 있으므로 scenario와 distractor를 전면 재작성해야 한다. |
| `MA-Q-0087` | `MINOR_EDIT` | `FAIL` | `authentic_distractors`, `wording_not_guessable`, `distinct_from_bank`, `public_style_without_copying` | 법적 scenario는 usable하지만 options가 bank 전반의 고정 position lead-ins를 반복한다. lead-ins를 제거하고 distractor마다 실제 competing legal premise를 부여해야 public MPJE-like item으로 보인다. |
| `MA-Q-0088` | `MINOR_EDIT` | `FAIL` | `authentic_distractors`, `wording_not_guessable`, `distinct_from_bank`, `public_style_without_copying` | 법적 scenario는 usable하지만 options가 bank 전반의 고정 position lead-ins를 반복한다. lead-ins를 제거하고 distractor마다 실제 competing legal premise를 부여해야 public MPJE-like item으로 보인다. |
| `MA-Q-0089` | `MINOR_EDIT` | `FAIL` | `authentic_distractors`, `wording_not_guessable`, `distinct_from_bank`, `public_style_without_copying` | 법적 scenario는 usable하지만 options가 bank 전반의 고정 position lead-ins를 반복한다. lead-ins를 제거하고 distractor마다 실제 competing legal premise를 부여해야 public MPJE-like item으로 보인다. |
| `MA-Q-0090` | `MINOR_EDIT` | `FAIL` | `authentic_distractors`, `wording_not_guessable`, `distinct_from_bank`, `public_style_without_copying` | 법적 scenario는 usable하지만 options가 bank 전반의 고정 position lead-ins를 반복한다. lead-ins를 제거하고 distractor마다 실제 competing legal premise를 부여해야 public MPJE-like item으로 보인다. |

## 판정 원칙

`PASS`는 schema의 10 criteria가 모두 true일 때만 부여했다. Legal key가 맞더라도 schedule-only flashcard, implausible workflow, vague proposition, generator phrase, position-based SATA lead-in, bank-level near-template이면 `FAIL`로 판정했다. Canonical item은 수정하지 않았다.
