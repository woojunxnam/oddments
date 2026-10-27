# Daily Refresh and RA-to-pharmacy bridge — 2026-10-27

## Scope

The owner requested quick information cards in the existing integrated notes, explanations suitable for a return from Regulatory Affairs to pharmacy practice, on-demand random topics, and a side navigation control on every public page. This is an additive educational layer, not a new question bank, medical decision engine, pharmacist credential, or independent legal audit.

### Published routes

- `notes/#refresh`: random information cards; next-topic button, deck/topic/text filters, optional conceal-and-reveal, saved cards and self-rated review queue.
- `notes/#refresh/today`: ten cards fixed for the New York calendar day. Pages do not send notifications or perform background monitoring.
- `notes/#return`: seven ordered learning stages and six private preparation checklist items. Stages are not a seven-day qualification program.
- `notes/#glossary`: 45 linked plain-language terms.
- `notes/#refresh/topic/<chapter-id>` and `notes/#refresh/card/<card-id>`: exact topic/card entry.

The notes home contains an on-demand quick-information tile. Chapters link to relevant cards. All five HTML documents, including the generated interactive practice page and complete-notes print edition, load the same route-preserving top/home/cards dock. Desktop shows the side controls; narrow screens use an expandable 44px-target menu. Print hides these controls.

## Content inventory and provenance

**232 cards = 72 authored foundation/workflow cards + 127 exact existing drug-appendix entries + 33 exact chapter summaries/highlights.** This does not mean 232 new clinical guidelines. Each has integrated-note unit IDs, inherited body hashes, inherited review dates, and inherited uncertainty flags. The drug appendix is not an independently rechecked list of currently marketed products or a dosing formulary.

`notes/refresh/guide.json` is the companion authoring source. `scripts/build_refresh.py` creates `site/notes/refresh-data.js` and `refresh-build.json` deterministically. The original `notes/guide.json` and question-bank source bytes are preserved. The build does not relabel inherited October 20–23 sources as freshly verified on October 27.

Explanations distinguish note summaries, teaching synthesis, fictional arithmetic, and narrowly researched official safety education. RA connections are labeled analogies, not claims that RA authorization or batch-release standards substitute for dispensing authority. Three fictional arithmetic cards refresh units/dose/quantity without giving actual patient dosing advice.

Unresolved legal overlaps (including Schedule VI continuity), future implementation dates, and source-access gaps retain their warnings. The default daily set excludes OPEN/date-sensitive/source-gap cards; explicit topic/all-card browsing retains access with warnings. This is not a resolution of those boundaries.

### Narrow external safety additions checked October 27, 2026

1. AHRQ, Use the Teach-Back Method (`https://www.ahrq.gov/health-literacy/improve/precautions/tool5.html`): own-words explanation, show-me, re-explanation. Safety teaching, not a new Massachusetts statutory mandate.
2. AHRQ, Brown Bag Medication Review (`https://www.ahrq.gov/health-literacy/improve/precautions/tool8.html`): actual medication containers/use, OTC/supplements, discrepancies and documentation.
3. FDA, FDA Pharmacists Help You Use Medicines Safely (`https://www.fda.gov/consumers/consumer-updates/fda-pharmacists-help-you-use-medicines-safely`): medicines/allergies, practical administration and access barriers, product-specific advice.

No patient-specific therapy selection, comprehensive interaction database, renal/hepatic dose table, vaccine-season protocol, clinical credentialing, or device skills certification is offered. The return path explicitly directs those activities to current clinical references and supervised employer training. No confidential patient data should be entered.

## Learning behavior and data protection

- The daily set begins with up to three due cards, then prioritizes less-seen foundation material and stage diversity. It is fixed once constructed for the day.
- Random mode shuffles without replacement until the current eligible deck is exhausted; starting another cycle avoids an immediate repeat when possible.
- Self-rating means **again: 1 day, unclear: 3 days, remembered: 7 days**. These fixed intervals are an app choice, not a validated adaptive algorithm, mastery assessment, or pass predictor.
- `oddments.mpje.refresh.v1` stores only card IDs, self-ratings/dates, preferences, saved IDs and checklist IDs in that browser. Existing notes and question-bank namespaces are not overwritten.
- JSON export/import validates size/schema/IDs/dates, rejects malformed schedules and merges without deleting existing saved records. No account, backend, automatic cross-device sync, analytics, or network API is used.
- Storage denial produces an explicit notice and in-session functionality. Keyboard focus, reduced motion, responsive text, safe-area positioning, visible warnings and preserved hash routes are tested.

## Verification

Source/generator tests check counts, IDs, references, inherited flags/dates/hashes, unchanged drug fields, stage coverage, exact deterministic outputs, route additions, all-page dock inclusion and storage isolation. Node tests check New York dates, DST-safe calendar arithmetic, deterministic selection, review grades and import sanitation.

The constrained local runtime permits inline DOM tests but blocks HTTP navigation. Those local checks use **explicitly simulated storage** and are not described as real-origin reload or navigation evidence. The permanent `Refresh cards and site navigation QA` workflow performs actual HTTP navigation, real-origin storage reload, all 232 card renders at 320px, backups, filtering, both themes, the five-page dock and regressions for the existing notes and 2,176-question practice reader.

Actual execution details and run links are recorded separately after hosted checks. No physical iPhone/Android/Safari, independent legal review, formal accessibility conformance, or exam/clinical readiness calibration is claimed.
