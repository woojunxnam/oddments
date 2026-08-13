# Question Authoring Standard

## Source-first authoring

1. Add or update the controlling rule record from an official source.
2. Record an exact section, URL, effective date when available, and verification date.
3. Add material drug data only from authoritative label and legal sources.
4. Write an original scenario from the verified rule. Do not paraphrase recalled or commercial questions.
5. Keep the question `AUDIT_PENDING` until automated QA, independent audit, and adjudication pass.

## Item requirements

- `SBA`: exactly one defensible answer.
- `SATA`: at least one correct answer unless an explicitly signaled zero-answer design is approved; the default is prohibited.
- `ORDERED_RESPONSE`: use only when law or an authoritative procedure fixes a unique sequence. General best-practice chronology is insufficient.
- Every choice needs a distinct rationale that explains why that choice is right or wrong.
- The stem must include every fact needed to select the answer and exclude facts that do not alter the decision.
- Do not use `always`, `never`, `only`, `all`, or `none` as giveaway language without legal necessity.
- Do not make the correct option materially longer, more qualified, or more precise than all distractors.

## Difficulty

- `3`: one meaningful legal determination with modest application.
- `4`: two linked determinations or a realistic exception/interaction.
- `5`: normally at least three meaningful determinations. The `reasoning_steps` array must contain at least three distinct steps.

Length, obscurity, and trivia do not create difficulty.

## Drug content

Use drug data only when it materially changes the legal reasoning. Include concise generic, brand, main indication, federal status, Massachusetts status, MassPAT status when relevant, and the legal consequence being tested. Do not turn explanations into NAPLEX pharmacotherapy reviews.

## Explanation contract

An explanation contains:

- `core_reasoning`: the controlling rule applied to the facts;
- `choice_analysis`: one unique rationale for every option;
- no more than three `related_facts`;
- one `mpje_trap` identifying the precise confusion.

No placeholder, boilerplate block, or broad citation may substitute for reasoning.

## Prohibited content

Do not store Pre-MPJE questions, recalled MPJE questions, leaked questions, NDA-protected material, or paid/commercial question-bank text. This repository is public.

